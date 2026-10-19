# -*- coding: utf-8 -*-
from pathlib import Path
import json,fitz,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];TMP=ROOT/'tmp/pdfs/ch4_final/pages';TMP.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'output/固体2級_第4章_反映結果';expected=json.loads((ROOT/'tmp/pdfs/ch4_final/expected.json').read_text(encoding='utf-8'))
questions=json.loads((ROOT/'content/questions/fem-basics.json').read_bytes())['questions']
results={};stem='固体2級_第4章_有限要素法の定式化'
for mode,tag in (('回答前','before'),('回答後','after')):
 base=ROOT/'tmp/pdfs/ch4_final/print' if '--pending' in sys.argv else ROOT/'アプリ/固体2級'
 doc=fitz.open(base/(stem+'_'+mode+'.pdf'));spills=[];paths=[];sections=[];nimages=0;links=[]
 if mode=='回答後':assert len(doc)==expected['after_sheets'],len(doc)
 for i,p in enumerate(doc):
  tx=p.get_text();labels={l:tx.count(l) for l in ('【基礎】','【考え方】','【ポイント】','【引っかけ】')}
  sections.append(labels);ni=len(p.get_image_info());nimages+=ni
  if mode=='回答後' and i<58:
   assert f'4-{i//2+1}' in tx,(i+1,tx[:100])
   if i%2:assert all(n==1 for n in labels.values()) and ni==0,(i+1,labels,ni)
   else:assert '正解' in tx and ni==1,(i+1,tx[:100],ni)
  elif mode=='回答前':assert '正解' not in tx and not any(labels.values()),i+1
  else:assert '関連する公式・用語' in tx and not any(labels.values()),i+1
  for b in p.get_text('dict')['blocks']:
   for line in b.get('lines',[]):
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     if x0<20 or y0<10 or x1>p.rect.width-15 or y1>p.rect.height-15:spills.append({'page':i+1,'bbox':span['bbox'],'text':span['text'][:40]})
  for a in p.get_links():
   assert a['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED),a
   assert 58<=a.get('page',-1)<len(doc),a;links.append(a['page'])
  if mode=='回答後' and i<58 and i%2:
   assert [a.get('page') for a in p.get_links()]==[expected['glossary_pages'][ident] for ident in questions[i//2].get('relatedFormulas',[])],i+1
  dest=TMP/f'{tag}-{i+1}.png';p.get_pixmap(matrix=fitz.Matrix(1.15,1.15)).save(dest);paths.append(dest)
 assert not spills,spills
 assert nimages==(expected['after_figures'] if mode=='回答後' else expected['before_figures'])
 if mode=='回答後':assert len(links)==expected['links'],links
 for k in range(0,len(paths),6):
  sheet=Image.new('RGB',(1500,1460),'white');draw=ImageDraw.Draw(sheet)
  for j,pth in enumerate(paths[k:k+6]):
   a=Image.open(pth);a.thumbnail((490,695));x=j%3*500;y=j//3*730
   sheet.paste(a,(x,y));draw.text((x+8,y+701),pth.stem,fill='black')
  sheet.save(TMP/f'{tag}-contact-{k//6+1}.png')
 results[mode]={'pages':len(doc),'figures':nimages,'links':len(links),'out_of_bounds_text':spills,'section_counts':sections}
results['browser']=json.loads((ROOT/'tmp/pdfs/ch4_final/browser-checks.json').read_text(encoding='utf-8'))
(OUT/'PDF出力検証.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({k:dict(pages=v['pages'],figures=v['figures'],links=v['links']) for k,v in results.items() if k!='browser'})
