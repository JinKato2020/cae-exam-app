# -*- coding: utf-8 -*-
"""熱流体力学2級 第6章「乱流モデル」の図(接頭辞 t2e6)を16枚描く。
JSON本体は編集しない。white 660x420 線画・機構だけ。ファイル名=figureImage(t2e6_01..16)。
required(回答前表示)には答え・正解値・結論を絶対に描かない(§3/§8)。
required=6問: t2e6_01, t2e6_02, t2e6_07, t2e6_09, t2e6_11, t2e6_12"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- ローカル補助(ch5スクリプトと同一書式) -----------------------
def box(d, cx, cy, w, h, text, fnt=FS, fill="white", oc=BLACK):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=oc, width=3, fill=fill)
    lines = text.split("\n")
    lh = fnt.size + 6
    y0 = cy - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        ctext(d, cx, y0 + i * lh, ln, fnt)


def table(d, x, y, rows, col_w, row_h=44, fnt=FT, hfnt=FS):
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
            d.text((xs[c] + 10, y + r * row_h + row_h / 2), cell,
                   font=f, fill=BLACK, anchor="lm")


def swirl(d, cx, cy, r, col=BLUE, wd=3, a0=20, a1=320):
    """渦(回転矢印)。PIL座標系(y下向き)で a0->a1 度に円弧＋終端に矢印。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    ae = math.radians(a1)
    ap = math.radians(a1 - 22)
    ex, ey = cx + r * math.cos(ae), cy + r * math.sin(ae)
    px, py = cx + r * math.cos(ap), cy + r * math.sin(ap)
    arrow(d, px, py, ex, ey, col, wd, 11)


# ==================================================================
# 6-1 required : 分子粘性による拡散 と 乱流渦による混合 の対比(渦粘性の考え方)
# 数式・答えは描かない
def f01():
    im, d = new()
    title(d, "分子の粘性と乱流の渦による混合")
    # 左: 分子粘性(細かな分子運動でゆっくり混ざる)
    lx, ly, lw, lh = 45, 70, 250, 285
    d.rectangle((lx, ly, lx + lw, ly + lh), outline=LGRAY, width=2)
    ctext(d, lx + lw / 2, ly + 26, "分子粘性による拡散", FS, BLACK)
    # 2層のせん断＋小さな分子運動の矢印
    d.line((lx + 20, ly + 150, lx + lw - 20, ly + 150), fill=GRAY, width=1)
    for i, xx in enumerate(range(lx + 30, lx + lw - 20, 34)):
        s = 1 if i % 2 == 0 else -1
        arrow(d, xx, ly + 150, xx + 8 * s, ly + 150 - 22 * s, GREEN, 2, 7)
        d.ellipse((xx - 4, ly + 150 - 4, xx + 4, ly + 150 + 4), fill=GREEN)
    ctext(d, lx + lw / 2, ly + lh - 26, "分子の細かな運動\n→ 混合はゆっくり", FT, GRAY)
    # 右: 乱流の渦(大小の渦が激しくかき混ぜる)
    rx, ry, rw, rh = 365, 70, 250, 285
    d.rectangle((rx, ry, rx + rw, ry + rh), outline=LGRAY, width=2)
    ctext(d, rx + rw / 2, ry + 26, "乱流の渦による混合", FS, BLACK)
    swirl(d, rx + 75, ry + 120, 42, BLUE, 3)
    swirl(d, rx + 175, ry + 105, 30, RED, 3)
    swirl(d, rx + 130, ry + 185, 48, BLUE, 3)
    swirl(d, rx + 200, ry + 190, 22, RED, 2)
    swirl(d, rx + 60, ry + 210, 24, RED, 2)
    ctext(d, rx + rw / 2, ry + rh - 26, "大小の渦が運動量を\n激しくかき混ぜる", FT, GRAY)
    note(d, "渦が『粘性が大きくなったように』運動量を混ぜる = 渦粘性の考え方")
    save(im, "t2e6_01")


