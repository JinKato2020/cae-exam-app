# -*- coding: utf-8 -*-
"""固体2級 5-24/5-26/5-27/8-14/8-16 の図を提供参考図を基に作り直す(アプリ最適化)。
白地660x420・figlib共通スタイル・3D(等角)表現・文字=figlib標準・余白圧縮。
★回答前と回答後で同じ「ベース図」を使い、回答後はベースに答えを描き加える(前後で図を変えない)。
 回答前(〜Setup)=ベース+問い / 回答後=ベース+答え。
このファイルが下記10キーの単一ソース(旧 figs_s2_5_26.py 等の該当キー定義を上書き):
 femThickSolid(Setup) f5ShrinkFit(Setup) f5Bimetal(Setup) model8ChannelBeam(Setup) model8Interface(Setup)
5-27は従来 preFigureImage 無し→ f5BimetalSetup を新設(JSON配線も追加)。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

A_F = (250, 236, 212); A_T = (246, 227, 197); A_R = (236, 214, 180)
B_F = (222, 233, 248); B_T = (209, 223, 244); B_R = (195, 212, 238)


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1)
    if L == 0:
        return
    n = max(1, int(L / seg)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg, x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


def iso_block(d, ox, oy, w, h, dp, front, top, right, out=BLACK, wd=3):
    dx = int(dp * 0.7); dy = int(dp * 0.42)
    d.polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)], outline=out, width=wd, fill=front)
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + w + dx, oy - dy), (ox + w, oy)], outline=out, width=wd, fill=top)
    d.polygon([(ox + w, oy), (ox + w + dx, oy - dy), (ox + w + dx, oy + h - dy), (ox + w, oy + h)], outline=out, width=wd, fill=right)
    return dx, dy


def torque_arc(d, cx, cy, rx, ry, col=BLUE):
    d.arc((cx - rx, cy - ry, cx + rx, cy + ry), -70, 70, fill=col, width=4)
    arrow(d, cx + rx * 0.34, cy - ry + 4, cx + rx * 0.42, cy - ry + 24, col, 4, 11)


def c_section(d, x, y, w, h, t, col=BLACK, fill=FILL1):
    pts = [(x, y), (x + w, y), (x + w, y + t), (x + t, y + t),
           (x + t, y + h - t), (x + w, y + h - t), (x + w, y + h), (x, y + h)]
    d.polygon(pts, outline=col, width=3, fill=fill)


def _bilayer(d, ox, oy, w, ha, hb, dp):
    dx = int(dp * 0.7); dy = int(dp * 0.42)
    iso_block(d, ox, oy + ha, w, hb, dp, B_F, B_T, B_R)
    iso_block(d, ox, oy, w, ha, dp, A_F, A_T, A_R)
    return dx, dy


def _hexagon(d, hx, hy, R):
    V = []
    for k in range(6):
        a = math.radians(k * 60)
        V.append((hx + R * math.cos(a), hy - R * math.sin(a)))
    order = {2: "1", 1: "2", 0: "3", 3: "4", 4: "5", 5: "6"}
    for i in range(6):
        p1 = V[i]; p2 = V[(i + 1) % 6]
        fill = (A_F if i in (0, 1, 2) else B_F)
        d.polygon([(hx, hy), p1, p2], outline=BLACK, width=2, fill=fill)
        c = ((hx + p1[0] + p2[0]) / 3, (hy + p1[1] + p2[1]) / 3)
        ctext(d, c[0], c[1], order[i], FT, BLACK)
    d.line((V[3][0], V[3][1], V[0][0], V[0][1]), fill=GREEN, width=3)
    node(d, hx, hy, 5, (30, 50, 70))


# ============ 5-24 厚みのあるブロック(ソリッド要素選択) ============
def _base_thick(d):
    title(d, "厚み・幅・奥行きが同程度のブロック")
    ox, oy, w, h, dp = 250, 150, 190, 135, 140
    dx, dy = iso_block(d, ox, oy, w, h, dp, FILL1, FILL2, FILL3)
    arrow(d, ox - 22, oy, ox - 22, oy + h, GREEN, 3, 11); arrow(d, ox - 22, oy + h, ox - 22, oy, GREEN, 3, 11)
    ctext(d, ox - 34, oy + h / 2, "厚み", FS, GREEN, "rm")
    arrow(d, ox, oy + h + 22, ox + w, oy + h + 22, BLUE, 3, 11); arrow(d, ox + w, oy + h + 22, ox, oy + h + 22, BLUE, 3, 11)
    ctext(d, ox + w / 2, oy + h + 38, "幅", FS, BLUE)
    arrow(d, ox + w + 14, oy + h + 6, ox + w + dx + 14, oy + h - dy + 6, RED, 3, 11)
    ctext(d, ox + w + dx + 24, oy + h - dy + 2, "奥行き", FS, RED, "lm")
    return ox, oy, w, h, dp, dx, dy


def f_thick_solid_setup():
    im, d = new(); _base_thick(d)
    note(d, "3方向とも同程度の塊。応力解析に最適な要素は?(答えは未記入)")
    save(im, "femThickSolidSetup")


def f_thick_solid_after():
    im, d = new()
    ox, oy, w, h, dp, dx, dy = _base_thick(d)
    for i in (1, 2):
        d.line((ox + w * i / 3, oy, ox + w * i / 3, oy + h), fill=GRAY, width=1)
        d.line((ox, oy + h * i / 3, ox + w, oy + h * i / 3), fill=GRAY, width=1)
        d.line((ox + w * i / 3, oy, ox + w * i / 3 + dx, oy - dy), fill=GRAY, width=1)
        d.line((ox + w, oy + h * i / 3, ox + w + dx, oy + h * i / 3 - dy), fill=GRAY, width=1)
    ctext(d, 330, 364, "六面体・四面体などのソリッド要素でメッシュ", FS, BLACK)
    note(d, "薄板→シェル / 細長い→はり・トラス / 塊→ソリッド")
    save(im, "femThickSolid")


# ============ 5-26 焼きばめ(初期ひずみ) ============
def _base_shrink(d):
    title(d, "焼きばめ:穴に少し大きい丸軸を圧入")
    d.rectangle((70, 100, 290, 270), outline=BLACK, width=3, fill=B_F)
    d.ellipse((120, 125, 240, 245), outline=BLACK, width=3, fill="white")
    arrow(d, 126, 185, 234, 185, BLUE, 3, 10); arrow(d, 234, 185, 126, 185, BLUE, 3, 10); ctext(d, 180, 165, "D", FS, BLUE)
    ctext(d, 180, 90, "穴の断面", FT, GRAY); ctext(d, 180, 285, "穴径 D=200mm", FT, BLUE)
    d.ellipse((430, 120, 600, 290), outline=BLACK, width=3, fill=(224, 244, 232))
    arrow(d, 440, 205, 590, 205, GREEN, 3, 10); arrow(d, 590, 205, 440, 205, GREEN, 3, 10); ctext(d, 515, 182, "D+δ", FS, GREEN)
    ctext(d, 515, 90, "挿入前の丸軸", FT, GRAY); ctext(d, 515, 300, "丸軸径 D+δ", FT, GREEN)
    arrow(d, 410, 195, 320, 195, BLACK, 3, 12); ctext(d, 365, 178, "圧入", FT, GRAY)
    ctext(d, 330, 332, "しめしろ(直径差) δ=0.10mm / {σ}=[E]({ε}−{ε^I})", FT, GRAY)
    return (180, 185, 60), (515, 205, 85)


def f_shrink_fit_setup():
    im, d = new(); _base_shrink(d)
    note(d, "丸軸へ各方向に与える初期ひずみ ε^I は?(答えは未記入)")
    save(im, "f5ShrinkFitSetup")


def f_shrink_fit_after():
    im, d = new()
    (hcx, hcy, hr), (scx, scy, sr) = _base_shrink(d)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        arrow(d, scx + (sr - 2) * math.cos(rad), scy - (sr - 2) * math.sin(rad), scx + (sr + 16) * math.cos(rad), scy - (sr + 16) * math.sin(rad), GREEN, 2, 8)
        arrow(d, hcx + (hr + 16) * math.cos(rad), hcy - (hr + 16) * math.sin(rad), hcx + (hr - 2) * math.cos(rad), hcy - (hr - 2) * math.sin(rad), BLUE, 2, 8)
    ctext(d, 330, 358, "丸軸:+δ/D=+0.10/200=+5×10⁻⁴(膨張) / 厚板:−δ/D(収縮)", FS, BLACK)
    note(d, "軸は大きくなろうとする=正。ひずみは径Dで割って無次元化")
    save(im, "f5ShrinkFit")


# ============ 5-27 バイメタル(異材貼合せ+加熱) ============
def _base_bimetal(d):
    title(d, "線膨張係数の違う2枚を全面接着→加熱")
    ox, oy, w, ha, hb, dp = 190, 170, 260, 44, 44, 120
    dx, dy = _bilayer(d, ox, oy, w, ha, hb, dp)
    ctext(d, ox + w / 2, oy + 22, "材料A:線膨張係数 αA", FT, (150, 90, 20))
    ctext(d, ox + w / 2, oy + ha + 22, "材料B:線膨張係数 αB", FT, (40, 90, 170))
    for fx in (ox + 40, ox + 110, ox + 180, ox + 240):
        arrow(d, fx, oy - dy - 46, fx, oy - dy - 12, RED, 3, 11)
    ctext(d, ox + w / 2, oy - dy - 62, "加熱:温度上昇 ΔT", FS, RED)
    d.line((ox + w + dx, oy + ha, ox + w + dx + 40, oy + ha + 46), fill=GREEN, width=2)
    ctext(d, ox + w + dx + 44, oy + ha + 52, "全面接着", FT, GREEN, "lm")
    ctext(d, 330, 318, "αA ≠ αB", FS, BLACK)
    return ox, oy, w, ha, hb, dp, dx, dy


def f_bimetal_setup():
    im, d = new(); _base_bimetal(d)
    note(d, "加熱すると応力と形状はどうなる?(答えは未記入)")
    save(im, "f5BimetalSetup")


def f_bimetal_after():
    im, d = new()
    ox, oy, w, ha, hb, dp, dx, dy = _base_bimetal(d)
    ctext(d, 330, 344, "界面に残留応力 → 全体がそる(反る)", FS, BLACK)
    d.arc((ox + 50, 352, ox + w - 50, 432), 202, 338, fill=RED, width=3)
    arrow(d, ox + 50 + 6, 372, ox + 44, 360, RED, 3, 10)
    note(d, "伸びたい量の差が拘束され、残留応力とそり(バイメタル)が同時に生じる")
    save(im, "f5Bimetal")


# ============ 8-14 開断面(溝形)はりの曲げ+ねじり ============
def _base_channel(d):
    title(d, "厚肉の溝形(開断面)はり:曲げ+ねじり")
    ox, oy, w, h, dp = 180, 175, 250, 96, 100
    dx, dy = iso_block(d, ox, oy, w, h, dp, FILL1, FILL2, FILL3)
    arrow(d, ox + 46, oy - dy - 34, ox + 46, oy - dy - 4, RED, 4, 12); ctext(d, ox + 46, oy - dy - 48, "曲げ", FT, RED)
    tx, ty = ox + w * 0.52, oy - dy * 0.5
    d.polygon([(tx - 24, ty - 4), (tx + 20, ty - 4), (tx + 30, ty + 10), (tx - 14, ty + 10)], outline=GREEN, width=2, fill=(224, 244, 232))
    ctext(d, tx + 4, oy - dy - 16, "上面の確認位置", FT, GREEN)
    arrow(d, tx + 74, ty + 3, tx + 28, ty + 3, GREEN, 3, 10); ctext(d, tx + 82, ty + 3, "軸方向", FT, GREEN, "lm")
    torque_arc(d, ox + w + dx + 30, oy + h / 2 - dy / 2, 22, h * 0.5, BLUE); ctext(d, ox + w + dx + 58, oy + h / 2 - dy / 2, "ねじりT", FT, BLUE, "lm")
    c_section(d, 58, 250, 58, 72, 16)
    d.line((58 + 58, 250 + 36, ox - 4, oy + h - 10), fill=GRAY, width=1)
    ctext(d, 58 + 29, 250 + 88, "厚肉の溝形断面(開断面)", FT, GRAY)
    return ox, oy, w, h, dp, dx, dy


def f_channel_beam_setup():
    im, d = new(); _base_channel(d)
    note(d, "開断面は反りを伴う。局所ひずみ評価に最適な要素は?(答えは未記入)")
    save(im, "model8ChannelBeamSetup")


def f_channel_beam_after():
    im, d = new()
    ox, oy, w, h, dp, dx, dy = _base_channel(d)
    ctext(d, ox + w * 0.5, oy + h + 24, "ねじり→断面が反る(ワーピング)", FT, RED)
    ctext(d, 420, 322, "はり理論では表せない", FT, GRAY)
    ctext(d, 420, 348, "→ 三次元ソリッド要素", FS, BLACK)
    note(d, "反りを含む局所ひずみ評価にはソリッド要素が必要(平面化も不可)")
    save(im, "model8ChannelBeam")


# ============ 8-16 異材界面の応力出力 ============
def _base_interface(d):
    title(d, "異材界面の応力出力(四面体要素)")
    lx, ly, lw, aH, bH = 70, 108, 180, 80, 80
    d.rectangle((lx, ly, lx + lw, ly + aH), outline=BLACK, width=3, fill=A_F)
    d.rectangle((lx, ly + aH, lx + lw, ly + aH + bH), outline=BLACK, width=3, fill=B_F)
    d.line((lx, ly + aH, lx + lw, ly + aH), fill=GREEN, width=3)
    node(d, lx + lw / 2, ly + aH, 5, "white")
    for fx in (lx + 28, lx + 66, lx + 114, lx + 152):
        arrow(d, fx, ly - 32, fx, ly - 4, RED, 3, 10)
    ctext(d, lx + lw / 2, ly - 46, "上面:一様分布荷重", FT, RED)
    ctext(d, lx + lw / 2, ly + aH / 2, "材料A(高剛性)", FT, (150, 90, 20))
    ctext(d, lx + lw / 2, ly + aH + bH / 2, "材料B(低剛性)", FT, (40, 90, 170))
    yb = ly + aH + bH
    for i in range(10):
        d.line((lx + i * lw / 10, yb, lx + i * lw / 10 - 9, yb + 13), fill=BLACK, width=2)
    d.line((lx, yb, lx + lw, yb), fill=BLACK, width=3)
    ctext(d, lx + lw / 2, yb + 22, "下面固定", FT, GRAY)
    arrow(d, lx - 24, yb, lx - 24, ly + aH - 14, BLACK, 2, 9); ctext(d, lx - 24, ly + aH - 26, "z", FT, BLACK)
    _hexagon(d, 500, 176, 88)
    ctext(d, 500, 72, "界面節点まわりの6要素", FT, GRAY)
    ctext(d, 330, 358, "σz[MPa]  1〜3:−1.41/−1.47/−1.42   4〜6:−0.564/−0.598/−0.592", FT, GRAY)


def f_interface_setup():
    im, d = new(); _base_interface(d)
    note(d, "界面の応力評価で『誤っている』記述は?(答えは未記入)")
    save(im, "model8InterfaceSetup")


def f_interface_after():
    im, d = new()
    _base_interface(d)
    ctext(d, 500, 284, "A側平均≈−1.43 / B側≈−0.59", FT, BLACK)
    ctext(d, 500, 306, "→ 界面で不連続", FT, GREEN)
    ctext(d, 500, 330, "✗ 主応力の大小だけはNG", FT, RED)
    note(d, "界面は応力不連続。局所座標系で評価。主応力の大小だけで論じるのは誤り(=④)")
    save(im, "model8Interface")


def main():
    f_thick_solid_setup(); f_thick_solid_after()
    f_shrink_fit_setup(); f_shrink_fit_after()
    f_bimetal_setup(); f_bimetal_after()
    f_channel_beam_setup(); f_channel_beam_after()
    f_interface_setup(); f_interface_after()
    print("done ch5/8: 10 figures (前後で同一ベース図+答え)")


if __name__ == "__main__":
    main()
