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


# ===== 第1章 =====
def deriv_1_4(name):  # 1-4 ans3
    im, d = new()
    title(d, "平行条件と直交条件（a=(2,4), b=(1,c)）")
    eq(d, 120, "平行(1次従属): (1,c)=t×(2,4) → t=1/2, c=2")
    eq(d, 185, "直交(内積=0): 2×1 + 4×c = 0 → c=-1/2", HI)
    eq(d, 250, "c=-1/2 は平行でない → 1次独立 かつ 直交")
    ansbox(d, "c=-1/2 で 1次独立 かつ 直交（答 ③）")
    save(im, name)


def deriv_1_15(name):  # 1-15 ans4
    im, d = new()
    title(d, "判別式 b^2-4ac で重解を判定")
    eq(d, 110, "ア: 2^2 - 4×1×2 = -4   （負 → 複素根）")
    eq(d, 160, "イ: 1^2 - 4×1×1 = -3   （負 → 複素根）")
    eq(d, 210, "ウ: 3^2 - 4×2×1 = +1   （正 → 相異なる実根）")
    eq(d, 260, "エ: 4^2 - 4×1×4 =  0   （重解）", HI)
    ansbox(d, "判別式=0 はエだけ（答 ④）")
    save(im, name)


# ===== 第2章 =====
def deriv_2_5(name):  # 2-5 ans1
    im, d = new()
    title(d, "無質量ばねは力をそのまま伝える → a=f/m")
    eq(d, 120, "無質量ばね: 合力=0 なので 力 f=8N が質点へ伝わる")
    eq(d, 190, "a = f / m = 8 / 2", HI)
    ansbox(d, "加速度 a = 4 m/s^2（答 ①）")
    save(im, name)


def deriv_2_11(name):  # 2-11 ans1
    im, d = new()
    title(d, "運動量保存 m1×v0 = (m1+m2)×v")
    eq(d, 120, "m1×v0 = (m1+m2)×v")
    eq(d, 190, "v = m1×v0 / (m1+m2) = 2×6 / (2+1) = 12/3", HI)
    ansbox(d, "共通速度 v = 4 m/s（答 ①）")
    save(im, name)


def deriv_2_16(name):  # 2-16 ans1
    im, d = new()
    title(d, "円運動の運動量と角運動量")
    eq(d, 115, "速度 v = l×omega = 2×3 = 6 m/s")
    eq(d, 175, "運動量 p = m×v = 0.5×6 = 3 kg m/s", HI)
    eq(d, 235, "角運動量 L = m×l^2×omega = 0.5×2^2×3 = 6", HI)
    ansbox(d, "p = 3,  L = 6（答 ①）")
    save(im, name)


def deriv_2_17(name):  # 2-17 ans4
    im, d = new()
    title(d, "角運動量保存で半径を l → l/2 に縮める")
    eq(d, 120, "m×l^2×omega = m×(l/2)^2×omega'")
    eq(d, 190, "omega' = l^2 / (l^2/4) × omega = 4×omega", HI)
    ansbox(d, "omega' = 4×omega（答 ④）")
    save(im, name)


def deriv_2_19(name):  # 2-19 ans3
    im, d = new()
    title(d, "棒＋両端質点の慣性モーメント（中心・直交軸）")
    eq(d, 115, "棒(2m): (1/12)×(2m)×L^2 = (1/6)m L^2")
    eq(d, 175, "質点2個(各 L/2): 2×m×(L/2)^2 = (1/2)m L^2")
    eq(d, 235, "I = 1/6 + 3/6 = 4/6 = 2/3  （×m L^2）", HI)
    ansbox(d, "I = (2/3) m L^2（答 ③）")
    save(im, name)


def deriv_2_20(name):  # 2-20 ans1
    im, d = new()
    title(d, "平行軸の定理 I_O = I_G + m×h^2")
    eq(d, 115, "h = l/2  （重心Gから端Oまでの距離）")
    eq(d, 175, "I_O = (1/12)m l^2 + m×(l/2)^2")
    eq(d, 235, "= 1/12 + 3/12 = 4/12  （×m l^2）", HI)
    ansbox(d, "I_O = (1/3) m l^2（答 ①）")
    save(im, name)


