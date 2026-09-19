# -*- coding: utf-8 -*-
"""熱流体力学1級 第17章「燃焼の基礎1」の問題図(t1e17*・15枚)を描画。
白地660x420・黒線画・機構のみ・装飾禁止。
豆腐回避のためギリシャ文字/添字/特殊記号はプレーン表記へ置換
(phi, alpha, nu, rho, Cp, lambda, W, D, CH4, O2, N2, CO2, H2O, R0, ^, <<, -> 等)。
required図(回答前)には答え・正解値・結論を描かない。helpful図(回答後)は補足説明。"""
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


# ============================================================
# 17-1 t1e17AirFuelRatio : 理論空燃比の構図(required・数値なし)
# ============================================================
def air_fuel_ratio():
    im, d = new(); title(d, "空気で完全燃焼: 空気全体(O2+N2)を質量に含める")
    # 左: 燃料 CH4
    box(d, 40, 150, 170, 260, (235, 242, 250))
    ctext(d, 105, 185, "燃料", FT, GRAY)
    ctext(d, 105, 220, "CH4", FL, BLUE)
    ctext(d, 105, 285, "(燃料の質量)", FT, GRAY)
    # 中央: 空気枠 O2:N2 = 1:4
    box(d, 230, 110, 470, 300, (250, 250, 250))
    ctext(d, 350, 128, "空気", FT, GRAY)
    # O2 を1個、N2 を4個(体積比 1:4)
    pcircle(d, 285, 175, 18, (250, 235, 235), RED, 3); ctext(d, 285, 175, "O2", FT, RED)
    for (px, py) in [(345, 165), (405, 165), (345, 225), (405, 225)]:
        pcircle(d, px, py, 18, (235, 242, 250), BLUE, 2); ctext(d, px, py, "N2", FT, BLUE)
    ctext(d, 350, 270, "O2 : N2 = 1 : 4", FT, BLACK)
    ctext(d, 350, 315, "(N2 は反応しないが空気の一部)", FT, GRAY)
    # 右: 生成物
    box(d, 520, 150, 640, 260, (235, 245, 235))
    ctext(d, 580, 178, "生成物", FT, GRAY)
    ctext(d, 580, 208, "CO2", FS, GREEN)
    ctext(d, 580, 236, "+ 2 H2O", FS, GREEN)
    # 矢印
    arrow(d, 172, 205, 228, 205, BLACK, 3, 12)
    arrow(d, 472, 205, 518, 205, BLACK, 3, 12)
    # 空燃比の考え方(質量の内訳を語で)
    ctext(d, 350, 355, "空燃比 = 空気の質量 / 燃料の質量", FT, BLACK)
    note(d, "N2 も空気の質量に必ず加える(数値は各自)")
    save(im, "t1e17AirFuelRatio")


# ============================================================
# 17-2 t1e17EquivalenceRatio : 当量比の数直線(required・数値解なし)
# ============================================================
def equivalence_ratio():
    im, d = new(); title(d, "当量比 phi の意味: 化学量論を1とした燃料の過不足")
    ox, oy, xl = 90, 240, 480
    # 数直線
    arrow(d, ox - 10, oy, ox + xl + 20, oy, BLACK, 3, 12)
    ctext(d, ox + xl + 26, oy, "phi", FS, BLACK, "lm")
    # 帯: リーン(左) / 量論(中) / リッチ(右)
    xm = ox + xl * 0.5
    d.rectangle((ox, oy - 26, xm, oy - 6), outline=BLUE, width=2, fill=(225, 235, 250))
    d.rectangle((xm, oy - 26, ox + xl, oy - 6), outline=RED, width=2, fill=(250, 230, 230))
    # 目盛り phi=1
    d.line((xm, oy - 34, xm, oy + 12), fill=BLACK, width=3)
    ctext(d, xm, oy + 30, "phi = 1", FS, BLACK)
    ctext(d, xm, oy + 55, "化学量論(過不足なし)", FT, GRAY)
    # 左: リーン
    ctext(d, ox + xl * 0.25, oy - 55, "リーン(希薄)", FS, BLUE)
    ctext(d, ox + xl * 0.25, oy - 16, "空気過剰 / 燃料少", FT, BLUE)
    ctext(d, ox + xl * 0.25, oy + 30, "phi < 1", FT, BLUE)
    # 右: リッチ
    ctext(d, ox + xl * 0.75, oy - 55, "リッチ(過濃)", FS, RED)
    ctext(d, ox + xl * 0.75, oy - 16, "燃料過剰 / 酸素少", FT, RED)
    ctext(d, ox + xl * 0.75, oy + 30, "phi > 1", FT, RED)
    # 定義の言葉(数値は書かない)
    box(d, 90, 330, 570, 385, FILL2)
    ctext(d, 330, 358, "phi = (実際の燃料/酸素比) / (化学量論の燃料/酸素比)", FT, BLACK)
    note(d, "酸素が量論より少なければ phi>1(リッチ)側(具体値は各自)")
    save(im, "t1e17EquivalenceRatio")


