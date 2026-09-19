# -*- coding: utf-8 -*-
"""熱流体力学1級 第18章「燃焼の基礎2」の公式・用語図(t1f18*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(sigma, kappa, Delta, propto, T^4, CO2, H2O, Kp, Kc, R0 等)。
※ 問題図 t1e18* とは別ファイル。上書きしない。"""
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


def pcircle(d, x, y, r, fill=FILL1, col=BLACK, wd=2):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wd, fill=fill)


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


# ============================================================
# ============  公式・用語図  t1f18*  (21)  ==================
# ============================================================

# 18-1 t1f18ActivationEnergy : 活性化エネルギーの定義(山型曲線)
def activation_energy():
    im, d = new(); title(d, "活性化エネルギー E : 反応物レベルから山頂までの高さ")
    ox, oy, xl, yl = 90, 360, 500, 285
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "反応の進行", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "ポテンシャルE", FT, BLACK, "rm")
    def yE(E): return oy - (E / 400.0) * yl
    y_r, y_t, y_p = yE(120), yE(340), yE(60)
    x_r, x_t, x_p = ox + 0.14 * xl, ox + 0.50 * xl, ox + 0.86 * xl
    d.line((ox + 0.02 * xl, y_r, x_r, y_r), fill=BLUE, width=3)
    pts = []
    for i in range(0, 101):
        t = i / 100
        x = x_r + (x_p - x_r) * t
        if t <= 0.5:
            s = t / 0.5; y = y_r + (y_t - y_r) * (0.5 - 0.5 * math.cos(math.pi * s))
        else:
            s = (t - 0.5) / 0.5; y = y_t + (y_p - y_t) * (0.5 - 0.5 * math.cos(math.pi * s))
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    d.line((x_p, y_p, ox + 0.97 * xl, y_p), fill=BLUE, width=3)
    for yy in (y_r, y_t, y_p):
        dashed(d, ox, yy, ox + xl, yy, LGRAY, 1, 6, 5)
    ctext(d, x_r, y_r + 20, "A+B (反応物)", FT, BLUE)
    ctext(d, x_t, y_t - 18, "(AB)* 遷移状態", FT, BLUE)
    ctext(d, x_p, y_p + 20, "C+D (生成物)", FT, GREEN)
    # 正反応の活性化エネルギー(反応物レベル->山頂)を赤矢印で
    xa = ox + 0.30 * xl
    arrow(d, xa, y_r, xa, y_t, RED, 3, 13)
    arrow(d, xa, y_t, xa, y_r, RED, 3, 13)
    ctext(d, xa - 8, (y_r + y_t) / 2, "E (正反応)", FT, RED, "rm")
    # 逆反応の活性化エネルギー(生成物->山頂)は別物と示す
    xb = ox + 0.70 * xl
    dashed(d, xb, y_t, xb, y_p, GRAY, 1, 5, 4)
    ctext(d, xb + 8, (y_t + y_p) / 2, "逆反応のE (別物)", FT, GRAY, "lm")
    # 反応熱(反応物-生成物差)は別物 -> 上部の空き領域に注記
    ctext(d, ox + 0.24 * xl, oy - 0.94 * yl, "反応物-生成物の差 = 反応熱(別物)", FT, GRAY)
    note(d, "E は反応物レベルから遷移状態の山頂までの高さ(反応熱や逆反応Eと混同しない)")
    save(im, "t1f18ActivationEnergy")


# 18-2 t1f18Arrhenius : アレニウスの法則(k の温度依存)
def arrhenius():
    im, d = new(); title(d, "アレニウスの法則  k = A exp(-E / R0 T)")
    ox, oy, xl, yl = 120, 350, 430, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "速度定数 k", FT, BLACK, "rm")
    # 高温で急上昇する曲線 k = exp(-b/T) 型
    pts = []
    for i in range(0, 201):
        t = 0.18 + (1.0 - 0.18) * i / 200        # T を規格化(小=低温)
        val = math.exp(-0.28 / t)                # exp(-E/R0T) の形
        pts.append((ox + ((t - 0.18) / 0.82) * xl, oy - val * yl * 1.35))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.62 * xl, oy - 0.42 * yl, "高温ほど急増", FT, RED, "lm")
    # 100K上げると約3倍の注記
    box(d, ox + 0.03 * xl, oy - yl - 4, ox + 0.55 * xl, oy - yl + 62, FILL1, 2)
    ctext(d, ox + 0.29 * xl, oy - yl + 12, "A: 頻度因子  E: 活性化E", FT, GRAY)
    ctext(d, ox + 0.29 * xl, oy - yl + 40, "R0: 一般気体定数  T: 絶対温度", FT, GRAY)
    note(d, "T が上がると -E/R0T の絶対値が小さくなり k が急激に大きくなる(圧力には非依存)")
    save(im, "t1f18Arrhenius")