# 6-2 required : 微小立方体に垂直応力(面に垂直)とせん断応力(面に沿う)を描き分け
# 2k などの結論は描かない
def f02():
    im, d = new()
    title(d, "流体要素にはたらく応力の向き")
    ox, oy, w, h, dp = 240, 150, 130, 130, 78
    iso_box(d, ox, oy, w, h, dp)
    dx, dy = int(dp * 0.8), int(dp * 0.5)
    # 垂直応力: 各面から外向き(面に垂直)
    fcx = ox + w / 2
    arrow(d, fcx, oy + h + 8, fcx, oy + h + 52, RED, 4, 14)      # 下面 垂直
    arrow(d, ox - 8, oy + h / 2, ox - 44, oy + h / 2, RED, 4, 13)   # 左面(前面)に垂直
    ctext(d, fcx, oy + h + 66, "垂直応力", FS, RED)
    ctext(d, fcx, oy + h + 88, "(面に垂直・対角成分)", FT, RED)
    # せん断応力: 前面に沿う矢印(横方向) + 右面に沿う矢印(縦方向)
    arrow(d, ox + 14, oy + 24, ox + w - 14, oy + 24, BLUE, 4, 13)   # 前面上辺に沿う
    arrow(d, ox + w + dx - 6, oy - dy + 16, ox + w + dx - 6, oy - dy + h - 16, BLUE, 4, 13)  # 右面に沿う縦
    ctext(d, ox + w / 2, oy - 40, "せん断応力(面に沿う=非対角成分)", FS, BLUE)
    save(im, "t2e6_02")


# 6-3 helpful : DNS / LES / RANS で解像する渦と格子の細かさの3段対比
# Re^(9/4)の値や倍率は書かない
def f03():
    im, d = new()
    title(d, "DNS・LES・RANS の解像度の違い")
    rows = [("DNS", "すべての渦を格子で解像", 14, "fine"),
            ("LES", "大きな渦は計算・小さい渦はモデル化", 26, "mix"),
            ("RANS", "平均場のみ(渦は解かない)", 0, "mean")]
    gx, gw, gh = 150, 150, 78
    for k, (name, desc, cw, kind) in enumerate(rows):
        gy = 70 + k * 108
        box(d, 80, gy + gh / 2, 90, 46, name, FS, fill=FILL2)
        # 格子＋渦の模式
        d.rectangle((gx, gy, gx + gw, gy + gh), outline=BLACK, width=2)
        if kind == "fine":
            for xx in range(gx, gx + gw + 1, 14):
                d.line((xx, gy, xx, gy + gh), fill=LGRAY, width=1)
            for yy in range(gy, gy + gh + 1, 14):
                d.line((gx, yy, gx + gw, yy), fill=LGRAY, width=1)
            swirl(d, gx + 45, gy + 40, 22, BLUE, 2)
            swirl(d, gx + 100, gy + 30, 12, RED, 2)
            swirl(d, gx + 110, gy + 58, 8, RED, 2)
        elif kind == "mix":
            for xx in range(gx, gx + gw + 1, 30):
                d.line((xx, gy, xx, gy + gh), fill=LGRAY, width=1)
            for yy in range(gy, gy + gh + 1, 30):
                d.line((gx, yy, gx + gw, yy), fill=LGRAY, width=1)
            swirl(d, gx + 55, gy + 40, 26, BLUE, 2)
            ctext(d, gx + 118, gy + 40, "小渦=\nモデル", FT, GRAY)
        else:
            for yy in range(gy + 14, gy + gh, 20):
                arrow(d, gx + 14, yy, gx + gw - 14, yy, GRAY, 2, 8)
            ctext(d, gx + gw / 2, gy + gh - 12, "平均流のみ", FT, GRAY)
        ctext(d, gx + gw + 16, gy + gh / 2, desc, FT, BLACK, "lm")
    note(d, "下ほど解像する渦が少なく、必要な格子は粗くてよい")
    save(im, "t2e6_03")


