// node tools/test_learning_figure.cjs
// RN Imageは同梱画像の寸法をstyleの初期値にする。URIだけのDOM画像では見逃す回帰を検査。
// Native実機の代わりではない。実コンポーネントのstyle・操作・表示領域の契約を確認する。
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const ts = require('typescript');
const jsx = require('react/jsx-runtime');
const flat = style => Array.isArray(style) ? Object.assign({}, ...style.map(flat)) : style || {};
const png = fs.readFileSync('assets/figures/s1e1SmallLarge.png');
const bundled = { uri: 'bundled.png', width: png.readUInt32BE(16), height: png.readUInt32BE(20) };
const ratio = 660 / 420;
const colors = { bg: '#fff', card: '#fff', text: '#111', sub: '#666', primary: '#123', border: '#888' };
const slots = []; let cursor = 0, pending = [], dirty = false;
const hooks = {
  useState(initial) {
    const i = cursor++;
    if (!(i in slots)) slots[i] = initial;
    return [slots[i], value => {
      const next = typeof value === 'function' ? value(slots[i]) : value;
      if (!Object.is(next, slots[i])) { slots[i] = next; dirty = true; }
    }];
  },
  useEffect(fn, deps) {
    const i = cursor++;
    if (!slots[i] || deps.some((v, j) => !Object.is(v, slots[i][j]))) { slots[i] = deps; pending.push(fn); }
  },
};
const imports = {
  react: hooks, 'react/jsx-runtime': jsx,
  'react-native': Object.fromEntries(['Image', 'Modal', 'Pressable', 'ScrollView', 'Text', 'View']
    .map(name => [name, name]).concat([['StyleSheet', { create: styles => styles }]])),
  'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
  './figures': { FIGURE_ASPECT: ratio },
  './data/figureStore': { hasFigure: () => true, figureSource: key => key === 'bundled' ? bundled : { uri: 'file:///ota.png' } },
};
const exportsObject = {};
const compiled = ts.transpileModule(fs.readFileSync('src/LearningFigure.tsx', 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.ReactJSX },
}).outputText;
vm.runInNewContext(compiled, { exports: exportsObject, require: name => {
  if (!(name in imports)) throw Error(`Unexpected import: ${name}`);
  return imports[name];
} });
let tree, figure = { figureImage: 'bundled', caption: '全体を確認する図' };
function render() {
  let retries = 0;
  do {
    dirty = false; cursor = 0; pending = [];
    tree = exportsObject.LearningFigure({ figure, colors });
    pending.forEach(effect => effect());
    assert(++retries < 12, 'render must settle');
  } while (dirty);
}
function nodes(node = tree, parent = null) {
  if (!node || typeof node !== 'object') return [];
  const children = [node.props?.children].flat(Infinity).filter(child => child != null);
  return [{ node, parent }, ...children.flatMap(child => nodes(child, node))];
}
const one = predicate => {
  const found = nodes().find(({ node }) => predicate(node));
  assert(found, 'element must exist'); return found.node;
};
function press(label) { one(n => n.type === 'Pressable' && n.props.accessibilityLabel === label).props.onPress(); render(); }
function layout(width, height) {
  one(n => n.type === 'View' && n.props.onLayout).props.onLayout({ nativeEvent: { layout: { width, height } } }); render();
}
function inlineBounds(parentWidth) {
  const { node: image, parent } = nodes().find(({ node }) => node.type === 'Image');
  const box = flat(parent.props.style);
  const frameWidth = box.width === '100%' ? parentWidth : box.width;
  const frameHeight = box.height ?? frameWidth / box.aspectRatio;
  // Image.ios.js / Image.android.js: [{width: source.width, height: source.height}, ..., props.style]
  const imageStyle = { width: image.props.source.width, height: image.props.source.height, ...flat(image.props.style) };
  const width = imageStyle.width === '100%' ? frameWidth : imageStyle.width;
  const height = imageStyle.height === '100%' ? frameHeight : imageStyle.height;
  assert.equal(image.props.resizeMode, 'contain');
  assert(width > 0 && width <= parentWidth, 'inline image must fit the actual card width');
  assert(Math.abs(height - width / ratio) < 0.01, 'native intrinsic height must not override the figure ratio');
}
function fittedBounds(width, height) {
  const modal = one(n => n.type === 'Modal');
  assert(modal.props.visible);
  const image = nodes(modal).find(({ node }) => node.type === 'Image').node;
  const style = flat(image.props.style);
  assert(style.width > 0 && style.width <= width - 31, '100% image must fit viewport width');
  assert(style.height > 0 && style.height <= height - 31, '100% image must fit viewport height');
  assert(Math.abs(style.width / style.height - ratio) < 0.001);
  return style;
}
for (const key of ['bundled', 'ota']) {
  figure = { ...figure, figureImage: key }; render();
  for (const width of [160, 252, 320, 700]) inlineBounds(width);
  press(`図を拡大：${figure.caption}`);
  for (const [width, height] of [[320, 480], [390, 560], [760, 160], [160, 210]]) {
    layout(width, height);
    const fitted = fittedBounds(width, height);
    press('図を拡大');
    const modalImage = nodes(one(n => n.type === 'Modal')).find(({ node }) => node.type === 'Image').node;
    assert.equal(flat(modalImage.props.style).width, fitted.width * 1.5);
    press('図を閉じる');
    assert.equal(one(n => n.type === 'Modal').props.visible, false);
    press(`図を拡大：${figure.caption}`);
    fittedBounds(width, height);
  }
  press('図を拡大'); layout(330, 460); fittedBounds(330, 460);
  one(n => n.type === 'Modal').props.onRequestClose(); render();
  assert.equal(one(n => n.type === 'Modal').props.visible, false);
}
press(`図を拡大：${figure.caption}`); press('図を拡大');
figure = { ...figure, figureImage: 'next-question' }; render();
assert.equal(one(n => n.type === 'Modal').props.visible, false, 'changing question must dismiss the old zoomed image');
console.log('LearningFigure: bundled/OTA sizing, narrow cards, landscape, zoom, reopen, rotation and dismissal PASS');
