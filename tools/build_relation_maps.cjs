// Solid concept maps: semantic source -> existing HTML/PNG keys -> archive + offline shards.
// Usage: node tools/build_relation_maps.cjs [--key map_solid_1_ch2] [--check-only]
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { execFileSync } = require('child_process');
const root = path.resolve(__dirname, '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8').replace(/^\uFEFF/, ''));
const data = read('相関図/solid_relations.json');
const catalog = read('content/catalog.json').fields.find(f => f.id === 'solid');
const keyOf = m => `map_solid_${m.grade}_${m.chapter === 'all' ? 'all' : 'ch' + m.chapter}`;
const fail = message => { throw new Error(message); };
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const selected = process.argv.includes('--key') ? process.argv[process.argv.indexOf('--key') + 1] : null;
const maps = data.maps.filter(m => !selected || keyOf(m) === selected);
if (!maps.length) fail('No maps selected');

function refsOf(node) { return node.refs ? node.refs.split(',') : []; }
function shortRefs(refs, all) {
  if (!refs) return '';
  const a = refs.split(',');
  if (all) return '第' + a.join('・') + '章';
  const result = [];
  for (let i = 0; i < a.length; i++) {
    const first = a[i]; let last = first;
    const match = first.match(/^(.*-)(\d+)$/);
    if (match) while (i + 1 < a.length && a[i + 1] === match[1] + (+last.split('-').pop() + 1)) last = a[++i];
    result.push(first === last ? first : first + '〜' + last);
  }
  return result.join('、');
}
function validate(m) {
  const grade = catalog.grades.find(g => g.id === 'g' + m.grade);
  const chapter = grade.chapters.find(c => c.id === 'ch' + m.chapter);
  const validRefs = new Set(m.chapter === 'all' ? grade.chapters.map(c => c.id.slice(2)) : read(chapter.content).questions.map(q => q.number));
  const covered = new Set();
  for (const panel of m.panels) {
    const nodes = panel.rows.flat(), byId = new Map(nodes.map(n => [n.id, n]));
    if (byId.size !== nodes.length) fail(keyOf(m) + ': duplicate node');
    if (panel.rows.some(r => !r.length || r.length > 2)) fail('Use one or two nodes per rank');
    for (const n of nodes) for (const ref of refsOf(n)) {
      if (!validRefs.has(ref)) fail(keyOf(m) + ': unknown reference ' + ref);
      covered.add(ref);
    }
    const connected = new Set();
    for (const [from, to, label] of panel.edges) {
      if (!byId.has(from) || !byId.has(to) || !label) fail(keyOf(m) + ': invalid relation');
      const a = panel.rows.findIndex(r => r.some(n => n.id === from));
      const b = panel.rows.findIndex(r => r.some(n => n.id === to));
      if (b !== a + 1) fail(keyOf(m) + ': relation must join adjacent ranks');
      connected.add(from); connected.add(to);
    }
    if (nodes.some(n => !connected.has(n.id))) fail(keyOf(m) + ': isolated classification node');
  }
  const missing = [...validRefs].filter(r => !covered.has(r));
  if (missing.length) fail(keyOf(m) + ': missing questions ' + missing.join(','));
  return { nodes: m.panels.flatMap(p => p.rows.flat()).length, relations: m.panels.reduce((s,p) => s + p.edges.length, 0), questions: covered.size };
}

const css = `
*{box-sizing:border-box}html,body{margin:0;background:#fff;color:#1F3A65;font-family:Meiryo,'メイリオ',Arial,sans-serif}
main{width:600px;padding:24px}header{padding:0 0 22px;border-bottom:3px solid #1F3A65}
.course{font-size:20px;font-weight:bold;margin:0 0 10px}h1{font-size:32px;line-height:1.5;margin:0;text-wrap:balance}
.how{font-size:19px;line-height:1.7;margin:14px 0 0;color:#1F3A65}.legend{font-size:18px;line-height:1.65;margin:12px 0 0}
section{margin-top:30px}h2{font-size:25px;line-height:1.6;margin:0 0 24px;padding:0 0 0 12px;border-left:5px solid #C82D2D;text-wrap:balance}
.graph{position:relative}.row{display:flex;justify-content:center;gap:24px;align-items:stretch;position:relative}
.row+.row{margin-top:112px}.node{width:264px;padding:16px 16px 14px;border:2px solid #1F3A65;border-radius:12px;background:#E1E7F2;position:relative;z-index:1}
.row.single .node{width:440px}.node h3{font-size:24px;line-height:1.55;margin:0 0 10px;font-weight:bold;overflow-wrap:anywhere}
.node p{font-size:22px;line-height:1.7;margin:0;overflow-wrap:anywhere}.refs{display:block;font-size:18px;line-height:1.65;margin-top:12px;padding-top:8px;border-top:1px solid #888888;overflow-wrap:anywhere}
.row:last-of-type .node{border-color:#C82D2D}.edge-label{position:absolute;transform:translate(-50%,-50%);font-size:19px;line-height:1.5;text-align:center;background:#fff;padding:3px 8px;z-index:2;max-width:240px;width:max-content}
.edge-label.compare{color:#888888}.edges{position:absolute;inset:0;width:100%;height:100%;overflow:visible;z-index:0;pointer-events:none}
.note{font-size:20px;line-height:1.8;margin:20px 0 0;padding:14px 0;border-top:1px solid #888888}
footer{font-size:18px;line-height:1.7;margin-top:28px;padding-top:16px;border-top:2px solid #1F3A65}
`;

