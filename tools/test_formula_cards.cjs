// node tools/test_formula_cards.cjs
// 用語カードの旧OTA互換、数式操作、検索・購入制限・一覧復帰を検査する。
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const ts = require('typescript');
const jsx = require('react/jsx-runtime');
const native = Object.fromEntries(['View', 'Text', 'Pressable', 'TextInput', 'ScrollView'].map(n => [n, n]));
native.StyleSheet = { create: s => s };
const compile = (source, imports = {}, globals = {}) => {
  const output = {};
  vm.runInNewContext(ts.transpileModule(source, { compilerOptions: {
    module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.ReactJSX,
  } }).outputText, { exports: output, require: name => {
    if (name === 'react/jsx-runtime') return jsx;
    if (name === 'react-native') return native;
    if (!(name in imports)) throw Error('Unexpected import: ' + name);
    return imports[name];
  }, ...globals });
  return output;
};
const { matchesFormula } = compile(fs.readFileSync('src/formulas.ts', 'utf8'), {
  './data/contentStore': { getContent: () => null }, './catalog': { FORMULA_KEY_BY_ID: {} },
});
const { FormulaCard, formulaDisplay } = compile(fs.readFileSync('src/FormulaCard.tsx', 'utf8'), {
  './MathText': { RichText: 'RichText' }, './LearningFigure': { LearningFigure: 'LearningFigure' },
});
const nodes = n => !n || typeof n !== 'object' ? [] : [n, ...[n.props?.children].flat(Infinity).flatMap(nodes)];
const t = { bg: '#fff', card: '#eee', text: '#111', sub: '#555', primary: '#123', reviewBtn: '#345', border: '#888' };
const item = { id: 'a', kind: 'formula', term: '変形勾配', summary: '小さな線の変化を表す。',
  formula: '$F=I+H$', body: '本文 $F$。', example: '確認 $H=0$。', figureImage: 'f', figureCaption: '矢印の長さを比べる。' };
let active;
const card = nodes(FormulaCard({ t, item, right: 'favorite', onScrollActive: a => { active = a; } }));
const math = card.filter(n => n.type === 'RichText');
assert.equal(math.length, 3);
for (const n of math) {
  assert(n.props.scroll && n.props.scrollOnlyOverflow, '本文・例の式も縮小せず横スクロールする');
  n.props.onScrollActiveChange(true); assert.equal(active, true);
  n.props.onScrollActiveChange(false); assert.equal(active, false);
}
assert.equal(card.find(n => n.type === 'LearningFigure').props.figure.caption, item.figureCaption);
const old = nodes(FormulaCard({ t, item: { ...item, summary: undefined, figureCaption: undefined } }));
assert(old.some(n => n.props?.children === '具体例・補足'), '旧原稿の補足を数値例と決め付けない');
assert.equal(old.find(n => n.type === 'LearningFigure').props.figure.caption, '変形勾配の図');
assert.equal(formulaDisplay('$A=B$\n$C=D$'), '$$A=B$$\n$$C=D$$');
assert.equal(formulaDisplay('$A=B=C$'), '$$A=B=C$$', '等式を勝手に分断しない');
assert.equal(formulaDisplay('条件：$A=0$'), '条件：$A=0$');
assert(matchesFormula({ ...item, body: 'TL法：変形前が基準' }, 'ｔｌ　変形前'));
assert(!matchesFormula(item, '変形勾配 不在語'));

const documents = [
  ...Array.from({ length: 11 }, (_, i) => ({ scope: 'solid1', ...JSON.parse(fs.readFileSync(`content/formulas/solid1-ch${i + 1}.json`, 'utf8')) })),
  ...Array.from({ length: 13 }, (_, i) => ({ scope: `solid2-ch${i + 1}`, ...JSON.parse(fs.readFileSync(`content/formulas/ch${i + 1}.json`, 'utf8')) })),
  ...Array.from({ length: 11 }, (_, i) => ({ scope: 'thermal2', ...JSON.parse(fs.readFileSync(`content/formulas/thermal2-ch${i + 1}.json`, 'utf8')) })),
  ...Array.from({ length: 16 }, (_, i) => ({ scope: 'thermal1', ...JSON.parse(fs.readFileSync(`content/formulas/thermal1-ch${i + 1}.json`, 'utf8')) })),
  ...Array.from({ length: 13 }, (_, i) => ({ scope: 'vib2', ...JSON.parse(fs.readFileSync(`content/formulas/vib2-ch${i + 1}.json`, 'utf8')) })),
  ...Array.from({ length: 9 }, (_, i) => ({ scope: 'vib1', ...JSON.parse(fs.readFileSync(`content/formulas/vib1-ch${i + 1}.json`, 'utf8')) })),
];
const ids = new Set();
for (const doc of documents) for (const it of doc.items) {
  const key = `${doc.scope}:${it.id}`;
  assert(!ids.has(key), '用語IDの重複'); ids.add(key);
  assert(it.summary?.trim(), it.id + ': 要点');
  for (const key of ['term', 'summary', 'figureCaption']) assert(!/[$\\^_]/.test(it[key] || ''), it.id + ': 通常Textに未組版の数式');
  if (it.figureImage) assert(it.figureCaption?.trim(), it.id + ': 図との対応');
}

