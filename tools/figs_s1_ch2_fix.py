# -*- coding: utf-8 -*-
"""固体1級 第2章 問2-6 の図を正しく描き直す。
等方硬化の単軸 σ-ε（引張1.0%/300MPaまで負荷→圧縮反転→逆降伏 -300MPa, ε=0.7%）。
要点の是正:
 - 閉じたヒステリシスループにしない（等方硬化は安定ループを作らない＝バウシンガー無し）。単一反転の開いた経路。
 - 弾性負荷の傾きと弾性除荷の傾きを厳密に平行（同じ E）。
 - 逆降伏の大きさ = 最大応力 300 と対称（-300）。初期降伏 200 とは別。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *  # new, save, plot, arrow, ctext, title, note, colors

im, d = new()
title(d, "等方硬化での反転と再降伏 (σ–ε)")

# 座標系: 原点(ox,oy)、ε右+ / σ上+。 X=ox+ε%*sx, Y=oy-σ*sy
ox, oy = 200, 214
sx = 300.0        # px / %ひずみ
sy = 0.45         # px / MPa
def P(e, s):      # e[%], s[MPa] -> ピクセル
    return (ox + e * sx, oy - s * sy)

# --- 軸（σは上下、εは右）---
d.line((150, oy, 560, oy), fill=BLACK, width=2)      # ε軸(負側も少し)
arrow(d, 540, oy, 560, oy, BLACK, 2, 11)
ctext(d, 568, oy, "ε", FS, BLACK, "lm")
d.line((ox, 372, ox, 62), fill=BLACK, width=2)       # σ軸(上下)
arrow(d, ox, 78, ox, 62, BLACK, 2, 11)
ctext(d, ox - 12, 56, "σ", FS, BLACK, "rm")

# --- 対称の目安（±300 の水平ガイド）---
for s, lab in [(300, "+300"), (-300, "−300")]:
    y = oy - s * sy
    for xx in range(210, 520, 14):
        d.line((xx, y, xx + 7, y), fill=LGRAY, width=1)
    ctext(d, ox - 14, y, lab, FT, GRAY, "rm")

# --- 応力経路 ---
# 1) 弾性負荷 0 -> (0.1%,200)
p0 = P(0, 0); p1 = P(0.1, 200)
plot(d, ox, oy, [p0, p1], BLUE, 4)
# 2) 塑性硬化 (0.1%,200) -> (1.0%,300)
p2 = P(1.0, 300)
plot(d, ox, oy, [p1, p2], RED, 4)
# 3) 弾性除荷+反転 (1.0%,300) -> (0.7%,-300)  ※傾きは1)と平行
p3 = P(0.7, -300)
plot(d, ox, oy, [p2, p3], BLUE, 4)
# 4) 圧縮側の再降伏(硬化) (0.7%,-300) -> (0.5%,-330)
p4 = P(0.5, -330)
plot(d, ox, oy, [p3, p4], RED, 4)

# --- 節点と注記 ---
for (e, s, txt, dx, dy, anc) in [
    (0.1, 200, "初期降伏 200", 10, 16, "lm"),
    (1.0, 300, "引張端 +300 (ε=1.0%)", -8, -6, "rm"),
    (0.7, -300, "逆降伏 −300 (ε=0.7%)", -8, 16, "rm"),
]:
    x, y = P(e, s)
    d.ellipse((x-4, y-4, x+4, y+4), fill=BLACK)
    ctext(d, x + dx, y + dy, txt, FT, BLACK, anc)

# 弾性戻り Δε=0.3%（σ=0 の高さで ε=0.7%↔1.0% を寸法表示）
ya = oy
xa, _ = P(0.7, 0); xb, _ = P(1.0, 0)
d.line((xa, ya - 40, xa, ya + 8), fill=GRAY, width=1)
d.line((xb, ya - 40, xb, ya + 8), fill=GRAY, width=1)
arrow(d, xa, ya - 30, xb, ya - 30, GRAY, 2, 9)
arrow(d, xb, ya - 30, xa, ya - 30, GRAY, 2, 9)
ctext(d, (xa + xb) / 2, ya - 44, "弾性戻り Δε=0.3%", FT, GRAY, "mm")

ctext(d, W/2, H-40, "等方硬化: 逆降伏 −300 は最大応力 +300 と対称の大きさ", FT, GRAY, "mm")
ctext(d, W/2, H-20, "(バウシンガー効果なし・安定な履歴ループにはならない)", FT, GRAY, "mm")

save(im, "s1e2IsoHysteresis")
