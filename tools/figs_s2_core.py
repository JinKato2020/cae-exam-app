# -*- coding: utf-8 -*-
"""固体2級 核心図の清書(②)。承認済み画風=ネイビー基調＋淡い塗りNAVYL＋薄い目盛＋AA(figlibのSSで自動)。
生成元が消失していた核心図を、内容は現行どおりに保ちつつ見やすく新規作成する。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def _dash(d, x1, y1, x2, y2, col=GRAY, w=2, dl=9, gp=6):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        a = min(t + dl, L)
        d.line((x1 + ux*t, y1 + uy*t, x1 + ux*a, y1 + uy*a), fill=col, width=w)
        t += dl + gp


def s2PrincipalMohr():
    # 平面応力 σx=60, σy=20, τ=15 → 中心40・半径25・σ1=65,σ2=15・θp≈18.4°
    im, d = new()
    title(d, "平面応力の主応力：モールの応力円")
    ox, oy = 150, 232          # 原点(σ=0, τ=0)
    s = 5.0                    # 5px/MPa
    cx = ox + int(40*s)        # 円中心 σ=40
    R = int(25*s)
    # --- 薄い目盛線 ---
    for sv in (0, 20, 40, 60):
        x = ox + int(sv*s)
        d.line((x, oy-2, x, oy+2), fill=GRAY, width=1)
    # --- 円(淡い塗り＋ネイビー枠) ---
    d.ellipse((cx-R, oy-R, cx+R, oy+R), outline=NAVY, width=3, fill=NAVYL)
    # --- 座標軸 ---
    arrow(d, ox, oy, ox+360, oy, BLACK, 2, 11); ctext(d, ox+366, oy, "σ (MPa)", FS, BLACK, "lm")
    arrow(d, ox, oy, ox, oy-150, BLACK, 2, 11); ctext(d, ox-12, oy-158, "τ", FS, BLACK, "mm")
    # --- 点 X(60,15), Y(20,-15), 中心, σ1, σ2 ---
    X = (ox+int(60*s), oy-int(15*s)); Y = (ox+int(20*s), oy+int(15*s))
    d.line((X[0], X[1], Y[0], Y[1]), fill=NAVY, width=2)      # 直径 XY
    s1 = (ox+int(65*s), oy); s2 = (ox+int(15*s), oy)
    # 2θp 角(中心で σ軸から X方向)
    angle_arc(d, cx, oy, 46, 0, math.degrees(math.atan2(15, 20)), "2θp", GRAY)
    node(d, cx, oy, 5, fill=BLACK)
    node(d, s1[0], s1[1], 6, fill=RED, col=RED); ctext(d, s1[0]+4, oy+20, "σ₁=65", FT, RED, "mm")
    node(d, s2[0], s2[1], 6, fill=GREEN, col=GREEN); ctext(d, s2[0]-4, oy+20, "σ₂=15", FT, GREEN, "mm")
    node(d, X[0], X[1], 6, fill=NAVY, col=NAVY); ctext(d, X[0]+14, X[1]-6, "X(σx,τ)=(60,15)", FT, NAVY, "lm")
    node(d, Y[0], Y[1], 6, fill=NAVY, col=NAVY); ctext(d, Y[0]-14, Y[1]+8, "Y(σy,−τ)=(20,−15)", FT, NAVY, "rm")
    ctext(d, cx-34, oy-16, "中心", FT, GRAY)
    note(d, "中心40・半径25 → σ₁=65, σ₂=15。 tan2θp=30/40 → θp≈18.4°")
    save(im, "s2PrincipalMohr")


def _mises_pts(cx, cy, sc, step=4):
    pts = []
    for k in range(0, 361, step):
        f = math.radians(k)
        r = 1.0 / math.sqrt(1 - 0.5*math.sin(2*f))
        pts.append((cx + r*math.cos(f)*sc, cy - r*math.sin(f)*sc))
    return pts


def s2YieldSurface():
    im, d = new(); title(d, "降伏条件の比較 (σ₃=0 面)")
    cx, cy, sc = 262, 216, 104
    def P(a, b): return (cx + a*sc, cy - b*sc)
    arrow(d, cx-168, cy, cx+150, cy, BLACK, 2, 11); ctext(d, cx+156, cy, "σ₁", FS, BLACK, "lm")
    arrow(d, cx, cy+162, cx, cy-162, BLACK, 2, 11); ctext(d, cx+14, cy-160, "σ₂", FS, BLACK, "mm")
    # 最大主応力説(赤破線 正方形)
    sq = [P(1,1), P(-1,1), P(-1,-1), P(1,-1), P(1,1)]
    for i in range(4): _dash(d, sq[i][0], sq[i][1], sq[i+1][0], sq[i+1][1], RED, 2)
    # トレスカ六角(緑)
    hexv = [P(1,0), P(1,1), P(0,1), P(-1,0), P(-1,-1), P(0,-1), P(1,0)]
    d.line(hexv, fill=GREEN, width=2, joint="curve")
    # ミーゼス楕円(ネイビー)
    d.line(_mises_pts(cx, cy, sc), fill=NAVY, width=4, joint="curve")
    # 凡例(右)
    lx, ly = 466, 150
    def leg(y, col, txt, dash=False, w=4):
        if dash: _dash(d, lx, y, lx+34, y, col, 3)
        else: d.line((lx, y, lx+34, y), fill=col, width=w)
        ctext(d, lx+42, y, txt, FT, col, "lm")
    leg(ly, NAVY, "ミーゼス(楕円)")
    leg(ly+32, GREEN, "トレスカ(六角)", w=2)
    leg(ly+64, RED, "最大主応力説(正方)", dash=True)
    note(d, "単軸引張では3説が一致(σ=σy)。純せん断はトレスカ0.5σy<ミーゼス0.577σyで先に降伏")
    save(im, "s2YieldSurface")


def stresstransform():
    im, d = new(); title(d, "応力の座標変換(要素と回転軸 r, s)")
    L = 148; cx, cy = 300, 214
    x0, y0, x1, y1 = cx-L//2, cy-L//2, cx+L//2, cy+L//2
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=FILL1)
    arrow(d, x0-56, cy, x0-6, cy, BLUE, 3, 12); ctext(d, x0-62, cy, "σx", FS, BLUE, "rm")
    arrow(d, x1+56, cy, x1+6, cy, BLUE, 3, 12); ctext(d, x1+62, cy, "σx", FS, BLUE, "lm")
    arrow(d, cx, y0-56, cx, y0-6, BLUE, 3, 12); ctext(d, cx, y0-66, "σy", FS, BLUE, "mm")
    arrow(d, cx, y1+56, cx, y1+6, BLUE, 3, 12); ctext(d, cx, y1+66, "σy", FS, BLUE, "mm")
    arrow(d, x0+22, y0-13, x1-22, y0-13, GRAY, 2, 10); ctext(d, x1+4, y0-13, "τxy", FT, GRAY, "lm")
    # 回転軸 r(45°), s(135°) を中心から
    rr = 96
    for ang, lab in [(45, "r"), (135, "s")]:
        ex = cx + rr*math.cos(math.radians(ang)); ey = cy - rr*math.sin(math.radians(ang))
        arrow(d, cx, cy, ex, ey, RED, 2, 11)
        ctext(d, ex + (10 if ang < 90 else -10), ey-4, lab, FS, RED, "mm")
    angle_arc(d, cx, cy, 42, 0, 45, "θ=45°", RED)
    node(d, cx, cy, 4, fill=BLACK)
    note(d, "座標軸を角θだけ回すと σx,σy,τxy から σr,σs,τrs に変換される(θ=45°の例)")
    save(im, "stresstransform")


def s2MisesJudge():
    im, d = new(); title(d, "ミーゼス降伏判定 (σy=300MPa)")
    cx, cy, sc = 278, 214, 104
    def P(a, b): return (cx + a*sc, cy - b*sc)
    # 楕円(淡い塗り＋ネイビー枠)
    d.polygon(_mises_pts(cx, cy, sc), fill=NAVYL)
    d.line(_mises_pts(cx, cy, sc), fill=NAVY, width=4, joint="curve")
    arrow(d, cx-166, cy, cx+150, cy, BLACK, 2, 11); ctext(d, cx+156, cy, "σ₁", FS, BLACK, "lm")
    arrow(d, cx, cy+162, cx, cy-162, BLACK, 2, 11); ctext(d, cx+14, cy-160, "σ₂", FS, BLACK, "mm")
    for lab, (a, b), col in [("①",(0.55,0.15),GREEN), ("②",(-0.35,0.25),GREEN),
                             ("③",(0.9,-0.7),RED), ("④",(-0.9,0.62),RED)]:
        x, y = P(a, b); node(d, x, y, 6, fill=col, col=col); ctext(d, x+13, y-11, lab, FS, col, "lm")
    note(d, "楕円の内=安全 / 外=降伏。 ①②=安全(内側)・③④=降伏(外側)")
    save(im, "s2MisesJudge")


def s2Truss2Bar():
    im, d = new(); title(d, "荷重を吊る2部材トラス(節点法)")
    hwall(d, 120, 470, 102, side=1)
    C = (316, 244)
    A = (96, 104); B = (398, 104)          # 部材1=浅い(30°)/部材2=急(60°)
    d.line((A[0], A[1], C[0], C[1]), fill=BLACK, width=5)
    d.line((B[0], B[1], C[0], C[1]), fill=BLACK, width=5)
    ctext(d, 150, 172, "部材1", FT, NAVY)
    ctext(d, 404, 168, "部材2", FT, NAVY)
    ctext(d, C[0]-34, C[1]-14, "30°", FT, GRAY)
    ctext(d, C[0]+30, C[1]-14, "60°", FT, GRAY)
    node(d, C[0], C[1], 7); ctext(d, C[0]+16, C[1]+2, "C", FT, BLACK, "lm")
    arrow(d, C[0], C[1]+8, C[0], C[1]+72, RED, 4, 14); ctext(d, C[0]+14, C[1]+66, "W", F, RED, "lm")
    note(d, "節点Cで水平・鉛直の釣合い → S₁=W/2, S₂=(√3/2)W(両方とも引張)")
    save(im, "s2Truss2Bar")


def s2CantileverUDL():
    im, d = new(); title(d, "片持ちはり＋等分布荷重(断面位置は自由端から測る)")
    bx0, bx1, by = 110, 500, 238
    d.rectangle((bx0, by-8, bx1, by+8), outline=BLACK, width=3, fill=FILL1)
    wall(d, bx1+2, by-46, by+46, side=1)
    ctext(d, bx1+26, by, "固定端", FT, GRAY, "lm")
    ctext(d, bx0-6, by, "自由端", FT, GRAY, "rm")
    d.line((bx0+12, by-64, bx1-10, by-64), fill=RED, width=2)
    for x in range(bx0+12, bx1-6, 38):
        arrow(d, x, by-64, x, by-12, RED, 2, 9)
    ctext(d, (bx0+bx1)//2, by-80, "w = 3 kN/m", FS, RED)
    secx = bx0 + 300
    _dash(d, secx, by+10, secx, by+70, GREEN)
    dim(d, bx0, by+92, secx, by+92, "自由端から x = 3 m")
    note(d, "固定端からでなく自由端から測る。 M = w·x²/2 = 3·3²/2 = 13.5 kN·m")
    save(im, "s2CantileverUDL")


def s2TwoBarsThermal():
    im, d = new(); title(d, "剛体板結合の2棒：棒2のみ昇温したときの変位")
    hwall(d, 180, 460, 110, side=1)
    b1x, b2x, topy, platey = 258, 392, 112, 262
    d.rectangle((b1x-7, topy, b1x+7, platey), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((b2x-7, topy, b2x+7, platey), outline=BLACK, width=3, fill=(255, 232, 232))
    d.rectangle((214, platey, 436, platey+22), outline=BLACK, width=3, fill=FILL3)
    ctext(d, b1x-26, 182, "棒1", FT, BLACK, "rm"); ctext(d, b1x-26, 202, "常温", FT, GRAY, "rm")
    ctext(d, b2x+26, 182, "棒2", FT, RED, "lm"); ctext(d, b2x+26, 202, "ΔT=80K", FT, RED, "lm")
    arrow(d, 325, platey+32, 325, platey+74, BLUE, 3, 13); ctext(d, 340, platey+54, "uT", FS, BLUE, "lm")
    note(d, "外力なし・板は水平のまま下降。 uT = αΔT·L/2 = 0.24 mm(棒1が半分引き戻す)")
    save(im, "s2TwoBarsThermal")


def s2OverhangBeam():
    im, d = new(); title(d, "突出しはりの支点反力(A・C支持、C右へ張出し)")
    y = 196; A = 96; sc = 108
    x10 = A + sc; C = A + 2*sc; xR = A + 3*sc
    d.rectangle((A, y-7, xR, y+7), outline=BLACK, width=3, fill=FILL1)
    pin_support(d, A, y+7, 20); roller_support(d, C, y+7, 20)
    ctext(d, A, y-28, "A(x=0)", FT, BLACK); ctext(d, C, y-28, "C(x=4)", FT, BLACK)
    force(d, x10, y-6, 0, 58, "10kN", RED); force(d, xR, y-6, 0, 58, "6kN", RED)
    dim(d, A, y+84, x10, y+84, "2m"); dim(d, C, y+84, xR, y+84, "2m")
    dim(d, x10, y+112, C, y+112, "2m")
    note(d, "ΣM_A=0: R_C·4 = 10·2 + 6·6 = 56 → R_C=14kN, R_A=2kN")
    save(im, "s2OverhangBeam")


def s2CantReactions():
    im, d = new(); title(d, "片持ちはりの固定端反力と固定モーメント")
    y = 206; x0 = 134; x1 = 498
    d.rectangle((x0, y-7, x1, y+7), outline=BLACK, width=3, fill=FILL1)
    wall(d, x1+2, y-46, y+46, side=1); ctext(d, x1+28, y-40, "D固定", FT, GRAY, "lm")
    d.line((x0, y-62, x1-6, y-62), fill=ORANGE, width=2)
    for x in range(x0, x1-4, 42): arrow(d, x, y-62, x, y-12, ORANGE, 2, 9)
    ctext(d, (x0+x1)//2, y-78, "w = 2 kN/m", FT, ORANGE)
    force(d, x0, y, 0, 70, "P=5kN", RED)
    arrow(d, x1-8, y+74, x1-8, y+12, BLUE, 3, 13); ctext(d, x1-2, y+58, "R_D", FT, BLUE, "lm")
    _curved_arrow(d, x1-8, y, 36, 205, 100, GREEN, 3); ctext(d, x1-48, y+24, "M_D", FT, GREEN, "rm")
    note(d, "R_D=P+wL=9kN, M_D=PL+wL²/2=10+4=14 kN·m")
    save(im, "s2CantReactions")


def s2SectionZ():
    im, d = new(); title(d, "同一断面積で断面係数Zを最大にする形(曲げ軸まわり)")
    cy = 198; xs = [112, 252, 392, 532]
    _dash(d, 64, cy, 584, cy, GRAY)
    r = 42; d.ellipse((xs[0]-r, cy-r, xs[0]+r, cy+r), outline=BLACK, width=3, fill=FILL1)
    s = 74; d.rectangle((xs[1]-s//2, cy-s//2, xs[1]+s//2, cy+s//2), outline=BLACK, width=3, fill=FILL1)
    ww, hh = 100, 46; d.rectangle((xs[2]-ww//2, cy-hh//2, xs[2]+ww//2, cy+hh//2), outline=BLACK, width=3, fill=FILL1)
    X = xs[3]; fw, ft, wh, we = 74, 13, 56, 16     # I形
    d.rectangle((X-fw//2, cy-wh//2-ft, X+fw//2, cy-wh//2), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((X-we//2, cy-wh//2, X+we//2, cy+wh//2), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((X-fw//2, cy+wh//2, X+fw//2, cy+wh//2+ft), outline=BLACK, width=3, fill=FILL1)
    labs = [("円 Z小", BLACK), ("正方形 Z小", BLACK), ("横長 Z最小", BLACK), ("I形 Z最大", RED)]
    for xc, (t_, c_) in zip(xs, labs): ctext(d, xc, cy+70, t_, FT, c_)
    note(d, "材料を中立軸から遠くへ配置するほど断面二次モーメントI・断面係数Zが大 → I形が有利")
    save(im, "s2SectionZ")


def s2RigidPlate2Bars():
    im, d = new(); title(d, "剛体板を2本の弾性棒で吊る(並列＝伸び等しい)")
    hwall(d, 168, 482, 100, side=1)
    b1x, b2x, topy, platey = 252, 402, 102, 250
    d.rectangle((b1x-13, topy, b1x+13, platey), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((b2x-6, topy, b2x+6, platey), outline=BLACK, width=3, fill=FILL2)
    d.rectangle((208, platey, 446, platey+20), outline=BLACK, width=3, fill=FILL3)
    ctext(d, b1x-28, 165, "棒1", FT, BLACK, "rm"); ctext(d, b1x-28, 220, "A₁(太)", FT, GRAY, "rm")
    ctext(d, b2x+24, 165, "棒2", FT, BLACK, "lm"); ctext(d, b2x+24, 220, "A₂(細)", FT, GRAY, "lm")
    _dash(d, 208, platey+40, 446, platey+40, GRAY)
    force(d, 327, platey+22, 0, 56, "P", RED)
    note(d, "板は水平のまま下降 → 両棒の伸びは等しい。 力は剛性比 k₁:k₂ で配分される")
    save(im, "s2RigidPlate2Bars")


def s2RigidBarWire():
    im, d = new(); title(d, "剛体棒をワイヤで支持：先端変位は伸びの b/a 倍")
    Ax, Ay = 112, 196; sc = 428
    wx = Ax + int(0.5*sc); Rx = Ax + sc            # a=0.5m, b=1.0m
    d.rectangle((Ax, Ay-7, Rx, Ay+7), outline=BLACK, width=3, fill=FILL1)
    pin_support(d, Ax, Ay+7, 20)
    hwall(d, wx-34, wx+34, 96, side=1)
    d.line((wx, 100, wx, Ay-7), fill=BLACK, width=3); ctext(d, wx+10, 140, "ワイヤ", FT, GRAY, "lm")
    _dash(d, Ax, Ay, Rx, Ay+34, GRAY)             # 回転後(誇張)
    force(d, Rx, Ay-4, 0, 52, "P", RED)
    ctext(d, Ax-4, Ay-18, "A", FS, BLACK, "rm")
    dim(d, Ax, Ay+70, wx, Ay+70, "a = 0.5m")
    dim(d, Ax, Ay+100, Rx, Ay+100, "b = 1.0m")
    note(d, "A点まわりに回転 → 先端変位 = (ワイヤ伸びδw)·(b/a)。 てこで拡大される")
    save(im, "s2RigidBarWire")


def s2PlateHoles():
    im, d = new(); title(d, "2つの円孔をもつ平板の引張(正味断面で評価)")
    px0, px1, py0, py1 = 158, 498, 150, 278; cxh = (px0+px1)//2; cyh = (py0+py1)//2
    d.rectangle((px0, py0, px1, py1), outline=BLACK, width=3, fill=FILL1)
    rh = 18
    for yy in (cyh-22, cyh+22):
        d.ellipse((cxh-rh, yy-rh, cxh+rh, yy+rh), outline=BLACK, width=3, fill="white")
    _dash(d, cxh, py0-6, cxh, py1+6, GREEN)
    ctext(d, cxh+54, cyh, "d=20 ×2", FT, GRAY, "lm")
    force(d, px0-6, cyh, -56, 0, "P", RED); force(d, px1+6, cyh, 56, 0, "P", RED)
    dim(d, px0, py1+28, px1, py1+28, "W = 100mm")
    note(d, "正味幅 W−2d=60mm、A_net=600mm²。 P=σ_allow·A_net/Kt=24kN")
    save(im, "s2PlateHoles")


def s2PoissonBar():
    im, d = new(); title(d, "ポアソン比 ν の比較(0.5に近いほど非圧縮)")
    base = 326; x0 = 96; bw = 66; gap = 140; H = 220; maxv = 0.5
    d.line((66, base, 600, base), fill=BLACK, width=2)
    data = [("ゴム", 0.50, True), ("鋼", 0.30, False), ("コンクリート", 0.15, False), ("コルク", 0.02, False)]
    for i, (name, v, hl) in enumerate(data):
        x = x0 + i*gap; h = int(v/maxv*H)
        fill = (223, 242, 228) if hl else NAVYL
        oc = GREEN if hl else NAVY
        d.rectangle((x, base-h, x+bw, base), outline=oc, width=3, fill=fill)
        ctext(d, x+bw//2, base-h-16, f"ν≈{v:.2f}", FT, oc)
        ctext(d, x+bw//2, base+18, name, FT, BLACK)
    note(d, "体積変化 ΔV/V ≈ (1−2ν)ε。 ν→0.5 で体積ほぼ不変＝非圧縮(ゴム)")
    save(im, "s2PoissonBar")


def s2ShearModulus():
    im, d = new(); title(d, "せん断弾性係数 G：せん断応力とせん断ひずみ")
    x0, y0, s, sh = 214, 150, 150, 56
    d.rectangle((x0, y0, x0+s, y0+s), outline=LGRAY, width=2)          # 変形前(淡)
    d.polygon([(x0, y0+s), (x0+s, y0+s), (x0+s+sh, y0), (x0+sh, y0)], outline=NAVY, width=3, fill=NAVYL)
    arrow(d, x0+sh+8, y0-14, x0+s+sh-8, y0-14, RED, 3, 11)
    ctext(d, x0+s//2+sh//2, y0-32, "せん断応力 τ", FS, RED)
    arrow(d, x0+s-8, y0+s+14, x0+8, y0+s+14, RED, 3, 11)
    ctext(d, x0+16, y0+s-42, "γ", FS, GREEN)
    note(d, "G=τ/γ(せん断変形への抵抗)。 等方材では G=E/2(1+ν) で決まる従属量")
    save(im, "s2ShearModulus")


def s2StrainDisp():
    im, d = new(); title(d, "微小要素のひずみと変位")
    x0, y0, s = 206, 158, 138; ex, ey, sh = 30, 24, 20
    d.rectangle((x0, y0, x0+s, y0+s), outline=BLACK, width=3, fill=FILL1)
    dc = [(x0, y0), (x0+s+ex, y0), (x0+s+ex+sh, y0+s+ey), (x0+sh, y0+s+ey)]
    for i in range(4): _dash(d, dc[i][0], dc[i][1], dc[(i+1)%4][0], dc[(i+1)%4][1], RED)
    arrow(d, x0+s, y0, x0+s+ex, y0, BLUE, 2, 9)
    ctext(d, x0+s//2+8, y0-16, "εx (水平の伸び)", FT, RED)
    ctext(d, x0+s+ex+28, y0+s//2+6, "εy (垂直の伸び)", FT, RED, "lm")
    ctext(d, x0+24, y0+s//2, "γxy", FT, GREEN, "lm")
    arrow(d, x0, y0+s, x0+sh, y0+s+ey, BLUE, 2, 9); ctext(d, x0+sh+4, y0+s+ey+2, "v", FT, BLUE, "lm")
    note(d, "実線=変形前 / 破線=変形後。 εx,εy=伸び, γxy=せん断角")
    save(im, "s2StrainDisp")


def _curved_arrow(d, cx, cy, R, a0, a1, col=BLUE, w=4):
    """中心(cx,cy)・半径Rの円弧(a0→a1度, 反時計正・右=0)を描き終端に矢じり。"""
    n = max(2, int(abs(a1 - a0) / 6))
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + R*math.cos(a), cy - R*math.sin(a)))
    d.line(pts, fill=col, width=w, joint="curve")
    ae = math.radians(a1); ex, ey = pts[-1]
    tx, ty = -math.sin(ae), -math.cos(ae)          # 接線(a増加方向, 画像座標)
    if a1 < a0: tx, ty = -tx, -ty
    for s in (0.5, -0.5):
        hx = ex - 14*(math.cos(s)*tx - math.sin(s)*ty)
        hy = ey - 14*(math.sin(s)*tx + math.cos(s)*ty)
        d.line((ex, ey, hx, hy), fill=col, width=w)


def s2HollowShaft():
    im, d = new(); title(d, "中空丸軸のねじり：最大せん断は外表面")
    cx, cy, Ro, Ri = 244, 214, 108, 54
    d.ellipse((cx-Ro, cy-Ro, cx+Ro, cy+Ro), outline=NAVY, width=3, fill=NAVYL)
    d.ellipse((cx-Ri, cy-Ri, cx+Ri, cy+Ri), outline=NAVY, width=3, fill="white")
    for a in (50, 140, 230, 320):                  # 外周に接線方向の赤いせん断矢印
        ar = math.radians(a); px, py = cx+Ro*math.cos(ar), cy-Ro*math.sin(ar)
        tx, ty = math.sin(ar), math.cos(ar)
        arrow(d, px-tx*18, py-ty*18, px+tx*18, py+ty*18, RED, 2, 9)
    _curved_arrow(d, cx, cy, Ro+34, 60, -60, BLUE, 4)   # トルク T
    ctext(d, cx+Ro+52, cy, "T", F, BLUE, "lm")
    dim(d, cx-Ro, cy+Ro+42, cx+Ro, cy+Ro+42, "do = 40")
    dim(d, cx-Ri, cy, cx+Ri, cy, "di = 20")
    note(d, "Zp=π(do⁴−di⁴)/(16·do)。 最大せん断は外表面。 Tmax=τa·Zp ≈ 707 N·m")
    save(im, "s2HollowShaft")


def s2ThinCylinder():
    im, d = new(); title(d, "内圧を受ける薄肉円筒(両端閉じ)")
    cy, R, X0, X1, ew = 196, 74, 170, 466, 22
    d.line((X0, cy-R, X1, cy-R), fill=BLACK, width=3)
    d.line((X0, cy+R, X1, cy+R), fill=BLACK, width=3)
    d.ellipse((X1-ew, cy-R, X1+ew, cy+R), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((X0-ew, cy-R, X0+ew, cy+R), outline=BLACK, width=3, fill=NAVYL)
    mx = 300
    for dx, dy in [(0, -1), (0.9, 0.5), (-0.9, 0.5)]:   # 内圧(放射状)
        arrow(d, mx, cy, mx+int(dx*(ew-4)), cy+int(dy*(R-12)), RED, 3, 11)
    ctext(d, mx, cy+R+16, "内圧 p = 2 MPa", FT, RED)
    dim(d, X0, cy-R-28, X1, cy-R-28, "L = 2 m")
    arrow(d, X0+ew+8, cy, X0+ew+8, cy-R+4, GREEN, 2, 10); ctext(d, X0+ew+14, cy-R//2, "r=0.5m", FT, GREEN, "lm")
    ctext(d, X1+ew+8, cy-R+6, "t=5mm", FT, GRAY, "lm")
    note(d, "E=200GPa, ν=0.3。 円周応力σθ=pd/2t は軸応力σa=pd/4t の2倍。 内容積変化ΔVを問う")
    save(im, "s2ThinCylinder")


def s2ConjugateShear():
    im, d = new(); title(d, "共役せん断応力：モーメントがつり合う配置")
    L = 150; cx, cy = 300, 214
    x0, y0, x1, y1 = cx-L//2, cy-L//2, cx+L//2, cy+L//2
    d.rectangle((x0, y0, x1, y1), outline=NAVY, width=3, fill=NAVYL)
    arrow(d, x0+16, y0-12, x1-16, y0-12, RED, 3, 11)     # 上辺 →(τyx)
    arrow(d, x1-16, y1+12, x0+16, y1+12, RED, 3, 11)     # 下辺 ←
    arrow(d, x1+12, y1-16, x1+12, y0+16, RED, 3, 11)     # 右辺 ↑(τxy)
    arrow(d, x0-12, y0+16, x0-12, y1-16, RED, 3, 11)     # 左辺 ↓
    ctext(d, cx, y0-26, "τyx", FS, RED); ctext(d, x1+30, cy, "τxy", FS, RED, "lm")
    note(d, "τxy と τyx は大きさが等しい(τxy=τyx)。偶力が相殺する向き(同一循環だと回転してしまう)")
    save(im, "s2ConjugateShear")


if __name__ == "__main__":
    s2PrincipalMohr(); s2YieldSurface(); stresstransform(); s2MisesJudge()
    s2Truss2Bar(); s2CantileverUDL(); s2TwoBarsThermal()
    s2HollowShaft(); s2ThinCylinder(); s2ConjugateShear()
    s2OverhangBeam(); s2CantReactions(); s2SectionZ()
    s2RigidPlate2Bars(); s2RigidBarWire(); s2PlateHoles()
    s2PoissonBar(); s2ShearModulus(); s2StrainDisp()
    print("done s2 core figures")
