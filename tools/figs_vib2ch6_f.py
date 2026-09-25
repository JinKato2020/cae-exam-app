# -*- coding: utf-8 -*-
"""振動2級 第6章「要素の選択・メッシング」公式・用語カード用の図 26枚。接頭辞 v2f6。
白地660×420・黒線画（figlib準拠）。公式カード＝回答後の根拠図なので結果・式を描いてよい。
文字化け回避のためギリシャ文字は綴り（rho, epsilon, theta, xi, eta, nu, Omega）で書く。
実行: python tools/figs_vib2ch6_f.py
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot, iso_box,
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


def dashrect(d, x0, y0, x1, y1, col=RED, wd=2):
    dash(d, x0, y0, x1, y0, col, wd)
    dash(d, x1, y0, x1, y1, col, wd)
    dash(d, x1, y1, x0, y1, col, wd)
    dash(d, x0, y1, x0, y0, col, wd)


def fillcell(d, x, y, cell, col):
    d.rectangle((x + 2, y + 2, x + cell - 2, y + cell - 2), fill=col)


def grid_lines(d, x, y, rows, cols, cell):
    for i in range(rows + 1):
        d.line((x, y + i * cell, x + cols * cell, y + i * cell), fill=BLACK, width=2)
    for j in range(cols + 1):
        d.line((x + j * cell, y, x + j * cell, y + rows * cell), fill=BLACK, width=2)


def xmark(d, x, y, s=7, col=RED, wd=3):
    d.line((x - s, y - s, x + s, y + s), fill=col, width=wd)
    d.line((x - s, y + s, x + s, y - s), fill=col, width=wd)


def tri(d, p1, p2, p3, fill=FILL1, wd=3):
    d.polygon([p1, p2, p3], outline=BLACK, width=wd, fill=fill)


# ============================================================
# 公式・用語図 v2f6（26枚）
# ============================================================

def f_shape_interp():  # 1  v2f6ShapeInterp
    im, d = new(); title(d, "形状関数による変位補間  {u}=[N]{ue}")
    P1 = (140, 320); P2 = (420, 320); P3 = (280, 150)
    tri(d, P1, P2, P3, fill=FILL1)
    for p, lb in [(P1, "u1"), (P2, "u2"), (P3, "u3")]:
        node(d, p[0], p[1], 6, "white")
        ctext(d, p[0], p[1] + (24 if p[1] > 250 else -24), lb, FT, RED)
    Q = (280, 265); node(d, Q[0], Q[1], 5, BLUE)
    for p in (P1, P2, P3):
        arrow(d, p[0], p[1], Q[0] + (p[0] - Q[0]) * 0.3, Q[1] + (p[1] - Q[1]) * 0.3, GRAY, 2, 8)
    ctext(d, 520, 210, "節点変位から", FT, GRAY)
    ctext(d, 520, 236, "要素内を補間", FT, GRAY)
    ctext(d, 520, 276, "一次対象は変位", FT, BLUE)
    save(im, "v2f6ShapeInterp")


def f_beam_shape():  # 2  v2f6BeamShape
    im, d = new(); title(d, "2節点はり要素の形状関数の次数")
    cy = 140
    d.line((150, cy, 450, cy), fill=BLACK, width=6)
    node(d, 150, cy, 6, "white"); node(d, 450, cy, 6, "white")
    arrow(d, 150, cy, 110, cy, RED, 3, 10); arrow(d, 450, cy, 490, cy, RED, 3, 10)
    for xn in (150, 450):
        curve_arrow(d, xn, cy, 26, 200, 330, GREEN, 2, 8)
    ctext(d, W / 2, 235, "軸方向： u = N1 u1 + N2 u2  （1次）", FS, BLUE)
    ctext(d, W / 2, 285, "たわみ： w = N1 w1 + N2 theta1 + N3 w2 + N4 theta2  （3次）", FT, GREEN)
    ctext(d, W / 2, 345, "各節点で たわみ w と 回転角 theta の2自由度", FT, GRAY)
    save(im, "v2f6BeamShape")


def f_bmatrix():  # 3  v2f6Bmatrix
    im, d = new(); title(d, "ひずみ-変位行列と定ひずみ要素")
    P1 = (150, 320); P2 = (430, 320); P3 = (290, 150)
    tri(d, P1, P2, P3, fill=FILL2)
    for p in (P1, P2, P3):
        node(d, p[0], p[1], 6, "white")
    ctext(d, 290, 270, "ひずみ一定", FT, RED)
    ctext(d, W / 2, 358, "{epsilon} = [B]{ue}  ,  [B]=一定 → 定ひずみ要素(CST)", FS, BLUE)
    save(im, "v2f6Bmatrix")


def f_inertia():  # 4  v2f6Inertia
    im, d = new(); title(d, "要素内の慣性力  {fin} = -rho {u''}")
    P1 = (150, 320); P2 = (430, 320); P3 = (290, 150)
    tri(d, P1, P2, P3, fill=FILL1)
    for p in (P1, P2, P3):
        node(d, p[0], p[1], 6, "white")
    # 慣性力の分布（要素内で1次に変化）を小矢印で
    for (fx, fy) in [(220, 300), (290, 270), (360, 300), (290, 230)]:
        arrow(d, fx, fy, fx, fy - 34, ORANGE, 2, 9)
    ctext(d, W / 2, 360, "rho 一定なら座標の1次関数で分布（一定や2次ではない）", FT, GRAY)
    ctext(d, 500, 200, "rho：密度", FT, GRAY)
    ctext(d, 500, 226, "u'':加速度", FT, GRAY)
    save(im, "v2f6Inertia")


def f_bilinear():  # 5  v2f6Bilinear
    im, d = new(); title(d, "双一次関数と4節点四辺形要素")
    ox, oy = 210, 120
    s = 160
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for p in [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]:
        node(d, p[0], p[1], 7, "white")
    ctext(d, ox + s / 2, oy + s / 2, "4節点", FT, GRAY)
    ctext(d, W / 2, 330, "u = a1 + a2 x + a3 y + a4 xy", F, BLUE)
    ctext(d, W / 2, 380, "= f(x) g(y) の形（双一次）→ パッチテスト合格", FT, GRAY)
    save(im, "v2f6Bilinear")


def f_order_nodes():  # 6  v2f6OrderNodes
    im, d = new(); title(d, "要素の次数と節点数")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：3節点三角形（1次）
    tri(d, (120, 280), (280, 280), (200, 140), fill="white")
    for p in [(120, 280), (280, 280), (200, 140)]:
        node(d, p[0], p[1], 6, "white")
    ctext(d, 200, 310, "3節点三角形（1次）", FT)
    # 右：6節点三角形（2次）
    A, B, C = (390, 280), (550, 280), (470, 140)
    tri(d, A, B, C, fill="white")
    for p in (A, B, C):
        node(d, p[0], p[1], 6, "white")
    for (p, q) in [(A, B), (B, C), (C, A)]:
        node(d, (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 5, RED)
    ctext(d, 470, 310, "6節点三角形（2次）", FT)
    ctext(d, 470, 334, "辺の中点にも節点", FT, GRAY)
    note(d, "同じ要素数なら高次要素の方が節点数は多い")
    save(im, "v2f6OrderNodes")


def f_element_choice():  # 7  v2f6ElementChoice
    im, d = new(); title(d, "要素選択の指針（対象の形状で使い分け）")
    # 細長い→はり
    d.line((90, 130, 230, 130), fill=BLACK, width=6)
    node(d, 90, 130, 5, "white"); node(d, 230, 130, 5, "white")
    ctext(d, 160, 158, "細長い部材 → はり要素", FT, GRAY)
    # 薄い板→シェル
    iso_box(d, 380, 120, 150, 10, 60)
    ctext(d, 455, 165, "薄い板 → シェル要素", FT, GRAY)
    # 複雑な塊→ソリッド
    iso_box(d, 130, 250, 120, 80, 55)
    ctext(d, 200, 355, "複雑な塊 → ソリッド要素", FT, GRAY)
    ctext(d, 470, 280, "はり・板要素が使えれば", FT, BLUE)
    ctext(d, 470, 306, "計算負荷を下げつつ", FT, BLUE)
    ctext(d, 470, 332, "精度も上げられる", FT, BLUE)
    save(im, "v2f6ElementChoice")


def f_element_kinds():  # 8  v2f6ElementKinds
    im, d = new(); title(d, "有限要素の種類（次元で分類）")
    y = 140
    # スカラー要素（点）
    d.ellipse((100, y - 10, 120, y + 10), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 110, y + 34, "スカラー要素", FT, GRAY)
    ctext(d, 110, y + 56, "(集中質量・ばね)", FT, GRAY)
    # 1次元要素（線）
    d.line((230, y, 330, y), fill=BLACK, width=5)
    node(d, 230, y, 4, "white"); node(d, 330, y, 4, "white")
    ctext(d, 280, y + 34, "1次元要素", FT, GRAY)
    ctext(d, 280, y + 56, "(棒・はり)", FT, GRAY)
    # 2次元要素（面）
    d.rectangle((410, y - 26, 500, y + 26), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 455, y + 44, "2次元要素", FT, GRAY)
    ctext(d, 455, y + 66, "(三角形・四辺形・シェル)", FT, GRAY)
    # 3次元ソリッド
    iso_box(d, 250, 300, 120, 70, 50)
    ctext(d, 320, 392, "3次元ソリッド要素（四面体・六面体）", FT, GRAY)
    save(im, "v2f6ElementKinds")


def f_stiffness_over():  # 9  v2f6StiffnessOver
    im, d = new(); title(d, "離散化による剛性の過大評価")
    ox, oy = 110, 330
    axes(d, ox, oy, 440, 250, "メッシュの細かさ", "変形量")
    ex = oy - 210
    dash(d, ox, ex, ox + 400, ex, LGRAY)
    ctext(d, ox + 300, ex - 16, "厳密解", FT, RED)
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 400 * t
        y = oy - 210 * (1 - math.exp(-3.0 * t))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    ctext(d, ox + 250, oy - 55, "剛性が過大 → 変形量が小さい", FT, BLUE)
    note(d, "細かくすると過大評価が緩和され厳密解へ近づく")
    save(im, "v2f6StiffnessOver")


def f_convergence():  # 10  v2f6Convergence
    im, d = new(); title(d, "メッシュ細分化と収束")
    ox, oy = 110, 330
    axes(d, ox, oy, 440, 250, "自由度（細分）", "誤差")
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 400 * t
        y = oy - 210 * (1 - math.exp(-3.2 * t))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    dash(d, ox, oy - 210, ox + 400, oy - 210, LGRAY)
    ctext(d, ox + 290, oy - 192, "厳密解へ収束", FT, RED)
    ctext(d, ox + 210, oy - 24, "パッチテスト合格が最低条件", FT, GRAY)
    save(im, "v2f6Convergence")


def f_locking():  # 11  v2f6Locking
    im, d = new(); title(d, "ロッキング（剛性の過大評価）")
    # 低次要素が変形を再現できず硬くなる
    ox, oy = 120, 150
    s = 120
    dashrect(d, ox, oy, ox + s, oy + s, LGRAY)
    ctext(d, ox + s / 2, oy - 16, "本来の変形", FT, GRAY)
    # ほとんど変形しない要素
    d.rectangle((ox + 200, oy, ox + 200 + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + 200 + s / 2, oy - 16, "硬すぎる（変形小）", FT, RED)
    ctext(d, W / 2, 320, "低次要素で変形を再現できず剛性が過大に", FT, GRAY)
    ctext(d, W / 2, 350, "→ 体積ロッキング と せん断ロッキング", FS, BLUE)
    save(im, "v2f6Locking")


def f_vol_locking():  # 12  v2f6VolLocking
    im, d = new(); title(d, "体積ロッキング（非圧縮性に近い材料）")
    ox, oy = 130, 150
    s = 150
    dashrect(d, ox, oy, ox + s, oy + s, LGRAY)
    # 体積一定拘束で変形しづらい
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + s / 2, oy + s / 2, "体積変化を", FT, GRAY)
    ctext(d, ox + s / 2, oy + s / 2 + 22, "過度に拘束", FT, GRAY)
    ctext(d, 460, 170, "ポアソン比 nu が", FT)
    ctext(d, 460, 196, "0.5 に近い材料", FT)
    ctext(d, 460, 236, "低減積分・混合要素", FT, BLUE)
    ctext(d, 460, 262, "で回避", FT, BLUE)
    ctext(d, W / 2, 360, "剛性が過大 → 変形が小さく評価される", FT, RED)
    save(im, "v2f6VolLocking")


def f_shear_locking():  # 13  v2f6ShearLocking
    im, d = new(); title(d, "せん断ロッキング（細長い構造の曲げ）")
    # 細長い片持ちはり
    cy = 180
    wall(d, 100, cy - 30, cy + 30, side=-1, n=5)
    d.rectangle((100, cy - 12, 470, cy + 12), outline=BLACK, width=3, fill=FILL1)
    force(d, 470, cy, 0, 50, "曲げ", RED)
    # 寄生せん断ひずみ（要素が平行四辺形に）
    ctext(d, W / 2, 290, "低次要素が純曲げで 寄生的なせん断ひずみ を生じる", FT, GRAY)
    ctext(d, W / 2, 330, "余分なせん断剛性で 硬くなる（たわみ小）", FS, BLUE)
    note(d, "薄い板・梁で顕著。低減積分などで緩和")
    save(im, "v2f6ShearLocking")


def f_high_vs_low():  # 14  v2f6HighVsLow
    im, d = new(); title(d, "高次要素 と 低次細分割の使い分け")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：低次要素で細分
    ox, oy = 90, 130
    n = 4; cell = 48
    for i in range(n):
        for j in range(n):
            d.rectangle((ox + j * cell, oy + i * cell,
                         ox + (j + 1) * cell, oy + (i + 1) * cell), outline=GRAY, width=1)
    for i in range(n + 1):
        for j in range(n + 1):
            node(d, ox + j * cell, oy + i * cell, 3, "white")
    ctext(d, ox + n * cell / 2, oy + n * cell + 26, "低次要素で細分", FT)
    ctext(d, ox + n * cell / 2, oy + n * cell + 50, "節点が多い", FT, GRAY)
    # 右：高次要素で粗く
    ox2, oy2 = 400, 150; s = 150
    d.rectangle((ox2, oy2, ox2 + s, oy2 + s), outline=GRAY, width=2)
    for p in [(ox2, oy2), (ox2 + s, oy2), (ox2 + s, oy2 + s), (ox2, oy2 + s)]:
        node(d, p[0], p[1], 5, "white")
    for p in [(ox2 + s / 2, oy2), (ox2 + s, oy2 + s / 2),
              (ox2 + s / 2, oy2 + s), (ox2, oy2 + s / 2)]:
        node(d, p[0], p[1], 5, RED)
    ctext(d, ox2 + s / 2, oy2 + s + 26, "高次要素で粗く", FT)
    ctext(d, ox2 + s / 2, oy2 + s + 50, "同精度なら節点が少ない", FT, GRAY)
    save(im, "v2f6HighVsLow")


def f_zooming():  # 15  v2f6Zooming
    im, d = new(); title(d, "ズーミング法（局所を細分して再解析）")
    # 全体（粗い）
    ox, oy = 90, 130
    d.rectangle((ox, oy, ox + 200, oy + 160), outline=BLACK, width=3, fill="white")
    for i in range(1, 4):
        d.line((ox + i * 50, oy, ox + i * 50, oy + 160), fill=GRAY, width=1)
    for j in range(1, 4):
        d.line((ox, oy + j * 40, ox + 200, oy + j * 40), fill=GRAY, width=1)
    dashrect(d, ox + 130, oy + 90, ox + 190, oy + 150, RED, 2)
    ctext(d, ox + 100, oy + 180, "全体モデル（粗い）", FT, GRAY)
    # ズーム（細かい）
    arrow(d, ox + 210, oy + 120, ox + 300, oy + 120, BLUE, 3, 13)
    ox2, oy2 = 400, 130
    d.rectangle((ox2, oy2, ox2 + 170, oy2 + 160), outline=RED, width=3, fill="white")
    n = 6; c = 170 / n
    for i in range(1, n):
        d.line((ox2 + i * c, oy2, ox2 + i * c, oy2 + 160), fill=GRAY, width=1)
        d.line((ox2, oy2 + i * c, ox2 + 170, oy2 + i * c), fill=GRAY, width=1)
    ctext(d, ox2 + 85, oy2 + 180, "応力集中部を細分", FT, RED)
    note(d, "粗い解を境界条件に取り込み局所だけ再解析")
    save(im, "v2f6Zooming")


def f_kirchhoff():  # 16  v2f6Kirchhoff
    im, d = new(); title(d, "Kirchhoff要素（薄板要素）")
    cy = 200
    x0, x1 = 110, 470
    pts = []
    for i in range(41):
        t = i / 40.0
        x = x0 + (x1 - x0) * t
        y = cy + 34 * math.sin(math.pi * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLACK)
    for t in (0.2, 0.5, 0.8):
        idx = max(1, int(t * 40))
        px, py = pts[idx]
        tx = pts[idx][0] - pts[idx - 1][0]; ty = pts[idx][1] - pts[idx - 1][1]
        L = math.hypot(tx, ty); nx, ny = -ty / L, tx / L
        d.line((px - nx * 28, py - ny * 28, px + nx * 28, py + ny * 28), fill=RED, width=3)
    ctext(d, W / 2, 300, "断面は変形後も中立面に垂直（せん断変形を無視）", FT, RED)
    ctext(d, W / 2, 340, "適用条件：広がり >= 板厚の約10倍", FS, GRAY)
    save(im, "v2f6Kirchhoff")


def f_mindlin():  # 17  v2f6Mindlin
    im, d = new(); title(d, "Reissner-Mindlin要素（厚板要素）")
    cy = 200
    x0, x1 = 110, 470
    pts = []
    for i in range(41):
        t = i / 40.0
        x = x0 + (x1 - x0) * t
        y = cy + 34 * math.sin(math.pi * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLACK)
    for t in (0.2, 0.5, 0.8):
        idx = max(1, int(t * 40))
        px, py = pts[idx]
        ang = math.radians(90 + 24 * math.cos(math.pi * t))
        dx, dy = math.cos(ang) * 28, math.sin(ang) * 28
        d.line((px - dx, py - dy, px + dx, py + dy), fill=BLUE, width=3)
    ctext(d, W / 2, 300, "断面の回転を許容 → 面外せん断変形を考慮", FT, BLUE)
    ctext(d, W / 2, 340, "たわみ と 断面回転角 を独立の自由度に", FS, GRAY)
    save(im, "v2f6Mindlin")


def f_shell():  # 18  v2f6Shell
    im, d = new(); title(d, "シェル要素と2次元応力近似")
    ox, oy = 130, 170
    w, h, dp = 300, 12, 90
    iso_box(d, ox, oy, w, h, dp)
    dim(d, ox, oy + 40, ox + w, oy + 40, "代表寸法 L", col=GRAY)
    arrow(d, ox - 14, oy, ox - 14, oy + h, RED, 2, 7)
    ctext(d, ox - 22, oy + h / 2, "t", FT, RED, "rm")
    ctext(d, W / 2, 300, "t << L → 板厚方向の応力を無視（2次元応力状態）", FS, BLUE)
    ctext(d, W / 2, 345, "ソリッドより少ないメッシュで済む", FT, GRAY)
    note(d, "曲面に平面シェル要素を使うときは分割を密に")
    save(im, "v2f6Shell")


def f_adaptive():  # 19  v2f6Adaptive
    im, d = new(); title(d, "アダプティブメッシュ法（R法・H法・P法）")
    labels = ["R法：節点を移動", "H法：要素を細分", "P法：次数を上げる"]
    for k in range(3):
        ox = 60 + k * 200; oy = 130; s = 150
        d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=2, fill="white")
        if k == 0:
            for i in range(4):
                for j in range(4):
                    fx = (j / 3.0) ** 1.6; fy = i / 3.0
                    node(d, ox + fx * s, oy + fy * s, 4, RED)
        elif k == 1:
            d.line((ox + s / 2, oy, ox + s / 2, oy + s), fill=GRAY, width=1)
            d.line((ox, oy + s / 2, ox + s, oy + s / 2), fill=GRAY, width=1)
            hx, hy = ox + s / 2, oy + s / 2
            d.line((hx + s / 4, hy, hx + s / 4, oy + s), fill=GRAY, width=1)
            d.line((hx, hy + s / 4, ox + s, hy + s / 4), fill=GRAY, width=1)
            for p in [(ox, oy), (ox + s, oy), (ox, oy + s), (ox + s, oy + s), (hx, hy)]:
                node(d, p[0], p[1], 3, BLACK)
        else:
            for p in [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]:
                node(d, p[0], p[1], 5, "white")
            for p in [(ox + s / 2, oy), (ox + s, oy + s / 2),
                      (ox + s / 2, oy + s), (ox, oy + s / 2), (ox + s / 2, oy + s / 2)]:
                node(d, p[0], p[1], 5, RED)
        ctext(d, ox + s / 2, oy + s + 36, labels[k], FT)
    ctext(d, W / 2, 388, "次数を上げて精度を向上させるのは P法", FT, BLUE)
    save(im, "v2f6Adaptive")


def f_symmetry():  # 20  v2f6Symmetry
    im, d = new(); title(d, "対称性を利用したモデル簡略化")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：全体（対称形状＋対称荷重ならOK）
    ox, oy = 120, 150
    d.rectangle((ox, oy, ox + 150, oy + 150), outline=BLACK, width=3, fill=FILL1)
    dash(d, ox + 75, oy, ox + 75, oy + 150, LGRAY)
    dash(d, ox, oy + 75, ox + 150, oy + 75, LGRAY)
    ctext(d, ox + 75, oy + 175, "対称形状", FT, GRAY)
    # 右：1/4モデル
    ox2, oy2 = 420, 150
    d.rectangle((ox2, oy2, ox2 + 90, oy2 + 90), outline=RED, width=3, fill=FILL2)
    wall(d, ox2, oy2, oy2 + 90, side=1, n=5)
    hwall(d, ox2, ox2 + 90, oy2 + 90, side=-1, n=5)
    ctext(d, ox2 + 45, oy2 + 115, "1/4 モデル", FT, RED)
    ctext(d, W / 2, 340, "荷重・応答も対称のときだけ簡略化できる", FS, BLUE)
    note(d, "変動力が非対称なら全体をモデル化する")
    save(im, "v2f6Symmetry")


def f_explicit():  # 21  v2f6Explicit
    im, d = new(); title(d, "陽解法（動的過渡応答）")
    # 時間軸で前の量から次を直接
    ox, oy = 100, 170
    for k, lb in enumerate(["t-dt", "t", "t+dt"]):
        x = ox + k * 190
        node(d, x, oy, 7, "white")
        ctext(d, x, oy + 26, lb, FT, GRAY)
    arrow(d, ox + 14, oy, ox + 190 - 14, oy, BLUE, 3, 12)
    arrow(d, ox + 190 + 14, oy, ox + 380 - 14, oy, BLUE, 3, 12)
    ctext(d, ox + 285, oy - 22, "前の量から直接", FT, BLUE)
    ctext(d, W / 2, 260, "連立方程式を解かずに次の変位を求める", FT, GRAY)
    ctext(d, W / 2, 300, "集中質量行列（対角）と相性がよい", FS, BLUE)
    ctext(d, W / 2, 345, "安定には時間刻み dt を十分小さく", FT, RED)
    save(im, "v2f6Explicit")


def f_solid_mesh():  # 22  v2f6SolidMesh
    im, d = new(); title(d, "中実部品の要素分割（四面体・六面体）")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：六面体（望ましい）
    iso_box(d, 120, 150, 120, 80, 55)
    ctext(d, 180, 260, "六面体（望ましい）", FT, BLUE)
    # 右：四面体1次（剛性過大→一般に使わない）
    A = (400, 280); B = (520, 280); C = (430, 230); Tp = (470, 150)
    for (p, q) in [(A, B), (A, C), (B, C), (A, Tp), (B, Tp), (C, Tp)]:
        d.line([p, q], fill=BLACK, width=2)
    for p in (A, B, C, Tp):
        node(d, p[0], p[1], 5, "white")
    ctext(d, 465, 305, "四面体1次", FT, RED)
    ctext(d, 465, 329, "剛性を過大評価→一般に不可", FT, GRAY)
    ctext(d, W / 2, 392, "四面体を使うなら2次要素にする", FT, GRAY)
    save(im, "v2f6SolidMesh")


def f_lumped_mass_elem():  # 23  v2f6LumpedMassElem
    im, d = new(); title(d, "集中質量要素（スカラー要素）")
    cx, cy = 290, 210
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cx, cy, "m", FS)
    ctext(d, cx, cy + 32, "形状を持たない1点", FT, GRAY)
    block(d, 150, 120, 220, 42, "質量 m", FT, FILL1)
    arrow(d, 185, 141, cx - 12, cy - 10, GRAY, 2, 8)
    block(d, 500, 140, 250, 42, "重心まわりの慣性モーメント", FT, FILL1)
    arrow(d, 430, 158, cx + 12, cy - 8, GRAY, 2, 8)
    block(d, 470, 330, 200, 42, "慣性乗積", FT, FILL1)
    arrow(d, 400, 320, cx + 12, cy + 8, GRAY, 2, 8)
    note(d, "検討周波数範囲で剛体とみなせる部品に使用")
    save(im, "v2f6LumpedMassElem")


def f_inertia_tensor():  # 24  v2f6InertiaTensor
    im, d = new(); title(d, "慣性テンソルと慣性主軸")
    matrix_grid(d, 90, 140,
                [["Ix", "-Ixy", "-Ixz"], ["-Ixy", "Iy", "-Iyz"], ["-Ixz", "-Iyz", "Iz"]],
                cell=58, fnt=FT)
    ctext(d, 90 + 1.5 * 58, 140 + 3 * 58 + 22, "慣性テンソル", FT, GRAY)
    ctext(d, 460, 150, "対角＝慣性モーメント", FT)
    ctext(d, 460, 176, "非対角＝慣性乗積", FT)
    ctext(d, 460, 220, "慣性主軸に合わせると", FT, BLUE)
    ctext(d, 460, 246, "慣性乗積 = 0", FT, BLUE)
    ctext(d, 460, 272, "（対角行列になる）", FT, BLUE)
    save(im, "v2f6InertiaTensor")


def f_gauss():  # 25  v2f6Gauss
    im, d = new(); title(d, "剛性行列と数値積分（ガウス積分）")
    ox, oy = 120, 130
    s = 150
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for gx in (ox + s * 0.25, ox + s * 0.75):
        for gy in (oy + s * 0.25, oy + s * 0.75):
            xmark(d, gx, gy)
    ctext(d, ox + s / 2, oy + s + 24, "2x2 ガウス点（×）", FT, RED)
    ctext(d, 470, 150, "[Ke] =", F, BLUE)
    ctext(d, 470, 190, "∫ [B]^T [D] [B] dOmega", FT, BLUE)
    ctext(d, 470, 240, "積分点での", FT, GRAY)
    ctext(d, 470, 266, "重み付き和で評価", FT, GRAY)
    ctext(d, W / 2, 388, "n点で 2n-1 次まで厳密に積分できる", FT, GRAY)
    save(im, "v2f6Gauss")


def f_integration_point():  # 26  v2f6IntegrationPoint
    im, d = new(); title(d, "積分点と外挿")
    ox, oy = 160, 140
    s = 160
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    corners = [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]
    for p in corners:
        node(d, p[0], p[1], 6, "white")
    gs = []
    for gx in (ox + s * 0.25, ox + s * 0.75):
        for gy in (oy + s * 0.25, oy + s * 0.75):
            xmark(d, gx, gy)
            gs.append((gx, gy))
    # 積分点→節点への外挿矢印
    arrow(d, gs[0][0], gs[0][1], corners[0][0] + 8, corners[0][1] + 8, GREEN, 2, 9)
    arrow(d, gs[3][0], gs[3][1], corners[2][0] - 8, corners[2][1] - 8, GREEN, 2, 9)
    ctext(d, ox + s / 2, oy + s + 26, "積分点（×）＝分点（区間内部）", FT, RED)
    ctext(d, ox + s / 2, oy + s + 50, "応力・ひずみは積分点で評価", FT, GRAY)
    ctext(d, ox + s / 2, oy - 16, "節点値は積分点から外挿", FT, GREEN)
    save(im, "v2f6IntegrationPoint")


if __name__ == "__main__":
    for fn in [f_shape_interp, f_beam_shape, f_bmatrix, f_inertia, f_bilinear,
               f_order_nodes, f_element_choice, f_element_kinds, f_stiffness_over,
               f_convergence, f_locking, f_vol_locking, f_shear_locking,
               f_high_vs_low, f_zooming, f_kirchhoff, f_mindlin, f_shell,
               f_adaptive, f_symmetry, f_explicit, f_solid_mesh,
               f_lumped_mass_elem, f_inertia_tensor, f_gauss, f_integration_point]:
        fn()
    print("done 26")
