# -*- coding: utf-8 -*-
"""固体系(数値/要素/モデリング/検証)の図なし18問へ後付けする図。
白地660x420・黒線画・機構/設定のみ(答えの数値は焼き込まない)。すべてhelpful(回答後表示)。
JSONは別途配線。ここでは assets/figures/<key>.png を生成するのみ。"""
import sys, math, os
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
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


def hatch_circle(d, cx, cy, r, col=GRAY, step=12):
    """円内を斜線ハッチ(剛体などの表現)。"""
    x = -r
    while x <= r:
        h = math.sqrt(max(0.0, r * r - x * x))
        d.line((cx + x, cy - h, cx + x + 2 * h, cy - h + 2 * h) if False else
               (cx + x, cy - h, cx + x, cy + h), fill=col, width=1)  # placeholder
        x += step


def hatch_circle2(d, cx, cy, r, col=GRAY, step=13):
    """45度の斜線で円内をハッチ。"""
    for c in range(-2 * r, 2 * r, step):
        # 直線 y = x + c との交差を円でクリップ
        pts = []
        for t in range(-r, r + 1):
            xx = t
            yy = xx + c
            if xx * xx + yy * yy <= r * r:
                pts.append((cx + xx, cy + yy))
        if len(pts) >= 2:
            d.line((pts[0][0], pts[0][1], pts[-1][0], pts[-1][1]), fill=col, width=1)


# ============================================================
# 1. num6GaussVsNC : ガウス点とニュートン・コーツ点の配置比較
# ============================================================
def num6GaussVsNC():
    im, d = new(); title(d, "ガウス点とニュートン・コーツ点の配置")
    ox, ex = 130, 560
    ya, yb = 150, 300

    def X(f):
        return ox + (ex - ox) * f

    for (yy, lab) in [(ya, "ガウス数値積分"), (yb, "ニュートン・コーツ")]:
        d.line((ox, yy, ex, yy), fill=BLACK, width=3)
        d.line((ox, yy - 12, ox, yy + 12), fill=BLACK, width=3)
        d.line((ex, yy - 12, ex, yy + 12), fill=BLACK, width=3)
        ctext(d, ox, yy + 28, "a", FS, BLACK)
        ctext(d, ex, yy + 28, "b", FS, BLACK)
        ctext(d, ox - 14, yy - 30, lab, FS, BLACK, "lm")

    # ガウス点(4点・両端を含まず・不等間隔・内部寄り)
    gpts = [0.069, 0.330, 0.670, 0.931]
    for f in gpts:
        node(d, X(f), ya, 6, fill=BLUE, col=BLUE)
    ctext(d, X(0.5), ya - 30, "内部のみ・不等間隔(端を含まない)", FT, BLUE)

    # ニュートン・コーツ点(5点・両端含む・等間隔)
    npts = [0.0, 0.25, 0.5, 0.75, 1.0]
    for f in npts:
        node(d, X(f), yb, 6, fill=RED, col=RED)
    ctext(d, X(0.5), yb + 50, "両端を含む等間隔", FT, RED)

    note(d, "ガウス点=区間内部の最適位置(等間隔でない)。ニュートン・コーツ点=両端を含む等間隔。")
    save(im, "num6GaussVsNC")


# ============================================================
# 2. elem7QuadTempEdge : 辺に沿う二次温度分布(途中で低下)
# ============================================================
def elem7QuadTempEdge():
    im, d = new(); title(d, "要素の辺に沿う二次温度分布")
    ox, oy = 140, 340
    axes(d, ox, oy, 430, 250, "辺に沿う位置", "温度 (℃)")

    # T(s)=40 s^2 -60 s +60  (s:0..1)  端60/40, 中間40, 最小37.5(s=0.75)
    def Xf(s):
        return ox + 400 * s

    def Yf(T):
        return oy - (T - 30.0) * (220.0 / 35.0)  # 30..65℃

    # 温度目盛
    for T in (35, 40, 50, 60):
        d.line((ox - 5, Yf(T), ox, Yf(T)), fill=BLACK, width=2)
        ctext(d, ox - 12, Yf(T), str(T), FT, BLACK, "rm")

    pts = []
    s = 0.0
    while s <= 1.0001:
        T = 40 * s * s - 60 * s + 60
        pts.append((Xf(s), Yf(T)))
        s += 0.02
    d.line(pts, fill=BLUE, width=3, joint="curve")

    # 節点(端60/40, 中間40) と 最小点(s=0.75,37.5)
    node(d, Xf(0.0), Yf(60), 6, fill="white", col=RED); ctext(d, Xf(0.0), Yf(60) - 16, "60℃(端)", FT, RED)
    node(d, Xf(0.5), Yf(40), 6, fill="white", col=RED); ctext(d, Xf(0.5), Yf(40) - 16, "40℃(中間)", FT, RED)
    node(d, Xf(1.0), Yf(40), 6, fill="white", col=RED); ctext(d, Xf(1.0) + 6, Yf(40) - 14, "40℃(端)", FT, RED, "lm")
    node(d, Xf(0.75), Yf(37.5), 6, fill="white", col=GREEN)
    ctext(d, Xf(0.75), Yf(37.5) + 20, "途中で 37.5℃ まで低下", FT, GREEN)
    dashed(d, Xf(0.75), oy, Xf(0.75), Yf(37.5), GRAY)

    note(d, "二次補間では辺の途中が両端の値域(40〜60℃)より下がり得る(下に凸)。")
    save(im, "elem7QuadTempEdge")


