# -*- coding: utf-8 -*-
"""Phase2 Batch4: 図なし14問へ後付けする図。
verification-basics 第11章 結果の検証の基礎
(ver-11-1c,2,3c,3d,4,4b,6,7,11,12,13,14,15,17)。
接頭辞 ver11*。白地660x420・黒線画・機構/概念のみ(答え番号・最終数値は焼き込まない)。
すべて helpful(回答後表示)。JSON配線は別途。"""
import sys, math, os
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3, col=BLACK):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def mlines(d, cx, cy, lines, fnt=FT, fill=BLACK, lh=23):
    n = len(lines)
    y0 = cy - (n - 1) * lh / 2
    for i, s in enumerate(lines):
        ctext(d, cx, y0 + i * lh, s, fnt, fill)


# ============================================================
# ver-11-1c 特異点が生じやすい箇所と一般部
# ============================================================
def ver11SingularSpots():
    im, d = new(); title(d, "応力特異点が生じやすい箇所と一般部")

    def panel(x0, y0, x1, y1, lab, col):
        box(d, x0, y0, x1, y1, "white", 2, GRAY)
        ctext(d, (x0 + x1) / 2, y1 - 16, lab, FT, col)

    # (1) 点荷重の直下
    panel(40, 55, 320, 210, "1) 点荷重の直下", RED)
    box(d, 110, 130, 250, 175, FILL1)
    arrow(d, 180, 78, 180, 128, RED, 4, 13)
    node(d, 180, 130, 6, fill=RED, col=RED)
    ctext(d, 180, 100, "P (一点集中)", FT, RED)
    # (2) 点拘束の近傍
    panel(340, 55, 620, 210, "2) 点拘束の近傍", RED)
    box(d, 410, 108, 550, 150, FILL1)
    node(d, 480, 150, 6, fill=RED, col=RED)
    pin_support(d, 480, 153, 14)
    ctext(d, 480, 92, "一点で拘束", FT, RED)
    # (3) 鋭い再入隅の先端
    panel(40, 225, 320, 380, "3) 鋭い再入隅の先端", RED)
    d.polygon([(90, 250), (270, 250), (270, 300), (175, 300), (175, 355), (90, 355)],
              outline=BLACK, width=3, fill=FILL1)
    node(d, 175, 300, 5, fill=RED, col=RED)
    ctext(d, 210, 330, "凹角(丸みなし)", FT, RED)
    # (4) 平板内部の一般部(特異点でない)
    panel(340, 225, 620, 380, "4) 平板内部の一般部", GREEN)
    box(d, 400, 250, 560, 340, FILL1)
    for i, xx in enumerate(range(410, 561, 30)):
        dashed(d, xx, 252, xx, 338, LGRAY, 2)
    ctext(d, 480, 290, "なだらかに変化", FT, GREEN)
    ctext(d, 480, 322, "(特異点ではない)", FT, GREEN)
    note(d, "点荷重直下・点拘束近傍・鋭い凹角先端は特異点。一般部はなだらかで特異点にならない。")
    save(im, "ver11SingularSpots")


# ============================================================
# ver-11-2 周縁固定 円板のたわみ
# ============================================================
def ver11PlateDefl():
    im, d = new(); title(d, "周縁固定の円板と中央の最大たわみ")
    y0 = 130
    # 圧力矢印
    for xx in range(150, 511, 45):
        arrow(d, xx, 92, xx, y0 - 4, BLUE, 2, 9)
    ctext(d, 330, 78, "一様圧力 p", FT, BLUE)
    # 両端固定壁
    wall(d, 120, y0 - 8, y0 + 40, side=1, n=3)
    wall(d, 540, y0 - 8, y0 + 40, side=-1, n=3)
    # 変形前(破線)と変形後(たわみ曲線)
    dashed(d, 120, y0, 540, y0, GRAY, 2)
    pts = []
    for i in range(0, 421, 8):
        xx = 120 + i
        t = i / 420.0
        w = 46 * (16 * t * t * (1 - t) * (1 - t))  # 端で0・中央最大
        pts.append((xx, y0 + w))
    d.line(pts, fill=BLACK, width=3, joint="curve")
    ctext(d, 330, y0 + 62, "たわみ w", FT, BLACK)
    arrow(d, 330, y0 + 2, 330, y0 + 44, RED, 2, 9)
    ctext(d, 360, y0 + 24, "w_max", FT, RED, "lm")
    # 寸法・諸量
    dim(d, 120, y0 - 40, 540, y0 - 40, "直径 2a", col=GRAY)
    box(d, 90, 250, 570, 322, FILL2)
    mlines(d, 330, 286,
           ["w_max = p a^4 / (64 D) ,   D = E t^3 / (12(1-ν^2))",
            "a=400mm  t=8mm  p=0.05MPa  E=2.0e5MPa  ν=0.3"], FT, BLACK, 28)
    note(d, "曲げ剛性 D を先に求め、たわみ式へ代入する2段階。オーダー違いを検算で除く。")
    save(im, "ver11PlateDefl")


