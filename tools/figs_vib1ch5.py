# -*- coding: utf-8 -*-
"""振動1級 第5章「構造複合系の解析」問題図 21枚。figlibで白地660x420線画。
方針: 正確さ最優先・機構のみ・装飾禁止。数式ラベルはASCII(w,wn,Ip,th=theta,e,T,M,K,G)で豆腐回避。
required図は答え(結論)を描かず機構だけ示す。"""
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


def disk(d, cx, cy, rx, ry, fill=FILL1):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=BLACK, width=3, fill=fill)


def spin_arrow(d, cx, cy, r, ccw=True, col=RED):
    """回転(スピン)を示す小円弧矢印。"""
    if ccw:
        d.arc((cx - r, cy - r, cx + r, cy + r), 20, 300, fill=col, width=3)
        ax, ay = cx + r * math.cos(math.radians(20)), cy + r * math.sin(math.radians(20))
        arrow(d, ax, ay + 10, ax, ay - 2, col, 2, 8)
    else:
        d.arc((cx - r, cy - r, cx + r, cy + r), 240, 520, fill=col, width=3)
        ax, ay = cx + r * math.cos(math.radians(240)), cy + r * math.sin(math.radians(240))
        arrow(d, ax, ay - 10, ax, ay + 2, col, 2, 8)


def bracket(d, x, y0, y1, left=True):
    t = 12 if left else -12
    d.line((x, y0, x, y1), fill=BLACK, width=2)
    d.line((x, y0, x + t, y0), fill=BLACK, width=2)
    d.line((x, y1, x + t, y1), fill=BLACK, width=2)


# ================================================ 5-1 Guyan縮小 (helpful)
def f_guyan():
    im, d = new(); title(d, "Guyanの静縮小:マスター節点(残す)とスレーブ節点(消去)")
    y = 210; x0, x1 = 90, 470
    # rotor shaft as beam
    d.line((x0, y, x1, y), fill=BLACK, width=5)
    # disks
    for dx in (170, 300):
        disk(d, dx, y, 16, 34, FILL2)
    nodes = list(range(x0, x1 + 1, 38))
    masters = {nodes[1], nodes[4], nodes[7], nodes[9]}
    for nx in nodes:
        if nx in masters:
            node(d, nx, y, 8, RED)
        else:
            node(d, nx, y, 5, "white")
    # forces on masters (bearing/control)
    force(d, nodes[1], y + 40, 0, -30, "軸受力", RED, FT)
    force(d, nodes[7], y + 40, 0, -30, "制御力", RED, FT)
    ctext(d, 280, 100, "●=マスター節点(物理座標に残す:軸受力・制御力の作用点)", FT, RED)
    ctext(d, 280, 122, "○=スレーブ(内部)節点 → 静的弾性変形の和で近似し消去", FT, GRAY)
    arrow(d, 500, y, 555, y, BLACK, 3, 13)
    box(d, 500, y + 20, 620, y + 70, FILL1)
    ctext(d, 560, y + 45, "縮小系\n(自由度 小)", FT)
    note(d, "内部変位を各マスター節点の静的変位の和で近似=Guyanの静縮小")
    save(im, "v1e5GuyanReduction")


# ================================================ 5-2 振れ回りと自動調心 (required)
def f_whirl_self():
    im, d = new(); title(d, "回転軸中央の回転体:図心M・重心G(Mからeずれ)の振れ回り")
    # left: vertical shaft side view
    sx = 150
    hwall(d, sx - 45, sx + 45, 95, side=-1, n=5)
    hwall(d, sx - 45, sx + 45, 345, side=1, n=5)
    d.line((sx, 95, sx, 345), fill=BLACK, width=3)
    disk(d, sx, 220, 42, 16, FILL2)
    spin_arrow(d, sx, 155, 26, True)
    ctext(d, sx + 42, 152, "w", FS, RED, "lm")
    ctext(d, sx, 372, "垂直回転軸+回転体", FT, GRAY)
    # right: O-xy whirl plane (top view)
    cx, cy = 460, 225
    axes(d, cx, cy, 150, 130, "x", "y")
    R = 78
    dsh(d, cx, cy, cx, cy, LGRAY)  # noop
    # whirl orbit of M
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=GRAY, width=1)
    dsh(d, cx - R, cy, cx + R, cy, LGRAY)
    ang = math.radians(38)
    Mx, My = cx + R * math.cos(ang), cy - R * math.sin(ang)
    e = 34
    Gx, Gy = Mx + e * math.cos(ang), My - e * math.sin(ang)
    d.line((cx, cy, Mx, My), fill=BLUE, width=2)
    d.line((Mx, My, Gx, Gy), fill=BLACK, width=2)
    node(d, cx, cy, 5, BLACK); ctext(d, cx - 12, cy + 12, "O", FT, BLACK)
    node(d, Mx, My, 6, FILL1); ctext(d, Mx - 6, My - 16, "M(図心)", FT, BLUE, "rm")
    node(d, Gx, Gy, 6, RED, RED); ctext(d, Gx + 10, Gy - 6, "G(重心)", FT, RED, "lm")
    ctext(d, (Mx + Gx) / 2 + 6, (My + Gy) / 2 - 12, "e", FT, BLACK)
    ctext(d, (cx + Mx) / 2 - 14, (cy + My) / 2, "X", FT, BLUE, "rm")
    ctext(d, cx, cy + 120, "破線円=図心Mの振れ回り軌道", FT, GRAY)
    note(d, "静止時の図心を原点O・回転で図心Mが半径Xで振れ回る(GはMからe)")
    save(im, "v1e5WhirlSelfCenter")


