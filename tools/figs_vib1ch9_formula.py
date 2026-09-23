# -*- coding: utf-8 -*-
"""振動1級 第9章「結果の検証と考察」公式・用語図 23枚。figlibで白地660x420線画。
文字化け回避のためギリシャ文字・特殊記号は英字/簡易表記(omega,phi,rho,B^T,法線が垂直,等)に置換。"""
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


def curve(fn, x0, x1, n=120):
    return [(x0 + (x1 - x0) * i / n, fn(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]


# 1. MAC:2つのモードベクトルの相関(1に近い=一致/0=直交)
def f_mac_matrix():
    im, d = new()
    title(d, "MAC: 実験モードとFEMモードの一致度(0〜1)")
    # 左:よく一致(MAC≈1)
    ox, oy = 150, 250
    axes(d, ox, oy, 130, 130, "phi_A", "phi_X")
    arrow(d, ox, oy, ox + 100, oy - 100, BLUE, 3, 12)
    arrow(d, ox, oy, ox + 96, oy - 104, RED, 3, 12)
    ctext(d, ox + 60, oy + 24, "MAC≒1 (一致)", FT, BLACK)
    # 右:直交(MAC≈0)
    ox2 = 430
    axes(d, ox2, oy, 130, 130, "phi_A", "phi_X")
    arrow(d, ox2, oy, ox2 + 110, oy - 8, BLUE, 3, 12)
    arrow(d, ox2, oy, ox2 + 8, oy - 110, RED, 3, 12)
    ctext(d, ox2 + 60, oy + 24, "MAC≒0 (独立)", FT, BLACK)
    box(d, 70, 320, 590, 388, FILL1)
    ctext(d, 330, 348, "MAC = |分子:内積の2乗| / (各ノルムの積)  分母は2乗しない", FT)
    ctext(d, 330, 372, "1に近い=モード形状が相関   0に近い=一次独立(直交)", FT)
    save(im, "v1f9MacMatrix")


# 2. 残差式:実測(omega,phi)を[K],[M]に代入→0ベクトルに近いか
def f_residual():
    im, d = new()
    title(d, "残差でモデル妥当性を裏取り: [[K]-omega^2[M]]{phi}={0} か")
    cx = 330
    box(d, 90, 120, 250, 190, FILL2); ctext(d, 170, 145, "実測 omega_i", FS); ctext(d, 170, 172, "実測モード phi_i", FT)
    box(d, 410, 120, 570, 190, FILL2); ctext(d, 490, 145, "FEM 行列", FS); ctext(d, 490, 172, "[K], [M]", FS)
    arrow(d, 250, 155, 300, 220, GRAY, 2, 11)
    arrow(d, 410, 155, 360, 220, GRAY, 2, 11)
    box(d, 200, 225, 460, 285, FILL1)
    ctext(d, 330, 255, "残差 r = [[K]-omega_i^2 [M]] phi_i", FS)
    arrow(d, 330, 285, 330, 320, BLACK, 3, 12)
    ctext(d, 330, 345, "r が 0ベクトルに近い → モデル妥当", FS, GREEN)
    ctext(d, 330, 378, "0から離れる → モデルと実機のずれが大きい", FT, RED)
    save(im, "v1f9Residual")


# 3. モード直交性:慣性力[M]phi_i と 変位 phi_j が垂直
def f_orthogonality():
    im, d = new()
    title(d, "固有モードの直交性(i≠j): 慣性力と変位が垂直=独立")
    ox, oy = 250, 260
    axes(d, ox, oy, 240, 170, "", "")
    # phi_j 変位ベクトル(水平)
    arrow(d, ox, oy, ox + 200, oy, BLUE, 4, 14); ctext(d, ox + 210, oy, "phi_j (変位)", FS, BLUE, "lm")
    # [M]phi_i 慣性力(垂直)
    arrow(d, ox, oy, ox, oy - 150, RED, 4, 14); ctext(d, ox + 8, oy - 150, "[M] phi_i (慣性力)", FS, RED, "lm")
    # 直角記号
    d.rectangle((ox, oy - 22, ox + 22, oy), outline=GRAY, width=2)
    ctext(d, ox + 40, oy - 34, "法線が垂直", FT, GRAY)
    box(d, 90, 320, 570, 388, FILL1)
    ctext(d, 330, 348, "phi_i^T [M] phi_j = 0,  phi_i^T [K] phi_j = 0  (i≠j)", FT)
    ctext(d, 330, 372, "一方の慣性力が他方の振動を励起しない=エネルギー的独立", FT)
    save(im, "v1f9Orthogonality")


# 4. コンプライアンスのモード展開(各モードの山を足す)
def f_compliance_modal():
    im, d = new()
    title(d, "コンプライアンスのモード展開: 各モードの共振ピークの和")
    ox, oy = 90, 300
    axes(d, ox, oy, 500, 210, "振動数 f", "|G_ij|")
    peaks = [(180, 150), (330, 110), (470, 80)]
    def resp(x):
        y = 0
        for px, h in peaks:
            y += h / (1 + ((x - px) / 26) ** 2)
        return oy - y
    plot(d, 0, 0, curve(resp, ox + 5, ox + 495, 200), BLUE, 3)
    for i, (px, h) in enumerate(peaks):
        ctext(d, ox + px, oy - h - 16, "モード%d" % (i + 1), FT, GRAY)
    # Δf の刻み
    for xx in range(int(ox + 150), int(ox + 210), 10):
        d.line((xx, oy, xx, oy + 8), fill=GRAY, width=1)
    ctext(d, ox + 180, oy + 22, "Δf を細かく", FT, RED)
    box(d, 90, 350, 590, 405, FILL1)
    ctext(d, 340, 377, "R=レジデュー(モード定数), eta=損失係数(振動数非依存). 鋭いピークほどΔf小", FT)
    save(im, "v1f9ComplianceModal")


# 5. Craig-Bampton法:静たわみ+拘束モード(動的モードを足す)
def f_craig_bampton():
    im, d = new()
    title(d, "Craig-Bampton法: 静たわみ + 拘束(動的)モード")
    # はり
    y0 = 170
    wall(d, 150, y0 - 30, y0 + 30, 1)
    # 静たわみ形状
    pts = curve(lambda x: y0 - 0.0016 * (x - 150) ** 2 * 0.4, 150, 470, 60)
    plot(d, 0, 0, pts, GRAY, 3)
    node(d, 470, pts[-1][1], 7); ctext(d, 490, pts[-1][1], "主自由度 a", FT, GRAY, "lm")
    ctext(d, 300, y0 + 40, "(1) 静たわみ(Guyanと同じ)", FT, GRAY)
    # 拘束モード(動的モード)
    y1 = 300
    wall(d, 150, y1 - 30, y1 + 30, 1)
    pts2 = curve(lambda x: y1 - 40 * math.sin(math.pi * (x - 150) / 320), 150, 470, 80)
    plot(d, 0, 0, pts2, BLUE, 3)
    node(d, 470, y1, 6, "white")
    ctext(d, 300, y1 + 46, "(2) 主自由度を固定した固有モード(拘束モード)", FT, BLUE)
    note(d, "精度悪化要因=主自由度位置/拘束モード本数/縮約節点数(不拘束モード数は無関係)")
    save(im, "v1f9CraigBampton")


# 6. Guyanの静縮小法:慣性項を無視し静たわみだけ
def f_guyan_static():
    im, d = new()
    title(d, "Guyanの静縮小法: 慣性項を無視し静たわみだけで縮約")
    y0 = 210
    wall(d, 150, y0 - 40, y0 + 40, 1)
    # 全自由度(多数の節点)
    for i in range(1, 7):
        xx = 150 + i * 55
        yy = y0 - 0.0016 * (xx - 150) ** 2 * 0.5
        node(d, xx, yy, 5, "white")
    ctext(d, 320, y0 + 60, "全自由度(消去する自由度 d を静的に釣り合わせる)", FT, GRAY)
    pts = curve(lambda x: y0 - 0.0016 * (x - 150) ** 2 * 0.5, 150, 480, 60)
    plot(d, 0, 0, pts, BLUE, 3)
    node(d, 480, pts[-1][1], 8, FILL2); ctext(d, 498, pts[-1][1], "残す主自由度 a", FT, BLACK, "lm")
    box(d, 90, 320, 590, 388, FILL1)
    ctext(d, 340, 348, "x_d = -[K_dd]^-1 [K_da] x_a  (質量項なし=静たわみのみ)", FT)
    ctext(d, 340, 372, "精度悪化要因=分割位置・残留自由度数(動的モード抽出数は無関係)", FT)
    save(im, "v1f9GuyanStatic")


# 7. 片持ちはりの上下曲げ/左右曲げ(断面の幅高さ入替で2倍差)
def f_cantilever_bending():
    im, d = new()
    title(d, "片持ちはり曲げ1次: 上下曲げと左右曲げで固有振動数2倍差")
    # 断面図
    box(d, 120, 150, 160, 230, FILL2)
    dim(d, 120, 240, 160, 240, "b=10", 0); dim(d, 175, 150, 175, 230, "h=20", 0)
    ctext(d, 140, 260, "矩形断面", FT, GRAY)
    # 上下曲げ(高さ方向にしなる=高い)
    y1 = 175
    wall(d, 300, y1 - 25, y1 + 25, 1)
    plot(d, 0, 0, curve(lambda x: y1 - 30 * ((x - 300) / 230) ** 2, 300, 530, 40), BLUE, 3)
    ctext(d, 415, y1 + 40, "上下曲げ h=20 → 高い(例718Hz)", FT, BLUE)
    # 左右曲げ(幅方向=低い)
    y2 = 290
    wall(d, 300, y2 - 25, y2 + 25, 1)
    plot(d, 0, 0, curve(lambda x: y2 - 55 * ((x - 300) / 230) ** 2, 300, 530, 40), RED, 3)
    ctext(d, 415, y2 + 45, "左右曲げ h=10 → 低い(例364Hz)", FT, RED)
    note(d, "f=3.51/(2 pi L^2) sqrt(EI/rho A),  I=b h^3/12 → 寸法比2で約2倍差")
    save(im, "v1f9CantileverBending")


# 8. 材料依存性 omega ∝ sqrt(E/rho)
def f_material_dependence():
    im, d = new()
    title(d, "固有角振動数の材料依存性: omega ∝ sqrt(E/rho)")
    ox, oy = 330, 210
    # ばね-マス(剛性=E, 質量=rho)
    hwall(d, ox - 120, ox + 120, 90, 1)
    spring(d, ox, 90, ox, 170)
    box(d, ox - 45, 170, ox + 45, 235, FILL2); ctext(d, ox, 202, "質量 ∝ rho", FT)
    ctext(d, ox + 80, 130, "剛性 ∝ E", FT, GRAY)
    arrow(d, ox, 235, ox, 285, BLUE, 3, 12); ctext(d, ox, 300, "振動", FT, BLUE)
    box(d, 80, 330, 590, 400, FILL1)
    ctext(d, 335, 356, "形状不変なら剛性∝E・質量∝rho → omega ∝ sqrt(E/rho)", FT)
    ctext(d, 335, 380, "rho→a rho, E→b E なら  omega_B = sqrt(b/a) omega_A", FT)
    save(im, "v1f9MaterialDependence")


# 9. 節と腹:荷重が節にあると共振しない
def f_node_antinode():
    im, d = new()
    title(d, "共振と荷重位置: 荷重がモードの節にあると共振しない")
    ox, oy = 110, 220
    axes(d, ox, oy, 470, 120, "", "")
    # モード形状(1周期の正弦=節と腹)
    A = 90
    pts = curve(lambda x: oy - A * math.sin(2 * math.pi * (x - ox) / 470), ox, ox + 470, 120)
    plot(d, 0, 0, pts, BLUE, 3)
    # 節(ゼロ交差)
    for k in (0, 0.5, 1.0):
        nx = ox + 470 * k
        node(d, nx, oy, 6, "white")
    ctext(d, ox + 235, oy + 22, "節(動かない)", FT, GRAY)
    # 腹
    ax1 = ox + 470 * 0.25
    ctext(d, ax1, oy - A - 16, "腹(大きく動く)", FT, GRAY)
    # 荷重を節に(共振しない)
    force(d, ox + 470 * 0.5, oy - 30, 0, 30, "荷重(節)", RED)
    ctext(d, ox + 470 * 0.5, oy + 60, "→ 励起されず共振しない", FT, RED)
    # 荷重を腹に(共振)
    force(d, ax1, oy - A - 34, 0, 30, "荷重(腹)", GREEN)
    ctext(d, ax1, oy - A - 60, "→ 共振する", FT, GREEN)
    save(im, "v1f9NodeAntinode")


# 10. 1自由度強制振動(不つり合い)の振幅・位相
def f_forced_response():
    im, d = new()
    title(d, "不つり合い励振の振幅A・位相遅れ phi (1自由度)")
    # 振幅曲線
    ox, oy = 100, 210
    axes(d, ox, oy, 220, 150, "omega", "A")
    def amp(x):
        r = (x - ox) / 60
        val = (r ** 2) / math.sqrt((1 - r ** 2) ** 2 + (0.18 * r) ** 2 + 1e-6)
        return oy - min(val * 20, 145)
    plot(d, 0, 0, curve(amp, ox + 5, ox + 215, 160), BLUE, 3)
    ctext(d, ox + 70, oy - 150, "共振で極大", FT, RED)
    dash(d, ox + 215, oy - 40, ox + 5, oy - 40, LGRAY)
    ctext(d, ox + 120, oy - 46, "mR/M に収束", FT, GRAY)
    # 位相曲線
    ox2 = 400
    axes(d, ox2, oy, 200, 150, "omega", "phi")
    def pha(x):
        r = (x - ox2) / 55
        p = math.atan2(0.18 * r, 1 - r ** 2)  # 0..pi
        return oy - p / math.pi * 140
    plot(d, 0, 0, curve(pha, ox2 + 5, ox2 + 195, 160), GREEN, 3)
    ctext(d, ox2 + 5, oy - 145, "pi", FT, GREEN, "lm")
    ctext(d, ox2 + 130, oy - 20, "共振でpiへ変化", FT, GREEN)
    note(d, "A=mR omega^2/sqrt((k-M omega^2)^2+(c omega)^2),  phi=atan(c omega/(k-M omega^2))")
    save(im, "v1f9ForcedResponse")


# 11. rpm換算(Hz×60=危険速度)
def f_rpm_conversion():
    im, d = new()
    title(d, "固有振動数[Hz] × 60 = 共振回転数[rpm]")
    cx, cy = 220, 200
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), outline=BLACK, width=3, fill=FILL1)
    node(d, cx, cy, 8, FILL2)
    # 偏心マス
    mx, my = cx + 50, cy - 40
    node(d, mx, my, 12, FILL3); ctext(d, mx, my, "m", FT)
    marc = math.radians(40)
    arrow(d, cx + 62 * math.cos(marc), cy - 62 * math.sin(marc),
          cx + 62 * math.cos(marc + 0.5), cy - 62 * math.sin(marc + 0.5), RED, 3, 11)
    ctext(d, cx, cy + 92, "回転数 N[rpm]", FT, GRAY)
    box(d, 380, 150, 600, 260, FILL1)
    ctext(d, 490, 180, "f=200Hz", FS)
    ctext(d, 490, 210, "↓ ×60", FT, RED)
    ctext(d, 490, 240, "N=12000rpm", FS)
    note(d, "回転数0で振動0(不つり合い力のみ). ある回転まで共振させない=固有振動数を上げる")
    save(im, "v1f9RpmConversion")


