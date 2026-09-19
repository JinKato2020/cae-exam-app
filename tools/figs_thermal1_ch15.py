# -*- coding: utf-8 -*-
"""熱流体力学1級 第15章「相変化」の図(t1e15*・t1f15*)を描画。
白地660x420・黒線画・機構のみ。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(sigma, rho, lambda, delta, mu, Delta p, T_S, T_W, p_v, p_sv, p_L,
 dR/dt, rho U^2, (1/2)rho U^2, tau, Omega 等)。
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


def vtube(d, cx, y0, y1, hw=44, wd=3):
    """鉛直円管(左右2本の壁)。"""
    d.line((cx - hw, y0, cx - hw, y1), fill=BLACK, width=wd)
    d.line((cx + hw, y0, cx + hw, y1), fill=BLACK, width=wd)


# ============================================================
# ===================  問題図  t1e15*  =======================
# ============================================================

# 15-1 t1e15PhaseChangeMap : 純物質のp-T相図(required・正誤判定なし)
def phase_change_map():
    im, d = new(); title(d, "純物質の p-T 相図 (圧力-温度)")
    ox, oy = 110, 360; xl, yl = 470, 300
    axes(d, ox, oy, xl, yl, "温度 T", "圧力 p")
    # 三重点と臨界点
    tp = (ox + 150, oy - 90)      # 三重点
    cp = (ox + 360, oy - 230)     # 臨界点
    # 固液境界(ほぼ鉛直・やや右上がり)
    d.line((tp[0], tp[1], tp[0] + 55, oy - 285), fill=BLUE, width=3)
    # 液気境界(三重点->臨界点)
    lg = []
    for i in range(61):
        t = i / 60
        x = tp[0] + (cp[0] - tp[0]) * t
        y = tp[1] + (cp[1] - tp[1]) * (t ** 1.6)
        lg.append((x, y))
    d.line(lg, fill=RED, width=3, joint="curve")
    # 固気境界(三重点->左下)
    d.line((tp[0], tp[1], ox + 20, oy - 8), fill=GREEN, width=3)
    # 点
    node(d, tp[0], tp[1], 5, fill=BLACK, col=BLACK)
    ctext(d, tp[0] - 8, tp[1] + 18, "三重点", FT, GRAY, "rm")
    node(d, cp[0], cp[1], 5, fill=BLACK, col=BLACK)
    ctext(d, cp[0] + 10, cp[1] - 8, "臨界点", FT, GRAY, "lm")
    # 各相名称のみ
    ctext(d, ox + 60, oy - 210, "固相", FS, BLUE)
    ctext(d, ox + 250, oy - 210, "液相", FS, RED)
    ctext(d, ox + 350, oy - 60, "気相", FS, GREEN)
    ctext(d, tp[0] + 95, tp[1] - 40, "液気境界(飽和蒸気圧曲線)", FT, RED, "lm")
    note(d, "3本の相境界線・三重点・臨界点を示す(各相の名称のみ)")
    save(im, "t1e15PhaseChangeMap")


# 15-2 t1e15PressureNegative : 飽和線と沸騰/キャビ矢印(helpful)
def pressure_negative():
    im, d = new(); title(d, "飽和蒸気圧曲線と 沸騰・キャビテーション")
    ox, oy = 110, 360; xl, yl = 470, 300
    axes(d, ox, oy, xl, yl, "温度 T", "圧力 p")
    # 飽和線(右上がり)
    sat = []
    for i in range(61):
        t = i / 60
        x = ox + 30 + t * (xl - 90)
        y = oy - 30 - (yl - 70) * (t ** 1.7)
        sat.append((x, y))
    d.line(sat, fill=BLACK, width=3, joint="curve")
    ctext(d, sat[-1][0] + 6, sat[-1][1] - 6, "飽和蒸気圧線", FT, GRAY, "lm")
    # 上側=液相, 下側=気相
    ctext(d, ox + 90, oy - 210, "液相 (飽和線の上側)", FS, BLUE)
    ctext(d, ox + 250, oy - 70, "気相 (飽和線の下側)", FS, GREEN)
    # 代表点
    mid = sat[32]
    node(d, mid[0], mid[1], 5, fill=BLACK, col=BLACK)
    # キャビテーション:圧力を下げて飽和線を下に横切る(下向き矢印)
    arrow(d, mid[0], mid[1] - 4, mid[0], mid[1] + 60, RED, 3, 12)
    ctext(d, mid[0] - 10, mid[1] + 40, "圧力低下=キャビテーション", FT, RED, "rm")
    # 沸騰:温度を上げて飽和線を右に横切る(右向き矢印)
    p2 = sat[24]
    node(d, p2[0], p2[1], 5, fill=BLACK, col=BLACK)
    arrow(d, p2[0] + 4, p2[1], p2[0] + 70, p2[1], ORANGE, 3, 12)
    ctext(d, p2[0] + 78, p2[1] - 14, "温度上昇=沸騰", FT, ORANGE, "lm")
    note(d, "飽和線を下へ横切る=キャビ(圧力側), 右へ横切る=沸騰(温度側)")
    save(im, "t1e15PressureNegative")


# 15-3 t1e15BoilingCurveRegions : 沸騰曲線4区間(required・区間名なし)
def boiling_curve_regions():
    im, d = new(); title(d, "プール沸騰曲線 (横軸=壁面過熱度, 縦軸=熱流束)")
    ox, oy = 100, 360; xl, yl = 490, 300
    axes(d, ox, oy, xl, yl, "壁面過熱度", "熱流束")
    # 曲線(単調増→ピーク→ディップ→再上昇)を4区間で
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    pts = []
    # 区間A: 0-0.22 ゆるやか上昇
    for i in range(23):
        t = i / 100; pts.append((X(t), Y(0.05 + 1.0 * t)))
    # 区間B: 0.22-0.45 急上昇してピーク
    for i in range(22, 46):
        t = i / 100; v = 0.27 + 2.9 * (t - 0.22); pts.append((X(t), Y(min(v, 0.95))))
    # 区間C: 0.45-0.70 低下(ディップ)
    for i in range(46, 71):
        t = i / 100; v = 0.95 - 2.4 * (t - 0.45); pts.append((X(t), Y(max(v, 0.35))))
    # 区間D: 0.70-1.0 再上昇
    for i in range(71, 101):
        t = i / 100; v = 0.35 + 1.4 * (t - 0.70); pts.append((X(t), Y(v)))
    d.line(pts, fill=BLACK, width=3, joint="curve")
    # 4区間の境界を薄い縦線+帯ラベル(A)(B)(C)(D)
    bounds = [0.0, 0.22, 0.45, 0.70, 1.0]
    labs = ["(A)", "(B)", "(C)", "(D)"]
    for k in range(4):
        xa, xb = X(bounds[k]), X(bounds[k + 1])
        if k > 0:
            dashed(d, xa, oy, xa, oy - yl, LGRAY, 1, 6, 5)
        ctext(d, (xa + xb) / 2, oy + 22, labs[k], FS, GRAY)
    note(d, "低過熱度側から (A)(B)(C)(D). 途中で熱流束が一度下がる(区間名は伏せる)")
    save(im, "t1e15BoilingCurveRegions")


# 15-4 t1e15DnbTempJump : 熱伝達率と温度差(required・数値なし)
def dnb_temp_jump():
    im, d = new(); title(d, "同じ熱流束でも h が下がると温度差が拡大 (DNB)")
    # 左: 核沸騰(h大 -> 温度差小)
    box(d, 55, 95, 320, 360, FILL1)
    ctext(d, 187, 118, "核沸騰 (h 大)", FS, BLUE)
    wall(d, 90, 150, 340, side=1, n=12)
    ctext(d, 78, 360, "壁", FT, GRAY, "rm")
    # 流体温度線
    d.line((150, 250, 300, 250), fill=GREEN, width=2); ctext(d, 300, 250, "流体温度", FT, GREEN, "lm")
    # 温度差(小)を横向き矢印で
    arrow(d, 96, 210, 150, 210, RED, 3, 12)
    ctext(d, 187, 190, "温度差 小", FT, RED)
    ctext(d, 187, 330, "同じ熱流束 q''", FT, GRAY)
    # 右: 膜沸騰(h小 -> 温度差大)
    box(d, 345, 95, 610, 360, FILL2)
    ctext(d, 477, 118, "膜沸騰 (h 小)", FS, RED)
    wall(d, 380, 150, 340, side=1, n=12)
    d.line((440, 250, 590, 250), fill=GREEN, width=2); ctext(d, 590, 250, "流体温度", FT, GREEN, "lm")
    arrow(d, 386, 210, 560, 210, RED, 3, 13)
    ctext(d, 470, 190, "温度差 大", FT, RED)
    ctext(d, 477, 330, "同じ熱流束 q''", FT, GRAY)
    note(d, "q''=h(T-T_b) 一定. h が下がると温度差 Delta T=q''/h が大きくなる(数値は各自)")
    save(im, "t1e15DnbTempJump")


# 15-5 t1e15SubcoolBoiling : サブクール沸騰の温度分布(helpful)
def subcool_boiling():
    im, d = new(); title(d, "サブクール沸騰: 壁近傍だけ局所的に沸点超え")
    wall(d, 120, 110, 360, side=1, n=14)
    ctext(d, 108, 100, "加熱壁", FT, GRAY, "rm")
    # 沸点(飽和温度)の鉛直基準線
    xsat = 360
    dashed(d, xsat, 110, xsat, 360, GRAY, 2, 8, 5)
    ctext(d, xsat, 90, "沸点(飽和温度)", FT, GRAY)
    # 温度分布曲線: 壁で高温(沸点超え)->バルクで沸点未満
    prof = []
    for i in range(101):
        t = i / 100
        # 壁(x=120)で高温、遠方で低温(サブクール)
        temp = 400 - (400 - 200) * (1 - math.exp(-3.2 * t))
        # 実座標: x=壁からの距離, 温度は右ほど高い表示にするため x位置=温度
        xx = 120 + (temp - 190) * 1.05
        yy = 120 + t * 220
        prof.append((xx, yy))
    d.line(prof, fill=RED, width=3, joint="curve")
    ctext(d, prof[3][0] + 60, prof[3][1], "壁近傍=沸点超え", FT, RED, "lm")
    ctext(d, prof[-1][0] + 6, prof[-1][1], "バルク=沸点未満(冷たい)", FT, BLUE, "lm")
    # 壁近傍の小気泡
    for yy in (160, 200, 240, 280):
        pcircle(d, 138, yy, 6, (235, 242, 250), BLUE, 2)
    note(d, "バルクは沸点未満でも, 加熱面近傍だけ局所的に沸騰し小気泡が発生する")
    save(im, "t1e15SubcoolBoiling")


# 15-6 t1e15BubbleNucleusLaplace : 気泡核とラプラス圧(helpful・数値なし)
def bubble_nucleus_laplace():
    im, d = new(); title(d, "液中の球形微小気泡とラプラス則  Delta p = 2 sigma / R")
    # 液体背景
    for yy in range(110, 370, 26):
        d.line((90, yy, 570, yy), fill=(232, 238, 245), width=1)
    cx, cy, R = 300, 235, 90
    pcircle(d, cx, cy, R, (235, 242, 250), BLUE, 3)
    ctext(d, cx, cy - 20, "蒸気", FS, BLUE)
    # 半径
    arrow(d, cx, cy, cx + R * math.cos(math.radians(-35)), cy - R * math.sin(math.radians(-35)), GRAY, 2, 10)
    ctext(d, cx + 40, cy - 22, "R", FT, GRAY)
    # 内圧・外圧
    ctext(d, cx, cy + 20, "内圧 p_in", FT, RED)
    ctext(d, cx - 150, cy, "外圧 p_out", FT, BLACK)
    # 表面張力(接線)を数か所
    for a in range(0, 360, 45):
        ax = cx + R * math.cos(math.radians(a)); ay = cy - R * math.sin(math.radians(a))
        tx, ty = -math.sin(math.radians(a)), -math.cos(math.radians(a))
        d.line((ax - tx * 16, ay - ty * 16, ax + tx * 16, ay + ty * 16), fill=GREEN, width=2)
    ctext(d, cx + R + 20, cy + R - 20, "表面張力 sigma", FT, GREEN, "lm")
    # 過剰圧
    box(d, 430, 300, 620, 360, FILL2)
    ctext(d, 525, 330, "過剰圧 = 2 sigma / R", FS, RED)
    note(d, "表面張力で内圧が外圧より 2 sigma/R だけ高い. R が小さいほど過剰圧は大(数値なし)")
    save(im, "t1e15BubbleNucleusLaplace")


# 15-7 t1e15FlowRegimeSequence : 鉛直管の流動様式(required・様式名ラベルのみ)
def flow_regime_sequence():
    im, d = new(); title(d, "鉛直円管内の流動様式(下から上へ)")
    cx = 200; y0, y1 = 70, 400; hw = 46
    vtube(d, cx, y0, y1, hw)
    # 下向き入口->上向き流れ矢印
    arrow(d, cx, 405, cx, 360, GRAY, 2, 11)
    ctext(d, cx, 415, "流れ(上向き)", FT, GRAY)
    # 気泡流(下部)
    for (px, py) in [(cx - 20, 355), (cx + 15, 345), (cx - 5, 335), (cx + 25, 358), (cx - 28, 340)]:
        pcircle(d, px, py, 6, (235, 242, 250), BLUE, 2)
    ctext(d, cx + hw + 20, 348, "気泡流", FS, BLACK, "lm")
    # スラグ流(大きな砲弾状気泡)
    d.ellipse((cx - 30, 268, cx + 30, 315), outline=BLUE, width=2, fill=(235, 242, 250))
    ctext(d, cx + hw + 20, 290, "スラグ流", FS, BLACK, "lm")
    # 環状噴霧流(壁に液膜+中央蒸気+液滴)
    d.rectangle((cx - hw, 190, cx - hw + 8, 250), fill=(210, 225, 245))
    d.rectangle((cx + hw - 8, 190, cx + hw, 250), fill=(210, 225, 245))
    for (px, py) in [(cx, 205), (cx - 12, 225), (cx + 14, 240), (cx + 4, 215)]:
        pcircle(d, px, py, 3, BLUE, BLUE, 1)
    ctext(d, cx + hw + 20, 220, "環状噴霧流", FS, BLACK, "lm")
    # 噴霧流(乾いた壁+液滴のみ)
    for (px, py) in [(cx - 15, 110), (cx + 10, 130), (cx + 20, 105), (cx - 25, 145), (cx, 155)]:
        pcircle(d, px, py, 3, BLUE, BLUE, 1)
    ctext(d, cx + hw + 20, 130, "噴霧流", FS, BLACK, "lm")
    note(d, "気泡流 -> スラグ流 -> 環状噴霧流 -> 噴霧流(様式名のみ)")
    save(im, "t1e15FlowRegimeSequence")


# 15-8 t1e15DryoutDroplet : ドライアウト(helpful)
def dryout_droplet():
    im, d = new(); title(d, "環状噴霧流の液膜とドライアウト(液滴の付着・離脱)")
    # 左: 液膜が健在(付着・離脱)
    ctext(d, 175, 95, "上流: 液膜あり", FS, BLUE)
    d.rectangle((90, 120, 100, 360), fill=(210, 225, 245), outline=BLACK, width=2)   # 左壁液膜
    d.rectangle((260, 120, 270, 360), fill=(210, 225, 245), outline=BLACK, width=2)  # 右壁液膜
    d.line((90, 120, 90, 360), fill=BLACK, width=3); d.line((270, 120, 270, 360), fill=BLACK, width=3)
    ctext(d, 180, 240, "蒸気+液滴", FT, GRAY)
    # 付着(液滴->壁) 離脱(壁->液滴)
    arrow(d, 180, 180, 105, 160, GREEN, 2, 9); ctext(d, 150, 150, "付着", FT, GREEN)
    arrow(d, 105, 300, 180, 320, ORANGE, 2, 9); ctext(d, 160, 335, "離脱", FT, ORANGE)
    for (px, py) in [(160, 200), (200, 260), (175, 300), (210, 200)]:
        pcircle(d, px, py, 4, BLUE, BLUE, 1)
    # 右: 下流で液膜が尽きて壁が乾く
    ctext(d, 480, 95, "下流: 液膜が尽きる", FS, RED)
    d.line((400, 120, 400, 360), fill=BLACK, width=3); d.line((560, 120, 560, 360), fill=BLACK, width=3)
    ctext(d, 480, 240, "壁が乾く(ドライアウト)", FT, RED)
    for (px, py) in [(460, 200), (500, 280), (480, 320)]:
        pcircle(d, px, py, 4, BLUE, BLUE, 1)
    arrow(d, 300, 240, 380, 240, GRAY, 3, 12)
    note(d, "液膜は液滴の付着(補給)と離脱(減少)の収支で決まる. 尽きるとドライアウト")
    save(im, "t1e15DryoutDroplet")


# 15-9 t1e15ChfMechanism : CHFの2機構対比(helpful)
def chf_mechanism():
    im, d = new(); title(d, "限界熱流束(CHF)の2機構")
    box(d, 45, 95, 320, 320, FILL1)
    ctext(d, 182, 120, "ドライアウト型", FS, BLUE)
    ctext(d, 182, 152, "環状流の液膜消失", FT)
    for i, s in enumerate(["低流量・長い加熱管で生じやすい",
                           "壁温上昇はゆるやか",
                           "(蒸気流の冷却が効く)"]):
        ctext(d, 182, 190 + i * 34, s, FT, GRAY)
    box(d, 340, 95, 615, 320, FILL2)
    ctext(d, 477, 120, "DNB型", FS, RED)
    ctext(d, 477, 152, "核沸騰->膜沸騰の遷移", FT)
    for i, s in enumerate(["高流量・短い加熱管で生じやすい",
                           "壁温上昇が急激",
                           "クオリティが負でも起こり得る"]):
        ctext(d, 477, 190 + i * 34, s, FT, GRAY)
    # 流量の矢印
    arrow(d, 180, 340, 90, 340, BLUE, 3, 12); ctext(d, 120, 360, "低流量", FT, BLUE)
    arrow(d, 480, 340, 590, 340, RED, 3, 12); ctext(d, 545, 360, "高流量", FT, RED)
    note(d, "両者の境界は必ずしも明確でない. 壁温上昇はDNB型の方が急激")
    save(im, "t1e15ChfMechanism")


# 15-10 t1e15CriticalHeatFluxTube : 均一加熱円管(required・数値なし)
def critical_heat_flux_tube():
    im, d = new(); title(d, "均一加熱円管: 入口サブクール水 -> 出口クオリティ最大")
    y0, y1 = 170, 250
    x0, x1 = 110, 560
    d.line((x0, y0, x1, y0), fill=BLACK, width=3)
    d.line((x0, y1, x1, y1), fill=BLACK, width=3)
    # 入口
    arrow(d, 60, 210, 108, 210, BLUE, 3, 13)
    ctext(d, 75, 185, "入口", FT, BLUE); ctext(d, 80, 235, "サブクール水", FT, BLUE)
    # 外周からの一定熱流束q(上下から)
    for xx in range(140, 550, 55):
        arrow(d, xx, 130, xx, 168, RED, 2, 9)
        arrow(d, xx, 290, xx, 252, RED, 2, 9)
    ctext(d, 335, 112, "一定熱流束 q (外周から加熱)", FT, RED)
    # 管内の蒸発進行(気泡増加)を模式的に
    for (px, py, r) in [(180, 210, 4), (250, 210, 6), (320, 208, 8), (400, 210, 10), (480, 210, 12)]:
        pcircle(d, px, py, r, (235, 242, 250), BLUE, 2)
    # 出口
    arrow(d, 562, 210, 610, 210, GRAY, 3, 13)
    ctext(d, 590, 185, "出口", FT, GRAY); ctext(d, 585, 235, "クオリティ最大", FT, GRAY)
    ctext(d, 335, 330, "限界熱流束状態への移行はクオリティ最大の出口で生じる", FT, GRAY)
    note(d, "x=(1/h_V)(4qL/GD - h_IN) で出口クオリティが決まる(数値は各自)")
    save(im, "t1e15CriticalHeatFluxTube")


# 15-11 t1e15BoilingCalcModel : 様式ごとの相関式切替(helpful)
def boiling_calc_model():
    im, d = new(); title(d, "沸騰流れ計算: 壁面温度で相関式モデルを切り替える")
    # 壁面温度軸(横)
    ox, oy = 70, 210; xl = 540
    arrow(d, ox, oy, ox + xl, oy, BLACK, 2, 11); ctext(d, ox + xl + 6, oy, "壁面温度", FT, BLACK, "lm")
    labs = ["単相強制対流", "核沸騰", "遷移沸騰", "膜沸騰"]
    cols = [GRAY, BLUE, ORANGE, RED]
    bw = xl / 4
    for k in range(4):
        xa = ox + k * bw
        d.rectangle((xa, oy - 40, xa + bw - 6, oy - 6), outline=cols[k], width=2, fill=FILL1)
        ctext(d, xa + bw / 2 - 3, oy - 23, labs[k], FT, cols[k])
        if k > 0:
            dashed(d, xa, oy - 45, xa, oy + 8, LGRAY, 1, 6, 4)
    ctext(d, ox + xl / 2, oy - 62, "様式ごとに異なる相関式ブロック", FT, GRAY)
    # 実験データ->相関式へ供給
    box(d, 200, 300, 460, 360, FILL2)
    ctext(d, 330, 330, "実験データ", FS, GREEN)
    arrow(d, 330, 298, 330, 240, GREEN, 3, 13)
    ctext(d, 350, 268, "相関式へ供給", FT, GREEN, "lm")
    note(d, "相関式は理論的厳密導出ではなく実験ベース. データ追加で精度が上がる")
    save(im, "t1e15BoilingCalcModel")


# 15-12 t1e15FilmCondensation : 膜状凝縮の幾何(required・数値なし)
def film_condensation():
    im, d = new(); title(d, "鉛直冷却面上の層流液膜(膜状凝縮)")
    # 冷却壁(左)
    wall(d, 150, 90, 380, side=-1, n=15)
    ctext(d, 130, 80, "冷却面 T_W", FT, BLUE, "lm")
    # 液膜(下ほど厚い)
    film = [(150, 90)]
    for i in range(61):
        t = i / 60
        x = 150 + (10 + 55 * (t ** 0.25))
        y = 90 + t * 290
        film.append((x, y))
    film.append((150, 380))
    d.polygon(film, fill=(210, 225, 245))
    d.line(film[1:-1], fill=BLUE, width=3, joint="curve")
    # 液膜表面温度T_S
    ctext(d, 260, 120, "液膜表面 T_S (=飽和温度)", FT, RED, "lm")
    # 蒸気側
    ctext(d, 470, 200, "蒸気雰囲気", FS, GRAY)
    # 熱流束矢印(蒸気->冷却面)
    for yy in (160, 230, 300):
        xf = 150 + (10 + 55 * (((yy - 90) / 290) ** 0.25))
        arrow(d, xf + 90, yy, xf + 8, yy, GREEN, 2, 10)
    ctext(d, 380, 340, "熱流束(蒸気->冷却面)", FT, GREEN)
    # 液膜厚δと位置x
    yy = 250; xf = 150 + (10 + 55 * (((yy - 90) / 290) ** 0.25))
    dim(d, 150, yy, xf, yy, "delta (液膜厚)", col=GRAY)
    arrow(d, 620, 90, 620, 380, GRAY, 2, 11); ctext(d, 632, 235, "x", FS, GRAY, "lm")
    ctext(d, 620, 75, "位置 x", FT, GRAY)
    note(d, "液膜表面=飽和温度 T_S, 冷却面=T_W. 下流ほど液膜厚 delta が増す(数値なし)")
    save(im, "t1e15FilmCondensation")


# 15-13 t1e15BubbleFlowPhaseChange : 相変化の要否対比(helpful)
def bubble_flow_phase_change():
    im, d = new(); title(d, "気泡を含む流れ: 相変化を考慮すべきか")
    # 左: 水中翼のキャビテーション(相変化=要考慮)
    box(d, 45, 90, 320, 360, FILL1)
    ctext(d, 182, 114, "A: 水中翼のキャビテーション", FT, BLUE)
    # 翼型
    foil = [(80, 230), (150, 205), (250, 220), (150, 245)]
    d.polygon(foil, outline=BLACK, width=3, fill=FILL2)
    # 翼上面の気泡(相変化)
    for (px, py, r) in [(140, 200, 6), (160, 196, 8), (185, 200, 7), (120, 205, 5)]:
        pcircle(d, px, py, r, (235, 242, 250), BLUE, 2)
    ctext(d, 182, 285, "圧力低下で液体が蒸気に", FT)
    ctext(d, 182, 312, "= 相変化 -> 考慮が必要", FS, RED)
    # 右: 炭酸飲料のCO2泡(脱ガス=不要)
    box(d, 340, 90, 615, 360, FILL2)
    ctext(d, 477, 114, "B: 炭酸飲料の泡", FT, GREEN)
    # コップ
    d.line((420, 150, 435, 320), fill=BLACK, width=3); d.line((535, 150, 520, 320), fill=BLACK, width=3)
    d.line((435, 320, 520, 320), fill=BLACK, width=3)
    for (px, py, r) in [(460, 300, 5), (490, 270, 6), (470, 240, 5), (500, 210, 7), (475, 185, 6)]:
        pcircle(d, px, py, r, "white", GREEN, 2)
    ctext(d, 477, 285, "溶存CO2が析出した気体", FT)
    ctext(d, 477, 312, "= 脱ガス -> 考慮は不要", FS, RED)
    note(d, "キャビ(相変化)は考慮必要, 脱ガス(溶存ガス析出)は考慮不要")
    save(im, "t1e15BubbleFlowPhaseChange")


# ---- キャビテーション4形態を翼まわりに描く共通関数 ----
def _cav_forms(d, x0, y0, w, h, emphasize=None):
    """4形態のミニ翼スケッチ。emphasize=強調する形態名。"""
    forms = ["シート", "バブル", "クラウド", "ボルテックス"]
    cw = w / 2; ch = h / 2
    pos = [(x0, y0), (x0 + cw, y0), (x0, y0 + ch), (x0 + cw, y0 + ch)]
    for name, (px, py) in zip(forms, pos):
        emph = (name == emphasize)
        col = RED if emph else BLACK
        box(d, px + 6, py + 6, px + cw - 6, py + ch - 6, (255, 240, 240) if emph else "white", 3 if emph else 2)
        # ミニ翼
        fx, fy = px + cw / 2, py + ch / 2 + 6
        foil = [(fx - 40, fy), (fx - 5, fy - 12), (fx + 40, fy - 2), (fx - 5, fy + 10)]
        d.polygon(foil, outline=BLACK, width=2, fill=FILL2)
        if name == "シート":
            d.line((fx - 20, fy - 9, fx + 20, fy - 4), fill=BLUE, width=4)   # 付着膜
        elif name == "バブル":
            for (bx, by) in [(fx, fy - 12), (fx + 14, fy - 10), (fx + 28, fy - 8)]:
                pcircle(d, bx, by, 4, (235, 242, 250), BLUE, 2)              # 移動する球群
        elif name == "クラウド":
            for k in range(9):
                bx = fx - 8 + (k % 3) * 10; by = fy - 16 + (k // 3) * 6
                pcircle(d, bx, by, 2, BLUE, BLUE, 1)                          # 雲状
        else:
            d.line((fx + 20, fy - 4, fx + 55, fy - 10), fill=BLUE, width=3)  # 渦コアのひも
        ctext(d, px + cw / 2, py + ch - 14, name, FT, col)


# 15-14 t1e15CavitationForms : 4形態+初生(helpful)
def cavitation_forms():
    im, d = new(); title(d, "キャビテーションの4形態 と 気泡核の初生")
    _cav_forms(d, 45, 60, 380, 300)
    # 右: 臨界サイズより大きい核が膨張->初生
    box(d, 445, 70, 620, 350, FILL1)
    ctext(d, 532, 92, "気泡核の初生", FS, BLACK)
    pcircle(d, 532, 150, 14, (235, 242, 250), BLUE, 2); ctext(d, 532, 150, "核", FT)
    ctext(d, 532, 180, "臨界サイズより大", FT, GRAY)
    arrow(d, 532, 195, 532, 225, RED, 3, 12)
    pcircle(d, 532, 270, 40, (235, 242, 250), BLUE, 3)
    ctext(d, 532, 315, "膨張して初生", FT, RED)
    note(d, "形態=バブル/シート/クラウド/ボルテックス. 臨界サイズ超えの核が膨張して初生")
    save(im, "t1e15CavitationForms")


# 15-15 t1e15CavitationNumber : キャビテーション数(required・結果数値なし)
def cavitation_number():
    im, d = new(); title(d, "キャビテーション数 sigma の定義")
    # 物体まわりの一様流
    arrow(d, 60, 150, 150, 150, BLUE, 3, 12)
    arrow(d, 60, 200, 150, 200, BLUE, 3, 12)
    arrow(d, 60, 250, 150, 250, BLUE, 3, 12)
    ctext(d, 90, 128, "一様流 U", FT, BLUE)
    # 物体(円柱/翼)
    pcircle(d, 250, 200, 45, FILL2)
    ctext(d, 250, 200, "物体", FT)
    # 流線が加速する様子
    for yy in (150, 250):
        d.line((295, yy, 420, yy), fill=BLUE, width=2)
    # ラベル
    ctext(d, 250, 285, "静圧 p, 流速 U, 密度 rho", FT, GRAY)
    ctext(d, 250, 308, "飽和蒸気圧 p_v", FT, GRAY)
    # 定義式
    box(d, 430, 150, 630, 260, FILL1)
    ctext(d, 530, 180, "sigma =", FS)
    ctext(d, 530, 210, "(p - p_v)", FS)
    d.line((470, 224, 590, 224), fill=BLACK, width=2)
    ctext(d, 530, 240, "(1/2) rho U^2", FS)
    ctext(d, 530, 285, "動圧 = (1/2) rho U^2", FT, GRAY)
    note(d, "sigma=(p-p_v)/((1/2)rho U^2). 大きいほど発生しにくい(計算結果は各自)")
    save(im, "t1e15CavitationNumber")


# 15-16 t1e15BubbleCavitation : 4形態・バブル強調(helpful)
def bubble_cavitation():
    im, d = new(); title(d, "バブル(トラベリング)キャビテーション")
    _cav_forms(d, 45, 60, 500, 300, emphasize="バブル")
    ctext(d, 300, 375, "バブル=主流に乗って移動する球形気泡群(強調)", FT, RED)
    save(im, "t1e15BubbleCavitation")


# 15-17 t1e15Aeration : エアレーション(helpful)
def aeration():
    im, d = new(); title(d, "エアレーション: 溶存空気が圧力低下で析出")
    # 左: 高圧(溶解) -> 右: 低圧(気泡析出)
    box(d, 55, 100, 300, 340, FILL1)
    ctext(d, 177, 122, "高圧: 空気は油に溶解", FT, BLUE)
    for (px, py) in [(110, 200), (150, 240), (200, 210), (240, 270), (130, 300), (210, 300)]:
        d.line((px - 4, py, px + 4, py), fill=GRAY, width=2)
        d.line((px, py - 4, px, py + 4), fill=GRAY, width=2)  # 溶けた分子(+印)
    ctext(d, 177, 320, "作動油", FT, GRAY)
    arrow(d, 305, 220, 355, 220, RED, 3, 13); ctext(d, 330, 200, "圧力低下", FT, RED)
    box(d, 360, 100, 610, 340, FILL2)
    ctext(d, 485, 122, "低圧: 過飽和で気泡析出", FT, RED)
    for (px, py, r) in [(420, 210, 8), (470, 260, 10), (520, 220, 7), (490, 300, 9), (550, 270, 8)]:
        pcircle(d, px, py, r, "white", GREEN, 2)
    ctext(d, 485, 320, "空気の泡(脱ガス)", FT, GRAY)
    # 圧力軸に分離圧と飽和蒸気圧を別配置
    ox = 110; oy = 375; xl = 440
    arrow(d, ox, oy, ox + xl, oy, BLACK, 2, 10); ctext(d, ox + xl + 6, oy, "圧力", FT, BLACK, "lm")
    d.line((ox + 300, oy - 7, ox + 300, oy + 7), fill=GREEN, width=3); ctext(d, ox + 300, oy - 18, "空気分離圧", FT, GREEN)
    d.line((ox + 120, oy - 7, ox + 120, oy + 7), fill=RED, width=3); ctext(d, ox + 120, oy - 18, "飽和蒸気圧", FT, RED)
    note(d, "空気分離圧は飽和蒸気圧と異なる. 蒸気キャビ(相変化)と区別される")
    save(im, "t1e15Aeration")


# 15-18 t1e15BubbleGrowthRate : 気泡成長の駆動(required・数値なし)
def bubble_growth_rate():
    im, d = new(); title(d, "慣性支配のキャビテーション気泡成長")
    for yy in range(110, 370, 26):
        d.line((90, yy, 570, yy), fill=(232, 238, 245), width=1)
    cx, cy, R = 300, 235, 80
    # 元の気泡(点線)と成長後(実線)
    dashed(d, cx - 55, cy, cx + 55, cy, GRAY, 1, 5, 4)
    d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), outline=GRAY, width=2)
    pcircle(d, cx, cy, R, (235, 242, 250), BLUE, 3)
    ctext(d, cx, cy - 18, "蒸気 p_sv", FS, BLUE)
    # 気泡壁の膨張速度dR/dt(外向き矢印)
    for a in (30, 150, 270):
        ax = cx + (R - 6) * math.cos(math.radians(a)); ay = cy - (R - 6) * math.sin(math.radians(a))
        bx = cx + (R + 34) * math.cos(math.radians(a)); by = cy - (R + 34) * math.sin(math.radians(a))
        arrow(d, ax, ay, bx, by, RED, 3, 12)
    ctext(d, cx + 90, cy - 70, "気泡壁速度 dR/dt", FT, RED, "lm")
    # 周囲液圧
    ctext(d, cx - 150, cy + 40, "周囲液圧 p_L", FT, BLACK)
    box(d, 400, 300, 620, 360, FILL2)
    ctext(d, 510, 330, "駆動力 = p_sv - p_L", FS, RED)
    note(d, "(dR/dt)^2 = (p_sv - p_L)/rho_L. 圧力差が成長を駆動する(数値なし)")
    save(im, "t1e15BubbleGrowthRate")


# 15-19 t1e15BubbleCollapse : 成長と急崩壊(helpful)
def bubble_collapse():
    im, d = new(); title(d, "気泡の緩やかな成長と急激な崩壊")
    ox, oy = 90, 340; xl, yl = 470, 260
    axes(d, ox, oy, xl, yl, "時間 t", "気泡半径 R")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    # 緩やか成長->ピーク->急崩壊
    pts = []
    for i in range(101):
        t = i / 100
        if t < 0.6:
            v = 0.9 * math.sin(math.pi / 2 * (t / 0.6))   # 緩やか成長
        else:
            v = 0.9 * (1 - ((t - 0.6) / 0.4) ** 3)        # 急崩壊
        pts.append((X(t), Y(max(v, 0.02))))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, X(0.3), Y(0.98), "緩やかに成長", FT, BLUE)
    ctext(d, X(0.86), Y(0.75), "急激に崩壊", FT, RED)
    # 崩壊時の吹き出し
    cxp, cyp = X(0.97), Y(0.05)
    box(d, cxp - 190, cyp - 60, cxp + 5, cyp + 10, FILL2)
    ctext(d, cxp - 92, cyp - 42, "崩壊時: 圧力・温度が急上昇", FT, RED)
    ctext(d, cxp - 92, cyp - 18, "圧力上昇=壊食 / 温度上昇=発光", FT, GRAY)
    note(d, "収縮(崩壊)は成長より速い. 圧力上昇が壊食, 温度上昇が発光の原因")
    save(im, "t1e15BubbleCollapse")


# 15-20 t1e15CollapseCompressibility : 崩壊と圧縮性(helpful)
def collapse_compressibility():
    im, d = new(); title(d, "崩壊直前: 液体の圧縮性と界面の凝縮")
    # 左: 崩壊直前の気泡
    cx, cy, R = 175, 210, 60
    for yy in range(120, 320, 24):
        d.line((60, yy, 300, yy), fill=(232, 238, 245), width=1)
    pcircle(d, cx, cy, R, (240, 235, 235), RED, 3)
    ctext(d, cx, cy - 12, "高温・高圧", FT, RED)
    # 気泡壁が内向き(液体音速に迫る)
    for a in (30, 150, 270):
        ax = cx + (R + 30) * math.cos(math.radians(a)); ay = cy - (R + 30) * math.sin(math.radians(a))
        bx = cx + (R + 4) * math.cos(math.radians(a)); by = cy - (R + 4) * math.sin(math.radians(a))
        arrow(d, ax, ay, bx, by, RED, 3, 11)
    ctext(d, cx, cy + R + 26, "気泡壁速度 -> 液体の音速", FT, RED)
    ctext(d, cx, cy + R + 48, "界面で蒸気の凝縮", FT, GREEN)
    # 右: R-P式 vs Fujikawa-Akamatsu式の考慮項
    box(d, 330, 100, 620, 350, FILL1)
    ctext(d, 475, 122, "考慮項の違い", FS, BLACK)
    ctext(d, 350, 160, "Rayleigh-Plesset式", FT, BLUE, "lm")
    ctext(d, 365, 186, "液体の圧縮性: 考慮しない", FT, GRAY, "lm")
    ctext(d, 365, 210, "界面の蒸発・凝縮: 考慮しない", FT, GRAY, "lm")
    ctext(d, 365, 234, "-> 最小半径を過小評価", FT, RED, "lm")
    d.line((345, 258, 605, 258), fill=LGRAY, width=1)
    ctext(d, 350, 282, "Fujikawa-Akamatsu式", FT, GREEN, "lm")
    ctext(d, 365, 308, "液体の圧縮性: 考慮", FT, GRAY, "lm")
    ctext(d, 365, 332, "界面の凝縮: 考慮", FT, GRAY, "lm")
    note(d, "崩壊時は圧縮性・界面凝縮が効く. R-P式はこれらを含まない")
    save(im, "t1e15CollapseCompressibility")


# 15-21 t1e15StepPressureResponse : ステップ加圧の応答(helpful)
def step_pressure_response():
    im, d = new(); title(d, "ステップ加圧に対する気泡径の応答(Rayleigh-Plesset)")
    ox, oy = 95, 340; xl, yl = 470, 260
    axes(d, ox, oy, xl, yl, "時間 t", "気泡径 D")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    # D1(初期)とD2(平衡)水平線
    D1, D2 = 0.85, 0.45
    dashed(d, ox, Y(D1), ox + xl, Y(D1), LGRAY, 1, 6, 5); ctext(d, ox - 8, Y(D1), "D1", FT, GRAY, "rm")
    d.line((ox, Y(D2), ox + xl, Y(D2)), fill=GREEN, width=2); ctext(d, ox + xl + 6, Y(D2), "D2", FT, GREEN, "lm")
    # 応答: D1から急収縮しD2を行き過ぎ、減衰リバウンド
    pts = []
    for i in range(121):
        t = i / 120
        if t < 0.12:
            v = D1
        else:
            tt = (t - 0.12) / 0.88
            osc = math.exp(-3.0 * tt) * math.cos(2 * math.pi * 2.2 * tt)
            v = D2 + (D1 - D2) * osc * 1.15
        pts.append((X(t), Y(max(v, 0.05))))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, X(0.22), Y(0.12), "深く収縮(行き過ぎ)", FT, RED)
    ctext(d, X(0.6), Y(0.72), "減衰リバウンド", FT, BLUE)
    ctext(d, X(0.9), Y(D2) - 26, "D2 に収束", FT, GREEN)
    note(d, "D1から急収縮しD2を通り越し, 減衰しながら跳ね返ってD2に落ち着く")
    save(im, "t1e15StepPressureResponse")


# 15-22 t1e15CavitationCFD : 均質媒体モデルの限界(helpful)
def cavitation_cfd():
    im, d = new(); title(d, "均質媒体モデル: 格子より大きい界面はぼやける")
    # 左: 実際の鋭い界面
    ctext(d, 175, 90, "実際: 鋭い気液界面", FS, BLUE)
    x0, y0, c = 70, 110, 42
    for i in range(6):
        for j in range(5):
            d.rectangle((x0 + j * c, y0 + i * c, x0 + j * c + c, y0 + i * c + c), outline=LGRAY, width=1)
    # 鋭い界面(曲線)
    sharp = []
    for i in range(41):
        t = i / 40; sharp.append((x0 + 20 + t * 170, y0 + 40 + 130 * (t ** 1.5)))
    d.line(sharp, fill=BLUE, width=3, joint="curve")
    ctext(d, x0 + 60, y0 + 40, "蒸気", FT, BLUE)
    ctext(d, x0 + 150, y0 + 200, "液", FT, GRAY)
    # 右: 平均化(格子より小さい気泡群でぼやける)
    ctext(d, 480, 90, "モデル: 気泡群に平均化", FS, RED)
    x0 = 400
    for i in range(6):
        for j in range(5):
            # ボイド率をグレー濃淡で
            t = 1 - ((i * 5 + j) / 30)
            g = int(200 - 90 * t) if (i + j) < 6 else 245
            xa, ya = x0 + j * c, y0 + i * c
            d.rectangle((xa, ya, xa + c, ya + c), outline=LGRAY, width=1,
                        fill=(g, g, min(255, g + 30)))
            if (i + j) < 6:
                pcircle(d, xa + c / 2, ya + c / 2, 4, BLUE, BLUE, 1)
    ctext(d, x0 + 100, y0 + 230, "鋭い界面が再現しにくい", FT, RED)
    arrow(d, 320, 220, 380, 220, GRAY, 3, 12)
    note(d, "格子より大きいキャビティを格子より小さい気泡群として扱う -> 界面がぼやける")
    save(im, "t1e15CavitationCFD")


# ============================================================
# ===============  公式・用語カード  t1f15*  =================
# ============================================================

# t1f15-1 飽和蒸気圧と蒸発潜熱
def f_saturation_latent_heat():
    im, d = new(); title(d, "飽和蒸気圧と蒸発潜熱")
    box(d, 90, 90, 570, 165, FILL2)
    ctext(d, 330, 118, "p_sat = p_sat(T)", FS)
    ctext(d, 330, 146, "L = h_g - h_f  (比エンタルピー差)", FS)
    # 潜熱が温度で減少し臨界点で0
    ox, oy = 120, 350; xl, yl = 260, 150
    axes(d, ox, oy, xl, yl, "温度 T", "潜熱 L")
    pts = []
    for i in range(101):
        t = i / 100; v = (1 - t) ** 0.5
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    ctext(d, ox + xl, oy - 10, "臨界点でL=0", FT, GRAY, "rm")
    ctext(d, 470, 210, "飽和蒸気圧は温度のみの関数", FT, BLUE)
    ctext(d, 470, 245, "潜熱=気液の比エンタルピー差", FT)
    ctext(d, 470, 280, "温度上昇で減少", FT)
    ctext(d, 470, 312, "臨界点でゼロ", FT, RED)
    note(d, "水は1気圧100℃で潜熱約2257 kJ/kg. 臨界点(約374℃)でゼロ")
    save(im, "t1f15SaturationLatentHeat")


# t1f15-2 沸騰とキャビテーション
def f_boiling_vs_cavitation():
    im, d = new(); title(d, "沸騰 と キャビテーション(液体の張力)")
    box(d, 45, 100, 320, 350, FILL1)
    ctext(d, 182, 124, "沸騰", FS, ORANGE)
    ctext(d, 182, 158, "温度が飽和温度を", FT)
    ctext(d, 182, 184, "十分上回って生じる", FT)
    ctext(d, 182, 226, "温度側の相変化", FS, ORANGE)
    ctext(d, 182, 268, "伝熱面のキャビティ内", FT, GRAY)
    ctext(d, 182, 294, "の蒸気泡が成長", FT, GRAY)
    box(d, 340, 100, 615, 350, FILL2)
    ctext(d, 477, 124, "キャビテーション", FS, BLUE)
    ctext(d, 477, 158, "圧力が飽和蒸気圧を", FT)
    ctext(d, 477, 184, "十分下回って生じる", FT)
    ctext(d, 477, 226, "圧力側の相変化", FS, BLUE)
    ctext(d, 477, 268, "液体は張力(負圧)に", FT, GRAY)
    ctext(d, 477, 294, "なり得る", FT, GRAY)
    note(d, "温度側=沸騰 / 圧力側=キャビテーション の裏返しの関係")
    save(im, "t1f15BoilingVsCavitation")


# t1f15-3 プール沸騰曲線の4領域
def f_boiling_curve():
    im, d = new(); title(d, "プール沸騰曲線の4領域")
    ox, oy = 100, 350; xl, yl = 470, 280
    axes(d, ox, oy, xl, yl, "壁面過熱度", "熱流束")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    pts = []
    for i in range(101):
        t = i / 100
        if t < 0.22: v = 0.05 + 1.0 * t
        elif t < 0.45: v = min(0.27 + 2.9 * (t - 0.22), 0.95)
        elif t < 0.70: v = max(0.95 - 2.4 * (t - 0.45), 0.35)
        else: v = 0.35 + 1.4 * (t - 0.70)
        pts.append((X(t), Y(v)))
    d.line(pts, fill=BLACK, width=3, joint="curve")
    bounds = [0.0, 0.22, 0.45, 0.70, 1.0]
    labs = ["液体単相", "核沸騰", "遷移沸騰", "膜沸騰"]
    cols = [GRAY, BLUE, ORANGE, RED]
    for k in range(4):
        xa, xb = X(bounds[k]), X(bounds[k + 1])
        if k > 0: dashed(d, xa, oy, xa, oy - yl, LGRAY, 1, 6, 5)
        ctext(d, (xa + xb) / 2, oy + 20, labs[k], FT, cols[k])
    ctext(d, X(0.45), Y(0.98), "ピーク(CHF)", FT, RED)
    note(d, "液体単相->核沸騰->遷移沸騰->膜沸騰. 遷移沸騰で熱流束が一度下がる")
    save(im, "t1f15BoilingCurve")


# t1f15-4 DNBと熱流束の式
def f_dnb():
    im, d = new(); title(d, "DNB と 熱流束の式  q'' = h(T - T_b)")
    box(d, 120, 90, 540, 150, FILL2)
    ctext(d, 330, 120, "q'' = h (T - T_b),   Delta T = q''/h", FS)
    ctext(d, 330, 185, "核沸騰(h大) -> 膜沸騰(h小) への遷移=DNB", FT, BLUE)
    ctext(d, 330, 220, "q'' 一定で h が1桁下がると", FT)
    ctext(d, 330, 250, "Delta T が10倍に -> 焼損(バーンアウト)", FS, RED)
    # 例
    box(d, 120, 285, 540, 355, FILL1)
    ctext(d, 330, 308, "例: q''=2.5e5, h:2.5e4->2.5e3", FT, GRAY)
    ctext(d, 330, 335, "Delta T: 10 K -> 100 K (増加90 K)", FT, GRAY)
    note(d, "熱流束一定なら温度差は熱伝達率に反比例する")
    save(im, "t1f15DNB")


# t1f15-5 サブクール沸騰
def f_subcooled_boiling():
    im, d = new(); title(d, "サブクール沸騰")
    wall(d, 120, 100, 340, side=1, n=13)
    ctext(d, 108, 92, "加熱壁", FT, GRAY, "rm")
    xsat = 360; dashed(d, xsat, 100, xsat, 340, GRAY, 2, 8, 5)
    ctext(d, xsat, 84, "沸点", FT, GRAY)
    prof = []
    for i in range(101):
        t = i / 100
        temp = 400 - 200 * (1 - math.exp(-3.2 * t))
        prof.append((120 + (temp - 190) * 1.05, 110 + t * 210))
    d.line(prof, fill=RED, width=3, joint="curve")
    for yy in (150, 190, 230, 270):
        pcircle(d, 138, yy, 6, (235, 242, 250), BLUE, 2)
    ctext(d, 200, 155, "壁近傍=沸点超え", FT, RED, "lm")
    ctext(d, 250, 300, "バルク=沸点未満", FT, BLUE, "lm")
    ctext(d, 480, 200, "サブクール度が小さくなると", FT, GRAY)
    ctext(d, 480, 228, "気泡が壁面から離脱", FT, GRAY)
    note(d, "バルクは冷たくても加熱面近傍だけ沸騰. 焼損は飽和沸騰でも起こる")
    save(im, "t1f15SubcooledBoiling")


# t1f15-6 ラプラス則
def f_laplace():
    im, d = new(); title(d, "ラプラス則 と 沸騰開始条件  Delta p = 2 sigma / R")
    box(d, 150, 90, 510, 150, FILL2)
    ctext(d, 330, 120, "Delta p = 2 sigma / R", F)
    cx, cy, R = 180, 265, 60
    pcircle(d, cx, cy, R, (235, 242, 250), BLUE, 3)
    ctext(d, cx, cy, "p_in", FT, RED)
    arrow(d, cx, cy, cx + R, cy, GRAY, 2, 9); ctext(d, cx + R - 14, cy - 14, "R", FT, GRAY)
    ctext(d, cx, cy + R + 20, "外圧 p_out", FT, BLACK)
    ctext(d, 470, 200, "R が小さいほど過剰圧 大", FT, RED)
    ctext(d, 470, 235, "微小核ほど内圧が高い", FT)
    ctext(d, 470, 275, "沸騰開始には壁温が", FT, GRAY)
    ctext(d, 470, 300, "飽和温度を超過して必要", FT, GRAY)
    note(d, "R=1um, sigma=0.072 なら Delta p≈1.44e5 Pa(約1気圧). 係数は2")
    save(im, "t1f15Laplace")


# t1f15-7 管内流動沸騰の流動様式
def f_flow_regimes():
    im, d = new(); title(d, "管内流動沸騰の流動様式(下から上へ)")
    cx = 175; y0, y1 = 75, 400; hw = 44
    vtube(d, cx, y0, y1, hw)
    arrow(d, cx, 405, cx, 365, GRAY, 2, 11)
    for (px, py) in [(cx - 18, 358), (cx + 12, 348), (cx - 3, 338), (cx + 22, 356)]:
        pcircle(d, px, py, 6, (235, 242, 250), BLUE, 2)
    ctext(d, cx + hw + 20, 350, "気泡流(核沸騰)", FT, BLACK, "lm")
    d.ellipse((cx - 28, 270, cx + 28, 315), outline=BLUE, width=2, fill=(235, 242, 250))
    ctext(d, cx + hw + 20, 292, "スラグ流", FT, BLACK, "lm")
    d.rectangle((cx - hw, 190, cx - hw + 8, 250), fill=(210, 225, 245))
    d.rectangle((cx + hw - 8, 190, cx + hw, 250), fill=(210, 225, 245))
    for (px, py) in [(cx, 205), (cx - 10, 228), (cx + 12, 240)]:
        pcircle(d, px, py, 3, BLUE, BLUE, 1)
    ctext(d, cx + hw + 20, 220, "環状噴霧流(強制対流蒸発)", FT, BLACK, "lm")
    for (px, py) in [(cx - 12, 115), (cx + 10, 135), (cx + 18, 105), (cx, 150)]:
        pcircle(d, px, py, 3, BLUE, BLUE, 1)
    ctext(d, cx + hw + 20, 128, "噴霧流(壁が乾く)", FT, BLACK, "lm")
    note(d, "上向きにクオリティ・ボイド率が増加. 気泡流->スラグ流->環状噴霧流->噴霧流")
    save(im, "t1f15FlowRegimes")


# t1f15-8 ドライアウトとポスト・ドライアウト
def f_dryout():
    im, d = new(); title(d, "ドライアウト と ポスト・ドライアウト")
    ox, oy = 90, 340; xl, yl = 480, 250
    axes(d, ox, oy, xl, yl, "位置(クオリティ増加 ->)", "壁温")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    # 壁温: ドライアウトまで低い -> 急上昇
    pts = []
    for i in range(101):
        t = i / 100
        if t < 0.62: v = 0.2 + 0.1 * t
        else: v = 0.26 + 3.0 * (t - 0.62)
        pts.append((X(t), Y(min(v, 0.95))))
    d.line(pts, fill=RED, width=3, joint="curve")
    dashed(d, X(0.62), oy, X(0.62), oy - yl, GRAY, 2, 7, 5)
    ctext(d, X(0.62), oy - yl - 12, "ドライアウト(液膜消失)", FT, GRAY)
    ctext(d, X(0.3), Y(0.35), "強制対流蒸発", FT, BLUE)
    ctext(d, X(0.85), Y(0.85), "ポスト・ドライアウト", FT, RED)
    ctext(d, X(0.85), Y(0.72), "熱伝達率急減・壁温急上昇", FT, GRAY)
    note(d, "液膜は液滴の付着・離脱の収支で決まる. クオリティ1未満でも起こり得る")
    save(im, "t1f15Dryout")


# t1f15-9 CHFのドライアウト型とDNB型
def f_chf_types():
    im, d = new(); title(d, "限界熱流束(CHF)のドライアウト型 と DNB型")
    box(d, 45, 95, 320, 340, FILL1)
    ctext(d, 182, 120, "ドライアウト型", FS, BLUE)
    for i, s in enumerate(["環状流の液膜消失", "低流量・長い加熱管",
                           "壁温上昇はゆるやか", "蒸気流の冷却が効く"]):
        ctext(d, 182, 160 + i * 40, s, FT)
    box(d, 340, 95, 615, 340, FILL2)
    ctext(d, 477, 120, "DNB型", FS, RED)
    for i, s in enumerate(["核沸騰->膜沸騰の遷移", "高流量・短い加熱管・大内径",
                           "壁温上昇が急激", "クオリティ負でも起こり得る"]):
        ctext(d, 477, 160 + i * 40, s, FT)
    note(d, "両者の境界は必ずしも明確でない. 壁温上昇はDNB型が急激")
    save(im, "t1f15CHFtypes")


# t1f15-10 均一加熱円管の出口クオリティ
def f_exit_quality():
    im, d = new(); title(d, "均一加熱円管の出口クオリティ")
    box(d, 90, 90, 570, 155, FILL2)
    ctext(d, 330, 122, "x = (1/h_V) ( 4qL/GD - h_IN )", F)
    # 管の絵
    y0, y1 = 200, 250
    d.line((110, y0, 470, y0), fill=BLACK, width=3); d.line((110, y1, 470, y1), fill=BLACK, width=3)
    arrow(d, 70, 225, 108, 225, BLUE, 3, 12); ctext(d, 88, 275, "入口\nサブクール", FT, BLUE)
    for xx in range(150, 460, 55):
        arrow(d, xx, 170, xx, 198, RED, 2, 8)
    ctext(d, 290, 285, "一定熱流束 q", FT, RED)
    arrow(d, 472, 225, 510, 225, GRAY, 3, 12); ctext(d, 500, 275, "出口\nx 最大", FT, GRAY)
    ctext(d, 330, 330, "h_IN の差し引きを忘れると誤答(0.20)", FT, GRAY)
    note(d, "例: q=5e5,L=2,D=0.01,G=1000,h_V=2e6,h_IN=2e5 -> x=0.10")
    save(im, "t1f15ExitQuality")


# t1f15-11 沸騰流れ計算と熱伝達相関式
def f_boiling_model():
    im, d = new(); title(d, "沸騰流れ計算と熱伝達相関式")
    ox, oy = 70, 200; xl = 540
    arrow(d, ox, oy, ox + xl, oy, BLACK, 2, 11); ctext(d, ox + xl + 6, oy, "壁面温度", FT, BLACK, "lm")
    labs = ["単相強制対流", "核沸騰", "遷移沸騰", "膜沸騰"]
    cols = [GRAY, BLUE, ORANGE, RED]; bw = xl / 4
    for k in range(4):
        xa = ox + k * bw
        d.rectangle((xa, oy - 40, xa + bw - 6, oy - 6), outline=cols[k], width=2, fill=FILL1)
        ctext(d, xa + bw / 2 - 3, oy - 23, labs[k], FT, cols[k])
    ctext(d, ox + xl / 2, oy - 60, "様式ごとに異なる相関式(判別=壁温・体積占有率)", FT, GRAY)
    box(d, 200, 290, 460, 350, FILL2); ctext(d, 330, 320, "実験データ", FS, GREEN)
    arrow(d, 330, 288, 330, 235, GREEN, 3, 13); ctext(d, 350, 262, "相関式へ", FT, GREEN, "lm")
    note(d, "相関式は実験ベース(理論厳密導出でない). 物性の圧力依存も考慮で精度向上")
    save(im, "t1f15BoilingModel")


# t1f15-12 Nusseltの膜状凝縮
def f_film_condensation():
    im, d = new(); title(d, "Nusseltの膜状凝縮(局所熱流束と液膜厚)")
    box(d, 55, 82, 605, 150, FILL2)
    ctext(d, 200, 116, "q_x = lambda(T_S - T_W)/delta", FS)
    ctext(d, 470, 116, "delta_x ∝ x^(1/4)", FS)
    # 冷却壁と液膜
    wall(d, 130, 170, 380, side=-1, n=12)
    ctext(d, 118, 165, "T_W", FT, BLUE, "lm")
    film = [(130, 170)]
    for i in range(41):
        t = i / 40; film.append((130 + 8 + 45 * (t ** 0.25), 170 + t * 205))
    film.append((130, 375)); d.polygon(film, fill=(210, 225, 245))
    d.line(film[1:-1], fill=BLUE, width=3, joint="curve")
    ctext(d, 235, 190, "T_S=飽和温度", FT, RED, "lm")
    yy = 290; xf = 130 + 8 + 45 * (((yy - 170) / 205) ** 0.25)
    dim(d, 130, yy, xf, yy, "delta", col=GRAY)
    arrow(d, 400, 170, 400, 375, GRAY, 2, 11); ctext(d, 412, 275, "x", FS, GRAY, "lm")
    ctext(d, 500, 210, "液膜が薄いほど熱流束大", FT)
    ctext(d, 500, 245, "下流ほど delta 厚く", FT)
    ctext(d, 500, 275, "-> 局所熱流束は減少", FT, RED)
    note(d, "例: lambda=0.68, T差20K, delta=1e-4 -> q_x≈1.36e5 W/m^2")
    save(im, "t1f15FilmCondensation")


# t1f15-13 キャビテーションの形態
def f_cavitation_forms():
    im, d = new(); title(d, "キャビテーションの形態")
    _cav_forms(d, 45, 60, 420, 300)
    box(d, 480, 80, 620, 350, FILL1)
    ctext(d, 550, 105, "特徴", FS)
    ctext(d, 550, 145, "バブル=移動", FT, GRAY)
    ctext(d, 550, 180, "シート=付着", FT, GRAY)
    ctext(d, 550, 215, "クラウド=雲状", FT, GRAY)
    ctext(d, 550, 250, "(激しい壊食)", FT, GRAY)
    ctext(d, 550, 285, "ボルテックス", FT, GRAY)
    ctext(d, 550, 312, "=渦コアのひも", FT, GRAY)
    note(d, "水より油の方が溶存ガスの影響を強く受けやすい")
    save(im, "t1f15CavitationForms")


# t1f15-14 気泡核の初生(臨界サイズ)
def f_nucleus_critical():
    im, d = new(); title(d, "気泡核の初生(臨界サイズ)")
    # 臨界サイズより小=安定(収縮), 大=膨張(初生)
    box(d, 45, 100, 320, 350, FILL1)
    ctext(d, 182, 124, "臨界サイズより小", FS, BLUE)
    pcircle(d, 182, 200, 26, (235, 242, 250), BLUE, 2)
    for a in (45, 135, 225, 315):
        ax = 182 + 40 * math.cos(math.radians(a)); ay = 200 - 40 * math.sin(math.radians(a))
        arrow(d, ax, ay, 182 + 28 * math.cos(math.radians(a)), 200 - 28 * math.sin(math.radians(a)), BLUE, 2, 9)
    ctext(d, 182, 270, "表面張力で安定", FT)
    ctext(d, 182, 300, "-> 収縮側", FS, BLUE)
    box(d, 340, 100, 615, 350, FILL2)
    ctext(d, 477, 124, "臨界サイズより大", FS, RED)
    pcircle(d, 477, 205, 34, (240, 235, 235), RED, 3)
    for a in (45, 135, 225, 315):
        ax = 477 + 40 * math.cos(math.radians(a)); ay = 205 - 40 * math.sin(math.radians(a))
        arrow(d, ax, ay, 477 + 58 * math.cos(math.radians(a)), 205 - 58 * math.sin(math.radians(a)), RED, 2, 9)
    ctext(d, 477, 285, "内圧が表面張力に勝つ", FT)
    ctext(d, 477, 315, "-> 膨張して初生", FS, RED)
    note(d, "圧力が下がるほど臨界サイズは小さくなり初生しやすい")
    save(im, "t1f15NucleusCritical")


# t1f15-15 キャビテーション数
def f_cavitation_number():
    im, d = new(); title(d, "キャビテーション数")
    box(d, 150, 95, 510, 175, FILL2)
    ctext(d, 330, 122, "sigma = (p - p_v) / ((1/2) rho U^2)", FS)
    ctext(d, 330, 152, "分子=静圧-飽和蒸気圧, 分母=動圧", FT, GRAY)
    ctext(d, 330, 220, "sigma 大 -> 発生しにくい", FS, BLUE)
    ctext(d, 330, 255, "sigma 小 -> 発生しやすい", FS, RED)
    ctext(d, 330, 295, "U 大で動圧増 -> sigma 小 / p_v 小 -> sigma 大", FT, GRAY)
    note(d, "例: p=5.234e4, p_v=2.34e3, rho=1000, U=10 -> sigma=1.0")
    save(im, "t1f15CavitationNumber")


# t1f15-16 エアレーション
def f_aeration():
    im, d = new(); title(d, "エアレーション(ガスキャビテーション)")
    box(d, 55, 95, 320, 345, FILL1)
    ctext(d, 187, 120, "溶存空気の析出(脱ガス)", FT, BLUE)
    ctext(d, 187, 155, "不凝縮ガス(空気)が", FT)
    ctext(d, 187, 182, "圧力低下で過飽和->気泡", FT)
    ctext(d, 187, 224, "油の空気溶解度は", FT, GRAY)
    ctext(d, 187, 250, "水より1桁大きい", FT, GRAY)
    ctext(d, 187, 292, "蒸気キャビとは別物", FS, RED)
    box(d, 340, 95, 615, 345, FILL2)
    ctext(d, 477, 120, "圧力の関係", FS)
    ox = 370; oy = 250; xl = 210
    arrow(d, ox, oy, ox + xl, oy, BLACK, 2, 10); ctext(d, ox + xl + 6, oy, "圧力", FT, BLACK, "lm")
    d.line((ox + 150, oy - 7, ox + 150, oy + 7), fill=GREEN, width=3); ctext(d, ox + 150, oy - 22, "空気分離圧", FT, GREEN)
    d.line((ox + 50, oy - 7, ox + 50, oy + 7), fill=RED, width=3); ctext(d, ox + 50, oy + 22, "飽和蒸気圧", FT, RED)
    ctext(d, 477, 305, "分離圧≠飽和蒸気圧", FT, GRAY)
    note(d, "分離圧は溶解度・実験方法で大きく変化する物性値でない圧力")
    save(im, "t1f15Aeration")


# t1f15-17 気泡成長速度(慣性支配)
def f_bubble_growth():
    im, d = new(); title(d, "キャビテーション気泡の成長速度(慣性支配)")
    box(d, 130, 95, 530, 160, FILL2)
    ctext(d, 330, 127, "(dR/dt)^2 = (p_sv - p_L)/rho_L", FS)
    cx, cy, R = 175, 285, 55
    dashed(d, cx, cy, cx + 30, cy, GRAY, 1, 4, 4)
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), outline=GRAY, width=2)
    pcircle(d, cx, cy, R, (235, 242, 250), BLUE, 3)
    for a in (30, 150, 270):
        ax = cx + (R - 4) * math.cos(math.radians(a)); ay = cy - (R - 4) * math.sin(math.radians(a))
        arrow(d, ax, ay, cx + (R + 28) * math.cos(math.radians(a)), cy - (R + 28) * math.sin(math.radians(a)), RED, 3, 11)
    ctext(d, cx, cy, "p_sv", FT, BLUE)
    ctext(d, 470, 210, "圧力差が大きいほど", FT)
    ctext(d, 470, 240, "速く成長する", FT)
    ctext(d, 470, 278, "p_L 一定なら R ∝ t", FT, GRAY)
    ctext(d, 470, 308, "熱律速では R ∝ t^(1/2)", FT, GRAY)
    note(d, "例: p_sv-p_L=4e3, rho_L=1000 -> (dR/dt)^2=4, dR/dt=2 m/s")
    save(im, "t1f15BubbleGrowth")


# t1f15-18 Rayleigh-Plesset式
def f_rayleigh_plesset():
    im, d = new(); title(d, "Rayleigh-Plesset 式")
    box(d, 40, 88, 620, 165, FILL2)
    ctext(d, 330, 112, "R d2R/dt2 + (3/2)(dR/dt)^2 =", FS)
    ctext(d, 330, 142, "(1/rho_L)( p_G - 2sigma/R - (4 eta_L/R) dR/dt - p_L )", FT)
    # ステップ加圧応答の小グラフ
    ox, oy = 90, 350; xl, yl = 280, 160
    axes(d, ox, oy, xl, yl, "t", "D")
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    D1, D2 = 0.85, 0.4
    d.line((ox, Y(D2), ox + xl, Y(D2)), fill=GREEN, width=2); ctext(d, ox + xl + 4, Y(D2), "D2", FT, GREEN, "lm")
    pts = []
    for i in range(121):
        t = i / 120
        if t < 0.1: v = D1
        else:
            tt = (t - 0.1) / 0.9
            v = D2 + (D1 - D2) * math.exp(-3.0 * tt) * math.cos(2 * math.pi * 2.2 * tt) * 1.15
        pts.append((X(t), Y(max(v, 0.04))))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, 470, 220, "非線形の運動方程式", FT)
    ctext(d, 470, 252, "p_G=p_v+p_g(蒸気+ガス)", FT, GRAY)
    ctext(d, 470, 285, "ステップ加圧->深く収縮", FT)
    ctext(d, 470, 315, "+減衰リバウンドでD2へ", FT, BLUE)
    note(d, "液体の圧縮性を含まないため崩壊時の最小半径を過小評価する")
    save(im, "t1f15RayleighPlesset")


# t1f15-19 気泡崩壊と液体の圧縮性
def f_collapse_compressibility():
    im, d = new(); title(d, "気泡崩壊と液体の圧縮性(Fujikawa-Akamatsu式)")
    cx, cy, R = 165, 205, 55
    pcircle(d, cx, cy, R, (240, 235, 235), RED, 3)
    ctext(d, cx, cy, "高温高圧", FT, RED)
    for a in (30, 150, 270):
        ax = cx + (R + 28) * math.cos(math.radians(a)); ay = cy - (R + 28) * math.sin(math.radians(a))
        arrow(d, ax, ay, cx + (R + 4) * math.cos(math.radians(a)), cy - (R + 4) * math.sin(math.radians(a)), RED, 3, 11)
    ctext(d, cx, cy + R + 26, "壁速度->液体音速", FT, RED)
    box(d, 320, 95, 620, 350, FILL1)
    ctext(d, 470, 120, "崩壊時に起こること", FS)
    for i, s in enumerate(["収縮は成長より速い",
                           "圧力上昇=壊食(1GPa以上)",
                           "温度上昇=発光(約1万℃)",
                           "界面で蒸気の凝縮",
                           "液体の圧縮性が効く"]):
        ctext(d, 470, 158 + i * 34, s, FT, RED if i in (1, 2) else BLACK)
    ctext(d, 470, 330, "-> Fujikawa-Akamatsu式で扱う", FT, GREEN)
    note(d, "R-P式は圧縮性・界面の蒸発凝縮を含まない. 発光=ソノルミネッセンス")
    save(im, "t1f15CollapseCompressibility")


# t1f15-20 均質媒体モデルの限界
def f_homogeneous_model():
    im, d = new(); title(d, "均質媒体モデルによる数値計算の限界")
    x0, y0, c = 70, 105, 40
    for i in range(6):
        for j in range(6):
            t = 1 - ((i + j) / 10)
            fill = (int(210 - 80 * max(t, 0)), int(220 - 40 * max(t, 0)), 250) if (i + j) < 7 else "white"
            d.rectangle((x0 + j * c, y0 + i * c, x0 + j * c + c, y0 + i * c + c), outline=LGRAY, width=1, fill=fill)
            if (i + j) < 7:
                pcircle(d, x0 + j * c + c / 2, y0 + i * c + c / 2, 3, BLUE, BLUE, 1)
    ctext(d, x0 + 120, y0 + 6 * c + 20, "格子より小さい気泡群に平均化", FT, GRAY)
    box(d, 360, 120, 620, 340, FILL1)
    ctext(d, 490, 145, "本質的な限界", FS)
    for i, s in enumerate(["格子より大きい界面は",
                           "  正確に再現しにくい",
                           "単相の乱流モデルは不適",
                           "  (乱流粘性を過大評価)",
                           "飽和蒸気圧以下でも",
                           "  必ず生じるとは限らない"]):
        ctext(d, 490, 178 + i * 26, s, FT, GRAY)
    note(d, "モデル定数は限られた対象のチューニング値. 万能ではない")
    save(im, "t1f15HomogeneousModel")


# ============================================================
if __name__ == "__main__":
    # --- 問題図 t1e15 (22) ---
    phase_change_map()
    pressure_negative()
    boiling_curve_regions()
    dnb_temp_jump()
    subcool_boiling()
    bubble_nucleus_laplace()
    flow_regime_sequence()
    dryout_droplet()
    chf_mechanism()
    critical_heat_flux_tube()
    boiling_calc_model()
    film_condensation()
    bubble_flow_phase_change()
    cavitation_forms()
    cavitation_number()
    bubble_cavitation()
    aeration()
    bubble_growth_rate()
    bubble_collapse()
    collapse_compressibility()
    step_pressure_response()
    cavitation_cfd()
    # --- 公式・用語図 t1f15 (20) ---
    f_saturation_latent_heat()
    f_boiling_vs_cavitation()
    f_boiling_curve()
    f_dnb()
    f_subcooled_boiling()
    f_laplace()
    f_flow_regimes()
    f_dryout()
    f_chf_types()
    f_exit_quality()
    f_boiling_model()
    f_film_condensation()
    f_cavitation_forms()
    f_nucleus_critical()
    f_cavitation_number()
    f_aeration()
    f_bubble_growth()
    f_rayleigh_plesset()
    f_collapse_compressibility()
    f_homogeneous_model()
    print("done ch15")
