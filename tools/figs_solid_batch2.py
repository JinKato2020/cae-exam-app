# -*- coding: utf-8 -*-
"""Phase2 Batch2: 図なし18問へ後付けする図。
modeling-basics 第8章(model8*) 11問 / solid1 第10章(s1e10*) 7問。
白地660x420・黒線画・機構/概念のみ(答えの番号・最終数値は焼き込まない)。すべて helpful(回答後表示)。
JSON配線は別途。ここでは assets/figures/<key>.png を生成するのみ。"""
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


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3, col=BLACK):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def mlines(d, cx, cy, lines, fnt=FT, fill=BLACK, lh=23):
    n = len(lines)
    y0 = cy - (n - 1) * lh / 2
    for i, s in enumerate(lines):
        ctext(d, cx, y0 + i * lh, s, fnt, fill)


# ============================================================
# modeling-basics 第8章
# ============================================================
def model8Purpose():
    im, d = new(); title(d, "構造解析(シミュレーション)の活用段階")
    stages = ["概念設計", "詳細設計", "製造・運用", "破損原因調査"]
    used = [True, True, False, True]
    x0, w, y = 60, 135, 150
    arrow(d, 40, y + 22, 620, y + 22, GRAY, 2, 12)
    ctext(d, 620, y + 44, "開発の流れ", FT, GRAY, "rm")
    for i, (s, u) in enumerate(zip(stages, used)):
        x = x0 + i * w
        f = FILL1 if u else (250, 250, 250)
        box(d, x, y - 30, x + w - 20, y + 14, f)
        ctext(d, x + (w - 20) / 2, y - 8, s, FS, BLACK)
        if u:
            node(d, x + (w - 20) / 2, y + 22, 6, fill=BLUE, col=BLUE)
            ctext(d, x + (w - 20) / 2, y + 62, "解析を活用", FT, BLUE)
    ctext(d, W / 2, 290, "破損調査 → 詳細設計 → 概念設計 と適用が拡大", FT, GRAY)
    ctext(d, W / 2, 320, "詳細設計で開発コストの約8割が決まるとされる", FT, GRAY)
    note(d, "解析は概念設計・詳細設計・破損原因調査など様々な段階で活用される。")
    save(im, "model8Purpose")


def model8UnitSys():
    im, d = new(); title(d, "FEMの単位系は一貫させる(mm–N系)")
    rows = [["量", "この系での単位"],
            ["長さ", "mm"],
            ["力", "N"],
            ["応力・弾性係数", "N/mm² = MPa"],
            ["変位", "mm"]]
    x0, y0, cw0, cw1, rh = 120, 90, 210, 210, 44
    for i, r in enumerate(rows):
        yy = y0 + i * rh
        f = FILL2 if i == 0 else FILL1
        box(d, x0, yy, x0 + cw0, yy + rh, f)
        box(d, x0 + cw0, yy, x0 + cw0 + cw1, yy + rh, f)
        ctext(d, x0 + cw0 / 2, yy + rh / 2, r[0], FT, BLACK)
        ctext(d, x0 + cw0 + cw1 / 2, yy + rh / 2, r[1], FT, BLACK)
    ctext(d, W / 2, 335, "換算の要:1 GPa = 1000 MPa = 1000 N/mm²", FS, RED)
    note(d, "長さmm・力Nなら応力と弾性係数は N/mm²(=MPa)。全物性を同じ系にそろえる。")
    save(im, "model8UnitSys")