# ================================================ 5-3 たわみ振動/傾き振動 (helpful)
def f_deflect_tilt():
    im, d = new(); title(d, "たわみ振動(傾かず並進) と 傾き振動(図心を保って傾く)")
    def shaft(ox, mode, lab):
        L = 200; y = 235
        x0, x1 = ox, ox + L
        cxm = (x0 + x1) / 2
        pin_support(d, x0, y + 4, 18); roller_support(d, x1, y + 4, 18)
        dsh(d, x0, y, x1, y, LGRAY)
        if mode == "defl":
            # translated disk, shaft bent as bow, no tilt of disk
            pts = [(x0 + L * t, y - 40 * math.sin(math.pi * t)) for t in [i / 40 for i in range(41)]]
            plot(d, 0, 0, pts, BLACK, 4)
            ycm = y - 40
            disk(d, cxm, ycm, 10, 28, FILL2)  # upright (no tilt)
            arrow(d, cxm + 40, ycm, cxm + 40, y, BLUE, 2, 9)
            ctext(d, cxm + 46, (ycm + y) / 2, "並進 x", FT, BLUE, "lm")
        else:
            # tilt: center fixed, disk tilted
            d.line((x0, y, x1, y), fill=BLACK, width=4)
            th = 0.42
            p1 = rot(cxm, y - 32, cxm, y, th); p2 = rot(cxm, y + 32, cxm, y, th)
            d.line((p1[0], p1[1], p2[0], p2[1]), fill=BLACK, width=6)
            angle_arc(d, cxm, y, 40, 60, 90, "th", GRAY)
            node(d, cxm, y, 4, RED, RED)
        ctext(d, cxm, y + 78, lab, FT)
    shaft(70, "defl", "たわみ振動: 傾かず x,y へ並進")
    d.line((330, 90, 330, 340), fill=LGRAY, width=1)
    shaft(370, "tilt", "傾き振動: 図心を保って傾く")
    note(d, "両端単純支持・中央に回転体。二つの変形モードを対比")
    save(im, "v1e5DeflectTiltMode")


# ================================================ 5-4 前後ふれまわり (helpful)
def f_fwd_bwd_whirl():
    im, d = new(); title(d, "前向き(前回り)ふれまわり と 後ろ向き(後回り)ふれまわり")
    def orbit(cx, whirl_ccw, spin_ccw, lab, sub):
        R = 82
        axes(d, cx, 235, 100, 95, "x", "y")
        d.ellipse((cx - R, 235 - R, cx + R, 235 + R), outline=BLUE, width=2)
        # whirl direction arrow on orbit
        a = math.radians(45)
        px, py = cx + R * math.cos(a), 235 - R * math.sin(a)
        tang = a + (math.pi / 2 if whirl_ccw else -math.pi / 2)
        arrow(d, px, py, px + 26 * math.cos(tang), py - 26 * math.sin(tang), BLUE, 3, 11)
        node(d, px, py, 6, FILL1)
        spin_arrow(d, cx, 235, 26, spin_ccw)
        ctext(d, cx, 350, lab, FS)
        ctext(d, cx, 372, sub, FT, GRAY)
    orbit(180, True, True, "前向きふれまわり", "振れ回り向き=回転向き(同方向)")
    d.line((330, 95, 330, 385), fill=LGRAY, width=1)
    orbit(490, False, True, "後ろ向きふれまわり", "振れ回り向き=回転と逆")
    save(im, "v1e5ForwardBackwardWhirl")


# ================================================ 5-5 ジャイロ連成 (helpful)
def f_gyro_coupling():
    im, d = new(); title(d, "軸方向角運動量 Ip*w の方向変化 → ジャイロモーメントが th を連成")
    cx, cy = 260, 245
    # tilted disk edge-on
    th = 0.42
    p1 = rot(cx, cy - 40, cx, cy, th); p2 = rot(cx, cy + 40, cx, cy, th)
    d.line((p1[0], p1[1], p2[0], p2[1]), fill=BLACK, width=6)
    disk(d, cx, cy, 12, 40, FILL2)
    node(d, cx, cy, 4, RED, RED)
    # angular momentum vector along axis (perpendicular to disk)
    axdir = th + math.pi / 2
    hx, hy = cx + 95 * math.cos(axdir), cy - 95 * math.sin(axdir)
    arrow(d, cx, cy, hx, hy, BLUE, 4, 14)
    ctext(d, hx + 6, hy - 10, "Ip*w (角運動量)", FT, BLUE, "lm")
    # change of direction dH
    axdir2 = axdir + 0.35
    hx2, hy2 = cx + 95 * math.cos(axdir2), cy - 95 * math.sin(axdir2)
    dsh(d, cx, cy, hx2, hy2, LGRAY)
    d.arc((cx - 95, cy - 95, cx + 95, cy + 95), -math.degrees(axdir2), -math.degrees(axdir), fill=RED, width=2)
    ctext(d, (hx + hx2) / 2 + 14, (hy + hy2) / 2 - 14, "dH", FT, RED)
    # coupling note with theta axes
    axes(d, 520, 300, 90, 90, "th_x", "th_y")
    arrow(d, 470, 150, 520, 190, RED, 3, 12)
    ctext(d, 500, 130, "ジャイロモーメント\n= th_x と th_y を連成", FT, RED)
    note(d, "速度 d(th) に比例するが減衰でなく、固有振動数を回転数に依存させる")
    save(im, "v1e5GyroCoupling")


