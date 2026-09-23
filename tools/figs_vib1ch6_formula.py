# -*- coding: utf-8 -*-
"""振動1級 第6章「音響連成系の解析基礎」公式・用語図 9枚。figlibで白地660x420線画。
文字化け回避のためギリシャ文字・記号は英字/簡易表記(omega,rho,lambda,phi等)に置換。"""
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


# 1. Plane-wave basics: continuity + momentum -> wave eq, sound speed
def f_planewave():
    im, d = new()
    title(d, "平面波の基礎2式 -> 波動方程式 (音速 c=sqrt(K/rho))")
    # thin tube with a travelling pressure wave
    tx0, tx1, cy = 90, 570, 150
    box(d, tx0, cy - 38, tx1, cy + 38, "white")
    pts = []
    for i in range(0, 121):
        t = i / 120.0
        x = tx0 + t * (tx1 - tx0)
        yy = cy - 26 * math.sin(2 * math.pi * 1.5 * t)
        pts.append((x, yy))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, tx0 + 60, cy - 48, "p (音圧)", FT, BLUE, "lm")
    # propagation direction c
    arrow(d, 250, cy + 60, 410, cy + 60, RED, 3, 13)
    ctext(d, 420, cy + 60, "伝搬 c", FT, RED, "lm")
    # particle velocity
    force(d, 150, cy, 40, 0, "v", GREEN)
    # equations
    ctext(d, 330, 250, "連続の式:  dv/dx = -(1/K) dp/dt", FS, BLACK)
    ctext(d, 330, 284, "運動方程式: rho dv/dt = -dp/dx", FS, BLACK)
    ctext(d, 330, 322, "=> d^2p/dx^2 = (1/c^2) d^2p/dt^2 ,  c=sqrt(K/rho)", FS, RED)
    note(d, "p,v の2式から片方を消去=波動方程式。硬く(K大)軽い(rho小)ほど音は速い")
    save(im, "v1f6PlaneWave")


# 2. Closed-closed pipe: pressure eigen-mode cos(n pi x / l)
def f_pipemode():
    im, d = new()
    title(d, "両端閉口管の音圧固有モード  phi_n = cos(n pi x / l)")
    tx0, tx1, cy = 120, 540, 200
    box(d, tx0, cy - 70, tx1, cy + 70, "white")
    # closed rigid ends
    d.line((tx0, cy - 70, tx0, cy + 70), fill=BLACK, width=6)
    d.line((tx1, cy - 70, tx1, cy + 70), fill=BLACK, width=6)
    ctext(d, tx0, cy + 90, "剛壁 (v=0)", FT, GRAY)
    ctext(d, tx1, cy + 90, "剛壁 (v=0)", FT, GRAY)
    dash(d, tx0, cy, tx1, cy, LGRAY)
    for n, col, amp in [(1, BLUE, 52), (2, RED, 40)]:
        pts = []
        for i in range(0, 121):
            t = i / 120.0
            x = tx0 + t * (tx1 - tx0)
            yy = cy - amp * math.cos(n * math.pi * t)
            pts.append((x, yy))
        plot(d, 0, 0, pts, col, 3)
    ctext(d, tx1 - 20, cy - 60, "n=1", FT, BLUE, "rm")
    ctext(d, tx1 - 20, cy - 34, "n=2", FT, RED, "rm")
    ctext(d, 330, 320, "両端で音圧が腹(速度ゼロ)。 f_n = n c / (2 l)  (n=1,2,3,...)", FS, BLACK)
    note(d, "整数倍で共鳴。1次は両端で音圧最大・中央でゼロ")
    save(im, "v1f6PipeMode")


