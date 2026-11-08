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
// 熱流体1級1〜8章も同じ殻で、公式番号107件の中に243設問を表示する。
let thermalAnswers = 0, thermalWritten = 0;
for (const file of ['thermal1-01-single-phase-physics', 'thermal1-02-single-phase-calc1', 'thermal1-03-single-phase-calc2', 'thermal1-04-grid-handling', 'thermal1-05-turbulence-models', 'thermal1-06-design-application', 'thermal1-07-acceleration-and-postprocessing', 'thermal1-08-results-and-evaluation']) {
  const raw = JSON.parse(fs.readFileSync(`content/questions/${file}.json`, 'utf8'));
  const expanded = parts.expandChapter(raw);
  assert.equal(expanded.questions.length, raw.meta.officialCount);
  for (const q of expanded.questions) {
    assert.equal(q.explanationMode, 'guided');
    const prompts = q.studyParts?.length ? q.studyParts : [q];
    thermalAnswers += prompts.length;
    for (const prompt of prompts) {
      assert(prompt.answerSummary && prompt.easyExplanation.length, `${prompt.id}: missing guided content`);
      if (prompt.responseType === 'written') {
        thermalWritten++;
        assert(prompt.officialWrittenEvidence && prompt.modelAnswer && prompt.answerCheckpoints.length);
      }
    }
  }
}
assert.equal(thermalAnswers, 243);
assert.equal(thermalWritten, 64);
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
assert.equal(sample.length, 5);
assert.deepEqual(sample.map(p=>p.officialQuestionItem),['tension','compression','loop','storage','loss']);
assert.equal(sample[2].responseType, 'written');
assert.equal(sample[0].id, 'solid1-11-06-timing');
assert.equal(sample[3].id, 'solid1-11-06-moduli');
assert(sample[3].easyExplanation.some(s=>s.figures?.some(f=>f.figureImage==='s1e11DynViscoModuli')));
data = real; catalog.rebuildCatalog();
assert.equal(catalog.questionsByIds([sample[3].id])[0].id, visco.id, 'old child bookmark must open grouped page');
const oldChild = { ...sample[3], rootQuestionId: visco.id, groupSize: 2 };
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
for q in children:
 q['choices']=['a','b','c','d'];q['answer']=2
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
 bad=copy.deepcopy(d);q=next(q for q in bad['questions'] if q.get('studyParts') and q['studyParts'][0].get('responseType')=='written')
 q['studyParts'][0]['officialWrittenEvidence']['excerpt']+=' invented'
 assert study_parts_errors(bad),'unverified written evidence must fail even without private source files'
thermal=json.loads(Path('content/questions/thermal1-07-acceleration-and-postprocessing.json').read_bytes())
assert not study_parts_errors(thermal),'verified numbered source lists must be accepted'
with patch.object(Path,'is_file',return_value=False):
 assert not study_parts_errors(thermal),'verified list evidence must work without private sources'
 bad=copy.deepcopy(thermal)
 next(q for q in bad['questions'] if q['number']=='7-1')['studyParts'][0]['officialWrittenEvidence']=next(q for q in thermal['questions'] if q['number']=='7-10')['studyParts'][0]['officialWrittenEvidence']
 assert study_parts_errors(bad),'7-10 evidence must not authorize 7-1'
q=next(q for q in d['questions'] if q.get('studyParts') and q['studyParts'][0].get('responseType')=='written')
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
# nuの誤エスケープはKaTeXでエラーにならなくても、数式の意味を変える。
d=json.loads(Path('content/questions/thermal1-05-turbulence-models.json').read_bytes())
assert not easy_explanation_errors(d)
d['questions'][0]['easyExplanation'][0]['body']='$'+chr(10)+'u_t$'
assert any('制御文字' in e for e in easy_explanation_errors(d)),'escaped math corruption must be blocked'


