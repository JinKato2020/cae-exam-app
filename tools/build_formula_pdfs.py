# -*- coding: utf-8 -*-
"""公式・用語(content/formulas/ch*.json)を章ごとに1PDFで出力。
数式=MathJax(SVG)、図=base64埋め込み。Edge headless の print-to-pdf を使用。
出力先 = CAE/アプリ/2級/ 固体2級_公式用語_第N章_<短縮タイトル>.pdf
使い方: python tools/build_formula_pdfs.py [章番号...]   (無指定なら1〜13章)
build_pdfs.py の姉妹ツール。"""
import json, os, base64, html, subprocess, sys

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FDIR = os.path.join(CAE, "content", "formulas")
FIG = os.path.join(CAE, "assets", "figures")
TMP = os.path.join(CAE, "tools", "_pdftmp")
OUTDIR = os.path.join(CAE, "アプリ", "2級")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def esc(s): return html.escape(s or "", quote=False)

def img_datauri(key):
    p = os.path.join(FIG, key + ".png")
    if not os.path.exists(p): return None
    b = base64.b64encode(open(p, "rb").read()).decode()
    return "data:image/png;base64," + b

def card(it):
    fig = ""
    if it.get("figureImage"):
        uri = img_datauri(it["figureImage"])
        if uri: fig = f"<div class='fig'><img src='{uri}'></div>"
    badge = "公式" if it.get("kind") == "formula" else "用語"
    bcls = "bformula" if it.get("kind") == "formula" else "bterm"
    formula = f"<div class='formula'>{esc(it['formula'])}</div>" if it.get("formula") else ""
    example = ""
    if it.get("example"):
        example = f"<div class='ex'><span class='exlabel'>数値例</span> {esc(it['example'])}</div>"
    return f"""<div class='card'>
      <div class='chead'><span class='badge {bcls}'>{badge}</span> <span class='term'>{esc(it['term'])}</span></div>
      {formula}
      <div class='body'>{esc(it['body'])}</div>
      {example}{fig}
    </div>"""

def build_html(doc):
    cards = "".join(card(it) for it in doc["items"])
    intro = f"<div class='intro'>{esc(doc.get('intro',''))}</div>" if doc.get("intro") else ""
    return f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<title>{esc(doc['title'])}</title>
<style>
@page {{ size:A4; margin:14mm 12mm; }}
body{{font-family:'Meiryo','Yu Gothic',sans-serif;color:#111;line-height:1.7;font-size:11pt;}}
h1{{font-size:16pt;border-bottom:2px solid #2456c9;padding-bottom:4px;}}
.sub{{color:#555;font-size:9pt;margin-bottom:8px;}}
.intro{{background:#f2f6ff;border:1px solid #d6e2ff;border-radius:6px;padding:8px 12px;font-size:10pt;margin:8px 0 14px;}}
.card{{break-inside:avoid;border:1px solid #ccc;border-radius:8px;padding:10px 14px;margin:10px 0;}}
.chead{{margin-bottom:6px;}}
.badge{{color:#fff;font-weight:700;font-size:9pt;border-radius:5px;padding:2px 8px;margin-right:6px;}}
.bformula{{background:#2456c9;}} .bterm{{background:#7c3aed;}}
.term{{font-weight:700;font-size:12.5pt;}}
.formula{{background:#f6f8fc;border:1px solid #dde3ee;border-radius:6px;padding:8px 12px;margin:6px 0;text-align:center;}}
.body{{margin:4px 0;}}
.ex{{background:#f7f7f4;border-left:3px solid #2456c9;padding:6px 10px;border-radius:4px;font-size:10pt;margin-top:8px;}}
.exlabel{{color:#2456c9;font-weight:700;}}
.fig{{text-align:center;margin:8px 0;}} .fig img{{max-width:70%;border:1px solid #ddd;border-radius:6px;}}
mjx-container{{overflow-x:auto;}}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"></script>
</head><body>
<h1>{esc(doc['title'])}　公式・用語</h1>
<div class="sub">CAE計算力学技術者 固体力学2級・オリジナル解説（初学者向け：公式／用語／数値例／図）</div>
{intro}{cards}
</body></html>"""

def main():
    chapters = [int(x) for x in sys.argv[1:]] or list(range(1, 14))
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    for ch in chapters:
        fp = os.path.join(FDIR, f"ch{ch}.json")
        if not os.path.exists(fp):
            print(f"ch{ch}: SKIP (no json)"); continue
        doc = json.load(open(fp, encoding="utf-8"))
        title = doc["title"]                       # 例: "第3章 熱伝導の基礎"
        short = title.split(" ", 1)[-1].replace(" ", "") if " " in title else title
        hp = os.path.join(TMP, f"formula_ch{ch}.html")
        open(hp, "w", encoding="utf-8").write(build_html(doc))
        out = os.path.join(OUTDIR, f"固体2級_公式用語_第{ch}章_{short}.pdf")
        url = "file:///" + hp.replace("\\", "/")
        cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
               f"--print-to-pdf={out}", "--print-to-pdf-no-header",
               "--virtual-time-budget=25000", "--run-all-compositor-stages-before-draw", url]
        subprocess.run(cmd, capture_output=True, timeout=120)
        ok = os.path.exists(out)
        print(f"ch{ch}: {'OK' if ok else 'FAIL'}  {out}  ({os.path.getsize(out)//1024 if ok else 0} KB)")
    print("公式・用語PDF出力完了")

if __name__ == "__main__":
    main()
