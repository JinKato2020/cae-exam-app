const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Users/jwpsa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
  const root=path.resolve(__dirname,'..');
  const tasks=JSON.parse(fs.readFileSync(path.join(root,'tmp/pdfs/ch3_final/tasks.json'),'utf8'));
  if(tasks.length!==2 || tasks.some(t=>!t.pdf.includes('固体2級_第3章_')))throw Error('Chapter-only guard');
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--disable-gpu','--no-sandbox']});
  try {
    const diagnostics=[];
    for(const task of tasks) {
      const page=await browser.newPage({viewport:{width:1200,height:1600}});
      const errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto(pathToFileURL(task.html).href,{waitUntil:'networkidle',timeout:60000});
      await page.waitForFunction(()=>window.MathJax && window.MathJax.startup && window.MathJax.startup.promise,{timeout:30000});
      await page.evaluate(async()=>{await MathJax.startup.promise;await document.fonts.ready;});
      const facts=await page.evaluate(()=>({math:document.querySelectorAll('mjx-container').length,mathErrors:document.querySelectorAll('mjx-merror').length,figures:document.images.length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length,sheets:document.querySelectorAll('.sheet').length,afterTags:document.querySelectorAll('.section-label').length}));
      if(facts.mathErrors||facts.brokenImages||errors.length)throw Error(JSON.stringify({mode:task.mode,facts,errors}));
      if(task.mode==='回答後' && (facts.figures!==18||facts.sheets!==36||facts.afterTags!==68))throw Error('After content count mismatch');
      if(task.mode==='回答前' && (facts.figures!==6||facts.afterTags))throw Error('Spoiler in before');
      await page.pdf({path:task.pdf,format:'A4',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false});
      diagnostics.push({mode:task.mode,...facts,bytes:fs.statSync(task.pdf).size});
      console.log(JSON.stringify(diagnostics.at(-1)));
      await page.close();
    }
    fs.writeFileSync(path.join(root,'tmp/pdfs/ch3_final/browser-checks.json'),JSON.stringify(diagnostics,null,2));
  }finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
