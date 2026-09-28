# -*- coding: utf-8 -*-
"""固体2級 計算問題の「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(配置/寸法/荷重)のみ。答え・正解値・結論は一切描かない(=required相当)。
既存の figureImage(解説図/答え示唆あり)は回答後(helpful)のまま残し、本図を回答前に出す(前後2図)。
JSON配線は別途。ここでは assets/figures/<key>.png を生成するのみ。
[[cae-figure-before-after-rule]] 厳命D の横展開。"""
import sys, math, os
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- 応力要素(与えられた応力状態のみ。主応力/相当応力など答えは描かない) ----
def stress_elem(d, cx, cy, h, sx=None, sy=None, txy=None, sx_t=True, sy_t=True, theta=None):
    d.rectangle((cx - h, cy - h, cx + h, cy + h), outline=BLACK, width=3, fill=FILL1)
    if sx is not None:
        if sx_t:  # 引張=外向き
            arrow(d, cx + h, cy, cx + h + 44, cy, RED, 3, 12)
            arrow(d, cx - h, cy, cx - h - 44, cy, RED, 3, 12)
        else:     # 圧縮=内向き
            arrow(d, cx + h + 44, cy, cx + h, cy, RED, 3, 12)
            arrow(d, cx - h - 44, cy, cx - h, cy, RED, 3, 12)
        ctext(d, cx + h + 58, cy - 16, sx, FS, RED, "lm")
    if sy is not None:
        if sy_t:
            arrow(d, cx, cy - h, cx, cy - h - 44, BLUE, 3, 12)
            arrow(d, cx, cy + h, cx, cy + h + 44, BLUE, 3, 12)
        else:
            arrow(d, cx, cy - h - 44, cx, cy - h, BLUE, 3, 12)
            arrow(d, cx, cy + h + 44, cx, cy + h, BLUE, 3, 12)
        ctext(d, cx, cy - h - 58, sy, FS, BLUE)
    if txy is not None:
        arrow(d, cx + h, cy + h * 0.55, cx + h, cy - h * 0.55, GREEN, 3, 11)
        arrow(d, cx - h, cy - h * 0.55, cx - h, cy + h * 0.55, GREEN, 3, 11)
        arrow(d, cx - h * 0.55, cy - h, cx + h * 0.55, cy - h, GREEN, 3, 11)
        arrow(d, cx + h * 0.55, cy + h, cx - h * 0.55, cy + h, GREEN, 3, 11)
        ctext(d, cx - h - 58, cy + h + 20, txy, FT, GREEN, "rm")
    if theta is not None:
        L = h + 60
        a = math.radians(theta)
        arrow(d, cx, cy, cx + L * math.cos(a), cy - L * math.sin(a), GRAY, 2, 11)
        ctext(d, cx + (L + 14) * math.cos(a), cy - (L + 14) * math.sin(a), "x'", FT, GRAY)
        angle_arc(d, cx, cy, 46, 0, theta, f"{theta}°", GRAY)


def f_stress_transform():   # 2-6
    im, d = new(); title(d, "応力の座標変換(45°回転面の垂直応力を求める)")
    stress_elem(d, 300, 215, 78, "σx=60", "σy=20", "τxy=30", theta=45)
    note(d, "与えられた面内応力状態。x軸から反時計回り45°回転した面の σx' はいくらか。")
    save(im, "s2StressTransformSetup")


def f_principal():          # 2-18
    im, d = new(); title(d, "平面応力状態(最大主応力・主軸角を求める)")
    stress_elem(d, 320, 215, 82, "σx=60", "σy=20", "τxy=15")
    note(d, "この応力状態の 最大主応力 σ1 と 主軸角 θp を求める。")
    save(im, "s2PrincipalSetup")


def f_pure_shear():         # 2-19
    im, d = new(); title(d, "純せん断のみの応力状態(主応力を求める)")
    stress_elem(d, 320, 215, 82, None, None, "τxy=40")
    ctext(d, 320, 215, "σx=σy=σz=0", FT, GRAY)
    note(d, "垂直応力ゼロ・せん断 τxy=40 MPa のみ。3つの主応力 (σ1,σ2,σ3) を求める。")
    save(im, "s2PureShearSetup")


