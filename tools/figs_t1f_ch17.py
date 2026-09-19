# -*- coding: utf-8 -*-
"""熱流体力学1級 第17章「燃焼の基礎1」の公式・用語図(t1f17*・21枚)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。問題図(t1e17*)とは別ファイル。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(phi, alpha, nu, rho, sigma, Cp, lambda, CH4, O2, N2, R0, Y_i, X_k, W_k, ^, ->, <<, div, grad 等)。
公式図なので定義式・関係式を明示してよい(問題図の required 制約は無い)。"""
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


def pcircle(d, x, y, r, fill=FILL1, col=BLACK, wd=2):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=wd, fill=fill)


def box(d, x0, y0, x1, y1, fill=FILL1, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=wd, fill=fill)


def eqbox(d, cx, cy, s, w=520, h=52, col=BLACK, fill=FILL2, fnt=F):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ctext(d, cx, cy, s, fnt, col)


# ============================================================
# 17-1 t1f17AirFuelRatio : 空燃比 A/F と 燃空比 F/A(互いに逆数)
# ============================================================
def air_fuel_ratio():
    im, d = new(); title(d, "空燃比 A/F と 燃空比 F/A: 質量の比(互いに逆数)")
    # 左: 空気の質量(大きい山)
    box(d, 55, 110, 285, 300, (235, 242, 250))
    ctext(d, 170, 132, "空気の質量 m_air", FT, BLUE)
    for (px, py, lab, col) in [(105, 185, "O2", RED), (170, 175, "N2", BLUE), (230, 190, "N2", BLUE),
                                (120, 245, "N2", BLUE), (200, 250, "N2", BLUE), (165, 220, "O2", RED)]:
        pcircle(d, px, py, 17, FILL1, col, 2); ctext(d, px, py, lab, FT, col)
    ctext(d, 170, 285, "空気は多い(分子多数)", FT, GRAY)
    # 右: 燃料の質量(小さい)
    box(d, 375, 150, 605, 300, (235, 245, 235))
    ctext(d, 490, 172, "燃料の質量 m_fuel", FT, GREEN)
    pcircle(d, 490, 235, 22, FILL1, GREEN, 2); ctext(d, 490, 235, "CH4", FS, GREEN)
    ctext(d, 490, 285, "燃料は少ない", FT, GRAY)
    # 比の式
    eqbox(d, 330, 350, "A/F = m_air / m_fuel     ,     F/A = 1 / (A/F)", 600, 50)
    note(d, "A/F が大きい=空気が多い(希薄). F/A はその逆数(燃料の割合)")
    save(im, "t1f17AirFuelRatio")


# ============================================================
# 17-2 t1f17StoichiometricAF : 理論空燃比(過不足なく完全燃焼)
# ============================================================
def stoichiometric_af():
    im, d = new(); title(d, "理論空燃比(A/F)st: 過不足なく完全燃焼させる空気量")
    # 反応式(H2 の例)
    ctext(d, 330, 80, "例) 2 H2 + O2 (+ 随伴 N2) -> 2 H2O", FS, BLACK)
    # 左: 燃料
    box(d, 45, 120, 190, 250, (235, 245, 235))
    ctext(d, 117, 142, "燃料", FT, GRAY)
    pcircle(d, 117, 190, 20, FILL1, GREEN, 2); ctext(d, 117, 190, "H2", FS, GREEN)
    ctext(d, 117, 232, "燃料質量", FT, GRAY)
    # 中: 空気(O2 1 に N2 4 が随伴)
    box(d, 220, 105, 460, 285, (235, 242, 250))
    ctext(d, 340, 122, "ちょうど必要な空気", FT, BLUE)
    pcircle(d, 275, 175, 18, (250, 235, 235), RED, 3); ctext(d, 275, 175, "O2", FT, RED)
    for (px, py) in [(335, 165), (395, 165), (335, 225), (395, 225)]:
        pcircle(d, px, py, 18, FILL1, BLUE, 2); ctext(d, px, py, "N2", FT, BLUE)
    ctext(d, 340, 265, "O2 : N2 = 1 : 4(体積)", FT, BLACK)
    # 右: 生成物(過不足なし)
    box(d, 490, 130, 620, 250, (245, 245, 245))
    ctext(d, 555, 155, "生成物", FT, GRAY)
    ctext(d, 555, 190, "2 H2O", FS, BLACK)
    ctext(d, 555, 225, "余りなし", FT, GRAY)
    arrow(d, 192, 185, 218, 185, BLACK, 3, 11)
    arrow(d, 462, 190, 488, 190, BLACK, 3, 11)
    # 式
    eqbox(d, 330, 335, "(A/F)st = (過不足なく燃やす空気質量) / (燃料質量)", 600, 46, BLACK, FILL2, FS)
    note(d, "N2 も空気質量に含める. 化学量論=余りも足りもしない基準の空燃比")
    save(im, "t1f17StoichiometricAF")


