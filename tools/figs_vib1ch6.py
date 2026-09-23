# -*- coding: utf-8 -*-
"""振動1級 第6章「音響連成系の解析基礎」問題図 37枚。figlibで白地660x420線画。
方針: 正確さ最優先・機構のみ・装飾禁止。ラベルはASCII簡易表記(p,v,c,rho,K,phi,Phi,w,k,S,l 等)で豆腐回避。
required図(6-7,6-9)は答え(結論)を描かず機構だけ示す。"""
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


def rot(px, py, cx, cy, ang):
    s, c = math.sin(ang), math.cos(ang)
    x, y = px - cx, py - cy
    return (cx + x * c - y * s, cy + x * s + y * c)


def duct(d, x0, x1, yt, yb, wd=3):
    """横向きの管(上下壁)。"""
    d.line((x0, yt, x1, yt), fill=BLACK, width=wd)
    d.line((x0, yb, x1, yb), fill=BLACK, width=wd)


# ================================================ 6-1 平面波の2式 (helpful)
def f_plane_wave_eqs():
    im, d = new(); title(d, "1次元管の平面波:音圧pと粒子速度v(2式で連結)")
    x0, x1 = 90, 570; yt, yb = 150, 250
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    arrow(d, 200, 120, 300, 120, GRAY, 2, 11); ctext(d, 250, 106, "伝播方向 c", FT, GRAY)
    pts = [(x0 + (x1 - x0) * t, ymid - 32 * math.sin(2 * math.pi * 1.5 * t)) for t in [i / 120 for i in range(121)]]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, x1 - 6, yt + 16, "音圧 p", FT, BLUE, "rm")
    for xx in (150, 260, 370, 480):
        arrow(d, xx, yb + 26, xx + 34, yb + 26, RED, 2, 9)
    ctext(d, 300, yb + 50, "粒子速度 v", FT, RED)
    box(d, 90, 300, 360, 350, FILL1)
    ctext(d, 225, 325, "連続の式: dv/dx = -(1/K) dp/dt", FT)
    box(d, 380, 300, 610, 350, FILL1)
    ctext(d, 495, 325, "運動方程式: rho dv/dt = -dp/dx", FT)
    note(d, "体積変化=連続の式、力=運動方程式。両式とも右辺マイナス")
    save(im, "v1e6PlaneWaveEqs")


# ================================================ 6-2 波動方程式・音速 (helpful)
def f_wave_speed():
    im, d = new(); title(d, "媒質中の平面波:音速 c=sqrt(K/rho)")
    x0, x1 = 90, 570; yt, yb = 160, 260
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    pts = [(x0 + (x1 - x0) * t, ymid - 36 * math.sin(2 * math.pi * t)) for t in [i / 120 for i in range(121)]]
    plot(d, 0, 0, pts, BLUE, 3)
    dim(d, x0, yb + 40, x1, yb + 40, "波長 lambda", col=GRAY)
    arrow(d, 260, 120, 400, 120, BLACK, 3, 13); ctext(d, 330, 104, "音速 c", FS, BLACK)
    ctext(d, 330, 312, "媒質: 体積弾性率 K, 密度 rho", FT, GRAY)
    ctext(d, 330, 342, "c = sqrt(K/rho)  (硬いほど速く・重いほど遅い)", FT)
    save(im, "v1e6WaveSpeedMedium")


# ================================================ 6-3 速度ポテンシャル (helpful)
def f_velocity_potential():
    im, d = new(); title(d, "速度ポテンシャルphiから粒子速度と音圧")
    box(d, 270, 195, 390, 255, (225, 235, 245))
    ctext(d, 330, 225, "phi", FL, BLUE)
    ctext(d, 330, 272, "速度ポテンシャル", FT, GRAY)
    arrow(d, 270, 215, 150, 165, BLACK, 3, 12)
    box(d, 40, 135, 200, 185, FILL1)
    ctext(d, 120, 160, "v = -dphi/dx", FT)
    ctext(d, 120, 200, "粒子速度 (x微分)", FT, GRAY)
    arrow(d, 390, 215, 510, 165, BLACK, 3, 12)
    box(d, 460, 135, 620, 185, FILL1)
    ctext(d, 540, 160, "p = rho dphi/dt", FT)
    ctext(d, 540, 200, "音圧 (時間微分)", FT, GRAY)
    note(d, "1つの関数phiから粒子速度(x微分)と音圧(時間微分)が定まる")
    save(im, "v1e6VelocityPotential")


# ================================================ 6-4 振動平板・ヘルムホルツ (helpful)
def f_plate_helmholtz():
    im, d = new(); title(d, "振動平板近傍の平面波→ヘルムホルツ方程式")
    px = 130
    d.line((px, 110, px, 340), fill=BLACK, width=6)
    for yy in (150, 225, 300):
        arrow(d, px, yy, px + 40, yy, RED, 3, 11)
    ctext(d, px + 10, 92, "振動板 (角振動数 w)", FT, RED, "lm")
    x0, x1 = 180, 560; yt, yb = 170, 280
    duct(d, x0, x1, yt, yb)
    pts = [(x0 + (x1 - x0) * t, (yt + yb) / 2 - 28 * math.sin(2 * math.pi * 1.3 * t)) for t in [i / 120 for i in range(121)]]
    plot(d, 0, 0, pts, BLUE, 3)
    arrow(d, 300, 150, 400, 150, GRAY, 2, 10); ctext(d, 350, 136, "平面波", FT, GRAY)
    box(d, 120, 320, 610, 366, FILL1)
    ctext(d, 365, 343, "phi = Phi(x) e^{jwt}  ->  d2Phi/dx2 + (w/c)^2 Phi = 0", FT)
    note(d, "時間変化をe^{jwt}と仮定 → 空間分布Phiのヘルムホルツ方程式に帰着")
    save(im, "v1e6VibratingPlateHelmholtz")


