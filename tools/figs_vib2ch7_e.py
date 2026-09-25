# -*- coding: utf-8 -*-
"""振動2級 第7章「モデリングの基礎」の問題図（全19枚）。接頭辞 v2e7。
白地660×420・黒線画（figlib準拠）。
required問題図は答え・正解値・結論・正解の選択肢を描かない（与件・配置・記号のみ）。
文字化け回避のためギリシャ文字は綴り（zeta, eta, alpha, beta）で書く。上付きはB^T等。
実行: python tools/figs_vib2ch7_e.py
"""
import sys
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
import math
from figlib import (new, save, title, ctext, arrow, force, dim, hwall, wall,
                    spring, node, angle_arc, pin_support, roller_support, note,
                    matrix_grid, axes, plot, iso_box,
                    F, FL, FS, FT, BLACK, GRAY, LGRAY, RED, BLUE, GREEN, ORANGE,
                    FILL1, FILL2, FILL3, W, H)


# ---- 共通ヘルパ ----
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


def dashpot(d, x0, y, x1, side_h=16, col=BLACK):
    """水平ダッシュポット記号。x0(左取付)〜x1(右取付)。"""
    xm = (x0 + x1) / 2
    # 左ロッド
    d.line((x0, y, xm - 18, y), fill=col, width=3)
    # シリンダ（コの字・右開き）
    d.line((xm - 18, y - side_h, xm + 22, y - side_h), fill=col, width=3)
    d.line((xm - 18, y + side_h, xm + 22, y + side_h), fill=col, width=3)
    d.line((xm - 18, y - side_h, xm - 18, y + side_h), fill=col, width=3)
    # ピストン板＋右ロッド
    d.line((xm + 4, y - side_h + 4, xm + 4, y + side_h - 4), fill=col, width=4)
    d.line((xm + 4, y, x1, y), fill=col, width=3)


def rubber(d, cx, cy, w=30, h=22, col=BLACK):
    """ゴムマウント（ばね＋ダッシュポットの塊）を簡易ハッチ矩形で。"""
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=col, width=2, fill=FILL2)
    for i in range(-1, 2):
        d.line((cx + i * 9, cy - h / 2, cx + i * 9 - 6, cy + h / 2), fill=col, width=1)


# ============================================================
# 問題図 v2e7（19枚）
# ============================================================

def rayleigh_damping_curve(name):  # required
    im, d = new()
    title(d, "レイリー減衰：質量比例項＋剛性比例項の和")
    ox, oy = 110, 340
    axes(d, ox, oy, 460, 260, "振動数", "減衰比")
    # 質量比例項（低周波で大→減少）
    p1 = []
    for i in range(61):
        t = i / 60.0
        x = ox + 420 * t
        y = oy - 200 * (0.85 * math.exp(-3.2 * t) + 0.03)
        p1.append((x, y))
    plot(d, 0, 0, p1, GREEN, 2)
    ctext(d, ox + 150, oy - 150, "質量比例項（低周波で大）", FT, GREEN)
    # 剛性比例項（高周波で大→増加）
    p2 = []
    for i in range(61):
        t = i / 60.0
        x = ox + 420 * t
        y = oy - 200 * (0.9 * t + 0.02)
        p2.append((x, y))
    plot(d, 0, 0, p2, ORANGE, 2)
    ctext(d, ox + 300, oy - 60, "剛性比例項（高周波で大）", FT, ORANGE)
    # 和（U字）
    ps = []
    for i in range(61):
        t = i / 60.0
        x = ox + 420 * t
        y = oy - 200 * (0.85 * math.exp(-3.2 * t) + 0.9 * t + 0.05)
        ps.append((x, y))
    plot(d, 0, 0, ps, BLUE, 3)
    ctext(d, ox + 230, oy - 205, "和（U字）", FS, BLUE)
    save(im, name)