# ============================================================
# 17-3 t1f17EquivalenceRatio : 当量比 phi(燃料側の指標)
# ============================================================
def equivalence_ratio():
    im, d = new(); title(d, "当量比 phi: 化学量論を1とした燃料の過不足")
    ox, oy, xl = 90, 210, 480
    arrow(d, ox - 10, oy, ox + xl + 20, oy, BLACK, 3, 12)
    ctext(d, ox + xl + 26, oy, "phi", FS, BLACK, "lm")
    xm = ox + xl * 0.5
    d.rectangle((ox, oy - 24, xm, oy - 6), outline=BLUE, width=2, fill=(225, 235, 250))
    d.rectangle((xm, oy - 24, ox + xl, oy - 6), outline=RED, width=2, fill=(250, 230, 230))
    d.line((xm, oy - 32, xm, oy + 12), fill=BLACK, width=3)
    ctext(d, xm, oy + 28, "phi = 1", FS, BLACK)
    ctext(d, xm, oy + 50, "化学量論", FT, GRAY)
    ctext(d, ox + xl * 0.25, oy - 55, "リーン(希薄)", FS, BLUE)
    ctext(d, ox + xl * 0.25, oy + 28, "phi < 1", FT, BLUE)
    ctext(d, ox + xl * 0.25, oy + 50, "空気過剰", FT, BLUE)
    ctext(d, ox + xl * 0.75, oy - 55, "リッチ(過濃)", FS, RED)
    ctext(d, ox + xl * 0.75, oy + 28, "phi > 1", FT, RED)
    ctext(d, ox + xl * 0.75, oy + 50, "燃料過剰", FT, RED)
    eqbox(d, 330, 330, "phi = (F/O)actual / (F/O)st = (A/F)st / (A/F)actual", 610, 50, BLACK, FILL2, FS)
    note(d, "燃空比なら実÷量論, 空燃比なら量論÷実(分子分母が入れ替わる)")
    save(im, "t1f17EquivalenceRatio")


# ============================================================
# 17-4 t1f17ExcessAirRatio : 空気過剰率 lambda(空気側の指標=phi の逆数)
# ============================================================
def excess_air_ratio():
    im, d = new(); title(d, "空気過剰率 lambda = 1/phi: 理論の何倍の空気か")
    ox, oy, xl = 90, 210, 480
    arrow(d, ox - 10, oy, ox + xl + 20, oy, BLACK, 3, 12)
    ctext(d, ox + xl + 26, oy, "lambda", FS, BLACK, "lm")
    xm = ox + xl * 0.5
    # phi と逆向き: 左=過濃(lambda<1) 右=希薄(lambda>1)
    d.rectangle((ox, oy - 24, xm, oy - 6), outline=RED, width=2, fill=(250, 230, 230))
    d.rectangle((xm, oy - 24, ox + xl, oy - 6), outline=BLUE, width=2, fill=(225, 235, 250))
    d.line((xm, oy - 32, xm, oy + 12), fill=BLACK, width=3)
    ctext(d, xm, oy + 28, "lambda = 1", FS, BLACK)
    ctext(d, xm, oy + 50, "化学量論", FT, GRAY)
    ctext(d, ox + xl * 0.25, oy - 55, "空気不足(過濃)", FS, RED)
    ctext(d, ox + xl * 0.25, oy + 28, "lambda < 1", FT, RED)
    ctext(d, ox + xl * 0.75, oy - 55, "空気過剰(希薄)", FS, BLUE)
    ctext(d, ox + xl * 0.75, oy + 28, "lambda > 1", FT, BLUE)
    eqbox(d, 330, 330, "lambda = 1 / phi = (A/F)actual / (A/F)st", 560, 50)
    note(d, "phi と向きが逆. lambda は空気側の視点(希薄燃焼・内燃機関でよく使う)")
    save(im, "t1f17ExcessAirRatio")