# 6-4 helpful : k-εモデル と 応力モデル(RSM) の特徴2列対比表
def f04():
    im, d = new()
    title(d, "k-εモデル と 応力モデル(RSM)")
    rows = [
        ["k-εモデル", "応力モデル(RSM)"],
        ["渦粘性で等方近似", "各応力成分を輸送方程式で解く"],
        ["非等方性は苦手", "非等方性を表現できる"],
        ["計算コスト 低い", "計算コスト 高い"],
        ["計算の安定性 良い", "計算の安定性 劣る"],
    ]
    table(d, 40, 95, rows, [270, 310], row_h=56, fnt=FS)
    save(im, "t2e6_04")


# 6-5 helpful : 渦粘性νt(運動量) と 熱の渦拡散αt(熱) の対比、比=乱流プラントル数Prt
# 計算結果の数値は書かない
def f05():
    im, d = new()
    title(d, "渦粘性 νt と 熱の渦拡散 αt の関係")
    box(d, 175, 150, 250, 90, "渦粘性 νt\n運動量の乱流輸送", FS, fill=FILL1)
    box(d, 485, 150, 250, 90, "熱の渦拡散 αt\n熱の乱流輸送", FS, fill=FILL1)
    arrow(d, 300, 150, 360, 150, BLACK, 3, 13)
    arrow(d, 360, 175, 300, 175, BLACK, 3, 13)
    box(d, 330, 300, 320, 70, "乱流プラントル数\nPrt = νt / αt", F, fill=FILL2)
    arrow(d, 175, 195, 250, 268, GRAY, 2, 11)
    arrow(d, 485, 195, 410, 268, GRAY, 2, 11)
    note(d, "運動量の伝わりやすさと熱の伝わりやすさの比が Prt")
    save(im, "t2e6_05")


# 6-6 helpful : k方程式の収支(生成Pk→散逸-ε、拡散=分子ν+乱流νt)
# どの選択肢が正解かは書かない
def f06():
    im, d = new()
    title(d, "乱流エネルギー k の収支")
    box(d, 330, 200, 220, 90, "乱流エネルギー\nk", F, fill=FILL2)
    # 生成 Pk (左から供給)
    arrow(d, 90, 200, 218, 200, GREEN, 4, 15)
    ctext(d, 150, 170, "生成 Pk", FS, GREEN)
    ctext(d, 150, 232, "平均流から供給", FT, GRAY)
    # 散逸 -ε (右へ 熱として散る)
    arrow(d, 442, 200, 575, 200, RED, 4, 15)
    ctext(d, 520, 170, "散逸 -ε", FS, RED)
    ctext(d, 520, 232, "熱へ", FT, GRAY)
    # 拡散 (上下: 空間へ運ぶ)
    arrow(d, 330, 154, 330, 90, BLUE, 3, 13)
    ctext(d, 330, 74, "拡散: 分子ν + 乱流νt で空間へ運ぶ", FT, BLUE)
    arrow(d, 330, 246, 330, 310, BLUE, 3, 13)
    ctext(d, 330, 330, "拡散(空間へ)", FT, BLUE)
    note(d, "(非定常)+(対流) = 生成 - 散逸 + 拡散  の構造")
    save(im, "t2e6_06")


# 6-7 required : チャネル乱流の設定図(平行平板・x/y/z座標・壁付近の速度分布)
# 応力の大小関係や答えは描かない
def f07():
    im, d = new()
    title(d, "平行平板間の完全発達乱流(チャネル乱流)")
    x0, x1 = 110, 560
    yt, yb = 100, 320
    hwall(d, x0 - 10, x1 + 10, yt, side=-1)   # 上壁(上にハッチ)
    hwall(d, x0 - 10, x1 + 10, yb, side=1)    # 下壁(下にハッチ)
    ctext(d, x1 + 6, yt - 8, "上壁", FT, BLACK, "lm")
    ctext(d, x1 + 6, yb + 8, "下壁", FT, BLACK, "lm")
    # 速度分布 U(y): 壁で0、中央で最大(右向き矢印を各高さに)
    xc = 230
    ymid = (yt + yb) / 2
    Hh = (yb - yt) / 2
    for yy in range(yt + 12, yb - 6, 20):
        f = 1 - ((yy - ymid) / Hh) ** 2
        arrow(d, xc, yy, xc + 150 * f, yy, BLUE, 2, 8)
    d.line((xc, yt, xc, yb), fill=GRAY, width=1)
    ctext(d, xc + 165, ymid, "平均速度 U(y)", FT, BLUE, "lm")
    # 座標軸 x(流れ) y(壁垂直) z(スパン=奥行)
    ax, ay = 150, 250
    arrow(d, ax, ay, ax + 70, ay, BLACK, 2, 11)
    ctext(d, ax + 80, ay, "x(流れ方向)", FT, BLACK, "lm")
    arrow(d, ax, ay, ax, ay - 60, BLACK, 2, 11)
    ctext(d, ax - 6, ay - 74, "y(壁垂直)", FT, BLACK, "mm")
    arrow(d, ax, ay, ax + 34, ay + 24, BLACK, 2, 10)
    ctext(d, ax + 40, ay + 30, "z(スパン)", FT, BLACK, "lm")
    save(im, "t2e6_07")


