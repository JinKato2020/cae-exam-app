# -*- coding: utf-8 -*-
"""熱流体力学1級 第2章「単相流の計算法1」公式・用語図 21枚。figlibで白地660x420線画。"""
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


def fbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ls = text.split("\n")
    for i, line in enumerate(ls):
        ctext(d, cx, cy - (len(ls) - 1) * 10 + i * 20, line, fnt)


# ---- Mach criterion
def f_mach():
    im, d = new()
    title(d, "非圧縮の判定（マッハ数 M=V/a）")
    ox, oy, L = 90, 240, 480
    x03 = ox + int(L * 0.3)
    box(d, ox, oy - 36, x03, oy, (225, 240, 225))
    box(d, x03, oy - 36, ox + L, oy, (245, 228, 228))
    arrow(d, ox, oy, ox + L + 20, oy, BLACK, 2, 11)
    ctext(d, ox + L + 26, oy, "M", FS, BLACK, "lm")
    for m, lab in [(0.0, "0"), (0.3, "0.3"), (1.0, "1.0")]:
        x = ox + int(L * m); d.line((x, oy - 5, x, oy + 5), fill=BLACK, width=2)
        ctext(d, x, oy + 18, lab, FT, BLACK)
    ctext(d, (ox + x03) / 2, oy - 18, "非圧縮でよい", FT, GREEN)
    ctext(d, (x03 + ox + L) / 2, oy - 18, "圧縮性を考慮", FT, RED)
    ctext(d, 330, 300, "密度変化が数％を超える境目 ≒ M0.3", FT, GRAY)
    save(im, "t1f2Mach")


# ---- Sound speed
def f_soundspeed():
    im, d = new()
    title(d, "音速 a=√(γRT)")
    ox, oy = 110, 320
    axes(d, ox, oy, 440, 250, "T", "a")
    pts = []
    for i in range(0, 101):
        T = 200 + i * 4
        a = math.sqrt(1.4 * 287 * T)
        pts.append((ox + i / 100 * 440, oy - (a - 250) / 200 * 250))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, 470, 130, "温度↑で音速↑", FT, BLUE)
    ctext(d, 330, 355, "γ:比熱比, R:気体定数, T:絶対温度", FT, GRAY)
    save(im, "t1f2SoundSpeed")


# ---- FDM
def f_fdm():
    im, d = new()
    title(d, "有限差分法（構造格子・差分商）")
    ox, oy, h = 160, 230, 80
    for i in range(4):
        for j in range(3):
            node(d, ox + i * h, oy - j * h + h, 6, "white", BLACK)
    # highlight 3 points for central diff
    y = oy + h
    for x, lab in [(ox, "i-1"), (ox + h, "i"), (ox + 2 * h, "i+1")]:
        d.ellipse((x - 12, y - 12, x + 12, y + 12), outline=RED, width=3)
        ctext(d, x, y + 24, lab, FT, RED)
    dim(d, ox, y + 50, ox + h, y + 50, "h")
    ctext(d, 470, 200, "∂u/∂x ≈\n(u(i+1)-u(i-1))/2h", FS, BLUE)
    note(d, "格子点上の値の差で微分を近似。構造格子向き")
    save(im, "t1f2FDM")


# ---- FVM
def f_fvm():
    im, d = new()
    title(d, "有限体積法（検査体積・保存則）")
    box(d, 250, 150, 410, 300, FILL1)
    ctext(d, 330, 225, "検査体積", FS, BLACK)
    arrow(d, 190, 225, 250, 225, GREEN, 4, 13); ctext(d, 210, 205, "流入", FT, GREEN)
    arrow(d, 410, 225, 470, 225, GREEN, 4, 13); ctext(d, 450, 205, "流出", FT, GREEN)
    arrow(d, 330, 100, 330, 150, GREEN, 4, 13)
    arrow(d, 330, 300, 330, 350, GREEN, 4, 13)
    note(d, "界面を通る流束の収支＝内部の変化。保存性が高く構造・非構造格子に適用")
    save(im, "t1f2FVM")


# ---- FEM
def f_fem():
    im, d = new()
    title(d, "有限要素法（弱形式・補間）")
    tri = [(200, 300), (420, 300), (310, 150)]
    d.polygon(tri, outline=BLACK, width=3, fill=FILL2)
    for i, p in enumerate(tri):
        node(d, p[0], p[1], 7, ORANGE, BLACK)
        ctext(d, p[0], p[1] + (22 if i < 2 else -22), f"節点{i+1}", FT, BLACK)
    ctext(d, 310, 255, "u=ΣNᵢuᵢ", FS, BLUE)
    note(d, "要素内を節点値と補間関数Nᵢで表す。非構造格子・複雑形状に強い")
    save(im, "t1f2FEM")