# 3. Complex intensity: active / reactive decomposition
def f_complexintensity():
    im, d = new()
    title(d, "複素音響インテンシティ  I = (1/2) p u*")
    ox, oy = 210, 300
    axes(d, ox, oy, 300, 210, "Re (アクティブ)", "Im (リアクティブ)")
    # a complex intensity vector
    Ix, Iy = 200, 130
    arrow(d, ox, oy, ox + Ix, oy - Iy, BLUE, 3, 13)
    ctext(d, ox + Ix + 8, oy - Iy - 10, "I", F, BLUE, "lm")
    # active (real) component
    arrow(d, ox, oy, ox + Ix, oy, RED, 2, 11)
    dash(d, ox + Ix, oy, ox + Ix, oy - Iy, LGRAY)
    ctext(d, ox + Ix / 2, oy + 18, "アクティブ Re[I]", FT, RED)
    # reactive (imag) component
    arrow(d, ox, oy, ox, oy - Iy, GREEN, 2, 11)
    ctext(d, ox - 8, oy - Iy / 2, "リアクティブ Im[I]", FT, GREEN, "rm")
    ctext(d, 330, 356, "進行波=実数(伝搬),  定在波=純虚数(その場で往復)", FS, BLACK)
    note(d, "u* は u の複素共役。実部が正味に運ばれる音のエネルギー")
    save(im, "v1f6ComplexIntensity")


# 4. Hat-type shape functions N_i
def f_shapefunc():
    im, d = new()
    title(d, "ハット型形状関数 N_i  (Phi(x)=sum Phi_i N_i)")
    base = 300
    xs = [130, 250, 370, 490, 550]
    d.line((100, base, 580, base), fill=BLACK, width=2)
    # nodes
    labels = ["i-1", "i", "i+1", "", ""]
    for x, lb in zip(xs, labels):
        node(d, x, base, 5, BLACK)
        if lb:
            ctext(d, x, base + 18, lb, FT, GRAY)
    top = 180
    # central hat N_i at x=250..490 peak 370
    plot(d, 0, 0, [(250, base), (370, top), (490, base)], BLUE, 4)
    ctext(d, 370, top - 16, "N_i =1", FT, BLUE)
    # neighbour hats (gray)
    plot(d, 0, 0, [(130, base), (250, top), (370, base)], LGRAY, 2)
    plot(d, 0, 0, [(370, base), (490, top), (550, base)], LGRAY, 2)
    ctext(d, 250, top + 4, "N_{i-1}", FT, GRAY)
    ctext(d, 490, top + 4, "N_{i+1}", FT, GRAY)
    ctext(d, 330, 348, "各節点で1・隣で0の三角形。要素内は節点値の直線内挿", FS, BLACK)
    note(d, "未知量は節点値 Phi_i だけ。連続分布を少ない自由度で近似")
    save(im, "v1f6ShapeFunc")


# 5. Wavelength-based mesh (lambda/6 - lambda/8)
def f_mesh():
    im, d = new()
    title(d, "波長基準の要素分割  (1波長 lambda を 6〜8分割)")
    x0, x1, cy = 110, 550, 190
    # one wavelength sine
    pts = []
    for i in range(0, 161):
        t = i / 160.0
        x = x0 + t * (x1 - x0)
        yy = cy - 55 * math.sin(2 * math.pi * t)
        pts.append((x, yy))
    plot(d, 0, 0, pts, BLUE, 3)
    dash(d, x0, cy, x1, cy, LGRAY)
    # 8 element divisions
    nseg = 8
    base = 300
    d.line((x0, base, x1, base), fill=BLACK, width=2)
    for k in range(nseg + 1):
        x = x0 + k * (x1 - x0) / nseg
        d.line((x, base - 12, x, base + 12), fill=BLACK, width=2)
    for k in range(nseg):
        xm = x0 + (k + 0.5) * (x1 - x0) / nseg
        node(d, xm, base, 4, RED)
    dim(d, x0, 120, x1, 120, "lambda (1波長)", col=GRAY)
    ctext(d, 330, 340, "要素サイズ <= lambda/6 〜 lambda/8。 構造波と音波の短い方に合わせる", FS, BLACK)
    note(d, "1波を6〜8要素で表せないと波が正しく再現できない")
    save(im, "v1f6Mesh")