# ============================================================
# 17-5 t1f17MoleMassFraction : モル分率 X_k と 質量分率 Y_k の変換
# ============================================================
def mole_mass_fraction():
    im, d = new(); title(d, "モル分率 X_k と 質量分率 Y_k の変換(W_bar が橋渡し)")
    # 左: 質量分率 Y_k
    box(d, 45, 95, 250, 245, (235, 245, 235))
    ctext(d, 147, 118, "質量分率 Y_k", FS, GREEN)
    ctext(d, 147, 150, "質量の割合", FT, GRAY)
    ctext(d, 147, 190, "重い成分が", FT, GRAY)
    ctext(d, 147, 215, "大きく見える", FT, GRAY)
    # 右: モル分率 X_k
    box(d, 410, 95, 615, 245, (235, 242, 250))
    ctext(d, 512, 118, "モル分率 X_k", FS, BLUE)
    ctext(d, 512, 150, "個数(物質量)の割合", FT, GRAY)
    ctext(d, 512, 190, "軽い成分が", FT, GRAY)
    ctext(d, 512, 215, "大きく見える", FT, GRAY)
    # 中央の双方向矢印 + 平均分子量
    arrow(d, 260, 155, 400, 155, BLACK, 3, 12)
    arrow(d, 400, 185, 260, 185, BLACK, 3, 12)
    ctext(d, 330, 130, "W_k と W_bar", FT, BLACK)
    ctext(d, 330, 205, "で換算", FT, GRAY)
    # 式
    eqbox(d, 330, 295, "X_k = Y_k * W_bar / W_k", 500, 46, BLACK, FILL2, FS)
    eqbox(d, 330, 355, "W_bar = 1 / sum(Y_k / W_k) = sum(X_k * W_k)", 560, 46, BLACK, (245, 245, 245), FS)
    note(d, "W_k=成分分子量, W_bar=平均分子量. 軽い成分ほどモル分率が増える")
    save(im, "t1f17MoleMassFraction")


# ============================================================
# 17-6 t1f17TransportCoefficients : 輸送物性係数(3つとも m^2/s)
# ============================================================
def transport_coefficients():
    im, d = new(); title(d, "輸送物性係数: 熱・物質・運動量の拡散(単位は共通 m^2/s)")
    cols = [("熱拡散係数 alpha", "= lambda/(rho Cp)", "熱の拡散", RED),
            ("物質拡散係数 D", "拡散方程式の係数", "物質の拡散", GREEN),
            ("動粘性係数 nu", "= mu/rho", "運動量の拡散", BLUE)]
    x0, w = 40, 193
    y0, hh = 95, 165
    for i, (name, defn, role, col) in enumerate(cols):
        cx = x0 + i * (w + 4)
        box(d, cx, y0, cx + w, y0 + hh, (248, 248, 248))
        ctext(d, cx + w / 2, y0 + 28, name, FT, col)
        d.line((cx + 12, y0 + 50, cx + w - 12, y0 + 50), fill=LGRAY, width=1)
        ctext(d, cx + w / 2, y0 + 80, defn, FT, GRAY)
        ctext(d, cx + w / 2, y0 + 112, role, FT, BLACK)
        ctext(d, cx + w / 2, y0 + 145, "m^2/s", FS, RED)
    eqbox(d, 330, 305, "3つとも単位 m^2/s -> 比をとると無次元(Pr, Sc, Le)", 600, 46, BLACK, FILL2, FS)
    note(d, "単位が揃うからこそ Pr=nu/alpha, Sc=nu/D, Le=alpha/D が無次元になる")
    save(im, "t1f17TransportCoefficients")


# ============================================================
# 17-7 t1f17PrandtlNumber : プラントル数 Pr = nu/alpha(速度層 vs 温度層)
# ============================================================
def prandtl_number():
    im, d = new(); title(d, "プラントル数 Pr = nu/alpha: 運動量拡散 と 熱拡散 の比")
    hwall(d, 60, 600, 150, 1, 12)
    ctext(d, 330, 130, "壁", FT, GRAY)
    # 速度境界層(青)
    vpts = [(60 + i * 5, 150 + 90 * math.exp(-i * 5 / 90.0)) for i in range(0, 109)]
    # 実際は境界層プロファイル: 壁で0, 上で自由流。ここは概念曲線
    d.line([(60, 300), (140, 300), (200, 260), (260, 195), (330, 175), (600, 172)], fill=BLUE, width=3, joint="curve")
    ctext(d, 470, 200, "速度境界層(nu)", FT, BLUE)
    # 温度境界層(赤・より薄い)
    d.line([(60, 300), (130, 300), (175, 250), (215, 205), (260, 190), (600, 188)], fill=RED, width=3, joint="curve")
    ctext(d, 300, 320, "温度境界層(alpha)", FT, RED)
    ctext(d, 100, 335, "壁", FT, GRAY)
    eqbox(d, 330, 370, "Pr = nu/alpha = Cp*mu/lambda   (気体で約0.7)", 600, 46, BLACK, FILL2, FS)
    note(d, "Pr>1 なら熱が伝わりにくく温度境界層が速度境界層より薄くなる")
    save(im, "t1f17PrandtlNumber")