// This function is serialized into the local HTML; the PNG and editable preview share one layout.
function drawRelations() {
  const ns = 'http://www.w3.org/2000/svg';
  const issues = [];
  document.querySelectorAll('.graph').forEach((graph, index) => {
    graph.querySelectorAll('.edges,.edge-label').forEach(el => el.remove());
    const svg = document.createElementNS(ns, 'svg'); svg.classList.add('edges');
    svg.setAttribute('aria-hidden', 'true');
    const bounds = graph.getBoundingClientRect();
    svg.setAttribute('viewBox', `0 0 ${bounds.width} ${bounds.height}`);
    svg.innerHTML = `<defs><marker id="arrow${index}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 Z" fill="#1F3A65"/></marker></defs>`;
    graph.prepend(svg);
    const relations = JSON.parse(graph.dataset.edges);
    const points = [];
    relations.forEach(([from, to, label, kind]) => {
      const a = graph.querySelector(`[data-id="${from}"]`).getBoundingClientRect();
      const b = graph.querySelector(`[data-id="${to}"]`).getBoundingClientRect();
      const x1 = a.x + a.width/2 - bounds.x, x2 = b.x + b.width/2 - bounds.x;
      const y1 = a.bottom - bounds.y + 3, y2 = b.top - bounds.y - 6;
      const mid = (y1 + y2)/2;
      const line = document.createElementNS(ns, 'path');
      line.setAttribute('d', `M ${x1} ${y1} L ${x1} ${y1+18} L ${x2} ${y2-18} L ${x2} ${y2}`);
      line.setAttribute('fill','none'); line.setAttribute('stroke',kind === 'compare' ? '#888888' : '#1F3A65'); line.setAttribute('stroke-width','2.5');
      if (kind === 'compare') line.setAttribute('stroke-dasharray','7 5'); else line.setAttribute('marker-end',`url(#arrow${index})`);
      svg.append(line);
      const caption = document.createElement('span'); caption.className = 'edge-label' + (kind === 'compare' ? ' compare' : ''); caption.textContent = label;
      // Separate branch captions into their own half of the gap, without detaching from the line.
      const isFork = relations.filter(e => e[0] === from).length > 1;
      const isJoin = relations.filter(e => e[1] === to).length > 1;
      const x = isFork ? x2 : isJoin ? x1 : (x1+x2)/2;
      caption.style.left = x + 'px'; caption.style.top = mid + 'px';
      graph.append(caption);
      points.push({caption,from,to});
    });
    const rect = el => el.getBoundingClientRect();
    const intersects = (a,b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
    points.forEach(({caption,from,to}, i) => {
      const b = rect(caption);
      if (b.left < bounds.left || b.right > bounds.right) issues.push(`edge outside graph: ${from}/${to}`);
      for(const node of graph.querySelectorAll('.node')) if(intersects(b,rect(node))) issues.push(`edge overlaps node: ${from}/${to}`);
      for(const prev of points.slice(0,i)) if(intersects(b,rect(prev.caption))) issues.push(`edge labels overlap: ${from}/${to}`);
    });
  });
  for(const el of document.querySelectorAll('.node,h1,h2,.note,.refs')) if(el.scrollWidth > el.clientWidth+1) issues.push('text overflow: '+el.textContent.slice(0,30));
  window.relationMapIssues = issues; window.relationMapReady = true;
}

function htmlOf(m) {
  const course = `固体${m.grade}級 · ${m.chapter === 'all' ? '全章' : '第' + m.chapter + '章'}`;
  const comparison = m.panels.some(p => p.edges.some(e => e[3] === 'compare'));
  return `<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(course+' 相関図')}</title><style>${css}</style><main>
<header><p class="course">${esc(course)} ／ 相関図</p><h1>${esc(m.title)}</h1><p class="legend">矢印の言葉で、項目どうしの関係をたどれます。${comparison ? '<br>点線は、比べて区別する関係です。' : ''}</p></header>
${m.panels.map(p => `<section><h2>${esc(p.title)}</h2><div class="graph" data-edges="${esc(JSON.stringify(p.edges))}">${p.rows.map(r => `<div class="row ${r.length===1?'single':''}">${r.map(n => `<article class="node" data-id="${esc(n.id)}"><h3>${esc(n.title)}</h3><p>${esc(n.body)}</p>${n.refs?`<span class="refs">${esc(shortRefs(n.refs,m.chapter==='all'))}</span>`:''}</article>`).join('')}</div>`).join('')}</div>${p.note?`<p class="note">${esc(p.note)}</p>`:''}</section>`).join('')}
<footer>線の言葉が、二つの項目の関係を表します。<br>番号から対応する章・問題へ戻って確認できます。</footer></main><script>${drawRelations.toString()};document.fonts.ready.then(drawRelations);</script></html>`;
}

(async () => {
  const counts = maps.map(m => ({key:keyOf(m), ...validate(m)}));
  if(process.argv.includes('--check-only')) { console.log(JSON.stringify({maps:counts.length,details:counts})); return; }
  let chromium;
  try { ({chromium} = require('playwright')); }
  catch { ({chromium} = require(path.join(process.env.USERPROFILE,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'))); }
  const browser = await chromium.launch({headless:true, executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', args:['--disable-gpu']});
  const staged = path.join(root,'tmp/relation-maps'); fs.mkdirSync(staged,{recursive:true});
  const outputs=[];
  try {
    for(const m of maps) {
      const dir=path.join(root,`相関図/固体${m.grade}級`);
      const prefix=`固体${m.grade}級_${m.chapter==='all'?'全章_':'第'+m.chapter+'章_'}`;
      const names=fs.readdirSync(dir).filter(n=>n.startsWith(prefix)&&n.endsWith('相関図プレビュー.html'));
      if(names.length!==1) fail('Ambiguous source path: '+prefix);
      const html=path.join(dir,names[0]), png=path.join(staged,keyOf(m)+'.png');
      fs.writeFileSync(html,htmlOf(m),'utf8');
      const page=await browser.newPage({viewport:{width:600,height:900},deviceScaleFactor:2});
      const errors=[]; page.on('pageerror',e=>errors.push(e.message));
      await page.goto(pathToFileURL(html).href,{waitUntil:'load'});
      await page.waitForFunction(()=>window.relationMapReady);
      const issues=await page.evaluate(()=>window.relationMapIssues);
      if(issues.length || errors.length) fail(keyOf(m)+': '+JSON.stringify({issues,errors}));
      await page.locator('main').screenshot({path:png});
      outputs.push({map:m,png,html}); await page.close();
    }
  } finally { await browser.close(); }
  // Install only after all selected maps passed the relation, reference and layout checks.
  for(const o of outputs) fs.copyFileSync(o.png,path.join(root,'assets/figures',keyOf(o.map)+'.png'));
  execFileSync('python',['-c', 'import sys; from pathlib import Path; from tools.compress_figures import compress_bytes\nfor name in sys.argv[1:]:\n p=Path(name); data=compress_bytes(str(p))\n if data is not None: p.write_bytes(data)', ...outputs.map(o=>path.join(root,'assets/figures',keyOf(o.map)+'.png'))],{cwd:root,stdio:'pipe'});
  for(const grade of new Set(maps.map(m=>m.grade))) {
    const entries={};
    for(const m of data.maps.filter(m=>m.grade===grade)) {
      const png=path.join(root,'assets/figures',keyOf(m)+'.png');
      entries[keyOf(m)]='data:image/png;base64,'+fs.readFileSync(png).toString('base64');
      if(maps.includes(m)) {
        const folder=m.chapter==='all'?'全章':'第'+String(m.chapter).padStart(2,'0')+'章';
        const basename=(m.chapter==='all'?'全章':m.chapter+'章')+'_after_相関図.png';
        const archive=path.join(root,'図',`固体${grade}級`,folder,basename);
        fs.mkdirSync(path.dirname(archive),{recursive:true}); fs.copyFileSync(png,archive);
      }
    }
    fs.writeFileSync(path.join(root,`src/mapData/solid_${grade}.ts`), '// 自動生成: tools/build_relation_maps.cjs。相関図PNGのオフライン表示。\n/* eslint-disable */\nconst maps: Record<string, string> = '+JSON.stringify(entries,null,2)+';\nexport default maps;\n','utf8');
  }
  console.log(JSON.stringify({maps:outputs.length,details:counts}));
})().catch(error=>{console.error(error.message);process.exitCode=1;});