# 6. Two closed spaces divided by an elastic panel; force = pressure diff
def f_panelcoupling():
    im, d = new()
    title(d, "弾性板で仕切る2閉空間  (外力 = 音圧差 PS1-PS2)")
    y0, y1 = 110, 300
    # outer rigid walls (hatch top/bottom + left/right)
    box(d, 90, y0, 570, y1, "white")
    hwall(d, 90, 570, y0, -1, 14)
    hwall(d, 90, 570, y1, 1, 14)
    wall(d, 90, y0, y1, 1, 9)
    wall(d, 570, y0, y1, -1, 9)
    # deflected elastic plate near middle (bulges to the right)
    cyp = (y0 + y1) / 2
    pts = []
    for i in range(0, 61):
        t = i / 60.0
        yy = y0 + 6 + t * (y1 - y0 - 12)
        xx = 330 + 30 * math.sin(math.pi * t)
        pts.append((xx, yy))
    d.line(pts, fill=BLACK, width=6, joint="curve")
    ctext(d, 300, y0 - 2, "弾性板 u", FT, BLACK)
    # spaces + pressures
    ctext(d, 200, cyp, "閉空間1\nPS1", FS, BLUE)
    ctext(d, 470, cyp, "閉空間2\nPS2", FS, GREEN)
    # pressure pushing the plate
    force(d, 250, cyp - 40, 46, 0, "PS1", RED)
    force(d, 430, cyp + 40, -46, 0, "PS2", RED)
    ctext(d, 330, 332, "rho_p h_p u'' + D (d4u/dy4+2d4u/dy2z2+d4u/dz4) = PS1 - PS2", FS, BLACK)
    note(d, "板を音圧差が押し、板の動きが両側の音場をまた変える相互作用")
    save(im, "v1f6PanelCoupling")


# 7. Acoustic tube + spring-supported vibrator coupling
def f_pipevib():
    im, d = new()
    title(d, "音響管 + ばね支持振動体の連成系")
    tx0, tx1, cy = 90, 570, 210
    ty0, ty1 = cy - 60, cy + 60
    box(d, tx0, ty0, tx1, ty1, "white")
    # rigid closed ends
    d.line((tx0, ty0, tx0, ty1), fill=BLACK, width=6)
    d.line((tx1, ty0, tx1, ty1), fill=BLACK, width=6)
    ctext(d, tx0 + 4, ty1 + 16, "剛壁 v1=0", FT, GRAY, "lm")
    ctext(d, tx1 - 4, ty1 + 16, "剛壁 v2=0", FT, GRAY, "rm")
    # left air p1, right air p2
    ctext(d, 190, cy, "空気 p1", FS, BLUE)
    ctext(d, 470, cy, "空気 p2", FS, GREEN)
    # vibrator mass at center, supported by spring from ceiling
    mx = 330
    spring(d, mx, ty0, mx, cy - 20, coils=5, amp=11, wd=2)
    box(d, mx - 26, cy - 20, mx + 26, cy + 36, FILL2)
    ctext(d, mx, cy + 8, "m_s", FS, BLACK)
    ctext(d, mx + 40, ty0 + 26, "k_s", FT, BLACK, "lm")
    # pressures pushing on the vibrator faces (area S)
    arrow(d, mx - 72, cy + 6, mx - 30, cy + 6, RED, 4, 13)
    ctext(d, mx - 78, cy + 6, "S p1", FT, RED, "rm")
    arrow(d, mx + 72, cy + 6, mx + 30, cy + 6, RED, 4, 13)
    ctext(d, mx + 78, cy + 6, "S p2", FT, RED, "lm")
    # displacement w
    arrow(d, mx, cy + 48, mx + 40, cy + 48, ORANGE, 2, 10)
    ctext(d, mx + 46, cy + 48, "w", FT, ORANGE, "lm")
    ctext(d, 330, 332, "m_s w'' = -k_s w + S p1(l1,t) - S p2(l1,t)", FS, BLACK)
    note(d, "空気圧が振動体を動かし、振動体の動きが空気を圧縮する連成の最小モデル")
    save(im, "v1f6PipeVib")


