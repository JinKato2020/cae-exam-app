# -*- coding: utf-8 -*-
"""固体2級 第8章(モデリングの基礎)の「回答前(preFigureImage)」配置図 14枚。
白地660x420・黒線画・構造形状と与えられた荷重/条件のみ。
答え(どの要素種類/対称モデル/モデル化方針を選ぶか・結論)は一切描かない(=required相当)。
既存 figureImage(結論キャプション付き=答え示唆)は回答後(helpful)のまま。JSON配線は別途。
[[cae-figure-before-after-rule]] の第8章横展開。"""
import sys, math
sys.path.insert(0, r"c:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


def hcyl(d, cx, cy, L, r):
    """横置き円筒(側面): 左右に半楕円の鏡。"""
    d.line((cx - L / 2, cy - r, cx + L / 2, cy - r), fill=BLACK, width=3)
    d.line((cx - L / 2, cy + r, cx + L / 2, cy + r), fill=BLACK, width=3)
    d.arc((cx - L / 2 - 18, cy - r, cx - L / 2 + 18, cy + r), 90, 270, fill=BLACK, width=3)
    d.arc((cx + L / 2 - 18, cy - r, cx + L / 2 + 18, cy + r), 270, 450, fill=BLACK, width=3)


# ---- 8-2 横置き容器・長手方向地震 ----
def f_saddle_axial():
    im, d = new(); title(d, "サドル支持の横置き円筒容器(長手方向の地震)")
    cx, cy = 320, 200; hcyl(d, cx, cy, 300, 70)
    for sx in (cx - 90, cx + 90):
        d.polygon((sx - 28, cy + 110, sx + 28, cy + 110, sx + 14, cy + 70, sx - 14, cy + 70), outline=BLACK, width=3, fill=FILL1)
        hwall(d, sx - 30, sx + 30, cy + 110, 1, 5)
    ctext(d, cx - 90, cy + 128, "固定", FT, GRAY); ctext(d, cx + 90, cy + 128, "スライド", FT, GRAY)
    arrow(d, cx - 40, cy, cx - 150, cy, RED, 3, 12); arrow(d, cx + 40, cy, cx + 150, cy, RED, 3, 12)
    ctext(d, cx, cy - 18, "長手(軸)方向 地震", FS, RED)
    dash(d, cx - 170, cy, cx + 175, cy, GRAY, 2); ctext(d, cx + 185, cy, "軸", FT, GRAY, "lm")
    note(d, "長手方向の地震。解析領域を最小にする対称モデルはどれか?")
    save(im, "model8SaddleAxialSetup")


def dash(d, x1, y1, x2, y2, col=GRAY, wd=2, seg=10):
    L = math.hypot(x2 - x1, y2 - y1); n = max(1, int(L / seg)); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        if i % 2 == 0:
            d.line((x1 + ux * i * seg, y1 + uy * i * seg, x1 + ux * (i + 1) * seg, y1 + uy * (i + 1) * seg), fill=col, width=wd)


# ---- 8-3 横置き容器・長手直交水平地震(上面図) ----
def f_saddle_transverse():
    im, d = new(); title(d, "横置き円筒容器・長手に直交する水平地震(上面図)")
    cx, cy = 320, 210; hcyl(d, cx, cy, 300, 60)
    for sx in (cx - 90, cx + 90):
        d.line((sx - 26, cy + 60, sx + 26, cy + 60), fill=BLACK, width=3)
    ctext(d, cx - 90, cy + 78, "固定", FT, GRAY); ctext(d, cx + 90, cy + 78, "スライド", FT, GRAY)
    arrow(d, cx, cy - 95, cx, cy - 64, RED, 3, 12); ctext(d, cx, cy - 112, "長手直交・水平地震", FS, RED)
    dash(d, cx - 170, cy, cx + 175, cy, GRAY, 2); ctext(d, cx + 185, cy, "長手", FT, GRAY, "lm")
    note(d, "長手に直交する水平地震。解析領域を最小にするモデルはどれか?")
    save(im, "model8SaddleTransverseSetup")


# ---- 8-4 連続アーチ高架橋・脚沈下 ----
def f_arch_bridge():
    im, d = new(); title(d, "連続アーチ高架橋・中央脚oの沈下")
    y0 = 300; xs = [80, 160, 240, 320, 400, 480, 560]; labs = ["a", "b", "c", "o", "c", "b", "a"]
    hwall(d, 60, 580, y0, 1, 20)
    for x in xs:
        d.line((x, y0, x, y0 - 70), fill=BLACK, width=3)
    for i in range(len(xs) - 1):
        x1, x2 = xs[i], xs[i + 1]
        d.arc((x1, y0 - 70 - (x2 - x1), x2, y0 - 70 + (x2 - x1)), 180, 360, fill=BLACK, width=3)
    for x, l in zip(xs, labs):
        ctext(d, x, y0 + 18, l, FT, BLACK)
    arrow(d, 320, y0 + 6, 320, y0 + 44, RED, 3, 12); ctext(d, 320, y0 - 92, "中央脚 o", FT, RED); ctext(d, 352, y0 + 30, "沈下", FT, RED, "lm")
    note(d, "中央脚oが沈下。平面ひずみで効率よく解く解析領域はどれか?")
    save(im, "model8ArchBridgeSetup")


# ---- 8-5 高圧容器ノズル交差部 ----
def f_nozzle():
    im, d = new(); title(d, "円筒胴と板厚の異なるノズルの交差部")
    sx, sy, sw, sh = 200, 110, 70, 250
    d.rectangle((sx, sy, sx + sw, sy + sh), outline=BLACK, width=3, fill=FILL1)
    ctext(d, sx + sw / 2, sy + sh + 16, "円筒胴", FT, GRAY)
    ny = sy + 120
    d.rectangle((sx + sw, ny, sx + sw + 150, ny + 48), outline=BLACK, width=3, fill=FILL1)
    ctext(d, sx + sw + 75, ny + 70, "ノズル(板厚違い)", FT, GRAY)
    arrow(d, sx + sw + 200, ny + 24, sx + sw + 152, ny + 24, BLUE, 3, 12); ctext(d, sx + sw + 205, ny + 24, "低温流体 注入", FT, BLUE, "lm")
    d.ellipse((sx + sw - 14, ny + 14, sx + sw + 18, ny + 40), outline=RED, width=2)
    note(d, "交差部のピーク熱応力を詳細に求める。最適なモデルはどれか?")
    save(im, "model8NozzleThermalSetup")


# ---- 8-6 スカート支持容器 ----
def f_skirt():
    im, d = new(); title(d, "スカートで支持された高圧容器(高温運転)")
    cx = 300; top, bot, r = 90, 300, 70
    d.line((cx - r, top + 10, cx - r, bot), fill=BLACK, width=3); d.line((cx + r, top + 10, cx + r, bot), fill=BLACK, width=3)
    d.arc((cx - r, top - 30, cx + r, top + 50), 180, 360, fill=BLACK, width=3)
    d.line((cx - r, bot, cx - r - 20, bot + 70), fill=BLACK, width=3); d.line((cx + r, bot, cx + r + 20, bot + 70), fill=BLACK, width=3)
    hwall(d, cx - r - 24, cx + r + 24, bot + 70, 1, 8)
    ctext(d, cx, bot + 40, "スカート", FT, GRAY)
    for yy in (top + 70, top + 130, top + 190):
        arrow(d, cx - r - 40, yy, cx - r - 8, yy, RED, 2, 9)
    ctext(d, cx - r - 70, top + 130, "内圧", FT, RED, "rm")
    d.ellipse((cx + r - 12, bot - 12, cx + r + 12, bot + 12), outline=RED, width=2); ctext(d, cx + r + 40, bot, "取付け部", FT, GRAY, "lm")
    note(d, "取付け部の繰返し熱応力(応力集中含む)を効率よく。最適モデルは?")
    save(im, "model8SkirtVesselSetup")


# ---- 8-7 地下LNGタンク ----
def f_lng():
    im, d = new(); title(d, "地下式 円筒LNGタンク(本体壁・止水壁・ドーム屋根)")
    cx = 320; top, bot, r = 150, 330, 120
    hwall(d, 120, 520, top - 10, 1, 16); ctext(d, 150, top - 28, "地面(地下)", FT, GRAY, "lm")
    d.arc((cx - r, top - 60, cx + r, top + 60), 180, 360, fill=BLACK, width=3); ctext(d, cx, top - 34, "ドーム屋根", FT, GRAY)
    for xx in (cx - r, cx + r):
        d.line((xx, top, xx, bot), fill=BLACK, width=3)
    d.line((cx - r - 24, top + 10, cx - r - 24, bot), fill=BLACK, width=2); ctext(d, cx - r - 55, (top + bot) / 2, "止水壁", FT, GRAY, "rm")
    d.line((cx - r, bot, cx + r, bot), fill=BLACK, width=3); ctext(d, cx + r + 10, (top + bot) / 2, "本体壁", FT, GRAY, "lm")
    note(d, "定常温度分布と内外圧による応力を効率よく。最適モデルは?")
    save(im, "model8LNGTankSetup")


# ---- 8-8 ダンベル形丸棒試験片 ----
def f_dumbbell():
    im, d = new(); title(d, "円形断面のダンベル形 丸棒引張試験片")
    cx, cy = 320, 210
    pts_top = [(150, cy - 55), (235, cy - 55), (285, cy - 22), (355, cy - 22), (405, cy - 55), (490, cy - 55)]
    pts_bot = [(x, 2 * cy - y) for (x, y) in pts_top]
    d.line(pts_top, fill=BLACK, width=3, joint="curve"); d.line(pts_bot, fill=BLACK, width=3, joint="curve")
    d.line((150, cy - 55, 150, cy + 55), fill=BLACK, width=3); d.line((490, cy - 55, 490, cy + 55), fill=BLACK, width=3)
    arrow(d, 150, cy, 70, cy, RED, 4, 14); arrow(d, 490, cy, 570, cy, RED, 4, 14)
    ctext(d, 60, cy, "P", FS, RED, "rm"); ctext(d, 580, cy, "P", FS, RED, "lm")
    ctext(d, cx, cy + 80, "平行部(ゲージ部)", FT, GRAY)
    note(d, "軸方向に引張る弾性解析を最も効率よく行える要素は?")
    save(im, "model8DumbbellSetup")


# ---- 8-9 有孔薄板の面内引張 ----
def f_plate_hole():
    im, d = new(); title(d, "円孔をもつ薄板の面内一様引張")
    ox, oy, w, h = 210, 150, 240, 130
    d.rectangle((ox, oy, ox + w, oy + h), outline=BLACK, width=3, fill=FILL1)
    cx, cy = ox + w / 2, oy + h / 2
    d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), outline=BLACK, width=3, fill="white"); ctext(d, cx, cy, "円孔", FT, GRAY)
    for yy in (oy + 35, oy + h - 35):
        arrow(d, ox - 8, yy, ox - 56, yy, RED, 3, 11); arrow(d, ox + w + 8, yy, ox + w + 56, yy, RED, 3, 11)
    ctext(d, ox - 80, cy, "一様引張", FT, RED, "rm"); ctext(d, ox + w + 80, cy, "一様引張", FT, RED, "lm")
    ctext(d, cx, oy + h + 24, "薄板・面外荷重なし", FT, GRAY)
    note(d, "孔縁の応力集中を経済的に解く。最も適切な要素は?")
    save(im, "model8PlateHoleSetup")


