# -*- coding: utf-8 -*-
"""固体2級第3章だけを生成する。回答後は1問につき問題・図／4節解説の2ページ。"""
from pathlib import Path
import json,re,sys,shutil
from build_solid_beforeafter_pdfs import esc,fig_block,expl_html,build_html
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'アプリ/固体2級'
TMP=ROOT/'tmp/pdfs/ch3_final'
TMP.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'content/questions/heat-basics.json').read_text(encoding='utf-8'))
terms=json.loads((ROOT/'content/formulas/ch3.json').read_text(encoding='utf-8'))
relation=next(it for it in terms['items'] if it['id']=='heat-transfer-rate-resistance')
assert data['meta']['grade']=='固体力学 2級' and data['meta']['chapter']==3 and len(data['questions'])==17
stem='固体2級_第3章_熱伝導の基礎'
after_base=build_html(data,'固体','2級',True)
head=after_base.split('</head>')[0]
css='''<style>
@page { size:A4; margin:14mm 14mm 12mm; }
body { font-family:'Meiryo','Yu Gothic',sans-serif; font-size:11pt; line-height:1.8; margin:0; }
.sheet { break-before:page; }
.sheet:first-child { break-before:auto; }
.running { color:#666; font-size:8.5pt; border-bottom:1px solid #ccc; padding-bottom:3mm; margin-bottom:5mm; }
.pagehead { font-size:14pt; font-weight:700; color:#1F3A65; margin:0 0 5mm; }
.q { margin:0 0 5mm; white-space:pre-line; }
.choices { margin:0 0 5mm; padding-left:7mm; }
.choices li { padding:1mm 0; break-inside:avoid; }
.choices li.ok { background:#eaf7ee; font-weight:700; }
.ans { margin:0 0 4mm; color:#1F3A65; font-weight:700; }
.fig { margin:3mm 0 0; text-align:center; }
.fig img { display:inline-block; width:155mm; max-width:100%; height:auto; border:1px solid #ddd; border-radius:5px; }
.figure-label { color:#666; font-size:8.5pt; text-align:center; margin:2mm 0 0; }
.exp { background:none; border:none; padding:0; border-radius:0; font-size:11pt; line-height:1.8; }
.eline { margin:0 0 5mm; break-inside:avoid; }
.section-label { color:#1F3A65; font-weight:700; }
.term-link { margin-top:5mm; font-size:10pt; }
.term-link a { color:#1877B8; text-decoration:underline; }
.term-copy { font-size:10.5pt; line-height:1.8; }
mjx-container { overflow:visible; }
</style>'''
body=[]
for q in data['questions']:
    choices=''.join(f'<li class="{"ok" if i+1==q["answer"] else ""}">{esc(c)}</li>' for i,c in enumerate(q['choices']))
    common=f'<div class="running">第3章 熱伝導の基礎 ／ 固体2級・オリジナル問題 ／ 回答後</div>'
    body.append(f'<section class="sheet question-sheet">{common}<h2 class="pagehead">{esc(q["number"])}　{esc(q["title"])}</h2><div class="q">{esc(q["question"])}</div><ol class="choices">{choices}</ol><div class="ans">正解：{q["answer"]}</div>{fig_block(q["figureImage"])}<div class="figure-label">回答後用の理解補助図　／　4節解説は次ページ</div></section>')
    explanation=expl_html(q['explanation'])
    explanation=re.sub(r'(【(?:基礎|考え方|ポイント|引っかけ)】)',r'<span class="section-label">\1</span>',explanation)
    termlink='<div class="term-link"><a href="#rate-resistance">関連用語：熱通過率Kと熱抵抗Rの関係（巻末）</a></div>' if relation['id'] in q.get('relatedFormulas',[]) else ''
    body.append(f'<section class="sheet explanation-sheet">{common}<h2 class="pagehead">{esc(q["number"])}　解説</h2><div class="exp">{explanation}</div>{termlink}</section>')

body.append(f'<section class="sheet glossary-sheet" id="rate-resistance"><div class="running">第3章 熱伝導の基礎 ／ 関連用語</div><h2 class="pagehead">熱通過率Kと熱抵抗Rの関係</h2><div class="q">同じ経路を、面積当たりで見るか、面積全体で見るかを分けます。</div>{fig_block(relation["figureImage"])}<div class="term-copy"><p>熱流束q：面積当たり（W/m²）。熱流量Q：面積全体（W）。</p><p>面積当たりは $q=K\\Delta T$、面積全体は $Q=Aq=KA\\Delta T=\\Delta T/R$。</p><p>したがって $R=1/(KA)$。KとRを比べるときは、面積Aを含めて換算します。</p></div></section>')
body.append(f'<section class="sheet glossary-sheet"><div class="running">第3章 熱伝導の基礎 ／ 関連用語・計算例</div><h2 class="pagehead">用語の意味と、面積を含む計算</h2><div class="term-copy"><p>{esc(relation["body"])}</p><h3>数値例</h3><p>{esc(relation["example"])}</p><p>Kの単位に含まれるKは、温度の単位ケルビンです。熱通過率の記号Kとは区別してください。</p></div></section>')
after=head+css+'</head><body>'+''.join(body)+'</body></html>'
before=build_html(data,'固体','2級',False)
before=before.replace('mjx-container{overflow-x:auto;}','mjx-container{overflow:visible;}').replace("<style>","<style>\n.card{white-space:normal;} .q{white-space:pre-line;}\n",1)
tasks=[]
for tag,doc in (('回答前',before),('回答後',after)):
    hp=TMP/(stem+'_'+tag+'.html');hp.write_text(doc,encoding='utf-8')
    pp=OUT/(stem+'_'+tag+'.pdf')
    old=ROOT/'tmp/pdfs/ch3_review'/pp.name
    if pp.exists() and not old.exists():shutil.copy2(pp,old)
    tasks.append({'html':str(hp),'pdf':str(pp),'mode':tag})
(TMP/'tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding='utf-8')
# Prove answer-before HTML contains neither answers, explanations nor after figures.
assert 'class=\'ok\'' not in before and 'class=\'ans\'' not in before
assert '【基礎】' not in before and before.count('data:image/png')==6
print('Chapter 3 HTML: before has six givens figures, no answers; after has 34 question sheets + 2 linked glossary sheets.')
