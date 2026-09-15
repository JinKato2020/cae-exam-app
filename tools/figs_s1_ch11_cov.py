# -*- coding: utf-8 -*-
"""固体力学1級 第11章「各種モデリング技術」1:1補完問題の図(接頭辞 s1e11)。
figs_s1_ch11.py と同じ体裁(白地660x420・黒線画)。JSON本体は編集しない。"""
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
# 補11(1)-5 s1e11Sequential : 逐次互い違い法のデータフロー
# ============================================================
def sequential():
    im, d = new(); title(d, "逐次互い違い法(直列に最新値を渡す)")
    def box(cx, cy, w, h, s, fill=FILL1, col=BLACK):
        d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=col, width=3, fill=fill)
        ctext(d, cx, cy, s, FS)
    # 既知量
    box(120, 150, 150, 46, "x_n , y_n(既知)")
    # 予測
    box(120, 250, 150, 46, "y_{n+1} を予測", fill=FILL2)
    # X を先に解く
    box(360, 250, 150, 56, "式Xを解く\n→ x_{n+1}")
    # Y を最新 x で解く
    box(560, 250, 150, 56, "式Yを解く\n→ y_{n+1}", fill=FILL2)
    arrow(d, 120, 173, 120, 226, BLACK, 3, 12)
    arrow(d, 195, 250, 284, 250, BLACK, 3, 13)
    arrow(d, 435, 250, 484, 250, BLACK, 3, 13)
    ctext(d, 360, 300, "最新 x_{n+1} を使用", FT, RED)
    note(d, "予測→一方を解く→最新値で他方を解く。直列だが並列型より収束が速い")
    save(im, "s1e11Sequential")


# ============================================================
# 補11(4)-3 s1e11Reciprocity : 直交異方性ラミナと相反則
# ============================================================
def reciprocity():
    im, d = new(); title(d, "直交異方性ラミナと相反則  ν12/E1=ν21/E2")
    x0, y0, x1, y1 = 130, 130, 470, 300
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    # 繊維方向(軸1, 高剛性)を水平線で
    for i in range(1, 8):
        yy = y0 + (y1 - y0) * i / 8
        d.line((x0 + 6, yy, x1 - 6, yy), fill=GRAY, width=2)
    # 軸1(E1 大)・軸2(E2 小)
    arrow(d, x1 + 10, (y0 + y1) / 2, x1 + 90, (y0 + y1) / 2, BLUE, 3, 12)
    ctext(d, x1 + 96, (y0 + y1) / 2, "軸1  E1(大)", FT, BLUE, "lm")
    arrow(d, (x0 + x1) / 2, y0 - 10, (x0 + x1) / 2, y0 - 80, GREEN, 3, 12)
    ctext(d, (x0 + x1) / 2, y0 - 92, "軸2  E2(小)", FT, GREEN)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2, "繊維方向=軸1", FS)
    ctext(d, W / 2, 350, "相反則: ν21 = ν12·E2/E1  (E2<E1 なので ν21<ν12)", FS, RED)
    note(d, "従ポアソン比は相反則で決まる。Q11=E1/(1-ν12ν21)")
    save(im, "s1e11Reciprocity")


# ============================================================
# 補11(4)-5 s1e11LoadVsDisp : 荷重/変位で比較量が変わる
# ============================================================
def load_vs_disp():
    im, d = new(); title(d, "強制変位なら応力・分布荷重なら変位で比較")
    d.line((330, 60, 330, 400), fill=LGRAY, width=1)
    # 左: 強制変位
    ctext(d, 165, 92, "等しい強制変位を与える", FS, BLUE)
    rows_l = ["両材料で変位=同じ", "↓", "ひずみも(ほぼ)同じ", "↓", "応力・反力で比較する"]
    for i, s in enumerate(rows_l):
        ctext(d, 165, 140 + i * 42, s, FS)
    ctext(d, 165, 358, "σ=E·ε → 異方性材は応力が高い", FT, GRAY)
    # 右: 分布荷重
    ctext(d, 495, 92, "等しい分布荷重を与える", FS, GREEN)
    rows_r = ["両材料で荷重=同じ", "↓", "変位に差が出る", "↓", "変位・ひずみで比較する"]
    for i, s in enumerate(rows_r):
        ctext(d, 495, 140 + i * 42, s, FS)
    ctext(d, 495, 358, "剛い材ほど変位が小さい", FT, GRAY)
    save(im, "s1e11LoadVsDisp")


if __name__ == "__main__":
    sequential()
    reciprocity()
    load_vs_disp()
    print("done ch11 cov")
