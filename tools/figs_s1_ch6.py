# -*- coding: utf-8 -*-
"""固体力学1級 第6章「動的解析」の問題図(s1e6*)を描画。
白地660x420・線画・機構のみ・物理的に正確・装飾禁止。ラベルは通常表記(豆腐回避)。"""
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


def dashpot(d, cx, cy, w=44, h=36):
    """ダッシュポット(粘性減衰)。シリンダ+ピストン。"""
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    # シリンダ(上・左・右の3辺、右開放)
    d.line((x1, y0, x0, y0), fill=BLACK, width=3)
    d.line((x0, y0, x0, y1), fill=BLACK, width=3)
    d.line((x0, y1, x1, y1), fill=BLACK, width=3)
    # ピストン板
    px = cx + 3
    d.line((px, y0 + 4, px, y1 - 4), fill=BLACK, width=4)
    # ピストンロッド
    d.line((px, cy, x1 + 16, cy), fill=BLACK, width=3)


def massblock(d, cx, cy, w, h, label="", fnt=F):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=FILL1)
    if label:
        ctext(d, cx, cy, label, fnt)


def small_grid(d, x0, y0, x1, y1, nx, ny):
    for i in range(nx + 1):
        xx = x0 + (x1 - x0) * i / nx
        d.line((xx, y0, xx, y1), fill=BLACK, width=2)
    for j in range(ny + 1):
        yy = y0 + (y1 - y0) * j / ny
        d.line((x0, yy, x1, yy), fill=BLACK, width=2)


# ============================================================
# 6-1 s1e6EqMotion : 運動方程式の各項と物理量の対応
# ============================================================
def eq_motion():
    im, d = new(); title(d, "運動方程式 [M]a+[C]v+[K]u=f の各項")
    ctext(d, W / 2, 78, "[M] a   +   [C] v   +   [K] u   =   f", F)
    ctext(d, W / 2, 104, "a:加速度   v:速度   u:変位   f:外力", FT, GRAY)
    cols = [(130, "[M]", "×加速度 a", "慣性項"),
            (330, "[C]", "×速度 v", "減衰項"),
            (530, "[K]", "×変位 u", "弾性項")]
    for cx, mat, mul, name in cols:
        ctext(d, cx, 150, mat, FL)
        ctext(d, cx, 182, mul, FS)
        ctext(d, cx, 320, name, F, BLUE)
    # + 記号
    ctext(d, 230, 150, "+", F); ctext(d, 430, 150, "+", F)
    # アイコン: 質量ブロック / ダッシュポット / ばね
    massblock(d, 130, 250, 66, 52, "m")
    dashpot(d, 330, 250)
    spring(d, 480, 250, 580, 250, coils=5, amp=12)
    note(d, "加速度→質量[M]、速度→減衰[C]、変位→剛性[K] が対応する")
    save(im, "s1e6EqMotion")


# ============================================================
# 6-2 s1e6WaveSpeed : 縦弾性波が棒を右へ進む
# ============================================================
def wave_speed():
    im, d = new(); title(d, "縦弾性波が棒を伝わる  v=√(E/ρ)")
    x0, x1, yc, hh = 60, 600, 220, 34
    d.rectangle((x0, yc - hh, x1, yc + hh), outline=BLACK, width=3, fill=FILL1)
    xf = 360  # 波面位置
    # 波面(疎密): 波面直前の圧縮域に密な縦線
    for i in range(8):
        xx = xf - 8 - i * 14
        d.line((xx, yc - hh + 3, xx, yc + hh - 3), fill=GRAY, width=2)
    d.line((xf, yc - hh, xf, yc + hh), fill=RED, width=3)
    ctext(d, xf, yc + hh + 18, "波面", FT, RED)
    # 進行方向の矢印
    arrow(d, xf - 30, yc - hh - 34, xf + 90, yc - hh - 34, BLACK, 3, 13)
    ctext(d, xf + 100, yc - hh - 34, "v", F, BLACK, "lm")
    ctext(d, (x0 + xf) / 2, yc, "圧縮(疎密)", FT, GRAY)
    note(d, "硬い(E大)ほど速く、重い(ρ大)ほど遅い。鋼では約5.1 km/s")
    save(im, "s1e6WaveSpeed")


