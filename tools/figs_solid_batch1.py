# -*- coding: utf-8 -*-
"""Phase2 Batch1: 図なし14問へ後付けする図。
fem-basics 第4章(fem4*)/numerical-basics 第6章(num6*)/element-tech 第7章(elem7*)。
白地660x420・黒線画・機構/概念のみ(答えの数値は焼き込まない)。すべて helpful(回答後表示)。
JSON配線は別途。ここでは assets/figures/<key>.png を生成するのみ。"""
import sys, math, os
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


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


# ============================================================
# fem-basics 第4章
# ============================================================
def fem4Galerkin():
    im, d = new(); title(d, "ガラーキン法:重み関数=形状関数→対称剛性")
    d.rectangle((55, 150, 250, 240), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 152, 178, "重み関数 w", FS, BLACK)
    ctext(d, 152, 212, "= 形状関数 N_i", FS, BLUE)
    arrow(d, 255, 195, 320, 195, BLACK, 3, 13)
    vals = [["k11", "k12", "k13"], ["k12", "k22", "k23"], ["k13", "k23", "k33"]]
    matrix_grid(d, 345, 118, vals, cell=68, fnt=FT)
    d.line((345, 118, 345 + 3 * 68, 118 + 3 * 68), fill=RED, width=2)
    ctext(d, 345 + 102, 118 + 204 + 20, "対角で対称  K_ij = K_ji", FT, RED)
    note(d, "重みと試験関数を同じにとると剛性行列が対称になり、変分原理と整合する。")
    save(im, "fem4Galerkin")


