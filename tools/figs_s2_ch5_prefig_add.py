# -*- coding: utf-8 -*-
"""固体2級 第5章(有限要素法の実践)の追加「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(ばね系の形状/固定/強制変位/ばね定数)のみ。
答え(各節点変位 u2,u3 の解)は一切描かない。既存 figureImage は回答後(helpful)のまま。
[[cae-figure-before-after-rule]] の第5章横展開(fem-5-19 直列3ばね)。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


# ---- 5-19 直列3ばね(節点1固定・節点4に強制変位。各節点変位を問う) ----
def f5SeriesSpringsSetup():
    im, d = new()
    title(d, "直列3ばね(節点1固定・節点4に強制変位。各節点変位を問う)")
    y = 210
    wx = 86                                   # 壁の位置
    wall(d, wx, y - 54, y + 54, side=1)       # 左端固定壁(右にハッチ)
    ctext(d, wx - 6, y + 78, "固定 (u1=0)", FT, GRAY, "mm")
    nx = [126, 272, 418, 564]                 # 節点1〜4のx座標
    # 壁→節点1 の剛結(固定を表す短い直線)
    d.line((wx, y, nx[0], y), fill=BLACK, width=4)
    # 3本のばね(節点間)
    klab = ["k1 = 100", "k2 = 200", "k3 = 200"]
    for i in range(3):
        spring(d, nx[i], y, nx[i + 1], y)
        cx = (nx[i] + nx[i + 1]) / 2
        ctext(d, cx, y - 44, klab[i], FS, BLUE)
    # 節点(白丸)+ 節点番号
    for i, x in enumerate(nx):
        node(d, x, y, 8, "white")
        ctext(d, x, y + 28, str(i + 1), FS, BLACK)
    ctext(d, nx[0], y + 52, "(固定)", FT, GRAY)
    # 節点4に強制変位 u4=6mm(右向き)。解いた u2,u3 は描かない
    ax0 = nx[3] + 14
    arrow(d, ax0, y, ax0 + 56, y, RED, 4, 15)
    ctext(d, ax0 + 30, y - 22, "u4 = 6 mm", FS, RED)
    ctext(d, nx[3], y + 28, "4", FS, BLACK)   # 念のため番号(上書き済だが保険)
    note(d, "節点1固定・節点4にu4=6mmを強制。各節点変位は?(答えは未記入)")
    save(im, "f5SeriesSpringsSetup")


def main():
    f5SeriesSpringsSetup()
    print("done 1 figure")


if __name__ == "__main__":
    main()
