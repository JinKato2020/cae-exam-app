# -*- coding: utf-8 -*-
"""固体力学1級 第7章「伝熱解析」の問題図(s1e7*)を描画。
白地660x420・線画・機構のみ・物理的に正確・装飾禁止。
豆腐回避のためギリシャ文字/特殊記号はローマ字表記に置換
(lambda,kappa,rho,c,sigma,eps,theta,dt,grad^2,T^4,degC 等)。"""
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


def wavy_arrow(d, x0, y, x1, amp=6, waves=3, col=ORANGE, wd=2, head=11):
    """x0->x1 へ波打つ矢印(ふく射=電磁波の表現)。"""
    n = 60
    pts = []
    for i in range(n + 1):
        t = i / n
        xx = x0 + (x1 - x0) * t
        yy = y - amp * math.sin(2 * math.pi * waves * t)
        pts.append((xx, yy))
    d.line(pts, fill=col, width=wd, joint="curve")
    ang = math.atan2(0, x1 - x0)
    for s in (0.5, -0.5):
        d.line((x1, y, x1 - head * math.cos(ang - s), y - head * math.sin(ang - s)), fill=col, width=wd)


def massblock(d, cx, cy, w, h, label="", fnt=F, fill=FILL1):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=fill)
    if label:
        ctext(d, cx, cy, label, fnt)


# ============================================================
# 7-1 s1e7ThreeModes : 伝熱の3機構
# ============================================================
def three_modes():
    im, d = new(); title(d, "伝熱の3機構 (conduction / convection / radiation)")
    # --- 熱伝導 conduction ---
    cx = 120
    d.rectangle((cx - 58, 120, cx + 58, 250), outline=BLACK, width=3, fill=FILL1)
    d.line((cx - 58, 120, cx - 58, 250), fill=RED, width=5)   # hot 左面
    d.line((cx + 58, 120, cx + 58, 250), fill=BLUE, width=5)  # cold 右面
    ctext(d, cx - 58, 106, "hot", FT, RED); ctext(d, cx + 58, 106, "cold", FT, BLUE)
    arrow(d, cx - 30, 185, cx + 40, 185, BLACK, 3, 12); ctext(d, cx, 165, "q", FT)
    ctext(d, cx, 272, "熱伝導 conduction", FT, BLUE)
    ctext(d, cx, 292, "固体内 temp gradient", FT, GRAY)
    # --- 対流 convection ---
    cx = 330
    d.line((cx - 55, 120, cx - 55, 250), fill=BLACK, width=4)  # 固体壁 wall
    ctext(d, cx - 55, 106, "wall", FT)
    for k in range(3):
        yy = 140 + k * 40
        pts = [(cx - 45 + 90 * i / 40, yy - 7 * math.sin(2 * math.pi * 2 * i / 40)) for i in range(41)]
        d.line(pts, fill=BLUE, width=2, joint="curve")
    arrow(d, cx - 45, 235, cx + 45, 235, RED, 2, 10)          # 流れ flow
    ctext(d, cx + 20, 165, "fluid", FT, BLUE)
    ctext(d, cx, 272, "対流熱伝達 convection", FT, GREEN)
    ctext(d, cx, 292, "流体 <-> 固体壁", FT, GRAY)
    # --- ふく射 radiation ---
    cx = 540
    massblock(d, cx - 48, 185, 30, 90, "", fill=(250, 225, 225))
    massblock(d, cx + 48, 185, 30, 90, "", fill=(225, 230, 250))
    ctext(d, cx - 48, 132, "hot", FT, RED); ctext(d, cx + 48, 132, "cold", FT, BLUE)
    for yy in (165, 185, 205):
        wavy_arrow(d, cx - 30, yy, cx + 30, amp=5, waves=3, col=ORANGE, wd=2)
    ctext(d, cx, 232, "vacuum OK", FT, GRAY)
    ctext(d, cx, 272, "ふく射 radiation", FT, ORANGE)
    ctext(d, cx, 292, "電磁波 媒体不要", FT, GRAY)
    note(d, "熱伝導=物体内の温度こう配, 対流=流体と壁, ふく射=電磁波(真空でも起こる)")
    save(im, "s1e7ThreeModes")