# ================================================ 6-5 基本境界条件 (helpful)
def f_pressure_bc():
    im, d = new(); title(d, "基本境界条件:端で音圧を規定(Phiの値を固定)")
    x0, x1 = 130, 560; yt, yb = 175, 275
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    d.line((x0, yt, x0, yb), fill=BLACK, width=3)
    d.line((x1, yt, x1, yb), fill=BLACK, width=3)
    ctext(d, x0, yb + 22, "x=0", FT, GRAY); ctext(d, x1, yb + 22, "x=l", FT, GRAY)
    force(d, x0, ymid, 40, 0, "", RED)
    ctext(d, x0 + 4, 140, "p = p0 e^{jwt}", FS, RED, "mm")
    node(d, x0, ymid, 6, RED, RED)
    ctext(d, 345, 320, "未知関数Phiの『値そのもの』を端で指定 = 基本境界条件", FT)
    ctext(d, 345, 348, "Phi0 = -j p0/(rho w)  に換算して固定", FT, GRAY)
    save(im, "v1e6PressureBC")


# ================================================ 6-6 自然境界条件 (helpful)
def f_velocity_bc():
    im, d = new(); title(d, "自然境界条件:端で粒子速度を規定(Phiの微分)")
    x0, x1 = 130, 560; yt, yb = 175, 275
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    d.line((x0, yt, x0, yb), fill=BLACK, width=3); d.line((x1, yt, x1, yb), fill=BLACK, width=3)
    ctext(d, x0, yb + 22, "x=0", FT, GRAY); ctext(d, x1, yb + 22, "x=l", FT, GRAY)
    arrow(d, x1 - 4, ymid, x1 + 44, ymid, RED, 4, 13)
    ctext(d, x1 + 10, 140, "v = vl e^{jwt}", FS, RED, "mm")
    node(d, x1, ymid, 6, RED, RED)
    ctext(d, 345, 320, "未知関数Phiの『微分(勾配)』を端で指定 = 自然境界条件", FT)
    ctext(d, 345, 348, "dPhi/dx = -vl", FT, GRAY)
    save(im, "v1e6VelocityBC")


# ================================================ 6-7 両端剛体壁・ばね支持振動体 (required)
def f_duct_spring_body():
    im, d = new(); title(d, "両端剛体壁の管路+ばね支持振動体(x=l1)")
    x0, x1 = 110, 560; yt, yb = 165, 275
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    wall(d, x0, yt, yb, side=1, n=6)
    wall(d, x1, yt, yb, side=-1, n=6)
    ctext(d, x0 + 4, yt - 16, "剛体壁", FT, GRAY, "lm"); ctext(d, x1 - 4, yt - 16, "剛体壁", FT, GRAY, "rm")
    xb = 330
    box(d, xb - 14, ymid - 40, xb + 14, ymid + 40, FILL2)
    spring(d, xb, yt, xb, ymid - 40, coils=4, amp=10)
    ctext(d, xb + 60, yt + 26, "ks, ms", FT, GRAY, "lm")
    arrow(d, xb, ymid + 70, xb + 46, ymid + 70, BLUE, 3, 11); ctext(d, xb + 54, ymid + 70, "w", FS, BLUE, "lm")
    ctext(d, (x0 + xb) / 2, ymid, "p1, v1", FT, RED)
    ctext(d, (xb + x1) / 2, ymid, "p2, v2", FT, RED)
    dim(d, x0, yb + 44, xb, yb + 44, "l1", col=GRAY)
    dim(d, xb, yb + 44, x1, yb + 44, "l2", col=GRAY)
    dim(d, x0, yb + 76, x1, yb + 76, "l (全長)", col=GRAY)
    note(d, "断面積S・全長l。両端は剛体壁、x=l1にばね支持振動体(質量ms)")
    save(im, "v1e6DuctSpringBody")


# ================================================ 6-8 自由体図(両側音圧) (helpful)
def f_body_force_balance():
    im, d = new(); title(d, "ばね支持振動体の自由体図(左右音圧+ばね力)")
    cx, cy = 330, 230
    box(d, cx - 26, cy - 70, cx + 26, cy + 70, FILL2)
    force(d, cx - 26, cy - 34, 74, 0, "+S p1", RED)
    ctext(d, cx - 130, cy - 56, "左音圧(右向き)", FT, GRAY, "lm")
    force(d, cx + 26, cy - 34, -74, 0, "-S p2", RED)
    ctext(d, cx + 130, cy - 56, "右音圧(左向き)", FT, GRAY, "rm")
    spring(d, cx, 95, cx, cy - 70, coils=4, amp=9)
    force(d, cx, cy + 30, -74, 0, "-ks w", GREEN)
    ctext(d, cx, cy + 100, "ばね復元力", FT, GRAY)
    arrow(d, cx - 26, cy + 70, cx + 40, cy + 70, BLUE, 3, 11); ctext(d, cx + 48, cy + 70, "w (右正)", FT, BLUE, "lm")
    note(d, "ms d2w/dt2 = -ks w + S p1 - S p2  (左右音圧は差として効く)")
    save(im, "v1e6BodyForceBalance")


# ================================================ 6-9 左端振動板・右端ばね支持 (required)
def f_driven_piston_spring():
    im, d = new(); title(d, "左端 振動板・右端 ばね支持振動体の管路")
    x0, x1 = 140, 500; yt, yb = 160, 270
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    d.line((x0, yt, x0, yb), fill=BLACK, width=6)
    arrow(d, x0 - 40, ymid, x0 - 4, ymid, RED, 4, 12)
    ctext(d, x0 - 38, 130, "v0 cos wt", FS, RED, "mm")
    ctext(d, x0, yb + 22, "x=0", FT, GRAY)
    xb = x1
    box(d, xb - 14, ymid - 38, xb + 14, ymid + 38, FILL2)
    spring(d, xb + 14, ymid, 590, ymid, coils=5, amp=11)
    wall(d, 600, ymid - 50, ymid + 50, side=-1, n=5)
    ctext(d, 560, ymid - 68, "ks, ms", FT, GRAY)
    arrow(d, xb, ymid + 64, xb + 42, ymid + 64, BLUE, 3, 11); ctext(d, xb + 50, ymid + 64, "w", FS, BLUE, "lm")
    ctext(d, x1, yb + 22, "x=l", FT, GRAY)
    ctext(d, (x0 + x1) / 2, ymid, "p, v", FT, RED)
    dim(d, x0, yb + 46, x1, yb + 46, "l", col=GRAY)
    note(d, "管内を速度ポテンシャルphiで記述。左端は振動板、右端はばね支持振動体")
    save(im, "v1e6DrivenPistonSpring")


