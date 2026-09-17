# -*- coding: utf-8 -*-
"""CAE固体2級 第9章 境界条件 図18枚。白地660x420・黒線画で統一。JSONは編集しない。
各図の内容は content/questions/boundary-conditions.json の figureHint に対応。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

# ---------- ローカル補助 ----------
def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=11):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg))
    for i in range(n):
        if i % 2:
            continue
        a, b = i / n, (i + 1) / n
        d.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=col, width=wd)

def rollers_along(d, x0, y0, x1, y1, n=6, off=11, r=5, sidesign=1):
    """辺x0y0-x1y1に沿ってローラー(小円+地線)を描く。sidesign=法線側(+1/-1)。"""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy * sidesign, ux * sidesign
    for i in range(n):
        t = (i + 0.5) / n
        cx = x0 + (x1 - x0) * t + nx * off
        cy = y0 + (y1 - y0) * t + ny * off
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=2)
    d.line((x0 + nx * (off + r), y0 + ny * (off + r),
            x1 + nx * (off + r), y1 + ny * (off + r)), fill=BLACK, width=2)

def moment(d, cx, cy, r=24, col=RED, a0=300, a1=150, label=""):
    """曲がり矢印(モーメント)。a0->a1(screen度)で反時計。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), a1, a0, fill=col, width=4)
    ar = math.radians(a1)
    tx, ty = cx + r * math.cos(ar), cy + r * math.sin(ar)
    tang = ar - math.pi / 2
    for s in (0.6, -0.6):
        d.line((tx, ty, tx - 14 * math.cos(tang - s), ty - 14 * math.sin(tang - s)), fill=col, width=4)
    if label:
        ctext(d, cx, cy, label, FS, col)

def sector(d, cx, cy, r0, r1, a0, a1, fill=None, col=BLACK, wd=3):
    """扇環(annular sector)。角度はscreen度。境界線+内外弧。"""
    if fill:
        pts = []
        steps = 40
        for i in range(steps + 1):
            a = math.radians(a0 + (a1 - a0) * i / steps)
            pts.append((cx + r1 * math.cos(a), cy + r1 * math.sin(a)))
        for i in range(steps + 1):
            a = math.radians(a1 + (a0 - a1) * i / steps)
            pts.append((cx + r0 * math.cos(a), cy + r0 * math.sin(a)))
        d.polygon(pts, fill=fill)
    d.arc((cx - r0, cy - r0, cx + r0, cy + r0), a0, a1, fill=col, width=wd)
    d.arc((cx - r1, cy - r1, cx + r1, cy + r1), a0, a1, fill=col, width=wd)
    for a in (a0, a1):
        ar = math.radians(a)
        d.line((cx + r0 * math.cos(ar), cy + r0 * math.sin(ar),
                cx + r1 * math.cos(ar), cy + r1 * math.sin(ar)), fill=col, width=wd)

def small_pin(d, x, y, s=13):
    d.polygon((x, y, x - s, y + s * 1.4, x + s, y + s * 1.4), outline=BLACK, width=2)
    d.line((x - s - 3, y + s * 1.4, x + s + 3, y + s * 1.4), fill=BLACK, width=2)

def small_roller(d, x, y, s=13):
    yy = y + s * 1.2
    d.polygon((x, y, x - s, yy, x + s, yy), outline=BLACK, width=2)
    for cx in (x - 6, x + 6):
        d.ellipse((cx - 4, yy, cx + 4, yy + 8), outline=BLACK, width=2)
    d.line((x - s - 2, yy + 8, x + s + 2, yy + 8), fill=BLACK, width=2)


# ================= 図1 bc9AnnulusSector =================
def bc9AnnulusSector():
    im, d = new(); title(d, "扇形セクターの傾斜境界条件")
    cx, cy = 250, 330; r0, r1 = 78, 176; a0, a1 = -52, 0   # screen: 0°=+x(A-A), 上向きが負角
    sector(d, cx, cy, r0, r1, a0, a1, fill=FILL1)
    # 内側の分布力p(内弧から外向き=半径方向内→外? 内圧は内面を外へ押す)
    for k in range(5):
        a = math.radians(a0 + (a1 - a0) * (k + 0.5) / 5)
        x1 = cx + (r0 - 20) * math.cos(a); y1 = cy + (r0 - 20) * math.sin(a)
        x2 = cx + r0 * math.cos(a); y2 = cy + r0 * math.sin(a)
        arrow(d, x1, y1, x2, y2, RED, 3, 10)
    ctext(d, cx + 30, cy - 34, "分布力 p", FT, RED, "lm")
    # A-A (x軸上, a=0)
    arrow(d, cx, cy, cx + r1 + 20, cy, GRAY, 2, 10); ctext(d, cx + r1 + 26, cy, "x", FS, GRAY, "lm")
    ctext(d, cx + (r0 + r1) / 2, cy + 20, "A-A", FS, BLACK)
    rollers_along(d, cx + r0, cy, cx + r1, cy, n=4, off=12, r=5, sidesign=1)  # y固定・x自由
    ctext(d, cx + (r0 + r1) / 2 + 4, cy + 44, "y固定・x自由", FT, GRAY)
    # B-B (傾いた境界, a=a1_low)
    ar = math.radians(a0)
    bx0, by0 = cx + r0 * math.cos(ar), cy + r0 * math.sin(ar)
    bx1, by1 = cx + r1 * math.cos(ar), cy + r1 * math.sin(ar)
    ctext(d, (bx0 + bx1) / 2 - 30, (by0 + by1) / 2 - 6, "B-B", FS, BLACK, "rm")
    rollers_along(d, bx0, by0, bx1, by1, n=4, off=12, r=5, sidesign=-1)  # 局所y'拘束
    # 局所座標 x'(境界方向)-y'(法線)
    mx, my = (bx0 + bx1) / 2, (by0 + by1) / 2
    ux, uy = math.cos(ar), math.sin(ar)
    arrow(d, mx, my, mx + 34 * ux, my + 34 * uy, BLUE, 2, 9); ctext(d, mx + 40 * ux, my + 40 * uy, "x'", FT, BLUE)
    arrow(d, mx, my, mx + 34 * uy, my - 34 * ux, BLUE, 2, 9); ctext(d, mx + 40 * uy, my - 40 * ux, "y'", FT, BLUE)
    note(d, "傾斜境界は局所座標x'-y'に変換し x'自由・y'拘束(対称)。余分な点拘束はしない")
    save(im, "bc9AnnulusSector")