# 12. 初期応力(応力剛性化)と平板要素
def f_stress_stiffening():
    im, d = new()
    title(d, "初期応力(応力剛性化): 自重の面内引張が面外剛性を上げる")
    # 吊り下げパネル(下凸)
    x0, x1 = 150, 510
    node(d, x0, 120, 6, "white"); node(d, x1, 120, 6, "white")
    ctext(d, 330, 105, "低剛性ゴムで吊る", FT, GRAY)
    pts = curve(lambda x: 170 + 55 * math.sin(math.pi * (x - x0) / (x1 - x0)), x0, x1, 80)
    plot(d, 0, 0, pts, BLUE, 4)
    ctext(d, 330, 250, "自重で下凸に変形", FT, GRAY)
    # 面内引張力(両端外向き)
    force(d, x0, 175, -55, 0, "引張", RED)
    force(d, x1, 175, 55, 0, "引張", RED)
    # 重力
    arrow(d, 330, 200, 330, 250, GRAY, 2, 11); ctext(d, 345, 228, "重力", FT, GRAY, "lm")
    box(d, 80, 300, 590, 400, FILL1)
    ctext(d, 335, 325, "面内引張力 → 面外剛性UP → 固有振動数が上昇", FT)
    ctext(d, 335, 352, "面内・面外が連成 → 平面応力+板曲げを併せ持つ『平板要素』が必要", FT)
    ctext(d, 335, 379, "板曲げ要素だけだと実測より低い固有振動数が出る", FT, RED)
    save(im, "v1f9StressStiffening")