# ================================================ 6-10 速度連続の境界条件 (helpful)
def f_driven_bc_continuity():
    im, d = new(); title(d, "速度連続の境界条件(左端=板速度・右端=体速度)")
    x0, x1 = 150, 510; yt, yb = 170, 280
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    d.line((x0, yt, x0, yb), fill=BLACK, width=6)
    arrow(d, x0 - 38, ymid, x0 - 2, ymid, RED, 4, 12); ctext(d, x0 - 36, 150, "v0 cos wt", FT, RED, "mm")
    arrow(d, x0 + 14, ymid, x0 + 54, ymid, BLUE, 3, 11)
    ctext(d, x0 + 70, 150, "v = v0 cos wt", FT, BLUE, "lm")
    xb = x1
    box(d, xb - 14, ymid - 36, xb + 14, ymid + 36, FILL2)
    arrow(d, xb, ymid + 62, xb + 40, ymid + 62, GREEN, 3, 11); ctext(d, xb + 48, ymid + 62, "dw/dt", FT, GREEN, "lm")
    arrow(d, xb - 54, ymid, xb - 14, ymid, BLUE, 3, 11)
    ctext(d, xb - 60, 150, "v(l,t)=dw/dt", FT, BLUE, "rm")
    ctext(d, x0, yb + 22, "x=0", FT, GRAY); ctext(d, x1, yb + 22, "x=l", FT, GRAY)
    note(d, "連成面では空気の粒子速度が板・振動体の速度に一致(加速度でない)")
    save(im, "v1e6DrivenBCContinuity")


# ================================================ 6-11 右端振動体 自由体図 (helpful)
def f_body_eq_motion():
    im, d = new(); title(d, "右端ばね支持振動体の自由体図")
    cx, cy = 320, 225
    box(d, cx - 26, cy - 70, cx + 26, cy + 70, FILL2)
    force(d, cx - 26, cy - 24, 84, 0, "+S p(l,t)", RED)
    ctext(d, cx - 120, cy - 46, "右端音圧の力", FT, GRAY, "lm")
    spring(d, cx + 26, cy + 30, 470, cy + 30, coils=5, amp=10)
    wall(d, 480, cy - 14, cy + 74, side=-1, n=4)
    force(d, cx, cy + 30, -74, 0, "-ks w", GREEN)
    arrow(d, cx - 26, cy + 82, cx + 40, cy + 82, BLUE, 3, 11); ctext(d, cx + 48, cy + 82, "w", FS, BLUE, "lm")
    note(d, "ms d2w/dt2 = -ks w + S p(l,t)  (音圧は面積Sを掛けて力に)")
    save(im, "v1e6BodyEqMotion")


# ================================================ 6-12 FEM分割 (helpful)
def f_fem_mesh():
    im, d = new(); title(d, "1次元有限要素分割:要素と節点でPhiを未知量に")
    x0, x1 = 90, 570; y = 255
    N = 6
    xs = [x0 + (x1 - x0) * i / N for i in range(N + 1)]
    duct(d, x0, x1, y - 30, y + 30)
    d.line((x0, y, x1, y), fill=BLACK, width=2)
    hbar = [40, 64, 52, 70, 46, 58, 36]
    for i, xx in enumerate(xs):
        d.line((xx, y - 30, xx, y + 30), fill=GRAY, width=2)
        node(d, xx, y, 6, "white")
        ctext(d, xx, y + 48, "x%d" % i, FT, GRAY)
        h = hbar[i]
        d.line((xx, y - 30, xx, y - 30 - h), fill=BLUE, width=3)
        ctext(d, xx, y - 30 - h - 10, "Phi%d" % i, FT, BLUE)
    for i in range(N):
        ctext(d, (xs[i] + xs[i + 1]) / 2, y + 12, "%d" % (i + 1), FT, GRAY)
    dim(d, x0, y + 72, x1, y + 72, "l", col=GRAY)
    note(d, "節点でPhiの値Phi0..PhiNを未知量、途中の値は内挿で定める")
    save(im, "v1e6FemMeshNodes")


# ================================================ 6-13 形状関数 (helpful)
def f_shape_function():
    im, d = new(); title(d, "形状関数(ハット型):自節点で1・隣で0")
    ox, oy = 90, 300; xlen = 480
    N = 6
    axes(d, ox, oy, xlen + 20, 180, "x", "N(x)")
    xs = [ox + xlen * i / N for i in range(N + 1)]
    top = oy - 130
    for i, xx in enumerate(xs):
        d.line((xx, oy, xx, oy + 8), fill=BLACK, width=2)
        ctext(d, xx, oy + 22, "x%d" % i, FT, GRAY)
    ctext(d, ox - 8, top, "1", FT, GRAY, "rm")
    cols = [BLUE, GREEN, RED, ORANGE, BLUE, GREEN, RED]
    for i, xx in enumerate(xs):
        left = xs[i - 1] if i > 0 else xx
        right = xs[i + 1] if i < N else xx
        plot(d, 0, 0, [(left, oy), (xx, top), (right, oy)], cols[i % len(cols)], 3)
    ctext(d, xs[2], top - 16, "N2", FT, GREEN)
    note(d, "Phi(x)=Phi0 N0(x)+Phi1 N1(x)+...+PhiN NN(x) (節点値の線形結合)")
    save(im, "v1e6ShapeFunctionHat")


# ================================================ 6-14 重み付き残差法 (helpful)
def f_weighted_residual():
    im, d = new(); title(d, "重み付き残差法:端を固定・内部を残差式で決定")
    x0, x1 = 90, 570; y = 210
    N = 6
    xs = [x0 + (x1 - x0) * i / N for i in range(N + 1)]
    d.line((x0, y, x1, y), fill=BLACK, width=3)
    for i, xx in enumerate(xs):
        if i == 0 or i == N:
            node(d, xx, y, 8, (255, 225, 225), RED)
        else:
            node(d, xx, y, 7, "white")
    ctext(d, xs[0], y - 24, "Phi0 固定", FT, RED); ctext(d, xs[N], y - 24, "PhiN 固定", FT, RED)
    ctext(d, (xs[1] + xs[N - 1]) / 2, y + 28, "内部節点 = 未知", FT, GRAY)
    box(d, 110, 280, 550, 330, FILL1)
    ctext(d, 330, 305, "int_0^l ( d2Phi/dx2 + k^2 Phi ) W dx = 0   (k=w/c)", FT)
    ctext(d, 330, 356, "端は基本境界条件で固定、内部は残差=0で連立", FT, GRAY)
    save(im, "v1e6WeightedResidual")