# ============================================================
# ver-11-3c エネルギーノルム誤差=全体的尺度(単調減少)
# ============================================================
def ver11EnergyNorm():
    im, d = new(); title(d, "エネルギーノルム誤差:全体的で単調に減少")
    axes(d, 90, 320, 470, 230, "要素細分化 →", "誤差")
    # 全体的なエネルギーノルム誤差:単調減少
    pts = []
    for i in range(0, 461, 10):
        t = i / 460.0
        y = 320 - (200 * math.exp(-3.0 * t) - 200 * math.exp(-3.0))
        pts.append((90 + i, y))
    d.line(pts, fill=BLUE, width=4, joint="curve")
    ctext(d, 430, 150, "エネルギーノルム誤差", FS, BLUE)
    ctext(d, 430, 174, "(全体的・単調減少)", FT, BLUE)
    # 局所の一点応力:特異点近傍で収束しない(振動)
    pts2 = []
    for i in range(0, 461, 6):
        t = i / 460.0
        y = 250 - 8 * math.sin(t * 22) - 20 * t
        pts2.append((90 + i, y))
    d.line(pts2, fill=RED, width=2, joint="curve")
    ctext(d, 300, 262, "局所の一点応力(特異点で収束せず)", FT, RED)
    note(d, "ひずみエネルギーに基づく全体尺度。細分化で単調減少し収束判定に使える。局所値は別物。")
    save(im, "ver11EnergyNorm")


# ============================================================
# ver-11-3d 収束次数 p (両対数の勾配)
# ============================================================
def ver11ConvOrder():
    im, d = new(); title(d, "収束次数 p:誤差-要素寸法の両対数勾配")
    ox, oy = 130, 320
    axes(d, ox, oy, 400, 240, "log h", "log e")
    ctext(d, ox + 200, oy + 26, "(要素寸法 h ・ 誤差 e の両対数)", FT, GRAY)
    # 直線(勾配 p)
    p1 = (ox + 90, oy - 60)    # h1, e1 (大きい h・大きい e)
    p2 = (ox + 320, oy - 200)  # h2=h1/2, e2
    d.line((p1[0], p1[1], p2[0], p2[1]), fill=BLUE, width=4)
    node(d, p1[0], p1[1], 6, fill=RED, col=RED)
    node(d, p2[0], p2[1], 6, fill=RED, col=RED)
    ctext(d, p1[0] - 6, p1[1] - 16, "(h1 , e1=4.0%)", FT, RED, "rm")
    ctext(d, p2[0] + 8, p2[1] - 12, "(h2=h1/2 , e2=1.0%)", FT, RED, "lm")
    # 勾配三角形
    dashed(d, p1[0], p1[1], p2[0], p1[1], GRAY, 2)
    dashed(d, p2[0], p1[1], p2[0], p2[1], GRAY, 2)
    ctext(d, (p1[0] + p2[0]) / 2, p1[1] + 16, "Δlog h", FT, GRAY)
    ctext(d, p2[0] + 14, (p1[1] + p2[1]) / 2, "Δlog e", FT, GRAY, "lm")
    box(d, 150, 350, 510, 388, FILL2)
    ctext(d, 330, 369, "e ∝ h^p  →  p = log(e1/e2) / log(h1/h2)", FT, BLACK)
    note(d, "2メッシュの誤差比と寸法比から勾配 p を求める。理論次数との差でコードを点検。")
    save(im, "ver11ConvOrder")