def model8OutputContour():
    im, d = new(); title(d, "応力の出力:節点値と要素値")
    # 左:節点値(なめらか補間)
    lx, ly, s, n = 70, 100, 46, 4
    for i in range(n + 1):
        d.line((lx, ly + i * s, lx + n * s, ly + i * s), fill=GRAY, width=1)
        d.line((lx + i * s, ly, lx + i * s, ly + n * s), fill=GRAY, width=1)
    # なめらかな等高線を数本
    for k in range(1, 4):
        d.arc((lx - 40 + k * 34, ly - 40 + k * 30, lx + n * s + 20 + k * 8, ly + n * s + 10),
              120, 210, fill=BLUE, width=2)
    for i in range(n + 1):
        for j in range(n + 1):
            node(d, lx + j * s, ly + i * s, 3, fill=BLUE, col=BLUE)
    ctext(d, lx + n * s / 2, ly + n * s + 24, "節点値", FS, BLUE)
    ctext(d, lx + n * s / 2, ly + n * s + 48, "なめらかに補間", FT, GRAY)
    # 右:要素値(要素ごと一色・不連続)
    rx = 400
    tones = [(238, 238, 238), (222, 222, 222), (205, 205, 205), (188, 188, 188)]
    for i in range(n):
        for j in range(n):
            t = tones[(i + j) % len(tones)]
            d.rectangle((rx + j * s, ly + i * s, rx + (j + 1) * s, ly + (i + 1) * s),
                        outline=BLACK, width=1, fill=t)
    ctext(d, rx + n * s / 2, ly + n * s + 24, "要素値", FS, BLACK)
    ctext(d, rx + n * s / 2, ly + n * s + 48, "要素ごと一色(不連続)", FT, GRAY)
    note(d, "異材界面では応力が不連続。界面評価は要素値やガウス点値・界面近傍の分布を使う。")
    save(im, "model8OutputContour")


def model8Dmat3D():
    im, d = new(); title(d, "三次元の応力6成分と [D] 行列")
    iso_box(d, 80, 150, 120, 110, 60)
    ctext(d, 155, 300, "応力6成分", FS, BLACK)
    ctext(d, 155, 328, "σx σy σz", FT, BLACK)
    ctext(d, 155, 350, "τxy τyz τzx", FT, BLACK)
    arrow(d, 300, 210, 360, 210, BLACK, 3, 14)
    vals = [["·"] * 6 for _ in range(6)]
    matrix_grid(d, 385, 105, vals, cell=34, fnt=FT)
    d.line((385, 105, 385 + 6 * 34, 105 + 6 * 34), fill=RED, width=2)
    ctext(d, 385 + 3 * 34, 105 + 6 * 34 + 20, "6行6列の対称行列", FT, RED)
    note(d, "二次元は応力3成分(3×3)、三次元は応力6成分だから [D] は6×6の対称行列。")
    save(im, "model8Dmat3D")


def model8DmatPStrain():
    im, d = new(); title(d, "平面ひずみと平面応力の区別")
    box(d, 55, 90, 320, 330, FILL1, col=BLUE)
    box(d, 350, 90, 610, 330, FILL2)
    ctext(d, 187, 118, "平面ひずみ", FS, BLUE)
    mlines(d, 187, 205, ["εz = 0", "σz ≠ 0(従属して生じる)",
                          "係数の分母に", "(1+ν)(1−2ν)", "厚い/長い断面"], FT, BLACK, 30)
    ctext(d, 480, 118, "平面応力", FS, BLACK)
    mlines(d, 480, 205, ["σz = 0", "εz ≠ 0(自由に縮む)",
                          "係数の分母に", "1 − ν²", "薄い板"], FT, BLACK, 30)
    note(d, "平面ひずみは εz=0(σz≠0)。用いる応力ひずみ行列の係数の分母が両者で異なる。")
    save(im, "model8DmatPStrain")


def model8DmatPStress():
    im, d = new(); title(d, "平面応力の [D] 行列とせん断成分")
    ctext(d, 120, 210, "[ ア ]", F, RED)
    ctext(d, 120, 240, "(係数)", FT, GRAY)
    ctext(d, 185, 210, "×", F, BLACK)
    vals = [["1", "ν", "0"], ["ν", "1", "0"], ["0", "0", "(1−ν)/2"]]
    matrix_grid(d, 220, 150, vals, cell=64, fnt=FT)
    d.rectangle((220 + 2 * 64, 150 + 2 * 64, 220 + 3 * 64, 150 + 3 * 64), outline=RED, width=3)
    ctext(d, W / 2, 340, "せん断成分 [ア]·(1−ν)/2 = G = E / {2(1+ν)} から [ア] を決める", FT, RED)
    note(d, "対角の1・非対角のν・せん断(1−ν)/2 をもつ形。せん断成分と G の一致から係数が定まる。")
    save(im, "model8DmatPStress")