# ---------- 横置き円筒の共通描画 ----------
def _hcyl_side(d, x0, x1, cy, R, fill=FILL1):
    ew = int(R * 0.42)
    d.rectangle((x0, cy - R, x1, cy + R), fill=fill)
    d.line((x0, cy - R, x1, cy - R), fill=BLACK, width=3)
    d.line((x0, cy + R, x1, cy + R), fill=BLACK, width=3)
    d.ellipse((x1 - ew, cy - R, x1 + ew, cy + R), outline=BLACK, width=3, fill=fill)
    d.arc((x0 - ew, cy - R, x0 + ew, cy + R), 90, 270, fill=BLACK, width=3)


def _saddle(d, cx, ytop, kind):
    """円筒下のサドル支承。kind='fix' or 'slide'。ytop=サドル上端(=円筒下面)。"""
    w = 34
    yb = ytop + 46
    d.polygon([(cx - w, yb), (cx + w, yb), (cx + w - 8, ytop + 6), (cx - w + 8, ytop + 6)],
              outline=BLACK, width=3, fill=FILL2)
    if kind == "fix":
        hwall(d, cx - w - 8, cx + w + 8, yb, side=1, n=7)
    else:
        for rx in (cx - 18, cx, cx + 18):
            d.ellipse((rx - 6, yb, rx + 6, yb + 12), outline=BLACK, width=2)
        d.line((cx - w - 8, yb + 12, cx + w + 8, yb + 12), fill=BLACK, width=2)


# ============================================================
# 3. model8SaddleAxial : 横置き円筒容器・軸(長手)方向地震
# ============================================================
def model8SaddleAxial():
    im, d = new(); title(d, "サドル支持の横置き円筒容器(軸方向地震)")
    x0, x1, cy, R = 170, 500, 210, 74
    _hcyl_side(d, x0, x1, cy, R)
    _saddle(d, x0 + 70, cy + R, "fix")
    _saddle(d, x1 - 70, cy + R, "slide")
    ctext(d, x0 + 70, cy + R + 74, "固定", FT, BLACK)
    ctext(d, x1 - 70, cy + R + 74, "スライド", FT, BLACK)
    # 軸(長手)方向の地震加速度
    force(d, x0 - 30, cy, 80, 0, "", RED)
    ctext(d, x0 - 40, cy - 20, "軸方向地震", FS, RED, "lm")
    dashed(d, x0 - 20, cy, x1 + 30, cy, GRAY)
    ctext(d, x1 + 34, cy, "軸", FT, GRAY, "lm")
    note(d, "長手(軸)方向の水平地震。長手を含む面が対称面(1/2モデルの候補)。")
    save(im, "model8SaddleAxial")