# ============================================================
# 6-3 s1e6PSWave : P波(縦)とS波(横)の対比
# ============================================================
def ps_wave():
    im, d = new(); title(d, "P波(縦波)とS波(横波)の対比")
    x0, x1 = 90, 590
    # --- 上段: P波 縦波(進行方向に平行な疎密) ---
    yc = 130
    arrow(d, x0, yc - 46, x1, yc - 46, BLACK, 2, 11); ctext(d, x1 + 8, yc - 46, "進行", FT, BLACK, "lm")
    n = 26
    for i in range(n):
        t = i / (n - 1)
        # 疎密: 密度を正弦で変調
        dens = 1 + 0.6 * math.sin(2 * math.pi * 2.0 * t)
        xx = x0 + (x1 - x0) * t
        col = BLACK if dens > 1 else LGRAY
        d.line((xx, yc - 14, xx, yc + 14), fill=col, width=2)
    # 粒子振動: 進行方向に平行(左右)
    arrow(d, 250, yc + 34, 300, yc + 34, RED, 3, 11); arrow(d, 250, yc + 34, 200, yc + 34, RED, 3, 11)
    ctext(d, W / 2, yc + 54, "P波: 振動方向は進行方向に平行・疎密(気体液体も伝わる)", FT, BLUE)
    d.line((40, 210, 620, 210), fill=LGRAY, width=1)
    # --- 下段: S波 横波(進行方向に垂直なせん断) ---
    yc = 300
    arrow(d, x0, yc + 60, x1, yc + 60, BLACK, 2, 11); ctext(d, x1 + 8, yc + 60, "進行", FT, BLACK, "lm")
    pts = []
    for i in range(81):
        t = i / 80
        xx = x0 + (x1 - x0) * t
        yy = yc - 30 * math.sin(2 * math.pi * 2.0 * t)
        pts.append((xx, yy))
    plot(d, 0, 0, pts, BLACK, 3)
    # 粒子振動: 進行方向に垂直(上下)
    arrow(d, 250, yc, 250, yc - 40, RED, 3, 11); arrow(d, 250, yc, 250, yc + 40, RED, 3, 11)
    ctext(d, W / 2, yc + 78, "S波: 振動方向は進行方向に垂直・せん断(固体中のみ)", FT, GREEN)
    save(im, "s1e6PSWave")


# ============================================================
# 6-4 s1e6ConsistMass : 2節点棒要素と形状関数、整合質量行列
# ============================================================
def consist_mass():
    im, d = new(); title(d, "2節点棒要素の整合質量  [m]=(ρAL/6)[[2,1],[1,2]]")
    # 棒要素
    x0, x1, yb = 120, 340, 110
    bar(d, x0, yb, x1, yb, thick=22, fill=FILL1)
    node(d, x0, yb, 8); node(d, x1, yb, 8)
    ctext(d, x0, yb - 26, "節点1", FT); ctext(d, x1, yb - 26, "節点2", FT)
    ctext(d, x0, yb + 26, "x=0", FT, GRAY); ctext(d, x1, yb + 26, "x=L", FT, GRAY)
    dim(d, x0, yb + 46, x1, yb + 46, "L", col=GRAY)
    # 形状関数グラフ
    ox, oy, xl, yl = 420, 300, 180, 120
    axes(d, ox, oy, xl, yl, "x", "N")
    d.line((ox, oy - yl, ox + xl, oy - yl), fill=LGRAY, width=1)
    ctext(d, ox - 12, oy - yl, "1", FT, GRAY, "rm")
    # N1 = 1 - x/L (top-left → bottom-right)
    plot(d, 0, 0, [(ox, oy - yl), (ox + xl, oy)], BLUE, 3)
    ctext(d, ox + 40, oy - yl - 12, "N1=1-x/L", FT, BLUE)
    # N2 = x/L (bottom-left → top-right)
    plot(d, 0, 0, [(ox, oy), (ox + xl, oy - yl)], GREEN, 3)
    ctext(d, ox + xl - 8, oy - yl - 12, "N2=x/L", FT, GREEN, "rm")
    # 整合質量行列
    ctext(d, 150, 250, "(ρAL/6)", F)
    matrix_grid(d, 230, 220, [["2", "1"], ["1", "2"]], cell=46)
    note(d, "対角に2・非対角に1。全成分の和はρAL(要素全質量)で質量保存")
    save(im, "s1e6ConsistMass")


