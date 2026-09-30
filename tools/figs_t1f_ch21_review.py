# -*- coding: utf-8 -*-
"""熱流体力学1級 第21章「層流拡散火炎」公開前レビュー用の図(t1e21*)を描画。
白地660x420・黒線画。条件図(Ansなし)には答え・数値・結論を描かない。
Ans図(末尾Ans)には答え・数値を描いてよい。
豆腐回避のためギリシャ文字/添字はプレーン表記へ(Z_st, S_L, T, dT 等)。"""
import sys, math
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


def dashed_circle(d, cx, cy, r, col=GRAY, wd=2, seg=64):
    prev = None
    for i in range(seg + 1):
        a = 2 * math.pi * i / seg
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if prev is not None and i % 2 == 0:
            d.line((prev[0], prev[1], p[0], p[1]), fill=col, width=wd)
        prev = p


def pcircle(d, x, y, r, fill=FILL1, col=BLACK, wd=2):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wd, fill=fill)


def dashed_poly(d, pts, col=GRAY, wd=2, dash=9, gap=6):
    for i in range(len(pts) - 1):
        dashed(d, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, wd, dash, gap)


# ============================================================
# 21-1  t1e21TvsZ  (条件図・上書き)  温度 T - 混合分率 Z の模式
# ============================================================
def t1e21TvsZ():
    im, d = new(); title(d, "拡散火炎の温度分布  T - 混合分率 Z (模式)")
    ox, oy, xl, yl = 120, 350, 460, 255
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "Z", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T", FS, BLACK, "rm")
    low, pk, zst = 0.13, 0.88, 0.05
    def X(z): return ox + z * xl
    def Y(v): return oy - v * yl
    # 両端は同じ低温、Z_st(左寄り)でピークの三角形状(急上昇->緩やかに低下)
    d.line((X(0.0), Y(low), X(zst), Y(pk)), fill=RED, width=3)
    d.line((X(zst), Y(pk), X(1.0), Y(low)), fill=RED, width=3)
    # Z_st の位置線
    dashed(d, X(zst), oy, X(zst), Y(pk), LGRAY, 1, 6, 5)
    ctext(d, X(zst), oy + 16, "Z_st", FT, GRAY)
    # 両端(与件の軸端のみ)
    ctext(d, X(0.0), oy + 16, "0", FT, BLACK)
    ctext(d, X(1.0), oy + 16, "1", FT, BLACK)
    ctext(d, X(0.02), Y(low) - 22, "酸化剤側", FT, GRAY, "lm")
    ctext(d, X(0.80), Y(low) - 22, "燃料側", FT, GRAY, "lm")
    note(d, "両端(酸化剤側Z=0・燃料側Z=1)は同じ温度. Z_stで温度がピークになる(数値は問わない)")
    save(im, "t1e21TvsZ")


# ============================================================
# 21-1 Ans  t1e21TvsZAns  数値入り
# ============================================================
def t1e21TvsZAns():
    im, d = new(); title(d, "拡散火炎の温度分布 T - Z (Ans, 模式・非比例)")
    ox, oy, xl, yl = 120, 350, 460, 255
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "Z", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T [K]", FS, BLACK, "rm")
    low, pk, zst = 0.13, 0.88, 0.05
    def X(z): return ox + z * xl
    def Y(v): return oy - v * yl
    d.line((X(0.0), Y(low), X(zst), Y(pk)), fill=RED, width=3)
    d.line((X(zst), Y(pk), X(1.0), Y(low)), fill=RED, width=3)
    dashed(d, X(zst), oy, X(zst), Y(pk), LGRAY, 1, 6, 5)
    # 両端 300K
    node(d, X(0.0), Y(low), 5, fill=BLUE, col=BLUE)
    node(d, X(1.0), Y(low), 5, fill=BLUE, col=BLUE)
    ctext(d, X(0.03), Y(low) + 18, "T=300K", FT, BLUE, "lm")
    ctext(d, X(0.86), Y(low) + 18, "T=300K", FT, BLUE, "rm")
    # ピーク 2300K
    node(d, X(zst), Y(pk), 5, fill=RED, col=RED)
    ctext(d, X(zst) + 8, Y(pk) - 4, "Z_st=0.05 で最高 T=2300K", FT, RED, "lm")
    # 温度上昇 dT
    dashed(d, X(zst), Y(low), X(zst) + 150, Y(low), LGRAY, 1, 6, 5)
    dim(d, X(zst) + 120, Y(low), X(zst) + 120, Y(pk), "dT=2000K", col=GRAY)
    ctext(d, X(zst), oy + 16, "0.05", FT, GRAY)
    note(d, "両端300K, Z_st=0.05でピーク2300K, 温度上昇 dT=2000K (模式図・非比例)")
    save(im, "t1e21TvsZAns")


