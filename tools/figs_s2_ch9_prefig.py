# -*- coding: utf-8 -*-
"""固体2級 第9章(境界条件)の「回答前(preFigureImage)」配置図 14枚。
白地660x420・黒線画・与件(模型形状/荷重/与えられた軸)のみ。
答え(課す拘束の向き・等価節点力の配分値・MPC関係式・どのモデルが不適か)は一切描かない(=required相当)。
既存 figureImage(答え示唆あり)は回答後(helpful)のまま。JSON配線は別途。
[[cae-figure-before-after-rule]] 厳命D の第9章横展開。"""
import sys, math, os
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


def arc_pts(cx, cy, r, a0, a1, step=4):
    """数学系(反時計回り・右=0°、y上向き)で角度a0->a1の円弧点列(画像座標)。"""
    pts = []; a = a0
    n = max(2, int(abs(a1 - a0) / step))
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(t), cy - r * math.sin(t)))
    return pts


def quarter_annulus(d, cx, cy, r1, r2, a0=0, a1=90):
    inner = arc_pts(cx, cy, r1, a0, a1); outer = arc_pts(cx, cy, r2, a0, a1)
    d.line(inner, fill=BLACK, width=3, joint="curve")
    d.line(outer, fill=BLACK, width=3, joint="curve")
    d.line((inner[0][0], inner[0][1], outer[0][0], outer[0][1]), fill=BLACK, width=3)
    d.line((inner[-1][0], inner[-1][1], outer[-1][0], outer[-1][1]), fill=BLACK, width=3)
    return inner, outer


# ---- 9-4 斜面すべり ----
def f_inclined_slope():
    im, d = new(); title(d, "斜面をスライドする節点(課す境界条件を問う)")
    ax, ay, bx, by = 175, 325, 395, 105           # 斜面(45°)
    d.line((ax, ay, bx, by), fill=BLACK, width=4)
    for i in range(10):                              # 地盤ハッチ(斜面の下側)
        t = i / 10.0; px = ax + (bx - ax) * t; py = ay + (by - ay) * t
        d.line((px, py, px + 16, py + 16), fill=BLACK, width=2)
    nx, ny = (ax + bx) / 2, (ay + by) / 2
    node(d, nx, ny, 8, "white")
    ux, uy = 0.707, -0.707                           # 斜面方向
    arrow(d, nx, ny, nx + 66 * ux, ny + 66 * uy, GRAY, 2, 11); ctext(d, nx + 80 * ux, ny + 80 * uy, "x'", FT, GRAY)
    arrow(d, nx, ny, nx - 60 * 0.707, ny - 60 * 0.707, GRAY, 2, 11); ctext(d, nx - 74 * 0.707, ny - 74 * 0.707, "y'", FT, GRAY)
    arrow(d, nx - 44 * ux, ny - 44 * uy, nx + 54 * ux, ny + 54 * uy, RED, 2, 10)  # スライド方向
    ctext(d, nx + 10, ny + 40, "斜面に沿ってスライド", FT, RED)
    axes(d, 150, 355, 70, 60, "x", "y")
    angle_arc(d, ax, ay, 46, 0, 45, "π/4", GRAY); d.line((ax, ay, ax + 70, ay), fill=GRAY, width=1)
    note(d, "x',y'は斜面に沿う局所座標。この節点に課す境界条件は?")
    save(im, "bc9InclinedSlopeSetup")


# ---- 9-13 厚肉円筒1/4モデルの内圧 ----
def f_thickcyl_quarter():
    im, d = new(); title(d, "厚肉円筒の1/4モデル(内圧の等価節点力を問う)")
    cx, cy, r1, r2 = 200, 330, 110, 215
    inner, outer = quarter_annulus(d, cx, cy, r1, r2)
    for a in range(5, 90, 18):                        # 内圧(内面から外向き)
        t = math.radians(a); px, py = cx + r1 * math.cos(t), cy - r1 * math.sin(t)
        arrow(d, px - 24 * math.cos(t), py + 24 * math.sin(t), px, py, RED, 2, 9)
    ctext(d, cx + 70, cy - 40, "内圧 p", FS, RED)
    for a in (0, 22.5, 45, 67.5, 90):                 # 内面8節点二次要素(隅+中間)
        t = math.radians(a); node(d, cx + r1 * math.cos(t), cy - r1 * math.sin(t), 6, "white")
    for s in ["内面円弧に内圧 p", "内面を8節点", "二次要素で分割"]:
        pass
    ctext(d, 455, 150, "内面円弧を", FT, GRAY, "lm"); ctext(d, 455, 174, "8節点二次要素", FT, GRAY, "lm")
    ctext(d, 455, 198, "で分割", FT, GRAY, "lm")
    note(d, "内圧pを節点に置き換えたときの等価節点力の配分は?")
    save(im, "bc9ThickCylQuarterSetup")


