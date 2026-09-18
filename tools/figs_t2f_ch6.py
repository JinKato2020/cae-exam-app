# -*- coding: utf-8 -*-
"""熱流体2級 第6章 乱流モデル の公式図(t2f6*)を描画。
白地660x420・黒線画・機構のみ(装飾禁止)。
豆腐対策: ギリシャ/特殊記号はローマ字表記(nu_t,epsilon,k,Cmu,Prt,Re,omega,Delta,y+ 等)。
接頭辞 t2f6 厳守(問題図 t2e6 と衝突させない・§13)。"""
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


def blob(d, cx, cy, r, col=BLUE, wd=2, seed=0, wob=0.28, npt=28):
    """不規則な渦(閉曲線)。"""
    pts = []
    for k in range(npt + 1):
        t = 2 * math.pi * k / npt
        rr = r * (1 + wob * math.sin(3 * t + seed) * 0.6 + wob * math.cos(2 * t + seed * 1.7) * 0.4)
        pts.append((cx + rr * math.cos(t), cy + rr * 0.85 * math.sin(t)))
    d.line(pts, fill=col, width=wd, joint="curve")


# ============================================================ t2f6ReynoldsAvg レイノルズ分解
im, d = new()
title(d, "レイノルズ分解  u = U(平均) + u'(変動)")
ox, oy, xlen, ylen = 80, 250, 500, 150
axes(d, ox, oy, xlen, ylen + 40, "t (時間)", "u")
# 平均線
umean = oy - 70
d.line((ox, umean, ox + xlen, umean), fill=BLUE, width=3)
ctext(d, ox + xlen + 8, umean, "U", FS, BLUE, "lm")
# 瞬時値(平均まわりに変動)
pts = []
for k in range(0, xlen + 1, 4):
    x = ox + k
    fl = 34 * (math.sin(k * 0.07) + 0.5 * math.sin(k * 0.19 + 1) + 0.3 * math.sin(k * 0.41 + 2))
    pts.append((x, umean - fl))
d.line(pts, fill=RED, width=2, joint="curve")
ctext(d, ox + xlen + 8, umean - 46, "u=U+u'", FT, RED, "lm")
# 変動幅の注記
kk = 250
xk = ox + kk
flk = 34 * (math.sin(kk * 0.07) + 0.5 * math.sin(kk * 0.19 + 1) + 0.3 * math.sin(kk * 0.41 + 2))
dim(d, xk, umean, xk, umean - flk, "u'", col=GRAY)
ctext(d, 330, 78, "瞬時値 = 平均U + 変動u'  ->  平均でレイノルズ応力 -u_i'u_j' が出現", FS, BLACK)
note(d, "RANS=平均量のみを解く / 変動の相関(レイノルズ応力)はモデル化が必要(クロージャ)")
save(im, "t2f6ReynoldsAvg")


# ============================================================ t2f6EddyViscosity 渦粘性の考え方
im, d = new()
title(d, "渦粘性近似  nu_t = Cmu k^2 / eps")
# 左: 分子粘性(小さな分子)
ctext(d, 175, 78, "分子粘性 nu (分子運動)", FS, BLUE)
d.rectangle((70, 110, 290, 300), outline=BLACK, width=2)
import random
random.seed(3)
for _ in range(26):
    px = 80 + random.random() * 200
    py = 120 + random.random() * 170
    node(d, px, py, r=3, fill=BLUE, col=BLUE)
    a = random.random() * 2 * math.pi
    arrow(d, px, py, px + 12 * math.cos(a), py + 12 * math.sin(a), GRAY, 1, 5)
ctext(d, 175, 318, "小さな分子が運動量を運ぶ", FT, GRAY)
# 右: 乱流の渦(大小の渦で激しく混合)
ctext(d, 490, 78, "乱流の渦 nu_t (大小の渦)", FS, RED)
d.rectangle((380, 110, 600, 300), outline=BLACK, width=2)
blob(d, 440, 165, 30, RED, 2, 0.3)
blob(d, 530, 150, 40, RED, 2, 1.1)
blob(d, 500, 240, 34, RED, 2, 2.0)
blob(d, 430, 250, 22, RED, 2, 3.1)
blob(d, 560, 225, 18, RED, 2, 0.8)
ctext(d, 490, 318, "渦が激しく混ぜる=見かけの粘性大", FT, GRAY)
arrow(d, 300, 205, 372, 205, BLACK, 3, 13)
ctext(d, 336, 188, "類似", FT, BLACK)
ctext(d, 330, 348, "nu_t は分子動粘性と同じ次元[m^2/s] -> nu_t ∝ k^2/eps (kは2乗, epsで割る)", FS, BLACK)
note(d, "渦粘性近似(ブシネスク): レイノルズ応力を nu_t x 平均速度勾配 で近似 / Cmu=0.09")
save(im, "t2f6EddyViscosity")


