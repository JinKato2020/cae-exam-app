# -*- coding: utf-8 -*-
"""熱流体力学1級 第2章「単相流の計算法1」問題図 14枚。figlibで白地660x420線画。"""
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


def flowbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    for i, line in enumerate(text.split("\n")):
        ctext(d, cx, cy - (len(text.split("\n")) - 1) * 10 + i * 20, line, fnt)


# -------------------------------------------------- 2-1 圧縮性判定(マッハ数)
def f_compress():
    im, d = new()
    title(d, "圧縮性を無視できる範囲（マッハ数）")
    ox, oy, L = 90, 250, 480
    x03 = ox + int(L * 0.3)
    box(d, ox, oy - 40, x03, oy, (225, 240, 225))
    box(d, x03, oy - 40, ox + L, oy, (245, 228, 228))
    arrow(d, ox, oy, ox + L + 20, oy, BLACK, 2, 11)
    ctext(d, ox + L + 26, oy, "M", FS, BLACK, "lm")
    for m, lab in [(0.0, "0"), (0.3, "0.3"), (0.6, "0.6"), (1.0, "1.0")]:
        x = ox + int(L * m)
        d.line((x, oy - 5, x, oy + 5), fill=BLACK, width=2)
        ctext(d, x, oy + 18, lab, FT, BLACK)
    d.line((x03, oy - 60, x03, oy + 5), fill=RED, width=2)
    ctext(d, (ox + x03) / 2, oy - 20, "非圧縮でよい", FS, GREEN)
    ctext(d, (x03 + ox + L) / 2, oy - 20, "圧縮性を考慮", FS, RED)
    ctext(d, x03, oy - 72, "M=0.3 が目安", FT, RED)
    note(d, "M=V/a。ただし温度差が大きいと低マッハでも密度変化を考慮（低マッハ数近似）")
    save(im, "t1e2Compress")


# -------------------------------------------------- 2-2 離散化三手法
def f_discretize3():
    im, d = new()
    title(d, "離散化の三手法")
    # FDM: grid points
    ctext(d, 140, 95, "有限差分法", FS, BLUE)
    for i in range(4):
        for j in range(3):
            node(d, 80 + i * 40, 150 + j * 40, 5, "white", BLACK)
    ctext(d, 140, 285, "格子点で差分\n(構造格子)", FT, GRAY)
    # FVM: cell + fluxes
    ctext(d, 330, 95, "有限体積法", FS, GREEN)
    box(d, 285, 140, 375, 230, FILL1)
    arrow(d, 260, 185, 285, 185, GREEN, 3, 11)
    arrow(d, 375, 185, 400, 185, GREEN, 3, 11)
    arrow(d, 330, 115, 330, 140, GREEN, 3, 11)
    ctext(d, 330, 185, "検査\n体積", FT, BLACK)
    ctext(d, 330, 285, "保存則を適用\n(界面流束)", FT, GRAY)
    # FEM: element + nodes
    ctext(d, 530, 95, "有限要素法", FS, ORANGE)
    d.polygon([(500, 230), (575, 230), (540, 150)], outline=BLACK, width=2, fill=FILL2)
    for p in [(500, 230), (575, 230), (540, 150)]:
        node(d, p[0], p[1], 5, ORANGE, BLACK)
    ctext(d, 537, 285, "弱形式・補間\n(非構造格子)", FT, GRAY)
    save(im, "t1e2Discretize3")


# -------------------------------------------------- 2-3 風上差分と数値粘性
def f_upwind():
    im, d = new()
    title(d, "風上差分と数値粘性")
    oy = 200
    arrow(d, 70, oy, 590, oy, BLACK, 2, 11)
    ctext(d, 596, oy, "x", FS, BLACK, "lm")
    xs = [120, 200, 280, 360, 440, 520]
    for i, x in enumerate(xs):
        node(d, x, oy, 5, "white", BLACK)
        ctext(d, x, oy + 20, f"i{i-2:+d}".replace("+0", ""), FT, GRAY)
    arrow(d, 250, 130, 330, 130, BLUE, 4, 15)
    ctext(d, 290, 112, "流れ U", FS, BLUE)
    # upwind stencil emphasis
    d.ellipse((280 - 12, oy - 12, 280 + 12, oy + 12), outline=RED, width=3)
    d.ellipse((200 - 12, oy - 12, 200 + 12, oy + 12), outline=RED, width=3)
    ctext(d, 240, oy - 30, "上流側を使う", FT, RED)
    # sharp vs smeared profile
    dash(d, 380, oy - 70, 380, oy - 10, GRAY)
    d.line((360, oy - 10, 380, oy - 10, 380, oy - 70, 400, oy - 70), fill=GREEN, width=3)
    plot(d, 0, 0, [(420, oy - 12), (445, oy - 20), (470, oy - 45), (500, oy - 62), (525, oy - 68)], ORANGE, 3)
    ctext(d, 380, oy - 86, "真の分布", FT, GREEN)
    ctext(d, 500, oy - 82, "数値粘性でなまる", FT, ORANGE)
    note(d, "対流項に導入→安定化するが数値粘性。QUICK(2次)・K-K(3次)で低減")
    save(im, "t1e2Upwind")


