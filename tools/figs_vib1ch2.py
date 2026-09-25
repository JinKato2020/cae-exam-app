# -*- coding: utf-8 -*-
"""振動1級 第2章「振動工学」問題図 45枚。figlibで白地660x420線画。
方針: 正確さ最優先・機構のみ・装飾禁止。数式ラベルはASCII(w,wn,wd,z=zeta,th=theta,eta,T0)で豆腐回避。
required図は答え(固有値・結論・正解の向き)を描かない。"""
import sys, math, os
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
        ctext(d, cx, cy - (len(ls) - 1) * 10 + i * 20, line, fnt)


def rot(px, py, cx, cy, ang):
    s, c = math.sin(ang), math.cos(ang)
    x, y = px - cx, py - cy
    return (cx + x * c - y * s, cy + x * s + y * c)


def curvepts(fn, x0, x1, n=80):
    return [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]


def wave(d, ox, oy, w, amp, cycles, env, col=BLUE, wd=2, n=260):
    pts = []
    for i in range(n + 1):
        t = i / n
        y = amp * env(t) * math.sin(2 * math.pi * cycles * t)
        pts.append((ox + t * w, oy - y))
    plot(d, 0, 0, pts, col, wd)


# ================================================ 2-1 やじろべえ (required)
def f_yajirobee():
    im, d = new(); title(d, "やじろべえ:支点O・重心G(下方a)・両端質点m(水平b)")
    Ox, Oy = 330, 135
    hwall(d, Ox - 60, Ox + 60, 100, side=-1, n=5)
    d.line((Ox, 100, Ox, Oy), fill=BLACK, width=2)
    node(d, Ox, Oy, 6); ctext(d, Ox - 16, Oy - 8, "O", FS, BLACK, "rm")
    b, a = 155, 150
    th = 0.16
    mL = rot(Ox - b, Oy, Ox, Oy, th); mR = rot(Ox + b, Oy, Ox, Oy, th)
    G = rot(Ox, Oy + a, Ox, Oy, th)
    # upright reference (dashed)
    dsh(d, Ox - b, Oy, Ox + b, Oy, LGRAY)
    dsh(d, Ox, Oy, Ox, Oy + a, LGRAY)
    # tilted body
    d.line((mL[0], mL[1], mR[0], mR[1]), fill=BLACK, width=4)
    d.line((Ox, Oy, G[0], G[1]), fill=BLACK, width=4)
    node(d, mL[0], mL[1], 11, FILL1); node(d, mR[0], mR[1], 11, FILL1)
    ctext(d, mL[0], mL[1] - 22, "m", FS); ctext(d, mR[0], mR[1] - 22, "m", FS)
    node(d, G[0], G[1], 9, FILL2); ctext(d, G[0] + 16, G[1], "G(重心)", FT, BLACK, "lm")
    ctext(d, (Ox + mR[0]) / 2 + 30, Oy + 6, "b", FT, GRAY)
    ctext(d, Ox + 14, Oy + a / 2, "a", FT, GRAY, "lm")
    angle_arc(d, Ox, Oy, 55, -90 + 0, -90 + math.degrees(th), "th", GRAY)
    note(d, "支点Oまわりの微小角 th で振動。重心Gは支点の下方 a")
    save(im, "v1e2YajirobeeMode")


# ================================================ 2-2 U字管 (required)
def f_utube():
    im, d = new(); title(d, "U字管の液柱振動(高低差 2x)")
    tw, lx, rx, top, bot = 20, 255, 405, 120, 335
    # tube outlines
    for cx in (lx, rx):
        d.line((cx - tw, top, cx - tw, bot), fill=BLACK, width=3)
        d.line((cx + tw, top, cx + tw, bot), fill=BLACK, width=3)
    d.line((lx - tw, bot, rx + tw, bot), fill=BLACK, width=3)
    d.line((lx + tw, bot - 2 * tw, rx - tw, bot - 2 * tw), fill=BLACK, width=3)
    neutral = 225; x = 45
    Ls, Rs = neutral - x, neutral + x
    # liquid fill
    d.rectangle((lx - tw + 2, Ls, lx + tw - 2, bot - 2), fill=(214, 232, 246), outline=None)
    d.rectangle((rx - tw + 2, Rs, rx + tw - 2, bot - 2), fill=(214, 232, 246), outline=None)
    d.rectangle((lx - tw + 2, bot - 2 * tw + 2, rx + tw - 2, bot - 2), fill=(214, 232, 246), outline=None)
    # redraw walls over fill
    for cx in (lx, rx):
        d.line((cx - tw, top, cx - tw, bot), fill=BLACK, width=3)
        d.line((cx + tw, top, cx + tw, bot), fill=BLACK, width=3)
    d.line((lx - tw, bot, rx + tw, bot), fill=BLACK, width=3)
    # surfaces
    d.line((lx - tw, Ls, lx + tw, Ls), fill=BLUE, width=3)
    d.line((rx - tw, Rs, rx + tw, Rs), fill=BLUE, width=3)
    # neutral level
    dsh(d, lx - 55, neutral, rx + 55, neutral, GRAY)
    ctext(d, lx - 60, neutral, "中立面", FT, GRAY, "rm")
    ctext(d, lx, Ls - 16, "+x", FT, RED); ctext(d, rx, Rs + 16, "-x", FT, RED)
    dim(d, rx + 60, Ls, rx + 60, Rs, "2x", col=GRAY)
    note(d, "一方がx上昇・他方がx下降 → 高低差は 2x")
    save(im, "v1e2UtubeColumn")


# ================================================ 2-3 応答倍率 (helpful)
def f_response_mag():
    im, d = new(); title(d, "応答倍率 Md の共鳴曲線(ピークは r<1 側)")
    ox, oy = 95, 345; xr, ym = 470, 255
    X = lambda r: ox + r / 2.0 * xr
    Y = lambda md: oy - min(md, 4.2) / 4.2 * ym
    axes(d, ox, oy, xr + 30, ym + 25, "r", "Md")
    dsh(d, X(1), oy, X(1), oy - ym, LGRAY); ctext(d, X(1) + 4, oy - ym + 14, "r=1", FT, GRAY, "lm")
    for z, col, lx in [(0.15, BLUE, 1.92), (0.35, GREEN, 1.42)]:
        pts = []
        for i in range(0, 201):
            r = i / 100.0
            md = 1 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
            pts.append((X(r), Y(md)))
        plot(d, 0, 0, pts, col, 3)
        ctext(d, X(lx), Y(1 / math.sqrt((1 - lx ** 2) ** 2 + (2 * z * lx) ** 2)) - 10,
              "z=%.2f" % z, FT, col, "lm")
    z = 0.15; rp = math.sqrt(1 - 2 * z * z); mp = 1 / (2 * z * math.sqrt(1 - z * z))
    dsh(d, X(rp), oy, X(rp), Y(mp), RED)
    node(d, X(rp), Y(mp), 5, RED, RED)
    ctext(d, X(rp) + 10, Y(mp) - 6, "ピーク rp=sqrt(1-2 z^2)<1", FT, RED, "lm")
    save(im, "v1e2ResponseMagnification")


# ================================================ 2-4 Q値と半値幅 (helpful)
def f_qfactor():
    im, d = new(); title(d, "共振の鋭さ Q と半値幅 dw  (Q = 1/2z)")
    ox, oy = 95, 345; xr, ym = 470, 255
    z = 0.09
    X = lambda r: ox + r / 2.0 * xr
    A = lambda r: 1 / math.sqrt((1 - r * r) ** 2 + (2 * z * r) ** 2)
    Amax = A(1.0)
    Y = lambda a: oy - a / (Amax * 1.15) * ym
    axes(d, ox, oy, xr + 30, ym + 25, "w/wn", "|H|")
    pts = [(X(i / 100.0), Y(A(i / 100.0))) for i in range(20, 201)]
    plot(d, 0, 0, pts, BLUE, 3)
    # peak Q
    dsh(d, X(1), oy, X(1), Y(Amax), LGRAY)
    ctext(d, X(1) + 8, Y(Amax) - 4, "Q = 1/2z", FT, RED, "lm")
    # half power line
    hp = Amax / math.sqrt(2)
    dsh(d, ox, Y(hp), X(1.7), Y(hp), RED)
    ctext(d, ox + 4, Y(hp) - 12, "Qmax/sqrt2", FT, RED, "lm")
    r1, r2 = math.sqrt(1 - 2 * z), math.sqrt(1 + 2 * z)
    dsh(d, X(r1), oy, X(r1), Y(hp), GRAY); dsh(d, X(r2), oy, X(r2), Y(hp), GRAY)
    dim(d, X(r1), Y(hp) + 26, X(r2), Y(hp) + 26, "dw", col=GRAY)
    ctext(d, X(1), oy + 16, "1", FT, GRAY)
    note(d, "半値幅 dw/wn = 2z → Q = wn/dw = 1/(2z)")
    save(im, "v1e2QFactorCurve")


