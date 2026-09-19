# -*- coding: utf-8 -*-
"""熱流体力学1級 第8章「結果と評価」問題図 14枚。figlibで白地660x420線画。
required(回答前提示) の8枚は「形・配置・軸」だけを中立に描き、正解の数値・結論注記・
選択肢番号は一切描かない。helpful(回答後) は理解補助のラベルまで(「正解は○」等は描かない)。"""
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


# ============================================================ 8-1 ヘルムホルツ共振器(helpful)
def f_helmholtz():
    im, d = new()
    title(d, "圧力測定孔＝ヘルムホルツ共振器(集中定数系)")
    # 左：物理的な孔の断面
    ctext(d, 185, 70, "圧力測定孔の断面", FS, BLACK)
    # 計器本体(固体)
    box(d, 95, 95, 275, 300, FILL2)
    # 小空間(体積V・白抜き)＋圧力変換器
    box(d, 120, 118, 250, 178, "white")
    ctext(d, 185, 138, "小空間 体積 V", FT, BLACK)
    box(d, 150, 152, 220, 170, (225, 235, 250))
    ctext(d, 185, 161, "圧力変換器", FT, BLUE)
    # 直管部(白抜きの細い管・長さL 径d)
    tx0, tx1 = 176, 194
    box(d, tx0, 178, tx1, 300, "white")
    # 壁面(=流れ側)と流れ
    d.line((95, 300, 275, 300), fill=BLACK, width=4)
    for gx in range(100, 276, 30):
        if gx < tx0 - 4 or gx > tx1 + 4:
            arrow(d, gx - 12, 322, gx + 12, 322, GRAY, 2, 8)
    ctext(d, 185, 342, "流れ(計測面)", FT, GRAY)
    # 寸法 L と d
    dim(d, 210, 178, 210, 300, "L(直管部)", col=GRAY)
    dim(d, tx0, 210, tx1, 210, "d", col=GRAY)
    # 右：ばね質量系との対応
    dash(d, 330, 85, 330, 350, LGRAY, 2, 8, 6)
    ctext(d, 500, 70, "ばね質量系との対応", FS, BLACK)
    hwall(d, 440, 560, 110, -1)
    spring(d, 500, 110, 500, 200, coils=5, amp=16, wd=3)
    ctext(d, 560, 155, "ばね\n小空間 V の\n圧縮性", FT, GREEN, "lm")
    fbox(d, 500, 240, 120, 56, "質量\n直管部の流体", (235, 240, 250), FT)
    arrow(d, 500, 272, 500, 320, RED, 3, 12)
    arrow(d, 500, 320, 500, 272, RED, 3, 12)
    ctext(d, 560, 300, "振動", FT, RED, "lm")
    note(d, "直管部の流体が質量、小空間の圧縮性がばねとして働く共振系になる")
    save(im, "t1e8Helmholtz")


# ============================================================ 8-2 流速測定法の使い分け(helpful)
def f_velocimetry_map():
    im, d = new()
    title(d, "流速測定法の使い分けマップ")
    # 左：大域=PIV
    box(d, 55, 70, 320, 300, (238, 242, 250))
    ctext(d, 187, 92, "大域的な速度場", FS, BLACK)
    ctext(d, 187, 116, "PIV(面を同時計測)", FT, BLUE)
    for i in range(5):
        for j in range(4):
            x = 95 + i * 45; y = 150 + j * 32
            arrow(d, x, y, x + 26, y - 8, BLUE, 2, 8)
    ctext(d, 187, 288, "照明面内の速度ベクトルを一括取得", FT, GRAY)
    # 右：局所=熱線流速計
    box(d, 340, 70, 605, 300, (235, 245, 235))
    ctext(d, 472, 92, "局所の乱流強度", FS, BLACK)
    ctext(d, 472, 116, "熱線流速計(1点の高速変動)", FT, GREEN)
    node(d, 400, 200, 6, RED, RED)
    ctext(d, 400, 222, "計測点", FT, RED)
    ox, oy = 430, 200
    pts = []
    for k in range(46):
        t = k / 45.0
        pts.append((ox + t * 150, oy - 34 * math.sin(t * 22) * math.exp(-0.0) * (0.4 + 0.6 * abs(math.sin(t * 7)))))
    curve(d, pts, GREEN, 2)
    ctext(d, 505, 250, "速い変動を高応答で計測", FT, GRAY)
    # 下段の注記
    note(d, "点計測(LDV・ピトー管)は面計測にトラバースが要り、断面計測(電磁・超音波)は局所変動が取れない", H - 40)
    save(im, "t1e8VelocimetryMap")