# ---- 8-10 フランジ周の離散ボルト ----
def f_bolt_circle():
    im, d = new(); title(d, "圧力容器フランジ周に離散配置した取付けボルト")
    cx, cy, R = 320, 215, 140
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=BLACK, width=3, fill=FILL1)
    d.ellipse((cx - R + 40, cy - R + 40, cx + R - 40, cy + R - 40), outline=BLACK, width=2, fill="white")
    for k in range(12):
        t = math.radians(k * 30); bx, by = cx + (R - 20) * math.cos(t), cy - (R - 20) * math.sin(t)
        d.ellipse((bx - 7, by - 7, bx + 7, by + 7), outline=BLACK, width=2, fill=FILL3)
    ctext(d, cx, cy, "内圧", FT, GRAY)
    note(d, "離散ボルト周りの局所応力集中を解く。最も適切な要素は?")
    save(im, "model8BoltCircleSetup")


# ---- 8-11 鉄塔 ----
def f_tower():
    im, d = new(); title(d, "円管部材で組まれた鉄塔(風荷重)")
    ax, ay, bw, tw, top, bot = 320, 0, 220, 70, 110, 330
    L = (ax - bw / 2, bot); R = (ax + bw / 2, bot); TL = (ax - tw / 2, top); TR = (ax + tw / 2, top)
    d.line((L, TL), fill=BLACK, width=3); d.line((R, TR), fill=BLACK, width=3); d.line((TL, TR), fill=BLACK, width=3)
    for i in range(1, 4):
        t = i / 4.0
        ly = bot + (top - bot) * t
        lx1 = ax - (bw / 2 + (tw / 2 - bw / 2) * t); lx2 = ax + (bw / 2 + (tw / 2 - bw / 2) * t)
        d.line((lx1, ly, lx2, ly), fill=BLACK, width=2)
    # ブレース(×)
    segs = [0, 0.33, 0.66, 1.0]
    for i in range(3):
        t0, t1 = segs[i], segs[i + 1]
        def P(t, side):
            y = bot + (top - bot) * t; hw = bw / 2 + (tw / 2 - bw / 2) * t
            return (ax + side * hw, y)
        d.line((P(t0, -1), P(t1, 1)), fill=BLACK, width=2); d.line((P(t0, 1), P(t1, -1)), fill=BLACK, width=2)
    hwall(d, L[0] - 10, R[0] + 10, bot, 1, 12)
    for yy in (top + 50, top + 120):
        arrow(d, ax - 200, yy, ax - 120, yy, RED, 3, 12)
    ctext(d, ax - 215, top + 50, "風荷重", FT, RED, "rm")
    ctext(d, ax, bot + 20, "脚柱・横材・斜材ブレース(円管)", FT, GRAY)
    note(d, "各部材の軸力・モーメントを求める。最適なモデル化は?")
    save(im, "model8TowerSetup")


