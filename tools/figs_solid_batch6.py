# -*- coding: utf-8 -*-
"""Phase2 Batch6: 固体2級 第12章 コンピュータの基礎(computer-basics.json)の
図なし26問へ後付けする図。接頭辞 comp12*(既存 comp12InfoLoss/Cancellation/
NewlineCode/CacheHierarchy/FloatingLicense/ParallelMemory/ParallelEff/Amdahl/
BandMatrix/Complexity/Ieee754/Overflow/SparseCRS/TwosComp と衝突しない新規名)。
白地660x420・黒線画・機構/概念のみ(答え番号・最終数値は焼き込まない)。すべて
helpful(回答後表示)。JSON配線は別途。文字化け回避のためASCII/通常文字のみ使用。"""
import sys, math, os
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---------------- 共通ヘルパ ----------------
def box(d, x0, y0, x1, y1, fill="white", col=BLACK, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def mlines(d, cx, cy, lines, fnt=FT, fill=BLACK, lh=21):
    n = len(lines)
    y0 = cy - (n - 1) * lh / 2
    for i, s in enumerate(lines):
        ctext(d, cx, y0 + i * lh, s, fnt, fill)


def _ctxt(cell):
    return cell if isinstance(cell, str) else cell[0]


def _ccol(cell):
    return BLACK if isinstance(cell, str) else cell[1]


def draw_table(d, x0, y0, cols, rowh, rows, fnt=FT):
    """rows: 各行=セルのリスト。セルは str または (str, color)。1行目=見出し(灰)。"""
    xs = [x0]
    for w in cols:
        xs.append(xs[-1] + w)
    for r, row in enumerate(rows):
        y = y0 + r * rowh
        fill = FILL2 if r == 0 else "white"
        for c in range(len(cols)):
            box(d, xs[c], y, xs[c + 1], y + rowh, fill=fill, wd=2)
            fnt2 = FS if r == 0 else fnt
            ctext(d, (xs[c] + xs[c + 1]) / 2, y + rowh / 2, _ctxt(row[c]), fnt2, _ccol(row[c]))
    return xs


# ============================================================
# comp-12-1 丸め誤差:表せない実数を最も近い表現値へ丸める
# ============================================================
def comp12RoundNearest():
    im, d = new(); title(d, "丸め誤差:表せない実数を最も近い表現値へ丸める")
    ax_y = 210
    x0, x1 = 90, 590
    d.line((x0, ax_y, x1, ax_y), fill=BLACK, width=3)
    # 表現できる値(等間隔の目盛)
    reps = [x0 + i * 100 for i in range(6)]
    for i, xx in enumerate(reps):
        d.line((xx, ax_y - 10, xx, ax_y + 10), fill=BLACK, width=3)
        node(d, xx, ax_y, 5, fill=BLUE, col=BLUE)
    ctext(d, 330, ax_y + 34, "表現できる値(有限桁で刻める点)", FT, BLUE)
    # 真の値(2目盛の間・近いほうへ寄っている)
    a = reps[2]; b = reps[3]
    tv = a + 0.36 * (b - a)
    d.line((tv, ax_y - 46, tv, ax_y + 4), fill=RED, width=3)
    node(d, tv, ax_y - 46, 6, fill=RED, col=RED)
    ctext(d, tv, ax_y - 62, "真の値(例:0.1)", FT, RED)
    # 丸め矢印(近いほうの表現値へ)
    arrow(d, tv, ax_y - 24, a + 6, ax_y - 24, GREEN, 3, 11)
    ctext(d, (tv + a) / 2, ax_y - 40, "近いほうへ丸め", FT, GREEN)
    node(d, a, ax_y - 24, 5, fill=GREEN, col=GREEN)
    ctext(d, 330, 320, "実数を有限桁の2進数で表す時、最も近い表現値に置き換える誤差", FT, BLACK)
    note(d, "CPU速度とは無関係。型の有効桁やアルゴリズムで決まる。桁落ち・打ち切りとは別物。")
    save(im, "comp12RoundNearest")


# ============================================================
# comp-12-2 計算順序で誤差の蓄積が変わる(同じ和でも)
# ============================================================
def comp12SumOrder():
    im, d = new(); title(d, "計算順序で誤差の蓄積が変わる(同じ和でも)")
    d.line((330, 60, 330, 360), fill=LGRAY, width=2)
    # 左:大きい数から
    box(d, 40, 70, 300, 130, FILL1, BLUE)
    ctext(d, 170, 92, "大きい数から順に加算", FS, BLUE)
    ctext(d, 170, 116, "大 + 小 + 小 + ...", FT, BLACK)
    arrow(d, 170, 132, 170, 168, BLACK, 3, 11)
    box(d, 55, 170, 285, 230, "white", GRAY, 2)
    mlines(d, 170, 200, ["小さい項が情報落ち", "して和に反映されない"], FT, RED, 24)
    arrow(d, 170, 232, 170, 268, BLACK, 3, 11)
    box(d, 55, 268, 285, 320, (250, 235, 235), RED, 2)
    ctext(d, 170, 294, "誤差の蓄積:大", FS, RED)
    # 右:小さい数からまとめて
    box(d, 360, 70, 620, 130, FILL1, GREEN)
    ctext(d, 490, 92, "小さい数からまとめて加算", FS, GREEN)
    ctext(d, 490, 116, "小 + 小 + ... + 大", FT, BLACK)
    arrow(d, 490, 132, 490, 168, BLACK, 3, 11)
    box(d, 375, 170, 605, 230, "white", GRAY, 2)
    mlines(d, 490, 200, ["小さい項どうしを先に足し", "情報落ちを抑える"], FT, GREEN, 24)
    arrow(d, 490, 232, 490, 268, BLACK, 3, 11)
    box(d, 375, 268, 605, 320, (232, 245, 235), GREEN, 2)
    ctext(d, 490, 294, "誤差の蓄積:小", FS, GREEN)
    note(d, "同じ答えの式でも、計算順序やアルゴリズムの工夫で誤差の蓄積を減らせる。")
    save(im, "comp12SumOrder")


# ============================================================
# comp-12-3 整数の割り算は小数点以下を切り捨て
# ============================================================
def comp12IntDiv():
    im, d = new(); title(d, "整数の割り算は小数点以下を切り捨て")
    # 実数の場合
    box(d, 55, 90, 605, 175, "white", GRAY, 2)
    ctext(d, 130, 132, "実数で計算", FS, BLUE)
    ctext(d, 300, 132, "1 ÷ 2  =  0.5", F, BLACK)
    ctext(d, 500, 132, "そのまま", FT, GRAY)
    # 整数の場合
    box(d, 55, 200, 605, 320, "white", RED, 2)
    ctext(d, 130, 260, "整数で計算", FS, RED)
    ctext(d, 300, 235, "1 ÷ 2  =  0.5", F, GRAY)
    arrow(d, 300, 258, 300, 288, RED, 3, 11)
    ctext(d, 420, 273, "小数点以下を切り捨て", FT, RED, "lm")
    ctext(d, 300, 300, "= 0  (0.5 ではない)", F, RED)
    note(d, "整数演算では割り算の途中で情報が失われ、実数計算とは異なる結果になる。")
    save(im, "comp12IntDiv")


# ============================================================
# comp-12-7 仮想記憶:主記憶が足りないときHDDの一部を代用
# ============================================================
def comp12VirtualMem():
    im, d = new(); title(d, "仮想記憶:主記憶が不足するとHDDの一部を代用")
    # 主記憶
    box(d, 60, 90, 300, 210, FILL2, BLUE)
    mlines(d, 180, 135, ["主記憶", "(メインメモリ)"], FS, BLACK, 26)
    ctext(d, 180, 185, "高速・容量に限り", FT, BLUE)
    # HDD スワップ領域
    box(d, 360, 90, 600, 250, FILL1, GRAY)
    ctext(d, 480, 112, "ハードディスク", FS, BLACK)
    box(d, 385, 140, 575, 225, (245, 235, 235), RED, 2)
    mlines(d, 480, 182, ["スワップ領域", "(主記憶の代用)"], FT, RED, 24)
    # 出し入れ矢印
    arrow(d, 300, 130, 360, 130, ORANGE, 3, 12); ctext(d, 330, 112, "退避", FT, ORANGE)
    arrow(d, 360, 175, 300, 175, ORANGE, 3, 12); ctext(d, 330, 195, "復帰", FT, ORANGE)
    ctext(d, 330, 300, "使えるメモリ量は増えるが、HDD経由なので主記憶より遅い", FT, BLACK)
    note(d, "キャッシュ(CPU内高速)やSSD(不揮発)とは別物。多発すると性能が下がる。")
    save(im, "comp12VirtualMem")


# ============================================================
# comp-12-8 プロセッサ関連技術の役割
# ============================================================
def comp12ProcTech():
    im, d = new(); title(d, "プロセッサ関連技術のそれぞれの役割")
    rows = [
        ["技術", "役割"],
        ["FPU", "浮動小数点演算を高速に処理"],
        ["GPGPU", "多数の演算器で並列に数値計算"],
        ["DSP", "積和演算に特化(信号処理向け)"],
        ["キャッシュ", ("よく使うデータを高速供給する記憶", BLACK)],
    ]
    draw_table(d, 55, 76, [150, 450], 48, rows)
    box(d, 55, 324, 605, 368, FILL1)
    ctext(d, 330, 346, "キャッシュは記憶技術であり、乗算を速くする専用演算回路ではない", FT, BLACK)
    save(im, "comp12ProcTech")


# ============================================================
# comp-12-9 ビット幅で広がるのは主にアドレス空間
# ============================================================
def comp12AddrSpace():
    im, d = new(); title(d, "ビット幅で広がるのは主にアドレス空間")
    # 32bit
    box(d, 70, 110, 250, 175, FILL2, BLACK)
    ctext(d, 160, 90, "32ビット機", FS, BLACK)
    mlines(d, 160, 142, ["アドレス空間", "約 4 GB"], FT, BLACK, 24)
    arrow(d, 260, 150, 360, 150, BLACK, 4, 15)
    ctext(d, 310, 128, "大幅に拡大", FT, GREEN)
    # 64bit
    box(d, 370, 90, 600, 210, FILL1, BLUE)
    ctext(d, 485, 70, "64ビット機", FS, BLUE)
    mlines(d, 485, 150, ["アドレス空間", "はるかに広い"], FT, BLACK, 26)
    # 精度の注意
    box(d, 60, 250, 600, 356, "white", RED, 2)
    mlines(d, 330, 303,
           ["数値の精度・範囲を決めるのは「型(有効桁)」であり、",
            "ビット幅を64にしても精度が自動で2倍になるわけではない"], FT, RED, 28)
    save(im, "comp12AddrSpace")


# ============================================================
# comp-12-10 高速化技術:演算の高速化か、転送の効率化か
# ============================================================
def comp12SpeedupTech():
    im, d = new(); title(d, "高速化技術:演算そのものを速くするか否か")
    rows = [
        ["技術", "主な効果"],
        ["マルチコア", ("複数処理を同時実行=演算の高速化", GREEN)],
        ["パイプライン", ("命令の疑似並列=処理の高速化", GREEN)],
        ["キャッシュ", ("頻用データの高速供給=高速化", GREEN)],
        ["DMA", ("CPUを介さぬ転送=転送の効率化", RED)],
    ]
    draw_table(d, 45, 76, [150, 470], 48, rows)
    box(d, 45, 324, 615, 368, FILL1)
    ctext(d, 330, 346, "DMAはデータ転送の負担を減らす技術で、演算そのものを速くはしない", FT, BLACK)
    save(im, "comp12SpeedupTech")


# ============================================================
# comp-12-11 CDメディアの種類(ROM/R/RW)
# ============================================================
def comp12CdMedia():
    im, d = new(); title(d, "CDメディアの種類:略号の意味で対応づける")
    rows = [
        ["メディア", "略号の意味", "書き込み"],
        ["CD-ROM", "Read Only Memory", "読み出し専用"],
        ["CD-R", "Recordable", "1回だけ書込(追記)"],
        ["CD-RW", "ReWritable", "繰り返し書換可"],
    ]
    draw_table(d, 45, 100, [160, 240, 220], 62, rows)
    note(d, "R=追記型で消去不可、RW=繰り返し消去・書込ができる。")
    save(im, "comp12CdMedia")


# ============================================================
# comp-12-12 記憶メディアの容量比較
# ============================================================
def comp12MediaCapacity():
    im, d = new(); title(d, "記憶メディアの代表的な容量の比較")
    ox, oy = 90, 330
    axes(d, ox, oy, 500, 250, "", "")
    ctext(d, ox + 4, oy - 244, "容量(対数目盛)", FT, BLACK, "lm")
    data = [("CD-R", 0.7), ("USBメモリ", 4.0), ("DVD-RAM", 4.7), ("Blu-ray", 128.0)]
    lo, hi = 0.7, 128.0
    bw = 74
    xs = [ox + 70, ox + 190, ox + 310, ox + 430]
    for (lab, gb), x in zip(data, xs):
        h = 40 + 210 * (math.log10(gb) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
        top = oy - h
        col = RED if gb == hi else FILL2
        d.rectangle((x - bw / 2, top, x + bw / 2, oy), outline=BLACK, width=3, fill=col)
        gbtxt = ("%gGB" % gb) if gb < 10 else "%dGB" % gb
        ctext(d, x, top - 14, gbtxt, FT, BLACK)
        ctext(d, x, oy + 18, lab, FT, BLACK)
    note(d, "光ディスクは世代が新しいほど大容量(CD<DVD<BD)。BDが桁違いに大きい。")
    save(im, "comp12MediaCapacity")


# ============================================================
# comp-12-14 OSの役割(資源管理+操作環境の提供)
# ============================================================
def comp12OsRole():
    im, d = new(); title(d, "OSは資源を管理し操作環境を提供する基本ソフト")
    # 3層(利用者/アプリ/OS/ハード)
    box(d, 120, 70, 540, 108, "white", GRAY, 2); ctext(d, 330, 89, "利用者", FS, BLACK)
    arrow(d, 330, 108, 330, 128, GRAY, 2, 9)
    box(d, 120, 128, 540, 170, FILL1, BLACK); ctext(d, 330, 149, "業務ソフト(アプリ)", FS, BLACK)
    box(d, 90, 190, 570, 268, FILL2, BLUE)
    ctext(d, 330, 210, "OS(基本ソフト)", FS, BLUE)
    ctext(d, 230, 246, "資源の管理", FT, BLACK); ctext(d, 430, 246, "操作環境(UI)提供", FT, BLACK)
    box(d, 90, 288, 570, 350, "white", BLACK, 2)
    ctext(d, 330, 319, "ハードウェア(CPU / メモリ / ディスク)", FT, BLACK)
    note(d, "OSは土台で、個々の業務ソフトはその上で動く。標準のOSに業務アプリはほぼ含まれない。")
    save(im, "comp12OsRole")


# ============================================================
# comp-12-15 主なOSの成り立ち(開発元と系統)
# ============================================================
def comp12OsOrigins():
    im, d = new(); title(d, "主なOSの成り立ち(開発元と系統)")
    rows = [
        ["OS", "開発元", "系統・特徴"],
        ["Windows", "Microsoft", "ソース非公開の商用OS"],
        ["UNIX", "AT&Tベル研", "商用UNIXの源流"],
        ["Linux", "Torvalds ら", "UNIXクローン(OSS)"],
        ["macOS", "Apple", "Linux由来ではない"],
    ]
    draw_table(d, 45, 78, [160, 200, 260], 54, rows)
    note(d, "Linuxはソース公開のオープンソースOS。各OSの開発元と系統を取り違えない。")
    save(im, "comp12OsOrigins")


# ============================================================
# comp-12-16 OSのライセンス(無償か商用か)
# ============================================================
def comp12OsLicense():
    im, d = new(); title(d, "OSのライセンス:無償・自由配布かどうか")
    rows = [
        ["OS", "ライセンス"],
        ["Windows", ("商用(有償・契約が必要)", BLACK)],
        ["macOS", ("商用(Apple製・専用)", BLACK)],
        ["商用UNIX", ("商用(対価が必要)", BLACK)],
        ["Linux", ("無償・自由に利用/配布(OSS)", GREEN)],
    ]
    draw_table(d, 80, 82, [200, 340], 52, rows)
    note(d, "Linuxはオープンソース(GPL)で無償・自由に使える。多数のディストリビューションがある。")
    save(im, "comp12OsLicense")


# ============================================================
# comp-12-17 OSバージョンアップの手順
# ============================================================
def comp12OsUpgrade():
    im, d = new(); title(d, "OSバージョンアップの安全な手順")
    steps = [
        ["新OSと業務ソフトの", "バージョン互換性を確認"],
        ["検証(テスト)環境で", "動作を確認"],
        ["問題なければ", "本番環境を更新"],
    ]
    x0, x1 = 130, 530; y = 80; bh = 62; gap = 26
    fills = [FILL1, FILL1, FILL2]
    for i, lines in enumerate(steps):
        box(d, x0, y, x1, y + bh, fills[i], BLACK)
        mlines(d, (x0 + x1) / 2, y + bh / 2, lines, FT, BLACK, 22)
        if i < len(steps) - 1:
            arrow(d, (x0 + x1) / 2, y + bh, (x0 + x1) / 2, y + bh + gap, BLACK, 3, 12)
        y += bh + gap
    box(d, 60, 328, 600, 372, "white", RED, 2)
    ctext(d, 330, 350, "本番から先に更新するのは危険。互換性未確認のまま省略しない。", FT, RED)
    note(d, "更新でソフトが動かなくなる例があるため「確認→検証→本番」の順で進める。", y=393)
    save(im, "comp12OsUpgrade")


# ============================================================
# comp-12-18 CAE導入時のOS選定の観点
# ============================================================
def comp12OsSelect():
    im, d = new(); title(d, "CAE導入時のコンピュータ・OS選定の観点")
    rows = [
        ["観点", "妥当か"],
        ["CAEソフトが動作保証するOSか", ("妥当", GREEN)],
        ["既存システム・網との連携のしやすさ", ("妥当", GREEN)],
        ["解析規模に見合う性能・メモリ容量", ("妥当", GREEN)],
        ["普及しているという理由だけで決める", ("不十分", RED)],
    ]
    xs = draw_table(d, 45, 80, [420, 200], 52, rows)
    # マーク
    for r in range(1, 5):
        y = 80 + r * 52 + 26
        col = GREEN if r < 4 else RED
        mk = "O" if r < 4 else "X"
        ctext(d, xs[1] + 22, y, mk, FS, col, "lm")
    note(d, "対応OS・連携・性能を総合判断する。普及度は一要素にすぎず単独の決め手にしない。")
    save(im, "comp12OsSelect")


# ============================================================
# comp-12-19 コンパイラ型とインタプリタ型
# ============================================================
def comp12CompInterp():
    im, d = new(); title(d, "コンパイラ型とインタプリタ型の違い")
    d.line((330, 58, 330, 360), fill=LGRAY, width=2)
    # コンパイラ型
    ctext(d, 170, 76, "コンパイラ型", FS, BLUE)
    box(d, 55, 96, 285, 138, FILL1); ctext(d, 170, 117, "ソース全体", FT, BLACK)
    arrow(d, 170, 138, 170, 168, BLACK, 3, 11); ctext(d, 245, 153, "事前に一括変換", FT, GRAY, "lm")
    box(d, 55, 168, 285, 210, FILL2); ctext(d, 170, 189, "機械語(実行形式)", FT, BLACK)
    arrow(d, 170, 210, 170, 240, BLACK, 3, 11)
    box(d, 55, 240, 285, 288, (232, 245, 235), GREEN); ctext(d, 170, 264, "実行(速い)", FS, GREEN)
    # インタプリタ型
    ctext(d, 490, 76, "インタプリタ型", FS, RED)
    box(d, 375, 96, 605, 138, FILL1); ctext(d, 490, 117, "ソース", FT, BLACK)
    for k, yy in enumerate((160, 200, 240)):
        arrow(d, 490, yy - 18, 490, yy, BLACK, 2, 9)
        box(d, 400, yy, 580, yy + 26, "white", GRAY, 2)
        ctext(d, 490, yy + 13, "1行ずつ翻訳しながら実行", FT, BLACK)
    ctext(d, 490, 300, "実行時に翻訳=一般に低速", FS, RED)
    note(d, "代表例:コンパイラ型=C/FORTRAN、インタプリタ型=BASIC等。速度差は現に生じる。")
    save(im, "comp12CompInterp")


# ============================================================
# comp-12-20 コンパイル結果はプラットフォーム依存
# ============================================================
def comp12PlatformDep():
    im, d = new(); title(d, "コンパイル結果は特定のCPU/OS向けに依存")
    box(d, 240, 66, 420, 112, FILL1, BLACK)
    mlines(d, 330, 89, ["実行形式(機械語)", "CPU/OS A 向けに変換"], FT, BLACK, 22)
    arrow(d, 290, 112, 180, 158, BLACK, 3, 12)
    arrow(d, 370, 112, 480, 158, BLACK, 3, 12)
    # A 環境:動く
    box(d, 70, 158, 290, 300, "white", GREEN, 2)
    ctext(d, 180, 180, "同じ CPU/OS A", FS, BLACK)
    box(d, 110, 210, 250, 260, (232, 245, 235), GREEN)
    ctext(d, 180, 235, "そのまま動く", FT, GREEN)
    ctext(d, 180, 285, "O", FL, GREEN)
    # B 環境:動かない
    box(d, 370, 158, 590, 300, "white", RED, 2)
    ctext(d, 480, 180, "異なる CPU/OS B", FS, BLACK)
    box(d, 410, 210, 550, 260, (250, 235, 235), RED)
    ctext(d, 480, 235, "そのまま動かない", FT, RED)
    ctext(d, 480, 285, "X", FL, RED)
    note(d, "別環境で動かすには再コンパイルが必要なことが多い(中間コードJVM等とは別)。")
    save(im, "comp12PlatformDep")


# ============================================================
# comp-12-21 主な言語の特徴と用途
# ============================================================
def comp12LangFeatures():
    im, d = new(); title(d, "主なプログラミング言語の特徴と用途")
    rows = [
        ["言語", "得意分野・特徴"],
        ["FORTRAN", "科学技術計算(数値ライブラリ豊富)"],
        ["COBOL", "事務処理"],
        ["Java", "オブジェクト指向・JVM上で動作"],
        ["C言語", "システム記述など汎用"],
    ]
    draw_table(d, 55, 82, [160, 440], 52, rows)
    note(d, "言語ごとの用途と特徴を取り違えない。FORTRANは科学技術計算で多用される。")
    save(im, "comp12LangFeatures")


# ============================================================
# comp-12-22 プログラミング言語の起源(年代)
# ============================================================
def comp12LangHistory():
    im, d = new(); title(d, "プログラミング言語の起源(年代)")
    ox = 90
    d.line((ox, 150, 600, 150), fill=BLACK, width=3)
    arrow(d, 590, 150, 620, 150, BLACK, 3, 12)
    ctext(d, 618, 176, "年代", FT, BLACK)
    # FORTRAN 1950s
    x1 = 200
    d.line((x1, 140, x1, 160), fill=BLACK, width=3); node(d, x1, 150, 6, fill=BLUE, col=BLUE)
    ctext(d, x1, 128, "1950年代", FT, BLUE)
    box(d, x1 - 130, 185, x1 + 130, 255, FILL1, BLUE)
    mlines(d, x1, 220, ["FORTRAN (IBM)", "世界初期の高級言語", "科学技術計算用"], FT, BLACK, 20)
    # C 1970s
    x2 = 470
    d.line((x2, 140, x2, 160), fill=BLACK, width=3); node(d, x2, 150, 6, fill=GREEN, col=GREEN)
    ctext(d, x2, 128, "1970年代", FT, GREEN)
    box(d, x2 - 130, 185, x2 + 130, 255, FILL1, GREEN)
    mlines(d, x2, 220, ["C言語 (ベル研)", "UNIXの大部分を記述", "その後広く普及"], FT, BLACK, 20)
    note(d, "起源(いつ・誰が・何のため)を押さえる。FORTRANは高級言語でアセンブリではない。")
    save(im, "comp12LangHistory")


# ============================================================
# comp-12-23 高水準言語と低水準言語
# ============================================================
def comp12LangLevel():
    im, d = new(); title(d, "高水準言語と低水準言語(人間寄りか機械寄りか)")
    # 帯
    d.line((90, 210, 600, 210), fill=BLACK, width=3)
    arrow(d, 90, 210, 60, 210, BLUE, 3, 12)
    arrow(d, 600, 210, 630, 210, RED, 3, 12)
    ctext(d, 175, 128, "人間に近い(高水準)", FS, BLUE)
    ctext(d, 500, 128, "機械に近い(低水準)", FS, RED)
    # 高水準の例
    for i, s in enumerate(["C++", "Java", "Perl"]):
        x = 130 + i * 90
        node(d, x, 210, 6, fill=BLUE, col=BLUE)
        box(d, x - 40, 160, x + 40, 192, FILL1, BLUE)
        ctext(d, x, 176, s, FT, BLACK)
    # 低水準の例
    x = 510
    node(d, x, 210, 6, fill=RED, col=RED)
    box(d, x - 90, 160, x + 90, 192, (250, 235, 235), RED)
    ctext(d, x, 176, "アセンブリ言語", FT, BLACK)
    ctext(d, 330, 270, "アセンブリはCPUの命令に1対1で近く機械依存が高い", FT, BLACK)
    note(d, "高水準言語は人間に理解しやすく機械独立性が高い。低水準は機械語やその記号化。")
    save(im, "comp12LangLevel")


# ============================================================
# comp-12-24 フローティング:導入台数と同時起動数は別
# ============================================================
def comp12FloatingSeats():
    im, d = new(); title(d, "フローティング:導入台数と同時起動数は別")
    # サーバ
    box(d, 245, 66, 415, 118, FILL2, BLACK)
    mlines(d, 330, 92, ["ライセンスサーバ", "契約=3本(同時起動数)"], FT, BLACK, 22)
    bus = 160
    d.line((70, bus, 590, bus), fill=BLACK, width=3)
    d.line((330, 118, 330, bus), fill=BLACK, width=3)
    # 5台導入(3台使用中+2台待ち)
    states = [("使用中", GREEN), ("使用中", GREEN), ("使用中", GREEN), ("待ち", RED), ("待ち", RED)]
    xs = [90, 210, 330, 450, 570]
    for x, (st, col) in zip(xs, states):
        d.line((x, bus, x, 210), fill=BLACK, width=2)
        box(d, x - 42, 210, x + 42, 262, "white", BLACK, 2)
        ctext(d, x, 236, "PC", F, BLACK)
        ctext(d, x, 282, st, FT, col)
    ctext(d, 330, 316, "導入は5台でも、同時起動は契約3本までに制限される", FT, BLACK)
    note(d, "導入台数は契約数を超えてよい。制限されるのは同時起動数(ノードロックとは別)。")
    save(im, "comp12FloatingSeats")


# ============================================================
# comp-12-26 LAN と WAN(規模の違い)
# ============================================================
def comp12LanWan():
    im, d = new(); title(d, "LAN と WAN:結ぶ範囲の違い")
    d.line((330, 58, 330, 360), fill=LGRAY, width=2)
    # LAN
    ctext(d, 170, 78, "LAN(構内網)", FS, BLUE)
    box(d, 60, 100, 285, 300, "white", BLUE, 2)
    ctext(d, 170, 122, "同じ建物・近接区域", FT, BLACK)
    for x in (110, 170, 230):
        box(d, x - 26, 180, x + 26, 225, FILL1, BLACK); ctext(d, x, 202, "PC", FT, BLACK)
        d.line((x, 180, x, 160), fill=BLACK, width=2)
    d.line((110, 160, 230, 160), fill=BLACK, width=3)
    ctext(d, 170, 262, "Local = 近接", FT, BLUE)
    # WAN
    ctext(d, 490, 78, "WAN(広域網)", FS, RED)
    box(d, 375, 100, 605, 300, "white", RED, 2)
    ctext(d, 490, 122, "通信事業者の回線で広域を結ぶ", FT, BLACK)
    for cx in (420, 560):
        d.ellipse((cx - 26, 175, cx + 26, 210), outline=BLACK, width=2)
        ctext(d, cx, 192, "拠点", FT, BLACK)
    d.line((446, 192, 534, 192), fill=BLACK, width=2)
    ctext(d, 490, 165, "遠隔地(都市間など)", FT, GRAY)
    ctext(d, 490, 262, "Wide = 広域", FT, RED)
    note(d, "LAN=Local Area Network(構内)、WAN=Wide Area Network(広域)。規模で区別する。")
    save(im, "comp12LanWan")


# ============================================================
# comp-12-27 暗号化なしなら物理搬送が相対的に安全
# ============================================================
def comp12SecureTransfer():
    im, d = new(); title(d, "暗号化しないなら通信経路を通さぬほうが安全")
    # ネットワーク経由(リスク)
    box(d, 45, 80, 320, 300, "white", RED, 2)
    ctext(d, 182, 100, "ネットワーク経由", FS, RED)
    box(d, 62, 135, 132, 175, FILL1, BLACK); ctext(d, 97, 155, "送信", FT, BLACK)
    box(d, 232, 135, 302, 175, FILL1, BLACK); ctext(d, 267, 155, "相手", FT, BLACK)
    d.line((132, 155, 232, 155), fill=BLACK, width=3)
    # 盗み見(第三者)
    ctext(d, 182, 205, "経路上の管理者・第三者", FT, RED)
    d.line((182, 175, 182, 220), fill=RED, width=2)
    ctext(d, 182, 240, "盗み見・改ざんの恐れ", FT, RED)
    ctext(d, 182, 275, "X", FL, RED)
    # 物理搬送(安全)
    box(d, 340, 80, 615, 300, "white", GREEN, 2)
    ctext(d, 477, 100, "記録メディアを郵送", FS, GREEN)
    d.ellipse((400, 150, 470, 185), outline=BLACK, width=3); ctext(d, 435, 167, "CD-R", FT, BLACK)
    arrow(d, 470, 167, 545, 167, BLACK, 3, 12); ctext(d, 507, 149, "郵送", FT, GRAY)
    box(d, 548, 148, 600, 188, FILL1, BLACK); ctext(d, 574, 168, "相手", FT, BLACK)
    ctext(d, 477, 220, "通信経路を使わない", FT, GREEN)
    ctext(d, 477, 275, "O", FL, GREEN)
    note(d, "この設問は「暗号化なし」前提での相対的な安全性。物理搬送は経路上の漏えいを避けやすい。")
    save(im, "comp12SecureTransfer")


# ============================================================
# comp-12-28 ネットワーク関連規格の用途(NFS ほか)
# ============================================================
def comp12NfsShare():
    im, d = new(); title(d, "ネットワーク関連規格の用途で区別する")
    rows = [
        ["規格", "用途"],
        ["NFS", ("複数機でファイルを相互共有・利用", GREEN)],
        ["NIS", "ユーザー名/ホスト名の分散管理"],
        ["RAID", "複数ディスクで高速・大容量・高信頼"],
        ["FTP", "ファイル転送(常時共有ではない)"],
    ]
    draw_table(d, 55, 82, [130, 470], 52, rows)
    note(d, "「共有・相互利用の規格」はNFS。ほかは対象(管理・ディスク・転送)が異なる。")
    save(im, "comp12NfsShare")


# ============================================================
# comp-12-29 ファイル転送とメールのプロトコル
# ============================================================
def comp12FtpProtocol():
    im, d = new(); title(d, "プロトコルの用途:ファイル転送とメール")
    rows = [
        ["プロトコル", "用途"],
        ["FTP", ("ファイル転送", GREEN)],
        ["SMTP", "メール送信"],
        ["POP3", "メール受信"],
        ["IMAP4", "メール受信"],
    ]
    draw_table(d, 90, 82, [200, 320], 52, rows)
    note(d, "ファイル転送=FTP、メール送受信=SMTP/POP3/IMAP4 と分けて覚える。")
    save(im, "comp12FtpProtocol")


# ============================================================
# comp-12-32 リバースエンジニアリング(実装から仕様へ)
# ============================================================
def comp12ReverseEng():
    im, d = new(); title(d, "リバースエンジニアリング:実装から設計仕様を抽出")
    # 順方向
    box(d, 40, 90, 620, 150, "white", GRAY, 2)
    ctext(d, 100, 120, "順方向の開発", FS, BLACK)
    for i, s in enumerate(["設計仕様", "設計", "実装(完成物)"]):
        x = 250 + i * 130
        box(d, x - 55, 100, x + 55, 140, FILL1, BLACK); ctext(d, x, 120, s, FT, BLACK)
        if i < 2:
            arrow(d, x + 55, 120, x + 75, 120, GRAY, 3, 10)
    # リバース
    box(d, 40, 200, 620, 300, "white", BLUE, 2)
    ctext(d, 100, 250, "リバース", FS, BLUE)
    box(d, 195, 230, 305, 270, FILL2, BLACK); ctext(d, 250, 250, "実装(完成物)", FT, BLACK)
    arrow(d, 305, 250, 375, 250, BLUE, 4, 14); ctext(d, 340, 232, "解析", FT, BLUE)
    box(d, 375, 230, 505, 270, (225, 235, 250), BLUE); mlines(d, 440, 250, ["設計仕様を抽出"], FT, BLACK, 20)
    arrow(d, 505, 250, 545, 250, GRAY, 3, 11)
    ctext(d, 575, 250, "修正・再開発へ", FT, GRAY)
    note(d, "完成物を解析して構造・仕様を明らかにし、修正や再開発に役立てる(新規開発や保護とは別)。")
    save(im, "comp12ReverseEng")


# ============================================================
# comp-12-33 情報セキュリティポリシーの階層
# ============================================================
def comp12SecPolicy():
    im, d = new(); title(d, "情報セキュリティポリシーの位置づけ(階層)")
    cx = 330
    tiers = [
        ("基本方針", "何を・なぜ守るか=組織全体の拠り所", 130, FILL2, BLUE),
        ("対策基準", "守るための基準・ルール", 220, FILL1, BLACK),
        ("実施手順", "担当者向けの具体的な操作手順", 300, "white", GRAY),
    ]
    yt = 80; h = 78
    for i, (name, desc, w, fill, col) in enumerate(tiers):
        y0 = yt + i * (h + 6)
        d.polygon([(cx - w / 2, y0), (cx + w / 2, y0),
                   (cx + (w + 90) / 2, y0 + h), (cx - (w + 90) / 2, y0 + h)],
                  outline=BLACK, width=3, fill=fill)
        ctext(d, cx, y0 + 26, name, FS, col)
        ctext(d, cx, y0 + 54, desc, FT, BLACK)
    arrow(d, 55, 340, 55, 90, BLUE, 3, 12); ctext(d, 50, 200, "上位=方針", FT, BLUE, "rm")
    note(d, "ポリシー=基本方針と対策基準。具体的な実施手順はその後に別途作る(手順書そのものではない)。")
    save(im, "comp12SecPolicy")


ALL = [comp12RoundNearest, comp12SumOrder, comp12IntDiv, comp12VirtualMem, comp12ProcTech,
       comp12AddrSpace, comp12SpeedupTech, comp12CdMedia, comp12MediaCapacity, comp12OsRole,
       comp12OsOrigins, comp12OsLicense, comp12OsUpgrade, comp12OsSelect, comp12CompInterp,
       comp12PlatformDep, comp12LangFeatures, comp12LangHistory, comp12LangLevel,
       comp12FloatingSeats, comp12LanWan, comp12SecureTransfer, comp12NfsShare,
       comp12FtpProtocol, comp12ReverseEng, comp12SecPolicy]

KEYS = ["comp12RoundNearest", "comp12SumOrder", "comp12IntDiv", "comp12VirtualMem", "comp12ProcTech",
        "comp12AddrSpace", "comp12SpeedupTech", "comp12CdMedia", "comp12MediaCapacity", "comp12OsRole",
        "comp12OsOrigins", "comp12OsLicense", "comp12OsUpgrade", "comp12OsSelect", "comp12CompInterp",
        "comp12PlatformDep", "comp12LangFeatures", "comp12LangHistory", "comp12LangLevel",
        "comp12FloatingSeats", "comp12LanWan", "comp12SecureTransfer", "comp12NfsShare",
        "comp12FtpProtocol", "comp12ReverseEng", "comp12SecPolicy"]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    miss = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(KEYS), "MISSING", miss)
