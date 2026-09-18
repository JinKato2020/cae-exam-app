# -*- coding: utf-8 -*-
"""熱流体2級 第4章 数値計算法 の公式図(t2f4*)を描画。
白地660x420・黒線画・機構のみ(装飾禁止)。
豆腐対策: ギリシャ/特殊記号はローマ字表記(Delta,phi,omega,alpha,u,x_i 等)。
接頭辞 t2f4 厳守(問題図 t2e4 と衝突させない・§13)。"""
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


# ============================================================ t2f4PdeType 型判別(数直線)
im, d = new()
title(d, "偏微分方程式の型判別  D = B^2 - 4AC")
ax_y = 175
ox, xl = 90, 480
arrow(d, ox, ax_y, ox + xl, ax_y, BLACK, 2, 11)
ctext(d, ox + xl + 12, ax_y, "D", FS, BLACK, "lm")
zero_x = ox + xl * 0.5
d.line((zero_x, ax_y - 10, zero_x, ax_y + 10), fill=BLACK, width=2)
ctext(d, zero_x, ax_y + 24, "D = 0", FT, GRAY)
# 3領域
ctext(d, ox + xl * 0.24, ax_y - 46, "D < 0", FS, BLUE)
ctext(d, ox + xl * 0.24, ax_y - 22, "楕円型", F, BLUE)
ctext(d, zero_x, ax_y - 70, "D = 0", FS, GREEN)
ctext(d, zero_x, ax_y - 46, "放物型", F, GREEN)
ctext(d, ox + xl * 0.78, ax_y - 46, "D > 0", FS, RED)
ctext(d, ox + xl * 0.78, ax_y - 22, "双曲型", F, RED)
# 例と物理対応
ctext(d, ox + xl * 0.24, ax_y + 70, "u_xx + u_yy = 0", FT, BLUE)
ctext(d, ox + xl * 0.24, ax_y + 92, "ラプラス(定常場)", FT, GRAY)
ctext(d, zero_x, ax_y + 118, "u_xx = u_y", FT, GREEN)
ctext(d, zero_x, ax_y + 140, "熱伝導(拡散)", FT, GRAY)
ctext(d, ox + xl * 0.78, ax_y + 70, "u_xx = u_yy", FT, RED)
ctext(d, ox + xl * 0.78, ax_y + 92, "波動(振動)", FT, GRAY)
note(d, "一般形の係数から判別式 D=B^2-4AC を作り、符号で3つの型に分類する")
save(im, "t2f4PdeType")


# ============================================================ t2f4Discretize 離散化3方式
im, d = new()
title(d, "離散化手法  FDM / FVM / FEM")
# --- FDM: 格子点に量 ---
bx0, by0, bs = 70, 130, 40
ctext(d, bx0 + bs, by0 - 30, "有限差分法 FDM", FT, BLACK)
for i in range(4):
    for j in range(4):
        x, y = bx0 + i * bs, by0 + j * bs
        d.line((bx0, y, bx0 + 3 * bs, y), fill=LGRAY, width=1)
        d.line((x, by0, x, by0 + 3 * bs), fill=LGRAY, width=1)
for i in range(4):
    for j in range(4):
        node(d, bx0 + i * bs, by0 + j * bs, r=4, fill=BLUE, col=BLUE)
