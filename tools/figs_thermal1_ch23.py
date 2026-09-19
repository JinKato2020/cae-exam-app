# -*- coding: utf-8 -*-
"""熱流体力学1級 第23章「混相燃焼」の問題図(t1e23*)を描画。
白地660x420・黒線画・機構/構造/座標系/プロファイルのみ・数値や答えは書かない。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(Re_p, C_D, We, D32, St, Da, alpha, sigma, P_D, P_S 等)。"""
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


# ============================================================
# ============  問題図  t1e23*  (15)  ========================
# ============================================================

# 23-1 t1e23DragCurve : 抗力係数 C_D - Re_p 両対数(required)
def drag_curve():
    im, d = new(); title(d, "粒子の抗力係数曲線  C_D - Re_p (両対数)")
    ox, oy, xl, yl = 110, 350, 470, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "Re_p (対数)", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "C_D (対数)", FS, BLACK, "rm")
    # ストークス則 C_D=24/Re_p : 両対数で傾き -1 の直線
    d.line((ox + 0.06 * xl, oy - 0.90 * yl, ox + 0.55 * xl, oy - 0.34 * yl), fill=RED, width=3)
    ctext(d, ox + 0.12 * xl, oy - 0.86 * yl, "ストークス則 C_D=24/Re_p", FT, RED, "lm")
    # 実測抗力曲線(Re_p増で頭打ち・ニュートン域で一定へ)
    pts = []
    for i in range(0, 201):
        t = i / 200
        # 左は直線に沿い、右で頭打ち(0.44付近)へ漸近
        v = 0.90 - 0.62 * t
        floor = 0.16
        v = max(v, floor + 0.05 * math.exp(-6 * (t - 0.55)))
        pts.append((ox + (0.06 + 0.88 * t) * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.78 * xl, oy - 0.24 * yl, "実測(頭打ち)", FT, BLUE, "lm")
    # Re_p<<1 域を破線枠で
    xL = ox + 0.06 * xl; xR = ox + 0.30 * xl
    dashed(d, xL, oy, xL, oy - yl - 4, LGRAY, 1, 6, 5)
    dashed(d, xR, oy, xR, oy - yl - 4, LGRAY, 1, 6, 5)
    ctext(d, (xL + xR) / 2, oy - yl + 6, "Re_p << 1 域", FT, GRAY)
    note(d, "低Re_p域ではストークス則(傾き-1)に一致し, Re_p増で抗力係数は頭打ちになる")
    save(im, "t1e23DragCurve")


# 23-2 t1e23Preferential : 選択的移動(渦から弾き出される粒子)(helpful)
def preferential():
    im, d = new(); title(d, "乱流中の粒子の選択的移動(渦から弾き出され帯に集まる)")
    import random
    random.seed(7)
    centers = [(200, 200), (430, 175), (300, 300), (500, 300)]
    # 渦(反時計回りの円弧+矢印)
    for cx, cy in centers:
        dashed_circle(d, cx, cy, 52, LGRAY, 2)
        # 回転を示す小矢印
        arrow(d, cx + 52, cy, cx + 52, cy - 22, GRAY, 2, 9)
        ctext(d, cx, cy, "渦", FT, GRAY)
    # 粒子(渦中心から離れ、渦間の歪速度帯に集まる)
    for cx, cy in centers:
        for _ in range(6):
            a = random.uniform(0, 2 * math.pi)
            r = random.uniform(56, 74)  # 渦の外周付近(中心には無い=空隙)
            d.ellipse((cx + r * math.cos(a) - 3, cy + r * math.sin(a) - 3,
                       cx + r * math.cos(a) + 3, cy + r * math.sin(a) + 3),
                      outline=BLUE, width=2, fill=BLUE)
    # 空隙の注記(渦中心)
    ctext(d, 200, 200 - 66, "渦中心=空隙", FT, RED)
    # 歪速度帯(渦と渦の間)に集まる矢印
    arrow(d, 240, 235, 275, 258, RED, 2, 10)
    ctext(d, 360, 360, "歪速度の強い帯に粒子が集中(青点)", FT, BLUE)
    note(d, "St~1の粒子は遠心力で渦度の強い中心から弾き出され, 分布が非一様になる")
    save(im, "t1e23Preferential")


# 23-3 t1e23CollisionModes : 液滴衝突の3形態(helpful)
def collision_modes():
    im, d = new(); title(d, "液滴衝突の3形態  すれ違い / 合体 / 分離")
    ytop = 150
    # --- 左: すれ違い(衝突なし) ---
    cx = 150
    pcircle(d, cx - 28, ytop, 22, FILL1, BLUE, 2)
    pcircle(d, cx + 28, ytop + 34, 22, FILL1, BLUE, 2)
    arrow(d, cx - 28, ytop, cx + 60, ytop - 10, GRAY, 2, 10)
    arrow(d, cx + 28, ytop + 34, cx - 60, ytop + 44, GRAY, 2, 10)
    ctext(d, cx, ytop + 90, "すれ違い", FS, BLACK)
    ctext(d, cx, ytop + 112, "(衝突なし)", FT, GRAY)
    # --- 中: 合体 ---
    cx = 340
    arrow(d, cx - 70, ytop + 17, cx - 30, ytop + 17, GRAY, 2, 10)
    arrow(d, cx + 70, ytop + 17, cx + 30, ytop + 17, GRAY, 2, 10)
    pcircle(d, cx, ytop + 17, 30, (232, 240, 250), BLUE, 3)
    ctext(d, cx, ytop + 90, "合体", FS, GREEN)
    ctext(d, cx, ytop + 112, "(coalescence)", FT, GRAY)
    # --- 右: 分離(grazing) ---
    cx = 520
    pcircle(d, cx - 20, ytop, 20, FILL1, BLUE, 2)
    pcircle(d, cx + 20, ytop + 34, 20, FILL1, BLUE, 2)
    # 接触後に分かれる軌跡
    arrow(d, cx - 60, ytop - 6, cx - 20, ytop, GRAY, 2, 9)
    arrow(d, cx + 20, ytop, cx + 70, ytop - 18, RED, 2, 10)
    arrow(d, cx + 60, ytop + 40, cx + 20, ytop + 34, GRAY, 2, 9)
    arrow(d, cx - 20, ytop + 34, cx - 70, ytop + 52, RED, 2, 10)
    ctext(d, cx, ytop + 90, "衝突後の分離", FS, RED)
    ctext(d, cx, ytop + 112, "(grazing)", FT, GRAY)
    note(d, "衝突の帰結は主に 合体 か 分離. これに すれ違い を加えた3形態でモデル化する")
    save(im, "t1e23CollisionModes")


# 23-4 t1e23WeberBreakup : ウェーバー数による分裂(required)
def weber_breakup():
    im, d = new(); title(d, "気流中の液滴分裂  動圧 P_D と 表面張力 P_S の競合")
    cy = 230
    stages = [(130, "球状", 34, 0.0), (330, "扁平化", 34, 0.5), (540, "分裂", 34, 1.0)]
    for cx, lab, r, prog in stages:
        if prog < 1.0:
            # 扁平楕円(progで縦を潰す)
            rx = r * (1 + 0.5 * prog)
            ry = r * (1 - 0.4 * prog)
            d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=BLUE, width=3, fill=(235, 242, 250))
        else:
            # 分裂した複数小滴
            for dxp, dyp, rr in [(-30, -14, 15), (2, 12, 17), (34, -8, 13), (18, -22, 10)]:
                d.ellipse((cx + dxp - rr, cy + dyp - rr, cx + dxp + rr, cy + dyp + rr),
                          outline=BLUE, width=2, fill=(235, 242, 250))
        ctext(d, cx, cy + 78, lab, FS, BLACK)
        if prog < 1.0:
            # 前よどみ点の動圧 P_D(気流→液滴、左から)
            arrow(d, cx - r - 46, cy, cx - r - 8, cy, RED, 3, 12)
            ctext(d, cx - r - 46, cy - 18, "P_D", FT, RED, "lm")
            # 表面張力 P_S(内向き)
            arrow(d, cx, cy - r - 30, cx, cy - r - 6, GREEN, 2, 10)
            ctext(d, cx + 10, cy - r - 26, "P_S", FT, GREEN, "lm")
    # 遷移矢印
    arrow(d, 190, cy, 260, cy, GRAY, 3, 12)
    arrow(d, 400, cy, 470, cy, GRAY, 3, 12)
    note(d, "気流の動圧が表面張力に打ち勝つ(P_D/P_S>=1)と, 液滴は扁平化して分裂する")
    save(im, "t1e23WeberBreakup")


