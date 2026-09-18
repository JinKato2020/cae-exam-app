# -*- coding: utf-8 -*-
"""熱流体2級 第3章「熱力学・伝熱」問題図(t2e3*)。19枚。
白地660x420・線画・機構/設定のみ。豆腐回避のためギリシャ文字/特殊記号はローマ字・通常表記に置換。
required 種別は答え・結論・数値を描かず設定のみ。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


# 1 t2e3HeatWorkEquiv / helpful : 1 kcal ≒ 4.2 kJ 等価をエネルギー棒2本で対比
def heat_work_equiv():
    im, d = new()
    title(d, "熱と仕事は等価: 1 kcal ≒ 4.2 kJ")
    baseY = 340
    # 左: 熱の棒
    hx = 190; bw = 90; hh = 210
    d.rectangle((hx - bw / 2, baseY - hh, hx + bw / 2, baseY), outline=BLACK, width=3, fill=FILL1)
    ctext(d, hx, baseY - hh - 22, "熱 Q", F, BLACK)
    ctext(d, hx, baseY + 22, "1 kcal", FS, BLACK)
    # 右: 仕事の棒 (同じ高さ=等価)
    wx = 470
    d.rectangle((wx - bw / 2, baseY - hh, wx + bw / 2, baseY), outline=BLACK, width=3, fill=FILL2)
    ctext(d, wx, baseY - hh - 22, "仕事 W", F, BLACK)
    ctext(d, wx, baseY + 22, "4.2 kJ", FS, BLACK)
    # 等価の双方向矢印
    arrow(d, hx + bw / 2 + 12, baseY - hh / 2, wx - bw / 2 - 12, baseY - hh / 2, GREEN, 3, 14)
    arrow(d, wx - bw / 2 - 12, baseY - hh / 2 + 30, hx + bw / 2 + 12, baseY - hh / 2 + 30, GREEN, 3, 14)
    ctext(d, (hx + wx) / 2, baseY - hh / 2 - 20, "同じエネルギー量", FT, GREEN)
    hwall(d, 100, 560, baseY, 1, 12)
    note(d, "熱と仕事はどちらもエネルギーで相互に換算できる(熱の仕事当量)")
    save(im, "t2e3HeatWorkEquiv")


# 2 t2e3IdealGasEq / helpful : pV=mRT を V で割ると p=rho R T になる式変形
def ideal_gas_eq():
    im, d = new()
    title(d, "状態方程式: pV = mRT を V で割ると p = rho R T")
    # 上の式ボックス
    d.rectangle((200, 110, 460, 170), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 140, "pV = mRT", F, BLACK)
    # 変形矢印
    arrow(d, 330, 175, 330, 245, BLACK, 3, 14)
    ctext(d, 380, 210, "両辺を V で割る", FT, GRAY, "lm")
    # 中間: p = (m/V) R T
    d.rectangle((175, 250, 485, 310), outline=BLACK, width=2, fill=FILL2)
    ctext(d, 330, 280, "p = (m / V) R T", F, BLACK)
    # rho = m/V の置換
    arrow(d, 330, 315, 330, 355, BLACK, 3, 14)
    ctext(d, 380, 335, "rho = m / V (密度)", FT, GRAY, "lm")
    d.rectangle((215, 360, 445, 405), outline=GREEN, width=3, fill=FILL1)
    ctext(d, 330, 382, "p = rho R T", F, GREEN)
    save(im, "t2e3IdealGasEq")


# 3 t2e3FirstLaw / helpful : 第0〜第3法則 対応表 + 第1法則 Q=deltaU+W を強調
def first_law():
    im, d = new()
    title(d, "熱力学の法則と 第1法則 Q = deltaU + W")
    rows = [
        ("第0法則", "温度が等しい = 熱平衡"),
        ("第1法則", "エネルギー保存  Q = deltaU + W"),
        ("第2法則", "エントロピーは増大する"),
        ("第3法則", "絶対零度でエントロピー最小"),
    ]
    x0, y0, w1, w2, rh = 70, 90, 150, 400, 70
    for i, (a, b) in enumerate(rows):
        y = y0 + i * rh
        hl = (i == 1)
        fillcol = FILL1 if hl else "white"
        d.rectangle((x0, y, x0 + w1, y + rh), outline=BLACK, width=2, fill=fillcol)
        d.rectangle((x0 + w1, y, x0 + w1 + w2, y + rh), outline=BLACK, width=2, fill=fillcol)
        col = GREEN if hl else BLACK
        ctext(d, x0 + w1 / 2, y + rh / 2, a, FS, col)
        ctext(d, x0 + w1 + w2 / 2, y + rh / 2, b, FS, col)
    # 強調枠
    d.rectangle((x0 - 3, y0 + rh - 3, x0 + w1 + w2 + 3, y0 + 2 * rh + 3), outline=GREEN, width=4)
    note(d, "Q=系に加えた熱, deltaU=内部エネルギー変化, W=系が外部にした仕事")
    save(im, "t2e3FirstLaw")


# 4 t2e3SecondLaw / helpful : 可逆 deltaS=Q/T, 不可逆 deltaS>Q/T を第2法則に位置づけ
def second_law():
    im, d = new()
    title(d, "第2法則: エントロピー変化 deltaS")
    # 上部: 第2法則の枠
    d.rectangle((150, 80, 510, 130), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 105, "第2法則: deltaS >= Q / T", F, BLACK)
    arrow(d, 250, 135, 170, 195, GRAY, 2, 11)
    arrow(d, 410, 135, 490, 195, GRAY, 2, 11)
    # 左: 可逆
    d.rectangle((60, 200, 320, 330), outline=GREEN, width=3, fill="white")
    ctext(d, 190, 230, "可逆過程", FS, GREEN)
    ctext(d, 190, 275, "deltaS = Q / T", F, GREEN)
    ctext(d, 190, 310, "(等号が成立)", FT, GRAY)
    # 右: 不可逆
    d.rectangle((340, 200, 600, 330), outline=BLACK, width=3, fill="white")
    ctext(d, 470, 230, "不可逆過程", FS, BLACK)
    ctext(d, 470, 275, "deltaS > Q / T", F, BLACK)
    ctext(d, 470, 310, "(不等号)", FT, GRAY)
    note(d, "実際の変化はすべて不可逆で、全体のエントロピーは増える")
    save(im, "t2e3SecondLaw")


# 5 t2e3Enthalpy / helpful : H = U + pV を U の上に pV を積む概念図
def enthalpy():
    im, d = new()
    title(d, "エンタルピー H = U + pV")
    cx = 250; bw = 150; baseY = 360
    uh = 150; ph = 90
    # 下: 内部エネルギー U
    d.rectangle((cx - bw / 2, baseY - uh, cx + bw / 2, baseY), outline=BLACK, width=3, fill=FILL1)
    ctext(d, cx, baseY - uh / 2, "U", FL, BLACK)
    ctext(d, cx, baseY + 20, "内部エネルギー", FT, GRAY)
    # 上: pV を積む
    d.rectangle((cx - bw / 2, baseY - uh - ph, cx + bw / 2, baseY - uh), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, baseY - uh - ph / 2, "pV", FL, BLACK)
    ctext(d, cx, baseY - uh - ph - 18, "流動仕事", FT, GRAY)
    # = H を右に
    arrow(d, cx + bw / 2 + 20, baseY - (uh + ph) / 2, cx + bw / 2 + 90, baseY - (uh + ph) / 2, BLACK, 3, 14)
    d.rectangle((470, baseY - uh - ph, 470 + 110, baseY), outline=GREEN, width=3, fill=FILL1)
    ctext(d, 525, baseY - (uh + ph) / 2, "H", FL, GREEN)
    ctext(d, 525, baseY + 20, "エンタルピー", FT, GREEN)
    save(im, "t2e3Enthalpy")


# 6 t2e3HeatEngine / required : 高温熱源→サイクル→低温熱源, Q1流入/W外部/Q2流出ブロック図
def heat_engine():
    im, d = new()
    title(d, "熱機関: 高温熱源 → サイクル → 低温熱源")
    # 高温熱源(上)
    d.rectangle((190, 70, 470, 130), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 100, "高温熱源 (温度 T1)", FS, BLACK)
    # サイクル(中央 円)
    cx, cy, r = 330, 250, 62
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill="white")
    ctext(d, cx, cy, "サイクル", FS, BLACK)
    # 低温熱源(下)
    d.rectangle((190, 350, 470, 405), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 377, "低温熱源 (温度 T2)", FS, BLACK)
    # Q1 流入
    arrow(d, 330, 132, 330, cy - r - 4, BLACK, 4, 15)
    ctext(d, 350, (132 + cy - r) / 2, "Q1 流入", FT, BLACK, "lm")
    # Q2 流出
    arrow(d, 330, cy + r + 4, 330, 348, BLACK, 4, 15)
    ctext(d, 350, (cy + r + 348) / 2, "Q2 流出", FT, BLACK, "lm")
    # W 外部仕事
    arrow(d, cx + r + 4, cy, 560, cy, GREEN, 4, 15)
    ctext(d, 545, cy - 20, "W 外部仕事", FT, GREEN, "mm")
    note(d, "高温から Q1 を受け、W を取り出し、残り Q2 を低温へ捨てる")
    save(im, "t2e3HeatEngine")


# 7 t2e3Adiabatic / helpful : p-V線図に等温線と断熱線, 断熱線の方が急
def adiabatic():
    im, d = new()
    title(d, "p-V 線図: 断熱線は等温線より急")
    ox, oy = 110, 350; xl, yl = 460, 260
    axes(d, ox, oy, xl, yl, "体積 V", "圧力 p")
    # 共通の起点
    V0 = 0.30
    def curve(gamma, col, wd):
        pts = []
        for i in range(0, 101):
            t = 0.30 + i / 100 * 0.62
            p = (V0 ** gamma) / (t ** gamma)
            pts.append((ox + t * xl, oy - p * yl * 0.82))
        plot(d, 0, 0, pts, col, wd)
        return pts
    iso = curve(1.0, GRAY, 3)      # 等温 pV=const
    adi = curve(1.4, GREEN, 3)     # 断熱 pV^gamma=const (急)
    ctext(d, iso[35][0] + 40, iso[35][1] + 6, "等温線 (pV=一定)", FT, GRAY, "lm")
    ctext(d, adi[18][0] + 14, adi[18][1] - 12, "断熱線 (pV^gamma=一定)", FT, GREEN, "lm")
    note(d, "同じ点から膨張すると断熱線の方が急に圧力が下がる")
    save(im, "t2e3Adiabatic")


# 8 t2e3SoundSpeed / required : 気体中を圧力波が速度 a で伝わる。与件 gamma,R,T をラベル
def sound_speed():
    im, d = new()
    title(d, "気体中を伝わる圧力波 (速度 a)")
    # 管
    x0, x1, yc, hh = 90, 570, 230, 70
    d.rectangle((x0, yc - hh, x1, yc + hh), outline=BLACK, width=3, fill="white")
    ctext(d, (x0 + x1) / 2, yc - hh - 20, "気体で満たされた管", FT, GRAY)
    # 圧力波(数本の縦線・右へ密になる波面)
    for i, xx in enumerate([220, 250, 285, 325]):
        w = 3 if i == 3 else 2
        col = GREEN if i == 3 else GRAY
        d.line((xx, yc - hh + 8, xx, yc + hh - 8), fill=col, width=w)
    ctext(d, 272, yc + hh + 22, "圧力波(波面)", FT, GRAY)
    # 伝播方向 a
    arrow(d, 340, yc, 500, yc, GREEN, 4, 15)
    ctext(d, 470, yc - 22, "速度 a", FS, GREEN)
    # 与件ラベル
    ctext(d, 150, yc, "gamma, R, T", FS, BLACK)
    note(d, "与件: 比熱比 gamma・気体定数 R・絶対温度 T")
    save(im, "t2e3SoundSpeed")


# 9 t2e3IsothermPV / helpful : p-V 上で 等温(双曲線)・等圧(水平)・等積(垂直)
def isotherm_pv():
    im, d = new()
    title(d, "p-V 線図: 等温・等圧・等積 の描き分け")
    ox, oy = 110, 350; xl, yl = 460, 260
    axes(d, ox, oy, xl, yl, "体積 V", "圧力 p")
    # 等温 双曲線
    pts = []
    for i in range(0, 101):
        t = 0.22 + i / 100 * 0.70
        pts.append((ox + t * xl, oy - (0.20 / t) * yl))
    plot(d, 0, 0, pts, GREEN, 3)
    ctext(d, pts[70][0] + 30, pts[70][1], "等温(双曲線)", FT, GREEN, "lm")
    # 等圧 水平
    py = oy - 0.72 * yl
    d.line((ox + 0.15 * xl, py, ox + 0.9 * xl, py), fill=BLUE, width=3)
    ctext(d, ox + 0.9 * xl + 8, py, "等圧(水平)", FT, BLUE, "lm")
    # 等積 垂直
    pxv = ox + 0.32 * xl
    d.line((pxv, oy - 0.12 * yl, pxv, oy - 0.92 * yl), fill=RED, width=3)
    ctext(d, pxv, oy - 0.92 * yl - 14, "等積(垂直)", FT, RED)
    save(im, "t2e3IsothermPV")


# 10 t2e3CycleWork / helpful : 閉サイクル内部面積 = 正味仕事
def cycle_work():
    im, d = new()
    title(d, "閉サイクルの囲む面積 = 正味仕事")
    ox, oy = 110, 350; xl, yl = 460, 260
    axes(d, ox, oy, xl, yl, "体積 V", "圧力 p")
    # 閉ループ(楕円状)
    cx, cy, rx, ry = ox + 0.5 * xl, oy - 0.5 * yl, 0.28 * xl, 0.30 * yl
    loop = []
    for i in range(0, 361, 6):
        a = math.radians(i)
        loop.append((cx + rx * math.cos(a), cy - ry * math.sin(a)))
    # 内部を薄く塗る
    d.polygon(loop, fill=FILL1, outline=None)
    d.line(loop + [loop[0]], fill=GREEN, width=3, joint="curve")
    # 進行方向(時計回り=正の仕事)
    arrow(d, cx + rx * 0.7, cy - ry * 0.72, cx + rx * 0.95, cy - ry * 0.2, GREEN, 3, 12)
    ctext(d, cx, cy, "面積 = 正味仕事 W", FS, BLACK)
    note(d, "閉サイクルが p-V 面上で囲む面積が1周の正味仕事を表す")
    save(im, "t2e3CycleWork")


# 11 t2e3Conduction / required : 厚さ L の平板, 高温Th/低温Tc, 1 m2 一次元定常熱伝導
def conduction():
    im, d = new()
    title(d, "平板の一次元定常熱伝導 (通過面 1 m2)")
    # 平板
    x0, x1, y0, y1 = 240, 420, 100, 340
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2, "平板", FS, GRAY)
    # 厚さ L
    dim(d, x0, y1 + 40, x1, y1 + 40, "厚さ L", 0, GRAY)
    # 面積 1 m2
    ctext(d, (x0 + x1) / 2, y0 - 22, "通過面 1 m2", FT, GRAY)
    # 高温 Th (左面)
    wall(d, x0, y0, y1, -1, 10)
    ctext(d, x0 - 60, (y0 + y1) / 2, "高温 Th", FS, RED, "mm")
    # 低温 Tc (右面)
    wall(d, x1, y0, y1, 1, 10)
    ctext(d, x1 + 62, (y0 + y1) / 2, "低温 Tc", FS, BLUE, "mm")
    # 熱流れ矢印(高温→低温)
    for yy in (y0 + 60, (y0 + y1) / 2, y1 - 60):
        arrow(d, x0 + 30, yy, x1 - 30, yy, GRAY, 2, 10)
    ctext(d, (x0 + x1) / 2, y1 + 70, "熱は高温側から低温側へ流れる", FT, GRAY)
    save(im, "t2e3Conduction")


# 12 t2e3Conductivity / helpful : 各材料の熱伝導率を対数棒グラフで高い順
def conductivity():
    im, d = new()
    title(d, "熱伝導率 (対数目盛・高い順)  W/(m K)")
    mats = [("銀", 420), ("アルミ", 236), ("鉄", 80), ("ガラス", 1.0), ("水", 0.6), ("空気", 0.026)]
    x0 = 150; y0 = 80; rh = 48; maxw = 400
    lo, hi = -1.7, 2.7   # log10 範囲
    for i, (nm, v) in enumerate(mats):
        y = y0 + i * rh
        lv = math.log10(v)
        w = (lv - lo) / (hi - lo) * maxw
        d.rectangle((x0, y, x0 + w, y + rh - 14), outline=BLACK, width=2, fill=FILL1)
        ctext(d, x0 - 10, y + (rh - 14) / 2, nm, FS, BLACK, "rm")
        ctext(d, x0 + w + 8, y + (rh - 14) / 2, str(v), FT, GRAY, "lm")
    note(d, "金属は大きく、気体は極端に小さい(対数目盛で表示)")
    save(im, "t2e3Conductivity")


# 13 t2e3Prandtl / helpful : Re,Pr,Nu,Gr 定義表。Pr = nu/a を明示
def prandtl():
    im, d = new()
    title(d, "無次元数の定義: Re, Pr, Nu, Gr")
    rows = [
        ("Re", "レイノルズ数 = 慣性力 / 粘性力"),
        ("Pr", "プラントル数 = nu / a (動粘性率/熱拡散率)"),
        ("Nu", "ヌセルト数 = 対流熱伝達 / 熱伝導"),
        ("Gr", "グラスホフ数 = 浮力 / 粘性力"),
    ]
    x0, y0, w1, w2, rh = 70, 90, 110, 440, 70
    for i, (a, b) in enumerate(rows):
        y = y0 + i * rh
        hl = (i == 1)
        fillcol = FILL1 if hl else "white"
        d.rectangle((x0, y, x0 + w1, y + rh), outline=BLACK, width=2, fill=fillcol)
        d.rectangle((x0 + w1, y, x0 + w1 + w2, y + rh), outline=BLACK, width=2, fill=fillcol)
        col = GREEN if hl else BLACK
        ctext(d, x0 + w1 / 2, y + rh / 2, a, FS, col)
        ctext(d, x0 + w1 + w2 / 2, y + rh / 2, b, FT, col)
    d.rectangle((x0 - 3, y0 + rh - 3, x0 + w1 + w2 + 3, y0 + 2 * rh + 3), outline=GREEN, width=4)
    note(d, "Pr は流体そのものの性質で決まる無次元数")
    save(im, "t2e3Prandtl")


# 14 t2e3MercuryPr / helpful : 各流体の Pr を対数目盛, 水銀が極端に小さい
def mercury_pr():
    im, d = new()
    title(d, "各流体のプラントル数 Pr (対数目盛)")
    fluids = [("水銀", 0.025), ("空気", 0.71), ("水", 7.0), ("油", 100.0)]
    x0 = 160; y0 = 100; rh = 62; maxw = 380
    lo, hi = -1.8, 2.2
    for i, (nm, v) in enumerate(fluids):
        y = y0 + i * rh
        lv = math.log10(v)
        w = (lv - lo) / (hi - lo) * maxw
        col = GREEN if i == 0 else FILL1
        d.rectangle((x0, y, x0 + w, y + rh - 18), outline=BLACK, width=2, fill=col)
        ctext(d, x0 - 10, y + (rh - 18) / 2, nm, FS, BLACK, "rm")
        ctext(d, x0 + w + 8, y + (rh - 18) / 2, "Pr ≒ " + str(v), FT, GRAY, "lm")
    ctext(d, x0 + 170, y0 + (rh - 18) / 2, "← 極端に小さい", FT, GREEN, "lm")
    note(d, "液体金属の水銀は Pr が極端に小さい(熱が伝わりやすい)")
    save(im, "t2e3MercuryPr")


# 15 t2e3Convection / required : 壁温 Tw > 主流温 T の壁沿い流れと壁→流体の熱伝達。与件 h
def convection():
    im, d = new()
    title(d, "壁面まわりの対流熱伝達 (壁温 Tw > 主流温 T)")
    # 壁(下)
    wy = 340
    hwall(d, 90, 570, wy, -1, 12)
    ctext(d, 320, wy + 26, "壁 (温度 Tw)", FS, RED)
    # 主流(壁に沿う流れ)
    for i, yy in enumerate([120, 170, 220]):
        arrow(d, 110, yy, 470, yy, GRAY, 2, 11)
    ctext(d, 500, 170, "主流 (温度 T)", FT, GRAY, "lm")
    # 壁→流体への熱伝達(上向き矢印)
    for xx in (200, 300, 400):
        arrow(d, xx, wy - 6, xx, 250, GREEN, 3, 12)
    ctext(d, 300, 285, "壁 → 流体 へ熱が伝わる", FT, GREEN)
    # 与件 h
    ctext(d, 150, wy - 40, "熱伝達率 h", FS, BLACK, "lm")
    note(d, "与件: 熱伝達率 h。壁温が主流温より高いと壁から流体へ熱が移る")
    save(im, "t2e3Convection")


# 16 t2e3BoundaryLayer / helpful : 速度境界層と温度境界層, Pr>1薄い/Pr<1厚い/Pr≈1一致
def boundary_layer():
    im, d = new()
    title(d, "速度境界層と温度境界層 (Pr による厚みの違い)")
    def panel(ox, oy, xl, thermal_ratio, label):
        wy = oy
        hwall(d, ox, ox + xl, wy, -1, 7)
        # 速度境界層(共通・青)
        vel = []
        for i in range(0, 51):
            t = i / 50
            vel.append((ox + t * xl, wy - 55 * math.sqrt(t)))
        plot(d, 0, 0, vel, BLUE, 2)
        # 温度境界層(赤・比率で厚み変化)
        thm = []
        for i in range(0, 51):
            t = i / 50
            thm.append((ox + t * xl, wy - 55 * thermal_ratio * math.sqrt(t)))
        plot(d, 0, 0, thm, RED, 2)
        ctext(d, ox + xl / 2, wy + 22, label, FT, BLACK)
    panel(70, 150, 150, 0.6, "Pr>1: 温度層 薄い")
    panel(255, 150, 150, 1.6, "Pr<1: 温度層 厚い")
    panel(440, 150, 150, 1.0, "Pr≒1: 一致")
    # 凡例
    d.line((120, 340, 160, 340), fill=BLUE, width=3); ctext(d, 168, 340, "速度境界層", FT, BLUE, "lm")
    d.line((330, 340, 370, 340), fill=RED, width=3); ctext(d, 378, 340, "温度境界層", FT, RED, "lm")
    note(d, "Pr>1 で温度境界層は速度境界層より薄く、Pr<1 で厚くなる")
    save(im, "t2e3BoundaryLayer")


# 17 t2e3Boussinesq / required : 加熱鉛直平板の自然対流。座標(x上/g下), 与件 T-T0, beta
def boussinesq():
    im, d = new()
    title(d, "加熱された鉛直平板まわりの自然対流")
    # 鉛直平板(左)
    px = 200
    d.rectangle((px - 16, 90, px, 360), outline=BLACK, width=3, fill=FILL1)
    ctext(d, px - 8, 75, "加熱平板", FT, RED)
    # 座標: x 上向き
    arrow(d, 120, 340, 120, 110, BLACK, 2, 11)
    ctext(d, 120, 96, "x (上)", FT, BLACK)
    # 重力 g 下向き
    arrow(d, 90, 150, 90, 340, GRAY, 3, 13)
    ctext(d, 78, 250, "g (下)", FT, GRAY, "rm")
    # 上昇する自然対流(平板沿いに上向きの流れ)
    for yy in (330, 280, 230, 180):
        arrow(d, px + 40, yy, px + 40, yy - 40, GREEN, 2, 10)
    ctext(d, px + 90, 250, "浮力で上昇する流れ", FT, GREEN, "lm")
    # 与件ラベル
    ctext(d, px + 120, 150, "与件: T - T0", FS, BLACK, "lm")
    ctext(d, px + 120, 185, "体膨張率 beta", FS, BLACK, "lm")
    note(d, "壁が周囲より高温だと密度差で浮力が生じ、流れが自然に立ち上がる")
    save(im, "t2e3Boussinesq")


# 18 t2e3ConvMap / helpful : 横軸Ra・縦軸Re に 強制/自然/複合対流 の領域分類
def conv_map():
    im, d = new()
    title(d, "対流の領域分類 (横軸 Ra ・ 縦軸 Re)")
    ox, oy = 120, 350; xl, yl = 440, 260
    axes(d, ox, oy, xl, yl, "Ra", "Re")
    # 対角の境界帯(複合対流)
    dashed(d, ox, oy - yl, ox + xl, oy, GRAY, 2, 10, 6)
    dashed(d, ox + 0.35 * xl, oy - yl, ox + xl, oy - 0.35 * yl, GRAY, 2, 10, 6)
    # 領域ラベル
    ctext(d, ox + 0.22 * xl, oy - 0.78 * yl, "強制対流\n(Re 大)", FT, BLUE)
    ctext(d, ox + 0.78 * xl, oy - 0.22 * yl, "自然対流\n(Ra 大)", FT, RED)
    ctext(d, ox + 0.55 * xl, oy - 0.55 * yl, "複合対流", FT, GREEN)
    note(d, "Re が大きければ強制対流、Ra が大きければ自然対流、中間は複合対流")
    save(im, "t2e3ConvMap")


# 19 t2e3NusseltRe / helpful : 両対数で Nu=0.023 Re^0.8 Pr^0.4 が直線・Nu が Re とともに増加
def nusselt_re():
    im, d = new()
    title(d, "両対数グラフ: Nu は Re とともに増加(直線)")
    ox, oy = 120, 350; xl, yl = 440, 260
    axes(d, ox, oy, xl, yl, "log Re", "log Nu")
    # 直線(傾き 0.8)
    x1, y1 = ox + 0.08 * xl, oy - 0.15 * yl
    x2, y2 = ox + 0.92 * xl, oy - 0.90 * yl
    d.line((x1, y1, x2, y2), fill=GREEN, width=3)
    ctext(d, (x1 + x2) / 2 + 20, (y1 + y2) / 2 - 20, "Nu = 0.023 Re^0.8 Pr^0.4", FT, GREEN, "lm")
    # 傾きの目印
    ctext(d, x2 - 10, y2 - 18, "傾き 0.8", FT, GRAY, "rm")
    note(d, "両対数では乗数の関係が直線になり、Re が増えると Nu も増える")
    save(im, "t2e3NusseltRe")


if __name__ == "__main__":
    heat_work_equiv(); ideal_gas_eq(); first_law(); second_law(); enthalpy()
    heat_engine(); adiabatic(); sound_speed(); isotherm_pv(); cycle_work()
    conduction(); conductivity(); prandtl(); mercury_pr(); convection()
    boundary_layer(); boussinesq(); conv_map(); nusselt_re()
    print("done t2 ch3: 19 figs")