# 13. 歪エネルギー分担率でばね倍率を決める
def f_strain_energy_share():
    im, d = new()
    title(d, "歪エネルギー分担率でばね倍率を決定")
    # 剛体を4つのばねで支持
    hwall(d, 120, 540, 110, 1)
    bx0, bx1 = 170, 490
    by = 300
    box(d, bx0, by, bx1, by + 45, FILL2); ctext(d, (bx0 + bx1) / 2, by + 22, "剛体(上下振動)", FT)
    tops = [(200, "上5%"), (300, "上5%"), (360, "下30%"), (460, "下30%")]
    for sx, lab in tops:
        col = RED if "下" in lab else GRAY
        spring(d, sx, 130, sx, by, coils=5, amp=10)
        ctext(d, sx, 200, lab, FT, col)
    box(d, 90, 350, 590, 405, FILL1)
    ctext(d, 340, 372, "全体倍率=(f_new/f_old)^2.  Σ(分担率e_i × 倍率x_i)/100 = 全体倍率 を解く", FT)
    ctext(d, 340, 394, "分担60%の下2箇所: 0.6y+0.4=1.36 → y≒1.6倍", FT, RED)
    save(im, "v1f9StrainEnergyShare")


# 14. 歯車かみ合い周波数(スペクトルのピーク)
def f_gear_mesh():
    im, d = new()
    title(d, "歯車かみ合い周波数 = 回転数 × 歯数 × 次数")
    # 2つの歯車
    def gear(cx, cy, r, n=12):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=BLACK, width=3, fill=FILL1)
        for i in range(n):
            a = 2 * math.pi * i / n
            d.line((cx + r * math.cos(a), cy + r * math.sin(a),
                    cx + (r + 8) * math.cos(a), cy + (r + 8) * math.sin(a)), fill=BLACK, width=3)
        node(d, cx, cy, 5, "white")
    gear(150, 160, 34); gear(210, 160, 22)
    ctext(d, 180, 215, "歯数 Z / 回転数 n", FT, GRAY)
    # スペクトル
    ox, oy = 300, 300
    axes(d, ox, oy, 280, 150, "f", "音圧")
    for k, (fx, h) in enumerate([(70, 110), (170, 70), (250, 45)]):
        d.line((ox + fx, oy, ox + fx, oy - h), fill=BLUE, width=4)
        ctext(d, ox + fx, oy - h - 12, "%d次" % (k + 1), FT, GRAY)
    ctext(d, ox + 70, oy + 20, "かみ合い1次", FT, RED)
    note(d, "ピーク分離にはΔfを十分細かく(例Δf=20Hz). 粗いと各次を検出できない")
    save(im, "v1f9GearMesh")