def damping_mechanisms(name):  # required
    im, d = new()
    title(d, "減衰の3機構：粘性・ヒステリシス・摩擦")
    d.line((225, 62, 225, 402), fill=LGRAY, width=1)
    d.line((445, 62, 445, 402), fill=LGRAY, width=1)
    # 粘性（ダッシュポット）
    dashpot(d, 40, 170, 195, 16)
    ctext(d, 115, 230, "粘性", FS)
    ctext(d, 115, 254, "(ダッシュポット)", FT, GRAY)
    # ヒステリシス（履歴ループ）
    ox, oy = 335, 175
    pts = []
    for i in range(61):
        th = 2 * math.pi * i / 60.0
        x = ox + 55 * math.cos(th)
        y = oy - 38 * math.sin(th) - 18 * math.cos(th)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 2)
    axes(d, ox - 75, oy + 55, 150, 120, "変位", "力", GRAY)
    ctext(d, 335, 254, "ヒステリシス", FS)
    ctext(d, 335, 278, "(履歴ループ)", FT, GRAY)
    # 摩擦（すべり）
    ox2 = 545
    hwall(d, ox2 - 60, ox2 + 55, 205, side=1, n=7)
    d.rectangle((ox2 - 45, 155, ox2 + 40, 205), outline=BLACK, width=3, fill=FILL1)
    arrow(d, ox2 + 40, 180, ox2 + 78, 180, RED, 3, 11)
    ctext(d, ox2, 254, "摩擦", FS)
    ctext(d, ox2, 278, "(すべり)", FT, GRAY)
    save(im, name)


def zeta_eta_relation(name):  # helpful
    im, d = new()
    title(d, "減衰比 zeta と損失係数 eta の比例関係")
    ox, oy = 130, 340
    axes(d, ox, oy, 420, 260, "zeta（減衰比）", "eta（損失係数）")
    # 直線 eta = 2 zeta（傾き2）
    x1 = ox + 380
    y1 = oy - 2 * 380 * (240 / 380) * 0.5  # 傾き調整
    pts = [(ox, oy), (ox + 380, oy - 230)]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + 300, oy - 190, "eta = 2 zeta", F, BLUE)
    # 補助点
    node(d, ox + 190, oy - 115, 4, RED)
    save(im, name)


def proportional_damping_ortho(name):  # required
    im, d = new()
    title(d, "比例減衰：モード座標で対角化される様子")
    # 物理座標（非対角あり）→ モード座標（対角）
    matrix_grid(d, 70, 150, [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]],
                cell=48, fnt=FS)
    ctext(d, 70 + 1.5 * 48, 150 + 3 * 48 + 22, "物理座標 [C]", FT, GRAY)
    arrow(d, 260, 246, 360, 246, BLUE, 3, 13)
    ctext(d, 310, 220, "モード変換", FT, BLUE)
    matrix_grid(d, 400, 150, [["c1", "0", "0"], ["0", "c2", "0"], ["0", "0", "c3"]],
                cell=48, fnt=FS)
    ctext(d, 400 + 1.5 * 48, 150 + 3 * 48 + 22, "モード座標（対角）", FT, GRAY)
    note(d, "各モードが独立に減衰する（連成しない）")
    save(im, name)


def containment_vessel(name):  # required
    im, d = new()
    title(d, "円筒形の原子炉格納容器（非対称な付属物）")
    cx = 300
    # 円筒胴
    d.rectangle((cx - 90, 150, cx + 90, 350), outline=BLACK, width=3, fill=FILL1)
    # 半球ドーム（上）
    d.arc((cx - 90, 90, cx + 90, 210), 180, 360, fill=BLACK, width=3)
    # 基礎
    hwall(d, cx - 120, cx + 120, 350, side=1, n=12)
    # 非対称付属物
    # エアロック（左）
    d.rectangle((cx - 130, 230, cx - 90, 280), outline=BLACK, width=2, fill=FILL2)
    ctext(d, cx - 160, 255, "エアロック", FT, GRAY, "rm")
    # クレーン（右上・アーム）
    d.line((cx + 90, 175, cx + 175, 175), fill=BLACK, width=3)
    d.line((cx + 175, 175, cx + 175, 205), fill=BLACK, width=2)
    ctext(d, cx + 180, 165, "クレーン", FT, GRAY, "lm")
    # 機器搬入口（右下）
    d.rectangle((cx + 90, 300, cx + 135, 340), outline=BLACK, width=2, fill=FILL2)
    ctext(d, cx + 175, 320, "機器搬入口", FT, GRAY, "lm")
    # 配管貫通部（左下・複数）
    for yy in (300, 325):
        d.line((cx - 90, yy, cx - 125, yy), fill=BLACK, width=3)
    ctext(d, cx - 130, 313, "配管貫通部", FT, GRAY, "rm")
    save(im, name)