# ============================================================
# 7-2 s1e7Fourier : 平板の直線温度分布と熱流束 q=lambda*dT/L
# ============================================================
def fourier():
    im, d = new(); title(d, "フーリエの法則  q = lambda * dT / L")
    # T-x グラフ
    ox, oy, xl, yl = 150, 300, 360, 200
    axes(d, ox, oy, xl, yl, "x (0 -> L)", "T")
    def Y(T): return oy - (T - 20) / 100 * yl   # 20..120 degC を高さに
    # 平板の帯(グラフ背景に薄く)
    dashed(d, ox, oy, ox, oy - yl, LGRAY, 1, 5, 4)
    dashed(d, ox + xl, oy, ox + xl, oy - yl, LGRAY, 1, 5, 4)
    # 直線温度分布 120 -> 20
    plot(d, 0, 0, [(ox, Y(120)), (ox + xl, Y(20))], RED, 3)
    node(d, ox, Y(120), 6, fill=RED, col=RED); node(d, ox + xl, Y(20), 6, fill=BLUE, col=BLUE)
    ctext(d, ox - 8, Y(120), "120 degC", FT, RED, "rm")
    ctext(d, ox + xl + 6, Y(20) - 24, "20 degC", FT, BLUE, "lb")
    ctext(d, ox + 40, oy - yl - 8, "hot", FT, RED); ctext(d, ox + xl - 40, oy + 18, "cold", FT, BLUE)
    # 熱流束の矢印(右向き)
    arrow(d, ox + 60, oy + 44, ox + xl - 20, oy + 44, BLACK, 4, 15)
    ctext(d, ox + xl / 2, oy + 62, "q = lambda*dT/L (高温->低温)", FT)
    note(d, "定常では温度は直線分布, 熱流束 q は板厚内で一定")
    save(im, "s1e7Fourier")


# ============================================================
# 7-3 s1e7ThermalDiff : 温度伝導率 kappa=lambda/(rho c)
# ============================================================
def thermal_diff():
    im, d = new(); title(d, "温度伝導率 (熱拡散率)  kappa = lambda / (rho*c)")
    # 分数表示
    cx = 300
    ctext(d, cx, 150, "lambda", F, BLUE)
    d.line((cx - 90, 175, cx + 90, 175), fill=BLACK, width=3)
    ctext(d, cx, 200, "rho * c", F, GREEN)
    ctext(d, cx - 150, 175, "kappa =", F)
    # 注記(意味)
    arrow(d, cx + 100, 150, cx + 200, 130, BLUE, 2, 10)
    ctext(d, cx + 205, 128, "熱伝導率", FT, BLUE, "lm")
    arrow(d, cx + 100, 200, cx + 200, 230, GREEN, 2, 10)
    ctext(d, cx + 205, 232, "密度x比熱 = 熱容量", FT, GREEN, "lm")
    ctext(d, W / 2, 300, "単位: (W/mK) / ((kg/m3)(J/kgK)) = m^2/s", FT, GRAY)
    ctext(d, W / 2, 330, "kappa が大きいほど温度変化が速く広がる", FT, GRAY)
    note(d, "非定常解析には lambda だけでなく密度 rho と比熱 c も必要")
    save(im, "s1e7ThermalDiff")


# ============================================================
# 7-4 s1e7BoundaryCond : 境界条件4種
# ============================================================
def boundary_cond():
    im, d = new(); title(d, "熱伝導の境界条件 4種")
    # 中央の物体
    x0, x1, y0, y1 = 250, 410, 150, 300
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2, "物体", FT, GRAY)
    # 上: 温度規定
    arrow(d, (x0 + x1) / 2, 100, (x0 + x1) / 2, y0 - 4, BLUE, 2, 10)
    ctext(d, (x0 + x1) / 2, 84, "温度規定  T = Tbar", FT, BLUE)
    # 右: 熱流束規定 / 断熱
    arrow(d, x1 + 4, (y0 + y1) / 2, x1 + 120, (y0 + y1) / 2, GREEN, 2, 10)
    ctext(d, x1 + 126, (y0 + y1) / 2 - 12, "熱流束規定 q=qbar", FT, GREEN, "lm")
    ctext(d, x1 + 126, (y0 + y1) / 2 + 8, "(qbar=0 で断熱)", FT, GREEN, "lm")
    # 下: 熱伝達
    arrow(d, (x0 + x1) / 2, y1 + 4, (x0 + x1) / 2, y1 + 60, ORANGE, 2, 10)
    ctext(d, (x0 + x1) / 2, y1 + 78, "熱伝達  q = h(T - Tf)", FT, ORANGE)
    # 左: ふく射
    arrow(d, x0 - 4, (y0 + y1) / 2, x0 - 120, (y0 + y1) / 2, RED, 2, 10)
    ctext(d, x0 - 126, (y0 + y1) / 2 - 12, "ふく射", FT, RED, "rm")
    ctext(d, x0 - 126, (y0 + y1) / 2 + 8, "q=eps*sigma*F(T^4-Tr^4)", FT, RED, "rm")
    note(d, "ふく射だけが絶対温度の4乗差 T^4-Tr^4 に比例(非線形)")
    save(im, "s1e7BoundaryCond")


