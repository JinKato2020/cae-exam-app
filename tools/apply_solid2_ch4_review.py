# -*- coding: utf-8 -*-
"""第4章の校閲と高校生向け四節解説。原本の抽出テキストに照合。"""
from pathlib import Path
import json,hashlib,re,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/固体2級_第4章_反映結果'
TMP=ROOT/'tmp/pdfs/ch4_review'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
QP=ROOT/'content/questions/fem-basics.json';FP=ROOT/'content/formulas/ch4.json'
def encoded(d):return (json.dumps(d,ensure_ascii=False,indent=2).replace('\n','\r\n')+'\r\n').encode('utf-8')
data=json.loads(QP.read_bytes());terms=json.loads(FP.read_bytes())
assert encoded(data)==QP.read_bytes() and encoded(terms)==FP.read_bytes()
assert data['meta']['chapter']==4 and len(data['questions'])==29
for p in (QP,FP):
 dest=TMP/(p.stem+'-before.json')
 if not dest.exists():shutil.copy2(p,dest)
hp=TMP/'protected-hashes.json'
if not hp.exists():
 paths=list((ROOT/'content/questions').glob('*.json'))+list((ROOT/'content/formulas').glob('*.json'))+list((ROOT/'アプリ').rglob('*.pdf'))
 hp.write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p not in (QP,FP)},ensure_ascii=False,indent=2),encoding='utf-8')
qs={q['number']:q for q in data['questions']}
def patch(n,**fields):qs[f'4-{n}'].update(fields)
def explain(n,base,thinking,point,traps):
 patch(n,explanation='\n'.join((r'【基礎】'+base,r'【考え方】'+thinking,r'【ポイント】'+point,r'【引っかけ】'+traps)))

