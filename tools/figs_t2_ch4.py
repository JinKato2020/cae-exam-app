# -*- coding: utf-8 -*-
"""熱流体力学2級 第4章「数値計算法」の図(接頭辞 t2e4)を13枚描く。
JSON本体は編集しない。white 660x420 線画・機構だけ。
required(回答前表示)には答え・正解値・結論を絶対に描かない(§3/§8)。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- ローカル補助 -------------------------------------------------
def box(d, cx, cy, w, h, text, fnt=FS, fill="white"):
    """中央(cx,cy)の角丸なし矩形＋中央テキスト。text は改行\n可。"""
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=BLACK, width=3, fill=fill)
    lines = text.split("\n")
    lh = fnt.size + 6
    y0 = cy - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        ctext(d, cx, y0 + i * lh, ln, fnt)


def table(d, x, y, rows, col_w, row_h=44, fnt=FT, hfnt=FS):
    """rows: 2次元リスト(1行目=見出し)。col_w: 各列幅。左詰めセル。"""
    ncol = len(col_w)
    xs = [x]
    for w in col_w:
        xs.append(xs[-1] + w)
    tw = sum(col_w)
    nrow = len(rows)
    # 見出し行の淡色塗り(先に塗ってから罫線)
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
# 4-1 required : 2階PDE 判別式D=B^2-4AC の符号→型 の一般対応表
# (本問の係数・判別結果・答え=楕円 は描かない)
def f01():
    im, d = new()
    title(d, "2階PDEの型判別（判別式で分類）")
    ctext(d, W / 2, 66, "一般形:  A・u_xx + B・u_xy + C・u_yy + ... = 0", F)
    rows = [
        ["判別式 D=B^2-4AC", "型", "代表する物理現象"],
        ["D > 0", "双曲型", "波動・振動"],
        ["D = 0", "放物型", "熱伝導・拡散"],
        ["D < 0", "楕円型", "定常場（ラプラス/ポアソン）"],
    ]
    table(d, 50, 100, rows, [220, 130, 260], row_h=58, fnt=FS)
    note(d, "本問は係数A,B,Cを読み取り、Dの符号で型を判定する")
    save(im, "t2e4PdeDiscriminant")


# 4-2 helpful : 4種の誤差 対比表
def f02():
    im, d = new()
    title(d, "数値計算の4つの誤差")
    rows = [
        ["誤差", "発生原因", "低減策"],
        ["丸め誤差", "有限桁の表現", "語長(ビット)を増やす"],
        ["打ち切り誤差", "級数の打ち切り", "展開の項数を増やす"],
        ["位相誤差", "時間の離散化", "スキームの改良"],
        ["エイリアジング誤差", "波数の折り返し", "パディング法"],
    ]
    table(d, 30, 80, rows, [200, 200, 230], row_h=60, fnt=FS)
    save(im, "t2e4ErrorTypes")


# 4-3 required : 5点ステンシル(中央=?, 左40 右120 上60 下20, Δx=Δy)
# (答え=中央値60 は描かない)
def f03():
    im, d = new()
    title(d, "ラプラス方程式の5点ステンシル")
    cx, cy = 330, 235
    L = 130
    pts = {"上": (cx, cy - L, "60"), "下": (cx, cy + L, "20"),
           "左": (cx - L, cy, "40"), "右": (cx + L, cy, "120")}
    for lab, (nx, ny, val) in pts.items():
        d.line((cx, cy, nx, ny), fill=GRAY, width=2)
    for lab, (nx, ny, val) in pts.items():
        node(d, nx, ny, r=30, fill="white")
        ctext(d, nx, ny, val, F)
    # 位置ラベル
    ctext(d, pts["上"][0], pts["上"][1] - 46, "上", FS, GRAY)
    ctext(d, pts["下"][0], pts["下"][1] + 46, "下", FS, GRAY)
    ctext(d, pts["左"][0] - 46, pts["左"][1], "左", FS, GRAY)
    ctext(d, pts["右"][0] + 46, pts["右"][1], "右", FS, GRAY)
    # 中央=未知
    node(d, cx, cy, r=34, fill=FILL1)
    ctext(d, cx, cy, "?", FL, RED)
    dim(d, cx + 6, cy - L + 30, cx + 6, cy - 34, "Δx=Δy", col=GRAY)
    save(im, "t2e4LaplaceStencil")


# 4-4 helpful : 4手法 対比表
def f04():
    im, d = new()
    title(d, "代表的な離散化手法")
    rows = [
        ["手法", "離散化の単位", "特徴"],
        ["有限差分法 (FDM)", "格子点", "差分商で勾配を近似"],
        ["有限要素法 (FEM)", "要素", "弱形式・ガラーキン法"],
        ["有限体積法 (FVM)", "検査体積", "界面フラックス・保存性"],
        ["スペクトル法", "波数", "高精度・形状に制約"],
    ]
    table(d, 30, 80, rows, [220, 150, 250], row_h=60, fnt=FS)
    save(im, "t2e4DiscretizationMethods")


# 4-5 required : 1次元3格子点 (φ=2,8,5)・u>0・Δx=0.5
# (答え=36 は描かない)
def f05():
    im, d = new()
    title(d, "1次精度風上差分（u>0）")
    y = 250
    xs = [180, 350, 520]
    labs = ["x-Δx", "x", "x+Δx"]
    vals = ["φ=2", "φ=8", "φ=5"]
    d.line((110, y, 590, y), fill=BLACK, width=2)
    ctext(d, 600, y, "x", FS, BLACK, "lm")
    for px, lb, vl in zip(xs, labs, vals):
        node(d, px, y, r=9, fill=BLACK)
        ctext(d, px, y + 26, lb, FS)
        ctext(d, px, y - 26, vl, FS, BLUE)
    # 流れ方向
    arrow(d, 250, y - 80, 450, y - 80, RED, 4, 15)
    ctext(d, 350, y - 104, "流れ  u>0", FS, RED)
    # Δx 寸法
    dim(d, xs[0], y + 60, xs[1], y + 60, "Δx=0.5", col=GRAY)
    dim(d, xs[1], y + 60, xs[2], y + 60, "Δx=0.5", col=GRAY)
    save(im, "t2e4UpwindNodes")


# 4-6 required : オイラー陽解法の時間前進 (y0=5, Δt=0.1, 2ステップ)
# (答え=y2=3.2 は描かない)
def f06():
    im, d = new()
    title(d, "オイラー陽解法の時間前進")
    y = 250
    xs = [150, 340, 530]
    labs = ["t0", "t1=t0+Δt", "t2=t1+Δt"]
    vals = ["y0=5", "y1=?", "y2=?"]
    cols = [BLUE, RED, RED]
    axes(d, 100, y, 500, 0, "t", "")
    for px, lb, vl, cl in zip(xs, labs, vals, cols):
        d.line((px, y - 6, px, y + 6), fill=BLACK, width=2)
        ctext(d, px, y + 26, lb, FT)
        ctext(d, px, y - 26, vl, FS, cl)
    arrow(d, xs[0], y - 60, xs[1], y - 60, BLACK, 3, 13)
    arrow(d, xs[1], y - 60, xs[2], y - 60, BLACK, 3, 13)
    ctext(d, (xs[0] + xs[1]) / 2, y - 82, "Δt=0.1", FT, GRAY)
    ctext(d, (xs[1] + xs[2]) / 2, y - 82, "Δt=0.1", FT, GRAY)
    ctext(d, W / 2, 340, "更新式:  y^(n+1) = y^n + Δt・f(y^n)", F)
    save(im, "t2e4EulerMarch")


# 4-7 helpful : SIMPLE法の圧力補正反復ループ
def f07():
    im, d = new()
    title(d, "SIMPLE法の圧力補正ループ")
    cx = 360
    boxes = [
        (95, "仮の圧力から予測速度を計算"),
        (170, "圧力補正方程式を解く"),
        (245, "速度・圧力を修正"),
        (325, "連続式を満たすか？"),
    ]
    for cy, txt in boxes:
        box(d, cx, cy, 320, 46, txt, FS)
    for i in range(len(boxes) - 1):
        arrow(d, cx, boxes[i][0] + 23, cx, boxes[i + 1][0] - 23, BLACK, 3, 12)
    # 収束→終了
    arrow(d, cx + 160, boxes[3][0], cx + 250, boxes[3][0], GREEN, 3, 12)
    ctext(d, cx + 235, boxes[3][0] - 18, "収束→終了", FT, GREEN)
    # 未収束フィードバック(左回り: 4→2)
    lx = 110
    d.line((cx - 160, boxes[3][0], lx, boxes[3][0]), fill=RED, width=3)
    d.line((lx, boxes[3][0], lx, boxes[1][0]), fill=RED, width=3)
    arrow(d, lx, boxes[1][0], cx - 160, boxes[1][0], RED, 3, 12)
    ctext(d, lx + 6, (boxes[1][0] + boxes[3][0]) / 2, "未収束\nなら反復",
          FT, RED, "lm")
    save(im, "t2e4SimpleLoop")


# 4-8 required : ルンゲ現象(等間隔標本＋高次多項式が端で振動)
# (手法名/正解=スプライン は描かない)
def f08():
    im, d = new()
    title(d, "高次多項式補間の端での振動")

    def runge(x):
        return 1.0 / (1.0 + 25.0 * x * x)

    n = 11
    nodes = [-1 + 2 * i / (n - 1) for i in range(n)]
    ynodes = [runge(x) for x in nodes]

    def lagrange(x):
        tot = 0.0
        for i in range(n):
            term = ynodes[i]
            for j in range(n):
                if j != i:
                    term *= (x - nodes[j]) / (nodes[i] - nodes[j])
            tot += term
        return tot

    ox, oy = 90, 315          # 原点(x=-1, y=0)相当は左端・baseline
    xscale = 500 / 2.0        # x:[-1,1]->500px
    yscale = 135.0            # y=1 -> 135px上
    axes(d, ox, oy, 520, 300, "x", "y")

    def px(x):
        return ox + (x + 1) * xscale

    def py(yv):
        return oy - yv * yscale
    # 補間曲線
    curve = []
    m = 240
    for k in range(m + 1):
        x = -1 + 2 * k / m
        curve.append((px(x), py(lagrange(x))))
    plot(d, ox, oy, curve, BLUE, 3)
    # 標本点(黒四角)
    for x, yv in zip(nodes, ynodes):
        X, Y = px(x), py(yv)
        d.rectangle((X - 5, Y - 5, X + 5, Y + 5), fill=BLACK)
    ctext(d, px(0), py(1.0) - 22, "標本点(等間隔)", FT, BLACK)
    note(d, "区間の両端で補間曲線が激しく振動する")
    save(im, "t2e4RungePhenomenon")


# 4-9 helpful : SORと他解法の対比表
def f09():
    im, d = new()
    title(d, "反復解法SORと他の解法")
    rows = [
        ["解法", "分類", "しくみ"],
        ["SOR法", "反復", "点反復＋緩和係数で加速"],
        ["TDMA", "直接", "三重対角を前進消去・後退代入"],
        ["CG法", "反復", "共役な探索方向を用いる"],
        ["ADI法", "反復", "行方向と列方向を交互に更新"],
    ]
    table(d, 25, 80, rows, [130, 110, 370], row_h=60, fnt=FS)
    save(im, "t2e4SorCompare")


# 4-10 helpful : 同じ要素数でも節点数が変わる(必要記憶量)
def f10():
    im, d = new()
    title(d, "要素の種類と節点数（必要記憶量）")

    def tri(cx, cy, s, mid, cap):
        A = (cx, cy - s)
        B = (cx - s * 0.9, cy + s * 0.7)
        C = (cx + s * 0.9, cy + s * 0.7)
        d.polygon([A, B, C], outline=BLACK, width=3)
        corners = [A, B, C]
        for p in corners:
            node(d, p[0], p[1], r=8, fill=BLACK)
        cnt = 3
        if mid:
            mids = [((A[0] + B[0]) / 2, (A[1] + B[1]) / 2),
                    ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2),
                    ((C[0] + A[0]) / 2, (C[1] + A[1]) / 2)]
            for p in mids:
                node(d, p[0], p[1], r=8, fill="white")
            cnt = 6
        ctext(d, cx, cy + s * 0.7 + 40, cap, FS)
        ctext(d, cx, cy + s * 0.7 + 68, "総節点数 " + str(cnt), FS, RED)
    tri(190, 210, 95, False, "3節点 三角形")
    tri(475, 210, 95, True, "6節点 三角形")
    note(d, "要素数が同じでも節点数が変われば必要記憶量が変わる")
    save(im, "t2e4FemMemory")


# 4-11 required : CFL=uΔt/Δx の定義図 (与件 u=4, Δx=0.02。答えΔtは描かない)
def f11():
    im, d = new()
    title(d, "クーラン数（CFL数）の定義")
    y = 210
    # 格子(いくつかのマス)
    x0 = 90
    dxpix = 90
    for i in range(6):
        xx = x0 + i * dxpix
        d.line((xx, y - 30, xx, y + 30), fill=BLACK, width=2)
    d.line((x0, y, x0 + 5 * dxpix, y), fill=BLACK, width=1)
    # 1マス=Δx を強調
    d.rectangle((x0, y - 30, x0 + dxpix, y + 30), outline=BLUE, width=3)
    dim(d, x0, y + 55, x0 + dxpix, y + 55, "Δx=0.02 m", col=BLUE)
    # 情報伝達距離 uΔt
    arrow(d, x0, y - 70, x0 + int(dxpix * 1.6), y - 70, RED, 4, 15)
    ctext(d, x0 + int(dxpix * 0.9), y - 94, "情報の伝達距離 = u・Δt", FS, RED)
    ctext(d, W / 2, 330, "CFL = u・Δt / Δx    （u=4 m/s）", F)
    note(d, "1ステップで情報が伝わる距離と格子幅の比")
    save(im, "t2e4CourantCFL")


# 4-12 helpful : 陽解法/陰解法 対比表
def f12():
    im, d = new()
    title(d, "陽解法と陰解法の比較")
    rows = [
        ["項目", "陽解法", "陰解法"],
        ["右辺の評価", "現時刻(既知)", "次時刻(未知)を含む"],
        ["連立方程式", "不要", "必要（行列/反復）"],
        ["1ステップの負荷", "小", "大"],
        ["安定性", "条件つき", "高い（大きなΔtも可）"],
    ]
    table(d, 30, 80, rows, [190, 190, 230], row_h=60, fnt=FS)
    save(im, "t2e4ImplicitExplicit")


# 4-13 helpful : 差分スキームの性質比較
def f13():
    im, d = new()
    title(d, "差分スキームの性質比較")
    rows = [
        ["スキーム", "数値粘性", "精度次数", "ガリレイ不変性"],
        ["1次 風上", "大", "1次", "満たさない"],
        ["3次 風上", "小", "3次", "満たさない"],
        ["中心差分", "なし", "2次", "満たす"],
    ]
    table(d, 25, 90, rows, [150, 130, 120, 210], row_h=64, fnt=FS)
    save(im, "t2e4SchemeProps")


if __name__ == "__main__":
    for fn in [f01, f02, f03, f04, f05, f06, f07,
               f08, f09, f10, f11, f12, f13]:
        fn()
    print("done 13")