# ============================================================
# 4. model8SaddleTransverse : 横置き円筒容器・長手直交水平の地震(上面図)
# ============================================================
def model8SaddleTransverse():
    im, d = new(); title(d, "横置き円筒容器・長手直交水平の地震(上面図)")
    x0, x1, cy, R = 170, 500, 220, 66
    # 上面図:長円(カプセル)
    d.rectangle((x0, cy - R, x1, cy + R), outline=None, fill=FILL1)
    d.line((x0, cy - R, x1, cy - R), fill=BLACK, width=3)
    d.line((x0, cy + R, x1, cy + R), fill=BLACK, width=3)
    d.arc((x0 - R, cy - R, x0 + R, cy + R), 90, 270, fill=BLACK, width=3)
    d.arc((x1 - R, cy - R, x1 + R, cy + R), 270, 90, fill=BLACK, width=3)
    dashed(d, x0 - R, cy, x1 + R, cy, GRAY)
    ctext(d, x1 + R + 6, cy, "軸(長手)", FT, GRAY, "lm")
    # サドル位置(上面から見た帯)
    for sx in (x0 + 70, x1 - 70):
        d.rectangle((sx - 12, cy - R, sx + 12, cy + R), outline=BLACK, width=2)
    ctext(d, x0 + 70, cy + R + 22, "固定", FT, BLACK)
    ctext(d, x1 - 70, cy + R + 22, "スライド", FT, BLACK)
    # 長手直交・水平の地震(画面上下=直交方向)
    force(d, (x0 + x1) / 2, cy - R - 30, 0, 34, "", RED)
    ctext(d, (x0 + x1) / 2 + 12, cy - R - 40, "長手直交・水平地震", FS, RED, "lm")
    note(d, "軸に直交する水平地震。長手直交の鉛直面が対称面になり、この面を対称とする1/2化が妥当。")
    save(im, "model8SaddleTransverse")


# ============================================================
# 5. model8ArchBridge : 連続アーチ高架橋・中央脚oの沈下
# ============================================================
def model8ArchBridge():
    im, d = new(); title(d, "連続アーチ高架橋(中央脚oの沈下)")
    labels = ["a", "b", "c", "o", "c", "b", "a"]
    xs = [80 + i * 83 for i in range(7)]
    ytop, ybase = 210, 340
    hwall(d, 40, 620, ybase, side=1, n=24)
    # 桁(デッキ)
    d.line((xs[0], ytop - 26, xs[-1], ytop - 26), fill=BLACK, width=5)
    # アーチ(脚間)
    for i in range(6):
        x0, x1 = xs[i], xs[i + 1]
        d.arc((x0, ytop - 26, x1, ytop + 70), 180, 360, fill=BLACK, width=3)
    # 脚
    for i, x in enumerate(xs):
        d.line((x, ytop - 26, x, ybase), fill=BLACK, width=4)
        ctext(d, x, ybase + 22, labels[i], FS, (RED if labels[i] == "o" else BLACK))
    # 中央脚oの沈下
    xo = xs[3]
    force(d, xo, ybase + 34, 0, 40, "", RED)
    ctext(d, xo + 12, ybase + 56, "沈下", FT, RED, "lm")
    ctext(d, xo, ytop - 46, "中央脚 o", FT, RED)
    note(d, "脚配置 a-b-c-o-c-b-a は左右対称。中央脚oの沈下も対称なので中央面で1/2化できる。")
    save(im, "model8ArchBridge")


# ============================================================
# 6. model8NozzleThermal : 円筒胴と板厚違いノズルの交差・低温注入
# ============================================================
def model8NozzleThermal():
    im, d = new(); title(d, "円筒胴と板厚の異なるノズルの交差(低温流体注入)")
    # 胴(縦・肉厚t1)
    sx0, sx1, sy0, sy1 = 250, 410, 110, 350
    d.rectangle((sx0, sy0, sx1, sy1), outline=BLACK, width=3)
    d.rectangle((sx0 + 14, sy0, sx1 - 14, sy1), outline=BLACK, width=2)
    ctext(d, sx0 + 7, (sy0 + sy1) / 2, "胴\n板厚t1", FT, GRAY, "mm")
    # ノズル(右側・肉厚t2:胴より厚い/薄いを二重線間隔で表現)
    ny = 220
    nx1 = 540
    d.rectangle((sx1 - 14, ny - 44, nx1, ny - 30), outline=BLACK, width=2)
    d.rectangle((sx1 - 14, ny + 30, nx1, ny + 44), outline=BLACK, width=2)
    d.line((sx1, ny - 30, nx1, ny - 30), fill=BLACK, width=2)
    d.line((sx1, ny + 30, nx1, ny + 30), fill=BLACK, width=2)
    ctext(d, (sx1 + nx1) / 2, ny - 58, "ノズル(板厚t2)", FT, GRAY)
    # 交差部(応力/温度集中)
    d.ellipse((sx1 - 26, ny - 26, sx1 + 26, ny + 26), outline=RED, width=3)
    ctext(d, sx1 - 6, ny + 44, "交差部(温度差)", FT, RED)
    # 低温流体の注入
    arrow(d, nx1 + 6, ny, nx1 - 70, ny, BLUE, 4, 14)
    ctext(d, nx1 + 10, ny - 18, "低温流体\n注入", FS, BLUE, "lm")
    note(d, "板厚の異なる胴とノズルが交差し、低温流体で局所に温度差(熱応力)。対称面で分割可能。")
    save(im, "model8NozzleThermal")