# ================================================ 6-15 弱形式化 (helpful)
def f_weak_form():
    im, d = new(); title(d, "形状関数の微分と部分積分による弱形式化")

    def panel(ox, oy, w, kind, lab):
        axes(d, ox, oy, w + 10, 70, "x", "")
        mid = ox + w / 2
        if kind == "N":
            plot(d, 0, 0, [(ox, oy), (mid, oy - 56), (ox + w, oy)], BLUE, 3)
        elif kind == "N1":
            plot(d, 0, 0, [(ox, oy - 26), (mid, oy - 26)], GREEN, 3)
            plot(d, 0, 0, [(mid, oy + 26), (ox + w, oy + 26)], GREEN, 3)
            dsh(d, mid, oy - 26, mid, oy + 26, LGRAY)
        else:
            arrow(d, mid - 1, oy, mid - 1, oy - 48, RED, 3, 11)
            arrow(d, mid + 1, oy, mid + 1, oy + 48, RED, 3, 11)
        ctext(d, ox + w / 2, oy + 56, lab, FT, GRAY)
    panel(70, 150, 150, "N", "N (ハット型)")
    panel(260, 150, 150, "N1", "dN/dx (段差)")
    panel(450, 150, 150, "Nd", "d2N/dx2 (無限大)")
    box(d, 90, 300, 570, 350, FILL1)
    ctext(d, 330, 325, "部分積分: int Phi'' W dx -> -int Phi' W' dx + [Phi' W]", FT)
    note(d, "2階微分が無限大になるのを避け微分階数を1つ下げる(弱形式)")
    save(im, "v1e6WeakForm")


# ================================================ 6-16 未知数の個数 (helpful)
def f_node_unknowns():
    im, d = new(); title(d, "要素数N=10→節点11:既知2・未知9")
    x0, x1 = 70, 590; y = 220
    N = 10
    xs = [x0 + (x1 - x0) * i / N for i in range(N + 1)]
    d.line((x0, y, x1, y), fill=BLACK, width=3)
    for i, xx in enumerate(xs):
        if i == 0 or i == N:
            node(d, xx, y, 8, (255, 225, 225), RED)
        else:
            node(d, xx, y, 8, (225, 235, 250), BLUE)
        ctext(d, xx, y + 24, "%d" % i, FT, GRAY)
    ctext(d, xs[0], y - 24, "既知", FT, RED); ctext(d, xs[N], y - 24, "既知", FT, RED)
    ctext(d, 330, y - 62, "内部 9個 = 未知 (連立方程式は9元)", FT, BLUE)
    ctext(d, 330, 320, "節点数 = N+1 = 11、既知2 → 未知 = N-1 = 9", FT, GRAY)
    save(im, "v1e6NodeUnknowns")


# ================================================ 6-17 吸音率・インピーダンス (helpful)
def f_absorption_impedance():
    im, d = new(); title(d, "吸音率(エネルギー比)と Z密度=p/v")
    ax = 430
    box(d, ax, 120, 560, 330, FILL2)
    for yy in range(130, 330, 18):
        d.line((ax, yy, ax + 30, yy - 12), fill=GRAY, width=1)
    ctext(d, 495, 105, "吸音材", FT, GRAY)
    arrow(d, 150, 170, ax - 4, 200, RED, 4, 13); ctext(d, 210, 158, "入射音 Ei", FT, RED)
    arrow(d, ax - 4, 250, 150, 290, BLUE, 3, 12); ctext(d, 210, 302, "反射音 Er", FT, BLUE)
    ctext(d, 255, 226, "吸音率 = (Ei - Er)/Ei", FT)
    box(d, 90, 344, 380, 388, FILL1)
    ctext(d, 235, 366, "音響インピーダンス密度 Z = p / v", FT)
    save(im, "v1e6AbsorptionImpedance")


# ================================================ 6-18 インテンシティ・パワー (helpful)
def f_intensity_power():
    im, d = new(); title(d, "音響インテンシティの面積分→音響パワー")
    cx, cy = 290, 235
    R = 130
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=GRAY, width=2)
    node(d, cx, cy, 8, RED, RED); ctext(d, cx, cy + 20, "音源", FT, GRAY)
    for k in range(8):
        a = math.radians(k * 45)
        x1 = cx + (R - 30) * math.cos(a); y1 = cy - (R - 30) * math.sin(a)
        x2 = cx + (R + 24) * math.cos(a); y2 = cy - (R + 24) * math.sin(a)
        arrow(d, x1, y1, x2, y2, BLUE, 3, 10)
    ctext(d, cx, cy - R - 26, "インテンシティ I (ベクトル)", FT, BLUE)
    box(d, 470, 250, 620, 320, FILL1)
    ctext(d, 545, 285, "音響パワー\n= 面積分 I.n dS", FT)
    ctext(d, 545, 150, "測定は複数マイク", FT, GRAY)
    save(im, "v1e6IntensityPower")


# ================================================ 6-19 複素インテンシティ (helpful)
def f_complex_intensity():
    im, d = new(); title(d, "複素インテンシティ I=(1/2)p u*")
    cx, cy = 260, 250
    axes(d, cx, cy, 300, 160, "Re (アクティブ)", "Im (リアクティブ)")
    ix, iy = cx + 200, cy - 100
    arrow(d, cx, cy, ix, iy, BLUE, 4, 14); ctext(d, ix + 6, iy - 8, "I", FS, BLUE, "lm")
    dsh(d, ix, iy, ix, cy, LGRAY); dsh(d, ix, iy, cx, iy, LGRAY)
    arrow(d, cx, cy, ix, cy, GREEN, 3, 11); ctext(d, (cx + ix) / 2, cy + 20, "アクティブ(エネルギー伝送)", FT, GREEN)
    arrow(d, cx, cy, cx, iy, RED, 3, 11); ctext(d, cx - 8, iy - 12, "リアクティブ(定在波)", FT, RED, "rm")
    save(im, "v1e6ComplexIntensity")


