# -*- coding: utf-8 -*-
"""固体力学1級 第7章「伝熱解析」1:1補完問題の図(s1e7*)。
白地660x420・線画・機構のみ。豆腐回避のためギリシャ文字はローマ字表記(eps,sigma 等)。
既存 tools/figs_s1_ch7.py に準拠。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *


# ============================================================
# 7-8 (公式 問7-8)  s1e7MultiReflect :
#   平行2灰色体面の多重反射級数。面1から E1 放射 -> 面2 吸収 eps2*E1,
#   反射(1-eps2)E1 -> 面1 反射 -> 面2 吸収 eps2(1-eps1)(1-eps2)E1 ...
# ============================================================
def multi_reflect():
    im, d = new()
    title(d, "灰色体2面間の多重反射: 面2が吸収する Q2")
    # 2枚の平板
    x1, x2 = 120, 420
    d.rectangle((x1 - 24, 90, x1, 320), outline=BLACK, width=3, fill=(250, 225, 225))
    d.rectangle((x2, 90, x2 + 24, 320), outline=BLACK, width=3, fill=(225, 230, 250))
    ctext(d, x1 - 12, 74, "面1", FT, RED); ctext(d, x2 + 12, 74, "面2", FT, BLUE)
    ctext(d, x1 - 12, 336, "eps1", FT, RED); ctext(d, x2 + 12, 336, "eps2", FT, BLUE)
    # 反射の道筋(左->右->左->右...) と 各回で面2が吸収する項
    seq = [(x1, 118), (x2, 148), (x1, 186), (x2, 216), (x1, 254), (x2, 284)]
    for i in range(len(seq) - 1):
        col = ORANGE if i % 2 == 0 else GRAY
        arrow(d, seq[i][0], seq[i][1], seq[i + 1][0], seq[i + 1][1], col, 2, 10)
    # 面1発の初回放射ラベル
    ctext(d, (x1 + x2) / 2, 124, "E1 放射", FT, ORANGE)
    # 面2が吸収する各項(右側に注記, e1=eps1,e2=eps2)
    ctext(d, x2 + 34, 148, "吸収: eps2 E1", FT, BLUE, "lm")
    ctext(d, x2 + 34, 216, "+ eps2(1-e1)(1-e2)E1", FT, BLUE, "lm")
    ctext(d, x2 + 34, 284, "+ ... 公比(1-e1)(1-e2)", FT, GRAY, "lm")
    # 総和(閉じた形)
    d.rectangle((150, 356, 512, 392), outline=BLACK, width=2, fill=FILL2)
    ctext(d, 331, 374, "Q2 = eps2*E1 / (1 - (1-eps1)(1-eps2))", FT)
    note(d, "初項は eps2*E1。反射のたび (1-eps1)(1-eps2) 倍の等比級数を面2が吸収")
    save(im, "s1e7MultiReflect")


if __name__ == "__main__":
    multi_reflect()
    print("done ch7 cov")