# -------------------------------------------------- 2-4 渦法
def f_vortex():
    im, d = new()
    title(d, "渦法（格子レス・渦要素）")
    # airfoil-ish body
    d.polygon([(150, 230), (250, 210), (330, 225), (250, 245)], outline=BLACK, width=3, fill=FILL2)
    ctext(d, 250, 228, "物体", FT, BLACK)
    arrow(d, 60, 200, 120, 200, BLUE, 3, 12)
    ctext(d, 85, 182, "流れ", FT, BLUE)
    # vortex elements (particles with rotation)
    import math as m
    for (x, y) in [(360, 200), (400, 235), (440, 190), (470, 250), (510, 215), (540, 180), (420, 300), (490, 300)]:
        d.arc((x - 12, y - 12, x + 12, y + 12), 20, 300, fill=RED, width=3)
        ax = x + 12 * m.cos(m.radians(300)); ay = y - 12 * m.sin(m.radians(300))
        arrow(d, ax + 6, ay, ax, ay - 2, RED, 2, 7)
    ctext(d, 450, 340, "渦要素（渦度をもつ粒子）を追跡＝ラグランジュ的", FT, GRAY)
    note(d, "格子不要・移動境界に強い・本質的に非定常")
    save(im, "t1e2Vortex")


# -------------------------------------------------- 2-5 粒子法
def f_particle():
    im, d = new()
    title(d, "粒子法（SPH・MPS）")
    # free surface
    plot(d, 0, 0, [(70, 150), (150, 140), (240, 165), (330, 135), (420, 160), (500, 145), (590, 170)], BLUE, 2)
    ctext(d, 120, 128, "自由表面", FT, BLUE)
    # particles
    for (x, y) in [(150, 220), (200, 250), (250, 225), (300, 260), (350, 230), (250, 300), (320, 310), (190, 305)]:
        node(d, x, y, 7, FILL1, BLACK)
    # kernel around one particle
    cx, cy = 250, 225
    for r, c in [(24, LGRAY), (16, (180, 180, 180)), (8, GRAY)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=2)
    ctext(d, 250, 175, "カーネル(ガウス関数)", FT, GRAY)
    arrow(d, 250, 190, 250, 205, GRAY, 2, 8)
    ctext(d, 470, 250, "離散的な粒子の\n相互作用で流れを再現\n→混相流・自由表面に強い", FT, GRAY)
    save(im, "t1e2Particle")


# -------------------------------------------------- 2-6 圧力・速度連成
def f_pressvel():
    im, d = new()
    title(d, "非圧縮流れの圧力・速度連成")
    flowbox(d, 200, 120, 260, 52, "連続の式は時間微分なし\n→圧力を直接解けない", (245, 228, 228))
    arrow(d, 200, 146, 200, 178, BLACK, 2, 11)
    flowbox(d, 200, 210, 260, 52, "圧力ポアソン方程式\n(運動方程式の発散をとる)", (225, 240, 225))
    ctext(d, 200, 250, "※回転ではなく発散", FT, RED)
    arrow(d, 330, 210, 400, 210, BLACK, 2, 11)
    flowbox(d, 500, 150, 230, 46, "MAC法：陽的に速度更新\n(非定常向け)", FILL1)
    flowbox(d, 500, 250, 230, 46, "SIMPLE法：圧力補正\n(定常向け)", FILL1)
    note(d, "圧力を残すため運動方程式の『発散』をとるのが要")
    save(im, "t1e2PressVel")


# -------------------------------------------------- 2-7 低マッハ数近似
def f_lowmach():
    im, d = new()
    title(d, "低マッハ数近似の解析手順")
    steps = ["熱力学的圧力", "温度\n(エネルギー方程式)", "密度\n(状態方程式)", "運動力学的圧力", "速度\n(運動方程式)"]
    ys = [90, 155, 220, 285, 350]
    for i, (s, y) in enumerate(zip(steps, ys)):
        fill = (225, 240, 225) if i in (1, 2) else FILL1
        flowbox(d, 330, y, 300, 50, s, fill)
        if i < 4:
            arrow(d, 330, y + 25, 330, ys[i + 1] - 25, BLACK, 2, 11)
    ctext(d, 560, 187, "密度を先に\n確定してから\n速度へ", FT, RED)
    save(im, "t1e2LowMach")


