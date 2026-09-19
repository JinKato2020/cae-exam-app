# -*- coding: utf-8 -*-
"""熱流体力学1級 第6章「設計応用」公式・用語図 20枚。figlibで白地660x420線画。
公式図は回答後扱いのため結論(Cp値・評価量など)を描いてよい。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_t1e6 import dash, box, fbox, curve, swirl, wavy


# ---- 1. 多目的最適化とトレードオフ
def f_multiobjective():
    im, d = new()
    title(d, "多目的最適化：トレードオフ(競合)と妥協解")
    ox, oy = 110, 340
    axes(d, ox, oy, 400, 250, "目的1(例:軽さ)", "目的2(例:強さ)")
    fr = [(ox + 30, oy - 220), (ox + 70, oy - 150), (ox + 140, oy - 100),
          (ox + 240, oy - 65), (ox + 360, oy - 45)]
    curve(d, fr, BLUE, 3)
    for p in fr:
        node(d, p[0], p[1], 6, BLUE, BLUE)
    ctext(d, ox + 250, oy - 130, "パレート的フロンティア(妥協解)", FT, BLUE)
    # 支配される(劣った)点
    for px, py in [(ox + 150, oy - 190), (ox + 230, oy - 160), (ox + 300, oy - 130)]:
        node(d, px, py, 5, GRAY, GRAY)
    ctext(d, ox + 300, oy - 195, "劣った(支配される)点", FT, GRAY)
    fbox(d, 470, 110, 300, 46, "定義=設計変数・目的関数・制約条件\n得た後もモデル化を見直し再計算", (240, 244, 250), FT)
    save(im, "t1f6MultiObjective")


# ---- 2. 応答曲面法と実験計画法
def f_rsm():
    im, d = new()
    title(d, "応答曲面法：少数点をCFD→近似曲面で多数評価")
    ox, oy = 110, 330
    axes(d, ox, oy, 420, 240, "設計変数", "目的関数")
    # 実サンプル点(実験計画法で配置)
    sx = [ox + 40, ox + 130, ox + 230, ox + 330, ox + 400]
    sy = [oy - 60, oy - 160, oy - 120, oy - 190, oy - 100]
    # 近似曲面(2次曲線)
    import numpy as _np
    xs = _np.array(sx, float); ys = _np.array(sy, float)
    cs = _np.polyfit(xs, ys, 2)
    cv = [(float(x), float(_np.polyval(cs, x))) for x in _np.linspace(sx[0], sx[-1], 100)]
    d.line(cv, fill=GREEN, width=3, joint="curve")
    for x, y in zip(sx, sy):
        node(d, x, y, 6, RED, RED)
        d.line((x, y, x, oy), fill=LGRAY, width=1)
    ctext(d, ox + 250, oy - 220, "近似曲面(応答曲面)", FT, GREEN)
    ctext(d, ox + 60, oy - 40, "●=CFDした点", FT, RED, "lm")
    fbox(d, 470, 100, 300, 46, "点は実験計画法で最適配置\n精度不足なら曲面を更新して反復", (240, 248, 240), FT)
    save(im, "t1f6RSM")


# ---- 3. 遺伝的アルゴリズムと関数評価回数
def f_ga():
    im, d = new()
    title(d, "遺伝的アルゴリズム：評価回数 ≈ 個体数 × 世代数")
    gens = ["第1世代", "第2世代", "第3世代", "…", "第Ngen世代"]
    for g, gx in enumerate(range(70, 590, 120)):
        ctext(d, gx + 35, 90, gens[g], FT, BLACK)
        for k in range(4):
            cy = 130 + k * 45
            col = (BLUE if (g + k) % 2 else GREEN)
            node(d, gx + 35, cy, 9, (230, 235, 250), col)
        if g < 4:
            arrow(d, gx + 60, 200, gx + 100, 200, GRAY, 2, 10)
    ctext(d, 300, 170, "選択・交叉・突然変異", FT, GRAY)
    ctext(d, 105, 330, "1世代=全個体を評価", FT, BLACK, "lm")
    fbox(d, 330, 375, 560, 40, "N_eval ≈ N_pop × N_gen（多点探査で局所解に強いが評価回数は多い）", (240, 244, 250), FS)
    save(im, "t1f6GA")


# ---- 4. 旋回失速・逆流
def f_rotating_stall():
    im, d = new()
    title(d, "部分流量運転：旋回失速(非軸対称)と逆流")
    cx, cy = 250, 220
    # 環状の羽根車(全周)
    d.ellipse((cx - 130, cy - 130, cx + 130, cy + 130), outline=BLACK, width=2)
    d.ellipse((cx - 45, cy - 45, cx + 45, cy + 45), outline=BLACK, width=2, fill=FILL1)
    ctext(d, cx, cy, "羽根車", FT, BLACK)
    for a in range(0, 360, 30):
        r0, r1 = 45, 130
        x0 = cx + r0 * math.cos(math.radians(a)); y0 = cy + r0 * math.sin(math.radians(a))
        x1 = cx + r1 * math.cos(math.radians(a + 18)); y1 = cy + r1 * math.sin(math.radians(a + 18))
        d.line((x0, y0, x1, y1), fill=LGRAY, width=2)
    # 失速セル(一部の流路)
    for a in (60, 90, 120):
        mx = cx + 90 * math.cos(math.radians(a)); my = cy + 90 * math.sin(math.radians(a))
        swirl(d, mx, my, 16, True, RED, 2)
    ctext(d, cx, cy - 155, "失速セル", FT, RED)
    # 周方向に伝播
    d.arc((cx - 150, cy - 150, cx + 150, cy + 150), 200, 300, fill=RED, width=2)
    arrow(d, cx - 130, cy + 75, cx - 110, cy + 110, RED, 2, 11)
    ctext(d, cx - 150, cy + 130, "周方向へ伝播", FT, RED, "lm")
    fbox(d, 520, 210, 240, 130, "非軸対称ゆえ\n1流路+周期境界では\n表せない\n→全周モデル化\n上下流も広く取る", (255, 236, 236), FT, RED)
    save(im, "t1f6RotatingStall")


# ---- 5. 漏れ流れ(ライナーリング・バランスホール)
def f_leakage_flow():
    im, d = new()
    title(d, "漏れ流れ：高圧の出口 → 低圧の入口へ還流")
    cl = 360
    dash(d, 60, cl, 610, cl, GRAY, 2, 10, 6)
    # 羽根車流路
    shroud = [(150, 300), (170, 250), (200, 200), (240, 165), (285, 150)]
    hub = [(150, 350), (200, 335), (250, 290), (290, 220), (315, 155)]
    curve(d, shroud, BLACK, 3); curve(d, hub, BLACK, 3)
    ctext(d, 220, 250, "羽根車", FS, BLACK)
    ctext(d, 300, 130, "出口(高圧)", FT, RED)
    ctext(d, 95, 330, "入口(低圧)", FT, BLUE)
    # 主流
    arrow(d, 180, 320, 280, 165, RED, 2, 11)
    # ライナーリング隙間の漏れ(出口高圧→入口へ)
    d.line((150, 296, 150, 250), fill=ORANGE, width=2)
    arrow(d, 150, 250, 150, 300, ORANGE, 2, 10)
    ctext(d, 90, 240, "ライナーリング\nの隙間漏れ", FT, ORANGE, "lm")
    # バランスホール(後円板の穴で還流)
    d.line((320, 200, 320, 320), fill=BLACK, width=2)
    d.ellipse((315, 250, 325, 275), outline=ORANGE, width=2)
    arrow(d, 320, 250, 320, 320, ORANGE, 2, 10)
    ctext(d, 335, 300, "バランスホール\n(スラスト調整穴)", FT, ORANGE, "lm")
    fbox(d, 490, 130, 240, 50, "設計点では小さいが\n部分流量では効いてくる", (255, 244, 232), FT, ORANGE)
    save(im, "t1f6LeakageFlow")


# ---- 6. 正規化ヘリシティ
def f_helicity():
    im, d = new()
    title(d, "正規化ヘリシティ Hn：縦渦の芯を可視化")
    # 渦管(らせん)
    cx, cy = 230, 250
    pts = []
    for i in range(120):
        t = i / 120
        ang = t * 6 * math.pi
        pts.append((cx - 130 + t * 260, cy + 55 * math.sin(ang)))
    d.line(pts, fill=LGRAY, width=2, joint="curve")
    ctext(d, cx, cy + 100, "渦管(縦渦)の芯", FT, GRAY)
    # 速度ベクトルuと渦度ベクトルωが揃う
    ax, ay = 180, 250
    arrow(d, ax, ay, ax + 115, ay - 42, BLUE, 3, 13)
    ctext(d, ax + 125, ay - 46, "速度 u", FS, BLUE, "lm")
    arrow(d, ax, ay + 6, ax + 100, ay - 24, RED, 3, 13)
    ctext(d, ax + 55, ay + 28, "渦度 ω=∇×u", FT, RED)
    fbox(d, 480, 120, 300, 78, "Hn = (u・ω)/(|u||ω|)\n= u と ω のなす角の余弦\n平行なほど ±1 → 縦渦の芯", (240, 244, 250), FT)
    note(d, "値が大きい領域＝流れに沿って巻きつく縦渦。旋回の向きも分かる")
    save(im, "t1f6Helicity")


# ---- 7. 逆圧力勾配と境界層剥離
def f_adverse_pressure():
    im, d = new()
    title(d, "逆圧力勾配：壁際の遅い流れが押し戻され剥離")
    # 拡大する壁(減速→静圧上昇)
    d.line((90, 150, 590, 110), fill=BLACK, width=3)
    wy = [300, 300, 305, 315, 330, 345]
    xs = [90, 190, 290, 380, 470, 560]
    curve(d, list(zip(xs, wy)), BLACK, 3)
    ctext(d, 330, 360, "壁(減速する流路)", FT, GRAY)
    # 圧力が下流ほど上昇
    arrow(d, 150, 130, 250, 128, GRAY, 2, 10)
    ctext(d, 330, 122, "静圧が下流ほど上昇 → 逆圧力勾配", FT, BLACK)
    # 境界層速度プロファイル(下流ほど反転)
    profs = [(180, 8), (300, 4), (430, -1), (520, -5)]
    for bx, top in profs:
        yb = 300 if bx < 300 else (305 if bx < 380 else (330 if bx < 500 else 345))
        # 参照: 壁面近似
        for k in range(6):
            yy = yb - k * 8
            u = (top) * (k / 5) * (2 - k / 5)
            col = RED if u < 0 else BLUE
            arrow(d, bx, yy, bx + max(6, abs(u) * 6) * (1 if u >= 0 else -1), yy, col, 1, 6)
    swirl(d, 545, 320, 14, False, RED, 2)
    ctext(d, 545, 290, "剥離(逆流)", FT, RED)
    note(d, "翼面(特に低圧側)の圧力分布で急勾配を探し剥離を把握する")
    save(im, "t1f6AdversePressure")


# ---- 8. 2次流れとコーナー剥離
def f_secondary_flow():
    im, d = new()
    title(d, "2次流れ：低エネルギー流体を隅へ集めコーナー剥離")
    # 流路断面(矩形ダクト)
    box(d, 170, 90, 490, 330, "white")
    ctext(d, 330, 350, "流路断面(羽根とケーシングの隅)", FT, GRAY)
    # 主流(紙面手前へ)＝×印
    ctext(d, 330, 200, "主流(奥へ)", FT, BLACK)
    d.ellipse((315, 215, 345, 245), outline=BLACK, width=2)
    d.line((320, 220, 340, 240), fill=BLACK, width=2)
    d.line((340, 220, 320, 240), fill=BLACK, width=2)
    # 2次流れの循環(隅へ向かう矢印)
    for (x0, y0, x1, y1) in [(200, 110, 250, 150), (460, 110, 410, 150),
                             (200, 310, 250, 270), (460, 310, 410, 270)]:
        arrow(d, x0, y0, x1, y1, BLUE, 2, 10)
    ctext(d, 250, 120, "2次流れ", FT, BLUE, "lm")
    # コーナーに高損失流体
    for (cx, cy) in [(185, 105), (475, 105), (185, 315), (475, 315)]:
        d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=RED, width=2, fill=(255, 228, 228))
    ctext(d, 250, 320, "コーナーに高損失流体→剥離", FT, RED, "lm")
    fbox(d, 570, 210, 150, 70, "限界流線・\n全圧コンターで\n損失源を特定", (255, 236, 236), FT, RED)
    save(im, "t1f6SecondaryFlow")


# ---- 9. 静圧回復係数
def f_pressure_recovery():
    im, d = new()
    title(d, "ディフューザの静圧回復係数 Cp = 1 − 1/AR²")
    x0, x1 = 130, 470
    d.line((x0, 175, x1, 120), fill=BLACK, width=3)
    d.line((x0, 245, x1, 300), fill=BLACK, width=3)
    d.line((x0, 175, x0, 245), fill=BLACK, width=2)
    d.line((x1, 120, x1, 300), fill=BLACK, width=2)
    arrow(d, x0 + 8, 210, x0 + 50, 210, BLUE, 2, 9)
    ctext(d, x0 - 6, 210, "U1", FT, BLUE, "rm")
    arrow(d, 360, 210, 420, 210, BLUE, 6, 16)
    ctext(d, x1 + 6, 210, "U2", FT, BLUE, "lm")
    dim(d, x0 - 24, 175, x0 - 24, 245, "A1", col=GRAY)
    dim(d, x1 + 24, 120, x1 + 24, 300, "A2", col=GRAY)
    fbox(d, 330, 360, 560, 52, "連続式 U2=U1/AR ＋ ベルヌーイ → Cp=1−(U2/U1)²=1−1/AR²\nAR=2 なら Cp=0.75（実機は剥離・2次流れで低下）", (240, 244, 250), FT)
    save(im, "t1f6PressureRecovery")


# ---- 10. 全圧損失と後処理
def f_total_pressure_loss():
    im, d = new()
    title(d, "全圧損失：p0=p+½ρU² は下流で減少")
    ox, oy = 110, 300
    axes(d, ox, oy, 420, 200, "流れ方向", "圧力")
    # 全圧(減少)
    curve(d, [(ox + 20, oy - 170), (ox + 150, oy - 160), (ox + 300, oy - 130), (ox + 400, oy - 95)], RED, 3)
    ctext(d, ox + 300, oy - 155, "全圧 p0(損失で減少)", FT, RED)
    # 静圧(回復で上昇)
    curve(d, [(ox + 20, oy - 40), (ox + 150, oy - 70), (ox + 300, oy - 95), (ox + 400, oy - 105)], BLUE, 3)
    ctext(d, ox + 260, oy - 40, "静圧 p(回復で上昇)", FT, BLUE)
    # 差=動圧
    d.line((ox + 400, oy - 95, ox + 400, oy - 105), fill=GRAY, width=1)
    fbox(d, 330, 375, 560, 40, "ζ = (p0,in − p0,out)/(½ρU_ref²)。全圧コンターで損失源(隅)を特定", (240, 244, 250), FS)
    save(im, "t1f6TotalPressureLoss")


# ---- 11. 摩擦抗力支配 と 形状抗力支配
def f_drag_types():
    im, d = new()
    title(d, "摩擦抗力支配(流線形) と 形状抗力支配(ブラフ体)")
    # 左：流線形(摩擦抗力)
    af = [(60, 200), (110, 178), (180, 182), (240, 200), (180, 210), (110, 208), (60, 200)]
    curve(d, af, BLACK, 3)
    dash(d, 70, 190, 230, 192, GREEN, 2, 6, 4)
    dash(d, 70, 208, 230, 208, GREEN, 2, 6, 4)
    ctext(d, 150, 158, "薄い付着境界層", FT, GREEN)
    ctext(d, 150, 250, "航空機(流線形)", FS, BLACK)
    ctext(d, 150, 275, "→摩擦抗力が主・境界層予測が命", FT, GREEN)
    # 右：ブラフ体(形状抗力)
    box(d, 400, 130, 470, 270, (238, 240, 245))
    swirl(d, 505, 175, 20, True, RED, 2)
    swirl(d, 510, 240, 20, False, RED, 2)
    ctext(d, 435, 200, "＋", F, BLACK)
    ctext(d, 495, 200, "−", F, BLACK)
    ctext(d, 435, 300, "ビル・自動車(ブラフ体)", FS, BLACK)
    ctext(d, 500, 325, "→前後の圧力差=形状抗力が主", FT, RED)
    note(d, "はく離させない設計=圧力差小=摩擦抗力主。角ではく離=圧力差大=形状抗力主")
    save(im, "t1f6DragTypes")


# ---- 12. 抗力係数と前面投影面積
def f_drag_coeff():
    im, d = new()
    title(d, "抗力係数 CD = D/(½ρU²A)、A=前面投影面積")
    # 車の側面
    hwall(d, 60, 400, 300, side=1, n=12)
    body = [(110, 280), (120, 200), (160, 165), (350, 160), (365, 280)]
    curve(d, body, BLACK, 3)
    d.line((110, 280, 365, 280), fill=BLACK, width=2)
    for tx in (170, 320):
        d.ellipse((tx - 18, 280 - 18, tx + 18, 280 + 18), outline=BLACK, width=2)
    for yy in (185, 220, 255):
        arrow(d, 55, yy, 100, yy, BLUE, 2, 10)
    ctext(d, 75, 300, "U", FS, BLUE)
    # 前面投影面積 A(高さ方向の寸法)
    dim(d, 95, 165, 95, 280, "A", col=GRAY)
    ctext(d, 240, 130, "前面投影面積 A", FT, GRAY)
    fbox(d, 500, 200, 250, 100, "抵抗 D=½ρU²A・CD\nAを小さく または\n形を整えCDを下げる\n両者の積が効く", (240, 244, 250), FT)
    save(im, "t1f6DragCoeff")


# ---- 13. カルマン渦とストローハル数・渦励振
def f_strouhal():
    im, d = new()
    title(d, "カルマン渦：St=fD/U≈0.2、f=St・U/D と渦励振")
    for yy in (130, 165, 200):
        arrow(d, 40, yy, 95, yy, BLUE, 2, 10)
    ctext(d, 65, 112, "U", FS, BLUE)
    ccx, ccy, r = 140, 165, 24
    d.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=BLACK, width=3, fill=FILL1)
    dim(d, ccx - r, ccy + r + 22, ccx + r, ccy + r + 22, "D", col=GRAY)
    for i, x in enumerate((215, 275, 335, 395)):
        up = (i % 2 == 0)
        swirl(d, x, ccy - 35 if up else ccy + 35, 15, cw=up, col=RED, wd=2)
    ctext(d, 300, 235, "周波数 f=St・U/D", FT, RED)
    # 共振曲線(渦励振)
    ox, oy = 440, 320
    axes(d, ox, oy, 180, 150, "f", "振幅")
    peak = ox + 90
    cv = [(ox + t, oy - 120 * math.exp(-((ox + t - peak) / 22) ** 2)) for t in range(0, 180, 4)]
    d.line(cv, fill=RED, width=3, joint="curve")
    dash(d, peak, oy, peak, oy - 130, GRAY, 1, 4, 4)
    ctext(d, peak, oy - 145, "固有振動数付近", FT, RED)
    ctext(d, peak + 10, oy - 60, "渦励振(共振)", FT, RED, "lm")
    save(im, "t1f6Strouhal")


# ---- 14. 空力騒音(ピーク音)と対策
def f_aeronoise():
    im, d = new()
    title(d, "空力騒音：規則的な渦=ピーク音 → 渦を乱して散らす")
    # 左：規則的な渦→単一周波数ピーク
    d.line((70, 90, 70, 300), fill=BLACK, width=6)
    for i, yy in enumerate((130, 180, 230)):
        swirl(d, 70 + (30 if i % 2 == 0 else -30), yy, 13, cw=(i % 2 == 0), col=RED, wd=2)
    ctext(d, 70, 320, "規則的な渦放出", FT, RED)
    ox, oy = 40, 400
    axes(d, ox, oy, 200, 60, "周波数", "音圧")
    d.line((ox + 90, oy, ox + 90, oy - 55), fill=RED, width=3)
    ctext(d, ox + 90, oy - 68, "単一周波数のピーク音", FT, RED)
    # 右：螺旋で乱す→広帯域
    d.line((420, 90, 420, 300), fill=BLACK, width=6)
    for k in range(8):
        yy = 100 + k * 25
        d.line((420 - 11, yy, 420 + 11, yy + 12), fill=GREEN, width=2)
    for yy, off in [(140, 32), (185, -28), (235, 30)]:
        swirl(d, 420 + off, yy, 10, cw=(off > 0), col=ORANGE, wd=2)
    ctext(d, 420, 320, "螺旋で渦を軸方向にずらす", FT, ORANGE)
    ox2 = 400
    axes(d, ox2, oy, 200, 60, "周波数", "音圧")
    cv = [(ox2 + t, oy - (20 + 8 * math.sin(t * 0.3))) for t in range(10, 195, 5)]
    d.line(cv, fill=ORANGE, width=2, joint="curve")
    ctext(d, ox2 + 100, oy - 70, "音を散らす(広帯域化)", FT, ORANGE)
    save(im, "t1f6AeroNoise")


# ---- 15. 排気口の数値不安定と対策
def f_outlet_stability():
    im, d = new()
    title(d, "排気口の数値不安定：固定条件の弊害と対策")
    # 上段：固定速度→圧力反射
    y = 130
    fbox(d, 170, y, 200, 46, "固定速度境界", (235, 240, 250), FT)
    arrow(d, 270, y, 330, y, BLACK, 2, 11)
    fbox(d, 430, y, 220, 46, "圧力反射で不安定", (255, 236, 236), FT, RED)
    # 下段：固定圧力→逆流
    y2 = 210
    fbox(d, 170, y2, 200, 46, "固定圧力境界", (235, 240, 250), FT)
    arrow(d, 270, y2, 330, y2, BLACK, 2, 11)
    fbox(d, 430, y2, 220, 46, "逆流速度で不安定", (255, 236, 236), FT, RED)
    # 対策
    fbox(d, 330, 320, 560, 76,
         "対策：排気口近傍に人工的な数値粘性\n外部に急拡大・管路など圧力損失部を付加\n最下流ゆえ室内気流全体への影響は小さい", (240, 248, 240), FT, GREEN)
    save(im, "t1f6OutletStability")


# ---- 16. 室内熱環境の熱源と熱輸送
def f_room_heat():
    im, d = new()
    title(d, "室内熱環境：熱源・吸熱源 と 対流・放射・伝導")
    box(d, 80, 80, 590, 330, "white")
    # 熱源
    d.rectangle((80, 120, 92, 210), outline=BLUE, width=2)
    arrow(d, 92, 150, 140, 168, ORANGE, 2, 9); ctext(d, 150, 130, "日射", FT, ORANGE, "lm")
    box(d, 300, 82, 355, 94, (255, 250, 220)); ctext(d, 327, 106, "照明", FT, ORANGE)
    ctext(d, 250, 300, "人体", FT, BLACK)
    d.ellipse((242, 250, 258, 266), outline=BLACK, width=2)
    d.line((250, 266, 250, 295), fill=BLACK, width=3)
    # 吸熱源
    box(d, 470, 82, 525, 94, (225, 235, 250)); ctext(d, 497, 70, "冷房(吸熱)", FT, BLUE)
    for xx in (485, 505):
        arrow(d, xx, 94, xx - 8, 140, BLUE, 2, 9)
    # 3輸送: 対流・放射・伝導
    arrow(d, 400, 280, 400, 190, BLUE, 2, 10); ctext(d, 400, 300, "対流", FT, BLUE)
    wavy(d, 262, 258, 330, 250, ORANGE, 2, 4, 5); ctext(d, 345, 246, "放射", FT, ORANGE, "lm")
    arrow(d, 200, 328, 200, 352, GRAY, 2, 9); ctext(d, 200, 366, "伝導(壁・床)", FT, GRAY)
    fbox(d, 500, 250, 150, 70, "対流+放射+伝導\nの3つで輸送\n対流だけは誤り", (240, 244, 250), FT)
    save(im, "t1f6RoomHeat")


# ---- 17. 吸込渦と対策
def f_suction_vortex():
    im, d = new()
    title(d, "ポンプ吸込み水槽：水中渦・空気吸込み渦と対策")
    d.line((80, 130, 80, 350), fill=BLACK, width=3)
    d.line((540, 130, 540, 350), fill=BLACK, width=3)
    d.line((80, 350, 540, 350), fill=BLACK, width=3)
    wy = 160
    d.line([(80 + i * 9, wy + 4 * math.sin(i * 0.6)) for i in range(52)], fill=BLUE, width=2)
    ctext(d, 130, wy - 14, "自由表面", FT, BLUE, "lm")
    # ベルマウス+取水管
    bx = 300
    d.line((bx - 50, 350, bx - 20, 315), fill=BLACK, width=3)
    d.line((bx + 50, 350, bx + 20, 315), fill=BLACK, width=3)
    d.line((bx - 20, 315, bx - 20, 90), fill=BLACK, width=3)
    d.line((bx + 20, 315, bx + 20, 90), fill=BLACK, width=3)
    arrow(d, bx, 300, bx, 110, BLUE, 3, 12)
    ctext(d, bx, 76, "取水管内の旋回速度成分↑", FT, BLUE)
    # 水中渦(キャビ)
    swirl(d, 200, 320, 16, True, RED, 2)
    ctext(d, 175, 300, "水中渦(キャビ)", FT, RED, "rm")
    # 空気吸込み渦(水面→ベルマウス)
    swirl(d, 370, 210, 14, False, RED, 2)
    dash(d, 370, 196, 370, 165, RED, 1, 4, 4)
    ctext(d, 390, 205, "空気吸込み渦", FT, RED, "lm")
    # 対策(邪魔板)
    d.line((430, 350, 430, 300), fill=GREEN, width=4)
    ctext(d, 460, 320, "邪魔板・多孔板", FT, GREEN, "lm")
    note(d, "評価量=圧力損失と旋回速度成分。渦中心位置の可視化も行う")
    save(im, "t1f6SuctionVortex")


# ---- 18. 自由表面のすべり壁近似
def f_free_surface():
    im, d = new()
    title(d, "自由表面：すべり壁近似(単相・非圧縮・定常)")
    # 左：近似(すべり壁)
    box(d, 60, 120, 300, 340, "white")
    d.line((60, 150, 300, 150), fill=GRAY, width=4)
    for xx in range(70, 300, 22):
        d.line((xx, 150, xx - 10, 138), fill=GRAY, width=1)
    ctext(d, 180, 130, "水面=すべり壁", FT, GRAY)
    arrow(d, 100, 200, 100, 300, BLUE, 2, 10)
    ctext(d, 180, 250, "単相・非圧縮\n定常で軽く解く", FT, BLACK)
    ctext(d, 180, 356, "実用の近似計算", FS, BLACK)
    # 右：詳細(自由表面=気液界面)
    box(d, 360, 120, 600, 340, "white")
    surf = [(360 + i * 12, 175 + 12 * math.sin(i * 0.9)) for i in range(21)]
    d.line(surf, fill=BLUE, width=3)
    ctext(d, 480, 140, "自由表面(気液界面)", FT, BLUE)
    ctext(d, 480, 210, "気相", FT, GRAY)
    ctext(d, 480, 260, "液相", FT, BLUE)
    swirl(d, 480, 300, 14, True, RED, 2)
    ctext(d, 480, 356, "詳細評価＋キャビテーションモデル", FT, BLACK)
    note(d, "ふつうはすべり壁で軽く。詳細評価や間欠的な渦は自由表面＋非定常で解く")
    save(im, "t1f6FreeSurface")


# ---- 19. 渦粘性型2方程式モデルの限界(浮力を伴う熱対流)
def f_buoyancy_limit():
    im, d = new()
    title(d, "渦粘性型の限界：壁平行方向の乱流熱流束は表せない")
    # 垂直高温面
    d.line((150, 90, 150, 350), fill=RED, width=6)
    ctext(d, 130, 366, "垂直な高温面", FT, RED, "rm")
    for yy in (140, 190, 240, 290):
        d.line((150, yy, 140, yy), fill=RED, width=2)
    # 壁平行方向の乱流熱流束=表せない(壁ぎわ・上向き)
    arrow(d, 170, 280, 170, 200, GREEN, 2, 10)
    ctext(d, 300, 95, "壁平行方向の乱流熱流束 u'θ'（渦粘性型では表せない）", FT, GREEN)
    d.line((170, 200, 240, 118), fill=GREEN, width=1)
    # 浮力による上昇流(さらに右)
    for xx in (225, 245):
        arrow(d, xx, 330, xx, 150, ORANGE, 2, 10)
    ctext(d, 320, 200, "浮力による上昇流\n(浮力を伴う熱対流)", FT, ORANGE, "lm")
    # 温度勾配方向(壁垂直)=渦粘性型で表せる
    arrow(d, 158, 310, 220, 310, BLUE, 2, 10)
    ctext(d, 230, 328, "温度勾配方向 → 渦粘性型で可", FT, BLUE, "lm")
    fbox(d, 490, 250, 300, 56, "浮力生成項 Gk=βgi・u'θ'\n平行方向成分は補助式で補う", (255, 236, 236), FT, RED)
    save(im, "t1f6BuoyancyLimit")


# ---- 20. 流体解析を進める3つの視点
def f_three_views():
    im, d = new()
    title(d, "流体解析を進める3つの視点")
    cols = [
        ("(1) 解析の対象と目的", ["何を", "何のために解くか", "の明確化"], (235, 240, 250)),
        ("(2) 数値解析技術", ["手法・高速化", "乱流/物理モデル", "CAD・メッシュ", "境界/初期条件", "精度・ポスト処理", "信頼性評価"], (240, 248, 240)),
        ("(3) 物理現象の評価", ["境界層・二次流れ", "圧力場・速度", "剥離逆流・渦構造", "非定常性・特異現象", "性能パラメータ", "実験との比較"], (255, 244, 232)),
    ]
    xs = [130, 330, 530]
    for (cx, (head, items, fill)) in zip(xs, cols):
        box(d, cx - 92, 70, cx + 92, 340, fill)
        ctext(d, cx, 92, head, FT, BLACK)
        d.line((cx - 80, 108, cx + 80, 108), fill=LGRAY, width=1)
        for i, it in enumerate(items):
            ctext(d, cx, 132 + i * 30, "・" + it, FT, GRAY)
    arrow(d, 226, 205, 234, 205, BLACK, 3, 12)
    arrow(d, 426, 205, 434, 205, BLACK, 3, 12)
    note(d, "オペレータに終わらず、対象に即したモデル化と結果の考察を行う枠組み")
    save(im, "t1f6ThreeViews")


if __name__ == "__main__":
    f_multiobjective(); f_rsm(); f_ga(); f_rotating_stall(); f_leakage_flow()
    f_helicity(); f_adverse_pressure(); f_secondary_flow(); f_pressure_recovery(); f_total_pressure_loss()
    f_drag_types(); f_drag_coeff(); f_strouhal(); f_aeronoise(); f_outlet_stability()
    f_room_heat(); f_suction_vortex(); f_free_surface(); f_buoyancy_limit(); f_three_views()
    print("done t1f6 (20)")