def fem4DispVsForce():
    im, d = new(); title(d, "変位法(剛性法)と応力法(力法)")
    d.rectangle((55, 78, 320, 358), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((350, 78, 610, 358), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 187, 106, "変位法(剛性法)", FS, BLUE)
    ctext(d, 480, 106, "応力法(力法)", FS, RED)
    ctext(d, 187, 158, "未知数 = 節点変位 {d}", FT, BLACK)
    ctext(d, 187, 196, "[K]{d} = {f} を解く", FT, BLACK)
    ctext(d, 187, 234, "応力は後から計算", FT, GRAY)
    ctext(d, 187, 300, "汎用FEMの主流", FS, BLUE)
    ctext(d, 187, 330, "(プログラム化しやすい)", FT, GRAY)
    ctext(d, 480, 158, "未知数 = 力・応力", FT, BLACK)
    ctext(d, 480, 196, "(不静定力)", FT, BLACK)
    ctext(d, 480, 234, "不静定次数↑で", FT, GRAY)
    ctext(d, 480, 264, "手間が急増", FT, GRAY)
    ctext(d, 480, 320, "汎用FEMでは非主流", FS, RED)
    note(d, "変位法は節点変位、応力法は力を未知数にとる。汎用FEMの主流は変位法。")
    save(im, "fem4DispVsForce")


def fem4VirtualWork():
    im, d = new(); title(d, "仮想仕事の原理:外部仮想仕事=内部仮想仕事")
    wall(d, 90, 155, 300, side=1, n=8)
    d.rectangle((90, 185, 330, 270), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 210, 227, "平衡状態の物体", FT, GRAY)
    force(d, 330, 227, 62, 0, "P", RED)
    # 仮想変位(破線)
    dashed(d, 90, 185, 356, 191, BLUE, 2)
    dashed(d, 90, 270, 356, 276, BLUE, 2)
    dashed(d, 356, 191, 356, 276, BLUE, 2)
    arrow(d, 300, 305, 352, 305, BLUE, 2, 10)
    ctext(d, 358, 305, "δu(仮想変位)", FT, BLUE, "lm")
    ctext(d, 330, 348, "δW_ext(外力) = δW_int(内力)", FS, BLACK)
    note(d, "平衡なら、拘束を満たす任意の微小な仮想変位δuで外力仕事=内部仕事となる。")
    save(im, "fem4VirtualWork")


def fem4WeakForm():
    im, d = new(); title(d, "強形式→弱形式(仮想仕事)")
    d.rectangle((70, 74, 590, 150), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 100, "強形式(微分形)", FS, BLACK)
    ctext(d, 330, 130, "領域内の平衡方程式 ＋ 力の境界条件", FT, GRAY)
    arrow(d, 330, 153, 330, 205, BLACK, 3, 14)
    ctext(d, 344, 179, "重み関数×領域積分 ＋ 部分積分", FT, BLUE, "lm")
    d.rectangle((70, 210, 590, 322), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 238, "弱形式(積分形)", FS, BLUE)
    ctext(d, 330, 270, "∫σδε dV = ∫b δu dV + ∫t δu dS", FT, BLACK)
    ctext(d, 330, 300, "内部仮想仕事 = 外部仮想仕事", FT, GRAY)
    note(d, "仮想仕事の原理は、平衡方程式と力の境界条件を弱形式(積分形)にまとめたもの。")
    save(im, "fem4WeakForm")


def fem4GalerkinVW():
    im, d = new(); title(d, "ガラーキン法と仮想仕事の原理は一致する")
    ys = [60, 130, 200, 270]
    texts = ["平衡方程式の残差 R に重み関数 w を掛け領域積分",
             "重み関数 w = 仮想変位 δu と読み替える",
             "部分積分して微分の階数を1つ下げる",
             "内部仮想仕事∫σδε dV ＋ 表面力の境界項∫t δu dS"]
    fills = [FILL1, FILL1, FILL1, FILL2]
    for y, t, f in zip(ys, texts, fills):
        d.rectangle((65, y, 595, y + 46), outline=BLACK, width=3, fill=f)
        ctext(d, 330, y + 23, t, FT, BLACK)
        if y != ys[-1]:
            arrow(d, 330, y + 46, 330, y + 68, BLACK, 3, 12)
    ctext(d, 330, ys[-1] + 46 + 18, "→ 仮想仕事の原理そのもの", FT, RED)
    note(d, "残差×重み(=仮想変位)を部分積分すると、仮想仕事の式に一致する。")
    save(im, "fem4GalerkinVW")


def fem4StrainDisp():
    im, d = new(); title(d, "2次元ひずみの幾何学的意味")
    s = 72; oy = 148

    def sq(ox):
        d.rectangle((ox, oy, ox + s, oy + s), outline=GRAY, width=2)

    # εx : x方向の伸び
    ox = 95; sq(ox)
    dashed(d, ox, oy, ox, oy + s, BLUE, 2)
    dashed(d, ox, oy + s, ox + s + 22, oy + s, BLUE, 2)
    dashed(d, ox + s + 22, oy + s, ox + s + 22, oy, BLUE, 2)
    dashed(d, ox + s + 22, oy, ox, oy, BLUE, 2)
    arrow(d, ox + s - 2, oy - 14, ox + s + 22, oy - 14, RED, 3, 9)
    ctext(d, ox + s / 2, oy + s + 34, "εx", F, RED)
    ctext(d, ox + s / 2, oy + s + 62, "x方向の伸び", FT, BLACK)

    # εy : y方向の伸び
    ox = 290; sq(ox)
    dashed(d, ox, oy, ox, oy + s + 22, BLUE, 2)
    dashed(d, ox, oy + s + 22, ox + s, oy + s + 22, BLUE, 2)
    dashed(d, ox + s, oy + s + 22, ox + s, oy, BLUE, 2)
    dashed(d, ox + s, oy, ox, oy, BLUE, 2)
    arrow(d, ox - 14, oy + s - 2, ox - 14, oy + s + 22, RED, 3, 9)
    ctext(d, ox + s / 2, oy + s + 34, "εy", F, RED)
    ctext(d, ox + s / 2, oy + s + 62, "y方向の伸び", FT, BLACK)

    # γxy : 直角の崩れ(せん断)
    ox = 485; sq(ox)
    dashed(d, ox, oy + s, ox + s, oy + s, BLUE, 2)
    dashed(d, ox, oy + s, ox + 22, oy, BLUE, 2)
    dashed(d, ox + 22, oy, ox + s + 22, oy, BLUE, 2)
    dashed(d, ox + s, oy + s, ox + s + 22, oy, BLUE, 2)
    angle_arc(d, ox, oy + s, 26, 48, 90, "γ", RED)
    ctext(d, ox + s / 2, oy + s + 34, "γxy", F, RED)
    ctext(d, ox + s / 2, oy + s + 62, "直角の崩れ", FT, BLACK)

    note(d, "垂直ひずみは各方向の伸び、せん断ひずみは直角の崩れとして生じる。")
    save(im, "fem4StrainDisp")


# ============================================================
# numerical-basics 第6章
# ============================================================
def num6HighOrderInteg():
    im, d = new(); title(d, "はり・シェルの曲げ応力評価と積分点")
    bx, by0, by1, bw = 150, 110, 330, 60
    d.rectangle((bx, by0, bx + bw, by1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, bx + bw / 2, by0 - 16, "板厚断面", FT, GRAY)
    cy = (by0 + by1) / 2
    dashed(d, bx - 10, cy, bx + bw + 210, cy, GRAY, 2)
    ctext(d, bx + bw + 216, cy, "中立軸", FT, GRAY, "lm")
    # ガウス点(内部)
    gx = bx + 18
    for f in (0.21, 0.79):
        node(d, gx, by0 + (by1 - by0) * f, 5, fill=BLUE, col=BLUE)
    # ニュートン・コーツ点(両端=表面を含む)
    ncx = bx + 42
    for f in (0.0, 0.5, 1.0):
        node(d, ncx, by0 + (by1 - by0) * f, 5, fill=GREEN, col=GREEN)
    # 曲げ応力の直線分布(表面で最大)
    sx = bx + bw + 14
    d.line((sx, by0, sx + 95, by0), fill=RED, width=2)
    d.line((sx, cy, sx + 95, by0), fill=RED, width=2)
    d.line((sx, by1, sx + 95, by1), fill=RED, width=2)
    d.line((sx, cy, sx + 95, by1), fill=RED, width=2)
    d.line((sx, by0, sx, by1), fill=RED, width=1)
    ctext(d, sx + 48, by0 - 16, "圧縮", FT, RED)
    ctext(d, sx + 48, by1 + 16, "引張", FT, RED)
    # 凡例
    node(d, 120, 358, 5, fill=BLUE, col=BLUE)
    ctext(d, 132, 358, "ガウス点(内部)", FT, BLUE, "lm")
    node(d, 330, 358, 5, fill=GREEN, col=GREEN)
    ctext(d, 342, 358, "N-コーツ点(表面含む)", FT, GREEN, "lm")
    note(d, "曲げ応力は板厚表面で最大。表面に積分点をもつN-コーツ公式が曲げ評価に有利。")
    save(im, "num6HighOrderInteg")


def num6LagrangeHermite():
    im, d = new(); title(d, "ラグランジュ補間とエルミート補間")
    # ラグランジュ(関数値のみ)
    axes(d, 80, 300, 210, 180, "x", "y")
    d.line([(110, 250), (145, 200), (180, 180), (215, 195), (250, 232)],
           fill=BLUE, width=3, joint="curve")
    for q in [(110, 250), (180, 180), (250, 232)]:
        node(d, q[0], q[1], 5, fill="white", col=BLUE)
    ctext(d, 180, 112, "ラグランジュ補間", FS, BLUE)
    ctext(d, 180, 326, "関数値だけを使用", FT, BLACK)
    ctext(d, 180, 350, "n点で n-1 次", FT, GRAY)
    # エルミート(関数値＋微係数)
    axes(d, 370, 300, 210, 180, "x", "y")
    d.line([(400, 250), (435, 205), (470, 180), (505, 200), (540, 232)],
           fill=GREEN, width=3, joint="curve")
    p2 = [(400, 250), (470, 180), (540, 232)]
    slopes = [(1, -0.7), (1, 0), (1, 0.7)]
    for q, sl in zip(p2, slopes):
        node(d, q[0], q[1], 5, fill="white", col=GREEN)
        L = math.hypot(sl[0], sl[1]) * 1.0
        ux, uy = sl[0] / L, sl[1] / L
        d.line((q[0] - 22 * ux, q[1] - 22 * uy, q[0] + 22 * ux, q[1] + 22 * uy),
               fill=RED, width=2)
    ctext(d, 470, 112, "エルミート補間", FS, GREEN)
    ctext(d, 470, 326, "関数値＋傾き(微係数)を使用", FT, BLACK)
    ctext(d, 470, 350, "n点で 2n-1 次", FT, GRAY)
    note(d, "ラグランジュは関数値のみ、エルミートは関数値と傾きの両方を用いる補間。")
    save(im, "num6LagrangeHermite")


# ============================================================
# element-tech 第7章
# ============================================================
def elem7SameDOF():
    im, d = new(); title(d, "総自由度が同じ:一次要素と高次要素")
    ly0 = 90
    # 一次・細かい分割
    lx0, cell, n = 60, 45, 4
    for i in range(n + 1):
        d.line((lx0, ly0 + i * cell, lx0 + n * cell, ly0 + i * cell), fill=BLACK, width=2)
        d.line((lx0 + i * cell, ly0, lx0 + i * cell, ly0 + n * cell), fill=BLACK, width=2)
    for i in range(n + 1):
        for j in range(n + 1):
            node(d, lx0 + j * cell, ly0 + i * cell, 3, fill=BLACK, col=BLACK)
    ctext(d, lx0 + n * cell / 2, ly0 + n * cell + 24, "一次要素・細かい分割", FT, BLUE)
    ctext(d, lx0 + n * cell / 2, ly0 + n * cell + 46, "(要素多・節点は角のみ)", FT, GRAY)
    # 高次・粗い分割
    rx0, rcell, m = 400, 90, 2
    for i in range(m + 1):
        d.line((rx0, ly0 + i * rcell, rx0 + m * rcell, ly0 + i * rcell), fill=BLACK, width=2)
        d.line((rx0 + i * rcell, ly0, rx0 + i * rcell, ly0 + m * rcell), fill=BLACK, width=2)
    for i in range(m + 1):
        for j in range(m + 1):
            node(d, rx0 + j * rcell, ly0 + i * rcell, 3, fill=BLACK, col=BLACK)
    for i in range(m + 1):
        for j in range(m):
            node(d, rx0 + j * rcell + rcell / 2, ly0 + i * rcell, 3, fill=RED, col=RED)
    for i in range(m):
        for j in range(m + 1):
            node(d, rx0 + j * rcell, ly0 + i * rcell + rcell / 2, 3, fill=RED, col=RED)
    ctext(d, rx0 + m * rcell / 2, ly0 + m * rcell + 24, "高次要素・粗い分割", FT, GREEN)
    ctext(d, rx0 + m * rcell / 2, ly0 + m * rcell + 46, "(要素少・辺中間に節点)", FT, GRAY)
    ctext(d, 320, 168, "総節点数", FT, RED)
    ctext(d, 320, 190, "ほぼ同じ", FT, RED)
    note(d, "総自由度をそろえると解析時間はほぼ同等、精度は高次要素が有利。")
    save(im, "elem7SameDOF")


def elem7RefineHole():
    im, d = new(); title(d, "応力集中部(円孔近傍)を細かく分割")
    x0, y0, x1, y1 = 130, 95, 555, 335
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, 48
    # 粗い背景格子
    for gx in range(int(x0) + 70, int(x1), 70):
        d.line((gx, y0, gx, y1), fill=LGRAY, width=1)
    for gy in range(int(y0) + 60, int(y1), 60):
        d.line((x0, gy, x1, gy), fill=LGRAY, width=1)
    # 円孔近傍の同心円+放射線(細分)
    for rr in (r + 18, r + 40, r + 64):
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=GRAY, width=1)
    for a in range(0, 360, 30):
        ar = math.radians(a)
        d.line((cx + r * math.cos(ar), cy + r * math.sin(ar),
                cx + (r + 64) * math.cos(ar), cy + (r + 64) * math.sin(ar)), fill=GRAY, width=1)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill="white")
    ctext(d, cx, cy, "円孔", FT, GRAY)
    ctext(d, cx, cy + r + 78, "近傍を細分", FT, RED)
    # 一様引張
    for yy in (y0 + 40, cy, y1 - 40):
        arrow(d, x0, yy, x0 - 36, yy, RED, 3, 10)
        arrow(d, x1, yy, x1 + 36, yy, RED, 3, 10)
    ctext(d, x0 - 42, y0 + 14, "引張", FT, RED, "rm")
    ctext(d, x1 + 42, y0 + 14, "引張", FT, RED, "lm")
    note(d, "応力こう配の大きい円孔近傍を細かく分割すると応力集中を精度よく捉えられる。")
    save(im, "elem7RefineHole")


