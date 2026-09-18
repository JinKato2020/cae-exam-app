# -*- coding: utf-8 -*-
"""熱流体2級 第3章 熱力学・伝熱学の基礎 の公式図(t2f3*)を描画。
白地660x420・黒線画・機構のみ(装飾禁止)。
豆腐対策: ギリシャ/特殊記号はローマ字表記(lambda,rho,gamma,nu,eta,beta,
Delta,T^4 等)。接頭辞 t2f3 厳守(問題図 t2e3 と衝突させない)。"""
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


def mapper(ox, oy, xlen, ylen, xmin, xmax, ymin, ymax):
    def m(x, y):
        return (ox + (x - xmin) / (xmax - xmin) * xlen,
                oy - (y - ymin) / (ymax - ymin) * ylen)
    return m


# ============================================================ t2f3HeatEngine 熱機関の効率
im, d = new()
title(d, "熱機関の効率  eta = W / Q1")
# 高温熱源1(上) - サイクル(中) - 低温熱源2(下)
d.rectangle((210, 70, 450, 120), outline=BLACK, width=3, fill=FILL2)
ctext(d, 330, 95, "高温熱源 1  (温度 T1)", FS, RED)
d.rectangle((250, 185, 410, 255), outline=BLACK, width=3, fill=FILL1)
ctext(d, 330, 210, "サイクル", FS)
ctext(d, 330, 232, "(熱機関)", FT, GRAY)
d.rectangle((210, 320, 450, 370), outline=BLACK, width=3, fill=FILL2)
ctext(d, 330, 345, "低温熱源 2  (温度 T2)", FS, BLUE)
# Q1 流入(上->中), Q2 流出(中->下), W 外部へ(右)
arrow(d, 330, 120, 330, 185, RED, 4, 14)
ctext(d, 348, 152, "Q1 (もらう熱)", FT, RED, "lm")
arrow(d, 330, 255, 330, 320, BLUE, 4, 14)
ctext(d, 348, 288, "Q2 (捨てる熱)", FT, BLUE, "lm")
arrow(d, 410, 220, 560, 220, GREEN, 4, 14)
ctext(d, 500, 200, "W (仕事)", FT, GREEN)
note(d, "もらった熱 Q1 のうち仕事になった割合 = eta ・ 冷凍機は逆向きで成績係数 COP = Q2 / W")
save(im, "t2f3HeatEngine")


# ============================================================ t2f3PVIsotherm 等温変化(pV線図)
im, d = new()
title(d, "等温変化:  pV = const.  (p-V 線図で双曲線)")
ox, oy, xl, yl = 120, 350, 460, 280
axes(d, ox, oy, xl + 14, yl + 16, "V (体積)", "p (圧力)")
m = mapper(ox, oy, xl, yl, 0, 5.2, 0, 5.2)
# 双曲線 pV=const (反比例)
C = 4.0
pts = []
V = 0.9
while V <= 5.0:
    pts.append(m(V, C / V))
    V += 0.05
plot(d, 0, 0, pts, BLUE, 3)
ctext(d, ox + xl * 0.55, oy - yl * 0.5, "pV = const.", FS, BLUE, "lm")
# 2状態点で pV 一定を示す
for V0 in (1.0, 4.0):
    p0 = C / V0
    px, py = m(V0, p0)
    node(d, px, py, r=5, fill=RED, col=RED)
    dashed(d, px, py, px, oy, LGRAY, 2)
    dashed(d, px, py, ox, py, LGRAY, 2)
ctext(d, m(1.0, 0)[0], oy + 16, "V1", FT, GRAY)
ctext(d, m(4.0, 0)[0], oy + 16, "V2", FT, GRAY)
note(d, "温度一定なら pV=mRT=一定 ・ 体積を絞ると圧力は反比例で上がる(右下がりの双曲線)")
save(im, "t2f3PVIsotherm")


