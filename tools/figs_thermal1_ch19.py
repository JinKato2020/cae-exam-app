# -*- coding: utf-8 -*-
"""熱流体力学1級 第19章「燃焼反応」の問題図(t1e19*・14枚)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(phi, alpha, beta, omega, log, ->, <->, H2, O2, CH4, CO2, H2O, PAH, C2H2 等)。
required図(回答前)には答え・正解値・結論を描かない。helpful図(回答後)は補足説明。"""
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
# 19-1 t1e19MechScale : 詳細化学反応機構の規模対比(helpful)
# ============================================================
def mech_scale():
    im, d = new(); title(d, "詳細化学反応機構: 素反応の集合が機構を成す(規模の対比)")
    # 左: 水素系(小さな箱・素反応 数十)
    box(d, 55, 110, 275, 330, (235, 242, 250))
    ctext(d, 165, 132, "水素-空気系", FS, BLUE)
    ctext(d, 165, 158, "素反応の集合が小さい", FT, GRAY)
    # 小さな矢印(素反応)を少数
    for (px, py) in [(105, 200), (165, 200), (225, 200),
                     (105, 250), (165, 250), (225, 250)]:
        arrow(d, px - 18, py, px + 18, py, BLUE, 2, 9)
    ctext(d, 165, 300, "1つ1つが素反応", FT, GRAY)
    # 右: 炭化水素系(大きな箱・素反応 数百)
    box(d, 355, 80, 630, 360, (250, 240, 235))
    ctext(d, 492, 104, "炭化水素(メタン等)-空気系", FT, RED)
    ctext(d, 492, 128, "素反応の集合がはるかに大きい", FT, GRAY)
    for row in range(6):
        for col in range(7):
            px = 385 + col * 36
            py = 165 + row * 28
            arrow(d, px - 12, py, px + 12, py, RED, 1, 6)
    ctext(d, 492, 345, "多数の素反応が連立", FT, GRAY)
    # 中央: 大小の対比
    ctext(d, 315, 220, "<", FL, BLACK)
    note(d, "素反応の数だけ化学種・連立ODEが増える(具体的な本数は各自)")
    save(im, "t1e19MechScale")


# ============================================================
# 19-2 t1e19H2ChainFlow : 水素酸化の連鎖反応フロー(helpful)
# ============================================================
def h2_chain_flow():
    im, d = new(); title(d, "水素酸化の連鎖: 起鎖 -> 分枝 -> (競合する三体) -> 再結合")
    stages = [
        (105, "起鎖反応", "分子から活性基が生成", BLUE, False),
        (255, "連鎖分枝", "活性基が急増(1個->2個)", RED, False),
        (405, "三体再結合", "分枝と競合(第三体M)", ORANGE, True),
        (555, "再結合", "活性基が失活+発熱", GREEN, False),
    ]
    for (cx, head, sub, col, dash) in stages:
        if dash:
            dashed(d, cx - 55, 130, cx + 55, 130, ORANGE, 3, 10, 6)
            dashed(d, cx - 55, 250, cx + 55, 250, ORANGE, 3, 10, 6)
            dashed(d, cx - 55, 130, cx - 55, 250, ORANGE, 3, 10, 6)
            dashed(d, cx + 55, 130, cx + 55, 250, ORANGE, 3, 10, 6)
        else:
            d.rectangle((cx - 55, 130, cx + 55, 250), outline=col, width=3, fill=(250, 250, 250))
        ctext(d, cx, 155, head, FT, col)
        ctext(d, cx, 200, sub, FT, GRAY)
    # 活性基の丸(H/OH/O)
    for (cx, labs) in [(105, ["H"]), (255, ["OH", "O"]), (405, ["H"]), (555, ["H2O"])]:
        for i, lab in enumerate(labs):
            pcircle(d, cx - 20 + i * 40, 228, 15, FILL1, BLACK, 2)
            ctext(d, cx - 20 + i * 40, 228, lab, FT, BLACK)
    # 段間の矢印
    for x in [160, 310, 460]:
        arrow(d, x, 190, x + 40, 190, BLACK, 3, 12)
    # 分枝と三体の競合(下向き注記)
    ctext(d, 330, 300, "分枝(反応b)と三体再結合(反応c)は同じ H+O2 を奪い合う", FT, GRAY)
    ctext(d, 330, 328, "この競合が第2爆発限界を決める", FT, GRAY)
    note(d, "破線枠=第三体Mが関与する枝. 具体的な反応式は各自")
    save(im, "t1e19H2ChainFlow")


