# -*- coding: utf-8 -*-
"""熱流体力学1級 第3章「単相流の計算法2」公式・用語図 19枚。figlibで白地660x420線画。"""
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


def wave(d, x0, x1, yc, amp, k, phase=0.0, col=BLUE, wd=3, n=240):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = yc - amp * math.sin(k * (x - x0) + phase)
        pts.append((x, y))
    d.line(pts, fill=col, width=wd, joint="curve")


# ---- 1. 数値誤差の分類（4種）
def f_errortypes():
    im, d = new()
    title(d, "数値誤差の分類（4つの発生源）")
    panels = [
        (40, 66, 336, 238, "丸め誤差", "3.141592...  ->  3.14", "桁を端数処理して落とす"),
        (348, 66, 620, 238, "打ち切り誤差", "1+x+x²/2+x³/6+...", "無限級数を有限項で切る"),
        (40, 250, 336, 404, "エイリアジング誤差", None, "高波数が低波数へ折り返す"),
        (348, 250, 620, 404, "位相誤差", None, "波の進み位置がずれる（leap-frog）"),
    ]
    for (x0, y0, x1, y1, ttl, mid, sub) in panels:
        box(d, x0, y0, x1, y1, (248, 248, 248))
        ctext(d, (x0 + x1) / 2, y0 + 22, ttl, FS, BLACK)
        cx = (x0 + x1) / 2
        if ttl == "丸め誤差":
            ctext(d, cx, (y0 + y1) / 2 + 6, mid, FS, BLUE)
            ctext(d, cx, y1 - 22, sub, FT, GRAY)
        elif ttl == "打ち切り誤差":
            ctext(d, cx, (y0 + y1) / 2, mid, FS, BLUE)
            d.line((cx + 60, (y0 + y1) / 2 - 12, cx + 60, (y0 + y1) / 2 + 12), fill=RED, width=2)
            ctext(d, cx, y1 - 22, sub, FT, GRAY)
        elif ttl == "エイリアジング誤差":
            wave(d, x0 + 22, x1 - 22, (y0 + y1) / 2, 20, 0.28, col=LGRAY, wd=2)
            wave(d, x0 + 22, x1 - 22, (y0 + y1) / 2, 20, 0.06, col=RED, wd=3)
            ctext(d, cx, y1 - 20, sub, FT, GRAY)
        else:
            wave(d, x0 + 22, x1 - 22, (y0 + y1) / 2, 18, 0.11, 0.0, col=LGRAY, wd=2)
            wave(d, x0 + 22, x1 - 22, (y0 + y1) / 2, 18, 0.11, 1.3, col=RED, wd=3)
            ctext(d, cx, y1 - 20, sub, FT, GRAY)
    save(im, "t1f3ErrorTypes")


# ---- 2. 計測の誤差の定義
def f_measure():
    im, d = new()
    title(d, "計測の誤差 ＝ 測定値 − 真値")
    oy = 250
    ox, ex = 80, 590
    arrow(d, ox, oy, ex + 20, oy, BLACK, 2, 11)
    ctext(d, ex + 30, oy, "値", FS, BLACK, "lm")
    xt, xm = 290, 445
    for x, lab, col, up in [(xt, "真値（推定値）", GREEN, 1), (xm, "測定値", BLUE, 1)]:
        d.line((x, oy - 60, x, oy + 8), fill=col, width=3)
        node(d, x, oy - 60, 6, fill=col, col=col)
        ctext(d, x, oy - 78, lab, FT, col)
    dim(d, xt, oy + 40, xm, oy + 40, "誤差", col=RED)
    ctext(d, (xt + xm) / 2, oy + 64, "＝ 測定値 − 真値", FT, RED)
    note(d, "真値そのものも計測・理論から得た推定値 -> 誤差は厳密には決められない")
    save(im, "t1f3Measure")