# ================================================ 5-6 回転数依存(キャンベル) (helpful)
def f_gyro_speed():
    im, d = new(); title(d, "回転数依存:前向きは上昇・後ろ向きは下降(キャンベル線図)")
    ox, oy = 100, 350; xr, ym = 470, 265
    axes(d, ox, oy, xr + 30, ym + 25, "回転速度 w", "固有振動数")
    w0 = oy - ym * 0.45
    X = lambda t: ox + t * xr
    fwd = [(X(t), w0 - t * ym * 0.42) for t in [i / 40 for i in range(41)]]
    bwd = [(X(t), w0 + t * ym * 0.30) for t in [i / 40 for i in range(41)]]
    plot(d, 0, 0, fwd, BLUE, 3)
    plot(d, 0, 0, bwd, GREEN, 3)
    # synchronous line w = natural
    syn = [(X(t), oy - t * ym * 0.9) for t in [i / 40 for i in range(41)]]
    dsh(d, syn[0][0], syn[0][1], syn[-1][0], syn[-1][1], GRAY)
    ctext(d, X(0.9), fwd[-1][1] - 12, "前向きふれまわり", FT, BLUE, "rm")
    ctext(d, X(0.9), bwd[-1][1] + 14, "後ろ向きふれまわり", FT, GREEN, "rm")
    ctext(d, X(0.62), oy - ym * 0.62, "同期線 w=固有", FT, GRAY, "lm")
    ctext(d, ox + 8, w0 - 4, "静止時", FT, GRAY, "lm")
    save(im, "v1e5GyroSpeedDependence")


# ================================================ 5-7 傾き回転体(required)
def f_gyro_tilt_rotor():
    im, d = new(); title(d, "垂直軸中央の回転体を傾ける:O-xy平面と傾き角 th_x, th_y")
    cx, cy = 330, 235
    # vertical shaft reference (dashed) + tilted shaft (solid)
    dsh(d, cx, 100, cx, 370, LGRAY)
    th = 0.28
    top = rot(cx, 110, cx, cy, th); bot = rot(cx, 360, cx, cy, th)
    d.line((top[0], top[1], bot[0], bot[1]), fill=BLACK, width=3)
    # tilted disk edge (perpendicular to tilted shaft)
    da = th + math.pi / 2
    d1 = (cx + 60 * math.cos(da), cy - 60 * math.sin(da))
    d2 = (cx - 60 * math.cos(da), cy + 60 * math.sin(da))
    d.line((d1[0], d1[1], d2[0], d2[1]), fill=BLACK, width=6)
    disk(d, cx, cy, 14, 58, FILL2)
    node(d, cx, cy, 4, RED, RED)
    # O-xy plane (perpendicular to nominal axis) as flat ellipse
    d.ellipse((cx - 150, cy - 26, cx + 150, cy + 26), outline=GRAY, width=1)
    arrow(d, cx, cy, cx + 150, cy - 8, GRAY, 2, 10); ctext(d, cx + 160, cy - 8, "x", FS, GRAY, "lm")
    arrow(d, cx, cy, cx - 60, cy - 40, GRAY, 2, 10); ctext(d, cx - 66, cy - 44, "y", FS, GRAY, "rm")
    ctext(d, cx - 15, cy + 16, "O", FT, BLACK, "rm")
    # tilt angle
    angle_arc(d, cx, cy, 70, 62, 90, "th", RED)
    ctext(d, cx + 70, 120, "軸を x,y まわりに\n傾ける角 th_x, th_y", FT, BLACK, "lm")
    spin_arrow(d, cx, 130, 22, True); ctext(d, cx + 24, 128, "w", FT, RED, "lm")
    note(d, "つり合い静止位置を通り軸に垂直な O-xy 平面と傾き角を示す")
    save(im, "v1e5GyroTiltRotor")


# ================================================ 5-8 FEMジャイロ行列 (helpful)
def f_gyro_matrix():
    im, d = new(); title(d, "回転軸のFEM:[M]{u..}+[G]{u.}+[K]{u}=不つり合い加振")
    y = 165; x0, x1 = 90, 470
    d.line((x0, y, x1, y), fill=BLACK, width=5)
    for dx in (200, 330):
        disk(d, dx, y, 12, 26, FILL2)
    for nx in range(x0, x1 + 1, 47):
        node(d, nx, y, 5, "white")
    ctext(d, 280, 205, "ビーム要素+節点でFEM分割", FT, GRAY)
    matrix_grid(d, 95, 250, [["m", "0"], ["0", "m"]], cell=48, fnt=FT)
    ctext(d, 143, 360, "[M] 対称", FT, GRAY)
    matrix_grid(d, 285, 250, [["0", "g"], ["-g", "0"]], cell=48, fnt=FT)
    ctext(d, 333, 360, "[G] 反対称", FT, RED)
    matrix_grid(d, 475, 250, [["k", "0"], ["0", "k"]], cell=48, fnt=FT)
    ctext(d, 523, 360, "[K] 対称", FT, GRAY)
    ctext(d, 545, 165, "不つり合いで\nふれまわり", FT, BLUE)
    save(im, "v1e5GyroMatrixFEM")