# ============================================================
# 6-5 s1e6MassOp : 剛性と質量の行列積の規模比較
# ============================================================
def mass_op():
    im, d = new(); title(d, "行列積の規模比較(質量 < 剛性)")
    x0 = 120
    # 剛性
    ctext(d, x0, 130, "剛性 [B]ᵀ[D][B]", F, BLACK, "lm")
    d.rectangle((x0, 150, x0 + 420, 190), outline=BLACK, width=3, fill=FILL3)
    ctext(d, x0 + 210, 170, "[B]は微分(ひずみ)含み列数・段数が多い", FT)
    # 質量
    ctext(d, x0, 240, "質量 [N]ᵀ[N]", F, BLACK, "lm")
    d.rectangle((x0, 260, x0 + 200, 300), outline=BLACK, width=3, fill=FILL1)
    ctext(d, x0 + 100, 280, "[N]のみ", FT)
    note(d, "質量の演算量は剛性より少ない。積分点2倍で演算量は約2倍(点数に比例)")
    save(im, "s1e6MassOp")


# ============================================================
# 6-6 s1e6Rayleigh : レイリー減衰 ζ(ω)=½(α/ω+βω) のU字曲線
# ============================================================
def rayleigh():
    im, d = new(); title(d, "レイリー減衰  ζ(ω)=½(α/ω+βω)")
    ox, oy, xl, yl = 90, 350, 480, 250
    axes(d, ox, oy, xl, yl, "ω", "ζ")
    alpha, beta = 2.0, 0.02
    w_lo, w_hi = 2.0, 22.0
    zmax = 0.55

    def X(w): return ox + (w - w_lo) / (w_hi - w_lo) * xl
    def Y(z): return oy - z / zmax * yl

    # α/ω 項(低周波支配, 破線)
    p1 = [(X(w), Y(0.5 * alpha / w)) for i in range(61) for w in [w_lo + (w_hi - w_lo) * i / 60]]
    for i in range(len(p1) - 1):
        dashed(d, p1[i][0], p1[i][1], p1[i + 1][0], p1[i + 1][1], BLUE, 2, 8, 5)
    # βω 項(高周波支配, 破線)
    p2 = [(X(w), Y(0.5 * beta * w)) for i in range(61) for w in [w_lo + (w_hi - w_lo) * i / 60]]
    for i in range(len(p2) - 1):
        dashed(d, p2[i][0], p2[i][1], p2[i + 1][0], p2[i + 1][1], GREEN, 2, 8, 5)
    # 合成U字(実線)
    pu = [(X(w), Y(0.5 * (alpha / w + beta * w))) for i in range(121) for w in [w_lo + (w_hi - w_lo) * i / 120]]
    plot(d, 0, 0, pu, RED, 3)
    ctext(d, X(4.5), Y(0.5 * alpha / 4.5) - 14, "α/ω(低周波)", FT, BLUE)
    ctext(d, X(18), Y(0.5 * beta * 18) - 14, "βω(高周波)", FT, GREEN)
    ctext(d, X(10), Y(0.55) - 4, "合成ζ", FT, RED)
    note(d, "低周波側はα項、高周波側はβ項が支配。ζは周波数に依存するU字形")
    save(im, "s1e6Rayleigh")