# ============================================================
# 7. model8SkirtVessel : スカート支持高圧容器・軸対称半断面
# ============================================================
def model8SkirtVessel():
    im, d = new(); title(d, "スカート支持の高圧容器(軸対称半断面)")
    ax = 200
    dashed(d, ax, 80, ax, 375, GRAY)
    ctext(d, ax, 70, "軸(回転対称)", FT, GRAY)
    xi, xo = 262, 280       # 胴の内/外半径
    ytop, yjoint = 150, 300
    # 胴壁(縦の二重線)
    d.line((xi, ytop, xi, yjoint), fill=BLACK, width=3)
    d.line((xo, ytop, xo, yjoint), fill=BLACK, width=3)
    # 上部鏡板(ドーム・楕円弧・右側1/4)
    d.arc((ax * 2 - xo, ytop - 70, xo, ytop + 70), 270, 360, fill=BLACK, width=3)
    d.arc((ax * 2 - xi, ytop - 56, xi, ytop + 56), 270, 360, fill=BLACK, width=3)
    ctext(d, (ax + xo) / 2 + 10, ytop - 52, "鏡板", FT, GRAY)
    # スカート(取付部から下へ)
    d.line((xi, yjoint, xi, 355), fill=BLACK, width=3)
    d.line((xo, yjoint, xo, 355), fill=BLACK, width=3)
    hwall(d, xi - 14, xo + 22, 355, side=1, n=6)
    ctext(d, xo + 30, 335, "スカート", FT, GRAY, "lm")
    # 内圧
    for yy in (ytop + 40, (ytop + yjoint) / 2, yjoint - 30):
        arrow(d, xi - 26, yy, xi - 4, yy, RED, 3, 10)
    ctext(d, xi - 30, ytop + 20, "内圧", FT, RED, "rm")
    # 取付部の応力集中
    d.ellipse((xi - 16, yjoint - 16, xo + 16, yjoint + 16), outline=RED, width=3)
    ctext(d, xo + 26, yjoint, "応力集中\n(取付部)", FT, RED, "lm")
    note(d, "回転対称形状+軸対称荷重(内圧)なので軸対称要素の半断面でよい。取付部で応力集中。")
    save(im, "model8SkirtVessel")


# ============================================================
# 8. model8LNGTank : 地下円筒LNGタンク・軸対称半断面
# ============================================================
def model8LNGTank():
    im, d = new(); title(d, "地下円筒LNGタンク(軸対称半断面)")
    ax = 190
    dashed(d, ax, 95, ax, 370, GRAY)
    ctext(d, ax, 84, "軸(回転対称)", FT, GRAY)
    ow1 = 390          # 本体壁(外面)
    iw = 306           # 止水壁
    ytopO, ybot = 165, 345
    # 地面(地下=上に地盤)
    hwall(d, 60, 470, 110, side=-1, n=16)
    ctext(d, 432, 98, "地面(地下)", FT, GRAY, "lm")
    # ドーム屋根(外/内・右側1/4)
    d.arc((ax * 2 - ow1, ytopO - 60, ow1, ytopO + 60), 270, 360, fill=BLACK, width=3)
    d.arc((ax * 2 - iw, ytopO - 44, iw, ytopO + 44), 270, 360, fill=BLACK, width=3)
    ctext(d, (ax + ow1) / 2, ytopO - 40, "ドーム屋根", FT, GRAY)
    # 本体壁(外)
    d.line((ow1, ytopO, ow1, ybot), fill=BLACK, width=3)
    d.line((ow1 - 16, ytopO + 6, ow1 - 16, ybot), fill=BLACK, width=3)
    ctext(d, ow1 + 6, 260, "本体壁", FT, GRAY, "lm")
    # 止水壁(内)
    d.line((iw, ytopO + 4, iw, ybot), fill=BLACK, width=3)
    d.line((iw - 14, ytopO + 8, iw - 14, ybot), fill=BLACK, width=3)
    ctext(d, iw - 7, ybot + 16, "止水壁", FT, GRAY)
    # 底版
    d.rectangle((ax, ybot, ow1, ybot + 20), outline=BLACK, width=3, fill=FILL2)
    ctext(d, (ax + iw) / 2 + 20, ybot + 10, "底版", FT, GRAY)
    note(d, "回転対称の本体壁・止水壁・ドーム屋根。軸対称モデルで半断面のみを扱える。")
    save(im, "model8LNGTank")