def model8TrussK():
    im, d = new(); title(d, "2節点トラス要素の局所剛性(軸のみ)")
    y = 190
    x1, x2 = 160, 470
    # 軸ばね
    from figlib import spring
    spring(d, x1, y, x2, y, coils=7, amp=16)
    node(d, x1, y, 8); node(d, x2, y, 8)
    ctext(d, x1, y - 34, "節点1", FT, BLACK)
    ctext(d, x2, y - 34, "節点2", FT, BLACK)
    ctext(d, (x1 + x2) / 2, y + 34, "軸剛性 EA/L", FS, BLUE)
    # 局所座標
    arrow(d, 120, 300, 220, 300, BLACK, 2, 11); ctext(d, 228, 300, "x(局所・軸)", FT, BLACK, "lm")
    arrow(d, 120, 300, 120, 240, BLACK, 2, 11); ctext(d, 120, 228, "y", FT, BLACK)
    # 軸方向力
    force(d, x2 + 6, y, 46, 0, "", RED)
    force(d, x1 - 6, y, -46, 0, "", RED)
    ctext(d, W / 2, 340, "軸(x)方向のみ ±EA/L、y方向の剛性は 0(せん断を伝えない)", FT, RED)
    note(d, "トラスは軸力のみを伝え、軸に直交する方向には剛性をもたない。局所系では1次元ばね。")
    save(im, "model8TrussK")


def model8EulerBeam():
    im, d = new(); title(d, "ベルヌーイ・オイラーはりの変位仮定")
    # 中立軸(変形前=破線、変形後=曲線)
    dashed(d, 80, 175, 590, 175, GRAY, 2)
    ctext(d, 596, 175, "変形前中立軸", FT, GRAY, "lm") if False else None
    pts = [(80, 175)]
    for i in range(1, 52):
        x = 80 + i * 10
        t = i / 51.0
        y = 175 + 70 * (t * t)
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, 150, 150, "中立軸 たわみ w(x)", FT, BLUE)
    # 着目断面 x0
    x0 = 330
    t0 = (x0 - 80) / 510.0
    y0 = 175 + 70 * (t0 * t0)
    slope = 70 * 2 * t0 / 510.0  # dw/dx
    ang = math.atan(slope)
    # 変形前の断面(鉛直・破線)
    dashed(d, x0, y0 - 70, x0, y0 + 70, GRAY, 2)
    # 変形後の断面(傾く・実線)。平面を保ち中立面に垂直→傾き角=たわみ角
    L = 70
    dx = L * math.sin(ang); dy = L * math.cos(ang)
    d.line((x0 - dx, y0 - dy, x0 + dx, y0 + dy), fill=BLACK, width=3)
    node(d, x0, y0, 4, fill=BLACK, col=BLACK)
    # 点P(z上方)と軸方向変位u
    px, py = x0 - dx * 0.7, y0 - dy * 0.7
    node(d, px, py, 4, fill=RED, col=RED)
    dashed(d, x0, py, px, py, GRAY, 1)
    arrow(d, x0, py + 0, px, py, RED, 2, 10)
    ctext(d, x0 + 10, y0 - 44, "z", FT, BLACK, "lm")
    ctext(d, 175, 108, "軸方向変位 u = −z · dw/dx", FT, RED, "lm")
    arrow(d, 300, 112, px - 4, py - 8, RED, 1, 8)
    angle_arc(d, x0, y0, 40, 90 - math.degrees(ang), 90, "θ", GRAY)
    ctext(d, W / 2, 348, "断面は平面を保ち中立面に垂直 → 軸方向変位 u は距離 z に比例", FT, GRAY)
    note(d, "たわみ角 θ=dw/dx だけ断面が傾き、u=−z·dw/dx(z の一次関数)となる。")
    save(im, "model8EulerBeam")


