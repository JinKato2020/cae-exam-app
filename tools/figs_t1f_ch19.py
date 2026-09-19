# -*- coding: utf-8 -*-
"""熱流体力学1級 第19章「燃焼反応」の公式・用語図(t1f19*・20枚)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。問題図(t1e19*)とは別ファイル。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(omega, alpha, beta, phi, k, [M], R0, T^n, ->, <=>, exp 等)。
公式図なので定義式・関係式を明示してよい。"""
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


def eqbox(d, cx, cy, s, w=520, h=52, col=BLACK, fill=FILL2, fnt=F):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ctext(d, cx, cy, s, fnt, col)


# ============================================================
# 19-1 t1f19DetailedMechanism : 詳細化学反応機構(素反応の集合体)
# ============================================================
def detailed_mechanism():
    im, d = new(); title(d, "詳細化学反応機構: 多数の素反応の集合(数百に及ぶ)")
    box(d, 45, 80, 615, 300, (248, 248, 248))
    ctext(d, 330, 102, "1つの燃焼 = 多数の素反応", FS, BLACK)
    reacs = ["H2+O2<=>HO2+H", "H+O2<=>OH+O", "OH+H2<=>H2O+H",
             "H+O2+M<=>HO2+M", "CH4+OH<=>CH3+H2O", "CO+OH<=>CO2+H",
             "H+OH+M<=>H2O+M", "CH3+O<=>CH2O+H"]
    for i, r in enumerate(reacs):
        cx = 55 + (i % 2) * 300
        cy = 135 + (i // 2) * 38
        box(d, cx, cy, cx + 285, cy + 30, (245, 245, 245), 2)
        ctext(d, cx + 142, cy + 15, r, FT, BLACK)
    ctext(d, 330, 288, "... メタン燃焼で数百(GRI-Mech3.0=325)", FT, GRAY)
    eqbox(d, 330, 350, "素反応数: 水素で数十, メタンで数百 -> 計算負荷が飛躍的に大", 620, 46, BLACK, FILL2, FS)
    note(d, "『メタン燃焼で最大10程度』は誤り. 簡略機構より負荷が飛躍的に高い")
    save(im, "t1f19DetailedMechanism")


# ============================================================
# 19-2 t1f19ElementaryReaction : 素反応と反応特性時間
# ============================================================
def elementary_reaction():
    im, d = new(); title(d, "素反応: 分子1段階の反応. 特性時間が刻み幅を決める")
    # 素反応の1段: A + B -> C + D
    box(d, 60, 100, 600, 190, (245, 245, 245))
    ctext(d, 130, 145, "反応物", FT, GRAY)
    pcircle(d, 200, 145, 20, FILL1, BLUE, 2); ctext(d, 200, 145, "H", FS, BLUE)
    ctext(d, 240, 145, "+", FS, BLACK)
    pcircle(d, 285, 145, 22, FILL1, RED, 2); ctext(d, 285, 145, "O2", FT, RED)
    arrow(d, 320, 145, 400, 145, BLACK, 3, 12)
    pcircle(d, 445, 145, 22, FILL1, GREEN, 2); ctext(d, 445, 145, "OH", FT, GREEN)
    ctext(d, 485, 145, "+", FS, BLACK)
    pcircle(d, 530, 145, 20, FILL1, ORANGE, 2); ctext(d, 530, 145, "O", FS, ORANGE)
    ctext(d, 330, 172, "分子レベルで実際に一段階で起きる反応", FT, GRAY)
    # 特性時間の帯(速い素反応が刻み幅を支配)
    ox, oy, xl = 90, 285, 470
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "特性時間", FT, BLACK, "lm")
    for (fx, lab, col) in [(0.10, "速い素反応", RED), (0.55, "中", GRAY), (0.88, "遅い", BLUE)]:
        px = ox + xl * fx
        d.line((px, oy - 10, px, oy + 10), fill=col, width=3)
        ctext(d, px, oy - 24, lab, FT, col)
    dashed(d, ox + xl * 0.10, oy + 16, ox + xl * 0.10, oy + 48, RED, 2, 6, 4)
    ctext(d, ox + xl * 0.10, oy + 62, "時間刻み幅を決める", FT, RED)
    note(d, "最も速い素反応に合わせ dt を細かく取る -> 非定常解析の負荷要因")
    save(im, "t1f19ElementaryReaction")


