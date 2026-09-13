# -*- coding: utf-8 -*-
"""
build_preview.py — 任意の問題JSONから「ブラウザ確認用の自己完結HTML」を生成する恒久ツール。

用途:
  問題ファイル(content/questions/*.json)を、数式(MathJax)・図解(base64埋め込み)・
  【基礎/考え方/計算/ポイント/引っかけ】の節整形つきで1枚のHTMLにする。
  出力HTMLを Artifact ツールで publish すればブラウザ(別端末含む)で確認できる。
  ※publish は本体(Claude)が Artifact ツールで行う。本スクリプトはHTML生成まで。

使い方:
  python tools/build_preview.py content/questions/solid1-08-element-technology.json
  python tools/build_preview.py 8            # 2級の章番号(build_pdfs.py の FILES 経由)でも可
  複数指定可。無指定なら全 content/questions/*.json を1枚ずつ生成。
  出力先: <CAE>/preview/<jsonのstem>.html （絶対パスを表示）

図解:
  各問の figureImage キーがあり assets/figures/<key>.png が存在すれば、解説パネル冒頭に
  base64 で埋め込む(figureHint をキャプションに)。ゆえに単体HTMLで図も見える。
"""
import json, os, sys, base64, glob

TOOLS = os.path.dirname(os.path.abspath(__file__))
CAE = os.path.dirname(TOOLS)
FIGDIR = os.path.join(CAE, "assets", "figures")
OUTDIR = os.path.join(CAE, "preview")

# 2級の章番号→ファイル対応(build_pdfs.py と同じ辞書)。数字引数を許すため。
FILES = {
    1: "math-basics.json", 2: "solid-basics.json", 3: "heat-basics.json",
    4: "fem-basics.json", 5: "fem-practice.json", 6: "numerical-basics.json",
    7: "element-tech.json", 8: "modeling-basics.json", 9: "boundary-conditions.json",
    10: "prepost-basics.json", 11: "verification-basics.json",
    12: "computer-basics.json", 13: "ethics.json",
}