`], { stdio: 'pipe' });
console.log('Guided grouped study: official written evidence, self-check, inline figures and data immutability PASS');
// 公式番号ごとのページを保持し、章の統一表示設定と個別回答の小問を確認する。
for (const [file, count] of [['math-basics', 12], ['solid-basics', 44], ['heat-basics', 17], ['fem-basics', 29], ['fem-practice', 29], ['numerical-basics', 15], ['element-tech', 17], ['modeling-basics', 27], ['boundary-conditions', 33], ['prepost-basics', 41], ['verification-basics', 17], ['computer-basics', 33], ['ethics', 12], ['thermal2-01-math-basics', 11], ['thermal2-02-fluid-basics', 22], ['thermal2-03-thermo-heat', 19], ['thermal2-04-numerical-methods', 13], ['thermal2-05-grid-generation', 15], ['thermal2-06-turbulence', 16], ['thermal2-07-boundary-conditions', 12], ['thermal2-08-post-processing', 14], ['thermal2-09-verification', 18], ['thermal2-10-computer-basics', 32], ['thermal2-11-ethics', 12]]) {
  const source = JSON.parse(fs.readFileSync('content/questions/' + file + '.json', 'utf8'));
  const expanded = parts.expandChapter(source);
  assert.equal(expanded.questions.length, count);
  assert.deepEqual(Array.from(expanded.questions, q => q.id), source.questions.map(q => q.id));
  assert(expanded.questions.every(q => q.explanationMode === 'guided' && q.answerSummary && q.easyExplanation.length));
  assert(expanded.questions.every(q => !q.parts && (q.studyParts?.length
    ? q.studyParts.every(p => p.responseType === 'choice' && [2, 4].includes(p.choices.length))
    : q.choices.length === 4)), 'retain one page per official question; answer each choice subquestion independently');
  for (const q of expanded.questions) {
    if (q.preFigureImage) assert(q.preFigures.some(f => f.figureImage === q.preFigureImage && f.caption));
    if (q.figureImage && q.figureImage !== q.preFigureImage) {
      assert([...q.easyExplanation,...(q.studyParts??[]).flatMap(p=>p.easyExplanation??[])].some(s => s.figures?.some(f => f.figureImage === q.figureImage && f.caption)), q.number + ': explanation figure lost');
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
for name in ('math-basics','solid-basics','heat-basics','fem-basics','fem-practice','numerical-basics','element-tech','modeling-basics','boundary-conditions','prepost-basics','verification-basics','computer-basics','ethics','thermal2-01-math-basics','thermal2-02-fluid-basics','thermal2-03-thermo-heat','thermal2-04-numerical-methods','thermal2-05-grid-generation','thermal2-06-turbulence','thermal2-07-boundary-conditions','thermal2-08-post-processing','thermal2-09-verification','thermal2-10-computer-basics','thermal2-11-ethics'):
 d=json.loads(Path('content/questions/'+name+'.json').read_bytes())
 require_editorial_review(d)
 bad=copy.deepcopy(d);bad['questions'][0].pop('answerSummary')
 assert easy_explanation_errors(bad),'guided mode needs an answer summary even without a length floor'
 bad=copy.deepcopy(d);bad['meta']['explanationMode']='standard'
 for q in bad['questions']: q.pop('explanationMode',None)
 bad['questions'][0]['easyExplanation']=[{'title':'test','body':'short'}]
 assert any('1200' in e for e in easy_explanation_errors(bad)),'non-guided explanations retain their existing rule'
 bad=copy.deepcopy(d);bad['questions'][0]['answerSummary']='unrendered ^T'
 assert presentation_errors(bad),'unrendered formulas must still fail'
`], {stdio: 'pipe'});
console.log('Solid2 and Thermal2 unified chapters: IDs, choice grouping, inline figures and quality gates PASS');