# ============================================================
# 17-8 t1f17SchmidtNumber : シュミット数 Sc = nu/D(速度層 vs 濃度層)
# ============================================================
def schmidt_number():
    im, d = new(); title(d, "シュミット数 Sc = nu/D: 運動量拡散 と 物質拡散 の比")
    hwall(d, 60, 600, 150, 1, 12)
    d.line([(60, 300), (140, 300), (200, 260), (260, 195), (330, 175), (600, 172)], fill=BLUE, width=3, joint="curve")
    ctext(d, 470, 200, "速度境界層(nu)", FT, BLUE)
    d.line([(60, 300), (135, 300), (178, 252), (218, 208), (262, 192), (600, 190)], fill=GREEN, width=3, joint="curve")
    ctext(d, 300, 320, "濃度境界層(D)", FT, GREEN)
    ctext(d, 100, 335, "壁", FT, GRAY)
    eqbox(d, 330, 370, "Sc = nu/D = mu/(rho*D)   (気体で約0.7〜1)", 600, 46, BLACK, FILL2, FS)
    note(d, "Pr の『熱』を『物質』に置換した数. Sc 大で濃度境界層が薄くなる")
    save(im, "t1f17SchmidtNumber")


# ============================================================
# 17-9 t1f17LewisNumber : ルイス数 Le = alpha/D(火炎面での熱と物質)
# ============================================================
def lewis_number():
    im, d = new(); title(d, "ルイス数 Le = alpha/D: 熱の拡散 と 物質の拡散 の比")
    fx = 330
    for yy in range(110, 320, 16):
        d.line((fx, yy, fx, yy + 9), fill=ORANGE, width=4)
    ctext(d, fx, 98, "火炎面", FT, ORANGE)
    ctext(d, 165, 125, "熱の拡散", FS, RED)
    ctext(d, 165, 150, "(alpha)", FT, RED)
    for yy in [185, 225, 265]:
        arrow(d, 120, yy, fx - 20, yy, RED, 3, 12)
    ctext(d, 150, 300, "既燃側から予熱", FT, GRAY)
    ctext(d, 495, 125, "反応物の拡散", FS, GREEN)
    ctext(d, 495, 150, "(D)", FT, GREEN)
    for yy in [185, 225, 265]:
        arrow(d, 640, yy, fx + 20, yy, GREEN, 3, 12)
    ctext(d, 510, 300, "未燃側から供給", FT, GRAY)
    eqbox(d, 330, 355, "Le = alpha/D = lambda/(rho*Cp*D)   (Le=1 で熱と物質が同速)", 620, 46, BLACK, FILL2, FS)
    note(d, "Le != 1 で火炎の伸張・曲率による不安定化や局所消炎が起きる")
    save(im, "t1f17LewisNumber")


# ============================================================
# 17-10 t1f17LePrScRelation : Le = Sc/Pr(nu を介した関係)
# ============================================================
def le_pr_sc_relation():
    im, d = new(); title(d, "Le = Sc / Pr: 共通の nu を消去して導く関係")
    top = (330, 115); bl = (150, 300); br = (510, 300)
    d.line((top[0], top[1], bl[0], bl[1]), fill=BLACK, width=3)
    d.line((top[0], top[1], br[0], br[1]), fill=BLACK, width=3)
    d.line((bl[0], bl[1], br[0], br[1]), fill=BLACK, width=3)
    for (p, lab, col) in [(top, "nu", BLACK), (bl, "alpha", RED), (br, "D", GREEN)]:
        pcircle(d, p[0], p[1], 30, FILL1, col, 3); ctext(d, p[0], p[1], lab, FS, col)
    ctext(d, top[0], top[1] - 45, "動粘性係数", FT, GRAY)
    ctext(d, bl[0] - 4, bl[1] + 38, "熱拡散率", FT, GRAY)
    ctext(d, br[0] + 4, br[1] + 38, "物質拡散係数", FT, GRAY)
    ctext(d, (top[0] + bl[0]) / 2 - 46, (top[1] + bl[1]) / 2, "Pr = nu/alpha", FT, BLACK)
    ctext(d, (top[0] + br[0]) / 2 + 48, (top[1] + br[1]) / 2, "Sc = nu/D", FT, BLACK)
    ctext(d, (bl[0] + br[0]) / 2, br[1] + 14, "Le = alpha/D", FS, BLUE)
    eqbox(d, 330, 365, "Le = (nu/D)/(nu/alpha) = Sc/Pr   (Le=Pr*Sc や Pr/Sc は誤り)", 620, 44, BLACK, FILL2, FS)
    note(d, "気体で Pr≈Sc≈0.7 なら Le≈1(気体燃焼で Le が1前後になる理由)")
    save(im, "t1f17LePrScRelation")