# 23-5 t1e23Atomization : 微粒化(1個->多数, 体積一定・表面積増)(required)
def atomization():
    im, d = new(); title(d, "微粒化  大きな1個の液滴 -> 多数の小液滴(体積は同じ)")
    # 左: 大きな1個
    c1x, c1y, r1 = 150, 220, 78
    pcircle(d, c1x, c1y, r1, (232, 240, 250), BLUE, 3)
    dim(d, c1x - r1, c1y + r1 + 22, c1x + r1, c1y + r1 + 22, "直径 D", col=GRAY)
    ctext(d, c1x, c1y - r1 - 18, "大液滴 1個", FT, BLUE)
    # 中央: 変換矢印
    arrow(d, 250, c1y, 350, c1y, GRAY, 3, 13)
    ctext(d, 300, c1y - 18, "微粒化", FT, GRAY)
    # 右: 多数の小液滴群
    import random
    random.seed(3)
    for _ in range(46):
        x = random.uniform(400, 590)
        y = random.uniform(140, 320)
        rr = 8
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=BLUE, width=2, fill=(232, 240, 250))
    ctext(d, 495, 118, "小液滴群(直径 D/alpha)", FT, BLUE)
    ctext(d, 495, 340, "個数 増 / 表面積総和 増", FT, RED)
    note(d, "総体積は保存. 径を1/alphaにすると個数はalpha^3倍, 表面積総和はalpha倍に増える")
    save(im, "t1e23Atomization")


