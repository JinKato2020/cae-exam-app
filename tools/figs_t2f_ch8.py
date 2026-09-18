# -*- coding: utf-8 -*-
"""熱流体2級 第8章 ポスト処理の基礎 の公式図(t2f8*)を8枚描画。
白地660x420・黒線画・機構のみ(装飾禁止)。公式図なので考え方・要素を描いてよい。
豆腐対策: ギリシャ/特殊記号はローマ字・通常表記(rho, nu, mu, tau_w, u_tau, kappa,
  y+, u+, ym+, p0 等)。接頭辞 t2f8 厳守(問題図 t2e8 と衝突させない)。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / dash)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash; b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


# ==================================================== t2f8AreaAverage 面積加重平均
im, d = new()
title(d, "面積加重平均  各微小面 dS を面積で重み付け")
x0, x1, y0, y1 = 150, 560, 90, 320
d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
ctext(d, (x0 + x1) / 2, y0 - 12, "断面 A", FT, GRAY)
# 大小さまざまな微小面 dS に分割(縦横不等間隔)
xs = [x0]
x = x0; step = 26.0
while x < x1 - 8:
    x += step; step *= 1.14
    if x < x1 - 4:
        xs.append(x)
xs.append(x1)
ysr = [y0, y0 + 60, y0 + 110, y0 + 165, y1]
for xx in xs:
    d.line((xx, y0, xx, y1), fill=LGRAY, width=1)
for yy in ysr:
    d.line((x0, yy, x1, yy), fill=LGRAY, width=1)
# 代表微小面 dS を1つ強調
hx0, hy0, hx1, hy1 = xs[3], ysr[1], xs[4], ysr[2]
d.rectangle((hx0, hy0, hx1, hy1), outline=RED, width=3)
ctext(d, (hx0 + hx1) / 2, (hy0 + hy1) / 2, "dS", FT, RED)
ctext(d, (hx0 + hx1) / 2, hy1 + 14, "面 f_i", FT, RED)
# 式
ctext(d, (x0 + x1) / 2, y1 + 40, "f_bar = ( 積算 f dS ) / ( 積算 dS )", FS, BLACK)
note(d, "各微小面の値に面積 dS を掛けて足し・総面積で割る(広い面ほど強く効く)")
save(im, "t2f8AreaAverage")


# ==================================================== t2f8ContourPlot コンター図(等値線)
im, d = new()
title(d, "コンター図(等値線図)  スカラー量の分布")
x0, x1, y0, y1 = 130, 560, 80, 330
d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
# 同心状の等値線(高い塊が右寄りにある想定)
cx, cy = 420, 205
for k, r in enumerate([30, 62, 96, 132]):
    d.ellipse((cx - r * 1.2, cy - r, cx + r * 1.2, cy + r), outline=BLACK, width=2)
    ctext(d, cx + r * 1.2 + 2, cy, str(4 - k), FT, GRAY, "lm")
ctext(d, cx, cy, "高", FT, RED)
ctext(d, x0 + 40, y1 - 24, "低", FT, BLUE)
ctext(d, (x0 + x1) / 2, y1 + 20, "同じ値どうしを結ぶ線(値が急変する所ほど密)", FT, GRAY)
note(d, "圧力・温度・渦度などスカラー量の分布を等値線や塗り分けで表す")
save(im, "t2f8ContourPlot")


# ==================================================== t2f8VectorPlot 速度ベクトル図
im, d = new()
title(d, "速度ベクトル図  各格子点に速度の矢印")
x0, x1, y0, y1 = 110, 570, 90, 330
d.rectangle((x0, y0, x1, y1), outline=BLACK, width=2)
# 格子点に矢印(向き=流れの向き, 長さ=速さ)。中央でせん断的に曲がる流れ
for gx in range(x0 + 40, x1 - 20, 66):
    for gy in range(y0 + 34, y1 - 20, 52):
        # 速さは中央ほど速い放物形, 向きは右+わずかに上下
        f = 1 - ((gy - (y0 + y1) / 2) / ((y1 - y0) / 2)) ** 2
        ln = 18 + 34 * f
        dyv = -8 * ((gx - x0) / (x1 - x0) - 0.5)
        arrow(d, gx, gy, gx + ln, gy + dyv, BLUE, 2, 8)
ctext(d, (x0 + x1) / 2, y1 + 20, "矢印の向き=流れの向き, 長さ=速さ", FT, GRAY)
note(d, "速度など大きさと向きを持つ量(ベクトル量)の可視化に用いる")
save(im, "t2f8VectorPlot")


# ==================================================== t2f8Streamline 流線図
im, d = new()
title(d, "流線図  流れに沿った曲線")
x0, x1, y0, y1 = 90, 590, 90, 330
d.rectangle((x0, y0, x1, y1), outline=BLACK, width=2)
# 円柱まわりの流線(中央に円・上下に回り込む曲線)
cx, cy, r = 340, 210, 44
d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL2)
ctext(d, cx, cy, "物体", FT, BLACK)
for off in (-96, -58, 58, 96):
    pts = []
    for i in range(0, 501, 8):
        xx = x0 + 10 + i
        # 物体近くで膨らむ流線
        bump = off * (1 + 60.0 / (1 + ((xx - cx) / 55.0) ** 2) / abs(off) * (abs(off) < 70))
        yy = cy + off + (r + 30) * (1 if off > 0 else -1) * math.exp(-((xx - cx) / 90.0) ** 2) * (abs(off) < 70)
        pts.append((xx, yy))
    plot(d, 0, 0, pts, BLUE, 2)
    arrow(d, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], BLUE, 2, 9)
ctext(d, (x0 + x1) / 2, y1 + 20, "定常流れでは仮想粒子の軌跡と一致", FT, GRAY)
note(d, "入口から出口までの流れの経路を直感的に見せる")
save(im, "t2f8Streamline")


# ==================================================== t2f8Drag 抗力(圧力+せん断の流れ方向成分)
im, d = new()
title(d, "抗力 = (圧力 + せん断) の 流れ方向(x)成分")
ox, oy = 110, 340
axes(d, ox, oy, 470, 250, "x", "y")
# 一様流
for yy in range(130, 300, 42):
    arrow(d, 130, yy, 240, yy, GRAY, 2, 11)
ctext(d, 180, 112, "流れ x", FS, GRAY)
# 物体(円)
cx, cy, r = 380, 230, 60
d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL2)
ctext(d, cx, cy - 4, "物体", FT, BLACK)
# 圧力(法線・前面へ内向き) 赤
arrow(d, cx - r - 42, cy, cx - r - 6, cy, RED, 3, 12)
ctext(d, cx - r - 48, cy - 22, "圧力(法線)", FT, RED, "mm")
# せん断(接線・表面に沿う) 緑
ang = math.radians(48)
sx, sy = cx - r * math.cos(ang), cy - r * math.sin(ang)
arrow(d, sx, sy, sx + 36 * math.sin(ang), sy + 36 * math.cos(ang) + 8, GREEN, 3, 11)
ctext(d, sx - 6, sy - 18, "せん断(接線)", FT, GREEN, "mm")
# 合力の流れ方向成分=抗力
arrow(d, cx + r + 6, cy, cx + r + 70, cy, BLACK, 4, 15)
ctext(d, cx + r + 78, cy, "抗力 D (x成分の和)", FS, BLACK, "lm")
ctext(d, 330, 372, "揚力は流れに直交する y 方向成分(混同しない)", FT, GRAY)
save(im, "t2f8Drag")


# ==================================================== t2f8Stagnation よどみ点
im, d = new()
title(d, "よどみ点  速度0 → 動圧0 → 静圧が全圧に一致")
# 一様流(左)
for yy in range(140, 300, 34):
    arrow(d, 80, yy, 190, yy, BLUE, 2, 11)
ctext(d, 130, 118, "一様流 U", FS, BLUE)
# 物体前面
cx, cy, r = 360, 220, 70
d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL2)
ctext(d, cx + 6, cy, "物体", FS, BLACK)
# よどみ点(前面・速度0)
sx, sy = cx - r, cy
node(d, sx, sy, 7, fill=RED, col=RED)
ctext(d, sx - 14, sy - 24, "よどみ点(U=0)", FS, RED, "rm")
# 式
ctext(d, 330, 350, "全圧 p0 = p + (1/2) rho U^2", FS, BLACK)
ctext(d, 330, 380, "よどみ点: U=0 なので 静圧 p = p0 (流入全圧に一致)", FT, GRAY)
save(im, "t2f8Stagnation")


# ==================================================== t2f8WallLaw 対数則の壁関数(y+場合分け)
im, d = new()
title(d, "対数則の壁関数  u+ と y+ の場合分け")
ox, oy = 110, 330
axes(d, ox, oy, 480, 210, "y+", "u+")
xlen = 480
def xpos(yp):
    return ox + (math.log10(yp) / 3.0) * xlen
# 粘性域: u+ = y+ (小さいy+)
seg1 = []
yp = 1.0
while yp <= 11.0:
    seg1.append((xpos(yp), oy - yp * 5))
    yp *= 1.05
plot(d, 0, 0, seg1, BLUE, 3)
ctext(d, xpos(3), oy - 3 * 5 - 16, "u+ = y+", FT, BLUE)
# 対数域: u+ = (1/kappa) ln(E y+)
seg2 = []
kappa, E = 0.41, 9.0
yp = 11.0
while yp <= 1000:
    u = (1 / kappa) * math.log(E * yp)
    seg2.append((xpos(yp), oy - u * 5))
    yp *= 1.06
plot(d, 0, 0, seg2, RED, 3)
ctext(d, xpos(150), oy - (1 / kappa) * math.log(E * 150) * 5 - 16,
      "u+ = (1/kappa) ln(E y+)", FT, RED)
# 境目 ym+
xm = xpos(11)
dashed(d, xm, oy, xm, oy - 200, LGRAY, 2, 7)
ctext(d, xm, oy + 16, "y+ = ym+", FT, GRAY)
ctext(d, 330, 372, "u_tau = sqrt(tau_w/rho),  y+ = rho u_tau y / mu (横軸 y+ は対数目盛)", FT, BLACK)
note(d, "壁に近い粘性域は u+=y+ / 外側は対数則で橋渡し(境目 ym+ で一致)")
save(im, "t2f8WallLaw")


# ==================================================== t2f8WallCoord 壁座標 y+ の適応条件確認
im, d = new()
title(d, "壁座標 y+  壁関数の適応条件は第1格子点で確認")
wx0, wx1, wy = 70, 420, 340
hwall(d, wx0, wx1, wy, side=1, n=11)
ctext(d, (wx0 + wx1) / 2, wy + 18, "壁面", FT, GRAY)
# y軸
arrow(d, wx0 + 18, wy, wx0 + 18, 92, BLACK, 2, 11)
ctext(d, wx0 + 6, 88, "y", FS, BLACK, "rm")
# 3層帯(y+=5, 30 目安)
lv5 = wy - 55; lv30 = wy - 140; lvtop = wy - 232
dashed(d, wx0 + 18, lv5, wx1, lv5, LGRAY, 2, 7)
dashed(d, wx0 + 18, lv30, wx1, lv30, LGRAY, 2, 7)
ctext(d, wx0 + 30, (wy + lv5) / 2, "粘性底層 y+ <= 5", FT, BLUE, "lm")
ctext(d, wx0 + 30, (lv5 + lv30) / 2, "緩衝層 5 < y+ < 30", FT, GREEN, "lm")
ctext(d, wx0 + 30, (lv30 + lvtop) / 2, "対数層 y+ >= 30", FT, RED, "lm")
# 第1格子点を対数層(30〜100)に置く
node(d, wx0 + 250, lv30 - 48, 6)
d.line((wx0 + 250, wy, wx0 + 250, lv30 - 48), fill=GRAY, width=1)
ctext(d, wx0 + 250, lv30 - 66, "壁面第1格子点", FT, BLACK)
# 右: 適応条件
dx0 = 450
d.line((dx0 - 10, 110, dx0 - 10, 330), fill=LGRAY, width=1)
lines = ["適応条件の確認:", "第1格子点の y+ が",
         "おおむね 30〜100 に", "入っているか",
         "", "y+ = rho u_tau y / mu"]
for i, s in enumerate(lines):
    ctext(d, dx0, 128 + i * 34, s, FT, BLACK, "lm")
note(d, "高Re型 k-eps + 壁関数は第1格子点の y+ 分布で妥当性をチェック")
save(im, "t2f8WallCoord")


print("ALL DONE")