# 公式と同じ論点へ戻す。文章・設定・選択肢は独自作成し正解番号を維持。
patch(3,title='重み付き残差法とガラーキン法',question=r'支配方程式 $\mathcal L u=f$ の近似解を $u_h=\sum_jN_jd_j$ とし、残差を $R=\mathcal L u_h-f$ とする。重み付き残差法の説明として適切なのはどれか。',choices=[r'重み関数 $w_i$ ごとに $\int_Vw_iR\,dV=0$ とする。$w_i=N_i$ と選ぶ方法がガラーキン法である。','近似解は必ず各点で残差を完全にゼロにする。','支配方程式を使わず、材料定数だけから解を決める。','残差を重み付けせず各点で二乗すれば、常にガラーキン法になる。'],relatedFormulas=['weighted-residual'])
patch(4,title='段付き棒のひずみエネルギー比較',question=r'同じ材料 $E=200\,\mathrm{GPa}$、全長 $L=300\,\mathrm{mm}$ の棒Iと棒IIを考える。棒Iは、固定端側100mmの断面積が200mm²、残り200mmが100mm²の段付き棒。棒IIは全長で断面積200mm²の一様棒である。左端固定で軸方向に変形させる。両棒に同じ引張力 $P=10\,\mathrm{kN}$ を与えた場合、および同じ端部伸び $\delta=0.12\,\mathrm{mm}$ を与えた場合の、ひずみエネルギーの大小関係はどれか。微小変形・線形弾性とし、途中に軸荷重はない。',choices=['同じ力でも同じ伸びでも、棒Iの方が大きい。','同じ力でも同じ伸びでも、棒IIの方が大きい。','同じ力では棒IIの方が大きく、同じ伸びでは棒Iの方が大きい。','同じ力では棒Iの方が大きく、同じ伸びでは棒IIの方が大きい。'])
patch(6,title='ひずみエネルギーと補ひずみエネルギー',question=r'応力 $\sigma$ とひずみ $\varepsilon$ の関係が原点を通る単調な弾性曲線であるとする。ひずみエネルギー密度 $U_0=\int_0^\varepsilon\sigma\,d\varepsilon$ と、補ひずみエネルギー密度 $U_0^*=\int_0^\sigma\varepsilon\,d\sigma$ について適切なのはどれか。',choices=[r'線形弾性なら両者は $\sigma\varepsilon/2$ で等しい。非線形弾性では一般に等しくない。','線形・非線形にかかわらず、両者は常に等しい。','補ひずみエネルギーは動的問題だけで定義される。','補ひずみエネルギーは必ずひずみエネルギーの2倍である。'],relatedFormulas=['energy-methods','strain-energy'])
patch(8,title='変位法・応力法と仮想仕事',question='変位法と応力法の、主な未知量と基礎となる原理の対応として適切なのはどれか。',choices=['変位法は応力を主な未知量とし、補仮想仕事の原理を用いる。','応力法は節点変位を主な未知量とし、仮想仕事の原理を用いる。','変位法は節点変位と仮想仕事の原理、応力法は応力・力と補仮想仕事の原理を対応させる。','どちらも材料定数を未知量とし、ひずみと変位の関係を使わない。'],relatedFormulas=['energy-methods','virtual-work'])
patch(9,question=qs['4-9']['question'].replace('両端はピン接合。','A、Bは位置が固定された支持点で、各接合部はピン接合。棒の自重は無視する。'))
patch(10,question='保守的な荷重と適切な拘束をもつ、安定な微小変形・線形弾性体が静的平衡にある。仮想仕事の原理について適切なのはどれか。')
patch(18,question=qs['4-18']['question'].replace('初期ひずみなし','初期ひずみ・初期応力なし'))
patch(20,title='B行列の成分と自由度の順序',question=r'微小変形の二次元変位要素で、節点変位を $\mathbf d=[u_1,v_1,u_2,v_2,\ldots]^T$、ひずみを $[\varepsilon_x,\varepsilon_y,\gamma_{xy}]^T$ の順に並べる。$N_{i,x}=\partial N_i/\partial x$ とする。節点 $i$ の2列に対応する $\mathbf B_i$ として正しいものはどれか。',choices=[r'$\begin{bmatrix}N_{i,y}&0\\0&N_{i,x}\\N_{i,x}&N_{i,y}\end{bmatrix}$',r'$\begin{bmatrix}N_{i,x}&0\\0&N_{i,y}\\N_{i,y}&N_{i,x}\end{bmatrix}$',r'$\begin{bmatrix}N_{i,x}&0\\0&N_{i,y}\\N_{i,x}&N_{i,y}\end{bmatrix}$',r'$\begin{bmatrix}N_{i,x}&0\\0&N_{i,y}\\-N_{i,y}&N_{i,x}\end{bmatrix}$'],relatedFormulas=['b-matrix','strain-displacement'])
patch(21,question=r'等方線形弾性体の平面応力と平面ひずみの材料行列 $\mathbf D$ を考える。$E>0,\ 0<\nu<0.5$ とする。適切な説明はどれか。')
patch(22,title='直列ばねの剛性方程式',question=r'節点1を固定し、節点1–2を $k_1=100\,\mathrm{N/mm}$、節点2–3を $k_2=200\,\mathrm{N/mm}$ のばねで結ぶ。右向きを正とする変位を $u_2,u_3$、既知の節点外力を $f_2,f_3$ とする。$\begin{bmatrix}A&B\\C&D\end{bmatrix}[u_2,u_3]^T=[f_2,f_3]^T$ の係数 $(A,B,C,D)$ はどれか。数値の単位はすべてN/mmとする。',choices=['(100, −200, −200, 200)','(300, 200, 200, 200)','(300, −100, −100, 200)','(300, −200, −200, 200)'],relatedFormulas=['element-stiffness','stiffness-properties'])
patch(23,title='斜めばねを含む系の剛性方程式',question=r'節点1は左右には動くが上下には動かない。左上と左下の固定点から節点1へ、水平となす角がそれぞれ45°の軸方向ばねを接続する。各ばねの軸方向ばね定数は $k=120\,\mathrm{N/mm}$。節点1と右側の節点2を、同じばね定数 $k$ の水平ばねで結ぶ。節点2も水平方向だけに動く。微小変形で、右向き変位 $u_1,u_2$ に対する2×2剛性行列はどれか。',choices=[r'$\begin{bmatrix}360&-120\\-120&120\end{bmatrix}\,\mathrm{N/mm}$',r'$\begin{bmatrix}240&120\\120&120\end{bmatrix}\,\mathrm{N/mm}$',r'$\begin{bmatrix}120&-120\\-120&120\end{bmatrix}\,\mathrm{N/mm}$',r'$\begin{bmatrix}240&-120\\-120&120\end{bmatrix}\,\mathrm{N/mm}$'],relatedFormulas=['element-stiffness','stiffness-properties'])
patch(24,title='剛性行列の対称性と対角成分',question=r'安定な等方線形弾性材料を用いる、微小変形・変位型FEMの剛性行列 $\mathbf K$ を考える。剛性をもつ並進自由度について、適切なのはどれか。',choices=['行列は必ず非対称である。','対角成分はすべて負である。','すべての非対角成分は、要素の方向によらず負である。','行列は対称で、対角成分は正である。非対角成分の符号は、一般には要素の方向などに依存する。'],relatedFormulas=['stiffness-properties','element-stiffness'])
patch(26,title='共有節点での重ね合わせ',question=r'直列の節点1–2–3に、ばね要素①（1–2）と②（2–3）を接続する。全体の節点2変位を $u_2$、要素ごとの同じ節点の変位を $u_2^{(1)},u_2^{(2)}$ とする。要素内力の節点2への寄与を $f_2^{(1)},f_2^{(2)}$、その和を $f_2$ とする。正しい組立ての関係はどれか。',choices=[r'$u_2=u_2^{(1)}+u_2^{(2)},\quad f_2=f_2^{(1)}=f_2^{(2)}$',r'$u_2=u_2^{(1)}=u_2^{(2)},\quad f_2=f_2^{(1)}-f_2^{(2)}$',r'$u_2=u_2^{(1)}=u_2^{(2)},\quad f_2=f_2^{(1)}+f_2^{(2)}$',r'$u_2=u_2^{(1)}+u_2^{(2)},\quad f_2=f_2^{(1)}+f_2^{(2)}$'],relatedFormulas=['stiffness-properties','element-stiffness'])
patch(27,relatedFormulas=['boundary-dof']);patch(28,relatedFormulas=['boundary-dof'])
patch(29,title='面積座標と体積座標',question=r'三角形の面積座標 $L_1,L_2,L_3$ と、四面体の体積座標 $\omega_1,\omega_2,\omega_3,\omega_4$ を考える。内部および辺・面上で成り立つ性質として適切なのはどれか。',choices=['各座標は長さの単位をもつ。',r'いずれも無次元で、同じ点の座標の和は1。一次三角形では $N_i=L_i$、一次四面体では $N_i=\omega_i$ となる。','三角形の重心でも四面体の重心でも、すべての座標は1/3である。','三角形や四面体の頂点では、対応する座標が0、他の座標が1になる。'])