# ============================================================
# 19-3 t1f19GlobalReactionRate : 総括反応モデルの反応速度
# ============================================================
def global_reaction_rate():
    im, d = new(); title(d, "総括反応モデル: 反応物と生成物を1本にまとめた速度式")
    ctext(d, 330, 82, "CH4 + 2 O2  ->  CO2 + 2 H2O", FS, BLACK)
    box(d, 60, 105, 600, 175, (245, 245, 245))
    ctext(d, 330, 125, "多数の素反応を『見かけの1反応』に集約", FT, GRAY)
    ctext(d, 330, 155, "分子レベルの実際の反応ではない", FT, RED)
    eqbox(d, 330, 220, "omega = k [CH4]^alpha [O2]^beta", 560, 50, BLACK, FILL2, F)
    # 反応次数の注意
    box(d, 60, 265, 600, 350, (250, 250, 250))
    ctext(d, 330, 288, "反応次数 alpha, beta の性質", FS, BLACK)
    ctext(d, 330, 315, "温度・濃度域で変化 / 整数とは限らない / 負もありうる", FT, GRAY)
    ctext(d, 330, 338, "『常に正』は誤り", FT, RED)
    note(d, "k=反応速度定数, [ ]=モル濃度. 総括モデルは実反応を示すわけではない")
    save(im, "t1f19GlobalReactionRate")


# ============================================================
# 19-4 t1f19ChainReaction : 連鎖反応(起鎖->分枝->再結合)
# ============================================================
def chain_reaction():
    im, d = new(); title(d, "連鎖反応: 起鎖 -> 連鎖分枝 -> 再結合(発熱)")
    steps = [("起鎖反応", "H2+O2 <=> HO2+H", "活性基が生成", BLUE),
             ("連鎖分枝反応", "H+O2 <=> OH+O", "活性基が急増(支配的)", RED),
             ("競合(三体再結合)", "H+O2+M <=> HO2+M", "分枝と競合", ORANGE),
             ("再結合反応", "H+OH+M <=> H2O+M", "失活+反応熱を放出", GREEN)]
    x0, w = 45, 570
    y0, hh = 78, 62
    for i, (name, expr, role, col) in enumerate(steps):
        cy = y0 + i * (hh + 8)
        box(d, x0, cy, x0 + w, cy + hh, (245, 245, 245))
        ctext(d, x0 + 14, cy + 22, name, FT, col, "lm")
        ctext(d, x0 + 14, cy + 44, role, FT, GRAY, "lm")
        ctext(d, x0 + 320, cy + hh / 2, expr, FS, BLACK, "lm")
        if i < 3:
            arrow(d, x0 + w / 2, cy + hh, x0 + w / 2, cy + hh + 8, BLACK, 2, 8)
    note(d, "活性基(ラジカル)の数が分枝で急増し, 再結合で失活して熱が出る")
    save(im, "t1f19ChainReaction")


# ============================================================
# 19-5 t1f19Radical : 活性基(ラジカル)
# ============================================================
def radical():
    im, d = new(); title(d, "活性基(ラジカル): 反応性の高い化学種 H, OH, O, HO2")
    box(d, 45, 85, 615, 200, (248, 248, 248))
    ctext(d, 330, 108, "対をなさない電子を持ち, すぐ反応する", FT, GRAY)
    for (px, lab, col) in [(150, "H", BLUE), (290, "OH", GREEN), (420, "O", ORANGE), (540, "HO2", RED)]:
        pcircle(d, px, 165, 26, FILL1, col, 3); ctext(d, px, 165, lab, FS, col)
    # 分枝で急増 -> 再結合で失活
    ox, oy, xl, yl = 100, 340, 460, 130
    axes(d, ox, oy, xl + 20, yl + 20, "時間", "活性基の数")
    pts = []
    for i in range(0, xl + 1):
        t = i / xl
        v = 0.08 + 0.85 / (1 + math.exp(-(t - 0.45) * 16)) - 0.35 * max(0, t - 0.7)
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    ctext(d, ox + xl * 0.55, oy - 0.95 * yl, "分枝で急増", FT, RED)
    ctext(d, ox + xl * 0.9, oy - 0.30 * yl, "再結合で失活", FT, GREEN)
    note(d, "分枝反応で急増し, 三体再結合(例 H+OH+M->H2O+M)で失活する")
    save(im, "t1f19Radical")


