# -*- coding: utf-8 -*-
"""固体力学1級 第5章 破壊力学・疲労解析 の問題図(s1e5*)を描画。
白地660x420・黒線画・機構のみ・物理的に正確。
ラベルはMeiryoで豆腐化しない通常表記(sigma/beta/theta/epsilon/nu/tau/Delta/KI 等)。"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def box(d, cx, cy, w, h, text, fnt=FS, fill="white"):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=fill)
    ctext(d, cx, cy, text, fnt)


def mesh(d, x0, y0, w, h, nx, ny, col=BLACK, wd=2):
    for i in range(nx + 1):
        x = x0 + w * i / nx
        d.line((x, y0, x, y0 + h), fill=col, width=wd)
    for j in range(ny + 1):
        y = y0 + h * j / ny
        d.line((x0, y, x0 + w, y), fill=col, width=wd)


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9):
    L = math.hypot(x2 - x1, y2 - y1)
    if L < 1:
        return
    n = max(1, int(L / dash))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash
            b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


# ============================================================ s1e5 問題図(20)

# 5-1 破壊現象の分類フロー
im, d = new()
title(d, "破壊現象の分類: 安定成長 -> 限界で不安定破壊")
box(d, 330, 90, 340, 46, "き裂の発生・存在(初期欠陥)")
arrow(d, 330, 113, 330, 150, BLACK, 3, 12)
box(d, 330, 178, 430, 50, "安定なき裂成長\n疲労き裂進展 / 応力腐食割れ", FT, FILL1)
arrow(d, 330, 203, 330, 250, RED, 3, 13)
ctext(d, 345, 226, "限界き裂長さに到達", FT, RED, "lm")
box(d, 175, 300, 220, 52, "ぜい性破壊\n(低じん性材料)", FT, FILL2)
box(d, 490, 300, 240, 52, "延性破壊・塑性不安定\n(高じん性材料)", FT, FILL2)
arrow(d, 300, 258, 210, 274, BLACK, 2, 10)
arrow(d, 360, 258, 455, 274, BLACK, 2, 10)
ctext(d, 330, 356, "小さいき裂=安定成長 -> 大きくなると不安定(急速)破壊", FT, GRAY)
save(im, "s1e5FractureMap")

# 5-2 き裂先端の 1/sqrt(r) 特異性
im, d = new()
title(d, "き裂先端の応力特異性  sigma = KI / sqrt(2*pi*r)")
ox, oy = 140, 350
axes(d, ox, oy, 450, 280, "r (先端からの距離)", "sigma")
C = 250 * math.sqrt(8.0)
pts = []
for px in range(4, 445):
    val = C / math.sqrt(px)
    if val > 270:
        continue
    pts.append((ox + px, oy - val))
plot(d, ox, oy, pts, BLUE, 3)
dashed(d, ox, oy - 275, ox, oy, RED, 2, 8)
ctext(d, ox + 12, oy - 258, "r -> 0 で sigma -> ∞ (発散)", FT, RED, "lm")
ctext(d, ox + 300, oy - 70, "1/sqrt(r) 特異性", FS, BLUE)
ctext(d, 330, 392, "特異点の応力値は使えない -> 強さ KI(応力拡大係数)で評価", FT, GRAY)
save(im, "s1e5CrackTipSing")

# 5-3 小規模降伏: 入れ子構造(K支配場>塑性域>プロセスゾーン)
im, d = new()
title(d, "小規模降伏: K支配場(弾性) > 塑性域 > プロセスゾーン")
cx, cy = 340, 235
# き裂(左から先端へ)
d.line((70, cy, cx, cy), fill=BLACK, width=5)
ctext(d, 120, cy - 16, "き裂", FT)
node(d, cx, cy, 5, fill=BLACK)
# 同心円
for r, col, lab, lx in [(150, BLUE, "K支配場(弾性場)", cx + 150),
                        (95, ORANGE, "塑性域", cx + 95),
                        (45, RED, "プロセスゾーン", cx)]:
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=3)
ctext(d, cx + 150, cy - 158, "K支配場(弾性場)", FT, BLUE)
ctext(d, cx + 118, cy - 70, "塑性域", FT, ORANGE, "lm")
ctext(d, cx, cy + 62, "プロセスゾーン(破壊)", FT, RED)
ctext(d, 330, 392, "KI が等しければ内部の状態も等しい -> KI=破壊靭性値 で破壊", FT, GRAY)
save(im, "s1e5SmallScaleYield")

# 5-4 き裂の3変形モード
im, d = new()
title(d, "き裂の3変形モード(重ね合わせで一般変形を表現)")


# 立体(アイソメ)の直方体を上下2スラブに割り、モード別に相対変位＋赤矢印で示す(→figlib.crack_mode)
crack_mode(d, 150, 205, 1)
ctext(d, 150, 300, "モードI: 開口形\n(垂直に引き離す)", FT)
crack_mode(d, 360, 205, 2)
ctext(d, 360, 300, "モードII: 面内せん断\n(き裂面に沿って前後にずれる)", FT)
crack_mode(d, 558, 205, 3)
ctext(d, 558, 300, "モードIII: 面外せん断\n(奥行き方向にずれる)", FT)
ctext(d, W / 2, 392, "一般のき裂変形 = モードI + II + III の重ね合わせ", FT, GRAY)
save(im, "s1e5ThreeModes")

# 5-5 中央貫通き裂と K=sigma*sqrt(pi*a)
im, d = new()
title(d, "中央貫通き裂(全長2a)と一様引張  K=sigma*sqrt(pi*a)")
px0, py0, pw, ph = 220, 110, 220, 210
d.rectangle((px0, py0, px0 + pw, py0 + ph), outline=BLACK, width=3, fill=FILL1)
cxp, cyp = px0 + pw / 2, py0 + ph / 2
# 中央き裂(水平)
half = 55
d.line((cxp - half, cyp, cxp + half, cyp), fill=BLACK, width=5)
dim(d, cxp - half, cyp + 26, cxp + half, cyp + 26, "2a", 0, RED)
node(d, cxp - half, cyp, 3, fill=BLACK)
node(d, cxp + half, cyp, 3, fill=BLACK)
# 遠方一様引張
for xx in (px0 + 45, cxp, px0 + pw - 45):
    force(d, xx, py0, 0, -45, "", RED)
    force(d, xx, py0 + ph, 0, 45, "", RED)
ctext(d, cxp, py0 - 58, "sigma (一様引張)", FT, RED)
ctext(d, cxp, py0 + ph + 60, "sigma", FT, RED)
ctext(d, 540, 170, "K = sigma*sqrt(pi*a)\na = 半き裂長さ\n破壊: K=KIC", FT, BLUE)
save(im, "s1e5Kformula")

# 5-6 相似則: 大小2枚の片側き裂板
im, d = new()
title(d, "相似則: 寸法 n 倍 -> 破壊応力 1/sqrt(n) 倍")
# 小(き裂 a)
box(d, 165, 220, 90, 130, "", fill=FILL1)
d.line((120, 220, 150, 220), fill=BLACK, width=5)  # 片側き裂 a
ctext(d, 135, 205, "a", FT, RED)
force(d, 165, 150, 0, -35, "sigma1", RED)
force(d, 165, 290, 0, 35, "", RED)
ctext(d, 165, 320, "小型: き裂 a", FT)
# 大(き裂 3a, 3倍相似)
box(d, 470, 210, 150, 200, "", fill=FILL2)
d.line((395, 210, 470, 210), fill=BLACK, width=5)  # 片側き裂 3a
ctext(d, 432, 195, "3a", FT, RED)
force(d, 470, 100, 0, -35, "sigma2", RED)
force(d, 470, 320, 0, 35, "", RED)
ctext(d, 470, 350, "大型(3倍相似): き裂 3a", FT)
ctext(d, 330, 392, "sigma1*sqrt(a)=sigma2*sqrt(3a) -> sigma2 = sigma1/sqrt(3)", FT, GRAY)
save(im, "s1e5Similitude")

# 5-7 引張(膜)+曲げ の重ね合わせ
im, d = new()
title(d, "直線分布応力 = 膜(3sigma) + 曲げ(±2sigma)")
SC = 11.0  # 応力->px


def profile(d, xax, ytop, ybot, s_top, s_bot, col, n=7):
    """xaxを基準線(ligament)、上端s_top・下端s_botの応力を右向き矢印で。"""
    d.line((xax, ytop, xax, ybot), fill=BLACK, width=2)
    for i in range(n):
        t = i / (n - 1)
        y = ytop + (ybot - ytop) * t
        s = s_top + (s_bot - s_top) * t
        L = s * SC
        if abs(L) < 2:
            d.line((xax, y, xax + 1, y), fill=col, width=2)
        else:
            arrow(d, xax, y, xax + L, y, col, 2, 8)
    # 分布の外形線
    d.line((xax + s_top * SC, ytop, xax + s_bot * SC, ybot), fill=col, width=2)


ytop, ybot = 150, 300
# 総分布(sigma 〜 5sigma)
profile(d, 120, ytop, ybot, 1, 5, BLACK)
ctext(d, 120, ytop - 18, "sigma", FT)
ctext(d, 175, ybot + 18, "5sigma", FT)
ctext(d, 130, 130, "総分布(直線)", FT)
ctext(d, 250, 225, "=", FL)
# 膜(一様 3sigma)
profile(d, 300, ytop, ybot, 3, 3, BLUE)
ctext(d, 335, 130, "膜 3sigma(平均)", FT, BLUE)
ctext(d, 415, 225, "+", FL)
# 曲げ(-2sigma 〜 +2sigma)
xb = 500
d.line((xb, ytop, xb, ybot), fill=BLACK, width=2)
for i in range(7):
    t = i / 6
    y = ytop + (ybot - ytop) * t
    s = -2 + 4 * t
    L = s * SC
    if abs(L) > 2:
        arrow(d, xb, y, xb + L, y, GREEN, 2, 8)
d.line((xb - 2 * SC, ytop, xb + 2 * SC, ybot), fill=GREEN, width=2)
ctext(d, xb, 130, "曲げ ±2sigma", FT, GREEN)
ctext(d, 330, 392, "膜=平均(sigma+5sigma)/2=3sigma, 曲げ=振幅(5sigma-sigma)/2=2sigma", FT, GRAY)
save(im, "s1e5TensionBending")

# 5-8 G-K 関係式(平面応力/平面ひずみ)
im, d = new()
title(d, "エネルギー解放率 G と 応力拡大係数 K の関係")
box(d, 330, 130, 520, 60, "G = (KI^2 + KII^2)/E'  +  (1+nu)*KIII^2/E", F, FILL1)
ctext(d, 330, 185, "面内モード I,II は等価弾性係数 E'、面外モード III は状態に依らず", FT, GRAY)
box(d, 190, 270, 250, 70, "平面応力\nE' = E", FS, FILL2)
box(d, 480, 270, 250, 70, "平面ひずみ\nE' = E/(1 - nu^2)", FS, FILL2)
ctext(d, 330, 360, "モードIII項は正符号で足す(+)", FT, GRAY)
save(im, "s1e5GKrelation")

# 5-9 G=KI^2/E' の代入(平面ひずみ)
im, d = new()
title(d, "平面ひずみのエネルギー解放率  G = KI^2 / E'")
# モードIき裂の小図
cx, cy = 150, 220
d.rectangle((cx - 70, cy - 60, cx + 70, cy + 60), outline=BLACK, width=2, fill=FILL1)
d.line((cx - 70, cy, cx, cy), fill=BLACK, width=4)
force(d, cx, cy - 60, 0, -32, "KI", RED)
force(d, cx, cy + 60, 0, 32, "", RED)
ctext(d, cx, cy + 95, "モードI", FT)
# 代入手順
box(d, 460, 150, 320, 46, "E' = E/(1 - nu^2)  (平面ひずみ)", FT, FILL2)
arrow(d, 460, 173, 460, 205, BLACK, 2, 10)
box(d, 460, 230, 320, 46, "G = KI^2 / E'", FS, FILL1)
arrow(d, 460, 253, 460, 285, BLACK, 2, 10)
box(d, 460, 310, 320, 46, "拘束大 -> E'大 -> G は平面応力より小", FT, FILL2)
ctext(d, 330, 392, "単位: (MPa*sqrt(m))^2 / Pa = J/m^2", FT, GRAY)
save(im, "s1e5Gcompute")

# 5-10 J積分: 経路積分Γと外向き法線n
im, d = new()
title(d, "J積分: き裂先端を囲む経路 Gamma と外向き法線 n")
cx, cy = 340, 225
# き裂
d.line((90, cy, cx, cy), fill=BLACK, width=5)
ctext(d, 140, cy - 16, "き裂", FT)
node(d, cx, cy, 4, fill=BLACK)
# 積分経路(き裂下面->先端まわり->上面): 開いたループ
r = 120
n = 60
path = []
for i in range(n + 1):
    ang = math.radians(-155 + 310 * i / n)  # 下面付近から上面付近まで
    path.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
d.line(path, fill=BLUE, width=3)
ctext(d, cx + r + 6, cy - 90, "Gamma", FS, BLUE, "lm")
# 外向き法線 n(数か所)
for i in [12, 30, 48]:
    ang = math.radians(-155 + 310 * i / n)
    bx, by = cx + r * math.cos(ang), cy - r * math.sin(ang)
    arrow(d, bx, by, bx + 26 * math.cos(ang), by - 26 * math.sin(ang), RED, 2, 9)
ctext(d, cx + 150, cy + 60, "n: 外向き法線", FT, RED)
ctext(d, 330, 392, "J = ∮(W*n1 - n*sigma*du/dx1)dGamma  経路に依らず一定", FT, GRAY)
save(im, "s1e5Jintegral")

# 5-11 傾斜き裂の応力分解
im, d = new()
title(d, "傾斜き裂の応力分解: sigma_n と tau (角度 beta)")
px0, py0, pw, ph = 235, 100, 200, 220
d.rectangle((px0, py0, px0 + pw, py0 + ph), outline=BLACK, width=2, fill=FILL1)
cxp, cyp = px0 + pw / 2, py0 + ph / 2
beta = math.radians(30)
# き裂(荷重に垂直な面=水平 から beta 傾ける)
Lh = 70
dx, dy = Lh * math.cos(beta), -Lh * math.sin(beta)
d.line((cxp - dx, cyp - dy, cxp + dx, cyp + dy), fill=BLACK, width=5)
# 遠方一様引張(鉛直)
for xx in (px0 + 40, cxp, px0 + pw - 40):
    force(d, xx, py0, 0, -38, "", RED)
    force(d, xx, py0 + ph, 0, 38, "", RED)
ctext(d, cxp, py0 - 52, "sigma (一様引張)", FT, RED)
# 角度 beta(き裂と水平線)
dashed(d, cxp, cyp, cxp + 80, cyp, GRAY)
angle_arc(d, cxp, cyp, 46, 0, 30, "beta", GRAY)
# き裂面法線方向の垂直応力 と せん断
nx, ny = math.sin(beta), math.cos(beta)  # き裂面の法線(上向き成分)
arrow(d, cxp, cyp, cxp + 55 * nx, cyp - 55 * ny, BLUE, 3, 11)
ctext(d, cxp + 62, cyp - 60, "sigma_n=sigma*cos^2(beta)", FT, BLUE, "lm")
arrow(d, cxp, cyp, cxp + 55 * math.cos(beta), cyp + 55 * math.sin(beta), GREEN, 3, 11)
ctext(d, cxp + 60, cyp + 55, "tau", FT, GREEN, "lm")
ctext(d, 330, 392, "beta=0 で KI最大・KII=0,  beta=45deg で KII最大", FT, GRAY)
save(im, "s1e5InclinedK")

# 5-12 混合モード疲労き裂: 折れ曲がり進展
im, d = new()
title(d, "混合モード疲労き裂: 等価 dKe で速度、Erdogan-Sih で方向")
cx, cy = 250, 230
d.line((90, cy, cx, cy), fill=BLACK, width=5)  # 元のき裂
ctext(d, 150, cy - 16, "元のき裂", FT)
node(d, cx, cy, 4, fill=BLACK)
# 折れ曲がり進展(角度theta)
th = math.radians(35)
ex, ey = cx + 120 * math.cos(th), cy - 120 * math.sin(th)
d.line((cx, cy, ex, ey), fill=RED, width=5)
ctext(d, ex + 10, ey - 4, "進展", FT, RED, "lm")
dashed(d, cx, cy, cx + 110, cy, GRAY)
angle_arc(d, cx, cy, 52, 0, 35, "theta", GRAY)
# 混合モード負荷
force(d, cx - 30, cy - 70, 40, 0, "", GREEN)
force(d, cx + 30, cy + 70, -40, 0, "", GREEN)
ctext(d, 500, 130, "速度: da/dN = C*(dKe)^n\n(dKI,dKII を等価 dKe に換算)", FT, BLUE)
ctext(d, 470, 300, "方向: Erdogan-Sih\n最大周方向応力説", FT, RED)
save(im, "s1e5MixedFatigue")

# 5-13 Barsoum の特異要素
im, d = new()
title(d, "Barsoum 特異要素: 中間節点を 1/4 点へ / 縮退三角形")
# 左: 8節点四角形、辺の中間節点を1/4点へ
lx0, ly0, lw, lh = 90, 150, 170, 140
d.rectangle((lx0, ly0, lx0 + lw, ly0 + lh), outline=BLACK, width=3, fill=FILL1)
# 角節点
corners = [(lx0, ly0), (lx0 + lw, ly0), (lx0 + lw, ly0 + lh), (lx0, ly0 + lh)]
for c in corners:
    node(d, c[0], c[1], 6)
ctext(d, lx0 - 8, ly0 + lh / 2, "先端", FT, RED, "rm")
d.line((lx0 - 4, ly0, lx0 - 4, ly0 + lh), fill=RED, width=3)  # き裂先端辺(左)
# 上辺と下辺の中間節点を左端(先端)から1/4点へ
qx_top = lx0 + lw * 0.25
node(d, qx_top, ly0, 6, fill=RED)
node(d, qx_top, ly0 + lh, 6, fill=RED)
# 右辺の中間節点は中央のまま
node(d, lx0 + lw, ly0 + lh / 2, 6)
dim(d, lx0, ly0 - 20, qx_top, ly0 - 20, "L/4", 0, RED)
dim(d, qx_top, ly0 - 20, lx0 + lw, ly0 - 20, "3L/4", 0, GRAY)
ctext(d, lx0 + lw / 2, ly0 + lh + 28, "中間節点を先端側 1/4 点へ\n-> ひずみに 1/sqrt(r) 特異性", FT)
# 右: 縮退三角形(先端で1辺を1点に)
tipx, tipy = 430, 220
p1 = (560, 155)
p2 = (560, 285)
d.polygon([(tipx, tipy), p1, p2], outline=BLACK, width=3, fill=FILL2)
node(d, tipx, tipy, 7, fill=RED)  # 縮退した3節点が集中
node(d, p1[0], p1[1], 6)
node(d, p2[0], p2[1], 6)
# 1/4点(斜辺の中間節点)
node(d, tipx + (p1[0] - tipx) * 0.25, tipy + (p1[1] - tipy) * 0.25, 6, fill=RED)
node(d, tipx + (p2[0] - tipx) * 0.25, tipy + (p2[1] - tipy) * 0.25, 6, fill=RED)
ctext(d, tipx - 6, tipy, "先端", FT, RED, "rm")
ctext(d, 480, 320, "一辺を縮退した三角形\n-> 積分の 1/r 特異性を打ち消す", FT)
save(im, "s1e5Barsoum")

# 5-14 仮想き裂進展法
im, d = new()
title(d, "仮想き裂進展法: 剛体移動領域 + 囲む変形要素 + 微小 da")
cx, cy = 300, 220
# 背景メッシュ
mesh(d, 120, 130, 420, 180, 10, 5, col=LGRAY, wd=1)
# き裂
d.line((120, cy, cx, cy), fill=BLACK, width=5)
node(d, cx, cy, 4, fill=BLACK)
ctext(d, 175, cy - 16, "き裂", FT)
# 剛体移動領域(先端まわりの箱)
d.rectangle((cx - 45, cy - 45, cx + 45, cy + 45), outline=RED, width=3)
ctext(d, cx, cy - 60, "剛体移動領域", FT, RED)
# 微小進展 da
arrow(d, cx, cy + 60, cx + 40, cy + 60, RED, 3, 11)
ctext(d, cx + 46, cy + 60, "da (微小)", FT, RED, "lm")
# 囲む変形要素(箱の外周を強調)
d.rectangle((cx - 75, cy - 75, cx + 75, cy + 75), outline=GREEN, width=2)
ctext(d, cx + 150, cy + 90, "外周=変形する要素", FT, GREEN)
ctext(d, 330, 392, "da はき裂長さの約 1e-3〜1e-4(自己相似進展の仮定)", FT, GRAY)
save(im, "s1e5VirtualCrack")

# 5-15 COD と CTOD
im, d = new()
title(d, "COD(き裂面の開口) と CTOD(先端鈍化の開口)")
mouthx, tipx, midy = 110, 470, 230
# 上下のき裂面(先端で鈍化=丸く閉じない)
upper = []
lower = []
gap_tip = 26  # CTOD
for i in range(0, 101):
    t = i / 100
    x = mouthx + (tipx - mouthx) * t
    open_mouth = 85
    # 開口量: 口で最大、先端でCTOD/2まで滑らかに減少
    op = (open_mouth - gap_tip / 2) * (1 - t) ** 0.6 + gap_tip / 2
    upper.append((x, midy - op))
    lower.append((x, midy + op))
d.line(upper, fill=BLACK, width=3)
d.line(lower, fill=BLACK, width=3)
# 先端の鈍化(半円)
d.arc((tipx - gap_tip / 2, midy - gap_tip / 2, tipx + gap_tip / 2, midy + gap_tip / 2), -90, 90, fill=BLACK, width=3)
# CTOD 寸法(先端)
dim(d, tipx - 4, midy - gap_tip / 2, tipx - 4, midy + gap_tip / 2, "CTOD", 0, RED)
ctext(d, tipx + 34, midy, "先端\n(鈍化)", FT, RED, "lm")
# COD 寸法(き裂面上の適当な位置)
px = 240
i = int((px - mouthx) / (tipx - mouthx) * 100)
dim(d, px, upper[i][1], px, lower[i][1], "COD", 0, BLUE)
ctext(d, px, upper[i][1] - 18, "き裂面上の位置", FT, BLUE)
ctext(d, 330, 392, "COD=き裂面の開口, CTOD=先端の鈍化開口(1要素隣の節点で代用可)", FT, GRAY)
save(im, "s1e5CODCTOD")

# 5-16 修正グッドマン線図
im, d = new()
title(d, "修正グッドマン線図  sigma_a=sigma_w(1-sigma_m/sigma_u)")
ox, oy = 120, 350
axes(d, ox, oy, 470, 300, "sigma_m (平均応力)", "sigma_a (応力振幅)")
sw_px = 250  # sigma_w=200 -> 250px
su_px = 420  # sigma_u=500 -> 420px
# グッドマン線(0,sigma_w)-(sigma_u,0)
P0 = (ox, oy - sw_px)
P1 = (ox + su_px, oy)
plot(d, ox, oy, [P0, P1], RED, 3)
ctext(d, ox - 8, P0[1], "sigma_w", FT, RED, "rm")
ctext(d, P1[0], oy + 16, "sigma_u", FT, RED)
# sigma_m=150 -> px, 読み取り sigma_a=140
sm_px = su_px * 150 / 500
sa_px = sw_px * (1 - 150 / 500)  # =0.7*250=175
qx = ox + sm_px
qy = oy - sa_px
dashed(d, qx, oy, qx, qy, GRAY)
dashed(d, ox, qy, qx, qy, GRAY)
node(d, qx, qy, 6, fill="white", col=BLUE)
ctext(d, qx, oy + 16, "sigma_m=150", FT, GRAY)
ctext(d, ox - 8, qy, "sigma_a", FT, BLUE, "rm")
ctext(d, 330, 392, "sigma_a=200*(1-150/500)=140,  sigma_max=150+140=290 MPa", FT, GRAY)
save(im, "s1e5Goodman")

# 5-17 コフィン・マンソン則(2直線の和)
im, d = new()
title(d, "ひずみ-寿命: 弾性項(傾きb) + 塑性項(傾きc) の両対数")
ox, oy = 120, 350
axes(d, ox, oy, 470, 300, "log(2N)", "log(epsilon)")
# 弾性項: 緩い傾き(b=-0.1)
el = [(ox, oy - 220), (ox + 440, oy - 180)]
plot(d, ox, oy, el, BLUE, 3)
ctext(d, ox + 445, oy - 178, "弾性項 A(2N)^b\n(傾き b=-0.1)", FT, BLUE, "rm")
# 塑性項: 急な傾き(c=-0.6)
pl = [(ox, oy - 275), (ox + 440, oy - 40)]
plot(d, ox, oy, pl, GREEN, 3)
ctext(d, ox + 120, oy - 250, "塑性項 B(2N)^c\n(傾き c=-0.6)\n=コフィン・マンソン則", FT, GREEN)
# 総和(上包絡・膝つき)
tot = [(ox, oy - 285), (ox + 130, oy - 235), (ox + 260, oy - 205), (ox + 440, oy - 178)]
plot(d, ox, oy, tot, RED, 3)
ctext(d, ox + 300, oy - 220, "総和(全ひずみ)", FT, RED)
# 交点(遷移寿命)
ix = 260
dashed(d, ox + ix, oy, ox + ix, oy - 205, LGRAY)
ctext(d, ox + ix, oy + 16, "遷移寿命", FT, GRAY)
ctext(d, 330, 392, "左=低サイクル(塑性支配), 右=高サイクル(弾性支配)", FT, GRAY)
save(im, "s1e5CoffinManson")

# 5-18 マイナー則と修正マイナー則(S-N線図)
im, d = new()
title(d, "S-N線図: 疲労限度 sigma_f と マイナー則の累積損傷")
ox, oy = 110, 350
axes(d, ox, oy, 480, 300, "log N", "sigma (応力振幅)")
# 疲労限度レベル
yf = oy - 90
kneex = ox + 300
# 斜め直線部
slope = [(ox + 20, oy - 265), (kneex, yf)]
plot(d, ox, oy, slope, BLACK, 3)
# 水平(疲労限度)
d.line((kneex, yf, ox + 480, yf), fill=BLACK, width=3)
ctext(d, ox + 480, yf - 14, "sigma_f(疲労限度)", FT, BLACK, "rm")
dashed(d, ox, yf, kneex, yf, LGRAY)
# 破線延長(直線部を下へ)
ex = ox + 470
ey = oy - 40
dashed(d, kneex, yf, ex, ey, RED, 2, 9)
ctext(d, kneex + 12, yf - 30, "破線=延長線(修正マイナー則)", FT, RED, "lm")
# 各応力点
for sy, lab, nx in [(oy - 225, "sigma1 (n1/N1=0.2)", ox + 70),
                    (oy - 155, "sigma2 (n2/N2=0.4)", ox + 150)]:
    # 斜線上の点
    t = (oy - 265 - sy) / (oy - 265 - yf)
    xx = ox + 20 + (kneex - ox - 20) * t
    node(d, xx, sy, 5, fill="white", col=BLUE)
    ctext(d, xx - 8, sy, lab, FT, BLUE, "rm")
# sigma3 (疲労限度以下, 破線上)
s3y = yf + 40
t3 = (s3y - yf) / (ey - yf)
x3 = kneex + (ex - kneex) * t3
node(d, x3, s3y, 5, fill="white", col=RED)
ctext(d, x3, s3y + 24, "sigma3(<sigma_f)", FT, RED)
ctext(d, 330, 392, "マイナー:sigma3で破断せず / 修正マイナー:n3/N3=1-0.6=0.4 -> 4e5回", FT, GRAY)
save(im, "s1e5Miner")

# 5-19 パリス則 da/dN-dK 線図(S字)
im, d = new()
title(d, "疲労き裂進展: log(da/dN) 対 log(dK) の S 字曲線")
ox, oy = 130, 350
axes(d, ox, oy, 460, 300, "log(dK)", "log(da/dN)")
xth = ox + 90   # dKth
xkc = ox + 380  # KIC 近傍
# S字: A領域(閾値近くで急立ち上がり)-B(直線)-C(急上昇)
pts = []
for i in range(0, 101):
    t = i / 100
    x = xth + (xkc - xth) * t
    # 中央は直線、両端で発散的
    yb = oy - 30 - 210 * t
    # A端(t小)で下へ潜り込み、C端(t大)で跳ね上げ
    corr = -70 * math.exp(-t / 0.08) + 70 * math.exp((t - 1) / 0.06)
    y = yb - corr
    y = max(oy - 285, min(oy - 10, y))
    pts.append((x, y))
plot(d, ox, oy, pts, BLUE, 3)
# dKth 垂直漸近
dashed(d, xth, oy, xth, oy - 285, RED, 2, 8)
ctext(d, xth, oy + 16, "dK_th", FT, RED)
# 領域ラベル
ctext(d, ox + 60, oy - 60, "A領域\n(下限界)", FT, GRAY)
ctext(d, ox + 235, oy - 145, "B領域\nda/dN=C(dK)^m\n(傾き m)", FT, BLUE)
ctext(d, ox + 405, oy - 220, "C領域\n(急速破壊)", FT, GRAY)
save(im, "s1e5ParisLaw")

# 5-20 疲労設計思想(椅子の脚の例)
im, d = new()
title(d, "疲労設計思想: 安全寿命 / フェールセーフ / 損傷許容")


def stool(d, cx, seaty, legs, thick, inspect=False):
    # 座面
    d.line((cx - 55, seaty, cx + 55, seaty), fill=BLACK, width=5)
    floor = seaty + 110
    d.line((cx - 75, floor, cx + 75, floor), fill=BLACK, width=2)
    if legs == 1:
        d.line((cx, seaty, cx, floor), fill=BLACK, width=thick)
    else:
        xs = [cx - 40 + 80 * i / (legs - 1) for i in range(legs)]
        for x in xs:
            d.line((x, seaty, x, floor), fill=BLACK, width=thick)
    if inspect:
        # 点検マーク(虫めがね)
        gx, gy = cx + 40, seaty + 55
        d.ellipse((gx - 12, gy - 12, gx + 12, gy + 12), outline=RED, width=3)
        d.line((gx + 9, gy + 9, gx + 22, gy + 22), fill=RED, width=3)


stool(d, 150, 150, 1, 16)
ctext(d, 150, 300, "安全寿命", FS)
ctext(d, 150, 326, "太い脚1本\n大きな安全率・点検なし", FT, GRAY)
stool(d, 355, 150, 4, 6)
ctext(d, 355, 300, "フェールセーフ", FS)
ctext(d, 355, 326, "多脚(多重安全)\n1本折れても倒れない", FT, GRAY)
stool(d, 555, 150, 2, 8, inspect=True)
ctext(d, 555, 300, "損傷許容", FS)
ctext(d, 555, 326, "点検でき裂発見\n破壊力学で残留強度評価", FT, GRAY)
save(im, "s1e5DesignPhil")


# ============================================================ 検証
KEYS = [
    "s1e5FractureMap", "s1e5CrackTipSing", "s1e5SmallScaleYield", "s1e5ThreeModes",
    "s1e5Kformula", "s1e5Similitude", "s1e5TensionBending", "s1e5GKrelation",
    "s1e5Gcompute", "s1e5Jintegral", "s1e5InclinedK", "s1e5MixedFatigue",
    "s1e5Barsoum", "s1e5VirtualCrack", "s1e5CODCTOD", "s1e5Goodman",
    "s1e5CoffinManson", "s1e5Miner", "s1e5ParisLaw", "s1e5DesignPhil",
]
missing = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
print("=" * 40)
print("keys expected:", len(KEYS))
print("missing:", missing if missing else "none")
