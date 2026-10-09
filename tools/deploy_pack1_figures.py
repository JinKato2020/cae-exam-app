# -*- coding: utf-8 -*-
"""pack1(ch1-3) 再チェック修正図を assets/figures へ反映する恒久ツール(2026-10-09)。
権威=再チェック修正パック/適用データ/第1-4章_適用マニフェスト.json の figureReplacements(7件)。
源SVG=再チェック修正パック/solid2_chNN/{before,after}/N-M.svg。
 - stage=after : 既存 figureImage キーPNGを差し替え描画(JSON不変)。
 - stage=before: 回答前(preFigureImage)。無ければ figureImage+"Setup" で新規発番しJSON配線。
ch1-3は維持章=この7件以外の図は触らない(gap-fill しない)。
使い方: python tools/deploy_pack1_figures.py [--write]
"""
import os, re, json, sys, subprocess, tempfile, shutil, time

CAE = r"C:\Users\jwpsa\Documents\desktop\claude\CAE"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FIG = os.path.join(CAE, "assets", "figures")
PACK = os.path.join(CAE, "図", "固体2級", "再チェック修正パック")
AD = os.path.join(PACK, "適用データ")
QMAP = {1: "math-basics", 2: "solid-basics", 3: "heat-basics"}
WRITE = "--write" in sys.argv

def viewbox(svg):
    s = open(svg, encoding="utf-8").read()
    m = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', s)
    return (int(float(m.group(1))), int(float(m.group(2)))) if m else (960, 560)

def render(svgpath, key):
    w, h = viewbox(svgpath); out = os.path.join(FIG, key + ".png")
    for _ in range(2):
        prof = tempfile.mkdtemp(prefix="p1f_"); t0 = time.time()
        try:
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                "--user-data-dir=" + prof, "--default-background-color=FFFFFFFF", "--force-device-scale-factor=2",
                "--screenshot=" + out, "--window-size=%d,%d" % (w, h),
                os.path.abspath(svgpath).replace("\\", "/")], capture_output=True, timeout=60)
        except Exception: pass
        finally: shutil.rmtree(prof, ignore_errors=True)
        if os.path.exists(out) and os.path.getmtime(out) >= t0 - 1: return True
    return False

man = json.load(open(os.path.join(AD, "第1-4章_適用マニフェスト.json"), encoding="utf-8"))
reps = man["figureReplacements"]

# chapter -> loaded json (lazy, write once)
loaded = {}
def getjson(ch):
    if ch not in loaded:
        p = os.path.join(CAE, "content", "questions", QMAP[ch] + ".json")
        loaded[ch] = (p, json.load(open(p, encoding="utf-8")))
    return loaded[ch]

changed = set(); done = 0; miss = []
print("=== pack1(ch1-3) 図反映計画 (figureReplacements %d件) ===" % len(reps))
for r in reps:
    pid = r["problemId"]; stage = r["stage"]
    ch = int(pid.split("-")[0])
    nn = "%02d" % ch
    src = os.path.join(PACK, "solid2_ch" + nn, stage, pid + ".svg")
    p, data = getjson(ch)
    q = next((x for x in data["questions"] if x.get("number") == pid), None)
    if q is None:
        print("  %s : NO-JSON" % pid); continue
    if not os.path.exists(src):
        print("  %s %s : ★SRC欠落 %s" % (pid, stage, src)); miss.append(src); continue
    if stage == "after":
        key = q.get("figureImage")
        if not key:
            print("  %s after : figureImageキー無し→スキップ" % pid); continue
        act = "回答後 %s.png 差替" % key
    else:  # before
        key = q.get("preFigureImage")
        newwire = False
        if not key:
            base = q.get("figureImage") or ("s2f%d_%s" % (ch, pid.replace("-", "_")))
            key = base + "Setup"; newwire = True
        act = "回答前 %s.png%s" % (key, "(新規配線)" if newwire else "差替")
    print("  %s %s -> %s  [%s]" % (pid, stage, os.path.basename(src), act))
    if WRITE:
        if render(src, key):
            done += 1
            if stage == "before" and q.get("preFigureImage") != key:
                q["preFigureImage"] = key
                if q.get("figure") in (None, "none"): q["figure"] = "helpful"
                if q.get("figureExempt"): q["figureExempt"] = False
                changed.add(ch)
        else:
            print("     ★render失敗:", key)
print("--- 計画: %d件 / SRC欠落=%d ---" % (len(reps), len(miss)))
if WRITE:
    for ch in changed:
        p, data = loaded[ch]
        with open(p, "w", encoding="utf-8", newline="\r\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2); f.write("\n")
        print("WROTE JSON:", os.path.basename(p))
    print("renderedPNG:", done)
