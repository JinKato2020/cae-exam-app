# -*- coding: utf-8 -*-
from pathlib import Path
import math,json,zipfile,xml.etree.ElementTree as ET
import fitz
from review_svg import SVG,N,R,G,F,W,graph,samples
from compress_figures import compress_bytes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/固体2級_第4章_反映結果';DEST=ROOT/'図/固体2級/第04章'
DEST.mkdir(parents=True,exist_ok=True)
mapping=json.loads((OUT/'図マッピング.json').read_text(encoding='utf-8'))
def save(d,n,mode='after'):d.save(DEST/mapping[f'4-{n}'][mode+'_svg'])
def fig(title,size=19):d=SVG(title);d.title(title,size);return d
def poly(d,pts,col):d.p.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{col}"/>')
def wall(d,x,y,h=70):
 d.path([(x,y-h/2),(x,y+h/2)],N,3)
 for yy in range(int(y-h/2),int(y+h/2),10):d.path([(x-9,yy+8),(x,yy)],G,1)
def spring(d,x,y,X,Y,label=None):
 dx=X-x;dy=Y-y;L=math.hypot(dx,dy);ux=dx/L;uy=dy/L
 pts=[(x,y),(x+ux*14,y+uy*14)]
 for i in range(13):
  t=14+(L-28)*i/12;off=7*((-1)**i) if 0<i<12 else 0
  pts.append((x+ux*t-uy*off,y+uy*t+ux*off))
 pts.append((X,Y));d.path(pts,N,2)
 if label:d.text((x+X)/2,(y+Y)/2-19,label,15,center=True)
def matrix(d,x,y,rows,col=N,size=22):
 hh=43*len(rows);w=164
 d.path([(x+8,y),(x,y),(x,y+hh),(x+8,y+hh)],col,2)
 d.path([(x+w-8,y),(x+w,y),(x+w,y+hh),(x+w-8,y+hh)],col,2)
 for i,row in enumerate(rows):
  for j,v in enumerate(row):d.text(x+42+j*81,y+29+i*43,v,size,col,center=True)

