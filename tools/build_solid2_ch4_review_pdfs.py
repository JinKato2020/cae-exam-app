# -*- coding: utf-8 -*-
"""第4章限定。各問の問題・図と解説を分け、関連用語へPDF内部リンクを付ける。"""
from pathlib import Path
import json,re
from build_solid_beforeafter_pdfs import esc,fig_block,expl_html,build_html,before_fig_key
ROOT=Path(__file__).resolve().parents[1];TMP=ROOT/'tmp/pdfs/ch4_final';OUT=ROOT/'アプリ/固体2級'
TMP.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'content/questions/fem-basics.json').read_bytes())
terms=json.loads((ROOT/'content/formulas/ch4.json').read_bytes());items={i['id']:i for i in terms['items']}
assert data['meta']['chapter']==4 and len(data['questions'])==29
# 最小の機械ゲート：旧体裁、参照切れ、必要なD公式の欠落を出力前に止める。
for q in data['questions']:
 assert len(q['explanation'].splitlines())==4 and all(line.startswith(label) for line,label in zip(q['explanation'].splitlines(),('【基礎】','【考え方】','【ポイント】','【引っかけ】'))),q['number']
 assert all(ident in items for ident in q.get('relatedFormulas',[])),q['number']
q21=next(q for q in data['questions'] if q['number']=='4-21')
assert all(marker in q21['explanation'] for marker in (r'\mathbf D_{\mathrm{ps}}',r'\mathbf D_{\mathrm{pe}}')),'4-21: D formulas missing'
head=build_html(data,'固体','2級',True).split('</head>')[0]
css='''<style>
@page { size:A4; margin:14mm 14mm 12mm; }
body {font-family:'Meiryo','Yu Gothic',sans-serif;font-size:10.5pt;line-height:1.75;margin:0;}
.sheet {break-before:page;} .sheet:first-child {break-before:auto;}
.running {color:#666;font-size:8.5pt;border-bottom:1px solid #ccc;padding-bottom:3mm;margin-bottom:5mm;}
.pagehead {font-size:14pt;font-weight:700;color:#1F3A65;margin:0 0 5mm;}
.q {margin:0 0 5mm;white-space:pre-line;}
.choices {margin:0 0 5mm;padding-left:7mm;} .choices li {padding:1mm 0;break-inside:avoid;}
.choices li.ok {background:#eaf7ee;font-weight:700;}
.ans {margin:0 0 3mm;color:#1F3A65;font-weight:700;}
.fig {margin:3mm 0 0;text-align:center;} .fig img {display:inline-block;width:145mm;max-width:100%;height:auto;border:1px solid #ddd;border-radius:5px;}
.figure-label {color:#666;font-size:8.5pt;text-align:center;margin:2mm 0 0;}
.exp {background:none;border:none;padding:0;border-radius:0;font-size:10.5pt;line-height:1.85;}
.eline {margin:0 0 5mm;break-inside:avoid;} .section-label {color:#1F3A65;font-weight:700;}
.term-link {margin-top:6mm;font-size:10pt;line-height:2;} a {color:#1877B8;text-decoration:underline;}
.term-copy {font-size:10.5pt;line-height:1.85;} .term-copy p {margin-bottom:5mm;}
.term-copy .formula {margin:7mm 0;font-size:10pt;}
.glossary-detail .term-copy {font-size:10.5pt;line-height:1.75;} .glossary-detail .term-copy p {margin:0 0 3mm;}
mjx-container {overflow:visible;}
</style>'''
body=[];linkcount=0
for q in data['questions']:
 choices=''.join(f'<li class="{"ok" if j+1==q["answer"] else ""}">{esc(c)}</li>' for j,c in enumerate(q['choices']))
 common='<div class="running">第4章 有限要素法の定式化 ／ 固体2級・オリジナル問題 ／ 回答後</div>'
 body.append(f'<section class="sheet question-sheet">{common}<h2 class="pagehead">{esc(q["number"])}　{esc(q["title"])}</h2><div class="q">{esc(q["question"])}</div><ol class="choices">{choices}</ol><div class="ans">正解：{q["answer"]}</div>{fig_block(q.get("figureImage"))}<div class="figure-label">回答後用の理解補助図 ／ 解説は次ページ</div></section>')
 explanation=re.sub(r'(【(?:基礎|考え方|ポイント|引っかけ)】)',r'<span class="section-label">\1</span>',expl_html(q['explanation']))
 links=[]
 for ident in q.get('relatedFormulas',[]):
  links.append(f'<a href="#term-{ident}">{esc(items[ident]["term"])}</a>');linkcount+=1
 body.append(f'<section class="sheet explanation-sheet">{common}<h2 class="pagehead">{esc(q["number"])}　解説</h2><div class="exp">{explanation}</div><div class="term-link">関連する公式・用語：<br>{"<br>".join(links)}</div></section>')
