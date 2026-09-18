# -*- coding: utf-8 -*-
"""熱流体力学2級 第7章「境界条件」の図(接頭辞 t2e7)を12枚描く。
JSON本体は編集しない。white 660x420 線画・機構だけ。ファイル名=figureImage(t2e7Xxx)。
required(回答前表示)には答え・正解値・結論を絶対に描かない([[cae-figure-before-after-rule]])。
required=7問: t2e7InflowBC, t2e7OutflowBC, t2e7HeatedPipeWall, t2e7CavityNaturalConv,
             t2e7LowReNearWall, t2e7FreeSurfaceChannel, t2e7BLedge
helpful=5問: t2e7WallPressureBC, t2e7WallFunctionLog, t2e7VelTempLogLaw,
             t2e7SupersonicChar, t2e7CarGroundBC
豆腐回避: 上付き/下付き特殊記号は使わず y+ / U+ / T+ / ^2 / T0 / u_tau 等の通常表記。
"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ---- ローカル補助(ch6と同一書式) --------------------------------
def box(d, cx, cy, w, h, text, fnt=FS, fill="white", oc=BLACK):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
                outline=oc, width=3, fill=fill)
    lines = text.split("\n")
    lh = fnt.size + 6
    y0 = cy - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        ctext(d, cx, y0 + i * lh, ln, fnt)


def swirl(d, cx, cy, r, col=BLUE, wd=3, a0=20, a1=320):
    d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=wd)
    ae = math.radians(a1); ap = math.radians(a1 - 22)
    ex, ey = cx + r * math.cos(ae), cy + r * math.sin(ae)
    px, py = cx + r * math.cos(ap), cy + r * math.sin(ap)
    arrow(d, px, py, ex, ey, col, wd, 11)


# ==================================================================
# 7-1 required : 円管の流入境界(一様速度・一定温度T0)。境界条件の種類名は書かない
def f_inflow():
    im, d = new()
    title(d, "円管の流入境界に与える速度と温度")
    x0, x1, yt, yb = 190, 600, 150, 300
    hwall(d, x0, x1, yt, side=-1, n=12)     # 上壁
    hwall(d, x0, x1, yb, side=1, n=12)      # 下壁
    # 流入境界(左の縦線)
    d.line((x0, yt, x0, yb), fill=BLUE, width=3)
    ctext(d, x0, yb + 22, "流入境界", FS, BLUE)
    # 一様な速度(そろった長さの矢印)
    for yy in range(yt + 20, yb - 8, 24):
        arrow(d, x0 + 4, yy, x0 + 66, yy, BLACK, 2, 9)
    ctext(d, 340, 200, "一様な速度 u", FS, BLACK, "lm")
    ctext(d, 340, 232, "一定温度 T0", FS, RED, "lm")
    # 管壁を加熱(外から壁へ)
    for xx in range(x0 + 40, x1 - 20, 62):
        arrow(d, xx, yt - 48, xx, yt - 12, RED, 2, 10)
        arrow(d, xx, yb + 48, xx, yb + 12, RED, 2, 10)
    ctext(d, (x0 + x1) / 2, yt - 62, "管壁を加熱", FT, RED)
    ctext(d, (x0 + x1) / 2, yb + 64, "管壁を加熱", FT, RED)
    save(im, "t2e7InflowBC")


# 7-2 required : 流出境界。入口で発達しつつ→下流で放物形→右端が流出境界。答えは書かない
def f_outflow():
    im, d = new()
    title(d, "円管内流れの発達と流出境界")
    x0, x1, yt, yb = 100, 580, 130, 310
    hwall(d, x0, x1, yt, side=-1, n=13)
    hwall(d, x0, x1, yb, side=1, n=13)
    ymid = (yt + yb) / 2; Hh = (yb - yt) / 2
    # 入口付近: 発達しつつある(平たい)分布
    xa = 150
    d.line((xa, yt, xa, yb), fill=GRAY, width=1)
    for yy in range(yt + 12, yb - 6, 20):
        f = 1 - abs((yy - ymid) / Hh) ** 4        # 平たいプロファイル
        arrow(d, xa, yy, xa + 90 * f, yy, BLUE, 2, 8)
    ctext(d, xa + 20, yb + 20, "入口付近(発達中)", FT, BLUE)
    # 下流: 十分発達した放物形分布
    xb = 400
    d.line((xb, yt, xb, yb), fill=GRAY, width=1)
    for yy in range(yt + 12, yb - 6, 20):
        f = 1 - ((yy - ymid) / Hh) ** 2           # 放物形
        arrow(d, xb, yy, xb + 120 * f, yy, BLUE, 2, 8)
    ctext(d, xb + 30, yb + 20, "下流(十分発達)", FT, BLUE)
    # 右端=流出境界
    d.line((x1, yt, x1, yb), fill=GREEN, width=3)
    ctext(d, x1, yt - 14, "流出境界", FS, GREEN)
    save(im, "t2e7OutflowBC")


# 7-3 required : 外周を水蒸気で一様加熱、入口空気10m/s 20°C。壁面境界条件名は書かない
def f_heatwall():
    im, d = new()
    title(d, "外周を一様加熱した円管への空気の流入")
    x0, x1, yt, yb = 190, 585, 150, 300
    hwall(d, x0, x1, yt, side=-1, n=11)
    hwall(d, x0, x1, yb, side=1, n=11)
    # 流入(左)
    d.line((x0, yt, x0, yb), fill=BLUE, width=3)
    for yy in range(yt + 18, yb - 8, 26):
        arrow(d, x0 + 4, yy, x0 + 58, yy, BLACK, 2, 9)
    # 流入空気の条件は入口の左外に置く(下部の加熱矢印と干渉させない)
    arrow(d, 120, (yt + yb) / 2, x0 - 4, (yt + yb) / 2, BLACK, 2, 10)
    ctext(d, 95, (yt + yb) / 2, "空気\n10 m/s\n20°C", FT, BLACK)
    # 水蒸気で一様加熱(外から壁へ)
    for xx in range(x0 + 36, x1 - 14, 56):
        arrow(d, xx, yt - 50, xx, yt - 12, RED, 3, 11)
        arrow(d, xx, yb + 50, xx, yb + 12, RED, 3, 11)
    ctext(d, (x0 + x1) / 2, yt - 64, "水蒸気で一様加熱", FS, RED)
    ctext(d, (x0 + x1) / 2, yb + 66, "水蒸気で一様加熱", FT, RED)
    save(im, "t2e7HeatedPipeWall")


# 7-4 helpful : 壁面上の微小要素で 圧力勾配項 と 粘性項 がつり合う(根拠図)
def f_wallpress():
    im, d = new()
    title(d, "壁面圧力は運動方程式のつり合いで決まる")
    hwall(d, 110, 560, 335, side=1, n=13)
    ctext(d, 540, 352, "固体壁", FT, BLACK, "lm")
    # 微小流体要素
    ex, ey, es = 330, 225, 74
    d.rectangle((ex - es / 2, ey - es / 2, ex + es / 2, ey + es / 2),
                outline=BLACK, width=3, fill=FILL1)
    ctext(d, ex, ey, "微小\n流体要素", FT, BLACK)
    # 壁面垂直(y)方向に2項がつり合う
    arrow(d, ex - 125, ey - 30, ex - 125, ey + 40, BLUE, 4, 14)
    ctext(d, ex - 125, ey - 50, "-(1/ρ)∂p/∂y", FS, BLUE)
    arrow(d, ex + 125, ey + 40, ex + 125, ey - 30, GREEN, 4, 14)
    ctext(d, ex + 125, ey - 50, "ν ∂^2 v/∂y^2", FS, GREEN)
    # y軸(壁垂直)
    arrow(d, 110, 320, 110, 205, BLACK, 2, 11)
    ctext(d, 110, 190, "y(壁垂直)", FT, BLACK)
    note(d, "壁面上で2つの項がつり合い壁面圧力が定まる")
    save(im, "t2e7WallPressureBC")


# 7-5 required : 2次元閉空間 上下断熱・左壁一定熱流束q流入・右壁D・内部循環・x/y軸。数値は書かない
def f_cavity():
    im, d = new()
    title(d, "2次元閉空間内の自然対流")
    x0, x1, y0, y1 = 235, 470, 95, 330
    hwall(d, x0, x1, y0, side=-1, n=8)      # 上壁(断熱)
    hwall(d, x0, x1, y1, side=1, n=8)       # 下壁(断熱)
    d.line((x0, y0, x0, y1), fill=RED, width=3)     # 左壁(熱流束)
    d.line((x1, y0, x1, y1), fill=BLACK, width=3)   # 右壁D
    ctext(d, (x0 + x1) / 2, y0 - 26, "断熱", FT, GRAY)
    ctext(d, (x0 + x1) / 2, y1 + 24, "断熱", FT, GRAY)
    # 左壁から流入する一定熱流束q
    for yy in range(y0 + 22, y1 - 10, 30):
        arrow(d, x0 - 2, yy, x0 + 40, yy, RED, 3, 11)
    ctext(d, 150, (y0 + y1) / 2 - 16, "左壁", FS, RED)
    ctext(d, 150, (y0 + y1) / 2 + 12, "一定熱流束 q", FS, RED)
    ctext(d, x1 + 8, (y0 + y1) / 2, "壁D", FS, BLACK, "lm")
    # 内部の自然対流循環
    swirl(d, (x0 + x1) / 2 + 24, (y0 + y1) / 2, 58, BLUE, 3)
    # 座標軸 x(水平)・y(鉛直)
    ax, ay = 130, 380
    arrow(d, ax, ay, ax + 52, ay, BLACK, 2, 10); ctext(d, ax + 62, ay, "x", FS)
    arrow(d, ax, ay, ax, ay - 52, BLACK, 2, 10); ctext(d, ax, ay - 64, "y", FS)
    save(im, "t2e7CavityNaturalConv")


# 7-6 helpful : 対数速度分布(U+ vs ln y+)・第一格子点y0・仮想原点・壁法則(根拠図)
def f_wallfunc():
    im, d = new()
    title(d, "壁関数(対数則)と壁面第一格子点")
    ox, oy = 150, 335; xlen, ylen = 400, 250
    axes(d, ox, oy, xlen, ylen, "ln y+", "U+")
    # 対数則の直線領域
    pts = []
    for i in range(20, 391, 6):
        xx = ox + i
        u = 40 + i * 0.46
        pts.append((xx, oy - min(u, 236)))
    plot(d, 0, 0, pts, BLUE, 3)
    # 第一格子点 y0
    mx = ox + 150
    uy = oy - min(40 + 150 * 0.46, 236)
    d.line((mx, oy, mx, uy), fill=GRAY, width=1)
    node(d, mx, uy, 6)
    ctext(d, mx, oy + 16, "第一格子点 y0", FT, BLACK)
    # 仮想原点
    ctext(d, ox + 6, oy + 16, "仮想原点", FT, GRAY, "lm")
    # 壁法則の式
    ctext(d, ox + 8, oy - ylen + 12,
          "U/u_tau = (1/κ) ln(y0 u_tau/ν) + C", FT, BLUE, "lm")
    note(d, "対数則の直線領域に第一格子点をとり壁面値を与える")
    save(im, "t2e7WallFunctionLog")


# 7-7 required : 低Re型 壁面近傍まで細かい格子・粘性底層を直接解像。k,εの与え方は書かない
def f_lowre():
    im, d = new()
    title(d, "低レイノルズ数型: 壁面まで細かい格子で直接解像")
    x0, x1, yw = 110, 560, 340
    hwall(d, 90, 585, yw, side=1, n=13)
    ctext(d, 588, yw + 16, "壁面", FT, BLACK, "lm")
    # 壁に近いほど細かい水平格子線
    ys = []
    y = yw - 6; dyv = 6.0
    while y > 95:
        ys.append(y)
        d.line((x0, y, x1, y), fill=LGRAY, width=1)
        y -= dyv; dyv *= 1.28
    ytop = ys[-1]
    for xx in range(x0, x1 + 1, 45):
        d.line((xx, ytop, xx, yw), fill=LGRAY, width=1)
    # 粘性底層(壁のごく近く)
    d.rectangle((x0, yw - 30, x1, yw), outline=None, fill=FILL1)
    for xx in range(x0, x1 + 1, 45):
        d.line((xx, yw - 30, xx, yw), fill=LGRAY, width=1)
    d.line((x0, yw - 30, x1, yw - 30), fill=LGRAY, width=1)
    ctext(d, x1 - 6, yw - 15, "粘性底層まで直接解像", FT, GRAY, "rm")
    note(d, "壁のごく近くほど格子を細かくし壁面近傍を直接解く")
    save(im, "t2e7LowReNearWall")


# 7-8 required : 3次元開水路の斜視図・上面自由表面・x/y/z軸とU/V/W・∂P/∂x=一定。答えは書かない
def f_freesurf():
    im, d = new()
    title(d, "自由表面をもつ3次元開水路")
    ox, oy, w, h, dp = 190, 190, 290, 130, 110
    dx, dy = int(dp * 0.8), int(dp * 0.5)
    # 前面(水)・上面(自由表面)・右面
    d.polygon([(ox, oy), (ox + w, oy), (ox + w, oy + h), (ox, oy + h)],
              outline=BLACK, width=3, fill=FILL1)
    d.polygon([(ox, oy), (ox + dx, oy - dy), (ox + w + dx, oy - dy), (ox + w, oy)],
              outline=BLACK, width=3, fill=(232, 242, 252))
    d.polygon([(ox + w, oy), (ox + w + dx, oy - dy),
               (ox + w + dx, oy + h - dy), (ox + w, oy + h)],
              outline=BLACK, width=3, fill=FILL3)
    ctext(d, ox + w / 2 + dx / 2, oy - dy / 2 - 2, "自由表面(上面)", FT, BLUE)
    # 流れ方向x(前面下辺に沿う矢印)
    arrow(d, ox + 30, oy + h + 28, ox + w - 30, oy + h + 28, BLACK, 3, 13)
    ctext(d, ox + w / 2, oy + h + 46, "流れ方向 x", FT, BLACK)
    ctext(d, ox + w / 2, oy + h + 68, "∂P/∂x = 一定 で駆動", FT, GRAY)
    # 座標三面図と速度成分
    cx, cy = 105, 300
    arrow(d, cx, cy, cx + 48, cy, BLACK, 2, 10); ctext(d, cx + 60, cy, "x, U", FT, BLACK, "lm")
    arrow(d, cx, cy, cx, cy - 48, BLACK, 2, 10); ctext(d, cx, cy - 60, "y, V", FT, BLACK)
    arrow(d, cx, cy, cx + 32, cy - 22, BLACK, 2, 10); ctext(d, cx + 44, cy - 28, "z, W", FT, BLACK, "lm")
    save(im, "t2e7FreeSurfaceChannel")


# 7-9 helpful : 速度対数則(U+ vs y+)と温度対数分布(T+ vs y+)を並べる(根拠図)
def f_veltemp():
    im, d = new()
    title(d, "速度の対数則と温度の対数分布")

    def logplot(ox, oy, xl, yl, ylab, eq, sub):
        axes(d, ox, oy, xl, yl, "y+", ylab)
        pts = []
        for i in range(14, xl - 6, 5):
            v = 24 + i * 0.9
            pts.append((ox + i, oy - min(v, yl - 8)))
        plot(d, 0, 0, pts, BLUE, 3)
        ctext(d, ox + xl / 2, oy + 34, sub, FS, BLACK)
        ctext(d, ox, oy - yl - 4, eq, FT, BLUE, "lm")

    logplot(90, 320, 210, 210, "U+",
            "U+ = (1/κ) ln y+ + C", "速度場")
    logplot(390, 320, 210, 210, "T+",
            "T+ = (1/κt) ln y0+ + C", "温度場")
    note(d, "κ ≈ 0.41,  C ≈ 5.0 (速度も温度も対数分布)")
    save(im, "t2e7VelTempLogLaw")


# 7-10 required : 平板境界層の側面・外縁で主流速度Ue(x)。圧力勾配の式や答えは書かない
def f_bledge():
    im, d = new()
    title(d, "平板境界層と外縁の主流速度 Ue(x)")
    x0, x1, yw = 90, 590, 330
    hwall(d, x0, x1, yw, side=1, n=14)
    ctext(d, (x0 + x1) / 2, yw + 22, "平板", FT, BLACK)
    # 境界層外縁(成長する曲線)
    edge = []
    for i in range(0, 501, 8):
        xx = x0 + i
        d0 = 130 * (0.18 + 0.82 * (i / 500.0) ** 0.5)
        edge.append((xx, yw - d0))
    plot(d, 0, 0, edge, GRAY, 2)
    ctext(d, edge[-1][0] - 66, edge[-1][1] - 16, "境界層外縁", FT, GRAY, "rm")
    # 外縁より上=主流速度Ue(x)
    for xx in range(150, 560, 68):
        arrow(d, xx, 108, xx + 52, 108, BLUE, 2, 10)
    ctext(d, (x0 + x1) / 2, 88, "主流速度 Ue(x)", FS, BLUE)
    # 境界層内の速度分布(2断面)
    for xb in (240, 430):
        i = xb - x0
        d0 = 130 * (0.18 + 0.82 * (i / 500.0) ** 0.5)
        d.line((xb, yw, xb, yw - d0), fill=GRAY, width=1)
        n = 6
        for kk in range(1, n + 1):
            yy = yw - d0 * kk / n
            f = (kk / n) ** 0.5
            arrow(d, xb, yy, xb + 44 * f, yy, BLUE, 2, 7)
    save(im, "t2e7BLedge")


# 7-11 helpful : 超音速(M=2)航空機まわり・情報が上流→下流へ一方向・特性線(根拠図)
def f_supersonic():
    im, d = new()
    title(d, "超音速流(マッハ2)の情報伝播")
    # 流入・流出境界
    d.line((80, 90, 80, 350), fill=BLUE, width=3)
    ctext(d, 80, 366, "流入境界", FT, BLUE)
    d.line((600, 90, 600, 350), fill=GREEN, width=3)
    ctext(d, 600, 366, "流出境界", FT, GREEN)
    # 主流(M=2)
    for yy in (140, 300):
        arrow(d, 95, yy, 150, yy, GRAY, 2, 10)
    ctext(d, 130, 118, "M = 2", FT, GRAY)
    # 航空機(デルタ・右向き)
    nx, ny = 250, 220
    d.polygon([(nx, ny), (nx + 95, ny - 22), (nx + 95, ny + 22)],
              outline=BLACK, width=3, fill=FILL2)
    # 特性線(マッハ波)は下流(右)へ
    arrow(d, nx, ny, nx + 300, ny - 96, RED, 2, 13)
    arrow(d, nx, ny, nx + 300, ny + 96, RED, 2, 13)
    ctext(d, nx + 250, ny - 96, "特性線", FT, RED)
    ctext(d, nx + 250, ny + 108, "(下流へ)", FT, RED)
    ctext(d, 330, 320, "擾乱は上流から下流へ一方向に伝わる", FT, GRAY)
    save(im, "t2e7SupersonicChar")


# 7-12 helpful : 自動車固定の相対座標系・車体表面0・地面が走行方向と逆に25m/s(根拠図)
def f_carground():
    im, d = new()
    title(d, "自動車固定の相対座標系と地面の境界条件")
    gy = 320
    # 走行方向(右)
    arrow(d, 430, 95, 560, 95, GRAY, 2, 12)
    ctext(d, 495, 78, "走行方向", FT, GRAY)
    # 車体(簡易シルエット)
    bx0, bx1 = 210, 430
    d.rectangle((bx0, gy - 46, bx1, gy - 12), outline=BLACK, width=3, fill=FILL2)  # 車体
    d.polygon([(bx0 + 42, gy - 46), (bx0 + 78, gy - 84),
               (bx1 - 78, gy - 84), (bx1 - 42, gy - 46)],
              outline=BLACK, width=3, fill=FILL1)  # ルーフ
    for wx in (bx0 + 46, bx1 - 46):
        d.ellipse((wx - 20, gy - 20, wx + 20, gy + 20), outline=BLACK, width=3, fill="white")
    ctext(d, (bx0 + bx1) / 2, gy - 108, "車体表面: 速度 0", FS, BLACK)
    # 地面
    d.line((80, gy, 600, gy), fill=BLACK, width=3)
    # 地面は走行方向と逆向き(左)に25 m/s
    for xx in range(540, 150, -80):
        arrow(d, xx, gy + 20, xx - 56, gy + 20, RED, 3, 12)
    ctext(d, 340, gy + 46, "地面: 走行方向と逆向きに 25 m/s", FS, RED)
    save(im, "t2e7CarGroundBC")


if __name__ == "__main__":
    for fn in [f_inflow, f_outflow, f_heatwall, f_wallpress, f_cavity,
               f_wallfunc, f_lowre, f_freesurf, f_veltemp, f_bledge,
               f_supersonic, f_carground]:
        fn()
    print("done 12")
