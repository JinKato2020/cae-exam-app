# -*- coding: utf-8 -*-
"""熱流体力学1級 第24章「解の検証」の問題図(t1e24*)を描画。
白地660x420・黒線画・機構/構造/座標系/プロファイルのみ・数値や答えは書かない。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(rho, epsilon, k, Y, Z, NO, T, FI, S, phi 等)。"""
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
# ============  問題図  t1e24*  (10)  ========================
# ============================================================

# 24-1 t1e24EddyDissipation : 渦消散モデル(混合律速)
def eddy_dissipation():
    im, d = new(); title(d, "渦消散モデル : 乱流混合が反応速度を律速する")
    # 燃料塊(左)と酸化剤塊(右)を渦で引き伸ばし混合
    blob(d, 175, 175, 70, 42, (232, 240, 250), BLUE, 3)
    ctext(d, 175, 175, "燃料 YF", FS, BLUE)
    blob(d, 470, 175, 70, 42, (232, 248, 236), GREEN, 3)
    ctext(d, 470, 175, "酸化剤 YO", FS, GREEN)
    # 乱流渦(巻き込み)矢印
    for cx, col in [(300, BLUE), (345, GREEN)]:
        d.arc((cx - 26, 150, cx + 26, 202), 0, 300, fill=col, width=2)
        arrow(d, cx + 24, 176, cx + 22, 160, col, 2, 8)
    ctext(d, 322, 128, "乱流渦で引き伸ばし混合", FT, GRAY)
    # 混合層(反応)帯
    box(d, 285, 235, 385, 300, (250, 236, 236), 2)
    ctext(d, 335, 258, "反応帯", FT, RED)
    ctext(d, 335, 282, "混合速度 ~ epsilon/k", FT, RED)
    arrow(d, 205, 200, 288, 250, BLUE, 2, 11)
    arrow(d, 440, 200, 382, 250, GREEN, 2, 11)
    # 式カード
    box(d, 55, 320, 605, 405, FILL1, 2)
    ctext(d, 330, 345, "R_F = A (rho epsilon / k) min[ YF, YO/sO, B YP/sP ]", FS, BLACK)
    ctext(d, 330, 375, "A, B = 経験定数(燃料種・当量比で調整)", FT, RED)
    note(d, "反応は乱流混合律速. 混合速度 epsilon/k と律速濃度 min[..] で決まる", y=312)
    save(im, "t1e24EddyDissipation")


# 24-2 t1e24SwirlRecirc : 旋回流と中心再循環流
def swirl_recirc():
    im, d = new(); title(d, "旋回バーナの中心再循環流(逆流)による保炎")
    # バーナ出口(左)から流れ
    box(d, 55, 175, 120, 295, FILL1, 3)
    ctext(d, 88, 235, "バーナ", FT, GRAY)
    axis = 235
    dashed(d, 120, axis, 610, axis, LGRAY, 1, 8, 6)
    ctext(d, 600, axis + 16, "中心軸", FT, GRAY, "rm")
    # 外周の順流(矢印A)上下2本
    for yy, lab in [(150, True), (320, False)]:
        arrow(d, 130, yy, 420, yy, BLUE, 3, 13)
    ctext(d, 275, 132, "外周 順流 (A)", FT, BLUE)
    # 中心軸上の逆流循環(矢印B) : 楕円状の再循環域
    d.arc((150, 190, 430, 280), 0, 360, fill=RED, width=1)
    arrow(d, 390, 210, 220, 210, RED, 3, 13)   # 中心へ戻る逆流
    arrow(d, 220, 262, 390, 262, RED, 2, 11)
    ctext(d, 300, axis + 4, "中心再循環流(逆流 B)", FT, RED)
    # 火炎が逆流域に保持
    d.line((175, 210, 205, 235), fill=ORANGE, width=3)
    d.line((175, 262, 205, 235), fill=ORANGE, width=3)
    node(d, 195, 235, 6, fill=(255, 236, 210), col=ORANGE)
    ctext(d, 150, 235, "火炎", FT, ORANGE, "rm")
    note(d, "強い旋回で中心軸に逆流が生じ, 高温既燃ガスが火炎基部へ戻り保炎する")
    save(im, "t1e24SwirlRecirc")