def containment_axisym_ng(name):  # required
    im, d = new()
    title(d, "軸対称モデル と 実際の非対称配管貫通部の対比")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：軸対称（周方向均一）
    cx = 175
    d.rectangle((cx - 55, 130, cx + 55, 300), outline=BLACK, width=3, fill=FILL1)
    d.arc((cx - 55, 90, cx + 55, 170), 180, 360, fill=BLACK, width=3)
    dash(d, cx, 90, cx, 320, LGRAY)  # 対称軸
    ctext(d, cx, 330, "軸対称（周方向均一）", FT, GRAY)
    ctext(d, cx, 354, "付属物を表せない", FT, RED)
    # 右：実際（非対称貫通部）
    cx2 = 490
    d.rectangle((cx2 - 55, 130, cx2 + 55, 300), outline=BLACK, width=3, fill=FILL1)
    d.arc((cx2 - 55, 90, cx2 + 55, 170), 180, 360, fill=BLACK, width=3)
    # 非対称な貫通部
    for (yy, sgn) in [(200, -1), (255, -1), (170, 1)]:
        x0 = cx2 + sgn * 55
        d.line((x0, yy, x0 + sgn * 35, yy), fill=BLACK, width=3)
    ctext(d, cx2, 330, "実際（非対称な貫通部）", FT, GRAY)
    save(im, name)


def chassis_frame(name):  # required
    im, d = new()
    title(d, "箱型断面のシャシフレームと車体取付けゴムマウント")
    # ラダーフレーム（2本の縦メンバ＋クロスメンバ）
    x0, x1 = 90, 560
    yT, yB = 160, 250
    for y in (yT, yB):
        d.rectangle((x0, y - 10, x1, y + 10), outline=BLACK, width=2, fill=FILL1)
    for x in (150, 300, 450, 540):
        d.rectangle((x - 8, yT, x + 8, yB), outline=BLACK, width=2, fill=FILL2)
    ctext(d, 325, 130, "箱型断面のシャシフレーム", FT, GRAY)
    # ゴムマウント位置（車体取付け）
    for x in (150, 300, 450):
        rubber(d, x, yB + 40, 34, 24)
        ctext(d, x, yB + 72, "マウント", FT, GRAY)
    ctext(d, 325, 340, "ゴムマウント位置（車体へ取付け）", FT, GRAY)
    save(im, name)


def powerplant_mount(name):  # required
    im, d = new()
    title(d, "ゴムマウント支持のパワープラント（並進・回転）")
    # フレーム（下）
    hwall(d, 110, 550, 340, side=1, n=14)
    d.line((110, 340, 550, 340), fill=BLACK, width=3)
    # ゴムマウント3点
    for x in (180, 330, 480):
        rubber(d, x, 315, 30, 24)
    # パワープラント塊
    d.rectangle((170, 170, 490, 300), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 330, 210, "パワープラント", FS)
    # 重心
    cg = (330, 235)
    r = 11
    d.ellipse((cg[0] - r, cg[1] - r, cg[0] + r, cg[1] + r), outline=BLACK, width=2)
    d.pieslice((cg[0] - r, cg[1] - r, cg[0] + r, cg[1] + r), 0, 90, fill=BLACK)
    d.pieslice((cg[0] - r, cg[1] - r, cg[0] + r, cg[1] + r), 180, 270, fill=BLACK)
    ctext(d, cg[0] + 18, cg[1] - 16, "重心", FT, GRAY, "lm")
    # 並進
    arrow(d, cg[0], cg[1], cg[0] + 60, cg[1], RED, 3, 12)
    ctext(d, cg[0] + 66, cg[1] - 14, "並進", FT, RED, "lm")
    # 回転
    curve_arrow(d, cg[0], cg[1], 44, 210, 330, GREEN, 2, 10)
    ctext(d, cg[0] - 60, cg[1] + 6, "回転", FT, GREEN)
    save(im, name)


