# -*- coding: utf-8 -*-
"""熱流体力学1級 第22章「乱流火炎」公開前レビュー用の図(t1e22*)を描画。
白地660x420・黒線画。条件図(Ansなし)には答え・数値・結論を描かない。
Ans図(末尾Ans)・回答後図には答え・数値を描いてよい。
豆腐回避のためギリシャ文字/添字はプレーン表記へ(S_T, S_L, u', l_F, Ka, Da, Z 等)。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- 共通ヘルパ ----
def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


# ============================================================
# 22-1  t1e22TurbFlameSpeed  (回答後図・上書き・直線)
#   S_T/S_L = 1 + 2(u'/S_L)
# ============================================================
def t1e22TurbFlameSpeed():
    im, d = new(); title(d, "乱流燃焼速度  S_T/S_L = 1 + 2(u'/S_L)  (直線)")
    ox, oy, xl, yl = 120, 355, 460, 265
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "u'/S_L", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "S_T/S_L", FS, BLACK, "rm")
    xmax, ymax = 5.0, 10.0
    def X(u): return ox + (u / xmax) * xl
    def Y(v): return oy - (v / ymax) * yl
    # 目盛
    for u in range(0, 6):
        dashed(d, X(u), oy, X(u), oy + 4, GRAY, 1, 3, 3)
        ctext(d, X(u), oy + 15, str(u), FT, GRAY)
    for v in range(0, 11, 2):
        ctext(d, ox - 12, Y(v), str(v), FT, GRAY, "rm")
    # 直線 S_T/S_L = 1 + 2(u'/S_L)  (切片1, 傾き2)
    d.line((X(0), Y(1), X(4.5), Y(1 + 2 * 4.5)), fill=BLUE, width=3)
    ctext(d, X(1.6), Y(1 + 2 * 1.6) - 16, "S_T/S_L = 1 + 2(u'/S_L)", FT, BLUE, "lm")
    # 点(4, 9)
    node(d, X(4), Y(9), 6, fill=RED, col=RED)
    dashed(d, X(4), oy, X(4), Y(9), LGRAY, 1, 6, 5)
    dashed(d, ox, Y(9), X(4), Y(9), LGRAY, 1, 6, 5)
    ctext(d, X(4) - 10, Y(9) - 10, "(4, 9)", FT, RED, "rm")
    ctext(d, X(4) - 10, Y(9) + 10, "S_T = 4.5 m/s", FT, RED, "rm")
    note(d, "べき指数 b=1 なので S_T/S_L は u'/S_L の直線. (4,9)で S_T=9*S_L=4.5 m/s")
    save(im, "t1e22TurbFlameSpeed")


# ---- Borghi/Peters ダイアグラム共通描画 ----
def _borghi_axes(d):
    ox, oy, xl, yl = 130, 350, 450, 275
    # x: l/l_F = 10^0 .. 10^4 , y: u'/S_L = 10^-1 .. 10^3
    xlo, xhi = 0, 4
    ylo, yhi = -1, 3
    arrow(d, ox, oy, ox + xl + 18, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 24, oy, "l/l_F", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 12, BLACK, 2, 11)
    ctext(d, ox - 10, oy - yl - 14, "u'/S_L", FS, BLACK, "rm")
    def X(lx): return ox + (lx - xlo) / (xhi - xlo) * xl
    def Y(ly): return oy - (ly - ylo) / (yhi - ylo) * yl
    # 対数目盛(10のべき)
    for lx in range(xlo, xhi + 1):
        dashed(d, X(lx), oy, X(lx), oy + 4, GRAY, 1, 3, 3)
        ctext(d, X(lx), oy + 15, "10^%d" % lx, FT, GRAY)
    for ly in range(ylo, yhi + 1):
        ctext(d, ox - 12, Y(ly), "10^%d" % ly, FT, GRAY, "rm")
    return ox, oy, xl, yl, xlo, xhi, ylo, yhi, X, Y


def _borghi_boundaries(d, X, Y, xlo, xhi, ylo, yhi):
    # u'/S_L = 1 (層流/しわ状 境界)
    dashed(d, X(xlo), Y(0), X(xhi), Y(0), GRAY, 2, 9, 6)
    # Re_t = 1 : u'/S_L = (l/l_F)^{-1}  -> log y = -log x  (傾き-1)
    d.line((X(xlo), Y(-xlo), X(xhi), Y(-xhi)), fill=GREEN, width=2)
    ctext(d, X(0.55), Y(-0.55) + 12, "Re_t=1", FT, GREEN, "lm")
    # Ka = 1 : u'/S_L = (l/l_F)^{1/3} -> log y = (1/3) log x  (傾き1/3)
    d.line((X(xlo), Y(xlo / 3.0), X(xhi), Y(xhi / 3.0)), fill=RED, width=2)
    ctext(d, X(3.1), Y(3.1 / 3.0) - 12, "Ka=1", FT, RED, "lm")
    # Ka = 100 : u'/S_L = 100^{2/3} (l/l_F)^{1/3} -> +2/3*2? log y=(1/3)log x + (2/3)*2
    #   log10(100^{2/3}) = 4/3 ; 傾き1/3で上方シフト
    b = 4.0 / 3.0
    d.line((X(xlo), Y(xlo / 3.0 + b), X(xhi), Y(xhi / 3.0 + b)), fill=RED, width=2)
    ctext(d, X(3.1), Y(3.1 / 3.0 + b) - 12, "Ka=100", FT, RED, "lm")


# ============================================================
# 22-2  t1e22RegimeMap  (回答後図・上書き)  Borghi/Peters図
# ============================================================
def t1e22RegimeMap():
    im, d = new(); title(d, "乱流燃焼レジーム図 (Borghi/Peters, 両対数)")
    ox, oy, xl, yl, xlo, xhi, ylo, yhi, X, Y = _borghi_axes(d)
    _borghi_boundaries(d, X, Y, xlo, xhi, ylo, yhi)
    # 領域名(Ka数境界で区切る)
    ctext(d, X(3.4), Y(-0.7), "しわ状火炎", FT, BLACK, "mm")
    ctext(d, X(3.4), Y(-0.7) + 15, "(wrinkled)", FT, GRAY, "mm")
    ctext(d, X(2.6), Y(0.35), "コルゲート火炎(corrugated)", FT, BLACK, "mm")
    ctext(d, X(2.6), Y(1.35), "薄い反応帯(thin reaction zone)", FT, BLACK, "mm")
    ctext(d, X(1.7), Y(2.55), "分断/分散反応(broken/distributed)", FT, BLACK, "mm")
    ctext(d, X(0.55), Y(2.4), "非乱流", FT, GRAY, "mm")
    note(d, "Ka境界(傾き1/3)で領域分け. Ka propto (l/l_F)^{-1/2} に整合する斜め境界")
    save(im, "t1e22RegimeMap")


# ============================================================
# 22-3  t1e22VesselFlame  (条件図に作り直し・答えバレ除去)
#   容器と点火位置・与件のみ。火炎面形状は描かない。
# ============================================================
def t1e22VesselFlame():
    im, d = new(); title(d, "横向き円筒容器の定容燃焼  条件(火炎面形状は問う)")
    # 横向き円筒容器 30mm(径) x 100mm(長さ)
    x0, x1 = 160, 520          # 長さ100mm
    ymid = 235
    ry = 60                    # 径30mm(見かけ半径)
    # 円筒胴(矩形+左右端の楕円)
    d.rectangle((x0, ymid - ry, x1, ymid + ry), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((x0 - 18, ymid - ry, x0 + 18, ymid + ry), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((x1 - 18, ymid - ry, x1 + 18, ymid + ry), outline=BLACK, width=3, fill="white")
    # 点火位置 Ig(左端)
    node(d, x0, ymid, 7, fill=RED, col=RED)
    ctext(d, x0 - 6, ymid - ry - 16, "Ig (端で点火)", FT, RED, "mm")
    # 寸法
    dim(d, x0, ymid + ry + 30, x1, ymid + ry + 30, "長さ 100 mm", col=GRAY)
    dim(d, x1 + 40, ymid - ry, x1 + 40, ymid + ry, "径 30 mm", col=GRAY)
    # 与件(混合気条件)
    ctext(d, 330, 112, "当量比1のメタン-空気予混合気", FT, BLUE)
    ctext(d, 330, 132, "初圧 1 MPa / 初温 600 K / 壁温 300 K", FT, BLUE)
    note(d, "端Igから燃え広がるときの火炎面形状の変化は問題で問う(ここでは描かない)")
    save(im, "t1e22VesselFlame")


# ============================================================
# 22-3 Ans  t1e22VesselFlameAns  火炎面の変化(球面->平面->凹)
# ============================================================
def t1e22VesselFlameAns():
    im, d = new(); title(d, "定容燃焼の火炎面変化  球面->平面->管端で凹 (Ans)")
    x0, x1 = 160, 560
    ymid = 235
    ry = 62
    d.rectangle((x0, ymid - ry, x1, ymid + ry), outline=BLACK, width=3, fill="white")
    d.ellipse((x0 - 16, ymid - ry, x0 + 16, ymid + ry), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((x1 - 16, ymid - ry, x1 + 16, ymid + ry), outline=BLACK, width=3, fill="white")
    node(d, x0, ymid, 6, fill=RED, col=RED)
    ctext(d, x0, ymid - ry - 14, "Ig", FT, RED)
    # 等時刻の火炎面: 近端=球面(円弧) -> 中央=ほぼ平面 -> 管端=中央が凹
    # 1) 球面(半径小)
    for R in (55, 100):
        pts = []
        for k in range(-40, 41):
            th = k / 40 * 1.15
            px = x0 + R * math.cos(th)
            py = ymid + R * math.sin(th)
            if ymid - ry + 2 <= py <= ymid + ry - 2:
                pts.append((px, py))
        if len(pts) > 1:
            d.line(pts, fill=RED, width=2, joint="curve")
    ctext(d, x0 + 70, ymid - ry - 12, "球面", FT, RED, "mm")
    # 2) 中央=ほぼ平面(縦線を少し湾曲)
    for xf in (320, 380):
        pts = []
        for k in range(-40, 41):
            t = k / 40
            py = ymid + t * (ry - 4)
            px = xf + 10 * (1 - t * t)      # わずかに前方湾曲
            pts.append((px, py))
        d.line(pts, fill=RED, width=2, joint="curve")
    ctext(d, 350, ymid - ry - 12, "平面", FT, RED, "mm")
    # 3) 管端(右)=中央が凹む
    xf = 480
    pts = []
    for k in range(-40, 41):
        t = k / 40
        py = ymid + t * (ry - 4)
        px = xf + 26 * (t * t)              # 中央が後退=凹
        pts.append((px, py))
    d.line(pts, fill=RED, width=3, joint="curve")
    ctext(d, xf + 34, ymid - ry - 12, "管端で凹", FT, RED, "mm")
    note(d, "点火直後は球面, 壁で拘束され平面化, 管端到達時は壁近傍が先行し中央がやや凹む")
    save(im, "t1e22VesselFlameAns")


# ============================================================
# 22  t1e22BorghiDiagramAns  点(9,9)をプロット, Ka=9 薄い反応帯
# ============================================================
def t1e22BorghiDiagramAns():
    im, d = new(); title(d, "Borghi図に動作点  (l/l_F,u'/S_L)=(9,9), Ka=9 (Ans)")
    ox, oy, xl, yl, xlo, xhi, ylo, yhi, X, Y = _borghi_axes(d)
    _borghi_boundaries(d, X, Y, xlo, xhi, ylo, yhi)
    # 領域名 A..E
    ctext(d, X(3.4), Y(-0.7), "A しわ状", FT, BLACK, "mm")
    ctext(d, X(2.7), Y(0.30), "B コルゲート", FT, BLACK, "mm")
    ctext(d, X(2.7), Y(1.30), "C 薄い反応帯", FT, BLACK, "mm")
    ctext(d, X(1.7), Y(2.55), "D 分断/分散反応", FT, BLACK, "mm")
    ctext(d, X(0.55), Y(2.4), "E 非乱流", FT, GRAY, "mm")
    # 点 (l/l_F, u'/S_L) = (9,9) -> log10(9)=0.954
    lg = math.log10(9)
    node(d, X(lg), Y(lg), 7, fill=RED, col=RED)
    dashed(d, X(lg), oy, X(lg), Y(lg), LGRAY, 1, 6, 5)
    dashed(d, ox, Y(lg), X(lg), Y(lg), LGRAY, 1, 6, 5)
    ctext(d, X(lg) + 10, Y(lg) - 8, "(9, 9)  Ka=9", FT, RED, "lm")
    ctext(d, X(lg) + 10, Y(lg) + 12, "-> C 薄い反応帯", FT, RED, "lm")
    note(d, "Ka=9(1<Ka<100)で薄い反応帯. Ka_delta=1=火炎予熱帯が最小渦で乱される境界")
    save(im, "t1e22BorghiDiagramAns")


# ============================================================
# 22  t1e22MixLayerPdfAns  平面せん断混合層の各点のP(Z)
# ============================================================
def t1e22MixLayerPdfAns():
    im, d = new(); title(d, "平面せん断混合層  各点の確率密度 P(Z) (Ans)")
    # 上=fuel(Z=1), 下=oxidizer(Z=0) の混合層(左細->右太)
    lx0, lx1 = 90, 600
    ymid = 150
    top = [(lx0, ymid - 6)]
    bot = [(lx0, ymid + 6)]
    for i in range(1, 41):
        t = i / 40
        x = lx0 + (lx1 - lx0) * t
        w = 6 + 44 * t
        top.append((x, ymid - w)); bot.append((x, ymid + w))
    d.line(top, fill=GRAY, width=2, joint="curve")
    d.line(bot, fill=GRAY, width=2, joint="curve")
    ctext(d, lx0 + 30, ymid - 60, "fuel  Z=1", FT, GREEN, "lm")
    ctext(d, lx0 + 30, ymid + 60, "oxidizer  Z=0", FT, BLUE, "lm")
    # 代表点 1..4 (上=燃料側 -> 下=酸化剤側)
    pts = [(200, ymid - 34, "1"), (330, ymid - 8, "2"),
           (450, ymid + 12, "3"), (560, ymid + 36, "4")]
    for (px, py, lab) in pts:
        node(d, px, py, 5, fill=BLACK)
        ctext(d, px, py - 14, lab, FT, BLACK)
    # 各点の P(Z) 小グラフ(下段)
    gy = 340; gw = 120; gh = 90
    gxs = [70, 220, 370, 520]
    peaks = [0.9, 0.62, 0.4, 0.12]   # Zピーク位置(点1=燃料側->点4=酸化剤側)
    intermit = [True, False, False, True]  # 純燃料/純酸化剤の間欠性(delta)
    for gi, (gx, zp, itm) in enumerate(zip(gxs, peaks, intermit)):
        arrow(d, gx, gy, gx + gw + 8, gy, BLACK, 1, 8)
        arrow(d, gx, gy, gx, gy - gh - 6, BLACK, 1, 8)
        ctext(d, gx + gw + 8, gy + 10, "Z", FT, GRAY, "mm")
        ctext(d, gx - 4, gy - gh - 8, "P(Z) 点%d" % (gi + 1), FT, GRAY, "lm")
        ctext(d, gx, gy + 12, "0", FT, GRAY); ctext(d, gx + gw, gy + 12, "1", FT, GRAY)
        # ピーク曲線
        cur = []
        for k in range(0, 61):
            z = k / 60
            v = math.exp(-((z - zp) / 0.13) ** 2)
            cur.append((gx + z * gw, gy - 6 - v * (gh - 16)))
        d.line(cur, fill=BLUE, width=2, joint="curve")
        # 純燃料/純酸化剤の間欠性(端にdeltaの棒)
        if itm:
            ze = 1.0 if zp > 0.5 else 0.0
            xb = gx + ze * gw
            arrow(d, xb, gy, xb, gy - gh + 4, RED, 3, 9)
            ctext(d, xb + (10 if ze < 0.5 else -10), gy - gh + 2,
                  "delta", FT, RED, "lm" if ze < 0.5 else "rm")
    note(d, "燃料側(点1)はZ=1近傍, 酸化剤側(点4)はZ=0近傍に鋭いピーク. 純成分側は間欠性(delta)")
    save(im, "t1e22MixLayerPdfAns")


# ============================================================
# 22  t1e22JetDiffFlameAns  乱流噴流拡散火炎 z=60mm 断面の半径分布
# ============================================================
def t1e22JetDiffFlameAns():
    im, d = new(); title(d, "乱流噴流拡散火炎  z=60mm(z/d~12) 半径方向分布 (Ans)")
    ox, oy, xl, yl = 120, 345, 470, 235
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "r", FS, BLACK, "lm")
    ctext(d, ox + xl + 4, oy + 16, "半径(中心->外周)", FT, GRAY, "rm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "分布", FS, BLACK, "rm")
    def X(u): return ox + u * xl
    def Y(v): return oy - v * yl
    rfl = 0.55   # 火炎帯(平均燃料と酸素が出会う)
    dashed(d, X(rfl), oy, X(rfl), Y(1.0), LGRAY, 1, 6, 5)
    ctext(d, X(rfl), oy - yl - 2, "火炎帯", FT, RED)
    N = 120
    # 温度 T(赤): 中心付近まで高温, 火炎帯で最高
    ptsT = []
    for i in range(N + 1):
        u = i / N
        v = 0.35 + 0.55 * math.exp(-((u - rfl) / 0.28) ** 2)
        ptsT.append((X(u), Y(v)))
    d.line(ptsT, fill=RED, width=3, joint="curve")
    ctext(d, X(rfl), Y(0.99), "T", FS, RED)
    # CH4(緑): 中心側に多く外側で0
    ptsF = []
    for i in range(N + 1):
        u = i / N
        v = 0.70 / (1 + math.exp((u - (rfl - 0.10)) / 0.06))
        ptsF.append((X(u), Y(v)))
    d.line(ptsF, fill=GREEN, width=3, joint="curve")
    ctext(d, X(0.06), Y(0.64), "CH4", FT, GREEN, "lm")
    # O2(青): 外側に多く火炎帯内側で0
    ptsO = []
    for i in range(N + 1):
        u = i / N
        v = 0.60 / (1 + math.exp(-(u - (rfl + 0.10)) / 0.06))
        ptsO.append((X(u), Y(v)))
    d.line(ptsO, fill=BLUE, width=3, joint="curve")
    ctext(d, X(0.90), Y(0.56), "O2", FT, BLUE, "rm")
    # N2(灰): 中心付近まで拡散(緩やかに高い)
    ptsN = []
    for i in range(N + 1):
        u = i / N
        v = 0.30 + 0.12 * u
        ptsN.append((X(u), Y(v)))
    d.line(ptsN, fill=GRAY, width=2, joint="curve")
    ctext(d, X(0.30), Y(0.30), "N2", FT, GRAY, "lm")
    note(d, "火炎帯=平均CH4とO2がともに小さくなり出会う領域(T最高). N2は中心まで拡散")
    save(im, "t1e22JetDiffFlameAns")


# ============================================================
if __name__ == "__main__":
    t1e22TurbFlameSpeed()
    t1e22RegimeMap()
    t1e22VesselFlame()
    t1e22VesselFlameAns()
    t1e22BorghiDiagramAns()
    t1e22MixLayerPdfAns()
    t1e22JetDiffFlameAns()
    print("done ch22 review figures")
