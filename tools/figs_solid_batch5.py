# -*- coding: utf-8 -*-
"""Phase2 Batch5: 図なし25問へ後付けする図。
prepost-basics 第10章 プリポスト処理の基礎
(pp-10-1..6,12,16,17,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36)。
接頭辞 pp10*(既存pp10キーと衝突しない新規名)。白地660x420・黒線画・機構/概念のみ
(答え番号・最終数値は焼き込まない)。すべて helpful(回答後表示)。JSON配線は別途。"""
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


def mlines(d, cx, cy, lines, fnt=FT, fill=BLACK, lh=21):
    n = len(lines)
    y0 = cy - (n - 1) * lh / 2
    for i, s in enumerate(lines):
        ctext(d, cx, y0 + i * lh, s, fnt, fill)


def pbox(d, x0, y0, x1, y1, lines, fill=FILL1, col=BLACK, fnt=FT, lh=20):
    box(d, x0, y0, x1, y1, fill, 3, col)
    mlines(d, (x0 + x1) / 2, (y0 + y1) / 2, lines, fnt, BLACK, lh)


def vflow(d, steps, x0=165, x1=495, y0=60, bh=40, gap=18, fills=None):
    y = y0
    for i, lines in enumerate(steps):
        f = fills[i] if fills else FILL1
        pbox(d, x0, y, x1, y + bh, lines, f)
        if i < len(steps) - 1:
            arrow(d, (x0 + x1) / 2, y + bh, (x0 + x1) / 2, y + bh + gap, BLACK, 3, 11)
        y += bh + gap
    return y


def hflow(d, steps, y0=150, bh=96, fills=None):
    n = len(steps)
    x = 40
    bw = (580 - (n - 1) * 30) / n
    for i, lines in enumerate(steps):
        f = fills[i] if fills else FILL1
        pbox(d, x, y0, x + bw, y0 + bh, lines, f, lh=22)
        if i < n - 1:
            arrow(d, x + bw + 2, y0 + bh / 2, x + bw + 28, y0 + bh / 2, BLACK, 3, 12)
        x += bw + 30


# ============================================================
# pp-10-1 起動から終了までの入れ子構造
# ============================================================
def pp10OpStack():
    im, d = new(); title(d, "起動から終了までの入れ子構造")
    box(d, 70, 66, 590, 356, "white", 3, BLACK)
    ctext(d, 330, 84, "計算機:起動・ログイン  …  終了", FT, BLACK)
    box(d, 140, 106, 520, 322, FILL1, 3, BLUE)
    ctext(d, 330, 124, "CAEアプリ:起動  …  ログアウト/終了", FT, BLUE)
    box(d, 220, 150, 440, 288, FILL2, 3, RED)
    mlines(d, 330, 219, ["解析実行", "(中核作業)"], FS, RED, 26)
    arrow(d, 40, 96, 40, 300, GREEN, 3, 12); ctext(d, 34, 200, "開く 外→内", FT, GREEN, "rm")
    arrow(d, 620, 300, 620, 96, ORANGE, 3, 12); ctext(d, 626, 200, "閉じる 内→外", FT, ORANGE, "lm")
    note(d, "土台(計算機)を先に開き内側(アプリ→解析)へ。閉じるときは内側から外側へ戻る。")
    save(im, "pp10OpStack")


# ============================================================
# pp-10-2 有限要素構造解析の3工程
# ============================================================
def pp10ThreeStages():
    im, d = new(); title(d, "有限要素構造解析の3工程")
    hflow(d, [["プリ処理", "", "モデル・メッシュ", "材料・境界条件", "を作る"],
              ["ソルバ", "", "剛性方程式を", "組み立て", "連立方程式を解く"],
              ["ポスト処理", "", "変形図・応力を", "表示して", "評価する"]],
          y0=140, bh=110, fills=[FILL1, FILL2, FILL1])
    ctext(d, 330, 100, "入力を作る → 計算する → 結果を見る", FT, GRAY)
    note(d, "前工程の出力が次工程の入力になる。1つのアプリに統合されても内部の実行順は同じ。")
    save(im, "pp10ThreeStages")


# ============================================================
# pp-10-3 プリ処理で用意する入力データ
# ============================================================
def pp10PreInputs():
    im, d = new(); title(d, "プリ処理で用意する入力データ")
    box(d, 40, 70, 300, 330, FILL1, 3, BLUE)
    ctext(d, 170, 90, "プリ処理", FS, BLUE)
    items = ["形状モデル", "メッシュ(要素分割)", "材料物性値", "境界条件(荷重・拘束)"]
    yy = 130
    for s in items:
        box(d, 62, yy, 278, yy + 40, "white", 2, GRAY)
        ctext(d, 170, yy + 20, s, FT, BLACK)
        yy += 50
    arrow(d, 302, 200, 358, 200, BLACK, 4, 14); ctext(d, 330, 182, "入力", FT, GRAY)
    box(d, 360, 150, 620, 250, FILL2, 3, BLACK)
    mlines(d, 490, 200, ["ソルバ", "連立方程式を解く"], FT, BLACK, 24)
    box(d, 360, 265, 620, 330, "white", 2, GRAY)
    mlines(d, 490, 297, ["ポスト処理", "結果を表示・評価(工程外の決裁は別)"], FT, GRAY, 22)
    note(d, "形状・メッシュ・物性・境界条件の入力一式を作るのがプリ処理。設定ミスはここで混入。")
    save(im, "pp10PreInputs")


