# -*- coding: utf-8 -*-
"""振動2級 第5章「有限要素法の基礎」の問題図（全19枚）。接頭辞 v2e5。
白地660×420・黒線画（figlib準拠）。
required問題図は答え・正解値・結論・正解の選択肢を描かない（与件・配置・記号のみ）。
文字化け回避のためギリシャ文字は綴り（mu, theta, xi, eta, Pi, sigma, epsilon）で書く。
実行: python tools/figs_vib2ch5_e.py
"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
import math
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot,
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


def fillcell(d, x, y, cell, col):
    d.rectangle((x + 2, y + 2, x + cell - 2, y + cell - 2), fill=col)


def grid_lines(d, x, y, rows, cols, cell):
    for i in range(rows + 1):
        d.line((x, y + i * cell, x + cols * cell, y + i * cell), fill=BLACK, width=2)
    for j in range(cols + 1):
        d.line((x + j * cell, y, x + j * cell, y + rows * cell), fill=BLACK, width=2)


# ============================================================
# 問題図 v2e5（19枚）
# ============================================================

def discretize_map(name):  # 5-1 required
    im, d = new()
    title(d, "連続体の離散化（無限自由度 → 有限自由度）")
    # 左：連続体
    d.ellipse((90, 120, 250, 260), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 170, 190, "連続体", FS)
    ctext(d, 170, 280, "無限自由度", FT, GRAY)
    arrow(d, 265, 190, 335, 190, BLACK, 3, 14)
    # 右：離散化(節点・要素)
    ox, oy = 360, 120
    for i in range(4):
        for j in range(4):
            node(d, ox + j * 45, oy + i * 45, 5, "white")
    for i in range(4):
        d.line((ox, oy + i * 45, ox + 3 * 45, oy + i * 45), fill=LGRAY, width=1)
        d.line((ox + i * 45, oy, ox + i * 45, oy + 3 * 45), fill=LGRAY, width=1)
    ctext(d, ox + 68, oy + 3 * 45 + 30, "節点・要素（有限自由度）", FT, GRAY)
    # 下：手法名の枠(空間離散化 と 時間積分)
    block(d, 200, 360, 300, 54, "", FILL1)
    ctext(d, 200, 344, "空間の離散化", FT, GRAY)
    ctext(d, 200, 368, "FEM / BEM / FDM", FS)
    block(d, 500, 360, 220, 54, "", FILL1)
    ctext(d, 500, 344, "時間の扱い", FT, GRAY)
    ctext(d, 500, 368, "時間積分法", FS)
    save(im, name)


def shape_func_interp(name):  # 5-2 required
    im, d = new()
    title(d, "形状関数による要素内変位の補間（2節点要素）")
    ox, oy = 130, 320
    # x軸(要素) と 変位u軸
    arrow(d, ox, oy, ox + 430, oy, BLACK, 2, 11); ctext(d, ox + 436, oy, "x", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - 210, BLACK, 2, 11); ctext(d, ox - 12, oy - 214, "変位 u", FT, BLACK, "rm")
    xL, xR = ox, ox + 380
    # 節点
    node(d, xL, oy, 6, BLACK); node(d, xR, oy, 6, BLACK)
    ctext(d, xL, oy + 22, "節点1", FT, GRAY); ctext(d, xR, oy + 22, "節点2", FT, GRAY)
    # 節点変位 u1,u2（高さ）
    u1, u2 = 70, 150
    dash(d, xL, oy, xL, oy - u1, LGRAY); dash(d, xR, oy, xR, oy - u2, LGRAY)
    node(d, xL, oy - u1, 5, RED); node(d, xR, oy - u2, 5, RED)
    ctext(d, xL - 12, oy - u1, "u1", FT, RED, "rm")
    ctext(d, xR + 12, oy - u2, "u2", FT, RED, "lm")
    # 補間曲線 u(x)
    pts = []
    for i in range(41):
        t = i / 40.0
        x = xL + (xR - xL) * t
        y = oy - (u1 + (u2 - u1) * (0.5 - 0.5 * math.cos(math.pi * t)))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE)
    ctext(d, (xL + xR) / 2, oy - 120, "u(x) = 形状関数で補間", FT, BLUE)
    note(d, "要素が変われば形状関数も変わる")
    save(im, name)


def beam_element_dof(name):  # 5-3 required
    im, d = new()
    title(d, "2節点はり要素の節点自由度")
    cy = 230
    x1, x2 = 180, 480
    d.line((x1, cy, x2, cy), fill=BLACK, width=6)
    node(d, x1, cy, 7, "white"); node(d, x2, cy, 7, "white")
    ctext(d, x1, cy + 78, "節点1", FT, GRAY); ctext(d, x2, cy + 78, "節点2", FT, GRAY)
    for xn in (x1, x2):
        # たわみ w（上下矢印）
        arrow(d, xn, cy - 20, xn, cy - 80, RED, 3, 12)
        ctext(d, xn, cy - 96, "w（たわみ）", FT, RED)
        # 回転角 theta（回転矢印）
        curve_arrow(d, xn, cy, 40, 200, 340, BLUE, 3, 11)
        ctext(d, xn, cy + 50, "theta（回転角）", FT, BLUE)
    note(d, "各節点に たわみ w と 回転角 theta")
    save(im, name)


def bar_long_wave(name):  # 5-4 required
    im, d = new()
    title(d, "一様な棒の縦振動と弾性波")
    cy = 210
    x0, x1 = 110, 560
    d.rectangle((x0, cy - 26, x1, cy + 26), outline=BLACK, width=3, fill=FILL1)
    # 軸方向座標 x
    arrow(d, x0, cy + 60, x1, cy + 60, BLACK, 2, 11); ctext(d, x1 + 8, cy + 60, "x（軸方向）", FT, BLACK, "lm")
    # 微小要素 dx
    a, b = 300, 360
    for xx in (a, b):
        d.line((xx, cy - 26, xx, cy + 26), fill=GRAY, width=2)
    dim(d, a, cy - 44, b, cy - 44, "dx", col=GRAY)
    # 軸方向変位
    arrow(d, 210, cy, 250, cy, RED, 3, 11); ctext(d, 200, cy - 20, "軸方向変位", FT, RED)
    # 縦波が速さ c で伝わる
    curve_arrow(d, 470, cy, 30, 150, 30, ORANGE, 3, 10)
    arrow(d, 430, cy + 90, 520, cy + 90, ORANGE, 3, 13)
    ctext(d, 475, cy + 108, "縦波が速さ c で伝わる", FT, ORANGE)
    save(im, name)


def potential_spring(name):  # 5-5 required
    im, d = new()
    title(d, "ばね＋荷重の系（全ポテンシャルエネルギー）")
    cy = 220
    xw, xb = 140, 420
    wall(d, xw, cy - 50, cy + 50, side=1, n=7)
    spring(d, xw, cy, xb, coils=6, amp=18)
    ctext(d, (xw + xb) / 2, cy - 40, "ばね定数 k", FT, GRAY)
    # 質点/端部ブロック
    d.rectangle((xb, cy - 34, xb + 40, cy + 34), outline=BLACK, width=3, fill=FILL2)
    # 荷重 f（右向き）
    force(d, xb + 40, cy, 90, 0, "f（荷重）", RED)
    # 変位 u
    dash(d, xb + 20, cy - 60, xb + 20, cy + 70, LGRAY)
    arrow(d, xb + 20, cy + 62, xb + 70, cy + 62, BLUE, 3, 12)
    ctext(d, xb + 80, cy + 62, "u（変位）", FT, BLUE, "lm")
    note(d, "弾性エネルギーと外力の仕事")
    save(im, name)


def disp_stress_method(name):  # 5-6 required
    im, d = new()
    title(d, "変位法の流れ（未知量＝節点変位）")
    y1, y2 = 150, 300
    block(d, 150, y1, 180, 54, "節点変位")
    block(d, 430, y1, 200, 54, "ひずみ")
    block(d, 430, y2, 200, 54, "応力")
    block(d, 150, y2, 180, 54, "剛性方程式")
    # 節点変位 →(ひずみ-変位関係)→ ひずみ
    arrow(d, 240, y1, 330, y1, BLACK, 3, 12)
    ctext(d, 285, y1 - 18, "ひずみ-変位関係", FT, GRAY)
    # ひずみ →(応力-ひずみ関係)→ 応力
    arrow(d, 430, y1 + 27, 430, y2 - 27, BLACK, 3, 12)
    ctext(d, 540, (y1 + y2) / 2, "応力-ひずみ関係", FT, GRAY, "mm")
    # 応力 → 剛性方程式
    arrow(d, 330, y2, 240, y2, BLACK, 3, 12)
    ctext(d, 285, y2 - 18, "つり合い", FT, GRAY)
    save(im, name)


def bem_vs_fem(name):  # 5-7 required
    im, d = new()
    title(d, "同じ形状に対する2つの離散化")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    # 左：FEM（領域全体を要素分割）
    ox, oy = 90, 150
    d.rectangle((ox, oy, ox + 160, oy + 140), outline=BLACK, width=3, fill="white")
    for i in range(1, 4):
        d.line((ox + i * 40, oy, ox + i * 40, oy + 140), fill=GRAY, width=1)
    for j in range(1, 4):
        d.line((ox, oy + j * 35, ox + 160, oy + j * 35), fill=GRAY, width=1)
    ctext(d, ox + 80, oy + 170, "有限要素法（FEM）", FS)
    ctext(d, ox + 80, oy + 196, "領域全体を要素分割", FT, GRAY)
    # 右：BEM（境界線だけを分割）
    ox2 = 400
    d.rectangle((ox2, oy, ox2 + 160, oy + 140), outline=BLACK, width=4, fill="white")
    for i in range(5):
        node(d, ox2 + i * 40, oy, 4, BLACK)
        node(d, ox2 + i * 40, oy + 140, 4, BLACK)
    for j in range(1, 4):
        node(d, ox2, oy + j * 35, 4, BLACK)
        node(d, ox2 + 160, oy + j * 35, 4, BLACK)
    ctext(d, ox2 + 80, oy + 170, "境界要素法（BEM）", FS)
    ctext(d, ox2 + 80, oy + 196, "境界線だけを分割", FT, GRAY)
    save(im, name)


def sparse_dense(name):  # 5-8 required
    im, d = new()
    title(d, "疎行列と密行列（同サイズ）")
    cell = 34
    n = 6
    # 左：疎行列（対角付近だけ非ゼロ・帯状）
    ox, oy = 90, 120
    for r in range(n):
        for c in range(n):
            if abs(r - c) <= 1:
                fillcell(d, ox + c * cell, oy + r * cell, cell, FILL3)
    grid_lines(d, ox, oy, n, n, cell)
    ctext(d, ox + n * cell / 2, oy + n * cell + 24, "疎行列（帯状に非ゼロ）", FS)
    # 右：密行列（全成分が埋まる）
    ox2 = 400
    for r in range(n):
        for c in range(n):
            fillcell(d, ox2 + c * cell, oy + r * cell, cell, FILL3)
    grid_lines(d, ox2, oy, n, n, cell)
    ctext(d, ox2 + n * cell / 2, oy + n * cell + 24, "密行列（全成分が非ゼロ）", FS)
    note(d, "灰色＝非ゼロ成分")
    save(im, name)


def q4_modes(name):  # 5-9 required
    im, d = new()
    title(d, "四辺形1次要素の基本変形モード")
    S = 90
    conf = [(120, 130, "剛体並進"), (400, 130, "剛体回転"),
            (120, 300, "一軸引張り"), (400, 300, "せん断")]
    for (ox, oy, lab) in conf:
        base = [(ox, oy), (ox + S, oy), (ox + S, oy + S), (ox, oy + S)]
        # 元(破線)
        dashrect(d, ox, oy, ox + S, oy + S, LGRAY)
        if lab == "剛体並進":
            dx = 22
            pts = [(p[0] + dx, p[1]) for p in base]
            for p in base:
                arrow(d, p[0], p[1], p[0] + dx, p[1], RED, 2, 8)
        elif lab == "剛体回転":
            cx, cy = ox + S / 2, oy + S / 2
            ang = math.radians(12)
            pts = []
            for p in base:
                vx, vy = p[0] - cx, p[1] - cy
                pts.append((cx + vx * math.cos(ang) - vy * math.sin(ang),
                            cy + vx * math.sin(ang) + vy * math.cos(ang)))
            curve_arrow(d, cx, cy, 30, 60, 120, RED, 2, 9)
        elif lab == "一軸引張り":
            e = 20
            pts = [(ox - e, oy), (ox + S + e, oy), (ox + S + e, oy + S), (ox - e, oy + S)]
            arrow(d, ox, oy + S / 2, ox - e - 6, oy + S / 2, RED, 2, 8)
            arrow(d, ox + S, oy + S / 2, ox + S + e + 6, oy + S / 2, RED, 2, 8)
        else:  # せん断
            sh = 26
            pts = [(ox + sh, oy), (ox + S + sh, oy), (ox + S, oy + S), (ox, oy + S)]
        d.line(pts + [pts[0]], fill=BLACK, width=3)
        ctext(d, ox + S / 2, oy + S + 24, lab, FT)
    save(im, name)


def node_interp(name):  # 5-10 required
    im, d = new()
    title(d, "三角形要素における内部点の補間")
    P1 = (170, 330); P2 = (500, 330); P3 = (330, 120)
    d.line([P1, P2, P3, P1], fill=BLACK, width=3)
    for p, lb in [(P1, "節点1"), (P2, "節点2"), (P3, "節点3")]:
        node(d, p[0], p[1], 8, "white")
        ctext(d, p[0], p[1] + (26 if p[1] > 250 else -26), lb, FT, GRAY)
    # 内部点 Pと各節点からの補間矢印
    Q = (330, 265)
    node(d, Q[0], Q[1], 5, RED)
    ctext(d, Q[0] + 14, Q[1] + 14, "内部点", FT, RED, "lm")
    for p in (P1, P2, P3):
        arrow(d, p[0], p[1], Q[0] + (p[0] - Q[0]) * 0.28, Q[1] + (p[1] - Q[1]) * 0.28, GRAY, 2, 9)
    note(d, "各節点の値から要素内部の値を補間")
    save(im, name)


def weighted_residual(name):  # 5-11 required
    im, d = new()
    title(d, "重みつき残差法：残差 R(x) に重み w(x)")
    ox, oy = 100, 250
    arrow(d, ox, oy, ox + 430, oy, BLACK, 2, 11); ctext(d, ox + 436, oy, "x", FT, BLACK, "lm")
    arrow(d, ox, oy + 80, ox, oy - 120, BLACK, 2, 11)
    # 残差 R(x) 曲線
    pts = []
    for i in range(61):
        t = i / 60.0
        x = ox + 400 * t
        y = oy - 70 * math.sin(math.pi * t) * math.cos(2.2 * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, RED)
    ctext(d, ox + 330, oy - 66, "残差 R(x)", FT, RED, "lm")
    # 重み w(x)
    dash(d, ox, oy - 40, ox + 400, oy - 40, BLUE)
    ctext(d, ox + 120, oy - 54, "重み w(x)", FT, BLUE)
    ctext(d, W / 2, oy + 70, "積分 ∫ w(x) R(x) dx = 0 となるよう近似解を決める", FT, GRAY)
    ctext(d, W / 2, oy + 96, "重みの取り方: ガラーキン / 選点法 / 最小二乗", FT, GRAY)
    save(im, name)


def partition_unity(name):  # 5-12 helpful
    im, d = new()
    title(d, "形状関数の性質：N1 + N2 = 1（1の分割）")
    ox, oy = 120, 320
    axes(d, ox, oy, 420, 240, "x", "N")
    xR = ox + 360
    top = 180
    dim(d, ox, oy + 30, xR, oy + 30, "0 <= x <= l", col=GRAY)
    dash(d, ox, oy - top, xR, oy - top, LGRAY)
    ctext(d, ox - 14, oy - top, "1", FT, GRAY, "rm")
    # N1 = 1 - x/l （下がる）
    plot(d, 0, 0, [(ox, oy - top), (xR, oy)], BLUE)
    ctext(d, ox + 70, oy - top + 40, "N1 = 1 - x/l", FT, BLUE, "lm")
    # N2 = x/l （上がる）
    plot(d, 0, 0, [(ox, oy), (xR, oy - top)], GREEN)
    ctext(d, xR - 100, oy - top + 40, "N2 = x/l", FT, GREEN, "lm")
    # 和 = 1 （水平・太赤破線）
    dash(d, ox, oy - top, xR, oy - top, RED, 3, 12)
    ctext(d, (ox + xR) / 2, oy - top - 18, "N1 + N2 = 1", FS, RED)
    save(im, name)


def static_dynamic_setup(name):  # 5-13 required
    im, d = new()
    title(d, "同じ構造に対する静的解析と動的解析")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    # 左：静荷重で変形
    ox, oy = 110, 190
    d.line((ox, oy, ox + 160, oy), fill=LGRAY, width=2)
    for i in range(5):
        node(d, ox + i * 40, oy, 4, "white")
    pts = [(ox + i * 40, oy + 44 * math.sin(math.pi * i / 4)) for i in range(5)]
    plot(d, 0, 0, pts, BLACK)
    force(d, ox + 80, oy - 60, 0, 44, "静荷重", RED)
    ctext(d, ox + 80, oy + 130, "静的解析", FS)
    ctext(d, ox + 80, oy + 156, "静荷重で変形", FT, GRAY)
    # 右：振動している
    ox2 = 400
    d.line((ox2, oy, ox2 + 160, oy), fill=LGRAY, width=2)
    for i in range(5):
        node(d, ox2 + i * 40, oy, 4, "white")
    up = [(ox2 + i * 40, oy - 40 * math.sin(math.pi * i / 4)) for i in range(5)]
    dn = [(ox2 + i * 40, oy + 40 * math.sin(math.pi * i / 4)) for i in range(5)]
    plot(d, 0, 0, up, BLUE); plot(d, 0, 0, dn, BLUE)
    arrow(d, ox2 + 80, oy - 50, ox2 + 80, oy - 20, BLUE, 2, 9)
    arrow(d, ox2 + 80, oy + 50, ox2 + 80, oy + 20, BLUE, 2, 9)
    ctext(d, ox2 + 80, oy + 130, "動的解析", FS)
    ctext(d, ox2 + 80, oy + 156, "振動している", FT, GRAY)
    save(im, name)


def unit_system(name):  # 5-14 required
    im, d = new()
    title(d, "整合単位系（基本量の単位）")
    ox, oy = 130, 90
    cw, ch = 200, 46
    rows = [("量", "単位"), ("長さ", "mm"), ("質量", "kg"),
            ("時間", "s"), ("密度", "kg/mm^3")]
    for i, (a, b) in enumerate(rows):
        y = oy + i * ch
        fill = FILL2 if i == 0 else "white"
        d.rectangle((ox, y, ox + cw, y + ch), outline=BLACK, width=2, fill=fill)
        d.rectangle((ox + cw, y, ox + cw * 2, y + ch), outline=BLACK, width=2, fill=fill)
        ctext(d, ox + cw / 2, y + ch / 2, a, FS)
        ctext(d, ox + cw * 1.5, y + ch / 2, b, FS)
    # 力 = 質量 × 加速度 の枠
    block(d, W / 2, 360, 420, 48, "力 = 質量 × 加速度", F, FILL1)
    save(im, name)


def global_assembly(name):  # 5-15 required
    im, d = new()
    title(d, "直列2ばねの全体剛性行列の組立")
    cy = 115
    xs = [130, 300, 470]
    wall(d, 100, cy - 34, cy + 34, side=1, n=5)
    for i in range(2):
        spring(d, xs[i], cy, xs[i + 1], coils=5, amp=13)
    for i, x in enumerate(xs):
        node(d, x, cy, 7, "white"); ctext(d, x, cy - 30, str(i + 1), FT, GRAY)
    ctext(d, (xs[0] + xs[1]) / 2, cy + 26, "k1", FT, BLUE)
    ctext(d, (xs[1] + xs[2]) / 2, cy + 26, "k2", FT, GREEN)
    # 3x3 全体行列に 2x2 要素行列を重ねる配置
    ox, oy, cell = 250, 205, 52
    grid_lines(d, ox, oy, 3, 3, cell)
    for i in range(3):
        ctext(d, ox - 16, oy + i * cell + cell / 2, str(i + 1), FT, GRAY)
        ctext(d, ox + i * cell + cell / 2, oy - 16, str(i + 1), FT, GRAY)
    # 要素1 → 節点1,2（左上2x2）
    dashrect(d, ox, oy, ox + 2 * cell, oy + 2 * cell, BLUE, 3)
    ctext(d, ox + cell, oy - 34, "[k_e1] を節点1-2へ", FT, BLUE)
    # 要素2 → 節点2,3（右下2x2）
    dashrect(d, ox + cell, oy + cell, ox + 3 * cell, oy + 3 * cell, GREEN, 3)
    ctext(d, ox + 2 * cell, oy + 3 * cell + 18, "[k_e2] を節点2-3へ", FT, GREEN)
    ctext(d, ox + 1.5 * cell, oy + 1.5 * cell, "重なり", FT, RED)
    save(im, name)


def constrained(name):  # 5-16 required
    im, d = new()
    title(d, "一端固定：固定自由度の行・列を除外")
    cy = 130
    xs = [150, 300, 450]
    wall(d, 120, cy - 34, cy + 34, side=1, n=5)
    for i in range(2):
        spring(d, xs[i], cy, xs[i + 1], coils=5, amp=12)
    for i, x in enumerate(xs):
        node(d, x, cy, 7, "white"); ctext(d, x, cy - 30, str(i + 1), FT, GRAY)
    ctext(d, xs[0], cy + 34, "固定", FT, RED)
    # 3x3 行列で 節点1の行・列を除外(破線で囲む)
    ox, oy, cell = 250, 200, 54
    grid_lines(d, ox, oy, 3, 3, cell)
    for i in range(3):
        ctext(d, ox - 16, oy + i * cell + cell / 2, str(i + 1), FT, GRAY)
        ctext(d, ox + i * cell + cell / 2, oy - 16, str(i + 1), FT, GRAY)
    # 1行目・1列目を斜線で除外表示
    for r in range(3):
        fillcell(d, ox, oy + r * cell, cell, FILL3)
        fillcell(d, ox + r * cell, oy, cell, FILL3)
    dashrect(d, ox + cell, oy + cell, ox + 3 * cell, oy + 3 * cell, RED, 3)
    ctext(d, ox + 2 * cell, oy + 3 * cell + 20, "残す部分（節点2,3）", FT, RED)
    ctext(d, ox + 3 * cell + 20, oy + cell / 2, "固定節点1の", FT, GRAY, "lm")
    ctext(d, ox + 3 * cell + 20, oy + cell / 2 + 20, "行・列を除外", FT, GRAY, "lm")
    save(im, name)


def mass_matrix_types(name):  # 5-17 helpful
    im, d = new()
    title(d, "整合質量行列と集中質量行列")
    d.line((330, 60, 330, 402), fill=LGRAY, width=2)
    # 左：整合（対角＋非対角に値）
    matrix_grid(d, 100, 150, [["a", "b"], ["b", "a"]], cell=64)
    ctext(d, 164, 300, "整合質量行列", FS)
    ctext(d, 164, 328, "非対角にも値", FT, GRAY)
    # 右：集中（対角のみ）
    matrix_grid(d, 400, 150, [["m", "0"], ["0", "m"]], cell=64)
    ctext(d, 464, 300, "集中質量行列", FS)
    ctext(d, 464, 328, "対角のみ（非対角0）", FT, GRAY)
    save(im, name)


def tri_mass(name):  # 5-18 required
    im, d = new()
    title(d, "3節点三角形要素の質量行列（2通りの考え方）")
    # 三角形要素
    P1 = (110, 320); P2 = (330, 320); P3 = (220, 140)
    d.line([P1, P2, P3, P1], fill=BLACK, width=3)
    for p in (P1, P2, P3):
        node(d, p[0], p[1], 7, "white")
    ctext(d, 220, 275, "面積 A", FT, GRAY)
    # 右上：整合＝面積上で積分
    arrow(d, 350, 200, 430, 200, GRAY, 3, 12)
    ctext(d, 540, 185, "整合", FS, BLUE)
    ctext(d, 540, 210, "面積上で積分", FT, GRAY)
    # 右下：集中＝全質量を各節点へ配分
    arrow(d, 350, 300, 430, 300, GRAY, 3, 12)
    ctext(d, 540, 285, "集中", FS, GREEN)
    ctext(d, 540, 310, "全質量を各節点へ配分", FT, GRAY)
    save(im, name)


def bar_consistent_mass(name):  # 5-19 required
    im, d = new()
    title(d, "2節点棒要素（線密度 mu・全長 l）")
    cy = 150
    x0, x1 = 130, 500
    d.rectangle((x0, cy - 22, x1, cy + 22), outline=BLACK, width=3, fill=FILL1)
    node(d, x0, cy, 6, BLACK); node(d, x1, cy, 6, BLACK)
    ctext(d, x0, cy - 40, "節点1", FT, GRAY); ctext(d, x1, cy - 40, "節点2", FT, GRAY)
    dim(d, x0, cy + 44, x1, cy + 44, "l", col=GRAY)
    ctext(d, (x0 + x1) / 2, cy, "線密度 mu", FT, GRAY)
    # 形状関数グラフ
    ox, oy = 130, 350
    arrow(d, ox, oy, ox + 380, oy, BLACK, 2, 10); ctext(d, ox + 386, oy, "x", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - 110, BLACK, 2, 10)
    xR = ox + 360; top = 90
    dash(d, ox, oy - top, xR, oy - top, LGRAY); ctext(d, ox - 12, oy - top, "1", FT, GRAY, "rm")
    plot(d, 0, 0, [(ox, oy - top), (xR, oy)], BLUE)
    ctext(d, ox + 60, oy - top + 26, "L1 = 1 - x/l", FT, BLUE, "lm")
    plot(d, 0, 0, [(ox, oy), (xR, oy - top)], GREEN)
    ctext(d, xR - 90, oy - top + 26, "L2 = x/l", FT, GREEN, "lm")
    save(im, name)


if __name__ == "__main__":
    discretize_map("v2e5DiscretizeMap")
    shape_func_interp("v2e5ShapeFuncInterp")
    beam_element_dof("v2e5BeamElementDOF")
    bar_long_wave("v2e5BarLongWave")
    potential_spring("v2e5PotentialSpring")
    disp_stress_method("v2e5DispStressMethod")
    bem_vs_fem("v2e5BEMvsFEM")
    sparse_dense("v2e5SparseDense")
    q4_modes("v2e5Q4Modes")
    node_interp("v2e5NodeInterp")
    weighted_residual("v2e5WeightedResidual")
    partition_unity("v2e5PartitionUnity")
    static_dynamic_setup("v2e5StaticDynamicSetup")
    unit_system("v2e5UnitSystem")
    global_assembly("v2e5GlobalAssembly")
    constrained("v2e5Constrained")
    mass_matrix_types("v2e5MassMatrixTypes")
    tri_mass("v2e5TriMass")
    bar_consistent_mass("v2e5BarConsistentMass")
    print("done 19")
