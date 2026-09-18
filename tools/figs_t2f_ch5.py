# -*- coding: utf-8 -*-
"""熱流体2級 第5章 格子生成法 の公式図(t2f5*)を描画。
白地660x420・黒線画・機構のみ(装飾禁止)。
豆腐対策: ギリシャ/特殊記号はローマ字表記(Delta,xi,eta,Re,J 等)。
接頭辞 t2f5 厳守(問題図 t2e5 と衝突させない・§13)。"""
import sys, os, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / dash))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            a = i * dash
            b = min((i + 1) * dash, L)
            d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)


def mapper(ox, oy, xlen, ylen, xmin, xmax, ymin, ymax):
    def m(x, y):
        return (ox + (x - xmin) / (xmax - xmin) * xlen,
                oy - (y - ymin) / (ymax - ymin) * ylen)
    return m


# ============================================================ t2f5StructVsUnstruct 構造 vs 非構造
im, d = new()
title(d, "構造格子 と 非構造格子")
# --- 構造格子(規則的な四角形) ---
ctext(d, 190, 78, "構造格子 (規則的)", FS, BLUE)
bx0, by0, cw, ch_, cols, rows = 70, 105, 48, 46, 5, 4
for i in range(cols + 1):
    d.line((bx0 + i * cw, by0, bx0 + i * cw, by0 + rows * ch_), fill=BLACK, width=2)
for j in range(rows + 1):
    d.line((bx0, by0 + j * ch_, bx0 + cols * cw, by0 + j * ch_), fill=BLACK, width=2)
for i in range(cols + 1):
    for j in range(rows + 1):
        node(d, bx0 + i * cw, by0 + j * ch_, r=3, fill=BLUE, col=BLUE)
ctext(d, 190, by0 + rows * ch_ + 26, "配列に連続格納 (i,j)", FT, GRAY)
ctext(d, 190, by0 + rows * ch_ + 46, "計算効率が高い", FT, GRAY)
# --- 非構造格子(不規則な三角形) ---
ctext(d, 490, 78, "非構造格子 (不規則)", FS, RED)
tris = [
    [(380, 120), (452, 110), (430, 178)],
    [(452, 110), (532, 120), (500, 182)],
    [(532, 120), (605, 118), (582, 185)],
    [(380, 120), (430, 178), (392, 248)],
    [(430, 178), (500, 182), (462, 250)],
    [(500, 182), (582, 185), (546, 250)],
    [(430, 178), (462, 250), (392, 248)],
    [(500, 182), (546, 250), (462, 250)],
    [(582, 185), (605, 118), (606, 250)],
    [(582, 185), (606, 250), (546, 250)],
    [(392, 248), (462, 250), (432, 300)],
    [(462, 250), (546, 250), (520, 300)],
    [(432, 300), (462, 250), (520, 300)],
]
pts = set()
for t in tris:
    d.polygon(t, outline=BLACK, width=2)
    for p in t:
        pts.add(p)
for p in pts:
    node(d, p[0], p[1], r=3, fill=RED, col=RED)
ctext(d, 490, 326, "リスト構造(ポインタ)で管理", FT, GRAY)
ctext(d, 490, 346, "複雑形状に柔軟", FT, GRAY)
note(d, "規則的な並び=配列=構造格子 / 不規則=リスト参照=非構造格子")
save(im, "t2f5StructVsUnstruct")


# ============================================================ t2f5CartesianCut 直交格子と階段近似
im, d = new()
title(d, "直交格子(デカルト)と物体境界の階段状近似")
gx0, gy0, cw, n = 70, 95, 42, 12
gw = cw * n
for i in range(n + 1):
    d.line((gx0 + i * cw, gy0, gx0 + i * cw, gy0 + 6 * cw), fill=LGRAY, width=1)
for j in range(7):
    d.line((gx0, gy0 + j * cw, gx0 + gw, gy0 + j * cw), fill=LGRAY, width=1)