# ============================================================
# 7-5 s1e7HeatEquation : 非定常熱伝導方程式と必要入力
# ============================================================
def heat_equation():
    im, d = new(); title(d, "非定常熱伝導方程式  dT/dt = kappa * grad^2 T")
    d.rectangle((150, 90, 510, 140), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 115, "dT/dt = kappa * grad^2 T", F)
    ctext(d, 120, 180, "解を得るのに必要な入力:", FS, BLACK, "lm")
    items = ["1) 初期温度分布 (初期条件)  <- 時間項があるため必須",
             "2) 境界条件 (温度規定 / 熱流束 / 熱伝達 / ふく射)",
             "3) 物性値 rho (密度), c (比熱), lambda (熱伝導率)"]
    for i, s in enumerate(items):
        node(d, 135, 220 + i * 40, 5, fill=BLUE, col=BLUE)
        ctext(d, 150, 220 + i * 40, s, FT, BLACK, "lm")
    note(d, "時間が十分経つと dT/dt->0 となり定常状態に収束する")
    save(im, "s1e7HeatEquation")


# ============================================================
# 7-6 s1e7SeriesSolution : 過渡->定常(直線)への収束
# ============================================================
def series_solution():
    im, d = new(); title(d, "1次元非定常解: 過渡項が消え定常(直線)に近づく")
    ox, oy, xl, yl = 100, 340, 470, 250
    axes(d, ox, oy, xl, yl, "x (0 -> l)", "T")
    def Y(v): return oy - v * yl        # v: 0..1
    T1, T2 = 0.85, 0.15                 # 端点温度(正規化)
    # 定常直線 T1 + (T2-T1)x/l
    plot(d, 0, 0, [(ox, Y(T1)), (ox + xl, Y(T2))], RED, 3)
    ctext(d, ox + xl - 10, Y(T2) - 16, "定常項(直線) t->inf", FT, RED, "rm")
    # 過渡: 初期の膨らみが時間経過で減衰(t 小 -> 大)
    for k, (bump, col) in enumerate([(0.42, GRAY), (0.26, LGRAY), (0.13, (170, 190, 220))]):
        pts = []
        for i in range(61):
            t = i / 60
            base = T1 + (T2 - T1) * t
            yv = base + bump * math.sin(math.pi * t)
            pts.append((ox + xl * t, Y(yv)))
        plot(d, 0, 0, pts, col, 2)
    ctext(d, ox + xl * 0.5, Y(T1 + 0.42), "t 小", FT, GRAY)
    arrow(d, ox + 250, Y(0.75), ox + 250, Y(0.52), BLUE, 2, 9)
    ctext(d, ox + 300, Y(0.63), "過渡項 exp(-kappa n^2 pi^2 t/l^2) で減衰", FT, BLUE, "lm")
    note(d, "t->inf で過渡項(exp)が消え, 定常の直線分布が残る")
    save(im, "s1e7SeriesSolution")