# ---- Upwind
def f_upwind():
    im, d = new()
    title(d, "風上差分と数値粘性")
    oy = 220
    arrow(d, 80, oy, 580, oy, BLACK, 2, 11); ctext(d, 586, oy, "x", FS, BLACK, "lm")
    arrow(d, 200, 140, 300, 140, BLUE, 4, 14); ctext(d, 250, 122, "流れ U", FT, BLUE)
    d.line((250, oy - 8, 250, oy - 70), fill=GREEN, width=3)
    d.line((150, oy - 8, 250, oy - 8), fill=GREEN, width=3)
    d.line((250, oy - 70, 300, oy - 70), fill=GREEN, width=3)
    plot(d, 0, 0, [(300, oy - 66), (340, oy - 40), (390, oy - 18), (440, oy - 10)], ORANGE, 3)
    ctext(d, 200, oy - 86, "真の分布", FT, GREEN)
    ctext(d, 420, oy - 34, "数値粘性でなまる", FT, ORANGE)
    note(d, "上流側の値を重く使う→安定化だが数値粘性(Taylor展開で評価)")
    save(im, "t1f2Upwind")


# ---- QUICK / K-K
def f_quickkk():
    im, d = new()
    title(d, "高次精度スキーム")
    fbox(d, 200, 160, 260, 60, "QUICK\n2次精度", (225, 235, 245))
    fbox(d, 200, 280, 260, 60, "Kawamura-Kuwahara\n3次精度", (225, 240, 225))
    ctext(d, 470, 160, "数値粘性を\n低減", FS, BLUE)
    ctext(d, 470, 280, "さらに低減\n(3次)", FS, GREEN)
    note(d, "風上差分を高次化して数値粘性を抑える")
    save(im, "t1f2QuickKK")


# ---- Vortex
def f_vortex():
    im, d = new()
    title(d, "渦法（渦要素・ビオサバール則）")
    for (x, y) in [(200, 200), (260, 240), (320, 190), (380, 250), (440, 210), (300, 300), (400, 310)]:
        d.arc((x - 13, y - 13, x + 13, y + 13), 20, 300, fill=RED, width=3)
    ctext(d, 320, 360, "渦度をもつ粒子を追跡＝ラグランジュ的・非定常", FT, GRAY)
    note(d, "格子不要・移動境界に強い")
    save(im, "t1f2Vortex")


# ---- Particle
def f_particle():
    im, d = new()
    title(d, "粒子法（カーネルの重ね合わせ）")
    cx, cy = 330, 230
    for (x, y) in [(250, 220), (300, 250), (360, 225), (330, 290), (270, 285)]:
        node(d, x, y, 7, FILL1, BLACK)
    for r, c in [(30, LGRAY), (20, (180, 180, 180)), (10, GRAY)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=2)
    ctext(d, 330, 170, "ガウス関数カーネル", FT, GRAY)
    note(d, "離散粒子の相互作用で流れを再現。混相流・自由表面に強い")
    save(im, "t1f2Particle")


# ---- Pressure Poisson
def f_poisson():
    im, d = new()
    title(d, "圧力ポアソン方程式の導出")
    fbox(d, 330, 130, 360, 50, "運動方程式", FILL1)
    arrow(d, 330, 155, 330, 195, BLACK, 2, 11)
    ctext(d, 430, 175, "発散をとる", FT, RED, "lm")
    fbox(d, 330, 225, 360, 50, "＋ 連続の式(∇·u=0)を代入", (225, 240, 225))
    arrow(d, 330, 250, 330, 290, BLACK, 2, 11)
    fbox(d, 330, 320, 360, 50, "∇²p = …（圧力の式）", (225, 235, 245))
    ctext(d, 330, 390, "※回転ではなく『発散』をとる", FT, RED)
    save(im, "t1f2Poisson")


# ---- MAC
def f_mac():
    im, d = new()
    title(d, "MAC法（陽的・非定常向け）")
    fbox(d, 330, 140, 360, 50, "圧力ポアソン方程式→圧力", (225, 235, 245))
    arrow(d, 330, 165, 330, 205, BLACK, 2, 11)
    fbox(d, 330, 235, 360, 50, "圧力＋前ステップ速度→速度\n(陽的に時間積分)", (225, 240, 225), FT)
    arrow(d, 510, 235, 540, 235, BLACK, 2, 11)
    dash(d, 540, 235, 540, 110, GRAY); dash(d, 540, 110, 330, 110, GRAY)
    arrow(d, 330, 110, 330, 115, GRAY, 2, 9)
    ctext(d, 540, 300, "次ステップへ", FT, GRAY)
    save(im, "t1f2MAC")