# ---- 9-14 円孔板1/4モデルの対称境界 ----
def f_holeplate_quarter():
    im, d = new(); title(d, "円孔板の1/4対称モデル(各辺の境界条件を問う)")
    ox, oy, w, h = 200, 320, 240, 200
    d.rectangle((ox, oy - h, ox + w, oy), outline=BLACK, width=3, fill=FILL1)
    r = 60; d.pieslice((ox - r, oy - r, ox + r, oy + r), 270, 360, outline=BLACK, width=3, fill="white")
    for xx in (ox + w * 0.45, ox + w * 0.8):          # 上辺に引張
        arrow(d, xx, oy - h + 8, xx, oy - h - 40, RED, 3, 12)
    ctext(d, ox + w * 0.63, oy - h - 56, "引張", FS, RED)
    dash(d, ox - 30, oy, ox + w + 20, oy); ctext(d, ox + w + 40, oy, "AB(x軸)", FT, GRAY, "lm")
    dash(d, ox, oy + 24, ox, oy - h - 10); ctext(d, ox, oy + 40, "DE(y軸)", FT, GRAY)
    ctext(d, ox + r + 22, oy - 20, "円孔(原点)", FT, GRAY, "lm")
    note(d, "下辺AB・左辺DEは対称軸。各辺に課す境界条件は?")
    save(im, "bc9HolePlateQuarterSetup")


# ---- 9-17 モーメント荷重の反対称1/2モデル ----
def f_antisym_center():
    im, d = new(); title(d, "モーメント荷重の1/2モデル(反対称軸の境界条件を問う)")
    ox, oy, w, h = 180, 150, 300, 110
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    wall(d, ox, oy - 6, oy + h + 6, side=-1)          # 左端固定
    ctext(d, ox - 30, oy + h / 2, "固定", FT, GRAY, "rm")
    d.arc((ox + w - 26, oy + h / 2 - 30, ox + w + 34, oy + h / 2 + 30), -70, 70, fill=RED, width=3)
    arrow(d, ox + w + 24, oy + h / 2 - 24, ox + w + 30, oy + h / 2 - 8, RED, 3, 10)
    ctext(d, ox + w + 46, oy + h / 2, "M", FS, RED, "lm")
    dash(d, ox - 10, oy + h, ox + w + 50, oy + h, GRAY, 2)
    ctext(d, ox + w / 2, oy + h + 20, "反対称軸(センターライン)", FT, GRAY)
    note(d, "反対称軸上の節点に課す境界条件は?")
    save(im, "bc9AntisymCenterSetup")


# ---- 9-19 ディスク(8孔)の対称モデル選択 ----
def f_disc_cyclic():
    im, d = new(); title(d, "内圧・8孔ディスク(正しくない対称モデルを問う)")
    cx, cy, R = 320, 225, 150
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), outline=BLACK, width=3, fill="white")
    for a in range(5):                                # 中央内圧(外向き)
        t = math.radians(a * 72); arrow(d, cx + 30 * math.cos(t), cy - 30 * math.sin(t),
                                        cx + 58 * math.cos(t), cy - 58 * math.sin(t), RED, 2, 9)
    ctext(d, cx, cy - 2, "内圧p", FT, RED)
    for k in range(8):                                # ピッチπ/4で8孔
        t = math.radians(k * 45 + 22.5); hx, hy = cx + 100 * math.cos(t), cy - 100 * math.sin(t)
        d.ellipse((hx - 15, hy - 15, hx + 15, hy + 15), outline=BLACK, width=3, fill="white")
    note(d, "ピッチπ/4で8孔。対称性を使うモデルとして正しくないものは?")
    save(im, "bc9DiscCyclicSetup")