def f_mises():              # 2-32
    im, d = new(); title(d, "平面応力状態(ミーゼス基準で降伏判定)")
    stress_elem(d, 320, 210, 80, "σx=100", "σy=50", "τxy=40", sy_t=False)
    ctext(d, 320, 372, "材料の降伏応力 σY = 200 MPa", FT, GRAY)
    note(d, "σy は圧縮(−50 MPa)。相当応力を求め σY と比べて降伏の有無を判定する。")
    save(im, "s2MisesSetup")


def f_rigid_plate_2bars():  # 2-12
    im, d = new(); title(d, "剛体板を2本の弾性棒で吊る(板は水平を保つ)")
    hwall(d, 200, 470, 92, side=1)
    d.rectangle((240, 92, 266, 250), outline=BLACK, width=3, fill=FILL1)   # 棒1(太)
    ctext(d, 232, 165, "棒1(A1=太)", FT, BLACK, "rm")
    d.rectangle((416, 92, 426, 250), outline=BLACK, width=3, fill=FILL1)   # 棒2(細)
    ctext(d, 440, 165, "棒2(A2=細)", FT, BLACK, "lm")
    d.rectangle((205, 250, 465, 275), outline=BLACK, width=3, fill=FILL2)  # 剛体板
    ctext(d, 335, 262, "剛体板", FT, BLACK)
    force(d, 335, 275, 0, 62, "P", RED)
    ctext(d, 335, 355, "L=1000mm, E=200GPa", FT, GRAY)
    note(d, "板が傾かないよう鉛直荷重 P=30kN。太い棒1が受け持つ軸力を求める。")
    save(im, "s2RigidPlate2BarsSetup")


def f_overhang_beam():      # 2-20 / 2-21
    im, d = new(); title(d, "突出しはり(A・C支持、Cの右へ張出し)")
    def X(m): return 70 + m * (590 - 70) / 6.0
    yb = 200
    d.line((X(0), yb, X(6), yb), fill=BLACK, width=5)
    pin_support(d, X(0), yb); ctext(d, X(0), yb - 22, "A(x=0)", FT, BLACK)
    roller_support(d, X(4), yb); ctext(d, X(4), yb - 22, "C(x=4)", FT, BLACK)
    ctext(d, X(6) + 4, yb - 20, "端(x=6)", FT, GRAY)
    force(d, X(2), yb - 60, 0, 54, "10kN", RED)
    force(d, X(6), yb - 60, 0, 54, "6kN", RED)
    dim(d, X(0), yb + 60, X(2), yb + 60, "2m")
    dim(d, X(2), yb + 60, X(4), yb + 60, "2m")
    dim(d, X(4), yb + 60, X(6), yb + 60, "2m")
    note(d, "支点反力 R_A, R_C(および曲げモーメント)を求める。")
    save(im, "s2OverhangBeamSetup")


def f_cantilever_udl():     # 2-22
    im, d = new(); title(d, "片持ちはり+等分布荷重(断面位置は自由端から測る)")
    x0, x1, yb = 90, 590, 215
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    wall(d, x1, yb - 40, yb + 40, side=1)
    ctext(d, x0 - 4, yb + 20, "自由端", FT, GRAY, "lm")
    for m in range(11):
        xx = x0 + m * (x1 - x0) / 10
        arrow(d, xx, yb - 58, xx, yb - 6, RED, 2, 9)
    ctext(d, (x0 + x1) / 2, yb - 74, "w = 3 kN/m", FT, RED)
    xs = x1 - (x1 - x0) / 4.0  # 固定端から1m (L=4m)
    d.line((xs, yb - 6, xs, yb + 46), fill=GREEN, width=2)
    ctext(d, xs, yb + 60, "固定端から1m", FT, GREEN)
    dim(d, x0, yb + 86, xs, yb + 86, "自由端から x=3m")
    note(d, "自由端から x=3m(=固定端から1m)の断面の曲げモーメントを求める。")
    save(im, "s2CantileverUDLSetup")