# ================================================ 2-5 特性根 (helpful)
def f_char_roots():
    im, d = new(); title(d, "不足減衰系の特性根(複素平面)")
    cx, cy = 360, 220
    arrow(d, 120, cy, 610, cy, BLACK, 2, 11); ctext(d, 616, cy, "Re", FS, BLACK, "lm")
    arrow(d, cx, 380, cx, 70, BLACK, 2, 11); ctext(d, cx - 10, 62, "Im", FS, BLACK, "rm")
    sig, wd = 150, 110
    p1 = (cx - sig, cy - wd); p2 = (cx - sig, cy + wd)
    d.line((cx, cy, p1[0], p1[1]), fill=GRAY, width=2)
    d.line((cx, cy, p2[0], p2[1]), fill=GRAY, width=2)
    node(d, p1[0], p1[1], 6, RED, RED); node(d, p2[0], p2[1], 6, RED, RED)
    dsh(d, p1[0], cy, p1[0], p1[1], LGRAY)
    dsh(d, cx, p1[1], p1[0], p1[1], LGRAY)
    ctext(d, p1[0], cy + 16, "-z wn", FT, BLUE)
    ctext(d, cx - 8, p1[1], "+wd", FT, GREEN, "rm")
    ctext(d, cx - 8, p2[1], "-wd", FT, GREEN, "rm")
    r = math.hypot(sig, wd)
    ctext(d, (cx + p1[0]) / 2 - 10, (cy + p1[1]) / 2 - 12, "wn", FT, GRAY)
    ctext(d, 150, 100, "実部=減衰率 -z wn", FT, BLUE, "lm")
    ctext(d, 150, 124, "虚部=減衰固有 wd=wn sqrt(1-z^2)", FT, GREEN, "lm")
    save(im, "v1e2CharacteristicRoots")


# ================================================ 2-6 地震計 (required)
def f_seismograph():
    im, d = new(); title(d, "地震計:基礎に付けた質量m・ばねkと相対変位 z=x-y")
    # base frame attached to moving ground y
    hwall(d, 120, 540, 355, side=-1, n=14)
    ctext(d, 330, 378, "基礎(地面) 変位 y", FT, GRAY)
    # frame box moving with base
    fx0, fx1, fy0, fy1 = 210, 450, 150, 340
    d.line((fx0, fy0, fx0, fy1), fill=BLACK, width=3)
    d.line((fx1, fy0, fx1, fy1), fill=BLACK, width=3)
    d.line((fx0, fy0, fx1, fy0), fill=BLACK, width=3)
    d.line((fx0, fy1, fx1, fy1), fill=BLACK, width=3)
    # spring from top of frame to mass
    mcx, mcy = 330, 265
    spring(d, mcx, fy0 + 4, mcx, mcy - 26, coils=6, amp=13)
    ctext(d, mcx - 28, (fy0 + mcy) / 2, "k", FS, BLACK, "rm")
    box(d, mcx - 44, mcy - 26, mcx + 44, mcy + 26, FILL1)
    ctext(d, mcx, mcy, "m", F)
    # pointer / recorder
    d.line((mcx + 44, mcy, fx1 + 10, mcy), fill=BLACK, width=2)
    node(d, fx1 + 10, mcy, 4, RED, RED)
    ctext(d, fx1 + 16, mcy, "記録針", FT, GRAY, "lm")
    # absolute x of mass
    arrow(d, mcx, fy0 - 18, mcx + 40, fy0 - 18, BLUE, 2, 10)
    ctext(d, mcx + 46, fy0 - 18, "x(絶対変位)", FT, BLUE, "lm")
    # ground motion arrow
    arrow(d, 150, 355, 190, 355, GREEN, 3, 11)
    ctext(d, 170, 340, "y", FS, GREEN)
    note(d, "計器が記録するのは相対変位 z = x - y")
    save(im, "v1e2SeismographSetup")


# ================================================ 2-7 動吸振器 (required)
def f_dynamic_absorber():
    im, d = new(); title(d, "動吸振器:主系(m,k)+付加系(ma,ka)")
    hwall(d, 150, 510, 375, side=-1, n=12)
    cx = 330
    # main spring k
    spring(d, cx - 60, 375, cx - 60, 290, coils=6, amp=13)
    ctext(d, cx - 96, 332, "k", FS, BLACK, "rm")
    # main mass m
    box(d, cx - 70, 235, cx + 70, 290, FILL1)
    ctext(d, cx, 262, "m (主系)", FS)
    # external force
    arrow(d, cx + 40, 205, cx + 40, 233, RED, 4, 13)
    ctext(d, cx + 46, 196, "F cos(wt)", FT, RED, "lm")
    # absorber spring ka
    spring(d, cx, 235, cx, 165, coils=5, amp=11)
    ctext(d, cx - 26, 200, "ka", FT, BLACK, "rm")
    # absorber mass ma
    box(d, cx - 45, 118, cx + 45, 163, FILL2)
    ctext(d, cx, 140, "ma (付加系)", FT)
    note(d, "付加系(ma,ka)を主系に載せて主系の共振応答を抑える")
    save(im, "v1e2DynamicAbsorber")


# ================================================ 2-8 2自由度ばね系 (required)
def f_twodof_springs():
    im, d = new(); title(d, "2自由度系:壁-k-m-k-m-k-壁")
    y = 230
    wall(d, 70, 175, 285, side=1, n=8)
    wall(d, 590, 175, 285, side=-1, n=8)
    x1, x2 = 250, 430
    spring(d, 70, y, x1 - 45, y, coils=6, amp=13)
    box(d, x1 - 45, y - 34, x1 + 45, y + 34, FILL1); ctext(d, x1, y, "m", F)
    spring(d, x1 + 45, y, x2 - 45, y, coils=6, amp=13)
    box(d, x2 - 45, y - 34, x2 + 45, y + 34, FILL1); ctext(d, x2, y, "m", F)
    spring(d, x2 + 45, y, 590, y, coils=6, amp=13)
    ctext(d, 160, y - 46, "k", FS); ctext(d, 340, y - 46, "k", FS); ctext(d, 520, y - 46, "k", FS)
    arrow(d, x1, y - 52, x1 + 40, y - 52, BLUE, 2, 10); ctext(d, x1 + 46, y - 52, "x1", FT, BLUE, "lm")
    arrow(d, x2, y - 52, x2 + 40, y - 52, BLUE, 2, 10); ctext(d, x2 + 46, y - 52, "x2", FT, BLUE, "lm")
    note(d, "3本のばねkと2つの質量mからなる2自由度系")
    save(im, "v1e2TwoDofSprings")


# ================================================ 2-9 弦上の2質点 (required)
def f_string_two_mass():
    im, d = new(); title(d, "張力T0の弦を3等分する2点に質量m")
    y = 220; x0, x3 = 110, 550
    seg = (x3 - x0) / 3
    x1, x2 = x0 + seg, x0 + 2 * seg
    wall(d, x0, 175, 265, side=1, n=6)
    wall(d, x3, 175, 265, side=-1, n=6)
    # slightly displaced string (small transverse), no answer(mode) revealed
    ya, yb = y - 24, y + 16
    d.line((x0, y, x1, ya), fill=BLACK, width=3)
    d.line((x1, ya, x2, yb), fill=BLACK, width=3)
    d.line((x2, yb, x3, y), fill=BLACK, width=3)
    node(d, x1, ya, 10, FILL1); node(d, x2, yb, 10, FILL1)
    ctext(d, x1, ya - 22, "m", FS); ctext(d, x2, yb + 22, "m", FS)
    dsh(d, x0, y, x3, y, LGRAY)
    dim(d, x0, 300, x1, 300, "L/3", col=GRAY)
    dim(d, x1, 300, x2, 300, "L/3", col=GRAY)
    dim(d, x2, 300, x3, 300, "L/3", col=GRAY)
    ctext(d, x0 + 30, y - 30, "張力 T0", FT, RED, "lm")
    note(d, "3等分点(L/3ごと)に質量m。横振動の2自由度系")
    save(im, "v1e2StringTwoMass")


# ================================================ 2-10 正定値=お椀 (helpful)
def f_matrix_definite():
    im, d = new(); title(d, "対称正定値行列の2次形式=お椀型エネルギー面")
    # bowl contours (nested ellipses)
    cx, cy = 210, 235
    for i, r in enumerate([26, 52, 78, 104]):
        d.ellipse((cx - r, cy - r * 0.6, cx + r, cy + r * 0.6), outline=(90 + i * 30, 90 + i * 30, 90 + i * 30), width=2)
    node(d, cx, cy, 4, RED, RED)
    ctext(d, cx, cy + 96, "V = (1/2) x^T K x > 0", FT, BLACK)
    ctext(d, cx, cy + 118, "(最小点=平衡・お椀型)", FT, GRAY)
    # matrix + note
    matrix_grid(d, 420, 150, [["k11", "k12"], ["k12", "k22"]], cell=68, fnt=FT)
    ctext(d, 488, 300, "対称 K=K^T", FT, GRAY)
    ctext(d, 488, 326, "正定値 → 固有値は", FT, GRAY)
    ctext(d, 488, 348, "純虚数 (安定振動)", FT, BLUE)
    save(im, "v1e2MatrixDefiniteness")


