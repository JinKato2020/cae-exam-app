# -*- coding: utf-8 -*-
"""熱流体力学1級 第20章「層流予混合火炎」の公式・用語図(t1f20*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(rho, delta, lambda, Su, Sb, Tu, Tb, Le, Karlovitz, propto 等)。
※ 問題図 t1e20* とは別ファイル。上書きしない。"""
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
# ============  公式・用語図  t1f20*  (20)  ==================
# ============================================================

# 20-1 t1f20PremixedFlame : 層流予混合火炎(混合->噴出->円錐火炎)
def premixed_flame():
    im, d = new(); title(d, "層流予混合火炎 : 燃料と空気を混ぜてから燃やす")
    # バーナー管
    bx0, bx1, by0, by1 = 250, 410, 250, 380
    box(d, bx0, by0, bx1, by1, FILL1, 3)
    # 供給(燃料+空気)
    arrow(d, 70, 300, bx0 - 4, 300, BLUE, 3, 12)
    ctext(d, 130, 278, "燃料", FT, BLUE)
    arrow(d, 70, 345, bx0 - 4, 345, GREEN, 3, 12)
    ctext(d, 130, 367, "空気", FT, GREEN)
    ctext(d, (bx0 + bx1) / 2, 330, "予混合", FT, GRAY)
    ctext(d, (bx0 + bx1) / 2, 355, "(層流)", FT, GRAY)
    # 未燃ガスの上昇
    for xx in (300, 330, 360):
        arrow(d, xx, by0 - 2, xx, 205, GRAY, 2, 9)
    # 円錐火炎
    tipx, tipy = 330, 110
    d.line((bx0 + 18, by0, tipx, tipy), fill=RED, width=3)
    d.line((bx1 - 18, by0, tipx, tipy), fill=RED, width=3)
    ctext(d, 470, 150, "円錐状の", FT, RED, "lm")
    ctext(d, 470, 172, "層流予混合火炎", FT, RED, "lm")
    # 未燃/既燃ラベル
    ctext(d, 330, 225, "未燃予混合ガス Tu", FT, BLUE)
    ctext(d, 470, 118, "火炎面", FT, RED, "lm")
    # 逆火の注意矢印
    arrow(d, 300, 235, 300, by0 + 6, ORANGE, 2, 10)
    ctext(d, 200, 210, "供給を絞ると逆火", FT, ORANGE, "lm")
    note(d, "混ぜてから燃やす予混合燃焼. 火炎は薄く円錐状. 逆火(未燃側へ逆流)が起こり得る")
    save(im, "t1f20PremixedFlame")


# 20-2 t1f20FlameStructure : 火炎構造(予熱帯/反応帯/火炎帯・S字温度)
def flame_structure():
    im, d = new(); title(d, "火炎構造 : 予熱帯 -> 反応帯, 温度は Tu->Ti->Tb のS字")
    ox, oy, xl, yl = 90, 350, 500, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "位置 x", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 30, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 30, "温度 T", FT, BLACK, "rm")
    # 帯の区分
    xp0 = ox + 0.30 * xl   # 予熱帯開始
    xi = ox + 0.62 * xl    # 反応帯入口 Ti
    xr = ox + 0.80 * xl    # 反応帯終わり
    for xx in (xp0, xi, xr):
        dashed(d, xx, oy, xx, oy - yl - 4, LGRAY, 1, 6, 5)
    # S字温度分布
    y_u = oy - 0.10 * yl
    y_i = oy - 0.62 * yl
    y_b = oy - 0.92 * yl
    d.line((ox + 0.02 * xl, y_u, xp0, y_u), fill=BLUE, width=3)
    pts = []
    for i in range(0, 101):
        t = i / 100
        x = xp0 + (xr - xp0) * t
        # 前半(予熱帯)緩→後半(反応帯)急のS字
        y = y_u + (y_b - y_u) * (0.5 - 0.5 * math.cos(math.pi * t))
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    d.line((xr, y_b, ox + 0.97 * xl, y_b), fill=GREEN, width=3)
    # Ti の点(勾配最大)
    node(d, xi, y_i, 5, fill=RED, col=RED)
    ctext(d, xi + 6, y_i - 14, "Ti(勾配最大)", FT, RED, "lm")
    ctext(d, ox + 0.14 * xl, y_u - 16, "Tu 未燃", FT, BLUE)
    ctext(d, ox + 0.90 * xl, y_b - 16, "Tb 既燃", FT, GREEN)
    # 帯ラベルと寸法
    ctext(d, (xp0 + xi) / 2, oy - yl - 14, "予熱帯 dp", FT, GRAY)
    ctext(d, (xi + xr) / 2, oy - yl - 14, "反応帯 dr", FT, GRAY)
    dim(d, xp0, oy + 24, xr, oy + 24, "火炎帯 d = dp + dr", col=GRAY)
    # 熱伝導の向き(反応帯->予熱帯)
    arrow(d, xi - 6, oy - 0.30 * yl, xp0 + 10, oy - 0.30 * yl, ORANGE, 2, 11)
    ctext(d, (xp0 + xi) / 2, oy - 0.30 * yl - 16, "熱伝導(反応帯->予熱帯)", FT, ORANGE)
    note(d, "予熱帯は熱伝導で加熱. Ti は温度勾配の極大点. 熱は下流から上流へ伝わる")
    save(im, "t1f20FlameStructure")


