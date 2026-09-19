# -*- coding: utf-8 -*-
"""熱流体1級 第5章 乱流解析と乱流モデル 公式・用語の図(接頭辞 t1f5)。
白地660x420線画・機構のみ。figlib.py を共通ライブラリとして使う。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def vprofile(d, x0, ybase, ytop, maxlen, col=BLUE, n=7, label=""):
    """壁(x0の左が壁)からのせん断速度分布。水平矢印で速度、長さは上ほど大。"""
    d.line((x0, ybase, x0, ytop), fill=BLACK, width=2)  # 壁
    for i in range(n + 1):
        y = ybase - (ybase - ytop) * i / n
        L = maxlen * (i / n) ** 0.6
        if L > 4:
            arrow(d, x0, y, x0 + L, y, col, 2, 8)
    # 速度分布の包絡線
    pts = []
    for i in range(n + 1):
        y = ybase - (ybase - ytop) * i / n
        L = maxlen * (i / n) ** 0.6
        pts.append((x0 + L, y))
    d.line(pts, fill=col, width=2)
    if label:
        ctext(d, x0 + maxlen / 2, ybase + 18, label, FT, col)


# 1 ブシネスク近似(分子粘性とのアナロジー)
def f_boussinesq():
    im, d = new(); title(d, "渦粘性近似:分子粘性とのアナロジー")
    vprofile(d, 120, 300, 90, 150, GRAY, 7, "")
    ctext(d, 175, 320, "分子粘性", FS)
    ctext(d, 175, 344, "τ = μ dU/dy", FT, GRAY)
    vprofile(d, 430, 300, 90, 150, BLUE, 7, "")
    ctext(d, 485, 320, "乱流(モデル)", FS)
    ctext(d, 485, 344, "-ρu'v' = ρ νt dU/dy", FT, BLUE)
    arrow(d, 300, 200, 360, 200, BLACK, 3, 12)
    ctext(d, 330, 182, "真似る", FT, RED)
    ctext(d, W / 2, 388, "u_i'u_j' = (2/3)k δij − νt(∂Ui/∂xj + ∂Uj/∂xi)", FS, BLACK)
    save(im, "t1f5Boussinesq")


# 2 渦粘性係数 νt=Cμk²/ε
def f_eddyvisc():
    im, d = new(); title(d, "渦粘性係数 νt = Cμ k² / ε")
    cx, cy = 300, 210
    for r in (95, 66, 38):
        d.arc((cx - r, cy - r, cx + r, cy + r), 20, 320, fill=BLUE, width=3)
    arrow(d, cx + 92, cy - 14, cx + 88, cy + 24, BLUE, 3, 12)  # 回転
    # 速度スケール
    arrow(d, cx, cy, cx + 150, cy, RED, 3, 12)
    ctext(d, cx + 95, cy - 16, "速度 √k", FT, RED)
    # 長さスケール
    dim(d, cx - 95, cy + 120, cx + 95, cy + 120, "長さ k^{3/2}/ε", 0, GRAY)
    ctext(d, W / 2, 372, "νt =(速度 √k)×(長さ k^{3/2}/ε)= Cμ k²/ε   (Cμ=0.09)", FS)
    save(im, "t1f5EddyVisc")


# 3/4 非等方性(実現象 vs 等方性モデル)
def f_anisotropy():
    im, d = new(); title(d, "レイノルズ応力の非等方性:実現象と等方性モデル")
    base = 320
    # 実現象 u'u'>w'w'>v'v'
    x0 = 90; heights = [150, 95, 55]; labs = ["u'u'", "w'w'", "v'v'"]
    for i, (h, lb) in enumerate(zip(heights, labs)):
        x = x0 + i * 60
        d.rectangle((x, base - h, x + 42, base), outline=BLACK, width=2, fill=FILL2)
        ctext(d, x + 21, base + 16, lb, FT)
    ctext(d, x0 + 60, 350, "実現象(非等方)", FS, BLUE)
    # 等方モデル 3本同じ 2k/3
    x0 = 400; h = 100
    for i, lb in enumerate(labs):
        x = x0 + i * 60
        d.rectangle((x, base - h, x + 42, base), outline=BLACK, width=2, fill=(255, 236, 236))
        ctext(d, x + 21, base + 16, lb, FT)
    d.line((x0 - 8, base - h, x0 + 3 * 60 - 12, base - h), fill=RED, width=2)
    ctext(d, x0 + 60, base - h - 14, "= 2k/3", FT, RED)
    ctext(d, x0 + 60, 350, "線形(等方)モデル", FS, RED)
    hwall(d, 70, 590, base, 1, 12)
    save(im, "t1f5Anisotropy")


# 5 モデル階層(線形→非線形→応力方程式)
def f_nonlinear():
    im, d = new(); title(d, "乱流モデルの階層:非等方性の再現と計算コスト")
    boxes = [("線形渦粘性\n(等方)", 70, FILL1),
             ("非線形渦粘性\n(2次以上)", 275, FILL2),
             ("応力方程式\n(6成分を解く)", 480, FILL3)]
    for txt, x, fl in boxes:
        d.rectangle((x, 150, x + 120, 230), outline=BLACK, width=3, fill=fl)
        for j, line in enumerate(txt.split("\n")):
            ctext(d, x + 60, 178 + j * 24, line, FT)
    arrow(d, 195, 190, 270, 190, BLACK, 3, 12)
    arrow(d, 400, 190, 475, 190, BLACK, 3, 12)
    arrow(d, 100, 300, 560, 300, RED, 3, 13)
    ctext(d, 330, 282, "非等方性の再現力・計算コスト 増加 →", FT, RED)
    save(im, "t1f5Nonlinear")


# 6 k-ε 5定数の校正表
def f_keconstants():
    im, d = new(); title(d, "標準k-εの5定数と校正に使う基準流れ")
    rows = [["定数", "値", "決め方(基準流れ)"],
            ["Cμ", "0.09", "乱流境界層の局所平衡"],
            ["Cε2", "1.92", "一様減衰乱流 k∝t^-1"],
            ["Cε1", "1.44", "対数速度分布"],
            ["σε", "1.3", "対数速度分布"],
            ["σk", "1.0", "実験的知見"]]
    x0, y0, rh = 60, 70, 48
    wcol = [90, 90, 360]
    for r, row in enumerate(rows):
        y = y0 + r * rh
        x = x0
        for c, cell in enumerate(row):
            d.rectangle((x, y, x + wcol[c], y + rh), outline=BLACK, width=2,
                        fill=FILL2 if r == 0 else "white")
            ctext(d, x + wcol[c] / 2, y + rh / 2, cell, FT)
            x += wcol[c]
    save(im, "t1f5KeConstants")


# 7 局所平衡(対数層 Pk≈ε)
def f_localequil():
    im, d = new(); title(d, "Cμの校正:対数層の局所平衡 Pk ≈ ε")
    wall(d, 110, 90, 330, 1, 10)
    vprofile(d, 130, 330, 120, 200, BLUE, 8, "平均速度 U(y)")
    # 局所平衡バンド
    d.rectangle((300, 150, 560, 250), outline=RED, width=2)
    ctext(d, 430, 175, "対数層:生成 Pk ≈ 散逸 ε", FT, RED)
    ctext(d, 430, 205, "-u'v'/k ≈ 0.3", FT, RED)
    ctext(d, 430, 230, "→ Cμ ≈ (u'v'/k)² ≈ 0.09", FT, RED)
    ctext(d, W / 2, 378, "使うのはせん断応力 u'v'(垂直応力 u'u' ではない)", FT, GRAY)
    save(im, "t1f5LocalEquil")


# 8 一様減衰乱流 k∝t^-1
def f_decay():
    im, d = new(); title(d, "Cε2の校正:一様減衰乱流 k ∝ t^-1")
    # 格子
    gx = 90
    for i in range(5):
        d.line((gx, 120 + i * 20, gx, 130 + i * 20), fill=BLACK, width=3)
    for i in range(5):
        y = 120 + i * 20
        d.arc((gx + 6, y - 6, gx + 26, y + 8), 0, 360, fill=GRAY, width=1)
    ctext(d, gx, 250, "格子", FT, GRAY)
    arrow(d, gx + 20, 200, gx + 120, 200, GRAY, 2, 10)
    ctext(d, gx + 70, 185, "流れ", FT, GRAY)
    # 減衰曲線
    ox, oy = 250, 330; axes(d, ox, oy, 320, 210, "t", "k")
    pts = []
    for i in range(1, 60):
        t = i / 6.0
        k = 180 / (t + 0.8)
        pts.append((ox + 30 + t * 34, oy - k))
    plot(d, ox, oy, pts, BLUE, 3)
    ctext(d, ox + 240, oy - 60, "k ∝ t^-1", FS, BLUE)
    ctext(d, ox + 200, oy - 150, "→ Cε2 ≈ 2 (標準1.92)", FT, RED)
    save(im, "t1f5Decay")


# 9 対数速度分布
def f_loglaw():
    im, d = new(); title(d, "対数速度分布 u+ = (1/κ)ln y+ + B")
    ox, oy = 120, 340; axes(d, ox, oy, 460, 250, "ln y+", "u+")
    # 粘性底層(直線)
    d.line((ox, oy, ox + 90, oy - 120), fill=GRAY, width=2)
    ctext(d, ox + 55, oy - 80, "u+=y+", FT, GRAY)
    # 対数域(直線 in semilog)
    pts = [(ox + 130, oy - 120), (ox + 430, oy - 235)]
    plot(d, ox, oy, pts, BLUE, 3)
    ctext(d, ox + 300, oy - 150, "対数域 傾き 1/κ", FT, BLUE)
    ctext(d, ox + 300, oy - 125, "切片 B", FT, BLUE)
    ctext(d, W / 2, 388, "Cε2−Cε1 = κ²/(σε √Cμ) から Cε1・σε を決める", FT, GRAY)
    save(im, "t1f5LogLaw")


# 10 壁面漸近挙動
def f_wallasymptote():
    im, d = new(); title(d, "壁面漸近挙動:k∝y²・ε∝y⁰・u'v'∝y³")
    wall(d, 90, 90, 340, 1, 10)
    ox, oy = 110, 340; axes(d, ox, oy, 470, 250, "y(壁からの距離)", "")
    xs = [i for i in range(0, 220)]
    def curve(f, col, lab, ly):
        pts = [(ox + x, oy - f(x / 220.0)) for x in xs]
        plot(d, ox, oy, pts, col, 3)
        ctext(d, ox + 235, ly, lab, FT, col)
    curve(lambda t: 210 * t * t, BLUE, "k ∝ y²", oy - 200)
    curve(lambda t: 150, GREEN, "ε ∝ y⁰(有限)", oy - 165)
    curve(lambda t: 210 * t ** 3, RED, "-u'v' ∝ y³", oy - 60)
    ctext(d, W / 2, 388, "→ νt ∝ y³ が要求(標準式 Cμk²/ε は y⁴ でズレる)", FT, GRAY)
    save(im, "t1f5WallAsymptote")


# 11 減衰関数 f_μ
def f_fmu():
    im, d = new(); title(d, "低Re型の減衰関数 fμ(壁で νt を弱める)")
    ox, oy = 120, 340; axes(d, ox, oy, 460, 250, "y+", "fμ")
    d.line((ox, oy - 200, ox + 440, oy - 200), fill=LGRAY, width=1)
    ctext(d, ox + 400, oy - 212, "fμ→1", FT, GRAY)
    pts = []
    for i in range(0, 441):
        yp = i / 440.0 * 8
        fm = (1 - math.exp(-yp)) ** 2
        pts.append((ox + i, oy - 200 * fm))
    plot(d, ox, oy, pts, BLUE, 3)
    ctext(d, ox + 60, oy - 40, "壁: fμ→0", FT, RED)
    ctext(d, ox + 300, oy - 150, "離れると 標準k-ε", FT, GRAY)
    save(im, "t1f5Fmu")


# 12 壁の扱い2方式
def f_walltreat():
    im, d = new(); title(d, "壁の扱い:壁関数法 と 低Re型モデル")
    # 左:壁関数(粗い格子)
    wall(d, 80, 90, 330, 1, 9)
    for gy in (110, 200, 290):
        d.line((80, gy, 250, gy), fill=LGRAY, width=1)
    node(d, 80 + 60, 200, 5, RED)
    ctext(d, 165, 360, "壁関数法:粗い格子", FT)
    ctext(d, 165, 382, "底層は対数則で橋渡し", FT, GRAY)
    # 右:低Re(細かい格子)
    wall(d, 430, 90, 330, 1, 9)
    for gy in range(110, 331, 18):
        d.line((430, gy, 600, gy), fill=LGRAY, width=1)
    ctext(d, 515, 360, "低Re型:壁まで細かく", FT)
    ctext(d, 515, 382, "y+≲1・fμ で直接積分", FT, GRAY)
    save(im, "t1f5WallTreat")


# 13 系回転(回転チャネル)
def f_rotation():
    im, d = new(); title(d, "系回転と標準k-ε:非対称な u'v' を出せない")
    hwall(d, 120, 540, 110, -1, 12)
    hwall(d, 120, 540, 320, 1, 12)
    ctext(d, 90, 110, "圧力側", FT, GRAY); ctext(d, 90, 320, "負圧側", FT, GRAY)
    # 回転
    cx, cy = 330, 215
    d.arc((cx - 30, cy - 30, cx + 30, cy + 30), 30, 300, fill=GREEN, width=3)
    arrow(d, cx + 26, cy - 14, cx + 22, cy + 18, GREEN, 3, 11)
    ctext(d, cx, cy + 46, "回転 Ω", FT, GREEN)
    # 実際の非対称 u'v'(実線) と 標準k-ε対称(破線)
    pts = [(160 + i * 3.6, 215 - 80 * math.sin((i / 100.0) * math.pi) * (1 - 0.5 * (i / 100.0 - 0.5))) for i in range(101)]
    plot(d, 0, 0, pts, RED, 3)
    ctext(d, 470, 150, "実際:非対称(実線)", FT, RED)
    for i in range(0, 101, 6):
        x = 160 + i * 3.6; y = 215 - 70 * math.sin((i / 100.0) * math.pi)
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=GRAY)
    ctext(d, 470, 290, "標準k-ε:対称(点線)", FT, GRAY)
    save(im, "t1f5Rotation")


# 14 LES エネルギースペクトルとカットオフ
def f_les():
    im, d = new(); title(d, "LES:大きな渦は解像・小さな渦(SGS)はモデル")
    ox, oy = 110, 340; axes(d, ox, oy, 470, 250, "波数 k(小←大きな渦)", "E(k)")
    pts = []
    for i in range(5, 440):
        k = i / 440.0
        E = 200 * (k + 0.05) ** (-0.5) * math.exp(-3 * k)
        pts.append((ox + i, oy - min(E, 230)))
    plot(d, ox, oy, pts, BLUE, 3)
    xc = ox + 250
    d.line((xc, oy, xc, oy - 240), fill=RED, width=2)
    ctext(d, xc, oy - 252, "格子カットオフ", FT, RED)
    ctext(d, ox + 110, oy - 120, "解像(直接計算)", FT, GREEN)
    ctext(d, xc + 90, oy - 90, "SGS(モデル)", FT, ORANGE)
    save(im, "t1f5LES")


# 15 スマゴリンスキー(標準/ダイナミック)
def f_smagorinsky():
    im, d = new(); title(d, "スマゴリンスキー:標準 と ダイナミック")
    # 左:標準(固定Cs)
    x0, y0 = 70, 110
    for i in range(4):
        for j in range(4):
            d.rectangle((x0 + j * 32, y0 + i * 32, x0 + j * 32 + 32, y0 + i * 32 + 32),
                        outline=LGRAY, width=1)
    dim(d, x0, y0 + 145, x0 + 32, y0 + 145, "Δ", 0, GRAY)
    ctext(d, x0 + 64, 300, "標準:Cs 固定・等方", FT)
    ctext(d, x0 + 64, 322, "壁近傍/遷移に弱い", FT, GRAY)
    # 右:ダイナミック(テストフィルタ)
    x1 = 400
    for i in range(4):
        for j in range(4):
            d.rectangle((x1 + j * 32, y0 + i * 32, x1 + j * 32 + 32, y0 + i * 32 + 32),
                        outline=LGRAY, width=1)
    d.rectangle((x1, y0, x1 + 64, y0 + 64), outline=RED, width=3)
    ctext(d, x1 + 110, y0 + 32, "テストフィルタ", FT, RED)
    ctext(d, x1 + 64, 300, "ダイナミック:Csを", FT)
    ctext(d, x1 + 64, 322, "解像場から局所・逐次決定", FT, GRAY)
    ctext(d, W / 2, 372, "νSGS =(Cs Δ)² |S|", FS, BLUE)
    save(im, "t1f5Smagorinsky")


# 16 DES(翼まわり)
def f_des():
    im, d = new(); title(d, "DES:壁近傍RANS + 離れLES(ハイブリッド)")
    # 翼型
    pts = [(120, 250)]
    for i in range(1, 40):
        t = i / 40.0
        x = 120 + t * 260
        yt = 40 * math.sin(math.pi * t) * (1 - t) ** 0.5
        pts.append((x, 250 - yt))
    for i in range(40, -1, -1):
        t = i / 40.0
        x = 120 + t * 260
        yb = 12 * math.sin(math.pi * t)
        pts.append((x, 250 + yb))
    d.polygon(pts, outline=BLACK, width=3, fill=FILL1)
    # 境界層バンド(RANS)
    d.line([(p[0], p[1] - 10) for p in pts[:40]], fill=BLUE, width=2)
    ctext(d, 250, 300, "壁近傍:RANS(薄い層)", FT, BLUE)
    # 後流LES渦
    for cx in (430, 480, 530, 470, 520):
        cy = 235 if cx in (430, 530, 520) else 265
        r = 16
        d.arc((cx - r, cy - r, cx + r, cy + r), 0, 300, fill=ORANGE, width=2)
    ctext(d, 500, 180, "後流:LES(大規模渦)", FT, ORANGE)
    save(im, "t1f5DES")


# 17 DNS コスト ∝ Re³
def f_dns():
    im, d = new(); title(d, "DNS:最小渦まで解像・総計算 ∝ Re³")
    # 大渦の中の小渦(コルモゴロフ)
    d.rectangle((70, 110, 250, 290), outline=BLACK, width=2)
    d.arc((90, 130, 230, 270), 0, 360, fill=BLUE, width=2)
    for cx, cy in [(120, 160), (190, 150), (150, 210), (200, 230), (110, 240)]:
        d.arc((cx - 12, cy - 12, cx + 12, cy + 12), 0, 360, fill=GRAY, width=1)
    ctext(d, 160, 305, "最小渦(コルモゴロフ)まで", FT, GRAY)
    # スケーリング
    arrow(d, 300, 200, 380, 200, BLACK, 3, 12)
    ctext(d, 340, 182, "Re×10", FT, RED)
    ctext(d, 500, 150, "格子 N ∝ Re^{9/4}", FT)
    ctext(d, 500, 180, "刻み Δt ∝ Re^{-3/4}", FT)
    ctext(d, 500, 215, "総計算 ∝ Re³", FS, RED)
    ctext(d, 500, 245, "(Re10倍で1000倍)", FT, GRAY)
    save(im, "t1f5DNS")


# 18 空力音(直接/分離)
def f_aeroacoustics():
    im, d = new(); title(d, "流体音:直接計算 と 分離計算")
    # 直接
    d.arc((70, 160, 150, 240), 0, 360, fill=BLUE, width=2)
    ctext(d, 110, 200, "音源", FT, BLUE)
    for r in (55, 80, 105):
        d.arc((110 - r, 200 - r, 110 + r, 200 + r), -60, 60, fill=RED, width=2)
    ctext(d, 150, 310, "直接:同一格子で音まで", FT)
    ctext(d, 150, 332, "フィードバック可・激重", FT, GRAY)
    # 分離
    d.arc((410, 160, 490, 240), 0, 360, fill=BLUE, width=2)
    ctext(d, 450, 200, "音源", FT, BLUE)
    arrow(d, 500, 200, 560, 200, BLACK, 2, 10)
    for r in (30, 55, 80):
        d.arc((580 - r, 200 - r, 580 + r, 200 + r), -60, 60, fill=RED, width=2)
    ctext(d, 490, 310, "分離:音源→伝播を別々", FT)
    ctext(d, 490, 332, "軽いがFB不可", FT, GRAY)
    save(im, "t1f5Aeroacoustics")


# 19 SGDH(渦拡散型熱流束)
def f_sgdh():
    im, d = new(); title(d, "渦拡散型(SGDH):流れ方向熱流束を出せない")
    hwall(d, 110, 560, 330, 1, 12)
    ctext(d, 90, 330, "壁", FT, GRAY)
    # 温度勾配(壁垂直)
    arrow(d, 200, 320, 200, 120, ORANGE, 3, 12); ctext(d, 175, 110, "∂Θ/∂y", FT, ORANGE)
    # 熱流束(垂直のみ)
    arrow(d, 340, 320, 340, 150, RED, 4, 14); ctext(d, 375, 220, "v'θ' (垂直)", FT, RED)
    arrow(d, 460, 220, 520, 220, GRAY, 2, 10)
    d.line((490, 205, 505, 235), fill=RED, width=3); d.line((490, 235, 505, 205), fill=RED, width=3)
    ctext(d, 505, 250, "u'θ'=0(流れ方向)", FT, RED)
    ctext(d, W / 2, 388, "u_i'θ' = −(νt/Prt) ∂Θ/∂x_i", FS, BLUE)
    save(im, "t1f5SGDH")


# 20 GGDH
def f_ggdh():
    im, d = new(); title(d, "GGDH:レイノルズ応力経由で流れ方向熱流束を再現")
    hwall(d, 110, 560, 330, 1, 12)
    ctext(d, 90, 330, "壁", FT, GRAY)
    arrow(d, 200, 320, 200, 120, ORANGE, 3, 12); ctext(d, 175, 110, "∂Θ/∂y", FT, ORANGE)
    arrow(d, 340, 320, 340, 150, RED, 4, 14); ctext(d, 300, 150, "v'θ'", FT, RED)
    arrow(d, 340, 235, 470, 235, GREEN, 4, 14); ctext(d, 440, 215, "u'θ'≠0", FT, GREEN)
    ctext(d, 470, 290, "u'v' 経由で再現", FT, GREEN)
    ctext(d, 470, 315, "v'v'(壁で減衰)→減衰関数不要", FT, GRAY)
    ctext(d, W / 2, 388, "u_i'θ' = −Ct (k/ε) u_i'u_j' ∂Θ/∂x_j", FS, BLUE)
    save(im, "t1f5GGDH")


# 21 温度場の壁面境界条件
def f_tempfield():
    im, d = new(); title(d, "温度場モデル kθ-εθ の壁面境界条件")
    wall(d, 110, 90, 340, 1, 10)
    ox, oy = 130, 340; axes(d, ox, oy, 430, 250, "y", "")
    # k∝y²(壁でk=0)
    pts = [(ox + x, oy - 200 * (x / 200.0) ** 2) for x in range(0, 201)]
    plot(d, ox, oy, pts, BLUE, 3); ctext(d, ox + 210, oy - 150, "k(壁で0)", FT, BLUE)
    # kθ(∂kθ/∂y=0:壁で水平)
    pts = [(ox + x, oy - (60 + 130 * (1 - math.exp(-(x / 90.0))))) for x in range(0, 220)]
    plot(d, ox, oy, pts, RED, 3); ctext(d, ox + 230, oy - 120, "kθ(∂kθ/∂y=0)", FT, RED)
    ctext(d, W / 2, 384, "k=0, ε=ν∂²k/∂y², ∂kθ/∂y=0, εθ=α∂²kθ/∂y²", FT, GRAY)
    save(im, "t1f5TempField")


# 22 粗面の対数則(切片Cの下方シフト)
def f_roughwall():
    im, d = new(); title(d, "粗面:傾き1/κは不変・切片Cを下方シフト")
    ox, oy = 120, 340; axes(d, ox, oy, 460, 250, "log(uτ y/ν)", "u/uτ")
    # 滑面
    plot(d, ox, oy, [(ox + 40, oy - 90), (ox + 430, oy - 235)], BLUE, 3)
    ctext(d, ox + 360, oy - 210, "滑面 C=5.0", FT, BLUE)
    # 粗面(同じ傾き・下)
    plot(d, ox, oy, [(ox + 40, oy - 40), (ox + 430, oy - 185)], RED, 3)
    ctext(d, ox + 360, oy - 130, "粗面 C小", FT, RED)
    arrow(d, ox + 300, oy - 200, ox + 300, oy - 155, GRAY, 2, 10)
    ctext(d, ox + 335, oy - 178, "下方シフト", FT, GRAY)
    save(im, "t1f5RoughWall")


# 23 第二種二次流れ(矩形断面の隅渦)
def f_secondary():
    im, d = new(); title(d, "第二種二次流れ:矩形断面の隅に向かう渦")
    x0, y0, s = 190, 90, 240
    d.rectangle((x0, y0, x0 + s, y0 + s), outline=BLACK, width=3)
    cx, cy = x0 + s / 2, y0 + s / 2
    corners = [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]
    for i, (cxx, cyy) in enumerate(corners):
        # 隅へ向かう対の小渦(矢印)
        mx, my = (cxx + cx) / 2, (cyy + cy) / 2
        d.arc((mx - 26, my - 26, mx + 26, my + 26), 0, 300, fill=BLUE, width=2)
        ax = cxx + (cx - cxx) * 0.18; ay = cyy + (cy - cyy) * 0.18
        arrow(d, mx, my, ax, ay, RED, 2, 9)
    ctext(d, cx, y0 + s + 24, "断面内2方向の乱れの差 → 隅へ向かう二次流れ", FT, GRAY)
    ctext(d, cx, y0 + s + 46, "等方性モデルでは再現不可(非線形/応力モデルが必要)", FT, GRAY)
    save(im, "t1f5Secondary")


if __name__ == "__main__":
    f_boussinesq(); f_eddyvisc(); f_anisotropy(); f_nonlinear(); f_keconstants()
    f_localequil(); f_decay(); f_loglaw(); f_wallasymptote(); f_fmu()
    f_walltreat(); f_rotation(); f_les(); f_smagorinsky(); f_des()
    f_dns(); f_aeroacoustics(); f_sgdh(); f_ggdh(); f_tempfield()
    f_roughwall(); f_secondary()
    print("done ch5 formula figures")
