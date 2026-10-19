# -*- coding: utf-8 -*-
"""公式原本の主役の式と記号へ整合し、高校生がつまずく手順を補う。"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第3章_反映結果'
TMP=ROOT/'tmp/pdfs/ch3_aligned';TMP.mkdir(parents=True,exist_ok=True)
QP=ROOT/'content/questions/heat-basics.json';FP=ROOT/'content/formulas/ch3.json'
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2).replace('\n','\r\n')+'\r\n').encode('utf-8')
qraw=QP.read_bytes();fraw=FP.read_bytes();data=json.loads(qraw);terms=json.loads(fraw)
assert enc(data)==qraw and enc(terms)==fraw
if not (TMP/'before-questions.json').exists():
    (TMP/'before-questions.json').write_bytes(qraw);(TMP/'before-terms.json').write_bytes(fraw)
    paths=list((ROOT/'content/questions').glob('*.json'))+list((ROOT/'content/formulas').glob('*.json'))+list((ROOT/'アプリ/固体2級').glob('*.pdf'))
    (TMP/'before-hashes.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},ensure_ascii=False,indent=2),encoding='utf-8')
qs={q['number']:q for q in data['questions']}
data['meta']['source']='完全オリジナル（公式標準問題集は学習ポイント・用語・記号・標準公式の確認に使用し、問題文・数値設定・解説文・図は独自作成）'
q=qs['3-10'];q['title']='熱通過率Kを組み立てる';q['topic']='熱通過率'
q['question']=r'両側の流体を通じて熱が移る平板をモデル化する。高温流体の温度を $T_h$、低温流体の温度を $T_c$、それぞれの熱伝達率を $h_h$、$h_c$ とする。板厚は $t$、熱伝導率は $\lambda$。両面の面積は共通、定常一次元・発熱なし・接触熱抵抗なしである。両流体間の温度差と熱流束を $q=K(T_h-T_c)$ で結ぶ熱通過率 $K$ は、どの式で表せるか。'
q['choices']=[r'$K=1/(1/h_h+t/\lambda+1/h_c)$',r'$K=1/h_h+t/\lambda+1/h_c$',r'$K=h_h+\lambda/t+h_c$',r'$K=1/(h_h+\lambda/t+h_c)$']
q=qs['3-11'];q['title']='改善案を熱通過率Kで比べる';q['topic']='熱通過率の改善'
q['question']=r'平板の熱通過率は $1/K=1/h_h+t/\lambda+1/h_c$ で求める。初期の三項は、高温側 $1/h_h=0.20$、壁 $t/\lambda=0.04$、低温側 $1/h_c=0.01\,\mathrm{m^2K/W}$ である。定常一次元・発熱なしで、流体温度差は変えない。案 $A$ は高温側の熱伝達率を $25\%$ 増、案 $B$ は板厚を $25\%$ 減、案 $C$ は低温側の熱伝達率を $25\%$ 増とする。他は変えない。熱通過率 $K$ が最大の案と、その変更後の $1/K$ の組合せはどれか。'
q['choices']=[r'案 $C$、$0.20\,\mathrm{m^2K/W}$。',r'案 $A$、$0.21\,\mathrm{m^2K/W}$。',r'案 $A$、$0.20\,\mathrm{m^2K/W}$。',r'案 $B$、約 $0.19\,\mathrm{m^2K/W}$。']
q=qs['3-12']
q['question']=r'高温側流体は $160\,\mathrm{^\circ C}$、熱伝達率 $h_1=20\,\mathrm{W/(m^2K)}$。低温側流体は $20\,\mathrm{^\circ C}$、$h_2=5\,\mathrm{W/(m^2K)}$ である。その間に、高温側から層 $A$、層 $B$ の順に二層壁がある。Aの厚さは $d_1=0.04\,\mathrm m$、熱伝導率 $\lambda_1=0.4\,\mathrm{W/(m\,K)}$、Bは $d_2=0.08\,\mathrm m$、$\lambda_2=0.8\,\mathrm{W/(m\,K)}$。断面積共通、接触熱抵抗なし、定常一次元・発熱なしとする。熱流束と低温側の壁表面温度の組合せはどれか。'
for n in ('3-7','3-8'):
    qs[n]['question']=qs[n]['question'].replace('$s>0$','$H>0$')
q=qs['3-9'];q['question']=q['question'].replace('内半径は','内半径 $a$ は').replace('外半径は','外半径 $b$ は')
q=qs['3-14'];q['question']=r'高温側の流体1と低温側の流体2の間に平板がある。定常一次元、熱伝導率 $\lambda$ 一定、内部発熱なしで、全区間を同じ非零熱流束が通る。熱伝達率は流体1側が $h_1$、流体2側が $h_2$ で、$h_1=4h_2$ である。候補図の流体区間の横幅は模式表示で、実際の境界層厚さではない。適切な温度分布はどれか。'
q=qs['3-15'];q['question']=r'円筒壁の内半径を $a$、外半径を $b=1.5a$ とする。内側の高温流体1の熱伝達率を $h_1$、外側の低温流体2の熱伝達率を $h_2=h_1/6$ とする。端部の影響を無視し、発熱なし、$\lambda$ 一定の半径方向定常熱伝導である。内側流体と内表面の温度差を $\Delta T_1$、外表面と外側流体の温度差を $\Delta T_2$ とすると、比と壁内温度曲線の説明として適切なのはどれか。'
q['choices']=[c.replace(r'\Delta T_\text{out}',r'\Delta T_2').replace(r'\Delta T_\text{in}',r'\Delta T_1') for c in q['choices']]
ex={
'3-2':r'''【基礎】構造解析と熱伝導解析には、式の中で同じ役割を持つ量があります。「求める量→位置で微分した量→材料の式から得る量→外からの入力」の順に比べます。
【考え方】構造では、変位→軸ひずみ→軸応力→外力です。熱伝導では、温度→温度勾配→熱流束→熱の供給源になります。温度を位置で微分すると温度勾配、それにフーリエ則を使うと熱流束が得られます。この並びを示す正解は4です。
【ポイント】比較するのは式の役割であり、物理単位まで同じではありません。構造の材料係数Eに対応するのは熱伝導率λですが、どちらも本問の四つの量の並びには入りません。
【引っかけ】(1)は熱流束を最初に求める量とし、材料係数を入力源に置いています。(2)は温度を微分した結果を熱伝導率としています。(3)は温度と発熱源の役割を逆にし、熱流束と温度勾配の順も逆です。''',
'3-5':r'''【基礎】発熱なしの定常状態では、断面積が共通の両層を同じ熱流束が通ります。接触熱抵抗のない界面では、温度が途切れずにつながります。
【考え方】フーリエ則から、温度の傾きの大きさは $|dT/dx|=|q|/\lambda$ です。Aでは熱伝導率が3λなので傾きは $|q|/(3\lambda)$、Bでは $|q|/\lambda$。Bの傾きはAの3倍になります。温度が連続で、B側が3倍急な候補IIIが適切です。選択肢では4なので、正解は4です。
【ポイント】傾きは「距離当たりの温度変化」、温度降下は「傾き×厚さ」です。Aは厚さ2dなので温度降下は $|q|\,2d/(3\lambda)$、Bは $|q|\,d/\lambda$。比は2:3です。Aは厚くても熱を通しやすいため、Bより傾きが緩やかです。
【引っかけ】(1)のIIはAの方を急にしており逆です。(2)のIは両層の傾きが同じで、熱伝導率が違うのに同じ熱流束を通せません。(3)のIVは界面で温度が飛び、完全密着・接触熱抵抗なしの条件に反します。''',
'3-7':r'''【基礎】体積発熱率Hは、単位体積で毎秒生まれる熱の量で、単位はW/m³です。発熱した熱を両面へ逃がすため、内部は表面より高温になります。一定H・一定λの一次元定常式は $\lambda\,d^2T/dx^2+H=0$ です。
【考え方】式を整理すると $d^2T/dx^2=-H/\lambda$ で、温度を二回微分した結果が一定です。一回積分すると $dT/dx=-(H/\lambda)x+C_1$、もう一回積分すると $T=-H x^2/(2\lambda)+C_1x+C_2$ になります。C₁とC₂は両面の温度から決める定数です。x²の項を持つ二次関数なので、正解は2です。
【ポイント】「二回微分で一定→二回積分で二次関数」とたどります。H>0でx²の係数が負なので山形です。両面が同じ温度でも、発熱する内部まで同温ではありません。左右対称なので中央が最も高温で、熱は左右の表面へ流れます。
【引っかけ】(1)の一次関数は二階微分が0で、正の発熱を表せません。(3)の三次関数、(4)の正弦関数は、二階微分が一定になりません。''',
'3-8':r'''【基礎】左から入る熱に、壁の内部で生まれる熱が加わります。位置xまでに厚さxの部分が発熱するため、熱流束は $q(x)=q_0+Hx$ です。HはW/m³、xはmなので、Hxは流束と同じW/m²になります。
【考え方】第一に、熱はどこでも右へ流れるので温度は右へ下がります。第二に、右へ進むほど発熱分が加わり、運ぶ熱が増えます。フーリエ則の $dT/dx=-q/\lambda$ より、同じλでqが増えると温度の下がり方が急になります。「右へ下がる」「右ほど急」の両方に合う候補Cが適切で、正解は4です。
【ポイント】曲線全体の式を求めなくても、熱の向きと発熱による増加で判断できます。式で確認すると $d^2T/dx^2=-H/\lambda<0$。これは、右へ進むほど傾きがより負になり、下降が急になることを意味します。
【引っかけ】(1)のBは左側で温度が上がり、そこで熱が左へ流れてしまいます。(2)のAは直線で、右へ進むほど発熱分が加わることを表せません。(3)のDは右ほど下がり方が緩くなり、熱流束が増える条件と逆です。''',
'3-9':r'''【基礎】円筒の内半径をa、外半径をbとすると、外表面の熱流束は $q_b=\lambda(T_1-T_2)/[b\ln(b/a)]$ です。T₁は内面温度、T₂は外面温度。lnは自然対数で、本問ではその値0.4055が与えられています。円筒の面積が外側ほど増えることを含んだ式です。
【考え方】温度差は110−20=90K、半径比b/aは0.12/0.08=1.5です。式へ代入して、$q_b=0.04\times90/(0.12\times0.4055)\approx74.0\,\mathrm{W/m^2}$。次に管長1mの外面積は $2\pi\times0.12\times1\approx0.754\,\mathrm{m^2}$ なので、流出する熱は $74.0\times0.754\approx55.8\,\mathrm W$。つまり管長当たり約56W/mの報告も整合します。正解は3です。
【ポイント】熱流束qは面積当たりのW/m²、熱流量Qは全体のWです。面積Aで流束が一様なら $Q=qA$。外面の計算には外半径bを使います。内外で同じなのは熱流量で、面積当たりの熱流束ではありません。
【引っかけ】(1)は管長当たりの56を、面積当たりの値へそのまま使っています。(2)は内外面積が違うため熱流量も保存されないとしていますが、発熱なしの定常状態では保存されます。(4)の約111は、外面でなく内面の面積で換算した流束です。''',
'3-10':r'''【基礎】熱通過率Kは、壁を挟む二つの流体の温度差と熱流束を $q=K(T_h-T_c)$ で結ぶ係数です。単位はW/(m²K)。Kが大きいほど、同じ温度差で多くの熱が通ります。hₕは高温側、h꜀は低温側の熱伝達率、tは板厚、λは壁の熱伝導率です。
【考え方】熱は「高温流体→壁→低温流体」の順に通ります。高温側の温度差はq/hₕ、壁内はqt/λ、低温側はq/h꜀です。この三つを足すと両流体の温度差になるので、$T_h-T_c=q(1/h_h+t/\lambda+1/h_c)$。qについて整理し、$q=K(T_h-T_c)$ と比べると、$K=1/(1/h_h+t/\lambda+1/h_c)$。正解は1です。
【ポイント】分母の三項は、それぞれの区間の熱の通りにくさです。順番に通るため三項を足し、最後に逆数を取ります。1/Kの単位はm²K/Wで、面積当たりの熱抵抗に相当します。面積A全体の熱抵抗Rとは $R=1/(KA)$ の関係です。詳しい区別は関連用語で確認できます。
【引っかけ】(2)は1/KをKとしており、逆数が抜けています。(3)は各区間の通しやすさを直接足していますが、今回は直列です。(4)はhやλ/tを足した値の逆数で、単位もm²K/WとなりKと合いません。''',
'3-11':r'''【基礎】熱通過率は $K=1/(1/h_h+t/\lambda+1/h_c)$ です。流体温度差が同じなら、Kが大きい案ほど熱流束も大きくなります。そこで分母1/Kが最も小さい案を選びます。三項は面積当たりの熱抵抗に相当し、単位はm²K/Wです。
【考え方】案A：hₕが1.25倍なので、1/hₕは0.20/1.25=0.16となり、1/K=0.16+0.04+0.01=0.21。案B：板厚が0.75倍なので、1/K=0.20+0.04×0.75+0.01=0.24。案C：h꜀が1.25倍なので、1/K=0.20+0.04+0.01/1.25=0.248です。逆数を取るとKは順に約4.76、4.17、4.03W/(m²K)。最大は案Aなので、正解は2です。
【ポイント】hが25%増えると、1/hは25%減ではなく1/1.25=0.8倍になります。変更した項だけ計算し直してください。元々大きい高温側の項0.20を減らす案Aが、全体に最も効きます。Kと抵抗は逆数の関係なので、「Kを大きくする」と「1/Kを小さくする」は同じ判断です。
【引っかけ】(1)の案Cでは1/Kは0.248で、0.20にはなりません。(3)の0.20は、高温側の項を誤って25%減の0.15にして得る値です。(4)の約0.19は全体の0.25を25%減らした値に近く、壁の項だけを減らす案Bとは違います。''',
'3-12':r'''【基礎】二層壁では、熱通過率は $K=1/(1/h_1+d_1/\lambda_1+d_2/\lambda_2+1/h_2)$ です。h₁・h₂は流体と表面の熱伝達率、d₁・d₂は各層の厚さ、λ₁・λ₂は熱伝導率です。四つの区間を同じ熱流束が順番に通ります。
【考え方】分母の四項は1/20=0.05、0.04/0.4=0.10、0.08/0.8=0.10、1/5=0.20で、単位はm²K/Wです。合計は0.45、Kは1/0.45≈2.22W/(m²K)。流体温度差160−20=140Kから、$q=K\times140=140/0.45\approx311.1\,\mathrm{W/m^2}$ です。低温側表面温度をTₛとすると、$q=h_2(T_s-20)$。よって $T_s=20+q/h_2=20+311.1/5\approx82.2\,\mathrm{^\circ C}$。正解は2です。
【ポイント】Kには両流体間の全区間が含まれます。一方、表面温度を求めるときは、その表面と流体の間のhを使います。熱を外へ出すには表面が低温側流体より高温なので、20℃にq/h₂を足します。82.2℃が20℃と160℃の間にあることも確認します。
【引っかけ】(1)の表面20℃では低温側の温度差が0となり、熱を出せません。(3)は壁の0.10を一つ落とすと得る400W/m²・100℃です。(4)は低温側の1/h₂=0.20を落とすとq=560になります。その後の表面温度計算だけにh₂を使って132℃を出しても、全体の熱収支と合いません。''',
'3-14':r'''【基礎】流体温度と壁表面温度の差は、熱伝達式 $q=h\Delta T$ より $\Delta T=q/h$ です。同じqなら、hが大きい側ほど小さな温度差で熱を通せます。発熱なし・一定λの平板内では、温度は直線的に変わります。
【考え方】流体1側はh₁、流体2側はh₂で、h₁=4h₂です。したがって $\Delta T_1=q/(4h_2)$、$\Delta T_2=q/h_2$ となり、流体2側の温度差が1側の4倍です。壁内が直線で、右側の温度差が4倍になっている候補IVが適切です。正解は1です。
【ポイント】hが大きいとは、表面と流体の間で熱が移りやすいことです。だから同じ熱を小さな温度差で通せます。流体区間の横幅は模式表示なので、そこでの線の傾きでなく、流体と表面の縦の温度差を比較します。
【引っかけ】(2)のIIは左右の温度差が同じで、hの比と合いません。(3)のIIIは対流温度差が0で、有限hでは熱を通せません。(4)のIは左の温度差が大きく、大小が逆です。''',
'3-15':r'''【基礎】円筒では、内表面の面積は $A_1=2\pi aL$、外表面は $A_2=2\pi bL$ です。Lは管長。対流式 $Q=hA\Delta T$ より温度差は $\Delta T=Q/(hA)$ なので、hと面積の両方で決まります。発熱なしの定常状態では、内外の熱流量Qは同じです。
【考え方】b=1.5aなのでA₂=1.5A₁、h₂=h₁/6です。二つの温度差の比を取ると、同じQが消えて $\Delta T_2/\Delta T_1=(h_1A_1)/(h_2A_2)=6/1.5=4$ になります。つまり外側の温度差は内側の4倍です。さらに壁内も外側ほど熱が通る面積が増え、面積当たりの熱流束が小さくなります。同じλなら温度の下がり方も緩やかになるため、正解は1です。
【ポイント】まず温度差の比、次に壁内の曲線を別々に判断します。外側のhが1/6でも面積が1.5倍あるので、温度差は6倍ではなく4倍です。平板では面積が共通ですが、円筒では面積比を必ず含めます。
【引っかけ】(2)は温度差の比が逆で、壁内の勾配変化も逆です。(3)の6倍は面積比を忘れた値で、壁内を直線とするのも誤りです。(4)の壁が同温では温度勾配が0となり、高温流体から低温流体へ熱を通せません。''',
}
for n,e in ex.items():qs[n]['explanation']=e
# Existing app links resolve by exact item.id; replace obsolete IDs as well.
links={
1:['fourier-law'],2:['elastic-thermal-analogy'],3:['thermal-diffusivity'],4:['steady-temp-profiles','cylinder-conduction'],
5:['steady-temp-profiles','thermal-resistance','heat-transfer-rate-resistance'],6:['heat-boundary-conditions','fourier-law'],
7:['steady-heat-equation'],8:['steady-heat-equation','fourier-law'],9:['cylinder-conduction','heat-transfer-rate-resistance'],
10:['overall-heat-transfer','heat-transfer-rate-resistance'],11:['overall-heat-transfer','rate-limiting-resistance','heat-transfer-rate-resistance'],
12:['overall-heat-transfer','newton-cooling','heat-transfer-rate-resistance'],13:['lambda-vs-h'],14:['newton-cooling','heat-transfer-rate-resistance'],
15:['cylinder-conduction','newton-cooling','heat-transfer-rate-resistance'],16:['heat-boundary-conditions'],17:['heat-boundary-conditions','newton-cooling']}
for q in data['questions']:q['relatedFormulas']=links[int(q['number'].split('-')[1])]
byid={i['id']:i for i in terms['items']}
relation={'id':'heat-transfer-rate-resistance','kind':'term','term':'熱通過率Kと熱抵抗Rの関係',
'formula':r'$R=1/(KA)$',
'body':r'同じ伝熱経路を、面積当たりで見るか、面積A全体で見るかを分けます。①面積当たり：熱流束qの単位はW/m²で、熱通過率Kを使い $q=K\Delta T$ と表します。Kの単位はW/(m²K)、逆数1/Kは面積当たりの熱抵抗で、単位はm²K/Wです。②面積全体：熱流量Qの単位はWで、$Q=qA=KA\Delta T$。熱抵抗Rを使うと $Q=\Delta T/R$ なので、両式を比べて $R=1/(KA)$ となります。Rの単位はK/Wです。したがって、KをそのままRの逆数とするのではなく、面積Aも含めて換算します。同じ面積なら、Kが大きいほどRは小さく、同じ温度差で熱が多く通ります。平板の三区間では $1/K=1/h_h+t/\lambda+1/h_c$、$R=1/(Ah_h)+t/(A\lambda)+1/(Ah_c)$。前者は面積当たり、後者は面積全体の抵抗です。定常・発熱なし・共通面積の条件で使います。',
'example':r'$K=4\,\mathrm{W/(m^2K)}$、$A=2\,\mathrm{m^2}$、$\Delta T=50\,\mathrm K$ の場合、① $q=4\times50=200\,\mathrm{W/m^2}$。② $Q=200\times2=400\,\mathrm W$。③ $1/K=0.25\,\mathrm{m^2K/W}$、$R=1/(4\times2)=0.125\,\mathrm{K/W}$。④抵抗で検算しても $Q=50/0.125=400\,\mathrm W$ です。面積1m²ならRと1/Kの数値は同じですが、単位は異なります。',
'figureImage':'solid2Ch3RateResistanceTerm'}
if relation['id'] in byid:byid[relation['id']].update(relation)
else:terms['items'].insert(terms['items'].index(byid['overall-heat-transfer'])+1,relation)
it=byid['overall-heat-transfer'];it['formula']=r'$K=1/(1/h_h+t/\lambda+1/h_c)$'
it['body']=r'熱通過率Kは、高温流体から壁を通って低温流体へ移る熱流束を、$q=K(T_h-T_c)$ で表す係数です。hₕ・h꜀は両側の熱伝達率、tは板厚、λは壁の熱伝導率。高温側の温度差はq/hₕ、壁内はqt/λ、低温側はq/h꜀なので、三つを足すと $T_h-T_c=q(1/h_h+t/\lambda+1/h_c)$。この式をqについて整理すると、表示したKの式になります。Kが大きいほど、同じ流体温度差で多くの熱が通ります。Kの単位はW/(m²K)、1/Kは面積当たりの熱抵抗で単位はm²K/Wです。面積A全体の熱抵抗Rとは $R=1/(KA)$ の関係があります。多層平板ならt/λを各層の厚さ/熱伝導率の和に置き換えます。定常・発熱なし・共通面積の平板で使う式です。'
it['example']=r'$h_h=10$、$h_c=20\,\mathrm{W/(m^2K)}$、$t=0.10\,\mathrm m$、$\lambda=1\,\mathrm{W/(mK)}$ なら、$1/K=0.10+0.10+0.05=0.25\,\mathrm{m^2K/W}$。よって $K=4\,\mathrm{W/(m^2K)}$。流体温度差50Kなら $q=4\times50=200\,\mathrm{W/m^2}$ です。'
it['figureImage']='solid2Ch3Review10After'
it=byid['rate-limiting-resistance'];it['formula']=r'$1/K=1/h_h+t/\lambda+1/h_c$'
it['body']=r'同じ流体温度差なら、熱通過率Kが大きいほど熱流束は大きくなります。Kの分母を小さくするには、三項のうち大きな項を減らすことが有効です。それぞれの項は面積当たりの熱抵抗に相当します。比較はhとλそのものではなく、1/hとt/λへそろえて行います。hを25%増やすと1/hは1/1.25=0.8倍になり、25%減ではありません。板厚を25%減らすとt/λは0.75倍です。変更する項だけ計算し直し、分母の和を比較します。最大の項があるからといって、ほかを無条件に省いてよいわけではありません。'
it['example']=r'初期の三項が0.20、0.04、0.01m²K/Wなら、1/K=0.25、K=4W/(m²K)。高温側hを25%増やすと、1/K=0.16+0.04+0.01=0.21、K≈4.76W/(m²K)。壁だけを25%薄くすると1/K=0.24、K≈4.17W/(m²K)です。'
it['figureImage']='solid2Ch3Review11After'
for it in terms['items']:
    for key in ('formula','body','example'):
        if key in it:it[key]=it[key].replace('\\\\','\\').replace('hₕ','$h_h$').replace('h꜀','$h_c$')
for q in data['questions']:q['explanation']=q['explanation'].replace('hₕ','$h_h$').replace('h꜀','$h_c$')
ids={i['id'] for i in terms['items']};assert len(ids)==len(terms['items'])
old=json.loads(qraw)
for a,q in zip(old['questions'],data['questions']):
    assert (a['id'],a['answer'],a['officialRef'])==(q['id'],q['answer'],q['officialRef'])
    lines=q['explanation'].splitlines();assert len(lines)==4
    assert all(line.startswith(tag) for line,tag in zip(lines,('【基礎】','【考え方】','【ポイント】','【引っかけ】')))
    assert all(f'({i})' in lines[-1] for i in range(1,5) if i!=q['answer'])
    assert all(i in ids for i in q['relatedFormulas'])
assert qs['3-1']['explanation']==old['questions'][0]['explanation']
assert QP.read_bytes()==qraw and FP.read_bytes()==fraw,'Concurrent edit detected'
QP.write_bytes(enc(data));FP.write_bytes(enc(terms));(OUT/'第3章_完成問題.json').write_bytes(enc(data))
(OUT/'第3章_完成用語.json').write_bytes(enc(terms))
print('Chapter 3 aligned: K in 3-10/11/12; H in generation; term added; all 17 related links resolve; answers unchanged.')