# 20-3 t1f20ConservationEqs : 火炎面前後の3保存式
def conservation_eqs():
    im, d = new(); title(d, "火炎面前後の保存則 : 質量・運動量・エネルギー")
    # 火炎面
    fx = 330
    d.line((fx, 90, fx, 300), fill=RED, width=3)
    ctext(d, fx, 78, "火炎面", FT, RED)
    # 上流(1)未燃 / 下流(2)既燃
    box(d, 60, 110, fx - 6, 300, (232, 240, 250))
    box(d, fx + 6, 110, 600, 300, (232, 248, 236))
    ctext(d, 195, 132, "断面1 (未燃)", FS, BLUE)
    ctext(d, 465, 132, "断面2 (既燃)", FS, GREEN)
    ctext(d, 195, 165, "rho1, u1, p1, h1", FT, GRAY)
    ctext(d, 465, 165, "rho2, u2, p2, h2", FT, GRAY)
    arrow(d, 90, 210, 300, 210, BLUE, 3, 12); ctext(d, 195, 190, "u1", FT, BLUE)
    arrow(d, 360, 210, 585, 210, GREEN, 4, 13); ctext(d, 470, 190, "u2 (>u1)", FT, GREEN)
    ctext(d, 195, 255, "密度 大", FT, GRAY)
    ctext(d, 465, 255, "密度 小 (膨張)", FT, GRAY)
    # 3式
    box(d, 55, 320, 605, 405, FILL1, 2)
    ctext(d, 330, 342, "質量:  rho1 u1 = rho2 u2 = mdot", FT, BLACK)
    ctext(d, 330, 368, "運動量:  p1 + rho1 u1^2 = p2 + rho2 u2^2", FT, BLACK)
    ctext(d, 330, 394, "エネルギー:  h1 + u1^2/2 = h2 + u2^2/2", FT, BLACK)
    note(d, "燃焼で密度低下 -> 質量保存より u2>u1. これが圧力低下の議論の起点", y=312)
    save(im, "t1f20ConservationEqs")


# 20-4 t1f20RayleighLine : Rayleigh線(p-1/rho, 傾き -mdot^2)
def rayleigh_line():
    im, d = new(); title(d, "Rayleigh線 : (p2-p1)/(1/rho2 - 1/rho1) = -mdot^2")
    ox, oy, xl, yl = 130, 340, 420, 230
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "比容積 1/rho", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "圧力 p", FS, BLACK, "rm")
    # 右下がり直線(傾き -mdot^2 <0)
    x1, y1 = ox + 0.10 * xl, oy - 0.85 * yl   # 未燃(1) 小さい1/rho,高い p
    x2, y2 = ox + 0.85 * xl, oy - 0.20 * yl   # 既燃(2) 大きい1/rho,低い p
    d.line((x1, y1, x2, y2), fill=BLUE, width=3)
    node(d, x1, y1, 6, fill=BLUE, col=BLUE); ctext(d, x1 - 10, y1 - 12, "1 未燃", FT, BLUE, "rm")
    node(d, x2, y2, 6, fill=GREEN, col=GREEN); ctext(d, x2 + 10, y2 + 14, "2 既燃", FT, GREEN, "lm")
    # 密度低下=比容積増加, 圧力低下 の注記
    dashed(d, x1, y1, x1, oy, GRAY, 1, 6, 5)
    dashed(d, x2, y2, x2, oy, GRAY, 1, 6, 5)
    dashed(d, ox, y1, x1, y1, GRAY, 1, 6, 5)
    dashed(d, ox, y2, x2, y2, GRAY, 1, 6, 5)
    arrow(d, x2 + 40, y1, x2 + 40, y2, RED, 3, 12)
    ctext(d, x2 + 48, (y1 + y2) / 2, "p 低下", FT, RED, "lm")
    ctext(d, ox + 0.30 * xl, oy - 0.72 * yl, "傾き -mdot^2 < 0", FT, RED, "lm")
    note(d, "燃焼後は密度低下(1/rho 増). 傾きが負なので圧力 p は低下する")
    save(im, "t1f20RayleighLine")


