# -*- coding: utf-8 -*-
"""熱流体力学1級 第23章「混相燃焼」の公式・用語図(t1f23*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(rho, mu, sigma, Re_p, C_D, St, We, D32, Da, alpha, propto 等)。
※ 問題図 t1e23* とは別ファイル。上書きしない。"""
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


def dashed_circle(d, cx, cy, r, col=GRAY, wd=2, seg=64):
    prev = None
    for i in range(seg + 1):
        a = 2 * math.pi * i / seg
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if prev is not None and i % 2 == 0:
            d.line((prev[0], prev[1], p[0], p[1]), fill=col, width=wd)
        prev = p


def pcircle(d, x, y, r, fill=FILL1, col=BLACK, wd=2):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wd, fill=fill)


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


# ============================================================
# ============  公式・用語図  t1f23*  (13)  ==================
# ============================================================

# ch23-1 t1f23ParticleEOM : 粒子のラグランジュ型運動方程式と抗力
def particle_eom():
    im, d = new(); title(d, "粒子の運動方程式  m_p dV_p/dt = F + m_p g")
    # 気流(背景の流線矢印)
    for y in (120, 160):
        arrow(d, 70, y, 300, y, LGRAY, 2, 10)
    ctext(d, 120, 100, "気流 速度 V", FT, BLUE)
    # 粒子
    cx, cy, r = 330, 230, 40
    pcircle(d, cx, cy, r, (232, 240, 250), BLUE, 3)
    ctext(d, cx, cy, "粒子", FT, BLUE)
    ctext(d, cx, cy + r + 16, "直径 d_p, 速度 V_p", FT, GRAY)
    # 抗力 F(スリップ方向=気流向き)
    arrow(d, cx + r, cy - 10, cx + r + 90, cy - 10, RED, 4, 14)
    ctext(d, cx + r + 20, cy - 30, "抗力 F", FT, RED, "lm")
    # 重力
    arrow(d, cx, cy + r, cx, cy + r + 70, GREEN, 4, 14)
    ctext(d, cx + 8, cy + r + 50, "重力 m_p g", FT, GREEN, "lm")
    # スリップ速度
    arrow(d, cx - 100, cy - 70, cx - 30, cy - 70, BLUE, 3, 12)
    ctext(d, cx - 110, cy - 90, "スリップ速度 |V - V_p|", FT, BLUE, "lm")
    # 抗力式カード
    box(d, 55, 330, 605, 405, FILL1, 2)
    ctext(d, 330, 356, "F = (1/8) pi d_p^2 rho (V-V_p) |V-V_p| C_D", FS, BLACK)
    ctext(d, 330, 386, "投影面積 x 気体密度 x スリップ速度^2 x 抗力係数", FT, GRAY)
    note(d, "1個ずつ追跡(ラグランジュ). 抗力は気流と粒子の相対速度で決まる", y=318)
    save(im, "t1f23ParticleEOM")