# ================================================ 2-11 ねじり剛体モード (helpful)
def f_torsion_rigid():
    im, d = new(); title(d, "2円板ねじり:同位相(剛体 w=0)と逆位相(w2)")
    def disks( cx, s1, s2, lab, sub):
        d.line((cx - 90, 235, cx + 90, 235), fill=BLACK, width=3)  # shaft
        for dx, s in [(-60, s1), (60, s2)]:
            d.ellipse((cx + dx - 34, 201, cx + dx + 34, 269), outline=BLACK, width=3, fill=FILL1)
            # rotation arrow
            a0, a1 = (20, 160) if s > 0 else (-160, -20)
            d.arc((cx + dx - 22, 213, cx + dx + 22, 257), a0, a1, fill=RED, width=3)
            ang = math.radians(a1)
            tx, ty = cx + dx + 22 * math.cos(ang), 235 + 22 * math.sin(ang)
            arrow(d, tx, ty, tx + (-8 if s > 0 else 8), ty - 8, RED, 2, 7)
        ctext(d, cx, 300, lab, FS)
        ctext(d, cx, 324, sub, FT, GRAY)
    disks(190, 1, 1, "同位相(同じ向き)", "剛体回転 w=0")
    d.line((330, 190, 330, 340), fill=LGRAY, width=1)
    disks(480, 1, -1, "逆位相(逆向き)", "2次モード w2>0")
    save(im, "v1e2TorsionRigidBody")


# ================================================ 2-12 質量正規化 (helpful)
def f_mass_norm():
    im, d = new(); title(d, "同一モード形をスケール違いで:質量正規化は長さのみ変わる")
    def shape(ox, amp, col, lab):
        x0, ytop, ybot = ox, 110, 330
        dsh(d, x0, ytop, x0, ybot, LGRAY)
        pts = [(x0 + amp * math.sin(math.pi * t), ytop + (ybot - ytop) * t) for t in [i / 40 for i in range(41)]]
        plot(d, 0, 0, pts, col, 4)
        ctext(d, x0, ybot + 22, lab, FT, col)
    shape(150, 40, BLUE, "任意スケール phi")
    shape(330, 70, GREEN, "別スケール 2 phi")
    arrow(d, 405, 220, 455, 220, BLACK, 3, 13)
    shape(540, 55, RED, "質量正規化 phi_n")
    ctext(d, 330, 370, "形は同一・長さ(振幅)だけ変わる。phi_n^T M phi_n = 1", FT, GRAY)
    save(im, "v1e2MassNormalization")


# ================================================ 2-13 レイリー商 (helpful)
def f_rayleigh_quotient():
    im, d = new(); title(d, "レイリー商 = モード剛性 / モード質量")
    cx = 300
    box(d, cx - 180, 130, cx + 180, 178, (225, 240, 225))
    ctext(d, cx, 154, "phi^T K phi  (モード剛性)", FS)
    d.line((cx - 190, 195, cx + 190, 195), fill=BLACK, width=3)
    box(d, cx - 180, 212, cx + 180, 260, (225, 235, 245))
    ctext(d, cx, 236, "phi^T M phi  (モード質量)", FS)
    ctext(d, cx + 210, 195, "= w^2", F, RED, "lm")
    arrow(d, cx, 285, cx, 320, GRAY, 2, 11)
    ctext(d, cx, 345, "sqrt をとると角振動数 w", FS, BLUE)
    note(d, "真のモード形で最小=最低次固有振動数(上界を与える)")
    save(im, "v1e2RayleighQuotient")


# ================================================ 2-14 モード座標 (helpful)
def f_modal_coord():
    im, d = new(); title(d, "モード重ね合わせ: x = eta1 phi1 + eta2 phi2")
    def shape(ox, mode, amp, col, lab):
        x0, ytop, ybot = ox, 120, 320
        dsh(d, x0, ytop, x0, ybot, LGRAY)
        if mode == 1:
            pts = [(x0 + amp * math.sin(math.pi * t), ytop + (ybot - ytop) * t) for t in [i / 40 for i in range(41)]]
        else:
            pts = [(x0 + amp * math.sin(2 * math.pi * t), ytop + (ybot - ytop) * t) for t in [i / 40 for i in range(41)]]
        plot(d, 0, 0, pts, col, 4)
        ctext(d, x0, ybot + 20, lab, FT, col)
    shape(120, 1, 45, BLUE, "eta1 phi1")
    ctext(d, 210, 220, "+", F)
    shape(300, 2, 45, GREEN, "eta2 phi2")
    ctext(d, 390, 220, "=", F)
    # combined
    x0, ytop, ybot = 520, 120, 320
    dsh(d, x0, ytop, x0, ybot, LGRAY)
    pts = [(x0 + 0.7 * 45 * math.sin(math.pi * t) + 0.5 * 45 * math.sin(2 * math.pi * t),
            ytop + (ybot - ytop) * t) for t in [i / 60 for i in range(61)]]
    plot(d, 0, 0, pts, RED, 4)
    ctext(d, x0, ybot + 20, "物理変位 x", FT, RED)
    save(im, "v1e2ModalCoordinate")


# ================================================ 2-15 周波数応答(行列式=0) (helpful)
def f_freq_response():
    im, d = new(); title(d, "det([K]-w^2[M])=0 の各根で応答が発散")
    ox, oy = 90, 345; xr, ym = 500, 255
    w1, w2 = 0.9, 1.9
    X = lambda w: ox + w / 3.0 * xr
    def amp(w):
        return abs(1 / ((w1 * w1 - w * w) + 1e-3)) + abs(0.6 / ((w2 * w2 - w * w) + 1e-3))
    axes(d, ox, oy, xr + 30, ym + 25, "w", "|x|")
    pts = []
    for i in range(4, 300):
        w = i / 100.0
        a = amp(w)
        pts.append((X(w), max(oy - min(a, 6) / 6 * ym, oy - ym)))
    plot(d, 0, 0, pts, BLUE, 2)
    for w, lab in [(w1, "w1"), (w2, "w2")]:
        dsh(d, X(w), oy, X(w), oy - ym, RED)
        ctext(d, X(w), oy + 16, lab, FT, RED)
    ctext(d, 330, 90, "固有振動数(det=0)で応答が無限大", FT, GRAY)
    save(im, "v1e2FrequencyResponse")


# ================================================ 2-16 モード重ね合わせ応答 (helpful)
def f_mode_superpose():
    im, d = new(); title(d, "各モード応答の和:固有振動数ごとにピーク")
    ox, oy = 90, 345; xr, ym = 500, 255
    w1, w2, z = 1.0, 2.1, 0.06
    X = lambda w: ox + w / 3.0 * xr
    def modal(w, wn):
        return 1 / math.sqrt((1 - (w / wn) ** 2) ** 2 + (2 * z * (w / wn)) ** 2)
    axes(d, ox, oy, xr + 30, ym + 25, "w", "|x|")
    Y = lambda a: oy - min(a, 9) / 9 * ym
    p1 = [(X(i / 100.0), Y(modal(i / 100.0, w1))) for i in range(10, 300)]
    p2 = [(X(i / 100.0), Y(0.8 * modal(i / 100.0, w2))) for i in range(10, 300)]
    ps = [(X(i / 100.0), Y(modal(i / 100.0, w1) + 0.8 * modal(i / 100.0, w2))) for i in range(10, 300)]
    plot(d, 0, 0, p1, LGRAY, 2); plot(d, 0, 0, p2, LGRAY, 2)
    plot(d, 0, 0, ps, BLUE, 3)
    ctext(d, X(w1), oy + 16, "w1", FT, RED); ctext(d, X(w2), oy + 16, "w2", FT, RED)
    ctext(d, 470, 110, "太線=総和\n細線=各モード", FT, GRAY)
    save(im, "v1e2ModeSuperposition")


# ================================================ 2-17 航空機の剛体+弾性 (required)
def f_aircraft():
    im, d = new(); title(d, "自由飛行機:剛体運動 と 主翼の弾性たわみ")
    cy = 210
    # fuselage
    d.polygon([(240, cy - 16), (430, cy - 16), (455, cy), (430, cy + 16), (240, cy + 16), (225, cy)],
              outline=BLACK, width=3, fill=FILL1)
    # tail
    d.polygon([(240, cy - 16), (225, cy - 46), (255, cy - 16)], outline=BLACK, width=3, fill=FILL2)
    # rigid wing (dashed reference) + elastic bent wing (solid)
    for s in (-1, 1):
        base = (335, cy + s * 14)
        tip = (335 + s * 0, cy + s * 90)
        dsh(d, base[0] - 70, base[1], base[0] + 70, base[1], LGRAY)  # rigid ref
        # bent wing
        pts = [(base[0] + t * 90, base[1] + s * 34 * (t / 90) ** 2) for t in range(0, 91, 9)]
        pts2 = [(base[0] - t * 90, base[1] + s * 34 * (t / 90) ** 2) for t in range(0, 91, 9)]
    # simpler: draw wings left/right with bending
    for s in (-1, 1):
        pts = [(335 + s * (t), cy - 4 + 26 * (t / 110) ** 2) for t in range(0, 111, 8)]
        d.line(pts, fill=BLUE, width=5, joint="curve")
        dsh(d, 335, cy - 4, 335 + s * 110, cy - 4, LGRAY)
    ctext(d, 150, cy - 60, "剛体運動\n(並進・回転)", FT, GRAY)
    arrow(d, 130, cy, 175, cy, GRAY, 3, 12)
    force(d, 335, 120, 0, 30, "F", RED)
    ctext(d, 470, cy + 70, "主翼たわみ=弾性変形", FT, BLUE, "lm")
    ctext(d, 470, cy + 40, "(点線=剛体位置)", FT, GRAY, "lm")
    note(d, "自由支持: 剛体モード(振動数0)と弾性モードが共存")
    save(im, "v1e2AircraftElastic")