# ============================================================
# 19-3 t1e19GlobalRateOrder : 総括反応モデル(helpful)
# ============================================================
def global_rate_order():
    im, d = new(); title(d, "総括反応モデル: 多数の素反応を1本にまとめた経験式")
    # 左: 多数の素反応(細い矢印の束)
    box(d, 45, 110, 250, 340, (250, 250, 250))
    ctext(d, 147, 132, "多数の素反応", FT, BLUE)
    for row in range(7):
        yy = 165 + row * 24
        arrow(d, 70, yy, 225, yy, BLUE, 1, 7)
    ctext(d, 147, 320, "分子レベルの実反応", FT, GRAY)
    # 束ねる矢印(集約)
    arrow(d, 258, 225, 340, 225, BLACK, 4, 16)
    ctext(d, 300, 200, "束ねる", FT, GRAY)
    # 右: 1本の太い矢印(総括反応)
    box(d, 350, 150, 630, 300, (235, 245, 235))
    ctext(d, 490, 178, "総括反応(1段)", FS, GREEN)
    arrow(d, 375, 225, 605, 225, GREEN, 7, 22)
    ctext(d, 490, 258, "CH4 + 2 O2 -> CO2 + 2 H2O", FT, BLACK)
    # 速度式の枠(次数だけ・数値なし)
    box(d, 200, 355, 460, 400, FILL2)
    ctext(d, 330, 378, "omega = k [CH4]^alpha [O2]^beta", FS, BLACK)
    note(d, "反応次数 alpha,beta は実験へのあてはめ量(化学量論係数とは限らない)")
    save(im, "t1e19GlobalRateOrder")


# ============================================================
# 19-4 t1e19PotentialEnergyCurves : ポテンシャル曲線A/B/C(required)
# ============================================================
def potential_energy_curves():
    im, d = new(); title(d, "反応過程に対するポテンシャルエネルギー(3曲線 A,B,C)")
    ox, oy, xl, yl = 90, 350, 500, 260
    # 軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "反応過程", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "ポテンシャルE", FT, BLACK, "rm")
    # 共通の反応物レベル(左端)
    r_y = oy - 0.35 * yl
    dashed(d, ox, r_y, ox + 60, r_y, GRAY, 1, 6, 5)
    ctext(d, ox + 30, r_y - 14, "反応物", FT, GRAY)
    # 山のピーク位置
    peak_x = ox + xl * 0.48
    # 3曲線: 生成物側の高さが異なる
    def curve(prod_frac, col, lab, peak_frac):
        r_level = 0.35
        p_level = prod_frac
        peak = peak_frac
        pts = []
        for i in range(0, 501):
            t = i / 500
            if t < 0.48:
                # 反応物レベル -> 山
                s = t / 0.48
                v = r_level + (peak - r_level) * (0.5 * (1 - math.cos(math.pi * s)))
            else:
                s = (t - 0.48) / 0.52
                v = peak + (p_level - peak) * (0.5 * (1 - math.cos(math.pi * s)))
            pts.append((ox + t * xl, oy - v * yl))
        d.line(pts, fill=col, width=3, joint="curve")
        # ラベルは生成物側末端に
        ctext(d, ox + xl + 4, oy - p_level * yl, lab, FS, col, "lm")
    curve(0.62, RED, "A", 0.88)     # 生成物が高い
    curve(0.35, BLUE, "B", 0.80)    # 生成物が反応物と同レベル
    curve(0.10, GREEN, "C", 0.72)   # 生成物が低い
    ctext(d, ox + xl * 0.5, oy + 26, "左=反応物, 右=生成物", FT, GRAY)
    note(d, "A/B/C の到達レベルの高低だけを示す(どれが発熱かは各自)")
    save(im, "t1e19PotentialEnergyCurves")