# ============================================================
# pp-10-4 強度評価のFEM作業の流れ
# ============================================================
def pp10FemWorkflow():
    im, d = new(); title(d, "強度評価のFEM作業の流れ")
    hflow(d, [["モデル形状", "入力"], ["要素分割", "(メッシュ)"],
              ["シミュ", "レーション"], ["結果評価"]],
          y0=140, bh=80, fills=[FILL1, FILL1, FILL2, FILL1])
    # フィードバックループ(評価→形状へ戻る)
    dashed(d, 570, 130, 570, 96, RED, 2)
    dashed(d, 570, 96, 100, 96, RED, 2)
    arrow(d, 100, 96, 100, 138, RED, 2, 10)
    ctext(d, 330, 86, "問題があれば形状・メッシュへ戻り反復", FT, RED)
    note(d, "形状→分割→計算→評価の順。前段の成果が次段の入力。1周の順序は固定。")
    save(im, "pp10FemWorkflow")


# ============================================================
# pp-10-5 応力勾配に応じた要素分割
# ============================================================
def pp10GradientRefine():
    im, d = new(); title(d, "応力勾配に応じた要素分割")
    # フィレット付き部材(左に応力集中)
    x0, y0 = 60, 90
    d.polygon([(x0, y0), (x0 + 120, y0), (x0 + 120, y0 + 60)], outline=None, fill="white")
    box(d, x0, y0, x0 + 300, y0 + 60, FILL1)         # 上の細い部分
    box(d, x0, y0 + 60, x0 + 300, y0 + 150, FILL1)   # 下の太い部分
    # フィレット(段の隅)
    d.arc((x0 + 300 - 40, y0 + 60, x0 + 300 + 40, y0 + 140), 180, 270, fill=BLACK, width=3)
    ctext(d, x0 + 300, y0 + 40, "応力集中(隅)", FT, RED)
    # 細かいメッシュ(隅付近)
    for xx in range(x0 + 250, x0 + 305, 12):
        dashed(d, xx, y0 + 60, xx, y0 + 150, LGRAY, 1)
    for yy in range(y0 + 62, y0 + 150, 12):
        dashed(d, x0 + 250, yy, x0 + 300, yy, LGRAY, 1)
    # 粗いメッシュ(遠方)
    for xx in range(x0, x0 + 130, 40):
        dashed(d, xx, y0 + 60, xx, y0 + 150, LGRAY, 1)
    ctext(d, x0 + 40, y0 + 110, "粗", FS, GRAY); ctext(d, x0 + 275, y0 + 105, "細", FS, RED)
    # 応力分布グラフ
    axes(d, 90, 370, 470, 90, "位置", "応力")
    pts = []
    for i in range(0, 471, 8):
        t = i / 470.0
        val = 20 + 150 * math.exp(-((t - 0.62) ** 2) / 0.01)
        pts.append((90 + i, 370 - val))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, 90 + 300, 300, "勾配が急な所=細かく", FT, RED)
    note(d, "応力変化が急な部位ほど要素を小さく、ゆるやかな遠方は粗く。限られた資源を厚く配る。")
    save(im, "pp10GradientRefine")


# ============================================================
# pp-10-6 細→粗をなだらかにつなぐ粗密
# ============================================================
def pp10CoarseFineTransition():
    im, d = new(); title(d, "細→粗をなだらかにつなぐ粗密(穴あき板)")
    # 板
    box(d, 60, 80, 600, 300, "white", 3, BLACK)
    cx, cy, r = 180, 190, 46
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill="white")
    ctext(d, cx, cy, "穴", FT, GRAY)
    # 引張
    for yy in (120, 190, 260):
        arrow(d, 30, yy, 60, yy, RED, 3, 11)
        arrow(d, 600, yy, 630, yy, RED, 3, 11)
    # 集中部=細
    for rr in range(r + 8, r + 40, 10):
        d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 0, 360, fill=LGRAY, width=1)
    ctext(d, cx, cy + 62, "細(集中部)", FT, RED)
    # 遷移域
    for xx in range(260, 340, 22):
        dashed(d, xx, 84, xx, 296, LGRAY, 1)
    ctext(d, 300, 320, "遷移域(徐々に)", FT, ORANGE)
    # 遠方=粗
    for xx in range(360, 601, 55):
        dashed(d, xx, 84, xx, 296, LGRAY, 1)
    ctext(d, 490, 320, "粗(遠方)", FT, GRAY)
    note(d, "集中部は細かく、遠方は粗く、境目は遷移域でなだらかに。急変は扁平要素を招く。")
    save(im, "pp10CoarseFineTransition")


