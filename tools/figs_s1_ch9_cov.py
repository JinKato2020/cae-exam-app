# -*- coding: utf-8 -*-
"""固体力学1級 第9章「数値解析法」1:1補完問題の図(s1e9*)。
白地660x420・線画・機構のみ。豆腐回避のためギリシャ文字はローマ字表記(lambda 等)。
既存 tools/figs_s1_ch9*.py があれば準拠、無い分をここで新規描画。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


# ============================================================
# 9-3 (公式 問9-3)  s1e9Subspace :
#   サブスペース法= p本のベクトル束[X]を同時に反復し、
#   低次 p 個の固有対 (lambda1..lambdap) へまとめて収束。相似変換は使わない。
# ============================================================
def subspace():
    im, d = new()
    title(d, "サブスペース法: p本のベクトルを同時反復し低次 p 固有対へ")
    # 左: p 列のベクトル束 [X]
    ox, oy, cw, ch, p = 80, 150, 26, 150, 4
    for j in range(p):
        x = ox + j * (cw + 6)
        d.rectangle((x, oy, x + cw, oy + ch), outline=BLACK, width=2, fill=FILL1)
        arrow(d, x + cw / 2, oy + ch + 6, x + cw / 2, oy + ch + 30, GRAY, 2, 8)
    ctext(d, ox + p * (cw + 6) / 2 - 3, oy - 18, "[X] : p 列", FT, BLACK)
    ctext(d, ox + p * (cw + 6) / 2 - 3, oy + ch + 44, "[A]^-1 反復 + 直交化", FT, GRAY)
    # 中央: 変換矢印
    arrow(d, 250, oy + ch / 2, 340, oy + ch / 2, BLACK, 3, 14)
    ctext(d, 295, oy + ch / 2 - 18, "収束", FT, GRAY)
    # 右: 固有値軸に低次 p 個が確定
    ax = 360
    arrow(d, ax, oy + ch, ax + 225, oy + ch, BLACK, 2, 11)
    ctext(d, ax + 205, oy + ch + 22, "lambda", FT, BLACK, "mm")
    labs = [("l1", 30, GREEN), ("l2", 80, GREEN), ("l3", 130, GREEN), ("lp", 175, GREEN),
            ("l(p+1)", 245, GRAY)]
    for name, dx, col in labs:
        x = ax + dx
        d.line((x, oy + ch - 8, x, oy + ch + 8), fill=col, width=3)
        ctext(d, x, oy + ch - 22, name, FT, col)
    dashed(d, ax + 210, oy + 10, ax + 210, oy + ch + 20, LGRAY, 1, 5, 4)
    ctext(d, ax + 105, oy + 4, "求めたい低次 p 個", FT, GREEN)
    ctext(d, ax + 60, oy + 44, "収束率 q=|l1/l(p+1)|", FT, GRAY, "lm")
    ctext(d, ax + 60, oy + 68, "(p 大で分母大 -> 速い)", FT, GRAY, "lm")
    note(d, "近接・重複固有値も可, 疎行列を利用でき大規模向き。相似変換で対角化する方法ではない")
    save(im, "s1e9Subspace")


# ============================================================
# 9-9 (公式 問9-9)  s1e9MethodID :
#   荷重-変位曲線上の反復パターンで手法を判別。
#   (A) ニュートン法=反復ごとに接線更新(傾き変化)
#   (B) 修正ニュートン法=全反復で同じ傾き(平行)・反復多い
# ============================================================
def method_id():
    im, d = new()
    title(d, "反復パターンで判別: 接線更新(A) と 平行(B)")

    def panel(ox, oy, xl, yl, updated, label, col):
        axes(d, ox, oy, xl, yl, "変位 u", "荷重 P")
        # 非線形の平衡曲線(だんだん寝る)
        curve = []
        for i in range(101):
            t = i / 100
            curve.append((ox + t * xl, oy - (1 - math.exp(-2.3 * t)) / (1 - math.exp(-2.3)) * yl))
        plot(d, 0, 0, curve, GRAY, 3)
        Ptar = oy - yl * 0.92
        dashed(d, ox, Ptar, ox + xl, Ptar, LGRAY, 1, 5, 4)
        ctext(d, ox + xl, Ptar - 12, "目標荷重", FT, GRAY, "rm")
        # 反復(階段): updated=True で各段の傾きを変える, False で同一傾き
        xs = [0.0, 0.30, 0.52, 0.68, 0.80, 0.90]
        def Pc(t): return (1 - math.exp(-2.3 * t)) / (1 - math.exp(-2.3))
        k0 = 2.3 / (1 - math.exp(-2.3))          # 初期接線の傾き(正規化)
        for i in range(len(xs) - 1):
            ua, ub = xs[i], xs[i + 1]
            xa, ya = ox + ua * xl, oy - Pc(ua) * yl
            # 予測(接線を目標荷重まで)-> 修正(曲線へ戻る)の折れ線を簡略化
            xb = ox + ub * xl
            yb_curve = oy - Pc(ub) * yl
            arrow(d, xa, ya, xb, yb_curve, col, 2, 8)
            # 接線の傾きを可視化する短い線分
            slope = (2.3 * math.exp(-2.3 * ua) / (1 - math.exp(-2.3))) if updated else k0
            seg = 34
            d.line((xa, ya, xa + seg, ya - slope * seg / xl * yl * 0.10), fill=col, width=2)
        ctext(d, ox + xl / 2, oy + 34, label, FT, col)

    panel(80, 300, 210, 210, True, "(A) ニュートン法: 接線更新", BLUE)
    panel(390, 300, 210, 210, False, "(B) 修正ニュートン法: 平行(反復多)", RED)
    note(d, "各反復で傾きが変わる=ニュートン法, 全反復で同じ傾き(平行)=修正ニュートン法")
    save(im, "s1e9MethodID")


if __name__ == "__main__":
    subspace()
    method_id()
    print("done ch9 cov")
