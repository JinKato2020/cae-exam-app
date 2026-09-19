# -*- coding: utf-8 -*-
"""熱流体力学1級 第18章「燃焼の基礎2」の問題図(t1e18*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(sigma, Delta, kappa, propto, <=, CO2, H2O, T^4, 1/T 等)。
required図(回答前)は答えの数値・結論を直接は書かない構図にする。"""
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
# ============  問題図  t1e18*  (14)  ========================
# ============================================================

# 18-1 t1e18ActivationEnergyCurve : 正反応の活性化エネルギー(required)
def activation_energy_curve():
    im, d = new(); title(d, "反応過程に沿ったポテンシャルエネルギー")
    ox, oy, xl, yl = 90, 360, 500, 280
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "反応過程", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 14, "ポテンシャルエネルギー", FT, BLACK, "rm")
    # レベル値をピクセル高さへ(120,350,80 kJ/mol)。最大350を上端付近へ。
    def yE(E): return oy - (E / 400.0) * yl
    y_r, y_t, y_p = yE(120), yE(350), yE(80)
    x_r, x_t, x_p = ox + 0.14 * xl, ox + 0.5 * xl, ox + 0.86 * xl
    # 反応物レベルの平坦部
    d.line((ox + 0.02 * xl, y_r, x_r, y_r), fill=BLUE, width=3)
    # 反応物 -> 遷移状態(山を登る)-> 生成物(降りる) をなめらかな曲線で
    pts = []
    for i in range(0, 101):
        t = i / 100
        # x を x_r..x_p へ, y を余弦の山でつなぐ
        x = x_r + (x_p - x_r) * t
        if t <= 0.5:
            s = t / 0.5
            y = y_r + (y_t - y_r) * (0.5 - 0.5 * math.cos(math.pi * s))
        else:
            s = (t - 0.5) / 0.5
            y = y_t + (y_p - y_t) * (0.5 - 0.5 * math.cos(math.pi * s))
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 生成物レベルの平坦部
    d.line((x_p, y_p, ox + 0.97 * xl, y_p), fill=BLUE, width=3)
    # 各レベルの補助破線と値のみ記入(Ea等の矢印ラベルは付けない)
    for (yy, xx, lab, al) in [(y_r, x_r, "A+B : 120 kJ/mol", "rm"),
                              (y_t, x_t, "(AB)* : 350 kJ/mol", "mm"),
                              (y_p, x_p, "C+D : 80 kJ/mol", "lm")]:
        dashed(d, ox, yy, xx, yy, GRAY, 1, 6, 5)
    ctext(d, x_r, y_r + 20, "A+B", FT, BLUE)
    ctext(d, x_t, y_t - 18, "(AB)*", FT, BLUE)
    ctext(d, x_p, y_p + 20, "C+D", FT, BLUE)
    ctext(d, ox + 6, y_r - 16, "120", FT, GRAY, "lm")
    ctext(d, x_t + 8, y_t, "350", FT, GRAY, "lm")
    ctext(d, ox + 0.97 * xl + 6, y_p, "80", FT, GRAY, "lm")
    note(d, "反応物・遷移状態・生成物の各レベル(kJ/mol)から活性化エネルギーを読む")
    save(im, "t1e18ActivationEnergyCurve")