def f_truss_2bar():         # 2-27
    im, d = new(); title(d, "荷重を吊る2部材トラス(節点法)")
    cx, cy = 390, 305
    yceil = 100
    dyc = cy - yceil  # 205
    x1 = cx - dyc / math.tan(math.radians(30))  # 部材1: 水平から30°
    x2 = cx + dyc / math.tan(math.radians(60))  # 部材2: 水平から60°
    hwall(d, 30, 560, yceil, side=1)
    bar(d, x1, yceil, cx, cy)      # 部材1
    bar(d, x2, yceil, cx, cy)      # 部材2
    ctext(d, (x1 + cx) / 2 - 6, (yceil + cy) / 2 - 16, "部材1", FT, BLUE)
    ctext(d, (x2 + cx) / 2 + 24, (yceil + cy) / 2 - 16, "部材2", FT, BLUE)
    angle_arc(d, cx, cy, 52, 150, 180, "30°", GRAY)  # 左・水平から上へ30°
    angle_arc(d, cx, cy, 52, 0, 60, "60°", GRAY)     # 右・水平から上へ60°
    node(d, cx, cy); ctext(d, cx + 16, cy + 4, "C", FT, BLACK, "lm")
    force(d, cx, cy, 0, 62, "W", RED)
    note(d, "節点Cに鉛直下向き荷重 W。部材内力 S1, S2 を節点法で求める。")
    save(im, "s2Truss2BarSetup")


def f_cant_reactions():     # 2-29
    im, d = new(); title(d, "片持ちはり(自由端に集中荷重+全長に等分布)")
    x0, x1, yb = 100, 560, 215
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    wall(d, x1, yb - 40, yb + 40, side=1)
    ctext(d, x1 + 6, yb, "固定端 D", FT, BLACK, "lm")
    for m in range(10):
        xx = x0 + 14 + m * (x1 - x0 - 20) / 9
        arrow(d, xx, yb - 54, xx, yb - 6, ORANGE, 2, 9)
    ctext(d, (x0 + x1) / 2, yb - 70, "w = 2 kN/m", FT, ORANGE)
    force(d, x0, yb - 64, 0, 58, "P=5kN", RED)
    ctext(d, x0, yb + 22, "自由端(左)", FT, GRAY)
    dim(d, x0, yb + 70, x1, yb + 70, "L = 2m")
    note(d, "固定端Dの鉛直反力 R_D と固定モーメント M_D を求める。")
    save(im, "s2CantReactionsSetup")


def f_hollow_shaft():       # 2-15
    im, d = new(); title(d, "中空丸軸の断面(許容せん断応力からトルクを求める)")
    cx, cy = 240, 220; ro, ri = 110, 55
    d.ellipse((cx - ro, cy - ro, cx + ro, cy + ro), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=BLACK, width=3, fill="white")
    dim(d, cx - ro, cy + ro + 26, cx + ro, cy + ro + 26, "do=40mm")
    dim(d, cx - ri, cy, cx + ri, cy, "di=20mm")
    d.arc((430, 150, 590, 300), -40, 220, fill=BLUE, width=4)
    arrow(d, 590, 240, 585, 205, BLUE, 4, 13)
    ctext(d, 510, 130, "トルク T", FS, BLUE)
    ctext(d, 510, 330, "許容せん断応力", FT, GRAY)
    ctext(d, 510, 350, "τa = 60 MPa", FT, GRAY)
    note(d, "許容せん断応力を超えない最大トルク T_max を求める。")
    save(im, "s2HollowShaftSetup")


def f_plate_holes():        # 2-39
    im, d = new(); title(d, "2つの円孔をもつ平板(軸方向引張)")
    px, pw, pt, pb = 205, 150, 135, 330   # 板の左x,幅,上y,下y
    d.rectangle((px, pt, px + pw, pb), outline=BLACK, width=3, fill=FILL1)
    hy = (pt + pb) / 2
    for hx in (px + pw * 0.32, px + pw * 0.68):
        d.ellipse((hx - 17, hy - 17, hx + 17, hy + 17), outline=BLACK, width=3, fill="white")
    for xx in (px + pw * 0.3, px + pw * 0.5, px + pw * 0.7):
        arrow(d, xx, pt - 8, xx, pt - 46, RED, 3, 12)
        arrow(d, xx, pb + 46, xx, pb + 8, RED, 3, 12)
    ctext(d, px + pw / 2, pt - 62, "引張 P", FS, RED)
    for i, s in enumerate(["板幅 W=100mm", "板厚 t=10mm", "孔径 d=20mm",
                           "応力集中係数 Kt=3", "σ許容 = 120 MPa"]):
        ctext(d, 420, 150 + i * 30, s, FT, GRAY, "lm")
    note(d, "孔縁の最大応力が許容応力を超えない 許容最大荷重 P を求める。")
    save(im, "s2PlateHolesSetup")


