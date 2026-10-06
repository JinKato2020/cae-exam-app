# -*- coding: utf-8 -*-
"""固体2級 第2章(固体力学の基礎)の図生成。
白地660x420・黒線画・アプリ最適化(文字=figlib標準/余白を詰める/冗長な見出し・与件の重複は描かない)。

- 回答前(preFigureImage, 〜Setup): 配置/寸法/荷重/与えられた応力状態のみ。答えは描かない(required相当)。
- 回答後(figureImage): 解(ポアソン比の値/主応力の±45°とσ1,σ2/モール円の中心・半径)を描く(helpful)。

2-2/2-16/2-17/2-30 は提供参考図を基に 3D円筒で作図し直し(文字サイズ・余白をアプリ最適化)。
他7問(2-4/2-5/2-13/2-23/2-24/2-25/2-26/2-36)のSetupは従来通り。
[[cae-figure-before-after-rule]] 第2章横展開。"""
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
    a = math.radians(20)
    tx, ty = cx + r * math.cos(a), cy - r * math.sin(a)
    arrow(d, tx + 14, ty + 2, tx, ty, col, 3, 11)


# ============ 共通ヘルパー(3D円筒・トルク・モール円) ============
def cyl3d(d, x0, x1, yc, ry, rx=18, fill=FILL1, cap=FILL2):
    """横向き3D円筒。左端=手前の開口(明)、右端=奥のふくらみ(淡)。"""
    d.ellipse((x1 - rx, yc - ry, x1 + rx, yc + ry), outline=BLACK, width=3, fill=cap)
    d.rectangle((x0, yc - ry, x1, yc + ry), fill=fill)
    d.line((x0, yc - ry, x1, yc - ry), fill=BLACK, width=3)
    d.line((x0, yc + ry, x1, yc + ry), fill=BLACK, width=3)
    d.ellipse((x0 - rx, yc - ry, x0 + rx, yc + ry), outline=BLACK, width=3, fill=fill)


def torque_end(d, xe, yc, ry, side=1, col=BLUE):
    """円筒端のトルク(回転)記号。side=1:右端 / -1:左端。"""
    if side == 1:
        d.arc((xe - 6, yc - ry - 6, xe + 40, yc + ry + 6), -70, 70, fill=col, width=4)
        arrow(d, xe + 32, yc - ry + 4, xe + 36, yc - ry + 26, col, 4, 11)
    else:
        d.arc((xe - 40, yc - ry - 6, xe + 6, yc + ry + 6), 110, 250, fill=col, width=4)
        arrow(d, xe - 32, yc + ry - 4, xe - 36, yc + ry - 26, col, 4, 11)


def shear_square(d, cx, cy, h, col=GREEN, tag=True):
    """軸に平行な微小四角要素+共役せん断(偶力)。純せん断状態。"""
    d.rectangle((cx - h, cy - h, cx + h, cy + h), outline=BLACK, width=3, fill="white")
    # 右面 上向き / 左面 下向き / 上面 左向き / 下面 右向き(つり合う偶力)
    arrow(d, cx + h, cy + h * 0.6, cx + h, cy - h * 0.6, col, 3, 10)
    arrow(d, cx - h, cy - h * 0.6, cx - h, cy + h * 0.6, col, 3, 10)
    arrow(d, cx + h * 0.6, cy - h, cx - h * 0.6, cy - h, col, 3, 10)
    arrow(d, cx - h * 0.6, cy + h, cx + h * 0.6, cy + h, col, 3, 10)
    if tag:
        ctext(d, cx + h + 18, cy, "τ", FS, col, "lm")


def mohr_axes(d, cx, cy, span):
    """モール円用の局所σ-τ軸(原点cx,cy)。"""
    arrow(d, cx - span, cy, cx + span, cy, BLACK, 2, 10); ctext(d, cx + span + 10, cy, "σ", FT, BLACK, "lm")
    arrow(d, cx, cy + span * 0.8, cx, cy - span * 0.9, BLACK, 2, 10); ctext(d, cx, cy - span * 0.9 - 10, "τ", FT, BLACK)


