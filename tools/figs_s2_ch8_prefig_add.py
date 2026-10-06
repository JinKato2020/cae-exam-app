# -*- coding: utf-8 -*-
"""固体2級 第8章(モデリングの基礎)の「回答前(preFigureImage)」配置図 追加分。
第1バッチ(figs_s2_ch8_prefig.py)で未対応だった、公式に配置図があり解き手が構造を
見る必要のある問題のみを追加する: 8-16(異材界面)/8-22(トラス要素)/8-23(E-B はり)/8-25(薄板引張)。
白地660x420・黒線画・与件(構造形状/荷重/座標系)のみ。答え(どのマトリックス/変位近似/大小)は描かない。
[[cae-figure-before-after-rule]] の第8章横展開(追加)。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg,
                    x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


# ---- 8-16 異材(A上/B下)弾性体の界面(応力出力の評価を問う) ----
def f_interface():
    im, d = new(); title(d, "異材(上A/下B)弾性体の界面(応力評価を問う)")
    ox, top, w = 210, 120, 240
    yI, yB = 220, 310                                   # 界面, 下端
    # 材料A(上): 上面中央に逆三角のくさび状切り込み
    nx = ox + w / 2
    polyA = [(ox, top), (nx - 42, top), (nx, top + 50), (nx + 42, top),
             (ox + w, top), (ox + w, yI), (ox, yI)]
    d.polygon(polyA, outline=BLACK, width=3, fill=FILL1)
    # 材料B(下)
    d.rectangle((ox, yI, ox + w, yB), outline=BLACK, width=3, fill=FILL2)
    # 四面体を想わせる軽いメッシュ(界面近傍)
    for xx in (ox + 60, ox + 120, ox + 180):
        d.line((xx, top if xx not in (ox + 120,) else top + 50, xx, yB), fill=LGRAY, width=1)
    for (a, b) in [((ox, top), (ox + 80, yI)), ((ox + w, top), (ox + w - 80, yI)),
                   ((ox, yI), (ox + 80, yB)), ((ox + w, yI), (ox + w - 80, yB))]:
        d.line((a[0], a[1], b[0], b[1]), fill=LGRAY, width=1)
    # 界面(強調)+共有節点
    d.line((ox, yI, ox + w, yI), fill=RED, width=4)
    ctext(d, ox + w + 12, yI, "界面", FT, RED, "lm")
    node(d, nx, yI, 7, fill="white", col=RED)
    # 上面に一様分布荷重(下向き)
    for xx in (ox + 26, ox + 64, ox + w - 64, ox + w - 26):
        arrow(d, xx, top - 44, xx, top - 6, RED, 3, 11)
    ctext(d, nx, top - 58, "一様分布荷重", FS, RED)
    # 下面 完全拘束
    hwall(d, ox - 6, ox + w + 6, yB, side=1, n=12)
    ctext(d, nx, yB + 22, "下面 完全拘束", FT, GRAY)
    ctext(d, ox - 14, top + 44, "材料A", FT, BLACK, "rm")
    ctext(d, ox - 14, (yI + yB) / 2, "材料B", FT, BLACK, "rm")
    axes(d, ox + w + 60, yB, 60, 56, "x", "y")
    note(d, "界面節点を上下要素が共有。界面の応力評価の記述で誤っているものは?(答えは未記入)")
    save(im, "model8InterfaceSetup")


# ---- 8-22 傾いた2節点トラス要素(局所剛性方程式を問う) ----
def f_trussk():
    im, d = new(); title(d, "角θ傾いた2節点トラス要素(局所剛性方程式を問う)")
    # 全体座標
    oxg, oyg = 120, 350
    axes(d, oxg, oyg, 90, 80, "x", "y")
    # 傾いたトラス(節点1->節点2)
    n1 = (190, 322); n2 = (490, 162)
    bar(d, n1[0], n1[1], n2[0], n2[1], thick=0)
    node(d, n1[0], n1[1], 8, "white"); ctext(d, n1[0] - 16, n1[1] + 10, "1", FS, BLACK, "rm")
    node(d, n2[0], n2[1], 8, "white"); ctext(d, n2[0] + 14, n2[1] - 8, "2", FS, BLACK, "lm")
    ux, uy = (n2[0] - n1[0]), (n2[1] - n1[1])
    L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    px, py = -uy, ux                                     # 画面上の垂直方向
    mx, my = (n1[0] + n2[0]) / 2, (n1[1] + n2[1]) / 2
    # 局所座標 x_bar(軸方向)・y_bar(直交)
    arrow(d, mx, my, mx + 66 * ux, my + 66 * uy, GRAY, 2, 11); ctext(d, mx + 80 * ux, my + 80 * uy, "x'(軸)", FT, GRAY, "lm")
    arrow(d, mx, my, mx + 56 * px, my + 56 * py, GRAY, 2, 11); ctext(d, mx + 70 * px, my + 70 * py, "y'", FT, GRAY)
    ctext(d, mx - 10 * ux + 18 * px, my - 10 * uy + 18 * py, "E, A, L", FT, BLUE, "lm")
    # 角θ(全体x軸と軸方向)
    th = math.degrees(math.atan2(-(n2[1] - n1[1]), n2[0] - n1[0]))
    d.line((n1[0], n1[1], n1[0] + 90, n1[1]), fill=GRAY, width=1)
    angle_arc(d, n1[0], n1[1], 50, 0, th, "θ", GRAY)
    note(d, "全体座標x,yに対し角θ傾く。局所系の剛性方程式の係数行列 k' は?(行列は未記入)")
    save(im, "model8TrussKSetup")


# ---- 8-23 細長い角柱はり(E-B はりの変位近似を問う) ----
def f_eulerbeam():
    im, d = new(); title(d, "細長い角柱はり(変位の近似を問う)")
    ox, oy, w, h, dp = 150, 250, 330, 70, 60
    iso_box(d, ox, oy, w, h, dp)
    dx = int(dp * 0.8)
    # 座標軸(左端)
    bx, by = ox - 30, oy + h
    arrow(d, bx, by, bx + 70, by, BLACK, 2, 11); ctext(d, bx + 80, by, "x", FT, BLACK, "lm")
    arrow(d, bx, by, bx, by - 70, BLACK, 2, 11); ctext(d, bx - 8, by - 82, "z", FT, BLACK, "rm")
    arrow(d, bx, by, bx + 44, by - 28, BLACK, 2, 11); ctext(d, bx + 52, by - 30, "y", FT, BLACK, "lm")
    # 寸法
    dim(d, ox, oy + h + 34, ox + w, oy + h + 34, "長さ l", 0)
    dim(d, ox + w + dx + 16, oy, ox + w + dx + 16, oy + h, "h", 0)
    ctext(d, ox + w / 2, 150, "b ≪ l,  h ≪ l", FT, GRAY)
    # y軸まわりの曲げモーメント(与件)
    cxm, cym = ox + w - 10, oy + h / 2
    d.arc((cxm - 24, cym - 34, cxm + 44, cym + 34), -70, 70, fill=RED, width=3)
    arrow(d, cxm + 30, cym - 28, cxm + 36, cym - 10, RED, 3, 10)
    ctext(d, cxm + 54, cym, "M (y軸まわり)", FT, RED, "lm")
    # 先端たわみ方向(与件: 下=z+)
    arrow(d, ox + w, oy + h + 4, ox + w, oy + h + 42, GRAY, 2, 10); ctext(d, ox + w + 6, oy + h + 42, "先端たわみ(z+)", FT, GRAY, "lm")
    note(d, "y軸まわり曲げで先端は下(z+)へたわむ。はり内部の変位u,v,wの近似は?(答えは未記入)")
    save(im, "model8EulerBeamSetup")


# ---- 8-25 薄い平板の一様引張(平面ひずみ仮定時のεxを問う) ----
def f_thinplate():
    im, d = new(); title(d, "薄い平板の一様引張(平面ひずみ仮定時のεxを問う)")
    ox, oy, w, h, dp = 210, 150, 230, 140, 28
    iso_box(d, ox, oy, w, h, dp)
    dx = int(dp * 0.8)
    # x方向一様引張 p(両側)
    for yy in (oy + 36, oy + h - 36):
        arrow(d, ox - 8, yy, ox - 58, yy, RED, 3, 11)
        arrow(d, ox + w + 8, yy, ox + w + 58, yy, RED, 3, 11)
    ctext(d, ox - 78, oy + h / 2, "一様引張 p", FT, RED, "rm")
    ctext(d, ox + w + 78, oy + h / 2, "p", FS, RED, "lm")
    # 座標軸(z=板厚方向)
    bx, by = ox + w / 2, oy + h + 70
    arrow(d, bx, by, bx + 60, by, BLACK, 2, 11); ctext(d, bx + 68, by, "x", FT, BLACK, "lm")
    arrow(d, bx, by, bx, by - 54, BLACK, 2, 11); ctext(d, bx - 8, by - 64, "y", FT, BLACK, "rm")
    arrow(d, bx, by, bx + 38, by - 24, BLACK, 2, 11); ctext(d, bx + 46, by - 26, "z(板厚)", FT, BLACK, "lm")
    note(d, "薄板をx方向へ一様引張p(zは板厚)。これを平面ひずみで解いた場合のεxは?(答えは未記入)")
    save(im, "model8ThinPlateSetup")


def main():
    f_interface(); f_trussk(); f_eulerbeam(); f_thinplate()
    print("done ch8 add 4 figures")


if __name__ == "__main__":
    main()