# ============================================================
# 7-7 s1e7ThetaMethod : theta法の評価点と安定性
# ============================================================
def theta_method():
    im, d = new(); title(d, "theta法: 時刻 t = tn + theta*dt で評価")
    y = 150
    x0, x1 = 130, 530
    arrow(d, 90, y, 590, y, BLACK, 2, 11); ctext(d, 600, y, "t", FS, BLACK, "lm")
    d.line((x0, y - 7, x0, y + 7), fill=BLACK, width=2); ctext(d, x0, y + 24, "tn", FT, GRAY)
    d.line((x1, y - 7, x1, y + 7), fill=BLACK, width=2); ctext(d, x1, y + 24, "tn+1", FT, GRAY)
    pts = [(x0, "theta=0", BLUE), ((x0 + x1) / 2, "theta=1/2", GREEN), (x1, "theta=1", RED)]
    for px, lab, col in pts:
        node(d, px, y, 7, fill=col, col=col)
        ctext(d, px, y - 24, lab, FT, col)
    # 表
    ty = 230
    rows = [("theta = 0", "前進差分 (陽解法)", "条件付き安定", BLUE),
            ("theta = 1/2", "クランク・ニコルソン", "無条件安定", GREEN),
            ("theta = 1", "後退差分 (陰解法)", "無条件安定", RED)]
    for i, (a, b, c, col) in enumerate(rows):
        yy = ty + i * 44
        ctext(d, 130, yy, a, FT, col, "lm")
        ctext(d, 280, yy, b, FT, BLACK, "lm")
        ctext(d, 470, yy, c, FT, GRAY, "lm")
    note(d, "theta<1/2 (前進差分) のみ条件付き安定, theta>=1/2 は無条件安定")
    save(im, "s1e7ThetaMethod")


# ============================================================
# 7-8 s1e7StabilityLimit : 前進差分の安定限界 dt
# ============================================================
def stability_limit():
    im, d = new(); title(d, "前進差分の安定限界  kappa*dt/delta^2 <= 1/2")
    # 20分割の棒
    x0, x1, y = 80, 580, 130
    n = 20
    d.rectangle((x0, y - 18, x1, y + 18), outline=BLACK, width=3, fill=FILL1)
    for i in range(1, n):
        xx = x0 + (x1 - x0) * i / n
        d.line((xx, y - 18, xx, y + 18), fill=GRAY, width=1)
    dim(d, x0, y + 44, x0 + (x1 - x0) / n, y + 44, "delta=0.05", col=GRAY)
    ctext(d, (x0 + x1) / 2, y - 40, "l = 1 を 20要素に等分割, kappa = 1", FT, GRAY)
    # 導出
    lines = ["安定条件:  kappa*dt / delta^2 <= 1/2",
             "dt について解く:  dt <= delta^2 / (2*kappa)",
             "dt <= 0.05^2 / (2*1) = 0.0025 / 2 = 0.00125"]
    for i, s in enumerate(lines):
        ctext(d, W / 2, 230 + i * 40, s, FS, BLACK if i < 2 else RED)
    note(d, "安定な dt は要素長さの2乗に比例(細かくすると dt は急減)")
    save(im, "s1e7StabilityLimit")


# ============================================================
# 7-9 s1e7StabAccuracy : 安定性 != 精度
# ============================================================
def stab_accuracy():
    im, d = new(); title(d, "安定性(発散しない) と 精度(真の解に近い) は別")
    ox, oy, xl, yl = 100, 330, 480, 230
    axes(d, ox, oy, xl, yl, "t", "T")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    # 解析解(真の解): なめらかな指数減衰
    exact = [(X(i / 100), Y(0.9 * math.exp(-2.2 * i / 100))) for i in range(101)]
    plot(d, 0, 0, exact, GRAY, 3)
    ctext(d, X(0.55), Y(0.9 * math.exp(-2.2 * 0.55)) - 16, "解析解 (真の解)", FT, GRAY, "lm")
    # 数値解(dt 大): 安定だが粗く真の解から外れる(折れ線)
    ts = [0, 0.18, 0.36, 0.54, 0.72, 0.9]
    num = []
    for k, t in enumerate(ts):
        v = 0.9 * math.exp(-2.2 * t) + (0.14 if k % 2 else -0.10) * math.exp(-1.0 * t)
        num.append((X(t), Y(max(v, 0))))
    plot(d, 0, 0, num, RED, 2)
    for p in num: node(d, p[0], p[1], 4, fill=RED, col=RED)
    ctext(d, X(0.5), Y(0.42), "数値解 dt大: 安定だが不正確", FT, RED, "lm")
    note(d, "無条件安定でも精度確保には dt を小さくとる必要がある")
    save(im, "s1e7StabAccuracy")


