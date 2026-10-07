# -*- coding: utf-8 -*-
r"""振動2級 図の回答後overlay追記＋英語ラベル日本語化＋PNG化（恒久ツール・2026-10-08完成）。

分担(確定): 図\振動2級\{章-番号}.svg はChatGPT生成の中立図。構造=
  <g id="neutral-model">…中立(回答前)の中身…</g>  <g id="answer-overlay"/>…空(Claude追記枠)…
方針(ユーザー承認済):
  ①英語ラベルを日本語化(全SVG共通・TRANS辞書で機械置換。未訳290種)
  ②導出51枚は answer-overlay を埋めて回答後図を作る(中立132枚は前後同一=figキー1枚)
  ③回答前=overlay空 / 回答後=overlay埋 を同一ファイルで両立
  画風は 9-2(表)・4-9(波形) の試作でユーザー承認済。
★バグ教訓: overlayテキストの < > & は必ず esc() でXMLエスケープ。
レンダ: headless Chrome(viewBox読取り2x)。Bash実行時 dangerouslyDisableSandbox:true。

使い方:
  python tools/vib2_overlay.py scan        → 未訳の英語ラベル一覧(辞書穴埋め確認用)
  python tools/vib2_overlay.py build        → 全SVG: 日本語化(原本上書き)＋-ans生成＋全PNGを OUT へ
  python tools/vib2_overlay.py build 9      → 第9章だけ(章番号指定で部分build)
"""
import os, re, math, glob, subprocess, sys

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVGDIR = os.path.join(CAE, "図", "振動2級")
OUT = os.path.join(SVGDIR, "_png")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROF = os.path.join(SVGDIR, "_chromeprof")

NAVY = "#1F3A65"; RED = "#C82D2D"; GRAY = "#888888"; LIGHT = "#E1E7F2"

