# -*- coding: utf-8 -*-
"""固体力学1級 第3章「幾何学的非線形」の問題図(s1e3*)・公式図(s1f3*)を描画。
白地660x420・線画・機構のみ・物理的に正確・装飾禁止。ラベルは通常表記(豆腐回避)。"""
import sys, math, os
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


def vmode(x0, ytop, ybot, amp, mode="half", n=48):
    """縦の柱の座屈モード形の点列を返す。x0=直線位置, amp=最大横たわみ。"""
    pts = []
    for i in range(n + 1):
        t = i / n
        y = ytop + (ybot - ytop) * t
        if mode == "half":      off = amp * math.sin(math.pi * t)
        elif mode == "full":    off = amp * math.sin(2 * math.pi * t)      # 両端固定風(全波)
        elif mode == "cant":    off = amp * (1 - math.cos(math.pi * t / 2))  # 片持ち 1/4波
        elif mode == "fixsimp": off = amp * math.sin(1.43 * math.pi * t) * (1 - t * 0.15)
        else:                   off = 0
        pts.append((x0 + off, y))
    return pts


def curvepts(fn, x0, x1, n=60):
    return [ (x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1) ]


# ============================================================
# s1e3GeoNLJudge : 幾何学的非線形の要否 4事例 2x2
# ============================================================
def geo_nl_judge():
    im, d = new(); title(d, "幾何学的非線形の要否(線形で足りるのはどれ)")
    d.line((330, 60, 330, 395), fill=LGRAY, width=1)
    d.line((30, 228, 630, 228), fill=LGRAY, width=1)
    # TL: 太く短い柱(線形でOK) 答
    hwall(d, 110, 230, 205, side=1, n=6)
    d.rectangle((150, 120, 190, 205), outline=BLACK, width=3, fill=FILL1)
    force(d, 170, 95, 0, 22, "", RED)
    ctext(d, 170, 78, "小さい軸圧縮", FT)
    ctext(d, 170, 216, "太く短い柱→線形でOK", FT, GREEN)
    # TR: 初期張力を入れた膜(面外荷重)
    d.line((380, 150, 600, 150), fill=BLACK, width=3)
    node(d, 380, 150, 5); node(d, 600, 150, 5)
    force(d, 380, 150, -22, 0, "", BLUE); force(d, 600, 150, 22, 0, "", BLUE)
    force(d, 490, 120, 0, 24, "", RED)
    ctext(d, 490, 108, "面外荷重", FT)
    ctext(d, 490, 180, "初期張力膜→考慮要", FT)
    # BL: 面内圧縮の薄板
    d.rectangle((155, 265, 185, 375), outline=BLACK, width=3, fill=FILL1)
    force(d, 130, 270, 22, 0, "", RED); force(d, 210, 270, -22, 0, "", RED)
    ctext(d, 170, 392, "面内圧縮薄板→考慮要", FT)
    # BR: 周辺固定の薄い円板 + 中央面外荷重
    d.ellipse((410, 300, 570, 340), outline=BLACK, width=3)
    wall(d, 410, 305, 335, side=1, n=3); wall(d, 570, 305, 335, side=-1, n=3)
    force(d, 490, 292, 0, 24, "", RED)
    ctext(d, 490, 392, "周辺固定円板→考慮要", FT)
    save(im, "s1e3GeoNLJudge")


# ============================================================
# s1e3BeamLargeRot : 片持ちはり大たわみ + 断面は微小ひずみ
# ============================================================
def beam_large_rot():
    im, d = new(); title(d, "大変位・大回転でも各点のひずみは微小")
    wall(d, 90, 110, 300, side=1, n=8)
    # 大きくたわむ片持ちはり(先端が上に巻き上がる)
    fn = lambda x: 300 - 190 * (1 - math.cos((x - 90) / 300 * (math.pi * 0.72)))
    pts = curvepts(fn, 90, 470, 70)
    d.line(pts, fill=BLACK, width=6, joint="curve")
    node(d, pts[-1][0], pts[-1][1], 5)
    ctext(d, pts[-1][0] + 8, pts[-1][1] - 14, "先端は大きく移動・回転", FT, GRAY, "lm")
    # 中間の微小要素→拡大枠
    mx, my = pts[35]
    d.rectangle((mx - 9, my - 9, mx + 9, my + 9), outline=RED, width=2)
    dashed(d, mx + 9, my - 9, 500, 250, RED); dashed(d, mx + 9, my + 9, 500, 360, RED)
    d.rectangle((500, 250, 600, 360), outline=RED, width=2)
    d.rectangle((525, 280, 575, 330), outline=BLACK, width=2, fill=FILL1)
    dashed(d, 578, 280, 578, 330, GRAY)
    ctext(d, 550, 268, "拡大", FT)
    ctext(d, 550, 348, "微小ひずみ ε<1%", FT)
    save(im, "s1e3BeamLargeRot")