# 23-6 t1e23LiquidColumn : 液柱分裂(WAVE, blob->parcel)(helpful)
def liquid_column():
    im, d = new(); title(d, "液柱分裂モデル  ノズル -> 不安定波(WAVE) -> parcel液滴")
    cy = 230
    # ノズル
    box(d, 55, cy - 30, 130, cy + 30, FILL1, 3)
    ctext(d, 92, cy - 48, "ノズル", FT, GRAY)
    ctext(d, 92, cy, "径 d0", FT, GRAY)
    # 液柱(表面に成長する波)
    xs = 130
    xe = 330
    top = []
    bot = []
    for i in range(0, 101):
        t = i / 100
        x = xs + (xe - xs) * t
        amp = 6 + 20 * t  # 下流ほど波が成長
        y0 = cy - 24 + amp * math.sin(2 * math.pi * 3 * t)
        y1 = cy + 24 - amp * math.sin(2 * math.pi * 3 * t)
        top.append((x, y0)); bot.append((x, y1))
    d.line(top, fill=BLUE, width=3, joint="curve")
    d.line(bot, fill=BLUE, width=3, joint="curve")
    d.line((xs, cy - 24, xs, cy + 24), fill=BLUE, width=3)
    ctext(d, 220, cy - 78, "表面に成長する不安定波(WAVE)", FT, RED)
    ctext(d, 200, cy, "blob(初期径=ノズル径)", FT, GRAY)
    # 分裂 -> parcel 液滴群
    import random
    random.seed(5)
    for _ in range(26):
        x = random.uniform(360, 600)
        y = random.uniform(cy - 70, cy + 70)
        rr = random.uniform(4, 10)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=BLUE, width=2, fill=(232, 240, 250))
    arrow(d, 335, cy, 360, cy, GRAY, 3, 12)
    ctext(d, 480, cy - 90, "多数のparcel液滴に分裂", FT, BLUE)
    note(d, "液柱表面に最も速く増幅する波が成長して分裂. 初期粒径はノズル直径にとる")
    save(im, "t1e23LiquidColumn")


