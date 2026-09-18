# -*- coding: utf-8 -*-
"""熱流体力学2級 第8章「ポスト処理の基礎」の問題図(接頭辞 t2e8)を14枚描く。
JSON本体は編集しない。white 660x420 線画・機構だけ。ファイル名=figureImage(t2e8Xxx)。
required(回答前表示)には答え・正解値・結論を絶対に描かない([[cae-figure-before-after-rule]])。
required=10問: t2e8CrossSectionAvg, t2e8YplusCheck, t2e8ContinuityDuct, t2e8DragForce,
              t2e8Flow3D, t2e8MassFlow, t2e8ConjugateHeat, t2e8ResultNames,
              t2e8StreamlinePick, t2e8Stagnation
helpful=4問: t2e8Convergence, t2e8EnergyLoss, t2e8ShockWave, t2e8StreamlinePathline
豆腐回避: 特殊記号は使わず rho / un / y+ / u+ / T0 / ^2 / m/s 等の通常表記。日本語ラベルはOK。
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- ローカル補助(ch7と同一書式) --------------------------------
def box(d, cx, cy, w, h, text, fnt=FS, fill="white", oc=BLACK):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=oc, width=3, fill=fill)
    lines = text.split("\n")
    lh = fnt.size + 6
    y0 = cy - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        ctext(d, cx, y0 + i * lh, ln, fnt)


def swirl(d, cx, cy, r, col=BLUE, wd=3, a0=20, a1=320):
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    ae = math.radians(a1); ap = math.radians(a1 - 22)
    ex, ey = cx + r * math.cos(ae), cy + r * math.sin(ae)
    px, py = cx + r * math.cos(ap), cy + r * math.sin(ap)
    arrow(d, px, py, ex, ey, col, wd, 11)


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / dash)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash; b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


def hgrad(d, x0, y0, x1, y1, steps=9, g0=245, g1=150):
    """左→右へ段階的に濃くなる塗り分け(色階調のコンター風)。"""
    for i in range(steps):
        xa = x0 + (x1 - x0) * i / steps
        xb = x0 + (x1 - x0) * (i + 1) / steps
        g = int(g0 + (g1 - g0) * i / max(1, steps - 1))
        d.rectangle((xa, y0, xb, y1), fill=(g, g, g))


# ==================================================================
# 8-1 required : 任意断面を正面から。粗密のある格子・圧力がばらつく。答えは書かない
def f_crosssec():
    im, d = new()
    title(d, "粗密のある格子をもつ任意断面の圧力分布")
    x0, x1, y0, y1 = 150, 560, 90, 330
    # 断面外形
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
    # 圧力がばらつく様子を淡い階調で(左密で高め→右粗で低め等)
    hgrad(d, x0 + 2, y0 + 2, x1 - 1, y1 - 1, 8, 250, 210)
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
    # 縦格子線: 左は密・右は粗(粗密混在)
    xs = []
    x = x0; step = 10.0
    while x < x1 - 4:
        xs.append(x)
        d.line((x, y0, x, y1), fill=LGRAY, width=1)
        x += step; step *= 1.22
    # 横格子線(ほぼ等間隔)
    for k in range(1, 7):
        yy = y0 + (y1 - y0) * k / 7
        d.line((x0, yy, x1, yy), fill=LGRAY, width=1)
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
    # 節点を数点だけ描いて格子点であることを示す
    for xg in xs[::2]:
        for k in range(1, 7):
            yy = y0 + (y1 - y0) * k / 7
            d.ellipse((xg - 2, yy - 2, xg + 2, yy + 2), fill=GRAY)
    ctext(d, x0 + 34, y1 + 22, "密な格子", FT, BLUE)
    ctext(d, x1 - 44, y1 + 22, "粗い格子", FT, BLUE)
    ctext(d, (x0 + x1) / 2, y0 - 10, "任意断面(圧力が場所でばらつく)", FT, GRAY)
    note(d, "格子に粗密がある断面で圧力の平均値をどう求めるか")
    save(im, "t2e8CrossSectionAvg")


# 8-2 required : 壁面近傍を拡大。壁からy・第一格子点・y+の目安。答え(y+分布確認)は書かない
def f_ypluscheck():
    im, d = new()
    title(d, "壁面近傍の第一格子点と壁座標 y+")
    yw = 300
    hwall(d, 90, 470, yw, side=1, n=12)
    ctext(d, 500, yw + 12, "壁面", FT, BLACK, "lm")
    # 壁からの距離yと第一格子点
    px = 250
    node(d, px, yw - 96, 7)
    d.line((px, yw, px, yw - 96), fill=GRAY, width=1)
    dim(d, px + 20, yw, px + 20, yw - 96, "壁からの距離 y", 0, GRAY)
    ctext(d, px, yw - 116, "壁面第一格子点", FT, BLACK)
    # 参考: 対数則が成立する領域の目安を右の横軸に(状況設定)
    ax0, ax1, ay = 300, 600, 380
    arrow(d, ax0, ay, ax1, ay, BLACK, 2, 10)
    ctext(d, ax1 + 4, ay, "y+", FS, BLACK, "lm")
    for xp, lab in [(ax0 + 70, "30"), (ax0 + 170, "100")]:
        d.line((xp, ay - 5, xp, ay + 5), fill=BLACK, width=2)
        ctext(d, xp, ay + 14, lab, FT, GRAY)
    # 対数則の目安帯
    dashed(d, ax0 + 70, ay - 26, ax0 + 170, ay - 26, GRAY, 2, 7)
    ctext(d, ax0 + 120, ay - 40, "対数則が成立する目安", FT, GRAY)
    save(im, "t2e8YplusCheck")


# 8-3 helpful : 残差(対数目盛)の収束履歴 と モニター値が一定に漸近。考え方を示してよい
def f_convergence():
    im, d = new()
    title(d, "収束の確認: 残差の低下 と モニター値の定常化")
    # 左: 残差 vs 反復回数(片対数)
    ox, oy, xl, yl = 90, 320, 210, 210
    axes(d, ox, oy, xl, yl, "反復回数", "残差")
    ctext(d, ox - 8, oy - yl - 4, "(対数目盛)", FT, GRAY, "lm")
    for amp, col, lab in [(1.0, BLUE, "質量"), (0.7, GREEN, "運動量")]:
        pts = []
        for i in range(0, xl - 8, 4):
            v = (yl - 20) * amp * math.exp(-i / 55.0) + 8
            pts.append((ox + i, oy - v))
        plot(d, 0, 0, pts, col, 2)
    ctext(d, ox + xl - 10, oy - 40, "質量", FT, BLUE, "rm")
    ctext(d, ox + xl - 10, oy - 22, "運動量", FT, GREEN, "rm")
    # 収束判定値
    dashed(d, ox, oy - 16, ox + xl, oy - 16, LGRAY, 2, 7)
    ctext(d, ox + 6, oy - 28, "収束判定値", FT, GRAY, "lm")
    # 右: モニター物理量が一定値へ漸近
    ox2, oy2 = 380, 320
    axes(d, ox2, oy2, xl, yl, "反復回数", "モニター値")
    pts = []
    for i in range(0, xl - 8, 4):
        v = (yl - 40) * (1 - math.exp(-i / 45.0)) + 20
        pts.append((ox2 + i, oy2 - v))
    plot(d, 0, 0, pts, RED, 2)
    dashed(d, ox2, oy2 - (yl - 40) - 20, ox2 + xl, oy2 - (yl - 40) - 20, LGRAY, 2, 7)
    ctext(d, ox2 + xl - 6, oy2 - (yl - 40) - 34, "一定値に漸近", FT, GRAY, "rm")
    note(d, "残差が判定値まで低下し・モニター値が変化しなくなれば収束")
    save(im, "t2e8Convergence")


# 8-4 required : 斜視図の流路。入口4cm角(2m/s一様流入)・出口2x4cm。答えの値は書かない
def f_continuity():
    im, d = new()
    title(d, "流路の流入境界と流出境界(連続の式)")
    # 入口(左, 大きい正方形の面)
    ix, iy, iw, ih = 110, 150, 90, 150
    dx, dy = 46, 30
    # 出口(右, 小さい長方形の面)
    ox, oy, ow, oh = 500, 195, 45, 105
    # 側面(入口→出口をつなぐ胴)
    d.polygon([(ix + dx, iy - dy), (ox + dx, oy - dy),
               (ox + dx, oy - dy + oh), (ix + dx, iy - dy + ih)],
              outline=BLACK, width=2, fill=FILL2)                       # 上面
    d.polygon([(ix, iy + ih), (ox, oy + oh),
               (ox + dx, oy - dy + oh), (ix + dx, iy - dy + ih)],
              outline=BLACK, width=2, fill=FILL3)                       # 下面/手前
    # 入口面(正方形)
    d.polygon([(ix, iy), (ix + dx, iy - dy), (ix + dx, iy - dy + ih), (ix, iy + ih)],
              outline=BLACK, width=3, fill=(232, 242, 252))
    # 出口面(長方形)
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + dx, oy - dy + oh), (ox, oy + oh)],
              outline=BLACK, width=3, fill=(232, 242, 252))
    # 入口の一様流入矢印(面に垂直=右奥へ)
    for yy in range(iy + 22, iy + ih - 10, 34):
        arrow(d, ix - 46, yy, ix + 6, yy - 8, BLACK, 2, 9)
    ctext(d, ix - 30, iy - 20, "2 m/s(一様)", FT, BLACK)
    ctext(d, ix + dx / 2, iy + ih + 40, "流入境界\n一辺 4 cm の正方形", FT, BLUE)
    ctext(d, ox + dx / 2, oy + oh + 40, "流出境界\n2 cm x 4 cm", FT, GREEN)
    save(im, "t2e8ContinuityDuct")


# 8-5 required : x-y平面・左から一様流・右に角柱・面に圧力(法線)/せん断(接線)。抗力の答えは書かない
def f_drag():
    im, d = new()
    title(d, "一様流中の角柱に働く圧力とせん断")
    # 座標軸
    ox, oy = 110, 340
    axes(d, ox, oy, 470, 250, "x", "y")
    # 一様流(左から右)
    for yy in range(130, 300, 40):
        arrow(d, 130, yy, 250, yy, BLUE, 2, 11)
    ctext(d, 175, 112, "流れ(一様流 x方向)", FS, BLUE)
    # 角柱(x軸上・右寄り)
    bx, by, bw, bh = 380, 235, 90, 90
    d.rectangle((bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2),
                outline=BLACK, width=3, fill=FILL2)
    ctext(d, bx, by, "角柱", FS, BLACK)
    # 前面に圧力(法線=面に垂直, 左面へ内向き)
    for yy in (by - 26, by, by + 26):
        arrow(d, bx - bw / 2 - 34, yy, bx - bw / 2 - 4, yy, RED, 2, 9)
    ctext(d, bx - bw / 2 - 40, by - 52, "圧力(法線方向)", FT, RED, "mm")
    # 上下面にせん断(接線=面に沿う)
    arrow(d, bx - 26, by - bh / 2 - 6, bx + 26, by - bh / 2 - 6, GREEN, 2, 9)
    arrow(d, bx - 26, by + bh / 2 + 6, bx + 26, by + bh / 2 + 6, GREEN, 2, 9)
    ctext(d, bx + 58, by - bh / 2 - 16, "せん断(接線方向)", FT, GREEN, "lm")
    save(im, "t2e8DragForce")


# 8-6 required : 3次元流れ領域を斜視図・内部に立体的で複雑な流れ。向きを確認したい状況。答えなし
def f_flow3d():
    im, d = new()
    title(d, "3次元の流れ領域(流れの向きを確認したい)")
    ox, oy, w, h, dp = 165, 165, 300, 150, 120
    dx, dy = int(dp * 0.8), int(dp * 0.5)
    # 直方体領域(枠のみ)
    d.polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)],
              outline=BLACK, width=3)
    d.line((ox, oy, ox + dx, oy - dy), fill=BLACK, width=2)
    d.line((ox + w, oy, ox + w + dx, oy - dy), fill=BLACK, width=2)
    d.line((ox + w, oy + h, ox + w + dx, oy + h - dy), fill=BLACK, width=2)
    d.line((ox + dx, oy - dy, ox + w + dx, oy - dy), fill=BLACK, width=2)
    d.line((ox + w + dx, oy - dy, ox + w + dx, oy + h - dy), fill=BLACK, width=2)
    # 内部の立体的で複雑な流れ(曲線+うず)
    cx, cy = ox + w / 2, oy + h / 2
    for k, col in [(0, BLUE), (1, GRAY)]:
        pts = []
        for t in range(0, 210, 6):
            a = math.radians(t)
            r = 20 + t * 0.34
            pts.append((cx - 60 + r * math.cos(a) + k * 30,
                        cy + 20 * math.sin(a * 1.4) - r * 0.18))
        plot(d, 0, 0, pts, col, 2)
    swirl(d, cx + 70, cy - 6, 40, BLUE, 2)
    # 座標三面
    ax, ay = 90, 330
    arrow(d, ax, ay, ax + 44, ay, BLACK, 2, 10); ctext(d, ax + 56, ay, "x", FT, BLACK, "lm")
    arrow(d, ax, ay, ax, ay - 44, BLACK, 2, 10); ctext(d, ax, ay - 56, "y", FT, BLACK)
    arrow(d, ax, ay, ax + 30, ay - 20, BLACK, 2, 10); ctext(d, ax + 40, ay - 26, "z", FT, BLACK, "lm")
    save(im, "t2e8Flow3D")


# 8-7 helpful : 流路距離に沿って全圧が損失分低下・静圧/動圧/全圧の内訳。考え方OK
def f_energyloss():
    im, d = new()
    title(d, "全圧(静圧+動圧)の低下量がエネルギー損失")
    ox, oy, xl, yl = 100, 330, 470, 240
    axes(d, ox, oy, xl, yl, "流路に沿った距離", "圧力")
    # 静圧(下段・ゆるやかに変化), 動圧を積み上げて全圧
    def sp(i):    # 静圧
        return 70 + 18 * math.sin(i / 90.0)
    def dp(i):    # 動圧
        return 60 - 8 * math.sin(i / 90.0)
    loss = 55.0
    ps, pt = [], []
    for i in range(0, xl - 10, 6):
        s = sp(i)
        tot = s + dp(i) - loss * (i / (xl - 10))   # 全圧は損失分だけ低下
        ps.append((ox + i, oy - s))
        pt.append((ox + i, oy - tot))
    plot(d, 0, 0, ps, GREEN, 2)
    plot(d, 0, 0, pt, RED, 3)
    ctext(d, ox + xl - 8, oy - sp(xl - 10) - 4, "静圧", FT, GREEN, "rm")
    ctext(d, ox + 60, oy - (sp(0) + dp(0)) - 8, "全圧(静圧+動圧)", FT, RED, "lm")
    # 入口と出口の全圧差=損失
    xin, xout = ox + 6, ox + xl - 16
    tin = sp(0) + dp(0)
    tout = sp(xl - 10) + dp(xl - 10) - loss
    dashed(d, xin, oy - tin, xout + 10, oy - tin, LGRAY, 2, 6)
    dim(d, xout, oy - tin, xout, oy - tout, "損失", 0, GRAY)
    ctext(d, xout + 40, oy - (tin + tout) / 2, "全圧差\n=エネルギー損失", FT, GRAY, "lm")
    save(im, "t2e8EnergyLoss")


# 8-8 required : 流出口の境界面を斜視図・un・rho・A のラベル。質量流量の答えは書かない
def f_massflow():
    im, d = new()
    title(d, "流出口の境界面を通過する質量流量")
    # 斜視図の面(平行四辺形)
    ox, oy = 240, 150
    w, h = 150, 170
    dx, dy = 70, 42
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + dx, oy - dy + h), (ox, oy + h)],
              outline=BLACK, width=3, fill=(236, 236, 236))
    ctext(d, ox + dx / 2, oy - dy + h / 2, "流出口\n面積 A", FS, BLACK)
    # 面に垂直な速度 un(面の法線方向=右手前へ)
    fx, fy = ox + dx / 2, oy - dy / 2 + h / 2
    arrow(d, fx, fy, fx + 95, fy + 26, RED, 4, 15)
    ctext(d, fx + 108, fy + 30, "un(面に垂直)", FS, RED, "lm")
    # 密度ラベル
    ctext(d, ox - 12, oy + h + 24, "密度 rho", FS, BLUE, "lm")
    note(d, "面に垂直な速度 un ・密度 rho ・面積 A から質量流量を評価する")
    save(im, "t2e8MassFlow")


# 8-9 helpful : 超音速物体まわりで圧力等値線が衝撃波位置に密集。概念を示してよい
def f_shockwave():
    im, d = new()
    title(d, "衝撃波の位置に密集する圧力(密度)等値線")
    # 流入(超音速)
    for yy in (150, 210, 270):
        arrow(d, 70, yy, 140, yy, GRAY, 2, 10)
    ctext(d, 105, 128, "M > 1", FT, GRAY)
    # 物体(くさび/ノーズ, 右向き)
    nx, ny = 330, 210
    d.polygon([(nx, ny), (nx + 150, ny - 40), (nx + 150, ny + 40)],
              outline=BLACK, width=3, fill=FILL2)
    ctext(d, nx + 100, ny, "物体", FT, BLACK)
    # 弓状衝撃波: ノーズ前方に等値線が密集(何本かの弧)
    for k, off in enumerate([0, 10, 20, 46, 78]):
        r = 120 + off
        cxx = nx + 40 + off
        # 前方に凸の弧
        d.arc((cxx - r, ny - r, cxx + r, ny + r), 118, 242, fill=RED, width=2)
    ctext(d, nx - 70, ny - 96, "等値線が密集\n=衝撃波", FT, RED)
    arrow(d, nx - 40, ny - 60, nx - 6, ny - 30, RED, 2, 10)
    note(d, "圧力・密度が急変する所ほど等値線が密になり衝撃波が浮かぶ")
    save(im, "t2e8ShockWave")


# 8-10 required : 発熱固体(ハッチ)と接する流体を含む断面。熱が固体→流体へ。答え(不適切な処理)は書かない
def f_conjugate():
    im, d = new()
    title(d, "発熱する固体と接する流体の熱伝達")
    # 下半分=発熱する固体(ハッチ), 上半分=流体
    x0, x1 = 120, 560
    ymid = 250; ytop = 110; ybot = 340
    # 流体領域(上)
    d.rectangle((x0, ytop, x1, ymid), outline=BLACK, width=2)
    ctext(d, x0 + 60, ytop + 20, "流体", FS, BLUE, "lm")
    # 流体の流れ矢印
    for yy in range(ytop + 26, ymid - 8, 34):
        arrow(d, x0 + 8, yy, x0 + 70, yy, BLUE, 2, 9)
    # 固体領域(下, ハッチング)
    d.rectangle((x0, ymid, x1, ybot), outline=BLACK, width=3, fill=FILL2)
    for xx in range(x0, x1, 16):
        d.line((xx, ybot, min(xx + 24, x1), ymid), fill=LGRAY, width=1)
    d.rectangle((x0, ymid, x1, ybot), outline=BLACK, width=3)
    ctext(d, x0 + 90, ybot - 20, "発熱する固体", FS, RED, "lm")
    # 界面を通って固体→流体へ熱(上向き矢印)
    for xx in range(x0 + 50, x1 - 20, 70):
        arrow(d, xx, ymid + 4, xx, ymid - 40, RED, 3, 11)
    ctext(d, (x0 + x1) / 2, ymid + 4, "固体→流体へ熱が伝わる", FT, RED)
    save(im, "t2e8ConjugateHeat")


# 8-11 required : 管3つ (a)そろった矢印 (b)左右で階調変化 (c)平行線。ラベル(a)(b)(c)のみ・名称は書かない
def f_resultnames():
    im, d = new()
    title(d, "管内流れの3種類の結果処理図(a)(b)(c)")
    x0, x1 = 150, 560
    ys = [92, 200, 308]
    hh = 66
    # (a) そろった右向き矢印が並ぶ
    ya = ys[0]
    d.rectangle((x0, ya, x1, ya + hh), outline=BLACK, width=2)
    for xx in range(x0 + 24, x1 - 20, 48):
        for yy in range(ya + 16, ya + hh - 8, 22):
            arrow(d, xx, yy, xx + 30, yy, BLACK, 2, 8)
    ctext(d, x0 - 12, ya + hh / 2, "(a)", FS, BLACK, "rm")
    # (b) 左→右で段階的に色階調が変化する塗り分け
    yb = ys[1]
    hgrad(d, x0, yb, x1, yb + hh, 9, 245, 150)
    d.rectangle((x0, yb, x1, yb + hh), outline=BLACK, width=2)
    ctext(d, x0 - 12, yb + hh / 2, "(b)", FS, BLACK, "rm")
    # (c) 管軸に平行な水平線が複数本
    yc = ys[2]
    d.rectangle((x0, yc, x1, yc + hh), outline=BLACK, width=2)
    for k in range(1, 6):
        yy = yc + hh * k / 6
        d.line((x0 + 6, yy, x1 - 6, yy), fill=BLACK, width=2)
    ctext(d, x0 - 12, yc + hh / 2, "(c)", FS, BLACK, "rm")
    save(im, "t2e8ResultNames")


# 8-12 required : 図1=L字領域+4境界の相対圧, 図2=静圧/流速の等値線図。条件提示のみ・正解の流線は描かない
def f_streamlinepick():
    im, d = new()
    title(d, "図1 凸型領域の圧力境界条件 と 図2 静圧・流速分布")
    # --- 図1: L字(凸型)領域 ---
    # L字ポリゴン
    ax, ay = 60, 120
    P = [(ax, ay), (ax + 150, ay), (ax + 150, ay + 90),
         (ax + 250, ay + 90), (ax + 250, ay + 200),
         (ax, ay + 200)]
    d.polygon(P, outline=BLACK, width=3, fill=(248, 248, 248))
    ctext(d, ax + 90, ay - 14, "図1", FT, GRAY)
    # 4つの流れ境界に相対圧ラベル
    # 境界4=0.02 上部
    ctext(d, ax + 75, ay + 6, "境界4  0.02", FT, BLUE)
    arrow(d, ax + 75, ay + 18, ax + 75, ay + 44, BLUE, 2, 9)
    # 境界1=0.10 右下
    ctext(d, ax + 250 - 6, ay + 150, "境界1  0.10", FT, RED, "rm")
    # 境界2=0.05 左下
    ctext(d, ax + 6, ay + 190, "境界2  0.05", FT, GREEN, "lm")
    # 境界3=0(基準) 中段
    ctext(d, ax + 250 + 6, ay + 130, "境界3  0(基準)", FT, BLACK, "lm")
    arrow(d, ax + 244, ay + 130, ax + 254, ay + 130, BLACK, 2, 8)
    ctext(d, ax + 130, ay + 216, "他辺はスリップ壁", FT, GRAY)
    # --- 図2: 静圧・流速の等値線図(小さめ2枚) ---
    def contbox(cx, cy, w, h, lab, unit, vals):
        d.rectangle((cx, cy, cx + w, cy + h), outline=BLACK, width=2)
        # 数本の等値線(斜めの弧)と数値ラベル
        for i, v in enumerate(vals):
            xx = cx + w * (i + 1) / (len(vals) + 1)
            dashed(d, xx, cy + 4, xx - 18, cy + h - 4, GRAY, 1, 6)
            ctext(d, xx, cy + h + 12, v, FT, GRAY)
        ctext(d, cx + w / 2, cy - 12, lab + " " + unit, FT, BLACK)
    bx = 400
    ctext(d, bx + 95, 66, "図2", FT, GRAY)
    contbox(bx, 96, 190, 90, "静圧分布", "[Pa]", ["0.10", "0.05", "0"])
    contbox(bx, 236, 190, 90, "流速分布", "[m/s]", ["低", "中", "高"])
    save(im, "t2e8StreamlinePick")


# 8-13 required : 左から一様流(2m/s,rho1.0)・中央に角柱・前面によどみ点A・流入静圧0.30Pa。答え(よどみ点静圧)は書かない
def f_stagnation():
    im, d = new()
    title(d, "一様流中の角柱前面のよどみ点 A")
    # 流入境界(左)
    d.line((80, 110, 80, 320), fill=BLUE, width=3)
    ctext(d, 80, 96, "流入境界", FT, BLUE)
    ctext(d, 90, 340, "流入静圧 0.30 Pa", FS, BLUE, "lm")
    # 一様流(左から右)
    for yy in range(140, 300, 34):
        arrow(d, 95, yy, 210, yy, BLACK, 2, 11)
    ctext(d, 150, 118, "一様流速 2.0 m/s", FS, BLACK)
    ctext(d, 150, 300, "流体密度 1.0 kg/m^3", FT, BLACK)
    # 角柱(中央)
    bx, by, bw, bh = 360, 215, 90, 130
    d.rectangle((bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2),
                outline=BLACK, width=3, fill=FILL2)
    ctext(d, bx + 8, by, "角柱", FS, BLACK)
    # よどみ点A(前面中央・流れがぶつかる位置)
    ax_, ay_ = bx - bw / 2, by
    node(d, ax_, ay_, 7, fill=RED, col=RED)
    ctext(d, ax_ - 16, ay_ - 22, "よどみ点 A", FS, RED, "rm")
    save(im, "t2e8Stagnation")


# 8-14 helpful : 非定常でのある瞬間の流線 と 粒子の軌跡(パスライン)が一致しない対比。概念OK
def f_streampath():
    im, d = new()
    title(d, "非定常流れ: ある瞬間の流線 と 粒子の軌跡(パスライン)")
    # 出発点
    sx, sy = 110, 240
    node(d, sx, sy, 6, fill=BLACK, col=BLACK)
    ctext(d, sx, sy + 22, "出発点", FT, GRAY)
    # ある瞬間の流線(その時刻の速度場に接する曲線・ゆるい曲線)
    sl = []
    for i in range(0, 460, 8):
        xx = sx + i
        yy = sy - 70 * math.sin(i / 150.0)
        sl.append((xx, yy))
    plot(d, 0, 0, sl, BLUE, 3)
    ctext(d, sl[-1][0] - 4, sl[-1][1] - 16, "流線(ある瞬間)", FS, BLUE, "rm")
    # 粒子の軌跡(パスライン・時間で速度場が変わるため別経路)
    pl = []
    for i in range(0, 460, 8):
        xx = sx + i
        yy = sy + 60 * math.sin(i / 110.0) + i * 0.12
        pl.append((xx, yy))
    plot(d, 0, 0, pl, RED, 3)
    ctext(d, pl[-1][0] - 4, pl[-1][1] + 18, "パスライン(粒子の軌跡)", FS, RED, "rm")
    note(d, "非定常では流線と粒子の軌跡は一致しない(定常なら一致)")
    save(im, "t2e8StreamlinePathline")


if __name__ == "__main__":
    for fn in [f_crosssec, f_ypluscheck, f_convergence, f_continuity, f_drag,
               f_flow3d, f_energyloss, f_massflow, f_shockwave, f_conjugate,
               f_resultnames, f_streamlinepick, f_stagnation, f_streampath]:
        fn()
    print("done 14")