# 24-3 t1e24RansEnsemble : 瞬時(LES)と平均(RANS)火炎面の対比
def rans_ensemble():
    im, d = new(); title(d, "円筒容器内の予混合火炎伝播 : 瞬時(LES) と 平均(RANS)")
    # 左:LES的な瞬時しわ状火炎面
    lcx, lcy, R = 175, 245, 95
    box(d, 70, 150, 285, 355, "white", 2)
    ctext(d, 178, 132, "瞬時場(LES的)", FT, BLUE)
    node(d, lcx, lcy - 55, 5, fill=RED, col=RED)
    ctext(d, lcx + 8, lcy - 68, "Ig", FT, RED, "lm")
    # しわ状の閉曲線
    prev = None
    for i in range(0, 361, 4):
        a = math.radians(i)
        rr = R * (1 + 0.16 * math.sin(7 * a) * math.cos(2 * a))
        p = (lcx + rr * math.cos(a) * 0.95, (lcy - 55) + rr * math.sin(a) * 0.95)
        if prev is not None:
            d.line((prev[0], prev[1], p[0], p[1]), fill=RED, width=2)
        prev = p
    ctext(d, lcx, lcy + 92, "しわ状火炎面", FT, RED)
    # 右:RANS的な滑らかな同心円
    rcx, rcy = 470, 245
    box(d, 375, 150, 590, 355, "white", 2)
    ctext(d, 482, 132, "アンサンブル平均(RANS的)", FT, GREEN)
    node(d, rcx, rcy - 55, 5, fill=RED, col=RED)
    ctext(d, rcx + 8, rcy - 68, "Ig", FT, RED, "lm")
    for rr in (40, 66, 92):
        d.ellipse((rcx - rr, (rcy - 55) - rr * 0.95, rcx + rr, (rcy - 55) + rr * 0.95),
                  outline=GREEN, width=2)
    ctext(d, rcx, rcy + 92, "滑らかな同心円状", FT, GREEN)
    # r/z 軸(小さく)
    arrow(d, 300, 375, 355, 375, BLACK, 2, 9); ctext(d, 360, 375, "r", FT, BLACK, "lm")
    arrow(d, 300, 375, 300, 335, BLACK, 2, 9); ctext(d, 300, 328, "z", FT, BLACK)
    note(d, "容器 phi100mm 厚さ20mm. 平均操作で個々の渦のしわがならされる")
    save(im, "t1e24RansEnsemble")


# 24-4 t1e24LiftedFlame : 浮き上がり噴流拡散火炎(予混合基部)
def lifted_flame():
    im, d = new(); title(d, "浮き上がり噴流拡散火炎 : 予混合基部と拡散火炎")
    # ノズル(下)
    nx = 330
    box(d, nx - 26, 355, nx + 26, 400, FILL1, 3)
    ctext(d, nx, 378, "ノズル", FT, GRAY)
    arrow(d, nx, 355, nx, 300, BLUE, 3, 12)
    ctext(d, nx + 40, 330, "燃料噴流", FT, BLUE, "lm")
    # 浮き上がり距離(ノズル出口->火炎基部)
    baseY = 250
    dashed(d, nx - 90, 355, nx - 90, baseY, GRAY, 1, 6, 5)
    arrow(d, nx - 90, 355, nx - 90, baseY, GRAY, 2, 11)
    arrow(d, nx - 90, baseY, nx - 90, 355, GRAY, 2, 11)
    ctext(d, nx - 96, (355 + baseY) / 2, "浮き上がり距離", FT, GRAY, "rm")
    # 火炎基部の予混合火炎(横帯)
    d.line((nx - 55, baseY, nx + 55, baseY), fill=GREEN, width=4)
    ctext(d, nx + 70, baseY, "予混合火炎(基部)", FT, GREEN, "lm")
    # 下流の拡散火炎(上に開く2本)
    d.line((nx - 55, baseY, nx - 30, 115), fill=RED, width=3)
    d.line((nx + 55, baseY, nx + 30, 115), fill=RED, width=3)
    d.line((nx - 30, 115, nx + 30, 115), fill=RED, width=2)
    ctext(d, nx + 90, 175, "拡散火炎", FT, RED, "lm")
    note(d, "基部の予混合火炎の乱流燃焼速度と流速の釣り合いで浮き上がり位置が決まる")
    save(im, "t1e24LiftedFlame")


