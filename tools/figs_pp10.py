# -*- coding: utf-8 -*-
"""CAE固体2級 第10章プリポスト処理 図16枚。白地660x420・線画。JSONは編集しない。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

# ---- ローカル補助 ----
def grid(d, x0, y0, x1, y1, nx, ny, col=LGRAY, wd=1):
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        d.line((x, y0, x, y1), fill=col, width=wd)
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        d.line((x0, y, x1, y), fill=col, width=wd)

def rings(d, cx, cy, r0, r1, nr, nsp, a0=0, a1=360, col=BLACK, wd=1):
    for i in range(nr + 1):
        r = r0 + (r1 - r0) * i / nr
        d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    for k in range(nsp + 1):
        a = math.radians(a0 + (a1 - a0) * k / nsp)
        d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a),
                cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=col, width=wd)

def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=9):
    L = math.hypot(x2 - x1, y2 - y1)
    n = max(1, int(L / dash))
    for i in range(n):
        if i % 2:
            continue
        t0, t1 = i / n, (i + 1) / n
        d.line((x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0,
                x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1), fill=col, width=wd)

def dot(d, x, y, r=6, col=RED):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=BLACK, width=2)

JET = [(20, 60, 200), (0, 150, 220), (0, 175, 110), (150, 200, 0),
       (240, 205, 0), (240, 130, 0), (215, 35, 35)]

def colorbar(d, x, y0, y1, cols, labels):
    n = len(cols); h = (y1 - y0) / n
    for i, c in enumerate(cols):
        yy = y1 - (i + 1) * h
        d.rectangle((x, yy, x + 26, yy + h), fill=c, outline=BLACK, width=1)
    for i, lb in enumerate(labels):
        yy = y1 - i * (y1 - y0) / (len(labels) - 1)
        ctext(d, x + 34, yy, lb, FT, BLACK, "lm")

# ===== 1. 丸穴薄板の引張 =====
def f_HolePlateTension():
    im, d = new(); title(d, "丸穴薄板の引張(穴縁Aに応力集中)")
    x0, y0, x1, y1 = 160, 120, 500, 300
    cx, cy, r = 330, 210, 38
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
    grid(d, x0, y0, x1, y1, 8, 4)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white", outline=BLACK, width=3)
    rings(d, cx, cy, r, r + 34, 3, 16)
    force(d, x0, cy, -50, 0, "P"); force(d, x1, cy, 50, 0, "P")
    dot(d, cx, cy - r); ctext(d, cx + 14, cy - r - 16, "A", F, RED, "lm")
    dot(d, cx, cy + r)
    note(d, "引張と直交する穴縁(A)で応力が最大")
    save(im, "pp10HolePlateTension")

# ===== 2. 丸穴片持ちはり =====
def f_HoleCantilever():
    im, d = new(); title(d, "丸穴片持ちはり(穴周りを板厚方向に細分)")
    wall(d, 130, 140, 300)
    x0, x1, yt, yb = 130, 520, 150, 290
    cx, cy, r = 320, 220, 30
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3)
    grid(d, x0, yt, x1, yb, 9, 4)
    # 穴周りは板厚方向(縦)に複数要素で細分
    for gx in range(int(cx - 70), int(cx + 71), 14):
        d.line((gx, yt, gx, yb), fill=LGRAY, width=1)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill="white", outline=BLACK, width=3)
    rings(d, cx, cy, r, r + 26, 3, 16)
    force(d, x1 - 6, yt - 2, 0, 46, "F")
    note(d, "穴の近くほど要素を小さく(板厚方向に複数層)")
    save(im, "pp10HoleCantilever")

# ===== 3. V切欠き薄板 =====
def f_NotchPlate():
    im, d = new(); title(d, "V切欠き薄板(切欠き先端に細メッシュ)")
    x0, y0, x1, y1 = 160, 120, 500, 300
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
    grid(d, x0, y0, x1, y1, 8, 4)
    tx, ty = 330, 224   # 切欠き先端
    lx, rx = 300, 360   # 上縁の開口
    # V切欠き(上縁から先端まで、内部は空)を白で抜く
    d.polygon([(lx, y0), (rx, y0), (tx, ty)], fill="white", outline=BLACK, width=3)
    # 先端まわりに扇状の細メッシュ
    rings(d, tx, ty, 8, 40, 3, 8, a0=15, a1=165)
    force(d, x0, 210, -48, 0, "P"); force(d, x1, 210, 48, 0, "P")
    dot(d, tx, ty); ctext(d, tx + 12, ty + 16, "先端", FT, RED, "lm")
    note(d, "先端の応力集中を捉えるため要素を細かく")
    save(im, "pp10NotchPlate")

# ===== 4. 円板の上下圧縮 1/4対称 =====
def f_CompressDisk():
    im, d = new(); title(d, "円板の上下圧縮:1/4対称モデル")
    ox, oy, R = 190, 330, 190   # 原点(左下)・半径
    d.arc((ox - R, oy - R, ox + R, oy + R), -90, 0, fill=BLACK, width=3)
    d.line((ox, oy, ox + R, oy), fill=BLACK, width=3)     # 底(対称面)
    d.line((ox, oy, ox, oy - R), fill=BLACK, width=3)     # 左(対称面)
    # 放射メッシュ(荷重点=上ほど細かく)
    for i in range(1, 5):
        rr = R * i / 4
        d.arc((ox - rr, oy - rr, ox + rr, oy + rr), -90, 0, fill=LGRAY, width=1)
    for a in range(0, 91, 15):
        ar = math.radians(a)
        d.line((ox, oy, ox + R * math.cos(ar), oy - R * math.sin(ar)), fill=LGRAY, width=1)
    rings(d, ox, oy - R, 6, 34, 2, 4, a0=0, a1=90)
    force(d, ox, oy - R - 4, 0, 40, "P")   # 上面(対称軸)の集中荷重
    ctext(d, ox + R * 0.5, oy + 18, "対称拘束", FT, BLUE)
    ctext(d, ox - 40, oy - R * 0.5, "対称拘束", FT, BLUE, "mm")
    note(d, "1/4だけ解いて全体を代表(対称面は面直を拘束)")
    save(im, "pp10CompressDisk")

# ===== 5. 溶接止端部 =====
def f_WeldToe():
    im, d = new(); title(d, "溶接止端部(板厚10mm・止端から3mmで評価)")
    # 母材(横板)
    bx0, bx1, byt, byb = 140, 520, 240, 290
    d.rectangle((bx0, byt, bx1, byb), fill=FILL1, outline=BLACK, width=3)
    dim(d, bx1 + 16, byt, bx1 + 16, byb, "板厚10mm", col=GRAY)
    # 立板
    d.rectangle((330, 120, 380, byt), fill=FILL2, outline=BLACK, width=3)
    # 溶接ビード(すみ肉)
    toe = (300, byt)
    d.polygon([(300, byt), (330, byt), (330, 205)], fill=FILL3, outline=BLACK, width=2)
    # 止端と評価点(3mm=板厚の30%, 10mm->50px なので15px)
    dot(d, toe[0], toe[1]); ctext(d, toe[0] - 6, toe[1] - 16, "止端", FT, RED, "mm")
    ev = (toe[0] - 15, byt)
    dot(d, ev[0], ev[1], col=BLUE)
    dim(d, ev[0], byt + 18, toe[0], byt + 18, "3mm(板厚の30%)", col=BLUE)
    ctext(d, ev[0] - 8, byt - 16, "評価点", FT, BLUE, "rm")
    note(d, "止端は特異点。少し離れた点で応力を評価する")
    save(im, "pp10WeldToe")

# ===== 6. 長方形 vs 平行四辺形 =====
def f_QuadParallelogram():
    im, d = new(); title(d, "四辺形要素:長方形(良)と平行四辺形(歪)")
    # 左:長方形
    a = [(100, 150), (250, 150), (250, 300), (100, 300)]
    d.polygon(a, outline=BLACK, width=3)
    mt = ((a[0][0] + a[1][0]) / 2, 150); mb = ((a[3][0] + a[2][0]) / 2, 300)
    ml = (100, 225); mr = (250, 225)
    dashed(d, mt[0], mt[1], mb[0], mb[1], BLUE); dashed(d, ml[0], ml[1], mr[0], mr[1], BLUE)
    ctext(d, 175, 335, "90°(良)", FS, GREEN)
    # 右:平行四辺形
    b = [(380, 150), (560, 150), (600, 300), (420, 300)]
    d.polygon(b, outline=BLACK, width=3)
    mt2 = ((b[0][0] + b[1][0]) / 2, 150); mb2 = ((b[3][0] + b[2][0]) / 2, 300)
    ml2 = ((b[0][0] + b[3][0]) / 2, 225); mr2 = ((b[1][0] + b[2][0]) / 2, 225)
    dashed(d, mt2[0], mt2[1], mb2[0], mb2[1], BLUE); dashed(d, ml2[0], ml2[1], mr2[0], mr2[1], BLUE)
    ctext(d, 500, 335, "傾き(歪)", FS, RED)
    note(d, "対辺中点を結ぶ線の交角が90°から離れるほど悪い")
    save(im, "pp10QuadParallelogram")

# ===== 7. 台形の対角線分割 =====
def f_QuadTrapezoid():
    im, d = new(); title(d, "台形要素:対角線分割で面積差を比較")
    q = [(150, 150), (470, 150), (390, 300), (230, 300)]
    d.polygon(q, outline=BLACK, width=3)
    # 対角線
    d.line((q[0][0], q[0][1], q[2][0], q[2][1]), fill=RED, width=2)
    d.line((q[1][0], q[1][1], q[3][0], q[3][1]), fill=BLUE, width=2)
    # 対角線1で2三角形に分け面積差を示す
    d.polygon([q[0], q[1], q[2]], fill=(255, 236, 236))
    d.polygon([q[0], q[2], q[3]], fill=(232, 240, 255))
    d.polygon(q, outline=BLACK, width=3)
    d.line((q[0][0], q[0][1], q[2][0], q[2][1]), fill=BLACK, width=2)
    ctext(d, 350, 200, "面積 大", FS, RED)
    ctext(d, 240, 255, "面積 小", FS, BLUE)
    note(d, "対角線で分けた三角形の面積差が大きいほど歪んだ要素")
    save(im, "pp10QuadTrapezoid")

# ===== 8. 良→悪の並べ比較 =====
def f_QuadCompare():
    im, d = new(); title(d, "四辺形の良→悪(角度と面積差で判定)")
    base = 300
    # 良:正方形
    q1 = [(70, 180), (190, 180), (190, base), (70, base)]
    # やや:傾き
    q2 = [(260, 180), (380, 180), (410, base), (240, base)]
    # 悪:大きく歪む
    q3 = [(470, 180), (590, 180), (640, base), (430, base)]
    for q in (q1, q2, q3):
        d.polygon(q, outline=BLACK, width=3)
    ctext(d, 130, 150, "良", F, GREEN); ctext(d, 130, base + 22, "角90°", FT, GREEN)
    ctext(d, 320, 150, "やや", F, ORANGE); ctext(d, 320, base + 22, "角ずれ小", FT, ORANGE)
    ctext(d, 530, 150, "悪", F, RED); ctext(d, 530, base + 22, "角ずれ大", FT, RED)
    note(d, "内角が90°から離れ面積差が増すほど精度が落ちる")
    save(im, "pp10QuadCompare")

# ===== 9. 穴あきソリッド→六面体プリミティブ =====
def f_SolidPrimitive():
    im, d = new(); title(d, "穴あきソリッドを六面体プリミティブに分割")
    # 左:穴あきブロック
    iso_box(d, 70, 200, 150, 90, 55)
    d.ellipse((120, 215, 160, 240), fill="white", outline=BLACK, width=2)  # 穴(上面)
    d.line((120, 227, 120, 285), fill=GRAY, width=1); d.line((160, 227, 160, 285), fill=GRAY, width=1)
    ctext(d, 150, 320, "穴あきソリッド", FT, BLACK)
    arrow(d, 300, 250, 360, 250, BLACK, 4, 15)
    # 右:穴を囲む六面体プリミティブ(4分割)
    for (ox, oy) in [(400, 190), (470, 190), (400, 250), (470, 250)]:
        iso_box(d, ox, oy, 62, 42, 30)
    ctext(d, 500, 330, "六面体プリミティブの集合", FT, BLACK)
    note(d, "分割しにくい形は単純な六面体の集まりに置き換える")
    save(im, "pp10SolidPrimitive")

# ===== 10. スイープ(掃引) =====
def f_Sweeping():
    im, d = new(); title(d, "掃引:ソース面を層状に伸ばし六面体を生成")
    sx, sy, w, h = 120, 200, 120, 120   # ソース面(前)
    dx, dy = 55, 34                      # 掃引方向(奥)
    layers = 3
    # 各層の四辺形をずらして描く(奥から手前)
    for k in range(layers, -1, -1):
        ox = sx + dx * k; oy = sy - dy * k
        col = LGRAY if k else BLACK
        d.rectangle((ox, oy, ox + w, oy + h), outline=col, width=2 if k else 3)
        d.line((ox + w / 2, oy, ox + w / 2, oy + h), fill=col, width=1)
        d.line((ox, oy + h / 2, ox + w, oy + h / 2), fill=col, width=1)
    # 掃引方向の稜線
    for (px, py) in [(sx, sy), (sx + w, sy), (sx + w, sy + h), (sx, sy + h)]:
        d.line((px, py, px + dx * layers, py - dy * layers), fill=BLACK, width=2)
    arrow(d, sx + w + 20, sy + h + 30, sx + w + 20 + dx, sy + h + 30 - dy, GREEN, 4, 14)
    ctext(d, sx + w + 70, sy + h + 6, "掃引方向", FT, GREEN, "lm")
    ctext(d, sx + w / 2, sy + h + 26, "ソース面(四辺形)", FT, BLACK)
    note(d, "ソース面の四辺形をそのまま押し出して六面体を積む")
    save(im, "pp10Sweeping")

# ===== 11. ねじり丸棒の破断 =====
def f_TorsionFracture():
    im, d = new(); title(d, "ねじり丸棒:ぜい性45°らせん / 延性 軸直角")
    def bar_h(y):
        x0, x1, rr = 150, 500, 34
        d.line((x0, y - rr, x1, y - rr), fill=BLACK, width=3)
        d.line((x0, y + rr, x1, y + rr), fill=BLACK, width=3)
        d.arc((x0 - 14, y - rr, x0 + 14, y + rr), 90, 270, fill=BLACK, width=3)
        d.arc((x1 - 14, y - rr, x1 + 14, y + rr), 270, 450, fill=BLACK, width=3)
        d.ellipse((x1 - 14, y - rr, x1 + 14, y + rr), outline=BLACK, width=2)
        # ねじりトルク(両端の回転矢印)
        d.arc((x0 - 26, y - 26, x0 + 2, y + 26), 200, 340, fill=GRAY, width=2)
        return x0, x1, rr
    # 上:ぜい性(45°らせん破断)
    x0, x1, rr = bar_h(150)
    for cx in (280, 340):
        d.line((cx - rr, 150 + rr, cx + rr, 150 - rr), fill=RED, width=3)
    ctext(d, 130, 110, "ぜい性:45°らせん破断", FS, RED, "lm")
    # 下:延性(軸直角破断)
    x0, x1, rr = bar_h(300)
    d.line((330, 300 - rr, 330, 300 + rr), fill=BLUE, width=3)
    ctext(d, 130, 355, "延性:軸に直角な破断", FS, BLUE, "lm")
    save(im, "pp10TorsionFracture")

# ===== 12. z荷重片持ち板のたわみ等高線 =====
def f_CantileverContour():
    im, d = new(); title(d, "z荷重片持ち板:自由端ほど大きいたわみ")
    wall(d, 150, 140, 300)
    x0, x1, yt, yb = 150, 520, 140, 300
    d.rectangle((x0, yt, x1, yb), outline=BLACK, width=3)
    n = 6
    for i in range(1, n + 1):
        x = x0 + (x1 - x0) * i / (n + 1)
        c = JET[min(len(JET) - 1, i)]
        d.line((x, yt, x, yb), fill=c, width=3)
        ctext(d, x, yb + 14, str(i), FT, c)
    ctext(d, x0 + 6, yt - 12, "0(固定)", FT, JET[0], "lm")
    ctext(d, x1 - 6, yt - 12, "最大(自由端)", FT, JET[-1], "rm")
    force(d, x1 - 4, yt - 4, 0, 40, "z")
    note(d, "たわみは固定端で0、自由端に向かって増える")
    save(im, "pp10CantileverContour")

# ===== 13. 2軸引張 自由表面の主応力ベクトル =====
def f_StressVector():
    im, d = new(); title(d, "2軸引張の自由表面:面内の主応力ベクトル")
    cx, cy, s = 330, 220, 70
    d.rectangle((cx - s, cy - s, cx + s, cy + s), fill=FILL1, outline=BLACK, width=3)
    # 最大主応力(長い矢印・両向き)
    force(d, cx + s, cy, 60, 0, "最大主応力", RED)
    force(d, cx - s, cy, -60, 0, "", RED)
    # 中間主応力(短い矢印・直交)
    force(d, cx, cy - s, 0, -40, "中間主応力", BLUE)
    force(d, cx, cy + s, 0, 40, "", BLUE)
    ctext(d, cx, cy, "面直=0", FT, GRAY)
    note(d, "自由表面は面直の主応力が0。主応力は面内の2本")
    save(im, "pp10StressVector")

# ===== 14. 主応力矢印列:6要素目で90°急変 =====
def f_PrincipalArrows():
    im, d = new(); title(d, "最大主応力の矢印列:6要素目で向きが90°急変")
    y = 220; n = 8; x0 = 90; step = 62
    for i in range(n):
        cx = x0 + i * step
        col = RED if i == 5 else BLACK
        d.rectangle((cx - 24, y - 24, cx + 24, y + 24), outline=col, width=3 if i == 5 else 2)
        if i == 5:  # 90°急変(縦向き)
            arrow(d, cx, y + 18, cx, y - 18, RED, 3, 11)
            arrow(d, cx, y - 18, cx, y + 18, RED, 3, 11)
        else:       # 横向き(両矢印)
            arrow(d, cx - 18, y, cx + 18, y, BLACK, 3, 11)
            arrow(d, cx + 18, y, cx - 18, y, BLACK, 3, 11)
        ctext(d, cx, y + 40, str(i + 1), FT, col)
    ctext(d, x0 + 5 * step, y - 44, "急変", FT, RED)
    note(d, "隣り合う要素で主応力の向きが飛ぶ=要注意(粗い/特異)")
    save(im, "pp10PrincipalArrows")

# ===== 15. 一様引張 単色コンタ =====
def f_UniformContour():
    im, d = new(); title(d, "一様引張σx:高低差がなく単色のコンタ")
    x0, y0, x1, y1 = 150, 130, 470, 300
    d.rectangle((x0, y0, x1, y1), fill=JET[3], outline=BLACK, width=3)
    grid(d, x0, y0, x1, y1, 6, 3, col=(120, 160, 60))
    force(d, x0, (y0 + y1) / 2, -46, 0, "σx"); force(d, x1, (y0 + y1) / 2, 46, 0, "σx")
    colorbar(d, 510, 150, 300, [JET[3]] * 5, ["", "", "σx", "", ""])
    ctext(d, 310, 215, "全域 同色", F, "white")
    note(d, "断面が一定なら応力は一定=色の濃淡が出ない")
    save(im, "pp10UniformContour")

# ===== 16. 相当応力の塗りコンタ+凡例 =====
def f_FilledContour():
    im, d = new(); title(d, "相当応力の塗りコンタ(最小0以上+凡例)")
    x0, y0, x1, y1 = 130, 130, 470, 300
    n = len(JET); bw = (x1 - x0) / n
    for i in range(n):
        bx = x0 + i * bw
        d.rectangle((bx, y0, bx + bw, y1), fill=JET[i], outline=None)
    d.rectangle((x0, y0, x1, y1), outline=BLACK, width=3)
    for i in range(1, n):
        bx = x0 + i * bw
        d.line((bx, y0, bx, y1), fill="white", width=1)
    colorbar(d, 510, 140, 300, JET, ["0", "", "", "中", "", "", "最大"])
    ctext(d, 300, y1 + 16, "相当応力(von Mises)は常に0以上", FT, BLACK)
    note(d, "塗りコンタは値の帯を色分け。凡例(カラーバー)で対応を読む")
    save(im, "pp10FilledContour")

if __name__ == "__main__":
    f_HolePlateTension()
    f_HoleCantilever()
    f_NotchPlate()
    f_CompressDisk()
    f_WeldToe()
    f_QuadParallelogram()
    f_QuadTrapezoid()
    f_QuadCompare()
    f_SolidPrimitive()
    f_Sweeping()
    f_TorsionFracture()
    f_CantileverContour()
    f_StressVector()
    f_PrincipalArrows()
    f_UniformContour()
    f_FilledContour()
    print("done")