ctext(d, bx0 + bs * 1.5, by0 + 3 * bs + 26, "格子点に値", FT, GRAY)
# --- FVM: 検査体積+フラックス ---
cx0 = 285
d.line((cx0 - 10, by0, cx0 + 3 * bs + 10, by0), fill=LGRAY, width=1)
ctext(d, cx0 + bs * 1.5, by0 - 30, "有限体積法 FVM", FT, BLACK)
vx, vy = cx0 + bs * 0.5, by0 + bs * 0.7
d.rectangle((vx, vy, vx + 2 * bs, vy + 1.6 * bs), outline=BLACK, width=3, fill=FILL1)
node(d, vx + bs, vy + 0.8 * bs, r=5, fill=BLACK, col=BLACK)
arrow(d, vx - 26, vy + 0.8 * bs, vx, vy + 0.8 * bs, GREEN, 3, 11)
arrow(d, vx + 2 * bs, vy + 0.8 * bs, vx + 2 * bs + 26, vy + 0.8 * bs, GREEN, 3, 11)
arrow(d, vx + bs, vy - 26, vx + bs, vy, GREEN, 3, 11)
arrow(d, vx + bs, vy + 1.6 * bs, vx + bs, vy + 1.6 * bs + 26, GREEN, 3, 11)
ctext(d, vx + bs, vy + 0.8 * bs + 30, "検査体積", FT, GRAY)
ctext(d, cx0 + bs * 1.5, by0 + 3 * bs + 26, "界面フラックスで保存", FT, GRAY)
# --- FEM: 三角形要素 ---
ex0 = 500
ctext(d, ex0 + bs, by0 - 30, "有限要素法 FEM", FT, BLACK)
P = [(ex0, by0 + 2.4 * bs), (ex0 + 2 * bs, by0 + 2.6 * bs), (ex0 + 0.9 * bs, by0 + 0.6 * bs),
     (ex0 + 2.3 * bs, by0 + 0.9 * bs)]
d.polygon([P[0], P[1], P[2]], outline=BLACK, width=2, fill=FILL1)
d.polygon([P[1], P[3], P[2]], outline=BLACK, width=2, fill=FILL2)
for p in P:
    node(d, p[0], p[1], r=4, fill=RED, col=RED)
ctext(d, ex0 + bs, by0 + 3 * bs + 26, "要素+基底関数(弱形式)", FT, GRAY)
note(d, "FDM=格子点に値 / FVM=検査体積で保存則 / FEM=要素の基底関数 / スペクトル法=波数")
save(im, "t2f4Discretize")


# ============================================================ t2f4Stencil 5点ステンシル
im, d = new()
title(d, "ラプラス方程式の5点ステンシル")
cx, cy, s = 330, 220, 92
# 十字に4近傍
nb = [(cx, cy - s, "phi(i,j+1)", "+1"), (cx, cy + s, "phi(i,j-1)", "+1"),
      (cx - s, cy, "phi(i-1,j)", "+1"), (cx + s, cy, "phi(i+1,j)", "+1")]
for (x, y, lab, cf) in nb:
    d.line((cx, cy, x, y), fill=LGRAY, width=2)
for (x, y, lab, cf) in nb:
    node(d, x, y, r=22, fill=FILL2, col=BLACK)
    ctext(d, x, y, cf, FS, BLUE)
node(d, cx, cy, r=26, fill=(255, 236, 236), col=RED)
ctext(d, cx, cy, "-4", F, RED)
ctext(d, cx, cy - s - 34, "phi(i,j+1)", FT, GRAY)
ctext(d, cx, cy + s + 34, "phi(i,j-1)", FT, GRAY)
ctext(d, cx - s, cy + 40, "phi(i-1,j)", FT, GRAY)
ctext(d, cx + s, cy + 40, "phi(i+1,j)", FT, GRAY)
ctext(d, cx, 360, "phi(i+1,j)+phi(i-1,j)+phi(i,j+1)+phi(i,j-1) - 4 phi(i,j) = 0", FS, BLACK)
note(d, "Delta x=Delta y なら内点値=上下左右4点の平均 / ポアソンは右辺に Delta x^2 f")
save(im, "t2f4Stencil")


# ============================================================ t2f4Upwind 対流項の差分方向
im, d = new()
title(d, "対流項の差分スキーム  (流れ u>0 は上流=左側を使う)")
xs = [130, 250, 370, 490, 610]
labs = ["x_{i-2}", "x_{i-1}", "x_i", "x_{i+1}", ""]
gy = 180
d.line((110, gy, 590, gy), fill=BLACK, width=2)
for k in range(4):
    x = xs[k]
    node(d, x, gy, r=7, fill="white", col=BLACK)
    ctext(d, x, gy + 26, labs[k], FT, GRAY)
