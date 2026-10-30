const { test } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { resolveVersion, token, listVersions, applyVersion } = require('./resolve_build_version.cjs');

const version = (v, state = 'READY_FOR_DISTRIBUTION', platform = 'IOS') => ({
  attributes: { versionString: v, appVersionState: state, platform },
});
const response = (data, next) => ({ ok: true, status: 200, json: async () => ({ data, links: { next } }) });
const app = { id: 'example-id', attributes: { bundleId: 'com.safa.cae' } };

test('observed Apple rejections advance the marketing version numerically', () => {
  assert.equal(resolveVersion('1.2.9', [version('1.2.9')]).version, '1.2.10');
  assert.equal(resolveVersion('1.2.10', [version('1.2.10')]).version, '1.2.11');
  assert.equal(resolveVersion('1.2.11', [version('1.2.11')]).version, '1.2.12');
  assert.equal(resolveVersion('1.2.9', [version('1.2.10'), version('1.2.8')]).version, '1.2.11');
});
test('a newer configured version is retained; another platform does not change iOS', () => {
  assert.equal(resolveVersion('1.3.0', [version('1.2.11'), version('9.0', 'READY_FOR_SALE', 'MAC_OS')]).version, '1.3.0');
  assert.equal(resolveVersion('1.0.0', []).version, '1.0.0');
});
test('submitted and approved-but-unreleased versions cannot become a race during compilation', () => {
  for (const state of ['IN_REVIEW', 'WAITING_FOR_REVIEW', 'ACCEPTED', 'PENDING_DEVELOPER_RELEASE', 'PROCESSING_FOR_DISTRIBUTION']) {
    assert.equal(resolveVersion('1.2.11', [version('1.2.11', state)]).version, '1.2.12');
  }
});
test('an editable draft can still receive more TestFlight builds', () => {
  assert.equal(resolveVersion('1.2.11', [version('1.2.10'), version('1.2.11', 'PREPARE_FOR_SUBMISSION')]).version, '1.2.11');
});
test('legacy state and two-part versions work; unknown or corrupt data stops the build', () => {
  assert.equal(resolveVersion('1.2', [{ attributes: { versionString: '1.2', platform: 'IOS', appStoreState: 'READY_FOR_SALE' } }]).version, '1.2.1');
  assert.throws(() => resolveVersion('1.2.11', [version('1.2.11', 'NEW_UNKNOWN_STATE')]));
  assert.throws(() => resolveVersion('1.2.11', [{}]));
  assert.throws(() => resolveVersion('1.2.11-beta', []));
});
test('all version pages are read, without relying on sort order', async () => {
  const seen = [];
  const fetch = async url => {
    seen.push(url);
    if (seen.length === 1) return response([app]);
    if (seen.length === 2) return response([version('1.2.9')], 'https://api.appstoreconnect.apple.com/v1/pages/2');
    return response([version('1.2.11')]);
  };
  const versions = await listVersions('com.safa.cae', 'test-token', fetch);
  assert.equal(resolveVersion('1.2.10', versions).version, '1.2.12');
  assert.equal(seen.length, 3);
  assert.equal(new URL(seen[0]).searchParams.get('filter[bundleId]'), 'com.safa.cae');
});
test('Apple auth failure or an unidentified app never falls back to the saved version', async () => {
  await assert.rejects(listVersions('com.safa.cae', 'test', async () => ({ ok: false, status: 403 })), /HTTP 403/);
  await assert.rejects(listVersions('com.safa.cae', 'test', async () => response([])), /uniquely/);
});
test('rate limiting retries are bounded', async () => {
  let calls = 0;
  const fetch = async () => {
    calls++;
    if (calls <= 2) return { ok: false, status: 429 };
    return calls === 3 ? response([app]) : response([]);
  };
  assert.deepEqual(await listVersions('com.safa.cae', 'test', fetch, async () => {}), []);
  assert.equal(calls, 4);
  calls = 0;
  await assert.rejects(listVersions('com.safa.cae', 'test', async () => { calls++; return { ok: false, status: 503 }; }, async () => {}), /HTTP 503/);
  assert.equal(calls, 3);
});
test('pagination cannot send the signing token to another host', async () => {
  let calls = 0;
  const fetch = async () => ++calls === 1 ? response([app]) : response([], 'https://example.com/steal');
  await assert.rejects(listVersions('com.safa.cae', 'test', fetch), /pagination URL/);
  assert.equal(calls, 2);
});
test('JWT uses ES256 with a short lifetime and the existing credential format', () => {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
  const pem = privateKey.export({ type: 'pkcs8', format: 'pem' });
  const jwt = token({ APP_STORE_CONNECT_KEY_ID: ' KEYID\n', APP_STORE_CONNECT_ISSUER_ID: 'issuer', APP_STORE_CONNECT_API_KEY_BASE64: Buffer.from(pem).toString('base64') }, 1000);
  const [header, payload, sig] = jwt.split('.');
  assert.equal(JSON.parse(Buffer.from(header, 'base64url')).alg, 'ES256');
  assert.deepEqual(JSON.parse(Buffer.from(payload, 'base64url')), { iss: 'issuer', iat: 1000, exp: 1600, aud: 'appstoreconnect-v1' });
  assert.ok(crypto.verify('sha256', Buffer.from(header + '.' + payload), { key: publicKey, dsaEncoding: 'ieee-p1363' }, Buffer.from(sig, 'base64url')));
  assert.throws(() => token({}), /credentials/);
});
test('applying the shared version changes only expo.version', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cae-version-'));
  const file = path.join(dir, 'app.json');
  const config = { expo: { version: '1.2.9', runtimeVersion: '1.0.0', ios: { bundleIdentifier: 'com.safa.cae' } } };
  try {
    fs.writeFileSync(file, JSON.stringify(config));
    applyVersion(file, '1.2.12');
    config.expo.version = '1.2.12';
    assert.deepEqual(JSON.parse(fs.readFileSync(file)), config);
    assert.throws(() => applyVersion(file, undefined));
  } finally { fs.unlinkSync(file); fs.rmdirSync(dir); }
});
test('CI command fails without Apple access and emits no fallback version or credentials', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cae-version-cli-'));
  const file = path.join(dir, 'app.json'), output = path.join(dir, 'output');
  const command = path.resolve(__dirname, 'resolve_build_version.cjs');
  try {
    fs.writeFileSync(file, JSON.stringify({ expo: { version: '1.2.11', ios: { bundleIdentifier: 'com.safa.cae' } } }));
    const env = { ...process.env, CHECK_APPLE: 'true', GITHUB_OUTPUT: output,
      APP_STORE_CONNECT_KEY_ID: 'private-marker', APP_STORE_CONNECT_ISSUER_ID: '', APP_STORE_CONNECT_API_KEY_BASE64: '' };
    const blocked = spawnSync(process.execPath, [command], { cwd: dir, env, encoding: 'utf8' });
    assert.notEqual(blocked.status, 0);
    assert.ok(!fs.existsSync(output));
    assert.ok(!blocked.stdout.includes('private-marker') && !blocked.stderr.includes('private-marker'));
    const applied = spawnSync(process.execPath, [command, '--apply'], { cwd: dir,
      env: { ...env, RESOLVED_APP_VERSION: '1.2.12' }, encoding: 'utf8' });
    assert.equal(applied.status, 0);
    assert.equal(JSON.parse(fs.readFileSync(file)).expo.version, '1.2.12');
  } finally { fs.unlinkSync(file); fs.rmdirSync(dir); }
});