# 18-2 t1e18MoleBalance : 圧力に依存しない平衡組成(helpful)
def mole_balance():
    im, d = new(); title(d, "反応前後のモル数の釣り合い(Delta nu = 0 なら圧力無依存)")
    rows = [
        ("2H2 + O2 <-> 2H2O", 3, 2),
        ("N2 + 3H2 <-> 2NH3", 4, 2),
        ("CO + H2O <-> CO2 + H2", 2, 2),
        ("2SO2 + O2 <-> 2SO3", 3, 2),
    ]
    y0 = 95
    for i, (eq, nl, nr) in enumerate(rows):
        cy = y0 + i * 78
        ctext(d, 40, cy, eq, FT, BLACK, "lm")
        # 天秤: 支点 px, 左右のモル数を高さで表現
        px = 430
        fulcy = cy + 28
        # 傾き: 多い側が下がる
        tilt = 0.0
        if nl > nr: tilt = 12
        elif nl < nr: tilt = -12
        lx, rx = px - 90, px + 90
        ly, ry = fulcy - 6 + tilt, fulcy - 6 - tilt
        d.line((lx, ly, rx, ry), fill=BLACK, width=3)     # 梁
        d.line((px, fulcy - 6, px, fulcy + 22), fill=BLACK, width=3)  # 支柱
        d.polygon((px - 10, fulcy + 22, px + 10, fulcy + 22, px, fulcy + 6),
                  outline=BLACK, width=2, fill=FILL1)      # 支点
        # 皿(左=反応側, 右=生成側)モル数を丸の数で
        for k in range(nl):
            pcircle(d, lx - 10 + (k % 3) * 16, ly - 14 - (k // 3) * 15, 6, FILL2)
        for k in range(nr):
            pcircle(d, rx - 10 + (k % 3) * 16, ry - 14 - (k // 3) * 15, 6, (235, 242, 250), BLUE, 2)
        ctext(d, lx, ly + 16, "反応 %d" % nl, FT, GRAY)
        ctext(d, rx, ry + 16, "生成 %d" % nr, FT, GRAY)
        if nl == nr:
            ctext(d, 620, cy, "釣合(Delta nu=0)", FT, GREEN, "rm")
        else:
            ctext(d, 620, cy, "傾く(Delta nu!=0)", FT, RED, "rm")
    note(d, "左右のモル数が等しい反応だけ全圧を変えても平衡がずれない")
    save(im, "t1e18MoleBalance")


# 18-3 t1e18ArrheniusPlot : アレニウスプロット(required・k値やEは書かない)
def arrhenius_plot():
    im, d = new(); title(d, "アレニウスプロット  ln k 対 1/T")
    ox, oy, xl, yl = 120, 350, 440, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "1/T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "ln k", FS, BLACK, "rm")
    # 右下がり直線: 小さい 1/T(高温)で ln k 大, 大きい 1/T(低温)で ln k 小
    x1p, x2p = ox + 0.25 * xl, ox + 0.75 * xl   # 1/T の2点(左=1/1000, 右=1/800)
    y1p, y2p = oy - 0.80 * yl, oy - 0.30 * yl    # 対応する ln k(高温ほど上)
    d.line((ox + 0.10 * xl, oy - 0.95 * yl, ox + 0.90 * xl, oy - 0.15 * yl), fill=BLUE, width=3)
    # 二点を軸上に目盛る(1/800, 1/1000)
    for (xp, yp, lab) in [(x1p, y1p, "1/1000 K"), (x2p, y2p, "1/800 K")]:
        node(d, xp, yp, 5, fill=BLUE, col=BLUE)
        dashed(d, xp, oy, xp, yp, GRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, GRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, GRAY)
    # 傾きの注記
    ctext(d, ox + 0.62 * xl, oy - 0.72 * yl, "傾き = -E / R0", FT, RED, "lm")
    # 傾き三角形
    tx0, ty0 = ox + 0.45 * xl, oy - 0.55 * yl
    tx1, ty1 = ox + 0.62 * xl, oy - 0.55 * yl
    ty2 = oy - 0.38 * yl
    dashed(d, tx0, ty0, tx1, ty1, GRAY, 1, 5, 4)
    dashed(d, tx1, ty1, tx1, ty2, GRAY, 1, 5, 4)
    note(d, "2点の傾き -E/R0 から活性化エネルギーを求める(k値・答えは各自)")
    save(im, "t1e18ArrheniusPlot")


# 18-4 t1e18RateEquilibrium : 平衡定数と反応速度定数(helpful)
def rate_equilibrium():
    im, d = new(); title(d, "正反応(kf)と逆反応(kb)の釣り合いと平衡")
    # 反応物側・生成物側の箱
    box(d, 60, 150, 250, 250, (225, 235, 250))
    ctext(d, 155, 185, "反応物", FS, BLUE); ctext(d, 155, 218, "aA + bB", FT, BLUE)
    box(d, 410, 150, 600, 250, (225, 245, 230))
    ctext(d, 505, 185, "生成物", FS, GREEN); ctext(d, 505, 218, "cC + dD", FT, GREEN)
    # 正反応(上向き矢印)kf, 逆反応(下向き)kb
    arrow(d, 255, 178, 405, 178, RED, 3, 13)
    ctext(d, 330, 158, "正反応 速度定数 kf", FT, RED)
    arrow(d, 405, 222, 255, 222, BLUE, 3, 13)
    ctext(d, 330, 242, "逆反応 速度定数 kb", FT, BLUE)
    # 平衡条件
    box(d, 120, 300, 540, 372, FILL2)
    ctext(d, 330, 322, "平衡: 正反応速度 = 逆反応速度  ->  qnet = 0", FT)
    ctext(d, 330, 352, "kf [A]^a [B]^b = kb [C]^c [D]^d", FS, BLACK)
    note(d, "平衡では両向きの速度が等しく, 濃度比が速度定数の比で定まる")
    save(im, "t1e18RateEquilibrium")


# 18-5 t1e18ReactionHeatLevels : 反応熱のエネルギー準位(helpful)
def reaction_heat_levels():
    im, d = new(); title(d, "反応物と生成物のエンタルピー準位(メタン燃焼)")
    ox, oy, xl, yl = 90, 360, 500, 280
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "反応進行", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "エンタルピー H", FT, BLACK, "rm")
    # 反応物 -75, 生成物 -878(相対)。基準線を上に置き, 発熱で下向き。
    y_r = oy - 0.78 * yl        # 反応物(高い)
    y_p = oy - 0.20 * yl        # 生成物(低い)
    x_rL, x_rR = ox + 0.08 * xl, ox + 0.38 * xl
    x_pL, x_pR = ox + 0.58 * xl, ox + 0.90 * xl
    d.line((x_rL, y_r, x_rR, y_r), fill=BLUE, width=4)
    ctext(d, (x_rL + x_rR) / 2, y_r - 20, "CH4 + 2O2", FT, BLUE)
    ctext(d, (x_rL + x_rR) / 2, y_r + 18, "(反応物)", FT, GRAY)
    d.line((x_pL, y_p, x_pR, y_p), fill=GREEN, width=4)
    ctext(d, (x_pL + x_pR) / 2, y_p - 20, "CO2 + 2H2O", FT, GREEN)
    ctext(d, (x_pL + x_pR) / 2, y_p + 18, "(生成物)", FT, GRAY)
    # 反応熱 ΔH(発熱で下向き)
    xm = ox + 0.48 * xl
    dashed(d, x_rR, y_r, xm, y_r, GRAY, 1, 6, 5)
    dashed(d, x_pL, y_p, xm, y_p, GRAY, 1, 6, 5)
    arrow(d, xm, y_r, xm, y_p, RED, 3, 13)
    ctext(d, xm + 12, (y_r + y_p) / 2, "Delta H_rxn < 0 (発熱)", FT, RED, "lm")
    note(d, "生成物が反応物より低い = 発熱. 差が反応熱(数値は各自)")
    save(im, "t1e18ReactionHeatLevels")


# 18-6 t1e18GibbsFormation : 標準生成ギブス自由エネルギー(helpful)
def gibbs_formation():
    im, d = new(); title(d, "標準生成ギブス自由エネルギー: 単体は 0, 化合物は非0")
    ox, oy, xl, yl = 90, 250, 500, 150
    # 基準線 ΔGf=0
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "物質", FS, BLACK, "lm")
    arrow(d, ox, oy + 90, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "Delta Gf", FT, BLACK, "rm")
    d.line((ox, oy, ox + xl, oy), fill=BLACK, width=2)
    ctext(d, ox + xl + 4, oy - 14, "基準線 Delta Gf = 0", FT, GRAY, "lm")
    # 単体3本(0)・化合物1本(負)
    items = [("O2", 0), ("N2", 0), ("C(黒鉛)", 0), ("H2O", -1)]
    bw = 50
    for i, (lab, v) in enumerate(items):
        cx = ox + 0.14 * xl + i * 0.22 * xl
        if v == 0:
            d.rectangle((cx - bw / 2, oy - 4, cx + bw / 2, oy), outline=BLACK, width=2, fill=FILL2)
            ctext(d, cx, oy + 22, lab, FT, GRAY)
            ctext(d, cx, oy - 18, "0 (単体)", FT, GREEN)
        else:
            yb = oy + 0.70 * yl
            d.rectangle((cx - bw / 2, oy, cx + bw / 2, yb), outline=BLACK, width=2, fill=(250, 230, 230))
            ctext(d, cx, yb + 22, lab, FT, RED)
            ctext(d, cx, (oy + yb) / 2, "非0", FT, RED)
            ctext(d, cx, yb + 44, "(化合物)", FT, GRAY)
    note(d, "安定な単体は定義により 0, 化合物(水)だけ基準線から離れる")
    save(im, "t1e18GibbsFormation")


# 18-7 t1e18EntropyProcess : エントロピーの正しい理解(helpful)
def entropy_process():
    im, d = new(); title(d, "断熱系のエントロピー変化(第二法則)")
    # 断熱系の枠
    box(d, 60, 90, 600, 360, "white", 2)
    # ハッチで断熱を表現
    for xx in range(60, 601, 26):
        d.line((xx, 90, xx + 14, 76), fill=LGRAY, width=1)
    ctext(d, 330, 108, "断熱された閉じた系", FT, GRAY)
    # 中央から3方向
    cx, cy = 200, 235
    node(d, cx, cy, 8, fill=FILL1)
    ctext(d, cx, cy + 26, "ある状態", FT, GRAY)
    # 可逆(S一定)
    arrow(d, cx + 20, cy - 40, 430, 150, GREEN, 3, 13)
    ctext(d, 470, 145, "可逆変化: S 一定", FT, GREEN, "lm")
    # 不可逆(S増大)
    arrow(d, cx + 20, cy, 430, 235, RED, 3, 13)
    ctext(d, 470, 232, "不可逆変化: S 増大", FT, RED, "lm")
    # S減少(禁止)
    arrow(d, cx + 20, cy + 40, 430, 320, GRAY, 3, 13)
    ctext(d, 470, 322, "S 減少", FT, GRAY, "lm")
    # ×印
    d.line((548, 305, 578, 335), fill=RED, width=4)
    d.line((578, 305, 548, 335), fill=RED, width=4)
    note(d, "断熱系では S は増大するか(可逆なら)一定. 減少は起こらない")
    save(im, "t1e18EntropyProcess")


# 18-8 t1e18ExergyGibbs : 等温燃焼のエクセルギー(helpful)
def exergy_gibbs():
    im, d = new(); title(d, "エンタルピー差の内訳: 有効分(エクセルギー)と無効分")
    # 全体バー = H0-H1
    bx0, bx1, by0, by1 = 90, 590, 150, 210
    total = bx1 - bx0
    # 有効分 E = G0-G1(大部分), 無効分 TΔS(小)。比 770:30
    xs = bx0 + total * (770.0 / 800.0)
    d.rectangle((bx0, by0, xs, by1), outline=BLACK, width=3, fill=(225, 245, 230))
    d.rectangle((xs, by0, bx1, by1), outline=BLACK, width=3, fill=(250, 230, 230))
    ctext(d, (bx0 + xs) / 2, (by0 + by1) / 2, "有効分 E = G0 - G1", FT, GREEN)
    ctext(d, (xs + bx1) / 2, by1 + 22, "無効分 T1(S0-S1)", FT, RED)
    # 全体幅の寸法
    dim(d, bx0, by0 - 24, bx1, by0 - 24, "エンタルピー差 H0 - H1", col=GRAY)
    # 区切り位置の縦破線
    dashed(d, xs, by0 - 6, xs, by1 + 40, GRAY, 1, 6, 5)
    # 説明
    box(d, 90, 270, 590, 350, FILL1)
    ctext(d, 340, 295, "E = (H0 - H1) - T1 (S0 - S1)", FS, BLACK)
    ctext(d, 340, 328, "取り出せる有効エネルギー = エンタルピー差 - 使えない分", FT, GRAY)
    note(d, "エクセルギーはエンタルピー差から T*Delta S を差し引いた有効分")
    save(im, "t1e18ExergyGibbs")


# 18-9 t1e18DiffusionPressure : 拡散係数の圧力依存性(helpful)
def diffusion_pressure():
    im, d = new(); title(d, "拡散係数の圧力依存性  D propto 1/p (温度一定)")
    ox, oy, xl, yl = 110, 330, 300, 220
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "圧力 p", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "拡散係数 D", FT, BLACK, "rm")
    # 反比例曲線
    pts = []
    for i in range(0, 201):
        t = 0.12 + (1.0 - 0.12) * i / 200
        val = 0.12 / t
        pts.append((ox + t * xl, oy - val * yl * 1.05))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.55 * xl, oy - 0.55 * yl, "D propto 1/p", FT, BLUE, "lm")
    # 右: 平均自由行程の対比(低圧=疎, 高圧=密)
    box(d, 440, 100, 620, 210, "white", 2)
    ctext(d, 530, 118, "低圧(疎)", FT, GRAY)
    for (px, py) in [(465, 150), (500, 175), (545, 145), (590, 180), (515, 195)]:
        pcircle(d, px, py, 6, FILL2)
    ctext(d, 530, 228, "平均自由行程 長い -> 拡散しやすい", FT, GRAY)
    box(d, 440, 260, 620, 370, "white", 2)
    ctext(d, 530, 278, "高圧(密)", FT, GRAY)
    for px in range(455, 616, 20):
        for py in range(300, 361, 20):
            pcircle(d, px, py, 5, FILL2)
    ctext(d, 530, 385, "行程 短い -> 拡散しにくい", FT, RED)
    note(d, "高圧ほど分子が密集し平均自由行程が短く, 拡散係数は小さくなる")
    save(im, "t1e18DiffusionPressure")