# ============================================================ t2f6ReynoldsStress レイノルズ応力テンソル
im, d = new()
title(d, "レイノルズ応力テンソル  R_ij = u_i' u_j'")
vals = [["u'u'", "u'v'", "u'w'"],
        ["v'u'", "v'v'", "v'w'"],
        ["w'u'", "w'v'", "w'w'"]]
gx, gy, cell = 120, 120, 66
matrix_grid(d, gx, gy, vals, cell=cell)
# 対角を青枠で強調
for i in range(3):
    d.rectangle((gx + i * cell, gy + i * cell, gx + (i + 1) * cell, gy + (i + 1) * cell), outline=BLUE, width=4)
ctext(d, gx + 1.5 * cell, gy - 22, "対角=垂直応力(青)", FS, BLUE)
# 右側の説明
rx = gx + 3 * cell + 40
ctext(d, rx, gy + 20, "対角 (青枠)", FS, BLUE, "lm")
ctext(d, rx, gy + 46, "= レイノルズ垂直応力", FT, BLACK, "lm")
ctext(d, rx, gy + 92, "非対角", FS, RED, "lm")
ctext(d, rx, gy + 118, "= レイノルズせん断応力", FT, BLACK, "lm")
ctext(d, rx, gy + 164, "対称: R_ij = R_ji", FT, GRAY, "lm")
d.line((gx, gy + 3 * cell + 30, gx + 3 * cell, gy + 3 * cell + 30), fill=GRAY, width=1)
ctext(d, gx + 1.5 * cell, gy + 3 * cell + 52, "u'u' + v'v' + w'w' = 2k  (kではなく2k)", FS, BLACK)
note(d, "対角=垂直応力 / 非対角=せん断応力 / 対称テンソル / 対角和=2k")
save(im, "t2f6ReynoldsStress")


# ============================================================ t2f6DnsLesRans 3階層の解像度
im, d = new()
title(d, "乱流計算の3階層  DNS / LES / RANS")
cols = [("DNS", 60, BLUE, "全ての渦を直接計算", "モデルなし"),
        ("LES", 245, GREEN, "格子以上=直接計算", "格子以下=SGSモデル"),
        ("RANS", 430, RED, "平均量のみ計算", "全変動をモデル化")]
for name, x, col, l1, l2 in cols:
    d.rectangle((x, 90, x + 170, 300), outline=col, width=3)
    ctext(d, x + 85, 108, name, F, col)
    d.line((x, 126, x + 170, 126), fill=col, width=2)
random.seed(7)
# DNS: 大小いろいろな渦を細かく
for _ in range(9):
    blob(d, 60 + 30 + random.random() * 110, 150 + random.random() * 120, 8 + random.random() * 20, BLUE, 2, random.random() * 6)
ctext(d, 145, 314, "解像 最も細かい", FT, GRAY)
# LES: 大きな渦のみ + 薄いモデル格子
for _ in range(4):
    blob(d, 245 + 30 + random.random() * 110, 160 + random.random() * 100, 20 + random.random() * 16, GREEN, 2, random.random() * 6)
for j in range(6):
    d.line((250, 140 + j * 26, 410, 140 + j * 26), fill=LGRAY, width=1)
ctext(d, 330, 314, "中間", FT, GRAY)
# RANS: 平均のなめらかな分布のみ
for j in range(4):
    yy = 250 - j * 30
    xx = 445 + j * 34
    d.line((445, yy, xx, yy), fill=RED, width=2)
    arrow(d, 445, yy, xx, yy, RED, 2, 8)
ctext(d, 515, 314, "解像 最も粗い", FT, GRAY)
ctext(d, 330, 340, "格子点数・計算時間: DNS > LES > RANS   /   DNS格子点 N ∝ Re^(9/4)", FS, BLACK)
note(d, "Re を10倍 -> DNS格子点は 10^(9/4)≒180倍に急増(高Reで非現実的)")
save(im, "t2f6DnsLesRans")