# ch23-3 t1f23DragLaw : ストークス則と抗力係数
def drag_law():
    im, d = new(); title(d, "抗力係数 C_D と ストークス則 (Re_p による違い)")
    ox, oy, xl, yl = 110, 340, 470, 235
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "Re_p (対数)", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "C_D (対数)", FS, BLACK, "rm")
    # 低Re: ストークス則(傾き-1直線)
    d.line((ox + 0.05 * xl, oy - 0.88 * yl, ox + 0.50 * xl, oy - 0.36 * yl), fill=RED, width=3)
    ctext(d, ox + 0.08 * xl, oy - 0.84 * yl, "C_D = 24/Re_p (Re_p<<1)", FT, RED, "lm")
    # 補正域(Schiller-Naumann)頭打ち
    pts = []
    for i in range(0, 201):
        t = i / 200
        v = max(0.88 - 0.60 * t, 0.16 + 0.06 * math.exp(-6 * (t - 0.5)))
        pts.append((ox + (0.05 + 0.88 * t) * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.70 * xl, oy - 0.30 * yl, "補正式 (Re_p<=1000)", FT, BLUE, "lm")
    # 気泡 16/Re_p の注記
    ctext(d, ox + 0.42 * xl, oy - 0.72 * yl, "球形気泡は C_D=16/Re_p (別値)", FT, GRAY, "lm")
    box(d, 55, 372, 605, 408, "white", 1)
    ctext(d, 330, 390, "低Re: 24/Re_p / 中Re: 24/Re_p(1+0.15 Re_p^0.678) / 蒸発で抗力低下", FT, BLACK)
    note(d, "Re_p<<1でストークス則. Re_p増で補正が要る. 気泡は16/Re_pで混同注意", y=100)
    save(im, "t1f23DragLaw")


# ch23-4 t1f23Stokes : ストークス数と選択的移動
def stokes():
    im, d = new(); title(d, "ストークス数  St = tau_p / tau_f  と選択的移動")
    # 定義カード
    box(d, 150, 90, 510, 165, FILL1, 2)
    ctext(d, 330, 116, "St = tau_p / tau_f", FL, BLACK)
    ctext(d, 330, 150, "粒子応答時間 / 乱流時間スケール", FT, GRAY)
    # 3ケース
    ys = 260
    # St<<1 追従
    box(d, 55, 195, 250, 380, (235, 248, 238), 2)
    ctext(d, 152, 216, "St << 1", FS, GREEN)
    ctext(d, 152, 244, "流体によく追従", FT, GRAY)
    dashed_circle(d, 152, 300, 38, LGRAY, 1)
    for a in range(0, 360, 90):
        rad = math.radians(a)
        d.ellipse((152 + 20 * math.cos(rad) - 3, 300 + 20 * math.sin(rad) - 3,
                   152 + 20 * math.cos(rad) + 3, 300 + 20 * math.sin(rad) + 3), fill=BLUE)
    ctext(d, 152, 358, "偏析 弱い", FT, GREEN)
    # St~1 選択的移動
    box(d, 258, 195, 402, 380, (250, 236, 236), 2)
    ctext(d, 330, 216, "St ~ 1", FS, RED)
    ctext(d, 330, 244, "選択的移動", FT, RED)
    dashed_circle(d, 330, 300, 38, LGRAY, 1)
    # 中心=空隙、外周に粒子
    for a in range(0, 360, 60):
        rad = math.radians(a)
        d.ellipse((330 + 44 * math.cos(rad) - 3, 300 + 44 * math.sin(rad) - 3,
                   330 + 44 * math.cos(rad) + 3, 300 + 44 * math.sin(rad) + 3), fill=BLUE)
    arrow(d, 330, 300, 330 + 30, 300 - 18, RED, 2, 8)
    ctext(d, 330, 358, "渦中心=空隙", FT, RED)
    # St>>1 無関心
    box(d, 410, 195, 605, 380, (235, 240, 250), 2)
    ctext(d, 507, 216, "St >> 1", FS, BLUE)
    ctext(d, 507, 244, "乱流変動に無関心", FT, GRAY)
    dashed_circle(d, 507, 300, 38, LGRAY, 1)
    arrow(d, 460, 300, 555, 300, BLUE, 3, 11)
    ctext(d, 507, 358, "弾道的に直進", FT, BLUE)
    note(d, "St~1で渦度の強い領域から遠心力で弾き出され, 歪速度の強い帯に集まる(偏析最大)")
    save(im, "t1f23Stokes")


# ch23-7 t1f23Weber : ウェーバー数と分裂の臨界条件
def weber():
    im, d = new(); title(d, "ウェーバー数  We = rho(u_g-u_l)^2 d / sigma  と分裂条件")
    # 動圧と表面張力の競合模式
    cx, cy, r = 175, 210, 55
    d.ellipse((cx - r - 8, cy - r + 8, cx + r + 8, cy + r - 8), outline=BLUE, width=3, fill=(235, 242, 250))
    ctext(d, cx, cy, "液滴 d", FT, BLUE)
    # 動圧 P_D(潰す, 外から左右)
    arrow(d, cx - r - 60, cy, cx - r - 8, cy, RED, 4, 13)
    ctext(d, cx - r - 62, cy - 20, "P_D 動圧", FT, RED, "lm")
    # 表面張力 P_S(丸く保つ, 内向き)
    for a in (60, 120, 240, 300):
        rad = math.radians(a)
        arrow(d, cx + (r + 26) * math.cos(rad), cy + (r + 26) * math.sin(rad),
              cx + (r + 4) * math.cos(rad), cy + (r + 4) * math.sin(rad), GREEN, 2, 9)
    ctext(d, cx, cy - r - 24, "P_S 表面張力", FT, GREEN)
    # 式カード
    box(d, 55, 300, 605, 408, FILL1, 2)
    ctext(d, 330, 326, "P_D/P_S = (1/8) rho(u_g-u_l)^2 d / sigma = We/8", FS, BLACK)
    ctext(d, 330, 356, "分裂の目安 : P_D/P_S >= 1  すなわち  We >~ 8", FS, RED)
    ctext(d, 330, 386, "臨界We はオーネゾルゲ数 Oh が大きいほど高くなる", FT, GRAY)
    ctext(d, 430, 150, "We = 慣性(動圧) / 表面張力", FT, GRAY, "lm")
    note(d, "動圧が表面張力に打ち勝つ(We>~8)と液滴が分裂する", y=118)
    save(im, "t1f23Weber")


# ch23-10 t1f23BreakupModel : 噴霧分裂モデル(DDM/blob/WAVE)
def breakup_model():
    im, d = new(); title(d, "噴霧分裂モデル  DDM(parcel) / blob / WAVE")
    cy = 200
    # ノズル
    box(d, 55, cy - 26, 120, cy + 26, FILL1, 3)
    ctext(d, 87, cy - 44, "ノズル d0", FT, GRAY)
    # blob(初期径=ノズル径)
    pcircle(d, 160, cy, 26, (232, 240, 250), BLUE, 3)
    ctext(d, 160, cy + 44, "blob", FT, BLUE)
    ctext(d, 160, cy + 64, "初期径=ノズル径", FT, GRAY)
    arrow(d, 190, cy, 240, cy, GRAY, 3, 12)
    # 液柱の不安定波(WAVE)
    xs, xe = 245, 400
    top, bot = [], []
    for i in range(0, 81):
        t = i / 80; x = xs + (xe - xs) * t
        amp = 4 + 14 * t
        top.append((x, cy - 20 + amp * math.sin(2 * math.pi * 3 * t)))
        bot.append((x, cy + 20 - amp * math.sin(2 * math.pi * 3 * t)))
    d.line(top, fill=BLUE, width=3, joint="curve")
    d.line(bot, fill=BLUE, width=3, joint="curve")
    ctext(d, 320, cy - 54, "WAVE: 表面の不安定波", FT, RED)
    arrow(d, 405, cy, 450, cy, GRAY, 3, 12)
    # parcel 群
    import random
    random.seed(2)
    for _ in range(20):
        x = random.uniform(465, 600); y = random.uniform(cy - 50, cy + 50); rr = random.uniform(4, 9)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=BLUE, width=2, fill=(232, 240, 250))
    ctext(d, 530, cy + 66, "parcel 液滴群", FT, BLUE)
    # 説明カード
    box(d, 55, 300, 605, 408, FILL1, 2)
    ctext(d, 330, 324, "DDM : 多数の実液滴を代表液滴 parcel で表す", FT, BLACK)
    ctext(d, 330, 352, "blob : 初期粒径=ノズル径, 初期数=噴射流量から算出", FT, BLACK)
    ctext(d, 330, 380, "WAVE : 最も速く増幅する表面波で分裂を決める", FT, RED)
    note(d, "ディーゼル噴霧で広く使われる分裂モデル群", y=290)
    save(im, "t1f23BreakupModel")