# 6-8 helpful : 標準k-εモデルのモデル定数 標準値一覧表
def f08():
    im, d = new()
    title(d, "標準 k-εモデルのモデル定数")
    rows = [
        ["定数", "標準値", "役割"],
        ["Cμ", "0.09", "渦粘性 νt=Cμ k²/ε の係数"],
        ["σk", "1.0", "k の拡散(乱流プラントル数)"],
        ["σε", "1.3", "ε の拡散"],
        ["Cε1", "1.44", "ε方程式の生成側定数"],
        ["Cε2", "1.92", "ε方程式の散逸側定数"],
    ]
    table(d, 45, 80, rows, [90, 110, 370], row_h=52, fnt=FS)
    save(im, "t2e6_08")


# 6-9 required : 壁近傍の層構造(粘性底層→バッファ層→対数則) 概念図
# 縦=速度、横=壁からの距離。どのモデルが正しいかは書かない
def f09():
    im, d = new()
    title(d, "壁面近傍の乱流の層構造")
    ox, oy = 95, 340
    xlen, ylen = 430, 250
    axes(d, ox, oy, xlen, ylen, "壁からの距離", "速度")
    # 3層の帯
    bands = [(ox, ox + 100, FILL1, "粘性\n底層"),
             (ox + 100, ox + 195, FILL2, "バッファ層"),
             (ox + 195, ox + xlen - 10, FILL3, "対数速度分布の領域")]
    for xa, xb, col, lab in bands:
        d.rectangle((xa, oy - ylen + 6, xb, oy), fill=col, outline=None)
        d.line((xb, oy - ylen + 6, xb, oy), fill=LGRAY, width=1)
        ctext(d, (xa + xb) / 2, oy - ylen + 24, lab, FT, GRAY)
    # 速度分布曲線: 壁近傍は急、外側でゆるやかに増加
    pts = []
    for i in range(0, 421, 8):
        xx = ox + i
        u = 250 * (1 - math.exp(-i / 60.0)) * (0.55 + 0.09 * math.log10(i + 2))
        u = min(u, 240)
        pts.append((xx, oy - u))
    plot(d, 0, 0, pts, BLUE, 3)
    note(d, "壁のごく近くほど速度が急に変化する")
    save(im, "t2e6_09")


# 6-10 helpful : RANS渦粘性モデルを解く輸送方程式の数で分類した表
def f10():
    im, d = new()
    title(d, "RANS乱流モデルの分類(輸送方程式の数)")
    rows = [
        ["方程式数", "モデル", "渦粘性の求め方"],
        ["0方程式", "混合長 / Baldwin-Lomax", "代数式(壁距離など)"],
        ["1方程式", "Spalart-Allmaras", "渦粘性相当量の輸送方程式"],
        ["2方程式", "k-ε / k-ω / SST", "k と ε(またはω)の輸送方程式"],
    ]
    table(d, 25, 110, rows, [110, 240, 280], row_h=64, fnt=FT)
    save(im, "t2e6_10")