# 流れの向き
arrow(d, 150, 118, 430, 118, BLUE, 3, 13)
ctext(d, 300, 100, "流れ u > 0", FS, BLUE)
# 1次風上: i と i-1
d.line((xs[1], gy, xs[2], gy), fill=RED, width=5)
ctext(d, 330, 250, "1次風上: x_i と x_{i-1} (上流2点)", FS, RED)
# 2次中心: i-1 と i+1
dashed(d, xs[1], gy + 40, xs[3], gy + 40, GREEN, 3, 10)
ctext(d, xs[2], gy + 40, "o", FS, GREEN)
ctext(d, 330, 290, "2次中心: x_{i-1} と x_{i+1} (前後対称)", FS, GREEN)
ctext(d, 330, 330, "QUICK/2次風上: 上流寄りに3点以上", FS, GRAY)
note(d, "u<0 では上流が反対側 / 風上=安定・数値粘性大, 中心=高精度・振動しやすい")
save(im, "t2f4Upwind")


# ============================================================ t2f4TimeScheme 時間発展(陽/陰)
im, d = new()
title(d, "時間発展法  陽解法 と 陰解法")
# 時間軸(横)に n-1, n, n+1
tx = {"n-1": 150, "n": 330, "n+1": 510}
ty = 260
d.line((100, ty, 560, ty), fill=BLACK, width=2)
arrow(d, 560, ty, 590, ty, BLACK, 2, 10)
ctext(d, 600, ty, "t", FS, BLACK, "lm")
for lab, x in tx.items():
    d.line((x, ty - 8, x, ty + 8), fill=BLACK, width=2)
    node(d, x, ty, r=7, fill="white", col=BLACK)
    ctext(d, x, ty + 26, lab, FT, GRAY)
# 陽: L を n で評価 -> n+1 を直接(軸の上)
arrow(d, tx["n"], ty - 20, tx["n+1"], ty - 20, BLUE, 3, 12)
ctext(d, (tx["n"] + tx["n+1"]) / 2, ty - 40, "陽: L^n で更新", FS, BLUE)
ctext(d, (tx["n"] + tx["n+1"]) / 2, ty - 62, "(行列不要・条件付き安定)", FT, GRAY)
# 陰: 未来値 n+1 を使う(軸の下・右に小さな上向き矢印)
arrow(d, tx["n+1"] + 26, ty + 40, tx["n+1"] + 26, ty + 8, RED, 3, 12)
ctext(d, 330, ty + 66, "陰: L^{n+1} を含む → 行列が必要・無条件安定", FS, RED)
ctext(d, 330, ty + 96, "クランク・ニコルソン = (L^n + L^{n+1})/2  (2次精度)", FS, GREEN)
note(d, "陽=現在値で更新 / 陰=未来値を含む / CN=平均で2次精度 / AB=多段の陽解法")
save(im, "t2f4TimeScheme")


# ============================================================ t2f4CFL クーラン数
im, d = new()
title(d, "クーラン数  C = u Delta t / Delta x")
# 格子セル(幅 Delta x)
gy = 210
gx0 = 90
dx = 100
for k in range(5):
    x = gx0 + k * dx
    d.line((x, gy - 18, x, gy + 18), fill=BLACK, width=2)