# ============================================================
# pp-10-12 3次元要素の節点数の違い
# ============================================================
def pp10Elem3DNodes():
    im, d = new(); title(d, "3次元要素の節点数の違い")

    def cube(ox, oy, w, mids=False):
        dx, dy = 34, 22
        pts_f = [(ox, oy), (ox + w, oy), (ox + w, oy + w), (ox, oy + w)]
        d.polygon(pts_f, outline=BLACK, width=2)
        d.polygon([(ox + dx, oy - dy), (ox + w + dx, oy - dy),
                   (ox + w + dx, oy + w - dy), (ox + dx, oy + w - dy)], outline=BLACK, width=2)
        for (a, b) in zip(pts_f, [(ox + dx, oy - dy), (ox + w + dx, oy - dy),
                                  (ox + w + dx, oy + w - dy), (ox + dx, oy + w - dy)]):
            d.line((a[0], a[1], b[0], b[1]), fill=BLACK, width=2)
        corners = pts_f + [(ox + dx, oy - dy), (ox + w + dx, oy - dy),
                           (ox + w + dx, oy + w - dy), (ox + dx, oy + w - dy)]
        for (px, py) in corners:
            node(d, px, py, 4, fill=RED, col=RED)
        if mids:
            edges = [((ox, oy), (ox + w, oy)), ((ox + w, oy), (ox + w, oy + w)),
                     ((ox + w, oy + w), (ox, oy + w)), ((ox, oy + w), (ox, oy))]
            for a, b in edges:
                node(d, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 3, fill=BLUE, col=BLUE)

    # 四面体一次(4節点)
    box(d, 40, 70, 240, 300, "white", 2, GRAY)
    tp = [(140, 90), (70, 250), (210, 245), (150, 210)]
    d.line([tp[0], tp[1], tp[2], tp[0]], fill=BLACK, width=2)
    d.line([tp[0], tp[3]], fill=BLACK, width=2)
    d.line([tp[1], tp[3]], fill=BLACK, width=2)
    d.line([tp[2], tp[3]], fill=BLACK, width=2)
    for p in tp:
        node(d, p[0], p[1], 4, fill=RED, col=RED)
    ctext(d, 140, 285, "四面体 一次 = 4節点", FT, BLACK)
    # 立方体一次(8節点)
    box(d, 250, 70, 450, 300, "white", 2, GRAY)
    cube(300, 150, 90, mids=False)
    ctext(d, 350, 285, "立方体 一次 = 8節点", FT, BLACK)
    # 六面体二次(20節点)
    box(d, 460, 70, 620, 300, "white", 2, GRAY)
    cube(500, 150, 80, mids=True)
    ctext(d, 540, 285, "六面体 二次 = 20節点", FT, RED)
    box(d, 60, 320, 600, 360, FILL2)
    ctext(d, 330, 340, "二次要素は辺に中間節点(青)をもち節点がはるかに多い", FT, BLACK)
    note(d, "六面体二次は20節点。要素数に対し節点数は多く、四面体一次と同数にはならない。")
    save(im, "pp10Elem3DNodes")


# ============================================================
# pp-10-16 メッシュ品質の点検項目
# ============================================================
def pp10QualityChecks():
    im, d = new(); title(d, "メッシュ品質の点検項目")
    rows = [("ヤコビ行列式が負・零でないか", "点検する", GREEN),
            ("スキュー(角度の歪み)が大きくないか", "点検する", GREEN),
            ("アスペクト比(縦横比)が大きくないか", "点検する", GREEN),
            ("数値積分点の数(積分次数)", "ソルバが自動決定", RED)]
    y = 90
    for name, verdict, col in rows:
        box(d, 55, y, 400, y + 56, FILL1)
        ctext(d, 227, y + 28, name, FT, BLACK)
        box(d, 400, y, 605, y + 56, "white", 2, col)
        mark = "O" if col == GREEN else "-"
        ctext(d, 420, y + 28, mark, FS, col, "lm")
        ctext(d, 505, y + 28, verdict, FT, col)
        y += 64
    note(d, "形状の歪み(ヤコビ・スキュー・アスペクト比)は点検対象。積分点数は自動決定で点検不要。")
    save(im, "pp10QualityChecks")


# ============================================================
# pp-10-17 要素サイズの急変で生じる扁平要素
# ============================================================
def pp10AbruptSizeJump():
    im, d = new(); title(d, "要素サイズの急変と扁平要素")
    # 左:急変(悪い)
    box(d, 45, 70, 320, 300, "white", 2, GRAY)
    ctext(d, 182, 90, "急変(遷移域なし)", FS, RED)
    for xx in range(60, 160, 20):
        for yy in range(120, 280, 20):
            box(d, xx, yy, xx + 20, yy + 20, "white", 1, LGRAY)
    box(d, 200, 120, 300, 280, "white", 2, LGRAY)
    # 境目の扁平要素
    d.polygon([(160, 120), (200, 120), (200, 200), (160, 160)], outline=RED, width=2)
    d.polygon([(160, 160), (200, 200), (200, 280), (160, 280)], outline=RED, width=2)
    ctext(d, 182, 315, "細長い扁平・歪み要素", FT, RED)
    # 右:遷移(良い)
    box(d, 340, 70, 615, 300, "white", 2, GRAY)
    ctext(d, 477, 90, "遷移域あり(なだらか)", FS, GREEN)
    for xx in range(355, 425, 14):
        for yy in range(120, 280, 14):
            box(d, xx, yy, xx + 14, yy + 14, "white", 1, LGRAY)
    for xx in range(430, 480, 22):
        for yy in range(120, 280, 22):
            box(d, xx, yy, xx + 22, yy + 22, "white", 1, LGRAY)
    box(d, 490, 120, 600, 280, "white", 1, LGRAY)
    ctext(d, 477, 315, "健全な要素", FT, GREEN)
    note(d, "サイズを急に変えると境目で扁平・歪み要素が生じ精度が落ちる。遷移域でなだらかに。")
    save(im, "pp10AbruptSizeJump")


