# -*- coding: utf-8 -*-
"""固体2級 第9章 9-11/9-16/9-17/9-18/9-27/9-32 の図を提供参考図(ChatGPT作図)を基に作り直す。
白地660x420・figlib共通スタイル・文字=figlib標準・余白圧縮。
★回答前と回答後で同じ「ベース図」を使い、回答後はベースに答えを描き加える(前後で図を変えない)。
 回答前(〜Setup)=ベース+問い / 回答後=ベース+答え。
このファイルが下記キーの単一ソース(旧 figs_bc9.py 等の該当キー定義を上書き):
 bc9SelfWeightBeam(Setup) bc9SymBeam(+Setup新設) bc9AntisymCenter(Setup)
 bc9CrackPlateQuarter(required単一) bc9MeshRbmFix(Setup) bc9MpcBeamPlane(Setup)"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / seg)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg, x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


def roller_h(d, x, y, s=11):
    d.polygon((x, y, x - s * 1.3, y - s, x - s * 1.3, y + s), outline=BLACK, width=2)
    for cy in (y - s * 0.5, y + s * 0.5):
        d.ellipse((x - s * 1.3 - 9, cy - 4, x - s * 1.3, cy + 4), outline=BLACK, width=2)


def moment_arc(d, cx, cy, r, col=RED):
    d.arc((cx - r, cy - r, cx + r, cy + r), -60, 150, fill=col, width=4)
    a = math.radians(-60)
    tx, ty = cx + r * math.cos(a), cy + r * math.sin(a)
    arrow(d, tx - 12, ty - 10, tx, ty, col, 4, 12)


def xmark(d, x, y, s=9, col=RED):
    d.line((x - s, y - s, x + s, y + s), fill=col, width=3); d.line((x + s, y - s, x - s, y + s), fill=col, width=3)


def mesh(d, x0, y0, cw, ch, nc, nr, nodes=True, fill=FILL1):
    for i in range(nr):
        for j in range(nc):
            d.rectangle((x0 + j * cw, y0 + i * ch, x0 + (j + 1) * cw, y0 + (i + 1) * ch), outline=BLACK, width=2, fill=fill)
    if nodes:
        for i in range(nr + 1):
            for j in range(nc + 1):
                node(d, x0 + j * cw, y0 + i * ch, 4, "white")


# ============ 9-11 分割したはりの自重の等価節点力 ============
def _beam8(d, x0, yT, yB, n=8):
    cw = (560 - x0) / n
    for j in range(n):
        d.rectangle((x0 + j * cw, yT, x0 + (j + 1) * cw, yB), outline=BLACK, width=2, fill=(238, 243, 250))
    for i in (yT, yB):
        for j in range(n + 1):
            node(d, x0 + j * cw, i, 4, "white")
    return cw


def _base_selfweight(d):
    title(d, "長さ方向に8分割した単純支持ばり")
    x0, yT, yB, n = 80, 190, 250, 8
    cw = _beam8(d, x0, yT, yB, n)
    for j in range(n):
        cx = x0 + (j + 0.5) * cw
        arrow(d, cx, yT + 10, cx, yB - 8, BLUE, 3, 10)
    pin_support(d, x0, yB); roller_support(d, 560, yB)
    dim(d, x0, 165, 560, 165, "長さ L=1.6m")
    arrow(d, 566, yT, 566, yB, GREEN, 2, 9); arrow(d, 566, yB, 566, yT, GREEN, 2, 9); ctext(d, 574, (yT + yB) / 2, "h=0.25m", FT, GREEN, "lm")
    ctext(d, 300, 286, "自重:鉛直下向き", FT, BLUE)
    ctext(d, 300, 330, "板厚 t=0.02m / ρ=8000kg/m³ / g=10m/s²", FT, GRAY)
    return x0, yT, yB, cw


def f_selfweight_setup():
    im, d = new()
    x0, yT, yB, cw = _base_selfweight(d)
    ix = x0 + 4 * cw
    node(d, ix, yT, 5, "white", RED)
    d.line((ix, yT - 4, ix + 60, 150), fill=RED, width=1); ctext(d, ix + 66, 144, "2要素が共有する内部節点", FT, RED, "lm")
    note(d, "内部節点1個に配分される鉛直自重の等価節点力は?(答えは未記入)")
    save(im, "bc9SelfWeightBeamSetup")


def f_selfweight_after():
    im, d = new()
    x0, yT, yB, cw = _base_selfweight(d)
    node(d, x0, yT, 6, "white", BLUE); ctext(d, x0, yT - 20, "端 20N", FT, BLUE)
    ix = x0 + 4 * cw
    node(d, ix, yT, 6, "white", RED)
    d.line((ix, yT - 4, ix + 50, 150), fill=RED, width=1); ctext(d, ix + 56, 144, "内部 40N (=W/16)", FT, RED, "lm")
    ctext(d, 300, 358, "W=ρgLht=640N / 内部=W/16=40N・端=W/32=20N", FS, BLACK)
    note(d, "共有節点は端の2倍。総重量を節点数で割らない")
    save(im, "bc9SelfWeightBeam")


# ============ 9-16 対称モデルのはり要素拘束 ============
def _dof_symbols(d, nx, ny):
    arrow(d, nx, ny, nx + 56, ny, BLUE, 3, 11); ctext(d, nx + 66, ny, "u", FS, BLUE, "lm")
    arrow(d, nx, ny, nx, ny - 56, RED, 3, 11); ctext(d, nx + 12, ny - 60, "v", FS, RED, "lm")
    d.arc((nx - 34, ny - 34, nx + 34, ny + 34), 150, 260, fill=GREEN, width=3)
    arrow(d, nx - 30, ny - 14, nx - 20, ny - 30, GREEN, 3, 10); ctext(d, nx - 44, ny - 30, "θ", FS, GREEN, "rm")


def _base_symbeam(d):
    title(d, "中央集中荷重の単純支持ばり(対称利用)")
    x0, x1, yb = 110, 560, 135
    d.line((x0, yb, x1, yb), fill=BLACK, width=6)
    pin_support(d, x0, yb); roller_support(d, x1, yb)
    cx = (x0 + x1) / 2
    force(d, cx, yb - 56, 0, 48, "P", RED)
    dash(d, cx, yb + 6, cx, yb + 66, GREEN, 2); ctext(d, cx + 70, yb + 46, "中央の対称面", FT, GREEN, "lm")
    ctext(d, cx, 92, "全体:中央集中荷重の単純支持ばり", FT, GRAY)
    hy = 275
    d.line((x0, hy, cx, hy), fill=BLUE, width=6)
    pin_support(d, x0, hy)
    node(d, cx, hy, 6, "white")
    ctext(d, x0 + 70, hy - 40, "半分をモデル化", FT, BLUE)
    return cx, hy


def f_symbeam_setup():
    im, d = new()
    cx, hy = _base_symbeam(d)
    _dof_symbols(d, cx, hy)
    ctext(d, 300, 358, "u:x方向変位  v:y方向変位  θ:面内回転", FT, GRAY)
    note(d, "対称面上の節点でどの自由度を拘束する?(答えは未記入)")
    save(im, "bc9SymBeamSetup")


def f_symbeam_after():
    im, d = new()
    cx, hy = _base_symbeam(d)
    arrow(d, cx, hy, cx, hy - 52, GREEN, 3, 11); ctext(d, cx + 12, hy - 56, "v 自由", FS, GREEN, "lm")
    arrow(d, cx, hy, cx + 50, hy, RED, 3, 11); xmark(d, cx + 26, hy, 9, RED); ctext(d, cx + 30, hy + 20, "u=0", FS, RED)
    d.arc((cx - 32, hy - 32, cx + 32, hy + 32), 150, 250, fill=RED, width=3); xmark(d, cx - 24, hy - 20, 7, RED); ctext(d, cx - 46, hy - 26, "θ=0", FS, RED, "rm")
    ctext(d, 300, 358, "対称面: u=0, θ=0 を拘束 / たわみ v は自由", FS, BLACK)
    note(d, "対称面を横切る並進と傾く回転を止め、たわみ方向は残す")
    save(im, "bc9SymBeam")


# ============ 9-17 モーメント荷重と反対称境界 ============
def _base_antisym(d):
    title(d, "片端固定・他端モーメントの部材(反対称)")
    x0, x1, yt, yb = 120, 520, 100, 155
    wall(d, x0, yt - 6, yb + 6, side=-1)
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=(238, 243, 250))
    dash(d, x0, (yt + yb) / 2, x1 + 40, (yt + yb) / 2, GREEN, 2)
    moment_arc(d, x1 + 26, (yt + yb) / 2, 26, RED); ctext(d, x1 + 60, (yt + yb) / 2, "M", FS, RED, "lm")
    ctext(d, (x0 + x1) / 2, 84, "全体モデル", FT, GRAY)
    my0, mh = 225, 48
    wall(d, x0, my0 - 6, my0 + mh + 6, side=-1)
    mesh(d, x0, my0, (x1 - x0) / 10, mh, 10, 1)
    dash(d, x0, my0 + mh, x1 + 50, my0 + mh, GREEN, 2)
    axes(d, x1 + 36, my0 + mh, 40, 44, "x", "y")
    ctext(d, (x0 + x1) / 2, 206, "上半分を平面要素でモデル化", FT, BLUE)
    ctext(d, (x0 + x1) / 2, my0 + mh + 18, "センターライン(長手方向・中立軸)", FT, GREEN)
    return x0, x1, my0, mh


def f_antisym_setup():
    im, d = new()
    _base_antisym(d)
    note(d, "センターライン上の節点に課す条件は?(答えは未記入)")
    save(im, "bc9AntisymCenterSetup")


def f_antisym_after():
    im, d = new()
    x0, x1, my0, mh = _base_antisym(d)
    yc = my0 + mh
    for k in (2, 5, 8):
        nx = x0 + k * (x1 - x0) / 10
        node(d, nx, yc, 5, "white", RED)
    ctext(d, (x0 + x1) / 2, 328, "反対称面: 接線 u=0 を拘束 / 法線 v は自由", FS, BLACK)
    note(d, "対称荷重↔法線拘束 / 反対称荷重↔接線拘束。端モーメントは反対称の代表")
    save(im, "bc9AntisymCenter")


# ============ 9-18 境界条件から解析対象を読み取る(required単一) ============
def f_crack_quarter():
    im, d = new(); title(d, "ある平面要素モデルの境界条件")
    px0, py0, pw, ph = 190, 110, 280, 200
    d.rectangle((px0, py0, px0 + pw, py0 + ph), outline=BLACK, width=3, fill=(238, 243, 250))
    for yy in range(py0 + 28, py0 + ph, 44):
        roller_h(d, px0, yy)
    ctext(d, px0 - 52, py0 + ph / 2, "左辺\nx方向拘束", FT, BLUE, "rm")
    for k in range(6):
        fx = px0 + pw * (k + 0.5) / 6
        arrow(d, fx, py0 - 4, fx, py0 - 34, RED, 3, 11)
    ctext(d, px0 + pw / 2, py0 - 48, "上辺:y方向の一様引張", FT, RED)
    midx = px0 + pw * 0.45
    d.line((px0, py0 + ph, midx, py0 + ph), fill=GREEN, width=4)
    ctext(d, (px0 + midx) / 2, py0 + ph + 18, "自由区間", FT, GREEN)
    for xx in [midx + (px0 + pw - midx) * t for t in (0.2, 0.5, 0.8)]:
        roller_support(d, xx, py0 + ph, 12)
    ctext(d, (midx + px0 + pw) / 2, py0 + ph + 40, "下辺の一部:y方向拘束", FT, BLUE)
    axes(d, px0 + pw + 40, py0 + ph - 10, 44, 48, "x", "y")
    note(d, "この境界条件が表す解析対象は?(答えは未記入)")
    save(im, "bc9CrackPlateQuarter")


# ============ 9-27 解が求まらないときの追加拘束 ============
def _rbm_mesh(d, x0, y0, cw, ch, nc, nr):
    mesh(d, x0, y0, cw, ch, nc, nr)
    for j in range(nc + 1):
        roller_support(d, x0 + j * cw, y0 + nr * ch, 12)


def _base_rbm(d):
    title(d, "下辺をy拘束・左上に荷重→解が求まらない")
    x0, y0, cw, ch, nc, nr = 175, 112, 80, 52, 4, 3
    _rbm_mesh(d, x0, y0, cw, ch, nc, nr)
    arrow(d, x0 - 70, y0, x0 - 6, y0, RED, 4, 13); ctext(d, x0 - 80, y0 - 22, "Fx", FS, RED, "rm")
    arrow(d, x0, y0 - 62, x0, y0 - 6, RED, 4, 13); ctext(d, x0 + 20, y0 - 56, "Fy", FS, RED, "lm")
    ctext(d, x0 + nc * cw, y0 - 40, "左上節点に x・y方向荷重", FT, GRAY, "mm")
    ctext(d, x0 + nc * cw / 2, y0 + nr * ch + 38, "下辺の全節点:y方向のみ拘束", FT, BLUE)
    return x0, y0, cw, ch, nc, nr


def f_rbm_setup():
    im, d = new()
    _base_rbm(d)
    note(d, "計算できるようにする追加拘束は?(答えは未記入)")
    save(im, "bc9MeshRbmFixSetup")


def f_rbm_after():
    im, d = new()
    x0, y0, cw, ch, nc, nr = _base_rbm(d)
    bx, by = x0, y0 + nr * ch
    roller_h(d, bx, by)
    d.ellipse((bx - 12, by - 12, bx + 12, by + 12), outline=RED, width=3)
    arrow(d, bx - 62, by - 36, bx - 12, by - 8, RED, 3, 11); ctext(d, bx - 68, by - 44, "x拘束を追加", FT, RED, "rm")
    ctext(d, 330, 360, "不足はx並進1つだけ→最小限で剛体移動を除去(荷重点は拘束しない)", FT, BLACK)
    note(d, "下辺y拘束だけだと横滑り(剛体モード)が残り特異")
    save(im, "bc9MeshRbmFix")


# ============ 9-32 はり要素と平面要素の結合MPC ============
def _base_mpc(d):
    title(d, "はり要素と平面要素の結合(基準節点B・オフセット節点C)")
    by = 262; bx0, Bx = 80, 290
    d.line((bx0, by, Bx, by), fill=BLUE, width=6)
    node(d, Bx, by, 6, "white", BLUE)
    ctext(d, (bx0 + Bx) / 2, by + 24, "2次元はり要素", FT, BLUE)
    ctext(d, Bx, by + 48, "基準節点 B", FT, BLUE)
    mx0, my0, cw2, ch2 = 410, 135, 56, 42
    mesh(d, mx0, my0, cw2, ch2, 4, 2)
    Cx, Cy = mx0, my0 + 2 * ch2
    node(d, Cx, Cy, 6, "white", GREEN)
    ctext(d, mx0 + 2 * cw2, my0 - 14, "平面応力要素", FT, GRAY)
    ctext(d, Cx + 14, Cy - 2, "平面側の節点 C", FT, GREEN, "lm")
    dash(d, Bx, by, Cx, by, GRAY, 2)
    dash(d, Cx, Cy, Cx, by, GREEN, 2)
    arrow(d, Cx - 26, by, Cx - 26, Cy, BLACK, 2, 9); arrow(d, Cx - 26, Cy, Cx - 26, by, BLACK, 2, 9)
    ctext(d, Cx - 38, (by + Cy) / 2, "y", FS, BLACK, "rm")
    axes(d, 95, 150, 40, 44, "x", "y")
    return by, Bx, Cx, Cy


def f_mpc_setup():
    im, d = new()
    by, Bx, Cx, Cy = _base_mpc(d)
    arrow(d, Bx, by, Bx + 50, by, BLUE, 3, 11); ctext(d, Bx + 36, by + 18, "uB", FT, BLUE)
    arrow(d, Bx, by, Bx, by - 52, RED, 3, 11); ctext(d, Bx + 14, by - 54, "vB", FT, RED, "lm")
    d.arc((Bx - 26, by - 4, Bx + 40, by + 52), -10, 150, fill=GREEN, width=3); ctext(d, Bx - 8, by + 40, "θ", FS, GREEN, "rm")
    ctext(d, 330, 352, "θ:z軸まわりの微小回転 / C は B から y 離れた節点", FT, GRAY)
    note(d, "微小変形で節点変位を整合させるMPCは?(答えは未記入)")
    save(im, "bc9MpcBeamPlaneSetup")


def f_mpc_after():
    im, d = new()
    by, Bx, Cx, Cy = _base_mpc(d)
    d.arc((Bx - 26, by - 4, Bx + 40, by + 52), -10, 150, fill=GREEN, width=3); ctext(d, Bx - 8, by + 40, "θ", FS, GREEN, "rm")
    arrow(d, Cx, Cy, Cx - 46, Cy, RED, 3, 11); ctext(d, Cx - 52, Cy - 16, "−yθ", FT, RED, "rm")
    ctext(d, 330, 352, "u = uB − yθ,  v = vB(回転をオフセットで並進に変換)", FS, BLACK)
    note(d, "断面がθ回転→y離れたCは軸方向に −yθ。曲げを連続化")
    save(im, "bc9MpcBeamPlane")


def main():
    f_selfweight_setup(); f_selfweight_after()
    f_symbeam_setup(); f_symbeam_after()
    f_antisym_setup(); f_antisym_after()
    f_crack_quarter()
    f_rbm_setup(); f_rbm_after()
    f_mpc_setup(); f_mpc_after()
    print("done ch9: 11 figures (前後で同一ベース図+答え, 9-18は単一)")


if __name__ == "__main__":
    main()