# ============================================================ t2f6KeVsRsm k-e vs 応力モデル
im, d = new()
title(d, "k-eps モデル と 応力モデル(RSM)")
rows = [("解く量", "k と eps (2本)", "各レイノルズ応力\n成分の輸送方程式"),
        ("応力の扱い", "等方な渦粘性で近似", "非等方性を直接表現"),
        ("計算コスト", "低い", "高い"),
        ("安定性", "良い", "劣る"),
        ("向く流れ", "一般的なせん断流", "旋回流・二次流れ\n(非等方性が重要)")]
x0, y0 = 60, 78
wlab, wa, wb, rh = 130, 200, 210, 56
# ヘッダ
d.rectangle((x0 + wlab, y0, x0 + wlab + wa, y0 + 40), outline=BLUE, width=3)
ctext(d, x0 + wlab + wa / 2, y0 + 20, "k-eps モデル", FS, BLUE)
d.rectangle((x0 + wlab + wa, y0, x0 + wlab + wa + wb, y0 + 40), outline=RED, width=3)
ctext(d, x0 + wlab + wa + wb / 2, y0 + 20, "応力モデル RSM", FS, RED)
for i, (lab, a, b) in enumerate(rows):
    yy = y0 + 40 + i * rh
    d.rectangle((x0, yy, x0 + wlab, yy + rh), outline=GRAY, width=2)
    ctext(d, x0 + wlab / 2, yy + rh / 2, lab, FT, BLACK)
    d.rectangle((x0 + wlab, yy, x0 + wlab + wa, yy + rh), outline=GRAY, width=2)
    d.rectangle((x0 + wlab + wa, yy, x0 + wlab + wa + wb, yy + rh), outline=GRAY, width=2)
    for j, s in enumerate(a.split("\n")):
        ctext(d, x0 + wlab + wa / 2, yy + rh / 2 - 9 * (len(a.split("\n")) - 1) + j * 18, s, FT, BLACK)
    for j, s in enumerate(b.split("\n")):
        ctext(d, x0 + wlab + wa + wb / 2, yy + rh / 2 - 9 * (len(b.split("\n")) - 1) + j * 18, s, FT, BLACK)
note(d, "k-eps=低コスト・安定だが非等方性は苦手 / RSM=非等方性を表現できるが高コスト・低安定")
save(im, "t2f6KeVsRsm")


# ============================================================ t2f6TurbPrandtl 乱流プラントル数
im, d = new()
title(d, "乱流熱流束と乱流プラントル数  Prt = nu_t / alpha_t")
# 左: 運動量の乱流輸送
ctext(d, 175, 82, "運動量の乱流輸送", FS, BLUE)
d.rectangle((70, 108, 290, 250), outline=BLUE, width=2)
blob(d, 150, 150, 26, BLUE, 2, 0.5)
blob(d, 220, 190, 30, BLUE, 2, 1.6)
arrow(d, 100, 230, 260, 230, BLUE, 2, 9)
ctext(d, 180, 270, "渦粘性 nu_t が運ぶ", FT, GRAY)
# 右: 熱の乱流輸送
ctext(d, 490, 82, "熱の乱流輸送", FS, RED)
d.rectangle((380, 108, 600, 250), outline=RED, width=2)
blob(d, 460, 150, 26, RED, 2, 0.5)
blob(d, 530, 190, 30, RED, 2, 1.6)
ctext(d, 490, 168, "熱", FS, RED)
ctext(d, 490, 270, "熱の渦拡散係数 alpha_t が運ぶ", FT, GRAY)
arrow(d, 300, 178, 372, 178, BLACK, 3, 12)
ctext(d, 336, 160, "類似", FT, BLACK)
ctext(d, 330, 312, "両者の比 = 乱流プラントル数  Prt = nu_t / alpha_t  ->  alpha_t = nu_t / Prt", FS, BLACK)
ctext(d, 330, 340, "Prt は多くの流れで 0.9 前後のほぼ一定値", FT, GRAY)
note(d, "alpha_t は熱伝達係数ではなく熱の渦拡散係数 / Prt は乱流レイノルズ数ではない")
save(im, "t2f6TurbPrandtl")


