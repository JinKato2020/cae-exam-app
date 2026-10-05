# -*- coding: utf-8 -*-
"""固体2級 第4〜7章 回答前図(preFigureImage)=中立設定図 9枚。
原本どおり図依存へ戻す10問のうち、5-20(既存f5BarSeries2Elを流用)を除く9問の設定図。
所与データ(寸法/荷重/材料値/配置)のみを描き、答え・結論・導出は一切描かない。
白地660x420・黒線画で統一。JSONは編集しない。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=11):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg))
    for i in range(n):
        if i % 2:
            continue
        a, b = i / n, (i + 1) / n
        d.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=col, width=wd)


# ---- 4-23 斜めばね要素の設定 (f4InclinedSpringSetup) ----
def f4InclinedSpringSetup():
    im, d = new(); title(d, "斜めばね要素と全体座標の傾き")
    ox, oy = 180, 330
    axes(d, ox, oy, 330, 230, "x", "y")
    th = math.radians(60); L = 215
    ex, ey = ox + L * math.cos(th), oy - L * math.sin(th)
    spring(d, ox, oy, ex, ey, coils=6, amp=14)
    node(d, ox, oy, 6, fill="white"); node(d, ex, ey, 6, fill="white")
    angle_arc(d, ox, oy, 54, 0, 60, "θ=60°", BLACK)
    ctext(d, (ox + ex) / 2 + 26, (oy + ey) / 2 - 6, "k=120 N/mm", FS, BLUE, "lm")
    note(d, "ばね定数 k と傾き角 θ は図のとおり。全体剛性の x-y 連成成分 k_xy を求める")
    save(im, "f4InclinedSpringSetup")


# ---- 4-26 3要素直列のアセンブリ設定 (femAssemblySetup) ----
def femAssemblySetup():
    im, d = new(); title(d, "3要素直列系のアセンブリ")
    y = 220; xs = [120, 270, 420, 560]
    labels = [("A", "k=150"), ("B", "k=250"), ("C", "k=100")]
    for i in range(3):
        spring(d, xs[i], y, xs[i + 1], y, coils=5, amp=12)
        mx = (xs[i] + xs[i + 1]) / 2
        ctext(d, mx, y - 40, labels[i][0], FS, BLACK)
        ctext(d, mx, y - 20, labels[i][1], FT, BLUE)
    for i, x in enumerate(xs):
        node(d, x, y, 8, fill="white")
        ctext(d, x, y + 26, str(i + 1), FS, BLACK)
    # 節点3を対象として丸で指示(値は書かない)
    d.ellipse((xs[2] - 20, y - 20, xs[2] + 20, y + 20), outline=RED, width=3)
    ctext(d, xs[2], y + 50, "求める成分=節点3", FT, RED)
    note(d, "各ばね定数は図のとおり。全体剛性マトリックスの (3,3) 成分を求める")
    save(im, "femAssemblySetup")


# ---- 5-28 初期ひずみ法の設定 (f5ResidualStrainSetup) ----
def f5ResidualStrainSetup():
    im, d = new(); title(d, "引張状態で接着した部材(初期ひずみ法)")
    x0, x1 = 200, 470
    # 部材A(上):引張状態
    ay0, ay1 = 150, 200
    d.rectangle((x0, ay0, x1, ay1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + x1) / 2, (ay0 + ay1) / 2, "部材A", FS, BLACK)
    arrow(d, x0 - 10, (ay0 + ay1) / 2, x0 - 54, (ay0 + ay1) / 2, RED, 3, 12)
    arrow(d, x1 + 10, (ay0 + ay1) / 2, x1 + 54, (ay0 + ay1) / 2, RED, 3, 12)
    ctext(d, x1 + 60, (ay0 + ay1) / 2, "σ=200MPa", FS, RED, "lm")
    ctext(d, x0 - 60, (ay0 + ay1) / 2, "σ", FS, RED, "rm")
    # 部材B(下):接着
    by0, by1 = 205, 255
    d.rectangle((x0, by0, x1, by1), outline=BLACK, width=3, fill=FILL2)
    ctext(d, (x0 + x1) / 2, (by0 + by1) / 2, "部材B", FS, BLACK)
    ctext(d, (x0 + x1) / 2, by1 + 26, "引張状態のAにBを接着 → その後に除荷", FT, GRAY)
    ctext(d, x0, ay0 - 24, "E_A=200GPa, ν_A=0.3", FT, BLUE, "lm")
    note(d, "部材Aの材料定数と引張応力は図のとおり。Aに与える初期ひずみとして正しいものは?")
    save(im, "f5ResidualStrainSetup")


# ---- 7-7 二次三角形要素の辺の温度 (elem7QuadTempEdgeSetup) ----
def elem7QuadTempEdgeSetup():
    im, d = new(); title(d, "二次三角形要素の辺の温度")
    V1 = (200, 330); V2 = (470, 330); V3 = (335, 150)
    d.line((V1[0], V1[1], V2[0], V2[1]), fill=BLACK, width=3)
    d.line((V2[0], V2[1], V3[0], V3[1]), fill=BLACK, width=3)
    d.line((V3[0], V3[1], V1[0], V1[1]), fill=BLACK, width=3)
    mids = [((V1[0] + V2[0]) / 2, (V1[1] + V2[1]) / 2),
            ((V2[0] + V3[0]) / 2, (V2[1] + V3[1]) / 2),
            ((V3[0] + V1[0]) / 2, (V3[1] + V1[1]) / 2)]
    for p in (V1, V2, V3, *mids):
        node(d, p[0], p[1], 6, fill="white")
    # 下辺 V1-M12-V2 に温度ラベル
    ctext(d, V1[0] - 6, V1[1] + 22, "60℃", FS, RED, "mm")
    ctext(d, mids[0][0], mids[0][1] + 22, "40℃", FS, RED, "mm")
    ctext(d, V2[0] + 6, V2[1] + 22, "40℃", FS, RED, "mm")
    ctext(d, V1[0] - 20, V1[1] - 4, "隅", FT, GRAY, "rm")
    ctext(d, mids[0][0], mids[0][1] - 16, "中間", FT, GRAY)
    note(d, "辺の3節点の温度は図のとおり。この辺に沿う温度分布として適切なものは?")
    save(im, "elem7QuadTempEdgeSetup")


# ---- 7-15 片持ち板(面内荷重)の設定 (elem7CantPlateSetup) ----
def elem7CantPlateSetup():
    im, d = new(); title(d, "片持ち板の面内荷重と寸法")
    x0, x1, yt, yb = 190, 490, 170, 250
    wall(d, x0, yt - 8, yb + 8, side=-1)
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    # 自由端に面内荷重W(下向き)
    arrow(d, x1, (yt + yb) / 2, x1, (yt + yb) / 2 + 60, RED, 4, 14)
    ctext(d, x1 + 16, (yt + yb) / 2 + 40, "W=10N", FS, RED, "lm")
    # 寸法
    dim(d, x0, yb + 34, x1, yb + 34, "L=150mm", 0)
    dim(d, x0 - 54, yt, x0 - 54, yb, "h=20mm", 0)
    ctext(d, (x0 + x1) / 2, yt - 18, "板厚 b=1mm, E=2×10⁵ N/mm²", FT, BLUE)
    note(d, "寸法・面内荷重・E は図のとおり。断面二次モーメントと理論たわみ・分割方針の組合せは?")
    save(im, "elem7CantPlateSetup")


# ---- 7-16 要素種類と曲げ精度の設定 (elem7ElemBendRankSetup) ----
def elem7ElemBendRankSetup():
    im, d = new(); title(d, "3種の要素で解く片持ばりの曲げ")
    # 上:片持ばり+先端荷重
    wx = 120; yb = 150
    wall(d, wx, yb - 26, yb + 26, side=-1)
    d.rectangle((wx, yb - 22, wx + 250, yb + 22), outline=BLACK, width=3, fill=FILL1)
    ax = wx + 250
    arrow(d, ax, yb, ax, yb + 54, RED, 4, 14); ctext(d, ax + 16, yb + 36, "荷重", FT, RED, "lm")
    ctext(d, ax, yb - 34, "A(先端)", FT, GRAY)
    ctext(d, wx + 300, yb, "理論たわみ 0.80mm", FT, BLUE, "lm")
    # 下:3要素タイプの候補(中立に併記・序列は描かない)
    cy = 300; bx = [150, 340, 520]
    # 三角形
    d.polygon([(bx[0] - 34, cy + 26), (bx[0] + 34, cy + 26), (bx[0], cy - 26)], outline=BLACK, width=3, fill=FILL1)
    ctext(d, bx[0], cy + 50, "三角形(定ひずみ)", FT, BLACK)
    # iso4
    d.rectangle((bx[1] - 32, cy - 26, bx[1] + 32, cy + 26), outline=BLACK, width=3, fill=FILL1)
    for p in [(bx[1] - 32, cy - 26), (bx[1] + 32, cy - 26), (bx[1] - 32, cy + 26), (bx[1] + 32, cy + 26)]:
        node(d, p[0], p[1], 4, fill="white")
    ctext(d, bx[1], cy + 50, "iso 4節点", FT, BLACK)
    # iso8
    d.rectangle((bx[2] - 32, cy - 26, bx[2] + 32, cy + 26), outline=BLACK, width=3, fill=FILL1)
    for p in [(bx[2] - 32, cy - 26), (bx[2] + 32, cy - 26), (bx[2] - 32, cy + 26), (bx[2] + 32, cy + 26),
              (bx[2], cy - 26), (bx[2], cy + 26), (bx[2] - 32, cy), (bx[2] + 32, cy)]:
        node(d, p[0], p[1], 4, fill="white")
    ctext(d, bx[2], cy + 50, "iso 8節点", FT, BLACK)
    note(d, "この3種で解析。各モデルの たわみ比と、比0.25のモデルの計算たわみの組合せは?")
    save(im, "elem7ElemBendRankSetup")


# ---- 7-17 正方形要素のヤコビアン設定 (elem7SquareDetJSetup) ----
def elem7SquareDetJSetup():
    im, d = new(); title(d, "片持ばりの分割とヤコビアン")
    # (A) 一様正方形メッシュ
    ax0, ay0 = 70, 120; a = 28
    ctext(d, ax0 + 2 * a, ay0 - 16, "分割(A) 一辺 a=5mm 正方形", FT, BLACK)
    for i in range(5):
        for j in range(2):
            d.rectangle((ax0 + i * a, ay0 + j * a, ax0 + (i + 1) * a, ay0 + (j + 1) * a), outline=BLACK, width=2, fill=FILL1)
    dim(d, ax0, ay0 + 2 * a + 20, ax0 + a, ay0 + 2 * a + 20, "a", 0)
    # (B) 扁平要素
    bx0, by0 = 70, 250; bw = 46; bh = 18
    ctext(d, bx0 + 2 * bw, by0 - 16, "分割(B) 扁平要素", FT, BLACK)
    for i in range(3):
        d.rectangle((bx0 + i * bw, by0, bx0 + (i + 1) * bw, by0 + bh), outline=BLACK, width=2, fill=FILL2)
    # 親要素(局所座標)
    px, py, pr = 520, 230, 60
    d.rectangle((px - pr, py - pr, px + pr, py + pr), outline=BLACK, width=3, fill=FILL1)
    axes(d, px, py, pr + 28, pr + 28, "ξ", "η")
    ctext(d, px + pr, py + 18, "+1", FT, GRAY); ctext(d, px - pr, py + 18, "−1", FT, GRAY)
    ctext(d, px, py - pr - 48, "親要素 −1≤ξ,η≤1", FT, BLACK)
    note(d, "(A)は一様正方形, (B)は扁平。(A)1要素のヤコビ行列式 detJ と要素剛性について適切なものは?")
    save(im, "elem7SquareDetJSetup")


# ---- 7-8 円弧境界と8節点要素(新規) (elem7CurvedIsoSetup) ----
def elem7CurvedIsoSetup():
    im, d = new(); title(d, "円弧境界を8節点要素で表す")
    # 図A:中間節点を円弧上に配置 / 図B:中間節点を弦の中点に配置
    def panel(cx, label, mid_on_arc):
        # 下辺を円弧とする四辺形要素(上辺直線)
        lx, rx = cx - 70, cx + 70; ty, by = 150, 250
        # 隅節点
        corners = [(lx, ty), (rx, ty), (rx, by), (lx, by)]
        # 下辺(lx,by)-(rx,by)を円弧に(下にふくらむ)
        bulge = 34
        # 弦中点と円弧上の点
        chord_mx, chord_my = (lx + rx) / 2, by
        arc_mx, arc_my = (lx + rx) / 2, by + bulge
        # 要素の輪郭(上辺直線+左右辺+下辺は円弧近似)
        d.line((lx, ty, rx, ty), fill=BLACK, width=3)
        d.line((rx, ty, rx, by), fill=BLACK, width=3)
        d.line((lx, by, lx, ty), fill=BLACK, width=3)
        # 下辺の実際の円弧(対象境界)を点線で
        steps = 24
        pts = []
        for k in range(steps + 1):
            t = k / steps
            xx = lx + (rx - lx) * t
            yy = by + bulge * math.sin(math.pi * t)
            pts.append((xx, yy))
        for k in range(steps):
            if k % 2 == 0:
                d.line((pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1]), fill=GRAY, width=2)
        ctext(d, cx, by + bulge + 20, "実際の円弧境界", FT, GRAY)
        # 要素の下辺(隅2点を結ぶ辺)=中間節点の位置で曲げ方が変わる
        mnx, mny = (arc_mx, arc_my) if mid_on_arc else (chord_mx, chord_my)
        if mid_on_arc:
            d.line((lx, by, mnx, mny), fill=BLACK, width=3)
            d.line((mnx, mny, rx, by), fill=BLACK, width=3)
        else:
            d.line((lx, by, rx, by), fill=BLACK, width=3)
        # 節点
        for p in corners:
            node(d, p[0], p[1], 5, fill="white")
        node(d, (lx + rx) / 2, ty, 5, fill="white")      # 上辺中間
        node(d, lx, (ty + by) / 2, 5, fill="white")       # 左辺中間
        node(d, rx, (ty + by) / 2, 5, fill="white")       # 右辺中間
        node(d, mnx, mny, 5, fill=(255, 230, 230))        # 下辺中間(配置が論点)
        ctext(d, cx, ty - 22, label, FS, BLUE)
    panel(185, "図A:中間節点を円弧上に", True)
    panel(475, "図B:中間節点を弦の中点に", False)
    note(d, "8節点要素で円弧境界を表す。中間節点の配置として適切なのは図A・図Bのどちらか?")
    save(im, "elem7CurvedIsoSetup")


# ---- 7-14 4節点vs8節点の設定(新規) (elem7Node4v8Setup) ----
def elem7Node4v8Setup():
    im, d = new(); title(d, "先端集中荷重を受ける片持ばり")
    wx = 150; yb = 220
    wall(d, wx, yb - 40, yb + 40, side=-1)
    ctext(d, wx - 26, yb, "固定", FT, GRAY, "rm")
    d.rectangle((wx, yb - 34, wx + 300, yb + 34), outline=BLACK, width=3, fill=FILL1)
    ax = wx + 300
    arrow(d, ax, yb - 54, ax, yb - 4, RED, 4, 15)
    ctext(d, ax + 14, yb - 40, "集中荷重", FT, RED, "lm")
    ctext(d, (wx + ax) / 2, yb, "平面応力要素", FT, GRAY)
    note(d, "8節点要素=高さ4×長さ10分割, 4節点要素=高さ6×長さ20分割。適切な記述はどれか?")
    save(im, "elem7Node4v8Setup")


if __name__ == "__main__":
    for fn in [f4InclinedSpringSetup, femAssemblySetup, f5ResidualStrainSetup,
               elem7QuadTempEdgeSetup, elem7CantPlateSetup, elem7ElemBendRankSetup,
               elem7SquareDetJSetup, elem7CurvedIsoSetup, elem7Node4v8Setup]:
        fn()
    print("=== all 9 ch4-7 prefig figures done ===")