# ================= 図2 bc9AntisymBeamFix =================
def bc9AntisymBeamFix():
    im, d = new(); title(d, "反対称荷重を受ける両端固定ばりの1/2モデル")
    # 上:全体
    y = 120; wall(d, 120, y - 22, y + 22, side=1, n=5); wall(d, 540, y - 22, y + 22, side=-1, n=5)
    bar(d, 120, y, 540, y, thick=20)
    arrow(d, 240, y - 4, 240, y - 52, RED, 4, 13); ctext(d, 240, y - 62, "P", FS, RED)
    arrow(d, 420, y + 4, 420, y + 52, RED, 4, 13); ctext(d, 420, y + 62, "P", FS, RED)
    ctext(d, 330, y, "C", FS, BLACK); node(d, 330, y, 6)
    dash(d, 330, y - 60, 330, y + 60, GRAY)
    ctext(d, 330, y - 74, "反対称面(中央C)", FT, GRAY)
    ctext(d, 480, y - 74, "全体:反対称荷重", FT, GRAY)
    # 下:1/2モデル
    y2 = 300; wall(d, 120, y2 - 22, y2 + 22, side=1, n=5); bar(d, 120, y2, 360, y2, thick=20)
    arrow(d, 240, y2 - 4, 240, y2 - 52, RED, 4, 13); ctext(d, 240, y2 - 62, "P", FS, RED)
    node(d, 360, y2, 8); ctext(d, 360, y2 - 24, "C", FS, BLACK)
    # 中央: u=0, v=0, θ自由
    rollers_along(d, 360, y2 - 18, 360, y2 + 18, n=3, off=13, r=5, sidesign=1)
    ctext(d, 420, y2 - 14, "u=0, v=0", FS, BLUE, "lm")
    ctext(d, 420, y2 + 14, "θ 自由", FS, BLUE, "lm")
    ctext(d, 240, y2 + 40, "1/2モデル(左半分)", FT, GRAY)
    note(d, "反対称面では並進u・vを拘束し、面内回転θは自由にする")
    save(im, "bc9AntisymBeamFix")


# ================= 図3 bc9AntisymCenter =================
def bc9AntisymCenter():
    im, d = new(); title(d, "モーメント荷重と反対称境界条件(1/2モデル)")
    # 平面部材:左端固定・他端モーメント。センターライン=縦(y方向)の反対称軸
    x0, x1, yt, yb = 250, 470, 110, 330
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    # センターライン(反対称軸)= x=x0 (左辺)。仕様: 線上節点 u=0。縦線として描く
    cl = x0
    dash(d, cl, yt - 30, cl, yb + 30, RED)
    ctext(d, cl, yt - 42, "センターライン(反対称軸)", FT, RED)
    rollers_along(d, cl, yt, cl, yb, n=6, off=13, r=5, sidesign=-1)
    ctext(d, cl - 60, (yt + yb) / 2, "u=0\n(x拘束)", FS, BLUE, "mm")
    # 他端(右)にモーメント
    moment(d, x1 + 34, (yt + yb) / 2, 26, RED, label="M")
    ctext(d, x1 + 34, (yt + yb) / 2 + 46, "モーメント", FT, RED)
    # 反対称=上下で応力の向きが逆(矢印)
    arrow(d, (x0 + x1) / 2, yt - 8, (x0 + x1) / 2 + 40, yt - 8, ORANGE, 3, 11)
    arrow(d, (x0 + x1) / 2, yb + 8, (x0 + x1) / 2 - 40, yb + 8, ORANGE, 3, 11)
    ctext(d, (x0 + x1) / 2, yb + 30, "上下で応力が逆向き=反対称", FT, ORANGE)
    note(d, "反対称軸上の節点は x方向変位 u=0 を課す(対称と違い法線変位は拘束しない)")
    save(im, "bc9AntisymCenter")