# ---- 9-20 扇形セクターの傾斜境界 ----
def f_annulus_sector():
    im, d = new(); title(d, "有孔円板の1セクター(境界A-A・B-Bの条件を問う)")
    cx, cy, r1, r2 = 180, 300, 90, 210
    inner, outer = quarter_annulus(d, cx, cy, r1, r2, 0, 50)
    for a in range(6, 50, 12):                        # 内面に分布力p
        t = math.radians(a); px, py = cx + r1 * math.cos(t), cy - r1 * math.sin(t)
        arrow(d, px - 22 * math.cos(t), py + 22 * math.sin(t), px, py, RED, 2, 9)
    ctext(d, cx + 90, cy - 30, "分布力 p", FS, RED)
    ctext(d, cx + r2 * 0.75, cy + 14, "A-A (x軸上)", FT, GRAY, "lm")
    mt = math.radians(50)
    ctext(d, cx + (r2 + 30) * math.cos(mt), cy - (r2 + 30) * math.sin(mt), "B-B(傾斜)", FT, GRAY, "lm")
    axes(d, cx - 10, cy + 30, 70, 50, "x", "y")
    note(d, "1セクターを取り出す。境界A-A・B-Bに課す条件は?")
    save(im, "bc9AnnulusSectorSetup")


# ---- 9-21 反対称荷重の両端固定ばり1/2 ----
def f_antisym_beamfix():
    im, d = new(); title(d, "反対称荷重の両端固定ばり(中央の境界条件を問う)")
    def X(m): return 110 + m * (550 - 110) / 4.0
    yb = 215
    d.line((X(0), yb, X(4), yb), fill=BLACK, width=5)
    wall(d, X(0), yb - 36, yb + 36, side=-1); ctext(d, X(0) - 26, yb, "固定", FT, GRAY, "rm")
    wall(d, X(4), yb - 36, yb + 36, side=1); ctext(d, X(4) + 26, yb, "固定", FT, GRAY, "lm")
    force(d, X(1.4), yb - 58, 0, 50, "P", RED)         # 逆向き集中力(反対称)
    force(d, X(2.6), yb + 58, 0, -50, "P", RED)
    dash(d, X(2), yb - 70, X(2), yb + 80, GRAY, 2)
    ctext(d, X(2), yb + 96, "中央(反対称面)", FT, GRAY)
    note(d, "中央対称位置で逆向きの集中力。1/2モデルの中央に課す境界条件は?")
    save(im, "bc9AntisymBeamFixSetup")


# ---- 9-22 対向圧縮を受ける円板の1/4モデル ----
def f_disc_compress():
    im, d = new(); title(d, "対向圧縮を受ける円板(1/4モデルの荷重・境界を問う)")
    cx, cy, R = 320, 215, 135
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=3, fill=FILL1)
    arrow(d, cx, cy - R - 46, cx, cy - R - 4, RED, 4, 14); ctext(d, cx + 16, cy - R - 30, "P", FS, RED, "lm")
    arrow(d, cx, cy + R + 46, cx, cy + R + 4, RED, 4, 14); ctext(d, cx + 16, cy + R + 30, "P", FS, RED, "lm")
    dash(d, cx - R - 10, cy, cx + R + 10, cy, GRAY, 2)
    dash(d, cx, cy - R - 10, cx, cy + R + 10, GRAY, 2)
    ctext(d, cx + R * 0.5, cy - R * 0.5, "1/4", FT, GRAY)
    note(d, "上下から対向圧縮P。対称性を使う1/4モデルの荷重と境界条件は?")
    save(im, "bc9DiscCompressSetup")


# ---- 9-27 解が求まらないときの追加拘束 ----
def f_mesh_rbmfix():
    im, d = new(); title(d, "板メッシュ(解が求まらない原因と追加拘束を問う)")
    ox, oy, w, h, nx, ny = 180, 320, 260, 180, 4, 3
    for i in range(ny + 1):
        d.line((ox, oy - i * h / ny, ox + w, oy - i * h / ny), fill=BLACK, width=2)
    for j in range(nx + 1):
        d.line((ox + j * w / nx, oy, ox + j * w / nx, oy - h), fill=BLACK, width=2)
    for j in range(nx + 1):                            # 下辺 y方向ローラー(与件)
        roller_support(d, ox + j * w / nx, oy, 14)
    ctext(d, ox + w / 2, oy + 42, "下辺: y方向ローラー", FT, GRAY)
    force(d, ox - 44, oy - h - 22, 40, 22, "Fx,Fy", RED)  # 左上隅に荷重
    note(d, "下辺はy方向ローラー、左上隅に荷重。解が求まらない。追加すべき拘束は?")
    save(im, "bc9MeshRbmFixSetup")


