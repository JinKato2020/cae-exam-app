# -*- coding: utf-8 -*-
"""熱流体力学2級 第5章「格子生成法」の図(接頭辞 t2e5)を15枚描く。
JSON本体は編集しない。white 660x420 線画・機構だけ。
required(回答前表示)には答え・正解値・結論を絶対に描かない(§3/§8)。
required=5問: t2e5StructVsUnstruct, t2e5CartesianStaircase, t2e5StretchLayers,
              t2e5OctreeSplit, t2e5OversetGrids"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- ローカル補助(ch4スクリプトと同一書式) -----------------------
def box(d, cx, cy, w, h, text, fnt=FS, fill="white"):
    """中央(cx,cy)の矩形＋中央テキスト。text は改行\n可。"""
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=BLACK, width=3, fill=fill)
    lines = text.split("\n")
    lh = fnt.size + 6
    y0 = cy - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        ctext(d, cx, y0 + i * lh, ln, fnt)


def table(d, x, y, rows, col_w, row_h=44, fnt=FT, hfnt=FS):
    """rows: 2次元リスト(1行目=見出し)。col_w: 各列幅。左詰めセル。"""
    xs = [x]
    for w in col_w:
        xs.append(xs[-1] + w)
    tw = sum(col_w)
    nrow = len(rows)
    d.rectangle((x, y, x + tw, y + row_h), fill=FILL2)
    for i in range(nrow + 1):
        yy = y + i * row_h
        d.line((x, yy, x + tw, yy), fill=BLACK, width=2)
    for xx in xs:
        d.line((xx, y, xx, y + nrow * row_h), fill=BLACK, width=2)
    for r, row in enumerate(rows):
        f = hfnt if r == 0 else fnt
        for c, cell in enumerate(row):
            d.text((xs[c] + 8, y + r * row_h + row_h / 2), cell,
                   font=f, fill=BLACK, anchor="lm")


# ==================================================================
# 5-1 required : 構造格子(規則的な四角形)と非構造格子(不規則な三角形)の対比
# (データ構造の説明・正解は描かない)
def f01():
    im, d = new()
    title(d, "構造格子と非構造格子の見た目")
    # --- 左: 構造格子(規則的な正方形セル) ---
    x0, y0, cw, n = 55, 90, 42, 6
    for i in range(n + 1):
        d.line((x0, y0 + i * cw, x0 + n * cw, y0 + i * cw), fill=BLUE, width=2)
        d.line((x0 + i * cw, y0, x0 + i * cw, y0 + n * cw), fill=BLUE, width=2)
    ctext(d, x0 + n * cw / 2, y0 + n * cw + 30, "構造格子", F)
    ctext(d, x0 + n * cw / 2, y0 + n * cw + 58, "(規則的に並ぶ四角形)", FT, GRAY)
    # --- 右: 非構造格子(不規則な三角形) ---
    bx, by, bw, bh, m = 400, 90, 210, 252, 5
    pts = {}
    for j in range(m + 1):
        for i in range(m + 1):
            px = bx + i * bw / m
            py = by + j * bh / m
            if 0 < i < m and 0 < j < m:  # 内部だけ規則性を崩す
                px += 13 * math.sin(i * 1.7 + j * 2.3)
                py += 13 * math.cos(i * 2.1 + j * 1.3)
            pts[(i, j)] = (px, py)
    for j in range(m):
        for i in range(m):
            a, b = pts[(i, j)], pts[(i + 1, j)]
            c, e = pts[(i, j + 1)], pts[(i + 1, j + 1)]
            # 対角向きも交互に変えて不規則感を出す
            if (i + j) % 2 == 0:
                tris = [(a, b, e), (a, e, c)]
            else:
                tris = [(a, b, c), (b, e, c)]
            for t in tris:
                d.polygon(list(t), outline=RED, width=2)
    ctext(d, bx + bw / 2, by + bh + 30, "非構造格子", F)
    ctext(d, bx + bw / 2, by + bh + 58, "(不規則に並ぶ三角形)", FT, GRAY)
    save(im, "t2e5StructVsUnstruct")


# 5-2 required : 直交格子に曲線境界を重ね、階段状に近似される様子
# (正解は描かない)
def f02():
    im, d = new()
    title(d, "直交格子による境界の階段状近似")
    x0, y0, cw, n = 70, 80, 45, 11
    ny = 6
    # 直交・等間隔格子
    for i in range(n + 1):
        d.line((x0 + i * cw, y0, x0 + i * cw, y0 + ny * cw), fill=LGRAY, width=1)
    for j in range(ny + 1):
        d.line((x0, y0 + j * cw, x0 + n * cw, y0 + j * cw), fill=LGRAY, width=1)
    # 実際の曲線境界(円弧)
    cx, cy, R = x0 + n * cw + 40, y0 + ny * cw + 40, 320
    arc = []
    a = math.pi
    while a <= math.pi * 1.5 + 0.001:
        arc.append((cx + R * math.cos(a), cy + R * math.sin(a)))
        a += 0.02
    plot(d, 0, 0, arc, RED, 3)
    # 格子に沿った階段状近似(セル辺のみでたどる)
    step = []
    for i in range(n + 1):
        xx = x0 + i * cw
        # この列で境界(円)より内側になる最下段セル境界を求める
        best = None
        for j in range(ny + 1):
            yy = y0 + j * cw
            if (xx - cx) ** 2 + (yy - cy) ** 2 >= R ** 2:
                best = yy
                break
        if best is None:
            best = y0 + ny * cw
        step.append((xx, best))
    stair = []
    for i in range(len(step)):
        stair.append(step[i])
        if i + 1 < len(step):
            stair.append((step[i + 1][0], step[i][1]))  # 横→縦で階段
    plot(d, 0, 0, stair, BLUE, 3)
    ctext(d, x0 + 120, y0 + 24, "実際の境界(曲線)", FS, RED, "lm")
    ctext(d, x0 + 60, y0 + ny * cw - 20, "格子による階段状近似", FS, BLUE, "lm")
    save(im, "t2e5CartesianStaircase")


# 5-3 helpful : 生成法の分類(構造/非構造)の2列対比表
def f03():
    im, d = new()
    title(d, "格子生成法の分類")
    rows = [
        ["構造格子の生成法", "非構造格子の生成法"],
        ["マルチブロック法", "デローニー分割法"],
        ["代数的方法", "アドバンシングフロント法"],
        ["偏微分方程式法", "ボロノイ分割法"],
    ]
    table(d, 55, 110, rows, [270, 285], row_h=62, fnt=FS)
    save(im, "t2e5GenMethodClass")


# 5-4 required : 壁面から等比拡大する境界層格子 (Δ1=0.2mm, r=1.25)
# (答え=Δ3の値は描かない)
def f04():
    im, d = new()
    title(d, "境界層格子の等比ストレッチ")
    wy = 350           # 壁面(下端)
    x0, x1 = 120, 470
    hwall(d, x0 - 10, x1 + 10, wy, side=1)  # 壁(下にハッチ)
    d1 = 20            # 第1層の画素高さ
    r = 1.25
    ys = [wy]
    h = d1
    for k in range(6):
        ys.append(ys[-1] - h)
        h *= r
    # 水平な格子線
    for yy in ys:
        d.line((x0, yy, x1, yy), fill=BLUE, width=2)
    # 縦の格子線(セルらしく)
    for i in range(6):
        xx = x0 + i * (x1 - x0) / 5
        d.line((xx, ys[0], xx, ys[-1]), fill=LGRAY, width=1)
    # Δ1,Δ2,Δ3 の寸法(右側)
    dx = x1 + 30
    labs = ["Δ1", "Δ2", "Δ3"]
    for k in range(3):
        dim(d, dx, ys[k], dx, ys[k + 1], labs[k], col=GRAY)
    ctext(d, x0 + (x1 - x0) / 2, wy + 40, "壁面", FS, BLACK)
    ctext(d, W / 2, 66, "Δ1 = 0.2 mm,  拡大比 r = 1.25", F)
    note(d, "外側へ向かって格子幅を一定比で拡大していく")
    save(im, "t2e5StretchLayers")


# 5-5 helpful : r法/h法/p法 の対比表
def f05():
    im, d = new()
    title(d, "解適合格子の r法・h法・p法")
    rows = [
        ["手法", "操作の内容", "適用できる格子"],
        ["r法", "格子点を移動(総数は不変)", "構造・非構造"],
        ["h法", "格子点を追加・削除", "主に非構造"],
        ["p法", "要素内の近似次数を上げる", "有限要素法"],
    ]
    table(d, 30, 95, rows, [90, 300, 220], row_h=68, fnt=FS)
    save(im, "t2e5RHPmethods")


# 5-6 required : 8分木細分化 (1セル→8個、2段階目は?)
# (末端セルの総数=答えは描かない)
def f06():
    im, d = new()
    title(d, "8分木(オクトツリー)格子の細分化")
    # 親セル1個
    iso_box(d, 80, 200, 90, 90, 60)
    ctext(d, 145, 320, "親セル 1個", FS)
    arrow(d, 210, 220, 290, 220, BLACK, 3, 13)
    ctext(d, 250, 196, "各方向に\n2分割", FT, GRAY)
    # 分割後(8個の子セル): 立方体に中面線を入れて8分割を示す
    ox, oy, w, h, dp = 315, 200, 90, 90, 60
    iso_box(d, ox, oy, w, h, dp)
    dx, dy = int(dp * 0.8), int(dp * 0.5)
    # 前面の中線
    d.line((ox + w / 2, oy, ox + w / 2, oy + h), fill=BLACK, width=2)
    d.line((ox, oy + h / 2, ox + w, oy + h / 2), fill=BLACK, width=2)
    # 上面の中線
    d.line((ox + dx / 2, oy - dy / 2, ox + w + dx / 2, oy - dy / 2), fill=BLACK, width=2)
    d.line((ox + w / 2, oy, ox + w / 2 + dx, oy - dy), fill=BLACK, width=2)
    # 右面の中線
    d.line((ox + w, oy + h / 2, ox + w + dx, oy + h / 2 - dy), fill=BLACK, width=2)
    d.line((ox + w + dx / 2, oy - dy / 2, ox + w + dx / 2, oy + h - dy / 2), fill=BLACK, width=2)
    ctext(d, ox + w / 2, oy + h + 40, "8個の子セル", FS)
    arrow(d, ox + w + dx + 15, 220, ox + w + dx + 95, 220, BLACK, 3, 13)
    ctext(d, ox + w + dx + 55, 196, "さらに\n2段階目", FT, GRAY)
    # 2段階目は ? で示す(答えは描かない)
    box(d, 560, 220, 80, 80, "?", FL, fill=FILL1)
    note(d, "各セルを x・y・z 方向に2分割 → 子セルは8個")
    save(im, "t2e5OctreeSplit")


# 5-7 required : 重合(オーバーセット)格子。背景直交格子＋物体まわりの格子、重合部を強調
# (正解は描かない)
def f07():
    im, d = new()
    title(d, "重合(オーバーセット)格子")
    # 背景の直交格子
    x0, y0, cw, nx, ny = 60, 80, 45, 12, 6
    for i in range(nx + 1):
        d.line((x0 + i * cw, y0, x0 + i * cw, y0 + ny * cw), fill=LGRAY, width=1)
    for j in range(ny + 1):
        d.line((x0, y0 + j * cw, x0 + nx * cw, y0 + j * cw), fill=LGRAY, width=1)
    ctext(d, x0 + 6, y0 + ny * cw + 22, "背景格子(直交)", FS, GRAY, "lm")
    # 物体まわりのO型格子(同心円＋放射線)
    cx, cy = x0 + nx * cw / 2, y0 + ny * cw / 2
    rings = [26, 55, 84]
    for R in rings:
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLUE, width=2)
    for k in range(12):
        a = k * math.pi / 6
        d.line((cx + rings[0] * math.cos(a), cy + rings[0] * math.sin(a),
                cx + rings[-1] * math.cos(a), cy + rings[-1] * math.sin(a)),
               fill=BLUE, width=1)
    # 物体
    d.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cx, cy, "物体", FT)
    # 重合部(外側リング)を赤で強調
    R = rings[-1]
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=RED, width=3)
    arrow(d, cx + R + 70, cy - 60, cx + R * 0.92, cy - R * 0.38, RED, 3, 12)
    ctext(d, cx + R + 74, cy - 66, "重合部(内挿でつなぐ)", FS, RED, "lm")
    save(im, "t2e5OversetGrids")


# 5-8 helpful : 計算空間(ξ,η)の単位正方形 → 物理空間(x,y)の長方形 の写像
# (ヤコビアンの値=答えは描かない)
def f08():
    im, d = new()
    title(d, "計算空間から物理空間への写像")
    # 左: 計算空間 単位正方形(2x2 分割)
    lx, ly, s = 70, 120, 150
    for i in range(3):
        d.line((lx + i * s / 2, ly, lx + i * s / 2, ly + s), fill=BLUE, width=2)
        d.line((lx, ly + i * s / 2, lx + s, ly + i * s / 2), fill=BLUE, width=2)
    axes(d, lx, ly + s + 20, 90, 90, "ξ", "η")
    ctext(d, lx + s / 2, ly - 20, "計算空間 (ξ,η)", FS)
    ctext(d, lx + s / 2, ly + s / 2, "1×1", FT, GRAY)
    # 右: 物理空間 長方形(幅2, 高さ3 の比)
    rx, ry = 400, 100
    rw, rh = 130, 195
    for i in range(3):
        d.line((rx + i * rw / 2, ry, rx + i * rw / 2, ry + rh), fill=RED, width=2)
        d.line((rx, ry + i * rh / 2, rx + rw, ry + i * rh / 2), fill=RED, width=2)
    axes(d, rx, ry + rh + 20, 100, 130, "x", "y")
    ctext(d, rx + rw / 2, ry - 20, "物理空間 (x,y)", FS)
    dim(d, rx, ry + rh + 46, rx + rw, ry + rh + 46, "x=2ξ", col=GRAY)
    dim(d, rx + rw + 30, ry, rx + rw + 30, ry + rh, "y=3η", col=GRAY)
    # 写像矢印
    arrow(d, lx + s + 25, ly + s / 2, rx - 25, ry + rh / 2, BLACK, 3, 15)
    ctext(d, (lx + s + rx) / 2, ly + s / 2 - 24, "写像\nx=2ξ, y=3η", FT, BLACK)
    save(im, "t2e5JacobianMap")


# 5-9 helpful : 構造格子の生成法の分類ツリー
def f09():
    im, d = new()
    title(d, "構造格子の生成法の分類")
    box(d, W / 2, 80, 300, 46, "構造格子の生成法", FS, fill=FILL2)
    # 2枝
    lx, rx, y2 = 200, 460, 175
    box(d, lx, y2, 250, 60, "代数的方法\n(補間関数・写像関数)", FT, fill=FILL1)
    box(d, rx, y2, 220, 46, "偏微分方程式法", FS, fill=FILL1)
    arrow(d, W / 2 - 60, 103, lx, y2 - 30, BLACK, 2, 11)
    arrow(d, W / 2 + 60, 103, rx, y2 - 23, BLACK, 2, 11)
    # PDE法の3型
    types = [("楕円型", 380), ("放物型", 460), ("双曲型", 540)]
    ty = 320
    for lab, tx in types:
        box(d, tx, ty, 74, 46, lab, FS)
        arrow(d, rx, y2 + 23, tx, ty - 23, BLACK, 2, 10)
    save(im, "t2e5GenMethodTree")


# 5-10 helpful : 翼型まわりの O型・C型・H型 トポロジー
def f10():
    im, d = new()
    title(d, "境界適合格子のトポロジー")

    def airfoil(cx, cy, w=34, h=13):
        d.ellipse((cx - w, cy - h, cx + w, cy + h), outline=BLACK, width=3, fill=FILL3)

    # O型: 物体を1周する閉じた格子線(同心)
    cx, cy = 130, 210
    for R in (30, 52, 74):
        d.ellipse((cx - R - 8, cy - R, cx + R + 8, cy + R), outline=BLUE, width=2)
    for k in range(8):
        a = k * math.pi / 4
        d.line((cx + 30 * math.cos(a), cy + 30 * math.sin(a),
                cx + (82) * math.cos(a), cy + 74 * math.sin(a)), fill=BLUE, width=1)
    airfoil(cx, cy)
    ctext(d, cx, cy + 110, "O型", F)
    ctext(d, cx, cy + 138, "物体を1周", FT, GRAY)

    # C型: 前方〜上下を包み、後方に切れ目(後流)
    cx, cy = 340, 205
    R1, R2 = 58, 80
    d.arc((cx - R1, cy - R1, cx + R1, cy + R1), 45, 315, fill=BLUE, width=2)
    d.arc((cx - R2, cy - R2, cx + R2, cy + R2), 45, 315, fill=BLUE, width=2)
    for R in (R1, R2):
        for sgn in (1, -1):
            yy = cy + sgn * R * math.sin(math.radians(45))
            d.line((cx + R * math.cos(math.radians(45)), yy, cx + 110, yy), fill=BLUE, width=2)
    for k in range(5):
        a = math.radians(90 + k * 45)
        d.line((cx + R1 * math.cos(a), cy + R1 * math.sin(a),
                cx + R2 * math.cos(a), cy + R2 * math.sin(a)), fill=BLUE, width=1)
    airfoil(cx - 6, cy)
    ctext(d, cx, cy + 110, "C型", F)
    ctext(d, cx, cy + 138, "後方に切れ目", FT, GRAY)

    # H型: 格子線が交差せず通り抜ける
    cx, cy = 545, 205
    for xx in range(cx - 70, cx + 71, 28):
        d.line((xx, cy - 80, xx, cy + 80), fill=BLUE, width=2)
    for yy in range(cy - 80, cy + 81, 27):
        d.line((cx - 70, yy, cx + 70, yy), fill=BLUE, width=2)
    airfoil(cx, cy)
    ctext(d, cx, cy + 110, "H型", F)
    ctext(d, cx, cy + 138, "交差せず通り抜け", FT, GRAY)
    save(im, "t2e5GridTopologies")


# 5-11 helpful : 噴流の出口付近・剪断層に格子を集中(粗密の対比)
def f11():
    im, d = new()
    title(d, "格子点の集中(噴流の例)")
    # ノズル(左)
    nx, ny = 70, 210
    d.line((nx, ny - 40, nx + 60, ny - 22), fill=BLACK, width=3)
    d.line((nx, ny + 40, nx + 60, ny + 22), fill=BLACK, width=3)
    ctext(d, nx + 10, ny - 60, "ノズル出口", FT, BLACK, "lm")
    # 剪断層(噴流の上下縁): 出口から広がる
    top = [(nx + 60, ny - 22), (300, ny - 55), (600, ny - 85)]
    bot = [(nx + 60, ny + 22), (300, ny + 55), (600, ny + 85)]
    plot(d, 0, 0, top, RED, 2)
    plot(d, 0, 0, bot, RED, 2)
    # 縦の格子線: 出口付近は密、遠方は粗
    xs = [80, 100, 122, 148, 180, 300, 440, 590]
    for xx in xs:
        # 上下縁を線形補間
        def edge(pts, x):
            for i in range(len(pts) - 1):
                if pts[i][0] <= x <= pts[i + 1][0]:
                    t = (x - pts[i][0]) / (pts[i + 1][0] - pts[i][0])
                    return pts[i][1] + t * (pts[i + 1][1] - pts[i][1])
            return pts[-1][1]
        yt, yb = edge(top, xx), edge(bot, xx)
        d.line((xx, yt, xx, yb), fill=BLUE, width=1)
    ctext(d, 150, ny + 100, "出口付近=密", FS, BLUE)
    ctext(d, 150, ny - 92, "剪断層=密", FS, RED)
    ctext(d, 520, ny + 108, "遠方=粗", FS, GRAY)
    note(d, "物理量の変化が大きい領域ほど格子を細かくする")
    save(im, "t2e5Clustering")


# 5-12 helpful : 代数的格子生成の要素 + マルチグリッド法は別枠(解法の加速)
def f12():
    im, d = new()
    title(d, "代数的格子生成法の構成要素")
    box(d, 220, 110, 320, 56, "1次元(線上):\ntan・tanh・スプライン関数", FT, fill=FILL1)
    box(d, 220, 195, 320, 56, "面・空間:\ntransfinite内挿(混合関数)", FT, fill=FILL1)
    box(d, 220, 280, 320, 46, "簡単な形状: 写像関数", FS, fill=FILL1)
    ctext(d, 220, 340, "↑ これらが格子を生成する", FT, GRAY)
    # 別枠: マルチグリッド法
    d.rectangle((440, 150, 640, 300), outline=RED, width=3)
    ctext(d, 540, 178, "マルチグリッド法", FS, RED)
    ctext(d, 540, 218, "= 連立方程式の", FT, BLACK)
    ctext(d, 540, 244, "収束を速める解法", FT, BLACK)
    ctext(d, 540, 278, "(格子生成ではない)", FT, RED)
    save(im, "t2e5AlgebraicGen")


# 5-13 helpful : 偏微分方程式による格子生成の3型 対比表
def f13():
    im, d = new()
    title(d, "偏微分方程式による格子生成の型")
    rows = [
        ["型", "解き方", "特徴"],
        ["楕円型", "境界値問題(全境界に条件)", "平滑な格子・平滑化に利用"],
        ["双曲型", "物体表面から外へ解き進める", "直交性良・外部境界形状は不可制御"],
        ["放物型", "外部境界から内へ解き進める", "内部境界形状は不可制御"],
    ]
    table(d, 25, 95, rows, [80, 250, 280], row_h=68, fnt=FT)
    save(im, "t2e5PdeGridTypes")


# 5-14 helpful : 幾何形状入力フォーマットの一覧(CAD系 vs ASCIIは符号化方式)
def f14():
    im, d = new()
    title(d, "幾何形状の入力フォーマット")
    rows = [
        ["形式", "種別", "内容"],
        ["STEP", "CAD (ISO国際標準)", "製品データの表現・交換"],
        ["IGES", "CAD (中間フォーマット)", "3次元データの交換"],
        ["STL", "CAD (表面の三角形分割)", "表面を三角形で近似"],
        ["ASCII", "文字の符号化方式", "CADフォーマットではない"],
    ]
    table(d, 25, 85, rows, [110, 230, 270], row_h=58, fnt=FT)
    save(im, "t2e5CadFormats")


# 5-15 helpful : 1個の六面体→複数の四面体、壁面の境界層はプリズム格子
# (セル数=答えは描かない)
def f15():
    im, d = new()
    title(d, "六面体・四面体・プリズム格子")
    # 左: 1個の六面体 → 複数の四面体
    iso_box(d, 60, 160, 84, 84, 54)
    ctext(d, 115, 285, "六面体1個", FS)
    arrow(d, 185, 190, 255, 190, BLACK, 3, 13)
    ctext(d, 220, 168, "分割", FT, GRAY)
    # 四面体(いくつか)のかたまり: 三角形をいくつか重ねて示す
    tx, ty = 270, 150
    tets = [
        [(tx, ty + 90), (tx + 55, ty), (tx + 95, ty + 70)],
        [(tx, ty + 90), (tx + 95, ty + 70), (tx + 45, ty + 120)],
        [(tx + 55, ty), (tx + 110, ty + 30), (tx + 95, ty + 70)],
    ]
    for t in tets:
        d.polygon(t, outline=BLACK, width=2, fill=FILL1)
    ctext(d, tx + 55, ty + 150, "四面体 5〜6個", FS, RED)
    # 右: 壁面の境界層プリズム格子(壁に直交する層状セル)
    wx0, wx1, wy = 460, 620, 330
    hwall(d, wx0 - 5, wx1 + 5, wy, side=1)
    for j in range(4):
        yy = wy - (j + 1) * 18
        d.line((wx0, yy, wx1, yy), fill=BLUE, width=2)
    for i in range(6):
        xx = wx0 + i * (wx1 - wx0) / 5
        d.line((xx, wy, xx, wy - 4 * 18), fill=BLUE, width=1)
    ctext(d, (wx0 + wx1) / 2, wy + 26, "壁面", FT)
    ctext(d, (wx0 + wx1) / 2, wy - 4 * 18 - 22, "プリズム格子", FS, BLUE)
    ctext(d, (wx0 + wx1) / 2, 120, "(境界層は壁に直交)", FT, GRAY)
    save(im, "t2e5HexTetPrism")


if __name__ == "__main__":
    for fn in [f01, f02, f03, f04, f05, f06, f07, f08,
               f09, f10, f11, f12, f13, f14, f15]:
        fn()
    print("done 15")
