// Run: node tools/test_content_ota.cjs
// Reproduce Android's file-URI decoding at the native boundary; no network/device required.
const assert = require('node:assert/strict');
const path = require('node:path');
const { build } = require('esbuild');

async function main() {
  const root = path.resolve(__dirname, '..');
  const disk = new Map();
  const nativePath = uri => decodeURIComponent(new URL(uri).pathname);
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
      b.onLoad({ filter: /[\\/]content[\\/]_manifest\.json$/ }, () => ({ contents: '{"files":{}}', loader: 'json' }));
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
    console.log('OTA: Android URI decoding, restart cache, partial retry, unchanged and revised content PASS');
  } finally {
    globalThis.fetch = oldFetch;
    delete globalThis.__otaFsMock;
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