// Appの本物のFormulaTabを、Native要素だけ置き換えて操作する。
const app = fs.readFileSync('App.tsx', 'utf8');
const tabSource = app.slice(app.indexOf('function FormulaTab('), app.indexOf('// 公式・用語の個別ページ'));
let slots = [], cursor = 0;
const useState = initial => { const i = cursor++; if (!(i in slots)) slots[i] = initial;
  return [slots[i], value => { slots[i] = value; }]; };
const useRef = initial => { const i = cursor++; return slots[i] ?? (slots[i] = { current: initial }); };
const { FormulaTab } = compile('export ' + tabSource, {}, {
  ...native, useState, useRef, matchesFormula, FormulaCard, FormulaItemScreen: 'Detail', BackLink: 'Back', Button: 'Button',
  styles: {}, isChapterLocked: (_p, _f, _g, id) => id === 'locked', entKey: () => '', entInfoByKey: () => null,
  isBookmarked: (bookmarks, id) => !!bookmarks[id], formulaDoc: () => ({ title: '章' }),
  useScrollAreaLock: () => ({ lock: { current: true }, events: { onContentSizeChange() {} } }), useSwipeNav: () => ({}),
});
let opened, paywall = false;
const props = { t, view: 'list', course: {}, rows: [
  { chapterId: 'free', chapterTitle: '第1章', favId: 'a', item },
  { chapterId: 'locked', chapterTitle: '第4章', favId: 'b', item: { ...item, id: 'b', term: '変形の接触' } },
], proState: {}, field: 'solid', grade: '1', kind: 'term', fav: false, bookmarks: {}, listChapterId: null,
  scrollAreaLockRef: { current: false }, onOpenItem: (...args) => { opened = args; }, onOpenPaywall: () => { paywall = true; },
};
const render = () => { cursor = 0; return nodes(FormulaTab(props)); };
let tree = render();
tree.find(n => n.type === 'TextInput').props.onChangeText('変形'); tree = render();
const result = tree.find(n => n.props?.accessibilityLabel === '変形勾配を開く');
assert(result, '現在の種類が用語でも公式を全章から検索できる');
result.props.onPress(); assert.deepEqual(opened, ['free', 'a']);
tree.find(n => n.props?.accessibilityLabel === '変形の接触を開く').props.onPress(); assert(paywall, '検索から購入制限を回避できない');
const list = tree.find(n => n.type === 'ScrollView');
list.props.onScroll({ nativeEvent: { contentOffset: { y: 280 } } });
props.view = 'item'; props.chapterId = 'free'; props.itemId = 'a';
const detail = render().find(n => n.type === 'Detail'); assert.equal(detail.props.siblings.length, 2);
props.view = 'list'; tree = render();
const returned = tree.find(n => n.type === 'ScrollView'); let restored;
returned.props.ref.current = { scrollTo: p => { restored = p.y; } };
returned.props.onContentSizeChange(390, 1200); assert.equal(restored, 280, '検索結果へ戻ると直前の位置を復元する');
tree.find(n => n.type === 'TextInput').props.onChangeText('見つからない用語'); tree = render();
assert(!tree.some(n => n.props?.accessibilityLabel === '変形勾配を開く'));
// 実レンダラーの再レイアウト契約。狭い初期幅→通常幅でも短い式と本文高さを戻す。
const mathSource = fs.readFileSync('src/MathText.tsx', 'utf8');
let available = 5;
class Element {
  constructor(width, name = '') { this.width = width; this.className = name; this.children = []; }
  get classList() { return { contains: name => this.className === name }; }
  get parentNode() { return this.parentElement; }
  getBoundingClientRect() { return { width: this.width, height: 120 }; }
  insertBefore(child, next) { child.remove(); child.parentElement = this; this.children.splice(this.children.indexOf(next), 0, child); }
  appendChild(child) { child.remove(); child.parentElement = this; this.children.push(child); }
  remove() { if (this.parentElement) { const p = this.parentElement; p.children.splice(p.children.indexOf(this), 1); this.parentElement = null; } }
}
const body = new Element(320), shortMath = new Element(50), longMath = new Element(500);
body.appendChild(shortMath); body.appendChild(longMath);
const scrollEnvironment = { SCROLL: true, SCROLL_ONLY_OVERFLOW: true, contentWidth: () => available,
  document: { querySelectorAll: () => [shortMath, longMath], createElement: () => new Element(available) } };