# ============================================================
# 6-7 s1e6Hourglass : 1点積分要素の砂時計(アワーグラス)モード
# ============================================================
def hourglass():
    im, d = new(); title(d, "アワーグラスモード(1点積分のゼロエネルギーモード)")
    # 左: 元の四角形要素 + 中心積分点
    cx, cy, s = 200, 240, 90
    d.rectangle((cx - s, cy - s, cx + s, cy + s), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 6, fill=RED, col=RED)
    ctext(d, cx, cy + 20, "1積分点", FT, RED)
    ctext(d, cx, cy + s + 28, "元の要素", FT)
    # 右: アワーグラス変形(砂時計形)。元を破線、変形を実線
    ex, ey = 470, 240
    dashed(d, ex - s, ey - s, ex + s, ey - s); dashed(d, ex + s, ey - s, ex + s, ey + s)
    dashed(d, ex + s, ey + s, ex - s, ey + s); dashed(d, ex - s, ey + s, ex - s, ey - s)
    # 砂時計(上三角+下三角が中心でくびれる)
    d.line((ex - s, ey - s, ex + s, ey - s), fill=BLACK, width=3)  # 上辺
    d.line((ex + s, ey - s, ex, ey), fill=BLACK, width=3)
    d.line((ex, ey, ex - s, ey - s), fill=BLACK, width=3)
    d.line((ex - s, ey + s, ex + s, ey + s), fill=BLACK, width=3)  # 下辺
    d.line((ex + s, ey + s, ex, ey), fill=BLACK, width=3)
    d.line((ex, ey, ex - s, ey + s), fill=BLACK, width=3)
    node(d, ex, ey, 6, fill=RED, col=RED)
    ctext(d, ex, ey + s + 28, "砂時計状に変形", FT)
    note(d, "中心の1積分点でひずみ0→エネルギーを生じない偽の変形。抗力で抑制する")
    save(im, "s1e6Hourglass")


# ============================================================
# 6-8 s1e6CrashEnergy : 衝突のエネルギー収支
# ============================================================
def crash_energy():
    im, d = new(); title(d, "衝突解析のエネルギー収支(全エネルギーはほぼ一定)")
    ox, oy, xl, yl = 90, 350, 500, 250
    axes(d, ox, oy, xl, yl, "時間", "エネルギー")
    top = 1.0

    def X(t): return ox + t * xl
    def Y(v): return oy - v / 1.1 * yl

    ke, ie, tot = [], [], []
    for i in range(81):
        t = i / 80
        kef = 0.9 * (0.5 * (1 + math.cos(math.pi * t))) + 0.05
        ke.append((X(t), Y(kef)))
        ie.append((X(t), Y(top - kef)))
        tot.append((X(t), Y(top)))
    plot(d, 0, 0, tot, GRAY, 2)
    plot(d, 0, 0, ke, RED, 3)
    plot(d, 0, 0, ie, BLUE, 3)
    ctext(d, X(0.15), Y(0.92), "運動E", FT, RED, "lm")
    ctext(d, X(0.62), Y(0.78), "内部(ひずみ)E", FT, BLUE, "lm")
    ctext(d, X(0.55), Y(1.0) - 12, "全エネルギー(ほぼ一定)", FT, GRAY)
    note(d, "運動E→内部Eへ移る。全Eが跳ぶのは計算異常のサイン")
    save(im, "s1e6CrashEnergy")


# ============================================================
# 6-9 s1e6CentralDiff : 中心差分の3点ステンシル(二段法)
# ============================================================
def central_diff():
    im, d = new(); title(d, "中心差分法の3点ステンシル(二段法)")
    y = 210
    xs = [150, 330, 510]
    labs = ["t n-1", "t n", "t n+1"]
    arrow(d, 80, y, 600, y, BLACK, 2, 11); ctext(d, 610, y, "t", FS, BLACK, "lm")
    for x, lab in zip(xs, labs):
        d.line((x, y - 6, x, y + 6), fill=BLACK, width=2)
        ctext(d, x, y + 22, lab, FT, GRAY)
    # 既知2時刻(塗り) → 未知(白)
    node(d, xs[0], y - 60, 9, fill=BLACK, col=BLACK); ctext(d, xs[0], y - 84, "u n-1(既知)", FT)
    node(d, xs[1], y - 60, 9, fill=BLACK, col=BLACK); ctext(d, xs[1], y - 84, "u n(既知)", FT)
    node(d, xs[2], y - 60, 9, fill="white", col=RED); ctext(d, xs[2], y - 84, "u n+1(未知)", FT, RED)
    arrow(d, xs[0], y - 48, xs[2] - 14, y - 60, BLUE, 2, 11)
    arrow(d, xs[1], y - 48, xs[2] - 14, y - 64, BLUE, 2, 11)
    ctext(d, W / 2, y + 70, "加速度 ün=(u n+1 - 2u n + u n-1)/Δt²", FS)
    note(d, "直前2時刻の変位から次の変位を求める→二段法(多段法)")
    save(im, "s1e6CentralDiff")