# ============================================================
# 7-10 s1e7SteadyLimit : 非定常 vs 定常
# ============================================================
def steady_limit():
    im, d = new(); title(d, "非定常 と 定常 の違い")
    # 左: 非定常
    d.rectangle((60, 100, 300, 320), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 180, 122, "非定常 (non-steady)", FS, BLUE)
    for i, s in enumerate(["時間項あり  dT/dt", "dT/dt = kappa*grad^2 T", "初期条件 必要",
                            "rho, c も必要"]):
        ctext(d, 180, 160 + i * 38, s, FT)
    # 右: 定常
    d.rectangle((360, 100, 600, 320), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 480, 122, "定常 (steady)", FS, RED)
    for i, s in enumerate(["時間項なし", "grad^2 T = 0", "初期条件 不要",
                            "lambda のみでよい"]):
        ctext(d, 480, 160 + i * 38, s, FT)
    # 矢印
    arrow(d, 300, 210, 360, 210, BLACK, 3, 13)
    ctext(d, 330, 190, "dT/dt=0", FT, GRAY)
    note(d, "非定常式で時間項を 0 とおくと定常式になる")
    save(im, "s1e7SteadyLimit")


# ============================================================
# 7-11 s1e7HollowCylinder : 中空円筒と昇温時の応力ピーク
# ============================================================
def hollow_cylinder():
    im, d = new(); title(d, "中空円筒: 速い昇温で内面応力が昇温終了時にピーク")
    # 左: 断面(同心円)
    cx, cy = 175, 220
    d.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - 45, cy - 45, cx + 45, cy + 45), outline=BLACK, width=3, fill="white")
    dim(d, cx, cy, cx + 45, cy, "a", col=GRAY)
    dim(d, cx, cy - 60, cx, cy - 100, "b", col=GRAY)
    ctext(d, cx, cy, "内面 h1", FT, RED)
    ctext(d, cx, cy - 118, "外面 h2", FT, BLUE)
    # 内面から外へ 温度こう配矢印
    for ang in (30, 150, 270):
        a = math.radians(ang)
        arrow(d, cx + 45 * math.cos(a), cy - 45 * math.sin(a),
              cx + 95 * math.cos(a), cy - 95 * math.sin(a), ORANGE, 2, 9)
    # 右: 周方向応力の時間変化
    ox, oy, xl, yl = 380, 330, 230, 210
    axes(d, ox, oy, xl, yl, "時間 t", "内面 応力")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    # 速い昇温: 昇温終了(t=0.5)でピーク後 減衰
    fast = []
    for i in range(101):
        t = i / 100
        v = (1.0 * (t / 0.5)) if t <= 0.5 else (1.0 * math.exp(-3.0 * (t - 0.5)) + 0.15)
        fast.append((X(t), Y(min(v, 1.0))))
    plot(d, 0, 0, fast, RED, 3)
    dashed(d, X(0.5), oy, X(0.5), Y(1.0), LGRAY, 1, 5, 4)
    ctext(d, X(0.5), Y(1.0) - 12, "ピーク(昇温終了)", FT, RED)
    ctext(d, X(0.85), Y(0.2), "定常応力", FT, GRAY)
    note(d, "速い昇温は内面近傍に急な温度こう配->過渡ピークが定常より大きい")
    save(im, "s1e7HollowCylinder")


# ============================================================
# 7-12 s1e7FemHeat : FEM 非定常熱伝導の要素方程式
# ============================================================
def fem_heat():
    im, d = new(); title(d, "FEM 非定常熱伝導  [C]{dT/dt} + [K]{T} = {F}")
    d.rectangle((120, 100, 540, 155), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 128, "[C]{dT/dt} + [K]{T} = {F}", F)
    # 各項の注記
    ctext(d, 200, 200, "[C]", F, BLUE); ctext(d, 200, 226, "熱容量", FT, BLUE)
    ctext(d, 340, 200, "[K]", F, GREEN); ctext(d, 340, 226, "熱伝導", FT, GREEN)
    ctext(d, 470, 200, "{F}", F, ORANGE); ctext(d, 470, 226, "熱流束", FT, ORANGE)
    # 定常への移行
    arrow(d, 330, 265, 330, 300, BLACK, 3, 12)
    ctext(d, 430, 282, "dT/dt = 0 とおく", FT, GRAY, "lm")
    d.rectangle((220, 310, 440, 355), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 332, "定常  [K]{T} = {F}", FS, RED)
    note(d, "時間項を 0 にすると定常式になる(FEM は定常も非定常も統一的に扱える)")
    save(im, "s1e7FemHeat")