# ============================================================
# 19-6 t1f19ExoEndothermic : 発熱反応と吸熱反応(ポテンシャル曲線)
# ============================================================
def exo_endothermic():
    im, d = new(); title(d, "発熱反応と吸熱反応: 反応過程 vs ポテンシャルエネルギー")
    ox, oy, xl, yl = 90, 350, 470, 250
    axes(d, ox, oy, xl + 20, yl + 20, "反応過程", "ポテンシャルE")
    y0 = oy - 0.42 * yl   # 始状態レベル
    peak = oy - 0.92 * yl
    # 共通の始状態〜山
    def curve(end_y, col, lab, laby):
        pts = []
        for i in range(0, xl + 1):
            t = i / xl
            if t < 0.5:
                v = y0 + (peak - y0) * (0.5 * (1 - math.cos(math.pi * t / 0.5)))
            else:
                s = (t - 0.5) / 0.5
                v = peak + (end_y - peak) * (0.5 * (1 - math.cos(math.pi * s)))
            pts.append((ox + t * xl, v))
        d.line(pts, fill=col, width=3, joint="curve")
        ctext(d, ox + xl + 8, end_y, lab, FT, col, "lm")
    curve(oy - 0.55 * yl, ORANGE, "A", 0)          # 解離的(始より高い付近)
    curve(oy - 0.33 * yl, BLUE, "B(吸熱)", 0)       # 始より少し高い=吸熱
    curve(oy - 0.10 * yl, RED, "C(発熱)", 0)        # 始より大きく低い=発熱
    dashed(d, ox, y0, ox + xl, y0, GRAY, 1, 6, 5)
    ctext(d, ox + 60, y0 - 12, "始状態", FT, GRAY)
    note(d, "山越え後が始状態より大きく低い=発熱(C). 高くなる=吸熱(B)")
    save(im, "t1f19ExoEndothermic")


# ============================================================
# 19-7 t1f19ActivationEnergy : 活性化エネルギー(障壁)
# ============================================================
def activation_energy():
    im, d = new(); title(d, "活性化エネルギー E: 反応が越える山の高さ(障壁)")
    ox, oy, xl, yl = 90, 350, 470, 250
    axes(d, ox, oy, xl + 20, yl + 20, "反応過程", "ポテンシャルE")
    y0 = oy - 0.30 * yl
    peak = oy - 0.85 * yl
    yf = oy - 0.12 * yl
    pts = []
    for i in range(0, xl + 1):
        t = i / xl
        if t < 0.5:
            v = y0 + (peak - y0) * (0.5 * (1 - math.cos(math.pi * t / 0.5)))
        else:
            s = (t - 0.5) / 0.5
            v = peak + (yf - peak) * (0.5 * (1 - math.cos(math.pi * s)))
        pts.append((ox + t * xl, v))
    d.line(pts, fill=RED, width=3, joint="curve")
    xpk = ox + xl * 0.5
    dashed(d, ox, y0, xpk, y0, GRAY, 1, 6, 5)
    dashed(d, xpk, peak, xpk + 60, peak, GRAY, 1, 6, 5)
    # 障壁の高さ E
    d.line((ox + 60, y0, ox + 60, peak), fill=BLACK, width=2)
    arrow(d, ox + 60, y0, ox + 60, peak, BLACK, 2, 10)
    ctext(d, ox + 78, (y0 + peak) / 2, "E(活性化エネルギー)", FT, BLACK, "lm")
    ctext(d, ox + xl * 0.15, y0 - 14, "始状態", FT, GRAY)
    eqbox(d, 400, 388, "速度は exp(-E/R0 T) に比例 : 高温ほど障壁を越える", 560, 40, BLACK, FILL2, FS)
    note(d, "E が高いほど反応しにくい. 温度上昇で反応速度が急増する")
    save(im, "t1f19ActivationEnergy")


# ============================================================
# 19-8 t1f19HeatOfReaction : 反応熱(標準生成エンタルピーの差)
# ============================================================
def heat_of_reaction():
    im, d = new(); title(d, "反応熱 = 生成物 - 反応物 の標準生成エンタルピー差")
    ctext(d, 330, 78, "例) C3H8 + 5 O2 = 3 CO2 + 4 H2O", FS, BLACK)
    # レベル図
    ox = 120; yreact = 150; yprod = 300
    box(d, ox, yreact - 18, ox + 150, yreact + 18, (250, 230, 230))
    ctext(d, ox + 75, yreact, "反応物 -104", FT, RED)
    box(d, ox + 340, yprod - 18, ox + 490, yprod + 18, (230, 240, 250))
    ctext(d, ox + 415, yprod, "生成物 -2150", FT, BLUE)
    arrow(d, ox + 150, yreact, ox + 340, yprod, BLACK, 3, 13)
    d.line((ox, yreact - 18, ox + 490, yreact - 18), fill=LGRAY, width=1)
    dashed(d, ox + 415, yreact, ox + 415, yprod, GRAY, 1, 6, 5)
    arrow(d, ox + 415, yreact, ox + 415, yprod, GREEN, 2, 11)
    ctext(d, ox + 430, (yreact + yprod) / 2, "放出熱 2046", FT, GREEN, "lm")
    eqbox(d, 330, 355, "dH = sum(生成物 dHf) - sum(反応物 dHf) = -2046 kJ/mol", 620, 44, BLACK, FILL2, FS)
    note(d, "水を気相-242で低位, 液相-286で高位. 負なら発熱でその絶対値が発熱量")
    save(im, "t1f19HeatOfReaction")