// 質問の数だけ回答できる小問を置く。組合せ形式を例外にしない。
for (const [file, pageCount, responseCount] of [['vib1-01-analytical-mechanics',22,75],['vib1-02-vibration-engineering',45,107],['vib1-03-finite-element-technology',30,79],['vib1-04-coupling-boundary',22,53],['vib1-05-structural-coupled-systems',21,63],['vib1-06-acoustic-coupled-systems',37,100],['vib1-07-fluid-coupled-systems',21,65],['vib1-08-numerical-computation',37,93],['vib1-09-result-verification',26,68],['vib2-01-math-basics',18,30],['vib2-02-dynamics',23,40],['vib2-03-strength-of-materials',17,24],['vib2-04-vibration-acoustics',44,64],['vib2-05-fem-basics',19,37],['vib2-06-element-meshing',13,22],['vib2-09-numerical-methods',19,51],['vib2-10-post-processing',19,39],["vib2-07-modeling-basics",19,49],["vib2-08-boundary-load-conditions",21,44],["vib2-11-result-verification",23,66],["vib2-12-computer-basics",17,19],["vib2-13-ethics",7,15]]) {
 const source=JSON.parse(fs.readFileSync('content/questions/'+file+'.json','utf8'));
 const expanded=parts.expandChapter(source);
 assert.equal(expanded.questions.length,pageCount);
 assert.equal(source.questions.reduce((n,q)=>n+(q.studyParts?.length??1),0),responseCount);
 assert(expanded.questions.every(q=>q.explanationMode==='guided'));
 for(const q of source.questions) {
   assert.deepEqual(q.officialQuestionItems,q.studyParts?.map(p=>p.officialQuestionItem)??['main']);
   if(q.studyParts?.length) {
     const answered=Object.fromEntries(q.studyParts.map(p=>[p.id,{choice:p.answer}]));
     assert(parts.studyResult(q.studyParts,answered).correct);
     delete answered[q.studyParts.at(-1).id];
     assert(!parts.studyResult(q.studyParts,answered).complete);
   }
 }
}
require('node:child_process').execFileSync('python',['-c',`
import json,copy,sys
from pathlib import Path
sys.path.insert(0,'tools')
from check_quality import require_editorial_review,study_parts_errors
for file in ('vib1-01-analytical-mechanics','vib1-02-vibration-engineering','vib1-03-finite-element-technology','vib1-04-coupling-boundary','vib1-05-structural-coupled-systems','vib1-06-acoustic-coupled-systems','vib1-07-fluid-coupled-systems','vib1-08-numerical-computation','vib1-09-result-verification','vib2-01-math-basics','vib2-02-dynamics','vib2-03-strength-of-materials','vib2-04-vibration-acoustics','vib2-05-fem-basics','vib2-06-element-meshing','vib2-09-numerical-methods','vib2-10-post-processing','vib2-07-modeling-basics','vib2-08-boundary-load-conditions','vib2-11-result-verification','vib2-12-computer-basics','vib2-13-ethics'):
 d=json.loads(Path('content/questions/'+file+'.json').read_bytes())
 require_editorial_review(d)
 bad=copy.deepcopy(d)
 q=next(q for q in bad['questions'] if len(q.get('studyParts',[]))>1)
 q['studyParts'].pop()
 assert study_parts_errors(bad),'missing combination item must block release'
 bad=copy.deepcopy(d)
 q=next(q for q in bad['questions'] if len(q.get('studyParts',[]))>1)
 q['studyParts'][1]['officialQuestionItem']=q['studyParts'][0]['officialQuestionItem']
 assert study_parts_errors(bad),'duplicate item cannot cover another question'
`],{stdio:'pipe'});
console.log('Vibration2: all question items independently answerable on shared pages PASS');

// 固体・熱流体の既存教材も、公式番号のページと各回答項目の対応を保持する。
const expectedCoverage = {
  '固体力学 1級': [212,443,107], '固体力学 2級': [326,400,0],
  '熱流体力学 1級': [352,628,78], '熱流体力学 2級': [184,263,0],
};
const actualCoverage = Object.fromEntries(Object.keys(expectedCoverage).map(k=>[k,[0,0,0]]));
for(const file of fs.readdirSync('content/questions').filter(f=>f.endsWith('.json'))) {
 const source=JSON.parse(fs.readFileSync('content/questions/'+file,'utf8'));
 const totals=actualCoverage[source.meta?.grade];if(!totals)continue;
 assert.equal(source.meta.questionCoverageVersion,'all-items-v1');
 const expanded=parts.expandChapter(source);
 assert.deepEqual(Array.from(expanded.questions,q=>q.id),source.questions.map(q=>q.id));
 for(const q of source.questions) {
   totals[0]++;totals[1]+=q.studyParts?.length||1;
   totals[2]+=(q.studyParts||[]).filter(p=>p.responseType==='written').length;
   assert.deepEqual(q.officialQuestionItems,q.studyParts?.map(p=>p.officialQuestionItem)??['main']);
   if(q.studyParts?.length>1) {
     assert(q.sharedQuestion?.trim());
     const responses=Object.fromEntries(q.studyParts.map(p=>[p.id,p.responseType==='written'?{revealed:true,understood:true}:{choice:p.answer}]));
     assert(parts.studyResult(q.studyParts,responses).correct);
     delete responses[q.studyParts.at(-1).id];
     assert(!parts.studyResult(q.studyParts,responses).complete);
   }
 }
}
assert.deepEqual(actualCoverage,expectedCoverage);
console.log('Registered official-question items: stable pages, separate responses, written evidence and totals PASS');