# ============================================================
# 6-10 s1e6Newmark : ニューマークβ 平均加速度法 vs 線形加速度法
# ============================================================
def newmark():
    im, d = new(); title(d, "ニューマークβ(γ=1/2): 1ステップ内の加速度")
    ox, oy, xl, yl = 120, 330, 420, 210
    axes(d, ox, oy, xl, yl, "t", "加速度 a")
    an, an1 = 0.35, 0.85  # 端点値(0..1)
    def Y(v): return oy - v * yl
    yn, yn1 = Y(an), Y(an1)
    # 端点マーカ
    node(d, ox, yn, 6, fill=BLACK, col=BLACK); node(d, ox + xl, yn1, 6, fill=BLACK, col=BLACK)
    ctext(d, ox - 10, yn, "a n", FT, GRAY, "rm"); ctext(d, ox + xl + 10, yn1, "a n+1", FT, GRAY, "lm")
    d.line((ox, oy, ox, oy - yl), fill=LGRAY, width=1)
    d.line((ox + xl, oy, ox + xl, oy - yl), fill=LGRAY, width=1)
    # 平均加速度法(β=1/4): 水平一定
    yavg = Y((an + an1) / 2)
    plot(d, 0, 0, [(ox, yavg), (ox + xl, yavg)], RED, 3)
    ctext(d, ox + xl / 2, yavg - 14, "平均加速度法 β=1/4(一定・無条件安定)", FT, RED)
    # 線形加速度法(β=1/6): 直線
    plot(d, 0, 0, [(ox, yn), (ox + xl, yn1)], BLUE, 3)
    ctext(d, ox + xl / 2, Y((an + an1) / 2) + 40, "線形加速度法 β=1/6(直線・条件付き安定)", FT, BLUE)
    ctext(d, ox, oy + 20, "t n", FT, GRAY); ctext(d, ox + xl, oy + 20, "t n+1", FT, GRAY)
    save(im, "s1e6Newmark")


# ============================================================
# 6-11 s1e6NumDamp : 数値減衰は高周波を抑え低周波を残す
# ============================================================
def num_damp():
    im, d = new(); title(d, "数値減衰: 高周波モードを抑え低周波モードは保つ")
    x0, x1 = 90, 600
    # 上段: 高周波モード(急速に減衰)
    yc = 140
    arrow(d, x0 - 10, yc, x1 + 10, yc, LGRAY, 1, 9)
    pts = []
    for i in range(201):
        t = i / 200
        xx = x0 + (x1 - x0) * t
        yy = yc - 55 * math.exp(-3.2 * t) * math.sin(2 * math.pi * 9 * t)
        pts.append((xx, yy))
    plot(d, 0, 0, pts, RED, 2)
    # 包絡線(破線)
    env = [(x0 + (x1 - x0) * i / 60, yc - 55 * math.exp(-3.2 * i / 60)) for i in range(61)]
    for i in range(len(env) - 1):
        dashed(d, env[i][0], env[i][1], env[i + 1][0], env[i + 1][1], GRAY, 1, 6, 5)
    ctext(d, W / 2, yc - 78, "高周波モード → 数値減衰で急速に抑制(実質意味なし)", FT, RED)
    d.line((40, 235, 620, 235), fill=LGRAY, width=1)
    # 下段: 低周波モード(振幅維持)
    yc = 320
    arrow(d, x0 - 10, yc, x1 + 10, yc, LGRAY, 1, 9)
    pts = []
    for i in range(201):
        t = i / 200
        xx = x0 + (x1 - x0) * t
        yy = yc - 50 * math.sin(2 * math.pi * 2 * t)
        pts.append((xx, yy))
    plot(d, 0, 0, pts, BLUE, 2)
    ctext(d, W / 2, yc + 72, "低周波モード → 振幅を保つ(HHT-α法は低周波の精度を維持)", FT, BLUE)
    save(im, "s1e6NumDamp")