# 曲線状の物体境界
cx, cy, rr = gx0 + 30, gy0 + 6 * cw, 200
curve = []
for k in range(61):
    ang = math.radians(90 + 60 * k / 60)  # 90->150度あたりの弧
    curve.append((cx + rr * math.cos(math.radians(20 + 50 * k / 60)),
                  cy - rr * math.sin(math.radians(20 + 50 * k / 60))))
plot(d, 0, 0, curve, BLUE, 3)
ctext(d, gx0 + 250, gy0 + 40, "曲線状の物体境界", FT, BLUE)
# 階段状近似(格子線に沿ってギザギザ)
stair = [(gx0, gy0 + 6 * cw)]
xx, yy = gx0, gy0 + 6 * cw
for step in range(6):
    xx += cw
    stair.append((xx, yy))
    yy -= cw
    stair.append((xx, yy))
    xx += cw
    stair.append((xx, yy))
for i in range(len(stair) - 1):
    d.line((stair[i][0], stair[i][1], stair[i + 1][0], stair[i + 1][1]), fill=RED, width=4)
ctext(d, gx0 + 230, gy0 + 6 * cw - 20, "階段状に近似(ギザギザ)", FT, RED)
# カットセル
csx, csy = gx0 + 8 * cw, gy0 + 2 * cw
d.rectangle((csx, csy, csx + cw, csy + cw), outline=GREEN, width=3)
d.line((csx, csy + cw, csx + cw, csy), fill=GREEN, width=3)
ctext(d, csx + cw + 60, csy + cw / 2, "カットセル", FT, GREEN)
note(d, "メトリック計算不要で軽いが、物体境界を階段状にしか表せない(近傍精度が低下)")
save(im, "t2f5CartesianCut")


# ============================================================ t2f5GenMethodClass 生成法の分類(2列)
im, d = new()
title(d, "格子生成法の分類")
# 左: 構造格子系
lx, ly, bw, bh = 60, 95, 250, 230
d.rectangle((lx, ly, lx + bw, ly + bh), outline=BLUE, width=3)
d.line((lx, ly + 46, lx + bw, ly + 46), fill=BLUE, width=2)
ctext(d, lx + bw / 2, ly + 23, "構造格子系", F, BLUE)
for i, s in enumerate(["・マルチブロック法", "・重合格子(オーバーセット)", "・接合格子"]):
    ctext(d, lx + 20, ly + 84 + i * 46, s, FS, BLACK, "lm")
# 右: 非構造格子系
rx = 350
d.rectangle((rx, ly, rx + bw, ly + bh), outline=RED, width=3)
d.line((rx, ly + 46, rx + bw, ly + 46), fill=RED, width=2)
ctext(d, rx + bw / 2, ly + 23, "非構造格子系", F, RED)
for i, s in enumerate(["・デローニー分割法", "・アドバンシングフロント法", "・四分木 / 八分木法"]):
    ctext(d, rx + 20, ly + 84 + i * 46, s, FS, BLACK, "lm")
note(d, "ブロック分割で構造格子をつなぐ=構造格子系 / 点群から要素を張る=非構造格子系")
save(im, "t2f5GenMethodClass")