# ---- 8-12 長いトンネル ----
def f_tunnel():
    im, d = new(); title(d, "断面一様で長いトンネル")
    ox, oy, w, h, dp = 170, 140, 230, 180, 90
    d.polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)], outline=BLACK, width=3, fill=FILL1)
    d.polygon([(ox, oy), (ox + dp, oy - dp * 0.5), (ox + w + dp, oy - dp * 0.5), (ox + w, oy)], outline=BLACK, width=2, fill=FILL2)
    d.polygon([(ox + w, oy), (ox + w + dp, oy - dp * 0.5), (ox + w + dp, oy + h - dp * 0.5), (ox + w, oy + h)], outline=BLACK, width=2, fill=FILL3)
    tx, ty = ox + w / 2, oy + h / 2 + 20
    d.arc((tx - 45, ty - 70, tx + 45, ty + 20), 180, 360, fill=BLACK, width=3)
    d.line((tx - 45, ty + 20, tx - 45, ty - 25), fill=BLACK, width=3); d.line((tx + 45, ty + 20, tx + 45, ty - 25), fill=BLACK, width=3)
    d.line((tx - 45, ty + 20, tx + 45, ty + 20), fill=BLACK, width=3)
    ctext(d, tx, oy + h + 18, "横断面", FT, GRAY)
    arrow(d, ox + w, oy + h + 30, ox + w + dp, oy + h + 30 - dp * 0.5, GRAY, 2, 10); ctext(d, ox + w + dp + 8, oy + h + 10, "長手方向(断面一様)", FT, GRAY, "lm")
    note(d, "長手直交の横断面を効率よく二次元で解く。最適なモデル化は?")
    save(im, "model8TunnelSetup")


