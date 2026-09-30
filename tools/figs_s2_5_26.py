# -*- coding: utf-8 -*-
"""固体2級 5-26(焼きばめ=丸軸圧入の残留応力)の図を作成。
公式問5-26の主眼=初期ひずみの符号・大きさ: 丸軸に +δ/D(軸は大きくなろうとする=正)、
厚板は逆符号 -δ/D(板は小さくなろうとする=負)を与え {σ}=[E]({ε}-{εI}) で線形弾性解析。
- f5ShrinkFitSetup : 回答前(丸軸D+δ・穴D・しめしろδの設定のみ。符号=答えは示さない)
- f5ShrinkFit      : 回答後(軸=+δ/D膨張・板=-δ/D収縮 を矢印と符号で明示)
白地660x420。"""
import sys, math
sys.path.insert(0, r"C:\Users\jwpsa\Documents\desktop\claude\CAE\tools")
from figlib import *

CX, CY = 240, 232
RSHAFT, RPLATE = 60, 138


def section(d, contract_arrows=False, expand_arrows=False):
    """厚板(外)+丸軸(内)の断面。必要なら軸=外向き膨張/板=内向き収縮の矢印。"""
    d.ellipse((CX - RPLATE, CY - RPLATE, CX + RPLATE, CY + RPLATE), outline=BLACK, width=3, fill=FILL2)
    d.ellipse((CX - RSHAFT, CY - RSHAFT, CX + RSHAFT, CY + RSHAFT), outline=BLACK, width=3, fill=FILL1)
    ctext(d, CX, CY, "丸軸", FS)
    ctext(d, CX, CY - RPLATE + 24, "厚板", FT, GRAY)
    for k in range(8):
        a = math.pi * k / 4
        ux, uy = math.cos(a), math.sin(a)
        if expand_arrows:  # 軸: 内→外(膨張)
            arrow(d, CX + ux * 18, CY + uy * 18, CX + ux * (RSHAFT - 4), CY + uy * (RSHAFT - 4), RED, 3, 10)
        if contract_arrows:  # 板: 外→内(収縮)
            r1, r2 = RSHAFT + 34, RSHAFT + 6
            arrow(d, CX + ux * r1, CY + uy * r1, CX + ux * r2, CY + uy * r2, BLUE, 3, 10)


# ===== 回答前: 設定のみ(符号は伏せる) =====
im, d = new()
title(d, "焼きばめ（丸軸圧入）: しめしろ δ")
section(d)
tx = 470
ctext(d, tx, 108, "丸軸の径 = D+δ", FT, BLACK)
ctext(d, tx, 132, "穴の径 = D", FT, BLACK)
ctext(d, tx, 172, "しめしろ δ", F, RED)
ctext(d, tx, 200, "= 軸径 − 穴径", FT, GRAY)
ctext(d, tx, 246, "初期ひずみ法で", FT, BLACK)
ctext(d, tx, 270, "残留応力を解く。", FT, BLACK)
ctext(d, tx, 310, "与える初期ひずみ", FS, BLACK)
ctext(d, tx, 336, "の符号と大きさは？", FS, BLACK)
note(d, "{σ}=[E]({ε}−{εI})。丸軸と厚板それぞれに与える初期ひずみ εI は？")
save(im, "f5ShrinkFitSetup")

# ===== 回答後: 符号を明示 =====
im, d = new()
title(d, "初期ひずみの符号: 軸=+δ/D(膨張)・板=−δ/D(収縮)")
section(d, contract_arrows=True, expand_arrows=True)
tx = 470
ctext(d, tx, 120, "軸は大きく", FS, RED)
ctext(d, tx, 146, "なろうとする", FS, RED)
ctext(d, tx, 172, "→ +δ/D (正)", FS, RED)
ctext(d, tx, 224, "板は小さく", FS, BLUE)
ctext(d, tx, 250, "なろうとする", FS, BLUE)
ctext(d, tx, 276, "→ −δ/D (負)", FS, BLUE)
ctext(d, tx, 326, "{σ}=[E]({ε}−{εI})", FT, GRAY)
note(d, "重なり量 δ を径 D で割った δ/D が初期ひずみ。軸に+、板に−(逆符号)で干渉を再現。")
save(im, "f5ShrinkFit")