def model8Idealize3():
    im, d = new(); title(d, "二次元理想化:平面応力・平面ひずみ・軸対称")
    cols = [
        (155, "平面応力", ["薄い板", "σz = 0", "εz ≠ 0", "応力3成分"]),
        (330, "平面ひずみ", ["長い/厚い", "εz = 0", "σz ≠ 0", "応力3成分"]),
        (505, "軸対称", ["回転体", "面内3成分＋", "周方向1成分", "＝4成分"]),
    ]
    for cx, ttl, lines in cols:
        box(d, cx - 82, 78, cx + 82, 118, FILL2)
        ctext(d, cx, 98, ttl, FS, BLUE)
        # アイコン
        if ttl == "平面応力":
            d.rectangle((cx - 55, 140, cx + 55, 165), outline=BLACK, width=3, fill=FILL1)
        elif ttl == "平面ひずみ":
            d.rectangle((cx - 55, 135, cx + 55, 185), outline=BLACK, width=3, fill=FILL1)
        else:
            dashed(d, cx, 130, cx, 195, GRAY, 2)
            d.rectangle((cx + 8, 135, cx + 48, 190), outline=BLACK, width=3, fill=FILL1)
        mlines(d, cx, 255, lines, FT, BLACK, 26)
    note(d, "平面応力=σz0/εz残る、平面ひずみ=εz0/σz残る、軸対称=面内3＋周方向1の4成分。")
    save(im, "model8Idealize3")


def model8ThickStrain():
    im, d = new(); title(d, "厚さ方向に拘束された厚肉体(平面ひずみ)")
    # 厚肉ブロック(アイソメ)
    iso_box(d, 210, 150, 180, 120, 90)
    # z軸(厚さ方向=奥行き)
    arrow(d, 250, 320, 300, 275, BLACK, 2, 11); ctext(d, 262, 300, "z(厚さ)", FT, BLACK, "rm")
    ctext(d, W / 2, 320, "厚さ方向に変形しにくい → εz = 0", FS, RED)
    ctext(d, W / 2, 348, "面内応力 σx, σy から σz ≠ 0 が従属的に生じる", FT, GRAY)
    # 面内応力矢印
    force(d, 210, 215, -46, 0, "σx", RED); force(d, 390, 215, 46, 0, "", RED)
    note(d, "εz=0 を課すのが平面ひずみ。σz は0ではなく面内応力から決まる(平面応力との違い)。")
    save(im, "model8ThickStrain")


def model8Revolve():
    im, d = new(); title(d, "軸対称:三次元回転体を二次元(r–z)で解く")
    # 回転軸
    dashed(d, 150, 80, 150, 340, GRAY, 2)
    ctext(d, 150, 66, "回転軸 z", FT, GRAY)
    # r-z 断面(L形の半断面)
    d.polygon([(160, 110), (230, 110), (230, 320), (160, 320)], outline=BLACK, width=3, fill=FILL1)
    ctext(d, 195, 215, "r–z", FT, BLACK)
    ctext(d, 195, 240, "断面", FT, BLACK)
    arrow(d, 150, 335, 240, 335, BLACK, 2, 10); ctext(d, 248, 335, "r", FT, BLACK, "lm")
    # 回転矢印
    d.arc((300, 150, 460, 300), -60, 120, fill=BLUE, width=3)
    arrow(d, 455, 165, 470, 200, BLUE, 3, 12)
    ctext(d, 380, 130, "回転", FS, BLUE)
    # 3D 円筒
    d.ellipse((470, 110, 590, 150), outline=BLACK, width=3, fill=FILL2)
    d.line((470, 130, 470, 300), fill=BLACK, width=3)
    d.line((590, 130, 590, 300), fill=BLACK, width=3)
    d.arc((470, 280, 590, 320), 0, 180, fill=BLACK, width=3)
    ctext(d, 530, 335, "三次元回転体", FT, GRAY)
    note(d, "回転対称な形状・荷重なら、3次元問題を2次元(r–z)断面でモデル化・解析できる。")
    save(im, "model8Revolve")


