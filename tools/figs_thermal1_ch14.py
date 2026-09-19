# -*- coding: utf-8 -*-
"""熱流体力学1級 第14章「粒子追跡モデル」の図(t1e14*・t1f14*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(tau_p, beta, rho_p, rho_f, nu, mu, Delta t, Omega, St, e, mu_f,
 v_n, v_t, J_n, J_t, W_1, W_2, N^2, u-v 等)。
required図(回答前)には答え・正解値・結論を描かない。"""
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


def dotline(d, x1, y1, x2, y2, col=GRAY, wd=2, dot=2, gap=7):
    dashed(d, x1, y1, x2, y2, col, wd, dot, gap)


def spin(d, cx, cy, r, col=GREEN, wd=3):
    """回転(角運動量)を表す円弧矢印。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), -30, 210, fill=col, width=wd)
    ax, ay = cx + r * math.cos(math.radians(-30)), cy - r * math.sin(math.radians(-30))
    arrow(d, ax + 6, ay + 10, ax, ay, col, wd, 10)


# ============================================================
# 14-1 t1e14MethodSelection : 粒子追跡法 vs 多流体モデル(helpful)
# ============================================================
def method_selection():
    im, d = new(); title(d, "粒子追跡法 と 多流体モデル の使い分け")
    box(d, 40, 90, 320, 350, FILL1)
    ctext(d, 180, 112, "粒子追跡法 (Euler-Lagrange)", FS, BLUE)
    for i, s in enumerate(["分散相を1個ずつ追う",
                           "粒径ばらつき/空間の偏りに強い",
                           "総数が大きいと",
                           "記憶容量・計算時間の制約"]):
        ctext(d, 180, 150 + i * 38, s, FT)
    # 個別粒子のイメージ
    for (px, py) in [(90, 320), (130, 328), (170, 316), (210, 330), (250, 320)]:
        pcircle(d, px, py, 7, FILL2)
    box(d, 340, 90, 620, 350, FILL2)
    ctext(d, 480, 112, "多流体モデル", FS, GREEN)
    for i, s in enumerate(["体積率・数密度など統計量で扱う",
                           "総数が増えても計算負荷は小",
                           "粒径/空間分布のばらつきが",
                           "大きいと精度が低下しうる"]):
        ctext(d, 480, 150 + i * 38, s, FT)
    # 連続的な濃度分布のイメージ
    for i in range(10):
        g = 210 - i * 8
        d.line((360 + i * 26, 322, 360 + i * 26, 336), fill=(g, g, g), width=6)
    note(d, "総数多い/分布が一様 -> 多流体, 総数少/ばらつき大 -> 粒子追跡")
    save(im, "t1e14MethodSelection")


# ============================================================
# 14-2 t1e14RelaxationTimeStability : tau_p ∝ a^2(helpful, 答え数値は書かない)
# ============================================================
def relaxation_time_stability():
    im, d = new(); title(d, "粒子緩和時間  tau_p = a^2(2beta+1)/(9nu)   tau_p ∝ a^2")
    # 大粒子
    pcircle(d, 150, 170, 46, FILL1); ctext(d, 150, 170, "a", F)
    ctext(d, 150, 232, "大きい粒子", FT, GRAY)
    d.rectangle((110, 260, 190, 300), outline=BLACK, width=2, fill=FILL2)
    ctext(d, 150, 280, "tau_p 長い", FT, BLUE)
    # 小粒子(半径を小さく)
    arrow(d, 220, 170, 300, 170, BLACK, 3, 12); ctext(d, 260, 150, "a を小さく", FT, GRAY)
    pcircle(d, 380, 170, 23, FILL1); ctext(d, 380, 170, "a/2", FS)
    ctext(d, 380, 232, "小さい粒子", FT, GRAY)
    d.rectangle((360, 288, 400, 300), outline=BLACK, width=2, fill=FILL2)
    ctext(d, 380, 274, "tau_p 短い", FT, BLUE)
    # 安定条件
    box(d, 440, 150, 630, 300, FILL1)
    ctext(d, 535, 175, "陽解法の安定条件", FS, RED)
    ctext(d, 535, 210, "Delta t < tau_p", F)
    ctext(d, 535, 250, "a を小さくするほど", FT)
    ctext(d, 535, 274, "条件はきびしくなる", FT, RED)
    note(d, "小さい粒子ほど緩和が速く(tau_p 小), 陽解法では非常に小さな Delta t が必要")
    save(im, "t1e14RelaxationTimeStability")


# ============================================================
# 14-3 t1e14TimeIntegration : 緩和方程式の時間積分(required・手法名は書かない)
# ============================================================
def time_integration():
    im, d = new(); title(d, "緩和方程式の時間積分  dv/dt = (u - v)/tau")
    ctext(d, W / 2, 78, "tau = 0.1 s,   Delta t = 1 s", FS, BLACK)
    box(d, 120, 100, 540, 150, FILL2)
    ctext(d, 330, 125, "v^(n+1) = (1 - Delta t/tau) v^n + (Delta t/tau) u", FS)
    # 増幅率の枠
    d.rectangle((175, 118, 315, 143), outline=RED, width=3)
    arrow(d, 245, 165, 245, 195, RED, 2, 10)
    ctext(d, 245, 210, "増幅率 G = (1 - Delta t/tau)", FT, RED)
    # 数直線: |G|<1 安定 / |G|>1 発散
    y = 300; x0, x1 = 90, 590; cx = (x0 + x1) / 2
    arrow(d, x0 - 5, y, x1 + 15, y, BLACK, 2, 11); ctext(d, x1 + 25, y, "G", FS, BLACK, "lm")
    for gx, lab in [(cx - 130, "-1"), (cx + 130, "+1")]:
        d.line((gx, y - 8, gx, y + 8), fill=BLACK, width=2); ctext(d, gx, y + 22, lab, FT, GRAY)
    d.line((cx, y - 6, cx, y + 6), fill=GRAY, width=1); ctext(d, cx, y + 22, "0", FT, GRAY)
    # 安定域 / 発散域
    d.line((cx - 130, y - 26, cx + 130, y - 26), fill=GREEN, width=4)
    ctext(d, cx, y - 40, "|G| < 1 : 安定", FT, GREEN)
    dashed(d, x0, y - 26, cx - 130, y - 26, RED, 4, 10, 6)
    dashed(d, cx + 130, y - 26, x1, y - 26, RED, 4, 10, 6)
    ctext(d, cx - 210, y - 40, "|G|>1 発散", FT, RED)
    ctext(d, cx + 210, y - 40, "|G|>1 発散", FT, RED)
    note(d, "増幅率の絶対値が1を超えると解は発散する(硬い問題では時間積分法の選択が要点)")
    save(im, "t1e14TimeIntegration")


# ============================================================
# 14-4 t1e14OneWayCoupling : 連成の3段階(helpful)
# ============================================================
def one_way_coupling():
    im, d = new(); title(d, "連成の段階  one-way / two-way / four-way")
    def fluid(cx): pcircle(d, cx, 150, 26, (225, 235, 250), BLUE, 3); ctext(d, cx, 150, "流体", FT, BLUE)
    def part(cx, cy=230): pcircle(d, cx, cy, 20, FILL1); ctext(d, cx, cy, "粒子", FT)
    # one-way
    cx = 140; fluid(cx); part(cx)
    arrow(d, cx, 178, cx, 208, BLACK, 3, 12)
    ctext(d, cx, 300, "one-way", FS, BLUE)
    ctext(d, cx, 324, "流体->粒子のみ", FT, GRAY)
    ctext(d, cx, 344, "希薄:流れを乱さない", FT, GRAY)
    # two-way
    cx = 330; fluid(cx); part(cx)
    arrow(d, cx - 6, 178, cx - 6, 208, BLACK, 3, 12)
    arrow(d, cx + 6, 208, cx + 6, 178, RED, 3, 12)
    ctext(d, cx, 300, "two-way", FS, GREEN)
    ctext(d, cx, 324, "流体<->粒子 双方向", FT, GRAY)
    ctext(d, cx, 344, "反作用も返す", FT, GRAY)
    # four-way
    cx = 520; fluid(cx); part(cx - 22, 235); part(cx + 22, 235)
    arrow(d, cx, 178, cx, 210, BLACK, 3, 12)
    arrow(d, cx - 8, 235, cx + 8 - 2, 235, ORANGE, 3, 11)
    arrow(d, cx + 8, 250, cx - 8 + 2, 250, ORANGE, 3, 11)
    ctext(d, cx, 300, "four-way", FS, ORANGE)
    ctext(d, cx, 324, "粒子<->粒子 衝突も", FT, GRAY)
    ctext(d, cx, 344, "濃密系", FT, GRAY)
    note(d, "希薄なほど片方向で足りる. 濃度が上がるほど高次の連成が必要")
    save(im, "t1e14OneWayCoupling")


# ============================================================
# 14-5 t1e14PsiCellCoupling : PSI-Cell法の前提(helpful)
# ============================================================
def psi_cell_coupling():
    im, d = new(); title(d, "PSI-Cell法: 粒子の反力をセルの体積力に加える")
    # 左: 適用可(粒子<セル, 後流がセル内)
    x0, y0 = 70, 110
    for i in range(3):
        for j in range(3):
            box(d, x0 + j * 70, y0 + i * 70, x0 + j * 70 + 70, y0 + i * 70 + 70, "white", 2)
    ccx, ccy = x0 + 105, y0 + 105
    pcircle(d, ccx, ccy, 12, FILL2)
    # 後流(速度欠損)がセル内に収まる
    for k in range(3):
        arrow(d, ccx + 14, ccy - 10 + k * 10, ccx + 44, ccy - 10 + k * 10, GRAY, 2, 8)
    d.ellipse((ccx + 12, ccy - 20, ccx + 56, ccy + 20), outline=GREEN, width=2)
    arrow(d, ccx, ccy + 40, ccx, ccy + 12, RED, 3, 11)
    ctext(d, ccx, ccy + 56, "反力=体積力", FT, RED)
    ctext(d, x0 + 105, y0 + 220, "粒子<<格子, 後流がセル内", FT, GREEN)
    ctext(d, x0 + 105, y0 + 244, "-> PSI-Cell 適用可", FT, GREEN)
    # 右: 不適(後流が隣接セルへはみ出す)
    x0 = 400
    for i in range(3):
        for j in range(3):
            box(d, x0 + j * 70, y0 + i * 70, x0 + j * 70 + 70, y0 + i * 70 + 70, "white", 2)
    ccx = x0 + 105
    pcircle(d, ccx, ccy, 12, FILL2)
    d.ellipse((ccx - 60, ccy - 30, ccx + 70, ccy + 30), outline=RED, width=2)
    ctext(d, x0 + 105, y0 + 220, "後流が隣接セルへ拡大", FT, RED)
    ctext(d, x0 + 105, y0 + 244, "-> 1セルで表せず不適", FT, RED)
    note(d, "前提: 粒子が格子より十分小さく, 後流の速度欠損がそのセル内に収まること")
    save(im, "t1e14PsiCellCoupling")


# ============================================================
# 14-6 t1e14SphMpsDem : SPH/MPS/DEMの分類(helpful)
# ============================================================
def sph_mps_dem():
    im, d = new(); title(d, "粒子法の分類: 計算上の粒子が何を表すか")
    box(d, 50, 95, 330, 350, FILL1)
    ctext(d, 190, 118, "SPH ・ MPS", FS, BLUE)
    ctext(d, 190, 144, "連続体(流体)を粒子で離散化", FT)
    # 連続体を代表点で表す点群
    for i in range(5):
        for j in range(6):
            pcircle(d, 90 + j * 40, 190 + i * 24, 6, (225, 235, 250), BLUE, 2)
    ctext(d, 190, 322, "粒子=連続体の代表点", FT, BLUE)
    ctext(d, 190, 344, "Smoothed Particle Hydrodynamics /", 0, GRAY) if False else None
    ctext(d, 190, 344, "SPH / MPS = 連続体の離散化", FT, GRAY)
    box(d, 350, 95, 630, 350, FILL2)
    ctext(d, 490, 118, "DEM", FS, GREEN)
    ctext(d, 490, 144, "実在する固体粒子そのもの", FT)
    for (px, py, r) in [(430, 210, 22), (500, 195, 28), (560, 235, 20),
                        (470, 270, 24), (545, 290, 26), (600, 210, 16)]:
        pcircle(d, px, py, r, FILL1)
    ctext(d, 490, 322, "粒子=実在粒子の運動", FT, GREEN)
    ctext(d, 490, 344, "Discrete Element Method", FT, GRAY)
    note(d, "SPH=Smoothed Particle Hydrodynamics, MPS=Moving Particle Semi-implicit")
    save(im, "t1e14SphMpsDem")


# ============================================================
# 14-7 t1e14VelocityInterpolation : 補間法(helpful)
# ============================================================
def velocity_interpolation():
    im, d = new(); title(d, "粒子位置の流体速度を格子値から補間する")
    # 左: 格子と粒子, 格子点の速度ベクトル
    x0, y0 = 60, 110
    for i in range(3):
        for j in range(3):
            gx, gy = x0 + j * 80, y0 + i * 80
            node(d, gx, gy, 4, fill=BLUE, col=BLUE)
            arrow(d, gx, gy, gx + 26, gy - 12, BLUE, 2, 8)
    box(d, x0, y0, x0 + 160, y0 + 160, None if False else "white", 1) if False else None
    for k in range(4):
        d.rectangle((x0 - 0, y0, x0 + 160, y0 + 160), outline=LGRAY, width=1)
    pcircle(d, x0 + 95, y0 + 60, 10, FILL2)
    ctext(d, x0 + 95, y0 + 60, "P", FT)
    ctext(d, x0 + 80, y0 + 200, "格子上の速度 -> 粒子位置へ補間", FT, GRAY)
    # 右: 1次元プロファイル 線形 vs スプライン
    ox, oy, xl, yl = 360, 300, 250, 180
    axes(d, ox, oy, xl, yl, "x", "u")
    ptsx = [0.0, 0.25, 0.5, 0.75, 1.0]
    ptsy = [0.2, 0.7, 0.4, 0.85, 0.55]
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    for t, v in zip(ptsx, ptsy):
        node(d, X(t), Y(v), 4, fill=BLACK, col=BLACK)
    # 線形補間(区分直線)
    d.line([(X(t), Y(v)) for t, v in zip(ptsx, ptsy)], fill=BLUE, width=2, joint="curve")
    # スプライン(滑らかな曲線)
    sp = []
    for i in range(101):
        t = i / 100
        # なめらかに通す簡易補間(sin重ね)
        v = 0.5 + 0.28 * math.sin(2 * math.pi * t - 0.6) + 0.08 * math.sin(4 * math.pi * t)
        sp.append((X(t), Y(v)))
    d.line(sp, fill=RED, width=2, joint="curve")
    ctext(d, X(0.55), Y(0.05), "線形=区分直線(簡便/散逸大)", FT, BLUE, "mm")
    ctext(d, X(0.5), Y(1.02), "スプライン=高階まで連続", FT, RED, "mm")
    note(d, "スペクトル補間=高精度だが直交級数分解が要る(複雑形状は不可)")
    save(im, "t1e14VelocityInterpolation")


# ============================================================
# 14-8 t1e14WallCollisionMomentum : 壁面衝突の成分分解(helpful)
# ============================================================
def wall_collision_momentum():
    im, d = new(); title(d, "壁面衝突: 運動量の法線成分・接線成分と回転")
    hwall(d, 90, 570, 320, side=1, n=16)
    cxi = 250   # 入射位置
    # 入射(斜め下向き)
    pcircle(d, cxi, 200, 20, FILL1)
    arrow(d, cxi - 80, 130, cxi - 8, 195, BLUE, 3, 13); ctext(d, cxi - 95, 120, "入射", FT, BLUE)
    # 成分分解(入射側)
    dotline(d, cxi, 320, cxi, 150, GRAY, 2)
    ctext(d, cxi + 60, 150, "法線 (normal)", FT, GRAY, "lm")
    # 反射(斜め上向き)
    pcircle(d, 430, 200, 20, FILL1)
    arrow(d, 438, 195, 510, 130, RED, 3, 13); ctext(d, 520, 120, "反射", FT, RED, "lm")
    # 法線成分: 反発係数eで反転・減衰
    arrow(d, 250, 260, 250, 300, BLUE, 2, 10); ctext(d, 250, 316, "v_n 入", FT, BLUE)
    arrow(d, 430, 300, 430, 250, RED, 2, 10); ctext(d, 430, 316, "e*v_n 出", FT, RED)
    # 接線成分: 摩擦で変化
    arrow(d, 300, 340, 380, 340, ORANGE, 2, 10); ctext(d, 340, 358, "接線 v_t は摩擦で変化", FT, ORANGE)
    # 回転(角運動量)発生
    spin(d, 430, 200, 30, GREEN, 3); ctext(d, 470, 180, "回転(角運動量)発生", FT, GREEN, "lm")
    note(d, "法線=反発係数eで反転減衰, 接線=摩擦で変化し衝突前に回転が無くても回転が生じる")
    save(im, "t1e14WallCollisionMomentum")


# ============================================================
# 14-9 t1e14WallImpulse : 壁面衝撃力の幾何(required・数値は書かない)
# ============================================================
def wall_impulse():
    im, d = new(); title(d, "壁面衝突の衝撃力  J_n(法線) と J_t(接線)")
    hwall(d, 90, 570, 300, side=1, n=16)
    cx = 260
    pcircle(d, cx, 190, 22, FILL1); ctext(d, cx, 190, "m", FT)
    # 入射速度と成分
    arrow(d, cx - 90, 110, cx - 10, 182, BLUE, 3, 13); ctext(d, cx - 100, 100, "入射", FT, BLUE)
    dotline(d, cx, 300, cx, 130, GRAY, 2)
    arrow(d, cx, 214, cx, 270, BLUE, 2, 10); ctext(d, cx + 30, 250, "v_n", FT, BLUE, "lm")
    arrow(d, cx + 24, 300, cx + 90, 300, ORANGE, 2, 10); ctext(d, cx + 100, 300, "v_t", FT, ORANGE, "lm")
    # 記号枠
    box(d, 380, 110, 630, 230, FILL2)
    ctext(d, 505, 135, "法線衝撃力  J_n = (1+e) m v_n", FT)
    ctext(d, 505, 168, "接線衝撃力  J_t =", FT)
    ctext(d, 505, 198, "min[ mu_f(1+e)m v_n ,  (2/7)m v_t ]", FT)
    ctext(d, 505, 262, "e=反発係数,  mu_f=クーロン動摩擦", FT, GRAY)
    ctext(d, 505, 288, "摩擦律速 と 接線速度律速 の小さいほう", FT, GRAY)
    note(d, "接線衝撃力は二つの上限のうち小さいほう(min)で決まる")
    save(im, "t1e14WallImpulse")


# ============================================================
# 14-10 t1e14CollisionStokes : 衝突ストークス数(helpful)
# ============================================================
def collision_stokes():
    im, d = new(); title(d, "衝突ストークス数  St = tau_p / tau_coll")
    # 2本のバー
    ctext(d, 130, 110, "tau_p (緩和時間)", FT, BLUE)
    d.rectangle((70, 125, 300, 150), outline=BLACK, width=2, fill=(225, 235, 250))
    ctext(d, 130, 175, "tau_coll (平均自由時間)", FT, GREEN)
    d.rectangle((70, 190, 160, 215), outline=BLACK, width=2, fill=(225, 245, 230))
    ctext(d, 430, 150, "比をとる -> St", FT, GRAY)
    # 数直線
    y = 300; x0, x1 = 90, 590; cx = (x0 + x1) / 2
    arrow(d, x0 - 5, y, x1 + 15, y, BLACK, 2, 11); ctext(d, x1 + 25, y, "St", FS, BLACK, "lm")
    d.line((cx, y - 10, cx, y + 10), fill=RED, width=3); ctext(d, cx, y + 24, "St = 1", FT, RED)
    ctext(d, cx - 150, y - 26, "St << 1", FS, BLUE)
    ctext(d, cx - 150, y + 30, "衝突を無視できる", FT, BLUE)
    ctext(d, cx + 150, y - 26, "St >> 1", FS, GREEN)
    ctext(d, cx + 150, y + 30, "衝突を無視できない", FT, GREEN)
    note(d, "低濃度でも tau_p が大きく変動速度が大きいと St>1 となり衝突を無視できない")
    save(im, "t1e14CollisionStokes")


# ============================================================
# 14-11 t1e14ContactForceModel : 接触力モデル(helpful)
# ============================================================
def contact_force_model():
    im, d = new(); title(d, "DEMの接触力モデル: 線形バネ と Hertz")
    # 左: 線形バネ
    box(d, 45, 100, 320, 350, FILL1)
    ctext(d, 182, 122, "線形バネモデル", FS, BLUE)
    pcircle(d, 90, 190, 22, FILL2); pcircle(d, 274, 190, 22, FILL2)
    spring(d, 112, 190, 252, coils=5, amp=12, wd=2)
    ctext(d, 182, 250, "反発力 ∝ 変位 (線形)", FT)
    ctext(d, 182, 282, "衝突時間は衝突速度に依存せず一定", FT, BLUE)
    ctext(d, 182, 312, "-> 必要な時間刻みも速度に無関係", FT, GRAY)
    # 右: Hertz
    box(d, 340, 100, 620, 350, FILL2)
    ctext(d, 480, 122, "Hertz 接触モデル", FS, GREEN)
    pcircle(d, 385, 190, 22, FILL1); pcircle(d, 575, 190, 22, FILL1)
    # 非線形バネ(密なコイル)
    spring(d, 407, 190, 553, coils=8, amp=10, wd=2)
    ctext(d, 480, 250, "非線形バネ(弾性接触理論)", FT)
    ctext(d, 480, 282, "衝突速度が大きいほど衝突時間が短い", FT, GREEN)
    ctext(d, 480, 312, "-> 速いほど小さな時間刻みが必要", FT, GRAY)
    note(d, "衝突時間の速度依存性が, 安定計算に必要な時間刻み幅の依存性に直結")
    save(im, "t1e14ContactForceModel")


# ============================================================
# 14-12 t1e14BlockPartition : ブロック分割法(helpful)
# ============================================================
def block_partition():
    im, d = new(); title(d, "ブロック分割法: 近傍だけ判定して高速化")
    x0, y0, c = 70, 90, 52
    n = 6
    for i in range(n + 1):
        d.line((x0, y0 + i * c, x0 + n * c, y0 + i * c), fill=LGRAY, width=1)
        d.line((x0 + i * c, y0, x0 + i * c, y0 + n * c), fill=LGRAY, width=1)
    # 対象粒子のブロック(中央)と隣接3x3を強調
    br, bc = 2, 2
    d.rectangle((x0 + bc * c, y0 + br * c, x0 + (bc + 1) * c, y0 + (br + 1) * c), outline=RED, width=3)
    d.rectangle((x0 + (bc - 1) * c, y0 + (br - 1) * c, x0 + (bc + 2) * c, y0 + (br + 2) * c),
                outline=BLUE, width=2)
    # 粒子を散らす
    import random
    random.seed(3)
    for _ in range(28):
        px = x0 + 6 + random.random() * (n * c - 12)
        py = y0 + 6 + random.random() * (n * c - 12)
        pcircle(d, px, py, 4, FILL2)
    pcircle(d, x0 + bc * c + c / 2, y0 + br * c + c / 2, 6, (250, 225, 225), RED, 2)
    ctext(d, x0 + n * c / 2, y0 + n * c + 22, "対象ブロック(赤)と隣接3x3(青)だけ判定", FT, GRAY)
    # 右: 計算量
    box(d, 430, 120, 630, 300, FILL1)
    ctext(d, 530, 150, "全粒子対で判定", FT)
    ctext(d, 530, 180, "計算時間 ∝ N^2", FS, RED)
    arrow(d, 530, 205, 530, 235, BLACK, 3, 12)
    ctext(d, 530, 258, "近傍限定(ブロック分割)", FT)
    ctext(d, 530, 285, "∝ N 程度に短縮", FS, GREEN)
    note(d, "ブロックは (相対速度の最大値 x 判定時間間隔) より大きく取る")
    save(im, "t1e14BlockPartition")


# ============================================================
# 14-13 t1e14BBOSedimentation : 沈降球の力のつり合い(required・数値なし)
# ============================================================
def bbo_sedimentation():
    im, d = new(); title(d, "静止流体中を沈降する球形粒子(Re << 1)")
    # 流体背景(薄い水平線)
    for yy in range(120, 360, 26):
        d.line((90, yy, 570, yy), fill=(232, 238, 245), width=1)
    cx, cy = 330, 230
    pcircle(d, cx, cy, 40, FILL1); ctext(d, cx, cy, "a, rho_p", FT)
    # 重力(下)
    force(d, cx, cy + 40, 0, 70, "重力 (rho_p)", RED)
    # 浮力(上)
    force(d, cx - 22, cy - 40, 0, -60, "浮力 (rho)", BLUE)
    # ストークス抗力(上)
    force(d, cx + 22, cy - 40, 0, -60, "抗力 6*pi*mu*a*U", GREEN)
    # 沈降方向
    arrow(d, 520, 180, 520, 300, GRAY, 2, 11); ctext(d, 540, 240, "沈降 U", FT, GRAY, "lm")
    ctext(d, cx, 360, "終端状態では 重力 = 浮力 + ストークス抗力 でつり合う", FT, GRAY)
    note(d, "粒子レイノルズ数 Re << 1(ストークス域). 加速度・非定常抗力は終端で消える")
    save(im, "t1e14BBOSedimentation")


# ============================================================
# 14-14 t1e14TwoBubblesInLine : 直列2気泡(required・大小関係は書かない)
# ============================================================
def two_bubbles_in_line():
    im, d = new(); title(d, "静止液中を直列に上昇する2つの気泡")
    # 液中の背景
    for yy in range(110, 380, 26):
        d.line((120, yy, 540, yy), fill=(232, 238, 245), width=1)
    cx = 330
    # 前方(上)の気泡
    pcircle(d, cx, 160, 34, (235, 242, 250), BLUE, 3); ctext(d, cx, 160, "a", FT)
    arrow(d, cx, 122, cx, 82, RED, 3, 13); ctext(d, cx + 26, 95, "W_1(前方)", FT, RED, "lm")
    # 後方(下)の気泡
    pcircle(d, cx, 300, 34, (235, 242, 250), BLUE, 3); ctext(d, cx, 300, "a", FT)
    arrow(d, cx, 262, cx, 222, RED, 3, 13); ctext(d, cx + 26, 235, "W_2(後方)", FT, RED, "lm")
    # 重心間距離L
    dim(d, cx - 70, 160, cx - 70, 300, "L (>> a)", col=GRAY)
    # 参照: 単一気泡の終端速度W
    pcircle(d, 150, 230, 26, (245, 245, 245), GRAY, 2); ctext(d, 150, 230, "a", FT, GRAY)
    arrow(d, 150, 200, 150, 165, GRAY, 2, 11); ctext(d, 150, 150, "単一気泡 W", FT, GRAY)
    note(d, "レイノルズ数は1より十分小さい. 誘起速度の向きや W,W_1,W_2 の大小は各自考える")
    save(im, "t1e14TwoBubblesInLine")


# ============================================================
# 14-15 t1e14SpringDashpot : DEMのバネとダンパー(helpful)
# ============================================================
def spring_dashpot():
    im, d = new(); title(d, "DEM: 粒子接触部のバネ と ダンパー")
    pcircle(d, 150, 200, 46, FILL1); ctext(d, 150, 200, "粒子1", FT)
    pcircle(d, 510, 200, 46, FILL1); ctext(d, 510, 200, "粒子2", FT)
    # バネ(上)
    spring(d, 196, 172, 464, coils=7, amp=14, wd=3)
    ctext(d, 330, 138, "バネ = 弾性的な反発(運動量交換)", FT, BLUE)
    # ダンパー(下)
    d.line((196, 235, 300, 235), fill=BLACK, width=3)
    d.rectangle((300, 218, 340, 252), outline=BLACK, width=3, fill=FILL2)  # シリンダ
    d.line((330, 235, 464, 235), fill=BLACK, width=3)
    d.line((360, 220, 360, 250), fill=BLACK, width=4)                     # ピストン
    ctext(d, 330, 278, "ダンパー = エネルギー散逸", FT, GREEN)
    ctext(d, 330, 322, "有限の時間刻みで衝突を緩和して安定に解く", FT, GRAY)
    note(d, "接触・衝突の運動量交換とエネルギー散逸を表す(狭隘部の流体潤滑力とは別物)")
    save(im, "t1e14SpringDashpot")


# ============================================================
# 14-16 t1e14BubbleTracking : 気泡追跡法(helpful)
# ============================================================
def bubble_tracking():
    im, d = new(); title(d, "気泡追跡法 (液相=連続体, 気泡=質点 の Euler-Lagrange)")
    # 左: 連続体格子+質点の気泡
    x0, y0 = 60, 105
    for i in range(4):
        for j in range(4):
            d.rectangle((x0 + j * 55, y0 + i * 45, x0 + j * 55 + 55, y0 + i * 45 + 45),
                        outline=LGRAY, width=1)
    ctext(d, x0 + 110, y0 - 4, "液相=連続体の格子", FT, GRAY)
    for (px, py) in [(x0 + 40, y0 + 30), (x0 + 130, y0 + 80), (x0 + 90, y0 + 140),
                     (x0 + 180, y0 + 50), (x0 + 60, y0 + 120), (x0 + 150, y0 + 150)]:
        pcircle(d, px, py, 8, (235, 242, 250), BLUE, 2)
    ctext(d, x0 + 110, y0 + 210, "気泡=質点として追跡", FT, BLUE)
    # 右: 利点と短所
    box(d, 360, 100, 630, 250, FILL1)
    ctext(d, 495, 122, "利点", FS, GREEN)
    for i, s in enumerate(["多数の気泡を同時に扱える",
                           "気泡のサイズ分布を扱える",
                           "合体・分裂もモデルで表現"]):
        ctext(d, 495, 152 + i * 30, s, FT)
    box(d, 360, 262, 630, 340, FILL2)
    ctext(d, 495, 285, "短所(質点近似ゆえ)", FT, RED)
    ctext(d, 495, 315, "気液相互作用は経験的相関式に依存", FT)
    note(d, "界面追跡法(界面を陽に追う)との対比. 相関式依存は利点ではなく短所")
    save(im, "t1e14BubbleTracking")


# ============================================================
# 14-17 t1e14RotatingTrajectory : 回転場中の粒子軌跡(required・対応は書かない)
# ============================================================
def rotating_trajectory():
    im, d = new(); title(d, "一定角速度 Omega で回転する液体中の粒子軌跡")
    cx, cy = 300, 235
    R = 120
    # 回転場の枠
    d.ellipse((cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8), outline=LGRAY, width=1)
    node(d, cx, cy, 4, fill=GRAY, col=GRAY); ctext(d, cx, cy + 16, "渦中心", FT, GRAY)
    # 回転向き
    d.arc((cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8), 200, 250, fill=GRAY, width=2)
    ctext(d, cx, cy - R - 22, "Omega", FT, GRAY)
    # 出発点(R,0)
    sx, sy = cx + R, cy
    node(d, sx, sy, 5, fill=BLACK, col=BLACK); ctext(d, sx + 8, sy - 14, "t=0 出発", FT, GRAY, "lm")
    # 内向き螺旋(実線)
    p1 = []
    for i in range(241):
        th = i / 240 * 4 * math.pi
        r = R * math.exp(-0.055 * th)
        p1.append((cx + r * math.cos(th), cy - r * math.sin(th)))
    d.line(p1, fill=BLUE, width=3, joint="curve")
    # 円軌道(破線)
    p2 = []
    for i in range(241):
        th = i / 240 * 2 * math.pi
        p2.append((cx + R * math.cos(th), cy - R * math.sin(th)))
    for i in range(0, len(p2) - 1, 6):
        d.line((p2[i], p2[i + 1]), fill=GREEN, width=2)
    # 外向き螺旋(点線)
    p3 = []
    for i in range(1, 200):
        th = i / 240 * 4 * math.pi
        r = R * math.exp(0.05 * th)
        if r > R + 90: break
        p3.append((cx + r * math.cos(th), cy - r * math.sin(th)))
    for i in range(0, len(p3) - 1, 4):
        d.ellipse((p3[i][0] - 1, p3[i][1] - 1, p3[i][0] + 1, p3[i][1] + 1), fill=RED)
    # 凡例(どれがどのSt/betaかは書かない)
    lx = 500
    d.line((lx, 150, lx + 40, 150), fill=BLUE, width=3); ctext(d, lx + 48, 150, "渦中心へ", FT, BLUE, "lm")
    dashed(d, lx, 185, lx + 40, 185, GREEN, 2, 8, 5); ctext(d, lx + 48, 185, "円軌道", FT, GREEN, "lm")
    dotline(d, lx, 220, lx + 40, 220, RED, 2, 2, 6); ctext(d, lx + 48, 220, "渦中心から離れる", FT, RED, "lm")
    ctext(d, lx + 40, 258, "軸: 粒子位置 (x_p, y_p)", FT, GRAY)
    note(d, "St(追従性)と密度比 beta(最終的な集まり方)で軌跡が決まる")
    save(im, "t1e14RotatingTrajectory")


# ============================================================
# ===============  公式・用語カード  t1f14*  =================
# ============================================================

# t1f14-1 粒子の運動方程式
def f_particle_eq():
    im, d = new(); title(d, "粒子の運動方程式 (Euler-Lagrange法)")
    box(d, 70, 90, 590, 165, FILL2)
    ctext(d, 330, 118, "dy/dt = v", FS)
    ctext(d, 330, 146, "dv/dt = [3/(2beta+1)] Du/Dt + (u - v)/tau_p", FS)
    ctext(d, 200, 210, "第1項", F, BLUE); ctext(d, 200, 240, "流体加速度項", FT, BLUE)
    ctext(d, 200, 264, "(圧力勾配+仮想質量)", FT, GRAY)
    ctext(d, 200, 288, "beta = rho_p/rho_f", FT, GRAY)
    ctext(d, 470, 210, "第2項", F, GREEN); ctext(d, 470, 240, "ストークス抗力項", FT, GREEN)
    ctext(d, 470, 264, "速度差 (u - v) に比例", FT, GRAY)
    ctext(d, 470, 288, "時定数 tau_p で緩和", FT, GRAY)
    note(d, "気泡(beta<<1)は 3/(2beta+1)≈3 で流体加速に強く従う, 重い粒子(beta>>1)は鈍い")
    save(im, "t1f14ParticleEqOfMotion")


# t1f14-2 粒子緩和時間
def f_relaxation_time():
    im, d = new(); title(d, "粒子緩和時間  tau_p")
    box(d, 150, 95, 510, 155, FILL2)
    ctext(d, 330, 125, "tau_p = a^2 (2beta+1) / (9 nu)", F)
    ctext(d, 330, 185, "a=粒子半径,  beta=rho_p/rho_f,  nu=動粘性", FT, GRAY)
    ctext(d, 330, 225, "要点: tau_p ∝ a^2", FS, RED)
    ctext(d, 330, 262, "小さい粒子ほど緩和が速い(すぐ流体に追従)", FT)
    ctext(d, 330, 292, "大きい粒子ほど緩和が遅い(慣性で遅れる)", FT)
    ctext(d, 330, 330, "ストークス数 St = tau_p / tau_f", FT, BLUE)
    note(d, "安定条件 Delta t < tau_p を左右. 半径を半分にすると tau_p は 1/4")
    save(im, "t1f14RelaxationTime")


# t1f14-3 陽解法の安定条件
def f_stability_conditions():
    im, d = new(); title(d, "陽解法の数値安定条件(3つの制約)")
    rows = [("(i)  Delta t << T", "流体速度の変動周期 T より十分小さい", BLUE),
            ("(ii) Delta t < tau_p", "粒子緩和時間より小さい", GREEN),
            ("(iii) |v| Delta t / Delta x <= 1", "クーラン条件(1ステップで格子幅を越えない)", ORANGE)]
    for i, (a, b, col) in enumerate(rows):
        yy = 130 + i * 70
        box(d, 60, yy - 26, 600, yy + 30, FILL1)
        ctext(d, 90, yy, a, FS, col, "lm")
        ctext(d, 90, yy + 22, b, FT, GRAY, "lm")
    note(d, "a が小さいと tau_p ∝ a^2 が小さく (ii) が満たしにくい -> 微小粒子は不安定になりやすい")
    save(im, "t1f14StabilityConditions")


# t1f14-4 緩和方程式の陽解法/陰解法
def f_integration_stability():
    im, d = new(); title(d, "緩和方程式の時間積分: 陽解法 と 陰解法")
    box(d, 45, 95, 320, 340, FILL1)
    ctext(d, 182, 118, "オイラー陽解法", FS, RED)
    ctext(d, 182, 152, "v^(n+1) =", FT)
    ctext(d, 182, 178, "(1 - Delta t/tau) v^n + (Delta t/tau) u", 0, BLACK) if False else \
        ctext(d, 182, 178, "(1-Delta t/tau)v^n + (Delta t/tau)u", FT)
    ctext(d, 182, 214, "増幅率 |1 - Delta t/tau| < 1", FT)
    ctext(d, 182, 250, "tau=0.1, Delta t=1 なら", FT, GRAY)
    ctext(d, 182, 276, "1 - 10 = -9  -> 発散", FS, RED)
    ctext(d, 182, 312, "高次法でも救えない", FT, GRAY)
    box(d, 340, 95, 615, 340, FILL2)
    ctext(d, 477, 118, "オイラー陰解法", FS, GREEN)
    ctext(d, 477, 152, "v^(n+1) =", FT)
    ctext(d, 477, 178, "[v^n + (Delta t/tau)u] / (1 + Delta t/tau)", FT)
    ctext(d, 477, 214, "任意の Delta t で |増幅率|<1", FT)
    ctext(d, 477, 250, "同条件で 1/(1+10)=1/11", FS, GREEN)
    ctext(d, 477, 286, "-> 無条件に安定", FT)
    ctext(d, 477, 312, "硬い緩和項に有効", FT, GRAY)
    note(d, "Delta t が tau よりずっと大きい硬い問題では陰解法・半陰解法が有効")
    save(im, "t1f14IntegrationStability")


# t1f14-5 連成の段階
def f_coupling_levels():
    im, d = new(); title(d, "連成の段階  one-way / two-way / four-way")
    rows = [("one-way (片方向)", "粒子は流体から力を受けるが反作用は返さない", "微小かつ希薄", BLUE),
            ("two-way (双方向)", "粒子から流体への反作用も返す", "濃度が上がり流れに影響", GREEN),
            ("four-way", "粒子どうしの接触・衝突も含める", "濃密で衝突が支配的", ORANGE)]
    for i, (a, b, c, col) in enumerate(rows):
        yy = 120 + i * 78
        box(d, 55, yy - 28, 605, yy + 36, FILL1)
        ctext(d, 80, yy - 6, a, FS, col, "lm")
        ctext(d, 80, yy + 20, b, FT, BLACK, "lm")
        ctext(d, 440, yy - 6, "適用: " + c, FT, GRAY, "lm")
    note(d, "濃度が上がるほど高次の連成が必要になる")
    save(im, "t1f14CouplingLevels")


# t1f14-6 PSI-Cell法
def f_psi_cell():
    im, d = new(); title(d, "PSI-Cell法 (Particle-Source-in-Cell)")
    # セル
    x0, y0 = 80, 110
    for i in range(3):
        for j in range(3):
            box(d, x0 + j * 66, y0 + i * 66, x0 + j * 66 + 66, y0 + i * 66 + 66, "white", 2)
    ccx, ccy = x0 + 99, y0 + 99
    pcircle(d, ccx, ccy, 12, FILL2)
    for k in range(3):
        arrow(d, ccx + 14, ccy - 10 + k * 10, ccx + 40, ccy - 10 + k * 10, GRAY, 2, 7)
    arrow(d, ccx, ccy + 40, ccx, ccy + 14, RED, 3, 11)
    ctext(d, x0 + 99, y0 + 210, "セル内粒子の反力合計", FT, RED)
    ctext(d, x0 + 99, y0 + 234, "= 流体運動方程式の体積力", FT, RED)
    box(d, 400, 120, 620, 300, FILL2)
    ctext(d, 510, 145, "適用の前提", FS, GREEN)
    ctext(d, 510, 182, "(1) 粒子径 << 格子", FT)
    ctext(d, 510, 214, "  (点として扱える)", FT, GRAY)
    ctext(d, 510, 250, "(2) 後流の速度欠損が", FT)
    ctext(d, 510, 278, "  そのセル内に収まる", FT)
    note(d, "後流欠損が隣接セルまで広がると1セルの体積力では表せず不適切(Crowe 1977)")
    save(im, "t1f14PsiCell")


# t1f14-7 SPH/MPS/DEM
def f_sph_mps_dem():
    im, d = new(); title(d, "格子を使わない粒子法の2系統")
    box(d, 50, 100, 330, 350, FILL1)
    ctext(d, 190, 124, "SPH ・ MPS", FS, BLUE)
    ctext(d, 190, 156, "連続体(流体)を", FT)
    ctext(d, 190, 182, "計算上の粒子で離散化", FT)
    for i in range(4):
        for j in range(5):
            pcircle(d, 100 + j * 40, 230 + i * 26, 6, (225, 235, 250), BLUE, 2)
    ctext(d, 190, 344, "粒子 = 連続体の代表点", FT, BLUE)
    box(d, 350, 100, 630, 350, FILL2)
    ctext(d, 490, 124, "DEM (離散要素法)", FS, GREEN)
    ctext(d, 490, 156, "実在する固体粒子を", FT)
    ctext(d, 490, 182, "計算上の粒子として解く", FT)
    for (px, py, r) in [(430, 240, 22), (500, 225, 28), (565, 260, 20), (475, 295, 24), (555, 305, 22)]:
        pcircle(d, px, py, r, FILL1)
    ctext(d, 490, 344, "粒子 = 実在粒子の運動", FT, GREEN)
    note(d, "計算上の粒子が『連続体の離散点か/実在粒子か』が決定的な違い")
    save(im, "t1f14SphMpsDem")


# t1f14-8 補間法
def f_velocity_interpolation():
    im, d = new(); title(d, "粒子位置の流体速度の補間法")
    rows = [("スペクトル補間", "高精度. ただし直交級数に分解できる場合のみ", "複雑形状は不可", BLUE),
            ("線形補間(2次ラグランジュ)", "計算負荷が低く簡便", "乱流では散逸が大", GREEN),
            ("スプライン補間", "高階微係数まで連続, 低次でも正確", "係数計算の負荷やや大", ORANGE)]
    for i, (a, b, c, col) in enumerate(rows):
        yy = 120 + i * 78
        box(d, 50, yy - 28, 610, yy + 36, FILL1)
        ctext(d, 75, yy - 6, a, FS, col, "lm")
        ctext(d, 75, yy + 20, b, FT, BLACK, "lm")
        ctext(d, 430, yy + 20, c, FT, RED, "lm")
    note(d, "粒子速度=流体速度とみなせるのは St が十分小さく外力が働かない特殊な場合のみ")
    save(im, "t1f14VelocityInterpolation")


# t1f14-9 壁面衝突の衝撃力
def f_wall_impulse():
    im, d = new(); title(d, "壁面衝突の衝撃力(法線・接線)")
    box(d, 80, 100, 580, 200, FILL2)
    ctext(d, 330, 130, "J_n = (1+e) m v_n", FS)
    ctext(d, 330, 170, "J_t = min[ mu_f(1+e)m v_n ,  (2/7)m v_t ]", FS)
    ctext(d, 330, 232, "接線は『滑りが消えるか否か』で小さいほう(min)", FT)
    ctext(d, 200, 268, "mu_f(1+e)m v_n", FT, BLUE); ctext(d, 200, 292, "滑りが残る(摩擦律速)", FT, GRAY)
    ctext(d, 470, 268, "(2/7) m v_t", FT, GREEN); ctext(d, 470, 292, "滑りが消える(接線速度律速)", FT, GRAY)
    ctext(d, 330, 330, "係数 2/7 は球の慣性モーメントに由来. 摩擦で回転(角運動量)が生じる", FT, GRAY)
    note(d, "例: m=1e-6, e=0.5, v_n=2, v_t=1.5, mu_f=0.3 -> 摩擦側9.0e-7, 接線側4.3e-7 の小さいほう")
    save(im, "t1f14WallImpulse")


# t1f14-10 衝突頻度と衝突ストークス数
def f_collision_frequency():
    im, d = new(); title(d, "粒子間衝突頻度 と 衝突ストークス数")
    box(d, 90, 100, 570, 160, FILL2)
    ctext(d, 330, 130, "f_coll = pi d_p^2 n |V_R|,     St = tau_p / tau_coll", FS)
    ctext(d, 330, 190, "d_p=粒径, n=数密度, V_R=相対速度", FT, GRAY)
    # 数直線
    y = 275; x0, x1 = 100, 580; cx = (x0 + x1) / 2
    arrow(d, x0 - 5, y, x1 + 15, y, BLACK, 2, 11); ctext(d, x1 + 25, y, "St", FS, BLACK, "lm")
    d.line((cx, y - 10, cx, y + 10), fill=RED, width=3); ctext(d, cx, y + 22, "1", FT, RED)
    ctext(d, cx - 150, y - 24, "St << 1", FS, BLUE); ctext(d, cx - 150, y + 26, "衝突を無視できる", FT, BLUE)
    ctext(d, cx + 150, y - 24, "St >> 1", FS, GREEN); ctext(d, cx + 150, y + 26, "無視できない", FT, GREEN)
    note(d, "体積分率 1e-3 程度でも tau_p 大・変動速度大なら St>1 で衝突を無視できない")
    save(im, "t1f14CollisionFrequency")


# t1f14-11 接触力モデル
def f_contact_force_model():
    im, d = new(); title(d, "DEMの接触力モデル(線形バネ・Hertz)")
    box(d, 45, 100, 320, 350, FILL1)
    ctext(d, 182, 124, "線形バネモデル", FS, BLUE)
    ctext(d, 182, 158, "反発力 ∝ 変位(線形)", FT)
    pcircle(d, 92, 205, 20, FILL2); pcircle(d, 272, 205, 20, FILL2)
    spring(d, 112, 205, 252, coils=5, amp=11, wd=2)
    ctext(d, 182, 258, "衝突時間は衝突速度に依存せず一定", FT, BLUE)
    ctext(d, 182, 300, "必要な時間刻みも", FT, GRAY)
    ctext(d, 182, 324, "衝突速度に依存しない", FT, GRAY)
    box(d, 340, 100, 620, 350, FILL2)
    ctext(d, 480, 124, "Hertz 接触モデル", FS, GREEN)
    ctext(d, 480, 158, "非線形バネ(弾性接触理論)", FT)
    pcircle(d, 390, 205, 20, FILL1); pcircle(d, 570, 205, 20, FILL1)
    spring(d, 410, 205, 550, coils=8, amp=9, wd=2)
    ctext(d, 480, 258, "衝突速度が大きいほど衝突時間が短い", FT, GREEN)
    ctext(d, 480, 300, "速いほど小さな", FT, GRAY)
    ctext(d, 480, 324, "時間刻みが必要", FT, GRAY)
    note(d, "どちらもダンパーを加えてエネルギー散逸(反発係数)を表現する")
    save(im, "t1f14ContactForceModel")


# t1f14-12 ブロック分割法
def f_block_partition():
    im, d = new(); title(d, "ブロック分割法(近傍探索による高速化)")
    x0, y0, c = 70, 95, 50
    n = 6
    for i in range(n + 1):
        d.line((x0, y0 + i * c, x0 + n * c, y0 + i * c), fill=LGRAY, width=1)
        d.line((x0 + i * c, y0, x0 + i * c, y0 + n * c), fill=LGRAY, width=1)
    d.rectangle((x0 + 2 * c, y0 + 2 * c, x0 + 3 * c, y0 + 3 * c), outline=RED, width=3)
    d.rectangle((x0 + 1 * c, y0 + 1 * c, x0 + 4 * c, y0 + 4 * c), outline=BLUE, width=2)
    pcircle(d, x0 + 2 * c + c / 2, y0 + 2 * c + c / 2, 6, (250, 225, 225), RED, 2)
    ctext(d, x0 + n * c / 2, y0 + n * c + 20, "対象+隣接ブロックだけ判定", FT, GRAY)
    box(d, 430, 130, 630, 300, FILL1)
    ctext(d, 530, 158, "全粒子対 -> ∝ N^2", FS, RED)
    arrow(d, 530, 185, 530, 215, BLACK, 3, 12)
    ctext(d, 530, 240, "近傍限定 -> ∝ N", FS, GREEN)
    ctext(d, 530, 278, "程度に短縮", FT, GRAY)
    note(d, "接触判定は最大粒子直径より, 衝突判定は(相対速度最大 x 判定間隔)より大きく取る")
    save(im, "t1f14BlockPartition")


# t1f14-13 BBO方程式
def f_bbo_equation():
    im, d = new(); title(d, "沈降球の運動方程式 (BBO方程式) と各項")
    box(d, 40, 90, 620, 150, FILL2)
    ctext(d, 330, 110, "(4pi/3)a^3 rho_p dU/dt =", FT)
    ctext(d, 330, 134, "(4pi/3)a^3(rho_p-rho)g - 6pi mu a U - (2pi/3)a^3 rho dU/dt - Basset", FT)
    terms = [("第1項", "重力 と 浮力 の差", BLUE),
             ("第2項", "定常ストークス抗力 6pi mu a U", GREEN),
             ("第3項", "仮想(付加)質量力", ORANGE),
             ("第4項", "Basset 履歴力(渦度拡散の履歴)", RED)]
    for i, (a, b, col) in enumerate(terms):
        yy = 190 + i * 34
        ctext(d, 110, yy, a, FS, col, "lm")
        ctext(d, 210, yy, b, FT, BLACK, "lm")
    ctext(d, 330, 336, "t=0: dU/dt = (rho_p-rho)/(rho_p+rho/2) g (第2・4項は0)", FT, GRAY)
    note(d, "Basset力を無視すると過渡の沈降速度を過大評価する")
    save(im, "t1f14BBOEquation")


# t1f14-14 ストークス終端速度
def f_stokes_terminal():
    im, d = new(); title(d, "ストークス終端速度")
    box(d, 170, 95, 490, 155, FILL2)
    ctext(d, 330, 125, "U = 2 a^2 (rho_p - rho) g / (9 mu)", F)
    # つり合いの絵
    cx, cy = 160, 260
    pcircle(d, cx, cy, 30, FILL1)
    force(d, cx, cy + 30, 0, 50, "重力", RED)
    force(d, cx - 16, cy - 30, 0, -44, "浮力", BLUE)
    force(d, cx + 16, cy - 30, 0, -44, "抗力", GREEN)
    ctext(d, 470, 210, "半径の2乗 a^2 に比例", FT)
    ctext(d, 470, 240, "密度差 (rho_p-rho) に比例", FT)
    ctext(d, 470, 270, "粘性 mu に反比例", FT)
    ctext(d, 470, 305, "密度差>0:沈降, <0:上昇(気泡)", FT, GRAY)
    note(d, "半径ではなく直径を代入したり係数2や密度差を落とすと桁を誤る. 半径2倍で終端4倍")
    save(im, "t1f14StokesTerminalVelocity")


# t1f14-15 気泡追跡法 vs 界面追跡法
def f_bubble_vs_interface():
    im, d = new(); title(d, "気泡追跡法 と 界面追跡法 の使い分け")
    box(d, 45, 100, 320, 350, FILL1)
    ctext(d, 182, 124, "気泡追跡法 (Euler-Lagrange)", FS, BLUE)
    ctext(d, 182, 152, "液相=連続体, 気泡=質点", FT)
    for i, s in enumerate(["多数の気泡・サイズ分布を扱える",
                           "合体・分裂もモデルで表現",
                           "気液相互作用は経験的相関式に依存"]):
        col = RED if i == 2 else BLACK
        ctext(d, 182, 190 + i * 34, s, FT, col)
    ctext(d, 182, 316, "多数の気泡の統計挙動向き", FT, GRAY)
    box(d, 340, 100, 620, 350, FILL2)
    ctext(d, 480, 124, "界面追跡法 (VOF・Level Set)", FS, GREEN)
    ctext(d, 480, 152, "気液界面を陽に追う", FT)
    for i, s in enumerate(["界面の変形・ちぎれ・合体を直接計算",
                           "形状変化そのものが得られる",
                           "多数の気泡は計算負荷が大"]):
        ctext(d, 480, 190 + i * 34, s, FT)
    ctext(d, 480, 316, "界面形状の変化を見たいとき向き", FT, GRAY)
    note(d, "『相関式に依存しなくなる』は気泡追跡法の利点ではない(むしろ短所)")
    save(im, "t1f14BubbleVsInterfaceTracking")


# t1f14-16 回転場中の粒子軌跡
def f_rotating_field():
    im, d = new(); title(d, "回転場中の粒子軌跡 (ストークス数と密度比)")
    box(d, 70, 90, 590, 150, FILL2)
    ctext(d, 330, 110, "St = Omega a^2 (2 rho_p + rho_f)/(9 mu),   beta = rho_p/rho_f", FT)
    ctext(d, 330, 136, "St=追従性, beta=最終的な集まり方 を支配", FT, GRAY)
    cx, cy = 200, 290
    node(d, cx, cy, 4, fill=GRAY, col=GRAY); ctext(d, cx, cy + 14, "渦中心", FT, GRAY)
    # 内向き(beta<1) 破線
    p = []
    for i in range(200):
        th = i / 240 * 4 * math.pi
        r = 95 * math.exp(-0.06 * th)
        p.append((cx + r * math.cos(th), cy - r * math.sin(th)))
    for i in range(0, len(p) - 1, 5):
        d.line((p[i], p[i + 1]), fill=BLUE, width=2)
    # 外向き(beta>1) 点線
    p = []
    for i in range(1, 160):
        th = i / 240 * 4 * math.pi
        r = 30 * math.exp(0.07 * th)
        if r > 95: break
        p.append((cx + r * math.cos(th), cy - r * math.sin(th)))
    for i in range(0, len(p), 3):
        d.ellipse((p[i][0] - 1, p[i][1] - 1, p[i][0] + 1, p[i][1] + 1), fill=RED)
    ctext(d, 430, 200, "St 小: 回転流に追従しやすい", FT, BLACK, "lm")
    ctext(d, 430, 240, "beta<1(気泡): 渦中心へ集まる", FT, BLUE, "lm")
    ctext(d, 430, 280, "beta>1(重い): 渦中心から離れる", FT, RED, "lm")
    ctext(d, 430, 320, "St 大: 慣性で初め中心へ向かう", FT, GRAY, "lm")
    note(d, "St が追従性を, beta が最終的な集まり方(中心へ/外へ)を支配する")
    save(im, "t1f14RotatingFieldTrajectory")


# ============================================================
if __name__ == "__main__":
    # --- 問題図 t1e14 (17) ---
    method_selection()
    relaxation_time_stability()
    time_integration()
    one_way_coupling()
    psi_cell_coupling()
    sph_mps_dem()
    velocity_interpolation()
    wall_collision_momentum()
    wall_impulse()
    collision_stokes()
    contact_force_model()
    block_partition()
    bbo_sedimentation()
    two_bubbles_in_line()
    spring_dashpot()
    bubble_tracking()
    rotating_trajectory()
    # --- 公式・用語図 t1f14 (16) ---
    f_particle_eq()
    f_relaxation_time()
    f_stability_conditions()
    f_integration_stability()
    f_coupling_levels()
    f_psi_cell()
    f_sph_mps_dem()
    f_velocity_interpolation()
    f_wall_impulse()
    f_collision_frequency()
    f_contact_force_model()
    f_block_partition()
    f_bbo_equation()
    f_stokes_terminal()
    f_bubble_vs_interface()
    f_rotating_field()
    print("done ch14")
