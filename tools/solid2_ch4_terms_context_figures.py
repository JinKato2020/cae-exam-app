# -*- coding: utf-8 -*-
from pathlib import Path
import json,xml.etree.ElementTree as ET,zipfile
import fitz
from review_svg import SVG,N,R,G,F,W,graph,samples
from compress_figures import compress_bytes
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'図/固体2級/第04章';OUT=ROOT/'output/固体2級_第4章_反映結果'
mapping={
'discretization-workflow':('solid2Ch4TermMethodsOverview','4-term_discretization_methods.svg'),
'weighted-residual':('solid2Ch4TermWeightedResidual','4-term_weighted_residual.svg'),
'rayleigh-ritz':('solid2Ch4TermRayleighRitz','4-term_rayleigh_ritz.svg'),
'finite-difference':('solid2Ch4TermFiniteDifference','4-term_finite_difference.svg'),
'shape-function':('solid2Ch4TermShapeRoles','4-term_shape_function_roles.svg')}
def figure(title,size=19):d=SVG(title);d.title(title,size);return d
def save(d,ident):d.save(DEST/mapping[ident][1])
d=figure('連続な問題から、方程式を作って解く')
d.rect(30,57,600,47,F,N);d.text(330,87,'物理の法則・材料・境界条件 ＋ 近似する未知の分布',17,center=True)
for xx in (123,330,537):d.arrow(xx,106,xx,126,G,1.5)
for xx in (25,235,445):d.rect(xx,135,190,129,F,N)
d.text(120,160,'重み付き残差法',18,center=True);d.text(120,184,'式のずれを積分で評価',14,center=True)
d.rect(35,198,170,55,W,R,1.5);d.text(120,220,'ガラーキン法',17,R,center=True);d.text(120,243,'重み＝近似の基底関数',13,center=True)
d.text(330,160,'レイリー・リッツ法',16,center=True);d.text(330,202,'エネルギーの',18,center=True);d.text(330,231,'停留条件を使う',18,center=True)
d.text(540,160,'差分法',19,center=True);d.text(540,202,'微分を、格子点の',16,center=True);d.text(540,231,'値の差で近似する',16,center=True)
for xx in (123,330,537):d.arrow(xx,269,xx,294,G,1.5)
d.rect(40,300,580,39,W,R,1.5);d.text(330,326,'作る：有限個の未知数の連立方程式',20,R,center=True)
d.arrow(330,342,330,357,G,1.5)
d.text(330,380,'解く：未知の値を求める（ガウス・ザイデル法など）',17,center=True)
d.text(330,411,'線形弾性のFEMは、左・中央の原理を要素と形状関数で適用',13,G,center=True)
save(d,'discretization-workflow')

d=figure('ガラーキン法：近似と重みに同じ基底を使う',18)
for xx,title,formula,caption in ((35,'未知の分布を近似する','u = N d','大きさdは、まだ未知'),(367,'同じNでずれを評価する','w = N','これを重みとして使う')):
 d.rect(xx,78,257,225,F,N,1);d.text(xx+128,109,title,17,center=True);d.text(xx+128,144,formula,23,R,center=True)
 graph(d,xx+43,178,173,67,[(0,0),(.5,1),(1,0)],N,xlabel='x',ylabel='N')
 d.text(xx+128,286,caption,15,center=True)
d.arrow(300,198,354,198,R,3)
d.text(330,345,'残差×重みを積分して0 → 未知係数dの方程式',18,center=True)
d.text(330,385,'FEMでは、要素内の形を表す形状関数Nを使う',17,center=True)
d.text(330,412,'積分が0でも、各点の残差が0とは限らない',13,G,center=True);save(d,'weighted-residual')

d=figure('レイリー・リッツ法：エネルギーから未知量を決める',17)
d.text(177,82,'指定変位を守る候補を選ぶ',17,center=True)
graph(d,63,130,231,123,[(0,0),(.5,.28),(1,0)],G,xlabel='x',ylabel='u')
for height,col in ((.60,N),(.93,G)):d.path([(63,253),(178.5,253-height*123),(294,253)],col,2)
d.text(177,299,'両端は0、中央の高さdが未知',15,center=True)
d.arrow(310,195,344,195,R,2.5)
d.text(491,82,'Π(d)の最小を探す',18,center=True)
graph(d,386,130,211,123,samples(lambda t:4*(t-.5)**2),N,xlabel='d',ylabel='Π')
d.dot(491.5,253,R,5);d.text(492,299,'傾き0、安定なら最小',16,R,center=True)
d.text(330,352,'① 変位の候補を入れる → ② Πをdの式にする',18,center=True)
d.text(330,391,'③ dで微分して0 → 方程式を作る',19,R,center=True)
d.text(330,412,'図の曲線と尺度は模式表示。計算例は本文を参照。',12,G,center=True);save(d,'rayleigh-ritz')