# ============================================================
# 17-11 t1f17FicksLaw : フィックの法則 j_k = -rho D grad(Y_k)
# ============================================================
def ficks_law():
    im, d = new(); title(d, "フィックの法則: 濃度勾配と逆向きに拡散流束")
    ox, oy, xl, yl = 90, 320, 470, 200
    axes(d, ox, oy, xl + 20, yl + 20, "位置 x", "質量分率 Y_k")
    # 濃度プロファイル(左で高く右で低い)
    pts = [(ox + i, oy - (yl * (1 - i / xl) ** 1.2 * 0.9 + 0.05 * yl)) for i in range(0, xl + 1, 6)]
    d.line(pts, fill=GREEN, width=3, joint="curve")
    ctext(d, ox + 70, oy - 0.85 * yl, "濃い(Y_k 大)", FT, GREEN)
    ctext(d, ox + xl - 70, oy - 0.20 * yl, "薄い(Y_k 小)", FT, GRAY)
    # 勾配 grad Y (負) を細矢印、流束 j は正方向(薄い側)へ
    dashed(d, ox + 240, oy - 130, ox + 240, oy, GRAY, 1, 6, 5)
    arrow(d, ox + 170, oy - 90, ox + 320, oy - 90, RED, 4, 14)
    ctext(d, ox + 245, oy - 112, "拡散流束 j_k", FT, RED)
    ctext(d, ox + 245, oy - 68, "(濃い->薄い)", FT, GRAY)
    eqbox(d, 330, 375, "j_k = - rho * D * grad(Y_k)   (勾配と逆向き)", 600, 44, BLACK, FILL2, FS)
    note(d, "係数 D=物質拡散係数. 化学種保存式の拡散項として入る")
    save(im, "t1f17FicksLaw")


# ============================================================
# 17-12 t1f17SoretEffect : ソレー効果(温度勾配 -> 物質拡散)
# ============================================================
def soret_effect():
    im, d = new(); title(d, "ソレー効果(熱拡散): 温度勾配が成分の拡散を駆動")
    # 上段: ソレー(温度->物質)
    box(d, 40, 75, 620, 215, (250, 250, 250))
    ctext(d, 130, 100, "ソレー効果", FS, RED)
    d.rectangle((70, 130, 300, 185), outline=BLACK, width=2)
    ctext(d, 100, 157, "高温", FT, RED); ctext(d, 270, 157, "低温", FT, BLUE)
    arrow(d, 92, 157, 285, 157, RED, 2, 11)
    ctext(d, 185, 200, "温度勾配(原因)", FT, GRAY)
    arrow(d, 330, 150, 415, 150, BLACK, 3, 12)
    ctext(d, 520, 137, "軽い成分が偏る", FT, BLACK)
    ctext(d, 520, 167, "物質拡散(結果)", FT, GRAY)
    # 下段: デュフォー(逆現象・混同注意)
    box(d, 40, 235, 620, 375, (250, 250, 250))
    ctext(d, 130, 260, "デュフォー効果", FS, BLUE)
    d.rectangle((70, 290, 300, 345), outline=BLACK, width=2)
    ctext(d, 100, 317, "高濃度", FT, BLUE); ctext(d, 270, 317, "低濃度", FT, GRAY)
    arrow(d, 97, 317, 285, 317, BLUE, 2, 11)
    ctext(d, 185, 360, "濃度勾配(原因)", FT, GRAY)
    arrow(d, 330, 310, 415, 310, BLACK, 3, 12)
    ctext(d, 520, 297, "熱が移動", FT, BLACK)
    ctext(d, 520, 327, "熱流束(結果)", FT, GRAY)
    note(d, "ソレー=温度勾配->物質拡散. 逆(濃度->熱)がデュフォー効果")
    save(im, "t1f17SoretEffect")


# ============================================================
# 17-13 t1f17GoverningEquationCount : 支配方程式の本数 N+4
# ============================================================
def governing_equation_count():
    im, d = new(); title(d, "3次元 N 化学種 燃焼流の支配方程式は N+4 本")
    rows = [("質量保存(連続の式)", "1 本", BLACK),
            ("運動量保存(x, y, z の3方向)", "3 本", BLUE),
            ("エネルギー保存", "1 本", RED),
            ("化学種保存(独立なのは N-1 本)", "N - 1 本", GREEN)]
    x0, w = 60, 400
    y0, hh = 90, 50
    for i, (name, cnt, col) in enumerate(rows):
        cy = y0 + i * (hh + 7)
        box(d, x0, cy, x0 + w, cy + hh, (245, 245, 245))
        ctext(d, x0 + 14, cy + hh / 2, name, FT, BLACK, "lm")
        ctext(d, x0 + w + 65, cy + hh / 2, cnt, FS, col)
    ytot = y0 + 4 * (hh + 7) + 4
    box(d, x0, ytot, x0 + w + 130, ytot + 44, FILL2)
    ctext(d, x0 + (w + 130) / 2, ytot + 22, "合計 = N + 4 本", FL, BLACK)
    ctext(d, 330, ytot + 66, "全化学種の和は質量保存に一致 -> 独立は N-1 本", FT, GRAY)
    note(d, "状態方程式は補助式として別途必要(N+4 には数えない)")
    save(im, "t1f17GoverningEquationCount")