# ---- 8-13 懸荷用フック ----
def f_hook():
    # 回答後図 model8Hook と同一の「開いたC字=吊りフック」形状(中立)。
    # 構造形状・荷重・与件(円形で太い断面)のみ。要素種別/曲がりはり/せん断等の
    # 答え・ヒントは描かない。
    im, d = new(); title(d, "曲率をもつ太い断面の懸荷用フック")
    cx, cy = 320, 215
    Ro, Ri = 100, 52
    # 本体(開いた太い環=大きく湾曲した太いはり)
    d.arc((cx - Ro, cy - Ro, cx + Ro, cy + Ro), -30, 290, fill=BLACK, width=4)
    d.arc((cx - Ri, cy - Ri, cx + Ri, cy + Ri), -30, 290, fill=BLACK, width=4)
    for a in (-30, 290):
        ar = math.radians(a)
        d.line((cx + Ri * math.cos(ar), cy + Ri * math.sin(ar),
                cx + Ro * math.cos(ar), cy + Ro * math.sin(ar)), fill=BLACK, width=4)
    # 上部シャンク(天井に取付)
    d.rectangle((cx - 15, 70, cx + 15, cy - Ro + 6), outline=BLACK, width=3, fill=FILL1)
    hwall(d, cx - 26, cx + 26, 70, side=-1, n=5)
    # 断面が太い・円形(与件のみ)
    dim(d, cx - Ro - 16, cy, cx - Ri - 4, cy, "太い断面", col=GRAY)
    ctext(d, cx + Ro + 8, cy, "円形断面", FT, GRAY, "lm")
    # 吊り荷重(内側下部)
    lx, ly = cx, cy + (Ri + Ro) / 2 + 6
    force(d, lx, ly, 0, 64, "W", RED)
    note(d, "最大応力を求める。FEMで最も適切な要素は?")
    save(im, "model8HookSetup")