# ============================================================ t2f5GridQuality 格子品質の4指標
im, d = new()
title(d, "格子品質  直交性・スキューネス・アスペクト比・滑らかさ")
# 良い格子(左)
ctext(d, 175, 80, "良い格子", FS, BLUE)
d.rectangle((100, 100, 250, 240), outline=BLUE, width=3)
angle_arc(d, 100, 240, 26, 0, 90, "~90deg", BLUE)
ctext(d, 175, 262, "直交・正方形に近い", FT, GRAY)
# 悪い格子(右): スキュー+高アスペクト
ctext(d, 480, 80, "悪い格子", FS, RED)
d.polygon([(400, 240), (560, 240), (600, 100), (440, 100)], outline=RED, width=3)
ctext(d, 495, 262, "歪み(スキュー)大", FT, GRAY)
d.rectangle((400, 300, 600, 330), outline=RED, width=3)
ctext(d, 500, 350, "アスペクト比が大きい(細長い)", FT, GRAY)
# 滑らかさ
ctext(d, 175, 300, "隣接セルの大きさ比", FT, GRAY)
d.rectangle((110, 320, 150, 360), outline=BLACK, width=2)
d.rectangle((150, 320, 210, 360), outline=BLACK, width=2)
ctext(d, 175, 382, "急変させない(比<=1.5)", FT, GRAY)
note(d, "直交性=交角の直角度 / スキューネス=歪み / アスペクト比=縦横比 / 滑らかさ=大きさの連続")
save(im, "t2f5GridQuality")


# ============================================================ t2f5StretchLayers 境界層の等比拡大
im, d = new()
title(d, "境界層格子の等比拡大  Delta_n = Delta_1 r^(n-1)")
wx0, wx1, wy = 120, 560, 340
hwall(d, wx0, wx1, wy, side=1)
ctext(d, (wx0 + wx1) / 2, wy + 30, "壁面 (wall)", FT, GRAY)
# 層(下から上へ間隔が拡大)
d1 = 26
r = 1.3
y = wy
widths = [d1 * r ** k for k in range(5)]
labels = ["Delta_1", "Delta_2", "Delta_3", "Delta_4", "Delta_5"]
for k, w in enumerate(widths):
    y_next = y - w
    d.line((wx0, y_next, wx1, y_next), fill=BLUE, width=2)
    dim(d, wx0 - 40, y, wx0 - 40, y_next, labels[k], col=RED if k < 3 else GRAY)
    y = y_next
ctext(d, (wx0 + wx1) / 2, 88, "外側ほど格子幅を r 倍で拡大", FS, BLUE)
ctext(d, 400, 120, "r <= 1.5 が望ましい", FT, GRAY)
note(d, "第n層 = Delta_1 * r^(n-1) (指数は n-1) / 例 Delta_1=0.2mm, r=1.25 -> Delta_3=0.3125mm")
save(im, "t2f5StretchLayers")


# ============================================================ t2f5BoundaryLayer 境界層厚さと1/√Re
im, d = new()
title(d, "境界層の厚さ  delta ~ 1 / sqrt(Re)")
px0, px1, py = 90, 600, 300
hwall(d, px0, px1, py, side=1)
ctext(d, 340, py + 28, "平板 (flat plate)", FT, GRAY)
# 流入プロファイル
for k in range(4):
    yy = py - 30 - k * 24
    arrow(d, px0 - 40, yy, px0 - 4, yy, BLUE, 2, 8)
ctext(d, px0 - 44, py - 130, "一様流", FT, BLUE, "mm")
# 境界層曲線 delta(x) ~ sqrt(x)
curve = []
for k in range(101):
    x = px0 + (px1 - px0 - 20) * k / 100
    delta = 120 * math.sqrt((k / 100) + 0.02)
    curve.append((x, py - delta * 0.9))
plot(d, 0, 0, curve, RED, 3)
ctext(d, px1 - 120, py - 130, "delta(x): 境界層", FT, RED)
# 壁近傍の細格子
for k in range(5):
    yy = py - 8 - k * 9
    d.line((px0 + 150, yy, px0 + 260, yy), fill=LGRAY, width=1)
ctext(d, px0 + 205, py - 78, "壁近傍は細格子", FT, GRAY)
ctext(d, 340, 110, "Re が大きいほど境界層は薄い (delta ~ 1/sqrt(Re))", FS, BLACK)
note(d, "境界層厚さ 1/sqrt(Re) を基準に、層内へ数点〜10点入る密度をとる")
save(im, "t2f5BoundaryLayer")


