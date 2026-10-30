// Shared CI preflight. Uses the existing App Store Connect secrets, without writing keys to disk.
const crypto = require('node:crypto');
const fs = require('node:fs');
const API = 'https://api.appstoreconnect.apple.com';

// Submitted versions may become approved while the native build is running.
const RESERVED = new Set([
  'ACCEPTED', 'READY_FOR_DISTRIBUTION', 'READY_FOR_SALE',
  'PENDING_DEVELOPER_RELEASE', 'PENDING_APPLE_RELEASE', 'PENDING_CONTRACT',
  'PREORDER_READY_FOR_SALE', 'PROCESSING_FOR_APP_STORE', 'PROCESSING_FOR_DISTRIBUTION',
  'DEVELOPER_REMOVED_FROM_SALE', 'REMOVED_FROM_SALE', 'REPLACED_WITH_NEW_VERSION',
  'IN_REVIEW', 'WAITING_FOR_REVIEW', 'WAITING_FOR_EXPORT_COMPLIANCE',
]);
const OPEN = new Set([
  'PREPARE_FOR_SUBMISSION', 'READY_FOR_REVIEW', 'DEVELOPER_REJECTED',
  'REJECTED', 'METADATA_REJECTED', 'INVALID_BINARY',
]);

function parts(version) {
  if (typeof version !== 'string' || !/^\d+(?:\.\d+){0,2}$/.test(version)) {
    throw Error('Invalid numeric app version');
  }
  const values = version.split('.').map(Number);
  if (!values.every(Number.isSafeInteger)) throw Error('App version is out of range');
  return [...values, 0, 0].slice(0, 3);
}
function compare(a, b) {
  const x = parts(a), y = parts(b);
  return x[0] - y[0] || x[1] - y[1] || x[2] - y[2];
}
function resolveVersion(configured, versions) {
  parts(configured);
  let floor = null;
  for (const version of versions) {
    const a = version.attributes;
    if (!a || !a.platform) throw Error('Apple returned an incomplete version record');
    if (a.platform !== 'IOS') continue;
    parts(a.versionString);
    const state = a.appVersionState ?? a.appStoreState;
    if (!RESERVED.has(state) && !OPEN.has(state)) throw Error('Unknown Apple version state');
    if (RESERVED.has(state) && (floor === null || compare(a.versionString, floor) > 0)) {
      floor = a.versionString;
    }
  }
  let version = configured;
  if (floor !== null && compare(configured, floor) <= 0) {
    const values = parts(floor);
    values[2]++;
    version = values.join('.');
    parts(version);
  }
  return { version, floor };
}

function token(env, now = Math.floor(Date.now() / 1000)) {
  const kid = (env.APP_STORE_CONNECT_KEY_ID ?? '').replace(/\s/g, '');
  const iss = (env.APP_STORE_CONNECT_ISSUER_ID ?? '').replace(/\s/g, '');
  const encoded = (env.APP_STORE_CONNECT_API_KEY_BASE64 ?? '').replace(/\s/g, '');
  if (!kid || !iss || !encoded) throw Error('App Store Connect credentials are missing');
  const key = crypto.createPrivateKey(Buffer.from(encoded, 'base64').toString('utf8'));
  const encode = value => Buffer.from(JSON.stringify(value)).toString('base64url');
  const data = encode({ alg: 'ES256', kid, typ: 'JWT' }) + '.'
    + encode({ iss, iat: now, exp: now + 600, aud: 'appstoreconnect-v1' });
  return data + '.' + crypto.sign('sha256', Buffer.from(data), { key, dsaEncoding: 'ieee-p1363' }).toString('base64url');
}

async function listVersions(bundleId, jwt, fetchImpl = fetch, pause = ms => new Promise(r => setTimeout(r, ms))) {
  async function request(input) {
    const url = new URL(input, API);
    if (url.origin !== API) throw Error('Invalid Apple pagination URL');
    for (let attempt = 0; attempt < 3; attempt++) {
      let response;
      try {
        response = await fetchImpl(url.href, {
          headers: { Authorization: 'Bearer ' + jwt },
          signal: AbortSignal.timeout(15000), redirect: 'error',
        });
      } catch { throw Error('App Store Connect lookup failed; native build was not started'); }
      if ((response.status === 429 || response.status >= 500) && attempt < 2) {
        await pause(500 * (attempt + 1));
        continue;
      }
      if (!response.ok) throw Error('App Store Connect lookup failed (HTTP ' + response.status + ')');
      const body = await response.json();
      if (!Array.isArray(body.data)) throw Error('Invalid App Store Connect response');
      return body;
    }
  }
  const appQuery = new URL('/v1/apps', API);
  appQuery.search = new URLSearchParams({ 'filter[bundleId]': bundleId, 'fields[apps]': 'bundleId', limit: '2' });
  const apps = await request(appQuery.href);
  if (apps.data.length !== 1 || apps.data[0].attributes?.bundleId !== bundleId) {
    throw Error('Could not uniquely identify the app in App Store Connect');
  }
  const first = new URL('/v1/apps/' + encodeURIComponent(apps.data[0].id) + '/appStoreVersions', API);
  first.search = new URLSearchParams({
    'filter[platform]': 'IOS', limit: '200',
    'fields[appStoreVersions]': 'platform,versionString,appStoreState,appVersionState',
  });
  const versions = [], seen = new Set();
  let next = first.href;
  while (next) {
    if (seen.has(next) || seen.size >= 100) throw Error('Invalid Apple pagination');
    seen.add(next);
    const body = await request(next);
    versions.push(...body.data);
    next = body.links?.next;
  }
  return versions;
}

function applyVersion(path, version) {
  parts(version);
  const app = JSON.parse(fs.readFileSync(path, 'utf8'));
  app.expo.version = version;
  fs.writeFileSync(path, JSON.stringify(app, null, 2) + '\n');
}

async function main() {
  if (process.argv.includes('--apply')) {
    applyVersion('app.json', process.env.RESOLVED_APP_VERSION);
    return;
  }
  const app = JSON.parse(fs.readFileSync('app.json', 'utf8'));
  const configured = app.expo.version;
  const check = process.env.CHECK_APPLE === 'true';
  if (!['true', 'false'].includes(process.env.CHECK_APPLE)) throw Error('CHECK_APPLE must be explicitly set');
  const versions = check ? await listVersions(app.expo.ios.bundleIdentifier, token(process.env)) : [];
  const result = resolveVersion(configured, versions);
  if (!process.env.GITHUB_OUTPUT) throw Error('CI output destination is missing');
  fs.appendFileSync(process.env.GITHUB_OUTPUT, 'app_version=' + result.version + '\n');
  const message = 'App version: ' + configured + ' -> ' + result.version
    + (check ? ' (Apple reserved floor: ' + (result.floor ?? 'none') + ')' : ' (no iOS submission)');
  console.log(message); // Never log the token, credentials or raw API response.
  if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, message + '\n');
}

module.exports = { parts, compare, resolveVersion, token, listVersions, applyVersion };
if (require.main === module) main().catch(() => {
  console.error('::error::Version preflight failed. Check Apple API access, credentials and version data. Native builds were not started.');
  process.exitCode = 1;
});
