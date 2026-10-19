# 固体2級 第2章「固体力学の基礎」公式・用語 刷新 — ChatGPT入力パック

あなたはCAE(計算力学技術者)試験アプリの教材編集者です。下の「現行データ(改修前)」を土台に、
**この章の公式・用語リストを"最重要だけ"に選び直し**てください。ゼロから創作せず、改修前を踏まえて取捨・加筆します。

## 編集方針(必守)
1. **最重要だけ残す**：第2章=固体力学の基礎 の大局テーマ(応力・ひずみ・弾性係数・主応力/モール円・降伏条件 等)に直結する項目だけ。
   枝葉・細則・重複・マニアックな派生は**削る**。目安 **8〜15項目**(現行25→厳選)。
2. **term/formula はシンプルに**：1項目=1概念/1公式。式(formula)は要点1本に絞る。
3. **body は厚く**：「何か・なぜ重要か・いつ使うか・物理的な意味・つまずきやすい点」を
   **中学生でも分かる言葉で300〜500字**。難しい用語は必ずかみ砕く。
4. **example は具体的に**：身近な数値・例え(鋼はE≈2.1×10⁵MPa 等)。
5. **figureImage は「現行データ(改修前)」の値をそのまま引き継ぐ**：残す項目には、下の現行データで**同じ項目(用語・公式が対応する項目)に付いている `figureImage` の値をそのままコピー**する。
   - 画像の中身を目で確認する必要は**ない**(既存の対応が正しい前提で、そのまま使う)。
   - **勝手に空(`""`)にしない**。言い換え・統合をしても、元になった項目の `figureImage` を引き継ぐ。
   - `""`(空)にしてよいのは、**改修前に存在しない完全新規の項目で、対応する既存図が無い場合だけ**。新しい図キーは作らない。
6. 数式は **KaTeXの$...$**。バックスラッシュは正しく1個(例: `\dfrac`, `\nu`, `\sigma`)。JSONとして**二重に重ねたバックスラッシュ(`\\dfrac` のような過剰エスケープ)や、改行のつもりの `\n` を文字列に混ぜるのは禁止**。改行したいときは項目を分けるか句点で区切る。

## 原本(最重要)マップ — ここから「最重要」を選ぶ基準
固体2級 第2章=公式標準問題 **全44問**。番号は公式問。**1〜11は最重要=落とさない。12と材料試験(2-43)は1問のみ＝任意。**

1. 材料定数・弾性係数(2-1〜2-3)：E・G・ν、$G=E/2(1+\nu)$
2. 応力-ひずみ曲線・材料試験(2-4,2-5,2-43)：公称/真、降伏点・引張強さ・一様/破断伸び、0.2%耐力、シャルピー/ビッカース/クリープ
3. ひずみ-変位・応力座標変換・主応力・モール円(2-6,2-7,2-16〜2-19)
4. 棒の伸び・組合せ棒・トラス(2-8〜2-12,2-27)
5. せん断応力・ねじり(2-13〜2-16)
6. **★はりの曲げ(2-20〜2-26,2-28,2-29＝9問・最多出題)**：反力・曲げモーメント図／たわみとEI／断面二次モーメント $I=\int z^2\,dA$／断面係数 $Z=I/c$ と $\sigma_{\max}=M/Z$／FBD
7. 薄肉円筒(2-30)：$\sigma_\theta=pd/2t,\ \sigma_a=pd/4t$
8. 降伏条件・破損則(2-31〜2-34)：ミーゼス/トレスカ/最大主応力説/八面体/脆性・延性
9. 疲労(2-35〜2-38)：S-N曲線・疲労限度・平均応力・疲労限推定
10. 応力集中(2-39)：応力集中係数 $K_t$
11. 熱応力(2-40〜2-42)
12. 応力波(2-44)：$C=\sqrt{E/\rho}$

### ★補強指示(必須)
現行データは「はり」が *たわみとEI* の1項目だけだが、はりは**9問＝最多出題**。次を項目として足す(統合でも可)：
**断面二次モーメント** $I=\int z^2 dA$、**断面係数** $Z=I/c$・$\sigma_{\max}=M/Z$、**反力と曲げモーメント図**。
→ 図は下の候補 `s2IsectionInertia`／`s2SectionZ`／`s2BMD`／`s2OverhangBeam` を**流用**(新規作図不要)。

## 図の扱い(②図の流用／新規作図の規約)
- 各項目の `figureImage` は、下の「**流用できる図キー**(この章で実在)」から**内容が合うものを選んで**入れる。問題で使われている図をそのまま流用し、**新しい画像・新しいキー名は作らない**。
- 合う図が無い項目は `figureImage:""` にし、代わりに **`figureNeed`** に「どんな図が要るか(1行)」を書く。存在しないキー名を書くと実装時にエラーになる。
- 既存項目を言い換え・統合した場合も、元項目の図キーを引き継ぐ。