# ============ 2-2 ポアソン比(ひずみゲージ) ============
def _base_poisson(d):
    title(d, "引張を受ける丸棒とひずみゲージ")
    x0, x1, yc, ry = 215, 455, 205, 44
    cyl3d(d, x0, x1, yc, ry)
    arrow(d, x0 - 24, yc, x0 - 78, yc, RED, 4, 15); ctext(d, x0 - 86, yc, "引張荷重 P", FT, RED, "rm")
    arrow(d, x1 + 6, yc, x1 + 60, yc, RED, 4, 15); ctext(d, x1 + 68, yc, "引張荷重 P", FT, RED, "lm")
    d.rectangle((300, yc - 34, 362, yc - 18), outline=BLUE, width=3)
    d.line((331, yc - 34, 331, yc - 64), fill=BLUE, width=2)
    ctext(d, 331, yc - 76, "軸方向ゲージ", FT, BLUE)
    d.rectangle((406, yc - 22, 420, yc + 26), outline=GREEN, width=3)
    d.line((420, yc + 20, 452, yc + 48), fill=GREEN, width=2)
    ctext(d, 456, yc + 54, "横方向ゲージ", FT, GREEN, "lm")
    ctext(d, 330, 322, "測定: 軸ひずみ εa=+1.00×10⁻³ / 横ひずみ εt=−0.30×10⁻³", FT, GRAY)


def f_poisson_rod():
    im, d = new(); _base_poisson(d)
    note(d, "2つのひずみからポアソン比 ν を求める(答えは未記入)")
    save(im, "s2PoissonRodSetup")


def f_poisson_rod_after():
    im, d = new(); _base_poisson(d)
    ctext(d, 330, 352, "ν = −εt/εa = −(−0.30×10⁻³)/(1.00×10⁻³) = 0.30", FS, BLACK)
    note(d, "縦に伸ばすと横に縮む。その比(符号を反転)がポアソン比 ν")
    save(im, "s2PoissonRod")


# ============ 2-4 公称応力-公称ひずみ線図 ============
def f_stress_strain_curve():
    im, d = new(); title(d, "金属の公称応力-公称ひずみ線図(正しい記述を問う)")
    ox, oy = 120, 345
    axes(d, ox, oy, 460, 290, "ε", "σ")
    pts = [(ox, oy), (ox + 70, oy - 150),
           (ox + 82, oy - 162), (ox + 110, oy - 165),
           (ox + 180, oy - 210), (ox + 290, oy - 248),
           (ox + 350, oy - 252),
           (ox + 410, oy - 228), (ox + 445, oy - 190)]
    plot(d, 0, 0, pts, BLUE, 3)
    fx, fy = pts[-1]
    d.line((fx - 8, fy - 8, fx + 8, fy + 8), fill=RED, width=3)
    d.line((fx - 8, fy + 8, fx + 8, fy - 8), fill=RED, width=3)
    note(d, "この線図に関する正しい記述は?(各部の名称は未記入)")
    save(im, "s2StressStrainCurveSetup")


# ============ 2-5 0.2%耐力の定義 ============
def f_offset_yield():
    im, d = new(); title(d, "明確な降伏点を示さない材料の応力-ひずみ線図")
    ox, oy = 150, 345
    axes(d, ox, oy, 430, 290, "ε", "σ")
    pts = [(ox, oy), (ox + 60, oy - 120), (ox + 110, oy - 185),
           (ox + 180, oy - 230), (ox + 270, oy - 252), (ox + 360, oy - 262),
           (ox + 420, oy - 266)]
    plot(d, 0, 0, pts, BLUE, 3)
    tx = ox + 58
    d.line((tx, oy - 6, tx, oy + 6), fill=BLACK, width=2)
    dash(d, tx, oy, tx, oy - 40, GRAY, 2)
    ctext(d, tx, oy + 22, "0.002", FT, GRAY)
    ctext(d, tx, oy + 40, "(0.2%)", FT, GRAY)
    note(d, "この曲線で『0.2%耐力』を求める作図法は?(作図は未記入)")
    save(im, "s2OffsetYieldSetup")


