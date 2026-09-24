# -*- coding: utf-8 -*-
"""Phase2 Batch7(最終): 固体2級 第9章 境界条件(boundary-conditions.json)の
図なし5問へ後付けする図。接頭辞 bc9*(既存 figs_bc9.py の bc9* と衝突しない新規名)。
対象: 9-6 / 9-23 / 9-24 / 9-28 / 9-24b。すべて helpful(回答後表示)。
白地660x420・黒線・機構/概念のみ(正解番号・最終数値は焼き込まない)。
文字化け回避のためASCII/通常文字のみ使用。"""
import sys, math, os
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---------------- 共通ヘルパ ----------------
def box(d, x0, y0, x1, y1, fill="white", col=BLACK, wd=3):
    d.rectangle((x0, y0, x1, y1), outline=col, width=wd, fill=fill)


def mlines(d, cx, cy, lines, fnt=FT, fill=BLACK, lh=21):
    n = len(lines)
    y0 = cy - (n - 1) * lh / 2
    for i, s in enumerate(lines):
        ctext(d, cx, y0 + i * lh, s, fnt, fill)


def _ctxt(cell):
    return cell if isinstance(cell, str) else cell[0]


def _ccol(cell):
    return BLACK if isinstance(cell, str) else cell[1]


def draw_table(d, x0, y0, cols, rowh, rows, fnt=FT):
    xs = [x0]
    for w in cols:
        xs.append(xs[-1] + w)
    for r, row in enumerate(rows):
        y = y0 + r * rowh
        fill = FILL2 if r == 0 else "white"
        for c in range(len(cols)):
            box(d, xs[c], y, xs[c + 1], y + rowh, fill=fill, wd=2)
            fnt2 = FS if r == 0 else fnt
            ctext(d, (xs[c] + xs[c + 1]) / 2, y + rowh / 2, _ctxt(row[c]), fnt2, _ccol(row[c]))
    return xs


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=11):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg))
    for i in range(n):
        if i % 2:
            continue
        a, b = i / n, (i + 1) / n
        d.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=col, width=wd)


def rotrect(d, cx, cy, w, h, ang, col=BLACK, wd=3, dashed=False, fill=None):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    pts = []
    for sx, sy in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        pts.append((cx + sx * ca - sy * sa, cy + sx * sa + sy * ca))
    if fill and not dashed:
        d.polygon(pts, fill=fill)
    for i in range(4):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % 4]
        if dashed:
            dash(d, x1, y1, x2, y2, col, wd)
        else:
            d.line((x1, y1, x2, y2), fill=col, width=wd)
    return pts


def small_pin(d, x, y, s=13):
    d.polygon((x, y, x - s, y + s * 1.4, x + s, y + s * 1.4), outline=BLACK, width=2)
    d.line((x - s - 3, y + s * 1.4, x + s + 3, y + s * 1.4), fill=BLACK, width=2)


def small_roller(d, x, y, s=13):
    yy = y + s * 1.2
    d.polygon((x, y, x - s, yy, x + s, yy), outline=BLACK, width=2)
    for cx in (x - 6, x + 6):
        d.ellipse((cx - 4, yy, cx + 4, yy + 8), outline=BLACK, width=2)
    d.line((x - s - 2, yy + 8, x + s + 2, yy + 8), fill=BLACK, width=2)