# ============================================================ 8-3 格子細分化と実験値比較(required)
def f_grid_convergence():
    im, d = new()
    title(d, "格子細分化にともなう平均圧力の変化")
    ox, oy = 100, 345
    axes(d, ox, oy, 480, 285, "格子細分化(粗→細)", "平均圧力 p")
    # 収束値(漸近線)
    yc = oy - 0.92 * 275
    dash(d, ox, yc, ox + 470, yc, LGRAY, 2, 9, 6)
    ctext(d, ox + 400, yc - 14, "収束値", FT, GRAY, "lm")
    # 計算点 A(粗)→D(細)
    data = [("A", 0.14, 0.60), ("B", 0.38, 0.78), ("C", 0.63, 0.86), ("D", 0.86, 0.90)]
    pts = []
    for name, fx, fy in data:
        x = ox + fx * 470; y = oy - fy * 275
        pts.append((x, y))
    curve(d, pts, BLUE, 3)
    for (name, fx, fy), (x, y) in zip(data, pts):
        node(d, x, y, 5, BLUE, BLUE)
        ctext(d, x, y - 18, name, FT, BLUE)
    # 実験値 E (■)
    ex, ey = ox + 0.50 * 470, oy - 0.80 * 275
    d.rectangle((ex - 6, ey - 6, ex + 6, ey + 6), fill=BLACK)
    ctext(d, ex + 30, ey, "実験値 E", FT, BLACK, "lm")
    save(im, "t1e8GridConvergence")


# ============================================================ 8-4 移流スキームの波形(required)
def f_advection_schemes():
    im, d = new()
    title(d, "移流する矩形波に対する3つの数値解")
    labels = ["(a)", "(b)", "(c)"]
    x0s = [55, 260, 465]
    w = 150
    base = 320
    top = 130          # 波高1.0の位置
    for idx, x0 in enumerate(x0s):
        # 軸(下線)
        d.line((x0, base, x0 + w, base), fill=BLACK, width=2)
        # 厳密解の矩形波(破線)
        rl, rr = x0 + w * 0.30, x0 + w * 0.62
        dash(d, rl, base, rl, top, GRAY, 2, 7, 5)
        dash(d, rl, top, rr, top, GRAY, 2, 7, 5)
        dash(d, rr, top, rr, base, GRAY, 2, 7, 5)
        # 数値解
        pts = []
        for k in range(0, w + 1, 3):
            x = x0 + k
            u = (x - x0) / float(w)
            if idx == 0:      # (a) ほぼ矩形を維持(鋭い台形)
                if u < 0.26 or u > 0.66:
                    v = 0.0
                elif u < 0.30:
                    v = (u - 0.26) / 0.04
                elif u > 0.62:
                    v = (0.66 - u) / 0.04
                else:
                    v = 1.0
            elif idx == 1:    # (b) なだらかにぼやけた山(ガウス)
                v = math.exp(-((u - 0.46) ** 2) / (2 * 0.11 ** 2)) * 0.9
            else:             # (c) 上部が振動
                if 0.30 <= u <= 0.62:
                    v = 1.0 + 0.22 * math.sin((u - 0.30) / 0.32 * math.pi * 5)
                elif 0.20 <= u < 0.30:
                    v = 0.28 * math.sin((u - 0.20) / 0.10 * math.pi * 2)
                elif 0.62 < u <= 0.74:
                    v = 0.28 * math.sin((0.74 - u) / 0.12 * math.pi * 2)
                else:
                    v = 0.0
            v = max(v, 0.0)
            pts.append((x, base - v * (base - top)))
        curve(d, pts, BLUE, 2)
        ctext(d, x0 + w / 2, base + 24, labels[idx], FS, BLACK)
    ctext(d, W / 2, 78, "破線＝厳密解(矩形波) / 実線＝数値解", FT, GRAY)
    save(im, "t1e8AdvectionSchemes")