# ============================================================
# 17-14 t1f17ContinuityEquation : 連続の式(圧縮性・密度を発散に含む)
# ============================================================
def continuity_equation():
    im, d = new(); title(d, "連続の式(質量保存): 密度を発散の中に残す")
    ox, oy, w, h = 250, 165, 150, 150
    dx, dy = 55, 35
    d.polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)], outline=BLACK, width=3, fill=(248, 248, 248))
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + w + dx, oy - dy), (ox + w, oy)], outline=BLACK, width=3, fill=(240, 240, 240))
    d.polygon([(ox + w, oy), (ox + w + dx, oy - dy), (ox + w + dx, oy + h - dy), (ox + w, oy + h)], outline=BLACK, width=3, fill=(232, 232, 232))
    ctext(d, ox + w / 2, oy + h / 2 - 12, "密度の時間変化", FT, RED)
    ctext(d, ox + w / 2, oy + h / 2 + 14, "d(rho)/dt", FS, RED)
    arrow(d, ox - 90, oy + h / 2, ox - 6, oy + h / 2, BLUE, 4, 14)
    ctext(d, ox - 90, oy + h / 2 - 20, "流入 rho u", FT, BLUE, "lm")
    arrow(d, ox + w + dx + 6, oy + h / 2 - dy / 2, ox + w + dx + 90, oy + h / 2 - dy / 2, GREEN, 4, 14)
    ctext(d, ox + w + dx + 16, oy + h / 2 - dy / 2 - 20, "流出 rho u", FT, GREEN, "lm")
    eqbox(d, 330, 360, "d(rho)/dt + div(rho*u) = 0   (非圧縮 div u=0 は不可)", 620, 44, BLACK, FILL2, FS)
    note(d, "燃焼は温度で密度が大きく変わる. rho を発散内に残す形が必須")
    save(im, "t1f17ContinuityEquation")


# ============================================================
# 17-15 t1f17SpeciesTransport : 化学種の保存式(対流・拡散・反応)
# ============================================================
def species_transport():
    im, d = new(); title(d, "化学種 k の保存式: 対流 + 拡散 + 反応")
    terms = [("時間変化", "d(rho Y_k)/dt", "蓄積", BLACK),
             ("対流項", "div(rho u Y_k)", "流れが運ぶ", BLUE),
             ("拡散項", "div(rho D grad Y_k)", "フィックの法則", GREEN),
             ("反応項", "omega_k(dot)", "生成・消滅", RED)]
    x0, w = 45, 570
    y0, hh = 95, 60
    for i, (name, expr, role, col) in enumerate(terms):
        cy = y0 + i * (hh + 6)
        box(d, x0, cy, x0 + w, cy + hh, (245, 245, 245))
        ctext(d, x0 + 16, cy + 21, name, FT, col, "lm")
        ctext(d, x0 + 16, cy + 43, role, FT, GRAY, "lm")
        ctext(d, x0 + 210, cy + hh / 2, expr, FS, BLACK, "lm")
    eqbox(d, 330, 355, "d(rho Y_k)/dt + div(rho u Y_k) = div(rho D grad Y_k) + omega_k", 630, 44, BLACK, FILL2, FT)
    note(d, "全化学種で和をとると拡散・反応が消え連続の式へ -> 独立は N-1 本")
    save(im, "t1f17SpeciesTransport")


# ============================================================
# 17-16 t1f17ProgressVariable : 反応進行変数 c(未燃0->既燃1)
# ============================================================
def progress_variable():
    im, d = new(); title(d, "反応進行変数 c: 未燃 c=0 -> 既燃 c=1 で正規化")
    ox, oy, xl, yl = 110, 330, 430, 220
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "位置", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T", FS, BLACK, "rm")
    pts = []
    for i in range(0, xl + 1):
        t = i / xl
        v = 0.10 + 0.80 * (0.5 * (1 + math.tanh((t - 0.5) * 7)))
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    dashed(d, ox, oy - 0.10 * yl, ox + xl, oy - 0.10 * yl, GRAY, 1, 6, 5)
    dashed(d, ox, oy - 0.90 * yl, ox + xl, oy - 0.90 * yl, GRAY, 1, 6, 5)
    ctext(d, ox - 8, oy - 0.10 * yl, "Tu", FT, BLUE, "rm")
    ctext(d, ox - 8, oy - 0.90 * yl, "Tb", FT, RED, "rm")
    ctext(d, ox + xl * 0.15, oy - 0.04 * yl, "未燃(c=0)", FT, BLUE)
    ctext(d, ox + xl * 0.82, oy - 0.97 * yl, "既燃(c=1)", FT, RED)
    eqbox(d, 400, 375, "c = (T - Tu)/(Tb - Tu) = (Y - Yu)/(Yb - Yu)", 500, 44, BLACK, FILL2, FS)
    note(d, "温度でも生成物質量分率でも定義できる. 火炎位置・厚みの議論に使う")
    save(im, "t1f17ProgressVariable")