def rotarc(d, cx, cy, r, a0, a1, col=GRAY, wd=3, label=""):
    """反時計まわりの回転矢印(screen度でa0->a1)。先端に矢じり。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), a1, a0, fill=col, width=wd)
    ar = math.radians(a1)
    tx, ty = cx + r * math.cos(ar), cy + r * math.sin(ar)
    tang = ar - math.pi / 2
    for s in (0.6, -0.6):
        d.line((tx, ty, tx - 12 * math.cos(tang - s), ty - 12 * math.sin(tang - s)), fill=col, width=wd)
    if label:
        ctext(d, cx, cy, label, FT, col)


# ============================================================
# bc-9-6 等価節点力:物体力と表面力の与え方
# ============================================================
def bc9EqForceTypes():
    im, d = new(); title(d, "等価節点力:物体力と表面力の与え方")
    rows = [
        ["区分", "代表例", "与え方のポイント"],
        ["物体力", "自重  b = rho*g", "要素質量を形状関数で配分"],
        ["物体力", "遠心力 b = rho*r*w^2", ("距離 r の1乗に比例(2乗でない)", RED)],
        ["表面力", "圧力 p", "受圧する辺に分布荷重として"],
    ]
    draw_table(d, 35, 74, [95, 235, 300], 46, rows)
    box(d, 35, 268, 625, 320, FILL1, GRAY, 2)
    mlines(d, 330, 294,
           ["節点への配分は形状関数で決まる(端 1/2 : 内側 1)。",
            "圧力の合力を節点数で単純に割った値にはならない。"], FT, BLACK, 22)
    note(d, "自重・遠心力=物体力、圧力=表面力。遠心力は r の1乗に比例するのが要注意点。")
    save(im, "bc9EqForceTypes")


# ============================================================
# bc-9-23 剛体モードの総数(並進+回転)
# ============================================================
def bc9RigidModeCount():
    im, d = new(); title(d, "剛体モードの総数(並進+回転で数える)")
    d.line((330, 58, 330, 360), fill=LGRAY, width=2)
    # ---- 左:2次元 ----
    ctext(d, 165, 76, "2次元問題", FS, BLUE)
    cx, cy = 165, 200
    box(d, cx - 55, cy - 45, cx + 55, cy + 45, FILL1, BLACK)
    arrow(d, cx, cy, cx + 92, cy, BLUE, 3, 12); ctext(d, cx + 104, cy, "並進x", FT, BLUE, "lm")
    arrow(d, cx, cy, cx, cy - 92, BLUE, 3, 12); ctext(d, cx, cy - 104, "並進y", FT, BLUE)
    rotarc(d, cx, cy, 30, 210, 60, GREEN, 3)
    ctext(d, cx - 44, cy + 22, "回転", FT, GREEN)
    ctext(d, 165, 312, "並進2 + 回転1 = 3", FS, BLACK)
    # ---- 右:3次元 ----
    ctext(d, 495, 76, "3次元問題", FS, RED)
    ox, oy = 452, 205
    iso_box(d, ox, oy, 80, 60, 44)
    bcx, bcy = ox + 40, oy + 30
    arrow(d, bcx, bcy, bcx + 96, bcy, BLUE, 3, 11); ctext(d, bcx + 108, bcy, "x", FT, BLUE, "lm")
    arrow(d, bcx, bcy, bcx, bcy - 100, BLUE, 3, 11); ctext(d, bcx, bcy - 112, "y", FT, BLUE)
    arrow(d, bcx, bcy, bcx + 52, bcy - 34, BLUE, 3, 11); ctext(d, bcx + 62, bcy - 40, "z", FT, BLUE, "lm")
    ctext(d, 495, 290, "並進3(x,y,z)", FT, GREEN)
    ctext(d, 495, 312, "+ 回転3 = 6", FS, BLACK)
    note(d, "剛体モードはひずみエネルギーを生まないゼロエネルギーモード。必ず拘束して取り除く。")
    save(im, "bc9RigidModeCount")


# ============================================================
# bc-9-24 剛体モードは変形せず動く(ひずみ0)
# ============================================================
def bc9RigidModeProps():
    im, d = new(); title(d, "剛体モード:形は変わらず動く(ひずみを生じない)")
    # 変形前(点線)
    rotrect(d, 155, 175, 120, 110, 0, GRAY, 2, dashed=True)
    ctext(d, 155, 240, "変形前", FT, GRAY)
    # 剛体移動後(同じ形・並進+回転)
    rotrect(d, 445, 195, 120, 110, 18, BLACK, 3, fill=FILL1)
    rotrect(d, 445, 195, 120, 110, 18, BLACK, 3)
    ctext(d, 470, 262, "剛体移動後(同じ形)", FT, BLACK)
    arrow(d, 225, 178, 360, 192, ORANGE, 4, 15)
    ctext(d, 292, 158, "並進 + 回転", FT, ORANGE)
    # 説明
    box(d, 45, 290, 615, 362, "white", BLUE, 2)
    mlines(d, 330, 326,
           ["形が変わらない  →  ひずみ=0 / ひずみエネルギー=0",
            "K phi = 0(剛体モード)。拘束しないと det(K)=0 で特異になる"], FT, BLACK, 28)
    note(d, "剛体モードはひずみを生じない。一定ひずみが加わるという説明は誤り。")
    save(im, "bc9RigidModeProps")


# ============================================================
# bc-9-28 MPC:従属自由度は1式のみ/独立は再利用可
# ============================================================
def bc9MpcDofRule():
    im, d = new(); title(d, "MPC:従属自由度は1式まで/独立は再利用可")
    d.line((330, 58, 330, 372), fill=LGRAY, width=2)
    # ---- 左:OK ----
    ctext(d, 165, 78, "OK", FS, GREEN)
    box(d, 40, 100, 290, 150, FILL1, BLACK)
    ctext(d, 165, 125, "式1:  u2 = f(u1, u3)", FS, BLACK)
    box(d, 40, 165, 290, 215, FILL1, BLACK)
    ctext(d, 165, 190, "式2:  u4 = g(u1, u5)", FS, BLACK)
    box(d, 55, 240, 275, 320, (232, 245, 235), GREEN, 2)
    mlines(d, 165, 280, ["u1 は独立自由度として", "複数の式で使ってよい"], FT, BLACK, 24)
    ctext(d, 165, 345, "従属は u2 / u4 で重複なし", FT, GREEN)
    # ---- 右:NG ----
    ctext(d, 495, 78, "NG", FS, RED)
    box(d, 375, 100, 620, 150, (250, 235, 235), BLACK)
    ctext(d, 497, 125, "式1:  u2 = f(u1)", FS, BLACK)
    box(d, 375, 165, 620, 215, (250, 235, 235), BLACK)
    ctext(d, 497, 190, "式2:  u2 = h(u5)", FS, BLACK)
    # u2 を2式の従属にした矛盾
    d.line((360, 125, 360, 190), fill=RED, width=3)
    ctext(d, 345, 157, "u2", FT, RED, "rm")
    box(d, 388, 240, 608, 320, "white", RED, 2)
    mlines(d, 498, 280, ["同じ u2 を2式の従属に", "= 消去で条件が矛盾"], FT, RED, 24)
    ctext(d, 498, 345, "X 従属自由度の重複は禁止", FT, RED)
    note(d, "従属自由度は1自由度につき1式まで。独立自由度としてなら何度使ってもよい。", y=395)
    save(im, "bc9MpcDofRule")


# ============================================================
# bc-9-24b 拘束の過不足が解に及ぼす影響
# ============================================================
def bc9ConstraintBalance():
    im, d = new(); title(d, "拘束の過不足が解に及ぼす影響")

    def body(x0, y0):
        box(d, x0, y0, x0 + 110, y0 + 58, FILL1, BLACK)

    # ---- 不足 ----
    box(d, 35, 74, 220, 300, "white", RED, 2)
    ctext(d, 127, 96, "拘束が不足", FS, RED)
    body(72, 140)
    arrow(d, 127, 150, 180, 122, ORANGE, 3, 12)
    rotarc(d, 127, 169, 40, 210, 30, ORANGE, 2)
    ctext(d, 127, 232, "剛体モードが残る", FT, BLACK)
    ctext(d, 127, 256, "det(K)=0 で特異", FT, RED)
    ctext(d, 127, 278, "= 解けない", FT, RED)
    # ---- 適切 ----
    box(d, 237, 74, 422, 300, "white", GREEN, 2)
    ctext(d, 329, 96, "適切", FS, GREEN)
    box(d, 274, 140, 384, 198, FILL1, BLACK)
    small_pin(d, 288, 198)
    small_roller(d, 370, 198)
    hwall(d, 262, 396, 226, side=1, n=9)
    ctext(d, 329, 250, "最小限の拘束", FT, BLACK)
    ctext(d, 329, 274, "正しく解ける", FT, GREEN)
    # ---- 過剰 ----
    box(d, 439, 74, 624, 300, "white", ORANGE, 2)
    ctext(d, 531, 96, "拘束が過剰", FS, ORANGE)
    box(d, 476, 140, 586, 198, FILL1, BLACK)
    wall(d, 476, 140, 198, side=-1, n=5)
    hwall(d, 476, 586, 198, side=1, n=7)
    for xx in (505, 557):
        arrow(d, xx, 168, xx, 140, BLUE, 3, 10)
    ctext(d, 531, 224, "余分に止める", FT, BLACK)
    ctext(d, 531, 250, "不自然な反力・応力", FT, ORANGE)
    ctext(d, 531, 274, "(拘束反力)", FT, ORANGE)
    note(d, "不足→特異で解けない / 過剰→拘束反力で誤った応力。必要最小限を過不足なく。")
    save(im, "bc9ConstraintBalance")


ALL = [bc9EqForceTypes, bc9RigidModeCount, bc9RigidModeProps, bc9MpcDofRule, bc9ConstraintBalance]
KEYS = [f.__name__ for f in ALL]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    miss = [k for k in KEYS if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(KEYS), "MISSING", miss)
