// node tools/test_question_parts.cjs — OTAでの設問追加・並替・削除と旧形式を検証
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const ts = require('typescript');
function load(file, imports = {}) {
  const exports = {};
  const code = ts.transpileModule(fs.readFileSync(file, 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
  }).outputText;
  vm.runInNewContext(code, { exports, require: name => {
    if (!(name in imports)) throw Error(`Unexpected import: ${name}`);
    return imports[name];
  } }, { filename: file });
  return exports;
}
const parts = load('src/questionParts.ts');
const simple = id => ({ id, number: id, question: `question ${id}`, choices: ['a','b','c','d'], answer: 1, explanation: 'explanation' });
const chapter = questions => ({ meta: { count: questions.length }, questions });
const ordinary = simple('ordinary');
assert.equal(parts.expandChapter(chapter([ordinary])).questions[0], ordinary);
const root = { ...simple('root'), sharedQuestion: 'common conditions', figureImage: 'parent-only', relatedFormulas: ['term'], parts: [simple('a'), simple('b')] };
const before = JSON.stringify(root);
const expanded = parts.expandChapter(chapter([ordinary, root]));
assert.equal(expanded.meta.count, 3);
assert.equal(expanded.questions[1].question, 'common conditions\n\nquestion a');
assert.equal(expanded.questions[1].figureImage, undefined, 'parent answer figure must not leak to child');
assert.equal(expanded.questions[1].relatedFormulas[0], 'term');
assert.equal(JSON.stringify(root), before, 'bundled/OTA raw data must remain immutable');
const changed = parts.expandChapter(chapter([ordinary, { ...root, parts: [simple('b'), simple('c'), simple('a')] }]));
const session = parts.refreshQuestionSession(expanded.questions, 2, changed.questions);
assert.equal(session.questions.length, 4);
assert.equal(session.questions[session.index].id, 'b', 'reorder must retain current stable ID');
assert.equal(session.questions[3].id, 'a');
const review = parts.refreshQuestionSession([expanded.questions[2]], 0, changed.questions);
assert.equal(review.questions.length, 1, 'wrong-only review must not acquire unselected siblings');
assert.equal(review.questions[0].id, 'b');
const removed = parts.refreshQuestionSession(expanded.questions, 2, [ordinary]);
assert.equal(removed.questions.length, 1);
assert.equal(removed.index, 0);
assert.equal(parts.refreshQuestionSession([simple('gone')], 0, []).questions.length, 0);
const nested = parts.expandChapter(chapter([{ ...root, parts: [{ ...simple('branch'), sharedQuestion: 'inner', parts: [simple('leaf')] }] }]));
assert.equal(nested.questions[0].id, 'leaf');
assert.equal(nested.questions[0].question, 'common conditions\n\ninner\n\nquestion leaf');
assert.equal(nested.questions[0].partLabel, '設問 1 / 1 · 1 / 1');
// 実際のカタログを再構築して、OTA追加を一覧・ジャンプ・公式参照へ反映する。
let data = chapter([root]);
const catalog = load('src/catalog.ts', {
  './questionParts': parts,
  './data/contentStore': { getContent: key => key === 'content/catalog.json'
    ? { fields: [{ id:'solid', name:'solid', grades:[{ id:'g1', name:'g1', chapters:[{ id:'ch11', title:'chapter', content:'chapter' }] }] }] }
    : data },
});
assert.equal(catalog.ALL_QUESTIONS.length, 2);
assert.equal(catalog.questionsByIds(['root']).length, 2, 'old parent links must resolve to parts');
data = chapter([{ ...root, parts: [simple('b'), simple('c'), simple('a')] }]);
catalog.rebuildCatalog();
assert.equal(catalog.ALL_QUESTIONS.length, 3);
assert.equal(catalog.QUESTION_CHAPTER.c, 'ch11');
const real = JSON.parse(fs.readFileSync('content/questions/solid1-11-modeling-techniques.json','utf8'));
const realExpanded = parts.expandChapter(real);
assert.equal(realExpanded.questions.length, real.questions.length + 1);
const sample = realExpanded.questions.filter(q => q.rootQuestionId === 'solid1-11-06');
assert.equal(sample.length, 2);
assert.equal(sample[0].answer, 3);
assert.equal(sample[1].answer, 1);
assert.notEqual(sample[0].id, sample[1].id);
assert.equal(sample[1].figureImage, 's1e11DynViscoModuli');
// 設問を増やしても親5問分の無料範囲と、分野×級の購入権限を維持する。
data = chapter([simple('one'),simple('two'),simple('three'),simple('four'),root,simple('paid')]);
catalog.rebuildCatalog();
const pro = load('src/pro/proState.ts', {
  '../catalog': catalog,
  '@react-native-async-storage/async-storage': { default: {} },
});
assert.equal(pro.FREE_QUESTION_IDS.has('a'), true);
assert.equal(pro.FREE_QUESTION_IDS.has('b'), true);
assert.equal(pro.FREE_QUESTION_IDS.has('paid'), false);
assert.equal(pro.entOfQuestion('b').key, 'solid_g1');
data = chapter([simple('one'),simple('two'),simple('three'),simple('four'),simple('five'),root]);
catalog.rebuildCatalog();pro.rebuildProState();
assert.equal(pro.FREE_QUESTION_IDS.has('a'), false);
assert.equal(pro.isLocked(catalog.questionsByIds(['a'])[0], { owned: [], devPro: false }), true);
assert.equal(pro.isLocked(catalog.questionsByIds(['a'])[0], { owned: ['solid_g1'], devPro: false }), false);
require('node:child_process').execFileSync('python', ['-c', `
import sys,json,copy
from pathlib import Path
sys.path.insert(0,'tools')
from check_quality import editorial_errors,part_structure_errors
d=json.loads(Path('content/questions/solid1-11-modeling-techniques.json').read_bytes())
assert not editorial_errors(d)
for defect in ('duplicate','answer','fallback'):
 b=copy.deepcopy(d);q=next(q for q in b['questions'] if q.get('parts'))
 if defect=='duplicate':q['parts'][1]['id']=q['parts'][0]['id']
 if defect=='answer':q['parts'][1]['answer']=9
 if defect=='fallback':q['answer']=1
 assert part_structure_errors(b),defect
`], { stdio: 'pipe' });
console.log('Question parts: legacy, independent scoring, OTA add/reorder/remove, nested context, review scope and catalog PASS');
