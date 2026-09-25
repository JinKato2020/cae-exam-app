# -*- coding: utf-8 -*-
"""振動2級 第8章「境界条件および荷重条件」公式・用語カード用の図 30枚。接頭辞 v2f8。
白地660×420・黒線画（figlib準拠）。公式カード＝回答後の根拠図なので結果・式を描いてよい。
文字化け回避のためギリシャ文字は綴り（alpha, beta, zeta, omega, lambda, theta）で書く。上付きは omega^2, B^T 等。
実行: python tools/figs_vib2ch8_f.py
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot, iso_box, bar,
                    F, FL, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN, ORANGE,
                    FILL1, FILL2, FILL3, W, H)


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=9):
    n = max(1, int(math.hypot(x2 - x1, y2 - y1) / seg))
    for k in range(n):
        if k % 2:
            continue
        t0, t1 = k / n, (k + 1) / n
        d.line([(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)], fill=col, width=wd)


def block(d, cx, cy, w, h, label="", fnt=FS, fill=FILL1, col=BLACK):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=col, width=3, fill=fill)
    if label:
        ctext(d, cx, cy, label, fnt)


def curve_arrow(d, cx, cy, r, a0, a1, col=BLUE, wd=3, head=12):
    d.arc((cx - r, cy - r, cx + r, cy + r), -a1, -a0, fill=col, width=wd)
    A = math.radians(a1)
    ex, ey = cx + r * math.cos(A), cy - r * math.sin(A)
    ang = math.atan2(-math.cos(A), -math.sin(A))
    for s in (0.5, -0.5):
        d.line((ex, ey, ex - head * math.cos(ang - s), ey - head * math.sin(ang - s)),
               fill=col, width=wd)


def dashrect(d, x0, y0, x1, y1, col=RED, wd=2):
    dash(d, x0, y0, x1, y0, col, wd)
    dash(d, x1, y0, x1, y1, col, wd)
    dash(d, x1, y1, x0, y1, col, wd)
    dash(d, x0, y1, x0, y0, col, wd)


def xmark(d, x, y, s=7, col=RED, wd=3):
    d.line((x - s, y - s, x + s, y + s), fill=col, width=wd)
    d.line((x - s, y + s, x + s, y - s), fill=col, width=wd)


def tri(d, p1, p2, p3, fill=FILL1, wd=3):
    d.polygon([p1, p2, p3], outline=BLACK, width=wd, fill=fill)


def dashpot(d, x0, y, x1, side_h=16, col=BLACK):
    xm = (x0 + x1) / 2
    d.line((x0, y, xm - 18, y), fill=col, width=3)
    d.line((xm - 18, y - side_h, xm + 22, y - side_h), fill=col, width=3)
    d.line((xm - 18, y + side_h, xm + 22, y + side_h), fill=col, width=3)
    d.line((xm - 18, y - side_h, xm - 18, y + side_h), fill=col, width=3)
    d.line((xm + 4, y - side_h + 4, xm + 4, y + side_h - 4), fill=col, width=4)
    d.line((xm + 4, y, x1, y), fill=col, width=3)


def ground(d, x0, x1, y, n=12):
    hwall(d, x0, x1, y, side=1, n=n)


# ============================================================
# 公式・用語図 v2f8（30枚）
# ============================================================

def f_quad_nodal_load():  # 1  v2f8QuadNodalLoad
    im, d = new(); title(d, "分布圧力→等価節点荷重（四角形1次要素）")
    ox, oy, s = 210, 130, 190
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    # 一様圧力 P（下向き矢印を上面に並べる）
    for i in range(5):
        x = ox + s * i / 4
        arrow(d, x, oy - 42, x, oy - 8, BLUE, 2, 9)
    ctext(d, ox + s / 2, oy - 58, "一様圧力 P（全体力 P x A）", FT, BLUE)
    corners = [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]
    for p in corners:
        node(d, p[0], p[1], 7, "white")
    # 各節点に F=PA/4
    ctext(d, ox + s / 2, oy + s / 2, "4節点で均等分担", FT, GRAY)
    for p in corners:
        sx = -1 if p[0] < ox + s / 2 else 1
        sy = -1 if p[1] < oy + s / 2 else 1
        arrow(d, p[0] + sx * 18, p[1] + sy * 18, p[0] + sx * 46, p[1] + sy * 46, RED, 3, 11)
    ctext(d, W / 2, oy + s + 40, "各節点  F = P x A / 4", FS, RED)
    save(im, "v2f8QuadNodalLoad")


def f_tri_nodal_load():  # 2  v2f8TriNodalLoad
    im, d = new(); title(d, "分布圧力→等価節点荷重（三角形1次要素）")
    # 正方形板を対角線で2三角形に分割
    A = (170, 320); B = (450, 320); C = (450, 110); Dp = (170, 110)
    d.rectangle((A[0], C[1], B[0], A[1]), outline=BLACK, width=3, fill=FILL1)
    d.line((Dp[0], Dp[1], B[0], B[1]), fill=BLACK, width=3)  # 対角線
    ctext(d, 310, 250, "要素1  P/2", FT, GRAY)
    ctext(d, 320, 175, "要素2  P/2", FT, GRAY)
    # 頂点節点（1要素のみ）
    node(d, A[0], A[1], 7, "white"); ctext(d, A[0] - 8, A[1] + 20, "F1 = P/6", FT, RED, "lm")
    node(d, C[0], C[1], 7, "white"); ctext(d, C[0] + 10, C[1] - 8, "F1 = P/6", FT, RED, "lm")
    # 対角線を共有する節点（2要素合計）
    node(d, Dp[0], Dp[1], 8, RED); ctext(d, Dp[0] - 8, Dp[1] - 8, "F2 = P/3", FT, RED, "rm")
    node(d, B[0], B[1], 8, RED); ctext(d, B[0] + 10, B[1] + 18, "F2 = P/3", FT, RED, "lm")
    ctext(d, W / 2, 390, "共有節点は2要素分を合計  F1 < F2", FT, BLUE)
    save(im, "v2f8TriNodalLoad")


def f_road_excitation_freq():  # 3  v2f8RoadExcitationFreq
    im, d = new(); title(d, "走行凹凸による励起周波数  f = v / lambda")
    ox, oy = 80, 300
    w = 500
    # 正弦路面
    pts = [(ox + w * i / 120, oy - 26 * math.sin(2 * math.pi * i / 40)) for i in range(121)]
    plot(d, 0, 0, pts, BLACK, 3)
    dim(d, ox, oy + 60, ox + w / 3, oy + 60, "波長 lambda", col=GRAY)
    # 車（矩形）＋速度
    cxx = ox + 250
    d.rectangle((cxx - 40, oy - 90, cxx + 40, oy - 50), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cxx - 34, oy - 54, cxx - 14, oy - 34), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((cxx + 14, oy - 54, cxx + 34, oy - 34), outline=BLACK, width=3, fill=FILL2)
    arrow(d, cxx + 40, oy - 70, cxx + 110, oy - 70, RED, 3, 12)
    ctext(d, cxx + 120, oy - 70, "速度 v", FT, RED, "lm")
    ctext(d, W / 2, 388, "1秒に乗り越える山の数 = f  （短い波長ほど高周波）", FT, BLUE)
    save(im, "v2f8RoadExcitationFreq")


def f_rpm_to_hz():  # 4  v2f8RpmToHz
    im, d = new(); title(d, "回転数(rpm) → 周波数(Hz)  f = rpm / 60")
    cx, cy = 200, 210
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 6, "white")
    curve_arrow(d, cx, cy, 92, 40, 320, BLUE, 3, 13)
    ctext(d, cx, cy + 105, "1分間に rpm 回転", FT, GRAY)
    # 変換矢印
    arrow(d, 320, cy, 400, cy, BLACK, 3, 13)
    ctext(d, 360, cy - 20, "/ 60", FS, RED)
    block(d, 520, cy, 200, 70, "f [Hz]\n(1秒あたり回転数)", FS, FILL2)
    ctext(d, W / 2, 388, "アンバランス振動は回転周波数と一致", FT, BLUE)
    save(im, "v2f8RpmToHz")


def f_support_stiffness():  # 5  v2f8SupportStiffness
    im, d = new(); title(d, "支持剛性  K = F / x")
    hwall(d, 130, 530, 120, side=-1, n=12)
    spring(d, 330, 120, 330, 250, coils=6, amp=22)
    block(d, 330, 300, 150, 70, "支持部", FS, FILL1)
    # 荷重F
    arrow(d, 330, 340, 330, 400, RED, 4, 14)
    ctext(d, 350, 380, "荷重 F", FT, RED, "lm")
    # 変位x
    arrow(d, 470, 250, 470, 300, BLUE, 3, 11)
    ctext(d, 485, 275, "変位 x", FT, BLUE, "lm")
    ctext(d, 130, 300, "K = F / x", F, RED, "lm")
    ctext(d, W / 2, 392, "mm は m に直す（x10^-3）", FT, GRAY)
    save(im, "v2f8SupportStiffness")


def f_large_mass_method():  # 6  v2f8LargeMassMethod
    im, d = new(); title(d, "大質量法（加速度加振）  F = M a")
    # 構造物
    d.rectangle((120, 130, 260, 320), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 190, 225, "解析対象", FT, GRAY)
    # 剛体結合
    for y in (170, 230, 290):
        dash(d, 260, y, 360, y, RED, 2)
    ctext(d, 310, 320, "剛体結合", FT, RED)
    # 大質量M
    d.ellipse((360, 175, 470, 285), outline=BLACK, width=4, fill=FILL3)
    ctext(d, 415, 230, "大質量 M", FS)
    ctext(d, 415, 300, "（数桁大きい）", FT, GRAY)
    # 入力力F
    arrow(d, 470, 230, 560, 230, BLUE, 4, 14)
    ctext(d, 555, 205, "力 F = M a", FS, BLUE, "rm")
    ctext(d, W / 2, 392, "F = M a より結合点に加速度 a を与える", FT, BLUE)
    save(im, "v2f8LargeMassMethod")


def f_unbalance_force():  # 7  v2f8UnbalanceForce
    im, d = new(); title(d, "アンバランス加振力  F = m r omega^2")
    cx, cy = 190, 200
    r = 62
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 5, "white")
    # 偏心質量
    mx, my = cx + r * math.cos(math.radians(-35)), cy - r * math.sin(math.radians(-35))
    d.ellipse((mx - 12, my - 12, mx + 12, my + 12), outline=BLACK, width=2, fill=FILL3)
    ctext(d, mx + 6, my + 18, "質量 m", FT, GRAY, "lm")
    dash(d, cx, cy, mx, my, GRAY, 2); ctext(d, (cx + mx) / 2, (cy + my) / 2 - 12, "r", FT, GRAY)
    curve_arrow(d, cx, cy, 80, 10, 120, GRAY, 2, 10); ctext(d, cx - 8, cy - 92, "omega", FT, GRAY)
    # 遠心力（外向き）
    arrow(d, mx, my, mx + 40, my + 28, RED, 4, 13)
    ctext(d, mx + 46, my + 34, "F", FS, RED, "lm")
    # グラフ：車速-加振力 2次曲線
    ox, oy = 380, 330
    axes(d, ox, oy, 230, 200, "回転数", "F", GRAY)
    gp = [(ox + 210 * i / 40, oy - 180 * (i / 40) ** 2) for i in range(41)]
    plot(d, 0, 0, gp, BLUE, 3)
    ctext(d, ox + 120, oy - 150, "F ~ omega^2", FT, BLUE)
    ctext(d, W / 2, 400, "回転数2倍で加振力4倍（2次曲線）", FT, BLUE)
    save(im, "v2f8UnbalanceForce")


def f_phase_diff_wheelbase():  # 8  v2f8PhaseDiffWheelbase
    im, d = new(); title(d, "前後輪の位相差  d_phi = 2 pi L / lambda")
    ox, oy = 70, 250
    w = 520
    pts = [(ox + w * i / 120, oy - 30 * math.sin(2 * math.pi * i / 40)) for i in range(121)]
    plot(d, 0, 0, pts, BLACK, 3)
    dim(d, ox, oy + 70, ox + w / 3, oy + 70, "波長 lambda (= 2 pi)", col=GRAY)
    # 前輪・後輪
    xr = ox + 130; xf = ox + 320
    for (x, lab) in ((xr, "後輪"), (xf, "前輪")):
        yy = oy - 30 * math.sin(2 * math.pi * (x - ox) / (w / 3))
        d.ellipse((x - 20, yy - 40, x + 20, yy), outline=BLACK, width=3, fill=FILL2)
        ctext(d, x, yy - 55, lab, FT, GRAY)
    dim(d, xr, oy - 100, xf, oy - 100, "ホイールベース L", col=RED)
    ctext(d, W / 2, 390, "同じ入力を位相差 2 pi L / lambda だけずらす", FT, BLUE)
    save(im, "v2f8PhaseDiffWheelbase")


def f_boundary_condition():  # 9  v2f8BoundaryCondition
    im, d = new(); title(d, "境界条件（拘束条件）")
    # 塔状構造物を地面に固定
    d.rectangle((280, 90, 380, 300), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 195, "構造物", FT, GRAY)
    ground(d, 180, 480, 300, n=14)
    # 拘束記号（並進拘束）
    for x in (300, 360):
        arrow(d, x, 300, x, 340, RED, 0, 0)
    xmark(d, 300, 320, 8, RED, 3); xmark(d, 360, 320, 8, RED, 3)
    ctext(d, 330, 355, "接地位置で並進を拘束", FT, RED)
    ctext(d, W / 2, 392, "止める節点・方向を実物どおりに設定", FT, BLUE)
    save(im, "v2f8BoundaryCondition")


def f_equiv_nodal_load():  # 10  v2f8EquivNodalLoad
    im, d = new(); title(d, "等価節点荷重（分布荷重→節点集中力）")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：分布圧力
    ox, oy, s = 90, 150, 150
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for i in range(5):
        x = ox + s * i / 4
        arrow(d, x, oy - 34, x, oy - 6, BLUE, 2, 8)
    ctext(d, ox + s / 2, oy + s + 26, "分布圧力 P", FT, GRAY)
    # 変換
    arrow(d, 250, 230, 340, 230, BLACK, 3, 13)
    # 右：節点集中力
    ox2, oy2 = 400, 150
    d.rectangle((ox2, oy2, ox2 + s, oy2 + s), outline=BLACK, width=3, fill=FILL2)
    for p in [(ox2, oy2), (ox2 + s, oy2), (ox2 + s, oy2 + s), (ox2, oy2 + s)]:
        node(d, p[0], p[1], 6, "white")
        sy = -22 if p[1] < oy2 + s / 2 else 22
        arrow(d, p[0], p[1] - sy - (14 if sy < 0 else -14), p[0], p[1], RED, 3, 10)
    ctext(d, ox2 + s / 2, oy2 + s + 26, "各節点に集中力（P/4）", FT, RED)
    ctext(d, W / 2, 392, "力は節点でしか受けられない", FT, BLUE)
    save(im, "v2f8EquivNodalLoad")


def f_simple_support():  # 11  v2f8SimpleSupport
    im, d = new(); title(d, "単純支持（変位0・傾きは自由）")
    cy = 200
    d.line((150, cy, 510, cy), fill=BLACK, width=6)
    node(d, 150, cy, 7, "white"); node(d, 510, cy, 7, "white")
    pin_support(d, 150, cy)
    roller_support(d, 510, cy)
    # たわみ形状（傾きあり）
    dp = [(150 + 360 * i / 40, cy + 40 * math.sin(math.pi * i / 40)) for i in range(41)]
    plot(d, 0, 0, dp, BLUE, 2)
    ctext(d, 150, cy - 30, "w=0", FT, RED); ctext(d, 510, cy - 30, "w=0", FT, RED)
    ctext(d, 330, cy - 40, "傾き w' は拘束しない", FT, GREEN)
    ctext(d, W / 2, 380, "変位のみ0（傾きも0にすると固定支持）", FT, BLUE)
    save(im, "v2f8SimpleSupport")


def f_fixed_support():  # 12  v2f8FixedSupport
    im, d = new(); title(d, "固定支持・埋め込み拘束（変位も傾きも0）")
    wall(d, 200, 110, 300, side=1, n=9)
    cy = 205
    d.line((200, cy, 500, cy), fill=BLACK, width=6)
    node(d, 200, cy, 7, "white"); node(d, 500, cy, 7, "white")
    ctext(d, 250, cy - 30, "w=0, w'=0", FT, RED)
    # たわみ形状（根元は水平）
    dp = [(200 + 300 * i / 40, cy + 55 * (1 - math.cos(math.pi / 2 * i / 40))) for i in range(41)]
    plot(d, 0, 0, dp, BLUE, 2)
    ctext(d, W / 2, 360, "コンクリート埋め込み部などは並進も回転も拘束", FT, BLUE)
    save(im, "v2f8FixedSupport")


def f_symmetry_plane():  # 13  v2f8SymmetryPlane
    im, d = new(); title(d, "対称面・鏡面対称（1/2モデル化）")
    # 全体形状
    cx = 330
    dash(d, cx, 80, cx, 330, RED, 2)
    ctext(d, cx, 350, "対称面", FT, RED)
    # 左半分（実モデル）
    d.polygon([(150, 300), (cx, 300), (cx, 150), (230, 120)], outline=BLACK, width=3, fill=FILL1)
    ctext(d, 235, 240, "1/2モデル", FT, GRAY)
    # 右半分（省略・淡色破線）
    dash(d, cx, 300, 510, 300, LGRAY, 2)
    dash(d, cx, 150, 430, 120, LGRAY, 2)
    dash(d, 510, 300, 430, 120, LGRAY, 2)
    ctext(d, 450, 240, "省略", FT, LGRAY)
    # 対称面上の節点に面外拘束
    for y in (180, 240, 290):
        node(d, cx, y, 5, "white")
        xmark(d, cx + 16, y, 6, RED, 2)
    ctext(d, W / 2, 388, "対称面：面外並進＋対称を崩す回転を拘束", FT, BLUE)
    save(im, "v2f8SymmetryPlane")


def f_out_of_plane():  # 14  v2f8OutOfPlane
    im, d = new(); title(d, "面外変形の拘束（対称面を突き抜けない）")
    cx = 300
    # 対称面（縦の面）
    d.line((cx, 100, cx, 330), fill=BLACK, width=3)
    dash(d, cx, 90, cx, 100, RED, 2)
    ctext(d, cx, 350, "対称面", FT, RED)
    node(d, cx, 215, 8, "white")
    # 面外方向（水平）の動きを禁止
    arrow(d, cx, 215, cx + 70, 215, LGRAY, 2, 10)
    arrow(d, cx, 215, cx - 70, 215, LGRAY, 2, 10)
    xmark(d, cx + 80, 215, 9, RED, 3)
    xmark(d, cx - 80, 215, 9, RED, 3)
    ctext(d, cx + 120, 245, "面外変位=0", FT, RED)
    # 面内は自由（縦方向）
    arrow(d, cx, 215, cx, 150, GREEN, 2, 9)
    ctext(d, cx - 55, 150, "面内は自由", FT, GREEN, "rm")
    ctext(d, W / 2, 388, "面に垂直な方向の並進変位を0にする", FT, BLUE)
    save(im, "v2f8OutOfPlane")


def f_dof_constraint():  # 15  v2f8DOFConstraint
    im, d = new(); title(d, "拘束自由度（並進3＋回転3）")
    cx, cy = 210, 200
    node(d, cx, cy, 8, "white")
    # 並進3方向
    arrow(d, cx, cy, cx + 70, cy, BLUE, 3, 11); ctext(d, cx + 80, cy, "Tx", FT, BLUE, "lm")
    arrow(d, cx, cy, cx, cy - 70, BLUE, 3, 11); ctext(d, cx, cy - 84, "Ty", FT, BLUE)
    arrow(d, cx, cy, cx - 50, cy + 40, BLUE, 3, 11); ctext(d, cx - 60, cy + 48, "Tz", FT, BLUE, "rm")
    # 回転3方向
    curve_arrow(d, cx, cy, 40, 200, 320, GREEN, 2, 9)
    ctext(d, cx - 6, cy + 62, "Rx, Ry, Rz", FT, GREEN)
    # 表
    tx, ty = 400, 130
    rows = [["Tx", "拘束"], ["Ty", "自由"], ["Tz", "自由"],
            ["Rx", "自由"], ["Ry", "拘束"], ["Rz", "拘束"]]
    for i, (a, b) in enumerate(rows):
        yy = ty + i * 38
        col = RED if b == "拘束" else GREEN
        ctext(d, tx, yy, a, FS, BLACK, "lm")
        ctext(d, tx + 60, yy, b, FS, col, "lm")
    ctext(d, W / 2, 392, "6自由度の拘束・自由の組合せで指定", FT, BLUE)
    save(im, "v2f8DOFConstraint")


def f_large_mass_term():  # 16  v2f8LargeMassTerm
    im, d = new(); title(d, "大質量法（加速度加振の実現手法）")
    # 構造物（塔）＋基礎に大質量
    d.rectangle((280, 90, 380, 250), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 170, "構造物", FT, GRAY)
    for x in (300, 360):
        dash(d, x, 250, x, 290, RED, 2)
    ctext(d, 450, 275, "剛体結合", FT, RED, "lm")
    d.ellipse((260, 290, 400, 360), outline=BLACK, width=4, fill=FILL3)
    ctext(d, 330, 325, "大質量 M", FS)
    arrow(d, 400, 325, 500, 325, BLUE, 4, 14)
    ctext(d, 505, 325, "M a", FS, BLUE, "lm")
    ctext(d, W / 2, 392, "F = M a で狙った加速度を発生させる", FT, BLUE)
    save(im, "v2f8LargeMassTerm")


def f_seismic_analysis():  # 17  v2f8SeismicAnalysis
    im, d = new(); title(d, "地震応答解析（加速度は基礎から入力）")
    # 塔
    d.rectangle((290, 90, 370, 300), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 190, "構造物", FT, GRAY)
    ground(d, 180, 480, 300, n=14)
    # 基礎に加速度入力（左右）
    arrow(d, 200, 340, 280, 340, RED, 4, 14)
    arrow(d, 460, 340, 380, 340, RED, 4, 14)
    ctext(d, 330, 340, "地震加速度", FT, RED)
    # 応答（先端が揺れる）
    dash(d, 330, 90, 300, 90, BLUE, 2)
    dash(d, 330, 90, 360, 90, BLUE, 2)
    ctext(d, W / 2, 392, "動的応答解析で変位・応力を求める", FT, BLUE)
    save(im, "v2f8SeismicAnalysis")


def f_dominant_freq():  # 18  v2f8DominantFreq
    im, d = new(); title(d, "卓越振動数（最も揺れを支配する周波数）")
    ox, oy = 90, 320
    axes(d, ox, oy, 480, 240, "振動数", "エネルギー", GRAY)
    # ピークのあるスペクトル
    pk = 28
    sp = [(ox + 460 * i / 60,
           oy - 210 * math.exp(-((i - pk) / 9.0) ** 2)) for i in range(61)]
    plot(d, 0, 0, sp, BLUE, 3)
    xp = ox + 460 * pk / 60
    dash(d, xp, oy, xp, oy - 210, RED, 2)
    ctext(d, xp, oy - 228, "卓越振動数", FT, RED)
    # 固有振動数が近いと共振
    node(d, xp + 6, oy + 16, 4, RED)
    ctext(d, W / 2, 392, "固有振動数がここに入ると共振の危険", FT, BLUE)
    save(im, "v2f8DominantFreq")


def f_dynamic_vs_modal():  # 19  v2f8DynamicVsModal
    im, d = new(); title(d, "固有値解析と動的応答解析の使い分け")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：固有値解析（周波数のみ）
    ctext(d, 165, 90, "固有値解析", FS, BLUE)
    ox, oy = 70, 260
    axes(d, ox, oy, 200, 140, "振動数", "", GRAY)
    for fx in (0.3, 0.55, 0.8):
        x = ox + 200 * fx
        d.line((x, oy, x, oy - 120), fill=BLUE, width=3)
    ctext(d, 165, 300, "共振周波数と揺れ方", FT, GRAY)
    ctext(d, 165, 330, "→ 振幅は分からない", FT, RED)
    # 右：動的応答解析（時刻歴）
    ctext(d, 495, 90, "動的応答解析", FS, GREEN)
    ox2, oy2 = 380, 190
    axes(d, ox2, oy2, 220, 90, "時間", "", GRAY)
    tp = [(ox2 + 210 * i / 60, oy2 - 60 * math.exp(-0.02 * i) * math.sin(2 * math.pi * i / 15)) for i in range(61)]
    plot(d, 0, 0, tp, GREEN, 2)
    ctext(d, 495, 300, "実際の応答振幅・時間変化", FT, GRAY)
    ctext(d, 495, 330, "→ 揺れの大きさが分かる", FT, GREEN)
    save(im, "v2f8DynamicVsModal")


def f_transient_response():  # 20  v2f8TransientResponse
    im, d = new(); title(d, "過渡応答解析（初速度→自由振動）")
    # 衝突：刃先が岩に当たる
    d.polygon([(120, 200), (200, 180), (200, 240)], outline=BLACK, width=3, fill=FILL1)
    ctext(d, 160, 165, "刃先", FT, GRAY)
    d.rectangle((200, 160, 250, 260), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 225, 285, "岩盤", FT, GRAY)
    # 初速度
    arrow(d, 150, 210, 195, 210, RED, 4, 13)
    ctext(d, 145, 235, "初速度（初期値）", FT, RED, "lm")
    # 自由振動の時刻歴
    ox, oy = 300, 300
    axes(d, ox, oy, 300, 140, "時間", "応答", GRAY)
    tp = [(ox + 290 * i / 80, oy - 90 - 55 * math.exp(-0.035 * i) * math.sin(2 * math.pi * i / 16)) for i in range(81)]
    plot(d, 0, 0, tp, BLUE, 2)
    ctext(d, W / 2, 392, "衝突後の速度を初期条件に時刻歴を追う", FT, BLUE)
    save(im, "v2f8TransientResponse")


def f_random_vibration():  # 21  v2f8RandomVibration
    im, d = new(); title(d, "ランダム振動（不規則・統計的に扱う）")
    import random
    random.seed(8)
    ox, oy = 80, 200
    w = 500
    pts = []
    v = 0
    for i in range(w + 1):
        v += random.uniform(-6, 6)
        v *= 0.9
        pts.append((ox + i, oy + v))
    plot(d, 0, 0, pts, BLACK, 2)
    axes(d, ox - 10, 330, w + 20, 260, "時間", "変位", GRAY)
    ctext(d, W / 2, 360, "決まった波形を持たない → PSD で入力", FS, BLUE)
    ctext(d, W / 2, 392, "路面走行・地震などの不規則振動", FT, GRAY)
    save(im, "v2f8RandomVibration")


def f_psd():  # 22  v2f8PSD
    im, d = new(); title(d, "パワースペクトル密度（PSD）")
    ox, oy = 90, 320
    axes(d, ox, oy, 480, 250, "振動数", "PSD（パワー密度）", GRAY)
    sp = [(ox + 460 * i / 60,
           oy - 200 * (0.4 * math.exp(-((i - 15) / 8.0) ** 2)
                       + 0.9 * math.exp(-((i - 38) / 6.0) ** 2) + 0.05)) for i in range(61)]
    plot(d, 0, 0, sp, BLUE, 3)
    ctext(d, ox + 300, oy - 190, "各周波数のエネルギー分布", FT, GRAY)
    ctext(d, W / 2, 392, "大きさの分布のみ（位相情報は持たない）", FT, BLUE)
    save(im, "v2f8PSD")


def f_rms():  # 23  v2f8RMS
    im, d = new(); title(d, "RMS値（応答PSDの面積の平方根）")
    ox, oy = 90, 320
    axes(d, ox, oy, 470, 240, "振動数", "応答PSD", GRAY)
    sp = [oy - 190 * (0.9 * math.exp(-((i - 34) / 8.0) ** 2) + 0.05) for i in range(61)]
    poly = [(ox, oy)] + [(ox + 450 * i / 60, sp[i]) for i in range(61)] + [(ox + 450, oy)]
    d.polygon(poly, fill=FILL3, outline=BLUE)
    plot(d, 0, 0, [(ox + 450 * i / 60, sp[i]) for i in range(61)], BLUE, 3)
    ctext(d, ox + 255, oy - 90, "面積 = 積分", FT, GRAY)
    ctext(d, W / 2, 388, "RMS = sqrt( PSD を全周波数で積分 )", FS, RED)
    save(im, "v2f8RMS")


def f_time_history():  # 24  v2f8TimeHistory
    im, d = new(); title(d, "時刻歴（応答を時間の関数で表す）")
    ox, oy = 80, 210
    axes(d, ox, oy, 500, 150, "時間 t", "応答", GRAY)
    tp = [(ox + 480 * i / 120, oy - 90 * math.exp(-0.012 * i) * math.sin(2 * math.pi * i / 22)) for i in range(121)]
    plot(d, 0, 0, tp, BLUE, 2)
    ctext(d, W / 2, 330, "確定的な入力（地震波形など）に向く", FS, BLUE)
    ctext(d, W / 2, 372, "ランダム振動は PSD・RMS で評価", FT, GRAY)
    save(im, "v2f8TimeHistory")


def f_fatigue_freq():  # 25  v2f8FatigueFreq
    im, d = new(); title(d, "疲労評価のための周波数選定")
    ox, oy = 90, 320
    axes(d, ox, oy, 480, 250, "振動数", "振幅 / 応答", GRAY)
    # 入力振幅スペクトル
    inp = [(ox + 460 * i / 60, oy - 200 * (0.8 * math.exp(-((i - 14) / 7.0) ** 2) + 0.04)) for i in range(61)]
    plot(d, 0, 0, inp, BLUE, 2)
    ctext(d, ox + 110, oy - 190, "入力が大きい周波数", FT, BLUE)
    xi = ox + 460 * 14 / 60
    dash(d, xi, oy, xi, oy - 175, BLUE, 2)
    # 固有振動数（共振）
    xr = ox + 460 * 42 / 60
    d.line((xr, oy, xr, oy - 210), fill=RED, width=3)
    ctext(d, xr, oy - 228, "固有振動数（共振）", FT, RED)
    ctext(d, W / 2, 392, "両方を正弦波入力で検討する", FT, GREEN)
    save(im, "v2f8FatigueFreq")


def f_psd_relation():  # 26  v2f8PSDRelation
    im, d = new(); title(d, "変位・速度・加速度の PSD 関係")
    ox, oy = 100, 330
    axes(d, ox, oy, 445, 260, "振動数", "PSD", GRAY)
    # 交点（omega=1 付近）
    xj = ox + 90
    dash(d, xj, oy, xj, oy - 240, LGRAY, 2)
    ctext(d, xj, oy + 16, "omega=1", FT, GRAY)
    # 変位（右下がり）
    disp = [(ox + 20 + 430 * i / 60, oy - 40 - 150 * math.exp(-2.2 * i / 60)) for i in range(61)]
    plot(d, 0, 0, disp, BLUE, 3); ctext(d, ox + 430, oy - 55, "変位", FT, BLUE, "lm")
    # 速度（omega倍）
    vel = [(ox + 20 + 430 * i / 60, oy - 70 - 90 * math.exp(-0.8 * i / 60)) for i in range(61)]
    plot(d, 0, 0, vel, GREEN, 3); ctext(d, ox + 430, oy - 130, "速度", FT, GREEN, "lm")
    # 加速度（omega^2倍・右上がり）
    acc = [(ox + 20 + 430 * i / 60, oy - 90 - 140 * (i / 60) ** 1.4) for i in range(61)]
    plot(d, 0, 0, acc, RED, 3); ctext(d, ox + 430, oy - 235, "加速度", FT, RED, "lm")
    ctext(d, W / 2, 400, "高周波側は 加速度 > 速度 > 変位（omega, omega^2 倍）", FT, BLUE)
    save(im, "v2f8PSDRelation")


def f_forced_displacement():  # 27  v2f8ForcedDisplacement
    im, d = new(); title(d, "強制変位入力（変位そのものを与える）")
    # タイヤ接地面に変位入力
    cx, cy = 300, 190
    d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=BLACK, width=2, fill=FILL3)
    ctext(d, cx, cy - 78, "タイヤ", FT, GRAY)
    # 接地面
    node(d, cx, cy + 55, 6, "white")
    arrow(d, cx, cy + 110, cx, cy + 62, RED, 4, 13)
    ctext(d, cx + 15, cy + 95, "強制変位", FT, RED, "lm")
    # 路面うねり
    ox = 130
    pts = [(ox + 340 * i / 60, cy + 130 - 12 * math.sin(2 * math.pi * i / 20)) for i in range(61)]
    plot(d, 0, 0, pts, BLACK, 3)
    ctext(d, W / 2, 388, "路面変形がタイヤ変形より十分小さいとき有効", FT, BLUE)
    save(im, "v2f8ForcedDisplacement")


def f_spring_damper_boundary():  # 28  v2f8SpringDamperBoundary
    im, d = new(); title(d, "ばね要素・減衰要素による境界のモデル化")
    # 車体側（固定壁）＝左、部材＝右。ばねと減衰を並列で結合
    wall(d, 130, 120, 300, side=1, n=9)
    spring(d, 130, 165, 380, coils=6, amp=16)
    dashpot(d, 130, 250, 380, 16)
    d.rectangle((380, 130, 480, 285), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 430, 207, "部材", FS)
    ctext(d, 250, 138, "ばね（剛性）", FT, GRAY)
    ctext(d, 250, 285, "減衰", FT, GRAY)
    ctext(d, W / 2, 350, "ウェザーストリップは剛性＋減衰の両方で表す", FS, BLUE)
    ctext(d, W / 2, 388, "（バックドア全周などの弾性境界）", FT, GRAY)
    save(im, "v2f8SpringDamperBoundary")


def f_rigid_mass_element():  # 29  v2f8RigidMassElement
    im, d = new(); title(d, "剛体要素・質量要素の使い分け")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：剛とみなせる → 剛体要素
    ctext(d, 165, 88, "十分剛な部分", FS, BLUE)
    cg = (165, 210)
    d.rectangle((cg[0] - 55, cg[1] - 30, cg[0] + 55, cg[1] + 30), outline=BLACK, width=3, fill=FILL1)
    for s in ((70, 320), (260, 320)):
        d.line((cg[0], cg[1] + 30, s[0], s[1]), fill=BLACK, width=4)
        node(d, s[0], s[1], 6, "white")
    ctext(d, 165, 350, "剛体要素で結合（変形不要）", FT, GRAY)
    # 右：慣性のみ → 質量要素
    ctext(d, 495, 88, "重さだけ効く付属物", FS, GREEN)
    d.rectangle((430, 190, 560, 250), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 495, 220, "主構造", FT, GRAY)
    d.ellipse((483, 140, 507, 164), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 495, 128, "質量要素", FT, GREEN)
    arrow(d, 495, 164, 495, 188, GRAY, 2, 8)
    ctext(d, 495, 350, "慣性（重さ）だけを表す", FT, GRAY)
    save(im, "v2f8RigidMassElement")


def f_wheelbase():  # 30  v2f8Wheelbase
    im, d = new(); title(d, "ホイールベース（前後車軸間距離 L）")
    cy = 200
    # 車体
    d.rectangle((190, cy - 60, 470, cy - 20), outline=BLACK, width=3, fill=FILL1)
    d.polygon([(230, cy - 60), (270, cy - 95), (390, cy - 95), (430, cy - 60)],
              outline=BLACK, width=3, fill=FILL2)
    # 車輪
    xr, xf = 240, 420
    for x in (xr, xf):
        d.ellipse((x - 26, cy - 20, x + 26, cy + 32), outline=BLACK, width=3, fill=FILL3)
        node(d, x, cy + 6, 5, "white")
    d.line((190, cy + 60, 470, cy + 60), fill=BLACK, width=2)
    dim(d, xr, cy + 60, xf, cy + 60, "ホイールベース L", col=RED)
    ctext(d, W / 2, 320, "前輪・後輪が同じ凹凸を時間差で通過", FT, GRAY)
    ctext(d, W / 2, 360, "位相差 = 2 pi L / lambda", FS, BLUE)
    save(im, "v2f8Wheelbase")


if __name__ == "__main__":
    for fn in [f_quad_nodal_load, f_tri_nodal_load, f_road_excitation_freq,
               f_rpm_to_hz, f_support_stiffness, f_large_mass_method,
               f_unbalance_force, f_phase_diff_wheelbase, f_boundary_condition,
               f_equiv_nodal_load, f_simple_support, f_fixed_support,
               f_symmetry_plane, f_out_of_plane, f_dof_constraint,
               f_large_mass_term, f_seismic_analysis, f_dominant_freq,
               f_dynamic_vs_modal, f_transient_response, f_random_vibration,
               f_psd, f_rms, f_time_history, f_fatigue_freq, f_psd_relation,
               f_forced_displacement, f_spring_damper_boundary,
               f_rigid_mass_element, f_wheelbase]:
        fn()
    print("done 30")
