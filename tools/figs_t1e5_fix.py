# -*- coding: utf-8 -*-
"""熱流体力学1級 第5章「乱流モデル」レビュー修正図（再生成）。
生成元スクリプト(t1e5*)が消失していたため、公開前レビュー指摘に沿って新規に作図する。
figlibで白地660x420線画。
方針（[[cae-figure-before-after-rule]]）:
  Setup(preFigureImage=回答前) は「条件・与えデータ」だけを中立に描き、答え・導出・結論は描かない。
  本体(figureImage=回答後) は導出・結論（数値・べき乗・壁面値/勾配）まで描く。
対象: 5-2(Cμ), 5-3(壁面漸近), 5-11(温度場BC), 5-12(GGDH・helpful=後のみ)。
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def curve(d, pts, col=BLACK, wd=3):
    d.line(pts, fill=col, width=wd, joint="curve")


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = t; b = min(t + dl, L)
        d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)
        t += dl + gap


def dcurve(d, pts, col=GRAY, wd=2):
    """破線の曲線。"""
    for i in range(len(pts) - 1):
        if i % 2 == 0:
            d.line((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]), fill=col, width=wd)


# ============================================================ 5-2 Cμの評価（局所平衡層）
def _cmu_base(d):
    """壁と局所平衡層(対数層)の模式。共通の下地。"""
    # 壁
    d.rectangle((80, 360, 470, 380), outline=BLACK, width=2, fill=FILL3)
    for x in range(90, 470, 22):
        d.line((x, 380, x - 12, 396), fill=GRAY, width=2)
    ctext(d, 275, 405, "壁面 (y=0)", FT, BLACK)
    # y軸（上向き）
    arrow(d, 80, 360, 80, 80, BLACK, 2, 11)
    ctext(d, 70, 84, "y", FS, BLACK, "rm")
    # 平均速度プロファイル（対数的）
    pts = []
    for yy in range(0, 281, 8):
        u = 150 * (math.log(1 + yy / 12.0) / math.log(1 + 280 / 12.0))
        pts.append((90 + u, 360 - yy))
    curve(d, pts, BLUE, 3)
    ctext(d, 90 + 155, 120, "U(y)", FT, BLUE, "lm")
    # 局所平衡層(対数層)の帯
    dash(d, 80, 250, 470, 250, GRAY, 2)
    dash(d, 80, 170, 470, 170, GRAY, 2)
    ctext(d, 360, 210, "局所平衡層(対数層)", FT, BLACK)


def f_cmu_setup():
    im, d = new()
    title(d, "局所平衡層での定数 Cμ の評価（与件）")
    _cmu_base(d)
    # 与えデータのみ
    box(d, 486, 150, 648, 300, FILL1, BLACK, 2)
    ctext(d, 567, 175, "与えデータ", FS, BLACK)
    ctext(d, 567, 210, "-u'v'/k ≈ 0.3", FT, BLACK)
    ctext(d, 567, 245, "生成 ≈ 散逸", FT, BLACK)
    ctext(d, 567, 268, "Pk ≈ ε", FT, BLACK)
    note(d, "与件のみ。Cμ の値や導出は描かない（回答前）")
    save(im, "t1e5CmuLayerSetup")


def f_cmu():
    im, d = new()
    title(d, "局所平衡層での定数 Cμ の評価（導出）")
    _cmu_base(d)
    box(d, 486, 96, 648, 356, FILL1, BLACK, 2)
    ctext(d, 567, 120, "導出", FS, BLACK)
    lines = [
        "構成則:",
        "-u'v'=Cμ(k²/ε)·∂U/∂y",
        "平衡: Pk=-u'v'·∂U/∂y=ε",
        "⇒ -u'v'/k = √Cμ",
        "√Cμ ≈ 0.3",
        "∴ Cμ=(-u'v'/k)²",
        "   ≈ 0.09",
    ]
    yy = 150
    for i, s in enumerate(lines):
        col = RED if s.startswith("∴") or "0.09" in s else BLACK
        ctext(d, 567, yy + i * 27, s, FT, col)
    save(im, "t1e5CmuLayer")


def box(d, x0, y0, x1, y1, fill=FILL1, col=BLACK, wd=2):  # local (figlib has no box)
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


# ============================================================ 5-3 壁面漸近挙動とνtのべき乗
def _nearwall_axes(d):
    ox, oy = 95, 350
    axes(d, ox, oy, 360, 285, "大きさ", "y")
    ctext(d, ox + 8, oy - 276, "y：壁からの距離", FT, GRAY, "lm")
    return ox, oy


def f_nearwall_setup():
    im, d = new()
    title(d, "壁近傍の速度変動の漸近挙動（与件）")
    ox, oy = _nearwall_axes(d)
    H0 = 270
    # y 上向き。曲線は横軸=大きさ。u'∝y, w'∝y, v'∝y^2
    up = [(ox + 150 * (yy / H0), oy - yy) for yy in range(0, H0 + 1, 6)]          # u'∝y
    wp = [(ox + 105 * (yy / H0), oy - yy) for yy in range(0, H0 + 1, 6)]          # w'∝y
    vp = [(ox + 150 * (yy / H0) ** 2, oy - yy) for yy in range(0, H0 + 1, 6)]     # v'∝y^2
    curve(d, up, BLUE, 3);  ctext(d, ox + 158, oy - H0 + 6, "u' ∝ y", FT, BLUE, "lm")
    curve(d, wp, GREEN, 3); ctext(d, ox + 112, oy - H0 + 30, "w' ∝ y", FT, GREEN, "lm")
    curve(d, vp, RED, 3);   ctext(d, ox + 158, oy - H0 + 54, "v' ∝ y²", FT, RED, "lm")
    note(d, "与件（速度変動の次数）のみ。k・ε・νt の結論は描かない（回答前）")
    save(im, "t1e5NearWallSetup")


def f_nearwall():
    im, d = new()
    title(d, "壁近傍の漸近挙動：k・ε・νt のべき乗（導出）")
    ox, oy = _nearwall_axes(d)
    H0 = 270
    up = [(ox + 120 * (yy / H0), oy - yy) for yy in range(0, H0 + 1, 6)]
    vp = [(ox + 120 * (yy / H0) ** 2, oy - yy) for yy in range(0, H0 + 1, 6)]
    curve(d, up, BLUE, 2);  ctext(d, ox + 126, oy - H0 + 6, "u',w' ∝ y", FT, BLUE, "lm")
    curve(d, vp, RED, 2);   ctext(d, ox + 60, oy - H0 + 34, "v' ∝ y²", FT, RED, "lm")
    # 導出ボックス
    d.rectangle((360, 120, 648, 330), outline=BLACK, width=2, fill=FILL1)
    ctext(d, 504, 144, "壁面漸近（導出）", FS, BLACK)
    rows = [
        "k=½(u'²+v'²+w'²) ∝ y²",
        "ε → 有限（壁面で一定）∝ y⁰",
        "νt=Cμ k²/ε ∝ (y²)²/y⁰",
        "        = y⁴",
    ]
    for i, s in enumerate(rows):
        col = RED if s.strip().startswith("νt") or "y⁴" in s else BLACK
        ctext(d, 504, 178 + i * 34, s, FT, col)
    save(im, "t1e5NearWall")


# ============================================================ 5-11 温度場2方程式モデルの壁面BC
def _plate_base(d):
    """一様熱流束加熱の平板 y=0 と 速度BL・温度BL。"""
    d.rectangle((70, 300, 470, 322), outline=BLACK, width=2, fill=FILL3)
    for x in range(80, 470, 22):
        d.line((x, 322, x - 12, 338), fill=GRAY, width=2)
    ctext(d, 270, 350, "加熱平板 y=0（一様熱流束 q_w）", FT, BLACK)
    # 一様熱流束の上向き矢印
    for x in (120, 200, 280, 360):
        arrow(d, x, 300, x, 268, ORANGE, 2, 9)
    ctext(d, 430, 284, "q_w 一定", FT, ORANGE, "lm")
    # y軸
    arrow(d, 70, 300, 70, 70, BLACK, 2, 11); ctext(d, 60, 74, "y", FS, BLACK, "rm")
    # 速度BLと温度BL（模式の縁）
    vb = [(70 + 150 * (1 - math.exp(-((300 - yy) / 90))), yy) for yy in range(80, 301, 6)]
    tb = [(70 + 195 * (1 - math.exp(-((300 - yy) / 120))), yy) for yy in range(80, 301, 6)]
    dcurve(d, vb, BLUE, 2); ctext(d, 70 + 150, 92, "速度BL", FT, BLUE, "lm")
    dcurve(d, tb, RED, 2);  ctext(d, 70 + 205, 120, "温度BL", FT, RED, "lm")


def f_wallbc_setup():
    im, d = new()
    title(d, "温度場2方程式モデルの壁面境界条件（配置）")
    _plate_base(d)
    note(d, "平板・座標・一様熱流束の配置のみ。k・kθ の分布や式は描かない（回答前）")
    save(im, "t1e5WallBcSetup")


def f_wallbc():
    im, d = new()
    title(d, "壁面境界条件：k と kθ の壁際挙動（回答後）")
    # 左：k のプロファイル（壁で0、∝y²で立ち上がり）
    ox1, oy1 = 90, 350
    axes(d, ox1, oy1, 210, 285, "k", "y")
    H0 = 270
    kp = [(ox1 + 150 * (yy / H0) ** 2, oy1 - yy) for yy in range(0, H0 + 1, 6)]
    curve(d, kp, BLUE, 3)
    ctext(d, ox1 + 60, oy1 - 250, "k ∝ y²", FT, BLUE, "lm")
    node(d, ox1, oy1, 6, RED, RED)
    ctext(d, ox1 + 4, oy1 + 20, "壁面 k=0", FT, RED, "lm")
    # 右：kθ のプロファイル（壁で有限, ∂kθ/∂y=0 → 立ち上がり傾き0）
    ox2, oy2 = 400, 350
    axes(d, ox2, oy2, 210, 285, "kθ", "y")
    # 壁面で kθ0>0, 勾配0（放物線的に増加開始）
    ktp = [(ox2 + 70 + 90 * (yy / H0) ** 2, oy2 - yy) for yy in range(0, H0 + 1, 6)]
    curve(d, ktp, RED, 3)
    node(d, ox2 + 70, oy2, 6, RED, RED)
    dash(d, ox2, oy2, ox2 + 70, oy2, GRAY, 2)          # 壁面値 kθ0
    ctext(d, ox2 + 70, oy2 + 20, "壁面 kθ≠0", FT, RED, "lm")
    # 壁面での接線（水平）＝勾配0を明示
    d.line((ox2 + 40, oy2, ox2 + 150, oy2), fill=GREEN, width=2)
    ctext(d, ox2 + 150, oy2 - 14, "∂kθ/∂y=0", FT, GREEN, "lm")
    save(im, "t1e5WallBc")


# ============================================================ 5-12 GGDHモデル（helpful=回答後のみ）
def f_ggdh():
    im, d = new()
    title(d, "GGDHモデルと壁面漸近：予測次数と必要次数の比較")
    # 上段：主流方向熱流束の有無（渦粘性型 vs GGDH）
    ctext(d, 175, 74, "渦粘性型（勾配拡散）", FS, BLACK)
    box0 = lambda x0, y0, x1, y1, f=FILL1: d.rectangle((x0, y0, x1, y1), outline=BLACK, width=2, fill=f)
    box0(60, 92, 300, 200)
    arrow(d, 80, 150, 180, 150, BLUE, 3, 12); ctext(d, 130, 132, "主流 U", FT, BLUE)
    ctext(d, 180, 176, "u'θ' = 0（表せない）", FT, RED)
    ctext(d, 485, 74, "GGDH", FS, BLACK)
    box0(360, 92, 620, 200)
    arrow(d, 380, 150, 480, 150, BLUE, 3, 12)
    arrow(d, 430, 150, 430, 118, GREEN, 2, 10)
    ctext(d, 500, 176, "u'θ' ≠ 0（表せる）", FT, GREEN)
    # 下段：壁面漸近の次数比較
    d.rectangle((60, 224, 620, 388), outline=BLACK, width=2, fill=FILL1)
    ctext(d, 340, 248, "壁垂直熱流束 v'θ' の壁面漸近（y→0）", FS, BLACK)
    rows = [
        ("一定係数GGDHの予測", "v'θ' ∝ y⁶", RED),
        ("物理的に必要（等温壁）", "v'θ' ∝ y³", BLACK),
        ("物理的に必要（熱流束固定壁）", "v'θ' ∝ y²", BLACK),
    ]
    for i, (lab, order, col) in enumerate(rows):
        yy = 288 + i * 32
        ctext(d, 120, yy, lab, FT, BLACK, "lm")
        ctext(d, 470, yy, order, FT, col, "lm")
    ctext(d, 340, 384, "一定係数のままでは必要な次数に合わない（壁面補正が要る）", FT, RED)
    save(im, "t1e5Ggdh")


if __name__ == "__main__":
    f_cmu_setup(); f_cmu()
    f_nearwall_setup(); f_nearwall()
    f_wallbc_setup(); f_wallbc()
    f_ggdh()
    print("done t1e5_fix (7)")