TEMPLATE = r"""<title>%%TITLE%%</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Zen+Kaku+Gothic+New:wght@500;700&family=Roboto+Mono:wght@500&display=swap">
<style>
:root{
  --ground:#f5f7fa; --surface:#ffffff; --surface-2:#eef2f6;
  --ink:#1a2027; --muted:#5b6673; --faint:#8792a0;
  --accent:#2b6c8f; --accent-soft:#e3eef4;
  --ok:#1f8a54; --ok-soft:#e4f4ea; --ok-border:#bfe3cd;
  --border:#e2e7ee; --border-strong:#d2d9e2;
  --shadow:0 1px 2px rgba(20,30,45,.05),0 6px 18px rgba(20,30,45,.05);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0f1319; --surface:#171d25; --surface-2:#1f2731;
    --ink:#e7ecf2; --muted:#9aa6b3; --faint:#6f7c8a;
    --accent:#5aa7c9; --accent-soft:#1d2e39;
    --ok:#46c088; --ok-soft:#16362a; --ok-border:#2c5a45;
    --border:#262e39; --border-strong:#333d4a;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"]{
  --ground:#0f1319; --surface:#171d25; --surface-2:#1f2731;
  --ink:#e7ecf2; --muted:#9aa6b3; --faint:#6f7c8a;
  --accent:#5aa7c9; --accent-soft:#1d2e39;
  --ok:#46c088; --ok-soft:#16362a; --ok-border:#2c5a45;
  --border:#262e39; --border-strong:#333d4a;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 8px 22px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
body{background:var(--ground); color:var(--ink);
  font-family:"Noto Sans JP",system-ui,sans-serif; line-height:1.75;
  margin:0; padding-block:40px 72px; -webkit-font-smoothing:antialiased;}
.wrap{max-width:760px; margin:0 auto; padding-inline:18px;}
header{margin-bottom:28px;}
.eyebrow{font-family:"Roboto Mono",monospace; font-size:12px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent); font-weight:500; margin:0 0 10px;}
h1{font-family:"Zen Kaku Gothic New",sans-serif; font-weight:700;
  font-size:clamp(26px,5vw,34px); line-height:1.25; margin:0; text-wrap:balance; letter-spacing:.01em;}
.sub{color:var(--muted); margin:10px 0 0; font-size:15px;}
.meta-row{display:flex; flex-wrap:wrap; gap:8px; margin-top:18px;}
.pill{font-size:12.5px; padding:4px 11px; border-radius:999px; background:var(--surface-2);
  color:var(--muted); border:1px solid var(--border); font-weight:500;}
.pill.strong{background:var(--accent-soft); color:var(--accent); border-color:transparent;}
.toolbar{display:flex; gap:10px; align-items:center; margin:22px 0 4px;}
button.ghost{font-family:inherit; font-size:13.5px; font-weight:500; cursor:pointer;
  color:var(--accent); background:transparent; border:1px solid var(--border-strong);
  padding:8px 15px; border-radius:9px; transition:background .15s,border-color .15s;}
button.ghost:hover{background:var(--accent-soft); border-color:var(--accent);}
button.ghost:focus-visible{outline:2px solid var(--accent); outline-offset:2px;}
.card{background:var(--surface); border:1px solid var(--border); border-radius:14px;
  padding:24px 24px 22px; margin-top:20px; box-shadow:var(--shadow);}
.card-head{display:flex; align-items:center; gap:12px; margin-bottom:6px; flex-wrap:wrap;}
.num{font-family:"Roboto Mono",monospace; font-weight:500; font-size:14px; color:#fff;
  background:var(--accent); padding:3px 10px; border-radius:7px; font-variant-numeric:tabular-nums; letter-spacing:.02em;}
.topic{font-size:12.5px; color:var(--muted);}
.diff{margin-left:auto; font-size:12px; color:var(--faint); white-space:nowrap;}
.diff b{color:var(--accent); font-weight:700; letter-spacing:.08em;}
.q-title{font-family:"Zen Kaku Gothic New",sans-serif; font-weight:700; font-size:19px;
  margin:4px 0 12px; line-height:1.4; text-wrap:balance;}
.q-body{font-size:15.5px; margin:0 0 16px; color:var(--ink);}
ol.choices{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:9px;}
ol.choices li{display:flex; gap:11px; align-items:flex-start; padding:11px 14px;
  border:1px solid var(--border); border-radius:10px; background:var(--surface);
  font-size:15px; transition:background .18s,border-color .18s;}
.mark{font-weight:700; color:var(--muted); flex:none; font-size:16px; line-height:1.5;
  font-family:"Zen Kaku Gothic New",sans-serif;}
.card.revealed li.correct{background:var(--ok-soft); border-color:var(--ok-border);}
.card.revealed li.correct .mark{color:var(--ok);}
.card.revealed li.correct::after{content:"正解"; margin-left:auto; align-self:center; flex:none;
  font-size:11.5px; font-weight:700; color:var(--ok); background:var(--surface);
  border:1px solid var(--ok-border); padding:2px 8px; border-radius:999px; letter-spacing:.05em;}
.reveal-btn{margin-top:16px;}
.explain{margin-top:18px; padding-top:18px; border-top:1px dashed var(--border-strong);}
.figure{margin:0 0 18px; text-align:center;}
.figure img{max-width:100%; border:1px solid var(--border); border-radius:10px; background:#fff;}
.figure figcaption{font-size:12.5px; color:var(--faint); margin-top:7px;}
.ans-line{font-family:"Zen Kaku Gothic New",sans-serif; font-weight:700; font-size:15px;
  color:var(--ok); margin:0 0 14px; display:flex; align-items:center; gap:8px;}
.ans-line .chip{font-family:"Roboto Mono",monospace; background:var(--ok); color:#fff;
  padding:2px 9px; border-radius:6px; font-size:13px;}
.exp-block{margin:0 0 12px;}
.exp-block:last-child{margin-bottom:0;}
.exp-label{display:inline-block; font-family:"Zen Kaku Gothic New",sans-serif; font-weight:700;
  font-size:12.5px; color:var(--accent); background:var(--accent-soft); padding:2px 10px;
  border-radius:6px; margin-bottom:5px; letter-spacing:.03em;}
.exp-text{font-size:14.5px; color:var(--ink); margin:0; line-height:1.85;}
mjx-container{overflow-x:auto; overflow-y:hidden; max-width:100%;}
footer{margin-top:36px; color:var(--faint); font-size:12.5px; text-align:center; line-height:1.7;}
</style>
<div class="wrap">
  <header>
    <p class="eyebrow">%%EYEBROW%%</p>
    <h1>%%H1%%</h1>
    <p class="sub">%%SUB%%</p>
    <div class="meta-row" id="metaRow"></div>
    <div class="toolbar"><button class="ghost" id="toggleAll" aria-pressed="false">解答をすべて表示</button></div>
  </header>
  <main id="list"></main>
  <footer>確認用プレビュー ／ 元データ: %%FILENAME%%</footer>
</div>
<script>
const DATA = %%DATA%%;
const FIGS = %%FIGS%%;
const MARKS = ["①","②","③","④","⑤","⑥"];
const DIFF = {1:"基礎",2:"標準",3:"応用"};
function diffDots(n){let s="";for(let i=1;i<=3;i++)s+=(i<=n?"●":"○");return s;}
function esc(t){return (t==null?"":String(t)).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function renderExplanation(text){
  const lines=(text||"").split("\n").filter(l=>l.trim().length);
  return lines.map(line=>{
    const m=line.match(/^【(.+?)】([\s\S]*)$/);
    if(m) return `<div class="exp-block"><span class="exp-label">${esc(m[1])}</span><p class="exp-text">${esc(m[2].trim())}</p></div>`;
    return `<div class="exp-block"><p class="exp-text">${esc(line)}</p></div>`;
  }).join("");
}
function figureHtml(q){
  const key=q.figureImage; if(!key||!FIGS[key]) return "";
  const cap=q.figureHint?`<figcaption>${esc(q.figureHint)}</figcaption>`:"";
  return `<figure class="figure"><img alt="図: ${esc(q.title)}" src="${FIGS[key]}">${cap}</figure>`;
}
function buildCard(q){
  const el=document.createElement("article"); el.className="card";
  const choices=q.choices.map((c,i)=>{
    const correct=(i+1)===q.answer?" correct":"";
    return `<li class="c${correct}"><span class="mark">${MARKS[i]}</span><span>${esc(c)}</span></li>`;
  }).join("");
  el.innerHTML=`
    <div class="card-head">
      <span class="num">${esc(q.number)}</span>
      <span class="topic">${esc(q.topic)}</span>
      <span class="diff">難易度 <b>${diffDots(q.difficulty)}</b> ${DIFF[q.difficulty]||""}</span>
    </div>
    <h2 class="q-title">${esc(q.title)}</h2>
    <p class="q-body">${esc(q.question)}</p>
    <ol class="choices">${choices}</ol>
    <button class="ghost reveal-btn" aria-pressed="false">答えと解説</button>
    <div class="explain" hidden>
      ${figureHtml(q)}
      <p class="ans-line">正解 <span class="chip">${MARKS[q.answer-1]}</span></p>
      ${renderExplanation(q.explanation)}
    </div>`;
  const btn=el.querySelector(".reveal-btn"), exp=el.querySelector(".explain");
  btn.addEventListener("click",()=>{
    const open=exp.hidden; exp.hidden=!open;
    el.classList.toggle("revealed",open);
    btn.textContent=open?"解説を隠す":"答えと解説";
    btn.setAttribute("aria-pressed",open?"true":"false");
  });
  return el;
}
const list=document.getElementById("list");
DATA.questions.forEach(q=>list.appendChild(buildCard(q)));
const dist={1:0,2:0,3:0,4:0}; DATA.questions.forEach(q=>{if(dist[q.answer]!=null)dist[q.answer]++;});
const nFig=DATA.questions.filter(q=>q.figureImage&&FIGS[q.figureImage]).length;
document.getElementById("metaRow").innerHTML=
  `<span class="pill strong">全 ${DATA.questions.length} 問</span>`+
  `<span class="pill">正解分布 ①${dist[1]}/②${dist[2]}/③${dist[3]}/④${dist[4]}</span>`+
  `<span class="pill">図解 ${nFig} 問</span>`+
  `<span class="pill">完全オリジナル</span>`;
const allBtn=document.getElementById("toggleAll");
allBtn.addEventListener("click",()=>{
  const open=allBtn.getAttribute("aria-pressed")!=="true";
  document.querySelectorAll(".card").forEach(card=>{
    const exp=card.querySelector(".explain"), b=card.querySelector(".reveal-btn");
    exp.hidden=!open; card.classList.toggle("revealed",open);
    b.textContent=open?"解説を隠す":"答えと解説"; b.setAttribute("aria-pressed",open?"true":"false");
  });
  allBtn.textContent=open?"解答をすべて隠す":"解答をすべて表示";
  allBtn.setAttribute("aria-pressed",open?"true":"false");
});
</script>
<script>window.MathJax={tex:{inlineMath:[["$","$"]]},svg:{fontCache:"global"},startup:{typeset:true}};</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js" async></script>
"""

