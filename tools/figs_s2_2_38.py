# -*- coding: utf-8 -*-
"""固体力学2級 第2章 問2-38 用の図(s2NotchStress)を再作成。
主題=切欠き底の応力こう配(応力の空間変化)と疲労強度の関係。
公式2-38 の正解①(こう配を考慮して評価)に合わせ、Kf式は前面に出さない。
白地660x420。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8):
    L = math.hypot(x2 - x1, y2 - y1)
    n = max(1, int(L / dash))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a, b = i * dash, min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


im, d = new()
title(d, "切欠き底の応力こう配（応力の空間変化）")

# --- 上段: 切欠きをもつ帯板の引張 ---
# 帯板本体(上辺に U 切欠き)
d.line((110, 120, 308, 120), fill=BLACK, width=3)
d.arc((308, 98, 352, 142), 0, 180, fill=BLACK, width=3)   # 上辺中央のU切欠き
d.line((352, 120, 550, 120), fill=BLACK, width=3)
d.line((550, 120, 550, 205), fill=BLACK, width=3)
d.line((550, 205, 110, 205), fill=BLACK, width=3)
d.line((110, 205, 110, 120), fill=BLACK, width=3)

# 引張荷重 P
force(d, 110, 162, -45, 0, "P", RED)
force(d, 550, 162, 45, 0, "P", RED)

# 切欠き底と断面(こう配を見る向き)
ctext(d, 330, 150, "切欠き底", FT, RED)
dashed(d, 330, 144, 330, 205)          # 切欠き底から板内部へ向かう断面
arrow(d, 330, 205, 330, 232, GRAY, 2, 10)
ctext(d, 398, 220, "内部へ(距離 x)", FT, GRAY)

# --- 下段: 断面上の応力分布 σ(x) ---
gx, gy = 160, 372          # 原点
gtop, gright = 250, 578
d.line((gx, gy, gright, gy), fill=BLACK, width=2)   # x軸
d.line((gx, gy, gx, gtop), fill=BLACK, width=2)     # σ軸
ctext(d, gx - 22, gtop - 4, "σ", FS)
ctext(d, 380, 392, "切欠き底からの距離 x →", FT)

y_sn, y_smax = 342, 262     # 公称応力・最大応力(σmax=Kt·σn)の縦位置
x0, x1 = 172, 566
# σ(x)= σn +(σmax-σn)e^{-k x} : 底で最大、内部へ急減 → 急な応力こう配
pts = []
for i in range(101):
    t = i / 100
    px = x0 + t * (x1 - x0)
    py = y_sn + (y_smax - y_sn) * math.exp(-3.6 * t)
    pts.append((px, py))
d.line(pts, fill=ORANGE, width=4)

# 公称応力 σn の水平線
dashed(d, gx, y_sn, gright, y_sn, GRAY, 2, 8)
ctext(d, gright - 6, y_sn + 14, "σn(公称応力)", FT, GRAY, "rm")

# σmax(切欠き底)
d.ellipse((x0 - 4, y_smax - 4, x0 + 4, y_smax + 4), fill=RED)
ctext(d, x0 + 10, y_smax - 6, "σmax = Kt·σn", FS, RED, "lm")

# 急なこう配の注記
arrow(d, 205, 292, 232, 330, BLUE, 2, 10)
ctext(d, 300, 300, "急な応力こう配", FS, BLUE, "lm")

ctext(d, W / 2, 410,
      "こう配が急なほど疲労強度の低下は Kt ほど大きくない → こう配を考慮して評価",
      FT, (70, 70, 70))

save(im, "s2NotchStress")
