# -*- coding: utf-8 -*-
"""固体2級 公開前レビュー: ch10/11 の回答前(preFigureImage)観察図。
観察された図(等高線・応力ベクトル・主応力矢印・V&V手順の空欄)を、答えを示さずに提示する。
[[cae-figure-before-after-rule]]。"""
import sys
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def f_contour_setup():          # 10-37
    im, d = new(); title(d, "z荷重を受けた片持ち板：表示された等高線")
    wall(d, 150, 140, 300)
    x0, x1, yt, yb = 150, 520, 140, 300
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3)
    n = 6
    for i in range(1, n + 1):
        x = x0 + (x1 - x0) * i / (n + 1)
        g = 205 - int(160 * i / n)
        d.line((x, yt, x, yb), fill=(g, g, g), width=3)
        ctext(d, x, yb + 14, str(i), FT, GRAY)
    ctext(d, x0 + 6, yt - 12, "小", FT, GRAY, "lm")
    ctext(d, x1 - 6, yt - 12, "大", FT, GRAY, "rm")
    force(d, x1 - 4, yt - 4, 0, 40, "z荷重")
    note(d, "等高線は自由端側ほど値が大きい。この等高線が表す量は何か。")
    save(im, "pp10CantileverContourSetup")


def f_stress_vec_setup():       # 10-38
    im, d = new(); title(d, "自由表面の応力ベクトル図(面内2軸引張の箇所)")
    cx, cy, s = 330, 215, 72
    d.rectangle((cx - s, cy - s, cx + s, cy + s), fill=FILL1, outline=BLACK, width=3)
    force(d, cx + s, cy, 58, 0, "", GREEN); force(d, cx - s, cy, -58, 0, "", GREEN)
    force(d, cx, cy - s, 0, -42, "", GREEN); force(d, cx, cy + s, 0, 42, "", GREEN)
    ctext(d, cx, cy - 8, "自由表面", FT, GRAY)
    ctext(d, cx, cy + 14, "面直応力 ≈ 0", FT, GRAY)
    ctext(d, cx + s + 62, cy - 6, "面内の矢印", FT, GRAY, "lm")
    note(d, "自由表面で面内2方向に矢印が描かれている。この矢印が示す応力は何か。")
    save(im, "pp10StressVectorSetup")


def f_principal_arrows_setup():  # 10-39
    im, d = new(); title(d, "最大主応力の矢印列：6要素目だけ向きが90°急変")
    y = 205; n = 8; x0 = 90; step = 62
    for i in range(n):
        cx = x0 + i * step
        col = RED if i == 5 else BLACK
        d.rectangle((cx - 24, y - 24, cx + 24, y + 24), outline=col, width=3 if i == 5 else 2)
        if i == 5:
            arrow(d, cx, y + 18, cx, y - 18, RED, 3, 11)
            arrow(d, cx, y - 18, cx, y + 18, RED, 3, 11)
        else:
            arrow(d, cx - 18, y, cx + 18, y, BLACK, 3, 11)
            arrow(d, cx + 18, y, cx - 18, y, BLACK, 3, 11)
        ctext(d, cx, y + 40, str(i + 1), FT, col)
    ctext(d, x0 + 5 * step, y - 42, "90°急変", FT, RED)
    ctext(d, 330, 300, "この付近では σ1 と σ2 の大きさが接近している", FS, GRAY)
    note(d, "6要素目だけ最大主応力の向きが90°飛んでいる。この現象の解釈は何か。")
    save(im, "pp10PrincipalArrowsSetup")


def f_vvproc_setup():           # 11-16
    im, d = new(); title(d, "ASME V&V の手順(空欄 A・B・C・D を答える)")

    def box(cx, cy, w, h, letter):
        d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=FILL1)
        ctext(d, cx, cy, "?", FL)
        d.ellipse((cx - w / 2 - 4, cy - h / 2 - 4, cx - w / 2 + 26, cy - h / 2 + 26), outline=RED, width=3, fill="white")
        ctext(d, cx - w / 2 + 11, cy - h / 2 + 11, letter, F, RED)

    ax, ay = 210, 120; bx, by = 210, 300; dx, dy = 500, 300
    box(ax, ay, 200, 66, "A"); box(bx, by, 200, 66, "B"); box(dx, dy, 210, 66, "D")
    ctext(d, ax, ay - 50, "現実の物理現象 → 概念モデル → A", FT, GRAY)
    arrow(d, ax, ay + 33, bx, by - 33, BLACK, 3, 14)
    d.ellipse((bx + 8, (ay + by) / 2 - 15, bx + 38, (ay + by) / 2 + 15), outline=RED, width=3, fill="white")
    ctext(d, bx + 23, (ay + by) / 2, "C", F, RED)
    ctext(d, bx + 46, (ay + by) / 2, "A→B の実装が正しいかを調べる活動", FT, GRAY, "lm")
    arrow(d, bx + 100, by - 12, dx - 105, dy - 12, BLACK, 3, 13)
    arrow(d, dx - 105, dy + 12, bx + 100, by + 12, BLACK, 3, 13)
    ctext(d, (bx + dx) / 2 - 12, by - 52, "左右を比較", FT, GRAY)
    note(d, "左=解析経路、右=実験経路の出発点 D。空欄 A〜D に入る語を答える。")
    save(im, "ver11VVProcSetup")


if __name__ == "__main__":
    for fn in [f_contour_setup, f_stress_vec_setup, f_principal_arrows_setup, f_vvproc_setup]:
        fn()
    print("done ch1013 prefig")