# ============================================================
# ver-11-4 開断面→スポット溶接で閉断面化・ねじり・ワーピング
# ============================================================
def ver11ThinTorsion():
    im, d = new(); title(d, "薄肉断面のねじり:開断面と閉断面(そり拘束)")
    # 左:開断面(C形)自由にそる=低ねじり剛性
    box(d, 40, 60, 320, 225, "white", 2, GRAY)
    ctext(d, 180, 78, "開断面(C形)", FS, BLACK)
    d.line((150, 105, 230, 105), fill=BLACK, width=5)
    d.line((150, 105, 150, 190), fill=BLACK, width=5)
    d.line((150, 190, 230, 190), fill=BLACK, width=5)
    angle_arc(d, 130, 147, 28, 200, 340, "T", RED)
    ctext(d, 180, 208, "そりを拘束せず→剛性低い", FT, RED)
    # 右:スポット溶接で閉断面化=そり拘束・高剛性
    box(d, 340, 60, 620, 225, "white", 2, GRAY)
    ctext(d, 480, 78, "スポット溶接で閉断面化", FS, BLACK)
    box(d, 440, 105, 540, 190, FILL1)
    for (yy) in (110, 150, 185):
        node(d, 440, yy, 4, fill=RED, col=RED)
    ctext(d, 560, 148, "溶接部", FT, RED, "lm")
    angle_arc(d, 490, 147, 34, 200, 340, "T", BLUE)
    ctext(d, 480, 208, "そり拘束→ほぼ閉断面・高剛性", FT, BLUE)
    box(d, 60, 250, 600, 322, FILL2)
    mlines(d, 330, 286,
           ["溶接でワーピング(そり)が拘束され断面はほぼ閉断面として働く",
            "→ はり理論のねじり剛性と比較する検証は妥当(要 十分な分割)"], FT, BLACK, 28)
    note(d, "スポット溶接でそりが拘束され閉断面的に働く。分割が十分ならはり理論値と照合できる。")
    save(im, "ver11ThinTorsion")


# ============================================================
# ver-11-4b アワーグラス(ゼロエネルギー)モードの点検
# ============================================================
def ver11Hourglass():
    im, d = new(); title(d, "次数低減積分とアワーグラスモードの点検")
    # 通常の要素と1点積分
    box(d, 60, 90, 200, 230, FILL1)
    node(d, 130, 160, 5, fill=RED, col=RED)
    ctext(d, 130, 250, "1点積分(中央)", FT, BLACK)
    ctext(d, 130, 274, "計算が軽い", FT, GRAY)
    arrow(d, 205, 160, 255, 160, BLACK, 3, 12)
    # アワーグラス変形(ひずみエネルギーを生まない砂時計形)
    hx, hy, s = 260, 90, 140
    # 変形前(破線)
    dashed(d, hx, hy, hx + s, hy, LGRAY, 2)
    dashed(d, hx, hy + s, hx + s, hy + s, LGRAY, 2)
    dashed(d, hx, hy, hx, hy + s, LGRAY, 2)
    dashed(d, hx + s, hy, hx + s, hy + s, LGRAY, 2)
    # 砂時計:上辺右へ・下辺左へ、側辺を内側にくびれ
    d.polygon([(hx + 22, hy), (hx + s + 22, hy), (hx + s - 22, hy + s), (hx - 22, hy + s)],
              outline=RED, width=3)
    ctext(d, hx + s / 2, hy + s + 22, "アワーグラス変形", FT, RED)
    ctext(d, hx + s / 2, hy + s + 46, "(ゼロエネルギーモード)", FT, RED)
    # エネルギー比バー
    box(d, 470, 95, 620, 300, "white", 2, GRAY)
    ctext(d, 545, 114, "エネルギー比", FT, BLACK)
    # 全ひずみエネルギー(大)
    d.rectangle((492, 150, 522, 285), outline=BLACK, width=2, fill=FILL3)
    ctext(d, 507, 300, "全ひずみE", FT, GRAY)
    # アワーグラスE(小=健全 / 大=疑い)
    d.rectangle((560, 250, 590, 285), outline=RED, width=2, fill=(255, 230, 230))
    ctext(d, 575, 300, "HG E", FT, RED)
    ctext(d, 545, 132, "HG/全 が数%超=疑い", FT, RED)
    note(d, "アワーグラスE/全ひずみEが大きい(目安数%超)ほど非物理的モードの混入を疑う。")
    save(im, "ver11Hourglass")


