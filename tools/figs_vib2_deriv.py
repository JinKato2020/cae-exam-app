# -*- coding: utf-8 -*-
"""振動2級 計算問題の「回答後(helpful)」導出図。接頭辞 v2eDeriv。
白地660x420。回答後にだけ表示する解説図なので、代入と結論(答えの数値)を示す。
文字化け回避のため √・²・Δ・∝・≈ は使わず、平方根/の2乗/約/× ÷ ^ / で表記する。
実行: python tools/figs_vib2_deriv.py
"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import (new, save, title, ctext, arrow, note,
                    F, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN,
                    FILL1, W, H)

LX = 80          # 数式の左端
EQ = BLACK
HI = BLUE        # 途中結果


def eq(d, y, s, col=EQ, fnt=FS):
    ctext(d, LX, y, s, fnt, col, "lm")


def ansbox(d, s, y=336):
    d.rectangle((100, y, 560, y + 56), outline=BLUE, width=3, fill=FILL1)
    ctext(d, 330, y + 28, s, F, BLUE, "mm")


def deriv_stiffness(name):  # 10-7
    im, d = new()
    title(d, "剛性比の求め方（固有振動数を 1.2 倍にする）")
    eq(d, 120, "固有振動数 f は 剛性 k の平方根に比例（質量 m は一定）")
    eq(d, 185, "f2 / f1 = 1.2")
    eq(d, 250, "k2 / k1 = (1.2) の2乗 = 1.44", HI)
    ansbox(d, "剛性を 約 1.44 倍にする")
    save(im, name)


def deriv_spl(name):  # 10-15
    im, d = new()
    title(d, "音圧レベルの計算（p = 0.2 Pa）")
    eq(d, 110, "L = 20 × log10( p / p0 )   ,   p0 = 2×10^-5 Pa")
    eq(d, 165, "p / p0 = 0.2 / (2×10^-5) = 1×10^4", HI)
    eq(d, 220, "log10(10^4) = 4", HI)
    eq(d, 275, "L = 20 × 4 = 80 dB", HI)
    ansbox(d, "音圧レベル L = 80 dB")
    save(im, name)


def deriv_octave(name):  # 10-18
    im, d = new()
    title(d, "1/3 オクターブバンドの帯域端（中心 800 Hz）")
    eq(d, 105, "帯域端 = 中心 fc × 2^(±1/6)   ,   2^(1/6) = 約 1.122")
    eq(d, 160, "上限 = 800 × 1.122 = 約 898 Hz", HI)
    eq(d, 210, "下限 = 800 ÷ 1.122 = 約 713 Hz", HI)
    # 帯域バー
    y = 268
    arrow(d, 150, y, 520, y, GRAY, 2, 10)
    for x, lab in [(200, "713"), (335, "800"), (470, "898")]:
        d.line((x, y - 8, x, y + 8), fill=BLACK, width=2)
        ctext(d, x, y + 22, lab, FT, BLACK)
    ansbox(d, "約 713 Hz ～ 約 898 Hz")
    save(im, name)


def deriv_drift(name):  # 11-2
    im, d = new()
    title(d, "一定オフセット加速度の 2 階積分（ドリフト）")
    eq(d, 115, "x = (1/2) × a0 × t^2   （a0 = 0.2 m/s^2, t = 10 s）")
    eq(d, 175, "= (1/2) × 0.2 × 10^2", HI)
    eq(d, 235, "= (1/2) × 0.2 × 100", HI)
    ansbox(d, "ドリフト変位 x = 10 m")
    save(im, name)


def deriv_freqres(name):  # 11-18
    im, d = new()
    title(d, "FFT の周波数分解能（fs = 1024 Hz, N = 2048）")
    eq(d, 130, "周波数分解能 = fs / N")
    eq(d, 200, "= 1024 / 2048", HI)
    ansbox(d, "周波数分解能 = 0.5 Hz")
    save(im, name)


if __name__ == "__main__":
    deriv_stiffness("v2eDeriv10_7")
    deriv_spl("v2eDeriv10_15")
    deriv_octave("v2eDeriv10_18")
    deriv_drift("v2eDeriv11_2")
    deriv_freqres("v2eDeriv11_18")
    print("done 5")
