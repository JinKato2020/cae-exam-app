# -*- coding: utf-8 -*-
"""熱流体力学1級 第1章「単相流の物理」問題図 15枚。figlibで白地660x420線画を描く。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dash(d, x1, y1, x2, y2, col=BLACK, wd=2, dl=10, gap=7):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = t
        b = min(t + dl, L)
        d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)
        t += dl + gap


def hatch_poly(d, pts, col=LGRAY, spacing=9, wd=1):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    # simple diagonal hatch clipped by polygon bbox via point-in-poly
    def inside(px, py):
        c = False; n = len(pts); j = n - 1
        for i in range(n):
            xi, yi = pts[i]; xj, yj = pts[j]
            if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
                c = not c
            j = i
        return c
    v = int(x0)
    off = int(x0 - (y1 - y0))
    x = off
    while x < x1 + (y1 - y0):
        # line of slope 1: from (x,y0) to (x+(y1-y0),y1)
        seg = []
        steps = 60
        for k in range(steps + 1):
            t = k / steps
            px = x + (y1 - y0) * t
            py = y0 + (y1 - y0) * t
            if inside(px, py):
                seg.append((px, py))
        if len(seg) >= 2:
            d.line((seg[0][0], seg[0][1], seg[-1][0], seg[-1][1]), fill=col, width=wd)
        x += spacing


# ---------------------------------------------------------------- 1-1 Manometer
def f_manometer():
    im, d = new()
    title(d, "傾斜円管路とU字マノメータ")
    # inclined pipe centerline A(lower-left) -> B(upper-right)
    ax, ay = 150, 235
    bx, by = 505, 120
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    px, py = -uy, ux  # perpendicular (points downward-ish)
    wpipe = 15
    # pipe walls
    for s in (1, -1):
        d.line((ax + px * s * wpipe, ay + py * s * wpipe,
                bx + px * s * wpipe, by + py * s * wpipe), fill=BLACK, width=3)
    # centerline
    dash(d, ax, ay, bx, by, GRAY, 1, 8, 6)
    # flow arrow V along pipe
    arrow(d, ax + ux * 95, ay + uy * 95, ax + ux * 185, ay + uy * 185, BLUE, 4, 15)
    ctext(d, ax + ux * 140, ay + uy * 140 - 22, "V", F, BLUE, "mm")
    ctext(d, ax + ux * 250, ay + uy * 250 - 24, "水 ρ, λ", FS, BLACK)
    # tap points A,B on lower wall (py points downward)
    Ax, Ay = ax + ux * 70 + px * wpipe, ay + uy * 70 + py * wpipe
    Bx, By = ax + ux * 300 + px * wpipe, ay + uy * 300 + py * wpipe
    node(d, Ax, Ay, 5, BLACK, BLACK); ctext(d, Ax - 6, Ay - 16, "A", FS, BLACK)
    node(d, Bx, By, 5, BLACK, BLACK); ctext(d, Bx + 4, By - 14, "B", FS, BLACK)
    # U-tube manometer, larger and lower
    lx, rx = 275, 400
    botY = 390
    topL, topR = Ay + 8, By + 8
    # connecting tubes from taps down to leg tops
    d.line((Ax, Ay, lx, topL), fill=BLACK, width=2)
    d.line((Bx, By, rx, topR), fill=BLACK, width=2)
    # U tube outline (two legs + rounded bottom)
    d.line((lx, topL, lx, botY), fill=BLACK, width=2)
    d.line((rx, topR, rx, botY), fill=BLACK, width=2)
    d.line((lx, botY, rx, botY), fill=BLACK, width=2)
    # fill liquid with level difference h: left meniscus lower(=larger y), right higher
    mlL, mlR = 330, 288
    d.rectangle((lx - 5, mlL, lx + 5, botY), fill=FILL3)
    d.rectangle((rx - 5, mlR, rx + 5, botY), fill=FILL3)
    d.line((lx - 5, botY, rx + 5, botY), fill=FILL3, width=3)
    # meniscus level lines + h dimension between them
    dash(d, lx - 20, mlL, rx + 55, mlL, GRAY, 1, 7, 5)
    dash(d, rx + 5, mlR, rx + 55, mlR, GRAY, 1, 7, 5)
    dim(d, rx + 45, mlR, rx + 45, mlL, "h", 0, GRAY)
    ctext(d, (lx + rx) / 2, botY - 20, "封入液 ρ'", FT, BLACK)
    # dimensions L (along pipe) and H (vertical height difference)
    dim(d, ax + px * 42, ay + py * 42, bx + px * 42, by + py * 42, "L", 0, GRAY)
    dash(d, bx, by, 560, by, LGRAY, 1, 6, 4)
    dash(d, ax, ay, 108, ay, LGRAY, 1, 6, 4)
    dim(d, 118, ay, 118, by, "H", 0, GRAY)
    ctext(d, 70, 70, "内径 d", FS, BLACK)
    save(im, "t1e1Manometer")


# ---------------------------------------------------------------- 1-2 Vorticity
def f_vorticity():
    im, d = new()
    title(d, "流線(等ψ線)と流体粒子の渦度")
    # several streamlines (wavy curves)
    for i, y0 in enumerate(range(120, 360, 40)):
        pts = []
        for xx in range(90, 580, 6):
            yy = y0 + 30 * math.sin((xx - 90) / 70.0)
            pts.append((xx, yy))
        plot(d, 0, 0, pts, BLUE, 2)
        if i == 2:
            ctext(d, 585, y0, "ψ=const", FT, BLUE, "lm")
    # small rotation arrow (vorticity) at a point
    cx, cy = 330, 235
    r = 26
    d.arc((cx - r, cy - r, cx + r, cy + r), 20, 300, fill=RED, width=3)
    # arrowhead on arc (at ~300deg end -> pointing tangential)
    aa = math.radians(300)
    ex, ey = cx + r * math.cos(-aa), cy + r * math.sin(-aa)
    arrow(d, ex - 1, ey - 12, ex + 6, ey + 2, RED, 3, 10)
    ctext(d, cx, cy, "ζ", FS, RED)
    node(d, cx, cy, 3, RED, RED)
    # definition note
    note(d, "u = ∂ψ/∂y ,  v = -∂ψ/∂x   (ζ=渦度)")
    save(im, "t1e1Vorticity")


# ---------------------------------------------------------------- 1-3 SoundSpeed
def f_soundspeed():
    im, d = new()
    title(d, "液体中を伝わる圧力パルス")
    # long tube
    x0, x1, ytop, ybot = 90, 590, 170, 290
    d.line((x0, ytop, x1, ytop), fill=BLACK, width=3)
    d.line((x0, ybot, x1, ybot), fill=BLACK, width=3)
    d.line((x0, ytop, x0, ybot), fill=BLACK, width=3)
    d.line((x1, ytop, x1, ybot), fill=BLACK, width=3)
    ctext(d, 340, 320, "液体  K, ρ", FS, BLACK)
    # small compression at left (piston tap)
    d.rectangle((x0, ytop, x0 + 14, ybot), fill=FILL3)
    arrow(d, x0 - 34, 230, x0 + 10, 230, RED, 3, 12)
    ctext(d, x0 - 40, 205, "微小圧縮", FT, RED, "mm")
    # pressure wave front moving right at speed a
    wf = 330
    dash(d, wf, ytop - 4, wf, ybot + 4, RED, 3, 9, 6)
    arrow(d, wf, 230, wf + 90, 230, RED, 4, 15)
    ctext(d, wf + 95, 230, "a", F, RED, "lm")
    ctext(d, wf, ytop - 16, "波面", FT, RED)
    note(d, "圧力パルスが速度 a で右へ伝わる")
    save(im, "t1e1SoundSpeed")


# ---------------------------------------------------------------- 1-4 FlatPlate
def f_flatplate():
    im, d = new()
    title(d, "平板に沿う強制対流境界層")
    plate_y = 300
    x0, x1 = 120, 580
    hwall(d, x0, x1, plate_y, 1, 12)
    ctext(d, (x0 + x1) / 2, plate_y + 34, "平板", FS, BLACK)
    # leading edge
    node(d, x0, plate_y, 4, BLACK, BLACK)
    ctext(d, x0 - 6, plate_y - 18, "前縁", FT, BLACK)
    # freestream arrows u_inf
    for yy in (150, 185, 220):
        arrow(d, 60, yy, 118, yy, BLUE, 3, 12)
    ctext(d, 55, 130, "u∞", F, BLUE, "mm")
    # velocity boundary layer (grows as sqrt)
    vpts = []
    for xx in range(x0, x1 + 1, 6):
        th = 90 * math.sqrt((xx - x0) / (x1 - x0))
        vpts.append((xx, plate_y - th))
    plot(d, 0, 0, vpts, BLACK, 2)
    ctext(d, x1 - 10, plate_y - 100, "速度境界層", FT, BLACK, "rm")
    # thermal boundary layer (slightly different, dashed)
    tpts = []
    for xx in range(x0, x1 + 1, 6):
        th = 68 * math.sqrt((xx - x0) / (x1 - x0))
        tpts.append((xx, plate_y - th))
    for k in range(0, len(tpts) - 1, 2):
        d.line((tpts[k][0], tpts[k][1], tpts[k + 1][0], tpts[k + 1][1]), fill=ORANGE, width=2)
    ctext(d, x1 - 10, plate_y - 52, "温度境界層", FT, ORANGE, "rm")
    # distance x from leading edge
    xloc = 430
    dash(d, xloc, plate_y, xloc, plate_y + 60, GRAY, 1, 6, 4)
    dim(d, x0, plate_y + 55, xloc, plate_y + 55, "x", 0, GRAY)
    # local heat transfer h_x position
    arrow(d, xloc, plate_y - 4, xloc, plate_y - 40, RED, 3, 11)
    ctext(d, xloc + 8, plate_y - 24, "h_x", FS, RED, "lm")
    save(im, "t1e1FlatPlate")


# ---------------------------------------------------------------- 1-5 RotatingStall
def f_rotatingstall():
    im, d = new()
    title(d, "翼列(羽根車)の1流路が失速・閉塞")
    cx, cy = 330, 235
    ro, ri = 150, 70
    d.ellipse((cx - ro, cy - ro, cx + ro, cy + ro), outline=BLACK, width=3)
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=BLACK, width=3)
    n = 12
    for i in range(n):
        a = 2 * math.pi * i / n
        x1 = cx + ri * math.cos(a); y1 = cy + ri * math.sin(a)
        x2 = cx + ro * math.cos(a); y2 = cy + ro * math.sin(a)
        d.line((x1, y1, x2, y2), fill=BLACK, width=3)
    # hatch one passage (between blade k and k+1) -> stalled cell
    k = 10
    a0 = 2 * math.pi * k / n
    a1 = 2 * math.pi * (k + 1) / n
    poly = []
    for t in [j / 10 for j in range(11)]:
        aa = a0 + (a1 - a0) * t
        poly.append((cx + ro * math.cos(aa), cy + ro * math.sin(aa)))
    for t in [j / 10 for j in range(11)]:
        aa = a1 - (a1 - a0) * t
        poly.append((cx + ri * math.cos(aa), cy + ri * math.sin(aa)))
    hatch_poly(d, poly, RED, 7, 2)
    am = (a0 + a1) / 2
    ctext(d, cx + (ro + 26) * math.cos(am), cy + (ro + 26) * math.sin(am), "失速セル", FT, RED)
    ctext(d, cx, cy, "回転", FT, GRAY)
    save(im, "t1e1RotatingStall")


# ---------------------------------------------------------------- 1-6 Surging
def f_surging():
    im, d = new()
    title(d, "ポンプ揚程曲線と管路系")
    ox, oy = 90, 330
    axes(d, ox, oy, 280, 230, "Q (流量)", "h (揚程)")
    # head curve: rises (positive slope) then falls (negative slope) -> hump
    pts = []
    for i in range(0, 261, 4):
        xx = ox + i
        # a hump: increase then decrease
        yy = oy - (60 + 120 * math.sin(math.pi * i / 260) - 0.0000 * i)
        pts.append((xx, yy))
    plot(d, 0, 0, pts, BLUE, 3)
    # mark positive-slope (right-rising) region and negative-slope region
    ctext(d, ox + 70, oy - 210, "正勾配(右上がり)", FT, RED, "mm")
    ctext(d, ox + 205, oy - 205, "右下がり", FT, GRAY, "mm")
    # piping system schematic (tank + line) at right
    tx, ty = 470, 120
    d.rectangle((tx, ty, tx + 120, ty + 80), outline=BLACK, width=3)
    d.line((tx, ty + 24, tx + 120, ty + 24), fill=BLUE, width=2)  # water surface
    ctext(d, tx + 60, ty + 12, "容量部(タンク)", FT, BLACK)
    # pipe from tank down and to pump
    d.line((tx + 60, ty + 80, tx + 60, 300), fill=BLACK, width=3)
    d.line((tx + 60, 300, 560, 300), fill=BLACK, width=3)
    d.ellipse((tx - 10, 285, tx + 30, 325), outline=BLACK, width=3)
    ctext(d, tx + 10, 305, "P", FS, BLACK)
    ctext(d, tx + 60, 345, "管路系", FT, BLACK)
    save(im, "t1e1Surging")


# ---------------------------------------------------------------- 1-7 WallLaw
def f_walllaw():
    im, d = new()
    title(d, "乱流境界層の壁法則(片対数)")
    ox, oy = 110, 340
    axes(d, ox, oy, 440, 250, "log y+", "U+")
    # viscous sublayer: U+=y+  -> on semilog x, y = 10^X, appears as exponential-ish rising steeply at right of low region
    # draw sublayer segment (low y+) as steep near-straight then log-law shallower straight
    # sublayer line
    subl = []
    for i in range(0, 130):
        xx = ox + i
        yy = oy - (i * 1.15)
        subl.append((xx, yy))
    plot(d, 0, 0, subl, GREEN, 3)
    ctext(d, ox + 70, oy - 175, "U+ = y+", FT, GREEN, "lm")
    ctext(d, ox + 40, oy - 30, "粘性底層", FT, GREEN)
    # buffer transition (dashed short)
    dash(d, ox + 129, oy - 148, ox + 190, oy - 168, GRAY, 2, 8, 5)
    # log-law line (shallower slope)
    logl = []
    for i in range(190, 430):
        xx = ox + i
        yy = oy - (168 + (i - 190) * 0.30)
        logl.append((xx, yy))
    plot(d, 0, 0, logl, BLUE, 3)
    ctext(d, ox + 300, oy - 205, "対数則", FT, BLUE, "lm")
    save(im, "t1e1WallLaw")


# ---------------------------------------------------------------- 1-8 WaterHammer
def f_waterhammer():
    im, d = new()
    title(d, "タンク・管路・弁の瞬時閉止")
    # big tank at left
    d.rectangle((70, 120, 190, 320), outline=BLACK, width=3)
    d.line((70, 150, 190, 150), fill=BLUE, width=2)
    dash(d, 70, 150, 60, 150, BLUE, 1, 6, 4)
    ctext(d, 130, 110, "タンク(水位一定)", FT, BLACK)
    # horizontal pipe
    py0, py1 = 250, 285
    d.line((190, py0, 520, py0), fill=BLACK, width=3)
    d.line((190, py1, 520, py1), fill=BLACK, width=3)
    # flow U1
    arrow(d, 260, (py0 + py1) / 2, 340, (py0 + py1) / 2, BLUE, 4, 14)
    ctext(d, 300, (py0 + py1) / 2 - 20, "U1", FS, BLUE)
    dim(d, 200, py1 + 25, 510, py1 + 25, "L (管長)", 0, GRAY)
    # valve at right end (closed)
    d.line((520, py0 - 8, 520, py1 + 8), fill=RED, width=4)
    d.polygon((512, py0, 528, py0, 520, (py0 + py1) / 2), outline=RED, width=2)
    d.polygon((512, py1, 528, py1, 520, (py0 + py1) / 2), outline=RED, width=2)
    ctext(d, 540, 240, "弁", FS, RED, "lm")
    ctext(d, 540, 262, "(瞬時閉止)", FT, RED, "lm")
    # observation point O just upstream of valve
    node(d, 495, (py0 + py1) / 2, 5, RED, RED)
    ctext(d, 495, py0 - 16, "O", FS, RED)
    save(im, "t1e1WaterHammer")


# ---------------------------------------------------------------- 1-9 MHD
def f_mhd():
    im, d = new()
    title(d, "矩形ダクト内の導電性流体(MHD)")
    # rectangular duct (iso-ish rectangle)
    x0, y0, w, h = 190, 170, 280, 130
    d.rectangle((x0, y0, x0 + w, y0 + h), outline=BLACK, width=3)
    # flow direction v (along duct, to the right)
    arrow(d, x0 + 40, y0 + h / 2, x0 + 150, y0 + h / 2, BLUE, 4, 15)
    ctext(d, x0 + 95, y0 + h / 2 - 20, "v (流れ)", FS, BLUE)
    # magnetic flux density B upward
    for bx in (x0 + 90, x0 + 190):
        arrow(d, bx, y0 + h + 60, bx, y0 - 40, GREEN, 3, 13)
    ctext(d, x0 + 200, y0 - 30, "B (磁束密度)", FS, GREEN, "lm")
    # current density j into page (depth) : circle-with-cross symbol + arrow going "into"
    jx, jy = x0 + w - 60, y0 + h / 2
    r = 16
    d.ellipse((jx - r, jy - r, jx + r, jy + r), outline=ORANGE, width=3)
    d.line((jx - 11, jy - 11, jx + 11, jy + 11), fill=ORANGE, width=3)
    d.line((jx - 11, jy + 11, jx + 11, jy - 11), fill=ORANGE, width=3)
    ctext(d, jx, jy + 30, "j (電流密度,奥へ)", FT, ORANGE)
    note(d, "導電性流体・電磁場の連成")
    save(im, "t1e1MHD")


# ---------------------------------------------------------------- 1-10 Separation
def f_separation():
    im, d = new()
    title(d, "逆圧力勾配下の境界層はく離")
    # curved wall (convex, descending then the flow separates)
    wpts = []
    for xx in range(90, 580, 4):
        yy = 250 + 70 * math.sin((xx - 90) / 320.0 * math.pi)  # bump
        wpts.append((xx, yy))
    plot(d, 0, 0, wpts, BLACK, 3)
    # hatch below wall (short ticks)
    for k in range(0, len(wpts), 12):
        x, y = wpts[k]
        d.line((x, y, x + 10, y + 14), fill=BLACK, width=1)
    # velocity profiles at several sections
    sections = [(160, "順圧"), (300, ""), (400, "勾配0"), (500, "逆流")]
    for sx, lab in sections:
        # base y on wall
        idx = int((sx - 90) / 4)
        idx = max(0, min(idx, len(wpts) - 1))
        wy = wpts[idx][1]
        # profile shape
        prof = []
        for j in range(0, 90, 4):
            yy = wy - j
            if sx <= 300:
                u = 42 * (j / 88.0) ** 0.5          # full
            elif sx == 400:
                u = 42 * (j / 88.0) ** 1.6          # zero gradient at wall
            else:
                u = -14 * math.exp(-j / 20.0) + 42 * (j / 88.0) ** 1.9  # reverse near wall
            prof.append((sx + u, yy))
        plot(d, 0, 0, prof, BLUE, 2)
        d.line((sx, wy, sx, wy - 88), fill=GRAY, width=1)
        if lab:
            ctext(d, sx, wy + 22, lab, FT, RED if lab in ("勾配0", "逆流") else GRAY)
    # separation point marker
    sep = 400
    idx = int((sep - 90) / 4); wy = wpts[idx][1]
    node(d, sep, wy, 5, RED, RED)
    ctext(d, sep + 6, wy - 100, "はく離点", FT, RED, "lm")
    # adverse pressure gradient arrow
    arrow(d, 300, 120, 470, 120, ORANGE, 3, 12)
    ctext(d, 385, 104, "逆圧力勾配", FT, ORANGE)
    save(im, "t1e1Separation")


# ---------------------------------------------------------------- 1-11 NaturalConv
def f_naturalconv():
    im, d = new()
    title(d, "加熱鉛直平板の自然対流")
    # vertical heated plate at left
    px = 200
    wall(d, px, 120, 340, -1, 12)  # hatch to left, plate face to right
    ctext(d, px - 40, 230, "加熱壁", FS, BLACK, "mm")
    ctext(d, px - 40, 255, "T_w", FT, RED, "mm")
    ctext(d, 520, 130, "周囲 T∞", FS, BLACK)
    # boundary layer edge (grows upward)
    edge = []
    for yy in range(340, 119, -4):
        th = 20 + 70 * ((340 - yy) / 220.0)
        edge.append((px + th, yy))
    plot(d, 0, 0, edge, GRAY, 2)
    ctext(d, px + 100, 150, "境界層", FT, GRAY, "lm")
    # rising buoyant flow arrows (upward) inside layer
    for yy in (310, 250, 190):
        arrow(d, px + 35, yy, px + 35, yy - 46, BLUE, 3, 12)
    ctext(d, px + 55, 300, "浮力による上昇流", FT, BLUE, "lm")
    # velocity profile at one section
    sy = 280
    prof = []
    for j in range(0, 90, 3):
        xx = px + j
        u = 46 * (j / 30.0) * math.exp(-j / 40.0)
        prof.append((xx, sy - u))
    plot(d, 0, 0, prof, GREEN, 2)
    ctext(d, px + 95, sy - 10, "速度分布", FT, GREEN, "lm")
    save(im, "t1e1NaturalConv")


# ---------------------------------------------------------------- 1-12 CriticalNozzle
def f_criticalnozzle():
    im, d = new()
    title(d, "収縮ノズルと臨界(スロート)状態")
    # converging nozzle: wide inlet -> narrow throat
    x0, x1 = 130, 500
    ymid = 240
    upper = [(x0, ymid - 100), (350, ymid - 40), (x1, ymid - 38)]
    lower = [(x0, ymid + 100), (350, ymid + 40), (x1, ymid + 38)]
    d.line(upper, fill=BLACK, width=3, joint="curve")
    d.line(lower, fill=BLACK, width=3, joint="curve")
    d.line((x0, ymid - 100, x0, ymid + 100), fill=BLACK, width=3)
    # inlet stagnation state
    ctext(d, x0 - 4, ymid - 130, "入口(よどみ点)", FT, BLACK)
    ctext(d, 175, ymid, "p0, 速度≈0", FS, BLACK)
    # throat / critical state M=1
    thx = 470
    dash(d, thx, ymid - 60, thx, ymid + 60, RED, 2, 8, 5)
    arrow(d, x0 + 40, ymid, thx - 20, ymid, BLUE, 4, 15)
    ctext(d, thx + 6, ymid - 60, "スロート", FT, RED, "lm")
    ctext(d, thx + 6, ymid - 40, "p*, M=1", FS, RED, "lm")
    ctext(d, thx + 6, ymid + 10, "(音速に達する)", FT, RED, "lm")
    save(im, "t1e1CriticalNozzle")


# ---------------------------------------------------------------- 1-13 Nozzle
def f_nozzle():
    im, d = new()
    title(d, "ラバルノズル(先細り→末広がり)")
    ymid = 235
    # profile: wide -> throat -> wide
    xs = list(range(110, 551, 5))
    up = []; lo = []
    thx = 330
    for xx in xs:
        if xx <= thx:
            r = 100 - 70 * (xx - 110) / (thx - 110)
        else:
            r = 30 + 75 * (xx - thx) / (550 - thx)
        up.append((xx, ymid - r)); lo.append((xx, ymid + r))
    d.line(up, fill=BLACK, width=3, joint="curve")
    d.line(lo, fill=BLACK, width=3, joint="curve")
    d.line((110, ymid - 100, 110, ymid + 100), fill=BLACK, width=3)
    d.line((550, ymid - 105, 550, ymid + 105), fill=BLACK, width=3)
    # throat marker
    dash(d, thx, ymid - 30, thx, ymid + 30, GRAY, 2, 7, 5)
    ctext(d, thx, ymid + 55, "スロート", FT, GRAY)
    # flow x direction + A(x) + M positions
    arrow(d, 150, ymid, 520, ymid, BLUE, 3, 14)
    ctext(d, 500, ymid - 18, "x", FS, BLUE)
    ctext(d, 180, ymid - 70, "M<1 (亜音速)", FT, BLACK)
    ctext(d, 430, ymid - 80, "M>1 (超音速)", FT, BLACK)
    ctext(d, thx, ymid - 45, "M=1", FT, RED)
    ctext(d, 250, ymid + 90, "断面積 A(x)", FT, BLACK)
    save(im, "t1e1Nozzle")


# ---------------------------------------------------------------- 1-14 ShockTube
def f_shocktube():
    im, d = new()
    title(d, "衝撃波管内の各波・領域")
    x0, x1 = 80, 590
    ytop, ybot = 180, 280
    # tube walls
    d.line((x0, ytop, x1, ytop), fill=BLACK, width=3)
    d.line((x0, ybot, x1, ybot), fill=BLACK, width=3)
    d.line((x0, ytop, x0, ybot), fill=BLACK, width=3)
    d.line((x1, ytop, x1, ybot), fill=BLACK, width=3)
    # region boundaries: expansion(left) | region4? use physical low/high
    # From left: 膨張波 region | 接触面 | 衝撃波面 | driven gas
    exp_l, exp_r = 170, 230
    contact = 360
    shock = 470
    # expansion fan (several lines)
    for i in range(5):
        xx = exp_l + i * (exp_r - exp_l) / 4
        d.line((xx, ytop, exp_l + 8, ybot), fill=GRAY, width=1)
    ctext(d, 200, ytop - 14, "膨張波", FT, GRAY)
    # contact surface (dashed)
    dash(d, contact, ytop, contact, ybot, GREEN, 2, 8, 5)
    ctext(d, contact, ybot + 16, "接触面", FT, GREEN)
    # shock front
    d.line((shock, ytop, shock, ybot), fill=RED, width=3)
    arrow(d, shock, 230, shock + 55, 230, RED, 4, 14)
    ctext(d, shock, ytop - 14, "衝撃波面", FT, RED)
    # region labels along the tube
    ctext(d, 120, 230, "高圧側", FT, BLACK)
    ctext(d, 300, 230, "膨張後", FT, BLACK)
    ctext(d, 415, 230, "駆動後", FT, BLACK)
    ctext(d, 540, 230, "低圧側", FT, BLACK)
    # flow direction reference
    arrow(d, 250, 320, 330, 320, BLUE, 3, 12)
    ctext(d, 355, 320, "流れ方向 x", FT, BLUE, "lm")
    save(im, "t1e1ShockTube")


# ---------------------------------------------------------------- 1-15 ExpansionWave
def f_expansionwave():
    im, d = new()
    title(d, "膨張波の x-t 線図")
    ox, oy = 110, 350
    axes(d, ox, oy, 440, 280, "x", "t")
    # right end at x = xR
    xR = ox + 400
    dash(d, xR, oy, xR, oy - 280, LGRAY, 1, 6, 5)
    ctext(d, xR, oy + 16, "右端(開放)", FT, GRAY)
    # expansion fan from right end (origin of fan at (xR, oy))
    fan_dirs = [(-0.3, -1), (-0.6, -1), (-0.9, -1), (-1.25, -1), (-1.7, -1)]
    for i, (dxr, dyr) in enumerate(fan_dirs):
        ex = xR + dxr * 190
        ey = oy - 190
        d.line((xR, oy, ex, ey), fill=GRAY, width=1 if 0 < i < 4 else 2)
    ctext(d, xR - 120, oy - 120, "膨張波(扇状)", FT, GRAY)
    # region (4) high pressure (right, before wave) and (3) outflow (left, after)
    ctext(d, xR - 40, oy - 60, "(4)", F, BLACK)
    ctext(d, xR - 40, oy - 75, "高圧側", FT, BLACK, "mm")
    ctext(d, ox + 70, oy - 170, "(3)", F, BLACK)
    ctext(d, ox + 70, oy - 190, "流出側", FT, BLACK, "mm")
    # point a inside the fan
    ax_, ay_ = xR - 120, oy - 150
    node(d, ax_, ay_, 5, RED, RED)
    ctext(d, ax_ - 14, ay_ - 2, "a", F, RED, "rm")
    save(im, "t1e1ExpansionWave")


if __name__ == "__main__":
    f_manometer()
    f_vorticity()
    f_soundspeed()
    f_flatplate()
    f_rotatingstall()
    f_surging()
    f_walllaw()
    f_waterhammer()
    f_mhd()
    f_separation()
    f_naturalconv()
    f_criticalnozzle()
    f_nozzle()
    f_shocktube()
    f_expansionwave()
    print("done")