# ============================================================
# Beckの柱(従動力) 共通描画  s1e3FollowerForce / s1f3FollowerForce
# ============================================================
def _beck(name, ttl):
    im, d = new(); title(d, ttl)
    hwall(d, 235, 335, 380, side=1, n=8)
    # たわんだ片持ち柱(下端固定・上へ)
    fn = lambda y: 285 + 70 * (1 - math.cos((380 - y) / 300 * (math.pi / 2)))
    pts = [ (fn(y), y) for y in range(380, 90, -6) ]
    d.line(pts, fill=BLACK, width=6, joint="curve")
    tipx, tipy = pts[-1]
    # 先端の接線方向(圧縮=柱内向き)に追従する従動荷重
    p2x, p2y = pts[-6]
    dx, dy = tipx - p2x, tipy - p2y
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    ax, ay = tipx + ux * 70, tipy + uy * 70
    arrow(d, ax, ay, tipx, tipy, RED, 4, 15)
    ctext(d, ax + 6, ay - 12, "P(先端接線方向)", FT, RED, "lm")
    # 元の直立軸(点線)
    dashed(d, 285, 380, 285, 100, LGRAY)
    ctext(d, 150, 200, "変形で荷重の向きが\n追従→従動力", FT, GRAY, "lm")
    ctext(d, 285, 405, "Beckの柱:荷重剛性が非対称→フラッター", FT)
    save(im, name)


# ============================================================
# 極分解 F=RU  s1e3PolarDecomp / s1f3PolarDecomp
# ============================================================
def _polar(name):
    im, d = new(); title(d, "変形勾配の極分解  F = R U")
    # 1) 元の正方形
    d.rectangle((60, 180, 140, 260), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 100, 285, "元の正方要素", FT)
    ctext(d, 100, 165, "F", FT, GRAY)
    # 矢印 U(伸ばす)
    arrow(d, 160, 220, 240, 220, BLACK, 3, 13)
    ctext(d, 200, 204, "U:伸ばす", FT)
    # 2) 伸びた長方形
    d.rectangle((260, 165, 380, 260), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 320, 285, "右ストレッチ U", FT)
    # 矢印 R(回す)
    arrow(d, 400, 220, 470, 210, BLACK, 3, 13)
    ctext(d, 435, 190, "R:回す", FT)
    # 3) 回転した長方形(30度傾ける)
    cx, cy, w, h, ang = 560, 220, 120, 95, math.radians(30)
    c, s = math.cos(ang), math.sin(ang)
    corn = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
    poly = [ (cx + px * c - py * s, cy + px * s + py * c) for px, py in corn ]
    d.polygon(poly, outline=BLACK, width=3, fill=FILL2)
    ctext(d, 560, 300, "R U(伸びて回転)", FT)
    angle_arc(d, cx, cy, 55, 0, 30, "", GRAY)
    save(im, name)


# ============================================================
# s1e3StretchBar : 棒がLからlへ伸びる  λ=l/L
# ============================================================
def stretch_bar():
    im, d = new(); title(d, "棒の伸びと伸び比  λ = l / L")
    node(d, 120, 150, 6)
    bar(d, 120, 150, 320, 150, thick=26)
    node(d, 320, 150, 6)
    dim(d, 120, 110, 320, 110, "初期長さ L", col=GRAY)
    ctext(d, 220, 178, "変形前", FT, GRAY)
    node(d, 120, 280, 6)
    bar(d, 120, 280, 460, 280, thick=26)
    node(d, 460, 280, 6)
    dim(d, 120, 240, 460, 240, "変形後長さ l", col=GRAY)
    dashed(d, 320, 267, 320, 293, RED)
    arrow(d, 340, 280, 448, 280, RED, 3, 12)
    ctext(d, 220, 308, "変形後", FT, GRAY)
    ctext(d, 330, 358, "λ = l/L ,   E11 = (1/2)(λ^2 - 1)", FT)
    save(im, "s1e3StretchBar")