# ---- 3. 不確かさ
def f_uncertainty():
    im, d = new()
    title(d, "不確かさ（uncertainty）＝ ばらつきの幅")
    ox, oy = 100, 330
    arrow(d, ox, oy, ox + 470, oy, BLACK, 2, 11)
    ctext(d, ox + 480, oy, "値", FS, BLACK, "lm")
    cx = ox + 235
    sig = 70
    pts = []
    for i in range(0, 471):
        x = ox + i
        y = oy - 190 * math.exp(-((x - cx) ** 2) / (2 * sig ** 2))
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    d.line((cx, oy, cx, oy - 200), fill=GRAY, width=2)
    ctext(d, cx, oy + 20, "中心値", FT, GRAY)
    dim(d, cx - sig, oy - 118, cx + sig, oy - 118, "ばらつき幅", col=RED)
    note(d, "真値との差が決められない -> 結果がどれだけばらつくかで信頼度を表す")
    save(im, "t1f3Uncertainty")


# ---- 4. エイリアジング誤差と除去
def f_aliasing():
    im, d = new()
    title(d, "エイリアジング誤差（高波数の折り返し）")
    ox, oy = 70, 210
    arrow(d, ox, oy, ox + 520, oy, BLACK, 2, 10)
    x1 = ox + 500
    wave(d, ox, x1, oy, 70, 0.30, col=LGRAY, wd=2)
    wave(d, ox, x1, oy, 70, 0.055, col=RED, wd=3)
    # サンプル点（粗い間隔）
    for k in range(0, 11):
        x = ox + k * 50
        y = oy - 70 * math.sin(0.30 * (x - ox))
        node(d, x, y, 5, fill=BLACK, col=BLACK)
    ctext(d, x1 - 40, oy - 96, "真の高波数成分", FT, GRAY, "rm")
    ctext(d, x1 - 40, oy + 96, "見かけの低波数（折り返し）", FT, RED, "rm")
    ctext(d, 330, 330, "擬スペクトル法の非線形項で発生", FT, BLACK)
    note(d, "除去法：パディング法・トランケーション法・フェイズシフト法")
    save(im, "t1f3Aliasing")


# ---- 5. 不等間隔格子の1階差分
def f_nonuniform():
    im, d = new()
    title(d, "不等間隔格子の1階差分（点3まわり）")
    oy = 240
    ox = 90
    x2, x3, x4 = ox + 90, ox + 250, ox + 470   # Δ2=160, Δ3=220 (不等)
    d.line((ox, oy, ox + 520, oy), fill=BLACK, width=2)
    for x, lab in [(x2, "φ2"), (x3, "φ3"), (x4, "φ4")]:
        d.line((x, oy - 6, x, oy + 6), fill=BLACK, width=2)
        node(d, x, oy - 60, 7)
        d.line((x, oy - 53, x, oy), fill=GRAY, width=1)
        ctext(d, x, oy - 80, lab, FS, BLACK)
    ctext(d, x3, oy + 28, "中央点（点3）", FT, BLUE)
    dim(d, x2, oy + 62, x3, oy + 62, "Δ2", col=GRAY)
    dim(d, x3, oy + 62, x4, oy + 62, "Δ3", col=GRAY)
    note(d, "左右の間隔が違う -> 重みが非対称・誤差項は Δ2Δ3/6 の積で残る")
    save(im, "t1f3NonUniform")


# ---- 6. 精度次数（中心差分は2次）
def f_order():
    im, d = new()
    title(d, "精度次数：誤差 ∝ Δ²（2次精度）")
    ox, oy = 110, 340
    axes(d, ox, oy, 440, 260, "格子幅 Δ（対数）", "誤差（対数）")
    # slope-2 straight line on log-log
    x0, y0 = ox + 40, oy - 40
    x1, y1 = ox + 380, oy - 220
    d.line((x0, y0, x1, y1), fill=BLUE, width=3)
    ctext(d, x1 - 6, y1 - 16, "傾き 2", FS, BLUE, "rm")
    # slope triangle
    tx, ty = ox + 150, oy - 95
    d.line((tx, ty, tx + 80, ty), fill=GRAY, width=2)
    d.line((tx + 80, ty, tx + 80, ty - 80), fill=GRAY, width=2)
    ctext(d, tx + 40, ty + 14, "1", FT, GRAY)
    ctext(d, tx + 96, ty - 40, "2", FT, GRAY)
    note(d, "Δを半分にすると誤差は約 1/4（2次精度）。次数が高いほど誤差が小さい")
    save(im, "t1f3Order")