# ============================================================
# pp-10-20 デローニー法:外接円に他節点を含めない
# ============================================================
def pp10Delaunay():
    im, d = new(); title(d, "デローニー法:外接円に他節点を含めない")
    # 節点
    P = {"A": (150, 300), "B": (330, 130), "C": (500, 300), "D": (110, 130)}
    tri = [P["A"], P["B"], P["C"]]
    d.line([tri[0], tri[1], tri[2], tri[0]], fill=BLACK, width=3)
    # 外接円
    (x1, y1), (x2, y2), (x3, y3) = tri
    ax = x2 - x1; ay = y2 - y1; bx = x3 - x1; by = y3 - y1
    dd = 2 * (ax * by - ay * bx)
    ux = (by * (ax * ax + ay * ay) - ay * (bx * bx + by * by)) / dd
    uy = (ax * (bx * bx + by * by) - bx * (ax * ax + ay * ay)) / dd
    cx, cy = x1 + ux, y1 + uy
    r = math.hypot(cx - x1, cy - y1)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLUE, width=2)
    node(d, cx, cy, 3, fill=BLUE, col=BLUE)
    for k, p in P.items():
        col = GREEN if k == "D" else RED
        node(d, p[0], p[1], 6, fill=col, col=col)
        ctext(d, p[0], p[1] - 18, k, FT, col)
    ctext(d, 470, 150, "外接円(青)", FT, BLUE)
    ctext(d, 110, 158, "他節点Dは円の外", FT, GREEN)
    ctext(d, 330, 355, "円の内側に他の節点が入らない三角形分割 → 最小内角を大きく保つ", FT, BLACK)
    note(d, "細長い要素を避け、点・線・面のサイズ指定で所望の粗密の三角形/四面体を自動生成。")
    save(im, "pp10Delaunay")


# ============================================================
# pp-10-21 異機種CAD間の中間ファイル(IGES)
# ============================================================
def pp10IgesExchange():
    im, d = new(); title(d, "異機種CAD間の中間ファイル(IGES)")
    box(d, 40, 150, 200, 260, FILL1); mlines(d, 120, 205, ["CAD A", "(社内)"], FS, BLACK, 26)
    box(d, 250, 140, 410, 270, "white", 3, BLUE)
    mlines(d, 330, 205, ["IGES", "中間ファイル", "ANSI制定"], FT, BLUE, 26)
    box(d, 460, 150, 620, 260, FILL1); mlines(d, 540, 205, ["CAD B", "(他社)"], FS, BLACK, 26)
    arrow(d, 202, 205, 248, 205, BLACK, 4, 14); ctext(d, 225, 187, "出力", FT, GRAY)
    arrow(d, 412, 205, 458, 205, BLACK, 4, 14); ctext(d, 435, 187, "入力", FT, GRAY)
    ctext(d, 330, 300, "機種の違うCAD間を橋渡しする汎用の形状交換形式", FT, BLACK)
    note(d, "IGESはANSI制定の中間ファイル形式。DXFはAutoCAD互換用、GIFは画像で用途が別。")
    save(im, "pp10IgesExchange")


# ============================================================
# pp-10-22 区切りテキスト(CSV)を列で読み込む
# ============================================================
def pp10CsvColumns():
    im, d = new(); title(d, "区切りテキスト(CSV)を列で読み込む")
    box(d, 40, 90, 300, 320, "white", 2, GRAY)
    ctext(d, 170, 108, "CSV(カンマ区切り)", FT, BLACK)
    lines = ["node, sx, sy", "1, 120.5, 30.2", "2, 98.1, 45.7", "3, 60.4, 52.9"]
    yy = 150
    for s in lines:
        ctext(d, 60, yy, s, FT, BLUE, "lm"); yy += 34
    arrow(d, 302, 205, 360, 205, BLACK, 4, 14); ctext(d, 331, 187, "取込", FT, GRAY)
    # 表計算グリッド
    gx, gy, cw, ch = 370, 130, 78, 40
    cols = ["node", "sx", "sy"]
    cells = [["1", "120.5", "30.2"], ["2", "98.1", "45.7"], ["3", "60.4", "52.9"]]
    for j, c in enumerate(cols):
        box(d, gx + j * cw, gy, gx + (j + 1) * cw, gy + ch, FILL2)
        ctext(d, gx + j * cw + cw / 2, gy + ch / 2, c, FT, BLACK)
    for r, row in enumerate(cells):
        for j, v in enumerate(row):
            box(d, gx + j * cw, gy + (r + 1) * ch, gx + (j + 1) * cw, gy + (r + 2) * ch, "white", 1, GRAY)
            ctext(d, gx + j * cw + cw / 2, gy + (r + 1) * ch + ch / 2, v, FT, BLACK)
    ctext(d, gx + cw * 1.5, gy + ch * 5 + 6, "列ごとに整理", FT, GREEN)
    note(d, "CSVは区切りテキストで表計算が列として直接読める。IGES/DXFは形状交換用で不向き。")
    save(im, "pp10CsvColumns")


# ============================================================
# pp-10-23 IGES交換:実装差で面が欠ける
# ============================================================
def pp10IgesFail():
    im, d = new(); title(d, "IGES交換:実装差で面が欠ける")
    # 元の健全ソリッド
    box(d, 55, 95, 235, 300, "white", 2, GRAY); ctext(d, 145, 112, "元のソリッド(CAD A)", FT, BLACK)
    iso_box(d, 95, 200, 100, 70, 55)
    ctext(d, 145, 315, "健全", FT, GREEN)
    arrow(d, 250, 200, 320, 200, BLACK, 4, 14)
    ctext(d, 285, 178, "IGES", FT, BLUE); ctext(d, 285, 222, "変換", FT, GRAY)
    # 読み込み後(面欠落)
    box(d, 340, 95, 620, 300, "white", 2, GRAY); ctext(d, 480, 112, "読込後(CAD B)", FT, BLACK)
    ox, oy, w, h, dp = 420, 200, 100, 70, 55
    dx, dy = int(dp * 0.8), int(dp * 0.5)
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + w + dx, oy - dy), (ox + w, oy)], outline=BLACK, width=3, fill=FILL2)
    d.polygon([(ox + w, oy), (ox + w + dx, oy - dy), (ox + w + dx, oy + h - dy), (ox + w, oy + h)], outline=BLACK, width=3, fill=FILL3)
    # 前面が欠落(赤破線の穴)
    dashed(d, ox, oy, ox + w, oy, RED, 2)
    dashed(d, ox + w, oy, ox + w, oy + h, RED, 2)
    dashed(d, ox + w, oy + h, ox, oy + h, RED, 2)
    dashed(d, ox, oy + h, ox, oy, RED, 2)
    ctext(d, ox + w / 2, oy + h / 2, "面欠落", FT, RED)
    ctext(d, 480, 315, "ヒーリングが必要", FT, RED)
    note(d, "IGESは汎用交換形式だがCADごとの実装差で面が欠けるなど読込失敗が起きやすい。")
    save(im, "pp10IgesFail")