# ================================================ 5-9 回転座標系 (helpful)
def f_rotating_frame():
    im, d = new(); title(d, "空間固定 O-xy と 角速度 w で回る回転座標 O-XY (th=wt)")
    cx, cy = 320, 235
    # fixed axes
    arrow(d, cx, cy, cx + 190, cy, GRAY, 2, 11); ctext(d, cx + 198, cy, "x", FS, GRAY, "lm")
    arrow(d, cx, cy, cx, cy - 170, GRAY, 2, 11); ctext(d, cx - 10, cy - 178, "y", FS, GRAY, "rm")
    th = math.radians(35)
    # rotating axes
    Xx, Xy = cx + 190 * math.cos(th), cy - 190 * math.sin(th)
    Yx, Yy = cx + 170 * math.cos(th + math.pi / 2), cy - 170 * math.sin(th + math.pi / 2)
    arrow(d, cx, cy, Xx, Xy, BLUE, 3, 12); ctext(d, Xx + 8, Xy, "X", FS, BLUE, "lm")
    arrow(d, cx, cy, Yx, Yy, BLUE, 3, 12); ctext(d, Yx - 6, Yy - 10, "Y", FS, BLUE, "rm")
    angle_arc(d, cx, cy, 60, 0, math.degrees(th), "th=wt", BLACK)
    spin_arrow(d, cx + 120, cy - 120, 22, True); ctext(d, cx + 120, cy - 150, "w", FT, RED)
    # mass point on X axis
    px, py = cx + 130 * math.cos(th), cy - 130 * math.sin(th)
    node(d, px, py, 7, FILL1); ctext(d, px + 6, py - 14, "質点 P", FT, RED, "lm")
    note(d, "回転座標系では見かけの力=コリオリ力(速度比例)・遠心力(変位比例)")
    save(im, "v1e5RotatingFrame")


# ================================================ 5-10 内部/外部減衰の場所 (helpful)
def f_internal_damping():
    im, d = new(); title(d, "内部減衰(回転する要素間) と 外部減衰(回転-静止要素間)")
    # stationary surroundings
    hwall(d, 90, 570, 350, side=1, n=16)
    ctext(d, 330, 372, "静止部(周囲空気・軸受ハウジング)", FT, GRAY)
    y = 210; sx0, sx1 = 130, 530
    d.line((sx0, y, sx1, y), fill=BLACK, width=5)
    disk(d, 300, y, 18, 46, FILL2)
    # internal damping: inside shaft / between rotating parts (dashpot on shaft)
    dx = 200
    d.line((dx, y - 8, dx, y - 34), fill=BLACK, width=2)
    d.rectangle((dx - 12, y - 58, dx + 12, y - 34), outline=BLUE, width=3)
    d.line((dx, y - 46, dx - 9, y - 46), fill=BLUE, width=4)
    ctext(d, dx, y - 74, "内部減衰\n(軸材料・回転物体間)", FT, BLUE)
    # external damping: rotor to stationary (dashpot to ground)
    ex = 300
    d.line((ex + 40, y, ex + 40, y + 60), fill=BLACK, width=2)
    d.rectangle((ex + 28, y + 60, ex + 52, y + 86), outline=RED, width=3)
    d.line((ex + 40, y + 74, ex + 52, y + 74), fill=RED, width=4)
    d.line((ex + 40, y + 86, ex + 40, y + 104), fill=BLACK, width=2)
    ctext(d, ex + 120, y + 76, "外部減衰\n(回転体-静止物体間)", FT, RED, "lm")
    spin_arrow(d, 300, y, 30, True)
    note(d, "内部減衰は高速で自由振動を不安定化しうる・定常強制振動の振幅には無影響")
    save(im, "v1e5InternalDamping")