# 4-1：実在しうる穴付き板の厚みと、穴を横切らない三角形メッシュ。
# 角度ごとの内周点と長方形外周点を結ぶ環状の要素で、穴と角を正確に残す。
d=fig('実物の形を、要素と節点に置き換える',20)
d.text(156,90,'穴のある板部品',19,center=True)
d.text(505,90,'同じ形状の有限要素モデル',18,center=True)
mesh_info={}
def plate(x,y,w,h,meshed,ident):
 dx,dy=14,-13;cx,cy=x+w/2,y+h/2;r=30
 for pts in ([(x,y),(x+dx,y+dy),(x+w+dx,y+dy),(x+w,y)],[(x+w,y),(x+w+dx,y+dy),(x+w+dx,y+h+dy),(x+w,y+h)]):
  poly(d,pts,F);d.path(pts+[pts[0]],N,1.5)
 d.rect(x,y,w,h,F,N,2)
 if meshed:
  angles=[2*math.pi*i/32 for i in range(32)]
  angles+=list({math.atan2(sy*h/2,sx*w/2)%(2*math.pi) for sx in (-1,1) for sy in (-1,1)})
  angles=sorted(set(angles));rings=[]
  for level in range(5):
   points=[]
   for theta in angles:
    co,si=math.cos(theta),math.sin(theta)
    limit=min(w/2/max(abs(co),1e-14),h/2/max(abs(si),1e-14))
    rr=r+(limit-r)*level/4;points.append((cx+rr*co,cy+rr*si))
   rings.append(points)
  n=len(angles);triangles=[]
  for level in range(4):
   for j in range(n):
    jj=(j+1)%n;a,b,c,e=rings[level][j],rings[level][jj],rings[level+1][jj],rings[level+1][j]
    triangles += [(a,b,c),(a,c,e)] if (level+j)%2==0 else [(a,b,e),(b,c,e)]
  signed_areas=[((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2 for a,b,c in triangles]
  assert all(v < -1e-7 for v in signed_areas),min(abs(v) for v in signed_areas)
  ring=rings[0]
  hole_polygon_area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]+ring[:1]))/2)
  assert math.isclose(sum(abs(v) for v in signed_areas),w*h-hole_polygon_area,rel_tol=1e-10)
  edges=set()
  for tri in triangles:
   for a,b in zip(tri,tri[1:]+tri[:1]):edges.add(tuple(sorted((a,b))))
  for a,b in edges:d.path([a,b],N,.65)
  for ring in rings:
   for xx,yy in ring:d.dot(xx,yy,N,1.15)
  selected=rings[2][5];d.dot(*selected,R,3.2)
  d.path([selected,(selected[0]+13,selected[1]+36),(548,319)],R,1.2)
  d.text(570,336,'節点',17,R,center=True)
  target=triangles[178];px=sum(p[0] for p in target)/3;py=sum(p[1] for p in target)/3
  poly(d,target,W);d.path(list(target)+[target[0]],R,1.7)
  d.path([(px,py),(394,315)],R,1.2);d.text(399,340,'三角形要素',16,R,center=True)
  mesh_info.update(nodes=len(rings)*n,elements=len(triangles),hole_radius=r,corners_preserved=True,zero_or_inverted_elements=0,minimum_element_area=min(abs(v) for v in signed_areas),total_element_area=sum(abs(v) for v in signed_areas),geometry_area=w*h-hole_polygon_area)
 # 二円の交差領域を直接パス化。レンダラー依存のclipPathは使わない。
 # 前面の穴の外へ奥の円を描くと、二つの穴に見えるので避ける。
 d.circle(cx,cy,r,F,N)
 lens=[]
 for ox,oy,otherx,othery in ((cx,cy,cx+dx,cy+dy),(cx+dx,cy+dy,cx,cy)):
  for j in range(512):
   theta=2*math.pi*j/512;px=ox+r*math.cos(theta);py=oy+r*math.sin(theta)
   if (px-otherx)**2+(py-othery)**2<=r*r+1e-7:lens.append((px,py))
 mx,my=cx+dx/2,cy+dy/2;lens.sort(key=lambda p:math.atan2(p[1]-my,p[0]-mx))
 poly(d,lens,W);d.path(lens+[lens[0]],G,1.4)
 d.p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{N}" stroke-width="1.5"/>')
 return cx,cy