# ============================================================
# 17-3 t1e17MoleMassFraction : モル分率->質量分率(required・数値なし)
# ============================================================
def mole_mass_fraction():
    im, d = new(); title(d, "モル分率(個数の割合) と 質量分率(質量の割合)")
    # 左: 個数で数える箱 = モル分率
    box(d, 40, 110, 290, 320, (250, 250, 250))
    ctext(d, 165, 130, "個数で数える = モル分率", FT, BLACK)
    # O2 と N2 を同数(各3個)
    o2 = [(90, 180), (165, 180), (240, 180)]
    n2 = [(90, 250), (165, 250), (240, 250)]
    for (px, py) in o2:
        pcircle(d, px, py, 20, (250, 235, 235), RED, 2); ctext(d, px, py, "O2", FT, RED)
    for (px, py) in n2:
        pcircle(d, px, py, 20, (235, 242, 250), BLUE, 2); ctext(d, px, py, "N2", FT, BLUE)
    ctext(d, 165, 300, "O2 と N2 が同数(モル分率が等しい)", FT, GRAY)
    # 変換矢印(平均分子量 W_bar を介する)
    arrow(d, 300, 215, 370, 215, BLACK, 3, 13)
    ctext(d, 335, 190, "平均分子量", FT, GRAY)
    ctext(d, 335, 240, "W_bar を介す", FT, GRAY)
    # 右: 天秤で質量を比較 = 質量分率
    box(d, 380, 110, 640, 320, (250, 250, 250))
    ctext(d, 510, 130, "質量で量る = 質量分率", FT, BLACK)
    # 天秤: 支点と傾いた梁(重いO2側が下がる)
    fx, fy = 510, 235
    d.polygon((fx, fy, fx - 14, fy + 34, fx + 14, fy + 34), outline=BLACK, width=2, fill=FILL2)
    d.line((fx, fy + 34, fx, fy + 50), fill=BLACK, width=2)
    # 傾いた梁(左=O2が重く下がる)
    lx, ly = fx - 80, fy - 8
    rx, ry = fx + 80, fy - 36
    d.line((lx, ly, rx, ry), fill=BLACK, width=3)
    d.line((fx, fy, (lx + rx) / 2, (ly + ry) / 2), fill=BLACK, width=2)
    # 皿
    pcircle(d, lx, ly + 22, 18, (250, 235, 235), RED, 2); ctext(d, lx, ly + 22, "O2", FT, RED)
    pcircle(d, rx, ry + 22, 18, (235, 242, 250), BLUE, 2); ctext(d, rx, ry + 22, "N2", FT, BLUE)
    d.line((lx, ly, lx, ly + 4), fill=BLACK, width=1)
    ctext(d, 510, 300, "重い分子ほど質量割合が大きい", FT, GRAY)
    note(d, "同じモル分率でも重い成分は質量分率が大きくなる(具体値は各自)")
    save(im, "t1e17MoleMassFraction")