# ============================================================ 8-5 薄翼の揚力係数-迎角曲線(required)
def f_airfoil_cl_alpha():
    im, d = new()
    title(d, "薄翼の揚力係数-迎角曲線")
    ox, oy = 100, 350
    axes(d, ox, oy, 470, 300, "迎角 α", "揚力係数 CL")
    sx = 470 / 20.0
    sy = 270 / 1.7
    px = lambda a: ox + a * sx
    py = lambda c: oy - c * sy
    # 実際の傾向：α=12で失速→急低下
    act = []
    for a in [i * 0.5 for i in range(0, 41)]:
        if a <= 12:
            c = 0.10 * a
        else:
            c = 1.20 - 0.16 * (a - 12)
        act.append((px(a), py(max(c, 0.1))))
    curve(d, act, RED, 3)
    ctext(d, px(15.5), py(0.35), "実際", FT, RED, "lm")
    # 標準k-ε：失速角が右へ、ピーク後は緩やか
    ke = []
    for a in [i * 0.5 for i in range(0, 41)]:
        if a <= 16:
            c = 0.095 * a
        else:
            c = 1.52 - 0.05 * (a - 16)
        ke.append((px(a), py(c)))
    curve(d, ke, BLUE, 3)
    ctext(d, px(17), py(1.55), "計算(k-ε)", FT, BLUE, "lm")
    # 翼型の小アイコン
    ax, ay = 150, 110
    d.polygon([(ax, ay), (ax + 90, ay - 10), (ax + 130, ay), (ax + 90, ay + 4), (ax, ay)],
              outline=BLACK, width=2, fill=FILL1)
    save(im, "t1e8AirfoilCLalpha")


# ============================================================ 8-6 LES比較の可否マトリクス(helpful)
def f_les_compare_matrix():
    im, d = new()
    title(d, "LES結果の比較検討：組合せの可否")
    cols = ["PTV", "DNS", "ピトー管", "LDV\n(ｱﾝｻﾝﾌﾞﾙ平均)"]
    rows = ["瞬時値", "時間平均"]
    x0, y0 = 190, 120
    cw, ch = 105, 90
    # 列見出し
    for j, c in enumerate(cols):
        cx = x0 + cw / 2 + j * cw
        for i, line in enumerate(c.split("\n")):
            ctext(d, cx, y0 - 34 + i * 16, line, FT, BLACK)
    # 行見出し
    for i, r in enumerate(rows):
        ctext(d, x0 - 40, y0 + ch / 2 + i * ch, r, FT, BLACK)
    # 罫線
    for i in range(len(rows) + 1):
        d.line((x0, y0 + i * ch, x0 + len(cols) * cw, y0 + i * ch), fill=BLACK, width=2)
    for j in range(len(cols) + 1):
        d.line((x0 + j * cw, y0, x0 + j * cw, y0 + len(rows) * ch), fill=BLACK, width=2)
    # セルの記入(瞬時値どうしの直接比較=不適、時間平均×LDV=妥当)
    def cell(i, j, mark, sub, col):
        cx = x0 + cw / 2 + j * cw; cy = y0 + ch / 2 + i * ch
        ctext(d, cx, cy - 12, mark, F, col)
        ctext(d, cx, cy + 16, sub, FT, col)
    cell(0, 0, "×", "不適", RED)
    cell(0, 1, "×", "不適", RED)
    cell(0, 2, "×", "不適", RED)
    cell(1, 3, "○", "妥当", GREEN)
    d.rectangle((x0 + 3 * cw, y0 + ch, x0 + 4 * cw, y0 + 2 * ch), outline=GREEN, width=4)
    note(d, "時間平均LES と アンサンブル平均LDV の比較だけがエルゴード性で成立する")
    save(im, "t1e8LESCompareMatrix")