# ---- 7. スペクトル法（直交関数系の重ね合わせ）
def f_spectral():
    im, d = new()
    title(d, "スペクトル法：解＝直交関数の重ね合わせ")
    # target curve
    ox = 60
    wave(d, ox, ox + 150, 130, 34, 0.05, col=BLUE, wd=3)
    ctext(d, ox + 75, 82, "解 f(x)", FT, BLUE)
    ctext(d, ox + 175, 130, "＝", F, BLACK)
    modes = [(ox + 210, 0.05, "a1 φ1"), (ox + 350, 0.11, "a2 φ2"), (ox + 490, 0.17, "a3 φ3")]
    for i, (mx, k, lab) in enumerate(modes):
        wave(d, mx, mx + 110, 130, 26, k, col=BLACK, wd=2)
        ctext(d, mx + 55, 82, lab, FT, BLACK)
        if i < 2:
            ctext(d, mx + 128, 130, "＋", F, BLACK)
    ctext(d, ox + 600, 130, "…", F, BLACK)
    fbox(d, 330, 250, 560, 56, "試行関数＝直交関数系（フーリエ・チェビシェフ・ルジャンドル）", (240, 240, 248), FS)
    note(d, "重み付き残差法で係数を決める。高精度 -> 乱流DNSに用いる")
    save(im, "t1f3Spectral")