# ============================================================
# 9. model8Dumbbell : ダンベル形引張試験片(軸対称)
# ============================================================
def model8Dumbbell():
    im, d = new(); title(d, "ダンベル形引張試験片(軸対称・軸方向引張)")
    cy = 220
    # 上側プロファイル(左グリップ→ゲージ→右グリップ)
    top = [(120, cy - 58), (196, cy - 58), (262, cy - 30), (398, cy - 30),
           (464, cy - 58), (540, cy - 58)]
    d.line(top, fill=BLACK, width=3, joint="curve")
    bot = [(x, 2 * cy - y) for (x, y) in top]
    d.line(bot, fill=BLACK, width=3, joint="curve")
    d.line((120, cy - 58, 120, cy + 58), fill=BLACK, width=3)
    d.line((540, cy - 58, 540, cy + 58), fill=BLACK, width=3)
    # 回転対称軸
    dashed(d, 90, cy, 570, cy, GRAY)
    ctext(d, 330, cy - 44, "回転対称軸(軸対称)", FT, GRAY)
    ctext(d, 330, cy + 44, "平行部(ゲージ部)", FT, GRAY)
    # 軸方向引張
    force(d, 120, cy, -60, 0, "P", RED)
    force(d, 540, cy, 60, 0, "P", RED)
    note(d, "軸まわりに回転対称な形状を軸方向に引張る=軸対称問題(軸対称要素で扱える)。")
    save(im, "model8Dumbbell")


# ============================================================
# 10. model8PlateHole : 円孔付き薄板・面内一様引張
# ============================================================
def model8PlateHole():
    im, d = new(); title(d, "円孔付き薄板の面内一様引張")
    x0, x1, y0, y1 = 170, 490, 150, 300
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, 42
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill="white")
    ctext(d, cx, cy, "円孔", FT, GRAY)
    # 一様引張(左右)
    for yy in (y0 + 35, cy, y1 - 35):
        arrow(d, x0, yy, x0 - 46, yy, RED, 3, 12)
        arrow(d, x1, yy, x1 + 46, yy, RED, 3, 12)
    ctext(d, x0 - 52, y0 + 12, "一様引張", FT, RED, "rm")
    ctext(d, x1 + 52, y0 + 12, "一様引張", FT, RED, "lm")
    # 応力集中(荷重直交=孔の上下縁)
    for yy in (cy - r, cy + r):
        d.ellipse((cx - 8, yy - 8, cx + 8, yy + 8), outline=BLUE, width=3)
    ctext(d, cx, cy + r + 22, "応力集中(孔縁・荷重直交)", FT, BLUE)
    note(d, "面内引張で孔縁(荷重に直交する上下)に応力集中。対称性で1/4化できる。")
    save(im, "model8PlateHole")


# ============================================================
# 11. model8BoltCircle : フランジ周方向の離散ボルト(周期対称)
# ============================================================
def model8BoltCircle():
    im, d = new(); title(d, "フランジ周方向の離散ボルト(周期/サイクリック対称)")
    cx, cy = 300, 230
    Ro, Rb, Ri = 150, 118, 78
    N = 12
    d.ellipse((cx - Ro, cy - Ro, cx + Ro, cy + Ro), outline=BLACK, width=3)
    d.ellipse((cx - Ri, cy - Ri, cx + Ri, cy + Ri), outline=BLACK, width=3, fill="white")
    ctext(d, cx, cy, "内孔", FT, GRAY)
    # 周期対称の1セクター(30度)を強調
    a0, a1 = -105, -75
    for a in (a0, a1):
        ar = math.radians(a)
        dashed(d, cx, cy, cx + Ro * math.cos(ar), cy + Ro * math.sin(ar), RED, 2)
    ctext(d, cx + 20, cy - Ro - 6, "1セクター(360/12)", FT, RED, "lm")
    # ボルト
    for i in range(N):
        ar = math.radians(360 * i / N - 90)
        bx, by = cx + Rb * math.cos(ar), cy + Rb * math.sin(ar)
        d.ellipse((bx - 8, by - 8, bx + 8, by + 8), outline=BLACK, width=2, fill=FILL2)
    ctext(d, cx, cy + Ro + 24, "取付けボルト(周方向に等配置)", FT, GRAY)
    note(d, "ボルトが周方向に離散配置=周期(サイクリック)対称。1セクターだけモデル化できる。")
    save(im, "model8BoltCircle")


