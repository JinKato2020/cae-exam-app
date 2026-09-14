# -*- coding: utf-8 -*-
"""固体力学1級 第7章 伝熱解析 の公式図(s1f7*)を描画。
白地660x420・黒線画・機構のみ・物理的に正確(装飾禁止)。
豆腐対策: ギリシャ/特殊記号はローマ字・英語に置換(lambda,sigma,epsilon,kappa,
rho,theta,alpha,dt,grad^2,T^4,degC 等)。接頭辞 s1f7 厳守(問題図 s1e7 と衝突させない)。"""
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


# ============================================================ s1f7HeatBalance 微小要素の熱収支
im, d = new()
title(d, "熱収支:  正味流入 = 蓄熱  ->  rho c dT/dt = lambda grad^2 T")
# 微小要素(正方形)
ex0, ey0, ex1, ey1 = 260, 165, 400, 285
d.rectangle((ex0, ey0, ex1, ey1), outline=BLACK, width=3, fill=FILL1)
ctext(d, (ex0 + ex1) / 2, (ey0 + ey1) / 2 - 12, "微小要素", FS)
ctext(d, (ex0 + ex1) / 2, (ey0 + ey1) / 2 + 12, "dx dy", FT, GRAY)
cy = (ey0 + ey1) / 2
cx = (ex0 + ex1) / 2
# x方向: 流入 qx (左), 流出 qx+dqx (右)
arrow(d, 150, cy, ex0, cy, RED, 3, 12)
ctext(d, 150, cy - 16, "qx (流入)", FT, RED, "lm")
arrow(d, ex1, cy, 510, cy, RED, 3, 12)
ctext(d, 512, cy - 16, "qx + dqx (流出)", FT, RED, "lm")
# y方向: 流入 qy (下), 流出 qy+dqy (上)
arrow(d, cx, 380, cx, ey1, BLUE, 3, 12)
ctext(d, cx + 8, 372, "qy (流入)", FT, BLUE, "lm")
arrow(d, cx, ey0, cx, 95, BLUE, 3, 12)
ctext(d, cx + 8, 88, "qy + dqy (流出)", FT, BLUE, "lm")
# 蓄熱の注記
ctext(d, cx, cy + 40, "溜まる熱 = rho c dT/dt", FT, GREEN)
note(d, "各方向の熱流束の差(勾配)の合計が要素に溜まり温度を上げる  (kappa=lambda/rho c)")
save(im, "s1f7HeatBalance")


# ============================================================ s1f7Fourier フーリエの法則
im, d = new()
title(d, "フーリエの法則  q = -lambda dT/dx  (高温->低温)")
# 平面壁
wx0, wx1, wy0, wy1 = 150, 470, 120, 300
d.rectangle((wx0, wy0, wx1, wy1), outline=BLACK, width=3, fill=FILL1)
ctext(d, (wx0 + wx1) / 2, wy1 + 22, "平面壁 (厚さ方向 x)", FT, GRAY)
# 高温側 T1 (左) 低温側 T2 (右)
ctext(d, wx0 - 8, wy0 - 4, "T1 高温", FT, RED, "rm")
ctext(d, wx1 + 8, wy1 + 4, "T2 低温", FT, BLUE, "lm")
# 温度分布(直線, 定常でlambda一定): 左上->右下
d.line((wx0, wy0 + 12, wx1, wy1 - 12), fill=BLACK, width=3)
node(d, wx0, wy0 + 12, r=5, fill=RED, col=RED)
node(d, wx1, wy1 - 12, r=5, fill=BLUE, col=BLUE)
ctext(d, (wx0 + wx1) / 2 - 10, (wy0 + wy1) / 2 - 26, "T(x) 直線分布", FT, BLACK)
# 熱流束の向き(高温->低温)
for yy in (150, 210, 270):
    arrow(d, wx0 + 20, yy, wx1 - 20, yy, GREEN, 2, 10)
ctext(d, (wx0 + wx1) / 2, 210 - 40, "熱流束 q ->", FT, GREEN)
# 勾配三角形
gx, gy = 350, 240
d.line((gx, gy, gx + 70, gy), fill=GRAY, width=2)
d.line((gx + 70, gy, gx + 70, gy + 34), fill=GRAY, width=2)
ctext(d, gx + 35, gy + 12, "dx", FT, GRAY)
ctext(d, gx + 92, gy + 17, "dT", FT, GRAY, "lm")
note(d, "勾配 dT/dx が負(x増で温度下降)のとき q は正 ・ lambda 大ほど同じ温度差でよく熱を通す")
save(im, "s1f7Fourier")