# ============================================================
# pp-10-24 パラメトリック:寸法変更に形状が追従
# ============================================================
def pp10Parametric():
    im, d = new(); title(d, "パラメトリック:寸法変更に形状が追従")
    # 変更前
    box(d, 60, 110, 200, 220, FILL1)
    dim(d, 60, 240, 200, 240, "L = 50", col=BLUE)
    ctext(d, 130, 95, "変更前", FT, BLACK)
    arrow(d, 250, 175, 360, 175, BLACK, 4, 15)
    ctext(d, 305, 155, "L を 50→80 に", FT, RED)
    ctext(d, 305, 200, "変更", FT, GRAY)
    # 変更後(横に伸びる)
    box(d, 400, 110, 600, 220, FILL2)
    dim(d, 400, 240, 600, 240, "L = 80", col=RED)
    ctext(d, 500, 95, "変更後(形状が追従)", FT, BLACK)
    box(d, 90, 300, 570, 360, "white", 2, GRAY)
    ctext(d, 330, 330, "寸法をパラメータとして保持 → 値を変えると形状が連動して変形", FT, BLACK)
    note(d, "設計変更のやり直しが速い。最適化(重量最小化)やヒーリング(修復)とは目的が別。")
    save(im, "pp10Parametric")


# ============================================================
# pp-10-25 NURBS:制御点と重みで形が決まる
# ============================================================
def pp10Nurbs():
    im, d = new(); title(d, "NURBS:制御点と重みで形が決まる")
    cps = [(90, 320), (200, 110), (400, 110), (560, 300)]
    # 制御多角形(破線)
    for i in range(len(cps) - 1):
        dashed(d, cps[i][0], cps[i][1], cps[i + 1][0], cps[i + 1][1], GRAY, 2)
    for i, p in enumerate(cps):
        node(d, p[0], p[1], 6, fill=RED, col=RED)
        ctext(d, p[0], p[1] - 18, "P%d" % i, FT, RED)
    # 曲線(制御点は通らない・重み小)
    pts = []
    for t in [i / 60 for i in range(61)]:
        x = ((1 - t) ** 3 * cps[0][0] + 3 * (1 - t) ** 2 * t * cps[1][0]
             + 3 * (1 - t) * t * t * cps[2][0] + t ** 3 * cps[3][0])
        y = ((1 - t) ** 3 * cps[0][1] + 3 * (1 - t) ** 2 * t * cps[1][1]
             + 3 * (1 - t) * t * t * cps[2][1] + t ** 3 * cps[3][1])
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    ctext(d, 330, 205, "重み小の曲線", FT, BLUE)
    # 重み大で制御点側へ引き寄せ(別曲線)
    pts2 = []
    for t in [i / 60 for i in range(61)]:
        w = [1, 4, 4, 1]
        b = [(1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3]
        den = sum(w[i] * b[i] for i in range(4))
        x = sum(w[i] * b[i] * cps[i][0] for i in range(4)) / den
        y = sum(w[i] * b[i] * cps[i][1] for i in range(4)) / den
        pts2.append((x, y))
    d.line(pts2, fill=GREEN, width=3, joint="curve")
    ctext(d, 330, 150, "重み大 → 制御点側へ引き寄せ", FT, GREEN)
    note(d, "制御点の位置と各点の重みで形が決まる。制御点は曲面上に無く、直線や円弧も表現できる。")
    save(im, "pp10Nurbs")


# ============================================================
# pp-10-26 ベジエ曲面の接続:接線連続は自動でない
# ============================================================
def pp10BezierJoin():
    im, d = new(); title(d, "ベジエ曲面の接続:接線連続は自動でない")
    jx = 330
    # 左パッチ曲線
    l = [(70, 300), (170, 140), (270, 160), (jx, 220)]
    dashed(d, l[0][0], l[0][1], l[1][0], l[1][1], LGRAY, 2)
    dashed(d, l[2][0], l[2][1], l[3][0], l[3][1], LGRAY, 2)
    pts = []
    for t in [i / 50 for i in range(51)]:
        x = ((1 - t) ** 3 * l[0][0] + 3 * (1 - t) ** 2 * t * l[1][0] + 3 * (1 - t) * t * t * l[2][0] + t ** 3 * l[3][0])
        y = ((1 - t) ** 3 * l[0][1] + 3 * (1 - t) ** 2 * t * l[1][1] + 3 * (1 - t) * t * t * l[2][1] + t ** 3 * l[3][1])
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 右パッチ曲線(接続部で向きが折れる=キンク)
    r = [(jx, 220), (390, 300), (490, 150), (600, 250)]
    dashed(d, r[0][0], r[0][1], r[1][0], r[1][1], LGRAY, 2)
    pts2 = []
    for t in [i / 50 for i in range(51)]:
        x = ((1 - t) ** 3 * r[0][0] + 3 * (1 - t) ** 2 * t * r[1][0] + 3 * (1 - t) * t * t * r[2][0] + t ** 3 * r[3][0])
        y = ((1 - t) ** 3 * r[0][1] + 3 * (1 - t) ** 2 * t * r[1][1] + 3 * (1 - t) * t * t * r[2][1] + t ** 3 * r[3][1])
        pts2.append((x, y))
    d.line(pts2, fill=GREEN, width=3, joint="curve")
    node(d, jx, 220, 7, fill=RED, col=RED)
    ctext(d, jx, 195, "接続部でキンク(折れ)", FT, RED)
    ctext(d, 150, 120, "左パッチ", FT, BLUE); ctext(d, 520, 120, "右パッチ", FT, GREEN)
    note(d, "複数のベジエ面を貼り合わせても接線(1階微係数)連続は保証されない。重みは持たない。")
    save(im, "pp10BezierJoin")


# ============================================================
# pp-10-27 CADデータ品質(PDQ)
# ============================================================
def pp10Pdq():
    im, d = new(); title(d, "CADデータ品質(PDQ):微小図形・面の離れ")
    box(d, 60, 80, 600, 300, "white", 3, BLACK)
    # 面の離れ(隙間)
    d.line((150, 120, 150, 260), fill=BLACK, width=3)
    d.line((165, 120, 165, 260), fill=BLACK, width=3)
    dashed(d, 157, 120, 157, 260, RED, 2)
    ctext(d, 157, 285, "面の離れ(隙間)", FT, RED)
    # 微小サーフェス
    box(d, 300, 150, 315, 165, "white", 2, RED)
    ctext(d, 350, 130, "微小サーフェス", FT, RED)
    arrow(d, 350, 145, 315, 158, RED, 2, 9)
    # 微小図形要素(短いエッジ)
    d.line((460, 200, 468, 200), fill=RED, width=4)
    ctext(d, 500, 175, "微小エッジ", FT, RED)
    arrow(d, 500, 188, 466, 199, RED, 2, 9)
    ctext(d, 330, 320, "PDQ = Product Data Quality(3次元CADデータそのものの健全さ)", FT, BLACK)
    note(d, "PDQはCADデータの品質指標。アスペクト比・スキュー・ヤコビアンはメッシュ要素の指標。")
    save(im, "pp10Pdq")


# ============================================================
# pp-10-28 ヒーリング:壊れた形状を健全に整える
# ============================================================
def pp10Healing():
    im, d = new(); title(d, "ヒーリング:壊れた形状を健全に整える")
    # 変換で壊れた形状
    box(d, 55, 95, 270, 300, "white", 2, GRAY); ctext(d, 162, 112, "変換で生じた不具合", FT, RED)
    d.line((110, 150, 220, 150), fill=BLACK, width=3)      # 上辺
    d.line((110, 150, 110, 260), fill=BLACK, width=3)      # 左辺
    d.line((220, 150, 220, 210), fill=BLACK, width=3)      # 右辺(途切れ)
    dashed(d, 220, 210, 220, 260, RED, 2)                  # 未縫合エッジ
    d.line((110, 260, 180, 260), fill=BLACK, width=3)      # 下辺(隙間)
    dashed(d, 180, 260, 220, 260, RED, 2)
    box(d, 150, 180, 162, 192, "white", 2, RED)            # 微小サーフェス
    ctext(d, 162, 315, "隙間・未縫合・微小面", FT, RED)
    arrow(d, 285, 200, 355, 200, GREEN, 4, 15); ctext(d, 320, 180, "ヒーリング", FT, GREEN)
    # 修復後
    box(d, 370, 95, 605, 300, "white", 2, GRAY); ctext(d, 487, 112, "修復後(健全)", FT, BLACK)
    box(d, 420, 150, 560, 260, FILL1, 3, GREEN)
    ctext(d, 487, 315, "メッシュ生成できる", FT, GREEN)
    note(d, "ヒーリングは面の隙間・未縫合エッジ・微小面を修復。デフィーチャーやタイイングとは別作業。")
    save(im, "pp10Healing")


# ============================================================
# pp-10-29 アセンブリの階層構造と拘束
# ============================================================
def pp10Assembly():
    im, d = new(); title(d, "アセンブリの階層構造と拘束")
    # ツリー
    box(d, 55, 80, 320, 340, "white", 2, GRAY); ctext(d, 187, 98, "ツリー型の階層", FT, BLACK)
    box(d, 130, 118, 250, 150, FILL2); ctext(d, 190, 134, "アセンブリ", FT, BLACK)
    box(d, 80, 185, 195, 215, FILL1); ctext(d, 137, 200, "サブアセンブリ", FT, BLACK)
    box(d, 210, 185, 300, 215, FILL1); ctext(d, 255, 200, "パーツ", FT, BLACK)
    box(d, 75, 255, 145, 285, "white", 1, GRAY); ctext(d, 110, 270, "パーツ", FT, BLACK)
    box(d, 155, 255, 225, 285, "white", 1, GRAY); ctext(d, 190, 270, "パーツ", FT, BLACK)
    d.line((190, 150, 190, 168, 137, 168, 137, 185), fill=BLACK, width=2)
    d.line((190, 168, 255, 168, 255, 185), fill=BLACK, width=2)
    d.line((137, 215, 137, 240, 110, 240, 110, 255), fill=BLACK, width=2)
    d.line((137, 240, 190, 240, 190, 255), fill=BLACK, width=2)
    ctext(d, 187, 315, "拘束:一致・距離・平行・角度・接線", FT, GRAY)
    # 異種CAD変換は難しい
    box(d, 340, 110, 480, 220, FILL1); ctext(d, 410, 165, "CAD A", FS, BLACK); ctext(d, 410, 190, "カーネルX", FT, GRAY)
    box(d, 500, 110, 620, 220, FILL1); ctext(d, 560, 165, "CAD B", FS, BLACK); ctext(d, 560, 190, "カーネルY", FT, GRAY)
    arrow(d, 482, 150, 498, 150, RED, 3, 11)
    d.line((484, 165, 496, 177), fill=RED, width=3); d.line((496, 165, 484, 177), fill=RED, width=3)
    ctext(d, 480, 255, "カーネルが違うとトポロジー表現が異なり", FT, RED)
    ctext(d, 480, 278, "簡単・確実な変換はできない(不具合が出やすい)", FT, RED)
    note(d, "階層構造と拘束・トポロジーで構成。カーネルの違う異種CADへの変換は容易ではない。")
    save(im, "pp10Assembly")


# ============================================================
# pp-10-30 コンタ表示に向く量・向かない量
# ============================================================
def pp10ContourQty():
    im, d = new(); title(d, "コンタ表示に向く量・向かない量")
    # 向く(連続量)
    box(d, 45, 80, 320, 320, "white", 2, GREEN); ctext(d, 182, 100, "向く:連続的な物理量", FS, GREEN)
    # なめらかコンタ帯
    for i, c in enumerate([(40, 80, 190), (30, 150, 200), (30, 170, 90), (230, 200, 40), (210, 90, 40)]):
        d.rectangle((70 + i * 36, 140, 70 + (i + 1) * 36, 200), fill=c, outline="white", width=1)
    ctext(d, 145, 215, "値を色分け", FT, GRAY)
    mlines(d, 182, 265, ["各軸応力成分・ミーゼス応力", "主応力・変位"], FT, BLACK, 24)
    # 向かない(離散ラベル)
    box(d, 340, 80, 615, 320, "white", 2, RED); ctext(d, 477, 100, "向かない:離散ラベル", FS, RED)
    mlines(d, 477, 200, ["節点番号・要素番号", "材料ID・拘束記号", "座標系・積分点番号", "ファイル名・計算時間"], FT, BLACK, 30)
    ctext(d, 477, 300, "連続量でないため色分け不可", FT, RED)
    note(d, "コンタは値の大小を色分けする=連続的なスカラ量が対象。番号・IDなどの離散ラベルは不向き。")
    save(im, "pp10ContourQty")


# ============================================================
# pp-10-32 積分点(ガウス点)で応力が最も高精度
# ============================================================
def pp10GaussStress():
    im, d = new(); title(d, "積分点(ガウス点)で応力が最も高精度")
    # 四辺形要素
    x0, y0, s = 180, 110, 200
    box(d, x0, y0, x0 + s, y0 + s, FILL1)
    # 節点(角)
    for (px, py) in [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)]:
        node(d, px, py, 7, fill="white", col=BLACK)
    ctext(d, x0 - 10, y0 - 10, "節点", FT, GRAY, "rm")
    # ガウス点(2x2)を星印(+)で
    g = 0.211  # (1-1/sqrt3)/2 approx
    for gx in (x0 + s * g, x0 + s * (1 - g)):
        for gy in (y0 + s * g, y0 + s * (1 - g)):
            d.line((gx - 8, gy, gx + 8, gy), fill=RED, width=3)
            d.line((gx, gy - 8, gx, gy + 8), fill=RED, width=3)
    ctext(d, x0 + s / 2, y0 + s / 2, "ガウス点(赤+)", FT, RED)
    # 説明
    box(d, 410, 110, 620, 175, "white", 2, RED)
    mlines(d, 515, 142, ["ガウス点:誤差最小になる", "位置 → 応力が最良"], FT, RED, 22)
    box(d, 410, 200, 620, 300, "white", 2, GRAY)
    mlines(d, 515, 250, ["節点応力:積分点値の", "外挿・隣接要素の平均", "→ 精度が落ちる"], FT, BLACK, 24)
    note(d, "高精度の理由は積分点位置が誤差最小に選ばれること。個数が多いからではない(点は節点より少)。")
    save(im, "pp10GaussStress")