# 20-5 t1f20RankineHugoniot : h2-h1 = (1/2)(1/rho2+1/rho1)(p2-p1)
def rankine_hugoniot():
    im, d = new(); title(d, "Rankine-Hugoniot : h2-h1 = (1/2)(1/rho2 + 1/rho1)(p2-p1)")
    # 導出の流れを縦に
    box(d, 60, 90, 600, 150, (232, 240, 250), 2)
    ctext(d, 330, 120, "3保存式 -> 途中式 h2-h1 = (1/2)(rho2^2/rho1^2 - 1)u2^2", FT, BLACK)
    arrow(d, 330, 152, 330, 182, GRAY, 3, 12)
    box(d, 60, 186, 600, 246, FILL1, 2)
    ctext(d, 330, 216, "h2 - h1 = (1/2)(1/rho2 + 1/rho1)(p2 - p1)", FS, BLACK)
    arrow(d, 330, 248, 330, 278, GRAY, 3, 12)
    # 符号の判定
    box(d, 60, 282, 600, 405, (232, 248, 236), 2)
    ctext(d, 330, 306, "u2 > u1  =>  h2 - h1 < 0 (左辺 負)", FT, BLUE)
    ctext(d, 330, 336, "(1/rho2 + 1/rho1) > 0  (常に 正)", FT, GRAY)
    ctext(d, 330, 366, "=>  p2 - p1 < 0  :  燃焼後に圧力低下", FS, RED)
    note(d, "膨張で u2>u1 ゆえエンタルピー変化は負. 比容積和は正だから圧力は低下する", y=394)
    save(im, "t1f20RankineHugoniot")


# 20-6 t1f20BurnedGasVelocity : S = Su(Tb/Tu - 1)
def burned_gas_velocity():
    im, d = new(); title(d, "静止気体中の火炎下流向き速度  S = Su (Tb/Tu - 1)")
    # 火炎面
    fx = 330
    d.line((fx, 110, fx, 300), fill=RED, width=3)
    ctext(d, fx, 96, "火炎面", FT, RED)
    ctext(d, 150, 135, "静止 未燃ガス Tu", FT, BLUE)
    ctext(d, 495, 135, "既燃ガス Tb (膨張)", FT, GREEN)
    # 火炎伝播 Su(未燃側へ)
    arrow(d, fx - 8, 200, 150, 200, RED, 4, 14)
    ctext(d, 230, 180, "火炎伝播 Su", FT, RED)
    # 既燃ガスの下流向き速度 S
    arrow(d, fx + 8, 250, 560, 250, GREEN, 4, 14)
    ctext(d, 470, 230, "既燃ガス速度 S", FT, GREEN)
    # 導出カード
    box(d, 60, 320, 600, 405, FILL1, 2)
    ctext(d, 330, 344, "質量保存 Su rho_u = Sb rho_b -> 膨張速度 Sb = Su (rho_u/rho_b)", FT, BLACK)
    ctext(d, 330, 372, "同圧 rho_u/rho_b = Tb/Tu -> S = Sb - Su = Su(Tb/Tu - 1)", FT, RED)
    note(d, "燃えて膨張したぶんだけ既燃ガスが押し出されて動く(温度比が効く)", y=310)
    save(im, "t1f20BurnedGasVelocity")


# 20-7 t1f20SoapBubble : シャボン玉法 Su=(ru/rb)^3 Sb
def soap_bubble():
    im, d = new(); title(d, "シャボン玉法  Su = (ru/rb)^3 Sb")
    # 点火前(小) -> 全燃焼後(大)
    c1x, c1y, r1 = 180, 220, 55
    pcircle(d, c1x, c1y, r1, (238, 244, 250), BLUE, 3)
    node(d, c1x, c1y, 5, fill=RED, col=RED)
    ctext(d, c1x, c1y + 22, "点火", FT, RED)
    ctext(d, c1x, c1y - r1 - 16, "点火前 半径 ru", FT, BLUE)
    c2x, c2y, r2 = 470, 220, 95
    pcircle(d, c2x, c2y, r2, (238, 248, 240), GREEN, 3)
    # 内側に既燃・球状火炎伝播
    dashed(d, c2x, c2y, c2x + r2, c2y, GRAY, 1, 6, 5)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        arrow(d, c2x + 0.55 * r2 * math.cos(rad), c2y + 0.55 * r2 * math.sin(rad),
              c2x + 0.92 * r2 * math.cos(rad), c2y + 0.92 * r2 * math.sin(rad), RED, 2, 9)
    ctext(d, c2x, c2y - r2 - 16, "全燃焼後 半径 rb (>ru)", FT, GREEN)
    arrow(d, c1x + r1 + 10, c1y, c2x - r2 - 10, c1y, GRAY, 3, 13)
    ctext(d, 330, 150, "球状火炎が外向きに伝播 Sb", FT, GRAY)
    # 式カード
    box(d, 60, 330, 600, 405, FILL1, 2)
    ctext(d, 330, 354, "連続 Su=(rho_b/rho_u)Sb, 質量 rho_u ru^3 = rho_b rb^3", FT, BLACK)
    ctext(d, 330, 382, "=>  Su = (ru/rb)^3 Sb   (膨張比が大きいほど Su は小)", FT, RED)
    note(d, "定圧仮定. 燃えて rb>ru に膨らむので Su は伝播速度 Sb より小さい", y=320)
    save(im, "t1f20SoapBubble")


