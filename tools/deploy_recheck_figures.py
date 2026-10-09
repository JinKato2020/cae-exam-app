#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""再チェックパック(ch5-8/pack2)の図を assets/figures へ反映する恒久ツール(2026-10-09)。
権威=再チェック修正パック/適用データ/figure_manifest.json(問ごと before/after のSVGパス。before無し=回答前図なし)。
源SVG=再チェック修正パック/solid2_chNN/{before,after}/N-M.svg。
対応付け:
  figureImageキー(回答後)= JSON既存。無ければ発番(s2f{ch}_{num})。after SVG を描画。
  preFigureImageキー(回答前)= before有時のみ。JSON既存(かつfigと別)ならそれ。pre==fig or None なら発番=figキー+"Setup"。before SVG を描画。
  before無し=回答前図なし: preFigureImage を外す(None)・figure='helpful'。
PNGは headless Chrome 2x スクショで assets/figures/<key>.png に出力(git管理下=復元可)。
使い方: python tools/deploy_recheck_figures.py <章> [--write]   (--write無=計画のみ)
"""
import os, re, json, sys, subprocess, tempfile, shutil, time
CAE = r"C:\Users\jwpsa\Documents\desktop\claude\CAE"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FIG = os.path.join(CAE, "assets", "figures")
PACK = os.path.join(CAE, "図", "固体2級", "再チェック修正パック")
AD = os.path.join(PACK, "適用データ")
QMAP = {5:"fem-practice",6:"numerical-basics",7:"element-tech",8:"modeling-basics"}

ch = int(sys.argv[1]); WRITE = "--write" in sys.argv
jpath = os.path.join(CAE, "content", "questions", QMAP[ch] + ".json")
data = json.load(open(jpath, encoding="utf-8"))
byno = {q.get("number"): q for q in data["questions"]}
man = json.load(open(os.path.join(AD, "figure_manifest.json"), encoding="utf-8"))

def viewbox(svg):
    s = open(svg, encoding="utf-8").read()
    m = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', s)
    return (int(float(m.group(1))), int(float(m.group(2)))) if m else (960, 560)

def render(svgpath, key):
    w, h = viewbox(svgpath); out = os.path.join(FIG, key + ".png")
    for _ in range(2):
        prof = tempfile.mkdtemp(prefix="drf_"); t0 = time.time()
        try:
            subprocess.run([CHROME,"--headless=new","--disable-gpu","--hide-scrollbars","--no-first-run",
                "--user-data-dir="+prof,"--default-background-color=FFFFFFFF","--force-device-scale-factor=2",
                "--screenshot="+out,"--window-size=%d,%d"%(w,h),
                os.path.abspath(svgpath).replace("\\","/")],capture_output=True,timeout=60)
        except Exception: pass
        finally: shutil.rmtree(prof, ignore_errors=True)
        if os.path.exists(out) and os.path.getmtime(out) >= t0 - 1: return True
    return False

def src(kind, num):
    nn = "%02d" % ch
    return os.path.join(PACK, "solid2_ch"+nn, kind, num+".svg")

def is_replace(a): return a == "replace"
def is_remove(a): return a == "remove_old_and_show_none"

print("=== ch%d 図反映計画 (manifest action準拠) ===" % ch)
done = 0; rep = 0; rem = 0; miss = []
for e in man.get("questions", man if isinstance(man, list) else []):
    num = e.get("id") or e.get("number")
    if not num or not num.startswith("%d-" % ch): continue
    q = byno.get(num)
    if not q: print("  %s : NO-JSON" % num); continue
    ba = e.get("beforeAction", "remove_old_and_show_none" if not e.get("before") else "replace")
    aa = e.get("afterAction", "remove_old_and_show_none" if not e.get("after") else "replace")
    renders = []  # (label, srcpath, key)
    # ---- 回答後(figureImage) ----
    if is_replace(aa):
        fig_key = q.get("figureImage") or ("s2f%d_%s" % (ch, num.replace("-", "_")))
        renders.append(("after->fig", src("after", num), fig_key)); rep += 1
        new_fig = fig_key
    else:
        new_fig = None  # 回答後図なし=旧図削除
    # ---- 回答前(preFigureImage) ----
    if is_replace(ba):
        pre = q.get("preFigureImage")
        if (not pre) or (pre == q.get("figureImage")):
            pre = (new_fig or ("s2f%d_%s" % (ch, num.replace("-", "_")))) + "Setup"
        renders.append(("before->pre", src("before", num), pre)); rep += 1
        new_pre = pre
    else:
        new_pre = None  # 回答前図なし
    if new_fig is None and new_pre is None:
        new_figure = "none"; rem += 1
    else:
        new_figure = "helpful"
    # 実行
    for label, s, key in renders:
        ok_src = os.path.exists(s)
        print("  %s %s  %s -> %s.png%s" % (num, label, os.path.basename(s), key, "" if ok_src else "  ★SRC欠落"))
        if not ok_src: miss.append(s)
        if WRITE and ok_src:
            if render(s, key): done += 1
            else: print("     ★render失敗:", key)
    if WRITE and new_figure != "none":
        # replace(納品図)のみJSON更新。remove指定は触らない=後で deploy_neutral_gaps が旧図で補填
        q["figureImage"] = new_fig
        q["preFigureImage"] = new_pre
        q["figure"] = new_figure
        if q.get("figureExempt") and (new_fig or new_pre): q["figureExempt"] = False
    tag = "図なし(旧図削除)" if new_figure == "none" else ("回答前:%s / 回答後:%s" % (new_pre or "なし", new_fig))
    print("     => %s / figure=%s" % (tag, new_figure))
print("--- 計画: replace描画=%d / 図なし化(remove)=%d / SRC欠落=%d ---" % (rep, rem, len(miss)))
if miss: print("欠落SRC:", miss[:10])

if WRITE:
    with open(jpath, "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write("\n")
    print("WROTE JSON:", jpath, "/ renderedPNG:", done)