# ============================================================
# 12. model8Tower : 円管部材の鉄塔・水平風荷重
# ============================================================
def model8Tower():
    im, d = new(); title(d, "円管部材の鉄塔(水平風荷重)")
    ybase, ytop = 350, 90
    levels = [ybase, 298, 246, 194, 142, ytop]

    def LX(y):
        return 150 + (270 - 150) * (ybase - y) / (ybase - ytop)

    def RX(y):
        return 510 + (390 - 510) * (ybase - y) / (ybase - ytop)

    hwall(d, 120, 540, ybase, side=1, n=18)
    # 脚柱
    d.line((LX(ybase), ybase, LX(ytop), ytop), fill=BLACK, width=4)
    d.line((RX(ybase), ybase, RX(ytop), ytop), fill=BLACK, width=4)
    # 横材+斜材(Xブレース)
    for i in range(len(levels) - 1):
        yb2, yt2 = levels[i], levels[i + 1]
        d.line((LX(yb2), yb2, RX(yb2), yb2), fill=BLACK, width=3)
        d.line((LX(yt2), yt2, RX(yt2), yt2), fill=BLACK, width=3)
        d.line((LX(yb2), yb2, RX(yt2), yt2), fill=GRAY, width=2)
        d.line((RX(yb2), yb2, LX(yt2), yt2), fill=GRAY, width=2)
    ctext(d, 330, ybase + 30, "円管部材(脚柱・横材・斜材ブレース)", FT, GRAY)
    # 風荷重(左から水平)
    for y in (300, 200, 120):
        arrow(d, LX(y) - 66, y, LX(y) - 6, y, RED, 3, 12)
    ctext(d, 70, 120, "風荷重", FS, RED, "lm")
    note(d, "水平風を受ける鉄塔。円管の軸力が主で、部材をはり(トラス)要素で表す対象。")
    save(im, "model8Tower")


# ============================================================
# 13. model8Tunnel : 断面一様の長いトンネル(平面ひずみ)
# ============================================================
def model8Tunnel():
    im, d = new(); title(d, "断面一様の長いトンネル(平面ひずみ)")
    # 前面(横断面)
    fx0, fy0, fw, fh = 170, 130, 210, 210
    d.rectangle((fx0, fy0, fx0 + fw, fy0 + fh), outline=BLACK, width=3, fill=FILL1)
    # トンネル開口(馬蹄形:上半円+側壁+床)
    tcx, tw, tcy = fx0 + fw / 2, 58, fy0 + 150
    d.arc((tcx - tw, tcy - 100, tcx + tw, tcy + 16), 180, 360, fill=BLACK, width=3)
    d.line((tcx - tw, tcy - 42, tcx - tw, tcy), fill=BLACK, width=3)
    d.line((tcx + tw, tcy - 42, tcx + tw, tcy), fill=BLACK, width=3)
    d.line((tcx - tw, tcy, tcx + tw, tcy), fill=BLACK, width=3)
    ctext(d, tcx, tcy + 26, "横断面", FT, GRAY)
    # 奥行き(長手)へ押し出し
    dx, dy = 150, -70
    for (px, py) in [(fx0, fy0), (fx0 + fw, fy0), (fx0 + fw, fy0 + fh)]:
        dashed(d, px, py, px + dx, py + dy, GRAY)
    d.rectangle((fx0 + dx, fy0 + dy, fx0 + fw + dx, fy0 + fh + dy), outline=LGRAY, width=2)
    arrow(d, fx0 + fw + 20, fy0 + fh - 10, fx0 + fw + dx, fy0 + fh - 10 + dy, BLUE, 3, 13)
    ctext(d, fx0 + fw + dx, fy0 + fh + dy - 18, "長手方向(断面一様)", FT, BLUE, "mm")
    note(d, "長手に長く断面が一様→長手方向ひずみ≒0。横断面を平面ひずみでモデル化できる。")
    save(im, "model8Tunnel")