# 18-3 t1f18ArrheniusPlot : アレニウスプロット(対数形・傾き=-E/R0)
def arrhenius_plot():
    im, d = new(); title(d, "アレニウスプロット  ln k = ln A - (E/R0)(1/T)")
    ox, oy, xl, yl = 130, 340, 420, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "1/T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "ln k", FS, BLACK, "rm")
    # 右下がり直線
    xA, yA = ox + 0.05 * xl, oy - 0.90 * yl
    xB, yB = ox + 0.90 * xl, oy - 0.15 * yl
    d.line((xA, yA, xB, yB), fill=BLUE, width=3)
    # 切片 ln A (1/T -> 0 側)
    node(d, ox, oy - (0.90 + (0.90 - 0.15) * (0.0 - 0.05) / (0.90 - 0.05)) * yl, 5, fill=BLUE, col=BLUE)
    dashed(d, ox, yA, xA, yA, GRAY, 1, 6, 5)
    ctext(d, ox + 6, yA - 12, "切片 = ln A", FT, GREEN, "lm")
    # 傾き三角形
    tx0, ty0 = ox + 0.45 * xl, oy - 0.585 * yl
    tx1 = ox + 0.68 * xl
    ty1 = ty0
    ty2 = oy - 0.38 * yl
    dashed(d, tx0, ty0, tx1, ty1, GRAY, 1, 5, 4)
    dashed(d, tx1, ty1, tx1, ty2, GRAY, 1, 5, 4)
    ctext(d, (tx0 + tx1) / 2, ty0 - 12, "d(1/T)", FT, GRAY)
    ctext(d, tx1 + 8, (ty1 + ty2) / 2, "d(ln k)", FT, GRAY, "lm")
    ctext(d, ox + 0.30 * xl, oy - 0.72 * yl, "傾き = -E / R0", FT, RED, "lm")
    note(d, "1/T 対 ln k は直線. 傾き -E/R0 から E を, 切片 ln A から A を求める")
    save(im, "t1f18ArrheniusPlot")


# 18-4 t1f18ModifiedArrhenius : 修正アレニウス(T^n 項)
def modified_arrhenius():
    im, d = new(); title(d, "修正アレニウスの法則  k = A T^n exp(-E / R0 T)")
    # 式の分解カード
    box(d, 60, 90, 600, 168, FILL1, 2)
    ctext(d, 330, 118, "k  =  A  x  T^n  x  exp(-E / R0 T)", FL, BLACK)
    ctext(d, 150, 150, "頻度因子", FT, GRAY)
    ctext(d, 330, 150, "温度べき乗(補正)", FT, RED)
    ctext(d, 500, 150, "指数項(山越え)", FT, BLUE)
    # n による違いの模式(右上がり)
    ox, oy, xl, yl = 130, 350, 420, 150
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "T^n 寄与", FT, BLACK, "rm")
    for (n, col, lab) in [(0.0, GRAY, "n=0 (通常アレニウス)"), (0.5, BLUE, "n=0.5 (sqrt T)"), (1.0, RED, "n=1")]:
        pts = []
        for i in range(0, 201):
            t = i / 200
            val = t ** n if n > 0 else 0.5
            pts.append((ox + t * xl, oy - val * yl * 0.9))
        d.line(pts, fill=col, width=3, joint="curve")
    ctext(d, ox + 0.55 * xl, oy - 0.85 * yl, "n=1", FT, RED, "lm")
    ctext(d, ox + 0.62 * xl, oy - 0.55 * yl, "n=0.5", FT, BLUE, "lm")
    ctext(d, ox + 0.60 * xl, oy - 0.42 * yl, "n=0 (一定)", FT, GRAY, "lm")
    note(d, "T^n で頻度因子の温度依存を補正. n=0 で通常のアレニウスに戻る")
    save(im, "t1f18ModifiedArrhenius")


