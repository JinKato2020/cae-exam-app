# -*- coding: utf-8 -*-
"""熱流体力学1級 第6章「設計応用」問題図 12枚。figlibで白地660x420線画。
required(回答前)の t1e6PumpImpeller / t1e6Diffuser / t1e6KarmanVortex / t1e6SumpPump は
正解・結論(Cp値・放出周波数・評価手順など)を一切描かず、部品配置・流路・設定のみを中立に示す。"""
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
    """回転を表す3/4円弧＋矢じり。cw=時計回り。"""
    a0, a1 = 20, 300
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    end = math.radians(a1 if cw else a0)
    ex, ey = cx + r * math.cos(end), cy + r * math.sin(end)
    t = end + (math.pi / 2 if cw else -math.pi / 2)
    for s in (0.6, -0.6):
        d.line((ex, ey, ex - 10 * math.cos(t - s), ey - 10 * math.sin(t - s)), fill=col, width=wd)


def wavy(d, x1, y1, x2, y2, col=ORANGE, wd=2, amp=5, n=6):
    """放射(輻射)を表す波線矢印。"""
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    px, py = -uy, ux
    pts = []
    for i in range(n * 2 + 1):
        t = i / (n * 2)
        s = amp * math.sin(i * math.pi / 2)
        pts.append((x1 + ux * L * t + px * s, y1 + uy * L * t + py * s))
    d.line(pts, fill=col, width=wd, joint="curve")
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (0.5, -0.5):
        d.line((x2, y2, x2 - 11 * math.cos(ang - s), y2 - 11 * math.sin(ang - s)), fill=col, width=wd)


# ============================================================ 6-1 数値最適化(helpful)
def f_optimization():
    im, d = new()
    title(d, "数値最適化の枠組み：トレードオフ と 反復ループ")
    # 左：多目的トレードオフ曲線
    ox, oy = 70, 320
    axes(d, ox, oy, 200, 200, "目的1", "目的2")
    # パレート的フロンティア(凸な減少曲線)
    fr = [(ox + 20, oy - 170), (ox + 45, oy - 120), (ox + 85, oy - 80),
          (ox + 135, oy - 55), (ox + 185, oy - 40)]
    curve(d, fr, BLUE, 3)
    for p in fr:
        node(d, p[0], p[1], 5, BLUE, BLUE)
    ctext(d, ox + 120, oy - 130, "妥協解の並び", FT, BLUE)
    # 劣った点(灰・右上=両目的とも悪い)
    for px, py in [(ox + 110, oy - 120), (ox + 150, oy - 95), (ox + 90, oy - 140)]:
        node(d, px, py, 4, GRAY, GRAY)
    ctext(d, ox + 100, oy + 26, "トレードオフ(競合)関係", FT, BLACK)
    # 右：反復ループ(実験計画法→CFD→応答曲面→GA探索)
    steps = ["実験計画法で\nサンプル点選定", "CFDで評価", "応答曲面を作成", "GAで探索・更新"]
    cx = 500
    ys = [98, 168, 238, 308]
    for i, (s, y) in enumerate(zip(steps, ys)):
        fbox(d, cx, y, 190, 52, s, (240, 244, 250), FT)
        if i < 3:
            arrow(d, cx, y + 26, cx, ys[i + 1] - 26, BLACK, 2, 11)
    # 反復の戻り矢印
    d.line((cx + 95, 308, cx + 130, 308), fill=GRAY, width=2)
    d.line((cx + 130, 308, cx + 130, 98), fill=GRAY, width=2)
    arrow(d, cx + 130, 98, cx + 95, 98, GRAY, 2, 11)
    ctext(d, cx + 145, 203, "反復", FT, GRAY, "lm")
    note(d, "競合する目的の妥協解を、応答曲面で評価を軽くしながら反復探索する")
    save(im, "t1e6Optimization")


