# -*- coding: utf-8 -*-
"""各章の問題・解答・解説・図を1章=1PDFで出力(セッション直下=プロジェクト直下)。
数式=MathJax(SVG)、図=base64埋め込み。Edge headless の print-to-pdf を使用。
使い方: python tools/build_pdfs.py [章番号...]   (無指定なら1〜5章)
再利用可能な恒久ツール。新章を作ったら CHAPTERS に足すだけ。"""
import json, os, base64, html, subprocess, sys, glob

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(CAE, "content", "questions")
FIG = os.path.join(CAE, "assets", "figures")
TMP = os.path.join(CAE, "tools", "_pdftmp")
OUTDIR = os.path.join(CAE, "アプリ", "2級")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

# 章番号 → 問題ファイル
FILES = {1:"math-basics.json",2:"solid-basics.json",3:"heat-basics.json",
         4:"fem-basics.json",5:"fem-practice.json",6:"numerical-basics.json",7:"element-tech.json",
         8:"modeling-basics.json",9:"boundary-conditions.json",
         10:"prepost-basics.json",11:"verification-basics.json",
         12:"computer-basics.json",13:"ethics.json"}

def esc(s): return html.escape(s, quote=False)

def img_datauri(key):
    p=os.path.join(FIG,key+".png")
    if not os.path.exists(p): return None
    b=base64.b64encode(open(p,"rb").read()).decode()
    return "data:image/png;base64,"+b

def expl_html(s):
    return "".join(f"<div class='eline'>{esc(l.strip())}</div>" for l in s.split("\n") if l.strip())

def card(q):
    fig=""
    if q.get("figureImage"):
        uri=img_datauri(q["figureImage"])
        if uri: fig=f"<div class='fig'><img src='{uri}'></div>"
    ch="".join(f"<li class='{'ok' if i+1==q['answer'] else ''}'>{esc(c)}</li>" for i,c in enumerate(q["choices"]))
    return f"""<div class='card'>
      <div class='chead'><span class='num'>{esc(q['number'])}</span> <span class='ttl'>{esc(q['title'])}</span>
        <span class='meta'>難{q.get('difficulty','?')}・{esc(q.get('topic',''))}</span></div>
      <div class='q'>{esc(q['question'])}</div>{fig}
      <ol class='choices'>{ch}</ol>
      <div class='ans'><b>正解 : {q['answer']}</b></div>
      <div class='exp'>{expl_html(q['explanation'])}</div>
    </div>"""

def subject_of(path_or_name):
    """ファイル名から分野を判別: vib*→振動 / thermal*→熱流体 / それ以外(solid*・ch*)→固体。"""
    b=os.path.basename(path_or_name).lower()
    if "vib" in b: return "振動","振動"
    if "thermal" in b: return "熱流体","熱流体力学"
    return "固体","固体力学"

def versioned_out(outdir, stem, ext=".pdf"):
    """作成/修正のたびに版を残す。初版=<stem><ext>、以降の保存は<stem>_r1,_r2…と自動採番。
    既存ファイルは上書きしない=履歴を保全。最新版=最大の r 番号(初版のみなら無印)。"""
    base = os.path.join(outdir, stem + ext)
    if not os.path.exists(base):
        return base
    n = 0
    pre = stem + "_r"
    for f in os.listdir(outdir):
        if f.startswith(pre) and f.endswith(ext):
            tail = f[len(pre):-len(ext)]
            if tail.isdigit():
                n = max(n, int(tail))
    return os.path.join(outdir, f"{stem}_r{n+1}{ext}")

def build_html(data, subject_full="固体力学"):
    meta=data["meta"]
    grade="1級" if "1級" in meta.get("grade","") else "2級"
    cat=meta["category"]; ch=meta.get("chapter")
    cards="".join(card(q) for q in data["questions"])
    return grade, ch, cat, f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
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
<div class="sub">CAE計算力学技術者 {subject_full}{grade}・オリジナル問題（問題／解答／解説／図）</div>
{cards}
</body></html>"""

def main():
    # 引数: 数字=2級のch番号(従来通り) / ファイル名stem(例 solid1-01-nonlinear-stress-strain)=そのJSONを1本ビルド。
    # 無指定なら2級 ch1〜13。級は各JSONの meta.grade で判別し 出力先 アプリ/<級>/ を切替。
    args=sys.argv[1:]
    tasks=[]  # 問題JSONの絶対パス
    if not args:
        tasks=[os.path.join(QDIR,FILES[ch]) for ch in range(1,14)]
    else:
        for a in args:
            if a.isdigit():
                tasks.append(os.path.join(QDIR,FILES[int(a)]))
            else:
                stem=a[:-5] if a.endswith(".json") else a
                tasks.append(os.path.join(QDIR,f"{stem}.json"))
    os.makedirs(TMP,exist_ok=True)
    for fp in tasks:
        if not os.path.exists(fp):
            print(f"{fp}: SKIP (no json)"); continue
        data=json.load(open(fp,encoding="utf-8"))
        subj_short,subj_full=subject_of(fp)
        grade,ch,cat,doc=build_html(data,subj_full)
        short=cat.split(" ",1)[-1].replace(" ","") if " " in cat else cat
        outdir=os.path.join(CAE,"アプリ",subj_short+grade)
        os.makedirs(outdir,exist_ok=True)
        hp=os.path.join(TMP,f"q_{subj_short}{grade}_ch{ch}.html")
        open(hp,"w",encoding="utf-8").write(doc)
        out=versioned_out(outdir, f"{subj_short}{grade}_第{ch}章_{short}")
        url="file:///"+hp.replace("\\","/")
        cmd=[EDGE,"--headless=new","--disable-gpu","--no-sandbox",
             f"--print-to-pdf={out}","--print-to-pdf-no-header",
             "--virtual-time-budget=25000","--run-all-compositor-stages-before-draw",url]
        r=subprocess.run(cmd,capture_output=True,timeout=120)
        ok=os.path.exists(out)
        print(f"ch{ch}({grade}): {'OK' if ok else 'FAIL'}  {out}  ({os.path.getsize(out)//1024 if ok else 0} KB)")
    print("PDF出力完了")

if __name__=="__main__":
    main()
