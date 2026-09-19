# -*- coding: utf-8 -*-
"""熱流体力学1級 第4章「格子の取り扱い」公式・用語図 27枚。figlibで白地660x420線画。
公式図は回答後扱いのため結論を描いてよい。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_t1e4 import _hexa, _tetra, _prism, _pyramid, _draw_elements


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=10, gap=7):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = t; b = min(t + dl, L)
        d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)
        t += dl + gap


def box(d, x0, y0, x1, y1, fill=FILL1, col=BLACK, wd=2):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def fbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS, col=BLACK):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ls = text.split("\n")
    for i, line in enumerate(ls):
        ctext(d, cx, cy - (len(ls) - 1) * 11 + i * 22, line, fnt, col)


def numnode(d, x, y, n, r=11, fill=(230, 230, 250), col=BLUE):
    node(d, x, y, r, fill=fill, col=col)
    ctext(d, x, y, str(n), FT, col)


# ---- 1. 一般座標変換
def f_general_transform():
    im, d = new()
    title(d, "一般座標変換：曲面適合格子 ⇄ 矩形格子")
    ox, oy = 55, 350
    W0, ny, nx = 200, 4, 6
    def ybot(t): return oy - 55 * math.exp(-((t - 0.5) * 3.2) ** 2)
    ytop = oy - 190
    for i in range(nx + 1):
        t = i / nx; x = ox + t * W0; yb = ybot(t)
        d.line([(x, yb + (ytop - yb) * j / ny) for j in range(ny + 1)], fill=BLUE, width=2)
    for j in range(ny + 1):
        pts = []
        for i in range(nx + 1):
            t = i / nx; x = ox + t * W0; yb = ybot(t)
            pts.append((x, yb + (ytop - yb) * j / ny))
        d.line(pts, fill=BLUE, width=2)
    ctext(d, ox + W0 / 2, oy + 22, "物理空間 (x, y)", FS, BLACK)
    arrow(d, 290, 200, 372, 200, BLACK, 3, 14)
    arrow(d, 372, 250, 290, 250, GRAY, 2, 11)
    ctext(d, 331, 178, "写像", FT, BLACK)
    rx, ry = 400, 350; Wc = Hc = 190; mx, my = 6, 4
    for i in range(mx + 1):
        x = rx + Wc * i / mx; d.line((x, ry, x, ry - Hc), fill=GREEN, width=2)
    for j in range(my + 1):
        y = ry - Hc * j / my; d.line((rx, y, rx + Wc, y), fill=GREEN, width=2)
    ctext(d, rx + Wc / 2, ry + 22, "計算空間 (ξ, η)", FS, BLACK)
    note(d, "保存形の方程式は変換後も保存形。ただし離散化後は一様流保持が係数に依存")
    save(im, "t1f4GeneralTransform")


# ---- 2. GCL
def f_gcl():
    im, d = new()
    title(d, "幾何学的保存則 (GCL)：変形格子で体積を整合")
    # 時刻n セル(実線)
    a = [(150, 300), (300, 300), (300, 150), (150, 150)]
    d.polygon(a, outline=BLUE, width=3)
    ctext(d, 225, 320, "時刻 n のセル", FT, BLUE)
    # 時刻n+1 変形後(点線)
    b = [(160, 300), (320, 290), (350, 140), (175, 160)]
    for i in range(4):
        dash(d, b[i][0], b[i][1], b[(i + 1) % 4][0], b[(i + 1) % 4][1], RED, 2)
    ctext(d, 300, 120, "時刻 n+1(変形)", FT, RED)
    # 掃く体積(面が動いた領域)を薄く塗る
    swept = [a[1], a[2], b[2], b[1]]
    d.polygon(swept, outline=ORANGE, width=1, fill=(255, 240, 220))
    d.polygon([a[1], a[2], b[2], b[1]], outline=ORANGE, width=2)
    ctext(d, 380, 220, "面が掃く体積", FT, ORANGE, "lm")
    arrow(d, 335, 220, 320, 220, ORANGE, 2, 10)
    fbox(d, 500, 330, 280, 60, "セル体積の変化 ＝\n各面が掃く体積の総和", (255, 244, 232), FS)
    note(d, "動く・変形する格子で一様流を壊さないために満たすべき条件")
    save(im, "t1f4Gcl")


# ---- 3. スタガード
def f_staggered():
    im, d = new()
    title(d, "スタガード格子：圧力=中心・速度=界面")
    ox, oy, s = 170, 110, 130
    for i in range(3):
        d.line((ox, oy + i * s, ox + 2 * s, oy + i * s), fill=LGRAY, width=2)
        d.line((ox + i * s, oy, ox + i * s, oy + 2 * s), fill=LGRAY, width=2)
    for cx in (ox + s / 2, ox + 1.5 * s):
        for cy in (oy + s / 2, oy + 1.5 * s):
            node(d, cx, cy, 8, (230, 230, 250), BLUE)
    ctext(d, ox + s / 2, oy + s / 2 - 22, "p", FT, BLUE)
    for fx in (ox, ox + s, ox + 2 * s):
        arrow(d, fx - 22, oy + s / 2, fx + 22, oy + s / 2, RED, 2, 10)
    ctext(d, ox + s + 28, oy + s / 2 - 16, "u", FT, RED, "lm")
    for fy in (oy, oy + s, oy + 2 * s):
        arrow(d, ox + 1.5 * s, fy + 22, ox + 1.5 * s, fy - 22, GREEN, 2, 10)
    ctext(d, ox + 1.5 * s + 14, oy + s + 28, "v", FT, GREEN, "lm")
    note(d, "半格子ずらす→圧力振動を抑え、3配置の中で保存性が最も良い")
    save(im, "t1f4Staggered")


# ---- 4. コロケート
def f_collocated():
    im, d = new()
    title(d, "コロケート格子：p, u, v をセル中心に配置")
    ox, oy, s = 170, 110, 130
    for i in range(3):
        d.line((ox, oy + i * s, ox + 2 * s, oy + i * s), fill=LGRAY, width=2)
        d.line((ox + i * s, oy, ox + i * s, oy + 2 * s), fill=LGRAY, width=2)
    for cx in (ox + s / 2, ox + 1.5 * s):
        for cy in (oy + s / 2, oy + 1.5 * s):
            node(d, cx, cy, 9, (230, 230, 250), BLUE)
            arrow(d, cx - 14, cy, cx + 14, cy, RED, 2, 8)
            arrow(d, cx, cy + 14, cx, cy - 14, GREEN, 2, 8)
            ctext(d, cx, cy - 26, "p,u,v", FT, BLUE)
    # 界面流速(隣接圧力で評価)
    mx = ox + s
    node(d, mx, oy + s / 2, 5, ORANGE, ORANGE)
    ctext(d, mx, oy + s / 2 - 40, "界面流速", FT, ORANGE)
    ctext(d, mx, oy + 2 * s + 22, "隣接セルの圧力で評価", FT, ORANGE)
    note(d, "全変数がセル中心→実装が単純。界面流速は運動量補間で圧力振動を回避")
    save(im, "t1f4Collocated")


# ---- 5. レギュラー
def f_regular():
    im, d = new()
    title(d, "レギュラー格子：p, u, v を同一の格子点に配置")
    ox, oy, s = 170, 110, 130
    for i in range(3):
        d.line((ox, oy + i * s, ox + 2 * s, oy + i * s), fill=LGRAY, width=2)
        d.line((ox + i * s, oy, ox + i * s, oy + 2 * s), fill=LGRAY, width=2)
    for i in range(3):
        for j in range(3):
            gx, gy = ox + i * s, oy + j * s
            node(d, gx, gy, 8, (230, 230, 250), BLUE)
    ctext(d, ox, oy - 18, "p, u, v", FT, BLUE)
    note(d, "同一点に配置→離散化は容易だが圧力振動(市松模様の偽解)を生じやすい")
    save(im, "t1f4Regular")


# ---- 6. マルチブロック
def f_multiblock():
    im, d = new()
    title(d, "マルチブロック法：境界を一致させて接続")
    ox, oy = 90, 110
    cols = [(235, 240, 250), (240, 248, 240), (250, 244, 236)]
    for k in range(3):
        bx = ox + k * 130
        box(d, bx, oy, bx + 130, oy + 200, cols[k])
        for i in range(1, 5):
            d.line((bx, oy + i * 40, bx + 130, oy + i * 40), fill=LGRAY, width=1)
        for i in range(1, 4):
            d.line((bx + i * 32, oy, bx + i * 32, oy + 200), fill=LGRAY, width=1)
        ctext(d, bx + 65, oy + 100, "ブロック%d" % (k + 1), FT, GRAY)
    for k in range(1, 3):
        d.line((ox + k * 130, oy, ox + k * 130, oy + 200), fill=RED, width=3)
    ctext(d, ox + 195, oy + 216, "接合面(境界を一致)", FT, RED)
    note(d, "領域を複数ブロックに分け境界をぴったり合わせる。データ交換ルールに従い格子生成")
    save(im, "t1f4Multiblock")


# ---- 7. オーバーセット(+ドナーセル)
def f_overset():
    im, d = new()
    title(d, "オーバーセット法：格子を重ね、ドナーセルで受け渡し")
    ox, oy = 60, 100
    box(d, ox, oy, ox + 320, oy + 200, (250, 250, 250))
    for i in range(1, 8):
        d.line((ox + i * 40, oy, ox + i * 40, oy + 200), fill=LGRAY, width=1)
    for j in range(1, 5):
        d.line((ox, oy + j * 40, ox + 320, oy + j * 40), fill=LGRAY, width=1)
    ccx, ccy = ox + 180, oy + 100
    d.ellipse((ccx - 70, ccy - 70, ccx + 70, ccy + 70), outline=BLACK, width=2)
    d.ellipse((ccx - 35, ccy - 35, ccx + 35, ccy + 35), outline=GRAY, width=2)
    node(d, ox + 40, oy + 40, 6, GREEN, GREEN)
    node(d, ccx, ccy, 6, GRAY, GRAY)
    # ドナー: 受け取り点と供給元(内点)を矢印で結ぶ
    recv = (ccx - 60, ccy - 30); donor = (ccx - 100, ccy - 30)
    node(d, recv[0], recv[1], 6, ORANGE, ORANGE)
    node(d, donor[0], donor[1], 6, GREEN, GREEN)
    arrow(d, donor[0], donor[1] - 14, recv[0], recv[1] - 14, ORANGE, 2, 9)
    ctext(d, (donor[0] + recv[0]) / 2, recv[1] - 30, "補間", FT, ORANGE)
    ly = oy + 224
    node(d, ox + 6, ly, 6, GREEN, GREEN); ctext(d, ox + 16, ly, "内点", FT, GREEN, "lm")
    node(d, ox + 90, ly, 6, GRAY, GRAY); ctext(d, ox + 100, ly, "計算に用いない点", FT, GRAY, "lm")
    node(d, ox + 6, ly + 22, 6, ORANGE, ORANGE); ctext(d, ox + 16, ly + 22, "ドナーセルから値を受ける点", FT, ORANGE, "lm")
    fbox(d, 500, 150, 250, 90, "ドナーセル＝\n値を供給する側の内点\n(格子間の橋渡し)", (255, 244, 232), FT, ORANGE)
    save(im, "t1f4Overset")


# ---- 8. PDE格子生成の3型
def f_gridgentypes():
    im, d = new()
    title(d, "偏微分方程式による格子生成：楕円/双曲/放物型")
    heads = ["型", "問題", "特徴", "用途"]
    xs = [40, 165, 300, 540, 620]
    rows = [("楕円型", "境界値問題", "滑らか・直交性制御が難・反復で重い", "内部流"),
            ("双曲型", "初期値問題", "高速・直交性に優れる", "外部流"),
            ("放物型", "初期値的", "外部境界は可・内部境界は不可", "併用")]
    y0 = 74
    box(d, xs[0], y0, xs[4], y0 + 36, (235, 235, 245))
    for c in range(4):
        ctext(d, (xs[c] + xs[c + 1]) / 2, y0 + 18, heads[c], FT, BLACK)
    for r, row in enumerate(rows):
        yy = y0 + 36 + r * 66
        box(d, xs[0], yy, xs[4], yy + 66, (250, 250, 250))
        ctext(d, (xs[0] + xs[1]) / 2, yy + 33, row[0], FS, BLUE)
        ctext(d, (xs[1] + xs[2]) / 2, yy + 33, row[1], FT, BLACK)
        ws = row[2].split("・")
        for i, w in enumerate(ws):
            ctext(d, (xs[2] + xs[3]) / 2, yy + 20 + i * 18, w, FT, GRAY)
        ctext(d, (xs[3] + xs[4]) / 2, yy + 33, row[3], FT, RED)
    for c in range(1, 4):
        d.line((xs[c], y0, xs[c], y0 + 36 + 3 * 66), fill=LGRAY, width=1)
    fbox(d, 330, 350, 560, 56, "楕円型の分布制御：ポアソン方程式のソース項 P, Q で格子を引き寄せる", (240, 244, 250), FS)
    save(im, "t1f4GridGenTypes")


# ---- 9. 代数的格子生成
def f_algebraic():
    im, d = new()
    title(d, "代数的格子生成：補間で直接 点を並べる")
    # 1次元 stretching
    oy = 150
    d.line((80, oy, 580, oy), fill=BLACK, width=2)
    n = 10
    for i in range(n + 1):
        t = i / n
        tt = 0.5 - 0.5 * math.cos(math.pi * t)  # 両端密
        x = 80 + 500 * tt
        d.line((x, oy - 7, x, oy + 7), fill=BLUE, width=2)
        node(d, x, oy, 4, BLUE, BLUE)
    ctext(d, 330, oy - 26, "1次元補間関数(Stretching function)で線分上に分布", FT, BLACK)
    arrow(d, 330, 190, 330, 240, BLACK, 2, 12)
    ctext(d, 430, 215, "多次元へ拡張", FT, GRAY, "lm")
    # 多次元 (transfinite内挿)
    ox, oy2, s = 250, 270, 110
    for i in range(6):
        d.line((ox + s * i / 5, oy2, ox + s * i / 5, oy2 + s), fill=GREEN, width=1)
        d.line((ox, oy2 + s * i / 5, ox + s, oy2 + s * i / 5), fill=GREEN, width=1)
    ctext(d, ox + s / 2, oy2 + s + 20, "Transfinite 内挿法で面・体を生成", FT, GREEN)
    note(d, "偏微分方程式を解かず高速。分布制御が直接的でGUI対話環境に向く")
    save(im, "t1f4Algebraic")


# ---- 10. ラグランジュ
def f_lagrange():
    im, d = new()
    title(d, "ラグランジュ多項式：指定点を全て通る")
    ox, oy = 100, 340
    axes(d, ox, oy, 450, 250, "ξ", "r")
    pxs = [ox + 60, ox + 170, ox + 280, ox + 390]
    pys = [oy - 60, oy - 180, oy - 90, oy - 160]
    # 通過曲線
    import numpy as _np
    xs = _np.array([p for p in pxs], float); ys = _np.array([p for p in pys], float)
    cs = _np.polyfit(xs, ys, 3)
    curve = [(x, _np.polyval(cs, x)) for x in _np.linspace(pxs[0], pxs[-1], 120)]
    d.line([(float(a), float(b)) for a, b in curve], fill=BLUE, width=3, joint="curve")
    for px, py in zip(pxs, pys):
        node(d, px, py, 6, BLUE, BLUE)
        d.line((px, py, px, oy), fill=LGRAY, width=1)
    ctext(d, 330, 90, "基底 φj(ξi)=δij（自分の点で1・他点で0）", FT, BLACK)
    note(d, "N点ならN−1次。指定点を必ず全て通る（『通らない』は誤り）")
    save(im, "t1f4Lagrange")


# ---- 11. エルミート
def f_hermite():
    im, d = new()
    title(d, "エルミート多項式：位置 ＋ 勾配 を指定")
    ox, oy = 100, 340
    axes(d, ox, oy, 450, 250, "ξ", "r")
    pxs = [ox + 70, ox + 220, ox + 360]
    pys = [oy - 70, oy - 170, oy - 90]
    slopes = [0.8, -0.1, -0.9]
    d.line(list(zip(pxs, pys)), fill=BLUE, width=3, joint="curve")
    for px, py, sl in zip(pxs, pys, slopes):
        node(d, px, py, 6, BLUE, BLUE)
        d.line((px - 30, py - sl * 30, px + 30, py + sl * 30), fill=RED, width=2)
        d.line((px, py, px, oy), fill=LGRAY, width=1)
    ctext(d, 330, 90, "各点で位置 r と勾配 dr/dξ の両方を与える", FT, BLACK)
    ctext(d, ox + 360, oy - 130, "赤=指定勾配(接線)", FT, RED)
    note(d, "境界での格子線の入射角まで制御できる（ラグランジュより自由度が高い）")
    save(im, "t1f4Hermite")


# ---- 12. スプライン
def f_spline():
    im, d = new()
    title(d, "スプライン(B-spline)：区分多項式を滑らかに接続")
    ox, oy = 100, 340
    axes(d, ox, oy, 450, 250, "ξ", "r")
    pxs = [ox + 40, ox + 130, ox + 220, ox + 310, ox + 400]
    pys = [oy - 40, oy - 150, oy - 80, oy - 170, oy - 60]
    for i in range(len(pxs) - 1):
        col = BLUE if i % 2 == 0 else GREEN
        mx0 = pxs[i]; mx1 = pxs[i + 1]
        seg = [(x, pys[i] + (pys[i + 1] - pys[i]) * (0.5 - 0.5 * math.cos(math.pi * (x - mx0) / (mx1 - mx0))))
               for x in [mx0 + (mx1 - mx0) * t / 20 for t in range(21)]]
        d.line(seg, fill=col, width=3, joint="curve")
    for px, py in zip(pxs, pys):
        node(d, px, py, 6, "white", BLACK)
    ctext(d, 330, 90, "制御点・ノットベクトルで定義。高次導関数まで連続", FT, BLACK)
    note(d, "色分けした各区分多項式が接続点で滑らかにつながる")
    save(im, "t1f4Spline")


# ---- 13. Transfinite
def f_transfinite():
    im, d = new()
    title(d, "Transfinite補間：4辺の分布を混ぜて内部を埋める")
    ox, oy, s = 90, 350, 240
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3)
    n = 6
    for i in range(n + 1):
        t = i / n; tt = 0.5 - 0.5 * math.cos(math.pi * t)
        # 内部格子(混合結果)を薄く
    # 内部の格子(結果)を描く
    for i in range(n + 1):
        ti = i / n; xi = 0.5 - 0.5 * math.cos(math.pi * ti)
        d.line((ox + s * xi, oy, ox + s * xi, oy - s), fill=(210, 220, 245), width=1)
    for j in range(n + 1):
        tj = j / n; yj = 0.5 - 0.5 * math.cos(math.pi * tj)
        d.line((ox, oy - s * yj, ox + s, oy - s * yj), fill=(210, 220, 245), width=1)
    for i in range(n + 1):
        t = i / n; tt = 0.5 - 0.5 * math.cos(math.pi * t)
        node(d, ox + s * tt, oy, 4, BLUE, BLUE); node(d, ox + s * tt, oy - s, 4, BLUE, BLUE)
        node(d, ox, oy - s * tt, 4, GREEN, GREEN); node(d, ox + s, oy - s * tt, 4, GREEN, GREEN)
    ctext(d, ox + s / 2, oy + 22, "ξ", FT, BLUE)
    ctext(d, ox - 22, oy - s / 2, "η", FT, GREEN)
    fbox(d, 490, 150, 300, 70, "r = ξ方向補間 ＋ η方向補間\n − 四隅の重複(角点)を差引く", (240, 244, 250), FT)
    ctext(d, 490, 240, "混合関数の選択で格子の質が変わる", FT, GRAY)
    ctext(d, 490, 300, "手順：まず4辺→次に内部", FT, RED)
    save(im, "t1f4Transfinite")


# ---- 14. ボクセル
def f_voxel():
    im, d = new()
    title(d, "ボクセル格子：直交セルで形状を表現")
    titles = ["バイナリ(0/1)", "体積率", "距離関数(SDF)"]
    for p in range(3):
        bx, by = 40 + p * 205, 80
        for i in range(6):
            for j in range(6):
                x0 = bx + i * 28; y0 = by + j * 28
                cxx, cyy = x0 + 14, y0 + 14
                dist = math.hypot(cxx - (bx + 84), cyy - (by + 84))
                inside = dist < 62
                if p == 0:
                    fill = (210, 225, 245) if inside else "white"
                    d.rectangle((x0, y0, x0 + 28, y0 + 28), outline=LGRAY, width=1, fill=fill)
                    ctext(d, cxx, cyy, "1" if inside else "0", FT, BLUE if inside else LGRAY)
                elif p == 1:
                    frac = max(0.0, min(1.0, (62 - dist) / 28 + 0.5)); g = int(245 - 120 * frac)
                    d.rectangle((x0, y0, x0 + 28, y0 + 28), outline=LGRAY, width=1, fill=(g, g + 10, 250))
                else:
                    d.rectangle((x0, y0, x0 + 28, y0 + 28), outline=LGRAY, width=1, fill="white")
                    ctext(d, cxx, cyy, str(int((dist - 62) / 14)), FT, GRAY)
        d.ellipse((bx + 84 - 62, by + 84 - 62, bx + 84 + 62, by + 84 + 62), outline=RED, width=2)
        ctext(d, bx + 84, by + 180, titles[p], FT, BLACK)
    note(d, "入力=三角形パッチ/点群/CT断層。水密でなくても生成可・座標変換メトリクス不要で有利")
    save(im, "t1f4Voxel")


# ---- 15. CSG
def f_csg():
    im, d = new()
    title(d, "CSG(構成的立体幾何)：基本立体のブール演算")
    # A ∪ B, A − B, A ∩ B の3例
    ops = ["和 (∪)", "差 (−)", "積 (∩)"]
    for p in range(3):
        cx = 130 + p * 200; cy = 210
        if p == 0:
            d.rectangle((cx - 55, cy - 30, cx + 20, cy + 45), outline=BLUE, width=2, fill=(225, 235, 250))
            d.ellipse((cx - 20, cy - 45, cx + 55, cy + 30), outline=BLUE, width=2, fill=(225, 235, 250))
        elif p == 1:
            d.rectangle((cx - 55, cy - 30, cx + 20, cy + 45), outline=BLUE, width=2, fill=(225, 235, 250))
            d.ellipse((cx - 20, cy - 45, cx + 55, cy + 30), outline="white", width=2, fill="white")
            d.ellipse((cx - 20, cy - 45, cx + 55, cy + 30), outline=RED, width=2)
        else:
            d.rectangle((cx - 55, cy - 30, cx + 20, cy + 45), outline=LGRAY, width=1)
            d.ellipse((cx - 20, cy - 45, cx + 55, cy + 30), outline=LGRAY, width=1)
            # 交差領域を近似的に塗る
            d.pieslice((cx - 20, cy - 45, cx + 55, cy + 30), 90, 270, outline=GREEN, width=2, fill=(225, 245, 230))
            d.rectangle((cx - 20, cy - 30, cx + 20, cy + 30), outline=GREEN, width=1, fill=(225, 245, 230))
        ctext(d, cx, cy + 75, ops[p], FS, BLACK)
    ctext(d, 130, 100, "直方体", FT, GRAY); ctext(d, 330, 100, "円柱", FT, GRAY)
    note(d, "直方体・球・円柱などの基本立体を和・差・積で組合せて複雑形状を構成")
    save(im, "t1f4Csg")


# ---- 16. SDF
def f_sdf():
    im, d = new()
    title(d, "SDF(符号付き距離関数)：表面までの距離＋内外符号")
    cx, cy = 300, 220
    # 物体境界(不規則な閉曲線を円で代表)
    R = 70
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=RED, width=3)
    ctext(d, cx, cy - R - 16, "物体表面(値=0)", FT, RED)
    # 等距離線(内側=負、外側=正)
    for k, r in enumerate([30, 50, 90, 110]):
        col = BLUE if r < R else GREEN
        dash(d, cx - r, cy, cx + r, cy, col, 1, 4, 5)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=1)
    ctext(d, cx, cy, "−", F, BLUE)
    ctext(d, cx + 100, cy + 70, "＋", F, GREEN)
    ctext(d, cx - 130, cy, "内側 = 負", FT, BLUE, "lm")
    ctext(d, cx + 120, cy - 40, "外側 = 正", FT, GREEN, "lm")
    fbox(d, 300, 360, 560, 46, "法線・曲率も3次元スカラ値のみで表現できる(陰関数表現)", (240, 244, 250), FS)
    save(im, "t1f4Sdf")


# ---- 17. カットセル
def f_cutcell():
    im, d = new()
    title(d, "カットセル法：境界でセルを切って形状に合わせる")
    ox, oy, s, n = 130, 90, 40, 6
    for i in range(n):
        for j in range(n):
            d.rectangle((ox + i * s, oy + j * s, ox + i * s + s, oy + j * s + s), outline=LGRAY, width=1)
    # 曲線境界
    cpts = [(ox + t * s * n / 40, oy + 70 + 120 * (t / 40)) for t in range(41)]
    d.line(cpts, fill=RED, width=3)
    # 小さくカットされたセルを強調
    box(d, ox + 1 * s, oy + 2 * s, ox + 1 * s + s, oy + 2 * s + 12, (255, 225, 225), RED, 2)
    arrow(d, ox + 4 * s, oy + 30, ox + 1.5 * s, oy + 2 * s, RED, 2, 10)
    ctext(d, ox + 4.4 * s, oy + 24, "小さいセル", FT, RED, "lm")
    fbox(d, 500, 300, 260, 88, "小セル→陽解法で\nCFL条件が厳しい\n→隣接セルと結合", (255, 236, 236), FT, RED)
    note(d, "階段状より精度よく形状を表現できる")
    save(im, "t1f4CutCell")


# ---- 18. IBM
def f_ibm():
    im, d = new()
    title(d, "埋込境界法(IBM)：外力項で境界条件を課す")
    ox, oy, s, n = 120, 90, 38, 7
    for i in range(n):
        for j in range(n):
            gx, gy = ox + i * s, oy + j * s
            node(d, gx, gy, 3, LGRAY, LGRAY)
    # 物体境界(格子と独立の連結点群)
    ccx, ccy, R = ox + 3 * s, oy + 3 * s, 90
    circ = [(ccx + R * math.cos(a), ccy + R * math.sin(a)) for a in [math.radians(t) for t in range(0, 361, 20)]]
    d.line(circ, fill=RED, width=2)
    for p in circ[::2]:
        node(d, p[0], p[1], 4, RED, RED)
    # 近似δ関数で近傍格子点へ力配分
    lp = circ[4]
    for gx, gy in [(ox + 2 * s, oy + s), (ox + 3 * s, oy + s), (ox + 2 * s, oy + 2 * s)]:
        arrow(d, lp[0], lp[1], gx, gy, ORANGE, 1, 7)
    ctext(d, ccx, ccy, "物体", FT, RED)
    fbox(d, 520, 200, 240, 100, "格子は形状に\n合わせない。\n外力項＋近似δ関数で\n力を格子点へ配分", (255, 244, 232), FT, ORANGE)
    note(d, "格子を張り替えないので物体の移動・変形も柔軟に扱える")
    save(im, "t1f4Ibm")


# ---- 19. デローニ
def f_delaunay():
    im, d = new()
    title(d, "デローニ分割：空円条件(外接円に他節点なし)")
    pts = [(120, 320), (260, 350), (210, 180), (360, 270), (330, 130)]
    tris = [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
    for (i, j, k) in tris:
        d.polygon([pts[i], pts[j], pts[k]], outline=BLUE, width=3)
    (x1, y1), (x2, y2), (x3, y3) = pts[0], pts[1], pts[2]
    ax, ay, bx, by = x2 - x1, y2 - y1, x3 - x1, y3 - y1
    d2 = 2 * (ax * by - ay * bx)
    ux = (by * (ax * ax + ay * ay) - ay * (bx * bx + by * by)) / d2
    uy = (ax * (bx * bx + by * by) - bx * (ax * ax + ay * ay)) / d2
    cxr, cyr = x1 + ux, y1 + uy; rr = math.hypot(cxr - x1, cyr - y1)
    d.ellipse((cxr - rr, cyr - rr, cxr + rr, cyr + rr), outline=RED, width=2)
    node(d, cxr, cyr, 4, RED, RED)
    for p in pts:
        node(d, p[0], p[1], 6, "white", BLACK)
    fbox(d, 520, 200, 240, 90, "各要素の外接円\n(3次元は外接球)の\n内部に他節点なし", (255, 236, 236), FT, RED)
    note(d, "つぶれた要素を避け最小内角を最大化する良質な分割")
    save(im, "t1f4Delaunay")


# ---- 20. アドバンシングフロント
def f_advancing_front():
    im, d = new()
    title(d, "アドバンシングフロント法(先端前進法)")
    d.line((90, 120, 570, 120), fill=BLACK, width=3)
    ctext(d, 330, 104, "境界(初期フロント)", FT, GRAY)
    base = [(120, 120), (180, 120), (240, 120), (300, 120), (360, 120), (420, 120), (480, 120), (540, 120)]
    # 1段目(生成済)
    for i in range(len(base) - 1):
        apex = ((base[i][0] + base[i + 1][0]) / 2, 120 + 55)
        d.polygon([base[i], base[i + 1], apex], outline=GREEN, width=2)
        node(d, apex[0], apex[1], 4, GREEN, GREEN)
    for p in base:
        node(d, p[0], p[1], 4, "white", BLACK)
    # 新フロント
    front2 = [((base[i][0] + base[i + 1][0]) / 2, 175) for i in range(len(base) - 1)]
    d.line(front2, fill=ORANGE, width=2)
    ctext(d, 330, 200, "新しいフロント", FT, ORANGE)
    arrow(d, 330, 215, 330, 265, GREEN, 2, 12)
    ctext(d, 330, 290, "先端を内部へ順次前進(節点と要素を同時生成)", FT, GREEN)
    note(d, "境界近くで品質の良い要素を作りやすい。デローニ分割とは考え方が異なる")
    save(im, "t1f4AdvancingFront")


# ---- 21. 非構造格子
def f_unstructured():
    im, d = new()
    title(d, "非構造格子：規則性なく任意形状に適合")
    import random
    random.seed(11)
    # 不規則な三角形分割(円形領域)
    cx, cy, R = 240, 220, 130
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in range(0, 360, 30)]
    inner = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
             for a, r in [(20, 70), (110, 55), (200, 75), (290, 60), (150, 30), (330, 35)]]
    allp = pts + inner + [(cx, cy)]
    # 簡易に中心から扇状の三角＋内部点結線
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        near = min(inner, key=lambda q: math.hypot(q[0] - (pts[i][0] + pts[j][0]) / 2, q[1] - (pts[i][1] + pts[j][1]) / 2))
        d.polygon([pts[i], pts[j], near], outline=BLUE, width=1)
    for a in range(len(inner)):
        d.line((inner[a][0], inner[a][1], inner[(a + 1) % len(inner)][0], inner[(a + 1) % len(inner)][1]), fill=BLUE, width=1)
    for p in allp:
        node(d, p[0], p[1], 3, "white", BLACK)
    fbox(d, 520, 200, 250, 130, "構造格子との比較：\n・メモリ使用量 多\n・演算量 多\n・メモリアクセス不連続\n→処理速度は低下傾向", (250, 250, 236), FT, GRAY)
    note(d, "任意複雑形状に強い。格子点の追加・削除がしやすく解適合格子法を導入しやすい")
    save(im, "t1f4Unstructured")


# ---- 22. ハイブリッド格子
def f_hybrid():
    im, d = new()
    title(d, "ハイブリッド格子：プリズム＋四面体＋ピラミッド")
    ox, x1, yw = 70, 590, 340
    d.line((ox, yw, x1, yw), fill=BLACK, width=3)
    for i in range(14):
        xx = ox + i * (x1 - ox) / 14
        d.line((xx + (x1 - ox) / 14, yw, xx, yw + 14), fill=BLACK, width=2)
    ctext(d, 330, yw + 26, "物体表面", FT, GRAY)
    # プリズム層(壁近傍)
    for layer in range(3):
        y0 = yw - (layer + 1) * 24; y1r = yw - layer * 24
        d.line((ox, y0, x1, y0), fill=BLUE, width=1)
        for i in range(14):
            xx = ox + i * (x1 - ox) / 13
            d.line((xx, y0, xx, y1r), fill=BLUE, width=1)
    d.line((ox, yw, x1, yw), fill=BLUE, width=1)
    ctext(d, 150, yw - 36, "プリズム層", FT, BLUE, "lm")
    # ピラミッド(遷移) ライン
    ytrans = yw - 3 * 24
    dash(d, ox, ytrans, x1, ytrans, ORANGE, 2)
    ctext(d, 470, ytrans + 12, "ピラミッド(遷移)", FT, ORANGE, "lm")
    # 四面体(外側)
    for i in range(8):
        x0 = ox + 30 + i * 62
        for j in range(2):
            y0 = 100 + j * 55
            d.polygon([(x0, y0), (x0 + 62, y0), (x0 + 31, y0 + 55)], outline=GREEN, width=1)
            d.polygon([(x0 + 62, y0), (x0 + 31, y0 + 55), (x0 + 93, y0 + 55)], outline=GREEN, width=1)
    ctext(d, 150, 96, "四面体(外側)", FT, GREEN, "lm")
    note(d, "壁際=プリズムで境界層を解像、外側=四面体、つなぎ目=ピラミッド。精度と効率を両立")
    save(im, "t1f4Hybrid")


# ---- 23. 3次元要素
def f_elements():
    im, d = new()
    title(d, "非構造格子の3次元要素")
    _draw_elements(d, roles=True)
    save(im, "t1f4Elements")


# ---- 24. 解適合格子法
def f_adaptive():
    im, d = new()
    title(d, "解適合格子法：誤差の大きい領域に格子を集中")
    ox, oy, s, n = 90, 100, 40, 10
    # 基準格子
    for i in range(n // 2 + 1):
        d.line((ox, oy + i * s, ox + (n // 2) * s, oy + i * s), fill=LGRAY, width=1)
        d.line((ox + i * s, oy, ox + i * s, oy + (n // 2) * s), fill=LGRAY, width=1)
    # 高勾配領域(赤)＝局所細分化
    hx, hy = ox + 3 * s, oy + 3 * s
    for i in range(2):
        for j in range(2):
            cx0 = hx + i * s; cy0 = hy + j * s
            for a in range(2):
                for b in range(2):
                    d.rectangle((cx0 + a * s / 2, cy0 + b * s / 2, cx0 + (a + 1) * s / 2, cy0 + (b + 1) * s / 2), outline=RED, width=1)
    # 境界層/渦の模式
    d.ellipse((hx - 6, hy - 6, hx + 2 * s + 6, hy + 2 * s + 6), outline=RED, width=2)
    ctext(d, hx + s, hy + 2 * s + 24, "誤差大の領域(渦・境界層)", FT, RED)
    fbox(d, 510, 200, 250, 120, "非構造格子なら\n局所的に相似分割でき\n大域的な再生成は不要。\n誤差指標で細分化/粗大化", (255, 236, 236), FT, GRAY)
    note(d, "格子を細かくしても解が変わらなくなるまで＝格子依存性の排除")
    save(im, "t1f4Adaptive")


# ---- 25. 格子品質
def f_quality():
    im, d = new()
    title(d, "格子品質：歪度・アスペクト比・直交性")
    panels = [(40, 70, 236, 300, "歪度(スキューネス)"), (240, 70, 436, 300, "アスペクト比"), (440, 70, 620, 300, "直交性")]
    # 歪度
    x0, y0, x1, y1, _ = panels[0]
    d.polygon([(x0 + 40, y0 + 60), (x0 + 150, y0 + 50), (x0 + 130, y0 + 150), (x0 + 30, y0 + 140)], outline=GREEN, width=2)
    ctext(d, (x0 + x1) / 2, y0 + 100, "良い", FT, GREEN)
    d.polygon([(x0 + 40, y0 + 180), (x0 + 160, y0 + 175), (x0 + 90, y0 + 215), (x0 + 55, y0 + 205)], outline=RED, width=2)
    ctext(d, (x0 + x1) / 2, y0 + 195, "つぶれ=悪い", FT, RED)
    # アスペクト比
    x0, y0, x1, y1, _ = panels[1]
    d.rectangle((x0 + 55, y0 + 50, x0 + 125, y0 + 120), outline=GREEN, width=2)
    ctext(d, (x0 + x1) / 2, y0 + 85, "1に近い=良い", FT, GREEN)
    d.rectangle((x0 + 30, y0 + 170, x0 + 165, y0 + 200), outline=RED, width=2)
    ctext(d, (x0 + x1) / 2, y0 + 220, "細長い=悪い", FT, RED)
    # 直交性
    x0, y0, x1, y1, _ = panels[2]
    cx = (x0 + x1) / 2
    d.line((cx - 40, y0 + 90, cx + 40, y0 + 90), fill=GREEN, width=2)
    d.line((cx, y0 + 50, cx, y0 + 130), fill=GREEN, width=2)
    ctext(d, cx, y0 + 150, "直角=良い", FT, GREEN)
    d.line((cx - 40, y0 + 200, cx + 40, y0 + 200), fill=RED, width=2)
    d.line((cx - 20, y0 + 165, cx + 20, y0 + 235), fill=RED, width=2)
    ctext(d, cx, y0 + 255, "斜め=悪い", FT, RED)
    for (px0, py0, px1, py1, ttl) in panels:
        d.rectangle((px0, py0, px1, py1), outline=LGRAY, width=2)
        ctext(d, (px0 + px1) / 2, py0 + 16, ttl, FT, BLACK)
    note(d, "四面体は正四面体・六面体は立方体に近いほど良い。楕円型は直交性制御が難、双曲型は良好")
    save(im, "t1f4Quality")


# ---- 26. 双一次写像(結論可)
def f_bilinear():
    im, d = new()
    title(d, "双一次写像：4節点四角形要素(1,1)(7,3)(3,5)(1,9)")
    # 左:計算空間
    ox, oy, s = 60, 330, 170
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3)
    corners = [(ox, oy), (ox + s, oy), (ox + s, oy - s), (ox, oy - s)]
    for k, (cx, cy) in enumerate(corners):
        numnode(d, cx, cy, k + 1, 11, (230, 230, 250), BLUE)
    ctext(d, ox + s / 2, oy + 20, "計算空間 [-1,1]²", FT, BLACK)
    ctext(d, ox, oy + 6, "(-1,-1)", FT, GRAY, "rm")
    arrow(d, 250, 200, 320, 200, BLACK, 3, 13)
    ctext(d, 285, 178, "双一次写像", FT, BLACK)
    # 右:物理空間
    rx, ry = 360, 350
    def P(x, y): return (rx + 22 * x, ry - 28 * (y - 1))
    q = [P(1, 1), P(7, 3), P(3, 5), P(1, 9)]
    d.polygon(q, outline=BLUE, width=3)
    labs = ["(1,1)", "(7,3)", "(3,5)", "(1,9)"]
    offs = [(-4, 16), (18, 4), (18, 0), (-4, -16)]
    for k, ((px, py), lab, (dxx, dyy)) in enumerate(zip(q, labs, offs)):
        numnode(d, px, py, k + 1, 11, (230, 230, 250), BLUE)
        ctext(d, px + dxx, py + dyy, lab, FT, GRAY, "lm" if dxx >= 0 else "rm")
    ctext(d, rx + 70, ry + 20, "物理空間 (x, y)", FT, BLACK)
    fbox(d, 490, 92, 320, 42, "形状関数 ¼(1±ξ)(1±η) で4頂点を補間", (240, 244, 250), FT)
    save(im, "t1f4Bilinear")


# ---- 27. ヤコビアン特異領域(結論可)
def f_jacobian():
    im, d = new()
    title(d, "ヤコビアン det J の符号：特異領域を判定")
    ox, oy, s = 130, 340, 240
    def PX(xi, eta): return (ox + (xi + 1) / 2 * s, oy - (eta + 1) / 2 * s)
    # 特異領域(det J<=0): η >= -7/8 ξ + 9/8。正方形内では (1,1/4)-(1,1)-(1/7,1)の三角
    p1 = PX(1, 0.25); p2 = PX(1, 1); p3 = PX(1 / 7, 1)
    d.polygon([p1, p2, p3], outline=RED, width=2, fill=(255, 228, 228))
    # 正方形枠
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3)
    for i in range(1, 8):
        v = -1 + 2 * i / 8
        d.line((PX(v, -1)[0], oy, PX(v, -1)[0], oy - s), fill=(230, 230, 230), width=1)
        d.line((ox, PX(-1, v)[1], ox + s, PX(-1, v)[1]), fill=(230, 230, 230), width=1)
    # 直線 η=-7/8ξ+9/8
    d.line((p1[0], p1[1], p3[0], p3[1]), fill=RED, width=3)
    node(d, p1[0], p1[1], 4, RED, RED); node(d, p3[0], p3[1], 4, RED, RED)
    ctext(d, p1[0] + 6, p1[1] + 14, "(1, 1/4)", FT, RED, "lm")
    ctext(d, p3[0] - 6, p3[1] - 14, "(1/7, 1)", FT, RED, "rm")
    # ラベル
    ctext(d, PX(0.65, 0.8)[0], PX(0.65, 0.8)[1], "det J ≤ 0\n(特異・使用不可)", FT, RED)
    ctext(d, PX(-0.3, -0.4)[0], PX(-0.3, -0.4)[1], "det J > 0\n(1対1対応)", FT, BLUE)
    ctext(d, ox + s / 2, oy + 20, "ξ", FT, BLACK); ctext(d, ox - 22, oy - s / 2, "η", FT, BLACK)
    ctext(d, ox, oy + 6, "(-1,-1)", FT, GRAY, "rm")
    fbox(d, 520, 150, 250, 70, "det J = 9/2 − 7/2 ξ − 4η\n特異：η ≥ −7/8 ξ + 9/8", (255, 236, 236), FT, RED)
    note(d, "直線より上側で写像が特異になり格子として使えない")
    save(im, "t1f4Jacobian")


if __name__ == "__main__":
    f_general_transform(); f_gcl(); f_staggered(); f_collocated(); f_regular()
    f_multiblock(); f_overset(); f_gridgentypes(); f_algebraic(); f_lagrange()
    f_hermite(); f_spline(); f_transfinite(); f_voxel(); f_csg()
    f_sdf(); f_cutcell(); f_ibm(); f_delaunay(); f_advancing_front()
    f_unstructured(); f_hybrid(); f_elements(); f_adaptive(); f_quality()
    f_bilinear(); f_jacobian()
    print("done t1f4 (27)")