# 6-11 required : 速度境界層(厚)と温度境界層(高Prで薄)の厚さの違い
# どのモデルが正しいかは書かない
def f11():
    im, d = new()
    title(d, "速度境界層と温度境界層(高プラントル数流体)")
    x0, x1 = 90, 590
    wy = 330
    hwall(d, x0 - 10, x1 + 10, wy, side=1)     # 壁(下にハッチ)
    ctext(d, x1 + 4, wy + 6, "壁面", FT, BLACK, "lm")
    # 速度境界層(厚い): 上に立ち上がる曲線
    velo = []
    for i in range(0, 501, 8):
        xx = x0 + i
        d0 = 150 * (0.4 + 0.6 * (i / 500.0) ** 0.5)   # 境界層厚さの伸び
        velo.append((xx, wy - d0))
    plot(d, 0, 0, velo, BLUE, 3)
    # 温度境界層(薄い): 速度より低い高さ
    temp = []
    for i in range(0, 501, 8):
        xx = x0 + i
        d0 = 70 * (0.4 + 0.6 * (i / 500.0) ** 0.5)
        temp.append((xx, wy - d0))
    plot(d, 0, 0, temp, RED, 3)
    ctext(d, x1 - 40, wy - 150, "速度境界層(厚い)", FS, BLUE, "rm")
    ctext(d, x1 - 40, wy - 62, "温度境界層(薄い)", FS, RED, "rm")
    # 壁近傍の急な温度勾配を矢印で
    dim(d, x0 + 120, wy, x0 + 120, wy - 84, "δ", col=BLUE)
    dim(d, x0 + 60, wy, x0 + 60, wy - 40, "δT", col=RED)
    note(d, "高プラントル数流体では温度境界層が速度境界層より薄い")
    save(im, "t2e6_11")


# 6-12 required : LESの考え方(格子Δ以上の大渦は直接計算、Δ以下はSGSモデル)
# 計算結果の数値は書かない
def f12():
    im, d = new()
    title(d, "LES: 大きな渦は計算・小さな渦はモデル化")
    x0, y0, cw, nx, ny = 90, 80, 46, 10, 5
    for i in range(nx + 1):
        d.line((x0 + i * cw, y0, x0 + i * cw, y0 + ny * cw), fill=LGRAY, width=1)
    for j in range(ny + 1):
        d.line((x0, y0 + j * cw, x0 + nx * cw, y0 + j * cw), fill=LGRAY, width=1)
    # フィルター幅Δ(=1セル)を寸法で示す
    dim(d, x0, y0 - 16, x0 + cw, y0 - 16, "Δ", col=GRAY)
    ctext(d, x0 + nx * cw + 10, y0 - 16, "フィルター幅Δ(格子幅)", FT, GRAY, "lm")
    # 大きな渦(格子以上): 直接計算
    swirl(d, x0 + 120, y0 + 120, 55, BLUE, 3)
    ctext(d, x0 + 120, y0 + 120, "大きな渦\n(直接計算)", FT, BLUE)
    # 小さな渦(Δ以下): モデル化
    swirl(d, x0 + 330, y0 + 70, 16, RED, 2)
    swirl(d, x0 + 360, y0 + 130, 12, RED, 2)
    swirl(d, x0 + 320, y0 + 160, 10, RED, 2)
    ctext(d, x0 + 345, y0 + 200, "小さな渦(Δ以下)\n=SGSモデルで表す", FT, RED)
    note(d, "格子より大きい渦は解き、小さい渦はサブグリッドモデルで表現")
    save(im, "t2e6_12")