def elem7CstBendMesh():
    im, d = new(); title(d, "定ひずみ三角形要素による片持ばりの曲げ")
    wall(d, 90, 130, 300, side=1, n=8)
    x0, y0, x1, y1 = 90, 150, 500, 285
    nx, ny = 8, 3
    cw = (x1 - x0) / nx; ch = (y1 - y0) / ny
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    for i in range(ny + 1):
        d.line((x0, y0 + i * ch, x1, y0 + i * ch), fill=GRAY, width=1)
    for j in range(nx + 1):
        d.line((x0 + j * cw, y0, x0 + j * cw, y1), fill=GRAY, width=1)
    for i in range(ny):
        for j in range(nx):
            d.line((x0 + j * cw, y0 + i * ch, x0 + (j + 1) * cw, y0 + (i + 1) * ch),
                   fill=GRAY, width=1)
    force(d, x1, y0 - 46, 0, 40, "W", RED)
    dim(d, x0, y1 + 30, x1, y1 + 30, "長手方向(要分割)", col=GRAY)
    dim(d, x1 + 28, y0, x1 + 28, y1, "高さ", col=GRAY)
    note(d, "要素内ひずみ一定のため、長手・高さ両方向に十分な分割が必要。")
    save(im, "elem7CstBendMesh")