# 20-8 t1f20ThermalTheory : Su = (a0/d)(Tb-Tu)/(Ti-Tu) ~ a0/d
def thermal_theory():
    im, d = new(); title(d, "熱理論 : 層流燃焼速度 Su は熱拡散率 a0 に比例")
    # 予熱帯のエネルギー収支の模式
    ox, oy = 90, 250
    box(d, 90, 130, 300, 250, (250, 236, 236))
    ctext(d, 195, 112, "予熱帯", FT, RED)
    ctext(d, 195, 165, "熱伝導 流入", FT, GRAY)
    arrow(d, 320, 190, 300, 190, ORANGE, 3, 12)
    ctext(d, 360, 168, "反応帯からの", FT, GRAY, "lm")
    ctext(d, 360, 190, "熱伝導 lambda(dT/dx)i", FT, ORANGE, "lm")
    arrow(d, 90, 215, 300, 215, BLUE, 3, 12)
    ctext(d, 195, 232, "質量流束 mdot=rho_u Su", FT, BLUE)
    # 式の導出
    box(d, 55, 285, 605, 405, FILL1, 2)
    ctext(d, 330, 308, "予熱帯収支 lambda(dT/dx)i = mdot cp (Ti-Tu),  mdot=rho_u Su", FT, BLACK)
    ctext(d, 330, 336, "(dT/dx)i = (Tb-Tu)/d  を代入して整理", FT, GRAY)
    ctext(d, 330, 364, "Su = (a0/d)(Tb-Tu)/(Ti-Tu) ~ a0/d,   a0 = lambda/(rho_u cp)", FS, RED)
    ctext(d, 330, 392, "Ti ~ Tb とすると Su は熱拡散率 a0 に比例 (Su propto a0)", FT, RED)
    note(d, "熱が伝わりやすい(a0 大)ほど, 火炎帯が薄い(d 小)ほど燃焼速度は速い", y=118)
    save(im, "t1f20ThermalTheory")


# 20-9 t1f20ThermalDiffusivity : a0 = lambda/(rho_u cp)
def thermal_diffusivity():
    im, d = new(); title(d, "熱拡散率  a0 = lambda / (rho_u cp)  [m^2/s]")
    # 分数の可視化カード
    box(d, 180, 110, 480, 210, FILL1, 2)
    ctext(d, 330, 138, "a0 = lambda / (rho_u cp)", FL, BLACK)
    ctext(d, 330, 178, "熱伝導率 / (密度 x 比熱)", FT, GRAY)
    # 大小の効き
    box(d, 60, 240, 330, 360, (232, 248, 236), 2)
    ctext(d, 195, 264, "a0 が大きい", FS, GREEN)
    ctext(d, 195, 296, "lambda 大 / rho,cp 小", FT, GRAY)
    ctext(d, 195, 326, "熱が速く広がる", FT, GREEN)
    ctext(d, 195, 348, "-> Su 速い", FT, GREEN)
    box(d, 340, 240, 600, 360, (250, 236, 236), 2)
    ctext(d, 470, 264, "a0 が小さい", FS, RED)
    ctext(d, 470, 296, "lambda 小 / rho,cp 大", FT, GRAY)
    ctext(d, 470, 326, "熱が広がりにくい", FT, RED)
    ctext(d, 470, 348, "-> Su 遅い", FT, RED)
    note(d, "熱の広がりやすさの物性値. 層流燃焼速度 Su は a0 に比例(Su propto a0)")
    save(im, "t1f20ThermalDiffusivity")


# 20-10 t1f20BurningVelocity : Su(ガス基準) と Sb(静止系基準)
def burning_velocity():
    im, d = new(); title(d, "層流燃焼速度 Su と 火炎伝播速度 Sb の違い")
    fx = 330
    d.line((fx, 110, fx, 285), fill=RED, width=3)
    ctext(d, fx, 96, "火炎面", FT, RED)
    ctext(d, 165, 130, "未燃ガス Tu", FT, BLUE)
    ctext(d, 495, 130, "既燃ガス Tb", FT, GREEN)
    # Su: ガスに対する火炎の速さ
    arrow(d, fx - 8, 175, 175, 175, RED, 4, 14)
    ctext(d, 250, 156, "Su : ガスに対する速さ", FT, RED)
    # Sb: 静止系での火炎の速さ(膨張ぶん速い)
    arrow(d, fx + 8, 235, 575, 235, GREEN, 4, 14)
    ctext(d, 470, 258, "Sb : 静止系での速さ", FT, GREEN)
    box(d, 60, 305, 600, 405, FILL1, 2)
    ctext(d, 330, 330, "Su : 混合気の圧力・温度・当量比で決まる(a0 に比例)", FT, BLACK)
    ctext(d, 330, 358, "Sb = Su (rho_u/rho_b) = Su (Tb/Tu)  (膨張ぶん速い)", FT, GREEN)
    ctext(d, 330, 386, "Su=ガス基準, Sb=静止(地面)基準. 混同しない", FT, RED)
    note(d, "バーナー上で火炎を静止させるには噴出速度を Su に釣り合わせる", y=296)
    save(im, "t1f20BurningVelocity")