# ============================================================
# 17-17 t1f17ReynoldsAverage : レイノルズ平均 f = f_bar + f'
# ============================================================
def reynolds_average():
    im, d = new(); title(d, "レイノルズ平均: 平均 f_bar と変動 f' に分ける")
    ox, oy, xl, yl = 90, 240, 480, 150
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "時間 t", FT, BLACK, "lm")
    arrow(d, ox, oy + 60, ox, oy - yl, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl, "f", FS, BLACK, "rm")
    # 平均線
    ybar = oy - 80
    dashed(d, ox, ybar, ox + xl, ybar, BLUE, 2, 9, 6)
    ctext(d, ox + xl + 8, ybar, "f_bar", FT, BLUE, "lm")
    # 揺らぐ信号(平均まわりに変動)
    pts = []
    for i in range(0, xl + 1, 4):
        t = i / xl
        val = 55 * (math.sin(t * 20) * 0.5 + math.sin(t * 33 + 1) * 0.3 + math.sin(t * 9) * 0.4)
        pts.append((ox + i, ybar - val))
    d.line(pts, fill=RED, width=2, joint="curve")
    ctext(d, ox + xl * 0.55, oy - yl + 6, "瞬時値 f = f_bar + f'", FT, RED)
    # f' の指示
    d.line((ox + 200, ybar, ox + 200, ybar - 55), fill=GRAY, width=1)
    ctext(d, ox + 210, ybar - 30, "f'(変動)", FT, GRAY, "lm")
    eqbox(d, 330, 340, "f = f_bar + f'   ,   f' のバー = 0", 500, 44, BLACK, FILL2, FS)
    note(d, "変動の単純平均はゼロ. ただし f'^2 のバー(乱れの強さ)は非ゼロ")
    save(im, "t1f17ReynoldsAverage")


# ============================================================
# 17-18 t1f17FavreAverage : ファーブル平均(密度加重)
# ============================================================
def favre_average():
    im, d = new(); title(d, "ファーブル平均(密度加重): f_tilde = (rho f のバー)/rho_bar")
    box(d, 40, 80, 620, 200, (235, 245, 235))
    ctext(d, 150, 105, "密度で重み付けした平均", FS, GREEN)
    ctext(d, 150, 150, "f = f_tilde + f''", F, BLACK)
    ctext(d, 150, 182, "f_tilde = rho 加重平均", FT, GRAY)
    box(d, 380, 118, 605, 185, (250, 250, 250))
    ctext(d, 492, 142, "加重平均で消える変動", FT, BLACK)
    ctext(d, 492, 168, "( f'' のチルダ = 0 )", FS, GREEN)
    # 対比: レイノルズとの違い
    box(d, 40, 220, 620, 340, (250, 250, 250))
    ctext(d, 330, 245, "普通の平均(レイノルズ)との違い", FS, BLUE)
    ctext(d, 330, 285, "rho * f_bar = rho_bar * f_tilde で橋渡し", FT, BLACK)
    ctext(d, 330, 315, "密度一定なら f_tilde は f_bar に一致", FT, GRAY)
    eqbox(d, 330, 372, "f_tilde = (rho f のバー) / rho_bar", 500, 44, BLACK, FILL2, FS)
    note(d, "密度変動との相関項を減らせる. 可圧縮乱流・乱流燃焼の基本")
    save(im, "t1f17FavreAverage")


# ============================================================
# 17-19 t1f17FavreScalarTransport : ファーブル平均スカラー輸送の4項
# ============================================================
def favre_scalar_transport():
    im, d = new(); title(d, "ファーブル平均スカラー phi の輸送方程式(右辺4項)")
    ctext(d, 330, 78, "d(rho_bar phi_tilde)/dt  =  (1)+(2)+(3)+(4)", FS, BLACK)
    terms = [("(1) 対流項", "- div(rho_bar phi_tilde u_tilde)", "平均流で運ぶ", BLACK, False),
             ("(2) 分子拡散項", "div(rho a_phi grad phi のバー)", "分子拡散", BLUE, False),
             ("(3) 乱流拡散項", "div(- rho_bar (phi'' u'') のチルダ)", "変動の相関 -> 未閉じ", RED, True),
             ("(4) 反応項", "omega_phi のバー", "平均反応速度", GREEN, False)]
    x0, w = 40, 580
    y0, hh = 105, 60
    for i, (name, expr, role, col, hl) in enumerate(terms):
        cy = y0 + i * (hh + 6)
        fillc = (250, 230, 230) if hl else (245, 245, 245)
        box(d, x0, cy, x0 + w, cy + hh, fillc, 4 if hl else 2)
        ctext(d, x0 + 14, cy + 21, name, FT, col, "lm")
        ctext(d, x0 + 14, cy + 43, role, FT, GRAY, "lm")
        ctext(d, x0 + 195, cy + hh / 2, expr, FT, BLACK, "lm")
    note(d, "第3項(乱流拡散)は未知の相関を含み乱流モデルで閉じる最重要項")
    save(im, "t1f17FavreScalarTransport")