# ============ 2-13 共役せん断応力 ============
def f_conjugate_shear():
    im, d = new(); title(d, "微小四角形要素のせん断応力(共役せん断を問う)")
    cx, cy, h = 330, 215, 72
    d.rectangle((cx - h, cy - h, cx + h, cy + h), outline=BLACK, width=3, fill=FILL1)
    arrow(d, cx + h, cy + h * 0.6, cx + h, cy - h * 0.6, RED, 3, 11)
    arrow(d, cx - h, cy - h * 0.6, cx - h, cy + h * 0.6, RED, 3, 11)
    ctext(d, cx + h + 40, cy, "τxy(与件)", FT, RED, "lm")
    ctext(d, cx, cy - h - 24, "τyx = ?", FS, GRAY)
    ctext(d, cx, cy + h + 24, "τyx = ?", FS, GRAY)
    axes(d, cx - h - 60, cy + h + 48, 56, 48, "x", "y")
    note(d, "x面に τxy。y面に働く共役せん断 τyx の大きさ・向きは?")
    save(im, "s2ConjugateShearSetup")


# ============ 2-16 丸棒の純ねじり(表面要素の主応力) ============
def _base_torsion(d):
    title(d, "純トルクを受ける丸棒と表面の微小要素")
    x0, x1, yc, ry = 70, 300, 250, 42
    cyl3d(d, x0, x1, yc, ry)
    torque_end(d, x1, yc, ry, side=1); torque_end(d, x0, yc, ry, side=-1)
    ctext(d, x1 + 54, yc, "T", FS, BLUE, "lm"); ctext(d, x0 - 54, yc, "T", FS, BLUE, "rm")
    d.rectangle((176, yc - 14, 206, yc + 14), outline=GREEN, width=3, fill=(236, 248, 238))
    dash(d, 206, yc - 14, 470, 150, GRAY, 2)
    ex, ey, eh = 500, 150, 48
    shear_square(d, ex, ey, eh, GREEN)
    ctext(d, ex, ey - eh - 20, "表面の微小要素", FT, BLACK)
    arrow(d, ex - eh, ey + eh + 26, ex + eh, ey + eh + 26, GRAY, 2, 9); ctext(d, ex, ey + eh + 40, "軸方向", FT, GRAY)
    arrow(d, ex - eh - 24, ey + eh, ex - eh - 24, ey - eh, GRAY, 2, 9); ctext(d, ex - eh - 40, ey, "円周", FT, GRAY, "rm")
    return ex, ey, eh


def f_torsion_principal():
    im, d = new(); _base_torsion(d)
    note(d, "表面は純せん断τ。主応力 σ1,σ2 の向き・大きさは?(答えは未記入)")
    save(im, "s2TorsionPrincipalSetup")


def f_torsion_after():
    im, d = new()
    ex, ey, eh = _base_torsion(d)
    # 同じ表面要素に主応力(±45°): σ1=+τ引張(赤・外向き) / σ2=−τ圧縮(緑・内向き)
    r = eh + 24; k = 0.71
    arrow(d, ex, ey, ex + r * k, ey - r * k, RED, 3, 11); arrow(d, ex, ey, ex - r * k, ey + r * k, RED, 3, 11)
    arrow(d, ex + r * k, ey + r * k, ex + (eh - 8) * k, ey + (eh - 8) * k, GREEN, 3, 11)
    arrow(d, ex - r * k, ey - r * k, ex - (eh - 8) * k, ey - (eh - 8) * k, GREEN, 3, 11)
    ctext(d, ex + r * k + 12, ey - r * k - 4, "σ1=+τ", FT, RED, "lm")
    ctext(d, ex + r * k + 12, ey + r * k + 4, "σ2=−τ", FT, GREEN, "lm")
    ctext(d, 300, 330, "主応力は ±45°方向: σ1=+τ(引張), σ2=−τ(圧縮)", FS, BLACK)
    note(d, "純せん断τは±45°で引張+τ・圧縮−τに等価(大きさはτ)")
    save(im, "s2TorsionPrincipal")