# ============================================================ 6-2 遠心ポンプ子午面(required)
def f_pump_impeller():
    im, d = new()
    title(d, "遠心ポンプの子午面断面：部品配置と流路")
    cl = 372  # 中心線
    dash(d, 60, cl, 610, cl, GRAY, 2, 10, 6)
    ctext(d, 600, cl + 14, "軸中心", FT, GRAY)
    # 吸込み(左からの軸流)
    d.line((60, 300, 200, 300), fill=BLACK, width=2)    # ケーシング内壁(上)
    d.line((60, 350, 175, 350), fill=BLACK, width=2)    # 内壁(下)
    arrow(d, 75, 325, 150, 325, BLUE, 3, 12)
    ctext(d, 95, 306, "吸込み", FT, BLUE)
    # 予旋回止め
    for xx in (150, 158):
        d.line((xx, 305, xx, 345), fill=GREEN, width=2)
    ctext(d, 154, 366, "予旋回止め", FT, GREEN)
    # 羽根車流路(シュラウド=上, ハブ=下)：軸流→半径流へ転向
    shroud = [(200, 300), (215, 270), (235, 220), (255, 175), (290, 150)]
    hub = [(175, 350), (215, 340), (255, 300), (285, 240), (305, 160)]
    curve(d, shroud, BLACK, 3)
    curve(d, hub, BLACK, 3)
    # 羽根(流路を横切る線)
    for a, b in [(shroud[1], hub[1]), (shroud[2], hub[2]), (shroud[3], hub[3])]:
        d.line((a[0], a[1], b[0], b[1]), fill=LGRAY, width=2)
    ctext(d, 250, 250, "羽根車", FS, BLACK)
    # 主流線(吸込み→羽根車→出口)
    ml = [(120, 330), (180, 322), (220, 300), (250, 250), (280, 190), (300, 158)]
    curve(d, ml, RED, 2)
    arrow(d, 293, 172, 300, 156, RED, 2, 11)
    ctext(d, 330, 250, "主流", FT, RED, "lm")
    # ライナーリング(入口シール隙間・漏れ経路)
    d.line((200, 296, 235, 296), fill=ORANGE, width=2)
    dash(d, 205, 292, 232, 292, ORANGE, 2, 5, 4)
    ctext(d, 150, 285, "ライナーリング", FT, ORANGE, "lm")
    arrow(d, 200, 285, 215, 293, ORANGE, 1, 8)
    # バランスホール(羽根車後円板の穴)
    d.line((320, 200, 320, 300), fill=BLACK, width=2)   # 後円板
    d.ellipse((315, 245, 325, 265), outline=ORANGE, width=2)
    ctext(d, 340, 300, "バランスホール", FT, ORANGE, "lm")
    arrow(d, 400, 292, 322, 258, ORANGE, 1, 8)
    # ディフューザ翼(羽根車出口の外側・上方)
    for i, xx in enumerate((300, 345, 390, 435)):
        d.line((xx, 60, xx + 18, 130), fill=BLUE, width=3)
    ctext(d, 400, 50, "ディフューザ翼", FS, BLUE)
    # ケーシング外郭
    caseo = [(200, 300), (200, 130), (300, 60), (470, 90), (500, 200), (470, 370)]
    curve(d, caseo, GRAY, 2)
    ctext(d, 520, 160, "ケーシング", FT, GRAY, "lm")
    note(d, "各部品の配置と流路のみを示す（部分流量での逆流・渦は描かない）")
    save(im, "t1e6PumpImpeller")