# ============================================================
# s1e3StressMeasures : PK応力(変形前面積) vs コーシー応力(現面積)
# ============================================================
def stress_measures():
    im, d = new(); title(d, "応力の基準面積:PK応力 と コーシー応力")
    # 左:変形前 太い断面 A0
    bar(d, 150, 180, 150, 300, thick=70)
    force(d, 150, 150, 0, -30, "", RED); ctext(d, 150, 120, "力", FT)
    dim(d, 115, 240, 185, 240, "A0", col=GRAY)
    ctext(d, 150, 330, "PK応力:変形前面積A0基準", FT)
    ctext(d, 150, 350, "(Green-Lagrangeと対・TL法)", FT, GRAY)
    # 右:変形後 細い断面 A
    bar(d, 470, 150, 470, 330, thick=38)
    force(d, 470, 120, 0, -30, "", RED); ctext(d, 470, 95, "力", FT)
    dim(d, 451, 240, 489, 240, "A", col=GRAY)
    ctext(d, 470, 355, "コーシー応力:現配置面積A基準", FT)
    ctext(d, 470, 375, "(対数ひずみと対・UL法)", FT, GRAY)
    save(im, "s1e3StressMeasures")


# ============================================================
# s1e3TrussUniaxial : 一軸トラス端に鉛直変位u・荷重F
# ============================================================
def truss_uniaxial():
    im, d = new(); title(d, "一軸トラス:端の鉛直変位 u と荷重 F")
    wall(d, 110, 130, 260, side=1, n=6)
    ax, ay = 110, 190
    bx, by = 520, 190
    # 元の水平部材(点線)
    dashed(d, ax, ay, bx, by, LGRAY)
    node(d, bx, by, 6); ctext(d, bx + 14, by - 6, "初期位置", FT, GRAY, "lm")
    dim(d, ax, 150, bx, 150, "初期長さ L", col=GRAY)
    # 変形後:端が u だけ下がる
    dbx, dby = 520, 300
    bar(d, ax, ay, dbx, dby, thick=0)
    node(d, ax, ay, 6); node(d, dbx, dby, 7)
    dashed(d, bx, by, dbx, dby, RED)
    arrow(d, dbx + 40, by, dbx + 40, dby, GRAY, 2, 10)
    ctext(d, dbx + 52, (by + dby) / 2, "u", FS, GRAY, "lm")
    force(d, dbx, dby + 8, 0, 40, "F", RED)
    ctext(d, 330, 360, "E11 = u^2/(2L^2) → F = E A u^3 /(2 L^3)", FT)
    save(im, "s1e3TrussUniaxial")


# ============================================================
# s1e3TLUL : TL法(参照=時刻0) と UL法(参照=時刻t)
# ============================================================
def tl_ul():
    im, d = new(); title(d, "参照配置の違い:TL法(時刻0) と UL法(時刻t)")
    # 左 TL
    ctext(d, 175, 70, "TL法", F)
    d.rectangle((90, 120, 160, 190), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 125, 205, "時刻0(基準)", FT, GREEN)
    poly = [(220, 130), (300, 115), (315, 195), (235, 210)]
    d.polygon(poly, outline=BLACK, width=3, fill=FILL2)
    ctext(d, 268, 225, "時刻t", FT, GRAY)
    arrow(d, 168, 165, 212, 160, GRAY, 2, 11)
    ctext(d, 175, 260, "常に時刻0を基準\n(S, E)を使う", FT, GRAY)
    d.line((330, 90, 330, 340), fill=LGRAY, width=1)
    # 右 UL
    ctext(d, 500, 70, "UL法", F)
    d.rectangle((410, 120, 480, 190), outline=LGRAY, width=2, fill="white")
    ctext(d, 445, 205, "時刻0", FT, GRAY)
    poly2 = [(545, 130), (625, 115), (640, 195), (560, 210)]
    d.polygon(poly2, outline=BLACK, width=3, fill=FILL2)
    ctext(d, 593, 225, "時刻t(基準)", FT, GREEN)
    arrow(d, 490, 160, 537, 160, GRAY, 2, 11)
    ctext(d, 505, 260, "現配置を基準に更新\n(σ, 対数ひずみ)", FT, GRAY)
    ctext(d, 330, 375, "参照時刻が違うだけ・内部仕事は同じ=等価", FT, GRAY)
    save(im, "s1e3TLUL")


