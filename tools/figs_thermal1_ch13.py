# -*- coding: utf-8 -*-
"""熱流体力学1級 第13章「界面追跡・捕獲法」(混相流第5章) の図を描画。
問題図 t1e13*(19枚) と 公式・用語図 t1f13*(16枚) の計35枚。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐(□)回避のためギリシャ文字/特殊記号はプレーン表記に置換
(phi,kappa,rho,sigma,eps,delta,tau,Dx=Δx,Dt=Δt,grad=∇,sqrt=√,n_k 等)。
required(回答前)図には答え・正解値・結論を描かない。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- 共通ヘルパ ----
def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9, gap=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dash, L)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def grid(d, x0, y0, x1, y1, n, m=None, col=LGRAY, wd=1):
    """一様格子。n=横分割, m=縦分割(省略時=n)。"""
    m = n if m is None else m
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        d.line((xx, y0, xx, y1), fill=col, width=wd)
    for j in range(m + 1):
        yy = y0 + (y1 - y0) * j / m
        d.line((x0, yy, x1, yy), fill=col, width=wd)


def panel(d, x0, y0, x1, y1, label="", col=GRAY, fill=None):
    if fill:
        d.rectangle((x0, y0, x1, y1), outline=col, width=2, fill=fill)
    else:
        d.rectangle((x0, y0, x1, y1), outline=col, width=2)
    if label:
        ctext(d, (x0 + x1) / 2, y0 - 14, label, FT, col)


# ============================================================
# 問題図 t1e13*  (19枚)
# ============================================================

# 5-1 t1e13CaptureVsTrack : 界面捕獲法 vs 界面追跡法 (helpful)
def CaptureVsTrack():
    im, d = new(); title(d, "界面捕獲法 と 界面追跡法 (どちらも固定格子)")
    # 左: 捕獲法 = 固定格子に関数phiの値、phi一定=界面
    gx0, gy0, gx1, gy1 = 60, 90, 300, 300
    grid(d, gx0, gy0, gx1, gy1, 6)
    # phi一定の等値線(界面)を曲線で
    pts = [(gx0 + (gx1 - gx0) * i / 40,
            gy0 + 105 + 60 * math.sin(math.pi * i / 40 - 0.4)) for i in range(41)]
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, 180, 78, "界面捕獲法", FS, RED)
    ctext(d, 180, 314, "固定格子上に関数 phi", FT, GRAY)
    ctext(d, 180, 332, "phi 一定 = 界面(赤線)", FT, GRAY)
    # 右: 追跡法 = 固定格子に界面要素(マーカー)を並べる
    hx0, hy0, hx1, hy1 = 360, 90, 600, 300
    grid(d, hx0, hy0, hx1, hy1, 6)
    mk = [(hx0 + (hx1 - hx0) * i / 8,
           hy0 + 105 + 60 * math.sin(math.pi * (i / 8) - 0.4)) for i in range(9)]
    for i in range(len(mk) - 1):
        d.line((mk[i][0], mk[i][1], mk[i + 1][0], mk[i + 1][1]), fill=BLUE, width=3)
    for p in mk:
        node(d, p[0], p[1], 5, fill=BLUE, col=BLUE)
    ctext(d, 480, 78, "界面追跡法(Front Tracking)", FT, BLUE)
    ctext(d, 480, 314, "固定格子上に界面要素(線素)", FT, GRAY)
    ctext(d, 480, 332, "マーカーの運動を追う", FT, GRAY)
    note(d, "いずれも格子は固定。捕獲=関数phiの分布 / 追跡=界面マーカー")
    save(im, "t1e13CaptureVsTrack")


# 5-2 t1e13VofVsLevelSet : VOF(体積存在率) vs Level Set(距離関数) (helpful)
def VofVsLevelSet():
    im, d = new(); title(d, "VOF法(体積率 F) と Level Set法(距離関数 phi)")
    # 左: VOF 各セルにF値
    gx0, gy0, gx1, gy1 = 60, 95, 300, 295
    grid(d, gx0, gy0, gx1, gy1, 5)
    Fv = [[0, 0, 0, 0.2, 0.9],
          [0, 0, 0.3, 0.9, 1],
          [0, 0.3, 0.9, 1, 1],
          [0.2, 0.9, 1, 1, 1],
          [0.9, 1, 1, 1, 1]]
    cw = (gx1 - gx0) / 5; ch = (gy1 - gy0) / 5
    for r in range(5):
        for c in range(5):
            v = Fv[r][c]
            g = int(255 - v * 120)
            d.rectangle((gx0 + c * cw + 1, gy0 + r * ch + 1,
                         gx0 + (c + 1) * cw - 1, gy0 + (r + 1) * ch - 1), fill=(g, g, g))
            ctext(d, gx0 + c * cw + cw / 2, gy0 + r * ch + ch / 2,
                  ("1" if v == 1 else ("0" if v == 0 else "%.1f" % v)), FT,
                  RED if 0 < v < 1 else GRAY)
    grid(d, gx0, gy0, gx1, gy1, 5)
    ctext(d, 180, 82, "VOF: 体積存在率 F (0..1)", FT, RED)
    ctext(d, 180, 312, "F=0.5 付近を界面とみなす", FT, GRAY)
    # 右: Level Set 符号付き距離の等高線
    hx0, hy0, hx1, hy1 = 360, 95, 600, 295
    d.rectangle((hx0, hy0, hx1, hy1), outline=LGRAY, width=1)
    cx, cy = 505, 200
    for k, r in enumerate([25, 50, 75, 100]):
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=GRAY, width=1)
    d.ellipse((cx - 50, cy - 40, cx + 50, cy + 40), outline=RED, width=3)
    ctext(d, cx, cy, "phi<0", FT, BLUE)
    ctext(d, cx + 78, cy - 60, "phi>0", FT, GREEN)
    ctext(d, cx, cy + 46, "phi=0 界面", FT, RED)
    ctext(d, 480, 82, "Level Set: 符号付き距離 phi", FT, BLUE)
    ctext(d, 480, 312, "phi=0 が界面 / 内外で正負", FT, GRAY)
    note(d, "どちらも固定格子上で変数(F または phi)を移流させる")
    save(im, "t1e13VofVsLevelSet")


# 5-3 t1e13ALE : ALE法の格子移動 (helpful)
def ALE():
    im, d = new(); title(d, "ALE法: 格子速度を流体と独立に定める")
    # 主図: 移動界面に沿う格子は追従、遠方は緩やか
    gx0, gy0, gx1, gy1 = 70, 90, 590, 260
    # 界面曲線
    def iface(x):
        t = (x - gx0) / (gx1 - gx0)
        return gy0 + 70 + 34 * math.sin(math.pi * t)
    # 縦線(界面に沿って上側を追従移動)
    for i in range(11):
        xx = gx0 + (gx1 - gx0) * i / 10
        d.line((xx, gy0, xx, gy1), fill=LGRAY, width=1)
    # 横線: 界面近傍は界面形状に沿い、遠方は水平
    for j in range(5):
        pts = []
        for i in range(53):
            xx = gx0 + (gx1 - gx0) * i / 52
            base = gy0 + (gy1 - gy0) * j / 4
            infl = (iface(xx) - (gy0 + 105)) * (1 - j / 4) * 0.8
            pts.append((xx, base + infl))
        plot(d, 0, 0, pts, LGRAY, 1)
    ipts = [(gx0 + (gx1 - gx0) * i / 52, iface(gx0 + (gx1 - gx0) * i / 52)) for i in range(53)]
    plot(d, 0, 0, ipts, RED, 3)
    ctext(d, 330, 78, "移動界面(赤)に格子が追従、遠方は変形を抑える", FT, RED)
    # 格子移動の矢印
    for i in (2, 5, 8):
        xx = gx0 + (gx1 - gx0) * i / 10
        arrow(d, xx, gy0 + 108, xx, gy0 + 88, GREEN, 2, 8)
    # 下部: 3つの位置づけ
    ctext(d, 150, 300, "純ラグランジュ", FT, GRAY)
    ctext(d, 150, 320, "格子が極端変形", FT, GRAY)
    ctext(d, 330, 300, "ALE(任意)", FS, GREEN)
    ctext(d, 330, 320, "中間・変形を抑制", FT, GREEN)
    ctext(d, 520, 300, "オイラー", FT, GRAY)
    ctext(d, 520, 320, "固定格子", FT, GRAY)
    note(d, "格子移動速度を流体速度と独立に選べる(Arbitrary=任意)")
    save(im, "t1e13ALE")


# 5-4 t1e13CellsPerBubble : 気泡径あたりのセル数 (required・答え書かない)
def CellsPerBubble():
    im, d = new(); title(d, "気泡径 d を計算格子(格子幅 Dx)で解像する")
    # 一様格子に球形気泡
    gx0, gy0, gx1, gy1 = 120, 80, 540, 320
    n = 14
    grid(d, gx0, gy0, gx1, gy1, n)
    cx, cy = (gx0 + gx1) / 2, (gy0 + gy1) / 2
    R = 108
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLUE, width=3)
    ctext(d, cx, cy, "気泡", FT, BLUE)
    # 直径寸法
    dim(d, cx - R, cy, cx + R, cy, "d (等価直径)", col=GRAY)
    # 格子幅寸法
    cw = (gx1 - gx0) / n
    dim(d, gx0, gy1 + 22, gx0 + cw, gy1 + 22, "Dx", col=GRAY)
    ctext(d, cx, gy1 + 46, "等価直径 d を格子幅 Dx のセルで割ると横切るセル数", FT, GRAY)
    ctext(d, cx, gy1 + 66, "上昇速度を精度良く解くには十分なセル数が必要", FT, GRAY)
    note(d, "セル数 = d / Dx。細かい格子(小さいDx)ほどセル数は増える")
    save(im, "t1e13CellsPerBubble")


# 5-5 t1e13InterfaceThickness : 界面厚さの違い (helpful)
def InterfaceThickness():
    im, d = new(); title(d, "界面厚さ: 境界適合格子法(零) と Front Tracking(有限)")
    # 左: 厚さ零の鋭い界面
    gx0, gy0, gx1, gy1 = 60, 100, 300, 300
    grid(d, gx0, gy0, gx1, gy1, 6)
    xm = (gx0 + gx1) / 2
    d.line((xm, gy0, xm, gy1), fill=RED, width=4)
    ctext(d, 180, 88, "境界適合格子法", FT, RED)
    ctext(d, 180, 314, "界面厚さ = 零(鋭い線)", FT, GRAY)
    # 右: 4セル程度に密度/粘性を滑らかに遷移
    hx0, hy0, hx1, hy1 = 360, 100, 600, 300
    grid(d, hx0, hy0, hx1, hy1, 6)
    xm2 = (hx0 + hx1) / 2
    band = (hx1 - hx0) / 6 * 2  # 4セル分の帯 ≒ ±2セル
    for i in range(int(-band), int(band), 3):
        g = int(150 + 90 * abs(i) / band)
        d.line((xm2 + i, hy0, xm2 + i, hy1), fill=(g, g, g), width=3)
    dashed(d, xm2 - band, hy0, xm2 - band, hy1, GRAY, 1)
    dashed(d, xm2 + band, hy0, xm2 + band, hy1, GRAY, 1)
    ctext(d, 480, 88, "Front Tracking", FT, BLUE)
    ctext(d, 480, 314, "近傍4セル程度で密度/粘性を遷移", FT, GRAY)
    ctext(d, 480, 332, "= 4格子程度の有限厚さ", FT, GRAY)
    note(d, "境界適合=厚さ零 / Front Tracking=有限厚さ(4格子程度)")
    save(im, "t1e13InterfaceThickness")


# 5-6 t1e13CaptureErrors : 界面捕獲法の誤差要因3つ (helpful)
def CaptureErrors():
    im, d = new(); title(d, "界面捕獲法の誤差要因")
    # (1) クーラン数大で界面が崩れる
    panel(d, 55, 95, 245, 255, "(1) クーラン数 大")
    grid(d, 60, 100, 240, 250, 5)
    pts = [(60 + 180 * i / 30, 175 + 30 * math.sin(2 * math.pi * i / 8)) for i in range(31)]
    plot(d, 0, 0, pts, RED, 2)
    ctext(d, 150, 270, "界面が崩れる", FT, GRAY)
    # (2) 密度比大で速度/圧力が振動
    panel(d, 255, 95, 405, 255, "(2) 密度比 大")
    ox, oy = 265, 230
    axes(d, ox, oy, 130, 110, "x", "u,p")
    zz = [(ox + 130 * i / 40, oy - 55 - 40 * math.sin(2 * math.pi * i / 6) * (0.5 + 0.5 * i / 40)) for i in range(41)]
    plot(d, 0, 0, zz, BLUE, 2)
    ctext(d, 330, 270, "速度/圧力が振動", FT, GRAY)
    # (3) 多次元で数値拡散(ぼやけ)
    panel(d, 415, 95, 605, 255, "(3) 多次元")
    grid(d, 420, 100, 600, 250, 5)
    cx, cy = 510, 175
    for k, r in enumerate([20, 30, 40]):
        g = 120 + k * 45
        d.ellipse((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), outline=(g, g, g), width=2)
    ctext(d, 510, 270, "界面がぼやける(数値拡散)", FT, GRAY)
    note(d, "体積保存にはソレノイダル条件と適切な移流計算が要る")
    save(im, "t1e13CaptureErrors")


# 5-7 t1e13BubbleNucleation : 4対象と連続体スケールで扱えるか (helpful)
def BubbleNucleation():
    im, d = new(); title(d, "界面追跡・捕獲法(連続体スケール)で扱える対象")
    # (A) 加熱平板で気泡核が無から発生
    panel(d, 55, 95, 245, 250, "(A) 気泡核生成")
    hwall(d, 70, 230, 230, 245)
    for cx in (110, 150, 190):
        d.ellipse((cx - 5, 218, cx + 5, 228), outline=BLUE, width=2)
    ctext(d, 150, 200, "無 -> 気泡核", FT, GRAY)
    ctext(d, 150, 264, "分子スケール", FT, RED)
    # (B) 傾斜平板の液膜表面波
    panel(d, 255, 95, 405, 250, "(B) 液膜表面波")
    d.line((262, 235, 398, 210), fill=BLACK, width=3)
    wv = [(262 + 130 * i / 40, 205 - 25 * i / 40 - 7 * math.sin(2 * math.pi * i / 8)) for i in range(41)]
    plot(d, 0, 0, wv, BLUE, 2)
    ctext(d, 330, 264, "連続体で可", FT, GREEN)
    # (C) 上昇単一気泡の終端形状
    panel(d, 415, 95, 500, 250, "(C) 単一気泡")
    d.ellipse((435, 195, 480, 225), outline=BLUE, width=2)
    arrow(d, 457, 190, 457, 150, GRAY, 2, 8)
    ctext(d, 457, 264, "可", FT, GREEN)
    # (D) 液滴衝突後の王冠
    panel(d, 510, 95, 605, 250, "(D) 王冠状液膜")
    d.arc((520, 200, 595, 250), 180, 360, fill=BLUE, width=2)
    for xx in (528, 545, 562, 579):
        d.line((xx, 220, xx, 200), fill=BLUE, width=2)
    ctext(d, 557, 264, "可", FT, GREEN)
    note(d, "界面が無から生じる現象は連続体スケールでは原理的に困難")
    save(im, "t1e13BubbleNucleation")


# 5-8 t1e13AdvectionSchemes : 移流方程式の数値解法対比 (helpful)
def AdvectionSchemes():
    im, d = new(); title(d, "移流方程式の数値解法 (矩形波を移流)")
    labs = [("FTCS(中心+陽)", 55, RED, "osc"),
            ("TVD(振動抑制)", 205, GREEN, "tvd"),
            ("CIP(補間)", 355, BLUE, "cip"),
            ("ラグランジュ(粒子)", 505, GRAY, "lag")]
    for lab, x0, col, kind in labs:
        ox, oy = x0, 250
        axes(d, ox, oy, 120, 110, "x", "")
        # 元の矩形波(点線)
        base = oy - 70
        dashed(d, ox + 30, oy, ox + 30, base, LGRAY, 1)
        dashed(d, ox + 30, base, ox + 70, base, LGRAY, 1)
        dashed(d, ox + 70, base, ox + 70, oy, LGRAY, 1)
        if kind == "osc":
            pts = [(ox + 5 + 115 * i / 60, oy - (70 if 0.35 < i / 60 < 0.62 else 0)
                    - 30 * math.sin(2 * math.pi * i / 5) * (1 if 0.2 < i / 60 < 0.8 else 0)) for i in range(61)]
            plot(d, 0, 0, pts, col, 2)
        elif kind == "tvd":
            plot(d, 0, 0, [(ox + 40, oy), (ox + 48, base), (ox + 80, base), (ox + 88, oy)], col, 2)
        elif kind == "cip":
            plot(d, 0, 0, [(ox + 42, oy), (ox + 45, base), (ox + 82, base), (ox + 85, oy)], col, 2)
        else:
            for xx in (ox + 45, ox + 58, ox + 71, ox + 84):
                node(d, xx, base, 3, fill=col, col=col)
            arrow(d, ox + 90, base - 14, ox + 108, base - 14, col, 2, 7)
        ctext(d, ox + 60, 285, lab, FT, col)
    note(d, "FTCSは振動・発散して不適切 / TVD・CIP・ラグランジュは安定に解ける")
    save(im, "t1e13AdvectionSchemes")


# 5-9 t1e13PhaseIndicator : 相関数X_k (required・答え書かない)
def PhaseIndicator():
    im, d = new(); title(d, "相関数 X_k と界面のデルタ関数")
    # 左: k相=1, 他相=0 の領域分け
    gx0, gy0, gx1, gy1 = 60, 95, 300, 295
    d.rectangle((gx0, gy0, gx1, gy1), outline=BLACK, width=2)
    # 界面曲線
    def iface(y):
        t = (y - gy0) / (gy1 - gy0)
        return gx0 + 150 + 45 * math.sin(math.pi * t)
    ipts = [(iface(gy0 + (gy1 - gy0) * j / 40), gy0 + (gy1 - gy0) * j / 40) for j in range(41)]
    # k相側を淡色
    poly = [(gx0, gy0)] + ipts + [(gx0, gy1)]
    d.polygon(poly, fill=(228, 236, 250))
    plot(d, 0, 0, ipts, RED, 3)
    ctext(d, 110, 130, "k相", FS, BLUE)
    ctext(d, 110, 155, "X_k = 1", FT, BLUE)
    ctext(d, 265, 130, "他相", FS, GRAY)
    ctext(d, 265, 155, "X_k = 0", FT, GRAY)
    # 外向き単位法線 n_k
    my = (gy0 + gy1) / 2; mx = iface(my)
    arrow(d, mx, my, mx + 46, my, GREEN, 3, 11)
    ctext(d, mx + 60, my - 14, "n_k", FT, GREEN)
    ctext(d, mx, gy1 + 16, "界面 x_i", FT, RED)
    # 右: 段階関数プロファイルと界面上に立つデルタ
    ox, oy = 360, 210
    axes(d, ox, oy, 210, 130, "位置", "X_k")
    step = oy - 90
    plot(d, 0, 0, [(ox, step), (ox + 95, step), (ox + 95, oy), (ox + 210, oy)], BLUE, 3)
    ctext(d, ox + 45, step - 12, "1", FT, BLUE)
    ctext(d, ox + 155, oy - 12, "0", FT, GRAY)
    # デルタ(界面位置=段差の所)
    arrow(d, ox + 95, oy, ox + 95, oy - 118, ORANGE, 3, 11)
    ctext(d, ox + 130, oy - 108, "delta(x-x_i)", FT, ORANGE)
    ctext(d, ox + 95, oy + 18, "界面", FT, RED)
    note(d, "X_k は界面で 1->0 の段階関数、勾配は界面上のみに立つデルタ関数")
    save(im, "t1e13PhaseIndicator")


# 5-10 t1e13LevelSetCurvature : 界面追跡方程式と平均曲率 (helpful)
def LevelSetCurvature():
    im, d = new(); title(d, "界面追跡方程式と平均曲率 kappa = -grad . n")
    # phi=一定の界面曲線
    cx, cy = 300, 220
    R = 120
    d.arc((cx - R, cy - R, cx + R, cy + R), 200, 340, fill=RED, width=3)
    ctext(d, cx, cy + 40, "phi = 一定 (界面)", FT, RED)
    # 単位法線 n = grad phi/|grad phi|
    for ang in (250, 270, 290):
        a = math.radians(ang)
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        arrow(d, px, py, px + 42 * math.cos(a), py + 42 * math.sin(a), GREEN, 2, 9)
    ctext(d, cx, cy + R + 46, "n = grad phi / |grad phi|", FT, GREEN)
    # 移流速度u
    arrow(d, cx - 150, cy - 40, cx - 90, cy - 40, BLUE, 3, 11)
    ctext(d, cx - 120, cy - 58, "u", FT, BLUE)
    ctext(d, cx - 120, cy - 20, "移流", FT, BLUE)
    # 注記
    ctext(d, W / 2, 330, "追跡: dphi/dt + u . grad phi = 0", FT, GRAY)
    ctext(d, W / 2, 352, "曲率 kappa=-grad.n はスカラー(再初期化式とは別物)", FT, GRAY)
    note(d, "法線の発散が平均曲率 kappa。表面張力 sigma*kappa の計算に使う")
    save(im, "t1e13LevelSetCurvature")


# 5-11 t1e13SmoothedDelta : 平滑化ヘビサイドとデルタ (helpful・ピーク値は書かない)
def SmoothedDelta():
    im, d = new(); title(d, "平滑化ヘビサイド H_eps と 平滑化デルタ delta_eps")
    # 上: H_eps のS字
    ox, oy = 120, 175
    axes(d, ox, oy, 420, 90, "phi", "H_eps")
    xm = ox + 210
    pts = []
    for i in range(121):
        t = i / 120
        phi = (t - 0.5) * 2  # -1..1 を |phi|<eps に対応
        y = oy - 45 - 40 * (0.5 * (phi + (1 / math.pi) * math.sin(math.pi * phi)))
        pts.append((ox + 420 * t, y))
    plot(d, 0, 0, pts, BLUE, 3)
    dashed(d, xm, oy, xm, oy - 88, LGRAY, 1)
    ctext(d, xm, oy + 16, "phi=0", FT, GRAY)
    ctext(d, ox + 60, oy - 80, "|phi|>=eps で 一定", FT, GRAY)
    # 下: delta_eps 釣鐘
    ox2, oy2 = 120, 370
    axes(d, ox2, oy2, 420, 100, "phi", "delta_eps")
    pts2 = []
    for i in range(121):
        t = i / 120
        phi = (t - 0.5) * 2
        if abs(phi) < 1:
            y = oy2 - 10 - 80 * 0.5 * (1 + math.cos(math.pi * phi))
        else:
            y = oy2
        pts2.append((ox2 + 420 * t, y))
    plot(d, 0, 0, pts2, RED, 3)
    ctext(d, ox2 + 210, oy2 - 100, "phi=0 でピーク", FT, RED)
    ctext(d, ox2 + 360, oy2 - 10, "|phi|>=eps で 0", FT, GRAY)
    ctext(d, W - 20, 150, "delta_eps = dH_eps/dphi", FT, GRAY, "rm")
    save(im, "t1e13SmoothedDelta")


# 5-12 t1e13DirectSimulation : 平均化モデル vs 直接解法 (helpful)
def DirectSimulation():
    im, d = new(); title(d, "平均化モデル と 直接解法(界面追跡・捕獲法)")
    # 左: 平均化モデル
    panel(d, 55, 95, 320, 300, "平均化モデル", BLUE)
    d.rectangle((80, 130, 295, 270), outline=LGRAY, width=1)
    # ぼんやりした分布(界面を陽に追わない)
    for k, r in enumerate([30, 55, 80]):
        g = 150 + k * 35
        d.ellipse((187 - r, 200 - r * 0.6, 187 + r, 200 + r * 0.6), outline=(g, g, g), width=2)
    ctext(d, 187, 285, "界面を陽に追わず平均量", FT, GRAY)
    ctext(d, 187, 118, "相間相互作用=相関式", FT, BLUE)
    # 右: 直接解法
    panel(d, 340, 95, 605, 300, "直接解法", RED)
    grid(d, 365, 130, 580, 270, 5)
    ipts = [(365 + 215 * i / 40, 175 + 45 * math.sin(math.pi * i / 40 - 0.3)) for i in range(41)]
    plot(d, 0, 0, ipts, RED, 3)
    ctext(d, 472, 285, "界面を陽に表し跳躍条件を課す", FT, GRAY)
    ctext(d, 472, 118, "瞬時局所の基礎式を直接解く", FT, RED)
    note(d, "固定格子で VOF / Level Set / Front Tracking を用いる")
    save(im, "t1e13DirectSimulation")


# 5-13 t1e13DampedOscillation : 液滴の減衰振動->球形 (required・答え書かない)
def DampedOscillation():
    im, d = new(); title(d, "液滴の減衰振動: 界面張力で球形へ近づく")
    # 左: 楕円
    cx, cy = 165, 210
    d.ellipse((cx - 55, cy - 95, cx + 55, cy + 95), outline=BLUE, width=3)
    ctext(d, cx, cy, "液滴", FT, BLUE)
    ctext(d, cx, 320, "初期: 変形(楕円体)", FT, GRAY)
    # 中間の矢印
    arrow(d, 250, 210, 400, 210, GRAY, 3, 13)
    ctext(d, 325, 190, "界面張力で減衰振動", FT, GRAY)
    # 右: 球
    cx2, cy2 = 500, 210
    d.ellipse((cx2 - 80, cy2 - 80, cx2 + 80, cy2 + 80), outline=BLUE, width=3)
    dim(d, cx2, cy2, cx2 + 80, cy2, "R", col=GRAY)
    ctext(d, cx2, 320, "終期: 半径 R の球形", FT, GRAY)
    ctext(d, W / 2, 348, "液滴と周囲は等密度 rho・等粘度、格子幅 Dx、界面は幅 4Dx で平滑化", FT, GRAY)
    note(d, "非定常項と表面張力項でクーラン数を見積る(数値は各自計算)")
    save(im, "t1e13DampedOscillation")


# 5-14 t1e13HeightFunction : VOF高さ関数による曲率評価 (helpful)
def HeightFunction():
    im, d = new(); title(d, "VOF 高さ関数 H^y による曲率評価 (|n_y|>|n_x|)")
    gx0, gy0, gx1, gy1 = 90, 90, 470, 320
    n = 7
    grid(d, gx0, gy0, gx1, gy1, n)
    cw = (gx1 - gx0) / n
    # 界面曲線 y=H^y(x)
    def hy(x):
        t = (x - gx0) / (gx1 - gx0)
        return gy0 + 150 + 55 * math.cos(math.pi * (t - 0.5))
    # 各列で下からF積み上げ(淡色)
    for c in range(n):
        xL = gx0 + c * cw
        top = hy(xL + cw / 2)
        d.rectangle((xL + 1, top, xL + cw - 1, gy1 - 1), fill=(225, 233, 248))
    ipts = [(gx0 + (gx1 - gx0) * i / 60, hy(gx0 + (gx1 - gx0) * i / 60)) for i in range(61)]
    plot(d, 0, 0, ipts, RED, 3)
    ctext(d, (gx0 + gx1) / 2, gy1 + 18, "各列で F を y方向に積み上げ = H^y(x)", FT, GRAY)
    # 法線
    mx = (gx0 + gx1) / 2
    arrow(d, mx, hy(mx), mx, hy(mx) - 40, GREEN, 2, 9)
    ctext(d, mx + 40, hy(mx) - 30, "n (|n_y|>|n_x|)", FT, GREEN)
    # 右注記
    ctext(d, 560, 150, "曲率は", FT, GRAY)
    ctext(d, 560, 175, "H^y の 1階・2階", FT, GRAY)
    ctext(d, 560, 200, "微分から評価", FT, GRAY)
    ctext(d, 560, 235, "|kappa| =", FT, BLACK)
    ctext(d, 560, 258, "|H''| / (1+H'^2)^{3/2}", FT, BLACK)
    note(d, "界面が主にx方向に伸びる向きは H^y を x で微分して曲率を得る")
    save(im, "t1e13HeightFunction")


# 5-15 t1e13Reinitialization : 再初期化 (helpful)
def Reinitialization():
    im, d = new(); title(d, "再初期化: |grad phi|=1 の距離関数性を回復")
    # 左: 移流後、等高線間隔が不均一
    hx0, hy0, hx1, hy1 = 60, 100, 300, 300
    d.rectangle((hx0, hy0, hx1, hy1), outline=LGRAY, width=1)
    cx, cy = 180, 200
    for r in [22, 38, 60, 90, 128]:
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=GRAY, width=1)
    d.ellipse((cx - 38, cy - 30, cx + 38, cy + 30), outline=RED, width=3)
    ctext(d, 180, 88, "移流後 (|grad phi| != 1)", FT, GRAY)
    ctext(d, 180, 314, "等高線間隔が不均一", FT, GRAY)
    # 矢印
    arrow(d, 310, 200, 350, 200, BLACK, 3, 12)
    ctext(d, 330, 178, "tau", FT, GRAY)
    # 右: 等間隔
    hx0, hy0, hx1, hy1 = 360, 100, 600, 300
    d.rectangle((hx0, hy0, hx1, hy1), outline=LGRAY, width=1)
    cx, cy = 480, 200
    for r in [30, 55, 80, 105]:
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=GRAY, width=1)
    d.ellipse((cx - 30, cy - 24, cx + 30, cy + 24), outline=RED, width=3)
    ctext(d, 480, 88, "再初期化後 (|grad phi|=1)", FT, GRAY)
    ctext(d, 480, 314, "等間隔=符号付き距離", FT, GRAY)
    note(d, "擬似時間 tau で界面(phi=0)位置は保ったまま距離関数性を回復")
    save(im, "t1e13Reinitialization")


# 5-16 t1e13CsfStability : CSF表面張力波の陽解法安定条件 (helpful・式書かない)
def CsfStability():
    im, d = new(); title(d, "CSF: 表面張力波が1ステップで1セルを越えない条件")
    # 界面セルに体積力
    gx0, gy0, gx1, gy1 = 90, 100, 570, 250
    n = 12
    grid(d, gx0, gy0, gx1, gy1, n, 3)
    cw = (gx1 - gx0) / n
    # 界面(毛管波)
    wv = [(gx0 + (gx1 - gx0) * i / 60,
           (gy0 + gy1) / 2 - 26 * math.sin(2 * math.pi * i / 30)) for i in range(61)]
    plot(d, 0, 0, wv, RED, 3)
    # 界面を含むセルに体積力矢印
    for c in range(1, n, 2):
        xx = gx0 + c * cw + cw / 2
        yy = (gy0 + gy1) / 2 - 26 * math.sin(2 * math.pi * (c / n))
        arrow(d, xx, yy, xx, yy - 22, ORANGE, 2, 8)
    ctext(d, (gx0 + gx1) / 2, 84, "界面セルに表面張力を体積力(橙)として付与", FT, ORANGE)
    # 波の伝播とセル
    ctext(d, (gx0 + gx1) / 2, 275, "毛管波(表面張力波)が伝播", FT, RED)
    dim(d, gx0, gy1 + 40, gx0 + cw, gy1 + 40, "Dx", col=GRAY)
    arrow(d, gx0 + 3 * cw, gy1 + 40, gx0 + 4 * cw, gy1 + 40, BLUE, 2, 9)
    ctext(d, gx0 + 3.5 * cw, gy1 + 62, "1ステップ Dt で 1セル以内", FT, BLUE, "lm")
    note(d, "陽解法では波が1ステップで1セルを越えない条件が時間刻みを縛る")
    save(im, "t1e13CsfStability")


# 5-17 t1e13CahnHilliard : 拡散界面モデル (helpful)
def CahnHilliard():
    im, d = new(); title(d, "Phase Field法(拡散界面): 秩序変数 phi と二重井戸")
    # 左: phi の滑らかな遷移プロファイル
    ox, oy = 70, 250
    axes(d, ox, oy, 240, 150, "位置", "phi")
    pts = []
    for i in range(121):
        t = i / 120
        y = oy - 20 - 110 * (0.5 * (1 + math.tanh((t - 0.5) * 8)))
        pts.append((ox + 240 * t, y))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 60, oy - 130, "+1", FT, BLUE)
    ctext(d, ox + 200, oy - 20, "-1", FT, BLUE)
    ctext(d, ox + 120, oy + 20, "有限幅で滑らかに遷移", FT, GRAY)
    # 右: 二重井戸ポテンシャル f(phi)
    ox2, oy2 = 360, 250
    axes(d, ox2, oy2, 230, 150, "phi", "f(phi)")
    pw = []
    for i in range(121):
        t = i / 120
        phi = (t - 0.5) * 2.4
        y = oy2 - 20 - 100 * ((phi * phi - 1) ** 2) / 1.5
        pw.append((ox2 + 230 * t, max(y, oy2 - 145)))
    plot(d, 0, 0, pw, RED, 3)
    ctext(d, ox2 + 115, oy2 - 130, "二重井戸ポテンシャル", FT, RED)
    ctext(d, W / 2, 330, "右辺 第1項=バルクエネルギー / 第2項=界面エネルギー", FT, GRAY)
    ctext(d, W / 2, 352, "Cahn-Hilliard=保存型 / Allen-Cahn=非保存型(相変化)", FT, GRAY)
    note(d, "熱力学的に自由エネルギーを phi で記述し界面を有限幅で扱う")
    save(im, "t1e13CahnHilliard")


# 5-18 t1e13InterfaceReconstruction : 界面再構成 SLIC/PLIC と CSF別系統 (helpful)
def InterfaceReconstruction():
    im, d = new(); title(d, "界面再構成: 体積率 F から界面を復元")
    # 左: SLIC 階段状
    gx0, gy0, gx1, gy1 = 60, 100, 250, 290
    grid(d, gx0, gy0, gx1, gy1, 4)
    cw = (gx1 - gx0) / 4; chh = (gy1 - gy0) / 4
    # 階段状界面
    stair = [(gx0, gy0 + chh), (gx0 + cw, gy0 + chh), (gx0 + cw, gy0 + 2 * chh),
             (gx0 + 2 * cw, gy0 + 2 * chh), (gx0 + 2 * cw, gy0 + 3 * chh),
             (gx0 + 3 * cw, gy0 + 3 * chh), (gx0 + 3 * cw, gy1), (gx1, gy1)]
    for i in range(len(stair) - 1):
        d.line((stair[i][0], stair[i][1], stair[i + 1][0], stair[i + 1][1]), fill=RED, width=3)
    ctext(d, 155, 88, "SLIC (階段状)", FT, RED)
    # 中: PLIC 区分的線分
    hx0, hy0, hx1, hy1 = 270, 100, 460, 290
    grid(d, hx0, hy0, hx1, hy1, 4)
    cw2 = (hx1 - hx0) / 4; ch2 = (hy1 - hy0) / 4
    seg = [((hx0, hy0 + ch2 * 1.2), (hx0 + cw2, hy0 + ch2 * 1.7)),
           ((hx0 + cw2, hy0 + ch2 * 1.7), (hx0 + 2 * cw2, hy0 + ch2 * 2.3)),
           ((hx0 + 2 * cw2, hy0 + ch2 * 2.3), (hx0 + 3 * cw2, hy0 + ch2 * 3.0)),
           ((hx0 + 3 * cw2, hy0 + ch2 * 3.0), (hx1, hy0 + ch2 * 3.5))]
    for a, b in seg:
        d.line((a[0], a[1], b[0], b[1]), fill=BLUE, width=3)
    ctext(d, 365, 88, "PLIC (区分的線分)", FT, BLUE)
    # 右: CSF 別系統
    panel(d, 485, 110, 605, 280, "CSF (別系統)", GRAY)
    ctext(d, 545, 150, "表面張力を", FT, GRAY)
    ctext(d, 545, 172, "体積力として", FT, GRAY)
    ctext(d, 545, 194, "与えるモデル", FT, GRAY)
    for yy in (225, 245, 265):
        arrow(d, 510, yy, 580, yy, ORANGE, 2, 8)
    note(d, "SLIC/PLIC/MARS=界面再構成 / CSF=表面張力の与え方で系統が異なる")
    save(im, "t1e13InterfaceReconstruction")


# 5-19 t1e13JumpCondition : 跳躍条件と関与因子 (helpful)
def JumpCondition():
    im, d = new(); title(d, "気液界面の跳躍条件: 物理量が不連続に跳ぶ")
    xm = 330
    d.line((xm, 90, xm, 300), fill=RED, width=4)
    ctext(d, xm, 78, "気液界面", FT, RED)
    ctext(d, 150, 110, "気相", FS, BLUE)
    ctext(d, 510, 110, "液相", FS, GREEN)
    # 圧力/速度/応力の跳び(段差)
    ox, oy = 90, 260
    for k, (lab, jump, col) in enumerate([("圧力 p", 40, BLUE), ("速度", 25, GREEN)]):
        yb = 150 + k * 70
        d.line((110, yb, xm, yb), fill=col, width=2)
        d.line((xm, yb - jump, 560, yb - jump), fill=col, width=2)
        dashed(d, xm, yb, xm, yb - jump, col, 1)
        ctext(d, 130, yb - 14, lab, FT, col, "lm")
    ctext(d, xm + 60, 165, "跳び(不連続)", FT, GRAY, "lm")
    # 関与因子(界面上に配置)
    ctext(d, xm, 320, "表面張力(ラプラス圧) / 蒸発凝縮 / 粘性応力 のつり合い", FT, GRAY)
    # 密度比は別枠
    panel(d, 430, 328, 640, 366, "", GRAY)
    ctext(d, 535, 347, "密度比=両相の物性(別)", FT, GRAY)
    note(d, "跳躍条件は界面での力学的・熱的つり合いから導く")
    save(im, "t1e13JumpCondition")


# ============================================================
# 公式・用語図 t1f13*  (16枚)
# ============================================================

# t1f13Capturing : 界面捕獲法(固定格子・関数phi)
def f_Capturing():
    im, d = new(); title(d, "界面捕獲法: 固定格子上の関数 phi で界面を捉える")
    gx0, gy0, gx1, gy1 = 120, 100, 540, 300
    grid(d, gx0, gy0, gx1, gy1, 7)
    cw = (gx1 - gx0) / 7; chh = (gy1 - gy0) / 5
    # 各セルにF値(濃淡)、F=0.5付近が界面
    ipts = [(gx0 + (gx1 - gx0) * i / 60, gy0 + 100 + 55 * math.sin(math.pi * i / 60 - 0.3)) for i in range(61)]
    # 界面下側を淡色
    poly = ipts + [(gx1, gy1), (gx0, gy1)]
    d.polygon(poly, fill=(228, 236, 250))
    grid(d, gx0, gy0, gx1, gy1, 7)
    plot(d, 0, 0, ipts, RED, 3)
    ctext(d, 200, 140, "F=0 (気)", FT, GRAY)
    ctext(d, 440, 270, "F=1 (液)", FT, BLUE)
    ctext(d, (gx0 + gx1) / 2, 88, "F=0.5 付近を界面とみなす(赤)", FT, RED)
    ctext(d, (gx0 + gx1) / 2, gy1 + 20, "格子は動かさず F の分布の移流で界面を表す", FT, GRAY)
    note(d, "VOF法・密度関数法・Level Set法が代表。界面上にマーカーを置かない")
    save(im, "t1f13Capturing")


# t1f13Tracking : 界面追跡法(Front Tracking)
def f_Tracking():
    im, d = new(); title(d, "界面追跡法(Front Tracking): 界面要素を追う")
    gx0, gy0, gx1, gy1 = 120, 100, 540, 300
    grid(d, gx0, gy0, gx1, gy1, 7)
    # 気泡を三角形要素(線素)で覆う
    cx, cy = (gx0 + gx1) / 2, (gy0 + gy1) / 2
    R = 95
    mk = [(cx + R * math.cos(2 * math.pi * k / 14), cy + R * 0.85 * math.sin(2 * math.pi * k / 14)) for k in range(14)]
    for i in range(len(mk)):
        a, b = mk[i], mk[(i + 1) % len(mk)]
        d.line((a[0], a[1], b[0], b[1]), fill=BLUE, width=3)
        node(d, a[0], a[1], 4, fill=BLUE, col=BLUE)
    ctext(d, cx, cy, "気泡(界面を陽に持つ)", FT, BLUE)
    # 頂点を流れとともに動かす矢印
    for k in (1, 5, 9):
        a = mk[k]
        arrow(d, a[0], a[1], a[0] + 22 * math.cos(2 * math.pi * k / 14),
              a[1] + 22 * 0.85 * math.sin(2 * math.pi * k / 14), GREEN, 2, 8)
    ctext(d, (gx0 + gx1) / 2, gy1 + 20, "近傍4セル程度で密度/粘性を滑らかに遷移(有限厚さ)", FT, GRAY)
    note(d, "2D=線素, 3D=三角形要素。界面は鋭いが厚さは4格子程度")
    save(im, "t1f13Tracking")


# t1f13VOF : VOF法
def f_VOF():
    im, d = new(); title(d, "VOF法: 体積存在率 F の移流 dF/dt + u.grad F = 0")
    gx0, gy0, gx1, gy1 = 90, 100, 400, 300
    n = 5
    grid(d, gx0, gy0, gx1, gy1, n)
    cw = (gx1 - gx0) / n; chh = (gy1 - gy0) / n
    Fv = [[0, 0, 0, 0.3, 1],
          [0, 0, 0.4, 1, 1],
          [0, 0.4, 1, 1, 1],
          [0.3, 1, 1, 1, 1],
          [1, 1, 1, 1, 1]]
    for r in range(n):
        for c in range(n):
            v = Fv[r][c]
            g = int(255 - v * 120)
            d.rectangle((gx0 + c * cw + 1, gy0 + r * chh + 1,
                         gx0 + (c + 1) * cw - 1, gy0 + (r + 1) * chh - 1), fill=(g, g, g))
            ctext(d, gx0 + c * cw + cw / 2, gy0 + r * chh + chh / 2,
                  ("1" if v == 1 else ("0" if v == 0 else "%.1f" % v)), FT,
                  RED if 0 < v < 1 else GRAY)
    grid(d, gx0, gy0, gx1, gy1, n)
    # PLIC線を重ねる
    ctext(d, 245, 88, "F: セルを相が占める割合(0..1)", FT, GRAY)
    ctext(d, 500, 140, "F=1 液", FT, BLUE)
    ctext(d, 500, 175, "F=0 気", FT, GRAY)
    ctext(d, 500, 210, "0<F<1", FT, RED)
    ctext(d, 500, 232, "= 界面セル", FT, RED)
    ctext(d, 500, 270, "PLIC等で界面を", FT, GRAY)
    ctext(d, 500, 292, "区分的線分に復元", FT, GRAY)
    note(d, "体積保存に優れるが再構成しないと界面がなまる(数値拡散)")
    save(im, "t1f13VOF")


# t1f13LevelSet : Level Set法
def f_LevelSet():
    im, d = new(); title(d, "Level Set法: 符号付き距離関数 phi (phi=0 が界面)")
    hx0, hy0, hx1, hy1 = 120, 100, 540, 300
    d.rectangle((hx0, hy0, hx1, hy1), outline=LGRAY, width=1)
    cx, cy = (hx0 + hx1) / 2, (hy0 + hy1) / 2
    for r in [30, 60, 90, 120, 150]:
        d.ellipse((cx - r, cy - r * 0.7, cx + r, cy + r * 0.7), outline=GRAY, width=1)
    d.ellipse((cx - 60, cy - 42, cx + 60, cy + 42), outline=RED, width=3)
    ctext(d, cx, cy, "phi<0 (内)", FT, BLUE)
    ctext(d, cx, cy - 58, "phi=0 界面", FT, RED)
    ctext(d, cx + 150, cy - 60, "phi>0 (外)", FT, GREEN)
    ctext(d, (hx0 + hx1) / 2, gy1 + 20 if False else hy1 + 18,
          "|grad phi|=1、法線 n=grad phi/|grad phi|、曲率 kappa=-grad.n", FT, GRAY)
    note(d, "距離関数なので法線・曲率が滑らかに求まる(表面張力計算に向く)")
    save(im, "t1f13LevelSet")


# t1f13ALE : ALE法(自由表面スロッシング例)
def f_ALE():
    im, d = new(); title(d, "ALE法: 表面追従格子 + 遠方は変形抑制")
    # 容器
    d.line((80, 90, 80, 320), fill=BLACK, width=3)
    d.line((580, 90, 580, 320), fill=BLACK, width=3)
    d.line((80, 320, 580, 320), fill=BLACK, width=3)
    # 自由表面(スロッシング)
    def surf(x):
        t = (x - 80) / 500
        return 150 + 30 * math.sin(math.pi * t * 1.5)
    for i in range(9):
        xx = 80 + 500 * i / 8
        d.line((xx, surf(xx) if xx <= 580 else 320, xx, 320), fill=LGRAY, width=1)
    for j in range(5):
        pts = []
        for i in range(41):
            xx = 80 + 500 * i / 40
            base = 320 - (320 - 165) * (1 - j / 4)
            infl = (surf(xx) - 165) * (1 - j / 4)
            pts.append((xx, base + infl))
        plot(d, 0, 0, pts, LGRAY, 1)
    spts = [(80 + 500 * i / 40, surf(80 + 500 * i / 40)) for i in range(41)]
    plot(d, 0, 0, spts, BLUE, 3)
    ctext(d, 330, 120, "自由表面に追従(界面近傍)", FT, BLUE)
    ctext(d, 330, 300, "遠方の格子は緩やかに動かし歪みを抑える", FT, GRAY)
    note(d, "格子速度を流体速度と独立に定める。純ラグランジュとオイラーの中間")
    save(im, "t1f13ALE")


# t1f13PhaseIndicator : 相関数X_kの勾配と界面積濃度
def f_PhaseIndicator():
    im, d = new(); title(d, "相関数 X_k: grad X_k = -delta(x-x_i) n_k")
    # 領域図
    gx0, gy0, gx1, gy1 = 70, 100, 320, 300
    d.rectangle((gx0, gy0, gx1, gy1), outline=BLACK, width=2)
    cx, cy = 195, 200
    d.ellipse((cx - 70, cy - 60, cx + 70, cy + 60), fill=(228, 236, 250), outline=RED, width=3)
    ctext(d, cx, cy, "X=1", FS, BLUE)
    ctext(d, gx0 + 35, gy0 + 24, "X=0", FT, GRAY)
    # 外向き法線 n_k と 逆向きのgrad X
    a = math.radians(30)
    px, py = cx + 70 * math.cos(a), cy - 60 * math.sin(a)
    arrow(d, px, py, px + 40 * math.cos(a), py - 40 * math.sin(a), GREEN, 2, 9)
    ctext(d, px + 52, py - 34, "n_k", FT, GREEN)
    arrow(d, px, py, px - 34 * math.cos(a), py + 34 * math.sin(a), ORANGE, 2, 9)
    ctext(d, px - 30, py + 40, "grad X_k", FT, ORANGE)
    # 右: 関係式(プレーン表記)
    ctext(d, 470, 130, "grad X_k = -delta(x-x_i) n_k", FT, BLACK)
    ctext(d, 470, 165, "dX_k/dt + u_i . grad X_k = 0", FT, BLACK)
    ctext(d, 470, 200, "a_i = delta(x-x_i)  (界面積濃度)", FT, BLACK)
    ctext(d, 470, 235, "X_k^2 = X_k", FT, BLACK)
    ctext(d, 470, 275, "integral delta dV = 界面面積", FT, GRAY)
    note(d, "grad は外向き法線 n_k と反対向き(符号に注意)。界面上のみに立つ")
    save(im, "t1f13PhaseIndicator")


# t1f13Curvature : 界面追跡方程式と平均曲率
def f_Curvature():
    im, d = new(); title(d, "界面追跡方程式と平均曲率")
    cx, cy = 250, 230
    R = 120
    d.arc((cx - R, cy - R, cx + R, cy + R), 210, 330, fill=RED, width=3)
    ctext(d, cx, cy + 30, "phi = 一定", FT, RED)
    for ang in (255, 270, 285):
        a = math.radians(ang)
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        arrow(d, px, py, px + 40 * math.cos(a), py + 40 * math.sin(a), GREEN, 2, 9)
    ctext(d, cx, cy + R + 44, "n = grad phi/|grad phi|", FT, GREEN)
    arrow(d, cx - 150, cy - 30, cx - 95, cy - 30, BLUE, 3, 11)
    ctext(d, cx - 122, cy - 50, "u", FT, BLUE)
    # 式
    ctext(d, 510, 150, "追跡:", FT, GRAY)
    ctext(d, 510, 175, "dphi/dt + u.grad phi = 0", FT, BLACK)
    ctext(d, 510, 220, "曲率(スカラー):", FT, GRAY)
    ctext(d, 510, 245, "kappa = -grad.n", FT, BLACK)
    ctext(d, 510, 268, "= -grad.(grad phi/|grad phi|)", FT, BLACK)
    note(d, "曲率 kappa はスカラー。法線ベクトル -grad phi/|grad phi| と混同しない")
    save(im, "t1f13Curvature")


# t1f13Reinitialization : 再初期化方程式
def f_Reinitialization():
    im, d = new(); title(d, "再初期化方程式  dphi/dtau = sign(phi0)[1 - |grad phi|]")
    # 左: 不均一
    hx0, hy0, hx1, hy1 = 60, 110, 300, 300
    d.rectangle((hx0, hy0, hx1, hy1), outline=LGRAY, width=1)
    cx, cy = 180, 205
    for r in [20, 34, 55, 85, 120]:
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=GRAY, width=1)
    d.ellipse((cx - 34, cy - 27, cx + 34, cy + 27), outline=RED, width=3)
    ctext(d, 180, 98, "移流後: 間隔 不均一", FT, GRAY)
    arrow(d, 310, 205, 350, 205, BLACK, 3, 12)
    ctext(d, 330, 185, "tau", FT, GRAY)
    # 右: 等間隔
    hx0, hy0, hx1, hy1 = 360, 110, 600, 300
    d.rectangle((hx0, hy0, hx1, hy1), outline=LGRAY, width=1)
    cx, cy = 480, 205
    for r in [28, 52, 76, 100]:
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=GRAY, width=1)
    d.ellipse((cx - 28, cy - 22, cx + 28, cy + 22), outline=RED, width=3)
    ctext(d, 480, 98, "回復後: |grad phi|=1 等間隔", FT, GRAY)
    note(d, "界面(phi=0)位置は動かさず符号付き距離関数へ収束させる")
    save(im, "t1f13Reinitialization")


# t1f13SmoothedHeaviside : 平滑化ヘビサイドとデルタ
def f_SmoothedHeaviside():
    im, d = new(); title(d, "平滑化ヘビサイド H_eps と 平滑化デルタ delta_eps")
    # 上: H_eps
    ox, oy = 130, 170
    axes(d, ox, oy, 400, 85, "phi", "H_eps")
    pts = []
    for i in range(121):
        t = i / 120
        phi = (t - 0.5) * 2
        y = oy - 42 - 38 * (0.5 * (phi + (1 / math.pi) * math.sin(math.pi * phi)))
        pts.append((ox + 400 * t, y))
    plot(d, 0, 0, pts, BLUE, 3)
    dashed(d, ox + 200, oy, ox + 200, oy - 84, LGRAY, 1)
    ctext(d, ox + 200, oy + 14, "phi=0", FT, GRAY)
    ctext(d, ox + 320, oy - 74, "|phi|>=eps で +1/2", FT, GRAY)
    # 下: delta_eps 釣鐘、ピーク 1/eps
    ox2, oy2 = 130, 370
    axes(d, ox2, oy2, 400, 100, "phi", "delta_eps")
    pts2 = []
    for i in range(121):
        t = i / 120
        phi = (t - 0.5) * 2
        if abs(phi) < 1:
            y = oy2 - 8 - 80 * 0.5 * (1 + math.cos(math.pi * phi))
        else:
            y = oy2
        pts2.append((ox2 + 400 * t, y))
    plot(d, 0, 0, pts2, RED, 3)
    dashed(d, ox2 + 200, oy2, ox2 + 200, oy2 - 88, LGRAY, 1)
    ctext(d, ox2 + 200, oy2 - 100, "phi=0 でピーク 1/eps", FT, RED)
    ctext(d, ox2 + 330, oy2 - 12, "|phi|>=eps で 0", FT, GRAY)
    ctext(d, W - 15, 150, "delta_eps = dH_eps/dphi", FT, GRAY, "rm")
    save(im, "t1f13SmoothedHeaviside")


# t1f13CSF : CSFモデル(表面張力の体積力化)
def f_CSF():
    im, d = new(); title(d, "CSFモデル: 表面張力を体積力 f ~ sigma*kappa*delta*n として付与")
    gx0, gy0, gx1, gy1 = 100, 110, 560, 270
    n = 10
    grid(d, gx0, gy0, gx1, gy1, n, 4)
    cw = (gx1 - gx0) / n
    wv = [(gx0 + (gx1 - gx0) * i / 60, (gy0 + gy1) / 2 - 24 * math.sin(2 * math.pi * i / 30)) for i in range(61)]
    plot(d, 0, 0, wv, RED, 3)
    ctext(d, (gx0 + gx1) / 2, 96, "界面(赤)を含むセルに体積力(橙)を分布", FT, RED)
    for c in range(1, n):
        xx = gx0 + c * cw
        yy = (gy0 + gy1) / 2 - 24 * math.sin(2 * math.pi * (c / n))
        arrow(d, xx, yy, xx, yy - 24, ORANGE, 2, 8)
    ctext(d, (gx0 + gx1) / 2, gy1 + 24, "平滑化デルタ delta_eps で界面近傍に分布(界面を陽に切り出さない)", FT, GRAY)
    ctext(d, (gx0 + gx1) / 2, gy1 + 46, "sigma=表面張力係数, kappa=曲率, n=法線", FT, GRAY)
    note(d, "VOF・Level Setどちらとも組合せ可。界面再構成とは別系統のモデル")
    save(im, "t1f13CSF")


# t1f13SurfaceTensionStability : 陽解法の安定条件
def f_SurfaceTensionStability():
    im, d = new(); title(d, "表面張力の陽解法 安定条件  Dt < C (rho/sigma)^{1/2} (Dx)^{3/2}")
    # 式ボックス
    d.rectangle((120, 90, 540, 138), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 114, "Dt < C (rho/sigma)^{1/2} (Dx)^{3/2}", F)
    # Dx を細かくするとDtが厳しくなる(片対数イメージ)
    ox, oy = 130, 340
    axes(d, ox, oy, 380, 170, "Dx", "許容 Dt")
    pts = []
    for i in range(1, 101):
        t = i / 100
        dx = 0.1 + t * 0.9
        y = oy - 150 * (dx ** 1.5)
        pts.append((ox + 380 * t, y))
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, ox + 300, oy - 130, "Dt ~ (Dx)^{3/2}", FT, RED, "lm")
    ctext(d, ox + 120, oy - 40, "Dx を細かくすると Dt が急に厳しくなる", FT, GRAY, "lm")
    ctext(d, W / 2, 372 - 8, "次元: [rho/sigma]=s^2/m^3 -> (rho/sigma)^{1/2}(Dx)^{3/2} は時間 s", FT, GRAY)
    note(d, "表面張力波が1ステップで1セルを越えない条件(表面張力律速)")
    save(im, "t1f13SurfaceTensionStability")


# t1f13HeightFunction : VOF高さ関数
def f_HeightFunction():
    im, d = new(); title(d, "VOF 高さ関数  H^y_{i,j}=(F_{i,j-1}+F_{i,j}+F_{i,j+1}) Dy")
    gx0, gy0, gx1, gy1 = 80, 100, 430, 310
    n = 7
    grid(d, gx0, gy0, gx1, gy1, n)
    cw = (gx1 - gx0) / n

    def hy(x):
        t = (x - gx0) / (gx1 - gx0)
        return gy0 + 140 + 50 * math.cos(math.pi * (t - 0.5))
    for c in range(n):
        xL = gx0 + c * cw
        top = hy(xL + cw / 2)
        d.rectangle((xL + 1, top, xL + cw - 1, gy1 - 1), fill=(225, 233, 248))
    ipts = [(gx0 + (gx1 - gx0) * i / 60, hy(gx0 + (gx1 - gx0) * i / 60)) for i in range(61)]
    plot(d, 0, 0, ipts, RED, 3)
    mx = (gx0 + gx1) / 2
    arrow(d, mx, hy(mx), mx, hy(mx) - 38, GREEN, 2, 9)
    ctext(d, mx + 30, hy(mx) - 30, "n", FT, GREEN)
    ctext(d, (gx0 + gx1) / 2, gy1 + 18, "列ごとに F を積み上げ = H^y", FT, GRAY)
    # 式
    ctext(d, 545, 150, "|n_y|>|n_x|:", FT, GRAY)
    ctext(d, 545, 180, "|kappa| =", FT, BLACK)
    ctext(d, 545, 205, "|H^y''| /", FT, BLACK)
    ctext(d, 545, 228, "(1+(H^y')^2)^{3/2}", FT, BLACK)
    ctext(d, 545, 268, "分母指数 3/2", FT, RED)
    note(d, "法線の主方向に応じて H^y(x で微分) か H^x(y で微分) を選ぶ")
    save(im, "t1f13HeightFunction")


# t1f13PhaseField : Phase Field(Cahn-Hilliard/Allen-Cahn)
def f_PhaseField():
    im, d = new(); title(d, "Phase Field法: 保存型 Cahn-Hilliard / 非保存型 Allen-Cahn")
    # phi 滑らか遷移
    ox, oy = 70, 250
    axes(d, ox, oy, 230, 150, "位置", "phi")
    pts = []
    for i in range(121):
        t = i / 120
        y = oy - 20 - 110 * (0.5 * (1 + math.tanh((t - 0.5) * 8)))
        pts.append((ox + 230 * t, y))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 115, oy + 20, "有限幅で滑らかに遷移", FT, GRAY)
    # 右: 式と対比
    ctext(d, 470, 130, "保存型(Cahn-Hilliard):", FT, GREEN)
    ctext(d, 470, 155, "dphi/dt = M(grad^2 f'(phi) - xi grad^4 phi)", FT, BLACK)
    ctext(d, 470, 185, "第1項=バルク / 第2項=界面エネルギー", FT, GRAY)
    ctext(d, 470, 215, "phi の総量は保存 (M=モビリティ)", FT, GRAY)
    ctext(d, 470, 250, "非保存型(Allen-Cahn):", FT, ORANGE)
    ctext(d, 470, 275, "蒸発凝縮など相変化に用いる", FT, GRAY)
    note(d, "界面厚みは xi(界面エネルギー)側で決まり M(モビリティ)には無関係")
    save(im, "t1f13PhaseField")


# t1f13Reconstruction : 界面再構成法(SLIC/PLIC/MARS)
def f_Reconstruction():
    im, d = new(); title(d, "界面再構成法: 体積率 F(=0.5) から界面を復元")
    # 左: SLIC 階段
    gx0, gy0, gx1, gy1 = 70, 110, 250, 290
    grid(d, gx0, gy0, gx1, gy1, 3)
    cw = (gx1 - gx0) / 3; chh = (gy1 - gy0) / 3
    stair = [(gx0, gy0 + chh), (gx0 + cw, gy0 + chh), (gx0 + cw, gy0 + 2 * chh),
             (gx0 + 2 * cw, gy0 + 2 * chh), (gx0 + 2 * cw, gy1), (gx1, gy1)]
    for i in range(len(stair) - 1):
        d.line((stair[i][0], stair[i][1], stair[i + 1][0], stair[i + 1][1]), fill=RED, width=3)
    ctext(d, 160, 98, "SLIC(階段状)", FT, RED)
    # 中: PLIC 傾いた線分
    hx0, hy0, hx1, hy1 = 280, 110, 460, 290
    grid(d, hx0, hy0, hx1, hy1, 3)
    cw2 = (hx1 - hx0) / 3; ch2 = (hy1 - hy0) / 3
    seg = [((hx0, hy0 + ch2 * 0.8), (hx0 + cw2, hy0 + ch2 * 1.5)),
           ((hx0 + cw2, hy0 + ch2 * 1.5), (hx0 + 2 * cw2, hy0 + ch2 * 2.2)),
           ((hx0 + 2 * cw2, hy0 + ch2 * 2.2), (hx1, hy0 + ch2 * 2.9))]
    for a, b in seg:
        d.line((a[0], a[1], b[0], b[1]), fill=BLUE, width=3)
    ctext(d, 370, 98, "PLIC(区分的線分)", FT, BLUE)
    # 右: MARS(マーカー+再構成)
    panel(d, 485, 120, 605, 285, "MARS", GRAY)
    for k in range(6):
        node(d, 500 + k * 18, 200 + 12 * math.sin(k), 4, fill=GRAY, col=GRAY)
    ctext(d, 545, 235, "マーカー+再構成", FT, GRAY)
    note(d, "同じ F=0.5 でも SLIC=階段, PLIC=傾いた線分。PLICが界面を鋭く保つ")
    save(im, "t1f13Reconstruction")


# t1f13JumpCondition : 気液界面の跳躍条件
def f_JumpCondition():
    im, d = new(); title(d, "気液界面の跳躍条件: ラプラス圧 Dp = sigma*kappa")
    xm = 330
    d.line((xm, 90, xm, 290), fill=RED, width=4)
    ctext(d, xm, 78, "気液界面", FT, RED)
    # 気泡と内外圧
    cx, cy = 200, 200
    d.ellipse((cx - 70, cy - 60, cx + 70, cy + 60), outline=BLUE, width=3)
    ctext(d, cx, cy, "気泡 内圧 高", FT, BLUE)
    for ang in (20, 90, 160, 250, 320):
        a = math.radians(ang)
        px, py = cx + 70 * math.cos(a), cy - 60 * math.sin(a)
        arrow(d, px - 18 * math.cos(a), py + 18 * math.sin(a), px, py, ORANGE, 2, 7)
    ctext(d, cx, cy + 84, "Dp = sigma*kappa (ラプラス圧)", FT, GRAY)
    # 右: 関与因子
    ctext(d, 490, 130, "跳躍条件に関与:", FT, GRAY)
    for i, s in enumerate(["・表面張力(圧力の跳び)", "・蒸発/凝縮(質量・運動量)", "・粘性応力のつり合い"]):
        ctext(d, 490, 160 + i * 26, s, FT, BLACK, "lm")
    panel(d, 470, 250, 630, 290, "", GRAY)
    ctext(d, 550, 270, "密度比=両相物性(別)", FT, GRAY)
    note(d, "界面での力学的・熱的つり合いから導く界面の境界条件")
    save(im, "t1f13JumpCondition")


# t1f13Challenges : 移流数値解法と計算困難な現象
def f_Challenges():
    im, d = new(); title(d, "移流方程式の数値解法 と 計算が困難な現象")
    # 左上: 矩形波移流の対比
    panel(d, 55, 90, 330, 250, "矩形波の移流")
    ox, oy = 75, 225
    axes(d, ox, oy, 240, 120, "x", "")
    base = oy - 80
    dashed(d, ox + 60, oy, ox + 60, base, LGRAY, 1)
    dashed(d, ox + 60, base, ox + 120, base, LGRAY, 1)
    dashed(d, ox + 120, base, ox + 120, oy, LGRAY, 1)
    # FTCS 振動
    ftcs = [(ox + 10 + 230 * i / 60, oy - (80 if 0.35 < i / 60 < 0.6 else 0)
             - 26 * math.sin(2 * math.pi * i / 5) * (1 if 0.2 < i / 60 < 0.85 else 0)) for i in range(61)]
    plot(d, 0, 0, ftcs, RED, 2)
    # CIP 鋭い
    plot(d, 0, 0, [(ox + 150, oy), (ox + 156, base), (ox + 200, base), (ox + 206, oy)], BLUE, 2)
    ctext(d, ox + 60, base - 14, "FTCS:振動", FT, RED)
    ctext(d, ox + 178, base - 14, "CIP:鋭い", FT, BLUE)
    # 右: 手法一覧
    panel(d, 345, 90, 605, 250, "解法")
    for i, (s, col) in enumerate([("FTCS = 不安定(不適)", RED),
                                  ("TVD = リミッターで振動抑制", GREEN),
                                  ("CIP = 補間で鋭さ保持", BLUE),
                                  ("ラグランジュ = 粒子を移流", GRAY)]):
        ctext(d, 360, 125 + i * 30, s, FT, col, "lm")
    # 下: 困難な現象
    ctext(d, W / 2, 285, "困難: 気泡核生成(無から界面) / 合体を正しく予測", FT, GRAY)
    ctext(d, W / 2, 312, "目安: 球形気泡の上昇速度予測は等価直径あたり約20セル", FT, GRAY)
    note(d, "FTCSは移流を安定に解けない。連続体スケールで無からの界面生成は困難")
    save(im, "t1f13Challenges")


# ============================================================
if __name__ == "__main__":
    # 問題図 t1e13* (19)
    CaptureVsTrack()
    VofVsLevelSet()
    ALE()
    CellsPerBubble()
    InterfaceThickness()
    CaptureErrors()
    BubbleNucleation()
    AdvectionSchemes()
    PhaseIndicator()
    LevelSetCurvature()
    SmoothedDelta()
    DirectSimulation()
    DampedOscillation()
    HeightFunction()
    Reinitialization()
    CsfStability()
    CahnHilliard()
    InterfaceReconstruction()
    JumpCondition()
    # 公式・用語図 t1f13* (16)
    f_Capturing()
    f_Tracking()
    f_VOF()
    f_LevelSet()
    f_ALE()
    f_PhaseIndicator()
    f_Curvature()
    f_Reinitialization()
    f_SmoothedHeaviside()
    f_CSF()
    f_SurfaceTensionStability()
    f_HeightFunction()
    f_PhaseField()
    f_Reconstruction()
    f_JumpCondition()
    f_Challenges()
    print("done ch13")