# 23-7 t1e23DdmScheme : DDM/PSI-Cell(オイラー格子+ラグランジュ液滴)(helpful)
def ddm_scheme():
    im, d = new(); title(d, "離散液滴モデル(DDM)  オイラー格子(気相)+ラグランジュ液滴")
    # オイラー格子
    gx0, gy0, gx1, gy1 = 90, 110, 590, 340
    nx, ny = 6, 4
    for i in range(nx + 1):
        x = gx0 + (gx1 - gx0) * i / nx
        d.line((x, gy0, x, gy1), fill=LGRAY, width=1)
    for j in range(ny + 1):
        y = gy0 + (gy1 - gy0) * j / ny
        d.line((gx0, y, gx1, y), fill=LGRAY, width=1)
    ctext(d, gx0 + 4, gy0 - 14, "オイラー格子(気相: 有限体積セル)", FT, GRAY, "lm")
    # ラグランジュ液滴(parcel)の軌跡
    pts = [(110, 300), (180, 265), (260, 235), (350, 215), (450, 200), (555, 185)]
    d.line(pts, fill=BLUE, width=3, joint="curve")
    for (x, y) in pts:
        d.ellipse((x - 7, y - 7, x + 7, y + 7), outline=BLUE, width=2, fill=(232, 240, 250))
    ctext(d, 350, 215 - 22, "代表液滴(parcel)の軌跡", FT, BLUE)
    # あるセルでの双方向交換(生成項)
    ex, ey = 350, 215
    arrow(d, ex, ey, ex, ey - 44, RED, 2, 11)
    arrow(d, ex, ey - 44, ex, ey, GREEN, 2, 11)
    ctext(d, ex + 12, ey - 30, "質量・運動量・熱の交換", FT, RED, "lm")
    ctext(d, ex + 12, ey - 10, "(PSI-Cell 生成項・双方向)", FT, GREEN, "lm")
    note(d, "気相はオイラー法, 液滴はラグランジュ法. セル毎に気液が生成項として双方向にやり取り")
    save(im, "t1e23DdmScheme")


# 23-8 t1e23SauterD32 : ザウター平均粒径 D32(多分散 vs 一様径)(required)
def sauter_d32():
    im, d = new(); title(d, "ザウター平均粒径 D32  体積と表面積を一致させる代表径")
    # 左: 多分散な液滴群
    box(d, 55, 90, 320, 360, "white", 2)
    ctext(d, 187, 110, "実際の液滴群(多分散)", FT, BLUE)
    import random
    random.seed(11)
    specs = [(120, 170, 26), (200, 160, 16), (250, 220, 30), (140, 250, 20),
             (110, 320, 12), (210, 300, 22), (270, 300, 14), (180, 350 - 130, 10)]
    for x, y, rr in specs:
        pcircle(d, x, y, rr, (232, 240, 250), BLUE, 2)
    # 右: 一様径 D32 群(同じ全体積・全表面積)
    box(d, 340, 90, 605, 360, "white", 2)
    ctext(d, 472, 110, "等価な一様径 D32 群", FT, RED)
    r0 = 21
    idx = 0
    for gy in (170, 235, 300):
        for gx in (400, 450, 500, 550):
            if idx < 10:
                pcircle(d, gx, gy, r0, (250, 236, 236), RED, 2)
                idx += 1
    arrow(d, 322, 225, 338, 225, GRAY, 3, 12)
    note(d, "全体積(径の3乗和)と全表面積(径の2乗和)を同時に一致させる代表径が D32")
    save(im, "t1e23SauterD32")