# 20-11 t1f20Flashback : 逆火(口径大で起こりやすい)
def flashback():
    im, d = new(); title(d, "逆火(フラッシュバック) : 火炎が未燃側へ逆流(口径大で顕著)")
    # 大口径バーナー(逆火)
    box(d, 90, 150, 230, 360, FILL1, 3)
    ctext(d, 160, 130, "口径 大 (A,B)", FS, BLUE)
    # 供給を絞る(細い上向き矢印)
    arrow(d, 160, 355, 160, 300, GRAY, 2, 10)
    ctext(d, 160, 375, "供給 小", FT, GRAY)
    # 火炎が下へ逆流
    d.line((100, 250, 160, 210), fill=RED, width=3)
    d.line((220, 250, 160, 210), fill=RED, width=3)
    arrow(d, 160, 220, 160, 320, RED, 4, 14)
    ctext(d, 285, 235, "消費 > 供給", FT, RED, "lm")
    ctext(d, 285, 262, "-> 火炎が管内へ逆流", FT, RED, "lm")
    ctext(d, 285, 289, "(発熱大・熱損失小)", FT, GRAY, "lm")
    # 小口径(消炎)の対比
    box(d, 470, 210, 540, 360, FILL1, 3)
    ctext(d, 505, 190, "口径 小 (C)", FT, GRAY)
    d.line((478, 300, 505, 275), fill=LGRAY, width=2)
    d.line((532, 300, 505, 275), fill=LGRAY, width=2)
    d.line((488, 250, 522, 284), fill=RED, width=3)
    d.line((522, 250, 488, 284), fill=RED, width=3)
    ctext(d, 505, 372, "壁面熱吸収大 -> 消炎", FT, RED)
    note(d, "予混合燃焼に特有で危険. 口径大=発熱大で逆火, 口径小=熱損失大で消炎")
    save(im, "t1f20Flashback")


# 20-12 t1f20Quenching : 消炎(壁面熱吸収 / 伸張 theta=90)
def quenching():
    im, d = new(); title(d, "消炎(クエンチ) : 壁面熱吸収 or 強い火炎伸張で吹き消え")
    # 左: 細管の壁面熱吸収
    box(d, 55, 100, 300, 360, "white", 2)
    ctext(d, 178, 122, "細い管 : 壁面熱吸収", FT, GRAY)
    wall(d, 95, 150, 340, side=1, n=8)
    wall(d, 262, 150, 340, side=-1, n=8)
    d.line((110, 260, 178, 220), fill=RED, width=3)
    d.line((246, 260, 178, 220), fill=RED, width=3)
    arrow(d, 110, 240, 100, 240, ORANGE, 2, 10)
    arrow(d, 246, 240, 256, 240, ORANGE, 2, 10)
    ctext(d, 178, 300, "熱が壁に奪われ消炎", FT, RED)
    # 右: 火炎伸張 theta=90 で吹き消え
    box(d, 320, 100, 605, 360, "white", 2)
    ctext(d, 462, 122, "強い伸張 theta -> 90deg", FT, GRAY)
    # 速度勾配(せん断)
    for i, yy in enumerate(range(170, 300, 26)):
        arrow(d, 350, yy, 350 + (i + 1) * 22, yy, BLUE, 2, 9)
    ctext(d, 360, 320, "速度勾配(せん断)", FT, BLUE, "lm")
    # 伸ばされる火炎
    d.line((470, 160, 560, 300), fill=RED, width=3)
    ctext(d, 560, 200, "火炎伸張大", FT, RED, "lm")
    ctext(d, 560, 224, "-> 吹き消え", FT, RED, "lm")
    note(d, "口径小の壁面熱吸収や, theta=90deg 付近の強い火炎伸張で火炎が保持できず消える")
    save(im, "t1f20Quenching")


