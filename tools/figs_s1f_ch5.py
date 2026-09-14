# -*- coding: utf-8 -*-
"""固体力学1級 第5章「破壊力学・疲労解析」の公式・用語図(s1f5*)を描画。
白地660x420・線画・機構のみ・物理的に正確・装飾禁止。ラベルはASCII表記(豆腐回避)。"""
import sys, math, os
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- 共通ヘルパ ----
def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def curvepts(fn, x0, x1, n=80):
    return [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]


# ============================================================
# s1f5Singularity : 1/sqrt(r) の応力特異性(r->0 で発散)
# ============================================================
def singularity():
    im, d = new(); title(d, "き裂先端の 1/sqrt(r) 応力特異性")
    ox, oy = 130, 350
    axes(d, ox, oy, 460, 280, "r (先端からの距離)", "sigma")
    # 主曲線 sigma = KI / sqrt(2 pi r) : A/sqrt(x)
    A = 760.0
    def f(x): return oy - min(260, A / math.sqrt(max(x - ox, 0.5)))
    pts = [(x, f(x)) for x in [ox + i for i in range(4, 452, 3)]]
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 2*KI の薄い曲線(KI は場の強さの倍率)
    def f2(x): return oy - min(268, 1.5 * A / math.sqrt(max(x - ox, 0.5)))
    pts2 = [(x, f2(x)) for x in [ox + i for i in range(9, 452, 3)]]
    d.line(pts2, fill=LGRAY, width=2, joint="curve")
    ctext(d, ox + 150, f2(ox + 150) - 12, "KI が2倍→どこでも2倍", FT, GRAY, "lm")
    # r->0 発散を示す上向き矢印
    arrow(d, ox + 6, oy - 150, ox + 6, oy - 250, RED, 2, 10)
    ctext(d, ox + 12, oy - 235, "r->0 で発散", FT, RED, "lm")
    ctext(d, ox + 250, oy - 150, "sigma = KI / sqrt(2 pi r)", FS, BLUE, "lm")
    ctext(d, ox + 250, oy - 128, "KI = 特異応力場の強さ", FT, GRAY, "lm")
    # 左上に小さなき裂の模式(先端から r を測る)
    cx, cy = ox + 210, 92
    d.line((cx - 60, cy, cx, cy), fill=BLACK, width=4)
    node(d, cx, cy, 4)
    arrow(d, cx, cy, cx + 60, cy + 14, GRAY, 2, 9)
    ctext(d, cx + 66, cy + 16, "r", FT, GRAY, "lm")
    ctext(d, cx - 34, cy - 14, "き裂", FT, GRAY)
    save(im, "s1f5Singularity")


# ============================================================
# s1f5Modes : き裂の3変形モード I(開口)/ II(面内せん断)/ III(面外せん断)
# ============================================================
def modes():
    im, d = new(); title(d, "き裂の3つの変形モード")
    bw, bh = 150, 150
    tops = [("Mode I (開口)", 40), ("Mode II (面内せん断)", 255), ("Mode III (面外せん断)", 470)]
    ytop = 140
    for lab, x0 in tops:
        d.rectangle((x0, ytop, x0 + bw, ytop + bh), outline=BLACK, width=2, fill=FILL1)
        ctext(d, x0 + bw / 2, ytop + bh + 30, lab, FT)
    yc = ytop + bh / 2
    # Mode I: 上に引く / 下に引く(き裂が縦に開く)
    x0 = 40; cx = x0 + bw / 2
    d.line((x0, yc, cx, yc - 8), fill=BLACK, width=3)
    d.line((x0, yc, cx, yc + 8), fill=BLACK, width=3)   # 開いたき裂
    node(d, cx, yc, 3)
    force(d, cx, ytop - 28, 0, 22, "", RED)
    force(d, cx, ytop + bh + 6, 0, -22, "", RED)
    ctext(d, x0 + bw / 2, ytop - 40, "垂直に引離す", FT, RED)
    # Mode II: 面内で前後にずらす(上=右 / 下=左)
    x0 = 255; cx = x0 + bw / 2
    d.line((x0, yc, x0 + bw, yc), fill=BLACK, width=2)
    force(d, x0 + 20, yc - 30, 55, 0, "", RED)          # 上半分 右へ
    force(d, x0 + bw - 20, yc + 30, -55, 0, "", RED)    # 下半分 左へ
    ctext(d, x0 + bw / 2, ytop - 20, "面内で ずらす", FT, RED)
    # Mode III: 面外(z方向)にねじる(上=手前 / 下=奥)= 斜め矢印で表現
    x0 = 470; cx = x0 + bw / 2
    d.line((x0, yc, x0 + bw, yc), fill=BLACK, width=2)
    arrow(d, cx - 10, yc - 12, cx + 42, yc - 40, RED, 3, 12)   # 上半分 面外へ(+z)
    arrow(d, cx + 10, yc + 12, cx - 42, yc + 40, RED, 3, 12)   # 下半分 面外へ(-z)
    ctext(d, x0 + bw / 2, ytop - 20, "面外(z)へずらす", FT, RED)
    ctext(d, W / 2, H - 22, "実際のき裂変形は I・II・III の重ね合わせ", FT, GRAY)
    save(im, "s1f5Modes")