# ============================================================
# 19-9 t1f19ModifiedArrhenius : 修正アレニウス式
# ============================================================
def modified_arrhenius():
    im, d = new(); title(d, "修正アレニウス式: 反応速度定数 k の温度依存")
    eqbox(d, 330, 105, "k = A * T^n * exp( -E / (R0 T) )", 560, 56, BLACK, FILL2, F)
    # 3パラメータの説明
    params = [("A", "頻度係数", "衝突の起こりやすさ", BLUE),
              ("T^n", "温度指数 n", "衝突頻度の温度依存", GREEN),
              ("exp(-E/R0 T)", "活性化エネルギー E", "高温で急増", RED)]
    x0, w = 40, 193
    y0, hh = 160, 120
    for i, (sym, name, role, col) in enumerate(params):
        cx = x0 + i * (w + 4)
        box(d, cx, y0, cx + w, y0 + hh, (248, 248, 248))
        ctext(d, cx + w / 2, y0 + 28, sym, FS, col)
        d.line((cx + 12, y0 + 50, cx + w - 12, y0 + 50), fill=LGRAY, width=1)
        ctext(d, cx + w / 2, y0 + 72, name, FT, BLACK)
        ctext(d, cx + w / 2, y0 + 98, role, FT, GRAY)
    ctext(d, 330, 305, "反応速度: 二体 omega=[S1][S2] k , 三体 omega=[S1][S2][M] k", FT, GRAY)
    note(d, "R0=一般気体定数. n=0 で通常のアレニウス式. 素反応ごとに与える")
    save(im, "t1f19ModifiedArrhenius")


# ============================================================
# 19-10 t1f19RateUnitConversion : 頻度係数の単位換算(二体/三体)
# ============================================================
def rate_unit_conversion():
    im, d = new(); title(d, "頻度係数 A の単位換算: 二体と三体で次数が違う")
    # 二体
    box(d, 40, 85, 620, 190, (235, 245, 235))
    ctext(d, 120, 108, "二体反応", FS, GREEN)
    ctext(d, 330, 108, "[cm^3/mol s]", FT, GRAY)
    ctext(d, 330, 145, "AI = 5.0e19  --( x10^-6 )-->  5.0e13 [m^3/mol s]", FT, BLACK)
    ctext(d, 330, 172, "1 cm^3 = 10^-6 m^3", FT, GRAY)
    # 三体
    box(d, 40, 205, 620, 310, (235, 242, 250))
    ctext(d, 120, 228, "三体反応", FS, BLUE)
    ctext(d, 330, 228, "[cm^6/mol^2 K s]", FT, GRAY)
    ctext(d, 330, 265, "AII = 7.0e16 --( x10^-12 )--> 7.0e4 [m^6/mol^2 K s]", FT, BLACK)
    ctext(d, 330, 292, "1 cm^6 = 10^-12 m^6 (第三体[M]で濃度が1つ多い)", FT, GRAY)
    eqbox(d, 330, 355, "活性化E: 1 cal = 4.2 J  ->  EI=500x4.2=2100 J/mol", 600, 44, BLACK, FILL2, FS)
    note(d, "第三体[M]の分だけ三体は濃度の次数が1多く, A の桁換算が異なる")
    save(im, "t1f19RateUnitConversion")


