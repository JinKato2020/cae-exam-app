# -*- coding: utf-8 -*-
"""振動2級 第3章 材料力学の基礎 の問題図（全17枚）。
問題図=接頭辞 v2e3。白地660×420・黒線画（figlib準拠）。
required問題図は答え・正解値・結論を描かない（与件のみ）。
文字化け回避のためギリシャ文字は綴り（sigma, tau, gamma, epsilon, nu）で書く。
実行: python tools/figs_vib2ch3_e.py
"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
import math
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
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


# ============================================================
# 問題図 v2e3（17枚）
# ============================================================

def axial_strain_def(name):  # 1 required
    im, d = new()
    title(d, "丸棒の引張による伸び（元長 L0・直径 D0）")
    # 上：元の棒
    y0 = 150
    x1, x2 = 130, 430
    d.rectangle((x1, y0 - 22, x2, y0 + 22), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x1 + x2) / 2, y0 - 40, "元の棒", FT, GRAY)
    dim(d, x1, y0 + 48, x2, y0 + 48, "L0", col=GRAY)
    dim(d, x2 + 26, y0 - 22, x2 + 26, y0 + 22, "D0", col=GRAY)
    # 下：引張後の棒（長い）
    y1 = 300
    x3, x4 = 130, 520
    d.rectangle((x3, y1 - 20, x4, y1 + 20), outline=BLACK, width=3, fill=FILL2)
    ctext(d, (x3 + x4) / 2, y1 - 38, "引張後の棒", FT, GRAY)
    dim(d, x3, y1 + 46, x2, y1 + 46, "L0", col=GRAY)
    dim(d, x2, y1 + 46, x4, y1 + 46, "dL", col=RED)
    dash(d, x2, y1 - 30, x2, y1 + 40, LGRAY)
    ctext(d, (x2 + x4) / 2, y1 + 72, "伸び dL = L1 - L0", FT, RED)
    save(im, name)


def poisson_contraction(name):  # 2 required
    im, d = new()
    title(d, "引張荷重 P による軸伸び・径縮み")
    cy = 240
    # 元の棒（破線・太め）
    x1, x2 = 190, 430
    hh0 = 40
    dash(d, x1, cy - hh0, x2, cy - hh0, GRAY)
    dash(d, x1, cy + hh0, x2, cy + hh0, GRAY)
    dash(d, x1, cy - hh0, x1, cy + hh0, GRAY)
    dash(d, x2, cy - hh0, x2, cy + hh0, GRAY)
    ctext(d, (x1 + x2) / 2, cy + hh0 + 20, "元（D0・L0）：破線", FT, GRAY)
    # 変形後（実線・細く長い）
    x3, x4 = 170, 470
    hh1 = 26
    d.rectangle((x3, cy - hh1, x4, cy + hh1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x3 + x4) / 2, cy, "変形後（D1・L1）", FT, BLACK)
    dim(d, x4 + 24, cy - hh1, x4 + 24, cy + hh1, "D1", col=BLACK)
    dim(d, x1 - 24, cy - hh0, x1 - 24, cy + hh0, "D0", col=GRAY)
    # 引張荷重 P
    force(d, x4, cy, 90, 0, "P", RED)
    force(d, x3, cy, -90, 0, "P", RED)
    save(im, name)


def shear_strain_angles(name):  # 3 required
    im, d = new()
    title(d, "せん断による正方形→平行四辺形の変形")
    # 元の正方形（破線）
    ox, oy, s = 240, 300, 150
    dash(d, ox, oy, ox + s, oy, GRAY)
    dash(d, ox, oy, ox, oy - s, GRAY)
    dash(d, ox + s, oy, ox + s, oy - s, GRAY)
    dash(d, ox, oy - s, ox + s, oy - s, GRAY)
    ctext(d, ox + s / 2, oy + 22, "元の正方形（破線）", FT, GRAY)
    # 変形後の平行四辺形（実線）：上辺が右へ、右辺が上で右へ傾く
    sh = 46
    P = [(ox, oy), (ox + s, oy),
         (ox + s + sh, oy - s), (ox + sh, oy - s)]
    d.line([P[0], P[1], P[2], P[3], P[0]], fill=BLACK, width=3)
    # 辺の回転角2つ
    # 縦辺（左辺）の傾き： du/dy 方向
    angle_arc(d, ox, oy - s, 40, 60, 90, "", RED)
    ctext(d, ox + 26, oy - s - 30, "du/dy", FT, RED, "lm")
    arrow(d, ox, oy - s, ox + sh, oy - s, RED, 2, 10)
    # 底辺は固定・上辺がずれる様子として横矢印
    # 右辺の回転（dv/dx 方向）を下辺右端で示す
    angle_arc(d, ox + s, oy, 42, 90, 118, "", BLUE)
    dash(d, ox + s, oy, ox + s, oy - 60, LGRAY)
    ctext(d, ox + s + 20, oy - 60, "dv/dx", FT, BLUE, "lm")
    arrow(d, ox + s, oy, ox + s + sh * 0.4, oy - 60, BLUE, 2, 10)
    save(im, name)


def disp_to_strain(name):  # 4 required
    im, d = new()
    title(d, "x 断面と x+dx 断面の変位（u と u+du）")
    # 変形前の棒
    y0 = 170
    x1, x2 = 120, 560
    d.rectangle((x1, y0 - 20, x2, y0 + 20), outline=BLACK, width=3, fill=FILL1)
    xa, xb = 280, 360
    for xx in (xa, xb):
        d.line((xx, y0 - 20, xx, y0 + 20), fill=BLACK, width=2)
    ctext(d, xa, y0 - 36, "x 断面", FT, GRAY)
    ctext(d, xb, y0 - 36, "x+dx 断面", FT, GRAY)
    dim(d, xa, y0 + 46, xb, y0 + 46, "dx", col=GRAY)
    ctext(d, x1 + 20, y0, "変形前", FT, GRAY, "lm")
    # 座標基準
    dash(d, x1, y0 - 40, x1, 330, LGRAY)
    # 変形後の棒（右へずれ、少し伸びる）
    y1 = 300
    off = 46
    d.rectangle((x1 + off, y1 - 18, x2 + off + 24, y1 + 18), outline=BLACK, width=3, fill=FILL2)
    xa2, xb2 = xa + off, xb + off + 12
    for xx in (xa2, xb2):
        d.line((xx, y1 - 18, xx, y1 + 18), fill=BLACK, width=2)
    ctext(d, x1 + 40, y1, "変形後", FT, GRAY, "lm")
    dim(d, xa, y1 - 40, xa2, y1 - 40, "u", col=RED)
    dim(d, xb, y1 + 44, xb2, y1 + 44, "u+du", col=BLUE)
    dash(d, xa, y1 - 50, xa, y1 + 30, LGRAY)
    dash(d, xb, y1 - 30, xb, y1 + 50, LGRAY)
    save(im, name)


def stress_strain_terms(name):  # 5 required
    im, d = new()
    title(d, "応力の定義と、弾性域・塑性域の概念")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    # 左：応力＝単位面積あたりの内力
    ctext(d, 165, 96, "応力 = 内力 / 断面積", FT, BLACK)
    d.rectangle((110, 150, 250, 300), outline=BLACK, width=3, fill=FILL1)
    dash(d, 110, 225, 250, 225, GRAY)   # 切断面
    ctext(d, 180, 210, "断面 A", FT, GRAY)
    for xx in (140, 180, 220):
        arrow(d, xx, 225, xx, 175, RED, 3, 10)
    ctext(d, 180, 130, "内力（面に分布）", FT, RED)
    force(d, 180, 300, 0, 70, "P", RED)
    # 右：弾性域（除荷で戻る）・塑性域（残留ひずみ）概念
    ox, oy = 400, 360
    arrow(d, ox, oy, ox + 200, oy, BLACK, 2, 10); ctext(d, ox + 150, oy + 18, "epsilon", FT, BLACK, "mm")
    arrow(d, ox, oy, ox, oy - 210, BLACK, 2, 10); ctext(d, ox - 8, oy - 216, "sigma", FT, BLACK, "rm")
    # 弾性域（直線・原点へ戻る）
    d.line((ox, oy, ox + 90, oy - 120), fill=BLUE, width=3)
    ctext(d, ox + 30, oy - 96, "弾性域", FT, BLUE, "lm")
    # 塑性域（曲がる）＋除荷線（原点に戻らず残留）
    d.line([(ox + 90, oy - 120), (ox + 140, oy - 150), (ox + 190, oy - 162)], fill=RED, width=3)
    ctext(d, ox + 150, oy - 140, "塑性域", FT, RED, "lm")
    dash(d, ox + 170, oy - 158, ox + 90, oy, RED)  # 除荷（弾性勾配で戻る）
    ctext(d, ox + 96, oy + 16, "残留ひずみ", FT, RED, "mm")
    save(im, name)


def plane_stress_element(name):  # 6 required
    im, d = new()
    title(d, "平面応力の微小要素（面内 sigma_x・sigma_y）")
    ox, oy, s = 270, 275, 118
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3, fill=FILL1)
    cx, cy = ox + s / 2, oy - s / 2
    # sigma_x（左右）
    arrow(d, ox + s, cy, ox + s + 80, cy, RED, 4, 14); ctext(d, ox + s + 86, cy, "sigma_x", FS, RED, "lm")
    arrow(d, ox, cy, ox - 80, cy, RED, 4, 14); ctext(d, ox - 86, cy, "sigma_x", FS, RED, "rm")
    # sigma_y（上下）
    arrow(d, cx, oy - s, cx, oy - s - 58, BLUE, 4, 14); ctext(d, cx, oy - s - 72, "sigma_y", FS, BLUE)
    arrow(d, cx, oy, cx, oy + 58, BLUE, 4, 14); ctext(d, cx, oy + 72, "sigma_y", FS, BLUE)
    note(d, "面外方向は sigma_z = 0（平面応力）")
    save(im, name)


def elastic_constants(name):  # 7 required
    im, d = new()
    title(d, "弾性定数 E・nu・G の関係（独立なのは2つ）")
    E = (330, 150)
    G = (190, 320)
    NU = (470, 320)
    # 連結線（先に描き、頂点の円で隠す）
    for a, b in [(E, G), (G, NU), (NU, E)]:
        d.line((a[0], a[1], b[0], b[1]), fill=GRAY, width=2)
    for p, sym, desc, dy in [(E, "E", "縦弾性係数", -50),
                             (G, "G", "横弾性係数", 48),
                             (NU, "nu", "ポアソン比", 48)]:
        d.ellipse((p[0] - 34, p[1] - 34, p[0] + 34, p[1] + 34), outline=BLACK, width=3, fill=FILL1)
        ctext(d, p[0], p[1], sym, F)
        ctext(d, p[0], p[1] + dy, desc, FT, GRAY)
    note(d, "3つのうち独立なのは2つ・残り1つは他の2つから決まる（従属）")
    save(im, name)


def mild_steel_ss_curve(name):  # 8 helpful
    im, d = new()
    title(d, "軟鋼の応力-ひずみ線図")
    ox, oy = 110, 360
    arrow(d, ox, oy, ox + 470, oy, BLACK, 2, 11); ctext(d, ox + 400, oy + 20, "ひずみ epsilon", FT, BLACK, "mm")
    arrow(d, ox, oy, ox, oy - 280, BLACK, 2, 11); ctext(d, ox - 8, oy - 286, "応力 sigma", FT, BLACK, "rm")
    # 弾性直線 → 比例限度
    pl = (ox + 90, oy - 150)
    d.line((ox, oy, pl[0], pl[1]), fill=BLUE, width=3)
    # 上降伏点・下降伏点（ギザ）
    uy = (ox + 110, oy - 175)
    ly = (ox + 130, oy - 150)
    d.line((pl[0], pl[1], uy[0], uy[1]), fill=RED, width=3)
    d.line((uy[0], uy[1], ly[0], ly[1]), fill=RED, width=3)
    # 降伏平坦部 → 加工硬化 → 引張強さ（最大）
    ts = (ox + 320, oy - 235)
    d.line([(ly[0], ly[1]), (ox + 180, oy - 152), (ox + 250, oy - 210), ts], fill=RED, width=3)
    # 破断点（下がって終わる）
    br = (ox + 400, oy - 175)
    d.line((ts[0], ts[1], br[0], br[1]), fill=RED, width=3)
    d.line((br[0], br[1], br[0] + 6, br[1] + 4), fill=RED, width=3)
    ctext(d, br[0] + 4, br[1] - 4, "×", FS, RED)
    # ラベル
    ctext(d, pl[0] - 46, pl[1] + 34, "比例限度", FT, BLUE, "mm")
    ctext(d, uy[0], uy[1] - 16, "上降伏点", FT, RED, "mm")
    ctext(d, ly[0] + 40, ly[1] + 22, "下降伏点", FT, RED, "mm")
    ctext(d, ts[0], ts[1] - 18, "引張強さ（最大）", FT, RED)
    ctext(d, br[0] + 12, br[1], "破断点", FT, RED, "lm")
    # 弾性域/塑性域区分
    dash(d, pl[0], oy, pl[0], pl[1], LGRAY)
    ctext(d, ox + 45, oy - 20, "弾性域", FT, BLUE, "mm")
    ctext(d, ox + 240, oy - 20, "塑性域", FT, RED, "mm")
    save(im, name)


def square_shear(name):  # 9 required
    im, d = new()
    title(d, "正方形断面（一辺 10mm）にせん断力 Q")
    ox, oy, s = 250, 300, 150
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3, fill=FILL1)
    dim(d, ox, oy + 26, ox + s, oy + 26, "10 mm", col=GRAY)
    dim(d, ox - 26, oy - s, ox - 26, oy, "10 mm", col=GRAY)
    ctext(d, ox + s / 2, oy - s / 2, "断面", FT, GRAY)
    # 断面に平行なせん断力 Q（上辺に沿う矢印）
    arrow(d, ox + 20, oy - s - 18, ox + s - 20, oy - s - 18, RED, 4, 15)
    ctext(d, ox + s / 2, oy - s - 36, "せん断力 Q = 3.0 kN", FS, RED)
    save(im, name)


def shear_strain_calc(name):  # 10 required
    im, d = new()
    title(d, "せん断応力 tau とせん断角 gamma")
    ox, oy, s = 250, 320, 150
    # 元（破線正方形）
    dash(d, ox, oy, ox + s, oy, GRAY)
    dash(d, ox, oy, ox, oy - s, GRAY)
    dash(d, ox + s, oy, ox + s, oy - s, GRAY)
    dash(d, ox, oy - s, ox + s, oy - s, GRAY)
    # 変形後（平行四辺形・上辺が右へ）
    sh = 48
    P = [(ox, oy), (ox + s, oy), (ox + s + sh, oy - s), (ox + sh, oy - s)]
    d.line([P[0], P[1], P[2], P[3], P[0]], fill=BLACK, width=3)
    # tau 矢印（上辺右向き・下辺左向き）
    arrow(d, ox + sh + 12, oy - s - 16, ox + s + sh - 12, oy - s - 16, RED, 4, 13)
    ctext(d, ox + s / 2 + sh, oy - s - 34, "tau", FS, RED)
    arrow(d, ox + s - 12, oy + 16, ox + 12, oy + 16, RED, 4, 13)
    ctext(d, ox + s / 2, oy + 34, "tau", FS, RED)
    # せん断角 gamma（左辺の傾き）
    angle_arc(d, ox, oy - s, 44, 62, 90, "", BLUE)
    ctext(d, ox + 30, oy - s - 26, "gamma", FS, BLUE, "lm")
    save(im, name)


def stepped_bar_axial(name):  # 11 required
    im, d = new()
    title(d, "左端固定の棒（全長 2L）に軸力 P1・P2")
    cy = 240
    x0, xm, xr = 150, 350, 540
    wall(d, x0, cy - 40, cy + 40, side=1, n=6)
    d.rectangle((x0, cy - 24, xr, cy + 24), outline=BLACK, width=3, fill=FILL1)
    d.line((xm, cy - 24, xm, cy + 24), fill=BLACK, width=2)
    node(d, xm, cy, 5, BLACK, BLACK)
    # 軸力 P1（中央）・P2（右端）
    force(d, xm, cy, 70, 0, "P1", RED)
    force(d, xr, cy, 60, 0, "P2", BLUE)
    # 区間長・断面積・ヤング率
    dim(d, x0, cy + 56, xm, cy + 56, "L", col=GRAY)
    dim(d, xm, cy + 56, xr, cy + 56, "L", col=GRAY)
    ctext(d, (x0 + xr) / 2, cy - 52, "断面積 A・ヤング率 E（一様）", FT, GRAY)
    save(im, name)


def hollow_circle_i(name):  # 12 required
    im, d = new()
    title(d, "中空円断面（外径 D=40mm・内径 d=20mm）")
    ox, oy = 320, 240
    RD, rd = 130, 65
    d.ellipse((ox - RD, oy - RD, ox + RD, oy + RD), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((ox - rd, oy - rd, ox + rd, oy + rd), outline=BLACK, width=3, fill="white")
    node(d, ox, oy, 5, BLACK, BLACK)
    # 中立軸（図心を通る水平軸）
    d.line((ox - RD - 40, oy, ox + RD + 40, oy), fill=RED, width=2)
    ctext(d, ox + RD + 46, oy, "中立軸", FT, RED, "lm")
    # 寸法
    dim(d, ox - RD, oy + RD + 24, ox + RD, oy + RD + 24, "D = 40 mm", col=GRAY)
    dim(d, ox - rd, oy, ox + rd, oy, "d = 20 mm", col=BLUE)
    save(im, name)


def beam_deflection(name):  # 13 required
    im, d = new()
    title(d, "はりのたわみ曲線 y(x)（曲げ剛性 EI）")
    ox, oy = 130, 210
    # 元のはり基準線（x軸）
    arrow(d, ox, oy, ox + 440, oy, BLACK, 2, 11); ctext(d, ox + 446, oy, "x", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy + 150, BLACK, 2, 11); ctext(d, ox - 10, oy + 156, "y（たわみ）", FT, BLACK, "rm")
    dash(d, ox, oy, ox + 420, oy, LGRAY)
    # たわみ曲線（下に垂れる）
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 420 * t
        y = oy + 120 * (t * t * (3 - 2 * t)) * (1 - 0.15 * t)
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3)
    ctext(d, ox + 150, oy + 40, "たわみ曲線 y(x)", FT, BLUE, "mm")
    # 曲げモーメント M と曲げ剛性 EI
    curve_arrow(d, ox + 300, oy + 90, 34, 200, 340, ORANGE, 3, 11)
    ctext(d, ox + 300, oy + 138, "曲げモーメント M", FT, ORANGE, "mm")
    ctext(d, ox + 210, oy - 22, "曲げ剛性 EI", FT, GRAY, "mm")
    save(im, name)


def simple_beam_reactions(name):  # 14 required
    im, d = new()
    title(d, "単純支持はり（全長 L=4m）と集中荷重 P")
    cy = 250
    xA, xB = 140, 540
    d.line((xA, cy, xB, cy), fill=BLACK, width=7)
    pin_support(d, xA, cy)
    roller_support(d, xB, cy)
    ctext(d, xA, cy + 66, "A（ピン）", FT, GRAY)
    ctext(d, xB, cy + 66, "B（ローラ）", FT, GRAY)
    # 荷重 P（Aから1m）：L=4m → 1m は 1/4
    xP = xA + (xB - xA) * 0.25
    arrow(d, xP, cy - 90, xP, cy - 6, RED, 4, 15); ctext(d, xP, cy - 106, "P = 600 N", FS, RED)
    # 反力 RA・RB（上向き・値は描かない）
    arrow(d, xA, cy + 54, xA, cy + 6, BLUE, 4, 14); ctext(d, xA - 30, cy + 34, "RA", FT, BLUE, "rm")
    arrow(d, xB, cy + 54, xB, cy + 6, BLUE, 4, 14); ctext(d, xB + 30, cy + 34, "RB", FT, BLUE, "lm")
    # 寸法
    dim(d, xA, cy - 130, xP, cy - 130, "1 m", col=GRAY)
    dim(d, xA, cy + 96, xB, cy + 96, "L = 4 m", col=GRAY)
    save(im, name)


def cantilever_setup(name):  # 15 required
    im, d = new()
    title(d, "片持ちはり：固定端から距離 a に荷重 P")
    cy = 240
    x0, xL = 150, 560
    wall(d, x0, cy - 40, cy + 40, side=1, n=6)
    d.line((x0, cy, xL, cy), fill=BLACK, width=7)
    # x 座標軸
    arrow(d, x0, cy - 70, x0 + 120, cy - 70, BLACK, 2, 10); ctext(d, x0 + 126, cy - 70, "x", FT, BLACK, "lm")
    # 荷重 P（距離 a）
    xP = x0 + (xL - x0) * 0.5
    arrow(d, xP, cy - 92, xP, cy - 6, RED, 4, 15); ctext(d, xP, cy - 108, "P", FS, RED)
    # 寸法 a・L
    dim(d, x0, cy + 40, xP, cy + 40, "a", col=GRAY)
    dim(d, x0, cy + 78, xL, cy + 78, "L", col=GRAY)
    save(im, name)


def free_end_bc(name):  # 16 required
    im, d = new()
    title(d, "はりの自由端の境界条件（拡大）")
    cy = 240
    x0, xe = 140, 400
    d.line((x0, cy, xe, cy), fill=BLACK, width=8)
    ctext(d, x0 + 10, cy - 24, "はり", FT, GRAY, "lm")
    # 自由端
    node(d, xe, cy, 6, "white", BLACK)
    ctext(d, xe, cy + 30, "自由端", FT, BLACK)
    # y 座標軸
    arrow(d, x0 - 20, cy - 90, x0 - 20, cy + 60, BLACK, 2, 10); ctext(d, x0 - 32, cy - 96, "y", FT, BLACK, "rm")
    # 外力なし → M=0, Q=0
    ctext(d, xe + 20, cy - 44, "外力なし", FT, GRAY, "lm")
    ctext(d, xe + 20, cy - 12, "曲げモーメント M = 0", FT, RED, "lm")
    ctext(d, xe + 20, cy + 14, "せん断力 Q = 0", FT, BLUE, "lm")
    save(im, name)


def simple_support_bc(name):  # 17 required
    im, d = new()
    title(d, "単純支持端の境界条件（拡大）")
    cy = 240
    x0, xe = 200, 520
    d.line((x0, cy, xe, cy), fill=BLACK, width=8)
    # 支点（ピン/ローラ）
    pin_support(d, x0, cy)
    ctext(d, x0, cy + 66, "支点（ピン/ローラ）", FT, GRAY)
    # たわみ y=0
    dash(d, x0, cy - 90, x0, cy + 40, LGRAY)
    ctext(d, x0 - 14, cy - 96, "たわみ y = 0", FT, RED, "rm")
    # 回転自由（モーメント=0）：回転を表す弧矢印
    curve_arrow(d, x0, cy, 50, 20, 150, ORANGE, 3, 11)
    ctext(d, x0 + 90, cy - 40, "回転は自由", FT, ORANGE, "lm")
    ctext(d, x0 + 90, cy - 16, "→ モーメント = 0", FT, BLUE, "lm")
    save(im, name)


if __name__ == "__main__":
    axial_strain_def("v2e3AxialStrainDef")
    poisson_contraction("v2e3PoissonContraction")
    shear_strain_angles("v2e3ShearStrainAngles")
    disp_to_strain("v2e3DispToStrain")
    stress_strain_terms("v2e3StressStrainTerms")
    plane_stress_element("v2e3PlaneStressElement")
    elastic_constants("v2e3ElasticConstants")
    mild_steel_ss_curve("v2e3MildSteelSSCurve")
    square_shear("v2e3SquareShear")
    shear_strain_calc("v2e3ShearStrainCalc")
    stepped_bar_axial("v2e3SteppedBarAxial")
    hollow_circle_i("v2e3HollowCircleI")
    beam_deflection("v2e3BeamDeflection")
    simple_beam_reactions("v2e3SimpleBeamReactions")
    cantilever_setup("v2e3CantileverSetup")
    free_end_bc("v2e3FreeEndBC")
    simple_support_bc("v2e3SimpleSupportBC")
    print("done")