# ============ 2-17 荷重状態とモール円の対応 ============
def _base_mohr(d):
    title(d, "2つの荷重状態とモールの応力円")
    ax0, ax1, ayc, ary = 70, 250, 180, 34
    cyl3d(d, ax0, ax1, ayc, ary)
    torque_end(d, ax1, ayc, ary, side=1); ctext(d, ax1 + 52, ayc, "T", FS, BLUE, "lm")
    ctext(d, (ax0 + ax1) / 2, 108, "A 純ねじり(純せん断)", FS, BLUE)
    ctext(d, (ax0 + ax1) / 2, ayc + ary + 24, "せん断応力 τ のみ", FT, GRAY)
    bx0, bx1, byc, bry = 420, 580, 180, 34
    cyl3d(d, bx0, bx1, byc, bry)
    arrow(d, bx0 - 10, byc, bx0 - 56, byc, RED, 4, 14); ctext(d, bx0 - 64, byc, "σ", FS, RED, "rm")
    arrow(d, bx1 + 10, byc, bx1 + 56, byc, RED, 4, 14); ctext(d, bx1 + 64, byc, "σ", FS, RED, "lm")
    ctext(d, (bx0 + bx1) / 2, 108, "B 単軸引張", FS, RED)
    ctext(d, (bx0 + bx1) / 2, byc + bry + 24, "軸方向の引張応力 σ", FT, GRAY)


def _mini_mohr(d, cc, ocy, R, origin_x, col, label):
    arrow(d, min(cc - R, origin_x) - 14, ocy, cc + R + 22, ocy, BLACK, 2, 8); ctext(d, cc + R + 30, ocy, "σ", FT, BLACK, "lm")
    arrow(d, origin_x, ocy + 28, origin_x, ocy - 38, BLACK, 2, 8); ctext(d, origin_x - 6, ocy - 44, "τ", FT, BLACK, "rm")
    d.ellipse((cc - R, ocy - R, cc + R, ocy + R), outline=col, width=3)
    node(d, cc, ocy, 3, BLACK)
    ctext(d, cc, ocy + R + 18, label, FT, GRAY)


def f_mohr_compare():
    im, d = new(); _base_mohr(d)
    note(d, "モール円(横軸σ/縦軸τ)の中心・半径は?(答えは未記入)")
    save(im, "s2MohrCompareSetup")


def f_mohr_after():
    im, d = new(); _base_mohr(d)
    _mini_mohr(d, 150, 322, 28, 150, BLUE, "中心0・半径τ")
    _mini_mohr(d, 458, 322, 28, 430, RED, "中心σ/2・半径σ/2")
    note(d, "ねじり=原点中心(半径τ) / 引張=σ/2中心(半径σ/2)。最大せん断=半径")
    save(im, "s2MohrCompare")


# ============ 2-23 先端集中モーメントの片持ちはり ============
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


# ============ 2-24 中央集中荷重の単純支持はり ============
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