// 複数図を、小問ごとに保持する。
const layer=JSON.parse(fs.readFileSync('content/questions/thermal1-22-turbulent-flame.json','utf8')).questions.find(q=>q.number==='22-13');
assert(layer.preFigures.some(f=>f.figureImage==='t1e22MixLayerPdf'));
assert.deepEqual(layer.studyParts.map(p=>p.easyExplanation.flatMap(s=>s.figures||[]).map(f=>f.figureImage).filter(k=>k.startsWith('t1e22MixLayerPdfPoint'))),[1,2,3,4].map(n=>['t1e22MixLayerPdfPoint'+n]));
console.log('Multiple figures: shared setup and a matching figure for each response PASS');

// 第3・4章は保存済み公式の各質問・空欄と照合した項目を固定する。
const vibration34Items = {
  "3": {
    "4": [
      "a",
      "b"
    ],
    "5": [
      "a",
      "b",
      "c"
    ],
    "8": [
      "a",
      "b"
    ],
    "14": [
      "a",
      "b"
    ],
    "16": [
      "moment",
      "shear"
    ],
    "17": [
      "deflection",
      "moment"
    ]
  },
  "4": {
    "11": [
      "a",
      "b"
    ],
    "12": [
      "a",
      "b"
    ],
    "17": [
      "a",
      "b"
    ],
    "20": [
      "value",
      "unit"
    ],
    "21": [
      "zeta",
      "omega-d"
    ],
    "24": [
      "mass",
      "stiffness"
    ],
    "26": [
      "translation",
      "rotation"
    ],
    "28": [
      "omega1",
      "omega2"
    ],
    "29": [
      "a",
      "b",
      "c"
    ],
    "30": [
      "omega1",
      "omega2"
    ],
    "31": [
      "phi1",
      "phi2"
    ],
    "32": [
      "modal-mass",
      "modal-stiffness"
    ],
    "33": [
      "max",
      "norm",
      "mass"
    ],
    "34": [
      "amplitude1",
      "amplitude2"
    ],
    "36": [
      "initial",
      "boundary"
    ],
    "39": [
      "a",
      "b",
      "c"
    ],
    "40": [
      "a",
      "b"
    ]
  }
};
for(const [file,ch] of [['vib2-03-strength-of-materials',3],['vib2-04-vibration-acoustics',4]]) {
 const data=JSON.parse(fs.readFileSync('content/questions/'+file+'.json','utf8'));
 for(const q of data.questions) {
  const n=Number(q.number.split('-')[1]);
  assert.deepEqual(q.studyParts?.map(p=>p.officialQuestionItem)??['main'],vibration34Items[ch][n]??['main'],q.number+': official question item missing');
 }
}

// 保存済み公式第5・6章の質問・空欄と照合して確定した項目。
const vibration56Items = {
  "5": {
    "3": [
      "displacement",
      "slope"
    ],
    "6": [
      "a",
      "b",
      "c",
      "d"
    ],
    "7": [
      "a",
      "b",
      "c"
    ],
    "8": [
      "a",
      "b",
      "c",
      "d"
    ],
    "9": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "10": [
      "a",
      "b"
    ],
    "17": [
      "a",
      "b",
      "c"
    ],
    "18": [
      "a",
      "b",
      "c"
    ]
  },
  "6": {
    "1": [
      "a",
      "b"
    ],
    "3": [
      "a",
      "b",
      "c"
    ],
    "4": [
      "a",
      "b",
      "c"
    ],
    "5": [
      "a",
      "b"
    ],
    "9": [
      "a",
      "b"
    ],
    "12": [
      "a",
      "b"
    ],
    "13": [
      "a",
      "b"
    ]
  }
};
for(const [file,ch] of [['vib2-05-fem-basics',5],['vib2-06-element-meshing',6]]) {
 const data=JSON.parse(fs.readFileSync('content/questions/'+file+'.json','utf8'));
 for(const q of data.questions){
  const n=Number(q.number.split('-')[1]);
  assert.deepEqual(q.studyParts?.map(p=>p.officialQuestionItem)??['main'],vibration56Items[ch][n]??['main'],q.number+': official question item missing');
 }
}

