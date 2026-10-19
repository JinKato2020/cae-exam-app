const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/jwpsa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const qs=JSON.parse(fs.readFileSync(path.join(root,'content/questions/fem-basics.json'),'utf8'));
 const terms=JSON.parse(fs.readFileSync(path.join(root,'content/formulas/ch4.json'),'utf8'));
 const expressions=[...qs.questions.flatMap(q=>[q.question,...q.choices,q.explanation]),...terms.items.flatMap(i=>[i.formula||'',i.body||'',i.example||''])].flatMap(s=>[...s.matchAll(/\$([^$]+)\$/g)].map(m=>m[1]));
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu','--no-sandbox']});
 try{const p=await browser.newPage();await p.addScriptTag({url:'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js'});
 const errors=await p.evaluate(es=>es.flatMap(expr=>{try{katex.renderToString(expr,{throwOnError:true,strict:'error'});return [];}catch(e){return [{expr,error:e.message}];}}),expressions);
 fs.writeFileSync(path.join(root,'output/固体2級_第4章_反映結果/KaTeX検証.json'),JSON.stringify({version:'0.16.9',expressions:expressions.length,errors},null,2));
 if(errors.length)throw Error(JSON.stringify(errors));console.log(`PASS ${expressions.length} expressions`);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
