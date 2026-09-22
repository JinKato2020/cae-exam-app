# -*- coding: utf-8 -*-
"""振動1級 第5章「構造複合系の解析」公式・用語図 12枚。figlibで白地660x420線画。
文字化け回避のためギリシャ文字は英字表記(omega/theta/I_p等)に置換。"""
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


def disk(d, cx, cy, r=52, fill=FILL1):
    """回転円板(正面)。"""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=fill)


def shaft(d, x1, y, x2, y2=None, wd=6):
    y2 = y if y2 is None else y2
    d.line((x1, y, x2, y2), fill=BLACK, width=wd)


# 1. Guyan static reduction: master / slave DOF
def f_guyan():
    im, d = new()
    title(d, "Guyanの静縮小 (Master/Slave 自由度)")
    # full model: shaft with many nodes; master = bearings, slave = internal
    y = 150
    shaft(d, 90, y, 570, y, 6)
    xs = list(range(120, 560, 55))
    masters = {xs[0], xs[-1], xs[len(xs) // 2]}
    for x in xs:
        if x in masters:
            node(d, x, y, 9, RED)
        else:
            node(d, x, y, 6, "white")
    ctext(d, xs[0], y - 22, "Master", FT, RED)
    ctext(d, xs[len(xs) // 2], y - 22, "Master", FT, RED)
    ctext(d, xs[-1], y - 22, "Master", FT, RED)
    ctext(d, 330, y + 26, "白=Slave(内部) 自由度を静的に消去", FT, GRAY)
    # arrow to reduced model
    arrow(d, 330, 200, 330, 250, BLACK, 2, 11)
    ctext(d, 400, 224, "縮小", FT, RED, "lm")
    yr = 300
    shaft(d, 200, yr, 460, yr, 6)
    for x in (200, 330, 460):
        node(d, x, yr, 9, RED)
    ctext(d, 330, yr + 30, "Master節点だけの縮小系  u_slave = -[Kss]^-1 [Ksm] u_master", FT, BLACK)
    note(d, "軸受・制御力が働く節点をMasterに残し、内部自由度を弾性変形で近似消去")
    save(im, "v1f5Guyan")


# 2. Whirling motion: center M and mass G, unbalance e
def f_whirl():
    im, d = new()
    title(d, "振れ回り運動 (図心M・重心G・不つり合い e)")
    ox, oy = 330, 220
    # rotation orbit of M
    R = 110
    d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
    ctext(d, ox, oy - R - 16, "図心Mの軌道 (半径 x,y)", FT, GRAY)
    # bearing center O
    node(d, ox, oy, 5, BLACK); ctext(d, ox - 16, oy + 8, "O", FT, BLACK, "rm")
    # M at angle
    a = math.radians(35)
    Mx, My = ox + R * math.cos(a), oy - R * math.sin(a)
    arrow(d, ox, oy, Mx, My, BLUE, 3, 12)
    node(d, Mx, My, 8, FILL2); ctext(d, Mx + 14, My - 6, "M (図心)", FT, BLUE, "lm")
    # G offset by e from M
    e = 46
    Gx, Gy = Mx + e * math.cos(a), My - e * math.sin(a)
    d.line((Mx, My, Gx, Gy), fill=RED, width=3)
    node(d, Gx, Gy, 7, (250, 225, 225)); ctext(d, Gx + 12, Gy - 6, "G (重心)", FT, RED, "lm")
    ctext(d, (Mx + Gx) / 2 + 4, (My + Gy) / 2 - 16, "e", FT, RED)
    # centrifugal excitation
    force(d, Gx, Gy, 40 * math.cos(a), -40 * math.sin(a), "me*omega^2", RED)
    ctext(d, 330, 372, "m x'' + k x = m e omega^2 cos(omega t)  (同様に y)", FS, BLACK)
    note(d, "不つり合い e による遠心力 me*omega^2 が加振力となり M も G も円運動")
    save(im, "v1f5Whirl")


# 3. Self-centering: at high speed G moves to rotation center O
def f_selfcentering():
    im, d = new()
    title(d, "自動調心性 (高速で重心Gが回転中心Oへ)")
    # two panels: low speed vs high speed
    for k, (ox, lab, speed) in enumerate([(180, "低速 omega 小", 0), (490, "高速 omega 大", 1)]):
        oy = 230
        R = 80
        d.ellipse((ox - R, oy - R, ox + R, oy + R), outline=LGRAY, width=2)
        node(d, ox, oy, 5, BLACK); ctext(d, ox - 14, oy + 6, "O", FT, BLACK, "rm")
        if speed == 0:
            a = math.radians(40)
            Mx, My = ox + 55 * math.cos(a), oy - 55 * math.sin(a)
            Gx, Gy = Mx + 40 * math.cos(a), My - 40 * math.sin(a)
        else:
            # M on radius e circle, G near O
            a = math.radians(40)
            Mx, My = ox + 40 * math.cos(a), oy - 40 * math.sin(a)
            Gx, Gy = ox + 6, oy - 4
        arrow(d, ox, oy, Mx, My, BLUE, 2, 10)
        node(d, Mx, My, 7, FILL2); ctext(d, Mx + 12, My - 6, "M", FT, BLUE, "lm")
        d.line((Mx, My, Gx, Gy), fill=RED, width=2)
        node(d, Gx, Gy, 6, (250, 225, 225)); ctext(d, Gx + 10, Gy + 10, "G", FT, RED, "lm")
        ctext(d, ox, oy + R + 26, lab, FT, BLACK)
    arrow(d, 275, 230, 390, 230, RED, 3, 13)
    ctext(d, 330, 210, "omega 増", FT, RED)
    note(d, "危険速度を十分超えると G が軸心Oに寄り、図心Mだけが半径eの円を描く")
    save(im, "v1f5SelfCentering")


# 4. Tilting vibration with gyroscopic term
def f_tiltgyro():
    im, d = new()
    title(d, "傾き振動とジャイロモーメント")
    # shaft horizontal with a tilted disk in middle
    cy = 200
    shaft(d, 90, cy, 570, cy, 6)
    wall(d, 90, cy - 40, cy + 40, 1, 5)
    wall(d, 570, cy - 40, cy + 40, -1, 5)
    cx = 330
    # tilted disk drawn as ellipse (tilt about vertical)
    tilt = 18
    d.polygon([
        (cx - 12, cy - 62), (cx + 12, cy - 58),
        (cx + 12, cy + 62), (cx - 12, cy + 58)], outline=BLACK, width=3, fill=FILL1)
    ctext(d, cx, cy - 78, "傾いた円板", FT, BLACK)
    # spin arrow
    d.arc((cx - 30, cy - 30, cx + 30, cy + 30), -60, 120, fill=BLUE, width=3)
    arrow(d, cx + 30 * math.cos(math.radians(-60)), cy - 30 * math.sin(math.radians(-60)),
          cx + 40, cy + 10, BLUE, 2, 10)
    ctext(d, cx + 46, cy + 14, "自転 omega", FT, BLUE, "lm")
    # gyro moment arrow (out of tilt)
    arrow(d, cx + 30, cy - 40, cx + 90, cy - 70, RED, 3, 12)
    ctext(d, cx + 96, cy - 72, "ジャイロ\nモーメント", FT, RED, "lm")
    ctext(d, 330, 330, "I theta_x'' + I_p omega theta_y' + k_theta theta_x = 0", FS, BLACK)
    ctext(d, 330, 356, "I theta_y'' - I_p omega theta_x' + k_theta theta_y = 0", FS, BLACK)
    note(d, "theta_x と theta_y がジャイロ項で連成し、前向き・後向きの2固有振動数を生む")
    save(im, "v1f5TiltGyro")


# 5. Gyro term: antisymmetric coupling matrix
def f_gyro():
    im, d = new()
    title(d, "ジャイロ項の反対称結合 [G]=-[G]^T")
    # matrix showing antisymmetric off-diagonal
    matrix_grid(d, 175, 150, [["0", "+I_p omega"], ["-I_p omega", "0"]], cell=150, fnt=FS)
    ctext(d, 250, 120, "theta_x", FT, BLUE)
    ctext(d, 400, 120, "theta_y", FT, BLUE)
    ctext(d, 330, 340, "対角0・非対角は符号反転 (反対称) -> 減衰でなく復元力に作用", FT, GRAY)
    ctext(d, 330, 368, "omega=0 で消滅し連成も無くなる", FS, RED)
    save(im, "v1f5Gyro")


# 6. Rotating frame: Coriolis + centrifugal
def f_rotatingframe():
    im, d = new()
    title(d, "回転座標系 O-XY (コリオリ力・遠心力)")
    ox, oy = 300, 220
    # rotating axes X,Y tilted
    th = math.radians(25)
    L = 150
    arrow(d, ox, oy, ox + L * math.cos(th), oy - L * math.sin(th), BLACK, 2, 11)
    ctext(d, ox + L * math.cos(th) + 12, oy - L * math.sin(th), "X", FS, BLACK, "lm")
    arrow(d, ox, oy, ox - L * math.sin(th), oy - L * math.cos(th), BLACK, 2, 11)
    ctext(d, ox - L * math.sin(th) - 12, oy - L * math.cos(th) - 4, "Y", FS, BLACK, "rm")
    node(d, ox, oy, 5, BLACK); ctext(d, ox - 14, oy + 10, "O", FT, BLACK, "rm")
    # frame spin arrow
    d.arc((ox - 40, oy - 40, ox + 40, oy + 40), 200, 340, fill=GRAY, width=2)
    ctext(d, ox, oy + 52, "座標系が omega で回転", FT, GRAY)
    # mass point
    Px, Py = ox + 95 * math.cos(th) - 20 * math.sin(th), oy - 95 * math.sin(th) - 20 * math.cos(th)
    node(d, Px, Py, 7, FILL2); ctext(d, Px, Py - 20, "m", FT, BLACK)
    # centrifugal (radial out) and coriolis (perp)
    force(d, Px, Py, 44 * math.cos(th), -44 * math.sin(th), "遠心力 m omega^2", RED)
    force(d, Px, Py, -34 * math.sin(th), -34 * math.cos(th), "コリオリ 2m omega", GREEN)
    ctext(d, 330, 360, "m X'' + kX = 2m omega Y' + m omega^2 X + me omega^2", FT, BLACK)
    note(d, "コリオリ項は座標変換で現れるだけでエネルギーを散逸しない(減衰ではない)")
    save(im, "v1f5RotatingFrame")


# 7. Geometric stiffness by tension
def f_geomstiff():
    im, d = new()
    title(d, "幾何剛性 (張力で横剛性が増加)")
    # a taut string with lateral displacement, tension pulling back
    y0 = 200
    wall(d, 110, y0 - 40, y0 + 40, 1, 5)
    wall(d, 550, y0 - 40, y0 + 40, -1, 5)
    # deflected string
    pts = []
    for i in range(0, 101):
        t = i / 100.0
        yy = y0 - 55 * math.sin(math.pi * t)
        pts.append((110 + t * 440, yy))
    plot(d, 0, 0, pts, BLUE, 3)
    # straight reference
    dash(d, 110, y0, 550, y0, LGRAY)
    # tension arrows along ends
    force(d, 110, y0, -46, 0, "T", RED)
    force(d, 550, y0, 46, 0, "T", RED)
    # restoring component at mid
    mx = 330
    arrow(d, mx, y0 - 55, mx, y0 - 20, GREEN, 3, 12)
    ctext(d, mx + 10, y0 - 40, "張力の横成分\n=復元力増", FT, GREEN, "lm")
    ctext(d, 330, 320, "引張T -> 剛性増 -> 固有振動数up   圧縮 -> 剛性減", FS, BLACK)
    note(d, "張力(初期応力)を幾何剛性 [Kg] として剛性に加えてから固有値解析する")
    save(im, "v1f5GeomStiff")


# 8. Suspension bridge fish-bone model procedure
def f_suspension():
    im, d = new()
    title(d, "吊り橋 魚骨モデルの解析手順")
    # simple suspension bridge sketch top
    y = 150
    # towers
    for tx in (200, 460):
        d.line((tx, y - 60, tx, y + 40), fill=BLACK, width=4)
    # deck (beam)
    bar(d, 150, y + 40, 510, y + 40, 0)
    # main cable (parabola)
    cab = []
    for i in range(0, 101):
        t = i / 100.0
        x = 150 + t * 360
        # parabola dipping between towers
        yy = (y - 60) + 90 * (2 * (x - 330) / 360) ** 2
        yy = min(yy, y + 30)
        cab.append((x, yy))
    plot(d, 0, 0, cab, BLACK, 3)
    # hangers
    for hx in range(230, 440, 40):
        yy = (y - 60) + 90 * (2 * (hx - 330) / 360) ** 2
        yy = min(yy, y + 30)
        d.line((hx, yy, hx, y + 40), fill=GRAY, width=2)
    ctext(d, 330, y - 74, "ケーブル=トラス / 桁・塔=はり", FT, GRAY)
    # procedure boxes
    fbox(d, 150, 300, 210, 54, "1. 重力で静解析\n-> ケーブル張力", (225, 235, 245), FT)
    arrow(d, 258, 300, 300, 300, BLACK, 2, 11)
    fbox(d, 400, 300, 210, 54, "2. 張力を幾何剛性\nに反映", (225, 240, 225), FT)
    arrow(d, 400, 330, 400, 360, BLACK, 2, 11)
    fbox(d, 400, 385, 210, 40, "3. 固有値解析", FILL1, FT)
    note(d, "張力を無視した線形解析では誤り。静解析->幾何剛性->固有値の順")
    save(im, "v1f5Suspension")


# 9. Bernoulli-Euler beam: plane sections stay normal
def f_eulerbeam():
    im, d = new()
    title(d, "ベルヌーイ・オイラーはり (断面が中立軸に垂直保持)")
    # bent beam centerline
    y0 = 210
    pts = []
    for i in range(0, 101):
        t = i / 100.0
        yy = y0 - 70 * math.sin(math.pi * t * 0.5)
        pts.append((120 + t * 420, yy))
    plot(d, 0, 0, pts, BLACK, 4)
    ctext(d, 330, 300, "中立軸", FT, GRAY)
    # cross-sections perpendicular to centerline at few points
    for t in (0.25, 0.55, 0.85):
        i = int(t * 100)
        x, y = pts[i]
        # tangent direction
        x2, y2 = pts[min(i + 1, 100)]
        ang = math.atan2(y2 - y, x2 - x)
        # normal
        nx, ny = -math.sin(ang), math.cos(ang)
        d.line((x - nx * 42, y - ny * 42, x + nx * 42, y + ny * 42), fill=BLUE, width=3)
        # right-angle mark
        rx, ry = math.cos(ang), math.sin(ang)
        d.line((x + rx * 16, y + ry * 16, x + rx * 16 + nx * 14, y + ry * 16 + ny * 14), fill=RED, width=2)
        d.line((x + nx * 16, y + ny * 16, x + nx * 16 + rx * 14, y + ny * 16 + ry * 14), fill=RED, width=2)
    ctext(d, 330, 340, "変形後も断面(青)は中立軸に垂直(90deg)=せん断変形を無視", FS, BLACK)
    note(d, "細長い一様断面はりの曲げ固有振動数はこの理論で十分な精度")
    save(im, "v1f5EulerBeam")


# 10. Timoshenko beam: shear deformation, section not normal
def f_timoshenko():
    im, d = new()
    title(d, "チモシェンコはり (せん断変形・断面は非垂直)")
    y0 = 210
    pts = []
    for i in range(0, 101):
        t = i / 100.0
        yy = y0 - 70 * math.sin(math.pi * t * 0.5)
        pts.append((120 + t * 420, yy))
    plot(d, 0, 0, pts, BLACK, 4)
    ctext(d, 330, 300, "中立軸", FT, GRAY)
    for t in (0.25, 0.55, 0.85):
        i = int(t * 100)
        x, y = pts[i]
        x2, y2 = pts[min(i + 1, 100)]
        ang = math.atan2(y2 - y, x2 - x)
        nx, ny = -math.sin(ang), math.cos(ang)
        # section rotated by extra shear angle gamma from normal
        g = math.radians(20)
        rnx = nx * math.cos(g) - ny * math.sin(g)
        rny = nx * math.sin(g) + ny * math.cos(g)
        d.line((x - rnx * 42, y - rny * 42, x + rnx * 42, y + rny * 42), fill=BLUE, width=3)
        # true normal dashed for comparison
        dash(d, x, y, x + nx * 42, y + ny * 42, LGRAY)
    ctext(d, 330, 340, "断面(青)が垂直(灰破線)から角度 gamma だけ回転=せん断変形を考慮", FS, BLACK)
    note(d, "太く短いはり・高次モードでベルヌーイ・オイラーより高精度")
    save(im, "v1f5Timoshenko")


# 11. Warping and warping restraint of open section
def f_warping():
    im, d = new()
    title(d, "ワーピング(反り)とワーピング拘束")
    # open channel section drawn iso, warped (out-of-plane distortion)
    # left: free warping, right: restrained -> stiffness up
    # left channel
    def channel(ox, oy, warp):
        # C-shape flanges/web, front face lines with warp offsets
        dz = 60
        # web
        p = [(ox, oy), (ox, oy + 90)]
        d.line(p, fill=BLACK, width=3)
        # flanges top/bottom with out-of-plane (skew) offset when warp
        s = warp
        d.line((ox, oy, ox + 60 + s, oy - 18 - s * 0.4), fill=BLACK, width=3)
        d.line((ox, oy + 90, ox + 60 - s, oy + 108 + s * 0.4), fill=BLACK, width=3)
        # rear (depth) edges
        for (px, py) in [(ox, oy), (ox, oy + 90), (ox + 60 + s, oy - 18 - s * 0.4), (ox + 60 - s, oy + 108 + s * 0.4)]:
            dash(d, px, py, px + 40, py - 26, LGRAY)
    channel(150, 150, 26)
    ctext(d, 200, 290, "開放断面が反る\n(ワーピング自由)", FT, BLUE)
    arrow(d, 300, 200, 370, 200, BLACK, 2, 11)
    channel(430, 150, 4)
    # restraint wall at the joint
    wall(d, 415, 120, 270, -1, 7)
    ctext(d, 490, 290, "結合部で反りを拘束\n-> 剛性増加", FT, RED)
    note(d, "溝形など開放断面の反りが結合部で抑えられ剛性up。シェル要素で正確に表現")
    save(im, "v1f5Warping")


# 12. Tire geometric stiffness: normal pressure -> tension -> out-of-plane stiffness
def f_tire():
    im, d = new()
    title(d, "タイヤの法線圧力・面外剛性 (幾何剛性)")
    ox, oy = 300, 220
    # tire cross-section: two concentric circles (torus section as ring)
    Ro, Ri = 120, 78
    d.ellipse((ox - Ro, oy - Ro, ox + Ro, oy + Ro), outline=BLACK, width=3)
    d.ellipse((ox - Ri, oy - Ri, ox + Ri, oy + Ri), outline=BLACK, width=3)
    ctext(d, ox, oy, "内圧 p", FS, RED)
    # normal pressure arrows on inner surface (outward = normal)
    for a in range(0, 360, 45):
        ar = math.radians(a)
        x1 = ox + Ri * math.cos(ar); y1 = oy - Ri * math.sin(ar)
        x2 = ox + (Ri + 26) * math.cos(ar); y2 = oy - (Ri + 26) * math.sin(ar)
        arrow(d, x1, y1, x2, y2, RED, 2, 9)
    # tension (stretch) in shell surface, tangential
    for a in (35, 215):
        ar = math.radians(a)
        x = ox + (Ro) * math.cos(ar); y = oy - (Ro) * math.sin(ar)
        tx, ty = -math.sin(ar), -math.cos(ar)
        arrow(d, x - tx * 30, y - ty * 30, x + tx * 30, y + ty * 30, GREEN, 3, 11)
    ctext(d, ox + Ro + 4, oy - Ro + 10, "伸張力(引張)", FT, GREEN, "lm")
    ctext(d, 330, 356, "法線圧力 -> 表面が伸びて伸張力 -> 面外剛性が増加", FS, BLACK)
    note(d, "内圧を上げるほど伸張力が増し、横倒れ(面外)に対する硬さが上がる")
    save(im, "v1f5Tire")


if __name__ == "__main__":
    f_guyan(); f_whirl(); f_selfcentering(); f_tiltgyro()
    f_gyro(); f_rotatingframe(); f_geomstiff(); f_suspension()
    f_eulerbeam(); f_timoshenko(); f_warping(); f_tire()
    print("done v1f5 formula")
