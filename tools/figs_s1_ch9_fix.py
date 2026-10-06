# -*- coding: utf-8 -*-
"""固体1級 第9章 レビュー修正の図(回答後 helpful)を再生成。生成元が消失していた図。
- s1e9Complexity(9-15): 直接法 O(n^3) に整合する右上がりの曲線(旧図は途中で水平になり式と矛盾)。
  O(n^3)は密行列消去の概算である旨も添える。
※ 旧 s1e9IterMatrix(9-3) は s1e9CondNumber(figs_s1_figfix5.py)へ差し替え・生成停止。"""
import sys
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


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
    f_complexity()