# ============================================================
# 19-5 t1e19EnthalpyCycle : 反応物/生成物のエンタルピー準位(helpful)
# ============================================================
def enthalpy_cycle():
    im, d = new(); title(d, "反応物と生成物のエンタルピー準位(低位/高位発熱量)")
    ox, oy, yl = 110, 330, 240
    # 縦軸(エンタルピー)
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "エンタルピー", FT, BLACK, "rm")
    # 反応物準位(高い)
    ry = oy - 0.80 * yl
    d.line((ox + 30, ry, ox + 200, ry), fill=RED, width=4)
    ctext(d, ox + 115, ry - 16, "反応物 CH4 + 2 O2", FT, RED)
    # 生成物準位(2本: 気相水=低位, 液相水=高位でわずかに低い)
    py_gas = oy - 0.30 * yl   # 気相水(低位): 生成物が少し高い
    py_liq = oy - 0.20 * yl   # 液相水(高位): さらに低い準位
    d.line((ox + 300, py_gas, ox + 470, py_gas), fill=GREEN, width=4)
    ctext(d, ox + 385, py_gas - 16, "生成物 CO2 + 2 H2O(気)", FT, GREEN)
    dashed(d, ox + 300, py_liq, ox + 470, py_liq, GRAY, 2, 8, 5)
    ctext(d, ox + 385, py_liq + 16, "H2O(液)は更に低い準位", FT, GRAY)
    # 落差(発熱)の矢印
    arrow(d, ox + 250, ry, ox + 250, py_gas, BLUE, 3, 13)
    ctext(d, ox + 262, (ry + py_gas) / 2, "低位反応熱", FT, BLUE, "lm")
    arrow(d, ox + 500, ry, ox + 500, py_liq, ORANGE, 3, 13)
    ctext(d, ox + 512, (ry + py_liq) / 2, "高位反応熱", FT, ORANGE, "lm")
    ctext(d, 330, oy + 26, "低位=気相水 / 高位=液相水(潜熱の分だけ高位が大)", FT, GRAY)
    note(d, "準位差が反応熱. 具体的な数値は各自")
    save(im, "t1e19EnthalpyCycle")


# ============================================================
# 19-6 t1e19FallOffCurve : フォールオフ曲線(helpful)
# ============================================================
def fall_off_curve():
    im, d = new(); title(d, "三体再結合のフォールオフ: log k 対 log P")
    ox, oy, xl, yl = 100, 340, 470, 250
    # 軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "log P", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "log k", FS, BLACK, "rm")
    # 低圧漸近線(傾き1)
    lx0, lx1 = ox + 20, ox + 250
    ly0, ly1 = oy - 20, oy - 0.62 * yl
    dashed(d, lx0, ly0, lx1 + 80, ly1 - 60, GRAY, 2, 8, 5)
    ctext(d, ox + 90, oy - 0.30 * yl, "低圧: 傾き1", FT, BLUE)
    # 高圧漸近線(水平 k_inf)
    ky = oy - 0.82 * yl
    dashed(d, ox + 180, ky, ox + xl, ky, GRAY, 2, 8, 5)
    ctext(d, ox + xl - 30, ky - 14, "高圧: k_inf に漸近", FT, RED, "rm")
    # S字曲線(fall-off)
    pts = []
    for i in range(0, 471):
        t = i / 470
        # 低圧で傾き1、高圧で水平
        lo = 0.08 + 0.90 * t          # 低圧漸近(直線)
        hi = 0.82                      # 高圧漸近(水平)
        w = 0.5 * (1 + math.tanh((t - 0.55) * 6))  # 遷移の重み
        v = lo * (1 - w) + hi * w
        v = min(v, 0.82)
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLACK, width=3, joint="curve")
    ctext(d, ox + xl * 0.5, oy - 0.95 * yl, "遷移域 = フォールオフ領域", FT, GRAY)
    note(d, "低圧は圧力比例・高圧は頭打ち. 傾きの数値は各自")
    save(im, "t1e19FallOffCurve")