# ============================================================ t2f6KEquation k方程式の収支
im, d = new()
title(d, "乱流エネルギー k の収支  Pk - eps + 拡散")
# 中央のkタンク
cx, cy, rr = 330, 210, 62
d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=BLACK, width=3, fill=FILL1)
ctext(d, cx, cy, "乱流エネルギー k", FS, BLACK)
# 生成 Pk (左から流入)
arrow(d, 120, 150, cx - rr - 4, cy - 24, BLUE, 4, 14)
ctext(d, 150, 120, "生成 Pk", FS, BLUE)
ctext(d, 150, 142, "平均流から供給", FT, GRAY)
ctext(d, 120, 96, "Pk = -u_i'u_j' dU_i/dx_j", FT, BLUE)
# 散逸 -eps (右下へ流出=熱)
arrow(d, cx + rr - 10, cy + rr - 20, 560, 320, RED, 4, 14)
ctext(d, 540, 300, "散逸 -eps", FS, RED)
ctext(d, 545, 322, "熱へ散る", FT, GRAY)
# 拡散(上下へ広がる=空間輸送)
arrow(d, cx, cy - rr - 2, cx, cy - rr - 46, GREEN, 3, 12)
arrow(d, cx, cy + rr + 2, cx, cy + rr + 46, GREEN, 3, 12)
ctext(d, cx + 150, cy - rr - 30, "拡散(空間へ運ぶ)", FS, GREEN)
ctext(d, cx + 150, cy - rr - 8, "分子ν + 乱流 nu_t/sigma_k", FT, GRAY)
note(d, "非定常+対流 = 生成Pk - 散逸eps + 拡散(分子粘性ν部分 と 乱流nu_t/sigma_k部分)")
save(im, "t2f6KEquation")


# ============================================================ t2f6ChannelAniso チャネル乱流の垂直応力
im, d = new()
title(d, "チャネル乱流の垂直応力  等方モデル vs 物理")
# 上: チャネル(平行平板)の設定
hwall(d, 90, 350, 80, side=1)
hwall(d, 90, 350, 150, side=-1)
ctext(d, 220, 66, "壁", FT, GRAY)
for k in range(3):
    yy = 100 + k * 16
    arrow(d, 110, yy, 200 + k * 30, yy, BLUE, 2, 8)
ctext(d, 300, 115, "完全発達 (dU/dx=0, V=W=0)", FT, BLUE)
# 左下: 等方モデル(3本同じ高さ)
bx = 90
ctext(d, bx + 90, 195, "等方モデルの結果", FS, RED)
labs = ["u'u'", "v'v'", "w'w'"]
for i, lab in enumerate(labs):
    x = bx + 20 + i * 60
    h = 70
    d.rectangle((x, 330 - h, x + 40, 330), outline=RED, width=3, fill=FILL2)
    ctext(d, x + 20, 348, lab, FT, BLACK)
d.line((bx + 10, 330 - 70, bx + 210, 330 - 70), fill=GRAY, width=1)
ctext(d, bx + 110, 230, "3成分とも 2k/3 で等値", FT, GRAY)
ctext(d, bx + 110, 372, "-> 非等方性を再現できない", FT, RED)
# 右下: 物理(u'u'>w'w'>v'v')
bx2 = 400
ctext(d, bx2 + 90, 195, "物理的に正しい分布", FS, BLUE)
hs = {"u'u'": 100, "w'w'": 66, "v'v'": 40}
order = ["u'u'", "w'w'", "v'v'"]
for i, lab in enumerate(order):
    x = bx2 + 20 + i * 60
    h = hs[lab]
    d.rectangle((x, 330 - h, x + 40, 330), outline=BLUE, width=3, fill=FILL1)
    ctext(d, x + 20, 348, lab, FT, BLACK)
ctext(d, bx2 + 110, 372, "u'u' > w'w' > v'v' (応力モデルが必要)", FT, BLUE)
note(d, "せん断応力 u'v' = -nu_t dU/dy は速度勾配があり非ゼロで正しく計算される")
save(im, "t2f6ChannelAniso")


