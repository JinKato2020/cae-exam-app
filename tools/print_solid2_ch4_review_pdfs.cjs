const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/jwpsa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const root=path.resolve(__dirname,'..'),tmp=path.join(root,'tmp/pdfs/ch4_final');
 const tasks=JSON.parse(fs.readFileSync(path.join(tmp,'tasks.json'),'utf8'));
 const expected=JSON.parse(fs.readFileSync(path.join(tmp,'expected.json'),'utf8'));
 if(tasks.length!==2||tasks.some(t=>!t.pdf.includes('固体2級_第4章_')))throw Error('Chapter guard');
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu','--no-sandbox']});
 try{
  const results=[];
  for(const task of tasks.filter(t=>!process.argv.includes('--after-only')||t.mode==='回答後')){
   const page=await browser.newPage({viewport:{width:1200,height:1600}});const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(pathToFileURL(task.html).href,{waitUntil:'networkidle',timeout:60000});
   await page.waitForFunction(()=>window.MathJax?.startup?.promise,{timeout:30000});
   await page.evaluate(async()=>{await MathJax.startup.promise;await document.fonts.ready;});
   const facts=await page.evaluate(()=>({mathErrors:document.querySelectorAll('mjx-merror').length,figures:document.images.length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,sheets:document.querySelectorAll('.sheet').length,afterTags:document.querySelectorAll('.section-label').length,links:document.querySelectorAll('.term-link a').length,mathOverflows:[...document.querySelectorAll('mjx-container')].flatMap(el=>{const r=el.getBoundingClientRect(),p=el.closest('.sheet')||el.closest('.card');if(!p)return [];const b=p.getBoundingClientRect();return r.width>b.width-10?[{width:r.width,parent:b.width,formula:el.textContent.slice(0,50)}]:[];})}));
   if(facts.mathErrors||facts.brokenImages||errors.length)throw Error(JSON.stringify({facts,errors}));
   if(task.mode==='回答後'&&(facts.sheets!==expected.after_sheets||facts.figures!==expected.after_figures||facts.afterTags!==expected.after_tags||facts.links!==expected.links))throw Error('After counts');
   if(task.mode==='回答前'&&(facts.figures!==expected.before_figures||facts.afterTags||facts.links))throw Error('Before contains answer');
   const stagedDir=path.join(tmp,'print');fs.mkdirSync(stagedDir,{recursive:true});
   const staged=path.join(stagedDir,path.basename(task.pdf));
   const buffer=await page.pdf({format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false});
   fs.writeFileSync(staged,buffer);
   let installed=true,lockError=null;
   try{fs.copyFileSync(staged,task.pdf);}catch(e){
    try{fs.renameSync(staged,task.pdf);}catch(e2){installed=false;lockError=e2.code;}
   }
   results.push({mode:task.mode,...facts,bytes:buffer.length,installed,staged,lockError});await page.close();
  }
  fs.writeFileSync(path.join(tmp,'browser-checks.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