# ============================================================ 6-3 ディフューザ(required)
def f_diffuser():
    im, d = new()
    title(d, "ディフューザ(拡大流路)：入口A1・U1 → 出口A2・U2")
    # 壁(入口は狭く・出口は広い)
    x0, x1 = 150, 540
    d.line((x0, 175, x1, 110), fill=BLACK, width=3)   # 上壁
    d.line((x0, 245, x1, 310), fill=BLACK, width=3)   # 下壁
    d.line((x0, 175, x0, 245), fill=BLACK, width=2)   # 入口面
    d.line((x1, 110, x1, 310), fill=BLACK, width=2)   # 出口面
    # 入口の速い流れ(短く密な矢印)
    for yy in (195, 210, 225):
        arrow(d, x0 + 8, yy, x0 + 55, yy, BLUE, 2, 9)
    ctext(d, x0 - 6, 210, "U1(速い)", FT, BLUE, "rm")
    # 中間〜出口へ向かって太くなる矢印(減速)
    arrow(d, 300, 210, 355, 210, BLUE, 4, 14)
    arrow(d, 420, 210, 460, 210, BLUE, 7, 18)
    ctext(d, x1 + 8, 210, "U2(遅い)", FT, BLUE, "lm")
    ctext(d, 345, 240, "減速＝動圧を静圧へ", FT, GRAY)
    # 面積の寸法(A1, A2)
    dim(d, x0 - 26, 175, x0 - 26, 245, "A1", col=GRAY)
    dim(d, x1 + 26, 110, x1 + 26, 310, "A2", col=GRAY)
    ctext(d, 345, 355, "面積比 AR = A2 / A1", FS, BLACK)
    note(d, "流路が広がり流れが減速する設定のみ（静圧回復係数の値は描かない）")
    save(im, "t1e6Diffuser")


# ============================================================ 6-4 ブラフ体 vs 流線形(helpful)
def f_bluff_streamline():
    im, d = new()
    title(d, "角張ったビル(形状抗力) と 航空機翼(摩擦抗力)")
    # 左：ビル(ブラフ体)
    for yy in (150, 180, 210):
        arrow(d, 40, yy, 95, yy, BLUE, 2, 10)
    box(d, 110, 120, 175, 320, (238, 240, 245))
    ctext(d, 142, 335, "角張ったビル", FS, BLACK)
    # 角ではく離
    d.line((110, 120, 130, 100), fill=RED, width=2)
    ctext(d, 150, 92, "角で剥離", FT, RED)
    # 大規模後流(渦)
    swirl(d, 205, 175, 22, True, RED, 2)
    swirl(d, 210, 260, 22, False, RED, 2)
    ctext(d, 255, 300, "大規模後流", FT, RED, "lm")
    ctext(d, 142, 220, "＋", F, BLACK)          # 前面高圧
    ctext(d, 200, 218, "−", F, BLACK)           # 背面低圧
    ctext(d, 142, 108, "形状(圧力)抗力支配", FT, RED)
    # 右：航空機翼(流線形)
    for yy in (150, 180, 210):
        arrow(d, 360, yy, 405, yy, BLUE, 2, 10)
    af = [(420, 200), (470, 178), (540, 182), (600, 200), (540, 210), (470, 208), (420, 200)]
    curve(d, af, BLACK, 3)
    ctext(d, 510, 250, "航空機翼(流線形)", FS, BLACK)
    # 薄く付着した境界層
    dash(d, 430, 190, 590, 192, GREEN, 2, 6, 4)
    dash(d, 430, 208, 590, 208, GREEN, 2, 6, 4)
    ctext(d, 510, 168, "境界層が薄く付着", FT, GREEN)
    ctext(d, 510, 285, "摩擦抗力(粘性)支配", FT, GREEN)
    note(d, "はく離の有無で抵抗の内訳（形状抗力/摩擦抗力）と境界層予測の重要度が変わる")
    save(im, "t1e6BluffVsStreamline")


