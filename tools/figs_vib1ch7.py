# -*- coding: utf-8 -*-
"""振動1級 第7章「流体連成系の解析基礎」問題図 21枚。figlibで白地660x420線画。
方針: 正確さ最優先・機構のみ・装飾禁止。ラベルはASCII簡易表記(y,theta,L,M,V,D,rho,pi,a^2,
St,Cm,Mf,Mv,fn 等)で豆腐回避。helpful図は結論を露骨に描かず機構・関係のみ示す。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ------------------------------------------------ helpers
def dsh(d, x1, y1, x2, y2, col=GRAY, wd=2, dl=9, gap=6):
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


def marc(d, cx, cy, r, a0, a1, col=RED, wd=3, label="", ccw=True):
    """モーメント/回転の弧+終端矢印。a0,a1は度(数学系:反時計回り、右=0)。"""
    d.arc((cx - r, cy - r, cx + r, cy + r), -a1, -a0, fill=col, width=wd)
    ae = math.radians(a1 if ccw else a0)
    ex, ey = cx + r * math.cos(ae), cy - r * math.sin(ae)
    # 接線方向
    tx, ty = (-math.sin(ae), -math.cos(ae)) if ccw else (math.sin(ae), math.cos(ae))
    hx, hy = ex + 14 * tx, ey + 14 * ty
    arrow(d, ex - 0.1 * tx, ey - 0.1 * ty, hx, hy, col, wd, 12)
    if label:
        am = math.radians((a0 + a1) / 2)
        ctext(d, cx + (r + 18) * math.cos(am), cy - (r + 18) * math.sin(am), label, FS, col)


def vortex(d, x, y, r, ccw=True, col=BLUE):
    """カルマン渦1個。円+回転方向を示す接線矢印。"""
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=2)
    if ccw:
        arrow(d, x + 4, y - r, x - 7, y - r, col, 2, 7)
    else:
        arrow(d, x - 4, y - r, x + 7, y - r, col, 2, 7)


def duct(d, x0, x1, yt, yb, wd=3):
    d.line((x0, yt, x1, yt), fill=BLACK, width=wd)
    d.line((x0, yb, x1, yb), fill=BLACK, width=wd)


# ================================================ 7-1 フラッター2自由度連成 (helpful)
def f_flutter_2dof():
    im, d = new(); title(d, "翼型剛体の2自由度系:空気力L,Mが上下yと回転thetaを連成")
    cx, cy = 340, 210
    # 翼型(楕円)
    d.ellipse((cx - 95, cy - 26, cx + 95, cy + 26), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 6, "white")
    ctext(d, cx, cy + 20, "弾性軸", FT, GRAY)
    # 上下ばね(下方向・床へ)
    spring(d, cx - 40, cy + 26, cx - 40, cy + 96, coils=4, amp=9)
    hwall(d, cx - 90, cx + 10, cy + 100, side=1, n=6)
    ctext(d, cx - 40, cy + 118, "並進ばね ky", FT, GRAY)
    # 回転ばね(弾性軸まわりのトーション)
    marc(d, cx, cy, 44, 200, 320, GREEN, 2, "回転ばね k_theta", ccw=True)
    # 上下自由度 y
    arrow(d, cx + 120, cy, cx + 120, cy - 48, BLUE, 3, 12); ctext(d, cx + 132, cy - 26, "y (上下)", FT, BLUE, "lm")
    # 回転自由度 theta
    marc(d, cx + 60, cy, 30, 20, 120, BLUE, 2, "theta", ccw=True)
    # 一様流と空気力
    for yy in (cy - 40, cy, cy + 40):
        arrow(d, 70, yy, 150, yy, GRAY, 2, 10)
    ctext(d, 100, cy - 62, "一様流 V", FS, GRAY)
    arrow(d, cx - 50, cy - 26, cx - 50, cy - 74, RED, 3, 12); ctext(d, cx - 50, cy - 90, "揚力 L", FT, RED)
    marc(d, cx, cy, 60, 320, 40, RED, 3, "M", ccw=True)
    note(d, "構造は非連成でも空気力L,Mが減衰・剛性行列の非対角項を作り連成させる")
    save(im, "v1e7FlutterCoupling2DOF")


# ================================================ 7-2 対角化→非連成 (helpful)
def f_decoupled_diagonal():
    im, d = new(); title(d, "非対角(連成)項を除き対角化:独立な2つの1自由度系に分離")
    # 左:連成行列
    matrix_grid(d, 70, 150, [["c11", "c12"], ["c21", "c22"]], cell=64, highlight=(0, 1), fnt=FS)
    ctext(d, 70 + 64, 150 + 2 * 64 + 18, "非対角=連成項", FT, RED)
    arrow(d, 210, 214, 300, 214, BLACK, 3, 14); ctext(d, 255, 196, "対角化", FT, GRAY)
    matrix_grid(d, 320, 150, [["c1", "0"], ["0", "c2"]], cell=64, fnt=FS)
    ctext(d, 320 + 64, 150 + 2 * 64 + 18, "対角=非連成", FT, GREEN)
    # 分離された2つの1自由度系(右上の空き領域へ)
    ctext(d, 565, 132, "独立な2系", FT, GRAY)
    def sdof(ox, lab, sign, scol):
        box(d, ox - 22, 150, ox + 22, 182, FILL2)
        ctext(d, ox, 166, lab, FT)
        spring(d, ox, 182, ox, 222, coils=4, amp=8)
        hwall(d, ox - 24, ox + 24, 226, side=1, n=4)
        ctext(d, ox, 246, sign, FT, scol)
    sdof(522, "y系", "正→収束", GREEN)
    sdof(608, "th系", "負→発散", RED)
    note(d, "各1自由度系の減衰項の符号でフラッター(発散)を判別できる")
    save(im, "v1e7DecoupledDiagonalMatrix")


# ================================================ 7-3 特性根の安定判別 (helpful)
def f_root_stability():
    im, d = new(); title(d, "特性根の複素平面:左半面=安定・右半面=不安定(フラッター)")
    cx, cy = 330, 245
    # 実軸・虚軸
    arrow(d, 90, cy, 590, cy, BLACK, 2, 11); ctext(d, 596, cy, "Re", FS, BLACK, "lm")
    arrow(d, cx, 400, cx, 90, BLACK, 2, 11); ctext(d, cx - 12, 84, "Im", FS, BLACK, "rm")
    # 左半面=安定(淡く網掛け)
    for xx in range(96, cx, 16):
        dsh(d, xx, 104, xx, 380, (225, 240, 225), 1, 6, 6)
    ctext(d, 195, 118, "左半面: 安定(減衰)", FT, GREEN)
    ctext(d, 475, 118, "右半面: 不安定", FT, RED)
    # 安定な共役根(左)
    for sy in (1, -1):
        px, py = cx - 120, cy - sy * 70
        d.line((px - 8, py - 8, px + 8, py + 8), fill=GREEN, width=3)
        d.line((px - 8, py + 8, px + 8, py - 8), fill=GREEN, width=3)
    # 不安定な共役根(右)=フラッター
    for sy in (1, -1):
        px, py = cx + 100, cy - sy * 80
        d.line((px - 8, py - 8, px + 8, py + 8), fill=RED, width=3)
        d.line((px - 8, py + 8, px + 8, py - 8), fill=RED, width=3)
    ctext(d, cx + 118, cy - 80, "フラッター", FT, RED, "lm")
    note(d, "特性根の実部が全て負なら安定、1つでも正なら振幅が発散する")
    save(im, "v1e7CharacteristicRootStability")


# ================================================ 7-4 スロッシング復元=重力 (helpful)
def f_sloshing_gravity():
    im, d = new(); title(d, "スロッシングの復元力=重力(U字管の1自由度化と自由液面)")
    # 左:U字管
    ox = 150
    d.arc((ox - 60, 220, ox + 60, 340), 0, 180, fill=BLACK, width=3)
    d.line((ox - 60, 150, ox - 60, 280), fill=BLACK, width=3)
    d.line((ox + 60, 150, ox + 60, 280), fill=BLACK, width=3)
    # 傾いた水面(左低・右高)
    d.line((ox - 60, 210, ox - 32, 210), fill=BLUE, width=4)
    d.line((ox + 32, 180, ox + 60, 180), fill=BLUE, width=4)
    d.line((ox - 46, 210, ox + 46, 180), fill=BLUE, width=2)
    arrow(d, ox + 46, 180, ox + 46, 214, RED, 3, 11); ctext(d, ox + 70, 200, "重力復元", FT, RED, "lm")
    ctext(d, ox, 360, "U字管(1自由度化)", FT, GRAY)
    # 右:広い容器の自由液面(波打ち)
    bx0, bx1 = 380, 570; by = 300
    d.line((bx0, 170, bx0, by), fill=BLACK, width=3)
    d.line((bx1, 170, bx1, by), fill=BLACK, width=3)
    d.line((bx0, by, bx1, by), fill=BLACK, width=3)
    pts = [(bx0 + (bx1 - bx0) * t, 220 - 20 * math.sin(math.pi * t)) for t in [i / 60 for i in range(61)]]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, (bx0 + bx1) / 2, 250, "液体(慣性)", FT, GRAY)
    ctext(d, (bx0 + bx1) / 2, 360, "自由液面のスロッシング", FT, GRAY)
    note(d, "復元力は重力・相手は流体の慣性。低振動数で自由液面が大きく揺れる")
    save(im, "v1e7SloshingRestoreGravity")


# ================================================ 7-5 スロッシング vs バルジング (helpful)
def f_sloshing_vs_bulging():
    im, d = new(); title(d, "スロッシング(自由液面)とバルジング(容器壁変形)の対比")
    def tank(ox, mode, lab, freqlab):
        w = 150; yt, yb = 150, 330
        if mode == "slosh":
            d.line((ox, yt, ox, yb), fill=BLACK, width=3)
            d.line((ox + w, yt, ox + w, yb), fill=BLACK, width=3)
        else:  # 壁が変形(たわむ)
            pts_l = [(ox + 16 * math.sin(math.pi * (y - yt) / (yb - yt)), y) for y in range(yt, yb + 1, 6)]
            plot(d, 0, 0, pts_l, RED, 3)
            pts_r = [(ox + w + 16 * math.sin(math.pi * (y - yt) / (yb - yt)), y) for y in range(yt, yb + 1, 6)]
            plot(d, 0, 0, pts_r, RED, 3)
        d.line((ox, yb, ox + w, yb), fill=BLACK, width=3)
        if mode == "slosh":
            pts = [(ox + w * t, 210 - 26 * math.sin(math.pi * t)) for t in [i / 60 for i in range(61)]]
            plot(d, 0, 0, pts, BLUE, 3)
        else:
            d.line((ox, 210, ox + w, 210), fill=BLUE, width=3)
        ctext(d, ox + w / 2, yb + 22, lab, FT, GRAY)
        ctext(d, ox + w / 2, yb + 44, freqlab, FT, (BLUE if mode == "slosh" else RED))
    tank(120, "slosh", "スロッシング", "低振動数・液面大")
    tank(400, "bulge", "バルジング", "高振動数・壁変形")
    note(d, "スロッシング固有振動数は容器半径と水深に依存する")
    save(im, "v1e7SloshingVsBulging")


# ================================================ 7-6 ギャロッピング半円柱 (helpful)
def f_galloping_half_cylinder():
    im, d = new(); title(d, "ギャロッピング:ばね吊り半円柱(平面に風)の自励振動")
    cx, cy = 360, 220
    # 半円柱(平らな面を左=風上へ)。半円: 平面が左、丸みが右
    d.pieslice((cx - 40, cy - 55, cx + 70, cy + 55), -90, 90, outline=BLACK, width=3, fill=FILL1)
    d.line((cx - 40 + 55, cy - 55, cx - 40 + 55, cy + 55), fill=BLACK, width=3)
    ctext(d, cx + 10, cy, "半円柱", FT, GRAY)
    # ばね吊り(上)
    spring(d, cx + 15, cy - 55, cx + 15, cy - 120, coils=4, amp=9)
    hwall(d, cx - 40, cx + 70, cy - 124, side=-1, n=6)
    # 一様風(左から)
    for yy in (cy - 35, cy, cy + 35):
        arrow(d, 80, yy, 200, yy, GRAY, 2, 11)
    ctext(d, 120, cy - 58, "一様風 V", FS, GRAY)
    # 上下運動と成長する振幅
    arrow(d, cx + 100, cy, cx + 100, cy - 60, BLUE, 3, 12)
    arrow(d, cx + 100, cy, cx + 100, cy + 60, BLUE, 3, 12)
    ctext(d, cx + 116, cy, "上下運動", FT, BLUE, "lm")
    # 成長する振動(右に成長波形)
    pts = [(480 + 90 * t, cy - (10 + 34 * t) * math.sin(2 * math.pi * 1.6 * t)) for t in [i / 80 for i in range(81)]]
    plot(d, 0, 0, pts, RED, 2)
    ctext(d, 525, cy + 78, "振幅が増大", FT, RED)
    note(d, "小さな乱れから振幅が増大する自励振動(強制振動ではない)")
    save(im, "v1e7GallopingHalfCylinder")


# ================================================ 7-7 ギャロッピング揚力の向き (helpful)
def f_galloping_lift_dir():
    im, d = new(); title(d, "ギャロッピング:運動と同じ向きに揚力→運動を助長")
    cx, cy = 300, 235
    # 断面(半円)
    d.pieslice((cx - 40, cy - 45, cx + 50, cy + 45), -90, 90, outline=BLACK, width=3, fill=FILL1)
    d.line((cx + 5, cy - 45, cx + 5, cy + 45), fill=BLACK, width=3)
    # 物体の上向き運動
    arrow(d, cx, cy - 50, cx, cy - 110, BLUE, 4, 13); ctext(d, cx, cy - 128, "物体速度 y' (上向き)", FT, BLUE)
    # 一様風 U(水平)
    arrow(d, 80, cy, 180, cy, GRAY, 3, 12); ctext(d, 120, cy - 20, "風 U", FS, GRAY)
    # 相対風(見かけ):下向き成分が付き斜めに
    arrow(d, cx - 150, cy - 60, cx - 30, cy - 10, ORANGE, 2, 11)
    ctext(d, cx - 150, cy - 74, "相対風(見かけの迎え角)", FT, ORANGE, "lm")
    # 生じる揚力=上向き(運動と同じ)
    arrow(d, cx + 60, cy, cx + 60, cy - 70, RED, 4, 14); ctext(d, cx + 74, cy - 40, "揚力(上向き)", FT, RED, "lm")
    note(d, "揚力が運動方向を助長するため振幅が増大=自励振動になる")
    save(im, "v1e7GallopingLiftDirection")


# ================================================ 7-8 カルマン渦の放出 (helpful)
def f_karman_shedding():
    im, d = new(); title(d, "配管内円柱の後流:上下交互のカルマン渦が周期的に放出")
    x0, x1 = 90, 590; yt, yb = 130, 330
    duct(d, x0, x1, yt, yb)
    ymid = (yt + yb) / 2
    # 流入
    for yy in (yt + 30, ymid, yb - 30):
        arrow(d, x0 + 6, yy, x0 + 60, yy, GRAY, 2, 10)
    ctext(d, x0 + 40, yt + 12, "流れ V", FT, GRAY)
    # 円柱
    cx = 200
    d.ellipse((cx - 22, ymid - 22, cx + 22, ymid + 22), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, ymid + 40, "円柱 D", FT, GRAY)
    # 上下交互の渦列(互い違い)
    xs = [290, 350, 410, 470, 530]
    for i, xx in enumerate(xs):
        up = (i % 2 == 0)
        yy = ymid - 40 if up else ymid + 40
        vortex(d, xx, yy, 15, ccw=up, col=(BLUE if up else RED))
    note(d, "流れ直交方向の励振が渦の剥離振動数と同じ振動数で起こる")
    save(im, "v1e7KarmanVortexShedding")


# ================================================ 7-9 カルマン渦共振 (helpful)
def f_karman_resonance():
    im, d = new(); title(d, "一様流中のばね支持円柱:f=StV/D が fn に近づくと共振")
    ymid = 235
    # 流入
    for yy in (ymid - 55, ymid, ymid + 55):
        arrow(d, 70, yy, 150, yy, GRAY, 2, 11)
    ctext(d, 105, ymid - 78, "一様流 V", FS, GRAY)
    # ばね支持円柱(上からばね)
    cx = 230
    spring(d, cx, ymid - 26, cx, 110, coils=4, amp=10)
    hwall(d, cx - 40, cx + 40, 106, side=-1, n=5)
    ctext(d, cx + 46, 130, "ばね K", FT, GRAY, "lm")
    d.ellipse((cx - 26, ymid - 26, cx + 26, ymid + 26), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, ymid, "M,D", FT, GRAY)
    # 円柱の横振動
    arrow(d, cx, ymid + 34, cx + 44, ymid + 34, BLUE, 3, 11)
    arrow(d, cx, ymid + 34, cx - 44, ymid + 34, BLUE, 3, 11)
    ctext(d, cx, ymid + 58, "横振動 fn=(1/2pi)sqrt(K/M)", FT, BLUE)
    # 後流の渦AとB
    vortex(d, 360, ymid - 42, 15, ccw=True, col=BLUE); ctext(d, 360, ymid - 70, "渦A", FT, BLUE)
    vortex(d, 430, ymid + 42, 15, ccw=False, col=RED); ctext(d, 430, ymid + 70, "渦B", FT, RED)
    vortex(d, 500, ymid - 42, 15, ccw=True, col=BLUE)
    ctext(d, 470, ymid, "f = St V / D", FT, BLACK)
    note(d, "渦発生周波数 f=StV/D が円柱固有振動数 fn に近づくと共振する")
    save(im, "v1e7KarmanCylinderResonance")


# ================================================ 7-10 ロックイン域 (helpful)
def f_lock_in():
    im, d = new(); title(d, "ロックイン:渦はく離振動数が固有振動数付近で流速に無関係化")
    ox, oy = 110, 340; xlen, ylen = 460, 240
    axes(d, ox, oy, xlen, ylen, "流速 V", "振動数 f")
    # 固有振動数 fn(水平破線)
    fn = oy - 120
    dsh(d, ox, fn, ox + xlen, fn, LGRAY)
    ctext(d, ox - 8, fn, "fn", FT, GRAY, "rm")
    # 渦はく離振動数の直線 f=StV/D、ロックイン域で水平に張り付く
    x_a = ox + 130; x_b = ox + 300
    plot(d, 0, 0, [(ox + 20, oy - 30), (x_a, fn - 6)], BLUE, 3)          # 上昇部
    plot(d, 0, 0, [(x_a, fn - 6), (x_b, fn - 6)], RED, 4)               # ロックイン(水平)
    plot(d, 0, 0, [(x_b, fn - 6), (ox + xlen - 10, oy - 210)], BLUE, 3)  # 再上昇
    ctext(d, (x_a + x_b) / 2, fn - 26, "ロックイン域", FT, RED)
    # ロックイン域の範囲(縦破線)
    dsh(d, x_a, oy, x_a, fn, LGRAY); dsh(d, x_b, oy, x_b, fn, LGRAY)
    ctext(d, ox + xlen - 40, oy - 200, "f=StV/D", FT, BLUE, "rm")
    note(d, "この領域では流速を変えても円柱の振動数は固有振動数に保たれる")
    save(im, "v1e7LockInRegion")


# ================================================ 7-11 ハウスナー集中質量 (helpful)
def f_housner_lumped():
    im, d = new(); title(d, "ハウスナーの集中質量:インパルシブ+コンベクティブ質量")
    x0, x1 = 180, 480; yt, yb = 150, 340
    d.line((x0, yt, x0, yb), fill=BLACK, width=3)
    d.line((x1, yt, x1, yb), fill=BLACK, width=3)
    d.line((x0, yb, x1, yb), fill=BLACK, width=3)
    d.line((x0, 200, x1, 200), fill=BLUE, width=3)  # 自由液面
    ctext(d, (x0 + x1) / 2, 186, "自由液面", FT, BLUE)
    # 水平加速度
    arrow(d, x0 - 90, 250, x0 - 20, 250, RED, 4, 13); ctext(d, x0 - 100, 232, "水平加速度", FT, RED, "rm")
    # インパルシブ質量(壁に剛結)
    mi = 300
    box(d, mi - 24, yb - 60, mi + 24, yb - 12, FILL2); ctext(d, mi, yb - 36, "mi", FS)
    d.line((x0, yb - 36, mi - 24, yb - 36), fill=BLACK, width=3)
    d.line((mi + 24, yb - 36, x1, yb - 36), fill=BLACK, width=3)
    ctext(d, mi, yb + 20, "インパルシブ質量(壁に固定)", FT, GRAY)
    # コンベクティブ質量(ばね支持・自由液面で揺れる)
    mc = 330
    box(d, mc - 22, 210, mc + 22, 250, FILL1); ctext(d, mc, 230, "mc", FS)
    spring(d, x0, 230, mc - 22, 230, coils=4, amp=8)
    spring(d, mc + 22, 230, x1, 230, coils=4, amp=8)
    ctext(d, mc, 268, "コンベクティブ質量(揺動)", FT, GRAY)
    note(d, "容器内液体を壁固定の衝撃質量とばね支持の揺動質量に分けて表す")
    save(im, "v1e7HousnerLumpedMass")


# ================================================ 7-12 VOF vs ALE (helpful)
def f_vof_vs_ale():
    im, d = new(); title(d, "自由表面の扱い:VOF(空間固定メッシュ)とALE(追随メッシュ)")
    def gridbox(ox):
        x1 = ox + 190; yt, yb = 150, 330
        box(d, ox, yt, x1, yb, "white")
        return ox, x1, yt, yb
    # 左:VOF
    ox, x1, yt, yb = gridbox(130)
    for gx in range(ox, x1 + 1, 38):
        d.line((gx, yt, gx, yb), fill=LGRAY, width=1)
    for gy in range(yt, yb + 1, 36):
        d.line((ox, gy, x1, gy), fill=LGRAY, width=1)
    # 自由表面(斜め)=セルの充填率で表現
    d.line((ox, 250, x1, 210), fill=BLUE, width=3)
    for gx in range(ox, x1, 38):
        ctext(d, gx + 19, 300, "1.0", FT, GRAY)
    ctext(d, ox + 95, 210, "0.5", FT, RED)
    ctext(d, (ox + x1) / 2, yb + 22, "VOF:充填率で界面を捕捉(流体解析)", FT, GRAY)
    # 右:ALE
    ox, x1, yt, yb = gridbox(400)
    surf = 230
    for gx in range(ox, x1 + 1, 38):
        d.line((gx, yt, gx, yb), fill=LGRAY, width=1)
    # メッシュが液位に追随(液面より上は無い/線が液面に沿う)
    for k in range(6):
        gy = surf + k * (yb - surf) / 5
        d.line((ox, gy, x1, gy), fill=LGRAY, width=1)
    d.line((ox, surf, x1, surf), fill=BLUE, width=3)
    arrow(d, x1 + 6, surf, x1 + 6, surf - 30, BLUE, 2, 9); ctext(d, x1 + 12, surf - 40, "追随", FT, BLUE, "lm")
    ctext(d, (ox + x1) / 2, yb + 22, "ALE:メッシュが液位に追随(構造解析)", FT, GRAY)
    save(im, "v1e7VOFvsALEMesh")


# ================================================ 7-13 ALEメッシュひずみ (helpful)
def f_ale_distortion():
    im, d = new(); title(d, "ALEメッシュ:液位増大で引き伸ばされ歪む→リメッシュ")
    def panel(ox, stretch, lab):
        x1 = ox + 180; yt, yb = 150, 320
        d.line((ox, yb, x1, yb), fill=BLACK, width=3)
        d.line((ox, yt, ox, yb), fill=BLACK, width=2)
        d.line((x1, yt, x1, yb), fill=BLACK, width=2)
        surf = yt + 20 if stretch else yt + 90
        # 縦線(引き伸ばしで間隔が広がる)
        for gx in range(ox, x1 + 1, 36):
            d.line((gx, surf, gx, yb), fill=LGRAY, width=1)
        rows = 3 if stretch else 5
        for k in range(rows + 1):
            gy = surf + k * (yb - surf) / rows
            d.line((ox, gy, x1, gy), fill=LGRAY, width=1)
        d.line((ox, surf, x1, surf), fill=BLUE, width=3)
        ctext(d, (ox + x1) / 2, yb + 22, lab, FT, GRAY)
    panel(90, False, "初期(適正メッシュ)")
    arrow(d, 285, 240, 335, 240, BLACK, 3, 13)
    panel(360, True, "液位増大→縦に伸び歪む")
    arrow(d, 450, 200, 450, 240, RED, 3, 11); ctext(d, 470, 190, "重力復元", FT, RED, "lm")
    note(d, "歪みが大きくなればリメッシュで切り直す。復元力は重力")
    save(im, "v1e7ALEMeshDistortion")


# ================================================ 7-14 付加減衰の自励 (helpful)
def f_added_damping():
    im, d = new(); title(d, "付加減衰:構造減衰+付加減衰の和が正で収束・負で発散")
    # 構造物(流体中で振動)
    cx, cy = 180, 220
    box(d, cx - 20, cy - 60, cx + 20, cy + 60, FILL2)
    for gy in range(140, 320, 14):
        dsh(d, 90, gy, 270, gy, (215, 228, 240), 1, 5, 6)  # 流体の背景
    box(d, cx - 20, cy - 60, cx + 20, cy + 60, FILL2)
    arrow(d, cx + 20, cy, cx + 60, cy, BLUE, 3, 11); ctext(d, cx + 66, cy, "速度 v", FT, BLUE, "lm")
    # 速度比例の付加減衰力
    arrow(d, cx - 20, cy - 30, cx - 60, cy - 30, RED, 3, 11); ctext(d, cx - 66, cy - 30, "付加減衰力 ~v", FT, RED, "rm")
    ctext(d, cx, 340, "流体中で振動", FT, GRAY)
    # 収束/発散の2波形
    ox, oy = 320, 210
    axes(d, ox, oy, 260, 130, "t", "x")
    pc = [(ox + 250 * t, oy - 60 * math.exp(-1.6 * t) * math.sin(2 * math.pi * 2 * t)) for t in [i / 100 for i in range(101)]]
    plot(d, 0, 0, pc, GREEN, 2); ctext(d, ox + 200, oy - 70, "和>0:収束", FT, GREEN)
    ox2, oy2 = 320, 360
    pd = [(ox2 + 250 * t, oy2 - 26 * math.exp(1.4 * t) * math.sin(2 * math.pi * 2 * t)) for t in [i / 100 for i in range(101)]]
    # クリップ
    pd = [(x, max(300, min(400, y))) for (x, y) in pd]
    plot(d, 0, 0, pd, RED, 2); ctext(d, ox2 + 200, 316, "和<0:発散(自励)", FT, RED)
    save(im, "v1e7AddedDampingSelfExcite")


# ================================================ 7-15 付加質量係数と壁 (helpful)
def f_added_mass_coef_wall():
    im, d = new(); title(d, "付加質量係数Cm:壁に近いほど・粘性が高いほど増大")
    ox, oy = 110, 330; xlen, ylen = 460, 230
    axes(d, ox, oy, xlen, ylen, "壁への近さ→", "Cm")
    # 基準 Cm=1.0(無限静止流体)
    base = oy - 60
    dsh(d, ox, base, ox + xlen, base, LGRAY); ctext(d, ox - 8, base, "1.0", FT, GRAY, "rm")
    ctext(d, ox + 90, base - 16, "無限流体 Cm=1.0", FT, GRAY)
    # 壁接近で増大する曲線
    pts = [(ox + xlen * t, base - 150 * t ** 2) for t in [i / 60 for i in range(61)]]
    plot(d, 0, 0, pts, BLUE, 3)
    ctext(d, ox + xlen - 40, oy - 210, "壁近接で増大", FT, BLUE, "rm")
    # 粘性大の曲線(さらに上)
    pts2 = [(ox + xlen * t, base - 30 - 150 * t ** 2) for t in [i / 60 for i in range(61)]]
    for k in range(0, len(pts2) - 1, 2):
        d.line((pts2[k][0], pts2[k][1], pts2[k + 1][0], pts2[k + 1][1]), fill=RED, width=2)
    ctext(d, ox + 250, oy - 190, "粘性が高いほど大", FT, RED)
    note(d, "壁に近づく閉塞で付加質量が増え、Cmが1.0より大きくなる")
    save(im, "v1e7AddedMassCoefficientWall")


# ================================================ 7-16 円柱の付加質量 (helpful)
def f_added_mass_cylinder():
    im, d = new(); title(d, "円柱の付加質量 Mf=pi rho a^2(排除流体質量に等しい)")
    cx, cy = 300, 225
    # 静止流体(背景の点)
    for gx in range(120, 500, 30):
        for gy in range(130, 330, 30):
            if (gx - cx) ** 2 + (gy - cy) ** 2 > 60 ** 2:
                d.ellipse((gx - 1, gy - 1, gx + 1, gy + 1), fill=LGRAY)
    ctext(d, 150, 150, "静止流体 rho", FT, GRAY)
    # 円柱(半径a)
    d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), outline=BLACK, width=3, fill=FILL2)
    arrow(d, cx, cy, cx + 46, cy, GRAY, 2, 9); ctext(d, cx + 24, cy - 14, "a", FT, GRAY)
    # 軸直角方向の加速運動
    arrow(d, cx - 46, cy, cx - 120, cy, RED, 4, 14); ctext(d, cx - 126, cy - 18, "加速度 (軸直角)", FT, RED, "rm")
    # 引きずられる周囲流体
    for a in (30, 150, 210, 330):
        ar = math.radians(a)
        sx, sy = cx + 60 * math.cos(ar), cy - 60 * math.sin(ar)
        arrow(d, sx, sy, sx - 34, sy, BLUE, 2, 9)
    ctext(d, cx + 90, cy + 70, "周囲流体を引きずる", FT, BLUE)
    box(d, 420, 300, 620, 350, FILL1)
    ctext(d, 520, 325, "Mf = pi rho a^2 (単位長さ)", FT)
    save(im, "v1e7AddedMassCylinder")


# ================================================ 7-17 水没で固有振動数低下 (helpful)
def f_submerged_freq_drop():
    im, d = new(); title(d, "気体中と液体中の比較:付加質量で固有振動数が低下")
    def cantilever(ox, medium, lab):
        wall(d, ox, 150, 300, side=1, n=6)
        d.line((ox, 225, ox + 150, 225), fill=BLACK, width=6)
        node(d, ox + 150, 225, 8, FILL2)
        if medium == "liq":
            for gy in range(150, 320, 14):
                dsh(d, ox - 4, gy, ox + 190, gy, (215, 228, 240), 1, 5, 6)
            wall(d, ox, 150, 300, side=1, n=6)
            d.line((ox, 225, ox + 150, 225), fill=BLACK, width=6)
            node(d, ox + 150, 225, 8, FILL2)
        ctext(d, ox + 80, 330, lab, FT, GRAY)
    cantilever(90, "gas", "(a) 気体中")
    cantilever(380, "liq", "(b) 液体中(付加質量)")
    # 矢印:見かけ質量増→fn低下・減衰増
    box(d, 120, 350, 560, 396, FILL1)
    ctext(d, 340, 373, "液体中: 見かけ質量↑ → 固有振動数 fn↓ ・ 減衰↑", FT, RED)
    save(im, "v1e7SubmergedFreqDrop")


# ================================================ 7-18 海水配管の整流板 (helpful)
def f_seawater_straightener():
    im, d = new(); title(d, "海水配管内の整流板:両面と配管内壁に仮想質量を定義")
    x0, x1 = 120, 560; yt, yb = 160, 300
    # 配管(内壁)
    duct(d, x0, x1, yt, yb)
    for gy in range(yt + 4, yb, 12):
        dsh(d, x0, gy, x1, gy, (210, 226, 240), 1, 5, 6)  # 海水
    duct(d, x0, x1, yt, yb)
    ctext(d, x0 + 60, yt - 16, "海水で満たされた配管", FT, GRAY, "lm")
    # 整流板(縦板)
    px = 340; ymid = (yt + yb) / 2
    d.line((px, yt + 14, px, yb - 14), fill=BLACK, width=6)
    ctext(d, px, yb + 20, "整流板", FT, GRAY)
    # 両面の仮想質量
    arrow(d, px - 6, ymid, px - 46, ymid, RED, 3, 11)
    arrow(d, px + 6, ymid, px + 46, ymid, RED, 3, 11)
    ctext(d, px, yt - 2, "板の両面に仮想質量", FT, RED)
    # 配管内壁にも仮想質量
    arrow(d, 200, yt + 4, 200, yt + 40, BLUE, 3, 11)
    arrow(d, 200, yb - 4, 200, yb - 40, BLUE, 3, 11)
    ctext(d, 200, ymid, "内壁にも", FT, BLUE)
    arrow(d, 470, yt + 4, 470, yt + 40, BLUE, 3, 11)
    arrow(d, 470, yb - 4, 470, yb - 40, BLUE, 3, 11)
    note(d, "仮想質量(流体付加質量)を整流板の両面と配管内側壁面に定義する")
    save(im, "v1e7SeawaterPipeStraightener")


# ================================================ 7-19 曲がり配管の耐震 (helpful)
def f_bent_pipe_seismic():
    im, d = new(); title(d, "曲がり配管をはり要素でモデル化:加圧水は圧力+密度増で考慮")
    # 両端の壁
    wall(d, 90, 120, 210, side=1, n=5); ctext(d, 90, 108, "固定", FT, GRAY, "lm")
    wall(d, 570, 300, 390, side=-1, n=5); ctext(d, 570, 388, "固定", FT, GRAY, "rm")
    # 三次元的に曲がった配管(はり要素:節点+直線)
    pts = [(110, 165), (200, 165), (260, 230), (260, 320), (380, 360), (470, 300), (470, 200), (550, 345)]
    d.line(pts, fill=BLACK, width=6, joint="curve")
    for p in pts:
        node(d, p[0], p[1], 6, "white")
    ctext(d, 300, 150, "はり(パイプ)要素", FT, GRAY)
    # 内部加圧水
    box(d, 120, 350, 400, 398, FILL1)
    ctext(d, 260, 374, "内部加圧水: 圧力条件 + 材料密度↑ で考慮", FT, BLUE)
    save(im, "v1e7BentPipeSeismic")


# ================================================ 7-20 流体反力 (helpful)
def f_fluid_reaction():
    im, d = new(); title(d, "水中で加速する扁平構造:流体反力 F=Mv x'' で見かけ質量増")
    cx, cy = 300, 225
    # 水(背景)
    for gy in range(140, 330, 14):
        dsh(d, 100, gy, 520, gy, (212, 226, 240), 1, 5, 6)
    ctext(d, 150, 150, "水", FT, GRAY)
    # 扁平構造物(横長の板)
    box(d, cx - 70, cy - 16, cx + 70, cy + 16, FILL2)
    ctext(d, cx, cy, "扁平構造", FT, GRAY)
    # 加速度
    arrow(d, cx, cy - 16, cx, cy - 90, BLACK, 4, 14); ctext(d, cx + 12, cy - 70, "加速度 x''", FS, BLACK, "lm")
    # 流体反力(逆向き)
    arrow(d, cx - 40, cy + 16, cx - 40, cy + 86, RED, 4, 14); ctext(d, cx - 40, cy + 104, "流体反力 F=Mv x''", FT, RED)
    arrow(d, cx + 40, cy + 16, cx + 40, cy + 86, RED, 4, 14)
    # 引きずられる流体
    for sx in (cx - 100, cx + 100):
        arrow(d, sx, cy - 40, sx, cy - 90, BLUE, 2, 9)
    ctext(d, cx + 130, cy - 70, "流体を引きずる", FT, BLUE, "lm")
    box(d, 120, 350, 560, 396, FILL1)
    ctext(d, 340, 373, "見かけの質量が付加質量 Mv だけ増える", FT)
    save(im, "v1e7FluidReactionForce")


# ================================================ 7-21 円筒水槽内の板 (helpful)
def f_plate_in_tank():
    im, d = new(); title(d, "円筒水槽内の板A:壁との隙間が狭いほど付加質量増→fn低下")
    # 円筒水槽(上面楕円)
    ox, oy = 180, 150; w, h = 300, 200
    d.ellipse((ox, oy - 20, ox + w, oy + 20), outline=BLACK, width=3)
    d.line((ox, oy, ox, oy + h), fill=BLACK, width=3)
    d.line((ox + w, oy, ox + w, oy + h), fill=BLACK, width=3)
    d.arc((ox, oy + h - 20, ox + w, oy + h + 20), 0, 180, fill=BLACK, width=3)
    ctext(d, ox + w / 2, oy - 34, "固定円筒(水槽)", FT, GRAY)
    # 自由液面
    d.ellipse((ox + 6, oy + 30 - 12, ox + w - 6, oy + 30 + 12), outline=BLUE, width=2)
    ctext(d, ox + w / 2, oy + 30, "自由液面", FT, BLUE)
    # 板A(偏心配置=片側の隙間が狭い)
    px = ox + w * 0.62
    d.line((px, oy + 40, px, oy + h + 4), fill=RED, width=6)
    ctext(d, px, oy + h + 24, "板 A", FT, RED)
    # 隙間寸法(狭い側/広い側)
    dim(d, px + 6, oy + 90, ox + w - 4, oy + 90, "狭い", col=GRAY)
    dim(d, ox + 4, oy + 130, px - 6, oy + 130, "広い", col=GRAY)
    arrow(d, px + 30, oy + 60, px + 6, oy + 60, RED, 2, 9)
    ctext(d, 560, 250, "隙間が狭いほど\n付加質量↑\n曲げfn↓", FT, RED)
    save(im, "v1e7PlateInCylinderTank")


# ================================================ main
def main():
    f_flutter_2dof()
    f_decoupled_diagonal()
    f_root_stability()
    f_sloshing_gravity()
    f_sloshing_vs_bulging()
    f_galloping_half_cylinder()
    f_galloping_lift_dir()
    f_karman_shedding()
    f_karman_resonance()
    f_lock_in()
    f_housner_lumped()
    f_vof_vs_ale()
    f_ale_distortion()
    f_added_damping()
    f_added_mass_coef_wall()
    f_added_mass_cylinder()
    f_submerged_freq_drop()
    f_seawater_straightener()
    f_bent_pipe_seismic()
    f_fluid_reaction()
    f_plate_in_tank()
    print("done v1e7 problem (21)")


if __name__ == "__main__":
    main()
