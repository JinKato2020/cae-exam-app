# -*- coding: utf-8 -*-
"""femSpringSeries.png を問題 fem-4-22 に一致させて再生成。
問題: 節点1(固定)-2-3-4 に3本のばね直列。k1=100/k2=200/k3=400 N/mm、節点4に P=800N。
(旧図は2ばね・節点3個・P=300N で問題と不一致だった)"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

im, d = new()
title(d, "直列ばね:節点1固定・節点4に荷重 P")

y = 235
wall(d, 95, 150, 320, side=1)          # 左の固定壁
xs = [105, 255, 405, 545]              # 節点1,2,3,4 のx座標
ks = ["k1=100 N/mm", "k2=200 N/mm", "k3=400 N/mm"]

for i in range(3):
    spring(d, xs[i] + 8, y, xs[i + 1] - 8, coils=6, amp=14)
    ctext(d, (xs[i] + xs[i + 1]) / 2, y - 40, ks[i], FS)

for i, x in enumerate(xs, start=1):
    node(d, x, y)
    ctext(d, x, y + 26, str(i), FS)

arrow(d, xs[3], y, xs[3] + 62, y, RED, 4, 15)  # 節点4に右向き荷重
ctext(d, xs[3] + 34, y - 22, "P=800N", FS, RED)

save(im, "femSpringSeries")
