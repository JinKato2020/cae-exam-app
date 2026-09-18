# -*- coding: utf-8 -*-
"""熱流体力学1級 第3章 問題図 12枚。figlibで白地660x420線画。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=10, gap=7):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = t; b = min(t + dl, L)
        d.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=col, width=wd)
        t += dl + gap


def box(d, x0, y0, x1, y1, fill=FILL1, col=BLACK, wd=2):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def flowbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        ctext(d, cx, cy - (len(lines) - 1) * 10 + i * 20, line, fnt)


# -------------------------------------------------- 3-1 誤差の分類
def f_errortypes():
    im, d = new()
    title(d, "数値解析における誤差の分類")
    rows = [("丸め誤差", "端数処理（有限桁）", "計算機の桁数で端数を丸める", (225, 240, 225)),
            ("打ち切り誤差", "級数を有限項で打切り", "テイラー級数などを途中で切る", (245, 240, 225)),
            ("エイリアジング誤差", "高波数の折り返し", "粗い格子で高波数が低波数に化ける", (235, 235, 245)),
            ("不確かさ", "真値は得られない", "測定・モデルに残る本質的なばらつき", (245, 228, 228))]
    for i, (name, key, desc, col) in enumerate(rows):
        y = 105 + i * 72
        box(d, 55, y - 28, 605, y + 28, col)
        ctext(d, 155, y, name, FS, BLACK)
        ctext(d, 340, y, key, FT, RED)
        ctext(d, 510, y, desc, FT, GRAY)
    note(d, "由来が異なる4種を区別する（丸め=桁／打切り=近似／折返し=解像度／不確かさ=本質）")
    save(im, "t1e3ErrorTypes")


# -------------------------------------------------- 3-2 不等間隔格子（required・答えを描かない）
def f_nonuniform():
    im, d = new()
    title(d, "不等間隔格子上の3点")
    oy = 230
    arrow(d, 60, oy, 600, oy, BLACK, 2, 11)
    ctext(d, 606, oy, "x", FS, BLACK, "lm")
    # 点2,3,4 を不等間隔に配置（左が広い h_L、右が狭い h_R）
    x2, x3, x4 = 150, 360, 480
    for x, lab in [(x2, "2"), (x3, "3"), (x4, "4")]:
        d.line((x, oy - 6, x, oy + 6), fill=BLACK, width=2)
        node(d, x, oy, 8, FILL1, BLACK)
        ctext(d, x, oy + 26, lab, FS, BLACK)
    dim(d, x2, oy - 46, x3, oy - 46, "h_L")
    dim(d, x3, oy - 46, x4, oy - 46, "h_R")
    ctext(d, (x2 + x3) / 2, oy - 74, "左隣との間隔", FT, GRAY)
    ctext(d, (x3 + x4) / 2, oy - 74, "右隣との間隔", FT, GRAY)
    note(d, "h_L と h_R が異なる（不等間隔）。点3での差分近似を考える")
    save(im, "t1e3NonUniform")


# -------------------------------------------------- 3-3 スペクトル法
def f_spectral():
    im, d = new()
    title(d, "スペクトル法（直交関数系による展開）")
    flowbox(d, 330, 95, 420, 46, "重み付き残差法 ＋ 直交関数系", (225, 240, 225))
    arrow(d, 230, 118, 175, 165, BLACK, 2, 11)
    arrow(d, 430, 118, 485, 165, BLACK, 2, 11)
    flowbox(d, 165, 200, 230, 56, "フーリエ級数\n（周期方向）", (235, 235, 245), FT)
    flowbox(d, 495, 200, 230, 56, "チェビシェフ多項式\n（非周期・壁方向）", (245, 240, 225), FT)
    # チャネル流れ DNS の模式
    y0, y1 = 300, 380
    hwall(d, 120, 540, y0, side=1, n=14)
    hwall(d, 120, 540, y1, side=-1, n=14)
    ctext(d, 330, (y0 + y1) / 2 - 2, "チャネル流れ DNS", FT, BLACK)
    ctext(d, 300, y0 - 14, "壁垂直方向＝チェビシェフ", FT, GRAY)
    ctext(d, 300, y1 + 16, "一様方向＝フーリエ＋周期境界", FT, GRAY)
    save(im, "t1e3Spectral")


# -------------------------------------------------- 3-4 Adams-Bashforth（陽解法・外挿）
def f_ab2():
    im, d = new()
    title(d, "2次アダムス・バッシュフォース法（陽的外挿）")
    ox, oy = 90, 300
    axes(d, ox, oy, 470, 210, "t", "u")
    xs = {"n-1": 170, "n": 320, "n+1": 470}
    ys = {"n-1": 230, "n": 190}
    for lab, x in xs.items():
        d.line((x, oy - 4, x, oy + 4), fill=BLACK, width=2)
        ctext(d, x, oy + 20, lab, FT, BLACK)
    p1 = (xs["n-1"], ys["n-1"]); p2 = (xs["n"], ys["n"])
    node(d, *p1, 6, BLUE, BLUE); node(d, *p2, 6, BLUE, BLUE)
    # 既知の傾き H^{n-1}, H^n
    dash(d, p1[0] - 40, p1[1] + 22, p1[0] + 40, p1[1] - 22, GRAY)
    dash(d, p2[0] - 40, p2[1] + 22, p2[0] + 40, p2[1] - 22, GRAY)
    ctext(d, p1[0] - 6, p1[1] - 26, "H^(n-1)", FT, GRAY)
    ctext(d, p2[0] - 6, p2[1] - 26, "H^n", FT, GRAY)
    # 外挿して u^{n+1} を予測
    pnew = (xs["n+1"], 150)
    plot(d, 0, 0, [p2, pnew], RED, 3)
    node(d, *pnew, 7, "white", RED)
    ctext(d, pnew[0] + 4, pnew[1] - 22, "u^(n+1) を予測", FT, RED, "mm")
    ctext(d, 330, 95, "既知の2点の傾きから未来へ外挿（陽的・反復不要）", FT, GRAY)
    save(im, "t1e3Ab2")


# -------------------------------------------------- 3-5 GSMAC（速度・圧力同時緩和）
def f_gsmac():
    im, d = new()
    title(d, "GSMAC：速度・圧力の同時緩和（符号関係）")
    steps = [
        ("速度場の発散を計算   div u > 0", (245, 228, 228)),
        ("→ 修正ポテンシャル φ < 0", (235, 235, 245)),
        ("→ 圧力 p を下げる（p ← p + φ 型）", (225, 240, 225)),
        ("→ 速度を修正して発散を 0 へ", FILL1)]
    ys = [110, 185, 260, 335]
    for i, ((s, col), y) in enumerate(zip(steps, ys)):
        flowbox(d, 330, y, 430, 52, s, col)
        if i < 3:
            arrow(d, 330, y + 26, 330, ys[i + 1] - 26, BLACK, 2, 11)
    ctext(d, 585, 222, "発散(＋)と\n圧力補正(−)は\n逆符号", FT, RED)
    save(im, "t1e3Gsmac")


# -------------------------------------------------- 3-6 CIP法（3次補間 vs 1次）
def f_cip():
    im, d = new()
    title(d, "CIP法：値と勾配を保持する3次補間")
    oy = 320
    # 左: 1次補間（なまる）
    ox = 90
    axes(d, ox, oy, 210, 210, "x", "f")
    d.line((ox, oy - 30, ox + 90, oy - 30), fill=GRAY, width=2)
    plot(d, 0, 0, [(ox + 90, oy - 30), (ox + 130, oy - 150)], GRAY, 3)
    d.line((ox + 130, oy - 150, ox + 200, oy - 150), fill=GRAY, width=2)
    ctext(d, ox + 105, oy + 20, "1次補間", FS, GRAY)
    ctext(d, ox + 105, oy - 190, "界面がなまる", FT, GRAY)
    # 右: CIP（値+勾配で鋭い界面）
    ox = 380
    axes(d, ox, oy, 210, 210, "x", "f")
    pts = [(ox, oy - 30), (ox + 70, oy - 34), (ox + 100, oy - 90), (ox + 118, oy - 150), (ox + 200, oy - 156)]
    plot(d, 0, 0, pts, BLUE, 3)
    for p in [(ox + 60, oy - 32), (ox + 140, oy - 152)]:
        node(d, p[0], p[1], 6, BLUE, BLUE)
        d.line((p[0] - 22, p[1], p[0] + 22, p[1]), fill=RED, width=2)  # 勾配（接線）
    ctext(d, ox + 105, oy + 20, "CIP（3次）", FS, BLUE)
    ctext(d, ox + 120, oy - 190, "値＋勾配を保持→鋭い", FT, BLUE)
    ctext(d, ox - 30, oy - 40, "赤線=各点の勾配情報も一緒に運ぶ", FT, RED, "lm")
    save(im, "t1e3Cip")


# -------------------------------------------------- 3-7 流体構造連成（弱連成 vs 強連成）
def f_fsi():
    im, d = new()
    title(d, "流体構造連成：弱連成 と 強連成")
    # 弱連成
    ctext(d, 175, 80, "弱連成（分離反復）", FS, GREEN)
    flowbox(d, 110, 150, 130, 46, "流体を解く", (235, 235, 245), FT)
    flowbox(d, 245, 150, 130, 46, "構造を解く", (245, 240, 225), FT)
    arrow(d, 176, 150, 180, 150, BLACK, 2, 10)
    # 界面で反復ループ
    d.line((110, 173, 110, 210), fill=BLACK, width=2)
    d.line((110, 210, 245, 210), fill=BLACK, width=2)
    arrow(d, 245, 210, 245, 173, BLACK, 2, 10)
    ctext(d, 178, 228, "界面条件で反復", FT, RED)
    ctext(d, 175, 260, "別々に解き交互に受け渡し", FT, GRAY)
    d.line((330, 70, 330, 300), fill=LGRAY, width=2)
    # 強連成
    ctext(d, 490, 80, "強連成（同時解法）", FS, RED)
    flowbox(d, 490, 165, 210, 90, "流体 ＋ 構造\nを1つの連立系で\n同時に解く", (245, 228, 228), FT)
    ctext(d, 490, 245, "界面条件を系に内包", FT, GRAY)
    note(d, "界面条件＝速度連続と力のつり合い。強連成は安定・高コスト、弱連成は軽い・付加質量で不安定化")
    save(im, "t1e3Fsi")


# -------------------------------------------------- 3-8 スタッガード格子（required・答えを描かない）
def f_staggered():
    im, d = new()
    title(d, "スタッガード格子の変数配置")
    ox, oy, h = 150, 120, 110
    nx, ny = 3, 2
    # セル格子
    for j in range(ny + 1):
        d.line((ox, oy + j * h, ox + nx * h, oy + j * h), fill=LGRAY, width=2)
    for i in range(nx + 1):
        d.line((ox + i * h, oy, ox + i * h, oy + ny * h), fill=LGRAY, width=2)
    # 圧力 p = セル中心
    for j in range(ny):
        for i in range(nx):
            cx, cy = ox + i * h + h / 2, oy + j * h + h / 2
            node(d, cx, cy, 8, (225, 240, 225), BLACK)
            ctext(d, cx, cy, "p", FT, BLACK)
    # 速度 u = 縦の界面（左右境界）
    for j in range(ny):
        for i in range(nx + 1):
            cx, cy = ox + i * h, oy + j * h + h / 2
            arrow(d, cx - 14, cy, cx + 14, cy, BLUE, 2, 8)
            ctext(d, cx, cy - 15, "u", FT, BLUE)
    # 速度 v = 横の界面（上下境界）
    for j in range(ny + 1):
        for i in range(nx):
            cx, cy = ox + i * h + h / 2, oy + j * h
            arrow(d, cx, cy + 14, cx, cy - 14, GREEN, 2, 8)
            ctext(d, cx + 15, cy, "v", FT, GREEN)
    ctext(d, 330, oy + ny * h + 40, "p=セル中心／u,v=セル境界（半格子ずれ）", FT, GRAY)
    note(d, "圧力と速度を半格子ずらして配置（配置のみ）")
    save(im, "t1e3Staggered")


# -------------------------------------------------- 3-9 Roe法（リーマン問題）
def f_roe():
    im, d = new()
    title(d, "リーマン問題と Roe 平均")
    oy0, oy1 = 130, 300
    xi = 330  # 界面
    d.line((xi, oy0 - 10, xi, oy1 + 20), fill=BLACK, width=3)
    ctext(d, xi, oy1 + 40, "界面", FT, BLACK)
    box(d, 90, oy0, xi, oy1, (235, 235, 245))
    box(d, xi, oy0, 570, oy1, (245, 240, 225))
    ctext(d, (90 + xi) / 2, oy0 + 40, "左状態", FS, BLACK)
    ctext(d, (90 + xi) / 2, oy0 + 75, "Q_L", F, BLUE)
    ctext(d, (xi + 570) / 2, oy0 + 40, "右状態", FS, BLACK)
    ctext(d, (xi + 570) / 2, oy0 + 75, "Q_R", F, ORANGE)
    # Roe平均行列と波
    flowbox(d, xi, oy1 - 30, 200, 44, "Roe平均行列 A", (255, 236, 236))
    for ang, lab in [(150, "u-a"), (90, "u"), (30, "u+a")]:
        a = math.radians(ang)
        arrow(d, xi, oy1 - 30, xi + 95 * math.cos(a), oy1 - 30 - 95 * math.sin(a), RED, 2, 10)
    ctext(d, xi, 105, "波の伝播（左右へ）", FT, RED)
    note(d, "左右の不連続を、線形化した A の固有値（波速）と固有ベクトルで分解して流束を評価")
    save(im, "t1e3Roe")


# -------------------------------------------------- 3-10 1次元オイラー方程式の特性線（3本）
def f_euler1d():
    im, d = new()
    title(d, "1次元オイラー方程式の特性線（x-t平面）")
    ox, oy = 90, 350
    axes(d, ox, oy, 480, 280, "x", "t")
    x0 = ox + 280  # 起点
    d.line((x0, oy - 4, x0, oy + 4), fill=BLACK, width=2)
    ctext(d, x0, oy + 20, "x0", FT, BLACK)
    top = oy - 240
    lines = [(("u", BLUE), 70),      # 傾き u>0（右へ）
             (("u+a", GREEN), 170),  # u+a（急right）
             (("u-a", RED), -150)]   # u-a<0（左へ）
    for (lab, col), dx in lines:
        arrow(d, x0, oy, x0 + dx, top, col, 3, 12)
        ctext(d, x0 + dx + (10 if dx >= 0 else -10), top - 6, lab, FS, col,
              "lm" if dx >= 0 else "rm")
    ctext(d, 210, 95, "傾き dx/dt = u, u+a, u-a（u-a<0 は左向き）", FT, GRAY, "lm")
    note(d, "3本の特性速度で情報が伝わる。u-a<0 なら左へ伝播する波が存在")
    save(im, "t1e3Euler1D")


# -------------------------------------------------- 3-11 全エネルギーの積み上げと圧力
def f_pressure():
    im, d = new()
    title(d, "全エネルギー e と圧力 p の関係")
    ox = 200
    base = 350
    w = 120
    ie_h = 150   # 内部エネルギー
    ke_h = 90    # 運動エネルギー
    # 積み上げ棒
    box(d, ox, base - ie_h, ox + w, base, (225, 240, 225))
    ctext(d, ox + w / 2, base - ie_h / 2, "内部\nエネルギー", FT, BLACK)
    box(d, ox, base - ie_h - ke_h, ox + w, base - ie_h, (235, 235, 245))
    ctext(d, ox + w / 2, base - ie_h - ke_h / 2, "運動\nエネルギー\nrho u^2 / 2", FT, BLACK)
    d.line((ox - 30, base, ox + w + 200, base), fill=BLACK, width=2)
    dim(d, ox + w + 30, base, ox + w + 30, base - ie_h - ke_h, "全エネルギー e")
    # 圧力の関係式
    arrow(d, ox + w / 2, base - ie_h + 6, ox - 40, base - ie_h + 6, RED, 2, 10)
    ctext(d, ox - 50, base - ie_h + 6, "内部エネルギー", FT, RED, "rm")
    flowbox(d, 470, 180, 250, 60, "p = (γ−1) ×\n内部エネルギー（×密度）", (245, 228, 228), FT)
    note(d, "e = 内部エネルギー + 運動エネルギー。圧力は内部エネルギー分から状態方程式で得る")
    save(im, "t1e3Pressure")


# -------------------------------------------------- 3-12 特性曲線（2本・u±c）
def f_charact():
    im, d = new()
    title(d, "特性曲線（x-t平面, 傾き u+c と u-c）")
    ox, oy = 90, 350
    axes(d, ox, oy, 480, 280, "x", "t")
    x0 = ox + 250
    d.line((x0, oy - 4, x0, oy + 4), fill=BLACK, width=2)
    ctext(d, x0, oy + 20, "x0", FT, BLACK)
    # u+c: 右へ曲がる特性曲線
    pts_p = []
    for i in range(0, 26):
        t = i / 25.0
        yy = oy - t * 250
        xx = x0 + 190 * (t ** 1.25)
        pts_p.append((xx, yy))
    plot(d, 0, 0, pts_p, GREEN, 3)
    ctext(d, pts_p[-1][0] + 10, pts_p[-1][1] - 6, "u+c", FS, GREEN, "lm")
    # u-c<0: 左へ向かう特性曲線
    pts_m = []
    for i in range(0, 26):
        t = i / 25.0
        yy = oy - t * 250
        xx = x0 - 150 * (t ** 1.1)
        pts_m.append((xx, yy))
    plot(d, 0, 0, pts_m, RED, 3)
    ctext(d, pts_m[-1][0] - 10, pts_m[-1][1] - 6, "u-c", FS, RED, "rm")
    ctext(d, 330, 95, "傾き dx/dt = u+c, u-c（u-c<0 は左向き）", FT, GRAY)
    note(d, "2本の特性曲線に沿ってリーマン不変量が伝わる。u-c<0 なら左へ伝播")
    save(im, "t1e3Charact")


if __name__ == "__main__":
    f_errortypes(); f_nonuniform(); f_spectral(); f_ab2(); f_gsmac()
    f_cip(); f_fsi(); f_staggered(); f_roe(); f_euler1d()
    f_pressure(); f_charact()
    print("done t1e3")
