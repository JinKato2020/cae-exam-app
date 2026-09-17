# -*- coding: utf-8 -*-
"""固体力学2級 第11章「結果の検証」の図(ver11*)を描画。
白地660x420・線画・機構のみ・物理的に正確・装飾禁止。豆腐は通常表記へ。"""
import sys, math, os
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def moment_arc(d, cx, cy, r, a0, a1, col=BLUE, wd=3):
    """モーメント弧(a0->a1, 度・数学系反時計回り)+終端矢印。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), -a1, -a0, fill=col, width=wd)
    ae = math.radians(a1)
    ex, ey = cx + r * math.cos(ae), cy - r * math.sin(ae)
    tang = ae + math.pi / 2  # 反時計回りの接線方向
    for s in (0.5, -0.5):
        d.line((ex, ey, ex - 13 * math.cos(tang - s), ey + 13 * math.sin(tang - s)),
               fill=col, width=wd)


# ============================================================
# ver11HoleQtr : 円孔帯板の1/4対称モデル
# ============================================================
def hole_qtr():
    im, d = new(); title(d, "円孔帯板の1/4対称モデル")
    bx, by = 170, 320          # 板中心(=孔中心)=1/4モデルの左下隅
    PW, PH = 300, 210          # 右へ半幅, 上へ半高
    r = 62                     # 孔半径(φ20)
    tx, ty = bx + PW, by - PH
    # 材料外形(左辺=最小断面/対称面, 下辺=対称面, 孔は左下の1/4円)
    d.line((bx + r, by, tx, by), fill=BLACK, width=3)   # 下辺
    d.line((tx, by, tx, ty), fill=BLACK, width=3)       # 右辺
    d.line((tx, ty, bx, ty), fill=BLACK, width=3)       # 上辺
    d.line((bx, ty, bx, by - r), fill=BLACK, width=3)   # 左辺(=最小断面)
    d.arc((bx - r, by - r, bx + r, by + r), 270, 360, fill=BLACK, width=3)  # 孔の1/4
    ctext(d, bx + 22, by - 20, "孔 φ20", FT, GRAY, "lm")
    # 対称面:左辺(ux=0)ローラ
    d.line((bx - 18, ty, bx - 18, by), fill=BLACK, width=2)
    for yy in (ty + 45, (ty + by) / 2, by - r - 22):
        d.ellipse((bx - 15, yy - 6, bx - 3, yy + 6), outline=BLACK, width=2)
    ctext(d, bx - 22, ty - 6, "対称面 ux=0", FT, GRAY, "rm")
    # 対称面:下辺(uy=0)ローラ
    d.line((bx + r, by + 18, tx, by + 18), fill=BLACK, width=2)
    for xx in (bx + r + 40, (bx + r + tx) / 2, tx - 40):
        d.ellipse((xx - 6, by + 3, xx + 6, by + 15), outline=BLACK, width=2)
    ctext(d, (bx + r + tx) / 2, by + 34, "対称面 uy=0", FT, GRAY)
    # 引張(右辺)
    for yy in (ty + 35, (ty + by) / 2, by - 35):
        force(d, tx, yy, 48, 0, "", RED)
    ctext(d, tx + 58, ty + 35, "引張", FT, RED, "lm")
    # 最小断面(左辺の正味断面) sigma_nom
    ctext(d, bx + 8, (ty + (by - r)) / 2, "最小断面\nσnom", FT, BLUE, "lm")
    # 孔縁の応力集中 sigma_max
    arrow(d, bx + 95, by - r - 34, bx + 6, by - r - 2, RED, 2, 10)
    ctext(d, bx + 100, by - r - 38, "σmax = α・σnom (孔縁)", FS, RED, "lm")
    note(d, "対称性より 1/4 のみモデル化。最小断面の孔縁で応力が集中する。")
    save(im, "ver11HoleQtr")


# ============================================================
# ver11CylExtrap : 内表面応力の外挿(内圧円筒・軸対称)
# ============================================================
def cyl_extrap():
    im, d = new(); title(d, "内表面応力の外挿(内圧円筒・軸対称)")
    ox, oy = 150, 340
    axes(d, ox, oy, 430, 250, "内表面からの距離 (mm)", "周方向応力 (MPa)")

    def X(mm): return ox + mm * 20.0            # 0..20mm -> 400px
    def Y(mpa): return oy - (mpa - 30.0) * (240.0 / 16.0)  # 30..46MPa

    # x目盛(0/5/10/15/20)
    for mm in (0, 5, 10, 15, 20):
        d.line((X(mm), oy, X(mm), oy + 5), fill=BLACK, width=2)
        ctext(d, X(mm), oy + 16, str(mm), FT, BLACK)
    # 要素中心応力の2点
    p5 = (X(5), Y(42)); p15 = (X(15), Y(37)); p0 = (X(0), Y(44.5))
    d.line((p5[0], p5[1], p15[0], p15[1]), fill=BLUE, width=3)      # 実測(要素中心)
    dashed(d, p5[0], p5[1], p0[0], p0[1], RED)                     # 外挿
    node(d, p5[0], p5[1], 5, fill="white", col=BLUE)
    node(d, p15[0], p15[1], 5, fill="white", col=BLUE)
    node(d, p0[0], p0[1], 6, fill="white", col=RED)
    ctext(d, p5[0], p5[1] - 18, "42MPa", FT, BLUE)
    ctext(d, p15[0] + 10, p15[1] + 6, "37MPa", FT, BLUE, "lm")
    ctext(d, p0[0] + 8, p0[1] - 14, "外挿 44.5MPa", FS, RED, "lm")
    ctext(d, X(9), oy - 30, "青実線=要素中心の応力(実測), 赤破線=内表面へ外挿", FT, BLUE)
    save(im, "ver11CylExtrap")


# ============================================================
# ver11BeamPos : 荷重位置がずれた単純支持はりの最大たわみ位置
# ============================================================
def beam_pos():
    im, d = new(); title(d, "集中荷重位置と最大たわみ位置(単純支持はり)")
    x0, yb, L = 130, 190, 400
    Ltot, a = 600.0, 200.0
    b = Ltot - a
    ax, bxr = x0, x0 + L

    def PX(mm): return x0 + L * (mm / Ltot)

    # はり
    d.line((ax, yb, bxr, yb), fill=BLACK, width=6)
    pin_support(d, ax, yb)
    roller_support(d, bxr, yb)
    # 荷重 P(左端から200mm)
    lx = PX(a)
    force(d, lx, yb - 78, 0, 62, "P", RED)
    dim(d, ax, yb - 96, lx, yb - 96, "200mm", col=GRAY)
    ctext(d, (ax + bxr) / 2, yb - 96, "", FT)
    # たわみ曲線(実たわみ式・相対値)
    ys = []
    for i in range(0, 121):
        x = Ltot * i / 120.0
        if x <= a:
            w = b * x * (Ltot**2 - b**2 - x**2)
        else:
            xp = Ltot - x
            w = a * xp * (Ltot**2 - a**2 - xp**2)
        ys.append((x, w))
    wmax = max(v for _, v in ys)
    scale = 62.0 / wmax
    pts = [(PX(x), yb + v * scale) for x, v in ys]
    dashed_pts = pts
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 最大たわみ位置(相対値の最大)
    xm = max(ys, key=lambda t: t[1])[0]
    d.line((PX(xm), yb, PX(xm), yb + 62), fill=RED, width=1)
    node(d, PX(xm), yb + 62, 5, fill="white", col=RED)
    # 中央の基準線
    dashed(d, PX(300), yb, PX(300), yb + 70, GRAY)
    ctext(d, PX(300) + 30, yb + 80, "中央", FT, GRAY, "lm")
    ctext(d, PX(xm) - 30, yb + 100, "最大たわみ", FT, RED, "rm")
    note(d, "荷重が中央からずれると、最大たわみ位置も中央からずれる(長い側へ寄る)。")
    save(im, "ver11BeamPos")


# ============================================================
# ver11RigidFBD : 剛体要素による軸力Pの偏心とモーメント(FBD)
# ============================================================
def rigid_fbd():
    im, d = new(); title(d, "剛体要素による軸力Pの偏心 モーメント M = P・a")
    wx, yb = 120, 250
    tipx = 400
    a = 110                       # 偏心量(px)
    # 固定壁 + はり(軸線)
    wall(d, wx, yb - 60, yb + 60, side=-1, n=8)
    bar(d, wx, yb, tipx, yb, thick=26, fill=FILL1)
    dashed(d, wx, yb, 560, yb, GRAY)               # はり軸線
    ctext(d, 560, yb + 4, "はり軸線", FT, GRAY, "lm")
    # 剛体要素(先端から上へ長さ a)
    bar(d, tipx, yb, tipx, yb - a, thick=16, fill=FILL3)
    ctext(d, tipx + 12, yb - a / 2, "剛体要素\n(長さ a)", FT, BLACK, "lm")
    node(d, tipx, yb, 5)
    node(d, tipx, yb - a, 5)
    # 偏心した作用線上の軸力 P(引張)
    dashed(d, wx, yb - a, 560, yb - a, GRAY)        # Pの作用線
    force(d, tipx, yb - a, 75, 0, "P", RED)
    dim(d, tipx + 55, yb, tipx + 55, yb - a, "a", col=GRAY)
    # 等価系(軸線上): 軸力P + モーメントP・a
    force(d, tipx, yb, 62, 0, "P", BLUE)
    moment_arc(d, tipx, yb, 44, 20, 160, BLUE, 3)
    ctext(d, tipx - 8, yb + 40, "M = P・a", FS, BLUE, "mm")
    note(d, "作用線が軸線から a ずれる → 軸力Pは 軸力P + モーメントP・a と等価。")
    save(im, "ver11RigidFBD")


# ============================================================
# ver11WallTemp : 断熱円筒壁の半径方向温度分布(界面で温度の飛び)
# ============================================================
def wall_temp():
    im, d = new(); title(d, "断熱円筒壁の温度分布(界面で温度の飛び)")
    ox, oy = 120, 340
    xin, xi, xout = ox + 30, ox + 230, ox + 430
    # 層の背景
    d.rectangle((xin, oy - 250, xi, oy), fill=(246, 238, 231))
    d.rectangle((xi, oy - 250, xout, oy), fill=(236, 240, 246))
    axes(d, ox, oy, 460, 250, "半径方向位置 r", "温度 T")
    dashed(d, xi, oy, xi, oy - 250, GRAY)
    ctext(d, (xin + xi) / 2, oy - 232, "レンガ層", FT, ORANGE)
    ctext(d, (xi + xout) / 2, oy - 232, "ブロック層", FT, BLUE)
    # 温度折れ線(層で勾配が異なり, 界面で段差)
    y_in, y_bi = oy - 205, oy - 150     # レンガ:内表面->界面(急勾配)
    y_bo, y_out = oy - 110, oy - 40      # ブロック:界面(段差後)->外表面(緩勾配)
    d.line((xin, y_in, xi, y_bi), fill=RED, width=3)
    d.line((xi, y_bo, xout, y_out), fill=RED, width=3)
    dashed(d, xi, y_bi, xi, y_bo, RED)   # 温度の飛び(段差)
    node(d, xin, y_in, 4, fill="white", col=RED)
    node(d, xi, y_bi, 4, fill="white", col=RED)
    node(d, xi, y_bo, 4, fill="white", col=RED)
    node(d, xout, y_out, 4, fill="white", col=RED)
    ctext(d, xin - 6, y_in - 14, "内表面(高温)", FT, GRAY, "lm")
    ctext(d, xout + 6, y_out - 4, "外表面", FT, GRAY, "lm")
    ctext(d, xi + 10, (y_bi + y_bo) / 2, "温度の飛び\n(段差)", FT, RED, "lm")
    save(im, "ver11WallTemp")


# ============================================================
# ver11VVProc : ASME V&V の手順(穴埋め)
# ============================================================
def vv_proc():
    im, d = new(); title(d, "ASME V&V の手順(A・B・C・D を答えよ)")

    def box(cx, cy, w, h, text, letter, fill=FILL1):
        d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                    outline=BLACK, width=3, fill=fill)
        ctext(d, cx, cy, text, FS)
        d.ellipse((cx - w / 2 - 4, cy - h / 2 - 4, cx - w / 2 + 26, cy - h / 2 + 26),
                  outline=RED, width=3, fill="white")
        ctext(d, cx - w / 2 + 11, cy - h / 2 + 11, letter, F, RED)

    ax, ay = 210, 110      # A 数理モデル
    bx, by = 210, 300      # B 計算モデル
    dx, dy = 500, 300      # D 物理(実験)モデル
    box(ax, ay, 200, 66, "数理モデル", "A")
    box(bx, by, 200, 66, "計算モデル", "B")
    box(dx, dy, 210, 66, "物理(実験)モデル", "D")
    # A -> B (検証 C)
    arrow(d, ax, ay + 33, bx, by - 33, BLACK, 3, 14)
    d.ellipse((bx + 8, (ay + by) / 2 - 15, bx + 38, (ay + by) / 2 + 15),
              outline=RED, width=3, fill="white")
    ctext(d, bx + 23, (ay + by) / 2, "C", F, RED)
    ctext(d, bx + 46, (ay + by) / 2, "コード検証・計算(解)の検証", FT, GRAY, "lm")
    # B <-> D (妥当性確認)
    arrow(d, bx + 100, by - 12, dx - 105, dy - 12, BLACK, 3, 13)
    arrow(d, dx - 105, dy + 12, bx + 100, by + 12, BLACK, 3, 13)
    ctext(d, (bx + dx) / 2 - 12, by - 52, "妥当性確認", FT, GRAY)
    ctext(d, (bx + dx) / 2 - 12, by + 52, "(実験と比較)", FT, GRAY)
    note(d, "A→B の一致=検証(Verification), B の結果と D の一致=妥当性確認(Validation)。")
    save(im, "ver11VVProc")


if __name__ == "__main__":
    hole_qtr()
    cyl_extrap()
    beam_pos()
    rigid_fbd()
    wall_temp()
    vv_proc()
    keys = ["ver11HoleQtr", "ver11CylExtrap", "ver11BeamPos",
            "ver11RigidFBD", "ver11WallTemp", "ver11VVProc"]
    miss = [k for k in keys if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(keys), "MISSING", miss)
