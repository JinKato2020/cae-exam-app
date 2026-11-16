// Run: node tools/test_content_ota.cjs
// Reproduce Android's file-URI decoding at the native boundary; no network/device required.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { build } = require('esbuild');

async function main() {
  const root = path.resolve(__dirname, '..');
  const disk = new Map();
  let iosCache = false;
  const nativePath = uri => iosCache ? new URL(uri).pathname : decodeURIComponent(new URL(uri).pathname);
  const dir = '/docs/cae-content/';
  const contentKey = 'content/questions/thermal2-01-math-basics.json';
  const figureKey = 'figures/example.png';
  let downloads = 0;
  let failFigure = true;
  let revision = 'new';
  const payload = () => JSON.stringify({ questions: [{ easyExplanation: [{ title: '例', body: revision }] }] });
  const fsMock = {
    documentDirectory: 'file:///docs/', cacheDirectory: 'file:///cache/',
    async getInfoAsync(uri) { return { exists: disk.has(nativePath(uri)) }; },
    async makeDirectoryAsync(uri) { disk.set(nativePath(uri), null); },
    async deleteAsync(uri) {
      const p = nativePath(uri);
      for (const k of [...disk.keys()]) if (k === p || k.startsWith(p.endsWith('/') ? p : p + '/')) disk.delete(k);
    },
    async moveAsync() { throw Error('no old directory'); },
    async readAsStringAsync(uri) { const p = nativePath(uri); if (!disk.has(p)) throw Error('missing'); return disk.get(p); },
    async writeAsStringAsync(uri, text) { disk.set(nativePath(uri), text); },
    async readDirectoryAsync(uri) {
      const p = nativePath(uri);
      return [...disk.keys()].filter(k => k.startsWith(p) && k !== p && !k.slice(p.length).includes('/')).map(k => k.slice(p.length));
    },
    async downloadAsync(url, uri) {
      downloads++;
      const p = nativePath(uri);
      // Legacy content%2Fquestions%2F... becomes nested paths and fails here on Android.
      if (!disk.has(p.slice(0, p.lastIndexOf('/') + 1))) throw Error('parent directory missing');
      if (url.includes(figureKey) && failFigure) return { status: 503 };
      disk.set(p, url.includes(contentKey) ? payload() : 'PNG');
      return { status: 200 };
    },
  };
  const code = (await build({
    entryPoints: [path.join(root, 'src/data/contentOta.ts')], bundle: true,
    platform: 'node', format: 'cjs', write: false,
    plugins: [{ name: 'native-boundary', setup(b) {
      b.onResolve({ filter: /^expo-file-system\/legacy$/ }, () => ({ path: 'filesystem', namespace: 'test' }));
      b.onLoad({ filter: /.*/, namespace: 'test' }, () => ({ contents: 'module.exports = globalThis.__otaFsMock;' }));
      b.onLoad({ filter: /[\\/]content[\\/]_manifest\.json$/ }, () => ({ contents: '{"files":{"content/bundled.json":{"sha256":"bundled"}}}', loader: 'json' }));
    } }],
  })).outputFiles[0].text;
  const oldFetch = globalThis.fetch;
  globalThis.__otaFsMock = fsMock;
  globalThis.fetch = async () => ({ ok: true, text: async () => JSON.stringify({ files: {
    [contentKey]: { sha256: revision }, [figureKey]: { sha256: 'image' },
  } }) });
  try {
    const mod = { exports: {} };
    new Function('module', 'exports', code)(mod, mod.exports);
    const { syncContent, loadCache } = mod.exports;
    assert.deepEqual(await syncContent(), { updated: 1 });
    assert.equal((await loadCache()).content[contentKey].questions[0].easyExplanation[0].body, 'new');
    failFigure = false;
    assert.deepEqual(await syncContent(), { updated: 1 }); // Resume only the interrupted image.
    assert.ok((await loadCache()).figures.example.startsWith('file:///docs/cae-content/v2-'));
    const before = downloads;
    assert.deepEqual(await syncContent(), { updated: 0 });
    assert.equal(downloads, before);
    revision = 'revised';
    assert.deepEqual(await syncContent(), { updated: 1 });
    assert.equal((await loadCache()).content[contentKey].questions[0].easyExplanation[0].body, 'revised');
    assert.ok([...disk.keys()].filter(k => k !== dir).every(k => !k.slice(dir.length).includes('/')));
    // iOS can retain both the legacy filename and v2 filename for one chapter.
    // The old chapter must never overwrite the new chapter just because it is listed last.
    const tag = disk.get(dir + '_bundle.tag');
    const chapterKey = 'content/questions/solid1-09-numerical-analysis.json';
    const latest = JSON.parse(fs.readFileSync(path.join(root, chapterKey), 'utf8'));
    const legacy = { ...latest, questions: latest.questions.map(q => {
      const old = { ...q }; delete old.easyExplanation;
      if (old.number === '9-1') { old.figure = 'none'; delete old.figureImage; }
      return old;
    }) };
    const legacyName = encodeURIComponent(chapterKey);
    const currentName = 'v2-' + legacyName.replace(/~/g, '%7E').replace(/%/g, '~');
    iosCache = true;
    for (const order of [[currentName, legacyName], [legacyName, currentName], [legacyName]]) {
      disk.clear(); disk.set(dir, null);
      disk.set(dir + '_bundle.tag', tag);
      disk.set(dir + '_shas.json', JSON.stringify({ [chapterKey]: 'chapter9-latest' }));
      for (const name of order) disk.set(dir + name, JSON.stringify(name === currentName ? latest : legacy));
      const chapter = (await loadCache()).content[chapterKey];
      const expected = order.includes(currentName) ? latest : legacy;
      assert.deepEqual(chapter, expected, 'iOS cache must prefer v2 regardless of directory order');
    }
    // Successful sync removes retired, untracked, duplicate and bundled-identical files only.
    disk.clear(); disk.set(dir, null); iosCache = true;
    const file = key => dir + 'v2-' + encodeURIComponent(key).replace(/~/g, '%7E').replace(/%/g, '~');
    disk.set(dir + '_bundle.tag', tag);
    disk.set(dir + '_shas.json', JSON.stringify({
      [contentKey]: revision, [figureKey]: 'image',
      'figures/retired.png': 'old', 'content/bundled.json': 'bundled',
    }));
    disk.set(file(contentKey), payload()); disk.set(file(figureKey), 'PNG');
    disk.set(dir + encodeURIComponent(contentKey), 'old duplicate');
    disk.set(file('figures/retired.png'), 'old image');
    disk.set(file('figures/untracked.png'), 'abandoned download');
    disk.set(file('content/bundled.json'), '{}');
    disk.set('/cache/cae-content/', null);
    disk.set('/cache/cae-content/old.png', 'old');
    disk.set('/docs/progress.json', 'learning history');
    const stableFetch = globalThis.fetch;
    const obsolete = file('figures/retired.png');
    globalThis.fetch = async () => ({ ok: true, text: async () => '{"files":{}}' });
    await syncContent();
    assert.ok(disk.has(obsolete), 'empty manifest must not trigger deletion');
    globalThis.fetch = async () => { throw Error('offline'); };
    await syncContent();
    assert.ok(disk.has(obsolete), 'offline must preserve existing data');
    globalThis.fetch = stableFetch;
    // Incomplete download defers all pruning.
    revision = 'retry';
    failFigure = true;
    disk.set(dir + '_shas.json', JSON.stringify({ [contentKey]: 'old', [figureKey]: 'old', 'figures/retired.png': 'old' }));
    await syncContent();
    assert.ok(disk.has(obsolete), 'partial sync must defer pruning');
    failFigure = false;
    await syncContent();
    assert.ok(!disk.has(obsolete));
    assert.ok(!disk.has(file('figures/untracked.png')));
    assert.ok(!disk.has(dir + encodeURIComponent(contentKey)));
    assert.ok(!disk.has(file('content/bundled.json')));
    assert.ok(!disk.has('/cache/cae-content/old.png'));
    assert.equal(disk.get('/docs/progress.json'), 'learning history');
    assert.equal((await loadCache()).content[contentKey].questions[0].easyExplanation[0].body, revision);
    assert.ok(disk.has(file(figureKey)));
    assert.deepEqual(Object.keys(JSON.parse(disk.get(dir + '_shas.json'))).sort(), [contentKey, figureKey].sort());
    const settled = downloads;
    assert.deepEqual(await syncContent(), { updated: 0 });
    assert.equal(downloads, settled, 'cleanup must not trigger repeat downloads');
    // A retired-only update must notify the caller to reapply cached overrides.
    disk.set(file('figures/retired.png'), 'old');
    disk.set(dir + '_shas.json', JSON.stringify({ [contentKey]: revision, [figureKey]: 'image', 'figures/retired.png': 'old' }));
    assert.equal((await syncContent()).updated, 1);
    console.log('OTA cleanup: complete/partial/offline/empty, duplicates, retired, bundle, history and refresh PASS');
    console.log('OTA: Android URI decoding, restart cache, partial retry, unchanged and revised content PASS');
    console.log('OTA: iOS chapter 9 legacy/v2 duplicates, both directory orders and legacy-only compatibility PASS');
  } finally {
    globalThis.fetch = oldFetch;
    delete globalThis.__otaFsMock;
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
