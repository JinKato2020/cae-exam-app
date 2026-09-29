# -*- coding: utf-8 -*-
"""振動2級 第9章 数値解析法 の図の充実（恒久ツール）。元の生成スクリプトが失われていたため復元＋充実。
 v2e9ComplianceCurve       … 9-17 回答後。低次側 残留質量 −1/(Y_ik ω²)・高次側 残留剛性 1/Z_ik の近似項を明示。
 v2e9MatrixFormAns         … 9-1  回答後。具体係数の連立1次方程式→行列形式(行=式/列=変数)。回答前は空欄版 v2e9MatrixForm。
 v2e9LUDecompAns           … 9-4  回答後。2×2の具体的なLU消去(ピボット・乗数)。回答前は v2e9LUDecomp。
 v2e9FirstOrderFormAns     … 9-16 回答後。1階化 z˙=[A]z+[B]f のブロックを具体化([A]=[[0,I],[-M⁻¹K,-M⁻¹C]] 等)。回答前は v2e9FirstOrderForm。
実行: python tools/figs_vib2ch9_e.py
"""
import math
from figlib import new, save, title, ctext, plot, W, H, FL, F, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN, FILL1, FILL2, FILL3


def bracket(d, x0, y0, x1, y1, col=BLACK, wd=3, ear=10):
    d.line([(x0 + ear, y0), (x0, y0), (x0, y1), (x0 + ear, y1)], fill=col, width=wd)
    d.line([(x1 - ear, y0), (x1, y0), (x1, y1), (x1 - ear, y1)], fill=col, width=wd)


def compliance_curve(name):
    im, d = new()
    title(d, "コンプライアンス-周波数曲線と残留項の近似")
    ox, oy = 90, 322
    w, h = 500, 250
    # 軸
    d.line([(ox, oy), (ox, oy - h)], fill=BLACK, width=2)
    d.line([(ox, oy), (ox + w, oy)], fill=BLACK, width=2)
    ctext(d, ox - 10, oy - h + 6, "コンプライアンス", FT, BLACK, "rm")
    ctext(d, ox + w + 4, oy, "周波数", FT, BLACK, "lm")
    # 対象帯域の網掛け
    xa, xb = ox + 205, ox + 350
    d.rectangle([xa, oy - h + 20, xb, oy], fill=(235, 240, 250), outline=None)
    ctext(d, (xa + xb) / 2, oy - h + 34, "対象帯域", FT, BLUE)
    ctext(d, xa, oy + 16, "ωa", FT, BLUE); ctext(d, xb, oy + 16, "ωb", FT, BLUE)
    # 3つの共振ピーク
    peaks = [(ox + 130, 78, 24), (ox + 278, 120, 34), (ox + 430, 62, 24)]
    pts = []
    for i in range(0, w - 10, 3):
        x = ox + 15 + i
        y = oy - 26
        for xp, hh, ww in peaks:
            y -= hh / (1 + ((x - xp) / ww) ** 2)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 110, oy + 34, "低次モード領域", FT, GRAY)
    ctext(d, ox + 430, oy + 34, "高次モード領域", FT, GRAY)
    # 残留項の近似（充実点）
    d.line([(ox + 60, oy - 210), (ox + 120, oy - 150)], fill=GREEN, width=1)
    ctext(d, ox + 60, oy - 224, "低次側の残留（残留質量）", FT, GREEN)
    ctext(d, ox + 60, oy - 206, "≈ −1/(Y_ik ω²)", FS, GREEN)
    ctext(d, ox + 430, oy - 224, "高次側の残留（残留剛性）", FT, RED)
    ctext(d, ox + 430, oy - 206, "≈ 1/Z_ik", FS, RED)
    save(im, name)