# ============================================================
# 19-11 t1f19ThirdBody : 第三体 M
# ============================================================
def third_body():
    im, d = new(); title(d, "第三体 M: 生成種とエネルギー授受し安定化させる")
    ctext(d, 330, 78, "H + O2 + M  <=>  HO2 + M", FS, BLACK)
    # 反応: H, O2 が結合 -> 高エネルギーHO2 -> M が余分なEを奪う
    pcircle(d, 120, 170, 20, FILL1, BLUE, 2); ctext(d, 120, 170, "H", FS, BLUE)
    ctext(d, 160, 170, "+", FS, BLACK)
    pcircle(d, 205, 170, 22, FILL1, RED, 2); ctext(d, 205, 170, "O2", FT, RED)
    arrow(d, 240, 170, 315, 170, BLACK, 3, 12)
    pcircle(d, 365, 170, 26, (255, 235, 235), RED, 3); ctext(d, 365, 170, "HO2*", FT, RED)
    ctext(d, 365, 210, "高エネルギー", FT, GRAY)
    # M が衝突しエネルギーを奪う
    pcircle(d, 470, 110, 22, FILL1, GRAY, 2); ctext(d, 470, 110, "M", FS, GRAY)
    arrow(d, 455, 128, 388, 158, GRAY, 2, 11)
    arrow(d, 392, 175, 470, 220, ORANGE, 2, 11)
    ctext(d, 500, 220, "余分なEを奪う", FT, ORANGE, "lm")
    arrow(d, 400, 170, 470, 170, BLACK, 3, 12)
    pcircle(d, 530, 170, 26, FILL1, GREEN, 3); ctext(d, 530, 170, "HO2", FT, GREEN)
    ctext(d, 530, 210, "安定化", FT, GREEN)
    box(d, 60, 250, 600, 340, (250, 250, 250))
    ctext(d, 330, 275, "M の候補: Ar, He, N2, CO, CO2, H2O(条件で H2,O2,OH も)", FT, GRAY)
    ctext(d, 330, 312, "全ての化学種が第三体になるわけではない(誤りに注意)", FT, RED)
    note(d, "M は反応に直接関与せず, エネルギーの授受だけを担う")
    save(im, "t1f19ThirdBody")


# ============================================================
# 19-12 t1f19FallOff : fall-off反応(Lindemann近似)
# ============================================================
def fall_off():
    im, d = new(); title(d, "fall-off反応: 低圧 k=k0[M] -> 高圧 k=k_inf の遷移")
    ox, oy, xl, yl = 100, 320, 450, 210
    axes(d, ox, oy, xl + 20, yl + 20, "log P", "log k")
    # S字 fall-off 曲線
    pts = []
    for i in range(0, xl + 1):
        t = i / xl
        v = 0.10 + 0.80 / (1 + math.exp(-(t - 0.5) * 9))
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    # 低圧漸近(傾き1)
    dashed(d, ox + 20, oy - 0.05 * yl, ox + xl * 0.55, oy - 0.62 * yl, BLUE, 2, 8, 5)
    ctext(d, ox + 95, oy - 0.30 * yl, "低圧: 傾き1", FT, BLUE, "lm")
    ctext(d, ox + 60, oy - 0.02 * yl, "k -> k0[M]", FT, BLUE)
    # 高圧漸近(一定)
    dashed(d, ox + xl * 0.5, oy - 0.90 * yl, ox + xl, oy - 0.90 * yl, GREEN, 2, 8, 5)
    ctext(d, ox + xl * 0.78, oy - 0.97 * yl, "高圧: k -> k_inf(一定)", FT, GREEN)
    eqbox(d, 330, 375, "k = k_inf * Pr/(1+Pr) , Pr = k0[M]/k_inf", 600, 44, BLACK, FILL2, FS)
    note(d, "中間圧をLindemann近似で表す. 第三体濃度[M]が圧力に強く依存")
    save(im, "t1f19FallOff")


# ============================================================
# 19-13 t1f19SensitivityCoefficient : 感度解析・感度係数
# ============================================================
def sensitivity_coefficient():
    im, d = new(); title(d, "感度解析: 各素反応が燃焼速度へ与える寄与度合い")
    ox, oy, xl, yl = 110, 240, 430, 120
    d.line((ox, oy, ox + xl + 20, oy), fill=BLACK, width=2)
    arrow(d, ox, oy + yl, ox, oy - yl, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl, "感度", FT, BLACK, "rm")
    ctext(d, ox + xl + 26, oy, "反応", FT, BLACK, "lm")
    vals = [0.95, 0.18, -0.72, 0.12, -0.20]
    bw = 55
    for i, v in enumerate(vals):
        cx = ox + 40 + i * (bw + 20)
        col = RED if v >= 0 else BLUE
        top = oy - v * yl
        d.rectangle((cx, min(oy, top), cx + bw, max(oy, top)), outline=BLACK, width=2, fill=(250, 230, 230) if v >= 0 else (225, 235, 250))
        ctext(d, cx + bw / 2, oy + 18, "反応%d" % (i + 1), FT, GRAY)
    ctext(d, ox + 40 + bw / 2, oy - 0.95 * yl - 14, "正=速度を上げる", FT, RED)
    ctext(d, ox + 40 + 2 * (bw + 20) + bw / 2, oy + 0.72 * yl + 20, "負=下げる", FT, BLUE)
    eqbox(d, 330, 355, "S = (kj/phi_i) * (d phi_i / d kj)  (寄与度. 速度の大小ではない)", 620, 44, BLACK, FILL2, FS)
    note(d, "感度が小さくても反応が不要とは限らない. 大=反応速度が大 も誤り")
    save(im, "t1f19SensitivityCoefficient")