# ============================================================ 6-5 室内気流と排気口(helpful)
def f_room_airflow():
    im, d = new()
    title(d, "室内気流：排気口周辺で数値不安定が起こりやすい")
    # 部屋
    box(d, 90, 80, 580, 350, "white")
    # 給気口(天井左)
    box(d, 120, 78, 175, 90, (235, 240, 250))
    ctext(d, 147, 66, "給気口", FT, BLUE)
    arrow(d, 150, 92, 200, 140, BLUE, 3, 12)
    # 大きな循環流
    for (cx, cy, cw) in [(335, 215, True)]:
        d.arc((cx - 150, cy - 100, cx + 150, cy + 100), 0, 360, fill=GRAY, width=1)
    arrow(d, 470, 130, 470, 180, GRAY, 2, 11)
    arrow(d, 200, 300, 200, 250, GRAY, 2, 11)
    ctext(d, 335, 215, "室内循環流", FT, GRAY)
    # 排気口(下部右)
    box(d, 500, 348, 555, 352, (250, 235, 235))
    arrow(d, 527, 330, 527, 360, RED, 3, 12)
    ctext(d, 527, 366, "排気口", FT, RED)
    # 不安定領域の強調
    dash(d, 470, 300, 470, 360, RED, 1, 4, 4)
    d.ellipse((480, 300, 575, 360), outline=RED, width=2)
    ctext(d, 527, 292, "数値不安定", FT, RED)
    fbox(d, 300, 388, 560, 30, "対策：排気口近傍に数値粘性 / 外部に圧力損失部(急拡大・管路)を付加", (255, 236, 236), FT, RED)
    save(im, "t1e6RoomAirflow")


# ============================================================ 6-6 オフィス熱環境(helpful)
def f_office_thermal():
    im, d = new()
    title(d, "オフィス熱環境：熱源・吸熱源 と 対流・放射・伝導")
    box(d, 80, 80, 590, 340, "white")
    # 窓+日射(左壁)
    d.rectangle((80, 130, 92, 240), outline=BLUE, width=2)
    for yy in (150, 180, 210):
        arrow(d, 92, yy, 150, yy + 20, ORANGE, 2, 10)
    ctext(d, 120, 120, "窓・日射(熱源)", FT, ORANGE, "lm")
    # 照明(天井)
    box(d, 300, 82, 360, 96, (255, 250, 220))
    ctext(d, 330, 106, "照明(熱源)", FT, ORANGE)
    wavy(d, 330, 100, 330, 150, ORANGE, 2, 4, 5)
    # 冷房(吸熱・天井右)
    box(d, 470, 82, 530, 96, (225, 235, 250))
    ctext(d, 500, 70, "冷房(吸熱源)", FT, BLUE)
    for xx in (485, 500, 515):
        arrow(d, xx, 96, xx - 10, 150, BLUE, 2, 9)
    # 人体(熱源)
    px, py = 250, 300
    d.ellipse((px - 8, py - 60, px + 8, py - 44), outline=BLACK, width=2)  # 頭
    d.line((px, py - 44, px, py - 10), fill=BLACK, width=3)               # 胴
    d.line((px, py - 10, px - 12, py + 20), fill=BLACK, width=2)
    d.line((px, py - 10, px + 12, py + 20), fill=BLACK, width=2)
    ctext(d, px, py + 34, "人体(熱源)", FT, BLACK)
    wavy(d, px + 10, py - 40, px + 70, py - 60, ORANGE, 2, 4, 5)   # 放射
    ctext(d, px + 78, py - 62, "放射(輻射)", FT, ORANGE, "lm")
    # 対流(気流)
    arrow(d, 400, 280, 400, 200, BLUE, 2, 10)
    ctext(d, 400, 300, "対流(気流)", FT, BLUE)
    # 伝導(壁・床へ)
    arrow(d, 300, 338, 300, 360, GRAY, 2, 9)
    ctext(d, 360, 356, "伝導(壁・床)", FT, GRAY, "lm")
    note(d, "熱源=日射・照明・人体／吸熱源=冷房。輸送は対流＋放射＋伝導の3つ")
    save(im, "t1e6OfficeThermal")