def hatchback_backdoor(name):  # required
    im, d = new()
    title(d, "ハッチバックのバックドア（正面図）")
    ox, oy = 200, 100
    w, h = 260, 250
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + w / 2, oy - 4, "鋼板（プレス成形）", FT, GRAY, "mb")
    # ガラス（上部）
    d.rectangle((ox + 30, oy + 25, ox + w - 30, oy + 120), outline=BLACK, width=2, fill=FILL3)
    ctext(d, ox + w / 2, oy + 72, "ガラス", FS, GRAY)
    # ワイパ
    d.line((ox + 60, oy + 115, ox + 150, oy + 60), fill=BLACK, width=3)
    ctext(d, ox + 95, oy + 135, "ワイパ", FT, GRAY)
    # ロック（下部中央）
    d.rectangle((ox + w / 2 - 18, oy + h - 40, ox + w / 2 + 18, oy + h - 10),
                outline=BLACK, width=2, fill=FILL2)
    ctext(d, ox + w / 2, oy + h - 25, "ロック", FT, GRAY)
    # 板厚注記
    ctext(d, ox + w + 20, oy + 180, "板厚 t（薄板）", FT, RED, "lm")
    arrow(d, ox + w + 18, oy + 178, ox + w - 4, oy + 178, RED, 2, 9)
    save(im, name)


def radiator_support(name):  # required
    im, d = new()
    title(d, "ラジエータ：上下各2箇所のゴムクッション支持")
    ox, oy = 210, 130
    w, h = 240, 180
    # ラジサポ枠
    dashrect(d, ox - 40, oy - 40, ox + w + 40, oy + h + 40, GRAY, 2)
    ctext(d, ox + w / 2, oy - 55, "ラジエータサポート", FT, GRAY)
    # ラジエータ本体（コア・格子）
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    for i in range(1, 8):
        d.line((ox + i * w / 8, oy, ox + i * w / 8, oy + h), fill=LGRAY, width=1)
    ctext(d, ox + w / 2, oy + h / 2 - 40, "ラジエータ", FS)
    # 上2・下2 ゴムクッション
    for x in (ox + 50, ox + w - 50):
        rubber(d, x, oy - 20, 26, 20)
        rubber(d, x, oy + h + 20, 26, 20)
    ctext(d, ox + w + 60, oy - 20, "上2箇所", FT, GRAY, "lm")
    ctext(d, ox + w + 60, oy + h + 20, "下2箇所", FT, GRAY, "lm")
    # 重心
    cg = (ox + w / 2, oy + h / 2)
    node(d, cg[0], cg[1], 8, "white")
    ctext(d, cg[0], cg[1] + 24, "重心", FT, GRAY)
    save(im, name)