# ================================================ 2-18 コンプライアンスFRF (helpful)
def f_compliance_frf():
    im, d = new(); title(d, "帯域内共振+帯域外(低次=剰余質量/高次=剰余剛性)")
    ox, oy = 90, 340; xr, ym = 500, 250
    b0, b1 = ox + 150, ox + 350
    z = 0.05
    X = lambda w: ox + w / 4.0 * xr
    def amp(w):
        s = 0
        for wn, g in [(1.7, 1.0), (2.6, 0.7)]:
            s += g / math.sqrt((1 - (w / wn) ** 2) ** 2 + (2 * z * (w / wn)) ** 2)
        return s
    axes(d, ox, oy, xr + 30, ym + 25, "w", "受容度")
    Y = lambda a: oy - min(a, 9) / 9 * ym
    pts = [(X(i / 100.0), Y(amp(i / 100.0))) for i in range(10, 400)]
    plot(d, 0, 0, pts, BLUE, 2)
    dsh(d, b0, oy, b0, oy - ym, GRAY); dsh(d, b1, oy, b1, oy - ym, GRAY)
    ctext(d, (b0 + b1) / 2, 78, "解析帯域", FT, RED)
    ctext(d, ox + 60, 130, "低次寄与\n=剰余質量", FT, GRAY)
    ctext(d, b1 + 55, 150, "高次寄与\n=剰余剛性", FT, GRAY)
    save(im, "v1e2ComplianceFRF")


# ================================================ 2-19 レイリー減衰 (helpful)
def f_rayleigh_damping():
    im, d = new(); title(d, "レイリー減衰:質量比例(低域)+剛性比例(高域)")
    ox, oy = 95, 345; xr, ym = 480, 255
    a, b = 0.9, 0.16
    X = lambda w: ox + w / 6.0 * xr
    zmax = 0.5
    Y = lambda z: oy - min(z, zmax) / zmax * ym
    axes(d, ox, oy, xr + 30, ym + 25, "w", "z(減衰比)")
    massp = [(X(w / 20), Y(a / (2 * (w / 20)))) for w in range(4, 120)]
    stiffp = [(X(w / 20), Y(b * (w / 20) / 2)) for w in range(4, 120)]
    total = [(X(w / 20), Y(a / (2 * (w / 20)) + b * (w / 20) / 2)) for w in range(4, 120)]
    plot(d, 0, 0, massp, GREEN, 2); plot(d, 0, 0, stiffp, ORANGE, 2); plot(d, 0, 0, total, BLUE, 3)
    ctext(d, X(0.7), Y(a / (2 * 0.7)) - 10, "a/(2w) 質量比例", FT, GREEN, "lm")
    ctext(d, X(4.6), Y(b * 4.6 / 2) - 10, "bw/2 剛性比例", FT, ORANGE, "rm")
    ctext(d, X(2.6), Y(a / (2 * 2.6) + b * 2.6 / 2) + 20, "和(レイリー減衰)", FT, BLUE)
    save(im, "v1e2RayleighDamping")


# ================================================ 2-20 減衰系モード根 (helpful)
def f_damped_roots():
    im, d = new(); title(d, "減衰系のモード根 lr = -wr z +- j wr sqrt(1-z^2)")
    cx, cy = 360, 225
    arrow(d, 120, cy, 610, cy, BLACK, 2, 11); ctext(d, 616, cy, "Re", FS, BLACK, "lm")
    arrow(d, cx, 385, cx, 75, BLACK, 2, 11); ctext(d, cx - 10, 67, "Im", FS, BLACK, "rm")
    wr = 175
    for z in [0.2, 0.5]:
        sig = wr * z; wd = wr * math.sqrt(1 - z * z)
        for s in (-1, 1):
            p = (cx - sig, cy - s * wd)
            d.line((cx, cy, p[0], p[1]), fill=LGRAY, width=1)
            node(d, p[0], p[1], 5, RED, RED)
        # arc radius wr
    d.arc((cx - wr, cy - wr, cx + wr, cy + wr), 90, 270, fill=GRAY, width=1)
    ctext(d, cx - wr - 6, cy - wr + 20, "半径 wr", FT, GRAY, "rm")
    ctext(d, 130, 100, "実部 -wr z (減衰)", FT, BLUE, "lm")
    ctext(d, 130, 124, "虚部 wr sqrt(1-z^2)", FT, GREEN, "lm")
    ctext(d, 150, cy + 150, "z 増→根が実軸へ寄る", FT, GRAY, "lm")
    save(im, "v1e2DampedModalRoots")


# ================================================ 2-21 実モードvs複素モード (helpful)
def f_complex_mode():
    im, d = new(); title(d, "実モード(同位相・定在波) と 複素モード(位相ずれ・進行波)")
    def beam(ox, phases, col, lab):
        x0, x1, yc = ox, ox + 220, 240
        dsh(d, x0, yc, x1, yc, LGRAY)
        for ph in phases:
            pts = [(x0 + (x1 - x0) * t / 40, yc - 42 * math.sin(math.pi * t / 40 + ph) * math.cos(ph * 0.0 + 0) ) for t in range(41)]
            # standing: same node positions; use sin(pi t)*cos(ph)
            pts = [(x0 + (x1 - x0) * t / 40, yc - 42 * math.sin(math.pi * t / 40) * math.cos(ph)) for t in range(41)]
            plot(d, 0, 0, pts, col, 2)
        ctext(d, (x0 + x1) / 2, 330, lab, FT, col)
    beam(70, [0, 0.6, 1.2, 1.9], BLUE, "実モード: 節が固定")
    d.line((330, 90, 330, 340), fill=LGRAY, width=1)
    # complex/traveling: sin(pi t - ph)
    def beam2(ox, col, lab):
        x0, x1, yc = ox, ox + 220, 240
        dsh(d, x0, yc, x1, yc, LGRAY)
        for ph in [0, 0.9, 1.8, 2.7]:
            pts = [(x0 + (x1 - x0) * t / 40, yc - 42 * math.sin(math.pi * t / 40 - ph)) for t in range(41)]
            plot(d, 0, 0, pts, col, 2)
        ctext(d, (x0 + x1) / 2, 330, lab, FT, col)
    beam2(370, GREEN, "複素モード: 節が移動")
    save(im, "v1e2ComplexMode")


# ================================================ 2-22 状態空間 (helpful)
def f_state_space():
    im, d = new(); title(d, "状態空間表現:{x; xdot} を積んだ2N次系へ1階化")
    # state vector bracket
    bx, by0, by1 = 120, 120, 330
    d.line((bx, by0, bx - 12, by0), fill=BLACK, width=2)
    d.line((bx, by0, bx, by1), fill=BLACK, width=2)
    d.line((bx, by1, bx - 12, by1), fill=BLACK, width=2)
    d.line((bx + 90, by0, bx + 102, by0), fill=BLACK, width=2)
    d.line((bx + 90, by0, bx + 90, by1), fill=BLACK, width=2)
    d.line((bx + 90, by1, bx + 102, by1), fill=BLACK, width=2)
    d.line((bx, 225, bx + 90, 225), fill=LGRAY, width=1)
    ctext(d, bx + 45, 175, "x  (N)", FS)
    ctext(d, bx + 45, 278, "xdot (N)", FS)
    ctext(d, bx + 45, 350, "状態 y (2N)", FT, GRAY)
    arrow(d, bx + 120, 225, bx + 175, 225, BLACK, 3, 13)
    flowbox(d, 470, 225, 300, 90, "1階化\nydot = D y + E f", (225, 240, 225), FS)
    ctext(d, 470, 300, "M xddot+C xdot+K x=f を", FT, GRAY)
    ctext(d, 470, 322, "1階連立へ変換(非対称D可)", FT, GRAY)
    save(im, "v1e2StateSpace")