# ============================================================ 6-7 自動車空力(helpful)
def f_car_aero():
    im, d = new()
    title(d, "1BOX自動車の空力：圧力抗力を決める流れ")
    # 地面
    hwall(d, 40, 620, 350, side=1, n=18)
    # 車体(矩形に近い1BOX側面)
    body = [(140, 320), (150, 210), (200, 160), (470, 155), (490, 320)]
    curve(d, body, BLACK, 3)
    d.line((140, 320, 490, 320), fill=BLACK, width=2)
    # タイヤ(回転)
    for tx in (210, 430):
        d.ellipse((tx - 24, 320 - 24, tx + 24, 320 + 24), outline=BLACK, width=3)
        swirl(d, tx, 320, 14, True, GREEN, 2)
    ctext(d, 320, 300, "回転するタイヤ", FT, GREEN)
    # 流入
    for yy in (180, 230, 280):
        arrow(d, 45, yy, 110, yy, BLUE, 2, 10)
    # 前縁剥離＋再付着
    d.line((150, 210), fill=RED)
    swirl(d, 175, 180, 12, True, RED, 2)
    ctext(d, 175, 150, "前縁剥離→再付着", FT, RED)
    # 上面後方の剥離
    swirl(d, 455, 175, 12, True, RED, 2)
    ctext(d, 450, 128, "上面後方の剥離", FT, RED)
    # 背面の大きな後流＋カルマン渦
    swirl(d, 540, 210, 22, False, RED, 2)
    swirl(d, 555, 280, 22, True, RED, 2)
    ctext(d, 555, 155, "背面の後流(背面圧)", FT, RED)
    ctext(d, 560, 320, "カルマン渦", FT, RED)
    # 床下流れ
    arrow(d, 250, 335, 470, 335, BLUE, 2, 10)
    ctext(d, 350, 348, "床下流れ", FT, BLUE)
    note(d, "ブラフ体は圧力抗力が主。剥離・再付着・背面圧・後流変動＋床下/タイヤを考慮")
    save(im, "t1e6CarAero")


# ============================================================ 6-8 カルマン渦(required)
def f_karman_vortex():
    im, d = new()
    title(d, "円柱(電線)まわりのカルマン渦：一様流U・直径D")
    # 一様流
    for yy in (150, 190, 230, 270):
        arrow(d, 40, yy, 120, yy, BLUE, 2, 11)
    ctext(d, 70, 128, "一様流 U", FS, BLUE)
    # 円柱
    ccx, ccy, r = 175, 210, 30
    d.ellipse((ccx - r, ccy - r, ccx + r, ccy + r), outline=BLACK, width=3, fill=FILL1)
    dim(d, ccx - r, ccy + r + 26, ccx + r, ccy + r + 26, "D", col=GRAY)
    ctext(d, ccx, ccy - r - 16, "円柱(電線断面)", FT, BLACK)
    # 交互のカルマン渦列(上下で回転向きを変えた渦を千鳥に)
    xs = [260, 330, 400, 470, 540]
    for i, x in enumerate(xs):
        up = (i % 2 == 0)
        cy = ccy - 45 if up else ccy + 45
        swirl(d, x, cy, 18, cw=up, col=RED, wd=2)
    ctext(d, 400, 320, "交互に放出される渦列", FT, RED)
    note(d, "円柱と背後の渦列の配置のみ（放出周波数の値・答えは描かない）")
    save(im, "t1e6KarmanVortex")