# -------------------------------------------------- 2-8 9点ステンシル（required・答えを描かない）
def f_stencil():
    im, d = new()
    title(d, "等間隔 h の9点格子")
    cx, cy, h = 330, 220, 90
    pos = {0: (0, 0), 1: (1, 0), 2: (1, -1), 3: (0, -1), 4: (-1, -1),
           5: (-1, 0), 6: (-1, 1), 7: (0, 1), 8: (1, 1)}
    # grid lines
    for gx in (-1, 0, 1):
        d.line((cx + gx * h, cy - h, cx + gx * h, cy + h), fill=LGRAY, width=1)
    for gy in (-1, 0, 1):
        d.line((cx - h, cy + gy * h, cx + h, cy + gy * h), fill=LGRAY, width=1)
    for k, (gx, gy) in pos.items():
        x, y = cx + gx * h, cy + gy * h
        node(d, x, y, 11, FILL1 if k else (255, 236, 236), BLACK)
        ctext(d, x, y, str(k), FS, BLACK)
    # spacing h dims
    dim(d, cx, cy + h + 34, cx + h, cy + h + 34, "h")
    dim(d, cx - h - 34, cy, cx - h - 34, cy - h, "h")
    axes(d, 120, 360, 90, 90, "x", "y")
    note(d, "中央=0、右=1・右上=2・上=3・左上=4・左=5・左下=6・下=7・右下=8")
    save(im, "t1e2Stencil")


# -------------------------------------------------- 2-9 AUSM
def f_ausm():
    im, d = new()
    title(d, "AUSM：流束の分離")
    flowbox(d, 330, 130, 300, 52, "界面の流束 F", FILL2)
    arrow(d, 250, 156, 180, 210, BLACK, 2, 11)
    arrow(d, 410, 156, 480, 210, BLACK, 2, 11)
    flowbox(d, 175, 245, 210, 54, "対流項\n(質量・運動量・\nエネルギーを運ぶ)", (225, 240, 225), FT)
    flowbox(d, 490, 245, 210, 54, "圧力項\n(界面に働く圧力)", (225, 235, 245), FT)
    ctext(d, 330, 245, "＋", F, BLACK)
    note(d, "式が簡潔・不連続面に強い・堅牢 → 極超音速流れに有効")
    save(im, "t1e2Ausm")


# -------------------------------------------------- 2-10 前処理法
def f_precond():
    im, d = new()
    title(d, "低マッハ数の剛直性と前処理法")
    # before: very different speeds
    ctext(d, 175, 95, "低マッハ数（前処理なし）", FS, RED)
    arrow(d, 90, 150, 300, 150, BLACK, 3, 13)
    ctext(d, 310, 150, "音速 a", FT, BLACK, "lm")
    arrow(d, 90, 195, 120, 195, BLACK, 3, 11)
    ctext(d, 130, 195, "対流速度 u", FT, BLACK, "lm")
    ctext(d, 175, 235, "a/u が大 → stiff（収束困難）", FT, RED)
    d.line((330, 110, 330, 250), fill=LGRAY, width=2)
    # after: balanced
    ctext(d, 500, 95, "前処理あり", FS, GREEN)
    arrow(d, 380, 150, 560, 150, BLACK, 3, 12)
    ctext(d, 566, 150, "a'", FT, BLACK, "lm")
    arrow(d, 380, 195, 540, 195, BLACK, 3, 12)
    ctext(d, 546, 195, "u", FT, BLACK, "lm")
    ctext(d, 480, 235, "比をそろえる（前処理行列）", FT, GREEN)
    note(d, "Chorin=擬似圧縮性法／Merkleら=前処理行列で滑らかに移行する前処理法")
    save(im, "t1e2Precond")


# -------------------------------------------------- 2-11 サザーランドの式
def f_sutherland():
    im, d = new()
    title(d, "サザーランドの式：粘性の温度依存")
    ox, oy = 100, 330
    axes(d, ox, oy, 470, 250, "T", "μ")
    pts = []
    for i in range(0, 101):
        T = 250 + i * 3.0
        mu = (T / 273) ** 1.5 * (273 + 111) / (T + 111)
        px = ox + (T - 250) / 300 * 470
        py = oy - (mu - 0.8) / 1.2 * 250
        pts.append((px, min(max(py, oy - 250), oy)))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, 470, 120, "温度↑で粘性↑\n(気体)", FT, BLUE)
    ctext(d, 300, 360, "μ/μ₀=(T/T₀)^(3/2)·(T₀+C)/(T+C)", FT, GRAY)
    save(im, "t1e2Sutherland")


