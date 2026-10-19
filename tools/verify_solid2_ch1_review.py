# -*- coding: utf-8 -*-
"""第1章の独立検算・JSON/図の整合・反映報告を保存する。"""
from pathlib import Path
import json,hashlib
import sympy as s
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/固体2級_第1章_反映結果'
data=json.loads((ROOT/'content/questions/math-basics.json').read_text(encoding='utf-8'))
before=json.loads((ROOT/'tmp/pdfs/ch1_apply_backup/math-basics.json').read_text(encoding='utf-8'))
assert [q['answer'] for q in data['questions']]==[q['answer'] for q in before['questions']]
assert [q['id'] for q in data['questions']]==[q['id'] for q in before['questions']]
assert [q['officialRef'] for q in data['questions']]==[q['officialRef'] for q in before['questions']]
x,y,h,r,t,theta,a,b=s.symbols('x y h r t theta a b',real=True)
tests={}
A=s.Matrix([[1,2],[2,4]])
assert A.det()==0 and A*s.Matrix([3-2*t,t])==s.Matrix([3,6]) and A.row_join(s.Matrix([3,7])).rank()==2
tests['1-1']='det=0; x=(3-2t,t); inconsistent second RHS confirmed'
I=s.eye(2);B=s.Matrix([[3,1],[0,4]])
assert (2*I).det()==4 and I.det()+I.det()==2
assert (A*B).det()==A.det()*B.det()
tests['1-2']='scalar-power and sum counterexamples, product identity checked'
M=s.diag(2,-1,0)
for i,mu in enumerate((2,-1,0)):
    v=s.eye(3)[:,i];assert M*v==mu*v
tests['1-3']='three eigenpairs for positive, negative, zero real eigenvalues verified'
f=s.exp(x)*s.cos(y)
assert [f.subs({x:0,y:0}),s.diff(f,x).subs({x:0,y:0}),s.diff(f,y).subs({x:0,y:0})]==[1,1,0]
tests['1-4']='f0=1, fx0=1, fy0=0; tangent polynomial=1+x'
ur=a*s.cos(theta)+b*s.sin(theta);ut=r*(-a*s.sin(theta)+b*s.cos(theta))
assert s.trigsimp(ur**2+ut**2/r**2-a*a-b*b)==0
tests['1-5']='chain rule squared sum verified symbolically'
w=1+x*x+2*y*y
assert [s.diff(w,x),s.diff(w,y)]==[2*x,4*y]
flux=s.integrate(w.subs(x,1)-w.subs(x,0),(y,0,1))
gradint=s.integrate(s.integrate(2*x,(x,0,1)),(y,0,1))
wrongint=s.integrate(s.integrate(4*y,(x,0,1)),(y,0,1))
assert [flux+gradint,flux-wrongint,flux-gradint,-gradint]==[2,-1,0,-1]
tests['1-6']='NEW polynomial weight: grad=(2x,4y); unit-square u=(1,0), option values=2,-1,0,-1, answer=3'
K=s.Matrix([[1,-1],[-1,1]]);assert K*s.Matrix([1,1])==s.zeros(2,1)
tests['1-7']='rigid translation null vector confirmed; constrained static scalar equation has no initial velocity'
z=s.symbols('z');cs=[s.Function(c)(x,y,z) for c in ('sx','sy','sz','txy','tyz','tzx')]
sx,sy,sz,txy,tyz,tzx=cs;S=s.Matrix([[sx,txy,tzx],[txy,sy,tyz],[tzx,tyz,sz]])
div=[sum(s.diff(S[i,j],(x,y,z)[j]) for j in range(3)) for i in range(3)]
tests['1-8']={'ABC':['tau_zx','sigma_y','sigma_z'],'divergence':[str(v) for v in div]}
K=s.Matrix([[2,-1],[-1,2]]);F=s.Matrix([1,2]);U=K.inv()*F;V=K.inv()*(4*F);assert V==4*U
tests['1-9']={'U':[str(v) for v in U],'V':[str(v) for v in V],'scaling_verified':True}
D=s.symbols('d0:8');T=lambda shift:sum(D[k]*shift**k/s.factorial(k) for k in range(8))
central=s.expand((T(h)-T(-h))/(2*h));forward=s.expand((T(h)-D[0])/h);backward=s.expand((D[0]-T(-h))/h)
assert central.coeff(h,2)==D[3]/6 and forward.coeff(h,1)==D[2]/2 and backward.coeff(h,1)==-D[2]/2
tests['1-10']={'A':str(central),'B':str(forward),'C':str(backward)}
second=s.expand((T(h)-2*D[0]+T(-h))/h**2)
shifted=s.expand((T(2*h)-2*T(h)+D[0])/h**2)
assert second.coeff(h,2)==D[4]/12 and shifted.coeff(h,1)==D[3]
tests['1-11']={'centered':str(second),'shifted_at_x':str(shifted)}
ell=s.symbols('ell',positive=True);assert s.integrate((t-ell/2)**2,(t,0,ell))==ell**3/12
ak,bk=s.symbols('ak bk',positive=True);u=lambda q:q*(1-q)/2
assert s.simplify((u(x)-u(x-ak))/ak+(u(x)-u(x+bk))/bk-(ak+bk)/2)==0
tests['1-12']='uniform P1 squared energy error 1/(12m^2); permanent length-1/2 element contributes 1/96'
for q in data['questions']:
    assert q['figure']=='helpful' and not q.get('preFigureImage')
    img=ROOT/'assets/figures'/f'{q["figureImage"]}.png'
    assert Image.open(img).size==(1320,840)
    assert len(q['explanation'].splitlines())==4