explain(1,'有限要素法は、物体を小さな要素に分け、節点の変位など有限個の未知数で近似する方法です。この独立な変位成分を自由度と呼びます。',r'複雑な形状や境界条件を、有限個の自由度の連立方程式へ変換して解けることが利点です。線形静解析なら $\mathbf K\mathbf d=\mathbf f$ と表し、正解は1です。','近似なので、要素の選択とメッシュを細かくしたときの収束確認が必要です。','(2)支配方程式に基づく近似法です。(3)材料定数は試験などで別途与えます。(4)粗くすれば常に高精度になるわけではありません。')
explain(2,'離散化は「連続な問題から、有限個の未知数の方程式を作る段階」です。その方程式を解く計算とは区別します。','ガウス・ザイデル法は、できあがった連立一次方程式の未知数を順に更新して解く反復法です。離散化法ではないので正解は3です。','離散化してから、直接法や反復法で連立方程式を解きます。','(1)重み付き残差法は積分条件から方程式を作ります。(2)レイリー・リッツ法はエネルギーの停留条件を使います。(4)差分法は微分を格子点の差で近似します。')
explain(3,r'残差 $R$ は、近似解を支配方程式へ代入したときの「式のずれ」です。近似解では、一般に各点のずれを完全には消せません。',r'重み関数 $w_i$ を掛けて積分し、$\int_Vw_iR\,dV=0$ という条件を重みごとに課します。近似に使う $N_i$ を重みにも使うのがガラーキン法なので、正解は1です。','積分が0でも、各点で残差が0とは限りません。正のずれと負のずれが積分で打ち消される場合もあります。','(2)各点で完全一致するとは限りません。(3)残差を作るには支配方程式が必要です。(4)残差の二乗と、同じ基底関数を重みにする操作は別です。')
explain(4,r'棒の剛性を $k=P/\delta$ とすると、同じ力では $U=P^2/(2k)$、同じ伸びでは $U=k\delta^2/2$ です。段付き棒では区間ごとの伸びを足します。',r'$E=200000\,\mathrm{N/mm^2}$。棒Iは $\delta_I/P=100/(E\times200)+200/(E\times100)=1.25\times10^{-5}\,\mathrm{mm/N}$ なので $k_I=80000\,\mathrm{N/mm}$。棒IIは $k_{II}=E\times200/300=133333.3\,\mathrm{N/mm}$ です。同じ10000Nなら $U_I=0.625\,\mathrm J>U_{II}=0.375\,\mathrm J$。同じ0.12mmなら $U_I=0.576\,\mathrm J<U_{II}=0.960\,\mathrm J$。正解は4です。',r'棒Iの方が柔らかいので、同じ力では大きく伸びます。同じ伸びでは、硬い棒IIの方が大きな力を必要とします。$1\,\mathrm{N\,mm}=0.001\,\mathrm J$ です。','(1)(2)何を同じにするかで大小関係が逆転します。(3)力一定と伸び一定の大小関係を逆にしています。')
explain(5,'ひずみエネルギー密度は、単位体積に蓄えられるエネルギーです。初期項のない線形弾性では、対応する応力とひずみの積の和を1/2倍します。',r'$U_0=(\sigma_x\varepsilon_x+\sigma_y\varepsilon_y+\tau_{xy}\gamma_{xy})/2$ です。工学せん断ひずみ $\gamma_{xy}$ を用いているので、せん断項をさらに2倍しません。正解は3です。',r'平面応力では $\sigma_z=0$、平面ひずみでは $\varepsilon_z=0$ なので、面外の積はどちらも0です。密度の単位は $\mathrm{Pa}=\mathrm{J/m^3}$ です。','(1)係数1/2がありません。(2)対応する方向が違い、せん断項もありません。(4)応力の二乗だけではエネルギー密度の単位になりません。')
explain(6,r'応力–ひずみ線図で、曲線の下の面積が $U_0$、曲線と縦軸の間の面積が $U_0^*$ です。二つの面積の合計は長方形の面積 $\sigma\varepsilon$ になります。',r'線形弾性の直線は長方形を同じ面積の三角形に分けるため、両者は $\sigma\varepsilon/2$ です。曲線では一般に二つの面積が異なります。正解は1です。','ここで比較するのは材料のひずみエネルギーと補ひずみエネルギーです。外力の項まで含む全ポテンシャルエネルギーとは区別します。','(2)曲線で常に等しくなるとは限りません。(3)静的弾性でも使います。(4)線形では同じ値であり、一定の2倍関係はありません。')
explain(7,r'全ポテンシャルエネルギーは $\Pi=U-W$ です。$U$ は蓄えられるひずみエネルギー、$-W$ は保守的な外力のポテンシャルです。指定変位を守る変位だけを比較します。',r'ばねなら $\Pi(u)=ku^2/2-Pu$。微分すると $d\Pi/du=ku-P=0$ から $u=P/k$、二階微分は $k>0$ なので最小です。本問の安定な線形弾性でも最小となり、正解は3です。','一階の変化が0という「停留」だけでは最小とは限りません。本問では正定値の剛性と適切な拘束があるので最小と判断できます。','(1)最大ではありません。(2)指定変位を満たす候補に限ります。(4)荷重点だけでなく、全体のエネルギーを比較します。')
explain(8,'変位法は変位を先に求め、ひずみ・応力へ進みます。応力法は応力や部材力などを先に求め、変形のつながりを満たすように決めます。','変位法には、試しの変位に対して仕事が釣り合う「仮想仕事の原理」が対応します。応力法には、試しの応力・力の変化を用いる「補仮想仕事の原理」が対応します。正解は3です。','「何を未知量にするか」と「何を仮に変化させるか」を組にして覚えます。','(1)変位法の主な未知量は変位です。(2)応力法の主な未知量は応力や力です。(4)材料定数は入力し、どちらも変位とひずみの関係が必要です。')
explain(9,r'仮想変位は、力の釣合いを調べるための小さな試しの移動です。$\delta x$ と $\delta y$ は独立に選べるので、仕事の式の各係数が0になります。',r'Cでの仕事の和は $(-N_{CA}\cos30^\circ+N_{CB}\cos60^\circ)\delta x+(N_{CA}\sin30^\circ+N_{CB}\sin60^\circ-20)\delta y=0$ です。水平式から $N_{CB}=\sqrt3N_{CA}$。鉛直式へ入れると $N_{CA}/2+3N_{CA}/2=20$ より $N_{CA}=10\,\mathrm{kN}$。したがって $N_{CB}=10\sqrt3=17.32\,\mathrm{kN}$、正解は4です。','任意の試しの移動で仕事が釣り合う、という条件から水平・鉛直の力の釣合いが出ます。両部材力が正なので引張です。',r'(1)10kNはCAの力です。(2)20を $\sin60^\circ$ だけで割ると、CAの鉛直成分を無視します。(3)34.64kNでは水平式を合わせても鉛直力が40kNとなり、20kNと釣り合いません。')
explain(10,'仮想仕事の原理は、許容される試しの微小変位に対して「内部の仕事＝外力の仕事」が成り立つことです。','静的平衡では、すべての許容仮想変位に対して両者が等しくなるので、正解は1です。変位が指定された場所では指定値を変えられないため、仮想変位は0です。','本問の安定な線形弾性・保守荷重では、この条件は全ポテンシャルエネルギーの停留条件と対応し、平衡状態で最小となります。実変位と仮想変位は別で、指定変位が0でなくても、その場所の仮想変位は0です。','(2)実変位の一定倍に限りません。(3)適切に定式化すれば非線形材料にも使えます。(4)外部仕事は一般に0ではなく、内部仕事と等しくなります。')
explain(11,'平衡方程式は物体の各点で力の釣合いを表します。仮想仕事の式は、その釣合いを物体全体の積分で表した形です。','平衡方程式に仮想変位を掛けて積分し、部分積分すると、内部の仕事と境界の表面力の仕事が現れます。領域内の平衡と指定表面力条件をまとめるので、正解は3です。','ひずみ–変位関係と材料則は引き続き必要です。変位境界条件も、許容変位と仮想変位に組み込みます。','(1)材料則だけの式ではありません。(2)ひずみ–変位関係だけでもありません。(4)通常の仮想仕事は変位条件だけの罰則項ではありません。')
explain(12,r'仕事は「力×その方向の変位」です。表面力 $\mathbf t$ は単位面積当たりの力なので、面上で積分します。',r'指定表面の外部仮想仕事は $\int_{\Gamma_t}\mathbf t\cdot\delta\mathbf u\,dS$ です。内積は同じ方向の力と変位を掛けて足す操作です。正解は3です。',r'単位は $(\mathrm{N/m^2})\times\mathrm m\times\mathrm{m^2}=\mathrm{N\,m}$。積分記号の下が体積Vか表面 $\Gamma_t$ かも確認します。','(1)体積力の仕事です。(2)内部の応力の仕事です。(4)慣性に関する項です。')
explain(13,r'$\mathbf B\mathbf d$ は全ひずみ、$\boldsymbol\varepsilon_0$ は熱膨張などの初期ひずみです。差に材料行列 $\mathbf D$ を掛けて応力にし、初期応力 $\boldsymbol\sigma_0$ を加えます。',r'内力 $\int_V\mathbf B^T\boldsymbol\sigma\,dV$ へ代入すると、$\mathbf K\mathbf d-\int_V\mathbf B^T\mathbf D\boldsymbol\varepsilon_0\,dV+\int_V\mathbf B^T\boldsymbol\sigma_0\,dV=\mathbf f$。初期項を右辺へ移すので、初期ひずみ項はプラス、初期応力項はマイナスになります。正解は3です。',r'$\mathbf B^T$ は応力を節点力へ換算する側の行列です。初期ひずみは無次元なので、$\mathbf D$ で応力にしてから換算します。','(1)初期応力の移項後の符号が逆です。(2)初期ひずみにDを掛けていません。(4)既に応力である初期応力へDを重ねて掛けています。')
explain(14,'残差は平衡式のずれ、仮想変位はそのずれを測る重みです。部分積分は、微分を一方の関数から他方へ移す操作です。','残差に仮想変位を掛けて積分し、部分積分すると、応力と仮想ひずみの内部仕事、表面力と仮想変位の境界仕事が得られます。正解は1です。','指定変位の境界では仮想変位が0。指定表面力の境界では、その既知の力を境界項に入れます。重みに近似の基底関数を使えばガラーキン法につながります。','(2)部分積分で慣性が自動的に消えるわけではありません。(3)表面力の条件を境界項へ反映します。(4)ガラーキン法でも部分積分を使います。')
explain(15,r'形状関数は、節点変位から要素内の変位を補う重みです。$N_i(x_j)=\delta_{ij}$ は「自分の節点で1、他の節点で0」を意味します。',r'補間は $u=\sum_iN_iu_i$。全節点を同じ $c$ だけ動かすと、$u=c\sum_iN_i=c$ です。和が1なので、要素全体の同じ平行移動を再現できます。正解は2です。','形状関数は補間、Bは微分によるひずみへの変換、Dは材料の応力への変換です。','(1)一般に位置によって変わります。(3)和が0なら一様変位を再現できません。(4)応力には変位の微分と材料則も必要です。')
explain(16,r'一次棒要素では変位を直線で補間します。左端の重み $N_1=1-x/L$、右端の重み $N_2=x/L$ を使います。',r'$x=3L/4$ では $N_1=1/4,\ N_2=3/4$。$u=(1/4)\times3+(3/4)\times9=7.5\,\mathrm{mm}$。正解は4です。','右端に近いので、答えも右端の9mmに近くなります。重みの和は1、答えは3〜9mmの間です。','(1)6mmは中央の値です。(2)9mmは右端そのものの値です。(3)4.5mmは重みを左右逆にした値です。')
explain(17,r'垂直ひずみは、その方向の変位の変わり方です。$\varepsilon_x=\partial u/\partial x$、$\varepsilon_y=\partial v/\partial y$。コンマは偏微分の略記です。',r'直角の変化には、横線と縦線の両方の傾きが寄与するので、工学せん断ひずみは $\gamma_{xy}=u_{,y}+v_{,x}$ です。正解は2です。',r'微小剛体回転 $u=-\omega y,\ v=\omega x$ なら、和は $-\omega+\omega=0$。回転するだけではせん断変形しません。','(1)垂直ひずみの微分方向が逆です。(3)変位成分が逆で、せん断も差です。(4)せん断は差ではなく和です。')
explain(18,r'CSTは「一定ひずみ三角形」です。変位を $u=a_1+a_2x+a_3y$、$v=b_1+b_2x+b_3y$ の一次式で補います。',r'微分すると $\varepsilon_x=a_2,\ \varepsilon_y=b_3,\ \gamma_{xy}=a_3+b_2$ で、位置によらない定数です。Dも一定で初期項もないので、応力も一定です。正解は2です。','「一次式を一回微分すると定数になる」が理由です。隣の要素とはひずみや応力の値が違っても構いません。','(1)一次式なのは変位です。(3)一定とは0という意味ではありません。(4)面積だけでなく、節点座標と節点変位が必要です。')
explain(19,r'節点変位 $\mathbf d$ から要素内変位を求めるのがN、ひずみを求めるのがB、ひずみから応力を求めるのがDです。',r'形状関数を座標で微分して並べると、$\boldsymbol\varepsilon=\mathbf B\mathbf d$ が得られます。これがBの役割なので正解は2です。','変位がmmなら、Bの単位は通常1/mmで、掛けたひずみは無次元です。','(1)変位の補間はNの役割です。(3)材料則はDの役割です。(4)節点力には剛性行列が必要で、Bだけでは求められません。')
explain(20,r'Bの列は節点変位、行はひずみ成分に対応します。ここでは列が $u_i,v_i$、行が $\varepsilon_x,\varepsilon_y,\gamma_{xy}$ の順です。',r'$u=N_iu_i+\cdots$、$v=N_iv_i+\cdots$ を微分します。第1行は $\varepsilon_x=u_{,x}$ なので $[N_{i,x},0]$。第2行は $\varepsilon_y=v_{,y}$ なので $[0,N_{i,y}]$。第3行は $\gamma_{xy}=u_{,y}+v_{,x}$ なので $[N_{i,y},N_{i,x}]$。正解は2です。','自由度の並べ方を変えると列の並びも変わります。行列だけを暗記せず、各ひずみの式から一行ずつ作ります。','(1)垂直ひずみのx・y微分が逆です。(3)せん断行のx・y微分が逆です。(4)工学せん断ひずみは和なので、負符号は入りません。')
explain(21,r'Dはひずみを応力へ変換する材料行列です。等方線形弾性では、独立な材料定数はヤング率 $E$ とポアソン比 $\nu$ です。',r'平面応力では面外応力 $\sigma_z=0$、平面ひずみでは面外ひずみ $\varepsilon_z=0$。条件が違うので、同じ材料でも面内のDは一般に異なります。正解は1です。',r'二次元のDは $[\varepsilon_x,\varepsilon_y,\gamma_{xy}]^T$ を $[\sigma_x,\sigma_y,\tau_{xy}]^T$ へ変換します。$G=E/[2(1+\nu)]$ もEとνで決まります。','(2)平面応力と平面ひずみの条件が逆です。(3)等方材料のGは独立な第三の定数ではありません。(4)第三成分は面外成分ではなく面内せん断成分です。')
explain(22,r'一つのばねの伸びは両端変位の差です。節点ごとの力への寄与は、自分の変位に $+k$、相手の変位に $-k$ を掛けます。',r'節点2では $f_2=k_1(u_2-0)+k_2(u_2-u_3)=300u_2-200u_3$。節点3では $f_3=k_2(u_3-u_2)=-200u_2+200u_3$。したがって $(A,B,C,D)=(300,-200,-200,200)$、正解は4です。','節点2の対角は接続する二本の剛性の和です。非対角は節点2–3を直接つなぐばねの負の剛性です。','(1)節点2の対角に二本目の200を足していません。(2)非対角の符号が逆です。(3)節点2–3のばねは100ではなく200です。')
explain(23,r'斜めばねでは、水平変位を軸方向へ投影し、軸力を水平へ戻します。二回の投影があるので、一本の水平剛性は $k\cos^2\theta$ です。',r'45°のばね一本は $120\times(1/\sqrt2)^2=60\,\mathrm{N/mm}$。上下二本で120です。水平ばねの寄与 $120\begin{bmatrix}1&-1\\-1&1\end{bmatrix}$ に、固定点へつながる斜め二本の120を第1対角へ足します。結果は $\begin{bmatrix}240&-120\\-120&120\end{bmatrix}\,\mathrm{N/mm}$ で、正解は4です。','水平変位→軸伸びでcos、軸力→水平力でもcosを掛けます。上下の鉛直成分は対称に打ち消されます。','(1)斜めばねの水平への投影を省いています。(2)水平ばねの非対角は負です。(3)固定点へつながる斜め二本の剛性を省いています。')
explain(24,r'剛性行列は節点変位と節点力の関係です。線形弾性では $K_{ij}=K_{ji}$ となり、対角はその自由度を動かすのに必要な剛性を表します。','本問の標準的な線形弾性では対称で、剛性をもつ自由度の対角成分は正です。一般の非対角成分は方向などに依存するので、正解は4です。',r'一次元のばねでは非対角が $-k$ ですが、斜め要素の同一節点x–y成分は $k\cos\theta\sin\theta$ で正になる場合もあります。','(1)線形弾性の本条件では対称です。(2)剛性をもつ自由度の対角は正です。(3)一次元ばねの負の非対角をすべての要素へ広げられません。')
explain(25,'全節点を同じ量だけ動かすと、各ばねの両端の変位差は0です。伸びがないので力も生じません。',r'同一変位は $\mathbf d=c\mathbf1$。$\mathbf K\mathbf d=\mathbf0$ が任意のcで成り立つので $\mathbf K\mathbf1=\mathbf0$ です。全成分1のベクトルを掛けると各行の和になるため、行和は0。正解は2です。','この説明は拘束前の一次元ばね系です。固定した自由度を除いた後の行列では、行和0は一般に残りません。','(1)ばねごとの剛性が違っても成立します。(3)要素数の偶奇とは関係ありません。(4)回転などを含む一般の行列へ、全成分1のベクトルを無条件に使えません。')
explain(26,'共有節点は一つの場所なので、接続する要素で変位は共通です。一方、力への寄与は、それぞれの要素から足し合わせます。',r'$u_2=u_2^{(1)}=u_2^{(2)}$、$f_2=f_2^{(1)}+f_2^{(2)}$ です。例えば剛性150と250N/mmのばねなら、節点2の対角剛性は400N/mmになります。正解は3です。','「変位は共通、力は加算」が組立ての基本です。各力は同じ全体座標の向きで符号を持つので、和の式に符号付きの値を入れます。','(1)変位を加算し、力を共通にしていて逆です。(2)定義した符号付きの力は差ではなく和です。(4)変位を足すと共有点が一つの変位になりません。')
explain(27,'指定変位は既知です。その変位を保つ支持の力、すなわち反力は、釣合いを満たすように決まります。',r'計算した変位 $\mathbf d$ から、元の剛性行列と既知外力を用いて $\mathbf R=\mathbf K\mathbf d-\mathbf f$ と求めます。正解は2です。','変位境界条件は幾何学的条件、力の境界条件は力学的条件です。固定節点に既知の集中外力がある場合も、反力計算に含めます。','(1)拘束節点に集中外力を加えることはできます。(3)変位0でも荷重を支える反力が出ます。(4)外力を加えるだけでは剛体運動を止められません。')
explain(28,'二次元トラスの節点は、xとyの二つの並進変位を持ちます。独立な回転自由度はありません。',r'全自由度は $5\times2=10$。節点1で2成分、節点3と5で各1成分を拘束するので、未知数は $10-(2+1+1)=6$。正解は1です。','節点2・4のx,yと、節点3・5のxが未知です。未知数の個数と、構造の安定性は別に確認します。','(2)10は拘束前の総数です。(3)4は拘束した成分数です。(4)8は節点1の拘束だけを差し引いた値です。')
explain(29,r'面積座標は部分面積を全体面積で割った比、体積座標は部分体積を全体体積で割った比です。どちらも単位のない割合です。',r'部分面積・体積の和が全体になるので、$L_1+L_2+L_3=1$、$\omega_1+\omega_2+\omega_3+\omega_4=1$。一次要素では、この比が節点値を補間する形状関数になります。正解は2です。','対応する頂点で自分の座標が1、他は0。三角形の重心では各1/3、四面体の重心では各1/4です。','(1)面積同士・体積同士の比なので無次元です。(3)四面体の重心は各1/4です。(4)頂点では1と0の関係が逆です。')