def excavator_arm(name):  # required
    im, d = new()
    title(d, "油圧ショベルの作業機（ブーム・アーム・バケット）")
    # 座標系
    axes(d, 70, 380, 90, 70, "x", "y", GRAY)
    # 旋回中心（車体側）
    base = (140, 320)
    node(d, base[0], base[1], 7, FILL2)
    # ブーム
    bt = (300, 170)
    d.line((base[0], base[1], bt[0], bt[1]), fill=BLACK, width=8)
    ctext(d, 210, 230, "ブーム", FT, GRAY)
    # アーム
    at = (430, 250)
    d.line((bt[0], bt[1], at[0], at[1]), fill=BLACK, width=7)
    ctext(d, 380, 195, "アーム", FT, GRAY)
    # バケット
    bk = [(at[0], at[1]), (at[0] + 55, at[1] + 30), (at[0] + 30, at[1] + 70),
          (at[0] - 10, at[1] + 55)]
    d.polygon(bk, outline=BLACK, width=3, fill=FILL1)
    ctext(d, at[0] + 40, at[1] + 92, "バケット", FT, GRAY)
    # 油圧シリンダ3本
    dashpot(d, base[0] + 20, 265, 260, 12)
    ctext(d, 190, 285, "シリンダ1", FT, BLUE)
    dashpot(d, bt[0] - 10, 195, at[0] - 30, 10)
    ctext(d, 360, 165, "シリンダ2", FT, BLUE)
    d.line((at[0] - 5, at[1] - 10, at[0] + 25, at[1] + 20), fill=BLUE, width=3)
    ctext(d, at[0] + 60, at[1] + 5, "シリンダ3", FT, BLUE, "lm")
    # バケットリンク
    d.line((at[0] + 25, at[1] + 20, bk[1][0], bk[1][1]), fill=GRAY, width=2)
    ctext(d, at[0] + 55, at[1] + 35, "リンク", FT, GRAY, "lm")
    save(im, name)


def rail_control_box(name):  # required
    im, d = new()
    title(d, "車体下部にビームを介しぶら下がる制御箱（側面）")
    # 車体床（上・水平面）
    hwall(d, 90, 570, 130, side=-1, n=15)
    ctext(d, 330, 110, "鉄道車両 車体下部", FT, GRAY)
    # 取付けビーム（左右2本の吊り）
    for x in (220, 440):
        d.line((x, 130, x, 210), fill=BLACK, width=5)
    ctext(d, 330, 175, "取付け部（ビーム）", FT, GRAY)
    # 制御箱
    ox, oy = 180, 210
    w, h = 300, 150
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + w / 2, oy - 4, "制御箱", FS, GRAY, "mb")
    # 内部の複数電子機器
    for (rx, ry, rw, rh) in [(30, 25, 70, 45), (120, 25, 70, 45),
                             (210, 25, 60, 45), (30, 85, 110, 45),
                             (160, 85, 110, 45)]:
        d.rectangle((ox + rx, oy + ry, ox + rx + rw, oy + ry + rh),
                    outline=GRAY, width=2, fill=FILL3)
    ctext(d, ox + w / 2, oy + h + 20, "内部に複数の電子機器", FT, GRAY)
    save(im, name)


def screw_compressor_shaft(name):  # required
    im, d = new()
    title(d, "スクリュ式空気圧縮機の断面（オス・メスロータ）")
    # ケーシング（2円の重なり）
    c1 = (270, 240)
    c2 = (400, 240)
    r1, r2 = 90, 70
    d.ellipse((c1[0] - r1, c1[1] - r1, c1[0] + r1, c1[1] + r1), outline=BLACK, width=3)
    d.ellipse((c2[0] - r2, c2[1] - r2, c2[0] + r2, c2[1] + r2), outline=BLACK, width=3)
    # オスロータ（凸ローブ）
    for a in range(0, 360, 90):
        ax = c1[0] + (r1 - 20) * math.cos(math.radians(a))
        ay = c1[1] - (r1 - 20) * math.sin(math.radians(a))
        d.ellipse((ax - 14, ay - 14, ax + 14, ay + 14), outline=GRAY, width=2, fill=FILL2)
    node(d, c1[0], c1[1], 6, "white")
    ctext(d, c1[0], c1[1] + 30, "オスロータ", FT, GRAY)
    # メスロータ（凹溝）
    for a in range(45, 360, 72):
        ax = c2[0] + (r2 - 14) * math.cos(math.radians(a))
        ay = c2[1] - (r2 - 14) * math.sin(math.radians(a))
        d.line((c2[0], c2[1], ax, ay), fill=GRAY, width=2)
    node(d, c2[0], c2[1], 6, "white")
    ctext(d, c2[0] + 20, c2[1] + 40, "メスロータ", FT, GRAY, "lm")
    # 軸中心の節点
    ctext(d, c1[0], c1[1] - 24, "軸中心の節点", FT, RED)
    # 吸込・吐出口
    arrow(d, 150, 200, 185, 210, BLUE, 3, 11)
    ctext(d, 120, 190, "吸込口", FT, BLUE, "mm")
    arrow(d, 470, 270, 505, 280, BLUE, 3, 11)
    ctext(d, 520, 290, "吐出口", FT, BLUE, "lm")
    save(im, name)