# 20-13 t1f20EquivalenceRatio : 当量比依存(過濃側でピーク)
def equivalence_ratio():
    im, d = new(); title(d, "層流燃焼速度の当量比依存 : メタン空気は やや過濃 でピーク")
    ox, oy, xl, yl = 110, 350, 460, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "当量比 phi", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "層流燃焼速度 Su", FT, BLACK, "rm")
    # phi=1 の位置
    x1 = ox + 0.45 * xl
    dashed(d, x1, oy, x1, oy - yl - 4, LGRAY, 1, 6, 5)
    ctext(d, x1, oy + 18, "phi=1 (化学量論)", FT, GRAY)
    # ピークはやや過濃(phi>1)
    xpk = ox + 0.55 * xl
    pts = []
    for i in range(0, 201):
        t = i / 200
        x = ox + t * xl
        # ピークを xpk 付近に
        val = math.exp(-((x - xpk) / (0.22 * xl)) ** 2)
        pts.append((x, oy - val * yl * 0.9))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ypk = oy - 0.9 * yl
    node(d, xpk, ypk, 6, fill=RED, col=RED)
    dashed(d, xpk, oy, xpk, ypk, GRAY, 1, 6, 5)
    ctext(d, xpk, oy + 18, "phi やや >1", FT, RED)
    ctext(d, xpk + 10, ypk - 14, "最大(過濃側)", FT, RED, "lm")
    ctext(d, ox + 0.12 * xl, oy - 0.30 * yl, "希薄", FT, GRAY)
    ctext(d, ox + 0.88 * xl, oy - 0.30 * yl, "過濃", FT, GRAY)
    note(d, "ちょうど phi=1 ではなく, 熱解離の影響で やや過濃(phi>1)側で Su が最大になる")
    save(im, "t1f20EquivalenceRatio")


# 20-14 t1f20PressureDependence : 圧力依存(メタン空気で低下)
def pressure_dependence():
    im, d = new(); title(d, "層流燃焼速度の圧力依存 : メタン空気は高圧ほど低下")
    ox, oy, xl, yl = 120, 350, 430, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "圧力 p", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "層流燃焼速度 Su", FT, BLACK, "rm")
    # 右下がり曲線
    pts = []
    for i in range(0, 201):
        t = 0.10 + (1.0 - 0.10) * i / 200
        val = 0.30 / t
        pts.append((ox + ((t - 0.10) / 0.9) * xl, oy - val * yl * 0.9))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 1/5/10 気圧の点
    for (t, lab, col) in [(0.14, "1 atm", GREEN), (0.5, "5 atm", ORANGE), (0.92, "10 atm", RED)]:
        xp = ox + ((t - 0.10) / 0.9) * xl
        val = 0.30 / t
        yp = oy - val * yl * 0.9
        node(d, xp, yp, 5, fill=col, col=col)
        dashed(d, xp, oy, xp, yp, LGRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, col)
    ctext(d, ox + 0.55 * xl, oy - 0.55 * yl, "高圧ほど遅い", FT, RED, "lm")
    ctext(d, ox + 0.4 * xl, oy - 0.85 * yl, "(当量比1.0 メタン空気)", FT, GRAY, "lm")
    note(d, "1気圧が最も速く, 10気圧が最も遅い. 圧力上昇で Su は小さくなる")
    save(im, "t1f20PressureDependence")


# 20-15 t1f20DilutionEffect : 希釈ガス(水蒸気 vs アルゴン)
def dilution_effect():
    im, d = new(); title(d, "希釈ガスの効果 : 比熱大の水蒸気は火炎温度を下げ Su 減")
    # 左: 水蒸気希釈
    box(d, 55, 100, 320, 370, (235, 240, 250), 2)
    ctext(d, 187, 124, "水蒸気で希釈", FS, BLUE)
    ctext(d, 187, 154, "比熱 大", FT, RED)
    # 火炎温度バー(低め)
    d.rectangle((150, 230, 225, 320), outline=BLACK, width=2, fill=(235, 240, 250))
    ctext(d, 187, 200, "火炎温度 低", FT, RED)
    ctext(d, 187, 340, "-> Su 小", FT, RED)
    # 右: アルゴン希釈
    box(d, 340, 100, 605, 370, (235, 248, 238), 2)
    ctext(d, 472, 124, "アルゴンで希釈", FS, GREEN)
    ctext(d, 472, 154, "比熱 小", FT, GREEN)
    d.rectangle((435, 185, 510, 320), outline=BLACK, width=2, fill=(235, 248, 238))
    ctext(d, 472, 160, "火炎温度 高", FT, GREEN)
    ctext(d, 472, 340, "-> Su 大", FT, GREEN)
    note(d, "同条件ならアルゴン希釈のほうが水蒸気希釈より層流燃焼速度が大きい")
    save(im, "t1f20DilutionEffect")