# ---- SIMPLE
def f_simple():
    im, d = new()
    title(d, "SIMPLE法（圧力補正・定常向け）")
    fbox(d, 330, 130, 360, 46, "速度を推定（陰的）", FILL1)
    arrow(d, 330, 153, 330, 190, BLACK, 2, 11)
    fbox(d, 330, 215, 360, 46, "圧力補正式で圧力・速度を修正", (225, 240, 225))
    arrow(d, 330, 238, 330, 275, BLACK, 2, 11)
    fbox(d, 330, 300, 360, 46, "連続の式を満たすまで反復", (225, 235, 245))
    arrow(d, 510, 300, 545, 300, BLACK, 2, 11)
    dash(d, 545, 300, 545, 130, GRAY); dash(d, 545, 130, 330, 130, GRAY)
    save(im, "t1f2SIMPLE")


# ---- Artificial compressibility
def f_artcomp():
    im, d = new()
    title(d, "人工圧縮性解法")
    fbox(d, 330, 160, 470, 60, "連続の式に擬似時間微分項を付加\n(1/β)∂p/∂τ", (225, 240, 225))
    arrow(d, 330, 190, 330, 235, BLACK, 2, 11)
    fbox(d, 330, 265, 470, 56, "N-S式と連立して定常解へ収束", FILL1)
    note(d, "Chorinの擬似圧縮性法が起源。圧縮性の枠組みで非圧縮を解く")
    save(im, "t1f2ArtComp")


# ---- Low Mach
def f_lowmach():
    im, d = new()
    title(d, "低マッハ数近似（圧力の分離）")
    fbox(d, 175, 150, 230, 56, "熱力学的圧力\n(密度・温度を決める)", (225, 235, 245), FT)
    fbox(d, 485, 150, 230, 56, "運動力学的圧力\n(流れを駆動)", (225, 240, 225), FT)
    fbox(d, 330, 270, 420, 56, "手順: 熱力学的圧力→温度→密度\n→運動力学的圧力→速度", FILL1, FT)
    note(d, "マッハ数は小さいが密度変化が無視できない浮力流れ向け")
    save(im, "t1f2LowMach")


# ---- Laplacian central difference
def f_laplacian():
    im, d = new()
    title(d, "粘性項（ラプラシアン）の中心差分")
    cx, cy, h = 250, 220, 70
    pts = {"0": (0, 0), "1": (1, 0), "3": (0, -1), "5": (-1, 0), "7": (0, 1)}
    for gx, gy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        d.line((cx, cy, cx + gx * h, cy + gy * h), fill=LGRAY, width=2)
    for k, (gx, gy) in pts.items():
        x, y = cx + gx * h, cy + gy * h
        node(d, x, y, 12, FILL1, BLACK); ctext(d, x, y, k, FS, BLACK)
    ctext(d, 480, 200, "(∇²u)₀ =\n((u1+u3+u5+u7)\n  −4u0)/h²", FS, BLUE)
    note(d, "点0が周囲平均より小さいと正(加速)。粘性は物理量を平均化=拡散")
    save(im, "t1f2Laplacian")


# ---- AUSM
def f_ausm():
    im, d = new()
    title(d, "AUSM（流束分離）")
    fbox(d, 330, 130, 220, 46, "界面の流束 F", FILL2)
    arrow(d, 270, 153, 200, 205, BLACK, 2, 11)
    arrow(d, 390, 153, 460, 205, BLACK, 2, 11)
    fbox(d, 190, 240, 200, 46, "対流項", (225, 240, 225))
    fbox(d, 470, 240, 200, 46, "圧力項", (225, 235, 245))
    ctext(d, 330, 240, "＋", F, BLACK)
    note(d, "簡潔・不連続面に強い・堅牢 → 極超音速流れ")
    save(im, "t1f2Ausm")


# ---- Preconditioning
def f_precond():
    im, d = new()
    title(d, "前処理法（波の速さの比をそろえる）")
    ctext(d, 175, 110, "前処理なし(stiff)", FS, RED)
    arrow(d, 90, 160, 300, 160, BLACK, 3, 13); ctext(d, 306, 160, "a", FT, BLACK, "lm")
    arrow(d, 90, 200, 118, 200, BLACK, 3, 11); ctext(d, 124, 200, "u", FT, BLACK, "lm")
    d.line((330, 120, 330, 240), fill=LGRAY, width=2)
    ctext(d, 500, 110, "前処理あり", FS, GREEN)
    arrow(d, 380, 160, 560, 160, BLACK, 3, 12); ctext(d, 566, 160, "a'", FT, BLACK, "lm")
    arrow(d, 380, 200, 545, 200, BLACK, 3, 12); ctext(d, 551, 200, "u", FT, BLACK, "lm")
    note(d, "低マッハでa/uが大→stiff。前処理行列で比をそろえ収束改善(Merkleら)")
    save(im, "t1f2Precond")


