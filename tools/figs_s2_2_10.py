# -*- coding: utf-8 -*-
"""固体力学2級 第2章 問2-10 用の図を公式(楔形平板)に合わせて再作成。
公式問2-10 = 中央幅a→両端幅b の対称な楔形"平板"(厚t一定)を軸方向引張。
幅が線形→断面積が線形→伸びに対数 ln(a/b) が出るのが主眼。
- s2TaperBarSetup : 回答前(形状・寸法のみ、答えなし)
- taperbar        : 回答後(A(x)と δ=2PL/(Et(a-b))ln(a/b))
白地660x420。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def wedge_plate(d, cx=330, cy=212, halfL=190, ha=58, hb=24, fill=FILL1):
    """対称な楔形平板を描く。中央半幅ha(幅a)・端半幅hb(幅b)。"""
    xL, xR = cx - halfL, cx + halfL
    pts = [(xL, cy - hb), (cx, cy - ha), (xR, cy - hb),
           (xR, cy + hb), (cx, cy + ha), (xL, cy + hb)]
    d.polygon(pts, outline=BLACK, fill=fill)
    # ポリゴンの outline は細いので主要辺を太線で上書き
    for a, b in [(0, 1), (1, 2), (3, 4), (4, 5)]:
        d.line((pts[a][0], pts[a][1], pts[b][0], pts[b][1]), fill=BLACK, width=3)
    d.line((xL, cy - hb, xL, cy + hb), fill=BLACK, width=3)
    d.line((xR, cy - hb, xR, cy + hb), fill=BLACK, width=3)
    return xL, xR, cx, cy, ha, hb


# ===== 回答前: 形状・寸法のみ =====
im, d = new()
title(d, "楔形平板（厚さ t 一定・軸方向引張）")
xL, xR, cx, cy, ha, hb = wedge_plate(d)
force(d, xL, cy, -46, 0, "P", RED)
force(d, xR, cy, 46, 0, "P", RED)
# 中心線
d.line((cx, cy - ha - 10, cx, cy + ha + 10), fill=LGRAY, width=1)
# 寸法
dim(d, cx - 16, cy - ha, cx - 16, cy + ha, "a (中央幅)")
dim(d, xR + 20, cy - hb, xR + 20, cy + hb, "b (端幅)")
dim(d, xL, cy + ha + 34, cx, cy + ha + 34, "L")
dim(d, cx, cy + ha + 34, xR, cy + ha + 34, "L")
ctext(d, cx, 96, "厚さ t は一定・幅は b→a→b に線形変化", FT, GRAY)
ctext(d, W / 2, 402, "軸方向引張荷重 P による全体の伸び δ を求める。", FT, (70, 70, 70))
save(im, "s2TaperBarSetup")

# ===== 回答後: 断面積の式と結果 =====
im, d = new()
title(d, "楔形平板の伸び（幅が線形 → 対数 ln が出る）")
xL, xR, cx, cy, ha, hb = wedge_plate(d, cy=185, ha=52, hb=22)
force(d, xL, cy, -46, 0, "P", RED)
force(d, xR, cy, 46, 0, "P", RED)
d.line((cx, cy - ha - 8, cx, cy + ha + 8), fill=LGRAY, width=1)
ctext(d, cx, 258, "中央を原点 x、右半分(長さ L)を2倍する", FT, GRAY)
ctext(d, W / 2, 300, "A(x) = { a − (a−b)·x/L } · t   （断面積が x に線形）", FS)
ctext(d, W / 2, 340, "δ = 2·∫(x:0→L) P/(E·A(x)) dx = 2PL / (E·t·(a−b)) · ln(a/b)", FS, (180, 30, 30))
ctext(d, W / 2, 384, "断面積が幅に比例(線形)するので積分に対数が現れる。", FT, (70, 70, 70))
ctext(d, W / 2, 406, "丸棒(面積∝d²)なら 1/(d₁d₂) となり対数は出ない（別問題）。", FT, GRAY)
save(im, "taperbar")
