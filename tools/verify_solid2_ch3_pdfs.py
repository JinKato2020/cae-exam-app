# -*- coding: utf-8 -*-
from pathlib import Path
import json
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第3章_反映結果'
TMP=ROOT/'tmp/pdfs/ch3_final/pages';TMP.mkdir(parents=True,exist_ok=True)
STEM='固体2級_第3章_熱伝導の基礎'
results={}
for mode,count,tag in (('回答前',9,'before'),('回答後',36,'after')):
    path=ROOT/'アプリ/固体2級'/(STEM+'_'+mode+'.pdf')
    doc=fitz.open(path);assert len(doc)==count
    tags=[];images=[];spills=[];pagepaths=[]
    for i,p in enumerate(doc):
        text=p.get_text();sections={label:text.count(label) for label in ('【基礎】','【考え方】','【ポイント】','【引っかけ】')}
        tags.append(sections);images.append(len(p.get_image_info()))
        if mode=='回答後' and i<34:
            assert f'3-{i//2+1}' in text
            if i%2:assert all(v==1 for v in sections.values()) and images[-1]==0
            else:assert '正解' in text and images[-1]==1
        elif mode=='回答後':assert '熱' in text and all(v==0 for v in sections.values())
        else:assert '正解' not in text and all(v==0 for v in sections.values())
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if x0<20 or y0<10 or x1>p.rect.width-15 or y1>p.rect.height-15:spills.append({'page':i+1,'bbox':span['bbox'],'text':span['text'][:35]})
        target=TMP/f'{tag}-{i+1}.png';p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(target);pagepaths.append(target)
    assert not spills,spills
    assert sum(images)==(18 if mode=='回答後' else 6)
    if mode=='回答後':
        destinations=[link.get('page') for p in doc for link in p.get_links()]
        assert len(destinations)==7 and all(page==34 for page in destinations),destinations
    results[mode]={'pages':len(doc),'out_of_bounds_text_spans':0,'page_section_counts':tags,'page_image_counts':images}
    for k in range(0,len(pagepaths),4):
        sheet=Image.new('RGB',(1192,1740),'white');draw=ImageDraw.Draw(sheet)
        for j,p in enumerate(pagepaths[k:k+4]):
            sheet.paste(Image.open(p).resize((596,843)),((j%2)*596,(j//2)*870))
            draw.text(((j%2)*596+5,(j//2)*870+844),p.stem,fill='black')
        sheet.save(TMP/f'{tag}-contact-{k//4+1}.png')
results['browser']=json.loads((ROOT/'tmp/pdfs/ch3_final/browser-checks.json').read_text(encoding='utf-8'))
(OUT/'PDF出力検証.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PDF PASS: before=9 pages/6 figures; after=36 pages/18 figures/68 sections; 7 links reach glossary page35; no text spills.')