# ================= 図4 bc9AxisymCylBC =================
def bc9AxisymCylBC():
    im, d = new(); title(d, "内圧円筒の軸対称モデルの境界条件")
    # 回転軸z(左), 壁断面矩形(r_in..r_out), 内圧p, 軸方向対称=下端z方向ローラー
    zx = 150
    d.line((zx, 90, zx, 360), fill=BLACK, width=2); dash(d, zx, 70, zx, 90, BLACK)
    ctext(d, zx, 78, "z(回転軸)", FT, BLACK)
    ri, ro, yt, yb = 300, 430, 130, 330
    d.rectangle((ri, yt, ro, yb), outline=BLACK, width=3, fill=FILL1)
    # 内面(左)に内圧pを右向き(外向き)に
    for k in range(4):
        yy = yt + (yb - yt) * (k + 0.5) / 4
        arrow(d, ri - 34, yy, ri, yy, RED, 3, 11)
    ctext(d, ri - 60, (yt + yb) / 2, "内圧 p", FS, RED, "rm")
    # 半径寸法
    dash(d, zx, yb + 16, ri, yb + 16, GRAY); dim(d, zx, yb + 30, ri, yb + 30, "内半径", 0)
    dim(d, ri, yb + 30, ro, yb + 30, "肉厚", 0)
    # 軸方向対称:下端をz方向ローラー(=y方向拘束,半径自由)
    rollers_along(d, ri, yb, ro, yb, n=4, off=12, r=5, sidesign=1)
    ctext(d, (ri + ro) / 2, yb + 54, "下端 z方向拘束(軸対称)", FT, BLUE)
    ctext(d, (ri + ro) / 2, yt - 16, "半径方向は拘束不要", FT, GRAY)
    note(d, "軸対称+軸方向対称:半分高さで下端をz方向拘束。周方向応力で半径方向は自己平衡")
    save(im, "bc9AxisymCylBC")


# ================= 図5 bc9CrackPlateQuarter =================
def bc9CrackPlateQuarter():
    im, d = new(); title(d, "境界条件から解析対象を読み取る")
    x0, x1, yt, yb = 220, 470, 110, 320
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    # 左辺 x拘束
    rollers_along(d, x0, yt, x0, yb, n=6, off=13, r=5, sidesign=-1)
    ctext(d, x0 - 46, (yt + yb) / 2, "x拘束", FT, BLUE, "rm")
    # 下辺:一部(左側=き裂に相当)は自由、残り(右側)をy拘束
    xm = (x0 + x1) / 2
    d.line((x0, yb, xm, yb), fill=RED, width=5)  # き裂に相当(自由)
    ctext(d, (x0 + xm) / 2, yb + 20, "自由(き裂)", FT, RED)
    rollers_along(d, xm, yb, x1, yb, n=3, off=13, r=5, sidesign=1)
    ctext(d, (xm + x1) / 2, yb + 40, "y拘束", FT, BLUE)
    # 上辺 y方向引張
    for k in range(5):
        xx = x0 + (x1 - x0) * (k + 0.5) / 5
        arrow(d, xx, yt, xx, yt - 42, RED, 3, 11)
    ctext(d, xm, yt - 54, "一様引張(y)", FS, RED)
    note(d, "左辺x拘束+下辺の一部だけy拘束(残りは自由)=垂直引張の中央き裂板の1/4モデル")
    save(im, "bc9CrackPlateQuarter")


# ================= 図6 bc9DiscCompress =================
def bc9DiscCompress():
    im, d = new(); title(d, "対向圧縮を受ける円板の1/4モデル")
    # 左:全体イメージ
    cx, cy, r = 165, 220, 78
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL1)
    arrow(d, cx, cy - r - 40, cx, cy - r - 4, RED, 4, 13); ctext(d, cx, cy - r - 52, "P", FS, RED)
    arrow(d, cx, cy + r + 40, cx, cy + r + 4, RED, 4, 13); ctext(d, cx, cy + r + 52, "P", FS, RED)
    ctext(d, cx, cy + r + 74, "全体(対向圧縮)", FT, GRAY)
    # 右:1/4扇(原点=中心)
    ox, oy, R = 400, 320, 150
    sector(d, ox, oy, 0.001, R, -90, 0, fill=FILL1)
    # 上端(=y軸上部,原点直上)に P/2
    arrow(d, ox, oy - R - 42, ox, oy - R - 4, RED, 4, 13); ctext(d, ox + 16, oy - R - 26, "P/2", FS, RED, "lm")
    # 左辺(y軸=縦) x拘束
    rollers_along(d, ox, oy - R, ox, oy, n=5, off=13, r=5, sidesign=-1)
    ctext(d, ox - 50, oy - R / 2, "x拘束", FT, BLUE, "rm")
    # 下辺(x軸=横) y拘束
    rollers_along(d, ox, oy, ox + R, oy, n=5, off=13, r=5, sidesign=1)
    ctext(d, ox + R / 2, oy + 40, "y拘束", FT, BLUE)
    ctext(d, ox + 60, oy - R + 10, "1/4モデル", FT, GRAY, "lm")
    note(d, "直交2軸の対称で1/4化。上端の集中荷重は半分の P/2 を与える")
    save(im, "bc9DiscCompress")