# 24-5 t1e24SprayEquiv : 噴霧火炎の当量比比較(3段x2列)
def spray_equiv():
    im, d = new(); title(d, "噴霧火炎 : 高当量比 と 低当量比 の比較(3量)")
    # 列見出し
    colx = [235, 470]
    ctext(d, colx[0], 62, "高当量比", FS, RED)
    ctext(d, colx[1], 62, "低当量比", FS, BLUE)
    # 行見出し
    rows = ["ガス温度", "フレーム指数", "すす濃度"]
    rowy = [110, 210, 310]
    for lab, yy in zip(rows, rowy):
        ctext(d, 95, yy + 30, lab, FT, GRAY, "mm")
    # 上方噴霧・下方予混合ガスの表示(左上に小さく)
    arrow(d, 235, 78, 235, 92, GRAY, 2, 8)
    # 各セル
    for ci, cx in enumerate(colx):
        high = (ci == 0)
        # 温度セル:高当量比は拡散火炎で広く高温
        box(d, cx - 78, rowy[0], cx + 78, rowy[0] + 60, "white", 2)
        if high:
            blob(d, cx, rowy[0] + 30, 60, 22, (250, 226, 226), RED, 2)
            ctext(d, cx, rowy[0] + 30, "広い高温域", FT, RED)
        else:
            blob(d, cx, rowy[0] + 30, 34, 18, (250, 236, 236), RED, 2)
            ctext(d, cx, rowy[0] + 30, "狭い", FT, RED)
        # フレーム指数セル
        box(d, cx - 78, rowy[1], cx + 78, rowy[1] + 60, "white", 2)
        if high:
            ctext(d, cx, rowy[1] + 24, "拡散火炎片 多", FT, RED)
            ctext(d, cx, rowy[1] + 44, "FI < 0 領域大", FT, RED)
        else:
            ctext(d, cx, rowy[1] + 24, "予混合火炎片 多", FT, BLUE)
            ctext(d, cx, rowy[1] + 44, "FI > 0 領域大", FT, BLUE)
        # すすセル
        box(d, cx - 78, rowy[2], cx + 78, rowy[2] + 60, "white", 2)
        if high:
            for sx in range(cx - 50, cx + 51, 20):
                node(d, sx, rowy[2] + 30, 7, fill=(90, 90, 90), col=BLACK)
            ctext(d, cx, rowy[2] + 52, "すす 多", FT, RED)
        else:
            node(d, cx, rowy[2] + 26, 6, fill=(160, 160, 160), col=BLACK)
            ctext(d, cx, rowy[2] + 50, "すす 少", FT, BLUE)
    note(d, "高当量比は液滴の群燃焼で拡散火炎領域が増え, その領域ですすが多く生成")
    save(im, "t1e24SprayEquiv")


# 24-6 t1e24FlameIndex : フレームインデックス(勾配内積の符号)
def flame_index():
    im, d = new(); title(d, "フレームインデックス FI = grad(YF) . grad(YO2) の符号")
    # 左:同じ向き(内積正=予混合火炎片)
    box(d, 55, 95, 320, 360, (235, 244, 250), 2)
    ctext(d, 187, 120, "勾配が同じ向き", FS, BLUE)
    ox, oy = 130, 260
    arrow(d, ox, oy, ox + 90, oy - 55, BLUE, 4, 14)
    ctext(d, ox + 96, oy - 62, "grad YF", FT, BLUE, "lm")
    arrow(d, ox, oy + 22, ox + 78, oy - 26, GREEN, 4, 14)
    ctext(d, ox + 84, oy - 20, "grad YO2", FT, GREEN, "lm")
    ctext(d, 187, 330, "FI > 0 : 予混合火炎片", FS, BLUE)
    # 右:逆向き(内積負=拡散火炎片)
    box(d, 340, 95, 605, 360, (250, 236, 236), 2)
    ctext(d, 472, 120, "勾配が逆向き", FS, RED)
    ox2, oy2 = 472, 250
    arrow(d, ox2, oy2, ox2 - 80, oy2 - 45, BLUE, 4, 14)
    ctext(d, ox2 - 86, oy2 - 52, "grad YF", FT, BLUE, "rm")
    arrow(d, ox2, oy2, ox2 + 80, oy2 + 45, GREEN, 4, 14)
    ctext(d, ox2 + 86, oy2 + 52, "grad YO2", FT, GREEN, "lm")
    ctext(d, 472, 330, "FI < 0 : 拡散火炎片", FS, RED)
    note(d, "同じ向き(内積正)=予めよく混ざる=予混合, 逆向き(内積負)=拡散で出会う=拡散")
    save(im, "t1e24FlameIndex")


