# -*- coding: utf-8 -*-
"""振動1級 第9章「結果の検証と考察」問題図 26枚。figlibで白地660x420線画。
方針: 正確さ最優先・機構のみ・装飾禁止。数式ラベルはASCII(w=omega,phi,z=zeta,B^T等)で豆腐回避。
required図は答え(固有値・結論・正解の向き・数値解)を描かない。helpful図は結果値を描いてよい。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ------------------------------------------------ helpers
def dsh(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = t; b = min(t + dl, L)
        d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)
        t += dl + gap


def box(d, x0, y0, x1, y1, fill=FILL1, col=BLACK, wd=2):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def flowbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS, col=BLACK):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill, col)
    ls = text.split("\n")
    for i, line in enumerate(ls):
        ctext(d, cx, cy - (len(ls) - 1) * 10 + i * 20, line, fnt, col)


def damper(d, x, ya, yb, w=14):
    """縦ダンパ。ya,ybは端点(順不同)。下側に筒・上からピストン棒。"""
    yt, yl = min(ya, yb), max(ya, yb)
    ym = (yt + yl) / 2
    # cylinder (bottom half)
    d.rectangle((x - w, ym - 6, x + w, yl), outline=BLACK, width=3)
    # piston rod from top end down to piston plate
    d.line((x, yt, x, ym + 6), fill=BLACK, width=3)
    d.line((x - w + 3, ym + 6, x + w - 3, ym + 6), fill=BLACK, width=5)


# ================================================ 9-1 MAC定義 (helpful)
def f_mac_definition():
    im, d = new(); title(d, "MAC の定義と 残差 ([K]-w^2[M]) phi -> {0} の対応")
    cx = 210
    # MAC as fraction
    ctext(d, cx, 120, "MAC(a,b) =", F)
    d.line((cx - 130, 190, cx + 130, 190), fill=BLACK, width=3)
    ctext(d, cx, 165, "( phi_a^T phi_b )^2", FS)
    ctext(d, cx, 215, "(phi_a^T phi_a)(phi_b^T phi_b)", FT)
    ctext(d, cx, 262, "= 内積の2乗 / ノルム積", FT, GRAY)
    ctext(d, cx, 300, "1に近い=よく一致", FT, BLUE)
    # residual eqn
    d.line((410, 100, 410, 340), fill=LGRAY, width=1)
    rx = 535
    box(d, rx - 110, 140, rx + 110, 200, (225, 240, 225))
    ctext(d, rx, 170, "([K] - w^2 [M]) phi", FS)
    arrow(d, rx, 205, rx, 245, GRAY, 3, 12)
    box(d, rx - 60, 250, rx + 60, 300, (245, 230, 230))
    ctext(d, rx, 275, "-> {0}", F, RED)
    ctext(d, rx, 322, "真の固有対で残差ゼロ", FT, GRAY)
    save(im, "v1e9MacDefinition")


# ================================================ 9-2 モード直交性 (helpful)
def f_mode_orthogonality():
    im, d = new(); title(d, "[M] を介した2モードの直交:phi_i^T [M] phi_j = 0 (i != j)")
    def modeshape(ox, mode, col, lab):
        x0, ytop, ybot = ox, 110, 320
        dsh(d, x0, ytop, x0, ybot, LGRAY)
        n = 40; amp = 55
        pts = []
        for i in range(n + 1):
            t = i / n
            y = amp * math.sin(mode * math.pi * t)
            pts.append((x0 + y, ytop + (ybot - ytop) * t))
        plot(d, 0, 0, pts, col, 4)
        for i in range(0, n + 1, 8):
            t = i / n
            y = amp * math.sin(mode * math.pi * t)
            node(d, x0 + y, ytop + (ybot - ytop) * t, 4, col, col)
        ctext(d, x0, ybot + 22, lab, FT, col)
    modeshape(160, 1, BLUE, "phi_1 (1次)")
    modeshape(370, 2, GREEN, "phi_2 (2次)")
    ctext(d, 560, 180, "慣性力 [M]phi_i", FT, GRAY)
    ctext(d, 560, 210, "と変位 phi_j が", FT, GRAY)
    ctext(d, 560, 240, "重み[M]で直交", FT, GRAY)
    note(d, "質量行列を重みとした内積がゼロ=モード直交性")
    save(im, "v1e9ModeOrthogonality")


# ================================================ 9-3 MAC行列 (helpful)
def f_mac_matrix():
    im, d = new(); title(d, "理想的な MAC 行列:対角 ~1(濃)・非対角 ~0(淡)")
    n = 4
    cell = 62
    ox, oy = 210, 90
    for r in range(n):
        for c in range(n):
            v = 1.0 if r == c else (0.05 + 0.08 * (1 - abs(r - c) / n))
            g = int(255 - v * 205)
            d.rectangle((ox + c * cell, oy + r * cell, ox + (c + 1) * cell, oy + (r + 1) * cell),
                        outline=BLACK, width=2, fill=(g, g, g))
            tcol = "white" if v > 0.6 else BLACK
            ctext(d, ox + c * cell + cell / 2, oy + r * cell + cell / 2, "%.2f" % v, FT, tcol)
    ctext(d, ox - 18, oy + n * cell / 2, "実験モード i", FT, GRAY, "mm")
    ctext(d, ox + n * cell / 2, oy - 16, "FEMモード j", FT, GRAY)
    ctext(d, ox + n * cell + 20, oy + 30, "対角=1", FT, BLUE, "lm")
    ctext(d, ox + n * cell + 20, oy + 150, "非対角~0", FT, GRAY, "lm")
    note(d, "対応するモード対のみ相関が高い=良い対応づけ")
    save(im, "v1e9MacMatrix")


# ================================================ 9-4 MAC計算結果 (helpful)
def f_mac_calc_result():
    im, d = new(); title(d, "実験モードとFEMモードの重ね描き -> MAC ~= 0.996")
    x0, ytop, ybot = 300, 100, 330
    dsh(d, x0, ytop, x0, ybot, LGRAY)
    n = 40; amp = 90
    exp = [(x0 + amp * math.sin(math.pi * (i / n)), ytop + (ybot - ytop) * i / n) for i in range(n + 1)]
    fem = [(x0 + (amp - 4) * math.sin(math.pi * (i / n)) + 3 * math.sin(2 * math.pi * i / n),
            ytop + (ybot - ytop) * i / n) for i in range(n + 1)]
    plot(d, 0, 0, exp, BLUE, 4)
    plot(d, 0, 0, fem, RED, 3)
    for i in range(0, n + 1, 8):
        node(d, exp[i][0], exp[i][1], 4, BLUE, BLUE)
    ctext(d, 470, 150, "実験モード", FT, BLUE, "lm")
    ctext(d, 470, 178, "FEMモード", FT, RED, "lm")
    box(d, 430, 250, 620, 310, (225, 240, 225))
    ctext(d, 525, 280, "MAC ~= 0.996", FS, GREEN)
    note(d, "ほぼ重なる -> MACは1に極めて近い")
    save(im, "v1e9MacCalcResult")


# ================================================ 9-5 FRFピークと分解能 (helpful)
def f_frf_modal_peak():
    im, d = new(); title(d, "共振ピーク:df 細かい(捕捉)と df 粗い(取り逃す)")
    ox, oy = 95, 345; xr, ym = 470, 255
    wn, z = 1.0, 0.03
    X = lambda r: ox + r / 2.0 * xr
    A = lambda r: 1 / math.sqrt((1 - (r / wn) ** 2) ** 2 + (2 * z * (r / wn)) ** 2)
    Amax = A(1.0)
    Y = lambda a: oy - min(a, Amax) / Amax * ym
    axes(d, ox, oy, xr + 30, ym + 25, "w", "|H|")
    fine = [(X(i / 500.0), Y(A(i / 500.0))) for i in range(20, 1000)]
    plot(d, 0, 0, fine, BLUE, 2)
    # coarse sampling markers (miss the peak)
    coarse_r = [0.3, 0.55, 0.8, 1.05, 1.3, 1.55, 1.8]
    cpts = [(X(r), Y(A(r))) for r in coarse_r]
    for p in cpts:
        node(d, p[0], p[1], 5, ORANGE, ORANGE)
    plot(d, 0, 0, cpts, ORANGE, 2)
    ctext(d, X(1.0), Y(Amax) - 14, "真のピーク", FT, BLUE)
    ctext(d, X(1.45), Y(A(1.3)) + 24, "粗い df:ピークを取り逃す", FT, ORANGE, "lm")
    note(d, "周波数分解能 df を細かくしないと鋭い共振を過小評価")
    save(im, "v1e9FrfModalPeak")


# ================================================ 9-6 Craig-Bampton (required)
def f_craig_bampton_setup():
    im, d = new(); title(d, "Craig-Bampton:境界節点で内部を切り分け 拘束+動的モードで縮約")
    # substructure block
    box(d, 130, 110, 400, 320, FILL1)
    # internal mesh
    for gx in range(1, 5):
        d.line((130 + gx * 54, 110, 130 + gx * 54, 320), fill=LGRAY, width=1)
    for gy in range(1, 4):
        d.line((130, 110 + gy * 52, 400, 110 + gy * 52), fill=LGRAY, width=1)
    ctext(d, 265, 215, "内部自由度", FS, GRAY)
    # boundary nodes on right edge
    for yy in (130, 190, 250, 300):
        node(d, 400, yy, 7, RED, RED)
    ctext(d, 415, 130, "境界節点 b", FT, RED, "lm")
    arrow(d, 430, 250, 500, 250, BLACK, 3, 13)
    # reduction: two mode sets
    box(d, 505, 120, 625, 195, (225, 240, 225))
    ctext(d, 565, 145, "拘束モード", FT)
    ctext(d, 565, 172, "(境界を単位変位)", FT, GRAY)
    box(d, 505, 235, 625, 315, (225, 235, 245))
    ctext(d, 565, 262, "内部固定の", FT)
    ctext(d, 565, 288, "動的(固定界面)モード", FT, GRAY)
    note(d, "境界を残し内部を少数モードで縮約する部分構造法")
    save(im, "v1e9CraigBamptonSetup")


# ================================================ 9-7 Guyan縮小 (required)
def f_guyan_setup():
    im, d = new(); title(d, "Guyan(静的)縮小:主自由度 m を残し 従属自由度 s を静的に凝縮")
    # a small structure with master (kept) and slave (removed) nodes
    ox, oy = 150, 300; step = 90
    coords = {(0,0):"m",(1,0):"s",(2,0):"m",(0,1):"s",(1,1):"s",(2,1):"m"}
    # springs (grid connections)
    def P(c): return (ox + c[0]*step, oy - c[1]*step*1.6)
    edges = [((0,0),(1,0)),((1,0),(2,0)),((0,1),(1,1)),((1,1),(2,1)),
             ((0,0),(0,1)),((1,0),(1,1)),((2,0),(2,1))]
    for a, b in edges:
        d.line((P(a)[0], P(a)[1], P(b)[0], P(b)[1]), fill=GRAY, width=2)
    for c, kind in coords.items():
        if kind == "m":
            node(d, P(c)[0], P(c)[1], 11, (225, 240, 225), GREEN)
            ctext(d, P(c)[0], P(c)[1], "m", FT, GREEN)
        else:
            node(d, P(c)[0], P(c)[1], 9, FILL2, GRAY)
            ctext(d, P(c)[0], P(c)[1], "s", FT, GRAY)
    ctext(d, 470, 130, "m = 主自由度(残す)", FT, GREEN, "lm")
    ctext(d, 470, 165, "s = 従属自由度(消す)", FT, GRAY, "lm")
    ctext(d, 470, 215, "慣性を無視し", FT, GRAY, "lm")
    ctext(d, 470, 245, "静的関係 s = -Kss^-1 Ksm m", FT, GRAY, "lm")
    ctext(d, 470, 275, "で s を m に凝縮", FT, GRAY, "lm")
    note(d, "従属自由度の慣性を無視する静的縮小(高次で誤差)")
    save(im, "v1e9GuyanSetup")


# ================================================ 9-8 片持ちはり断面 (required)
def f_cantilever_section():
    im, d = new(); title(d, "矩形断面(幅10 x 高20)の片持ちはり(長さ150):2方向の曲げ")
    # beam side view (length)
    wall(d, 120, 150, 300, side=1, n=6)
    d.rectangle((120, 205, 470, 245), outline=BLACK, width=3, fill=FILL1)
    dim(d, 120, 285, 470, 285, "長さ 150", col=GRAY)
    ctext(d, 295, 225, "片持ちはり", FT, GRAY)
    # cross-section
    scx, scy = 560, 210
    hw, hh = 22, 44  # width10, height20 -> scale
    d.rectangle((scx - hw, scy - hh, scx + hw, scy + hh), outline=BLACK, width=3, fill=FILL2)
    dim(d, scx - hw, scy + hh + 22, scx + hw, scy + hh + 22, "幅 10", col=GRAY)
    dim(d, scx + hw + 30, scy - hh, scx + hw + 30, scy + hh, "高 20", col=GRAY)
    # two bending directions arrows
    arrow(d, scx, scy - hh - 8, scx, scy - hh - 40, BLUE, 3, 11)
    arrow(d, scx, scy + hh + 8, scx, scy + hh + 40, BLUE, 3, 11)
    ctext(d, scx + 46, scy - hh - 30, "上下曲げ", FT, BLUE, "lm")
    arrow(d, scx - hw - 8, scy, scx - hw - 40, scy, RED, 3, 11)
    ctext(d, scx - hw - 46, scy + 18, "左右曲げ", FT, RED, "rm")
    note(d, "断面2次モーメントが方向で異なる -> 曲げ2方向で剛性が違う")
    save(im, "v1e9CantileverSection")


# ================================================ 9-9 材料スケーリング (helpful)
def f_material_scaling():
    im, d = new(); title(d, "材料 A -> B で固有振動数は w_B = sqrt(b/a) * w_A 倍")
    # A block
    box(d, 110, 150, 250, 300, FILL1)
    ctext(d, 180, 200, "材料A", FS)
    ctext(d, 180, 235, "E_a, rho_a", FT, GRAY)
    ctext(d, 180, 268, "a = E_a/rho_a", FT, BLUE)
    arrow(d, 265, 225, 360, 225, BLACK, 3, 14)
    ctext(d, 312, 200, "同一形状", FT, GRAY)
    box(d, 375, 150, 515, 300, FILL2)
    ctext(d, 445, 200, "材料B", FS)
    ctext(d, 445, 235, "E_b, rho_b", FT, GRAY)
    ctext(d, 445, 268, "b = E_b/rho_b", FT, RED)
    box(d, 100, 330, 560, 385, (225, 240, 225))
    ctext(d, 330, 357, "w ~ sqrt(E/rho) -> w_B / w_A = sqrt(b/a)", FS, GREEN)
    save(im, "v1e9MaterialScaling")


# ================================================ 9-10 L型フレーム荷重 (required)
def f_lframe_load():
    im, d = new(); title(d, "L型フレーム:モードの節/腹 と 荷重作用点(節の近く)")
    # L-shape: vertical + horizontal member
    ax, ay = 180, 320   # corner
    top = (180, 120)
    right = (470, 320)
    wall(d, 150, 320, 360, side=1, n=4)
    d.line((ax, ay, top[0], top[1]), fill=BLACK, width=6)
    d.line((ax, ay, right[0], right[1]), fill=BLACK, width=6)
    # node/antinode markers (mode shape reference, no numeric answer)
    node(d, ax, ay, 8, FILL2, GRAY); ctext(d, ax - 18, ay + 18, "節", FT, GRAY, "rm")
    node(d, top[0], top[1], 7, FILL1, BLUE); ctext(d, top[0] + 16, top[1], "腹", FT, BLUE, "lm")
    node(d, right[0], right[1], 7, FILL1, BLUE); ctext(d, right[0], right[1] + 22, "腹", FT, BLUE)
    # node region near corner on horizontal member
    midn = (300, 320)
    node(d, midn[0], midn[1], 6, FILL2, GRAY); ctext(d, midn[0], midn[1] + 22, "節付近", FT, GRAY)
    # applied load at node vicinity
    force(d, midn[0], midn[1] - 60, 0, 44, "F", RED)
    note(d, "節の近くに荷重が作用すると そのモードは励振されにくい")
    save(im, "v1e9LframeLoad")


# ================================================ 9-11 洗濯機モデル (required)
def f_washing_machine():
    im, d = new(); title(d, "洗濯機の1自由度 k-M-c モデルと 遠心力 m R w^2")
    hwall(d, 150, 510, 350, side=1, n=12)
    cx = 330
    # spring + damper to mass
    spring(d, cx - 70, 350, cx - 70, 250, coils=6, amp=13)
    ctext(d, cx - 104, 300, "k", FS, BLACK, "rm")
    damper(d, cx + 70, 350, 262)
    ctext(d, cx + 96, 300, "c", FS, BLACK, "lm")
    box(d, cx - 90, 190, cx + 90, 250, FILL1)
    ctext(d, cx, 220, "M (槽)", FS)
    # rotating unbalance m at radius R
    drum_c = (cx, 130)
    d.ellipse((drum_c[0] - 46, drum_c[1] - 46, drum_c[0] + 46, drum_c[1] + 46), outline=BLACK, width=3)
    ang = math.radians(-40)
    mp = (drum_c[0] + 34 * math.cos(ang), drum_c[1] + 34 * math.sin(ang))
    node(d, mp[0], mp[1], 9, FILL2)
    ctext(d, mp[0] + 12, mp[1] - 12, "m", FT)
    d.line((drum_c[0], drum_c[1], mp[0], mp[1]), fill=GRAY, width=2)
    ctext(d, drum_c[0] + 22, drum_c[1] + 4, "R", FT, GRAY, "lm")
    arrow(d, mp[0], mp[1], mp[0] + 30, mp[1] - 26, RED, 3, 11)
    ctext(d, mp[0] + 34, mp[1] - 34, "m R w^2", FT, RED, "lm")
    # rotation arrow
    d.arc((drum_c[0] - 46, drum_c[1] - 46, drum_c[0] + 46, drum_c[1] + 46), -20, 90, fill=GRAY, width=2)
    note(d, "回転体の偏心 m が半径 R で回り 遠心力 m R w^2 が加振源")
    save(im, "v1e9WashingMachineModel")


# ================================================ 9-12 モータ回転数と共振 (helpful)
def f_motor_rpm_resonance():
    im, d = new(); title(d, "rpm軸:12000rpm(200Hz)で共振 -> 剛性up で 250Hz超へ移動")
    ox, oy = 90, 345; xr, ym = 500, 255
    # x axis in rpm, resonance response
    X = lambda rpm: ox + rpm / 20000.0 * xr
    def peak(rpm0, h, wdt):
        return lambda rpm: h / (1 + ((rpm - rpm0) / wdt) ** 2)
    axes(d, ox, oy, xr + 30, ym + 25, "回転数 rpm", "応答")
    p1 = peak(12000, 8.0, 700)
    p2 = peak(15000, 5.5, 900)  # 250Hz=15000rpm
    Y = lambda a: oy - min(a, 9) / 9 * ym
    c1 = [(X(r), Y(p1(r))) for r in range(0, 20001, 100)]
    c2 = [(X(r), Y(p2(r))) for r in range(0, 20001, 100)]
    plot(d, 0, 0, c1, BLUE, 3)
    plot(d, 0, 0, c2, GREEN, 3)
    dsh(d, X(12000), oy, X(12000), Y(8.0), RED)
    ctext(d, X(12000), oy + 16, "12000rpm", FT, RED)
    ctext(d, X(12000), Y(8.0) - 12, "現状(200Hz)", FT, BLUE)
    dsh(d, X(15000), oy, X(15000), Y(5.5), GRAY)
    ctext(d, X(15000) + 6, oy + 16, "15000rpm", FT, GREEN, "lm")
    ctext(d, X(15000) + 6, Y(5.5) - 12, "剛性up(250Hz)", FT, GREEN, "lm")
    arrow(d, X(12200), Y(8.0), X(14800), Y(6.0), ORANGE, 2, 11)
    note(d, "固有振動数を運転回転数より上へ逃がす")
    save(im, "v1e9MotorRpmResonance")


# ================================================ 9-13 パネル自重たわみ (required)
def f_panel_gravity_sag():
    im, d = new(); title(d, "吊り下げ薄板:自重で下凸にたわみ 面内引張力が生じる")
    # two hangers at top
    hwall(d, 180, 480, 110, side=-1, n=8)
    lx, rx = 220, 440
    d.line((lx, 110, lx, 150), fill=BLACK, width=2)
    d.line((rx, 110, rx, 150), fill=BLACK, width=2)
    node(d, lx, 150, 5); node(d, rx, 150, 5)
    # sagging plate (downward-convex curve)
    n = 40
    pts = []
    for i in range(n + 1):
        t = i / n
        x = lx + (rx - lx) * t
        y = 150 + 120 * (1 - (2 * t - 1) ** 2)  # parabola sag
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 5)
    # gravity arrows
    for t in (0.25, 0.5, 0.75):
        x = lx + (rx - lx) * t
        y = 150 + 120 * (1 - (2 * t - 1) ** 2)
        arrow(d, x, y + 6, x, y + 46, GRAY, 2, 10)
    ctext(d, 330, 330, "自重 g", FT, GRAY)
    # in-plane tension arrows along the membrane at supports
    arrow(d, lx, 150, lx - 34, 132, RED, 3, 11)
    arrow(d, rx, 150, rx + 34, 132, RED, 3, 11)
    ctext(d, lx - 40, 118, "面内引張", FT, RED, "rm")
    ctext(d, rx + 40, 118, "面内引張", FT, RED, "lm")
    note(d, "たわむと膜に面内張力(応力剛性)が発生し剛性が上がる")
    save(im, "v1e9PanelGravitySag")


# ================================================ 9-14 ひずみエネルギー分担 (helpful)
def f_strain_energy_share():
    im, d = new(); title(d, "ひずみエネルギー分担率:上2点 5% ・ 下2点 30% (下を1.6倍)")
    ox, oy = 130, 340; bw = 70; gap = 40
    labels = ["上A", "上B", "下C", "下D"]
    vals = [5, 5, 30, 30]
    cols = [BLUE, BLUE, RED, RED]
    maxv = 35
    for i, (lab, v, col) in enumerate(zip(labels, vals, cols)):
        x = ox + i * (bw + gap)
        h = v / maxv * 230
        d.rectangle((x, oy - h, x + bw, oy), outline=BLACK, width=2, fill=col)
        ctext(d, x + bw / 2, oy - h - 16, "%d%%" % v, FT, col)
        ctext(d, x + bw / 2, oy + 18, lab, FT)
    d.line((ox - 20, oy, ox + 4 * (bw + gap), oy), fill=BLACK, width=2)
    ctext(d, ox - 30, oy - 115, "分担率", FT, GRAY, "rm")
    # 1.6x annotation
    x2 = ox + 2 * (bw + gap)
    arrow(d, x2 - 24, oy - 60, x2 - 24, oy - 200, ORANGE, 2, 10)
    ctext(d, x2 - 30, oy - 130, "下側を1.6倍に強化", FT, ORANGE, "rm")
    save(im, "v1e9StrainEnergyShare")


# ================================================ 9-15 ギヤかみ合いスペクトル (helpful)
def f_gear_mesh_spectrum():
    im, d = new(); title(d, "ギヤかみ合い:1次 ~2220Hz / 2次 ~4440Hz (df=20Hz 刻み)")
    ox, oy = 80, 345; xr, ym = 520, 255
    fmax = 5200
    X = lambda f: ox + f / fmax * xr
    axes(d, ox, oy, xr + 30, ym + 25, "周波数 Hz", "振幅")
    # spectral lines at mesh harmonics
    lines = [(2220, 0.9, "かみ合い1次 ~2220"), (4440, 0.6, "2次 ~4440")]
    for f, h, lab in lines:
        d.line((X(f), oy, X(f), oy - h * ym), fill=BLUE, width=3)
        node(d, X(f), oy - h * ym, 4, BLUE, BLUE)
        ctext(d, X(f), oy - h * ym - 14, lab, FT, BLUE)
    # sidebands hint (df=20Hz) around 1st
    for k in (-2, -1, 1, 2):
        f = 2220 + k * 100
        d.line((X(f), oy, X(f), oy - 0.25 * ym), fill=GRAY, width=1)
    ctext(d, X(2220), oy + 30, "df=20Hz 刻みで分解", FT, GRAY)
    note(d, "かみ合い周波数=歯数 x 回転数。df を細かくして側帯波も分離")
    save(im, "v1e9GearMeshSpectrum")


# ================================================ 9-16 2入力系ブロック図 (required)
def f_two_input_system():
    im, d = new(); title(d, "2入力系:W_R->H_R, W_L->H_L が出力 Z に合流")
    # inputs
    flowbox(d, 120, 160, 120, 66, "入力 W_R", (225, 235, 245))
    flowbox(d, 120, 300, 120, 66, "入力 W_L", (225, 235, 245))
    # transfer functions
    flowbox(d, 330, 160, 120, 66, "伝達 H_R", (225, 240, 225))
    flowbox(d, 330, 300, 120, 66, "伝達 H_L", (225, 240, 225))
    arrow(d, 180, 160, 270, 160, BLACK, 3, 12)
    arrow(d, 180, 300, 270, 300, BLACK, 3, 12)
    # summation
    sx, sy = 500, 230
    d.ellipse((sx - 26, sy - 26, sx + 26, sy + 26), outline=BLACK, width=3)
    ctext(d, sx, sy, "+", F)
    arrow(d, 390, 160, sx - 8, sy - 22, BLACK, 3, 12)
    arrow(d, 390, 300, sx - 8, sy + 22, BLACK, 3, 12)
    arrow(d, sx + 28, sy, 600, sy, BLACK, 3, 12)
    ctext(d, 612, sy, "出力 Z", FS, BLACK, "lm")
    note(d, "Z = H_R W_R + H_L W_L (2つの入力経路の重ね合わせ)")
    save(im, "v1e9TwoInputSystem")


# ================================================ 9-17 応答スペクトル基礎 (helpful)
def f_response_spectrum_basis():
    im, d = new(); title(d, "応答スペクトル:zddot入力 -> 各モード q_i最大 -> phi_ji で重ね合わせ y_j")
    flowbox(d, 120, 150, 150, 66, "地動加速度\nzddot(t)", (245, 230, 230))
    arrow(d, 200, 150, 265, 150, BLACK, 3, 12)
    # per-mode max responses
    flowbox(d, 360, 110, 150, 56, "モード1 最大 q_1", (225, 240, 225), FT)
    flowbox(d, 360, 190, 150, 56, "モード2 最大 q_2", (225, 240, 225), FT)
    arrow(d, 195, 165, 285, 110, GRAY, 2, 10)
    arrow(d, 195, 165, 285, 190, GRAY, 2, 10)
    # combine with phi
    sx, sy = 560, 150
    d.ellipse((sx - 24, sy - 24, sx + 24, sy + 24), outline=BLACK, width=3)
    ctext(d, sx, sy, "sum", FT)
    arrow(d, 435, 110, sx - 10, sy - 18, GRAY, 2, 10)
    arrow(d, 435, 190, sx - 10, sy + 18, GRAY, 2, 10)
    ctext(d, 500, 108, "x phi_j1", FT, BLUE)
    ctext(d, 500, 205, "x phi_j2", FT, BLUE)
    arrow(d, sx, sy + 26, sx, 260, BLACK, 3, 12)
    flowbox(d, sx, 300, 150, 56, "節点 j の応答 y_j", (225, 235, 245), FT)
    note(d, "各モードの最大応答 q_i にモード形 phi_ji を掛けて足し合わせる")
    save(im, "v1e9ResponseSpectrumBasis")


# ================================================ 9-18 SRSS結合 (helpful)
def f_srss_combination():
    im, d = new(); title(d, "モード結合:絶対値和(過大評価) と SRSS の比較")
    # component bars
    ox, oy = 110, 320; bw = 46; gap = 22
    comps = [3.0, 2.4, 1.6]
    for i, v in enumerate(comps):
        x = ox + i * (bw + gap)
        h = v / 4.0 * 180
        d.rectangle((x, oy - h, x + bw, oy), outline=BLACK, width=2, fill=FILL2)
        ctext(d, x + bw / 2, oy - h - 14, "%.1f" % v, FT, GRAY)
        ctext(d, x + bw / 2, oy + 16, "q%d" % (i + 1), FT)
    d.line((ox - 10, oy, ox + 3 * (bw + gap), oy), fill=BLACK, width=2)
    # absolute sum bar
    absum = sum(comps)
    srss = math.sqrt(sum(v * v for v in comps))
    bx = 400
    d.rectangle((bx, oy - absum / 8.0 * 180, bx + 60, oy), outline=BLACK, width=2, fill=(245, 225, 225))
    ctext(d, bx + 30, oy - absum / 8.0 * 180 - 14, "%.1f" % absum, FT, RED)
    ctext(d, bx + 30, oy + 16, "絶対値和", FT, RED)
    ctext(d, bx + 30, oy + 36, "(過大)", FT, RED)
    bx2 = 520
    d.rectangle((bx2, oy - srss / 8.0 * 180, bx2 + 60, oy), outline=BLACK, width=2, fill=(225, 240, 225))
    ctext(d, bx2 + 30, oy - srss / 8.0 * 180 - 14, "%.2f" % srss, FT, GREEN)
    ctext(d, bx2 + 30, oy + 16, "SRSS", FT, GREEN)
    ctext(d, bx2 + 30, oy + 36, "sqrt(sum q^2)", FT, GREEN)
    note(d, "各モードが同時最大にはならない -> SRSSが現実的")
    save(im, "v1e9SrssCombination")


# ================================================ 9-19 加速度応答スペクトル軸 (helpful)
def f_accel_spectrum_axes():
    im, d = new(); title(d, "加速度応答スペクトル:横軸=固有周期T 縦軸=最大絶対加速度 (z別)")
    ox, oy = 95, 345; xr, ym = 480, 255
    X = lambda T: ox + T / 3.0 * xr
    axes(d, ox, oy, xr + 30, ym + 25, "固有周期 T [s]", "最大絶対加速度")
    def spec(T, z):
        # illustrative shape: rises then plateau then decays, damping lowers it
        base = 3.0 / (1 + ((T - 0.4) / 0.35) ** 2) + 0.6
        return base * (0.5 / (0.5 + z))
    Y = lambda a: oy - min(a, 3.5) / 3.5 * ym
    for z, col in [(0.02, BLUE), (0.05, GREEN), (0.10, ORANGE)]:
        pts = [(X(i / 100.0), Y(spec(i / 100.0, z))) for i in range(2, 300)]
        plot(d, 0, 0, pts, col, 3)
        ctext(d, X(1.6), Y(spec(1.6, z)) - 10, "z=%.2f" % z, FT, col, "lm")
    note(d, "減衰比 z が大きいほどスペクトル値は下がる")
    save(im, "v1e9AccelSpectrumAxes")


# ================================================ 9-20 近接モードのSRSS誤差 (helpful)
def f_srss_close_modes():
    im, d = new(); title(d, "近接する2モード:相関が大きく SRSS では誤差")
    ox, oy = 90, 345; xr, ym = 500, 255
    X = lambda w: ox + w / 3.0 * xr
    def peak(w0, h, wdt):
        return lambda w: h / (1 + ((w - w0) / wdt) ** 2)
    axes(d, ox, oy, xr + 30, ym + 25, "w", "応答")
    p1 = peak(1.45, 6.0, 0.10)
    p2 = peak(1.60, 5.5, 0.10)
    Y = lambda a: oy - min(a, 9) / 9 * ym
    c1 = [(X(i / 100.0), Y(p1(i / 100.0))) for i in range(10, 300)]
    c2 = [(X(i / 100.0), Y(p2(i / 100.0))) for i in range(10, 300)]
    plot(d, 0, 0, c1, BLUE, 2); plot(d, 0, 0, c2, GREEN, 2)
    dsh(d, X(1.45), oy, X(1.45), oy - ym, LGRAY)
    dsh(d, X(1.60), oy, X(1.60), oy - ym, LGRAY)
    ctext(d, X(1.35), 110, "w1", FT, BLUE); ctext(d, X(1.70), 110, "w2", FT, GREEN)
    ctext(d, 470, 150, "固有振動数が近い", FT, GRAY, "mm")
    ctext(d, 470, 178, "-> モード相関大", FT, RED, "mm")
    ctext(d, 470, 206, "-> 単純SRSSは不正確", FT, RED, "mm")
    note(d, "近接モードは CQC など相関を考慮した結合が必要")
    save(im, "v1e9SrssCloseModes")


# ================================================ 9-21 最大応答の意味 (helpful)
def f_max_response_meaning():
    im, d = new(); title(d, "各節点変位の包絡線から節点ごと最大値を抽出(発生時刻はバラバラ)")
    ox, oy = 90, 220
    arrow(d, ox, oy, ox + 520, oy, BLACK, 2, 11); ctext(d, ox + 526, oy, "t", FS, BLACK, "lm")
    arrow(d, ox, oy + 140, ox, oy - 140, BLACK, 2, 11); ctext(d, ox - 10, oy - 148, "変位", FS, BLACK, "rm")
    # three node waveforms peaking at different times
    specs = [(110, 130, BLUE, "節点1", 90), (95, 190, GREEN, "節点2", 150), (75, 250, ORANGE, "節点3", 300)]
    for amp, period, col, lab, tpk in specs:
        pts = [(ox + t, oy - amp * math.sin(2 * math.pi * t / period)) for t in range(0, 501)]
        plot(d, 0, 0, pts, col, 2)
        # mark max within window
        # find peak nearest tpk
        d.line((ox + tpk, oy, ox + tpk, oy - amp), fill=col, width=1)
        node(d, ox + tpk, oy - amp, 5, col, col)
        ctext(d, ox + tpk, oy - amp - 12, lab + " max", FT, col)
    note(d, "最大応答は節点ごとに別時刻で発生 -> 同時刻の分布ではない")
    save(im, "v1e9MaxResponseMeaning")


# ================================================ 9-22 乗り心地PSD (helpful)
def f_ride_comfort_psd():
    im, d = new(); title(d, "乗り心地:軌道不整PSD -> 車輪加速度 P_i -> |H|^2 -> 車体 P_0")
    flowbox(d, 110, 150, 140, 60, "軌道不整\nPSD S(f)", (225, 235, 245), FT)
    arrow(d, 180, 150, 245, 150, BLACK, 3, 12)
    flowbox(d, 320, 150, 140, 60, "車輪入力 P_i", (245, 240, 225), FT)
    arrow(d, 390, 150, 455, 150, BLACK, 3, 12)
    flowbox(d, 530, 150, 130, 60, "伝達 |H|^2", (225, 240, 225), FT)
    arrow(d, 530, 185, 530, 250, BLACK, 3, 12)
    flowbox(d, 530, 290, 150, 60, "車体応答 P_0", (245, 230, 230), FT)
    ctext(d, 330, 250, "P_0(f) = |H(f)|^2 P_i(f)", FS, GRAY)
    # small psd curve
    ox, oy = 120, 360; xr, ym = 300, 70
    axes(d, ox, oy, xr, ym + 10, "f", "PSD")
    pts = [(ox + t, oy - ym * math.exp(-((t - 90) / 60) ** 2)) for t in range(0, xr)]
    plot(d, 0, 0, pts, BLUE, 2)
    save(im, "v1e9RideComfortPsd")


# ================================================ 9-23 流体の部分構造 (required)
def f_substructure_fluid():
    im, d = new(); title(d, "水中構造の部分構造分割:境界結合+各節点に付加質量")
    # water region
    d.rectangle((90, 150, 570, 340), outline=None, fill=(224, 238, 248))
    for wy in (170, 200, 230):
        pts = [(90 + t, wy + 6 * math.sin(t / 22)) for t in range(0, 481, 6)]
        plot(d, 0, 0, pts, (150, 190, 220), 1)
    ctext(d, 130, 165, "流体(水)", FT, (60, 110, 160))
    # structure split into two substructures
    box(d, 250, 180, 340, 320, FILL1)
    box(d, 340, 180, 430, 320, FILL2)
    ctext(d, 295, 250, "部分A", FT)
    ctext(d, 385, 250, "部分B", FT)
    # boundary interface nodes
    for yy in (200, 250, 300):
        node(d, 340, yy, 6, RED, RED)
    ctext(d, 340, 165, "境界(結合)", FT, RED)
    # added mass arrows on surface nodes
    for (nx, ny) in [(250, 210), (250, 290), (430, 210), (430, 290)]:
        node(d, nx, ny, 5, "white", BLACK)
        s = -1 if nx < 340 else 1
        arrow(d, nx, ny, nx + s * 30, ny, BLUE, 2, 9)
    ctext(d, 330, 360, "各節点に付加質量(流体の慣性) を付与", FT, BLUE)
    note(d, "構造を部分構造に分け境界で結合、流体は付加質量で表現")
    save(im, "v1e9SubstructureFluid")


# ================================================ 9-24 はり要素の応力精度 (helpful)
def f_beam_stress_accuracy():
    im, d = new(); title(d, "応力分布:はり要素(粗) と シェル/ソリッド(断面変形を捕捉)")
    # left: beam element - linear stress across depth
    ox = 130; cy = 230; hh = 90
    d.line((ox, cy - hh, ox, cy + hh), fill=BLACK, width=2)  # section line
    ctext(d, ox, cy - hh - 20, "はり要素(粗)", FT, BLUE)
    # linear distribution
    for k in range(-hh, hh + 1, 18):
        L = 80 * (k / hh)
        d.line((ox, cy + k, ox + L, cy + k), fill=BLUE, width=2)
    d.line((ox + 80, cy - hh, ox - 80, cy + hh), fill=BLUE, width=3)
    ctext(d, ox + 40, cy + hh + 24, "線形(平面保持)", FT, GRAY)
    d.line((330, 110, 330, 360), fill=LGRAY, width=1)
    # right: shell/solid - nonlinear (warping / stress concentration)
    ox2 = 470
    d.line((ox2, cy - hh, ox2, cy + hh), fill=BLACK, width=2)
    ctext(d, ox2, cy - hh - 20, "シェル/ソリッド", FT, RED)
    pts = []
    for k in range(-hh, hh + 1, 6):
        t = k / hh
        L = 80 * (t + 0.35 * math.sin(math.pi * t) * (1 - abs(t)))  # curved profile
        pts.append((ox2 + L, cy + k))
    plot(d, 0, 0, pts, RED, 3)
    for k in range(-hh, hh + 1, 18):
        t = k / hh
        L = 80 * (t + 0.35 * math.sin(math.pi * t) * (1 - abs(t)))
        d.line((ox2, cy + k, ox2 + L, cy + k), fill=RED, width=2)
    ctext(d, ox2 + 40, cy + hh + 24, "断面変形/応力集中", FT, GRAY)
    note(d, "はり要素は断面の局所変形を表せず 応力を過小評価しうる")
    save(im, "v1e9BeamStressAccuracy")


# ================================================ 9-25 バルブ位相設定 (required)
def f_phase_valve_setup():
    im, d = new(); title(d, "加振点と バルブ a(位相0) ・ b(位相90) の変位波形(設定)")
    # structure schematic
    d.line((110, 130, 550, 130), fill=BLACK, width=5)
    wall(d, 110, 110, 175, side=1, n=3)
    # excitation point
    ax = 180
    force(d, ax, 105, 0, 34, "加振", RED)
    node(d, ax, 130, 6, RED, RED)
    # valve a and b positions
    va, vb = 330, 480
    node(d, va, 130, 7, FILL1, BLUE); ctext(d, va, 112, "a", FT, BLUE)
    node(d, vb, 130, 7, FILL1, GREEN); ctext(d, vb, 112, "b", FT, GREEN)
    # displacement waveforms below
    def wf(ox, ph, col, lab):
        oy = 260; w = 130; amp = 40
        arrow(d, ox, oy, ox + w + 14, oy, BLACK, 2, 9)
        pts = [(ox + w * t, oy - amp * math.sin(2 * math.pi * 1.2 * t + ph)) for t in [i / 60 for i in range(61)]]
        plot(d, 0, 0, pts, col, 2)
        ctext(d, ox + w / 2, oy + 46, lab, FT, col)
    wf(180, 0.0, BLUE, "a:位相0")
    wf(400, math.pi / 2, GREEN, "b:位相90")
    dsh(d, va, 140, 245, 220, LGRAY)
    dsh(d, vb, 140, 465, 220, LGRAY)
    note(d, "各点の変位波形の位相差(0 と 90)が与えられた設定")
    save(im, "v1e9PhaseValveSetup")


# ================================================ 9-26 シート骨格の位相 (required)
def f_seat_frame_phase():
    im, d = new(); title(d, "シート骨格の点a-d と 各Y変位波形(0/90/180/-90)")
    # seat frame (L-ish side view)
    d.line((160, 320, 160, 170), fill=BLACK, width=6)   # backrest
    d.line((160, 320, 340, 320), fill=BLACK, width=6)   # seat pan
    d.line((340, 320, 360, 360), fill=BLACK, width=4)   # front leg
    d.line((175, 320, 175, 360), fill=BLACK, width=4)   # rear leg
    pts = {"a": (160, 175), "b": (250, 320), "c": (340, 320), "d": (160, 250)}
    cols = {"a": BLUE, "b": GREEN, "c": ORANGE, "d": RED}
    for k, (x, y) in pts.items():
        node(d, x, y, 7, FILL1, cols[k]); ctext(d, x - 14, y - 12, k, FT, cols[k])
    # waveforms on right with given phases
    phases = {"a": 0.0, "b": math.pi / 2, "c": math.pi, "d": -math.pi / 2}
    labels = {"a": "0", "b": "90", "c": "180", "d": "-90"}
    bx = 430; by = 120; w = 170; amp = 22; dy = 66
    for i, k in enumerate(["a", "b", "c", "d"]):
        oy = by + i * dy
        arrow(d, bx, oy, bx + w + 12, oy, BLACK, 2, 8)
        wf = [(bx + w * t, oy - amp * math.sin(2 * math.pi * 1.3 * t + phases[k])) for t in [j / 60 for j in range(61)]]
        plot(d, 0, 0, wf, cols[k], 2)
        ctext(d, bx - 10, oy, k, FT, cols[k], "rm")
        ctext(d, bx + w + 20, oy, labels[k], FT, cols[k], "lm")
    ctext(d, bx + w / 2, by - 26, "Y変位波形(位相)", FT, GRAY)
    note(d, "各点のY変位の位相関係(0/90/180/-90)が与えられている")
    save(im, "v1e9SeatFramePhase")


if __name__ == "__main__":
    f_mac_definition()
    f_mode_orthogonality()
    f_mac_matrix()
    f_mac_calc_result()
    f_frf_modal_peak()
    f_craig_bampton_setup()
    f_guyan_setup()
    f_cantilever_section()
    f_material_scaling()
    f_lframe_load()
    f_washing_machine()
    f_motor_rpm_resonance()
    f_panel_gravity_sag()
    f_strain_energy_share()
    f_gear_mesh_spectrum()
    f_two_input_system()
    f_response_spectrum_basis()
    f_srss_combination()
    f_accel_spectrum_axes()
    f_srss_close_modes()
    f_max_response_meaning()
    f_ride_comfort_psd()
    f_substructure_fluid()
    f_beam_stress_accuracy()
    f_phase_valve_setup()
    f_seat_frame_phase()
    print("=== done 26 figures ===")