# ---- 9-29 不整合メッシュのMPC ----
def f_mpc_midnode():
    im, d = new(); title(d, "不整合メッシュ(中点節点に課すMPCを問う)")
    ox, oy, w = 150, 190, 360
    d.rectangle((ox, oy - 90, ox + w, oy), outline=BLACK, width=3, fill=FILL1)   # 粗要素
    n1 = (ox, oy); n3 = (ox + w, oy); n2 = (ox + w / 2, oy)
    d.rectangle((ox + w / 2, oy, ox + w, oy + 90), outline=BLACK, width=3, fill=FILL2)  # 細要素(下・右半分)
    d.rectangle((ox, oy, ox + w / 2, oy + 90), outline=BLACK, width=3, fill=FILL2)
    d.line((ox + w / 2, oy, ox + w / 2, oy + 90), fill=BLACK, width=2)
    for (p, lab, an) in [(n1, "1", "rm"), (n2, "2", "mm"), (n3, "3", "lm")]:
        node(d, p[0], p[1], 7, "white"); ctext(d, p[0] + (0 if lab == "2" else (12 if an == "lm" else -12)), p[1] - 20, lab, FT, BLACK, an)
    ctext(d, ox + w / 2, oy - 110, "粗要素(節点1-3)", FT, GRAY)
    ctext(d, ox + w / 2, oy + 108, "細要素(中点に節点2)", FT, GRAY)
    note(d, "粗要素の辺の中点に細要素の節点2がある。節点2に課すMPCは?")
    save(im, "bc9MpcMidNodeSetup")


# ---- 9-30 剛体を介した荷重のMPC ----
def f_rigidslide_mpc():
    im, d = new(); title(d, "剛体を介して荷重を受ける上部節点(MPCを問う)")
    ox, oy, w, h = 180, 300, 300, 120
    d.rectangle((ox, oy - h, ox + w, oy), outline=BLACK, width=3, fill=FILL1)     # 構造体
    d.rectangle((ox - 10, oy - h - 34, ox + w + 10, oy - h), outline=BLACK, width=3, fill=FILL3)  # 剛体
    ctext(d, ox + w / 2, oy - h - 17, "剛体(y方向にスライド・摩擦なし)", FT, GRAY)
    force(d, ox + w / 2, oy - h - 78, 0, 40, "P", RED)
    for k in range(4):
        px = ox + (k + 0.5) * w / 4; node(d, px, oy - h, 7, "white"); ctext(d, px, oy - h + 18, str(k + 1), FT, BLACK)
    note(d, "上部節点1〜4は剛体を介して荷重Pを受ける。課すMPCは?")
    save(im, "bc9RigidSlideMPCSetup")


# ---- 9-31 斜面をスライドする節点のMPC ----
def f_inclined_mpc():
    im, d = new(); title(d, "斜面をスライドする節点(全体座標でのMPCを問う)")
    ax, ay, bx, by = 175, 325, 395, 105
    d.line((ax, ay, bx, by), fill=BLACK, width=4)
    for i in range(10):
        t = i / 10.0; px = ax + (bx - ax) * t; py = ay + (by - ay) * t
        d.line((px, py, px + 16, py + 16), fill=BLACK, width=2)
    nx, ny = (ax + bx) / 2, (ay + by) / 2; node(d, nx, ny, 8, "white")
    ux, uy = 0.707, -0.707
    arrow(d, nx, ny, nx + 66 * ux, ny + 66 * uy, GRAY, 2, 11); ctext(d, nx + 80 * ux, ny + 80 * uy, "x'", FT, GRAY)
    arrow(d, nx, ny, nx - 60 * 0.707, ny - 60 * 0.707, GRAY, 2, 11); ctext(d, nx - 74 * 0.707, ny - 74 * 0.707, "y'", FT, GRAY)
    axes(d, 150, 355, 70, 60, "x", "y")
    angle_arc(d, ax, ay, 46, 0, 45, "π/4", GRAY); d.line((ax, ay, ax + 70, ay), fill=GRAY, width=1)
    note(d, "斜面(π/4)をスライドする節点。全体座標 u,v で表すMPCは?")
    save(im, "bc9InclinedMPCSetup")


