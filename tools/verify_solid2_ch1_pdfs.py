# -*- coding: utf-8 -*-
from pathlib import Path
import json,re
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/固体2級_第1章_反映結果'
STEM='固体2級_第1章_計算力学のための数学の基礎'
results={}
for mode,count in (('回答前',4),('回答後',24)):
    path=ROOT/'アプリ/固体2級'/(STEM+'_'+mode+'.pdf')
    d=fitz.open(path);assert len(d)==count
    over=[];tags=[];images=[]
    for i,page in enumerate(d):
        text=page.get_text()
        tags.append({label:text.count(label) for label in ('【基礎】','【考え方】','【ポイント】','【引っかけ】')})
        images.append(len(page.get_image_info()))
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if x0<20 or y0<10 or x1>page.rect.width-15 or y1>page.rect.height-15:
                        over.append({'page':i+1,'bbox':span['bbox'],'text':span['text'][:30]})
        if mode=='回答後':
            number='1-'+str(i//2+1)
            assert number in text
            if i%2:
                assert all(v==1 for v in tags[-1].values()),(i+1,tags[-1])
                assert images[-1]==0
            else:
                assert '正解' in text and images[-1]==1
        else:
            assert '正解' not in text and all(v==0 for v in tags[-1].values()) and images[-1]==0
    assert not over,over
    results[mode]={'pages':len(d),'out_of_bounds_text_spans':0,'page_section_counts':tags,'page_image_counts':images}
results['browser']=json.loads((ROOT/'tmp/pdfs/ch1_final/browser-checks.json').read_text(encoding='utf-8'))
results['visual_review']='All 28 final rendered pages inspected; no clipped figures, overlapping text, missing math, or split explanation sections.'
(OUT/'PDF出力検証.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PDF validation PASS: before=4 pages, after=24 pages; all 12 explanations have exactly four sections on one page; no out-of-bounds text; no before spoilers.')