# ================================================ 5-11 内部減衰の起源(振れ回り-回転の差) (helpful)
def f_int_ext_damping():
    im, d = new(); title(d, "内部減衰=振れ回り角速度と回転角速度の差に起因")
    # whirl orbit + spin
    cx, cy = 220, 235
    axes(d, cx, cy, 110, 100, "x", "y")
    R = 80
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLUE, width=2)
    a = math.radians(50)
    px, py = cx + R * math.cos(a), cy - R * math.sin(a)
    node(d, px, py, 7, FILL1)
    tang = a + math.pi / 2
    arrow(d, px, py, px + 24 * math.cos(tang), py - 24 * math.sin(tang), BLUE, 3, 11)
    ctext(d, px + 20, py - 20, "振れ回り wp", FT, BLUE, "lm")
    spin_arrow(d, cx, cy, 30, True)
    ctext(d, cx, cy + 6, "回転 w", FT, RED)
    ctext(d, cx, cy + 118, "差 (w - wp) が\n材料ひずみ変化を生む", FT, BLACK)
    # right: internal vs external location list
    x = 400
    box(d, x, 130, x + 210, 210, (225, 235, 245))
    ctext(d, x + 105, 152, "内部減衰", FS, BLUE)
    ctext(d, x + 105, 180, "同回転要素間\n(軸材料・回転物体)", FT, GRAY)
    box(d, x, 235, x + 210, 315, (230, 240, 230))
    ctext(d, x + 105, 257, "外部減衰", FS, RED)
    ctext(d, x + 105, 285, "回転-静止要素間\n(周囲空気など)", FT, GRAY)
    note(d, "内部減衰は定常強制振動では相対運動が生じず振幅に影響しない")
    save(im, "v1e5IntExtDamping")


# ================================================ 5-12 伝達マトリクス法 (helpful)
def f_transfer_matrix():
    im, d = new(); title(d, "回転軸をビーム要素で分割:各断面を伝達行列でつなぐ(伝達マトリクス法)")
    y = 200; x0 = 80
    stations = [x0 + i * 90 for i in range(6)]
    d.line((x0, y, stations[-1], y), fill=BLACK, width=5)
    for i, sx in enumerate(stations):
        node(d, sx, y, 6, "white")
        ctext(d, sx, y + 20, "i=%d" % i, FT, GRAY)
    for i in range(len(stations) - 1):
        mx = (stations[i] + stations[i + 1]) / 2
        box(d, mx - 22, y - 66, mx + 22, y - 36, FILL1)
        ctext(d, mx, y - 51, "[T]", FT)
        arrow(d, stations[i], y - 51, mx - 24, y - 51, GRAY, 2, 9)
        arrow(d, mx + 24, y - 51, stations[i + 1], y - 51, GRAY, 2, 9)
    disk(d, stations[2], y, 12, 30, FILL2)
    ctext(d, 330, 300, "状態ベクトル {変位, 傾き, モーメント, せん断力} を", FT, GRAY)
    ctext(d, 330, 324, "各要素の伝達行列 [T] で端から端へ順に伝える", FT, GRAY)
    note(d, "当初=伝達マトリクス法 → 計算機の向上でFEMへ移行")
    save(im, "v1e5TransferMatrixBeam")


# ================================================ 5-13 ひずみエネルギー重み (helpful)
def f_strain_energy():
    im, d = new(); title(d, "連結部材A・B:あるモードのひずみエネルギー分布 A75% / B25%")
    y = 200
    wall(d, 90, y - 60, y + 60, side=1, n=6)
    xa0, xab, xb1 = 90, 380, 560
    # member A (thick) and B
    bar(d, xa0, y, xab, y, thick=30, fill=(225, 235, 250))
    bar(d, xab, y, xb1, y, thick=30, fill=(230, 245, 230))
    node(d, xab, y, 7, FILL1)
    ctext(d, (xa0 + xab) / 2, y, "部材A", FS, BLUE)
    ctext(d, (xab + xb1) / 2, y, "部材B", FS, GREEN)
    ctext(d, (xa0 + xab) / 2, y - 30, "zeta_A=2%", FT, BLUE)
    ctext(d, (xab + xb1) / 2, y - 30, "zeta_B=6%", FT, GREEN)
    # strain energy bar
    bx0, bx1, by = 120, 540, 320
    total = bx1 - bx0
    d.rectangle((bx0, by, bx0 + total * 0.75, by + 34), outline=BLACK, width=2, fill=(200, 220, 245))
    d.rectangle((bx0 + total * 0.75, by, bx1, by + 34), outline=BLACK, width=2, fill=(210, 235, 210))
    ctext(d, bx0 + total * 0.375, by + 17, "A: 75%", FT, BLUE)
    ctext(d, bx0 + total * 0.875, by + 17, "B: 25%", FT, GREEN)
    ctext(d, 330, 372, "ひずみエネルギー比で重み付け: zeta=zeta_A*fA + zeta_B*fB", FT, GRAY)
    save(im, "v1e5StrainEnergyWeight")