# ============================================================
# s1f5Barsoum : 8節点要素の中間節点を1/4点へ(特異要素)
# ============================================================
def barsoum():
    im, d = new(); title(d, "Barsoum特異要素:中間節点を1/4点へ")
    # 左:通常8節点要素(中間節点=辺の中点)
    ax, ay, s = 70, 150, 170
    def quad(ox, oy, quarter):
        # 四隅
        C = [(ox, oy + s), (ox + s, oy + s), (ox + s, oy), (ox, oy)]  # A(左下=先端),B,C,D
        d.polygon(C, outline=BLACK, width=3)
        for p in C: node(d, p[0], p[1], 5)
        tip = C[0]
        # 4辺の中間節点
        edges = [(C[0], C[1]), (C[1], C[2]), (C[2], C[3]), (C[3], C[0])]
        for (p, q) in edges:
            frac = 0.5
            # 先端(C[0])を含む辺なら quarter 指定で1/4点へ
            if quarter and (p == tip or q == tip):
                # 先端側から 1/4 の位置
                if p == tip:
                    frac_from_tip = 0.25
                    mx = p[0] + (q[0] - p[0]) * frac_from_tip
                    my = p[1] + (q[1] - p[1]) * frac_from_tip
                else:
                    mx = q[0] + (p[0] - q[0]) * 0.25
                    my = q[1] + (p[1] - q[1]) * 0.25
                # 元の中点(点線・白 node)から矢印
                cm = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
                node(d, cm[0], cm[1], 5, fill="white", col=LGRAY)
                arrow(d, cm[0], cm[1], mx, my, RED, 2, 9)
                node(d, mx, my, 6, fill="white", col=RED)
            else:
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                node(d, mx, my, 5)
        return tip
    tip = quad(ax, ay, quarter=True)
    ctext(d, tip[0], tip[1] + 22, "き裂先端", FT, RED)
    ctext(d, ax + s / 2, ay - 18, "8節点 四辺形要素", FT)
    ctext(d, ax + s / 2, ay + s + 40, "先端に接する辺の中間節点\nを 1/4 点へ寄せる", FT, GRAY)
    # 右:先端側の一辺を1点に縮退した三角形(精度向上)
    bx, by = 400, 150
    T = [(bx, by + s / 2), (bx + s, by + s), (bx + s, by)]  # 先端(左)を1点に縮退
    d.polygon(T, outline=BLACK, width=3)
    node(d, T[0][0], T[0][1], 6, fill="white", col=RED)     # 縮退した先端(3節点が重なる)
    node(d, T[1][0], T[1][1], 5); node(d, T[2][0], T[2][1], 5)
    # 先端側2辺の1/4点
    for q in (T[1], T[2]):
        mx = T[0][0] + (q[0] - T[0][0]) * 0.25
        my = T[0][1] + (q[1] - T[0][1]) * 0.25
        node(d, mx, my, 6, fill="white", col=RED)
        # 外側辺の中点
        node(d, (q[0] + T[1][0]) / 2 if q == T[2] else (q[0] + T[2][0]) / 2,
             (q[1] + T[1][1]) / 2 if q == T[2] else (q[1] + T[2][1]) / 2, 5)
    ctext(d, T[0][0] - 6, T[0][1], "先端\n(3節点縮退)", FT, RED, "rm")
    ctext(d, bx + s / 2, by - 18, "縮退三角形(精度向上)", FT)
    ctext(d, bx + s / 2, by + s + 40, "1/sqrt(r) 特異性を1要素で表現", FT, GRAY)
    save(im, "s1f5Barsoum")