# 23-9 t1e23BoilingAltitude : 沸騰と高度(飽和蒸気圧曲線)(helpful)
def boiling_altitude():
    im, d = new(); title(d, "飽和蒸気圧曲線と沸点  山上は低圧で低温沸騰")
    ox, oy, xl, yl = 110, 350, 460, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "飽和蒸気圧 Psat", FS, BLACK, "rm")
    # 飽和蒸気圧曲線(指数的に増加)
    pts = []
    for i in range(0, 201):
        t = i / 200
        v = 0.10 * math.exp(2.4 * t)
        v = min(v, 0.95)
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.62 * xl, oy - 0.40 * yl, "飽和蒸気圧曲線", FT, BLUE, "lm")
    # 1気圧の水平線 -> 100degC
    y1 = oy - 0.72 * yl
    dashed(d, ox, y1, ox + xl, y1, GRAY, 1, 7, 5)
    ctext(d, ox + xl - 6, y1 - 12, "1 気圧(地上)", FT, GRAY, "rm")
    # 山上の低い気圧
    y2 = oy - 0.50 * yl
    dashed(d, ox, y2, ox + xl, y2, ORANGE, 1, 7, 5)
    ctext(d, ox + xl - 6, y2 - 12, "山上の低い気圧", FT, ORANGE, "rm")
    # 交点
    def tx_at(v):
        return ox + (math.log(v / 0.10) / 2.4) * xl
    x1 = tx_at(0.72); x2 = tx_at(0.50)
    node(d, x1, y1, 5, fill=BLACK); node(d, x2, y2, 5, fill=ORANGE, col=ORANGE)
    dashed(d, x1, y1, x1, oy, GRAY, 1, 6, 5); ctext(d, x1, oy + 16, "100degC", FT, BLACK)
    dashed(d, x2, y2, x2, oy, ORANGE, 1, 6, 5); ctext(d, x2, oy + 16, "低温で沸騰", FT, ORANGE)
    note(d, "沸騰は 飽和蒸気圧=雰囲気圧 で起こる. 蒸発潜熱は低圧ほど大きい(山上>地上)")
    save(im, "t1e23BoilingAltitude")


# 23-10 t1e23KelvinEq : Kelvinの式(D と P/Ps)(helpful)
def kelvin_eq():
    im, d = new(); title(d, "Kelvinの式  微小液滴ほど表面蒸気圧 P/Ps が高い")
    ox, oy, xl, yl = 110, 350, 460, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "液滴直径 D", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "P / Ps", FS, BLACK, "rm")
    # P/Ps=1 の水準線(平面, D->無限大)
    y1 = oy - 0.18 * yl
    dashed(d, ox, y1, ox + xl, y1, GRAY, 1, 7, 5)
    ctext(d, ox + xl - 6, y1 - 12, "P/Ps = 1 (平面 D->無限大)", FT, GRAY, "rm")
    # 曲線: Dが小さいほどP/Psが1より大きく急上昇(ln(P/Ps) prop 1/D)
    pts = []
    for i in range(0, 201):
        t = 0.04 + (1.0 - 0.04) * i / 200
        v = 0.18 + 0.028 / t  # 1/D 依存で左端で急上昇
        v = min(v, 0.92)
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, ox + 0.10 * xl, oy - 0.80 * yl, "微小液滴ほど蒸気圧 高", FT, RED, "lm")
    arrow(d, ox + 0.22 * xl, oy - 0.70 * yl, ox + 0.10 * xl, oy - 0.78 * yl, RED, 2, 10)
    note(d, "右辺が 1/D に比例するため, 直径が小さいほど P/Ps>1 となり蒸発しやすい")
    save(im, "t1e23KelvinEq")


