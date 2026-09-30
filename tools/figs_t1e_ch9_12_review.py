# -*- coding: utf-8 -*-
"""熱流体1級 混相流 ch9-12 第2次公開前レビュー用の図(t1e9*/t1e10*/t1e11*/t1e12*)を再生成。
白地660x420。旧generatorが消失していたため、現存PNGの体裁を踏襲して指摘点のみ修正。
条件図(回答前=required/preFigureImage)には結論・答えを描かない。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

LBLUE = (226, 238, 250)   # 淡い液体背景
BUBBLE = (222, 235, 250)  # 気泡の淡色


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def qbez(A, C, B, n=40):
    """2次ベジェ A->B(制御点C)の点列。"""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * A[0] + 2 * (1 - t) * t * C[0] + t * t * B[0]
        y = (1 - t) ** 2 * A[1] + 2 * (1 - t) * t * C[1] + t * t * B[1]
        pts.append((x, y))
    return pts


def hatch_bar(d, x1, y1, x2, y2, col=RED, wd=2, step=12):
    """横線ハッチの矩形棒(y1<y2 で上端y1)。"""
    d.rectangle((x1, y1, x2, y2), outline=col, width=wd)
    yy = y1 + step
    while yy < y2:
        d.line((x1 + 2, yy, x2 - 2, yy), fill=col, width=1)
        yy += step


# ============================================================
# 9-2  t1e9DimensionalGroups (required・回答前)
#   π定理の計算ルール(解法ヒント)を削除し、目的量Vの行を追加。次元表のみ。
# ============================================================
def t1e9DimensionalGroups():
    im, d = new(); title(d, "終端速度を支配する物理量と基本次元 (MLT系)")
    x0, y0 = 95, 66
    wlab, wcol = 232, 88
    rows = [
        ("V (終端速度)", "0", "1", "-1"),
        ("d (気泡径)", "0", "1", "0"),
        ("ρL (液密度)", "1", "-3", "0"),
        ("μL (粘性)", "1", "-1", "-1"),
        ("σ (界面張力)", "1", "0", "-2"),
        ("Δρg (浮力)", "1", "-2", "-2"),
    ]
    header = ("物理量", "M", "L", "T")
    rh = 45
    nR = len(rows) + 1
    x1 = x0 + wlab + 3 * wcol
    y1 = y0 + nR * rh
    # 外枠と罫線
    for i in range(nR + 1):
        d.line((x0, y0 + i * rh, x1, y0 + i * rh), fill=BLACK, width=2)
    xs = [x0, x0 + wlab, x0 + wlab + wcol, x0 + wlab + 2 * wcol, x1]
    for xv in xs:
        d.line((xv, y0, xv, y1), fill=BLACK, width=2)
    # ヘッダ
    ctext(d, x0 + 14, y0 + rh / 2, header[0], FS, BLACK, "lm")
    for j in range(3):
        ctext(d, xs[j + 1] + wcol / 2, y0 + rh / 2, header[j + 1], FS, BLACK)
    # 行(Vは強調=青)
    for r, row in enumerate(rows):
        yy = y0 + (r + 1) * rh + rh / 2
        col = BLUE if r == 0 else BLACK
        ctext(d, x0 + 14, yy, row[0], FS, col, "lm")
        for j in range(3):
            ctext(d, xs[j + 1] + wcol / 2, yy, row[j + 1], FS, col)
    note(d, "終端速度Vと、それを支配する物理量のMLT次元")
    save(im, "t1e9DimensionalGroups")


# ============================================================
# 9-12  Chisholm 二相増倍  前(pre=高さ比較不可) / 後(≈300kPa)
# ============================================================
def _chisholm_base(d):
    oy = 352
    arrow(d, 92, oy, 615, oy, BLACK, 2, 11)
    arrow(d, 92, oy, 92, 95, BLACK, 2, 11)
    ctext(d, 84, 90, "ΔP", FS, BLACK, "rm")
    cx = {"LO": 175, "GO": 335, "TP": 495}
    bw = 74
    ctext(d, cx["LO"], oy + 18, "液相のみ LO", FT, BLACK)
    ctext(d, cx["GO"], oy + 18, "気相のみ GO", FT, BLACK)
    ctext(d, cx["TP"], oy + 18, "二相 TP", FT, BLACK)
    ctext(d, 355, 118, "ΦL² = ΔP_TP / ΔP_LO", FT, GRAY)
    ctext(d, 355, 140, "X² = ΔP_LO / ΔP_GO", FT, LGRAY)
    return oy, cx, bw


def t1e9ChisholmMultiplierPre():
    im, d = new(); title(d, "同一管の圧力損失:液相のみ/気相のみ/二相 (回答前)")
    oy, cx, bw = _chisholm_base(d)
    sc = 1.9  # kPa->px (100kPa=190px)
    # LO=100, GO=1 は実高、TP は不定(高さ比較不可)
    d.rectangle((cx["LO"] - bw / 2, oy - 100 * sc, cx["LO"] + bw / 2, oy), outline=BLACK, width=2, fill=BLUE)
    ctext(d, cx["LO"], oy - 100 * sc - 16, "100 kPa", FS, BLUE)
    d.rectangle((cx["GO"] - bw / 2, oy - max(1 * sc, 4), cx["GO"] + bw / 2, oy), outline=BLACK, width=2, fill=GREEN)
    ctext(d, cx["GO"], oy - 22, "1 kPa", FS, GREEN)
    # TP: 破線の側辺 + ジグザグの破断上端(=高さ不明)+ ?
    xl, xr = cx["TP"] - bw / 2, cx["TP"] + bw / 2
    ytop = 175
    dashed(d, xl, oy, xl, ytop, RED, 2, 8, 6)
    dashed(d, xr, oy, xr, ytop, RED, 2, 8, 6)
    zig = []
    for i in range(9):
        zig.append((xl + (xr - xl) * i / 8, ytop + (10 if i % 2 else -10)))
    d.line(zig, fill=RED, width=2)
    ctext(d, cx["TP"], ytop - 30, "?", F, RED)
    ctext(d, cx["TP"], 150, "(高さは不定)", FT, RED)
    note(d, "二相の圧力損失ΔP_TPは未知。棒の高さは他と比較しない")
    save(im, "t1e9ChisholmMultiplierPre")


def t1e9ChisholmMultiplier():
    im, d = new(); title(d, "同一管の圧力損失:液相のみ/気相のみ/二相 (回答後)")
    oy, cx, bw = _chisholm_base(d)
    sc = 0.80  # kPa->px (300kPa=240px, 100kPa=80px)
    d.rectangle((cx["LO"] - bw / 2, oy - 100 * sc, cx["LO"] + bw / 2, oy), outline=BLACK, width=2, fill=BLUE)
    ctext(d, cx["LO"], oy - 100 * sc - 16, "100 kPa", FS, BLUE)
    d.rectangle((cx["GO"] - bw / 2, oy - max(1 * sc, 4), cx["GO"] + bw / 2, oy), outline=BLACK, width=2, fill=GREEN)
    ctext(d, cx["GO"], oy - 22, "1 kPa", FS, GREEN)
    hatch_bar(d, cx["TP"] - bw / 2, oy - 300 * sc, cx["TP"] + bw / 2, oy, RED, 2, 12)
    ctext(d, cx["TP"], oy - 300 * sc - 16, "≈300 kPa", FS, RED)
    ctext(d, 355, 162, "X=10 → ΦL²≈3.0", FT, RED)
    note(d, "ΦL²=1+20/X+1/X²≈3.0, ΔP_TP=ΦL²·ΔP_LO≈300kPa (LOより高い)")
    save(im, "t1e9ChisholmMultiplier")


# ============================================================
# 9-13  t1e9EinsteinViscosity (helpful・回答後)
#   清浄気泡=1+α を主線・切片1、剛体球=1+2.5α を破線で区別併記。
# ============================================================
def t1e9EinsteinViscosity():
    im, d = new(); title(d, "見かけ分子粘性の増加 (清浄気泡は 1+α)")
    ox, oy, xl, yl = 110, 350, 470, 250
    vmax = 3.0
    arrow(d, ox, oy, ox + xl + 18, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "α", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 12, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 14, "μeff / μ", FS, BLACK, "rm")

    def X(a): return ox + (a / 0.4) * xl
    def Y(v): return oy - (v / vmax) * yl
    # 切片1の目印
    dashed(d, ox, Y(1.0), X(0.4), Y(1.0), LGRAY, 1, 6, 5)
    ctext(d, ox - 12, Y(1.0), "1", FT, GRAY, "rm")
    # 剛体球 1+2.5α (破線・区別用)
    dashed(d, X(0), Y(1.0), X(0.4), Y(1 + 2.5 * 0.4), GRAY, 2, 10, 6)
    ctext(d, X(0.30), Y(1 + 2.5 * 0.30) + 4, "剛体球: 1 + 2.5α", FT, GRAY, "lm")
    # 清浄気泡 1+α (主線・青)
    d.line((X(0), Y(1.0), X(0.4), Y(1 + 0.4)), fill=BLUE, width=3)
    node(d, X(0), Y(1.0), 5, fill=BLUE, col=BLUE)
    ctext(d, X(0.20), Y(1 + 0.20) - 16, "清浄気泡: μeff/μ = 1 + α", FS, BLUE, "lm")
    note(d, "分子粘性はボイド率αとともに増加(清浄気泡は係数~1)。渦粘性は条件依存で一意でない")
    save(im, "t1e9EinsteinViscosity")


# ============================================================
# 9-14  t1e9VanDerWaalsSound (helpful・回答後)
#   接線の傾きラベルを (∂p/∂ρ)_T = Cs²/γ に修正。
# ============================================================
def t1e9VanDerWaalsSound():
    im, d = new(); title(d, "ファンデルワールス等温線と音速² (接線の傾き)")
    ox, oy, xl, yl = 108, 350, 472, 250
    pmax = 0.6

    def P(x): return x / (1 - 0.8 * x) - 3.5 * x * x + 0.15
    def X(x): return ox + x * xl
    def Y(p): return oy - (p / pmax) * yl
    arrow(d, ox, oy, ox + xl + 18, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "ρ", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 12, BLACK, 2, 11)
    ctext(d, ox - 10, oy - yl - 14, "p", FS, BLACK, "rm")
    curve = [(X(0.03 + 0.94 * i / 200), Y(P(0.03 + 0.94 * i / 200))) for i in range(201)]
    d.line(curve, fill=BLUE, width=3, joint="curve")
    # 接線(右側の急上昇枝)
    x0 = 0.83
    p0 = P(x0)
    slope = 1 / (1 - 0.8 * x0) ** 2 - 7 * x0
    dx = 0.13
    ax, ay = X(x0 - dx), Y(p0 - slope * dx)
    bx, by = X(x0 + dx), Y(p0 + slope * dx)
    d.line((ax, ay, bx, by), fill=RED, width=3)
    node(d, X(x0), Y(p0), 6, fill=RED, col=RED)
    ctext(d, X(0.34), Y(0.30), "傾き (∂p/∂ρ)_T = Cs²/γ", FS, RED, "lm")
    note(d, "斥力項 1/(1-ρb) と 引力項 aρ² の寄与。音速 Cs²=γ(∂p/∂ρ)_T")
    save(im, "t1e9VanDerWaalsSound")


# ============================================================
# 10-10  t1e10HistoryForce (helpful・回答後)
#   履歴力の矢印を「上向き」→「左向き(=右向き加速に対抗)」へ。
# ============================================================
def t1e10HistoryForce():
    im, d = new(); title(d, "加速運動する分散要素に働く履歴力 (Basset力)")
    ys = 210
    cxs = [110, 250, 390, 530]
    r = 26
    for i, cx in enumerate(cxs):
        d.ellipse((cx - r, ys - r, cx + r, ys + r), outline=BLACK, width=2, fill=FILL1)
        if i < 3:
            arrow(d, cxs[i] + r + 6, ys, cxs[i + 1] - r - 6, ys, GRAY, 2, 10)
    # 速度(加速=増加)を示す青矢印
    vlen = [26, 40, 56, 74]
    for cx, vl in zip(cxs, vlen):
        arrow(d, cx - vl / 2, ys + 52, cx + vl / 2, ys + 52, BLUE, 3, 10)
    ctext(d, 320, ys + 78, "速度が増加(加速運動) →", FT, BLUE)
    # 時間軸
    arrow(d, 70, ys + 118, 590, ys + 118, BLACK, 2, 11)
    ctext(d, 330, ys + 138, "時間 t →", FT, BLACK)
    # 履歴力(3個目):左向き(加速方向に対抗)
    arrow(d, cxs[2] - r - 2, ys - 34, cxs[2] - r - 78, ys - 34, RED, 4, 15)
    ctext(d, cxs[2] - 46, ys - 58, "履歴力", F, RED)
    note(d, "過去の運動履歴が現在の力に及ぶ。加速に対抗する向き。粘度に依存・密度に直接依存しない")
    save(im, "t1e10HistoryForce")


# ============================================================
# 10-13  t1e10EnergyDissipation (helpful・回答後)
#   終端速度Uの矢印を「下向き」→「上向き(気泡は上昇)」へ。
# ============================================================
def t1e10EnergyDissipation():
    im, d = new(); title(d, "終端速度で上昇する気泡のエネルギ収支")
    d.rectangle((55, 60, 605, 380), outline=(150, 170, 200), width=2, fill=LBLUE)
    ctext(d, 78, 82, "静止液 (ρ)", FT, GRAY, "lm")
    bx, by, br = 255, 245, 56
    d.ellipse((bx - br, by - br, bx + br, by + br), outline=BLACK, width=3, fill="white")
    ctext(d, bx, by, "気泡 V", FS, BLACK)
    # 浮力(上)
    arrow(d, bx, by - br - 4, bx, by - br - 78, RED, 4, 15)
    ctext(d, bx + 20, by - br - 70, "浮力", F, RED, "lm")
    # 終端速度 U(上向き)
    arrow(d, 455, by + 40, 455, by - 80, GRAY, 3, 12)
    ctext(d, 475, by - 20, "終端速度 U", FT, GRAY, "lm")
    note(d, "解放される位置エネルギの割合 ρgUV = 流れ場全体の粘性散逸率 Ed")
    save(im, "t1e10EnergyDissipation")


# ============================================================
# 11-11  t1e11YoungContactAngle (required・回答前)
#   固体面の張力ラベルを入替:左向き=σSG、右向き=σSL(ヤング式と一致)。
# ============================================================
def t1e11YoungContactAngle():
    im, d = new(); title(d, "固体面上の液滴とヤングの式")
    sy = 300
    # 固体面(ハッチ)
    d.line((70, sy, 590, sy), fill=BLACK, width=3)
    for x in range(90, 590, 34):
        d.line((x, sy, x - 16, sy + 16), fill=BLACK, width=2)
    ctext(d, 560, sy + 16, "固体", FS, BLACK, "lm")
    # 接触点と液滴(右側に張り出す弧)
    cpx = 210
    node(d, cpx, sy, 5, fill=RED, col=RED)
    apex = (335, 168)
    end = (460, sy)
    d.line(qbez((cpx, sy), apex, end, 48), fill=BLUE, width=3, joint="curve")
    ctext(d, 380, 214, "液滴", FS, BLUE, "lm")
    # 気液張力 σ(接線・右上)
    arrow(d, cpx, sy, cpx + 70, sy - 78, RED, 3, 12)
    ctext(d, cpx + 34, sy - 62, "σ(気液)", FT, RED, "lm")
    # 接触角
    ctext(d, cpx + 26, sy - 18, "θY", FT, GRAY, "lm")
    # 固体面の張力:左=σSG、右=σSL(入替済)
    arrow(d, cpx - 6, sy, cpx - 70, sy, BLACK, 2, 11)
    ctext(d, cpx - 78, sy + 16, "σSG", FT, BLACK)
    arrow(d, cpx + 6, sy, cpx + 70, sy, BLACK, 2, 11)
    ctext(d, cpx + 74, sy + 16, "σSL", FT, BLACK)
    note(d, "ヤングの式: σSG - σSL = σ cosθY", y=H - 24)
    save(im, "t1e11YoungContactAngle")


# ============================================================
# 11-12  t1e11ContactAngleHysteresis (helpful・回答後)
#   右上がり板 → 下り勾配は左。滑落矢印を左下へ、左=前進(θf大)/右=後退(θb小)。
# ============================================================
def t1e11ContactAngleHysteresis():
    im, d = new(); title(d, "接触角ヒステリシス (前進角・後退角)")
    # 右上がりの板
    A, B = (70, 356), (486, 208)

    def onplate(t): return (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)
    d.line((A[0], A[1], B[0], B[1]), fill=BLACK, width=4)
    # ハッチ(板の下)
    for t in [i / 12 for i in range(13)]:
        px, py = onplate(t)
        d.line((px, py, px - 12, py + 18), fill=BLACK, width=2)
    # 液滴(板上の弧)
    cL = onplate(0.36)   # 下側=左(前進側)
    cR = onplate(0.60)   # 上側=右(後退側)
    nx, ny = -0.335, -0.942  # 板法線(上向き左寄り)
    mid = ((cL[0] + cR[0]) / 2, (cL[1] + cR[1]) / 2)
    apex = (mid[0] + nx * 70, mid[1] + ny * 70)
    ctrl = (2 * apex[0] - mid[0], 2 * apex[1] - mid[1])
    d.line(qbez(cL, ctrl, cR, 48), fill=BLUE, width=3, joint="curve")
    ctext(d, apex[0] + 6, apex[1] - 10, "液滴", FT, BLUE, "lm")
    node(d, cL[0], cL[1], 4, fill=RED, col=RED)
    node(d, cR[0], cR[1], 4, fill=RED, col=RED)
    # ラベル:左下=前進(θf大)、右上=後退(θb小)
    ctext(d, cL[0] - 96, cL[1] + 24, "下側=前進角 θf(大)", FT, BLACK, "lm")
    ctext(d, cR[0] + 8, cR[1] - 26, "上側=後退角 θb(小)", FT, BLACK, "lm")
    # 滑落:板に沿って左下へ
    s0 = onplate(0.30)
    s1 = onplate(0.10)
    arrow(d, s0[0], s0[1] + 30, s1[0], s1[1] + 30, RED, 3, 13)
    ctext(d, (s0[0] + s1[0]) / 2, (s0[1] + s1[1]) / 2 + 50, "滑落", FS, RED)
    # 参照:静止(水平面)
    rx, ry = 545, 350
    d.line((rx - 45, ry, rx + 45, ry), fill=BLACK, width=3)
    for x in range(int(rx - 40), int(rx + 45), 14):
        d.line((x, ry, x - 10, ry + 12), fill=BLACK, width=2)
    d.line(qbez((rx - 32, ry), (rx, ry - 44), (rx + 32, ry), 32), fill=GREEN, width=2, joint="curve")
    ctext(d, rx, ry - 54, "静止 θ", FT, GREEN)
    note(d, "滑落中は θb(後退・上側) < θ < θf(前進・下側)")
    save(im, "t1e11ContactAngleHysteresis")


# ============================================================
# 12-1  界面積濃度  前(pre=定義のみ) / 後(結論つき)
# ============================================================
_BUBBLES = [(95, 130, 15), (150, 115, 12), (205, 140, 17), (255, 120, 13),
            (300, 150, 15), (115, 190, 13), (170, 205, 18), (225, 195, 12),
            (285, 210, 16), (120, 260, 14), (180, 270, 12), (240, 255, 17),
            (300, 275, 13), (150, 320, 16), (215, 330, 12), (275, 325, 15)]


def _iac_common(d):
    # 左:検査体積の箱と気泡群
    bx0, by0, bx1, by1 = 60, 78, 350, 372
    d.rectangle((bx0, by0, bx1, by1), outline=BLACK, width=2)
    ctext(d, (bx0 + bx1) / 2, by0 + 18, "検査体積 V", FT, BLACK)
    for (cx, cy, r) in _BUBBLES:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLUE, width=2, fill=BUBBLE)
    ctext(d, (bx0 + bx1) / 2, by1 - 16, "気相体積率 α = 気相体積 / V", FT, GRAY)
    # 右:単一球
    ccx, ccy, cr = 495, 160, 74
    d.ellipse((ccx - cr, ccy - cr, ccx + cr, ccy + cr), outline=BLUE, width=2, fill=BUBBLE)
    ctext(d, ccx, ccy, "直径 d", FS, BLACK)
    ctext(d, 500, 258, "球1個: 体積 πd³/6 , 表面積 πd²", FT, BLACK)
    ctext(d, 500, 292, "界面積濃度 a_int = 6α / d  [1/m]", FS, BLUE)


def t1e12InterfacialAreaConcPre():
    im, d = new(); title(d, "球形気泡群の界面積濃度 (回答前)")
    _iac_common(d)
    save(im, "t1e12InterfacialAreaConcPre")


def t1e12InterfacialAreaConc():
    im, d = new(); title(d, "球形気泡群の界面積濃度 (回答後)")
    _iac_common(d)
    ctext(d, 500, 324, "α 大・d 小 ほど a_int 大", FT, GRAY)
    save(im, "t1e12InterfacialAreaConc")


# ============================================================
if __name__ == "__main__":
    t1e9DimensionalGroups()
    t1e9ChisholmMultiplierPre()
    t1e9ChisholmMultiplier()
    t1e9EinsteinViscosity()
    t1e9VanDerWaalsSound()
    t1e10HistoryForce()
    t1e10EnergyDissipation()
    t1e11YoungContactAngle()
    t1e11ContactAngleHysteresis()
    t1e12InterfacialAreaConcPre()
    t1e12InterfacialAreaConc()
    print("done ch9-12 review figures")