# ============================================================
# 6-12 s1e6ExpImp : 陽解法と陰解法の計算フロー対比
# ============================================================
def exp_imp():
    im, d = new(); title(d, "陽解法(中心差分)と陰解法(ニューマークβ)")
    d.line((330, 60, 330, 400), fill=LGRAY, width=1)
    # 左: 陽解法
    ctext(d, 165, 90, "陽解法", F, BLUE)
    lines_l = ["集中質量[M](対角)", "→ 各自由度で割り算", "→ 逆行列計算 不要", "1ステップは軽い", "条件安定(Δt小)"]
    for i, s in enumerate(lines_l):
        ctext(d, 165, 135 + i * 42, s, FS)
    # 右: 陰解法
    ctext(d, 495, 90, "陰解法", F, GREEN)
    lines_r = ["係数[K^]は非対角", "→ 連立方程式を解く", "→ 逆行列/分解 必要", "1ステップは重い", "無条件安定(Δt大可)"]
    for i, s in enumerate(lines_r):
        ctext(d, 495, 135 + i * 42, s, FS)
    note(d, "1ステップの計算量は陽解法が少ない(逆行列計算がいらない)")
    save(im, "s1e6ExpImp")


# ============================================================
# 6-13 s1e6Courant : クーラン条件 v·Δt < ℓ
# ============================================================
def courant():
    im, d = new(); title(d, "クーラン条件  v·Δt < ℓ")
    x0, x1, y = 120, 560, 210
    # 要素(長さℓ)
    d.rectangle((x0, y - 34, x1, y + 34), outline=BLACK, width=3, fill=FILL1)
    node(d, x0, y, 8); node(d, x1, y, 8)
    dim(d, x0, y + 62, x1, y + 62, "ℓ (要素長さ)", col=GRAY)
    # 応力波が1ステップで進む距離 v·Δt(ℓより短い)
    xf = 360
    arrow(d, x0, y, xf, y, RED, 4, 15)
    dim(d, x0, y - 62, xf, y - 62, "v·Δt", col=RED)
    ctext(d, xf, y - 20, "波面", FT, RED)
    note(d, "1ステップで応力波が要素長ℓを超えなければ安定。Δt < ℓ/v")
    save(im, "s1e6Courant")


# ============================================================
# 6-14 s1e6MassScale : マルチタイムステップ と マススケーリング
# ============================================================
def mass_scale():
    im, d = new(); title(d, "計算量を減らす工夫")
    d.line((330, 60, 330, 400), fill=LGRAY, width=1)
    # 左: マルチタイムステップ(領域ごとに別Δt)
    ctext(d, 165, 88, "マルチタイムステップ", FS, BLUE)
    small_grid(d, 60, 130, 160, 210, 5, 4)  # 小要素領域
    ctext(d, 110, 232, "小要素→Δt小", FT)
    small_grid(d, 200, 130, 300, 210, 2, 2)  # 大要素領域
    ctext(d, 250, 232, "大要素→Δt大", FT)
    ctext(d, 165, 280, "領域ごとに刻みを変える", FT, GRAY)
    ctext(d, 165, 306, "(サブサイクリング)", FT, GRAY)
    # 右: マススケーリング(密度↑で波速↓)
    ctext(d, 495, 88, "マススケーリング", FS, GREEN)
    steps = ["密度 ρ を大きくする", "↓", "波速 v=√(E/ρ) が下がる", "↓", "Δt=ℓ/v を大きくできる"]
    for i, s in enumerate(steps):
        ctext(d, 495, 135 + i * 40, s, FS)
    note(d, "マススケーリングは慣性の影響が小さい問題で有効(高速衝突では結果を歪める)")
    save(im, "s1e6MassScale")


