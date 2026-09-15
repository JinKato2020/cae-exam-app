# -*- coding: utf-8 -*-
"""固体力学1級 第6章「動的解析」1:1補完問題の図(接頭辞 s1e6)。
figs_s1_ch6.py と同じ体裁(白地660x420・黒線画・機構のみ)。JSON本体は編集しない。"""
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
# 補-14 s1e6AutoDt : 応力-ひずみ勾配と応力波速度・自動時間増分
# ============================================================
def auto_dt():
    im, d = new(); title(d, "応力波速度と自動時間増分  v∝√((dσ/dε)/ρ)")
    ox, oy, xl, yl = 110, 350, 460, 250
    axes(d, ox, oy, xl, yl, "ひずみ ε", "応力 σ")

    def P(fx, fy): return (ox + xl * fx, oy - yl * fy)

    # 弾性基準線(勾配E, 破線): 自動設定が仮定する波速の基準
    e = P(0.62, 0.62)
    dashed(d, ox, oy, e[0], e[1], GRAY, 2, 9, 6)
    ctext(d, e[0] + 8, e[1] - 4, "勾配E(基準)", FT, GRAY, "lm")
    # 金属: 降伏後に勾配低下(塑性波速度 < 弾性波速度 → 基準は安全側)
    metal = [P(0, 0), P(0.34, 0.48), P(0.9, 0.60)]
    plot(d, 0, 0, metal, BLUE, 3)
    ctext(d, P(0.9, 0.60)[0], P(0.9, 0.60)[1] + 16, "金属:勾配↓", FT, BLUE, "rm")
    # 非金属: 勾配がEを超えて増大 → 実波速 > 基準 → 要修正
    nonm = [P(0, 0), P(0.40, 0.22), P(0.66, 0.86)]
    plot(d, 0, 0, nonm, RED, 3)
    ctext(d, P(0.66, 0.86)[0] + 8, P(0.66, 0.86)[1], "非金属:勾配↑>E", FT, RED, "lm")
    note(d, "非金属で勾配がEを超えると実波速>基準→自動時間増分の修正が要る")
    save(im, "s1e6AutoDt")


# ============================================================
# 補-16 s1e6DynRelax : 動的緩和法(減衰させ静的釣り合いへ)
# ============================================================
def dyn_relax():
    im, d = new(); title(d, "動的緩和法: 振動を減衰させ静的釣り合いへ")
    ox, oy, xl, yl = 100, 250, 470, 150
    # 軸(中央に平衡線)
    arrow(d, ox, oy, ox + xl + 12, oy, BLACK, 2, 11); ctext(d, ox + xl + 20, oy, "時間", FS, BLACK, "lm")
    arrow(d, ox, oy + 120, ox, oy - 130, BLACK, 2, 11); ctext(d, ox - 12, oy - 134, "変位", FS, BLACK, "rm")
    # 静的釣り合い線
    yeq = oy - 60
    dashed(d, ox, yeq, ox + xl, yeq, GREEN, 2, 10, 6)
    ctext(d, ox + xl, yeq - 12, "静的釣り合い", FT, GREEN, "rm")
    # 減衰振動(平衡値へ収束)
    pts = []
    for i in range(241):
        t = i / 240
        xx = ox + xl * t
        yy = yeq - (oy - yeq) * math.exp(-3.0 * t) * math.cos(2 * math.pi * 3.2 * t)
        pts.append((xx, yy))
    plot(d, 0, 0, pts, RED, 3)
    note(d, "全節点の速度・加速度を減衰。マススケーリング=密度↑で波速↓・Δt↑")
    save(im, "s1e6DynRelax")


if __name__ == "__main__":
    auto_dt()
    dyn_relax()
    print("done ch6 cov")
