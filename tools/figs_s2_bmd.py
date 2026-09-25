# -*- coding: utf-8 -*-
"""固体2級 2-21 の曲げモーメント図 s2BMD を「引張側に作図」規約で再生成。
上に凸(負・hogging)の支点C=-12 を軸の上、下に凸(正・sagging)の荷重点=+4 を軸の下に描く。
（従来は正を上・負を下の材料力学規約だったのを上下反転）"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

im, d = new()
title(d, "突出しはりの曲げモーメント図（支点Cで負の最大）")

# x=0..6[m] を pixel 70..590 に写像
def X(xm): return 70 + xm * (590 - 70) / 6.0
BASE = 232                      # 基線(モーメント0)のy
UP12 = BASE - 120              # -12(上に凸=負)を上側へ
DN4  = BASE + 40               # +4(下に凸=正)を下側へ

# 基線
d.line((50, BASE, 612, BASE), fill=BLACK, width=3)

# 折れ線: A(0)=0 -> 荷重点(2)=+4[下] -> 支点C(4)=-12[上] -> 端(6)=0
pA=(X(0),BASE); pL=(X(2),DN4); pC=(X(4),UP12); pE=(X(6),BASE)
plot(d, 0,0, [pA,pL,pC,pE], col=BLUE, wd=4)

# 節点の点
for (px,py) in [pL,pC]:
    d.ellipse((px-6,py-6,px+6,py+6), fill=BLACK)

# 位置ラベル
ctext(d, X(0)-2, BASE+22, "A", F, BLACK, "mm")
ctext(d, X(4), UP12-42, "C", F, BLACK, "mm")
ctext(d, X(6)+8, BASE+22, "端", FS, GRAY, "mm")

# 値ラベル（引張側規約: -12を上・+4を下）
ctext(d, X(2), DN4+24, "+4", F, RED, "mm")
ctext(d, X(4), UP12-16, "−12 (最大)", F, RED, "mm")

note(d, "引張側に作図（上に凸=負を上側へ）。|M|最大は支点C：12 kN·m（負・上に凸）")
save(im, "s2BMD")