# ============================================================
# 19-7 t1e19ThirdBody : 第三体Mによる安定化(helpful)
# ============================================================
def third_body():
    im, d = new(); title(d, "第三体M: 余剰エネルギーを持ち去り生成化学種を安定化")
    # 2つのラジカルが結合
    pcircle(d, 180, 175, 26, (250, 235, 235), RED, 3); ctext(d, 180, 175, "A", FS, RED)
    pcircle(d, 260, 175, 26, (235, 242, 250), BLUE, 3); ctext(d, 260, 175, "B", FS, BLUE)
    arrow(d, 210, 175, 232, 175, BLACK, 2, 9)
    ctext(d, 220, 135, "結合", FT, GRAY)
    # 生成物 AB
    arrow(d, 300, 175, 360, 175, BLACK, 3, 13)
    d.rounded_rectangle((375, 148, 470, 205), radius=14, outline=GREEN, width=3, fill=(235, 245, 235))
    ctext(d, 422, 176, "AB(安定)", FT, GREEN)
    # 第三体M が衝突し余剰エネルギーを持ち去る
    pcircle(d, 300, 90, 22, FILL2, BLACK, 2); ctext(d, 300, 90, "M", FS, BLACK)
    arrow(d, 300, 112, 300, 150, BLACK, 2, 11)
    ctext(d, 340, 100, "衝突", FT, GRAY, "lm")
    arrow(d, 320, 90, 400, 60, ORANGE, 3, 12)
    ctext(d, 430, 55, "余剰エネルギーを持ち去る", FT, ORANGE, "lm")
    # 第三体候補(効率の大小=矢印の太さ)
    box(d, 60, 250, 620, 375, (250, 250, 250))
    ctext(d, 340, 272, "第三体効率は化学種ごとに異なる(矢印が太いほど効率大)", FT, BLACK)
    cands = [("H2O", 130, 6), ("CO2", 270, 5), ("N2", 410, 3), ("Ar", 540, 2)]
    for (lab, cx, wd) in cands:
        pcircle(d, cx, 320, 20, FILL1, BLACK, 2); ctext(d, cx, 320, lab, FT, BLACK)
        arrow(d, cx, 355, cx, 335, ORANGE, wd, 10)
    ctext(d, 130, 375, "効率大", FT, GRAY)
    ctext(d, 540, 375, "効率小", FT, GRAY)
    note(d, "有効第三体濃度 = 効率×各成分濃度の和(具体値は各自)")
    save(im, "t1e19ThirdBody")


# ============================================================
# 19-8 t1e19ArrheniusUnits : 頻度係数の単位対比(required)
# ============================================================
def arrhenius_units():
    im, d = new(); title(d, "反応I(二分子)と反応II(三分子)の頻度係数の単位")
    # 左: 反応I(二分子, 濃度2つ)
    box(d, 45, 90, 320, 360, (235, 242, 250))
    ctext(d, 182, 116, "反応I(二分子)", FS, BLUE)
    ctext(d, 182, 150, "omega = [S1][S2] k", FT, BLACK)
    # 濃度2つを丸で
    pcircle(d, 130, 205, 24, FILL1, BLUE, 2); ctext(d, 130, 205, "S1", FT, BLUE)
    pcircle(d, 235, 205, 24, FILL1, BLUE, 2); ctext(d, 235, 205, "S2", FT, BLUE)
    ctext(d, 182, 250, "濃度は2つ", FT, GRAY)
    d.line((70, 285, 295, 285), fill=LGRAY, width=1)
    ctext(d, 182, 310, "頻度係数の単位", FT, BLACK)
    ctext(d, 182, 338, "cm^3 系", FS, RED)
    # 右: 反応II(三分子, 濃度3つ+M)
    box(d, 340, 90, 615, 360, (250, 240, 235))
    ctext(d, 477, 116, "反応II(三分子)", FS, RED)
    ctext(d, 477, 150, "omega = [S1][S2][M] k", FT, BLACK)
    pcircle(d, 400, 205, 22, FILL1, RED, 2); ctext(d, 400, 205, "S1", FT, RED)
    pcircle(d, 477, 205, 22, FILL1, RED, 2); ctext(d, 477, 205, "S2", FT, RED)
    pcircle(d, 554, 205, 22, FILL2, BLACK, 2); ctext(d, 554, 205, "M", FT, BLACK)
    ctext(d, 477, 250, "濃度は3つ(第三体M を含む)", FT, GRAY)
    d.line((365, 285, 590, 285), fill=LGRAY, width=1)
    ctext(d, 477, 310, "頻度係数の単位", FT, BLACK)
    ctext(d, 477, 338, "cm^6 系(次数が違う)", FS, RED)
    note(d, "濃度の次数が違うと単位も違う. cm->m の換算値は各自")
    save(im, "t1e19ArrheniusUnits")