# ============================================================ t2f5Octree 8分木の細分化
im, d = new()
title(d, "8分木(オクトツリー)格子  N = 8^L  (8 = 2x2x2)")
# 立方体(アイソメ)を各方向2分割 => 8子セル
ox, oy, w, h, dp = 90, 130, 160, 160, 90
iso_box(d, ox, oy, w, h, dp)
dx, dy = int(dp * 0.8), int(dp * 0.5)
# 前面中線
d.line((ox + w / 2, oy, ox + w / 2, oy + h), fill=BLACK, width=2)
d.line((ox, oy + h / 2, ox + w, oy + h / 2), fill=BLACK, width=2)
# 上面中線
d.line((ox + dx / 2, oy - dy / 2, ox + w + dx / 2, oy - dy / 2), fill=BLACK, width=2)
d.line((ox + w / 2, oy, ox + w / 2 + dx, oy - dy), fill=BLACK, width=2)
# 右面中線
d.line((ox + w, oy + h / 2, ox + w + dx, oy + h / 2 - dy), fill=BLACK, width=2)
d.line((ox + w + dx / 2, oy - dy / 2, ox + w + dx / 2, oy + h - dy / 2), fill=BLACK, width=2)
ctext(d, ox + w / 2, oy + h + 34, "1段階 -> 8 子セル", FS, BLUE)
# 矢印
arrow(d, 300, 210, 380, 210, BLACK, 3, 13)
# 2段階目 = ?
d.rectangle((400, 150, 560, 310), outline=GRAY, width=3)
d.line((480, 150, 480, 310), fill=LGRAY, width=1)
d.line((400, 230, 560, 230), fill=LGRAY, width=1)
d.rectangle((400, 150, 480, 230), outline=BLACK, width=2)
d.line((440, 150, 440, 230), fill=LGRAY, width=1)
d.line((400, 190, 480, 190), fill=LGRAY, width=1)
ctext(d, 480, 330, "2段階目 -> 各セルを再分割 (?)", FS, RED)
ctext(d, 480, 118, "細かく/粗く 双方向に適応", FT, GRAY)
note(d, "各段でセル数8倍: L段で 8^L (2段階=64) / 並びは不規則で非構造格子扱い")
save(im, "t2f5Octree")


# ============================================================ t2f5Jacobian 座標変換のヤコビアン
im, d = new()
title(d, "座標変換のヤコビアン  J = x_xi*y_eta - x_eta*y_xi")
# 計算空間: 単位正方形
cs = 110
csx, csy = 90, 120
d.rectangle((csx, csy, csx + cs, csy + cs), outline=BLUE, width=3, fill=FILL1)
ctext(d, csx + cs / 2, csy - 22, "計算空間 (xi, eta)", FS, BLUE)
dim(d, csx, csy + cs + 26, csx + cs, csy + cs + 26, "1", col=GRAY)
dim(d, csx - 26, csy, csx - 26, csy + cs, "1", col=GRAY)
# 写像矢印
arrow(d, csx + cs + 30, csy + cs / 2, csx + cs + 130, csy + cs / 2, BLACK, 3, 14)
ctext(d, csx + cs + 80, csy + cs / 2 - 20, "x=2xi, y=3eta", FT, BLACK)
# 物理空間: 2x3長方形
pw, ph = 130, 195
psx, psy = 400, 90
d.rectangle((psx, psy, psx + pw, psy + ph), outline=RED, width=3, fill=FILL2)
ctext(d, psx + pw / 2, psy - 22, "物理空間 (x, y)", FS, RED)
dim(d, psx, psy + ph + 26, psx + pw, psy + ph + 26, "2 (=x_xi)", col=GRAY)
dim(d, psx + pw + 30, psy, psx + pw + 30, psy + ph, "3 (=y_eta)", col=GRAY)
ctext(d, 330, 360, "面積比 J = 2 x 3 = 6  (符号は正)", FS, BLACK)
note(d, "J = 単位セルが物理空間で占める面積比(3次元は体積比) / J<=0 は格子の折れ重なり")
save(im, "t2f5Jacobian")