# わかりづらい・変更後の内容と一致しない図のみ、独自図へ差し替え。
new={1:'realistic_plate_mesh',3:'weighted_residual',4:'energy_comparison',6:'complementary_energy',8:'displacement_stress_methods',9:'truss_virtual_work',13:'initial_strain_stress',18:'cst_constant',20:'b_matrix_layout',22:'series_stiffness',23:'inclined_pair',24:'stiffness_properties',26:'assembly_shared_node',29:'area_volume_coordinates'}
before={4,9,22,23,26,29}
mapping={}
for n,short in new.items():
 key=f'solid2Ch4Review{n:02}After';pre=f'solid2Ch4Review{n:02}Before' if n in before else None
 patch(n,figure='helpful',figureImage=key,figureHint='校閲後の問題・解説に対応する高校生向け理解補助図')
 if pre:patch(n,preFigureImage=pre)
 else:qs[f'4-{n}'].pop('preFigureImage',None)
 mapping[f'4-{n}']={'after_svg':f'4-{n}_{short}_after.svg','after_key':key,'before_svg':f'4-{n}_{short}_before.svg' if pre else None,'before_key':pre}
for it in terms['items']:
 if it['id']=='energy-methods':it['figureImage']=qs['4-6']['figureImage']
 if it['id']=='thermal-force':it['figureImage']=qs['4-13']['figureImage']
 if it['id']=='stiffness-properties':it['figureImage']=qs['4-26']['figureImage']
 if it['id']=='area-coordinate':it['figureImage']=qs['4-29']['figureImage']
 if it['id']=='strain-displacement':it['figureImage']=qs['4-18']['figureImage']
 if it['id']=='min-potential':it['body']=it['body'].replace('エネルギーの釣合いからも','エネルギーの停留条件からも')
original=json.loads((TMP/'fem-basics-before.json').read_bytes())
assert [q['answer'] for q in data['questions']]==[q['answer'] for q in original['questions']]
assert [(q['id'],q['officialRef']) for q in data['questions']]==[(q['id'],q['officialRef']) for q in original['questions']]
ids={it['id'] for it in terms['items']}
for q in data['questions']:
 e=q['explanation'];assert len(e.splitlines())==4
 assert [re.match(r'【([^】]+)】',s).group(1) for s in e.splitlines()]==['基礎','考え方','ポイント','引っかけ']
 assert all(f'({i})' in e for i in range(1,5) if i!=q['answer'])
 assert all(i in ids for i in q.get('relatedFormulas',[]))
for d in (data,terms):
 s=json.dumps(d,ensure_ascii=False)
 assert not any(x in s for x in ('$$',r'\\[',r'\\]',r'\\(',r'\\)',r'\\begin{aligned}',r'\\begin{vmatrix}',r'\\boxed'))
QP.write_bytes(encoded(data));FP.write_bytes(encoded(terms))
(OUT/'図マッピング.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in (QP,FP):shutil.copy2(p,OUT/p.name)
print('29 explanations; answer/id/ref unchanged; links resolve; JSON roundtrip passed.')