# ---- 8-14 開断面(溝形)はり ----
def f_channel():
    im, d = new(); title(d, "厚肉の溝形(開断面)はり(曲げ＋ねじり)")
    ox, oy = 250, 150
    pts = [(ox + 120, oy), (ox, oy), (ox, oy + 180), (ox + 120, oy + 180),
           (ox + 120, oy + 150), (ox + 30, oy + 150), (ox + 30, oy + 30), (ox + 120, oy + 30)]
    d.polygon(pts, outline=BLACK, width=3, fill=FILL1)
    ctext(d, ox + 150, oy + 90, "溝形(開断面)", FT, GRAY, "lm")
    arrow(d, ox + 60, oy - 50, ox + 60, oy - 8, RED, 3, 12); ctext(d, ox + 60, oy - 66, "曲げ荷重", FS, RED)
    d.arc((ox + 20, oy + 196, ox + 100, oy + 236), 200, 520, fill=RED, width=3); arrow(d, ox + 96, oy + 214, ox + 104, oy + 228, RED, 3, 9)
    ctext(d, ox + 60, oy + 250, "ねじり", FT, RED)
    note(d, "上面の軸方向ひずみへのねじりの影響を局所的に確認。最適な要素は?")
    save(im, "model8ChannelBeamSetup")


# ---- 8-15 円筒サイロ・横風 ----
def f_silo():
    im, d = new(); title(d, "円錐屋根付き円筒サイロ(横風)")
    cx = 330; top, bot, r = 150, 330, 85
    d.polygon([(cx - r, top), (cx + r, top), (cx, top - 70)], outline=BLACK, width=3, fill=FILL1); ctext(d, cx, top - 90, "円錐屋根", FT, GRAY)
    d.rectangle((cx - r, top, cx + r, bot), outline=BLACK, width=3, fill=FILL1); ctext(d, cx, (top + bot) / 2, "円筒サイロ", FT, GRAY)
    hwall(d, cx - r - 16, cx + r + 16, bot, 1, 10); ctext(d, cx, bot + 20, "地面に固定", FT, GRAY)
    for yy in (top + 50, top + 110, top + 170):
        arrow(d, cx - r - 90, yy, cx - r - 8, yy, RED, 3, 11)
    ctext(d, cx - r - 120, top + 110, "風荷重", FT, RED, "rm")
    note(d, "横風に対する応力分布を効率よく詳細に。最適なモデル化は?")
    save(im, "model8SiloSetup")


def main():
    f_saddle_axial(); f_saddle_transverse(); f_arch_bridge(); f_nozzle(); f_skirt(); f_lng()
    f_dumbbell(); f_plate_hole(); f_bolt_circle(); f_tower(); f_tunnel(); f_hook(); f_channel(); f_silo()
    print("done 14 figures")


if __name__ == "__main__":
    main()