# ================================================ 5-14 焼き嵌めステータ (helpful)
def f_shrink_fit():
    im, d = new(); title(d, "モータのステータ断面:鉄心・コイル・ケース(焼き嵌め結合=有限剛性)")
    cx, cy = 330, 230
    # case (outer ring)
    d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), outline=BLACK, width=4)
    d.ellipse((cx - 128, cy - 128, cx + 128, cy + 128), outline=BLACK, width=2)
    ctext(d, cx, cy - 168, "ケース", FT, GRAY)
    # core (laminated) ring
    d.ellipse((cx - 118, cy - 118, cx + 118, cy + 118), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), outline=BLACK, width=3, fill="white")
    ctext(d, cx, cy, "鉄心\n(積層鋼板)", FT)
    # slots/coils (teeth)
    for k in range(12):
        a = math.radians(k * 30)
        x1, y1 = cx + 60 * math.cos(a), cy + 60 * math.sin(a)
        x2, y2 = cx + 118 * math.cos(a), cy + 118 * math.sin(a)
        d.line((x1, y1, x2, y2), fill=GRAY, width=2)
    ctext(d, cx + 90, cy + 96, "コイル", FT, ORANGE, "lm")
    # shrink-fit contact = finite stiffness springs (radial) between core and case
    for k in range(4):
        a = math.radians(45 + k * 90)
        x1, y1 = cx + 118 * math.cos(a), cy + 118 * math.sin(a)
        x2, y2 = cx + 128 * math.cos(a), cy + 128 * math.sin(a)
        d.line((x1, y1, x2, y2), fill=RED, width=4)
    ctext(d, cx + 150, cy + 130, "焼き嵌め/圧入=有限の結合剛性", FT, RED, "mm", )
    ctext(d, 330, 392, "コイルは質量のみ考慮・鉄心-ケース結合は有限剛性でモデル化", FT, GRAY)
    save(im, "v1e5ShrinkFitStator")


# ================================================ 5-15 制振材料 (helpful)
def f_damping_material():
    im, d = new(); title(d, "製品表面の一部に制振材料を付加(そのモードのひずみエネルギー40%)")
    wall(d, 90, 175, 285, side=1, n=6)
    y = 230; x0, x1 = 90, 560
    bar(d, x0, y, x1, y, thick=26, fill=FILL1)
    # damping material patch on part of surface
    px0, px1 = 360, 540
    d.rectangle((px0, y - 30, px1, y - 13), outline=RED, width=2, fill=(250, 225, 225))
    ctext(d, (px0 + px1) / 2, y - 45, "制振材料 (eta=0.10)", FT, RED)
    ctext(d, (x0 + px0) / 2, y - 45, "基材(損失係数~0)", FT, GRAY)
    # strain energy proportion bar
    bx0, bx1, by = 120, 540, 330
    total = bx1 - bx0
    d.rectangle((bx0, by, bx1 - total * 0.4, by + 30), outline=BLACK, width=2, fill=FILL2)
    d.rectangle((bx1 - total * 0.4, by, bx1, by + 30), outline=BLACK, width=2, fill=(250, 220, 220))
    ctext(d, bx1 - total * 0.2, by + 15, "付加部 40%", FT, RED)
    ctext(d, bx0 + total * 0.3, by + 15, "他部 60%", FT, GRAY)
    ctext(d, 330, 385, "モード損失係数=eta*(ひずみエネルギー比) → 減衰比 zeta=eta_mode/2", FT, GRAY)
    save(im, "v1e5DampingMaterial")


# ================================================ 5-16 ケーブル張力(幾何剛性) (helpful)
def f_cable_tension():
    im, d = new(); title(d, "両端固定ケーブル:張力Tが復元力(幾何剛性)・横風で1次モード振動")
    y = 235; x0, x1 = 130, 530
    wall(d, x0, y - 60, y + 60, side=1, n=5)
    wall(d, x1, y - 60, y + 60, side=-1, n=5)
    dsh(d, x0, y, x1, y, LGRAY)
    # 1st mode half sine
    pts = [(x0 + (x1 - x0) * t, y - 55 * math.sin(math.pi * t)) for t in [i / 60 for i in range(61)]]
    plot(d, 0, 0, pts, BLUE, 4)
    node(d, x0, y, 5, BLACK); node(d, x1, y, 5, BLACK)
    # tension arrows at ends
    force(d, x0, y, -34, 0, "T", RED)
    force(d, x1, y, 34, 0, "T", RED)
    # wind arrows
    for yy in (150, 175):
        arrow(d, 250, yy, 300, yy, GREEN, 2, 9)
    ctext(d, 250, 135, "横風", FT, GREEN)
    dim(d, x0, y + 90, x1, y + 90, "L", col=GRAY)
    ctext(d, 330, 385, "f1=(1/2L)sqrt(T/rho): 張力Tが大きいほど固有振動数が高い", FT, GRAY)
    save(im, "v1e5CableTension")


# ================================================ 5-17 吊り橋魚骨モデル (required)
def f_suspension():
    im, d = new(); title(d, "吊り橋の魚骨モデル:2タワー・メインケーブル・ハンガー・主梁/横梁")
    baseY = 330
    tL, tR = 150, 510
    topY = 120
    # towers
    for tx in (tL, tR):
        d.line((tx, baseY, tx, topY), fill=BLACK, width=5)
        d.line((tx - 16, baseY, tx + 16, baseY), fill=BLACK, width=4)
    hwall(d, 100, 560, baseY + 4, side=1, n=16)
    # main cable (parabola sag between towers, plus side spans to anchors)
    def cable(x):
        t = (x - tL) / (tR - tL)
        return topY + 150 * 4 * t * (1 - t)  # sag
    cpts = [(x, cable(x)) for x in range(tL, tR + 1, 6)]
    plot(d, 0, 0, cpts, BLUE, 3)
    # side spans
    d.line((tL, topY, 90, baseY - 10), fill=BLUE, width=3)
    d.line((tR, topY, 570, baseY - 10), fill=BLUE, width=3)
    # deck (main girder)
    deckY = 275
    d.line((95, deckY, 565, deckY), fill=BLACK, width=5)
    ctext(d, 330, deckY + 16, "主梁(橋桁・はり要素)", FT, GRAY)
    # hangers vertical
    for x in range(tL + 20, tR - 10, 34):
        cy = cable(x)
        if cy < deckY - 4:
            d.line((x, cy, x, deckY), fill=GRAY, width=2)
    # cross beams (ribs) = fishbone
    for x in range(120, 546, 40):
        d.line((x, deckY - 8, x, deckY + 8), fill=GRAY, width=2)
    ctext(d, 330, 100, "メインケーブル(大変形)", FT, BLUE)
    ctext(d, tL, topY - 16, "タワー", FT, GRAY)
    ctext(d, 250, 200, "ハンガーケーブル", FT, GRAY)
    note(d, "ハンガー・メインケーブル=トラス要素、橋桁・主塔=はり要素")
    save(im, "v1e5SuspensionFishbone")