# 6-13 helpful : 3つの解析対象(ア境界層 / イ平行平板 / ウ円柱後流の非定常渦)
# RANS可否の判定結果は書かない
def f13():
    im, d = new()
    title(d, "3つの解析対象")
    # ア: 平板上の乱流境界層(平均速度分布)
    ax0, ax1, ay = 40, 220, 250
    hwall(d, ax0, ax1, ay, side=1, n=7)
    for i, xx in enumerate(range(ax0 + 30, ax1 - 5, 46)):
        for yy in range(ay - 10, ay - 90, -16):
            f = (ay - yy) / 90.0
            arrow(d, xx, yy, xx + 34 * f + 6, yy, BLUE, 2, 7)
    ctext(d, (ax0 + ax1) / 2, ay + 30, "ア. 乱流境界層", FS)
    ctext(d, (ax0 + ax1) / 2, ay + 52, "(平均速度分布)", FT, GRAY)
    # イ: 平行平板間の発達乱流(平均速度分布)
    bx0, bx1 = 250, 410
    byt, byb = 170, 300
    hwall(d, bx0, bx1, byt, side=-1, n=7)
    hwall(d, bx0, bx1, byb, side=1, n=7)
    bmid = (byt + byb) / 2
    Hh = (byb - byt) / 2
    for yy in range(byt + 10, byb - 4, 16):
        f = 1 - ((yy - bmid) / Hh) ** 2
        arrow(d, bx0 + 30, yy, bx0 + 30 + 70 * f, yy, BLUE, 2, 7)
    ctext(d, (bx0 + bx1) / 2, byb + 30, "イ. 平行平板間乱流", FS)
    ctext(d, (bx0 + bx1) / 2, byb + 52, "(平均速度分布)", FT, GRAY)
    # ウ: 円柱後方の非定常なカルマン渦列
    ccx, ccy = 470, 230
    d.ellipse((ccx - 16, ccy - 16, ccx + 16, ccy + 16), outline=BLACK, width=3, fill=FILL3)
    arrow(d, ccx - 70, ccy, ccx - 30, ccy, GRAY, 2, 9)
    for k, sx in enumerate(range(ccx + 40, ccx + 170, 42)):
        sgn = 1 if k % 2 == 0 else -1
        swirl(d, sx, ccy + sgn * 26, 16, RED, 2,
              a0=0 if sgn > 0 else 180, a1=320 if sgn > 0 else 500)
    ctext(d, ccx + 60, ccy + 80, "ウ. 円柱後流の渦", FS)
    ctext(d, ccx + 60, ccy + 102, "(非定常な渦列)", FT, GRAY)
    save(im, "t2e6_13")


# 6-14 helpful : 円柱まわりの流れをレイノルズ数別に3枚
# どれが定常計算可かは書かない
def f14():
    im, d = new()
    title(d, "円柱まわりの流れのレイノルズ数依存")

    def cyl(cx, cy, r=15):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL3)

    yc = 190
    # Re=1: 上下対称の定常層流(はく離なし)
    cx = 130
    cyl(cx, yc)
    arrow(d, cx - 75, yc, cx - 30, yc, GRAY, 2, 9)
    for sgn in (1, -1):
        pts = [(cx - 15, yc + sgn * 15)]
        for t in range(0, 101, 10):
            xx = cx + t
            yy = yc + sgn * (16 * math.exp(-t / 45.0) + 2)
            pts.append((xx, yy))
        plot(d, 0, 0, pts, BLUE, 2)
    ctext(d, cx, yc + 95, "Re = 1", FS)
    ctext(d, cx, yc + 117, "上下対称・定常", FT, GRAY)
    # Re=100: カルマン渦列(非定常)
    cx = 330
    cyl(cx, yc)
    arrow(d, cx - 75, yc, cx - 30, yc, GRAY, 2, 9)
    for k, sx in enumerate(range(cx + 34, cx + 150, 38)):
        sgn = 1 if k % 2 == 0 else -1
        swirl(d, sx, yc + sgn * 24, 15, RED, 2,
              a0=0 if sgn > 0 else 180, a1=320 if sgn > 0 else 500)
    ctext(d, cx + 40, yc + 95, "Re = 100", FS)
    ctext(d, cx + 40, yc + 117, "カルマン渦・非定常", FT, GRAY)
    # Re=10000: 乱れた乱流後流
    cx = 545
    cyl(cx, yc)
    arrow(d, cx - 70, yc, cx - 30, yc, GRAY, 2, 9)
    for k in range(26):
        a = k * 1.7
        rr = 14 + 6 * math.sin(a * 1.3)
        bx = cx + 30 + (k * 3.2) % 95
        by = yc + 34 * math.sin(a) * math.exp(-((bx - cx) / 130.0))
        swirl(d, bx, by, 7 + (k % 3) * 2, RED, 1, a0=k * 20, a1=k * 20 + 300)
    ctext(d, cx, yc + 95, "Re = 10000", FS)
    ctext(d, cx, yc + 117, "乱れた乱流後流", FT, GRAY)
    save(im, "t2e6_14")