# ================= 図7 bc9DiscCyclic =================
def bc9DiscCyclic():
    im, d = new(); title(d, "対称モデルとして正しくないもの")
    def disc(cx, cy, r, holes, a0=None, a1=None, bad=False):
        if a0 is None:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL1)
        else:
            sector(d, cx, cy, 0.001, r, a0, a1, fill=FILL1)
        for i in range(8):
            a = math.radians(360 * i / 8 - 90)
            hx, hy = cx + r * 0.6 * math.cos(a), cy + r * 0.6 * math.sin(a)
            inside = True
            if a0 is not None:
                deg = (math.degrees(a)) % 360
                lo, hi = a0 % 360, a1 % 360
                inside = (lo <= deg <= hi) if lo <= hi else (deg >= lo or deg <= hi)
            if inside:
                d.ellipse((hx - 7, hy - 7, hx + 7, hy + 7), outline=BLACK, width=2, fill="white")
        if bad:
            d.line((cx - r, cy - r, cx + r, cy + r), fill=RED, width=4)
            d.line((cx - r, cy + r, cx + r, cy - r), fill=RED, width=4)
    disc(150, 150, 52, 8, 180, 360); ctext(d, 150, 215, "半分(π)", FT, BLACK)
    ctext(d, 150, 232, "剛体モード不足=不適", FT, RED)
    d.line((150 - 52, 150, 150 + 52, 150), fill=RED, width=4)
    disc(360, 150, 52, 8, 180, 270); ctext(d, 360, 215, "1/4(π/2) 可", FT, BLACK)
    disc(540, 150, 52, 8, 180, 225); ctext(d, 540, 215, "1/8(π/4) 可", FT, BLACK)
    disc(255, 300, 52, 8, 180, 202.5); ctext(d, 255, 365, "1/16(π/8) 可", FT, BLACK)
    disc(450, 300, 52, 8); ctext(d, 450, 365, "全体(参照)", FT, GRAY)
    note(d, "ピッチπ/4なら1/8等の周期対称は可。半分モデルは並進剛体モードの拘束が不足=不適")
    save(im, "bc9DiscCyclic")


# ================= 図8 bc9DiscretizeRatios =================
def bc9DiscretizeRatios():
    im, d = new(); title(d, "等価節点力の配分比")
    # (a) 4節点物体力 各1/4
    x0, y0 = 120, 130; s = 70
    d.rectangle((x0, y0, x0 + s, y0 + s), outline=BLACK, width=2, fill=FILL1)
    for (cx, cy) in [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]:
        node(d, cx, cy, 6); ctext(d, cx, cy - 16 if cy == y0 else cy + 16, "1/4", FT, BLUE)
    ctext(d, x0 + s / 2, y0 + s + 28, "(a)4節点 物体力", FT, BLACK)
    # (b) 8節点二次 物体力 隅-1/12・中間1/3
    bx, by = 380, 130
    d.rectangle((bx, by, bx + s, by + s), outline=BLACK, width=2, fill=FILL1)
    corners = [(bx, by), (bx + s, by), (bx, by + s), (bx + s, by + s)]
    mids = [(bx + s / 2, by), (bx, by + s / 2), (bx + s, by + s / 2), (bx + s / 2, by + s)]
    for cx, cy in corners:
        node(d, cx, cy, 6); ctext(d, cx, cy - 16 if cy == by else cy + 16, "-1/12", FT, RED)
    for cx, cy in mids:
        node(d, cx, cy, 6)
    ctext(d, bx + s / 2, by + s / 2, "中間 1/3", FT, BLUE)
    ctext(d, bx + s / 2, by + s + 28, "(b)8節点 物体力", FT, BLACK)
    # (c) 2節点辺 1/2:1/2
    cx0, cy0 = 150, 300
    d.line((cx0, cy0, cx0 + 160, cy0), fill=BLACK, width=4)
    for xx, lab in [(cx0, "1/2"), (cx0 + 160, "1/2")]:
        node(d, xx, cy0, 6); ctext(d, xx, cy0 + 20, lab, FT, BLUE)
    ctext(d, cx0 + 80, cy0 - 20, "一様表面力", FT, GRAY)
    ctext(d, cx0 + 80, cy0 + 44, "(c)2節点辺", FT, BLACK)
    # (d) 3節点辺 1/6:2/3:1/6
    dx0, dy0 = 400, 300
    d.line((dx0, dy0, dx0 + 160, dy0), fill=BLACK, width=4)
    for xx, lab in [(dx0, "1/6"), (dx0 + 80, "2/3"), (dx0 + 160, "1/6")]:
        node(d, xx, dy0, 6); ctext(d, xx, dy0 + 20, lab, FT, BLUE)
    ctext(d, dx0 + 80, dy0 + 44, "(d)3節点辺", FT, BLACK)
    note(d, "配分比:2節点辺=1/2:1/2、3節点辺=1/6:2/3:1/6。8節点物体力は隅が負(-1/12)")
    save(im, "bc9DiscretizeRatios")