# ---- Sutherland
def f_sutherland():
    im, d = new()
    title(d, "サザーランドの式")
    ox, oy = 110, 320
    axes(d, ox, oy, 440, 250, "T", "μ")
    pts = []
    for i in range(0, 101):
        T = 250 + i * 3.0
        mu = (T / 273) ** 1.5 * (273 + 111) / (T + 111)
        py = oy - (mu - 0.8) / 1.2 * 250
        pts.append((ox + i / 100 * 440, min(max(py, oy - 250), oy)))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, 460, 130, "気体:温度↑で\n粘性↑", FT, BLUE)
    ctext(d, 330, 360, "μ/μ₀=(T/T₀)^(3/2)·(T₀+C)/(T+C)", FT, GRAY)
    save(im, "t1f2Sutherland")


# ---- Limiter
def f_limiter():
    im, d = new()
    title(d, "TVDリミッター（minmod）")
    ox, oy, sc = 110, 320, 100
    axes(d, ox, oy, 430, 250, "r", "B")
    dash(d, ox, oy, ox + 100, oy - 200, GRAY); ctext(d, ox + 108, oy - 195, "B=2r", FT, GRAY, "lm")
    dash(d, ox, oy - 2 * sc, ox + 390, oy - 2 * sc, LGRAY); ctext(d, ox + 395, oy - 2 * sc, "B=2", FT, GRAY, "lm")
    node(d, ox + sc, oy - sc, 5, RED, RED); ctext(d, ox + sc + 8, oy - sc - 12, "(1,1)", FT, RED, "lm")
    pts = []
    for i in range(0, 390):
        r = i / sc; B = max(0.0, min(r, 1.0))
        pts.append((ox + i, oy - B * sc))
    plot(d, 0, 0, pts, BLUE, 4)
    ctext(d, ox + 250, oy - sc - 18, "minmod", FS, BLUE)
    note(d, "minmod(散逸的)<Van Leer<Superbee(圧縮的)")
    save(im, "t1f2Limiter")


# ---- MUSCL
def f_muscl():
    im, d = new()
    title(d, "MUSCL法（セル内の傾きを再構築）")
    oy = 250
    for i, x in enumerate([150, 260]):
        v = [110, 150][i]
        d.line((x - 50, oy - v + 130, x + 50, oy - v + 130), fill=GRAY, width=3)
        d.line((x - 55, oy, x + 55, oy), fill=BLACK, width=1)
    ctext(d, 205, 110, "セル平均(1次)", FT, GRAY)
    arrow(d, 330, 160, 375, 160, BLACK, 2, 11)
    for i, x in enumerate([440, 550]):
        v = [110, 150][i]
        d.line((x - 50, oy - v + 130 + 18, x + 50, oy - v + 130 - 18), fill=BLUE, width=3)
        node(d, x + 50, oy - v + 130 - 18, 4, BLUE, BLUE)
    ctext(d, 495, 110, "傾き再構築(高次)", FT, BLUE)
    note(d, "空間高次精度化。TVD化・衝撃波捕獲はリミッター併用。CFLと無関係")
    save(im, "t1f2Muscl")


# ---- Reaction flow
def f_reaction():
    im, d = new()
    title(d, "化学反応流の分類")
    rows = [("平衡流", "tf ≫ tc", (225, 240, 225)),
            ("非平衡流", "tf ≈ tc", (245, 240, 225)),
            ("凍結流", "tf ≪ tc", (245, 228, 228))]
    for i, (name, rel, col) in enumerate(rows):
        y = 130 + i * 80
        box(d, 90, y - 30, 570, y + 30, col)
        ctext(d, 200, y, name, F, BLACK)
        ctext(d, 420, y, rel, F, RED)
    ctext(d, 330, 380, "tf:流通の特性時間, tc:反応の特性時間", FT, GRAY)
    save(im, "t1f2Reaction")


if __name__ == "__main__":
    f_mach(); f_soundspeed(); f_fdm(); f_fvm(); f_fem(); f_upwind(); f_quickkk()
    f_vortex(); f_particle(); f_poisson(); f_mac(); f_simple(); f_artcomp()
    f_lowmach(); f_laplacian(); f_ausm(); f_precond(); f_sutherland()
    f_limiter(); f_muscl(); f_reaction()
    print("done t1f2")