# ================================================ 5-18 はりのせん断変形 (helpful)
def f_beam_shear():
    im, d = new(); title(d, "ベルヌーイ・オイラーはり と チモシェンコはり:断面の向きの違い")
    def seg(ox, mode, lab, sub):
        yc = 235; L = 190
        x0, x1 = ox, ox + L
        # neutral axis bent (bow)
        pts = [(x0 + L * t, yc - 34 * math.sin(math.pi * t / 2)) for t in [i / 40 for i in range(41)]]
        plot(d, 0, 0, pts, BLACK, 4)
        # cross-section at mid
        xm = x0 + L * 0.62
        ym = yc - 34 * math.sin(math.pi * 0.62 / 2)
        # tangent slope of neutral axis
        dth = math.atan2(-34 * (math.pi / 2) * math.cos(math.pi * 0.62 / 2) / L, 1)
        if mode == "be":
            # section perpendicular to neutral axis
            secang = dth + math.pi / 2
            col = BLUE
        else:
            # timoshenko: extra shear angle -> section NOT perpendicular
            secang = dth + math.pi / 2 - 0.32
            col = RED
        s1 = (xm + 40 * math.cos(secang), ym - 40 * math.sin(secang))
        s2 = (xm - 40 * math.cos(secang), ym + 40 * math.sin(secang))
        d.line((s1[0], s1[1], s2[0], s2[1]), fill=col, width=5)
        # reference normal (perpendicular) dashed
        nang = dth + math.pi / 2
        n1 = (xm + 40 * math.cos(nang), ym - 40 * math.sin(nang))
        dsh(d, xm, ym, n1[0], n1[1], LGRAY)
        node(d, xm, ym, 4, RED, RED)
        ctext(d, (x0 + x1) / 2, 335, lab, FS, col)
        ctext(d, (x0 + x1) / 2, 357, sub, FT, GRAY)
    seg(70, "be", "ベルヌーイ・オイラー", "断面は中立軸に垂直を保つ")
    d.line((330, 90, 330, 345), fill=LGRAY, width=1)
    seg(370, "ti", "チモシェンコ", "せん断変形で断面が回転(垂直からずれ)")
    save(im, "v1e5BeamShearSection")


# ================================================ 5-19 シャシフレーム(開放断面) (required)
def f_chassis():
    im, d = new(); title(d, "自動車:キャビン・梯子型シャシフレーム(閉断面+一部開放断面)・マウント")
    # ladder frame (top view schematic)
    fy0, fy1 = 250, 320
    fx0, fx1 = 110, 550
    # two side rails
    d.line((fx0, fy0, fx1, fy0), fill=BLACK, width=6)
    d.line((fx0, fy1, fx1, fy1), fill=BLACK, width=6)
    # cross members (ladder rungs)
    for x in range(fx0 + 40, fx1, 80):
        d.line((x, fy0, x, fy1), fill=BLACK, width=4)
    ctext(d, 330, fy1 + 22, "梯子型シャシフレーム(閉断面部材)", FT, GRAY)
    # one open-section member highlighted
    ox = fx0 + 40 + 2 * 80
    d.line((ox, fy0, ox, fy1), fill=RED, width=5)
    ctext(d, ox, fy0 - 16, "開放断面部材", FT, RED)
    # cabin box on top
    box(d, 230, 130, 430, 205, FILL1)
    ctext(d, 330, 167, "車体キャビン", FS)
    # rubber mounts between cabin and frame
    for mx in (260, 400):
        spring(d, mx, 205, mx, fy0 - 2, coils=4, amp=8)
    ctext(d, 470, 232, "ゴム製マウント", FT, GRAY, "lm")
    # cross-section insets (top-right): closed vs open
    d.rectangle((470, 130, 496, 156), outline=BLACK, width=3); ctext(d, 505, 143, "閉断面", FT, GRAY, "lm")
    # C shape open
    cxs, cys = 480, 175
    d.line((cxs + 13, cys, cxs - 13, cys), fill=RED, width=3)
    d.line((cxs - 13, cys, cxs - 13, cys + 26), fill=RED, width=3)
    d.line((cxs - 13, cys + 26, cxs + 13, cys + 26), fill=RED, width=3)
    ctext(d, cxs + 22, cys + 13, "開放断面(C形)", FT, RED, "lm")
    note(d, "開放断面は反り(ワーピング)を生じ結合部のワーピング拘束で剛性増加")
    save(im, "v1e5ChassisFrameOpen")