# ================================================ 6-20 吸音層ダクト (helpful)
def f_lined_duct():
    im, d = new(); title(d, "吸音層ダクト:左右境界のZ・p・vと吸音層長la")
    x0, x1 = 110, 560; yt, yb = 175, 275
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    xm = 360
    for xx in range(xm, x1, 14):
        d.line((xx, yt, xx, yb), fill=LGRAY, width=1)
    d.line((xm, yt, xm, yb), fill=BLACK, width=2)
    ctext(d, (x0 + xm) / 2, ymid, "空気層", FT, GRAY)
    ctext(d, (xm + x1) / 2, ymid, "吸音層", FT, GRAY)
    d.line((x0, yt, x0, yb), fill=RED, width=3)
    ctext(d, x0, yt - 16, "Z1", FT, RED); ctext(d, x0 + 2, yb + 20, "p1,v1", FT, RED)
    d.line((x1, yt, x1, yb), fill=BLUE, width=3)
    ctext(d, x1, yt - 16, "Z2", FT, BLUE); ctext(d, x1 - 2, yb + 20, "p2,v2", FT, BLUE)
    arrow(d, 250, ymid - 46, 300, ymid - 46, GRAY, 2, 9); ctext(d, 275, ymid - 64, "v (右向き)", FT, GRAY)
    dim(d, xm, yb + 44, x1, yb + 44, "la", col=GRAY)
    note(d, "特性インピーダンスza・伝搬定数ga・長さla の吸音層を伝達行列で表す")
    save(im, "v1e6LinedDuctImpedance")


# ================================================ 6-21 板連成2閉空間 (helpful)
def f_plate_cavities():
    im, d = new(); title(d, "音場-弾性体結合系:弾性板で2閉空間V1,V2に仕切る")
    ox, oy = 150, 185; w, h, dp = 360, 175, 70
    dx, dy = int(dp * 0.8), int(dp * 0.5)
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3)
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + w + dx, oy - dy), (ox + w, oy)], outline=BLACK, width=2)
    d.line((ox + w, oy, ox + w + dx, oy - dy), fill=BLACK, width=2)
    d.line((ox + w + dx, oy - dy, ox + w + dx, oy + h - dy), fill=BLACK, width=2)
    d.line((ox + w, oy + h, ox + w + dx, oy + h - dy), fill=BLACK, width=2)
    mx = ox + w / 2
    d.line((mx, oy, mx, oy + h), fill=RED, width=4)
    d.line((mx, oy, mx + dx, oy - dy), fill=RED, width=3)
    ctext(d, mx, oy + h + 18, "弾性板", FT, RED)
    arrow(d, mx, oy + h / 2 + 30, mx + 40, oy + h / 2 + 30, RED, 3, 11); ctext(d, mx + 46, oy + h / 2 + 30, "たわみ(x正)", FT, RED, "lm")
    ctext(d, ox + w * 0.25, oy + h / 2, "V1\nP1", FS, BLUE)
    ctext(d, ox + w * 0.75, oy + h / 2, "V2\nP2", FS, GREEN)
    axes(d, 130, 385, 60, 44, "x", "z")
    arrow(d, 130, 385, 168, 366, GRAY, 2, 9); ctext(d, 174, 362, "y", FT, GRAY, "lm")
    ctext(d, 520, 385, "板以外=剛壁", FT, GRAY)
    save(im, "v1e6PlateCoupledCavities")


# ================================================ 6-22 モード法・相反 (helpful)
def f_modal_reciprocity():
    im, d = new(); title(d, "相反定理:構造加振<->評価点体積加速度加振")

    def panel(ox, srcstruct, lab):
        box(d, ox, 140, ox + 180, 300, FILL1)
        pin = (ox + 30, 260); ev = (ox + 150, 180)
        if srcstruct:
            force(d, pin[0], pin[1] + 44, 0, -34, "F", RED, FT)
            node(d, pin[0], pin[1], 6, RED, RED); ctext(d, pin[0], pin[1] + 62, "入力点", FT, GRAY)
            node(d, ev[0], ev[1], 6, BLUE, BLUE); ctext(d, ev[0] + 6, ev[1] - 14, "評価点 P", FT, BLUE, "lm")
        else:
            node(d, ev[0], ev[1], 6, BLUE, BLUE); ctext(d, ev[0] + 6, ev[1] - 14, "体積加速度", FT, BLUE, "lm")
            for k in range(6):
                a = math.radians(k * 60); arrow(d, ev[0], ev[1], ev[0] + 22 * math.cos(a), ev[1] - 22 * math.sin(a), BLUE, 2, 7)
            node(d, pin[0], pin[1], 6, RED, RED); ctext(d, pin[0], pin[1] + 18, "入力点 応答", FT, RED)
        ctext(d, ox + 90, 322, lab, FT, GRAY)
    panel(60, True, "(a) 構造加振 F -> 評価点音圧 P")
    d.line((330, 100, 330, 350), fill=LGRAY, width=1)
    panel(360, False, "(b) 評価点を体積加速度で加振")
    note(d, "相反定理: P/F は加振点と評価点を入れ替えても等しい")
    save(im, "v1e6ModalReciprocity")


# ================================================ 6-23 音響管モード (helpful)
def f_duct_mode_shape():
    im, d = new(); title(d, "音響管の1次音圧モード phi=cos(pi x/l)")
    x0, x1 = 130, 500; yt, yb = 170, 280
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    wall(d, x0, yt, yb, side=1, n=6)
    xb = x1
    box(d, xb - 14, ymid - 34, xb + 14, ymid + 34, FILL2); ctext(d, xb + 26, ymid - 48, "m", FT, GRAY, "lm")
    spring(d, xb + 14, ymid, 580, ymid, coils=5, amp=10)
    wall(d, 590, ymid - 46, ymid + 46, side=-1, n=4)
    ctext(d, 552, ymid + 40, "k", FT, GRAY)
    ctext(d, x0, yb + 22, "x=0", FT, GRAY); ctext(d, x1, yb + 22, "x=l", FT, GRAY)
    pts = [(x0 + (x1 - x0) * t, ymid - 40 * math.cos(math.pi * t)) for t in [i / 80 for i in range(81)]]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, (x0 + x1) / 2, ymid - 58, "phi = cos(pi x/l)", FT, BLUE)
    note(d, "両端剛壁とみた1次モード:両端で振幅大・中央で0")
    save(im, "v1e6DuctModeShape")