d=figure('差分法：値の差 → 傾きの差 → 二回の微分',18)
pts=[(105,218),(330,116),(555,218)];d.path(pts,N,3)
for (xx,yy),label in zip(pts,('左の値','中央の値','右の値')):d.dot(xx,yy,N,5);d.text(xx,yy-20,label,17,center=True)
d.text(185,169,'左の傾き',17,R,center=True);d.text(481,169,'右の傾き',17,R,center=True)
d.path([(105,270),(555,270)],G,1.5)
for xx in (105,330,555):d.path([(xx,260),(xx,280)],G,1.5)
d.text(217,300,'間隔h',17,G,center=True);d.text(442,300,'間隔h',17,G,center=True)
d.text(330,339,'（右の傾き − 左の傾き）をhで割る',19,R,center=True)
d.text(330,381,'≈（左の値 − 2×中央の値 ＋ 右の値）/ h²',18,center=True)
d.text(330,411,'この近似を微分方程式へ入れ、点の値の方程式にする',13,G,center=True);save(d,'finite-difference')

d=figure('形状関数N：六つの使いどころ',21)
roles=[('① 未知の分布を表す','u = ΣNi di','節点値はまだ未知'),('② ひずみを計算する','Nを微分 → B','ひずみ = B×節点変位'),('③ 重みとして使う','ガラーキン法：w = Ni','積分から方程式へ'),('④ 分布荷重を換算する','荷重×Nを積分','同じ仮想仕事の節点力'),('⑤ 結果を表示する','解いた節点値を入れる','要素内部の値も求まる'),('⑥ 座標・形状を表す','x = ΣNi xi','節点座標から内部座標')]
for i,(heading,formula,caption) in enumerate(roles):
 xx=25+i%3*211;yy=90+i//3*123
 d.rect(xx,yy,188,106,F,N,1)
 d.text(xx+94,yy+27,heading,15,center=True)
 d.text(xx+94,yy+61,formula,14,R,center=True)
 d.text(xx+94,yy+90,caption,13,center=True)
d.text(330,69,'共通の働き：節点の値で、内部の分布を表す',17,center=True)
d.text(330,358,'式を作る段階でも、方程式を解いた後でも使う',18,center=True)
d.text(330,397,'N：内挿 ／ B：微分 ／ D：材料の関係',19,center=True)
d.text(330,413,'Nの形は、要素の種類・節点数・次数で変わる',12,G,center=True);save(d,'shape-function')

ns='{http://www.w3.org/2000/svg}'
for ident,(key,name) in mapping.items():
 p=DEST/name;tree=ET.parse(p);assert tree.getroot().attrib['viewBox']=='0 0 660 420'
 assert not any(tree.findall('.//'+ns+t) for t in ('text','image','use','foreignObject'))
 for e in tree.iter():
  assert not any('href' in k for k in e.attrib)
  for k in ('fill','stroke'):
   if k in e.attrib:assert e.attrib[k] in (N,R,G,F,W,'none')
 doc=fitz.open(p);pdf=fitz.open('pdf',doc.convert_to_pdf());scale=1320/pdf[0].rect.width
 target=ROOT/'assets/figures'/f'{key}.png';pdf[0].get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).save(target)
 comp=compress_bytes(target)
 if comp:target.write_bytes(comp)
 (OUT/name.replace('.svg','.png')).write_bytes(target.read_bytes())
placement='# 第4章 公式・用語の追加図\n\n共通：660×420 SVG、文字はメイリオをパス化、PNG1320×840、外部参照・フォント・ラスター画像なし。主線 #1F3A65、結果・注目箇所 #C82D2D、補助 #888888、面塗り #E1E7F2（不透明）、背景白。\n\n'
for ident,(key,name) in mapping.items():placement+=f'- {ident}：{name} → {key}\n'
placement+='\n図は原理の比較・近似の選び方を示す模式図。重み付き残差法の一種がガラーキン法。レイリー・リッツ法と差分法をその下位に入れない。FEMは要素・形状関数に基づき、線形弾性では前二者の原理から導ける。ガウス・ザイデル法は離散化後に方程式を解く手法。形状関数の六用途は順に実行する六工程を意味しない。\n'
(OUT/'用語図の配置指示.md').write_text(placement,encoding='utf-8');(DEST/'用語図の配置指示.md').write_text(placement,encoding='utf-8')
with zipfile.ZipFile(OUT/'固体2級_第4章_用語図.zip','w',zipfile.ZIP_DEFLATED) as z:
 for _,name in mapping.values():z.write(DEST/name,name)
 z.write(OUT/'用語図の配置指示.md','図の配置指示.md')
(OUT/'用語図マッピング.json').write_text(json.dumps({i:{'key':k,'svg':n} for i,(k,n) in mapping.items()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('5 glossary SVG/PNG diagrams rendered and verified.')