# ch23-11 t1f23PsiCell : 分離流(SF)モデルとPSI-Cell
def psi_cell():
    im, d = new(); title(d, "分離流(SF)モデルと PSI-Cell  気液の双方向連成")
    # 気相(オイラー)
    box(d, 60, 100, 300, 250, (235, 240, 250), 2)
    ctext(d, 180, 124, "気相", FS, BLUE)
    ctext(d, 180, 152, "オイラー法", FT, GRAY)
    ctext(d, 180, 178, "支配方程式に", FT, GRAY)
    ctext(d, 180, 200, "生成項を加える", FT, GRAY)
    # 液滴(ラグランジュ)
    box(d, 360, 100, 600, 250, (235, 248, 238), 2)
    ctext(d, 480, 124, "液滴", FS, GREEN)
    ctext(d, 480, 152, "ラグランジュ法", FT, GRAY)
    ctext(d, 480, 178, "代表液滴(parcel)", FT, GRAY)
    ctext(d, 480, 200, "を1個ずつ追跡", FT, GRAY)
    # 双方向の交換
    arrow(d, 305, 155, 355, 155, RED, 4, 13)
    arrow(d, 355, 195, 305, 195, GREEN, 4, 13)
    ctext(d, 330, 262, "質量・運動量・熱の交換(PSI-Cell 生成項)", FT, RED)
    # 説明カード
    box(d, 55, 300, 605, 408, FILL1, 2)
    ctext(d, 330, 326, "DDM: 液滴をラグランジュ的に解き, 交換量を", FT, BLACK)
    ctext(d, 330, 354, "気相支配方程式の生成項(ソース項)に加える(双方向)", FT, BLACK)
    ctext(d, 330, 384, "計算量削減に確率密度関数(PDF)を用いる手法もある", FT, GRAY)
    note(d, "気相=オイラー, 液滴=ラグランジュ. 気液双方に交換項が現れる", y=290)
    save(im, "t1f23PsiCell")