# 18-10 t1e18ViscosityTemp : 気体粘性係数の温度依存性(helpful)
def viscosity_temp():
    im, d = new(); title(d, "粘性係数の温度依存性: 気体と液体で逆")
    ox, oy, xl, yl = 110, 350, 460, 260
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "粘性係数 mu", FT, BLACK, "rm")
    # 気体: 右上がり sqrt(T)
    gpts = []
    for i in range(0, 201):
        t = i / 200
        val = 0.20 + 0.62 * math.sqrt(t)
        gpts.append((ox + t * xl, oy - val * yl))
    d.line(gpts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.72 * xl, oy - 0.82 * yl, "気体: mu propto sqrt(T) (右上がり)", FT, BLUE, "mm")
    # 液体: 右下がり
    lpts = []
    for i in range(0, 201):
        t = i / 200
        val = 0.85 * math.exp(-1.9 * t) + 0.06
        lpts.append((ox + t * xl, oy - val * yl))
    d.line(lpts, fill=RED, width=3, joint="curve")
    ctext(d, ox + 0.40 * xl, oy - 0.20 * yl, "液体: 右下がり", FT, RED, "lm")
    note(d, "気体は熱運動が主役で温度上昇とともに粘性増大(液体は逆に減少)")
    save(im, "t1e18ViscosityTemp")


