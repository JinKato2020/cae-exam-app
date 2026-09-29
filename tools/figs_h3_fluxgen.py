# -*- coding: utf-8 -*-
"""固体2級 3-8 の温度分布図 h3FluxGen を再生成。
定常・一様発熱 + 高温側から熱流束流入。k T'' + q̇ = 0（T''=一定<0 → 上に凸）。
高温面(x=0)の境界: -k T'(0)=q>0 → T'(0)=-q/k<0（初期こう配は0でなく右下がり）。
旧図は高温側で水平（初期こう配ゼロ）に見え、レビュー指摘の通り誤り。ここで初期こう配を負に修正。
T(x)=T_hot - a x - b x^2（a,b>0）, 冷却側ほどこう配が急。"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

im, d = new()
title(d, "定常壁：熱流束流入＋内部発熱の温度分布")

# --- T-x プロット領域 ---
OX, OYb = 108, 300            # 原点(左下)。x軸=OYb, T軸=OX
XL, XR = 128, 566             # 壁内 x=0..L の描画範囲
YHOT, YCOLD = 96, 250         # 高温面・冷却面の温度に対応するy
# 軸
arrow(d, OX, OYb, OX, 82, BLACK, 2, 11); ctext(d, OX-8, 74, "温度 T", FS, BLACK, "mm")
arrow(d, OX, OYb, 596, OYb, BLACK, 2, 11); ctext(d, 604, OYb, "x", FS, BLACK, "lm")

# T(t)=T_hot - a t - b t^2 (t=0..1, a=0.3D, b=0.7D → T(1)=T_cold)
# こう配 f'(0)=0.3(>0, 有限), f'(1)=1.7 → 冷却側で約5.7倍急
def curveY(t): return YHOT + (YCOLD - YHOT) * (0.30*t + 0.70*t*t)
pts = [(XL + (XR-XL)*i/60.0, curveY(i/60.0)) for i in range(61)]
plot(d, 0,0, pts, col=(30,60,170), wd=4)

# 端点(高温・低温)
d.ellipse((XL-6, YHOT-6, XL+6, YHOT+6), fill=BLACK)
d.ellipse((XR-6, YCOLD-6, XR+6, YCOLD+6), fill=BLACK)
ctext(d, XL+6, YHOT-18, "高温", FS, RED, "lm")
ctext(d, XR-4, YCOLD+18, "低温", FS, BLUE, "mm")

# 初期こう配が0でないことを示す接線ガイド（高温面）
tx0, ty0 = XL, YHOT
tx1 = XL+70; ty1 = YHOT + (curveY(70.0/(XR-XL)) - YHOT)  # 接線に近い短い破線
# 破線（初期こう配 dT/dx=-q/k<0）
for i in range(0,70,10):
    a=(XL+i, YHOT + (0.30)*(YCOLD-YHOT)*(i/(XR-XL)))
    b=(XL+i+6, YHOT + (0.30)*(YCOLD-YHOT)*((i+6)/(XR-XL)))
    d.line((a[0],a[1],b[0],b[1]), fill=GRAY, width=2)
ctext(d, XL+80, YHOT+10, "初期こう配 = −q/k ≠ 0", FT, GRAY, "lm")

# 高温側・冷却側ラベル（x軸上）
ctext(d, XL, OYb+18, "高温側", FS, BLACK, "mm")
ctext(d, XR, OYb+18, "冷却側", FS, BLACK, "mm")

# --- 壁（内部発熱）と流入熱流束 ---
wx0, wx1, wy0, wy1 = 108, 566, 330, 388
d.rectangle((wx0, wy0, wx1, wy1), outline=BLACK, width=3, fill=FILL1)
# 内部発熱の＋印
for i in range(6):
    cx = wx0 + 60 + i*72
    ctext(d, cx, (wy0+wy1)//2, "＋", F, RED)
# 流入熱流束の矢印（左＝高温側から）
arrow(d, 66, (wy0+wy1)//2, 104, (wy0+wy1)//2, RED, 5, 15)
ctext(d, 150, wy0+16, "熱流束 q", FS, RED, "lm")
ctext(d, W/2, wy1+14, "内部発熱 H（一様）", FT, RED)

note(d, "上に凸の放物線。高温面でも初期こう配は0でなく、冷却側へ向かうほどこう配が急。", y=H-8)
save(im, "h3FluxGen")