# ============================================================
# 7-13 s1e7CapConductMat : 熱容量 と 熱伝導 マトリクスの構成
# ============================================================
def cap_conduct_mat():
    im, d = new(); title(d, "熱容量[c] と 熱伝導[k] マトリクスの構成物性")
    # 左: 熱容量
    d.rectangle((60, 110, 315, 320), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 187, 135, "熱容量 [c]", FS, BLUE)
    ctext(d, 187, 175, "[c] = int rho*c [N]^T[N] dV", FT)
    ctext(d, 187, 220, "含む物性: rho (密度)", FT, GRAY)
    ctext(d, 187, 246, "c (比熱)", FT, GRAY)
    ctext(d, 187, 288, "-> 非定常項(時間変化)", FT, BLUE)
    # 右: 熱伝導
    d.rectangle((345, 110, 600, 320), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 472, 135, "熱伝導 [k]", FS, GREEN)
    ctext(d, 472, 175, "[k] = int lambda (dN/dx..) dV", FT)
    ctext(d, 472, 220, "含む物性: lambda (熱伝導率)", FT, GRAY)
    ctext(d, 472, 246, "+ 形状関数の空間微分", FT, GRAY)
    ctext(d, 472, 288, "-> 空間の温度こう配", FT, GREEN)
    note(d, "[c]=rho*c(時間変化), [k]=lambda と微分(空間こう配) と物性が対応")
    save(im, "s1e7CapConductMat")


# ============================================================
# 7-14 s1e7Nonlinear : 非線形伝熱の要因と解法
# ============================================================
def nonlinear():
    im, d = new(); title(d, "伝熱問題が非線形になる要因 と 解法")
    ctext(d, 175, 90, "非線形の2要因", FS, RED)
    d.rectangle((60, 115, 310, 175), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 185, 145, "1) 温度依存物性 lambda(T)", FT)
    d.rectangle((60, 190, 310, 250), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 185, 220, "2) ふく射の T^4", FT)
    ctext(d, 485, 90, "解法", FS, GREEN)
    d.rectangle((360, 115, 610, 175), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 485, 145, "反復計算で収束させる", FT)
    d.rectangle((360, 190, 610, 250), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 485, 213, "非線形定常は非定常を", FT)
    ctext(d, 485, 233, "長時間回して定常解を得る", FT)
    note(d, "非線形問題は一発では解けず反復計算が必要")
    save(im, "s1e7Nonlinear")


# ============================================================
# 7-15 s1e7LambdaTdep : lambda一定=直線 / lambda増加=上に凸
# ============================================================
def lambda_tdep():
    im, d = new(); title(d, "平面壁の定常温度分布 (熱流束 q は一定)")
    ox, oy, xl, yl = 110, 340, 460, 250
    axes(d, ox, oy, xl, yl, "x (hot -> cold)", "T")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl     # v:0(cold)..1(hot)
    ctext(d, X(0.05), Y(1.0) + 16, "hot", FT, RED, "lm")
    ctext(d, X(0.95), Y(0.0) - 14, "cold", FT, BLUE, "rm")
    # (A) lambda 一定 -> 直線
    plot(d, 0, 0, [(X(0), Y(1.0)), (X(1), Y(0.0))], BLUE, 3)
    ctext(d, X(0.62), Y(0.30), "(A) lambda 一定 = 直線", FT, BLUE, "lm")
    # (B) lambda 温度とともに増加 -> 上に凸(高温側で傾き緩)
    pts = []
    for i in range(101):
        t = i / 100
        # 上に凸: 高温側(左)でなだらか, 低温側(右)で急
        v = math.sqrt(max(1 - t, 0))   # 上に凸の曲線
        pts.append((X(t), Y(v)))
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, X(0.30), Y(0.90), "(B) lambda 増加 = 上に凸", FT, RED, "lm")
    ctext(d, X(0.12), Y(0.78), "高温側は傾き緩", FT, GRAY, "lm")
    note(d, "q 一定, lambda 大 -> 温度こう配 小. 高温側で lambda 大なら傾き緩(上に凸)")
    save(im, "s1e7LambdaTdep")