def elem7CantPlate():
    im, d = new(); title(d, "片持ち板の面内曲げ(設定)")
    wall(d, 110, 130, 300, side=1, n=8)
    x0, y0, x1, y1 = 110, 155, 520, 275
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + x1) / 2, y0 - 18, "厚さ b = 1 mm(面外)", FT, GRAY)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2, "E = 2×10⁵ N/mm²", FT, GRAY)
    force(d, x1, y0 - 46, 0, 40, "W = 10 N", RED)
    dim(d, x0, y1 + 34, x1, y1 + 34, "L = 150 mm", col=GRAY)
    dim(d, x1 + 30, y0, x1 + 30, y1, "h = 20 mm", col=GRAY)
    note(d, "自由端に面内荷重 W=10 N。断面二次モーメント・理論たわみを求める設定。")
    save(im, "elem7CantPlate")


def elem7ElemBendRank():
    im, d = new(); title(d, "要素種類と曲げ変形の表現力")
    # 三角形(定ひずみ)
    tcx = 160
    d.polygon([(tcx - 45, 230), (tcx + 45, 230), (tcx, 150)], outline=BLACK, width=3, fill=FILL1)
    for p in [(tcx - 45, 230), (tcx + 45, 230), (tcx, 150)]:
        node(d, p[0], p[1], 4, fill=BLACK, col=BLACK)
    ctext(d, tcx, 252, "三角形(定ひずみ)", FT, BLUE)
    # 4節点四辺形
    for cx in (330, 500):
        s = 80; x = cx - s / 2; y = 150
        d.rectangle((x, y, x + s, y + s), outline=BLACK, width=3, fill=FILL1)
        for p in [(x, y), (x + s, y), (x, y + s), (x + s, y + s)]:
            node(d, p[0], p[1], 4, fill=BLACK, col=BLACK)
    ctext(d, 330, 252, "4節点四辺形", FT, BLUE)
    # 8節点四辺形の辺中間節点
    for p in [(500, 150), (500, 230), (460, 190), (540, 190)]:
        node(d, p[0], p[1], 4, fill=RED, col=RED)
    ctext(d, 500, 252, "8節点四辺形", FT, BLUE)
    # 柔軟性の軸
    arrow(d, 90, 300, 570, 300, BLACK, 3, 13)
    ctext(d, 110, 322, "剛い(たわみ小)", FT, GRAY, "lm")
    ctext(d, 550, 322, "正確(たわみ大)", FT, GRAY, "rm")
    for cx in (160, 330, 500):
        d.line((cx, 262, cx, 300), fill=GRAY, width=1)
    note(d, "曲げの柔らかさは 三角形 < 4節点 < 8節点。剛い要素ほど計算たわみは小さい。")
    save(im, "elem7ElemBendRank")