# 20-16 t1f20FlammabilityLimit : 可燃限界(下限界/上限界, H2 vs CH4)
def flammability_limit():
    im, d = new(); title(d, "可燃限界 : 下限界〜上限界の間だけ火炎が伝播")
    ox, xl = 110, 460
    # 帯グラフ2本
    def band(y, lo, hi, lab, col):
        y0, y1 = y, y + 46
        d.rectangle((ox, y0, ox + xl, y1), outline=BLACK, width=2, fill="white")
        xl0 = ox + lo * xl; xh0 = ox + hi * xl
        d.rectangle((xl0, y0, xh0, y1), outline=col, width=2, fill=(235, 244, 250) if col == BLUE else (235, 248, 238))
        ctext(d, (xl0 + xh0) / 2, (y0 + y1) / 2, "可燃範囲", FT, col)
        ctext(d, ox - 8, (y0 + y1) / 2, lab, FT, col, "rm")
        dashed(d, xl0, y0, xl0, y1 + 8, GRAY, 1, 5, 4)
        dashed(d, xh0, y0, xh0, y1 + 8, GRAY, 1, 5, 4)
    ctext(d, ox + xl / 2, 90, "燃料濃度 ->", FT, GRAY)
    band(130, 0.05, 0.16, "CH4", GREEN)
    band(230, 0.05, 0.80, "H2", BLUE)
    ctext(d, ox + 0.05 * xl, 300, "下限界(薄い)", FT, GRAY)
    ctext(d, ox + 0.80 * xl, 300, "上限界(濃い)", FT, GRAY)
    box(d, 60, 325, 600, 405, FILL1, 2)
    ctext(d, 330, 350, "濃い側=上限界, 薄い側=下限界. 温度・圧力・重力に依存", FT, BLACK)
    ctext(d, 330, 380, "H2は拡散速度大で可燃範囲が CH4 より広い", FT, BLUE)
    note(d, "細すぎる管では壁面熱損失で消炎するため十分太い円管で測る", y=316)
    save(im, "t1f20FlammabilityLimit")


# 20-17 t1f20Karlovitz : カルロビッツ数 K=(dUu/dy)(d/Uu)
def karlovitz():
    im, d = new(); title(d, "カルロビッツ数(火炎伸張度)  K = (dUu/dy)(d/Uu)")
    # せん断流場と湾曲火炎
    ox = 90
    # 速度勾配プロファイル
    for i, yy in enumerate(range(140, 300, 24)):
        arrow(d, ox, yy, ox + (i + 1) * 20, yy, BLUE, 2, 9)
    ctext(d, ox + 5, 320, "速度勾配 dUu/dy", FT, BLUE, "lm")
    # 火炎面(曲率半径R) と A,B点・流線間隔
    ax, ay = 360, 180
    bx, by = 360, 250
    d.arc((300, 120, 470, 320), -60, 60, fill=RED, width=3)
    ctext(d, 455, 130, "火炎面(曲率R)", FT, RED, "lm")
    node(d, ax, ay, 5, fill=BLACK); ctext(d, ax - 10, ay - 12, "A", FT, BLACK, "rm")
    node(d, bx, by, 5, fill=BLACK); ctext(d, bx - 10, by + 12, "B", FT, BLACK, "rm")
    arrow(d, ax + 10, ay, ax + 70, ay, GRAY, 2, 10); ctext(d, ax + 45, ay - 14, "Uu", FT, GRAY)
    dim(d, 300, ay, 300, by, "dy = d sin(theta)", col=GRAY)
    # 式カード
    box(d, 60, 335, 600, 405, FILL1, 2)
    ctext(d, 330, 358, "質量流束増加率 1 + (dUu/dy)(d sin theta / Uu)", FT, BLACK)
    ctext(d, 330, 386, "一般式  K = (dUu/dy)(d / Uu)   (d=予熱帯厚さ)", FS, RED)
    note(d, "火炎が引き伸ばされる度合い. theta -> 90deg で吹き消え(消炎)しやすい", y=326)
    save(im, "t1f20Karlovitz")


# 20-18 t1f20LewisNumber : ルイス数 Le=lambda/(rho D Cp)
def lewis_number():
    im, d = new(); title(d, "ルイス数  Le = lambda / (rho D Cp) : 熱拡散/物質拡散")
    # 定義カード
    box(d, 150, 95, 510, 180, FILL1, 2)
    ctext(d, 330, 122, "Le = lambda / (rho D Cp)", FL, BLACK)
    ctext(d, 330, 160, "熱の拡散 / 物質の拡散", FT, GRAY)
    # Le<1 と Le>1 の対比
    box(d, 55, 205, 330, 370, (235, 248, 238), 2)
    ctext(d, 192, 230, "Le < 1", FS, GREEN)
    ctext(d, 192, 262, "物質拡散 優勢", FT, GRAY)
    arrow(d, 192, 285, 192, 312, GREEN, 3, 12)
    ctext(d, 192, 332, "反応物流入でエンタルピー増", FT, GREEN)
    ctext(d, 192, 356, "火炎温度 上がりやすい", FT, GREEN)
    box(d, 340, 205, 605, 370, (250, 236, 236), 2)
    ctext(d, 472, 230, "Le > 1", FS, RED)
    ctext(d, 472, 262, "熱拡散 優勢", FT, GRAY)
    arrow(d, 472, 285, 472, 312, RED, 3, 12)
    ctext(d, 472, 332, "エンタルピー流出", FT, RED)
    ctext(d, 472, 356, "火炎温度 低下(伸張で消炎)", FT, RED)
    note(d, "熱と物質の拡散のアンバランス(拡散熱的不均衡)=ルイス数効果. 火炎安定を左右")
    save(im, "t1f20LewisNumber")


