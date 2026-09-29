# -*- coding: utf-8 -*-
"""固体1級 第1章 レビュー修正の図(回答後 helpful)を再生成。
生成元が消失していた s1e1GLcompute / s1e1Conjugate を作り直す。
- s1e1GLcompute(1-10): 設問の変形勾配 F=[[1.2,0.1],[0,1.0]] に一致した計算フロー
  (旧図は別問題の単純せん断 F12=0.5 を描いていた誤り)。
- s1e1Conjugate(1-17): 仕事共役表。σ:D は現体積当たり、基準体積当たりは Jσ:D=τ:D と明示
  (旧図は基準体積の枠内に σ コーシー↔D を並べていた不整合)。
[[cae-figure-before-after-rule]]。回答前(Setup)図はいずれも正しいので触らない。"""
import sys
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def f_gl_compute_post():     # 1-10 回答後
    im, d = new(); title(d, "計算フロー  F → C=F^T F → E=1/2(C-I)")
    y = 175; cell = 58; yc = y + cell
    matrix_grid(d, 52,  y, [["1.2", "0.1"], ["0", "1.0"]],       cell=cell, fnt=FT)
    ctext(d, 52 + cell,  y - 24, "F", FS)
    matrix_grid(d, 282, y, [["1.44", "0.12"], ["0.12", "1.01"]], cell=cell, fnt=FT)
    ctext(d, 282 + cell, y - 24, "C", FS)
    matrix_grid(d, 512, y, [["0.22", "0.06"], ["0.06", "0.005"]], cell=cell, fnt=FT)
    ctext(d, 512 + cell, y - 24, "E", FS)
    arrow(d, 172, yc, 276, yc, BLACK, 3, 11); ctext(d, 224, yc - 16, "F^T F", FT)
    arrow(d, 402, yc, 506, yc, BLACK, 3, 11); ctext(d, 454, yc - 16, "1/2(C-I)", FT)
    note(d, "例: F=[[1.2,0.1],[0,1.0]]。C=F^T F、E=1/2(C-I)。よって E₁₁=0.22, E₁₂=0.06")
    save(im, "s1e1GLcompute")


def f_conjugate():           # 1-17 回答後
    im, d = new(); title(d, "仕事共役の応力・ひずみ速度ペア")
    ctext(d, W / 2, 66, "基準体積当たり  W = τ:D = S:(dE/dt) = Π:(dF/dt)   (τ = Jσ)", FS)
    x0, xm, x1 = 55, 330, 605
    top = 96; rh = 40; nrow = 5
    for i in range(nrow + 1):
        d.line((x0, top + i * rh, x1, top + i * rh), fill=BLACK, width=2)
    for xx in (x0, xm, x1):
        d.line((xx, top, xx, top + nrow * rh), fill=BLACK, width=2)

    def row(i, a, b, col=BLACK):
        yy = top + i * rh + rh / 2
        ctext(d, (x0 + xm) / 2, yy, a, FS, col)
        ctext(d, (xm + x1) / 2, yy, b, FS, col)
    row(0, "応力", "共役なひずみ速度")
    row(1, "τ  キルヒホッフ (=Jσ)", "D  ストレッチング")
    row(2, "S  第2PK", "dE/dt  (グリーン)")
    row(3, "Π  第1PK", "dF/dt  (変形勾配)")
    row(4, "σ  コーシー ※現体積", "D （σ:D は現体積当たり）", GRAY)
    note(d, "σ:D は現体積当たり。基準体積当たりにするには Jσ:D = τ:D とする(表の τ:D 行)")
    save(im, "s1e1Conjugate")


if __name__ == "__main__":
    f_gl_compute_post()
    f_conjugate()
