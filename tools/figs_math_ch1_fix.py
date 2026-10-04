# -*- coding: utf-8 -*-
"""固体2級 第1章の公式用語カード用の図を日本語で作り直す（旧版は英語表記でgenerator消失）。
mathDet3x3 = 3×3行列式の余因子展開 / mathEigenVec = 固有ベクトルの意味。白地660x420・figlib。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def mathDet3x3():
    im, d = new(); title(d, "3×3行列式：第1列による余因子展開")
    main = [["2", "3", "1"], ["0", "1", "4"], ["5", "2", "0"]]
    cell = 56
    mx, my = 108, 86
    matrix_grid(d, mx, my, main, cell=cell)
    # 第1列(余因子展開に使う列)を赤枠で強調
    d.rectangle((mx, my, mx + cell, my + 3 * cell), outline=RED, width=3)
    # 符号(+,-,+) を各行の左に
    signs = ["＋", "−", "＋"]
    for i, s in enumerate(signs):
        ctext(d, mx - 26, my + i * cell + cell / 2, s, FS, RED)
    # 小行列式 M11, M31
    def minor(d, x, y, vals, cap, det):
        matrix_grid(d, x, y, vals, cell=48)
        ctext(d, x + 48, y - 16, cap, FS, BLUE)
        ctext(d, x + 48, y + 2 * 48 + 18, det, FT, BLUE)
    minor(d, 470, 92, [["1", "4"], ["2", "0"]], "M11", "det=1·0−4·2=−8")
    minor(d, 470, 250, [["3", "1"], ["1", "4"]], "M31", "det=3·4−1·1=11")
    # 矢印(第1列の 2→M11, 5→M31)
    arrow(d, mx + cell, my + cell / 2, 466, 140, RED, 2, 10)
    arrow(d, mx + cell, my + 2 * cell + cell / 2, 466, 300, BLUE, 2, 10)
    ctext(d, 330, 200, "C21=−M21\n(0倍なので不要)", FT, GRAY)
    note(d, "det(A)=2·(+M11)+0·(−M21)+5·(+M31)=2·(−8)+5·11=39")
    save(im, "mathDet3x3")


def mathEigenVec():
    im, d = new(); title(d, "固有ベクトル：向きが変わらず λ 倍されるベクトル")
    ox, oy = 330, 300
    node(d, ox, oy, 5, fill=BLACK)

    def dash(x1, y1, x2, y2, col, wd=3, dl=10, gp=7):
        L = math.hypot(x2 - x1, y2 - y1); t = 0
        uxx, uyy = (x2 - x1) / L, (y2 - y1) / L
        while t < L:
            a = min(t + dl, L)
            d.line((x1 + uxx * t, y1 + uyy * t, x1 + uxx * a, y1 + uyy * a), fill=col, width=wd)
            t += dl + gp

    # 固有ベクトル v 方向(2,-1)（右上がり）。A v = λ v （同じ向きに伸びる）
    ux, uy = 2 / math.sqrt(5), -1 / math.sqrt(5)
    vlen = 62
    lam = 2.6
    avx, avy = ox + ux * vlen * lam, oy + uy * vlen * lam
    arrow(d, ox, oy, avx, avy, RED, 4, 15)
    ctext(d, avx - 150, avy - 18, "A v = λv（向き不変・λ倍）", FT, RED, "lm")
    vx, vy = ox + ux * vlen, oy + uy * vlen
    node(d, vx, vy, 5, fill="white", col=RED)
    ctext(d, vx + 4, vy + 18, "固有ベクトル v", FT, RED, "lm")
    # 一般ベクトル u（青）と A u（向きが変わる・青破線）
    wx, wy = ox - 120, oy - 95   # u 方向 左上
    arrow(d, ox, oy, wx, wy, BLUE, 3, 12)
    ctext(d, wx + 2, wy - 12, "一般ベクトル u", FT, BLUE, "lm")
    aux, auy = ox - 175, oy - 48   # A u はより水平寄り＝向きが回転
    dash(ox, oy, aux, auy, BLUE)
    arrow(d, aux + 10, auy - 2.7, aux, auy, BLUE, 3, 12)
    ctext(d, aux + 4, auy + 18, "A u（向きが変わる）", FT, BLUE, "lm")
    note(d, "[A]{x}=λ{x} を満たす {x}＝固有ベクトル、λ＝固有値。固有ベクトルだけ向きが保たれる")
    save(im, "mathEigenVec")


def mathDetScale():
    im, d = new(); title(d, "行列式 ＝ 面積（体積）の拡大率　とその性質")
    LB = (222, 235, 250)
    # 単位正方形
    sx, sy, s = 80, 150, 70
    d.rectangle((sx, sy, sx + s, sy + s), outline=BLACK, width=3, fill=FILL1)
    ctext(d, sx + s / 2, sy + s / 2, "面積 1", FT, BLACK)
    ctext(d, sx + s / 2, sy + s + 20, "単位正方形", FT, GRAY)
    # ×A 矢印
    arrow(d, sx + s + 14, sy + s / 2, sx + s + 110, sy + s / 2, RED, 3, 13)
    ctext(d, sx + s + 62, sy + s / 2 - 18, "×A", FS, RED)
    # 変換後の平行四辺形(面積=|A|)
    P0 = (300, 230)
    v1 = (104, -22); v2 = (42, -96)
    P1 = (P0[0] + v1[0], P0[1] + v1[1])
    P2 = (P0[0] + v2[0], P0[1] + v2[1])
    P3 = (P0[0] + v1[0] + v2[0], P0[1] + v1[1] + v2[1])
    d.polygon([P0, P1, P3, P2], outline=BLACK, width=3, fill=LB)
    ctext(d, (P0[0] + P3[0]) / 2, (P0[1] + P3[1]) / 2, "面積 = |A|", FS, BLUE)
    ctext(d, P0[0] + 70, P0[1] + 22, "det A = この拡大率", FT, GRAY)
    # 性質
    y = 300
    for line, col in [("・各辺を c 倍（cA）→ 面積は c² 倍 ： |cA| = c²|A|（n次なら cⁿ|A|）", BLACK),
                      ("・変換の合成（AB）→ 倍率の積 ： |AB| = |A||B|", BLACK),
                      ("・和では成り立たない ： |A+B| ≠ |A| + |B|", RED)]:
        ctext(d, 70, y, line, FT, col, "lm")
        y += 32
    save(im, "mathDetScale")


def mathGaussGreen():
    im, d = new(); title(d, "ガウス・グリーンの公式：領域 Ω と境界 Γ")
    LB = (226, 238, 250)
    cx, cy, rx, ry = 290, 225, 170, 115
    # 領域Ω(楕円)と境界Γ
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=BLACK, width=3, fill=LB)
    ctext(d, cx - 40, cy + 10, "領域 Ω", F, BLACK)
    ctext(d, cx - 40, cy + 40, "(体積/面積積分)", FT, GRAY)
    ctext(d, cx, cy - ry - 16, "境界 Γ", FS, BLACK)
    # ベクトル場 g(内部に数本)
    for (gx, gy) in [(cx - 70, cy - 30), (cx - 10, cy + 20), (cx - 100, cy + 40), (cx - 40, cy - 55)]:
        arrow(d, gx, gy, gx + 34, gy - 10, GRAY, 2, 8)
    ctext(d, cx - 120, cy - 70, "ベクトル場 g", FT, GRAY, "lm")
    # 境界上の点Pで外向き法線nとg
    P = (cx + rx, cy)   # 楕円の右端=法線は+x
    node(d, P[0], P[1], 5, fill=RED, col=RED)
    arrow(d, P[0], P[1], P[0] + 70, P[1], RED, 4, 14)
    ctext(d, P[0] + 76, P[1], "外向き法線 n", FT, RED, "lm")
    # その点での g と 流出成分 g·n
    arrow(d, P[0], P[1], P[0] + 52, P[1] - 40, GREEN, 3, 12)
    ctext(d, P[0] + 40, P[1] - 50, "g", FS, GREEN, "lm")
    def dash(x1, y1, x2, y2, col, wd=2, dl=8, gp=6):
        import math as m
        L = m.hypot(x2 - x1, y2 - y1); t = 0; ux, uy = (x2 - x1) / L, (y2 - y1) / L
        while t < L:
            a = min(t + dl, L); d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd); t += dl + gp
    dash(P[0] + 52, P[1] - 40, P[0] + 52, P[1], GRAY)
    ctext(d, P[0] + 26, P[1] + 18, "g·n=流出成分", FT, GREEN, "lm")
    note(d, "領域Ωの積分 ⇔ 境界Γ上の流出 g·n の積分（部分積分の多次元版＝発散定理の一般形）")
    save(im, "mathGaussGreen")


if __name__ == "__main__":
    mathDetScale()
    mathEigenVec()
    mathGaussGreen()
    print("done math ch1 figures")
