# -*- coding: utf-8 -*-
"""振動2級 第12章 コンピュータの基礎 の問題図（再生成用・恒久ツール）。
元の生成スクリプトが失われていたため復元。figlib準拠・白地660x420。
 v2e12round … 12-16 数値誤差の種類（丸め誤差/桁落ち/オーバーフロー）の一覧表。定義は正しい。
 v2e12err   … 12-1 桁落ち（近い2数の減算で有効桁が激減）。設問「2〜3桁まで減る」に合わせ 6桁→2桁の例。
 v2e12bin   … 12-8 10進→2進。50=110010 を桁行に確定表示（32,16,2 を使用）。
実行: python tools/figs_vib2ch12_e.py
"""
from figlib import new, save, title, ctext, W, H, F, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN, FILL1, FILL2


def round_table(name):
    im, d = new()
    title(d, "数値誤差の種類の違い")
    x0, xm, x1 = 60, 240, 600
    top, rh = 96, 60
    rows = [("用語", "何が起きるか", True),
            ("丸め誤差", "有効桁数を超え正確に表せずずれる", False),
            ("桁落ち", "近い値の加減算で上位桁が失われる", False),
            ("オーバーフロー", "扱える最大値を超えてしまう", False)]
    for r, (a, b, hd) in enumerate(rows):
        y = top + r * rh
        fill = FILL2 if hd else "white"
        d.rectangle([x0, y, xm, y + rh], outline=BLACK, width=2, fill=fill)
        d.rectangle([xm, y, x1, y + rh], outline=BLACK, width=2, fill=fill)
        ctext(d, (x0 + xm) / 2, y + rh / 2, a, FS, BLACK)
        ctext(d, (xm + x1) / 2, y + rh / 2, b, FS, BLACK)
    ctext(d, W / 2, H - 24, "精度は変数の型やアルゴリズムに依存（CPU速度ではない）", FT, GRAY)
    save(im, name)


def cancellation_err(name):
    im, d = new()
    title(d, "桁落ち：近い2数の減算で有効桁が激減")
    # A=0.012345, B=0.012321, A-B=0.000024  （上位 0.0123 が相殺 → 有効6桁→2桁）
    A = list("0.012345"); B = list("0.012321"); D = list("0.000024")
    x0, dx = 150, 46
    yA, yB, yD = 150, 205, 262
    ctext(d, 105, yA, "A", F, BLUE)
    ctext(d, 105, yB, "B", F, GREEN); ctext(d, 128, yB, "−", F, GREEN)
    for i, c in enumerate(A):
        ctext(d, x0 + i * dx, yA, c, F, BLUE)
    for i, c in enumerate(B):
        ctext(d, x0 + i * dx, yB, c, F, GREEN)
    # 減算線
    d.line([(95, yB + 22), (x0 + len(A) * dx - 20, yB + 22)], fill=BLACK, width=2)
    for i, c in enumerate(D):
        col = RED if i >= 6 else GRAY   # 残る有効桁(下2桁)を赤
        ctext(d, x0 + i * dx, yD, c, F, col)
    # 相殺する上位桁を枠で囲う（インデックス2〜5 = "0123"）
    bx0 = x0 + 2 * dx - 22; bx1 = x0 + 5 * dx + 22
    d.rectangle([bx0, yA - 26, bx1, yB + 26], outline=GRAY, width=2)
    ctext(d, W / 2, yD + 44, "上位の等しい桁どうしが相殺 → 有効桁 6桁→2桁", FT, RED)
    ctext(d, W / 2, H - 24, "加減算で近い値どうしのとき顕著（乗除算では起きない）", FT, GRAY)
    save(im, name)


def dec_to_bin(name):
    im, d = new()
    title(d, "10進→2進：桁の重み（位取り）で表す  50 = 110010₂")
    weights = ["32", "16", "8", "4", "2", "1"]
    bits = ["1", "1", "0", "0", "1", "0"]           # 50 = 32+16+2
    used = [True, True, False, False, True, False]
    x0, cw = 118, 76
    yw, yb = 132, 196
    rh = 56
    ctext(d, 78, yw + rh / 2, "重み", FS, GRAY, "rm")
    ctext(d, 78, yb + rh / 2, "桁", FS, GRAY, "rm")
    for i in range(6):
        x = x0 + i * cw
        d.rectangle([x, yw, x + cw, yw + rh], outline=BLACK, width=2, fill=FILL2)
        ctext(d, x + cw / 2, yw + rh / 2, weights[i], FS, BLACK)
        bf = (250, 232, 232) if used[i] else "white"
        d.rectangle([x, yb, x + cw, yb + rh], outline=BLACK, width=2, fill=bf)
        ctext(d, x + cw / 2, yb + rh / 2, bits[i], F, RED if used[i] else GRAY)
    ctext(d, W / 2, 300, "大きい重みから引き、使った重み（32・16・2）の桁を1にする", FT, GRAY)
    ctext(d, W / 2, H - 24, "重み=2のべき乗（下位から 1,2,4,8,16,32,…）", FT, GRAY)
    save(im, name)


if __name__ == "__main__":
    round_table("v2e12round")
    cancellation_err("v2e12err")
    dec_to_bin("v2e12bin")
    print("done")
