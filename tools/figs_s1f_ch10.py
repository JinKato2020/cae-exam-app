# -*- coding: utf-8 -*-
"""固体1級 第10章 解析の検証 —— 公式/用語図(接頭辞 s1f10)。白地660x420・黒線画。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

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


# ============ s1ch10-2 VerifyFlow ============
def f_verify_flow():
    im, d = new(); title(d, "非線形解析の標準的な検証手順(4段階)")
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
    note(d, "いきなり本番モデルを解かず、単純なものから段階的に確認")
    save(im, "s1f10VerifyFlow")

# ============ s1ch10-3 Disk ============
def f_disk():
    im, d = new(); title(d, "極限解析:外周固定円板の崩壊荷重")
    axl = 108; edge = 540; yt = 205; yb = 240
    for yy in range(150, 300, 12):
        d.line((axl, yy, axl, yy+6), fill=GRAY, width=1)
    ctext(d, axl, 138, "対称軸", FT, GRAY)
    d.rectangle((axl, yt, edge, yb), outline=BLACK, width=3, fill=FILL1)
    for x in range(140, 521, 48):
        arrow(d, x, 168, x, yt-2, BLUE, 3, 10)
    ctext(d, 330, 156, "一様圧力 p", FS, BLUE)
    wall(d, edge, 185, 260, side=1, n=8)
    ctext(d, edge+26, 275, "固定", FT, BLACK)
    d.rectangle((edge-34, yt, edge, yb), outline=RED, width=2, fill=(250, 220, 220))
    ctext(d, edge-70, 285, "塑性ヒンジ", FT, RED)
    dim(d, axl, 320, edge, 320, "半径 a", col=GRAY)
    dim(d, 88, yt, 88, yb, "t", col=GRAY)
    note(d, "M0=Sy t^2/4, pc=2.08*6M0/a^2(剛完全塑性・薄肉シェル+塑性ヒンジ)")
    save(im, "s1f10Disk")

# ============ s1ch10-4 Aspect ============
def f_aspect():
    im, d = new(); title(d, "要素のアスペクト比と解析精度")
    # 良い要素
    d.rectangle((110, 130, 250, 270), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 180, 200, "比≒1", F, GREEN)
    ctext(d, 180, 292, "良い(正方形に近い)", FT, GREEN)
    # 悪い要素
    d.rectangle((360, 175, 590, 225), outline=BLACK, width=3, fill=FILL3)
    ctext(d, 475, 200, "比 大", F, RED)
    ctext(d, 475, 250, "悪い(細長い)", FT, RED)
    note(d, "見かけの寸法を小さくしても、比が1から外れると精度は上がらない")
    save(im, "s1f10Aspect")

# ============ s1ch10-6 BeamHinge ============
def f_beam_hinge():
    im, d = new(); title(d, "骨組の極限解析:塑性ヒンジの積分点評価")
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
    arrow(d, x1, yb-70, x1, yb-14, RED, 4, 14); ctext(d, x1+8, yb-45, "P", F, RED, "lm")
    d.line((ips[0], yb-16, ips[0], yb+16), fill=RED, width=3)
    ctext(d, ips[0], yb+46, "塑性ヒンジ", FT, RED)
    dim(d, x0, yb+70, ips[0], yb+70, "L/10", col=GRAY)
    dim(d, ips[0], yb+95, x1, yb+95, "有効スパン Leff=9L/10", col=GRAY)
    note(d, "P_FEM=Mp/Leff → 理論値 Mp/L より大きめ(約1.11倍)")
    save(im, "s1f10BeamHinge")

# ============ s1ch10-7 Buckle ============
def f_buckle():
    im, d = new(); title(d, "薄板の座屈と対称条件によるモードの抜け")
    xL, xR = 120, 540; a = xR - xL
    def panel(cy, m, lab, col):
        d.rectangle((xL, cy-52, xR, cy+52), outline=BLACK, width=2, fill=(252, 252, 252))
        d.line((xL, cy, xR, cy), fill=LGRAY, width=1)
        pts = [(xL+a*i/200, cy-40*math.sin(m*math.pi*i/200)) for i in range(201)]
        d.line(pts, fill=col, width=3, joint="curve")
        xc = (xL+xR)/2
        for yy in range(cy-52, cy+52, 10):
            d.line((xc, yy, xc, yy+5), fill=GRAY, width=1)
        ctext(d, xL-8, cy, lab, FT, col, "rm")
    panel(140, 2, "m=2", BLUE)
    ctext(d, 330, 205, "m=2:反対称・理論の最小(k2=4.0)", FT, BLUE)
    panel(300, 3, "m=3", RED)
    ctext(d, 330, 366, "対称条件でm=2が抜け→m=3(k3≒4.69)で座屈", FT, RED)
    ctext(d, 330+8, 88, "x=a/2 対称線", FT, GRAY, "lm")
    save(im, "s1f10Buckle")

# ============ s1ch10-8 Creep ============
def f_creep():
    im, d = new(); title(d, "定常クリープ(ノルトン則)と応力の再分布")
    ox, oy = 80, 320; xlen, ylen = 330, 220
    axes(d, ox, oy, xlen, ylen, "log(時間)", "相当応力")
    x0, x1 = ox+10, ox+xlen-10
    asy_in, asy_out = oy-115, oy-150
    def approach(start, asym):
        return [(x0+(x1-x0)*i/100, asym+(start-asym)*math.exp(-3.0*i/100)) for i in range(101)]
    d.line(approach(oy-200, asy_in), fill=RED, width=3, joint="curve")
    d.line(approach(oy-45, asy_out), fill=BLUE, width=3, joint="curve")
    d.line((x0, asy_in, x1, asy_in), fill=LGRAY, width=1)
    d.line((x0, asy_out, x1, asy_out), fill=LGRAY, width=1)
    ctext(d, x1-30, oy-212, "内面(低下)", FT, RED)
    ctext(d, x1-30, oy-31, "外面(上昇)", FT, BLUE)
    ctext(d, x1+6, asy_out, "定常値へ漸近", FT, GRAY, "lm")
    cx, cy = 545, 130
    d.ellipse((cx-58, cy-58, cx+58, cy+58), outline=BLACK, width=3)
    d.ellipse((cx-28, cy-28, cx+28, cy+28), outline=BLACK, width=3, fill="white")
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        arrow(d, cx+28*math.cos(a), cy+28*math.sin(a), cx+45*math.cos(a), cy+45*math.sin(a), BLUE, 2, 7)
    ctext(d, cx, cy, "p", FS, BLUE)
    ctext(d, cx, cy+72, "内圧p・厚肉円筒", FT, BLACK)
    save(im, "s1f10Creep")

# ============ s1ch10-9 Weld ============
def f_weld():
    im, d = new(); title(d, "溶接残留応力の熱弾塑性解析(断面)")
    # 母材2枚(突合せ)
    d.rectangle((70, 210, 320, 330), outline=BLACK, width=3, fill=FILL1)
    d.rectangle((340, 210, 590, 330), outline=BLACK, width=3, fill=FILL1)
    ctext(d, 150, 300, "母材", FS, BLACK); ctext(d, 510, 300, "母材", FS, BLACK)
    # 溶接ビード(上部の盛り)
    d.polygon([(300, 210), (360, 210), (350, 160), (310, 160)], outline=BLACK, width=3, fill=FILL3)
    d.arc((300, 150, 360, 200), 200, 340, fill=BLACK, width=3)
    # 溶融池/溶接金属
    d.ellipse((305, 205, 355, 285), outline=RED, width=3, fill=(250, 225, 225))
    ctext(d, 330, 245, "溶接金属", FT, RED)
    # HAZ
    d.ellipse((285, 195, 375, 300), outline=ORANGE, width=2)
    ctext(d, 415, 180, "HAZ(熱影響部)", FT, ORANGE)
    arrow(d, 405, 188, 368, 220, ORANGE, 2, 8)
    # 入熱
    arrow(d, 330, 120, 330, 150, RED, 4, 12); ctext(d, 330, 108, "集中入熱(急加熱・急冷)", FT, RED)
    note(d, "非定常熱伝導→各時刻の温度場→熱弾塑性解析(温度場は独立=一方向)")
    save(im, "s1f10Weld")

# ============ s1ch10-10 Hardening ============
def f_hardening():
    im, d = new(); title(d, "硬化則:等方・移動・複合とバウシンガー効果")
    sx, sy = 17, 36; hw, hh = 82, 92; cy = 205
    def panel(cx, ttl, loops, notes, marks):
        cross_axes(d, cx, cy, hw, hh, "e", "s")
        ctext(d, cx, cy-hh-24, ttl, FS, BLACK)
        for pts, col, wd in loops:
            poly_data(d, cx, cy, sx, sy, pts, col, wd)
        for (mx, my, col) in marks:
            node(d, cx+mx*sx, cy-my*sy, 4, col, col)
        for j, (t, col) in enumerate(notes):
            ctext(d, cx, cy+hh+18+j*17, t, FT, col)
    iso = [(0, 0), (1, 1), (4, 1.45), (1.1, -1.45), (-3, -2.06), (1.12, 2.06)]
    panel(115, "等方硬化",
          [([(0, 0), (1, 1), (4, 1.45)], GRAY, 2), (iso[2:], BLUE, 3)],
          [("降伏曲面が一様膨張", BLUE), ("再降伏対称・拡大", GRAY)],
          [(1.1, -1.45, RED)])
    kin_v = [(0, 0), (1, 1), (4, 1.4)]
    kin = [(4, 1.4), (2, -0.6), (-4, -1.4), (-2, 0.6), (4, 1.4)]
    panel(330, "移動硬化",
          [(kin_v, GRAY, 2), (kin, BLUE, 3)],
          [("平行移動・弾性域2σy", BLUE), ("安定な閉ループ", GREEN)],
          [(2, -0.6, RED)])
    ctext(d, 330+2*sx+8, cy+0.6*sy, "早期再降伏", FT, RED, "lm")
    comb = [(0, 0), (4, 1.4), (1.6, -1.0), (-4, -1.55), (-1.6, 0.85), (4, 1.55)]
    panel(545, "複合硬化",
          [(comb, BLUE, 3)],
          [("両者の中間", BLUE), ("ラチェットに最適", GREEN)],
          [(1.6, -1.0, RED)])
    save(im, "s1f10Hardening")

# ============ s1ch10-12 Normal ============
def f_normal():
    im, d = new(); title(d, "ばらつき:標準偏差σ と 平均値の標準偏差 σ/√n")
    ox, oy = 90, 330; xlen = 480
    d.line((ox, oy, ox+xlen, oy), fill=BLACK, width=2)
    mu = ox + xlen/2
    for yy in range(oy, 95, -10):
        d.line((mu, yy, mu, yy-5), fill=GRAY, width=1)
    ctext(d, mu, oy+18, "μ(平均)", FT, BLACK)
    def bell(sig_px, amp, col, wd):
        pts = [(x, oy-amp*math.exp(-0.5*((x-mu)/sig_px)**2)) for x in range(ox+5, ox+xlen-4, 3)]
        d.line(pts, fill=col, width=wd, joint="curve")
    bell(120, 150, BLUE, 3)
    bell(54, 210, RED, 3)
    ctext(d, mu+150, oy-70, "測定値のばらつき σ", FT, BLUE)
    ctext(d, mu+120, oy-190, "平均値のばらつき σ/√n", FT, RED)
    dim(d, mu, oy-40, mu+120, oy-40, "σ", col=BLUE)
    dim(d, mu, oy-150, mu+54, oy-150, "σ/√n", col=RED)
    note(d, "sx=√(Σ(Si-S̄)^2/(n-1))(不偏・n-1で割る), 標準誤差=sx/√n")
    save(im, "s1f10Normal")

# ============ s1ch10-14 PDCA ============
def f_pdca():
    im, d = new(); title(d, "PDCAサイクル(ISO9001)")
    cx, cy, r = 330, 225, 118
    quad = [(-45, 45, "P", "Plan:計画・標準化", ORANGE),
            (45, 135, "D", "Do:実行", BLUE),
            (135, 225, "C", "Check:評価・監視", GREEN),
            (225, 315, "A", "Act:改善処置", RED)]
    for a0, a1, letter, lab, col in quad:
        am = math.radians((a0+a1)/2)
        ctext(d, cx+r*math.cos(am), cy-r*math.sin(am), letter, FL, col)
        ctext(d, cx+(r+62)*math.cos(am), cy-(r+62)*math.sin(am), lab, FT, col)
        d.arc((cx-r, cy-r, cx+r, cy+r), a0+6, a1-6, fill=col, width=5)
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        tx, ty = cx+r*math.cos(a), cy-r*math.sin(a)
        arrow(d, tx, ty, tx+10*math.sin(a), ty+10*math.cos(a), BLACK, 2, 9)
    note(d, "どれか1段でも欠けるとPDCAにならない(計画→実行→評価→改善)")
    save(im, "s1f10PDCA")

# ============ s1ch10-16 Workflow ============
def f_workflow():
    im, d = new(); title(d, "解析業務の標準的な実施手順")
    steps = ["契約内容の確認", "顧客要件の明確化", "実行計画書の作成",
             "解析計画書の作成", "メッシュ・データ作成", "事前検証(予備計算)",
             "計算実行", "解析の検証", "解析の妥当性確認",
             "報告書作成", "最終検査・納品"]
    col_x = [175, 485]; y0 = 70; dy = 56; w, h = 220, 40
    order = [(col_x[0], y0+i*dy, steps[i]) for i in range(6)]
    order += [(col_x[1], y0+i*dy, steps[6+i]) for i in range(5)]
    ver = {"解析の検証", "解析の妥当性確認"}
    for x, y, s in order:
        hl = s in ver
        box(d, x, y, w, h, s, FT, fill=(240, 255, 244) if hl else "white",
            bcol=GREEN if hl else BLACK, tcol=GREEN if hl else BLACK)
    for i in range(5):
        arrow(d, col_x[0], y0+i*dy+h/2, col_x[0], y0+(i+1)*dy-h/2, BLACK, 2, 9)
    arrow(d, col_x[0]+w/2, y0+5*dy, col_x[1]-w/2, y0, BLACK, 2, 9)
    for i in range(4):
        arrow(d, col_x[1], y0+i*dy+h/2, col_x[1], y0+(i+1)*dy-h/2, BLACK, 2, 9)
    note(d, "検証(Verification)の後に妥当性確認(Validation)の順序が重要")
    save(im, "s1f10Workflow")


if __name__ == "__main__":
    f_verify_flow(); f_disk(); f_aspect(); f_beam_hinge(); f_buckle()
    f_creep(); f_weld(); f_hardening(); f_normal(); f_pdca(); f_workflow()
    print("=== s1f10 done: 11 figures ===")
