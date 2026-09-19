# -*- coding: utf-8 -*-
"""熱流体力学1級 第20章「層流予混合火炎」の問題図(t1e20*)を描画。
白地660x420・黒線画・機構/構造/座標系/プロファイルのみ・数値や答えは書かない。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(Su, phi, Le, K, delta, rho, Tu, Tb, eta, theta 等)。"""
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


# S字状温度分布(Tu->Tb)を返す共通関数(ピクセル点列)
def scurve_pts(ox, oy, xl, yl, ylo=0.10, yhi=0.86, x0=0.10, x1=0.55):
    """x0..x1 の区間で立ち上がるロジスティック状S字。左端Tu(低)右端Tb(高)。"""
    pts = []
    for i in range(0, 201):
        t = i / 200
        if t <= x0:
            v = ylo
        elif t >= x1:
            v = yhi
        else:
            s = (t - x0) / (x1 - x0)
            v = ylo + (yhi - ylo) * (0.5 - 0.5 * math.cos(math.pi * s))
        pts.append((ox + t * xl, oy - v * yl))
    return pts


# ============================================================
# ============  問題図  t1e20*  (13)  ========================
# ============================================================

# 20-1 t1e20FlameStructure : 火炎構造(予熱帯・反応帯)(required)
def flame_structure():
    im, d = new(); title(d, "層流予混合火炎の火炎構造(予熱帯と反応帯)")
    ox, oy, xl, yl = 100, 350, 470, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "x", FS, BLACK, "lm")
    ctext(d, ox + 30, oy + 18, "未燃側", FT, GRAY, "lm")
    ctext(d, ox + xl - 10, oy + 18, "既燃側", FT, GRAY, "rm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T", FS, BLACK, "rm")
    # 帯の仕切り:予熱帯 [xp0..xr0], 反応帯 [xr0..xr1]
    xp0 = ox + 0.28 * xl
    xr0 = ox + 0.48 * xl
    xr1 = ox + 0.60 * xl
    for xx in (xp0, xr0, xr1):
        dashed(d, xx, oy, xx, oy - yl - 4, LGRAY, 1, 6, 5)
    ctext(d, (xp0 + xr0) / 2, oy - yl - 2, "予熱帯", FT, GRAY)
    ctext(d, (xr0 + xr1) / 2 + 6, oy - yl + 16, "反応帯", FT, RED)
    # S字温度曲線
    pts = scurve_pts(ox, oy, xl, yl, ylo=0.14, yhi=0.82, x0=0.28, x1=0.60)
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # Tu / Tb 水準線ラベル
    dashed(d, ox, oy - 0.14 * yl, xp0, oy - 0.14 * yl, GRAY, 1, 6, 5)
    dashed(d, xr1, oy - 0.82 * yl, ox + xl, oy - 0.82 * yl, GRAY, 1, 6, 5)
    ctext(d, ox + 6, oy - 0.14 * yl - 14, "Tu", FT, BLUE, "lm")
    ctext(d, ox + xl - 6, oy - 0.82 * yl - 14, "Tb", FT, BLUE, "rm")
    note(d, "反応帯からの熱伝導で予熱帯が暖まり, 温度がS字状にTu->Tbへ上がる")
    save(im, "t1e20FlameStructure")


# 20-2 t1e20BurnerDiameter : バーナー口径3本(required)
def burner_diameter():
    im, d = new(); title(d, "口径の異なる円筒バーナー上の予混合火炎")
    base = 350
    specs = [("A(太)", 150, 78), ("B(中)", 350, 52), ("C(細)", 540, 30)]
    for lab, cx, wdt in specs:
        x0, x1 = cx - wdt / 2, cx + wdt / 2
        top = 250
        # 円筒(縦2本線+底)
        d.line((x0, base, x0, top), fill=BLACK, width=3)
        d.line((x1, base, x1, top), fill=BLACK, width=3)
        d.line((x0, base, x1, base), fill=BLACK, width=3)
        ctext(d, cx, base + 22, lab, FT, BLACK)
        # 噴出矢印(上向き)
        arrow(d, cx, top + 4, cx, top - 26, BLUE, 2, 10)
        # 火炎のとんがり(予混合火炎コーン)
        ftop = top - 78
        d.line((x0, top - 30, cx, ftop), fill=RED, width=3)
        d.line((x1, top - 30, cx, ftop), fill=RED, width=3)
        d.line((x0, top - 30, x1, top - 30), fill=RED, width=2)
    ctext(d, 330, 110, "未燃予混合ガスを噴出 -> バーナー上に層流火炎", FT, GRAY)
    note(d, "口径 A > B > C。同組成ガスの供給量をゆっくり減らして挙動を比べる")
    save(im, "t1e20BurnerDiameter")