# ============================================================
# s1e3RigidRotStress : 伸長後90度回転しても主応力は物質線に付随
# ============================================================
def rigid_rot_stress():
    im, d = new(); title(d, "剛体回転しても主応力は物質線に付随(TL法)")
    # 左:X1方向に伸ばした棒(水平)
    bar(d, 90, 200, 250, 200, thick=40)
    arrow(d, 60, 200, 88, 200, RED, 3, 12); arrow(d, 280, 200, 252, 200, RED, 3, 12)
    ctext(d, 170, 245, "X1方向に伸長", FT)
    ctext(d, 170, 168, "主応力 S11", FT, RED)
    axes(d, 90, 300, 60, 40, "X1", "X2")
    # 回転矢印
    arrow(d, 300, 200, 360, 200, BLACK, 3, 13)
    ctext(d, 330, 178, "90度回転", FT)
    # 右:縦向きになった棒。主応力も一緒に回り、物質線(元X1)に付随
    bar(d, 500, 130, 500, 290, thick=40)
    arrow(d, 500, 100, 500, 128, RED, 3, 12); arrow(d, 500, 320, 500, 292, RED, 3, 12)
    ctext(d, 545, 210, "主応力 S11\n(元X1=物質線)", FT, RED, "lm")
    save(im, "s1e3RigidRotStress")


# ============================================================
# s1e3TangentStiff : K_T = K0 + K_L + K_G の構成
# ============================================================
def tangent_stiff():
    im, d = new(); title(d, "TL法の接線剛性  K_T = K0 + K_L + K_G")
    def box(x, tag, sub, col=BLACK):
        d.rectangle((x, 170, x + 120, 250), outline=col, width=3)
        ctext(d, x + 60, 200, tag, F, col)
        ctext(d, x + 60, 228, sub, FT, GRAY)
    ctext(d, 55, 210, "K_T =", F)
    box(100, "K0", "増分剛性")
    ctext(d, 235, 210, "+", F)
    box(255, "K_L", "初期変位")
    ctext(d, 390, 210, "+", F)
    box(410, "K_G", "初期応力", RED)
    ctext(d, 120, 300, "微小変形理論\n(変位に非依存)", FT, GRAY)
    ctext(d, 315, 300, "今の変位で変化\nTL特有(ULで消える)", FT, GRAY)
    ctext(d, 470, 300, "今の応力で変化\n=幾何剛性", FT, GRAY)
    ctext(d, 330, 370, "UL法では K_T = K0 + K_G", FT)
    save(im, "s1e3TangentStiff")


# ============================================================
# s1e3LoadDispCritical : 荷重変位曲線の極限点・分岐点で接線水平
# ============================================================
def load_disp_critical():
    im, d = new(); title(d, "座屈点で接線剛性が特異(接線が水平)")
    ox, oy = 90, 350
    axes(d, ox, oy, 500, 290, "変位 w", "荷重 P")
    # 極限点をもつ曲線(山)
    fn = lambda x: oy - (0.9 * (x - ox) - 0.0019 * (x - ox) ** 2)
    pts = curvepts(fn, ox, ox + 470, 80)
    d.line(pts, fill=BLUE, width=3, joint="curve")
    # 極限点(頂点・水平接線)
    lx = ox + 237
    ly = fn(lx)
    node(d, lx, ly, 6)
    d.line((lx - 55, ly, lx + 55, ly), fill=RED, width=2)
    ctext(d, lx, ly - 22, "極限点(det K_T=0)", FT, RED)
    # 分岐点(途中で枝分かれ)
    bx = ox + 120; by = fn(bx)
    node(d, bx, by, 6)
    br = [ (bx + 90 * (i / 30), by - 70 * (i / 30)) for i in range(31) ]
    d.line(br, fill=GREEN, width=2, joint="curve")
    ctext(d, bx - 6, by + 20, "分岐点", FT, GREEN, "rm")
    save(im, "s1e3LoadDispCritical")