# 23-11 t1e23DsquaredHistory : 単一油粒燃焼の3期間(D^2-t)(helpful)
def dsquared_history():
    im, d = new(); title(d, "単一油粒燃焼の3期間  D^2 の時間変化(A加熱->B蒸発->C燃焼)")
    ox, oy, xl, yl = 110, 350, 470, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "時間 t", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "(粒径)^2 = D^2", FS, BLACK, "rm")
    # 期間区切り: A[0..tA], B[tA..tB], C[tB..tend]
    tA, tB, tend = 0.22, 0.60, 0.92
    yA = 0.86   # 初期(ほぼ平坦の加熱)
    yB = 0.78   # A終わり
    yC = 0.30   # B終わり(蒸発で減少)
    yE = 0.06   # 燃えつき
    def X(t): return ox + t * xl
    def Y(v): return oy - v * yl
    # A: ほぼ平坦
    d.line((X(0.02), Y(yA), X(tA), Y(yB)), fill=BLUE, width=3)
    # B: 蒸発で直線減少
    d.line((X(tA), Y(yB), X(tB), Y(yC)), fill=BLUE, width=3)
    # C: 燃焼で急減
    d.line((X(tB), Y(yC), X(tend), Y(yE)), fill=BLUE, width=3)
    for t in (tA, tB):
        dashed(d, X(t), oy, X(t), oy - yl - 4, LGRAY, 1, 6, 5)
    ctext(d, X((0.02 + tA) / 2), oy - yl + 6, "A 加熱", FT, GRAY)
    ctext(d, X((tA + tB) / 2), oy - yl + 6, "B 蒸発", FT, GREEN)
    ctext(d, X((tB + tend) / 2), oy - yl + 6, "C 燃焼", FT, RED)
    # t1(着火, B途中〜Bで) t2(燃えつき)
    node(d, X(tA), oy, 5, fill=ORANGE, col=ORANGE); ctext(d, X(tA), oy + 16, "t1 着火", FT, ORANGE)
    node(d, X(tend), Y(yE), 5, fill=RED, col=RED); ctext(d, X(tend), oy + 16, "t2 燃えつき", FT, RED)
    note(d, "A加熱->B蒸発(t1で自然着火)->C燃焼(t2で燃えつき). A+Bが着火遅れに相当")
    save(im, "t1e23DsquaredHistory")


# 23-12 t1e23Extinction : 単一液滴の消炎(球殻火炎+質量流束)(required)
def extinction():
    im, d = new(); title(d, "単一液滴の拡散燃焼と消炎  直径減少で滞留時間短->消炎")
    stages = [(160, 42, 92, "大直径: 火炎保持"),
              (400, 26, 66, "小直径: 消炎へ")]
    cy = 235
    for cx, rd, rf, lab in stages:
        # 火炎(球殻)
        dashed_circle(d, cx, cy, rf, RED, 2)
        # 液滴
        pcircle(d, cx, cy, rd, (232, 240, 250), BLUE, 3)
        ctext(d, cx, cy, "液滴", FT, BLUE)
        # 燃料蒸気の質量流束(外向き矢印)
        for a in range(0, 360, 60):
            rad = math.radians(a)
            arrow(d, cx + rd * math.cos(rad), cy + rd * math.sin(rad),
                  cx + (rf - 6) * math.cos(rad), cy + (rf - 6) * math.sin(rad), GREEN, 2, 9)
        ctext(d, cx, cy + rf + 22, lab, FS, BLACK)
    ctext(d, 280, cy, "縮小", FT, GRAY)
    arrow(d, 250, cy, 320, cy, GRAY, 3, 12)
    ctext(d, 400, 120, "燃料蒸気の質量流束は直径に反比例して増大", FT, GREEN)
    note(d, "直径が小さくなると反応場の滞留時間が短くなり(Da<<1), 球殻火炎が消える")
    save(im, "t1e23Extinction")


