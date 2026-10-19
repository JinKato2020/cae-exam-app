const fs=require('fs');
const path=require('path');
const {chromium}=require('C:/Users/jwpsa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const root=path.resolve(__dirname,'..');
  const qs=JSON.parse(fs.readFileSync(path.join(root,'content/questions/heat-basics.json'),'utf8'));
  const terms=JSON.parse(fs.readFileSync(path.join(root,'content/formulas/ch3.json'),'utf8'));
  const input=[...qs.questions.flatMap(q=>[q.question,...q.choices,q.explanation]),...terms.items.flatMap(it=>[it.formula||'',it.body||'',it.example||''])];
  const expressions=input.flatMap(text=>[...text.matchAll(/\$([^$]+)\$/g)].map(m=>m[1]));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu','--no-sandbox']});
  try{
    const page=await browser.newPage();page.setDefaultTimeout(20000);
    await page.addScriptTag({url:'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js'});
    const errors=await page.evaluate(exprs=>exprs.flatMap(expr=>{try{window.katex.renderToString(expr,{throwOnError:true,strict:'error'});return [];}catch(e){return [{expr,error:e.message}];}}),expressions);
    if(errors.length)throw Error(JSON.stringify(errors));
    fs.writeFileSync(path.join(root,'output/固体2級_第3章_反映結果/KaTeX検証.json'),JSON.stringify({version:'0.16.9',expressions:expressions.length,parseErrors:errors},null,2));
    console.log(`KaTeX 0.16.9 PASS: ${expressions.length} expressions from all 17 questions and 13 glossary items.`);
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