# ============================================================ t2f5GenMethodTree 構造格子生成法の分類木
im, d = new()
title(d, "構造格子の生成法")
# 根
rx, ry, rw, rh = 230, 70, 200, 44
d.rectangle((rx, ry, rx + rw, ry + rh), outline=BLACK, width=3)
ctext(d, rx + rw / 2, ry + rh / 2, "構造格子の生成法", FS, BLACK)
root_c = (rx + rw / 2, ry + rh)
# 2分岐
alg = (150, 170); pde = (490, 170)
bw2, bh2 = 190, 44
for (cx, cy), lab, col in [(alg, "代数的方法", BLUE), (pde, "偏微分方程式(PDE)法", GREEN)]:
    d.line((root_c[0], root_c[1], cx, cy), fill=BLACK, width=2)
    d.rectangle((cx - bw2 / 2, cy, cx + bw2 / 2, cy + bh2), outline=col, width=3)
    ctext(d, cx, cy + bh2 / 2, lab, FS, col)
# 代数的方法の子
ctext(d, alg[0], alg[1] + bh2 + 34, "補間関数・写像関数", FT, GRAY)
ctext(d, alg[0], alg[1] + bh2 + 58, "(速い・対話向き)", FT, GRAY)
# PDE法の子(楕円/双曲/放物)
kids = [("楕円型", 400), ("双曲型", 490), ("放物型", 580)]
for lab, cx in kids:
    d.line((pde[0], pde[1] + bh2, cx, pde[1] + bh2 + 30), fill=BLACK, width=2)
    ctext(d, cx, pde[1] + bh2 + 44, lab, FT, GREEN)
ctext(d, 490, pde[1] + bh2 + 76, "楕円=平滑 / 双曲=表面から外 / 放物=外から内", FT, GRAY)
note(d, "代数的方法(補間・写像) と PDE法(楕円/双曲/放物の3型)に大別")
save(im, "t2f5GenMethodTree")


# ============================================================ t2f5PdeGridTypes PDE格子生成の3型
im, d = new()
title(d, "偏微分方程式による格子生成  楕円 / 双曲 / 放物")
cols = [("楕円型", 70, BLUE, ["全境界に条件", "(境界値問題)", "平滑な格子", "= 平滑化に利用"]),
        ("双曲型", 250, GREEN, ["物体表面から", "外へ解き進む", "直交性に優れる", "外部境界は不可制御"]),
        ("放物型", 430, RED, ["外部境界から", "内へ解き進む", "(双曲の逆向き)", "内部境界は不可制御"])]
bw3 = 160
for name, x, col, rows in cols:
    d.rectangle((x, 90, x + bw3, 340), outline=col, width=3)
    d.line((x, 132, x + bw3, 132), fill=col, width=2)
    ctext(d, x + bw3 / 2, 111, name, F, col)
    for i, s in enumerate(rows):
        ctext(d, x + bw3 / 2, 160 + i * 42, s, FT, BLACK)
note(d, "楕円=境界値問題で平滑 / 双曲=表面起点で直交性良 / 放物=外部起点(向きが逆)")
save(im, "t2f5PdeGridTypes")


# ============================================================ t2f5Topologies O/C/H型トポロジー
im, d = new()
title(d, "格子トポロジー  O型 / C型 / H型")


def airfoil(d, cx, cy, s=1.0):
    pts = []
    for k in range(37):
        t = 2 * math.pi * k / 36
        rr = 34 * s * (1 + 0.15 * math.cos(t))
        pts.append((cx + rr * math.cos(t), cy + 0.55 * rr * math.sin(t)))
    d.polygon(pts, outline=BLACK, width=3, fill=FILL1)