# 23-13 t1e23GroupCombustion : 群燃焼の4形態(helpful)
def group_combustion():
    im, d = new(); title(d, "群燃焼数 G と噴霧火炎の燃焼形態(Gの小さい順)")
    import random
    labels = ["単一液滴燃焼", "内部群燃焼", "外部群燃焼", "外殻燃焼"]
    cxs = [130, 300, 460, 590]
    cy = 220
    R = 52
    for k, (cx, lab) in enumerate(zip(cxs, labels)):
        # 液滴塊(点群)
        random.seed(20 + k)
        drops = []
        for _ in range(9):
            a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, R * 0.8)
            drops.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        # 塊の外周
        dashed_circle(d, cx, cy, R, LGRAY, 1)
        if k == 0:
            # 各液滴に個別の火炎
            for (x, y) in drops:
                dashed_circle(d, x, y, 9, RED, 1)
                d.ellipse((x - 3, y - 3, x + 3, y + 3), outline=BLUE, width=1, fill=BLUE)
        elif k == 1:
            # 内部の一部に群火炎(内側の集団を囲む)
            for (x, y) in drops:
                d.ellipse((x - 3, y - 3, x + 3, y + 3), outline=BLUE, width=1, fill=BLUE)
            dashed_circle(d, cx, cy, R * 0.55, RED, 2)
        elif k == 2:
            for (x, y) in drops:
                d.ellipse((x - 3, y - 3, x + 3, y + 3), outline=BLUE, width=1, fill=BLUE)
            dashed_circle(d, cx, cy, R * 0.9, RED, 2)
        else:
            # 外殻だけに火炎
            for (x, y) in drops:
                d.ellipse((x - 3, y - 3, x + 3, y + 3), outline=BLUE, width=1, fill=BLUE)
            dashed_circle(d, cx, cy, R + 6, RED, 3)
        ctext(d, cx, cy + R + 26, lab, FT, BLACK)
    arrow(d, 90, 350, 600, 350, GRAY, 2, 11)
    ctext(d, 345, 368, "G 小 ------------------------> G 大", FT, GRAY)
    note(d, "G小=内部まで酸素供給され個々に燃焼. G大=外殻に火炎が偏る(赤破線=火炎)")
    save(im, "t1e23GroupCombustion")


# 23-14 t1e23CoalProximate : 石炭の工業分析(積み上げ棒)(required)
def coal_proximate():
    im, d = new(); title(d, "石炭の工業分析  水分/揮発分/固定炭素/灰分 の質量割合")
    bx0, bx1 = 200, 340
    top, bot = 110, 360
    total = bot - top
    # 割合(下から: 灰分/固定炭素/揮発分/水分 の順に積む) -- 概念図(数値は書かない)
    segs = [("水分", 0.10, (210, 225, 245)),
            ("揮発分", 0.28, (250, 236, 210)),
            ("固定炭素", 0.52, (215, 215, 215)),
            ("灰分", 0.10, (235, 235, 235))]
    y = top
    seg_y = {}
    for lab, frac, col in segs:
        h = total * frac
        d.rectangle((bx0, y, bx1, y + h), outline=BLACK, width=2, fill=col)
        ctext(d, (bx0 + bx1) / 2, y + h / 2, lab, FT, BLACK)
        seg_y[lab] = (y, y + h)
        y += h
    # 可燃分 / 不燃分 の区分ブラケット
    vt = seg_y["揮発分"][0]; fcb = seg_y["固定炭素"][1]
    d.line((bx1 + 14, vt, bx1 + 14, fcb), fill=GREEN, width=3)
    ctext(d, bx1 + 20, (vt + fcb) / 2, "可燃分", FT, GREEN, "lm")
    ctext(d, bx1 + 20, (vt + fcb) / 2 + 18, "(揮発分+固定炭素)", FT, GREEN, "lm")
    mt = seg_y["水分"][0]; ab = seg_y["灰分"][1]
    d.line((bx0 - 14, mt, bx0 - 14, seg_y["水分"][1]), fill=GRAY, width=3)
    d.line((bx0 - 14, seg_y["灰分"][0], bx0 - 14, ab), fill=GRAY, width=3)
    ctext(d, bx0 - 20, mt + 6, "不燃分(水分)", FT, GRAY, "rm")
    ctext(d, bx0 - 20, ab - 6, "不燃分(灰分)", FT, GRAY, "rm")
    # 燃料比の定義矢印
    fc = seg_y["固定炭素"]; vf = seg_y["揮発分"]
    arrow(d, bx1 + 90, (fc[0] + fc[1]) / 2, bx1 + 90, (vf[0] + vf[1]) / 2, RED, 2, 10)
    ctext(d, bx1 + 96, (fc[0] + vf[1]) / 2, "燃料比 = 固定炭素/揮発分", FT, RED, "lm")
    note(d, "工業分析は 不燃分(水分・灰分)と 可燃分(揮発分・固定炭素)に区分する(割合は概念値)")
    save(im, "t1e23CoalProximate")