# ============================================================
# 17-4 t1e17TransportUnits : 輸送物性係数の単位表(helpful)
# ============================================================
def transport_units():
    im, d = new(); title(d, "輸送物性係数の単位: 3つとも m^2/s で揃う")
    # 上段: 3列の表
    cols = [("熱拡散率 alpha", "lambda / (rho Cp)", "m^2/s"),
            ("物質拡散係数 D", "拡散方程式の係数", "m^2/s"),
            ("動粘性係数 nu", "mu / rho", "m^2/s")]
    x0, w = 40, 193
    y0, hh = 90, 150
    for i, (name, defn, unit) in enumerate(cols):
        cx = x0 + i * (w + 4)
        box(d, cx, y0, cx + w, y0 + hh, (235, 242, 250) if i != 1 else (235, 245, 235))
        ctext(d, cx + w / 2, y0 + 26, name, FT, BLACK)
        d.line((cx + 12, y0 + 48, cx + w - 12, y0 + 48), fill=LGRAY, width=1)
        ctext(d, cx + w / 2, y0 + 78, defn, FT, GRAY)
        ctext(d, cx + w / 2, y0 + 120, unit, FS, RED)
    ctext(d, 330, y0 + hh + 26, "いずれも「拡散が広がる面積/時間」-> 単位は m^2/s で共通", FT, BLACK)
    # 下段: 割る前の量(対比)
    box(d, 40, 300, 330, 380, (250, 250, 250))
    ctext(d, 185, 322, "熱伝導率 lambda", FT, BLACK)
    ctext(d, 185, 352, "単位 W/(m K)", FS, GRAY)
    box(d, 350, 300, 620, 380, (250, 250, 250))
    ctext(d, 485, 322, "粘性係数 mu", FT, BLACK)
    ctext(d, 485, 352, "単位 Pa s", FS, GRAY)
    note(d, "lambda・mu は密度・比熱で割る前の量(m^2/s ではない)")
    save(im, "t1e17TransportUnits")


# ============================================================
# 17-5 t1e17LewisNumber : ルイス数の概念(required・定義式なし)
# ============================================================
def lewis_number():
    im, d = new(); title(d, "ルイス数 Le: 熱の拡散 と 物質の拡散 の比")
    # 火炎面(中央の縦線)
    fx = 330
    for yy in range(110, 340, 16):
        d.line((fx, yy, fx, yy + 9), fill=ORANGE, width=4)
    ctext(d, fx, 95, "火炎面", FT, ORANGE)
    # 左: 熱の拡散(温度勾配)
    ctext(d, 165, 120, "熱の拡散", FS, RED)
    ctext(d, 165, 148, "(熱拡散率 alpha)", FT, RED)
    for i, yy in enumerate([190, 230, 270]):
        arrow(d, 120 - i * 0, yy, fx - 20, yy, RED, 3, 12)
    ctext(d, 150, 305, "温度勾配で熱が広がる", FT, GRAY)
    # 右: 物質の拡散(濃度勾配)
    ctext(d, 495, 120, "物質(反応物)の拡散", FS, BLUE)
    ctext(d, 495, 148, "(拡散係数 D)", FT, BLUE)
    for yy in [190, 230, 270]:
        arrow(d, 640, yy, fx + 20, yy, BLUE, 3, 12)
    ctext(d, 510, 305, "濃度勾配で反応物が広がる", FT, GRAY)
    # 比が Le
    box(d, 180, 350, 480, 395, FILL2)
    ctext(d, 330, 372, "Le = 熱の拡散のしやすさ / 物質の拡散のしやすさ", FT, BLACK)
    note(d, "両者の比が Le(定義式の形は各自)")
    save(im, "t1e17LewisNumber")