expanded={'discretization-workflow','weighted-residual','rayleigh-ritz','finite-difference','shape-function'}
glossary_pages={};sheetcount=58;glossary_figures=0
def term_paragraphs(text):
 return ''.join('<p>'+re.sub(r'(【[^】]+】)',r'<b>\1</b>',esc(part))+'</p>' for part in text.split('\n\n'))
for it in terms['items']:
 glossary_pages[it['id']]=sheetcount
 # Long formulas are split at the logical boundary without changing the mathematics.
 formula=it.get('formula','')
 if it['id']=='thermal-force':
  formula=formula.replace(r',\quad\mathbf K',r'$。$\mathbf K').replace(r'+\int_V\mathbf B^T\mathbf D',r'$ $+\int_V\mathbf B^T\mathbf D').replace(r'-\int_V\mathbf B^T\boldsymbol\sigma_0',r'$ $-\int_V\mathbf B^T\boldsymbol\sigma_0')
 common='<div class="running">第4章 有限要素法の定式化 ／ 関連する公式・用語</div>'
 if it['id'] in expanded:
  intro=it['body'].split('\n\n')[0]
  first_example=f'<div class="term-copy"><h3>節点値から変位とひずみを求める例</h3><p>{esc(it["example"])}</p></div>' if it['id']=='shape-function' else ''
  body.append(f'<section class="sheet glossary-sheet" id="term-{it["id"]}">{common}<h2 class="pagehead">{esc(it["term"])}</h2><div class="term-copy">{term_paragraphs(intro)}</div>{fig_block(it["figureImage"])}{first_example}<div class="figure-label">図で全体像を確認し、次ページで各役割と式を読む</div></section>')
  details='\n\n'.join(it['body'].split('\n\n')[1:]) if it['id']=='shape-function' else it['body']
  example='' if it['id']=='shape-function' else f'<h3>具体的な計算例</h3><p>{esc(it["example"])}</p>'
  body.append(f'<section class="sheet glossary-sheet glossary-detail">{common}<h2 class="pagehead">{esc(it["term"])}：説明</h2><div class="term-copy"><div class="formula">{esc(formula)}</div>{term_paragraphs(details)}{example}</div></section>')
  sheetcount+=2;glossary_figures+=1
 else:
  body.append(f'<section class="sheet glossary-sheet" id="term-{it["id"]}">{common}<h2 class="pagehead">{esc(it["term"])}</h2><div class="term-copy"><div class="formula">{esc(formula)}</div><p>{esc(it["body"])}</p><h3>計算例</h3><p>{esc(it["example"])}</p></div></section>')
  sheetcount+=1
after=head+css+'</head><body>'+''.join(body)+'</body></html>'
before=build_html(data,'固体','2級',False).replace('mjx-container{overflow-x:auto;}','mjx-container{overflow:visible;}')
before=before.replace('<style>','<style>\n.card{white-space:normal;} .q{white-space:pre-line;}\n',1)
assert '【基礎】' not in before and "class='ok'" not in before and "class='ans'" not in before
tasks=[];stem='固体2級_第4章_有限要素法の定式化'
for mode,doc in (('回答前',before),('回答後',after)):
 hp=TMP/(stem+'_'+mode+'.html');hp.write_text(doc,encoding='utf-8')
 tasks.append({'html':str(hp),'pdf':str(OUT/(stem+'_'+mode+'.pdf')),'mode':mode})
(TMP/'tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding='utf-8')
(TMP/'expected.json').write_text(json.dumps({'after_sheets':sheetcount,'after_figures':29+glossary_figures,'after_tags':116,'before_figures':sum(bool(before_fig_key(q)) for q in data['questions']),'links':linkcount,'glossary':list(items),'glossary_pages':glossary_pages},indent=2),encoding='utf-8')
print('HTML prepared; chapter 4 only; glossary links enabled.')