# ================================================ 6-24 連成行列 非対称 (helpful)
def f_coupling_matrix_asym():
    im, d = new(); title(d, "連成の全体行列は非対称・相反定理は成立")
    ox, oy, cell = 120, 130, 88
    matrix_grid(d, ox, oy, [["Ks", "A"], ["0", "Ka"]], cell=cell, highlight=(0, 1), fnt=FS)
    ctext(d, ox + cell, oy - 18, "非対称 (A が上のみ)", FT, RED)
    ctext(d, ox + cell, oy + 2 * cell + 20, "[K] 全体剛性行列", FT, GRAY)
    box(d, 380, 150, 610, 300, FILL1)
    ctext(d, 495, 185, "相反定理は成立", FS, GREEN)
    ctext(d, 495, 232, "構造入力点の力 F\n<-> 受音点音圧 P", FT, GRAY)
    ctext(d, 495, 278, "同じ周波数応答関数", FT, GRAY)
    note(d, "連成で固有周波数は単体からずれる・FEMとBEMは併用可")
    save(im, "v1e6CouplingMatrixAsym")


# ================================================ 6-25 波長基準メッシュ (helpful)
def f_wavelength_mesh():
    im, d = new(); title(d, "要素分割の目安:波長の1/6〜1/8")
    ox, oy = 90, 230; xlen = 480
    axes(d, ox, oy, xlen + 20, 90, "x", "")
    pts = [(ox + xlen * t, oy - 60 * math.sin(2 * math.pi * t)) for t in [i / 120 for i in range(121)]]
    plot(d, 0, 0, pts, BLUE, 3)
    dim(d, ox, oy + 95, ox + xlen, oy + 95, "波長 lambda", col=GRAY)
    n = 8
    for i in range(n + 1):
        xx = ox + xlen * i / n
        d.line((xx, oy - 70, xx, oy + 70), fill=LGRAY, width=1)
        node(d, xx, oy, 4, "white")
    ctext(d, 330, 355, "要素サイズ = lambda/6 〜 lambda/8", FT)
    save(im, "v1e6WavelengthMesh")


# ================================================ 6-26 音響モード採用範囲 (helpful)
def f_acoustic_mode_range():
    im, d = new(); title(d, "音響モードの採用範囲 f=c/lambda")
    box(d, 110, 130, 420, 330, "white", BLACK, 4)
    ctext(d, 265, 350, "パッケージ(鋼製平板の箱)", FT, GRAY)
    node(d, 265, 235, 9, RED, RED); ctext(d, 265, 255, "圧縮機(点音源)", FT, GRAY)
    for k in range(8):
        a = math.radians(k * 45); arrow(d, 265, 235, 265 + 30 * math.cos(a), 235 - 30 * math.sin(a), BLUE, 1, 6)
    pts = [(110 + 310 * t, 130 - 14 * math.sin(2 * math.pi * 6 * t)) for t in [i / 120 for i in range(121)]]
    plot(d, 0, 0, pts, GREEN, 2)
    ctext(d, 265, 100, "構造の最小波長 lambda", FT, GREEN)
    box(d, 450, 190, 620, 275, FILL1)
    ctext(d, 535, 232, "f = c/lambda\n(高い音響固有振動数)", FT)
    save(im, "v1e6AcousticModeRange")


# ================================================ 6-27 自由音場+隙間 (helpful)
def f_free_field_gap():
    im, d = new(); title(d, "自由音場+点音源:小隙間のヘルムホルツ共鳴")
    cx, cy = 300, 235
    for r in (150, 162, 174):
        d.ellipse((cx - r - 40, cy - r, cx + r + 40, cy + r), outline=LGRAY, width=1)
    ctext(d, cx, 400, "吸収境界 (PML)", FT, GRAY)
    box(d, 220, 175, 380, 300, FILL2)
    box(d, 250, 205, 350, 285, "white")
    d.line((295, 175, 295, 205), fill="white", width=6)
    d.line((305, 175, 305, 205), fill="white", width=6)
    arrow(d, 300, 145, 300, 190, RED, 2, 9); ctext(d, 330, 145, "小さな隙間=のど", FT, RED, "lm")
    ctext(d, 300, 245, "空洞", FT, GRAY)
    node(d, 520, 235, 8, RED, RED); ctext(d, 520, 255, "点音源", FT, GRAY)
    note(d, "隙間が小さくてもヘルムホルツ共鳴を作りうる→モデル化が要る場合")
    save(im, "v1e6FreeFieldGap")


# ================================================ 6-28 不拘束モード留意点 (helpful)
def f_unconstrained_mode():
    im, d = new(); title(d, "不拘束モードの留意点:剰余剛性・半波長・多点拘束")
    box(d, 60, 120, 210, 210, FILL1)
    ctext(d, 135, 104, "(a)集中加振", FT, GRAY)
    arrow(d, 135, 252, 135, 212, RED, 3, 11); node(d, 135, 210, 5, RED, RED)
    ctext(d, 135, 272, "剰余剛性を加振点に", FT)
    ox, oy = 250, 165
    pts = [(ox + 180 * t, oy - 24 * math.sin(2 * math.pi * t)) for t in [i / 100 for i in range(101)]]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 90, 104, "(b)構造振動の腹", FT, GRAY)
    dim(d, ox + 45, oy + 40, ox + 135, oy + 40, "半波長", col=GRAY)
    ctext(d, ox + 90, oy + 72, "半波長まで採用", FT)
    ox2 = 480
    for i in range(4):
        node(d, ox2, 150 + i * 30, 5, BLUE)
    for j in range(3):
        node(d, ox2 + 90, 160 + j * 40, 5, GREEN)
    for i in range(4):
        for j in range(3):
            dsh(d, ox2, 150 + i * 30, ox2 + 90, 160 + j * 40, LGRAY)
    ctext(d, ox2 + 45, 104, "(c)連成面", FT, GRAY)
    ctext(d, ox2 + 45, 300, "多点拘束で結合", FT)
    save(im, "v1e6UnconstrainedMode")


# ================================================ 6-29 音響剛体モード (helpful)
def f_rigid_body_mode():
    im, d = new(); title(d, "音響剛体モード:一様圧力・1個・0Hz")
    box(d, 150, 140, 470, 320, FILL1, BLACK, 4)
    wall(d, 150, 140, 320, side=1, n=6)
    wall(d, 470, 140, 320, side=-1, n=6)
    hwall(d, 150, 470, 140, side=-1, n=10)
    hwall(d, 150, 470, 320, side=1, n=10)
    ctext(d, 305, 228, "圧力 p が一様分布\n(断熱変化)", FS, BLUE)
    arrow(d, 470, 230, 522, 230, RED, 3, 12); ctext(d, 530, 230, "境界の垂直速度\n→体積変化で励起", FT, RED, "lm")
    ctext(d, 305, 355, "剛体モードは1個・固有振動数 0 Hz", FT, GRAY)
    save(im, "v1e6RigidBodyMode")