## 出力フォーマット(これだけを返す。前後の説明文は不要)
アプリ直系スキーマのJSON1つ。キーは現行と同じ:
```json
{
  "chapter": 2,
  "title": "固体力学の基礎",
  "intro": "(章の導入。1〜2文)",
  "items": [
    {
      "id": "kebab-case-id",
      "kind": "formula",            // "formula"(公式) または "term"(用語)
      "term": "用語名(日本語・記号つき可)",
      "formula": "$...$",           // kind=term で式が無ければ "" 可
      "body": "厚い解説(300〜500字・中学生レベル)",
      "example": "具体例",
      "figureImage": "s2PoissonRod", // 「流用できる図キー」から内容が合う1つ。合う図が無い時だけ ""
      "figureNeed": ""               // figureImage="" の時だけ、どんな図が要るかを1行で。図があるなら省略/""
    }
  ]
}
```

## 流用できる図キー(この章で実在・内容メモ)
以下から選ぶ。合うものが無ければ `figureImage:""`＋`figureNeed`。

- `s2ShearModulus` … せん断弾性係数Gの定義(せん断応力τ–せん断ひずみγ)
- `s2PoissonRod` … 丸棒の軸引張とポアソン比(縦伸び・横縮み)
- `s2PoissonBar` … 非圧縮(ν→0.5)で体積ほぼ不変の説明
- `s2StressStrainCurve` … 公称応力–ひずみ線図(降伏点・引張強さ・一様伸び・破断伸び)
- `s2OffsetYield` … 0.2%オフセット耐力の作図(弾性勾配に平行な直線と交点)
- `stresstransform` … 応力の座標変換(x-y → 回転した x'-y')
- `s2StrainDisp` … ひずみ–変位(変位場 u,v,w から各ひずみ)
- `s2MohrCompare` … 各単純荷重状態とモールの応力円の対応
- `s2PrincipalMohr` … 平面応力の主応力とモール円
- `s2Mohr3DShear` … 3次元純せん断の状態
- `squarebar` … 正方形断面棒の軸引張(単位換算・E算出)
- `fixedbar2mat` … 両端固定の段付き2材棒(不静定・適合条件)
- `taperbar` … 楔形(テーパ)棒の伸び(対数)
- `s2RigidBarWire` … 剛棒＋ワイヤ(傾いた支持)
- `s2RigidPlate2Bars` … 剛板を支える並列2本の弾性棒
- `s2Truss2Bar` … 2部材トラス(30°/60°)と節点法
- `s2ConjugateShear` … 共役せん断応力(直角面に等大のτ)
- `s2PureShear` … 一様せん断の境界条件
- `s2HollowShaft` … 中空丸軸のねじり(Tmax・極断面二次モーメントIp)
- `s2TorsionPrincipal` … ねじり表面の45°主応力方向
- `s2OverhangBeam` … 張り出しはりの反力
- `s2BMD` … 曲げモーメント図(最大曲げモーメント)
- `s2CantileverUDL` … 片持ちはり＋等分布荷重
- `s2CantMoment` … 片持ちはり自由端＋集中モーメント
- `s2BeamDeflEI` … 単純支持はり中央集中荷重のたわみ(曲げ剛性EI)
- `s2SectionZ` … 断面係数Zの形状比較(正方形/円/三角/ひし形)
- `s2IsectionInertia` … I型断面の断面二次モーメントI
- `s2FBD` … フリーボディダイアグラム(部材を切り出して反力分解)
- `s2CantReactions` … 片持ちはりの反力・固定端モーメント
- `s2ThinCylinder` … 薄肉円筒の円周方向/軸方向応力(σθ=pd/2t)
- `s2YieldSurface` … 平面応力の降伏曲線(最大主応力説/トレスカ/ミーゼス比較)
- `s2MisesJudge` … ミーゼス相当応力による降伏判定
- `s2Octahedral` … 八面体せん断応力
- `s2BrittleDuctile` … 脆性材料と延性材料の破損評価の使い分け
- `s2FatigueSurface` … 疲労破壊(表面起点/内部欠陥起点)
- `s2GoodmanDiagram` … 平均応力と疲労(S-N群・グッドマン線図)
- `s2SNCurve` … S-N曲線と疲労限度
- `s2NotchStress` … 切欠き・応力集中と疲労(応力集中係数Kt)
- `s2PlateHoles` … 2円孔板の応力集中(公称応力と最大応力)
- `s2ThermalContrast` … 拘束の有無と熱応力の発生
- `s2HalfHeatedBar` … 一部だけ加熱された両端固定棒の熱応力
- `s2TwoBarsThermal` … 並列2棒(片方昇温)の熱応力
- `s2MaterialTests` … 材料試験(シャルピー=じん性/ビッカース=硬さ/クリープ=高温)
- `s2StressWave` … 応力波の伝ぱ速度 C=√(E/ρ)