# ============================================================ t2f6KeConstants モデル定数表
im, d = new()
title(d, "標準 k-eps モデルのモデル定数")
consts = [("Cmu", "0.09", "局所平衡から (0.9 ではない)"),
          ("sigma_k", "1.0", "k の拡散定数(実験的知見)"),
          ("sigma_eps", "1.3", "eps の拡散定数"),
          ("C_eps1", "1.44", "対数速度分布との整合"),
          ("C_eps2", "1.92", "一様減衰乱流から (2.92 ではない)")]
x0, y0 = 90, 100
w1, w2, w3, rh = 130, 100, 250, 48
d.rectangle((x0, y0, x0 + w1, y0 + 36), outline=BLUE, width=3)
ctext(d, x0 + w1 / 2, y0 + 18, "定数", FS, BLUE)
d.rectangle((x0 + w1, y0, x0 + w1 + w2, y0 + 36), outline=BLUE, width=3)
ctext(d, x0 + w1 + w2 / 2, y0 + 18, "標準値", FS, BLUE)
d.rectangle((x0 + w1 + w2, y0, x0 + w1 + w2 + w3, y0 + 36), outline=BLUE, width=3)
ctext(d, x0 + w1 + w2 + w3 / 2, y0 + 18, "決め方・注意", FS, BLUE)
for i, (a, b, c) in enumerate(consts):
    yy = y0 + 36 + i * rh
    d.rectangle((x0, yy, x0 + w1, yy + rh), outline=GRAY, width=2)
    ctext(d, x0 + w1 / 2, yy + rh / 2, a, FS, BLACK)
    d.rectangle((x0 + w1, yy, x0 + w1 + w2, yy + rh), outline=GRAY, width=2)
    ctext(d, x0 + w1 + w2 / 2, yy + rh / 2, b, FS, RED)
    d.rectangle((x0 + w1 + w2, yy, x0 + w1 + w2 + w3, yy + rh), outline=GRAY, width=2)
    ctext(d, x0 + w1 + w2 + 12, yy + rh / 2, c, FT, BLACK, "lm")
note(d, "Cmu=0.09, sigma_k=1.0, sigma_eps=1.3, C_eps1=1.44, C_eps2=1.92 (桁・取り違えに注意)")
save(im, "t2f6KeConstants")


# ============================================================ t2f6WallLaw 壁近傍構造(壁法則)
im, d = new()
title(d, "壁近傍の速度分布(壁法則)")
ctext(d, 330, 60, "標準 k-eps は粘性底層を苦手 -> 壁関数 か 低Re型で対処", FS, BLACK)
ox, oy = 110, 330
axes(d, ox, oy, 470, 190, "y+ (壁からの無次元距離)", "U+")
# 対数則風の速度分布曲線
pts = []
for k in range(1, 470, 3):
    up = 2.4 * math.log10(k + 1) * 40 / 3
    pts.append((ox + k, oy - min(up, 175)))
d.line(pts, fill=RED, width=3, joint="curve")
# 3領域の帯
b1 = ox + 90
b2 = ox + 210
d.line((b1, oy, b1, oy - 175), fill=LGRAY, width=1)
d.line((b2, oy, b2, oy - 175), fill=LGRAY, width=1)
ctext(d, (ox + b1) / 2, oy - 188, "粘性底層", FT, BLUE)
ctext(d, (b1 + b2) / 2, oy - 188, "バッファ層", FT, GREEN)
ctext(d, (b2 + ox + 470) / 2, oy - 188, "対数速度分布の領域", FT, RED)
note(d, "低Re型 k-eps: nu_t=Cmu f_mu k^2/eps の減衰関数 f_mu で壁近傍を改善(高Reにも使える)")
save(im, "t2f6WallLaw")


# ============================================================ t2f6RansModels RANSモデル分類(方程式数)
im, d = new()
title(d, "RANS渦粘性モデルの分類(解く方程式の数)")
rows = [("0 方程式", BLUE, "混合長 / Baldwin-Lomax", "代数式で渦粘性を与える\n(輸送方程式を解かない)"),
        ("1 方程式", GREEN, "Spalart-Allmaras", "渦粘性相当量の輸送方程式\nを1本解く(kではない)"),
        ("2 方程式", RED, "k-eps / k-omega / SST", "k と eps または omega=k/nu_t\nを解く(SST=逆圧力勾配に強い)")]