# 20-3 t1e20RayleighLine : Rayleigh線(p 対 1/rho)(helpful)
def rayleigh_line():
    im, d = new(); title(d, "Rayleigh線  圧力 p 対 比容積 1/rho")
    ox, oy, xl, yl = 120, 350, 440, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "比容積 1/rho", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "圧力 p", FS, BLACK, "rm")
    # 右下がり直線(Rayleigh線)
    xa, ya = ox + 0.12 * xl, oy - 0.85 * yl   # 状態1(未燃):左上
    xb, yb = ox + 0.82 * xl, oy - 0.28 * yl   # 状態2(既燃):右下
    # 直線を両端に少し延長
    d.line((ox + 0.05 * xl, oy - 0.91 * yl, ox + 0.92 * xl, oy - 0.20 * yl),
           fill=BLUE, width=3)
    ctext(d, ox + 0.55 * xl, oy - 0.62 * yl, "Rayleigh線", FT, BLUE, "lm")
    for (xp, yp, lab) in [(xa, ya, "1 (未燃)"), (xb, yb, "2 (既燃)")]:
        node(d, xp, yp, 6, fill=BLUE, col=BLUE)
        dashed(d, xp, oy, xp, yp, GRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, GRAY, 1, 6, 5)
        ctext(d, xp, yp - 18, lab, FT, GRAY)
    note(d, "未燃1から既燃2へは比容積が増え, 直線に沿って移る(向きだけ示す)")
    save(im, "t1e20RayleighLine")


# 20-4 t1e20FlamePropagationRest : 静止気体中の火炎伝播(required)
def flame_propagation_rest():
    im, d = new(); title(d, "静止未燃ガス中を伝播する火炎面と既燃ガスの動き")
    # 水平な管
    tx0, tx1, ty0, ty1 = 70, 590, 150, 300
    d.line((tx0, ty0, tx1, ty0), fill=BLACK, width=3)
    d.line((tx0, ty1, tx1, ty1), fill=BLACK, width=3)
    d.line((tx0, ty0, tx0, ty1), fill=BLACK, width=3)
    d.line((tx1, ty0, tx1, ty1), fill=BLACK, width=3)
    cy = (ty0 + ty1) / 2
    # 火炎面(中央やや左)
    fx = 300
    d.line((fx, ty0, fx, ty1), fill=RED, width=4)
    ctext(d, fx, ty0 - 16, "火炎面", FT, RED)
    # 未燃(左)・既燃(右)
    ctext(d, (tx0 + fx) / 2, ty0 + 26, "静止未燃ガス", FT, BLUE)
    ctext(d, (tx0 + fx) / 2, ty0 + 50, "Tu", FT, BLUE)
    ctext(d, (fx + tx1) / 2, ty0 + 26, "既燃ガス", FT, GREEN)
    ctext(d, (fx + tx1) / 2, ty0 + 50, "Tb", FT, GREEN)
    # 火炎面が左へ進む(Su)
    arrow(d, fx - 8, cy, fx - 70, cy, RED, 4, 14)
    ctext(d, fx - 40, cy - 18, "Su (火炎の進行)", FT, RED)
    # 既燃ガスが右へ動く(S)
    arrow(d, fx + 30, cy + 40, fx + 110, cy + 40, GREEN, 4, 14)
    ctext(d, fx + 70, cy + 58, "S (既燃ガスの動き)", FT, GREEN)
    note(d, "静止座標では火炎面が未燃側へ進み, 既燃ガスは膨張で反対側へ流れる")
    save(im, "t1e20FlamePropagationRest")