def matrix_form_ans(name):
    im, d = new()
    title(d, "連立1次方程式 → 行列形式（具体例）")
    eqs = ["2x₁ + 1x₂ + 0x₃ = 5",
           "1x₁ + 3x₂ + 1x₃ = 10",
           "0x₁ + 1x₂ + 2x₃ = 8"]
    for i, e in enumerate(eqs):
        ctext(d, 40, 120 + i * 46, "式" + "₁₂₃"[i], FT, GRAY, "lm")
        ctext(d, 90, 120 + i * 46, e, FS, BLACK, "lm")
    A = [[2, 1, 0], [1, 3, 1], [0, 1, 2]]
    b = [5, 10, 8]
    ox, oy, c = 350, 96, 50
    bracket(d, ox - 8, oy, ox + 3 * c + 8, oy + 3 * c)
    for r in range(3):
        for cc in range(3):
            ctext(d, ox + cc * c + c / 2, oy + r * c + c / 2, str(A[r][cc]), FS, BLACK)
    ctext(d, ox + 1.5 * c, oy + 3 * c + 22, "[A] 行=式 / 列=変数", FT, GRAY)
    # {x}
    xo = ox + 3 * c + 26
    bracket(d, xo, oy, xo + 46, oy + 3 * c)
    for r in range(3):
        ctext(d, xo + 23, oy + r * c + c / 2, "x" + "₁₂₃"[r], FS, BLUE)
    ctext(d, xo + 60, oy + 1.5 * c, "=", F, BLACK)
    # {b}
    bo = xo + 84
    bracket(d, bo, oy, bo + 46, oy + 3 * c)
    for r in range(3):
        ctext(d, bo + 23, oy + r * c + c / 2, str(b[r]), FS, RED)
    ctext(d, W / 2, H - 22, "係数・右辺・解の対応が確定（回答後）", FT, GRAY)
    save(im, name)


def lu_decomp_ans(name):
    im, d = new()
    title(d, "LU分解の消去（具体例）  A = L U")
    ctext(d, W / 2, 78, "A = [[2, 1], [4, 3]]", FS, BLACK)
    # 消去ステップ
    ctext(d, W / 2, 126, "消去: 乗数 m₂₁ = 4 / 2 = 2 → 行2 − 2×行1", FT, GREEN)
    # L, U
    oy, c = 170, 56
    ox = 120
    ctext(d, ox - 20, oy + c, "L =", FS, BLACK, "rm")
    bracket(d, ox, oy, ox + 2 * c, oy + 2 * c)
    Lm = [["1", "0"], ["2", "1"]]
    for r in range(2):
        for cc in range(2):
            ctext(d, ox + cc * c + c / 2, oy + r * c + c / 2, Lm[r][cc], FS, BLUE)
    ctext(d, ox + c, oy + 2 * c + 20, "下三角(対角=1・乗数)", FT, GRAY)
    ox2 = 400
    ctext(d, ox2 - 20, oy + c, "U =", FS, BLACK, "rm")
    bracket(d, ox2, oy, ox2 + 2 * c, oy + 2 * c)
    Um = [["2", "1"], ["0", "1"]]
    for r in range(2):
        for cc in range(2):
            ctext(d, ox2 + cc * c + c / 2, oy + r * c + c / 2, Um[r][cc], FS, RED)
    ctext(d, ox2 + c, oy + 2 * c + 20, "上三角(消去後のピボット)", FT, GRAY)
    ctext(d, W / 2, H - 22, "ピボット2で行2を消去 → L の乗数と U が確定", FT, GRAY)
    save(im, name)


def first_order_form_ans(name):
    im, d = new()
    title(d, "2階形の1階化  z˙ = [A] z + [B] f（ブロック確定）")
    ctext(d, W / 2, 84, "M x¨ + C x˙ + K x = f ,  z = {x ; x˙}", FS, BLACK)
    oy, cw, ch = 150, 130, 46
    ox = 150
    ctext(d, ox - 24, oy + ch, "[A] =", FS, BLACK, "rm")
    bracket(d, ox, oy, ox + 2 * cw, oy + 2 * ch)
    Ablk = [["0", "I"], ["−M⁻¹K", "−M⁻¹C"]]
    for r in range(2):
        for cc in range(2):
            ctext(d, ox + cc * cw + cw / 2, oy + r * ch + ch / 2, Ablk[r][cc], FS, BLUE)
    # [B]
    ox2 = ox + 2 * cw + 70
    ctext(d, ox2 - 24, oy + ch, "[B] =", FS, BLACK, "rm")
    bracket(d, ox2, oy, ox2 + cw, oy + 2 * ch)
    Bblk = ["0", "M⁻¹"]
    for r in range(2):
        ctext(d, ox2 + cw / 2, oy + r * ch + ch / 2, Bblk[r], FS, RED)
    ctext(d, W / 2, oy + 2 * ch + 46, "次数 n の2階系 → 次数 2n の1階系（z˙ = A z + B f）", FT, GRAY)
    ctext(d, W / 2, H - 22, "各ブロックに 0・I・−M⁻¹K・−M⁻¹C・M⁻¹ を代入して確定", FT, GRAY)
    save(im, name)


if __name__ == "__main__":
    compliance_curve("v2e9ComplianceCurve")
    matrix_form_ans("v2e9MatrixFormAns")
    lu_decomp_ans("v2e9LUDecompAns")
    first_order_form_ans("v2e9FirstOrderFormAns")
    print("done")
