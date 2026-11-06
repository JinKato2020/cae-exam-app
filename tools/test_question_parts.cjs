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
const groupedChoice = { id: 'one', responseType: 'choice', answer: 2 };
const groupedWritten = { id: 'two', responseType: 'written', answer: 0 };
const grouped = [groupedChoice, groupedWritten];
assert.equal(parts.studyResult([], {}).complete, false);
assert.equal(parts.studyResult(grouped, { one: { choice: 2 } }).complete, false);
assert.equal(parts.studyResult(grouped, { one: { choice: 2 }, two: { revealed: true } }).complete, false);
assert.equal(parts.studyResult(grouped, { one: { choice: 2 }, two: { revealed: true, understood: true } }).correct, true);
assert.equal(parts.studyResult(grouped, { one: { choice: 2 }, two: { revealed: true, understood: false } }).complete, true);
assert.equal(parts.studyResult(grouped, { one: { choice: 2 }, two: { revealed: true, understood: false } }).correct, false);
assert.equal(parts.studyResult(grouped, { one: { choice: 1 }, two: { revealed: true, understood: true } }).correct, false);
const simple = id => ({ id, number: id, question: `question ${id}`, choices: ['a','b','c','d'], answer: 1, explanation: 'explanation' });
const chapter = questions => ({ meta: { count: questions.length }, questions });
const ordinary = simple('ordinary');
assert.equal(parts.expandChapter(chapter([ordinary])).questions[0], ordinary);
const guidedChapter = { ...chapter([ordinary]), meta: { count: 1, explanationMode: 'guided' } };
assert.equal(parts.expandChapter(guidedChapter).questions[0].explanationMode, 'guided');
assert.equal(ordinary.explanationMode, undefined, 'chapter display policy must not mutate source JSON');
// 章番号で表示を限定しない。実データ全章を画面が読む形へ展開して確認する。
const solid1Files = fs.readdirSync('content/questions').filter(name => /^solid1-\d\d-.*\.json$/.test(name));
assert.equal(solid1Files.length, 11);
for (const file of solid1Files) {
  const raw = JSON.parse(fs.readFileSync(`content/questions/${file}`, 'utf8'));
  for (const q of parts.expandChapter(raw).questions) {
    assert.equal(q.explanationMode, 'guided', `${q.id}: unified display must reach the screen`);
    for (const answer of q.studyParts?.length ? q.studyParts : [q]) {
      assert(answer.easyExplanation?.length, `${answer.id}: unified answer must not be empty`);
    }
  }
}
assert.equal(parts.expandChapter(chapter([{ ...ordinary, studyParts: grouped }])).questions.length, 1,
  'grouped study remains one official question in navigation and progress');
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
assert.equal(realExpanded.questions.length, real.questions.length);
const visco = realExpanded.questions.find(q => q.id === 'solid1-11-06');
const sample = visco.studyParts;
assert.equal(sample.length, 3);
assert.equal(sample[0].answer, 3);
assert.equal(sample[1].responseType, 'written');
assert.equal(sample[2].answer, 1);
assert.equal(sample[0].id, 'solid1-11-06-timing');
assert.equal(sample[2].id, 'solid1-11-06-moduli');
assert.equal(sample[2].figureImage, 's1e11DynViscoModuli');
data = real; catalog.rebuildCatalog();
assert.equal(catalog.questionsByIds([sample[2].id])[0].id, visco.id, 'old child bookmark must open grouped page');
const oldChild = { ...sample[2], rootQuestionId: visco.id, groupSize: 2 };
const mergedSession = parts.refreshQuestionSession([oldChild], 0, realExpanded.questions);
assert.equal(mergedSession.questions.length, 1, 'one old child must survive consolidation');
assert.equal(mergedSession.questions[0].id, visco.id);
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
# Retain explicit legacy-parts coverage after the real chapter moves to studyParts.
source=next(q for q in d['questions'] if q['number']=='11(2)-2')
children=[copy.deepcopy(q) for q in source['studyParts'] if q['responseType']=='choice']
legacy=copy.deepcopy(children[0]);legacy['id']='legacy-parent';legacy['parts']=children
d={'questions':[legacy]}
assert not part_structure_errors(d)
for defect in ('duplicate','answer','fallback'):
 b=copy.deepcopy(d);q=next(q for q in b['questions'] if q.get('parts'))
 if defect=='duplicate':q['parts'][1]['id']=q['parts'][0]['id']
 if defect=='answer':q['parts'][1]['answer']=9
 if defect=='fallback':q['answer']=1
 assert part_structure_errors(b),defect
