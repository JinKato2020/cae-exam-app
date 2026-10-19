# -*- coding: utf-8 -*-
from pathlib import Path
import json,math,zipfile,xml.etree.ElementTree as ET
import fitz
from review_svg import SVG,N,R,G,F,W,graph,samples
from compress_figures import compress_bytes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/固体2級_第3章_反映結果';DEST=ROOT/'図/固体2級/第03章'
DEST.mkdir(parents=True,exist_ok=True)
mapping=json.loads((OUT/'図マッピング.json').read_text(encoding='utf-8'))
models={}
def save(d,n,mode='after'):
    name=mapping[f'3-{n}'][mode+'_svg'];assert name;d.save(DEST/name)
def after(n,title):d=SVG(title);d.title(title);return d

d=after(1,'フーリエ則：温度勾配2倍 → 熱流束も2倍')
d.text(330,69,'同じ材料・同じ距離で比べる',18,center=True)
for x,label,pts,width in ((65,'① 温度勾配が小さい',[(0,.12),(1,.46)],3),(370,'② 温度勾配が2倍',[(0,.12),(1,.8)],6)):
    d.text(x+110,112,label,17,center=True)
    graph(d,x,145,205,120,pts,N,xlabel='位置',ylabel='温度')
    # Equal line/head sizes; arrow length encodes heat-flux magnitude.
    d.arrow(x+185,315,x+185-(80 if width==3 else 160),315,R,3)
    d.text(x+110,350,'熱流束は小さい' if width==3 else '熱流束の大きさも2倍',17,R,center=True)
d.text(330,384,'赤い矢印：向き＝熱の流れる向き、長さ＝大きさ',16,center=True)
d.text(330,411,'熱は高温側から低温側へ流れる',16,center=True);save(d,1)

d=after(2,'物理量の対応：式の中での役割をそろえる')
for x,label in ((115,'役割'),(330,'構造の棒'),(545,'熱伝導')):d.text(x,80,label,17,center=True)
rows=[('未知量','変位 u','温度 T'),('位置で微分','軸ひずみ ε','温度勾配'),('構成則の結果','軸応力 σ','熱流束 q'),('入力源','外力','熱の供給源')]
for i,row in enumerate(rows):
    yy=107+62*i;d.rect(27,yy,606,46)
    for x,label in zip((115,330,545),row):d.text(x,yy+29,label,17,R if x==545 else N,center=True)
d.text(330,390,'比べるのは「式の中での役割」',18,center=True);save(d,2)

d=after(3,'定常解析：温度が落ち着いた状態を求める')
for xx,heading,lines,col in ((30,'境界温度を変更',('まだ落ち着いて','いない'),N),(245,'変化の途中',('内部の温度が','変わっている'),N),(460,'定常状態',('各場所の温度が','時間で変わらない'),R)):
    d.rect(xx,121,170,142,F,col);d.text(xx+85,157,heading,17,col,center=True)
    for yy,label in zip((203,234),lines):d.text(xx+85,yy,label,15,col,center=True)
for xx in (204,419):d.arrow(xx,191,xx+34,191,G,2)
d.text(330,84,'同じ境界温度を保ち続ける',18,center=True)
d.text(330,319,'定常解析で求めるのは、右の最終状態',19,R,center=True)
d.text(330,373,'定常でも、場所による温度差や熱の流れは残る',16,center=True);save(d,3)

d=after(4,'平板は直線、円筒は外へ行くほど緩やか')
d.text(176,78,'平板：面積一定',17,center=True);d.text(483,78,'円筒：面積はrに比例',17,center=True)
graph(d,55,112,237,158,[(0,1),(1,0)],R,endlabels=('高温面','低温面'))
logfun=lambda t:1-math.log(1+2*t)/math.log(3)
graph(d,363,112,237,158,samples(logfun),R,xlabel='r',endlabels=('r₁','r₂'))
d.text(177,333,'熱流束一定 → 傾き一定',16,center=True);d.text(482,333,'熱流束は1/r → 外ほど緩い',16,center=True)
d.text(330,387,'発熱なし・定常：熱流量 Q は両方とも保存',17,center=True);models['3-4-cylinder']=samples(logfun);save(d,4)