# ================================================ 2-23 粘性 vs 構造減衰 (helpful)
def f_structural_damping():
    im, d = new(); title(d, "1サイクル散逸:粘性減衰(w比例) と 構造減衰(一定)")
    ox, oy = 95, 340; xr, ym = 470, 250
    X = lambda w: ox + w / 5.0 * xr
    Y = lambda e: oy - min(e, 5) / 5 * ym
    axes(d, ox, oy, xr + 30, ym + 25, "w", "1周期の散逸")
    visc = [(X(w / 20), Y(0.9 * (w / 20))) for w in range(2, 100)]
    struct = [(X(w / 20), Y(2.4)) for w in range(2, 100)]
    plot(d, 0, 0, visc, BLUE, 3); plot(d, 0, 0, struct, RED, 3)
    ctext(d, X(4.3), Y(0.9 * 4.3) - 8, "粘性: w に比例", FT, BLUE, "rm")
    ctext(d, X(1.2), Y(2.4) - 14, "構造(履歴)減衰: 一定", FT, RED, "lm")
    ctext(d, 330, 385, "構造減衰=複素剛性 k(1+ j eta) → 散逸が振動数によらない", FT, GRAY)
    save(im, "v1e2StructuralDamping")


# ================================================ 2-24 履歴減衰で有限ピーク (helpful)
def f_hysteretic_mode():
    im, d = new(); title(d, "複素剛性 k(1+ j eta) で共振ピークが有限に")
    ox, oy = 95, 345; xr, ym = 480, 255
    X = lambda r: ox + r / 2.0 * xr
    axes(d, ox, oy, xr + 30, ym + 25, "w/wn", "|x|")
    Y = lambda a: oy - min(a, 8) / 8 * ym
    # undamped -> spike to top (dashed)
    dsh(d, X(1), oy, X(1), oy - ym, RED)
    ctext(d, X(1) + 6, 95, "無減衰→発散", FT, RED, "lm")
    eta = 0.14
    pts = []
    for i in range(20, 200):
        r = i / 100.0
        a = 1 / math.sqrt((1 - r * r) ** 2 + eta ** 2)
        pts.append((X(r), Y(a)))
    plot(d, 0, 0, pts, BLUE, 3)
    node(d, X(1), Y(1 / eta), 5, BLUE, BLUE)
    ctext(d, X(1.3), Y(1 / eta) - 6, "履歴減衰→有限(1/eta)", FT, BLUE, "lm")
    save(im, "v1e2HystereticMode")


# ================================================ 2-25 基礎加振 (required)
def f_base_excitation():
    im, d = new(); title(d, "基礎加振:床 y=Y sin(wt) 上のばねk・ダンパc・質量m")
    # moving floor
    d.rectangle((150, 340, 510, 362), outline=BLACK, width=3, fill=FILL2)
    for i in range(9):
        xx = 160 + i * 40
        d.line((xx, 362, xx - 12, 378), fill=GRAY, width=2)
    arrow(d, 300, 351, 360, 351, GREEN, 3, 12)
    ctext(d, 330, 392, "y = Y sin(wt) (基礎)", FT, GREEN)
    # spring and damper up to mass
    mcx, mcy = 330, 210
    spring(d, mcx - 55, 340, mcx - 55, mcy + 30, coils=6, amp=12)
    ctext(d, mcx - 88, 275, "k", FS, BLACK, "rm")
    # damper
    dx = mcx + 55
    d.line((dx, 340, dx, 300), fill=BLACK, width=3)
    d.rectangle((dx - 14, 262, dx + 14, 300), outline=BLACK, width=3)
    d.line((dx, mcy + 30, dx, 278), fill=BLACK, width=3)
    d.line((dx - 11, 278, dx + 11, 278), fill=BLACK, width=4)
    ctext(d, dx + 22, 285, "c", FS, BLACK, "lm")
    box(d, mcx - 65, mcy - 30, mcx + 65, mcy + 30, FILL1)
    ctext(d, mcx, mcy, "m", F)
    arrow(d, mcx, mcy - 46, mcx, mcy - 80, BLUE, 2, 10)
    ctext(d, mcx, mcy - 92, "x (絶対変位)", FT, BLUE)
    note(d, "床の運動 y が k,c を通じて質量 m を揺らす")
    save(im, "v1e2BaseExcitation")


# ================================================ 2-26 ヒステリシスループ (helpful)
def f_hysteresis_loop():
    im, d = new(); title(d, "応力-ひずみのヒステリシスループ(面積=散逸)")
    ox, oy = 340, 235
    axes(d, ox - 220, oy + 130, 260, 0, "", "")  # placeholder
    arrow(d, ox - 200, oy, ox + 200, oy, BLACK, 2, 11); ctext(d, ox + 206, oy, "ひずみ e", FS, BLACK, "lm")
    arrow(d, ox, oy + 150, ox, oy - 150, BLACK, 2, 11); ctext(d, ox - 10, oy - 158, "応力 s", FS, BLACK, "rm")
    pts = []
    for i in range(0, 361):
        th = math.radians(i)
        e = 150 * math.cos(th)
        s = 110 * math.sin(th) + 55 * math.cos(th)
        pts.append((ox + e, oy - s))
    d.polygon(pts, outline=BLUE, width=3)
    # shade lightly by hatching
    for i in range(-140, 141, 14):
        d.line((ox + i, oy - 40, ox + i, oy - 40), fill=LGRAY, width=1)
    ctext(d, ox + 60, oy - 40, "面積=1サイクルの\n散逸エネルギー", FT, RED)
    save(im, "v1e2HysteresisLoop")


# ================================================ 2-27 線形/非線形の定義 (helpful)
def f_nonlinear_def():
    im, d = new(); title(d, "線形(直線)と非線形(曲線):加法性・同次性")
    # left linear
    ox, oy = 110, 320
    axes(d, ox, oy, 190, 230, "入力", "出力")
    d.line((ox, oy, ox + 170, oy - 200), fill=BLUE, width=3)
    ctext(d, ox + 90, oy - 40, "直線", FT, BLUE)
    ctext(d, 185, 350, "加法性・同次性が成立", FT, GREEN)
    d.line((330, 90, 330, 350), fill=LGRAY, width=1)
    # right nonlinear
    ox2, oy2 = 400, 320
    axes(d, ox2, oy2, 200, 230, "入力", "出力")
    pts = [(ox2 + t, oy2 - 200 * (t / 180) ** 2) for t in range(0, 181, 6)]
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, ox2 + 120, oy2 - 60, "曲線", FT, RED)
    ctext(d, 490, 350, "加法性・同次性が破れる", FT, RED)
    save(im, "v1e2NonlinearDefinition")


# ================================================ 2-28 ダフィング自由振動 背骨曲線 (helpful)
def f_duffing_free():
    im, d = new(); title(d, "硬化ばね:背骨曲線(振幅大で固有振動数が高域へ)")
    ox, oy = 110, 350
    axes(d, ox, oy, 460, 290, "w", "振幅 A")
    # backbone: A increases as w increases (bends right)
    pts = [(ox + (0.0 + 0.45 * (A / 250) ** 2) * 400 + 60, oy - A) for A in range(0, 261, 6)]
    plot(d, 0, 0, pts, BLUE, 3)
    dsh(d, ox + 60, oy, ox + 60, oy - 260, LGRAY)
    ctext(d, ox + 60, oy + 16, "w0(微小振幅)", FT, GRAY)
    ctext(d, ox + 330, oy - 210, "振幅大で\n高域へ", FT, RED)
    ctext(d, 330, 392, "硬化ばね(復元力が3次で増加)→背骨が右へ倒れる", FT, GRAY)
    save(im, "v1e2DuffingFreeVib")


# ================================================ 2-29 振幅で周期が変わる (helpful)
def f_duffing_amp():
    im, d = new(); title(d, "非線形自由振動:振幅で最大変位も周期も変わる")
    ox, oy = 90, 220
    arrow(d, ox, oy, ox + 520, oy, BLACK, 2, 11); ctext(d, ox + 526, oy, "t", FS, BLACK, "lm")
    arrow(d, ox, oy + 130, ox, oy - 130, BLACK, 2, 11); ctext(d, ox - 10, oy - 138, "x", FS, BLACK, "rm")
    # small amplitude, longer period-ish
    p1 = [(ox + t, oy - 45 * math.sin(2 * math.pi * t / 150)) for t in range(0, 501)]
    plot(d, 0, 0, p1, GREEN, 2)
    # a times amplitude, shorter period (hardening)
    p2 = [(ox + t, oy - 100 * math.sin(2 * math.pi * t / 110)) for t in range(0, 501)]
    plot(d, 0, 0, p2, BLUE, 2)
    ctext(d, ox + 470, oy - 60, "振幅 1", FT, GREEN, "lm")
    ctext(d, ox + 470, oy - 112, "振幅 a", FT, BLUE, "lm")
    ctext(d, 330, 392, "線形と違い、最大変位 a 倍でも周期が振幅に依存", FT, GRAY)
    save(im, "v1e2DuffingAmplitude")


