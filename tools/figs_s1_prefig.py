# -*- coding: utf-8 -*-
"""固体1級 計算問題の「回答前(preFigureImage)」配置図。
白地660x420・黒線画・与件(配置/寸法/荷重)のみ。答え・正解値・結論は一切描かない(=required相当)。
既存の figureImage(解説図/答え示唆あり)は回答後(helpful)のまま残し、本図を回答前に出す(前後2図)。
JSON配線は別途。ここでは assets/figures/<key>.png を生成するのみ。
[[cae-figure-before-after-rule]] 厳命D の横展開(固体2級→固体1級)。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def f_thermal_yield():   # 2-15
    im, d = new(); title(d, "両端を固定した部材を一様加熱(降伏する温度 T を求める)")
    x0, x1, ym, th = 185, 480, 205, 48
    wall(d, x0, ym - 60, ym + 60, side=-1)   # 左壁(外=左にハッチ)
    wall(d, x1, ym - 60, ym + 60, side=1)    # 右壁(外=右にハッチ)
    d.rectangle((x0, ym - th / 2, x1, ym + th / 2), outline=BLACK, width=3, fill=FILL1)
    ctext(d, (x0 + x1) / 2, ym, "加熱  0℃ → T", F, RED)
    ctext(d, x0 - 8, ym - 78, "剛体壁で固定", FT, GRAY, "lm")
    note(d, "与件: E=200 GPa, α=1×10⁻⁵/℃, 降伏応力 σy=300−0.3T (MPa)。この部材が降伏する温度 T は?")
    save(im, "s1e2ThermalYieldSetup")


def f_penalty():         # 4-8
    im, d = new(); title(d, "直列ばね＋接触(ペナルティ法)：節点3の変位 u₃ を求める")
    y = 215
    wall(d, 95, y - 42, y + 42, side=-1)
    node(d, 110, y); ctext(d, 110, y - 30, "節点1(固定)", FT)
    spring(d, 110, y, 250, y); ctext(d, 180, y - 28, "K₁", FS)
    node(d, 250, y); ctext(d, 250, y + 28, "節点2", FT)
    # 接触界面(節点2と3が接触)
    node(d, 305, y); ctext(d, 305, y + 28, "節点3", FT)
    d.line((278, y - 34, 278, y + 34), fill=GRAY, width=2)
    ctext(d, 278, y - 48, "接触", FT, GRAY)
    ctext(d, 278, y + 50, "ペナルティ α", FT, GRAY)
    spring(d, 305, y, 445, y); ctext(d, 375, y - 28, "K₂", FS)
    node(d, 445, y)
    force(d, 445, y, 62, 0, "F", RED)
    note(d, "与件: K₁=K₂=100 N/mm, F=200 N, ペナルティ係数 α=1000 N/mm。節点3の変位 u₃ は?")
    save(im, "s1e4PenaltySetup")


def _plate_crack(d, cx, cy, w, h, crack, sig, cap):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), outline=BLACK, width=3, fill=FILL1)
    d.line((cx - crack / 2, cy, cx + crack / 2, cy), fill=BLACK, width=5)  # 中央き裂
    arrow(d, cx, cy - h / 2, cx, cy - h / 2 - 34, RED, 3, 12)
    arrow(d, cx, cy + h / 2, cx, cy + h / 2 + 34, RED, 3, 12)
    ctext(d, cx, cy - h / 2 - 48, sig, FS, RED)
    ctext(d, cx, cy + h / 2 + 50, cap, FT)


def f_similitude():      # 5-6
    im, d = new(); title(d, "幾何相似な大小のき裂板(大型が破壊する応力 σ₂ を求める)")
    _plate_crack(d, 165, 210, 78, 96, 34, "σ₁", "小型: き裂 a")
    _plate_crack(d, 460, 210, 150, 178, 100, "σ₂=?", "大型: き裂 3a(寸法3倍)")
    note(d, "与件: 幾何相似(全寸法3倍)・同一材料・形状補正 Y 共通。小型は σ₁=120 MPa で破壊。大型の σ₂ は?")
    save(im, "s1e5SimilitudeSetup")


def f_energyKI():        # 5-23
    im, d = new(); title(d, "対称半分モデルでエネルギー解放率 G と KI を求める")
    x0, x1, yt, yb = 175, 495, 130, 300
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3, fill=FILL1)
    acx = x0 + 130
    d.line((x0, yb, acx, yb), fill=RED, width=5)      # き裂 a(自由面)
    hwall(d, acx, x1, yb, side=1)                     # 対称面(拘束)
    ctext(d, (x0 + acx) / 2, yb + 30, "き裂 a(自由)", FT, RED)
    ctext(d, (acx + x1) / 2, yb + 30, "対称面(拘束)", FT, GRAY)
    arrow(d, acx, yb - 16, acx + 34, yb - 16, BLUE, 2, 10)
    ctext(d, acx + 44, yb - 16, "Δa", FT, BLUE, "lm")
    for i in range(4):
        xx = x0 + 22 + i * 30
        arrow(d, xx, yb, xx, yb - 32, RED, 2, 9)
    ctext(d, x0 + 55, yb - 48, "節点荷重 P", FT, RED)
    note(d, "与件: Σ(P·Δv)=0.40 J, Δa=1.0×10⁻⁴ m, 平面応力 E=200 GPa。G=Σ(P·Δv)/Δa, KI=√(E′G) (E′=E)。")
    save(im, "s1e5EnergyKISetup")


def f_radshield():       # 7-18
    im, d = new(); title(d, "平行2面に放射シールド1枚を挿入(挿入後の伝熱量 Q* を求める)")
    y0, y1 = 135, 300
    d.rectangle((150, y0, 166, y1), outline=BLACK, width=3, fill=FILL2); ctext(d, 158, y0 - 16, "面1 T₁", FS, RED)
    d.rectangle((322, y0, 332, y1), outline=BLACK, width=3, fill=FILL1); ctext(d, 327, y0 - 16, "薄板(シールド)", FT)
    d.rectangle((490, y0, 506, y1), outline=BLACK, width=3, fill=FILL2); ctext(d, 498, y0 - 16, "面2 T₂", FS, BLUE)
    for yy in (175, 218, 261):
        arrow(d, 168, yy, 320, yy, ORANGE, 2, 10)
        arrow(d, 334, yy, 488, yy, ORANGE, 2, 10)
    ctext(d, 158, y1 + 18, "放射率 ε", FT); ctext(d, 327, y1 + 18, "ε", FT); ctext(d, 498, y1 + 18, "ε", FT)
    note(d, "与件: T₁>T₂・放射率はすべて ε で等しい。シールド無しの伝熱量 Q=600 W/m²。1枚挿入後の Q* は?")
    save(im, "s1e7RadShieldSetup")


def f_viewfactor():      # 7-19
    im, d = new(); title(d, "向かい合う2黒体面の形態係数 F₂₁ を求める(相反則)")
    d.rectangle((150, 130, 166, 320), outline=BLACK, width=3, fill=FILL2); ctext(d, 175, 112, "面1 A₁=4 m²", FT, BLACK, "lm")
    d.rectangle((494, 175, 510, 275), outline=BLACK, width=3, fill=FILL2); ctext(d, 485, 157, "面2 A₂=2 m²", FT, BLACK, "rm")
    for yy in (185, 220, 255):
        arrow(d, 168, yy, 492, yy, GRAY, 2, 10)
    ctext(d, 330, 150, "Q₁₂=300 W", FS)
    ctext(d, 158, 334, "E₁=500 W/m²", FT)
    note(d, "与件: A₁=4 m², A₂=2 m², E₁=500 W/m², 面1→面2 到達 Q₁₂=300 W。相反則 A₁F₁₂=A₂F₂₁。F₂₁ は?")
    save(im, "s1e7ViewFactorSetup")


def f_disk():            # 10-2
    im, d = new(); title(d, "外周固定・一様圧力を受ける円板の崩壊荷重 p_c を求める(軸対称断面)")
    ym, t, xL, xR = 235, 30, 155, 470
    d.line((xL, 120, xL, 330), fill=GRAY, width=2); ctext(d, xL, 108, "対称軸", FT, GRAY)
    d.rectangle((xL, ym - t / 2, xR, ym + t / 2), outline=BLACK, width=3, fill=FILL1)
    wall(d, xR, ym - 46, ym + 46, side=1); ctext(d, xR + 24, ym, "固定", FT, GRAY, "lm")
    for i in range(7):
        xx = xL + 28 + i * 44
        arrow(d, xx, ym - t / 2 - 32, xx, ym - t / 2, BLUE, 2, 10)
    ctext(d, (xL + xR) / 2, ym - t / 2 - 46, "一様圧力 p", FS, BLUE)
    dim(d, xL, ym + 72, xR, ym + 72, "半径 a=250 mm")
    ctext(d, xL + 66, ym + t / 2 + 18, "板厚 t=25 mm", FT, GRAY, "lm")
    note(d, "与件: t=25 mm, a=250 mm, 降伏点 S_y=255 MPa。M₀=S_y t²/4, p_c=2.08·6M₀/a²。p_c は?")
    save(im, "s1e10DiskCollapseSetup")


def f_platebuckle():     # 10-6
    im, d = new(); title(d, "四辺単純支持板の一方向圧縮座屈(対称条件の影響を調べる)")
    x0, x1, y0, y1 = 150, 510, 155, 285
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    for yy in (y0 + 32, (y0 + y1) // 2, y1 - 32):
        arrow(d, x0 - 42, yy, x0, yy, RED, 3, 12)
        arrow(d, x1 + 42, yy, x1, yy, RED, 3, 12)
    ctext(d, (x0 + x1) // 2, y0 - 16, "四辺単純支持", FT)
    ctext(d, x0 - 48, y0 + 10, "圧縮", FT, RED, "rm")
    xm = (x0 + x1) // 2
    for yy in range(y0, y1, 12):
        d.line((xm, yy, xm, yy + 6), fill=BLUE, width=2)
    ctext(d, xm, y1 + 16, "x=a/2 に対称条件", FT, BLUE)
    dim(d, x0, y1 + 42, x1, y1 + 42, "a")
    dim(d, x1 + 60, y0, x1 + 60, y1, "b")
    ctext(d, (x0 + x1) // 2, y1 + 62, "アスペクト比 a/b=2", FT, GRAY)
    note(d, "与件: a/b=2・四辺単純支持・一方向圧縮。k=(mb/a+a/mb)², Pₓ=k·π²D/b。対称条件下のFEM値は理論値(m=2)の何倍?")
    save(im, "s1e10PlateBuckleSetup")


def f_creep():           # 10-7
    im, d = new(); title(d, "内圧を受ける厚肉円筒の定常クリープ(内面の σθ(a) を求める)")
    cx, cy, ra, rb = 300, 215, 62, 132
    d.ellipse((cx - rb, cy - rb, cx + rb, cy + rb), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((cx - ra, cy - ra, cx + ra, cy + ra), outline=BLACK, width=3, fill="white")
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        arrow(d, cx + 12 * math.cos(a), cy - 12 * math.sin(a),
              cx + (ra - 4) * math.cos(a), cy - (ra - 4) * math.sin(a), BLUE, 2, 8)
    ctext(d, cx, cy, "p", F, BLUE)
    a1 = math.radians(35)
    arrow(d, cx, cy, cx + ra * math.cos(a1), cy - ra * math.sin(a1), GRAY, 2, 8)
    ctext(d, cx + (ra + 14) * math.cos(a1), cy - (ra + 14) * math.sin(a1), "a", FT, GRAY)
    a2 = math.radians(-30)
    arrow(d, cx, cy, cx + rb * math.cos(a2), cy - rb * math.sin(a2), GRAY, 2, 8)
    ctext(d, cx + (rb + 14) * math.cos(a2), cy - (rb + 14) * math.sin(a2), "b", FT, GRAY)
    ctext(d, cx + rb + 40, cy, "内半径 a\n外半径 b", FT, GRAY, "lm")
    note(d, "与件: b/a=2・内圧 p=100 MPa・ノルトン則 dε/dt=kσⁿ (n=3)・平面ひずみ。内面 r=a の周方向応力 σθ(a) は?")
    save(im, "s1e10CreepRedistSetup")


if __name__ == "__main__":
    f_thermal_yield()
    f_penalty()
    f_similitude()
    f_energyKI()
    f_radshield()
    f_viewfactor()
    f_disk()
    f_platebuckle()
    f_creep()
    print("done: 9 preFigureImage for solid1")