# ============================================================
# pp-10-33 積分点値と補間関数で要素内コンタ
# ============================================================
def pp10ElemContour():
    im, d = new(); title(d, "積分点値と補間関数で要素内コンタ")
    x0, y0, s = 90, 110, 230
    box(d, x0, y0, x0 + s, y0 + s, "white", 3, BLACK)
    g = 0.211
    gpts = []
    for gx in (x0 + s * g, x0 + s * (1 - g)):
        for gy in (y0 + s * g, y0 + s * (1 - g)):
            gpts.append((gx, gy))
    # コンタ(要素内で変化・一定でない)
    for k, yy in enumerate(range(y0 + 20, y0 + s, 26)):
        d.line((x0 + 6, yy + 30, x0 + s - 6, yy - 20), fill=BLUE, width=2)
    for (gx, gy) in gpts:
        d.line((gx - 7, gy, gx + 7, gy), fill=RED, width=3)
        d.line((gx, gy - 7, gx, gy + 7), fill=RED, width=3)
    ctext(d, x0 + s / 2, y0 + s + 18, "積分点値(赤+)+補間関数 → 要素内の等値線", FT, BLACK)
    box(d, 360, 120, 620, 300, FILL2)
    mlines(d, 490, 210,
           ["線形四辺形要素の応力は", "要素内で一定ではない", "", "精度のよい積分点の値を", "補間関数で要素内へ広げ", "等値線として描く"], FT, BLACK, 26)
    note(d, "積分点の応力値と要素の補間(形状)関数で要素内部の各点の応力を評価し描画する。")
    save(im, "pp10ElemContour")