# ============================================================
# 分岐座屈 と 飛移り座屈  s1e3BucklingTypes / s1f3BuckleTypes
# ============================================================
def _buckle_types(name):
    im, d = new(); title(d, "分岐座屈 と 飛移り(スナップスルー)座屈")
    # 左:分岐座屈
    ox, oy = 70, 320
    axes(d, ox, oy, 230, 240, "w", "P")
    main = [(ox, oy), (ox, oy - 150)]
    d.line(main, fill=BLUE, width=3)
    node(d, ox, oy - 150, 6)
    ctext(d, ox + 8, oy - 150, "分岐点", FT, RED, "lm")
    branch = [ (ox + 120 * (i / 30), oy - 150 - 55 * (i / 30)) for i in range(31) ]
    d.line(branch, fill=GREEN, width=3, joint="curve")
    br2 = [ (ox - 120 * (i / 30) if ox - 120 * (i/30) > ox-0 else ox, 0) for i in range(0) ]
    dashed(d, ox, oy - 150, ox, oy - 205, LGRAY)
    ctext(d, 185, 355, "分岐座屈(枝分かれ)", FT)
    # 右:飛移り座屈(極限点+飛移り)
    ox2, oy2 = 380, 320
    axes(d, ox2, oy2, 240, 240, "w", "P")
    fn = lambda x: oy2 - (1.15 * (x - ox2) - 0.0125 * (x - ox2) ** 2)
    up = curvepts(fn, ox2, ox2 + 92, 40)
    d.line(up, fill=BLUE, width=3, joint="curve")
    lx = ox2 + 46; ly = fn(lx)
    node(d, lx, ly, 6); ctext(d, lx, ly - 20, "極限点", FT, RED)
    # 飛移り(水平点線ジャンプ)
    tx = ox2 + 175; ty = ly
    dashed(d, lx, ly, tx, ty, RED)
    arrow(d, tx - 30, ty, tx, ty, RED, 3, 11)
    node(d, tx, ty, 6)
    # 下側の安定分枝
    down = curvepts(lambda x: oy2 - (0.2 * (x - ox2) + 0.004 * (x - ox2) ** 2), ox2 + 92, ox2 + 200, 40)
    d.line(down, fill=BLUE, width=3, joint="curve")
    ctext(d, 500, 355, "飛移り座屈(極限点で飛移り)", FT)
    save(im, name)


# ============================================================
# 境界条件別の座屈モード形  s1e3ColumnBC / s1f3EulerBuckle
# ============================================================
def _column_bc(name, ttl):
    im, d = new(); title(d, ttl)
    ctext(d, 330, 58, "Pcr = λ π^2 EI / l^2   (拘束が強いほど λ 大)", FT, GRAY)
    ytop, ybot = 100, 345
    cols = [
        (95,  "half", "両端単純支持", "λ=1",    "pin", "pin"),
        (245, "full", "両端固定",     "λ=4",    "fix", "fix"),
        (395, "cant", "片持ち(固定-自由)", "λ=0.25", "fix", "free"),
        (545, "fixsimp", "固定-単純", "λ=2.04", "fix", "pin"),
    ]
    for x0, mode, nm, lam, top, bot in cols:
        dashed(d, x0, ytop, x0, ybot, LGRAY)
        pts = vmode(x0, ytop, ybot, 30, mode)
        d.line(pts, fill=BLUE, width=4, joint="curve")
        # 上端支持
        if top == "pin":
            node(d, x0, ytop, 6)
        elif top == "fix":
            d.line((x0 - 24, ytop, x0 + 24, ytop), fill=BLACK, width=3)
            for i in range(5): d.line((x0 - 24 + i * 12, ytop, x0 - 34 + i * 12, ytop - 11), fill=BLACK, width=2)
        elif top == "free":
            node(d, pts[0][0], ytop, 5)
            force(d, x0, ytop - 42, 0, 26, "", RED)
        # 下端支持
        if bot == "pin":
            pin_support(d, x0, ybot, 16)
        elif bot == "fix":
            d.line((x0 - 24, ybot, x0 + 24, ybot), fill=BLACK, width=3)
            for i in range(5): d.line((x0 - 24 + i * 12, ybot + 11, x0 - 14 + i * 12, ybot), fill=BLACK, width=2)
        elif bot == "free":
            fx = pts[-1][0]
            node(d, fx, ybot, 5)
            force(d, fx, ybot + 40, 0, -26, "", RED)
        ctext(d, x0, ybot + 46, nm, FT)
        ctext(d, x0, ybot + 64, lam, FT, RED)
    save(im, name)