# 3-5 candidate set preserves I=equal slope, II=inverse, III=correct, IV=jump.
c5={'I':[(0,1),(1,0)],'II':[(0,1),(2/3,1/7),(1,0)],'III':[(0,1),(2/3,.6),(1,0)],'IV':[(0,1),(2/3,.66),(2/3,.51),(1,0)]}
d=SVG('二層壁の候補温度線');d.title('候補温度線：同じ端面温度、Aの厚さ2d・Bはd',17)
for i,(name,pts) in enumerate(c5.items()):
    x=50+(i%2)*326;y=94+(i//2)*180
    d.text(x+114,y-28,name,20,center=True);graph(d,x,y,230,108,pts,N)
    d.path([(x+230*2/3,y-3),(x+230*2/3,y+108)],G,1,'4 4')
    d.text(x+75,y+133,'層A',13,center=True);d.text(x+192,y+133,'層B',13,center=True)
save(d,5,'before');models['3-5-candidates']=c5
d=after(5,'二層壁の全候補：赤のIIIが条件に合う')
for i,(name,pts) in enumerate(c5.items()):
    x=50+(i%2)*326;y=95+(i//2)*165;col=R if name=='III' else N
    d.text(x+114,y-28,name,20,col,center=True);graph(d,x,y,230,88,pts,col)
    d.path([(x+230*2/3,y-3),(x+230*2/3,y+88)],G,1,'4 4')
    d.text(x+75,y+115,'A：2d、3λ',12,center=True);d.text(x+192,y+115,'B：d、λ',12,center=True)
d.text(330,405,'III：温度連続、勾配B/A = 3、温度降下A:B = 2:3',16,R,center=True);save(d,5)

# User-approved additional colors are confined to 3-6.
BLUE,ORANGE='#1877B8','#D87513'
def insulation(d,x,y,w,h):
    d.rect(x,y,w,h,'#EEEEEE',G,1)
    if w>h:
        for xx in range(int(x)+5,int(x+w)-7,12):d.path([(xx,y+h-2),(xx+7,y+2)],G,1)
    else:
        for yy in range(int(y)+5,int(y+h)-7,12):d.path([(x+2,yy+7),(x+w-2,yy)],G,1)
d=SVG('3-6 問題図：境界条件の場所');d.title('問題図：どの面に、どんな条件を与える？',19)
d.text(330,66,'H：ここから熱が入る',18,R,center=True)
d.rect(140,122,350,180,F,N)
insulation(d,122,122,18,180);insulation(d,140,302,350,18)
insulation(d,140,104,90,18);insulation(d,400,104,90,18)
d.path([(230,122),(400,122)],R,4)
for xx in (265,315,365):d.arrow(xx,81,xx,151,R,3)
d.path([(490,122),(490,302)],ORANGE,6)
d.text(72,199,'D：断熱',15,center=True);d.text(72,227,'出入りなし',13,center=True)
d.text(572,188,'F：温度一定',15,ORANGE,center=True)
d.text(572,216,'この面全体を',13,center=True);d.text(572,240,'同じ温度に保つ',13,center=True)
d.text(315,221,'熱が伝わる材料',18,center=True)
d.text(315,348,'D：上辺のH以外・左辺・下辺は断熱',16,center=True)
d.arrow(47,381,92,381,R,3);d.text(102,386,'熱の流れ',14)
insulation(d,265,372,40,18);d.text(316,386,'断熱材の模式表示',14)
d.text(330,412,'問題図には、与えられた条件だけを表示',12,G,center=True);save(d,6,'before')
d=after(6,'解説図：境界ごとに、線と矢印の意味を読む')
d.path([(32,57),(74,57)],BLUE,3);d.text(83,62,'等温線＝同じ温度の場所',14,BLUE)
d.arrow(373,57,410,57,R,3);d.text(422,62,'熱の流れ',14,R)
for x in (20,235,450):d.rect(x,78,190,212,W,G,1)
d.text(115,103,'F：温度一定',17,ORANGE,center=True)
d.rect(40,123,145,100,F)
for xx in (78,108,138):d.path([(xx,123),(xx,223)],BLUE,2)
d.path([(185,123),(185,223)],ORANGE,6)
d.arrow(81,180,169,180,R,3)
d.text(115,246,'境界上はどこでも',14,center=True)
d.text(115,267,'同じ温度＝等温線',14,BLUE,center=True)
d.text(330,103,'D：断熱',17,center=True)
d.rect(270,123,138,100,F);insulation(d,254,123,16,100)
for yy in (143,183,215):d.path([(270,yy),(407,yy)],BLUE,2)
d.path([(270,183),(282,183),(282,195),(270,195)],G,1.5)
d.arrow(346,208,346,137,R,3)
d.text(330,246,'等温線は境界に直角',14,BLUE,center=True)
d.text(330,267,'熱は境界に沿って流れる',13,R,center=True)
d.text(545,103,'H：熱の流入',17,R,center=True)
d.rect(470,175,150,48,F);d.path([(470,175),(620,175)],N,3)
d.arrow(507,175,507,122,G,2);d.text(484,143,'n',15,G)
d.text(494,118,'外向き',12,G,center=True)
d.arrow(574,131,574,212,R,3);d.text(601,148,'流入',12,R,center=True)
d.text(545,246,'外向きを正にすると',14,center=True)
d.text(545,267,'流入する熱流束は負',14,R,center=True)
d.text(330,315,'断熱：境界を横切る熱は0。沿う熱は流れてよい。',16,center=True)
d.text(330,349,'H：q・n = −λ ∂T/∂n = −qin',20,R,center=True)
d.text(330,376,'qin > 0 は内向きの流入量、n は外向き単位法線',14,center=True)
d.text(330,408,'境界付近の向きの模式図。角と温度勾配0の場所は除く。',12,G,center=True);save(d,6)

def generation_setup(title):
    d=SVG(title);d.title(title);d.rect(102,130,457,141,F,N)
    for xx in (170,270,370,470):d.text(xx,203,'H > 0',17,R,center=True)
    d.text(65,203,'T₀',20,center=True);d.text(603,203,'T₀',20,center=True)
    d.arrow(115,322,554,322,G,1.3);d.text(334,351,'厚さ方向 x（0からL）',16,center=True)
    d.text(330,389,'両端面は同じ温度、側面は断熱',17,center=True);return d
save(generation_setup('一様な内部発熱と、両端面の温度指定'),7,'before')
d=after(7,'内部で発熱 → 温度は山形の二次関数')
gen=lambda t:4*t*(1-t);graph(d,87,100,487,170,samples(gen),R,endlabels=('x=0、T₀','x=L、T₀'))
d.path([(330.5,100),(330.5,270)],G,1,'4 4');d.text(330,86,'中央が最も高温',18,R,center=True)
d.arrow(285,318,148,318,R,2);d.arrow(377,318,514,318,R,2)
d.text(330,353,'熱は中央から左右の表面へ逃げる',18,center=True)
d.text(330,393,'両面が同じ温度でも、発熱する内部は高温',16,center=True);models['3-7-normalized']=samples(gen);save(d,7)

c8={'A':lambda t:1-t,'B':lambda t:.6+1.2*t-1.8*t*t,'C':lambda t:1-.5*t-.5*t*t,'D':lambda t:(1-t)**2}
d=SVG('左流入と一様発熱を持つ壁の候補温度曲線');d.title('候補温度曲線：どれも右面温度を満たす',18)
for i,(name,fun) in enumerate(c8.items()):
    x=50+(i%2)*326;y=94+(i//2)*180
    d.text(x+114,y-28,name,20,center=True);graph(d,x,y,230,108,samples(fun),N,endlabels=('左面','右面'))
save(d,8,'before');models['3-8-candidates']={k:samples(v) for k,v in c8.items()}
d=after(8,'流入＋発熱の全候補：赤のCが条件に合う')
for i,(name,fun) in enumerate(c8.items()):
    x=50+(i%2)*326;y=95+(i//2)*165;col=R if name=='C' else N
    d.text(x+114,y-28,name,20,col,center=True);graph(d,x,y,230,88,samples(fun),col,endlabels=('左面','右面'))
d.text(330,405,'C：右へ下がる ＋ 発熱で右ほど熱が増え、急になる',16,R,center=True);save(d,8)

d=after(9,'円筒の熱損失：管長当たりから面積当たりへ')
d.circle(168,203,113,F,N);d.circle(168,203,75,W,N)
d.arrow(168,203,281,203,G,1.3);d.arrow(168,203,168,128,G,1.3)
d.text(183,239,'b = 0.12 m',14,center=True);d.text(175,111,'a = 0.08 m',14,center=True)
d.text(477,97,'管長1mで考える',18,center=True)
d.text(477,141,'外面流束：74.0 W/m²',19,R,center=True)
d.text(477,188,'外面積：0.754 m²',18,center=True)
d.text(477,233,'流束 × 外面積',17,center=True)
d.text(477,280,'= 55.8 W',20,R,center=True)
d.text(330,353,'内面110℃、外面20℃、λ = 0.04 W/(mK)',16,center=True)
d.text(330,393,'保存されるのは熱流量Q。外ほど流束は小さい。',17,center=True);save(d,9)

d=after(10,'熱通過率K：流体から壁を通って流体へ')
labels=[('高温側の熱伝達','温度差 q/hh'),('壁内の熱伝導','温度差 qt/λ'),('低温側の熱伝達','温度差 q/hc')]
for i,(label,formula) in enumerate(labels):
    xx=39+211*i;d.rect(xx,124,160,98,F,N);d.text(xx+80,151,label,16,center=True);d.text(xx+80,188,formula,17,center=True)
    if i<2:d.arrow(xx+160,173,xx+206,173,R,2)
d.text(330,85,'q = K(Th − Tc)：同じ熱流束qが順に通る',17,center=True)
d.text(330,275,'Th − Tc = q(1/hh + t/λ + 1/hc)',19,center=True)
d.text(330,326,'K = 1 / (1/hh + t/λ + 1/hc)',22,R,center=True)
d.text(330,379,'三つの温度差を足し、qについて整理する',17,center=True)
d.text(330,410,'Kの単位：W/(m²K)',14,G,center=True);save(d,10)

d=after(11,'熱通過率K：分母が小さいほど、Kは大きい')
rows=[('初期',[.20,.04,.01],.25),('案A',[.16,.04,.01],.21),('案B',[.20,.03,.01],.24),('案C',[.20,.04,.008],.248)]
d.text(330,70,'1/K = 1/hh + t/λ + 1/hc',18,center=True)
for xx,label in ((61,'案'),(235,'変える項の計算'),(448,'変更後1/K'),(579,'K')):d.text(xx,109,label,16,center=True)
for i,(label,values,total) in enumerate(rows[1:]):
    yy=129+i*59;col=R if i==0 else N;d.rect(30,yy,600,46,F,col,1)
    entries=[('A','1/hh：0.20 / 1.25','0.210','4.76'),('B','t/λ：0.04 × 0.75','0.240','4.17'),('C','1/hc：0.01 / 1.25','0.248','4.03')][i]
    for xx,value in zip((61,235,448,579),entries):d.text(xx,yy+30,value,16,col,center=True)
d.text(330,337,'案A：1/Kが最小 → Kが最大',19,R,center=True)
d.text(330,375,'hが25%増 → 1/hは1/1.25 = 0.8倍',17,center=True)
d.text(330,410,'単位：1/Kはm²K/W、KはW/(m²K)',14,G,center=True);models['3-11-bars']=rows;save(d,11)

d=after(12,'二層壁：熱通過率K → 熱流束 → 外表面温度')
vals=[160,144.444444444,113.333333333,82.222222222,20];xs=[0,.17,.40,.80,1]
d.text(330,72,'内側流体160℃ → 壁 → 外側流体20℃',18,center=True)
for i,(label,calc,value) in enumerate((('内側対流','1/20','0.05'),('層A','0.04/0.4','0.10'),('層B','0.08/0.8','0.10'),('外側対流','1/5','0.20'))):
    xx=23+158*i;d.rect(xx,102,139,100,F,N,1)
    d.text(xx+69.5,128,label,16,center=True);d.text(xx+69.5,160,calc,16,center=True);d.text(xx+69.5,190,value,18,center=True)
d.text(330,237,'① 1/K = 0.05 + 0.10 + 0.10 + 0.20 = 0.45',17,center=True)
d.text(330,278,'② q = K(160 − 20) ≈ 311.1 W/m²',19,R,center=True)
d.text(330,325,'③ Ts = 20 + q/h₂ ≈ 82.2℃',19,R,center=True)
d.text(330,366,'外気温 ＋ 外側対流に必要な温度差',17,center=True)
d.text(330,411,'1/Kの単位：m²K/W。枠は計算の区間を示す。',13,G,center=True);models['3-12-profile']={'temperatures':vals,'positions':xs};save(d,12)

d=after(13,'λは物体内部、hは表面と流体の間')
d.rect(45,108,570,143,W,N,1);d.rect(65,143,260,88,F,N)
d.text(195,134,'物体内部：熱伝導率 λ',17,center=True)
d.text(463,134,'表面と流体：熱伝達率 h',17,center=True)
d.text(463,221,'空気・水などの流体',15,center=True)
d.arrow(100,183,283,183,R,3);d.arrow(325,183,542,183,R,3)
d.text(330,302,'金属：自由電子が電気も熱も運ぶ',20,R,center=True)
d.text(330,347,'電気を通しやすい金属は、熱も通しやすい傾向',16,center=True)
d.text(330,396,'断熱材：熱伝導率が小さく、熱を通しにくい',17,center=True);save(d,13)

c14={'I':[(0,1),(.25,.55),(.75,.1),(1,0)],'II':[(0,1),(.25,.8),(.75,.2),(1,0)],'III':[(0,1),(.25,1),(.75,0),(1,0)],'IV':[(0,1),(.25,.9),(.75,.4),(1,0)]}
d=SVG('両側対流と平板伝導の候補温度線');d.title('候補I〜IV：流体区間の横幅は模式図',18)
for i,(name,pts) in enumerate(c14.items()):
    x=50+(i%2)*326;y=94+(i//2)*180
    d.text(x+114,y-28,name,20,center=True);graph(d,x,y,230,108,pts,N)
    for loc in (.25,.75):d.path([(x+230*loc,y-3),(x+230*loc,y+108)],G,1,'4 4')
    for pos,label in ((.125,'流体1'),(.5,'壁'),(.875,'流体2')):d.text(x+230*pos,y+135,label,12,center=True)
save(d,14,'before');models['3-14-candidates']=c14
d=after(14,'平板と両側対流の全候補：赤のIVが条件に合う')
for i,(name,pts) in enumerate(c14.items()):
    x=50+(i%2)*326;y=95+(i//2)*165;col=R if name=='IV' else N
    d.text(x+114,y-28,name,20,col,center=True);graph(d,x,y,230,88,pts,col)
    for loc in (.25,.75):d.path([(x+230*loc,y-3),(x+230*loc,y+88)],G,1,'4 4')
    for pos,label in ((.125,'流体1'),(.5,'壁'),(.875,'流体2')):d.text(x+230*pos,y+114,label,12,center=True)
d.text(330,405,'IV：右側の温度差は左側の4倍。壁内は直線。',17,R,center=True);save(d,14)

d=after(15,'円筒の対流温度差は、hと面積の両方で決まる')
d.text(167,74,'b = 1.5a',17,center=True)
radial=lambda t:1-math.log(1+.5*t)/math.log(1.5)
graph(d,60,119,215,144,samples(radial),R,xlabel='r',endlabels=('a：内面','b：外面'))
d.text(474,105,'h₂ = h₁ / 6',19,center=True)
d.text(474,151,'A₂ = 1.5 A₁',19,center=True)
d.text(474,218,'ΔT₂ / ΔT₁',21,R,center=True)
d.text(474,258,'= 6 / 1.5 = 4',23,R,center=True)
d.text(330,327,'同じ熱を、外側では1.5倍の面積へ分ける',17,center=True)
d.text(330,369,'壁内の温度は対数型：外ほど下降が緩い',18,center=True)
d.text(330,408,'面積比を忘れると、誤って温度差を6倍にする',16,R,center=True);models['3-15-cylinder']=samples(radial);save(d,15)

d=after(16,'対称面では法線流束0、接線流束は残り得る')
d.rect(57,106,233,184,F,N);d.path([(57,198),(290,198)],G,1.5,'5 4')
d.arrow(86,164,259,164,N,2);d.arrow(86,232,259,232,N,2)
d.text(174,90,'元の全体モデル',16,center=True);d.text(174,329,'y = 0 が対称面',16,center=True)
d.arrow(308,155,350,155,G,1.3)
d.rect(373,106,233,92,F,N);d.path([(373,198),(606,198)],R,3)
d.text(489,90,'上半分だけ',16,center=True);d.text(489,230,'切断面：qy = 0',18,R,center=True)
d.arrow(402,172,565,172,N,2);d.text(489,270,'面に沿うqxは残り得る',15,center=True)
d.text(330,372,'対称面を横切る熱は0。面に沿う熱は流れてよい。',17,R,center=True)
d.text(330,407,'温度の値そのものを0に固定しない',17,center=True);save(d,16)

def pipe(mode):
    d=SVG('管壁のr-z断面と境界の指定');d.title('長い直管の一様な部分をr-z断面で考える',18)
    d.rect(113,134,431,134,F,N)
    d.arrow(77,299,77,93,G,1.2);d.text(65,80,'r',17,G)
    d.arrow(113,330,563,330,G,1.2);d.text(573,337,'z',17,G)
    d.text(330,105,'大気・外面',18,center=True);d.text(330,305,'高温流体・内面',18,center=True)
    d.text(235 if mode=='after' else 330,201,'管の材料',18,center=True)
    if mode=='after':
        d.path([(113,134),(544,134)],R,3);d.path([(113,268),(544,268)],R,3)
        d.text(330,77,'外面：外気温と外側hで熱伝達',16,R,center=True)
        d.text(330,378,'内面：高温流体の温度と内側hで熱伝達',16,R,center=True)
        d.text(90,228,'断熱',15,R,center=True);d.text(587,228,'断熱',15,R,center=True)
        d.arrow(403,257,403,145,R,3)
        d.text(330,407,'切断面：長手方向の温度変化がないため、熱流束0',15,center=True)
    else:
        d.text(84,223,'切断面',14,center=True);d.text(589,223,'切断面',14,center=True)
        d.text(330,390,'材料・寸法・流体条件は軸方向に一様',17,center=True)
    return d
save(pipe('before'),17,'before');save(pipe('after'),17)

# Related glossary illustration: area-normalized and total quantities.
d=SVG('熱通過率Kと熱抵抗R：面積当たりと全体');d.title('熱通過率Kと熱抵抗Rの関係',20)
d.text(330,70,'同じ経路・同じ温度差ΔTで比べる',18,center=True)
for xx,label,formula,units,coeff in ((25,'面積当たり','q = KΔT','q：W/m²','K：W/(m²K)'),(355,'面積A全体','Q = ΔT/R','Q：W','R：K/W')):
    d.rect(xx,104,280,155,F,N,1);d.text(xx+140,136,label,18,center=True)
    d.text(xx+140,176,formula,23,R,center=True)
    d.text(xx+140,211,units,16,center=True);d.text(xx+140,241,coeff,16,center=True)
d.text(330,298,'Q = Aq = AKΔT → R = 1/(KA)',22,R,center=True)
d.text(330,338,'1/K：面積当たりの抵抗（m²K/W）',17,center=True)
d.text(330,373,'同じ面積なら、Kが大きいほどRは小さい',17,center=True)
d.text(330,409,'面積1m²ならRと1/Kの数値は同じでも、単位は別',13,G,center=True)
term_svg=DEST/'3-term_heat_rate_resistance.svg';d.save(term_svg)

# Validate SVG contract and render only this chapter's dedicated keys.
ns='{http://www.w3.org/2000/svg}'
count=0
for number,info in mapping.items():
    for mode in ('after','before'):
        name,key=info[mode+'_svg'],info[mode+'_key']
        if not name:continue
        svg=DEST/name;tree=ET.parse(svg);e=tree.getroot()
        assert e.attrib['viewBox']=='0 0 660 420' and e.attrib['width']=='660' and e.attrib['height']=='420'
        assert not any(tree.findall('.//'+ns+tag) for tag in ('text','image','use','foreignObject'))
        for node in tree.iter():
            assert not any('href' in k for k in node.attrib)
            for attr in ('fill','stroke'):
                if attr in node.attrib:assert node.attrib[attr] in (N,R,G,F,W,'none')+((BLUE,ORANGE,'#EEEEEE') if number=='3-6' else ())
            for attr in ('opacity','fill-opacity'):
                if attr in node.attrib:assert node.attrib[attr]=='1'
        doc=fitz.open(svg);pdf=fitz.open('pdf',doc.convert_to_pdf());scale=1320/pdf[0].rect.width
        target=ROOT/'assets/figures'/f'{key}.png';pdf[0].get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).save(target)
        compressed=compress_bytes(target)
        if compressed:target.write_bytes(compressed)
        (OUT/name.replace('.svg','.png')).write_bytes(target.read_bytes());count+=1
tree=ET.parse(term_svg);assert tree.getroot().attrib['viewBox']=='0 0 660 420'
assert not any(tree.findall('.//'+ns+tag) for tag in ('text','image','use','foreignObject'))
doc=fitz.open(term_svg);pdf=fitz.open('pdf',doc.convert_to_pdf());target=ROOT/'assets/figures/solid2Ch3RateResistanceTerm.png'
pdf[0].get_pixmap(matrix=fitz.Matrix(1320/pdf[0].rect.width,1320/pdf[0].rect.width),alpha=False).save(target)
compressed=compress_bytes(target)
if compressed:target.write_bytes(compressed)
(OUT/'3-term_heat_rate_resistance.png').write_bytes(target.read_bytes())
(OUT/'図の数値モデル.json').write_text(json.dumps(models,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
placement='''# 第3章 図の配置指示

回答後17図と回答前6図を収録。回答前は候補線または与件だけを示し、正解番号・正しい候補の強調・導出した比や数値を入れない。回答後は解説の結論を表示する。
共通：viewBox="0 0 660 420"、width=660、height=420、白背景、メイリオの文字をパス化。外部参照・外部フォント・ラスター画像なし。PNGは全体を2倍で描いた1320×840。
色：主線 #1F3A65（物体・候補・通常注記）、強調 #C82D2D（熱流方向・正しい結果・回答後温度線）、補助 #888888（軸・寸法・界面）、面塗り #E1E7F2（不透明な材料や表の背景）。回答前の赤い矢印は問題で与えられた熱の流入・発熱の表示に限る。
3-3は境界変更から定常状態までの概念図で、所要時間を示さない。3-6は局所的な等温線と境界の向きを示す。3-12の枠は抵抗計算の区間、3-14の流体区間は模式表示で、実際の寸法を表さない。

'''
placement+='3-6のみ利用者の指定で追加色を使用：青 #1877B8 は等温線、オレンジ #D87513 は温度固定面、淡灰 #EEEEEE と斜線は断熱材。赤は熱流、灰の矢印は外向き法線。\n\n'
placement+='| 問題 | 回答後 | 回答前 |\n|---|---|---|\n'
for n,info in mapping.items():placement+=f'| {n} | {info["after_svg"]} | {info["before_svg"] or "なし"} |\n'
placement+='\n関連用語：3-term_heat_rate_resistance.svg。熱通過率Kと熱抵抗Rの面積換算を説明。Kの単位のKは温度単位ケルビン。\n'
(OUT/'図の配置指示.md').write_text(placement,encoding='utf-8');(DEST/'図の配置指示.md').write_text(placement,encoding='utf-8')
with zipfile.ZipFile(OUT/'固体2級_第3章_図_完成版.zip','w',zipfile.ZIP_DEFLATED) as z:
    for info in mapping.values():
        for mode in ('after','before'):
            if info[mode+'_svg']:z.write(DEST/info[mode+'_svg'],info[mode+'_svg'])
    z.write(OUT/'図の配置指示.md','図の配置指示.md')
    z.write(term_svg,term_svg.name)
print(f'{count} question SVGs and 1 glossary SVG rendered. Chapter 3 keys only.')