# ============================================================
# 14. model8Hook : 曲率をもつ太い断面の吊りフック(曲がりはり)
# ============================================================
def model8Hook():
    im, d = new(); title(d, "曲率をもつ太い断面の吊りフック(曲がりはり)")
    cx, cy = 320, 215
    Ro, Ri = 100, 52
    # 本体(開いた太い環)
    d.arc((cx - Ro, cy - Ro, cx + Ro, cy + Ro), -30, 290, fill=BLACK, width=4)
    d.arc((cx - Ri, cy - Ri, cx + Ri, cy + Ri), -30, 290, fill=BLACK, width=4)
    for a in (-30, 290):
        ar = math.radians(a)
        d.line((cx + Ri * math.cos(ar), cy + Ri * math.sin(ar),
                cx + Ro * math.cos(ar), cy + Ro * math.sin(ar)), fill=BLACK, width=4)
    # 上部シャンク
    d.rectangle((cx - 15, 70, cx + 15, cy - Ro + 6), outline=BLACK, width=3, fill=FILL1)
    hwall(d, cx - 26, cx + 26, 70, side=-1, n=5)
    # 断面が太いことの寸法
    dim(d, cx - Ro - 16, cy, cx - Ri - 4, cy, "太い断面", col=GRAY)
    # 荷重(内側下部に吊り下げ)
    lx, ly = cx, cy + (Ri + Ro) / 2 + 6
    force(d, lx, ly, 0, 62, "W", RED)
    ctext(d, cx + 70, cy, "急な曲率\n(曲がりはり)", FT, GRAY, "lm")
    note(d, "曲率が大きく断面が太い→直線はり近似は不可。曲がりはり/ソリッドで応力を評価する。")
    save(im, "model8Hook")


# ============================================================
# 15. model8ChannelBeam : 厚肉溝形(開断面)はり・曲げ+ねじり
# ============================================================
def model8ChannelBeam():
    im, d = new(); title(d, "厚肉の溝形(開断面)はり(曲げ+ねじり)")
    # 溝形断面(コの字・左開き) 断面図
    x0, y0 = 250, 120
    t = 20
    H, Bf = 200, 90
    # 外形コの字(右向き開口)
    d.polygon([(x0, y0), (x0 + Bf, y0), (x0 + Bf, y0 + t), (x0 + t, y0 + t),
               (x0 + t, y0 + H - t), (x0 + Bf, y0 + H - t), (x0 + Bf, y0 + H),
               (x0, y0 + H)], outline=BLACK, width=3, fill=FILL1)
    ctext(d, x0 + Bf + 40, y0 + H / 2, "溝形(開断面)", FT, GRAY, "lm")
    # 図心 G と せん断中心 S(ずれ)
    gx, gy = x0 + 34, y0 + H / 2
    sx = x0 - 34
    node(d, gx, gy, 5, fill="white", col=BLUE); ctext(d, gx + 10, gy, "G(図心)", FT, BLUE, "lm")
    node(d, sx, gy, 5, fill="white", col=RED); ctext(d, sx - 10, gy, "S(せん断中心)", FT, RED, "rm")
    dashed(d, sx, gy, gx, gy, GRAY)
    ctext(d, (sx + gx) / 2, gy - 16, "偏心 e", FT, GRAY)
    # 曲げ(下向き荷重)+ ねじり
    force(d, gx, y0 - 44, 0, 36, "曲げ荷重", RED)
    angle_arc(d, sx, y0 + H + 20, 26, 200, 340, "ねじり T", RED)
    note(d, "開断面はせん断中心Sが図心Gからずれる。荷重がSを通らないと曲げに加えねじりが生じる。")
    save(im, "model8ChannelBeam")