# ============================================================
# s1e3EulerColumn : 両端単純支持 第1次座屈モード(半波正弦)
# ============================================================
def euler_column():
    im, d = new(); title(d, "両端単純支持柱の第1次座屈モード(半波正弦)")
    x0, ytop, ybot = 300, 100, 330
    dashed(d, x0, ytop, x0, ybot, LGRAY)
    pts = vmode(x0, ytop, ybot, 55, "half")
    d.line(pts, fill=BLUE, width=5, joint="curve")
    node(d, x0, ytop, 7)
    pin_support(d, x0, ybot, 20)
    force(d, x0, ytop - 55, 0, 34, "P", RED)
    ctext(d, x0 + 62, (ytop + ybot) / 2, "w = C sin(πx/l)", FS, BLUE, "lm")
    dim(d, 235, ytop, 235, ybot, "l", col=GRAY)
    ctext(d, 330, 375, "Pcr = π^2 EI / l^2   (λ=1)", FT)
    save(im, "s1e3EulerColumn")


# ============================================================
# s1e3EigenBuckling : (K0+λKG)v=0 一般固有値問題と座屈荷重λP
# ============================================================
def eigen_buckling():
    im, d = new(); title(d, "線形座屈固有値解析  (K0 + λ K_G) v = 0")
    d.rectangle((120, 150, 540, 230), outline=BLACK, width=3)
    ctext(d, 330, 190, "( K0 + λ K_G ) { v } = { 0 }", F)
    ctext(d, 330, 258, "1回の一般固有値解析で解く", FT, GRAY)
    arrow(d, 240, 285, 240, 320, GRAY, 2, 11)
    arrow(d, 430, 285, 430, 320, GRAY, 2, 11)
    ctext(d, 240, 342, "固有値 λ", FS)
    ctext(d, 240, 366, "→ 座屈荷重 = λ P", FT, RED)
    ctext(d, 430, 342, "固有ベクトル v", FS)
    ctext(d, 430, 366, "→ 座屈モード形", FT)
    ctext(d, 330, 120, "P:基準荷重(K_G は P による応力から作る)", FT, GRAY)
    save(im, "s1e3EigenBuckling")


# ============================================================
# s1e3LinearBucklingNG : 座屈前挙動の比較 4構造 2x2
# ============================================================
def linear_buckling_ng():
    im, d = new(); title(d, "線形座屈解析の可否(座屈前が線形か)")
    d.line((330, 60, 330, 395), fill=LGRAY, width=1)
    d.line((30, 228, 630, 228), fill=LGRAY, width=1)
    # TL: 集中荷重アーチ(座屈前から曲げ非線形→不適)  ※答=不適切
    arcpts = [ (100 + 160 * (i / 40), 200 - 60 * math.sin(math.pi * i / 40)) for i in range(41) ]
    d.line(arcpts, fill=BLACK, width=4, joint="curve")
    pin_support(d, 100, 200, 12); pin_support(d, 260, 200, 12)
    force(d, 180, 108, 0, 26, "", RED)
    ctext(d, 180, 250, "集中荷重アーチ", FT)
    ctext(d, 180, 268, "座屈前から非線形→不適", FT, RED)
    # TR: 一様収縮リング(適)
    d.ellipse((445, 105, 545, 195), outline=BLACK, width=4)
    for a in range(0, 360, 45):
        r = math.radians(a); cx, cy = 495, 150
        force(d, cx + 62 * math.cos(r), cy + 56 * math.sin(r),
              -20 * math.cos(r), -20 * math.sin(r), "", BLUE)
    ctext(d, 495, 250, "一様収縮リング → 適", FT, GREEN)
    # BL: オイラー柱(適)
    dashed(d, 160, 270, 160, 375, LGRAY)
    d.line(vmode(160, 270, 375, 20, "half"), fill=BLUE, width=4, joint="curve")
    pin_support(d, 160, 375, 12); node(d, 160, 270, 5)
    force(d, 160, 255, 0, 18, "", RED)
    ctext(d, 250, 322, "オイラー柱 → 適", FT, GREEN, "lm")
    # BR: 荷重点直下に柱がある骨組(適)
    d.line((430, 300, 560, 300), fill=BLACK, width=4)
    d.line((495, 300, 495, 375), fill=BLACK, width=4)
    pin_support(d, 495, 375, 12)
    force(d, 495, 278, 0, 20, "", RED)
    ctext(d, 495, 392, "直下柱骨組 → 適", FT, GREEN)
    save(im, "s1e3LinearBucklingNG")