# ============================================================ 6-9 螺旋ストレーク(helpful)
def f_helical_strake():
    im, d = new()
    title(d, "ロッドアンテナ：裸の丸棒 と 螺旋紐(ストレーク)")
    # 左：裸の丸棒
    x0 = 150
    d.line((x0, 90, x0, 350), fill=BLACK, width=8)
    ctext(d, x0, 372, "裸の丸棒", FS, BLACK)
    for i, yy in enumerate((140, 200, 260)):
        up = (i % 2 == 0)
        cx = x0 + 40 if up else x0 - 40
        swirl(d, cx, yy, 16, cw=up, col=RED, wd=2)
    ctext(d, x0, 116, "規則的なカルマン渦", FT, RED)
    ctext(d, x0, 320, "→ピーク音・加振", FT, RED)
    # 右：螺旋紐
    x1 = 470
    d.line((x1, 90, x1, 350), fill=BLACK, width=8)
    # 螺旋(斜めに巻く紐)
    for k in range(9):
        yy = 100 + k * 28
        d.line((x1 - 12, yy, x1 + 12, yy + 14), fill=GREEN, width=2)
    ctext(d, x1, 372, "螺旋紐を巻いた棒", FS, BLACK)
    # 渦放出を軸方向にずらす=不規則
    for yy, off in [(150, 34), (190, -30), (240, 30), (280, -34)]:
        swirl(d, x1 + off, yy, 11, cw=(off > 0), col=ORANGE, wd=2)
    ctext(d, x1, 116, "渦放出を軸方向にずらす", FT, ORANGE)
    ctext(d, x1, 320, "→騒音・加振を低減", FT, ORANGE)
    fbox(d, 330, 396, 470, 28, "副作用：表面突起により空気抵抗は増える", (255, 244, 232), FT, GRAY)
    save(im, "t1e6HelicalStrake")


# ============================================================ 6-10 解析の3視点(helpful)
def f_analysis_framework():
    im, d = new()
    title(d, "流体解析を進める3つの視点")
    ys = 170
    fbox(d, 130, ys, 200, 70, "(1)\n解析の対象と目的", (235, 240, 250), FS)
    fbox(d, 355, ys, 210, 90, "(2) 数値解析技術\n手法・乱流モデル\nメッシュ・境界条件\nポスト処理", (240, 248, 240), FT)
    fbox(d, 575, ys, 150, 90, "(3) 物理現象の評価\n剥離・二次流れ\n渦構造・非定常性", (255, 244, 232), FT)
    arrow(d, 230, ys, 250, ys, BLACK, 3, 13)
    arrow(d, 460, ys, 500, ys, BLACK, 3, 13)
    # 実験との比較→前段へ戻す
    fbox(d, 355, 320, 260, 46, "実験との比較・妥当性の考察", (245, 245, 245), FT)
    arrow(d, 575, 218, 575, 297, GRAY, 2, 11)          # (3)→比較
    d.line((225, 297, 225, 240), fill=GRAY, width=2)
    arrow(d, 225, 240, 225, 210, GRAY, 2, 11)          # 比較→(1)側へ戻す
    d.line((225, 297, 355, 297), fill=GRAY, width=2)
    ctext(d, 200, 268, "見直し", FT, GRAY, "rm")
    note(d, "オペレータに終わらず、対象に即したモデル化と結果の考察を行う枠組み")
    save(im, "t1e6AnalysisFramework")


# ============================================================ 6-11 ポンプ吸込み水槽(required)
def f_sump_pump():
    im, d = new()
    title(d, "ポンプ吸込み水槽：系統断面と各部の配置")
    # 水槽
    d.line((80, 130, 80, 360), fill=BLACK, width=3)     # 左壁
    d.line((520, 130, 520, 360), fill=BLACK, width=3)   # 右壁
    d.line((80, 360, 520, 360), fill=BLACK, width=3)    # 床
    # 自由表面(水面)
    wy = 160
    yy = wy
    pts = [(80 + i * 8, wy + 4 * math.sin(i * 0.6)) for i in range(56)]
    d.line(pts, fill=BLUE, width=2)
    ctext(d, 150, wy - 16, "自由表面(水面)", FT, BLUE, "lm")
    ctext(d, 470, 200, "水槽", FT, GRAY)
    # ベルマウス(漏斗)＋取水管
    bx = 300
    d.line((bx - 55, 360, bx - 20, 320), fill=BLACK, width=3)  # 漏斗左
    d.line((bx + 55, 360, bx + 20, 320), fill=BLACK, width=3)  # 漏斗右
    d.line((bx - 20, 320, bx - 20, 90), fill=BLACK, width=3)   # 取水管左
    d.line((bx + 20, 320, bx + 20, 90), fill=BLACK, width=3)   # 取水管右
    ctext(d, bx + 70, 335, "ベルマウス", FT, BLACK, "lm")
    ctext(d, bx + 30, 250, "取水管", FT, BLACK, "lm")
    ctext(d, bx, 74, "ポンプ入口へ", FT, BLUE)
    arrow(d, bx, 120, bx, 92, BLUE, 3, 12)
    # 取水の流れ(床から漏斗へ集まる)
    for sx in (150, 200, 450, 400):
        arrow(d, sx, 340, bx + (18 if sx > bx else -18), 335, GRAY, 2, 9)
    arrow(d, bx, 315, bx, 240, BLUE, 3, 12)
    # 検討対象の渦(控えめ)
    swirl(d, 220, 300, 16, True, ORANGE, 1)
    ctext(d, 200, 290, "水中渦", FT, ORANGE, "rm")
    swirl(d, 360, 200, 14, False, ORANGE, 1)
    dash(d, 360, 186, 360, 165, ORANGE, 1, 4, 4)
    ctext(d, 385, 195, "空気吸込み渦", FT, ORANGE, "lm")
    note(d, "各部の配置と流れのみ（評価手順・答えは描かない）")
    save(im, "t1e6SumpPump")