# ============================================================
# solid1 第10章(ISO9001・検証と品質)
# ============================================================
def s1e10Quality3():
    im, d = new(); title(d, "工学シミュレーションの品質を支える3要素")
    # 上の梁
    box(d, 120, 78, 540, 118, FILL2)
    ctext(d, 330, 98, "シミュレーションの品質(ISO9001)", FS, BLUE)
    cols = [(200, ["①解析ソフト", "ウェアの検証"]),
            (330, ["②適切な", "解析プロセス"]),
            (460, ["③十分な力量を", "有する解析要員"])]
    for cx, lines in cols:
        box(d, cx - 78, 150, cx + 78, 300, FILL1)
        mlines(d, cx, 225, lines, FT, BLACK, 26)
    ctext(d, W / 2, 330, "機能の豊富さや計算機の速さは品質の本質ではない", FT, RED)
    note(d, "品質は『ソフトウェアの検証』『適切なプロセス』『要員の力量』の3本柱で支える。")
    save(im, "s1e10Quality3")


def s1e10Competence():
    im, d = new(); title(d, "解析要員の力量(competence)")
    box(d, 70, 150, 220, 250, FILL1)
    mlines(d, 145, 200, ["知識", "＋", "技能"], FS, BLACK, 30)
    arrow(d, 227, 200, 300, 200, BLACK, 3, 14)
    ctext(d, 263, 180, "適用", FT, BLUE)
    box(d, 305, 150, 590, 250, FILL2, col=BLUE)
    mlines(d, 447, 200, ["実際の問題に適用", "できる能力", "＝ 力量"], FS, BLACK, 30)
    ctext(d, W / 2, 300, "知識・技能を『持っている』だけでは力量ではない", FT, RED)
    ctext(d, W / 2, 328, "経験年数の長さそのものも力量ではない", FT, GRAY)
    note(d, "力量=知識及び技能を、意図した結果のため実際の問題に適用できる能力。")
    save(im, "s1e10Competence")


def s1e10PlanDocs():
    im, d = new(); title(d, "実行計画書と解析計画書の役割")
    box(d, 55, 95, 320, 320, FILL1)
    box(d, 350, 95, 610, 320, FILL2)
    ctext(d, 187, 122, "実行計画書", FS, BLUE)
    ctext(d, 187, 150, "(管理面)", FT, GRAY)
    mlines(d, 187, 225, ["・工程計画", "・要員計画", "・プロジェクト管理"], FT, BLACK, 30)
    ctext(d, 480, 122, "解析計画書", FS, BLUE)
    ctext(d, 480, 150, "(技術面)", FT, GRAY)
    mlines(d, 480, 235, ["・解析条件・対象", "・モデル化", "・解析方法/手順", "＋検証・妥当性確認の方法"], FT, BLACK, 28)
    ctext(d, W / 2, 348, "計画書のレビューは第三者が行う", FT, RED)
    note(d, "実行計画書=管理面、解析計画書=技術面＋V&Vの実施方法。役割が異なる。")
    save(im, "s1e10PlanDocs")


def s1e10ValidMethods():
    im, d = new(); title(d, "妥当性確認:独立した手法との比較")
    box(d, 250, 90, 410, 145, FILL2, col=BLUE)
    ctext(d, 330, 117, "解析結果", FS, BLUE)
    items = [(150, ["手計算・", "工学式/理論解"]),
             (330, ["妥当性確認済みの", "類似解析"]),
             (510, ["実験・実機の", "計測結果"])]
    for cx, lines in items:
        box(d, cx - 90, 240, cx + 90, 320, FILL1)
        mlines(d, cx, 280, lines, FT, BLACK, 26)
        arrow(d, 330, 148, cx, 236, GRAY, 2, 11)
    ctext(d, W / 2, 190, "＝ 独立した外部の基準と比較する", FS, RED)
    note(d, "妥当性確認は、手計算・理論解・類似解析・実験など独立した手法の結果と比較して行う。")
    save(im, "s1e10ValidMethods")