x0, y0 = 70, 90
w1, w2, w3, rh = 130, 230, 230, 90
for i, (a, col, b, c) in enumerate(rows):
    yy = y0 + i * rh
    d.rectangle((x0, yy, x0 + w1, yy + rh), outline=col, width=3)
    ctext(d, x0 + w1 / 2, yy + rh / 2, a, FS, col)
    d.rectangle((x0 + w1, yy, x0 + w1 + w2, yy + rh), outline=GRAY, width=2)
    ctext(d, x0 + w1 + w2 / 2, yy + rh / 2, b, FT, BLACK)
    d.rectangle((x0 + w1 + w2, yy, x0 + w1 + w2 + w3, yy + rh), outline=GRAY, width=2)
    for j, s in enumerate(c.split("\n")):
        ctext(d, x0 + w1 + w2 + w3 / 2, yy + rh / 2 - 10 + j * 20, s, FT, BLACK)
note(d, "0方程式=代数式 / 1方程式=渦粘性相当量 / 2方程式=k と eps(または omega)")
save(im, "t2f6RansModels")


# ============================================================ t2f6WallAsymptote 壁面漸近挙動と高Pr
im, d = new()
title(d, "壁面漸近挙動  nu_t ∝ y^3  と 高プラントル数流体")
# 左: nu_t ∝ y^3 のグラフ
ox, oy = 90, 300
axes(d, ox, oy, 220, 200, "nu_t", "y (壁距離)")
pts = []
for k in range(0, 200, 3):
    y = k  # y up
    nut = (k / 200) ** 3 * 200
    pts.append((ox + nut, oy - y))
d.line(pts, fill=RED, width=3, joint="curve")
ctext(d, ox + 120, oy - 150, "nu_t ∝ y^3", FS, RED)
ctext(d, ox + 110, 70, "壁のごく近くで急減衰", FT, GRAY)
# 右: 速度境界層 vs 温度境界層(高Pr=薄い)
wx0, wx1, wy = 380, 610, 300
hwall(d, wx0, wx1, wy, side=1)
ctext(d, (wx0 + wx1) / 2, wy + 26, "壁", FT, GRAY)
# 速度境界層(厚い)
cv = []
for k in range(0, wx1 - wx0 - 10, 3):
    x = wx0 + k
    dv = 90 * math.sqrt((k / (wx1 - wx0)) + 0.02)
    cv.append((x, wy - dv))
d.line(cv, fill=BLUE, width=3, joint="curve")
ctext(d, wx1 - 40, wy - 96, "速度境界層(厚)", FT, BLUE)
# 温度境界層(薄い, 高Pr)
ct = []
for k in range(0, wx1 - wx0 - 10, 3):
    x = wx0 + k
    dt = 42 * math.sqrt((k / (wx1 - wx0)) + 0.02)
    ct.append((x, wy - dt))
d.line(ct, fill=RED, width=3, joint="curve")
ctext(d, wx1 - 30, wy - 40, "温度境界層(薄)", FT, RED)
ctext(d, (wx0 + wx1) / 2, 78, "高Pr流体=薄い温度境界層", FS, BLACK)
note(d, "壁近傍が温度場に決定的 -> 漸近挙動を満たす低Re型 k-eps が望ましい")
save(im, "t2f6WallAsymptote")


# ============================================================ t2f6Smagorinsky LESフィルターとSGS
im, d = new()
title(d, "LES: 格子以上=直接計算 / 格子以下=SGSモデル")
# 格子(フィルター幅Delta)
gx0, gy0, cw, nx, ny = 70, 100, 46, 8, 5
for i in range(nx + 1):
    d.line((gx0 + i * cw, gy0, gx0 + i * cw, gy0 + ny * cw), fill=LGRAY, width=1)
for j in range(ny + 1):
    d.line((gx0, gy0 + j * cw, gx0 + nx * cw, gy0 + j * cw), fill=LGRAY, width=1)
dim(d, gx0, gy0 + ny * cw + 24, gx0 + cw, gy0 + ny * cw + 24, "Delta (フィルター幅)", col=GRAY)
# 大きな渦(格子以上=直接計算)
blob(d, gx0 + 3 * cw, gy0 + 2 * cw, 62, BLUE, 3, 0.4)
ctext(d, gx0 + 3 * cw, gy0 + 2 * cw, "大きな渦", FT, BLUE)
ctext(d, gx0 + 3 * cw, gy0 - 6, "格子以上=直接計算", FT, BLUE)
# 小さな渦(格子以下=モデル化)
random.seed(11)
for _ in range(10):
    px = gx0 + 5 * cw + random.random() * 2.4 * cw
    py = gy0 + 0.4 * cw + random.random() * 3.6 * cw
    blob(d, px, py, 6 + random.random() * 6, RED, 1, random.random() * 6, 0.3, 16)
