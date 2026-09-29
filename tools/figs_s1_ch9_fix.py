# -*- coding: utf-8 -*-
"""固体1級 第9章 レビュー修正の図(回答後 helpful)を再生成。生成元が消失していた2図。
- s1e9IterMatrix(9-3): 条件数の設問に合わせ、固有値 {-80,0.5,4,20} の絶対値を並べ
  |λ|max=80 / |λ|min=0.5 = 160 を示す(旧図は無関係な反復収束の模式図だった)。
- s1e9Complexity(9-15): 直接法 O(n^3) に整合する右上がりの曲線(旧図は途中で水平になり式と矛盾)。
  O(n^3)は密行列消去の概算である旨も添える。"""
import sys
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def f_cond_number():         # 9-3 回答後
    im, d = new(); title(d, "条件数 cond(K) = |λ|max / |λ|min")
    lam = ["-80", "0.5", "4", "20"]
    ab = ["80", "0.5", "4", "20"]
    x0 = 120; cw = 95; y0 = 110; rh = 46
    ncol = len(lam) + 1
    # 枠線
    for i in range(3):
        d.line((x0, y0 + i * rh, x0 + ncol * cw, y0 + i * rh), fill=BLACK, width=2)
    for j in range(ncol + 1):
        d.line((x0 + j * cw, y0, x0 + j * cw, y0 + 2 * rh), fill=BLACK, width=2)
    ctext(d, x0 + cw / 2, y0 + rh / 2, "λ", FS)
    ctext(d, x0 + cw / 2, y0 + rh + rh / 2, "|λ|", FS)
    for j, (l, a) in enumerate(zip(lam, ab), start=1):
        ctext(d, x0 + j * cw + cw / 2, y0 + rh / 2, l, FS)
        ctext(d, x0 + j * cw + cw / 2, y0 + rh + rh / 2, a, FS)
    # 最大(80=1列目)を赤、最小(0.5=2列目)を青で強調
    d.rectangle((x0 + 1 * cw, y0 + rh, x0 + 2 * cw, y0 + 2 * rh), outline=RED, width=4)
    d.rectangle((x0 + 2 * cw, y0 + rh, x0 + 3 * cw, y0 + 2 * rh), outline=BLUE, width=4)
    ctext(d, x0 + 1 * cw + cw / 2, y0 + 2 * rh + 18, "最大", FT, RED)
    ctext(d, x0 + 2 * cw + cw / 2, y0 + 2 * rh + 18, "最小", FT, BLUE)
    ctext(d, W / 2, 268, "|λ|max = 80,   |λ|min = 0.5", FS)
    ctext(d, W / 2, 305, "cond(K) = 80 / 0.5 = 160", F, RED)
    note(d, "条件数は必ず絶対値で評価する。負の -80 が絶対値最大、0.5 が絶対値最小")
    save(im, "s1e9IterMatrix")


def f_complexity():          # 9-15 回答後
    im, d = new(); title(d, "直接法の計算時間 ∝ O(n³)(右上がり)")
    ox, oy = 120, 330; xlen, ylen = 430, 250
    axes(d, ox, oy, xlen, ylen, "自由度 n", "計算時間")
    tmax = 3.3; ymax = 120.0
    pts = []
    t = 0.0
    while t <= 3.05:
        yv = 4.0 * t ** 3
        px = ox + (t / tmax) * xlen
        py = oy - (yv / ymax) * ylen
        pts.append((px, py)); t += 0.05
    plot(d, ox, oy, pts, RED, 4)
    # 代表点 (n,4s) と (3n,108s)
    for t, sec, lab in [(1.0, 4.0, "n → 4秒"), (3.0, 108.0, "3n → 108秒")]:
        px = ox + (t / tmax) * xlen; py = oy - (sec / ymax) * ylen
        d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=BLACK)
        d.line((px, oy, px, py), fill=GRAY, width=1)
        ctext(d, px + 6, py - 14, lab, FT, BLACK, "lm")
        ctext(d, px, oy + 16, "n" if t == 1.0 else "3n", FT, GRAY)
    note(d, "自由度3倍で時間は3³=27倍。O(n³)は密行列のガウス消去を想定した概算(疎行列は別)")
    save(im, "s1e9Complexity")


if __name__ == "__main__":
    f_cond_number()
    f_complexity()