# ch23-12 t1f23Dsquared : D^2乗則
def dsquared():
    im, d = new(); title(d, "D^2乗則  D^2(t) = D0^2 - K t  (準定常の蒸発・燃焼)")
    ox, oy, xl, yl = 120, 340, 450, 240
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "時間 t", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "D^2", FS, BLACK, "rm")
    # 直線 D^2 = D0^2 - K t
    x0, y0v = 0.02, 0.90
    x1, y1v = 0.82, 0.06
    d.line((ox + x0 * xl, oy - y0v * yl, ox + x1 * xl, oy - y1v * yl), fill=BLUE, width=3)
    node(d, ox + x0 * xl, oy - y0v * yl, 5, fill=BLUE, col=BLUE)
    ctext(d, ox + x0 * xl + 8, oy - y0v * yl - 12, "D0^2", FT, BLUE, "lm")
    # 傾き -K
    ctext(d, ox + 0.45 * xl, oy - 0.55 * yl, "傾き -K (蒸発定数)", FT, RED, "lm")
    # 寿命 t_life
    node(d, ox + x1 * xl, oy - y1v * yl, 5, fill=RED, col=RED)
    dashed(d, ox + x1 * xl, oy - y1v * yl, ox + x1 * xl, oy, LGRAY, 1, 6, 5)
    ctext(d, ox + x1 * xl, oy + 16, "t_life = D0^2 / K", FT, RED)
    box(d, 55, 366, 605, 408, "white", 1)
    ctext(d, 330, 388, "直径の2乗が時間の一次関数で減少. 表面積(D^2)が支配的に効く", FT, BLACK)
    note(d, "蒸発・燃焼では液滴径の2乗が直線的に減る. 寿命は D0^2/K で見積もる", y=100)
    save(im, "t1f23Dsquared")