# 18-5 t1f18Kp : 分圧基準の平衡定数(圧力項 (p/N)^Delta nu)
def kp():
    im, d = new(); title(d, "分圧基準の平衡定数 Kp と圧力依存(Delta nu)")
    ctext(d, 330, 78, "nA A + nB B  <->  nC C + nD D", FS, BLACK)
    # Kp 式
    box(d, 55, 100, 605, 176, FILL1, 2)
    ctext(d, 330, 128, "Kp = (NC^nC ND^nD)/(NA^nA NB^nB) x (p_total/N_total)^Delta nu", FT, BLACK)
    ctext(d, 330, 156, "Delta nu = (nC+nD) - (nA+nB)   <- 反応前後のモル数変化", FT, RED)
    # 2ケースの天秤で圧力依存の有無
    def balance(cx, cy, nl, nr, eq, dep):
        ctext(d, cx, cy - 62, eq, FT, BLACK)
        tilt = 12 if nl > nr else (-12 if nl < nr else 0)
        lx, rx = cx - 78, cx + 78
        ly, ry = cy - 6 + tilt, cy - 6 - tilt
        d.line((lx, ly, rx, ry), fill=BLACK, width=3)
        d.line((cx, cy - 6, cx, cy + 20), fill=BLACK, width=3)
        d.polygon((cx - 9, cy + 20, cx + 9, cy + 20, cx, cy + 6), outline=BLACK, width=2, fill=FILL1)
        for k in range(nl):
            pcircle(d, lx - 12 + (k % 3) * 15, ly - 14 - (k // 3) * 14, 6, FILL2)
        for k in range(nr):
            pcircle(d, rx - 12 + (k % 3) * 15, ry - 14 - (k // 3) * 14, 6, (235, 242, 250), BLUE, 2)
        ctext(d, lx, ly + 16, "反応 %d" % nl, FT, GRAY)
        ctext(d, rx, ry + 16, "生成 %d" % nr, FT, GRAY)
        ctext(d, cx, cy + 46, dep, FT, (RED if "依存" in dep else GREEN))
    balance(180, 310, 3, 2, "2CO + O2 <-> 2CO2", "Delta nu=-1 : 圧力に依存")
    balance(490, 310, 3, 3, "CH4+2O2 <-> CO2+2H2O", "Delta nu=0 : 圧力に無依存")
    note(d, "(p/N)^Delta nu の因子ゆえ Delta nu!=0 で平衡組成が全圧に依存する")
    save(im, "t1f18Kp")


# 18-6 t1f18Kc : 濃度基準平衡定数 Kc = kf/kb
def kc():
    im, d = new(); title(d, "濃度基準の平衡定数  Kc = kf / kb")
    box(d, 60, 140, 260, 250, (225, 235, 250))
    ctext(d, 160, 172, "反応物", FS, BLUE); ctext(d, 160, 210, "aA + bB", FT, BLUE)
    box(d, 400, 140, 600, 250, (225, 245, 230))
    ctext(d, 500, 172, "生成物", FS, GREEN); ctext(d, 500, 210, "cC + dD", FT, GREEN)
    arrow(d, 265, 170, 395, 170, RED, 3, 13); ctext(d, 330, 150, "正反応 kf", FT, RED)
    arrow(d, 395, 222, 265, 222, BLUE, 3, 13); ctext(d, 330, 242, "逆反応 kb", FT, BLUE)
    box(d, 90, 290, 570, 372, FILL1, 2)
    ctext(d, 330, 314, "平衡: q_net=0  ->  kf[A]^a[B]^b = kb[C]^c[D]^d", FT, BLACK)
    ctext(d, 330, 348, "Kc = [C]^c[D]^d / [A]^a[B]^b = kf / kb", FS, BLACK)
    note(d, "平衡定数は正逆の反応速度定数の比. kf>kb なら Kc>1 で生成物側に偏る")
    save(im, "t1f18Kc")


# 18-7 t1f18KpKcRelation : Kp と Kc の関係
def kp_kc_relation():
    im, d = new(); title(d, "Kp と Kc の関係  Kp = Kc (R0 T)^Delta nu")
    # 2つの箱を換算係数でつなぐ
    box(d, 70, 150, 250, 250, (225, 245, 230))
    ctext(d, 160, 185, "Kc", FL, GREEN); ctext(d, 160, 220, "濃度基準", FT, GRAY)
    box(d, 410, 150, 590, 250, (225, 235, 250))
    ctext(d, 500, 185, "Kp", FL, BLUE); ctext(d, 500, 220, "分圧基準", FT, GRAY)
    arrow(d, 255, 190, 405, 190, BLACK, 3, 13)
    ctext(d, 330, 168, "x (R0 T)^Delta nu", FS, RED)
    ctext(d, 330, 214, "理想気体 p_i = c_i R0 T", FT, GRAY)
    # Delta nu=0 の特例
    box(d, 90, 290, 570, 372, FILL1, 2)
    ctext(d, 330, 314, "Delta nu = 0  ->  (R0 T)^0 = 1  ->  Kp = Kc", FT, GREEN)
    ctext(d, 330, 348, "Delta nu != 0  ->  温度で換算係数が変わる", FT, RED)
    note(d, "分圧と濃度の橋渡し. モル数不変(Delta nu=0)なら両者は一致する")
    save(im, "t1f18KpKcRelation")


# 18-8 t1f18ReactionHeat : 反応熱=生成物-反応物の生成エンタルピー差
def reaction_heat():
    im, d = new(); title(d, "反応熱 = 生成物の生成エンタルピー和 - 反応物の和")
    ox, oy, xl, yl = 90, 355, 500, 285
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "反応の進行", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "エンタルピー H", FT, BLACK, "rm")
    y_r = oy - 0.78 * yl
    y_p = oy - 0.22 * yl
    x_rL, x_rR = ox + 0.06 * xl, ox + 0.36 * xl
    x_pL, x_pR = ox + 0.60 * xl, ox + 0.92 * xl
    d.line((x_rL, y_r, x_rR, y_r), fill=BLUE, width=4)
    ctext(d, (x_rL + x_rR) / 2, y_r - 20, "反応物 (CH4+2O2)", FT, BLUE)
    ctext(d, (x_rL + x_rR) / 2, y_r + 18, "sum dHf(反応物)", FT, GRAY)
    d.line((x_pL, y_p, x_pR, y_p), fill=GREEN, width=4)
    ctext(d, (x_pL + x_pR) / 2, y_p - 20, "生成物 (CO2+2H2O)", FT, GREEN)
    ctext(d, (x_pL + x_pR) / 2, y_p + 18, "sum dHf(生成物)", FT, GRAY)
    xm = ox + 0.48 * xl
    dashed(d, x_rR, y_r, xm, y_r, GRAY, 1, 6, 5)
    dashed(d, x_pL, y_p, xm, y_p, GRAY, 1, 6, 5)
    arrow(d, xm, y_r, xm, y_p, RED, 3, 13)
    ctext(d, xm + 12, (y_r + y_p) / 2, "Delta H_r < 0 (発熱)", FT, RED, "lm")
    note(d, "Delta H_r = sum dHf(生成物) - sum dHf(反応物). 状態量ゆえ経路によらない")
    save(im, "t1f18ReactionHeat")


# 18-9 t1f18HessLaw : ヘスの法則(経路によらず反応熱一定)
def hess_law():
    im, d = new(); title(d, "ヘスの法則 : 反応熱は経路によらず始点と終点で決まる")
    # 三角の状態図: C -> CO -> CO2, C -> CO2 直接
    C  = (140, 180)
    CO = (400, 110)
    CO2 = (520, 300)
    for (p, lab, col) in [(C, "C + O2", BLUE), (CO, "CO + 1/2 O2", ORANGE), (CO2, "CO2", GREEN)]:
        pcircle(d, p[0], p[1], 34, FILL1, col, 3)
        ctext(d, p[0], p[1], lab, FT, col)
    # 直接経路
    arrow(d, C[0] + 30, C[1] + 12, CO2[0] - 30, CO2[1] - 12, GREEN, 3, 13)
    ctext(d, 300, 268, "直接: dH(C->CO2)", FT, GREEN, "mm")
    # 経由経路
    arrow(d, C[0] + 26, C[1] - 8, CO[0] - 34, CO[1] + 4, ORANGE, 3, 13)
    ctext(d, 270, 118, "dH1 (C->CO)", FT, ORANGE)
    arrow(d, CO[0] + 4, CO[1] + 34, CO2[0] - 6, CO2[1] - 34, ORANGE, 3, 13)
    ctext(d, 490, 195, "dH2 (CO->CO2)", FT, ORANGE, "lm")
    # 等式
    box(d, 60, 350, 600, 400, FILL1, 2)
    ctext(d, 330, 375, "dH(C->CO2) = dH1 + dH2   (どちらの道でも同じ)", FT, BLACK)
    note(d, "直接測りにくい反応熱も, 測れる反応のたし引きで間接的に求められる")
    save(im, "t1f18HessLaw")


# 18-10 t1f18StdEnthalpy : 標準生成エンタルピー(標準物質=0)
def std_enthalpy():
    im, d = new(); title(d, "標準生成エンタルピー dHf : 安定な単体は 0")
    ox, oy, xl, yl = 90, 235, 500, 150
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "物質", FS, BLACK, "lm")
    arrow(d, ox, oy + 120, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "dHf", FT, BLACK, "rm")
    d.line((ox, oy, ox + xl, oy), fill=BLACK, width=2)
    ctext(d, ox + xl + 4, oy - 14, "基準線 dHf = 0", FT, GRAY, "lm")
    items = [("H2", 0), ("O2", 0), ("N2", 0), ("C(黒鉛)", 0), ("CO2", -1)]
    for i, (lab, v) in enumerate(items):
        cx = ox + 0.10 * xl + i * 0.19 * xl
        if v == 0:
            d.rectangle((cx - 22, oy - 4, cx + 22, oy), outline=BLACK, width=2, fill=FILL2)
            ctext(d, cx, oy + 22, lab, FT, GRAY)
            ctext(d, cx, oy - 18, "0", FT, GREEN)
        else:
            yb = oy + 0.62 * yl
            d.rectangle((cx - 22, oy, cx + 22, yb), outline=BLACK, width=2, fill=(250, 230, 230))
            ctext(d, cx, yb + 22, lab, FT, RED)
            ctext(d, cx, (oy + yb) / 2, "約 -394", FT, RED)
            ctext(d, cx, yb + 44, "kJ/mol", FT, GRAY)
    ctext(d, ox + 0.10 * xl + 1.5 * 0.19 * xl, oy - yl + 6, "標準物質(H2,O2,N2,黒鉛...) = 0", FT, GREEN)
    note(d, "安定な単体は定義で 0. 化合物(CO2 等)は 0 でない固有値を持つ")
    save(im, "t1f18StdEnthalpy")


# 18-11 t1f18GibbsFormation : G=H-TS, Delta G=Delta H - T Delta S
def gibbs_formation():
    im, d = new(); title(d, "ギブス自由エネルギー  G = H - T S")
    # 式の分解
    box(d, 55, 90, 605, 165, FILL1, 2)
    ctext(d, 330, 118, "Delta G = Delta H  -  T Delta S", FL, BLACK)
    ctext(d, 200, 148, "発熱の寄与", FT, RED)
    ctext(d, 460, 148, "乱雑さの寄与", FT, BLUE)
    # 綱引きの図
    cx, cy = 330, 260
    d.line((110, cy, 550, cy), fill=BLACK, width=3)
    node(d, cx, cy, 10, fill=FILL1)
    arrow(d, cx - 20, cy, 130, cy, RED, 4, 14); ctext(d, 130, cy - 20, "Delta H", FS, RED, "lm")
    arrow(d, cx + 20, cy, 530, cy, BLUE, 4, 14); ctext(d, 530, cy - 20, "T Delta S", FS, BLUE, "rm")
    ctext(d, cx, cy + 26, "綱引きで反応の向きが決まる", FT, GRAY)
    # 自発性の判定
    box(d, 90, 320, 570, 388, FILL2, 2)
    ctext(d, 330, 344, "Delta G < 0 : 自発的に進む(最大仕事の大きさ)", FT, GREEN)
    ctext(d, 330, 372, "標準生成G: 安定な単体=0, 化合物(CO2)=非0", FT, GRAY)
    note(d, "定温定圧で Delta G が負なら反応は自発. その大きさが取り出せる最大仕事")
    save(im, "t1f18GibbsFormation")


# 18-12 t1f18DeltaGEquilibrium : Delta G0 = -R0 T ln K
def deltag_equilibrium():
    im, d = new(); title(d, "平衡とギブス自由エネルギー  Delta G0 = -R0 T ln K")
    ox, oy, xl, yl = 120, 250, 430, 150
    # 横軸 Delta G0(左が負), 縦軸 ln K
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "Delta G0", FS, BLACK, "lm")
    arrow(d, ox, oy + 110, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "ln K", FS, BLACK, "rm")
    d.line((ox, oy, ox + xl, oy), fill=LGRAY, width=1)
    # 右下がり直線 lnK = -DeltaG0/(R0T)
    d.line((ox + 0.05 * xl, oy - 0.9 * yl, ox + 0.95 * xl, oy + 0.72 * yl), fill=BLUE, width=3)
    ctext(d, ox + 0.10 * xl, oy - 0.75 * yl, "Delta G0 < 0 : K>1 生成物側", FT, GREEN, "lm")
    ctext(d, ox + 0.52 * xl, oy + 0.50 * yl, "Delta G0 > 0 : K<1 反応物側", FT, RED, "lm")
    ctext(d, ox + 0.55 * xl, oy - 0.25 * yl, "傾き = -1/(R0 T)", FT, BLUE, "lm")
    note(d, "熱力学量 Delta G0 から到達できる平衡位置 K を予測する(反応の速さとは別)")
    save(im, "t1f18DeltaGEquilibrium")


# 18-13 t1f18Entropy : エントロピー(状態量・断熱系で増大)
def entropy():
    im, d = new(); title(d, "エントロピー S : 状態量, 断熱系では減少しない")
    box(d, 55, 85, 605, 300, "white", 2)
    for xx in range(55, 606, 26):
        d.line((xx, 85, xx + 14, 71), fill=LGRAY, width=1)
    ctext(d, 330, 100, "断熱された閉じた系", FT, GRAY)
    cx, cy = 175, 195
    node(d, cx, cy, 8, fill=FILL1)
    ctext(d, cx, cy + 24, "ある状態", FT, GRAY)
    arrow(d, cx + 18, cy - 30, 430, 135, GREEN, 3, 13)
    ctext(d, 445, 132, "可逆 : S 一定", FT, GREEN, "lm")
    arrow(d, cx + 18, cy + 6, 430, 205, RED, 3, 13)
    ctext(d, 445, 205, "不可逆 : S 増大", FT, RED, "lm")
    arrow(d, cx + 18, cy + 42, 430, 270, GRAY, 3, 13)
    ctext(d, 445, 272, "S 減少 (起こらない)", FT, GRAY, "lm")
    d.line((548, 255, 578, 285), fill=RED, width=4)
    d.line((578, 255, 548, 285), fill=RED, width=4)
    # 状態量の注記
    box(d, 90, 320, 570, 388, FILL1, 2)
    ctext(d, 330, 344, "S は状態量: 2状態が決まれば経路によらず定まる", FT, BLACK)
    ctext(d, 330, 372, "絞り・自由膨張は不可逆 -> S 増大(第二法則)", FT, GRAY)
    note(d, "断熱閉系では可逆で一定, 不可逆で増大. 総和が減少することはない")
    save(im, "t1f18Entropy")


# 18-14 t1f18Exergy : エクセルギー E = G0 - G1
def exergy():
    im, d = new(); title(d, "エクセルギー E = (H0-H1) - T1(S0-S1) = G0 - G1")
    bx0, bx1, by0, by1 = 90, 590, 150, 210
    total = bx1 - bx0
    xs = bx0 + total * (770.0 / 800.0)
    d.rectangle((bx0, by0, xs, by1), outline=BLACK, width=3, fill=(225, 245, 230))
    d.rectangle((xs, by0, bx1, by1), outline=BLACK, width=3, fill=(250, 230, 230))
    ctext(d, (bx0 + xs) / 2, (by0 + by1) / 2, "有効分 E = G0 - G1", FT, GREEN)
    ctext(d, (xs + bx1) / 2, by1 + 24, "無効分", FT, RED)
    ctext(d, (xs + bx1) / 2, by1 + 44, "T1(S0-S1)", FT, RED)
    dim(d, bx0, by0 - 24, bx1, by0 - 24, "エンタルピー差 H0 - H1", col=GRAY)
    dashed(d, xs, by0 - 6, xs, by1 + 56, GRAY, 1, 6, 5)
    box(d, 90, 275, 590, 355, FILL1, 2)
    ctext(d, 340, 300, "等温燃焼 T0=T1 -> E = G0 - G1", FS, BLACK)
    ctext(d, 340, 332, "取り出せる最大仕事 = ギブス自由エネルギーの減少分", FT, GRAY)
    note(d, "エンタルピー差から使えない分 T1*Delta S を引いた有効分がエクセルギー")
    save(im, "t1f18Exergy")


# 18-15 t1f18Diffusion : 拡散係数 D propto 1/rho (圧力に反比例)
def diffusion():
    im, d = new(); title(d, "拡散係数  D propto sqrt(T) / rho  (圧力に反比例)")
    ox, oy, xl, yl = 100, 330, 300, 220
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "圧力 p", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "拡散係数 D", FT, BLACK, "rm")
    pts = []
    for i in range(0, 201):
        t = 0.12 + (1.0 - 0.12) * i / 200
        val = 0.12 / t
        pts.append((ox + t * xl, oy - val * yl * 1.05))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.5 * xl, oy - 0.55 * yl, "D propto 1/p", FT, BLUE, "lm")
    # 圧力2倍で D 半減の目盛
    for (t, lab) in [(0.24, "p"), (0.48, "2p")]:
        xp = ox + t * xl; val = 0.12 / t
        yp = oy - val * yl * 1.05
        node(d, xp, yp, 5, fill=BLUE, col=BLUE)
        dashed(d, xp, oy, xp, yp, GRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, GRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, GRAY)
    # 右: 密度対比
    box(d, 440, 95, 620, 205, "white", 2)
    ctext(d, 530, 112, "低圧(疎)", FT, GRAY)
    for (px, py) in [(465, 150), (500, 175), (545, 145), (590, 178), (515, 190)]:
        pcircle(d, px, py, 6, FILL2)
    ctext(d, 530, 222, "自由行程 長 -> 拡散大", FT, GRAY)
    box(d, 440, 255, 620, 365, "white", 2)
    ctext(d, 530, 272, "高圧(密)", FT, GRAY)
    for px in range(455, 616, 20):
        for py in range(296, 356, 20):
            pcircle(d, px, py, 5, FILL2)
    ctext(d, 530, 382, "行程 短 -> 拡散小", FT, RED)
    note(d, "1/rho ゆえ密度(圧力)に反比例. sqrt(T) で高温ほど拡散は速くなる")
    save(im, "t1f18Diffusion")


