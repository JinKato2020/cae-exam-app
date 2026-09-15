# -*- coding: utf-8 -*-
"""固体力学1級 第1章「非線形解析における応力とひずみ」1:1補完問題の図(s1e1*)。
白地660x420・線画・機構のみ。豆腐回避のためギリシャ文字/特殊記号はローマ字表記。
既存 tools/figs_s1_ch1*.py があればそれに準拠、無い分はここで新規描画。"""
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


def square(d, cx, cy, s, col=BLACK, wd=3, fill=None, ang=0.0):
    """中心(cx,cy)・一辺sの正方形をang度回転して描く。"""
    h = s / 2
    pts = [(-h, -h), (h, -h), (h, h), (-h, h)]
    a = math.radians(ang)
    rot = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    d.polygon(rot, outline=col, width=wd, fill=fill)
    return rot


# ============================================================
# 1-2 (公式 問1-2)  s1e1NonlinCause :
#   有限変形で釣合いが変位に非線形になる直接原因の識別。
#   剛体並進(大変位でもひずみ0=原因でない) vs 回転成分/断面変化(=原因)
# ============================================================
def nonlin_cause():
    im, d = new()
    title(d, "有限変形で釣合いが非線形になる要因の識別")
    # --- (a) 剛体並進: 原因でない ---
    cx, cy = 120, 190
    square(d, cx, cy, 60, LGRAY, 2)                 # 変形前(基準)
    dashed(d, cx + 30, cy, cx + 150, cy, GRAY, 2)   # 並進経路
    square(d, cx + 150, cy, 60, GREEN, 3, FILL1)    # 並進後(形は不変)
    arrow(d, cx + 34, cy - 46, cx + 116, cy - 46, GREEN, 2, 10)
    ctext(d, cx + 75, cy - 62, "並進(大)", FT, GREEN)
    ctext(d, cx + 90, cy + 60, "剛体並進", FT, BLACK)
    ctext(d, cx + 90, cy + 82, "ひずみ 0", FT, GREEN)
    ctext(d, cx + 90, cy + 104, "原因でない", FT, RED)
    # --- (b) 剛体回転成分: 原因 ---
    cx, cy = 360, 190
    square(d, cx, cy, 60, LGRAY, 2)
    square(d, cx, cy, 60, BLUE, 3, None, 38)        # 回転後
    angle_arc(d, cx, cy, 46, 0, 38, "R", BLUE)
    ctext(d, cx, cy + 66, "剛体回転成分", FT, BLACK)
    ctext(d, cx, cy + 88, "F=R*U に R を含む", FT, GRAY)
    ctext(d, cx, cy + 110, "非線形の要因", FT, RED)
    # --- (c) 断面変化: 原因 ---
    cx, cy = 560, 190
    d.rectangle((cx - 22, cy - 55, cx + 22, cy + 55), outline=LGRAY, width=2)      # 変形前
    d.polygon([(cx - 12, cy - 70), (cx + 12, cy - 70), (cx + 12, cy + 70), (cx - 12, cy + 70)],
              outline=ORANGE, width=3, fill=FILL1)                                  # 伸長+断面縮小
    force(d, cx, cy - 70, 0, -30, "P", RED)
    force(d, cx, cy + 70, 0, 30, "P", RED)
    ctext(d, cx, cy + 96, "断面変化", FT, BLACK)
    ctext(d, cx, cy + 118, "(変形後で釣合い)", FT, GRAY)
    note(d, "非線形の要因=回転成分・断面変化・非線形ひずみ。剛体並進だけは直接原因でない")
    save(im, "s1e1NonlinCause")


if __name__ == "__main__":
    nonlin_cause()
    print("done ch1 cov")
