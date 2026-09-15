# -*- coding: utf-8 -*-
"""固体力学1級 第4章 境界非線形(接触) の問題図(s1e4*)・公式図(s1f4*)を描画。
白地660x420・黒線画・機構のみ・物理的に正確。ラベルはMeiryoで豆腐化しない通常表記(lambda/sigma/mu/tau_y/pi/^2 等)。"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def box(d, cx, cy, w, h, text, fnt=FS, fill="white"):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=fill)
    ctext(d, cx, cy, text, fnt)


def mesh(d, x0, y0, w, h, nx, ny, col=BLACK, wd=2):
    for i in range(nx + 1):
        x = x0 + w * i / nx
        d.line((x, y0, x, y0 + h), fill=col, width=wd)
    for j in range(ny + 1):
        y = y0 + h * j / ny
        d.line((x0, y, x0 + w, y), fill=col, width=wd)


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9):
    L = math.hypot(x2 - x1, y2 - y1)
    n = max(1, int(L / dash))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash
            b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


# ============================================================ s1e4 問題図(20)

# 4-1 接触の定義: 2物体が距離0で接し、圧縮のみ伝達・不可侵
im, d = new()
title(d, "接触の定義: 距離0・不可侵・圧縮のみ")
d.rectangle((110, 150, 320, 300), outline=BLACK, width=3, fill=FILL1)
d.rectangle((340, 150, 550, 300), outline=BLACK, width=3, fill=FILL2)
d.line((330, 140, 330, 310), fill=BLACK, width=4)
ctext(d, 330, 125, "接触面 g=0", FT)
force(d, 250, 225, 55, 0, "押す(圧縮)", RED)
force(d, 410, 225, -55, 0, "押す(圧縮)", RED)
ctext(d, 215, 330, "物体1", FS)
ctext(d, 445, 330, "物体2", FS)
ctext(d, 330, 360, "引張は伝わらない / めり込まない(不可侵)", FT, GRAY)
save(im, "s1e4ContactDefinition")

# 4-2 ギャップ関数 g=(x2-x1).n1 の3状態
im, d = new()
title(d, "ギャップ関数 g=(x2-x1)*n1  の3状態")
for cx, lab, gtext, dy in [(140, "g>0 離間", "すきま", -34), (330, "g=0 接触", "", 0), (520, "g<0 貫通", "めり込み", 20)]:
    y1 = 250
    hwall(d, cx - 70, cx + 70, y1, 1, 6)  # 面1(下)
    ctext(d, cx, y1 + 32, "n1", FT)
    arrow(d, cx, y1, cx, y1 - 40, BLUE, 2, 10)  # 法線n1(上向き)
    top = y1 - 40 + dy  # 物体2の下面
    d.rectangle((cx - 55, top - 55, cx + 55, top), outline=BLACK, width=3, fill=FILL1)
    ctext(d, cx, top - 28, "物体2", FT)
    if dy < 0:
        dim(d, cx + 68, top, cx + 68, y1, "g", 0)
    elif dy > 0:
        dashed(d, cx - 55, y1, cx + 55, y1)
    ctext(d, cx, 300, lab, FS, BLACK if dy != 0 else RED)
save(im, "s1e4GapFunction")

# 4-3 KKT 相補性: g軸-sigma軸のL字領域
im, d = new()
title(d, "相補性条件(KKT): g>=0, sigma<=0, sigma*g=0")
ox, oy = 330, 210
d.line((ox - 200, oy, ox + 220, oy), fill=LGRAY, width=1)
d.line((ox, oy - 150, ox, oy + 160), fill=LGRAY, width=1)
ctext(d, ox + 232, oy, "g", FS)
ctext(d, ox, oy - 165, "sigma", FS)
# 有効な相補領域(L字): 正のg軸(sigma=0) と 負のsigma軸(g=0)
d.line((ox, oy, ox + 210, oy), fill=RED, width=6)
d.line((ox, oy, ox, oy + 150), fill=RED, width=6)
ctext(d, ox + 120, oy - 16, "g>0 なら sigma=0 (離間)", FT, RED)
ctext(d, ox + 118, oy + 150, "g=0 なら sigma<0 (接触)", FT, RED, "lm")
ctext(d, ox, oy + 150, "", FT)
d.text((ox + 8, oy + 138), "g=0 のとき圧縮 sigma<0", font=FT, fill=RED)
ctext(d, ox - 100, oy - 70, "積 sigma*g=0\n(片方は必ず0)", FT, GRAY)
save(im, "s1e4KKT")

# 4-4 マスター/スレーブ面
def draw_master_slave(fname):
    im, d = new()
    title(d, "マスター面(固い・粗い) / スレーブ面(軟らかい・細かい)")
    # スレーブ(上・細かい)
    mesh(d, 100, 130, 460, 70, 20, 2)
    ctext(d, 300, 118, "スレーブ面: 軟らかい・細メッシュ", FT)
    # 接触界面 + スレーブ節点
    yif = 210
    for k in range(21):
        x = 100 + 460 * k / 20
        node(d, x, yif, 4)
    # マスター(下・粗い)
    mesh(d, 100, 220, 460, 80, 4, 2, wd=3)
    ctext(d, 300, 315, "マスター面: 固い・粗メッシュ (接触方向を支配)", FT)
    arrow(d, 150, yif - 22, 260, yif - 22, GREEN, 3, 12)
    ctext(d, 305, yif - 22, "スレーブ節点はマスター面に沿って滑る", FT, GREEN, "lm")
    save(im, fname)
draw_master_slave("s1e4MasterSlave")

# 4-5 リジッドサーフェス(剛体面=マスター)と接触要素は方向固定
im, d = new()
title(d, "リジッドサーフェス(剛体面=マスター) と接触要素")
# 剛体面(曲面, メッシュなし)
pts = [(120 + i, 250 - 40 * math.sin(math.pi * i / 420)) for i in range(0, 421, 6)]
d.line(pts, fill=BLACK, width=4)
for i in range(0, 421, 30):
    x = 120 + i
    y = 250 - 40 * math.sin(math.pi * i / 420)
    d.line((x, y, x - 8, y + 14), fill=BLACK, width=2)
ctext(d, 300, 288, "剛体面(変形しない)=マスター面", FT)
# 変形するスレーブ体(メッシュ)
mesh(d, 190, 120, 280, 70, 12, 2)
ctext(d, 330, 108, "変形するスレーブ体", FT)
ctext(d, 330, 335, "接触要素は接触方向が固定 -> 大きな滑りは不可", FT, GRAY)
save(im, "s1e4RigidSurface")

# 4-6 点接触(整合メッシュ) vs 面接触(不整合メッシュ)
im, d = new()
title(d, "点接触(節点整合) と 面接触(節点-セグメント)")
# 左: 点接触・整合
ctext(d, 165, 70, "点接触: 節点を一致", FS)
for k in range(6):
    x = 70 + k * 40
    node(d, x, 200, 5)
    node(d, x, 235, 5)
    dashed(d, x, 205, x, 230, RED, 2, 6)
mesh(d, 70, 130, 200, 70, 5, 2)
mesh(d, 70, 235, 200, 70, 5, 2)
ctext(d, 165, 320, "整合 -> 高精度だが作業膨大", FT, GRAY)
# 右: 面接触・不整合
ctext(d, 500, 70, "面接触: 節点位置は不揃い", FS)
for k in range(4):
    x = 400 + k * 50
    node(d, x, 200, 5)
mesh(d, 400, 130, 190, 70, 4, 2)
d.line((400, 235, 590, 235), fill=BLACK, width=3)
for k in range(7):
    x = 400 + k * 31
    node(d, x, 235, 5)
for k in range(4):
    x = 400 + k * 50
    dashed(d, x, 205, x, 232, RED, 2, 6)
mesh(d, 400, 235, 190, 70, 7, 2)
ctext(d, 495, 320, "整合不要・容易だが離散化誤差", FT, GRAY)
save(im, "s1e4PointVsSurface")

# 4-7 ラグランジュ未定乗数法: 直列ばね K1-K2 接触モデル
def spring_contact_model(fname, title_s, penalty=False):
    im, d = new()
    title(d, title_s)
    yb = 220
    wall(d, 60, yb - 45, yb + 45, 1, 6)
    n2 = 250 if not penalty else 250
    n3 = 300
    spring(d, 75, yb, n2 - 12, coils=6, amp=14)
    node(d, n2, yb, 8)
    node(d, n3, yb, 8)
    ctext(d, 165, yb - 40, "K1", FS)
    if penalty:
        spring(d, n2 + 8, yb, n3 - 8, coils=4, amp=10)
        ctext(d, (n2 + n3) / 2, yb - 34, "alpha", FT, RED)
        dashed(d, n2, yb + 22, n2, yb + 60, GRAY)
        dashed(d, n3, yb + 22, n3, yb + 60, GRAY)
        dim(d, n2, yb + 52, n3, yb + 52, "g=-F/alpha (微小貫入)", 0, RED)
    else:
        d.line((n2, yb - 18, n2, yb + 18), fill=RED, width=2)
        d.line((n3, yb - 18, n3, yb + 18), fill=RED, width=2)
        force(d, n2 - 4, yb + 40, 20, 0, "", RED)
        force(d, n3 + 4, yb + 40, -20, 0, "", RED)
        ctext(d, (n2 + n3) / 2, yb + 75, "接触: lambda(=接触力)", FT, RED)
    spring(d, n3 + 8, yb, 470 - 8, coils=6, amp=14)
    node(d, 470, yb, 8)
    ctext(d, 385, yb - 40, "K2", FS)
    force(d, 470, yb, 70, 0, "F", RED)
    ctext(d, n2, yb - 22, "u2", FT)
    ctext(d, n3, yb - 22, "u3", FT)
    ctext(d, 63, yb - 62, "節点1 固定", FT)
    if penalty:
        ctext(d, 330, 340, "u3 = u2 + F/alpha (alpha大で貫入->0)", FT, GRAY)
    else:
        ctext(d, 330, 340, "g=u2-u3 を厳密に0に拘束 (lambda追加=正定値性喪失)", FT, GRAY)
    save(im, fname)
spring_contact_model("s1e4Lagrange", "ラグランジュ未定乗数法: g=u2-u3, lambda=接触力", penalty=False)

# 4-8 ペナルティ法
spring_contact_model("s1e4Penalty", "ペナルティ法: 接触ばね alpha と微小貫入", penalty=True)

# 4-9 拡張ラグランジュ(Uzawa): 反復で g->0, lambda->-F
im, d = new()
title(d, "拡張ラグランジュ(Uzawa更新): g->0, lambda->-F")
ox, oy = 110, 330
axes(d, ox, oy, 470, 250, "反復 k", "")
gk = [0.20, 0.09, 0.04, 0.016, 0.006]
lk = [0.0, 0.55, 0.80, 0.92, 0.98]  # |lambda|/F
gp = [(ox + 40 + i * 100, oy - gk[i] / 0.20 * 210) for i in range(5)]
lp = [(ox + 40 + i * 100, oy - lk[i] * 210) for i in range(5)]
plot(d, ox, oy, gp, BLUE, 3)
plot(d, ox, oy, lp, RED, 3)
for p in gp:
    node(d, p[0], p[1], 5, fill="white", col=BLUE)
for p in lp:
    node(d, p[0], p[1], 5, fill="white", col=RED)
for i in range(5):
    ctext(d, ox + 40 + i * 100, oy + 16, str(i + 1), FT)
ctext(d, 470, oy - 40, "残留貫入 g -> 0", FT, BLUE, "rm")
ctext(d, 470, oy - 215, "乗数 |lambda| -> F", FT, RED, "rm")
save(im, "s1e4AugmentedLagrange")

# 4-10 擬似荷重 f=K A^2 L /V の組み立て
im, d = new()
title(d, "擬似荷重 f = K * A^2 * L / V")
# マスターセグメント(面)
d.line((150, 220, 470, 220), fill=BLACK, width=4)
ctext(d, 310, 205, "マスターセグメント 面積 A", FT)
# 要素体積V
d.polygon([(150, 220), (470, 220), (500, 300), (180, 300)], outline=BLACK, width=2, fill=FILL1)
ctext(d, 325, 265, "要素体積 V", FS)
# 貫入したスレーブ節点
node(d, 310, 265, 8, fill=FILL2)
dashed(d, 310, 220, 310, 265, GRAY)
dim(d, 340, 220, 340, 265, "貫入深さ L", 0, RED)
# 反発力
force(d, 310, 265, 0, -70, "f (反発力)", RED)
ctext(d, 330, 340, "AL減少->体積ひずみ AL/V->応力 KAL/V->x面積A-> f=KA^2L/V", FT, GRAY)
save(im, "s1e4PseudoLoad")

# 4-11 クーロン摩擦: ステップ関数 と tanh平滑化
def coulomb_fig(fname):
    im, d = new()
    title(d, "クーロン摩擦: ステップ関数 と tanh 平滑化")
    ox, oy = 330, 220
    axes(d, ox, oy, 0, 0)
    d.line((ox - 210, oy, ox + 210, oy), fill=BLACK, width=2)
    d.line((ox, oy - 130, ox, oy + 130), fill=BLACK, width=2)
    ctext(d, ox + 222, oy, "v", FS)
    ctext(d, ox - 14, oy - 145, "摩擦力", FT, BLACK, "rm")
    F0 = 90
    # ステップ関数(不連続): v<0 -> +F0, v>0 -> -F0
    d.line((ox - 200, oy - F0, ox, oy - F0), fill=RED, width=3)
    d.line((ox, oy - F0, ox, oy + F0), fill=RED, width=3)
    d.line((ox, oy + F0, ox + 200, oy + F0), fill=RED, width=3)
    ctext(d, ox - 120, oy - F0 - 14, "ステップ(不連続)", FT, RED)
    dashed(d, ox - 200, oy - F0, ox + 200, oy - F0, LGRAY)
    dashed(d, ox - 200, oy + F0, ox + 200, oy + F0, LGRAY)
    ctext(d, ox + 205, oy - F0, "+mu|N|", FT, GRAY, "lm")
    ctext(d, ox + 205, oy + F0, "-mu|N|", FT, GRAY, "lm")
    # tanh 平滑化
    tp = [(ox + x, oy + F0 * math.tanh(x / 40.0)) for x in range(-200, 201, 4)]
    plot(d, ox, oy, tp, BLUE, 3)
    ctext(d, ox + 120, oy + F0 + 16, "tanh(|v|/alpha) 平滑化", FT, BLUE)
    save(im, fname)
coulomb_fig("s1e4CoulombSmooth")

# 4-12 せん断降伏応力 tau_y = sigma_y/sqrt(3)
im, d = new()
title(d, "ミーゼス: せん断降伏応力 tau_y = sigma_y / sqrt(3)")
# 引張要素
d.rectangle((110, 170, 210, 270), outline=BLACK, width=3, fill=FILL1)
force(d, 160, 170, 0, -55, "sigma_y", RED)
force(d, 160, 270, 0, 55, "", RED)
ctext(d, 160, 300, "単軸引張 sigma_y", FT)
# せん断要素
d.rectangle((330, 170, 430, 270), outline=BLACK, width=3, fill=FILL1)
force(d, 330, 165, 90, 0, "tau_y", GREEN)
force(d, 430, 275, -90, 0, "", GREEN)
force(d, 435, 170, 0, 90, "", GREEN)
force(d, 325, 270, 0, -90, "", GREEN)
ctext(d, 380, 300, "純せん断 tau_y", FT)
ctext(d, 540, 220, "tau_y\n= sigma_y/sqrt3\n≒ 0.577 sigma_y", FS, BLUE)
save(im, "s1e4ShearYield")

# 4-13 クーロン(増加) vs せん断摩擦(一定)
im, d = new()
title(d, "摩擦力: クーロン(増加) と せん断摩擦(一定)")
ox, oy = 110, 340
axes(d, ox, oy, 470, 250, "加工の進展(接触圧の増加)", "摩擦力")
coul = [(ox, oy - 20), (ox + 440, oy - 225)]
plot(d, ox, oy, coul, RED, 3)
ctext(d, ox + 445, oy - 225, "クーロン mu*圧力", FT, RED, "rm")
shear = [(ox, oy - 120), (ox + 440, oy - 120)]
plot(d, ox, oy, shear, GREEN, 3)
ctext(d, ox + 300, oy - 108, "せん断摩擦 mu*tau_y (一定)", FT, GREEN)
save(im, "s1e4FrictionCompare")

# 4-14 固着/滑り: ステップ関数と有限(人工)剛性で平滑遷移
im, d = new()
title(d, "固着/滑り: ステップ関数 と 有限(人工)剛性")
ox, oy = 330, 225
d.line((ox - 210, oy, ox + 210, oy), fill=BLACK, width=2)
d.line((ox, oy - 130, ox, oy + 130), fill=BLACK, width=2)
ctext(d, ox + 224, oy, "相対滑り", FT, BLACK, "lm")
ctext(d, ox - 14, oy - 145, "摩擦力", FT, BLACK, "rm")
F0 = 90
# ステップ: 固着=剛性無限大(垂直), 滑り=一定
d.line((ox, oy - F0, ox, oy + F0), fill=RED, width=3)
d.line((ox, oy - F0, ox + 200, oy - F0), fill=RED, width=3)
d.line((ox, oy + F0, ox - 200, oy + F0), fill=RED, width=3)
ctext(d, ox - 120, oy - F0 - 14, "ステップ(剛性が無限大->0)", FT, RED)
# 平滑: 有限剛性で立ち上がり、プラトーへ
sp = [(ox + x, oy - F0 * math.tanh(x / 55.0)) for x in range(-200, 201, 4)]
plot(d, ox, oy, sp, BLUE, 3)
ctext(d, ox + 120, oy + F0 + 16, "有限剛性で平滑遷移", FT, BLUE)
save(im, "s1e4StickSlip")

# 4-15 チャタリング: 振動継続 と 構造減衰で収束
im, d = new()
title(d, "チャタリング: 接触/解離の振動 と 構造減衰で収束")
# 上: 減衰なし(振動継続)
ox, oy = 90, 160
d.line((ox, oy, ox + 490, oy), fill=LGRAY, width=1)
wp = [(ox + x, oy - 45 * math.sin(x / 14.0)) for x in range(0, 491, 4)]
plot(d, ox, oy, wp, RED, 2)
ctext(d, ox + 250, oy - 62, "減衰なし: 接触/解離を繰り返す", FT, RED)
# 下: 構造減衰で収束
oy2 = 320
d.line((ox, oy2, ox + 490, oy2), fill=LGRAY, width=1)
wp2 = [(ox + x, oy2 - 55 * math.exp(-x / 160.0) * math.sin(x / 14.0)) for x in range(0, 491, 4)]
plot(d, ox, oy2, wp2, BLUE, 2)
ctext(d, ox + 250, oy2 - 70, "構造減衰: 高周波をダンプアウトし収束", FT, BLUE)
save(im, "s1e4Chattering")

# 4-16 荷重経路依存性: 摩擦あり(依存) vs 摩擦なし(非依存)
im, d = new()
title(d, "荷重経路依存性: 摩擦あり=依存 / 摩擦なし=非依存")
ox, oy = 110, 340
axes(d, ox, oy, 470, 250, "変位", "荷重")
# 摩擦なし(一意): 滑らかな曲線
fn = [(ox + x, oy - (x * 0.42)) for x in range(0, 441, 8)]
plot(d, ox, oy, fn, GREEN, 3)
ctext(d, ox + 445, oy - 185, "摩擦なし: 経路非依存(一意)", FT, GREEN, "rm")
# 摩擦あり(増分で異なる): 粗い階段 と 細かい階段
coarse = []
x = 0
y = 0
while x <= 440:
    coarse.append((ox + x, oy - y))
    coarse.append((ox + x, oy - (y + 45)))
    y += 45
    x += 80
plot(d, ox, oy, coarse, RED, 2)
fine = [(ox + x, oy - x * 0.55) for x in range(0, 441, 8)]
plot(d, ox, oy, fine, ORANGE, 2)
ctext(d, ox + 250, oy - 235, "摩擦あり: 増分で解が変わる(経路依存)", FT, RED)
save(im, "s1e4LoadPath")

# 4-17 摩擦発熱 熱-応力連成 の流れ図
im, d = new()
title(d, "摩擦発熱: 熱-応力連成の流れ")
box(d, 330, 90, 360, 44, "摩擦力 x 相対滑り量")
arrow(d, 330, 112, 330, 148, BLACK, 3, 12)
box(d, 330, 172, 300, 44, "摩擦仕事増分")
arrow(d, 330, 194, 330, 230, BLACK, 3, 12)
ctext(d, 345, 212, "x 変換係数", FT, GRAY, "lm")
box(d, 330, 254, 340, 44, "熱量(熱流束)")
arrow(d, 330, 276, 330, 312, BLACK, 3, 12)
box(d, 330, 336, 420, 44, "熱伝導解析の発熱項(外部熱流束)")
save(im, "s1e4FrictionHeat")

# 4-18 接触探索: 総当り O(n^2) vs 木 O(n log n)
im, d = new()
title(d, "接触探索: 総当り O(n^2)  と  木 O(n log n)")
# 左: 総当り(全ペア)
lx = [90, 90, 90, 90]
ly = [140, 190, 240, 290]
rx = [230, 230, 230, 230]
for i in range(4):
    node(d, 90, ly[i], 7)
    node(d, 230, ly[i], 7)
for a in range(4):
    for b in range(4):
        d.line((97, ly[a], 223, ly[b]), fill=LGRAY, width=1)
ctext(d, 160, 110, "総当り: 全ペア照合", FT)
ctext(d, 160, 325, "O(n^2)", FS, RED)
# 右: 2分木
def tnode(x, y):
    node(d, x, y, 7, fill=FILL2)
root = (470, 130)
l1 = [(410, 200), (530, 200)]
l2 = [(380, 270), (440, 270), (500, 270), (560, 270)]
for c in l1:
    d.line((root[0], root[1], c[0], c[1]), fill=BLACK, width=2)
d.line((l1[0][0], l1[0][1], l2[0][0], l2[0][1]), fill=BLACK, width=2)
d.line((l1[0][0], l1[0][1], l2[1][0], l2[1][1]), fill=BLACK, width=2)
d.line((l1[1][0], l1[1][1], l2[2][0], l2[2][1]), fill=BLACK, width=2)
d.line((l1[1][0], l1[1][1], l2[3][0], l2[3][1]), fill=BLACK, width=2)
tnode(*root)
for c in l1 + l2:
    tnode(*c)
ctext(d, 470, 110, "座標ソート+2分木", FT)
ctext(d, 470, 325, "O(n log n)", FS, BLUE)
save(im, "s1e4ContactSearch")

# 4-19 ヘルツ圧力分布: 円形接触面 と 半楕円分布 pmax=3P/(2 pi a^2)
def hertz_pressure(fname, with_topview=True):
    im, d = new()
    title(d, "ヘルツ接触: 円形接触面 と 半楕円圧力 pmax=3P/(2 pi a^2)")
    # 断面: 半楕円圧力分布
    ox = 330
    base = 320
    a = 150
    pmax = 150
    d.line((ox - a - 30, base, ox + a + 30, base), fill=BLACK, width=3)
    pts = []
    for r in range(-a, a + 1, 3):
        p = pmax * math.sqrt(max(0.0, 1 - (r / a) ** 2))
        pts.append((ox + r, base - p))
    plot(d, ox, base, pts, BLUE, 3)
    # 圧力矢印(中央最大)
    for r in range(-a + 20, a, 30):
        p = pmax * math.sqrt(max(0.0, 1 - (r / a) ** 2))
        arrow(d, ox + r, base - p, ox + r, base - 4, RED, 2, 7)
    arrow(d, ox, base + 4, ox, base - pmax, GRAY, 2, 9)
    ctext(d, ox + 16, base - pmax + 6, "pmax", FT, BLUE, "lm")
    dim(d, ox, base + 26, ox + a, base + 26, "a", 0)
    ctext(d, ox, base + 44, "中央最大・縁ゼロ  p=pmax*sqrt(1-(r/a)^2)", FT, GRAY)
    if with_topview:
        cx, cy, rr = 150, 110, 45
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=BLACK, width=3, fill=FILL1)
        node(d, cx, cy, 3, fill=BLACK)
        dim(d, cx, cy, cx + rr, cy, "a", 0)
        ctext(d, cx, cy + rr + 16, "接触面(円形)", FT)
    save(im, fname)
hertz_pressure("s1e4HertzPressure", with_topview=True)

# 4-20 ヘルツ 荷重依存: 両対数で傾き1/3
im, d = new()
title(d, "ヘルツ接触の荷重依存: 両対数で傾き 1/3")
ox, oy = 120, 340
axes(d, ox, oy, 460, 250, "log P", "")
ctext(d, ox - 16, oy - 250, "log", FT, BLACK, "rm")
# a ~ P^(1/3): 傾き1/3
la = [(ox, oy - 30), (ox + 430, oy - 30 - 430 / 3.0)]
plot(d, ox, oy, la, BLUE, 3)
ctext(d, ox + 435, oy - 30 - 430 / 3.0, "a: 傾き 1/3", FT, BLUE, "rm")
# pmax ~ P^(1/3): 別切片で同傾き
lp = [(ox, oy - 150), (ox + 430, oy - 150 - 430 / 3.0)]
plot(d, ox, oy, lp, RED, 3)
ctext(d, ox + 435, oy - 150 - 430 / 3.0, "pmax: 傾き 1/3", FT, RED, "rm")
# 傾き三角
d.line((ox + 90, oy - 60, ox + 210, oy - 60), fill=GRAY, width=2)
d.line((ox + 210, oy - 60, ox + 210, oy - 100), fill=GRAY, width=2)
ctext(d, ox + 150, oy - 48, "3", FT, GRAY)
ctext(d, ox + 224, oy - 80, "1", FT, GRAY)
ctext(d, 330, 388, "P を8倍にしても a, pmax は 8^(1/3)=2 倍のみ", FT, GRAY)
save(im, "s1e4HertzExponent")


# ============================================================ s1f4 公式図(7)

# ギャップ関数: 2面と法線n・距離g
im, d = new()
title(d, "ギャップ関数 g = (x2 - x1) * n1")
hwall(d, 130, 530, 270, 1, 10)
ctext(d, 330, 300, "面1", FT)
node(d, 330, 270, 5, fill=BLACK)
ctext(d, 315, 258, "x1", FT, BLACK, "rm")
arrow(d, 330, 270, 330, 210, BLUE, 3, 11)
ctext(d, 348, 220, "n1(外向き法線)", FT, BLUE, "lm")
d.rectangle((250, 120, 470, 190), outline=BLACK, width=3, fill=FILL1)
ctext(d, 360, 155, "面2", FT)
node(d, 330, 190, 5, fill=BLACK)
ctext(d, 315, 180, "x2", FT, BLACK, "rm")
dim(d, 300, 190, 300, 270, "g (すきま)", 0, RED)
ctext(d, 330, 355, "g>0 離間 / g=0 接触 / g<0 貫通", FT, GRAY)
save(im, "s1f4Gap")

# KKT 相補領域
im, d = new()
title(d, "相補性条件: g>=0, sigma<=0, sigma*g=0")
ox, oy = 330, 210
d.line((ox - 200, oy, ox + 220, oy), fill=LGRAY, width=1)
d.line((ox, oy - 150, ox, oy + 160), fill=LGRAY, width=1)
ctext(d, ox + 232, oy, "g", FS)
ctext(d, ox, oy - 165, "sigma", FS)
d.line((ox, oy, ox + 210, oy), fill=RED, width=6)
d.line((ox, oy, ox, oy + 150), fill=RED, width=6)
ctext(d, ox + 118, oy - 16, "g>0 -> sigma=0", FT, RED)
d.text((ox + 8, oy + 138), "g=0 -> sigma<0", font=FT, fill=RED)
ctext(d, ox - 100, oy - 70, "積 sigma*g=0\n片方は必ず0", FT, GRAY)
save(im, "s1f4KKT")

# マスター/スレーブ面
draw_master_slave("s1f4MasterSlave")

# ラグランジュ&ペナルティ(LagPen): 厳密 vs 微小貫入
im, d = new()
title(d, "ラグランジュ(厳密) と ペナルティ(微小貫入)")
# 左: ラグランジュ 貫入なし
lx = 175
yb = 210
wall(d, 80, yb - 30, yb + 30, 1, 5)
spring(d, 92, yb, lx - 12, coils=5, amp=11)
node(d, lx, yb, 7)
node(d, lx + 45, yb, 7)
d.line((lx, yb - 15, lx, yb + 15), fill=RED, width=2)
d.line((lx + 45, yb - 15, lx + 45, yb + 15), fill=RED, width=2)
ctext(d, lx + 22, yb - 28, "g=0", FT, RED)
ctext(d, 175, 290, "ラグランジュ: lambda追加\n貫入なし・厳密", FT)
# 右: ペナルティ ばねalpha・微小貫入
rx = 430
wall(d, 340, yb - 30, yb + 30, 1, 5)
spring(d, 352, yb, rx - 30, coils=5, amp=11)
node(d, rx - 18, yb, 7)
node(d, rx + 6, yb, 7)
spring(d, rx - 12, yb, rx, coils=3, amp=7)
ctext(d, rx - 6, yb - 28, "alpha", FT, RED)
dim(d, rx - 18, yb + 24, rx + 6, yb + 24, "g=-F/alpha", 0, RED)
ctext(d, 445, 290, "ペナルティ: 接触ばね alpha\n微小貫入が残る", FT)
save(im, "s1f4LagPen")

# クーロン摩擦 平滑化
coulomb_fig("s1f4Coulomb")

# ヘルツ: 2円(2球)押付けと接触半径a
im, d = new()
title(d, "ヘルツ接触: 2球の押付けと接触半径 a")
cx = 330
r = 120
top_c = (cx, 180)
bot_c = (cx, 300)
d.ellipse((cx - r, top_c[1] - r, cx + r, top_c[1] + r), outline=BLACK, width=3)
d.ellipse((cx - r, bot_c[1] - r, cx + r, bot_c[1] + r), outline=BLACK, width=3)
ctext(d, cx, top_c[1], "R1", FS)
ctext(d, cx, bot_c[1], "R2", FS)
# 接触半径
a = 46
d.line((cx - a, 240, cx + a, 240), fill=RED, width=3)
dim(d, cx, 240, cx + a, 240, "a", 0, RED)
force(d, cx, 40, 0, 60, "P", RED)
force(d, cx, 400, 0, -60, "P", RED)
ctext(d, 330, 388, "接触面は円形・接触半径 a ∝ P^(1/3)", FT, GRAY)
save(im, "s1f4Hertz")

# 圧力分布 半楕円
im, d = new()
title(d, "ヘルツ圧力分布: p = pmax * sqrt(1-(r/a)^2)")
ox = 330
base = 300
a = 170
pmax = 150
d.line((ox - a - 30, base, ox + a + 30, base), fill=BLACK, width=3)
pts = [(ox + rr, base - pmax * math.sqrt(max(0.0, 1 - (rr / a) ** 2))) for rr in range(-a, a + 1, 3)]
plot(d, ox, base, pts, BLUE, 3)
for rr in range(-a + 24, a, 34):
    p = pmax * math.sqrt(max(0.0, 1 - (rr / a) ** 2))
    arrow(d, ox + rr, base - p, ox + rr, base - 4, RED, 2, 7)
arrow(d, ox, base + 4, ox, base - pmax, GRAY, 2, 9)
ctext(d, ox + 16, base - pmax + 8, "pmax", FT, BLUE, "lm")
dim(d, ox, base + 26, ox + a, base + 26, "a", 0)
dim(d, ox, base + 50, ox - a, base + 50, "a", 0)
ctext(d, ox, base + 76, "中央最大・縁ゼロ (ドーム状)", FT, GRAY)
save(im, "s1f4Pressure")


# ============================================================ 検証
KEYS = [
    "s1e4ContactDefinition", "s1e4GapFunction", "s1e4KKT", "s1e4MasterSlave",
    "s1e4RigidSurface", "s1e4PointVsSurface", "s1e4Lagrange", "s1e4Penalty",
    "s1e4AugmentedLagrange", "s1e4PseudoLoad", "s1e4CoulombSmooth", "s1e4ShearYield",
    "s1e4FrictionCompare", "s1e4StickSlip", "s1e4Chattering", "s1e4LoadPath",
    "s1e4FrictionHeat", "s1e4ContactSearch", "s1e4HertzPressure", "s1e4HertzExponent",
    "s1f4Gap", "s1f4KKT", "s1f4MasterSlave", "s1f4LagPen", "s1f4Coulomb",
    "s1f4Hertz", "s1f4Pressure",
]
missing = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
print("=" * 40)
print("keys expected:", len(KEYS))
print("missing:", missing if missing else "none")