# ============================================================
# 6-15 s1e6SDOF : 1自由度ばね質量系
# ============================================================
def sdof():
    im, d = new(); title(d, "1自由度不減衰系  ωn=√(k/m)")
    y = 220
    wall(d, 110, 140, 300, side=1, n=8)
    spring(d, 110, y, 360, y, coils=7, amp=18)
    ctext(d, 235, y - 34, "k", F, BLACK)
    massblock(d, 420, y, 96, 84, "m")
    # 変位方向
    arrow(d, 420, y + 66, 490, y + 66, RED, 3, 12)
    ctext(d, 500, y + 66, "x", FS, RED, "lm")
    note(d, "ωn=√(k/m)。剛性が上がれば速く、質量が増えれば遅く振動する")
    save(im, "s1e6SDOF")


# ============================================================
# 6-16 s1e6TwoDOF : 壁-k1-m1-k2-m2 の2質点2ばね系
# ============================================================
def two_dof():
    im, d = new(); title(d, "2質点2ばね系  壁-k1-m1-k2-m2")
    y = 220
    wall(d, 55, 150, 290, side=1, n=8)
    spring(d, 55, y, 185, y, coils=5, amp=15)
    ctext(d, 120, y - 30, "k1", FS)
    massblock(d, 245, y, 84, 74, "m1")
    spring(d, 287, y, 415, y, coils=5, amp=15)
    ctext(d, 351, y - 30, "k2", FS)
    massblock(d, 475, y, 84, 74, "m2")
    # 変位
    arrow(d, 245, y - 58, 300, y - 58, RED, 3, 11); ctext(d, 310, y - 58, "x1", FT, RED, "lm")
    arrow(d, 475, y - 58, 530, y - 58, RED, 3, 11); ctext(d, 540, y - 58, "x2", FT, RED, "lm")
    note(d, "低次・高次の2つの固有モードをもつ。特性方程式(ω²の2次式)から求める")
    save(im, "s1e6TwoDOF")


# ============================================================
# 6-17 s1e6ModeSuper : モード重合(3モードを重ね合わせ)
# ============================================================
def mode_super():
    im, d = new(); title(d, "モード重合法(卓越モードの重ね合わせ)")
    def modewave(x0, x1, yc, k, col, amp=26):
        pts = []
        for i in range(61):
            t = i / 60
            xx = x0 + (x1 - x0) * t
            yy = yc - amp * math.sin(k * math.pi * t)
            pts.append((xx, yy))
        plot(d, 0, 0, pts, col, 3)
    lx0, lx1 = 60, 240
    ycs = [110, 200, 290]
    ks = [1, 2, 3]
    cols = [BLUE, GREEN, ORANGE]
    labs = ["1次モード", "2次モード", "3次モード"]
    for yc, k, c, lab in zip(ycs, ks, cols, labs):
        d.line((lx0, yc, lx1, yc), fill=LGRAY, width=1)
        modewave(lx0, lx1, yc, k, c)
        ctext(d, lx1 + 6, yc, lab, FT, c, "lm")
    ctext(d, 150, 150, "+", F); ctext(d, 150, 245, "+", F)
    ctext(d, 320, 200, "=", FL)
    # 合成
    rx0, rx1, ryc = 380, 620, 200
    d.line((rx0, ryc, rx1, ryc), fill=LGRAY, width=1)
    pts = []
    for i in range(121):
        t = i / 120
        xx = rx0 + (rx1 - rx0) * t
        yy = ryc - (26 * math.sin(math.pi * t) + 16 * math.sin(2 * math.pi * t) + 10 * math.sin(3 * math.pi * t))
        pts.append((xx, yy))
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, (rx0 + rx1) / 2, ryc + 40, "全体応答", FT, RED)
    note(d, "卓越する数個のモードで近似(全モードなら直接時間積分と一致)")
    save(im, "s1e6ModeSuper")


