# -*- coding: utf-8 -*-
"""固体2級 5-11(均等分布力=圧力の与え方)の図を作成。
公式問5-11は「一様分布圧力を要素の辺/面の法線方向に等価節点力へ換算して与える」概念問題。
- f5PressureSetup   : 回答前(一様圧力の設定のみ・答え=方法は示さない)
- f5Pressure2Nodal  : 回答後(法線方向の等価節点力へ換算、2節点直線辺では両節点に等分 pL/2)
白地660x420。"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

N1 = (160, 250); N2 = (500, 250); TOP = 195  # 一様圧力の上端(高さ一定)


def draw_edge_and_pressure(d):
    # 一様分布圧力(高さ一定の長方形プロファイル・法線=下向き)
    d.rectangle((N1[0], TOP, N2[0], N1[1]), outline=BLUE, width=2, fill=(232, 238, 255))
    nseg = 7
    for i in range(nseg + 1):
        x = N1[0] + (N2[0] - N1[0]) * i / nseg
        arrow(d, x, TOP + 3, x, N1[1] - 2, BLUE, 2, 8)
    # 要素の辺と2節点
    d.line((N1[0], N1[1], N2[0], N2[1]), fill=BLACK, width=5)
    node(d, N1[0], N1[1], 8); node(d, N2[0], N2[1], 8)
    ctext(d, N1[0] - 6, N1[1] + 20, "節点1", FT, BLACK, "mm")
    ctext(d, N2[0] + 6, N2[1] + 20, "節点2", FT, BLACK, "mm")
    ctext(d, (N1[0] + N2[0]) // 2, TOP - 16, "一様分布圧力 p（辺に垂直＝法線方向）", FT, BLUE)


# ===== 回答前: 設定のみ（方法＝答えは示さない）=====
im, d = new()
title(d, "要素の辺に作用する一様分布圧力（節点へどう与える？）")
draw_edge_and_pressure(d)
dim(d, N1[0], N1[1] + 52, N2[0], N1[1] + 52, "辺の長さ L")
ctext(d, (N1[0] + N2[0]) // 2, N1[1] + 92, "p は辺全体で一定", FT, GRAY)
note(d, "この一様圧力を節点に与える正しい方法は？（圧力[Pa]は節点にそのまま入れられない）")
save(im, "f5PressureSetup")

# ===== 回答後: 法線方向の等価節点力へ換算、両節点に等分 =====
im, d = new()
title(d, "一様圧力 → 等価節点力（法線方向・両節点に等分）")
draw_edge_and_pressure(d)
# 等価節点力（両節点で等しい＝等分）
for nx in (N1[0], N2[0]):
    arrow(d, nx, N1[1] + 12, nx, N1[1] + 66, RED, 4, 13)
ctext(d, N1[0], N1[1] + 84, "pL/2", FS, RED)
ctext(d, N2[0], N1[1] + 84, "pL/2", FS, RED)
ctext(d, (N1[0] + N2[0]) // 2, 128, "{f} = ∫ N^T p dS （仮想仕事）", FT, GRAY)
note(d, "一様圧力は法線方向の等価節点力に換算。2節点直線辺では両節点に等分(各 pL/2)。")
save(im, "f5Pressure2Nodal")