# ============================================================ s1f7BoundaryCond 境界条件4種
im, d = new()
title(d, "熱伝導の境界条件 4種")
# 2x2 パネル
panels = [
    (60, 70, "(1) 温度規定", "表面温度を与える", "T = Tbar", RED),
    (350, 70, "(2) 熱流束規定", "熱流束を与える (q=0 は断熱)", "q = qbar", BLUE),
    (60, 250, "(3) 熱伝達", "まわりの流体とやりとり", "q = h (T - Tf)", GREEN),
    (350, 250, "(4) ふく射", "放射でやりとり(T^4 -> 非線形)", "q = eps sigma F (T^4 - Tr^4)", ORANGE),
]
for px, py, lab, sub, eq, col in panels:
    w, h = 250, 160
    d.rectangle((px, py, px + w, py + h), outline=LGRAY, width=2)
    ctext(d, px + 12, py + 18, lab, FS, col, "lm")
    # 物体表面(左側の縦壁)と外向き法線
    sx = px + 30
    d.line((sx, py + 44, sx, py + h - 16), fill=BLACK, width=3)
    for i in range(5):
        yy = py + 50 + i * 20
        d.line((sx, yy, sx - 12, yy - 8), fill=BLACK, width=2)  # 物体側ハッチ(左)
    ny = py + 92
    if col == RED:
        ctext(d, sx + 6, ny - 26, "Tbar", FT, RED, "lm")
        d.line((sx, ny, sx + 90, ny), fill=RED, width=3)
    elif col == BLUE:
        arrow(d, sx, ny, sx + 90, ny, BLUE, 3, 11)
        ctext(d, sx + 96, ny, "qbar", FT, BLUE, "lm")
    elif col == GREEN:
        arrow(d, sx, ny, sx + 70, ny, GREEN, 3, 11)
        ctext(d, sx + 78, ny - 22, "流体 Tf", FT, GREEN, "lm")
        ctext(d, sx + 78, ny + 2, "h", FT, GREEN, "lm")
    else:
        for k, yy in enumerate((ny - 16, ny, ny + 16)):
            arrow(d, sx, yy, sx + 66, yy, ORANGE, 2, 9)
        ctext(d, sx + 74, ny, "放射 Tr", FT, ORANGE, "lm")
    ctext(d, px + w / 2, py + h - 30, eq, FT, BLACK)
    ctext(d, px + w / 2, py + h - 12, sub, FT, GRAY)
save(im, "s1f7BoundaryCond")


# ============================================================ s1f7FemMatrix FEM定式化
im, d = new()
title(d, "FEM 定式化:  [C]{dT/dt} + [K]{T} = {F}")
# [C] 熱容量マトリックス
cx0 = 70
matrix_grid(d, cx0, 150, [["c", "c"], ["c", "c"]], cell=42)
ctext(d, cx0 + 42, 132, "[C]", FS, BLUE)
ctext(d, cx0 + 42, 250, "熱容量", FT, BLUE)
ctext(d, cx0 + 42, 270, "(温まりにくさ)", FT, GRAY)
ctext(d, cx0 + 100, 192, "{dT/dt}", FT, BLACK, "lm")
ctext(d, cx0 + 178, 192, "+", F, BLACK, "lm")
# [K] 熱伝導マトリックス
kx0 = 320
matrix_grid(d, kx0, 150, [["k", "k"], ["k", "k"]], cell=42)
ctext(d, kx0 + 42, 132, "[K]", FS, GREEN)
ctext(d, kx0 + 42, 250, "熱伝導", FT, GREEN)
ctext(d, kx0 + 42, 270, "(+熱伝達境界)", FT, GRAY)
ctext(d, kx0 + 100, 192, "{T}", FT, BLACK, "lm")
ctext(d, kx0 + 150, 192, "=", F, BLACK, "lm")
# {F} 熱流束ベクトル
fx0 = 560
d.rectangle((fx0, 150, fx0 + 40, 234), outline=BLACK, width=2)
d.line((fx0, 192, fx0 + 40, 192), fill=BLACK, width=1)
ctext(d, fx0 + 20, 171, "F", FS)
ctext(d, fx0 + 20, 213, "F", FS)
ctext(d, fx0 + 20, 132, "{F}", FS, RED)
ctext(d, fx0 + 20, 250, "熱流束", FT, RED)
ctext(d, fx0 + 20, 270, "(発熱/規定/流体)", FT, GRAY)
note(d, "構造解析 Ku=f と相似 ・ 定常([C]項=0)では [K]{T}={F} ・ 断熱面は {F} に項が出ないだけ")
save(im, "s1f7FemMatrix")


