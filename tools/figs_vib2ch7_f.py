# -*- coding: utf-8 -*-
"""振動2級 第7章「モデリングの基礎」公式・用語カード用の図 30枚。接頭辞 v2f7。
白地660×420・黒線画（figlib準拠）。公式カード＝回答後の根拠図なので結果・式を描いてよい。
文字化け回避のためギリシャ文字は綴り（zeta, eta, alpha, beta, rho, lambda, nu）で書く。上付きはB^T等。
実行: python tools/figs_vib2ch7_f.py
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot, iso_box,
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


# ============================================================
# 公式・用語図 v2f7（30枚）
# ============================================================

def f_rayleigh_damping():  # 1
    im, d = new(); title(d, "レイリー減衰  [C] = alpha[M] + beta[K]")
    ox, oy = 110, 330
    axes(d, ox, oy, 440, 240, "振動数", "減衰比")
    p1 = [(ox + 400 * i / 60, oy - 190 * (0.85 * math.exp(-3.2 * i / 60) + 0.03)) for i in range(61)]
    plot(d, 0, 0, p1, GREEN, 2)
    ctext(d, ox + 130, oy - 140, "alpha[M]（低周波に効く）", FT, GREEN)
    p2 = [(ox + 400 * i / 60, oy - 190 * (0.9 * i / 60 + 0.02)) for i in range(61)]
    plot(d, 0, 0, p2, ORANGE, 2)
    ctext(d, ox + 300, oy - 55, "beta[K]（高周波に効く）", FT, ORANGE)
    ps = [(ox + 400 * i / 60, oy - 190 * (0.85 * math.exp(-3.2 * i / 60) + 0.9 * i / 60 + 0.05)) for i in range(61)]
    plot(d, 0, 0, ps, BLUE, 3)
    ctext(d, W / 2, 388, "[M]と[K]の重み付き線形和で[C]を作る", FT, GRAY)
    save(im, "v2f7RayleighDamping")


def f_eta_zeta():  # 2
    im, d = new(); title(d, "減衰比 zeta と損失係数 eta")
    ox, oy = 130, 330
    axes(d, ox, oy, 400, 240, "zeta", "eta")
    plot(d, 0, 0, [(ox, oy), (ox + 360, oy - 220)], BLUE, 3)
    ctext(d, ox + 280, oy - 175, "eta = 2 zeta", F, BLUE)
    node(d, ox + 180, oy - 110, 4, RED)
    ctext(d, W / 2, 388, "損失係数は減衰比の約2倍", FT, GRAY)
    save(im, "v2f7EtaZeta")


def f_quad_shape():  # 3
    im, d = new(); title(d, "四角形1次要素（双一次・xy項あり）")
    ox, oy = 200, 130
    s = 180
    d.rectangle((ox, oy, ox + s, oy + s), outline=BLACK, width=3, fill=FILL1)
    for p in [(ox, oy), (ox + s, oy), (ox + s, oy + s), (ox, oy + s)]:
        node(d, p[0], p[1], 7, "white")
    ctext(d, ox + s / 2, oy + s / 2, "4節点", FT, GRAY)
    ctext(d, W / 2, 348, "u = a1 + a2 x + a3 y + a4 xy （滑らか）", FS, BLUE)
    save(im, "v2f7QuadShape")


def f_tri_shape():  # 4
    im, d = new(); title(d, "三角形1次要素（1次・定ひずみ）")
    P1 = (150, 320); P2 = (430, 320); P3 = (290, 150)
    tri(d, P1, P2, P3, fill=FILL2)
    for p in (P1, P2, P3):
        node(d, p[0], p[1], 7, "white")
    ctext(d, 290, 265, "ひずみ一定", FT, RED)
    ctext(d, W / 2, 358, "u = a1 + a2 x + a3 y （定ひずみ要素・3節点）", FS, BLUE)
    save(im, "v2f7TriShape")


def f_acoustic_mesh():  # 5
    im, d = new(); title(d, "音場のメッシュ（波長の1/6以下に刻む）")
    ox, oy = 90, 210
    w = 480
    pts = [(ox + w * i / 80, oy - 45 * math.sin(2 * math.pi * i / 80)) for i in range(81)]
    plot(d, 0, 0, pts, BLUE, 2)
    d.line((ox, oy, ox + w, oy), fill=LGRAY, width=1)
    for i in range(7):
        x = ox + w * i / 6
        d.line((x, oy - 52, x, oy + 52), fill=GRAY, width=1)
        node(d, x, oy, 3, "white")
    dim(d, ox, oy + 70, ox + w, oy + 70, "1波長 lambda", col=GRAY)
    ctext(d, W / 2, 330, "波1周期を6分割（要素寸法 <= lambda/6）", FS, BLUE)
    save(im, "v2f7AcousticMesh")


def f_viscous_damping():  # 6
    im, d = new(); title(d, "粘性減衰（速度に比例する減衰力）")
    dashpot(d, 130, 180, 420, 20)
    arrow(d, 420, 180, 500, 180, RED, 3, 12)
    ctext(d, 510, 180, "速度 v", FT, RED, "lm")
    ctext(d, W / 2, 270, "減衰力 = c v （速度比例）", FS, BLUE)
    ctext(d, W / 2, 320, "1周期あたりの損失は振動数に依存", FT, GRAY)
    save(im, "v2f7ViscousDamping")


def f_hysteretic_damping():  # 7
    im, d = new(); title(d, "ヒステリシス減衰（履歴ループ）")
    ox, oy = 300, 200
    pts = [(ox + 90 * math.cos(2 * math.pi * i / 60),
            oy - 55 * math.sin(2 * math.pi * i / 60) - 26 * math.cos(2 * math.pi * i / 60))
           for i in range(61)]
    plot(d, 0, 0, pts, BLUE, 2)
    axes(d, ox - 120, oy + 90, 240, 180, "変位", "力", GRAY)
    ctext(d, W / 2, 330, "振幅のみに依存（材料内部・接合部すべり）", FT, GRAY)
    ctext(d, W / 2, 366, "ループ面積 = 1周期の散逸エネルギー", FT, BLUE)
    save(im, "v2f7HystereticDamping")


def f_friction_damping():  # 8
    im, d = new(); title(d, "摩擦減衰（クーロン摩擦・接触面すべり）")
    hwall(d, 150, 510, 250, side=1, n=12)
    d.rectangle((230, 190, 430, 250), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 220, "ボルト締結部", FT, GRAY)
    arrow(d, 430, 220, 500, 220, RED, 3, 12)
    ctext(d, 510, 220, "すべり", FT, RED, "lm")
    # 摩擦力
    arrow(d, 330, 252, 330, 285, GREEN, 3, 11)
    ctext(d, 330, 300, "摩擦力（一定・向きは速度と逆）", FT, GREEN)
    save(im, "v2f7FrictionDamping")


def f_damping_ratio():  # 9
    im, d = new(); title(d, "減衰比 zeta（実減衰 / 臨界減衰）")
    ox, oy = 100, 220
    axes(d, ox, oy, 460, 150, "時間", "変位", GRAY)
    # zeta=0（減衰なし）
    p0 = [(ox + 420 * i / 120, oy - 90 * math.sin(2 * math.pi * i / 30)) for i in range(121)]
    plot(d, 0, 0, p0, LGRAY, 1)
    ctext(d, ox + 420, oy - 95, "zeta=0", FT, GRAY, "lm")
    # zeta 中間（減衰振動）
    pz = [(ox + 420 * i / 120, oy - 90 * math.exp(-0.05 * i) * math.sin(2 * math.pi * i / 30)) for i in range(121)]
    plot(d, 0, 0, pz, BLUE, 2)
    ctext(d, ox + 250, oy - 70, "0<zeta<1（減衰振動）", FT, BLUE)
    # zeta=1（臨界・振動せず戻る）
    pc = [(ox + 420 * i / 120, oy - 80 * math.exp(-0.09 * i)) for i in range(121)]
    plot(d, 0, 0, pc, RED, 2)
    ctext(d, ox + 250, oy + 50, "zeta=1（臨界減衰）", FT, RED)
    save(im, "v2f7DampingRatio")


def f_loss_factor():  # 10
    im, d = new(); title(d, "損失係数 eta（履歴ループ面積 / 弾性エネ）")
    ox, oy = 300, 200
    pts = [(ox + 95 * math.cos(2 * math.pi * i / 60),
            oy - 55 * math.sin(2 * math.pi * i / 60) - 24 * math.cos(2 * math.pi * i / 60))
           for i in range(61)]
    d.polygon(pts, outline=BLUE, width=2, fill=FILL3)
    axes(d, ox - 125, oy + 90, 250, 180, "変位", "力", GRAY)
    ctext(d, ox, oy, "ループ面積", FT, GRAY)
    ctext(d, W / 2, 340, "eta が大きいほど制振材の性能が高い", FT, BLUE)
    save(im, "v2f7LossFactor")


def f_proportional_damping():  # 11
    im, d = new(); title(d, "比例粘性（レイリー）モデル [C]=aM+bK")
    # ばね＋ダッシュポット並列（比例減衰の模式）
    hwall(d, 130, 530, 130, side=-1, n=12)
    spring(d, 200, 180, 340, coils=6, amp=14)
    dashpot(d, 200, 250, 340, 16)
    d.rectangle((340, 150, 440, 280), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 390, 215, "m", FS)
    ctext(d, 270, 200, "剛性 K", FT, GRAY)
    ctext(d, 270, 280, "減衰 C", FT, GRAY)
    ctext(d, W / 2, 360, "[C]=aM+bK → モード直交性が成立", FS, BLUE)
    save(im, "v2f7ProportionalDamping")


def f_modal_orthogonality():  # 12
    im, d = new(); title(d, "モード直交性（各固有モードが独立）")
    matrix_grid(d, 150, 140, [["m1", "0", "0"], ["0", "m2", "0"], ["0", "0", "m3"]],
                cell=52, fnt=FS)
    ctext(d, 150 + 1.5 * 52, 140 + 3 * 52 + 20, "M・Kが対角化", FT, GRAY)
    ctext(d, 470, 180, "各モードが", FT, BLUE)
    ctext(d, 470, 208, "互いに独立", FT, BLUE)
    ctext(d, 470, 250, "→ 連成方程式を", FT, GRAY)
    ctext(d, 470, 278, "モード分解できる", FT, GRAY)
    save(im, "v2f7ModalOrthogonality")


def f_shell_element():  # 13
    im, d = new(); title(d, "シェル要素（曲面薄肉・面内＋面外曲げ）")
    # 曲面（円弧状）シェル
    ox, oy = 150, 220
    pts = [(ox + 360 * i / 40, oy - 60 * math.sin(math.pi * i / 40)) for i in range(41)]
    d.line(pts, fill=BLACK, width=3, joint="curve")
    off = [(p[0], p[1] + 14) for p in pts]
    d.line(off, fill=BLACK, width=3, joint="curve")
    for i in (0, 20, 40):
        d.line((pts[i][0], pts[i][1], off[i][0], off[i][1]), fill=BLACK, width=2)
    ctext(d, W / 2, 300, "面内変形＋面外曲げを表す2次元要素", FS, BLUE)
    ctext(d, W / 2, 345, "薄肉の曲面構造に用いる", FT, GRAY)
    save(im, "v2f7ShellElement")


def f_axisym_shell():  # 14
    im, d = new(); title(d, "軸対称シェル（断面のみで表現）")
    cx = 300
    dash(d, cx, 100, cx, 340, LGRAY)  # 回転軸
    ctext(d, cx, 350, "回転軸", FT, GRAY)
    # 断面（片側の母線）
    prof = [(cx + 60, 320), (cx + 60, 180), (cx + 30, 140), (cx + 30, 120)]
    d.line(prof, fill=BLACK, width=4)
    # 回転で生成される面のイメージ（薄い弧）
    d.arc((cx - 60, 300, cx + 60, 340), 0, 180, fill=LGRAY, width=2)
    d.arc((cx - 60, 100, cx + 60, 140), 0, 180, fill=LGRAY, width=2)
    ctext(d, W / 2, 380, "非対称な付属物は表現できない", FT, RED)
    save(im, "v2f7AxisymShell")


def f_plate_element():  # 15
    im, d = new(); title(d, "板要素（薄板の面内・面外変形）")
    # 四角形板
    ox, oy = 200, 140
    iso_box(d, ox, oy, 200, 12, 90)
    # たわみ（面外）
    arrow(d, ox + 100, oy - 6, ox + 100, oy - 46, RED, 3, 12)
    ctext(d, ox + 100, oy - 60, "面外たわみ", FT, RED)
    ctext(d, W / 2, 300, "三角形・四角形の板要素", FS, BLUE)
    ctext(d, W / 2, 345, "面内変形と面外曲げを表す", FT, GRAY)
    save(im, "v2f7PlateElement")


def f_solid_element():  # 16
    im, d = new(); title(d, "ソリッド要素（3次元の体積・厚み変化）")
    iso_box(d, 200, 180, 160, 120, 80)
    ctext(d, W / 2, 340, "3次元の応力・厚み方向の変化を表す", FS, BLUE)
    ctext(d, W / 2, 380, "四面体・六面体などの立体要素", FT, GRAY)
    save(im, "v2f7SolidElement")


def f_beam_element():  # 17
    im, d = new(); title(d, "はり要素（断面特性＋要素長で剛性決定）")
    cy = 200
    d.line((130, cy, 500, cy), fill=BLACK, width=7)
    node(d, 130, cy, 6, "white"); node(d, 500, cy, 6, "white")
    ctext(d, 315, cy - 20, "軸・断面中心に節点", FT, GRAY)
    dim(d, 130, cy + 40, 500, cy + 40, "要素長 L", col=GRAY)
    # 断面
    d.rectangle((300, 290, 340, 350), outline=BLACK, width=2, fill=FILL1)
    ctext(d, 380, 320, "断面特性 A, I", FT, BLUE, "lm")
    ctext(d, W / 2, 388, "曲げ・軸・ねじりを表す線要素", FT, GRAY)
    save(im, "v2f7BeamElement")


def f_rod_element():  # 18
    im, d = new(); title(d, "棒（トラス）要素（軸方向力のみ）")
    cy = 200
    d.line((130, cy, 500, cy), fill=BLACK, width=5)
    node(d, 130, cy, 6, "white"); node(d, 500, cy, 6, "white")
    arrow(d, 130, cy, 90, cy, RED, 3, 11)
    arrow(d, 500, cy, 540, cy, RED, 3, 11)
    ctext(d, W / 2, cy - 26, "軸方向の引張・圧縮のみ", FS, BLUE)
    ctext(d, W / 2, 320, "曲げ剛性を持たない（トラス材）", FT, GRAY)
    save(im, "v2f7RodElement")


def f_rigid_element():  # 19
    im, d = new(); title(d, "剛体要素（変形しない結合要素）")
    cg = (300, 200)
    d.ellipse((cg[0] - 12, cg[1] - 12, cg[0] + 12, cg[1] + 12), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cg[0], cg[1] - 30, "集中質量（重心）", FT, GRAY)
    # 剛体の腕を支持点へ
    sup = [(150, 320), (450, 320), (500, 130)]
    for s in sup:
        d.line((cg[0], cg[1], s[0], s[1]), fill=BLACK, width=4)
        node(d, s[0], s[1], 6, "white")
    ctext(d, W / 2, 370, "重心から支持点へ伸ばす剛体の腕（変形しない）", FT, BLUE)
    save(im, "v2f7RigidElement")


def f_spring_damper_element():  # 20
    im, d = new(); title(d, "ばね・減衰要素（防振ゴムマウント）")
    hwall(d, 130, 530, 130, side=-1, n=12)
    spring(d, 230, 180, 380, coils=6, amp=14)
    dashpot(d, 230, 250, 380, 16)
    d.rectangle((380, 150, 470, 280), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 425, 215, "質量", FS)
    ctext(d, 300, 200, "ばね（剛性）", FT, GRAY)
    ctext(d, 300, 280, "減衰", FT, GRAY)
    ctext(d, W / 2, 350, "剛性＋減衰の組で防振ゴムを表す", FS, BLUE)
    save(im, "v2f7SpringDamperElement")


def f_lumped_mass():  # 21
    im, d = new(); title(d, "集中質量要素（質量＋慣性モーメント）")
    cx, cy = 300, 200
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cx, cy, "m", FS)
    block(d, 150, 130, 200, 42, "質量 m", FT, FILL1)
    arrow(d, 185, 151, cx - 14, cy - 12, GRAY, 2, 8)
    block(d, 490, 150, 240, 42, "重心まわり慣性モーメント", FT, FILL1)
    arrow(d, 420, 168, cx + 14, cy - 8, GRAY, 2, 8)
    ctext(d, W / 2, 330, "質量と慣性を1点に集約", FT, BLUE)
    save(im, "v2f7LumpedMass")


def f_mass_element():  # 22
    im, d = new(); title(d, "質量要素（慣性のみを表す）")
    cx, cy = 300, 200
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cx, cy, "m", FS)
    curve_arrow(d, cx, cy, 44, 210, 330, GREEN, 2, 10)
    ctext(d, cx, cy + 70, "質量・慣性モーメントのみ", FS, BLUE)
    ctext(d, W / 2, 340, "剛性・減衰は持たない", FT, GRAY)
    save(im, "v2f7MassElement")


def f_mpc():  # 23
    im, d = new(); title(d, "多点拘束要素（MPC）")
    master = (200, 200)
    node(d, master[0], master[1], 9, RED)
    ctext(d, master[0], master[1] - 26, "主節点", FT, RED)
    slaves = [(400, 130), (430, 220), (400, 310)]
    for s in slaves:
        dash(d, master[0], master[1], s[0], s[1], BLUE, 2)
        node(d, s[0], s[1], 6, "white")
    ctext(d, 430, 260, "従属節点", FT, GRAY, "lm")
    ctext(d, W / 2, 370, "複数節点の自由度を関係式で拘束", FS, BLUE)
    save(im, "v2f7MPC")


def f_shared_double_node():  # 24
    im, d = new(); title(d, "共有節点 と 二重節点（＋剛体結合）")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：共有節点（1個）
    ox = 100
    d.rectangle((ox, 160, ox + 160, 185), outline=BLACK, width=2, fill=FILL1)
    d.rectangle((ox, 185, ox + 160, 210), outline=BLACK, width=2, fill=FILL2)
    node(d, ox + 80, 185, 8, RED)
    ctext(d, ox + 80, 250, "共有節点（1個）", FT)
    # 右：二重節点（2個＋剛体結合）
    ox2 = 400
    d.rectangle((ox2, 155, ox2 + 160, 180), outline=BLACK, width=2, fill=FILL1)
    d.rectangle((ox2, 195, ox2 + 160, 220), outline=BLACK, width=2, fill=FILL2)
    node(d, ox2 + 80, 180, 7, "white")
    node(d, ox2 + 80, 195, 7, "white")
    dash(d, ox2 + 80, 180, ox2 + 80, 195, RED, 2)
    ctext(d, ox2 + 80, 250, "二重節点（2個＋剛体結合）", FT)
    save(im, "v2f7SharedDoubleNode")


def f_equiv_stiffness_density():  # 25
    im, d = new(); title(d, "リブを等価剛性・等価密度で側板に含める")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：詳細（側板＋リブ）
    ox = 110
    d.rectangle((ox, 150, ox + 150, 300), outline=BLACK, width=3, fill=FILL1)
    for y in (185, 230, 275):
        d.line((ox, y, ox + 150, y), fill=GRAY, width=3)
    ctext(d, ox + 75, 320, "側板＋リブ（詳細）", FT, GRAY)
    arrow(d, 275, 225, 360, 225, BLUE, 3, 13)
    # 右：等価（均質板）
    ox2 = 420
    d.rectangle((ox2, 150, ox2 + 150, 300), outline=BLACK, width=3, fill=FILL2)
    ctext(d, ox2 + 75, 225, "等価剛性・密度", FT, BLUE)
    ctext(d, ox2 + 75, 320, "均質な側板に簡略化", FT, GRAY)
    save(im, "v2f7EquivStiffnessDensity")


def f_added_mass():  # 26
    im, d = new(); title(d, "付加質量（剛性寄与小の部材＝重さのみ反映）")
    # 主構造
    d.rectangle((150, 170, 510, 230), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 200, "主構造（剛性を担う）", FT, GRAY)
    # 付加質量（集中質量として点で）
    for x in (230, 330, 430):
        d.ellipse((x - 12, 130, x + 12, 154), outline=BLACK, width=2, fill=FILL3)
        arrow(d, x, 154, x, 168, GRAY, 2, 7)
    ctext(d, 330, 110, "剛性寄与小の部材（集中質量／密度調整）", FT, BLUE)
    ctext(d, W / 2, 300, "重さだけを反映し剛性には加えない", FT, GRAY)
    save(im, "v2f7AddedMass")


def f_offset():  # 27
    im, d = new(); title(d, "オフセット（板中心面と節点位置のずれ）")
    ox, oy = 130, 180
    w = 400
    d.rectangle((ox, oy, ox + w, oy + 24), outline=BLACK, width=2, fill=FILL1)
    ctext(d, ox - 8, oy + 12, "板1", FT, GRAY, "rm")
    d.rectangle((ox, oy + 24, ox + w, oy + 52), outline=BLACK, width=2, fill=FILL3)
    ctext(d, ox - 8, oy + 38, "板2（制振材）", FT, GRAY, "rm")
    dash(d, ox, oy + 12, ox + w, oy + 12, BLUE, 1)
    dash(d, ox, oy + 38, ox + w, oy + 38, GREEN, 1)
    arrow(d, ox + w + 16, oy + 12, ox + w + 16, oy + 38, RED, 2, 8)
    ctext(d, ox + w + 22, oy + 25, "オフセット", FT, RED, "lm")
    ctext(d, W / 2, 320, "節点位置を板厚方向にずらして重ねる", FT, BLUE)
    save(im, "v2f7Offset")


def f_nugget():  # 28
    im, d = new(); title(d, "ナゲット（スポット溶接の溶融凝固部）")
    ox = 150
    d.rectangle((ox, 170, ox + 300, 200), outline=BLACK, width=2, fill=FILL1)
    d.rectangle((ox, 200, ox + 300, 230), outline=BLACK, width=2, fill=FILL2)
    # ナゲット（ソリッド・レンズ状）
    cx = ox + 150
    d.ellipse((cx - 30, 185, cx + 30, 215), outline=BLACK, width=3, fill=FILL3)
    ctext(d, cx, 200, "", FT)
    ctext(d, cx, 260, "溶融凝固部（ナゲット）", FT, RED)
    ctext(d, W / 2, 320, "ソリッド要素で立体的に表す", FS, BLUE)
    save(im, "v2f7Nugget")


def f_mesh_size():  # 29
    im, d = new(); title(d, "要素寸法の目安")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：音場（波長1/6以下）
    ox, oy = 90, 180
    pts = [(ox + 200 * i / 40, oy - 30 * math.sin(2 * math.pi * i / 40)) for i in range(41)]
    plot(d, 0, 0, pts, BLUE, 2)
    for i in range(7):
        x = ox + 200 * i / 6
        d.line((x, oy - 36, x, oy + 36), fill=GRAY, width=1)
    ctext(d, ox + 100, oy + 60, "音場：lambda/6 以下", FT, BLUE)
    # 右：構造（一定サイズ・小段差省略）
    ox2, oy2 = 380, 150
    cell = 40
    for i in range(3):
        for j in range(5):
            d.rectangle((ox2 + j * cell, oy2 + i * cell,
                         ox2 + (j + 1) * cell, oy2 + (i + 1) * cell), outline=LGRAY, width=1)
    ctext(d, ox2 + 100, oy2 + 145, "構造：一定サイズ", FT, GRAY)
    ctext(d, ox2 + 100, oy2 + 169, "小段差は省略", FT, RED)
    save(im, "v2f7MeshSize")


def f_moment_of_inertia():  # 30
    im, d = new(); title(d, "慣性モーメント（回転のしにくさ）")
    # 剛体部品と重心まわり回転
    cg = (300, 210)
    d.rectangle((cg[0] - 90, cg[1] - 45, cg[0] + 90, cg[1] + 45), outline=BLACK, width=3, fill=FILL1)
    node(d, cg[0], cg[1], 7, "white")
    ctext(d, cg[0], cg[1] - 62, "重心", FT, GRAY)
    curve_arrow(d, cg[0], cg[1], 70, 210, 330, GREEN, 2, 11)
    ctext(d, cg[0] - 100, cg[1] + 6, "回転", FT, GREEN)
    ctext(d, W / 2, 330, "並進の質量に対応する回転の慣性", FS, BLUE)
    ctext(d, W / 2, 372, "剛体部品は重心まわりに回転する", FT, GRAY)
    save(im, "v2f7MomentOfInertia")


if __name__ == "__main__":
    for fn in [f_rayleigh_damping, f_eta_zeta, f_quad_shape, f_tri_shape,
               f_acoustic_mesh, f_viscous_damping, f_hysteretic_damping,
               f_friction_damping, f_damping_ratio, f_loss_factor,
               f_proportional_damping, f_modal_orthogonality, f_shell_element,
               f_axisym_shell, f_plate_element, f_solid_element, f_beam_element,
               f_rod_element, f_rigid_element, f_spring_damper_element,
               f_lumped_mass, f_mass_element, f_mpc, f_shared_double_node,
               f_equiv_stiffness_density, f_added_mass, f_offset, f_nugget,
               f_mesh_size, f_moment_of_inertia]:
        fn()
    print("done 30")
