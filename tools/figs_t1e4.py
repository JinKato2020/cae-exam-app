# -*- coding: utf-8 -*-
"""熱流体力学1級 第4章「格子の取り扱い」問題図 14枚。figlibで白地660x420線画。
required(回答前)の t1e4GeneralTransform / t1e4GridArrangement / t1e4Transfinite / t1e4Jacobian は
正解・結論・特異範囲を一切描かない(設定・概念のみ)。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


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


# ============================================================ 4-1 一般座標変換(required)
def f_general_transform():
    im, d = new()
    title(d, "一般座標変換：物理空間 と 計算空間")
    # 左：物理空間(x,y) 曲面適合の歪んだ格子
    ox, oy = 55, 360
    W0, ny = 210, 4
    def ybot(t):  # t in [0,1] 下境界=バンプ
        return oy - 60 * math.exp(-((t - 0.5) * 3.2) ** 2)
    ytop = oy - 200
    nx = 6
    for i in range(nx + 1):
        t = i / nx
        x = ox + t * W0
        yb = ybot(t)
        pts = [(x, yb + (ytop - yb) * (j / ny)) for j in range(ny + 1)]
        d.line(pts, fill=BLUE, width=2)
    for j in range(ny + 1):
        pts = []
        for i in range(nx + 1):
            t = i / nx
            x = ox + t * W0
            yb = ybot(t)
            pts.append((x, yb + (ytop - yb) * (j / ny)))
        d.line(pts, fill=BLUE, width=2)
    ctext(d, ox + W0 / 2, oy + 24, "物理空間 (x, y)", FS, BLACK)
    ctext(d, ox + W0 / 2, oy - 214, "曲面に沿う境界適合格子", FT, GRAY)
    # 中央：写像矢印
    arrow(d, 300, 210, 372, 210, BLACK, 3, 14)
    ctext(d, 336, 186, "写像", FT, BLACK)
    ctext(d, 336, 232, "座標変換", FT, GRAY)
    # 右：計算空間(ξ,η) 矩形一様格子
    rx, ry = 400, 360
    Wc, Hc = 200, 200
    mx, my = 6, 4
    for i in range(mx + 1):
        x = rx + Wc * i / mx
        d.line((x, ry, x, ry - Hc), fill=GREEN, width=2)
    for j in range(my + 1):
        y = ry - Hc * j / my
        d.line((rx, y, rx + Wc, y), fill=GREEN, width=2)
    ctext(d, rx + Wc / 2, ry + 24, "計算空間 (ξ, η)", FS, BLACK)
    ctext(d, rx + Wc / 2, ry - Hc - 14, "矩形・等間隔格子", FT, GRAY)
    note(d, "曲面に沿う格子を矩形の計算空間へ写す＝差分法で任意形状を扱う")
    save(im, "t1e4GeneralTransform")


# ============================================================ 4-2 変数配置(required・中立)
def f_grid_arrangement():
    im, d = new()
    title(d, "変数配置：スタガード・コロケート・レギュラー")
    labels = ["スタガード格子", "コロケート格子", "レギュラー格子"]
    subs = ["p=中心 / u,v=界面", "p,u,v=中心", "p,u,v=格子点"]
    cxs = [150, 355, 560]
    s = 96
    for k, cx in enumerate(cxs):
        oy = 120
        x0, y0 = cx - s / 2, oy
        # 1セル枠
        d.rectangle((x0, y0, x0 + s, y0 + s), outline=LGRAY, width=2)
        if k == 0:  # スタガード
            node(d, x0 + s / 2, y0 + s / 2, 8, (230, 230, 250), BLUE)
            ctext(d, x0 + s / 2, y0 + s / 2, "p", FT, BLUE)
            arrow(d, x0 - 12, y0 + s / 2, x0 + 12, y0 + s / 2, RED, 2, 9)
            arrow(d, x0 + s - 12, y0 + s / 2, x0 + s + 12, y0 + s / 2, RED, 2, 9)
            ctext(d, x0 + s + 20, y0 + s / 2, "u", FT, RED, "lm")
            arrow(d, x0 + s / 2, y0 + s + 12, x0 + s / 2, y0 + s - 12, GREEN, 2, 9)
            arrow(d, x0 + s / 2, y0 + 12, x0 + s / 2, y0 - 12, GREEN, 2, 9)
            ctext(d, x0 + s / 2 + 14, y0 - 14, "v", FT, GREEN, "lm")
        elif k == 1:  # コロケート
            cx0, cy0 = x0 + s / 2, y0 + s / 2
            node(d, cx0, cy0, 9, (230, 230, 250), BLUE)
            ctext(d, cx0, cy0 - 22, "p", FT, BLUE)
            arrow(d, cx0 - 14, cy0, cx0 + 14, cy0, RED, 2, 9)
            ctext(d, cx0 + 22, cy0, "u", FT, RED, "lm")
            arrow(d, cx0, cy0 + 14, cx0, cy0 - 14, GREEN, 2, 9)
            ctext(d, cx0, cy0 + 24, "v", FT, GREEN)
        else:  # レギュラー
            for (nx, ny) in [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]:
                node(d, nx, ny, 7, (230, 230, 250), BLUE)
            ctext(d, x0, y0 - 16, "p,u,v", FT, BLUE)
        ctext(d, cx, oy + s + 36, labels[k], FS, BLACK)
        ctext(d, cx, oy + s + 60, subs[k], FT, GRAY)
    note(d, "同じ1セルでの変数の置き場所の違い（配置のみ）")
    save(im, "t1e4GridArrangement")


# ============================================================ 4-3 マルチブロック/オーバーセット
def f_multiblock():
    im, d = new()
    title(d, "マルチブロック法 と オーバーセット法")
    # 左：マルチブロック(境界一致)
    ox, oy = 50, 110
    for (bx, bw, col) in [(ox, 90, (235, 240, 250)), (ox + 90, 90, (240, 248, 240))]:
        box(d, bx, oy, bx + bw, oy + 160, col)
        for i in range(1, 4):
            d.line((bx, oy + i * 40, bx + bw, oy + i * 40), fill=LGRAY, width=1)
        for i in range(1, 3):
            d.line((bx + i * 30, oy, bx + i * 30, oy + 160), fill=LGRAY, width=1)
    d.line((ox + 90, oy, ox + 90, oy + 160), fill=RED, width=3)
    ctext(d, ox + 90, oy + 178, "境界を一致させ接続", FT, RED)
    ctext(d, ox + 90, oy - 14, "マルチブロック法", FS, BLACK)
    # 右：オーバーセット(重合・3種の点)
    rx, ry = 360, 110
    box(d, rx, ry, rx + 240, ry + 160, (250, 250, 250))
    for i in range(1, 6):
        d.line((rx + i * 40, ry, rx + i * 40, ry + 160), fill=LGRAY, width=1)
        d.line((rx, ry + i * 27, rx + 240, ry + i * 27), fill=LGRAY, width=1)
    # 重ねた別格子(円形領域=物体)
    d.ellipse((rx + 80, ry + 40, rx + 180, ry + 130), outline=BLACK, width=2)
    # 3種の点
    numnode(d, rx + 40, ry + 40, "", 6, GREEN, GREEN); node(d, rx + 40, ry + 40, 6, GREEN, GREEN)
    node(d, rx + 130, ry + 85, 6, GRAY, GRAY)          # 計算外点(物体内)
    node(d, rx + 200, ry + 120, 6, GREEN, GREEN)       # 内点
    node(d, rx + 90, ry + 55, 6, ORANGE, ORANGE)       # ドナー受け取り点
    ctext(d, rx + 120, ry - 14, "オーバーセット法", FS, BLACK)
    # 凡例
    ly = ry + 178
    node(d, rx + 6, ly, 6, GREEN, GREEN); ctext(d, rx + 16, ly, "内点", FT, GREEN, "lm")
    node(d, rx + 92, ly, 6, GRAY, GRAY); ctext(d, rx + 102, ly, "計算に用いない点", FT, GRAY, "lm")
    node(d, rx + 6, ly + 22, 6, ORANGE, ORANGE); ctext(d, rx + 16, ly + 22, "ドナーセルから値を受ける点", FT, ORANGE, "lm")
    save(im, "t1e4Multiblock")


# ============================================================ 4-4 PDE格子生成(3型)
def f_pde_grid():
    im, d = new()
    title(d, "偏微分方程式による格子生成：3つの型")
    heads = ["型", "解く問題", "特徴", "主な用途"]
    xs = [40, 175, 315, 540, 620]
    rows = [
        ("楕円型", "境界値問題", "滑らか・直交性/分布の制御が難・反復で重い", "内部流"),
        ("双曲型", "初期値問題", "計算が速い・直交性に優れる", "外部流"),
        ("放物型", "初期値問題的", "外部境界は可・内部境界は不可・単体使用少", "併用"),
    ]
    y0 = 78
    # ヘッダ
    box(d, xs[0], y0, xs[4], y0 + 40, (235, 235, 245))
    for c in range(4):
        ctext(d, (xs[c] + xs[c + 1]) / 2, y0 + 20, heads[c], FT, BLACK)
    for r, row in enumerate(rows):
        yy = y0 + 40 + r * 92
        box(d, xs[0], yy, xs[4], yy + 92, (250, 250, 250))
        ctext(d, (xs[0] + xs[1]) / 2, yy + 46, row[0], FS, BLUE)
        ctext(d, (xs[1] + xs[2]) / 2, yy + 46, row[1], FT, BLACK)
        # 特徴は折り返し
        words = row[2].split("・")
        for i, w in enumerate(words):
            ctext(d, (xs[2] + xs[3]) / 2, yy + 24 + i * 20, w, FT, GRAY)
        ctext(d, (xs[3] + xs[4]) / 2, yy + 46, row[3], FT, RED)
    for c in range(1, 4):
        d.line((xs[c], y0, xs[c], y0 + 40 + 3 * 92), fill=LGRAY, width=1)
    save(im, "t1e4PdeGrid")


# ============================================================ 4-5 補間関数の対比
def f_interpolation():
    im, d = new()
    title(d, "代数的格子生成の補間関数")
    panels = [(40, 62, 336, 236, "ラグランジュ"), (348, 62, 620, 236, "エルミート"),
              (40, 250, 336, 404, "スプライン (B-spline)"), (348, 250, 620, 404, "Vinokur")]
    for (x0, y0, x1, y1, ttl) in panels:
        box(d, x0, y0, x1, y1, (250, 250, 250))
        ctext(d, (x0 + x1) / 2, y0 + 18, ttl, FS, BLACK)
        cx = (x0 + x1) / 2
        if ttl == "ラグランジュ":
            pxs = [x0 + 40, x0 + 120, x0 + 200, x0 + 250]
            pys = [y1 - 40, y1 - 110, y1 - 60, y1 - 100]
            d.line(list(zip(pxs, pys)), fill=BLUE, width=3, joint="curve")
            for px, py in zip(pxs, pys):
                node(d, px, py, 6, BLUE, BLUE)
            ctext(d, cx, y1 - 16, "指定点を全て通る", FT, GRAY)
        elif ttl == "エルミート":
            pxs = [x0 + 50, x0 + 150, x0 + 220]
            pys = [y1 - 50, y1 - 100, y1 - 55]
            d.line(list(zip(pxs, pys)), fill=BLUE, width=3, joint="curve")
            for px, py in zip(pxs, pys):
                node(d, px, py, 6, BLUE, BLUE)
                d.line((px - 22, py + 8, px + 22, py - 8), fill=RED, width=2)  # 勾配(接線)
            ctext(d, cx, y1 - 16, "位置＋勾配(接線)を指定", FT, GRAY)
        elif ttl.startswith("スプライン"):
            pxs = [x0 + 30, x0 + 90, x0 + 150, x0 + 210, x0 + 260]
            pys = [y1 - 30, y1 - 70, y1 - 45, y1 - 80, y1 - 40]
            for i in range(len(pxs) - 1):
                col = BLUE if i % 2 == 0 else GREEN
                d.line([(pxs[i], pys[i]), (pxs[i + 1], pys[i + 1])], fill=col, width=3)
                node(d, pxs[i], pys[i], 5, "white", BLACK)
            node(d, pxs[-1], pys[-1], 5, "white", BLACK)
            ctext(d, cx, y1 - 16, "区分多項式を滑らかに接続", FT, GRAY)
        else:  # Vinokur
            oy = y1 - 40
            d.line((x0 + 30, oy, x1 - 30, oy), fill=BLACK, width=2)
            n = 9
            for i in range(n + 1):
                t = i / n
                # 両端密・中央疎(tanh的)
                tt = 0.5 + 0.5 * math.tanh(2.4 * (t - 0.5)) / math.tanh(1.2)
                x = x0 + 30 + (x1 - x0 - 60) * tt
                d.line((x, oy - 6, x, oy + 6), fill=BLUE, width=2)
            ctext(d, cx, y1 - 16, "両端の格子幅を指定して分布", FT, GRAY)
    save(im, "t1e4Interpolation")


# ============================================================ 4-6 Transfinite(required)
def f_transfinite():
    im, d = new()
    title(d, "Transfinite補間：計算空間の単位正方形")
    ox, oy = 200, 350
    s = 240
    # 単位正方形[0,1]x[0,1]
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3)
    # 内部=内挿対象(ハッチ)
    for i in range(1, 12):
        y = oy - s * i / 12
        dash(d, ox + 4, y, ox + s - 4, y, LGRAY, 1, 8, 8)
    ctext(d, ox + s / 2, oy - s / 2, "内部＝内挿の対象領域", FT, GRAY)
    # 4辺に格子点分布
    n = 6
    for i in range(n + 1):
        t = i / n
        # 下辺 η=0, 上辺 η=1(両端やや密)
        tt = 0.5 - 0.5 * math.cos(math.pi * t)
        d.line((ox + s * tt, oy - 6, ox + s * tt, oy + 6), fill=BLUE, width=2)
        node(d, ox + s * tt, oy, 4, BLUE, BLUE)
        node(d, ox + s * tt, oy - s, 4, BLUE, BLUE)
        # 左辺 ξ=0, 右辺 ξ=1
        d.line((ox - 6, oy - s * tt, ox + 6, oy - s * tt), fill=GREEN, width=2)
        node(d, ox, oy - s * tt, 4, GREEN, GREEN)
        node(d, ox + s, oy - s * tt, 4, GREEN, GREEN)
    # 軸ラベル
    ctext(d, ox + s / 2, oy + 26, "ξ  (0 → 1)", FT, BLUE)
    ctext(d, ox - 30, oy - s / 2, "η\n(0→1)", FT, GREEN)
    ctext(d, ox, oy + 8, "(0,0)", FT, GRAY, "rm")
    ctext(d, ox + s, oy - s - 12, "(1,1)", FT, GRAY)
    note(d, "4辺に与えた格子点分布から内部を埋める（設定のみ）")
    save(im, "t1e4Transfinite")


# ============================================================ 4-7 ボクセル表現
def f_voxel():
    im, d = new()
    title(d, "ボクセル格子：直交セルによる形状表現")
    # 円形物体を格子で覆う
    ox, oy = 60, 90
    c = 34
    ccx, ccy = ox + 3.2 * c, oy + 3.0 * c
    rr = 2.3 * c
    titles = ["バイナリ(0/1)", "体積率", "距離関数(レベルセット)"]
    for p in range(3):
        bx = 40 + p * 205
        by = 80
        # 6x6 セル
        for i in range(6):
            for j in range(6):
                x0 = bx + i * 28
                y0 = by + j * 28
                cxx, cyy = x0 + 14, y0 + 14
                dist = math.hypot(cxx - (bx + 84), cyy - (by + 84))
                inside = dist < 62
                if p == 0:
                    fill = (210, 225, 245) if inside else "white"
                    d.rectangle((x0, y0, x0 + 28, y0 + 28), outline=LGRAY, width=1, fill=fill)
                    ctext(d, cxx, cyy, "1" if inside else "0", FT, (40, 80, 190) if inside else LGRAY)
                elif p == 1:
                    frac = max(0.0, min(1.0, (62 - dist) / 28 + 0.5))
                    g = int(245 - 120 * frac)
                    d.rectangle((x0, y0, x0 + 28, y0 + 28), outline=LGRAY, width=1, fill=(g, g + 10, 250))
                else:
                    d.rectangle((x0, y0, x0 + 28, y0 + 28), outline=LGRAY, width=1, fill="white")
                    ctext(d, cxx, cyy, str(int((dist - 62) / 14)), FT, GRAY)
        d.ellipse((bx + 84 - 62, by + 84 - 62, bx + 84 + 62, by + 84 + 62), outline=RED, width=2)
        ctext(d, bx + 84, by + 185, titles[p], FT, BLACK)
    note(d, "入力＝三角形パッチ/点群/CT断層。ソルバーはマスク情報・距離情報で形状を認識")
    save(im, "t1e4Voxel")


# ============================================================ 4-8 カットセル/IBM(精度向上)
def f_cutcell():
    im, d = new()
    title(d, "階段状 → カットセル法 → 埋込境界法")
    labels = ["階段状近似", "カットセル法", "埋込境界法(IBM)"]
    subs = ["直交セルの階段", "境界でセルを切断", "外力項で境界条件"]
    def curve(t):  # 共通の曲線境界
        return 70 - 40 * t
    for p in range(3):
        bx = 40 + p * 205
        by, s, n = 90, 24, 5
        # 曲線境界(赤)
        cpts = [(bx + i * (s * n) / 30, by + curve(i / 30) + 30) for i in range(31)]
        for i in range(n):
            for j in range(n):
                x0 = bx + i * s; y0 = by + j * s
                d.rectangle((x0, y0, x0 + s, y0 + s), outline=LGRAY, width=1)
        if p == 0:  # 階段状:境界下のセルを塗る
            for i in range(n):
                cx = bx + i * s + s / 2
                yb = by + curve(i / n * 0.9) + 30
                for j in range(n):
                    y0 = by + j * s
                    if y0 + s / 2 > yb:
                        d.rectangle((bx + i * s, y0, bx + i * s + s, y0 + s), outline=LGRAY, width=1, fill=(215, 225, 245))
        elif p == 1:  # カットセル:曲線でセルを切る
            d.line(cpts, fill=RED, width=3)
            # 小さくカットされたセルを強調
            d.rectangle((bx + 1 * s, by + 2 * s, bx + 2 * s, by + 2 * s + 10), outline=RED, width=2, fill=(255, 225, 225))
            ctext(d, bx + s * n / 2, by + s * n + 22, "小セル→CFL厳しい", FT, RED)
        else:  # IBM:格子点上に力を配分
            d.line(cpts, fill=RED, width=3)
            for i in range(n):
                x = bx + i * s
                yb = by + curve(i / n) + 30
                node(d, x, yb, 4, ORANGE, ORANGE)
            ctext(d, bx + s * n / 2, by + s * n + 22, "格子点へ外力配分", FT, ORANGE)
        if p == 1:
            d.line(cpts, fill=RED, width=3)
        ctext(d, bx + s * n / 2, by + s * n + 2, labels[p], FT, BLACK)
        ctext(d, bx + s * n / 2, by - 8, subs[p], FT, GRAY)
    arrow(d, 165, 210, 250, 210, GRAY, 2, 10)
    arrow(d, 370, 210, 455, 210, GRAY, 2, 10)
    note(d, "右へ行くほど形状表現の精度が向上する")
    save(im, "t1e4CutCell")


# ============================================================ 4-9 デローニ空円条件
def f_delaunay():
    im, d = new()
    title(d, "デローニ分割：空円条件 と 先端前進法")
    # 左：空円条件
    pts = [(90, 300), (210, 320), (170, 170), (300, 250)]
    tri = [pts[0], pts[1], pts[2]]
    d.polygon(tri, outline=BLUE, width=3)
    d.polygon([pts[1], pts[2], pts[3]], outline=BLUE, width=3)
    for p in pts:
        node(d, p[0], p[1], 6, "white", BLACK)
    # 三角形の外接円(tri)
    (x1, y1), (x2, y2), (x3, y3) = tri
    ax = x2 - x1; ay = y2 - y1; bx = x3 - x1; by = y3 - y1
    d2 = 2 * (ax * by - ay * bx)
    ux = (by * (ax * ax + ay * ay) - ay * (bx * bx + by * by)) / d2
    uy = (ax * (bx * bx + by * by) - bx * (ax * ax + ay * ay)) / d2
    cxr, cyr = x1 + ux, y1 + uy
    rr = math.hypot(cxr - x1, cyr - y1)
    d.ellipse((cxr - rr, cyr - rr, cxr + rr, cyr + rr), outline=RED, width=2)
    ctext(d, 195, 355, "外接円の内部に他の節点なし", FT, RED)
    ctext(d, 195, 120, "デローニ分割(空円条件)", FS, BLACK)
    # 右：先端前進法
    d.line((400, 90, 620, 90), fill=BLACK, width=3)
    ctext(d, 510, 74, "境界(フロント)", FT, GRAY)
    base = [(420, 90), (470, 90), (520, 90), (570, 90)]
    for i in range(len(base) - 1):
        apex = ((base[i][0] + base[i + 1][0]) / 2, 90 + 55)
        d.polygon([base[i], base[i + 1], apex], outline=GREEN, width=2)
        node(d, apex[0], apex[1], 5, GREEN, GREEN)
    for p in base:
        node(d, p[0], p[1], 5, "white", BLACK)
    arrow(d, 510, 100, 510, 150, GREEN, 2, 11)
    ctext(d, 510, 175, "先端を内部へ前進", FT, GREEN)
    ctext(d, 510, 210, "アドバンシングフロント法", FS, BLACK)
    save(im, "t1e4Delaunay")


# ============================================================ 4-10 CAD→CFD ワークフロー
def f_cad_clean():
    im, d = new()
    title(d, "CAD → CFD解析格子 作成の流れ")
    steps = [
        "データ形式の変換\n(IGES / STEP / STL)",
        "固体モデル→流体領域\n(ブール演算)",
        "不要データの除去\n(寸法線/補助線/微小穴)",
        "曲面パッチの品質改善\n(歪んだパッチを作り直す)",
    ]
    ys = [110, 195, 280, 365]
    for i, (s, y) in enumerate(zip(steps, ys)):
        fbox(d, 330, y, 420, 60, s, (240, 244, 250))
        if i < 3:
            arrow(d, 330, y + 30, 330, ys[i + 1] - 30, BLACK, 2, 12)
    save(im, "t1e4CadClean")


# ============================================================ 4-11 ハイブリッド非構造格子
def f_unstructured():
    im, d = new()
    title(d, "ハイブリッド格子：壁近傍プリズム＋外側四面体")
    # 物体壁(下)
    ox, x1 = 70, 590
    yw = 340
    hwall(d, ox, x1, yw, side=-1, n=14)  # ハッチ下向き? side=-1上... 壁は下。ここでは物体表面を下辺に
    ctext(d, 330, yw + 18, "物体表面", FT, GRAY)
    # 壁近傍：プリズム層(層状の四角)
    for layer in range(3):
        y0 = yw - (layer + 1) * 26
        y1 = yw - layer * 26
        for i in range(13):
            xx = ox + i * 40
            d.line((xx, y0, xx, y1), fill=BLUE, width=1)
            d.line((ox, y0, x1, y0), fill=BLUE, width=1)
    d.line((ox, yw, x1, yw), fill=BLUE, width=1)
    ctext(d, x1 + 4, yw - 40, "", FT)
    ctext(d, 120, yw - 40, "プリズム層(境界層)", FT, BLUE, "lm")
    # 外側：四面体(三角)
    import random
    random.seed(3)
    ytop = 90
    yb = yw - 3 * 26
    tpts = []
    for i in range(9):
        for j in range(3):
            x = ox + 20 + i * 62 + (j % 2) * 20
            y = ytop + j * ((yb - ytop) / 3) + 8
            tpts.append((x, y))
    # 単純に三角格子を敷く
    for i in range(8):
        for j in range(2):
            x0 = ox + 30 + i * 62
            y0 = ytop + 10 + j * 55
            d.polygon([(x0, y0), (x0 + 62, y0), (x0 + 31, y0 + 55)], outline=GREEN, width=1)
            d.polygon([(x0 + 62, y0), (x0 + 31, y0 + 55), (x0 + 93, y0 + 55)], outline=GREEN, width=1)
    ctext(d, 130, ytop + 2, "四面体(外側領域)", FT, GREEN, "lm")
    note(d, "壁際=層状プリズムで境界層を解像／外側=四面体。構造格子よりメモリ・演算量は多い傾向")
    save(im, "t1e4Unstructured")


# ============================================================ 4-12 3次元要素4種
def f_elements():
    im, d = new()
    title(d, "3次元要素：六面体・四面体・プリズム・ピラミッド")
    _draw_elements(d, roles=True)
    save(im, "t1e4Elements")


def _draw_elements(d, roles=True):
    # 六面体
    _hexa(d, 70, 150)
    ctext(d, 120, 250, "六面体", FS, BLACK)
    if roles: ctext(d, 120, 272, "計算効率が良い", FT, GRAY)
    # 四面体
    _tetra(d, 230, 150)
    ctext(d, 285, 250, "四面体", FS, BLACK)
    if roles: ctext(d, 285, 272, "複雑形状に適合", FT, GRAY)
    # プリズム
    _prism(d, 390, 150)
    ctext(d, 450, 250, "プリズム", FS, BLACK)
    if roles: ctext(d, 450, 272, "壁近傍・境界層向き", FT, GRAY)
    # ピラミッド
    _pyramid(d, 560, 150)
    ctext(d, 595, 250, "ピラミッド", FS, BLACK)
    if roles: ctext(d, 595, 272, "六面体↔四面体の遷移", FT, GRAY)


def _hexa(d, x, y):
    w, h, dx, dy = 70, 70, 32, 22
    d.polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], outline=BLACK, width=2, fill=FILL1)
    d.polygon([(x, y), (x + dx, y - dy), (x + w + dx, y - dy), (x + w, y)], outline=BLACK, width=2, fill=FILL2)
    d.polygon([(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)], outline=BLACK, width=2, fill=FILL3)


def _tetra(d, x, y):
    a = (x, y + 70); b = (x + 80, y + 60); c = (x + 40, y + 78); apex = (x + 38, y - 5)
    for p in [a, b, c]:
        d.line((p[0], p[1], apex[0], apex[1]), fill=BLACK, width=2)
    d.polygon([a, b, c], outline=BLACK, width=2, fill=FILL1)
    d.line((a[0], a[1], b[0], b[1]), fill=BLACK, width=2)


def _prism(d, x, y):
    dx, dy = 30, 20
    a = (x, y + 70); b = (x + 70, y + 70); c = (x + 20, y + 10)
    a2 = (a[0] + dx, a[1] - dy); b2 = (b[0] + dx, b[1] - dy); c2 = (c[0] + dx, c[1] - dy)
    d.polygon([a, b, c], outline=BLACK, width=2, fill=FILL1)
    for p, q in [(a, a2), (b, b2), (c, c2)]:
        d.line((p[0], p[1], q[0], q[1]), fill=BLACK, width=2)
    d.polygon([a2, b2, c2], outline=BLACK, width=2, fill=FILL2)


def _pyramid(d, x, y):
    w, dx, dy = 60, 26, 18
    a = (x, y + 70); b = (x + w, y + 70)
    c = (x + w + dx, y + 70 - dy); e = (x + dx, y + 70 - dy)
    apex = (x + w / 2 + dx / 2, y - 5)
    d.polygon([a, b, c, e], outline=BLACK, width=2, fill=FILL1)
    for p in [a, b, c, e]:
        d.line((p[0], p[1], apex[0], apex[1]), fill=BLACK, width=2)


# ============================================================ 4-13 複雑形状 4方法
def f_complex_domain():
    im, d = new()
    title(d, "複雑形状の解析領域を扱う4方法")
    panels = [(40, 62, 336, 236, "構造格子の組合せ"), (348, 62, 620, 236, "非構造格子(四面体)"),
              (40, 250, 336, 404, "粒子法(格子なし)"), (348, 250, 620, 404, "ボクセル法")]
    for (x0, y0, x1, y1, ttl) in panels:
        box(d, x0, y0, x1, y1, (250, 250, 250))
        ctext(d, (x0 + x1) / 2, y0 + 18, ttl, FS, BLACK)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 8
        if ttl == "構造格子の組合せ":
            for bx, col in [(x0 + 40, (235, 240, 250)), (x0 + 130, (240, 248, 240))]:
                box(d, bx, cy - 40, bx + 90, cy + 40, col)
                for i in range(1, 4):
                    d.line((bx, cy - 40 + i * 20, bx + 90, cy - 40 + i * 20), fill=LGRAY, width=1)
                    d.line((bx + i * 30, cy - 40, bx + i * 30, cy + 40), fill=LGRAY, width=1)
            ctext(d, cx, y1 - 16, "マルチブロック/オーバーセット", FT, GRAY)
        elif ttl.startswith("非構造"):
            for i in range(4):
                for j in range(2):
                    x0t = x0 + 40 + i * 48; y0t = cy - 34 + j * 40
                    d.polygon([(x0t, y0t), (x0t + 48, y0t), (x0t + 24, y0t + 40)], outline=GREEN, width=1)
                    d.polygon([(x0t + 48, y0t), (x0t + 24, y0t + 40), (x0t + 72, y0t + 40)], outline=GREEN, width=1)
            ctext(d, cx, y1 - 16, "四面体で複雑形状に適合", FT, GRAY)
        elif ttl.startswith("粒子"):
            import random
            random.seed(7)
            for _ in range(46):
                px = random.uniform(x0 + 30, x1 - 30); py = random.uniform(y0 + 30, y1 - 26)
                node(d, px, py, 4, BLUE, BLUE)
            ctext(d, cx, y1 - 16, "粒子で流体を表現", FT, GRAY)
        else:
            for i in range(6):
                for j in range(3):
                    x0t = x0 + 60 + i * 30; y0t = cy - 42 + j * 30
                    dist = math.hypot(x0t + 15 - cx, y0t + 15 - cy)
                    fill = (215, 225, 245) if dist < 55 else "white"
                    d.rectangle((x0t, y0t, x0t + 30, y0t + 30), outline=LGRAY, width=1, fill=fill)
            ctext(d, cx, y1 - 16, "直方体セルに形状情報", FT, GRAY)
    save(im, "t1e4ComplexDomain")


# ============================================================ 4-14 双一次写像(required)
def f_jacobian():
    im, d = new()
    title(d, "双一次写像：計算空間 と 物理空間")
    # 左：計算空間の正方形[-1,1]^2
    ox, oy = 70, 355
    s = 200
    d.rectangle((ox, oy - s, ox + s, oy), outline=BLACK, width=3)
    # グリッド線
    for i in range(1, 4):
        d.line((ox + s * i / 4, oy, ox + s * i / 4, oy - s), fill=LGRAY, width=1)
        d.line((ox, oy - s * i / 4, ox + s, oy - s * i / 4), fill=LGRAY, width=1)
    corners = [(ox, oy), (ox + s, oy), (ox + s, oy - s), (ox, oy - s)]
    for k, (cx, cy) in enumerate(corners):
        numnode(d, cx, cy, k + 1, 11, (230, 230, 250), BLUE)
    ctext(d, ox + s / 2, oy + 22, "計算空間 (ξ, η)", FS, BLACK)
    ctext(d, ox, oy + 8, "(-1,-1)", FT, GRAY, "rm")
    ctext(d, ox + s, oy - s - 12, "(1,1)", FT, GRAY)
    # 中央：写像矢印
    arrow(d, 300, 240, 372, 240, BLACK, 3, 14)
    ctext(d, 336, 216, "双一次写像", FT, BLACK)
    # 右：物理空間の4節点四角形(概念的な一般四角形・座標値は描くが答えは描かない)
    rx, ry = 400, 355
    # 節点1(1,1)2(7,3)3(3,5)4(1,9) をスケールして配置
    def P(x, y):
        return (rx + 24 * x, ry - 30 * (y - 1))
    q = [P(1, 1), P(7, 3), P(3, 5), P(1, 9)]
    d.polygon(q, outline=BLUE, width=3)
    for k, (px, py) in enumerate(q):
        numnode(d, px, py, k + 1, 11, (230, 230, 250), BLUE)
    labs = ["(1,1)", "(7,3)", "(3,5)", "(1,9)"]
    offs = [(-6, 16), (16, 6), (16, 0), (-6, -16)]
    for (px, py), lab, (dxx, dyy) in zip(q, labs, offs):
        ctext(d, px + dxx, py + dyy, lab, FT, GRAY, "lm" if dxx >= 0 else "rm")
    ctext(d, rx + 90, ry + 22, "物理空間 (x, y)", FS, BLACK)
    note(d, "正方形の計算空間を4節点四角形へ写す設定（ヤコビアンの値・特異範囲は描かない）")
    save(im, "t1e4Jacobian")


if __name__ == "__main__":
    f_general_transform()
    f_grid_arrangement()
    f_multiblock()
    f_pde_grid()
    f_interpolation()
    f_transfinite()
    f_voxel()
    f_cutcell()
    f_delaunay()
    f_cad_clean()
    f_unstructured()
    f_elements()
    f_complex_domain()
    f_jacobian()
    print("done t1e4 (14)")
