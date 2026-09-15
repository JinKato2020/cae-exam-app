# -*- coding: utf-8 -*-
"""固体1級 第11章 各種モデリング技術 — 問題図(接頭辞 s1e11)。
figlib で白地660x420・黒線画。JSON本体は編集しない。
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

def dashpot(d, x1, y, x2, h=15):
    """ダッシュポット(粘性要素)。x1→x2 の直線上に描く。"""
    L = x2 - x1
    a = x1 + 0.28*L      # シリンダ左
    b = x1 + 0.78*L      # シリンダ右(開放)
    d.line((x1, y, a, y), fill=BLACK, width=3)
    d.line((a, y-h, b, y-h), fill=BLACK, width=2)
    d.line((a, y-h, a, y+h), fill=BLACK, width=2)
    d.line((a, y+h, b, y+h), fill=BLACK, width=2)
    px = x1 + 0.60*L
    d.line((px, y-h+3, px, y+h-3), fill=BLACK, width=6)   # ピストン板
    d.line((px, y, x2, y), fill=BLACK, width=3)           # ピストン棒

def vbar(d, x, y0, y1):
    d.line((x, y0, x, y1), fill=BLACK, width=5)

def dcircle(d, x, y, r, fill="white"):
    d.ellipse((x-r, y-r, x+r, y+r), outline=BLACK, width=2, fill=fill)

# ---------------------------------------------------------------- 11-1
def f_CouplingClass():
    im, d = new(); title(d, "連成の2つのクラス")
    # クラスI:2領域が境界で接する
    ctext(d, 175, 78, "クラスI(境界で接する)", FS)
    d.rectangle((55, 120, 175, 240), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 115, 180, "領域A", FS)
    d.rectangle((175, 120, 295, 240), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 235, 180, "領域B", FS)
    d.line((175, 120, 175, 240), fill=RED, width=5)
    arrow(d, 150, 262, 200, 262, RED, 3, 10)
    arrow(d, 200, 278, 150, 278, RED, 3, 10)
    ctext(d, 175, 300, "境界条件で連成", FT, RED)
    # クラスII:2領域が重複
    ctext(d, 485, 78, "クラスII(領域が重なる)", FS)
    d.ellipse((375, 120, 515, 240), outline=BLACK, width=3)
    d.ellipse((455, 120, 595, 240), outline=BLACK, width=3)
    ctext(d, 405, 180, "現象X", FT)
    ctext(d, 565, 180, "現象Y", FT)
    ctext(d, 485, 180, "重複", FT, RED)
    ctext(d, 485, 300, "支配方程式(構成則)で連成", FT, RED)
    note(d, "境界条件を介す=I / 領域重複・支配方程式を介す=II")
    save(im, "s1e11CouplingClass")

# ---------------------------------------------------------------- 11-2
def f_OneWay():
    im, d = new(); title(d, "片方向連成(静的線形熱応力)")
    d.rectangle((60, 165, 250, 255), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 155, 198, "温度場", F); ctext(d, 155, 226, "ソルバー", FS)
    ctext(d, 155, 285, "先に独立に解く", FT, GRAY)
    d.rectangle((410, 165, 600, 255), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 505, 198, "応力場", F); ctext(d, 505, 226, "ソルバー", FS)
    ctext(d, 505, 285, "後で解く", FT, GRAY)
    arrow(d, 250, 210, 410, 210, BLUE, 4, 15)
    ctext(d, 330, 188, "温度・熱ひずみ", FT, BLUE)
    note(d, "逆向きの矢印はない(応力→温度は無い=片方向)")
    save(im, "s1e11OneWay")

# ---------------------------------------------------------------- 11-4
def f_Staggered():
    im, d = new(); title(d, "連成問題の解法の系統")
    def box(x0, y0, x1, y1, t1, t2="", fill=FILL1):
        d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=fill)
        cx, cy = (x0+x1)/2, (y0+y1)/2
        if t2:
            ctext(d, cx, cy-11, t1, FS); ctext(d, cx, cy+11, t2, FT, GRAY)
        else:
            ctext(d, cx, cy, t1, FS)
    box(255, 60, 405, 100, "連成問題の解法")
    d.line((330, 100, 330, 125), fill=BLACK, width=2)
    d.line((150, 125, 510, 125), fill=BLACK, width=2)
    d.line((150, 125, 150, 150), fill=BLACK, width=2)
    d.line((510, 125, 510, 150), fill=BLACK, width=2)
    box(55, 150, 245, 200, "一体型解法", "強連成", FILL2)
    box(415, 150, 605, 200, "分離型解法")
    d.line((510, 200, 510, 225), fill=BLACK, width=2)
    d.line((420, 225, 600, 225), fill=BLACK, width=2)
    d.line((420, 225, 420, 250), fill=BLACK, width=2)
    d.line((600, 225, 600, 250), fill=BLACK, width=2)
    box(340, 250, 500, 310, "互い違い法", "弱連成(予測値)", FILL2)
    box(510, 250, 630, 310, "ブロック反復", "強連成", FILL2)
    note(d, "一体型=強連成 / 単純な互い違い=弱連成 / 反復収束させれば分離型でも強連成")
    save(im, "s1e11Staggered")

# ---------------------------------------------------------------- 11-5
def f_Mullins():
    im, d = new(); title(d, "ゴムのヒステリシス(マリンス効果)")
    ox, oy = 100, 355
    axes(d, ox, oy, 500, 300, "伸長比 λ", "応力 σ")
    x0 = ox + 40      # λ=1 の位置
    xA = ox + 470     # 点A
    yb = oy - 5       # 底(応力小)
    yA = oy - 260     # 点A(応力大)
    init, low = [], []
    n = 40
    for i in range(n+1):
        t = i/n
        x = x0 + (xA-x0)*t
        init.append((x, yb - (yb-yA)*(t**0.8)))   # 初回曲線(上)
        low.append((x, yb - (yb-yA)*(t**1.7)))    # 除荷・再負荷(下=軟化)
    plot(d, 0, 0, init, BLUE, 4)
    plot(d, 0, 0, low, RED, 4)
    node(d, xA, yA, 6, "white", BLACK); ctext(d, xA+14, yA-6, "A", FS)
    ctext(d, x0-6, yb+2, "λ=1", FT, GRAY, "rm")
    # 方向の目印
    arrow(d, init[18][0], init[18][1]+2, init[22][0], init[22][1]-2, BLUE, 3, 10)
    ctext(d, 250, 150, "初回負荷曲線", FT, BLUE)
    ctext(d, 360, 295, "除荷・再負荷(軟化)", FT, RED)
    note(d, "除荷で低応力経路→再負荷も同経路→A超で初回曲線に復帰(履歴依存)")
    save(im, "s1e11Mullins")

# ---------------------------------------------------------------- 11-6
def f_DynViscoEllipse():
    im, d = new(); title(d, "動的粘弾性の応力-ひずみ(リサージュ楕円)")
    cx, cy = 330, 240
    e0, s0 = 150, 140
    delta = math.radians(35)
    # 中心を通る軸
    arrow(d, cx-e0-40, cy, cx+e0+40, cy, BLACK, 2, 11); ctext(d, cx+e0+48, cy, "ε", FS, BLACK, "lm")
    arrow(d, cx, cy+s0+40, cx, cy-s0-40, BLACK, 2, 11); ctext(d, cx+14, cy-s0-42, "σ", FS, BLACK, "lm")
    pts = []
    for i in range(0, 361, 4):
        th = math.radians(i)
        x = cx + e0*math.sin(th)
        y = cy - s0*math.sin(th+delta)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 4)
    # ε=0 の切片 σ=σ0 sinδ
    yint = cy - s0*math.sin(delta)
    node(d, cx, yint, 5, "white", RED)
    ctext(d, cx+14, yint-4, "σ0 sinδ", FT, RED, "lm")
    node(d, cx, 2*cy-yint, 5, "white", RED)
    # ε0 の目印
    d.line((cx+e0, cy-4, cx+e0, cy+4), fill=GRAY, width=2)
    ctext(d, cx+e0, cy+18, "ε0", FT, GRAY)
    note(d, "囲む面積=1サイクルの損失エネルギー(位相差δで楕円が開く・δ=0で直線)")
    save(im, "s1e11DynViscoEllipse")

# ---------------------------------------------------------------- 11-7
def f_Payne():
    im, d = new(); title(d, "ペイン効果(複素弾性率の振幅依存)")
    ox, oy = 90, 350
    axes(d, ox, oy, 470, 270, "ひずみ振幅", "複素弾性率 E*")
    pts = []
    n = 40
    for i in range(n+1):
        t = i/n
        x = ox + 30 + 420*t
        # 高→低のシグモイド低下
        y = (oy-40) - 190*(1-1/(1+math.exp((t-0.5)*8)))
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 4)
    ctext(d, 250, 110, "振幅↑で低下", FT, BLUE)
    # 小振幅=楕円
    e = []
    for i in range(0, 361, 8):
        th = math.radians(i)
        e.append((150+22*math.sin(th), 150-14*math.sin(th+math.radians(20))))
    plot(d, 0, 0, e, GRAY, 2); ctext(d, 150, 185, "小振幅:楕円", FT, GRAY)
    # 大振幅=眼鏡型(8の字)
    g = []
    for i in range(0, 361, 6):
        th = math.radians(i)
        g.append((470+34*math.sin(th), 300-40*math.sin(2*th)))
    plot(d, 0, 0, g, ORANGE, 2); ctext(d, 470, 355, "大振幅:眼鏡型", FT, ORANGE)
    note(d, "ひずみ振幅の増大で貯蔵弾性率(E*)が低下・軌跡が楕円→眼鏡型に")
    save(im, "s1e11Payne")

# ---------------------------------------------------------------- 11-8
def f_Master():
    im, d = new(); title(d, "温度時間換算則とマスターカーブ")
    # 左:各温度の緩和曲線
    ox, oy = 55, 250
    axes(d, ox, oy, 250, 150, "log t", "E(t)")
    ctext(d, 175, 82, "各温度の緩和曲線", FT, GRAY)
    cols = [BLUE, GREEN, ORANGE]; labs = ["T1(低温)", "T2", "T3(高温)"]
    for k, off in enumerate([0, 55, 110]):
        pts = []
        for i in range(31):
            t = i/30
            x = ox + 20 + off + 90*t
            y = (oy-15) - 110*(1-1/(1+math.exp((t-0.5)*7)))
            pts.append((x, y))
        plot(d, 0, 0, pts, cols[k], 3)
        ctext(d, ox+20+off+45, oy+18, labs[k], FT, cols[k])
    arrow(d, 315, 175, 360, 175, RED, 4, 14); ctext(d, 337, 155, "logα", FT, RED)
    ctext(d, 337, 195, "でシフト", FT, RED)
    # 右:マスターカーブ
    ox2, oy2 = 375, 250
    axes(d, ox2, oy2, 250, 150, "log t", "E(t)")
    ctext(d, 500, 82, "マスターカーブ", FT, GRAY)
    pts = []
    for i in range(61):
        t = i/60
        x = ox2 + 15 + 225*t
        y = (oy2-15) - 110*(1-1/(1+math.exp((t-0.5)*6)))
        pts.append((x, y))
    plot(d, 0, 0, pts, RED, 4)
    note(d, "3温度の緩和曲線を対数時間軸で logα ずらし1本に重ねる")
    save(im, "s1e11Master")

# ---------------------------------------------------------------- 11-9
def f_Maxwell():
    im, d = new(); title(d, "一般化マクスウェルモデル")
    xL, xR = 110, 570; y0, y1 = 95, 340
    vbar(d, xL, y0, y1); vbar(d, xR, y0, y1)
    ys = [125, 200, 275, 325]
    # E∞ バネ(長期弾性率)
    spring(d, xL, ys[0], xR, ys[0], coils=7, amp=13)
    ctext(d, 340, ys[0]-24, "E∞ (長期弾性率のバネ)", FT, GRAY)
    # マクスウェル要素(バネ+ダッシュポット直列)
    for k, y in enumerate([ys[1], ys[2]], start=1):
        xm = 340
        spring(d, xL, y, xm, y, coils=5, amp=12)
        dashpot(d, xm, y, xR, y)
        ctext(d, (xL+xm)/2, y-22, "E%d" % k, FT)
        ctext(d, (xm+xR)/2, y-22, "η%d" % k, FT)
    ctext(d, 340, ys[3], "⋮ (τi = ηi / Ei の異なる要素を並列)", FT, GRAY)
    # 一定ひずみ
    arrow(d, xL-40, 217, xL, 217, RED, 4, 14)
    arrow(d, xR+40, 217, xR, 217, RED, 4, 14)
    ctext(d, xL-45, 240, "ε0", FT, RED); ctext(d, xR+45, 240, "ε0", FT, RED)
    note(d, "各要素の応力が並列に足し合う → E(t)=E∞+ΣEi e^(-t/τi) (プローニー級数)")
    save(im, "s1e11Maxwell")

# ---------------------------------------------------------------- 11-10
def f_Effective():
    im, d = new(); title(d, "有効応力と損傷変数 D")
    # 棒 + 引張荷重
    d.rectangle((175, 120, 485, 185), outline=BLACK, width=3, fill=FILL1)
    arrow(d, 175, 152, 120, 152, RED, 4, 15); ctext(d, 112, 152, "F", F, RED, "rm")
    arrow(d, 485, 152, 540, 152, RED, 4, 15); ctext(d, 548, 152, "F", F, RED, "lm")
    # 破断面の位置
    d.line((330, 120, 330, 185), fill=GRAY, width=2)
    arrow(d, 330, 205, 330, 245, GRAY, 2, 10)
    # 断面(見かけ面積Aと空隙)
    d.rectangle((250, 250, 410, 390), outline=BLACK, width=3, fill=FILL2)
    ctext(d, 330, 235, "断面(見かけ面積 A)", FT, GRAY)
    for (vx, vy, vr) in [(285, 290, 13), (355, 300, 16), (300, 350, 14), (375, 355, 11), (330, 320, 10)]:
        d.ellipse((vx-vr, vy-vr, vx+vr, vy+vr), outline=BLACK, width=2, fill="white")
    ctext(d, 470, 300, "空隙(D)", FT)
    arrow(d, 448, 300, 392, 300, GRAY, 2, 10)
    ctext(d, 330, 405, "有効(負担)面積 (1-D)A → 有効応力 σ̃ = σ/(1-D)", FT, RED)
    save(im, "s1e11Effective")

# ---------------------------------------------------------------- 11-11
def f_Gurson():
    im, d = new(); title(d, "延性損傷:ボイドの発生・成長・合体")
    labs = ["発生", "成長", "合体"]
    xs = [70, 265, 460]
    for k, x0 in enumerate(xs):
        d.rectangle((x0, 150, x0+130, 290), outline=BLACK, width=3, fill=FILL1)
        ctext(d, x0+65, 315, labs[k], FS)
        cx, cy = x0+65, 220
        if k == 0:
            dcircle(d, cx, cy, 16)
        elif k == 1:
            dcircle(d, cx, cy, 34)
        else:
            dcircle(d, cx-22, cy, 30); dcircle(d, cx+22, cy, 30)
            d.line((cx-4, cy-24, cx+4, cy-24), fill="white", width=6)  # 合体の橋
    ctext(d, 330, 108, "母材(剛塑性体)中の同心球形ボイド(ボイド率 f)", FT, GRAY)
    for i in range(2):
        arrow(d, xs[i]+140, 220, xs[i+1]-10, 220, GRAY, 3, 12)
    note(d, "ボイド率 f を降伏関数に取り込む=ガルソン / 合体効果を加える=GTN")
    save(im, "s1e11Gurson")

# ---------------------------------------------------------------- 11-12
def f_Cohesive():
    im, d = new(); title(d, "結合力モデル(CZM)")
    # 左:き裂先端前方の結合力域
    ctext(d, 190, 80, "き裂と結合力域", FT, GRAY)
    d.rectangle((45, 110, 340, 320), outline=LGRAY, width=2, fill=FILL1)
    # 開いたき裂面
    d.line((45, 200, 175, 210), fill=BLACK, width=3)   # 下面
    d.line((45, 200, 175, 190), fill=BLACK, width=3)   # 上面(開口)
    ctext(d, 95, 165, "き裂", FT)
    # 結合力域(牽引力で閉じようとする)
    for xx in range(180, 261, 20):
        arrow(d, xx, 187, xx, 200, RED, 2, 8)
        arrow(d, xx, 213, xx, 200, RED, 2, 8)
    ctext(d, 220, 245, "結合力域", FT, RED)
    ctext(d, 220, 262, "(トラクション)", FT, RED)
    node(d, 265, 200, 5, "white", BLACK); ctext(d, 285, 178, "先端", FT)
    # 右:トラクション-分離則
    ox, oy = 380, 300
    axes(d, ox, oy, 205, 180, "δ", "牽引力 t")
    ctext(d, ox+120, oy+30, "開口量 δ", FT, GRAY)
    pts = [(ox, oy)]
    for i in range(1, 61):
        t = i/60
        x = ox + 200*t
        if t < 0.3:
            y = oy - 150*(t/0.3)
        else:
            y = oy - 150*(1-(t-0.3)/0.7)
        pts.append((x, y))
    plot(d, 0, 0, pts, BLUE, 4)
    ctext(d, ox+63, oy-165, "破壊強度", FT, GRAY)
    ctext(d, ox+150, oy-55, "面積=破壊エネルギー", FT, GRAY)
    note(d, "牽引力-開口量の関係(トラクション-分離則)で非線形破壊域を表す")
    save(im, "s1e11Cohesive")

# ---------------------------------------------------------------- 11-15
def f_OffAxis():
    im, d = new(); title(d, "直交異方性材料の座標変換(off-axis)")
    cx, cy = 330, 235; s = 100; th = math.radians(24)
    c, si = math.cos(th), math.sin(th)
    def R(px, py):   # ローカル→画面(y下向き)
        return (cx + px*c - py*si, cy - (px*si + py*c))
    # 回転した板
    corners = [R(-s, -s), R(s, -s), R(s, s), R(-s, s)]
    d.polygon(corners, outline=BLACK, width=3, fill=FILL1)
    # 繊維(軸1方向=ローカルx)
    for ly in range(-70, 71, 28):
        a = R(-s+8, ly); b = R(s-8, ly)
        d.line((a[0], a[1], b[0], b[1]), fill=GRAY, width=2)
    # 材料主軸 1,2
    a1 = R(s+34, 0); arrow(d, cx, cy, a1[0], a1[1], BLUE, 3, 12); ctext(d, a1[0]+10, a1[1], "軸1(繊維)", FT, BLUE, "lm")
    a2 = R(0, s+30); arrow(d, cx, cy, a2[0], a2[1], BLUE, 3, 12); ctext(d, a2[0]-6, a2[1]-10, "軸2", FT, BLUE)
    # 全体座標 x,y (左下)
    gx, gy = 90, 360
    arrow(d, gx, gy, gx+70, gy, BLACK, 2, 11); ctext(d, gx+78, gy, "x", FS, BLACK, "lm")
    arrow(d, gx, gy, gx, gy-70, BLACK, 2, 11); ctext(d, gx-10, gy-74, "y", FS, BLACK, "rm")
    # 角度θ
    angle_arc(d, cx, cy, 44, 0, 24, "θ", GRAY)
    d.line((cx, cy, cx+70, cy), fill=GRAY, width=1)
    # 荷重(x方向)
    arrow(d, 120, 150, 175, 150, RED, 3, 12)
    arrow(d, 540, 150, 485, 150, RED, 3, 12)
    ctext(d, 330, 128, "荷重(x方向)", FT, RED)
    note(d, "繊維方向と荷重方向のずれ(θ≠0,90°)で 垂直応力→せん断ひずみ の連成")
    save(im, "s1e11OffAxis")

# ---------------------------------------------------------------- 11-17
def f_Laminate():
    im, d = new(); title(d, "積層板の板厚方向 z 座標(ABD剛性)")
    xl, xr = 150, 360
    ys = [130, 170, 210, 250, 290]   # 界面(4層)
    for k in range(len(ys)-1):
        fill = [FILL1, FILL2, FILL3, FILL2][k]
        d.rectangle((xl, ys[k], xr, ys[k+1]), outline=BLACK, width=2, fill=fill)
    zmid = (ys[0]+ys[-1])/2
    # z軸
    zx = 400
    arrow(d, zx, ys[-1]+30, zx, ys[0]-30, BLACK, 2, 11); ctext(d, zx, ys[0]-40, "z", FS)
    d.line((xl, zmid, 470, zmid), fill=RED, width=2)   # 中央面 z=0
    ctext(d, 435, zmid-13, "中央面 z=0", FT, RED)
    labs = ["z0", "z1", "z2", "z3", "z4"]
    for k, y in enumerate(ys):
        d.line((zx-6, y, zx+6, y), fill=BLACK, width=2)
        ctext(d, zx+24, y, labs[k], FT, GRAY, "lm")
    # N と M
    arrow(d, xl-45, zmid, xl, zmid, GREEN, 4, 13); ctext(d, xl-52, zmid, "N", F, GREEN, "rm")
    d.arc((500, 190, 590, 280), 40, 320, fill=BLUE, width=4)
    arrow(d, 585, 205, 578, 190, BLUE, 3, 10)
    ctext(d, 545, 300, "M(曲げ)", FT, BLUE)
    ctext(d, 545, 150, "面内力 N", FT, GREEN)
    note(d, "各層剛性を z で積分 → 面内A・カップリングB・曲げD (対称積層で B=0)")
    save(im, "s1e11Laminate")

# ---------------------------------------------------------------- 11-18
def f_Fsdt():
    im, d = new(); title(d, "板厚方向のせん断ひずみ分布(FSDT / HSDT)")
    # 左:FSDT=一定
    def frame(cx, top, bot, lab, sub):
        d.line((cx, top, cx, bot), fill=BLACK, width=2)     # z軸(板厚)
        d.line((cx-70, top, cx-70, bot), fill=LGRAY, width=2)
        d.line((cx+70, top, cx+70, bot), fill=LGRAY, width=2)
        ctext(d, cx, top-22, lab, FS); ctext(d, cx, bot+24, sub, FT, GRAY)
    ty, by = 110, 320
    frame(190, ty, by, "FSDT", "せん断ひずみ一定")
    xoff = 190 + 48
    d.line((xoff, ty, xoff, by), fill=BLUE, width=4)
    for yy in range(ty, by+1, 30):
        d.line((190, yy, xoff, yy), fill=BLUE, width=1)
    frame(470, ty, by, "HSDT", "高次(曲線)分布")
    pts = []
    for i in range(31):
        t = i/30
        z = ty + (by-ty)*t
        g = math.sin(math.pi*t)      # 端で0・中央最大
        pts.append((470 + 55*g, z))
    plot(d, 0, 0, pts, GREEN, 4)
    ctext(d, 330, 355, "γ(z)", FT, GRAY)
    note(d, "FSDT:平面保持でせん断ひずみが板厚方向に一定 / HSDT:高次で曲線分布")
    save(im, "s1e11Fsdt")

# ---------------------------------------------------------------- 11-19
def f_Crack():
    im, d = new(); title(d, "コンクリートのひび割れモデル")
    def grid(x0, y0, cell, n):
        for i in range(n+1):
            d.line((x0, y0+i*cell, x0+n*cell, y0+i*cell), fill=LGRAY, width=1)
            d.line((x0+i*cell, y0, x0+i*cell, y0+n*cell), fill=LGRAY, width=1)
    # 左:分散クラック(要素内で平滑化)
    ctext(d, 175, 82, "分散クラックモデル", FS)
    gx, gy, cell = 80, 110, 62
    grid(gx, gy, cell, 3)
    for r in range(3):
        for c in range(3):
            cx, cy = gx+c*cell+cell/2, gy+r*cell+cell/2
            for o in (-14, 0, 14):   # 要素内の平行ハッチ=平滑化された割れ
                d.line((cx-16, cy+o+16, cx+16, cy+o-16), fill=RED, width=2)
    ctext(d, 175, 320, "要素内に平滑化(マクロ剛性低下)", FT, GRAY)
    # 右:離散クラック(要素境界)
    ctext(d, 485, 82, "離散クラックモデル", FS)
    gx2 = 390
    grid(gx2, gy, cell, 3)
    zig = [(gx2, gy+cell), (gx2+cell, gy+cell), (gx2+cell, gy+2*cell),
           (gx2+2*cell, gy+2*cell), (gx2+2*cell, gy+cell), (gx2+3*cell, gy+cell)]
    d.line(zig, fill=RED, width=5, joint="curve")
    ctext(d, 485, 320, "要素境界に沿う個別のき裂", FT, GRAY)
    note(d, "分散=要素内で平滑化 / 離散=要素境界に個々のき裂を表現")
    save(im, "s1e11Crack")

# ---------------------------------------------------------------- 11-20
def f_Dilatancy():
    im, d = new(); title(d, "地盤のダイレイタンシー(せん断→体積変化)")
    def sand(cx, rows_y, r=17, cols=4, dx=0):
        for j, yy in enumerate(rows_y):
            offset = dx if j == 0 else 0
            for i in range(cols):
                x = cx + i*(2*r+4) - (cols-1)*(r+2) + offset
                dcircle(d, x, yy, r, FILL2)
    # 左:密な砂=膨張
    ctext(d, 175, 80, "密な砂 → 膨張", FS, GREEN)
    sand(175, [230, 268], dx=22)                 # 上段が乗り上げてずれる
    arrow(d, 175, 205, 240, 205, RED, 3, 11)     # せん断
    arrow(d, 175, 293, 110, 293, RED, 3, 11)
    arrow(d, 300, 250, 300, 205, GREEN, 4, 13); ctext(d, 318, 225, "体積↑", FT, GREEN, "lm")
    ctext(d, 175, 320, "粒子が乗り上げ体積増加", FT, GRAY)
    # 右:緩い砂=収縮
    ctext(d, 490, 80, "緩い砂 → 収縮", FS, ORANGE)
    for (x, y) in [(455, 220), (525, 222), (490, 250), (560, 255), (470, 285), (540, 288)]:
        dcircle(d, x, y, 16, FILL2)
    arrow(d, 430, 200, 495, 200, RED, 3, 11)
    arrow(d, 560, 300, 495, 300, RED, 3, 11)
    arrow(d, 610, 225, 610, 275, ORANGE, 4, 13); ctext(d, 620, 250, "体積↓", FT, ORANGE, "lm")
    ctext(d, 490, 320, "粒子が隙間に落ち込み体積減少", FT, GRAY)
    note(d, "せん断に伴う非可逆な体積変化(密=膨張・緩=収縮)=ダイレイタンシー")
    save(im, "s1e11Dilatancy")

if __name__ == "__main__":
    f_CouplingClass(); f_OneWay(); f_Staggered(); f_Mullins()
    f_DynViscoEllipse(); f_Payne(); f_Master(); f_Maxwell()
    f_Effective(); f_Gurson(); f_Cohesive(); f_OffAxis()
    f_Laminate(); f_Fsdt(); f_Crack(); f_Dilatancy()
    print("=== s1e11 done ===")