# ---- 8. チャネル流DNS（方向で級数を使い分け）
def f_channel():
    im, d = new()
    title(d, "チャネル流DNS：方向で級数を使い分け")
    x0, x1 = 90, 570
    yt, yb = 120, 320
    hwall(d, x0, x1, yt, side=1)
    hwall(d, x0, x1, yb, side=-1)
    # velocity profile (wall-normal)
    xc = 250
    pts = []
    for i in range(0, 41):
        y = yt + (yb - yt) * i / 40
        eta = (y - (yt + yb) / 2) / ((yb - yt) / 2)
        u = 70 * (1 - eta ** 2)
        pts.append((xc + u, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # wall-normal arrow -> Chebyshev
    arrow(d, 470, yb - 6, 470, yt + 6, GREEN, 3, 12)
    ctext(d, 500, (yt + yb) / 2, "壁垂直方向\nチェビシェフ級数", FT, GREEN, "lm")
    # streamwise arrow -> Fourier
    arrow(d, x0 + 20, 360, x1 - 20, 360, ORANGE, 3, 12)
    ctext(d, (x0 + x1) / 2, 384, "壁平行方向：フーリエ級数（周期境界・十分発達を仮定）", FT, ORANGE)
    ctext(d, (x0 + x1) / 2, yt - 22, "壁", FT, GRAY)
    save(im, "t1f3Channel")


# ---- 9. 陽解法（Adams-Bashforth）既知2点から外挿
def f_adamsbashforth():
    im, d = new()
    title(d, "陽解法（Adams-Bashforth）：既知2点から外挿")
    ox, oy = 90, 330
    axes(d, ox, oy, 470, 250, "t", "u")
    xa, xb, xc = ox + 90, ox + 230, ox + 370
    ya, yb = oy - 90, oy - 150      # 既知
    yc = oy - 245                   # 外挿先
    # 既知2点の傾きで外挿（点線）
    d.line((xa, ya, xb, yb), fill=BLACK, width=3)
    dash(d, xb, yb, xc, yc, col=RED, wd=3)
    node(d, xa, ya, 7, fill=BLACK, col=BLACK)
    node(d, xb, yb, 7, fill=BLACK, col=BLACK)
    node(d, xc, yc, 8, fill="white", col=RED)
    for x, lab in [(xa, "t n−1"), (xb, "t n"), (xc, "t n+1")]:
        d.line((x, oy - 4, x, oy + 4), fill=BLACK, width=2)
        ctext(d, x, oy + 18, lab, FT, BLACK)
    ctext(d, xa - 6, ya - 16, "既知 H n−1", FT, GRAY, "rm")
    ctext(d, xb - 6, yb - 16, "既知 H n", FT, GRAY, "rm")
    ctext(d, xc, yc - 20, "未知 u n+1", FT, RED)
    ctext(d, 330, 300, "傾き ＝ 3/2 H n − 1/2 H n−1（行列を解かず前進）", FT, BLUE)
    save(im, "t1f3AdamsBashforth")


# ---- 10. 陰解法（Crank-Nicolson）n と n+1 の平均（台形則）
def f_cranknicolson():
    im, d = new()
    title(d, "陰解法（Crank-Nicolson）：n と n+1 の平均（台形則）")
    ox, oy = 100, 330
    axes(d, ox, oy, 460, 250, "t", "H")
    xn, xn1 = ox + 130, ox + 330
    yn, yn1 = oy - 90, oy - 190
    # 台形（H^n と H^{n+1} を結ぶ）
    d.polygon([(xn, oy), (xn, yn), (xn1, yn1), (xn1, oy)], outline=BLUE, width=3, fill=(235, 240, 250))
    node(d, xn, yn, 7, fill=BLACK, col=BLACK)
    node(d, xn1, yn1, 7, fill="white", col=RED)
    for x, lab, yl in [(xn, "t n", yn), (xn1, "t n+1", yn1)]:
        d.line((x, oy - 4, x, oy + 4), fill=BLACK, width=2)
        ctext(d, x, oy + 18, lab, FT, BLACK)
    ctext(d, xn - 8, yn - 16, "H n（既知）", FT, GRAY, "rm")
    ctext(d, xn1 + 8, yn1 - 16, "H n+1（未知）", FT, RED, "lm")
    # 平均レベル
    ym = (yn + yn1) / 2
    dash(d, xn, ym, xn1, ym, col=GREEN, wd=2)
    ctext(d, (xn + xn1) / 2, ym - 16, "平均 (H n + H n+1)/2", FT, GREEN)
    ctext(d, 330, 300, "未知が両辺に入る -> 連立を解くが安定・2次精度", FT, BLUE)
    save(im, "t1f3CrankNicolson")


# ---- 11. GSMAC有限要素法（同時緩和の反復）
def f_gsmac():
    im, d = new()
    title(d, "GSMAC-FEM：速度・圧力の同時緩和（反復）")
    fbox(d, 175, 110, 230, 54, "予測速度\n（対流・粘性）", (240, 240, 248))
    fbox(d, 485, 110, 250, 54, "優対角ポアソン\n-> 修正速度ポテンシャル φ", (240, 248, 240))
    fbox(d, 485, 250, 250, 54, "速度・圧力を修正", (248, 240, 240))
    fbox(d, 175, 250, 230, 60, "div u < 基準値 ?", (250, 250, 232))
    arrow(d, 290, 110, 358, 110, BLACK, 3, 12)
    arrow(d, 485, 138, 485, 222, BLACK, 3, 12)
    arrow(d, 358, 250, 292, 250, BLACK, 3, 12)
    # loop back (yes / no)
    arrow(d, 175, 220, 175, 138, GREEN, 3, 12)
    ctext(d, 158, 180, "No（反復）", FT, GREEN, "rm")
    arrow(d, 175, 282, 175, 360, RED, 3, 12)
    ctext(d, 195, 340, "Yes -> 収束", FT, RED, "lm")
    note(d, "非対角成分を記憶せず（対角・集中質量・離散ナブラのみ）-> 省メモリ・高速")
    save(im, "t1f3Gsmac")


# ---- 12. CIP法（値と勾配の両方を運ぶ）
def f_cip():
    im, d = new()
    title(d, "CIP法：値 f と勾配 ∂f/∂x の両方を運ぶ")
    ox, oy = 90, 300
    axes(d, ox, oy, 470, 210, "x", "f")
    # 急な分布（なまりにくい）
    xs = [ox + 40, ox + 130, ox + 220, ox + 310, ox + 400]
    ys = [oy - 30, oy - 40, oy - 150, oy - 160, oy - 165]
    d.line(list(zip(xs, ys)), fill=BLUE, width=3, joint="curve")
    n = len(xs)
    for i in range(n):
        x, y = xs[i], ys[i]
        node(d, x, y, 6, fill=BLUE, col=BLUE)
        # 勾配（局所の接線方向）
        j0 = max(0, i - 1); j1 = min(n - 1, i + 1)
        slope = (ys[j1] - ys[j0]) / (xs[j1] - xs[j0])
        hx = 24
        d.line((x - hx, y - slope * hx, x + hx, y + slope * hx), fill=RED, width=2)
    arrow(d, ox + 120, oy + 30, ox + 320, oy + 30, GRAY, 3, 12)
    ctext(d, ox + 220, oy + 50, "移流", FT, GRAY)
    ctext(d, ox + 300, oy - 200, "勾配（赤）も変数に持つ", FT, RED)
    note(d, "値と勾配を同時に移流 -> 急な分布もなまりにくい。係数は陽的に決定（行列不要）")
    save(im, "t1f3Cip")


# ---- 13. 流体構造連成（弱連成・強連成）
def f_fsi():
    im, d = new()
    title(d, "流体構造連成：弱連成 と 強連成")
    # 界面
    ix = 330
    box(d, 70, 90, ix, 250, (235, 240, 250))
    box(d, ix, 90, 590, 250, (245, 236, 236))
    ctext(d, 200, 110, "流体系", FS, BLUE)
    ctext(d, 460, 110, "構造系", FS, RED)
    d.line((ix, 90, ix, 250), fill=BLACK, width=3)
    ctext(d, ix, 268, "界面", FT, GRAY)
    # 弱連成：界面で交換＋反復
    arrow(d, ix - 12, 165, ix - 70, 165, BLUE, 3, 11)
    arrow(d, ix + 12, 195, ix + 70, 195, RED, 3, 11)
    ctext(d, ix, 150, "交換", FT, GRAY)
    fbox(d, 200, 330, 250, 54, "弱連成：別々に解いて\n界面で交換・反復", (240, 240, 248), FS, BLUE)
    fbox(d, 470, 330, 250, 54, "強連成：全体を1つの\nマトリックスで直接解く", (248, 240, 240), FS, RED)
    note(d, "弱連成＝柔軟・大規模向き（緩和パラメータ） / 強連成＝頑健・大容量")
    save(im, "t1f3Fsi")


# ---- 14. 界面条件（運動学的・動力学的）
def f_interface():
    im, d = new()
    title(d, "界面条件：運動学的条件 と 動力学的条件")
    ix = 330
    box(d, 70, 80, ix, 360, (235, 240, 250))
    box(d, ix, 80, 590, 360, (245, 236, 236))
    ctext(d, 195, 100, "流体", FS, BLUE)
    ctext(d, 460, 100, "構造物", FS, RED)
    d.line((ix, 80, ix, 360), fill=BLACK, width=3)
    ctext(d, ix, 66, "界面", FT, GRAY)
    # 運動学的：法線速度が一致
    y1 = 175
    arrow(d, ix - 70, y1, ix - 8, y1, BLUE, 3, 12)
    arrow(d, ix + 8, y1, ix + 70, y1, RED, 3, 12)
    ctext(d, ix, y1 - 24, "運動学的条件", FT, BLACK)
    ctext(d, ix, y1 + 22, "速度(変位)の法線成分が一致", FT, GRAY)
    # 動力学的：トラクションがつり合う
    y2 = 290
    arrow(d, ix - 8, y2, ix - 70, y2, BLUE, 3, 12)
    arrow(d, ix + 8, y2, ix + 70, y2, RED, 3, 12)
    ctext(d, ix, y2 - 24, "動力学的条件", FT, BLACK)
    ctext(d, ix, y2 + 22, "トラクション（応力）がつり合う", FT, GRAY)
    save(im, "t1f3Interface")


# ---- 15. スタッガード格子（p中心・u,v面）
def f_staggered():
    im, d = new()
    title(d, "スタッガード格子：圧力はセル中心・速度はセル面")
    ox, oy = 160, 110
    s = 130
    # 2x2 セル格子線
    for i in range(3):
        d.line((ox, oy + i * s, ox + 2 * s, oy + i * s), fill=LGRAY, width=2)
        d.line((ox + i * s, oy, ox + i * s, oy + 2 * s), fill=LGRAY, width=2)
    # 圧力：セル中心
    for cx in (ox + s / 2, ox + 1.5 * s):
        for cy in (oy + s / 2, oy + 1.5 * s):
            node(d, cx, cy, 8, fill=(230, 230, 250), col=BLUE)
    ctext(d, ox + s / 2, oy + s / 2 - 22, "p", FT, BLUE)
    ctext(d, ox + s / 2, oy + s / 2 + 22, "i,j", FT, GRAY)
    # u：縦セル面（水平矢印）
    for fx in (ox, ox + s, ox + 2 * s):
        arrow(d, fx - 22, oy + s / 2, fx + 22, oy + s / 2, RED, 2, 10)
    ctext(d, ox + s + 30, oy + s / 2 - 18, "u  i+1/2,j", FT, RED, "lm")
    # v：横セル面（鉛直矢印）
    for fy in (oy, oy + s, oy + 2 * s):
        arrow(d, ox + 1.5 * s, fy + 22, ox + 1.5 * s, fy - 22, GREEN, 2, 10)
    ctext(d, ox + 1.5 * s + 16, oy + s + 30, "v  i,j+1/2", FT, GREEN, "lm")
    note(d, "定義点を半格子ずらす -> 隣どうしの圧力差で駆動・圧力振動（市松模様）を防ぐ")
    save(im, "t1f3Staggered")


# ---- 16. スタッガード格子の圧力ポアソン（5点ステンシル）
def f_poissonstag():
    im, d = new()
    title(d, "圧力ポアソン方程式（スタッガード・5点）")
    cx, cy = 300, 220
    s = 96
    P = [(cx, cy, "p i,j"), (cx + s, cy, "p i+1,j"), (cx - s, cy, "p i−1,j"),
         (cx, cy - s, "p i,j+1"), (cx, cy + s, "p i,j−1")]
    for (x, y, _) in P[1:]:
        d.line((cx, cy, x, y), fill=BLACK, width=2)
    for i, (x, y, lab) in enumerate(P):
        node(d, x, y, 10, fill=(230, 230, 250) if i == 0 else "white", col=BLUE)
        oy2 = -22 if y <= cy else 22
        ctext(d, x, y + oy2, lab, FT, BLUE)
    # 半格子ずれ速度（面）
    for (mx, my, lab, col) in [((cx + cx + s) / 2, cy, "u i+1/2,j", RED),
                               ((cx + cx - s) / 2, cy, "u i−1/2,j", RED),
                               (cx, (cy + cy - s) / 2, "v i,j+1/2", GREEN),
                               (cx, (cy + cy + s) / 2, "v i,j−1/2", GREEN)]:
        node(d, mx, my, 5, fill=col, col=col)
    ctext(d, cx + s + 40, cy + 40, "面上の速度", FT, RED, "lm")
    node(d, cx + s + 26, cy + 40, 5, fill=RED, col=RED)
    ctext(d, cx + s + 40, cy + 64, "（半格子ずれ）", FT, GREEN, "lm")
    node(d, cx + s + 26, cy + 64, 5, fill=GREEN, col=GREEN)
    note(d, "左辺＝Δ基準の正しいラプラシアン / 右辺＝半格子ずれ速度と F の発散")
    save(im, "t1f3PoissonStag")


# ---- 17. Roeの近似リーマン解法（Property U）
def f_roe():
    im, d = new()
    title(d, "Roeの近似リーマン解法（左右状態の平均行列）")
    oy = 210
    ix = 330
    d.line((ix, 110, ix, 300), fill=BLACK, width=3)
    ctext(d, ix, 92, "界面", FT, GRAY)
    # 左右状態（ステップ）
    d.line((110, oy - 70, ix, oy - 70), fill=BLUE, width=4)
    d.line((ix, oy + 40, 560, oy + 40), fill=RED, width=4)
    ctext(d, 200, oy - 92, "左状態 Q_L", FS, BLUE)
    ctext(d, 460, oy + 66, "右状態 Q_R", FS, RED)
    node(d, ix, oy - 70, 6, fill=BLUE, col=BLUE)
    node(d, ix, oy + 40, 6, fill=RED, col=RED)
    fbox(d, 330, 345, 560, 48, "F(Q_R) − F(Q_L) ＝ A(Q_R,Q_L)（Q_R − Q_L）", (240, 240, 248), FS)
    ctext(d, 330, 150, "平均ヤコビ行列 A で流束差＝状態差", FT, BLACK)
    note(d, "Property U を満たす平均行列（衝撃波を正しく捕獲）。単純算術平均は不可")
    save(im, "t1f3Roe")


# ---- 18. 1次元オイラー方程式（x-t平面の3特性線）
def f_euler():
    im, d = new()
    title(d, "1次元オイラー方程式：x-t平面の3特性線")
    ox, oy = 330, 360
    axes(d, ox, oy, 250, 280, "x", "t")
    d.line((ox - 250, oy, ox, oy), fill=BLACK, width=2)  # 左側のx軸も延長
    arrow(d, ox, oy, ox - 250, oy, BLACK, 2, 11)
    # 3本の特性線（傾き=1/速度、原点から扇形）
    lines = [(-150, "λ = u − a", BLUE), (-20, "λ = u", GREEN), (150, "λ = u + a", RED)]
    top = oy - 250
    for dxtop, lab, col in lines:
        xt = ox + dxtop
        d.line((ox, oy, xt, top), fill=col, width=3)
        ctext(d, xt + (18 if dxtop >= 0 else -18), top - 10, lab, FT, col,
              "lm" if dxtop >= 0 else "rm")
    ctext(d, ox, oy - 130, "3つの特性速度\nu, u−a, u+a", FT, BLACK)
    note(d, "双曲型：ヤコビ行列の固有値 u, u−a, u+a。符号で上流側を選び風上化")
    save(im, "t1f3Euler")


# ---- 19. 理想気体の圧力（全エネルギーの分解）
def f_idealgas():
    im, d = new()
    title(d, "理想気体の圧力：全エネルギーの分解")
    # 積み上げバー：全エネルギー e = 内部 + 運動
    bx = 130
    top = 110
    h_int = 150
    h_kin = 90
    w = 120
    box(d, bx, top, bx + w, top + h_int, (235, 240, 250))
    ctext(d, bx + w / 2, top + h_int / 2, "内部\nエネルギー", FS, BLUE)
    box(d, bx, top + h_int, bx + w, top + h_int + h_kin, (245, 236, 236))
    ctext(d, bx + w / 2, top + h_int + h_kin / 2, "運動 ρu²/2", FS, RED)
    dim(d, bx - 34, top, bx - 34, top + h_int + h_kin, "全エネルギー e", col=GRAY)
    # 内部エネルギー -> 圧力
    arrow(d, bx + w + 20, top + h_int / 2, bx + w + 130, top + h_int / 2, BLUE, 3, 13)
    fbox(d, 495, top + h_int / 2, 300, 60,
         "p ＝ (γ−1) × 内部エネルギー\n＝ (γ−1)(e − ρu²/2)", (240, 240, 248), FS)
    note(d, "全エネルギーから運動エネルギーを引いた内部エネルギーに (γ−1) を掛ける＝圧力")
    save(im, "t1f3IdealGas")


if __name__ == "__main__":
    f_errortypes()
    f_measure()
    f_uncertainty()
    f_aliasing()
    f_nonuniform()
    f_order()
    f_spectral()
    f_channel()
    f_adamsbashforth()
    f_cranknicolson()
    f_gsmac()
    f_cip()
    f_fsi()
    f_interface()
    f_staggered()
    f_poissonstag()
    f_roe()
    f_euler()
    f_idealgas()
    print("done 19")