# ============================================================ 8-7 サイクロンの旋回速度分布(required)
def f_cyclone_vortex():
    im, d = new()
    title(d, "サイクロン断面の旋回方向速度分布")
    ox, oy = 105, 345
    axes(d, ox, oy, 470, 285, "半径位置(内壁→中心軸)", "旋回速度")
    xl = 470
    # 計算(k-ε)：内壁0→中心へ直線増加(三角形)
    d.line((ox, oy, ox + xl, oy - 0.88 * 265), fill=BLUE, width=3)
    ctext(d, ox + xl - 8, oy - 0.88 * 265 - 14, "計算(k-ε)", FT, BLUE, "rm")
    # 参考：ランキン渦(外側=自由渦で減少・中心付近=強制渦で0へ、途中ピーク)
    pts = []
    for k in range(0, 471, 6):
        u = k / 470.0                       # 0=内壁, 1=中心
        # ピークを u=0.55 付近に。壁(左)で0、中心(右)で0
        if u < 0.55:
            v = 0.62 * (u / 0.55)           # 自由渦側の立ち上がり(壁で0)
        else:
            v = 0.62 * ((1 - u) / 0.45)     # 強制渦側(中心で0)
        pts.append((ox + k, oy - v * 265))
    dash_pts = pts
    for i in range(len(dash_pts) - 1):
        if i % 2 == 0:
            d.line((dash_pts[i][0], dash_pts[i][1], dash_pts[i + 1][0], dash_pts[i + 1][1]), fill=GRAY, width=2)
    ctext(d, ox + 0.55 * xl, oy - 0.62 * 265 - 16, "ランキン渦(参考)", FT, GRAY)
    save(im, "t1e8CycloneVortex")


# ============================================================ 8-8 PIVとCFDの比較(helpful)
def f_piv_cfd():
    im, d = new()
    title(d, "遠心ポンプ 2次元PIV と CFD の比較の注意点")
    # 左：2次元PIV計測面(ローカル座標)
    ctext(d, 165, 70, "2次元PIV(ローカル座標)", FT, BLACK)
    d.polygon([(70, 130), (250, 110), (250, 240), (70, 260)], outline=BLUE, width=3, fill=(235, 240, 250))
    ctext(d, 160, 100, "シート光", FT, ORANGE)
    for i in range(4):
        for j in range(3):
            x = 100 + i * 42; y = 150 + j * 34
            arrow(d, x, y - 4, x + 24, y - 10, BLUE, 2, 7)
    # 右：CFD計算格子(全体座標)
    ctext(d, 500, 70, "CFD(全体座標)", FT, BLACK)
    box(d, 410, 110, 590, 250, "white")
    for gx in range(410, 591, 30):
        d.line((gx, 110, gx, 250), fill=LGRAY, width=1)
    for gy in range(110, 251, 28):
        d.line((410, gy, 590, gy), fill=LGRAY, width=1)
    # 座標変換の矢印
    arrow(d, 258, 185, 402, 185, RED, 3, 13)
    ctext(d, 330, 168, "速度ベクトルの座標変換", FT, RED)
    # 下段の注記
    ctext(d, W / 2, 300, "定常RANS → 実験の時間平均と比較", FT, GRAY)
    ctext(d, W / 2, 326, "非定常RANS/LES → 双方を時間平均して比較", FT, GRAY)
    ctext(d, W / 2, 352, "カルマン渦 → ストローハル数で評価", FT, GRAY)
    save(im, "t1e8PIVCFD")