# O型
ox = 130; oy = 210
ctext(d, ox, 78, "O型 (物体を1周)", FS, BLUE)
for rr in (55, 78):
    d.ellipse((ox - rr, oy - rr * 0.7, ox + rr, oy + rr * 0.7), outline=BLUE, width=2)
for a in range(0, 360, 45):
    ra = math.radians(a)
    d.line((ox + 40 * math.cos(ra), oy + 28 * math.sin(ra),
            ox + 78 * math.cos(ra), oy + 55 * math.sin(ra)), fill=LGRAY, width=1)
airfoil(d, ox, oy)
# C型
cx = 340; cy = 210
ctext(d, cx, 78, "C型 (後方に切れ目)", FS, GREEN)
d.arc((cx - 78, cy - 60, cx + 78, cy + 60), 120, 400, fill=GREEN, width=2)
d.arc((cx - 55, cy - 42, cx + 55, cy + 42), 120, 400, fill=GREEN, width=2)
d.line((cx + 40, cy, cx + 120, cy), fill=GREEN, width=2)  # 後方カット
airfoil(d, cx, cy)
ctext(d, cx + 95, cy + 22, "後流", FT, GRAY)
# H型
hx = 545; hy = 210
ctext(d, hx, 78, "H型 (通り抜け)", FS, RED)
for yy in (oy - 55, oy - 30, oy + 30, oy + 55):
    d.line((hx - 78, yy, hx + 78, yy), fill=RED, width=2)
for xx in (hx - 60, hx - 30, hx + 30, hx + 60):
    d.line((xx, oy - 55, xx, oy + 55), fill=RED, width=1)
airfoil(d, hx, hy)
note(d, "物理空間の巻いた格子線は、計算空間では長方形の規則格子に対応する")
save(im, "t2f5Topologies")


# ============================================================ t2f5RHPmethods r/h/p法
im, d = new()
title(d, "解適合格子法  r法 / h法 / p法")


def minigrid(d, ox, oy, n=3, cw=34, col=LGRAY):
    for i in range(n + 1):
        d.line((ox + i * cw, oy, ox + i * cw, oy + n * cw), fill=col, width=1)
        d.line((ox, oy + i * cw, ox + n * cw, oy + i * cw), fill=col, width=1)


# r法: 点を移動
ctext(d, 130, 90, "r法: 点を移動", FS, BLUE)
minigrid(d, 70, 120, 3)
node(d, 70 + 34, 120 + 34, r=5, fill="white", col=GRAY)
arrow(d, 70 + 34, 120 + 34, 70 + 34 + 24, 120 + 34 + 14, RED, 3, 11)
node(d, 70 + 34 + 24, 120 + 34 + 14, r=5, fill=RED, col=RED)
ctext(d, 130, 250, "総数は不変", FT, GRAY)
# h法: 点を追加/削除
ctext(d, 330, 90, "h法: 追加/削除", FS, GREEN)
minigrid(d, 270, 120, 3)
d.line((270 + 34, 120 + 34, 270 + 68, 120 + 34), fill=GREEN, width=2)
d.line((270 + 51, 120 + 34, 270 + 51, 120 + 68), fill=GREEN, width=2)
node(d, 270 + 51, 120 + 34, r=5, fill=RED, col=RED)
node(d, 270 + 51, 120 + 68, r=5, fill=RED, col=RED)
node(d, 270 + 51, 120 + 51, r=4, fill=RED, col=RED)
ctext(d, 330, 250, "密度を変える", FT, GRAY)
# p法: 次数を上げる
ctext(d, 540, 90, "p法: 次数上げ", FS, RED)
d.rectangle((480, 120, 600, 220), outline=BLACK, width=2)
for (px, py) in [(480, 120), (600, 120), (480, 220), (600, 220)]:
    node(d, px, py, r=4, fill=BLACK, col=BLACK)
for (px, py) in [(540, 120), (540, 220), (480, 170), (600, 170), (540, 170)]:
    node(d, px, py, r=4, fill=RED, col=RED)
