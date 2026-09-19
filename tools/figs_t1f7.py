# -*- coding: utf-8 -*-
"""熱流体力学1級 第7章「高速化とポスト処理」公式・用語図 18枚。figlibで白地660x420線画。
公式図は回答後扱いのため結論・式を描いてよい。機構のみ・装飾禁止。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *
from figs_t1e7 import dash, box, fbox, curve, swirl


def wavy(d, x0, y0, x1, y1, col=BLUE, wd=2, amp=4, period=16):
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    px, py = -uy, ux
    pts = []
    t = 0.0
    while t <= L:
        s = amp * math.sin(2 * math.pi * t / period)
        pts.append((x0 + ux * t + px * s, y0 + uy * t + py * s))
        t += 2
    d.line(pts, fill=col, width=wd, joint="curve")


# ---- 1. スピードアップ Sn=t1/tn
def f_speedup():
    im, d = new()
    title(d, "スピードアップ Sn=t1/tn（1台の時間÷n台の時間）")
    x0 = 150
    # 1プロセッサ: 並列部 p·t1(青) + 非並列部 (1-p)t1(灰)
    y1 = 150
    par = 320; ser = 80
    box(d, x0, y1 - 22, x0 + par, y1 + 22, (210, 224, 250), BLUE, 2)
    box(d, x0 + par, y1 - 22, x0 + par + ser, y1 + 22, FILL2, GRAY, 2)
    ctext(d, x0 + par / 2, y1, "並列できる部分 p·t1", FT, BLUE)
    ctext(d, x0 + par + ser / 2, y1, "非並列", FT, GRAY)
    ctext(d, x0 - 12, y1, "t1", FS, BLACK, "rm")
    ctext(d, x0 + 130, y1 - 40, "1プロセッサ(逐次)", FT, BLACK, "lm")
    # nプロセッサ: 並列部は 1/n、非並列部はそのまま残る
    y2 = 250
    parn = par // 4
    box(d, x0, y2 - 22, x0 + parn, y2 + 22, (210, 224, 250), BLUE, 2)
    box(d, x0 + parn, y2 - 22, x0 + parn + ser, y2 + 22, FILL2, GRAY, 2)
    ctext(d, x0 + parn / 2, y2, "p·t1/n", FT, BLUE)
    ctext(d, x0 + parn + ser / 2, y2, "残る", FT, GRAY)
    ctext(d, x0 - 12, y2, "tn", FS, BLACK, "rm")
    ctext(d, x0 + 200, y2 - 40, "n=4 プロセッサ(並列部だけ縮む)", FT, BLACK, "lm")
    dash(d, x0 + par + ser, y1 - 22, x0 + par + ser, y2 + 34, LGRAY, 1, 5, 4)
    dash(d, x0 + parn + ser, y2 - 22, x0 + parn + ser, y2 + 34, GRAY, 1, 5, 4)
    fbox(d, 330, 350, 560, 46, "Sn = t1/tn ,  tn = p·t1/n + (1−p)·t1\n例) p=0.8・n=4 → tn=0.4t1 → S4=2.5倍", (240, 244, 250), FT)
    save(im, "t1f7Speedup")


# ---- 2. アムダールの法則(頭打ち)
def f_amdahl():
    im, d = new()
    title(d, "アムダールの法則：速度向上は Smax=1/(1−p) で頭打ち")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 275, "プロセッサ数 n", "速度向上 S")
    p = 0.9
    Smax = 1.0 / (1 - p)
    sc = (oy - 90) / Smax
    xn = lambda n: ox + (n / 64.0) * 450
    dash(d, ox, oy - Smax * sc, ox + 460, oy - Smax * sc, GRAY, 2, 10, 6)
    ctext(d, ox + 250, oy - Smax * sc - 16, "Smax = 1/(1−p)（天井）", FT, GRAY, "lm")
    pts = []
    for n in range(1, 65):
        S = 1.0 / (p / n + (1 - p))
        pts.append((xn(n), oy - S * sc))
    curve(d, pts, BLUE, 3)
    # 理想線 S=n(初めは沿うがすぐ離れる)
    dash(d, ox, oy, xn(Smax), oy - Smax * sc, LGRAY, 2, 7, 5)
    ctext(d, xn(6), oy - 6 * sc - 14, "理想 S=n", FT, LGRAY, "lm")
    ctext(d, xn(48), oy - Smax * sc + 26, "n を増やしても頭打ち", FT, BLUE)
    fbox(d, 500, 120, 260, 46, "非並列部 (1−p) が\n最終的な速さの天井を決める", (240, 244, 250), FT)
    save(im, "t1f7Amdahl")


# ---- 3. 並列効率 E=Sn/n
def f_efficiency():
    im, d = new()
    title(d, "並列効率 E=Sn/n（理想1から低下）")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 275, "プロセッサ数 n", "効率 E")
    p = 0.8
    top = oy - 250
    e1 = top  # E=1 の高さ
    dash(d, ox, e1, ox + 460, e1, GRAY, 2, 10, 6)
    ctext(d, ox + 40, e1 - 14, "E=1（理想=無駄なし）", FT, GRAY, "lm")
    xn = lambda n: ox + (n / 16.0) * 450
    pts = []
    for n in range(1, 17):
        E = 1.0 / (1 + (n - 1) * (1 - p))
        pts.append((xn(n), oy - E * 250))
    curve(d, pts, GREEN, 3)
    for n in (1, 4, 16):
        E = 1.0 / (1 + (n - 1) * (1 - p))
        node(d, xn(n), oy - E * 250, 5, GREEN, GREEN)
    ctext(d, xn(4), oy - (1 / (1 + 3 * 0.2)) * 250 - 16, "n=4→63%", FT, GREEN, "lm")
    ctext(d, xn(16), oy - (1 / (1 + 15 * 0.2)) * 250 - 16, "n=16→25%", FT, GREEN, "lm")
    note(d, "台数を増やすほど 1台あたりの働きは落ちる（増やした分効いているかを確認）")
    save(im, "t1f7Efficiency")


# ---- 4. 通信オーバーヘッド
def f_comm_overhead():
    im, d = new()
    title(d, "並列時間 = 計算(1/n) ＋ 通信オーバーヘッド")
    ox, oy = 90, 345
    axes(d, ox, oy, 500, 285, "プロセッサ数 n", "実行時間")
    ns = [1, 2, 4, 8, 16]
    comp = {1: 200, 2: 100, 4: 50, 8: 25, 16: 12}
    comm = {n: 6 * n for n in ns}
    bw = 46
    for i, n in enumerate(ns):
        bx = ox + 40 + i * 90
        c = comp[n]; m = comm[n]
        box(d, bx, oy - c, bx + bw, oy, (210, 224, 250), BLUE, 2)       # 計算
        box(d, bx, oy - c - m, bx + bw, oy - c, (250, 226, 200), ORANGE, 2)  # 通信
        ctext(d, bx + bw / 2, oy + 14, "n=%d" % n, FT, BLACK)
        node(d, bx + bw / 2, oy - c - m, 3, RED, RED)
    ctext(d, ox + 40 + bw + 6, oy - 100, "計算=C/n\n(減る)", FT, BLUE, "lm")
    ctext(d, ox + 40 + 3 * 90 + bw + 6, oy - 60, "通信=nで増える", FT, ORANGE, "lm")
    ctext(d, ox + 40 + 3 * 90 + bw / 2, oy - 73 - 20, "総時間の最小", FT, RED)
    note(d, "高並列ほど分割境界が増えて通信が支配的に→帯域不足だと効率が急落")
    save(im, "t1f7CommOverhead")


# ---- 5. 計算負荷均衡と粒度
def f_load_balance():
    im, d = new()
    title(d, "計算負荷均衡と粒度：偏ると手待ちで効率低下")
    # 左：負荷不均衡
    baseL = 300; x0 = 90
    loads = [140, 60, 200, 90]
    tmax = max(loads)
    for i, L in enumerate(loads):
        bx = x0 + i * 45
        box(d, bx, baseL - L, bx + 30, baseL, (210, 224, 250), BLUE, 2)
        if L < tmax:  # 手待ち(遊び)をハッチ
            box(d, bx, baseL - tmax, bx + 30, baseL - L, (245, 230, 230), RED, 1)
        ctext(d, bx + 15, baseL + 12, "P%d" % (i + 1), FT, BLACK)
    dash(d, x0 - 6, baseL - tmax, x0 + 4 * 45, baseL - tmax, RED, 2, 7, 5)
    ctext(d, x0 + 90, baseL - tmax - 14, "最遅に律速", FT, RED)
    ctext(d, x0 + 90, 90, "負荷不均衡", FS, RED)
    ctext(d, x0 + 90, 110, "赤=手待ち(遊び)", FT, RED)
    # 右：均衡
    x1 = 390
    for i in range(4):
        bx = x1 + i * 45
        box(d, bx, baseL - 122, bx + 30, baseL, (215, 245, 220), GREEN, 2)
        ctext(d, bx + 15, baseL + 12, "P%d" % (i + 1), FT, BLACK)
    ctext(d, x1 + 90, 90, "負荷均衡", FS, GREEN)
    ctext(d, x1 + 90, 110, "同時に終わる=効率↑", FT, GREEN)
    fbox(d, 330, 400, 640, 34, "粒度=並列部の分布。粗粒度=大きく固まる／細粒度=細切れ。均等分割と粒度への配慮が要る", (240, 244, 250), FT)
    save(im, "t1f7LoadBalance")


# ---- 6. メッセージパッシング(MPI) と データ並列(HPF)
def f_message_passing():
    im, d = new()
    title(d, "メッセージパッシング(MPI) と データ並列(HPF)")
    # 左：MPI
    ctext(d, 175, 70, "MPI：処理もデータも細かく指示", FT, BLUE)
    cxs = [(120, 130), (230, 130), (120, 230), (230, 230)]
    for (cx, cy) in cxs:
        box(d, cx - 35, cy - 26, cx + 35, cy + 26, (210, 224, 250), BLUE, 2)
        ctext(d, cx, cy - 8, "PE", FT, BLACK)
        ctext(d, cx, cy + 10, "データ+処理", FT, GRAY)
    arrow(d, 155, 130, 195, 130, RED, 2, 9); arrow(d, 195, 145, 155, 145, RED, 2, 9)
    arrow(d, 120, 156, 120, 204, RED, 2, 9); arrow(d, 230, 204, 230, 156, RED, 2, 9)
    ctext(d, 175, 300, "メッセージ(通信)を明示", FT, RED)
    ctext(d, 175, 322, "記述は難・可搬性は高い(C/Fortran)", FT, GRAY)
    dash(d, 330, 60, 330, 340, LGRAY, 1, 6, 5)
    # 右：HPF
    ctext(d, 495, 70, "HPF：逐次コードに指示文を挿入", FT, GREEN)
    box(d, 400, 95, 590, 250, "white", BLACK, 2)
    lines = ["do i=1,N", "  !HPF$ distribute", "    a(i)=b(i)+c(i)", "end do"]
    for i, s in enumerate(lines):
        col = GREEN if "HPF" in s else BLACK
        ctext(d, 410, 118 + i * 30, s, FT, col, "lm")
    ctext(d, 495, 275, "指示文は逐次コンパイラでは", FT, GRAY)
    ctext(d, 495, 296, "コメント扱い→逐次版と両立・簡単", FT, GREEN)
    save(im, "t1f7MessagePassing")


# ---- 7. 超線形速度向上とキャッシュ効果
def f_superlinear():
    im, d = new()
    title(d, "超線形速度向上：担当データが小さくキャッシュに収まる")
    ox, oy = 100, 340
    axes(d, ox, oy, 470, 275, "プロセッサ数 n", "速度向上 S")
    xn = lambda n: ox + (n / 16.0) * 450
    # 理想 S=n
    dash(d, ox, oy, xn(16), oy - 16 * 15, LGRAY, 2, 7, 5)
    ctext(d, xn(13), oy - 13 * 15 - 12, "理想 S=n", FT, LGRAY, "lm")
    # 実測: 低nで理想を少し上回る→高nで頭打ち・低下
    pts = []
    for n in range(1, 17):
        if n <= 4:
            S = n * 1.12
        else:
            S = 4 * 1.12 + (n - 4) * 0.55 - max(0, n - 10) * 0.9
        pts.append((xn(n), oy - S * 15))
    curve(d, pts, BLUE, 3)
    ctext(d, xn(3), oy - 3 * 1.12 * 15 - 16, "理想超え=キャッシュ効果", FT, GREEN, "lm")
    ctext(d, xn(13), oy - 5.5 * 15 + 18, "高並列で通信増→低下", FT, RED, "lm")
    fbox(d, 500, 110, 260, 46, "担当メモリが減りヒット率↑\n→ 一時的に理論値 n を超える", (240, 248, 240), FT)
    save(im, "t1f7Superlinear")


# ---- 8. ラグランジュ補間の基底関数
def f_lagrange():
    im, d = new()
    title(d, "ラグランジュ補間：基底 φk は自節点で1・他節点で0")
    ox, oy = 90, 300
    axes(d, ox, oy, 480, 220, "x", "φ")
    xs = [ox + 60, ox + 180, ox + 300, ox + 420]
    labs = ["x1", "x2", "x3", "x4"]
    one = oy - 170
    dash(d, ox, one, ox + 470, one, LGRAY, 1, 6, 5)
    ctext(d, ox - 8, one, "1", FT, GRAY, "rm")
    for xv, lb in zip(xs, labs):
        d.line((xv, oy, xv, oy + 6), fill=BLACK, width=2)
        ctext(d, xv, oy + 18, lb, FT, BLACK)
    # φ2 (x2で1, 他0) を山型で
    def bump(peak_x, col):
        pts = []
        for k in range(0, 481, 6):
            x = ox + k
            v = math.exp(-((x - peak_x) / 55.0) ** 2)
            pts.append((x, oy - v * 170))
        curve(d, pts, col, 3)
    bump(xs[1], BLUE)
    bump(xs[2], RED)
    for xv in xs:
        node(d, xv, oy, 4, BLACK, BLACK)
    node(d, xs[1], one, 5, BLUE, BLUE)
    node(d, xs[2], one, 5, RED, RED)
    ctext(d, xs[1], one - 16, "φ2", FT, BLUE)
    ctext(d, xs[2], one - 16, "φ3", FT, RED)
    fbox(d, 330, 380, 620, 34, "p(x)=Σ dk·φk(x)。各点値 dk を重み φk で足すと全データ点を通る n 次多項式", (240, 244, 250), FT)
    save(im, "t1f7Lagrange")


# ---- 9. 双1次補間・3重線形補間
def f_interpolation():
    im, d = new()
    title(d, "双1次補間(4隅) と 3重線形補間(8隅)")
    # 左：双1次(正方セル)
    x0, y0, s = 90, 120, 170
    box(d, x0, y0, x0 + s, y0 + s, "white", BLACK, 2)
    corners = [(x0, y0), (x0 + s, y0), (x0, y0 + s), (x0 + s, y0 + s)]
    for (cx, cy) in corners:
        node(d, cx, cy, 6, BLUE, BLUE)
    qx, qy = x0 + s * 0.62, y0 + s * 0.4
    dash(d, x0, qy, x0 + s, qy, LGRAY, 1, 5, 4)
    dash(d, qx, y0, qx, y0 + s, LGRAY, 1, 5, 4)
    node(d, qx, qy, 6, RED, RED)
    ctext(d, qx + 10, qy + 16, "Q", FT, RED, "lm")
    ctext(d, x0 + s / 2, y0 + s + 26, "双1次：4隅→内部点", FT, BLACK)
    # 右：3重線形(立方体アイソメ)
    bx, by, ss, dx, dy = 400, 150, 130, 55, 34
    front = [(bx, by), (bx + ss, by), (bx + ss, by + ss), (bx, by + ss)]
    back = [(px + dx, py - dy) for (px, py) in front]
    for a, b in zip(front, back):
        d.line((a[0], a[1], b[0], b[1]), fill=GRAY, width=1)
    d.polygon(front, outline=BLACK, width=2)
    d.line(back + [back[0]], fill=GRAY, width=1)
    for p in front + back:
        node(d, p[0], p[1], 5, BLUE, BLUE)
    cx = bx + ss * 0.5 + dx * 0.4; cy = by + ss * 0.5 - dy * 0.3
    node(d, cx, cy, 6, RED, RED)
    ctext(d, bx + ss / 2, by + ss + 34, "3重線形：8隅→内部点", FT, BLACK)
    note(d, "低次で安定・格子データからの取り出しに向く（可視化やデータ受け渡しで多用）")
    save(im, "t1f7Interpolation")


# ---- 10. ルンゲの現象
def f_runge():
    im, d = new()
    title(d, "ルンゲの現象：高次多項式は端で激しく振動")
    ox, oy = 90, 250
    axes(d, ox, oy, 480, 190, "x", "y")
    mid = oy - 120
    # 真の関数(ベル型)を青
    def fx(x):  # x in [-1,1] -> screen
        return 1.0 / (1 + 25 * x * x)
    tp = []
    for k in range(0, 481, 4):
        xr = -1 + 2 * k / 480.0
        tp.append((ox + k, oy - fx(xr) * 150))
    curve(d, tp, BLUE, 3)
    ctext(d, ox + 240, oy - 150 - 14, "真の関数", FT, BLUE)
    # 高次補間(端で振動)を赤: 中央は一致、端で大きく振れる
    rp = []
    for k in range(0, 481, 4):
        xr = -1 + 2 * k / 480.0
        base = fx(xr)
        osc = 0.5 * (xr ** 8) * math.sin(9 * xr)  # 端ほど大
        rp.append((ox + k, oy - (base + osc) * 150))
    curve(d, rp, RED, 2)
    # 等間隔ノード
    for j in range(9):
        xr = -1 + 2 * j / 8.0
        node(d, ox + (xr + 1) / 2 * 480, oy - fx(xr) * 150, 4, RED, RED)
    ctext(d, ox + 40, oy - 40, "端で振動", FT, RED, "lm")
    ctext(d, ox + 440, oy - 40, "端で振動", FT, RED, "rm")
    fbox(d, 330, 350, 620, 40, "対策：実務は線形/スプライン補間・最小二乗の併用、勾配値も使えば少ない点で滑らか", (240, 244, 250), FT)
    save(im, "t1f7Runge")


# ---- 11. レンダリングのパイプラインと陰面消去
def f_rendering():
    im, d = new()
    title(d, "レンダリングの流れと陰面消去(Zバッファ)")
    steps = ["形状\nモデリング", "座標\n変換", "陰面\n消去", "シェー\nディング"]
    x = 70
    for i, s in enumerate(steps):
        cx = x + i * 150
        fbox(d, cx, 130, 120, 60, s, (235, 240, 250), FT)
        if i < 3:
            arrow(d, cx + 60, 130, cx + 90, 130, BLACK, 3, 12)
    # 下段：Zバッファ=奥行き比較で手前を残す
    eye = (90, 300)
    node(d, eye[0], eye[1], 6, BLACK, BLACK); ctext(d, 90, 328, "視点", FT, BLACK)
    box(d, 250, 250, 300, 340, (210, 224, 250), BLUE, 2)   # 手前(近)
    box(d, 330, 235, 380, 355, (235, 235, 235), GRAY, 2)   # 奥(遠)
    ctext(d, 275, 360, "手前(近)", FT, BLUE)
    ctext(d, 355, 372, "奥(遠・隠れる)", FT, GRAY)
    arrow(d, eye[0] + 10, eye[1], 248, 295, BLACK, 2, 10)
    ctext(d, 500, 250, "奥行き(Z)を比べ\n手前の面だけ残す\n=見えない面を消す", FT, BLACK)
    ctext(d, 500, 320, "代表:Zバッファ法・\n奥行きソート・レイトレース", FT, GRAY)
    save(im, "t1f7Rendering")


# ---- 12. ボリュームレンダリングと伝達関数
def f_volume_rendering():
    im, d = new()
    title(d, "ボリュームレンダリング：伝達関数(値→色・不透明度)")
    ox, oy = 90, 250
    axes(d, ox, oy, 300, 170, "スカラ値", "不透明度")
    # 不透明度カーブ
    pts = []
    for k in range(0, 301, 5):
        v = math.exp(-((k - 180) / 45.0) ** 2)
        pts.append((ox + k, oy - v * 140))
    curve(d, pts, RED, 3)
    ctext(d, ox + 180, oy - 155, "不透明度(Opacity)", FT, RED)
    # カラーマップ帯
    cols = [(40, 80, 190), (30, 150, 60), (210, 190, 20), (210, 130, 20), (200, 40, 40)]
    for i, c in enumerate(cols):
        box(d, ox + i * 60, oy + 20, ox + (i + 1) * 60, oy + 44, c, c, 1)
    ctext(d, ox + 150, oy + 60, "カラーマップ(値→色)", FT, BLACK)
    # 右：もや状のボリューム
    for (cx, cy, r) in [(500, 150, 60), (540, 190, 45), (470, 200, 40)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=LGRAY, width=1)
    swirl(d, 510, 175, 22, True, GRAY, 1)
    ctext(d, 510, 250, "境界のない\n濃度分布を描く", FT, GRAY)
    fbox(d, 330, 385, 620, 34, "伝達関数=カラーマップ+不透明度。設定は試行錯誤・定量評価には不向き", (240, 244, 250), FT)
    save(im, "t1f7VolumeRendering")


# ---- 13. レイキャスティング
def f_ray_casting():
    im, d = new()
    title(d, "レイキャスティング：視線に沿って値をサンプリングし積分")
    eye = (70, 210)
    node(d, eye[0], eye[1], 7, BLACK, BLACK); ctext(d, 70, 236, "視点", FT, BLACK)
    # スクリーン(画素列)
    sx = 160
    d.line((sx, 120, sx, 300), fill=BLUE, width=3)
    for yy in range(130, 301, 20):
        d.line((sx - 5, yy, sx + 5, yy), fill=BLUE, width=1)
    ctext(d, sx, 108, "スクリーン(画素)", FT, BLUE)
    # ボリューム
    box(d, 300, 110, 560, 310, "white", GRAY, 2)
    ctext(d, 430, 96, "ボリューム", FT, GRAY)
    # 視線(1本)＋サンプル点
    py = 205
    arrow(d, eye[0] + 12, eye[1], 590, py - 2, RED, 2, 12)
    for x in range(310, 561, 30):
        node(d, x, py - (x - 310) * 0.02, 5, (255, 225, 225), RED)
    ctext(d, 430, py + 40, "一定間隔でサンプリング→積分", FT, RED)
    ctext(d, 200, py - 20, "画素", FT, RED)
    fbox(d, 330, 375, 620, 40, "積分時に不透明度も考慮→半透明画像。テクスチャ方式ならGPUで高速化", (240, 244, 250), FT)
    save(im, "t1f7RayCasting")


# ---- 14. LIC(線積分畳み込み)
def f_lic():
    im, d = new()
    title(d, "LIC：ノイズを流れ方向に畳み込みベクトル場を可視化")
    # 左：ベクトル場+ノイズ
    box(d, 70, 90, 300, 320, "white", GRAY, 1)
    import random
    random.seed(3)
    for _ in range(60):
        rx = random.randint(78, 292); ry = random.randint(98, 312)
        g = random.randint(150, 210)
        d.point((rx, ry), fill=(g, g, g))
        d.rectangle((rx, ry, rx + 1, ry + 1), fill=(g, g, g))
    for gx in range(100, 291, 55):
        for gy in range(120, 311, 55):
            ang = math.radians(-25 + (gy - 120) * 0.15)
            arrow(d, gx, gy, gx + 26 * math.cos(ang), gy + 26 * math.sin(ang), BLUE, 1, 6)
    ctext(d, 185, 340, "乱数ノイズ + ベクトル場", FT, BLACK)
    arrow(d, 310, 200, 360, 200, BLACK, 3, 13)
    ctext(d, 335, 178, "畳み込み", FT, GRAY)
    # 右：流れの筋
    box(d, 375, 90, 600, 320, "white", GRAY, 1)
    for gy in range(105, 316, 16):
        pts = []
        for k in range(0, 226, 8):
            x = 375 + k
            ang = -0.4 + (gy - 105) * 0.006
            y = gy + 18 * math.sin((k) * 0.02 + gy * 0.03)
            pts.append((x, y))
        curve(d, pts, GRAY, 1)
    ctext(d, 487, 340, "流れの筋模様(全体像)", FT, BLACK)
    note(d, "初期輝度は乱数(スポットノイズ)でよい。矢印より重なりが少なく全体像が分かる")
    save(im, "t1f7LIC")


# ---- 15. 立体視ディスプレイ
def f_stereo():
    im, d = new()
    title(d, "立体視：左右2枚の画像を左右の目に分けて見せる")
    # 頭と両眼
    d.ellipse((70, 170, 130, 230), outline=BLACK, width=2)
    node(d, 88, 195, 5, "white", BLACK); node(d, 112, 195, 5, "white", BLACK)
    ctext(d, 100, 250, "左目 / 右目", FT, BLACK)
    # 左目画像・右目画像(視差で物体位置がずれる)
    box(d, 200, 110, 320, 200, "white", BLUE, 2)
    node(d, 250, 155, 10, (210, 224, 250), BLUE); ctext(d, 260, 92, "左目用", FT, BLUE)
    box(d, 200, 220, 320, 310, "white", RED, 2)
    node(d, 272, 265, 10, (255, 225, 225), RED); ctext(d, 260, 328, "右目用(視差でずれ)", FT, RED)
    arrow(d, 132, 190, 198, 155, BLUE, 1, 8)
    arrow(d, 132, 205, 198, 265, RED, 1, 8)
    # 方式
    fbox(d, 480, 150, 300, 46, "パッシブ：偏光/カラーフィルタ眼鏡", (235, 240, 250), FT, BLUE)
    fbox(d, 480, 210, 300, 46, "アクティブ：時分割シャッタ眼鏡", (255, 244, 232), FT, ORANGE)
    fbox(d, 480, 270, 300, 46, "裸眼：バリア/レンチキュラ", (240, 248, 240), FT, GREEN)
    note(d, "VR=センシング+シミュレーション+ディスプレイ。左右画像の生成が基本")
    save(im, "t1f7Stereo")


# ---- 16. MR/AR/AV
def f_mrar():
    im, d = new()
    title(d, "MR・AR・AV：現実と仮想の融合の段階")
    y = 150
    # 連続線
    arrow(d, 70, y, 600, y, BLACK, 2, 12)
    ctext(d, 70, y + 24, "現実空間", FT, BLUE, "lm")
    ctext(d, 595, y + 24, "仮想空間", FT, GREEN, "rm")
    # AR
    ctext(d, 200, y - 40, "AR", FS, ORANGE)
    d.line((200, y - 26, 200, y), fill=ORANGE, width=2)
    ctext(d, 200, y - 62, "現実に仮想を足す", FT, ORANGE)
    # AV
    ctext(d, 470, y - 40, "AV", FS, ORANGE)
    d.line((470, y - 26, 470, y), fill=ORANGE, width=2)
    ctext(d, 470, y - 62, "仮想に現実を足す", FT, ORANGE)
    # MR = 全体の総称
    d.line((150, y + 60, 520, y + 60), fill=GRAY, width=1)
    d.line((150, y + 55, 150, y + 65), fill=GRAY, width=1)
    d.line((520, y + 55, 520, y + 65), fill=GRAY, width=1)
    ctext(d, 335, y + 80, "MR(複合現実感)=両方向を含む融合の総称", FT, GRAY)
    # 例示イラスト
    box(d, 130, 250, 300, 360, "white", BLUE, 2)
    ctext(d, 215, 240, "AR 例", FT, ORANGE)
    d.rectangle((160, 300, 210, 350), outline=BLUE, width=2)
    arrow(d, 240, 340, 240, 300, GREEN, 2, 10); ctext(d, 240, 290, "仮想ナビ", FT, GREEN)
    box(d, 360, 250, 530, 360, (240, 248, 240), GREEN, 2)
    ctext(d, 445, 240, "AV 例", FT, ORANGE)
    swirl(d, 445, 305, 26, True, GREEN, 1)
    d.rectangle((420, 320, 470, 350), outline=BLUE, width=2); ctext(d, 445, 372, "現実映像を取り込む", FT, BLUE)
    save(im, "t1f7MRAR")


# ---- 17. GPGPU / SIMD
def f_gpgpu():
    im, d = new()
    title(d, "GPGPU/SIMD：多数コアが同一命令で並列処理")
    # 命令
    fbox(d, 150, 110, 180, 50, "同一命令\n(1つ)", (235, 240, 250), FT, BLUE)
    # 多数コア格子
    ox, oy = 320, 90
    for r in range(4):
        for c in range(6):
            cx = ox + c * 48; cy = oy + r * 48
            box(d, cx, cy, cx + 36, cy + 36, (215, 245, 220), GREEN, 2)
    ctext(d, ox + 3 * 48, oy + 4 * 48 + 6, "多数のコア(高い並列度)", FT, GREEN)
    for r in range(4):
        arrow(d, 240, 135 + r * 20, 315, oy + r * 48 + 18, BLUE, 1, 8)
    # データストリーム
    ctext(d, 150, 200, "大量の\n単純データ", FT, BLACK)
    for k in range(5):
        node(d, 120 + k * 15, 250, 5, FILL2, GRAY)
    arrow(d, 200, 250, 300, 250, BLACK, 2, 10)
    fbox(d, 330, 360, 640, 40, "一様な計算(行列演算)は速い／条件分岐(if)が多いと不得手。開発=CUDA・OpenCL", (240, 244, 250), FT)
    save(im, "t1f7GPGPU")


# ---- 18. 性能チューニングの流れ
def f_tuning():
    im, d = new()
    title(d, "性能チューニング：測って直すサイクルを回す")
    steps = [("① ベンチマーク\n設定", 180, 130, (235, 240, 250)),
             ("② ホットスポット\n特定(測定)", 480, 130, (255, 244, 232)),
             ("③ 実装を修正", 480, 290, (240, 248, 240)),
             ("④ 再測定で\n効果確認", 180, 290, (235, 240, 250))]
    for (s, cx, cy, fill) in steps:
        fbox(d, cx, cy, 190, 66, s, fill, FT)
    arrow(d, 275, 130, 385, 130, BLACK, 3, 12)   # 1->2
    arrow(d, 480, 163, 480, 257, BLACK, 3, 12)   # 2->3
    arrow(d, 385, 290, 275, 290, BLACK, 3, 12)   # 3->4
    arrow(d, 180, 257, 180, 163, BLACK, 3, 12)   # 4->1(繰り返す)
    ctext(d, 330, 210, "まず『どこが遅いか』を\n測ってから直す", FT, GRAY)
    note(d, "原因=メモリアクセス・アルゴリズム・分岐・入出力・キャッシュミス等。並列は通信減+負荷均一")
    save(im, "t1f7Tuning")


if __name__ == "__main__":
    f_speedup(); f_amdahl(); f_efficiency(); f_comm_overhead(); f_load_balance()
    f_message_passing(); f_superlinear(); f_lagrange(); f_interpolation(); f_runge()
    f_rendering(); f_volume_rendering(); f_ray_casting(); f_lic(); f_stereo()
    f_mrar(); f_gpgpu(); f_tuning()
    print("done t1f7 (18)")