# ============================================================
# 7-16 s1e7StefanBoltz : ステファン・ボルツマン と 灰色体
# ============================================================
def stefan_boltz():
    im, d = new(); title(d, "ふく射: 黒体 Eb=sigma*T^4, 灰色体 E=eps*sigma*T^4")
    # 左: 高温体
    massblock(d, 150, 200, 90, 130, "", fill=(250, 225, 225))
    ctext(d, 150, 135, "高温 T", FT, RED)
    ctext(d, 150, 200, "Eb = sigma*T^4", FT)
    # ふく射(真空を越える)
    for yy in (175, 200, 225):
        wavy_arrow(d, 205, yy, 455, amp=6, waves=6, col=ORANGE, wd=2)
    ctext(d, 330, 148, "vacuum OK (媒体不要)", FT, GRAY)
    # 右: 低温体
    massblock(d, 510, 200, 90, 130, "", fill=(225, 230, 250))
    ctext(d, 510, 135, "低温 Tr", FT, BLUE)
    ctext(d, 510, 200, "灰色体", FT)
    ctext(d, 510, 224, "E=eps*sigma*T^4", FT)
    ctext(d, W / 2, 300, "放射率 eps < 1,  キルヒホッフの法則 eps = alpha", FT, GRAY)
    note(d, "T^4 に比例(温度2倍で16倍). ふく射は真空でも起こる")
    save(im, "s1e7StefanBoltz")


# ============================================================
# 7-17 s1e7GrayPlates : 平行2灰色体面 と 係数 f
# ============================================================
def gray_plates():
    im, d = new(); title(d, "平行2灰色体面のふく射  Q = f*sigma(T1^4 - T2^4)")
    # 2枚の平板
    d.rectangle((120, 110, 145, 320), outline=BLACK, width=3, fill=(250, 225, 225))
    d.rectangle((515, 110, 540, 320), outline=BLACK, width=3, fill=(225, 230, 250))
    ctext(d, 132, 92, "面1", FT, RED); ctext(d, 527, 92, "面2", FT, BLUE)
    ctext(d, 132, 336, "T1, eps1", FT, RED); ctext(d, 527, 336, "T2, eps2", FT, BLUE)
    # 多重反射(ジグザグ)
    zig = [(148, 150)]
    xs = [148, 512]
    ys = [150, 190, 230, 270]
    seq = [(148, 150), (512, 175), (148, 205), (512, 235), (148, 265), (512, 290)]
    for i in range(len(seq) - 1):
        arrow(d, seq[i][0], seq[i][1], seq[i + 1][0], seq[i + 1][1], ORANGE, 2, 9)
    ctext(d, 330, 130, "多重反射", FT, GRAY)
    # 係数 f
    d.rectangle((210, 200, 450, 260), outline=BLACK, width=2, fill=FILL2)
    ctext(d, 330, 230, "f = 1 / (1/eps1 + 1/eps2 - 1)", FT)
    note(d, "両面とも黒体(eps=1)なら f=1(黒体の式に一致). 放射率が小さいほど f 小")
    save(im, "s1e7GrayPlates")