# 20-5 t1e20SoapBubbleMethod : シャボン玉法(required)
def soap_bubble_method():
    im, d = new(); title(d, "シャボン玉法(定圧)による層流燃焼速度の測定")
    cx, cy = 330, 235
    r_u = 60    # 点火前(未燃)実線円
    r_b = 130   # 全燃焼後 破線円
    # 大きい破線円(rb)
    dashed_circle(d, cx, cy, r_b, GRAY, 2)
    # 小さい実線円(ru)
    d.ellipse((cx - r_u, cy - r_u, cx + r_u, cy + r_u), outline=BLUE, width=3)
    # 中心の点火点
    node(d, cx, cy, 6, fill=RED, col=RED)
    ctext(d, cx, cy + 18, "点火点", FT, GRAY)
    # 外向きの火炎伝播矢印(1本)
    ang = math.radians(-35)
    arrow(d, cx + r_u * math.cos(ang), cy + r_u * math.sin(ang),
          cx + r_b * math.cos(ang), cy + r_b * math.sin(ang), RED, 3, 13)
    # 半径ラベル
    dashed(d, cx, cy, cx - r_u, cy, BLUE, 1, 5, 4)
    ctext(d, cx - r_u / 2, cy - 14, "ru", FT, BLUE)
    ctext(d, cx, cy - r_b - 14, "rb (全燃焼後)", FT, GRAY)
    ctext(d, cx - r_u - 8, cy + r_u + 6, "点火前", FT, BLUE, "rm")
    note(d, "点火前の未燃球(ru)が球状に燃え広がり全燃焼後(rb)へ膨張する")
    save(im, "t1e20SoapBubbleMethod")


# 20-6 t1e20EquivalenceRatioCurve : 当量比と燃焼速度(helpful)
def equivalence_ratio_curve():
    im, d = new(); title(d, "層流燃焼速度の当量比依存(ピークはphi=1のやや右)")
    ox, oy, xl, yl = 110, 350, 460, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "当量比 phi", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "層流燃焼速度 Su", FT, BLACK, "rm")
    # phi=1 の目盛線(グラフ幅の中央付近)
    x_phi1 = ox + 0.45 * xl
    dashed(d, x_phi1, oy, x_phi1, oy - yl - 4, GRAY, 1, 6, 5)
    ctext(d, x_phi1, oy + 16, "phi = 1", FT, GRAY)
    # 上に凸の曲線, ピークは phi=1 のわずかに右(t_peak=0.52)
    t_peak = 0.52
    pts = []
    for i in range(0, 201):
        t = 0.05 + (0.95 - 0.05) * i / 200
        v = 0.85 * math.exp(-((t - t_peak) ** 2) / (2 * 0.16 ** 2))
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # ピーク位置の縦破線
    xp = ox + t_peak * xl
    yp = oy - 0.85 * yl
    dashed(d, xp, oy, xp, yp, LGRAY, 1, 5, 4)
    node(d, xp, yp, 5, fill=BLUE, col=BLUE)
    note(d, "熱解離の影響で燃焼速度の最大はわずかに過濃側(phi>1)へずれる")
    save(im, "t1e20EquivalenceRatioCurve")


