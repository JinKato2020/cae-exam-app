# -*- coding: utf-8 -*-
"""熱流体力学1級 第22章 追加図 t1e22PdfTheta を描画。
温度の離散確率分布(棒グラフ)。横軸=theta(K), 縦軸=確率 P。
白地660x420・黒線画・既存ch22スタイルに合わせる。平均値は書かない。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# t1e22PdfTheta : 温度の離散確率分布(300K/1200K/2000K = 0.4/0.2/0.4)
def pdf_theta():
    im, d = new(); title(d, "温度の離散確率分布")
    ox, oy, xl, yl = 120, 345, 440, 250
    # 軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "theta (K)", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "確率 P", FS, BLACK, "rm")

    def Y(p): return oy - (p / 0.5) * yl
    # 縦軸目盛 0..0.5
    for p in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        d.line((ox - 5, Y(p), ox, Y(p)), fill=GRAY, width=1)
        ctext(d, ox - 12, Y(p), "%.1f" % p, FT, GRAY, "rm")
    # 離散確率の棒
    bars = [(300, 0.4), (1200, 0.2), (2000, 0.4)]
    xs = [ox + xl * 0.22, ox + xl * 0.5, ox + xl * 0.78]
    bw = 70
    for cx, (temp, p) in zip(xs, bars):
        top = Y(p)
        d.rectangle((cx - bw / 2, top, cx + bw / 2, oy), outline=BLACK, width=2, fill=(232, 240, 250))
        ctext(d, cx, top - 14, "%.1f" % p, FT, BLUE)
        ctext(d, cx, oy + 18, "%d K" % temp, FT, BLACK)
    note(d, "3つの温度に与えた離散確率(縦軸=確率P). 合計は1")
    save(im, "t1e22PdfTheta")


if __name__ == "__main__":
    pdf_theta()
    print("done t1e22PdfTheta")