# ============================================================ t2f3PVCycle サイクルの仕事
im, d = new()
title(d, "サイクルのなす仕事  W = 閉曲線に囲まれた面積")
ox, oy, xl, yl = 120, 350, 460, 280
axes(d, ox, oy, xl + 14, yl + 16, "V (体積)", "p (圧力)")
m = mapper(ox, oy, xl, yl, 0, 5.2, 0, 5.2)
# 楕円状の閉サイクル
cx0, cy0, aa, bb = 2.6, 2.7, 1.5, 1.5
loop = []
for k in range(201):
    th = 2 * math.pi * k / 200
    loop.append(m(cx0 + aa * math.cos(th), cy0 + bb * math.sin(th)))
# 内部を淡色で塗る(仕事に相当)
d.polygon(loop, fill=(235, 235, 245))
d.line(loop, fill=BLUE, width=3, joint="curve")
# 周回の向き(時計回り=正の仕事)
a1 = m(cx0 + aa * math.cos(math.radians(60)), cy0 + bb * math.sin(math.radians(60)))
a2 = m(cx0 + aa * math.cos(math.radians(20)), cy0 + bb * math.sin(math.radians(20)))
arrow(d, a1[0], a1[1], a2[0], a2[1], RED, 3, 12)
ctext(d, m(cx0, cy0)[0], m(cx0, cy0)[1], "W = 面積", FS, BLACK)
note(d, "W = 反時計積分 p dV ・ 1サイクル1周で囲む面積が正味の仕事になる")
save(im, "t2f3PVCycle")


# ============================================================ t2f3Fourier フーリエの法則(定常熱伝導)
im, d = new()
title(d, "フーリエの法則  q = -lambda dT/dx  (定常は直線分布)")
wx0, wx1, wy0, wy1 = 160, 470, 120, 300
d.rectangle((wx0, wy0, wx1, wy1), outline=BLACK, width=3, fill=FILL1)
ctext(d, (wx0 + wx1) / 2, wy1 + 22, "平板 (厚さ D)", FT, GRAY)
ctext(d, wx0 - 8, wy0 - 4, "T1 高温", FT, RED, "rm")
ctext(d, wx1 + 8, wy1 + 4, "T2 低温", FT, BLUE, "lm")
# 温度分布(直線): 左上->右下
d.line((wx0, wy0 + 12, wx1, wy1 - 12), fill=BLACK, width=3)
node(d, wx0, wy0 + 12, r=5, fill=RED, col=RED)
node(d, wx1, wy1 - 12, r=5, fill=BLUE, col=BLUE)
ctext(d, (wx0 + wx1) / 2 - 6, (wy0 + wy1) / 2 - 26, "T(x) 直線", FT, BLACK)
# 熱流束の向き(高温->低温)
for yy in (150, 210, 270):
    arrow(d, wx0 + 20, yy, wx1 - 20, yy, GREEN, 2, 10)
ctext(d, (wx0 + wx1) / 2, 210 - 42, "熱流束 q ->", FT, GREEN)
note(d, "定常一次元では熱流束が一定なので温度勾配も一定=直線 ・ 通過熱量 Q = lambda (T1-T2)/D x A x t")
save(im, "t2f3Fourier")


# ============================================================ t2f3Convection 対流熱伝達
im, d = new()
title(d, "対流熱伝達  q = h (Tw - T)  (ニュートンの冷却則)")
# 壁(左)を高温 Tw、まわりの流体を主流温度 T
wx = 150
d.rectangle((90, 110, wx, 320), outline=BLACK, width=3, fill=FILL2)
ctext(d, 120, 215, "壁", FS, RED)
ctext(d, 120, 100, "壁面 Tw", FT, RED)
# 主流(流体)の流れ矢印
for yy in (140, 185, 230, 275):
    arrow(d, 360, yy, 520, yy, BLUE, 2, 10)
ctext(d, 470, 100, "主流 (流体温度 T)", FT, BLUE)
# 境界層(速度が壁付近で立ち上がる曲線)
bl = []
for yy in range(120, 311, 6):
    t = (yy - 120) / 190.0
    # 壁からの距離が下ほど…単純に境界層縁のふくらみ
    bl.append((wx + 120 * (1 - 0.6 * math.sin(math.pi * t) * 0), yy))