plate(38,150,225,140,False,'part');plate(382,150,225,140,True,'model')
d.arrow(294,220,350,220,R,3)
d.text(322,256,'分割',17,R,center=True)
d.text(154,333,'厚みと貫通穴をもつ板',16,center=True)
d.text(330,383,'節点の変位から、部品全体の変形を近似する',18,center=True)
d.text(330,411,'図のメッシュは形状を説明する模式図です',13,G,center=True)
save(d,1)
(OUT/'4-1_メッシュ形状検証.json').write_text(json.dumps(mesh_info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

d=fig('重み付き残差法：各点のずれを、積分で調べる')
d.text(330,76,'R = 近似解を入れた左辺 − 右辺',20,center=True)
graph(d,85,122,480,118,[(0,.5),(.25,.8),(.5,.5),(.75,.2),(1,.5)],N,xlabel='位置',ylabel='R')
d.path([(85,181),(565,181)],G,1,'4 4');d.text(60,188,'0',14,G)
d.text(218,152,'正のずれ',15,center=True);d.text(459,221,'負のずれ',15,center=True)
d.text(330,302,'重み w を掛けた残差の積分を0にする',19,R,center=True)
d.text(330,342,'ガラーキン法：重みには形状関数 N を使う',18,center=True)
d.text(330,391,'積分が0でも、各点のずれが0とは限らない',17,center=True);save(d,3)

def bars(after=False):
 d=fig('段付き棒Iと一様棒II：同じ材料・同じ全長')
 wall(d,65,113,62);d.rect(65,91,175,44,F,N);d.rect(240,102,350,22,F,N)
 d.text(330,76,'棒I：左100mmは200mm²、右200mmは100mm²',16,center=True)
 wall(d,65,204,62);d.rect(65,182,525,44,F,N)
 d.text(330,169,'棒II：全長300mm、断面積200mm²',16,center=True)
 for yy in (113,204):d.arrow(590,yy,635,yy,N,2)
 if after:
  d.text(330,266,'棒Iの剛性80,000 ＜ 棒IIの133,333 N/mm',17,center=True)
  for yy,t in ((311,'同じ力：柔らかいIほど伸びる → UI > UII'),(352,'同じ伸び：硬いIIほど力が要る → UI < UII')):d.text(330,yy,t,18,R,center=True)
  d.text(330,403,'力一定：0.625 > 0.375 J ／ 伸び一定：0.576 < 0.960 J',15,center=True)
 else:
  d.text(330,286,'E = 200 GPa（共通）',19,center=True)
  d.text(330,334,'場合①：同じ引張力10kNを与える',18,center=True)
  d.text(330,383,'場合②：同じ端部伸び0.12mmを与える',18,center=True)
 return d
save(bars(),4,'before');save(bars(True),4)

d=fig('ひずみエネルギーと補ひずみエネルギー')
for xx,fn,label in ((55,lambda t:t,'線形：二つの面積は等しい'),(368,lambda t:t*t,'非線形：一般に面積は異なる')):
 x,y,w,h=xx,121,223,159
 poly(d,[(x,y+h),(x+w,y+h),(x+w,y),(x,y)],W)
 lower=[(x,y+h)]+[(x+w*t,y+h-h*v) for t,v in samples(fn)]+[(x+w,y+h)]
 upper=[(x,y+h),(x,y),(x+w,y)]+[(x+w*t,y+h-h*v) for t,v in reversed(samples(fn))]
 poly(d,upper,F);poly(d,lower,'#FFFFFF')
 graph(d,x,y,w,h,samples(fn),N,xlabel='ε',ylabel='σ')
 d.path([(x,y),(x+w,y),(x+w,y+h)],G,1,'3 3')
 d.text(x+60,y+52,'補エネルギー',13,center=True)
 d.text(x+168,y+135,'ひずみ',14,center=True);d.text(x+168,y+153,'エネルギー',14,center=True)
 d.text(x+w/2,343,label,15,R,center=True)
d.text(330,393,'両方を足すと、長方形の面積 σ×ε',18,center=True);save(d,6)

d=fig('変位法と応力法：未知量と原理を組にする')
for xx,title,lines in ((25,'変位法',('未知量：節点変位','仮に変える：変位','仮想仕事の原理')),(355,'応力法',('未知量：応力・力','仮に変える：応力・力','補仮想仕事の原理'))):
 d.rect(xx,110,280,228,F,N);d.text(xx+140,150,title,23,center=True)
 for yy,s in zip((207,252,307),lines):d.text(xx+140,yy,s,18,R if yy==307 else N,center=True)
d.text(330,389,'どちらも、釣合い・材料則・変形のつながりを使う',17,center=True);save(d,8)

def truss(after=False):
 d=fig('二本の棒と節点C：水平・鉛直の釣合い')
 C=(330,269);A=(104,138.5);B=(436,85.4)
 d.path([A,C,B],N,4)
 for pt,l in ((A,'A'),(B,'B'),(C,'C')):d.dot(*pt,N,5);d.text(pt[0]+13,pt[1]-12,l,18)
 for pt in (A,B):wall(d,pt[0],pt[1],28)
 d.path([(190,269),(478,269)],G,1,'4 4')
 d.text(265,259,'30°',18,center=True);d.text(365,252,'60°',18,center=True)
 d.arrow(330,269,330,344,R,3);d.text(407,327,'20kN（下向き）',16,center=True)
 if after:
  d.arrow(307,256,225,209,R,2);d.text(171,231,'CA：10kN',16,R,center=True)
  d.arrow(342,248,378,187,R,2);d.text(474,198,'CB：17.32kN',16,R,center=True)
  d.text(330,399,'任意の仮想変位 → 水平・鉛直の係数がともに0',17,center=True)
 else:d.text(330,399,'固定されたA・B ／ Cを仮にδx、δy動かす',17,center=True)
 return d
save(truss(),9,'before');save(truss(True),9)

d=fig('初期ひずみと初期応力：右辺へ移すと符号が変わる')
for yy,label,mid,right in ((105,'初期ひずみ ε₀','Dε₀：応力に換算','右辺：プラス'),(217,'初期応力 σ₀','既に応力の単位','右辺：マイナス')):
 d.rect(22,yy,184,63,F,N);d.text(114,yy+37,label,18,center=True)
 d.arrow(210,yy+31,235,yy+31,G,2)
 d.rect(239,yy,194,63,F,N);d.text(336,yy+37,mid,16,center=True)
 d.arrow(437,yy+31,462,yy+31,G,2)
 d.rect(466,yy,173,63,W,R);d.text(552,yy+37,right,17,R,center=True)
d.text(330,80,'Bの転置と積分で、応力を節点力へ換算',17,center=True)
d.text(330,329,'内力：Kd − 初期ひずみ項 ＋ 初期応力項 = 外力',16,center=True)
d.text(330,376,'移項：Kd = 外力 ＋ 初期ひずみ項 − 初期応力項',16,R,center=True)
d.text(330,410,'右辺の＋・−と、各節点の力の向きは分けて読む',13,G,center=True);save(d,13)

d=fig('CST：変位を一次式で補うと、ひずみは一定')
d.path([(68,239),(208,101),(284,239),(68,239)],N,3)
poly(d,[(68,239),(208,101),(284,239)],F)
for p in ((68,239),(208,101),(284,239)):d.dot(*p,N,5)
d.text(177,195,'三節点三角形',16,center=True)
d.arrow(298,190,354,190,R,3)
d.rect(367,111,263,163,F,N)
d.text(498,151,'変位：一次式',20,center=True)
d.text(498,198,'一回微分する',18,center=True)
d.text(498,248,'ひずみ：定数',21,R,center=True)
d.text(330,330,'u = a + bx + cy → ∂u/∂x = b',21,center=True)
d.text(330,382,'材料行列Dも一定・初期項なし → 応力も一定',17,center=True);save(d,18)

d=fig('B行列：各行をひずみの式から作る')
d.text(261,87,'ui の列',18,center=True);d.text(426,87,'vi の列',18,center=True)
rows=[('εx','Ni,x','0','uをxで微分'),('εy','0','Ni,y','vをyで微分'),('γxy','Ni,y','Ni,x','二つの勾配の和')]
for i,(l,a,b,c) in enumerate(rows):
 yy=112+i*77;d.rect(190,yy,324,61,F,N,1)
 d.text(132,yy+38,l,22,center=True);d.text(261,yy+38,a,23,R if i==2 else N,center=True);d.text(426,yy+38,b,23,R if i==2 else N,center=True)
 d.text(585,yy+38,c,12,center=True)
d.text(330,367,'Ni,x は、形状関数Niのx方向の微分',17,center=True)
d.text(330,406,'行：ひずみ成分 ／ 列：節点変位成分',17,center=True);save(d,20)

def series(after=False):
 d=fig('直列二本のばね：節点2には二本が接続')
 wall(d,60,138);spring(d,60,138,290,138,'100 N/mm');spring(d,290,138,555,138,'200 N/mm')
 for xx,l in ((60,'1：固定'),(290,'2'),(555,'3')):d.dot(xx,138,N);d.text(xx,173,l,16,center=True)
 for xx,l in ((290,'u₂, f₂'),(555,'u₃, f₃')):d.arrow(xx,208,xx+58,208,G,1.5);d.text(xx,240,l,17,center=True)
 if after:
  matrix(d,72,282,[['300','−200'],['−200','200']],R,20)
  d.text(428,305,'f₂ = 300u₂ − 200u₃',18,center=True)
  d.text(428,350,'f₃ = −200u₂ + 200u₃',18,center=True)
  d.text(330,402,'行列の単位：N/mm ／ 変位：mm ／ 力：N',15,center=True)
 else:
  d.text(330,306,'節点1の変位は0、右向きを正とする',18,center=True)
  d.text(330,374,'二本の要素の力を、各節点で足し合わせる',17,center=True)
 return d
save(series(),22,'before');save(series(True),22)

def inclined(after=False):
 d=fig('斜め二本と水平一本：全ばねの軸剛性は120N/mm',17)
 spring(d,72,104,220,252);spring(d,72,400,220,252);spring(d,220,252,485,252)
 wall(d,72,104,38);wall(d,72,400,27)
 d.path([(103,252),(292,252)],G,1,'4 4')
 d.text(167,222,'45°',17,center=True);d.text(167,283,'45°',17,center=True)
 for xx,l in ((220,'1'),(485,'2')):
  d.dot(xx,252,N,5);d.text(xx,283,l,17,center=True);d.arrow(xx,312,xx+65,312,G,2)
 d.text(353,216,'k',20,center=True)
 d.text(436,356,'両節点とも水平だけに動く',16,center=True)
 if after:
  d.text(427,79,'一本：k cos²45° = 60',18,R,center=True)
  d.text(427,119,'二本：水平剛性120',18,R,center=True)
  d.text(427,164,'K₁₁ = 120 + 120 = 240',17,R,center=True)
  d.text(418,403,'K₁₂ = K₂₁ = −120、K₂₂ = 120 N/mm',15,center=True)
 else:
  d.text(427,84,'軸方向だけに伸びるばね',16,center=True)
  d.text(427,124,'固定点の変位は0',17,center=True)
  d.text(436,403,'微小変形・左右の変位が未知',16,center=True)
 return d
save(inclined(),23,'before');save(inclined(True),23)

d=fig('剛性行列の性質：対角と非対角を区別')
matrix(d,60,130,[['K₁₁','K₁₂'],['K₂₁','K₂₂']],N,20)
d.text(434,147,'対称：K₁₂ = K₂₁',22,R,center=True)
d.text(434,204,'剛性をもつ対角成分は正',17,center=True)
d.text(330,290,'一次元ばねの別節点間：−k',20,center=True)
d.text(330,334,'斜め要素の同一節点x–y間：k cosθ sinθ',19,center=True)
d.text(330,389,'非対角成分が、いつでも負とは限らない',19,R,center=True);save(d,24)

def assembly(after=False):
 d=fig('共有節点：変位は一つ、力は足し合わせる')
 spring(d,72,136,330,136,'要素①');spring(d,330,136,588,136,'要素②')
 for xx,l in ((72,'1'),(330,'2：共有'),(588,'3')):d.dot(xx,136,N,5);d.text(xx,176,l,17,center=True)
 d.rect(34,229,276,96,F,N);d.rect(350,229,276,96,F,N)
 d.text(172,260,'要素①からの寄与',17,center=True);d.text(488,260,'要素②からの寄与',17,center=True)
 d.text(172,301,'u₂⁽¹⁾、f₂⁽¹⁾',22,center=True);d.text(488,301,'u₂⁽²⁾、f₂⁽²⁾',22,center=True)
 if after:
  d.text(330,367,'u₂ = u₂⁽¹⁾ = u₂⁽²⁾',22,R,center=True)
  d.text(330,408,'f₂ = f₂⁽¹⁾ + f₂⁽²⁾',22,R,center=True)
 else:d.text(330,391,'同じ点を共有する二つの要素を組み立てる',18,center=True)
 return d
save(assembly(),26,'before');save(assembly(True),26)

def coordinates(after=False):
 d=fig('三角形は面積の比、四面体は体積の比')
 a,b,c,p=(42,278),(291,278),(156,91),(160,208)
 poly(d,[a,b,c],F);d.path([a,b,c,a],N,2)
 for i,v in enumerate((a,b,c),1):d.path([v,p],G,1.5);d.dot(*v,N);d.text(v[0],v[1]+23 if i<3 else v[1]-12,str(i),15,center=True)
 d.dot(*p,R);d.text(180,201,'P',17,R)
 d.text(104,181,'A₂',17,center=True);d.text(219,184,'A₁',17,center=True);d.text(167,253,'A₃',17,center=True)
 # A tetrahedron with four vertices; hidden edge drawn dashed, not a solid cube.
 v1,v2,v3,v4=(363,280),(612,280),(494,91),(452,201)
 poly(d,[v1,v2,v3],F);d.path([v1,v2,v3,v1],N,2)
 d.path([v1,v4,v2],G,1.5,'4 4');d.path([v4,v3],G,1.5,'4 4')
 pp=(494,236)
 for vv in (v1,v2,v3,v4):d.path([pp,vv],R,1,'3 3')
 d.dot(*pp,R);d.text(508,237,'P',15,R)
 for i,v in enumerate((v1,v2,v3,v4),1):d.dot(*v,N);d.text(v[0]+8,v[1]+20,str(i),14)
 d.text(490,324,'四つの小体積Viに分ける',15,center=True)
 d.text(169,324,'三つの小面積Aiに分ける',15,center=True)
 if after:
  d.text(165,365,'Li = Ai / A、和は1',18,R,center=True)
  d.text(493,365,'ωi = Vi / V、和は1',18,R,center=True)
  d.text(330,409,'重心：三角形は各1/3 ／ 四面体は各1/4',18,center=True)
 else:d.text(330,389,'面積・体積を、同じ種類の全体量で割る座標',18,center=True)
 return d
save(coordinates(),29,'before');save(coordinates(True),29)

ns='{http://www.w3.org/2000/svg}';count=0
for info in mapping.values():
 for mode in ('after','before'):
  name,key=info[mode+'_svg'],info[mode+'_key']
  if not name:continue
  p=DEST/name;tree=ET.parse(p);assert tree.getroot().attrib['viewBox']=='0 0 660 420'
  assert not any(tree.findall('.//'+ns+t) for t in ('text','image','use','foreignObject'))
  for e in tree.iter():
   assert not any('href' in k for k in e.attrib)
   for k in ('fill','stroke'):
    if k in e.attrib:assert e.attrib[k] in (N,R,G,F,W,'none')
  doc=fitz.open(p);pdf=fitz.open('pdf',doc.convert_to_pdf());scale=1320/pdf[0].rect.width
  target=ROOT/'assets/figures'/f'{key}.png';pdf[0].get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False).save(target)
  compressed=compress_bytes(target)
  if compressed:target.write_bytes(compressed)
  (OUT/name.replace('.svg','.png')).write_bytes(target.read_bytes());count+=1
placement='# 第4章 図の配置指示\n\n変更した問題と理解が難しい箇所のみ新しい独自図へ差し替え。その他は既存図を使用。\n\n色：主線 #1F3A65／結果・強調 #C82D2D／補助線 #888888／面塗り #E1E7F2（不透明）／背景白。\n660×420、文字はメイリオをパス化、外部参照・フォント・ラスター画像なし。PNGは1320×840。\n回答前は与件のみ、回答後は結果を表示。\n\n'
placement+='4-1は厚みと貫通穴をもつ板部品と、同じ形状を分割した三角形メッシュの対応。内周から外周への環状分割で穴を保持する。分割は概念説明用で、精度を保証する解析メッシュではない。4-3の曲線は残差の符号の模式図。4-6は単調な応力–ひずみ曲線の面積区分。4-23のばね図は模式図で、計算の角度は45°。4-29は面積・体積比の概念図で、図の寸法から値を読み取らない。\n\n'
for n,info in mapping.items():placement+=f'- {n}：{info["after_svg"]}；回答前：{info["before_svg"] or "なし"}\n'
(OUT/'図の配置指示.md').write_text(placement,encoding='utf-8');(DEST/'図の配置指示.md').write_text(placement,encoding='utf-8')
with zipfile.ZipFile(OUT/'固体2級_第4章_図_完成版.zip','w',zipfile.ZIP_DEFLATED) as z:
 for info in mapping.values():
  for mode in ('after','before'):
   if info[mode+'_svg']:z.write(DEST/info[mode+'_svg'],info[mode+'_svg'])
 z.write(OUT/'図の配置指示.md','図の配置指示.md')
print(f'{count} SVG/PNG figures validated and rendered.')