# ============================================================
# 16. model8Silo : 円錐屋根付き円筒サイロ・横風荷重
# ============================================================
def model8Silo():
    im, d = new(); title(d, "円錐屋根付き円筒サイロ(横風荷重)")
    cx = 340
    bx0, bx1 = cx - 90, cx + 90
    ytop, ybot = 150, 340
    hwall(d, bx0 - 40, bx1 + 40, ybot, side=1, n=14)
    # 円筒胴
    d.rectangle((bx0, ytop, bx1, ybot), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((bx0, ybot - 14, bx1, ybot + 14), outline=BLACK, width=2)
    # 円錐屋根
    d.polygon([(bx0, ytop), (bx1, ytop), (cx, ytop - 78)], outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, ytop - 92, "円錐屋根", FT, GRAY)
    ctext(d, cx, (ytop + ybot) / 2, "円筒サイロ", FT, GRAY)
    ctext(d, cx, ybot + 30, "地面に固定", FT, GRAY)
    # 横風荷重(左から)
    for yy in (ytop + 30, (ytop + ybot) / 2, ybot - 30):
        arrow(d, bx0 - 70, yy, bx0 - 6, yy, RED, 3, 12)
    ctext(d, bx0 - 76, ytop + 30, "風荷重", FS, RED, "rm")
    note(d, "横風は周方向に非一様な圧力→軸対称にはならず、全周(3次元)シェルで扱う対象。")
    save(im, "model8Silo")


# ============================================================
# 17. model8Interface : 上材A/下材Bの界面と囲む要素1〜6
# ============================================================
def model8Interface():
    im, d = new(); title(d, "上材A/下材Bの界面(節点を囲む要素1〜6)")
    ox = 150
    cw = 120
    yA0, yI, yB1 = 130, 230, 330   # A上端, 界面, B下端
    ncol = 3
    # 材料A(上)グリッド
    for j in range(ncol + 1):
        d.line((ox + j * cw, yA0, ox + j * cw, yI), fill=BLACK, width=2)
    d.line((ox, yA0, ox + ncol * cw, yA0), fill=BLACK, width=2)
    # 材料B(下)グリッド
    for j in range(ncol + 1):
        d.line((ox + j * cw, yI, ox + j * cw, yB1), fill=BLACK, width=2)
    d.line((ox, yB1, ox + ncol * cw, yB1), fill=BLACK, width=2)
    # 界面線(強調)
    d.line((ox, yI, ox + ncol * cw, yI), fill=RED, width=4)
    ctext(d, ox + ncol * cw + 10, yI, "界面", FT, RED, "lm")
    # 要素番号
    for c in range(ncol):
        ctext(d, ox + c * cw + cw / 2, (yA0 + yI) / 2, str(c + 1), FL, BLACK)
        ctext(d, ox + c * cw + cw / 2, (yI + yB1) / 2, str(c + 4), FL, BLACK)
    # 界面節点(共有)
    for j in range(ncol + 1):
        node(d, ox + j * cw, yI, 7, fill=RED, col=RED)
    ctext(d, ox + ncol * cw / 2, yA0 - 18, "材料A(上)", FS, BLACK)
    ctext(d, ox + ncol * cw / 2, yB1 + 18, "材料B(下)", FS, BLACK)
    note(d, "界面の節点を上下の要素(1〜6)が共有=接合。接触/界面では節点共有かMPCで連続を課す。")
    save(im, "model8Interface")


# ============================================================
# 18. ver11RigidHoleStrip : 帯板中央の剛体円孔部・一様引張
# ============================================================
def ver11RigidHoleStrip():
    im, d = new(); title(d, "帯板中央の剛体円孔部を含む一様引張")
    x0, x1, y0, y1 = 130, 530, 150, 290
    cy = (y0 + y1) / 2
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    # 中央の剛体円部
    cx, r = (x0 + x1) / 2, 46
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill="white")
    hatch_circle2(d, cx, cy, r - 3, GRAY)
    ctext(d, cx, cy - r - 14, "剛体円孔部", FT, BLACK)
    # 一様引張(荷重方向=水平)
    for yy in (y0 + 30, cy, y1 - 30):
        arrow(d, x0, yy, x0 - 44, yy, RED, 3, 12)
        arrow(d, x1, yy, x1 + 44, yy, RED, 3, 12)
    ctext(d, x0 - 50, y0 + 10, "一様引張", FT, RED, "rm")
    ctext(d, x1 + 50, y0 + 10, "一様引張", FT, RED, "lm")
    # 中心線(対称線)
    dashed(d, x0 - 20, cy, x1 + 20, cy, BLUE)
    ctext(d, x1 + 24, cy + 16, "中心線(対称線)", FT, BLUE, "lm")
    note(d, "荷重方向・形状とも上下対称。中心線を対称面として上半分だけをモデル化できる。")
    save(im, "ver11RigidHoleStrip")


ALL = [num6GaussVsNC, elem7QuadTempEdge, model8SaddleAxial, model8SaddleTransverse,
       model8ArchBridge, model8NozzleThermal, model8SkirtVessel, model8LNGTank,
       model8Dumbbell, model8PlateHole, model8BoltCircle, model8Tower, model8Tunnel,
       model8Hook, model8ChannelBeam, model8Silo, model8Interface, ver11RigidHoleStrip]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    keys = ["num6GaussVsNC", "elem7QuadTempEdge", "model8SaddleAxial", "model8SaddleTransverse",
            "model8ArchBridge", "model8NozzleThermal", "model8SkirtVessel", "model8LNGTank",
            "model8Dumbbell", "model8PlateHole", "model8BoltCircle", "model8Tower", "model8Tunnel",
            "model8Hook", "model8ChannelBeam", "model8Silo", "model8Interface", "ver11RigidHoleStrip"]
    miss = [k for k in keys if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(keys), "MISSING", miss)
