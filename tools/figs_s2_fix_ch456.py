# -*- coding: utf-8 -*-
"""固体2級 レビュー修正(第4・5・6章)で図を問題条件に合わせて再生成する。
元の生成スクリプトはリポジトリに残っていないため figlib.py で作り直す。
 f4LinearInterp : u1=3,u2=9,x=3L/4 → u=7.5mm(誤:u1=2,u2=6,x=L/4,3mm)
 f4InclinedSpring: k=120,θ=60°,k_xy=k sinθcosθ≈52.0(誤:k=100,30°,k_xx=75)
 f5BodyForce    : 物体力(体積力:重力/遠心力/浮力,dV) と 表面力(圧力,dS) の対比 ※5-12概念化に伴い差替
 f5SeriesSprings: 3ばね・4節点,u4=6→u2=3,u3=4.5(誤:2ばね・3節点)
 num6ElemGauss  : 8点を奥行き2層で表示(誤:手前1面に8点)
実行すると assets/figures/*.png を上書きする。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8, gap=6):
    total = math.hypot(x2 - x1, y2 - y1)
    if total == 0:
        return
    ux, uy = (x2 - x1) / total, (y2 - y1) / total
    t = 0.0
    while t < total:
        a = min(t + dash, total)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def cross(d, x, y, s, col, wd):
    d.line((x - s, y - s, x + s, y + s), fill=col, width=wd)
    d.line((x - s, y + s, x + s, y - s), fill=col, width=wd)


def fig_f4_linear_interp():
    im, d = new()
    title(d, "1次要素の線形補間  u(x)=N₁u₁+N₂u₂")
    ox, oy = 110, 345
    xL = 420                      # x=L のピクセル位置オフセット
    sy = 26                       # u 1mm あたり
    def X(f): return ox + f * xL  # f は 0..1 の x/L
    def U(u): return oy - u * sy
    axes(d, ox, oy, xL + 70, 10 * sy + 30, "x", "")
    ctext(d, ox - 6, U(10) + 4, "u (mm)", FS, BLACK, "rm")
    # 節点値を結ぶ直線
    p1 = (X(0), U(3)); p2 = (X(1), U(9))
    plot(d, 0, 0, [p1, p2], BLUE, 3)
    node(d, *p1, 7); node(d, *p2, 7)
    ctext(d, X(0) - 6, U(3) + 20, "u₁=3", FS, BLACK, "lm")
    ctext(d, X(1) + 8, U(9) - 6, "u₂=9", FS, BLACK, "lm")
    # 内挿点 x=3L/4, u=7.5
    px, py = X(0.75), U(7.5)
    dashed(d, px, py, px, oy)
    dashed(d, px, py, ox, py)
    d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=RED, outline=RED)
    ctext(d, ox - 8, py, "7.5", FS, RED, "rm")
    ctext(d, px, oy + 16, "x=3L/4", FT, RED)
    ctext(d, X(1), oy + 16, "L", FT, BLACK)
    note(d, "節点2寄りの点なので N₂=3/4 が大きく、u=¼·3+¾·9=7.5 mm")
    save(im, "f4LinearInterp")


def fig_f4_inclined_spring():
    im, d = new()
    title(d, "斜めばねの剛性成分  k_xy = k sinθcosθ")
    ox, oy = 90, 350
    axes(d, ox, oy, 250, 300, "x", "y")
    # 60度傾いたばね
    th = math.radians(60); Lp = 250
    ex, ey = ox + Lp * math.cos(th), oy - Lp * math.sin(th)
    spring(d, ox, oy, ex, ey, coils=6, amp=15)
    node(d, ox, oy, 6); node(d, ex, ey, 6)
    angle_arc(d, ox, oy, 58, 0, 60, "θ=60°")
    ctext(d, (ox + ex) / 2 + 26, (oy + ey) / 2, "k=120 N/mm", FS, BLUE, "lm")
    # 全体座標の3成分
    tx = 360
    ctext(d, tx, 165, "全体座標の剛性成分:", FS, BLACK, "lm")
    ctext(d, tx, 200, "k_xx = k cos²θ = 30", FS, GRAY, "lm")
    ctext(d, tx, 232, "k_yy = k sin²θ = 90", FS, GRAY, "lm")
    ctext(d, tx, 266, "k_xy = k sinθcosθ ≈ 52.0", FS, RED, "lm")
    note(d, "k_xy = k sinθcosθ = 120×sin60°×cos60° ≈ 52.0 N/mm")
    save(im, "f4InclinedSpring")


def fig_f5_body_force():
    # 5-12(概念:物体力の取扱い)用。物体力=体積力(重力/遠心力/浮力・体積全体dV)と
    # 表面力(圧力・表面のみdS)の違いを対比。圧力は表面力=物体力でない(=誤り選択の答え)。
    im, d = new()
    title(d, "物体力(体積力) と 表面力(圧力) の違い")
    # 左:物体力=体積全体に作用
    lx0, lx1, y0, y1 = 90, 235, 130, 300
    d.rectangle((lx0, y0, lx1, y1), outline=BLACK, width=3, fill=FILL1)
    for cx in range(lx0 + 24, lx1 - 10, 36):
        for cy in range(y0 + 22, y1 - 6, 40):
            arrow(d, cx, cy, cx, cy + 22, GRAY, 2, 7)
    ctext(d, (lx0 + lx1) // 2, 108, "物体力(体積力)", FS, BLACK)
    ctext(d, (lx0 + lx1) // 2, 322, "重力・遠心力・浮力", FT, BLACK)
    ctext(d, (lx0 + lx1) // 2, 348, "体積全体に作用  ∫N^T b dV", FT, GRAY)
    # 右:表面力=表面のみに作用(圧力)
    rx0, rx1 = 425, 570
    d.rectangle((rx0, y0, rx1, y1), outline=BLACK, width=3, fill=FILL1)
    for cx in range(rx0 + 18, rx1 - 6, 26):
        arrow(d, cx, y0 - 26, cx, y0 - 2, BLUE, 2, 8)   # 上面(表面)に垂直な圧力
    ctext(d, (rx0 + rx1) // 2, 108, "表面力(圧力)", FS, BLUE)
    ctext(d, (rx0 + rx1) // 2, 322, "圧力は表面だけに作用", FT, BLUE)
    ctext(d, (rx0 + rx1) // 2, 348, "面のみ  ∫N^T p dS", FT, GRAY)
    ctext(d, 330, 215, "≠", FL, BLACK)
    note(d, "物体力=体積全体(dV)。圧力は表面のみ(dS)=表面力→物体力ではない。")
    save(im, "f5BodyForce")


def fig_f5_series_springs():
    im, d = new()
    title(d, "直列3ばねと強制変位(節点1固定・節点4を強制変位)")
    y = 210
    wall(d, 60, y - 60, y + 60, side=1)
    nx = [80, 235, 390, 545]
    ks = ["k₁=100", "k₂=200", "k₃=200"]
    for i in range(3):
        spring(d, nx[i], y, nx[i + 1], y, coils=5, amp=14)
        ctext(d, (nx[i] + nx[i + 1]) / 2, y - 36, ks[i], FS, BLACK)
    for x in nx:
        node(d, x, y, 6)
    # 節点4に強制変位(値は下のラベルに記載)
    force(d, nx[3], y, 58, 0, "", BLUE)
    labels = [("節点1", "u₁=0", BLUE), ("節点2", "u₂=?", RED),
              ("節点3", "u₃=4.5", BLACK), ("節点4", "u₄=6", BLUE)]
    for x, (a, b, c) in zip(nx, labels):
        ctext(d, x, y + 34, a, FT, BLACK)
        ctext(d, x, y + 54, b, FS, c)
    note(d, "節点2・3は外力なし → 連立を解くと u₂=3・u₃=4.5 mm")
    save(im, "f5SeriesSprings")


def fig_num6_elem_gauss():
    im, d = new()
    title(d, "8節点六面体の完全積分(2×2×2=8点)")
    ox, oy, w, h, dp = 205, 155, 230, 175, 115
    dx, dy = int(dp * 0.8), int(dp * 0.5)   # 92, 57
    iso_box(d, ox, oy, w, h, dp)
    fx = [ox + w * 0.30, ox + w * 0.70]
    fy = [oy + h * 0.32, oy + h * 0.68]
    front = [(x, y) for y in fy for x in fx]
    back = [(x + dx, y - dy) for (x, y) in front]
    for (fp, bp) in zip(front, back):
        dashed(d, fp[0], fp[1], bp[0], bp[1], LGRAY, 1, 6, 5)
    for (x, y) in back:
        cross(d, x, y, 9, (225, 150, 150), 2)
    for (x, y) in front:
        cross(d, x, y, 11, RED, 3)
    note(d, "各方向2点 → 奥行きにも2層。2×2×2 = 8点")
    save(im, "num6ElemGauss")


if __name__ == "__main__":
    fig_f4_linear_interp()
    fig_f4_inclined_spring()
    fig_f5_body_force()
    fig_f5_series_springs()
    fig_num6_elem_gauss()