# ============================================================
# 7-18 s1e7RadShield : 放射シールドで伝熱半減
# ============================================================
def rad_shield():
    im, d = new(); title(d, "放射シールド: 薄板1枚で伝熱量が半分  Q* = Q/2")
    # 面1, 薄板, 面2
    d.rectangle((110, 120, 132, 300), outline=BLACK, width=3, fill=(250, 225, 225))
    d.rectangle((320, 120, 335, 300), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((520, 120, 542, 300), outline=BLACK, width=3, fill=(225, 230, 250))
    ctext(d, 121, 104, "面1 T1", FT, RED)
    ctext(d, 327, 104, "薄板(shield)", FT, GRAY)
    ctext(d, 531, 104, "面2 T2", FT, BLUE)
    ctext(d, 121, 314, "eps", FT, GRAY); ctext(d, 327, 314, "eps", FT, GRAY); ctext(d, 531, 314, "eps", FT, GRAY)
    # ふく射矢印
    for yy in (170, 210, 250):
        wavy_arrow(d, 135, yy, 318, amp=5, waves=4, col=ORANGE, wd=2)
        wavy_arrow(d, 338, yy, 518, amp=5, waves=4, col=ORANGE, wd=2)
    # 直列抵抗のイメージ
    ctext(d, 225, 340, "抵抗1", FT, GRAY); ctext(d, 428, 340, "抵抗2 (直列)", FT, GRAY)
    note(d, "放射率が皆等しいとき N枚で伝熱量は 1/(N+1). 1枚で Q*=Q/2=300 W/m2")
    save(im, "s1e7RadShield")


# ============================================================
# 7-19 s1e7ViewFactor : 形態係数 と 相反則
# ============================================================
def view_factor():
    im, d = new(); title(d, "形態係数 と 相反則  A1*F12 = A2*F21")
    # 面1(大) と 面2(小)
    d.rectangle((110, 120, 135, 320), outline=BLACK, width=3, fill=FILL1)   # A1=4 大
    d.rectangle((525, 170, 545, 270), outline=BLACK, width=3, fill=FILL2)   # A2=2 小
    ctext(d, 122, 104, "面1 A1=4", FT); ctext(d, 535, 154, "面2 A2=2", FT)
    ctext(d, 122, 336, "E1=500 W/m2", FT, GRAY)
    for yy in (170, 210, 250):
        arrow(d, 140, yy, 522, yy - (yy - 220) * 0.15, ORANGE, 2, 9)
    ctext(d, 330, 132, "Q12 = 300 W", FT, GRAY)
    # 計算
    lines = ["F12 = Q12 / (A1*E1) = 300 / (4*500) = 0.15",
             "相反則:  A1*F12 = A2*F21",
             "F21 = A1*F12 / A2 = (4*0.15)/2 = 0.30"]
    for i, s in enumerate(lines):
        ctext(d, W / 2, 300 + i * 30, s, FT, BLACK if i < 2 else RED)
    note(d, "面積で F12 != F21 だが A*F は両向きで等しい(相反則)")
    save(im, "s1e7ViewFactor")


# ============================================================
# 7-20 s1e7BiotNumber : ビオ数 Bi=hL/lambda
# ============================================================
def biot_number():
    im, d = new(); title(d, "ビオ数  Bi = h*L / lambda")
    ctext(d, W / 2, 78, "内部の熱伝導 lambda/L  vs  表面の熱伝達 h の比", FT, GRAY)
    # 左: Bi 小 -> 温度一様
    cx = 190
    d.rectangle((cx - 70, 130, cx + 70, 250), outline=BLACK, width=3, fill=FILL1)
    for yy in range(140, 250, 22):
        d.line((cx - 68, yy, cx + 68, yy), fill=(235, 235, 235), width=1)
    arrow(d, cx - 110, 190, cx - 72, 190, ORANGE, 2, 9); ctext(d, cx - 120, 190, "h", FT, ORANGE, "rm")
    ctext(d, cx, 190, "温度ほぼ一様", FT, BLUE)
    ctext(d, cx, 270, "Bi << 1", FS, BLUE)
    # 右: Bi 大 -> 温度こう配大
    cx = 470
    d.rectangle((cx - 70, 130, cx + 70, 250), outline=BLACK, width=3, fill=FILL1)
    # 濃淡グラデ(左濃->右薄)を縦線密度で表現
    for i in range(14):
        xx = cx - 66 + i * 9.4
        g = int(120 + i * 9)
        d.line((xx, 132, xx, 248), fill=(g, g, g), width=2)
    arrow(d, cx - 110, 190, cx - 72, 190, ORANGE, 2, 9); ctext(d, cx - 120, 190, "h", FT, ORANGE, "rm")
    ctext(d, cx, 190, "温度こう配 大", FT, RED)
    ctext(d, cx, 270, "Bi >> 1", FS, RED)
    ctext(d, W / 2, 320, "例: h=100, L=0.05, lambda=20 -> Bi = 5/20 = 0.25 (小さめ)", FT, GRAY)
    note(d, "Bi 小=物体内ほぼ一様, Bi 大=物体内に温度こう配ができる")
    save(im, "s1e7BiotNumber")


# ============================================================
if __name__ == "__main__":
    three_modes()
    fourier()
    thermal_diff()
    boundary_cond()
    heat_equation()
    series_solution()
    theta_method()
    stability_limit()
    stab_accuracy()
    steady_limit()
    hollow_cylinder()
    fem_heat()
    cap_conduct_mat()
    nonlinear()
    lambda_tdep()
    stefan_boltz()
    gray_plates()
    rad_shield()
    view_factor()
    biot_number()
    print("done ch7")