# ============================================================
# 初期不整の P-w 曲線が Pcr 漸近線に近づく  s1e3ImperfectionCurve / s1f3Imperfection
# ============================================================
def _imperfection(name):
    im, d = new(); title(d, "初期不整のある柱:P-w曲線が Pcr に漸近")
    ox, oy = 90, 350
    axes(d, ox, oy, 520, 290, "中央たわみ w", "荷重 P")
    Pcr = oy - 235
    # Pcr 漸近線
    dashed(d, ox, Pcr, ox + 500, Pcr, RED)
    ctext(d, ox + 505, Pcr, "Pcr(理想の座屈荷重)", FT, RED, "lm")
    # 理想の真直柱:分岐(垂直→水平分岐)
    d.line((ox, oy, ox, Pcr), fill=GRAY, width=2)
    d.line((ox, Pcr, ox + 210, Pcr), fill=GRAY, width=2)
    ctext(d, ox + 70, Pcr - 16, "理想(a=0)", FT, GRAY)
    # 初期不整 大小2本:w = a P/(Pcr-P)
    for a, col, lab in [(16, BLUE, "初期不整 大"), (7, GREEN, "初期不整 小")]:
        pts = []
        for i in range(0, 97):
            P = (i / 100.0)  # 0..0.96 of Pcr
            w = a * P / (1 - P) if P < 0.98 else 500
            px = ox + w
            py = oy - P * 235
            if px > ox + 500: break
            pts.append((px, py))
        d.line(pts, fill=col, width=3, joint="curve")
        ctext(d, pts[-1][0] + 4, pts[-1][1] + 6, lab, FT, col, "lm")
    ctext(d, 330, 400, "振幅 a が小さいほど理想の座屈に近い", FT, GRAY)
    save(im, name)


# ============================================================
# s1e3Elastica : 座屈後の大変形弾性柱(エラスティカ)+安定な荷重増加
# ============================================================
def elastica():
    im, d = new(); title(d, "エラスティカ:座屈後も安定に荷重が増加")
    # 大きくたわんだ弾性柱の形
    x0, ytop, ybot = 190, 100, 340
    pin_support(d, x0, ybot, 18)
    for amp, col in [(20, LGRAY), (55, GREEN), (95, BLUE)]:
        d.line(vmode(x0, ytop, ybot, amp, "half"), fill=col, width=4, joint="curve")
    node(d, x0, ytop, 6)
    force(d, x0, ytop - 45, 0, 28, "P", RED)
    ctext(d, x0, ybot + 30, "座屈後 大たわみ", FT)
    # 右:P-w 曲線(座屈後も上昇=安定)
    ox, oy = 400, 330
    axes(d, ox, oy, 210, 230, "w", "P")
    d.line((ox, oy, ox, oy - 120), fill=BLUE, width=3)
    node(d, ox, oy - 120, 5); ctext(d, ox + 6, oy - 120, "分岐点", FT, RED, "lm")
    post = curvepts(lambda x: oy - 120 - 70 * (1 - math.exp(-(x - ox) / 90)), ox, ox + 190, 40)
    d.line(post, fill=GREEN, width=3, joint="curve")
    ctext(d, ox + 110, oy - 165, "座屈後も荷重増加", FT, GREEN)
    save(im, "s1e3Elastica")


# ============================================================
# s1e3LogStrain : 単軸棒の伸びと対数ひずみ・コーシー応力(UL法)
# ============================================================
def log_strain():
    im, d = new(); title(d, "UL法:対数ひずみ ln(1+u) とコーシー応力")
    node(d, 110, 150, 6); bar(d, 110, 150, 280, 150, thick=30); node(d, 280, 150, 6)
    dim(d, 110, 118, 280, 118, "初期長さ L", col=GRAY)
    node(d, 110, 260, 6); bar(d, 110, 260, 440, 260, thick=30); node(d, 440, 260, 6)
    dim(d, 110, 228, 440, 228, "現長さ l = L(1+u)", col=GRAY)
    dashed(d, 280, 245, 280, 275, RED)
    force(d, 460, 260, 40, 0, "f", RED)
    ctext(d, 330, 320, "対数ひずみ  ε = ln(l/L) = ln(1+u)", FT)
    ctext(d, 330, 348, "コーシー応力 σ = f / A(現面積)", FT)
    ctext(d, 330, 380, "f = E ln(1+u)   (単位面積 A=1)", FT, GRAY)
    save(im, "s1e3LogStrain")


