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


if __name__ == "__main__":
    s2PrincipalMohr(); s2YieldSurface(); stresstransform(); s2MisesJudge()
    s2Truss2Bar(); s2CantileverUDL(); s2TwoBarsThermal()
    print("done s2 core figures")
