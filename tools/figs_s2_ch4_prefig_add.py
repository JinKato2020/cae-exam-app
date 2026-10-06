# -*- coding: utf-8 -*-
"""固体2級 第4章(有限要素法の定式化)の「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(幾何構成)のみ。
対象: 4-29(面積座標)。答え(0〜1・和が1・形状関数と一致・無次元)は一切描かない。
原本図=三角形を内部点で3つの小三角形に分割した図に対応。L=A/A の式・和=1・等値線は描かない。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


# ---- 4-29 三角形の面積座標の幾何構成(性質を問う) ----
def f_area_coord():
    im, d = new()
    title(d, "三角形要素の面積座標の幾何構成(性質を問う)")
    # 頂点(節点1=上、2=左下、3=右下)
    n1 = (330, 95)
    n2 = (150, 330)
    n3 = (510, 330)
    # 内部点P(重心を避け非対称に配置=等分を示唆しない)
    P = (300, 235)
    # 3つの小三角形を淡色で塗り分け
    d.polygon([P, n2, n3], fill=FILL1)   # 節点1に対する小三角形 A1
    d.polygon([P, n1, n3], fill=FILL2)   # 節点2に対する小三角形 A2
    d.polygon([P, n1, n2], fill=FILL3)   # 節点3に対する小三角形 A3
    # 三角形の外枠
    d.line([n1, n2, n3, n1], fill=BLACK, width=3, joint="curve")
    # 内部点Pと各頂点を結ぶ線
    for v in (n1, n2, n3):
        d.line((P[0], P[1], v[0], v[1]), fill=BLACK, width=2)
    # 節点番号
    node(d, n1[0], n1[1], 7, "white"); ctext(d, n1[0], n1[1] - 20, "1", FS, BLACK)
    node(d, n2[0], n2[1], 7, "white"); ctext(d, n2[0] - 18, n2[1] + 6, "2", FS, BLACK)
    node(d, n3[0], n3[1], 7, "white"); ctext(d, n3[0] + 18, n3[1] + 6, "3", FS, BLACK)
    # 内部点P
    node(d, P[0], P[1], 6, "white"); ctext(d, P[0] - 16, P[1] - 4, "P", FS, RED, "rm")
    # 小三角形の面積ラベル(節点に対向する小三角形)
    ctext(d, 300, 300, "A1", FT, GRAY)   # P-2-3(下)
    ctext(d, 395, 205, "A2", FT, GRAY)   # P-1-3(右)
    ctext(d, 235, 185, "A3", FT, GRAY)   # P-1-2(左)
    note(d, "点Pと3頂点を結ぶ3つの小三角形(面積A1,A2,A3)。面積座標Lの性質は?(答えは未記入)")
    save(im, "f4AreaCoordSetup")


def main():
    f_area_coord()
    print("done ch4 prefig add")


if __name__ == "__main__":
    main()
