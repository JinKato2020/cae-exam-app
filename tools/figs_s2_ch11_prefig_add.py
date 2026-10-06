# -*- coding: utf-8 -*-
"""固体2級 第11章(結果の検証の基礎)の「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(構造形状/荷重/拘束/対称線)のみ。
答え(変形線図・M図・変位分布・温度分布・反力の合力・外挿値・開/閉断面の剛性比較)は一切描かない(=required相当)。
既存 figureImage は結論・応答曲線を含む(答え示唆)ため回答後(helpful)のまま。JSON配線は別途。
[[cae-figure-before-after-rule]] の第11章展開。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg,
                    x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


# ---- 11-3 内圧円筒の軸対称モデル(内表面応力の外挿・相対誤差を問う) ----
def f_cyl_extrap():
    im, d = new(); title(d, "内圧円筒の軸対称モデル(内表面応力の精度を問う)")
    zx = 170                                            # 回転軸(z)
    dash(d, zx, 90, zx, 360, GRAY); ctext(d, zx, 76, "z(回転軸)", FT, GRAY)
    ri, ro, yt, yb = 250, 430, 100, 300
    d.rectangle((ri, yt, ro, yb), outline=BLACK, width=3, fill=FILL1)
    # 内面に内圧 p(内側→外向き=右向き)
    for k in range(5):
        yy = yt + (yb - yt) * (k + 0.5) / 5
        arrow(d, ri - 34, yy, ri, yy, RED, 3, 11)
    ctext(d, ri - 56, (yt + yb) / 2, "内圧 p", FT, RED, "rm")
    # 内表面からの距離 5mm / 15mm の要素中心(応力値は描かない)
    x5 = ri + 34; x15 = ri + 92
    node(d, x5, (yt + yb) / 2, 6, "white"); node(d, x15, (yt + yb) / 2, 6, "white")
    dim(d, ri, yb + 16, x5, yb + 16, "5mm", 0)
    dim(d, ri, yb + 44, x15, yb + 44, "15mm", 0)
    ctext(d, (ri + ro) / 2 + 20, yt - 16, "r-z断面(軸対称要素)", FT, GRAY)
    ctext(d, x15 + 24, (yt + yb) / 2, "要素中心の応力2点", FT, GRAY, "lm")
    note(d, "内表面から5mm/15mmの応力を外挿し内表面応力を理論値と比較。相対誤差は?(値は未記入)")
    save(im, "ver11CylExtrapSetup")


# ---- 11-4 薄肉開断面をスポット溶接で閉断面化しねじり(検証記述を問う) ----
def f_thin_torsion():
    im, d = new(); title(d, "薄肉開断面をスポット溶接で閉断面化しねじり(検証を問う)")
    # 角形薄肉断面(外形+内形=肉厚)。上辺中央に継ぎ目(開断面)→スポット溶接で閉じる
    ox, oy, w, h, t = 230, 150, 200, 150, 22
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((ox + t, oy + t, ox + w - t, oy + h - t), outline=BLACK, width=3, fill="white")
    # 上辺中央の継ぎ目(隙間)
    gx = ox + w / 2
    d.rectangle((gx - 7, oy, gx + 7, oy + t), outline="white", width=0, fill="white")
    d.line((gx - 7, oy, gx - 7, oy + t), fill=BLACK, width=2)
    d.line((gx + 7, oy, gx + 7, oy + t), fill=BLACK, width=2)
    # スポット溶接(継ぎ目をとめる)
    for yy in (oy + t + 6, oy + t + 30, oy + t + 54):
        node(d, gx, yy, 5, fill=RED, col=RED)
    ctext(d, gx + 70, oy - 6, "継ぎ目=スポット溶接", FT, RED, "lm")
    # ねじり T(断面まわり)
    cx, cy = ox + w / 2, oy + h / 2
    d.arc((cx - 58, cy - 40, cx + 58, cy + 40), 20, 320, fill=BLUE, width=3)
    arrow(d, cx + 54, cy - 18, cx + 58, cy + 2, BLUE, 3, 11)
    ctext(d, cx, cy, "ねじり T", FS, BLUE)
    ctext(d, ox - 12, oy + h / 2, "薄肉断面", FT, GRAY, "rm")
    note(d, "溶接で閉断面化した薄肉はりのねじり。はり理論のねじり剛性と照合する検証は?(答えは未記入)")
    save(im, "ver11ThinTorsionSetup")


# ---- 11-5 単純支持はり・左端から200mmに集中荷重(変形傾向を問う) ----
def f_beam_pos():
    im, d = new(); title(d, "単純支持はり・端から200mmに集中荷重(変形傾向を問う)")
    x0, x1, yb = 110, 560, 220
    Ltot = 1000.0
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    small_pin(d, x0, yb + 3); small_roller(d, x1, yb + 3)
    def PX(mm): return x0 + (x1 - x0) * mm / Ltot
    lx = PX(200)
    force(d, lx, yb - 74, 0, 58, "P", RED)
    dim(d, x0, yb - 92, lx, yb - 92, "200mm", 0)
    dim(d, x0, yb + 52, x1, yb + 52, "L = 1000mm", 0)
    dash(d, PX(500), yb - 36, PX(500), yb + 6, GRAY); ctext(d, PX(500), yb - 50, "中央", FT, GRAY)
    note(d, "左端から200mmに集中荷重P。たわみ曲線の妥当な傾向は?(たわみ線図は未記入)")
    save(im, "ver11BeamPosSetup")


# ---- 11-6 総和が等しい3種の荷重配置(最大変形量の大小を問う) ----
def f_load_arrange():
    im, d = new(); title(d, "総和が等しい3種の荷重配置(最大変形量の大小を問う)")
    def beam(y, lab):
        x0, x1 = 110, 520
        d.line((x0, y, x1, y), fill=BLACK, width=5)
        small_pin(d, x0, y + 3); small_roller(d, x1, y + 3)
        ctext(d, x1 + 36, y, lab, FT, GRAY, "lm")
        return x0, x1
    # (a) 中央1点集中
    x0, x1 = beam(110, "中央集中")
    cx = (x0 + x1) / 2
    arrow(d, cx, 110 - 46, cx, 110 - 6, RED, 4, 13)
    # (b) 等分布
    x0, x1 = beam(215, "等分布")
    for xx in range(int(x0) + 14, int(x1), 40):
        arrow(d, xx, 215 - 34, xx, 215 - 6, BLUE, 2, 9)
    # (c) 複数点分散
    x0, x1 = beam(320, "複数点分散")
    for xx in (x0 + 100, x0 + 205, x0 + 310):
        arrow(d, xx, 320 - 34, xx, 320 - 6, GREEN, 3, 10)
    ctext(d, 310, 360, "荷重の総和は3ケースとも等しい", FT, GRAY)
    note(d, "総和が等しい3配置の最大変形量の大小は?(たわみ線図は未記入)")
    save(im, "ver11LoadArrangeSetup")


# ---- 11-7 単純支持はり・中央集中荷重(応力最大位置を問う) ----
def f_moment_peak():
    im, d = new(); title(d, "単純支持はり・中央集中荷重(応力最大位置を問う)")
    x0, x1, yb = 110, 560, 230
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    small_pin(d, x0, yb + 3); small_roller(d, x1, yb + 3)
    cx = (x0 + x1) / 2
    force(d, cx, yb - 78, 0, 60, "P", RED)
    dim(d, x0, yb + 52, x1, yb + 52, "L", 0)
    note(d, "単純支持はりに集中荷重P。曲げ応力が最大となる位置は?(M図・応力は未記入)")
    save(im, "ver11MomentPeakSetup")


# ---- 11-8 片持ちはり1+剛体要素+はり2を軸方向Pで引く(変形モードを問う) ----
def f_rigid_fbd():
    im, d = new(); title(d, "片持ちはり1+剛体要素+はり2を軸方向Pで引く(変形を問う)")
    wx, yb = 130, 270
    tip = 380; a = 96
    wall(d, wx, yb - 54, yb + 54, side=-1, n=8); ctext(d, wx - 26, yb, "固定", FT, GRAY, "rm")
    bar(d, wx, yb, tip, yb, thick=24, fill=FILL1)
    ctext(d, (wx + tip) / 2, yb + 34, "片持ちはり1", FT, BLACK)
    # 剛体要素(先端から上へ長さ a)
    bar(d, tip, yb, tip, yb - a, thick=14, fill=FILL3)
    node(d, tip, yb, 5); node(d, tip, yb - a, 5)
    dim(d, tip + 40, yb, tip + 40, yb - a, "a", 0)
    ctext(d, tip + 18, yb - a / 2 - 22, "剛体要素", FT, GRAY, "lm")
    # はり2(剛体要素上端から右へ)+ 先端に軸方向引張 P
    bar(d, tip, yb - a, 540, yb - a, thick=24, fill=FILL1)
    ctext(d, (tip + 540) / 2 + 10, yb - a - 22, "はり2", FT, BLACK)
    arrow(d, 540, yb - a, 600, yb - a, RED, 4, 14); ctext(d, 606, yb - a, "P", FS, RED, "lm")
    note(d, "はり2の先端を軸方向Pで引く。系の変形モードとして正しいのは?(変形・M は未記入)")
    save(im, "ver11RigidFBDSetup")


# ---- 11-9 帯板中央に剛体円孔部・一様引張(変位分布を問う) ----
def f_rigid_hole():
    im, d = new(); title(d, "帯板中央に剛体円孔部・一様引張(変位分布を問う)")
    x0, x1, y0, y1 = 150, 540, 160, 258
    cy = (y0 + y1) / 2
    wall(d, x0, y0 - 12, y1 + 12, side=-1); ctext(d, x0 - 16, y1 + 20, "左端固定", FT, GRAY, "rm")
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    cx, r = (x0 + x1) / 2, 38
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL3)
    for k in range(-2, 3):                               # 剛体を示すハッチ
        xx = cx + k * 14
        dd = math.sqrt(max(0, r * r - (k * 14) ** 2))
        d.line((xx, cy - dd, xx, cy + dd), fill=GRAY, width=1)
    ctext(d, cx, y0 - 14, "剛体円孔部", FT, BLACK)
    for yy in (y0 + 22, cy, y1 - 22):                    # 右端 一様引張(右)
        arrow(d, x1, yy, x1 + 42, yy, RED, 3, 12)
    ctext(d, x1 + 48, cy, "一様引張", FT, RED, "lm")
    dash(d, x0, cy, x1, cy, GRAY); ctext(d, (x0 + cx) / 2, cy + 18, "中心線", FT, GRAY)
    note(d, "中心線上の荷重方向変位の分布として正しいのは?(変位線図は未記入)")
    save(im, "ver11RigidHoleStripSetup")


# ---- 11-10 円筒断熱壁(内レンガ+外ブロック)(温度分布を問う) ----
def f_wall_temp():
    im, d = new(); title(d, "円筒断熱壁(内レンガ+外ブロック)(温度分布を問う)")
    ox, yt, yb = 190, 120, 320
    xi, xmid, xo = ox, ox + 150, ox + 290               # 内面, 界面, 外面
    d.rectangle((xi, yt, xmid, yb), outline=BLACK, width=3, fill=(246, 238, 231))
    d.rectangle((xmid, yt, xo, yb), outline=BLACK, width=3, fill=(236, 240, 246))
    ctext(d, (xi + xmid) / 2, (yt + yb) / 2, "レンガ\n(λ大)", FT, ORANGE)
    ctext(d, (xmid + xo) / 2, (yt + yb) / 2, "ブロック\n(λ小)", FT, BLUE)
    dash(d, xmid, yt - 6, xmid, yb + 6, GRAY)
    # 内面:高温ガス・熱伝達大(多くの矢印)
    for yy in (yt + 30, yt + 70, yt + 110, yt + 150):
        arrow(d, xi - 44, yy, xi, yy, RED, 3, 11)
    ctext(d, xi - 50, yt + 10, "高温ガス(h大)", FT, RED, "rm")
    # 外面:空気・熱伝達小(少ない矢印)
    for yy in (yt + 70, yt + 130):
        arrow(d, xo, yy, xo + 44, yy, BLUE, 2, 10)
    ctext(d, xo + 50, yt + 100, "空気(h小)", FT, BLUE, "lm")
    # 半径方向
    arrow(d, xi, yb + 24, xo, yb + 24, BLACK, 2, 10); ctext(d, xo + 8, yb + 24, "r", FT, BLACK, "lm")
    ctext(d, (xi + xo) / 2, yb + 44, "円筒壁の半径方向断面", FT, GRAY)
    note(d, "定常温度分布として妥当なのは?(温度線図は未記入)")
    save(im, "ver11WallTempSetup")


# ---- 11-11 面内荷重・下端拘束の平板(反力の合力を問う) ----
def f_react_sum():
    im, d = new(); title(d, "面内荷重・下端拘束の長方形平板(反力の合力を問う)")
    ox, oy, w, h = 240, 130, 230, 150
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + w / 2, oy + h / 2, "長方形平板", FT, GRAY)
    # 上辺に面内荷重(右向き)
    for xx in (ox + 40, ox + w / 2, ox + w - 40):
        arrow(d, xx, oy - 36, xx, oy - 4, RED, 3, 11)
    ctext(d, ox + w / 2, oy - 52, "面内荷重", FS, RED)
    # 下端 拘束
    hwall(d, ox - 6, ox + w + 6, oy + h, side=1, n=12)
    ctext(d, ox + w / 2, oy + h + 22, "下端 拘束", FT, GRAY)
    note(d, "拘束点に生じる反力の合力について正しいのは?(反力は未記入)")
    save(im, "ver11ReactSumSetup")


# ---- 11-11c 辺に三角形分布線荷重(反力の総和を問う) ----
def f_tri_load():
    im, d = new(); title(d, "辺に三角形分布線荷重(反力の総和を問う)")
    ox, oy, w, h = 160, 240, 340, 90
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + w / 2, oy + h / 2, "板", FT, GRAY)
    # 上辺に三角形分布(左端0 -> 右端 w0)。配分・総和は描かない
    n = 10
    for m in range(n + 1):
        t = m / float(n); xx = ox + w * t; Lh = 6 + 56 * t
        arrow(d, xx, oy - 8 - Lh, xx, oy - 8, GREEN, 2, 9)
    d.line((ox, oy - 14, ox + w, oy - 70), fill=GREEN, width=2)  # 強度の包絡線
    ctext(d, ox - 6, oy - 20, "0", FT, GREEN, "rm")
    ctext(d, ox + w + 10, oy - 70, "w0 = 6 N/mm", FT, GREEN, "lm")
    dim(d, ox, oy + h + 24, ox + w, oy + h + 24, "L = 100mm", 0)
    note(d, "一端0・他端6N/mmの三角形分布線荷重。拘束点の反力の総和は?(合力値は未記入)")
    save(im, "ver11TriLoadSetup")


def main():
    f_cyl_extrap(); f_thin_torsion(); f_beam_pos(); f_load_arrange(); f_moment_peak()
    f_rigid_fbd(); f_rigid_hole(); f_wall_temp(); f_react_sum(); f_tri_load()
    print("done ch11 add 10 figures")


if __name__ == "__main__":
    main()
