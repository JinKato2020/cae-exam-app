# -*- coding: utf-8 -*-
"""固体2級 2-21 の曲げモーメント図 s2BMD を「符号つき M 軸（上＝正／下＝負）」で再生成。
計算値の符号どおりに描く: 荷重点 M=+4（正・sagging）は基線の上、支点C M=-12（負・hogging）は基線の下。
縦軸の正負の約束を図中に明示（レビュー指摘: 図の符号と計算が逆／約束を明示せよ への対応）。"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

im, d = new()
title(d, "突出しはりの曲げモーメント図（M図）")
ctext(d, W/2, 58, "縦軸 = 曲げモーメント M [kN·m]（上＝正 sagging ／ 下＝負 hogging）", FS, GRAY)

# x=0..6[m] を pixel に写像
def X(xm): return 70 + xm * (560 - 70) / 6.0
BASE = 208                     # 基線(M=0)のy
SC   = 8.6                     # px / (kN·m)
def Y(m): return BASE - m * SC   # 正は上・負は下

POSF=(226,236,255); NEGF=(255,228,228)   # 正=淡青 / 負=淡赤
# 値の折れ線: A(0)=0 -> 荷重点(2)=+4 -> 支点C(4)=-12 -> 自由端(6)=0
pA=(X(0),Y(0)); pL=(X(2),Y(4)); pC=(X(4),Y(-12)); pE=(X(6),Y(0))
xz=2.5                         # +4→-12 が M=0 を横切る位置

# 領域の塗り（正=上/負=下）
d.polygon([(X(0),BASE),pL,(X(xz),BASE)], fill=POSF)
d.polygon([(X(xz),BASE),pC,(X(6),BASE)], fill=NEGF)

# 符号つき M 軸（0 を基線に、上向き＝正）
arrow(d, 50, BASE, 50, 150, BLACK, 2, 11)
d.line((50, BASE, 50, BASE+96), fill=BLACK, width=2)
ctext(d, 50, 138, "M", F, BLACK)
ctext(d, 62, 160, "＋", FS, BLUE, "lm")
ctext(d, 62, BASE+84, "−", FS, RED, "lm")
ctext(d, 40, BASE, "0", FS, BLACK, "rm")

# 基線
d.line((50, BASE, 604, BASE), fill=BLACK, width=3)

# 折れ線本体
plot(d, 0,0, [pA,pL,pC,pE], col=(30,60,170), wd=4)
for (px,py) in [pL,pC]:
    d.ellipse((px-6,py-6,px+6,py+6), fill=BLACK)

# 位置ラベル
ctext(d, X(0), BASE+22, "A (x=0)", FS, BLACK)
ctext(d, X(2), Y(4)-22, "荷重点 (x=2, 10 kN)", FT, GRAY)
ctext(d, X(4)+92, Y(-12), "支点C (x=4)", FT, GRAY, "lm")
ctext(d, X(6)+6, BASE+20, "自由端 (x=6)", FT, GRAY, "mm")

# 値ラベル（符号つき・計算値と一致）
ctext(d, X(2), Y(4)-44, "M = +4", F, BLUE)
ctext(d, X(4), Y(-12)+30, "M = −12  (|M|最大)", F, RED)

note(d, "|M|最大は支点C：12 kN·m（負＝hogging＝上側引張）。図の上下の符号は計算値どおり。")
save(im, "s2BMD")