# 8. Dynamic-absorber effect: single peak splits into two
def f_twopeak():
    im, d = new()
    title(d, "動吸振器効果  1ピーク -> 2ピークに分裂")
    ox, oy = 120, 320
    axes(d, ox, oy, 440, 240, "周波数 f", "音圧応答")
    fc = ox + 220  # acoustic 1st resonance location
    dash(d, fc, oy, fc, oy - 230, LGRAY)
    ctext(d, fc, oy + 18, "音響1次 f", FT, GRAY)
    # without damper: single tall peak (gray dashed)
    pts1 = []
    for i in range(0, 221):
        x = ox + i * 2
        r = 200 / (1 + ((x - fc) / 20.0) ** 2)
        pts1.append((x, oy - r))
    for k in range(0, len(pts1) - 1, 2):
        d.line((pts1[k][0], pts1[k][1], pts1[k + 1][0], pts1[k + 1][1]), fill=GRAY, width=2)
    ctext(d, fc + 70, oy - 190, "吸振器なし", FT, GRAY, "lm")
    # with tuned damper: two peaks
    pts2 = []
    for i in range(0, 221):
        x = ox + i * 2
        r = 150 / (1 + ((x - (fc - 55)) / 16.0) ** 2) + 150 / (1 + ((x - (fc + 55)) / 16.0) ** 2)
        pts2.append((x, oy - min(r, 175)))
    plot(d, 0, 0, pts2, BLUE, 3)
    ctext(d, fc - 55, oy - 160, "2ピーク", FT, BLUE)
    ctext(d, 330, 356, "機械系の固有振動数を音響1次に一致 -> ピークが2つに割れる", FS, BLACK)
    note(d, "減衰が小さいほど分裂が明瞭。共鳴のピークを抑える音響版")
    save(im, "v1f6TwoPeak")


# 9. Absorbing-layer duct: transfer matrix
def f_ducttransfer():
    im, d = new()
    title(d, "吸音層ダクトの伝達マトリクス")
    # duct with absorbing layer
    tx0, tx1, cy = 90, 570, 120
    box(d, tx0, cy - 40, tx1, cy + 40, "white")
    # absorbing layer region hatched
    ax0, ax1 = 230, 430
    box(d, ax0, cy - 40, ax1, cy + 40, FILL2)
    for x in range(ax0, ax1, 14):
        d.line((x, cy - 40, x + 20, cy + 40), fill=LGRAY, width=1)
    ctext(d, (ax0 + ax1) / 2, cy, "吸音層 (z_a, gamma_a, l_a)", FT, GRAY)
    # input / output ports
    arrow(d, 120, cy, 170, cy, BLUE, 3, 12)
    ctext(d, 140, cy - 24, "p1, S v1", FT, BLUE)
    arrow(d, 490, cy, 540, cy, GREEN, 3, 12)
    ctext(d, 500, cy - 24, "p2, S v2", FT, GREEN)
    # transfer relation with 2x2 symbolic matrix
    ctext(d, 150, 235, "{p1, S v1} =", FS, BLACK, "lm")
    matrix_grid(d, 300, 200, [["A", "B"], ["C", "D"]], cell=52, fnt=FS)
    ctext(d, 420, 235, "{p2, S v2}", FS, BLACK, "lm")
    # legend
    ctext(d, 330, 330, "A=D=cosh(gamma_a l_a),  B=(z_a/S)sinh,  C=(S/z_a)sinh", FT, BLACK)
    ctext(d, 330, 356, "出口が剛壁 v2=0 / 開放 p2=0 で入口インピーダンス Z1=p1/(S v1) が定まる", FT, BLACK)
    note(d, "区間ごとの行列を掛け合わせるだけで全体の音響特性を求められる")
    save(im, "v1f6DuctTransfer")


if __name__ == "__main__":
    f_planewave(); f_pipemode(); f_complexintensity()
    f_shapefunc(); f_mesh(); f_panelcoupling()
    f_pipevib(); f_twopeak(); f_ducttransfer()
    print("done v1f6 formula")