# ================= 図9 bc9ElementReaction =================
def bc9ElementReaction():
    im, d = new(); title(d, "1要素モデルの反力のつり合い")
    x0, x1, yt, yb = 250, 430, 130, 320
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    for cx, cy in [(x0, yt), (x1, yt), (x0, yb), (x1, yb)]:
        node(d, cx, cy, 6)
    # 上辺に水平力F(→)
    arrow(d, (x0 + x1) / 2 - 30, yt - 16, (x0 + x1) / 2 + 70, yt - 16, RED, 4, 14)
    ctext(d, (x0 + x1) / 2 + 80, yt - 16, "F", FS, RED, "lm")
    # 下隅A,B ピン支持
    small_pin(d, x0, yb + 2); ctext(d, x0 - 18, yb + 8, "A", FS, BLACK, "rm")
    small_pin(d, x1, yb + 2); ctext(d, x1 + 18, yb + 8, "B", FS, BLACK, "lm")
    # 鉛直反力(偶力): Aで上, Bで下
    arrow(d, x0, yb + 46, x0, yb + 90, BLUE, 4, 13); ctext(d, x0, yb + 104, "R↑", FT, BLUE)
    arrow(d, x1, yb + 90, x1, yb + 46, BLUE, 4, 13); ctext(d, x1, yb + 104, "R↓", FT, BLUE)
    dim(d, x0, yb + 130, x1, yb + 130, "幅 b")
    dim(d, x1 + 40, yt, x1 + 40, yb, "高さ H")
    note(d, "水平反力の和=-F。鉛直反力は逆向きの偶力(R=F·H/b)で水平力のモーメントと釣り合う")
    save(im, "bc9ElementReaction")


# ================= 図10 bc9FrameStability =================
def bc9FrameStability():
    im, d = new(); title(d, "剛体モードが拘束されない構造")
    def frame(ox, oy, w, h, left, right, top_rigid, label, unstable):
        # 柱2本+はり。left/right = 'pin'|'roller'|'fix'
        d.line((ox, oy, ox, oy - h), fill=BLACK, width=4)          # 左柱
        d.line((ox + w, oy, ox + w, oy - h), fill=BLACK, width=4)  # 右柱
        d.line((ox, oy - h, ox + w, oy - h), fill=BLACK, width=4)  # はり
        def joint(x, y, kind):
            if kind == 'pin':
                small_pin(d, x, y)
            elif kind == 'roller':
                small_roller(d, x, y)
            else:
                hwall(d, x - 18, x + 18, y, side=1, n=4)
        joint(ox, oy, left); joint(ox + w, oy, right)
        if not top_rigid:
            node(d, ox, oy - h, 6); node(d, ox + w, oy - h, 6)  # ピン接合の隅
        ctext(d, ox + w / 2, oy + 40, label, FT, BLACK)
        if unstable:
            d.line((ox - 6, oy - h - 6, ox + w + 6, oy + 6), fill=RED, width=3)
            d.line((ox - 6, oy + 6, ox + w + 6, oy - h - 6), fill=RED, width=3)
            ctext(d, ox + w / 2, oy + 58, "不安定", FT, RED)
        else:
            ctext(d, ox + w / 2, oy + 58, "安定", FT, GRAY)
    frame(90, 150, 110, 80, 'fix', 'fix', True, "(a)両端固定・剛接", False)
    frame(280, 150, 110, 80, 'pin', 'roller', True, "(b)ピン+ローラー", False)
    frame(470, 150, 110, 80, 'roller', 'roller', True, "(c)両端ローラー", True)
    frame(190, 320, 110, 80, 'pin', 'pin', False, "(d)両端ピン・ピン接合", False)
    frame(400, 320, 110, 80, 'pin', 'roller', False, "(e)ピン接合+ローラー", True)
    note(d, "○=ピン。回転拘束が全く無い(c)(e)は剛体モードが残り不安定")
    save(im, "bc9FrameStability")