def deriv_2_23(name):  # 2-23 ans1
    im, d = new()
    title(d, "すべり a1 と 転がり a2 の加速度比")
    eq(d, 115, "a1 = g×sin(theta)")
    eq(d, 175, "a2 = g×sin(theta) / (1 + I/(m R^2)),  I/(m R^2)=2/5")
    eq(d, 235, "a2/a1 = 1/(1 + 2/5) = 1/(7/5) = 5/7", HI)
    ansbox(d, "a2/a1 = 5/7  （<1 なので a1>a2）（答 ①）")
    save(im, name)


# ===== 第3章 =====
def deriv_3_9(name):  # 3-9 ans3
    im, d = new()
    title(d, "平均せん断応力 tau = Q / A")
    eq(d, 115, "A = 10×10 = 100 mm^2 = 1.0×10^-4 m^2")
    eq(d, 175, "Q = 3.0 kN = 3000 N")
    eq(d, 235, "tau = 3000 / (1.0×10^-4) = 3.0×10^7 Pa", HI)
    ansbox(d, "tau = 30 MPa（答 ③）")
    save(im, name)


def deriv_3_10(name):  # 3-10 ans4
    im, d = new()
    title(d, "せん断のフックの法則 gamma = tau / G")
    eq(d, 115, "tau = 60 MPa = 6.0×10^7 Pa")
    eq(d, 175, "G = 75 GPa = 7.5×10^10 Pa")
    eq(d, 235, "gamma = 6.0×10^7 / 7.5×10^10 = 0.80×10^-3", HI)
    ansbox(d, "gamma = 8.0×10^-4（無次元）（答 ④）")
    save(im, name)


def deriv_3_11(name):  # 3-11 ans2
    im, d = new()
    title(d, "区間ごとの内力から右端変位を求める")
    eq(d, 115, "右区間 N2 = P2 → delta2 = P2×L/(A E)")
    eq(d, 175, "左区間 N1 = P1+P2 → delta1 = (P1+P2)×L/(A E)")
    eq(d, 235, "delta = delta1 + delta2 = (P1 + 2×P2)×L/(A E)", HI)
    ansbox(d, "右端変位 = (P1+2 P2) L /(A E)（答 ②）")
    save(im, name)


def deriv_3_12(name):  # 3-12 ans1
    im, d = new()
    title(d, "中空円断面 I = (pi/64)×(D^4 - d^4)")
    eq(d, 115, "D^4 = 40^4 = 2,560,000,  d^4 = 20^4 = 160,000 (mm^4)")
    eq(d, 175, "I = (pi/64)×(2,560,000 - 160,000) = (pi/64)×2,400,000")
    eq(d, 235, "= pi×37,500 = 約 1.18×10^5 mm^4", HI)
    ansbox(d, "I = 約 1.18×10^5 mm^4（答 ①）")
    save(im, name)


def deriv_3_14(name):  # 3-14 ans3
    im, d = new()
    title(d, "単純支持はりの支点反力（B点まわりモーメント）")
    eq(d, 115, "RA = P×(L-a)/L = 600×(4-1)/4 = 600×3/4 = 450 N", HI)
    eq(d, 175, "RB = P×a/L = 600×1/4 = 150 N", HI)
    eq(d, 235, "検算: RA + RB = 450 + 150 = 600 = P")
    ansbox(d, "RA = 450 N,  RB = 150 N（答 ③）")
    save(im, name)


if __name__ == "__main__":
    deriv_stiffness("v2eDeriv10_7")
    deriv_spl("v2eDeriv10_15")
    deriv_octave("v2eDeriv10_18")
    deriv_drift("v2eDeriv11_2")
    deriv_freqres("v2eDeriv11_18")
    # 第1章
    deriv_1_4("v2eDeriv1_4")
    deriv_1_15("v2eDeriv1_15")
    # 第2章
    deriv_2_5("v2eDeriv2_5")
    deriv_2_11("v2eDeriv2_11")
    deriv_2_16("v2eDeriv2_16")
    deriv_2_17("v2eDeriv2_17")
    deriv_2_19("v2eDeriv2_19")
    deriv_2_20("v2eDeriv2_20")
    deriv_2_23("v2eDeriv2_23")
    # 第3章
    deriv_3_9("v2eDeriv3_9")
    deriv_3_10("v2eDeriv3_10")
    deriv_3_11("v2eDeriv3_11")
    deriv_3_12("v2eDeriv3_12")
    deriv_3_14("v2eDeriv3_14")
    print("done", 5 + 14)