# ============================================================ 8-9 曲がり管路の2次流れ(required)
def f_bend_secondary_flow():
    im, d = new()
    title(d, "曲がり出口断面の速度分布")
    ox, oy = 95, 340
    axes(d, ox, oy, 320, 285, "位置 x/D(内壁→外壁)", "速度 v/U")
    xl = 320
    # 計算(実線)：内壁側で立ち上がり外壁側で最大
    calc = []
    for k in range(0, 321, 6):
        u = k / 320.0
        v = 0.30 + 0.60 * u ** 1.4
        calc.append((ox + k, oy - v * 265))
    curve(d, calc, BLUE, 3)
    ctext(d, ox + xl - 4, oy - 0.90 * 265 - 14, "計算", FT, BLUE, "rm")
    # 実験(○)：計算より全体に高め
    for k in range(20, 321, 40):
        u = k / 320.0
        v = 0.30 + 0.60 * u ** 1.4 + 0.12
        node(d, ox + k, oy - v * 265, 5, "white", RED)
    ctext(d, ox + 120, oy - 0.98 * 265, "実験", FT, RED, "lm")
    # 別枠：断面内の第1種2次流れ(一対の渦)
    cx, cy = 520, 235
    box(d, cx - 80, cy - 85, cx + 80, cy + 85, "white")
    ctext(d, cx, cy - 100, "断面内の2次流れ", FT, BLACK)
    swirl(d, cx - 38, cy, 34, cw=False, col=GREEN, wd=2)
    swirl(d, cx + 38, cy, 34, cw=True, col=GREEN, wd=2)
    save(im, "t1e8BendSecondaryFlow")


# ============================================================ 8-10 抗力予測精度の散布図(required)
def f_drag_scatter():
    im, d = new()
    title(d, "抗力係数の予測精度：計算 vs 実験")
    ox, oy = 110, 350
    axes(d, ox, oy, 400, 300, "CD(Comp.)", "CD(Exp.)")
    L = 380
    # 一致線
    dash(d, ox, oy, ox + L, oy - L * (300 / 400.0), GRAY, 2, 9, 6)
    ctext(d, ox + L - 10, oy - L * (300 / 400.0) + 16, "一致線", FT, GRAY, "rm")
    sx = L / 1.0
    sy = (300) / 1.0
    px = lambda v: ox + v * sx
    py = lambda v: oy - v * sy
    # 一致線近傍のケース
    good = [("No.2", 0.30, 0.31), ("No.3", 0.40, 0.42), ("No.4", 0.50, 0.50),
            ("No.5", 0.58, 0.59), ("No.6", 0.66, 0.67), ("No.8", 0.74, 0.73)]
    for name, xc, yc in good:
        node(d, px(xc), py(yc), 5, BLUE, BLUE)
        ctext(d, px(xc) + 8, py(yc) - 10, name, FT, BLUE, "lm")
    # 外れる2ケース No.1, No.7
    for name, xc, yc in [("No.1", 0.24, 0.44), ("No.7", 0.80, 0.55)]:
        node(d, px(xc), py(yc), 6, "white", RED)
        ctext(d, px(xc) + 8, py(yc) - 10, name, FT, RED, "lm")
    # 右上：後部傾斜角の定義図
    bx, by = 540, 110
    d.polygon([(bx - 55, by + 25), (bx + 35, by + 25), (bx + 20, by - 5), (bx - 40, by - 5)],
              outline=BLACK, width=2, fill=FILL1)
    d.line((bx + 35, by + 25, bx + 60, by + 25), fill=BLACK, width=2)
    dash(d, bx + 20, by - 5, bx + 60, by - 5, GRAY, 1, 5, 4)
    ctext(d, bx + 30, by + 6, "α", FT, RED)
    ctext(d, bx, by + 40, "後部傾斜角", FT, GRAY)
    save(im, "t1e8DragScatter")