# ============================================================
# s1e3GeoStiffness : 初期張力(膜/ケーブル)が幾何剛性で安定化
# ============================================================
def geo_stiffness():
    im, d = new(); title(d, "初期張力による幾何剛性で膜/ケーブルが安定化")
    # 上:張力なし → 横力でふにゃふにゃ(大たわみ)
    wall(d, 90, 100, 175, side=1, n=4); wall(d, 570, 100, 175, side=-1, n=4)
    slack = curvepts(lambda x: 138 + 55 * math.sin(math.pi * (x - 90) / 480), 90, 570, 40)
    d.line(slack, fill=GRAY, width=3, joint="curve")
    force(d, 330, 118, 0, 40, "", RED)
    ctext(d, 652, 120, "張力なし\n→大たわむ", FT, GRAY, "rm")
    # 下:初期張力あり → 横力に対し硬い(小たわみ)
    wall(d, 90, 275, 350, side=1, n=4); wall(d, 570, 275, 350, side=-1, n=4)
    ax, ay = 90, 312; bx, by = 570, 312
    stiff = curvepts(lambda x: 312 + 14 * math.sin(math.pi * (x - 90) / 480), 90, 570, 40)
    d.line(stiff, fill=BLUE, width=4, joint="curve")
    force(d, ax + 8, ay, -24, 0, "", GREEN); force(d, bx - 8, by, 24, 0, "", GREEN)
    ctext(d, 330, 282, "初期張力 T", FT, GREEN)
    force(d, 330, 292, 0, 30, "", RED)
    ctext(d, 652, 350, "張力あり\n→硬い(安定)", FT, BLUE, "rm")
    save(im, "s1e3GeoStiffness")


# ============================================================
# 実行
# ============================================================
if __name__ == "__main__":
    # 問題図 s1e3*
    geo_nl_judge()
    beam_large_rot()
    _beck("s1e3FollowerForce", "従動力(follower force):Beckの柱")
    _polar("s1e3PolarDecomp")
    stretch_bar()
    stress_measures()
    truss_uniaxial()
    tl_ul()
    rigid_rot_stress()
    tangent_stiff()
    load_disp_critical()
    _buckle_types("s1e3BucklingTypes")
    _column_bc("s1e3ColumnBC", "境界条件別の座屈モードと係数λ")
    euler_column()
    eigen_buckling()
    linear_buckling_ng()
    _imperfection("s1e3ImperfectionCurve")
    elastica()
    log_strain()
    geo_stiffness()
    # 公式図 s1f3*
    _polar("s1f3PolarDecomp")
    _beck("s1f3FollowerForce", "従動力と荷重剛性(非対称):Beckの柱")
    _column_bc("s1f3EulerBuckle", "オイラー座屈荷重 Pcr と境界条件の係数λ")
    _buckle_types("s1f3BuckleTypes")
    _imperfection("s1f3Imperfection")

    # 検証
    keys = ["s1e3GeoNLJudge","s1e3BeamLargeRot","s1e3FollowerForce","s1e3PolarDecomp",
            "s1e3StretchBar","s1e3StressMeasures","s1e3TrussUniaxial","s1e3TLUL",
            "s1e3RigidRotStress","s1e3TangentStiff","s1e3LoadDispCritical","s1e3BucklingTypes",
            "s1e3ColumnBC","s1e3EulerColumn","s1e3EigenBuckling","s1e3LinearBucklingNG",
            "s1e3ImperfectionCurve","s1e3Elastica","s1e3LogStrain","s1e3GeoStiffness",
            "s1f3PolarDecomp","s1f3FollowerForce","s1f3EulerBuckle","s1f3BuckleTypes","s1f3Imperfection"]
    miss = [k for k in keys if not os.path.exists(os.path.join(OUT, k + ".png"))]
    print("TOTAL", len(keys), "MISSING", miss)