# ============================================================
# 17-6 t1e17DimensionlessNumbers : Pr/Sc/Le の三角関係(helpful)
# ============================================================
def dimensionless_numbers():
    im, d = new(); title(d, "Pr・Sc・Le は nu を介して結ばれる")
    # 三角形の頂点: nu(上)・alpha(左下)・D(右下)
    top = (330, 120)
    bl = (140, 320)
    br = (520, 320)
    d.line((top[0], top[1], bl[0], bl[1]), fill=BLACK, width=3)
    d.line((top[0], top[1], br[0], br[1]), fill=BLACK, width=3)
    d.line((bl[0], bl[1], br[0], br[1]), fill=BLACK, width=3)
    # 頂点ノード
    for (p, lab, col) in [(top, "nu", BLACK), (bl, "alpha", RED), (br, "D", BLUE)]:
        pcircle(d, p[0], p[1], 30, FILL1, col, 3); ctext(d, p[0], p[1], lab, FS, col)
    ctext(d, top[0], top[1] - 45, "動粘性係数", FT, GRAY)
    ctext(d, bl[0] - 4, bl[1] + 40, "熱拡散率", FT, GRAY)
    ctext(d, br[0] + 4, br[1] + 40, "物質拡散係数", FT, GRAY)
    # 辺のラベル(比)
    ctext(d, (top[0] + bl[0]) / 2 - 40, (top[1] + bl[1]) / 2, "Pr = nu/alpha", FT, BLACK)
    ctext(d, (top[0] + br[0]) / 2 + 42, (top[1] + br[1]) / 2, "Sc = nu/D", FT, BLACK)
    ctext(d, (bl[0] + br[0]) / 2, br[1] + 16, "Le = alpha/D", FS, GREEN)
    note(d, "共通の nu を消去すると Le = Sc/Pr の関係が導ける")
    save(im, "t1e17DimensionlessNumbers")


# ============================================================
# 17-7 t1e17SoretEffect : ソレ効果とデュフォ効果の対比(helpful)
# ============================================================
def soret_effect():
    im, d = new(); title(d, "ソレ効果 と デュフォ効果(互いに逆の相反現象)")
    # 上段: ソレ効果(温度勾配 -> 物質流束)
    box(d, 40, 80, 620, 220, (250, 250, 250))
    ctext(d, 120, 105, "ソレ効果(熱拡散)", FS, RED)
    # 温度勾配(高温->低温)
    d.rectangle((70, 135, 300, 185), outline=BLACK, width=2)
    ctext(d, 100, 160, "高温", FT, RED); ctext(d, 270, 160, "低温", FT, BLUE)
    arrow(d, 90, 160, 285, 160, RED, 2, 11)
    ctext(d, 185, 205, "温度勾配(原因)", FT, GRAY)
    arrow(d, 330, 150, 420, 150, BLACK, 3, 12)
    ctext(d, 500, 138, "-> 気体成分が移動", FT, BLACK)
    ctext(d, 500, 168, "(物質流束が結果)", FT, GRAY)
    # 下段: デュフォ効果(濃度勾配 -> 熱流束)
    box(d, 40, 240, 620, 380, (250, 250, 250))
    ctext(d, 120, 265, "デュフォ効果", FS, BLUE)
    d.rectangle((70, 295, 300, 345), outline=BLACK, width=2)
    ctext(d, 100, 320, "高濃度", FT, BLUE); ctext(d, 270, 320, "低濃度", FT, GRAY)
    arrow(d, 95, 320, 285, 320, BLUE, 2, 11)
    ctext(d, 185, 365, "濃度勾配(原因)", FT, GRAY)
    arrow(d, 330, 310, 420, 310, BLACK, 3, 12)
    ctext(d, 500, 298, "-> 熱が移動", FT, BLACK)
    ctext(d, 500, 328, "(熱流束が結果)", FT, GRAY)
    note(d, "原因と結果が逆: ソレ=温度->物質, デュフォ=濃度->熱")
    save(im, "t1e17SoretEffect")


