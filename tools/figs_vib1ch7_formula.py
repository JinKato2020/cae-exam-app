# -*- coding: utf-8 -*-
"""振動1級 第7章「流体連成系の解析基礎」公式・用語図 5枚。figlibで白地660x420線画。
文字化け回避のためギリシャ文字・記号は英字/簡易表記(rho,theta,pi,a^2,St,V,D等)に置換。"""
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


def marc(d, cx, cy, r, a0, a1, col=RED, wd=3, label="", ccw=True):
    d.arc((cx - r, cy - r, cx + r, cy + r), -a1, -a0, fill=col, width=wd)
    ae = math.radians(a1 if ccw else a0)
    ex, ey = cx + r * math.cos(ae), cy - r * math.sin(ae)
    tx, ty = (-math.sin(ae), -math.cos(ae)) if ccw else (math.sin(ae), math.cos(ae))
    arrow(d, ex, ey, ex + 14 * tx, ey + 14 * ty, col, wd, 12)
    if label:
        am = math.radians((a0 + a1) / 2)
        ctext(d, cx + (r + 18) * math.cos(am), cy - (r + 18) * math.sin(am), label, FS, col)


def vortex(d, x, y, r, ccw=True, col=BLUE):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=2)
    if ccw:
        arrow(d, x + 4, y - r, x - 7, y - r, col, 2, 7)
    else:
        arrow(d, x - 4, y - r, x + 7, y - r, col, 2, 7)


# 1. 非定常空気力 L と モーメント M(上下y・回転thetaの2自由度)
def f_two_dof_aero():
    im, d = new()
    title(d, "非定常空気力: 上下y・回転thetaの剛体に働く力Lとモーメント M")
    cx, cy = 340, 215
    d.ellipse((cx - 100, cy - 26, cx + 100, cy + 26), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 6, "white"); ctext(d, cx, cy + 20, "弾性軸", FT, GRAY)
    # 一様流
    for yy in (cy - 42, cy, cy + 42):
        arrow(d, 70, yy, 150, yy, GRAY, 2, 10)
    ctext(d, 100, cy - 64, "一様流 V", FS, GRAY)
    # 上下自由度 y
    arrow(d, cx + 130, cy, cx + 130, cy - 50, BLUE, 3, 12); ctext(d, cx + 142, cy - 28, "y", FS, BLUE, "lm")
    # 回転自由度 theta
    marc(d, cx + 66, cy, 30, 20, 120, BLUE, 2, "theta", ccw=True)
    # 空気力 L(上下方向の力)
    arrow(d, cx - 50, cy - 26, cx - 50, cy - 82, RED, 4, 14); ctext(d, cx - 50, cy - 98, "力 L", FS, RED)
    # モーメント M
    marc(d, cx, cy, 62, 320, 40, RED, 3, "M", ccw=True)
    box(d, 90, 330, 570, 388, FILL1)
    ctext(d, 330, 359, "L,M は y,theta とその速度に依存 → 減衰・剛性行列に非対角(連成)項", FT)
    save(im, "v1f7TwoDofAeroForce")


# 2. スロッシング(自由液面の揺動・重力復元)
def f_sloshing():
    im, d = new()
    title(d, "スロッシング: 自由液面が重力復元力で揺れる(低振動数)")
    x0, x1 = 160, 500; yt, yb = 150, 330
    d.line((x0, yt, x0, yb), fill=BLACK, width=3)
    d.line((x1, yt, x1, yb), fill=BLACK, width=3)
    d.line((x0, yb, x1, yb), fill=BLACK, width=3)
    ctext(d, (x0 + x1) / 2, yt - 6, "容器", FT, GRAY)
    # 傾いた自由液面(平衡=破線)
    ymean = 220
    dash(d, x0, ymean, x1, ymean, LGRAY); ctext(d, x1 + 10, ymean, "平衡位置", FT, GRAY, "lm")
    pts = [(x0 + (x1 - x0) * t, ymean - 30 * math.sin(math.pi * t)) for t in [i / 60 for i in range(61)]]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, (x0 + x1) / 2, 270, "液体", FT, GRAY)
    # 重力復元(高い側を戻す)
    arrow(d, x0 + 40, ymean - 26, x0 + 40, ymean + 6, RED, 3, 11); ctext(d, x0 + 40, ymean - 44, "重力復元", FT, RED)
    ctext(d, 330, 356, "自由液面が平衡からずれると重力で復元 → 低振動数で大きく揺れる", FS, BLACK)
    save(im, "v1f7Sloshing")