# ================================================ 5-20 タイヤ幾何剛性 (required)
def f_tire_pressure():
    im, d = new(); title(d, "空気充填タイヤ断面:内圧が法線方向に作用・表面が伸ばされる")
    cx, cy = 330, 245
    # wheel disk (rim) - central hub
    d.rectangle((cx - 20, cy - 70, cx + 20, cy + 70), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, cy, "ホイール", FT, GRAY)
    # tire cross-section (torus cut) left and right lobes
    for s in (-1, 1):
        bx = cx + s * 20
        # outer arc of tire lobe
        pts = []
        for k in range(0, 61):
            a = math.radians(-80 + k * 160 / 60)
            pts.append((bx + s * (30 + 55 * math.cos(a)), cy - 90 * math.sin(a)))
        plot(d, 0, 0, pts, BLACK, 4)
        # inner arc
        ipts = []
        for k in range(0, 61):
            a = math.radians(-80 + k * 160 / 60)
            ipts.append((bx + s * (30 + 30 * math.cos(a)), cy - 62 * math.sin(a)))
        plot(d, 0, 0, ipts, GRAY, 2)
        # normal pressure arrows from inside pushing outward on inner surface
        for k in (15, 30, 45):
            a = math.radians(-80 + k * 160 / 60)
            ix, iy = bx + s * (30 + 30 * math.cos(a)), cy - 62 * math.sin(a)
            ox2, oy2 = bx + s * (30 + 48 * math.cos(a)), cy - 82 * math.sin(a)
            arrow(d, ix, iy, ox2, oy2, RED, 2, 8)
    ctext(d, cx, cy + 118, "内圧 p (法線方向)", FT, RED)
    # stretch (tension) arrows tangential on crown
    arrow(d, cx - 60, cy - 100, cx - 100, cy - 108, BLUE, 3, 10)
    arrow(d, cx + 60, cy - 100, cx + 100, cy - 108, BLUE, 3, 10)
    ctext(d, cx, cy - 120, "表面に伸張力 → 面外剛性が増加", FT, BLUE)
    note(d, "法線方向の内圧で外側に凸のタイヤ表面が伸ばされ幾何剛性が増す")
    save(im, "v1e5TirePressureStiff")


# ================================================ 5-21 ボデーパネルのビード (required)
def f_panel_bead():
    im, d = new(); title(d, "自動車フロアパネル:薄板・ビード(高さ2-5mm)・曲面形状(シェル要素)")
    # perspective panel (parallelogram)
    p = [(150, 300), (480, 300), (560, 180), (230, 180)]
    d.polygon(p, outline=BLACK, width=3, fill=FILL1)
    # surrounding frame (骨格)
    d.line((150, 300, 130, 320), fill=BLACK, width=4)
    d.line((480, 300, 500, 320), fill=BLACK, width=4)
    ctext(d, 305, 322, "骨格", FT, GRAY)
    # beads = parallel raised ridges (double lines) along panel
    for i in range(3):
        x0 = 210 + i * 70
        d.line((x0, 292, x0 + 78, 190), fill=BLUE, width=3)
        d.line((x0 + 8, 292, x0 + 86, 190), fill=BLUE, width=3)
    ctext(d, 300, 250, "ビード", FT, BLUE)
    # curved area indicated by arc
    d.arc((400, 210, 520, 300), 200, 340, fill=GREEN, width=3)
    ctext(d, 500, 250, "曲面形状", FT, GREEN, "lm")
    # bead cross-section inset (2-5mm)
    ix, iy = 150, 360
    d.line((ix, iy, ix + 40, iy), fill=BLACK, width=3)
    d.line((ix + 40, iy, ix + 50, iy - 16), fill=BLACK, width=3)
    d.line((ix + 50, iy - 16, ix + 70, iy - 16), fill=BLACK, width=3)
    d.line((ix + 70, iy - 16, ix + 80, iy), fill=BLACK, width=3)
    d.line((ix + 80, iy, ix + 120, iy), fill=BLACK, width=3)
    dim(d, ix + 130, iy, ix + 130, iy - 16, "2-5mm", col=GRAY)
    ctext(d, ix + 60, iy + 18, "ビード断面(薄板の張り出し)", FT, GRAY)
    note(d, "薄板=シェル要素。ビードも曲面形状も剛性を変えるので織り込む")
    save(im, "v1e5BodyPanelBead")


# ================================================ main
def main():
    f_guyan()
    f_whirl_self()
    f_deflect_tilt()
    f_fwd_bwd_whirl()
    f_gyro_coupling()
    f_gyro_speed()
    f_gyro_tilt_rotor()
    f_gyro_matrix()
    f_rotating_frame()
    f_internal_damping()
    f_int_ext_damping()
    f_transfer_matrix()
    f_strain_energy()
    f_shrink_fit()
    f_damping_material()
    f_cable_tension()
    f_suspension()
    f_beam_shear()
    f_chassis()
    f_tire_pressure()
    f_panel_bead()


if __name__ == "__main__":
    main()