# ============================================================
# 19-14 t1f19AdiabaticFlameTemp : 断熱火炎温度
# ============================================================
def adiabatic_flame_temp():
    im, d = new(); title(d, "断熱火炎温度 Tf = Tini + q/Cm(近似推定)")
    ox, oy, xl, yl = 110, 320, 430, 210
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "反応進行", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T", FS, BLACK, "rm")
    yini = oy - 0.15 * yl
    yf = oy - 0.85 * yl
    dashed(d, ox, yini, ox + xl, yini, GRAY, 1, 6, 5)
    dashed(d, ox, yf, ox + xl, yf, GRAY, 1, 6, 5)
    ctext(d, ox - 8, yini, "Tini", FT, BLUE, "rm")
    ctext(d, ox - 8, yf, "Tf", FT, RED, "rm")
    pts = []
    for i in range(0, xl + 1):
        t = i / xl
        v = 0.15 + 0.70 * (0.5 * (1 + math.tanh((t - 0.5) * 7)))
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    # 温度上昇分 q/Cm
    d.line((ox + xl - 30, yini, ox + xl - 30, yf), fill=BLACK, width=2)
    arrow(d, ox + xl - 30, yini, ox + xl - 30, yf, BLACK, 2, 10)
    ctext(d, ox + xl - 22, (yini + yf) / 2, "q/Cm", FT, BLACK, "lm")
    eqbox(d, 330, 375, "Tf = Tini + q/Cm  (q=発熱量, Cm=平均比熱)", 580, 44, BLACK, FILL2, FS)
    note(d, "熱解離を無視するため実際よりかなり高い温度を算出する")
    save(im, "t1f19AdiabaticFlameTemp")


# ============================================================
# 19-15 t1f19FlameTempOrder : 燃料別の断熱火炎温度の序列
# ============================================================
def flame_temp_order():
    im, d = new(); title(d, "断熱火炎温度の序列(空気, 当量比1): 燃料で変わる")
    fuels = [("アセチレン", 0.95, RED), ("エチレン", 0.78, ORANGE),
             ("ベンゼン", 0.66, GREEN), ("オクタン", 0.55, BLUE), ("メタン", 0.45, GRAY)]
    ox, oy, yl = 90, 340, 230
    bw, gap = 78, 22
    d.line((ox - 10, oy, ox + 5 * (bw + gap), oy), fill=BLACK, width=2)
    arrow(d, ox - 10, oy, ox - 10, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 22, oy - yl - 8, "Tf", FT, BLACK, "rm")
    for i, (name, h, col) in enumerate(fuels):
        cx = ox + i * (bw + gap)
        top = oy - h * yl
        d.rectangle((cx, top, cx + bw, oy), outline=BLACK, width=2, fill=(245, 245, 245))
        d.rectangle((cx, top, cx + bw, top + 12), outline=BLACK, width=1, fill=col)
        ctext(d, cx + bw / 2, oy + 16, name, FT, col)
    arrow(d, ox + 30, 90, ox + 4 * (bw + gap), 90, BLACK, 2, 11)
    ctext(d, ox + 2 * (bw + gap), 76, "高い <---------------------> 低い", FT, GRAY)
    note(d, "アセチレン>エチレン>ベンゼン>オクタン>メタン. 火炎温度はNOxに直結")
    save(im, "t1f19FlameTempOrder")


