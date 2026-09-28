# -*- coding: utf-8 -*-
"""固体2級 レビュー修正(第11・12章の図)。figlib.py で再生成。
 ver11WallTemp  : 材料界面での誤った温度の飛びを除去し、界面は温度連続(勾配のみ
                  変化)、表面(内外)で熱伝達率に応じた流体との温度差を描く。
 comp12InfoLoss : 設問と同じ 1234+1.987-1233 を有効数字4桁で2段階に示す
                  (加算=情報落ち → 減算=桁落ち)。
実行すると assets/figures/*.png を上書きする。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *


def dashed(d, x1, y1, x2, y2, col=GRAY, wd=2, dash=8, gap=6):
    total = math.hypot(x2 - x1, y2 - y1)
    if total == 0:
        return
    ux, uy = (x2 - x1) / total, (y2 - y1) / total
    t = 0.0
    while t < total:
        a = min(t + dash, total)
        d.line((x1 + ux * t, y1 + uy * t, x1 + ux * a, y1 + uy * a), fill=col, width=wd)
        t += dash + gap


def fig_ver11_wall_temp():
    im, d = new()
    title(d, "断熱円筒壁の温度分布(界面は連続・表面で飛び)")
    ox, oy = 95, 350
    xs_in, x_int, xs_out, x_end = 150, 330, 520, 600
    # 層の塗り分け
    d.rectangle((xs_in, 90, x_int, oy), fill=(255, 239, 224), outline=None)   # レンガ
    d.rectangle((x_int, 90, xs_out, oy), fill=(231, 238, 250), outline=None)  # ブロック
    axes(d, ox, oy, 530, 300, "", "")
    ctext(d, ox - 6, 82, "温度 T", FS, BLACK, "rm")
    ctext(d, 622, oy + 18, "半径方向", FS, BLACK, "rm")
    # 壁面(内・外)と界面
    d.line((xs_in, 90, xs_in, oy), fill=BLACK, width=2)
    d.line((xs_out, 90, xs_out, oy), fill=BLACK, width=2)
    dashed(d, x_int, 90, x_int, oy, GRAY, 2)
    # 温度プロファイル
    Tf_in, Tw_in, Ti, Tw_out, Tf_out = 105, 130, 190, 295, 348
    dashed(d, ox, Tf_in, xs_in, Tf_in, (200, 90, 90), 2)      # 内側流体温度
    dashed(d, xs_out, Tf_out, x_end, Tf_out, (200, 90, 90), 2)  # 外側流体温度
    d.line((xs_in, Tf_in, xs_in, Tw_in), fill=RED, width=3)   # 内表面の小さな飛び
    d.line((xs_in, Tw_in, x_int, Ti), fill=RED, width=3)      # レンガ(緩やか)
    d.line((x_int, Ti, xs_out, Tw_out), fill=RED, width=3)    # ブロック(急)
    d.line((xs_out, Tw_out, xs_out, Tf_out), fill=RED, width=3)  # 外表面の大きな飛び
    node(d, x_int, Ti, 5, fill="white", col=RED)             # 界面=連続点
    # ラベル
    ctext(d, (xs_in + x_int) / 2, 104, "レンガ層(λ大)", FT, (170, 90, 20))
    ctext(d, (x_int + xs_out) / 2, 104, "ブロック層(λ小)", FT, (40, 80, 160))
    ctext(d, x_int + 8, Ti + 16, "界面:温度連続", FT, GREEN, "lm")
    ctext(d, ox + 6, Tf_in - 12, "内側流体", FT, GRAY, "lm")
    ctext(d, xs_out + 2, Tf_out - 12, "外側流体", FT, GRAY, "lm")
    ctext(d, xs_in - 4, 150, "h大→飛び小", FT, RED, "rm")
    ctext(d, xs_out + 6, 322, "h小→飛び大", FT, RED, "lm")
    note(d, "材料界面は温度連続(勾配のみ変化)。表面は熱伝達率で流体と温度差(飛び)")
    save(im, "ver11WallTemp")


def fig_comp12_info_loss():
    im, d = new()
    title(d, "有効数字4桁での 1234 + 1.987 − 1233")
    x = 70
    ctext(d, x, 108, "① 加算 → 情報落ち", F, BLACK, "lm")
    ctext(d, x + 24, 148, "1234.000 + 1.987 = 1235.987  →  4桁に丸め 1236", FS, BLACK, "lm")
    ctext(d, x + 24, 180, "小さい 1.987 の下位桁が消える", FS, RED, "lm")
    ctext(d, x, 240, "② 減算 → 桁落ち", F, BLACK, "lm")
    ctext(d, x + 24, 280, "1236 − 1233 = 3", FS, BLACK, "lm")
    ctext(d, x + 24, 312, "近い数どうしの差 → 有効桁が1桁に激減", FS, RED, "lm")
    ctext(d, x, 352, "真値 2.987 に対し、計算結果は 3", FS, GRAY, "lm")
    note(d, "有効数字4桁: ①加算=情報落ち / ②減算=桁落ち")
    save(im, "comp12InfoLoss")


if __name__ == "__main__":
    fig_ver11_wall_temp()
    fig_comp12_info_loss()
