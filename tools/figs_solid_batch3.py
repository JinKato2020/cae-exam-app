# -*- coding: utf-8 -*-
"""Phase2 Batch3: 図なし18問へ後付けする図。
fem-practice 第5章 有限要素法の実践(fem-5-1..10,13,16,18,21,22,23,28,29)。
接頭辞 f5*。白地660x420・黒線画・機構/概念のみ(答えの番号・最終数値は焼き込まない)。すべて helpful(回答後表示)。
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


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3, col=BLACK):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def mlines(d, cx, cy, lines, fnt=FT, fill=BLACK, lh=23):
    n = len(lines)
    y0 = cy - (n - 1) * lh / 2
    for i, s in enumerate(lines):
        ctext(d, cx, y0 + i * lh, s, fnt, fill)


def quad(d, pts, col=BLACK, wd=3, fill=FILL1, ndot=True, ncol=BLACK, r=5):
    d.polygon(pts, outline=col, width=wd, fill=fill)
    if ndot:
        for p in pts:
            node(d, p[0], p[1], r, fill="white", col=ncol)


# ============================================================
# fem-5-1 アイソパラメトリック要素の考え方
# ============================================================
def f5IsoConcept():
    im, d = new(); title(d, "アイソパラメトリック要素の考え方")
    quad(d, [(70, 120), (215, 105), (230, 250), (85, 265)], fill=FILL1)
    ctext(d, 150, 292, "要素(節点 i)", FT, GRAY)
    box(d, 275, 165, 400, 235, FILL2, col=BLUE)
    mlines(d, 337, 200, ["形状関数 Ni", "(座標・変位で同一)"], FT, BLUE, 24)
    arrow(d, 402, 185, 470, 155, BLACK, 3, 12)
    arrow(d, 402, 215, 470, 258, BLACK, 3, 12)
    box(d, 472, 128, 615, 182, FILL1)
    mlines(d, 543, 155, ["位置座標を補間", "x=ΣNixi, y=ΣNiyi"], FT, BLACK, 24)
    box(d, 472, 232, 615, 286, FILL1)
    mlines(d, 543, 259, ["変位を補間", "u=ΣNiui, v=ΣNivi"], FT, BLACK, 24)
    ctext(d, W / 2, 330, "次数は要素タイプ次第:4節点=1次〜高次まで取り得る", FT, RED)
    note(d, "座標と変位をまったく同一の形状関数で補間する要素。次数は限定されない。")
    save(im, "f5IsoConcept")


# ============================================================
# fem-5-2 iso/super/subパラメトリック
# ============================================================
def f5IsoSuperSub():
    im, d = new(); title(d, "座標節点と変位節点の数による要素の分類")
    cols = [(150, "アイソパラメトリック", "座標節点 = 変位節点", "(同数・同一形状関数)"),
            (330, "スーパーパラメトリック", "座標節点 > 変位節点", "(座標を高次で表す)"),
            (510, "サブパラメトリック", "座標節点 < 変位節点", "(座標を低次で表す)")]
    for cx, ttl, l1, l2 in cols:
        box(d, cx - 88, 78, cx + 88, 116, FILL2, col=BLUE)
        ctext(d, cx, 97, ttl, FT, BLUE)
        # element sketch: black=座標節点, red=変位節点(追加分)
        x0, y0, s = cx - 45, 150, 90
        box(d, x0, y0, x0 + s, y0 + s, FILL1)
    # iso: corner black only
    for p in [(105, 150), (195, 150), (105, 240), (195, 240)]:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    # super: coord high -> extra coord(black) midside
    for p in [(285, 150), (375, 150), (285, 240), (375, 240)]:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    for p in [(330, 150), (330, 240), (285, 195), (375, 195)]:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    # sub: disp high -> extra disp(red) midside, coord only corners(black)
    for p in [(465, 150), (555, 150), (465, 240), (555, 240)]:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    for p in [(510, 150), (510, 240), (465, 195), (555, 195)]:
        node(d, p[0], p[1], 5, fill=RED, col=RED)
    for cx, ttl, l1, l2 in cols:
        ctext(d, cx, 268, l1, FT, BLACK)
        ctext(d, cx, 292, l2, FT, GRAY)
    node(d, 250, 330, 5, fill=BLACK, col=BLACK); ctext(d, 262, 330, "座標節点", FT, BLACK, "lm")
    node(d, 400, 330, 5, fill=RED, col=RED); ctext(d, 412, 330, "変位節点(追加)", FT, RED, "lm")
    note(d, "iso=同数、super=座標が高次(節点多)、sub=座標が低次(節点少)。実務はisoが主流。")
    save(im, "f5IsoSuperSub")


# ============================================================
# fem-5-3 4節点=1次 / 8節点=2次
# ============================================================
def f5NodeOrder():
    im, d = new(); title(d, "四辺形要素の節点数と形状関数の次数")
    # 4-node
    x0, y0, s = 95, 130, 150
    box(d, x0, y0, x0 + s, y0 + s, FILL1)
    for p in [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]:
        node(d, p[0], p[1], 6, fill=BLACK, col=BLACK)
    ctext(d, x0 + s / 2, y0 + s + 26, "4節点要素", FS, BLUE)
    ctext(d, x0 + s / 2, y0 + s + 54, "各辺の節点は両端2つ", FT, GRAY)
    ctext(d, x0 + s / 2, y0 + s + 78, "→ 形状関数は 1次(線形)", FT, RED)
    # 8-node
    x1 = 415
    box(d, x1, y0, x1 + s, y0 + s, FILL1)
    for p in [(x1, y0), (x1 + s, y0), (x1, y0 + s), (x1 + s, y0 + s)]:
        node(d, p[0], p[1], 6, fill=BLACK, col=BLACK)
    for p in [(x1 + s / 2, y0), (x1 + s / 2, y0 + s), (x1, y0 + s / 2), (x1 + s, y0 + s / 2)]:
        node(d, p[0], p[1], 6, fill=RED, col=RED)
    ctext(d, x1 + s / 2, y0 + s + 26, "8節点要素", FS, BLUE)
    ctext(d, x1 + s / 2, y0 + s + 54, "各辺に中間節点(赤)を追加", FT, GRAY)
    ctext(d, x1 + s / 2, y0 + s + 78, "→ 形状関数は 2次", FT, RED)
    note(d, "辺上の節点数で次数が決まる。8節点の方が高次で表現能力が高い。")
    save(im, "f5NodeOrder")


# ============================================================
# fem-5-4 四辺形=局所座標(ξ,η) / 三角形=面積座標
# ============================================================
def f5QuadTriCoord():
    im, d = new(); title(d, "要素と内挿に用いる座標系")
    # 四辺形
    x0, y0, s = 90, 130, 150
    box(d, x0, y0, x0 + s, y0 + s, FILL1)
    for p in [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    cx, cy = x0 + s / 2, y0 + s / 2
    arrow(d, cx, cy, cx + 55, cy, BLUE, 2, 10); ctext(d, cx + 62, cy, "ξ", FS, BLUE, "lm")
    arrow(d, cx, cy, cx, cy - 55, BLUE, 2, 10); ctext(d, cx, cy - 68, "η", FS, BLUE)
    ctext(d, x0 + s / 2, y0 + s + 30, "四辺形要素", FS, BLACK)
    ctext(d, x0 + s / 2, y0 + s + 56, "局所座標 (ξ, η)", FT, RED)
    # 三角形
    tx, ty = 400, 130
    tp = [(tx + 75, ty), (tx, ty + 150), (tx + 150, ty + 150)]
    d.polygon(tp, outline=BLACK, width=3, fill=FILL1)
    for p in tp:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    gx = (tp[0][0] + tp[1][0] + tp[2][0]) / 3
    gy = (tp[0][1] + tp[1][1] + tp[2][1]) / 3
    ctext(d, tp[0][0], tp[0][1] - 16, "L1", FT, BLUE)
    ctext(d, tp[1][0] - 16, tp[1][1] + 6, "L2", FT, BLUE, "rm")
    ctext(d, tp[2][0] + 16, tp[2][1] + 6, "L3", FT, BLUE, "lm")
    ctext(d, gx, gy, "L1+L2+L3=1", FT, GRAY)
    ctext(d, tx + 75, ty + 150 + 30, "三角形要素", FS, BLACK)
    ctext(d, tx + 75, ty + 150 + 56, "面積座標 (L1,L2,L3)", FT, RED)
    note(d, "四辺形は局所座標(ξ,η)で内挿。面積座標は三角形(体積座標は四面体)用。")
    save(im, "f5QuadTriCoord")


# ============================================================
# fem-5-5 局所→全体 座標写像
# ============================================================
def f5CoordMap():
    im, d = new(); title(d, "局所座標から全体座標への写像")
    # 局所 正方形 -1..1
    x0, y0, s = 70, 135, 150
    box(d, x0, y0, x0 + s, y0 + s, FILL1)
    for p, lb in zip([(x0, y0 + s), (x0 + s, y0 + s), (x0 + s, y0), (x0, y0)],
                     ["1", "2", "3", "4"]):
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    cx, cy = x0 + s / 2, y0 + s / 2
    arrow(d, cx, cy, cx + 50, cy, BLUE, 2, 9); ctext(d, cx + 58, cy, "ξ", FT, BLUE, "lm")
    arrow(d, cx, cy, cx, cy - 50, BLUE, 2, 9); ctext(d, cx, cy - 62, "η", FT, BLUE)
    ctext(d, x0 + s / 2, y0 - 18, "局所座標(親要素)", FT, GRAY)
    ctext(d, x0 + s / 2, y0 + s + 26, "−1 ≤ ξ,η ≤ 1", FT, BLACK)
    # 写像矢印
    arrow(d, x0 + s + 18, cy, x0 + s + 92, cy, BLACK, 3, 14)
    ctext(d, x0 + s + 55, cy - 20, "写像", FT, BLUE)
    ctext(d, x0 + s + 55, cy + 22, "Ni", FT, BLUE)
    # 全体 歪んだ四辺形
    gp = [(400, 300), (560, 285), (585, 150), (430, 130)]
    quad(d, gp, fill=FILL1, ncol=BLACK, r=5)
    for p, lb in zip(gp, ["(x1,y1)", "(x2,y2)", "(x3,y3)", "(x4,y4)"]):
        ctext(d, p[0], p[1] - 16, lb, FT, GRAY)
    ctext(d, 505, 112, "全体座標", FT, GRAY)
    ctext(d, 490, 340, "座標も変位と同じ Ni で補間", FT, RED)
    note(d, "親要素(局所)から実要素(全体)への写像を、変位と同一の形状関数で行う。")
    save(im, "f5CoordMap")


# ============================================================
# fem-5-6 4節点1次要素の変形表現(曲げは2次で不可)
# ============================================================
def f5BendLimit():
    im, d = new(); title(d, "4節点1次要素が表せる変形・表しにくい変形")
    base = [(0, 0), (110, 0), (110, 90), (0, 90)]

    def elem(ox, oy, corners, col, dashbase=True):
        if dashbase:
            for i in range(4):
                a = (ox + base[i][0], oy + base[i][1])
                b = (ox + base[(i + 1) % 4][0], oy + base[(i + 1) % 4][1])
                dashed(d, a[0], a[1], b[0], b[1], LGRAY, 2)
        pts = [(ox + c[0], oy + c[1]) for c in corners]
        d.polygon(pts, outline=col, width=3)

    # 一様伸び(ξ方向)
    elem(70, 130, [(-14, 0), (124, 0), (124, 90), (-14, 90)], GREEN)
    ctext(d, 125, 245, "一様伸び", FT, GREEN)
    ctext(d, 125, 268, "(表現できる)", FT, GRAY)
    # せん断
    elem(270, 130, [(22, 0), (132, 0), (88, 90), (-22, 90)], GREEN)
    ctext(d, 325, 245, "せん断", FT, GREEN)
    ctext(d, 325, 268, "(表現できる)", FT, GRAY)
    # 曲げ(2次変形) : 上辺短縮・下辺伸長を直線辺のまま近似 → 表せない
    ox, oy = 470, 130
    d.line((ox + 20, oy, ox + 90, oy), fill=RED, width=3)       # 上辺(縮む)
    d.line((ox - 10, oy + 90, ox + 120, oy + 90), fill=RED, width=3)  # 下辺(伸びる)
    d.line((ox + 20, oy, ox - 10, oy + 90), fill=RED, width=3)
    d.line((ox + 90, oy, ox + 120, oy + 90), fill=RED, width=3)
    # 本来の曲がり(曲線)を破線で
    dashed(d, ox + 20, oy, ox + 90, oy, GRAY, 2)
    ctext(d, ox + 55, 245, "曲げ", FT, RED)
    ctext(d, ox + 55, 268, "(座標に2次で変化)", FT, RED)
    ctext(d, W / 2, 320, "曲げは断面内で応力・ひずみが2次的に変化 → 1次要素単独では表せない", FT, GRAY)
    note(d, "一様伸び・せん断は1次で表現可。曲げは細分・高次要素・非適合モードで補う。")
    save(im, "f5BendLimit")


# ============================================================
# fem-5-7 ヤコビ行列の役割
# ============================================================
def f5Jacobian():
    im, d = new(); title(d, "ヤコビ行列 J:局所と全体の微分を結ぶ")
    box(d, 45, 165, 205, 245, FILL1)
    mlines(d, 125, 205, ["局所での微分", "∂N/∂ξ , ∂N/∂η"], FT, BLACK, 26)
    arrow(d, 208, 205, 300, 205, BLACK, 3, 14)
    ctext(d, 254, 182, "J⁻¹ を掛ける", FT, BLUE)
    box(d, 303, 165, 470, 245, FILL1)
    mlines(d, 386, 205, ["全体での微分", "∂N/∂x , ∂N/∂y"], FT, BLACK, 26)
    arrow(d, 473, 205, 545, 205, BLACK, 3, 14)
    box(d, 548, 170, 618, 240, FILL2, col=RED)
    ctext(d, 583, 205, "[B]", FS, RED)
    # J行列
    vals = [["∂x/∂ξ", "∂y/∂ξ"], ["∂x/∂η", "∂y/∂η"]]
    matrix_grid(d, 210, 275, vals, cell=95, fnt=FT)
    ctext(d, 305, 275 + 190 + 4, "ヤコビ行列 J", FT, GRAY)
    note(d, "連鎖律で局所↔全体の微分を橋渡し。J⁻¹ を掛けて[B]に必要な全体微分を得る。")
    save(im, "f5Jacobian")


# ============================================================
# fem-5-8 非適合モード
# ============================================================
def f5Incompatible():
    im, d = new(); title(d, "非適合モード:1次要素に曲げ表現を追加")
    x0, y0, s = 90, 110, 150
    box(d, x0, y0, x0 + s, y0 + s, FILL1)
    for p in [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    # 内部の放物線バブル(節点で0)
    cx = x0 + s / 2
    ptsh = [(x0 + i, y0 + s / 2 - 34 * (1 - ((i - s / 2) / (s / 2)) ** 2))
            for i in range(0, s + 1, 6)]
    d.line(ptsh, fill=RED, width=3, joint="curve")
    cy = y0 + s / 2
    ptsv = [(cx - 34 * (1 - ((j - s / 2) / (s / 2)) ** 2), y0 + j)
            for j in range(0, s + 1, 6)]
    d.line(ptsv, fill=BLUE, width=3, joint="curve")
    ctext(d, cx, y0 + s + 22, "内部モード(節点で0)", FT, GRAY)
    box(d, 290, 110, 615, 175, FILL2)
    ctext(d, 452, 142, "N5=1−ξ² , N6=1−η²", FS, BLACK)
    box(d, 290, 190, 615, 250, FILL1)
    mlines(d, 452, 220, ["曲げ(純曲げ)の変形を追加", "→ 要素の曲げ表現能力↑"], FT, BLACK, 26)
    box(d, 290, 265, 615, 325, FILL1, col=BLUE)
    mlines(d, 452, 295, ["静的縮約で消去 → 全体の未知数は増えない", "ただし要素間の適合性は失われる"], FT, BLUE, 26)
    note(d, "節点を持たない内部変数。静的縮約で消せるため全体自由度は増えないが適合性は犠牲。")
    save(im, "f5Incompatible")


# ============================================================
# fem-5-9 セレンディピティ vs ラグランジュ
# ============================================================
def f5SerendipLagrange():
    im, d = new(); title(d, "ラグランジュ要素とセレンディピティ要素")
    x0, y0, s = 100, 135, 150
    box(d, x0, y0, x0 + s, y0 + s, FILL1)
    corners = [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]
    mids = [(x0 + s / 2, y0), (x0 + s / 2, y0 + s), (x0, y0 + s / 2), (x0 + s, y0 + s / 2)]
    for p in corners + mids:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    node(d, x0 + s / 2, y0 + s / 2, 6, fill=RED, col=RED)  # 内部節点
    ctext(d, x0 + s / 2, y0 + s + 26, "9節点ラグランジュ要素", FS, BLUE)
    ctext(d, x0 + s / 2, y0 + s + 52, "内部節点(赤)を持つ", FT, RED)
    x1 = 415
    box(d, x1, y0, x1 + s, y0 + s, FILL1)
    corners2 = [(x1, y0), (x1 + s, y0), (x1, y0 + s), (x1 + s, y0 + s)]
    mids2 = [(x1 + s / 2, y0), (x1 + s / 2, y0 + s), (x1, y0 + s / 2), (x1 + s, y0 + s / 2)]
    for p in corners2 + mids2:
        node(d, p[0], p[1], 5, fill=BLACK, col=BLACK)
    ctext(d, x1 + s / 2, y0 + s + 26, "8節点セレンディピティ要素", FS, BLUE)
    ctext(d, x1 + s / 2, y0 + s + 52, "内部節点を持たない", FT, GRAY)
    note(d, "ラグランジュ=内部節点も配置。セレンディピティ=節点を境界中心にし内部節点を減らす。")
    save(im, "f5SerendipLagrange")


# ============================================================
# fem-5-10 変位2次 → ひずみ1次(微分で次数-1)
# ============================================================
def f5DispStrainOrder():
    im, d = new(); title(d, "8節点要素:変位は2次・ひずみは1次")
    axes(d, 90, 285, 210, 170, "x", "u")
    pts = [(90 + i * 4, 285 - (60 + 90 * ((i * 4) / 200.0) - 70 * ((i * 4) / 200.0) ** 2))
           for i in range(0, 51)]
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, 195, 118, "変位 u", FS, BLUE)
    ctext(d, 195, 305, "概ね2次(放物線)", FT, GRAY)
    axes(d, 400, 285, 210, 170, "x", "ε")
    d.line((418, 250, 590, 170), fill=GREEN, width=3)
    ctext(d, 505, 118, "ひずみ ε = du/dx", FS, GREEN)
    ctext(d, 505, 305, "概ね1次(直線)", FT, GRAY)
    arrow(d, 305, 200, 395, 200, RED, 3, 13)
    ctext(d, 350, 178, "微分", FT, RED)
    ctext(d, 350, 222, "次数−1", FT, RED)
    note(d, "ひずみは変位の微分なので次数が1つ下がる:変位2次 → ひずみ1次。")
    save(im, "f5DispStrainOrder")


# ============================================================
# fem-5-13 死荷重
# ============================================================
def f5DeadLoad():
    im, d = new(); title(d, "死荷重(一定・不変)と活荷重(変動)")
    box(d, 55, 95, 320, 330, FILL1, col=BLUE)
    box(d, 350, 95, 610, 330, FILL2)
    ctext(d, 187, 120, "死荷重", FS, BLUE)
    # 梁に一定の下向き矢印
    d.line((85, 175, 290, 175), fill=BLACK, width=4)
    for xx in range(100, 291, 38):
        arrow(d, xx, 150, xx, 173, RED, 3, 9)
    mlines(d, 187, 250, ["時間・変形に依存せず", "常に一定の大きさ・向き", "例:自重", "対語=活荷重"], FT, BLACK, 28)
    ctext(d, 480, 120, "活荷重", FS, BLACK)
    d.line((375, 175, 585, 175), fill=BLACK, width=4)
    for xx, h in zip(range(392, 586, 38), [14, 26, 18, 30, 20, 12]):
        arrow(d, xx, 173 - h - 23, xx, 173, GRAY, 3, 9)
    mlines(d, 480, 250, ["大きさ・作用位置が変化", "移動荷重・変動荷重", "地震・風など"], FT, BLACK, 28)
    note(d, "死荷重=時間にも変形にも依存しない一定荷重。変動する荷重は活荷重・動的荷重。")
    save(im, "f5DeadLoad")


# ============================================================
# fem-5-16 ディリクレ=値そのもの / ノイマン=微分値
# ============================================================
def f5DirichletValue():
    im, d = new(); title(d, "ディリクレ条件とノイマン条件")
    box(d, 55, 90, 320, 320, FILL1, col=BLUE)
    box(d, 350, 90, 610, 320, FILL2)
    ctext(d, 187, 116, "ディリクレ条件", FS, BLUE)
    ctext(d, 187, 143, "(第1種・基本)", FT, GRAY)
    mlines(d, 187, 220, ["物理量そのもの=変位を指定", "0 でない強制変位も可", "剛体移動を拘束し", "方程式を解ける形にする"], FT, BLACK, 30)
    ctext(d, 480, 116, "ノイマン条件", FS, BLUE)
    ctext(d, 480, 143, "(第2種・自然)", FT, GRAY)
    mlines(d, 480, 205, ["物理量の微分値=力を指定", "(構造なら力・応力)"], FT, BLACK, 30)
    # 小さな棒:左固定(値)・右に力(微分値)
    wall(d, 370, 250, 300, side=1, n=4)
    d.rectangle((370, 262, 560, 288), outline=BLACK, width=3, fill=FILL1)
    force(d, 560, 275, 40, 0, "F", RED)
    ctext(d, W / 2, 345, "ディリクレ=値そのもの / ノイマン=微分値", FT, RED)
    note(d, "ディリクレ=変位(値)を指定し剛体移動を拘束。ノイマン=力(微分値)を指定する。")
    save(im, "f5DirichletValue")


# ============================================================
# fem-5-18 熱伝導の境界条件
# ============================================================
def f5ThermalBC():
    im, d = new(); title(d, "熱伝導問題の境界条件")
    box(d, 250, 150, 410, 270, FILL1)
    ctext(d, 330, 210, "解析領域", FS, GRAY)
    ctext(d, 330, 234, "(温度場 T)", FT, GRAY)
    # ディリクレ(左)
    d.line((250, 150, 250, 270), fill=RED, width=5)
    ctext(d, 150, 190, "ディリクレ", FT, RED)
    ctext(d, 150, 214, "節点温度 T を指定", FT, BLACK)
    arrow(d, 235, 240, 250, 240, RED, 2, 9)
    # ノイマン(右)
    arrow(d, 410, 190, 445, 190, BLUE, 3, 12)
    ctext(d, 510, 176, "ノイマン", FT, BLUE)
    ctext(d, 510, 200, "熱流束 q を指定", FT, BLACK)
    ctext(d, 510, 224, "(断熱は q=0)", FT, GRAY)
    # ロビン(下)
    for xx in range(275, 386, 26):
        arrow(d, xx, 300, xx, 272, GREEN, 2, 8)
    ctext(d, 330, 320, "ロビン(対流):熱伝達係数 h・周囲温度 T∞ を指定", FT, GREEN)
    note(d, "ディリクレ=温度指定、ノイマン=熱流束(断熱=0)、ロビン=対流。温度指定がディリクレ。")
    save(im, "f5ThermalBC")


# ============================================================
# fem-5-21 荷重(ノイマン)=右辺のみ操作
# ============================================================
def f5NeumannLoad():
    im, d = new(); title(d, "荷重(力)境界条件の処理:右辺だけを操作")
    ctext(d, 120, 200, "[ K ]", FL, BLACK)
    box(d, 78, 168, 168, 232, None, wd=2, col=GRAY)
    ctext(d, 120, 258, "剛性行列", FT, GRAY)
    ctext(d, 120, 282, "(材料・形状で決まる)", FT, GRAY)
    ctext(d, 120, 306, "変更しない", FT, BLUE)
    ctext(d, 210, 200, "{ u }", F, BLACK)
    ctext(d, 275, 200, "=", FL, BLACK)
    box(d, 320, 168, 420, 232, FILL2, col=RED)
    ctext(d, 370, 200, "{ f }", F, RED)
    ctext(d, 370, 258, "荷重ベクトル", FT, RED)
    ctext(d, 370, 282, "(右辺)", FT, GRAY)
    arrow(d, 470, 200, 435, 200, RED, 3, 13)
    mlines(d, 545, 205, ["等価節点力を", "ここに加算する"], FT, RED, 26)
    note(d, "力(ノイマン)条件は右辺の荷重ベクトルに加算するだけ。剛性行列Kは変更しない。")
    save(im, "f5NeumannLoad")


# ============================================================
# fem-5-22 熱応力に必要な材料定数
# ============================================================
def f5ThermalConst():
    im, d = new(); title(d, "熱応力解析に必要な材料定数")
    labels = [(160, "E", "縦弾性係数"), (330, "ν", "ポアソン比"), (500, "α", "線膨張係数")]
    for cx, sym, name in labels:
        col = RED if sym == "α" else BLUE
        box(d, cx - 78, 120, cx + 78, 250, FILL2 if sym == "α" else FILL1, col=col)
        ctext(d, cx, 170, sym, FL, col)
        ctext(d, cx, 215, name, FT, BLACK)
    ctext(d, 245, 185, "＋", F, BLACK)
    ctext(d, 415, 185, "＋", F, BLACK)
    ctext(d, 500, 278, "温度変化で必須", FT, RED)
    ctext(d, W / 2, 315, "熱ひずみ(初期ひずみ) ε0 = α ΔT", FS, BLACK)
    note(d, "E・ν に加え線膨張係数αが必須。密度・比熱・熱伝導率は熱応力の計算には直接不要。")
    save(im, "f5ThermalConst")


# ============================================================
# fem-5-23 自由膨張の熱ひずみ ε0=αΔT(応力ゼロ)
# ============================================================
def f5ThermalStrainFree():
    im, d = new(); title(d, "拘束のない自由膨張と熱ひずみ")
    y0, y1 = 150, 220
    # 変形前(破線)
    for xx in (110, 430):
        pass
    dashed(d, 110, y0, 430, y0, GRAY, 2)
    dashed(d, 110, y1, 430, y1, GRAY, 2)
    dashed(d, 430, y0, 430, y1, GRAY, 2)
    dashed(d, 110, y0, 110, y1, GRAY, 2)
    ctext(d, 270, y0 - 16, "温度上昇前", FT, GRAY)
    # 変形後(実線・伸長)
    d.rectangle((110, y0, 510, y1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 310, (y0 + y1) / 2, "自由に伸びる(拘束なし)", FT, BLACK)
    arrow(d, 435, (y0 + y1) / 2, 505, (y0 + y1) / 2, RED, 3, 12)
    ctext(d, 300, y1 + 30, "温度上昇 ΔT", FT, RED)
    ctext(d, W / 2, 300, "熱ひずみ(初期ひずみ) ε0 = α ΔT", FS, BLACK)
    ctext(d, W / 2, 330, "拘束がなければ自由に伸縮 → 応力は生じない", FT, GRAY)
    note(d, "自由膨張では熱ひずみ ε0=αΔT だけ伸び、拘束がないため応力は発生しない。")
    save(im, "f5ThermalStrainFree")


# ============================================================
# fem-5-28 残留応力・初期ひずみ法
# ============================================================
def f5ResidualStrain():
    im, d = new(); title(d, "残留応力の解析(初期ひずみ法)")
    ys = [70, 150, 230]
    steps = ["① 部材Aを引張った状態で部材Bに接着する",
             "② 外力を取り除く → Aは自然長へ戻ろうとし、Bが妨げる",
             "③ 初期ひずみ法:引張で生じたひずみと逆符号の"]
    for y, t in zip(ys, steps):
        box(d, 55, y, 605, y + 52, FILL1)
        ctext(d, 330, y + 26, t, FT, BLACK)
        if y != ys[-1]:
            arrow(d, 330, y + 52, 330, y + 70, BLACK, 3, 12)
    ctext(d, 330, ys[-1] + 74, "初期ひずみを部材Aに与えて線形弾性解析 → 残留応力", FT, RED)
    note(d, "自然形状へ戻すため、引張で生じたひずみの逆符号を初期ひずみとしてAに与える。")
    save(im, "f5ResidualStrain")


# ============================================================
# fem-5-29 変位法の解析手順
# ============================================================
def f5SolveFlow():
    im, d = new(); title(d, "変位法(剛性法)の解析手順")
    steps = ["各要素の\n要素剛性行列\nを作成",
             "全体剛性行列\nへ組み立て\n(アセンブリ)",
             "境界条件\n(拘束・荷重)\nを適用",
             "連立方程式\nK u = f\nを解く",
             "変位から\nひずみ・応力\nを計算"]
    n = len(steps)
    bw, gap = 108, 12
    x0 = (W - (n * bw + (n - 1) * gap)) / 2
    y0, y1 = 150, 270
    for i, s in enumerate(steps):
        x = x0 + i * (bw + gap)
        f = FILL2 if i == n - 1 else FILL1
        box(d, x, y0, x + bw, y1, f)
        mlines(d, x + bw / 2, (y0 + y1) / 2, s.split("\n"), FT, BLACK, 26)
        if i < n - 1:
            arrow(d, x + bw, (y0 + y1) / 2, x + bw + gap, (y0 + y1) / 2, BLACK, 3, 9)
    ctext(d, W / 2, 305, "部品を作る → 組み立てる → 条件を入れる → 解く → 後処理", FT, GRAY)
    note(d, "応力・ひずみは変位が求まった後の後処理。順序を崩さないことが要点。")
    save(im, "f5SolveFlow")


ALL = [f5IsoConcept, f5IsoSuperSub, f5NodeOrder, f5QuadTriCoord, f5CoordMap, f5BendLimit,
       f5Jacobian, f5Incompatible, f5SerendipLagrange, f5DispStrainOrder, f5DeadLoad,
       f5DirichletValue, f5ThermalBC, f5NeumannLoad, f5ThermalConst, f5ThermalStrainFree,
       f5ResidualStrain, f5SolveFlow]

KEYS = ["f5IsoConcept", "f5IsoSuperSub", "f5NodeOrder", "f5QuadTriCoord", "f5CoordMap",
        "f5BendLimit", "f5Jacobian", "f5Incompatible", "f5SerendipLagrange",
        "f5DispStrainOrder", "f5DeadLoad", "f5DirichletValue", "f5ThermalBC",
        "f5NeumannLoad", "f5ThermalConst", "f5ThermalStrainFree", "f5ResidualStrain",
        "f5SolveFlow"]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    miss = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(KEYS), "MISSING", miss)