# -------------------------------------------------- 2-12 リミッター
def f_limiter():
    im, d = new()
    title(d, "流束制限関数（リミッター）")
    ox, oy = 110, 330
    axes(d, ox, oy, 440, 250, "r", "B")
    sc = 110  # 1 unit
    # B=2r and B=2 and B=1 references
    dash(d, ox, oy, ox + 110, oy - 220, GRAY)
    ctext(d, ox + 118, oy - 210, "B=2r", FT, GRAY, "lm")
    dash(d, ox, oy - 2 * sc, ox + 400, oy - 2 * sc, LGRAY)
    ctext(d, ox + 405, oy - 2 * sc, "B=2", FT, GRAY, "lm")
    # TVD region shade edge
    node(d, ox + sc, oy - sc, 5, RED, RED)
    ctext(d, ox + sc + 10, oy - sc - 12, "(1,1)", FT, RED, "lm")
    # minmod curve: B=max(0,min(r,1))
    pts = []
    for i in range(0, 400):
        r = i / sc
        B = max(0.0, min(r, 1.0))
        pts.append((ox + i, oy - B * sc))
    plot(d, 0, 0, pts, BLUE, 4)
    ctext(d, ox + 300, oy - sc - 20, "minmod: B=max(0,min(r,1))", FT, BLUE)
    note(d, "単調性: 0≤B≤2 かつ B≤2r。(1,1)通過で広く2次精度")
    save(im, "t1e2Limiter")


# -------------------------------------------------- 2-13 MUSCL法
def f_muscl():
    im, d = new()
    title(d, "MUSCL法：セル内分布の再構築")
    oy = 250
    xs = [120, 240, 360, 480]
    vals = [150, 200, 130, 210]
    # left: piecewise constant (cell averages)
    ctext(d, 180, 100, "セル平均（1次）", FS, GRAY)
    for i, x in enumerate(xs[:2]):
        d.line((x - 55, oy - (vals[i] - 130), x + 55, oy - (vals[i] - 130)), fill=GRAY, width=3)
        d.line((x - 60, oy, x + 60, oy), fill=BLACK, width=1)
        dash(d, x - 60, oy, x - 60, oy - 90, LGRAY)
    # arrow
    arrow(d, 300, 150, 340, 150, BLACK, 2, 11)
    # right: reconstructed slopes
    ctext(d, 430, 100, "傾きを再構築（高次）", FS, BLUE)
    for i, x in enumerate(xs[2:], start=2):
        v = vals[i] - 130
        d.line((x - 55, oy - v + 22, x + 55, oy - v - 22), fill=BLUE, width=3)
        node(d, x + 55, oy - v - 22, 4, BLUE, BLUE)
        ctext(d, x + 60, oy - v - 34, "界面値", FT, BLUE, "lm")
    note(d, "空間の高次精度化。TVD化・衝撃波捕獲はリミッター併用。CFLとは無関係")
    save(im, "t1e2Muscl")


# -------------------------------------------------- 2-14 化学反応流の分類
def f_reaction():
    im, d = new()
    title(d, "化学反応流の分類（tf と tc の比）")
    rows = [("平衡流", "tf ≫ tc", "反応が速く各点で完了", (225, 240, 225)),
            ("非平衡流", "tf ≈ tc", "反応が流れに追いつかない", (245, 240, 225)),
            ("凍結流", "tf ≪ tc", "反応が進まず組成固定", (245, 228, 228))]
    for i, (name, rel, desc, col) in enumerate(rows):
        y = 120 + i * 85
        box(d, 70, y - 32, 590, y + 32, col)
        ctext(d, 150, y, name, F, BLACK)
        ctext(d, 320, y, rel, F, RED)
        ctext(d, 480, y, desc, FT, GRAY)
    ctext(d, 330, 385, "tf=流通の特性時間, tc=反応の特性時間", FT, GRAY)
    save(im, "t1e2Reaction")


if __name__ == "__main__":
    f_compress(); f_discretize3(); f_upwind(); f_vortex(); f_particle()
    f_pressvel(); f_lowmach(); f_stencil(); f_ausm(); f_precond()
    f_sutherland(); f_limiter(); f_muscl(); f_reaction()
    print("done t1e2")