def s1e10Trace():
    im, d = new(); title(d, "シミュレーションのトレーサビリティ")
    chain = ["対象物", "解析目的", "モデル化", "解析データ", "手法/手順", "結果"]
    x0, w, y = 40, 102, 150
    for i, s in enumerate(chain):
        x = x0 + i * w
        box(d, x, y, x + w - 16, y + 50, FILL1)
        ctext(d, x + (w - 16) / 2, y + 25, s, FT, BLACK)
        if i < len(chain) - 1:
            arrow(d, x + w - 16, y + 25, x + w, y + 25, BLACK, 2, 9)
    ctext(d, W / 2, 245, "↑ 結果に到る履歴を後から追える状態", FT, GRAY)
    box(d, 160, 275, 500, 320, FILL2, col=BLUE)
    ctext(d, 330, 297, "実現の要:適切な記録の作成・保持", FS, BLUE)
    note(d, "トレーサビリティ=履歴を追える状態。その実現には記録の作成・保持が重要。")
    save(im, "s1e10Trace")


def s1e10Outsource():
    im, d = new(); title(d, "解析のアウトソーシングと品質責任")
    box(d, 250, 78, 410, 128, FILL2)
    ctext(d, 330, 103, "顧客", FS, BLACK)
    box(d, 70, 195, 285, 305, FILL1, col=BLUE)
    mlines(d, 177, 240, ["発注者(受託組織)", "納品物件の", "品質責任は残る"], FT, BLACK, 28)
    box(d, 400, 195, 600, 305, FILL1)
    mlines(d, 500, 247, ["委託先", "(外部業者)"], FT, BLACK, 28)
    arrow(d, 320, 132, 240, 192, GRAY, 2, 11)
    ctext(d, 232, 160, "受託", FT, GRAY, "rm")
    arrow(d, 290, 250, 396, 250, BLACK, 3, 13)
    ctext(d, 343, 226, "社内に準じる", FT, BLUE)
    ctext(d, 343, 274, "品質活動を要求", FT, BLUE)
    note(d, "外部委託しても納品物件の品質責任は発注者に残り、委託先にも品質活動を求めうる。")
    save(im, "s1e10Outsource")


def s1e10Contract():
    im, d = new(); title(d, "契約内容の確認で重要な項目")
    items = ["納期", "契約金額", "業務範囲(業務所掌)", "瑕疵担保条項"]
    x0, y0, w, h = 110, 100, 210, 70
    for i, s in enumerate(items):
        r, c = divmod(i, 2)
        x = x0 + c * (w + 30); y = y0 + r * (h + 30)
        box(d, x, y, x + w, y + h, FILL1)
        ctext(d, x + w / 2, y + h / 2, s, FS, BLACK)
    ctext(d, W / 2, 330, "契約内容は『契約書』の表題に限らない(発注書・仕様書の一部でも成立)", FT, RED)
    note(d, "プロジェクトリーダが確認する重要項目=納期・契約金額・業務範囲・瑕疵担保条項。")
    save(im, "s1e10Contract")


ALL = [model8Purpose, model8UnitSys, model8OutputContour, model8Dmat3D, model8DmatPStrain,
       model8DmatPStress, model8TrussK, model8EulerBeam, model8Idealize3, model8ThickStrain,
       model8Revolve, s1e10Quality3, s1e10Competence, s1e10PlanDocs, s1e10ValidMethods,
       s1e10Trace, s1e10Outsource, s1e10Contract]

KEYS = ["model8Purpose", "model8UnitSys", "model8OutputContour", "model8Dmat3D",
        "model8DmatPStrain", "model8DmatPStress", "model8TrussK", "model8EulerBeam",
        "model8Idealize3", "model8ThickStrain", "model8Revolve", "s1e10Quality3",
        "s1e10Competence", "s1e10PlanDocs", "s1e10ValidMethods", "s1e10Trace",
        "s1e10Outsource", "s1e10Contract"]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    miss = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(KEYS), "MISSING", miss)