# 24-7 t1e24MixFracSpray : 混合分率の保存(ガス火炎) vs 非保存(噴霧火炎)
def mix_frac_spray():
    im, d = new(); title(d, "混合分率 Z : ガス火炎(保存) と 噴霧火炎(非保存)")
    # 左:ガス拡散火炎(気相のみ・保存)
    box(d, 55, 100, 320, 300, (235, 244, 250), 2)
    ctext(d, 187, 122, "ガス拡散火炎(気相のみ)", FT, BLUE)
    # 下流方向にZ一定
    arrow(d, 90, 200, 300, 200, GRAY, 2, 11); ctext(d, 300, 216, "下流 x", FT, GRAY, "rm")
    dashed(d, 90, 165, 300, 165, BLUE, 2, 8, 5)
    ctext(d, 195, 150, "Z 一定(保存量)", FT, BLUE)
    # 右:噴霧火炎(蒸発で気相へ供給・非保存)
    box(d, 340, 100, 605, 300, (250, 240, 232), 2)
    ctext(d, 472, 122, "噴霧火炎(液滴あり)", FT, RED)
    arrow(d, 375, 250, 590, 250, GRAY, 2, 11); ctext(d, 590, 266, "下流 x", FT, GRAY, "rm")
    # 液滴と蒸発矢印
    for dx in (400, 445, 490):
        node(d, dx, 210, 6, fill=(235, 235, 235), col=BLACK)
        arrow(d, dx, 205, dx, 185, ORANGE, 2, 8)
    ctext(d, 445, 172, "液滴から蒸発", FT, ORANGE)
    # Zが増加する上り曲線
    pts = [(375 + i * 2.1, 250 - (i / 100) * 55) for i in range(0, 101)]
    d.line(pts, fill=RED, width=3, joint="curve")
    ctext(d, 560, 195, "Z 増加", FT, RED, "lm")
    box(d, 55, 320, 605, 405, FILL1, 2)
    ctext(d, 330, 345, "ガス火炎 : 気相に燃料源なし -> Z は反応で不変(保存量)", FT, BLUE)
    ctext(d, 330, 378, "噴霧火炎 : 液滴蒸発が気相の燃料源 -> Z は下流で増加(非保存)", FT, RED)
    save(im, "t1e24MixFracSpray")


# 24-8 t1e24RadExtinction : ふく射考慮と失火の対比
def rad_extinction():
    im, d = new(); title(d, "噴霧噴流火炎 : ふく射考慮(失火) と 無視(高温) の対比")
    # 共通:左端中心から噴霧供給
    for panel, (y0, lab, col, ext) in enumerate([
            (100, "ふく射 考慮", RED, True),
            (270, "ふく射 無視", GREEN, False)]):
        box(d, 55, y0, 605, y0 + 130, "white", 2)
        ctext(d, 110, y0 + 16, lab, FT, col)
        cy = y0 + 78
        # ノズル/噴霧供給(左端中心)
        node(d, 80, cy, 5, fill=RED, col=RED)
        arrow(d, 85, cy, 130, cy, BLUE, 2, 10)
        # 火炎の高温域(細長い雫形)
        if ext:
            blob(d, 250, cy, 110, 30, (250, 226, 226), RED, 2)
            ctext(d, 250, cy, "温度 低", FT, RED)
            # 下流の失火(破線円)
            dashed_circle(d, 470, cy, 40, RED, 2)
            ctext(d, 470, cy, "失火", FT, RED)
            # 放熱矢印(火炎->周囲)
            for ax in (200, 300):
                arrow(d, ax, cy - 28, ax, cy - 52, ORANGE, 2, 9)
            ctext(d, 250, y0 + 20, "周囲空気 300K へ放熱", FT, ORANGE, "lm")
        else:
            blob(d, 330, cy, 200, 34, (250, 226, 226), RED, 2)
            ctext(d, 330, cy, "高温を保つ(失火なし)", FT, GREEN)
    note(d, "周囲空気(300K)が火炎より低温 -> ふく射で放熱 -> 温度低下 -> 下流で失火")
    save(im, "t1e24RadExtinction")


