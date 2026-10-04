# -*- coding: utf-8 -*-
"""固体1級・2級の問題を「回答前」「回答後」に分けて章ごとにPDF出力する。
- 回答前PDF = 問題文＋選択肢(正解印なし)＋回答前図(preFigureImage、無ければ figure=='required' の figureImage のみ)。答え・解説は載せない。
- 回答後PDF = 問題文＋選択肢(正解を強調)＋正解＋解説＋回答後図(figureImage)。
出力先= アプリ/固体1級/ ・ アプリ/固体2級/。実行前に「古い問題PDF(固体N級_第*.pdf)」だけ削除(公式用語PDFは残す)。
固体2級はファイル名に級プレフィックスが無いため、meta.grade で級を判別する。
使い方: python tools/build_solid_beforeafter_pdfs.py            … 全章再生成
       python tools/build_solid_beforeafter_pdfs.py 1:5,6 2:3  … 指定した級:章だけ再生成(無駄を省く。他章PDFは温存)
       python tools/build_solid_beforeafter_pdfs.py 5          … 章番号のみ(両級の該当章)
恒久ツール。App.tsx の前後出し分けロジックに準拠。build_vib_beforeafter_pdfs.py の固体版。"""
import json, os, base64, html, subprocess, glob, sys, re


def _want(g, ch, path, specs):
    """引数 specs にマッチする章だけ True。specs 空なら全章 True(従来動作)。
    対応形式: "1:5,6"(級:章) / JSONパス・ファイル名 / "5"(章番号・両級)。"""
    if not specs:
        return True
    base = os.path.basename(path)
    for s in specs:
        if s == base or ((os.sep in s or "/" in s) and os.path.normpath(s) == os.path.normpath(path)):
            return True
        m = re.match(r"^([12]):([0-9,]+)$", s)
        if m and m.group(1) == g and str(ch) in m.group(2).split(","):
            return True
        if s.isdigit() and int(s) == ch:
            return True
    return False

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(CAE, "content", "questions")
FIG = os.path.join(CAE, "assets", "figures")
TMP = os.path.join(CAE, "tools", "_pdftmp")
EDGE = next((p for p in [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
] if os.path.exists(p)), r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")  # Chrome優先(Edge headlessがMathJax印刷に失敗する環境への対策)


def esc(s):
    return html.escape(s, quote=False)


def fig_exists(key):
    return bool(key) and os.path.exists(os.path.join(FIG, key + ".png"))


def img_datauri(key):
    p = os.path.join(FIG, key + ".png")
    if not os.path.exists(p):
        return None
    b = base64.b64encode(open(p, "rb").read()).decode()
    return "data:image/png;base64," + b


def expl_html(s):
    return "".join(f"<div class='eline'>{esc(l.strip())}</div>" for l in s.split("\n") if l.strip())


def before_fig_key(q):
    # App.tsx: 回答前は preFigureImage 優先、無ければ figure=='required' の時だけ figureImage。
    pre = q.get("preFigureImage")
    if fig_exists(pre):
        return pre
    if q.get("figure") == "required" and fig_exists(q.get("figureImage")):
        return q["figureImage"]
    return None


def fig_block(key):
    if not key:
        return ""
    uri = img_datauri(key)
    return f"<div class='fig'><img src='{uri}'></div>" if uri else ""


def card(q, after):
    if after:
        figkey = q.get("figureImage") if fig_exists(q.get("figureImage")) else None
        ch = "".join(f"<li class='{'ok' if i+1==q['answer'] else ''}'>{esc(c)}</li>" for i, c in enumerate(q["choices"]))
        tail = (f"<ol class='choices'>{ch}</ol>"
                f"<div class='ans'><b>正解 : {q['answer']}</b></div>"
                f"<div class='exp'>{expl_html(q['explanation'])}</div>")
    else:
        figkey = before_fig_key(q)
        ch = "".join(f"<li>{esc(c)}</li>" for c in q["choices"])
        tail = f"<ol class='choices'>{ch}</ol>"
    return f"""<div class='card'>
      <div class='chead'><span class='num'>{esc(q['number'])}</span> <span class='ttl'>{esc(q['title'])}</span>
        <span class='meta'>難{q.get('difficulty','?')}・{esc(q.get('topic',''))}</span></div>
      <div class='q'>{esc(q['question'])}</div>{fig_block(figkey)}
      {tail}
    </div>"""


def build_html(data, subject_full, grade, after):
    meta = data["meta"]
    cat = meta["category"]
    mode = "回答後（正解・解説つき）" if after else "回答前（答えを伏せた出題面）"
    cards = "".join(card(q, after) for q in data["questions"])
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<title>{esc(cat)}</title>
<style>
@page {{ size:A4; margin:14mm 12mm; }}
body{{font-family:'Meiryo','Yu Gothic',sans-serif;color:#111;line-height:1.65;font-size:11pt;}}
h1{{font-size:16pt;border-bottom:2px solid #2456c9;padding-bottom:4px;}}
.sub{{color:#555;font-size:9pt;margin-bottom:8px;}}
.card{{break-inside:avoid;border:1px solid #ccc;border-radius:8px;padding:10px 12px;margin:9px 0;}}
.chead{{margin-bottom:4px;}} .num{{font-weight:700;color:#2456c9;}} .ttl{{font-weight:700;}}
.meta{{color:#666;font-size:8.5pt;}}
.q{{margin:4px 0;}}
.fig{{text-align:center;margin:8px 0;}} .fig img{{max-width:74%;border:1px solid #ddd;border-radius:6px;}}
ol.choices{{margin:6px 0;padding-left:20px;}} ol.choices li.ok{{font-weight:700;background:#eaf7ee;}}
.ans{{color:#1f9d55;margin:4px 0;}}
.exp{{background:#f7f7f4;border-left:3px solid #2456c9;padding:6px 10px;border-radius:4px;font-size:10pt;}}
.eline{{margin:3px 0;}}
mjx-container{{overflow-x:auto;}}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"></script>
</head><body>
<h1>{esc(cat)}</h1>
<div class="sub">CAE計算力学技術者 {subject_full}{grade}・オリジナル問題 ／ {mode}</div>
{cards}
</body></html>"""


def to_pdf(doc, htmlpath, pdfpath):
    open(htmlpath, "w", encoding="utf-8").write(doc)
    url = "file:///" + htmlpath.replace("\\", "/")
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--print-to-pdf={pdfpath}", "--print-to-pdf-no-header",
           "--virtual-time-budget=25000", "--run-all-compositor-stages-before-draw", url]
    subprocess.run(cmd, capture_output=True, timeout=120)
    return os.path.exists(pdfpath)


def collect():
    # 固体の全問題ファイルを走査し、meta.grade で 1級/2級 に振り分ける
    # (固体2級はファイル名に級プレフィックスが無く descriptive 名のため)。
    plan = {"1": [], "2": []}
    for fp in sorted(glob.glob(os.path.join(QDIR, "*.json"))):
        try:
            data = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        g = str(data.get("meta", {}).get("grade", ""))
        if "固体" not in g:
            continue
        if "1級" in g:
            plan["1"].append((fp, data))
        elif "2級" in g:
            plan["2"].append((fp, data))
    for k in plan:
        plan[k].sort(key=lambda t: t[1]["meta"].get("chapter", 0))
    return plan


def main():
    os.makedirs(TMP, exist_ok=True)
    specs = sys.argv[1:]
    if specs:
        print(f"[対象限定] {specs} に該当する章だけ再生成します")
    plan = collect()
    for g in ("1", "2"):
        files = [(fp, data) for (fp, data) in plan[g] if _want(g, data["meta"].get("chapter"), fp, specs)]
        if not files:
            continue
        outdir = os.path.join(CAE, "アプリ", f"固体{g}級")
        os.makedirs(outdir, exist_ok=True)
        # 古い問題PDF削除。無指定=全章一括掃除 / 指定=該当章のみ(他章は温存)。公式用語PDFは残す。
        removed = 0
        if not specs:
            for f in glob.glob(os.path.join(outdir, f"固体{g}級_第*.pdf")):
                os.remove(f); removed += 1
        print(f"[固体{g}級] 対象{len(files)}章 / 旧問題PDF削除: {removed}件")
        for fp, data in files:
            meta = data["meta"]
            ch = meta.get("chapter")
            if specs:
                for f in glob.glob(os.path.join(outdir, f"固体{g}級_第{ch}章_*.pdf")):
                    os.remove(f)
            cat = meta["category"]
            short = cat.split(" ", 1)[-1].replace(" ", "") if " " in cat else cat
            for after, tag in [(False, "回答前"), (True, "回答後")]:
                doc = build_html(data, "固体", f"{g}級", after)
                stem = f"固体{g}級_第{ch}章_{short}_{tag}"
                hp = os.path.join(TMP, f"solid{g}_ch{ch}_{tag}.html")
                out = os.path.join(outdir, stem + ".pdf")
                ok = to_pdf(doc, hp, out)
                kb = os.path.getsize(out) // 1024 if ok else 0
                print(f"  第{ch}章 {tag}: {'OK' if ok else 'FAIL'} ({kb}KB) {stem}.pdf")
    print("完了")


if __name__ == "__main__":
    main()