def elem7SquareDetJ():
    im, d = new(); title(d, "同一正方形要素の写像と剛性")
    lx, ly, ls = 90, 150, 120
    d.rectangle((lx, ly, lx + ls, ly + ls), outline=BLACK, width=3, fill=FILL1)
    ctext(d, lx + ls / 2, ly - 16, "局所座標", FT, GRAY)
    ctext(d, lx + ls / 2, ly + ls / 2, "-1≤ξ,η≤1", FT, BLACK)
    arrow(d, lx + ls + 12, ly + ls / 2, lx + ls + 78, ly + ls / 2, BLACK, 3, 13)
    ctext(d, lx + ls + 45, ly + ls / 2 - 16, "写像", FT, BLUE)
    rx, ry, rs = lx + ls + 90, 150, 120
    d.rectangle((rx, ry, rx + rs, ry + rs), outline=BLACK, width=3, fill=FILL1)
    ctext(d, rx + rs / 2, ry - 16, "全体座標", FT, GRAY)
    dim(d, rx, ry + rs + 22, rx + rs, ry + rs + 22, "一辺 a", col=GRAY)
    dim(d, rx + rs + 24, ry, rx + rs + 24, ry + rs, "a", col=GRAY)
    ctext(d, W / 2, 335, "同一寸法・同一形状の正方形 → 要素剛性は全要素で同じ", FT, RED)
    note(d, "ヤコビ行列式は要素内で一定・正。剛性は形状と寸法で決まり絶対位置に依存しない。")
    save(im, "elem7SquareDetJ")


ALL = [fem4Galerkin, fem4DispVsForce, fem4VirtualWork, fem4WeakForm, fem4GalerkinVW,
       fem4StrainDisp, num6HighOrderInteg, num6LagrangeHermite, elem7SameDOF,
       elem7RefineHole, elem7CstBendMesh, elem7CantPlate, elem7ElemBendRank, elem7SquareDetJ]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    keys = ["fem4Galerkin", "fem4DispVsForce", "fem4VirtualWork", "fem4WeakForm",
            "fem4GalerkinVW", "fem4StrainDisp", "num6HighOrderInteg", "num6LagrangeHermite",
            "elem7SameDOF", "elem7RefineHole", "elem7CstBendMesh", "elem7CantPlate",
            "elem7ElemBendRank", "elem7SquareDetJ"]
    miss = [k for k in keys if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(keys), "MISSING", miss)
