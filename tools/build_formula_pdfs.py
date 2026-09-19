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

# 主役の数式を必ず $$…$$（MathJax display＝大きい中央表示）に統一する。
# アプリ側 App.tsx displayMath() と同じ規則。
# 長い公式は横に収まらないと右が切れる。ただ縮小すると読めないので、できる限り改行して
# 各行を短くする（App.tsx wrapLongDisplay と同じロジック）：
#   ① トップレベルの \quad / \qquad で独立式を分割
#   ② それでも長い行は トップレベルの + と（先頭以外の）= でさらに改行
# 括弧・ブレース(\{ \} 含む)の深さ0だけが対象。割れない単一長大式はそのまま(A4ならほぼ収まる)。
import re as _re

def _esc_depth(s, i, depth):
    nx = s[i + 1] if i + 1 < len(s) else ""
    if nx in "{([": return depth + 1
    if nx in "})]": return max(0, depth - 1)
    return depth

def _split_quad(inner):
    parts = []; depth = 0; last = 0; i = 0; n = len(inner)
    while i < n:
        c = inner[i]
        if c == "\\":
            m = _re.match(r"\\q?quad(?![a-zA-Z])", inner[i:])
            if depth == 0 and m:
                parts.append(inner[last:i]); i += len(m.group(0)); last = i; continue
            depth = _esc_depth(inner, i, depth); i += 2; continue
        if c in "{([": depth += 1
        elif c in "})]": depth = max(0, depth - 1)
        i += 1
    parts.append(inner[last:])
    return [p.strip() for p in parts if p.strip()]

def _break_ops(seg):
    idx = []; depth = 0; i = 0; n = len(seg)
    while i < n:
        c = seg[i]
        if c == "\\":
            depth = _esc_depth(seg, i, depth); i += 2; continue
        if c in "{([": depth += 1; i += 1; continue
        if c in "})]": depth = max(0, depth - 1); i += 1; continue
        if depth == 0:
            if c == "+" and i > 0: idx.append(i)
            elif c == "=" and i > 8: idx.append(i)
        i += 1
    if not idx:
        return [seg]
    lines = []; start = 0
    for p in idx:
        if p > start: lines.append(seg[start:p])
        start = p
    lines.append(seg[start:])
    return [s.strip() for s in lines if s.strip()]

def wrap_long(inner):
    if len(inner) < 50:
        return inner
    lines = []
    for seg in _split_quad(inner):
        lines += _break_ops(seg) if len(seg) >= 60 else [seg]
    if len(lines) <= 1:
        return inner
    return r"\begin{gather*}" + r" \\ ".join(lines) + r"\end{gather*}"

def display_math(s):
    x = (s or "").strip()
    if x.startswith("$$") and x.endswith("$$") and len(x) > 4:
        inner = x[2:-2]
    elif x.startswith("$") and x.endswith("$") and len(x) > 2 and x[1:-1].find("$") == -1:
        inner = x[1:-1]
    elif x.find("$") == -1 and len(x) > 0:
        inner = x
    else:
        return x
    return "$$" + wrap_long(inner) + "$$"

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
    formula = f"<div class='formula'>{esc(display_math(it['formula']))}</div>" if it.get("formula") else ""
    example = ""
    if it.get("example"):
        example = f"<div class='ex'><span class='exlabel'>数値例</span> {esc(it['example'])}</div>"
    return f"""<div class='card'>
      <div class='chead'><span class='badge {bcls}'>{badge}</span> <span class='term'>{esc(it['term'])}</span></div>
      {formula}
      <div class='body'>{esc(it['body'])}</div>
      {example}{fig}
    </div>"""

def subject_of(path_or_name):
    """ファイル名から分野を判別: thermal*→熱流体 / それ以外(solid*・ch*)→固体。"""
    b = os.path.basename(path_or_name).lower()
    if "thermal" in b: return "熱流体", "熱流体力学"
    return "固体", "固体力学"

def build_html(doc, subject_full="固体力学"):
    grade = "1級" if "1級" in doc.get("grade", "2級") else "2級"
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
<div class="sub">CAE計算力学技術者 {subject_full}{esc(grade)}・オリジナル解説（初学者向け：公式／用語／数値例／図）</div>
{intro}{cards}
</body></html>"""

def main():
    # 引数: 数字=2級のch番号(従来通り) / ファイル名(例 solid1-ch8)=そのJSONを1本ビルド。
    # 無指定なら2級 ch1〜13。級は各JSONの "grade"(既定 "2級")で判別し 出力先 アプリ/<級>/ を切替。
    args = sys.argv[1:]
    tasks = []  # (jsonパス, ラベル)
    if not args:
        tasks = [(os.path.join(FDIR, f"ch{ch}.json"), f"ch{ch}") for ch in range(1, 14)]
    else:
        for a in args:
            stem = a[:-5] if a.endswith(".json") else (f"ch{a}" if a.isdigit() else a)
            tasks.append((os.path.join(FDIR, f"{stem}.json"), stem))
    os.makedirs(TMP, exist_ok=True)
    for fp, label in tasks:
        if not os.path.exists(fp):
            print(f"{label}: SKIP (no json)"); continue
        doc = json.load(open(fp, encoding="utf-8"))
        grade = "1級" if "1級" in doc.get("grade", "2級") else "2級"
        subj_short, subj_full = subject_of(fp)
        ch = doc.get("chapter", label)
        title = doc["title"]                       # 例: "第3章 熱伝導の基礎"
        short = title.split(" ", 1)[-1].replace(" ", "") if " " in title else title
        outdir = os.path.join(CAE, "アプリ", subj_short + grade)
        os.makedirs(outdir, exist_ok=True)
        hp = os.path.join(TMP, f"formula_{subj_short}{grade}_ch{ch}.html")
        open(hp, "w", encoding="utf-8").write(build_html(doc, subj_full))
        out = os.path.join(outdir, f"{subj_short}{grade}_公式用語_第{ch}章_{short}.pdf")
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