# ── 英→日 対訳辞書(全290種・scan実データ由来。長い句から先にマッチ) ──
TRANS = {
    # --- 計算機/数値(ch9,12) ---
    "Direct method": "直接法", "Iterative method": "反復法", "Direct methods": "直接法",
    "Iterative methods": "反復法", "Linear-system solvers": "連立1次方程式の解法",
    "Eigenvalue solvers": "固有値解析法", "Computation": "計算量", "Accuracy": "精度",
    "Convergence": "収束条件", "Initial vector": "初期ベクトル", "Multiply by A": "行列Aを掛ける",
    "Normalize": "正規化する", "Normalization": "正規化", "Repeat": "繰り返す",
    "Large matrix": "大規模行列", "Requested subset": "必要な個数ぶん",
    "First-order state form": "1階標準形(状態方程式)", "Second-order MCK form": "2階MCK形",
    "Smaller Δt": "刻み幅 Δt 小", "Larger Δt": "刻み幅 Δt 大", "Current state": "現在ステップ",
    "Next state": "次ステップ", "State equation": "状態方程式", "Compliance": "コンプライアンス",
    "Undamped mode shapes": "非減衰系の固有モード", "Time signal": "時間波形",
    "Spectrum": "周波数スペクトル", "Real subtraction": "実数の減算", "Rounding": "丸め誤差",
    "Cancellation": "桁落ち", "Overflow": "オーバーフロー", "Integer division": "整数除算",
    "Expression": "式", "Example": "例", "Multicore": "マルチコア", "Compatibility": "互換性",
    "Efficiency": "実行効率", "Portability": "移植性", "Object orientation": "オブジェクト指向",
    "Assembly": "アセンブリ言語", "High-level language": "高水準言語", "Category": "分類",
    "Address space": "アドレス空間", "Data width": "データ長", "Data type": "データ型",
    "Architecture A": "構成A", "Architecture B": "構成B", "Storage": "記憶",
    "Processing": "演算", "Control": "制御", "Sign": "符号部", "Exponent": "指数部",
    "Significand": "仮数部", "Precision : ______": "有効桁 : ______",
    "Range : ______": "表現範囲 : ______", "Weight": "重み", "Pipeline": "パイプライン",
    "Cache": "キャッシュ", "Memory": "メモリ",
    # --- 行列/連立 ---
    "Matrix A": "行列A", "Matrix B": "行列B", "Sparse matrix": "疎行列",
    "Dense matrix": "密行列", "Filled: potentially nonzero; white: zero": "塗り:非ゼロの可能性／白:ゼロ",
    "Filled cells: nonzero entries": "塗りマス:非ゼロ成分", "Equations": "方程式",
    "Coefficients": "係数", "Unknowns": "未知数", "One row per equation": "行=式に対応",
    "One column per variable": "列=変数に対応",
    # --- FEM(ch5,6) ---
    "Continuum": "連続体", "Nodes / elements": "節点・要素", "Spatial discretization": "空間離散化",
    "Weighted residual: ∫ w(x) R(x) dx": "重みつき残差: ∫ w(x) R(x) dx",
    "Displacement approach": "変位法", "Stress approach": "応力法",
    "Interpolation within an element": "要素内の補間", "Element → shape functions": "要素 → 形状関数",
    "Line density μ": "線密度 μ", "Density": "密度", "Static loading": "静荷重",
    "Vibration": "振動", "Force = mass × acceleration": "力＝質量×加速度",
    "Displacement": "変位", "Added mass": "付加質量", "Add mass": "質量付加",
    "F in-plane": "面内成分 F", "F out-of-plane": "面外成分 F", "Time-varying load F(t)": "変動力 F(t)",
    "Axial deformation": "軸方向の伸び", "Bending": "曲げ", "Straight interpolation": "直線補間",
    "Smooth deflection": "なめらかなたわみ", "Linear hexahedra": "1次六面体",
    "Linear tetrahedra": "1次四面体", "Quadratic hexahedra": "2次六面体",
    "Quadratic tetrahedra": "2次四面体", "Point mass": "集中質量要素",
    "Inertia about center of mass": "重心まわりの慣性モーメント", "Products of inertia": "慣性乗積",
    "1D element": "1次元要素", "2D quadrilateral": "2次元四辺形要素",
    "×  Gauss integration points": "×  ガウス積分点", "3-node triangle": "3節点三角形要素",
    "4-node quadrilateral": "4節点四角形要素", "Lower order": "低次要素", "Higher order": "高次要素",
    "Triangle": "三角形", "Quad": "四辺形", "Solid": "ソリッド", "Computation time": "計算時間",
    "Applicable geometry": "適用できる形状", "Mesh refinement": "メッシュの細かさ",
    "Exact solution": "厳密解", "Lower order / fine mesh": "低次要素／細かい分割",
    "Higher order / coarse mesh": "高次要素／粗い分割", "Kirchhoff (thin plate)": "キルヒホッフ(薄板)",
    "Reissner–Mindlin": "ライスナー・ミンドリン(厚板)",
    "Thickness / in-plane dimension: t / L": "板厚／面内寸法: t / L",
    "Thin curved shell": "薄肉曲面シェル", "Thickness t; representative length L": "板厚 t・代表寸法 L",
    # --- 減衰/モデル化(ch7) ---
    "Damping ratio": "減衰比", "Viscous": "粘性減衰", "Hysteresis": "ヒステリシス減衰",
    "Friction": "摩擦減衰", "Rubber cushion": "ゴムクッション", "Support frame": "支持フレーム",
    "Powerplant": "パワープラント", "Body base": "車体ベース", "Excitation source": "加振源",
    "Elastic mounts": "弾性マウント", "Rubber mount": "ゴムマウント",
    # --- 構造物名(ch7,11) ---
    "Car body": "車体", "Body shell": "ボディシェル", "Boom": "ブーム", "Bucket": "バケット",
    "Rock": "岩盤", "Control box": "制御箱", "Motor rotor": "電動機回転子",
    "Male rotor": "オスロータ", "Female rotor": "メスロータ", "Inlet": "吸込口", "Outlet": "吐出口",
    "Underfloor equipment": "床下機器", "Interior acoustic volume": "車室内音場",
    "Airlock": "エアロック", "Equipment hatch": "機器搬入口", "Pipe penetration": "配管貫通部",
    "Crane": "クレーン", "Radiator": "ラジエータ", "Side member": "サイドメンバ",
    "Steel panel": "鋼板部分", "Glass": "ガラス部分", "Wiper": "ワイパ", "Concrete": "コンクリート",
    "Hinge": "ヒンジ", "Door bracket": "ドア側ブラケット", "Body bracket": "ボディ側ブラケット",
    "Shared node": "共有節点", "Connector region": "結合部", "Bolt joint": "ボルト結合",
    "Layer cross-section": "二重要素の断面", "Cross-section": "断面", "Local mesh": "周辺メッシュ",
    "Cross-section rotation": "断面の回転", "Beam": "はり",
    # --- 計測/検証(ch11) ---
    "Sandbag": "土のう", "Coherence": "コヒーレンス", "Reciprocity": "相反性", "Panel": "パネル",
    "Hammer mass": "ハンマの質量", "Tip material": "チップの材質", "Force window": "フォース窓",
    "Exponential window": "指数窓", "Impact hammer": "インパクトハンマ", "Shaker": "動電型加振器",
    "Sensor attachment": "センサ取付け", "Sensor": "センサ", "Local coordinates": "ローカル座標系",
    "Excitation locations": "加振点", "Excitation position": "加振位置",
    "Excitation frequency": "加振周波数", "Response amplitude": "応答振幅",
    "Measured waveform required": "計測波形が必要",
    "Insert original measurement before use": "使用前に実測波形を挿入",
    "Node coordinates": "節点座標", "Element connectivity": "要素結合", "Model": "モデル",
    "Measurement": "計測", "Geometry": "形状", "Material": "材料", "Structure": "構造",
    "Mesh": "メッシュ", "Boundary": "境界", "Load": "荷重", "Increase thickness": "板厚増",
    "Reduce weight": "軽量化", "Add support": "支持追加", "Stiffness": "剛性", "Mass": "質量",
    # --- 境界/荷重(ch8,10) ---
    "Input PSD": "入力PSD", "Response PSD": "応答PSD", "Model boundary?": "モデル境界?",
    "Rigid-body modes": "剛体モード", "Sum of forces": "力の総和", "Units / scale": "単位／桁",
    "Boundary conditions": "境界条件", "Operating frequency band": "運転周波数域",
    "Initial natural frequency": "もとの固有振動数", "Frame count": "フレーム数",
    "Surface / interior": "表面／内部", "Color depth": "色深度", "Node count": "節点数",
    # --- 音響(ch4,10) ---
    "A / A₀  (log scale)": "A / A₀ (対数目盛)", "Weighting (dB)": "重み(dB)",
    "p / p₀  (log scale)": "p / p₀ (対数目盛)", "Sound pressure level (dB)": "音圧レベル(dB)",
    "Schematic pressure axis (not to scale)": "音圧軸(模式・比例ではない)", "Generator": "発電機",
    "Propagation": "伝播", "Temperature / sound": "温度と音速", "Sound in air": "空気中の音",
    "Medium boundary": "媒質境界", "Medium A": "媒質A", "Medium B": "媒質B",
    "Frequency (log scale)": "周波数(対数目盛)", "Frequency": "周波数",
    # --- 波形/応答/物理(ch4) ---
    "Initial displacement": "初期変位", "Initial velocity": "初期速度", "Amplitude": "振幅",
    "Mode shape: {a, a}": "モード形: {a, a}", "Prescribed mode: {1, 1}": "指定モード: {1, 1}",
    "Amplitude reference": "振幅の基準", "Fixed": "固定", "Free": "自由", "Mode": "モード",
    "transform": "変換", "N DOF": "N 自由度", "Time integration": "時間積分",
    "Internal forces only": "内力のみ", "Conservative forces only": "保存力のみ",
    "Momentum": "運動量", "Energy": "エネルギー", "Lock": "ロック", "Contact line": "接触線",
    "Contact": "接触", "Stopped": "停止時", "Operating": "運転中",
    # --- 技術者倫理(ch13) ---
    "Error found": "誤りを発見", "Revised results": "訂正版", "Information": "情報",
    "Access": "アクセス", "Handling": "扱い", "Client": "依頼元",
    "Inspection body": "検査機関", "Previous employer criteria": "前職の評価基準",
    "Commissioned results": "委託された解析結果", "License": "使用許諾",
    "Designated PC": "指定PC", "Other PC": "隣のPC", "Borrowed PC": "借用PC",
    "Individual": "個人の利益", "Organization": "自組織の利益", "Other organization": "他組織の利益",
    "Judgment": "判断", "Consideration": "検討", "Decision": "決定",
    "Public explanation": "報道されても説明可か", "Other party perspective": "相手の立場で可か",
    "Third party explanation": "第三者に説明可か", "Instructions": "指示に従う",
    "Design error": "設計ミス", "Risk": "危険", "Responsible person": "責任者",
    "Internal channel": "組織内の別ルート",
    # --- 汎用(短語・後ろに置いて誤爆防止) ---
    "Geometry A": "形状A", "Geometry B": "形状B", "Case A": "ケースA", "Case B": "ケースB",
    "Case C": "ケースC", "Features": "特徴", "Advantages": "長所", "Limitations": "短所",
    "Role": "役割", "Purpose": "目的", "Setting": "設定", "Check": "確認", "Input": "入力",
    "Length": "長さ", "Unit": "単位", "Increase": "増加", "Decrease": "減少",
    "Frame": "フレーム", "Support": "支持", "Body": "車体", "Time": "時間", "Force": "力",
}