# ============================================================ s1f7ThermalStress 熱応力
im, d = new()
title(d, "熱応力:  両端拘束 + 温度上昇 -> 圧縮応力")
# 上段: 自由なら伸びる(点線が元の長さ)
by = 150
wall(d, 120, by - 30, by + 30, 1, 6)
d.rectangle((120, by - 18, 430, by + 18), outline=BLACK, width=3, fill=FILL2)
ctext(d, 275, by, "自由に加熱 dT", FT)
dashed(d, 430, by - 30, 430, by + 30, LGRAY, 2)
arrow(d, 430, by, 500, by, GREEN, 3, 11)
ctext(d, 508, by, "自由なら dL=alpha dT L 伸びる", FT, GREEN, "lm")
# 下段: 両端拘束 -> 伸びられず圧縮応力
cy2 = 290
wall(d, 120, cy2 - 30, cy2 + 30, 1, 6)
wall(d, 540, cy2 - 30, cy2 + 30, -1, 6)
d.rectangle((132, cy2 - 18, 528, cy2 + 18), outline=BLACK, width=3, fill=FILL1)
ctext(d, 330, cy2 - 2, "両端拘束で加熱 dT", FT)
# 圧縮を表す内向き矢印
arrow(d, 210, cy2, 160, cy2, RED, 3, 11)
arrow(d, 450, cy2, 500, cy2, RED, 3, 11)
ctext(d, 330, cy2 + 28, "sigma = -E alpha dT (圧縮)", FT, RED)
note(d, "拘束 + 温度差で内部応力 ・ 急加熱ほど温度勾配が急で過渡的にピーク大 -> 非定常解析が重要")
save(im, "s1f7ThermalStress")


# ============================================================ s1f7StefanBoltzmann E=sigma T^4
im, d = new()
title(d, "ステファンボルツマン則  Eb = sigma T^4  (絶対温度)")
ox, oy, xl, yl = 110, 350, 470, 285
axes(d, ox, oy, xl + 12, yl + 15, "T (絶対温度 K)", "Eb (放射)")
xmax = 2.2
m = mapper(ox, oy, xl, yl, 0, xmax, 0, xmax ** 4)
pts = [m(xmax * i / 200, (xmax * i / 200) ** 4) for i in range(201)]
plot(d, 0, 0, pts, RED, 3)
ctext(d, ox + xl * 0.62, oy - yl * 0.55, "T^4 に比例(急増)", FS, RED, "lm")
# T倍増 -> 16倍
T0 = 1.0
p1 = m(T0, T0 ** 4)
p2 = m(2 * T0, (2 * T0) ** 4)
node(d, p1[0], p1[1], r=5, fill=RED, col=RED)
node(d, p2[0], p2[1], r=5, fill=RED, col=RED)
dashed(d, p2[0], p2[1], p2[0], oy, LGRAY, 2)
dashed(d, p2[0], p2[1], ox, p2[1], LGRAY, 2)
ctext(d, p1[0] + 8, p1[1] - 12, "T", FT, GRAY, "lm")
ctext(d, p2[0], oy + 16, "2T", FT, GRAY)
ctext(d, ox - 6, p2[1], "16 倍", FT, GRAY, "rm")
note(d, "T が 2倍 -> 放射は 2^4 = 16倍 ・ 灰色体は E = eps sigma T^4 (eps<1)")
save(im, "s1f7StefanBoltzmann")


# ============================================================ s1f7ParallelPlate 平行2平板
im, d = new()
title(d, "平行2平板のふく射  Q = f sigma (T1^4 - T2^4)")
# 2枚の平行平板
p1x, p2x = 180, 470
py0, py1 = 120, 310
d.rectangle((p1x - 16, py0, p1x, py1), outline=BLACK, width=3, fill=FILL2)
d.rectangle((p2x, py0, p2x + 16, py1), outline=BLACK, width=3, fill=FILL2)
ctext(d, p1x - 8, py0 - 18, "面1", FT, RED)
ctext(d, p2x + 8, py0 - 18, "面2", FT, BLUE)
ctext(d, p1x - 8, py1 + 18, "T1, eps1", FT, RED)
ctext(d, p2x + 8, py1 + 18, "T2, eps2", FT, BLUE)
# 多重反射(放射と反射を繰り返す)
arrow(d, p1x + 2, 165, p2x - 2, 165, RED, 2, 10)
dashed(d, p2x - 2, 195, p1x + 2, 195, GRAY, 2)  # 反射
arrow(d, p1x + 2, 225, p2x - 2, 225, RED, 2, 10)
dashed(d, p2x - 2, 255, p1x + 2, 255, GRAY, 2)
ctext(d, (p1x + p2x) / 2, 285, "多重反射 -> 係数 f", FT, GRAY)
# f の式
ctext(d, W / 2, 350, "f = 1 / ( 1/eps1 + 1/eps2 - 1 )", FS, BLACK)
note(d, "両面が黒体(eps=1)なら f=1 ・ よく反射する面(eps小)ほど f 小でふく射伝熱が減る")
save(im, "s1f7ParallelPlate")