def embed_figs(d):
    figs = {}
    for q in d.get("questions", []):
        key = q.get("figureImage")
        if not key or key in figs:
            continue
        p = os.path.join(FIGDIR, key + ".png")
        if os.path.exists(p):
            b = base64.b64encode(open(p, "rb").read()).decode("ascii")
            figs[key] = "data:image/png;base64," + b
    return figs

def build(jsonpath):
    d = json.load(open(jsonpath, encoding="utf-8"))
    meta = d.get("meta", {})
    stem = os.path.splitext(os.path.basename(jsonpath))[0]
    title = (meta.get("category") or stem)
    eyebrow = "計算力学技術者試験 · " + (meta.get("grade") or "")
    nums = [q.get("number", "") for q in d.get("questions", [])]
    rng = f"{nums[0]}〜{nums[-1]} " if nums else ""
    sub = f"{rng}作問プレビュー（完全オリジナル）"
    figs = embed_figs(d)
    html = (TEMPLATE
            .replace("%%TITLE%%", title)
            .replace("%%EYEBROW%%", eyebrow)
            .replace("%%H1%%", title)
            .replace("%%SUB%%", sub)
            .replace("%%FILENAME%%", os.path.basename(jsonpath))
            .replace("%%DATA%%", json.dumps(d, ensure_ascii=False))
            .replace("%%FIGS%%", json.dumps(figs, ensure_ascii=False)))
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, stem + ".html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"OK  {out}  ({len(d.get('questions',[]))}問, 図{len(figs)})")
    return out

def resolve(arg):
    if arg.isdigit():
        f = FILES.get(int(arg))
        if not f:
            print("unknown chapter:", arg); return None
        return os.path.join(CAE, "content", "questions", f)
    return arg if os.path.isabs(arg) else os.path.join(CAE, arg)

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        targets = sorted(glob.glob(os.path.join(CAE, "content", "questions", "*.json")))
    else:
        targets = [p for p in (resolve(a) for a in args) if p]
    for t in targets:
        build(t)
