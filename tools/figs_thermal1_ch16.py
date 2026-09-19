# -*- coding: utf-8 -*-
"""熱流体力学1級 第16章「結果の検証と妥当性確認」の図(t1e16*・t1f16*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(sigma, Delta p, Delta t, Delta x, rho, nu, alpha, R_0, r^p, sqrt, <=, ^3 等)。
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


def dotline(d, x1, y1, x2, y2, col=GRAY, wd=2, dot=2, gap=7):
    dashed(d, x1, y1, x2, y2, col, wd, dot, gap)


def pcircle(d, x, y, r, fill=FILL1, col=BLACK, wd=2):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wd, fill=fill)


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


# ============================================================
# ============  問題図  t1e16*  (10)  ========================
# ============================================================

# 16-1 t1e16VandVLoop : V&V の関係(helpful)
def vandv_loop():
    im, d = new(); title(d, "V&V の関係: Verification と Validation")
    # 上段: 数理モデル -> 離散化 -> 数値解 (Verification)
    box(d, 60, 95, 230, 150, (225, 235, 250))
    ctext(d, 145, 115, "数理モデル", FT, BLUE); ctext(d, 145, 135, "(支配方程式)", FT, BLUE)
    box(d, 290, 95, 400, 150, FILL1); ctext(d, 345, 122, "離散化", FT)
    box(d, 460, 95, 630, 150, (225, 235, 250))
    ctext(d, 545, 122, "数値解", FT, BLUE)
    arrow(d, 230, 122, 288, 122, BLACK, 3, 11)
    arrow(d, 400, 122, 458, 122, BLACK, 3, 11)
    # Verification の矢印(数値解 <-> 数理モデル)
    d.line((60, 175, 630, 175), fill=LGRAY, width=1)
    arrow(d, 545, 152, 545, 200, BLUE, 3, 12)
    arrow(d, 145, 200, 145, 152, BLUE, 3, 12)
    ctext(d, 345, 205, "Verification(検証): 支配方程式の解 <-> 数値解", FT, BLUE)
    ctext(d, 345, 228, "『方程式を正しく解いているか』(数学)", FT, GRAY)
    # 下段: 実在の物理現象 <-> 計算結果 (Validation)
    box(d, 60, 270, 300, 330, (225, 245, 230))
    ctext(d, 180, 290, "実在の物理現象", FT, GREEN); ctext(d, 180, 312, "(実験・実測)", FT, GREEN)
    box(d, 390, 270, 630, 330, (225, 245, 230))
    ctext(d, 510, 300, "計算結果", FT, GREEN)
    arrow(d, 300, 292, 388, 292, GREEN, 3, 12)
    arrow(d, 388, 312, 300, 312, GREEN, 3, 12)
    ctext(d, 345, 352, "Validation(妥当性確認): 物理現象 <-> 計算結果 『正しい方程式を解いているか』(物理)", FT, GREEN)
    note(d, "左=方程式を正しく解く(Verification), 右=正しい方程式を解く(Validation)")
    save(im, "t1e16VandVLoop")


# 16-2 t1e16LaplaceBubble : 静止気泡のラプラス圧(required・数値なし)
def laplace_bubble():
    im, d = new(); title(d, "液中に静止した球形気泡(単一の気液界面)")
    # 液体背景
    d.rectangle((90, 80, 570, 380), outline=LGRAY, width=1)
    for yy in range(100, 380, 30):
        d.line((92, yy, 568, yy), fill=(235, 240, 247), width=1)
    ctext(d, 130, 95, "液体", FT, GRAY)
    cx, cy, R = 330, 235, 95
    # 気泡(界面1枚)
    pcircle(d, cx, cy, R, (250, 250, 250), BLUE, 3)
    ctext(d, cx, cy - 22, "気泡(気相)", FT, BLUE)
    ctext(d, cx, cy + 4, "界面は1枚", FT, GRAY)
    ctext(d, cx, cy + 26, "(単一の気液界面)", FT, GRAY)
    # 半径R
    arrow(d, cx, cy, cx + R * math.cos(math.radians(-35)), cy - R * math.sin(math.radians(-35)), BLACK, 2, 10)
    ctext(d, cx + 45, cy + 30, "R", FS, BLACK)
    # 表面張力 sigma(界面接線方向)
    ang = math.radians(120)
    tx, ty = cx + R * math.cos(ang), cy - R * math.sin(ang)
    arrow(d, tx, ty, tx - 34, ty - 20, GREEN, 2, 9)
    arrow(d, tx, ty, tx + 20, ty + 34, GREEN, 2, 9)
    ctext(d, tx - 40, ty - 34, "表面張力 sigma", FT, GREEN, "mm")
    # 内圧 p_in / 外圧 p_out
    ctext(d, cx, cy - 55, "p_in(気泡内圧)", FT, RED)
    arrow(d, 560, 130, 500, 175, RED, 2, 10)
    ctext(d, 560, 118, "p_out(外部液圧)", FT, RED, "mm")
    note(d, "半径R・表面張力sigma・内圧p_in・外圧p_outの関係を問う(数値は各自)")
    save(im, "t1e16LaplaceBubble")


# 16-3 t1e16InterfaceCourant : 界面のクーラン数(required・dt数値なし)
def interface_courant():
    im, d = new(); title(d, "界面を横切る格子とクーラン数  C = u Delta t / Delta x")
    # 格子セル1枚
    x0, y0, w, h = 210, 130, 240, 150
    box(d, x0, y0, x0 + w, y0 + h, "white", 3)
    dim(d, x0, y0 - 24, x0 + w, y0 - 24, "Delta x (格子幅)", col=GRAY)
    # 界面(縦線)が時間ステップで uΔt 進む
    xi0 = x0 + 60
    xi1 = x0 + 150
    d.line((xi0, y0 - 4, xi0, y0 + h + 4), fill=BLUE, width=3)
    ctext(d, xi0 - 6, y0 + h + 20, "界面(t)", FT, BLUE, "mm")
    dashed(d, xi1, y0 - 4, xi1, y0 + h + 4, BLUE, 3, 8, 5)
    ctext(d, xi1 + 30, y0 + h + 20, "界面(t+Delta t)", FT, BLUE, "mm")
    # 速度uで距離uΔt進む
    arrow(d, xi0, y0 + h / 2, xi1, y0 + h / 2, RED, 3, 12)
    ctext(d, (xi0 + xi1) / 2, y0 + h / 2 - 18, "u Delta t", FT, RED)
    ctext(d, (xi0 + xi1) / 2, y0 - 4, "速度 u", FT, RED)
    # 定義と目安
    box(d, 120, 320, 540, 372, FILL2)
    ctext(d, 330, 336, "C = u Delta t / Delta x  = 1ステップで界面が進む距離 / 格子幅", FT)
    ctext(d, 330, 358, "界面捕獲の目安:  C <= 0.3", FS, GREEN)
    note(d, "Cが大きいと界面捕獲精度が落ち界面が振動しやすい(時間刻みの数値は各自)")
    save(im, "t1e16InterfaceCourant")


# 16-4 t1e16BubbleVolumeDrift : 体積ドリフト(helpful)
def bubble_volume_drift():
    im, d = new(); title(d, "上昇する単一気泡の見かけ体積ドリフト(数値誤差)")
    # 液中背景
    for yy in range(90, 380, 28):
        d.line((90, yy, 380, yy), fill=(235, 240, 247), width=1)
    # 下(初期)
    cx1, cy1, R0 = 210, 320, 40
    pcircle(d, cx1, cy1, R0, (250, 250, 250), BLUE, 3)
    arrow(d, cx1, cy1, cx1 + R0, cy1, BLACK, 2, 9); ctext(d, cx1 + 22, cy1 + 18, "R_0", FT)
    ctext(d, cx1, cy1 + R0 + 20, "初期", FT, GRAY)
    # 上(上昇後・わずかに大きい)
    cx2, cy2, R1 = 250, 150, int(40 * 1.18)
    pcircle(d, cx2, cy2, R1, (250, 250, 250), BLUE, 3)
    arrow(d, cx2, cy2, cx2 + R1, cy2, BLACK, 2, 9); ctext(d, cx2 + 26, cy2 + 18, "1.05 R_0", FT, RED)
    ctext(d, cx2, cy2 + R1 + 18, "上昇後", FT, GRAY)
    # 上昇矢印
    arrow(d, 150, 300, 175, 190, GRAY, 2, 11); ctext(d, 135, 245, "上昇", FT, GRAY, "rm")
    # 説明
    box(d, 400, 120, 630, 320, FILL1)
    ctext(d, 515, 145, "非圧縮・定物性値では", FT)
    ctext(d, 515, 170, "体積は一定のはず", FS, BLUE)
    ctext(d, 515, 205, "見かけ半径が増える", FT, RED)
    ctext(d, 515, 230, "= 数値誤差で膨張", FT, RED)
    ctext(d, 515, 268, "体積比 = (R/R_0)^3", FS)
    ctext(d, 515, 296, "半径の3乗で効く", FT, GRAY)
    note(d, "半径のわずかな誤差が3乗されて体積誤差に拡大する")
    save(im, "t1e16BubbleVolumeDrift")


# 16-5 t1e16DampedOscillation : 自由振動の急減衰(required・原因なし)
def damped_oscillation():
    im, d = new(); title(d, "気泡の自由振動(振幅が急激に減衰)")
    ox, oy, xl, yl = 90, 235, 500, 150
    axes(d, ox, oy, xl + 20, yl + 10, "時間 t", "")
    # 縦軸ラベル
    ctext(d, ox - 30, oy - yl - 4, "気泡半径", FT, BLACK, "rm")
    # 平衡線
    dashed(d, ox, oy, ox + xl, oy, GRAY, 1, 6, 5)
    ctext(d, ox + xl + 24, oy, "平衡", FT, GRAY, "lm")
    # 減衰振動波形
    pts = []
    for i in range(0, 501):
        t = i / 500
        env = math.exp(-3.2 * t)
        v = env * math.cos(2 * math.pi * 3.2 * t)
        pts.append((ox + t * xl, oy - v * yl * 0.9))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 減衰包絡線
    env_pts = [(ox + (i / 500) * xl, oy - math.exp(-3.2 * (i / 500)) * yl * 0.9) for i in range(0, 501, 10)]
    dotline_pts = env_pts
    for i in range(len(dotline_pts) - 1):
        dashed(d, dotline_pts[i][0], dotline_pts[i][1], dotline_pts[i + 1][0], dotline_pts[i + 1][1], RED, 2, 6, 5)
    ctext(d, ox + 150, oy - yl * 0.7, "振幅が急激に減衰", FT, RED)
    note(d, "この減衰を招く要因は何か(原因ラベルは各自考える)")
    save(im, "t1e16DampedOscillation")


# 16-6 t1e16FlowSaturation : 流量の頭打ち(required・原因なし)
def flow_saturation():
    im, d = new(); title(d, "圧力差に対する流量特性(与えられた計算結果)")
    ox, oy, xl, yl = 110, 340, 470, 240
    axes(d, ox, oy, xl + 20, yl + 10, "sqrt(Delta p)", "流量 Q")
    # 立ち上がり(直線) -> 頭打ち(プラトー)
    pts = []
    xbreak = 0.45
    qmax = 0.82
    for i in range(0, 501):
        t = i / 500
        if t <= xbreak:
            q = (qmax / xbreak) * t * 0.92
        else:
            q0 = (qmax / xbreak) * xbreak * 0.92
            q = q0 + (qmax - q0) * (1 - math.exp(-(t - xbreak) / 0.12))
        pts.append((ox + t * xl, oy - q * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 頭打ち位置を示す破線
    ybreak = oy - ((qmax / xbreak) * xbreak * 0.92) * yl
    dashed(d, ox, ybreak - 30, ox + xl, ybreak - 30, GRAY, 1, 6, 5)
    ctext(d, ox + xl * 0.75, ybreak - 48, "頭打ち(プラトー)", FT, GRAY)
    ctext(d, ox + xl * 0.18, oy - yl * 0.35, "直線的に増加", FT, GRAY)
    note(d, "ある圧力差を境に流量が頭打ちになる. その原因の解釈を問う(答えは各自)")
    save(im, "t1e16FlowSaturation")


# 16-7 t1e16WallTempProfile : 内壁温度分布(required・相関式名なし)
def wall_temp_profile():
    im, d = new(); title(d, "加熱鉛直円管の内壁温度の高さ分布(計測)")
    # 横軸=内壁温度, 縦軸=管高さ
    ox, oy, xl, yl = 150, 350, 420, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11); ctext(d, ox + xl + 26, oy, "内壁温度", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11); ctext(d, ox - 12, oy - yl - 12, "管高さ", FS, BLACK, "rm")
    # 折れ線: 下部ほぼ一定 -> 遷移点で急上昇 -> 上部高温
    # 高さ(縦)を下から上へ。温度(横)。
    Tlow = 0.30      # 下部一定温度(横位置)
    Thigh = 0.85     # 上部高温(横位置)
    hbreak = 0.55    # 遷移高さ(縦割合)
    pts = []
    # 下部: 高さ 0..hbreak で温度ほぼ一定
    pts.append((ox + Tlow * xl, oy))
    pts.append((ox + Tlow * xl, oy - hbreak * yl))
    # 遷移: 急上昇(温度が横に急増)
    pts.append((ox + Thigh * xl, oy - (hbreak + 0.06) * yl))
    # 上部: やや上昇しつつ高温
    pts.append((ox + (Thigh + 0.05) * xl, oy - yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 遷移高さの補助線
    dashed(d, ox, oy - hbreak * yl, ox + Thigh * xl, oy - hbreak * yl, GRAY, 1, 6, 5)
    ctext(d, ox + Thigh * xl + 8, oy - (hbreak + 0.03) * yl, "急上昇", FT, RED, "lm")
    ctext(d, ox + Tlow * xl - 8, oy - hbreak * 0.5 * yl, "下部:ほぼ一定", FT, GRAY, "rm")
    ctext(d, ox + Thigh * xl - 6, oy - 0.9 * yl, "上部:高温", FT, GRAY, "rm")
    note(d, "下部一定->ある高さで内壁温度が不連続的に急上昇->上部高温(流動様式名は各自)")
    save(im, "t1e16WallTempProfile")


# 16-8 t1e16ValidationMethods : 検証手法の難易度帯(helpful)
def validation_methods():
    im, d = new(); title(d, "キャビテーション検証手法: 定性(容易) と 定量(困難)")
    # 難易度の帯
    d.rectangle((60, 120, 600, 165), outline=BLACK, width=2, fill=FILL1)
    arrow(d, 70, 142, 590, 142, GRAY, 2, 12)
    ctext(d, 100, 100, "容易(定性)", FT, GREEN)
    ctext(d, 560, 100, "困難(定量)", FT, RED)
    # 左: 定性比較
    box(d, 55, 200, 350, 360, (225, 245, 230))
    ctext(d, 202, 222, "定性的な比較(容易)", FS, GREEN)
    for i, s in enumerate(["流量特性の傾向の一致",
                           "可視化写真とボイド率分布の形状",
                           "PIV速度ベクトルの傾向"]):
        ctext(d, 202, 260 + i * 34, "・" + s, FT)
    # 右: 定量比較
    box(d, 370, 200, 605, 360, (250, 230, 230))
    ctext(d, 487, 222, "定量的な比較(困難)", FS, RED)
    ctext(d, 487, 270, "ボイド率そのものの", FT)
    ctext(d, 487, 298, "数値の一致", FS, RED)
    ctext(d, 487, 332, "不確かさが大きい", FT, GRAY)
    note(d, "傾向・形状の一致は容易, 数値の一致(定量)は困難")
    save(im, "t1e16ValidationMethods")


# 16-9 t1e16GridConvergence : 格子収束(required・GCI値なし)
def grid_convergence():
    im, d = new(); title(d, "格子収束性: 格子を細かくすると収束値へ近づく")
    ox, oy, xl, yl = 110, 340, 470, 240
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11); ctext(d, ox + xl + 26, oy, "格子幅 h", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11); ctext(d, ox - 12, oy - yl - 12, "計算量(例:断面平均ボイド率)", FT, BLACK, "rm")
    # 収束値の水平線
    yconv = oy - 0.30 * yl
    dashed(d, ox, yconv, ox + xl, yconv, GRAY, 1, 7, 5)
    ctext(d, ox + xl + 24, yconv, "収束値", FT, GRAY, "lm")
    # 点列: h 大(粗) -> h 小(細) で収束値に近づく
    hs = [0.85, 0.42, 0.18]   # 粗, 中, 細(格子幅の割合)
    # 収束: 値は h^2 で収束値へ近づく
    for i, h in enumerate(hs):
        val = 0.30 + 0.55 * (h ** 2)   # 収束値0.30に上乗せ
        X = ox + h * xl
        Y = oy - val * yl
        node(d, X, Y, 5, fill=BLUE, col=BLUE)
    # 粗2格子(r=2)を強調: 中(粗) と 細
    lab = ["粗 h", "中 h/2", "細 h/4"]
    for i, h in enumerate(hs):
        val = 0.30 + 0.55 * (h ** 2)
        X = ox + h * xl; Y = oy - val * yl
        ctext(d, X, Y - 20, lab[i], FT, GRAY)
    # 曲線で結ぶ
    cpts = []
    for k in range(0, 101):
        h = 0.05 + (0.9 - 0.05) * k / 100
        val = 0.30 + 0.55 * (h ** 2)
        cpts.append((ox + h * xl, oy - val * yl))
    d.line(cpts, fill=LGRAY, width=2, joint="curve")
    ctext(d, ox + 0.5 * xl, oy - 0.12 * yl, "細分化比 r=2 (粗・細の2格子)", FT, GRAY)
    note(d, "GCI は格子細分化に伴う離散化誤差の目安(GCIの数値は各自)")
    save(im, "t1e16GridConvergence")


# 16-10 t1e16PeriodicChannel : 周期条件と体積変化の矛盾(required・対策なし)
def periodic_channel():
    im, d = new(); title(d, "水平チャネルの周期条件 と 弾性体粒子の体積変化")
    # チャネル(上下壁)
    x0, x1, ytop, ybot = 110, 560, 130, 300
    hwall(d, x0, x1, ytop, side=1, n=15)     # 上壁(下にハッチ)
    hwall(d, x0, x1, ybot, side=-1, n=15)    # 下壁(上にハッチ)
    # 流れ方向(圧力駆動)
    arrow(d, x0 + 30, 215, x0 + 130, 215, RED, 3, 12)
    ctext(d, x0 + 80, 195, "流れ(圧力駆動)", FT, RED)
    ctext(d, x0 + 40, 320, "上流:高圧", FT, GRAY)
    ctext(d, x1 - 40, 320, "下流:低圧", FT, GRAY)
    # 周期境界条件(入口=出口をつなぐ)
    dashed(d, x0, ytop - 4, x0, ybot + 4, BLUE, 2, 8, 5)
    dashed(d, x1, ytop - 4, x1, ybot + 4, BLUE, 2, 8, 5)
    ctext(d, x0, 118, "入口", FT, BLUE); ctext(d, x1, 118, "出口", FT, BLUE)
    d.arc((x0 - 30, 60, x1 + 30, 130), 200, 340, fill=BLUE, width=2)
    ctext(d, (x0 + x1) / 2, 60, "速度に周期境界条件(入口=出口)", FT, BLUE)
    # 弾性体粒子: 上流小 -> 下流ほど膨張
    for i, (px, r) in enumerate([(x0 + 90, 16), (x0 + 210, 20), (x0 + 330, 25), (x0 + 430, 31)]):
        pcircle(d, px, 240, r, FILL1)
    ctext(d, x0 + 90, 275, "小", FT, GRAY); ctext(d, x0 + 430, 280, "膨張", FT, RED)
    ctext(d, (x0 + x1) / 2, 360, "低圧ほど弾性体粒子が膨張 <-> 体積流量一定の周期条件 が両立せず破綻", FT, RED)
    note(d, "体積変化と体積流量一定の周期条件の矛盾を図示(対策は各自)")
    save(im, "t1e16PeriodicChannel")


# ============================================================
# ============  公式・用語カード  t1f16*  (21)  ==============
# ============================================================

# t1f16-1 Verification
def f_verification():
    im, d = new(); title(d, "Verification(検証)= 方程式を正しく解いているか")
    box(d, 60, 90, 600, 150, (225, 235, 250))
    ctext(d, 330, 120, "支配方程式の解  <->  離散化した数値解  の一致を確認", FT, BLUE)
    ctext(d, 330, 185, "『solving the equations RIGHT』(数学の問題)", FS, BLACK)
    for i, s in enumerate(["実験は使わない",
                           "解析解・高精度参照解と比較",
                           "格子収束(GCI)で離散化誤差を同定"]):
        ctext(d, 330, 225 + i * 34, "・" + s, FT)
    note(d, "コード開発時のモデル化・離散化誤差を定量化する作業")
    save(im, "t1f16Verification")


# t1f16-2 Validation
def f_validation():
    im, d = new(); title(d, "Validation(妥当性確認)= 正しい方程式を解いているか")
    box(d, 60, 90, 600, 150, (225, 245, 230))
    ctext(d, 330, 120, "実在の物理現象  <->  計算結果  の一致を実験で確認", FT, GREEN)
    ctext(d, 330, 185, "『solving the RIGHT equations』(物理の問題)", FS, BLACK)
    for i, s in enumerate(["実験・実測との比較が本質",
                           "モデルが実現象をどれだけ再現できるか",
                           "Verification とは対象が異なり補完的"]):
        ctext(d, 330, 225 + i * 34, "・" + s, FT)
    note(d, "可視化写真・PIV・流量傾向の比較. ボイド率の定量一致は難しい")
    save(im, "t1f16Validation")


# t1f16-3 V&V ガイドライン
def f_vandv_guideline():
    im, d = new(); title(d, "V&V ガイドライン(AIAA G-077-1998 等)")
    box(d, 45, 100, 320, 320, (225, 235, 250))
    ctext(d, 182, 128, "Verification", FS, BLUE)
    ctext(d, 182, 165, "= 離散化誤差の同定", FT)
    ctext(d, 182, 195, "(数学)", FT, GRAY)
    ctext(d, 182, 245, "方程式を", FT, BLUE)
    ctext(d, 182, 275, "正しく解く", FS, BLUE)
    box(d, 340, 100, 615, 320, (225, 245, 230))
    ctext(d, 477, 128, "Validation", FS, GREEN)
    ctext(d, 477, 165, "= 実験・現象との一致", FT)
    ctext(d, 477, 195, "(物理)", FT, GRAY)
    ctext(d, 477, 245, "正しい方程式を", FT, GREEN)
    ctext(d, 477, 275, "解く", FS, GREEN)
    note(d, "ISO9000 のソフト品質保証とは別概念. 混同しない")
    save(im, "t1f16VandVGuideline")


# t1f16-4 ラプラス圧
def f_laplace_pressure():
    im, d = new(); title(d, "ラプラス圧(表面張力ベンチマーク)")
    box(d, 170, 95, 490, 155, FILL2)
    ctext(d, 330, 125, "Delta p = 2 sigma / R", F)
    # 気泡の絵
    cx, cy = 160, 270
    pcircle(d, cx, cy, 46, (250, 250, 250), BLUE, 3)
    ctext(d, cx, cy, "sigma, R", FT, BLUE)
    ctext(d, cx, cy + 68, "界面1枚の気泡", FT, GRAY)
    # 右: 要点
    ctext(d, 460, 205, "単一の気液界面: 2 sigma / R", FT)
    ctext(d, 460, 238, "シャボン膜(界面2枚): 4 sigma / R", FT, RED)
    ctext(d, 460, 275, "内外圧力差は表面張力の関数", FT)
    ctext(d, 460, 305, "-> 表面張力モデルの検証に好適", FT, GREEN)
    note(d, "sigma=0.072 N/m, R=1.0 mm なら Delta p=144 Pa(数値解が一致すれば離散化が正しい)")
    save(im, "t1f16LaplacePressure")


# t1f16-5 表面張力の検証問題の選び方
def f_surface_tension_benchmark():
    im, d = new(); title(d, "表面張力の検証問題の選び方")
    box(d, 45, 100, 320, 350, (225, 245, 230))
    ctext(d, 182, 124, "検証に適する(sigmaの関数)", FS, GREEN)
    for i, s in enumerate(["液柱の振動周期",
                           "液滴の振動周期",
                           "静止球形気泡の内外圧力差",
                           "(ラプラス圧 2 sigma/R)"]):
        col = GRAY if i == 3 else BLACK
        ctext(d, 182, 165 + i * 40, "・" + s if i != 3 else s, FT, col)
    box(d, 340, 100, 620, 350, (250, 230, 230))
    ctext(d, 480, 124, "検証に不向き", FS, RED)
    ctext(d, 480, 170, "液中を上昇する", FT)
    ctext(d, 480, 200, "球形気泡の終端速度", FS)
    ctext(d, 480, 245, "浮力と抗力で決まり", FT, GRAY)
    ctext(d, 480, 275, "sigma に依存しない", FT, RED)
    ctext(d, 480, 312, "(抗力の検証にはなる)", FT, GRAY)
    note(d, "解が表面張力の関数となる問題を選ぶのが要点")
    save(im, "t1f16SurfaceTensionBenchmark")


# t1f16-6 界面捕獲のクーラン数
def f_interface_courant():
    im, d = new(); title(d, "界面捕獲のクーラン数")
    box(d, 150, 95, 510, 155, FILL2)
    ctext(d, 330, 125, "C = u Delta t / Delta x  <=  0.3", F)
    ctext(d, 330, 190, "界面を含む格子の C を 0.3 以下に保つ", FT)
    ctext(d, 330, 225, "C が大きすぎると:", FT, RED)
    for i, s in enumerate(["界面捕獲の精度が落ちる",
                           "計算が不安定化する",
                           "界面が時間ステップごとに細かく振動"]):
        ctext(d, 330, 258 + i * 30, "・" + s, FT, GRAY)
    note(d, "曲率をもつ界面(毛細管現象など)ではとくに注意. Delta t で調整")
    save(im, "t1f16InterfaceCourant")


# t1f16-7 壁面接触角
def f_contact_angle():
    im, d = new(); title(d, "壁面接触角の設定(自由表面計算)")
    # 壁と液面の接触角
    wall(d, 150, 120, 340, side=1, n=8)
    # 液面(接触角60-70度のイメージ)
    d.line((150, 300, 420, 230), fill=BLUE, width=3)
    ctext(d, 430, 225, "液面", FT, BLUE, "lm")
    angle_arc(d, 150, 300, 46, 0, 60, "theta", BLUE)
    ctext(d, 210, 320, "接触角 theta", FT, BLUE)
    # 右: 要点
    box(d, 380, 110, 620, 300, FILL1)
    ctext(d, 500, 135, "水の毛細管現象", FS)
    ctext(d, 500, 172, "theta = 60〜70 度が目安", FT, GREEN)
    ctext(d, 500, 215, "小さすぎる(例0度):", FT, RED)
    ctext(d, 500, 245, "壁近傍で液が過剰に上昇", FT, GRAY)
    ctext(d, 500, 275, "-> 界面が不安定・振動", FT, GRAY)
    note(d, "界面振動の原因: まず時間刻み・接触角・メッシュ解像度を疑う")
    save(im, "t1f16ContactAngle")


# t1f16-8 Level Set法の体積保存誤差
def f_volume_conservation():
    im, d = new(); title(d, "Level Set法の体積保存誤差")
    box(d, 150, 95, 510, 155, FILL2)
    ctext(d, 330, 125, "Delta V / V_0 = (R / R_0)^3 - 1", F)
    ctext(d, 330, 190, "非圧縮・定物性値なら体積(質量)は厳密に保存", FT)
    ctext(d, 330, 222, "体積が変化したら = 数値誤差", FT, RED)
    ctext(d, 330, 255, "(Level Set 関数の再初期化など)", FT, GRAY)
    ctext(d, 330, 295, "半径のわずかな誤差が3乗されて拡大", FT, BLUE)
    note(d, "見かけ半径 1.05 R_0 なら (1.05)^3 - 1 = 約15.8% も体積が増加")
    save(im, "t1f16VolumeConservation")


# t1f16-9 VOF法とLevel Set法の体積保存性
def f_vof_vs_levelset():
    im, d = new(); title(d, "VOF法 と Level Set法 の体積保存性")
    box(d, 45, 100, 320, 350, (225, 245, 230))
    ctext(d, 182, 124, "VOF 法", FS, GREEN)
    ctext(d, 182, 158, "各セルの体積分率を", FT)
    ctext(d, 182, 186, "直接輸送する", FT)
    ctext(d, 182, 228, "体積保存性が高い", FS, GREEN)
    ctext(d, 182, 300, "ほぼ体積一定", FT, GRAY)
    box(d, 340, 100, 620, 350, (250, 230, 230))
    ctext(d, 480, 124, "Level Set 法", FS, BLUE)
    ctext(d, 480, 158, "符号付き距離関数を輸送", FT)
    ctext(d, 480, 186, "距離関数がゆがむため", FT)
    ctext(d, 480, 214, "再初期化を繰り返す", FT)
    ctext(d, 480, 256, "再初期化で体積を失いやすい", FT, RED)
    ctext(d, 480, 300, "体積がじわじわ変化", FT, GRAY)
    note(d, "どちらを使うかで体積保存の検証の重み付けが変わる")
    save(im, "t1f16VofVsLevelSet")


# t1f16-10 GCL
def f_gcl():
    im, d = new(); title(d, "GCL(幾何学的保存則)")
    # 移動格子のイメージ
    x0, y0 = 70, 110
    for j in range(4):
        d.line((x0 + j * 55, y0, x0 + j * 55 + 20, y0 + 140), fill=LGRAY, width=1)
    for i in range(4):
        d.line((x0, y0 + i * 47, x0 + 3 * 55, y0 + i * 47), fill=LGRAY, width=1)
    arrow(d, x0 + 90, y0 + 160, x0 + 140, y0 + 160, GRAY, 2, 10)
    ctext(d, x0 + 90, y0 + 185, "格子が移動・変形", FT, GRAY)
    box(d, 350, 110, 620, 320, FILL1)
    ctext(d, 485, 135, "移動境界の物体適合格子で", FT)
    ctext(d, 485, 165, "格子移動が余計な質量・体積の", FT)
    ctext(d, 485, 193, "生成消滅を生まない条件", FT)
    ctext(d, 485, 235, "ALE法は GCL を満たすよう", FT, GREEN)
    ctext(d, 485, 263, "格子移動を行う", FT, GREEN)
    ctext(d, 485, 298, "破ると質量ドリフト(減衰ではない)", FT, RED)
    note(d, "GCL 違反はただちに振幅の急減衰にはつながらない(減衰の主因は数値粘性)")
    save(im, "t1f16GCL")


# t1f16-11 数値粘性
def f_numerical_viscosity():
    im, d = new(); title(d, "数値粘性(減衰の主因)")
    box(d, 60, 95, 600, 150, FILL2)
    ctext(d, 330, 122, "離散化(風上差分等)・格子の粗さから生じる見かけの粘性", FT)
    # 減衰する波
    ox, oy, xl, yl = 100, 250, 240, 70
    pts = []
    for i in range(0, 241):
        t = i / 240
        v = math.exp(-2.5 * t) * math.cos(2 * math.pi * 3 * t)
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=2, joint="curve")
    ctext(d, ox + xl / 2, oy + 55, "振動・波を実際以上に減衰", FT, BLUE)
    box(d, 380, 185, 620, 320, FILL1)
    ctext(d, 500, 210, "自由振動が急減衰したら", FT)
    ctext(d, 500, 242, "まず疑う:", FT, RED)
    ctext(d, 500, 272, "格子密度不足・差分精度不足", FT)
    ctext(d, 500, 300, "次に過大な物理粘度(桁誤り)", FT, GRAY)
    note(d, "格子を細かく・高次化すると数値粘性は改善する")
    save(im, "t1f16NumericalViscosity")


# t1f16-12 キャビテーションと有効断面積の減少
def f_cavitation_area():
    im, d = new(); title(d, "キャビテーションと有効断面積の減少")
    # 流路と気泡群
    x0, x1, yt, yb = 60, 340, 140, 300
    d.line((x0, yt, x1, yt), fill=BLACK, width=3)
    d.line((x0, yb, x1, yb), fill=BLACK, width=3)
    for (px, py, r) in [(150, 200, 14), (185, 240, 18), (210, 180, 12),
                        (245, 220, 20), (275, 195, 15), (300, 240, 13)]:
        pcircle(d, px, py, r, (235, 242, 250), BLUE, 2)
    arrow(d, 70, 220, 120, 220, RED, 3, 11)
    ctext(d, 200, 120, "気泡群が流路を占める", FT, BLUE)
    ctext(d, 200, 320, "-> 有効断面積が減少", FT, RED)
    # 右: 流量頭打ち
    ox, oy, xl, yl = 400, 320, 190, 200
    axes(d, ox, oy, xl + 15, yl + 10, "sqrt(Delta p)", "流量")
    pts = []
    for i in range(0, 201):
        t = i / 200
        q = 0.8 * (1 - math.exp(-t / 0.28)) if t > 0.35 else (0.8 * (1 - math.exp(-0.35 / 0.28))) / 0.35 * t
        pts.append((ox + t * xl, oy - q * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + xl * 0.6, oy - yl * 0.9, "頭打ち", FT, RED)
    note(d, "圧力差増大でキャビテーション増 -> 有効断面積減 -> 流量が頭打ち(音速超えではない)")
    save(im, "t1f16CavitationArea")


# t1f16-13 流動様式別の伝熱相関式
def f_flow_regime_ht():
    im, d = new(); title(d, "流動様式別の伝熱相関式(加熱二相流)")
    # 縦の管で下から上へ流動様式が変わる
    x0 = 90
    d.rectangle((x0, 90, x0 + 70, 360), outline=BLACK, width=2)
    ctext(d, x0 + 35, 375, "加熱管", FT, GRAY)
    # 下部: 気泡流
    for (py) in [330, 310, 290]:
        pcircle(d, x0 + 35, py, 6, (235, 242, 250), BLUE, 2)
    ctext(d, x0 + 120, 310, "気泡流(核沸騰)", FT, BLUE, "lm")
    # 中部: スラグ流
    pcircle(d, x0 + 35, 240, 20, (235, 242, 250), BLUE, 2)
    ctext(d, x0 + 120, 240, "スラグ流", FT, GREEN, "lm")
    # 沸騰遷移
    dashed(d, x0, 190, x0 + 70, 190, RED, 2, 7, 5)
    ctext(d, x0 + 120, 190, "沸騰遷移(内壁温度が急上昇)", FT, RED, "lm")
    # 上部: 蒸気強制対流
    for py in range(120, 175, 14):
        d.line((x0 + 15, py, x0 + 55, py), fill=(180, 180, 180), width=2)
    ctext(d, x0 + 120, 140, "蒸気単相/液滴を伴う蒸気の強制対流", FT, GRAY, "lm")
    note(d, "流動様式ごとに伝熱相関式を切替. 遷移後の高温域にスラグ流は存在しない")
    save(im, "t1f16FlowRegimeHT")


# t1f16-14 沸騰遷移
def f_boiling_transition():
    im, d = new(); title(d, "沸騰遷移(内壁温度の急上昇)")
    ox, oy, xl, yl = 130, 350, 380, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11); ctext(d, ox + xl + 26, oy, "内壁温度", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11); ctext(d, ox - 12, oy - yl - 12, "管高さ", FS, BLACK, "rm")
    pts = [(ox + 0.30 * xl, oy), (ox + 0.30 * xl, oy - 0.55 * yl),
           (ox + 0.85 * xl, oy - 0.62 * yl), (ox + 0.90 * xl, oy - yl)]
    d.line(pts, fill=BLUE, width=3, joint="curve")
    dashed(d, ox, oy - 0.55 * yl, ox + 0.85 * xl, oy - 0.55 * yl, RED, 1, 6, 5)
    ctext(d, ox + 0.9 * xl, oy - 0.58 * yl, "急上昇", FT, RED, "lm")
    ctext(d, ox + 0.30 * xl - 8, oy - 0.28 * yl, "液膜(下部)", FT, GRAY, "rm")
    ctext(d, ox + 0.7 * xl, oy - 0.92 * yl, "蒸気(上部)", FT, GRAY)
    ctext(d, ox + 0.55 * xl, oy - 0.45 * yl, "沸騰遷移", FT, RED)
    note(d, "壁が液膜->蒸気に移り熱伝達が急に悪化. 急上昇位置を沸騰遷移の相関式が支配")
    save(im, "t1f16BoilingTransition")


# t1f16-15 平均化モデルの保存則モデルと相関式
def f_averaging_model():
    im, d = new(); title(d, "平均化モデル: 保存則モデル と 相関式")
    box(d, 45, 100, 320, 350, (225, 235, 250))
    ctext(d, 182, 126, "保存則モデル", FS, BLUE)
    ctext(d, 182, 160, "(質量・運動量・エネルギー)", FT, GRAY)
    ctext(d, 182, 200, "均質流/多流体モデル", FT)
    ctext(d, 182, 250, "流動様式が変わっても", FT)
    ctext(d, 182, 280, "共通に保つ", FS, BLUE)
    box(d, 340, 100, 620, 350, (225, 245, 230))
    ctext(d, 480, 126, "伝熱相関式・相間相関式", FS, GREEN)
    ctext(d, 480, 172, "気泡流・スラグ流など", FT)
    ctext(d, 480, 210, "流動様式に対応", FT)
    ctext(d, 480, 255, "流動様式の変化に合わせ", FT)
    ctext(d, 480, 285, "切り替える", FS, GREEN)
    note(d, "『保存則モデルは共通, 相関式は流動様式ごと』が切り分けの要点")
    save(im, "t1f16AveragingModel")


# t1f16-16 相間摩擦・相間熱伝達モデル
def f_interfacial_models():
    im, d = new(); title(d, "相間摩擦・相間熱伝達モデル")
    # 2相の間の交換
    pcircle(d, 200, 210, 55, (235, 242, 250), BLUE, 3); ctext(d, 200, 210, "気相", FS, BLUE)
    pcircle(d, 440, 210, 55, (235, 245, 230), GREEN, 3); ctext(d, 440, 210, "液相", FS, GREEN)
    arrow(d, 258, 195, 382, 195, ORANGE, 3, 12); ctext(d, 320, 175, "相間摩擦(運動量交換)", FT, ORANGE)
    arrow(d, 382, 225, 258, 225, RED, 3, 12); ctext(d, 320, 245, "相間熱伝達(熱交換)", FT, RED)
    box(d, 60, 300, 600, 360, FILL1)
    ctext(d, 330, 330, "検証: これらのモデルが計算対象の流動様式に対応しているか確認", FT)
    note(d, "気泡流用モデルをスラグ流にそのまま使うと精度が出ない")
    save(im, "t1f16InterfacialModels")


# t1f16-17 径方向ボイド分布は計算の結果
def f_radial_void_result():
    im, d = new(); title(d, "径方向ボイド分布は計算の結果(相関式ではない)")
    # 円管断面をセルで表す
    cx, cy, R = 175, 220, 90
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=3)
    for gx in range(cx - R, cx + R + 1, 30):
        d.line((gx, cy - R, gx, cy + R), fill=LGRAY, width=1)
    for gy in range(cy - R, cy + R + 1, 30):
        d.line((cx - R, gy, cx + R, gy), fill=LGRAY, width=1)
    ctext(d, cx, cy + R + 22, "断面を複数セルで解く", FT, GRAY)
    # 径方向分布(結果として出る)
    ox, oy, xl, yl = 370, 330, 210, 200
    axes(d, ox, oy, xl + 15, yl + 10, "半径方向 r", "ボイド率")
    pts = []
    for i in range(0, 201):
        t = i / 200
        a = 0.3 + 0.55 * (t ** 3)   # 壁側で高い等の分布
        pts.append((ox + t * xl, oy - a * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + xl * 0.5, oy - yl * 0.95, "計算の結果として得られる", FT, GREEN)
    note(d, "多次元では分布は自動的に出る. 相関式として外から与えるのは筋違い")
    save(im, "t1f16RadialVoidResult")


# t1f16-18 定量比較の難しさと定性比較
def f_quant_vs_qual():
    im, d = new(); title(d, "定性比較(容易) と 定量比較(困難)")
    box(d, 45, 100, 320, 350, (225, 245, 230))
    ctext(d, 182, 124, "定性的な比較(容易)", FS, GREEN)
    for i, s in enumerate(["可視化写真と気泡群形状",
                           "PIV速度ベクトルの傾向",
                           "流量特性の傾向"]):
        ctext(d, 182, 168 + i * 40, "・" + s, FT)
    ctext(d, 182, 300, "傾向・形状の一致は示せる", FT, GRAY)
    box(d, 340, 100, 620, 350, (250, 230, 230))
    ctext(d, 480, 124, "定量的な比較(困難)", FS, RED)
    ctext(d, 480, 172, "局所ボイド率の", FT)
    ctext(d, 480, 202, "数値そのものの一致", FS)
    ctext(d, 480, 250, "核半径・数密度・初期ボイド率で", FT, GRAY)
    ctext(d, 480, 280, "結果が大きく変わる", FT, GRAY)
    ctext(d, 480, 315, "-> 不確かさが大きく困難", FT, RED)
    note(d, "傾向・形状の一致(定性)は容易, 数値の一致(定量)は困難と切り分ける")
    save(im, "t1f16QuantVsQual")


# t1f16-19 格子収束指数 GCI
def f_gci():
    im, d = new(); title(d, "格子収束指数 GCI")
    box(d, 90, 95, 570, 165, FILL2)
    ctext(d, 330, 120, "GCI = F_s |epsilon| / (r^p - 1)", FS)
    ctext(d, 330, 148, "epsilon = (f_2 - f_1) / f_1", FS)
    ctext(d, 330, 200, "f_1=細かい格子の解, f_2=粗い格子の解", FT, GRAY)
    ctext(d, 330, 228, "r=格子細分化比, p=観測収束次数", FT, GRAY)
    ctext(d, 330, 256, "F_s=安全係数(3格子:1.25 / 2格子:3)", FT, GRAY)
    ctext(d, 330, 296, "GCI 小 = 格子収束が良い(格子に依存しない)", FT, GREEN)
    note(d, "例: r=2,p=2,Fs=1.25,eps=0.030 なら GCI=1.25x0.030/(2^2-1)=1.25%")
    save(im, "t1f16GCI")


# t1f16-20 観測収束次数
def f_observed_order():
    im, d = new(); title(d, "観測収束次数(リチャードソン外挿)")
    box(d, 120, 95, 540, 160, FILL2)
    ctext(d, 330, 128, "p = ln[(f_3 - f_2)/(f_2 - f_1)] / ln r", FS)
    ctext(d, 330, 195, "3段階の格子解 f_1(細)・f_2(中)・f_3(粗)から求める", FT)
    ctext(d, 330, 228, "(格子細分化比 r 一定)", FT, GRAY)
    ctext(d, 330, 268, "求めた p が理論次数(例:2次精度なら2)に近ければ", FT)
    ctext(d, 330, 296, "コードが理論どおり収束している検証になる", FT, GREEN)
    note(d, "この p と2格子解からリチャードソン外挿で格子無限細分の推定値も得られる")
    save(im, "t1f16ObservedOrder")


# t1f16-21 埋込み境界法と周期条件・体積変化
def f_periodic_bc():
    im, d = new(); title(d, "埋込み境界法: 周期条件 と 体積変化の両立")
    # 破綻の図
    x0, x1, yt, yb = 60, 340, 130, 250
    d.line((x0, yt, x1, yt), fill=BLACK, width=2)
    d.line((x0, yb, x1, yb), fill=BLACK, width=2)
    for (px, r) in [(110, 12), (190, 16), (280, 22)]:
        pcircle(d, px, 190, r, FILL1)
    arrow(d, 70, 190, 100, 190, RED, 2, 10)
    ctext(d, 200, 118, "圧力損失で下流ほど低圧", FT, GRAY)
    ctext(d, 200, 275, "-> 弾性体粒子が膨張", FT, RED)
    ctext(d, 200, 300, "周期条件と両立せず破綻", FT, RED)
    # 対策(用語カードは結論を書いてよい)
    box(d, 380, 120, 620, 320, (225, 245, 230))
    ctext(d, 500, 145, "対策", FS, GREEN)
    ctext(d, 500, 185, "周期的な圧力変動に対して", FT)
    ctext(d, 500, 213, "のみ固体の体積変化を考慮", FT)
    ctext(d, 500, 250, "= ある平均圧力下の状態", FT, GREEN)
    ctext(d, 500, 278, "として周期条件を課す", FT, GREEN)
    ctext(d, 500, 308, "(鉛直管気液二相流でも採用)", FT, GRAY)
    note(d, "スパン・壁垂直に一様流束を与える方法は余計な流れを生み推奨されない")
    save(im, "t1f16PeriodicBC")


# ============================================================
if __name__ == "__main__":
    # --- 問題図 t1e16 (10) ---
    vandv_loop()
    laplace_bubble()
    interface_courant()
    bubble_volume_drift()
    damped_oscillation()
    flow_saturation()
    wall_temp_profile()
    validation_methods()
    grid_convergence()
    periodic_channel()
    # --- 公式・用語図 t1f16 (21) ---
    f_verification()
    f_validation()
    f_vandv_guideline()
    f_laplace_pressure()
    f_surface_tension_benchmark()
    f_interface_courant()
    f_contact_angle()
    f_volume_conservation()
    f_vof_vs_levelset()
    f_gcl()
    f_numerical_viscosity()
    f_cavitation_area()
    f_flow_regime_ht()
    f_boiling_transition()
    f_averaging_model()
    f_interfacial_models()
    f_radial_void_result()
    f_quant_vs_qual()
    f_gci()
    f_observed_order()
    f_periodic_bc()
    print("done ch16")