# ============================================================
# ver-11-6 荷重配置と最大変形量(単純支持はり)
# ============================================================
def ver11LoadArrange():
    im, d = new(); title(d, "総和が等しい荷重の配置と最大変形量")

    def beam(y, cap, defl_center):
        x0, x1 = 90, 570
        # 支点
        pin_support(d, x0, y, 14)
        roller_support(d, x1, y, 14)
        # たわみ曲線
        pts = []
        for i in range(0, 481, 8):
            t = i / 480.0
            w = defl_center * (16 * t * t * (1 - t) * (1 - t))
            pts.append((x0 + i, y + w))
        d.line(pts, fill=BLACK, width=3, joint="curve")
        dashed(d, x0, y, x1, y, LGRAY, 2)
        return x0, x1

    # (a) 中央集中
    y = 95
    x0, x1 = beam(y, "", 30)
    arrow(d, (x0 + x1) / 2, y - 34, (x0 + x1) / 2, y - 4, RED, 4, 12)
    ctext(d, 590, y, "中央1点集中", FT, RED, "lm")
    ctext(d, 300, y + 46, "δ = P L^3 / 48EI (最大)", FT, RED)
    # (b) 等分布
    y = 200
    x0, x1 = beam(y, "", 19)
    for xx in range(x0 + 10, x1, 40):
        arrow(d, xx, y - 30, xx, y - 4, BLUE, 2, 8)
    ctext(d, 590, y, "等分布", FT, BLUE, "lm")
    ctext(d, 300, y + 46, "δ = 5W L^3 / 384EI", FT, BLUE)
    # (c) 分散
    y = 305
    x0, x1 = beam(y, "", 14)
    for xx in (x0 + 120, x0 + 240, x0 + 360):
        arrow(d, xx, y - 30, xx, y - 4, GREEN, 3, 9)
    ctext(d, 590, y, "複数点に分散", FT, GREEN, "lm")
    ctext(d, 300, y + 46, "分散ほど小さい", FT, GREEN)
    note(d, "総荷重が同じでも中央1点集中が最大。分散させるほど最大変形量は小さくなる。")
    save(im, "ver11LoadArrange")


# ============================================================
# ver-11-7 曲げ応力最大位置=曲げモーメント最大=荷重点
# ============================================================
def ver11MomentPeak():
    im, d = new(); title(d, "曲げ応力が最大となる位置(単純支持・中央集中)")
    x0, x1, yb = 90, 570, 150
    # はり
    d.line((x0, yb, x1, yb), fill=BLACK, width=5)
    pin_support(d, x0, yb, 16)
    roller_support(d, x1, yb, 16)
    cx = (x0 + x1) / 2
    arrow(d, cx, yb - 44, cx, yb - 6, RED, 4, 13)
    ctext(d, cx, yb - 58, "P (荷重点)", FT, RED)
    # 反力
    arrow(d, x0, yb + 40, x0, yb + 8, GRAY, 3, 10)
    arrow(d, x1, yb + 40, x1, yb + 8, GRAY, 3, 10)
    ctext(d, x0, yb + 54, "R", FT, GRAY)
    ctext(d, x1, yb + 54, "R", FT, GRAY)
    # 曲げモーメント図(三角形・荷重点でピーク)
    my = 300
    d.line((x0, my, x1, my), fill=BLACK, width=2)
    d.polygon([(x0, my), (cx, my + 60), (x1, my)], outline=BLUE, width=3, fill=(232, 238, 250))
    ctext(d, cx, my + 76, "曲げモーメント図(荷重点で最大)", FT, BLUE)
    ctext(d, 610, my, "M", FT, BLUE, "lm")
    box(d, 250, 92, 470, 120, None, 2, GRAY)
    ctext(d, 360, 106, "σ = M / Z  ∝ M", FT, BLACK)
    note(d, "曲げ応力 σ=M/Z はモーメントに比例。中央集中では荷重点でモーメント最大→応力最大。")
    save(im, "ver11MomentPeak")