# ============================================================
# 17-8 t1e17ConservationEqs : 保存式の本数の積み上げ(helpful)
# ============================================================
def conservation_eqs():
    im, d = new(); title(d, "3次元 N 化学種 燃焼流の保存式の本数")
    rows = [("質量保存(連続の式)", "1 本", BLACK),
            ("運動量保存(x,y,z の3方向)", "3 本", BLUE),
            ("エネルギー保存", "1 本", RED),
            ("化学種保存(N 種のうち独立)", "N - 1 本", GREEN)]
    x0, w = 70, 400
    y0, hh = 95, 52
    for i, (name, cnt, col) in enumerate(rows):
        cy = y0 + i * (hh + 8)
        box(d, x0, cy, x0 + w, cy + hh, (245, 245, 245))
        ctext(d, x0 + 16, cy + hh / 2, name, FT, BLACK, "lm")
        ctext(d, x0 + w + 60, cy + hh / 2, cnt, FS, col)
    # 合計
    ytot = y0 + 4 * (hh + 8) + 6
    box(d, x0, ytot, x0 + w + 120, ytot + 46, FILL2)
    ctext(d, x0 + (w + 120) / 2, ytot + 23, "合計 = N + 4 本", FL, BLACK)
    ctext(d, 330, ytot + 70, "化学種は N 本でなく N-1 本(全化学種の和 = 質量保存に一致)", FT, GRAY)
    note(d, "状態方程式は補助式として別途必要(保存式には数えない)")
    save(im, "t1e17ConservationEqs")


# ============================================================
# 17-9 t1e17ProgressVariable : 反応進行変数(required・数値解なし)
# ============================================================
def progress_variable():
    im, d = new(); title(d, "反応進行変数 c: 未燃 c=0 -> 既燃 c=1")
    ox, oy, xl, yl = 110, 340, 440, 240
    # 軸
    arrow(d, ox, oy, ox + xl + 20, oy, BLACK, 2, 11)
    ctext(d, ox + xl + 26, oy, "火炎を横切る位置", FT, BLACK, "lm")
    arrow(d, ox, oy, ox, oy - yl - 10, BLACK, 2, 11)
    ctext(d, ox - 12, oy - yl - 12, "温度 T", FS, BLACK, "rm")
    # 温度プロファイル(左=未燃で低温 Tu, 右=既燃で高温 Tb)
    pts = []
    for i in range(0, 441):
        t = i / 440
        # なめらかなS字(tanh風)
        v = 0.10 + 0.80 * (0.5 * (1 + math.tanh((t - 0.5) * 7)))
        pts.append((ox + t * xl, oy - v * yl))
    d.line(pts, fill=RED, width=3, joint="curve")
    # Tu, Tb の水準線
    dashed(d, ox, oy - 0.10 * yl, ox + xl, oy - 0.10 * yl, GRAY, 1, 6, 5)
    dashed(d, ox, oy - 0.90 * yl, ox + xl, oy - 0.90 * yl, GRAY, 1, 6, 5)
    ctext(d, ox - 8, oy - 0.10 * yl, "Tu", FT, BLUE, "rm")
    ctext(d, ox - 8, oy - 0.90 * yl, "Tb", FT, RED, "rm")
    ctext(d, ox + xl * 0.15, oy - 0.05 * yl, "未燃気体", FT, BLUE)
    ctext(d, ox + xl * 0.82, oy - 0.96 * yl, "既燃気体", FT, RED)
    # 右軸: 反応進行変数 c(0->1)
    axx = ox + xl + 40
    arrow(d, axx, oy, axx, oy - yl - 10, GREEN, 2, 11)
    ctext(d, axx + 12, oy - yl - 12, "c", FS, GREEN, "lm")
    ctext(d, axx + 12, oy, "c=0", FT, GREEN, "lm")
    ctext(d, axx + 12, oy - yl, "c=1", FT, GREEN, "lm")
    note(d, "c は温度で正規化(未燃=0・既燃=1). 局所温度に対応する c の値を問う")
    save(im, "t1e17ProgressVariable")


