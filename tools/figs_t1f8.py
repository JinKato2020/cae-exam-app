# -*- coding: utf-8 -*-
"""熱流体力学1級 第8章「結果と評価」公式・用語図 16枚。figlibで白地660x420線画。
公式・用語図は回答後扱いのため結論・式・ラベルを描いてよい。機構のみ・装飾禁止。
問題図(t1e8)とは別系統。ここは接頭辞 t1f8。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- ローカル補助(figs_t1e7 と同じ書き方。t1e8 は未作成のため自前定義) ----
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


def fbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS, col=BLACK):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ls = text.split("\n")
    for i, line in enumerate(ls):
        ctext(d, cx, cy - (len(ls) - 1) * 11 + i * 22, line, fnt, col)


def curve(d, pts, col=BLACK, wd=2):
    d.line(pts, fill=col, width=wd, joint="curve")


def swirl(d, cx, cy, r, cw=True, col=BLUE, wd=2):
    a0, a1 = 20, 300
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    end = math.radians(a1 if cw else a0)
    ex, ey = cx + r * math.cos(end), cy + r * math.sin(end)
    t = end + (math.pi / 2 if cw else -math.pi / 2)
    for s in (0.6, -0.6):
        d.line((ex, ey, ex - 10 * math.cos(t - s), ey - 10 * math.sin(t - s)), fill=col, width=wd)


# ============================================================ 1. 数値解析の3つの誤差
def f_three_errors():
    im, d = new()
    title(d, "数値解析の3つの誤差：発生源で切り分ける")
    cx = 210
    b = [("実際の流れ現象", 90),
         ("支配方程式の厳密解", 175),
         ("離散化方程式の厳密解", 265),
         ("反復計算で得た解", 350)]
    for (s, y) in b:
        fbox(d, cx, y, 240, 42, s, (235, 240, 250), FS)
    # 誤差ラベル(矢印上)
    errs = [("(C) モデリング誤差", "実験でのみ評価可", 132, ORANGE),
            ("(A) 離散化誤差", "格子の優劣で変化", 220, BLUE),
            ("(B) 収束誤差", "反復残差・先に潰す", 307, GREEN)]
    for i, (e1, e2, ym, col) in enumerate(errs):
        arrow(d, cx, b[i][1] + 21, cx, b[i + 1][1] - 21, BLACK, 2, 11)
        ctext(d, cx + 130, ym - 9, e1, FT, col, "lm")
        ctext(d, cx + 130, ym + 9, e2, FT, GRAY, "lm")
    note(d, "収束(B)を十分潰し→格子で離散化(A)を下げ→残差にモデリング誤差(C)が残る")
    save(im, "t1f8ThreeErrors")


# ============================================================ 2. 検証と妥当性確認
def f_ver_val():
    im, d = new()
    title(d, "検証(Verification) と 妥当性確認(Validation)")
    b1 = (130, 150); b2 = (340, 150); b3 = (555, 150)
    fbox(d, *b1, 150, 56, "支配方程式\n・離散化式", (235, 240, 250), FT)
    fbox(d, *b2, 130, 56, "数値解", (240, 248, 240), FT)
    fbox(d, *b3, 150, 56, "実際の現象\n(実験)", (255, 244, 232), FT)
    arrow(d, b1[0] + 75, 150, b2[0] - 65, 150, BLUE, 3, 12)
    arrow(d, b2[0] + 65, 150, b3[0] - 75, 150, ORANGE, 3, 12)
    ctext(d, (b1[0] + b2[0]) / 2, 118, "検証", FT, BLUE)
    ctext(d, (b2[0] + b3[0]) / 2, 118, "妥当性確認", FT, ORANGE)
    fbox(d, 190, 300, 300, 92,
         "検証: 方程式を正しく\n解けているか\n対象=離散化誤差・収束誤差\n解析解比較・格子収束で確認",
         (240, 244, 252), FT, BLUE)
    fbox(d, 500, 300, 300, 92,
         "妥当性確認: 正しい式か\n(モデルが妥当か)\n対象=モデリング誤差\n信頼できる実験と比較",
         (252, 246, 240), FT, ORANGE)
    save(im, "t1f8VerVal")


# ============================================================ 3. 格子細分化による収束性
def f_grid_convergence():
    im, d = new()
    title(d, "格子細分化：収束値が実験値と一致するとは限らない")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 265, "格子細分化（粗 → 細）", "平均圧力 p")
    xn = lambda t: ox + 40 + t * 400   # t:0..1
    asym = oy - 210                    # 計算の収束値
    exp = oy - 150                     # 実験値E(別の値)
    # 計算値: 粗→細で asym に収束
    labs = ["A", "B", "C", "D"]
    pts = []
    for i in range(4):
        t = i / 3.0
        val = (oy - 60) + (asym - (oy - 60)) * (1 - math.exp(-2.4 * t)) / (1 - math.exp(-2.4))
        pts.append((xn(t), val))
    curve(d, pts, BLUE, 3)
    for (px, py), lb in zip(pts, labs):
        node(d, px, py, 5, BLUE, BLUE)
        ctext(d, px, py - 16, lb, FT, BLUE)
    dash(d, ox, asym, ox + 460, asym, BLUE, 2, 9, 6)
    ctext(d, ox + 300, asym - 14, "計算の収束値", FT, BLUE, "lm")
    dash(d, ox, exp, ox + 460, exp, RED, 2, 9, 6)
    node(d, ox + 430, exp, 5, RED, RED)
    ctext(d, ox + 300, exp + 16, "実験値 E（別の値）", FT, RED, "lm")
    note(d, "『実験に一番近い格子』を選ぶのは誤り。計算と実験の双方を見直す")
    save(im, "t1f8GridConvergence")


# ============================================================ 4. ヘルムホルツ共振器(圧力測定孔)
def f_helmholtz():
    im, d = new()
    title(d, "圧力測定孔＝ヘルムホルツ共振器（応答周波数）")
    # 上：壁(流れ側)
    hwall(d, 150, 520, 110, side=-1, n=14)
    ctext(d, 335, 88, "壁面（流れ側）", FT, GRAY)
    arrow(d, 335, 70, 335, 108, BLUE, 2, 10)
    ctext(d, 350, 78, "壁面静圧 Pi", FT, BLUE, "lm")
    # 直管部(細い) 直径d・長さL
    tx0, tx1 = 315, 355
    ty0, ty1 = 110, 225
    box(d, tx0, ty0, tx1, ty1, "white", BLACK, 2)
    dim(d, tx0, ty0 - 0, tx1, ty0 - 0, "d", col=GRAY)  # 幅d(上辺付近)
    ctext(d, tx1 + 40, (ty0 + ty1) / 2, "L", FS, BLACK, "lm")
    dash(d, tx1, ty0, tx1 + 30, ty0, LGRAY, 1, 5, 4)
    dash(d, tx1, ty1, tx1 + 30, ty1, LGRAY, 1, 5, 4)
    arrow(d, tx1 + 25, ty0, tx1 + 25, ty1, GRAY, 1, 8)
    arrow(d, tx1 + 25, ty1, tx1 + 25, ty0, GRAY, 1, 8)
    ctext(d, (tx0 + tx1) / 2, ty0 - 16, "直管部", FT, BLACK)
    # 小空間(体積V) + 圧力変換器
    cx0, cx1 = 275, 395
    cy0, cy1 = 225, 315
    box(d, cx0, cy0, cx1, cy1, (235, 240, 250), BLACK, 2)
    ctext(d, (cx0 + cx1) / 2, (cy0 + cy1) / 2 - 10, "小空間 体積 V", FT, BLACK)
    ctext(d, (cx0 + cx1) / 2, (cy0 + cy1) / 2 + 12, "圧力変換器 Pt", FT, GRAY)
    ctext(d, cx1 + 12, (cy0 + cy1) / 2, "音速 c", FT, GRAY, "lm")
    fbox(d, 335, 372, 620, 40,
         "f = √(πd²c² / 4LV) / 2π   （開口端補正: L→L+0.6d）\nこの f より高い変動圧は正しく測れない＝計測誤差の見積りが必須",
         (240, 244, 250), FT)
    save(im, "t1f8Helmholtz")


# ============================================================ 5. 流速測定法の使い分け
def f_flow_meas():
    im, d = new()
    title(d, "流速測定法の使い分け（何を検証したいか）")
    fbox(d, 180, 130, 300, 66, "大域的な速度場（面）\n→ PIV", (235, 240, 250), FS, BLUE)
    fbox(d, 500, 130, 300, 66, "局所的な乱流強度（点・変動）\n→ 熱線流速計", (240, 248, 240), FS, GREEN)
    fbox(d, 180, 240, 300, 66, "点計測（走査が必要）\nLDV・ピトー管・ヨーメーター", (245, 245, 245), FT, GRAY)
    fbox(d, 500, 240, 300, 66, "断面計測（局所は不可）\n電磁流速計・超音波流速計", (245, 245, 245), FT, GRAY)
    note(d, "大域か局所か／平均か変動か で選ぶ。点計測で面を作るにはトラバースが要る")
    save(im, "t1f8FlowMeas")


# ============================================================ 6. PIVとCFDの比較
def f_piv_cfd():
    im, d = new()
    title(d, "PIVとCFDの比較：座標変換と時間平均をそろえる")
    # 左：PIVのシート面+粒子
    box(d, 70, 100, 290, 300, "white", BLUE, 2)
    ctext(d, 180, 88, "PIV（2次元シート面）", FT, BLUE)
    import random
    random.seed(8)
    for _ in range(45):
        rx = random.randint(80, 280); ry = random.randint(110, 290)
        d.ellipse((rx, ry, rx + 3, ry + 3), fill=(90, 90, 90))
    arrow(d, 90, 285, 130, 250, GRAY, 1, 7)
    ctext(d, 180, 315, "ローカル座標", FT, GRAY)
    # 中：比較
    arrow(d, 300, 200, 360, 200, BLACK, 3, 13)
    ctext(d, 330, 178, "座標変換", FT, RED)
    # 右：CFD格子
    box(d, 370, 100, 590, 300, "white", GRAY, 2)
    for gx in range(370, 591, 22):
        d.line((gx, 100, gx, 300), fill=LGRAY, width=1)
    for gy in range(100, 301, 20):
        d.line((370, gy, 590, gy), fill=LGRAY, width=1)
    ctext(d, 480, 88, "CFD（計算座標）", FT, GRAY)
    ctext(d, 480, 315, "同じ断面を抽出", FT, GRAY)
    fbox(d, 335, 372, 620, 40,
         "定常RANS→実験の時間平均と比較／非定常RANS・LES→両者を時間平均\nカルマン渦など顕著な非定常は直接比較 or ストローハル数で評価",
         (240, 244, 250), FT)
    save(im, "t1f8PIVCFD")


# ============================================================ 7. 移流方程式の数値スキーム
def f_schemes():
    im, d = new()
    title(d, "移流方程式の数値スキーム（cΔt/Δx=0.5で矩形波を移動）")
    panels = [("(a) CIP：シャープ維持", 70, "cip"),
              ("(b) 1次風上：数値拡散でなまる", 265, "up"),
              ("(c) Lax-Wendroff：分散で振動", 460, "lw")]
    for (lab, x0, kind) in panels:
        w = 170; y0 = 100; yb = 330; ytop = 150
        box(d, x0, y0, x0 + w, yb, "white", GRAY, 1)
        ctext(d, x0 + w / 2, 350, lab, FT, BLACK)
        # 厳密解の矩形波(破線)
        a, b = x0 + 40, x0 + 105
        dash(d, x0 + 8, yb - 6, a, yb - 6, LGRAY, 1, 5, 4)
        dash(d, a, yb - 6, a, ytop, LGRAY, 1, 5, 4)
        dash(d, a, ytop, b, ytop, LGRAY, 1, 5, 4)
        dash(d, b, ytop, b, yb - 6, LGRAY, 1, 5, 4)
        dash(d, b, yb - 6, x0 + w - 8, yb - 6, LGRAY, 1, 5, 4)
        # 数値解(実線)
        pts = []
        for px in range(x0 + 8, x0 + w - 7, 3):
            t = px
            if kind == "cip":
                # ほぼ矩形(角がわずかに丸い)
                if a - 4 <= t <= b + 4:
                    y = ytop + (6 if (t < a + 3 or t > b - 3) else 0)
                else:
                    y = yb - 6
            elif kind == "up":
                # なだらかな山(ガウス的)
                c0 = (a + b) / 2
                y = yb - 6 - (yb - 6 - ytop) * math.exp(-((t - c0) / 40.0) ** 2)
            else:
                # 山＋角付近の振動
                c0 = (a + b) / 2
                base = (yb - 6 - ytop) * (1 if a <= t <= b else 0)
                osc = 14 * math.sin((t - a) * 0.5) if (a - 30 < t < b + 30) else 0
                y = yb - 6 - base - osc
                y = max(ytop - 18, min(yb - 6, y))
            pts.append((t, y))
        curve(d, pts, BLUE, 2)
    note(d, "1次風上=散逸誤差(数値拡散)／Lax-Wendroff=分散誤差／CIPは微分gも移流し3次内挿")
    save(im, "t1f8Schemes")


# ============================================================ 8. k-εと薄翼の失速
def f_stall():
    im, d = new()
    title(d, "標準k-εと薄翼の失速：失速角過大・失速後の低下が緩慢")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 270, "迎角 α", "揚力係数 CL")
    xa = lambda a: ox + a / 22.0 * 450
    # 実際(青): 直線→ピーク(α≈12)→急落
    real = []
    for a in [i * 0.5 for i in range(0, 45)]:
        if a <= 12:
            cl = a * 0.9
        else:
            cl = 12 * 0.9 - (a - 12) * 1.7
        real.append((xa(a), oy - max(0, cl) * 11))
    curve(d, real, BLUE, 3)
    ctext(d, xa(9), oy - 12 * 0.9 * 11 - 16, "実際", FT, BLUE)
    # k-ε(赤): 直線→高α(≈17)でピーク→緩やかに低下
    kep = []
    for a in [i * 0.5 for i in range(0, 45)]:
        if a <= 17:
            cl = a * 0.86
        else:
            cl = 17 * 0.86 - (a - 17) * 0.5
        kep.append((xa(a), oy - max(0, cl) * 11))
    curve(d, kep, RED, 3)
    ctext(d, xa(20), oy - 13 * 11, "標準k-ε", FT, RED, "lm")
    dash(d, xa(12), oy, xa(12), oy - 12 * 0.9 * 11, LGRAY, 1, 6, 5)
    dash(d, xa(17), oy, xa(17), oy - 17 * 0.86 * 11, LGRAY, 1, 6, 5)
    ctext(d, xa(15), oy - 40, "失速角\n過大", FT, RED)
    ctext(d, xa(6), oy - 200, "失速後の\n低下が緩慢", FT, RED, "lm")
    note(d, "層流→遷移を表せず、強い渦粘性で剥離が遅れる（失速角過大・低下が緩やか）")
    save(im, "t1f8Stall")


# ============================================================ 9. ランキン渦(旋回流)
def f_rankine():
    im, d = new()
    title(d, "旋回流：ランキン渦（実際）と強制渦のみ（k-εの誤り）")
    ox, oy = 110, 330
    axes(d, ox, oy, 460, 250, "半径 r（中心 → 内壁）", "旋回速度")
    xr = lambda t: ox + t * 440   # t:0(中心)..1(壁)
    peak = 0.42
    # 実際: 中心から強制渦(線形)→ピーク→自由渦(1/r的に減少)
    real = []
    for k in range(0, 101):
        t = k / 100.0
        if t <= peak:
            v = t / peak
        else:
            v = peak / t  # 自由渦 ~1/r
        real.append((xr(t), oy - v * 200))
    curve(d, real, BLUE, 3)
    ctext(d, xr(peak) + 10, oy - 200 - 6, "ランキン渦（実際）", FT, BLUE, "lm")
    node(d, xr(peak), oy - 200, 5, BLUE, BLUE)
    # k-ε: 中心0→壁で最大の直線(強制渦のみ)
    dash(d, xr(0), oy, xr(1), oy - 150, RED, 3, 10, 6)
    ctext(d, xr(0.72), oy - 150 * 0.72 + 18, "k-ε：強制渦のみ（線形・誤り）", FT, RED, "lm")
    note(d, "等方渦粘性は乱れの非等方性を表せない→ASM・応力方程式モデル・LESが必要")
    save(im, "t1f8Rankine")


# ============================================================ 10. 曲がり管の2次流れ
def f_secondary():
    im, d = new()
    title(d, "曲がり管の2次流れ（断面）と数値粘性の影響")
    # 正方形断面
    x0, y0, s = 150, 110, 210
    box(d, x0, y0, x0 + s, y0 + s, "white", BLACK, 2)
    ctext(d, x0 + s / 2, y0 - 16, "断面（矩形）", FT, GRAY)
    # 第1種2次流れ：遠心力起因の大きな対の渦
    swirl(d, x0 + s * 0.32, y0 + s * 0.5, 52, True, BLUE, 3)
    swirl(d, x0 + s * 0.68, y0 + s * 0.5, 52, False, BLUE, 3)
    ctext(d, x0 + s / 2, y0 + s * 0.5, "第1種\n(遠心力)", FT, BLUE)
    # 第2種2次流れ：隅の小さな渦
    for (fx, fy, cw) in [(0.08, 0.08, True), (0.92, 0.08, False),
                         (0.08, 0.92, False), (0.92, 0.92, True)]:
        swirl(d, x0 + s * fx, y0 + s * fy, 16, cw, GREEN, 2)
    ctext(d, x0 + s * 0.5, y0 + s + 18, "隅＝第2種(乱流非等方性・小)", FT, GREEN)
    # 右：スキームの影響
    arrow(d, x0 + s + 20, y0 + s / 2, x0 + s + 70, y0 + s / 2, BLACK, 2, 11)
    fbox(d, 545, 150, 200, 66, "1次風上\n数値粘性で2次流れ過小", (255, 244, 232), FT, ORANGE)
    fbox(d, 545, 250, 200, 66, "2次精度以上(QUICK)\nで正しく捉える", (240, 248, 240), FT, GREEN)
    note(d, "曲がり管は第1種が支配的。壁法則・対称条件は妥当、対策は高次スキーム化")
    save(im, "t1f8Secondary")


# ============================================================ 11. 渦粘性近似の限界(建物)
def f_eddy_viscosity():
    im, d = new()
    title(d, "渦粘性近似の限界：よどみ点で乱れ過大（k-ε 対 ASM）")
    def building(bx, by, sep):
        base = by + 90
        hwall(d, bx - 20, bx + 190, base, side=1, n=12)   # 地面
        box(d, bx + 60, by, bx + 130, base, (225, 230, 240), BLACK, 2)  # 立方体
        # 流入
        for k in range(3):
            arrow(d, bx - 15, by + 20 + k * 28, bx + 55, by + 20 + k * 28, BLUE, 2, 9)
        # よどみ点
        node(d, bx + 60, by + 45, 5, RED, RED)
        # 上面の剥離渦(あり/なし)
        if sep:
            swirl(d, bx + 100, by - 14, 20, True, GREEN, 2)
        return base
    building(90, 130, True)
    ctext(d, 185, 250, "実験 / ASM：上面に剥離渦あり", FT, GREEN)
    building(390, 130, False)
    ctext(d, 485, 250, "標準k-ε：よどみで乱れ過大→剥離消失", FT, RED)
    ctext(d, 275, 88, "よどみ点", FT, RED)
    dash(d, 330, 100, 330, 300, LGRAY, 1, 6, 5)
    note(d, "渦粘性近似は よどみ点・旋回・浮力成層 が苦手。非等方性を扱うモデルが要る")
    save(im, "t1f8EddyViscosity")


# ============================================================ 12. LES結果の比較(エルゴード性)
def f_les_comp():
    im, d = new()
    title(d, "LES結果の比較：瞬時どうしは不可、平均どうしは可")
    rows = [("LESの瞬時  対  実験/DNSの瞬時", "×", RED,
             "初期条件を再現不可・フィルタ不一致"),
            ("LESの時間平均  対  実験のアンサンブル平均", "○", GREEN,
             "エルゴード性で同値が保証される"),
            ("LESの瞬時  対  ピトー管(時間平均)", "×", RED,
             "そもそも量が違う(瞬時と時間平均)")]
    y = 110
    for (lab, mark, col, note_s) in rows:
        box(d, 70, y, 520, y + 66, (248, 248, 248), GRAY, 1)
        ctext(d, 85, y + 22, lab, FT, BLACK, "lm")
        ctext(d, 85, y + 46, note_s, FT, GRAY, "lm")
        ctext(d, 575, y + 33, mark, FL, col)
        y += 90
    note(d, "DNSと比べる時はDNSにLESと同じ空間フィルタをかけてから比較する")
    save(im, "t1f8LESComp")


# ============================================================ 13. LESの壁近傍格子解像度
def f_les_grid():
    im, d = new()
    title(d, "LESの壁近傍格子：不足すると対数則が上方へずれる")
    ox, oy = 110, 330
    axes(d, ox, oy, 460, 250, "y⁺（対数）", "U⁺")
    # 対数軸 y+ = 1..1000 → screen
    def xy(yp):
        return ox + (math.log10(yp) / 3.0) * 440
    # DNS(実線): 粘性低層 U+=y+ , 対数域 U+=2.5 ln y+ +5.0
    dns = []
    for k in range(0, 121):
        yp = 10 ** (k / 40.0)   # 1..1000
        up = yp if yp < 11 else 2.5 * math.log(yp) + 5.0
        dns.append((xy(yp), oy - up * 8))
    curve(d, dns, BLUE, 3)
    ctext(d, xy(200), oy - (2.5 * math.log(200) + 5) * 8 + 18, "DNS", FT, BLUE, "lm")
    # LES(○): 対数域で切片が上方シフト(+4)
    for k in range(0, 121, 8):
        yp = 10 ** (k / 40.0)
        up = yp if yp < 11 else 2.5 * math.log(yp) + 5.0 + (4.0 if yp >= 11 else 0)
        node(d, xy(yp), oy - up * 8, 4, "white", RED)
    ctext(d, xy(120), oy - (2.5 * math.log(120) + 9) * 8 - 14, "LES(格子不足)", FT, RED, "lm")
    fbox(d, 335, 372, 620, 40,
         "摩擦係数の過小予測→摩擦速度が小さく見積られ上方シフト\n要件: Δx⁺≈100・Δz⁺≈20・y⁺≈1（流れ方向/スパン方向も要解像）",
         (240, 244, 250), FT)
    save(im, "t1f8LESGrid")


# ============================================================ 14. 相対比較とバイアス誤差
def f_drag_scatter():
    im, d = new()
    title(d, "形状最適化：相対比較とバイアス誤差（自動車CD）")
    ox, oy = 130, 330
    axes(d, ox, oy, 430, 250, "CD（計算）", "CD（実験）")
    lo, hi = 0.24, 0.40
    sc = 420 / (hi - lo)
    px = lambda v: ox + (v - lo) * sc * 0.95
    py = lambda v: oy - (v - lo) * sc * 0.55
    # 一致線
    dash(d, px(lo), py(lo), px(hi), py(hi), LGRAY, 2, 9, 6)
    ctext(d, px(0.38), py(0.38) - 14, "一致線", FT, LGRAY, "lm")
    # 点: 一致線から一定量ずれつつ傾きは揃う(バイアス)。No.1だけ外れる
    data = [(0.27, 0.30, "1", True), (0.30, 0.315, "2", False),
            (0.315, 0.325, "3", False), (0.33, 0.34, "4", False),
            (0.35, 0.358, "7", False), (0.365, 0.372, "8", False)]
    reg = []
    for (cxv, cyv, lb, off) in data:
        col = RED if off else BLUE
        node(d, px(cxv), py(cyv), 5, col, col)
        ctext(d, px(cxv) + 10, py(cyv) + 4, "No.%s" % lb, FT, col, "lm")
        if not off:
            reg.append((px(cxv), py(cyv)))
    # 回帰的な破線(バイアスで平行にずれる)
    dash(d, reg[0][0] - 10, reg[0][1] - 6, reg[-1][0] + 10, reg[-1][1] - 6, BLUE, 2, 8, 5)
    note(d, "共通のバイアス誤差は平均で消えない・実験値を計算で補正しない／相対変化は使える")
    save(im, "t1f8DragScatter")


# ============================================================ 15. ストローハル数(カルマン渦)
def f_strouhal():
    im, d = new()
    title(d, "非定常評価：カルマン渦とストローハル数 St=fL/U")
    # 円柱
    ccx, ccy, cr = 150, 220, 26
    d.ellipse((ccx - cr, ccy - cr, ccx + cr, ccy + cr), outline=BLACK, width=3, fill=FILL2)
    ctext(d, ccx, ccy + cr + 16, "円柱 径L", FT, BLACK)
    # 流入
    for k in range(3):
        arrow(d, 60, ccy - 26 + k * 26, ccx - cr - 6, ccy - 26 + k * 26, BLUE, 2, 9)
    ctext(d, 75, ccy - 52, "U", FS, BLUE)
    # 後流の交互渦
    x = ccx + cr + 30
    for i in range(5):
        cw = (i % 2 == 0)
        cy = ccy - 22 if cw else ccy + 22
        swirl(d, x + i * 78, cy, 20, cw, ORANGE, 2)
    ctext(d, ccx + 250, ccy + 70, "交互に渦を放出（周波数 f）", FT, ORANGE)
    fbox(d, 335, 360, 620, 46,
         "St = f·L / U （f: 渦放出周波数, L: 代表長さ, U: 代表速度）\n非定常RANS/LESは時間平均で、周期現象は St など代表値で比較",
         (240, 244, 250), FT)
    save(im, "t1f8Strouhal")


# ============================================================ 16. プログラム検証の代表例題
def f_verify_cases():
    im, d = new()
    title(d, "プログラム検証の代表例題と着目点")
    cards = [
        ("キャビティ流れ", "中心軸の速度・渦度\n（層流）", 130, 140),
        ("バックステップ", "剥離・再付着距離\n後方循環域", 335, 140),
        ("ポアズイユ流れ", "解析解と比較\nメッシュ収束", 540, 140),
        ("円柱・角柱", "空気力・圧力係数\n統計量・可視化", 230, 285),
        ("翼形状", "圧力分布\n抗力・揚力係数", 445, 285),
    ]
    for (t, s, cx, cy) in cards:
        fbox(d, cx, cy, 190, 96, t + "\n" + s, (238, 242, 250), FT)
        # タイトル行を強調(上段)
        ctext(d, cx, cy - 32, t, FS, BLUE)
    note(d, "性質の分かった標準問題で適用範囲・精度を把握してから設計に適用する")
    save(im, "t1f8VerifyCases")


if __name__ == "__main__":
    f_three_errors(); f_ver_val(); f_grid_convergence(); f_helmholtz()
    f_flow_meas(); f_piv_cfd(); f_schemes(); f_stall(); f_rankine()
    f_secondary(); f_eddy_viscosity(); f_les_comp(); f_les_grid()
    f_drag_scatter(); f_strouhal(); f_verify_cases()
    print("done t1f8 (16)")