# 23-15 t1e23PulverizedCoal : 微粉炭の反応過程(時系列)(helpful)
def pulverized_coal():
    im, d = new(); title(d, "微粉炭の反応過程  加熱 -> 揮発分放出 -> チャー燃焼")
    cy = 210
    # 1: 加熱
    cx = 130
    pcircle(d, cx, cy, 34, (60, 60, 60), BLACK, 2)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        arrow(d, cx + 46 * math.cos(rad), cy + 46 * math.sin(rad),
              cx + 38 * math.cos(rad), cy + 38 * math.sin(rad), ORANGE, 2, 8)
    ctext(d, cx, cy + 70, "加熱", FS, BLACK)
    ctext(d, cx, cy + 92, "石炭粒子", FT, GRAY)
    arrow(d, cx + 60, cy, cx + 100, cy, GRAY, 3, 12)
    # 2: 揮発分放出(気相火炎)
    cx = 330
    pcircle(d, cx, cy, 28, (80, 80, 80), BLACK, 2)
    # 放出ガス+火炎
    dashed_circle(d, cx, cy, 58, RED, 2)
    for a in range(0, 360, 60):
        rad = math.radians(a)
        arrow(d, cx + 30 * math.cos(rad), cy + 30 * math.sin(rad),
              cx + 54 * math.cos(rad), cy + 54 * math.sin(rad), GREEN, 2, 9)
    ctext(d, cx, cy + 76, "揮発分放出", FS, GREEN)
    ctext(d, cx, cy + 98, "(気相で火炎・速い)", FT, GRAY)
    arrow(d, cx + 70, cy, cx + 110, cy, GRAY, 3, 12)
    # 3: チャー燃焼(多孔質)
    cx = 540
    pcircle(d, cx, cy, 32, (150, 150, 150), BLACK, 2)
    # 多孔質の穴
    for (dxp, dyp) in [(-12, -8), (8, -12), (-6, 10), (12, 6), (0, 0)]:
        d.ellipse((cx + dxp - 4, cy + dyp - 4, cx + dxp + 4, cy + dyp + 4), outline=BLACK, width=1)
    # 表面燃焼(内向き酸素)
    for a in range(0, 360, 60):
        rad = math.radians(a)
        arrow(d, cx + 52 * math.cos(rad), cy + 52 * math.sin(rad),
              cx + 36 * math.cos(rad), cy + 36 * math.sin(rad), RED, 2, 9)
    ctext(d, cx, cy + 76, "チャー燃焼", FS, RED)
    ctext(d, cx, cy + 98, "(多孔質固体・遅い)", FT, GRAY)
    # 時間軸
    arrow(d, 90, 350, 600, 350, GRAY, 2, 11)
    ctext(d, 345, 368, "時間 t (揮発分は速く, チャー燃焼は遅い)", FT, GRAY)
    note(d, "揮発分(低分子炭化水素・CO・H2)が速く燃え, 残る多孔質チャーが遅れて燃える")
    save(im, "t1e23PulverizedCoal")


# ============================================================
if __name__ == "__main__":
    drag_curve()          # 23-1
    preferential()        # 23-2
    collision_modes()     # 23-3
    weber_breakup()       # 23-4
    atomization()         # 23-5
    liquid_column()       # 23-6
    ddm_scheme()          # 23-7
    sauter_d32()          # 23-8
    boiling_altitude()    # 23-9
    kelvin_eq()           # 23-10
    dsquared_history()    # 23-11
    extinction()          # 23-12
    group_combustion()    # 23-13
    coal_proximate()      # 23-14
    pulverized_coal()     # 23-15
    print("done ch23 problems")