# 18-16 t1f18Viscosity : 粘性係数 mu propto sqrt(T) (気体)
def viscosity():
    im, d = new(); title(d, "気体の粘性係数  mu propto sqrt(T)  (液体とは逆)")
    ox, oy, xl, yl = 110, 350, 460, 260
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "粘性係数 mu", FT, BLACK, "rm")
    gpts = []
    for i in range(0, 201):
        t = i / 200
        val = 0.18 + 0.64 * math.sqrt(t)
        gpts.append((ox + t * xl, oy - val * yl))
    d.line(gpts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.66 * xl, oy - 0.86 * yl, "気体: mu propto sqrt(T)", FT, BLUE, "mm")
    lpts = []
    for i in range(0, 201):
        t = i / 200
        val = 0.85 * math.exp(-1.9 * t) + 0.06
        lpts.append((ox + t * xl, oy - val * yl))
    d.line(lpts, fill=RED, width=3, joint="curve")
    ctext(d, ox + 0.42 * xl, oy - 0.20 * yl, "液体: 右下がり(参考)", FT, RED, "lm")
    note(d, "気体は運動量輸送が主役で高温ほど粘性増大. 液体は逆に減少する")
    save(im, "t1f18Viscosity")


# 18-17 t1f18StefanBoltzmann : Eb = sigma T^4
def stefan_boltzmann():
    im, d = new(); title(d, "ステファン-ボルツマン則  Eb = sigma T^4 (4乗則)")
    ox, oy, xl, yl = 130, 350, 420, 260
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "絶対温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "ふく射能 Eb", FT, BLACK, "rm")
    pts = []
    for i in range(0, 201):
        t = i / 200
        val = t ** 4
        pts.append((ox + t * xl, oy - val * yl * 0.92))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    for (t, lab, hval) in [(0.5, "T", 0.5 ** 4), (1.0, "2T", 1.0)]:
        xp = ox + t * xl; yp = oy - hval * yl * 0.92
        node(d, xp, yp, 5, fill=BLUE, col=BLUE)
        dashed(d, xp, oy, xp, yp, GRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, GRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, GRAY)
    ctext(d, ox + 40, oy - (1.0 / 16) * yl * 0.92 - 16, "比 1", FT, GRAY, "lm")
    ctext(d, ox + xl - 8, oy - yl * 0.92 + 14, "比 16", FT, RED, "rm")
    ctext(d, ox + 0.20 * xl, oy - 0.55 * yl, "sigma = 5.67e-8 W/(m2 K4)", FT, GRAY, "lm")
    note(d, "温度2倍でふく射能は 2^4=16 倍. 高温場ではふく射熱移動が支配的になる")
    save(im, "t1f18StefanBoltzmann")