# 18-11 t1e18StefanBoltzmann : ステファン-ボルツマン則(helpful)
def stefan_boltzmann():
    im, d = new(); title(d, "黒体ふく射能  Eb = sigma T^4 (4乗則)")
    ox, oy, xl, yl = 130, 350, 420, 260
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "絶対温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "黒体ふく射能 Eb", FT, BLACK, "rm")
    # T^4 曲線(T=2000で高さ1に規格化, T=1000は1/16)
    pts = []
    for i in range(0, 201):
        t = i / 200               # t=1 を T=2000 とする
        val = t ** 4
        pts.append((ox + t * xl, oy - val * yl * 0.92))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # T=1000(t=0.5, 高さ=1/16)と T=2000(t=1)を目盛る
    for (t, lab, hval) in [(0.5, "1000 K", (0.5) ** 4), (1.0, "2000 K", 1.0)]:
        xp = ox + t * xl
        yp = oy - hval * yl * 0.92
        node(d, xp, yp, 5, fill=BLUE, col=BLUE)
        dashed(d, xp, oy, xp, yp, GRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, GRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, GRAY)
    ctext(d, ox + 40, oy - (1.0 / 16) * yl * 0.92 - 16, "高さ比 1", FT, GRAY, "lm")
    ctext(d, ox + xl - 8, oy - yl * 0.92 + 14, "高さ比 16", FT, RED, "rm")
    note(d, "温度2倍でふく射能は 2^4 = 16 倍. 高温で急増する")
    save(im, "t1e18StefanBoltzmann")