# ================================================ 2-30 ダフィング強制:跳躍 (helpful)
def f_duffing_forced():
    im, d = new(); title(d, "強制ダフィング:背骨が右へ倒れ跳躍現象(履歴)")
    ox, oy = 110, 360
    axes(d, ox, oy, 470, 300, "w", "振幅 A")
    A1, A2, Amax, dA = 110, 180, 250, 2
    Avals = list(range(0, Amax + 1, dA))
    x = 0.0; raw = []
    for i, A in enumerate(Avals):
        if i > 0:
            x += 0.0009 * (A - A1) * (A - A2) * dA
        raw.append((A, x))
    xmin = min(v for _, v in raw); xmax = max(v for _, v in raw)
    PX = lambda v: ox + 60 + (v - xmin) / (xmax - xmin) * 360
    PY = lambda A: oy - A * 1.02
    pt = {A: (PX(v), PY(A)) for A, v in raw}
    low = [pt[A] for A in Avals if A <= A1]
    mid = [pt[A] for A in Avals if A1 <= A <= A2]
    up = [pt[A] for A in Avals if A >= A2]
    plot(d, 0, 0, low, BLUE, 3)
    plot(d, 0, 0, up, BLUE, 3)
    for i in range(len(mid) - 1):
        dsh(d, mid[i][0], mid[i][1], mid[i + 1][0], mid[i + 1][1], GRAY, 2)
    # jump-up at rightmost (A1) ; jump-down at leftmost overhang (A2)
    xu = pt[A1][0]; xd = pt[A2][0]
    dsh(d, xu, oy, xu, oy - Amax * 1.02, LGRAY); dsh(d, xd, oy, xd, oy - Amax * 1.02, LGRAY)
    arrow(d, xu, pt[A1][1], xu, PY(228), RED, 3, 12)
    ctext(d, xu + 6, oy + 16, "w_up", FT, RED, "lm")
    ctext(d, xu + 8, PY(180), "跳躍(上)", FT, RED, "lm")
    arrow(d, xd, PY(200), xd, pt[80][1], RED, 3, 12)
    ctext(d, xd - 6, oy + 16, "w_down", FT, RED, "rm")
    ctext(d, xd - 8, PY(120), "跳躍(下)", FT, RED, "rm")
    ctext(d, ox + 300, PY(70), "点線=不安定枝", FT, GRAY, "lm")
    ctext(d, 330, 395, "多価領域(w_down<w<w_up)で3解。掃引方向で経路が違う=履歴", FT, GRAY)
    save(im, "v1e2DuffingForced")


# ================================================ 2-31 主共振+高調波/分数調波 (helpful)
def f_hysteresis_jump():
    im, d = new(); title(d, "主共振の両側に高調波・分数調波共振の小ピーク")
    ox, oy = 90, 345; xr, ym = 500, 255
    X = lambda r: ox + r / 3.0 * xr
    axes(d, ox, oy, xr + 30, ym + 25, "励振振動数 w", "応答")
    def bump(r0, h, wdt):
        return lambda r: h / (1 + ((r - r0) / wdt) ** 2)
    peaks = [(1.0, 8.0, 0.05, "主共振", RED), (0.5, 2.2, 0.03, "分数調波 w/2", GREEN),
             (2.0, 2.6, 0.05, "高調波 2w", ORANGE), (3.0, 1.6, 0.05, "3w", ORANGE)]
    fns = [bump(r0, h, w) for r0, h, w, _, _ in peaks]
    Y = lambda a: oy - min(a, 9) / 9 * ym
    pts = []
    for i in range(5, 300):
        r = i / 100.0
        a = sum(f(r) for f in fns)
        pts.append((X(r), Y(a)))
    plot(d, 0, 0, pts, BLUE, 2)
    for r0, h, w, lab, col in peaks:
        ctext(d, X(r0), Y(h) - 12, lab, FT, col)
    save(im, "v1e2HysteresisJump")


# ================================================ 2-32 振子の軟化 (helpful)
def f_pendulum_soft():
    im, d = new(); title(d, "単振子の軟化: sin(th) < th (大角度で復元弱)")
    ox, oy = 95, 300
    axes(d, ox, oy, 330, 250, "th", "復元項")
    sc = 150
    line = [(ox + t / 2.2 * sc, oy - t / 2.2 * sc) for t in [i / 100 * 2.2 for i in range(101)]]
    plot(d, 0, 0, line, GRAY, 2)
    ctext(d, ox + 150, oy - 175, "y=th(線形)", FT, GRAY, "lm")
    curv = [(ox + t / 2.2 * sc, oy - math.sin(t) / 2.2 * sc) for t in [i / 100 * 2.2 for i in range(101)]]
    plot(d, 0, 0, curv, BLUE, 3)
    ctext(d, ox + 200, oy - 95, "y=sin(th)", FT, BLUE, "lm")
    # pendulum sketch
    px, py = 540, 130
    node(d, px, py, 5)
    ang = math.radians(35)
    ex, ey = px + 90 * math.sin(ang), py + 90 * math.cos(ang)
    dsh(d, px, py, px, py + 95, LGRAY)
    d.line((px, py, ex, ey), fill=BLACK, width=3)
    node(d, ex, ey, 11, FILL1); ctext(d, ex + 14, ey, "m", FS, BLACK, "lm")
    angle_arc(d, px, py, 45, -90, -55, "th", GRAY)
    ctext(d, 540, 300, "大角度ほど軟化", FT, RED)
    save(im, "v1e2PendulumSoftening")


# ================================================ 2-33 分数調波スペクトル (helpful)
def f_subharmonic():
    im, d = new(); title(d, "スペクトル:高調波 nw と 分数調波 w/n")
    ox, oy = 80, 330; xr, ym = 520, 240
    arrow(d, ox, oy, ox + xr + 20, oy, BLACK, 2, 11); ctext(d, ox + xr + 26, oy, "振動数", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - ym - 10, BLACK, 2, 11); ctext(d, ox - 10, oy - ym - 16, "振幅", FS, BLACK, "rm")
    lines = [(0.5, 90, "w/2", GREEN), (1.0, 210, "w", RED), (1.5, 70, "3w/2", GREEN),
             (2.0, 130, "2w", ORANGE), (3.0, 80, "3w", ORANGE)]
    for f, h, lab, col in lines:
        x = ox + f / 3.2 * xr
        d.line((x, oy, x, oy - h), fill=col, width=4)
        ctext(d, x, oy - h - 12, lab, FT, col)
    dsh(d, ox + 1.0 / 3.2 * xr, oy, ox + 1.0 / 3.2 * xr, oy - ym, LGRAY)
    ctext(d, 330, 388, "固有振動数の近傍で分数調波成分が増大", FT, GRAY)
    save(im, "v1e2SubHarmonic")


# ================================================ 2-34 自由/強制/自励 波形 (helpful)
def f_self_types():
    im, d = new(); title(d, "自由(減衰)・強制(持続)・自励(成長)の時間波形")
    for i, (lab, env, col) in enumerate([
            ("自由振動(減衰)", lambda t: math.exp(-2.2 * t), BLUE),
            ("強制振動(持続)", lambda t: 1.0, GREEN),
            ("自励振動(成長)", lambda t: min(1.0, 0.15 * math.exp(2.4 * t)), RED)]):
        oy = 120 + i * 95
        arrow(d, 70, oy, 470, oy, BLACK, 2, 9)
        wave(d, 70, oy, 380, 32, 5, env, col, 2)
        ctext(d, 555, oy, lab, FT, col, "lm")
    ctext(d, 330, 400, "自励は外力なしに振幅が成長する点が特徴", FT, GRAY)
    save(im, "v1e2SelfExcitedTypes")


# ================================================ 2-35 自励の分類 (helpful)
def f_self_class():
    im, d = new(); title(d, "自励振動の分類")
    flowbox(d, 330, 105, 260, 46, "自励振動\n(外力なしで成長)", (245, 235, 225))
    arrow(d, 250, 128, 175, 180, BLACK, 2, 11)
    arrow(d, 410, 128, 490, 180, BLACK, 2, 11)
    flowbox(d, 165, 235, 250, 90,
            "1自由度型\n負性抵抗(負減衰)\n例:乾性摩擦・ガロッピング", (225, 240, 225), FT)
    flowbox(d, 495, 235, 250, 90,
            "多自由度型\n非対称・連成による\n例:フラッター・びびり", (225, 235, 245), FT)
    ctext(d, 330, 340, "共通:系が自らエネルギーを取り込む", FT, GRAY)
    save(im, "v1e2SelfExcitedClass")


# ================================================ 2-36 自励の特徴 (helpful)
def f_self_feature():
    im, d = new(); title(d, "自励振動:成長し一定振幅へ(供給と散逸の釣合い)")
    oy = 200
    arrow(d, 70, oy, 470, oy, BLACK, 2, 10); ctext(d, 476, oy, "t", FS, BLACK, "lm")
    arrow(d, 70, oy + 120, 70, oy - 120, BLACK, 2, 10); ctext(d, 60, oy - 128, "x", FS, BLACK, "rm")
    env = lambda t: min(1.0, 0.12 * math.exp(3.0 * t)) if t < 0.6 else 1.0
    wave(d, 70, oy, 400, 95, 7, env, RED, 2)
    dsh(d, 70, oy - 95, 470, oy - 95, LGRAY); dsh(d, 70, oy + 95, 470, oy + 95, LGRAY)
    ctext(d, 260, oy - 108, "一定振幅(リミットサイクル)", FT, GRAY)
    ctext(d, 560, 150, "エネルギー供給\n> 散逸 → 成長", FT, GREEN)
    ctext(d, 560, 250, "供給 = 散逸\n→ 一定振幅", FT, BLUE)
    save(im, "v1e2SelfExcitedFeature")