# ================================================ 6-30 3次元連成FEM式 (helpful)
def f_coupled_3d_matrix():
    im, d = new(); title(d, "3次元連成FEM式:Aで非対称・実固有値で低次元化")
    ox, oy, cell = 95, 130, 72
    matrix_grid(d, ox, oy, [["Ms", "0"], ["-A^T", "Ma"]], cell=cell, highlight=(1, 0), fnt=FT)
    ctext(d, ox + cell, oy + 2 * cell + 16, "[M]", FT, GRAY)
    ox2 = 335
    matrix_grid(d, ox2, oy, [["Ks", "A"], ["0", "Ka"]], cell=cell, highlight=(0, 1), fnt=FT)
    ctext(d, ox2 + cell, oy + 2 * cell + 16, "[K]", FT, GRAY)
    ctext(d, 330, 305, "xs=構造変位、xa=音響音圧", FT, BLUE)
    ctext(d, 330, 331, "連成行列Aにより全体行列は非対称", FT, RED)
    ctext(d, 330, 357, "減衰とAを無視した実固有値解析で低次元化→非対角", FT, GRAY)
    save(im, "v1e6Coupled3DMatrix")


# ================================================ 6-31 車室加振比較 (helpful)
def f_car_cabin_excitation():
    im, d = new(); title(d, "固体伝播騒音:(a)構造加振と(b)音響加振の比較")

    def car(ox, mode, lab):
        pts = [(ox, 300), (ox, 250), (ox + 40, 250), (ox + 70, 200), (ox + 150, 200), (ox + 175, 250), (ox + 230, 250), (ox + 230, 300)]
        d.line(pts, fill=BLACK, width=3, joint="curve")
        d.line((ox, 300, ox + 230, 300), fill=BLACK, width=3)
        for wx in (ox + 50, ox + 185):
            d.ellipse((wx - 16, 296, wx + 16, 328), outline=BLACK, width=3)
        for (ax, ay) in [(ox + 40, 250), (ox + 110, 200), (ox + 175, 250)]:
            node(d, ax, ay, 4, RED, RED)
        if mode == "struct":
            arrow(d, ox + 115, 342, ox + 115, 302, RED, 3, 11)
            ctext(d, ox + 115, 360, "加振機(構造加振)", FT, GRAY)
        else:
            node(d, ox + 110, 245, 7, BLUE, BLUE)
            for k in range(6):
                a = math.radians(k * 60); arrow(d, ox + 110, 245, ox + 110 + 20 * math.cos(a), 245 - 20 * math.sin(a), BLUE, 2, 7)
            ctext(d, ox + 115, 360, "スピーカ(音響加振)", FT, GRAY)
        ctext(d, ox + 115, 178, lab, FT)
    car(70, "struct", "(a) 構造加振")
    d.line((335, 110, 335, 375), fill=LGRAY, width=1)
    car(360, "speaker", "(b) 音響加振")
    ctext(d, 330, 400, "赤点=加速度計。加振方法で励起モードが変わり分布は一致しにくい", FT, GRAY)
    save(im, "v1e6CarCabinExcitation")


# ================================================ 6-32 自由音場FEM (helpful)
def f_free_field_fem():
    im, d = new(); title(d, "自由音場のFEM:一次テトラ要素+点音源")
    box(d, 250, 200, 350, 290, FILL2); ctext(d, 300, 245, "構造体", FT, GRAY)
    ring = [(150, 150), (300, 120), (460, 150), (520, 240), (460, 340), (300, 370), (150, 340), (120, 240)]
    for (px, py) in ring:
        node(d, px, py, 3, "white")
    for i in range(len(ring)):
        a = ring[i]; b = ring[(i + 1) % len(ring)]
        d.line((a[0], a[1], b[0], b[1]), fill=LGRAY, width=1)
    corners = [(250, 200), (350, 200), (350, 290), (250, 290)]
    for (px, py) in ring:
        nearest = min(corners, key=lambda c: (c[0] - px) ** 2 + (c[1] - py) ** 2)
        d.line((px, py, nearest[0], nearest[1]), fill=LGRAY, width=1)
    node(d, 500, 130, 8, RED, RED); ctext(d, 500, 112, "点音源", FT, GRAY)
    note(d, "線形音場は一次要素でも比較的精度が保てる")
    save(im, "v1e6FreeFieldFEM")


# ================================================ 6-33 車室内装吸音 (helpful)
def f_cabin_interior_absorb():
    im, d = new(); title(d, "車室内装の吸音:内装材に Z=p/v を定義")
    pts = [(120, 320), (120, 230), (200, 180), (430, 180), (470, 230), (540, 230), (540, 320)]
    d.line(pts, fill=BLACK, width=3, joint="curve")
    d.line((120, 320, 540, 320), fill=BLACK, width=3)
    for xx in range(210, 420, 16):
        d.line((xx, 182, xx + 8, 190), fill=RED, width=2)
    ctext(d, 315, 165, "ルーフライナ", FT, RED)
    box(d, 250, 250, 320, 318, FILL2)
    box(d, 232, 220, 252, 260, FILL2)
    ctext(d, 285, 336, "シート", FT, GRAY)
    box(d, 470, 232, 538, 260, FILL2); ctext(d, 505, 300, "インパネ", FT, GRAY)
    ctext(d, 320, 258, "内装材に Z = p/v", FT, BLUE)
    note(d, "音響インピーダンス密度 Z=音圧/粒子速度 を各吸音面に与える")
    save(im, "v1e6CabinInteriorAbsorb")