`], { stdio: 'pipe' });
console.log('Question parts: legacy, independent scoring, OTA add/reorder/remove, nested context, review scope and catalog PASS');
require('node:child_process').execFileSync('python', ['-c', `
import sys,json,copy
from pathlib import Path
sys.path.insert(0,'tools')
from check_quality import study_parts_errors,easy_explanation_errors,presentation_errors
d=json.loads(Path('content/questions/solid1-01-nonlinear-stress-strain.json').read_bytes())
assert not study_parts_errors(d)
from unittest.mock import patch
with patch.object(Path,'is_file',return_value=False):
 assert not study_parts_errors(d),'verified official evidence must work in CI without private source files'
 bad=copy.deepcopy(d);q=next(q for q in bad['questions'] if q.get('studyParts'))
 q['studyParts'][0]['officialWrittenEvidence']['excerpt']+=' invented'
 assert study_parts_errors(bad),'unverified written evidence must fail even without private source files'
q=next(q for q in d['questions'] if q.get('studyParts'))
q['studyParts'][0].pop('officialWrittenEvidence')
assert study_parts_errors(d),'original written questions without official evidence must be blocked'
d=json.loads(Path('content/questions/solid1-02-material-nonlinear.json').read_bytes())
q=next(q for q in d['questions'] if q.get('studyParts') and q['studyParts'][0].get('responseType')=='choice')
q['studyParts'][0]['answer']=99
assert study_parts_errors(d),'invalid choice answer must be blocked'
d=json.loads(Path('content/questions/solid1-03-geometric-nonlinear.json').read_bytes())
before=json.dumps(d)
assert not easy_explanation_errors(d)
assert json.dumps(d)==before,'validation must not append explanation figures into pre-answer figures'
d['questions'][0]['easyExplanation'][0]['figures']=[{'figureImage':'missing-inline-figure','caption':'test'}]
assert any('missing-inline-figure' in e for e in presentation_errors(d)),'inline figures must pass the same figure gate'
# 公式の語句記入も許可するが、選択式の「記述選択」は記述問題へ転用しない。
d=json.loads(Path('content/questions/solid1-06-dynamic-analysis.json').read_bytes())
with patch.object(Path,'is_file',return_value=False):
 assert not study_parts_errors(d),'verified official term/calculation entry must work without private sources'
 bad=copy.deepcopy(d)
 q=next(q for q in bad['questions'] if q['number']=='6-6')
 q['studyParts'][0]['officialWrittenEvidence']['excerpt']+=' invented'
 assert study_parts_errors(bad),'unregistered entry evidence must be rejected'
d=json.loads(Path('content/questions/solid1-05-fracture-fatigue.json').read_bytes())
q=next(q for q in d['questions'] if q['number']=='5-12')
p=copy.deepcopy(next(q for q in d['questions'] if q['number']=='5-13')['studyParts'][0])
p.update(id=q['id']+'-invented',number=q['number'],officialRef=q['officialRef'])
q['studyParts']=[p]
assert study_parts_errors(d),'a statement-selection question must not become a written question'

