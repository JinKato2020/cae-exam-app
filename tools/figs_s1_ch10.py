# -*- coding: utf-8 -*-
"""固体1級 第10章 解析の検証 —— 問題図(接頭辞 s1e10)。白地660x420・黒線画。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

# ---- 共通ヘルパ ----
def box(d, cx, cy, w, h, lines, fnt=FT, fill="white", bcol=BLACK, tcol=BLACK, lh=None):
    d.rectangle((cx-w/2, cy-h/2, cx+w/2, cy+h/2), outline=bcol, width=3, fill=fill)
    if isinstance(lines, str): lines = [lines]
    lh = lh or (fnt.size + 6)
    y0 = cy - (len(lines)-1)*lh/2
    for i, ln in enumerate(lines):
        ctext(d, cx, y0+i*lh, ln, fnt, tcol)

def cross_axes(d, cx, cy, hw, hh, xl="e", yl="s"):
    arrow(d, cx-hw, cy, cx+hw, cy, BLACK, 2, 9); ctext(d, cx+hw+8, cy, xl, FT, BLACK, "lm")
    arrow(d, cx, cy+hh, cx, cy-hh, BLACK, 2, 9); ctext(d, cx, cy-hh-10, yl, FT, BLACK)

def poly_data(d, cx, cy, sx, sy, pts, col=BLUE, wd=3):
    px = [(cx+e*sx, cy-s*sy) for (e, s) in pts]
    d.line(px, fill=col, width=wd, joint="curve")
    return px


# ================= 10-1 VerifySteps =================
def f_verify_steps():
    im, d = new(); title(d, "非線形解析の標準手順(4段階)とASME V&V対応")
    stages = [("(1)単純化モデル", "プログラム検証"),
              ("(2)線形解析", "計算結果の検証"),
              ("(3)非線形解析", "妥当性確認"),
              ("(4)パラメータ感度", "不確かさの定量化")]
    xs = [95, 253, 411, 569]; cy = 210; w, h = 138, 96
    for i, (a, b) in enumerate(stages):
        box(d, xs[i], cy, w, h, "")
        ctext(d, xs[i], cy-16, a, FS, BLACK)
        ctext(d, xs[i], cy+18, b, FT, GRAY)
        if i < 3:
            arrow(d, xs[i]+w/2, cy, xs[i+1]-w/2, cy, BLACK, 3, 12)
    note(d, "単純なものから段階的に確認 → 最後に感度で確からしさを見る")
    save(im, "s1e10VerifySteps")

# ================= 10-2 DiskCollapse =================
def f_disk_collapse():
    im, d = new(); title(d, "外周固定・一様圧力を受ける円板(軸対称断面)")
    axl = 108; edge = 540; yt = 205; yb = 240
    # 対称軸
    for yy in range(150, 300, 12):
        d.line((axl, yy, axl, yy+6), fill=GRAY, width=1)
    ctext(d, axl, 138, "対称軸", FT, GRAY)
    # 板(断面)
    d.rectangle((axl, yt, edge, yb), outline=BLACK, width=3, fill=FILL1)
    # 圧力 p 下向き
    for x in range(140, 521, 48):
        arrow(d, x, 168, x, yt-2, BLUE, 3, 10)
    ctext(d, 330, 156, "一様圧力 p", FS, BLUE)
    # 固定端(右) ハッチ壁
    wall(d, edge, 185, 260, side=1, n=8)
    ctext(d, edge+26, 275, "固定", FT, BLACK)
    # 塑性ヒンジ(固定端近傍 と 中央)
    d.rectangle((edge-34, yt, edge, yb), outline=RED, width=2, fill=(250, 220, 220))
    d.rectangle((axl, yt, axl+30, yb), outline=RED, width=2, fill=(250, 220, 220))
    ctext(d, edge-70, 285, "塑性ヒンジ", FT, RED)
    ctext(d, axl+95, 285, "(中央にも降伏域)", FT, RED)
    # 寸法 a, t
    dim(d, axl, 320, edge, 320, "半径 a=250mm", col=GRAY)
    dim(d, 88, yt, 88, yb, "t", col=GRAY)
    ctext(d, 60, 223, "板厚t=25", FT, GRAY)
    note(d, "全塑性モーメント M0=Sy t^2/4, 崩壊荷重 pc=2.08*6M0/a^2 ≒ 7.96MPa")
    save(im, "s1e10DiskCollapse")

# ================= 10-3 MeshAspect =================
def f_mesh_aspect():
    im, d = new(); title(d, "要素アスペクト比と崩壊荷重の収束")
    # 良い要素
    d.rectangle((70, 120, 150, 200), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 110, 224, "良い(比≒1)", FT, GREEN)
    # 悪い要素(細長い)
    d.rectangle((55, 270, 165, 300), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 110, 320, "悪い(細長い)", FT, RED)
    ctext(d, 110, 96, "同じ面積でも比で精度が変わる", FT, GRAY)
    # 圧力-中央変位曲線
    ox, oy = 370, 340
    axes(d, ox, oy, 250, 220, "中央変位", "圧力")
    pts = [(ox+8, oy-14), (ox+60, oy-95), (ox+95, oy-150), (ox+120, oy-180),
           (ox+150, oy-195), (ox+200, oy-200), (ox+245, oy-201)]
    plot(d, ox, oy, pts, BLUE, 3)
    # 崩壊荷重(急増点)
    kx, ky = ox+120, oy-180
    d.line((ox, ky, kx, ky), fill=RED, width=2)
    d.line((kx, oy, kx, ky), fill=LGRAY, width=1)
    node(d, kx, ky, 5, RED, RED)
    ctext(d, ox-6, ky, "pc", FT, RED, "rm")
    ctext(d, kx+70, ky-6, "変形が急増=崩壊荷重", FT, RED)
    save(im, "s1e10MeshAspect")

# ================= 10-4 PunchLimit =================
def f_punch_limit():
    im, d = new(); title(d, "パンチ押込み問題(半無限を有限領域で近似)")
    x0, x1, y0, y1 = 95, 565, 150, 350
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3, fill=(250, 250, 250))
    # 剛体パンチ
    px0, px1 = 265, 395
    d.rectangle((px0, 118, px1, y0), outline=BLACK, width=3, fill=FILL3)
    for x in range(px0+10, px1, 26):
        arrow(d, x, 96, x, 116, RED, 3, 9)
    ctext(d, 330, 130, "剛体パンチ", FS, BLACK)
    # 塑性すべり域(扇形の破線)
    cx = 330
    for r in (70, 120, 165):
        d.arc((cx-r, y0-r, cx+r, y0+r), 0, 180, fill=GRAY, width=2)
    d.line((px0, y0, x0+40, y1-20), fill=GRAY, width=1)
    d.line((px1, y0, x1-40, y1-20), fill=GRAY, width=1)
    ctext(d, cx, y0+80, "塑性すべり域", FS, GRAY)
    # ディリクレ境界(側面・底面ハッチ)
    hwall(d, x0, x1, y1, side=-1, n=16)
    wall(d, x0, y0, y1, side=1, n=8); wall(d, x1, y0, y1, side=-1, n=8)
    ctext(d, 330, y1+28, "ディリクレ境界(領域を変え収束を確認)", FT, BLACK)
    save(im, "s1e10PunchLimit")

# ================= 10-5 CantHinge =================
def f_cant_hinge():
    im, d = new(); title(d, "片持ちはり5要素・積分点位置と有効スパン")
    x0, x1, yb = 108, 560, 210
    wall(d, x0, 150, 270, side=1, n=8)
    bar(d, x0, yb, x1, yb, thick=26, fill=FILL1)
    n = 5; xs = [x0 + (x1-x0)*i/n for i in range(n+1)]
    for x in xs:
        node(d, x, yb, 5)
    ips = [(xs[i]+xs[i+1])/2 for i in range(n)]
    for x in ips:
        ctext(d, x, yb, "×", FS, RED)
    ctext(d, ips[0], yb-40, "積分点(要素中央)", FT, RED)
    # 荷重P
    arrow(d, x1, yb-70, x1, yb-14, RED, 4, 14); ctext(d, x1+8, yb-45, "P", F, RED, "lm")
    # 塑性ヒンジ=最寄り積分点
    d.line((ips[0], yb-16, ips[0], yb+16), fill=RED, width=3)
    ctext(d, ips[0], yb+46, "塑性ヒンジ", FT, RED)
    # 寸法
    dim(d, x0, yb+70, ips[0], yb+70, "L/10", col=GRAY)
    dim(d, ips[0], yb+95, x1, yb+95, "有効スパン 9L/10", col=GRAY)
    note(d, "P_FEM=Mp/(9L/10)=10Mp/9L(理論 Mp/L の約1.11倍)")
    save(im, "s1e10CantHinge")

# ================= 10-6 PlateBuckle =================
def f_plate_buckle():
    im, d = new(); title(d, "a/b=2 単純支持板の座屈モード(対称条件の影響)")
    xL, xR = 120, 540; a = xR - xL
    def panel(cy, m, lab, col):
        d.rectangle((xL, cy-52, xR, cy+52), outline=BLACK, width=2, fill=(252, 252, 252))
        # 変形前
        d.line((xL, cy, xR, cy), fill=LGRAY, width=1)
        pts = []
        for i in range(0, 201):
            x = xL + a*i/200
            y = cy - 40*math.sin(m*math.pi*i/200)
            pts.append((x, y))
        d.line(pts, fill=col, width=3, joint="curve")
        # 対称線 x=a/2
        xc = (xL+xR)/2
        for yy in range(cy-52, cy+52, 10):
            d.line((xc, yy, xc, yy+5), fill=GRAY, width=1)
        ctext(d, xL-8, cy, lab, FT, col, "rm")
    panel(140, 2, "m=2", BLUE)
    ctext(d, 330, 205, "m=2:反対称(本来の最小)/対称条件で消える", FT, BLUE)
    panel(300, 3, "m=3", RED)
    ctext(d, 330, 366, "m=3:対称条件を満たす → 座屈荷重 約1.17倍", FT, RED)
    ctext(d, 330+8, 88, "x=a/2 対称線", FT, GRAY, "lm")
    save(im, "s1e10PlateBuckle")

# ================= 10-7 CreepRedist =================
def f_creep_redist():
    im, d = new(); title(d, "定常クリープの応力再分布(厚肉円筒)")
    ox, oy = 80, 320; xlen, ylen = 330, 220
    axes(d, ox, oy, xlen, ylen, "log(時間)", "相当応力")
    x0, x1 = ox+10, ox+xlen-10
    asy_in, asy_out = oy-115, oy-150   # 内面はやや低い定常, 外面は高い定常(pixel: 上=大)
    st_in, st_out = oy-200, oy-45
    def approach(start, asym):
        pts = []
        for i in range(0, 101):
            x = x0 + (x1-x0)*i/100
            y = asym + (start-asym)*math.exp(-3.0*i/100)
            pts.append((x, y))
        return pts
    d.line(approach(st_in, asy_in), fill=RED, width=3, joint="curve")
    d.line(approach(st_out, asy_out), fill=BLUE, width=3, joint="curve")
    d.line((x0, asy_in, x1, asy_in), fill=LGRAY, width=1)
    d.line((x0, asy_out, x1, asy_out), fill=LGRAY, width=1)
    ctext(d, x1-30, st_in-12, "内面(低下)", FT, RED)
    ctext(d, x1-30, st_out+14, "外面(上昇)", FT, BLUE)
    ctext(d, x1+6, asy_out, "一定値に漸近", FT, GRAY, "lm")
    # 断面インセット
    cx, cy = 545, 130
    d.ellipse((cx-58, cy-58, cx+58, cy+58), outline=BLACK, width=3)
    d.ellipse((cx-28, cy-28, cx+28, cy+28), outline=BLACK, width=3, fill="white")
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        arrow(d, cx+28*math.cos(a), cy+28*math.sin(a), cx+45*math.cos(a), cy+45*math.sin(a), BLUE, 2, 7)
    ctext(d, cx, cy, "p", FS, BLUE)
    ctext(d, cx, cy+72, "内半径a・外半径b", FT, BLACK)
    save(im, "s1e10CreepRedist")

# ================= 10-8 WeldCouple =================
def f_weld_couple():
    im, d = new(); title(d, "溶接残留応力=熱→応力の一方向解析(完全連成不要)")
    labs = ["非定常\n熱伝導解析", "各時刻の\n温度場", "熱弾塑性\n解析", "残留応力"]
    xs = [95, 253, 411, 569]; cy = 190; w, h = 132, 92
    for i, s in enumerate(xs):
        box(d, s, cy, w, h, labs[i].split("\n"), FS)
        if i < 3:
            arrow(d, s+w/2, cy, xs[i+1]-w/2, cy, BLACK, 3, 12)
    # 戻り不可(応力→温度は独立)
    d.line((xs[2], cy+h/2+8, xs[0], cy+h/2+8), fill=LGRAY, width=2)
    ax = (xs[0]+xs[2])/2
    ctext(d, ax, cy+h/2+8, "×", F, RED)
    ctext(d, ax, cy+h/2+34, "応力場→温度場は戻さない(独立)", FT, RED)
    note(d, "温度履歴の実験比較は溶融池近傍で行う")
    save(im, "s1e10WeldCouple")

# ================= 10-9 Hardening =================
def f_hardening():
    im, d = new(); title(d, "硬化則(等方・移動・複合)とバウシンガー効果")
    sx, sy = 17, 36; hw, hh = 82, 92; cy = 205
    def panel(cx, ttl, loops, notes, marks):
        cross_axes(d, cx, cy, hw, hh, "e", "s")
        ctext(d, cx, cy-hh-24, ttl, FS, BLACK)
        for pts, col, wd in loops:
            poly_data(d, cx, cy, sx, sy, pts, col, wd)
        for (mx, my, txt, col) in marks:
            node(d, cx+mx*sx, cy-my*sy, 4, col, col)
        for j, (t, col) in enumerate(notes):
            ctext(d, cx, cy+hh+18+j*17, t, FT, col)
    # 等方硬化: 反転再降伏が対称(-σmax), 弾性除荷幅=2σmax, 閉じず拡大
    iso = [(0, 0), (1, 1), (4, 1.45), (1.1, -1.45), (-3, -2.06), (1.12, 2.06)]
    panel(115, "等方硬化",
          [([(0, 0), (1, 1), (4, 1.45)], GRAY, 2), (iso[2:], BLUE, 3)],
          [("再降伏は-σmaxと対称", BLUE), ("(バウシンガー無し)", GRAY)],
          [(1.1, -1.45, "", RED)])
    # 移動硬化: 弾性域=2σy一定, バウシンガーあり, 安定した閉ループ
    kin_v = [(0, 0), (1, 1), (4, 1.4)]
    kin = [(4, 1.4), (2, -0.6), (-4, -1.4), (-2, 0.6), (4, 1.4)]
    panel(330, "移動硬化",
          [(kin_v, GRAY, 2), (kin, BLUE, 3)],
          [("弾性域2σyで平行移動", BLUE), ("=安定な閉ループ", GREEN)],
          [(2, -0.6, "", RED)])
    ctext(d, 330+2*sx+8, cy+0.6*sy, "早期再降伏", FT, RED, "lm")
    # 複合: 中間
    comb = [(0, 0), (4, 1.4), (1.6, -1.0), (-4, -1.55), (-1.6, 0.85), (4, 1.55)]
    panel(545, "複合硬化",
          [(comb, BLUE, 3)],
          [("移動+等方の中間", BLUE), ("ラチェットに最適", GREEN)],
          [(1.6, -1.0, "", RED)])
    save(im, "s1e10Hardening")

# ================= 10-11 NormalDist =================
def f_normal_dist():
    im, d = new(); title(d, "正規分布:標準偏差σ と 平均値の標準偏差 σ/√n")
    ox, oy = 90, 330; xlen = 480
    d.line((ox, oy, ox+xlen, oy), fill=BLACK, width=2)
    mu = ox + xlen/2
    for yy in range(oy, 95, -10):
        d.line((mu, yy, mu, yy-5), fill=GRAY, width=1)
    ctext(d, mu, oy+18, "μ(平均)", FT, BLACK)
    def bell(sig_px, amp, col, wd):
        pts = []
        for x in range(ox+5, ox+xlen-4, 3):
            z = (x-mu)/sig_px
            pts.append((x, oy - amp*math.exp(-0.5*z*z)))
        d.line(pts, fill=col, width=wd, joint="curve")
    bell(120, 150, BLUE, 3)   # 測定値のばらつき σ(広い)
    bell(54, 210, RED, 3)     # 平均値のばらつき σ/√n(狭く高い)
    ctext(d, mu+150, oy-70, "測定値のばらつき σ", FT, BLUE)
    ctext(d, mu+120, oy-190, "平均値のばらつき σ/√n", FT, RED)
    # 幅の対比
    dim(d, mu, oy-40, mu+120, oy-40, "σ", col=BLUE)
    dim(d, mu, oy-150, mu+54, oy-150, "σ/√n", col=RED)
    note(d, "sx=√(Σ(Si-S̄)^2/(n-1)), 標準誤差=sx/√n(√nで割る)")
    save(im, "s1e10NormalDist")

# ================= 10-12 PDCA =================
def f_pdca():
    im, d = new(); title(d, "工学シミュレーションのPDCAサイクル")
    cx, cy, r = 330, 225, 118
    quad = [(-45, 45, "P", "Plan:標準プロセス策定", ORANGE),
            (45, 135, "D", "Do:解析実施", BLUE),
            (135, 225, "C", "Check:満足度調査", GREEN),
            (225, 315, "A", "Act:プロセス改善", RED)]
    for a0, a1, letter, lab, col in quad:
        am = math.radians((a0+a1)/2)
        lx, ly = cx+r*math.cos(am), cy-r*math.sin(am)
        ctext(d, lx, ly, letter, FL, col)
        ox_, oy_ = cx+(r+62)*math.cos(am), cy-(r+62)*math.sin(am)
        ctext(d, ox_, oy_, lab, FT, col)
        # 円環矢印(時計回り P->D->C->A)
        d.arc((cx-r, cy-r, cx+r, cy+r), a0+6, a1-6, fill=col, width=5)
    # 進行方向矢印(時計回り)
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        tx, ty = cx+r*math.cos(a), cy-r*math.sin(a)
        arrow(d, tx, ty, tx+10*math.sin(a), ty+10*math.cos(a), BLACK, 2, 9)
    note(d, "P・D・C・Aの4段が過不足なく循環して初めて品質が向上")
    save(im, "s1e10PDCA")

# ================= 10-15 Workflow =================
def f_workflow():
    im, d = new(); title(d, "解析業務の標準実施手順(空欄(1)(2)(3))")
    steps = ["[(1)]契約内容の確認", "顧客要件の明確化", "実行計画書の作成",
             "[(2)]解析計画書の作成", "メッシュ・データ作成", "事前検証(予備計算)",
             "計算実行", "解析の検証", "[(3)]解析の妥当性確認",
             "報告書作成", "最終検査・納品"]
    col_x = [175, 485]; y0 = 70; dy = 56; w, h = 220, 40
    order = []
    for i in range(6):
        order.append((col_x[0], y0+i*dy, steps[i]))
    for i in range(5):
        order.append((col_x[1], y0+i*dy, steps[6+i]))
    for i, (x, y, s) in enumerate(order):
        hl = s.startswith("[")
        box(d, x, y, w, h, s, FT, fill=(255, 244, 210) if hl else "white",
            bcol=RED if hl else BLACK, tcol=RED if hl else BLACK)
    # 左列縦矢印
    for i in range(5):
        arrow(d, col_x[0], y0+i*dy+h/2, col_x[0], y0+(i+1)*dy-h/2, BLACK, 2, 9)
    # 左6→右1
    arrow(d, col_x[0]+w/2, y0+5*dy, col_x[1]-w/2, y0, BLACK, 2, 9)
    for i in range(4):
        arrow(d, col_x[1], y0+i*dy+h/2, col_x[1], y0+(i+1)*dy-h/2, BLACK, 2, 9)
    save(im, "s1e10Workflow")

# ================= 10-17 VandV =================
def f_vandv():
    im, d = new(); title(d, "検証(Verification)と妥当性確認(Validation)")
    box(d, 172, 230, 290, 300, "", fill=(240, 246, 255))
    box(d, 488, 230, 290, 300, "", fill=(240, 255, 244))
    ctext(d, 172, 108, "検証 Verification", FS, BLUE)
    ctext(d, 488, 108, "妥当性確認 Validation", FS, GREEN)
    left = ["論理的・数値的に", "正しく解けたか", "", "・入力データの整合", "・予備/本計算の", "  結果の確認", "・解の収束確認"]
    right = ["工学的用途に", "適合するか", "", "独立手法と比較:", "・手計算/理論解", "・妥当性確認済の", "  類似解析", "・実験/実機計測"]
    for i, s in enumerate(left):
        ctext(d, 172, 150+i*30, s, FT, BLACK)
    for i, s in enumerate(right):
        ctext(d, 488, 150+i*28, s, FT, BLACK)
    note(d, "『計算を正しく解いたか』(検証) vs 『正しい問題を解いたか』(妥当性確認)")
    save(im, "s1e10VandV")

# ================= 10-20 VerifyTiming =================
def f_verify_timing():
    im, d = new(); title(d, "購入解析ソフトの検証タイミング(4場面)")
    ox, oy = 70, 220; xlen = 520
    arrow(d, ox, oy, ox+xlen, oy, BLACK, 3, 13); ctext(d, ox+xlen+8, oy, "時間", FT, BLACK, "lm")
    labs = ["購入時", "ハード\nリニューアル", "OS\nバージョンアップ", "ソフト\nバージョンアップ"]
    xs = [ox+70, ox+200, ox+330, ox+460]
    for i, x in enumerate(xs):
        node(d, x, oy, 8, RED, RED)
        for j, ln in enumerate(labs[i].split("\n")):
            ctext(d, x, oy-64+j*18, ln, FT, BLACK)
        arrow(d, x, oy-38, x, oy-10, GRAY, 2, 8)
        ctext(d, x, oy+30, "再検証", FT, BLUE)
        ctext(d, x, oy+48, "・記録", FT, BLUE)
    note(d, "計算機環境(ハード・OS・ソフト)の変化がトリガー。結果は必ず記録")
    save(im, "s1e10VerifyTiming")


if __name__ == "__main__":
    f_verify_steps(); f_disk_collapse(); f_mesh_aspect(); f_punch_limit()
    f_cant_hinge(); f_plate_buckle(); f_creep_redist(); f_weld_couple()
    f_hardening(); f_normal_dist(); f_pdca(); f_workflow(); f_vandv(); f_verify_timing()
    print("=== s1e10 done: 14 figures ===")
