# -*- coding: utf-8 -*-
"""固体2級 第12章 コンピュータ 図7枚。白地660x420・黒線画。JSON本体は編集しない。"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

# ---- 共通ヘルパ ----
def box(d, x0, y0, x1, y1, fill="white", col=BLACK, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)

def digits(d, x0, y, p, chars, colors=None):
    """等ピッチで1文字ずつ中央配置。x0=先頭セル中心x, p=ピッチ。"""
    for i, ch in enumerate(chars):
        c = BLACK if colors is None else colors[i]
        ctext(d, x0 + i * p, y, ch, F, c)


# ============================================================
# 1. comp12InfoLoss  情報落ち(桁の違う2数の加算)
# ============================================================
def info_loss():
    im, d = new()
    title(d, "情報落ち:桁の違う数の足し算で下位桁が消える")
    p = 37; x0 = 150
    win = 7                       # 有効桁の窓(例:7桁)
    bx = x0 + win * p - p / 2     # 窓の右境界x
    right = x0 + 12 * p + p / 2
    # 窓外(消える領域)を淡グレーで塗る
    d.rectangle((bx, 95, right, 300), fill=(238, 238, 238))
    # 有効桁の窓ラベル
    ctext(d, (x0 - p/2 + bx) / 2, 82, "有効桁の窓(例:7桁)", FT, BLUE)
    ctext(d, (bx + right) / 2, 82, "表現できず消える", FT, GRAY)
    # 赤い境界線
    d.line((bx, 95, bx, 300), fill=RED, width=3)

    A = list("1.234567000000")
    B = list("0.000000004321")
    # Aの数字色
    cA = [BLACK] * len(A)
    # Bの色:有効数字4321を赤(窓外で消える情報)
    cB = [BLACK] * len(B)
    for i in range(len(B)):
        if B[i] not in ".0":
            cB[i] = RED
    ctext(d, 92, 120, "A", F, BLACK, "rm")
    digits(d, x0, 120, p, A, cA)
    ctext(d, 92, 180, "+ B", F, BLACK, "rm")
    digits(d, x0, 180, p, B, cB)
    d.line((80, 218, right, 218), fill=BLACK, width=2)
    ctext(d, 92, 258, "A+B", F, BLACK, "rm")
    R = list("1.234567")
    digits(d, x0, 258, p, R, [BLACK]*len(R))
    note(d, "小さいBの有効数字(赤)は窓の外に落ち、和はAのまま=情報落ち")
    save(im, "comp12InfoLoss")


# ============================================================
# 2. comp12Cancellation  桁落ち(近い2数の引き算)
# ============================================================
def cancellation():
    im, d = new()
    title(d, "桁落ち:近い数の引き算で上位桁が消え有効桁が減る")
    p = 40; x0 = 175
    A = list("1.2345678")
    B = list("1.2345611")
    R = list("0.0000067??")
    # 打ち消し合う上位(先頭7セル 1.23456)を淡グレー
    d.rectangle((x0 - p/2, 95, x0 + 6.5 * p, 300), fill=(238, 238, 238))
    ctext(d, x0 + 3 * p, 82, "上位の同じ桁 → 打ち消し合う", FT, GRAY)
    ctext(d, x0 + 8.5 * p, 82, "残る有効桁", FT, RED)

    ctext(d, 110, 120, "A", F, BLACK, "rm")
    digits(d, x0, 120, p, A, [GRAY]*7 + [BLACK]*2)
    ctext(d, 110, 180, "- B", F, BLACK, "rm")
    digits(d, x0, 180, p, B, [GRAY]*7 + [BLACK]*2)
    d.line((90, 218, x0 + 10.5 * p, 218), fill=BLACK, width=2)
    ctext(d, 110, 258, "A-B", F, BLACK, "rm")
    cR = []
    for i, ch in enumerate(R):
        if ch == "?":
            cR.append(GRAY)
        elif ch in ".0":
            cR.append(GRAY)
        else:
            cR.append(RED)
    digits(d, x0, 258, p, R, cR)
    note(d, "有効数字が7桁→2桁に激減。下位(?)は不定=桁落ち")
    save(im, "comp12Cancellation")


# ============================================================
# 3. comp12NewlineCode  OS別 改行コード対照表
# ============================================================
def newline_code():
    im, d = new()
    title(d, "OS による改行コードの違い")
    cols = [230, 190, 120]            # OS / 改行コード / 記号
    x0 = 60; y0 = 90; rh = 62
    xs = [x0]
    for w in cols:
        xs.append(xs[-1] + w)
    rows = [
        ("OS / 環境", "改行コード", "16進"),
        ("Windows", "CR + LF", "0D 0A"),
        ("Unix / Linux / macOS", "LF", "0A"),
        ("旧 Mac OS(〜9)", "CR", "0D"),
    ]
    for r, row in enumerate(rows):
        y = y0 + r * rh
        fillc = FILL2 if r == 0 else "white"
        for c in range(3):
            box(d, xs[c], y, xs[c+1], y + rh, fill=fillc, wd=2)
            fnt = FS if (r == 0 or (r == 2 and c == 0)) else F
            ctext(d, (xs[c] + xs[c+1]) / 2, y + rh/2, row[c], fnt, BLACK)
    note(d, "CR=復帰(0x0D)、LF=改行(0x0A)。テキスト移送時の文字化け要因")
    save(im, "comp12NewlineCode")


# ============================================================
# 4. comp12CacheHierarchy  記憶階層(速度/容量)
# ============================================================
def cache_hierarchy():
    im, d = new()
    title(d, "記憶の階層:上ほど高速・小容量")
    cx = 320
    ws = [110, 190, 280, 380, 470]    # 各境界の幅
    labels = ["CPU レジスタ", "キャッシュメモリ", "主記憶(メインメモリ)", "補助記憶(SSD / HDD)"]
    fills = [FILL3, FILL2, FILL1, "white"]
    yt = 70; h = 72
    for i in range(4):
        tw, bw = ws[i], ws[i+1]
        y0 = yt + i * h; y1 = y0 + h
        d.polygon([(cx - tw/2, y0), (cx + tw/2, y0),
                   (cx + bw/2, y1), (cx - bw/2, y1)],
                  outline=BLACK, width=3, fill=fills[i])
        ctext(d, cx, (y0 + y1) / 2, labels[i], FS, BLACK)
    # 左:高速・小容量(上向き矢印)
    arrow(d, 45, 350, 45, 80, BLUE, 3, 13)
    ctext(d, 45, 70, "高速", FT, BLUE)
    ctext(d, 30, 210, "小", FT, BLUE)
    # 右:大容量・低速(下向き矢印)
    arrow(d, 600, 80, 600, 350, RED, 3, 13)
    ctext(d, 600, 366, "大容量", FT, RED)
    ctext(d, 615, 210, "低速", FT, RED)
    save(im, "comp12CacheHierarchy")


# ============================================================
# 5. comp12FloatingLicense  フローティングライセンス
# ============================================================
def floating_license():
    im, d = new()
    title(d, "フローティングライセンス:サーバに接続した台のみ使用可")
    # サーバ
    sx0, sy0, sx1, sy1 = 210, 70, 400, 140
    box(d, sx0, sy0, sx1, sy1, fill=FILL2)
    ctext(d, (sx0+sx1)/2, 95, "ライセンスサーバ", FS, BLACK)
    ctext(d, (sx0+sx1)/2, 120, "(同時使用数を貸与)", FT, GRAY)
    bus_y = 200
    d.line((90, bus_y, 400, bus_y), fill=BLACK, width=3)
    d.line((305, sy1, 305, bus_y), fill=BLACK, width=3)
    # 接続中クライアント3台
    for i, x in enumerate((90, 200, 310)):
        cx0, cy0 = x - 40, 250
        box(d, cx0, cy0, cx0 + 80, cy0 + 55, fill="white")
        ctext(d, x, cy0 + 27, "PC", F, BLACK)
        d.line((x, bus_y, x, cy0), fill=BLACK, width=2)
        ctext(d, x, cy0 + 72, "使用可", FT, GREEN)
    # 未接続クライアント
    dx = 545
    box(d, dx - 45, 250, dx + 45, 305, fill=(245, 235, 235))
    ctext(d, dx, 277, "PC", F, BLACK)
    # 切れた接続(点線風)+X印
    for yy in range(205, 250, 12):
        d.line((dx, yy, dx, yy + 6), fill=GRAY, width=2)
    d.line((dx - 14, 218, dx + 14, 246), fill=RED, width=4)
    d.line((dx + 14, 218, dx - 14, 246), fill=RED, width=4)
    ctext(d, dx, 320, "未接続=使用不可", FT, RED)
    save(im, "comp12FloatingLicense")


# ============================================================
# 6. comp12ParallelMemory  共有メモリ型 vs 分散メモリ型
# ============================================================
def parallel_memory():
    im, d = new()
    title(d, "並列計算機:メモリ構成の違い")
    d.line((330, 55, 330, 400), fill=LGRAY, width=2)
    ctext(d, 170, 70, "共有メモリ型", FS, BLUE)
    ctext(d, 495, 70, "分散メモリ型", FS, RED)

    # --- 左:共有メモリ ---
    mx0, mx1 = 55, 290
    box(d, mx0, 100, mx1, 145, fill=FILL2)
    ctext(d, (mx0+mx1)/2, 122, "共有メモリ", FS, BLACK)
    busL = 195
    d.line((70, busL, 280, busL), fill=BLACK, width=3)
    d.line((175, 145, 175, busL), fill=BLACK, width=3)
    for i, x in enumerate((80, 150, 220, 285 - 15)):
        cx = x
        box(d, cx - 26, 235, cx + 26, 285, fill="white")
        ctext(d, cx, 260, "CPU", FT, BLACK)
        d.line((cx, busL, cx, 235), fill=BLACK, width=2)
    ctext(d, 170, 320, "全CPUが1つのメモリを共有", FT, GRAY)

    # --- 右:分散メモリ ---
    netY = 110
    d.line((360, netY, 635, netY), fill=BLACK, width=3)
    ctext(d, 497, 92, "ネットワーク(相互結合網)", FT, GRAY)
    for x in (390, 497, 604):
        d.line((x, netY, x, 150), fill=BLACK, width=2)
        box(d, x - 32, 150, x + 32, 195, fill="white")     # CPU
        ctext(d, x, 172, "CPU", FT, BLACK)
        d.line((x, 195, x, 215), fill=BLACK, width=2)
        box(d, x - 32, 215, x + 32, 258, fill=FILL2)        # メモリ
        ctext(d, x, 236, "メモリ", FT, BLACK)
    ctext(d, 497, 320, "各CPUが専用メモリを持ち通信", FT, GRAY)
    save(im, "comp12ParallelMemory")


# ============================================================
# 7. comp12ParallelEff  並列化効率(理想1/n vs 実測)
# ============================================================
def parallel_eff():
    im, d = new()
    title(d, "並列化効率:理想時間 ÷ 実測時間")
    ox, oy = 120, 340
    unit = 240.0                       # 相対時間1.0 = 240px
    axes(d, ox, oy, 470, 285, "", "")
    ctext(d, ox + 6, oy - 276, "計算時間(相対)", FT, BLACK, "lm")
    # 目盛 0,0.5,1.0
    for v in (0.5, 1.0):
        yy = oy - v * unit
        d.line((ox - 6, yy, ox, yy), fill=BLACK, width=2)
        ctext(d, ox - 12, yy, f"{v:.1f}", FT, BLACK, "rm")
    ctext(d, ox - 12, oy, "0", FT, BLACK, "rm")

    bars = [("逐次\n(1CPU)", 1.00, FILL2),
            ("理想\n(4CPU)", 0.25, BLUE),
            ("実測\n(4CPU)", 0.40, RED)]
    bw = 78
    xs = [180, 300, 420]
    for (lab, v, col), x in zip(bars, xs):
        top = oy - v * unit
        d.rectangle((x - bw/2, top, x + bw/2, oy), outline=BLACK, width=3, fill=col)
        ctext(d, x, top - 14, f"{v:.2f}", FS, BLACK)
        for k, line in enumerate(lab.split("\n")):
            ctext(d, x, oy + 20 + k * 18, line, FT, BLACK)
    # 効率の注記(理想0.25 ÷ 実測0.40)
    ay = 120
    d.line((300, oy - 0.25*unit - 4, 300, ay), fill=GRAY, width=1)
    d.line((420, oy - 0.40*unit - 4, 420, ay), fill=GRAY, width=1)
    d.line((300, ay, 420, ay), fill=GRAY, width=1)
    ctext(d, 452, 140, "効率 = 理想 / 実測", FS, BLACK, "lm")
    ctext(d, 452, 166, "   = 0.25 / 0.40", FS, BLACK, "lm")
    ctext(d, 452, 194, "   = 62.5 %", F, RED, "lm")
    note(d, "理想は台数分の1(0.25)。実測0.40との比が並列化効率")
    save(im, "comp12ParallelEff")


if __name__ == "__main__":
    info_loss()
    cancellation()
    newline_code()
    cache_hierarchy()
    floating_license()
    parallel_memory()
    parallel_eff()
    print("done")