# ================================================ 2-37 ガロッピング (required)
def f_galloping():
    im, d = new(); title(d, "着氷送電線のガロッピング(横風で上下振動)")
    # support spring k and mass m (conductor section)
    hwall(d, 220, 440, 95, side=-1, n=6)
    cx = 330
    spring(d, cx, 99, cx, 175, coils=5, amp=12); ctext(d, cx - 24, 137, "k", FS, BLACK, "rm")
    # iced asymmetric cross-section
    d.ellipse((cx - 45, 180, cx + 45, 250), outline=BLACK, width=3, fill=FILL1)
    d.pieslice((cx - 45, 180, cx + 45, 250), 200, 320, outline=BLACK, width=3, fill=FILL3)  # ice
    ctext(d, cx - 70, 215, "着氷", FT, GRAY, "rm")
    ctext(d, cx, 215, "m", FS)
    # wind
    for yy in (150, 200, 250):
        arrow(d, 120, yy, 200, yy, GREEN, 3, 11)
    ctext(d, 150, 128, "横風 U", FS, GREEN)
    # vertical vibration DOF
    arrow(d, cx + 70, 200, cx + 70, 165, BLUE, 2, 10)
    arrow(d, cx + 70, 230, cx + 70, 265, BLUE, 2, 10)
    ctext(d, cx + 80, 215, "y(上下)", FT, BLUE, "lm")
    note(d, "非対称断面が風から鉛直方向にエネルギーを受ける(自励)")
    save(im, "v1e2Galloping")


# ================================================ 2-38 リミットサイクル (helpful)
def f_limit_cycle():
    im, d = new(); title(d, "van der Pol系:位相平面のリミットサイクル")
    cx, cy = 340, 225
    arrow(d, 110, cy, 600, cy, BLACK, 2, 11); ctext(d, 606, cy, "x", FS, BLACK, "lm")
    arrow(d, cx, 385, cx, 75, BLACK, 2, 11); ctext(d, cx - 10, 67, "xdot", FS, BLACK, "rm")
    # limit cycle (closed loop)
    lc = [(cx + 150 * math.cos(a), cy - 110 * math.sin(a)) for a in [i / 100 * 2 * math.pi for i in range(101)]]
    d.line(lc, fill=BLUE, width=3, joint="curve")
    # inward spiral from outside
    out = []
    for i in range(0, 220):
        a = i / 18.0; r = 1.0 - 0.55 * math.exp(-i / 60.0) * 0  # keep outside converging
        rr = 1.0 + 0.9 * math.exp(-i / 55.0)
        out.append((cx + 150 * rr * math.cos(a), cy - 110 * rr * math.sin(a)))
    plot(d, 0, 0, out, GREEN, 1)
    # outward spiral from inside
    ins = []
    for i in range(0, 200):
        a = i / 18.0; rr = 0.15 + 0.85 * (1 - math.exp(-i / 55.0))
        ins.append((cx + 150 * rr * math.cos(a), cy - 110 * rr * math.sin(a)))
    plot(d, 0, 0, ins, ORANGE, 1)
    ctext(d, cx + 175, cy - 120, "リミットサイクル", FT, BLUE, "lm")
    ctext(d, 150, 110, "外側→内へ", FT, GREEN, "lm")
    ctext(d, cx + 20, cy + 30, "内側→外へ", FT, ORANGE, "lm")
    save(im, "v1e2VanDerPolLimitCycle")


# ================================================ 2-39 乾性摩擦(ベルト) (required)
def f_dry_friction():
    im, d = new(); title(d, "移動ベルト上のばね-質量 と 摩擦力-相対速度特性")
    # left: belt system
    wall(d, 70, 130, 210, side=1, n=6)
    spring(d, 70, 175, 150, 175, coils=5, amp=12); ctext(d, 110, 150, "k", FT)
    box(d, 150, 150, 250, 200, FILL1); ctext(d, 200, 175, "m", F)
    # belt
    d.rectangle((90, 205, 300, 230), outline=BLACK, width=2, fill=FILL2)
    for i in range(6):
        arrow(d, 110 + i * 30, 218, 128 + i * 30, 218, GRAY, 2, 8)
    arrow(d, 260, 260, 300, 260, GREEN, 3, 11); ctext(d, 320, 260, "ベルト速度 v", FT, GREEN, "lm")
    # right: friction characteristic (negative slope) - NOT the stability answer, just the given mu curve
    ox, oy = 380, 300
    axes(d, ox, oy, 220, 210, "相対速度", "摩擦力")
    pts = [(ox + vx, oy - 150 + 0.9 * vx * (1 - math.exp(-vx / 60.0))) for vx in range(0, 190, 6)]
    # decreasing then leveling: mu drops with relative speed
    pts = []
    for vx in range(0, 190, 5):
        f = 150 - 90 * (1 - math.exp(-vx / 45.0))
        pts.append((ox + vx, oy - f))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 120, oy - 130, "負の勾配", FT, RED)
    note(d, "摩擦力が相対速度とともに減る(負勾配)=負性減衰の源")
    save(im, "v1e2DryFrictionBelt")


# ================================================ 2-40 チョークのびびり (required)
def f_chalk_chatter():
    im, d = new(); title(d, "黒板上のチョーク:変位y・回転角th・接触摩擦F(2自由度)")
    # blackboard surface (vertical line at right? use horizontal board with chalk pressing)
    hwall(d, 120, 560, 320, side=1, n=14)
    ctext(d, 330, 350, "黒板面", FT, GRAY)
    # chalk as inclined rod
    hx, hy = 330, 150   # holder end
    ang = math.radians(70)
    cxp, cyp = hx + 150 * math.cos(ang), hy + 150 * math.sin(ang)  # contact point on board (y=320)
    cxp, cyp = 360, 320
    d.line((hx, hy, cxp, cyp), fill=BLACK, width=8)
    ctext(d, hx - 10, hy - 6, "支持", FT, GRAY, "rm")
    node(d, cxp, cyp, 5, RED, RED)
    # y coordinate (holder vertical motion)
    arrow(d, hx - 40, hy, hx - 40, hy + 40, BLUE, 2, 10)
    ctext(d, hx - 48, hy + 20, "y", FS, BLUE, "rm")
    # rotation angle th
    dsh(d, hx, hy, hx, hy + 120, LGRAY)
    angle_arc(d, hx, hy, 55, -90, -90 + math.degrees(math.atan2(cxp - hx, cyp - hy)), "th", GRAY)
    # friction force at contact along board
    arrow(d, cxp, cyp, cxp + 70, cyp, RED, 4, 13)
    ctext(d, cxp + 76, cyp - 14, "摩擦力 F", FT, RED, "lm")
    # motion direction of chalk on board
    arrow(d, cxp - 30, cyp - 30, cxp - 90, cyp - 30, GRAY, 2, 10)
    ctext(d, cxp - 60, cyp - 44, "移動方向", FT, GRAY)
    note(d, "並進 y と回転 th の連成した2自由度自励系")
    save(im, "v1e2ChalkChatter")


# ================================================ 2-41 再生びびり (required)
def f_regen_chatter():
    im, d = new(); title(d, "再生びびり:前回の削り跡 x(t-tau) と今回 x(t) の差")
    # rotating workpiece (circle) with wavy machined surface
    cx, cy, R = 240, 235, 110
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=3)
    node(d, cx, cy, 4)
    # rotation arrow
    d.arc((cx - 55, cy - 55, cx + 55, cy + 55), 200, 90, fill=GRAY, width=2)
    arrow(d, cx + 39, cy - 39, cx + 50, cy - 24, GRAY, 2, 8)
    ctext(d, cx, cy + 60, "回転", FT, GRAY)
    # wavy surface (previous cut) on right edge
    wavy = []
    for a in range(-60, 61, 3):
        rad = math.radians(a)
        rr = R + 9 * math.sin(a / 6.0)
        wavy.append((cx + rr * math.cos(rad), cy + rr * math.sin(rad)))
    d.line(wavy, fill=BLUE, width=2, joint="curve")
    ctext(d, cx + 130, cy - 90, "前回の波状面\nx(t - tau)", FT, BLUE, "lm")
    # cutting tool
    tx = cx + R + 60
    d.polygon([(tx, cy - 12), (tx + 90, cy - 30), (tx + 90, cy + 30), (tx, cy + 12)], outline=BLACK, width=3, fill=FILL2)
    ctext(d, tx + 45, cy, "バイト", FT)
    arrow(d, tx + 40, cy - 40, tx, cy - 20, RED, 3, 11)
    ctext(d, tx + 46, cy - 48, "切削力", FT, RED, "lm")
    # current vibration x(t)
    arrow(d, tx + 20, cy + 45, tx + 20, cy + 12, GREEN, 2, 10)
    ctext(d, tx + 20, cy + 58, "x(t)", FT, GREEN)
    note(d, "1回転前の跡と今の変位の差が切込み厚を変え切削力を作る(時間遅れ)")
    save(im, "v1e2RegenerativeChatter")


