# -*- coding: utf-8 -*-
"""熱流体1級 第1章「単相流の物理」公式・用語図 22枚 (接頭辞 t1f1)。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# 1. t1f1Bernoulli : 損失付きベルヌーイ (傾いた円管+マノメータ,各項ラベル)
def f_bernoulli():
    im, d = new(); title(d, "ベルヌーイの式(損失付き): 各項のエネルギー")
    # 傾いた管
    ax, ay, bx, by = 110, 320, 540, 150
    bar(d, ax, ay, bx, by, thick=44, fill=FILL1)
    node(d, ax, ay, 6); node(d, bx, by, 6)
    ctext(d, ax-14, ay+22, "A", F); ctext(d, bx+16, by-20, "B", F)
    arrow(d, 150, 300, 210, 276, BLUE, 4, 14)
    ctext(d, 190, 258, "V", FS, BLUE)
    # 高さ差
    d.line((bx+70, ay, bx+70, by), fill=LGRAY, width=1)
    dim(d, bx+70, ay, bx+70, by, "z (高さ)", col=GRAY)
    # 各項ラベル
    ctext(d, 300, 372, "(1/2)V^2 : 運動 |  p/rho : 圧力 |  gz : 位置", FS)
    note(d, "A->B: エネルギー一定 + 損失 E_l (摩擦で下流へ)")
    save(im, "t1f1Bernoulli")


# 2. t1f1Friction : 管摩擦損失 (円管+長さL,径d,V, 壁摩擦)
def f_friction():
    im, d = new(); title(d, "管摩擦損失: E_l=lambda(L/d)(V^2/2)")
    x0, x1, yc, r = 120, 560, 220, 46
    d.rectangle((x0, yc-r, x1, yc+r), outline=BLACK, width=3)
    # 流速プロファイル
    for k in range(-3, 4):
        yy = yc + k*11
        f = 1 - (k/3.3)**2
        arrow(d, x0+18, yy, x0+18+int(70*f), yy, BLUE, 2, 8)
    ctext(d, x0+55, yc-r-14, "V", FS, BLUE)
    # 壁摩擦
    for xx in range(x0+40, x1-20, 55):
        arrow(d, xx+30, yc-r-6, xx, yc-r-6, RED, 2, 8)
        arrow(d, xx, yc+r+6, xx+30, yc+r+6, RED, 2, 8)
    ctext(d, x1-70, yc-r-20, "壁摩擦 tau_w", FT, RED)
    dim(d, x0, yc+r+40, x1, yc+r+40, "L (管長)")
    dim(d, x1+28, yc-r, x1+28, yc+r, "d (径)")
    note(d, "長い・細い・速い ほど損失大 / lambda=管摩擦係数(Re,粗さ)")
    save(im, "t1f1Friction")


# 3. t1f1Vorticity : 渦度 (せん断流で回る流体粒子)
def f_vorticity():
    im, d = new(); title(d, "渦度 zeta = du/dy - dv/dx (回転の強さ)")
    axes(d, 120, 340, 420, 250, "u (速度)", "y")
    # せん断速度プロファイル u=ay
    for k in range(0, 6):
        yy = 340 - k*45
        ln = 30 + k*55
        arrow(d, 120, yy, 120+ln, yy, BLUE, 2, 9)
    ctext(d, 360, 130, "u = a y", FS, BLUE)
    # 回転する小要素
    cx, cy = 430, 250
    d.ellipse((cx-30, cy-30, cx+30, cy+30), outline=GRAY, width=2)
    d.rectangle((cx-16, cy-16, cx+16, cy+16), outline=BLACK, width=2)
    for a in (60, 240):
        ar = math.radians(a)
        arrow(d, cx+34*math.cos(ar), cy-34*math.sin(ar),
              cx+34*math.cos(ar+0.9), cy-34*math.sin(ar+0.9), RED, 3, 11)
    ctext(d, cx, cy+52, "流体要素が回る", FT, RED)
    note(d, "上下で速度差 -> 要素が回転 / zeta=0 は渦なし流れ")
    save(im, "t1f1Vorticity")


# 4. t1f1VorticityTransport : 渦度輸送方程式 (移流+拡散の概念)
def f_vorticity_transport():
    im, d = new(); title(d, "渦度輸送方程式: 移流 + 粘性拡散")
    # 導出の流れ (箱)
    boxes = [("N-S 2本\n(運動方程式)", 130, 130), ("連続の式", 130, 250)]
    for t, x, y in boxes:
        d.rectangle((x-80, y-34, x+80, y+34), outline=BLACK, width=2, fill=FILL1)
        ctext(d, x, y, t, FT)
    d.rectangle((360-95, 190-40, 360+95, 190+40), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 360, 178, "圧力項を消去", FS); ctext(d, 360, 202, "-> zeta の式", FS)
    arrow(d, 210, 140, 265, 178); arrow(d, 210, 244, 265, 206)
    # 右: 移流と拡散のイメージ
    cx, cy = 545, 300
    arrow(d, 470, cy, 545, cy, BLUE, 3, 12); ctext(d, 505, cy-16, "移流", FT, BLUE)
    for rr in (14, 26, 38):
        d.ellipse((cx-rr, cy-rr, cx+rr, cy+rr), outline=GRAY, width=2)
    ctext(d, cx, cy+52, "粘性で拡散", FT, GREEN)
    ctext(d, 360, 300, "d(zeta)/dt + u dzeta/dx + v dzeta/dy", FT)
    ctext(d, 360, 322, "= (mu/rho) lap(zeta)", FT)
    note(d, "圧力を扱わず流れを計算できるのが利点")
    save(im, "t1f1VorticityTransport")


# 5. t1f1StreamFunction : 流れ関数と渦度-流れ関数法 (等psi線=流線 + 反復ループ)
def f_stream_function():
    im, d = new(); title(d, "流れ関数 psi: 等psi線 = 流線")
    # 等psi線(流線)群
    ox, oy = 90, 240
    for k, off in enumerate([-70, -35, 0, 35, 70]):
        pts = []
        for i in range(0, 61):
            xx = ox + i*4.0
            yy = oy + off + 40*math.sin(i/60*math.pi)
            pts.append((xx, yy))
        plot(d, 0, 0, pts, BLUE if off == 0 else GRAY, 3 if off == 0 else 2)
    ctext(d, 300, 120, "psi = 一定 の線", FS, BLUE)
    ctext(d, 300, 340, "u=dpsi/dy,  v=-dpsi/dx,  zeta=-lap(psi)", FT)
    # 反復ループ
    d.arc((470, 366, 610, 406), 0, 360, fill=GREEN, width=2)
    ctext(d, 540, 386, "zeta<->psi 反復", FT, GREEN)
    note(d, "渦度-流れ関数法: 連続の式を自動満足・2D非圧縮に多用")
    save(im, "t1f1StreamFunction")


# 6. t1f1Buckingham : バッキンガムのπ定理 (n量-m単位 -> n-m個のπ)
def f_buckingham():
    im, d = new(); title(d, "バッキンガムのpi定理: n量, m単位 -> (n-m)個のpi")
    d.rectangle((70, 120, 250, 300), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 160, 150, "物理量 n 個", FS)
    ctext(d, 160, 200, "基本単位 m 個", FS)
    ctext(d, 160, 250, "(長さ・質量・時間)", FT, GRAY)
    arrow(d, 265, 210, 400, 210, BLACK, 4, 15)
    ctext(d, 332, 188, "次元解析", FT)
    d.rectangle((410, 120, 600, 300), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 505, 165, "無次元数", FS)
    ctext(d, 505, 205, "pi_1 ... pi_(n-m)", FS)
    ctext(d, 505, 250, "phi(pi_1,..)=0", FS)
    note(d, "変数を m 個減らせる / 例: a,K,rho(n=3),単位3 -> pi 1個")
    save(im, "t1f1Buckingham")


# 7. t1f1SoundSpeed : 液体中の音速 (圧力波が管を伝わる, K/rho)
def f_sound_speed():
    im, d = new(); title(d, "液体中の音速 a = sqrt(K/rho)")
    x0, x1, yc, r = 90, 590, 210, 50
    d.rectangle((x0, yc-r, x1, yc+r), outline=BLACK, width=3)
    # 圧縮波面
    for wx in (230, 300, 370):
        d.line((wx, yc-r, wx, yc+r), fill=GRAY, width=2)
    d.line((190, yc-r, 190, yc+r), fill=RED, width=4)
    arrow(d, 200, yc, 300, yc, RED, 4, 14)
    ctext(d, 250, yc-r-16, "圧力波 a", FS, RED)
    ctext(d, 300, yc+r+38, "K 大(縮みにくい)ほど速い / rho 大ほど遅い", FT)
    ctext(d, 300, 360, "水: K~2.2e9, rho~1000 -> a~1500 m/s", FT, GRAY)
    save(im, "t1f1SoundSpeed")


# 8. t1f1Reynolds : レイノルズ数 (慣性力 vs 粘性力 / 層流-乱流遷移)
def f_reynolds():
    im, d = new(); title(d, "レイノルズ数 Re = rho V L / mu (慣性/粘性)")
    # 平板上の遷移
    hwall(d, 90, 590, 300, side=1, n=14)
    ctext(d, 90, 316, "前縁", FT, GRAY)
    # 層流部
    for xx in range(120, 300, 30):
        arrow(d, xx, 250, xx+22, 250, BLUE, 2, 8)
    ctext(d, 200, 150, "層流 (Re小)", FS, BLUE)
    # 乱流部
    for xx in range(320, 560, 26):
        yy = 250 + int(14*math.sin(xx/13.0))
        arrow(d, xx, yy, xx+20, 250+int(14*math.sin((xx+20)/13.0)), RED, 2, 7)
    ctext(d, 460, 150, "乱流 (Re大)", FS, RED)
    arrow(d, 300, 190, 340, 190, GRAY, 2, 9); ctext(d, 320, 172, "遷移", FT, GRAY)
    note(d, "Re_x=u_inf x/nu : 下流ほど大きく乱流化しやすい")
    save(im, "t1f1Reynolds")


# 9. t1f1Prandtl : プランドル数 (速度境界層 vs 温度境界層の厚さ比)
def f_prandtl():
    im, d = new(); title(d, "プランドル数 Pr = nu/alpha (運動量/熱の伝わり)")
    hwall(d, 90, 590, 330, side=1, n=14)
    # 速度境界層(青) 温度境界層(赤)
    pv = [(120+i*8, 330 - int(90*(1-math.exp(-i/9.0)))) for i in range(0, 56)]
    pt = [(120+i*8, 330 - int(45*(1-math.exp(-i/9.0)))) for i in range(0, 56)]
    plot(d, 0, 0, pv, BLUE, 3); plot(d, 0, 0, pt, RED, 3)
    ctext(d, 470, 232, "delta (速度)", FT, BLUE)
    ctext(d, 470, 300, "delta_T (温度)", FT, RED)
    ctext(d, 300, 120, "Pr>1: 温度境界層が薄い (水 Pr~7)", FT)
    ctext(d, 300, 150, "Pr<1: 逆 (空気 Pr~0.7, 液体金属で小)", FT, GRAY)
    save(im, "t1f1Prandtl")


# 10. t1f1Nusselt : ヌセルト数 (対流 vs 伝導のみ, 温度勾配)
def f_nusselt():
    im, d = new(); title(d, "ヌセルト数 Nu = h x / lambda (対流/伝導)")
    hwall(d, 90, 590, 330, side=1, n=14)
    ctext(d, 300, 356, "加熱壁", FT, RED)
    # 対流(流れ矢印)
    for xx in range(140, 520, 40):
        arrow(d, xx, 250, xx+26, 250, BLUE, 2, 9)
    ctext(d, 300, 150, "対流で熱を運ぶ (h)", FS, BLUE)
    # 壁の温度勾配
    arrow(d, 560, 330, 560, 210, RED, 3, 12); ctext(d, 575, 260, "T", FS, RED)
    ctext(d, 300, 190, "静止流体の伝導(lambda)と比較 -> Nu", FT)
    note(d, "平板強制対流: Nu_x=f(Re_x,Pr), 例 0.332 Re^1/2 Pr^1/3")
    save(im, "t1f1Nusselt")


# 11. t1f1Grashof : グラスホフ数 (加熱鉛直壁の浮力上昇流)
def f_grashof():
    im, d = new(); title(d, "グラスホフ数 Gr = g beta dT L^3 / nu^2 (浮力/粘性)")
    wall(d, 150, 90, 360, side=1, n=12)
    ctext(d, 128, 225, "加熱壁", FT, RED)
    # 上昇流プロファイル
    prof = [(170+int(70*math.exp(-abs(k)/3.0)*(1 if k >= 0 else 0.4)),
             360 - (k+2)*0) for k in range(0)]
    for yy in range(120, 350, 26):
        f = math.exp(-(yy-235)**2/9000)
        arrow(d, 165, yy, 165+int(80*(0.4+0.6*f)), yy, GRAY, 1, 6)
    # 上向き浮力
    for xx in (200, 240, 280):
        arrow(d, xx, 350, xx, 130, RED, 3, 12)
    ctext(d, 360, 160, "浮力で上昇流", FS, RED)
    dim(d, 470, 120, 470, 360, "L")
    note(d, "dT 大 -> Gr 大 -> 上昇流が強い (自然対流のRe役)")
    save(im, "t1f1Grashof")


# 12. t1f1Mach : マッハ数 (亜音速/音速/超音速とマッハコーン)
def f_mach():
    im, d = new(); title(d, "マッハ数 M = V/a (圧縮性の強さ)")
    ys = [130, 220, 310]
    labs = ["M<1 亜音速", "M=1 音速(臨界)", "M>1 超音速"]
    cols = [BLUE, ORANGE, RED]
    for y, lab, col in zip(ys, labs, cols):
        src = 160
        for r in (18, 40, 62):
            off = 0 if y == 220 else (-r if y == 130 else r*0.9)
            d.ellipse((src+off-r, y-r, src+off+r, y+r), outline=col, width=2)
        arrow(d, 100, y, 150, y, col, 3, 11)
        ctext(d, 360, y, lab, FS, col)
    # マッハコーン (超音速)
    d.line((160, 310, 300, 250), fill=RED, width=2)
    d.line((160, 310, 300, 370), fill=RED, width=2)
    note(d, "M<<1 は非圧縮扱い / M大で密度変化が効く")
    save(im, "t1f1Mach")


# 13. t1f1Reynolds handled; 13. t1f1LogLaw : 壁法則と対数則 (u+ - y+ 分布)
def f_log_law():
    im, d = new(); title(d, "壁法則と対数則 (u+ vs y+)")
    ox, oy = 130, 350
    axes(d, ox, oy, 430, 270, "y+ (対数)", "u+")
    # 粘性底層 u+=y+ (直線, 小y+)
    lin = [(ox+i*3, oy - i*3) for i in range(0, 34)]
    plot(d, 0, 0, lin, BLUE, 3)
    ctext(d, ox+120, oy-70, "u+=y+ (壁近傍)", FT, BLUE)
    # 対数則 (曲線)
    logp = []
    for i in range(34, 145):
        yp = i*3
        u = (oy) - int((1/0.41*math.log(i*0.7)+5.0)*7)
        logp.append((ox+yp, u))
    plot(d, 0, 0, logp, RED, 3)
    ctext(d, ox+300, oy-150, "u+=(1/kappa)ln y+ + B", FT, RED)
    ctext(d, 300, 388, "kappa~0.41, B~5.0 / u+=U/u_tau, y+=y u_tau/nu", FT, GRAY)
    save(im, "t1f1LogLaw")


# 14. t1f1FrictionVelocity : 摩擦速度とレイノルズ応力 (壁近くでピーク)
def f_friction_velocity():
    im, d = new(); title(d, "摩擦速度 u_tau=sqrt(tau_w/rho), レイノルズ応力")
    hwall(d, 90, 590, 340, side=1, n=14); ctext(d, 90, 364, "壁", FT, GRAY)
    # 壁面せん断応力
    arrow(d, 130, 340, 210, 340, RED, 4, 14); ctext(d, 200, 322, "tau_w", FS, RED)
    # レイノルズ応力 -rho u'v' の分布(壁近くでピーク)
    ox, oy = 320, 340
    axes(d, ox, oy, 240, 250, "-rho u'v'", "y")
    pts = []
    for k in range(0, 50):
        yy = oy - k*5
        val = 150*math.exp(-((k-6)/9.0)**2)
        pts.append((ox+int(val), yy))
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox+150, oy-70, "壁近くで最大", FT, BLUE)
    note(d, "-u'v'/u_tau^2 ~ 1 (1より遥かに大きくならない)")
    save(im, "t1f1FrictionVelocity")


# 15. t1f1Separation : 境界層のはく離 (逆圧力勾配で速度勾配0->剥離)
def f_separation():
    im, d = new(); title(d, "境界層のはく離 (逆圧力勾配)")
    # 曲面壁
    surf = [(90+i*5, 330 + int(60*math.sin(i/34.0*math.pi*0.9))) for i in range(0, 96)]
    plot(d, 0, 0, surf, BLACK, 3)
    # 圧力上昇の向き
    arrow(d, 150, 120, 520, 120, GRAY, 2, 11)
    ctext(d, 340, 100, "逆圧力勾配 (下流ほど圧力高)", FT, GRAY)
    # 速度プロファイル: 付着->勾配0->逆流
    for xx, sc, back in [(180, 1.0, 0), (330, 0.5, 0), (470, 0.15, 0), (560, -0.3, 1)]:
        base = 330 + int(60*math.sin((xx-90)/5/34.0*math.pi*0.9))
        for k in range(1, 7):
            yy = base - k*12
            ln = int((28)*sc*(k/6.0))
            col = RED if back else BLUE
            arrow(d, xx, yy, xx+ln, yy, col, 2, 6)
    ctext(d, 460, 250, "はく離点\n(壁面速度勾配=0)", FT, RED)
    node(d, 470, 330 + int(60*math.sin((470-90)/5/34.0*math.pi*0.9)), 5, fill=RED, col=RED)
    note(d, "以降は逆流・損失急増 / 翼で失速の原因")
    save(im, "t1f1Separation")


# 16. t1f1RotatingStall : 旋回失速とサージング (翼列伝播 + 右上がり特性)
def f_rotating_stall():
    im, d = new(); title(d, "旋回失速 と サージング")
    # 左: 翼列の失速セル伝播
    cx, cy = 175, 240
    d.ellipse((cx-90, cy-90, cx+90, cy+90), outline=BLACK, width=2)
    for a in range(0, 360, 45):
        ar = math.radians(a)
        bx, by = cx+70*math.cos(ar), cy-70*math.sin(ar)
        d.line((bx-14*math.cos(ar+0.6), by+14*math.sin(ar+0.6),
                bx+14*math.cos(ar+0.6), by-14*math.sin(ar+0.6)), fill=BLACK, width=3)
    # 失速セル
    ar = math.radians(90)
    d.ellipse((cx+55*math.cos(ar)-16, cy-55*math.sin(ar)-16,
               cx+55*math.cos(ar)+16, cy-55*math.sin(ar)+16), outline=RED, width=3)
    angle_arc(d, cx, cy, 105, 60, 130, "伝播 30-70%", RED)
    ctext(d, cx, cy+118, "旋回失速: 失速域が伝播", FT)
    # 右: 揚程曲線 (右上がりで不安定)
    ox, oy = 370, 350
    axes(d, ox, oy, 230, 250, "Q (流量)", "h (揚程)")
    curve = [(ox+i*4, oy-120 - int(40*math.sin(i/57.0*math.pi))) for i in range(0, 57)]
    plot(d, 0, 0, curve, BLUE, 3)
    ctext(d, ox+60, oy-230, "beta>0 右上がり\n=不安定(サージング)", FT, RED)
    ctext(d, ox+170, oy-120, "beta<0 安定", FT, GREEN)
    save(im, "t1f1RotatingStall")


# 17. t1f1Boussinesq : ブシネ近似 (浮力項だけ密度変化, 他は一定)
def f_boussinesq():
    im, d = new(); title(d, "ブシネ近似: 密度変化は浮力項だけ")
    # 運動方程式の項イメージ
    d.rectangle((80, 130, 590, 210), outline=BLACK, width=2, fill=FILL1)
    ctext(d, 335, 158, "運動方程式 (Navier-Stokes)", FS)
    ctext(d, 200, 190, "慣性・粘性: rho=一定", FT, GRAY)
    d.rectangle((360, 176, 500, 204), outline=RED, width=3)
    ctext(d, 430, 190, "浮力項: rho(T)", FT, RED)
    # 暖気上昇のイメージ
    hwall(d, 120, 550, 360, side=-1, n=12); ctext(d, 335, 380, "床(加熱)", FT, RED)
    for xx in (220, 320, 420):
        arrow(d, xx, 355, xx, 250, RED, 3, 12)
    ctext(d, 335, 235, "暖まった空気が軽く上昇", FT, RED)
    note(d, "圧縮性を厳密に扱わず自然対流を計算 / 支配数=Gr")
    save(im, "t1f1Boussinesq")


# 18. t1f1WaterHammer : 水撃 (弁急閉で圧力上昇 P1=rho c U1)
def f_water_hammer():
    im, d = new(); title(d, "水撃(ジューコフスキー): P1 = rho c U1")
    x0, x1, yc, r = 90, 520, 220, 44
    d.rectangle((x0, yc-r, x1, yc+r), outline=BLACK, width=3)
    # 弁(急閉)
    d.rectangle((x1, yc-r-6, x1+16, yc+r+6), outline=BLACK, width=3, fill=FILL3)
    ctext(d, x1+8, yc+r+26, "弁 急閉 (u=0)", FT)
    # 流入
    arrow(d, x0+20, yc, x0+90, yc, BLUE, 4, 14); ctext(d, x0+55, yc-r-14, "U1", FS, BLUE)
    # 圧力上昇波が上流へ伝播
    d.line((380, yc-r, 380, yc+r), fill=RED, width=5)
    arrow(d, 375, yc, 300, yc, RED, 4, 14); ctext(d, 340, yc-r-16, "圧力波 c", FS, RED)
    ctext(d, 300, 330, "急な圧力上昇 P1 = rho c U1", FS)
    note(d, "流速・音速が大きいほど圧力上昇大 / 特性曲線法で導出")
    save(im, "t1f1WaterHammer")


# 19. t1f1MOC : 特性曲線法とリーマン不変量 (x-t面 C+ C-)
def f_moc():
    im, d = new(); title(d, "特性曲線法: C+ / C- 上で不変量一定")
    axes(d, 120, 350, 430, 270, "x", "t")
    ox, oy = 120, 350
    # C+ 特性線群 (右上がり)
    for x0 in range(160, 420, 60):
        d.line((x0, oy, x0+180, oy-230), fill=BLUE, width=2)
    # C- 特性線群 (左上がり)
    for x0 in range(260, 520, 60):
        d.line((x0, oy, x0-180, oy-230), fill=RED, width=2)
    ctext(d, 470, 150, "C+: dx/dt=u+c", FT, BLUE)
    ctext(d, 200, 150, "C-: dx/dt=u-c", FT, RED)
    ctext(d, 300, 388, "C+ 上 p+rho c u 一定 / C- 上 p-rho c u 一定", FT)
    save(im, "t1f1MOC")


# 20. t1f1Lorentz : MHD とローレンツ力 (j x B, フレミング左手)
def f_lorentz():
    im, d = new(); title(d, "MHD: ローレンツ力 F_L = j x B")
    cx, cy = 320, 230
    # 電流 j (右) , 磁場 B (上), 力 F (奥/上向き)
    arrow(d, cx, cy, cx+150, cy, RED, 4, 15); ctext(d, cx+165, cy, "j (電流)", FS, RED, "lm")
    arrow(d, cx, cy, cx, cy-140, BLUE, 4, 15); ctext(d, cx, cy-160, "B (磁場)", FS, BLUE)
    arrow(d, cx, cy, cx-110, cy+90, GREEN, 4, 15); ctext(d, cx-120, cy+108, "F_L (力)", FS, GREEN, "rm")
    node(d, cx, cy, 6)
    ctext(d, 300, 380, "導電性流体 x 電磁場 (マルチフィジックス) / N-Sに体積力として加える", FT, GRAY)
    save(im, "t1f1Lorentz")


# 21. t1f1Isentropic : 等エントロピー関係と臨界圧力比 (p/p0 vs M)
def f_isentropic():
    im, d = new(); title(d, "等エントロピー関係 と 臨界圧力比")
    ox, oy = 130, 350
    axes(d, ox, oy, 420, 270, "M (マッハ数)", "p/p0")
    # p/p0 = (1+(g-1)/2 M^2)^(-g/(g-1)), g=1.4 ; p0点 M=0 -> 1
    g = 1.4
    pts = []
    for i in range(0, 220):
        M = i/100.0
        ratio = (1+(g-1)/2*M*M)**(-g/(g-1))
        pts.append((ox+int(M*180), oy-int(ratio*240)))
    plot(d, 0, 0, pts, BLUE, 3)
    # 臨界点 M=1, ~0.528
    mx = ox+int(1.0*180); my = oy-int(0.528*240)
    d.line((mx, oy, mx, my), fill=LGRAY, width=1)
    d.line((ox, my, mx, my), fill=LGRAY, width=1)
    node(d, mx, my, 5, fill=RED, col=RED)
    ctext(d, mx+10, my-16, "M=1: p*/p0~0.528", FT, RED)
    ctext(d, 300, 388, "空気 g=1.4 / 背圧が臨界比以下でのどがチョーク", FT, GRAY)
    save(im, "t1f1Isentropic")


# 22. t1f1Nozzle : 準1次元ノズルの面積-速度関係 (先細末広ラバル)
def f_nozzle():
    im, d = new(); title(d, "ラバルノズル: du/u = 1/(M^2-1) dA/A")
    # 先細末広ノズル形状
    yc = 240
    upper = [(120, yc-90), (300, yc-34), (360, yc-34), (560, yc-120)]
    lower = [(120, yc+90), (300, yc+34), (360, yc+34), (560, yc+120)]
    d.line(upper, fill=BLACK, width=3, joint="curve")
    d.line(lower, fill=BLACK, width=3, joint="curve")
    # のど
    d.line((330, yc-34, 330, yc+34), fill=LGRAY, width=1)
    ctext(d, 330, yc+58, "のど M=1", FT, RED)
    # 流れ加速
    arrow(d, 150, yc, 220, yc, BLUE, 3, 11)
    arrow(d, 400, yc, 520, yc, RED, 4, 15)
    ctext(d, 200, yc-70, "亜音速 M<1\n絞ると加速", FT, BLUE)
    ctext(d, 470, yc-80, "超音速 M>1\n広げて加速", FT, RED)
    note(d, "M<1: dA<0で加速・温度低下 / M>1: dA>0で加速")
    save(im, "t1f1Nozzle")


if __name__ == "__main__":
    f_bernoulli(); f_friction(); f_vorticity(); f_vorticity_transport()
    f_stream_function(); f_buckingham(); f_sound_speed(); f_reynolds()
    f_prandtl(); f_nusselt(); f_grashof(); f_mach(); f_log_law()
    f_friction_velocity(); f_separation(); f_rotating_stall(); f_boussinesq()
    f_water_hammer(); f_moc(); f_lorentz(); f_isentropic(); f_nozzle()
    print("DONE")