def rail_car_body(name):  # required
    im, d = new()
    title(d, "鉄道車両の車体外観（側板・窓・付加質量部）")
    # 車体箱
    ox, oy = 90, 130
    w, h = 480, 150
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + w / 2, oy - 4, "側板（薄板）", FT, GRAY, "mb")
    # 窓
    for i in range(4):
        wx = ox + 40 + i * 110
        d.rectangle((wx, oy + 30, wx + 70, oy + 80), outline=BLACK, width=2, fill=FILL3)
    ctext(d, ox + 40 + 35, oy + 55, "窓", FT, GRAY)
    # リブ（縦補強）
    for i in range(1, 5):
        rx = ox + i * w / 5
        d.line((rx, oy + 95, rx, oy + h), fill=GRAY, width=2)
    ctext(d, ox + w / 2, oy + h - 12, "リブ", FT, GRAY)
    # 腰掛・化粧板（付加質量）
    d.rectangle((ox + 20, oy + h - 22, ox + w - 20, oy + h), outline=BLACK, width=1, fill=FILL2)
    ctext(d, ox + w + 8, oy + h - 10, "腰掛・化粧板（付加質量）", FT, GRAY, "lm")
    # 台車
    for x in (ox + 90, ox + w - 90):
        d.rectangle((x - 45, oy + h + 20, x + 45, oy + h + 55), outline=BLACK, width=2, fill=FILL2)
        for cx in (x - 28, x + 28):
            d.ellipse((cx - 14, oy + h + 55, cx + 14, oy + h + 83), outline=BLACK, width=2)
    ctext(d, ox + 90, oy + h + 100, "台車", FT, GRAY)
    # 床下機器
    d.rectangle((ox + 200, oy + h + 25, ox + 280, oy + h + 55), outline=GRAY, width=2, fill=FILL3)
    ctext(d, ox + 320, oy + h + 40, "床下機器", FT, GRAY, "lm")
    save(im, name)


def car_body_acoustic(name):  # required
    im, d = new()
    title(d, "乗用車ボディシェルと車室内音場（構造・音響連成）")
    # ボディシェルの輪郭（乗用車側面）
    body = [(110, 300), (150, 220), (230, 190), (280, 130), (430, 130),
            (470, 200), (560, 220), (560, 300)]
    d.line(body + [body[0]], fill=BLACK, width=3, joint="curve")
    ctext(d, 335, 108, "ボディシェル（鈑金＝板要素）", FT, GRAY)
    # 板要素（鈑金）の分割線
    for x in (200, 290, 380, 470):
        d.line((x, 150, x, 200), fill=LGRAY, width=1)
    # 骨格はり要素（ピラー）
    for (x0, y0, x1, y1) in [(230, 190, 285, 135), (430, 132, 468, 198)]:
        d.line((x0, y0, x1, y1), fill=BLUE, width=5)
    ctext(d, 250, 165, "骨格はり要素", FT, BLUE, "mm")
    # 車室内音場
    ctext(d, 340, 245, "車室内 音場", FS, RED)
    for (wx, wy) in [(300, 260), (380, 260)]:
        for k in range(3):
            d.arc((wx - 12 - k * 10, wy - 12 - k * 10, wx + 12 + k * 10, wy + 12 + k * 10),
                  200, 340, fill=RED, width=1)
    ctext(d, 335, 300, "構造の振動と音場が連成", FT, GRAY)
    save(im, name)


