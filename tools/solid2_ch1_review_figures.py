# -*- coding: utf-8 -*-
"""第1章の回答後SVGを配置し、パス化文字を1320×840 PNGへレンダする。"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import math, json, shutil, zipfile
import xml.etree.ElementTree as ET
import fitz
from compress_figures import compress_bytes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/固体2級_第1章_反映結果'
DEST=ROOT/'図/固体2級/第01章'
DEST.mkdir(parents=True,exist_ok=True)
N,R,G,F,W='#1F3A65','#C82D2D','#888888','#E1E7F2','#FFFFFF'
font=TTFont('C:/Windows/Fonts/meiryo.ttc',fontNumber=0)
glyphs=font.getGlyphSet(); cmap=font.getBestCmap(); units=font['head'].unitsPerEm
class SVG:
    def __init__(self,title):self.p=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 420" width="660" height="420" role="img"><title>{title}</title><rect width="660" height="420" fill="{W}"/>']
    def text(self,x,y,label,size=17,color=N,center=False):
        width=sum(glyphs[cmap[ord(c)]].width*size/units for c in label)
        if center:x-=width/2
        assert x>=0 and x+width<=660,(label,x,width)
        self.p.append(f'<g aria-label="{label}" fill="{color}">')
        for c in label:
            name=cmap[ord(c)]; pen=SVGPathPen(glyphs); glyphs[name].draw(pen)
            self.p.append(f'<path d="{pen.getCommands()}" transform="translate({x:.3f} {y}) scale({size/units:.6f} {-size/units:.6f})"/>')
            x+=glyphs[name].width*size/units
        self.p.append('</g>')
    def rect(self,x,y,w,h,fill=F,stroke=None):self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')
    def path(self,points,color=N,width=2):
        coords=' '.join(('M' if i==0 else 'L')+f'{x:.2f} {y:.2f}' for i,(x,y) in enumerate(points))
        self.p.append(f'<path d="{coords}" stroke="{color}" stroke-width="{width}" fill="none"/>')
    def arrow(self,x,y,X,Y,color=G,width=1.6):
        self.path([(x,y),(X,Y)],color,width)
        dx,dy=X-x,Y-y;L=math.hypot(dx,dy);dx/=L;dy/=L
        self.p.append(f'<path d="M{X} {Y} L{X-9*dx-4*dy} {Y-9*dy+4*dx} L{X-9*dx+4*dy} {Y-9*dy-4*dx} Z" fill="{color}"/>')
    def save(self,name):
        path=DEST/name;path.write_text(''.join(self.p)+'</svg>',encoding='utf-8');return path

# Retain reviewed layout and outlined text for nine existing completed diagrams.
for folder in ('固体2級_1-1から1-3_校閲','固体2級_1-4から1-12_校閲'):
    for src in (ROOT/'output'/folder).glob('*.svg'):
        raw=src.read_text(encoding='utf-8')
        if 'width' not in ET.fromstring(raw).attrib:raw=raw.replace('viewBox="0 0 660 420"','viewBox="0 0 660 420" width="660" height="420"',1)
        (DEST/src.name).write_text(raw,encoding='utf-8')

d=SVG('行列式：定数倍・積・和の違い')
d.text(330,32,'行列式：図形を変える倍率から整理する',19,center=True)
d.rect(31,52,598,37);d.text(330,77,'二次の例：I₂ と 2I₂',17,center=True)
d.rect(100,127,60,60,F,N);d.rect(414,108,120,120,F,R)
d.text(130,218,'面積1',18,center=True);d.text(474,258,'面積4',18,R,center=True)
d.arrow(223,158,357,158);d.text(290,137,'横も縦も2倍',16,center=True)
d.text(330,297,'定数倍：det(2I₂) = 2² det(I₂) = 4',18,R,center=True)
d.text(330,334,'積：det(AB) = det(A) det(B)',18,center=True)
d.text(330,371,'和の反例：det(I₂ + I₂) = 4 ≠ 1 + 1',17,R,center=True)
d.text(330,405,'行列全体の和は、行列式の和に分けられない',16,center=True)
d.save('1-2_determinant_rules_after.svg')

d=SVG('静的解析の境界条件と時間の初期条件')
d.text(330,31,'静的解析：時間の出発点より、釣り合いの条件',18,center=True)
d.rect(125,132,365,43,F,N);d.path([(124,97),(124,207)],N,3)
for yy in range(100,204,15):d.path([(105,yy+12),(124,yy)],G,1.4)
d.arrow(490,154,596,154,R,3)
d.text(93,235,'左端：変位0',16,center=True);d.text(533,119,'右端：力P',16,R,center=True)
d.text(330,92,'例：左端を固定した棒を引く',17,center=True)
d.rect(28,269,290,101);d.rect(342,269,290,101)
d.text(173,294,'境界条件：場所の指定',17,center=True)
d.text(173,326,'どこを支え、どこへ力を加えるか',14,center=True)
d.text(173,352,'静的な変位を決める条件',15,R,center=True)
d.text(487,294,'初期条件：開始時刻の指定',16,center=True)
d.text(487,326,'最初の変位・速度はどうか',15,center=True)
d.text(487,352,'本問の静的解析では不要',15,R,center=True)
d.text(330,403,'支持で剛体運動を除き、静的な式 K U = F を解く',16,center=True)
d.save('1-7_static_boundary_after.svg')

d=SVG('線形な有限要素解の荷重比例')
d.text(330,31,'計算条件を固定し、荷重だけを4倍にする',19,center=True)
for yy,left,right,col in ((109,'荷重 F','節点値 U',N),(239,'荷重 4F','節点値 4U',R)):
    d.rect(31,yy-37,155,68,F,col);d.rect(252,yy-37,156,68,F,N);d.rect(474,yy-37,155,68,F,col)
    d.text(108,yy+6,left,19,col,center=True)
    d.text(330,yy+6,'同じ行列 K',18,center=True)
    d.text(551,yy+6,right,19,col,center=True)
    d.arrow(186,yy,251,yy);d.arrow(409,yy,473,yy)
d.arrow(108,145,108,195,R,2);d.text(158,178,'4倍',15,R,center=True)
d.arrow(551,145,551,195,R,2);d.text(601,178,'4倍',15,R,center=True)
d.text(330,316,'K(4U) = 4(KU) = 4F',21,R,center=True)
d.text(330,356,'同じ補間を使うので、近似解も v = 4u',18,center=True)
d.text(330,391,'境界の指定値0は、4倍しても0のまま',17,center=True)
d.save('1-9_linear_load_scaling_after.svg')

mapping=json.loads((OUT/'図マッピング.json').read_text(encoding='utf-8'))
ns='{http://www.w3.org/2000/svg}'
for number,(name,key,_hint) in mapping.items():
    svg=DEST/name;tree=ET.parse(svg);e=tree.getroot()
    assert e.attrib['viewBox']=='0 0 660 420' and e.attrib['width']=='660' and e.attrib['height']=='420'
    assert not any(tree.findall('.//'+ns+tag) for tag in ('text','image','use','foreignObject'))
    for node in tree.iter():
        assert not any('href' in k for k in node.attrib)
        for attr in ('fill','stroke'):
            if attr in node.attrib:assert node.attrib[attr] in (N,R,G,F,W,'none','white')
        for attr in ('opacity','fill-opacity'):
            if attr in node.attrib:assert node.attrib[attr]=='1'
    doc=fitz.open(svg);pdf=fitz.open('pdf',doc.convert_to_pdf());scale=1320/pdf[0].rect.width
    target=ROOT/'assets/figures'/f'{key}.png'
    pdf[0].get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).save(target)
    compressed=compress_bytes(target)
    if compressed:target.write_bytes(compressed)
    shutil.copy2(target,OUT/(name.removesuffix('.svg')+'.png'))
placement='''# 第1章 図の配置指示

全12点とも回答後専用（figure=helpful）。回答前には表示しない。
色：主線 #1F3A65、強調・結果 #C82D2D、補助線・寸法 #888888、面塗り #E1E7F2（不透明）、背景白。
各SVGはviewBox="0 0 660 420"、width=660、height=420。文字はパス化。外部参照・外部フォント・ラスター画像なし。
PNGはSVG全体を2倍倍率でレンダした1320×840。SVGの表示寸法自体は2倍にしない。
1-2・1-7・1-9には初学者の理解を助ける図を追加した。1-6の図は重み関数の具体形に依存せず、修正後の多項式の重みでも有効。
PDFでは問題・選択肢・正解・図の次ページに4節解説をまとめる。アプリでは既存の回答後図欄で表示。

| 問題 | SVG | アプリ図キー | 内容 |
|---|---|---|---|
'''
for number,(name,key,hint) in mapping.items():placement+=f'| {number} | {name} | {key} | {hint} |\n'
(DEST/'図の配置指示.md').write_text(placement,encoding='utf-8')
(OUT/'図の配置指示.md').write_text(placement,encoding='utf-8')
with zipfile.ZipFile(OUT/'固体2級_第1章_回答後図_完成版.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,key,hint in mapping.values():z.write(DEST/name,name)
    z.write(OUT/'図の配置指示.md','図の配置指示.md')
print('12 SVG contracts validated; 12 after-only PNGs rendered and compressed; complete diagram zip saved.')