// 保存済み公式第9・10章の質問・空欄・分類項目と照合した対応。
const vibration910Items = {
  "9": {
    "1": [
      "matrix",
      "solution"
    ],
    "2": [
      "a",
      "b",
      "c",
      "d"
    ],
    "3": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "5": [
      "a",
      "b",
      "c",
      "d"
    ],
    "9": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "10": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "11": [
      "a",
      "b",
      "c",
      "d"
    ],
    "12": [
      "a",
      "b",
      "c"
    ],
    "13": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "16": [
      "a",
      "b",
      "c"
    ],
    "17": [
      "a",
      "b",
      "c"
    ]
  },
  "10": {
    "2": [
      "a",
      "b"
    ],
    "3": [
      "a",
      "b",
      "c"
    ],
    "4": [
      "a",
      "b",
      "c"
    ],
    "5": [
      "a",
      "b",
      "c"
    ],
    "6": [
      "a",
      "b"
    ],
    "8": [
      "a",
      "b",
      "c"
    ],
    "11": [
      "a",
      "b",
      "c"
    ],
    "12": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "13": [
      "a",
      "b",
      "c"
    ],
    "15": [
      "formula",
      "reference"
    ],
    "19": [
      "a",
      "b"
    ]
  }
};
for(const [file,ch] of [['vib2-09-numerical-methods',9],['vib2-10-post-processing',10]]) {
 const data=JSON.parse(fs.readFileSync('content/questions/'+file+'.json','utf8'));
 for(const q of data.questions) {
  assert.deepEqual(q.studyParts?.map(p=>p.officialQuestionItem)??['main'],vibration910Items[ch][Number(q.number.split('-')[1])]??['main'],q.number+': official question item missing');
 }
}

// 第7・8・11〜13章：保存済み公式の独立した空欄・判定項目を保持。
const vibrationRemainingItems = {
  "7": {
    "2": [
      "a",
      "b"
    ],
    "3": [
      "a",
      "b",
      "c"
    ],
    "5": [
      "a",
      "b",
      "c"
    ],
    "7": [
      "a",
      "b",
      "c"
    ],
    "8": [
      "a",
      "b"
    ],
    "9": [
      "a",
      "b"
    ],
    "10": [
      "a",
      "b",
      "c"
    ],
    "11": [
      "a",
      "b"
    ],
    "13": [
      "a",
      "b",
      "c"
    ],
    "14": [
      "a",
      "b",
      "c",
      "d"
    ],
    "15": [
      "a",
      "b",
      "c"
    ],
    "16": [
      "a",
      "b",
      "c",
      "d"
    ],
    "17": [
      "a",
      "b",
      "c"
    ],
    "18": [
      "a",
      "b",
      "c",
      "d"
    ],
    "19": [
      "a",
      "b",
      "c",
      "d"
    ]
  },
  "8": {
    "4": [
      "tx",
      "ty",
      "tz",
      "rx",
      "ry",
      "rz"
    ],
    "5": [
      "tx",
      "ty",
      "tz",
      "rx",
      "ry",
      "rz"
    ],
    "6": [
      "a",
      "b"
    ],
    "7": [
      "a",
      "b"
    ],
    "9": [
      "a",
      "b"
    ],
    "10": [
      "a",
      "b",
      "c"
    ],
    "11": [
      "a",
      "b"
    ],
    "12": [
      "a",
      "b"
    ],
    "14": [
      "a",
      "b"
    ],
    "18": [
      "a",
      "b",
      "c"
    ],
    "20": [
      "a",
      "b",
      "c"
    ],
    "21": [
      "a",
      "b"
    ]
  },
  "11": {
    "2": [
      "a",
      "b"
    ],
    "4": [
      "a",
      "b"
    ],
    "8": [
      "a",
      "b",
      "c"
    ],
    "11": [
      "a",
      "b",
      "c"
    ],
    "12": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "13": [
      "a",
      "b",
      "c"
    ],
    "14": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "15": [
      "a",
      "b",
      "c"
    ],
    "16": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "17": [
      "a",
      "b",
      "c",
      "d"
    ],
    "18": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "19": [
      "a",
      "b",
      "c",
      "d",
      "e"
    ],
    "20": [
      "a",
      "b",
      "c",
      "d"
    ],
    "21": [
      "a",
      "b",
      "c"
    ],
    "22": [
      "a",
      "b",
      "c"
    ],
    "23": [
      "a",
      "b",
      "c",
      "d"
    ]
  },
  "12": {
    "5": [
      "a",
      "b",
      "c"
    ]
  },
  "13": {
    "4": [
      "a",
      "b",
      "c"
    ],
    "6": [
      "a",
      "b",
      "c",
      "d"
    ],
    "7": [
      "a",
      "b",
      "c",
      "d"
    ]
  }
};
for(const [file,ch] of [["vib2-07-modeling-basics",7],["vib2-08-boundary-load-conditions",8],["vib2-11-result-verification",11],["vib2-12-computer-basics",12],["vib2-13-ethics",13]]) {
 const data=JSON.parse(fs.readFileSync("content/questions/"+file+".json","utf8"));
 for(const q of data.questions) assert.deepEqual(q.studyParts?.map(p=>p.officialQuestionItem)??["main"],vibrationRemainingItems[ch][Number(q.number.split("-")[1])]??["main"],q.number+": official item missing");
}