# 18-18 t1f18BeerLaw : ガスふく射のベール則 I(x)/I(0)=exp(-kappa x)
def beer_law():
    im, d = new(); title(d, "ベールの法則  I(x)/I(0) = exp(-kappa x)")
    gx0, gx1, gy0, gy1 = 180, 480, 115, 240
    d.rectangle((gx0, gy0, gx1, gy1), outline=BLACK, width=2, fill=(238, 242, 248))
    ctext(d, (gx0 + gx1) / 2, gy0 - 14, "ガス層 (CO2 / H2O)", FT, GRAY)
    dim(d, gx0, gy1 + 20, gx1, gy1 + 20, "厚さ x", col=GRAY)
    arrow(d, 85, 178, gx0, 178, RED, 4, 14); ctext(d, 120, 158, "I(0)", FT, RED)
    arrow(d, gx1, 178, 600, 178, RED, 2, 12); ctext(d, 565, 158, "I(x)", FT, RED)
    ox, oy, xl, yl = gx0, 385, gx1 - gx0, 110
    pts = []
    for i in range(0, 201):
        t = i / 200
        val = math.exp(-2.3 * t)
        pts.append((ox + t * xl, oy - val * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    d.line((ox, oy, ox + xl, oy), fill=BLACK, width=1)
    ctext(d, ox + xl * 0.5, oy - 0.72 * yl, "exp(-kappa x) 減衰", FT, BLUE, "lm")
    ctext(d, ox - 6, oy - yl, "強度", FT, GRAY, "rm")
    note(d, "層が厚いほど, 吸収係数 kappa が大きいほど強度は指数的に弱まる")
    save(im, "t1f18BeerLaw")


# 18-19 t1f18GasRadiation : ガスふく射の選択吸収性・双極子モーメント
def gas_radiation():
    im, d = new(); title(d, "ガスふく射: 双極子モーメントを持つ分子だけが吸収放射")
    # 左: 吸収放射する分子(CO2, H2O)
    box(d, 45, 90, 320, 360, (225, 245, 230))
    ctext(d, 182, 114, "CO2 / H2O", FS, GREEN)
    ctext(d, 182, 144, "双極子モーメント あり", FT, GRAY)
    pcircle(d, 182, 200, 26, (235, 245, 230), GREEN, 2); ctext(d, 182, 200, "分子", FT, GREEN)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        x2 = 182 + 52 * math.cos(rad); y2 = 200 + 52 * math.sin(rad)
        arrow(d, 182 + 28 * math.cos(rad), 200 + 28 * math.sin(rad), x2, y2, ORANGE, 2, 9)
    ctext(d, 182, 300, "特定波長で強く", FT, GREEN)
    ctext(d, 182, 328, "吸収・放射する", FT, GREEN)
    # 右: 吸収放射しない分子(N2, O2)
    box(d, 340, 90, 615, 360, (240, 240, 240))
    ctext(d, 477, 114, "N2 / O2 (He,Ar)", FS, GRAY)
    ctext(d, 477, 144, "双極子モーメント なし", FT, GRAY)
    pcircle(d, 477, 200, 26, FILL2, GRAY, 2); ctext(d, 477, 200, "分子", FT, GRAY)
    d.line((452, 255, 502, 305), fill=RED, width=3)
    d.line((502, 255, 452, 305), fill=RED, width=3)
    ctext(d, 477, 330, "ほとんど吸収放射しない", FT, RED)
    note(d, "選択吸収性: 燃焼ガスの CO2・H2O がふく射熱移動の主役(キルヒホッフ則も成立)")
    save(im, "t1f18GasRadiation")


# 18-20 t1f18SurfaceReaction : 表面反応と活性点バランス
def surface_reaction():
    im, d = new(); title(d, "表面反応: 活性点(サイト s)の数も保存する")
    def surface(x0, x1, y, occ):
        d.line((x0, y, x1, y), fill=BLACK, width=3)
        for i in range(6):
            xx = x0 + (x1 - x0) * (i + 0.5) / 6
            d.line((xx, y, xx, y + 10), fill=BLACK, width=2)
        n = len(occ)
        for i, item in enumerate(occ):
            sx = x0 + (x1 - x0) * (i + 0.5) / n
            node(d, sx, y - 6, 6, fill="white")
            if item is not None:
                lab, col = item
                pcircle(d, sx, y - 34, 16, (235, 242, 250), col, 2)
                ctext(d, sx, y - 34, lab, FT, col)
            else:
                ctext(d, sx, y - 32, "空 s", FT, GRAY)
    ctext(d, 165, 95, "反応前", FS, BLACK)
    surface(55, 320, 250, [("CO", BLUE), ("O", GREEN), None])
    ctext(d, 188, 288, "CO(s)+O(s) : 活性点 2 占有", FT, GRAY)
    arrow(d, 330, 205, 400, 205, BLACK, 3, 13); ctext(d, 365, 184, "反応", FT, GRAY)
    ctext(d, 505, 95, "反応後", FS, BLACK)
    surface(410, 620, 250, [("CO2", RED), None, None])
    ctext(d, 515, 288, "CO2(s) + 空きサイト s", FT, GRAY)
    box(d, 60, 330, 600, 388, FILL1, 2)
    ctext(d, 330, 358, "CO(s) + O(s) <-> CO2(s) + s   (右辺に s を補い活性点2=2)", FT, BLACK)
    note(d, "質量だけでなく活性点の数も左右で等しくする. s を付け忘れない")
    save(im, "t1f18SurfaceReaction")


# 18-21 t1f18Adsorption : 物理吸着と化学吸着・脱離
def adsorption():
    im, d = new(); title(d, "吸着(物理吸着 と 化学吸着)と脱離")
    box(d, 45, 90, 320, 360, (225, 235, 250))
    ctext(d, 182, 114, "物理吸着", FS, BLUE)
    d.line((70, 250, 295, 250), fill=BLACK, width=3)
    for i in range(5):
        xx = 80 + i * 50
        d.line((xx, 250, xx, 258), fill=BLACK, width=2)
    pcircle(d, 182, 200, 18, (235, 242, 250), BLUE, 2); ctext(d, 182, 200, "分子", FT, BLUE)
    dashed(d, 182, 218, 182, 248, GRAY, 2, 5, 4)
    ctext(d, 182, 288, "van der Waals 力", FT, GRAY)
    ctext(d, 182, 316, "弱い / 電子共有なし", FT, RED)
    box(d, 340, 90, 615, 360, (225, 245, 230))
    ctext(d, 477, 114, "化学吸着", FS, GREEN)
    d.line((365, 250, 590, 250), fill=BLACK, width=3)
    for i in range(5):
        xx = 375 + i * 50
        d.line((xx, 250, xx, 258), fill=BLACK, width=2)
    pcircle(d, 477, 205, 18, (235, 245, 230), GREEN, 2); ctext(d, 477, 205, "分子", FT, GREEN)
    d.line((477, 223, 477, 250), fill=GREEN, width=4)
    ctext(d, 477, 288, "化学結合を形成", FT, GRAY)
    ctext(d, 477, 316, "強い / 電子共有あり", FT, GREEN)
    # 脱離の矢印
    arrow(d, 300, 175, 360, 175, GRAY, 2, 11)
    ctext(d, 330, 156, "吸着", FT, GRAY)
    arrow(d, 360, 138, 300, 138, GRAY, 2, 11)
    ctext(d, 330, 122, "脱離", FT, GRAY)
    note(d, "強弱に注意: 物理吸着は弱く, 化学吸着のほうが強い. 生成物は脱離して離れる")
    save(im, "t1f18Adsorption")


# ============================================================
if __name__ == "__main__":
    activation_energy()       # 18-1
    arrhenius()               # 18-2
    arrhenius_plot()          # 18-3
    modified_arrhenius()      # 18-4
    kp()                      # 18-5
    kc()                      # 18-6
    kp_kc_relation()          # 18-7
    reaction_heat()           # 18-8
    hess_law()                # 18-9
    std_enthalpy()            # 18-10
    gibbs_formation()         # 18-11
    deltag_equilibrium()      # 18-12
    entropy()                 # 18-13
    exergy()                  # 18-14
    diffusion()               # 18-15
    viscosity()               # 18-16
    stefan_boltzmann()        # 18-17
    beer_law()                # 18-18
    gas_radiation()           # 18-19
    surface_reaction()        # 18-20
    adsorption()              # 18-21
    print("done t1f ch18")