# ============================================================ s1f7RadShield 放射シールド
im, d = new()
title(d, "放射シールド:  薄板1枚挿入で伝熱が半分")
# 左: シールド無し Q
lx1, lx2 = 70, 240
py0, py1 = 130, 300
d.rectangle((lx1 - 14, py0, lx1, py1), outline=BLACK, width=3, fill=FILL2)
d.rectangle((lx2, py0, lx2 + 14, py1), outline=BLACK, width=3, fill=FILL2)
ctext(d, lx1 - 7, py0 - 18, "T1", FT, RED)
ctext(d, lx2 + 7, py0 - 18, "T2", FT, BLUE)
arrow(d, lx1 + 2, 215, lx2 - 2, 215, RED, 4, 13)
ctext(d, (lx1 + lx2) / 2, 195, "Q", FS, RED)
ctext(d, (lx1 + lx2) / 2, 320, "シールド無し", FT, GRAY)
# 右: シールド1枚 -> Q/2
rx1, rx2 = 400, 590
sh = (rx1 + rx2) / 2
d.rectangle((rx1 - 14, py0, rx1, py1), outline=BLACK, width=3, fill=FILL2)
d.rectangle((rx2, py0, rx2 + 14, py1), outline=BLACK, width=3, fill=FILL2)
d.rectangle((sh - 6, py0 + 10, sh + 6, py1 - 10), outline=BLACK, width=3, fill=FILL3)
ctext(d, rx1 - 7, py0 - 18, "T1", FT, RED)
ctext(d, rx2 + 7, py0 - 18, "T2", FT, BLUE)
ctext(d, sh, py0 - 18, "薄板", FT, GREEN)
arrow(d, rx1 + 2, 215, sh - 8, 215, RED, 3, 11)
arrow(d, sh + 8, 215, rx2 - 2, 215, RED, 3, 11)
ctext(d, (rx1 + sh) / 2 - 4, 195, "Q/2", FT, RED)
ctext(d, (rx1 + rx2) / 2, 320, "シールド1枚 (直列抵抗2段)", FT, GRAY)
d.line((330, 110, 330, 340), fill=LGRAY, width=2)
note(d, "放射率が等しければ 薄板1枚で Q -> Q/2 ・ N枚で Q/(N+1) (多層断熱 MLI の原理)")
save(im, "s1f7RadShield")


# ============================================================ s1f7ViewFactor 形態係数と相反則
im, d = new()
title(d, "形態係数と相反則  Ai Fij = Aj Fji")
# 面i(左, 大) と 面j(右, 小)
ix, iy0, iy1 = 150, 130, 320
jx, jy0, jy1 = 480, 175, 285
d.line((ix, iy0, ix, iy1), fill=BLACK, width=4)
d.line((jx, jy0, jx, jy1), fill=BLACK, width=4)
ctext(d, ix - 12, (iy0 + iy1) / 2, "面 i", FS, RED, "rm")
ctext(d, ix - 12, (iy0 + iy1) / 2 + 22, "面積 Ai", FT, GRAY, "rm")
ctext(d, jx + 12, (jy0 + jy1) / 2, "面 j", FS, BLUE, "lm")
ctext(d, jx + 12, (jy0 + jy1) / 2 + 22, "面積 Aj", FT, GRAY, "lm")
# i から出た放射のうち j に届く割合 Fij (届く線)
for ty in (iy0 + 30, (iy0 + iy1) / 2, iy1 - 30):
    for jyt in (jy0 + 20, (jy0 + jy1) / 2, jy1 - 20):
        pass
# i中心から j へ届く扇状の線束
icy = (iy0 + iy1) / 2
for jyt in (jy0 + 15, (jy0 + jy1) / 2, jy1 - 15):
    arrow(d, ix + 2, icy, jx - 2, jyt, GREEN, 2, 9)
# i から外れる(j に届かない)放射
dashed(d, ix + 2, iy0 + 20, ix + 130, iy0 - 10, LGRAY, 2)
dashed(d, ix + 2, iy1 - 20, ix + 130, iy1 + 30, LGRAY, 2)
ctext(d, (ix + jx) / 2, icy - 78, "Fij = i から j に届く割合", FT, GREEN)
ctext(d, (ix + jx) / 2, icy + 84, "(0 <= Fij <= 1, 温度に依らず幾何のみ)", FT, GRAY)
note(d, "凸/平面は Fii=0 ・ 閉空間は sum_j Fij = 1 ・ 相反則 Ai Fij = Aj Fji")
save(im, "s1f7ViewFactor")

print("done")
