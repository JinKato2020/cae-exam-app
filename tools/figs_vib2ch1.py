# -*- coding: utf-8 -*-
"""振動2級 第1章 計算力学のための数学の基礎 の図。
問題図=接頭辞 v2e1（1-6 座標回転 / 1-8 複素平面）、公式図=接頭辞 v2f1（同題）。
白地660×420・機構だけ描く線画（figlib準拠）。実行: python tools/figs_vib2ch1.py
"""
import math
from figlib import new, save, title, ctext, arrow, angle_arc, node, F, FS, FT, BLACK, GRAY, BLUE, RED, LGRAY


def _dash_line(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8):
    n = max(1, int(math.hypot(x2 - x1, y2 - y1) / dash))
    for k in range(n):
        if k % 2:
            continue
        t0, t1 = k / n, (k + 1) / n
        d.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=col, width=wd)


def coord_rotation(name):
    """xy座標系を角θだけ回転した x'y' 座標系。点Pの成分が座標系で変わることを示す。"""
    im, d = new()
    title(d, "座標系のθ回転（xy → x'y'）")
    ox, oy = 300, 250          # 原点
    L = 165
    # 元の座標軸 x(右), y(上)
    arrow(d, ox, oy, ox + L, oy, BLACK, 2, 11); ctext(d, ox + L + 12, oy, "x", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - L, BLACK, 2, 11); ctext(d, ox - 12, oy - L - 4, "y", FS, BLACK, "rm")
    # 回転後の座標軸 x'(θ), y'(θ+90)  θ=30°(反時計回り)
    th = math.radians(30)
    x1 = (ox + L * math.cos(th), oy - L * math.sin(th))
    y1 = (ox + L * math.cos(th + math.pi / 2), oy - L * math.sin(th + math.pi / 2))
    arrow(d, ox, oy, x1[0], x1[1], BLUE, 3, 12); ctext(d, x1[0] + 12, x1[1] - 4, "x'", FS, BLUE, "lm")
    arrow(d, ox, oy, y1[0], y1[1], BLUE, 3, 12); ctext(d, y1[0] - 12, y1[1] - 6, "y'", FS, BLUE, "rm")
    # 角θ
    angle_arc(d, ox, oy, 52, 0, 30, "θ", GRAY)
    # 点P と 両座標系での成分（破線）
    P = (ox + 128, oy - 96)
    node(d, P[0], P[1], 6, "white", RED); ctext(d, P[0] + 14, P[1] - 10, "P", FS, RED, "lm")
    _dash_line(d, P[0], P[1], P[0], oy, GRAY); _dash_line(d, P[0], P[1], ox, P[1], GRAY)
    ctext(d, (ox + P[0]) / 2, oy + 16, "x成分", FT, GRAY)
    ctext(d, ox - 30, (oy + P[1]) / 2, "y成分", FT, GRAY)
    ctext(d, 330, 392, "同じ点Pでも座標系を回すと成分(x,y)と(x',y')が変わる", FT, GRAY)
    save(im, name)


def complex_plane(name):
    """複素平面上の Z=A+iB。実部A・虚部B・大きさX=√(A²+B²)・偏角θ。"""
    im, d = new()
    title(d, "複素数 Z = A + iB（複素平面）")
    ox, oy = 250, 270          # 原点
    Lx, Ly = 300, 190
    # 実軸(Re)・虚軸(Im)
    arrow(d, ox, oy, ox + Lx, oy, BLACK, 2, 11); ctext(d, ox + Lx + 14, oy, "Re", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - Ly, BLACK, 2, 11); ctext(d, ox - 14, oy - Ly - 2, "Im", FS, BLACK, "rm")
    # 点Z
    A, B = 240, 150            # ピクセル上の A,B
    Z = (ox + A, oy - B)
    arrow(d, ox, oy, Z[0], Z[1], BLUE, 3, 13)
    node(d, Z[0], Z[1], 6, "white", RED)
    ctext(d, Z[0] + 16, Z[1] - 12, "Z = A + iB", FS, RED, "lm")
    # A(実部)・B(虚部) の破線
    _dash_line(d, Z[0], Z[1], Z[0], oy, GRAY); _dash_line(d, Z[0], Z[1], ox, Z[1], GRAY)
    ctext(d, (ox + Z[0]) / 2, oy + 16, "A（実部）", FT, GRAY)
    ctext(d, ox - 40, (oy + Z[1]) / 2, "B（虚部）", FT, GRAY)
    # 大きさ X と 偏角θ
    ctext(d, (ox + Z[0]) / 2 - 10, (oy + Z[1]) / 2 - 14, "X=√(A²+B²)", FT, BLUE)
    thdeg = math.degrees(math.atan2(B, A))
    angle_arc(d, ox, oy, 60, 0, thdeg, "θ", GRAY)
    ctext(d, 330, 398, "X=√(A²+B²), θ=tan⁻¹(B/A)（極形式 Z=X e^{iθ}）", FT, GRAY)
    save(im, name)


if __name__ == "__main__":
    coord_rotation("v2e1CoordRotation")
    complex_plane("v2e1ComplexPlane")
    coord_rotation("v2f1CoordRotation")
    complex_plane("v2f1ComplexPlane")
    print("done")