# ============================================================ 6-12 電子機器の熱流体(helpful)
def f_electronics():
    im, d = new()
    title(d, "電子機器内の熱流体：浮力を伴う熱対流")
    # ケース
    box(d, 90, 80, 590, 350, "white")
    ctext(d, 545, 96, "ケース", FT, GRAY)
    # 垂直ボード＋高温CPU
    bx = 250
    d.line((bx, 110, bx, 330), fill=BLACK, width=4)
    ctext(d, bx - 8, 340, "垂直ボード", FT, BLACK, "rm")
    box(d, bx + 4, 200, bx + 44, 250, (255, 225, 225), RED, 2)
    ctext(d, bx + 24, 225, "CPU", FT, RED)
    ctext(d, bx + 24, 262, "高温", FT, RED)
    # 冷却ファン(強制対流)
    fx, fy = 150, 150
    d.ellipse((fx - 26, fy - 26, fx + 26, fy + 26), outline=BLACK, width=2)
    for a in range(0, 360, 60):
        d.line((fx, fy, fx + 22 * math.cos(math.radians(a)), fy + 22 * math.sin(math.radians(a))), fill=GRAY, width=2)
    ctext(d, fx, fy - 40, "冷却ファン", FT, BLACK)
    for yy in (150, 175):
        arrow(d, fx + 30, yy, 240, yy, BLUE, 2, 10)
    ctext(d, 190, 195, "強制対流", FT, BLUE)
    # 浮力による上昇流
    for xx in (bx + 60, bx + 80):
        arrow(d, xx, 245, xx, 125, ORANGE, 2, 10)
    ctext(d, bx + 150, 175, "浮力による上昇流", FT, ORANGE)
    # 壁平行方向の乱流熱流束(壁ぎわ上向き)
    arrow(d, bx + 6, 205, bx + 6, 150, GREEN, 2, 9)
    d.line((bx + 6, 203, 205, 252), fill=GREEN, width=1)
    ctext(d, 160, 268, "壁平行方向の\n乱流熱流束", FT, GREEN)
    # 空気取入孔
    for yy in (300, 315):
        d.line((90, yy, 110, yy), fill=BLACK, width=2)
    ctext(d, 150, 320, "取入孔", FT, GRAY, "lm")
    note(d, "高温部の浮力を伴う熱対流。壁平行方向の乱流熱流束は渦粘性型では表せない")
    save(im, "t1e6Electronics")


if __name__ == "__main__":
    f_optimization()
    f_pump_impeller()
    f_diffuser()
    f_bluff_streamline()
    f_room_airflow()
    f_office_thermal()
    f_car_aero()
    f_karman_vortex()
    f_helical_strake()
    f_analysis_framework()
    f_sump_pump()
    f_electronics()
    print("done t1e6 (12)")
