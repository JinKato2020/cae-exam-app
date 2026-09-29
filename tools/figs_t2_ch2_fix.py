# -*- coding: utf-8 -*-
"""熱流体2級 第2章 図の再生成(生成元スクリプト消失のため新規作成)。
- t2e2AccelTank (2-4, required=設定図): 誤った図注 tanβ=a/g を削除。斜面θ・加速度a・
  水平からβ傾いた水面・重力g/慣性力ma/合力ベクトルのみ(数値・式は書かない)。
- t2e2Streakline (2-18, helpful=結果図): 流脈線を正しい座標
  発生源(0,0)→折れ点(1,-0.5)→先端(3,0.5) の折れ線に修正。
JSON本体は編集しない。white 660x420 線画。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def accel_tank():
    im, d = new()
    title(d, "加速するタンクの自由表面（相対的静止）")
    th = math.radians(20)
    ux, uy = math.cos(th), -math.sin(th)          # 斜面上向き(up-slope)
    nx, ny = -math.sin(th), -math.cos(th)          # 斜面の外向き法線(上)
    Bx, By = 150, 350                              # 斜面下端
    Tx, Ty = Bx + 380 * ux, By + 380 * uy          # 斜面上端
    # 水平の基準線(破線)と傾斜角θ
    for xx in range(Bx, 575, 14):
        d.line((xx, By, xx + 7, By), fill=LGRAY, width=2)
    d.line((Bx, By, Tx, Ty), fill=BLACK, width=3)  # 斜面
    for t in range(0, 380, 34):                    # 斜面のハッチ(地面側)
        px, py = Bx + t * ux, By + t * uy
        d.line((px, py, px + 16 * math.sin(th), py + 16 * math.cos(th)), fill=BLACK, width=1)
    angle_arc(d, Bx, By, 46, 0, 20, "θ", GRAY)
    # タンク(斜面上の箱・上面開放・縦長で水面が壁から壁へ収まる寸法)
    C = (Bx + 185 * ux, By + 185 * uy)
    half, Ht = 50, 115
    BL = (C[0] - half * ux, C[1] - half * uy)
    BR = (C[0] + half * ux, C[1] + half * uy)
    TL = (BL[0] + Ht * nx, BL[1] + Ht * ny)
    TR = (BR[0] + Ht * nx, BR[1] + Ht * ny)
    # 自由表面(水平からβ傾く。下流側=左が高い): 傾き +tan(β)
    m = math.tan(math.radians(15.7))
    cx = (BL[0] + BR[0] + TL[0] + TR[0]) / 4
    cy = (BL[1] + BR[1] + TL[1] + TR[1]) / 4

    def hit(P, Q):                                  # 表面線と壁分節の交点
        px, py = P; qx, qy = Q
        dx, dy = qx - px, qy - py
        t = (cy + m * (px - cx) - py) / (dy - m * dx)
        return (px + t * dx, py + t * dy)
    LS = hit(BL, TL); RS = hit(BR, TR)
    d.polygon([BL, BR, RS, LS], fill=(222, 234, 248), outline=None)  # 水(先に塗る)
    d.line((BL[0], BL[1], BR[0], BR[1]), fill=BLACK, width=3)   # 底
    d.line((BL[0], BL[1], TL[0], TL[1]), fill=BLACK, width=3)   # 左壁
    d.line((BR[0], BR[1], TR[0], TR[1]), fill=BLACK, width=3)   # 右壁
    d.line((LS[0], LS[1], RS[0], RS[1]), fill=BLUE, width=3)    # 自由表面
    # β(水面と水平の角)
    sp = (300, cy + m * (300 - cx))
    for xx in range(int(sp[0]), int(sp[0]) + 70, 12):
        d.line((xx, sp[1], xx + 6, sp[1]), fill=LGRAY, width=2)
    angle_arc(d, sp[0], sp[1], 40, -16, 0, "β", GRAY)
    # 加速度a(斜面に沿って上向き)
    ax, ay = 402, 196
    arrow(d, ax, ay, ax + 74 * ux, ay + 74 * uy, GREEN, 4, 14)
    ctext(d, ax + 82 * ux, ay + 74 * uy - 12, "a", F, GREEN, "lm")
    # 力ベクトル(重力g・慣性力ma・合力) 同一始点から
    O = (556, 250)
    force(d, O[0], O[1], 0, 72, "g", RED)                        # 重力(下)
    force(d, O[0], O[1], -62 * ux, -62 * uy, "ma", ORANGE)        # 慣性力(斜面下向き=-u)
    rx, ry = 0 - 62 * ux, 72 - 62 * uy
    arrow(d, O[0], O[1], O[0] + rx, O[1] + ry, BLUE, 4, 15)
    ctext(d, O[0] + rx - 8, O[1] + ry + 12, "合力", FS, BLUE, "rm")
    note(d, "水面は重力と慣性力の合力に垂直（角度・数値は本文参照）")
    save(im, "t2e2AccelTank")


def streakline():
    im, d = new()
    title(d, "非定常流の流脈線（t = 3 s の形）")
    ox, oy = 150, 232
    sx, sy = 104, 70
    def P(x, y): return (ox + x * sx, oy - y * sy)
    # 軸
    arrow(d, ox, oy, ox + 380, oy, BLACK, 2, 11); ctext(d, ox + 390, oy, "x", FS, BLACK, "lm")
    arrow(d, ox, oy + 60, ox, oy - 110, BLACK, 2, 11); ctext(d, ox - 12, oy - 116, "y", FS, BLACK, "rm")
    P0, P1, P2 = P(0, 0), P(1, -0.5), P(3, 0.5)
    # 流脈線(折れ線)
    d.line((P0[0], P0[1], P1[0], P1[1]), fill=BLUE, width=4)
    d.line((P1[0], P1[1], P2[0], P2[1]), fill=BLUE, width=4)
    # トレーサー粒子(連続放出)
    for a, b in [(P0, P1), (P1, P2)]:
        for t in (0.25, 0.5, 0.75):
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            d.ellipse((px - 3, py - 3, px + 3, py + 3), fill=BLUE, outline=BLUE)
    for pt in (P0, P1, P2):
        node(d, pt[0], pt[1], 6, fill="white", col=BLUE)
    ctext(d, P0[0] - 6, P0[1] - 16, "発生源 (0, 0)", FT, BLACK, "rm")
    ctext(d, P1[0], P1[1] + 22, "折れ点 (1, -0.5)", FT, BLACK, "mm")
    ctext(d, P2[0] + 8, P2[1] - 14, "先端 (3, 0.5)", FT, BLACK, "lm")
    note(d, "t=2 s で v が反転し線が折れる。非定常流では流線・流跡線・流脈線は一致しない")
    save(im, "t2e2Streakline")


if __name__ == "__main__":
    accel_tank()
    streakline()
    print("done ch2 fix 2")
