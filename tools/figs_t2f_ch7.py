# -*- coding: utf-8 -*-
"""熱流体2級 第7章 境界条件 の公式図(t2f7*)を描画。
白地660x420・黒線画・機構のみ(装飾禁止)。
豆腐対策: ギリシャ/特殊記号はローマ字・通常表記(u_tau, y+, u+, tau_w, rho, nu,
  lambda, kappa, eps, Tw, qw, Ue 等)。偏微分は d 表記(dT/dn 等)で統一。
接頭辞 t2f7 厳守(問題図 t2e7 と衝突させない)。"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8):
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


# ==================================================== t2f7DirichletNeumann 値 vs 勾配
im, d = new()
title(d, "境界条件の2分類  ディリクレ(値) と ノイマン(勾配)")
# 左: ディリクレ = 値を固定
ctext(d, 175, 64, "ディリクレ条件: 値を指定", FS, BLUE)
ox, oy = 110, 320
axes(d, ox, oy, 195, 180, "n", "u")
ctext(d, ox - 8, oy + 18, "境界", FT, GRAY, "mm")
f1 = 95
pts = []
for k in range(0, 196, 3):
    val = f1 + (k / 195) * 70 * math.sqrt(k / 195 + 0.05)
    pts.append((ox + k, oy - val))
d.line(pts, fill=BLACK, width=3, joint="curve")
node(d, ox, oy - f1, r=6, fill=RED, col=RED)
ctext(d, ox + 14, oy - f1 - 6, "u = f (値を固定)", FT, RED, "lm")
# 右: ノイマン = 勾配を固定
ctext(d, 485, 64, "ノイマン条件: 勾配を指定", FS, GREEN)
ox2, oy2 = 385, 320
axes(d, ox2, oy2, 195, 180, "n", "u")
ctext(d, ox2 - 8, oy2 + 18, "境界", FT, GRAY, "mm")
g1 = 70
ptsn = []
for k in range(0, 196, 3):
    ptsn.append((ox2 + k, oy2 - (g1 + (k / 195) * 95)))
d.line(ptsn, fill=BLACK, width=3, joint="curve")
node(d, ox2, oy2 - g1, r=5, fill=GREEN, col=GREEN)
d.line((ox2, oy2 - g1, ox2 + 78, oy2 - g1 - 38), fill=RED, width=3)
ctext(d, ox2 + 86, oy2 - g1 - 34, "傾き dU/dn = g", FT, RED, "lm")
ctext(d, ox2 + 100, oy2 - 168, "断熱なら dT/dn = 0", FT, GRAY, "mm")
note(d, "値が決まる壁=ディリクレ / 勾配が決まる壁(断熱 dT/dn=0)=ノイマン")
save(im, "t2f7DirichletNeumann")


# ==================================================== t2f7WallBC 壁面境界条件
im, d = new()
title(d, "壁面境界条件  滑りなし(速度)と 壁温3種(温度)")
# 下面の固体壁(全幅)
hwall(d, 70, 590, 300, side=1, n=18)
ctext(d, 330, 322, "固体壁", FT, GRAY)
# 左: 速度=滑りなし(No-Slip) 速度プロフィル
ctext(d, 175, 66, "速度: 滑りなし u=v=w=0", FS, BLUE)
bx = 95
for i in range(7):
    yy = 296 - i * 22
    ln = 14 + i * 22
    arrow(d, bx, yy, bx + ln, yy, BLUE, 2, 8)
d.line([(bx, 296), (bx + 14, 296), (bx + 14 + 6 * 22, 296 - 6 * 22)], fill=BLUE, width=2, joint="curve")
node(d, bx, 300, r=4, fill=RED, col=RED)
ctext(d, bx + 6, 150, "壁で u=0", FT, RED, "lm")
# 右: 温度は3種を使い分け
rx = 360
ctext(d, 478, 66, "温度: 壁の与え方で3種", FS, RED)
# 壁からの熱流束矢印(例)
for k in range(3):
    xx = rx + 40 + k * 60
    arrow(d, xx, 298, xx, 250, RED, 2, 9)
ctext(d, rx + 100, 236, "熱流束 qw", FT, RED)
opts = ["(1) 壁温一定 T=Tw (ディリクレ)",
        "(2) 熱流束一定 -lambda dT/dn=qw",
        "     (ノイマン)",
        "(3) 断熱 dT/dn=0 (ノイマン)"]
for i, s in enumerate(opts):
    ctext(d, rx - 12, 98 + i * 24, s, FT, BLACK, "lm")
note(d, "粘性流れ=速度は滑りなし / 温度は壁の熱の与え方で3種を使い分け")
save(im, "t2f7WallBC")


# ==================================================== t2f7NaturalConvBC 閉空間自然対流
im, d = new()
title(d, "閉空間の自然対流  加熱壁/冷却壁 と 上下断熱壁")
L, Rr, T, B = 210, 450, 96, 322
# 上下の断熱壁(ハッチ)
hwall(d, L, Rr, T, side=-1, n=12)
hwall(d, L, Rr, B, side=1, n=12)
ctext(d, 330, T - 20, "上壁 断熱  dT/dy = 0", FT, GRAY)
ctext(d, 330, B + 22, "下壁 断熱  dT/dy = 0", FT, GRAY)
# 左=加熱壁(赤) 右=冷却壁(青)
d.line((L, T, L, B), fill=RED, width=4)
d.line((Rr, T, Rr, B), fill=BLUE, width=4)
ctext(d, L - 12, (T + B) / 2 - 30, "加熱壁", FS, RED, "rm")
ctext(d, L - 12, (T + B) / 2 - 8, "q=-lambda dT/dx", FT, RED, "rm")
ctext(d, Rr + 12, (T + B) / 2 - 30, "冷却壁", FS, BLUE, "lm")
ctext(d, Rr + 12, (T + B) / 2 - 8, "T = Tc", FT, BLUE, "lm")
# 循環ループ(加熱側で上昇, 冷却側で下降)
cx, cy = (L + Rr) / 2, (T + B) / 2
d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), outline=GRAY, width=2)
arrow(d, cx - 70, cy + 10, cx - 70, cy - 20, RED, 3, 12)      # 左=上昇
arrow(d, cx + 70, cy - 10, cx + 70, cy + 20, BLUE, 3, 12)     # 右=下降
arrow(d, cx + 20, cy - 70, cx - 10, cy - 70, GRAY, 3, 11)     # 上=左向き
arrow(d, cx - 20, cy + 70, cx + 10, cy + 70, GRAY, 3, 11)     # 下=右向き
ctext(d, cx, cy, "自然対流", FT, GRAY)
note(d, "断熱=温度勾配0(ノイマン) / 加熱・冷却壁=熱流束を指定 / 定常は入熱=排熱")
save(im, "t2f7NaturalConvBC")


# ==================================================== t2f7WallLaw 壁法則(対数則3層)
im, d = new()
title(d, "壁法則(対数則)の3層構造  u+ vs y+")
ox, oy = 110, 330
axes(d, ox, oy, 480, 210, "y+", "u+")
xlen = 480
# x を対数目盛に見立てて y+=1〜1000 を全幅に写像
def xpos(yp):
    return ox + (math.log10(yp) / 3.0) * xlen
# u+(y+) は Reichardt 型の滑らかな合成則(壁近傍 u+=y+, 遠方で対数則)
def uplus(yp):
    return (1 / 0.41) * math.log(1 + 0.41 * yp) + 7.8 * (1 - math.exp(-yp / 11.0) - (yp / 11.0) * math.exp(-0.33 * yp))
# 3領域を色分け(粘性底層 青 / 緩衝層 緑 / 対数層 赤)で1本の滑らかな曲線を描く
def curve_seg(lo, hi, col):
    pts = []
    yp = lo
    while yp <= hi + 1e-9:
        pts.append((xpos(yp), oy - uplus(yp) * 5))
        yp *= 1.06
    d.line(pts, fill=col, width=3, joint="curve")
curve_seg(1, 5, BLUE)
curve_seg(5, 30, GREEN)
curve_seg(30, 1000, RED)
# 3層の境界線 y+=5, 30
for yp, lab, col in [(5, "y+ = 5", BLUE), (30, "y+ = 30", RED)]:
    xx = xpos(yp)
    dashed(d, xx, oy, xx, oy - 200, LGRAY, 2, 7)
    ctext(d, xx, oy + 16, lab, FT, col)
ctext(d, (xpos(1) + xpos(5)) / 2, 92, "粘性底層", FT, BLUE)
ctext(d, (xpos(1) + xpos(5)) / 2, 108, "u+=y+", FT, BLUE)
ctext(d, (xpos(5) + xpos(30)) / 2, 92, "緩衝層", FT, GREEN)
ctext(d, (xpos(30) + xpos(1000)) / 2, 92, "対数層", FT, RED)
ctext(d, (xpos(30) + xpos(1000)) / 2, 108, "対数則が成立", FT, RED)
ctext(d, 330, 372, "U/u_tau = (1/kappa) ln(y0 u_tau/nu) + C   (kappa=0.41, C=5.0)", FT, BLACK)
note(d, "壁近傍を直接解かず対数則で橋渡し / 仮想原点 y0 は粘性底層より上(対数層)")
save(im, "t2f7WallLaw")


# ==================================================== t2f7FreeSurface 自由表面Slip
im, d = new()
title(d, "自由表面のSlip条件  平行成分は勾配0・垂直V=0")
sx0, sx1 = 90, 590
surf = 110       # 自由表面(上)
bot = 320        # 壁(下)
# 自由表面(波なしの水平線)
d.line((sx0, surf, sx1, surf), fill=BLUE, width=3)
ctext(d, 330, surf - 18, "自由表面 (水路上面)", FS, BLUE)
# 底=固体壁(滑りなし)
hwall(d, sx0, sx1, bot, side=1, n=16)
ctext(d, 330, bot + 22, "壁 (滑りなし u=0)", FT, GRAY)
# 速度プロフィル U(y): 表面で最大かつ勾配0, 壁で0
bxp = 150
prof = []
for j in range(0, 22):
    y = bot - j * (bot - surf) / 21
    frac = (bot - y) / (bot - surf)          # 0(壁)〜1(表面)
    U = 150 * (1 - (1 - frac) ** 2)           # 表面で dU/dy=0, 壁で0
    prof.append((bxp + U, y))
    if j % 3 == 0:
        arrow(d, bxp, y, bxp + U, y, GRAY, 1, 6)
d.line(prof, fill=RED, width=3, joint="curve")
d.line((bxp, surf, bxp, bot), fill=BLACK, width=1)
# 表面のSlip注記
node(d, bxp + 150, surf, r=5, fill=BLUE, col=BLUE)
ctext(d, bxp + 165, surf + 4, "dU/dy = 0 (Slip)", FT, BLUE, "lm")
# V=0(表面を横切らない)
arrow(d, 470, surf - 34, 470, surf - 6, GREEN, 2, 9)
d.line((452, surf, 488, surf), fill=GREEN, width=3)
ctext(d, 500, surf - 26, "V = 0 (波なし)", FT, GREEN, "lm")
note(d, "自由表面=平行成分は勾配0(Slip)・垂直V=0 / 壁の滑りなし(全成分0)とは別物")
save(im, "t2f7FreeSurface")


# ==================================================== t2f7WallCoord 壁座標 y+ と u_tau
im, d = new()
title(d, "壁座標  y+ と 摩擦速度 u_tau")
wx0, wx1, wy = 55, 375, 342
# 壁(下)
hwall(d, wx0, wx1, wy, side=1, n=11)
ctext(d, (wx0 + wx1) / 2, wy + 20, "壁面", FT, GRAY)
# y 軸(壁からの距離)
arrow(d, wx0 + 18, wy, wx0 + 18, 92, BLACK, 2, 11)
ctext(d, wx0 + 6, 86, "y", FS, BLACK, "rm")
# 3層の帯(y+ = 5, 30 の境界)
lv5 = wy - 58
lv30 = wy - 145
lv_top = wy - 232
dashed(d, wx0 + 18, lv5, wx1, lv5, LGRAY, 2, 7)
dashed(d, wx0 + 18, lv30, wx1, lv30, LGRAY, 2, 7)
ctext(d, wx0 + 30, (wy + lv5) / 2 + 2, "粘性底層 y+ <= 5", FT, BLUE, "lm")
ctext(d, wx0 + 30, (lv5 + lv30) / 2, "緩衝層 5 < y+ < 30", FT, GREEN, "lm")
ctext(d, wx0 + 30, (lv30 + lv_top) / 2, "対数層 y+ >= 30", FT, RED, "lm")
# 壁面第1格子点(対数層に置く・右寄せで層ラベルと分離)
node(d, wx0 + 262, lv30 - 52, r=6, fill="white", col=BLACK)
ctext(d, wx0 + 262, lv30 - 70, "壁面第1格子点", FT, BLACK)
# 壁面せん断応力 tau_w(壁面に沿って・右寄り)
arrow(d, wx0 + 205, wy - 6, wx0 + 300, wy - 6, RED, 3, 12)
ctext(d, wx0 + 252, wy - 22, "tau_w", FT, RED)
# 右: 定義(枠内・全て 660 内に収める)
dx0 = 400
d.line((dx0 - 8, 110, dx0 - 8, 320), fill=LGRAY, width=1)
defs = ["u_tau = sqrt(tau_w/rho)",
        "y+ = y u_tau / nu",
        "u+ = U / u_tau",
        "t_tau = qw/(rho cp u_tau)",
        "(温度側 T+ も同様)"]
for i, s in enumerate(defs):
    ctext(d, dx0, 132 + i * 38, s, FT, BLACK, "lm")
note(d, "壁の摩擦を基準にした無次元量で壁近傍を普遍化 / 壁関数は第1点を対数層へ")
save(im, "t2f7WallCoord")


# ==================================================== t2f7BLEdge 境界層外縁の条件
im, d = new()
title(d, "境界層外縁の境界条件  U=Ue(x)")
wx0, wx1, wy = 70, 610, 330
hwall(d, wx0, wx1, wy, side=1, n=20)
ctext(d, (wx0 + wx1) / 2, wy + 20, "壁 (滑りなし)", FT, GRAY)
# 境界層外縁 delta(x)(壁から成長する破線)
edge = []
for k in range(0, wx1 - wx0 - 20, 4):
    x = wx0 + 10 + k
    dlt = 150 * math.sqrt((k + 6) / (wx1 - wx0))
    edge.append((x, wy - dlt))
dashed_pts = edge
for i in range(0, len(dashed_pts) - 1, 2):
    d.line((dashed_pts[i][0], dashed_pts[i][1], dashed_pts[i + 1][0], dashed_pts[i + 1][1]), fill=GRAY, width=2)
ctext(d, wx1 - 120, wy - 150, "境界層外縁 delta(x)", FT, GRAY, "lm")
# 主流(外縁より上, 一様な Ue 矢印)
for k in range(4):
    yy = 92 + k * 20
    arrow(d, 110, yy, 210, yy, BLUE, 2, 9)
ctext(d, 300, 100, "主流  U = Ue(x)", FS, BLUE, "lm")
# 境界層内の速度プロフィル(2断面)
for xs in (230, 430):
    dlt = 150 * math.sqrt((xs - wx0 - 10 + 6) / (wx1 - wx0))
    pr = []
    for j in range(0, 21):
        y = wy - j * dlt / 20
        frac = (wy - y) / dlt
        U = 70 * (1 - (1 - frac) ** 2)
        pr.append((xs + U, y))
    d.line(pr, fill=RED, width=3, joint="curve")
    d.line((xs, wy, xs, wy - dlt), fill=BLACK, width=1)
    node(d, xs + 70, wy - dlt, r=4, fill=BLUE, col=BLUE)
ctext(d, 330, 372, "外縁圧力:  -1/rho dP/dx = Ue dUe/dx  (dUe/dx を使う)", FT, BLACK)
note(d, "外縁=主流速度Ueと整合する圧力勾配を指定 / 壁垂直速度は連続の式から求める")
save(im, "t2f7BLEdge")


print("ALL DONE")