# ============================================================
# 17-10 t1e17FavreAveraging : レイノルズ分解とファーブル分解(required)
# ============================================================
def favre_averaging():
    im, d = new(); title(d, "レイノルズ分解 と ファーブル(密度加重)分解")
    # 上段: レイノルズ分解
    box(d, 40, 80, 620, 220, (235, 242, 250))
    ctext(d, 150, 105, "レイノルズ分解(単純平均)", FS, BLUE)
    ctext(d, 150, 145, "f = f_bar + f'", F, BLACK)
    ctext(d, 150, 185, "f_bar = 単純平均, f' = 変動", FT, GRAY)
    box(d, 380, 120, 610, 190, (250, 250, 250))
    ctext(d, 495, 145, "変動の単純平均はゼロ", FT, BLACK)
    ctext(d, 495, 172, "( f' のバー = 0 )", FS, BLUE)
    # 下段: ファーブル分解
    box(d, 40, 240, 620, 380, (235, 245, 235))
    ctext(d, 150, 265, "ファーブル分解(密度加重平均)", FS, GREEN)
    ctext(d, 150, 305, "f = f_tilde + f''", F, BLACK)
    ctext(d, 150, 345, "f_tilde = rho 加重平均", FT, GRAY)
    box(d, 380, 280, 610, 350, (250, 250, 250))
    ctext(d, 495, 305, "変動の密度加重平均はゼロ", FT, BLACK)
    ctext(d, 495, 332, "( f'' のチルダ = 0 )", FS, GREEN)
    note(d, "消える対: レイノルズ変動<->単純平均, ファーブル変動<->密度加重平均")
    save(im, "t1e17FavreAveraging")


# ============================================================
# 17-11 t1e17FavreRelations : ファーブル関係式の正誤表(helpful)
# ============================================================
def favre_relations():
    im, d = new(); title(d, "ファーブル平均の関係式: 成り立つ / 成り立たない")
    rows = [("rho f のバー = rho_bar * f_tilde", "OK", "定義の言い換え", GREEN),
            ("f_tilde = (rho f のバー) / rho_bar", "OK", "定義そのもの", GREEN),
            ("f'' のチルダ = 0", "OK", "密度加重平均で消える", GREEN),
            ("f'' のバー = 0", "NG", "密度相関で残る(一般に非ゼロ)", RED)]
    x0 = 40
    y0, hh = 95, 62
    for i, (expr, mark, reason, col) in enumerate(rows):
        cy = y0 + i * (hh + 6)
        box(d, x0, cy, x0 + 300, cy + hh, (245, 245, 245))
        ctext(d, x0 + 150, cy + hh / 2, expr, FT, BLACK)
        # 判定
        d.rectangle((x0 + 312, cy, x0 + 372, cy + hh),
                    outline=col, width=3, fill=(235, 245, 235) if mark == "OK" else (250, 230, 230))
        ctext(d, x0 + 342, cy + hh / 2, mark, FS, col)
        ctext(d, x0 + 388, cy + hh / 2, reason, FT, GRAY, "lm")
    note(d, "誤りは f'' のバー=0. 加重平均で消えるのは rho f'' のバーのほう")
    save(im, "t1e17FavreRelations")


# ============================================================
# 17-12 t1e17ScalarTransport : スカラー輸送方程式の4項(helpful)
# ============================================================
def scalar_transport():
    im, d = new(); title(d, "ファーブル平均スカラー phi の輸送方程式(右辺4項)")
    # 左辺
    ctext(d, 120, 115, "d(rho_bar phi_tilde)/dt  =", FS, BLACK)
    # 4項を段組み(上段=式, 下段=役割)
    terms = [("(1) 対流項", "- div( rho_bar phi_tilde u_tilde )", "平均量のみ", BLACK, False),
             ("(2) 分子拡散項", "div( rho a_phi grad(phi) のバー )", "分子レベルの拡散", BLUE, False),
             ("(3) 乱流拡散項", "div( - rho_bar (phi'' u'') のチルダ )", "変動の相関 -> 未閉じ", RED, True),
             ("(4) 反応項", "( omega_phi のバー )", "生成・消滅", GREEN, False)]
    x0, w = 40, 580
    y0, hh = 150, 58
    for i, (name, expr, note_s, col, hl) in enumerate(terms):
        cy = y0 + i * (hh + 5)
        fillc = (250, 230, 230) if hl else (245, 245, 245)
        box(d, x0, cy, x0 + w, cy + hh, fillc, 4 if hl else 2)
        ctext(d, x0 + 14, cy + 20, name, FT, col, "lm")
        ctext(d, x0 + 14, cy + 42, note_s, FT, GRAY, "lm")
        ctext(d, x0 + 175, cy + hh / 2, expr, FT, BLACK, "lm")
    note(d, "乱流拡散は変動どうしの相関 phi'' u'' を含む項(枠内)")
    save(im, "t1e17ScalarTransport")


