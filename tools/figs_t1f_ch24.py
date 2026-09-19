# -*- coding: utf-8 -*-
"""熱流体力学1級 第24章「解の検証」の公式・用語図(t1f24*)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆孔回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(rho, epsilon, k, Y, Z, NO, T, FI, S, Sigma, SL, propto 等)。
※ 問題図 t1e24* とは別ファイル。上書きしない。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- 共通ヘルパ ----
def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def dashed_circle(d, cx, cy, r, col=GRAY, wd=2, seg=64):
    prev = None
    for i in range(seg + 1):
        a = 2 * math.pi * i / seg
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if prev is not None and i % 2 == 0:
            d.line((prev[0], prev[1], p[0], p[1]), fill=col, width=wd)
        prev = p


def pcircle(d, x, y, r, fill=FILL1, col=BLACK, wd=2):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wd, fill=fill)


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


def blob(d, cx, cy, rx, ry, fill, col=BLACK, wd=2):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=col, width=wd, fill=fill)


# ============================================================
# ============  公式・用語図  t1f24*  (15)  ==================
# ============================================================

# ch24-1 t1f24VandV : 検証と妥当性確認(V&V)
def vandv():
    im, d = new(); title(d, "検証(Verification) と 妥当性確認(Validation)")
    box(d, 55, 110, 320, 360, (235, 244, 250), 2)
    ctext(d, 187, 138, "検証 Verification", FS, BLUE)
    ctext(d, 187, 176, "方程式・アルゴリズムを", FT, GRAY)
    ctext(d, 187, 200, "正しく解いているか", FT, GRAY)
    ctext(d, 187, 244, "格子収束・離散化誤差", FT, BLUE)
    ctext(d, 187, 268, "コーディング誤りの確認", FT, BLUE)
    ctext(d, 187, 320, "「正しく解けているか」", FT, BLACK)
    box(d, 340, 110, 605, 360, (235, 248, 238), 2)
    ctext(d, 472, 138, "妥当性確認 Validation", FS, GREEN)
    ctext(d, 472, 176, "その方程式・モデルが", FT, GRAY)
    ctext(d, 472, 200, "現実を正しく表すか", FT, GRAY)
    ctext(d, 472, 244, "火炎温度・NO濃度を", FT, GREEN)
    ctext(d, 472, 268, "実験値と比較", FT, GREEN)
    ctext(d, 472, 320, "「正しい方程式か」", FT, BLACK)
    note(d, "燃焼CFDでは両者を区別して精度を議論する(V and V)")
    save(im, "t1f24VandV")


# ch24-2 t1f24Validation : 量ごとの実験値比較
def validation():
    im, d = new(); title(d, "妥当性確認 : 量ごとに計算値と実験値を比較")
    # 温度:一致
    box(d, 55, 100, 320, 360, (235, 248, 238), 2)
    ctext(d, 187, 124, "温度(速い主反応で決まる)", FT, GREEN)
    ox, oy = 90, 300
    arrow(d, ox, oy, ox + 200, oy, BLACK, 2, 10)
    arrow(d, ox, oy, ox, oy - 150, BLACK, 2, 10)
    mp = [(ox + 20 * i, oy - 30 - 90 * math.exp(-((i - 5) / 3.0) ** 2)) for i in range(0, 10)]
    d.line(mp, fill=BLUE, width=3)
    d.line([(x, y) for x, y in mp], fill=GREEN, width=1)
    for x, y in mp[::2]:
        node(d, x, y, 3, fill=BLUE, col=BLUE)
    ctext(d, 187, 340, "計算 = 実測 : 一致", FT, GREEN)
    # NO:ずれる
    box(d, 340, 100, 605, 360, (250, 236, 236), 2)
    ctext(d, 472, 124, "NO(遅い反応で決まる)", FT, RED)
    ox2 = 375
    arrow(d, ox2, oy, ox2 + 200, oy, BLACK, 2, 10)
    arrow(d, ox2, oy, ox2, oy - 150, BLACK, 2, 10)
    calc = [(ox2 + 20 * i, oy - 40 - 100 * math.exp(-((i - 5) / 3.0) ** 2)) for i in range(0, 10)]
    meas = [(ox2 + 20 * i, oy - 20 - 45 * math.exp(-((i - 5) / 3.0) ** 2)) for i in range(0, 10)]
    d.line(calc, fill=RED, width=3)
    d.line(meas, fill=BLUE, width=2)
    ctext(d, 472, 152, "計算(過大)", FT, RED)
    ctext(d, 500, 300, "実測", FT, BLUE, "lm")
    ctext(d, 472, 340, "計算 != 実測 : ずれ", FT, RED)
    note(d, "温度が合ってもNOはずれることがある. ずれたら前提(化学時間・ふく射)を疑う")
    save(im, "t1f24Validation")


# ch24-4 t1f24EDM : 渦消散モデルの燃料消費率
def edm():
    im, d = new(); title(d, "渦消散モデル(EDM) : 燃焼は乱流混合律速")
    # 混合の模式(燃料・酸化剤の巻き込み)
    blob(d, 175, 165, 66, 40, (232, 240, 250), BLUE, 3); ctext(d, 175, 165, "燃料 YF", FS, BLUE)
    blob(d, 470, 165, 66, 40, (232, 248, 236), GREEN, 3); ctext(d, 470, 165, "酸化剤 YO", FS, GREEN)
    d.arc((300, 140, 350, 190), 0, 300, fill=GRAY, width=2)
    arrow(d, 300, 200, 288, 235, BLUE, 2, 9)
    ctext(d, 325, 122, "乱流混合 速度 epsilon/k", FT, GRAY)
    box(d, 290, 218, 380, 275, (250, 236, 236), 2)
    ctext(d, 335, 246, "反応帯", FT, RED)
    # 式カード
    box(d, 55, 300, 605, 405, FILL1, 2)
    ctext(d, 330, 326, "R_F = A (rho epsilon / k) min[ YF, YO/sO, B YP/sP ]", FS, BLACK)
    ctext(d, 330, 356, "epsilon/k = 混合速度,  min[..] = 律速濃度(少ない方)", FT, GRAY)
    ctext(d, 330, 384, "A, B = 経験定数(普遍でなく燃料種・当量比で調整)", FT, RED)
    note(d, "層流燃焼速度より乱流強度が大きい(混合律速)場合に用いる", y=294)
    save(im, "t1f24EDM")


# ch24-5 t1f24Recirc : 旋回流と再循環流(保炎)
def recirc():
    im, d = new(); title(d, "旋回流と中心再循環流 : 高温既燃ガスを戻し保炎")
    box(d, 55, 150, 120, 320, FILL1, 3); ctext(d, 88, 235, "バーナ", FT, GRAY)
    axis = 235
    dashed(d, 120, axis, 610, axis, LGRAY, 1, 8, 6)
    # 外周順流
    arrow(d, 130, 170, 430, 170, BLUE, 3, 13)
    arrow(d, 130, 300, 430, 300, BLUE, 3, 13)
    ctext(d, 280, 152, "旋回する外周流(順流)", FT, BLUE)
    # 中心再循環(逆流)
    d.arc((150, 190, 440, 280), 0, 360, fill=RED, width=1)
    arrow(d, 400, 212, 210, 212, RED, 3, 13)
    ctext(d, 300, axis + 4, "中心再循環流(逆流)", FT, RED)
    # 高温既燃ガスの戻り+火炎基部
    arrow(d, 250, 235, 175, 235, ORANGE, 2, 11)
    ctext(d, 300, 268, "高温既燃ガスを火炎基部へ", FT, ORANGE)
    node(d, 175, 235, 7, fill=(255, 236, 210), col=ORANGE)
    ctext(d, 150, 235, "火炎", FT, ORANGE, "rm")
    note(d, "燃料粒子の滞留時間を確保し火炎を安定(保炎). NOx濃度にも強く影響する")
    save(im, "t1f24Recirc")


# ch24-6 t1f24SwirlNumber : 旋回数 S = Gtheta/(R Gx)
def swirl_number():
    im, d = new(); title(d, "旋回数  S = Gtheta / (R Gx)")
    # 定義カード
    box(d, 165, 100, 495, 180, FILL1, 2)
    ctext(d, 330, 128, "S = Gtheta / (R Gx)", FL, BLACK)
    ctext(d, 330, 162, "角運動量流束 / (半径 x 軸方向運動量流束)", FT, GRAY)
    # しきい値の対比
    box(d, 55, 205, 330, 365, (250, 236, 236), 2)
    ctext(d, 192, 230, "S < 0.6", FS, RED)
    ctext(d, 192, 262, "旋回 弱い", FT, GRAY)
    ctext(d, 192, 300, "中心再循環流 なし", FT, RED)
    ctext(d, 192, 332, "保炎 弱い", FT, RED)
    box(d, 340, 205, 605, 365, (235, 248, 238), 2)
    ctext(d, 472, 230, "S >= 0.6", FS, GREEN)
    ctext(d, 472, 262, "旋回 強い", FT, GRAY)
    ctext(d, 472, 300, "中心軸に逆流(再循環)形成", FT, GREEN)
    ctext(d, 472, 332, "強い保炎", FT, GREEN)
    note(d, "目安 S >= 0.6 で中心再循環流が現れる. 燃焼器の保炎特性を見積もる基本指標")
    save(im, "t1f24SwirlNumber")


# ch24-7 t1f24Ensemble : RANSアンサンブル平均と火炎面
def ensemble():
    im, d = new(); title(d, "RANS アンサンブル平均 : 火炎面のしわがならされる")
    # 左:瞬時(しわ) 複数実現
    box(d, 55, 100, 320, 360, "white", 2)
    ctext(d, 187, 122, "瞬時の実現(多数)", FT, BLUE)
    cx, cy = 187, 240
    for off, col in [(-14, LGRAY), (0, RED), (14, LGRAY)]:
        prev = None
        for i in range(0, 361, 5):
            a = math.radians(i)
            rr = 78 * (1 + 0.18 * math.sin(6 * a + off))
            p = (cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.9)
            if prev is not None:
                d.line((prev[0], prev[1], p[0], p[1]), fill=col, width=2)
            prev = p
    ctext(d, 187, 340, "しわ状(渦ごとに変動)", FT, RED)
    # 矢印(平均操作)
    arrow(d, 325, 235, 340, 235, GRAY, 3, 12)
    ctext(d, 332, 210, "平均", FT, GRAY)
    # 右:平均(滑らか同心円)
    box(d, 350, 100, 605, 360, "white", 2)
    ctext(d, 477, 122, "アンサンブル平均(RANS)", FT, GREEN)
    cx2, cy2 = 477, 240
    for rr in (40, 62, 84):
        d.ellipse((cx2 - rr, cy2 - rr * 0.9, cx2 + rr, cy2 + rr * 0.9), outline=GREEN, width=2)
    ctext(d, 477, 340, "滑らかな同心円状", FT, GREEN)
    note(d, "瞬時のしわを見るにはLES/DNSが必要. 平滑なRANS結果を不正確と短絡しない")
    save(im, "t1f24Ensemble")


# ch24-8 t1f24Lifted : 浮き上がり火炎と予混合基部
def lifted():
    im, d = new(); title(d, "浮き上がり火炎 : 基部に予混合火炎 -> モデル併用が必要")
    nx = 300
    box(d, nx - 26, 355, nx + 26, 400, FILL1, 3); ctext(d, nx, 378, "ノズル", FT, GRAY)
    arrow(d, nx, 355, nx, 305, BLUE, 3, 12); ctext(d, nx + 38, 332, "燃料噴流", FT, BLUE, "lm")
    baseY = 255
    dashed(d, nx - 85, 355, nx - 85, baseY, GRAY, 1, 6, 5)
    arrow(d, nx - 85, 355, nx - 85, baseY, GRAY, 2, 11)
    arrow(d, nx - 85, baseY, nx - 85, 355, GRAY, 2, 11)
    ctext(d, nx - 92, (355 + baseY) / 2, "浮き上がり距離", FT, GRAY, "rm")
    d.line((nx - 52, baseY, nx + 52, baseY), fill=GREEN, width=4)
    ctext(d, nx + 66, baseY, "予混合火炎(基部)", FT, GREEN, "lm")
    d.line((nx - 52, baseY, nx - 28, 120), fill=RED, width=3)
    d.line((nx + 52, baseY, nx + 28, 120), fill=RED, width=3)
    d.line((nx - 28, 120, nx + 28, 120), fill=RED, width=2)
    ctext(d, nx + 80, 175, "拡散火炎", FT, RED, "lm")
    note(d, "基部の乱流燃焼速度と流速の釣り合いで浮き上がり位置決定. 拡散+予混合の併用モデルが要")
    save(im, "t1f24Lifted")


# ch24-9 t1f24FlameIndex : フレームインデックス FI
def flame_index():
    im, d = new(); title(d, "フレームインデックス  FI = grad(YF) . grad(YO2)")
    box(d, 55, 95, 320, 355, (235, 244, 250), 2)
    ctext(d, 187, 120, "勾配 同じ向き", FS, BLUE)
    ox, oy = 135, 255
    arrow(d, ox, oy, ox + 92, oy - 52, BLUE, 4, 14); ctext(d, ox + 98, oy - 58, "grad YF", FT, BLUE, "lm")
    arrow(d, ox, oy + 20, ox + 80, oy - 24, GREEN, 4, 14); ctext(d, ox + 86, oy - 18, "grad YO2", FT, GREEN, "lm")
    ctext(d, 187, 320, "FI > 0 : 予混合火炎片", FS, BLUE)
    box(d, 340, 95, 605, 355, (250, 236, 236), 2)
    ctext(d, 472, 120, "勾配 逆向き", FS, RED)
    ox2, oy2 = 472, 245
    arrow(d, ox2, oy2, ox2 - 82, oy2 - 44, BLUE, 4, 14); ctext(d, ox2 - 88, oy2 - 50, "grad YF", FT, BLUE, "rm")
    arrow(d, ox2, oy2, ox2 + 82, oy2 + 44, GREEN, 4, 14); ctext(d, ox2 + 88, oy2 + 50, "grad YO2", FT, GREEN, "lm")
    ctext(d, 472, 320, "FI < 0 : 拡散火炎片", FS, RED)
    note(d, "内積の符号で局所の燃焼形態を分類. DNS/LES結果から燃焼形態分布を読む")
    save(im, "t1f24FlameIndex")


# ch24-11 t1f24MixFrac : 混合分率 Z と保存量仮定
def mix_frac():
    im, d = new(); title(d, "混合分率 Z : 燃料側 Z=1, 酸化剤側 Z=0 の保存量")
    # 対向する燃料流と酸化剤流
    box(d, 55, 130, 200, 300, (250, 240, 232), 2)
    ctext(d, 127, 160, "燃料(ノズル流体)", FT, RED)
    ctext(d, 127, 235, "Z = 1", FL, RED)
    box(d, 460, 130, 605, 300, (235, 244, 250), 2)
    ctext(d, 532, 160, "酸化剤(周囲流体)", FT, BLUE)
    ctext(d, 532, 235, "Z = 0", FL, BLUE)
    # 中間の混合(Z勾配)
    arrow(d, 205, 215, 300, 215, RED, 2, 11)
    arrow(d, 455, 215, 360, 215, BLUE, 2, 11)
    ctext(d, 330, 175, "混合分率 0 < Z < 1", FT, GRAY)
    ctext(d, 330, 235, "Z", FL, BLACK)
    box(d, 55, 320, 605, 405, FILL1, 2)
    ctext(d, 330, 346, "Z = 燃料と酸化剤の質量混合割合. 反応で生成・消滅しない保存量", FT, BLACK)
    ctext(d, 330, 378, "保存量仮定が成立 = 気相に燃料源が無いガス火炎の場合", FT, RED)
    save(im, "t1f24MixFrac")


# ch24-12 t1f24SprayMixFrac : 噴霧火炎の混合分率非保存
def spray_mix_frac():
    im, d = new(); title(d, "噴霧火炎 : 液滴蒸発で気相の混合分率 Z が非保存")
    ox, oy, xl, yl = 110, 330, 460, 210
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "下流 x", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "気相の混合分率 Z", FT, BLACK, "rm")
    # 液滴(分散相)と蒸発矢印
    for dx in (0.15, 0.35, 0.55, 0.75):
        px = ox + dx * xl
        node(d, px, oy - 0.15 * yl, 6, fill=(235, 235, 235), col=BLACK)
        arrow(d, px, oy - 0.15 * yl - 6, px, oy - 0.35 * yl, ORANGE, 2, 8)
    ctext(d, ox + 0.45 * xl, oy - 0.08 * yl, "液滴(分散相)", FT, GRAY)
    ctext(d, ox + 0.20 * xl, oy - 0.42 * yl, "蒸発で気相へ燃料供給", FT, ORANGE, "lm")
    # Z増加曲線
    pts = [(ox + (i / 200) * xl, oy - (0.25 + 0.55 * (i / 200)) * yl) for i in range(0, 201)]
    d.line(pts, fill=RED, width=3, joint="curve")
    ctext(d, ox + 0.82 * xl, oy - 0.72 * yl, "Z 増加", FT, RED, "lm")
    note(d, "気相だけを見るとZは保存されず下流で増加. 保存量仮定の適用限界の代表例")
    save(im, "t1f24SprayMixFrac")


# ch24-13 t1f24GroupComb : 群燃焼とすす生成
def group_comb():
    im, d = new(); title(d, "群燃焼(グループ燃焼) : 高当量比で拡散火炎+すす増")
    # 左:低当量比(液滴疎・個別予混合的)
    box(d, 55, 100, 320, 360, (235, 244, 250), 2)
    ctext(d, 187, 124, "低当量比(液滴 疎)", FT, BLUE)
    for dx, dy in [(150, 200), (210, 230), (170, 280)]:
        node(d, dx, dy, 9, fill=(235, 235, 235), col=BLACK)
        dashed_circle(d, dx, dy, 20, BLUE, 1)
    ctext(d, 187, 330, "個別に予混合的に燃焼", FT, BLUE)
    # 右:高当量比(液滴密・群として拡散燃焼)
    box(d, 340, 100, 605, 360, (250, 236, 236), 2)
    ctext(d, 472, 124, "高当量比(液滴 密)", FT, RED)
    for dx, dy in [(440, 200), (480, 210), (510, 240), (455, 250), (495, 275)]:
        node(d, dx, dy, 8, fill=(235, 235, 235), col=BLACK)
    dashed_circle(d, 478, 235, 60, RED, 2)
    ctext(d, 478, 235, "群 拡散火炎", FT, RED)
    for sx in (430, 460, 490, 520):
        node(d, sx, 320, 5, fill=(90, 90, 90), col=BLACK)
    ctext(d, 555, 320, "すす 多", FT, RED, "lm")
    note(d, "すすは酸素不足で燃料過濃な拡散火炎領域で多く生成. 高当量比ほど すす濃度大")
    save(im, "t1f24GroupComb")


# ch24-14 t1f24Radiation : ふく射伝熱と火炎温度低下・失火
def radiation():
    im, d = new(); title(d, "ふく射伝熱 : 火炎温度低下 と 下流の失火")
    # 火炎(高温)から周囲(低温300K)へ放射
    blob(d, 300, 220, 130, 55, (250, 226, 226), RED, 3)
    ctext(d, 250, 220, "火炎(高温)", FS, RED)
    # 放射矢印(四方へ)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        sx = 300 + 135 * math.cos(rad); sy = 220 + 58 * math.sin(rad)
        arrow(d, sx, sy, 300 + 185 * math.cos(rad), 220 + 90 * math.sin(rad), ORANGE, 2, 9)
    ctext(d, 300, 115, "周囲空気 300K(低温)へ 正味放熱", FT, ORANGE)
    # 下流の失火(破線円)
    dashed_circle(d, 470, 220, 42, RED, 2)
    ctext(d, 470, 220, "失火", FT, RED)
    arrow(d, 405, 245, 445, 235, RED, 2, 10)
    box(d, 55, 320, 605, 405, FILL1, 2)
    ctext(d, 330, 346, "周囲が火炎より低温 -> ふく射で正味放熱 -> 火炎温度低下", FT, BLACK)
    ctext(d, 330, 378, "噴霧では蒸発速度は増すが温度は下がり, 下流で失火(局所消炎)", FT, RED)
    save(im, "t1f24Radiation")


# ch24-15 t1f24ThermalNO : 熱的NO(Zeldovich)の温度依存
def thermal_no():
    im, d = new(); title(d, "熱的NO(Zeldovich) : 生成速度 ~ exp(-Ta/T)")
    ox, oy, xl, yl = 120, 350, 440, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "火炎温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "NO 生成速度", FT, BLACK, "rm")
    # 急峻な指数曲線
    def h(t):
        return min(math.exp(6.5 * (t - 0.95)), 1.0) * 0.9 * yl
    pts = [(ox + (0.05 + 0.90 * i / 200) * xl, oy - h(0.05 + 0.90 * i / 200)) for i in range(0, 201)]
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 数十〜百K低下で大きく減少
    t1, t2 = 0.86, 0.72
    for t, lab, col in [(t2, "低温側", GREEN), (t1, "高温側", RED)]:
        xp = ox + t * xl; yp = oy - h(t)
        node(d, xp, yp, 6, fill=col, col=col)
        dashed(d, xp, oy, xp, yp, LGRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, LGRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, col)
    arrow(d, ox + 0.30 * xl, oy - h(t2), ox + 0.30 * xl, oy - h(t1), GRAY, 2, 10)
    ctext(d, ox + 0.30 * xl - 6, (oy - h(t1) + oy - h(t2)) / 2, "大きな差", FT, GRAY, "rm")
    note(d, "Ta=活性化温度(数万K). 数十〜百Kの温度低下で生成速度が大きく減少する")
    save(im, "t1f24ThermalNO")


# ch24-17 t1f24Unsteady : 非定常フレームレット法
def unsteady():
    im, d = new(); title(d, "非定常フレームレット法 : 遅いNOの時間変化を追う")
    ox, oy, xl, yl = 110, 350, 460, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "時間 t", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "NO 濃度", FT, BLACK, "rm")
    # 定常値(即座に高い水平線=過大)
    yss = oy - 0.80 * yl
    dashed(d, ox, yss, ox + xl, yss, RED, 2, 9, 6)
    ctext(d, ox + 0.62 * xl, yss - 16, "定常FL(即 平衡 NO=過大)", FT, RED, "lm")
    # 非定常(徐々に立ち上がる=実測寄り)
    pts = [(ox + (i / 200) * xl, oy - 0.50 * yl * (1 - math.exp(-3.0 * (i / 200)))) for i in range(0, 201)]
    d.line(pts, fill=GREEN, width=3, joint="curve")
    ctext(d, ox + 0.55 * xl, oy - 0.30 * yl, "非定常FL(時間変化を反映)", FT, GREEN, "lm")
    # 実測点
    for t in (0.3, 0.5, 0.7, 0.9):
        node(d, ox + t * xl, oy - 0.48 * yl * (1 - math.exp(-3.0 * t)), 4, fill=BLUE, col=BLUE)
    ctext(d, ox + 0.9 * xl, oy - 0.55 * yl, "実測", FT, BLUE)
    note(d, "混合分率に沿う1次元詳細反応でNOの履歴を追う. 定常FLの過大評価への対策")
    save(im, "t1f24Unsteady")


# ch24-18 t1f24CFM : コヒーレントフレームモデル
def cfm():
    im, d = new(); title(d, "コヒーレントフレームモデル : Rf = rho_u SL Sigma")
    # 火炎面を薄い層流火炎面の集合とみなす(しわのある帯)
    cx, cy = 330, 210
    prev = None
    for i in range(0, 201):
        t = i / 200
        x = 90 + t * 480
        y = cy - 40 * math.sin(2 * math.pi * 3 * t)
        if prev is not None:
            d.line((prev[0], prev[1], x, y), fill=RED, width=3)
        prev = (x, y)
    ctext(d, 330, 120, "しわの多い火炎面(火炎面密度 Sigma)", FT, RED)
    # 未燃側から供給
    for x in (170, 330, 490):
        arrow(d, x, 300, x, 258, BLUE, 2, 9)
    ctext(d, 330, 318, "未燃予混合ガス(rho_u, SL)", FT, BLUE)
    # 式カード
    box(d, 55, 335, 605, 405, FILL1, 2)
    ctext(d, 330, 360, "Rf = rho_u . SL . Sigma", FS, BLACK)
    ctext(d, 330, 388, "rho_u=未燃密度, SL=層流燃焼速度, Sigma=火炎面密度", FT, GRAY)
    note(d, "RANSと組み合わせ予混合火炎伝播を計算. 火炎面形状の時間変化を検証対象に", y=330)
    save(im, "t1f24CFM")


# ============================================================
if __name__ == "__main__":
    vandv()           # ch24-1
    validation()      # ch24-2
    edm()             # ch24-4
    recirc()          # ch24-5
    swirl_number()    # ch24-6
    ensemble()        # ch24-7
    lifted()          # ch24-8
    flame_index()     # ch24-9
    mix_frac()        # ch24-11
    spray_mix_frac()  # ch24-12
    group_comb()      # ch24-13
    radiation()       # ch24-14
    thermal_no()      # ch24-15
    unsteady()        # ch24-17
    cfm()             # ch24-18
    print("done t1f ch24")
