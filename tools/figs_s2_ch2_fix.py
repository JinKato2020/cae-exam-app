# -*- coding: utf-8 -*-
"""固体2級 第2章の公式用語カード用の図の修正（generator消失のため新規）。
s2StressStrainCurve = 公称応力-ひずみ線図（一様伸び・破断伸びを軸に明示）。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def _dash(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=8, gp=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dl, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dl + gp


def s2StressStrainCurve():
    im, d = new(); title(d, "公称応力-ひずみ線図の各部")
    ox, oy = 95, 330
    arrow(d, ox, oy, 610, oy, BLACK, 2, 11); ctext(d, 616, oy, "ひずみ", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, 70, BLACK, 2, 11); ctext(d, ox - 8, 60, "応力 σ", FS, BLACK, "rm")
    yld = (235, 178)     # A 降伏点
    peak = (390, 108)    # B 引張強さ(最大)
    brk = (480, 180)     # 破断点
    # 弾性直線 O→降伏点（傾き=E）
    d.line((ox, oy, yld[0], yld[1]), fill=BLUE, width=3)
    ctext(d, 150, 262, "傾き = E", FT, GRAY)
    # 降伏点→引張強さ（加工硬化・上に凸）
    hard = [yld, (285, 150), (335, 124), peak]
    d.line(hard, fill=BLUE, width=3, joint="curve")
    # 引張強さ→破断（くびれ・荷重低下）
    neck = [peak, (437, 138), brk]
    d.line(neck, fill=BLUE, width=3, joint="curve")
    # 点マーク
    node(d, yld[0], yld[1], 5, fill=BLACK); ctext(d, yld[0] - 8, yld[1] - 16, "A 降伏点", FT, RED, "rm")
    node(d, peak[0], peak[1], 5, fill=BLACK); ctext(d, peak[0], peak[1] - 16, "B 引張強さ(最大)", FT, RED)
    ctext(d, brk[0] + 8, brk[1] - 2, "× 破断", FS, RED, "lm")
    d.line((brk[0] - 7, brk[1] - 7, brk[0] + 7, brk[1] + 7), fill=RED, width=3)
    d.line((brk[0] - 7, brk[1] + 7, brk[0] + 7, brk[1] - 7), fill=RED, width=3)
    # 一様伸び C（引張強さ点のひずみ）と 破断伸び D（破断点のひずみ）を軸に明示
    _dash(d, peak[0], peak[1], peak[0], oy, GRAY)
    node(d, peak[0], oy, 4, fill=GREEN, col=GREEN)
    ctext(d, peak[0], oy + 18, "C 一様伸び", FT, GREEN)
    _dash(d, brk[0], brk[1], brk[0], oy, GRAY)
    node(d, brk[0], oy, 4, fill=ORANGE, col=ORANGE)
    ctext(d, brk[0] + 20, oy + 40, "D 破断伸び", FT, ORANGE)
    _dash(d, brk[0], oy + 34, brk[0], oy + 6, ORANGE, 2, 5, 4)
    note(d, "A降伏点→加工硬化→B引張強さ→くびれ→破断。C=一様伸び(B点)/D=破断伸び")
    save(im, "s2StressStrainCurve")


if __name__ == "__main__":
    s2StressStrainCurve()
    print("done s2 ch2 figures")
