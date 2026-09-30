# -*- coding: utf-8 -*-
"""熱流体力学1級 燃焼 ch17-20 の「回答後(解説)図」= 計算・導出の worked 図。
公開前レビュー(2026-09-30)の「回答後に追加すべき情報」表に対応。
これらは figure:"helpful"(回答後)として figureImage に割り当て、
回答前は既存の条件図を preFigureImage に置く(前後2図)。
白地660x420・黒線画・プレーン表記(ギリシャ文字/添字/特殊記号は置換)。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


def panel(key, ttl, lines, answer, note_s=None):
    """タイトル＋左寄せの計算ステップ行＋下部の解(枠)。lines は文字列 or (文字列,色)。"""
    im, d = new(); title(d, ttl)
    y = 102
    for ln in lines:
        txt, col = ln if isinstance(ln, tuple) else (ln, BLACK)
        ctext(d, 55, y, txt, FS, col, "lm")
        y += 40
    by0 = max(300, y + 10)
    box(d, 70, by0, 590, by0 + 58, FILL2)
    ctext(d, 330, by0 + 29, answer, FS, RED)
    if note_s:
        note(d, note_s)
    save(im, key)


def f17_1():
    panel("t1e17AirFuelRatioAns", "17-1 解答: メタンの理論空燃比",
          ["反応 CH4 + 2 O2 -> CO2 + 2 H2O",
           "必要な酸素 = 2 mol -> 窒素 = 2 x 4 = 8 mol",
           "空気の質量 = 2x32 + 8x28 = 64 + 224 = 288 g",
           "燃料の質量 = 1 x 16 = 16 g"],
          "空燃比 = 288 / 16 = 18",
          "N2 は反応しないが空気の質量に必ず加える")


def f17_2():
    panel("t1e17EquivalenceRatioAns", "17-2 解答: プロパン混合気の当量比",
          ["量論 C3H8 + 5 O2 : 燃料/酸素比 = 1/5 = 0.20",
           "実際 C3H8 1 mol + O2 4 mol : 比 = 1/4 = 0.25",
           "phi = 実際比 / 量論比 = 0.25 / 0.20"],
          "phi = 1.25 (酸素不足 = 過濃側)")


def f17_3():
    panel("t1e17MoleMassFractionAns", "17-3 解答: モル分率から質量分率へ",
          ["平均分子量 W_bar = 0.5x32 + 0.5x28 = 30",
           "Y(O2) = X(O2) W(O2) / W_bar",
           "= 0.5 x 32 / 30 = 16 / 30"],
          "Y(O2) = 0.533 (約 0.53)",
          "重い O2 は モル分率0.5 より質量分率が大きい")


def f17_9():
    panel("t1e17ProgressVariableAns", "17-9 解答: 反応進行変数 c",
          ["c = (T - Tu) / (Tb - Tu)",
           "= (1500 - 300) / (2100 - 300)",
           "= 1200 / 1800"],
          "c = 0.667 (約 0.67)",
          "T=1500K は Tu と Tb の中間よりやや高温側")


def f18_1():
    panel("t1e18ActivationEnergyAns", "18-1 解答: 正反応の活性化エネルギー",
          ["反応物 A+B のレベル = 120 kJ/mol",
           "遷移状態 (AB)* の頂上 = 350 kJ/mol",
           "Ea = 頂上 - 反応物 = 350 - 120"],
          "Ea = 230 kJ/mol",
          "逆反応 Ea=350-80=270, 反応熱=80-120=-40 kJ/mol")


def f18_3():
    panel("t1e18ArrheniusAns", "18-3 解答: アレニウス式から活性化エネルギー",
          ["ln(k2/k1) = -(E/R0)(1/T2 - 1/T1)",
           "1/1000 - 1/800 = -2.5e-4 /K,  ln100 = 4.605",
           "E = R0 ln100 / |1/T2-1/T1| = 8.31x4.605 / 2.5e-4"],
          "E = 1.53e5 J/mol = 153 kJ/mol")


def f18_13():
    panel("t1e18SurfaceReactionAns", "18-13 解答: 表面反応の活性点収支",
          ["左辺の活性点: CO(s) と O(s) で 2 個",
           "右辺の活性点: CO2(s) で 1 個",
           "差 2 - 1 = 1 個ぶんの活性点が再生 -> 右辺に +s"],
          "CO(s) + O(s) <=> CO2(s) + s",
          "反応後に空き活性点 s が1つ現れ両辺で活性点が保存")


def f19_4():
    panel("t1e19PotentialEnergyAns", "19-4 解答: 発熱反応を表す曲線",
          [("A: 生成物が反応物より高い -> 吸熱反応", RED),
           ("B: 生成物が反応物と同レベル -> ほぼ中立", BLUE),
           ("C: 生成物が反応物より低い -> 発熱反応", GREEN)],
          "発熱を表すのは 曲線 C",
          "反応熱 = 反応物 - 生成物. 山(活性化E)の高さとは別")


def f19_8():
    panel("t1e19ArrheniusUnitsAns", "19-8 解答: 頻度係数の単位換算 (cm -> m)",
          ["二分子: 1 cm^3 = 1e-6 m^3",
           "  AI = 3.0e18 x 1e-6 = 3.0e12 m^3/(mol s)",
           "三分子: 1 cm^6 = 1e-12 m^6",
           "  AII = 4.0e15 x 1e-12 = 4.0e3 m^6/(mol^2 K s)"],
          "AI=3.0e12, AII=4.0e3 (選択肢3)")


def f19_9():
    panel("t1e19SensitivityAns", "19-9 解答: 感度解析の解釈",
          [("反応1: 大きな正 -> 燃焼速度を最も速める", RED),
           ("反応3: 大きな負 -> 燃焼速度を下げる", BLUE),
           "反応2,4,5: 感度は小さいが不要ではない"],
          "誤り = 「感度最大 = 反応速度最大」(選択肢4)",
          "感度(影響の度合い)と反応速度の絶対量は別物")


def f19_14():
    panel("t1e19ExplosionLimitsAns", "19-14 解答: 爆発限界の名称",
          ["AB = 第1限界 (壁での停止が効く低圧側)",
           "BC = 第2限界 (連鎖分枝と三体停止の釣り合い)",
           "CD = 第3限界 / ABC付近の突起 = 爆発半島"],
          "選択肢3: 爆発半島・第1・第3・停止反応",
          "第2限界は H+O2+M->HO2+M でHを奪う三体停止と分枝の競合")


def f20_2():
    panel("t1e20BurnerDiameterAns", "20-2 解答: 口径と逆火・消炎",
          ["大口径 A・B: 壁面積の割合が小 -> 熱損失が相対的に小",
           "  流速低下で火炎が管内へ戻る = 逆火",
           "小口径 C: 壁面積の割合が大 -> 熱吸収で消炎"],
          "A・B = 逆火,  C = 消炎 (選択肢1)")


def f20_4():
    panel("t1e20FlamePropagationAns", "20-4 解答: 静止気体中の既燃ガス速度",
          ["Tb/Tu = 2100/300 = 7",
           "火炎面に対する流出 Sb = Su(Tb/Tu) = 0.40x7 = 2.80 m/s",
           "静止座標 S = Sb - Su = Su(Tb/Tu - 1)",
           "= 0.40 x (7 - 1) = 0.40 x 6"],
          "S = 2.40 m/s  (Sb=2.80 m/s とは別物)")


def f20_5():
    panel("t1e20SoapBubbleAns", "20-5 解答: シャボン玉法の層流燃焼速度",
          ["半径比 ru/rb = 3.0 / 6.0 = 0.5",
           "密度比 rho_b/rho_u = (ru/rb)^3 = 0.5^3 = 0.125",
           "Su = (rho_b/rho_u) Sb = 0.125 x 8.0"],
          "Su = 1.0 m/s")


def f20_7():
    panel("t1e20ThermalTheoryAns", "20-7 解答: 熱理論による層流燃焼速度",
          ["a0 = lambda/(rho_u cp) = 0.10 / (1.0 x 1200)",
           "= 8.33e-5 m^2/s",
           "delta = 0.5 mm = 5.0e-4 m",
           "Su = a0 / delta = 8.33e-5 / 5.0e-4"],
          "Su = 0.167 m/s (約 0.17)")


def f20_11():
    panel("t1e20KarlovitzAns", "20-11 解答: カルロビッツ数",
          ["delta = 0.4 mm = 4.0e-4 m",
           "K = (dUu/dy)(delta / Uu)",
           "= 500 x (4.0e-4) / 0.5 = 0.2 / 0.5"],
          "K = 0.4")


if __name__ == "__main__":
    f17_1(); f17_2(); f17_3(); f17_9()
    f18_1(); f18_3(); f18_13()
    f19_4(); f19_8(); f19_9(); f19_14()
    f20_2(); f20_4(); f20_5(); f20_7(); f20_11()
    print("done combustion after-figures (16)")