# 18-12 t1e18GasRadiationBeer : ガスふく射のビール則(required)
def gas_radiation_beer():
    im, d = new(); title(d, "ガス層を通るふく射の減衰  I(x) = I(0) exp(-kappa x)")
    # ガス層(厚さx)
    gx0, gx1, gy0, gy1 = 180, 470, 120, 250
    d.rectangle((gx0, gy0, gx1, gy1), outline=BLACK, width=2, fill=(238, 242, 248))
    ctext(d, (gx0 + gx1) / 2, gy0 - 14, "ガス層(CO2・水蒸気)", FT, GRAY)
    dim(d, gx0, gy1 + 22, gx1, gy1 + 22, "層の厚さ x", col=GRAY)
    # 入射・透過
    arrow(d, 90, 185, gx0, 185, RED, 4, 14)
    ctext(d, 120, 165, "I(0)", FT, RED)
    arrow(d, gx1, 185, 590, 185, RED, 2, 12)
    ctext(d, 555, 165, "I(x)", FT, RED)
    # 減衰曲線(層内で指数的に弱まる)
    ox, oy, xl, yl = gx0, 380, gx1 - gx0, 110
    pts = []
    for i in range(0, 201):
        t = i / 200
        val = math.exp(-2.3 * t)
        pts.append((ox + t * xl, oy - val * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    d.line((ox, oy, ox + xl, oy), fill=BLACK, width=1)
    ctext(d, ox + xl * 0.55, oy - 0.75 * yl, "指数関数的に減衰", FT, BLUE, "lm")
    ctext(d, ox - 6, oy - yl, "強度", FT, GRAY, "rm")
    note(d, "層が厚いほど吸収が進みふく射強度が指数的に弱まる(kappa=吸収係数)")
    save(im, "t1e18GasRadiationBeer")


# 18-13 t1e18SurfaceReactionSites : 表面反応と活性点(required)
def surface_reaction_sites():
    im, d = new(); title(d, "触媒表面の活性点上での CO 酸化(反応前後)")
    # 反応前(左)
    def surface(x0, x1, y, occ):
        # 触媒表面(下地)と活性点を丸で。occ = リスト[(ラベル,色) or None]
        d.line((x0, y, x1, y), fill=BLACK, width=3)
        for i in range(6):
            xx = x0 + (x1 - x0) * (i + 0.5) / 6
            d.line((xx, y, xx, y + 10), fill=BLACK, width=2)
        n = len(occ)
        for i, item in enumerate(occ):
            sx = x0 + (x1 - x0) * (i + 0.5) / n
            node(d, sx, y - 6, 6, fill="white")   # 活性点 s
            if item is not None:
                lab, col = item
                pcircle(d, sx, y - 32, 15, (235, 242, 250), col, 2)
                ctext(d, sx, y - 32, lab, FT, col)
            else:
                ctext(d, sx, y - 30, "空 s", FT, GRAY)
    ctext(d, 165, 95, "反応前", FS, BLACK)
    surface(60, 320, 250, [("CO", BLUE), ("O", GREEN), None])
    ctext(d, 190, 285, "CO(s) + O(s)  (活性点 2 占有)", FT, GRAY)
    # 矢印
    arrow(d, 330, 210, 400, 210, BLACK, 3, 13)
    ctext(d, 365, 188, "反応", FT, GRAY)
    # 反応後(右)
    ctext(d, 500, 95, "反応後", FS, BLACK)
    surface(410, 620, 250, [("CO2", RED), None, None])
    ctext(d, 515, 285, "CO2(s) + 空き活性点  (活性点は保存)", FT, GRAY)
    note(d, "吸着種1つが活性点1つを占有. 反応前後で活性点の総数を数える")
    save(im, "t1e18SurfaceReactionSites")


# 18-14 t1e18Adsorption : 物理吸着と化学吸着の対比(helpful)
def adsorption():
    im, d = new(); title(d, "物理吸着 と 化学吸着 の対比")
    # 左: 物理吸着(弱い)
    box(d, 45, 95, 320, 360, (225, 235, 250))
    ctext(d, 182, 120, "物理吸着", FS, BLUE)
    # 表面と分子(離れている=弱い)
    d.line((70, 250, 295, 250), fill=BLACK, width=3)
    for i in range(5):
        xx = 80 + i * 50
        d.line((xx, 250, xx, 258), fill=BLACK, width=2)
    pcircle(d, 182, 205, 18, (235, 242, 250), BLUE, 2); ctext(d, 182, 205, "分子", FT, BLUE)
    dashed(d, 182, 223, 182, 248, GRAY, 2, 5, 4)   # 弱い相互作用=破線
    ctext(d, 182, 290, "van der Waals 力", FT, GRAY)
    ctext(d, 182, 318, "弱い / 電子共有なし", FT, RED)
    # 右: 化学吸着(強い)
    box(d, 340, 95, 615, 360, (225, 245, 230))
    ctext(d, 477, 120, "化学吸着", FS, GREEN)
    d.line((365, 250, 590, 250), fill=BLACK, width=3)
    for i in range(5):
        xx = 375 + i * 50
        d.line((xx, 250, xx, 258), fill=BLACK, width=2)
    pcircle(d, 477, 210, 18, (235, 245, 230), GREEN, 2); ctext(d, 477, 210, "分子", FT, GREEN)
    d.line((477, 228, 477, 250), fill=GREEN, width=4)   # 強い結合=太実線
    ctext(d, 477, 290, "化学結合を形成", FT, GRAY)
    ctext(d, 477, 318, "強い / 電子共有あり", FT, GREEN)
    note(d, "強弱の向きに注意: 化学吸着のほうが物理吸着より強い")
    save(im, "t1e18Adsorption")


# ============================================================
if __name__ == "__main__":
    activation_energy_curve()   # 18-1
    mole_balance()              # 18-2
    arrhenius_plot()            # 18-3
    rate_equilibrium()          # 18-4
    reaction_heat_levels()      # 18-5
    gibbs_formation()           # 18-6
    entropy_process()           # 18-7
    exergy_gibbs()              # 18-8
    diffusion_pressure()        # 18-9
    viscosity_temp()            # 18-10
    stefan_boltzmann()          # 18-11
    gas_radiation_beer()        # 18-12
    surface_reaction_sites()    # 18-13
    adsorption()                # 18-14
    print("done ch18")