def spot_weld_bolt(name):  # required
    im, d = new()
    title(d, "スポット溶接部：共有節点結合 と ソリッド＋多点拘束")
    d.line((330, 62, 330, 402), fill=LGRAY, width=2)
    # 左：共有節点結合
    ox = 100
    d.rectangle((ox, 150, ox + 160, 175), outline=BLACK, width=2, fill=FILL1)
    d.rectangle((ox, 175, ox + 160, 200), outline=BLACK, width=2, fill=FILL2)
    node(d, ox + 80, 175, 8, RED)
    ctext(d, ox + 80, 230, "共有節点結合", FT)
    ctext(d, ox + 80, 254, "（節点1個を共有）", FT, GRAY)
    # 右：ソリッド＋多点拘束（ナゲット）
    ox2 = 400
    d.rectangle((ox2, 150, ox2 + 160, 175), outline=BLACK, width=2, fill=FILL1)
    d.rectangle((ox2, 185, ox2 + 160, 210), outline=BLACK, width=2, fill=FILL2)
    # ナゲット（ソリッド）
    d.rectangle((ox2 + 65, 172, ox2 + 95, 188), outline=BLACK, width=2, fill=FILL3)
    ctext(d, ox2 + 80, 180, "", FT)
    # MPCの拘束線
    for dx in (-30, 30):
        dash(d, ox2 + 80, 175, ox2 + 80 + dx, 168, RED, 2)
        dash(d, ox2 + 80, 185, ox2 + 80 + dx, 192, RED, 2)
    ctext(d, ox2 + 80, 230, "ソリッド＋多点拘束", FT)
    ctext(d, ox2 + 80, 254, "（ナゲットを立体表現）", FT, GRAY)
    # ボルト部接触範囲
    d.rectangle((150, 320, 510, 375), outline=GRAY, width=1, fill=FILL1)
    d.ellipse((300, 330, 360, 365), outline=RED, width=2)
    ctext(d, 330, 347, "ボルト部の接触範囲", FT, RED)
    save(im, name)


def damping_material_mesh(name):  # required
    im, d = new()
    title(d, "制振材の二重要素（上）と音場の1波長分割（下）")
    # 上：鈑金＋制振材の二重要素＋オフセット断面
    ox, oy = 120, 120
    w = 420
    # 鈑金
    d.rectangle((ox, oy, ox + w, oy + 22), outline=BLACK, width=2, fill=FILL1)
    ctext(d, ox - 8, oy + 11, "鈑金", FT, GRAY, "rm")
    # 制振材
    d.rectangle((ox, oy + 22, ox + w, oy + 48), outline=BLACK, width=2, fill=FILL3)
    ctext(d, ox - 8, oy + 35, "制振材", FT, GRAY, "rm")
    # 節点位置（各中心面）とオフセット
    dash(d, ox, oy + 11, ox + w, oy + 11, BLUE, 1)
    dash(d, ox, oy + 35, ox + w, oy + 35, GREEN, 1)
    arrow(d, ox + w + 14, oy + 11, ox + w + 14, oy + 35, RED, 2, 8)
    ctext(d, ox + w + 20, oy + 23, "オフセット", FT, RED, "lm")
    # 下：音場の正弦波1波長を複数要素で分割
    ox2, oy2 = 120, 300
    w2 = 420
    pts = []
    for i in range(81):
        t = i / 80.0
        x = ox2 + w2 * t
        y = oy2 - 40 * math.sin(2 * math.pi * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 2)
    d.line((ox2, oy2, ox2 + w2, oy2), fill=LGRAY, width=1)
    # 分割（6要素）
    for i in range(7):
        x = ox2 + w2 * i / 6
        d.line((x, oy2 - 46, x, oy2 + 46), fill=GRAY, width=1)
        node(d, x, oy2, 3, "white")
    dim(d, ox2, oy2 + 60, ox2 + w2, oy2 + 60, "1波長 lambda", col=GRAY)
    ctext(d, ox2 + w2 / 2, oy2 - 62, "1波長を複数要素で分割", FT, GRAY)
    save(im, name)