# ============================================================
# ver-11-11 反力の合力=外荷重の合力に等しく逆向き(釣合い)
# ============================================================
def ver11ReactSum():
    im, d = new(); title(d, "反力の合力による釣合い検証")
    # 平板
    box(d, 200, 120, 460, 250, FILL1)
    ctext(d, 330, 185, "面内荷重を受ける平板", FT, GRAY)
    # 外荷重(上向き横向き:ここでは右向き面内荷重)
    for yy in (150, 185, 220):
        arrow(d, 150, yy, 200, yy, RED, 3, 12)
    ctext(d, 120, 140, "外荷重", FT, RED)
    ctext(d, 120, 165, "合力 ΣF", FT, RED)
    # 下端拘束(壁)+反力
    hwall(d, 200, 460, 250, side=1, n=10)
    for xx in (240, 330, 420):
        arrow(d, xx, 300, xx, 258, BLUE, 3, 12)
    ctext(d, 330, 318, "拘束点の反力(合力 ΣR)", FT, BLUE)
    box(d, 120, 340, 540, 388, FILL2)
    ctext(d, 330, 364, "ΣR = -ΣF  (大きさ等しく向き逆)  →  不一致なら入力誤り", FT, BLACK)
    note(d, "拘束点反力の合計は外荷重の合力と大きさが等しく向きが逆。一致しなければ入力に誤り。")
    save(im, "ver11ReactSum")


# ============================================================
# ver-11-12 一貫単位系 mm-N-MPa → 応力 MPa
# ============================================================
def ver11UnitMMN():
    im, d = new(); title(d, "一貫単位系(mm・N・MPa)での応力の単位")
    rows = [("長さ", "mm"), ("縦弾性係数 E", "MPa = N/mm^2"), ("荷重", "N")]
    y = 90
    for name, unit in rows:
        box(d, 90, y, 330, y + 52, FILL1)
        ctext(d, 210, y + 26, name, FT, BLACK)
        box(d, 330, y, 570, y + 52, FILL2)
        ctext(d, 450, y + 26, unit, FT, BLUE)
        y += 60
    arrow(d, 330, y + 20, 330, y + 44, BLACK, 3, 12)
    box(d, 150, y + 50, 510, y + 100, "white", 3, RED)
    mlines(d, 330, y + 75,
           ["応力 = 力 / 面積 = N / mm^2", "→ 応力の単位は MPa (N/mm^2)"], FT, RED, 24)
    note(d, "mm・N・MPa は互いに整合する一貫単位系。応力=力/面積=N/mm^2=MPa で出力される。")
    save(im, "ver11UnitMMN")


# ============================================================
# ver-11-13 SI一貫単位系 → 密度 kg/m^3
# ============================================================
def ver11UnitSI():
    im, d = new(); title(d, "SI一貫単位系での質量密度の単位")
    box(d, 80, 80, 580, 150, FILL2)
    ctext(d, 330, 104, "長さ m ・ 縦弾性係数 Pa(N/m^2) ・ 力 N", FT, BLACK)
    ctext(d, 330, 132, "N = kg・m / s^2", FS, BLUE)
    # 慣性力の次元チェック
    box(d, 80, 175, 580, 275, FILL1)
    ctext(d, 330, 200, "慣性力 = 質量密度 × 体積 × 加速度", FT, BLACK)
    ctext(d, 330, 236,
          "[kg/m^3] × [m^3] × [m/s^2] = [kg・m/s^2] = [N]", FT, GREEN)
    box(d, 180, 300, 480, 350, "white", 3, RED)
    ctext(d, 330, 325, "質量密度 → kg/m^3", FS, RED)
    note(d, "力を N にするには質量密度は kg/m^3。N/m^3 は重量密度、g/cm^3 は別単位系。")
    save(im, "ver11UnitSI")


# ============================================================
# ver-11-14 応力はEに依存しない(荷重制御・単一材料)
# ============================================================
def ver11StressEindep():
    im, d = new(); title(d, "荷重制御の線形弾性:応力は E に依存しない")
    # 棒に力F
    wall(d, 90, 120, 200, side=1, n=4)
    d.rectangle((90, 140, 420, 180), outline=BLACK, width=3, fill=FILL1)
    force(d, 420, 160, 55, 0, "F", RED)
    dim(d, 90, 205, 420, 205, "断面積 A", col=GRAY)
    box(d, 90, 240, 350, 320, FILL1)
    mlines(d, 220, 280, ["応力 σ = F / A", "→ E を含まない"], FS, BLACK, 30)
    box(d, 370, 240, 590, 320, FILL2)
    mlines(d, 480, 280, ["ひずみ ε = σ / E", "変位 ∝ 1/E"], FS, BLUE, 30)
    ctext(d, 330, 350, "E を間違えても応力は不変。変位だけが E 比でずれる", FT, RED)
    note(d, "単一材料・力制御では応力=F/A で E に無関係。間違ったEでも応力はそのまま使える。")
    save(im, "ver11StressEindep")