# 6-15 helpful : 対流項の離散化 風上型(渦がにじむ) vs 保存性重視(渦を保つ)
# どちらが望ましいかの結論は書かない
def f15():
    im, d = new()
    title(d, "対流項の離散化と数値粘性")
    # 左: 風上型(数値粘性大 → 渦がにじんで潰れる)
    lx, ly = 60, 80
    d.rectangle((lx, ly, lx + 250, ly + 240), outline=LGRAY, width=2)
    ctext(d, lx + 125, ly + 24, "数値粘性の大きい風上型", FS, BLACK)
    for r in (58, 44, 30):
        col = (150 + (58 - r), 170, 210)
        d.ellipse((lx + 125 - r, ly + 140 - r, lx + 125 + r, ly + 140 + r),
                  outline=col, width=2)
    ctext(d, lx + 125, ly + 210, "渦がにじんで潰れる", FT, GRAY)
    # 右: 保存性重視(数値粘性小 → 渦の形が保たれる)
    rx, ry = 350, 80
    d.rectangle((rx, ry, rx + 250, ry + 240), outline=LGRAY, width=2)
    ctext(d, rx + 125, ry + 24, "数値粘性の小さい保存型", FS, BLACK)
    swirl(d, rx + 125, ry + 140, 58, BLUE, 3)
    swirl(d, rx + 125, ry + 140, 30, BLUE, 3)
    ctext(d, rx + 125, ry + 210, "渦の形が保たれる", FT, GRAY)
    note(d, "離散化により渦の再現性が変わる")
    save(im, "t2e6_15")


# 6-16 required? -> helpful : レイノルズ数の数直線に臨界2300・層流/遷移/発達乱流の帯
# どの手法が正解かは書かない
def f16():
    im, d = new()
    title(d, "臨界レイノルズ数付近の流れの状態")
    x0, x1 = 70, 600
    y = 210
    # 帯(層流 / 遷移 / 発達乱流)
    xc = 300   # 臨界2300の位置
    xt = 470   # 発達乱流の目安
    d.rectangle((x0, y - 26, xc, y + 26), fill=FILL1, outline=None)
    d.rectangle((xc, y - 26, xt, y + 26), fill=FILL2, outline=None)
    d.rectangle((xt, y - 26, x1, y + 26), fill=FILL3, outline=None)
    ctext(d, (x0 + xc) / 2, y, "層流域", FS, GRAY)
    ctext(d, (xc + xt) / 2, y, "遷移域(乱れ弱い)", FT, GRAY)
    ctext(d, (xt + x1) / 2, y, "発達した乱流域", FS, GRAY)
    # 数直線
    arrow(d, x0 - 5, y + 60, x1 + 20, y + 60, BLACK, 2, 11)
    ctext(d, x1 + 24, y + 60, "Re", FS, BLACK, "lm")
    # 臨界2300の境界
    d.line((xc, y - 40, xc, y + 68), fill=RED, width=3)
    ctext(d, xc, y - 54, "臨界 Re = 2300", FS, RED)
    d.line((xc, y + 60, xc, y + 66), fill=RED, width=3)
    # Re=2400 のマーカー(臨界のすぐ上)
    xm = xc + 28
    d.ellipse((xm - 7, y + 53, xm + 7, y + 67), fill=RED, outline=BLACK)
    arrow(d, xm, y + 96, xm, y + 70, BLACK, 2, 10)
    ctext(d, xm, y + 112, "Re = 2400(臨界のすぐ上)", FT, BLACK)
    save(im, "t2e6_16")


if __name__ == "__main__":
    for fn in [f01, f02, f03, f04, f05, f06, f07, f08,
               f09, f10, f11, f12, f13, f14, f15, f16]:
        fn()
    print("done 16")
