# -*- coding: utf-8 -*-
"""固体2級 レビュー修正(第7・9章の図)。figlib.py で再生成。
 elem7DetJ         : 幅8・高さ6・面積48・det J=48/4=12(誤:幅6高さ3・det J=4.5)
 bc9ThickCylQuarter: ラベルの重なりを解消し、2次要素辺の配分(隅1/6・中間2/3・
                     共有隅1/3)と F0=240N の各節点力を読みやすく再構成。
実行すると assets/figures/*.png を上書きする。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *


def fig_elem7_detj():
    im, d = new()
    title(d, "ヤコビ行列式 det J = 実面積 / 局所面積")
    # 左:局所座標の正方形(2×2=4)
    lx0, ly0, s = 95, 195, 105
    d.rectangle((lx0, ly0, lx0 + s, ly0 + s), outline=BLACK, width=3, fill=FILL1)
    cx, cy = lx0 + s / 2, ly0 + s / 2
    arrow(d, cx, cy, cx + 52, cy, BLACK, 2, 10); ctext(d, cx + 60, cy, "ξ", FS, BLACK, "lm")
    arrow(d, cx, cy, cx, cy - 52, BLACK, 2, 10); ctext(d, cx, cy - 62, "η", FS, BLACK)
    ctext(d, cx, ly0 + s + 18, "局所座標 −1≤ξ,η≤1", FT, BLACK)
    ctext(d, cx, ly0 + s + 40, "面積 = 2×2 = 4", FS, BLUE)
    # 写像
    arrow(d, 225, cy, 340, cy, BLACK, 3, 14)
    ctext(d, 282, cy - 18, "写像 J", FS, BLACK)
    # 右:実要素(8×6=48)
    rx0, ry0, rw, rh = 365, 160, 240, 180
    d.rectangle((rx0, ry0, rx0 + rw, ry0 + rh), outline=BLACK, width=3, fill=FILL1)
    ctext(d, rx0 + rw / 2, ry0 - 16, "面積 = 8×6 = 48", FS, GREEN)
    dim(d, rx0, ry0 + rh + 22, rx0 + rw, ry0 + rh + 22, "x方向 = 8")
    dim(d, rx0 + rw + 24, ry0, rx0 + rw + 24, ry0 + rh, "y = 6")
    ctext(d, 330, 390, "det J = 48 / 4 = 12", FL, RED)
    save(im, "elem7DetJ")


def _bracket(d, x1, x2, y, label):
    d.line((x1, y, x2, y), fill=GRAY, width=2)
    d.line((x1, y - 6, x1, y), fill=GRAY, width=2)
    d.line((x2, y - 6, x2, y), fill=GRAY, width=2)
    ctext(d, (x1 + x2) / 2, y + 14, label, FT, GRAY)


def fig_bc9_thick_cyl_quarter():
    im, d = new()
    title(d, "厚肉円筒1/4モデル 内圧の等価節点力")
    # 右上:1/4モデルの文脈(内圧pが内面を外向きに押す)
    ccx, ccy, ri, ro = 505, 150, 46, 104
    d.arc((ccx - ri, ccy - ri, ccx + ri, ccy + ri), -90, 0, fill=BLACK, width=2)
    d.arc((ccx - ro, ccy - ro, ccx + ro, ccy + ro), -90, 0, fill=BLACK, width=2)
    d.line((ccx, ccy - ri, ccx, ccy - ro), fill=BLACK, width=2)
    d.line((ccx + ri, ccy, ccx + ro, ccy), fill=BLACK, width=2)
    for a in (-72, -45, -18):
        r = math.radians(a); c, s = math.cos(r), math.sin(r)
        arrow(d, ccx + ri * c, ccy + ri * s, ccx + (ri + 17) * c, ccy + (ri + 17) * s, RED, 2, 8)
    ctext(d, ccx + 6, ccy - 6, "内圧p", FT, RED, "lm")
    ctext(d, ccx, ccy + 20, "1/4モデル", FT, GRAY)
    # 主図:内面の2次要素(3節点)辺2つ=5節点の配分
    xs = [95, 175, 255, 335, 415]
    y = 250
    fr = ["1/6", "2/3", "1/3", "2/3", "1/6"]
    fn = ["40N", "160N", "80N", "160N", "40N"]
    frac = [1 / 6, 2 / 3, 1 / 3, 2 / 3, 1 / 6]
    d.line((xs[0], y, xs[-1], y), fill=BLACK, width=3)
    for i, x in enumerate(xs):
        node(d, x, y, 6)
        col = RED if i == 2 else BLACK
        arrow(d, x, y, x, y + int(frac[i] * 82) + 8, RED if i == 2 else (200, 90, 90), 3, 11)
        ctext(d, x, y - 34, fr[i], FS, GREEN if i != 2 else RED)
        ctext(d, x, y - 14, fn[i], FT, col)
    ctext(d, xs[2], y - 52, "共有隅", FT, RED)
    _bracket(d, xs[0], xs[2], y + 78, "要素A")
    _bracket(d, xs[2], xs[4], y + 78, "要素B")
    note(d, "隅1/6・中間2/3。共有隅=2要素ぶん=1/3。 F0=240N → 隅40 / 中間160 / 共有隅80 N")
    save(im, "bc9ThickCylQuarter")


if __name__ == "__main__":
    fig_elem7_detj()
    fig_bc9_thick_cyl_quarter()