// 振動1級1〜9章：保存済み公式の空欄・候補ごとの問いを保持する。
const vibration1Items = {
  1: {1:'a b c',2:'a b c d',3:'a b c',4:'a b c',5:'a b c d',6:'a b c',7:'a b c',8:'a b c',9:'a b c',10:'a b c d',11:'a b c',12:'a-T a-U a-W b-M b-K b-F c',13:'a b c',14:'candidate-1 candidate-2 candidate-3 candidate-4',15:'candidate-1 candidate-2 candidate-3 candidate-4 candidate-5',16:'a b c',17:'a b c',18:'a b',19:'a b c',20:'a b c',21:'a b c',22:'a b c'},
  2: {3:'a b',5:'a b c',6:'a b c d',7:'a b c',8:'a b',9:'a b c',10:'a b c',11:'a b c',17:'a b c',18:'a b c',19:'a b c',20:'a b c',21:'a b',22:'a b c',23:'a b',25:'a b c',26:'a b c d',27:'a b c',28:'a b c',29:'a b',30:'statement-1 statement-2 statement-3 statement-4 statement-5',31:'a b c',32:'a b',33:'a b',34:'a b c',35:'a b',36:'a b c',37:'a b',38:'a b c d',41:'a b c',42:'a b c',43:'a b c',44:'a b',45:'a b'}
};
Object.assign(vibration1Items,{
  "3": {
    "1": "a b c",
    "2": "a b c",
    "3": "a b c d",
    "4": "a b c",
    "5": "a b c",
    "6": "a b c",
    "7": "a b c",
    "8": "a b c d",
    "9": "a b c",
    "10": "a b",
    "12": "a b c d",
    "13": "a b",
    "15": "N1 N2",
    "16": "N1 N2",
    "18": "a b c d",
    "19": "a b c",
    "22": "a b c",
    "23": "a b c",
    "24": "a b",
    "25": "a b c",
    "26": "a b c",
    "27": "a b c",
    "28": "a b c",
    "29": "a b c d",
    "30": "M K"
  },
  "4": {
    "1": "a b c",
    "3": "a b c d e",
    "4": "a b c",
    "5": "a b c d",
    "6": "a b c d",
    "8": "a b",
    "9": "a b",
    "10": "a b",
    "13": "y I",
    "14": "a b c d e",
    "17": "a b c d",
    "18": "a b c d",
    "20": "a b c d"
  }
});
Object.assign(vibration1Items,{
  "5": {
    "1": "a b c",
    "2": "a b c",
    "3": "a b",
    "4": "a b c",
    "5": "a b c",
    "7": "a b c",
    "8": "a b c d",
    "9": "a b c",
    "10": "a b c",
    "11": "a b c",
    "12": "a b c d e",
    "13": "a b c d",
    "14": "a b c",
    "15": "a b c",
    "16": "a b c",
    "18": "a b c",
    "19": "a b c d",
    "20": "a b c",
    "21": "a b c"
  },
  "6": {
    "1": "a b c d",
    "2": "a b c",
    "3": "a b c d",
    "4": "a b c",
    "5": "a b c",
    "6": "a b c",
    "7": "a b c",
    "9": "a b c",
    "10": "a b c d",
    "11": "a b c",
    "12": "a b c",
    "13": "a b",
    "14": "a b c",
    "15": "a b c",
    "16": "a b",
    "17": "a b c",
    "18": "a b c d",
    "19": "a b c",
    "20": "a b c d",
    "21": "a b",
    "22": "a b c",
    "23": "a b c",
    "25": "a b c",
    "28": "a b c",
    "29": "a b c d",
    "30": "a b c",
    "33": "a b c d",
    "34": "a b c d",
    "37": "a b c"
  }
});
Object.assign(vibration1Items,{
  "7": {
    "1": "a b c",
    "2": "a b c",
    "3": "a b c",
    "4": "a b c",
    "5": "a b c",
    "6": "a b c",
    "7": "a b c",
    "8": "a b c",
    "9": "a b c",
    "10": "a b c",
    "11": "a b c d",
    "12": "a b c d",
    "13": "a b c d",
    "14": "a b c",
    "15": "a b c d",
    "16": "a b c",
    "19": "a b c",
    "20": "a b c d",
    "21": "a b c d"
  },
  "8": {
    "1": "a b c d",
    "2": "a b c d",
    "3": "a b c",
    "4": "a b c",
    "5": "a b",
    "6": "a b c",
    "7": "a b c",
    "8": "a b c d",
    "9": "a b c",
    "10": "a b c",
    "11": "a b c",
    "13": "other self",
    "17": "a b",
    "21": "a b c d",
    "22": "a b c d e f",
    "23": "a b c d",
    "24": "a b c d",
    "28": "a b c",
    "29": "subsystem-1 subsystem-3",
    "30": "a b c",
    "31": "a b c d",
    "32": "a b c d",
    "33": "a b c",
    "36": "a b c d"
  },
  "9": {
    "1": "a b",
    "2": "a b c d",
    "3": "a b c d",
    "5": "a b c d",
    "6": "i ro ha ni",
    "7": "a b c",
    "8": "a b c",
    "10": "a b c",
    "11": "a b c d",
    "12": "a b c",
    "13": "a b c d",
    "15": "a b c",
    "17": "a b c",
    "18": "a b c d",
    "19": "a b",
    "22": "a b c",
    "23": "a b c d",
    "26": "a b c"
  }
});
for(const [file,ch] of [['vib1-01-analytical-mechanics',1],['vib1-02-vibration-engineering',2],['vib1-03-finite-element-technology',3],['vib1-04-coupling-boundary',4],['vib1-05-structural-coupled-systems',5],['vib1-06-acoustic-coupled-systems',6],['vib1-07-fluid-coupled-systems',7],['vib1-08-numerical-computation',8],['vib1-09-result-verification',9]]){
 const d=JSON.parse(fs.readFileSync('content/questions/'+file+'.json','utf8'));
 for(const q of d.questions){
  assert.deepEqual(q.studyParts?.map(p=>p.officialQuestionItem)??['main'],(vibration1Items[ch][Number(q.number.split('-')[1])]??'main').split(' '),q.id+': official item missing');
  assert((q.studyParts??[q]).every(p=>p.responseType!=='written'),'公式にない記述問題を加えない');
  assert((q.studyParts??[q]).every(p=>!p.title.includes('$')),'見出しは通常Textのため数式コードを置かない');
  for(const p of q.studyParts??[])assert(p.easyExplanation.some(s=>s.title==='選択肢を確かめる'),p.id+': incorrect-choice explanation must be visible');
 }
}
console.log('Vibration1 chapters 1-9: 261 official-number pages, 703 answers PASS');
