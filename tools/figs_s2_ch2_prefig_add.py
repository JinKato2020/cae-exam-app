# -*- coding: utf-8 -*-
"""固体2級 第2章(固体力学の基礎)の「回答前(preFigureImage)」配置図 追加分。
白地660x420・黒線画・与件(配置/寸法/荷重/与えられた応力状態)のみ。
答え(ポアソン比の値・各部名称・主応力の45°方向と大きさ・Z最大の形・最短寿命の履歴など)は
一切描かない(=required相当)。既存 figureImage(答え示唆あり)は回答後(helpful)のまま。
JSON配線は別途。[[cae-figure-before-after-rule]] 厳命D の第2章横展開。
新キー = 既存 figureImage キー + "Setup"。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / seg)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg,
                    x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


def moment_arc(d, cx, cy, r, col=RED):
    """反時計回りの集中モーメント(偶力)記号。矢じりを1つ付ける。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), 20, 320, fill=col, width=3)
    # 終端(20度側)に矢じり
    a = math.radians(20)
    tx, ty = cx + r * math.cos(a), cy - r * math.sin(a)
    arrow(d, tx + 14, ty + 2, tx, ty, col, 3, 11)


# ---- 2-2 ポアソン比(ひずみゲージ) ----
def f_poisson_rod():
    im, d = new(); title(d, "引張を受ける丸棒とひずみゲージ(ポアソン比を問う)")
    x0, x1, yc, th = 200, 460, 210, 34
    d.rectangle((x0, yc - th, x1, yc + th), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((x1 - 14, yc - th, x1 + 14, yc + th), outline=BLACK, width=3, fill=FILL2)
    arrow(d, x0 - 6, yc, x0 - 58, yc, RED, 4, 14); ctext(d, x0 - 72, yc, "P", FS, RED, "rm")
    arrow(d, x1 + 6, yc, x1 + 58, yc, RED, 4, 14); ctext(d, x1 + 72, yc, "P", FS, RED, "lm")
    # 軸ゲージ(軸方向に貼る・横長)
    d.rectangle((290, yc - 8, 360, yc + 8), outline=BLUE, width=2)
    ctext(d, 325, yc - 22, "軸ゲージ", FT, BLUE)
    # 横ゲージ(円周方向=横方向に貼る・縦長)
    d.rectangle((400, yc - 24, 416, yc + 24), outline=GREEN, width=2)
    ctext(d, 408, yc + 40, "横ゲージ", FT, GREEN)
    # 与えられた測定値(答えではない)
    ctext(d, 330, 320, "測定値: 軸ひずみ εa = +1.00×10⁻³", FT, GRAY)
    ctext(d, 330, 344, "        横ひずみ εt = −0.30×10⁻³", FT, GRAY)
    note(d, "測定した2つのひずみから求まるポアソン比 ν は?(答えは未記入)")
    save(im, "s2PoissonRodSetup")


# ---- 2-4 公称応力-公称ひずみ線図(各部の記述を問う) ----
def f_stress_strain_curve():
    im, d = new(); title(d, "金属の公称応力-公称ひずみ線図(正しい記述を問う)")
    ox, oy = 120, 345
    axes(d, ox, oy, 460, 290, "ε", "σ")
    pts = [(ox, oy), (ox + 70, oy - 150),            # 初期直線(弾性)
           (ox + 82, oy - 162), (ox + 110, oy - 165),  # 降伏付近の折れ
           (ox + 180, oy - 210), (ox + 290, oy - 248),  # 加工硬化
           (ox + 350, oy - 252),                        # 最大(山)
           (ox + 410, oy - 228), (ox + 445, oy - 190)]  # くびれ→破断手前
    plot(d, 0, 0, pts, BLUE, 3)
    fx, fy = pts[-1]
    d.line((fx - 8, fy - 8, fx + 8, fy + 8), fill=RED, width=3)  # 破断×
    d.line((fx - 8, fy + 8, fx + 8, fy - 8), fill=RED, width=3)
    note(d, "この線図に関する正しい記述は?(各部の名称は未記入)")
    save(im, "s2StressStrainCurveSetup")


# ---- 2-5 0.2%耐力の定義(作図法を問う) ----
def f_offset_yield():
    im, d = new(); title(d, "明確な降伏点を示さない材料の応力-ひずみ線図")
    ox, oy = 150, 345
    axes(d, ox, oy, 430, 290, "ε", "σ")
    pts = [(ox, oy), (ox + 60, oy - 120), (ox + 110, oy - 185),
           (ox + 180, oy - 230), (ox + 270, oy - 252), (ox + 360, oy - 262),
           (ox + 420, oy - 266)]  # なだらかに移行(明確な降伏点なし)
    plot(d, 0, 0, pts, BLUE, 3)
    # ひずみ軸に 0.2%(0.002) の目盛(与件)。平行線・交点(=答え)は描かない
    tx = ox + 58
    d.line((tx, oy - 6, tx, oy + 6), fill=BLACK, width=2)
    dash(d, tx, oy, tx, oy - 40, GRAY, 2)
    ctext(d, tx, oy + 22, "0.002", FT, GRAY)
    ctext(d, tx, oy + 40, "(0.2%)", FT, GRAY)
    note(d, "この曲線で『0.2%耐力』を求める作図法は?(作図は未記入)")
    save(im, "s2OffsetYieldSetup")


# ---- 2-13 共役せん断応力(y面のτyxを問う) ----
def f_conjugate_shear():
    im, d = new(); title(d, "微小四角形要素のせん断応力(共役せん断を問う)")
    cx, cy, h = 330, 215, 72
    d.rectangle((cx - h, cy - h, cx + h, cy + h), outline=BLACK, width=3, fill=FILL1)
    # x面(左右の面)に与えられたせん断 τxy(右面=上向き, 左面=下向き)
    arrow(d, cx + h, cy + h * 0.6, cx + h, cy - h * 0.6, RED, 3, 11)
    arrow(d, cx - h, cy - h * 0.6, cx - h, cy + h * 0.6, RED, 3, 11)
    ctext(d, cx + h + 40, cy, "τxy(与件)", FT, RED, "lm")
    # y面(上下の面)は未知
    ctext(d, cx, cy - h - 24, "τyx = ?", FS, GRAY)
    ctext(d, cx, cy + h + 24, "τyx = ?", FS, GRAY)
    axes(d, cx - h - 60, cy + h + 48, 56, 48, "x", "y")
    note(d, "x面に τxy。y面に働く共役せん断 τyx の大きさ・向きは?")
    save(im, "s2ConjugateShearSetup")


# ---- 2-16 丸棒の純ねじり(表面要素の主応力を問う) ----
def f_torsion_principal():
    im, d = new(); title(d, "純トルクを受ける丸棒の表面要素(主応力を問う)")
    x0, x1, yc, th = 150, 440, 250, 40
    d.rectangle((x0, yc - th, x1, yc + th), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((x1 - 16, yc - th, x1 + 16, yc + th), outline=BLACK, width=3, fill=FILL2)
    # トルク(両端の回転記号)
    d.arc((x1 - 6, yc - th - 6, x1 + 38, yc + th + 6), -70, 70, fill=BLUE, width=4)
    arrow(d, x1 + 30, yc - th + 6, x1 + 34, yc - th + 26, BLUE, 4, 11)
    ctext(d, x1 + 50, yc, "T", FS, BLUE, "lm")
    ctext(d, x0 + 70, yc, "中実丸棒", FT, GRAY)
    # 表面の微小要素(純せん断=せん断矢印のみ。主軸や45°は描かない)
    ex, ey, eh = 250, 120, 42
    d.rectangle((ex - eh, ey - eh, ex + eh, ey + eh), outline=BLACK, width=3, fill="white")
    arrow(d, ex + eh, ey + eh * 0.55, ex + eh, ey - eh * 0.55, GREEN, 3, 10)
    arrow(d, ex - eh, ey - eh * 0.55, ex - eh, ey + eh * 0.55, GREEN, 3, 10)
    arrow(d, ex - eh * 0.55, ey - eh, ex + eh * 0.55, ey - eh, GREEN, 3, 10)
    arrow(d, ex + eh * 0.55, ey + eh, ex - eh * 0.55, ey + eh, GREEN, 3, 10)
    ctext(d, ex + eh + 30, ey, "純せん断 τ", FT, GREEN, "lm")
    dash(d, ex, ey + eh, 300, yc - th, GRAY, 2)
    note(d, "表面要素は純せん断τ。主応力 σ1,σ2 の向きと大きさは?")
    save(im, "s2TorsionPrincipalSetup")


# ---- 2-17 荷重状態とモール円の対応(荷重状態のみ提示) ----
def f_mohr_compare():
    im, d = new(); title(d, "2つの荷重状態(対応するモール円を問う)")
    # (A) 純ねじり
    ax0, ax1, ayc, ath = 70, 250, 190, 34
    d.rectangle((ax0, ayc - ath, ax1, ayc + ath), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((ax1 - 14, ayc - ath, ax1 + 14, ayc + ath), outline=BLACK, width=3, fill=FILL2)
    d.arc((ax1 - 6, ayc - ath - 6, ax1 + 36, ayc + ath + 6), -70, 70, fill=BLUE, width=4)
    arrow(d, ax1 + 28, ayc - ath + 6, ax1 + 32, ayc - ath + 24, BLUE, 4, 11)
    ctext(d, ax1 + 46, ayc, "T", FT, BLUE, "lm")
    ctext(d, (ax0 + ax1) / 2, ayc + ath + 34, "(A) 純ねじり(純せん断)", FT, BLACK)
    # (B) 単軸引張
    bx0, bx1, byc, bth = 420, 580, 190, 34
    d.rectangle((bx0, byc - bth, bx1, byc + bth), outline=BLACK, width=3, fill=FILL1)
    arrow(d, bx0 - 6, byc, bx0 - 48, byc, RED, 4, 13); ctext(d, bx0 - 60, byc, "σ", FT, RED, "rm")
    arrow(d, bx1 + 6, byc, bx1 + 48, byc, RED, 4, 13); ctext(d, bx1 + 60, byc, "σ", FT, RED, "lm")
    ctext(d, (bx0 + bx1) / 2, byc + bth + 34, "(B) 単軸引張 σ", FT, BLACK)
    note(d, "各荷重に対応するモール円(中心・半径)は?")
    save(im, "s2MohrCompareSetup")


# ---- 2-23 先端集中モーメントの片持ちはり(内力分布を問う) ----
def f_cant_moment():
    im, d = new(); title(d, "自由端に集中モーメントを受ける片持ちはり")
    x0, x1, yb = 160, 540, 215
    wall(d, x0, yb - 42, yb + 42, side=-1); ctext(d, x0 - 24, yb, "固定端", FT, GRAY, "rm")
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    node(d, x1, yb, 6, "white"); ctext(d, x1, yb + 24, "自由端", FT, GRAY)
    moment_arc(d, x1, yb, 34, RED)
    ctext(d, x1 + 50, yb - 4, "M0", FS, RED, "lm")
    ctext(d, (x0 + x1) / 2, yb - 70, "横力(分布・集中荷重)は一切なし", FT, GRAY)
    note(d, "このはりのせん断力・曲げモーメント分布は?(内力は未記入)")
    save(im, "s2CantMomentSetup")


# ---- 2-24 中央集中荷重の単純支持はり(δを1/4にする変更を問う) ----
def f_beam_defl_ei():
    im, d = new(); title(d, "中央に集中荷重を受ける単純支持はり(δ=PL³/48EI)")
    x0, x1, yb = 110, 560, 210
    cx = (x0 + x1) / 2
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    pin_support(d, x0, yb); roller_support(d, x1, yb)
    force(d, cx, yb - 70, 0, 62, "P", RED)
    dim(d, x0, yb + 70, x1, yb + 70, "スパン L")
    dim(d, x0, yb + 104, cx, yb + 104, "L/2")
    ctext(d, cx, 318, "P・L は変えない。E,I は変更可", FT, GRAY)
    note(d, "中央たわみ δ を元の 1/4 にする E・I の変更は?")
    save(im, "s2BeamDeflEISetup")


# ---- 2-25 同一面積・同一全高の4断面(Z最大を問う) ----
def f_section_z():
    im, d = new(); title(d, "同一断面積・同一全高の4断面(断面係数Zを問う)")
    yc, hh = 215, 60          # 全高 = 2*hh = 120
    top, bot = yc - hh, yc + hh
    dash(d, 40, yc, 630, yc, GRAY, 2)                 # 曲げ軸(中立軸)
    dash(d, 40, top, 630, top, LGRAY, 2)             # 全高の上限
    dash(d, 40, bot, 630, bot, LGRAY, 2)
    ctext(d, 592, top - 14, "全高 h(共通)", FT, GRAY, "mm")
    # 1) 円
    c1 = 110
    d.ellipse((c1 - hh, top, c1 + hh, bot), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c1, bot + 26, "円", FT, BLACK)
    # 2) 正方形
    c2 = 260; s = 54
    d.rectangle((c2 - s, yc - s, c2 + s, yc + s), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c2, bot + 26, "正方形", FT, BLACK)
    # 3) 横長長方形(曲げ軸を短辺に平行=背が低い)
    c3 = 420; hw, hht = 70, 30
    d.rectangle((c3 - hw, yc - hht, c3 + hw, yc + hht), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c3, bot + 26, "横長", FT, BLACK)
    # 4) I形(薄ウェブ+フランジ)
    c4 = 575; fw, ft, wt = 46, 15, 14
    d.rectangle((c4 - fw, top, c4 + fw, top + ft), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((c4 - fw, bot - ft, c4 + fw, bot), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((c4 - wt, top + ft, c4 + wt, bot - ft), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c4, bot + 26, "I形", FT, BLACK)
    ctext(d, 335, bot + 52, "断面積A・全高h はすべて共通", FT, GRAY)
    note(d, "断面係数 Z が最も大きい(σmaxが最小の)断面は?(答えは未記入)")
    save(im, "s2SectionZSetup")


# ---- 2-26 I形断面の断面二次モーメント(誤りの記述を問う) ----
def f_isection_inertia():
    im, d = new(); title(d, "I形(H形)断面の断面二次モーメント(誤りを問う)")
    cx, yc = 250, 210; fw, ft, wt, hh = 72, 20, 16, 66
    top, bot = yc - hh, yc + hh
    d.rectangle((cx - fw, top, cx + fw, top + ft), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((cx - fw, bot - ft, cx + fw, bot), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((cx - wt, top + ft, cx + wt, bot - ft), outline=BLACK, width=3, fill=FILL2)
    dash(d, cx - fw - 40, yc, cx + fw + 150, yc, GRAY, 2)
    ctext(d, cx + fw + 170, yc, "図心軸", FT, GRAY, "lm")
    ctext(d, cx + fw + 24, top + ft / 2, "フランジ(上)", FT, BLACK, "lm")
    ctext(d, cx + fw + 24, bot - ft / 2, "フランジ(下)", FT, BLACK, "lm")
    ctext(d, cx + wt + 20, yc - 36, "ウェブ(薄い)", FT, BLACK, "lm")
    dim(d, cx - fw - 24, yc, cx - fw - 24, top + ft / 2, "d")   # 図心軸→上フランジ距離
    note(d, "図心軸まわりの I について誤っている記述は?(数値は未記入)")
    save(im, "s2IsectionInertiaSetup")


# ---- 2-36 4つの応力履歴(疲労寿命が最短のものを問う) ----
def _stress_history(d, ox, oy, w, amp, mean, label, scale=0.34):
    """応力-時間のミニ波形。ox,oy=左・ゼロ線。amp,meanはMPa。"""
    zero_y = oy
    axis_top = zero_y - 80; axis_bot = zero_y + 36
    arrow(d, ox, axis_bot, ox, axis_top, BLACK, 2, 9)        # σ軸
    arrow(d, ox, zero_y, ox + w + 16, zero_y, BLACK, 2, 9)   # t軸(=σ=0)
    ctext(d, ox - 8, axis_top - 2, "σ", FT, BLACK, "rm")
    my = zero_y - mean * scale
    dash(d, ox, my, ox + w, my, GRAY, 2)                    # 平均応力線
    pts = []
    n = 60
    for i in range(n + 1):
        t = i / n
        s = mean + amp * math.sin(2 * math.pi * 1.5 * t)
        pts.append((ox + 6 + t * (w - 6), zero_y - s * scale))
    plot(d, 0, 0, pts, BLUE, 2)
    ctext(d, ox + w / 2, axis_bot + 18, label, FT, BLACK)


def f_four_histories():
    im, d = new(); title(d, "4つの応力履歴(疲労寿命が最短のものを問う)")
    w = 230
    _stress_history(d, 70, 130, w, 50, 0, "① 振幅50 / 平均0")
    _stress_history(d, 380, 130, w, 80, 0, "② 振幅80 / 平均0")
    _stress_history(d, 70, 300, w, 60, 50, "③ 振幅60 / 平均50")
    _stress_history(d, 380, 300, w, 80, 100, "④ 振幅80 / 平均100")
    note(d, "いずれも降伏応力以下。疲労寿命が最も短いのは?(答えは未記入)")
    save(im, "s2GoodmanDiagramSetup")


def main():
    f_poisson_rod()
    f_stress_strain_curve()
    f_offset_yield()
    f_conjugate_shear()
    f_torsion_principal()
    f_mohr_compare()
    f_cant_moment()
    f_beam_defl_ei()
    f_section_z()
    f_isection_inertia()
    f_four_histories()
    print("done 11 figures")


if __name__ == "__main__":
    main()