# 20-7 t1e20ThermalTheoryProfile : 熱理論の温度分布と火炎帯厚さ(required)
def thermal_theory_profile():
    im, d = new(); title(d, "熱理論の温度分布と火炎帯厚さ delta")
    ox, oy, xl, yl = 110, 340, 460, 240
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "x", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T", FS, BLACK, "rm")
    # 火炎帯 [x0..x1]
    x0f, x1f = 0.30, 0.58
    pts = scurve_pts(ox, oy, xl, yl, ylo=0.16, yhi=0.80, x0=x0f, x1=x1f)
    d.line(pts, fill=BLUE, width=3, joint="curve")
    xa, xb = ox + x0f * xl, ox + x1f * xl
    xmid = ox + 0.44 * xl
    for xx in (xa, xmid, xb):
        dashed(d, xx, oy, xx, oy - yl - 4, LGRAY, 1, 6, 5)
    # 予熱帯・反応帯ラベル
    ctext(d, (xa + xmid) / 2, oy - yl + 4, "予熱帯", FT, GRAY)
    ctext(d, (xmid + xb) / 2 + 4, oy - yl + 22, "反応帯", FT, RED)
    # 火炎帯厚さ delta を両矢印で
    yd = oy - 0.92 * yl
    dashed(d, xa, oy - 0.80 * yl, xa, yd, LGRAY, 1, 5, 4)
    dashed(d, xb, oy - 0.80 * yl, xb, yd, LGRAY, 1, 5, 4)
    arrow(d, xa, yd, xb, yd, RED, 2, 11)
    arrow(d, xb, yd, xa, yd, RED, 2, 11)
    ctext(d, (xa + xb) / 2, yd - 14, "火炎帯厚さ delta", FT, RED)
    # Tu/Tb
    ctext(d, ox + 6, oy - 0.16 * yl - 14, "Tu", FT, BLUE, "lm")
    ctext(d, ox + xl - 6, oy - 0.80 * yl - 14, "Tb", FT, BLUE, "rm")
    note(d, "予熱帯の熱伝導と火炎帯厚さ delta から層流燃焼速度を見積もる")
    save(im, "t1e20ThermalTheoryProfile")


# 20-8 t1e20PressureDependence : 圧力と燃焼速度(helpful)
def pressure_dependence():
    im, d = new(); title(d, "層流燃焼速度の圧力依存(メタン・空気: 右下がり)")
    ox, oy, xl, yl = 120, 350, 440, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "圧力 p", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "層流燃焼速度 Su", FT, BLACK, "rm")
    # 単調減少曲線
    pts = []
    for i in range(0, 201):
        t = 0.06 + (0.94 - 0.06) * i / 200
        v = 0.85 * math.exp(-1.7 * t) + 0.06
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 1・5・10気圧の目盛
    for (t, lab) in [(0.10, "1"), (0.50, "5"), (0.90, "10")]:
        xp = ox + t * xl
        dashed(d, xp, oy, xp, oy - 4, GRAY, 1, 5, 4)
        ctext(d, xp, oy + 16, lab + " 気圧", FT, GRAY)
    note(d, "圧力が高いほど層流燃焼速度は小さくなる(負の圧力依存)")
    save(im, "t1e20PressureDependence")


# 20-9 t1e20DilutionComparison : 希釈ガスの比較(helpful)
def dilution_comparison():
    im, d = new(); title(d, "希釈ガスによる層流燃焼速度の低下(アルゴン vs 水蒸気)")
    ox, oy, xl, yl = 120, 350, 440, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "希釈濃度", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "層流燃焼速度 Su", FT, BLACK, "rm")
    # アルゴン(上・緩やか)
    apts = []
    for i in range(0, 201):
        t = i / 200
        v = 0.82 - 0.55 * t
        apts.append((ox + t * xl, oy - v * yl))
    d.line(apts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.72 * xl, oy - 0.50 * yl, "アルゴン希釈", FT, BLUE, "lm")
    # 水蒸気(下・急)
    spts = []
    for i in range(0, 201):
        t = i / 200
        v = 0.82 - 0.78 * t
        spts.append((ox + t * xl, oy - v * yl))
    d.line(spts, fill=RED, width=3, joint="curve")
    ctext(d, ox + 0.55 * xl, oy - 0.16 * yl, "水蒸気希釈", FT, RED, "lm")
    note(d, "比熱の大きい水蒸気ほど火炎温度を下げ, 燃焼速度をより低くする")
    save(im, "t1e20DilutionComparison")