# ================= 図11 bc9HolePlateQuarter =================
def bc9HolePlateQuarter():
    im, d = new(); title(d, "円孔板1/4モデルの対称境界条件")
    ox, oy = 230, 330; W2, H2 = 250, 220
    d.rectangle((ox, oy - H2, ox + W2, oy), outline=BLACK, width=3, fill=FILL1)
    # 原点側(左下)に円孔1/4
    rh = 70
    d.pieslice((ox - rh, oy - rh, ox + rh, oy + rh), -90, 0, fill="white", outline=BLACK, width=3)
    ctext(d, ox + rh + 10, oy - rh + 10, "円孔(1/4)", FT, GRAY, "lm")
    # 下辺AB(x軸=対称軸): y固定・x自由
    rollers_along(d, ox + rh, oy, ox + W2, oy, n=4, off=12, r=5, sidesign=1)
    ctext(d, ox + rh, oy + 14, "A", FS, BLACK); ctext(d, ox + W2, oy + 14, "B", FS, BLACK)
    ctext(d, (ox + rh + ox + W2) / 2, oy + 42, "AB: y固定・x自由", FT, BLUE)
    # 左辺DE(y軸=対称軸): x固定・y自由
    rollers_along(d, ox, oy - rh, ox, oy - H2, n=4, off=12, r=5, sidesign=-1)
    ctext(d, ox - 14, oy - rh, "D", FS, BLACK, "rm"); ctext(d, ox - 14, oy - H2, "E", FS, BLACK, "rm")
    ctext(d, ox - 66, (oy - rh + oy - H2) / 2, "DE:\nx固定\ny自由", FT, BLUE, "mm")
    # 上辺 引張
    for k in range(4):
        xx = ox + W2 * (k + 0.5) / 4
        arrow(d, xx, oy - H2, xx, oy - H2 - 40, RED, 3, 11)
    ctext(d, ox + W2 / 2, oy - H2 - 52, "引張", FS, RED)
    note(d, "対称軸上はローラー拘束:AB(x軸)はy固定、DE(y軸)はx固定")
    save(im, "bc9HolePlateQuarter")


# ================= 図12 bc9InclinedMPC =================
def bc9InclinedMPC():
    im, d = new(); title(d, "斜面をスライドする節点のMPC")
    # 45°斜面
    x0, y0 = 180, 340; x1, y1 = 460, 200
    d.line((x0, y0, x1, y1), fill=BLACK, width=4)
    for i in range(9):
        t = i / 9; hx = x0 + (x1 - x0) * t; hy = y0 + (y1 - y0) * t
        d.line((hx, hy, hx + 12, hy + 12), fill=BLACK, width=2)  # 下側ハッチ
    ctext(d, (x0 + x1) / 2 + 30, (y0 + y1) / 2 + 30, "斜面(水平とπ/4)", FT, GRAY, "lm")
    # 節点
    nx, ny = (x0 + x1) / 2, (y0 + y1) / 2
    node(d, nx, ny, 9, fill=RED)
    # 局所座標 x'(斜面方向), y'(法線)
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    px, py = -uy, ux  # 法線(上向き)
    arrow(d, nx, ny, nx + 46 * ux, ny + 46 * uy, BLUE, 3, 11); ctext(d, nx + 56 * ux, ny + 56 * uy, "x'(滑る)", FT, BLUE)
    arrow(d, nx, ny, nx + 46 * px, ny + 46 * py, GREEN, 3, 11); ctext(d, nx + 60 * px, ny + 56 * py, "y'(法線)", FT, GREEN)
    # 全体座標 x,y
    axes(d, 120, 380, 80, 80, "x", "y")
    ctext(d, 330, 110, "法線変位 v'=0  →  MPC:  u − v = 0  (v = u)", FS, RED)
    note(d, "斜面に沿ってのみ移動=法線変位ゼロ。45°では u=v の多点拘束(MPC)を課す")
    save(im, "bc9InclinedMPC")


# ================= 図13 bc9MeshRbmFix =================
def bc9MeshRbmFix():
    im, d = new(); title(d, "解が求まらないときの追加拘束")
    ox, oy = 210, 320; cw = 60; nx, ny = 4, 3
    for i in range(nx + 1):
        d.line((ox + i * cw, oy - ny * cw, ox + i * cw, oy), fill=LGRAY, width=1)
    for j in range(ny + 1):
        d.line((ox, oy - j * cw, ox + nx * cw, oy - j * cw), fill=LGRAY, width=1)
    d.rectangle((ox, oy - ny * cw, ox + nx * cw, oy), outline=BLACK, width=3)
    # 下辺 y方向ローラー
    rollers_along(d, ox, oy, ox + nx * cw, oy, n=5, off=12, r=5, sidesign=1)
    ctext(d, ox + nx * cw / 2, oy + 42, "下辺:y方向拘束", FT, BLUE)
    # 左上節点に荷重Fx,Fy
    lx, ly = ox, oy - ny * cw
    node(d, lx, ly, 7, fill=RED)
    arrow(d, lx, ly, lx + 46, ly, RED, 3, 12); ctext(d, lx + 54, ly - 4, "Fx", FT, RED, "lm")
    arrow(d, lx, ly, lx, ly - 40, RED, 3, 12); ctext(d, lx, ly - 52, "Fy", FT, RED)
    ctext(d, lx + 20, ly - 20, "荷重点(拘束しない)", FT, GRAY, "lm")
    # 追加拘束: 下辺左端の1節点をx方向に
    ax, ay = ox, oy
    d.ellipse((ax - 30 - 6, ay - 6, ax - 30 + 6, ay + 6), outline=GREEN, width=3)
    arrow(d, ax - 30, ay, ax - 4, ay, GREEN, 3, 11)
    ctext(d, ax - 30, ay + 24, "ここをx拘束(追加)", FT, GREEN, "mm")
    ctext(d, ox + nx * cw / 2 + 30, oy - ny * cw - 16, "→ x方向剛体移動が残る", FT, ORANGE)
    note(d, "下辺y拘束だけではx方向剛体移動が残る。荷重点でない1節点をx方向に追加拘束すると解ける")
    save(im, "bc9MeshRbmFix")