# ============================================================
# 17-13 t1e17Continuity : 連続の式の質量収支(required・式なし)
# ============================================================
def continuity():
    im, d = new(); title(d, "微小検査体積の質量収支(連続の式)")
    # 立方体(アイソメ)
    ox, oy, w, h = 250, 175, 150, 150
    dx, dy = 55, 35
    d.polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)], outline=BLACK, width=3, fill=(248, 248, 248))
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + w + dx, oy - dy), (ox + w, oy)], outline=BLACK, width=3, fill=(240, 240, 240))
    d.polygon([(ox + w, oy), (ox + w + dx, oy - dy), (ox + w + dx, oy + h - dy), (ox + w, oy + h)], outline=BLACK, width=3, fill=(232, 232, 232))
    # 内部: 密度変化
    ctext(d, ox + w / 2, oy + h / 2 - 12, "内部の密度変化", FT, RED)
    ctext(d, ox + w / 2, oy + h / 2 + 14, "d(rho)/dt", FS, RED)
    # 流入(左面)
    arrow(d, ox - 90, oy + h / 2, ox - 6, oy + h / 2, BLUE, 4, 14)
    ctext(d, ox - 90, oy + h / 2 - 20, "質量流入", FT, BLUE, "lm")
    ctext(d, ox - 90, oy + h / 2 + 22, "rho u", FT, BLUE, "lm")
    # 流出(右面)
    arrow(d, ox + w + dx + 6, oy + h / 2 - dy / 2, ox + w + dx + 90, oy + h / 2 - dy / 2, GREEN, 4, 14)
    ctext(d, ox + w + dx + 20, oy + h / 2 - dy / 2 - 22, "質量流出", FT, GREEN, "lm")
    ctext(d, ox + w + dx + 20, oy + h / 2 - dy / 2 + 22, "rho u", FT, GREEN, "lm")
    # 縦方向の流入出も1組
    arrow(d, ox + w / 2, oy + h + 70, ox + w / 2, oy + h + 6, BLUE, 3, 12)
    ctext(d, ox + w / 2, oy + h + 88, "rho u", FT, BLUE)
    note(d, "密度の時間変化 と 質量フラックス rho u の正味流出 がつり合う(式は各自)")
    save(im, "t1e17Continuity")


