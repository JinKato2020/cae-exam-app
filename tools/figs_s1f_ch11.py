# -*- coding: utf-8 -*-
"""固体1級 第11章 各種モデリング技術 — 公式・用語図(接頭辞 s1f11)。
figlib で白地660x420・黒線画。JSON本体は編集しない。
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

def dashpot(d, x1, y, x2, h=15):
    L = x2 - x1
    a = x1 + 0.28*L; b = x1 + 0.78*L
    d.line((x1, y, a, y), fill=BLACK, width=3)
    d.line((a, y-h, b, y-h), fill=BLACK, width=2)
    d.line((a, y-h, a, y+h), fill=BLACK, width=2)
    d.line((a, y+h, b, y+h), fill=BLACK, width=2)
    px = x1 + 0.60*L
    d.line((px, y-h+3, px, y+h-3), fill=BLACK, width=6)
    d.line((px, y, x2, y), fill=BLACK, width=3)

def vbar(d, x, y0, y1):
    d.line((x, y0, x, y1), fill=BLACK, width=5)

# ---------------------------------------------------------------- s1ch11-4
def f_Coupling():
    im, d = new(); title(d, "連成問題の解法(一体型/分離型)")
    # 左:一体型=強連成
    ctext(d, 175, 80, "一体型解法(強連成)", FS)
    d.rectangle((60, 110, 290, 250), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 175, 160, "全場を1つの", FS)
    ctext(d, 175, 188, "連立方程式に", FS)
    ctext(d, 175, 216, "まとめて直接解く", FS)
    ctext(d, 175, 285, "連成項をそのまま満たす", FT, GRAY)
    # 右:分離型=互い違い(弱連成)
    ctext(d, 485, 80, "分離型解法(互い違い法)", FS)
    d.rectangle((375, 130, 495, 210), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 435, 170, "場A", F)
    d.rectangle((555, 130, 630, 210), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 592, 170, "場B", FS)
    arrow(d, 495, 155, 555, 155, BLUE, 3, 12)
    arrow(d, 555, 190, 495, 190, RED, 3, 12)
    ctext(d, 525, 138, "予測値", FT, RED)
    ctext(d, 500, 285, "連成項に予測値=弱連成(反復収束で強連成)", FT, GRAY)
    note(d, "一体型=強連成 / 単純な互い違い=弱連成 / 反復すれば分離型でも強連成")
    save(im, "s1f11Coupling")

# ---------------------------------------------------------------- s1ch11-6
def f_DynEllipse():
    im, d = new(); title(d, "動的粘弾性:貯蔵弾性率 E' と損失弾性率 E''")
    cx, cy = 300, 245
    e0, s0 = 140, 135
    delta = math.radians(35)
    arrow(d, cx-e0-40, cy, cx+e0+40, cy, BLACK, 2, 11); ctext(d, cx+e0+48, cy, "ε", FS, BLACK, "lm")
    arrow(d, cx, cy+s0+40, cx, cy-s0-40, BLACK, 2, 11); ctext(d, cx+14, cy-s0-42, "σ", FS, BLACK, "lm")
    pts = []
    for i in range(0, 361, 4):
        th = math.radians(i)
        pts.append((cx + e0*math.sin(th), cy - s0*math.sin(th+delta)))
    plot(d, 0, 0, pts, BLUE, 4)
    yint = cy - s0*math.sin(delta)
    node(d, cx, yint, 5, "white", RED); ctext(d, cx+14, yint-6, "σ0 sinδ", FT, RED, "lm")
    node(d, cx, 2*cy-yint, 5, "white", RED)
    d.line((cx+e0, cy-4, cx+e0, cy+4), fill=GRAY, width=2); ctext(d, cx+e0, cy+18, "ε0", FT, GRAY)
    # 右上に式
    ctext(d, 560, 120, "E'=(σ0/ε0)cosδ", FT, BLUE)
    ctext(d, 560, 145, "E''=(σ0/ε0)sinδ", FT, ORANGE)
    ctext(d, 560, 170, "tanδ=E''/E'", FT, GRAY)
    note(d, "同位相成分=E'(cosδ・貯蔵) / 90°ずれ成分=E''(sinδ・損失)")
    save(im, "s1f11DynEllipse")

# ---------------------------------------------------------------- s1ch11-10
def f_GenMaxwell():
    im, d = new(); title(d, "一般化マクスウェルモデル(プローニー級数)")
    xL, xR = 110, 570; y0, y1 = 95, 335
    vbar(d, xL, y0, y1); vbar(d, xR, y0, y1)
    ys = [125, 200, 270, 320]
    spring(d, xL, ys[0], xR, ys[0], coils=7, amp=13)
    ctext(d, 340, ys[0]-24, "E∞ (長期弾性率のバネ)", FT, GRAY)
    for k, y in enumerate([ys[1], ys[2]], start=1):
        xm = 340
        spring(d, xL, y, xm, y, coils=5, amp=12)
        dashpot(d, xm, y, xR, y)
        ctext(d, (xL+xm)/2, y-22, "E%d" % k, FT)
        ctext(d, (xm+xR)/2, y-22, "η%d" % k, FT)
    ctext(d, 340, ys[3], "⋮ (緩和時間 τi = ηi / Ei が異なる要素を並列)", FT, GRAY)
    arrow(d, xL-40, 215, xL, 215, RED, 4, 14); arrow(d, xR+40, 215, xR, 215, RED, 4, 14)
    ctext(d, xL-45, 238, "ε0", FT, RED); ctext(d, xR+45, 238, "ε0", FT, RED)
    note(d, "一定ひずみで E(t)=E∞+ΣEi e^(-t/τi) (t→∞ で E∞ が残る)")
    save(im, "s1f11GenMaxwell")

# ---------------------------------------------------------------- s1ch11-12
def f_EffStress():
    im, d = new(); title(d, "有効面積 Ã=(1-D)A と有効応力")
    d.rectangle((175, 115, 485, 180), outline=BLACK, width=3, fill=FILL1)
    arrow(d, 175, 147, 118, 147, RED, 4, 15); ctext(d, 110, 147, "F", F, RED, "rm")
    arrow(d, 485, 147, 542, 147, RED, 4, 15); ctext(d, 550, 147, "F", F, RED, "lm")
    d.line((330, 115, 330, 180), fill=GRAY, width=2)
    arrow(d, 330, 198, 330, 238, GRAY, 2, 10)
    d.rectangle((250, 245, 410, 385), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 230, "見かけ面積 A", FT, GRAY)
    for (vx, vy, vr) in [(285, 285, 13), (355, 295, 16), (300, 345, 14), (375, 350, 11), (330, 315, 10)]:
        d.ellipse((vx-vr, vy-vr, vx+vr, vy+vr), outline=BLACK, width=2, fill="white")
    ctext(d, 468, 295, "空隙(D)", FT); arrow(d, 446, 295, 392, 295, GRAY, 2, 10)
    ctext(d, 330, 402, "有効面積 Ã=(1-D)A → σ̃=F/Ã=σ/(1-D)", FT, RED)
    save(im, "s1f11EffStress")

# ---------------------------------------------------------------- s1ch11-18
def f_Laminate():
    im, d = new(); title(d, "古典積層板理論(CLPT)とABD剛性")
    xl, xr = 150, 360
    ys = [130, 170, 210, 250, 290]
    for k in range(len(ys)-1):
        fill = [FILL1, FILL2, FILL3, FILL2][k]
        d.rectangle((xl, ys[k], xr, ys[k+1]), outline=BLACK, width=2, fill=fill)
    zmid = (ys[0]+ys[-1])/2
    zx = 400
    arrow(d, zx, ys[-1]+30, zx, ys[0]-30, BLACK, 2, 11); ctext(d, zx, ys[0]-40, "z", FS)
    d.line((xl, zmid, 470, zmid), fill=RED, width=2); ctext(d, 435, zmid-13, "中央面 z=0", FT, RED)
    labs = ["z0", "z1", "z2", "z3", "z4"]
    for k, y in enumerate(ys):
        d.line((zx-6, y, zx+6, y), fill=BLACK, width=2)
        ctext(d, zx+24, y, labs[k], FT, GRAY, "lm")
    arrow(d, xl-45, zmid, xl, zmid, GREEN, 4, 13); ctext(d, xl-52, zmid, "N", F, GREEN, "rm")
    d.arc((500, 185, 590, 275), 40, 320, fill=BLUE, width=4)
    arrow(d, 585, 200, 578, 185, BLUE, 3, 10)
    ctext(d, 545, 150, "面内力 N", FT, GREEN); ctext(d, 545, 295, "M(曲げ)", FT, BLUE)
    note(d, "N=Aε+Bκ, M=Bε+Dκ / Aを z^1・Bを z^2・Dを z^3 で積分(対称積層 B=0)")
    save(im, "s1f11Laminate")

if __name__ == "__main__":
    f_Coupling(); f_DynEllipse(); f_GenMaxwell(); f_EffStress(); f_Laminate()
    print("=== s1f11 done ===")