# ================= 図14 bc9PressureApply =================
def bc9PressureApply():
    im, d = new(); title(d, "一様分布荷重の与え方")
    # 左:妥当=要素面へ圧力分布荷重
    ox, oy = 120, 200; s = 120
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=2, fill=FILL1)
    for cx, cy in [(ox, oy), (ox + s, oy), (ox, oy + s), (ox + s, oy + s)]:
        node(d, cx, cy, 6)
    for k in range(6):
        xx = ox + s * k / 5
        arrow(d, xx, oy - 40, xx, oy - 4, GREEN, 2, 9)
    ctext(d, ox + s / 2, oy - 54, "圧力(分布)荷重", FS, GREEN)
    ctext(d, ox + s / 2, oy + s + 24, "○ 妥当", FS, GREEN)
    # 右:不適=各節点に等しい集中荷重
    bx = 400
    d.rectangle((bx, oy, bx + s, oy + s), outline=BLACK, width=2, fill=FILL1)
    for cx, cy in [(bx, oy), (bx + s, oy), (bx, oy + s), (bx + s, oy + s)]:
        node(d, cx, cy, 6)
    for xx in (bx, bx + s):
        arrow(d, xx, oy - 40, xx, oy - 4, RED, 3, 11)
    ctext(d, bx + s / 2, oy - 54, "節点に等分集中", FS, RED)
    ctext(d, bx + s / 2, oy + s + 24, "× 端が過小/過大", FS, RED)
    note(d, "一様分布は要素辺へ圧力荷重で与えるのが妥当。節点へ等分だと端節点の配分を誤る")
    save(im, "bc9PressureApply")


# ================= 図15 bc9RigidSlideMPC =================
def bc9RigidSlideMPC():
    im, d = new(); title(d, "剛体を介した荷重のMPC")
    # 下:構造体(台形)、上辺に節点1..4
    bx0, bx1, yb, yt = 200, 480, 330, 230
    d.polygon([(bx0, yb), (bx1, yb), (bx1 - 20, yt), (bx0 + 20, yt)], outline=BLACK, width=3, fill=FILL1)
    hwall(d, bx0 - 20, bx1 + 20, yb, side=1, n=12)
    xs = [bx0 + 30 + i * 70 for i in range(4)]
    for i, xx in enumerate(xs):
        node(d, xx, yt, 7, fill=RED); ctext(d, xx, yt + 16, str(i + 1), FT, BLACK)
    # 上:剛体(バー) y方向にスライド
    ry = yt - 30
    d.rectangle((xs[0] - 20, ry - 16, xs[-1] + 20, ry), outline=BLACK, width=3, fill=FILL3)
    ctext(d, (xs[0] + xs[-1]) / 2, ry - 30, "剛体(y方向にスライド・摩擦無)", FT, GRAY)
    arrow(d, (xs[0] + xs[-1]) / 2, ry - 58, (xs[0] + xs[-1]) / 2, ry - 20, RED, 4, 13)
    ctext(d, (xs[0] + xs[-1]) / 2 + 16, ry - 44, "P", FS, RED, "lm")
    # MPC: 節点2,3,4のy変位=節点1のy変位
    for xx in xs[1:]:
        dash(d, xs[0], yt - 6, xx, yt - 6, BLUE)
    ctext(d, (xs[0] + xs[-1]) / 2, yb + 30, "MPC:  v2 = v3 = v4 = v1  (y方向のみ・x自由)", FS, BLUE)
    note(d, "摩擦無しなのでx方向は自由。上部節点のy変位を1つの節点に一致させるMPCを課す")
    save(im, "bc9RigidSlideMPC")


# ================= 図16 bc9SelfWeightBeam =================
def bc9SelfWeightBeam():
    im, d = new(); title(d, "分割したはりの自重の等価節点力")
    ox, oy = 110, 220; seg = 55; n = 8
    d.rectangle((ox, oy - 26, ox + seg * n, oy + 26), outline=BLACK, width=3, fill=FILL1)
    for i in range(n + 1):
        d.line((ox + i * seg, oy - 26, ox + i * seg, oy + 26), fill=LGRAY, width=1)
    # 支持(単純支持)
    small_pin(d, ox, oy + 26); small_roller(d, ox + seg * n, oy + 26)
    # 各節点に下向き自重: 端=W/32(短), 内部=W/16(長)
    for i in range(n + 1):
        xx = ox + i * seg
        node(d, xx, oy, 5)
        length = 30 if (i == 0 or i == n) else 56
        arrow(d, xx, oy + 30, xx, oy + 30 + length, BLUE, 3, 11)
        if i == 0:
            ctext(d, xx, oy + 30 + length + 14, "W/32", FT, BLUE)
        elif i == 1:
            ctext(d, xx, oy + 30 + length + 14, "W/16", FT, BLUE)
    ctext(d, ox + seg * n / 2, oy - 44, "長さ方向に8等分(4節点一次要素)", FT, GRAY)
    note(d, "内部の共有節点は両隣の要素から配分され端節点(W/32)の2倍=W/16になる")
    save(im, "bc9SelfWeightBeam")