# ============================================================
# 19-16 t1f19NOxFormation : NOxの生成機構(3種)
# ============================================================
def nox_formation():
    im, d = new(); title(d, "NOxの3つの生成経路: サーマル/プロンプト/フューエル")
    # 火炎帯と火炎背後の帯
    box(d, 40, 90, 620, 200, (250, 250, 250))
    d.rectangle((150, 110, 210, 180), outline=ORANGE, width=3, fill=(255, 240, 220))
    ctext(d, 180, 145, "火炎帯", FT, ORANGE)
    d.rectangle((210, 110, 560, 180), outline=RED, width=2, fill=(255, 235, 235))
    ctext(d, 385, 145, "火炎背後(高温)", FT, RED)
    arrow(d, 60, 145, 148, 145, BLUE, 3, 12)
    ctext(d, 90, 125, "未燃", FT, GRAY)
    rows = [("サーマルNO", "空気中の窒素", "火炎背後(ゼルドビッチ機構)", RED),
            ("プロンプトNO", "空気中の窒素", "火炎帯で高速に生成", ORANGE),
            ("フューエルNO", "燃料中の窒素分", "燃料由来の窒素から", GREEN)]
    x0, w = 45, 570
    y0, hh = 215, 55
    for i, (name, src, place, col) in enumerate(rows):
        cy = y0 + i * (hh + 6)
        box(d, x0, cy, x0 + w, cy + hh, (245, 245, 245))
        ctext(d, x0 + 14, cy + hh / 2, name, FS, col, "lm")
        ctext(d, x0 + 175, cy + 18, "起源: " + src, FT, BLACK, "lm")
        ctext(d, x0 + 175, cy + 38, place, FT, GRAY, "lm")
    note(d, "サーマルNOは高温ほど増える. 経路で必要な反応機構が変わる")
    save(im, "t1f19NOxFormation")


# ============================================================
# 19-17 t1f19NOxReduction : NOx低減法
# ============================================================
def nox_reduction():
    im, d = new(); title(d, "NOx低減法: 最高温度を下げる/滞留短縮/酸素低下")
    methods = [("水・水蒸気噴射法", "燃焼ガスに水噴射し火炎温度を下げる", BLUE),
               ("希薄予混合燃焼法", "当量比を下げ希薄化し最高温度を下げる", GREEN),
               ("濃淡燃焼法", "希薄と過剰のバーナー交互で全体やや希薄", ORANGE),
               ("短炎燃焼法", "二次空気で高温域を希釈し火炎を短縮", RED)]
    x0, w = 45, 570
    y0, hh = 90, 58
    for i, (name, role, col) in enumerate(methods):
        cy = y0 + i * (hh + 8)
        box(d, x0, cy, x0 + w, cy + hh, (245, 245, 245))
        ctext(d, x0 + 14, cy + hh / 2, name, FS, col, "lm")
        ctext(d, x0 + 210, cy + hh / 2, role, FT, GRAY, "lm")
    box(d, x0, 340, x0 + w, 384, (255, 235, 235), 2)
    ctext(d, 330, 362, "誤: 当量比を『上げて過濃』では最高温度は下がらない", FT, RED)
    note(d, "希薄予混合は当量比を下げる(希薄化)のが正しい")
    save(im, "t1f19NOxReduction")


# ============================================================
# 19-18 t1f19SootFormation : すすの生成過程
# ============================================================
def soot_formation():
    im, d = new(); title(d, "すす生成: 前駆体 -> 核生成 -> 凝集 -> 表面成長 -> 酸化")
    stages = [("前駆体", "C2H2 / PAH", GRAY),
              ("核生成", "微小核", BLUE),
              ("凝集", "粒子が集合", GREEN),
              ("表面成長", "粒子が成長", ORANGE),
              ("酸化", "O2/OHで消費", RED)]
    x0 = 30; w = 112; y = 130
    for i, (name, sub, col) in enumerate(stages):
        cx = x0 + i * (w + 12)
        box(d, cx, y, cx + w, y + 90, (248, 248, 248))
        ctext(d, cx + w / 2, y + 30, name, FT, col)
        ctext(d, cx + w / 2, y + 62, sub, FT, GRAY)
        if i < 4:
            arrow(d, cx + w, y + 45, cx + w + 12, y + 45, BLACK, 2, 9)
    box(d, 60, 265, 600, 350, (250, 250, 250))
    ctext(d, 330, 288, "主に燃料過剰の『拡散燃焼領域』で生成", FS, RED)
    ctext(d, 330, 322, "噴霧火炎は予混合+拡散が混在(すすは拡散側)", FT, GRAY)
    note(d, "生成と酸化のせめぎ合いで最終すす量が決まる")
    save(im, "t1f19SootFormation")


