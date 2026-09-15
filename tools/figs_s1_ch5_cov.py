# -*- coding: utf-8 -*-
"""固体力学1級 第5章 破壊力学・疲労解析 の1:1対応補完問題(欠番 問5-5/5-14/5-16/5-20)の図。
白地660x420・黒線画・機構のみ・物理的に正確。接頭辞は既存と同じ s1e5*。
ラベルはMeiryoで豆腐化しない通常表記。"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def box(d, cx, cy, w, h, text, fnt=FS, fill="white"):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=fill)
    if text:
        ctext(d, cx, cy, text, fnt)


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9):
    L = math.hypot(x2 - x1, y2 - y1)
    if L < 1:
        return
    n = max(1, int(L / dash))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash
            b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


# ---- 問5-5: き裂線に対称な2点P,P'の応力・変位の対称性 -----------------------
im, d = new()
title(d, "き裂に対称な2点 P, P' の応力・変位の対称性")
cx, cy = 300, 220
# き裂(x軸に沿って左から先端へ)
d.line((80, cy, cx, cy), fill=BLACK, width=5)
ctext(d, 135, cy - 16, "き裂", FT)
node(d, cx, cy, 5, fill=BLACK)
# x軸(先端から右へ・破線)
dashed(d, cx, cy, cx + 240, cy, GRAY)
ctext(d, cx + 248, cy, "x", FT, GRAY, "lm")
# 対称な2点 P(上), P'(下)
Px, Py = cx + 130, cy - 70
d.line((Px, cy, Px, cy - 200 + 200), fill=None)  # noop keep
node(d, Px, Py, 6, fill="white", col=BLUE)
node(d, Px, cy + 70, 6, fill="white", col=RED)
dashed(d, Px, cy - 70, Px, cy + 70, LGRAY)
ctext(d, Px + 14, Py, "P(x_p, y_p)", FT, BLUE, "lm")
ctext(d, Px + 14, cy + 70, "P'(x_p, -y_p)", FT, RED, "lm")
# x軸に対称であることの補助
dim(d, Px - 26, cy, Px - 26, Py, "y_p", 0, GRAY)
dim(d, Px - 26, cy, Px - 26, cy + 70, "y_p", 0, GRAY)
ctext(d, 330, 372, "モードI(対称): tau_xy 符号反転・sigma_y 同値 / u_x 同値・u_y 反転", FT, GRAY)
ctext(d, 330, 396, "モードII(反対称): sigma_y 符号反転・tau_xy 同値 / u_y 同値・u_x 反転", FT, GRAY)
save(im, "s1e5ModeSymmetry")

# ---- 問5-14: エネルギー法による KI 評価(上半分モデル・節点荷重と変位増分) -----
im, d = new()
title(d, "エネルギー法: G = Σ(Pi*Δvi)/Δa,  KI = sqrt(E'*G)")
# 対称面(下辺)を利用した上半分モデル
mx0, my0, mw, mh = 120, 130, 300, 150
d.rectangle((mx0, my0, mx0 + mw, my0 + mh), outline=BLACK, width=3, fill=FILL1)
symy = my0 + mh  # 対称面(き裂線)
hwall(d, mx0, mx0 + mw, symy, side=1, n=12)  # 対称面(拘束)
ctext(d, mx0 + mw + 8, symy + 4, "対称面", FT, GRAY, "lm")
# き裂(対称面左側は自由=開口, 右側は拘束)。き裂長さ a と a+Δa
tipx = mx0 + mw * 0.55
d.line((mx0, symy, tipx, symy), fill=RED, width=5)  # き裂 a(自由面)
node(d, tipx, symy, 5, fill=BLACK)
dim(d, mx0, symy + 30, tipx, symy + 30, "a", 0, RED)
arrow(d, tipx, symy - 22, tipx + 34, symy - 22, RED, 3, 11)
ctext(d, tipx + 40, symy - 22, "Δa", FT, RED, "lm")
# 節点荷重 Pa..Pd と 荷重点変位 va..vd(上向き開口)
labels = ["Pa", "Pb", "Pc", "Pd"]
xs = [mx0 + mw * t for t in (0.10, 0.24, 0.38, 0.50)]
for x, lab in zip(xs, labels):
    force(d, x, symy, 0, -34, "", RED)
    ctext(d, x, symy + 16, lab, FT, RED)
box(d, 545, 175, 190, 96, "G = Σ Pi Δvi / Δa\n(平面応力)\nKI = sqrt(E*G)", FT, FILL2)
ctext(d, 330, 396, "対称の2倍と外力仕事1/2が相殺 -> 分母は Δa(2Δaではない)", FT, GRAY)
save(im, "s1e5EnergyKI")

# ---- 問5-16: 混合モードJ積分(延長線x1方向 vs 実進展方向) --------------------
im, d = new()
title(d, "混合モードJ積分: 延長線 x1 方向の全エネルギー解放率")
cx, cy = 300, 235
d.line((90, cy, cx, cy), fill=BLACK, width=5)  # き裂
ctext(d, 150, cy - 16, "き裂", FT)
node(d, cx, cy, 4, fill=BLACK)
# 延長線 x1 方向(J積分が対応する方向)
dashed(d, cx, cy, cx + 180, cy, BLUE, 2, 9)
arrow(d, cx + 150, cy, cx + 185, cy, BLUE, 3, 11)
ctext(d, cx + 192, cy, "x1(延長線)", FT, BLUE, "lm")
# 実際の進展方向(傾き theta, 赤)
th = math.radians(40)
ex, ey = cx + 130 * math.cos(th), cy - 130 * math.sin(th)
arrow(d, cx, cy, ex, ey, RED, 3, 12)
ctext(d, ex + 8, ey - 6, "実進展方向", FT, RED, "lm")
angle_arc(d, cx, cy, 60, 0, 40, "theta", GRAY)
# 積分経路 Gamma
r = 105
path = []
for i in range(61):
    ang = math.radians(-150 + 300 * i / 60)
    path.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
d.line(path, fill=GREEN, width=2)
ctext(d, cx - r - 6, cy - 60, "Gamma", FT, GREEN, "rm")
ctext(d, 330, 372, "J = 全モード(I,II,III)を含む全エネルギー解放率", FT, GRAY)
ctext(d, 330, 396, "評価方向は延長線 x1(実際の傾いた進展方向ではない)・経路に依らず一定", FT, GRAY)
save(im, "s1e5MixedJ")

# ---- 問5-20: マイナー則のS-N線図(最長寿命=疲労限考慮) ----------------------
im, d = new()
title(d, "S-N線図の取り方と算出寿命(マイナー則)")
ox, oy = 120, 350
axes(d, ox, oy, 470, 290, "log N", "sigma (応力振幅)")
kneex = ox + 230
yf = oy - 95  # 疲労限度レベル
# 有限寿命域の斜め直線部(共通)
d.line((ox + 20, oy - 250, kneex, yf), fill=BLACK, width=3)
ctext(d, ox + 60, oy - 235, "有限寿命域", FT, GRAY, "lm")
# (1) 疲労限考慮: 水平(最長寿命)
d.line((kneex, yf, ox + 470, yf), fill=GREEN, width=3)
ctext(d, ox + 470, yf - 14, "(1)疲労限考慮=最長", FT, GREEN, "rm")
# (2) 延長(疲労限なし): 直線をそのまま延長
ex2, ey2 = ox + 460, oy - 20
dashed(d, kneex, yf, ex2, ey2, RED, 2, 9)
ctext(d, ex2, ey2 + 6, "(2)延長(短)", FT, RED, "rm")
# (3) こう配を小さくして延長
ex3, ey3 = ox + 460, oy - 55
dashed(d, kneex, yf, ex3, ey3, ORANGE, 2, 9)
ctext(d, ex3, ey3 - 12, "(3)こう配小(短)", FT, ORANGE, "rm")
dashed(d, ox, yf, kneex, yf, LGRAY)
ctext(d, ox - 8, yf, "sigma_f", FT, BLACK, "rm")
ctext(d, 330, 396, "疲労限以下を『損傷なし』とみなすほど寿命は長い -> (1)が最長", FT, GRAY)
save(im, "s1e5SNlife")


# ============================================================ 検証
KEYS = ["s1e5ModeSymmetry", "s1e5EnergyKI", "s1e5MixedJ", "s1e5SNlife"]
missing = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
print("=" * 40)
print("keys expected:", len(KEYS))
print("missing:", missing if missing else "none")