ctext(d, gx0 + 6.2 * cw, gy0 + ny * cw + 24, "格子以下(SGS)", FT, RED, "mm")
# 式
ctext(d, 330, 340, "nu_SGS = (Cs fs Delta)^2 sqrt(2 S_ij S_ij)   (Cs≒0.1 は普遍でない)", FS, BLACK)
note(d, "fs=壁面減衰関数(壁で nu_SGS->0) / スマゴリンスキーは等方型でSGSの非等方性は再現不可")
save(im, "t2f6Smagorinsky")


# ============================================================ t2f6RansApplicability RANS適用範囲
im, d = new()
title(d, "RANSの適用範囲  平均場=可 / 非定常渦=不可")
# ア: 境界層(平均速度場) 可
ctext(d, 130, 78, "ア 乱流境界層", FS, BLUE)
hwall(d, 60, 200, 250, side=1)
for k in range(6):
    yy = 250 - 10 - k * 20
    dv = 20 + k * 14
    arrow(d, 60, yy, 60 + dv, yy, BLUE, 2, 7)
ctext(d, 130, 270, "平均速度場: RANS 可", FT, GREEN)
# イ: 平行平板(平均速度場) 可
ctext(d, 330, 78, "イ 発達した平行平板", FS, BLUE)
hwall(d, 260, 400, 120, side=-1)
hwall(d, 260, 400, 250, side=1)
for k in range(5):
    yy = 130 + k * 26
    dv = 40 - abs(k - 2) * 12
    arrow(d, 300, yy, 300 + 30 + dv, yy, BLUE, 2, 7)
ctext(d, 330, 270, "平均速度場: RANS 可", FT, GREEN)
# ウ: 円柱後流のカルマン渦(非定常) 不可
ctext(d, 540, 78, "ウ 円柱後流の渦", FS, RED)
node(d, 470, 185, r=16, fill=FILL2, col=BLACK)
blob(d, 520, 160, 16, RED, 2, 0.4)
blob(d, 560, 205, 16, RED, 2, 2.0)
blob(d, 600, 165, 15, RED, 2, 3.4)
ctext(d, 540, 270, "非定常渦: RANS 不可(LES)", FT, RED)
note(d, "平均量で足りる=RANS向き / 非定常な渦そのものが対象=RANS不向き(LES等が必要)")
save(im, "t2f6RansApplicability")


# ============================================================ t2f6CylinderRe 円柱まわりのRe依存
im, d = new()
title(d, "円柱まわり流れのレイノルズ数依存")
panels = [("Re <= 1", 130, "上下対称の定常層流", "(はく離なし)"),
          ("Re ~ 100", 330, "カルマン渦", "(非定常層流)"),
          ("Re ~ 10000", 540, "乱流の後流", "(乱れる)")]
for name, cx, l1, l2 in panels:
    ctext(d, cx, 74, name, FS, BLACK)
    node(d, cx - 70, 190, r=16, fill=FILL2, col=BLACK)
    # 上流矢印
    for k in range(3):
        yy = 175 + k * 15
        arrow(d, cx - 130, yy, cx - 92, yy, BLUE, 2, 7)
if True:
    # Re<=1: なめらかに閉じる流線
    cx = 130
    for dy in (-26, 0, 26):
        pts = [(cx - 92, 190 + dy)]
        for k in range(1, 40):
            x = cx - 54 + k * 3
            y = 190 + dy * (1 - 0.3 * math.exp(-((x - cx) / 40) ** 2)) if dy else 190
            pts.append((x, y))
        d.line(pts, fill=BLUE, width=2, joint="curve")
    ctext(d, cx, 250, "定常層流(計算可)", FT, GREEN)
    # Re~100: カルマン渦列
    cx = 330
    blob(d, cx + 0, 172, 15, RED, 2, 0.4)
    blob(d, cx + 40, 208, 15, RED, 2, 1.8)
    blob(d, cx + 80, 172, 14, RED, 2, 3.0)
    blob(d, cx + 120, 208, 14, RED, 2, 4.2)
    ctext(d, cx, 250, "非定常(定常計算不可)", FT, RED)
    # Re~10000: 乱れた後流
    cx = 540
    random.seed(5)
    for _ in range(9):
        blob(d, cx - 20 + random.random() * 130, 165 + random.random() * 55, 7 + random.random() * 10, RED, 1, random.random() * 6)
    ctext(d, cx, 250, "乱流(層流計算不可)", FT, RED)