# ============================================================
# 19-19 t1f19EquivalenceRatio : 当量比(燃焼反応での役割)
# ============================================================
def equivalence_ratio():
    im, d = new(); title(d, "当量比 phi: 火炎温度・NOx・すすを左右する主要指標")
    ox, oy, xl = 90, 180, 480
    arrow(d, ox - 10, oy, ox + xl + 20, oy, BLACK, 3, 12)
    ctext(d, ox + xl + 26, oy, "phi", FS, BLACK, "lm")
    xm = ox + xl * 0.5
    d.rectangle((ox, oy - 22, xm, oy - 6), outline=BLUE, width=2, fill=(225, 235, 250))
    d.rectangle((xm, oy - 22, ox + xl, oy - 6), outline=RED, width=2, fill=(250, 230, 230))
    d.line((xm, oy - 30, xm, oy + 12), fill=BLACK, width=3)
    ctext(d, xm, oy + 26, "phi=1", FT, BLACK)
    ctext(d, ox + xl * 0.25, oy - 46, "リーン(希薄)", FT, BLUE)
    ctext(d, ox + xl * 0.75, oy - 46, "リッチ(過濃)", FT, RED)
    box(d, 40, 230, 330, 355, (235, 242, 250))
    ctext(d, 185, 255, "phi < 1(希薄)", FS, BLUE)
    ctext(d, 185, 290, "最高温度が下がる", FT, GRAY)
    ctext(d, 185, 320, "サーマルNOを抑制", FT, BLACK)
    box(d, 340, 230, 620, 355, (250, 230, 230))
    ctext(d, 480, 255, "phi > 1(過濃)", FS, RED)
    ctext(d, 480, 290, "すすが出やすい", FT, GRAY)
    ctext(d, 480, 320, "未燃分が残りやすい", FT, BLACK)
    note(d, "火炎温度は phi=1 付近で最高. 希薄予混合燃焼はこの性質を利用")
    save(im, "t1f19EquivalenceRatio")


# ============================================================
# 19-20 t1f19ExplosionLimits : 爆発限界(第1/2/3限界と爆発半島)
# ============================================================
def explosion_limits():
    im, d = new(); title(d, "爆発限界(酸素-水素): 第1/第2/第3限界と爆発半島")
    ox, oy, xl, yl = 110, 350, 440, 250
    axes(d, ox, oy, xl + 20, yl + 20, "温度 T", "圧力 P")
    # Z字状の爆発限界曲線(低温側から A->B->C->D)
    A = (ox + 0.20 * xl, oy - 0.15 * yl)
    B = (ox + 0.42 * xl, oy - 0.55 * yl)
    C = (ox + 0.30 * xl, oy - 0.72 * yl)
    D = (ox + 0.62 * xl, oy - 0.95 * yl)
    d.line((A[0], A[1], B[0], B[1]), fill=RED, width=3)
    d.line((B[0], B[1], C[0], C[1]), fill=GREEN, width=3)
    d.line((C[0], C[1], D[0], D[1]), fill=BLUE, width=3)
    for (p, lab) in [(A, "A"), (B, "B"), (C, "C"), (D, "D")]:
        pcircle(d, p[0], p[1], 6, BLACK, BLACK, 1)
        ctext(d, p[0] - 12, p[1] - 12, lab, FT, BLACK)
    ctext(d, (A[0] + B[0]) / 2 + 40, (A[1] + B[1]) / 2, "第1限界 AB", FT, RED, "lm")
    ctext(d, (B[0] + C[0]) / 2 - 60, (B[1] + C[1]) / 2, "第2限界 BC", FT, GREEN, "rm")
    ctext(d, (C[0] + D[0]) / 2 + 30, (C[1] + D[1]) / 2, "第3限界 CD", FT, BLUE, "lm")
    ctext(d, B[0] - 10, B[1] + 30, "爆発半島", FT, GRAY)
    ctext(d, ox + 0.15 * xl, oy - 0.75 * yl, "爆発する", FT, GRAY)
    eqbox(d, 400, 388, "第2限界 = 連鎖分枝反応 と 停止反応 のつりあい", 560, 40, BLACK, FILL2, FS)
    note(d, "ABCの突起が爆発半島. CDは圧力が高いほど低温で爆発(熱爆発)")
    save(im, "t1f19ExplosionLimits")


# ============================================================
if __name__ == "__main__":
    detailed_mechanism()        # 19-1
    elementary_reaction()       # 19-2
    global_reaction_rate()      # 19-3
    chain_reaction()            # 19-4
    radical()                   # 19-5
    exo_endothermic()           # 19-6
    activation_energy()         # 19-7
    heat_of_reaction()          # 19-8
    modified_arrhenius()        # 19-9
    rate_unit_conversion()      # 19-10
    third_body()                # 19-11
    fall_off()                  # 19-12
    sensitivity_coefficient()   # 19-13
    adiabatic_flame_temp()      # 19-14
    flame_temp_order()          # 19-15
    nox_formation()             # 19-16
    nox_reduction()             # 19-17
    soot_formation()            # 19-18
    equivalence_ratio()         # 19-19
    explosion_limits()          # 19-20
    print("done t1f ch19")