# ---- 9-32 はり要素と平面要素の結合MPC ----
def f_mpc_beamplane():
    im, d = new(); title(d, "はり要素と平面要素の結合(回転を伝えるMPCを問う)")
    by = 170
    bar(d, 150, by, 330, by, thick=0)                 # はり要素
    node(d, 330, by, 8, "white"); ctext(d, 330, by - 22, "はり節点B", FT, BLACK)
    d.rectangle((360, by + 20, 520, by + 150), outline=BLACK, width=3, fill=FILL1)  # 平面要素
    node(d, 360, by + 20, 7, "white")
    dash(d, 330, by, 360, by + 20, GRAY, 2)           # 結合
    dim(d, 345, by, 345, by + 20, "y", 0)
    ctext(d, 440, by + 170, "平面要素(節点はオフセットy)", FT, GRAY)
    note(d, "はり節点Bと平面要素の節点(オフセットy)を結合。回転θを伝えるMPCは?")
    save(im, "bc9MpcBeamPlaneSetup")


# ---- 9-33 長い円管の軸方向境界条件 ----
def f_cyl_axial_mpc():
    im, d = new(); title(d, "長い円管の軸対称モデル(軸方向の境界条件を問う)")
    ox, oy, w, h = 250, 330, 120, 220
    d.rectangle((ox, oy - h, ox + w, oy), outline=BLACK, width=3, fill=FILL1)   # r-z断面
    dash(d, ox - 40, oy - h - 10, ox - 40, oy + 20, GRAY, 2)
    ctext(d, ox - 40, oy + 36, "軸(対称)", FT, GRAY)
    arrow(d, ox - 70, oy, ox - 70, oy - 70, BLACK, 2, 10); ctext(d, ox - 70, oy - 86, "z", FT, BLACK)
    arrow(d, ox - 70, oy, ox - 10, oy, BLACK, 2, 10); ctext(d, ox - 2, oy, "r", FT, BLACK, "lm")
    roller_support(d, ox + w * 0.3, oy, 14); roller_support(d, ox + w * 0.7, oy, 14)
    ctext(d, ox + w / 2, oy + 40, "下端: z方向拘束", FT, GRAY)
    dash(d, ox - 6, oy - h, ox + w + 30, oy - h, GRAY, 2); ctext(d, ox + w + 50, oy - h, "上端", FT, GRAY, "lm")
    note(d, "下端はz拘束。上端を平面に保つための軸方向境界条件は?")
    save(im, "bc9CylAxialMPCSetup")