dashed(d, wx + 95, 120, wx + 95, 310, GRAY, 2)
ctext(d, wx + 100, 128, "境界層", FT, GRAY, "lm")
# 壁から流体へ伝わる熱
arrow(d, wx, 215, wx + 90, 215, GREEN, 4, 14)
ctext(d, wx + 45, 195, "q", FS, GREEN)
note(d, "熱伝達率 h の定義 h = qw/(Tw - T) ・ Tw>T なら壁から流体へ q=h(Tw-T) の熱が伝わる")
save(im, "t2f3Convection")


# ============================================================ t2f3BoundaryLayer 速度/温度境界層とPr
im, d = new()
title(d, "速度境界層と温度境界層  (Pr = nu / a で厚さが決まる)")
# 平板(下)に沿う流れ、前縁から発達
px0, px1, py = 110, 560, 330
hwall(d, px0, px1, py, 1, 14)
ctext(d, (px0 + px1) / 2, py + 32, "等温加熱された平板", FT, GRAY)
# 速度境界層(実線, 厚い)
vb = [(px0, py)]
for x in range(px0, px1 + 1, 8):
    t = (x - px0) / (px1 - px0)
    vb.append((x, py - 120 * math.sqrt(max(t, 0))))
plot(d, 0, 0, vb, BLUE, 3)
ctext(d, px1 - 6, py - 120 * math.sqrt(1) - 6, "速度境界層", FT, BLUE, "rm")
# 温度境界層(点線, Pr>1 で薄い)
tb = [(px0, py)]
for x in range(px0, px1 + 1, 8):
    t = (x - px0) / (px1 - px0)
    tb.append((x, py - 72 * math.sqrt(max(t, 0))))
for i in range(len(tb) - 1):
    dashed(d, tb[i][0], tb[i][1], tb[i + 1][0], tb[i + 1][1], RED, 2, 8)
ctext(d, px1 - 6, py - 72 * math.sqrt(1) + 14, "温度境界層", FT, RED, "rm")
# 一様流入
for yy in (150, 190, 230):
    arrow(d, 40, yy, px0, yy, GRAY, 2, 9)
ctext(d, 60, 128, "一様流", FT, GRAY, "lm")
note(d, "Pr>1: 温度境界層 < 速度境界層 / Pr=1: 一致 / Pr<1: 温度境界層 > 速度境界層")
save(im, "t2f3BoundaryLayer")


# ============================================================ t2f3ConvClass 対流の分類
im, d = new()
title(d, "対流の分類  (横軸 Ra=Gr Pr, 縦軸 Re)")
ox, oy, xl, yl = 120, 350, 440, 280
axes(d, ox, oy, xl + 14, yl + 16, "Ra (= Gr Pr)", "Re")
# 3領域をざっくり区切る境界線
d.line((ox + xl * 0.45, oy, ox + xl * 0.45, oy - yl), fill=LGRAY, width=2)
d.line((ox, oy - yl * 0.45, ox + xl, oy - yl * 0.45), fill=LGRAY, width=2)
# 対角の複合対流帯
dashed(d, ox + xl * 0.2, oy - yl * 0.2, ox + xl * 0.9, oy - yl * 0.9, GRAY, 2)
# ラベル
ctext(d, ox + xl * 0.22, oy - yl * 0.72, "強制対流", FS, BLUE)
ctext(d, ox + xl * 0.22, oy - yl * 0.9, "(Re 大)", FT, GRAY)
ctext(d, ox + xl * 0.72, oy - yl * 0.22, "自然対流", FS, RED)
ctext(d, ox + xl * 0.72, oy - yl * 0.06, "(Ra 大)", FT, GRAY)
ctext(d, ox + xl * 0.6, oy - yl * 0.62, "複合対流", FS, GREEN)
ctext(d, ox + xl * 0.6, oy - yl * 0.5, "(両方効く)", FT, GRAY)
note(d, "Re 大で Ra 小=強制対流 ・ Ra 大で Re 小=自然対流 ・ 中間は両方効く複合対流")
save(im, "t2f3ConvClass")

print("done")
