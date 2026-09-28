# -*- coding: utf-8 -*-
"""固体2級のレビュー修正で2図を再生成する。
 - mathTrapezoid : 台形公式の図が y=x^2(近似3)になっていた誤りを、問題どおり y=x^3(近似5・真値4)へ修正。
 - squarebar     : 引張問題なのに荷重矢印が内向き(圧縮)だったのを、外向き(引張)へ修正。
共通描画は figlib.py を使用。実行すると assets/figures/*.png を上書きする。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *


def fig_math_trapezoid():
    im, d = new()
    title(d, "台形公式:∫₀²x³dx を2区間で近似(=5)")
    # 座標系
    ox, oy = 95, 355          # 原点(左下)
    sx = 175                  # x1単位あたりのピクセル
    sy = 34                   # y1単位あたりのピクセル(最大 f(2)=8 → 272px)
    def X(x): return ox + x * sx
    def Y(y): return oy - y * sy
    axes(d, ox, oy, 2 * sx + 40, 8 * sy + 45, "x", "y")
    # 台形(区間[0,1]と[1,2])を淡赤で塗り、弦・鉛直線を赤で描く
    LR = (255, 235, 235)
    d.polygon([(X(0), Y(0)), (X(1), Y(0)), (X(1), Y(1)), (X(0), Y(0))], fill=LR, outline=RED, width=3)
    d.polygon([(X(1), Y(0)), (X(2), Y(0)), (X(2), Y(8)), (X(1), Y(1))], fill=LR, outline=RED, width=3)
    # 真の曲線 y=x^3(弦が上側=過大評価が見える)
    pts = [(X(2 * i / 120), Y((2 * i / 120) ** 3)) for i in range(121)]
    plot(d, 0, 0, pts, BLUE, 3)
    # 節点と高さ
    for x, fy in [(0, 0), (1, 1), (2, 8)]:
        node(d, X(x), Y(fy), 6)
    ctext(d, X(1) + 14, Y(1) - 4, "1", FT, BLACK, "lm")
    ctext(d, X(2) + 14, Y(8) + 2, "8", FT, BLACK, "lm")
    # 台形の面積ラベル
    ctext(d, X(0.5), Y(0.35), "0.5", FT, RED)
    ctext(d, X(1.5), Y(2.6), "4.5", FT, RED)
    # x軸目盛
    for x in (0, 1, 2):
        ctext(d, X(x), oy + 16, str(x), FT, BLACK)
    note(d, "面積 = (0+1)/2 + (1+8)/2 = 0.5 + 4.5 = 5   (真値4・過大評価)")
    save(im, "mathTrapezoid")


def fig_squarebar():
    im, d = new()
    title(d, "正方形断面の角棒(軸引張)")
    # 棒
    x0, x1, y0, y1 = 185, 475, 175, 245
    my = (y0 + y1) // 2
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=(235, 240, 248))
    ctext(d, (x0 + x1) / 2, my, "正方形断面 b×b", F, BLACK)
    # 引張荷重P(外向き=棒から離れる向き)
    force(d, x0, my, -72, 0, "P", BLUE)
    force(d, x1, my, 72, 0, "P", BLUE)
    # 伸び a(右向き)
    force(d, x1 + 20, y0 - 30, 48, 0, "伸び a", RED, FT)
    # 長さ L
    dim(d, x0, y1 + 40, x1, y1 + 40, "長さ L")
    save(im, "squarebar")


if __name__ == "__main__":
    fig_math_trapezoid()
    fig_squarebar()
