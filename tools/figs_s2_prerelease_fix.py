# -*- coding: utf-8 -*-
"""固体2級 公開前レビュー修正の図（回答後）を正しい内容で再生成。
- femAssembly (4-26): 4節点・3要素、節点3の対角 K33=k2+k3=350 を強調（旧図は3節点2要素K22で別問題）
- femTrussDof (4-28): 5節点・ピン1+ローラー2、自由度 10-4=6（旧図は4節点・ローラー1で5になっていた）
- num6BackSub (6-3c): 上三角系 x1+2x2-x3=-3, 3x2+x3=0, 2x3=6 → (2,-1,3)（旧図は別の式(2,3,2)）
- num6GaussSteps (6-3): 例示の連立式を 6-3c と同じ正しい系にそろえる（旧図は誤った式）
生成元スクリプトが消失していたため新規作成。"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

# ============================================================ 4-26 femAssembly
im, d = new()
title(d, "4節点・3要素の組立て：節点3の対角成分 K₃₃")
# 直線に並ぶ4節点とばね要素A,B,C
nx = [110, 250, 390, 530]; ny = 96
cols = [BLUE, GREEN, ORANGE]; names = ["A (k₁=150)", "B (k₂=250)", "C (k₃=100)"]
for i in range(3):
    d.line((nx[i], ny, nx[i+1], ny), fill=cols[i], width=6)
    ctext(d, (nx[i]+nx[i+1])//2, ny+22, names[i], FT, cols[i])
for i, x in enumerate(nx):
    node(d, x, ny, 8)
    ctext(d, x, ny-24, str(i+1), F, BLACK)
# 全体剛性マトリックス(4x4)。(3,3)=k2+k3 を強調
vals = [["k₁", "−k₁", "0", "0"],
        ["−k₁", "k₁+k₂", "−k₂", "0"],
        ["0", "−k₂", "k₂+k₃", "−k₃"],
        ["0", "0", "−k₃", "k₃"]]
cell = 52; mx = (W - 4*cell)//2; my = 142
matrix_grid(d, mx, my, vals, cell=cell, highlight=(2, 2), fnt=FT)
# 強調セルへ引き出し
cx = mx + 2*cell + cell//2; cy = my + 2*cell + cell//2
ctext(d, cx, my + 4*cell + 18, "K₃₃ = k₂+k₃ = 250+100 = 350 N/mm", FS, RED)
note(d, "節点3につながるのは要素B・Cの2本だけ。要素A(1-2)は節点3に無関係で足さない。", 404)
save(im, "femAssembly")

# ============================================================ 4-28 femTrussDof
im, d = new()
title(d, "5節点2Dトラス：ピン支持1＋ローラー支持2")
# 節点座標（下弦1,2,3 / 上弦4,5）
P = {1: (150, 300), 2: (340, 300), 3: (530, 300), 4: (245, 175), 5: (435, 175)}
members = [(1, 2), (2, 3), (4, 5), (1, 4), (4, 2), (2, 5), (5, 3)]
for a, b in members:
    d.line((P[a][0], P[a][1], P[b][0], P[b][1]), fill=BLACK, width=5)
for i, (x, y) in P.items():
    node(d, x, y, 8)
    ly = y - 22 if i in (4, 5) else y - 22
    ctext(d, x, ly, str(i), F, BLACK)
# 支持：1=ピン(2拘束)、2・3=ローラー(各1拘束)
pin_support(d, P[1][0], P[1][1] + 8, 22)
roller_support(d, P[2][0], P[2][1] + 8, 22)
roller_support(d, P[3][0], P[3][1] + 8, 22)
ctext(d, P[1][0], P[1][1] + 66, "ピン(2拘束)", FT, GRAY)
ctext(d, P[2][0], P[2][1] + 66, "ローラー(1拘束)", FT, GRAY)
ctext(d, P[3][0], P[3][1] + 66, "ローラー(1拘束)", FT, GRAY)
note(d, "自由度 = 5節点×2 − 拘束(2+1+1) = 10 − 4 = 6")
save(im, "femTrussDof")

# ============================================================ 6-3c num6BackSub
im, d = new()
title(d, "後退代入（下から上へ）")
eqs = ["x₁ + 2x₂ − x₃ = −3", "3x₂ + x₃ = 0", "2x₃ = 6"]
res = ["x₁ = 2", "x₂ = −1", "x₃ = 3"]
bx0, bx1 = 90, 400; bh = 58
ys = [110, 210, 300]
for i, y in enumerate(ys):
    d.rectangle((bx0, y - bh//2, bx1, y + bh//2), outline=BLACK, width=2, fill=FILL1)
    ctext(d, (bx0+bx1)//2, y, eqs[i], F, BLACK)
    ctext(d, 470, y, "→ " + res[i], F, RED, "lm")
# 上向き矢印（下→上へ代入）
arrow(d, 430, 330, 430, 92, RED, 3, 13)
ctext(d, 405, 220, "順に代入", FT, RED)
note(d, "最下段 2x₃=6 → x₃=3。上へ代入して x₂=−1、x₁=−3−2(−1)+3=2。")
save(im, "num6BackSub")

# ============================================================ 6-3 num6GaussSteps
im, d = new()
title(d, "ガウス消去法：前進消去 と 後退代入")
# 満杯の3x3 → 上三角
g1 = [["∗", "∗", "∗"], ["∗", "∗", "∗"], ["∗", "∗", "∗"]]
g2 = [["∗", "∗", "∗"], ["0", "∗", "∗"], ["0", "0", "∗"]]
matrix_grid(d, 70, 95, g1, cell=46, fnt=FS)
matrix_grid(d, 430, 95, g2, cell=46, fnt=FS)
arrow(d, 220, 165, 415, 165, BLUE, 3, 13)
ctext(d, 318, 148, "前進消去", FS, BLUE)
ctext(d, 318, 182, "上三角化", FT, GRAY)
ctext(d, 116, 258, "満杯の係数行列", FT, GRAY)
ctext(d, 476, 258, "下三角側が 0", FT, GRAY)
# 後退代入する上三角系（6-3c と同じ正しい式）
eqs = ["x₁ + 2x₂ − x₃ = −3", "3x₂ + x₃ = 0", "2x₃ = 6"]
for i, y in enumerate([300, 335, 370]):
    ctext(d, 400, y, eqs[i], FS, BLACK)
arrow(d, 250, 375, 250, 292, RED, 3, 12)
ctext(d, 210, 335, "後退代入", FS, RED)
ctext(d, 232, 360, "下→上", FT, GRAY)
note(d, "前進消去＝上三角化 / 後退代入＝最下段から上へ解く")
save(im, "num6GaussSteps")

# ============================================================ 7-16 elem7ElemBendRank
im, d = new()
title(d, "要素種類と曲げ変形の表現力（変位比）")
cx = [150, 340, 530]; base = 250
labels = ["三角形(定ひずみ)", "4節点四辺形", "8節点四辺形"]
ratios = ["比 = 0.25", "比 = 0.60", "比 = 1.00"]
# 三角形
d.polygon([(cx[0], base-70), (cx[0]-55, base), (cx[0]+55, base)], outline=BLACK, width=3, fill=FILL1)
for p in [(cx[0], base-70), (cx[0]-55, base), (cx[0]+55, base)]:
    node(d, p[0], p[1], 6)
# 4節点四辺形
d.rectangle((cx[1]-50, base-62, cx[1]+50, base), outline=BLACK, width=3, fill=FILL1)
for p in [(cx[1]-50, base-62), (cx[1]+50, base-62), (cx[1]-50, base), (cx[1]+50, base)]:
    node(d, p[0], p[1], 6)
# 8節点四辺形（中間節点=赤）
d.rectangle((cx[2]-50, base-62, cx[2]+50, base), outline=BLACK, width=3, fill=FILL1)
for p in [(cx[2]-50, base-62), (cx[2]+50, base-62), (cx[2]-50, base), (cx[2]+50, base)]:
    node(d, p[0], p[1], 6)
for p in [(cx[2], base-62), (cx[2], base), (cx[2]-50, base-31), (cx[2]+50, base-31)]:
    d.ellipse((p[0]-5, p[1]-5, p[0]+5, p[1]+5), fill=RED)
for i in range(3):
    ctext(d, cx[i], base+20, labels[i], FS, BLUE)
    ctext(d, cx[i], base+44, ratios[i], F, BLACK)
# 剛い→正確 の矢印
arrow(d, 90, base+80, 590, base+80, BLACK, 2, 11)
ctext(d, 150, base+98, "剛い(たわみ小)", FT, GRAY)
ctext(d, 530, base+98, "正確(たわみ大, 比→1)", FT, GRAY)
note(d, "剛い順=三角形>4節点>8節点。比=計算たわみ/理論たわみ(計算=理論×比、0.25→0.80×0.25=0.20mm)。")
save(im, "elem7ElemBendRank")

# 5-11 の図(f5Pressure2Nodal/f5PressureSetup)は tools/figs_s2_5_11.py へ移設。
# 公式問5-11は「均等分布力(圧力)の与え方」の概念問題のため、一様圧力版に作り直した。
# (旧=線形分布(台形)荷重の等価節点力計算という主眼ずれの図。2026-09-30 差し替え)

# ============================================================ 6-6e num6SOR
im, d = new()
title(d, "SOR法：緩和係数 ω と収束")
ox, oy = 90, 330
arrow(d, ox, oy, ox, 90, BLACK, 2, 11); ctext(d, ox-8, 82, "反復回数", FS, BLACK, "mm")
arrow(d, ox, oy, 590, oy, BLACK, 2, 11); ctext(d, 600, oy, "ω", FS, BLACK, "lm")
def Xw(w): return ox + w*(560-ox)/2.0
pts = [(Xw(0.1), 110), (Xw(1.0), 235), (Xw(1.5), 300), (Xw(1.85), 250), (Xw(2.0), 110)]
plot(d, 0, 0, pts, col=(30, 60, 170), wd=4)
# 目盛
for w, lab in [(1.0, "1"), (2.0, "2")]:
    d.line((Xw(w), oy-4, Xw(w), oy+4), fill=BLACK, width=2)
    ctext(d, Xw(w), oy+18, lab, FS, BLACK)
# GS と ω_opt の破線
for i in range(oy, 235, -8): d.line((Xw(1.0), i, Xw(1.0), i-4), fill=GRAY, width=2)
for i in range(oy, 300, -8): d.line((Xw(1.5), i, Xw(1.5), i-4), fill=RED, width=2)
ctext(d, Xw(1.0), 220, "GS", FT, GRAY)
ctext(d, Xw(1.5), 320, "ω_opt", FT, RED)
ctext(d, Xw(1.62), 300, "最小", FT, RED, "lm")
ctext(d, Xw(1.9), 118, "発散", FS, RED, "mm")
note(d, "0<ω<2 は収束に必要(対称正定値行列などで十分)。ω=1でGS、過緩和(1<ω<2)で加速。")
save(im, "num6SOR")