# ============================================================
# 19-9 t1e19SensitivityBars : 感度係数の棒グラフ(required)
# ============================================================
def sensitivity_bars():
    im, d = new(); title(d, "層流燃焼速度に対する素反応の感度係数")
    ox, oy, xl, yl = 90, 235, 470, 150
    # ゼロ基準線と軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "素反応", FT, BLACK, "lm")
    arrow(d, ox, oy + yl, ox, oy - yl, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 2, "感度係数 S", FT, BLACK, "rm")
    ctext(d, ox - 14, oy, "0", FT, GRAY, "rm")
    # 棒(正=上・負=下). 反応1大正, 3大負, 2/4/5小
    bars = [("1", 0.85), ("2", 0.18), ("3", -0.75), ("4", -0.12), ("5", 0.15)]
    bw = 56
    for i, (lab, val) in enumerate(bars):
        cx = ox + 55 + i * (bw + 30)
        top = oy - val * yl
        col = RED if val >= 0 else BLUE
        d.rectangle((cx - bw / 2, min(oy, top), cx + bw / 2, max(oy, top)),
                    outline=BLACK, width=2, fill=(250, 232, 232) if val >= 0 else (232, 238, 250))
        ctext(d, cx, oy + yl + 16, "反応" + lab, FT, BLACK)
    ctext(d, ox + xl + 40, oy - yl + 10, "正=速める", FT, RED, "rm")
    ctext(d, ox + xl + 40, oy + yl - 10, "負=遅くする", FT, BLUE, "rm")
    note(d, "棒の向き=影響の向き, 高さ=影響の強さ(反応速度の絶対量とは別物)")
    save(im, "t1e19SensitivityBars")


# ============================================================
# 19-10 t1e19NOxPathways : NOx3経路(helpful)
# ============================================================
def nox_pathways():
    im, d = new(); title(d, "NOxの3つの生成経路(火炎帯 と 火炎背後)")
    # 火炎帯(左)と火炎背後(右)の帯
    box(d, 60, 100, 300, 360, (255, 244, 232))
    ctext(d, 180, 122, "火炎帯(反応帯)", FS, ORANGE)
    box(d, 360, 100, 600, 360, (250, 240, 240))
    ctext(d, 480, 122, "火炎背後(既燃・高温)", FS, RED)
    # 火炎面(境界)
    for yy in range(140, 350, 16):
        d.line((330, yy, 330, yy + 9), fill=ORANGE, width=4)
    # サーマルNO: 空気中N2 -> 火炎背後
    pcircle(d, 480, 180, 22, (235, 242, 250), BLUE, 2); ctext(d, 480, 180, "N2", FT, BLUE)
    ctext(d, 480, 152, "空気中の窒素", FT, GRAY)
    arrow(d, 480, 204, 480, 245, RED, 3, 12)
    ctext(d, 480, 262, "サーマルNO", FT, RED)
    ctext(d, 480, 285, "(ゼルドビッチ機構・高温)", FT, GRAY)
    # プロンプトNO: 火炎帯
    pcircle(d, 180, 185, 22, FILL1, ORANGE, 2); ctext(d, 180, 185, "CH", FT, ORANGE)
    arrow(d, 180, 209, 180, 250, ORANGE, 3, 12)
    ctext(d, 180, 267, "プロンプトNO", FT, ORANGE)
    ctext(d, 180, 290, "(火炎帯で速い)", FT, GRAY)
    # フューエルNO: 燃料中N分
    box(d, 60, 380, 340, 410, (250, 250, 250))
    ctext(d, 200, 395, "フューエルNO: 燃料中の窒素分が起源", FT, GREEN)
    note(d, "空欄a-dの答えは各自(経路の場所だけを示す)")
    save(im, "t1e19NOxPathways")