# ================================================ 6-34 建機キャビン (helpful)
def f_construction_cabin():
    im, d = new(); title(d, "建機キャビン:内部吸音材と音圧分布計算")
    box(d, 80, 300, 300, 360, FILL2)
    d.ellipse((70, 350, 320, 395), outline=BLACK, width=3)
    box(d, 150, 200, 270, 300, "white", BLACK, 3)
    ctext(d, 210, 190, "キャビン", FT, GRAY)
    box(d, 175, 255, 210, 298, FILL2); d.line((175, 255, 175, 230), fill=BLACK, width=3)
    ctext(d, 232, 272, "内装材(吸音)", FT, RED, "lm")
    d.line((300, 320, 430, 220), fill=BLACK, width=6)
    d.line((430, 220, 520, 300), fill=BLACK, width=6)
    d.line((520, 300, 560, 340), fill=BLACK, width=5)
    for k in range(3):
        d.ellipse((165 + k * 6, 215 + k * 6, 255 - k * 6, 285 - k * 6), outline=LGRAY, width=1)
    ctext(d, 210, 235, "音圧分布", FT, BLUE)
    note(d, "キャビン内の音圧分布を、内装吸音材をモデル化して計算")
    save(im, "v1e6ConstructionCabin")


# ================================================ 6-35 窓ガラス透過音 (helpful)
def f_cabin_glass_mesh():
    im, d = new(); title(d, "窓ガラス透過音:ガラスをメッシュ分割")
    box(d, 300, 150, 470, 320, "white", BLACK, 3); ctext(d, 385, 135, "キャビン", FT, GRAY)
    d.line((300, 150, 300, 320), fill=BLUE, width=5)
    for yy in range(150, 321, 20):
        d.line((296, yy, 304, yy), fill=BLUE, width=1)
    ctext(d, 268, 235, "窓ガラス\n(メッシュ)", FT, BLUE, "rm")
    box(d, 90, 250, 240, 340, FILL2); ctext(d, 165, 305, "エンジン", FT, GRAY)
    node(d, 165, 285, 7, RED, RED)
    arrow(d, 175, 270, 296, 235, RED, 3, 12)
    arrow(d, 306, 235, 390, 235, RED, 3, 12)
    node(d, 400, 235, 6, BLACK); ctext(d, 400, 218, "耳元", FT, GRAY)
    note(d, "構造と音波で波長の小さいほうに合わせ、波長の1/8を目安にメッシュ")
    save(im, "v1e6CabinGlassMesh")


# ================================================ 6-36 相反定理キャビン (helpful)
def f_reciprocity_cabin():
    im, d = new(); title(d, "相反定理でキャビン内音圧を予測")
    box(d, 260, 170, 400, 300, "white", BLACK, 3)
    ctext(d, 330, 155, "キャビン壁面", FT, GRAY)
    node(d, 120, 235, 8, RED, RED); ctext(d, 120, 258, "騒音源\n(単位体積速度)", FT, GRAY)
    arrow(d, 135, 235, 256, 220, RED, 3, 11)
    ctext(d, 195, 190, "外表面音圧", FT, RED)
    node(d, 330, 235, 7, BLUE, BLUE); ctext(d, 330, 260, "評価点(耳元)\n単位体積速度音源", FT, BLUE)
    for k in range(6):
        a = math.radians(k * 60); arrow(d, 330, 235, 330 + 18 * math.cos(a), 235 - 18 * math.sin(a), BLUE, 2, 7)
    arrow(d, 352, 205, 398, 192, BLUE, 3, 11); ctext(d, 470, 188, "壁面の振動速度", FT, BLUE, "mm")
    ctext(d, 330, 345, "外表面音圧 × 壁面振動速度 → 内部評価点の音圧", FT)
    save(im, "v1e6ReciprocityCabin")


# ================================================ 6-37 鉄道車輪放射音 (helpful)
def f_rail_wheel_radiation():
    im, d = new(); title(d, "鉄道車輪の振動放射音:反射面と観測点")
    cx, cy = 235, 215
    d.ellipse((cx - 90, cy - 90, cx + 90, cy + 90), outline=BLACK, width=4)
    d.ellipse((cx - 78, cy - 78, cx + 78, cy + 78), outline=BLACK, width=2)
    d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, cy, "ハブ", FT, GRAY)
    for k in range(6):
        a = math.radians(k * 60)
        d.line((cx + 26 * math.cos(a), cy + 26 * math.sin(a), cx + 78 * math.cos(a), cy + 78 * math.sin(a)), fill=GRAY, width=1)
    ctext(d, cx + 58, cy - 58, "ウェブ", FT, GRAY, "lm")
    ctext(d, cx - 96, cy + 82, "フランジ/踏面", FT, GRAY, "rm")
    arrow(d, cx, cy - 140, cx, cy - 95, RED, 3, 12); ctext(d, cx + 8, cy - 132, "上下加振", FT, RED, "lm")
    hwall(d, 100, 560, cy + 122, side=1, n=14)
    ctext(d, 175, cy + 142, "スラブ軌道(反射面)", FT, GRAY)
    node(d, 505, 175, 7, BLACK); ctext(d, 505, 158, "観測点", FT, GRAY)
    arrow(d, cx + 85, cy - 40, 495, 175, BLUE, 2, 10); ctext(d, 410, 108, "直接音", FT, BLUE)
    arrow(d, cx + 70, cy + 80, 355, cy + 120, GREEN, 2, 9)
    arrow(d, 365, cy + 118, 497, 190, GREEN, 2, 10); ctext(d, 430, cy + 92, "反射音", FT, GREEN, "lm")
    save(im, "v1e6RailWheelRadiation")


# ================================================ main
def main():
    f_plane_wave_eqs()
    f_wave_speed()
    f_velocity_potential()
    f_plate_helmholtz()
    f_pressure_bc()
    f_velocity_bc()
    f_duct_spring_body()
    f_body_force_balance()
    f_driven_piston_spring()
    f_driven_bc_continuity()
    f_body_eq_motion()
    f_fem_mesh()
    f_shape_function()
    f_weighted_residual()
    f_weak_form()
    f_node_unknowns()
    f_absorption_impedance()
    f_intensity_power()
    f_complex_intensity()
    f_lined_duct()
    f_plate_cavities()
    f_modal_reciprocity()
    f_duct_mode_shape()
    f_coupling_matrix_asym()
    f_wavelength_mesh()
    f_acoustic_mode_range()
    f_free_field_gap()
    f_unconstrained_mode()
    f_rigid_body_mode()
    f_coupled_3d_matrix()
    f_car_cabin_excitation()
    f_free_field_fem()
    f_cabin_interior_absorb()
    f_construction_cabin()
    f_cabin_glass_mesh()
    f_reciprocity_cabin()
    f_rail_wheel_radiation()


if __name__ == "__main__":
    main()