# ============================================================
# pp-10-34 表示手法:ワイヤー/フラット/スムーズ
# ============================================================
def pp10Shading():
    im, d = new(); title(d, "表示手法:ワイヤーフレーム/フラット/スムーズ")

    def sphere_facets(ox, oy, mode):
        # 疑似球(多角形帯)で3手法を対比
        r = 70
        if mode == 0:  # ワイヤーフレーム
            for a in range(0, 360, 30):
                d.line((ox, oy - r, ox + r * math.sin(math.radians(a)) * 0.4, oy,
                        ox, oy + r), fill=BLACK, width=1)
            for ry in (-40, 0, 40):
                rr = math.sqrt(max(r * r - ry * ry, 1))
                d.ellipse((ox - rr, oy + ry - 8, ox + rr, oy + ry + 8), outline=BLACK, width=1)
        elif mode == 1:  # フラット(面ごと1色)
            shades = [(90, 90, 90), (140, 140, 140), (180, 180, 180), (150, 150, 150), (110, 110, 110)]
            for i in range(5):
                a0 = -90 + i * 40; a1 = a0 + 40
                pts = [(ox, oy)]
                for a in range(int(a0), int(a1) + 1, 8):
                    pts.append((ox + r * math.cos(math.radians(a)), oy + r * math.sin(math.radians(a))))
                d.polygon(pts, fill=shades[i], outline=BLACK)
            d.ellipse((ox - r, oy - r, ox + r, oy + r), outline=BLACK, width=2)
        else:  # スムーズ(グラデーション)
            for i in range(r, 0, -2):
                v = int(70 + (1 - i / r) * 150)
                d.ellipse((ox - i, oy - i, ox + i, oy + i), fill=(v, v, v))
            d.ellipse((ox - r, oy - r, ox + r, oy + r), outline=BLACK, width=2)

    labels = ["ワイヤーフレーム", "フラットシェーディング", "スムーズシェーディング"]
    subs = ["線だけ(軽い)", "面ごと1色・法線で反射", "節点法線を補間・高品位"]
    for i, ox in enumerate((150, 340, 530)):
        box(d, ox - 95, 70, ox + 95, 350, "white", 2, GRAY)
        sphere_facets(ox, 190, i)
        ctext(d, ox, 305, labels[i], FT, (BLUE if i == 1 else BLACK))
        ctext(d, ox, 330, subs[i], FT, GRAY)
    note(d, "フラットは面単位で塗り法線から反射を計算する軽い手法。スムーズは補間で高品位に陰影づけ。")
    save(im, "pp10Shading")