# 3. ギャロッピング(非円形断面の空力自励振動)
def f_galloping():
    im, d = new()
    title(d, "ギャロッピング: 非円形断面の空力自励振動(揚力が運動を助長)")
    cx, cy = 320, 225
    # 半円柱断面
    d.pieslice((cx - 40, cy - 45, cx + 50, cy + 45), -90, 90, outline=BLACK, width=3, fill=FILL1)
    d.line((cx + 5, cy - 45, cx + 5, cy + 45), fill=BLACK, width=3)
    # 一様流
    for yy in (cy - 30, cy + 30):
        arrow(d, 90, yy, 180, yy, GRAY, 2, 11)
    ctext(d, 130, cy - 52, "一様流 U", FS, GRAY)
    # 物体の運動
    arrow(d, cx, cy - 50, cx, cy - 108, BLUE, 3, 12); ctext(d, cx, cy - 126, "運動 y'", FT, BLUE)
    # 同じ向きの揚力(助長)
    arrow(d, cx + 60, cy, cx + 60, cy - 66, RED, 4, 14); ctext(d, cx + 74, cy - 40, "揚力(同じ向き)", FT, RED, "lm")
    # 成長する振幅
    pts = [(470 + 90 * t, cy - (8 + 30 * t) * math.sin(2 * math.pi * 1.6 * t)) for t in [i / 80 for i in range(81)]]
    plot(d, 0, 0, pts, RED, 2)
    ctext(d, 515, cy + 80, "振幅増大", FT, RED)
    ctext(d, 330, 356, "小さな乱れに対し運動と同じ向きの揚力が発生し発散する自励振動", FS, BLACK)
    save(im, "v1f7Galloping")


# 4. 渦励振・カルマン渦(強制振動)
def f_karman_vortex():
    im, d = new()
    title(d, "渦励振(カルマン渦): 後流に上下交互の渦→周期的反力(強制振動)")
    ymid = 210
    # 流入
    for yy in (ymid - 45, ymid, ymid + 45):
        arrow(d, 70, yy, 150, yy, GRAY, 2, 11)
    ctext(d, 105, ymid - 66, "流れ V", FS, GRAY)
    # 円柱
    cx = 220
    d.ellipse((cx - 24, ymid - 24, cx + 24, ymid + 24), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, ymid + 42, "円柱 D", FT, GRAY)
    # 周期的反力(上下)
    arrow(d, cx, ymid - 24, cx, ymid - 64, RED, 3, 11)
    arrow(d, cx, ymid + 24, cx, ymid + 64, RED, 3, 11)
    ctext(d, cx + 54, ymid - 70, "周期的反力", FT, RED, "lm")
    # 上下交互の渦列(互い違い)
    xs = [300, 356, 412, 468, 524]
    for i, xx in enumerate(xs):
        up = (i % 2 == 0)
        yy = ymid - 38 if up else ymid + 38
        vortex(d, xx, yy, 15, ccw=up, col=(BLUE if up else RED))
    box(d, 90, 320, 570, 378, FILL1)
    ctext(d, 330, 349, "渦発生 f=St V/D。 固有振動数 fn=(1/2pi)sqrt(K/M) に近いと共振", FT)
    note(d, "渦励振は強制振動。ギャロッピング(自励)とは機構が異なる")
    save(im, "v1f7KarmanVortex")


# 5. 円柱の付加質量 Mf=pi rho a^2 と流体力
def f_added_mass_cylinder():
    im, d = new()
    title(d, "円柱の付加質量 Mf=pi rho a^2(排除流体質量に等しい)")
    cx, cy = 290, 215
    # 静止流体(点)
    for gx in range(110, 480, 30):
        for gy in range(120, 320, 30):
            if (gx - cx) ** 2 + (gy - cy) ** 2 > 58 ** 2:
                d.ellipse((gx - 1, gy - 1, gx + 1, gy + 1), fill=LGRAY)
    ctext(d, 150, 140, "静止流体 rho(完全流体)", FT, GRAY)
    # 円柱(半径a)
    d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), outline=BLACK, width=3, fill=FILL2)
    arrow(d, cx, cy, cx + 46, cy - 10, GRAY, 2, 9); ctext(d, cx + 22, cy - 24, "a", FT, GRAY)
    # 軸直角方向の運動
    arrow(d, cx - 46, cy, cx - 120, cy, RED, 4, 14); ctext(d, cx - 126, cy - 18, "運動(軸直角)", FT, RED, "rm")
    # 引きずられる周囲流体
    for a in (35, 145, 215, 325):
        ar = math.radians(a)
        sx, sy = cx + 62 * math.cos(ar), cy - 62 * math.sin(ar)
        arrow(d, sx, sy, sx - 32, sy, BLUE, 2, 9)
    ctext(d, cx + 96, cy + 74, "周囲流体を引きずる", FT, BLUE)
    box(d, 90, 338, 570, 392, FILL1)
    ctext(d, 330, 365, "流体力 = Mf x'' , Mf=pi rho a^2(単位長さ)= 排除流体質量", FT)
    save(im, "v1f7AddedMassCylinder")


if __name__ == "__main__":
    f_two_dof_aero(); f_sloshing(); f_galloping()
    f_karman_vortex(); f_added_mass_cylinder()
    print("done v1f7 formula (5)")