# ============================================================
# 19-11 t1e19NOxReduction : 当量比と火炎温度/NOx(helpful)
# ============================================================
def nox_reduction():
    im, d = new(); title(d, "当量比に対する最高火炎温度とNOx(山型)と低減方向")
    ox, oy, xl, yl = 100, 330, 470, 230
    # 軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "当量比 phi", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "火炎温度/NOx", FT, BLACK, "rm")
    # phi=1 の目盛
    xm = ox + xl * 0.5
    dashed(d, xm, oy, xm, oy - yl, GRAY, 1, 6, 5)
    ctext(d, xm, oy + 18, "phi=1", FT, GRAY)
    ctext(d, ox + xl * 0.2, oy + 18, "希薄(低)", FT, BLUE)
    ctext(d, ox + xl * 0.82, oy + 18, "過濃(高)", FT, RED)
    # 山型曲線(ピークは phi=1 よりわずかに過濃側)
    pts = []
    for i in range(0, 471):
        t = i / 470
        v = 0.9 * math.exp(-((t - 0.55) ** 2) / (2 * 0.16 ** 2))
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    ctext(d, xm + 70, oy - 0.85 * yl, "山の頂 = 高NOx", FT, RED, "lm")
    # 低減方向の矢印(希薄側/過濃側の両方向)
    arrow(d, xm - 30, oy - 0.55 * yl, ox + 60, oy - 0.18 * yl, BLUE, 3, 12)
    ctext(d, ox + 55, oy - 0.10 * yl, "希薄化で低減", FT, BLUE, "lm")
    arrow(d, xm + 40, oy - 0.5 * yl, ox + xl - 30, oy - 0.15 * yl, GRAY, 3, 12)
    ctext(d, ox + xl - 90, oy - 0.08 * yl, "過濃化で低減", FT, GRAY, "lm")
    note(d, "低減の要=最高火炎温度を下げる. どれが誤りかは各自")
    save(im, "t1e19NOxReduction")


# ============================================================
# 19-12 t1e19AdiabaticFlameTemp : 断熱火炎温度の相対比較(helpful)
# ============================================================
def adiabatic_flame_temp():
    im, d = new(); title(d, "4種の燃料の断熱火炎温度の相対比較(当量比1・空気)")
    ox, oy, yl = 90, 340, 230
    # 軸
    arrow(d, ox, oy, ox + 500, oy, BLACK, 2, 11)
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "断熱火炎温度(相対)", FT, BLACK, "rm")
    # 棒(相対高さのみ・数値なし). 飽和が低い/不飽和が高い
    bars = [("メタン", "CH4", 0.55, BLUE),
            ("オクタン", "C8H18", 0.62, BLUE),
            ("エチレン", "C2H4", 0.80, ORANGE),
            ("アセチレン", "C2H2", 0.95, RED)]
    bw = 70
    for i, (name, form, val, col) in enumerate(bars):
        cx = ox + 80 + i * 110
        top = oy - val * yl
        d.rectangle((cx - bw / 2, top, cx + bw / 2, oy), outline=BLACK, width=2, fill=(250, 245, 240))
        ctext(d, cx, top - 14, form, FT, col)
        ctext(d, cx, oy + 18, name, FT, BLACK)
    # 傾向の注記
    dashed(d, ox + 80, oy - 0.55 * yl, ox + 80 + 3 * 110, oy - 0.95 * yl, GRAY, 2, 8, 5)
    ctext(d, ox + 300, oy - 0.90 * yl, "不飽和度が高いほど高温の傾向", FT, GRAY)
    note(d, "棒は相対的な高低のみ. 実際の温度値・順位の数値は各自")
    save(im, "t1e19AdiabaticFlameTemp")


# ============================================================
# 19-13 t1e19SootFormation : すす生成過程(helpful)
# ============================================================
def soot_formation():
    im, d = new(); title(d, "すす生成の過程: 前駆体 -> 核生成 -> 凝集 -> 表面成長 -> 酸化")
    steps = [
        (95, "前駆体", "C2H2 / PAH", BLUE),
        (230, "核生成", "微小核が発生", BLACK),
        (365, "凝集", "粒子が集まる", ORANGE),
        (500, "表面成長", "粒子が大きく", RED),
        (605, "酸化", "O2/OHで消費", GREEN),
    ]
    for (cx, head, sub, col) in steps:
        d.rectangle((cx - 52, 130, cx + 52, 235), outline=col, width=2, fill=(250, 250, 250))
        ctext(d, cx, 155, head, FT, col)
        ctext(d, cx, 200, sub, FT, GRAY)
        # 粒子の大きさが成長を表す
    # 段間の矢印
    for x in [147, 282, 417, 552]:
        arrow(d, x, 182, x + 30, 182, BLACK, 3, 12)
    # 粒子サイズの成長イメージ(下段)
    sizes = [(95, 5), (230, 8), (365, 13), (500, 19), (605, 10)]
    for (cx, r) in sizes:
        pcircle(d, cx, 275, r, FILL2, BLACK, 2)
    ctext(d, 350, 305, "核生成から表面成長で粒径が増え、酸化で消費される", FT, GRAY)
    # 生成領域(拡散燃焼・燃料過濃側)
    box(d, 120, 335, 560, 385, (250, 245, 240))
    ctext(d, 340, 360, "主に拡散燃焼(燃料過濃・酸素不足)領域で生成", FT, RED)
    note(d, "空欄a-dの答えは各自(過程の並びと生成場を示す)")
    save(im, "t1e19SootFormation")