# ============================================================
# s1f5Ctod : き裂開口変位COD と き裂先端開口変位CTOD(先端鈍化)
# ============================================================
def ctod():
    im, d = new(); title(d, "き裂開口変位 COD と 先端開口変位 CTOD")
    # 本体
    d.rectangle((90, 90, 600, 360), outline=LGRAY, width=1)
    # き裂:左(表面=口)から右(先端)へ。先端は塑性で鈍化(丸くなる)
    tipx, tipy = 470, 225
    mouth = 90
    # 上面・下面(口で大きく開き、先端で鈍化した丸みへ)
    up = []
    lo = []
    for i in range(0, 101):
        t = i / 100.0
        x = mouth + (tipx - mouth) * t
        gap = 60 * (1 - t) + 10   # 口で広く、先端付近で 10(鈍化して0でない)
        up.append((x, tipy - gap / 2))
        lo.append((x, tipy + gap / 2))
    d.line(up, fill=BLACK, width=4, joint="curve")
    d.line(lo, fill=BLACK, width=4, joint="curve")
    # 先端の丸み(blunting)
    d.arc((tipx - 8, tipy - 10, tipx + 12, tipy + 10), -90, 90, fill=BLACK, width=4)
    ctext(d, tipx + 40, tipy - 40, "先端が丸くなる\n(鈍化 blunting)", FT, GRAY, "lm")
    arrow(d, tipx + 38, tipy - 26, tipx + 10, tipy - 6, GRAY, 2, 9)
    # CTOD(先端の開き量 = delta)
    d.line((tipx + 2, tipy - 9, tipx + 2, tipy + 9), fill=RED, width=1)
    arrow(d, tipx + 2, tipy - 9, tipx + 2, tipy + 9, RED, 2, 8)
    arrow(d, tipx + 2, tipy + 9, tipx + 2, tipy - 9, RED, 2, 8)
    ctext(d, tipx - 22, tipy + 40, "CTOD (delta)\n先端の開き", FT, RED)
    # COD(手前の位置での上下面相対変位)
    px = 250
    gy = 60 * (1 - (px - mouth) / (tipx - mouth)) + 10
    arrow(d, px, tipy - gy / 2, px, tipy + gy / 2, BLUE, 2, 9)
    arrow(d, px, tipy + gy / 2, px, tipy - gy / 2, BLUE, 2, 9)
    ctext(d, px - 10, tipy, "COD", FT, BLUE, "rm")
    ctext(d, px, tipy + gy / 2 + 22, "評価位置での開口量", FT, BLUE)
    ctext(d, mouth + 6, tipy - 55, "き裂口(表面)", FT, GRAY, "lm")
    save(im, "s1f5Ctod")


# ============================================================
# s1f5SN : S-N線図(右下がり→疲労限度で水平)
# ============================================================
def sn():
    im, d = new(); title(d, "S-N線図と疲労限度 sigma_w")
    ox, oy = 120, 340
    axes(d, ox, oy, 470, 270, "N (繰返し数, 対数)", "sigma_a (応力振幅)")
    yw = oy - 90            # 疲労限度の水平レベル
    # 右下がり→水平(疲労限度)
    pts = []
    for i in range(0, 101):
        t = i / 100.0
        x = ox + 30 + 400 * t
        if t < 0.62:
            y = (oy - 235) + (oy - 90 - (oy - 235)) * (t / 0.62)  # 下降
        else:
            y = yw
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 疲労限度の水平線を延長・ラベル
    dashed(d, ox, yw, ox + 30, yw, RED)
    ctext(d, ox - 8, yw, "sigma_w", FS, RED, "rm")
    ctext(d, ox + 430, yw - 16, "疲労限度(水平)= これ以下は破断しない", FT, RED, "rm")
    ctext(d, ox + 120, oy - 210, "応力振幅が大きいほど短寿命", FT, GRAY, "lm")
    save(im, "s1f5SN")


