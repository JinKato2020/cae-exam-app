# -*- coding: utf-8 -*-
"""振動2級 第3章「材料力学の基礎」公式・用語カード用の図 18枚。接頭辞 v2f3。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def rect(d, x0, y0, x1, y1, fill=FILL1, w=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=w, fill=fill)


# 1. 縦の伸びと横の縮み ------------------------------------------------------
def f01():
    im, d = new(); title(d, "縦の伸びと横の縮み（引張前後）")
    # 変形前
    x0, w0, top0, bot0 = 150, 78, 100, 300
    rect(d, x0 - w0/2, top0, x0 + w0/2, bot0)
    ctext(d, x0, 82, "変形前", FS)
    dim(d, x0 + w0/2 + 26, top0, x0 + w0/2 + 26, bot0, "L0")
    dim(d, x0 - w0/2, bot0 + 30, x0 + w0/2, bot0 + 30, "D0")
    # 変形後(縦に伸び横に縮む)
    x1, w1, top1, bot1 = 470, 54, 78, 322
    rect(d, x1 - w1/2, top1, x1 + w1/2, bot1, FILL2)
    ctext(d, x1, 60, "変形後", FS)
    force(d, x1, top1, 0, -40, "P")
    force(d, x1, bot1, 0, 40, "P")
    dim(d, x1 + w1/2 + 30, top1, x1 + w1/2 + 30, bot1, "L1 (>L0)")
    dim(d, x1 - w1/2, bot1 + 30, x1 + w1/2, bot1 + 30, "D1 (<D0)")
    note(d, "縦に伸びる分だけ横は縮む")
    save(im, "v2f3StrainNormalLateral")


# 2. ポアソン比 -------------------------------------------------------------
def f02():
    im, d = new(); title(d, "ポアソン比 nu = 横ひずみ / 縦ひずみ")
    x, w, top, bot = 210, 70, 110, 300
    rect(d, x - w/2, top, x + w/2, bot, FILL2)
    force(d, x, top, 0, -42, "P")
    force(d, x, bot, 0, 42, "P")
    # 縦ひずみ
    dim(d, x + w/2 + 26, top, x + w/2 + 26, bot, "縦: epsilon = dL/L")
    # 横ひずみ
    dim(d, x - w/2, bot + 30, x + w/2, bot + 30, "横: epsilon' = dD/D")
    ctext(d, 500, 175, "nu = - epsilon' / epsilon", F, BLUE)
    ctext(d, 500, 215, "(縦伸び1に対し", FT)
    ctext(d, 500, 236, "横がnuだけ縮む)", FT)
    ctext(d, 500, 268, "金属で約0.3", FT, GRAY)
    save(im, "v2f3PoissonRatio")


# 3. ひずみ-変位関係 epsilon=du/dx ------------------------------------------
def f03():
    im, d = new(); title(d, "ひずみと変位  epsilon = du/dx")
    y = 170; x0 = 90; x1 = 560
    d.line((x0, y, x1, y), fill=BLACK, width=4)
    force(d, x1, y, 40, 0, "P")
    # 微小要素dx(変形前)
    a, b = 250, 310
    for xx in (a, b):
        d.line((xx, y - 22, xx, y + 22), fill=GRAY, width=2)
    dim(d, a, y - 40, b, y - 40, "dx")
    # 変形後(下段)
    y2 = 300
    d.line((x0, y2, x1 + 30, y2), fill=LGRAY, width=4)
    a2, b2 = 250, 340   # dx が dx+du に伸びる
    for xx in (a2, b2):
        d.line((xx, y2 - 22, xx, y2 + 22), fill=RED, width=2)
    dim(d, a2, y2 + 40, b2, y2 + 40, "dx + du")
    d.line((b, y + 22, b2, y2 - 22), fill=RED, width=1)
    ctext(d, 470, 300, "変形後", FS)
    note(d, "要素の伸び du を元の長さ dx で割る")
    save(im, "v2f3StrainDisplacement")


# 4. せん断ひずみ gamma ------------------------------------------------------
def f04():
    im, d = new(); title(d, "せん断ひずみ gamma（直角の変化）")
    s = 150; x0 = 200; y0 = 110; delta = 60
    # 変形前(点線正方形)
    d.rectangle((x0, y0, x0 + s, y0 + s), outline=LGRAY, width=2)
    # 変形後(平行四辺形): 底辺固定, 上辺右にdelta
    bl = (x0, y0 + s); br = (x0 + s, y0 + s)
    tl = (x0 + delta, y0); tr = (x0 + s + delta, y0)
    d.polygon([bl, br, tr, tl], outline=BLACK, width=3)
    # 底面固定ハッチ
    hwall(d, x0 - 10, x0 + s + 10, y0 + s + 3, side=1, n=8)
    force(d, x0 + delta + s/2, y0 - 8, 46, 0, "tau", col=RED)
    # gamma 角: 左下角で 鉛直と変形左辺の間
    ang = math.degrees(math.atan2(s, delta))   # 変形左辺の仰角
    angle_arc(d, bl[0], bl[1], 48, ang, 90, "gamma", RED)
    note(d, "gamma = 直角からのずれ角（ラジアン）")
    save(im, "v2f3ShearStrain")


# 5. フックの法則 -----------------------------------------------------------
def f05():
    im, d = new(); title(d, "フックの法則  sigma=E epsilon,  tau=G gamma")
    # 左: sigma-epsilon
    ox, oy = 110, 300; axes(d, ox, oy, 180, 190, "epsilon", "sigma")
    plot(d, ox, oy, [(ox, oy), (ox + 150, oy - 160)], BLUE)
    ctext(d, ox + 130, oy - 100, "傾き E", FT, BLUE)
    # 右: tau-gamma
    ox2, oy2 = 400, 300; axes(d, ox2, oy2, 180, 190, "gamma", "tau")
    plot(d, ox2, oy2, [(ox2, oy2), (ox2 + 150, oy2 - 160)], GREEN)
    ctext(d, ox2 + 130, oy2 - 100, "傾き G", FT, GREEN)
    note(d, "弾性域では応力とひずみが比例する")
    save(im, "v2f3Hooke")


# 6. 弾性定数の関係 ---------------------------------------------------------
def f06():
    im, d = new(); title(d, "弾性定数の関係（2つ決めれば残りは従属）")
    E = (330, 110); G = (170, 320); nu = (490, 320)
    d.line([E, G, nu, E], fill=BLACK, width=3)
    for p, s in [(E, "E"), (G, "G"), (nu, "nu")]:
        node(d, p[0], p[1], 24, "white")
        ctext(d, p[0], p[1], s, F)
    ctext(d, 330, 250, "G = E / (2(1+nu))", FS, BLUE)
    ctext(d, 250, 220, "縦弾性", FT, GRAY)
    ctext(d, 410, 220, "横弾性", FT, GRAY)
    ctext(d, 330, 360, "ポアソン比", FT, GRAY)
    save(im, "v2f3ElasticConstants")


# 7. 一般化フックの法則 -----------------------------------------------------
def f07():
    im, d = new(); title(d, "一般化フックの法則（3軸応力）")
    ox, oy, w, h, dp = 250, 250, 120, 120, 90
    iso_box(d, ox, oy, w, h, dp)
    dx = int(dp*0.8); dy = int(dp*0.5)
    # sigma_x (右面から右へ)
    force(d, ox + w + dx, oy + h/2 - dy/2, 60, 0, "sigma_x", col=RED)
    # sigma_y (上面から上へ)
    force(d, ox + w/2 + dx/2, oy - dy, 0, -55, "sigma_y", col=BLUE)
    # sigma_z (前面から手前=左下へ)
    force(d, ox + w/2, oy + h, -50, 32, "sigma_z", col=GREEN)
    ctext(d, 330, 360, "各軸のひずみは3方向の応力とnuで連動", FT, GRAY)
    save(im, "v2f3GeneralizedHooke")


# 8. 平面応力と平面ひずみ ---------------------------------------------------
def f08():
    im, d = new(); title(d, "平面応力（薄板）と平面ひずみ（長柱）")
    # 左: 薄い板 sigma_z=0
    iso_box(d, 90, 250, 150, 120, 26)
    ctext(d, 165, 300, "平面応力", FS)
    ctext(d, 165, 340, "sigma_z = 0", FT, RED)
    ctext(d, 165, 362, "(薄い板)", FT, GRAY)
    # 右: 長い柱 epsilon_z=0
    iso_box(d, 400, 150, 90, 200, 70)
    ctext(d, 470, 300, "平面ひずみ", FS)
    ctext(d, 470, 340, "epsilon_z = 0", FT, BLUE)
    ctext(d, 470, 362, "(長い柱)", FT, GRAY)
    save(im, "v2f3PlaneStressStrain")


# 9. せん断応力 tau=Q/A -----------------------------------------------------
def f09():
    im, d = new(); title(d, "せん断応力  tau = Q / A")
    x0, y0, x1, y1 = 180, 120, 320, 320
    rect(d, x0, y0, x1, y1, FILL1)
    ctext(d, (x0+x1)/2, (y0+y1)/2, "断面 A", FS)
    # 断面に平行なせん断力Q
    force(d, x1 + 40, y0, 0, y1 - y0, "Q", col=RED)
    # tau 分布(断面に平行な小矢印)
    for yy in range(y0 + 30, y1, 45):
        arrow(d, x0 + 12, yy, x1 - 12, yy, GRAY, 2, 8)
    ctext(d, 500, 170, "tau: 断面に", FT)
    ctext(d, 500, 192, "平行な応力", FT)
    ctext(d, 500, 232, "Q を断面積 A", FT, BLUE)
    ctext(d, 500, 254, "で割った値", FT, BLUE)
    save(im, "v2f3ShearStress")


# 10. 弾性と塑性(負荷-除荷) -------------------------------------------------
def f10():
    im, d = new(); title(d, "弾性（原点へ戻る）と塑性（永久ひずみ）")
    ox, oy = 110, 320; axes(d, ox, oy, 470, 250, "epsilon", "sigma")
    # 弾性: 上って同じ線で戻る
    ep = (ox + 120, oy - 150)
    plot(d, ox, oy, [(ox, oy), ep], BLUE)
    arrow(d, ep[0], ep[1], ep[0] - 40, ep[1] + 50, BLUE, 2, 10)
    ctext(d, ox + 60, oy - 130, "弾性", FS, BLUE)
    # 塑性: 上って平行に除荷し残留ひずみ
    p1 = (ox + 270, oy - 40); p2 = (ox + 330, oy - 170)
    plot(d, ox, oy, [(ox, oy), p1, p2], RED)
    res = (ox + 210, oy)   # 除荷で戻る先(x軸上)
    plot(d, ox, oy, [p2, res], RED)
    d.line((res[0], oy, res[0], oy + 8), fill=RED, width=2)
    ctext(d, ox + 300, oy - 120, "塑性", FS, RED)
    ctext(d, res[0], oy + 24, "永久ひずみ", FT, RED)
    save(im, "v2f3StressDefinition")


# 11. 応力-ひずみ線図(軟鋼) -------------------------------------------------
def f11():
    im, d = new(); title(d, "軟鋼の応力-ひずみ線図")
    ox, oy = 90, 330; axes(d, ox, oy, 500, 260, "epsilon", "sigma")
    P = (ox + 90, oy - 150)     # 比例限度
    UY = (ox + 120, oy - 185)   # 上降伏点
    LY = (ox + 175, oy - 165)   # 下降伏点(降伏棚)
    TS = (ox + 360, oy - 235)   # 引張強さ(最大)
    FR = (ox + 450, oy - 190)   # 破断点
    # 弾性直線
    plot(d, ox, oy, [(ox, oy), P], BLUE)
    # 降伏棚〜加工硬化〜破断
    pts = [P, UY, LY, (ox + 230, oy - 168), TS, FR]
    plot(d, ox, oy, pts, RED)
    for p, s in [(P, "比例限度"), (UY, "上降伏点"), (LY, "下降伏点"),
                 (TS, "引張強さ"), (FR, "破断")]:
        node(d, p[0], p[1], 4, BLACK)
        ctext(d, p[0], p[1] - 16, s, FT)
    ctext(d, ox + 45, oy - 40, "弾性域", FT, BLUE)
    ctext(d, ox + 330, oy - 30, "塑性域", FT, RED)
    save(im, "v2f3StressStrainCurve")


# 12. 重ね合わせ(段付き棒) --------------------------------------------------
def f12():
    im, d = new(); title(d, "重ね合わせ  delta = (P1 + 2 P2) L / AE")
    y = 190; x0 = 110; xm = 350; xe = 560
    wall(d, x0, y - 40, y + 40, side=1)
    rect(d, x0, y - 30, xm, y + 30, FILL1)
    rect(d, xm, y - 30, xe, y + 30, FILL2)
    force(d, xm, y, 0, -70, "P1", col=RED)
    force(d, xe, y, 55, 0, "P2", col=BLUE)
    dim(d, x0, y + 55, xm, y + 55, "L")
    dim(d, xm, y + 55, xe, y + 55, "L")
    ctext(d, 330, 320, "各荷重による伸びを足し合わせる", FT, GRAY)
    save(im, "v2f3Superposition")


# 13. 断面二次モーメント(3断面) --------------------------------------------
def f13():
    im, d = new(); title(d, "断面二次モーメント（中立軸まわり）")
    def na(cx, y0, y1, name):
        d.line((cx - 90, (y0+y1)/2, cx + 90, (y0+y1)/2), fill=RED, width=2)
        ctext(d, cx, y1 + 22, name, FT)
    # 円
    cx = 150; cy = 200; r = 55
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=BLACK, width=3, fill=FILL1)
    na(cx, cy-r, cy+r, "円")
    arrow(d, cx, cy, cx, cy - r, GRAY, 2, 8); ctext(d, cx + 14, cy - r/2, "r", FT, GRAY)
    # 中空円
    cx = 340
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx-30, cy-30, cx+30, cy+30), outline=BLACK, width=3, fill="white")
    na(cx, cy-r, cy+r, "中空円")
    # 長方形
    cx = 530; bw = 70; bh = 110
    rect(d, cx-bw/2, cy-bh/2, cx+bw/2, cy+bh/2, FILL1)
    na(cx, cy-bh/2, cy+bh/2, "長方形")
    arrow(d, cx, cy, cx, cy - bh/2, GRAY, 2, 8); ctext(d, cx + 14, cy - bh/4, "r", FT, GRAY)
    note(d, "中立軸からの距離 r の2乗を断面で積分")
    save(im, "v2f3SecondMoment")


# 14. 断面二次極モーメント Ip=Ix+Iy ----------------------------------------
def f14():
    im, d = new(); title(d, "断面二次極モーメント  Ip = Ix + Iy")
    cx, cy, r = 260, 220, 95
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 5, BLACK); ctext(d, cx - 16, cy + 14, "図心", FT)
    # x,y軸
    d.line((cx - r - 20, cy, cx + r + 20, cy), fill=GRAY, width=2); ctext(d, cx + r + 30, cy, "x", FT, GRAY, "lm")
    d.line((cx, cy - r - 20, cx, cy + r + 20), fill=GRAY, width=2); ctext(d, cx, cy - r - 30, "y", FT, GRAY)
    # z軸(手前)
    force(d, cx, cy, -55, 42, "z (面外)", col=GREEN)
    # 距離r to 微小要素
    ex, ey = cx + 55, cy - 62
    d.line((cx, cy, ex, ey), fill=RED, width=2); ctext(d, (cx+ex)/2 + 6, (cy+ey)/2 - 10, "r", FT, RED)
    node(d, ex, ey, 4, RED); ctext(d, ex + 12, ey - 8, "dA", FT, RED, "lm")
    note(d, "図心を通る z 軸まわり = x,y 断面二次の和")
    save(im, "v2f3PolarMoment")


# 15. はりのたわみ ----------------------------------------------------------
def f15():
    im, d = new(); title(d, "はりのたわみ  d^2 y/dx^2 = - M / (EI)")
    x0, x1, y = 110, 560, 170
    d.line((x0, y, x1, y), fill=LGRAY, width=2)   # 変形前の軸
    pin_support(d, x0, y); roller_support(d, x1, y)
    force(d, (x0+x1)/2, y - 70, 0, 60, "P", col=RED)
    # たわみ曲線 y(x)
    pts = []
    for i in range(0, 101, 4):
        t = i/100; xx = x0 + (x1-x0)*t
        yy = y + 90 * (t*(1-t))*4   # 中央最大の下凸
        pts.append((xx, yy))
    plot(d, 0, 0, pts, BLUE)
    ctext(d, (x0+x1)/2 + 30, y + 100, "y(x)", FS, BLUE)
    axes(d, x0 - 30, y - 20, 40, 50, "x", "y")
    note(d, "曲率は曲げモーメント M と曲げ剛性 EI で決まる")
    save(im, "v2f3BeamDeflection")


# 16. 境界条件(3種の支持) --------------------------------------------------
def f16():
    im, d = new(); title(d, "支持と境界条件")
    y = 190
    # 自由端
    cx = 140
    d.line((cx - 55, y, cx + 30, y), fill=BLACK, width=5)
    node(d, cx + 30, y, 6, "white")
    ctext(d, cx, 250, "自由端", FS)
    ctext(d, cx, 285, "M=0, Q=0", FT, RED)
    # 単純支持
    cx = 340
    d.line((cx - 55, y, cx + 55, y), fill=BLACK, width=5)
    roller_support(d, cx, y)
    ctext(d, cx, 260, "単純支持", FS)
    ctext(d, cx, 295, "y=0, M=0", FT, RED)
    # 固定支持
    cx = 540
    wall(d, cx - 40, y - 40, y + 40, side=1)
    d.line((cx - 40, y, cx + 40, y), fill=BLACK, width=5)
    ctext(d, cx, 250, "固定支持", FS)
    ctext(d, cx, 285, "y=0, 傾き=0", FT, RED)
    save(im, "v2f3BoundaryConditions")


# 17. 反力 ------------------------------------------------------------------
def f17():
    im, d = new(); title(d, "支点反力（支持ごとの反力成分）")
    x0, x1, y = 130, 540, 160
    d.line((x0, y, x1, y), fill=BLACK, width=5)
    pin_support(d, x0, y); roller_support(d, x1, y)
    force(d, (x0+x1)/2, y - 70, 0, 60, "P", col=RED)
    force(d, x0, y + 40, 0, -45, "RA", col=BLUE)
    force(d, x1, y + 40, 0, -45, "RB", col=BLUE)
    ctext(d, x0, 290, "ピン", FT); ctext(d, x0, 312, "反力2成分", FT, GRAY)
    ctext(d, x1, 290, "ローラ", FT); ctext(d, x1, 312, "反力1成分", FT, GRAY)
    ctext(d, 335, 352, "固定支持は反力3成分（水平・鉛直・モーメント）", FT, GRAY)
    save(im, "v2f3Reactions")


# 18. SFD・BMD --------------------------------------------------------------
def f18():
    im, d = new(); title(d, "荷重図・SFD・BMD")
    x0, x1 = 120, 540; mid = (x0 + x1)/2
    # 荷重図
    y = 90
    d.line((x0, y, x1, y), fill=BLACK, width=4)
    pin_support(d, x0, y, 16); roller_support(d, x1, y, 16)
    force(d, mid, y - 46, 0, 38, "P", col=RED)
    # SFD
    yb = 200
    d.line((x0, yb, x1, yb), fill=GRAY, width=1)
    d.line((x0, yb - 30, mid, yb - 30), fill=BLUE, width=3)
    d.line((mid, yb - 30, mid, yb + 30), fill=BLUE, width=3)
    d.line((mid, yb + 30, x1, yb + 30), fill=BLUE, width=3)
    d.line((x0, yb, x0, yb - 30), fill=BLUE, width=3)
    d.line((x1, yb, x1, yb + 30), fill=BLUE, width=3)
    ctext(d, x0 - 30, yb, "SFD", FT, BLUE, "rm")
    # BMD
    yc = 320
    d.line((x0, yc, x1, yc), fill=GRAY, width=1)
    d.line((x0, yc, mid, yc + 55), fill=GREEN, width=3)
    d.line((mid, yc + 55, x1, yc), fill=GREEN, width=3)
    node(d, mid, yc + 55, 4, GREEN)
    ctext(d, mid, yc + 74, "最大曲げモーメント", FT, GREEN)
    ctext(d, x0 - 30, yc, "BMD", FT, GREEN, "rm")
    save(im, "v2f3SfdBmd")


if __name__ == "__main__":
    for fn in [f01, f02, f03, f04, f05, f06, f07, f08, f09, f10,
               f11, f12, f13, f14, f15, f16, f17, f18]:
        fn()
    print("done 18")