# 20-10 t1e20FlammabilityLimit : 可燃限界(可燃範囲)(helpful)
def flammability_limit():
    im, d = new(); title(d, "可燃範囲の比較(水素 と メタン)")
    ox = 90
    axis_y = 360
    arrow(d, ox, axis_y, ox + 500, axis_y, BLACK, 2, 11)
    ctext(d, ox + 506, axis_y, "燃料濃度", FS, BLACK, "lm")
    xl = 470
    # 各燃料の下限界・上限界(相対位置0-1)を帯で
    rows = [("水素", 0.06, 0.92, BLUE, 150),
            ("メタン", 0.12, 0.34, GREEN, 250)]
    for lab, lo, hi, col, yb in rows:
        x0 = ox + lo * xl
        x1 = ox + hi * xl
        d.rectangle((x0, yb - 22, x1, yb + 22), outline=col, width=3, fill=FILL1)
        ctext(d, ox - 6, yb, lab, FT, col, "rm")
        # 下限界・上限界の縦線
        dashed(d, x0, yb + 22, x0, axis_y, LGRAY, 1, 5, 4)
        dashed(d, x1, yb + 22, x1, axis_y, LGRAY, 1, 5, 4)
        ctext(d, x0, yb - 34, "下限界", FT, GRAY)
        ctext(d, x1, yb - 34, "上限界", FT, GRAY)
        ctext(d, (x0 + x1) / 2, yb, "可燃範囲", FT, col)
    note(d, "水素の可燃範囲(帯)はメタンより格段に広い(下限界〜上限界)")
    save(im, "t1e20FlammabilityLimit")


# 20-11 t1e20KarlovitzShear : せん断流中の火炎伸張(required)
def karlovitz_shear():
    im, d = new(); title(d, "せん断流中の湾曲した火炎面と火炎伸張")
    # 左:上ほど速い速度分布(せん断流)の矢印列
    bx = 70
    ys = [130, 165, 200, 235, 270, 305]
    lengths = [120, 100, 82, 64, 46, 28]  # 上ほど長い
    for y, Lg in zip(ys, lengths):
        arrow(d, bx, y, bx + Lg, y, BLUE, 2, 10)
    d.line((bx, 120, bx, 315), fill=GRAY, width=1)
    ctext(d, bx - 6, 118, "y", FT, GRAY, "rm")
    ctext(d, bx + 60, 100, "速度分布 Uu(y) (せん断流)", FT, BLUE)
    # 中央:湾曲した火炎面(曲率半径R)
    fcx, fcy, R = 470, 220, 150
    # 円弧の一部(左に凸)
    prev = None
    for i in range(-40, 41):
        a = math.radians(i)
        p = (fcx - R * math.cos(a) + R * 0.62, fcy + R * math.sin(a))
        if prev is not None:
            d.line((prev[0], prev[1], p[0], p[1]), fill=RED, width=3)
        prev = p
    ctext(d, fcx - 20, fcy - 130, "湾曲した火炎面", FT, RED)
    # 曲率半径Rの補助線(中心から火炎面へ)
    cxo = fcx + R * 0.62
    dashed(d, cxo, fcy, fcx - R + R * 0.62, fcy, GRAY, 1, 6, 5)
    node(d, cxo, fcy, 4, fill=GRAY, col=GRAY)
    ctext(d, (cxo + fcx - R + R * 0.62) / 2, fcy - 14, "R", FT, GRAY)
    # A点(火炎面上)から法線方向 eta 軸
    ax, ay = fcx - R + R * 0.62, fcy
    node(d, ax, ay, 5, fill=RED, col=RED)
    ctext(d, ax - 10, ay + 16, "A", FT, RED, "rm")
    arrow(d, ax, ay, ax - 70, ay, GREEN, 2, 11)   # 法線方向 eta(左向き)
    ctext(d, ax - 78, ay, "eta (法線)", FT, GREEN, "rm")
    # 流れ方向の矢印と角度theta
    arrow(d, ax, ay, ax - 55, ay - 45, BLUE, 2, 11)
    ctext(d, ax - 60, ay - 52, "流れ", FT, BLUE, "rm")
    angle_arc(d, ax, ay, 42, 150, 180, "theta", GRAY)
    note(d, "せん断による速度勾配が火炎面を引き伸ばす(火炎法線eta と流れの角theta)")
    save(im, "t1e20KarlovitzShear")