# ============ 2-25 同一面積・同一全高の4断面 ============
def f_section_z():
    im, d = new(); title(d, "同一断面積・同一全高の4断面(断面係数Zを問う)")
    yc, hh = 215, 60
    top, bot = yc - hh, yc + hh
    dash(d, 40, yc, 630, yc, GRAY, 2)
    dash(d, 40, top, 630, top, LGRAY, 2)
    dash(d, 40, bot, 630, bot, LGRAY, 2)
    ctext(d, 592, top - 14, "全高 h(共通)", FT, GRAY, "mm")
    c1 = 110
    d.ellipse((c1 - hh, top, c1 + hh, bot), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c1, bot + 26, "円", FT, BLACK)
    c2 = 260; s = 54
    d.rectangle((c2 - s, yc - s, c2 + s, yc + s), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c2, bot + 26, "正方形", FT, BLACK)
    c3 = 420; hw, hht = 70, 30
    d.rectangle((c3 - hw, yc - hht, c3 + hw, yc + hht), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c3, bot + 26, "横長", FT, BLACK)
    c4 = 575; fw, ft, wt = 46, 15, 14
    d.rectangle((c4 - fw, top, c4 + fw, top + ft), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((c4 - fw, bot - ft, c4 + fw, bot), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((c4 - wt, top + ft, c4 + wt, bot - ft), outline=BLACK, width=3, fill=FILL1)
    ctext(d, c4, bot + 26, "I形", FT, BLACK)
    ctext(d, 335, bot + 52, "断面積A・全高h はすべて共通", FT, GRAY)
    note(d, "断面係数 Z が最も大きい(σmaxが最小の)断面は?(答えは未記入)")
    save(im, "s2SectionZSetup")


# ============ 2-26 I形断面の断面二次モーメント ============
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
    dim(d, cx - fw - 24, yc, cx - fw - 24, top + ft / 2, "d")
    note(d, "図心軸まわりの I について誤っている記述は?(数値は未記入)")
    save(im, "s2IsectionInertiaSetup")


# ============ 2-30 内圧を受ける薄肉円筒 ============
def f_thin_cylinder():
    im, d = new(); title(d, "内圧を受ける薄肉円筒(両端閉じ)")
    x0, x1, yc, ry = 190, 470, 200, 58
    cyl3d(d, x0, x1, yc, ry)
    cm = (x0 + x1) / 2
    # 内圧(放射状の外向き矢印・青)
    arrow(d, cm, yc, cm, yc - ry + 6, BLUE, 3, 11)
    arrow(d, cm, yc, cm, yc + ry - 6, BLUE, 3, 11)
    arrow(d, cm - 70, yc, cm - 120, yc, BLUE, 3, 11)
    arrow(d, cm + 70, yc, cm + 120, yc, BLUE, 3, 11)
    ctext(d, cm, yc - 16, "内圧 p=2MPa", FT, BLUE)
    # 内半径(緑・左端)/ 板厚(赤・右上)
    arrow(d, x0 - 2, yc, x0 - 2, yc - ry + 4, GREEN, 3, 10)
    ctext(d, x0 - 10, yc - ry - 14, "内半径 r=0.5m", FT, GREEN, "mm")
    d.line((x1 - 6, yc - ry, x1 + 40, yc - ry - 38), fill=RED, width=2)
    ctext(d, x1 + 44, yc - ry - 46, "板厚 t=5mm", FT, RED, "lm")
    dim(d, x0, yc + ry + 34, x1, yc + ry + 34, "長さ L=2m")
    ctext(d, 330, 338, "E=200GPa / ν=0.3", FT, GRAY)
    note(d, "内容積の変化 ΔV は?")
    save(im, "s2ThinCylinder")


# ============ 2-36 4つの応力履歴 ============
def _stress_history(d, ox, oy, w, amp, mean, label, scale=0.34):
    zero_y = oy
    axis_top = zero_y - 80; axis_bot = zero_y + 36
    arrow(d, ox, axis_bot, ox, axis_top, BLACK, 2, 9)
    arrow(d, ox, zero_y, ox + w + 16, zero_y, BLACK, 2, 9)
    ctext(d, ox - 8, axis_top - 2, "σ", FT, BLACK, "rm")
    my = zero_y - mean * scale
    dash(d, ox, my, ox + w, my, GRAY, 2)
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
    # 2-2/2-16/2-17/2-30 = 3D円筒で作り直し(回答前+回答後)
    f_poisson_rod(); f_poisson_rod_after()
    f_torsion_principal(); f_torsion_after()
    f_mohr_compare(); f_mohr_after()
    f_thin_cylinder()
    # その他の回答前(従来)
    f_stress_strain_curve()
    f_offset_yield()
    f_conjugate_shear()
    f_cant_moment()
    f_beam_defl_ei()
    f_section_z()
    f_isection_inertia()
    f_four_histories()
    print("done ch2 figures (4問 再設計: 回答前4 + 回答後3, 他7)")


if __name__ == "__main__":
    main()
