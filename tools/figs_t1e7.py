# -*- coding: utf-8 -*-
"""熱流体力学1級 第7章「高速化とポスト処理」問題図 12枚。figlibで白地660x420線画。
required(回答前提示) の t1e7SpeedupCurve は「形」だけを中立に描き、原因のラベル・注記は一切描かない。"""
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


def fbox(d, cx, cy, w, h, text, fill=FILL1, fnt=FS, col=BLACK):
    box(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill)
    ls = text.split("\n")
    for i, line in enumerate(ls):
        ctext(d, cx, cy - (len(ls) - 1) * 11 + i * 22, line, fnt, col)


def curve(d, pts, col=BLACK, wd=2):
    d.line(pts, fill=col, width=wd, joint="curve")


def swirl(d, cx, cy, r, cw=True, col=BLUE, wd=2):
    a0, a1 = 20, 300
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    end = math.radians(a1 if cw else a0)
    ex, ey = cx + r * math.cos(end), cy + r * math.sin(end)
    t = end + (math.pi / 2 if cw else -math.pi / 2)
    for s in (0.6, -0.6):
        d.line((ex, ey, ex - 10 * math.cos(t - s), ey - 10 * math.sin(t - s)), fill=col, width=wd)


# ============================================================ 7-1 アムダール法則(helpful)
def f_amdahl():
    im, d = new()
    title(d, "アムダール法則：速度向上は頭打ちになる")
    ox, oy = 95, 340
    axes(d, ox, oy, 480, 275, "並列数 n", "速度向上 S")
    p = 0.9            # 並列化率 → Smax = 1/(1-p) = 10
    Smax = 1.0 / (1 - p)
    sc = (oy - 100) / Smax
    xn = lambda n: ox + (n / 64.0) * 460
    # 頭打ち漸近線
    dash(d, ox, oy - Smax * sc, ox + 470, oy - Smax * sc, GRAY, 2, 10, 6)
    ctext(d, ox + 250, oy - Smax * sc - 16, "Smax = 1/(1-p)（頭打ち値）", FT, GRAY, "lm")
    # 速度向上曲線
    pts = []
    for n in range(1, 65):
        S = 1.0 / ((1 - p) + p / n)
        pts.append((xn(n), oy - S * sc))
    curve(d, pts, BLUE, 3)
    ctext(d, xn(50), oy - 8.6 * sc + 22, "実際の速度向上 S(n)", FT, BLUE, "lm")
    # 理想線(S=n)＝比較(細い)
    dash(d, ox, oy, xn(Smax) + 4, oy - Smax * sc - 4, LGRAY, 2, 8, 6)
    ctext(d, xn(9), oy - Smax * sc + 8, "理想 S=n", FT, LGRAY, "lm")
    for n in (16, 32, 64):
        ctext(d, xn(n), oy + 14, str(n), FT, BLACK)
    note(d, "逐次部分が残るため、n を増やしても S は Smax=1/(1-p) で飽和する")
    save(im, "t1e7Amdahl")


# ============================================================ 7-2 負荷分散(helpful)
def f_load_balance():
    im, d = new()
    title(d, "負荷分散：最遅プロセッサが律速 → 均衡で待ちを解消")
    base = 350
    sc = 5.5           # 1ms = 5.5px
    def bars(x0, vals, cap, capcol, tag):
        for i, v in enumerate(vals):
            bx = x0 + i * 46
            box(d, bx, base - v * sc, bx + 34, base, (225, 235, 250))
            ctext(d, bx + 17, base + 14, "P%d" % (i + 1), FT, BLACK)
            ctext(d, bx + 17, base - v * sc - 12, "%d" % v, FT, BLUE)
            # 待ち時間(バー上端〜律速ライン)
            if v < cap:
                dash(d, bx + 17, base - v * sc, bx + 17, base - cap * sc, capcol, 1, 5, 4)
        dash(d, x0 - 6, base - cap * sc, x0 + len(vals) * 46 - 12, base - cap * sc, capcol, 2, 8, 5)
        ctext(d, x0 + len(vals) * 46 - 6, base - cap * sc, tag, FT, capcol, "lm")
    # 左：均衡前
    bars(70, [20, 20, 20, 32], 32, RED, "律速 32ms")
    ctext(d, 158, 90, "均衡前", FS, BLACK)
    ctext(d, 158, 112, "3台は待ち時間発生", FT, RED)
    # 右：均衡後
    bars(400, [23, 23, 23, 23], 23, GREEN, "平均 23ms")
    ctext(d, 488, 90, "均衡後", FS, BLACK)
    ctext(d, 488, 112, "全台そろって待ち無し", FT, GREEN)
    ctext(d, 60, base + 14, "計算時間", FT, GRAY, "rm")
    note(d, "最も遅い処理が全体を律速する。仕事を配り直すと総時間が短くなる")
    save(im, "t1e7LoadBalance")