# 15. 2入力系の出力PSD(クロススペクトル)
def f_two_input_psd():
    im, d = new()
    title(d, "2入力系の出力PSD: クロススペクトル項を含む")
    # 2入力→系→出力
    box(d, 90, 140, 200, 185, FILL2); ctext(d, 145, 162, "右入力 W_R", FT)
    box(d, 90, 235, 200, 280, FILL2); ctext(d, 145, 257, "左入力 W_L", FT)
    box(d, 300, 180, 430, 240, FILL1); ctext(d, 365, 200, "系", FS); ctext(d, 365, 224, "H_R, H_L", FT)
    arrow(d, 200, 162, 300, 195, GRAY, 2, 11)
    arrow(d, 200, 257, 300, 225, GRAY, 2, 11)
    box(d, 500, 185, 600, 235, FILL2); ctext(d, 550, 210, "出力 z", FS)
    arrow(d, 430, 210, 500, 210, GRAY, 2, 11)
    # 相関の弧
    d.arc((150, 150, 200, 270), -90, 90, fill=RED, width=2)
    ctext(d, 235, 210, "相関(P_RL)", FT, RED, "lm")
    box(d, 70, 300, 600, 400, FILL1)
    ctext(d, 335, 324, "P_z=|H_R|^2 P_RR + H_R* H_L P_RL + H_R H_L* P_RL* + |H_L|^2 P_LL", FT)
    ctext(d, 335, 350, "無相関のときだけ |H_R|^2 P_RR + |H_L|^2 P_LL で足りる", FT)
    ctext(d, 335, 376, "|H|の1乗の形は次元が合わず誤り", FT, RED)
    save(im, "v1f9TwoInputPSD")


