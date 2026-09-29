# -*- coding: utf-8 -*-
"""固体2級 公開前レビュー(C): 回答前(preFigureImage)配置図の追加分。
与件(配置/寸法/支持/荷重/材料)のみ。答え・反力・内力・変位・数値結論は描かない。
[[cae-figure-before-after-rule]] 厳命D。既存 figs_s2_prefig.py の続き(重複キーは作らない)。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def f_fixedbar_2mat():      # 2-9
    im, d = new(); title(d, "両端固定・2区間の棒(B点に軸方向荷重)")
    xL, xR, yb, th = 120, 560, 215, 26
    B = xL + 150
    wall(d, xL, yb - th - 24, yb + th + 24, side=1)
    wall(d, xR, yb - th - 24, yb + th + 24, side=-1)
    d.rectangle((xL, yb - th, B, yb + th), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((B, yb - th, xR, yb + th), outline=BLACK, width=3, fill=FILL2)
    node(d, B, yb); ctext(d, B, yb - th - 16, "B", FS, BLACK)
    force(d, B, yb, 66, 0, "P=12kN", RED)
    ctext(d, (xL + B) / 2, yb, "区間1", FT, BLACK)
    ctext(d, (B + xR) / 2, yb, "区間2", FT, BLACK)
    dim(d, xL, yb + th + 30, B, yb + th + 30, "L1=100")
    dim(d, B, yb + th + 30, xR, yb + th + 30, "L2=200")
    ctext(d, (xL + B) / 2, yb + th + 52, "E1=200GPa", FT, GRAY)
    ctext(d, (B + xR) / 2, yb + th + 52, "E2=100GPa", FT, GRAY)
    ctext(d, 340, 120, "断面積 A=100mm²(共通)", FT, GRAY)
    note(d, "両端は剛壁に固定。B点の軸方向変位 δ を求める。")
    save(im, "s2FixedBar2MatSetup")


def f_taper_bar():          # 2-10
    im, d = new(); title(d, "円錐台状の丸棒(軸方向引張)")
    xL, xR, yc, h1, h2 = 150, 520, 210, 70, 34
    wall(d, xL, yc - h1 - 20, yc + h1 + 20, side=1)
    d.polygon([(xL, yc - h1), (xR, yc - h2), (xR, yc + h2), (xL, yc + h1)],
              outline=BLACK, width=3, fill=FILL1)
    dim(d, xL - 28, yc - h1, xL - 28, yc + h1, "d1")
    dim(d, xR + 28, yc - h2, xR + 28, yc + h2, "d2")
    force(d, xR, yc, 70, 0, "P", RED)
    dim(d, xL, yc + h1 + 34, xR, yc + h1 + 34, "L")
    ctext(d, 330, 330, "縦弾性係数 E、直径は d1→d2 に直線変化", FT, GRAY)
    note(d, "軸方向引張荷重 P による全体の伸び δ を求める。")
    save(im, "s2TaperBarSetup")


def f_fbd_setup():          # 2-28
    im, d = new(); title(d, "ピン支持・ローラー支持の両端支持はり")
    def X(m): return 120 + m * (560 - 120) / 4.0
    yb = 210
    d.line((X(0), yb, X(4), yb), fill=BLACK, width=6)
    pin_support(d, X(0), yb); ctext(d, X(0), yb - 22, "ピン(左)", FT, BLACK)
    roller_support(d, X(4), yb); ctext(d, X(4), yb - 22, "ローラー(右)", FT, BLACK)
    force(d, X(2), yb - 64, 0, 56, "荷重(鉛直下向き)", RED)
    note(d, "このはりの正しい自由体図(反力の向きと数)を選ぶ。")
    save(im, "s2FbdSetup")


def f_twolayer_setup():     # 3-5
    im, d = new(); title(d, "二層平板 A|B の界面温度(定常)")
    x0, xm, x1, yt, yb = 190, 340, 490, 135, 295
    d.rectangle((x0, yt, xm, yb), outline=BLACK, width=3, fill=(255, 235, 235))
    d.rectangle((xm, yt, x1, yb), outline=BLACK, width=3, fill=(228, 238, 255))
    ctext(d, (x0 + xm) / 2, (yt + yb) / 2 - 10, "材料A", FS, BLACK)
    ctext(d, (x0 + xm) / 2, (yt + yb) / 2 + 16, "kA=10", FT, GRAY)
    ctext(d, (xm + x1) / 2, (yt + yb) / 2 - 10, "材料B", FS, BLACK)
    ctext(d, (xm + x1) / 2, (yt + yb) / 2 + 16, "kB=20", FT, GRAY)
    ctext(d, x0, yt - 16, "200°C", FS, RED)
    ctext(d, x1, yt - 16, "50°C", FS, BLUE)
    ctext(d, xm, yb + 44, "界面 T=?", FS, BLACK)
    arrow(d, x0 - 44, (yt + yb) / 2, x0 - 6, (yt + yb) / 2, RED, 3, 12)
    dim(d, x0, yb + 22, xm, yb + 22, "0.01m")
    dim(d, xm, yb + 22, x1, yb + 22, "0.01m")
    note(d, "A側200°C・B側50°C。A–B界面の温度を求める(接触熱抵抗は無視)。")
    save(im, "h3TwoLayerSetup")


def f_wallconv_setup():     # 3-12
    im, d = new(); title(d, "対流をともなう壁の外表面温度(定常)")
    xm0, xm1, yt, yb = 305, 375, 135, 300
    d.rectangle((xm0, yt, xm1, yb), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (xm0 + xm1) / 2, (yt + yb) / 2 - 10, "壁", FS, BLACK)
    ctext(d, (xm0 + xm1) / 2, (yt + yb) / 2 + 16, "λ=0.5", FT, GRAY)
    ctext(d, 200, yt - 16, "内側 200°C", FS, RED)
    ctext(d, 200, (yt + yb) / 2, "h_in=10", FT, GRAY)
    for i in range(3): arrow(d, 175, yt + 34 + i * 52, xm0 - 6, yt + 34 + i * 52, RED, 2, 10)
    ctext(d, 500, yt - 16, "外側 20°C", FS, BLUE)
    ctext(d, 500, (yt + yb) / 2, "h_out=5", FT, GRAY)
    for i in range(3): arrow(d, xm1 + 6, yt + 34 + i * 52, xm1 + 40, yt + 34 + i * 52, BLUE, 2, 10)
    ctext(d, (xm0 + xm1) / 2, yb + 20, "外表面 T=?", FT, BLACK)
    dim(d, xm0, yb + 42, xm1, yb + 42, "t=0.1m")
    note(d, "内外の流体温度・熱伝達率が与えられる。壁の外表面温度を求める。")
    save(im, "h3WallConvSetup")


def f_cylconv_setup():      # 3-15
    im, d = new(); title(d, "円管:内側 h1・外側 h2(h2≪h1)")
    cx, cy, r2, r1 = 245, 215, 118, 64
    d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - r1, cy - r1, cx + r1, cy + r1), outline=BLACK, width=3, fill=(255, 238, 238))
    ctext(d, cx, cy, "内側流体", FT, RED)
    d.line((cx, cy, cx + r1, cy), fill=GRAY, width=2); ctext(d, cx + r1 / 2, cy - 12, "r1", FT, GRAY)
    d.line((cx, cy - r1, cx, cy - r2), fill=GRAY, width=2); ctext(d, cx + 12, cy - (r1 + r2) / 2, "r2", FT, GRAY)
    ctext(d, cx, cy - r1 - 16, "管壁", FT, BLACK)
    ctext(d, 430, 150, "内側 h1(大)", FS, GRAY, "lm")
    ctext(d, 430, 190, "外側 h2 ≪ h1", FS, GRAY, "lm")
    ctext(d, 430, 230, "外側流体は低温", FT, GRAY, "lm")
    note(d, "定常で温度低下が最も大きい区間(内側伝達/管壁/外側伝達)はどこか。")
    save(im, "h3CylConvSetup")


def f_pipebc_setup():       # 3-17
    im, d = new(); title(d, "配管の一部を2D(半径×長手)で解析")
    x0, x1, yt, yb = 155, 525, 150, 300
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + x1) / 2, (yt + yb) / 2, "管壁(半径×長手 断面)", FT, BLACK)
    ctext(d, (x0 + x1) / 2, yt - 16, "外面 = 大気(管外)", FS, BLUE)
    ctext(d, (x0 + x1) / 2, yb + 16, "内面 = 高温流体(管内)", FS, RED)
    ctext(d, x0 - 6, (yt + yb) / 2, "長手切断面", FT, GRAY, "rm")
    ctext(d, x1 + 6, (yt + yb) / 2, "長手切断面", FT, GRAY, "lm")
    note(d, "上下面=熱伝達境界。左右の切断面をどう扱うかを含め妥当な境界条件を選ぶ。")
    save(im, "h3PipeBcSetup")


def f_stepbar_setup():      # 4-4
    im, d = new(); title(d, "段付き棒(左端固定・右端に軸方向引張P)")
    xL, xm, xR, yc, t1, t2 = 120, 330, 560, 210, 34, 20
    wall(d, xL, yc - t1 - 20, yc + t1 + 20, side=1)
    d.rectangle((xL, yc - t1, xm, yc + t1), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((xm, yc - t2, xR, yc + t2), outline=BLACK, width=3, fill=FILL2)
    force(d, xR, yc, 64, 0, "P=10kN", RED)
    ctext(d, (xL + xm) / 2, yc, "区間1", FT, BLACK)
    ctext(d, (xm + xR) / 2, yc, "区間2", FT, BLACK)
    dim(d, xL, yc + t1 + 30, xm, yc + t1 + 30, "L1=100")
    dim(d, xm, yc + t1 + 30, xR, yc + t1 + 30, "L2=200")
    ctext(d, (xL + xm) / 2, yc + t1 + 52, "A1=200mm²", FT, GRAY)
    ctext(d, (xm + xR) / 2, yc + t1 + 52, "A2=100mm²", FT, GRAY)
    ctext(d, 340, 120, "E=200GPa（全断面に同じ軸力P）", FT, GRAY)
    note(d, "区間1＋区間2に蓄えられるひずみエネルギーの合計を求める。")
    save(im, "femStepbarSetup")


def f_truss_twobar_setup():  # 4-9
    im, d = new(); title(d, "節点Cから2本の斜め棒(壁へ)・Cに鉛直荷重P")
    cx, cy, LA, LB = 335, 315, 205, 205
    ax = cx - LA * math.cos(math.radians(30)); ay = cy - LA * math.sin(math.radians(30))
    bx = cx + LB * math.cos(math.radians(60)); by = cy - LB * math.sin(math.radians(60))
    bar(d, ax, ay, cx, cy); bar(d, bx, by, cx, cy)
    for (px, py, s) in [(ax, ay, 1), (bx, by, -1)]:
        d.line((px, py - 20, px, py + 20), fill=BLACK, width=3)
        for i in range(4):
            d.line((px, py - 18 + i * 12, px + s * 12, py - 26 + i * 12), fill=BLACK, width=2)
    ctext(d, ax - 16, ay, "A(壁)", FT, BLACK, "rm")
    ctext(d, bx + 16, by, "B(壁)", FT, BLACK, "lm")
    ctext(d, (ax + cx) / 2 - 6, (ay + cy) / 2 - 14, "棒CA", FT, BLUE)
    ctext(d, (bx + cx) / 2 + 8, (by + cy) / 2 - 14, "棒CB", FT, BLUE)
    angle_arc(d, cx, cy, 52, 150, 180, "30°", GRAY)
    angle_arc(d, cx, cy, 52, 0, 60, "60°", GRAY)
    node(d, cx, cy); ctext(d, cx - 16, cy + 8, "C", FT, BLACK, "rm")
    force(d, cx, cy, 0, 62, "P=20kN", RED)
    note(d, "棒CAは水平から30°上方、棒CBは60°上方の壁へ結合。棒CBの軸力を求める。")
    save(im, "f4TrussTwoBarSetup")


def f_springseries_setup():  # 4-22
    im, d = new(); title(d, "直列ばね系(節点1固定→2→3→4)")
    y = 215; nx = [128, 250, 372, 494]
    ks = ["k1=100", "k2=200", "k3=400"]
    wall(d, 128, y - 40, y + 40, side=1)
    for i in range(3):
        spring(d, nx[i] + 10, y, nx[i + 1] - 10, y, coils=5, amp=13)
        ctext(d, (nx[i] + nx[i + 1]) / 2, y - 32, ks[i], FT, BLACK)
    for i, x in enumerate(nx):
        node(d, x, y); ctext(d, x + (14 if i == 0 else 0), y + 26, str(i + 1), FT, BLACK)
    force(d, nx[3], y, 52, 0, "P=800N", RED)
    note(d, "節点4に右向き荷重P。節点3の変位を求める。")
    save(im, "femSpringSeriesSetup")


def f_trussdof_setup():     # 4-28
    im, d = new(); title(d, "5節点2Dトラス(ピン1＋ローラー2)")
    P = {1: (150, 300), 2: (340, 300), 3: (530, 300), 4: (245, 175), 5: (435, 175)}
    for a, b in [(1, 2), (2, 3), (4, 5), (1, 4), (4, 2), (2, 5), (5, 3)]:
        d.line((P[a][0], P[a][1], P[b][0], P[b][1]), fill=BLACK, width=5)
    for i, (x, y) in P.items():
        node(d, x, y, 8); ctext(d, x, y - 22, str(i), F, BLACK)
    pin_support(d, P[1][0], P[1][1] + 8, 22)
    roller_support(d, P[2][0], P[2][1] + 8, 22)
    roller_support(d, P[3][0], P[3][1] + 8, 22)
    ctext(d, P[1][0], P[1][1] + 66, "ピン(2拘束)", FT, GRAY)
    ctext(d, P[2][0], P[2][1] + 66, "ローラー(1拘束)", FT, GRAY)
    ctext(d, P[3][0], P[3][1] + 66, "ローラー(1拘束)", FT, GRAY)
    note(d, "2次元・1節点2自由度。未知(自由)な変位自由度の総数を求める。")
    save(im, "femTrussDofSetup")


def f_thicksolid_setup():   # 5-24
    im, d = new(); title(d, "厚み≒幅≒奥行きの塊(ブロック)")
    iso_box(d, 245, 175, 155, 120, 92)
    ctext(d, 330, 345, "3辺が同程度の寸法(薄板でも細長い棒でもない)", FT, GRAY)
    note(d, "このブロック状構造の応力解析に最も適した要素はどれか。")
    save(im, "femThickSolidSetup")


if __name__ == "__main__":
    for fn in [f_fixedbar_2mat, f_taper_bar, f_fbd_setup, f_twolayer_setup,
               f_wallconv_setup, f_cylconv_setup, f_pipebc_setup, f_stepbar_setup,
               f_truss_twobar_setup, f_springseries_setup, f_trussdof_setup,
               f_thicksolid_setup]:
        fn()
    print("done addC")
