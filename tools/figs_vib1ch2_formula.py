# -*- coding: utf-8 -*-
"""振動1級 第2章「振動工学」公式・用語図 24枚。figlibで白地660x420線画。
文字化け回避のためギリシャ文字は英字表記(wn/wd/z/eta/tau等)に置換。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=10, gap=7):
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


def fbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ls = text.split("\n")
    for i, line in enumerate(ls):
        ctext(d, cx, cy - (len(ls) - 1) * 10 + i * 20, line, fnt)


def mass(d, cx, cy, w, h, label="m", fill=FILL2):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ctext(d, cx, cy, label, F)


def damper(d, x1, y, x2, y2=None, wd=3):
    """ダッシュポット(減衰器)を水平/斜めに描く。"""
    y2 = y if y2 is None else y2
    dx = x2 - x1; dy = y2 - y; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    px, py = -uy, ux
    m1 = (x1 + ux * L * 0.42, y + uy * L * 0.42)
    m2 = (x1 + ux * L * 0.58, y + uy * L * 0.58)
    d.line((x1, y, m1[0], m1[1]), fill=BLACK, width=wd)
    # cylinder (open box)
    s = 15
    c1 = (m2[0] + px * s, m2[1] + py * s); c2 = (m2[0] - px * s, m2[1] - py * s)
    e1 = (m1[0] + px * s, m1[1] + py * s); e2 = (m1[0] - px * s, m1[1] - py * s)
    d.line((e1[0], e1[1], c1[0], c1[1]), fill=BLACK, width=wd)
    d.line((e2[0], e2[1], c2[0], c2[1]), fill=BLACK, width=wd)
    d.line((c1[0], c1[1], c2[0], c2[1]), fill=BLACK, width=wd)
    # piston
    p1 = (m1[0] + px * s * 0.7, m1[1] + py * s * 0.7)
    p2 = (m1[0] - px * s * 0.7, m1[1] - py * s * 0.7)
    d.line((p1[0], p1[1], p2[0], p2[1]), fill=BLACK, width=wd)
    d.line((m1[0], m1[1], x2, y2), fill=BLACK, width=wd)


# 1. Damped SDOF: m-c-k, c_c=2sqrt(mk)
def f_dampedsdof():
    im, d = new()
    title(d, "減衰系1自由度 (c_c=2sqrt(mk))")
    hwall(d, 210, 450, 90, 1)
    # spring left, damper right, both from ceiling to mass
    spring(d, 250, 90, 250, 210)
    damper(d, 410, 90, 410, 210)
    ctext(d, 220, 150, "k", FS, BLACK, "rm")
    ctext(d, 440, 150, "c", FS, BLACK, "lm")
    mass(d, 330, 250, 120, 70, "m")
    force(d, 330, 285, 0, 55, "x", BLUE)
    ctext(d, 330, 360, "c_c=2sqrt(mk),  z=c/c_c,  wn=sqrt(k/m)", FT, GRAY)
    note(d, "wd=wn*sqrt(1-z^2)  (減衰固有角振動数)")
    save(im, "v1f2DampedSDOF")


# 2. Response magnification curve for various z
def f_responsemag():
    im, d = new()
    title(d, "応答倍率 Md の周波数応答 (z別)")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 280, "w/wn", "Md")
    d.line((ox + 130, oy + 5, ox + 130, oy - 5), fill=BLACK, width=2)
    ctext(d, ox + 130, oy + 16, "1", FT, BLACK)
    for z, col, lab in [(0.10, RED, "z=0.1"), (0.25, ORANGE, "z=0.25"), (0.5, BLUE, "z=0.5")]:
        pts = []
        for i in range(0, 241):
            r = i / 100.0
            Md = 1.0 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
            py = oy - min(Md, 5.2) / 5.5 * 280
            pts.append((ox + i / 240 * 470, py))
        plot(d, 0, 0, pts, col, 3)
        ctext(d, ox + 300, oy - (1.0 / (2 * z)) / 5.5 * 280 - 14, lab, FT, col, "lm")
    note(d, "z小ほど共振ピークが高く鋭い。z=1/sqrt2 でピーク消失")
    save(im, "v1f2ResponseMagnification")


# 3. Resonance peak location w=wn*sqrt(1-2z^2)
def f_resonancepeak():
    im, d = new()
    title(d, "共振点 w=wn*sqrt(1-2z^2)")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 280, "w/wn", "Md")
    z = 0.2
    pts = []; peak = None
    for i in range(0, 241):
        r = i / 100.0
        Md = 1.0 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
        py = oy - min(Md, 3.2) / 3.5 * 280
        pts.append((ox + i / 240 * 470, py))
        if peak is None or Md > peak[2]:
            peak = (ox + i / 240 * 470, py, Md)
    plot(d, 0, 0, pts, BLUE, 3)
    rp = math.sqrt(1 - 2 * z * z)
    xp = ox + rp * 100 / 240 * 470
    dash(d, xp, oy, xp, peak[1], RED)
    dash(d, ox, peak[1], xp, peak[1], RED)
    node(d, peak[0], peak[1], 5, RED, RED)
    ctext(d, xp, oy + 16, "sqrt(1-2z^2)", FT, RED)
    ctext(d, ox + 40, peak[1] - 14, "ピーク倍率\n1/(2z sqrt(1-z^2))", FT, RED, "lm")
    note(d, "共振点は wn より僅かに低周波側(減衰があるほど左へ)")
    save(im, "v1f2ResonancePeak")


# 4. Q factor: sharpness, half-power bandwidth
def f_qfactor():
    im, d = new()
    title(d, "Q値 Q~1/(2z) と半値幅 dw")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 280, "w", "|Md|")
    z = 0.12
    pts = []; peak = None
    for i in range(0, 241):
        r = i / 100.0
        Md = 1.0 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
        py = oy - min(Md, 4.4) / 4.7 * 280
        pts.append((ox + i / 240 * 470, py))
        if peak is None or Md > peak[3]:
            peak = (i, ox + i / 240 * 470, py, Md)
    plot(d, 0, 0, pts, BLUE, 3)
    # half power line at peak/sqrt2
    hp = peak[3] / math.sqrt(2)
    hy = oy - hp / 4.7 * 280
    # find crossing indices
    xs = []
    for i in range(0, 241):
        r = i / 100.0
        Md = 1.0 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
        if abs(Md - hp) < 0.08 and (not xs or i - (xs[-1]) > 10):
            xs.append(i)
    dash(d, ox, hy, ox + 470, hy, GRAY)
    ctext(d, ox + 476, hy, "peak/sqrt2", FT, GRAY, "lm")
    if len(xs) >= 2:
        x1 = ox + xs[0] / 240 * 470; x2 = ox + xs[-1] / 240 * 470
        dim(d, x1, hy - 24, x2, hy - 24, "dw", col=RED)
    node(d, peak[1], peak[2], 5, RED, RED)
    ctext(d, peak[1] + 8, peak[2] - 10, "鋭いほどQ大", FT, RED, "lm")
    note(d, "Q = wn/dw ~ 1/(2z)。半値幅 dw が狭いほど鋭い共振")
    save(im, "v1f2QFactor")


# 5. Transmissibility: base excitation, isolation above sqrt2 wn
def f_transmissibility():
    im, d = new()
    title(d, "変位伝達率 (基礎加振・sqrt2 wn 超で絶縁)")
    # small model top-left
    hwall(d, 40, 150, 70, 1)
    spring(d, 70, 70, 70, 150); damper(d, 130, 70, 130, 150)
    mass(d, 100, 185, 90, 50, "m")
    arrow(d, 40, 110, 40, 150, GREEN, 3, 10); ctext(d, 26, 130, "y", FT, GREEN)
    arrow(d, 155, 185, 155, 220, BLUE, 3, 10); ctext(d, 168, 205, "x", FT, BLUE)
    # curve
    ox, oy = 230, 350
    axes(d, ox, oy, 400, 250, "w/wn", "Tr")
    r2 = math.sqrt(2.0)
    x2p = ox + r2 * 100 / 300 * 400
    dash(d, x2p, oy, x2p, oy - 250, GRAY); ctext(d, x2p, oy + 16, "sqrt2", FT, GRAY)
    dash(d, ox, oy - 1.0 / 3.3 * 250, ox + 400, oy - 1.0 / 3.3 * 250, LGRAY)
    ctext(d, ox + 405, oy - 1.0 / 3.3 * 250, "Tr=1", FT, GRAY, "lm")
    z = 0.1
    pts = []
    for i in range(0, 301):
        r = i / 100.0
        Tr = math.sqrt((1 + (2 * z * r) ** 2) / ((1 - r * r) ** 2 + (2 * z * r) ** 2))
        py = oy - min(Tr, 3.3) / 3.3 * 250
        pts.append((ox + i / 300 * 400, py))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 300, oy - 40, "絶縁域\n(Tr<1)", FT, GREEN)
    note(d, "w > sqrt2*wn で伝達率<1=振動絶縁。ばねを柔らかく(wn小)")
    save(im, "v1f2Transmissibility")


# 6. Dynamic absorber
def f_dynamicabsorber():
    im, d = new()
    title(d, "動吸振器 (ka=ma*w^2 で主系静止)")
    hwall(d, 210, 450, 70, 1)
    spring(d, 250, 70, 250, 150); ctext(d, 224, 110, "k", FT, BLACK, "rm")
    damper(d, 410, 70, 410, 150); ctext(d, 436, 110, "c", FT, BLACK, "lm")
    mass(d, 330, 185, 150, 70, "M (主系)")
    force(d, 250, 185, 0, -60, "F sin wt", RED)
    # absorber below
    spring(d, 330, 220, 330, 285); ctext(d, 356, 252, "ka", FT, BLUE, "lm")
    mass(d, 330, 315, 90, 55, "ma", (225, 235, 245))
    ctext(d, 330, 375, "同調 wa=sqrt(ka/ma)=w のとき主系振幅=0", FT, GRAY)
    note(d, "付加系が逆位相で反力を出し、加振力を打ち消す")
    save(im, "v1f2DynamicAbsorber")


# 7. Vibration recorder / pickup
def f_vibrecorder():
    im, d = new()
    title(d, "振動計 (変位計 wn<<w / 加速度計 wn>>w)")
    hwall(d, 60, 300, 70, 1)
    spring(d, 100, 70, 100, 150); damper(d, 250, 70, 250, 150)
    mass(d, 175, 185, 150, 55, "おもり m")
    ctext(d, 175, 240, "相対変位を記録", FT, GRAY)
    # two regime boxes
    fbox(d, 480, 150, 300, 70, "wn << w (柔ばね)\n= 変位計\nおもりは静止し基礎変位を測る", (225, 235, 245), FT)
    fbox(d, 480, 290, 300, 70, "wn >> w (剛ばね)\n= 加速度計\n相対変位 ~ 加速度に比例", (225, 240, 225), FT)
    note(d, "測定周波数と器械固有振動数 wn の大小で用途が決まる")
    save(im, "v1f2VibrationRecorder")


# 8. Modal mass / stiffness quadratic form
def f_modalmassstiff():
    im, d = new()
    title(d, "モード質量・剛性 (phi^T M phi)")
    # phi^T  [M]  phi arrangement
    y = 190
    ctext(d, 110, y, "phi_r^T", F, BLUE)
    matrix_grid(d, 170, y - 78, [["M", "", ""], ["", "M", ""], ["", "", "M"]], cell=52)
    ctext(d, 350, y, "phi_r", F, BLUE)
    ctext(d, 420, y, "=", F)
    fbox(d, 510, y, 120, 60, "mr\n(スカラ)", (225, 235, 245), FS)
    ctext(d, 330, 330, "mr=phi_r^T M phi_r,   kr=phi_r^T K phi_r", FS, BLACK)
    note(d, "モードベクトルで挟む二次形式=そのモードの等価質量・剛性")
    save(im, "v1f2ModalMassStiffness")


# 9. Modal frequency & mass normalization
def f_modalfreqnorm():
    im, d = new()
    title(d, "モード角振動数 wr=sqrt(kr/mr) と質量正規化")
    fbox(d, 330, 120, 420, 50, "wr = sqrt( kr / mr )", (225, 240, 225), F)
    arrow(d, 330, 148, 330, 200, BLACK, 2, 11)
    ctext(d, 430, 174, "mr=1 に規格化", FT, RED, "lm")
    fbox(d, 330, 235, 460, 56, "質量正規化: phi^T M phi = 1\n=> kr = wr^2", (225, 235, 245), FS)
    fbox(d, 330, 340, 460, 46, "[M] -> I,  [K] -> diag(wr^2)", FILL1, FS)
    save(im, "v1f2ModalFreqNorm")


# 10. Orthogonality of modes
def f_orthogonality():
    im, d = new()
    title(d, "モードの直交性 (i!=j で内積0)")
    matrix_grid(d, 120, 130, [["x", "0", "0"], ["0", "x", "0"], ["0", "0", "x"]], cell=56,
                fnt=F)
    ctext(d, 300, 214, "phi_i^T M phi_j", FS, BLUE)
    ctext(d, 300, 158, "= 0  (i!=j)", FS, RED)
    ctext(d, 300, 186, "= mi (i=j)", FS, BLACK)
    ctext(d, 330, 340, "異なるモードは [M],[K] に関して直交 -> 連立が対角化", FT, GRAY)
    note(d, "各モードが独立=1自由度問題の重ね合わせに分解できる")
    save(im, "v1f2Orthogonality")


# 11. Rigid body mode w=0
def f_rigidbodymode():
    im, d = new()
    title(d, "剛体モード w=0 (拘束のない自由系)")
    # two disks connected by shaft, rotating together
    cy = 210
    for cx in (220, 440):
        d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), outline=BLACK, width=3, fill=FILL1)
        node(d, cx, cy, 6)
    d.line((220, cy, 440, cy), fill=BLACK, width=6)
    ctext(d, 220, cy + 78, "円板1", FT, BLACK); ctext(d, 440, cy + 78, "円板2", FT, BLACK)
    # both same-direction rotation arrows
    for cx in (220, 440):
        d.arc((cx - 72, cy - 72, cx + 72, cy + 72), -60, 60, fill=RED, width=3)
        arrow(d, cx + 72 * math.cos(math.radians(60)), cy - 72 * math.sin(math.radians(60)),
              cx + 78, cy - 20, RED, 3, 11)
    ctext(d, 330, 330, "一体で同方向回転 -> 変形なし・復元力0 -> w=0", FT, GRAY)
    note(d, "自由系(非拘束)には剛体運動に対応するゼロ固有値が現れる")
    save(im, "v1f2RigidBodyMode")


# 12. Mode superposition
def f_modesuperposition():
    im, d = new()
    title(d, "モード重ね合わせ (共振で分母->0)")
    ox = 90
    # three 1-dof responses summed
    for i, (col, lab) in enumerate([(RED, "1次"), (BLUE, "2次"), (GREEN, "3次")]):
        y = 120 + i * 55
        fbox(d, ox + 90, y, 150, 40,
             "qr", col if False else FILL1, FS)
        ctext(d, ox + 90, y, "q%d(t)" % (i + 1), FS, col)
        arrow(d, ox + 175, y, ox + 260, 175, BLACK, 2, 10)
    fbox(d, ox + 380, 175, 200, 56, "x(t)=Sum phi_r qr(t)", (225, 235, 245), FS)
    fbox(d, 330, 310, 520, 60,
         "qr(t) ~ Fr / (kr - w^2 mr)\n分母 -> 0 (w->wr) で共振", (245, 235, 235), FS)
    note(d, "全体応答=各モードの1自由度応答の線形和")
    save(im, "v1f2ModeSuperposition")


# 13. Compliance FRF with residuals
def f_compliance():
    im, d = new()
    title(d, "コンプライアンスFRFと剰余(Z,Y)")
    ox, oy = 100, 330
    axes(d, ox, oy, 470, 270, "w", "|H|")
    # FRF with two peaks
    z = 0.05
    pts = []
    for i in range(0, 471):
        w = 0.2 + i / 470 * 4.0
        H = 0.0
        for wr, a in [(1.0, 1.0), (2.6, 0.6)]:
            H += a / math.sqrt((wr * wr - w * w) ** 2 + (2 * z * wr * w) ** 2)
        py = oy - min(H, 3.0) / 3.2 * 270
        pts.append((ox + i / 470 * 470, py))
    plot(d, 0, 0, pts, BLUE, 3)
    # residual bands
    dash(d, ox, oy - 40, ox + 90, oy - 40, GREEN)
    ctext(d, ox + 4, oy - 54, "剰余剛性 Z (低域)", FT, GREEN, "lm")
    dash(d, ox + 380, oy - 30, ox + 470, oy - 30, ORANGE)
    ctext(d, ox + 300, oy - 44, "剰余質量 Y (高域)", FT, ORANGE, "lm")
    note(d, "帯域外モードの寄与を Z(剛性的)・Y(質量的)で補正し打切り誤差を減らす")
    save(im, "v1f2Compliance")


# 14. Rayleigh damping [C]=a[M]+b[K]
def f_rayleighdamping():
    im, d = new()
    title(d, "レイリー減衰 [C]=a[M]+b[K]")
    ox, oy = 100, 330
    axes(d, ox, oy, 470, 260, "wr", "zr")
    # alpha part: a/(2wr) decreasing
    p1 = []; p2 = []; ps = []
    a, b = 0.5, 0.02
    for i in range(1, 471):
        wr = 0.3 + i / 470 * 9.0
        za = a / (2 * wr); zb = b * wr / 2; zt = za + zb
        sc = 260 / 0.5
        p1.append((ox + i / 470 * 470, oy - min(za, 0.5) * sc))
        p2.append((ox + i / 470 * 470, oy - min(zb, 0.5) * sc))
        ps.append((ox + i / 470 * 470, oy - min(zt, 0.5) * sc))
    plot(d, 0, 0, p1, GREEN, 2); ctext(d, ox + 60, oy - 150, "a/(2wr) 低域", FT, GREEN, "lm")
    plot(d, 0, 0, p2, ORANGE, 2); ctext(d, ox + 300, oy - 150, "b*wr/2 高域", FT, ORANGE, "lm")
    plot(d, 0, 0, ps, RED, 3); ctext(d, ox + 200, oy - 230, "合計 zr", FT, RED, "lm")
    note(d, "質量比例a=低周波を、剛性比例b=高周波を減衰。2点で係数決定")
    save(im, "v1f2RayleighDamping")


# 15. Modal damping U-curve
def f_modaldamping():
    im, d = new()
    title(d, "モード減衰比 zr=a/(2wr)+b*wr/2")
    ox, oy = 100, 330
    axes(d, ox, oy, 470, 260, "wr", "zr")
    a, b = 0.6, 0.03
    ps = []
    for i in range(1, 471):
        wr = 0.3 + i / 470 * 9.0
        zt = a / (2 * wr) + b * wr / 2
        ps.append((ox + i / 470 * 470, oy - min(zt, 0.5) * 520))
    plot(d, 0, 0, ps, BLUE, 3)
    # minimum
    wmin = math.sqrt(a / b)
    xm = ox + (wmin - 0.3) / 9.0 * 470
    zmin = a / (2 * wmin) + b * wmin / 2
    node(d, xm, oy - min(zmin, 0.5) * 520, 5, RED, RED)
    dash(d, xm, oy, xm, oy - min(zmin, 0.5) * 520, RED)
    ctext(d, xm, oy + 16, "wr=sqrt(a/b)", FT, RED)
    ctext(d, ox + 380, oy - 210, "U字\n(両端で増加)", FT, GRAY)
    note(d, "中間周波で減衰最小、両端(低域/高域)で大きくなる")
    save(im, "v1f2ModalDamping")


# 16. Structural (hysteretic) damping loop + complex stiffness
def f_structuraldamping():
    im, d = new()
    title(d, "構造減衰: ヒステリシスループと複素剛性")
    ox, oy = 200, 220
    axes(d, ox, oy, 230, 150, "strain", "stress")
    axes(d, ox, oy, -180, -140)
    # ellipse hysteresis loop (tilted)
    pts = []
    A, B, tilt = 150, 55, 0.6
    for i in range(0, 121):
        t = i / 120 * 2 * math.pi
        ex = A * math.cos(t)
        sy = B * math.sin(t) + tilt * ex
        pts.append((ox + ex, oy - sy))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 120, oy - 130, "面積=1サイクル\n散逸エネルギ", FT, RED, "lm")
    fbox(d, 500, 300, 250, 70, "複素剛性\nk*(1+ j*eta)\neta=損失係数", (225, 240, 225), FS)
    note(d, "減衰力が速度でなく変位に比例=履歴減衰。1サイクル損失は周波数に依らない")
    save(im, "v1f2StructuralDamping")


# 17. Complex mode / state space
def f_complexmode():
    im, d = new()
    title(d, "複素モード: 状態方程式化 (x, xdot)")
    fbox(d, 175, 140, 250, 70, "2次系\nM xdd + C xd + K x = f\n(N自由度)", FILL1, FT)
    arrow(d, 300, 140, 380, 140, BLACK, 2, 11); ctext(d, 340, 122, "状態化", FT, RED)
    fbox(d, 500, 140, 250, 70, "1次系\nz'=A z\nz=[x; xdot] (2N)", (225, 235, 245), FT)
    fbox(d, 330, 290, 560, 80,
         "固有値=複素共役対 (減衰・振動を含む)\nモードも複素 -> 節点位相がそろわない(進行波的)",
         (245, 235, 235), FS)
    note(d, "非比例減衰では実モードにならず、2N次の複素固有値問題になる")
    save(im, "v1f2ComplexMode")


# 18. Duffing hardening backbone
def f_duffing():
    im, d = new()
    title(d, "ダフィング系: 硬化ばね背骨曲線")
    ox, oy = 120, 340
    axes(d, ox, oy, 460, 280, "w", "振幅 a")
    # linear resonance dashed vertical
    x0 = ox + 0.30 * 460
    dash(d, x0, oy, x0, oy - 280, LGRAY); ctext(d, x0, oy + 16, "w0", FT, GRAY)
    # backbone bends to right (hardening)
    pts = []
    for i in range(0, 281):
        a = i / 280.0
        w = 0.30 + 0.55 * a * a  # frequency rises with amplitude
        pts.append((ox + w * 460, oy - a * 280))
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, ox + 330, oy - 240, "背骨曲線\n(高周波側へ傾く)", FT, RED, "lm")
    note(d, "硬化ばね(k3>0)は振幅増で固有振動数が上昇=共振が右へ倒れる")
    save(im, "v1f2Duffing")


# 19. Jump phenomenon
def f_jump():
    im, d = new()
    title(d, "跳躍現象・履歴 (上昇/下降で経路違い)")
    ox, oy = 120, 340
    axes(d, ox, oy, 460, 280, "w", "振幅 a")
    # bent resonance curve (multivalued)
    up = []; dn = []
    for i in range(0, 281):
        w = 0.15 + i / 280 * 0.8
        # implicit S curve approx: draw an overhanging peak
    # draw overhanging peak manually
    curve = []
    for i in range(0, 201):
        t = i / 200.0
        # parametric bent peak
        a = math.sin(t * math.pi)
        w = 0.2 + 0.55 * t + 0.12 * a  # lean right
        curve.append((ox + w * 460, oy - a * 250 - 10))
    plot(d, 0, 0, curve, BLUE, 3)
    # jump arrows
    xj1 = ox + 0.63 * 460
    arrow(d, xj1, oy - 235, xj1, oy - 90, RED, 3, 12)
    ctext(d, xj1 + 8, oy - 160, "下降跳躍", FT, RED, "lm")
    xj2 = ox + 0.40 * 460
    arrow(d, xj2, oy - 70, xj2, oy - 190, GREEN, 3, 12)
    ctext(d, xj2 - 8, oy - 130, "上昇跳躍", FT, GREEN, "rm")
    note(d, "多価領域で振幅が不連続にジャンプ。掃引方向で経路が異なる=履歴")
    save(im, "v1f2JumpPhenomenon")


# 20. Sub/super/sub-harmonic resonance spectrum
def f_subresonance():
    im, d = new()
    title(d, "副共振: 高調波・分数調波")
    ox, oy = 90, 320
    axes(d, ox, oy, 490, 250, "振動数", "振幅")
    wn_x = ox + 0.5 * 490
    dash(d, wn_x, oy, wn_x, oy - 250, LGRAY); ctext(d, wn_x, oy + 16, "wn", FT, GRAY)
    peaks = [(0.25, 90, GREEN, "w=wn/2\n分数調波"),
             (0.50, 200, RED, "w=wn\n主共振"),
             (0.75, 120, BLUE, "3w=... 高調波"),
             (1.0, 80, ORANGE, "nw~wn\n超調波")]
    for fx, h, col, lab in peaks:
        x = ox + fx * 490
        d.line((x, oy, x, oy - h), fill=col, width=4)
        ctext(d, x, oy - h - 16, lab, FT, col)
    note(d, "非線形系では nw~wn(高調波)や w/n~wn(分数調波)でも共振が現れる")
    save(im, "v1f2SubResonance")


# 21. Self-excited vibration, negative damping growing waveform
def f_selfexcited():
    im, d = new()
    title(d, "自励振動と負性減衰 (振幅が成長)")
    ox, oy = 90, 220
    arrow(d, ox, oy, ox + 500, oy, BLACK, 2, 11); ctext(d, ox + 506, oy, "t", FS, BLACK, "lm")
    arrow(d, ox, oy + 120, ox, oy - 140, BLACK, 2, 11); ctext(d, ox - 12, oy - 145, "x", FS, BLACK, "rm")
    pts = []
    for i in range(0, 501):
        t = i / 500 * 6 * math.pi
        env = 12 * math.exp(0.18 * t / (2 * math.pi))
        pts.append((ox + i, oy - env * math.sin(t)))
    plot(d, 0, 0, pts, RED, 2)
    # envelope
    env_pts = [(ox + i, oy - 12 * math.exp(0.18 * (i / 500 * 6 * math.pi) / (2 * math.pi))) for i in range(0, 501)]
    dash(d, 0, 0, 0, 0)  # noop
    plot(d, 0, 0, env_pts, LGRAY, 2)
    ctext(d, ox + 360, oy - 110, "負性減衰で\n発散", FT, RED, "lm")
    note(d, "外部が一定でも系が自らエネルギを取り込む(負の実効減衰)=振幅増大")
    save(im, "v1f2SelfExcited")


# 22. Van der Pol limit cycle in phase plane
def f_vanderpol():
    im, d = new()
    title(d, "ファンデルポール: リミットサイクル")
    cx, cy = 330, 230
    axes(d, cx, cy, 190, 160)
    axes(d, cx, cy, -190, -160)
    ctext(d, cx + 200, cy, "x", FS, BLACK, "lm"); ctext(d, cx, cy - 168, "xdot", FS, BLACK)
    # integrate van der pol to show inward + outward spiral to closed orbit
    def vdp(x0, y0, col):
        mu = 1.0; dt = 0.02; x, y = x0, y0; pts = []
        for _ in range(1400):
            xd = y
            yd = mu * (1 - x * x) * y - x
            x += xd * dt; y += yd * dt
            pts.append((cx + x * 45, cy - y * 45))
        return pts
    plot(d, 0, 0, vdp(0.1, 0.1, GRAY), LGRAY, 2)   # spiral out
    plot(d, 0, 0, vdp(4.0, 0.0, GRAY), LGRAY, 2)    # spiral in
    plot(d, 0, 0, vdp(2.0, 0.0, RED)[-260:], RED, 3)  # closed orbit
    ctext(d, cx + 120, cy - 120, "閉軌道\n(周期解)", FT, RED, "lm")
    note(d, "内外どの初期値からも同一閉軌道へ収束=安定なリミットサイクル")
    save(im, "v1f2VanDerPol")


# 23. Regenerative chatter x(t) vs x(t-tau)
def f_regenerative():
    im, d = new()
    title(d, "再生びびり: x(t) と x(t-tau) の重畳")
    ox, oy = 90, 200
    arrow(d, ox, oy, ox + 500, oy, BLACK, 2, 11); ctext(d, ox + 506, oy, "刃先位置", FS, BLACK, "lm")
    # previous cut surface (wavy)
    prev = []; cur = []
    for i in range(0, 501):
        ph = i / 500 * 6 * math.pi
        prev.append((ox + i, oy + 40 - 20 * math.sin(ph)))
        cur.append((ox + i, oy + 40 - 22 * math.sin(ph - 1.1)))
    plot(d, 0, 0, prev, GRAY, 2); ctext(d, ox + 300, oy + 78, "前周: x(t-tau)", FT, GRAY, "lm")
    plot(d, 0, 0, cur, BLUE, 3); ctext(d, ox + 300, oy - 20, "今周: x(t)", FT, BLUE, "lm")
    # chip thickness variation arrows
    for i in (120, 250, 380):
        arrow(d, ox + i, oy + 40 - 20 * math.sin(i / 500 * 6 * math.pi),
              ox + i, oy + 40 - 22 * math.sin(i / 500 * 6 * math.pi - 1.1), RED, 2, 8)
    fbox(d, 330, 360, 560, 44, "位相差で切りくず厚が変動 -> 安定限界(SLD)を超えると発散", (245, 235, 235), FT)
    save(im, "v1f2Regenerative")


# 24. Parametric excitation / Mathieu instability tongue
def f_parametric():
    im, d = new()
    title(d, "係数励振(マシュー): w~2*w0 の不安定舌")
    # pendulum with moving pivot top-left
    px, py = 130, 90
    arrow(d, px, py - 40, px, py, RED, 3, 11); arrow(d, px, py + 30, px, py - 10, RED, 3, 11)
    ctext(d, px + 46, py - 8, "支点上下動\nw", FT, RED, "lm")
    d.line((px, py, px + 55, py + 100), fill=BLACK, width=3)
    node(d, px + 55, py + 100, 10, FILL2)
    ctext(d, px + 55, py + 128, "w0", FT, BLACK)
    # stability chart
    ox, oy = 300, 350
    axes(d, ox, oy, 330, 260, "w/w0", "励振振幅")
    x2 = ox + 0.5 * 330
    dash(d, x2, oy, x2, oy - 260, LGRAY); ctext(d, x2, oy + 16, "2", FT, GRAY)
    # tongue (V shape) at w/w0=2
    d.polygon([(x2, oy), (x2 - 40, oy - 240), (x2 + 40, oy - 240)], outline=RED, width=3, fill=(250, 232, 232))
    ctext(d, x2, oy - 150, "不安定舌", FT, RED)
    ctext(d, ox + 260, oy - 60, "安定", FT, GREEN)
    note(d, "主不安定領域は励振振動数が固有の約2倍(w~2*w0)で最も広く開く")
    save(im, "v1f2Parametric")


if __name__ == "__main__":
    f_dampedsdof(); f_responsemag(); f_resonancepeak(); f_qfactor()
    f_transmissibility(); f_dynamicabsorber(); f_vibrecorder(); f_modalmassstiff()
    f_modalfreqnorm(); f_orthogonality(); f_rigidbodymode(); f_modesuperposition()
    f_compliance(); f_rayleighdamping(); f_modaldamping(); f_structuraldamping()
    f_complexmode(); f_duffing(); f_jump(); f_subresonance()
    f_selfexcited(); f_vanderpol(); f_regenerative(); f_parametric()
    print("done v1f2 formula")