# ============================================================
# 19-14 t1e19ExplosionLimits : 水素-酸素系の爆発限界(required)
# ============================================================
def explosion_limits():
    im, d = new(); title(d, "水素-酸素系の爆発限界(温度-圧力平面)")
    ox, oy, xl, yl = 110, 345, 470, 270
    # 軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "温度", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "圧力", FT, BLACK, "rm")
    # Z字状の爆発限界曲線(低温側からA->B->C->D)
    # A:低圧(下), B:中圧右寄り, C:中圧左寄り(突起), D:高圧(上)
    A = (ox + 0.30 * xl, oy - 0.15 * yl)
    B = (ox + 0.62 * xl, oy - 0.42 * yl)
    C = (ox + 0.34 * xl, oy - 0.62 * yl)
    D = (ox + 0.72 * xl, oy - 0.92 * yl)
    # AB(第1限界): 右上がり
    d.line((A[0], A[1], B[0], B[1]), fill=BLACK, width=3, joint="curve")
    # BC(第2限界): 左上がり(圧力上げると爆発しなくなる逆傾向)
    d.line((B[0], B[1], C[0], C[1]), fill=BLACK, width=3, joint="curve")
    # CD(第3限界): 右上がり
    d.line((C[0], C[1], D[0], D[1]), fill=BLACK, width=3, joint="curve")
    # 点とラベル(A,B,C,D)
    for (p, lab) in [(A, "A"), (B, "B"), (C, "C"), (D, "D")]:
        node(d, p[0], p[1], 6)
        ctext(d, p[0] + 14, p[1] - 12, lab, FS, RED, "lm")
    # 曲線名(AB/BC/CD)は中点にだけ
    ctext(d, (A[0] + B[0]) / 2 + 16, (A[1] + B[1]) / 2 + 14, "AB", FT, GRAY)
    ctext(d, (B[0] + C[0]) / 2 - 20, (B[1] + C[1]) / 2, "BC", FT, GRAY)
    ctext(d, (C[0] + D[0]) / 2 - 18, (C[1] + D[1]) / 2, "CD", FT, GRAY)
    # 突起(半島)を破線の楕円で囲うのみ(名称は書かない)
    dashed(d, C[0] - 20, C[1] - 10, B[0] + 15, B[1] - 30, GRAY, 1, 6, 4)
    ctext(d, ox + 0.20 * xl, oy - 0.75 * yl, "爆発(内側)", FT, BLUE)
    ctext(d, ox + 0.80 * xl, oy - 0.25 * yl, "非爆発(外側)", FT, GRAY)
    note(d, "曲線をAB/BC/CDと点で示すのみ. 第1/2/3・半島名の答えは各自")
    save(im, "t1e19ExplosionLimits")


# ============================================================
if __name__ == "__main__":
    mech_scale()                # 19-1
    h2_chain_flow()             # 19-2
    global_rate_order()         # 19-3
    potential_energy_curves()   # 19-4
    enthalpy_cycle()            # 19-5
    fall_off_curve()            # 19-6
    third_body()                # 19-7
    arrhenius_units()           # 19-8
    sensitivity_bars()          # 19-9
    nox_pathways()              # 19-10
    nox_reduction()             # 19-11
    adiabatic_flame_temp()      # 19-12
    soot_formation()            # 19-13
    explosion_limits()          # 19-14
    print("done ch19")