# ============================================================
# ver-11-15 単位不統一(mm/GPa/MPa):応力は換算で復元・ひずみは不整合
# ============================================================
def ver11UnitMismatch():
    im, d = new(); title(d, "単位不統一(mm・GPa・MPa)の結果の扱い")
    # 応力(荷重に比例)は換算で復元可
    box(d, 55, 80, 320, 320, FILL1, col=GREEN)
    ctext(d, 187, 106, "応力", FS, GREEN)
    mlines(d, 187, 200,
           ["応力 ∝ 荷重(圧力)", "E の値によらず決まる", "→ 単位を正しく換算すれば", "正しい応力が得られる"],
           FT, BLACK, 30)
    # ひずみ・変位はE単位不整合でNG
    box(d, 340, 80, 605, 320, FILL2, col=RED)
    ctext(d, 472, 106, "ひずみ・変位", FS, RED)
    mlines(d, 472, 200,
           ["ε = σ / E", "E(GPa)と σ(MPa)が不整合", "→ そのままでは", "正しくならない"],
           FT, BLACK, 30)
    ctext(d, 330, 345, "応力=荷重に比例して復元可 / ひずみ・変位=E単位不整合で要注意", FT, GRAY)
    note(d, "内圧応力は荷重に比例し換算で復元可。ひずみ・変位はEの単位不整合により正しくならない。")
    save(im, "ver11UnitMismatch")


# ============================================================
# ver-11-17 検証(Verification)と妥当性確認(Validation)
# ============================================================
def ver11VerifValid():
    im, d = new(); title(d, "検証(Verification)と妥当性確認(Validation)")
    # 検証
    box(d, 45, 75, 320, 310, FILL1, col=BLUE)
    ctext(d, 182, 100, "検証 Verification", FS, BLUE)
    ctext(d, 182, 126, "「数式を正しく解けているか」", FT, BLACK)
    box(d, 70, 150, 295, 200, "white", 2, GRAY)
    ctext(d, 182, 175, "シミュレーション結果", FT, BLACK)
    dashed(d, 182, 202, 182, 230, GRAY, 2)
    box(d, 70, 232, 295, 282, "white", 2, BLUE)
    ctext(d, 182, 257, "既知の理論解 と比較", FT, BLUE)
    # 妥当性確認
    box(d, 340, 75, 615, 310, FILL2, col=RED)
    ctext(d, 477, 100, "妥当性確認 Validation", FS, RED)
    ctext(d, 477, 126, "「モデル化そのものが妥当か」", FT, BLACK)
    box(d, 365, 150, 590, 200, "white", 2, GRAY)
    ctext(d, 477, 175, "シミュレーション結果", FT, BLACK)
    dashed(d, 477, 202, 477, 230, GRAY, 2)
    box(d, 365, 232, 590, 282, "white", 2, RED)
    ctext(d, 477, 257, "実験結果 と比較", FT, RED)
    ctext(d, 330, 332, "理論解との一致=検証 / 実験との一致=妥当性確認", FT, GRAY)
    note(d, "数学的に正しく解けたかが検証(理論解比較)、現象を表せるかが妥当性確認(実験比較)。")
    save(im, "ver11VerifValid")


ALL = [ver11SingularSpots, ver11PlateDefl, ver11EnergyNorm, ver11ConvOrder,
       ver11ThinTorsion, ver11Hourglass, ver11LoadArrange, ver11MomentPeak,
       ver11ReactSum, ver11UnitMMN, ver11UnitSI, ver11StressEindep,
       ver11UnitMismatch, ver11VerifValid]

KEYS = ["ver11SingularSpots", "ver11PlateDefl", "ver11EnergyNorm", "ver11ConvOrder",
        "ver11ThinTorsion", "ver11Hourglass", "ver11LoadArrange", "ver11MomentPeak",
        "ver11ReactSum", "ver11UnitMMN", "ver11UnitSI", "ver11StressEindep",
        "ver11UnitMismatch", "ver11VerifValid"]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    miss = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(KEYS), "MISSING", miss)