# 20-12 t1e20LewisNumberQuench : 対向流火炎とルイス数(helpful)
def lewis_number_quench():
    im, d = new(); title(d, "対向流予混合火炎の火炎帯への熱の出入り(ルイス数効果)")
    cy = 235
    # 左右の対向ノズル
    # 左ノズル
    d.polygon([(40, cy - 55), (130, cy - 30), (130, cy + 30), (40, cy + 55)],
              outline=BLACK, width=3, fill=FILL1)
    arrow(d, 135, cy, 250, cy, BLUE, 3, 13)
    ctext(d, 85, cy, "ノズル", FT, GRAY)
    # 右ノズル
    d.polygon([(620, cy - 55), (530, cy - 30), (530, cy + 30), (620, cy + 55)],
              outline=BLACK, width=3, fill=FILL1)
    arrow(d, 525, cy, 410, cy, BLUE, 3, 13)
    ctext(d, 575, cy, "ノズル", FT, GRAY)
    # 中央の平たい火炎面(縦の帯)
    fx0, fx1 = 315, 345
    d.rectangle((fx0, cy - 90, fx1, cy + 90), outline=RED, width=3, fill=(250, 232, 232))
    ctext(d, (fx0 + fx1) / 2, cy - 108, "火炎帯", FT, RED)
    ctext(d, 330, 120, "対向する2流の間に平たい火炎面", FT, GRAY)
    # 火炎帯への熱の流入出(上下2ケース)
    # Le<1:火炎帯へ入る(温度上がる)
    arrow(d, 200, cy - 120, 305, cy - 60, GREEN, 3, 13)
    ctext(d, 175, cy - 128, "Le < 1: 熱・物質流入(強まる)", FT, GREEN, "lm")
    # Le>1:火炎帯から出る(温度下がる)
    arrow(d, 355, cy + 60, 460, cy + 120, RED, 3, 13)
    ctext(d, 465, cy + 122, "Le > 1: 流出(火炎温度低下)", FT, RED, "lm")
    note(d, "伸張下では Le<1 と Le>1 でエンタルピーの出入りの向きが逆になる")
    save(im, "t1e20LewisNumberQuench")


# 20-13 t1e20CellularFlame : セル状火炎(helpful)
def cellular_flame():
    im, d = new(); title(d, "平面火炎(上)とセル状火炎(下)の対比")
    # 上段:滑らかな平面火炎
    y_top = 150
    d.line((90, y_top, 570, y_top), fill=RED, width=4)
    ctext(d, 330, y_top - 26, "平面火炎(滑らか)", FT, GRAY)
    # 未燃・既燃の向き(上向き伝播を示す軽い矢印)
    for x in (170, 330, 490):
        arrow(d, x, y_top + 34, x, y_top + 8, BLUE, 2, 9)
    ctext(d, 330, y_top + 48, "未燃側から供給", FT, GRAY)
    # 下段:凹凸のセル状火炎
    y_bot = 320
    pts = []
    for i in range(0, 201):
        t = i / 200
        x = 90 + t * 480
        y = y_bot - 26 * math.sin(2 * math.pi * 4 * t)
        pts.append((x, y))
    d.line(pts, fill=RED, width=4, joint="curve")
    ctext(d, 330, y_bot - 56, "セル状火炎(凹凸)", FT, RED)
    for x in (170, 330, 490):
        arrow(d, x, y_bot + 40, x, y_bot + 14, BLUE, 2, 9)
    note(d, "希薄側にすると平面火炎が凹凸(セル状)に変形する")
    save(im, "t1e20CellularFlame")


# ============================================================
if __name__ == "__main__":
    flame_structure()            # 20-1
    burner_diameter()            # 20-2
    rayleigh_line()              # 20-3
    flame_propagation_rest()     # 20-4
    soap_bubble_method()         # 20-5
    equivalence_ratio_curve()    # 20-6
    thermal_theory_profile()     # 20-7
    pressure_dependence()        # 20-8
    dilution_comparison()        # 20-9
    flammability_limit()         # 20-10
    karlovitz_shear()            # 20-11
    lewis_number_quench()        # 20-12
    cellular_flame()             # 20-13
    print("done ch20")