# ---- 9-15 内圧円筒の軸対称モデル(課す境界条件を問う) ----
def f_axisym_cyl():
    im, d = new(); title(d, "内圧を受ける円筒の軸対称モデル(課す境界条件を問う)")
    # 左:高さ2Lの円筒(実物)。内圧を受ける
    cx, ct, cb, rw = 130, 110, 330, 42
    d.ellipse((cx - rw, ct - 14, cx + rw, ct + 14), outline=BLACK, width=3, fill=FILL1)
    d.line((cx - rw, ct, cx - rw, cb), fill=BLACK, width=3)
    d.line((cx + rw, ct, cx + rw, cb), fill=BLACK, width=3)
    d.arc((cx - rw, cb - 14, cx + rw, cb + 14), 0, 180, fill=BLACK, width=3)
    dash(d, cx, ct - 26, cx, cb + 26, GRAY)           # 回転軸
    for yy in (cb * 0.0 + ct + 55, (ct + cb) / 2, cb - 55):  # 内圧(内側→外向き)
        arrow(d, cx, yy, cx - rw + 6, yy, RED, 2, 9)
        arrow(d, cx, yy, cx + rw - 6, yy, RED, 2, 9)
    ctext(d, cx, cb + 44, "高さ2Lの円筒・内圧p", FT, BLACK)
    dim(d, cx - rw - 26, ct, cx - rw - 26, cb, "2L", 0)
    # 右:取り出す軸対称断面(r-z矩形)。内圧と回転軸のみ。拘束は描かない(=答え)
    zx = 360
    d.line((zx, 95, zx, 360), fill=BLACK, width=2); dash(d, zx, 75, zx, 95, BLACK)
    ctext(d, zx, 84, "z(回転軸)", FT, BLACK)
    ri, ro, yt, yb = 450, 530, 120, 335
    d.rectangle((ri, yt, ro, yb), outline=BLACK, width=3, fill=FILL1)
    for k in range(4):                                 # 内面(左)に内圧p(右向き=外向き)
        yy = yt + (yb - yt) * (k + 0.5) / 4
        arrow(d, ri - 32, yy, ri, yy, RED, 3, 11)
    ctext(d, ri - 54, (yt + yb) / 2, "内圧 p", FT, RED, "rm")
    dim(d, zx, yb + 18, ri, yb + 18, "内半径", 0)
    dim(d, ri, yb + 18, ro, yb + 18, "肉厚", 0)
    dim(d, ro + 24, yt, ro + 24, yb, "2L", 0)
    ctext(d, zx + 30, 100, "r-z断面を軸対称要素で分割", FT, GRAY, "lm")
    note(d, "この断面の節点に課す変位境界条件として適切なものは?(拘束は未記入)")
    save(im, "bc9AxisymCylBCSetup")


# ---- 9-8 1要素モデルの節点反力(反力のつり合いを問う) ----
def f_element_reaction():
    im, d = new(); title(d, "1要素モデルの節点反力(反力のつり合いを問う)")
    x0, x1, yt, yb = 250, 430, 130, 320
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    for cx, cy in [(x0, yt), (x1, yt), (x0, yb), (x1, yb)]:
        node(d, cx, cy, 6)
    arrow(d, (x0 + x1) / 2 - 30, yt - 16, (x0 + x1) / 2 + 70, yt - 16, RED, 4, 14)  # 上辺に水平力F
    ctext(d, (x0 + x1) / 2 + 80, yt - 16, "F", FS, RED, "lm")
    small_pin(d, x0, yb + 2); ctext(d, x0 - 20, yb + 10, "A", FS, BLACK, "rm")
    small_pin(d, x1, yb + 2); ctext(d, x1 + 20, yb + 10, "B", FS, BLACK, "lm")
    dim(d, x1 + 44, yt, x1 + 44, yb, "高さ 2l", 0)
    dim(d, x0, yb + 48, x1, yb + 48, "幅 l", 0)
    note(d, "上辺に水平力F、下隅A・Bをピン支持。各支点の反力のつり合いは?(反力は未記入)")
    save(im, "bc9ElementReactionSetup")


# ---- 9-9 三角形要素の辺ikの線形分布荷重(等価節点力を問う) ----
def f_eq_triload():
    im, d = new(); title(d, "三角形要素の辺ikの線形分布荷重(等価節点力を問う)")
    ix, iy, kx, ky, jx, jy = 180, 300, 480, 300, 350, 150
    d.polygon([(ix, iy), (kx, ky), (jx, jy)], outline=BLACK, width=3, fill=FILL1)
    node(d, ix, iy, 7); ctext(d, ix - 16, iy + 12, "i", FS, BLACK, "rm")
    node(d, kx, ky, 7); ctext(d, kx + 16, ky + 12, "k", FS, BLACK, "lm")
    node(d, jx, jy, 7); ctext(d, jx, jy - 18, "j", FS, BLACK)
    # 辺ik(下辺)に i端0 -> k端P の線形分布荷重(y方向・下向き)。配分値(答え)は描かない
    n = 9
    for m in range(n):
        t = m / (n - 1.0); x = ix + (kx - ix) * t; L = 6 + 52 * t
        arrow(d, x, iy + 8, x, iy + 8 + L, GREEN, 2, 9)
    d.line((ix, iy + 14, kx, iy + 66), fill=GREEN, width=2)   # 強度の三角形包絡線
    ctext(d, ix - 4, iy + 26, "0", FT, GREEN, "rm"); ctext(d, kx + 10, iy + 62, "P", FS, GREEN, "lm")
    dim(d, ix, iy + 84, kx, iy + 84, "辺ik 長さ a", 0)
    note(d, "辺ikにi端0→k端Pの線形分布荷重(y方向)。等価な節点力の配分は?(配分値は未記入)")
    save(im, "bc9EqTriLoadSetup")