def f_half_heated_bar():    # 2-41
    im, d = new(); title(d, "左半分だけ昇温した両端固定棒(熱応力)")
    x0, x1, yc = 120, 540, 215; th = 30
    xm = (x0 + x1) / 2
    wall(d, x0, yc - th - 20, yc + th + 20, side=1)
    wall(d, x1, yc - th - 20, yc + th + 20, side=-1)
    d.rectangle((x0, yc - th, xm, yc + th), outline=BLACK, width=3, fill=(255, 224, 224))
    d.rectangle((xm, yc - th, x1, yc + th), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + xm) / 2, yc, "ΔT=100K 上昇", FT, RED)
    ctext(d, (xm + x1) / 2, yc, "温度変化なし", FT, GRAY)
    dim(d, x0, yc + th + 34, xm, yc + th + 34, "L/2")
    dim(d, xm, yc + th + 34, x1, yc + th + 34, "L/2")
    ctext(d, xm, 320, "E=200GPa, α=12×10⁻⁶/K", FT, GRAY)
    note(d, "両端は剛壁に完全固定。棒に生じる軸方向熱応力(圧縮)の大きさを求める。")
    save(im, "s2HalfHeatedBarSetup")


def f_two_bars_thermal():   # 2-42
    im, d = new(); title(d, "剛体板で結合した2本の棒(棒2のみ昇温)")
    hwall(d, 210, 450, 95, side=1)
    d.rectangle((250, 95, 268, 250), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 300, 165, "棒1", FT, BLACK, "lm")
    d.rectangle((392, 95, 410, 250), outline=BLACK, width=3, fill=(255, 224, 224))
    ctext(d, 430, 165, "棒2(ΔT=80K)", FT, RED, "lm")
    d.rectangle((212, 250, 448, 273), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 261, "剛体板(水平を保つ)", FT, BLACK)
    arrow(d, 330, 285, 330, 330, GRAY, 2, 11)
    ctext(d, 348, 315, "u_T", FT, GRAY, "lm")
    ctext(d, 330, 355, "同一材質・断面・長さ L=500mm, α=12×10⁻⁶/K", FT, GRAY)
    note(d, "外力なし。棒2のみ昇温したときの剛体板の鉛直変位 u_T を求める。")
    save(im, "s2TwoBarsThermalSetup")


# ---- 他章の明確に幾何的な計算問題 ----
def f_cst_setup():          # 7-4
    im, d = new(); title(d, "3節点三角形要素(節点変位から εx を求める)")
    ox, oy, s = 150, 330, 58   # 1mm=58px, A原点
    A = (ox, oy); B = (ox + 5 * s, oy); C = (ox, oy - 4 * s)
    d.polygon([A, B, C], outline=BLACK, width=3, fill=FILL1)
    for p, nm, co, uu in [(A, "A(0,0)", (0, 24), "uA=0.008"),
                          (B, "B(5,0)", (0, 24), "uB=0.033"),
                          (C, "C(0,4)", (-6, -6), "uC=0.020")]:
        node(d, p[0], p[1])
        ctext(d, p[0] + co[0], p[1] + co[1], nm, FT, BLACK)
    ctext(d, A[0] - 6, A[1] + 42, "uA=0.008", FT, BLUE, "lm")
    ctext(d, B[0] - 40, B[1] + 42, "uB=0.033", FT, BLUE, "lm")
    ctext(d, C[0] - 6, C[1] - 26, "uC=0.020", FT, BLUE, "lm")
    ctext(d, 470, 300, "座標 mm / 変位 mm", FT, GRAY, "lm")
    note(d, "x方向変位 u=a0+a1x+a2y。各節点の u から要素の εx を求める。")
    save(im, "elem7CstSetup")