# ============================================================
# 21  t1e21CounterflowAns  対向流拡散火炎(火炎面は空気側)
# ============================================================
def t1e21CounterflowAns():
    im, d = new(); title(d, "対向流拡散火炎  火炎面はよどみ面より空気側 (Ans)")
    cx = 330
    ytop, ybot = 92, 332
    ystag = 220          # よどみ面(中央)
    yflame = 184         # 火炎面(よどみ面より上=空気側)
    # ノズル(上=空気, 下=燃料)
    box_w = 120
    d.rectangle((cx - box_w / 2, ytop - 26, cx + box_w / 2, ytop), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((cx - box_w / 2, ybot, cx + box_w / 2, ybot + 26), outline=BLACK, width=3, fill=FILL1)
    ctext(d, cx, ytop - 40, "空気 (Air) ノズル", FT, BLUE)
    ctext(d, cx, ybot + 40, "燃料 (メタン CH4) ノズル", FT, GREEN)
    # 対向流の噴出矢印
    for dxp in (-38, 0, 38):
        arrow(d, cx + dxp, ytop + 2, cx + dxp, ystag - 26, BLUE, 2, 10)
        arrow(d, cx + dxp, ybot - 2, cx + dxp, ystag + 26, GREEN, 2, 10)
    # よどみ面
    dashed(d, cx - 170, ystag, cx + 170, ystag, GRAY, 2, 9, 6)
    ctext(d, cx - 176, ystag, "よどみ面", FT, GRAY, "rm")
    # 火炎面(空気側)
    d.line((cx - 150, yflame, cx + 150, yflame), fill=RED, width=4)
    ctext(d, cx + 156, yflame, "火炎面", FS, RED, "lm")
    ctext(d, cx + 156, yflame + 20, "(空気側)", FT, RED, "lm")
    # 火炎面とよどみ面の隔たり
    dim(d, cx - 150, yflame, cx - 150, ystag, "", col=GRAY)
    note(d, "量論混合分率 Z_st が小さいため, 火炎面はよどみ面より空気(酸化剤)側に立つ")
    save(im, "t1e21CounterflowAns")


# ============================================================
# 21  t1e21SCurveAns  S字曲線(消炎点A/着火点B)
# ============================================================
def t1e21SCurveAns():
    im, d = new(); title(d, "拡散火炎のS字曲線  速度勾配 - 最高温度 (Ans)")
    ox, oy, xl, yl = 120, 355, 470, 265
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "a", FS, BLACK, "lm")
    ctext(d, ox + xl + 4, oy + 16, "速度勾配(伸長率)大->", FT, GRAY, "rm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "最高火炎温度", FS, BLACK, "rm")
    def X(u): return ox + u * xl
    def Y(v): return oy - v * yl
    # 上枝(燃焼枝・安定): 高温側, 右下がりで消炎点Aへ
    upper = [(0.06, 0.92), (0.28, 0.88), (0.50, 0.82), (0.68, 0.74), (0.80, 0.66)]
    d.line([(X(u), Y(v)) for u, v in upper], fill=RED, width=3, joint="curve")
    ctext(d, X(0.20), Y(0.94), "燃焼枝(安定)", FT, RED, "lm")
    # 中間枝(不安定・破線): Aから左下がりで着火点Bへ
    mid = [(0.80, 0.66), (0.55, 0.50), (0.30, 0.34)]
    dashed_poly(d, [(X(u), Y(v)) for u, v in mid], GRAY, 2, 10, 7)
    ctext(d, X(0.56), Y(0.44), "不安定枝(破線)", FT, GRAY, "lm")
    # 下枝(混合枝・安定): Bから右下がりで低温側へ
    lower = [(0.30, 0.34), (0.55, 0.22), (0.80, 0.15), (0.92, 0.13)]
    d.line([(X(u), Y(v)) for u, v in lower], fill=BLUE, width=3, joint="curve")
    ctext(d, X(0.55), Y(0.10), "混合枝(安定)", FT, BLUE, "lm")
    # 折り返し点 A(消炎) / B(着火)
    node(d, X(0.80), Y(0.66), 6, fill=RED, col=RED)
    ctext(d, X(0.80) + 10, Y(0.66) - 4, "A 消炎点", FT, RED, "lm")
    node(d, X(0.30), Y(0.34), 6, fill=BLUE, col=BLUE)
    ctext(d, X(0.30) - 10, Y(0.34) - 4, "B 着火点", FT, BLUE, "rm")
    # 弧長法の折り返し追跡
    arrow(d, X(0.80) + 24, Y(0.66) + 6, X(0.72) + 24, Y(0.58) + 6, GRAY, 2, 9)
    ctext(d, X(0.86), Y(0.48), "弧長法で", FT, GRAY, "lm")
    ctext(d, X(0.86), Y(0.42), "折り返しを追跡", FT, GRAY, "lm")
    note(d, "上枝=燃焼枝(安定), 中間=不安定, 下枝=混合枝(安定). A=消炎点/B=着火点で飛び移る")
    save(im, "t1e21SCurveAns")


# ============================================================
# 21  t1e21CoaxialAns  同軸流拡散火炎 断面A-A' 半径方向分布
# ============================================================
def t1e21CoaxialAns():
    im, d = new(); title(d, "同軸流拡散火炎 断面A-A'  半径方向分布 (Ans)")
    ox, oy, xl, yl = 120, 345, 470, 235
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "r", FS, BLACK, "lm")
    ctext(d, ox + xl + 4, oy + 16, "半径(中心->外周)", FT, GRAY, "rm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "分布", FS, BLACK, "rm")
    def X(u): return ox + u * xl
    def Y(v): return oy - v * yl
    rf = 0.48
    # 火炎面位置
    dashed(d, X(rf), oy, X(rf), Y(1.0), LGRAY, 1, 6, 5)
    ctext(d, X(rf), oy - yl - 2, "火炎面", FT, RED)
    N = 120
    # 温度 T(赤): 火炎面でピーク
    ptsT = []
    for i in range(N + 1):
        u = i / N
        v = 0.10 + 0.85 * math.exp(-((u - rf) / 0.16) ** 2)
        ptsT.append((X(u), Y(v)))
    d.line(ptsT, fill=RED, width=3, joint="curve")
    ctext(d, X(rf), Y(0.99), "T", FS, RED)
    # 生成物 P(橙): 火炎面でピーク・やや幅広
    ptsP = []
    for i in range(N + 1):
        u = i / N
        v = 0.06 + 0.55 * math.exp(-((u - rf) / 0.22) ** 2)
        ptsP.append((X(u), Y(v)))
    d.line(ptsP, fill=ORANGE, width=3, joint="curve")
    ctext(d, X(rf + 0.20), Y(0.42), "P(生成物)", FT, ORANGE, "lm")
    # 燃料 F(青): 中心で高く火炎面で0
    ptsF = []
    for i in range(N + 1):
        u = i / N
        v = 0.72 / (1 + math.exp((u - (rf - 0.06)) / 0.05))
        ptsF.append((X(u), Y(v)))
    d.line(ptsF, fill=BLUE, width=3, joint="curve")
    ctext(d, X(0.06), Y(0.66), "F(燃料)", FT, BLUE, "lm")
    # 酸化剤 O(緑): 火炎面外側で立ち上がる
    ptsO = []
    for i in range(N + 1):
        u = i / N
        v = 0.68 / (1 + math.exp(-(u - (rf + 0.08)) / 0.05))
        ptsO.append((X(u), Y(v)))
    d.line(ptsO, fill=GREEN, width=3, joint="curve")
    ctext(d, X(0.86), Y(0.60), "O(酸化剤)", FT, GREEN, "rm")
    note(d, "T・生成物Pは火炎面でピーク. 燃料Fと酸化剤Oは火炎面を挟んで分離し近傍でともに0")
    save(im, "t1e21CoaxialAns")


# ============================================================
# 21  t1e21LiftedAns  浮き上がり火炎の三又(トリプルフレーム)
# ============================================================
def t1e21LiftedAns():
    im, d = new(); title(d, "浮き上がり火炎の基部  三又(トリプルフレーム)構造 (Ans)")
    # 流れは左から右へ
    ystoic = 232
    # 上流からの流れ
    for yy in (150, 200, 250, 300):
        arrow(d, 60, yy, 120, yy, GRAY, 2, 10)
    ctext(d, 88, 128, "未燃流れ", FT, GRAY)
    # 混合分率の場: 上=希薄(酸化剤側), 下=過濃(燃料側)
    ctext(d, 150, 118, "酸化剤側(希薄 Z<Z_st)", FT, BLUE, "lm")
    ctext(d, 320, 340, "燃料側(過濃 Z>Z_st)", FT, GREEN, "lm")
    # 量論線 Z_st
    dashed(d, 130, ystoic, 600, ystoic, LGRAY, 2, 9, 6)
    ctext(d, 606, ystoic, "Z_st", FT, GRAY, "lm")
    # 三又の交点(トリプル点)
    tx, ty = 300, ystoic
    node(d, tx, ty, 5, fill=BLACK)
    # (a) 外側=希薄予混合火炎(上へ湾曲)
    wa = [(tx, ty), (tx - 40, ty - 30), (tx - 80, ty - 74)]
    d.line(wa, fill=RED, width=3, joint="curve")
    ctext(d, tx - 96, ty - 84, "(a) 希薄予混合火炎", FT, RED, "mm")
    # (b) 内側=過濃予混合火炎(下へ湾曲)
    wb = [(tx, ty), (tx - 40, ty + 30), (tx - 80, ty + 74)]
    d.line(wb, fill=GREEN, width=3, joint="curve")
    ctext(d, tx - 96, ty + 86, "(b) 過濃予混合火炎", FT, GREEN, "mm")
    # (c) 後方=拡散火炎(下流へ)
    d.line((tx, ty, 540, ty), fill=ORANGE, width=4)
    ctext(d, 470, ty - 16, "(c) 拡散火炎", FT, ORANGE, "mm")
    ctext(d, tx + 6, ty + 16, "トリプル点", FT, BLACK, "lm")
    note(d, "基部は3枝: (a)希薄予混合火炎 (b)過濃予混合火炎 (c)後方の拡散火炎")
    save(im, "t1e21LiftedAns")


# ============================================================
if __name__ == "__main__":
    t1e21TvsZ()
    t1e21TvsZAns()
    t1e21CounterflowAns()
    t1e21SCurveAns()
    t1e21CoaxialAns()
    t1e21LiftedAns()
    print("done ch21 review figures")