# ============================================================ 8-11 建物まわり k-ε vs ASM(required)
def f_building_ke_asm():
    im, d = new()
    title(d, "建物まわり乱流：実験・k-ε・ASM の比較")
    names = ["(1) 実験", "(2) k-ε", "(3) ASM"]
    x0s = [40, 245, 450]
    pw = 170
    floor = 320
    for idx, x0 in enumerate(x0s):
        cx = x0 + pw / 2
        ctext(d, cx, 72, names[idx], FS, BLACK)
        # 床
        d.line((x0, floor, x0 + pw, floor), fill=BLACK, width=3)
        # 建物(立方体)
        bx0, bx1 = cx - 30, cx + 30
        bt = floor - 70
        box(d, bx0, bt, bx1, floor, FILL2)
        # 流入
        arrow(d, x0 + 2, bt + 20, bx0 - 4, bt + 20, BLUE, 2, 9)
        # 前面よどみ部の乱れエネルギー(k-εでは過大=大きめ)
        r = 30 if idx == 1 else 14
        d.ellipse((bx0 - r, bt + 10 - r / 2, bx0 - 2, bt + 10 + r / 2), outline=RED, width=2)
        if idx == 1:
            ctext(d, bx0 - 20, bt - 6, "乱れ過大", FT, RED)
        # 上面の剥離渦：実験・ASMは有り、k-εは消失(直進)
        if idx == 1:
            arrow(d, bx0 - 6, bt - 6, bx1 + 30, bt - 10, BLUE, 2, 9)
            ctext(d, cx, bt - 26, "剥離消失", FT, GRAY)
        else:
            swirl(d, cx, bt - 22, 20, cw=True, col=BLUE, wd=2)
            ctext(d, cx, bt - 48, "剥離渦", FT, GRAY)
        # 後方循環
        swirl(d, bx1 + 22, floor - 28, 16, cw=False, col=GREEN, wd=2)
    save(im, "t1e8BuildingKeASM")


# ============================================================ 8-12 平行平板間乱流 U+-y+(required)
def f_les_log_law():
    im, d = new()
    title(d, "平行平板間乱流の平均速度分布 U+ - y+")
    ox, oy = 100, 350
    xlen, ylen = 460, 300
    axes(d, ox, oy, xlen, ylen, "y+", "U+")
    xL = lambda v: ox + (math.log10(v) / 3.0) * xlen     # y+:1..1000
    yU = lambda u: oy - (u / 30.0) * ylen                # U+:0..30
    # 目盛り(y+ 10^0..10^3)
    for e in range(0, 4):
        v = 10 ** e
        d.line((xL(v), oy, xL(v), oy - ylen), fill=LGRAY, width=1)
        ctext(d, xL(v), oy + 14, "10^%d" % e, FT, BLACK)
    for u in (0, 10, 20, 30):
        ctext(d, ox - 12, yU(u), str(u), FT, BLACK, "rm")
    # DNS(実線)
    def udns(yp):
        return min(yp, 2.44 * math.log(yp) + 5.0)
    dns = []
    yp = 1.0
    while yp <= 1000:
        dns.append((xL(yp), yU(udns(yp))))
        yp *= 1.06
    curve(d, dns, BLACK, 3)
    ctext(d, xL(300), yU(udns(300)) + 18, "DNS", FT, BLACK, "lm")
    # LES(○)：対数領域で上側へずれる
    yp = 1.2
    pts = []
    while yp <= 1000:
        shift = max(0.0, 2.2 * (math.log10(yp) - 1.5))
        pts.append((xL(yp), yU(udns(yp) + shift)))
        yp *= 1.9
    for x, y in pts:
        node(d, x, y, 4, "white", BLUE)
    ctext(d, xL(250), yU(udns(250) + 3.0) - 16, "LES", FT, BLUE, "lm")
    save(im, "t1e8LESLogLaw")