def door_hinge(name):  # required
    im, d = new()
    title(d, "ドアヒンジ構造とFEMモデル化（ピン軸まわり回転）")
    # 座標系
    axes(d, 70, 380, 80, 60, "x", "y", GRAY)
    # ボディ側ブラケット
    d.polygon([(180, 150), (240, 150), (240, 300), (180, 300)],
              outline=BLACK, width=3, fill=FILL2)
    ctext(d, 210, 320, "ボディ側ブラケット", FT, GRAY)
    # ドア側ブラケット
    d.polygon([(360, 170), (500, 170), (500, 280), (360, 280)],
              outline=BLACK, width=3, fill=FILL1)
    ctext(d, 430, 300, "ドア側ブラケット", FT, GRAY)
    # 上下の腕（ヒンジ）
    d.rectangle((240, 175, 360, 195), outline=BLACK, width=2, fill=FILL3)
    d.rectangle((240, 255, 360, 275), outline=BLACK, width=2, fill=FILL3)
    # ピン
    d.line((300, 160, 300, 290), fill=BLUE, width=5)
    ctext(d, 300, 145, "ピン", FT, BLUE)
    # A点・B点
    node(d, 300, 185, 7, "white")
    ctext(d, 275, 185, "A点", FT, RED, "rm")
    node(d, 300, 265, 7, "white")
    ctext(d, 275, 265, "B点", FT, RED, "rm")
    # ピン軸まわり回転
    curve_arrow(d, 430, 225, 40, 300, 60, GREEN, 2, 10)
    ctext(d, 500, 225, "ピン軸回転", FT, GREEN, "lm")
    save(im, name)


def step_mesh_uniform(name):  # required
    im, d = new()
    title(d, "メッシュより小さい段差部と周辺の一定サイズメッシュ")
    # 断面（段差）
    ox, oy = 120, 150
    # 部材外形：わずかな段差
    prof = [(ox, oy + 120), (ox, oy + 40), (ox + 180, oy + 40),
            (ox + 180, oy + 30), (ox + 200, oy + 30), (ox + 200, oy + 40),
            (ox + 420, oy + 40), (ox + 420, oy + 120)]
    d.line(prof, fill=BLACK, width=3)
    # 微小段差を拡大注記
    dashrect(d, ox + 170, oy + 22, ox + 210, oy + 48, RED, 2)
    ctext(d, ox + 190, oy + 8, "微小段差・ビードは省略", FT, RED)
    # 一定サイズメッシュで覆う
    cell = 40
    for i in range(0, 3):
        for j in range(0, 11):
            x = ox + j * cell
            y = oy + 40 + i * cell
            if x <= ox + 420:
                d.rectangle((x, y, x + cell, y + cell), outline=LGRAY, width=1)
    ctext(d, ox + 210, oy + 190, "周辺を一定サイズのメッシュで覆う", FT, GRAY)
    save(im, name)


if __name__ == "__main__":
    rayleigh_damping_curve("v2e7RayleighDampingCurve")
    damping_mechanisms("v2e7DampingMechanisms")
    zeta_eta_relation("v2e7ZetaEtaRelation")
    proportional_damping_ortho("v2e7ProportionalDampingOrtho")
    containment_vessel("v2e7ContainmentVessel")
    containment_axisym_ng("v2e7ContainmentAxisymNG")
    chassis_frame("v2e7ChassisFrame")
    powerplant_mount("v2e7PowerplantMount")
    hatchback_backdoor("v2e7HatchbackBackdoor")
    radiator_support("v2e7RadiatorSupport")
    excavator_arm("v2e7ExcavatorArm")
    rail_control_box("v2e7RailControlBox")
    screw_compressor_shaft("v2e7ScrewCompressorShaft")
    rail_car_body("v2e7RailCarBody")
    car_body_acoustic("v2e7CarBodyAcoustic")
    spot_weld_bolt("v2e7SpotWeldBolt")
    damping_material_mesh("v2e7DampingMaterialMesh")
    door_hinge("v2e7DoorHinge")
    step_mesh_uniform("v2e7StepMeshUniform")
    print("done 19")