# 24-9 t1e24UnsteadyFlamelet : 定常/非定常フレームレットとNO予測
def unsteady_flamelet():
    im, d = new(); title(d, "混合分率 Z 上の 温度 と NO : 定常/非定常フレームレット")
    ox, oy, xl, yl = 100, 355, 470, 250
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "混合分率 Z", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T / NO 濃度", FT, BLACK, "rm")
    # 温度(山形・定常フレームレットと実測が一致)
    tpts = []
    for i in range(0, 201):
        t = i / 200
        v = 0.80 * math.exp(-((t - 0.42) / 0.22) ** 2)
        tpts.append((ox + t * xl, oy - v * yl))
    d.line(tpts, fill=BLACK, width=3, joint="curve")
    ctext(d, ox + 0.42 * xl, oy - 0.86 * yl, "温度 T(定常=実測で一致)", FT, BLACK)

    def nocurve(peak, cen=0.30, wid=0.16):
        return [(ox + (i / 200) * xl,
                 oy - peak * math.exp(-(((i / 200) - cen) / wid) ** 2) * yl)
                for i in range(0, 201)]
    # NO:実測(中)・定常(過大上振れ)・非定常(実測寄り)
    d.line(nocurve(0.66), fill=RED, width=3, joint="curve")     # 定常(過大)
    d.line(nocurve(0.40), fill=GREEN, width=3, joint="curve")   # 非定常
    d.line(nocurve(0.34), fill=BLUE, width=2, joint="curve")    # 実測
    ctext(d, ox + 0.30 * xl, oy - 0.72 * yl, "定常FL(NO 過大)", FT, RED)
    ctext(d, ox + 0.62 * xl, oy - 0.42 * yl, "非定常FL", FT, GREEN, "lm")
    ctext(d, ox + 0.62 * xl, oy - 0.30 * yl, "実測", FT, BLUE, "lm")
    note(d, "遅いNO反応を定常値で与える定常FLはNOを過大評価. 非定常FLが実測に近づく")
    save(im, "t1e24UnsteadyFlamelet")


# 24-10 t1e24RadNoPredict : 熱的NO生成速度の温度依存(exp)
def rad_no_predict():
    im, d = new(); title(d, "熱的NO 生成速度 ~ exp(-Ta/T) の急峻な温度依存")
    ox, oy, xl, yl = 110, 355, 460, 260
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "火炎温度 T", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "NO 生成速度", FT, BLACK, "rm")
    # 急峻な右上がり(指数)曲線
    pts = []
    for i in range(0, 201):
        t = 0.05 + 0.90 * i / 200
        v = math.exp(6.0 * (t - 0.95))   # 急上昇
        pts.append((ox + t * xl, oy - min(v, 1.0) * 0.9 * yl))
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # T2=2100K(考慮・低温側) と T1=2200K(無視・高温側)
    def height(t):
        return min(math.exp(6.0 * (t - 0.95)), 1.0) * 0.9 * yl
    t2, t1 = 0.72, 0.86
    for t, lab, col in [(t2, "T2=2100K(考慮)", GREEN), (t1, "T1=2200K(無視)", RED)]:
        xp = ox + t * xl
        yp = oy - height(t)
        node(d, xp, yp, 6, fill=col, col=col)
        dashed(d, xp, oy, xp, yp, LGRAY, 1, 6, 5)
        dashed(d, ox, yp, xp, yp, LGRAY, 1, 6, 5)
        ctext(d, xp, oy + 16, lab, FT, col)
    # 高さの差
    yp2 = oy - height(t2); yp1 = oy - height(t1)
    arrow(d, ox + 0.30 * xl, yp2, ox + 0.30 * xl, yp1, GRAY, 2, 10)
    ctext(d, ox + 0.30 * xl - 6, (yp1 + yp2) / 2, "差 大", FT, GRAY, "rm")
    note(d, "わずか100K低下でも指数依存でNO生成速度は約半分以下(考慮の方が低い)")
    save(im, "t1e24RadNoPredict")


# ============================================================
if __name__ == "__main__":
    eddy_dissipation()    # 24-1
    swirl_recirc()        # 24-2
    rans_ensemble()       # 24-3
    lifted_flame()        # 24-4
    spray_equiv()         # 24-5
    flame_index()         # 24-6
    mix_frac_spray()      # 24-7
    rad_extinction()      # 24-8
    unsteady_flamelet()   # 24-9
    rad_no_predict()      # 24-10
    print("done t1e ch24")
