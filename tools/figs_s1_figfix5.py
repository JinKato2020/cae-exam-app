# -*- coding: utf-8 -*-
"""固体1級 図の作成/差し替え 5枚(2026-10-06)。
白地660x420・黒線画。figlib のスタイルを踏襲。JSON配線は本体が行う(ここでは PNG 生成のみ)。

作る5枚:
- s1e1FiniteStrainEA (1-8 helpful)   : 単軸引張 L→l の有限ひずみ(Green-Lagrange / Almansi)定義図。結果値は描かない。
- s1e3Bifurcation    (3-17 helpful)  : 分岐(座屈)の概念図。分岐点から安定・不安定の枝。
- s1e7HollowCylinderSetup (7-11 pre)  : 中空円筒の過渡熱応力「与件のみ」の中立setup図。結論は一切描かない。
- s1e9CondNumber     (9-3 helpful)   : 固有値の絶対値数直線。cond=|λ|max/|λ|min(値160は描かない)。
- s1e9IllConditioned (9-10 helpful)  : 悪条件の概念図(ほぼ平行な2直線=交点あいまい / 直交=良条件)。

旧キー s1e1TrueNominal / s1e3ImperfectionCurve / s1e9IterMatrix / s1e9Spectral を差し替え。
[[cae-figure-before-after-rule]]。
"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---------------------------------------------------------------- 1-8 (helpful)
def f_finite_strain():
    im, d = new()
    title(d, "単軸引張:変形前 L と変形後 l(有限ひずみの定義)")
    x0 = 150
    # 変形前の棒(L=200mm → 180px)
    yb, Lpx = 140, 180
    bar(d, x0, yb, x0 + Lpx, yb, thick=34)
    node(d, x0, yb, 6); node(d, x0 + Lpx, yb, 6)
    dim(d, x0, yb - 34, x0 + Lpx, yb - 34, "L = 200 mm")
    ctext(d, x0 - 16, yb, "変形前", FT, GRAY, "rm")
    # 変形後の棒(l=250mm → 225px、比0.9で一致)
    ya, lpx = 240, 225
    bar(d, x0, ya, x0 + lpx, ya, thick=34)
    node(d, x0, ya, 6); node(d, x0 + lpx, ya, 6)
    dim(d, x0, ya - 34, x0 + lpx, ya - 34, "l = 250 mm")
    ctext(d, x0 - 16, ya, "変形後", FT, GRAY, "rm")
    force(d, x0 + lpx, ya, 48, 0, "引張", RED)
    # 伸び u = l - L
    d.line((x0 + Lpx, yb + 20, x0 + Lpx, ya + 44), fill=GRAY, width=1)
    dim(d, x0 + Lpx, ya + 44, x0 + lpx, ya + 44, "u = 50 mm", col=RED)
    # 定義式(結果の数値は描かない)
    ctext(d, W / 2, 318, "グリーン・ラグランジュ  E = ½ { (l/L)² − 1 }", FS, BLACK)
    ctext(d, W / 2, 350, "アルマンジ  A = ½ { 1 − (L/l)² }", FS, BLACK)
    note(d, "定義式のみ(結果の数値は示さない)。l/L を使うか L/l を使うかで E と A が区別される")
    save(im, "s1e1FiniteStrainEA")


# ---------------------------------------------------------------- 3-17 (helpful)
def f_bifurcation():
    im, d = new()
    title(d, "分岐(座屈):分岐点から安定・不安定の枝")
    ox, oy, xlen, ylen = 120, 350, 470, 280
    axes(d, ox, oy, xlen, ylen, "変位 w", "荷重 P")
    By = oy - 185
    # 1次(基本)経路=鉛直
    d.line((ox, oy, ox, By), fill=BLUE, width=4)
    ctext(d, ox - 12, (oy + By) / 2, "1次", FT, BLUE, "rm")
    ctext(d, ox - 12, (oy + By) / 2 + 18, "(基本)経路", FT, BLUE, "rm")
    # 基本経路の延長(分岐後は不安定)=薄いグレー
    for yy in range(By, By - 60, -10):
        d.line((ox, yy, ox, yy - 5), fill=LGRAY, width=2)
    ctext(d, ox + 6, By - 52, "延長(不安定)", FT, LGRAY, "lm")
    # 分岐点 B
    node(d, ox, By, 7, "white", BLACK)
    ctext(d, ox + 16, By - 16, "分岐点 B", FS, BLACK, "lm")
    # (a) 安定対称分岐=右上がり(荷重増加)
    ps = []
    for i in range(0, 101):
        t = i / 100.0
        ps.append((ox + 320 * t, By - 108 * (t ** 0.85)))
    plot(d, 0, 0, ps, GREEN, 4)
    ctext(d, ps[-1][0] - 2, ps[-1][1] - 14, "安定対称分岐", FT, GREEN, "rm")
    ctext(d, ps[-1][0] - 2, ps[-1][1] + 2, "(荷重増加)", FT, GREEN, "rm")
    # (b) 不安定対称分岐=右下がり(荷重低下)
    pu = []
    for i in range(0, 101):
        t = i / 100.0
        pu.append((ox + 320 * t, By + 118 * (t ** 0.85)))
    plot(d, 0, 0, pu, RED, 4)
    ctext(d, pu[-1][0] - 2, pu[-1][1] + 14, "不安定対称分岐(荷重低下)", FT, RED, "rm")
    note(d, "分岐点に達しても荷重が最大とは限らない:増加し続ける枝(安定)も低下する枝(不安定)もある")
    save(im, "s1e3Bifurcation")


# ---------------------------------------------------------------- 7-11 (preFigureImage ★答えバレ厳禁)
def f_hollow_setup():
    im, d = new()
    title(d, "中空円筒の過渡熱応力(与件):内外面で熱伝達")
    cx, cy, rb, ra = 285, 218, 126, 60
    d.ellipse((cx - rb, cy - rb, cx + rb, cy + rb), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((cx - ra, cy - ra, cx + ra, cy + ra), outline=BLACK, width=3, fill="white")
    # 内面:内部ガス→壁(熱伝達 h1)=外向き矢印
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        arrow(d, cx + 16 * math.cos(a), cy - 16 * math.sin(a),
              cx + (ra - 5) * math.cos(a), cy - (ra - 5) * math.sin(a), ORANGE, 2, 8)
    ctext(d, cx, cy, "ガス Tg", FT, ORANGE)
    # 外面:壁→外部(熱伝達 h2)=外向き矢印
    for ang in range(0, 360, 45):
        a = math.radians(ang + 22)
        arrow(d, cx + (rb + 4) * math.cos(a), cy - (rb + 4) * math.sin(a),
              cx + (rb + 26) * math.cos(a), cy - (rb + 26) * math.sin(a), BLUE, 2, 8)
    # 半径 a, b
    a1 = math.radians(-35)
    arrow(d, cx, cy, cx + ra * math.cos(a1), cy - ra * math.sin(a1), GRAY, 2, 8)
    ctext(d, cx + (ra + 13) * math.cos(a1), cy - (ra + 13) * math.sin(a1), "a", FT, GRAY)
    a2 = math.radians(58)
    arrow(d, cx, cy, cx + rb * math.cos(a2), cy - rb * math.sin(a2), GRAY, 2, 8)
    ctext(d, cx + (rb * 0.55) * math.cos(a2) + 12, cy - (rb * 0.55) * math.sin(a2), "b", FT, GRAY)
    # 凡例(右側の空きに)
    lx = cx + rb + 14
    ctext(d, lx, cy - 74, "内面:ガス→壁", FT, ORANGE, "lm")
    ctext(d, lx, cy - 52, "熱伝達 h₁", FT, ORANGE, "lm")
    ctext(d, lx, cy + 54, "外面:壁→外部", FT, BLUE, "lm")
    ctext(d, lx, cy + 76, "熱伝達 h₂", FT, BLUE, "lm")
    ctext(d, W / 2, 370, "内部ガス温度 Tg を『急に上昇』『ゆっくり上昇』の2通りで与える", FT, BLACK)
    note(d, "与件(幾何 a,b・境界条件 h₁,h₂・昇温の与え方)のみ。応力分布やピーク位置は示さない")
    save(im, "s1e7HollowCylinderSetup")


# ---------------------------------------------------------------- 9-3 (helpful)
def f_cond_number():
    im, d = new()
    title(d, "条件数:固有値の絶対値で評価  cond(K)=|λ|max / |λ|min")
    ox, xr, y = 115, 560, 230
    lo, hi = -0.48, 2.05

    def px(absval):
        return ox + (math.log10(absval) - lo) / (hi - lo) * (xr - ox)

    arrow(d, ox - 12, y, xr + 22, y, BLACK, 2, 11)
    ctext(d, xr + 30, y, "|λ| (log)", FT, BLACK, "lm")
    data = [("0.5", 0.5, BLUE, "|λ|min"),
            ("4", 4, GRAY, ""),
            ("20", 20, GRAY, ""),
            ("80", 80, RED, "|λ|max")]
    for ab, val, col, tag in data:
        x = px(val)
        d.line((x, y - 10, x, y + 10), fill=col, width=3)
        node(d, x, y, 6, "white", col)
        ctext(d, x, y + 28, "|λ|=" + ab, FT, col)
        if tag:
            d.line((x, y - 28, x, y - 12), fill=col, width=2)
            ctext(d, x, y - 44, tag, FS, col)
    ctext(d, px(80), y + 52, "(−80 → |−80|=80)", FT, RED)
    ctext(d, W / 2, 322, "cond(K) = |λ|max / |λ|min", F)
    note(d, "負の固有値も絶対値で評価(−80→80)。絶対値が最大の80と最小の0.5の比が条件数")
    save(im, "s1e9CondNumber")


# ---------------------------------------------------------------- 9-10 (helpful)
def f_ill_conditioned():
    im, d = new()
    title(d, "悪条件:ほぼ平行な2直線は交点があいまい")
    # 左:悪条件(ほぼ平行・浅い角度で交差)
    ctext(d, 185, 80, "cond 大 = 悪条件", FS, RED)
    Px, Py = 195, 240
    # あいまいな交点領域(淡い楕円を先に描く)
    d.ellipse((Px - 60, Py - 20, Px + 60, Py + 20), fill=(255, 232, 232), outline=None)
    # 2直線(傾き -0.15 と +0.05 = ほぼ平行)
    for m, col in [(-0.15, BLUE), (0.05, GREEN)]:
        xa, xb = 70, 320
        d.line((xa, Py + m * (xa - Px), xb, Py + m * (xb - Px)), fill=col, width=3)
    ctext(d, Px, Py + 42, "交点が不確か", FT, RED)
    ctext(d, 185, 352, "入力の微小変化で解が大きく動く", FT, GRAY)
    # 右:良条件(ほぼ直交・明確に交差)
    ctext(d, 490, 80, "cond ≈ 1 = 良条件", FS, GREEN)
    Qx, Qy = 490, 235
    d.line((Qx - 72, Qy - 72, Qx + 72, Qy + 72), fill=BLUE, width=3)
    d.line((Qx - 72, Qy + 72, Qx + 72, Qy - 72), fill=GREEN, width=3)
    node(d, Qx, Qy, 6, "white", RED)
    ctext(d, Qx, Qy + 96, "交点が明確", FT, GREEN)
    ctext(d, 490, 352, "入力が変わっても解は安定", FT, GRAY)
    note(d, "cond(K)=‖K‖·‖K⁻¹‖ , 実対称なら |λ|max/|λ|min。大=悪条件(誤差に敏感)/ 1付近=良条件")
    save(im, "s1e9IllConditioned")


if __name__ == "__main__":
    f_finite_strain()
    f_bifurcation()
    f_hollow_setup()
    f_cond_number()
    f_ill_conditioned()
    print("=== s1 figfix5 done ===")