# ================= 図17 bc9ThickCylQuarter =================
def bc9ThickCylQuarter():
    im, d = new(); title(d, "厚肉円筒1/4モデルの内圧の等価節点力")
    ox, oy = 230, 340; r0, r1 = 90, 220
    sector(d, ox, oy, r0, r1, -90, 0, fill=FILL1)
    # 内弧に内圧p(半径方向内→外)
    for k in range(4):
        a = math.radians(-90 + 90 * (k + 0.5) / 4)
        x1 = ox + (r0 - 26) * math.cos(a); y1 = oy + (r0 - 26) * math.sin(a)
        x2 = ox + r0 * math.cos(a); y2 = oy + r0 * math.sin(a)
        arrow(d, x1, y1, x2, y2, RED, 3, 10)
    ctext(d, ox + 40, oy - 40, "内圧 p", FS, RED, "lm")
    # 内弧を8節点二次要素で分割: 隅1/6・中間2/3, 共有隅は2倍(1/3)
    angs = [-90, -60, -30, 0]  # 3ノードで1要素×… ここでは隅3点+中間で図示
    for i, ad in enumerate(angs):
        a = math.radians(ad)
        px, py = ox + r0 * math.cos(a), oy + r0 * math.sin(a)
        node(d, px, py, 6)
        lab = "1/3(共有)" if 0 < i < len(angs) - 1 else "1/6"
        col = ORANGE if 0 < i < len(angs) - 1 else BLUE
        ctext(d, ox + (r0 - 26) * math.cos(a), oy + (r0 - 26) * math.sin(a), lab, FT, col)
    for ad in (-75, -45, -15):
        a = math.radians(ad)
        px, py = ox + r0 * math.cos(a), oy + r0 * math.sin(a)
        node(d, px, py, 5, fill=FILL2)
        ctext(d, ox + (r0 + 22) * math.cos(a), oy + (r0 + 22) * math.sin(a), "2/3", FT, GREEN)
    ctext(d, ox + r1 * 0.7, oy - r1 * 0.7, "1/4モデル", FT, GRAY)
    note(d, "8節点二次要素:内面辺は隅1/6・中間2/3。隣接2要素で共有する隅節点は2倍(1/3)")
    save(im, "bc9ThickCylQuarter")


# ================= 図18 bc9ThreePointBeam =================
def bc9ThreePointBeam():
    im, d = new(); title(d, "三点曲げの境界条件で望ましくないもの")
    # 主図:はり + 中央P + 端A,B支持
    ox, oy = 130, 170; L = 400
    bar(d, ox, oy, ox + L, oy, thick=16)
    node(d, ox, oy, 6); node(d, ox + L, oy, 6); node(d, ox + L / 2, oy, 6)
    ctext(d, ox, oy - 22, "A", FS); ctext(d, ox + L, oy - 22, "B", FS); ctext(d, ox + L / 2, oy - 22, "C", FS)
    arrow(d, ox + L / 2, oy - 54, ox + L / 2, oy - 8, RED, 4, 13); ctext(d, ox + L / 2 + 14, oy - 40, "P", FS, RED, "lm")
    small_pin(d, ox, oy + 8); small_roller(d, ox + L, oy + 8)
    # 悪い例:両端ともローラー(x拘束無し)→横滑り
    y2 = 320; ox2 = 190; L2 = 280
    bar(d, ox2, y2, ox2 + L2, y2, thick=12)
    small_roller(d, ox2, y2 + 6); small_roller(d, ox2 + L2, y2 + 6)
    arrow(d, ox2 + L2 / 2, y2 - 44, ox2 + L2 / 2, y2 - 6, RED, 3, 11)
    arrow(d, ox2 + L2 + 20, y2 - 8, ox2 + L2 + 70, y2 - 8, ORANGE, 3, 12)
    ctext(d, ox2 + L2 + 74, y2 - 8, "横滑り", FT, ORANGE, "lm")
    ctext(d, ox2 + L2 / 2, y2 + 40, "× x方向拘束が無い=剛体的に横滑り(望ましくない)", FT, RED)
    note(d, "三点曲げは片端でx拘束が必要。両端ローラー等でx拘束が無いと剛体移動して解けない")
    save(im, "bc9ThreePointBeam")


if __name__ == "__main__":
    for fn in [bc9AnnulusSector, bc9AntisymBeamFix, bc9AntisymCenter, bc9AxisymCylBC,
               bc9CrackPlateQuarter, bc9DiscCompress, bc9DiscCyclic, bc9DiscretizeRatios,
               bc9ElementReaction, bc9FrameStability, bc9HolePlateQuarter, bc9InclinedMPC,
               bc9MeshRbmFix, bc9PressureApply, bc9RigidSlideMPC, bc9SelfWeightBeam,
               bc9ThickCylQuarter, bc9ThreePointBeam]:
        fn()
    print("=== all 18 bc9 figures done ===")