# 16. 応答スペクトル法:多自由度→各モード1自由度系
def f_response_spectrum_method():
    im, d = new()
    title(d, "応答スペクトル法: 多自由度を各モードの1自由度系に分解")
    # 多自由度建屋
    bx = 130
    for i in range(3):
        yy = 260 - i * 45
        box(d, bx - 40, yy, bx + 40, yy + 40, FILL2)
    hwall(d, bx - 60, bx + 60, 260, 1)
    ctext(d, bx, 300, "多自由度系", FT, GRAY)
    arrow(d, bx - 90, 260, bx - 60, 260, RED, 3, 11); ctext(d, bx - 95, 240, "地震 z''", FT, RED, "rm")
    # 分解の矢印
    arrow(d, 200, 200, 270, 200, BLACK, 3, 13)
    # 各モードの1自由度系
    for k, ky in enumerate([150, 230, 310]):
        hwall(d, 320, 380, ky - 20, 1)
        spring(d, 350, ky - 20, 350, ky + 5, coils=4, amp=8)
        box(d, 335, ky + 5, 365, ky + 25, FILL2)
        ctext(d, 420, ky + 8, "モード%d: q%d" % (k + 1, k + 1), FT, BLUE, "lm")
    note(d, "q_i''+2 zeta_i omega_i q_i'+omega_i^2 q_i = -beta_i z''  (beta_i=刺激係数),  y_j=Σ phi_ji q_i")
    save(im, "v1f9ResponseSpectrumMethod")


