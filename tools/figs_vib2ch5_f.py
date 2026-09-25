# -*- coding: utf-8 -*-
"""振動2級 第5章「有限要素法の基礎」公式・用語カード用の図 26枚。接頭辞 v2f5。
白地660×420・黒線画（figlib準拠）。公式カード＝回答後の根拠図なので結果・式を描いてよい。
文字化け回避のためギリシャ文字は綴り（rho, mu, xi, eta, Pi, sigma, epsilon）で書く。
実行: python tools/figs_vib2ch5_f.py
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot,
                    F, FL, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN, ORANGE,
                    FILL1, FILL2, FILL3, W, H)


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=9):
    n = max(1, int(math.hypot(x2 - x1, y2 - y1) / seg))
    for k in range(n):
        if k % 2:
            continue
        t0, t1 = k / n, (k + 1) / n
        d.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=col, width=wd)


def block(d, cx, cy, w, h, label="", fnt=FS, fill=FILL1, col=BLACK):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=col, width=3, fill=fill)
    if label:
        ctext(d, cx, cy, label, fnt)


def curve_arrow(d, cx, cy, r, a0, a1, col=BLUE, wd=3, head=12):
    d.arc((cx - r, cy - r, cx + r, cy + r), -a1, -a0, fill=col, width=wd)
    A = math.radians(a1)
    ex, ey = cx + r * math.cos(A), cy - r * math.sin(A)
    ang = math.atan2(-math.cos(A), -math.sin(A))
    for s in (0.5, -0.5):
        d.line((ex, ey, ex - head * math.cos(ang - s), ey - head * math.sin(ang - s)),
               fill=col, width=wd)


def fillcell(d, x, y, cell, col):
    d.rectangle((x + 2, y + 2, x + cell - 2, y + cell - 2), fill=col)


def grid_lines(d, x, y, rows, cols, cell):
    for i in range(rows + 1):
        d.line((x, y + i * cell, x + cols * cell, y + i * cell), fill=BLACK, width=2)
    for j in range(cols + 1):
        d.line((x + j * cell, y, x + j * cell, y + rows * cell), fill=BLACK, width=2)


# ============================================================
# 公式・用語図 v2f5（26枚）
# ============================================================

def f_discretize():  # 1
    im, d = new(); title(d, "離散化解法（有限自由度への近似）")
    d.ellipse((80, 130, 230, 260), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 155, 195, "連続体", FS); ctext(d, 155, 280, "無限自由度", FT, GRAY)
    arrow(d, 245, 195, 330, 195, BLACK, 3, 14); ctext(d, 288, 176, "近似", FT, GRAY)
    ox, oy = 360, 140
    for i in range(3):
        for j in range(4):
            node(d, ox + j * 42, oy + i * 42, 4, "white")
    for i in range(3):
        d.line((ox, oy + i * 42, ox + 3 * 42, oy + i * 42), fill=LGRAY, width=1)
    for j in range(4):
        d.line((ox + j * 42, oy, ox + j * 42, oy + 2 * 42), fill=LGRAY, width=1)
    ctext(d, ox + 63, oy + 2 * 42 + 30, "有限個の自由度", FT, GRAY)
    note(d, "無限自由度の問題を有限自由度で近似して解く")
    save(im, "v2f5Discretize")


def f_fem():  # 2
    im, d = new(); title(d, "有限要素法（FEM）＝空間の離散化")
    d.rectangle((120, 110, 320, 260), outline=BLACK, width=3, fill="white")
    for i in range(1, 5):
        d.line((120 + i * 40, 110, 120 + i * 40, 260), fill=GRAY, width=1)
    for j in range(1, 4):
        d.line((120, 110 + j * 37, 320, 110 + j * 37), fill=GRAY, width=1)
    ctext(d, 220, 285, "対象領域を要素分割", FT, GRAY)
    ctext(d, 480, 150, "偏微分方程式の", FT)
    ctext(d, 480, 176, "数値解法の一種", FT)
    ctext(d, 480, 216, "空間微分を積分し", FT, BLUE)
    ctext(d, 480, 242, "空間を離散化", FT, BLUE)
    note(d, "残るのは時間微分だけの常微分方程式")
    save(im, "v2f5FEM")


def f_bem():  # 3
    im, d = new(); title(d, "境界要素法（BEM）＝境界だけを離散化")
    ox, oy = 130, 120
    d.rectangle((ox, oy, ox + 180, oy + 150), outline=BLACK, width=4, fill="white")
    for i in range(6):
        node(d, ox + i * 36, oy, 4, BLACK); node(d, ox + i * 36, oy + 150, 4, BLACK)
    for j in range(1, 4):
        node(d, ox, oy + j * 37, 4, BLACK); node(d, ox + 180, oy + j * 37, 4, BLACK)
    ctext(d, ox + 90, oy + 175, "境界のみ分割", FT, GRAY)
    ctext(d, 480, 150, "内部の要素分割", FT)
    ctext(d, 480, 176, "が不要", FT)
    ctext(d, 480, 216, "外部問題（放射）", FT, BLUE)
    ctext(d, 480, 242, "に有利", FT, BLUE)
    note(d, "ただし係数行列は密行列になる")
    save(im, "v2f5BEM")


def f_fdm():  # 4
    im, d = new(); title(d, "有限差分法（FDM）＝差分商で近似")
    ox, oy = 120, 110
    for i in range(5):
        for j in range(6):
            node(d, ox + j * 70, oy + i * 55, 3, BLACK)
    for i in range(5):
        d.line((ox, oy + i * 55, ox + 5 * 70, oy + i * 55), fill=LGRAY, width=1)
    for j in range(6):
        d.line((ox + j * 70, oy, ox + j * 70, oy + 4 * 55), fill=LGRAY, width=1)
    ctext(d, W / 2, 360, "微分 ~ 差分商（隣接格子点の差 / 間隔）", FS, BLUE)
    ctext(d, W / 2, 388, "構造格子が前提・時間方向によく用いる", FT, GRAY)
    save(im, "v2f5FDM")


def f_bar_wave():  # 5
    im, d = new(); title(d, "棒の縦振動の支配方程式と波速")
    cy = 150
    d.rectangle((110, cy - 24, 470, cy + 24), outline=BLACK, width=3, fill=FILL1)
    arrow(d, 110, cy + 54, 470, cy + 54, BLACK, 2, 10); ctext(d, 478, cy + 54, "x", FT, BLACK, "lm")
    arrow(d, 490, cy, 545, cy, ORANGE, 3, 13); ctext(d, 515, cy - 20, "波速 c", FT, ORANGE)
    ctext(d, W / 2, 290, "rho (d^2 w/dt^2) = E (d^2 w/dx^2)", F, BLUE)
    ctext(d, W / 2, 340, "c = sqrt( E / rho )", F, RED)
    note(d, "w:変位  rho:密度  E:ヤング率")
    save(im, "v2f5BarWave")


def f_disp_stress():  # 6
    im, d = new(); title(d, "変位法と応力法")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    ctext(d, 165, 100, "変位法", FS, BLUE)
    block(d, 165, 160, 190, 40, "変位を未知量", FT, FILL1)
    arrow(d, 165, 182, 165, 214, BLACK, 2, 10)
    block(d, 165, 236, 190, 40, "ひずみ・応力へ", FT, FILL1)
    arrow(d, 165, 258, 165, 290, BLACK, 2, 10)
    block(d, 165, 312, 190, 40, "剛性方程式", FT, FILL2)
    ctext(d, 495, 100, "応力法", FS, GREEN)
    block(d, 495, 160, 190, 40, "応力を未知量", FT, FILL1)
    arrow(d, 495, 182, 495, 214, BLACK, 2, 10)
    block(d, 495, 236, 190, 40, "適合条件を課す", FT, FILL1)
    arrow(d, 495, 258, 495, 290, BLACK, 2, 10)
    block(d, 495, 312, 190, 40, "柔性方程式", FT, FILL2)
    save(im, "v2f5DispStress")


def f_potential():  # 7
    im, d = new(); title(d, "全ポテンシャルエネルギーと停留条件")
    cy = 150
    wall(d, 130, cy - 40, cy + 40, side=1, n=6)
    spring(d, 130, cy, 340, coils=6, amp=16)
    d.rectangle((340, cy - 28, 380, cy + 28), outline=BLACK, width=3, fill=FILL2)
    force(d, 380, cy, 80, 0, "f", RED)
    ctext(d, 235, cy - 34, "k", FT, GRAY)
    ctext(d, W / 2, 250, "Pi = (1/2) k u^2 - u f", F, BLUE)
    ctext(d, W / 2, 300, "dPi/du = k u - f = 0", F, BLACK)
    ctext(d, W / 2, 348, "=>  k u = f", F, RED)
    save(im, "v2f5Potential")


def f_spring_k():  # 8
    im, d = new(); title(d, "ばね要素（2節点）の要素剛性行列")
    cy = 150
    node(d, 180, cy, 7, "white"); node(d, 420, cy, 7, "white")
    spring(d, 180, cy, 420, coils=6, amp=15)
    ctext(d, 180, cy + 26, "u1,f1", FT, GRAY); ctext(d, 420, cy + 26, "u2,f2", FT, GRAY)
    ctext(d, 300, cy - 30, "ばね定数 k", FT, GRAY)
    matrix_grid(d, 210, 240, [["k", "-k"], ["-k", "k"]], cell=64)
    ctext(d, 400, 300, "[k_e]", F, BLUE, "lm")
    note(d, "各行の和が 0")
    save(im, "v2f5SpringK")


def f_assembly():  # 9
    im, d = new(); title(d, "全体剛性行列の組立（重ね合わせ）")
    cy = 120
    xs = [130, 280, 430]
    wall(d, 100, cy - 28, cy + 28, side=1, n=5)
    for i in range(2):
        spring(d, xs[i], cy, xs[i + 1], coils=4, amp=11)
    for i, x in enumerate(xs):
        node(d, x, cy, 6, "white"); ctext(d, x, cy - 26, str(i + 1), FT, GRAY)
    matrix_grid(d, 200, 190,
                [["k1", "-k1", "0"], ["-k1", "k1+k2", "-k2"], ["0", "-k2", "k2"]],
                cell=58, fnt=FT)
    note(d, "各要素行列を関係する節点位置へ足し込む")
    save(im, "v2f5Assembly")


def f_constraint():  # 10
    im, d = new(); title(d, "拘束条件（境界条件）の処理")
    ox, oy, cell = 130, 130, 56
    grid_lines(d, ox, oy, 3, 3, cell)
    for r in range(3):
        fillcell(d, ox, oy + r * cell, cell, FILL3)
        fillcell(d, ox + r * cell, oy, cell, FILL3)
    for i in range(3):
        ctext(d, ox - 16, oy + i * cell + cell / 2, str(i + 1), FT, GRAY)
    ctext(d, ox + 1.5 * cell, oy + 3 * cell + 22, "固定自由度の行・列を除外", FT, GRAY)
    ctext(d, 470, 150, "変位0の自由度は", FT)
    ctext(d, 470, 176, "行・列を縮約", FT)
    ctext(d, 470, 216, "未知数が減り", FT, BLUE)
    ctext(d, 470, 242, "剛性行列が正則に", FT, BLUE)
    save(im, "v2f5Constraint")


def f_rod_k():  # 11
    im, d = new(); title(d, "棒の等価ばね定数  k = A E / l")
    cy = 170
    wall(d, 120, cy - 34, cy + 34, side=1, n=5)
    d.rectangle((120, cy - 26, 470, cy + 26), outline=BLACK, width=3, fill=FILL1)
    force(d, 470, cy, 80, 0, "F", RED)
    dim(d, 120, cy + 48, 470, cy + 48, "l", col=GRAY)
    ctext(d, 295, cy, "断面積 A・ヤング率 E", FT, GRAY)
    ctext(d, W / 2, 300, "sigma = E epsilon,  F = A sigma,  x = epsilon l", FS, GRAY)
    ctext(d, W / 2, 348, "=>  F = (A E / l) x  =>  k = A E / l", F, RED)
    save(im, "v2f5RodK")


def f_shape_func():  # 12
    im, d = new(); title(d, "形状関数（内挿関数）[N]")
    P1 = (140, 320); P2 = (420, 320); P3 = (280, 150)
    d.line([P1, P2, P3, P1], fill=BLACK, width=3)
    for p, lb in [(P1, "u^1"), (P2, "u^2"), (P3, "u^3")]:
        node(d, p[0], p[1], 6, "white")
        ctext(d, p[0], p[1] + (24 if p[1] > 250 else -24), lb, FT, RED)
    Q = (280, 265); node(d, Q[0], Q[1], 5, BLUE)
    for p in (P1, P2, P3):
        arrow(d, p[0], p[1], Q[0] + (p[0] - Q[0]) * 0.3, Q[1] + (p[1] - Q[1]) * 0.3, GRAY, 2, 8)
    ctext(d, 520, 210, "{u} = Sum Nk {u^k}", FS, BLUE)
    ctext(d, 520, 250, "節点変位から", FT, GRAY)
    ctext(d, 520, 274, "要素内を内挿", FT, GRAY)
    save(im, "v2f5ShapeFunc")


def f_linear_shape():  # 13
    im, d = new(); title(d, "1次元2節点要素の形状関数")
    ox, oy = 120, 320
    axes(d, ox, oy, 420, 240, "x", "N")
    xR = ox + 360; top = 180
    dash(d, ox, oy - top, xR, oy - top, LGRAY); ctext(d, ox - 12, oy - top, "1", FT, GRAY, "rm")
    node(d, ox, oy, 5, BLACK); node(d, xR, oy, 5, BLACK)
    ctext(d, ox, oy + 22, "節点1 (x=0)", FT, GRAY); ctext(d, xR, oy + 22, "節点2 (x=l)", FT, GRAY)
    plot(d, 0, 0, [(ox, oy - top), (xR, oy)], BLUE)
    ctext(d, ox + 80, oy - top + 34, "N1 = 1 - x/l", FT, BLUE, "lm")
    plot(d, 0, 0, [(ox, oy), (xR, oy - top)], GREEN)
    ctext(d, xR - 110, oy - top + 34, "N2 = x/l", FT, GREEN, "lm")
    ctext(d, (ox + xR) / 2, oy - top - 18, "N1 + N2 = 1（クロネッカーのデルタ性）", FT, RED)
    save(im, "v2f5LinearShape")


def f_node_dof():  # 14
    im, d = new(); title(d, "節点と自由度（棒・はり）")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    # 左：棒（1節点1自由度）
    cy = 180
    d.rectangle((90, cy - 18, 300, cy + 18), outline=BLACK, width=3, fill=FILL1)
    node(d, 90, cy, 6, "white"); node(d, 300, cy, 6, "white")
    arrow(d, 90, cy, 130, cy, RED, 3, 11); arrow(d, 300, cy, 340, cy, RED, 3, 11)
    ctext(d, 195, cy + 120, "棒（縦振動）", FS)
    ctext(d, 195, cy + 148, "1節点=軸変位のみ（1自由度）", FT, GRAY)
    # 右：はり（2自由度）
    d.line((370, cy, 570, cy), fill=BLACK, width=6)
    node(d, 370, cy, 6, "white"); node(d, 570, cy, 6, "white")
    for xn in (370, 570):
        arrow(d, xn, cy - 20, xn, cy - 60, BLUE, 3, 11)
        curve_arrow(d, xn, cy, 30, 200, 340, GREEN, 2, 9)
    ctext(d, 470, cy + 120, "はり（曲げ）", FS)
    ctext(d, 470, cy + 148, "たわみ＋回転角（2自由度）", FT, GRAY)
    save(im, "v2f5NodeDOF")


def f_weighted_residual():  # 15
    im, d = new(); title(d, "重みつき残差法とガラーキン法")
    ox, oy = 100, 230
    arrow(d, ox, oy, ox + 430, oy, BLACK, 2, 11); ctext(d, ox + 436, oy, "x", FT, BLACK, "lm")
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 400 * t
        y = oy - 60 * math.sin(math.pi * t) * math.cos(2.0 * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, RED)
    ctext(d, ox + 330, oy - 58, "残差 R", FT, RED, "lm")
    ctext(d, W / 2, 300, "∫ w R dOmega = 0", F, BLUE)
    ctext(d, W / 2, 348, "ガラーキン法: 重み w = 試行関数", FT, GRAY)
    save(im, "v2f5WeightedResidual")


def f_ritz():  # 16
    im, d = new(); title(d, "レイリー・リッツ法（変分法）")
    ox, oy = 120, 340
    axes(d, ox, oy, 430, 250, "係数", "汎関数 Pi")
    # 下に凸の放物線（停留＝最小）
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 380 * t
        y = oy - 200 + 170 * (2 * t - 1) ** 2
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    minx = ox + 190
    node(d, minx, oy - 200, 5, RED)
    dash(d, minx, oy, minx, oy - 200, LGRAY)
    ctext(d, minx, oy - 220, "停留（dPi=0）", FT, RED)
    ctext(d, W / 2, 388, "汎関数に変分原理を適用し未知係数を決める", FT, GRAY)
    save(im, "v2f5Ritz")


def f_static_dynamic():  # 17
    im, d = new(); title(d, "静的解析と動的解析の基礎方程式")
    ctext(d, W / 2, 130, "静的：  [K]{u} = {F}", F, BLUE)
    d.line((90, 175, 570, 175), fill=LGRAY, width=1)
    ctext(d, W / 2, 235, "動的：", F, GREEN)
    ctext(d, W / 2, 285, "[M]{u''} + [C]{u'} + [K]{u} = {F(t)}", F, GREEN)
    ctext(d, W / 2, 350, "[M]:質量  [C]:減衰  [K]:剛性", FT, GRAY)
    ctext(d, W / 2, 380, "微小変形なら剛性 [K] は静・動で同一", FT, RED)
    save(im, "v2f5StaticDynamic")


def f_mass_matrix():  # 18
    im, d = new(); title(d, "質量行列（整合・集中）")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    matrix_grid(d, 110, 140, [["a", "b"], ["b", "a"]], cell=62)
    ctext(d, 172, 290, "整合質量行列", FS, BLUE)
    ctext(d, 172, 318, "形状関数で積分", FT, GRAY)
    ctext(d, 172, 342, "非対角に値", FT, GRAY)
    matrix_grid(d, 410, 140, [["m", "0"], ["0", "m"]], cell=62)
    ctext(d, 472, 290, "集中質量行列", FS, GREEN)
    ctext(d, 472, 318, "節点へ集中", FT, GRAY)
    ctext(d, 472, 342, "対角のみ", FT, GRAY)
    save(im, "v2f5MassMatrix")


def f_consistent_mass():  # 19
    im, d = new(); title(d, "棒要素の整合質量行列")
    cy = 130
    d.rectangle((150, cy - 20, 440, cy + 20), outline=BLACK, width=3, fill=FILL1)
    node(d, 150, cy, 6, BLACK); node(d, 440, cy, 6, BLACK)
    dim(d, 150, cy + 40, 440, cy + 40, "l", col=GRAY)
    ctext(d, 295, cy, "線密度 mu", FT, GRAY)
    ctext(d, W / 2, 230, "[M] = ∫ mu [ L1^2  L1L2 ; L1L2  L2^2 ] dx", FT, GRAY)
    ctext(d, 200, 320, "= (mu l / 6)", FS, RED)
    matrix_grid(d, 330, 285, [["2", "1"], ["1", "2"]], cell=58)
    save(im, "v2f5ConsistentMass")


def f_lumped_mass():  # 20
    im, d = new(); title(d, "棒要素の集中質量行列")
    cy = 130
    d.rectangle((150, cy - 20, 440, cy + 20), outline=BLACK, width=3, fill=FILL1)
    node(d, 150, cy, 8, "white"); node(d, 440, cy, 8, "white")
    ctext(d, 150, cy + 34, "mu l / 2", FT, RED); ctext(d, 440, cy + 34, "mu l / 2", FT, RED)
    ctext(d, 295, cy - 40, "全質量 mu l を両端へ等分", FT, GRAY)
    ctext(d, 200, 300, "= (mu l / 2)", FS, RED)
    matrix_grid(d, 330, 265, [["1", "0"], ["0", "1"]], cell=58)
    note(d, "対角行列・陽解法と相性がよい")
    save(im, "v2f5LumpedMass")


def f_sparse_dense():  # 21
    im, d = new(); title(d, "疎行列と密行列")
    cell = 32; n = 6
    ox, oy = 100, 120
    for r in range(n):
        for c in range(n):
            if abs(r - c) <= 1:
                fillcell(d, ox + c * cell, oy + r * cell, cell, FILL3)
    grid_lines(d, ox, oy, n, n, cell)
    ctext(d, ox + n * cell / 2, oy + n * cell + 22, "疎行列（FEM）", FS)
    ctext(d, ox + n * cell / 2, oy + n * cell + 46, "帯状に非ゼロ", FT, GRAY)
    ox2 = 400
    for r in range(n):
        for c in range(n):
            fillcell(d, ox2 + c * cell, oy + r * cell, cell, FILL3)
    grid_lines(d, ox2, oy, n, n, cell)
    ctext(d, ox2 + n * cell / 2, oy + n * cell + 22, "密行列（BEM）", FS)
    ctext(d, ox2 + n * cell / 2, oy + n * cell + 46, "ほぼ全成分が非ゼロ", FT, GRAY)
    save(im, "v2f5SparseDense")


def f_unit_system():  # 22
    im, d = new(); title(d, "整合単位系（単位を自分で整合させる）")
    ox, oy = 150, 90
    cw, ch = 180, 44
    rows = [("量", "単位"), ("長さ", "mm"), ("質量", "kg"),
            ("時間", "s"), ("密度", "kg/mm^3")]
    for i, (a, b) in enumerate(rows):
        y = oy + i * ch
        fill = FILL2 if i == 0 else "white"
        d.rectangle((ox, y, ox + cw, y + ch), outline=BLACK, width=2, fill=fill)
        d.rectangle((ox + cw, y, ox + cw * 2, y + ch), outline=BLACK, width=2, fill=fill)
        ctext(d, ox + cw / 2, y + ch / 2, a, FS)
        ctext(d, ox + cw * 1.5, y + ch / 2, b, FS)
    note(d, "モデラは単位を明示しない → 力・応力の単位を整合させる")
    save(im, "v2f5UnitSystem")


def f_jacobian():  # 23
    im, d = new(); title(d, "ヤコビアンと等パラメトリック要素")
    # 左：基準要素（正方形 xi,eta）
    ox, oy = 90, 150
    s = 130
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for p in [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]:
        node(d, p[0], p[1], 5, "white")
    arrow(d, ox, oy + s, ox + s + 20, oy + s, GRAY, 2, 9); ctext(d, ox + s + 26, oy + s, "xi", FT, GRAY, "lm")
    arrow(d, ox, oy + s, ox, oy - 20, GRAY, 2, 9); ctext(d, ox - 12, oy - 24, "eta", FT, GRAY)
    ctext(d, ox + s / 2, oy + s + 34, "基準要素 (-1..1)", FT, GRAY)
    # 写像矢印
    arrow(d, ox + s + 40, oy + s / 2, ox + s + 110, oy + s / 2, BLUE, 3, 13)
    ctext(d, ox + s + 75, oy + s / 2 - 20, "[J]", FS, BLUE)
    # 右：実要素（ゆがんだ四辺形 x,y）
    P = [(400, 190), (560, 160), (540, 300), (410, 320)]
    d.polygon(P, outline=BLACK, width=3, fill=FILL2)
    for p in P:
        node(d, p[0], p[1], 5, "white")
    ctext(d, 480, 340, "実要素 (x,y)", FT, GRAY)
    ctext(d, W / 2, 388, "dOmega = det[J] d(xi) d(eta)", FS, RED)
    save(im, "v2f5Jacobian")


def f_gauss():  # 24
    im, d = new(); title(d, "ガウス積分（数値積分）")
    ox, oy = 130, 150
    s = 180
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    # 2x2 のガウス点
    for gx in (ox + s * 0.25, ox + s * 0.75):
        for gy in (oy + s * 0.25, oy + s * 0.75):
            node(d, gx, gy, 6, RED);
    ctext(d, ox + s / 2, oy + s + 26, "積分点（ガウス点）", FT, RED)
    ctext(d, 440, 180, "積分を", FT)
    ctext(d, 440, 206, "積分点での", FT)
    ctext(d, 440, 232, "重み付き和で評価", FT)
    ctext(d, 440, 275, "n点で 2n-1 次まで", FT, BLUE)
    ctext(d, 440, 301, "厳密に積分", FT, BLUE)
    save(im, "v2f5Gauss")


def f_convergence():  # 25
    im, d = new(); title(d, "収束と要素次数（h法・p法）")
    ox, oy = 110, 330
    axes(d, ox, oy, 440, 250, "自由度", "誤差")
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 400 * t
        y = oy - 210 * (1 - math.exp(-3.2 * t))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    dash(d, ox, oy - 210, ox + 400, oy - 210, LGRAY)
    ctext(d, ox + 300, oy - 190, "厳密解へ収束", FT, RED)
    ctext(d, ox + 210, oy - 30, "h法: 要素を細かく", FT, GRAY)
    ctext(d, ox + 210, oy - 8, "p法: 次数を上げる", FT, GRAY)
    save(im, "v2f5Convergence")


def f_q4():  # 26
    im, d = new(); title(d, "双一次（4節点四辺形1次）要素")
    ox, oy = 200, 130
    s = 170
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for p in [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]:
        node(d, p[0], p[1], 7, "white")
    ctext(d, ox + s / 2, oy + s / 2, "4節点", FT, GRAY)
    ctext(d, W / 2, 340, "u = a1 + a2 x + a3 y + a4 xy", F, BLUE)
    ctext(d, W / 2, 385, "剛体運動・一定ひずみを表現 → パッチテスト合格", FT, GRAY)
    save(im, "v2f5Q4")


if __name__ == "__main__":
    for fn in [f_discretize, f_fem, f_bem, f_fdm, f_bar_wave, f_disp_stress,
               f_potential, f_spring_k, f_assembly, f_constraint, f_rod_k,
               f_shape_func, f_linear_shape, f_node_dof, f_weighted_residual,
               f_ritz, f_static_dynamic, f_mass_matrix, f_consistent_mass,
               f_lumped_mass, f_sparse_dense, f_unit_system, f_jacobian,
               f_gauss, f_convergence, f_q4]:
        fn()
    print("done 26")
