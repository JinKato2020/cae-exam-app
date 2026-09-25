# -*- coding: utf-8 -*-
"""振動2級 第2章 動力学の基礎 の図（全30枚）。
問題図=接頭辞 v2e2（23枚）、公式図=接頭辞 v2f2（7枚）。
白地660×420・黒線画（figlib準拠）。required問題図は答え・結論を描かない。
実行: python tools/figs_vib2ch2.py
"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
import math
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, note,
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


def block(d, cx, cy, w, h, label="", fnt=F, fill=FILL1, col=BLACK):
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


def panel_sep(d, xs, y0=64, y1=402):
    for x in xs:
        d.line((x, y0, x, y1), fill=LGRAY, width=2)


# ============================================================
# 問題図 v2e2（23枚）
# ============================================================

def newton_three_laws(name):  # 2-1 required
    im, d = new()
    title(d, "ニュートンの運動の3法則（概念）")
    panel_sep(d, [230, 430])
    # 第一法則: 力なしで等速
    ctext(d, 130, 96, "第一法則（慣性）", FS)
    block(d, 130, 250, 60, 40, "m")
    arrow(d, 70, 200, 190, 200, BLUE, 3, 12); ctext(d, 130, 182, "v（一定）", FT, BLUE)
    ctext(d, 130, 320, "力 = 0", FS, GRAY)
    # 第二法則: 力の矢印と加速度の矢印
    ctext(d, 330, 96, "第二法則（運動）", FS)
    block(d, 320, 250, 60, 40, "m")
    force(d, 350, 235, 70, 0, "f", RED)
    arrow(d, 300, 300, 380, 300, BLUE, 3, 12); ctext(d, 340, 318, "a", FT, BLUE)
    # 第三法則: 作用反作用
    ctext(d, 530, 96, "第三法則（作用・反作用）", FT)
    block(d, 495, 250, 50, 40, "A")
    block(d, 565, 250, 50, 40, "B")
    arrow(d, 522, 220, 560, 220, RED, 3, 12); ctext(d, 541, 204, "f", FT, RED)
    arrow(d, 538, 285, 500, 285, RED, 3, 12); ctext(d, 519, 300, "f", FT, RED)
    save(im, name)


def momentum_force_law(name):  # 2-2 required
    im, d = new()
    title(d, "運動量 p=mv と外力 f")
    # 質点と運動量・外力
    node(d, 250, 210, 12, FILL2, BLACK); ctext(d, 250, 210, "m", FS)
    arrow(d, 262, 210, 430, 210, BLUE, 4, 15); ctext(d, 380, 192, "運動量 p = mv", FS, BLUE)
    arrow(d, 250, 250, 400, 250, RED, 4, 15); ctext(d, 360, 270, "外力 f", FS, RED)
    ctext(d, 250, 150, "d(mv)/dt = f", FS, GRAY)
    # 作用反作用の小図
    d.line((150, 300, 560, 300), fill=LGRAY, width=2)
    ctext(d, 355, 322, "作用・反作用（2物体）", FT, GRAY)
    block(d, 300, 365, 46, 34, "A")
    block(d, 360, 365, 46, 34, "B")
    arrow(d, 324, 348, 356, 348, RED, 3, 11); ctext(d, 340, 338, "f", FT, RED)
    arrow(d, 336, 384, 304, 384, RED, 3, 11); ctext(d, 320, 394, "f", FT, RED)
    save(im, name)


def proportion_accel(name):  # 2-3 required
    im, d = new()
    title(d, "質量 m に力 f を加える")
    hwall(d, 120, 540, 320, side=1, n=14)
    block(d, 250, 285, 90, 60, "m")
    force(d, 295, 270, 110, 0, "f", RED)
    arrow(d, 200, 350, 330, 350, BLUE, 4, 14); ctext(d, 265, 372, "加速度 a", FS, BLUE)
    note(d, "力 f を加えると同じ向きに加速度 a が生じる")
    save(im, name)


def translation_1d(name):  # 2-4 required
    im, d = new()
    title(d, "x 軸上を並進する質点 m")
    ox, oy = 120, 280
    arrow(d, ox, oy, 600, oy, BLACK, 2, 11); ctext(d, 606, oy, "x", FS, BLACK, "lm")
    ctext(d, ox, oy + 20, "O", FS)
    px = 360
    dash(d, px, oy, px, 200, GRAY)
    block(d, px, 200, 74, 46, "m")
    dim(d, ox, 335, px, 335, "位置 x", col=GRAY)
    force(d, px + 37, 190, 90, 0, "f", RED)
    arrow(d, px - 45, 235, px + 45, 235, BLUE, 3, 12); ctext(d, px, 253, "v", FT, BLUE)
    arrow(d, px - 45, 160, px + 45, 160, GREEN, 3, 12); ctext(d, px, 146, "a", FT, GREEN)
    save(im, name)


def spring_mass_force(name):  # 2-5 required
    im, d = new()
    title(d, "ばね（ばね定数 k）の他端に力 f")
    hwall(d, 90, 590, 300, side=1, n=15)
    block(d, 170, 265, 84, 60, "m")
    spring(d, 212, 265, 430, 265, coils=6, amp=15)
    ctext(d, 320, 232, "k", FS)
    node(d, 430, 265, 6, BLACK, BLACK)
    force(d, 435, 265, 105, 0, "f", RED)
    note(d, "ばねの質量は無視。他端に力 f を加える")
    save(im, name)


def inertial_frames(name):  # 2-6 required
    im, d = new()
    title(d, "4つの座標系")
    panel_sep(d, [340], 60, 400)
    d.line((60, 232, 620, 232), fill=LGRAY, width=2)
    cells = [(180, 150, "(ア) 静止", "static"),
             (490, 150, "(イ) 等速並進", "uniform"),
             (180, 320, "(ウ) 等加速度並進", "accel"),
             (490, 320, "(エ) 回転", "rotate")]
    for cx, cy, lab, kind in cells:
        ctext(d, cx, cy - 62, lab, FS)
        # 座標十字
        arrow(d, cx - 40, cy, cx + 40, cy, BLACK, 2, 9)
        arrow(d, cx, cy + 30, cx, cy - 35, BLACK, 2, 9)
        if kind == "static":
            ctext(d, cx + 46, cy + 30, "v = 0", FT, GRAY)
        elif kind == "uniform":
            arrow(d, cx + 8, cy + 46, cx + 60, cy + 46, BLUE, 3, 11)
            ctext(d, cx + 34, cy + 60, "v（一定）", FT, BLUE)
        elif kind == "accel":
            arrow(d, cx + 8, cy + 46, cx + 60, cy + 46, GREEN, 3, 11)
            ctext(d, cx + 40, cy + 60, "a", FT, GREEN)
        else:
            curve_arrow(d, cx, cy, 48, 20, 150, ORANGE, 3, 11)
            ctext(d, cx - 4, cy - 60, "ω", FT, ORANGE)
    save(im, name)


def non_inertial(name):  # 2-7 required
    im, d = new()
    title(d, "非慣性系（加速度 a0 で運動）から観測")
    # 観測者の座標系（枠）
    d.rectangle((90, 150, 570, 360), outline=GRAY, width=2)
    ctext(d, 175, 172, "観測者の座標系", FT, GRAY)
    arrow(d, 110, 330, 200, 330, BLACK, 2, 10); ctext(d, 206, 330, "x'", FT, BLACK, "lm")
    arrow(d, 110, 330, 110, 250, BLACK, 2, 10)
    # 座標系の加速度 a0
    arrow(d, 300, 128, 430, 128, GREEN, 4, 14); ctext(d, 365, 112, "座標系の加速度 a0", FT, GREEN)
    # 質点と 実力 f・慣性力 -m a0
    node(d, 330, 265, 13, FILL2, BLACK); ctext(d, 330, 265, "m", FS)
    arrow(d, 343, 265, 470, 265, RED, 4, 15); ctext(d, 470, 247, "実力 f", FS, RED)
    arrow(d, 317, 265, 200, 265, BLUE, 4, 15); ctext(d, 195, 283, "慣性力 -m a0", FS, BLUE, "rm")
    save(im, name)


def projectile_init(name):  # 2-8 helpful
    im, d = new()
    title(d, "鉛直投げ上げの初期条件（t=0）")
    hwall(d, 120, 560, 370, side=1, n=13)
    bx = 250
    # 軌道（上昇→頂点→下降）を少し横に開いて可視化
    pts = []
    for i in range(41):
        t = i / 40.0
        y = 370 - 210 * (4 * t * (1 - t))       # 放物（高さ）
        x = bx + 60 * t                          # わずかに右へ
        pts.append((x, y))
    dash_pts = pts
    for k in range(len(dash_pts) - 1):
        if k % 2 == 0:
            d.line([dash_pts[k], dash_pts[k + 1]], fill=GRAY, width=2)
    node(d, bx, 370, 10, RED, RED)
    ctext(d, bx - 16, 388, "初期位置 x0", FT, RED, "rm")
    arrow(d, bx, 360, bx, 250, BLUE, 4, 15); ctext(d, bx - 12, 300, "初速 v0", FS, BLUE, "rm")
    # 重力
    arrow(d, 470, 200, 470, 280, GREEN, 3, 12); ctext(d, 484, 240, "g", FS, GREEN, "lm")
    note(d, "任意時刻の運動は 運動方程式 + 初期位置 x0・初速 v0 で定まる")
    save(im, name)


def momentum_conserv(name):  # 2-9 required
    im, d = new()
    title(d, "2質点が内力を及ぼし合う（衝突）")
    hwall(d, 90, 590, 330, side=1, n=15)
    node(d, 230, 290, 26, FILL2, BLACK); ctext(d, 230, 290, "m1", FS)
    node(d, 430, 290, 26, FILL3, BLACK); ctext(d, 430, 290, "m2", FS)
    arrow(d, 150, 240, 210, 240, BLUE, 3, 12); ctext(d, 178, 224, "v1", FT, BLUE)
    arrow(d, 510, 240, 450, 240, BLUE, 3, 12); ctext(d, 482, 224, "v2", FT, BLUE)
    # 内力の対
    arrow(d, 300, 290, 356, 290, RED, 4, 13); ctext(d, 330, 308, "f", FT, RED)
    arrow(d, 360, 320, 304, 320, RED, 4, 13); ctext(d, 332, 336, "-f", FT, RED)
    ctext(d, 330, 264, "内力の対", FT, GRAY)
    save(im, name)


def momentum_vs_energy(name):  # 2-10 helpful
    im, d = new()
    title(d, "運動方程式から2つの保存則へ")
    block(d, 330, 130, 260, 56, "運動方程式  ma = f", FS, FILL1)
    arrow(d, 300, 158, 185, 250, BLACK, 3, 13); ctext(d, 205, 208, "時間で積分", FT, GRAY)
    arrow(d, 360, 158, 475, 250, BLACK, 3, 13); ctext(d, 458, 208, "×v して積分", FT, GRAY)
    block(d, 175, 300, 240, 60, "運動量保存\nΣ m v = 一定", FS, FILL2)
    block(d, 485, 300, 240, 60, "力学的エネルギー保存\n½mv² + U = 一定", FS, FILL2)
    note(d, "出発点は同じ運動方程式だが、量も意味も異なる")
    save(im, name)


def stacked_blocks(name):  # 2-11 required
    im, d = new()
    title(d, "なめらかな床の台 m1 の上に物体 m2")
    # なめらかな床（コロで表現）
    d.line((90, 330, 590, 330), fill=BLACK, width=3)
    for cx in range(120, 580, 44):
        d.ellipse((cx, 330, cx + 16, 346), outline=GRAY, width=2)
    ctext(d, 500, 360, "なめらか（摩擦なし）", FT, GRAY)
    block(d, 300, 300, 200, 46, "台 m1", F, FILL1)   # 台
    block(d, 300, 255, 90, 44, "m2", F, FILL3)        # 物体
    ctext(d, 300, 210, "m1・m2 間には摩擦あり", FT, GRAY)
    arrow(d, 405, 300, 500, 300, RED, 4, 15); ctext(d, 500, 282, "初速 v0", FS, RED, "lm")
    save(im, name)


def conservation_conditions(name):  # 2-12 helpful
    im, d = new()
    title(d, "保存則が成り立つ条件（整理）")
    x0, y0, cw, ch = 210, 110, 190, 66
    cols = ["内力のみ\n(外力なし)", "保存力のみ\n(非保存力の仕事0)"]
    rows = ["運動量保存", "エネルギー保存"]
    cells = [["○", "外力あれば×"], ["摩擦あれば×", "○"]]
    # 列見出し
    for j, cl in enumerate(cols):
        ctext(d, x0 + cw / 2 + j * cw, y0 - 26, cl, FT, BLACK)
    # 行見出し + グリッド
    for i in range(3):
        d.line((x0, y0 + i * ch, x0 + 2 * cw, y0 + i * ch), fill=BLACK, width=2)
    for j in range(3):
        d.line((x0 + j * cw, y0, x0 + j * cw, y0 + 2 * ch), fill=BLACK, width=2)
    for i, rw in enumerate(rows):
        ctext(d, x0 - 60, y0 + ch / 2 + i * ch, rw, FT, BLACK)
        for j in range(2):
            val = cells[i][j]
            col = GREEN if val == "○" else GRAY
            ctext(d, x0 + cw / 2 + j * cw, y0 + ch / 2 + i * ch, val, FT, col)
    note(d, "運動量は『外力ゼロ』、エネルギーは『非保存力の仕事ゼロ』で保存")
    save(im, name)


def friction_fbd(name):  # 2-13 required
    im, d = new()
    title(d, "水平面上の物体の自由物体図")
    hwall(d, 100, 560, 320, side=1, n=15)
    block(d, 320, 285, 130, 66, "m")
    arrow(d, 320, 285, 320, 165, BLUE, 4, 15); ctext(d, 320, 150, "N（垂直抗力）", FS, BLUE)
    arrow(d, 320, 285, 320, 400, GREEN, 4, 15); ctext(d, 320, 402, "重力 mg", FS, GREEN, "mm")
    arrow(d, 385, 285, 500, 285, RED, 4, 15); ctext(d, 505, 285, "引く力", FS, RED, "lm")
    arrow(d, 255, 285, 150, 285, ORANGE, 4, 15); ctext(d, 145, 285, "摩擦力 F", FS, ORANGE, "rm")
    save(im, name)


def central_force(name):  # 2-14 required
    im, d = new()
    title(d, "中心力を受ける質点")
    ox, oy = 330, 250
    R = 140
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    node(d, ox, oy, 6, BLACK, BLACK); ctext(d, ox - 14, oy + 6, "O", FS, BLACK, "rm")
    ang = math.radians(40)
    px, py = ox + R * math.cos(ang), oy - R * math.sin(ang)
    node(d, px, py, 11, FILL2, BLACK); ctext(d, px + 10, py - 12, "m", FS, BLACK, "lm")
    # 位置ベクトル r
    arrow(d, ox, oy, px, py, GRAY, 2, 11); ctext(d, (ox + px) / 2 + 6, (oy + py) / 2 - 14, "r", FS, GRAY)
    # 中心へ向かう力
    arrow(d, px, py, px - 78 * math.cos(ang), py + 78 * math.sin(ang), RED, 4, 14)
    ctext(d, px - 40 * math.cos(ang) + 14, py + 40 * math.sin(ang) + 12, "中心力", FT, RED, "lm")
    # 接線方向の速度
    tx, ty = -math.sin(ang), -math.cos(ang)
    arrow(d, px, py, px + 80 * tx, py + 80 * ty, BLUE, 3, 12); ctext(d, px + 80 * tx - 14, py + 80 * ty - 6, "v", FS, BLUE, "rm")
    save(im, name)


def time_derivatives(name):  # 2-15 helpful
    im, d = new()
    title(d, "運動量・角運動量・エネルギーの微分関係")
    rows = [("運動量 p = mv", "d/dt", "外力 f"),
            ("角運動量 L", "d/dt", "モーメント T"),
            ("運動エネルギー ½mv²", "d/dv", "運動量 mv")]
    for i, (a, op, b) in enumerate(rows):
        y = 130 + i * 90
        block(d, 190, y, 230, 56, a, FS, FILL1)
        arrow(d, 310, y, 430, y, BLACK, 3, 13); ctext(d, 370, y - 18, op, FT, GRAY)
        block(d, 540, y, 180, 56, b, FS, FILL2)
    save(im, name)


def circular_motion(name):  # 2-16 required
    im, d = new()
    title(d, "原点まわりの円運動（半径 l・角速度 ω）")
    ox, oy = 300, 250
    R = 150
    arrow(d, ox - 200, oy, ox + 230, oy, BLACK, 2, 10); ctext(d, ox + 236, oy, "x", FT, BLACK, "lm")
    arrow(d, ox, oy + 130, ox, oy - 200, BLACK, 2, 10); ctext(d, ox - 12, oy - 205, "y", FT, BLACK, "rm")
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    node(d, ox, oy, 6, BLACK, BLACK); ctext(d, ox - 14, oy + 8, "O", FS, BLACK, "rm")
    ang = math.radians(52)
    px, py = ox + R * math.cos(ang), oy - R * math.sin(ang)
    d.line((ox, oy, px, py), fill=GRAY, width=2); ctext(d, (ox + px) / 2 - 12, (oy + py) / 2, "l", FS, GRAY)
    node(d, px, py, 12, FILL2, BLACK); ctext(d, px + 12, py - 12, "m", FS, BLACK, "lm")
    tx, ty = -math.sin(ang), -math.cos(ang)
    arrow(d, px, py, px + 78 * tx, py + 78 * ty, BLUE, 3, 12); ctext(d, px + 78 * tx - 10, py + 78 * ty - 12, "v", FS, BLUE, "rm")
    curve_arrow(d, ox, oy, 52, 30, 90, ORANGE, 3, 11); ctext(d, ox + 74, oy - 16, "ω", FS, ORANGE)
    save(im, name)


def radius_halved(name):  # 2-17 required
    im, d = new()
    title(d, "糸をたぐり半径を l → l/2 に縮める")
    ox, oy = 330, 240
    R = 150
    node(d, ox, oy, 6, BLACK, BLACK); ctext(d, ox, oy + 18, "O", FS)
    # before
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    p1 = (ox + R * math.cos(math.radians(35)), oy - R * math.sin(math.radians(35)))
    d.line((ox, oy, p1[0], p1[1]), fill=GRAY, width=2)
    dim(d, ox, oy + 175, ox + R, oy + 175, "l", col=GRAY)
    node(d, p1[0], p1[1], 10, FILL2, BLACK)
    ctext(d, p1[0] + 12, p1[1] - 12, "m（初め）", FT, BLACK, "lm")
    # after
    R2 = R / 2
    d.ellipse((ox - R2, oy - R2, ox + R2, oy + R2), outline=BLUE, width=2)
    p2 = (ox + R2 * math.cos(math.radians(120)), oy - R2 * math.sin(math.radians(120)))
    d.line((ox, oy, p2[0], p2[1]), fill=BLUE, width=2)
    node(d, p2[0], p2[1], 10, FILL3, BLUE)
    ctext(d, p2[0] - 12, p2[1] - 12, "m（縮めた後 半径 l/2）", FT, BLUE, "rm")
    save(im, name)


def centroid_inertia(name):  # 2-18 helpful
    im, d = new()
    title(d, "重心と慣性モーメント（軸依存）")
    # 同一物体（矩形板）
    d.rectangle((210, 200, 450, 300), outline=BLACK, width=3, fill=FILL1)
    G = (330, 250)
    node(d, G[0], G[1], 6, BLACK, BLACK); ctext(d, G[0], G[1] - 20, "G（重心）", FT, BLACK)
    # 重心を通る軸
    dash(d, G[0], 150, G[0], 350, RED)
    ctext(d, G[0], 138, "重心軸  I_G", FT, RED)
    # 別位置の軸
    ax = 450
    dash(d, ax, 150, ax, 350, BLUE)
    ctext(d, ax + 6, 138, "別の軸  I", FT, BLUE, "lm")
    dim(d, G[0], 330, ax, 330, "h", col=GRAY)
    note(d, "重心は物体固有／慣性モーメントは軸のとり方で変わる（I = I_G + M h²）")
    save(im, name)


def bar_two_masses(name):  # 2-19 required
    im, d = new()
    title(d, "棒（長さ L・質量 2m）両端に質点 m")
    cy = 250
    x1, x2 = 150, 510
    d.line((x1, cy, x2, cy), fill=BLACK, width=8)
    ctext(d, 330, cy - 22, "棒 質量 2m", FS)
    node(d, x1, cy, 16, FILL2, BLACK); ctext(d, x1, cy + 30, "m", FS)
    node(d, x2, cy, 16, FILL2, BLACK); ctext(d, x2, cy + 30, "m", FS)
    # 中心を通り棒に直交する回転軸
    dash(d, 330, 130, 330, 370, RED)
    ctext(d, 330, 118, "回転軸（中心・直交）", FT, RED)
    dim(d, x1, cy + 70, x2, cy + 70, "L", col=GRAY)
    save(im, name)


def bar_end_axis(name):  # 2-20 required
    im, d = new()
    title(d, "棒（長さ l・質量 m）の重心軸と端軸")
    cy = 250
    x1, x2 = 200, 520
    d.line((x1, cy, x2, cy), fill=BLACK, width=8)
    ctext(d, 360, cy - 22, "質量 m", FS)
    G = (x1 + x2) / 2
    # 重心軸 z'
    dash(d, G, 140, G, 360, RED)
    node(d, G, cy, 6, BLACK, BLACK)
    ctext(d, G, 128, "z'（重心 G）", FT, RED)
    # 端軸 z（端 O）
    dash(d, x1, 140, x1, 360, BLUE)
    node(d, x1, cy, 6, BLACK, BLACK)
    ctext(d, x1, 128, "z（端 O）", FT, BLUE)
    dim(d, x1, cy + 70, G, cy + 70, "l/2", col=GRAY)
    save(im, name)


def parallel_axis(name):  # 2-21 required
    im, d = new()
    title(d, "平行な2軸（重心軸 z' と z 軸）")
    G = (280, 250)
    R = 95
    d.ellipse((G[0] - R, G[1] - R, G[0] + R, G[1] + R), outline=BLACK, width=3, fill=FILL1)
    node(d, G[0], G[1], 6, BLACK, BLACK); ctext(d, G[0] - 14, G[1] + 6, "G", FS, BLACK, "rm")
    # z'軸（重心）
    dash(d, G[0], 120, G[0], 380, RED)
    ctext(d, G[0], 108, "z'（質量 M）", FT, RED)
    # z軸（平行）
    zx = 470
    dash(d, zx, 120, zx, 380, BLUE)
    ctext(d, zx, 108, "z", FT, BLUE)
    dim(d, G[0], 355, zx, 355, "h", col=GRAY)
    save(im, name)


def planar_motion_dof(name):  # 2-22 required
    im, d = new()
    title(d, "xy 平面内の剛体の運動")
    ox, oy = 130, 350
    arrow(d, ox, oy, ox + 120, oy, BLACK, 2, 10); ctext(d, ox + 126, oy, "x", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - 120, BLACK, 2, 10); ctext(d, ox - 12, oy - 126, "y", FT, BLACK, "rm")
    # 剛体（不定形）
    poly = [(360, 190), (470, 210), (490, 300), (400, 340), (330, 280)]
    d.polygon(poly, outline=BLACK, width=3, fill=FILL1)
    G = (410, 262)
    node(d, G[0], G[1], 6, BLACK, BLACK); ctext(d, G[0] + 8, G[1] + 12, "G", FT)
    # 3自由度
    arrow(d, G[0], G[1], G[0] + 90, G[1], RED, 4, 14); ctext(d, G[0] + 96, G[1], "x 並進", FT, RED, "lm")
    arrow(d, G[0], G[1], G[0], G[1] - 90, RED, 4, 14); ctext(d, G[0], G[1] - 104, "y 並進", FT, RED)
    curve_arrow(d, G[0], G[1], 46, 200, 340, ORANGE, 3, 12); ctext(d, G[0] - 60, G[1] + 6, "回転 θ", FT, ORANGE, "rm")
    note(d, "x 並進・y 並進・z 軸まわり回転の3つ")
    save(im, name)


def _incline_geom():
    """斜面の頂点と斜面(斜辺)方向。角θの頂点=A(左下)。"""
    A = (110, 360)          # 左下（角θの頂点）
    B = (560, 360)          # 右下（直角）
    thdeg = 24
    th = math.radians(thdeg)
    T = (560, 360 - (560 - 110) * math.tan(th))   # 右上
    # 斜辺A→Tの下り方向(T→A)単位
    ux, uy = (A[0] - T[0]), (A[1] - T[1])
    L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    nx, ny = -uy, ux                               # 上向き外法線(上左)
    if ny > 0:
        nx, ny = -nx, -ny
    return A, B, T, th, thdeg, (ux, uy), (nx, ny)


def _rot_box(d, cx, cy, w, h, th, label=""):
    """斜面角thに傾けた直方体（斜辺は右上がり=数学角+th）。"""
    ca, sa = math.cos(th), math.sin(th)
    pts = []
    for sx, sy in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        # 右上がりの斜面に合わせ時計回り(画像)へ傾ける
        pts.append((cx + sx * ca + sy * sa, cy - sx * sa + sy * ca))
    d.polygon(pts, outline=BLACK, width=3, fill=FILL2)
    if label:
        ctext(d, cx, cy, label, FT)


def incline_slide_roll(name):  # 2-23 required
    im, d = new()
    title(d, "斜面上：すべる直方体と転がる球")
    A, B, T, th, thdeg, (ux, uy), (nx, ny) = _incline_geom()
    d.polygon([A, B, T], outline=BLACK, width=3, fill=FILL1)
    angle_arc(d, A[0], A[1], 64, 0, thdeg, "", GRAY)
    ctext(d, A[0] + 92, A[1] - 14, "θ", FS, GRAY)
    # 直方体（すべり, a1）
    bcx, bcy = T[0] + ux * 150 + nx * 24, T[1] + uy * 150 + ny * 24
    _rot_box(d, bcx, bcy, 62, 40, th, "a1")
    ctext(d, bcx + 20, bcy - 40, "直方体（すべり）a1", FT, BLACK, "lm")
    # 球（転がり, a2）
    scx, scy = T[0] + ux * 320 + nx * 26, T[1] + uy * 320 + ny * 26
    d.ellipse((scx - 26, scy - 26, scx + 26, scy + 26), outline=BLACK, width=3, fill=FILL2)
    ctext(d, scx, scy, "球", FT)
    ctext(d, scx - 20, scy + 44, "転がり a2", FT, BLACK, "mm")
    save(im, name)


# ============================================================
# 公式図 v2f2（7枚）— 結論・式を描いてよい
# ============================================================

def f_inertial_force(name):
    im, d = new()
    title(d, "回転座標系の慣性力（遠心力・コリオリ力）")
    ox, oy = 330, 250
    R = 150
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    node(d, ox, oy, 6, BLACK, BLACK); ctext(d, ox - 14, oy + 8, "O", FS, BLACK, "rm")
    curve_arrow(d, ox, oy, 60, 30, 100, ORANGE, 3, 12); ctext(d, ox + 46, oy - 62, "ω", FS, ORANGE)
    ang = math.radians(45)
    px, py = ox + R * math.cos(ang), oy - R * math.sin(ang)
    d.line((ox, oy, px, py), fill=GRAY, width=2)
    node(d, px, py, 12, FILL2, BLACK); ctext(d, px + 12, py - 14, "m", FS, BLACK, "lm")
    # 遠心力（外向き=r方向）
    ex, ey = math.cos(ang), -math.sin(ang)
    arrow(d, px, py, px + 80 * ex, py + 80 * ey, RED, 4, 14)
    ctext(d, px + 80 * ex + 4, py + 80 * ey + 8, "遠心力", FT, RED, "lm")
    # 進行方向 v（接線）とそれに垂直なコリオリ力
    tx, ty = -math.sin(ang), -math.cos(ang)
    arrow(d, px, py, px + 70 * tx, py + 70 * ty, BLUE, 3, 12); ctext(d, px + 70 * tx - 10, py + 70 * ty - 14, "v", FS, BLUE, "rm")
    cxv, cyv = -ty, tx
    arrow(d, px, py, px + 66 * cxv, py + 66 * cyv, GREEN, 4, 13)
    ctext(d, px + 66 * cxv - 6, py + 66 * cyv + 12, "コリオリ力（v に垂直）", FT, GREEN, "mm")
    save(im, name)


def f_friction(name):
    im, d = new()
    title(d, "摩擦力 F = μN と力の釣り合い")
    hwall(d, 100, 560, 320, side=1, n=15)
    block(d, 320, 285, 130, 66, "m")
    arrow(d, 320, 285, 320, 165, BLUE, 4, 15); ctext(d, 320, 150, "垂直抗力 N", FS, BLUE)
    arrow(d, 320, 285, 320, 400, GREEN, 4, 15); ctext(d, 320, 402, "重力 mg", FS, GREEN, "mm")
    arrow(d, 385, 285, 500, 285, RED, 4, 15); ctext(d, 505, 285, "引く力", FS, RED, "lm")
    arrow(d, 255, 285, 150, 285, ORANGE, 4, 15); ctext(d, 145, 285, "摩擦力 F = μN", FS, ORANGE, "rm")
    save(im, name)


def f_central_force(name):
    im, d = new()
    title(d, "中心力・角運動量（腕 r・運動量 p）")
    ox, oy = 330, 255
    R = 140
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    node(d, ox, oy, 6, BLACK, BLACK); ctext(d, ox - 14, oy + 8, "O", FS, BLACK, "rm")
    ang = math.radians(48)
    px, py = ox + R * math.cos(ang), oy - R * math.sin(ang)
    arrow(d, ox, oy, px, py, GRAY, 2, 11); ctext(d, (ox + px) / 2 + 8, (oy + py) / 2 - 12, "腕 r", FS, GRAY)
    node(d, px, py, 12, FILL2, BLACK); ctext(d, px + 12, py - 14, "m", FS, BLACK, "lm")
    ex, ey = math.cos(ang), -math.sin(ang)
    arrow(d, px, py, px - 80 * ex, py - 80 * ey, RED, 4, 14); ctext(d, px - 40 * ex + 10, py - 40 * ey + 10, "中心力", FT, RED, "lm")
    tx, ty = -math.sin(ang), -math.cos(ang)
    arrow(d, px, py, px + 82 * tx, py + 82 * ty, BLUE, 4, 13); ctext(d, px + 82 * tx - 10, py + 82 * ty - 14, "運動量 p", FS, BLUE, "rm")
    ctext(d, 330, 400, "L = r × m v（中心力ではモーメント0 → L 一定）", FT, GRAY)
    save(im, name)


def f_circular(name):
    im, d = new()
    title(d, "円運動：v=lω・p=mlω・L=ml²ω")
    ox, oy = 300, 250
    R = 150
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    node(d, ox, oy, 6, BLACK, BLACK); ctext(d, ox - 14, oy + 8, "O", FS, BLACK, "rm")
    ang = math.radians(50)
    px, py = ox + R * math.cos(ang), oy - R * math.sin(ang)
    d.line((ox, oy, px, py), fill=GRAY, width=2); ctext(d, (ox + px) / 2 - 12, (oy + py) / 2, "l", FS, GRAY)
    node(d, px, py, 12, FILL2, BLACK); ctext(d, px + 12, py - 14, "m", FS, BLACK, "lm")
    tx, ty = -math.sin(ang), -math.cos(ang)
    arrow(d, px, py, px + 90 * tx, py + 90 * ty, BLUE, 4, 13); ctext(d, px + 90 * tx - 8, py + 90 * ty - 14, "v = lω", FS, BLUE, "rm")
    curve_arrow(d, ox, oy, 54, 28, 92, ORANGE, 3, 11); ctext(d, ox + 76, oy - 16, "ω", FS, ORANGE)
    ctext(d, 500, 360, "p = mlω\nL = ml²ω", FS, GRAY)
    save(im, name)


def f_moment_inertia(name):
    im, d = new()
    title(d, "慣性モーメント I = ∫ r² dm")
    # 回転軸
    ax = 200
    dash(d, ax, 110, ax, 370, RED); ctext(d, ax, 96, "回転軸", FT, RED)
    # 微小質量 dm と距離 r
    dm = (400, 200)
    d.rectangle((dm[0] - 12, dm[1] - 12, dm[0] + 12, dm[1] + 12), outline=BLACK, width=2, fill=FILL2)
    ctext(d, dm[0] + 22, dm[1] - 12, "dm", FT, BLACK, "lm")
    dim(d, ax, dm[1], dm[0], dm[1], "r", col=GRAY)
    ctext(d, 400, 245, "I = ∫ r² dm", FS, BLACK)
    # 棒（中心軸）の代表例
    d.line((300, 330, 500, 330), fill=BLACK, width=7)
    dash(d, 400, 300, 400, 400, RED)
    ctext(d, 400, 360, "棒（中心）: I = (1/12) m L²", FT, GRAY)
    save(im, name)


def f_parallel_axis(name):
    im, d = new()
    title(d, "平行軸の定理  I = I_G + M h²")
    G = (270, 245)
    R = 90
    d.ellipse((G[0] - R, G[1] - R, G[0] + R, G[1] + R), outline=BLACK, width=3, fill=FILL1)
    node(d, G[0], G[1], 6, BLACK, BLACK); ctext(d, G[0] - 14, G[1] + 6, "G", FS, BLACK, "rm")
    dash(d, G[0], 120, G[0], 380, RED); ctext(d, G[0], 108, "z'（重心・I_G）", FT, RED)
    zx = 470
    dash(d, zx, 120, zx, 380, BLUE); ctext(d, zx, 108, "z（I）", FT, BLUE)
    dim(d, G[0], 350, zx, 350, "h", col=GRAY)
    ctext(d, 330, 398, "軸が h 離れると I は M h² だけ増える", FT, GRAY)
    save(im, name)


def f_slope_roll(name):
    im, d = new()
    title(d, "斜面：すべり a1 と転がり a2（a1 > a2）")
    A, B, T, th, thdeg, (ux, uy), (nx, ny) = _incline_geom()
    d.polygon([A, B, T], outline=BLACK, width=3, fill=FILL1)
    angle_arc(d, A[0], A[1], 64, 0, thdeg, "", GRAY); ctext(d, A[0] + 92, A[1] - 14, "θ", FS, GRAY)
    # 直方体
    bcx, bcy = T[0] + ux * 150 + nx * 23, T[1] + uy * 150 + ny * 23
    _rot_box(d, bcx, bcy, 58, 36, th, "")
    ctext(d, bcx + 18, bcy - 34, "直方体", FT, BLACK, "lm")
    ctext(d, bcx + 18, bcy + 30, "a1 = g sinθ", FT, RED, "lm")
    # 球
    scx, scy = T[0] + ux * 320 + nx * 24, T[1] + uy * 320 + ny * 24
    d.ellipse((scx - 24, scy - 24, scx + 24, scy + 24), outline=BLACK, width=3, fill=FILL2)
    curve_arrow(d, scx, scy, 24, 200, 320, ORANGE, 2, 9)
    ctext(d, scx - 14, scy - 38, "球（転がり）", FT, BLACK, "mm")
    ctext(d, scx - 14, scy + 40, "a2 = gsinθ/(1+I/mR²)", FT, BLUE, "mm")
    save(im, name)


if __name__ == "__main__":
    # ---- 問題図 v2e2（23枚）----
    newton_three_laws("v2e2NewtonThreeLaws")
    momentum_force_law("v2e2MomentumForceLaw")
    proportion_accel("v2e2ProportionAccel")
    translation_1d("v2e2Translation1D")
    spring_mass_force("v2e2SpringMassForce")
    inertial_frames("v2e2InertialFrames")
    non_inertial("v2e2NonInertial")
    projectile_init("v2e2ProjectileInit")
    momentum_conserv("v2e2MomentumConserv")
    momentum_vs_energy("v2e2MomentumVsEnergy")
    stacked_blocks("v2e2StackedBlocks")
    conservation_conditions("v2e2ConservationConditions")
    friction_fbd("v2e2Friction")
    central_force("v2e2CentralForce")
    time_derivatives("v2e2TimeDerivatives")
    circular_motion("v2e2CircularMotion")
    radius_halved("v2e2RadiusHalved")
    centroid_inertia("v2e2CentroidInertia")
    bar_two_masses("v2e2BarTwoMasses")
    bar_end_axis("v2e2BarEndAxis")
    parallel_axis("v2e2ParallelAxis")
    planar_motion_dof("v2e2PlanarMotionDOF")
    incline_slide_roll("v2e2InclineSlideRoll")
    # ---- 公式図 v2f2（7枚）----
    f_inertial_force("v2f2InertialForce")
    f_friction("v2f2Friction")
    f_central_force("v2f2CentralForce")
    f_circular("v2f2Circular")
    f_moment_inertia("v2f2MomentInertia")
    f_parallel_axis("v2f2ParallelAxis")
    f_slope_roll("v2f2SlopeRoll")
    print("done")