# 17. SRSS:各モード最大を自乗和平方根で合成(絶対値和は過大)
def f_srss():
    im, d = new()
    title(d, "最大応答の合成: SRSS(自乗和の平方根)")
    ox, oy = 120, 250
    axes(d, ox, oy, 260, 170, "モード", "最大応答")
    vals = [130, 90, 60]
    for i, v in enumerate(vals):
        xx = ox + 50 + i * 70
        d.rectangle((xx - 20, oy - v, xx + 20, oy), outline=BLACK, width=2, fill=FILL2)
        ctext(d, xx, oy + 16, "q%d" % (i + 1), FT)
        ctext(d, xx, oy - v - 12, "%d" % v, FT, GRAY)
    box(d, 420, 140, 610, 300, FILL1)
    ctext(d, 515, 168, "絶対値和=130+90+60", FT, RED)
    ctext(d, 515, 190, "=280 (過大)", FT, RED)
    ctext(d, 515, 228, "SRSS=sqrt(130^2", FT, GREEN)
    ctext(d, 515, 250, "+90^2+60^2)", FT, GREEN)
    ctext(d, 515, 272, "≒166 (現実的)", FT, GREEN)
    note(d, "各モードは同時に最大にならない→SRSSで合成. 近接モードがあると誤差増")
    save(im, "v1f9SRSS")