vm.createContext(scrollEnvironment);
vm.runInContext(mathSource.slice(mathSource.indexOf('  function prepareMathScroll(){'), mathSource.indexOf('  // 横スクロールできる')), scrollEnvironment);
scrollEnvironment.prepareMathScroll(); assert.equal(shortMath.parentElement.className, 'math-scroll');
available = 320; scrollEnvironment.prepareMathScroll();
assert.equal(shortMath.parentElement, body, '幅が戻った短い式を本文内へ戻す');
assert.equal(longMath.parentElement.className, 'math-scroll', '長い式のスクロールは維持');
let reported;
// postは既存WebView高1800でなく、現在の本文高120を通知する。
vm.runInNewContext(mathSource.slice(mathSource.indexOf('  function post(){'), mathSource.indexOf('  function run(){')) + '\npost();', {
  SCROLL_ONLY_OVERFLOW: false, prepareMathScroll() {}, fitDisplays() {}, updateFade() {},
  document: { getElementById: () => ({ scrollHeight: 120, getBoundingClientRect: () => ({ height: 119.5 }) }),
    body: { scrollHeight: 120 }, documentElement: { scrollHeight: 1800 } },
  window: { ReactNativeWebView: { postMessage: value => { reported = Number(value); } } },
});
assert.equal(reported, 120);
// 初回の測定が終わった後の折返し・文字サイズ変更でも、現在の本文高を送り直す。
let bodyHeight = 120, pendingFrame;
const reflowEnvironment = {
  SCROLL_ONLY_OVERFLOW: false, prepareMathScroll() {}, fitDisplays() {}, updateFade() {},
  document: { getElementById: () => ({ get scrollHeight() { return bodyHeight; }, getBoundingClientRect: () => ({ height: bodyHeight }) }) },
  window: { ReactNativeWebView: { postMessage: value => { reported = Number(value); } } },
  requestAnimationFrame: fn => { assert(!pendingFrame); pendingFrame = fn; },
};
vm.createContext(reflowEnvironment);
vm.runInContext(mathSource.slice(mathSource.indexOf('  function post(){'), mathSource.indexOf('  function run(){')), reflowEnvironment);
reflowEnvironment.post();
bodyHeight = 270;
reflowEnvironment.schedulePost(); reflowEnvironment.schedulePost();
pendingFrame(); pendingFrame = null;
assert.equal(reported, 270, '遅れて増えた本文高を取り込み、末尾を切らない');
bodyHeight = 90; reflowEnvironment.schedulePost(); pendingFrame(); pendingFrame = null;
assert.equal(reported, 90, '短くなった場合も旧高さを残さない');
// 長い式の目印は式自身に限定し、末尾へ達したら解除する。
const mathRow = { scrollWidth: 500, clientWidth: 280, scrollLeft: 0, style: {} };
const fadeEnvironment = { SCROLL: true, document: { querySelectorAll: () => [mathRow] } };
vm.createContext(fadeEnvironment);
vm.runInContext(mathSource.slice(mathSource.indexOf('  function updateFade(){'), mathSource.indexOf('  function post(){')), fadeEnvironment);
fadeEnvironment.updateFade(); assert.match(mathRow.style.maskImage, /linear-gradient/);
mathRow.scrollLeft = 220; fadeEnvironment.updateFade(); assert.equal(mathRow.style.maskImage, 'none');
mathRow.clientWidth = 600; mathRow.scrollLeft = 0; fadeEnvironment.updateFade(); assert.equal(mathRow.style.maskImage, 'none');
assert(!mathSource.includes('id="fade"'), '本文の右端全体を覆うフェードを作らない');
// Native側も測定高を保持する。画面内スクロールの復習表示だけは残り高さを使用する。
native.Platform = { OS: 'ios' };
const { MathText } = compile(mathSource, { react: { useState }, 'react-native-webview': { WebView: 'WebView' } });
slots = []; cursor = 0;
let mathView = MathText({ text: '$x=1$', color: '#111' });
mathView.props.onMessage({ nativeEvent: { data: '270' } }); cursor = 0;
mathView = MathText({ text: '$x=1$', color: '#111' });
assert.equal(mathView.props.style.height, 270);
assert.equal(mathView.props.style.flex, 0);
assert.equal(mathView.props.containerStyle.height, 270);
assert.equal(mathView.props.containerStyle.flex, 0);
cursor = 0;
mathView = MathText({ text: '$x=1$', color: '#111', verticalScroll: true });
assert.equal(mathView.props.style.flex, 1);
assert.equal(mathView.props.containerStyle.height, undefined);
console.log(`Formula cards/search: PASS (${ids.size} solid1/solid2/thermal1/thermal2/vib2/vib1 items; legacy OTA; scroll; locked results; return position)`);
