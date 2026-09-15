# -*- coding: utf-8 -*-
"""固体1級 第2章 材料非線形 1:1化(欠番補充)の追加図。
接頭辞 s1e2（問題図）。豆腐(□)回避のため図中テキストは meiryo 対応の記号のみ使用。
 - s1e2MohrCoulomb : モール・クーロン限界線 τ=σtanφ+c にモール円が接する（問2-5）
 - s1e2KinematicHyst: 線形移動硬化の反転（|σ-α|=Y・逆降伏が小さい=バウシンガー）（問2-9）
 - s1e2PrandtlPaths : τ-σ の3荷重経路A/B/C（同一終点・軸ひずみ ε_A<ε_B<ε_C）（問2-11）
"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *  # new, save, title, ctext, arrow, axes, plot, note, colors


# =========================================================
# 問2-5  モール・クーロン限界線 + モール円（接する）
# =========================================================
im, d = new()
title(d, "モール・クーロンの降伏条件 (σ–τ平面)")
ox, oy = 120, 320
s = 38.0  # px / 単位（σ,τ 同一スケール＝接点関係を保つ）
def Pmc(sg, ta):
    return (ox + sg * s, oy - ta * s)
axes(d, ox, oy, 470, 250, "σ", "τ")

tanphi, c = 0.5, 0.8
# 限界線 τ = σ tanφ + c
xa, ya = Pmc(0, c)
xb, yb = Pmc(7, 7 * tanphi + c)
d.line((xa, ya, xb, yb), fill=RED, width=3)
ctext(d, xb + 6, yb - 4, "限界線 τ=σ tanφ + c", FT, RED, "lm")

# 粘着力 c（τ切片）
d.line((ox - 5, ya, ox + 5, ya), fill=GRAY, width=2)
ctext(d, ox - 12, ya, "c", FS, GRAY, "rm")

# 内部摩擦角 φ（切片で水平基準線との角）
d.line((xa, ya, xa + 70, ya), fill=LGRAY, width=1)
angle_arc(d, xa, ya, 46, 0, math.degrees(math.atan(tanphi)), "φ", GRAY)

# 接するモール円：中心をσ軸上(σc,0)に置き、半径=中心から限界線までの距離
sc = 3.0
r = (tanphi * sc + c) / math.sqrt(1 + tanphi ** 2)
cx, cy = Pmc(sc, 0)
rp = r * s
d.ellipse((cx - rp, cy - rp, cx + rp, cy + rp), outline=BLUE, width=3)
ctext(d, cx, cy + 16, "モール円", FT, BLUE, "mm")
# 中心・両端（主応力 σ3,σ1）
d.line((cx - rp, cy - 3, cx - rp, cy + 3), fill=BLUE, width=2)
d.line((cx + rp, cy - 3, cx + rp, cy + 3), fill=BLUE, width=2)
ctext(d, cx - rp, cy + 14, "σ3", FT, BLUE, "mm")
ctext(d, cx + rp, cy + 14, "σ1", FT, BLUE, "mm")

note(d, "円が限界線に接すると降伏（垂直応力σに依存＝静水圧を考慮）")
save(im, "s1e2MohrCoulomb")


# =========================================================
# 問2-9  線形移動硬化：反転とバウシンガー効果
# =========================================================
im, d = new()
title(d, "線形移動硬化での反転 (σ–ε)")
ox, oy = 205, 214
sx, sy = 300.0, 0.45
def Pk(e, sg):
    return (ox + e * sx, oy - sg * sy)

# 軸
d.line((150, oy, 560, oy), fill=BLACK, width=2)
arrow(d, 540, oy, 560, oy, BLACK, 2, 11); ctext(d, 568, oy, "ε", FS, BLACK, "lm")
d.line((ox, 372, ox, 62), fill=BLACK, width=2)
arrow(d, ox, 78, ox, 62, BLACK, 2, 11); ctext(d, ox - 12, 56, "σ", FS, BLACK, "rm")

# ±200(初期降伏) の水平ガイド
for sg, lab in [(200, "+200"), (-200, "−200")]:
    y = oy - sg * sy
    for xx in range(210, 520, 14):
        d.line((xx, y, xx + 7, y), fill=LGRAY, width=1)
    ctext(d, ox - 14, y, lab, FT, GRAY, "rm")

p0 = Pk(0, 0); p1 = Pk(0.1, 200); p2 = Pk(1.0, 300)
p3 = Pk(0.8, -100); p4 = Pk(0.6, -150)
plot(d, ox, oy, [p0, p1], BLUE, 4)   # 弾性負荷
plot(d, ox, oy, [p1, p2], RED, 4)    # 引張硬化
plot(d, ox, oy, [p2, p3], BLUE, 4)   # 弾性除荷+反転(傾きは弾性と平行)
plot(d, ox, oy, [p3, p4], RED, 4)    # 圧縮側硬化

for (e, sg, txt, dx, dy, anc) in [
    (0.1, 200, "初期降伏 +200", 10, -14, "lm"),
    (1.0, 300, "引張端 +300", -8, -8, "rm"),
    (0.8, -100, "逆降伏 −100", 12, 12, "lm"),
]:
    x, y = Pk(e, sg)
    d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=BLACK)
    ctext(d, x + dx, y + dy, txt, FT, BLACK, anc)

ctext(d, W / 2, H - 40, "|σ−α|=Y (Y=200) ・ 逆降伏の大きさ 100 < 初期 200", FT, GRAY, "mm")
ctext(d, W / 2, H - 20, "＝バウシンガー効果（大きさ不変・中心が背応力αだけ移動）", FT, GRAY, "mm")
save(im, "s1e2KinematicHyst")


# =========================================================
# 問2-11  τ-σ の3荷重経路 A/B/C（同一終点）
# =========================================================
im, d = new()
title(d, "3荷重経路 A・B・C (τ–σ平面・同一終点)")
ox, oy = 140, 330
sc2 = 52.0
def Pp(sg, ta):
    return (ox + sg * sc2, oy - ta * sc2)
axes(d, ox, oy, 460, 280, "σ", "τ")

SE, TE = 5.0, 4.0  # 終点
E = Pp(SE, TE)

# 経路A(赤): σを先に→τ  ／ 経路C(青): τを先に→σ ／ 経路B(緑): 直線
plot(d, ox, oy, [Pp(0, 0), Pp(SE, 0), E], RED, 4)
plot(d, ox, oy, [Pp(0, 0), Pp(0, TE), E], BLUE, 4)
plot(d, ox, oy, [Pp(0, 0), E], GREEN, 4)

ctext(d, *Pp(2.6, -0.35), "A", FL, RED)
ctext(d, Pp(0, 2.2)[0] - 16, Pp(0, 2.2)[1], "C", FL, BLUE, "rm")
ctext(d, Pp(2.3, 2.1)[0] + 6, Pp(2.3, 2.1)[1] - 14, "B", FL, GREEN)

# 終点
ex, ey = E
d.ellipse((ex - 5, ey - 5, ex + 5, ey + 5), fill=BLACK)
ctext(d, ex + 10, ey - 10, "終点(共通)", FT, BLACK, "lm")

ctext(d, W / 2, H - 40, "弾完全塑性・ミーゼス材料（プラントル・ロイス式）", FT, GRAY, "mm")
ctext(d, W / 2, H - 20, "同一終点でも軸ひずみは経路で異なる： ε_A ＜ ε_B ＜ ε_C", FT, GRAY, "mm")
save(im, "s1e2PrandtlPaths")

print("done ch2 cov figures")