d.line((gx0, gy, gx0 + 4 * dx, gy), fill=BLACK, width=2)
dim(d, gx0, gy + 46, gx0 + dx, gy + 46, "Delta x (格子幅)", col=GRAY)
# 1ステップで進む距離 u Delta t
node(d, gx0, gy - 60, r=6, fill=BLUE, col=BLUE)
travel = dx * 0.8   # C<1 の例
arrow(d, gx0, gy - 60, gx0 + travel, gy - 60, BLUE, 4, 14)
node(d, gx0 + travel, gy - 60, r=6, fill=BLUE, col=BLUE)
ctext(d, gx0 + travel / 2, gy - 82, "u Delta t (1ステップの伝達距離)", FT, BLUE)
dashed(d, gx0 + travel, gy - 60, gx0 + travel, gy + 18, LGRAY, 2)
ctext(d, 330, 320, "C = (伝達距離 u Delta t) / (格子幅 Delta x)", FS, BLACK)
ctext(d, 330, 350, "陽解法の安定条件:  C <= 1  (1ステップで1セル以内)", FS, RED)
note(d, "C>1 は情報が1セルを飛び越え破綻 ・ 格子を細かくすると許される Delta t も小さくなる")
save(im, "t2f4CFL")


# ============================================================ t2f4Iteration 反復解法の収束
im, d = new()
title(d, "反復解法の収束  (残差の減り方)")
ox, oy, xl, yl = 110, 340, 470, 250
axes(d, ox, oy, xl + 14, yl + 16, "反復", "残差")
m = mapper(ox, oy, xl, yl, 0, 10, 0, 1.0)
# 3つの減衰曲線: SOR最速 > GS > Jacobi
def decay(rate):
    return [m(t * 0.2, math.exp(-rate * t * 0.2)) for t in range(51)]
plot(d, 0, 0, decay(0.30), GRAY, 3)   # Jacobi
plot(d, 0, 0, decay(0.55), BLUE, 3)   # Gauss-Seidel
plot(d, 0, 0, decay(1.05), RED, 3)    # SOR
ctext(d, ox + xl * 0.62, oy - yl * 0.55, "ヤコビ (遅い)", FT, GRAY, "lm")
ctext(d, ox + xl * 0.40, oy - yl * 0.40, "ガウス・ザイデル", FT, BLUE, "lm")
ctext(d, ox + xl * 0.22, oy - yl * 0.30, "SOR (最速)", FT, RED, "lm")
note(d, "収束の速さ ヤコビ<ガウス・ザイデル<SOR / SOR は omega(1<omega<2)で加速")
save(im, "t2f4Iteration")


# ============================================================ t2f4Runge ルンゲ現象
im, d = new()
title(d, "補間  ルンゲ現象(高次多項式) と スプライン")
ox, oy, xl, yl = 90, 250, 500, 150
# データ点(等間隔)
xs = [-1 + 2 * k / 6 for k in range(7)]
def f(x):
    return 1.0 / (1.0 + 25 * x * x)   # ルンゲ関数
m = mapper(ox, oy, xl, yl, -1.1, 1.1, -0.35, 1.05)
# 軸
d.line((ox, oy, ox + xl, oy), fill=LGRAY, width=1)
# スプライン(滑らか=元関数に近い)
sp = [m(-1 + 2 * k / 200, f(-1 + 2 * k / 200)) for k in range(201)]
plot(d, 0, 0, sp, BLUE, 3)
# 高次多項式の振動(端で暴れる)を模式的に
poly = []
for k in range(201):
    x = -1 + 2 * k / 200
    osc = f(x) + 0.55 * (x ** 6) * math.cos(9 * x) * (abs(x) > 0.55)
    poly.append(m(x, osc))
for i in range(len(poly) - 1):
    dashed(d, poly[i][0], poly[i][1], poly[i + 1][0], poly[i + 1][1], RED, 2, 8)
# データ点
for x in xs:
    px, py = m(x, f(x))
    node(d, px, py, r=5, fill=BLACK, col=BLACK)
ctext(d, ox + xl * 0.5, oy - yl - 8, "スプライン: 滑らかに全点通過", FT, BLUE)
ctext(d, ox + xl * 0.88, oy - yl * 0.2, "端で振動", FT, RED)
ctext(d, ox + xl * 0.05, oy - yl * 0.2, "端で振動", FT, RED)
note(d, "高次多項式は端で振動=ルンゲ現象 / スプラインは区分多項式で滑らかに全点通過")
save(im, "t2f4Runge")


print("done")