# 18. 加速度応答スペクトル S_a(T,zeta)
def f_accel_response_spectrum():
    im, d = new()
    title(d, "加速度応答スペクトル S_a(T, zeta): 横軸=固有周期")
    ox, oy = 110, 320
    axes(d, ox, oy, 470, 240, "固有周期 T", "最大絶対加速度 S_a")
    def sa(x, sc):
        t = (x - ox) / 470
        return oy - sc * (200 * t * math.exp(-2.3 * t) + 8)
    for sc, lab, col in [(1.0, "zeta 小", RED), (0.7, "zeta 中", BLUE), (0.45, "zeta 大", GREEN)]:
        plot(d, 0, 0, curve(lambda x: sa(x, sc), ox + 5, ox + 465, 120), col, 3)
        ctext(d, ox + 430, sa(ox + 430, sc) - 12, lab, FT, col)
    note(d, "減衰比 zeta をパラメータに描く. 減衰大ほど応答小. 各モードのTからS_aを読む")
    save(im, "v1f9AccelResponseSpectrum")


# 19. 応答スペクトル法の限界(近接モードで誤差)
def f_spectrum_limit():
    im, d = new()
    title(d, "応答スペクトル法の性質と限界")
    ox, oy = 100, 200
    axes(d, ox, oy, 220, 120, "f", "")
    # 近接する2ピーク
    def two(x):
        return oy - (100 / (1 + ((x - (ox + 90)) / 12) ** 2) + 90 / (1 + ((x - (ox + 120)) / 12) ** 2))
    plot(d, 0, 0, curve(two, ox + 5, ox + 215, 160), BLUE, 3)
    ctext(d, ox + 105, oy - 130, "近接モード", FT, RED)
    ctext(d, ox + 105, oy + 22, "→ 相関強くSRSS誤差大", FT, RED)
    box(d, 360, 120, 610, 300, FILL1)
    ctext(d, 485, 148, "・多入力(別波)でも計算可", FT)
    ctext(d, 485, 178, "・出力=全期間の最大値", FT)
    ctext(d, 485, 200, "(時間断面ではない)", FT, GRAY)
    ctext(d, 485, 232, "・モード数を増やしても", FT)
    ctext(d, 485, 254, " 必ず精度向上しない", FT)
    ctext(d, 485, 282, "(応答が過大になる傾向)", FT, GRAY)
    save(im, "v1f9SpectrumLimit")


# 20. 流体連成(付加質量)
def f_added_mass():
    im, d = new()
    title(d, "流体連成(付加質量法): 周りの水を見かけの質量に")
    # 水中の配管断面
    box(d, 120, 130, 560, 320, fill=(232, 240, 250), col=BLUE, wd=2)
    ctext(d, 500, 150, "静止流体(水)", FT, BLUE)
    cx, cy = 300, 225
    d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), outline=BLACK, width=3, fill=FILL2)
    ctext(d, cx, cy, "構造", FT)
    # 引きずられる流体(付加質量)
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), outline=BLUE, width=2)
    ctext(d, cx, cy - 88, "付加質量(一緒に揺れる水)", FT, BLUE)
    arrow(d, cx - 40, cy, cx - 100, cy, RED, 4, 14); ctext(d, cx - 106, cy - 16, "運動", FT, RED, "rm")
    box(d, 90, 335, 590, 405, FILL1)
    ctext(d, 340, 360, "流れなし→付加質量で質量調整すれば応答スペクトル法・部分構造合成も適用可", FT)
    ctext(d, 340, 386, "付加質量を含めて固有値計算する方が精度が高い", FT)
    save(im, "v1f9AddedMass")


# 21. PSD入出力 P_0=|H|^2 P_i
def f_psd_input_output():
    im, d = new()
    title(d, "PSDの入出力関係: P_0(f) = |H(f)|^2 P_i(f)")
    # 入力PSD
    ox, oy = 90, 250
    axes(d, ox, oy, 130, 130, "f", "P_i")
    plot(d, 0, 0, curve(lambda x: oy - 70 * math.exp(-((x - (ox + 60)) / 40) ** 2), ox + 5, ox + 125, 60), GRAY, 3)
    ctext(d, ox + 60, oy + 18, "入力(軌道凹凸)", FT, GRAY)
    # 系
    box(d, 250, 200, 380, 260, FILL1); ctext(d, 315, 220, "|H(f)|^2", FS); ctext(d, 315, 244, "系", FT)
    arrow(d, 225, 225, 250, 225, GRAY, 2, 10)
    arrow(d, 380, 225, 410, 225, GRAY, 2, 10)
    # 出力PSD
    ox2 = 430
    axes(d, ox2, oy, 150, 130, "f", "P_0")
    plot(d, 0, 0, curve(lambda x: oy - 100 / (1 + ((x - (ox2 + 70)) / 18) ** 2), ox2 + 5, ox2 + 145, 80), BLUE, 3)
    ctext(d, ox2 + 70, oy + 18, "出力(車体応答)", FT, BLUE)
    note(d, "鉄車輪は軌道高低不整をトレース→P_iは軌道PSDと一対一. |H|は2乗で効く")
    save(im, "v1f9PsdInputOutput")