# 20-19 t1f20CounterflowFlame : 対向流予混合火炎
def counterflow_flame():
    im, d = new(); title(d, "対向流予混合火炎 : 向き合う流れの中の 伸張火炎")
    cy = 240
    # 上ノズルと下ノズル
    box(d, 250, 90, 410, 130, FILL1, 3); ctext(d, 330, 110, "予混合気ノズル", FT, GRAY)
    box(d, 250, 350, 410, 390, FILL1, 3); ctext(d, 330, 370, "予混合気ノズル", FT, GRAY)
    for xx in (285, 330, 375):
        arrow(d, xx, 132, xx, 205, BLUE, 3, 11)
        arrow(d, xx, 348, xx, 275, GREEN, 3, 11)
    # よどみ面と平面火炎
    dashed(d, 150, cy, 510, cy, GRAY, 1, 8, 6)
    ctext(d, 150, cy - 14, "よどみ面", FT, GRAY, "lm")
    d.line((230, cy - 24, 430, cy - 24), fill=RED, width=4)
    ctext(d, 445, cy - 24, "平面火炎", FT, RED, "lm")
    # 伸張(横に広がる)
    arrow(d, 330, cy, 250, cy, RED, 2, 10)
    arrow(d, 330, cy, 410, cy, RED, 2, 10)
    ctext(d, 330, cy + 18, "伸張(速度勾配)", FT, RED)
    note(d, "伸張率を自由に変えられる標準配置. Le を変えて火炎温度・消炎を比較できる")
    save(im, "t1f20CounterflowFlame")


# 20-20 t1f20CellularFlame : セル状火炎(熱物質拡散 vs 流体力学)
def cellular_flame():
    im, d = new(); title(d, "セル状火炎 : 平面火炎がセル状に変形(不安定)")
    # 平面 -> セル状 への遷移
    d.line((90, 180, 250, 180), fill=RED, width=4)
    ctext(d, 170, 150, "平面火炎(安定)", FT, GRAY)
    arrow(d, 265, 180, 335, 180, GRAY, 3, 13)
    ctext(d, 300, 156, "希薄化", FT, GRAY)
    # セル状(波打つ)
    pts = []
    for i in range(0, 141):
        x = 350 + i * 1.7
        y = 180 + 18 * math.sin(i / 141 * 6 * math.pi)
        pts.append((x, y))
    d.line(pts, fill=RED, width=4, joint="curve")
    ctext(d, 470, 150, "セル状", FT, RED)
    # 2種の不安定の説明
    box(d, 55, 240, 330, 380, (250, 236, 236), 2)
    ctext(d, 192, 264, "熱・物質拡散不安定", FS, RED)
    ctext(d, 192, 296, "Le < 1 で発生", FT, RED)
    ctext(d, 192, 326, "希薄メタン空気は Le<1", FT, GRAY)
    ctext(d, 192, 354, "-> セル状に変形", FT, RED)
    box(d, 340, 240, 605, 380, (235, 240, 250), 2)
    ctext(d, 472, 264, "流体力学的不安定", FS, BLUE)
    ctext(d, 472, 296, "火炎面の急な密度変化", FT, GRAY)
    ctext(d, 472, 326, "に起因", FT, BLUE)
    ctext(d, 472, 354, "(Le の大小とは別要因)", FT, GRAY)
    note(d, "希薄メタン空気(Le<1)では 熱・物質拡散不安定 でセル状になる(問4-13)")
    save(im, "t1f20CellularFlame")


# ============================================================
if __name__ == "__main__":
    premixed_flame()          # 20-1
    flame_structure()         # 20-2
    conservation_eqs()        # 20-3
    rayleigh_line()           # 20-4
    rankine_hugoniot()        # 20-5
    burned_gas_velocity()     # 20-6
    soap_bubble()             # 20-7
    thermal_theory()          # 20-8
    thermal_diffusivity()     # 20-9
    burning_velocity()        # 20-10
    flashback()               # 20-11
    quenching()               # 20-12
    equivalence_ratio()       # 20-13
    pressure_dependence()     # 20-14
    dilution_effect()         # 20-15
    flammability_limit()      # 20-16
    karlovitz()               # 20-17
    lewis_number()            # 20-18
    counterflow_flame()       # 20-19
    cellular_flame()          # 20-20
    print("done t1f ch20")