# ================================================ 2-42 支点上下動振子 (required)
def f_pivot_pendulum():
    im, d = new(); title(d, "支点が上下動する剛体棒振子 u=a sin(wt)")
    px, py = 330, 130
    # vertical excitation of pivot
    arrow(d, px - 45, py - 20, px - 45, py + 20, GREEN, 3, 11)
    ctext(d, px - 54, py, "u=a sin(wt)", FT, GREEN, "rm")
    node(d, px, py, 6); ctext(d, px + 14, py - 6, "支点", FT, GRAY, "lm")
    # rod at small angle
    th = 0.28
    L = 200
    ex, ey = px + L * math.sin(th), py + L * math.cos(th)
    dsh(d, px, py, px, py + L, LGRAY)
    d.line((px, py, ex, ey), fill=BLACK, width=6)
    node(d, ex, ey, 12, FILL1); ctext(d, ex + 16, ey, "m", F, BLACK, "lm")
    angle_arc(d, px, py, 60, -90, -90 + math.degrees(th), "th", GRAY)
    ctext(d, (px + ex) / 2 + 18, (py + ey) / 2, "l", FT, GRAY, "lm")
    note(d, "支点の鉛直加振がパラメータ励振となる(微小角 th)")
    save(im, "v1e2PivotExcitedPendulum")


# ================================================ 2-43 パラメータ励振 安定図 (helpful)
def f_parametric_general():
    im, d = new(); title(d, "パラメータ励振の安定図:不安定舌(減衰で狭まる)")
    ox, oy = 90, 350
    axes(d, ox, oy, 500, 290, "w", "励振振幅")
    labs = ["2w0/3", "w0", "2w0"]
    for k, x0 in enumerate([130, 300, 470]):
        left = [(x0 - a * 0.6, oy - a) for a in range(0, 210, 6)]
        right = [(x0 + a * 0.6, oy - a) for a in range(0, 210, 6)]
        d.line(left, fill=RED, width=2); d.line(right, fill=RED, width=2)
        dl = [(x0 - (a - 45) * 0.55, oy - a) for a in range(45, 210, 6)]
        dr = [(x0 + (a - 45) * 0.55, oy - a) for a in range(45, 210, 6)]
        d.line(dl, fill=BLUE, width=2); d.line(dr, fill=BLUE, width=2)
        ctext(d, x0, oy + 16, labs[k], FT, GRAY)
    box(d, 165, 78, 545, 150, "white", GRAY, 1)
    ctext(d, 355, 96, "赤=不安定舌(減衰なし)", FT, RED)
    ctext(d, 355, 118, "青=減衰ありで舌が縮む(浮く)", FT, BLUE)
    ctext(d, 355, 140, "舌の内側=不安定(振動成長)", FT, GRAY)
    save(im, "v1e2ParametricGeneral")


# ================================================ 2-44 非対称断面軸 (required)
def f_asymmetric_shaft():
    im, d = new(); title(d, "長方形断面軸:主軸で剛性が k+dk と k-dk")
    # cross-section rectangle (rotating)
    cx, cy = 330, 230
    w, h = 150, 84
    ang = math.radians(20)
    corn = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    poly = [rot(cx + px, cy + py, cx, cy, ang) for px, py in corn]
    d.polygon(poly, outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 4)
    # principal axes
    def axis(dx, dy, lab, col):
        a = rot(cx + dx, cy + dy, cx, cy, ang); b = rot(cx - dx, cy - dy, cx, cy, ang)
        d.line((a[0], a[1], b[0], b[1]), fill=col, width=2)
        ctext(d, a[0] + 8 * (1 if dx > 0 else -1), a[1], lab, FT, col, "lm" if dx > 0 else "rm")
    axis(105, 0, "最大剛性 k+dk", BLUE)   # long axis -> max stiffness
    axis(0, 70, "最小剛性 k-dk", RED)
    ctext(d, cx, cy + 150, "回転体(ロータ)が軸上に載る", FT, GRAY)
    # rotation
    d.arc((cx - 120, cy - 120, cx + 120, cy + 120), -60, 10, fill=GRAY, width=1)
    note(d, "断面の主軸で曲げ剛性が異なる → 回転で剛性が周期変動(パラメータ励振)")
    save(im, "v1e2AsymmetricShaft")


# ================================================ 2-45 弦のパラメータ励振 (required)
def f_string_parametric():
    im, d = new(); title(d, "弦+質量m:音叉で張力 T=T0(1+e cos(wt)) が周期変動")
    y = 215; x0, x1 = 110, 500
    wall(d, x0, 170, 260, side=1, n=6)
    # string with mass at center, small transverse
    mx = (x0 + x1) / 2
    d.line((x0, y, mx, y - 18), fill=BLACK, width=3)
    d.line((mx, y - 18, x1, y), fill=BLACK, width=3)
    node(d, mx, y - 18, 11, FILL1); ctext(d, mx, y - 40, "m", FS)
    dsh(d, x0, y, x1, y, LGRAY)
    ctext(d, x0 + 40, y - 14, "T0", FT, RED, "lm")
    # tuning fork at right end
    fk = x1
    d.line((fk, y, fk + 30, y), fill=BLACK, width=3)
    d.line((fk + 30, y - 30, fk + 30, y + 30), fill=BLACK, width=3)
    d.line((fk + 30, y - 30, fk + 55, y - 30), fill=BLACK, width=4)
    d.line((fk + 30, y + 30, fk + 55, y + 30), fill=BLACK, width=4)
    arrow(d, fk + 55, y - 30, fk + 55, y - 12, GREEN, 2, 8)
    arrow(d, fk + 55, y + 30, fk + 55, y + 12, GREEN, 2, 8)
    ctext(d, fk + 30, y + 55, "音叉", FT, GRAY)
    ctext(d, 330, 310, "T = T0 (1 + e cos(wt))", FS, RED)
    note(d, "張力(=剛性)が周期的に変わるパラメータ励振。e=変動率")
    save(im, "v1e2StringParametric")


# ================================================ run all
FUNCS = [
    (f_yajirobee, "v1e2YajirobeeMode"), (f_utube, "v1e2UtubeColumn"),
    (f_response_mag, "v1e2ResponseMagnification"), (f_qfactor, "v1e2QFactorCurve"),
    (f_char_roots, "v1e2CharacteristicRoots"), (f_seismograph, "v1e2SeismographSetup"),
    (f_dynamic_absorber, "v1e2DynamicAbsorber"), (f_twodof_springs, "v1e2TwoDofSprings"),
    (f_string_two_mass, "v1e2StringTwoMass"), (f_matrix_definite, "v1e2MatrixDefiniteness"),
    (f_torsion_rigid, "v1e2TorsionRigidBody"), (f_mass_norm, "v1e2MassNormalization"),
    (f_rayleigh_quotient, "v1e2RayleighQuotient"), (f_modal_coord, "v1e2ModalCoordinate"),
    (f_freq_response, "v1e2FrequencyResponse"), (f_mode_superpose, "v1e2ModeSuperposition"),
    (f_aircraft, "v1e2AircraftElastic"), (f_compliance_frf, "v1e2ComplianceFRF"),
    (f_rayleigh_damping, "v1e2RayleighDamping"), (f_damped_roots, "v1e2DampedModalRoots"),
    (f_complex_mode, "v1e2ComplexMode"), (f_state_space, "v1e2StateSpace"),
    (f_structural_damping, "v1e2StructuralDamping"), (f_hysteretic_mode, "v1e2HystereticMode"),
    (f_base_excitation, "v1e2BaseExcitation"), (f_hysteresis_loop, "v1e2HysteresisLoop"),
    (f_nonlinear_def, "v1e2NonlinearDefinition"), (f_duffing_free, "v1e2DuffingFreeVib"),
    (f_duffing_amp, "v1e2DuffingAmplitude"), (f_duffing_forced, "v1e2DuffingForced"),
    (f_hysteresis_jump, "v1e2HysteresisJump"), (f_pendulum_soft, "v1e2PendulumSoftening"),
    (f_subharmonic, "v1e2SubHarmonic"), (f_self_types, "v1e2SelfExcitedTypes"),
    (f_self_class, "v1e2SelfExcitedClass"), (f_self_feature, "v1e2SelfExcitedFeature"),
    (f_galloping, "v1e2Galloping"), (f_limit_cycle, "v1e2VanDerPolLimitCycle"),
    (f_dry_friction, "v1e2DryFrictionBelt"), (f_chalk_chatter, "v1e2ChalkChatter"),
    (f_regen_chatter, "v1e2RegenerativeChatter"), (f_pivot_pendulum, "v1e2PivotExcitedPendulum"),
    (f_parametric_general, "v1e2ParametricGeneral"), (f_asymmetric_shaft, "v1e2AsymmetricShaft"),
    (f_string_parametric, "v1e2StringParametric"),
]

if __name__ == "__main__":
    keys = [k for _, k in FUNCS]
    for fn, k in FUNCS:
        try:
            fn()
        except Exception as e:
            print("ERROR", k, repr(e))
    miss = [k for k in keys if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(keys), "SAVED", len(keys) - len(miss), "MISSING", miss)