ctext(d, 540, 250, "要素内の次数を上げる", FT, GRAY)
note(d, "構造格子は点の増減が難しく基本 r法 / 非構造格子は r・h・p すべて可")
save(im, "t2f5RHPmethods")


# ============================================================ t2f5Overset 重合格子
im, d = new()
title(d, "重合格子法 (オーバーセット)")
# 背景の直交格子
bx0, by0, cw, nx, ny = 70, 90, 42, 12, 6
for i in range(nx + 1):
    d.line((bx0 + i * cw, by0, bx0 + i * cw, by0 + ny * cw), fill=LGRAY, width=1)
for j in range(ny + 1):
    d.line((bx0, by0 + j * cw, bx0 + nx * cw, by0 + j * cw), fill=LGRAY, width=1)
ctext(d, bx0 + nx * cw - 70, by0 + 16, "背景格子", FT, GRAY)
# 物体まわりのO型格子
ocx, ocy = bx0 + 5 * cw, by0 + 3 * cw
for rr in (34, 58, 82):
    d.ellipse((ocx - rr, ocy - rr, ocx + rr, ocy + rr), outline=BLUE, width=2)
for a in range(0, 360, 30):
    ra = math.radians(a)
    d.line((ocx + 34 * math.cos(ra), ocy + 34 * math.sin(ra),
            ocx + 82 * math.cos(ra), ocy + 82 * math.sin(ra)), fill=BLUE, width=1)
node(d, ocx, ocy, r=20, fill=FILL2, col=BLACK)
ctext(d, ocx, ocy, "物体", FT, BLACK)
# 重合部の強調
d.ellipse((ocx - 82, ocy - 82, ocx + 82, ocy + 82), outline=RED, width=3)
ctext(d, ocx + 120, ocy - 70, "重合部(内挿域)", FS, RED)
note(d, "重合部で相互に内挿 / 密度は同程度が良い / 線形内挿は保存性を厳密には満たさない")
save(im, "t2f5Overset")


# ============================================================ t2f5HexTetPrism 六面体/四面体/プリズム
im, d = new()
title(d, "四面体 / 六面体 / プリズム格子")
# 六面体 -> 四面体分割
ox, oy, w, h, dp = 70, 130, 140, 130, 80
iso_box(d, ox, oy, w, h, dp)
dx, dy = int(dp * 0.8), int(dp * 0.5)
# 内部対角線(四面体分割の模式)
dashed(d, ox, oy, ox + w, oy + h, RED, 2, 9)
dashed(d, ox, oy, ox + w + dx, oy + h - dy, RED, 2, 9)
dashed(d, ox + w, oy, ox, oy + h, RED, 2, 9)
ctext(d, ox + w / 2, oy + h + 40, "1 六面体 ~ 5〜6 四面体", FS, BLUE)
ctext(d, ox + w / 2, oy + h + 64, "(同分解能で四面体はセル数 多)", FT, GRAY)
# プリズム(境界層)
wx0, wx1, wy = 380, 610, 300
hwall(d, wx0, wx1, wy, side=1)
ctext(d, (wx0 + wx1) / 2, wy + 28, "壁面", FT, GRAY)
ys = [wy, wy - 16, wy - 36, wy - 62, wy - 96]
for yy in ys:
    d.line((wx0, yy, wx1, yy), fill=GREEN, width=2)
for xx in range(wx0, wx1 + 1, 46):
    d.line((xx, wy, xx, wy - 96), fill=GREEN, width=1)
ctext(d, (wx0 + wx1) / 2, 100, "境界層 = プリズム格子", FS, GREEN)
ctext(d, (wx0 + wx1) / 2, 124, "格子線を壁面に直交させる", FT, GRAY)
note(d, "四面体=複雑形状に強いが必ず非構造・セル数多 / 六面体=節約 / 壁近傍はプリズム")
save(im, "t2f5HexTetPrism")


print("done")
