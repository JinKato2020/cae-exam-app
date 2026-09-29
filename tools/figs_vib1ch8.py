# -*- coding: utf-8 -*-
"""振動1級 第8章「数値計算技術」問題図。白地660x420線画。figlib共通。
方針: 正確さ最優先・機構のみ・装飾禁止。数式ラベルはASCII(u1,theta1)で豆腐回避。
※ 本ファイルは 8-21(静たわみモードと拘束/Craig-Bampton) の図の作り直し用に新規作成。
   旧ch8生成元は消失していたため、問題文の内容から再構成した(回答後=helpful図)。"""
import sys, math, os
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def cantilever(d, x0, y0, L, curve, col, tip_fixed=False):
    """左端x0を固定壁(ハッチ)にした片持ちはり。curve(t)=たわみ量(上を正)。"""
    wall(d, x0, y0 - 32, y0 + 32, side=1, n=6)
    pts = [(x0 + t * L, y0 - curve(t)) for t in [i / 60 for i in range(61)]]
    plot(d, 0, 0, pts, col, 3)
    if tip_fixed:
        wall(d, x0 + L, y0 - 32, y0 + 32, side=-1, n=6)


# ================================================ 8-21 静たわみモードと拘束 (helpful)
def f_static_deflection_mode():
    im, d = new(); title(d, "静たわみモード(Tu/Ttheta)と拘束モード(Craig-Bampton)")

    # Panel A: Tu = 単位 u1(先端並進)・theta1固定
    ctext(d, 205, 78, "Tu : theta1固定 で 単位 u1", FT, BLUE)
    cantilever(d, 95, 150, 210,
               lambda t: 42 * (3 * t * t - 2 * t ** 3), BLUE)   # 0->1, 両端傾き0
    node(d, 305, 150 - 42, 5, fill=BLUE); ctext(d, 316, 150 - 42, "u1=1", FT, BLUE, "lm")

    # Panel B: Ttheta = 単位 theta1(先端回転)・u1固定
    ctext(d, 205, 250, "Ttheta : u1固定 で 単位 theta1", FT, GREEN)
    cantilever(d, 95, 330, 210,
               lambda t: 150 * (t ** 3 - t * t), GREEN)          # 先端で0に戻る(回転のみ)
    # 先端の回転を示す短い接線
    d.line((285, 330, 325, 330 - 26), fill=GREEN, width=3)
    ctext(d, 330, 330 - 20, "theta1=1", FT, GREEN, "lm")

    # Panel C(右): Craig-Bampton = u1,theta1 を拘束した弾性振動モード(両端固定)
    ctext(d, 500, 250, "+ Craig-Bampton", FT, RED)
    cantilever(d, 400, 330, 170,
               lambda t: 40 * (1 - math.cos(2 * math.pi * t)) / 2, RED, tip_fixed=True)
    ctext(d, 500, 372, "u1,theta1を拘束した弾性振動モード", FT, RED)

    note(d, "残す先端自由度(u1,theta1)以外を拘束した静たわみ + 拘束(固定界面)固有モード")
    save(im, "v1e8StaticDeflectionMode")


FUNCS = [
    (f_static_deflection_mode, "v1e8StaticDeflectionMode"),
]

if __name__ == "__main__":
    for fn, k in FUNCS:
        try:
            fn()
        except Exception as e:
            print("ERROR", k, repr(e))
    miss = [k for _, k in FUNCS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(FUNCS), "MISSING", miss)