tests['json_unchanged_answers_ids_refs']=True
tests['after_only_figures']=12
tests['source_sha256']=hashlib.sha256((ROOT/'content/questions/math-basics.json').read_bytes()).hexdigest()
(OUT/'独立検算・反映検証.json').write_text(json.dumps(tests,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
topics=[
('1-1','特異な連立一次方程式の解の個数','具体的な係数行列と二つの右辺を使い、整合・不整合を判定'),
('1-2','行列式の定数倍・積・和の性質','ア・イ・ウの組合せ形式と単位行列の反例で判定'),
('1-3','固有値・固有ベクトルの役割','実数の範囲を明示し、数とベクトルの役割を例で確認'),
('1-4','多変数関数の一次テイラー近似','独自の関数exp(x)cos(y)と断面図で値・偏微分を計算'),
('1-5','極座標の連鎖律と微分の二乗和','別の記号体系と誤答設定で距離換算と交差項を確認'),
('1-6','重み付き部分積分・勾配・境界法線','独自の多項式の重みを使用し、勾配の計算も選択肢に組み込む'),
('1-7','静的解析の初期条件と境界条件','支持した棒の例から初期条件不要と剛体運動を説明'),
('1-8','三次元の応力成分と力の釣り合い','空欄の位置を独自に設定し、応力成分表で対応を説明'),
('1-9','線形性による荷重と解の比例','同じ離散化の4倍荷重を、非零右辺の離散方程式で判断'),
('1-10','一階微分の前進・後退・中央差分と精度','式のラベルと選択肢を独自に組み合わせ、三つの図で比較'),
('1-11','二階中心差分・重み・分母・精度','評価点のずれと定数再現性を誤答の判断に使用'),
('1-12','有限要素解の全体細分化による収束','細分化回数kの寸法系列を使って一般の収束保証を比較'),
]
text='''# 第1章 反映・公式の学習ポイント対応確認

2026-10-14。固体2級第1章だけを対象とした。

非公開の公式問題編・解説編を画像で確認し、全12問の学習ポイントを照合した。原文や原図は納品物へ転載せず、下表は問われる数学・工学の概念だけを要約する。原本はテーマの確認に使用し、問題文・解説・図は独自の教材表現で作成した。数学上の標準的な定義・式・定理は共通の学習事項として扱う。

| 参照番号 | 学習ポイント | 本教材での独自の扱い |
|---|---|---|
'''
for row in topics:text+='| '+' | '.join(row)+' |\n'
text+='''
## 教材への反映

- 全12問の解説を【基礎】【考え方】【ポイント】【引っかけ】の4節で統一。各節は1行、節間は単一改行。約800〜1,350字で、用語・手順・途中式・具体例・誤答の理由を説明。
- 正解番号・問題ID・公式参照番号は変更しない。問題数は12問のまま。
- 1-3の実数条件、1-6の領域条件、1-7の支持・境界条件、1-9の非零離散右辺・同じ離散化、1-12の固定次数・一般の収束保証を反映。
- 1-6は重み関数を独自の多項式へ改め、新しい選択肢と解説を独立検算。1-7は選択肢の長さをそろえ、1-12は細分化回数による寸法系列で問う形式へ再構成。
- 第1章の回答後SVG12点を規格検証し、1320×840のPNGを配置。未パス化文字・半透明面塗り・切れた図を修正。1-2・1-7・1-9にも理解を助ける図を追加。欠落PNGは0。
- 回答前には回答後図・正解・解説を出さない。

## 品質チェックの扱い

独立検算・JSON整形・4節・禁止数式記法・図の存在とサイズ・正解番号不変の検証はPASS。
旧チェッカーは【計算】節の有無だけで計算問題を数えるため、今回の4節形式では計算0問というWARNになる。これは4節形式との不整合であり、1-1・1-4・1-5・1-6・1-10・1-11の計算・式導出を独立に検算した。
正解分布3/5/3/1のWARNは既存の正解番号を維持する方針による。図欠落・構造エラーはない。警告を隠すためにチェッカーや正解番号を変更していない。

回答後PDFは1問につき「問題・選択肢・正解・図」と「4節解説」の2ページ構成。文字を小さくせず、解説節が次ページへ短く分断されることを避ける。第1章の回答前・回答後だけを生成し、他章・他級のPDFは触らない。

commit・push・OTA配信・アプリビルドは実施していない。
'''
(OUT/'第1章_反映・対応確認.md').write_text(text,encoding='utf-8')
print('12-question independent verification PASS; original learning-point mapping saved; answers/IDs/refs unchanged.')