`], { stdio: 'pipe' });
console.log('Guided grouped study: official written evidence, self-check, inline figures and data immutability PASS');
// 選択式の組合せ問題は分割せず、章の統一表示設定を全問へ継承する。
for (const [file, count] of [['math-basics', 12], ['solid-basics', 44], ['heat-basics', 17], ['fem-basics', 29], ['fem-practice', 29], ['numerical-basics', 15], ['element-tech', 17], ['modeling-basics', 27], ['boundary-conditions', 33], ['prepost-basics', 41], ['verification-basics', 17], ['computer-basics', 33], ['ethics', 12]]) {
  const source = JSON.parse(fs.readFileSync('content/questions/' + file + '.json', 'utf8'));
  const expanded = parts.expandChapter(source);
  assert.equal(expanded.questions.length, count);
  assert.deepEqual(Array.from(expanded.questions, q => q.id), source.questions.map(q => q.id));
  assert(expanded.questions.every(q => q.explanationMode === 'guided' && q.answerSummary && q.easyExplanation.length));
  assert(expanded.questions.every(q => !q.parts && (q.studyParts?.length
    ? q.studyParts.every(p => p.responseType === 'choice' && [2, 4].includes(p.choices.length))
    : q.choices.length === 4)), 'keep combination questions intact; permit grouped choice subquestions');
  for (const q of expanded.questions) {
    if (q.preFigureImage) assert(q.preFigures.some(f => f.figureImage === q.preFigureImage && f.caption));
    if (q.figureImage && q.figureImage !== q.preFigureImage) {
      assert(q.easyExplanation.some(s => s.figures?.some(f => f.figureImage === q.figureImage && f.caption)), q.number + ': explanation figure lost');
    }
  }
}
// 固体2級1〜4章も同じ小問機能を使う。検証用データだけをメモリ内で組み、教材は変えない。
for (const file of ['math-basics', 'solid-basics', 'heat-basics', 'fem-basics']) {
  const source = JSON.parse(fs.readFileSync('content/questions/' + file + '.json', 'utf8'));
  const parent = source.questions.find(q => q.preFigures?.length) ?? source.questions[0];
  const children = [2, 4].map((count, i) => ({
    ...parent, id: parent.id + '-grouping-test-' + i, responseType: 'choice',
    choices: parent.choices.slice(0, count), answer: count,
    preFigureImage: undefined, preFigures: [],
  }));
  const updated = { ...source, questions: source.questions.map(q => q.id === parent.id
    ? { ...q, sharedQuestion: q.question, studyParts: children } : q) };
  const expanded = parts.expandChapter(updated);
  assert.equal(expanded.questions.length, source.questions.length, file + ': no separate pages for subquestions');
  const grouped = expanded.questions.find(q => q.id === parent.id);
  assert.equal(grouped.explanationMode, 'guided');
  assert.equal(grouped.sharedQuestion, parent.question);
  assert.equal(grouped.preFigures, parent.preFigures, 'retain the shared figure on its parent');
  assert(grouped.studyParts.every(p => !p.preFigures.length));
  const answers = { [children[0].id]: { choice: children[0].answer } };
  assert.equal(parts.studyResult(grouped.studyParts, answers).complete, false);
  answers[children[1].id] = { choice: children[1].answer };
  assert.equal(parts.studyResult(grouped.studyParts, answers).correct, true);
  const previous = parts.expandChapter(source);
  const index = previous.questions.findIndex(q => q.id === parent.id);
  const session = parts.refreshQuestionSession(previous.questions, index, expanded.questions);
  assert.equal(session.questions[session.index].id, parent.id, 'OTA grouping retains the open question');
  assert.equal(session.questions[session.index].studyParts.length, 2);
}
require('node:child_process').execFileSync('python', ['-c', `
import json,sys,copy
from pathlib import Path
sys.path.insert(0,'tools')
from check_quality import require_editorial_review,easy_explanation_errors,presentation_errors
for name in ('math-basics','solid-basics','heat-basics','fem-basics','fem-practice','numerical-basics','element-tech','modeling-basics','boundary-conditions','prepost-basics','verification-basics','computer-basics','ethics'):
 d=json.loads(Path('content/questions/'+name+'.json').read_bytes())
 require_editorial_review(d)
 bad=copy.deepcopy(d);bad['questions'][0].pop('answerSummary')
 assert easy_explanation_errors(bad),'guided mode needs an answer summary even without a length floor'
 bad=copy.deepcopy(d);bad['meta']['explanationMode']='standard'
 bad['questions'][0]['easyExplanation']=[{'title':'test','body':'short'}]
 assert any('1200' in e for e in easy_explanation_errors(bad)),'non-guided explanations retain their existing rule'
 bad=copy.deepcopy(d);bad['questions'][0]['answerSummary']='unrendered ^T'
 assert presentation_errors(bad),'unrendered formulas must still fail'
`], {stdio: 'pipe'});
console.log('Solid2 unified chapters: IDs, choice grouping, inline figures and quality gates PASS');
