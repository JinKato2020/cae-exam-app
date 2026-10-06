# -*- coding: utf-8 -*-
"""固体2級 第3章(熱伝導の基礎)の「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(形状/境界条件/熱流束の向き)のみ。
答え(温度分布の形=直線/対数/放物線、温度差の大小)は一切描かない。
対象: 3-4, 3-7, 3-8, 3-14。既存 figureImage(答え示唆あり)は回答後(helpful)のまま。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


def hatch_edge(d, x0, y0, x1, y1, side, n=10, ln=14, col=BLACK):
    """辺(x0,y0)-(x1,y1)に沿って断熱ハッチ(短い斜線)を描く。sideは法線向き(dx,dy)。"""
    sx, sy = side
    for i in range(n):
        t = (i + 0.5) / n
        px = x0 + (x1 - x0) * t
        py = y0 + (y1 - y0) * t
        d.line((px, py, px + sx * ln, py + sy * ln), fill=col, width=2)


# ---- 3-4 平板と円筒の定常温度分布(分布の形を問う) ----
def f_dist_shapes():
    im, d = new()
    title(d, "平板と円筒の定常温度分布(分布の形を問う)")
    # 左: 平板(厚さ方向)
    px0, px1, pyt, pyb = 90, 210, 130, 320
    d.rectangle((px0, pyt, px1, pyb), outline=BLACK, width=3, fill=FILL1)
    d.line((px0, pyt, px0, pyb), fill=RED, width=6)      # 左面=高温 T1
    d.line((px1, pyt, px1, pyb), fill=BLUE, width=6)     # 右面=低温 T2
    ctext(d, px0, pyt - 16, "T1(高温)", FT, RED)
    ctext(d, px1, pyt - 16, "T2(低温)", FT, BLUE)
    arrow(d, px0 + 24, 225, px1 - 20, 225, GRAY, 3, 12)  # 熱流(高温->低温)
    dim(d, px0, pyb + 34, px1, pyb + 34, "板厚 t", 0)
    ctext(d, (px0 + px1) / 2, pyb + 58, "平板(厚さ方向)", FT, BLACK)
    # 右: 円筒(半径方向)
    cx, cy, Ro, Ri = 470, 225, 100, 42
    d.ellipse((cx - Ro, cy - Ro, cx + Ro, cy + Ro), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - Ri, cy - Ri, cx + Ri, cy + Ri), outline=RED, width=4, fill="white")
    ctext(d, cx, cy, "T1", FS, RED)                      # 内面=高温
    ctext(d, cx, cy - Ro - 14, "T2(低温)", FT, BLUE)
    arrow(d, cx + Ri + 2, cy, cx + Ro - 6, cy, GRAY, 3, 12)  # 半径方向の熱流(外向き)
    dim(d, cx, cy + Ri, cx, cy + Ro, "肉厚", 0)
    ctext(d, cx, cy + Ro + 22, "円筒(内半径a・外半径b)", FT, BLACK)
    note(d, "定常・発熱なし(T1>T2)。温度分布の形は?(答えは未記入)")
    save(im, "h3ShapesSetup")


# ---- 3-7 両面温度固定・上下断熱・一様内部発熱の板(分布の形を問う) ----
def f_genheat():
    im, d = new()
    title(d, "両面温度固定・一様内部発熱の板(分布の形を問う)")
    ox, w, ty, by = 190, 280, 130, 300
    d.rectangle((ox, ty, ox + w, by), outline=BLACK, width=3, fill=FILL1)
    # 左右面=温度固定(同じ温度)
    d.line((ox, ty, ox, by), fill=RED, width=6)
    d.line((ox + w, ty, ox + w, by), fill=RED, width=6)
    ctext(d, ox - 8, (ty + by) / 2, "温度固定", FT, RED, "rm")
    ctext(d, ox + w + 8, (ty + by) / 2, "温度固定", FT, RED, "lm")
    ctext(d, ox - 8, (ty + by) / 2 + 20, "T0", FT, RED, "rm")
    ctext(d, ox + w + 8, (ty + by) / 2 + 20, "T0", FT, RED, "lm")
    # 上下面=断熱ハッチ
    hatch_edge(d, ox, ty, ox + w, ty, (0, -1))
    hatch_edge(d, ox, by, ox + w, by, (0, 1))
    ctext(d, ox + w / 2, ty - 22, "断熱", FT, GRAY)
    ctext(d, ox + w / 2, by + 24, "断熱", FT, GRAY)
    # 一様内部発熱(ラベルは上、赤点は下方の2行でラベルと重ねない)
    ctext(d, ox + w / 2, ty + 28, "一様な内部発熱", FS, RED)
    for ix in range(5):
        for iy in range(2):
            dx = ox + w * (ix + 1) / 6.0
            dy = ty + 78 + iy * 56
            d.ellipse((dx - 4, dy - 4, dx + 4, dy + 4), fill=RED, outline=RED)
    note(d, "両面を同温固定・上下断熱・一様発熱。分布の形は?(未記入)")
    save(im, "h3GenheatSetup")


# ---- 3-8 熱流束流入+一様発熱の定常壁(分布の形を問う) ----
def f_fluxgen():
    im, d = new()
    title(d, "熱流束流入＋一様発熱の定常壁(分布の形を問う)")
    ox, w, ty, by = 210, 250, 130, 300
    d.rectangle((ox, ty, ox + w, by), outline=BLACK, width=3, fill=FILL1)
    # 左=高温側: 熱流束 q 流入(外側から壁へ)
    for iy in range(4):
        yy = ty + (by - ty) * (iy + 0.5) / 4.0
        arrow(d, ox - 44, yy, ox, yy, RED, 3, 11)
    ctext(d, ox - 44, ty - 14, "熱流束 q 流入", FT, RED, "lm")
    ctext(d, ox - 50, (ty + by) / 2, "高温側", FT, BLACK, "rm")
    # 右=冷却側: 温度固定 T0
    d.line((ox + w, ty, ox + w, by), fill=BLUE, width=6)
    ctext(d, ox + w + 8, (ty + by) / 2, "冷却側", FT, BLUE, "lm")
    ctext(d, ox + w + 8, (ty + by) / 2 + 20, "T0 固定", FT, BLUE, "lm")
    # 一様内部発熱(ラベルは上、赤点は下方の2行でラベルと重ねない)
    ctext(d, ox + w / 2, ty + 28, "一様な内部発熱", FS, RED)
    for ix in range(4):
        for iy in range(2):
            dx = ox + w * (ix + 1) / 5.0
            dy = ty + 78 + iy * 56
            d.ellipse((dx - 4, dy - 4, dx + 4, dy + 4), fill=RED, outline=RED)
    note(d, "高温側から熱流束流入+一様発熱・冷却側T0。形は?(未記入)")
    save(im, "h3FluxGenSetup")


# ---- 3-14 両側流体・同一熱流束の平板(表面温度差の大小を問う) ----
def f_deltat():
    im, d = new()
    title(d, "両側流体に接する平板(表面温度差の大小を問う)")
    # 流体1(左)・平板(中)・流体2(右)
    d.rectangle((70, 120, 290, 320), outline=LGRAY, width=1, fill=(228, 238, 252))
    d.rectangle((370, 120, 590, 320), outline=LGRAY, width=1, fill=(252, 236, 230))
    d.rectangle((290, 120, 370, 320), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 330, 112, "平板", FT, BLACK)
    # 流体ラベル(熱伝達率 h1>h2 は与件)
    ctext(d, 180, 152, "流体1", FS, BLUE)
    ctext(d, 180, 178, "熱伝達率 h1(大)", FT, BLUE)
    ctext(d, 480, 152, "流体2", FS, ORANGE)
    ctext(d, 480, 178, "熱伝達率 h2(小)", FT, ORANGE)
    # 同じ熱流束 q が板を貫く(左->右)
    arrow(d, 120, 260, 540, 260, RED, 4, 14)
    ctext(d, 330, 240, "同じ熱流束 q", FT, RED)
    note(d, "両側流体・同じ熱流束q・h1>h2。温度差の大小は?(未記入)")
    save(im, "h3DeltatSetup")


# ---- 3-16 二次元熱伝導の断熱境界(x に垂直な面)の条件(与件のみ) ----
def f_adiabatic():
    im, d = new()
    title(d, "二次元熱伝導の断熱境界(x に垂直な面)")
    # 解析領域
    ox, w, ty, by = 250, 300, 120, 330
    d.rectangle((ox, ty, ox + w, by), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + w / 2, (ty + by) / 2, "解析領域", FS, GRAY)
    # 左面=断熱面(y に平行・x に垂直)。緑太線＋断熱ハッチ(外向き=左)
    d.line((ox, ty, ox, by), fill=GREEN, width=6)
    hatch_edge(d, ox, ty, ox, by, (-1, 0))
    ctext(d, ox, ty - 18, "断熱面(y に平行)", FT, GREEN)
    # 座標軸(向きの明示: x は水平=面に垂直, y は鉛直=面に平行)
    axx, axy = 120, 350
    arrow(d, axx, axy, axx + 64, axy, BLACK, 3, 12)   # x 軸(右向き)
    ctext(d, axx + 74, axy, "x", FT, BLACK, "lm")
    arrow(d, axx, axy, axx, axy - 64, BLACK, 3, 12)   # y 軸(上向き)
    ctext(d, axx, axy - 80, "y", FT, BLACK)
    note(d, "x に垂直(y に平行)な面が断熱境界。この面上で成り立つことは?(未記入)")
    save(im, "h3AdiabaticSetup")


def main():
    f_dist_shapes()
    f_genheat()
    f_fluxgen()
    f_deltat()
    f_adiabatic()
    print("done ch3 prefig add")


if __name__ == "__main__":
    main()
