# -*- coding: utf-8 -*-
"""固体2級 第10章(プリポスト処理の基礎)の「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(部品形状/荷重/要素形状)のみ。
答え(応力集中箇所・細分の位置・対称モデルの取り方と対称拘束・要素品質の判定基準)は
一切描かない(=required相当)。概念・手順のみの問題には追加しない(選別して少数のみ)。
既存 figureImage(答え示唆あり)は回答後(helpful)のまま。JSON配線は別途。
[[cae-figure-before-after-rule]] 第10章横展開。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_bc9 import small_pin, small_roller


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg))
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg,
                    x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


def grid(d, x0, y0, x1, y1, nx, ny, col=LGRAY):
    """一様メッシュ(与件・粗密なし)。答えである粗密は描かない。"""
    for i in range(1, nx):
        x = x0 + (x1 - x0) * i / nx; d.line((x, y0, x, y1), fill=col, width=1)
    for j in range(1, ny):
        y = y0 + (y1 - y0) * j / ny; d.line((x0, y, x1, y), fill=col, width=1)


# ---- 10-7 丸穴あき薄板の左右引張(細分する集中部と要素種類を問う) ----
def f_hole_plate_tension():
    im, d = new(); title(d, "丸穴あき薄板の左右引張(細分する集中部と要素種類を問う)")
    x0, yt, x1, yb = 170, 130, 500, 300
    cx, cy, r = 335, 215, 40
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    grid(d, x0, yt, x1, yb, 9, 4)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white", outline=BLACK, width=3)
    force(d, x0, cy, -54, 0, "P"); force(d, x1, cy, 54, 0, "P")
    ctext(d, cx, yb + 22, "中央に丸穴・一様メッシュ", FT, GRAY)
    note(d, "左右に引張。細かくすべき応力集中箇所と用いる要素は?(答えは未記入)")
    save(im, "pp10HolePlateTensionSetup")


# ---- 10-8 丸穴あき片持ちはり(要素分割の方針を問う) ----
def f_hole_cantilever():
    im, d = new(); title(d, "丸穴あき片持ちはり(要素分割の方針を問う)")
    x0, yt, x1, yb = 150, 150, 520, 290
    cx, cy, r = 320, 220, 30
    wall(d, x0, yt - 4, yb + 4, side=-1); ctext(d, x0 - 26, (yt + yb) / 2, "固定", FT, GRAY, "rm")
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    grid(d, x0, yt, x1, yb, 10, 4)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white", outline=BLACK, width=3)
    force(d, x1 - 6, yt - 2, 0, 50, "F")
    ctext(d, (x0 + x1) / 2, yb + 22, "丸穴あり・一様メッシュ", FT, GRAY)
    note(d, "先端に曲げ荷重F。要素分割の方針は?(メッシュは一様・答えは未記入)")
    save(im, "pp10HoleCantileverSetup")


# ---- 10-9 V切欠き薄板の引張(精度よく評価する要素分割を問う) ----
def f_notch_plate():
    im, d = new(); title(d, "縁にV切欠きのある薄板の引張(要素分割を問う)")
    x0, yt, x1, yb = 170, 130, 500, 300
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    grid(d, x0, yt, x1, yb, 9, 4)
    tx, ty = 335, 230; lx, rx = 305, 365
    d.polygon([(lx, yt), (rx, yt), (tx, ty)], fill="white", outline=BLACK, width=3)
    force(d, x0, 215, -52, 0, "P"); force(d, x1, 215, 52, 0, "P")
    ctext(d, tx, ty + 18, "切欠き先端", FT, GRAY)
    ctext(d, (x0 + x1) / 2, yb + 22, "上縁にV切欠き・一様メッシュ", FT, GRAY)
    note(d, "左右に引張。応力を精度よく評価する要素分割は?(メッシュは一様・答えは未記入)")
    save(im, "pp10NotchPlateSetup")


# ---- 10-10 対向圧縮を受ける円板(対称性を使う効率的モデル化を問う) ----
def f_compress_disk():
    im, d = new(); title(d, "対向圧縮を受ける円板(対称性を使うモデル化を問う)")
    cx, cy, R = 330, 220, 130
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=3, fill=FILL1)
    arrow(d, cx, cy - R - 48, cx, cy - R - 4, RED, 4, 14); ctext(d, cx + 16, cy - R - 30, "P", FS, RED, "lm")
    arrow(d, cx, cy + R + 48, cx, cy + R + 4, RED, 4, 14); ctext(d, cx + 16, cy + R + 30, "P", FS, RED, "lm")
    dash(d, cx - R - 14, cy, cx + R + 14, cy, GRAY, 2)
    dash(d, cx, cy - R - 14, cx, cy + R + 14, GRAY, 2)
    ctext(d, cx + R + 30, cy, "中心線", FT, GRAY, "lm")
    note(d, "上下から対向して集中荷重P。対称性を使う効率的なモデル化は?(モデル・拘束は未記入)")
    save(im, "pp10CompressDiskSetup")


# ---- 10-13 平行四辺形に歪んだ四辺形要素(良否の判断基準を問う) ----
def f_quad_parallelogram():
    im, d = new(); title(d, "平行四辺形に歪んだ四辺形要素(良否の判断基準を問う)")
    p = [(235, 150), (455, 150), (505, 300), (285, 300)]
    d.polygon(p, outline=BLACK, width=3, fill=FILL1)
    for (vx, vy) in p:
        node(d, vx, vy, 7, "white")
    ctext(d, (p[0][0] + p[2][0]) / 2, 335, "平行四辺形に歪んだ1要素", FT, GRAY)
    note(d, "この四辺形要素は平行四辺形に歪んでいる。良し悪しの判断基準は?(基準は未記入)")
    save(im, "pp10QuadParallelogramSetup")


# ---- 10-14 台形状に歪んだ四辺形要素(テーパ歪みの指標を問う) ----
def f_quad_trapezoid():
    im, d = new(); title(d, "台形状に歪んだ四辺形要素(テーパ歪みの指標を問う)")
    q = [(180, 150), (480, 150), (395, 300), (265, 300)]
    d.polygon(q, outline=BLACK, width=3, fill=FILL1)
    for (vx, vy) in q:
        node(d, vx, vy, 7, "white")
    ctext(d, (q[0][0] + q[1][0]) / 2, 335, "台形状に歪んだ1要素", FT, GRAY)
    note(d, "この四辺形要素は台形状に歪んでいる。台形歪み(テーパ)をみる指標は?(指標は未記入)")
    save(im, "pp10QuadTrapezoidSetup")


def main():
    f_hole_plate_tension()
    f_hole_cantilever()
    f_notch_plate()
    f_compress_disk()
    f_quad_parallelogram()
    f_quad_trapezoid()
    print("done 6 figures")


if __name__ == "__main__":
    main()