# ============================================================
# 17-20 t1f17MulticomponentEOS : 多成分系の状態方程式
# ============================================================
def multicomponent_eos():
    im, d = new(); title(d, "多成分理想気体の状態方程式(導出の流れ)")
    box(d, 40, 95, 235, 300, (250, 250, 250))
    ctext(d, 137, 116, "混合気体", FT, GRAY)
    specs = [(85, 160, RED, "O2"), (150, 155, BLUE, "N2"), (195, 185, GREEN, "CO2"),
             (90, 225, ORANGE, "H2O"), (155, 230, RED, "O2"), (190, 260, BLUE, "N2")]
    for (px, py, col, lab) in specs:
        pcircle(d, px, py, 17, FILL1, col, 2); ctext(d, px, py, lab, FT, col)
    ctext(d, 137, 288, "化学種 i が混在", FT, GRAY)
    arrow(d, 240, 195, 300, 195, BLACK, 3, 12)
    box(d, 305, 135, 490, 255, (235, 242, 250))
    ctext(d, 397, 160, "各種のモル濃度", FT, BLUE)
    ctext(d, 397, 192, "c_i = rho Y_i / W_i", FS, BLACK)
    ctext(d, 397, 225, "総和 c = sum(c_i)", FT, GRAY)
    arrow(d, 495, 195, 555, 195, BLACK, 3, 12)
    box(d, 560, 145, 645, 245, FILL2)
    ctext(d, 602, 180, "p = c R0 T", FT, RED)
    ctext(d, 602, 215, "へ代入", FT, GRAY)
    eqbox(d, 330, 350, "p = rho R0 T sum(Y_i / W_i) = rho R0 T / W_bar", 620, 46, BLACK, FILL2, FS)
    note(d, "R0=一般気体定数. sum(Y_i/W_i)=1/W_bar. 組成で密度が変わる")
    save(im, "t1f17MulticomponentEOS")


# ============================================================
# 17-21 t1f17LowMachApprox : 低マッハ数近似(圧力は分離・密度は大変化)
# ============================================================
def low_mach_approx():
    im, d = new(); title(d, "低マッハ数近似: 圧力は分離, 密度は大きく変化")
    cards = [
        (40, 80, "流速 << 音速", "マッハ数が小さい", BLUE, "flow"),
        (340, 80, "圧力の空間変動は微小", "熱力学圧力は一定とみなす", GREEN, "flat"),
        (40, 240, "温度は大きく上昇", "燃焼で数倍に", RED, "up"),
        (340, 240, "密度は大きく低下", "圧力一定でも温度で", RED, "down"),
    ]
    for (x, y, head, sub, col, kind) in cards:
        box(d, x, y, x + 280, y + 145, (250, 250, 250))
        ctext(d, x + 140, y + 26, head, FS, col)
        ctext(d, x + 140, y + 122, sub, FT, GRAY)
        gx, gy, gw = x + 55, y + 88, 170
        if kind == "flow":
            arrow(d, gx, gy, gx + 60, gy, BLUE, 3, 11)
            ctext(d, gx + 100, gy, "<< 音速", FT, GRAY, "lm")
        elif kind == "flat":
            d.line((gx, gy, gx + gw, gy), fill=GREEN, width=3)
        elif kind == "up":
            d.line((gx, gy + 15, gx + 60, gy + 12, gx + 110, gy - 25, gx + gw, gy - 30), fill=RED, width=3, joint="curve")
        elif kind == "down":
            d.line((gx, gy - 28, gx + 60, gy - 24, gx + 110, gy + 10, gx + gw, gy + 14), fill=RED, width=3, joint="curve")
    note(d, "圧力変化が小=密度変化も小 ではない. 温度上昇で密度は大変化する")
    save(im, "t1f17LowMachApprox")


# ============================================================
if __name__ == "__main__":
    air_fuel_ratio()            # 17-1
    stoichiometric_af()         # 17-2
    equivalence_ratio()         # 17-3
    excess_air_ratio()          # 17-4
    mole_mass_fraction()        # 17-5
    transport_coefficients()    # 17-6
    prandtl_number()            # 17-7
    schmidt_number()            # 17-8
    lewis_number()              # 17-9
    le_pr_sc_relation()         # 17-10
    ficks_law()                 # 17-11
    soret_effect()              # 17-12
    governing_equation_count()  # 17-13
    continuity_equation()       # 17-14
    species_transport()         # 17-15
    progress_variable()         # 17-16
    reynolds_average()          # 17-17
    favre_average()             # 17-18
    favre_scalar_transport()    # 17-19
    multicomponent_eos()        # 17-20
    low_mach_approx()           # 17-21
    print("done t1f ch17")