# ch23-13 t1f23Sauter : ザウター平均粒径 D32
def sauter():
    im, d = new(); title(d, "ザウター平均粒径  D32 = sum(n_i D_i^3) / sum(n_i D_i^2)")
    # 左: 多分散
    box(d, 55, 95, 300, 300, "white", 2)
    ctext(d, 177, 116, "多分散な液滴群", FT, BLUE)
    specs = [(120, 165, 24), (200, 155, 15), (245, 210, 28), (135, 240, 18),
             (110, 275, 11), (210, 265, 20)]
    for x, y, rr in specs:
        pcircle(d, x, y, rr, (232, 240, 250), BLUE, 2)
    arrow(d, 305, 200, 350, 200, GRAY, 3, 12)
    # 右: 等価一様径 D32
    box(d, 355, 95, 605, 300, "white", 2)
    ctext(d, 480, 116, "等価な一様径 D32", FT, RED)
    idx = 0
    for gy in (165, 220, 275):
        for gx in (410, 460, 510, 560):
            if idx < 9:
                pcircle(d, gx, gy, 19, (250, 236, 236), RED, 2)
                idx += 1
    box(d, 55, 320, 605, 408, FILL1, 2)
    ctext(d, 330, 344, "全体積(D^3和)と全表面積(D^2和)を同時に一致させる代表径", FT, BLACK)
    ctext(d, 330, 374, "蒸発・燃焼は表面積が効くため 個数平均 D10 でなく D32 を使う", FT, RED)
    note(d, "D32 は個数平均径 D10 より大きく, 大径液滴に重みが寄る", y=310)
    save(im, "t1f23Sauter")


# ch23-15 t1f23Kelvin : Kelvinの式(微小液滴の蒸気圧)
def kelvin():
    im, d = new(); title(d, "Kelvinの式  ln(P/Ps) = 4 sigma M / (rho R T D)")
    ox, oy, xl, yl = 120, 330, 450, 220
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "液滴直径 D", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "P / Ps", FS, BLACK, "rm")
    # P/Ps=1 水準線
    y1 = oy - 0.16 * yl
    dashed(d, ox, y1, ox + xl, y1, GRAY, 1, 7, 5)
    ctext(d, ox + xl - 6, y1 - 12, "平面 (D->無限大) で P/Ps=1", FT, GRAY, "rm")
    # 1/D 依存の曲線
    pts = []
    for i in range(0, 201):
        t = 0.04 + (1.0 - 0.04) * i / 200
        v = min(0.16 + 0.030 / t, 0.94)
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.12 * xl, oy - 0.78 * yl, "微小液滴ほど P/Ps 大", FT, RED, "lm")
    box(d, 55, 358, 605, 408, "white", 1)
    ctext(d, 330, 383, "右辺が 1/D に比例 -> 径が小さいほど表面蒸気圧が高く 蒸発しやすい", FT, BLACK)
    note(d, "sigma:表面張力 M:分子量 rho:液密度 R:気体定数 T:絶対温度 D:直径", y=100)
    save(im, "t1f23Kelvin")


# ch23-16 t1f23BurnHistory : 単一油粒燃焼の3期間
def burn_history():
    im, d = new(); title(d, "単一油粒燃焼の3期間  A加熱 -> B蒸発 -> C燃焼")
    ox, oy, xl, yl = 110, 350, 470, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "時間 t", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "D^2", FS, BLACK, "rm")
    tA, tB, tend = 0.22, 0.60, 0.92
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    d.line((X(0.02), Y(0.86), X(tA), Y(0.80)), fill=BLUE, width=3)  # A加熱
    d.line((X(tA), Y(0.80), X(tB), Y(0.34)), fill=BLUE, width=3)    # B蒸発
    d.line((X(tB), Y(0.34), X(tend), Y(0.08)), fill=BLUE, width=3)  # C燃焼
    for t in (tA, tB):
        dashed(d, X(t), oy, X(t), oy - yl - 4, LGRAY, 1, 6, 5)
    ctext(d, X((0.02 + tA) / 2), oy - yl + 6, "A 加熱期間", FT, GRAY)
    ctext(d, X((tA + tB) / 2), oy - yl + 6, "B 蒸発期間", FT, GREEN)
    ctext(d, X((tB + tend) / 2), oy - yl + 6, "C 燃焼期間", FT, RED)
    node(d, X(tA), oy, 5, fill=ORANGE, col=ORANGE); ctext(d, X(tA), oy + 16, "t1 自然着火", FT, ORANGE)
    node(d, X(tend), Y(0.08), 5, fill=RED, col=RED); ctext(d, X(tend), oy + 16, "t2 燃えつき", FT, RED)
    # 着火遅れ(A+B)
    dashed(d, X(0.02), oy - yl - 20, X(tB), oy - yl - 20, RED, 1, 6, 5)
    ctext(d, X((0.02 + tB) / 2), oy - yl - 30, "着火遅れ = A + B", FT, RED)
    note(d, "加熱で温度上昇 -> 蒸発(t1で着火) -> 燃焼(t2で燃えつき)")
    save(im, "t1f23BurnHistory")


