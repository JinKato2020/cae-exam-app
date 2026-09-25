# -*- coding: utf-8 -*-
"""振動2級 第8章「境界条件および荷重条件」の問題図（全21枚）。接頭辞 v2e8。
白地660×420・黒線画（figlib準拠）。
required問題図は答え・正解値・結論・正解の選択肢を描かない（与件・配置・記号のみ）。
helpful問題図は回答後なので結論を描いてよい。
文字化け回避のためギリシャ文字は綴り（lambda, omega, theta, zeta）で書く。上付きはomega^2等。
実行: python tools/figs_vib2ch8_e.py
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


def dashrect(d, x0, y0, x1, y1, col=RED, wd=2):
    dash(d, x0, y0, x1, y0, col, wd)
    dash(d, x1, y0, x1, y1, col, wd)
    dash(d, x1, y1, x0, y1, col, wd)
    dash(d, x0, y1, x0, y0, col, wd)


def curve_arrow(d, cx, cy, r, a0, a1, col=BLUE, wd=3, head=12):
    d.arc((cx - r, cy - r, cx + r, cy + r), -a1, -a0, fill=col, width=wd)
    A = math.radians(a1)
    ex, ey = cx + r * math.cos(A), cy - r * math.sin(A)
    ang = math.atan2(-math.cos(A), -math.sin(A))
    for s in (0.5, -0.5):
        d.line((ex, ey, ex - head * math.cos(ang - s), ey - head * math.sin(ang - s)),
               fill=col, width=wd)


def rubber(d, cx, cy, w=30, h=22, col=BLACK):
    """ゴムマウント/クッションを簡易ハッチ矩形で。"""
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=col, width=2, fill=FILL2)
    for i in range(-1, 2):
        d.line((cx + i * 9, cy - h / 2, cx + i * 9 - 6, cy + h / 2), fill=col, width=1)


def triad(d, ox, oy, s=44, rot=False, col=BLACK):
    """簡易3D座標系(x右・y上・z奥)。rot=Trueで各軸まわり回転 theta を添える。"""
    # x（右）
    arrow(d, ox, oy, ox + s, oy, col, 2, 10)
    ctext(d, ox + s + 12, oy, "X", FT, col, "lm")
    # y（上）
    arrow(d, ox, oy, ox, oy - s, col, 2, 10)
    ctext(d, ox, oy - s - 12, "Y", FT, col, "mm")
    # z（奥・左下方向）
    zx, zy = ox - int(s * 0.6), oy + int(s * 0.55)
    arrow(d, ox, oy, zx, zy, col, 2, 10)
    ctext(d, zx - 10, zy + 6, "Z", FT, col, "mm")
    if rot:
        ctext(d, ox, zy + 26, "各軸回転 theta_X,Y,Z", FT, GRAY, "mm")


# ============================================================
# 問題図 v2e8（21枚）
# ============================================================

def quad_pressure_nodes(name):  # 8-1 required
    im, d = new()
    title(d, "四角形1次要素への一様面圧（上から見た図）")
    x0, y0, x1, y1 = 250, 160, 450, 360
    # 圧力 p を表す下向き矢印を面上に並べる
    for gx in (x0 + 30, (x0 + x1) / 2, x1 - 30):
        for gy in (y0 + 30, (y0 + y1) / 2, y1 - 30):
            arrow(d, gx, gy - 30, gx, gy + 6, BLUE, 2, 8)
    # 要素
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=None)
    ctext(d, (x0 + x1) / 2, (y0 + y1) / 2, "一様圧力 p", FS, BLUE)
    # 節点1〜4（四隅）
    node(d, x0, y0, 8, "white"); ctext(d, x0 - 16, y0 - 16, "1", FT, RED)
    node(d, x1, y0, 8, "white"); ctext(d, x1 + 16, y0 - 16, "2", FT, RED)
    node(d, x1, y1, 8, "white"); ctext(d, x1 + 16, y1 + 16, "3", FT, RED)
    node(d, x0, y1, 8, "white"); ctext(d, x0 - 16, y1 + 16, "4", FT, RED)
    # 寸法 一辺2m
    dim(d, x0, y1 + 34, x1, y1 + 34, "一辺 2 m", col=GRAY)
    dim(d, x1 + 46, y0, x1 + 46, y1, "2 m", col=GRAY)
    save(im, name)


def tri_split_nodes(name):  # 8-2 helpful
    im, d = new()
    title(d, "正方形を対角線で2つの三角形1次要素に分割")
    x0, y0, x1, y1 = 200, 130, 440, 370
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    # 対角線（左上→右下）
    d.line((x0, y0, x1, y1), fill=BLACK, width=3)
    ctext(d, x0 + 70, y0 + 150, "要素I", FT, GRAY)
    ctext(d, x0 + 165, y0 + 80, "要素II", FT, GRAY)
    # 単独の角節点（右上・左下）＝ F_a
    node(d, x1, y0, 8, "white"); ctext(d, x1 + 20, y0 - 6, "F_a", FS, RED, "lm")
    node(d, x0, y1, 8, "white"); ctext(d, x0 - 20, y1 + 6, "F_a", FS, RED, "rm")
    # 対角線上の共有節点（左上・右下）＝ F_b（両三角形が共有）
    node(d, x0, y0, 8, FILL3); ctext(d, x0 - 20, y0 - 6, "F_b", FS, BLUE, "rm")
    node(d, x1, y1, 8, FILL3); ctext(d, x1 + 20, y1 + 6, "F_b", FS, BLUE, "lm")
    ctext(d, (x0 + x1) / 2, y1 + 34, "F_a=単独節点 / F_b=対角線上の共有節点", FT, GRAY)
    # 一辺
    dim(d, x0, y0 - 22, x1, y0 - 22, "一辺 1.5 m", col=GRAY)
    save(im, name)


def simple_support_beam(name):  # 8-3 required
    im, d = new()
    title(d, "はりの単純支持（各節点：横変位 w と傾き w'）")
    bx0, bx1, by = 130, 540, 210
    # はり
    d.rectangle((bx0, by - 8, bx1, by + 8), outline=BLACK, width=3, fill=FILL1)
    # 節点
    xs = [bx0, 235, 335, 440, bx1]
    labels = ["1", "2", "3", "n", "n+1"]
    for x, lb in zip(xs, labels):
        node(d, x, by, 6, "white")
        ctext(d, x, by - 26, lb, FT, GRAY)
    # 両端の単純支持（左=ピン、右=ローラ）
    pin_support(d, bx0, by + 8)
    roller_support(d, bx1, by + 8)
    ctext(d, bx0, by + 70, "ピン支持", FT, GRAY)
    ctext(d, bx1, by + 70, "ローラ支持", FT, GRAY)
    # 代表節点(節点2)で自由度を図示：横変位wと傾きw'
    xr = 335
    arrow(d, xr + 60, by, xr + 60, by - 48, RED, 3, 12)
    ctext(d, xr + 78, by - 40, "w（横変位）", FT, RED, "lm")
    curve_arrow(d, xr, by, 40, 20, 90, GREEN, 2, 10)
    ctext(d, xr + 46, by + 30, "w'（傾き）", FT, GREEN, "lm")
    save(im, name)


def sym_plane_lpart(name):  # 8-4 required
    im, d = new()
    title(d, "L型部品の1/2モデル（XZ 面で対称切断）")
    # L型部品（アイソメ風）
    ox, oy = 170, 150
    # 縦壁
    d.polygon([(ox, oy), (ox + 60, oy), (ox + 60, oy + 170), (ox, oy + 170)],
              outline=BLACK, width=3, fill=FILL1)
    # 底板
    d.polygon([(ox, oy + 130), (ox + 200, oy + 130), (ox + 200, oy + 170),
               (ox, oy + 170)], outline=BLACK, width=3, fill=FILL2)
    ctext(d, ox + 130, oy + 30, "L型部品（1/2）", FT, GRAY)
    # 背面固定（縦壁の左面をハッチ壁）
    wall(d, ox - 4, oy, oy + 170, side=-1, n=9)
    ctext(d, ox - 40, oy + 190, "背面 完全固定", FT, GRAY, "mm")
    # 対称面 XZ をハッチングで示す（切断面＝底面レベルの薄い面）
    sx0, sx1, sy = ox, ox + 200, oy + 170
    for i in range(9):
        xx = sx0 + i * (sx1 - sx0) / 9
        d.line((xx, sy, xx + 12, sy + 18), fill=BLUE, width=1)
    dash(d, sx0, sy, sx1, sy, BLUE, 2)
    ctext(d, sx1 + 10, sy + 4, "対称面 XZ", FT, BLUE, "lm")
    # 荷重稜線（薄く）
    dash(d, ox + 60, oy, ox + 60, oy + 130, GRAY, 2)
    arrow(d, ox + 90, oy + 20, ox + 62, oy + 20, RED, 2, 9)
    ctext(d, ox + 130, oy + 12, "荷重稜線", FT, RED, "lm")
    # 座標系（回転theta付き）
    triad(d, 540, 330, 40, rot=True)
    save(im, name)


def hex_mirror(name):  # 8-5 required
    im, d = new()
    title(d, "六面体の1/2モデル（x 軸に垂直な対称面）")
    # 片側の直方体（アイソメ）
    iso_box(d, 210, 200, 200, 120, 70)
    ctext(d, 320, 300, "六面体（片側モデル）", FT, GRAY)
    # 切断面（前面）をハッチ＝対称面
    x0, y0, x1, y1 = 210, 200, 410, 320
    for i in range(9):
        yy = y0 + i * (y1 - y0) / 9
        d.line((x0, yy, x0 + 12, yy + 10), fill=BLUE, width=1)
    ctext(d, x0 - 10, y0 - 6, "対称面", FT, BLUE, "rm")
    ctext(d, x0 - 10, y0 + 12, "(x軸に垂直)", FT, BLUE, "rm")
    # 対称面上のノード（丸）
    for (nx, ny) in [(x0, y0 + 30), (x0, y0 + 90), (x0 + 60, y0), (x0 + 140, y0)]:
        node(d, nx, ny, 6, "white")
    ctext(d, 300, 345, "○＝対称面上のノード（6自由度）", FT, GRAY)
    # 座標系（回転付き）
    triad(d, 555, 150, 40, rot=True)
    save(im, name)


def vessel_embed(name):  # 8-6 required
    im, d = new()
    title(d, "下部がコンクリートに埋め込まれた軸対称構造物（断面）")
    cx = 300
    # 地面
    gy = 300
    hwall(d, 120, 520, gy, side=1, n=13)
    ctext(d, 470, gy - 12, "地面", FT, GRAY, "lm")
    # 縦長構造物
    d.rectangle((cx - 45, 90, cx + 45, 360), outline=BLACK, width=3, fill=FILL1)
    d.line((cx, 90, cx, 360), fill=LGRAY, width=1)  # 対称軸
    ctext(d, cx, 70, "軸対称構造物", FT, GRAY)
    # コンクリート基礎（埋め込み部）
    d.rectangle((cx - 110, gy, cx + 110, 385), outline=BLACK, width=2, fill=FILL3)
    for i in range(9):
        xx = cx - 110 + i * 220 / 9
        d.line((xx, gy, xx + 10, gy + 12), fill=GRAY, width=1)
    ctext(d, cx + 150, 345, "コンクリート基礎", FT, GRAY, "lm")
    ctext(d, cx, 375, "埋め込み部（ほぼ変形しない）", FT, GRAY)
    # 地面との接地位置に破線＋「モデル境界?」
    dash(d, cx - 130, gy, cx + 130, gy, RED, 2)
    ctext(d, cx - 135, gy - 16, "モデル境界 ?", FT, RED, "rm")
    save(im, name)


def large_mass(name):  # 8-7 required
    im, d = new()
    title(d, "大質量法：支持点に剛体要素で結合した大質量 M")
    # 構造物
    d.rectangle((110, 130, 300, 300), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 205, 200, "解析対象構造物", FS, GRAY)
    # 支持点（結合点）
    cp = (300, 250)
    node(d, cp[0], cp[1], 7, "white")
    ctext(d, cp[0], cp[1] + 24, "結合点", FT, GRAY)
    # 剛体要素
    d.line((cp[0], cp[1], 420, 250), fill=BLUE, width=4)
    ctext(d, 360, 232, "剛体要素", FT, BLUE)
    # 大質量 M
    d.rectangle((420, 200, 540, 300), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 480, 250, "大質量 M", FS)
    # 入力矢印（Mへ）
    arrow(d, 480, 160, 480, 198, RED, 4, 14)
    ctext(d, 480, 145, "入力", FT, RED)
    # 結合点に生じる加速度 a
    arrow(d, cp[0] - 6, cp[1] - 40, cp[0] - 6, cp[1] - 6, GREEN, 3, 12)
    ctext(d, cp[0] - 24, cp[1] - 44, "加速度 a", FT, GREEN, "rm")
    # 関係式
    ctext(d, 330, 360, "F = M a", F, GRAY)
    save(im, name)


def rough_road(name):  # 8-8 required
    im, d = new()
    title(d, "凹凸路面（波長 lambda）を車速 V で走行")
    # 路面プロファイル（正弦波）
    ox, oy, w = 80, 320, 500
    amp, waves = 22, 5
    pts = []
    for i in range(201):
        t = i / 200.0
        x = ox + w * t
        y = oy - amp * math.sin(2 * math.pi * waves * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLACK, 3)
    # 地の下側ハッチ
    for i in range(0, 25):
        xx = ox + i * w / 25
        d.line((xx, oy + amp + 6, xx + 10, oy + amp + 18), fill=GRAY, width=1)
    # 波長 lambda（1周期分）
    x_a = ox + w * (0.25 / waves) * 0 + ox * 0  # 使わない
    px0 = ox + w * (0.5 / waves)
    px1 = px0 + w / waves
    dim(d, px0, oy - 55, px1, oy - 55, "波長 lambda", col=BLUE)
    # 車（簡易ボディ＋2輪）
    bx = ox + 300
    d.rectangle((bx, oy - 90, bx + 120, oy - 45), outline=BLACK, width=3, fill=FILL1)
    d.polygon([(bx + 20, oy - 90), (bx + 45, oy - 112), (bx + 95, oy - 112),
               (bx + 110, oy - 90)], outline=BLACK, width=3, fill=FILL3)
    for wx in (bx + 25, bx + 95):
        d.ellipse((wx - 16, oy - 55, wx + 16, oy - 23), outline=BLACK, width=3, fill=FILL2)
    # 車速 V
    arrow(d, bx + 130, oy - 70, bx + 185, oy - 70, RED, 4, 14)
    ctext(d, bx + 160, oy - 88, "車速 V", FT, RED)
    # 関係式
    ctext(d, 330, 385, "加振周波数 f = V / lambda", FS, GRAY)
    save(im, name)


def backdoor_ws(name):  # 8-9 required
    im, d = new()
    title(d, "自動車バックドア（正面）とウェザーストリップ")
    ox, oy = 200, 90
    w, h = 260, 250
    # ドア外形
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    # ガラス
    d.rectangle((ox + 28, oy + 22, ox + w - 28, oy + 110), outline=BLACK, width=2, fill=FILL3)
    ctext(d, ox + w / 2, oy + 66, "ガラス", FT, GRAY)
    # 全周ウェザーストリップ（接触線＝内側の破線枠）
    dashrect(d, ox + 10, oy + 10, ox + w - 10, oy + h - 10, GREEN, 2)
    ctext(d, ox + w / 2, oy + h + 18, "全周ウェザーストリップ（W/S）接触線", FT, GREEN)
    # 上端ヒンジ2個
    for hx in (ox + 60, ox + w - 60):
        d.rectangle((hx - 16, oy - 14, hx + 16, oy + 2), outline=BLACK, width=2, fill=FILL2)
    ctext(d, ox + w / 2, oy - 24, "上端ヒンジ 2個", FT, GRAY)
    # ロック（下部中央）
    d.rectangle((ox + w / 2 - 18, oy + h - 34, ox + w / 2 + 18, oy + h - 6),
                outline=BLACK, width=2, fill=FILL2)
    ctext(d, ox + w / 2, oy + h - 20, "ロック", FT, GRAY)
    save(im, name)


def radiator_support(name):  # 8-10 required
    im, d = new()
    title(d, "ラジエータ→ゴムクッション→ラジサポ→サイドメンバ（直列）")
    # ラジエータ本体
    d.rectangle((70, 150, 200, 300), outline=BLACK, width=3, fill=FILL1)
    for i in range(1, 5):
        d.line((70 + i * 26, 150, 70 + i * 26, 300), fill=LGRAY, width=1)
    ctext(d, 135, 320, "ラジエータ本体", FT, GRAY)
    # ゴムクッション（ばね＋減衰＝rubber）
    rubber(d, 250, 225, 44, 34)
    ctext(d, 250, 262, "ゴムクッション", FT, GRAY)
    ctext(d, 250, 280, "(ばね・減衰)", FT, GRAY)
    # ラジサポ
    d.rectangle((300, 150, 400, 300), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 350, 225, "ラジ\nサポ", FS, BLACK, "mm")
    ctext(d, 350, 320, "ラジエータサポート", FT, GRAY)
    # ボルト締結（複数点）
    for by in (180, 235, 290):
        d.line((400, by, 460, by), fill=BLACK, width=3)
        d.ellipse((452, by - 6, 464, by + 6), outline=BLACK, width=2, fill=FILL3)
    ctext(d, 430, 130, "ボルト複数点", FT, GRAY)
    # サイドメンバ
    d.rectangle((460, 130, 500, 320), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 520, 225, "フロント\nサイドメンバ", FT, GRAY, "lm")
    # 剛性の大小が判断対象
    ctext(d, 330, 360, "ゴムクッションとラジサポの剛性の大小が判断対象", FT, RED)
    save(im, name)


def tire_stiff_var(name):  # 8-11 required
    im, d = new()
    title(d, "タイヤ周方向の剛性変動（左:1箇所 / 右:等間隔4箇所）")
    for (cx, nprot, cap) in [(180, 1, "突出 1 箇所"), (475, 4, "等間隔 4 箇所")]:
        r = 90
        cy = 150 + r + 60
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3)
        d.ellipse((cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22),
                  outline=GRAY, width=2)
        node(d, cx, cy, 5, "white")
        # 剛性突出部（外周の太いこぶ）
        for k in range(nprot):
            a = math.radians(90 - k * 360.0 / nprot)
            px = cx + r * math.cos(a)
            py = cy - r * math.sin(a)
            d.ellipse((px - 12, py - 12, px + 12, py + 12), outline=RED, width=3, fill=FILL3)
        # 回転方向
        curve_arrow(d, cx, cy, r + 18, 40, 110, BLUE, 2, 10)
        # 半径R
        arrow(d, cx, cy, cx + r * 0.7, cy - r * 0.7, GRAY, 2, 9)
        ctext(d, cx + 34, cy - 34, "R", FT, GRAY)
        ctext(d, cx, cy + r + 24, cap, FT, GRAY)
    ctext(d, 330, 60, "半径 R・車速 V・回転方向を共通に", FT, GRAY)
    save(im, name)


def excavator_bc(name):  # 8-12 required
    im, d = new()
    title(d, "油圧ショベルの作業機（境界A:取付部 / 境界B:刃先）")
    # 車体
    d.rectangle((70, 300, 200, 360), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 135, 330, "車体", FT, GRAY)
    for cx in (100, 170):
        d.ellipse((cx - 16, 355, cx + 16, 385), outline=BLACK, width=2, fill=FILL1)
    # 取付部（境界A）
    base = (200, 300)
    d.line((base[0], base[1], 330, 150), fill=BLACK, width=8)  # ブーム
    ctext(d, 250, 235, "ブーム", FT, GRAY, "lm")
    at = (450, 230)
    d.line((330, 150, at[0], at[1]), fill=BLACK, width=7)      # アーム
    ctext(d, 400, 175, "アーム", FT, GRAY)
    # バケット
    bk = [(at[0], at[1]), (at[0] + 55, at[1] + 25), (at[0] + 28, at[1] + 68),
          (at[0] - 12, at[1] + 52)]
    d.polygon(bk, outline=BLACK, width=3, fill=FILL1)
    ctext(d, at[0] + 30, at[1] + 90, "バケット", FT, GRAY)
    # 岩盤
    d.rectangle((430, at[1] + 78, 590, at[1] + 120), outline=BLACK, width=2, fill=FILL3)
    ctext(d, 510, at[1] + 99, "硬い岩盤", FT, GRAY)
    # 境界A
    d.ellipse((base[0] - 16, base[1] - 16, base[0] + 16, base[1] + 16), outline=RED, width=3)
    ctext(d, base[0] - 24, base[1] - 26, "境界A", FT, RED, "rm")
    # 境界B（刃先）
    bt = (at[0] + 28, at[1] + 68)
    d.ellipse((bt[0] - 15, bt[1] - 15, bt[0] + 15, bt[1] + 15), outline=RED, width=3)
    ctext(d, bt[0] + 22, bt[1], "境界B（刃先）", FT, RED, "lm")
    save(im, name)


def seismic_tower(name):  # 8-13 required
    im, d = new()
    title(d, "地盤上の塔状構造物と基礎への地震加速度入力")
    # 地盤
    gy = 340
    hwall(d, 120, 540, gy, side=1, n=14)
    ctext(d, 490, gy - 12, "地盤", FT, GRAY, "lm")
    # 塔（細長い台形）
    cx = 300
    d.polygon([(cx - 55, gy), (cx + 55, gy), (cx + 28, 90), (cx - 28, 90)],
              outline=BLACK, width=3, fill=FILL1)
    # 分割の横線
    for y in (140, 190, 240, 290):
        xw = 28 + (gy - y) / (gy - 90) * 27
        d.line((cx - xw, y, cx + xw, y), fill=LGRAY, width=1)
    ctext(d, cx + 90, 150, "塔状構造物", FT, GRAY, "lm")
    # 折損想定位置（薄く）
    dash(d, cx - 45, 250, cx + 45, 250, GRAY, 2)
    ctext(d, cx - 60, 250, "折損想定", FT, GRAY, "rm")
    # 基礎への地震加速度入力（左右揺れ）
    base = (cx, gy)
    arrow(d, base[0] - 70, gy + 24, base[0] - 20, gy + 24, RED, 4, 13)
    arrow(d, base[0] + 70, gy + 24, base[0] + 20, gy + 24, RED, 4, 13)
    ctext(d, cx, gy + 46, "基礎に地震加速度（左右揺れ）", FT, RED)
    save(im, name)


def random_psd(name):  # 8-14 required
    im, d = new()
    title(d, "ランダム振動：入力PSD から応答を求める流れ")

    def mini_psd(ox, oy, cap, peaked=False, col=BLUE):
        axes(d, ox, oy, 130, 90, "f", "PSD", GRAY)
        pts = []
        for i in range(61):
            t = i / 60.0
            x = ox + 120 * t
            if peaked:
                y = oy - 80 * (0.15 + 0.8 * math.exp(-((t - 0.5) ** 2) / 0.01))
            else:
                y = oy - 80 * (0.25 + 0.35 * math.sin(math.pi * t))
            pts.append((x, y))
        plot(d, 0, 0, pts, col, 2)
        ctext(d, ox + 60, oy + 22, cap, FT, GRAY)

    # 入力（PSDで与える＝問題文の与件）
    mini_psd(90, 180, "入力PSD（与件）", peaked=False)
    arrow(d, 235, 150, 285, 150, BLUE, 3, 12)
    # 応答（求める量＝（a）は伏せる。縦軸は?）
    axes(d, 300, 180, 130, 90, "f", "?", GRAY)
    pts = []
    for i in range(61):
        t = i / 60.0
        x = 300 + 120 * t
        y = 180 - 80 * (0.15 + 0.8 * math.exp(-((t - 0.5) ** 2) / 0.01))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 2)
    ctext(d, 360, 202, "応答（a）?", FT, RED)
    arrow(d, 445, 150, 495, 150, BLUE, 3, 12)
    # 推定量（b）は伏せる
    d.rectangle((500, 120, 600, 180), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 550, 150, "（b）?", FS, RED)
    ctext(d, 550, 200, "応答から推定", FT, GRAY)
    note(d, "入力PSD →（a）応答? →（b）? を推定（答えは伏せる）")
    save(im, name)


def fatigue_sine(name):  # 8-15 helpful
    im, d = new()
    title(d, "疲労検討で選ぶ周波数：大入力ピーク＋固有振動数")
    ox, oy = 110, 330
    axes(d, ox, oy, 460, 250, "周波数 f", "入力PSD")
    # 入力PSD（複数ピーク）
    pts = []
    for i in range(201):
        t = i / 200.0
        x = ox + 440 * t
        y = (0.12
             + 0.75 * math.exp(-((t - 0.30) ** 2) / 0.004)   # 大入力ピーク
             + 0.25 * math.exp(-((t - 0.65) ** 2) / 0.006)
             + 0.18 * math.exp(-((t - 0.85) ** 2) / 0.004))
        pts.append((x, oy - 230 * min(y, 1.0)))
    plot(d, 0, 0, pts, BLUE, 2)
    # 大入力ピークをマーク
    xp = ox + 440 * 0.30
    arrow(d, xp, oy - 250, xp, oy - 205, RED, 2, 10)
    ctext(d, xp, oy - 262, "入力振幅が大きい成分", FT, RED)
    # 固有振動数の位置（縦破線）
    xf = ox + 440 * 0.65
    dash(d, xf, oy, xf, oy - 210, GREEN, 2)
    ctext(d, xf + 6, oy - 220, "固有振動数", FT, GREEN, "lm")
    note(d, "この2種の周波数成分を検討する")
    save(im, name)


def compressor_rpm(name):  # 8-16 required
    im, d = new()
    title(d, "圧縮機の回転子・軸受（回転数 900〜4800 rpm）")
    # 軸受（左右）
    for bx in (150, 490):
        d.rectangle((bx - 22, 210, bx + 22, 280), outline=BLACK, width=3, fill=FILL2)
        for i in range(4):
            d.line((bx - 22, 218 + i * 16, bx + 22, 218 + i * 16), fill=LGRAY, width=1)
        ctext(d, bx, 296, "軸受", FT, GRAY)
    # 軸
    d.rectangle((150, 235, 490, 255), outline=BLACK, width=3, fill=FILL1)
    # 回転子（円板）
    cx, cy = 320, 245
    d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 6, "white")
    ctext(d, cx, cy + 80, "回転子", FT, GRAY)
    # 回転数範囲（回転矢印）
    curve_arrow(d, cx, cy, 78, 30, 150, BLUE, 3, 12)
    ctext(d, cx, cy - 96, "900 〜 4800 rpm", FS, BLUE)
    # 換算式
    ctext(d, 330, 372, "f [Hz] = rpm / 60", FS, GRAY)
    save(im, name)


def bearing_stiffness(name):  # 8-17 required
    im, d = new()
    title(d, "軸受を線形ばねとみなす（荷重 F と変位 x）")
    # 固定壁
    wall(d, 150, 150, 300, side=1, n=9)
    # ばね（水平）
    spring(d, 165, 225, 360, 225, coils=6, amp=18)
    # 軸受質点
    d.rectangle((360, 190, 440, 260), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 400, 225, "軸受", FS)
    # 荷重 F
    arrow(d, 440, 225, 530, 225, RED, 4, 15)
    ctext(d, 540, 225, "F = 1500 N", FS, RED, "lm")
    # 変位 x
    dash(d, 360, 285, 360, 300, GRAY, 2)
    dash(d, 400, 285, 400, 300, GRAY, 2)
    dim(d, 360, 300, 400, 300, "x = 0.005 mm", col=GRAY)
    # 式
    ctext(d, 330, 360, "支持剛性 K = F / x", F, GRAY)
    save(im, name)


def psd_derivatives(name):  # 8-18 required
    im, d = new()
    title(d, "変位・速度・加速度のPSD（同一横軸・両対数）")
    ox, oy = 110, 340
    axes(d, ox, oy, 470, 260, "周波数（対数）", "PSD（対数）")
    xL = ox + 470
    # 低周波の1点で交わり、高域で開く3直線（傾き大=最上、小=最下）
    x0 = ox + 60
    y0 = oy - 40           # 交点
    slopes = [(0.60, "(a)", BLUE), (0.42, "(b)", GREEN), (0.24, "(c)", ORANGE)]
    for sl, lab, col in slopes:
        x1 = ox + 440
        y1 = y0 - (x1 - x0) * sl
        plot(d, 0, 0, [(x0, y0), (x1, y1)], col, 3)
        ctext(d, x1 + 14, y1, lab, FS, col, "lm")
    node(d, x0, y0, 4, RED)
    ctext(d, x0 + 6, y0 + 16, "低周波で一致", FT, GRAY, "lm")
    note(d, "高域ほど3曲線の差が開く（各曲線の対応は伏せる）")
    save(im, name)


def tire_unbalance_curve(name):  # 8-19 helpful
    im, d = new()
    title(d, "車速と加振力の関係（4候補）")
    ox, oy = 110, 340
    axes(d, ox, oy, 470, 260, "車速", "加振力")
    xw, yw = 440, 240

    def curve(fn, col, lab, lx, ly):
        pts = []
        for i in range(1, 101):
            t = i / 100.0
            x = ox + xw * t
            v = fn(t)
            y = oy - yw * min(v, 1.0)
            pts.append((x, y))
        plot(d, 0, 0, pts, col, 2)
        ctext(d, lx, ly, lab, FT, col, "lm")

    curve(lambda t: 0.05 / (t + 0.05) * 0.9, GRAY, "反比例", ox + 60, oy - 200)
    curve(lambda t: 0.9 * t, GREEN, "比例(1乗)", ox + 300, oy - 210)
    curve(lambda t: 0.9 * t * t, BLUE, "2乗に比例", ox + 330, oy - 140)
    curve(lambda t: 0.5, ORANGE, "一定", ox + 250, oy - 115)
    save(im, name)


def road_undulation(name):  # 8-20 required
    im, d = new()
    title(d, "路面うねり（波長 lambda）上を走る車両・前後輪の位相差")
    ox, oy, w = 70, 320, 520
    amp, waves = 20, 4
    pts = []
    for i in range(201):
        t = i / 200.0
        x = ox + w * t
        y = oy - amp * math.sin(2 * math.pi * waves * t)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLACK, 3)
    for i in range(0, 26):
        xx = ox + i * w / 26
        d.line((xx, oy + amp + 6, xx + 9, oy + amp + 16), fill=GRAY, width=1)
    # 波長
    px0 = ox + w * (0.25 / waves)
    px1 = px0 + w / waves
    dim(d, px0, oy - 52, px1, oy - 52, "波長 lambda", col=BLUE)
    # 車両ボディ
    rx, fx = ox + 180, ox + 320   # 後輪・前輪 接地x（前輪が進行方向前方=右）
    by = oy - 120
    d.rectangle((rx - 20, by, fx + 20, by + 44), outline=BLACK, width=3, fill=FILL1)
    d.polygon([(rx + 20, by), (rx + 45, by - 24), (fx - 25, by - 24), (fx - 5, by)],
              outline=BLACK, width=3, fill=FILL3)
    # 前後輪（路面の異なる位相に接地）
    for wx in (rx, fx):
        wy = oy - amp * math.sin(2 * math.pi * waves * (wx - ox) / w)
        d.ellipse((wx - 18, wy - 34, wx + 18, wy), outline=BLACK, width=3, fill=FILL2)
    ctext(d, rx - 30, by + 70, "後輪", FT, GRAY, "rm")
    ctext(d, fx + 30, by + 70, "前輪", FT, GRAY, "lm")
    # ホイールベース L
    dim(d, rx, by + 78, fx, by + 78, "ホイールベース L", col=RED)
    # 車速
    arrow(d, fx + 40, by + 20, fx + 95, by + 20, RED, 4, 13)
    ctext(d, fx + 68, by + 4, "V", FT, RED)
    save(im, name)


def rail_wheel_unbalance(name):  # 8-21 required
    im, d = new()
    title(d, "鉄道車輪のアンバランス質量と遠心力（加振力）")
    cx, cy = 300, 240
    R = 120
    # 車輪（外周＋フランジ＋踏面）
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=4)
    d.ellipse((cx - R + 16, cy - R + 16, cx + R - 16, cy + R - 16), outline=GRAY, width=2)
    d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), outline=BLACK, width=3, fill=FILL2)
    node(d, cx, cy, 5, "white")
    # アンバランス質量 m（偏った位置）
    a = math.radians(55)
    r_off = 80
    mx = cx + r_off * math.cos(a)
    my = cy - r_off * math.sin(a)
    d.ellipse((mx - 14, my - 14, mx + 14, my + 14), outline=RED, width=3, fill=FILL3)
    ctext(d, mx + 2, my + 26, "質量 m", FT, RED, "mm")
    # 半径 r（中心→m）
    arrow(d, cx, cy, mx, my, GRAY, 2, 10)
    ctext(d, (cx + mx) / 2 - 12, (cy + my) / 2 + 10, "r", FT, GRAY)
    # 回転角速度 omega
    curve_arrow(d, cx, cy, R + 18, 20, 100, BLUE, 3, 12)
    ctext(d, cx + R + 8, cy - R + 20, "omega", FS, BLUE, "lm")
    # 遠心力（加振力）＝中心から外向き（mの延長）
    fx = cx + (r_off + 60) * math.cos(a)
    fy = cy - (r_off + 60) * math.sin(a)
    arrow(d, mx, my, fx, fy, GREEN, 4, 14)
    ctext(d, fx + 8, fy - 8, "遠心力（加振力）", FT, GREEN, "lm")
    save(im, name)


if __name__ == "__main__":
    quad_pressure_nodes("v2e8QuadPressureNodes")       # 8-1 required
    tri_split_nodes("v2e8TriSplitNodes")               # 8-2 helpful
    simple_support_beam("v2e8SimpleSupportBeam")       # 8-3 required
    sym_plane_lpart("v2e8SymPlaneLpart")               # 8-4 required
    hex_mirror("v2e8HexMirror")                        # 8-5 required
    vessel_embed("v2e8VesselEmbed")                    # 8-6 required
    large_mass("v2e8LargeMass")                        # 8-7 required
    rough_road("v2e8RoughRoad")                        # 8-8 required
    backdoor_ws("v2e8BackDoorWS")                      # 8-9 required
    radiator_support("v2e8RadiatorSupport")            # 8-10 required
    tire_stiff_var("v2e8TireStiffVar")                 # 8-11 required
    excavator_bc("v2e8ExcavatorBC")                    # 8-12 required
    seismic_tower("v2e8SeismicTower")                  # 8-13 required
    random_psd("v2e8RandomPSD")                        # 8-14 required
    fatigue_sine("v2e8FatigueSine")                    # 8-15 helpful
    compressor_rpm("v2e8CompressorRpm")                # 8-16 required
    bearing_stiffness("v2e8BearingStiffness")          # 8-17 required
    psd_derivatives("v2e8PSDderivatives")              # 8-18 required
    tire_unbalance_curve("v2e8TireUnbalanceCurve")     # 8-19 helpful
    road_undulation("v2e8RoadUndulation")              # 8-20 required
    rail_wheel_unbalance("v2e8RailWheelUnbalance")     # 8-21 required
    print("done 21")