# ============================================================ 8-13 数値解析の3つの誤差(helpful)
def f_three_errors():
    im, d = new()
    title(d, "数値解析における3つの誤差の関係")
    ys = 175
    boxes = [(105, "実際の\n流れ現象"), (265, "支配方程式\nの厳密解"),
             (425, "離散化方程式\nの厳密解"), (585, "反復計算\nの解")]
    for cx, s in boxes:
        fbox(d, cx, ys, 130, 66, s, (238, 242, 250), FT)
    arrows = [(105, 265, "モデリング誤差", "実験と比較して評価", RED),
              (265, 425, "離散化誤差", "格子の優劣で変わる", BLUE),
              (425, 585, "収束誤差", "反復の収束で抑える", GREEN)]
    for x1, x2, name, sub, col in arrows:
        arrow(d, x1 + 65, ys, x2 - 65, ys, col, 3, 13)
        mx = (x1 + x2) / 2
        ctext(d, mx, ys - 30, name, FT, col)
        ctext(d, mx, ys + 34, sub, FT, GRAY)
    note(d, "左から右へ、現象→支配方程式→離散化方程式→反復解 と近似が進む")
    save(im, "t1e8ThreeErrors")


# ============================================================ 8-14 プログラム検証の例題(helpful)
def f_verification_cases():
    im, d = new()
    title(d, "流体解析プログラムの検証例題と着目点")
    # (1) キャビティフロー
    box(d, 45, 80, 245, 235, "white")
    ctext(d, 145, 96, "キャビティフロー", FT, BLACK)
    arrow(d, 70, 118, 220, 118, BLUE, 2, 10)
    swirl(d, 145, 175, 42, cw=True, col=GRAY, wd=2)
    ctext(d, 145, 222, "閉空間の渦", FT, GRAY)
    # (2) バックステップ流れ
    box(d, 260, 80, 615, 235, "white")
    ctext(d, 437, 96, "バックステップ流れ", FT, BLACK)
    d.line((275, 140, 340, 140), fill=BLACK, width=3)
    d.line((340, 140, 340, 185), fill=BLACK, width=3)
    d.line((340, 185, 600, 185), fill=BLACK, width=3)
    arrow(d, 280, 125, 335, 125, BLUE, 2, 9)
    swirl(d, 375, 168, 16, cw=True, col=GREEN, wd=2)
    dash(d, 340, 205, 470, 205, RED, 2, 7, 5)
    ctext(d, 470, 216, "再付着距離", FT, RED, "lm")
    ctext(d, 437, 226, "剥離・再付着", FT, GRAY)
    # (3) ポアズイユ流れ
    box(d, 45, 250, 245, 400, "white")
    ctext(d, 145, 266, "ポアズイユ流れ", FT, BLACK)
    d.line((70, 292, 220, 292), fill=BLACK, width=3)
    d.line((70, 380, 220, 380), fill=BLACK, width=3)
    cy = 336
    for j in range(-4, 5):
        yy = cy + j * 10
        vx = 60 * (1 - (j / 4.0) ** 2)
        arrow(d, 90, yy, 90 + vx, yy, BLUE, 2, 7)
    curve(d, [(90 + 60 * (1 - (j / 4.0) ** 2), cy + j * 10) for j in range(-4, 5)], RED, 2)
    ctext(d, 145, 392, "放物線分布＋解析解比較", FT, GRAY)
    # (4) 円柱まわり流れ
    box(d, 260, 250, 615, 400, "white")
    ctext(d, 437, 266, "円柱まわり流れ", FT, BLACK)
    arrow(d, 275, 320, 320, 320, BLUE, 2, 9)
    node(d, 350, 320, 16, FILL2, BLACK)
    swirl(d, 405, 305, 13, cw=True, col=GREEN, wd=2)
    swirl(d, 445, 335, 13, cw=False, col=GREEN, wd=2)
    swirl(d, 485, 305, 13, cw=True, col=GREEN, wd=2)
    ctext(d, 437, 392, "カルマン渦・圧力係数分布", FT, GRAY)
    save(im, "t1e8VerificationCases")


if __name__ == "__main__":
    f_helmholtz()
    f_velocimetry_map()
    f_grid_convergence()
    f_advection_schemes()
    f_airfoil_cl_alpha()
    f_les_compare_matrix()
    f_cyclone_vortex()
    f_piv_cfd()
    f_bend_secondary_flow()
    f_drag_scatter()
    f_building_ke_asm()
    f_les_log_law()
    f_three_errors()
    f_verification_cases()
    print("done t1e8 (14)")