## 現行データ(改修前・これを土台に選び直す)
```json
{
  "chapter": 2,
  "title": "第2章 固体力学の基礎",
  "intro": "公式標準問題集の第2章（固体力学の基礎）で問われる公式・用語を、試験と同じ記号・形でまとめています。材料定数（E・G・ν）／応力-ひずみ線図・材料試験／ひずみ-変位・応力座標変換・主応力・モール円／棒の伸び・トラス／せん断とねじり／はりの曲げ（反力・BMD・たわみ・断面係数）／薄肉円筒／降伏条件と破損則／疲労／応力集中／熱応力／応力波、が出題範囲です。",
  "items": [
    {
      "id": "material-constants",
      "kind": "formula",
      "term": "材料定数（縦弾性係数E・横弾性係数G・ポアソン比ν）",
      "formula": "$G=\\dfrac{E}{2(1+\\nu)}$",
      "body": "縦弾性係数 $E$（ヤング率）は単軸応力でのσとεの比、横弾性係数（せん断弾性係数）$G$ はせん断応力とせん断ひずみの比、ポアソン比 $\\nu$ は（荷重方向に直交する縮み）÷（荷重方向の伸び）です。等方性線形弾性体ではこの3つに $G=E/2(1+\\nu)$ の関係があります。$E,G$ の次元は応力と同じです。",
      "example": "炭素鋼は $E\\approx2.1\\times10^{5}\\,\\mathrm{MPa}$ 程度。降伏後に除荷しても、除荷の勾配はほぼ $E$ に一致します（公式問2-1）。",
      "figureImage": "s2PoissonRod"
    },
    {
      "id": "hookes-law",
      "kind": "formula",
      "term": "フックの法則（縦弾性）",
      "formula": "$\\sigma=E\\varepsilon$",
      "body": "弾性域では応力σとひずみεが比例し、その比例定数が縦弾性係数 $E$ です。棒の引張では $\\sigma=P/A$、$\\varepsilon=\\Delta L/L$ なので $E=\\dfrac{\\sigma}{\\varepsilon}=\\dfrac{P/A}{\\Delta L/L}$。",
      "example": "正方形断面（辺 $b$）の棒に $P$：$\\sigma=P/b^{2}\\ [\\mathrm{N/mm^2}=\\mathrm{MPa}]$、$E=\\dfrac{P}{b^{2}}\\dfrac{L}{\\Delta L}$（$1\\,\\mathrm{N/mm^2}=1\\,\\mathrm{MPa}$。公式問2-8）。",
      "figureImage": "s2PoissonBar"
    },
    {
      "id": "poisson-ratio",
      "kind": "formula",
      "term": "ポアソン比",
      "formula": "$\\nu=-\\dfrac{\\varepsilon'}{\\varepsilon}$　（$\\varepsilon'$=横ひずみ, $\\varepsilon$=縦ひずみ）",
      "body": "引張ると縦に伸び横に縮みます。横ひずみと縦ひずみの比の大きさがポアソン比 $\\nu$ です。$\\nu=0.5$ で体積変化0（非圧縮）。ゴムは $\\nu$ が0.5に非常に近く、金属は0.3前後です。",
      "example": "ひずみゲージで縦 $\\varepsilon$・横 $\\varepsilon'$ を測れば $\\nu=-\\varepsilon'/\\varepsilon$、$E=\\dfrac{P}{bt\\,\\varepsilon}$（公式問2-2・2-3）。",
      "figureImage": "s2PoissonRod"
    },
    {
      "id": "shear-modulus",
      "kind": "formula",
      "term": "せん断応力とせん断弾性係数・共役せん断応力",
      "formula": "$\\tau=G\\gamma,\\qquad \\tau_{xy}=\\tau_{yx}$",
      "body": "せん断応力τとせん断ひずみγは $\\tau=G\\gamma$ で比例します。ある面にせん断応力があれば、必ず直角な面に等しい大きさのせん断応力が対になって生じます（共役せん断応力、$\\tau_{xy}=\\tau_{yx}$）。力とモーメントの釣合いから導かれます。",
      "example": "微小正方形の各辺に働くせん断応力は、力の釣合いとモーメントの釣合いが同時に成り立つ向きの組だけが許されます（公式問2-13・2-14）。",
      "figureImage": "s2ConjugateShear"
    },
    {
      "id": "stress-strain-curve",
      "kind": "term",
      "term": "公称応力-ひずみ線図（降伏点・引張強さ・一様伸び・破断伸び）",
      "formula": "公称 $\\sigma=P/A_0$, 公称 $\\varepsilon=\\Delta L/L_0$／真応力 $=P/A$, 真ひずみ $=\\ln(1+\\varepsilon)$",
      "body": "公称応力・ひずみは初期断面積・初期標点距離で定義します。降伏点を超えると塑性変形が始まり、加工硬化を経て最大値＝引張強さに達し、くびれて荷重が下がり破断します。引張強さに対応する伸びが一様伸び、破断に対応する伸びが破断伸びです。",
      "example": "真応力は変形中の断面積、真ひずみは対数ひずみ $\\ln(1+\\varepsilon)$。弾性域のように変形が小さい領域では真応力・真ひずみ≒公称応力・公称ひずみ（公式問2-4）。",
      "figureImage": "s2StressStrainCurve"
    },
    {
      "id": "offset-yield",
      "kind": "term",
      "term": "0.2%耐力（オフセット耐力）",
      "formula": "弾性勾配に平行な0.2%オフセット線と曲線の交点＝耐力",
      "body": "アルミ合金・銅合金などは明確な降伏点を示しません。そこで一定の永久ひずみ（通常0.2%）を生じる応力を降伏点の代わりに使い、これを0.2%耐力と呼びます。",
      "example": "ひずみ軸上の0.2%の点から弾性勾配 $E$ に平行な直線を引き、応力-ひずみ曲線との交点が耐力です（公式問2-5）。",
      "figureImage": "s2OffsetYield"
    },
    {
      "id": "strain-displacement",
      "kind": "formula",
      "term": "ひずみと変位の関係（微小ひずみ）",
      "formula": "$$\\begin{aligned}& \\varepsilon_x =\\partial u/\\partial x \\\\ & \\varepsilon_y =\\partial v/\\partial y \\\\ & \\varepsilon_z =\\partial w/\\partial z \\\\ & \\gamma_{xy} =\\partial u/\\partial y+\\partial v/\\partial x \\\\ & \\gamma_{yz} =\\partial v/\\partial z+\\partial w/\\partial y \\\\ & \\gamma_{zx} =\\partial w/\\partial x+\\partial u/\\partial z\\end{aligned}$$",
      "body": "変位 $u,v,w$ を微分すると各方向の垂直ひずみ、斜め方向の組合せでせん断ひずみが得られます。$\\gamma_{yz}=\\partial v/\\partial z+\\partial w/\\partial y$、$\\gamma_{zx}=\\partial w/\\partial x+\\partial u/\\partial z$ も同様です。",
      "example": "変位が1次式なら各ひずみは定数になります（公式問2-7）。",
      "figureImage": "s2StrainDisp"
    },
    {
      "id": "stress-transformation",
      "kind": "formula",
      "term": "応力の座標変換(x-y を反時計回りに回した x'-y')",
      "formula": "$$\\begin{aligned}& \\sigma_{x'} =\\tfrac{\\sigma_x+\\sigma_y}{2}+\\tfrac{\\sigma_x-\\sigma_y}{2}\\cos2\\theta+\\tau_{xy}\\sin2\\theta \\\\ & \\sigma_{y'} =\\tfrac{\\sigma_x+\\sigma_y}{2}-\\tfrac{\\sigma_x-\\sigma_y}{2}\\cos2\\theta-\\tau_{xy}\\sin2\\theta \\\\ & \\tau_{x'y'} =-\\tfrac{\\sigma_x-\\sigma_y}{2}\\sin2\\theta+\\tau_{xy}\\cos2\\theta\\end{aligned}$$",
      "body": "同じ場所にかかる同じ力でも、見る向き(座標軸)を変えると「まっすぐ押す力(垂直応力)」と「ずらす力(せん断応力)」への分け方が変わります。もとの $x,y$ 軸を反時計回りに角度 $\\theta$ だけ回した軸を $x',y'$ とすると、新しい成分 $\\sigma_{x'},\\sigma_{y'},\\tau_{x'y'}$ は、もとの $\\sigma_x,\\sigma_y,\\tau_{xy}$ から上の式で計算できます。角度が $2\\theta$ の形で入るのが特徴で、応力は「向きを180°変えると元に戻る」性質があるためです。この式を図にしたのが次のモールの応力円です。",
      "example": "$\\theta=30^{\\circ}$ なら $\\cos2\\theta=\\cos60^{\\circ}=\\tfrac12,\\ \\sin2\\theta=\\sin60^{\\circ}=\\tfrac{\\sqrt3}{2}$ を代入するだけ(公式問2-6)。",
      "figureImage": "s2PrincipalMohr"
    },
    {
      "id": "principal-stress-mohr",
      "kind": "formula",
      "term": "主応力とモールの応力円",
      "formula": "$$\\begin{aligned}& \\sigma_{1,2} =\\frac{\\sigma_x+\\sigma_y}{2}\\pm\\sqrt{\\left(\\frac{\\sigma_x-\\sigma_y}{2}\\right)^{2}+\\tau_{xy}^{2}} \\\\ & \\tan2\\omega =\\frac{2\\tau_{xy}}{\\sigma_x-\\sigma_y}\\end{aligned}$$",
      "body": "向き(軸)を回していくと、せん断応力がちょうど0になる特別な向きが見つかります。そのときの垂直応力が、その点で一番大きい値と一番小さい値になり、これを主応力 $\\sigma_1,\\sigma_2$ と呼びます($\\sigma_1\\geq\\sigma_2$)。上の式の $\\pm$ の大きい方が $\\sigma_1$、小さい方が $\\sigma_2$、$\\tan2\\omega$ の式でその向き(主軸)が分かります。これを1つの円で表したのがモールの応力円で、中心 $\\left(\\tfrac{\\sigma_x+\\sigma_y}{2},\\,0\\right)$・半径 $R=\\sqrt{\\left(\\tfrac{\\sigma_x-\\sigma_y}{2}\\right)^{2}+\\tau_{xy}^{2}}$ の円。円の右端・左端が主応力、上端・下端が最大せん断応力に対応します。",
      "example": "丸棒のねじりは純せん断（$\\sigma_x=\\sigma_y=0$）で、モール円の中心は原点・半径 $\\tau_{xy}$、主応力方向は軸から45°（公式問2-16〜2-19）。",
      "figureImage": "s2MohrCompare"
    },
    {
      "id": "max-shear-stress",
      "kind": "formula",
      "term": "主せん断応力(最大せん断応力)",
      "formula": "$$\\begin{aligned}& \\tau_{\\max} =\\frac{\\sigma_1-\\sigma_2}{2}=\\sqrt{\\left(\\frac{\\sigma_x-\\sigma_y}{2}\\right)^{2}+\\tau_{xy}^{2}} \\\\ & \\text{(3次元)}\\quad \\tau_{\\max} =\\frac{\\sigma_1-\\sigma_3}{2}\\end{aligned}$$",
      "body": "軸を回していくと、今度は「ずらす力(せん断応力)」が一番大きくなる向きがあります。その大きさが主せん断応力(最大せん断応力)です。平面の問題では、2つの主応力の差の半分、つまりモール円の半径 $R$ に等しく、主応力の向きからちょうど45°回った面に現れます。3次元では、一番大きい主応力 $\\sigma_1$ と一番小さい主応力 $\\sigma_3$ の差の半分 $\\tfrac{\\sigma_1-\\sigma_3}{2}$ が最大せん断応力です。金属が「ずれて」降伏・破壊するときの目安になります。",
      "example": "丸棒のねじり(純せん断)は $\\sigma_x=\\sigma_y=0$ なので $\\tau_{\\max}=\\tau_{xy}$、主応力は $\\pm\\tau_{xy}$ で軸から45°方向に現れます。",
      "figureImage": "s2MohrCompare"
    },
    {
      "id": "principal-stress-3d",
      "kind": "formula",
      "term": "3次元の主応力(応力の不変量)",
      "formula": "$\\sigma^{3}-I_1\\sigma^{2}+I_2\\sigma-I_3=0,\\quad I_1=\\sigma_x+\\sigma_y+\\sigma_z$",
      "body": "3次元では、ある1点の応力は6つの成分 $(\\sigma_x,\\sigma_y,\\sigma_z,\\tau_{xy},\\tau_{yz},\\tau_{zx})$ で表せます。ここでもせん断応力が全部0になる向きが3つあり、そのときの垂直応力が3つの主応力 $\\sigma_1\\geq\\sigma_2\\geq\\sigma_3$ です。これらは応力行列の固有値で、上の3次方程式の3つの解として求まります。係数 $I_1,I_2,I_3$ は軸の取り方を変えても値が変わらないので「応力の不変量」と呼び、$I_1$ は3つの垂直応力の和(=主応力の和)、$I_3$ は行列式です。",
      "example": "全方向から同じ圧力 $-p$ を受ける状態(静水圧)では $\\sigma_1=\\sigma_2=\\sigma_3=-p$ で、どの向きでもせん断応力は0。",
      "figureImage": null
    },
    {
      "id": "bar-elongation",
      "kind": "formula",
      "term": "棒の伸びと不静定（適合条件）",
      "formula": "$\\delta=\\dfrac{PL}{EA}$",
      "body": "軸力 $P$ を受ける棒の伸びは $\\delta=PL/(EA)$。断面や材料が途中で変わる棒は、各区間の伸びを足します。両端拘束など力の釣合いだけで解けない不静定問題では、変形の適合条件（つながり）を連立させます。",
      "example": "段付き棒・楔形棒・剛体＋ワイヤ・並列組合せ棒は、釣合い＋適合条件で解きます（例：並列2棒 $u=\\dfrac{L_1L_2\\,P}{E_1A_1L_2+E_2A_2L_1}$。公式問2-9〜2-12）。",
      "figureImage": "s2RigidPlate2Bars"
    },
    {
      "id": "truss-joint-method",
      "kind": "term",
      "term": "トラスと節点法",
      "formula": "各節点で $\\sum F_x=0,\\ \\sum F_y=0$（ピン結合＝モーメント不要）",
      "body": "トラスは部材がピンで結合され、各部材は軸力（引張・圧縮）だけを受けます。節点ごとに水平・鉛直の力の釣合いを立てて部材力を求めるのが節点法です。ピン結合なのでモーメントの釣合いは不要です。",
      "example": "天井から30°・60°でつるした2部材＋荷重 $P$：$x$ 方向 $\\tfrac12 S_2-\\tfrac{\\sqrt3}{2}S_1=0$、$y$ 方向 $\\tfrac{\\sqrt3}{2}S_2+\\tfrac12 S_1-P=0$（公式問2-27）。",
      "figureImage": "s2Truss2Bar"
    },
    {
      "id": "torsion-shaft",
      "kind": "formula",
      "term": "丸軸のねじり",
      "formula": "$$\\begin{aligned}& T =G I_p\\,\\theta, \\quad \\tau =G\\gamma=G r\\theta \\\\ & \\tau_{\\max} =G\\frac{D}{2}\\theta=\\frac{T\\,(D/2)}{I_p}, \\quad I_p =\\frac{\\pi}{32}(D^{4}-d^{4})\\end{aligned}$$",
      "body": "丸軸にトルク $T$ を加えると比ねじれ角 $\\theta$（単位長さあたりのねじれ角）が生じます。中心から半径 $r$ の点のせん断ひずみは $\\gamma=r\\theta$、フックの法則より $\\tau=G\\gamma=Gr\\theta$ なので、応力は中心で0・外周で最大です。外周 $r=D/2$ で $\\tau_{\\max}=G\\dfrac{D}{2}\\theta$。一方トルクは断面全体の積分から $T=G I_p\\theta$ になるので、$G\\theta=T/I_p$ を代入すると $G,\\theta$ が消えて $\\tau_{\\max}=\\dfrac{T(D/2)}{I_p}$ が得られます（$I_p$＝極断面二次モーメント、中空軸で $I_p=\\tfrac{\\pi}{32}(D^4-d^4)$）。",
      "example": "許容最大トルク $T_{\\max}=\\dfrac{2\\tau_{\\max}I_p}{D}=\\dfrac{\\pi}{16}\\tau_{\\max}\\dfrac{D^4-d^4}{D}$（公式問2-15）。",
      "figureImage": "s2HollowShaft"
    },
    {
      "id": "beam-deflection-EI",
      "kind": "formula",
      "term": "はりのたわみと曲げ剛性 EI",
      "formula": "たわみ $\\propto \\dfrac{1}{EI}$　（$EI$＝曲げ剛性）",
      "body": "はりのたわみは曲げ剛性 $EI$（縦弾性係数×断面二次モーメント）に反比例します。$E$ と $I$ を大きくすると、たわみは小さくなります。",
      "example": "$E$ と $I$ をそれぞれ2倍にすると $EI$ は4倍になり、中央たわみは $1/4$ になります（公式問2-24）。",
      "figureImage": "s2BeamDeflEI"
    },
    {
      "id": "thin-cylinder",
      "kind": "formula",
      "term": "薄肉円筒の応力",
      "formula": "$$\\begin{aligned}& \\sigma_\\theta =\\frac{pd}{2t} \\\\ & \\sigma_a =\\frac{pd}{4t}=\\frac{\\sigma_\\theta}{2}\\end{aligned}$$",
      "body": "内圧 $p$ を受ける薄肉円筒では、円周方向応力 $\\sigma_\\theta$ が軸方向応力 $\\sigma_a$ の2倍になります（$d$＝径、$t$＝板厚）。だから圧力容器は軸に沿った方向に割れやすいです。",
      "example": "ひずみ $\\varepsilon_\\theta=\\sigma_\\theta/E-\\nu\\sigma_a/E$ などから体積変化 $\\Delta V=\\dfrac{5-4\\nu}{2E}\\sigma_\\theta V$（公式問2-30）。",
      "figureImage": "s2ThinCylinder"
    },
    {
      "id": "yield-criteria",
      "kind": "term",
      "term": "降伏条件の3説(どの説で降伏を判定するか)",
      "formula": "①最大主応力説(脆性)　②トレスカ=最大せん断応力説(延性)　③ミーゼス=せん断ひずみエネルギー説(延性)",
      "body": "1方向だけの力なら「応力が降伏応力を超えたら降伏」で済みますが、いろいろな向きの力が同時にかかる(多軸)と、どうなったら降伏するかを決める「ものさし」が要ります。代表が次の3説です。①最大主応力説:一番大きい主応力が限界に達したら壊れる→もろい材料(鋳鉄・ガラス)向き。②最大せん断応力説(トレスカ):最大せん断応力が限界で降伏→延性金属、計算が簡単で安全側。③せん断ひずみエネルギー説(ミーゼス):形を変えるエネルギーで降伏→延性金属に最もよく合う。金属の実務ではミーゼスが基本です。次の2枚にそれぞれの式を示します。",
      "example": "全方向に同じ圧力(静水圧)だけでは、トレスカもミーゼスも降伏しないと判定します(形が変わらないため)。",
      "figureImage": "s2YieldSurface"
    },
    {
      "id": "tresca",
      "kind": "formula",
      "term": "トレスカの降伏条件(最大せん断応力説)",
      "formula": "$$\\sigma_1-\\sigma_3=\\sigma_Y\\quad\\Longleftrightarrow\\quad \\tau_{\\max}=\\dfrac{\\sigma_Y}{2}$$",
      "body": "「材料はずらす力(せん断)が限界を超えると降伏する」と考えるのがトレスカの説です。最大せん断応力 $\\tau_{\\max}=\\tfrac{\\sigma_1-\\sigma_3}{2}$ が、引張試験で降伏したときのせん断応力 $\\sigma_Y/2$ に達したら降伏とします。式にすると「一番大きい主応力 − 一番小さい主応力 = 降伏応力 $\\sigma_Y$」。計算が簡単で、ミーゼスより少し安全側(早めに降伏と判定)になります。",
      "example": "単軸引張は $\\sigma_1=\\sigma,\\ \\sigma_2=\\sigma_3=0$ なので $\\sigma=\\sigma_Y$ で降伏。純せん断は $\\sigma_1=\\tau,\\ \\sigma_3=-\\tau$ なので $2\\tau=\\sigma_Y$、$\\tau=\\sigma_Y/2$ で降伏。",
      "figureImage": "s2YieldSurface"
    },
    {
      "id": "von-mises",
      "kind": "formula",
      "term": "ミーゼスの降伏条件(せん断ひずみエネルギー説)と相当応力",
      "formula": "$$\\sigma_M=\\sqrt{\\dfrac{(\\sigma_1-\\sigma_2)^{2}+(\\sigma_2-\\sigma_3)^{2}+(\\sigma_3-\\sigma_1)^{2}}{2}}\\ \\leq\\ \\sigma_Y$$",
      "body": "延性のある金属が多軸の力で降伏するかを、最もよく当てる説です。「形を変えるエネルギー(せん断ひずみエネルギー)」が限界に達すると降伏する、という考えから、上の値(ミーゼス相当応力 $\\sigma_M$)を1つの代表値にまとめ、引張の降伏応力 $\\sigma_Y$ と比べます。$\\sigma_M\\geq\\sigma_Y$ で降伏。全方向に同じ圧力(静水圧)では $\\sigma_M=0$ になり、いくら圧力をかけても降伏しない(形が変わらない)ことをうまく表せます。FEMの応力評価で最もよく使われます。",
      "example": "単軸引張 $\\sigma_1=\\sigma$ では $\\sigma_M=\\sigma$。純せん断 $\\tau$ では $\\sigma_M=\\sqrt3\\,\\tau$ なので $\\tau=\\sigma_Y/\\sqrt3\\approx0.577\\,\\sigma_Y$ で降伏(トレスカの $0.5\\,\\sigma_Y$ より少し大きい)。",
      "figureImage": "s2YieldSurface"
    },
    {
      "id": "brittle-ductile",
      "kind": "term",
      "term": "脆性材料・延性材料の破損則",
      "formula": "脆性→最大主応力に注目／延性→ミーゼス相当応力に注目",
      "body": "鋳鉄・コンクリート・ガラスなどの脆性材料は、引張強さと等価な最大主応力で破壊を評価します。延性金属は弾性→降伏→塑性を経て破断し、多軸ではミーゼス相当応力（せん断ひずみエネルギー説）で降伏・破損を評価するのが一般的です。",
      "example": "弾性解析のミーゼス応力と降伏応力を比較して、延性材料の降伏判定・応力評価を行います（公式問2-34）。",
      "figureImage": "s2BrittleDuctile"
    },
    {
      "id": "stress-concentration",
      "kind": "term",
      "term": "応力集中",
      "formula": "$\\sigma_{\\max}=K_t\\,\\sigma_n$　（$K_t$＝応力集中係数）",
      "body": "穴・切欠き・段付きなど形状が急変する所では、公称応力 $\\sigma_n$ の $K_t$ 倍の応力が局所的に生じます（応力集中係数 $K_t$）。$K_t$ は形状比で決まり、設計で見落とすと破損の起点になります。",
      "example": "幅 $w$・板厚 $t$ の板の円孔（径 $d$）：公称 $\\sigma_n=P/(wt)$、最大 $\\sigma=K_t\\,P/((w-d)t)$（公式問2-39）。",
      "figureImage": "s2NotchStress"
    },
    {
      "id": "fatigue",
      "kind": "term",
      "term": "疲労（S-N曲線・疲労限度・平均応力）",
      "formula": "$$\\begin{aligned}& \\sigma_m =\\frac{\\sigma_{\\max}+\\sigma_{\\min}}{2}\\quad\\text{(平均応力)} \\\\ & \\sigma_a =\\frac{\\sigma_{\\max}-\\sigma_{\\min}}{2}\\quad\\text{(応力振幅)}\\end{aligned}$$",
      "body": "繰返し荷重では、静的強さよりはるかに低い応力でも破壊します（疲労）。応力振幅と破断繰返し数の関係がS-N曲線、これ以下なら壊れない応力振幅が疲労限度です。同じ応力振幅でも、引張の平均応力が大きいほど寿命が短くなります。",
      "example": "引張強さ≦1400MPaの鉄鋼では、疲労限は引張強さの0.4〜0.6倍程度と推定できます（公式問2-35〜2-38）。",
      "figureImage": "s2GoodmanDiagram"
    },
    {
      "id": "thermal-stress",
      "kind": "formula",
      "term": "熱ひずみと熱応力",
      "formula": "自由熱ひずみ $\\varepsilon_T=\\alpha\\Delta T$、完全拘束なら $\\sigma=-E\\alpha\\Delta T$",
      "body": "温度が $\\Delta T$ 変化すると材料は $\\alpha\\Delta T$ だけ伸び縮みします（$\\alpha$＝線膨張係数）。この変形が拘束されると熱応力が生じます。拘束がなくても、一部だけ温度が変わると周囲に拘束されて熱応力が出ます。",
      "example": "両端固定棒を一様に $\\Delta T$ 上げると $\\sigma=-E\\alpha\\Delta T$（圧縮）。直列・並列の組合せ棒では各部の応力を釣合い＋適合で求めます（公式問2-40〜2-42）。",
      "figureImage": "s2TwoBarsThermal"
    },
    {
      "id": "material-tests",
      "kind": "term",
      "term": "材料試験（じん性・硬さ・高温強度）",
      "formula": "シャルピー＝じん性／ビッカース＝硬さ／クリープ＝高温強度",
      "body": "シャルピー試験は切欠試験片を振子ハンマで打撃し、吸収エネルギーでじん性（粘り強さ）を測ります。ビッカース試験は対面角136°のダイヤ四角錐圧子を押し込み、硬さを測ります。クリープ試験は高温・一定応力で時間とともに進む変形・破断を調べます。",
      "example": "用途：衝撃に対する粘り＝シャルピー、表面の硬さ＝ビッカース、高温で使う部材の寿命＝クリープ（公式問2-43）。",
      "figureImage": "s2MaterialTests"
    },
    {
      "id": "stress-wave",
      "kind": "formula",
      "term": "応力波の伝ぱ速度",
      "formula": "$C=\\sqrt{\\dfrac{E}{\\rho}}$",
      "body": "衝撃を受けた面から固体中を応力波が伝わります。その速度 $C$ は縦弾性係数 $E$ と密度 $\\rho$ だけで決まり、応力の大きさには関係しません。",
      "example": "炭素鋼で約5100 m/s。一軸衝撃では応力 $\\sigma=EV/C$（$V$＝粒子速度。公式問2-44）。",
      "figureImage": "s2StressWave"
    }
  ]
}
```
