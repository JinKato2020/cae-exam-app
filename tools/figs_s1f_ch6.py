# -*- coding: utf-8 -*-
"""固体力学1級 第6章 動的解析 の公式・用語図(s1f6*)を描画。
白地660x420・黒線画・機構のみ・物理的に正確(装飾禁止)。
ラベルはMeiryoで豆腐化しない通常表記。ドット付き記号(u̇)は使わず a(加速度)/v(速度)/u(変位)。
ギリシャは Meiryo が持つ α β ζ ω Ω δ をそのまま、化けるものはASCII。上付きは ^2 表記。
接頭辞 s1f6 厳守(問題図 s1e6 と衝突させない)。"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / dash))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash
            b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


def dashpot(d, x1, y, x2, h=22):
    """水平ダッシュポット(粘性減衰要素)。x1=壁側, x2=質点側。"""
    L = x2 - x1
    cl = x1 + L * 0.18   # シリンダ左壁
    cr = x1 + L * 0.66   # シリンダ開口(右)
    px = x1 + L * 0.50   # ピストン板
    d.line((x1, y, cl, y), fill=BLACK, width=3)          # 壁側ロッド
    d.line((cl, y - h, cl, y + h), fill=BLACK, width=3)  # シリンダ左壁
    d.line((cl, y - h, cr, y - h), fill=BLACK, width=3)  # 上
    d.line((cl, y + h, cr, y + h), fill=BLACK, width=3)  # 下
    d.line((px, y - h + 4, px, y + h - 4), fill=BLACK, width=4)  # ピストン板
    d.line((px, y, x2, y), fill=BLACK, width=3)          # 質点側ロッド


def mapper(ox, oy, xlen, ylen, xmin, xmax, ymin, ymax):
    def m(x, y):
        return (ox + (x - xmin) / (xmax - xmin) * xlen,
                oy - (y - ymin) / (ymax - ymin) * ylen)
    return m


# ============================================================ s1f6Eom 運動方程式
im, d = new()
title(d, "運動方程式  Ma + Cv + Ku = f  (1自由度)")
wall(d, 80, 120, 300, 1, 9)
mx0, mx1, my0, my1 = 350, 460, 150, 290
d.rectangle((mx0, my0, mx1, my1), outline=BLACK, width=3, fill=FILL1)
ctext(d, (mx0 + mx1) / 2, (my0 + my1) / 2 - 8, "質量 M", F)
ctext(d, (mx0 + mx1) / 2, (my0 + my1) / 2 + 20, "(慣性 Ma)", FT, GRAY)
# 弾性(バネ K)
spring(d, 80, 178, mx0, 178, coils=6, amp=14)
ctext(d, 210, 150, "バネ K → 復元力 Ku", FT, GREEN)
# 減衰(ダッシュポット C)
dashpot(d, 80, 250, mx0, 250)
ctext(d, 210, 292, "減衰 C → 減衰力 Cv", FT, BLUE)
# 転がり支持(床)
for cx in (365, 400, 435):
    d.ellipse((cx - 7, 292, cx + 7, 306), outline=BLACK, width=2)
hwall(d, 345, 465, 308, 1, 8)
# 外力 f と変位 u
force(d, mx1, 200, 90, 0, "f (外力)", RED)
arrow(d, 405, 130, 470, 130, GRAY, 2, 10)
ctext(d, 500, 130, "u (変位)", FT, GRAY)
note(d, "Ma=慣性力  Cv=減衰力  Ku=弾性復元力   (a=加速度, v=速度, u=変位)")
save(im, "s1f6Eom")


# ============================================================ s1f6Wave 弾性波 P波/S波
im, d = new()
title(d, "弾性波  v∝√(E/ρ) :  P波(縦波)と S波(横波)")
# P波(縦波): 粒子は進行方向に振動、疎密の波
yP = 150
arrow(d, 90, 105, 590, 105, GRAY, 2, 11)
ctext(d, 500, 92, "進行方向", FT, GRAY)
k = 2 * math.pi / 120
for i in range(41):
    base = 95 + 480 * i / 40
    disp = 9 * math.sin(k * base)
    x = base + disp
    d.line((x, yP - 22, x, yP + 22), fill=BLACK, width=2)
# 粒子振動(進行方向に平行)
arrow(d, 300, yP + 44, 340, yP + 44, RED, 2, 9)
arrow(d, 300, yP + 44, 260, yP + 44, RED, 2, 9)
ctext(d, 300, yP + 60, "粒子振動 ∥ 進行方向", FT, RED)
ctext(d, 90, yP - 40, "P波(縦波): 疎密の波 約5-7km/s ・気体/液体も伝わる", FT, BLACK, "lm")
# S波(横波): 粒子は進行方向に垂直、正弦波形
yS = 320
A = 30
pts = [(95 + 480 * i / 200, yS - A * math.sin(4 * math.pi * i / 200)) for i in range(201)]
plot(d, 0, 0, pts, BLACK, 3)
arrow(d, 300, yS - 34, 300, yS - 64, RED, 2, 9)
arrow(d, 300, yS - 34, 300, yS - 4, RED, 2, 9)
ctext(d, 372, yS - 34, "粒子振動 ⊥ 進行方向", FT, RED)
ctext(d, 90, yS + 58, "S波(横波): せん断の波 約3-4km/s ・固体の中だけ", FT, BLACK, "lm")
save(im, "s1f6Wave")


# ============================================================ s1f6Mass 質量マトリックス
im, d = new()
title(d, "質量マトリックス:  整合質量  と  集中質量")
# 左: 整合質量(質量を要素全体に連続分布)
ctext(d, 190, 68, "整合質量 (consistent)", FS)
d.rectangle((100, 100, 280, 128), outline=BLACK, width=3, fill=FILL2)  # 分布質量の棒
node(d, 100, 114); node(d, 280, 114)
ctext(d, 100, 142, "節点1", FT); ctext(d, 280, 142, "節点2", FT)
ctext(d, 108, 250, "ρAL/6", FS)
matrix_grid(d, 160, 218, [["2", "1"], ["1", "2"]], cell=46)
ctext(d, 190, 328, "非対角あり・高精度", FT, GRAY)
ctext(d, 190, 348, "陰解法で逆行列が重い", FT, GRAY)
# 右: 集中質量(全質量を両端節点に半分ずつ)
ctext(d, 490, 68, "集中質量 (lumped)", FS)
d.line((410, 114, 570, 114), fill=BLACK, width=3)  # 質量ゼロの棒
node(d, 410, 114, r=17, fill=FILL3); node(d, 570, 114, r=17, fill=FILL3)
ctext(d, 410, 114, "m/2", FT); ctext(d, 570, 114, "m/2", FT)
ctext(d, 410, 148, "節点1", FT); ctext(d, 570, 148, "節点2", FT)
ctext(d, 408, 250, "ρAL/2", FS)
matrix_grid(d, 460, 218, [["1", "0"], ["0", "1"]], cell=46)
ctext(d, 490, 328, "対角のみ(逆行列が簡単)", FT, GRAY)
ctext(d, 490, 348, "陽解法で使える", FT, GRAY)
d.line((330, 90, 330, 360), fill=LGRAY, width=2)
save(im, "s1f6Mass")


# ============================================================ s1f6Rayleigh レイリー減衰
im, d = new()
title(d, "レイリー減衰  ζ(ω)=1/2(α/ω+βω)  ・ U字型")
ox, oy, xlen, ylen = 110, 350, 470, 280
axes(d, ox, oy, xlen + 10, ylen + 15, "ω", "ζ")
alpha, beta = 1.0, 0.9
xmin, xmax, ymax = 0.3, 3.6, 2.0
m = mapper(ox, oy, xlen, ylen, xmin, xmax, 0, ymax)
N = 240
# α項(質量比例, 低周波で効く)
pa = [m(xmin + (xmax - xmin) * i / N, 0.5 * alpha / (xmin + (xmax - xmin) * i / N)) for i in range(N + 1)]
for i in range(0, len(pa) - 1, 2):
    d.line((pa[i][0], pa[i][1], pa[i + 1][0], pa[i + 1][1]), fill=GRAY, width=2)
# β項(剛性比例, 高周波で効く)
xb0, xb1 = xmin, xmax
pb0 = m(xb0, 0.5 * beta * xb0); pb1 = m(xb1, 0.5 * beta * xb1)
dashed(d, pb0[0], pb0[1], pb1[0], pb1[1], GRAY, 2)
# 合計 ζ(ω)
pz = [m(xmin + (xmax - xmin) * i / N,
        min(ymax, 0.5 * (alpha / (xmin + (xmax - xmin) * i / N) + beta * (xmin + (xmax - xmin) * i / N))))
      for i in range(N + 1)]
plot(d, 0, 0, pz, BLUE, 3)
# 極小点
wmin = math.sqrt(alpha / beta); zmin = math.sqrt(alpha * beta)
pmx, pmy = m(wmin, zmin)
node(d, pmx, pmy, r=5, fill=BLUE, col=BLUE)
dashed(d, pmx, pmy, pmx, oy, LGRAY, 2)
ctext(d, pmx, pmy - 18, "極小", FT, BLUE)
ctext(d, 300, 120, "ζ(ω)  合計", FS, BLUE, "lm")
ctext(d, 175, 150, "α/ω 質量比例", FT, GRAY, "lm")
ctext(d, 430, 175, "βω 剛性比例", FT, GRAY, "lm")
note(d, "α項=低周波で効く粘性減衰 / β項=高周波で効く構造減衰")
save(im, "s1f6Rayleigh")


# ============================================================ s1f6Hourglass アワーグラスモード
im, d = new()
title(d, "アワーグラスモード (偽りのゼロエネルギーモード)")
# 左: 正常な4節点要素(1点積分)
lx = [140, 300, 300, 140]; ly = [150, 150, 300, 300]  # TL,TR,BR,BL
d.polygon(list(zip(lx, ly)), outline=BLACK, width=3, fill=FILL1)
for x, y in zip(lx, ly):
    node(d, x, y, r=6)
node(d, 220, 225, r=4, fill=BLACK)
ctext(d, 220, 225 + 20, "積分点(1点)", FT, GRAY)
ctext(d, 220, 330, "正常な要素", FS)
# 右: アワーグラス変形(節点変位パターン(+,-,+,-) → 中心のひずみ0)
cx = [430, 590, 590, 430]; cy = [150, 150, 300, 300]
e = 26
dx = [+e, -e, +e, -e]  # hourglass vector (CCW)
hx = [cx[i] + dx[i] for i in range(4)]
# 元の四角(点線)と変形形状(実線)
dashed(d, 430, 150, 590, 150); dashed(d, 590, 150, 590, 300)
dashed(d, 590, 300, 430, 300); dashed(d, 430, 300, 430, 150)
d.polygon(list(zip(hx, cy)), outline=RED, width=3)
for i in range(4):
    node(d, hx[i], cy[i], r=6, col=RED)
    if dx[i] > 0:
        arrow(d, cx[i], cy[i], hx[i], cy[i], RED, 2, 8)
    else:
        arrow(d, cx[i], cy[i], hx[i], cy[i], RED, 2, 8)
node(d, 510, 225, r=4, fill=BLACK)
ctext(d, 510, 225 + 20, "ひずみ 0", FT, RED)
ctext(d, 510, 330, "砂時計状の変形(抵抗力ゼロ)", FT)
note(d, "低減積分で発生 → アワーグラス抗力(アワーグラス速度に比例)で抑える")
save(im, "s1f6Hourglass")


# ============================================================ s1f6Newmark ニューマークβ法
im, d = new()
title(d, "ニューマークβ法:  平均加速度法 と 線形加速度法")
def nm_plot(oxp, lab, sub, kind):
    oyp, xl, yl = 320, 200, 190
    axes(d, oxp, oyp, xl + 10, yl + 10, "t", "a")
    ctext(d, oxp - 4, oyp + 18, "t_n", FT, GRAY)
    ctext(d, oxp + xl, oyp + 18, "t_n+1", FT, GRAY)
    an, an1 = 0.35 * yl, 0.85 * yl  # 端点の加速度(ピクセル高)
    x0, x1 = oxp, oxp + xl
    # 端点マーカ
    node(d, x0, oyp - an, r=4, fill=BLACK)
    node(d, x1, oyp - an1, r=4, fill=BLACK)
    ctext(d, x0 - 16, oyp - an, "a_n", FT, GRAY)
    ctext(d, x1 + 20, oyp - an1, "a_n+1", FT, GRAY)
    if kind == "avg":
        lev = (an + an1) / 2
        d.line((x0, oyp - lev, x1, oyp - lev), fill=BLUE, width=3)
        dashed(d, x0, oyp - an, x0, oyp - lev, LGRAY)
        dashed(d, x1, oyp - an1, x1, oyp - lev, LGRAY)
        ctext(d, (x0 + x1) / 2, oyp - lev - 16, "一定=平均", FT, BLUE)
    else:
        d.line((x0, oyp - an, x1, oyp - an1), fill=BLUE, width=3)
        ctext(d, (x0 + x1) / 2, oyp - (an + an1) / 2 - 16, "直線変化", FT, BLUE)
    ctext(d, oxp + xl / 2, 70, lab, FS)
    ctext(d, oxp + xl / 2, 92, sub, FT, GRAY)
nm_plot(70, "平均加速度法 β=1/4", "γ=1/2・無条件安定", "avg")
nm_plot(380, "線形加速度法 β=1/6", "γ=1/2・条件付き安定", "lin")
save(im, "s1f6Newmark")


# ============================================================ s1f6RespSpectrum 応答スペクトル
im, d = new()
title(d, "応答スペクトル:  1自由度系の最大応答")
# 左: 周期の異なる1自由度系を同じ地動で揺らす
base = 300
hwall(d, 60, 330, base, 1, 9)
arrow(d, 150, base + 26, 240, base + 26, RED, 3, 11)
arrow(d, 240, base + 26, 150, base + 26, RED, 3, 11)
ctext(d, 195, base + 42, "地動(共通の入力)", FT, RED)
for x, top, lab in [(105, 210, "ω1"), (195, 165, "ω2"), (285, 130, "ω3")]:
    spring(d, x, base, x, top + 18, coils=5, amp=11)
    d.rectangle((x - 20, top - 14, x + 20, top + 14), outline=BLACK, width=3, fill=FILL1)
    ctext(d, x, top, lab, FT)
ctext(d, 195, 96, "ω1<ω2<ω3(固有振動数)", FT, GRAY)
# 右: スペクトル曲線(最大応答 vs 固有周期)
ox, oy, xl, yl = 380, 320, 220, 210
axes(d, ox, oy, xl + 10, yl + 10, "T", "S_A")
ctext(d, ox + xl / 2, oy + 22, "固有周期 T", FT, GRAY)
m = mapper(ox, oy, xl, yl, 0, 3, 0, 1.1)
pts = []
for i in range(121):
    T = 3 * i / 120
    S = math.exp(-((T - 0.7) ** 2) / 0.30) * (1 - math.exp(-T / 0.12))
    pts.append(m(T, S))
plot(d, 0, 0, pts, BLUE, 3)
ctext(d, ox + xl / 2, oy - yl - 4, "応答スペクトル", FT, BLUE)
note(d, "S_V=ω S_D ,  S_A=ω^2 S_D   (ω=固有角振動数・S_D/S_V/S_A=変位/速度/加速度)")
save(im, "s1f6RespSpectrum")


# ============================================================ s1f6Resonance 共振曲線
im, d = new()
title(d, "共振曲線  M=1/√((1-(ω/Ω)^2)^2+(2ζω/Ω)^2)")
ox, oy, xl, yl = 110, 350, 470, 285
axes(d, ox, oy, xl + 10, yl + 12, "ω/Ω", "M=A/D")
ymax = 6.0
m = mapper(ox, oy, xl, yl, 0, 3, 0, ymax)
# 共振線 ω/Ω=1
p1 = m(1, 0); p1t = m(1, ymax)
dashed(d, p1[0], p1[1], p1t[0], p1t[1], LGRAY, 2)
ctext(d, p1[0], oy + 18, "1", FT, GRAY)
ctext(d, m(2, 0)[0], oy + 18, "2", FT, GRAY)
for zeta, col, ly in [(0.1, RED, "ζ=0.1"), (0.25, BLUE, "ζ=0.25"), (0.5, GREEN, "ζ=0.5")]:
    pts = []
    for i in range(301):
        r = 3 * i / 300
        M = 1.0 / math.sqrt((1 - r * r) ** 2 + (2 * zeta * r) ** 2)
        pts.append(m(r, min(M, ymax)))
    plot(d, 0, 0, pts, col, 3)
    Mpk = 1.0 / (2 * zeta)
    px, py = m(1, min(Mpk, ymax))
    ctext(d, px + 60, py, ly, FT, col, "lm")
ctext(d, p1t[0], p1t[1] - 4, "共振(ζ小ほど鋭く高い)", FT, GRAY)
note(d, "共振点 ω/Ω=1 での倍率 M≈1/(2ζ)   ・ ζ=0 では発散")
save(im, "s1f6Resonance")

print("done")