# ch23-18 t1f23GroupNumber : 群燃焼数 G と燃焼形態
def group_number():
    im, d = new(); title(d, "群燃焼数 G  = 総蒸発率 / ガス成分交換率")
    labels = ["単一液滴燃焼", "内部群燃焼", "外部群燃焼", "外殻燃焼"]
    cxs = [130, 300, 460, 590]
    cy = 200
    R = 48
    import random
    for k, (cx, lab) in enumerate(zip(cxs, labels)):
        random.seed(30 + k)
        drops = []
        for _ in range(8):
            a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, R * 0.78)
            drops.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        dashed_circle(d, cx, cy, R, LGRAY, 1)
        for (x, y) in drops:
            d.ellipse((x - 3, y - 3, x + 3, y + 3), outline=BLUE, width=1, fill=BLUE)
        if k == 0:
            for (x, y) in drops:
                dashed_circle(d, x, y, 8, RED, 1)
        elif k == 1:
            dashed_circle(d, cx, cy, R * 0.5, RED, 2)
        elif k == 2:
            dashed_circle(d, cx, cy, R * 0.85, RED, 2)
        else:
            dashed_circle(d, cx, cy, R + 6, RED, 3)
        ctext(d, cx, cy + R + 22, lab, FT, BLACK)
    arrow(d, 90, 300, 600, 300, GRAY, 2, 11)
    ctext(d, 345, 316, "G 小 ------------------------> G 大", FT, GRAY)
    box(d, 55, 335, 605, 408, FILL1, 2)
    ctext(d, 330, 358, "G は 平均液滴間距離と負の相関, 液滴径と正の相関", FT, BLACK)
    ctext(d, 330, 386, "G 小=個々に燃焼 / G 大=外殻に火炎が偏る(赤破線=火炎)", FT, RED)
    save(im, "t1f23GroupNumber")


# ch23-19 t1f23Proximate : 石炭の工業分析と元素分析
def proximate():
    im, d = new(); title(d, "石炭の工業分析(4成分)と元素分析")
    # 左: 工業分析(積み上げ棒)
    bx0, bx1, top, bot = 120, 240, 110, 360
    total = bot - top
    segs = [("水分", 0.10, (210, 225, 245)),
            ("揮発分", 0.28, (250, 236, 210)),
            ("固定炭素", 0.52, (215, 215, 215)),
            ("灰分", 0.10, (235, 235, 235))]
    y = top; seg_y = {}
    for lab, frac, col in segs:
        h = total * frac
        d.rectangle((bx0, y, bx1, y + h), outline=BLACK, width=2, fill=col)
        ctext(d, (bx0 + bx1) / 2, y + h / 2, lab, FT, BLACK)
        seg_y[lab] = (y, y + h); y += h
    ctext(d, (bx0 + bx1) / 2, top - 16, "工業分析", FT, BLUE)
    # 可燃分/不燃分 区分
    vt = seg_y["揮発分"][0]; fcb = seg_y["固定炭素"][1]
    d.line((bx1 + 12, vt, bx1 + 12, fcb), fill=GREEN, width=3)
    ctext(d, bx1 + 16, (vt + fcb) / 2, "可燃分", FT, GREEN, "lm")
    # 右: 元素分析
    box(d, 360, 130, 600, 340, "white", 2)
    ctext(d, 480, 152, "元素分析", FT, RED)
    elems = ["C 炭素", "H 水素", "N 窒素", "O 酸素", "S 硫黄", "灰分"]
    for i, e in enumerate(elems):
        ctext(d, 480, 182 + i * 26, e, FT, BLACK)
    arrow(d, 250, 235, 355, 235, GRAY, 3, 12)
    note(d, "工業分析=不燃分(水分・灰分)と可燃分(揮発分・固定炭素). 元素分析はC/H/N/O/S+灰分")
    save(im, "t1f23Proximate")