# ============================================================
# pp-10-35 メッシュ表示の処理パイプライン
# ============================================================
def pp10RenderPipeline():
    im, d = new(); title(d, "メッシュ表示の処理パイプライン")
    vflow(d, [["表面パッチ(ファセット)を抽出"],
              ["座標変換で回転(視点に合わせる)"],
              ["隠面消去(手前の面で隠れる面を消す)"],
              ["画像生成(画面へ描画)"]],
          x0=120, x1=540, y0=70, bh=48, gap=22,
          fills=[FILL1, FILL1, FILL2, FILL1])
    note(d, "描く表面を用意→向きを合わせる→重なりを整理→出力。隠面消去は座標変換の後・画像生成の前。")
    save(im, "pp10RenderPipeline")


# ============================================================
# pp-10-36 断面カラーコンタの処理順序
# ============================================================
def pp10SectionPipeline():
    im, d = new(); title(d, "断面カラーコンタの処理順序")
    vflow(d, [["切断平面の定義(どこで切るか)"],
              ["交差要素の抽出(何が切られるか)"],
              ["交点・断面パッチ生成(切り口の形)"],
              ["交点の物理量を補間(切り口の値)"],
              ["カラーコンタ画像生成(着色)"]],
          x0=110, x1=550, y0=58, bh=44, gap=15,
          fills=[FILL1, FILL1, FILL1, FILL2, FILL1])
    note(d, "どこで切る→何が切られる→切り口の形→切り口の値→着色。補間は断面パッチ生成の後。")
    save(im, "pp10SectionPipeline")


ALL = [pp10OpStack, pp10ThreeStages, pp10PreInputs, pp10FemWorkflow, pp10GradientRefine,
       pp10CoarseFineTransition, pp10Elem3DNodes, pp10QualityChecks, pp10AbruptSizeJump,
       pp10Delaunay, pp10IgesExchange, pp10CsvColumns, pp10IgesFail, pp10Parametric,
       pp10Nurbs, pp10BezierJoin, pp10Pdq, pp10Healing, pp10Assembly, pp10ContourQty,
       pp10GaussStress, pp10ElemContour, pp10Shading, pp10RenderPipeline, pp10SectionPipeline]

KEYS = ["pp10OpStack", "pp10ThreeStages", "pp10PreInputs", "pp10FemWorkflow", "pp10GradientRefine",
        "pp10CoarseFineTransition", "pp10Elem3DNodes", "pp10QualityChecks", "pp10AbruptSizeJump",
        "pp10Delaunay", "pp10IgesExchange", "pp10CsvColumns", "pp10IgesFail", "pp10Parametric",
        "pp10Nurbs", "pp10BezierJoin", "pp10Pdq", "pp10Healing", "pp10Assembly", "pp10ContourQty",
        "pp10GaussStress", "pp10ElemContour", "pp10Shading", "pp10RenderPipeline", "pp10SectionPipeline"]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    miss = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(KEYS), "MISSING", miss)