# ---- 9-11 単純支持ばりの自重の等価節点力(配分を問う) ----
def f_selfweight_beam():
    im, d = new(); title(d, "単純支持ばりの自重の等価節点力(配分を問う)")
    ox, oy, seg, n = 110, 210, 55, 8
    d.rectangle((ox, oy - 26, ox + seg * n, oy + 26), outline=BLACK, width=3, fill=FILL1)
    for i in range(n + 1):
        d.line((ox + i * seg, oy - 26, ox + i * seg, oy + 26), fill=LGRAY, width=1)
        node(d, ox + i * seg, oy, 5)
    small_pin(d, ox, oy + 26); small_roller(d, ox + seg * n, oy + 26)
    for i in range(n):                                   # 自重=一様下向き(等長=答えを示さない)
        xx = ox + seg * (i + 0.5); arrow(d, xx, oy + 34, xx, oy + 34 + 40, BLUE, 2, 9)
    ctext(d, ox + seg * n / 2, oy + 34 + 56, "自重 ρg(一様・下向き)", FT, BLUE)
    ctext(d, ox + seg * n / 2, oy - 46, "長さ方向に8等分(4節点一次要素)", FT, GRAY)
    ctext(d, ox, oy - 74, "端節点 F_B?", FT, RED); ctext(d, ox + seg, oy - 74, "内部節点 F_A?", FT, RED, "lm")
    note(d, "端節点F_Bと内部(共有)節点F_Aに配分される自重の等価節点力は?(配分値は未記入)")
    save(im, "bc9SelfWeightBeamSetup")


# ---- 9-12 梁モデル上辺への一様分布荷重の与え方を問う ----
def f_pressure_apply():
    im, d = new(); title(d, "梁モデル上辺への一様分布荷重の与え方を問う")
    ox, oy, cw, ch, nc, nr = 120, 170, 68, 70, 5, 2
    for c in range(nc):
        for r in range(nr):
            x = ox + c * cw; y = oy + r * ch
            d.rectangle((x, y, x + cw, y + ch), outline=BLACK, width=2, fill=FILL1)
    W, Hh = nc * cw, nr * ch
    for i in range(nc + 1):                              # 節点
        for r in range(nr + 1):
            node(d, ox + i * cw, oy + r * ch, 4)
    # 左端固定(縦ハッチ)
    d.line((ox, oy, ox, oy + Hh), fill=BLACK, width=4)
    for r in range(nr * 3 + 1):
        yy = oy + r * (Hh / (nr * 3))
        d.line((ox, yy, ox - 16, yy + 14), fill=BLACK, width=2)
    ctext(d, ox - 20, oy + Hh + 18, "左端 固定", FT, BLACK, "lm")
    for r in range(nr + 1):                              # 右端 一様引張(→)
        yy = oy + r * ch; arrow(d, ox + W, yy, ox + W + 44, yy, RED, 3, 11)
    ctext(d, ox + W + 50, oy + Hh / 2, "一様引張", FT, RED, "lm")
    d.line((ox, oy, ox + W, oy), fill=GREEN, width=5)    # 上辺ハイライト
    ctext(d, ox + W / 2, oy - 24, "この上辺に一様分布荷重を与えたい", FT, GREEN)
    note(d, "均等な4節点四辺形要素の梁。上辺への一様分布荷重の妥当な与え方は?(与え方は未記入)")
    save(im, "bc9PressureApplySetup")


def main():
    f_element_reaction(); f_eq_triload(); f_selfweight_beam(); f_pressure_apply()
    f_inclined_slope(); f_thickcyl_quarter(); f_holeplate_quarter(); f_antisym_center()
    f_disc_cyclic(); f_annulus_sector(); f_antisym_beamfix(); f_disc_compress()
    f_mesh_rbmfix(); f_mpc_midnode(); f_rigidslide_mpc(); f_inclined_mpc()
    f_mpc_beamplane(); f_cyl_axial_mpc(); f_axisym_cyl()
    print("done 15 figures")


if __name__ == "__main__":
    main()