# ch23-21 t1f23CoalReaction : 微粉炭燃焼の反応過程
def coal_reaction():
    im, d = new(); title(d, "微粉炭の反応過程  揮発分放出(速い) + チャー燃焼(遅い)")
    cy = 190
    # 1 加熱
    cx = 120
    pcircle(d, cx, cy, 30, (60, 60, 60), BLACK, 2)
    ctext(d, cx, cy + 52, "石炭粒子", FT, GRAY)
    ctext(d, cx, cy - 48, "加熱", FT, ORANGE)
    arrow(d, cx + 48, cy, cx + 92, cy, GRAY, 3, 12)
    # 2 揮発分放出(気相火炎)
    cx = 310
    pcircle(d, cx, cy, 24, (80, 80, 80), BLACK, 2)
    dashed_circle(d, cx, cy, 52, RED, 2)
    for a in range(0, 360, 60):
        rad = math.radians(a)
        arrow(d, cx + 26 * math.cos(rad), cy + 26 * math.sin(rad),
              cx + 48 * math.cos(rad), cy + 48 * math.sin(rad), GREEN, 2, 8)
    ctext(d, cx, cy + 74, "揮発分放出+気相燃焼", FT, GREEN)
    ctext(d, cx, cy - 66, "低分子HC・CO・H2 (速い)", FT, GRAY)
    arrow(d, cx + 66, cy, cx + 108, cy, GRAY, 3, 12)
    # 3 チャー燃焼
    cx = 520
    pcircle(d, cx, cy, 30, (150, 150, 150), BLACK, 2)
    for (dxp, dyp) in [(-10, -6), (8, -10), (-6, 8), (10, 6), (0, 0)]:
        d.ellipse((cx + dxp - 4, cy + dyp - 4, cx + dxp + 4, cy + dyp + 4), outline=BLACK, width=1)
    for a in range(0, 360, 60):
        rad = math.radians(a)
        arrow(d, cx + 48 * math.cos(rad), cy + 48 * math.sin(rad),
              cx + 34 * math.cos(rad), cy + 34 * math.sin(rad), RED, 2, 8)
    ctext(d, cx, cy + 74, "チャー表面燃焼", FT, RED)
    ctext(d, cx, cy - 48, "多孔質固体 (遅い)", FT, GRAY)
    # 時間軸+スケール
    arrow(d, 90, 320, 600, 320, GRAY, 2, 11)
    ctext(d, 200, 338, "揮発分 10-100 ms", FT, GREEN)
    ctext(d, 470, 338, "チャー 1 s 以上に及ぶ", FT, RED)
    box(d, 55, 360, 605, 408, "white", 1)
    ctext(d, 330, 385, "揮発分放出量: 石炭温度・加熱速度で増, 圧力・粒径で減. チャーはH 1-1.5%含む", FT, BLACK)
    save(im, "t1f23CoalReaction")


# ============================================================
if __name__ == "__main__":
    particle_eom()     # ch23-1
    drag_law()         # ch23-3
    stokes()           # ch23-4
    weber()            # ch23-7
    breakup_model()    # ch23-10
    psi_cell()         # ch23-11
    dsquared()         # ch23-12
    sauter()           # ch23-13
    kelvin()           # ch23-15
    burn_history()     # ch23-16
    group_number()     # ch23-18
    proximate()        # ch23-19
    coal_reaction()    # ch23-21
    print("done t1f ch23")