# ============================================================
# s1f5Goodman : 修正グッドマン線図 (0,sigma_w)-(sigma_u,0)
# ============================================================
def goodman():
    im, d = new(); title(d, "修正グッドマン線図(平均応力の影響)")
    ox, oy = 120, 340
    axes(d, ox, oy, 460, 270, "sigma_m (平均応力)", "sigma_a (許容振幅)")
    yw = oy - 200          # (0, sigma_w)
    xu = ox + 380          # (sigma_u, 0)
    # 直線 (0,sigma_w)-(sigma_u,0)
    d.line((ox, yw, xu, oy), fill=BLUE, width=3)
    node(d, ox, yw, 5); node(d, xu, oy, 5)
    ctext(d, ox - 8, yw, "sigma_w", FS, RED, "rm")
    ctext(d, xu, oy + 20, "sigma_u", FS, RED)
    # 例点(sigma_m=100 -> sigma_a 低下)を図示
    mx = ox + 380 * 0.25
    my = yw + (oy - yw) * 0.25
    dashed(d, mx, oy, mx, my, GRAY)
    dashed(d, ox, my, mx, my, GRAY)
    node(d, mx, my, 5, fill="white", col=GREEN)
    ctext(d, mx + 8, my - 12, "許容振幅", FT, GREEN, "lm")
    ctext(d, ox + 175, oy - 155, "sigma_a = sigma_w (1 - sigma_m / sigma_u)", FT, BLUE, "lm")
    ctext(d, ox + 175, oy - 133, "平均応力が大→許容振幅が直線的に減少", FT, GRAY, "lm")
    save(im, "s1f5Goodman")


# ============================================================
# s1f5Paris : パリス則 da/dN-dK 両対数S字(A/B/C 3領域)
# ============================================================
def paris():
    im, d = new(); title(d, "パリス則:da/dN - dK (両対数)")
    ox, oy = 150, 350
    axes(d, ox, oy, 440, 280, "log dK", "log (da/dN)")
    # S字:両端で垂直漸近(下=dKth, 上=KIC), 中央=直線(勾配m)
    thx = ox + 55        # 下限界 dKth の位置
    top = oy - 250
    pts = []
    for i in range(2, 99):
        v = i / 100.0                       # 0(下)..1(上)
        g = 3 * v * v - 2 * v * v * v       # smoothstep: 両端で dx/dv=0(=垂直)
        x = thx + 330 * g
        y = oy - (30 + (250 - 30) * v)
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # dKth 垂直漸近線
    dashed(d, thx, oy, thx, top, RED)
    ctext(d, thx, oy + 18, "dKth", FT, RED)
    ctext(d, thx - 4, top + 8, "下限界", FT, RED, "rm")
    # KIC 側(右上)漸近
    kicx = thx + 330
    dashed(d, kicx, oy, kicx, top, RED)
    ctext(d, kicx, oy + 18, "-> KIC", FT, RED)
    # 領域ラベル A / B / C
    ctext(d, thx + 20, oy - 60, "A", F, GRAY)
    ctext(d, thx + 165, oy - 130, "B", F, GRAY)
    ctext(d, thx + 300, oy - 205, "C", F, GRAY)
    # B領域の勾配 m
    ctext(d, thx + 205, oy - 120, "直線: da/dN = C (dK)^m", FT, BLUE, "lm")
    ctext(d, thx + 205, oy - 100, "勾配 = m", FT, GRAY, "lm")
    save(im, "s1f5Paris")


# ============================================================
# 実行
# ============================================================
if __name__ == "__main__":
    singularity()
    modes()
    barsoum()
    ctod()
    sn()
    goodman()
    paris()
    keys = ["s1f5Singularity", "s1f5Modes", "s1f5Barsoum", "s1f5Ctod",
            "s1f5SN", "s1f5Goodman", "s1f5Paris"]
    miss = [k for k in keys if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(keys), "MISSING", miss)