def apply_trans(svg):
    """ >英語< を日本語へ。語内の空白は \\s+ 許容、前後空白も許容、長い句から先に。"""
    for en in sorted(TRANS, key=len, reverse=True):
        pat = r'>\s*' + r'\s+'.join(re.escape(w) for w in en.split()) + r'\s*<'
        svg = re.sub(pat, (lambda j: (lambda m: '>' + j + '<'))(TRANS[en]), svg)
    return svg

# ── 描画ヘルパ ──
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def txt(x, y, s, size=19, fill=NAVY, anchor="middle", weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" '
            f'font-family="sans-serif">{esc(s)}</text>')
def ln(x1, y1, x2, y2, stroke=NAVY, w=2.4, dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}"{d} opacity="{op}"/>'
def poly(pts, stroke=NAVY, w=2.6, fill="none", dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    pd = " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="M {pd}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{d} opacity="{op}"/>'
def curve(fn, x0, x1, n=140, stroke=NAVY, w=2.6, dash=None, op=1.0):
    return poly([(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], stroke, w, "none", dash, op)
def box(x, y, w, h, fill=LIGHT, stroke=NAVY, sw=1.6, op=0.95, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}" rx="{rx}"/>'
def mask(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" opacity="0.92"/>'
def dot(x, y, r=5, fill=RED): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
def head(x, y, ang, stroke=NAVY, size=10):
    a1 = ang + math.radians(148); a2 = ang - math.radians(148)
    return (ln(x, y, x + size * math.cos(a1), y + size * math.sin(a1), stroke, 2.4)
            + ln(x, y, x + size * math.cos(a2), y + size * math.sin(a2), stroke, 2.4))
def arrow(x1, y1, x2, y2, stroke=NAVY, w=2.6, size=10):
    return ln(x1, y1, x2, y2, stroke, w) + head(x2, y2, math.atan2(y2 - y1, x2 - x1), stroke, size)
def block(cx, cy, lines, size=17, fill=NAVY, anchor="middle", lh=25, weight="normal"):
    y0 = cy - (len(lines) - 1) * lh / 2
    return "".join(txt(cx, y0 + i * lh, s, size, fill, anchor, weight) for i, s in enumerate(lines))

# ── 導出51番号 → overlay(回答後の追記) ──
def ov_3_5():  # 応力ひずみ線図(弾性/塑性・E・降伏点)。原点O=(730,500)
    return (ln(730, 500, 858, 372, NAVY, 3.2)
            + '<path d="M858,372 Q935,338 1012,330" fill="none" stroke="%s" stroke-width="3.2"/>' % NAVY
            + dot(858, 372, 5, RED)
            + txt(775, 462, "弾性域(比例)", 14, GRAY) + txt(950, 478, "塑性域", 14, GRAY)
            + txt(792, 418, "傾き = E", 15, RED, "start", "bold")
            + txt(905, 352, "降伏点／比例限度", 13, RED))

def ov_3_13():  # はりのたわみ基礎式
    return (txt(600, 520, "モーメント大 → 曲率大", 15, GRAY)
            + box(360, 600, 480, 95)
            + txt(600, 633, "たわみの基礎式", 16, RED, "middle", "bold")
            + txt(600, 668, "EI · d²y/dx² = −M(x)", 21, NAVY, "middle"))

def ov_4_9():  # 不減衰ωn(青一定)+減衰ωd(赤包絡)重ね描き。baseline350 ユーザー承認済
    BASE = 350.0; X0, X1 = 150.0, 850.0; A = 78.0
    def sine(stroke, ncyc, tau=None, amp=A):
        pts = [(X0 + (X1 - X0) * i / 360, BASE - amp * (math.exp(-((X0 + (X1 - X0) * i / 360) - X0) / tau) if tau else 1) * math.sin(2 * math.pi * ncyc * (i / 360))) for i in range(361)]
        return poly(pts, stroke, 2.6)
    def env(tau):
        up = [(X0 + (X1 - X0) * i / 120, BASE - A * math.exp(-((X0 + (X1 - X0) * i / 120) - X0) / tau)) for i in range(121)]
        dn = [(X0 + (X1 - X0) * i / 120, BASE + A * math.exp(-((X0 + (X1 - X0) * i / 120) - X0) / tau)) for i in range(121)]
        return poly(up, RED, 1.2, "none", "4 4", 0.7) + poly(dn, RED, 1.2, "none", "4 4", 0.7)
    return (sine(NAVY, 5.0) + env(900.0) + sine(RED, 4.6, tau=900.0)
            + txt(690, 150, "不減衰 ωn (一定振幅)", 18, NAVY, "start", "bold")
            + txt(690, 178, "減衰 ωd (ωd < ωn)", 18, RED, "start", "bold")
            + txt(690, 206, "→ 減衰側は周期がわずかに長い", 15, GRAY, "start"))

def ov_4_11():  # 周波数応答: 対策前ピーク50Hz / 対策後ピーク高周波へ。x軸490, 50Hz線x=500
    base = 490
    def peak(x0, amp, wid, stroke, dash=None):
        return curve(lambda x: base - amp / (1 + ((x - x0) / wid) ** 2), 135, 900, stroke=stroke, dash=dash)
    return (peak(500, 300, 55, RED, "7 5") + peak(690, 270, 60, NAVY)
            + arrow(540, 205, 655, 220, RED, 2.6)
            + txt(300, 165, "対策前(赤): 50Hzで共振", 15, RED, "start", "bold")
            + txt(300, 190, "対策後(紺): 固有振動数を上げ 50Hzから離す", 14, NAVY, "start", "bold"))

def ov_4_19():  # 不足減衰(赤・振動収束) vs 過減衰(紺・単調)。baseline350
    base = 350; x0 = 160; A = 150
    ud = lambda x: base - A * math.exp(-(x - x0) / 230) * math.cos(2 * math.pi * (x - x0) / 150)
    od = lambda x: base - A * math.exp(-(x - x0) / 120)
    return (curve(ud, x0, 890, stroke=RED, w=2.6) + curve(od, x0, 890, stroke=NAVY, w=2.6)
            + txt(560, 170, "不足減衰(赤): 行き過ぎて振動しつつ収束", 14, RED, "start", "bold")
            + txt(560, 195, "過減衰(紺): 振動せず単調に収束", 14, NAVY, "start", "bold")
            + txt(560, 220, "境界 = 臨界減衰 ζ = 1", 15, GRAY, "start", "bold"))

def ov_4_20():  # 0.4sに8周期→T=0.05→ω→k=mω²。baseline350, 区間150-850
    base = 350; X0, X1 = 150, 850; A = 55
    s = lambda x: base - A * math.sin(2 * math.pi * 8 * (x - X0) / (X1 - X0))
    ticks = "".join(ln(X0 + (X1 - X0) * k / 8, base - 6, X0 + (X1 - X0) * k / 8, base + 6, GRAY, 1.4) for k in range(9))
    return (mask(205, 165, 590, 250)
            + txt(500, 200, "0.4 s にちょうど 8 周期", 16, RED, "middle", "bold")
            + txt(500, 232, "T = 0.4/8 = 0.05 s → ω = 2π/T → k = m ω²", 16, NAVY, "middle")
            + curve(s, X0, X1, n=240, stroke=NAVY, w=2.6) + ticks)

def ov_4_23():  # 矩形パルスのフーリエ変換=sinc。右上にインセット
    ax, ay, bx = 690, 300, 920
    sval = lambda u: 1.0 if abs(u) < 1e-6 else math.sin(u) / u
    f = lambda x: ay - 72 * sval((x - 805) / 9.6)
    return (ln(ax, ay, bx, ay, GRAY, 1.6) + ln(ax, 235, ax, 345, GRAY, 1.6)
            + curve(f, ax + 5, bx, n=200, stroke=RED, w=2.4)
            + txt(805, 228, "F(ω) = 2T·sin(ωT)/(ωT)", 14, RED, "middle", "bold")
            + txt(bx, 322, "ω", 14, GRAY)
            + txt(805, 370, "幅 T が狭いほどスペクトルが広がる", 13, GRAY, "middle"))

def ov_4_29():  # モード重ね合わせ: 3つの独立1自由度モード振動子
    out = ""
    for (xi, mk), cy in zip([("ξ₁", "m₁*, k₁*"), ("ξ₂", "m₂*, k₂*"), ("ξ₃", "m₃*, k₃*")], [182, 332, 482]):
        out += txt(775, cy - 6, xi + " : 独立1自由度モード", 15, NAVY, "middle", "bold")
        out += txt(775, cy + 18, "(モード質量 " + mk.split(',')[0] + " / モード剛性" + mk.split(',')[1] + ")", 12, GRAY, "middle")
    return out + txt(515, 320, "→ 独立モードへ分解", 13, RED, "middle", "bold")

def ov_4_31():  # 第1次{1,1}同相 / 第2次{1,-1}逆相。質点中心(345,295)(655,295)
    return (arrow(345, 274, 420, 274, NAVY, 3) + arrow(655, 274, 730, 274, NAVY, 3)
            + arrow(345, 318, 420, 318, RED, 3) + arrow(655, 318, 580, 318, RED, 3)
            + txt(500, 465, "第1次モード {1,1}: 2質点が同じ向き(同相)", 14, NAVY, "middle", "bold")
            + txt(500, 490, "第2次モード {1,−1}: 逆向き(逆相)", 14, RED, "middle", "bold"))

def ov_4_32():  # 第1次{1,1}のモード質量/剛性
    return (arrow(345, 278, 422, 278, NAVY, 3) + arrow(655, 278, 732, 278, NAVY, 3)
            + box(150, 418, 700, 135)
            + txt(500, 450, "第1次モード {1,1} に対し", 16, RED, "middle", "bold")
            + block(500, 505, ["モード質量 m* = φᵀMφ = m + m = 2m", "モード剛性 k* = φᵀKφ (両質点の寄与が加算)"], 16, NAVY))

def ov_4_33():  # 固有モードの3通りの正規化。右パネル(690,185,245,280)
    return (box(675, 180, 265, 300)
            + txt(807, 212, "正規化の3通り (モード{a,a})", 15, RED, "middle", "bold")
            + block(807, 330, ["① 最大成分 = 1", "    → a = 1", "② ベクトルノルム = 1", "    → a = 1/√2",
                                "③ 質量正規化 φᵀMφ = 1", "    → a = 1/√(2m)"], 14, NAVY, "middle", 27))

def ov_4_36():  # 境界条件→モード形 / 初期条件→振幅・位相
    return (arrow(150, 228, 150, 266, NAVY, 2.4) + arrow(820, 255, 820, 266, NAVY, 2.4)
            + txt(485, 250, "境界条件(端の拘束) → モード形(固有関数)を決める", 14, NAVY, "middle", "bold")
            + arrow(320, 515, 320, 462, RED, 2.4) + arrow(680, 515, 680, 462, RED, 2.4)
            + txt(500, 447, "初期条件(初期変位・初期速度) → 各モードの振幅・位相を決める", 13, RED, "middle", "bold"))

def ov_4_37():  # λ=c/f=340/850=0.4m
    return (box(360, 418, 480, 72)
            + txt(600, 448, "λ = c / f = 340 / 850", 18, NAVY, "middle")
            + txt(600, 476, "= 0.4 m", 19, RED, "middle", "bold"))

def ov_4_38():  # 波数 k=2π/λ
    return (box(330, 420, 540, 80)
            + txt(600, 452, "波数 k = 2π / λ", 19, NAVY, "middle", "bold")
            + txt(600, 480, "λ が短いほど k が大きい", 15, GRAY, "middle"))

def ov_4_42():  # ΔL=6dB→音圧比≈2
    return (box(150, 118, 520, 92)
            + txt(410, 150, "レベル差 ΔL = 68 − 62 = 6 dB", 17, NAVY, "middle", "bold")
            + txt(410, 184, "音圧比 = 10^(6/20) ≈ 2", 18, RED, "middle", "bold"))

def ov_4_43():  # 音圧3倍→ΔL≈9.5dB
    return (box(300, 500, 600, 82)
            + txt(600, 532, "音圧 3 倍 → ΔL = 20·log₁₀(3)", 17, NAVY, "middle")
            + txt(600, 562, "≈ 9.5 dB 上昇", 18, RED, "middle", "bold"))

def ov_5_11():  # ガラーキン/選点/最小二乗。x軸320
    return (txt(500, 362, "∫ w(x) R(x) dx = 0 とおく", 17, NAVY, "middle", "bold")
            + block(500, 432, ["重み = 形状関数 → ガラーキン法", "重み = デルタ関数 → 選点法",
                                "重み = 残差自身 → 最小二乗法"], 15, NAVY, "middle", 28))

def ov_5_19():  # 棒要素の整合質量行列
    return (box(248, 543, 504, 52)
            + txt(500, 575, "Mᵢⱼ = ∫μLᵢLⱼdx = (μl/6)·[[2,1],[1,2]]", 16, RED, "middle", "bold"))

def ov_6_1():  # 軸=1次 / 曲げ=3次エルミート
    return (txt(260, 512, "→ 1次補間(直線)", 15, RED, "middle", "bold")
            + txt(735, 512, "→ 3次補間(エルミート)", 15, RED, "middle", "bold"))

def ov_6_5():  # FEM解は下側(剛め)から漸近+体積ロッキング。厳密解線y=235, x軸490
    f = lambda x: 235 + 170 * math.exp(-(x - 160) / 230)
    return (curve(f, 180, 870, stroke=NAVY, w=2.8)
            + txt(620, 300, "FEM解: 下側から漸近(変位は小さめ=剛め)", 13, NAVY, "middle", "bold")
            + txt(620, 360, "非圧縮材 → 体積ロッキングで収束悪化", 13, RED, "middle"))

def ov_7_1():  # レイリー減衰: 質量比例(下降)+剛性比例(上昇)→和U字。原点(230,550)
    cl = lambda y: max(198, min(545, y))
    mass = lambda x: cl(550 - 35000 / (x - 149))
    stiff = lambda x: cl(550 - 0.30 * (x - 230))
    summ = lambda x: cl(550 - (35000 / (x - 149) + 0.30 * (x - 230)))
    return (curve(mass, 258, 958, stroke=NAVY, w=2.2, dash="7 5")
            + curve(stiff, 258, 958, stroke=NAVY, w=2.2, dash="7 5")
            + curve(summ, 300, 940, stroke=RED, w=3.0)
            + txt(330, 250, "質量比例 α/2ω", 13, NAVY, "start")
            + txt(770, 300, "剛性比例 βω/2", 13, NAVY, "start")
            + txt(560, 215, "和 = レイリー減衰 (U字)", 15, RED, "middle", "bold")
            + txt(600, 640, "C = αM + βK", 17, NAVY, "middle", "bold"))

def ov_7_4():  # 比例減衰→対角化。行列域 対角強調
    return (ln(405, 222, 765, 477, RED, 3.0, "9 6")
            + txt(585, 150, "比例減衰 → モード座標で対角化", 17, RED, "middle", "bold")
            + txt(585, 585, "非対角成分 = 0 (モードの直交性)", 16, NAVY, "middle", "bold"))

def ov_8_14():  # 入力PSD→応答PSD→RMS。第3枠中心(940,360)
    return (txt(940, 175, "評価量", 15, RED, "middle", "bold")
            + txt(940, 345, "RMS", 30, RED, "middle", "bold")
            + txt(940, 390, "(実効値)", 16, NAVY, "middle")
            + txt(940, 450, "= √(∫ 応答PSD df)", 14, NAVY, "middle"))

def ov_8_15():  # 入力大の周波数と固有振動数の両方を優先。縦線x=450,650,900
    return (arrow(450, 232, 450, 202, RED, 2.6) + txt(450, 188, "入力大", 14, RED, "middle", "bold")
            + arrow(650, 232, 650, 202, NAVY, 2.6) + txt(650, 188, "固有振動数", 13, NAVY, "middle", "bold")
            + arrow(900, 232, 900, 202, NAVY, 2.6) + txt(900, 188, "固有振動数", 13, NAVY, "middle", "bold")
            + box(230, 600, 740, 72)
            + txt(600, 630, "入力振幅が大きい周波数 と 固有振動数 の両方で応答大", 14, NAVY, "middle", "bold")
            + txt(600, 657, "→ この2種の周波数を優先的に評価する", 14, RED, "middle", "bold"))

def ov_8_20():  # f=V/λ, Δφ=2πL/λ
    return (box(380, 538, 440, 112)
            + txt(600, 575, "加振周波数  f = V / λ", 18, NAVY, "middle")
            + txt(600, 618, "前後輪の位相差  Δφ = 2π L / λ", 18, RED, "middle", "bold"))

def ov_9_2():  # 直接法/反復法 対比表(ユーザー承認済)
    def cell(cx, cy, lines, fill=NAVY):
        n = len(lines); step = 24; y0 = cy - (n - 1) * step / 2 + 6
        return "".join(txt(cx, y0 + i * step, ln, 18, fill) for i, ln in enumerate(lines))
    return (cell(510, 270, ["有限回の演算で", "厳密解 (計算量 多)"]) + cell(750, 270, ["近似を反復", "疎行列で有利"])
            + cell(510, 360, ["丸め誤差のみ", "高精度"]) + cell(750, 360, ["停止条件で決まる"])
            + cell(510, 450, ["不要", "(有限回で完了)"], RED) + cell(750, 450, ["必要", "(発散しうる)"], RED))

def ov_9_6():  # 台形近似の誤差が小さい。ミニ軸 A(90,460) B(560,460)
    return (txt(277, 560, "長方形近似: 誤差 大", 14, NAVY, "middle", "bold")
            + txt(747, 560, "台形近似: 誤差 小", 14, RED, "middle", "bold")
            + txt(500, 120, "→ 台形近似のほうが真の面積とのずれ(誤差)が小さい", 15, RED, "middle", "bold"))

def ov_9_7():  # ガウス・ザイデル法=連立1次(反復)→固有値解析でない
    return (arrow(610, 300, 680, 300, NAVY, 2.4)
            + box(300, 538, 420, 58)
            + txt(510, 562, "ガウス・ザイデル法 = 連立1次方程式の反復解法", 13, NAVY, "middle", "bold")
            + txt(510, 585, "→ 固有値解析法ではない", 14, RED, "middle", "bold"))

def ov_9_8():  # べき乗法
    return (box(220, 540, 560, 56)
            + txt(500, 564, "反復のたびに 最大固有値 の固有ベクトル方向へ収束", 14, NAVY, "middle", "bold")
            + txt(500, 586, "→ べき乗法(反復乗算法)", 14, RED, "middle", "bold"))

def ov_9_9():  # ヤコビ法(相似変換→対角化)
    return (txt(650, 360, "→ 対角形へ収束", 13, RED, "middle", "bold")
            + box(230, 540, 540, 56)
            + txt(500, 564, "相似変換を繰り返す → 対角行列(対角に固有値)へ収束", 13, NAVY, "middle", "bold")
            + txt(500, 586, "= ヤコビ法(相似変換法)", 14, RED, "middle", "bold"))

def ov_9_10():  # サブスペース法
    return (box(220, 544, 560, 56)
            + txt(500, 568, "部分空間へ縮約 → 指定個数の固有値・固有ベクトルを同時抽出", 13, NAVY, "middle", "bold")
            + txt(500, 590, "= サブスペース法(部分空間反復法)", 14, RED, "middle", "bold"))

def ov_9_11():  # [A]z=λ[B]z のブロック。block(650,170,260,210) 分割x=780,y=275
    return (txt(715, 232, "0", 22, NAVY, "middle", "bold") + txt(845, 232, "I", 22, NAVY, "middle", "bold")
            + txt(715, 340, "−K", 20, RED, "middle", "bold") + txt(845, 340, "−C", 20, RED, "middle", "bold")
            + txt(640, 165, "[A] =", 15, NAVY, "end")
            + txt(500, 470, "状態ベクトル z={x; ẋ} で1階化 → [A]z = λ[B]z,  [B]=diag(I, M)", 13, NAVY, "middle", "bold"))

def ov_9_12():  # 複素平面: 左半面=安定。横軸(100,315)-(915,315), 縦軸x=500
    return ('<rect x="100" y="110" width="400" height="410" fill="%s" opacity="0.35"/>' % LIGHT
            + dot(360, 235, 6, RED) + dot(360, 395, 6, RED)
            + ln(500, 235, 360, 235, GRAY, 1.2, "4 3") + ln(500, 395, 360, 395, GRAY, 1.2, "4 3")
            + txt(250, 150, "Re(λ) < 0 : 安定", 15, NAVY, "middle", "bold")
            + txt(378, 228, "λ", 14, RED, "start")
            + txt(560, 475, "実部が負=安定 / 実部・虚部の比が減衰の大きさ", 13, GRAY, "middle"))

def ov_9_14():  # ウィルソンθ法: Δt大→高次モード数値減衰。box1(y115-265)/box2(y325-475)
    s1 = lambda x: 190 - 45 * math.sin(2 * math.pi * (x - 170) / 130)
    s2 = lambda x: 400 - 45 * math.exp(-(x - 170) / 300) * math.sin(2 * math.pi * (x - 170) / 130)
    return (curve(s1, 170, 820, n=200, stroke=NAVY, w=2.4)
            + curve(s2, 170, 820, n=200, stroke=RED, w=2.4)
            + txt(500, 555, "Δtを大きくとると高次モードが数値減衰で抑制(振幅↓) = ウィルソンθ法", 13, RED, "middle", "bold"))

def ov_9_15():  # 陽解法
    return (box(150, 500, 700, 82)
            + txt(500, 530, "陽解法: 反復(収束計算)なしで次ステップを逐次計算", 15, NAVY, "middle", "bold")
            + txt(500, 560, "ただし Δt が大きいと不安定(条件付き安定)", 15, RED, "middle", "bold"))

def ov_9_17():  # 剰余剛性(低次)/剰余質量(高次)。帯 x420-640, x軸490
    return (arrow(300, 250, 413, 250, NAVY, 2.4) + txt(298, 234, "ω<ωa(低次):", 13, NAVY, "end", "bold")
            + txt(298, 258, "剰余剛性", 14, RED, "end", "bold")
            + arrow(760, 250, 647, 250, NAVY, 2.4) + txt(762, 234, "ω>ωb(高次):", 13, NAVY, "start", "bold")
            + txt(762, 258, "剰余質量", 14, RED, "start", "bold")
            + txt(530, 560, "対象帯域の外側を 剰余剛性(低次)・剰余質量(高次) で補正", 13, NAVY, "middle", "bold"))

def ov_9_18():  # 非減衰モードで M,C,K 同時対角化。中立テキスト(y340)と重ならぬ上帯(y258-314)へ
    def diag(cx, cy, lab):
        o = box(cx - 48, cy - 28, 96, 56, LIGHT, NAVY, 1.4)
        for i in range(3):
            o += dot(cx - 24 + i * 24, cy - 16 + i * 16, 4.5, NAVY)
        o += txt(cx + 54, cy + 5, lab, 13, RED, "start", "bold")
        return o
    return (diag(230, 292, "[M]対角") + diag(500, 292, "[C]対角") + diag(770, 292, "[K]対角")
            + txt(500, 582, "非減衰系のモードで M・C・K が同時に対角化(モードの直交性) → 非対角 = 0", 12.5, NAVY, "middle", "bold"))

def ov_9_19():  # FFTの誤差: エイリアシング+リーケージ
    return (box(230, 480, 540, 92)
            + txt(500, 510, "FFT に伴う誤差", 16, RED, "middle", "bold")
            + block(500, 548, ["① エイリアシング(サンプリング不足)", "② リーケージ(切り出し区間が非整数周期)"], 14, NAVY, "middle", 26))

def ov_10_2():  # 曲げモード: 固定端(左)でひずみエネルギー密度 高=補強
    return ('<ellipse cx="185" cy="338" rx="55" ry="48" fill="%s" opacity="0.30"/>' % RED
            + arrow(330, 338, 245, 338, RED, 2.4)
            + txt(345, 333, "ひずみエネルギー密度 高", 14, RED, "start", "bold")
            + txt(345, 357, "= 剛性を強化すべき部位", 13, NAVY, "start"))

def ov_10_4():  # ねじりモード: 結合部に集中=補強優先。部材中点
    o = ""
    for x, y in [(205, 305), (385, 320), (595, 350), (825, 385)]:
        o += '<circle cx="%d" cy="%d" r="26" fill="%s" opacity="0.28"/>' % (x, y, RED)
    return o + txt(500, 560, "ひずみエネルギーが集中する結合部・部材 = 補強を優先すべき部位", 14, RED, "middle", "bold")

def ov_10_6():  # k↑→f↑ / m↑→f↓
    return (txt(270, 440, "剛性 k 増 → f 上昇", 14, NAVY, "middle", "bold")
            + txt(730, 440, "質量 m 増 → f 低下", 14, RED, "middle", "bold"))

def ov_10_7():  # f∝√k, f2/f1=1.2→k2/k1=1.44。軸原点(140,485)
    f = lambda x: 485 - 350 * math.sqrt((x - 140) / 750)
    return (curve(f, 140, 870, stroke=NAVY, w=2.8)
            + box(430, 180, 430, 110)
            + txt(645, 215, "f ∝ √k", 17, NAVY, "middle")
            + txt(645, 252, "f₂/f₁ = 1.2 → k₂/k₁ = 1.2² = 1.44", 16, RED, "middle", "bold"))

def ov_10_9():  # 妥当性チェックの各確認要点。右box(650,y,180,45) 行y177/277/377/477
    pts = ["拘束条件と整合する数か", "外力の総和 = 反力か", "単位系の桁は妥当か", "想定どおりか"]
    return "".join(txt(740, 185 + i * 100, s, 13, RED, "middle", "bold") for i, s in enumerate(pts))

def ov_10_16():  # データ量∝節点×フレーム×情報。右box(580,y,280,50) 行y160/265/370/475
    pts = ["表面節点のみ(内部省略)", "フレーム数を減らす", "表面だけ保持", "色深度を下げる"]
    return ("".join(txt(720, 168 + i * 105, s, 13, RED, "middle", "bold") for i, s in enumerate(pts))
            + txt(500, 560, "データ量 ∝ 節点数 × フレーム数 × 各節点情報 → 上記で削減", 14, NAVY, "middle", "bold"))

def ov_10_17():  # 車体ねじり低減策。部材中点
    o = ""
    for (x, y), lab in zip([(205, 305), (385, 320), (595, 350), (825, 385)], ["閉断面化", "クロスメンバ追加", "制振器付与", "ねじり剛性↑"]):
        o += '<circle cx="%d" cy="%d" r="22" fill="%s" opacity="0.26"/>' % (x, y, RED)
    return (o + txt(500, 540, "有効な対策: 閉断面化 / クロスメンバ追加 / 制振器の付与", 14, RED, "middle", "bold")
            + txt(500, 565, "(ねじり剛性を上げる・減衰を与える位置)", 13, NAVY, "middle"))

def ov_10_19():  # 剛体モード6個=並進3+回転3, 固有振動数0
    return (box(250, 500, 500, 86)
            + txt(500, 532, "剛体モード = 並進3 (x, y, z) + 回転3 = 計6個", 15, NAVY, "middle", "bold")
            + txt(500, 562, "拘束がないと 固有振動数 0 のモードが6個現れる", 14, RED, "middle", "bold"))

def ov_11_2():  # 加速度オフセット2階積分→t²でドリフト。軸原点(160,550), 零線y360
    drift = lambda x: 360 - 0.00055 * (x - 160) ** 2
    return (curve(drift, 160, 1040, stroke=RED, w=3.0)
            + txt(560, 250, "一定オフセットを2階積分 → 変位が t² で増大(ドリフト)", 14, RED, "middle", "bold"))

def ov_11_7():  # 剛性実物↑ or 質量実物↓ → 実測共振>計算。Increase列x600/Decrease列x920, Stiffness行y252/Mass行y327
    return (txt(600, 258, "○ 実測↑", 15, RED, "middle", "bold") + txt(920, 258, "—", 15, GRAY, "middle")
            + txt(600, 333, "—", 15, GRAY, "middle") + txt(920, 333, "○ 実測↑", 15, RED, "middle", "bold")
            + txt(600, 470, "剛性が実物で高い / 質量が実物で小さい → 実測の共振振動数が計算より高い", 14, NAVY, "middle", "bold"))

def ov_11_17():  # ゴム: 剛性・減衰が振幅・周波数に依存。軸原点(250,550)
    c1 = lambda x: 480 - 230 * (x - 250) / 720
    c2 = lambda x: 540 - 150 * ((x - 250) / 720) ** 1.6
    return (curve(c1, 260, 960, stroke=NAVY, w=2.6) + curve(c2, 260, 960, stroke=RED, w=2.6)
            + txt(820, 250, "剛性", 14, NAVY, "start", "bold") + txt(820, 400, "減衰", 14, RED, "start", "bold")
            + txt(610, 660, "剛性・減衰は振幅・周波数に依存 → 実働条件(振幅・周波数)で検証", 14, NAVY, "middle", "bold"))

OVERLAYS = {
    "3-5": ov_3_5, "3-13": ov_3_13, "4-9": ov_4_9, "4-11": ov_4_11, "4-19": ov_4_19,
    "4-20": ov_4_20, "4-23": ov_4_23, "4-29": ov_4_29, "4-31": ov_4_31, "4-32": ov_4_32,
    "4-33": ov_4_33, "4-36": ov_4_36, "4-37": ov_4_37, "4-38": ov_4_38, "4-42": ov_4_42,
    "4-43": ov_4_43, "5-11": ov_5_11, "5-19": ov_5_19, "6-1": ov_6_1, "6-5": ov_6_5,
    "7-1": ov_7_1, "7-4": ov_7_4, "8-14": ov_8_14, "8-15": ov_8_15, "8-20": ov_8_20,
    "9-2": ov_9_2, "9-6": ov_9_6, "9-7": ov_9_7, "9-8": ov_9_8, "9-9": ov_9_9,
    "9-10": ov_9_10, "9-11": ov_9_11, "9-12": ov_9_12, "9-14": ov_9_14, "9-15": ov_9_15,
    "9-17": ov_9_17, "9-18": ov_9_18, "9-19": ov_9_19, "10-2": ov_10_2, "10-4": ov_10_4,
    "10-6": ov_10_6, "10-7": ov_10_7, "10-9": ov_10_9, "10-14": None, "10-15": None,
    "10-16": ov_10_16, "10-17": ov_10_17, "10-19": ov_10_19, "11-2": ov_11_2,
    "11-7": ov_11_7, "11-17": ov_11_17,
}

# 10-14(A/C特性曲線)・10-15(音圧レベル直線)は軸テンプレが10-7と同一。専用overlay:
def ov_10_14():  # A特性(中音域持ち上げ低音落とす)+C特性(ほぼ平坦)。軸原点(140,485)
    A = lambda x: 300 - 150 * math.exp(-((x - 560) / 180) ** 2) + 0.28 * max(0, 560 - x)
    C = lambda x: 300 - 20 * math.exp(-((x - 540) / 260) ** 2)
    return (curve(lambda x: min(470, A(x)), 150, 880, stroke=RED, w=2.8)
            + curve(C, 150, 880, stroke=NAVY, w=2.6, dash="7 5")
            + txt(640, 180, "A特性(赤): 中音域↑・低音↓", 14, RED, "start", "bold")
            + txt(640, 210, "C特性(紺): 広帯域でほぼ平坦", 14, NAVY, "start", "bold"))

def ov_10_15():  # L=20log10(p/p0) 直線。軸原点(140,485)
    f = lambda x: 485 - 350 * (x - 140) / 750
    return (curve(f, 140, 870, stroke=NAVY, w=2.8)
            + txt(560, 300, "L = 20·log₁₀(p / p₀)", 16, RED, "middle", "bold")
            + txt(560, 330, "対数目盛上では直線 → 音圧pからLを読み取る", 13, NAVY, "middle"))

OVERLAYS["10-14"] = ov_10_14
OVERLAYS["10-15"] = ov_10_15

def inject(svg, overlay):
    out = svg.replace('<g id="answer-overlay"/>', '<g id="answer-overlay">%s</g>' % overlay)
    if out == svg:  # 自己閉じでない場合に対応
        out = re.sub(r'(<g id="answer-overlay"[^>]*>)', r'\1' + overlay.replace('\\', '\\\\'), svg, count=1)
    assert out != svg, "answer-overlay anchor not found"
    return out

def render(path):
    key = os.path.basename(path)[:-4]
    s = open(path, encoding="utf-8").read()
    m = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', s)
    w, h = (int(float(m.group(1))), int(float(m.group(2)))) if m else (1000, 600)
    os.makedirs(OUT, exist_ok=True); out = os.path.join(OUT, key + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--user-data-dir=" + PROF, "--default-background-color=FFFFFFFF", "--force-device-scale-factor=2",
                    "--screenshot=" + out, "--window-size=%d,%d" % (w, h),
                    os.path.abspath(path).replace("\\", "/")], capture_output=True)
    return os.path.exists(out) and os.path.getsize(out) > 0

def scan():
    pat = re.compile(r'<text[^>]*>([^<]*)</text>'); miss = {}
    for f in sorted(glob.glob(os.path.join(SVGDIR, "*.svg"))):
        if os.path.basename(f).endswith("-ans.svg"): continue
        for s in pat.findall(open(f, encoding="utf-8").read()):
            s = s.strip()
            if s and not re.search(r'[ぁ-んァ-ヶ一-龥]', s) and re.search(r'[A-Za-z]{4,}', s) and s not in TRANS:
                miss[s] = miss.get(s, 0) + 1
    for s, c in sorted(miss.items(), key=lambda kv: -kv[1]): print("%3d  %s" % (c, s))
    print("--- 未訳 %d 種 ---" % len(miss))

def build(chap=None):
    ok = ans = 0
    for f in sorted(glob.glob(os.path.join(SVGDIR, "*.svg"))):
        b = os.path.basename(f)[:-4]
        if b.endswith("-ans"): continue
        if chap and not b.startswith(chap + "-"): continue
        svg = apply_trans(open(f, encoding="utf-8").read())
        open(f, "w", encoding="utf-8").write(svg)  # 日本語化を原本へ反映
        if render(f): ok += 1
        if b in OVERLAYS and OVERLAYS[b]:
            ap = os.path.join(SVGDIR, "%s-ans.svg" % b)
            open(ap, "w", encoding="utf-8").write(inject(svg, OVERLAYS[b]()))
            if render(ap): ans += 1
    print("[build%s] 日本語化+PNG %d枚 / 回答後 %d枚 → %s" % (" " + chap if chap else "", ok, ans, OUT))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a and a[0] == "scan": scan()
    elif a and a[0] == "build": build(a[1] if len(a) > 1 else None)
    else: print("usage: vib2_overlay.py [scan | build [章番号]]")