# ============================================================
# 17-14 t1e17StateEquation : 多成分状態方程式の導出フロー(required・式なし)
# ============================================================
def state_equation():
    im, d = new(); title(d, "多成分理想気体の状態方程式(導出の流れ)")
    # 左: 複数化学種が混在する箱
    box(d, 40, 100, 250, 320, (250, 250, 250))
    ctext(d, 145, 122, "混合気体", FT, GRAY)
    specs = [(90, 165, RED, "O2"), (150, 160, BLUE, "N2"), (205, 190, GREEN, "CO2"),
             (95, 230, ORANGE, "H2O"), (160, 235, RED, "O2"), (200, 265, BLUE, "N2"),
             (110, 285, GREEN, "CO2")]
    for (px, py, col, lab) in specs:
        pcircle(d, px, py, 18, FILL1, col, 2); ctext(d, px, py, lab, FT, col)
    ctext(d, 145, 305, "化学種 i が混在", FT, GRAY)
    # 矢印1: 各種のモル濃度
    arrow(d, 258, 210, 320, 210, BLACK, 3, 12)
    box(d, 325, 150, 500, 270, (235, 242, 250))
    ctext(d, 412, 175, "各化学種の", FT, BLACK)
    ctext(d, 412, 205, "モル濃度", FS, BLUE)
    ctext(d, 412, 235, "rho Yi / Wi", FT, BLACK)
    # 矢印2: 総和 -> 全モル濃度
    arrow(d, 412, 278, 412, 320, BLACK, 3, 12)
    ctext(d, 412, 300, "総和", FT, GRAY, "lm")
    box(d, 300, 328, 525, 388, (235, 245, 235))
    ctext(d, 412, 358, "全モル濃度 c = 各種の和", FT, GREEN)
    # 矢印3: 理想気体式へ
    arrow(d, 528, 358, 600, 358, BLACK, 3, 12)
    box(d, 540, 150, 640, 300, FILL2)
    ctext(d, 590, 200, "理想", FT, BLACK)
    ctext(d, 590, 228, "気体", FT, BLACK)
    ctext(d, 590, 262, "p = c R0 T", FT, RED)
    note(d, "各種モル濃度 rho Yi/Wi を足して全モル濃度 -> p=cR0T へ(最終式は各自)")
    save(im, "t1e17StateEquation")


# ============================================================
# 17-15 t1e17LowMach : 低マッハ数燃焼流の特徴(helpful)
# ============================================================
def low_mach():
    im, d = new(); title(d, "低マッハ数燃焼流の特徴(密度変化は大きい)")
    # 4象限のカード
    cards = [
        (40, 80, "流速 << 音速", "マッハ数が小さい", BLUE, "flow"),
        (340, 80, "圧力はほぼ一定", "空間変動は音圧程度で小", GREEN, "flat"),
        (40, 240, "温度は大きく上昇", "発熱で数倍に", RED, "up"),
        (340, 240, "密度は大きく低下", "圧力一定でも温度上昇で", RED, "down"),
    ]
    for (x, y, head, sub, col, kind) in cards:
        box(d, x, y, x + 280, y + 145, (250, 250, 250))
        ctext(d, x + 140, y + 26, head, FS, col)
        ctext(d, x + 140, y + 120, sub, FT, GRAY)
        # 簡易アイコン(小グラフ)
        gx, gy, gw = x + 55, y + 90, 170
        if kind == "flow":
            arrow(d, gx, gy, gx + 60, gy, BLUE, 3, 11)
            ctext(d, gx + 100, gy, "<< 音速", FT, GRAY, "lm")
        elif kind == "flat":
            d.line((gx, gy, gx + gw, gy), fill=GREEN, width=3)
        elif kind == "up":
            d.line((gx, gy + 15, gx + 60, gy + 12, gx + 110, gy - 25, gx + gw, gy - 30), fill=RED, width=3, joint="curve")
        elif kind == "down":
            d.line((gx, gy - 28, gx + 60, gy - 24, gx + 110, gy + 10, gx + gw, gy + 14), fill=RED, width=3, joint="curve")
    note(d, "圧力だけが小さく変化. 温度・密度は大きく変化する非等温流")
    save(im, "t1e17LowMach")


# ============================================================
if __name__ == "__main__":
    air_fuel_ratio()          # 17-1
    equivalence_ratio()       # 17-2
    mole_mass_fraction()      # 17-3
    transport_units()         # 17-4
    lewis_number()            # 17-5
    dimensionless_numbers()   # 17-6
    soret_effect()            # 17-7
    conservation_eqs()        # 17-8
    progress_variable()       # 17-9
    favre_averaging()         # 17-10
    favre_relations()         # 17-11
    scalar_transport()        # 17-12
    continuity()              # 17-13
    state_equation()          # 17-14
    low_mach()                # 17-15
    print("done ch17")