# 22. はり要素の応力(精度の限界)
def f_beam_stress():
    im, d = new()
    title(d, "はり要素の応力: 積分点で計算可だが断面変形は表せない")
    # はり要素(積分点)
    y0 = 160
    bar(d, 130, y0, 400, y0, 26, FILL2)
    for xx in (200, 330):
        d.line((xx, y0 - 13, xx, y0 + 13), fill=RED, width=2)
        node(d, xx, y0, 4, RED); ctext(d, xx, y0 - 28, "積分点", FT, RED)
    ctext(d, 265, y0 + 32, "はり要素(はり理論の応力)", FT, GRAY)
    # シェル/ソリッド(断面変形)
    y1 = 300
    d.ellipse((200, y1 - 22, 260, y1 + 22), outline=BLACK, width=3)
    d.ellipse((205, y1 - 14, 255, y1 + 30), outline=RED, width=2)
    ctext(d, 230, y1 + 44, "断面がつぶれる変形", FT, RED)
    arrow(d, 300, y1, 360, y1, GRAY, 2, 11)
    ctext(d, 470, y1, "シェル/ソリッドで再現", FT, BLACK, "lm")
    note(d, "はり要素は積分点数が少なく分布は粗い. 応力精度が要るならシェル/ソリッドで再計算")
    save(im, "v1f9BeamStress")


# 23. 周波数応答の振幅・位相の読み方
def f_phase_interpret():
    im, d = new()
    title(d, "周波数応答の読み方: 位相差で瞬間変位を判断")
    ox, oy = 90, 200
    axes(d, ox, oy, 480, 120, "omega t", "変位")
    A = 70
    # 基準 phi=0
    plot(d, 0, 0, curve(lambda x: oy - A * math.cos(2 * math.pi * (x - ox) / 240), ox + 5, ox + 475, 200), BLACK, 3)
    # phi=90
    plot(d, 0, 0, curve(lambda x: oy - A * math.cos(2 * math.pi * (x - ox) / 240 + math.pi / 2), ox + 5, ox + 475, 200), BLUE, 2)
    # phi=180
    plot(d, 0, 0, curve(lambda x: oy - A * math.cos(2 * math.pi * (x - ox) / 240 + math.pi), ox + 5, ox + 475, 200), RED, 2)
    # t=0 の縦線
    dash(d, ox + 5, oy - A - 20, ox + 5, oy + A + 20, LGRAY)
    ctext(d, ox + 5, oy + A + 34, "基準点が最大(+1.0)の瞬間", FT, GRAY)
    box(d, 90, 320, 590, 400, FILL1)
    ctext(d, 340, 344, "phi=0: +最大 / phi=90: 0 / phi=180: -最大 / phi=-90: 0", FT)
    ctext(d, 340, 372, "x(t)=A cos(omega t + phi). 振幅だけでなく位相を読む", FT)
    save(im, "v1f9PhaseInterpret")


if __name__ == "__main__":
    f_mac_matrix(); f_residual(); f_orthogonality(); f_compliance_modal()
    f_craig_bampton(); f_guyan_static(); f_cantilever_bending(); f_material_dependence()
    f_node_antinode(); f_forced_response(); f_rpm_conversion(); f_stress_stiffening()
    f_strain_energy_share(); f_gear_mesh(); f_two_input_psd(); f_response_spectrum_method()
    f_srss(); f_accel_response_spectrum(); f_spectrum_limit(); f_added_mass()
    f_psd_input_output(); f_beam_stress(); f_phase_interpret()
    print("done v1f9 formula (23)")
