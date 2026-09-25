# -*- coding: utf-8 -*-
"""振動2級 第6章「要素の選択・メッシング」の問題図（全13枚）。接頭辞 v2e6。
白地660×420・黒線画（figlib準拠）。
required問題図は答え・正解値・結論・正解の選択肢を描かない（与件・配置・記号のみ）。
文字化け回避のためギリシャ文字は綴り（theta, epsilon, rho, xi, eta）で書く。
実行: python tools/figs_vib2ch6_e.py
"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
import math
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot, iso_box,
                    F, FL, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN, ORANGE,
                    FILL1, FILL2, FILL3, W, H)


# ---- 共通ヘルパ ----
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
    """math角(反時計回り・右=0°) a0→a1 の円弧矢印。a1端に矢じり。"""
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


def xmark(d, x, y, s=7, col=RED, wd=3):
    d.line((x - s, y - s, x + s, y + s), fill=col, width=wd)
    d.line((x - s, y + s, x + s, y - s), fill=col, width=wd)


def tri(d, p1, p2, p3, fill=FILL1, wd=3):
    d.polygon([p1, p2, p3], outline=BLACK, width=wd, fill=fill)


def tetra(d, ox, oy, s, second=False):
    """四面体の簡易アイソメ表現。second=Trueで辺の中点にも節点。"""
    A = (ox, oy + s)                     # 手前左
    B = (ox + s, oy + s)                 # 手前右
    C = (ox + int(s * 0.35), oy + int(s * 0.45))  # 手前奥(上)
    Tp = (ox + int(s * 0.62), oy)        # 頂点
    d.line([A, B], fill=BLACK, width=2)
    d.line([A, C], fill=BLACK, width=2)
    d.line([B, C], fill=BLACK, width=2)
    d.line([A, Tp], fill=BLACK, width=2)
    d.line([B, Tp], fill=BLACK, width=2)
    d.line([C, Tp], fill=BLACK, width=2)
    verts = [A, B, C, Tp]
    for p in verts:
        node(d, p[0], p[1], 5, "white")
    if second:
        edges = [(A, B), (A, C), (B, C), (A, Tp), (B, Tp), (C, Tp)]
        for (p, q) in edges:
            node(d, (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 4, RED)


def hexbox(d, ox, oy, w, h, dp, second=False):
    """六面体のアイソメ。second=Trueで各辺中点にも節点。"""
    iso_box(d, ox, oy, w, h, dp)
    dx = int(dp * 0.8); dy = int(dp * 0.5)
    # 8頂点
    front = [(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)]
    back = [(ox + dx, oy - dy), (ox + w + dx, oy - dy),
            (ox + w + dx, oy + h - dy), (ox + dx, oy + h - dy)]
    for p in front + back:
        node(d, p[0], p[1], 4, "white")
    if second:
        allp = front + back
        # いくつかの主要辺の中点
        pairs = [(0, 1), (1, 2), (2, 3), (3, 0),
                 (0, 4), (1, 5), (2, 6),
                 (4, 5), (5, 6), (6, 7), (7, 4)]
        for (i, j) in pairs:
            p, q = allp[i], allp[j]
            node(d, (p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 3, RED)


# ============================================================
# 問題図 v2e6（13枚）
# ============================================================

def beam_shape_order(name):  # 6-1 required
    im, d = new()
    title(d, "2節点はり要素：軸方向の伸びと曲げのたわみ")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：軸方向の伸び（直線的な補間）
    cy = 180
    x0, x1 = 100, 280
    d.rectangle((x0, cy - 15, x1, cy + 15), outline=BLACK, width=3, fill=FILL1)
    node(d, x0, cy, 6, "white"); node(d, x1, cy, 6, "white")
    arrow(d, x0, cy, x0 - 34, cy, RED, 3, 11)
    arrow(d, x1, cy, x1 + 34, cy, RED, 3, 11)
    ctext(d, 190, cy - 38, "軸方向の伸び", FS)
    # 直線補間グラフ
    gy = 320
    arrow(d, x0, gy, x1 + 12, gy, BLACK, 2, 9)
    plot(d, 0, 0, [(x0, gy - 18), (x1, gy - 62)], BLUE)
    node(d, x0, gy - 18, 4, BLUE); node(d, x1, gy - 62, 4, BLUE)
    ctext(d, 190, gy + 22, "変位は直線的に補間", FT, GRAY)
    # 右：曲げによるたわみ（なめらかな曲線＋回転角）
    x2, x3 = 380, 580
    # 元位置（破線）
    dash(d, x2, cy, x3, cy, LGRAY)
    node(d, x2, cy, 6, "white"); node(d, x3, cy, 6, "white")
    # たわみ曲線（3次的なくぼみ）
    pts = []
    for i in range(41):
        t = i / 40.0
        x = x2 + (x3 - x2) * t
        y = cy + 70 * (t * t * (3 - 2 * t))  # なめらかに下がる
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    node(d, x3, pts[-1][1], 5, RED)
    arrow(d, x3, cy, x3, pts[-1][1] - 6, RED, 2, 10)
    ctext(d, x3 + 14, (cy + pts[-1][1]) / 2, "w", FT, RED, "lm")
    # 回転角 theta（両節点で接線方向の回転）
    curve_arrow(d, x2, cy, 30, 300, 350, GREEN, 2, 9)
    ctext(d, x2 - 4, cy - 34, "theta", FT, GREEN)
    curve_arrow(d, x3, pts[-1][1], 30, 200, 250, GREEN, 2, 9)
    ctext(d, x3 - 40, pts[-1][1] + 6, "theta", FT, GREEN)
    ctext(d, 480, cy - 38, "曲げによるたわみ", FS)
    ctext(d, 480, 350, "各節点に たわみ w と 回転角 theta", FT, GRAY)
    save(im, name)


def tri_constant_strain(name):  # 6-2 required
    im, d = new()
    title(d, "3節点三角形要素：要素内ひずみが一様")
    P1 = (150, 330); P2 = (470, 330); P3 = (300, 130)
    tri(d, P1, P2, P3, fill=FILL2)
    for p, lb in [(P1, "節点1"), (P2, "節点2"), (P3, "節点3")]:
        node(d, p[0], p[1], 8, "white")
        ctext(d, p[0], p[1] + (26 if p[1] > 250 else -26), lb, FT, GRAY)
    ctext(d, 305, 275, "要素内ひずみ 一様", FS, RED)
    ctext(d, W / 2, 380, "{epsilon} = [B]{ue}", F, BLUE)
    save(im, name)


def element_compare(name):  # 6-3 required
    im, d = new()
    title(d, "要素の種類と次数による節点配置")
    # 上段：三角形 と 四辺形
    tri(d, (90, 175), (230, 175), (160, 80), fill="white")
    for p in [(90, 175), (230, 175), (160, 80)]:
        node(d, p[0], p[1], 6, "white")
    ctext(d, 160, 198, "3節点三角形", FT, GRAY)
    d.rectangle((360, 85, 500, 175), outline=BLACK, width=3, fill="white")
    for p in [(360, 85), (500, 85), (500, 175), (360, 175)]:
        node(d, p[0], p[1], 6, "white")
    ctext(d, 430, 198, "4節点四辺形", FT, GRAY)
    d.line((90, 235, 570, 235), fill=LGRAY, width=1)
    ctext(d, W / 2, 250, "同じ要素数での 低次 と 高次（辺の中間に節点）", FT, GRAY)
    # 下段：低次 と 高次（四辺形で比較）
    oy = 285
    d.rectangle((110, oy, 240, oy + 90), outline=BLACK, width=3, fill="white")
    for p in [(110, oy), (240, oy), (240, oy + 90), (110, oy + 90)]:
        node(d, p[0], p[1], 6, "white")
    ctext(d, 175, oy + 112, "低次要素", FT)
    d.rectangle((400, oy, 530, oy + 90), outline=BLACK, width=3, fill="white")
    corners = [(400, oy), (530, oy), (530, oy + 90), (400, oy + 90)]
    for p in corners:
        node(d, p[0], p[1], 6, "white")
    mids = [(465, oy), (530, oy + 45), (465, oy + 90), (400, oy + 45)]
    for p in mids:
        node(d, p[0], p[1], 5, RED)
    ctext(d, 465, oy + 112, "高次要素（節点が増える）", FT)
    save(im, name)


def element_variety(name):  # 6-4 required
    im, d = new()
    title(d, "要素の種類（計算時間・精度・適用形状が異なる）")
    y = 150
    # 棒
    d.line((70, y, 150, y), fill=BLACK, width=5)
    node(d, 70, y, 5, "white"); node(d, 150, y, 5, "white")
    ctext(d, 110, y + 40, "棒", FT, GRAY)
    # はり
    d.line((200, y, 290, y), fill=BLACK, width=6)
    node(d, 200, y, 5, "white"); node(d, 290, y, 5, "white")
    curve_arrow(d, 245, y, 18, 210, 330, GREEN, 2, 7)
    ctext(d, 245, y + 40, "はり", FT, GRAY)
    # 三角形
    tri(d, (340, y + 25), (430, y + 25), (385, y - 35), fill=FILL1)
    ctext(d, 385, y + 45, "三角形", FT, GRAY)
    # 四辺形
    d.rectangle((470, y - 30, 560, y + 25), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 515, y + 45, "四辺形", FT, GRAY)
    # 六面体ソリッド
    hexbox(d, 250, 290, 110, 70, 46)
    ctext(d, 320, 388, "六面体ソリッド", FT, GRAY)
    ctext(d, 500, 300, "対象の形状に応じて", FT)
    ctext(d, 500, 326, "使い分ける", FT)
    save(im, name)


def mesh_convergence(name):  # 6-5 helpful
    im, d = new()
    title(d, "メッシュ細分化と変形量の収束")
    ox, oy = 110, 330
    axes(d, ox, oy, 440, 250, "メッシュの細かさ", "変形量")
    # 厳密解（水平線・上限）
    ex = oy - 210
    dash(d, ox, ex, ox + 400, ex, LGRAY)
    ctext(d, ox + 300, ex - 16, "厳密解", FT, RED)
    # FEM解：下側から漸近（変形量が小→厳密解へ増加）
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 400 * t
        y = oy - 210 * (1 - math.exp(-3.0 * t))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    ctext(d, ox + 250, oy - 60, "FEM解（下側から収束）", FT, BLUE)
    note(d, "非圧縮材では体積ロッキングで収束しないことがある")
    save(im, name)


def plate_bending_elems(name):  # 6-6 required
    im, d = new()
    title(d, "板の曲げ：低次で細分 と 高次で粗分の節点数")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：低次要素で細かく分割
    ox, oy = 90, 130
    n = 4
    cell = 48
    for i in range(n):
        for j in range(n):
            d.rectangle((ox + j * cell, oy + i * cell,
                         ox + (j + 1) * cell, oy + (i + 1) * cell),
                        outline=GRAY, width=1)
    for i in range(n + 1):
        for j in range(n + 1):
            node(d, ox + j * cell, oy + i * cell, 3, "white")
    ctext(d, ox + n * cell / 2, oy + n * cell + 26, "低次要素で細かく分割", FT)
    ctext(d, ox + n * cell / 2, oy + n * cell + 50, "節点が多い", FT, GRAY)
    # 右：高次要素で粗く分割
    ox2, oy2 = 400, 150
    s = 150
    for gi in range(1):
        for gj in range(1):
            d.rectangle((ox2, oy2, ox2 + s, oy2 + s), outline=GRAY, width=2)
    corners = [(ox2, oy2), (ox2 + s, oy2), (ox2 + s, oy2 + s), (ox2, oy2 + s)]
    for p in corners:
        node(d, p[0], p[1], 5, "white")
    mids = [(ox2 + s / 2, oy2), (ox2 + s, oy2 + s / 2),
            (ox2 + s / 2, oy2 + s), (ox2, oy2 + s / 2)]
    for p in mids:
        node(d, p[0], p[1], 5, RED)
    ctext(d, ox2 + s / 2, oy2 + s + 26, "高次要素で粗く分割", FT)
    ctext(d, ox2 + s / 2, oy2 + s + 50, "節点が少ない", FT, GRAY)
    save(im, name)


def plate_shell_types(name):  # 6-7 required
    im, d = new()
    title(d, "薄板（Kirchhoff）と厚板（Reissner-Mindlin）の断面")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：薄板 = 断面は中立面に垂直のまま
    cy = 210
    x0, x1 = 80, 290
    # 変形した中立面（ゆるい曲線）
    pts = []
    for i in range(41):
        t = i / 40.0
        x = x0 + (x1 - x0) * t
        y = cy + 26 * math.sin(math.pi * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLACK)
    for t in (0.25, 0.5, 0.75):
        idx = int(t * 40)
        px, py = pts[idx]
        # 接線
        if idx == 0:
            idx = 1
        tx = pts[idx][0] - pts[idx - 1][0]
        ty = pts[idx][1] - pts[idx - 1][1]
        L = math.hypot(tx, ty)
        nx, ny = -ty / L, tx / L  # 中立面に垂直
        d.line((px - nx * 26, py - ny * 26, px + nx * 26, py + ny * 26),
               fill=RED, width=3)
    ctext(d, (x0 + x1) / 2, cy + 90, "薄板：断面は中立面に垂直", FT, RED)
    ctext(d, (x0 + x1) / 2, cy + 114, "広がり >= 板厚の約10倍", FT, GRAY)
    # 右：厚板 = 断面が回転（せん断変形）
    x2, x3 = 380, 590
    pts2 = []
    for i in range(41):
        t = i / 40.0
        x = x2 + (x3 - x2) * t
        y = cy + 26 * math.sin(math.pi * t)
        pts2.append((x, y))
    plot(d, 0, 0, pts2, BLACK)
    for t in (0.25, 0.5, 0.75):
        idx = int(t * 40)
        px, py = pts2[idx]
        # わざと垂直から傾けた断面（せん断変形）
        ang = math.radians(90 + 22 * math.cos(math.pi * t))
        dx2, dy2 = math.cos(ang) * 26, math.sin(ang) * 26
        d.line((px - dx2, py - dy2, px + dx2, py + dy2), fill=BLUE, width=3)
    ctext(d, (x2 + x3) / 2, cy + 90, "厚板：断面が回転（せん断考慮）", FT, BLUE)
    ctext(d, (x2 + x3) / 2, cy + 114, "たわみと回転角が独立", FT, GRAY)
    save(im, name)


def shell_approx(name):  # 6-8 required
    im, d = new()
    title(d, "薄肉シェル：板厚 t が代表寸法 L よりずっと小さい")
    # 薄い板（アイソメ）
    ox, oy = 130, 180
    w, h, dp = 300, 12, 90
    iso_box(d, ox, oy, w, h, dp)
    dim(d, ox, oy + 40, ox + w, oy + 40, "代表寸法 L", col=GRAY)
    ctext(d, ox - 20, oy + h / 2, "t", FT, RED, "rm")
    arrow(d, ox - 14, oy, ox - 14, oy + h, RED, 2, 7)
    ctext(d, W / 2, 300, "t << L  →  板厚方向の応力を無視（2次元応力状態で近似）", FS, BLUE)
    note(d, "曲面シェルに平面シェル要素を使うときは分割を密にする")
    save(im, name)


def adaptive_rhp(name):  # 6-9 required
    im, d = new()
    title(d, "アダプティブメッシュ法：R法・H法・P法")
    labels = ["R法（節点を移動）", "H法（要素を細分）", "P法（次数を上げる）"]
    ox0 = 60
    for k in range(3):
        ox = ox0 + k * 200
        oy = 130
        s = 150
        d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=2, fill="white")
        if k == 0:  # R法：節点を偏らせて移動
            for i in range(4):
                for j in range(4):
                    # 右側へ寄せる非一様格子
                    fx = (j / 3.0) ** 1.6
                    fy = i / 3.0
                    node(d, ox + fx * s, oy + fy * s, 4, RED)
            arrow(d, ox + 40, oy + s + 20, ox + s - 20, oy + s + 20, RED, 2, 9)
        elif k == 1:  # H法：右下だけ細分
            d.line((ox + s / 2, oy, ox + s / 2, oy + s), fill=GRAY, width=1)
            d.line((ox, oy + s / 2, ox + s, oy + s / 2), fill=GRAY, width=1)
            # 右下を4分割
            hx, hy = ox + s / 2, oy + s / 2
            d.line((hx + s / 4, hy, hx + s / 4, oy + s), fill=GRAY, width=1)
            d.line((hx, hy + s / 4, ox + s, hy + s / 4), fill=GRAY, width=1)
            for p in [(ox, oy), (ox + s, oy), (ox, oy + s), (ox + s, oy + s),
                      (hx, hy)]:
                node(d, p[0], p[1], 3, BLACK)
        else:  # P法：次数を上げる（辺中点に節点）
            corners = [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]
            for p in corners:
                node(d, p[0], p[1], 5, "white")
            mids = [(ox + s / 2, oy), (ox + s, oy + s / 2),
                    (ox + s / 2, oy + s), (ox, oy + s / 2), (ox + s / 2, oy + s / 2)]
            for p in mids:
                node(d, p[0], p[1], 5, RED)
        ctext(d, ox + s / 2, oy + s + 42, labels[k], FT)
    save(im, name)


def plate_part_transient(name):  # 6-10 required
    im, d = new()
    title(d, "上下左右対称・左端固定の板状部品と変動力 F")
    cy = 220
    # くびれ形状（対称）
    top = [(150, cy - 70), (260, cy - 70), (360, cy - 34),
           (460, cy - 70), (520, cy - 70)]
    bot = [(520, cy + 70), (460, cy + 70), (360, cy + 34),
           (260, cy + 70), (150, cy + 70)]
    d.polygon(top + bot, outline=BLACK, width=3, fill=FILL1)
    # 左端固定
    wall(d, 150, cy - 70, cy + 70, side=-1, n=8)
    ctext(d, 150, cy + 92, "左端固定", FT, GRAY)
    # 対称軸
    dash(d, 150, cy, 520, cy, LGRAY)
    dash(d, 335, cy - 78, 335, cy + 78, LGRAY)
    # 点A（右端）
    A = (520, cy)
    node(d, A[0], A[1], 6, RED)
    ctext(d, A[0] + 4, A[1] + 22, "点A", FT, RED, "lm")
    # 面内成分（板の面内・上向き）
    force(d, A[0], A[1], 0, -60, "面内成分", RED)
    # 面外成分（奥行き方向＝斜め）
    arrow(d, A[0], A[1], A[0] + 60, A[1] - 34, BLUE, 4, 14)
    ctext(d, A[0] + 66, A[1] - 40, "面外成分", FT, BLUE, "lm")
    ctext(d, 335, cy + 108, "変動力 F（面内＋面外）の過渡応答", FT, GRAY)
    save(im, name)


def solid_mesh_types(name):  # 6-11 required
    im, d = new()
    title(d, "中実部品の要素分割：六面体／四面体・1次／2次")
    # 六面体 1次
    hexbox(d, 90, 150, 110, 70, 46, second=False)
    ctext(d, 160, 250, "六面体 1次", FT, GRAY)
    # 六面体 2次
    hexbox(d, 400, 150, 110, 70, 46, second=True)
    ctext(d, 470, 250, "六面体 2次（辺中点にも節点）", FT, GRAY)
    # 四面体 1次
    tetra(d, 120, 300, 90, second=False)
    ctext(d, 165, 405, "四面体 1次", FT, GRAY)
    # 四面体 2次
    tetra(d, 430, 300, 90, second=True)
    ctext(d, 475, 405, "四面体 2次（辺中点にも節点）", FT, GRAY)
    save(im, name)


def lumped_mass_elem(name):  # 6-12 required
    im, d = new()
    title(d, "集中質量要素（スカラー要素）＝形状を持たない1点")
    cx, cy = 300, 220
    # 点（質量）
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cx, cy, "m", FS)
    ctext(d, cx, cy + 34, "形状を持たない1点", FT, GRAY)
    # 属性の吹き出し
    block(d, 150, 110, 220, 44, "質量 m", FT, FILL1)
    arrow(d, 190, 132, cx - 12, cy - 10, GRAY, 2, 9)
    block(d, 500, 130, 250, 44, "重心まわりの慣性モーメント", FT, FILL1)
    arrow(d, 430, 150, cx + 12, cy - 8, GRAY, 2, 9)
    block(d, 470, 330, 220, 44, "慣性乗積", FT, FILL1)
    arrow(d, 400, 320, cx + 12, cy + 8, GRAY, 2, 9)
    note(d, "検討する周波数範囲で剛体とみなせる部品に使用")
    save(im, name)


def gauss_points(name):  # 6-13 required
    im, d = new()
    title(d, "積分点（ガウス点）：応力・ひずみの評価点")
    # 左：1次元要素
    y = 150
    x0, x1 = 70, 300
    d.rectangle((x0, y - 18, x1, y + 18), outline=BLACK, width=3, fill=FILL1)
    node(d, x0, y, 6, "white"); node(d, x1, y, 6, "white")
    g1 = x0 + (x1 - x0) * 0.25
    g2 = x0 + (x1 - x0) * 0.75
    xmark(d, g1, y); xmark(d, g2, y)
    ctext(d, (x0 + x1) / 2, y + 40, "1次元要素の積分点（×）", FT, GRAY)
    # 外挿の矢印（積分点→節点）
    arrow(d, g1, y - 26, x0, y - 26, GREEN, 2, 9)
    arrow(d, g2, y - 26, x1, y - 26, GREEN, 2, 9)
    ctext(d, (x0 + x1) / 2, y - 40, "節点値は外挿", FT, GREEN)
    # 右：四辺形要素
    ox, oy = 360, 240
    s = 150
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for p in [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]:
        node(d, p[0], p[1], 6, "white")
    gs = []
    for gx in (ox + s * 0.25, ox + s * 0.75):
        for gy in (oy + s * 0.25, oy + s * 0.75):
            xmark(d, gx, gy)
            gs.append((gx, gy))
    # 1つの積分点から近い節点へ外挿矢印
    arrow(d, gs[0][0], gs[0][1], ox + 8, oy + 8, GREEN, 2, 8)
    ctext(d, ox + s / 2, oy + s + 26, "四辺形要素の積分点（×）", FT, GRAY)
    ctext(d, ox + s / 2, oy + s + 50, "応力・ひずみは積分点で評価", FT, RED)
    save(im, name)


if __name__ == "__main__":
    beam_shape_order("v2e6BeamShapeOrder")
    tri_constant_strain("v2e6TriConstantStrain")
    element_compare("v2e6ElementCompare")
    element_variety("v2e6ElementVariety")
    mesh_convergence("v2e6MeshConvergence")
    plate_bending_elems("v2e6PlateBendingElems")
    plate_shell_types("v2e6PlateShellTypes")
    shell_approx("v2e6ShellApprox")
    adaptive_rhp("v2e6AdaptiveRHP")
    plate_part_transient("v2e6PlatePartTransient")
    solid_mesh_types("v2e6SolidMeshTypes")
    lumped_mass_elem("v2e6LumpedMassElem")
    gauss_points("v2e6GaussPoints")
    print("done 13")