ctext(d, 330, 300, "層流の定常計算が妥当なのは 低Re(Re<=1) のみ", FS, BLACK)
note(d, "Re~50-500 でカルマン渦(非定常層流) / Re>1000 で乱流化")
save(im, "t2f6CylinderRe")


# ============================================================ t2f6LesDiscretization LESの離散化
im, d = new()
title(d, "LESの離散化  数値粘性は小さく(保存性重視)")
# 左: 風上型(数値粘性大->渦がにじむ)
ctext(d, 175, 82, "風上型(数値粘性 大)", FS, RED)
d.rectangle((60, 108, 300, 300), outline=RED, width=2)
# ぼやけた渦(二重線で滲みを表現)
for r in (44, 52, 60):
    d.ellipse((180 - r, 204 - r * 0.85, 180 + r, 204 + r * 0.85), outline=LGRAY, width=2)
blob(d, 180, 204, 30, RED, 2, 0.5)
ctext(d, 175, 318, "渦がにじんで潰れる", FT, GRAY)
# 右: 保存性重視(数値粘性小->渦が保たれる)
ctext(d, 485, 82, "保存性重視(数値粘性 小)", FS, BLUE)
d.rectangle((360, 108, 600, 300), outline=BLUE, width=2)
blob(d, 480, 204, 46, BLUE, 3, 0.5)
blob(d, 480, 204, 22, BLUE, 2, 2.0)
ctext(d, 485, 318, "渦の形が保たれる", FT, GRAY)
arrow(d, 315, 204, 355, 204, BLACK, 3, 12)
ctext(d, 330, 344, "対流項=数値粘性小の保存性重視 / 時間方向も2次精度以上が望ましい", FS, BLACK)
note(d, "安定化目的の風上型・低次単純手法は捉えたい渦を潰すためLESには不向き")
save(im, "t2f6LesDiscretization")


# ============================================================ t2f6CriticalRe 臨界レイノルズ数
im, d = new()
title(d, "臨界レイノルズ数  Re = U d / nu ,  Re_c ≒ 2300 (管内流)")
# 数直線
ax0, ax1, ay = 80, 600, 210
arrow(d, ax0, ay, ax1, ay, BLACK, 3, 13)
ctext(d, ax1 + 4, ay + 16, "Re", FS, BLACK, "lm")
# 臨界位置
xc = 380
d.line((xc, ay - 12, xc, ay + 12), fill=RED, width=3)
ctext(d, xc, ay - 26, "Re_c ≒ 2300", FT, RED)
# 領域帯
d.line((ax0, ay - 40, xc, ay - 40), fill=BLUE, width=2)
ctext(d, (ax0 + xc) / 2, ay - 54, "層流", FS, BLUE)
d.line((xc, ay - 40, xc + 90, ay - 40), fill=ORANGE, width=2)
ctext(d, xc + 45, ay - 62, "遷移域", FT, ORANGE)
d.line((xc + 90, ay - 40, ax1 - 10, ay - 40), fill=RED, width=2)
ctext(d, (xc + 90 + ax1) / 2, ay - 54, "十分発達した乱流", FS, RED)
# Re=2400の位置(臨界すれすれ)
x24 = xc + 24
arrow(d, x24, ay + 60, x24, ay + 16, GREEN, 3, 12)
ctext(d, x24 + 30, ay + 74, "Re=2400 (臨界すれすれ=弱い乱れ)", FT, GREEN)
ctext(d, 330, 320, "発達乱流前提のモデル(高Re型・低Re型)は誤差大 -> 直接計算が妥当", FS, BLACK)
note(d, "低Re型 k-eps の『低Re』は壁近傍の低Re領域の意味で、場全体が臨界すれすれとは別物")
save(im, "t2f6CriticalRe")


print("ALL DONE")