def f_reaction_beam():      # 9-8b
    im, d = new(); title(d, "単純支持ばり(反力の検算)")
    def X(m): return 90 + m * (570 - 90) / 4.0
    yb = 210
    d.line((X(0), yb, X(4), yb), fill=BLACK, width=5)
    pin_support(d, X(0), yb); ctext(d, X(0), yb - 22, "A", FT, BLACK)
    roller_support(d, X(4), yb); ctext(d, X(4), yb - 22, "B", FT, BLACK)
    force(d, X(1), yb - 62, 0, 54, "P=12kN", RED)
    dim(d, X(0), yb + 60, X(1), yb + 60, "a=1m")
    dim(d, X(0), yb + 92, X(4), yb + 92, "L=4m")
    note(d, "左端Aから1mに集中荷重 P。右端支持Bの鉛直反力を検算する。")
    save(im, "bc9ReactionBeamSetup")


def f_ver_hole():           # 11-1
    im, d = new(); title(d, "円孔をもつ帯板(応力集中の検証)")
    px, pw, pt, pb = 200, 130, 135, 330
    d.rectangle((px, pt, px + pw, pb), outline=BLACK, width=3, fill=FILL1)
    cx, cy = px + pw / 2, (pt + pb) / 2
    d.ellipse((cx - 25, cy - 25, cx + 25, cy + 25), outline=BLACK, width=3, fill="white")
    for xx in (px + pw * 0.28, px + pw * 0.72):
        arrow(d, xx, pt - 8, xx, pt - 46, RED, 3, 12)
        arrow(d, xx, pb + 46, xx, pb + 8, RED, 3, 12)
    ctext(d, cx, pt - 62, "引張 P=4000N", FS, RED)
    for i, s in enumerate(["板幅 W=100mm", "板厚 t=2mm", "孔径 2a=20mm",
                           "応力集中係数 α=2.5"]):
        ctext(d, 410, 155 + i * 30, s, FT, GRAY, "lm")
    note(d, "最小断面の公称応力を基準に、孔縁の理論最大応力 σmax を求める。")
    save(im, "ver11HoleSetup")


def f_ver_plate():          # 11-2
    im, d = new(); title(d, "周縁固定の円板に一様圧力(たわみの検証)")
    cx, cy = 330, 200; a = 200; th = 26
    # 側面図: 固定端(両側ハッチ)+ 板 + 圧力矢印
    d.rectangle((cx - a, cy - th / 2, cx + a, cy + th / 2), outline=BLACK, width=3, fill=FILL1)
    wall(d, cx - a, cy - th / 2 - 18, cy + th / 2 + 18, side=1)
    wall(d, cx + a, cy - th / 2 - 18, cy + th / 2 + 18, side=-1)
    for i in range(9):
        xx = cx - a + 24 + i * (2 * a - 48) / 8
        arrow(d, xx, cy - th / 2 - 46, xx, cy - th / 2 - 4, BLUE, 2, 9)
    ctext(d, cx, cy - th / 2 - 62, "一様圧力 p = 0.05 MPa", FT, BLUE)
    dim(d, cx - a, cy + th / 2 + 40, cx, cy + th / 2 + 40, "半径 a=400mm")
    ctext(d, cx, cy + 80, "板厚 t=8mm, E=2.0×10⁵MPa, ν=0.3", FT, GRAY)
    note(d, "中央の最大たわみ w_max の理論値(FEM検証の基準)を求める。")
    save(im, "ver11PlateSetup")


if __name__ == "__main__":
    for fn in [f_stress_transform, f_principal, f_pure_shear, f_mises,
               f_rigid_plate_2bars, f_overhang_beam, f_cantilever_udl, f_truss_2bar,
               f_cant_reactions, f_hollow_shaft, f_plate_holes, f_half_heated_bar,
               f_two_bars_thermal, f_cst_setup, f_reaction_beam, f_ver_hole, f_ver_plate]:
        fn()
    print("done")