# ============================================================ 7-3 通信方式の対比(helpful)
def f_message_passing():
    im, d = new()
    title(d, "メッセージパッシング(MPI) と データ並列(HPF)")
    # 左：MPI = プロセス間で明示的に通信
    ctext(d, 175, 66, "MPI：プロセス間で明示通信", FS, BLACK)
    pos = [(110, 140), (240, 140), (110, 250), (240, 250)]
    for i, (px, py) in enumerate(pos):
        fbox(d, px, py, 74, 46, "プロセス%d\n(独立メモリ)" % i, (235, 240, 250), FT)
    pairs = [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]
    for a, b in pairs:
        ax, ay = pos[a]; bx, by = pos[b]
        dash(d, ax, ay, bx, by, ORANGE, 2, 9, 6)
    ctext(d, 175, 200, "send / recv", FT, ORANGE)
    ctext(d, 175, 318, "各自のデータを明示的にやり取り", FT, GRAY)
    # 仕切り
    dash(d, 335, 80, 335, 340, LGRAY, 2, 8, 6)
    # 右：HPF = 配列をプロセッサに分散
    ctext(d, 500, 66, "HPF：配列を分散(データ並列)", FS, BLACK)
    ax0 = 380
    grp = [BLUE, GREEN, ORANGE, RED]
    for i in range(8):
        cx = ax0 + i * 30
        box(d, cx, 150, cx + 28, 200, (240, 240, 240), grp[i // 2], 2)
        ctext(d, cx + 14, 175, "A%d" % i, FT, BLACK)
    for k in range(4):
        ctext(d, ax0 + k * 60 + 29, 220, "PE%d" % k, FT, grp[k])
    ctext(d, 500, 260, "同じ操作を分散配列へ一斉適用", FT, GRAY)
    ctext(d, 500, 300, "(通信はコンパイラが自動生成)", FT, GRAY)
    note(d, "MPIは通信を人が書く／HPFは配列分散を宣言し処理を一括記述する")
    save(im, "t1e7MessagePassing")


# ============================================================ 7-4 レンダリングと陰面消去(helpful)
def f_render_pipeline():
    im, d = new()
    title(d, "レンダリングの流れ と 陰面消去(Zバッファ)")
    steps = ["形状データ", "座標変換\n投影", "ラスタ\nライズ", "陰面消去\n(Zバッファ)", "画像出力"]
    cxs = [80, 210, 340, 472, 604]
    for i, (s, cx) in enumerate(zip(steps, cxs)):
        fbox(d, cx, 120, 100, 54, s, (238, 242, 250), FT)
        if i < 4:
            arrow(d, cx + 50, 120, cxs[i + 1] - 50, 120, BLACK, 2, 10)
    # 陰面消去の概念
    ctext(d, 90, 220, "視点", FT, BLACK)
    node(d, 90, 250, 8, "white", BLACK)
    # 手前の面(残す)と 奥の面(隠れる)
    d.polygon([(250, 240), (330, 220), (330, 320), (250, 340)], outline=BLACK, width=3, fill=(225, 240, 228))
    ctext(d, 290, 285, "手前", FS, GREEN)
    d.polygon([(320, 230), (400, 212), (400, 300), (320, 318)], outline=GRAY, width=2, fill=None)
    dash(d, 320, 230, 400, 212, GRAY, 1, 6, 4)
    ctext(d, 430, 250, "奥(隠れる)", FT, GRAY, "lm")
    arrow(d, 98, 250, 245, 275, BLUE, 2, 10)
    ctext(d, 300, 355, "Zが小さい(手前)画素を残し、奥を消す", FT, GRAY)
    save(im, "t1e7RenderPipeline")


# ============================================================ 7-5 ラグランジュ線形補間(helpful)
def f_lagrange():
    im, d = new()
    title(d, "ラグランジュ線形補間：2点を通る直線で中間を読む")
    ox, oy = 95, 350
    axes(d, ox, oy, 470, 300, "x", "y")
    sx = (470 - 30) / 5.0        # x: 0..5
    sy = (300 - 30) / 20.0       # y: 0..20
    px = lambda x: ox + x * sx
    py = lambda y: oy - y * sy
    # データ2点 (1,4) (4,19)
    P1 = (px(1), py(4)); P2 = (px(4), py(19))
    # 直線 y = 5x - 1 を x=1..4 で
    d.line((P1[0], P1[1], P2[0], P2[1]), fill=BLUE, width=3)
    node(d, P1[0], P1[1], 6, BLUE, BLUE); ctext(d, P1[0] - 6, P1[1] + 16, "(1, 4)", FT, BLUE, "rm")
    node(d, P2[0], P2[1], 6, BLUE, BLUE); ctext(d, P2[0] + 10, P2[1], "(4, 19)", FT, BLUE, "lm")
    # x=3 の読み取り(=14, helpful)
    yx3 = 14
    dash(d, px(3), oy, px(3), py(yx3), RED, 2, 7, 5)
    dash(d, ox, py(yx3), px(3), py(yx3), RED, 2, 7, 5)
    node(d, px(3), py(yx3), 5, RED, RED)
    ctext(d, px(3), oy + 14, "x=3", FT, RED)
    ctext(d, ox - 8, py(yx3), "14", FT, RED, "rm")
    note(d, "2点を結ぶ直線上で x=3 の値を線形に読み取る（結果 14）")
    save(im, "t1e7Lagrange")


# ============================================================ 7-6 ボリュームレンダリング(helpful)
def f_volume_render():
    im, d = new()
    title(d, "ボリュームレンダリング：レイキャスティング と 伝達関数")
    # 左：視線に沿って積分
    node(d, 60, 210, 8, "white", BLACK); ctext(d, 60, 188, "視点", FT, BLACK)
    box(d, 150, 120, 340, 300, "white")
    for gx in range(150, 341, 38):
        d.line((gx, 120, gx, 300), fill=LGRAY, width=1)
    for gy in range(120, 301, 36):
        d.line((150, gy, 340, gy), fill=LGRAY, width=1)
    ctext(d, 245, 108, "ボリューム(格子データ)", FT, GRAY)
    # 視線(レイ)＋サンプル点
    ry = 210
    arrow(d, 68, ry, 360, ry, BLUE, 2, 12)
    for sx in range(165, 341, 26):
        node(d, sx, ry, 4, RED, RED)
    ctext(d, 245, 328, "視線に沿って値を積分(合成)", FT, BLUE)
    # 右：伝達関数
    ox, oy = 430, 300
    axes(d, ox, oy, 180, 170, "値", "色/不透明度")
    pts = [(ox + 8, oy - 8), (ox + 55, oy - 15), (ox + 90, oy - 120),
           (ox + 120, oy - 130), (ox + 165, oy - 40)]
    curve(d, pts, ORANGE, 3)
    ctext(d, ox + 90, 92, "伝達関数", FS, ORANGE)
    ctext(d, ox + 90, 116, "値→色・不透明度", FT, ORANGE)
    note(d, "視線ごとに値を積分し、伝達関数で値を色と不透明度へ割り当てて描画する")
    save(im, "t1e7VolumeRender")


# ============================================================ 7-7 立体視の3方式(helpful)
def f_stereoscopy():
    im, d = new()
    title(d, "立体視の3方式：左右眼の視差で奥行きを与える")
    def panel(cx, name, sub):
        # スクリーン
        d.line((cx - 55, 110, cx + 55, 110), fill=BLACK, width=4)
        ctext(d, cx, 96, name, FS, BLACK)
        # 左右の眼
        le, re = cx - 26, cx + 26
        node(d, le, 300, 9, (235, 240, 250), BLUE); ctext(d, le, 322, "左眼", FT, BLUE)
        node(d, re, 300, 9, (250, 235, 235), RED); ctext(d, re, 322, "右眼", FT, RED)
        # 左右像→各眼(視差)
        d.line((cx - 20, 112, le, 291), fill=BLUE, width=2)
        d.line((cx + 20, 112, re, 291), fill=RED, width=2)
        ctext(d, cx, 356, sub, FT, GRAY)
    panel(150, "パッシブ", "偏光メガネで\n左右像を分離")
    panel(355, "アクティブ", "シャッタメガネで\n時分割表示")
    panel(560, "裸眼", "レンズ/視差で\nメガネ無し")
    save(im, "t1e7Stereoscopy")


# ============================================================ 7-8 LIC(helpful)
def f_lic():
    im, d = new()
    title(d, "LIC(線積分畳み込み)：流れに沿って画素をぼかす")
    # 流れ場 u(x,y): ゆるい回転風
    def vel(x, y):
        return (math.cos(y * 0.9) * 0.8 + 0.6, math.sin(x * 0.9) * 0.6)
    # 左：ベクトル場(矢印)
    ctext(d, 175, 66, "ベクトル場", FS, BLACK)
    for i in range(6):
        for j in range(5):
            x = 70 + i * 42; y = 110 + j * 45
            vx, vy = vel(i * 0.8, j * 0.8)
            n = math.hypot(vx, vy)
            arrow(d, x, y, x + vx / n * 22, y + vy / n * 22, BLUE, 2, 8)
    # 右：LIC テクスチャ(流れに沿った短い筋)
    ctext(d, 490, 66, "LIC 画像", FS, BLACK)
    for i in range(11):
        for j in range(9):
            x = 380 + i * 24; y = 100 + j * 26
            vx, vy = vel(i * 0.45, j * 0.45)
            n = math.hypot(vx, vy)
            g = 60 + ((i * 7 + j * 13) % 5) * 30       # 疑似ノイズの濃淡
            col = (g, g, g)
            d.line((x - vx / n * 10, y - vy / n * 10, x + vx / n * 10, y + vy / n * 10), fill=col, width=2)
    arrow(d, 320, 250, 360, 250, GRAY, 2, 12)
    note(d, "各画素をベクトル場の流線に沿って畳み込み、流れ模様として可視化する")
    save(im, "t1e7LIC")


# ============================================================ 7-9 計算機構成とボトルネック(helpful)
def f_pc_upgrade():
    im, d = new()
    title(d, "計算機構成：CPU/GPU/メモリ/バス帯域 とボトルネック")
    fbox(d, 160, 130, 150, 56, "CPU\n(演算コア)", (235, 240, 250), FS)
    fbox(d, 500, 130, 150, 56, "GPU\n(多コア)", (235, 245, 235), FS)
    fbox(d, 330, 320, 190, 56, "主メモリ", (245, 245, 245), FS)
    # バス(帯域)
    arrow(d, 160, 158, 300, 292, BLACK, 4, 13)
    ctext(d, 150, 250, "バス帯域", FT, BLACK, "rm")
    arrow(d, 500, 158, 380, 292, BLACK, 4, 13)
    ctext(d, 470, 235, "バス帯域", FT, BLACK, "lm")
    arrow(d, 235, 130, 425, 130, GRAY, 2, 11)
    ctext(d, 330, 112, "CPU-GPU 転送", FT, GRAY)
    # ボトルネック(細い帯域)を強調
    d.ellipse((230, 250, 290, 300), outline=RED, width=3)
    ctext(d, 300, 262, "ボトルネック", FT, RED, "lm")
    ctext(d, 330, 372, "細い所(帯域不足)が全体速度を決める", FT, GRAY)
    save(im, "t1e7PCUpgrade")


# ============================================================ 7-10 速度向上曲線(required・原因は描かない)
def f_speedup_curve():
    im, d = new()
    title(d, "測定された速度向上曲線")
    ox, oy = 95, 350
    axes(d, ox, oy, 480, 300, "並列数 n", "速度向上 S")
    sx = (480 - 30) / 64.0
    sy = (300 - 30) / 12.0
    px = lambda n: ox + n * sx
    py = lambda s: oy - s * sy
    # 理論線 S=n (n=0..12 で上端へ)
    dash(d, px(0), py(0), px(12), py(12), GRAY, 2, 9, 6)
    ctext(d, px(12) + 6, py(12) + 2, "理論線 S=n", FT, GRAY, "lm")
    # 測定点(2でわずかに理論超え、16以降で右肩下がり)
    data = [(1, 1.0), (2, 2.1), (4, 3.8), (8, 6.2), (12, 8.4),
            (16, 9.3), (24, 8.3), (32, 7.0), (48, 5.6), (64, 4.8)]
    pts = [(px(n), py(s)) for n, s in data]
    curve(d, pts, BLUE, 3)
    for x, y in pts:
        node(d, x, y, 5, BLUE, BLUE)
    for n in (2, 16, 32, 64):
        ctext(d, px(n), oy + 14, str(n), FT, BLACK)
    ctext(d, px(40), py(6.5), "測定値", FT, BLUE, "lm")
    save(im, "t1e7SpeedupCurve")


# ============================================================ 7-11 GPGPU/SIMD(helpful)
def f_gpgpu():
    im, d = new()
    title(d, "GPGPU / SIMD：同一命令を多数データへ一斉適用")
    fbox(d, 330, 110, 260, 48, "1つの命令 (Single Instruction)", (255, 244, 232), FS)
    cxs = [95, 190, 285, 380, 475, 570]
    for i, cx in enumerate(cxs):
        arrow(d, 330, 134, cx, 196, ORANGE, 2, 9)
        fbox(d, cx, 220, 78, 46, "コア%d" % i, (235, 245, 235), FT)
        # 各コアの担当データ
        box(d, cx - 24, 300, cx + 24, 340, (235, 240, 250))
        ctext(d, cx, 320, "d%d" % i, FT, BLUE)
        arrow(d, cx, 243, cx, 298, GRAY, 2, 9)
    ctext(d, 330, 366, "多数コアが別々のデータ(d0..d5)を同じ命令で並列処理", FT, GRAY)
    save(im, "t1e7GPGPU")


# ============================================================ 7-12 性能チューニングの反復(helpful)
def f_tuning_loop():
    im, d = new()
    title(d, "性能チューニングの反復ループ")
    C = (330, 225)
    nodes = {
        "top": (330, 110, "ベンチマーク\n(性能測定)"),
        "right": (540, 225, "ホットスポット\n特定"),
        "bottom": (330, 340, "最適化\n(コード改良)"),
        "left": (120, 225, "再測定\n(効果確認)"),
    }
    for k, (x, y, s) in nodes.items():
        fbox(d, x, y, 170, 62, s, (238, 242, 250), FT)
    seq = ["top", "right", "bottom", "left", "top"]
    for a, b in zip(seq, seq[1:]):
        ax, ay, _ = nodes[a]; bx, by, _ = nodes[b]
        ang = math.atan2(by - ay, bx - ax)
        sx0 = ax + 95 * math.cos(ang); sy0 = ay + 40 * math.sin(ang)
        ex0 = bx - 95 * math.cos(ang); ey0 = by - 40 * math.sin(ang)
        arrow(d, sx0, sy0, ex0, ey0, GREEN, 3, 13)
    ctext(d, C[0], C[1], "反復", FS, GREEN)
    note(d, "測定→ホットスポット特定→最適化→再測定を繰り返し性能を高める")
    save(im, "t1e7TuningLoop")


if __name__ == "__main__":
    f_amdahl()
    f_load_balance()
    f_message_passing()
    f_render_pipeline()
    f_lagrange()
    f_volume_render()
    f_stereoscopy()
    f_lic()
    f_pc_upgrade()
    f_speedup_curve()
    f_gpgpu()
    f_tuning_loop()
    print("done t1e7 (12)")