# ============================================================
# 6-18 s1e6RespSpec : 応答スペクトルの物理的意味の3対1対応
# ============================================================
def resp_spec():
    im, d = new(); title(d, "応答スペクトルの物理的意味")
    rows = [("S_D", "ひずみ(最大変位)", 130),
            ("S_V", "エネルギー(最大)", 220),
            ("S_A", "力(慣性力 m·S_A)", 310)]
    for left, right, y in rows:
        d.rectangle((110, y - 30, 240, y + 30), outline=BLACK, width=3, fill=FILL1)
        ctext(d, 175, y, left, F)
        arrow(d, 250, y, 400, y, BLUE, 3, 14)
        d.rectangle((410, y - 30, 600, y + 30), outline=BLACK, width=3, fill=FILL2)
        ctext(d, 505, y, right, FS)
    note(d, "加速度→力、速度→エネルギー、変位→ひずみ の3対1で覚える")
    save(im, "s1e6RespSpec")


# ============================================================
# 6-19 s1e6SdSvSa : S_D, S_V=ωS_D, S_A=ω²S_D の関係
# ============================================================
def sd_sv_sa():
    im, d = new(); title(d, "応答スペクトルの関係  S_V=ωS_D, S_A=ω²S_D")
    base = 350
    bars = [(150, 70, "S_D", "変位", BLUE),
            (350, 130, "S_V=ω·S_D", "速度", GREEN),
            (550, 200, "S_A=ω²·S_D", "加速度", RED)]
    bw = 80
    for cx, h, lab, sub, col in bars:
        d.rectangle((cx - bw / 2, base - h, cx + bw / 2, base), outline=BLACK, width=3, fill=FILL1)
        ctext(d, cx, base - h - 16, lab, FS, col)
        ctext(d, cx, base + 18, sub, FT, GRAY)
    d.line((90, base, 610, base), fill=BLACK, width=2)
    # ×ω 矢印
    arrow(d, 200, 150, 300, 150, BLACK, 3, 12); ctext(d, 250, 134, "×ω", FT)
    arrow(d, 400, 130, 500, 130, BLACK, 3, 12); ctext(d, 450, 114, "×ω", FT)
    note(d, "変位→速度で×ω、速度→加速度でさらに×ω(変位→加速度は×ω²)")
    save(im, "s1e6SdSvSa")


# ============================================================
# 6-20 s1e6Resonance : 共振曲線(減衰比 ζ 違い)
# ============================================================
def resonance():
    im, d = new(); title(d, "共振曲線  M=1/√((1-r²)²+(2ζr)²)  (r=ω/Ω)")
    ox, oy, xl, yl = 90, 350, 500, 260
    axes(d, ox, oy, xl, yl, "ω/Ω", "M")
    r_hi = 2.5
    m_hi = 5.5

    def X(r): return ox + r / r_hi * xl
    def Y(m): return oy - min(m, m_hi) / m_hi * yl

    # 目盛 r=1
    x1 = X(1.0)
    dashed(d, x1, oy, x1, oy - yl, LGRAY, 1, 6, 5)
    ctext(d, x1, oy + 16, "1", FT, GRAY)
    zetas = [(0.1, RED, "ζ=0.1"), (0.25, BLUE, "ζ=0.25"), (0.5, GREEN, "ζ=0.5")]
    for z, col, lab in zetas:
        pts = []
        for i in range(251):
            r = r_hi * i / 250
            M = 1.0 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
            pts.append((X(r), Y(M)))
        plot(d, 0, 0, pts, col, 3)
        # ピーク付近にラベル
        Mp = 1.0 / (2 * z)
        ctext(d, X(1.0) + 26, Y(Mp), lab, FT, col, "lm")
    note(d, "ζが小さいほどピークは高い。共振点 ω/Ω=1 で M=1/(2ζ)")
    save(im, "s1e6Resonance")


# ============================================================
if __name__ == "__main__":
    eq_motion()
    wave_speed()
    ps_wave()
    consist_mass()
    mass_op()
    rayleigh()
    hourglass()
    crash_energy()
    central_diff()
    newmark()
    num_damp()
    exp_imp()
    courant()
    mass_scale()
    sdof()
    two_dof()
    mode_super()
    resp_spec()
    sd_sv_sa()
    resonance()
    print("done ch6")
