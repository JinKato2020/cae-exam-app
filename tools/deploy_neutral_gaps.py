#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ギャップ問(solid2_chNN納品図が無い問)へ旧図(ChatGPT中立SVG)を既存figureImageキーのPNGへ並列描画(2026-10-09)。
旧図= 図\固体2級\旧図\*.zip 内 svg/fig{番号}.svg(全問中立図)。figlib画像を置換(JSONキー不変=最小)。
描画= headless Chrome 2x・プロファイル隔離で並列(既定6並列)。恒久ツール。
使い方: python tools/deploy_neutral_gaps.py <章> [--write] [--workers N]
"""
import os,re,json,sys,glob,zipfile,tempfile,shutil,subprocess,time
from concurrent.futures import ThreadPoolExecutor
CAE=r"C:\Users\jwpsa\Documents\desktop\claude\CAE"
CHROME=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FIG=os.path.join(CAE,"assets","figures")
ROOT=os.path.join(CAE,"図","固体2級")
KYUZU=os.path.join(ROOT,"旧図")
QMAP={1:"math-basics",2:"solid-basics",3:"heat-basics",4:"fem-basics",5:"fem-practice",6:"numerical-basics",7:"element-tech",8:"modeling-basics",9:"boundary-conditions",10:"prepost-basics",11:"verification-basics",12:"computer-basics",13:"ethics"}
ch=int(sys.argv[1]); WRITE="--write" in sys.argv
workers=6
if "--workers" in sys.argv: workers=int(sys.argv[sys.argv.index("--workers")+1])

# 旧図 SVG を temp へ展開(num->svgpath)
TMP=tempfile.mkdtemp(prefix="kyuzu_")
kyu={}
for z in glob.glob(os.path.join(KYUZU,"*.zip")):
    with zipfile.ZipFile(z) as zf:
        for n in zf.namelist():
            m=re.match(r'svg/fig(\d+-\d+)\.svg$',n)
            if m:
                out=os.path.join(TMP,"fig%s.svg"%m.group(1))
                if not os.path.exists(out):
                    with zf.open(n) as src, open(out,'wb') as dst: dst.write(src.read())
                kyu[m.group(1)]=out

jpath=os.path.join(CAE,"content","questions",QMAP[ch]+".json")
data=json.load(open(jpath,encoding="utf-8"))
# solid2_chNN 納品(before/after)番号
nn="%02d"%ch
deliv=set()
for sub in ("before","after"):
    for x in glob.glob(os.path.join(ROOT,f"solid2_ch{nn}",sub,"*.svg")):
        deliv.add(os.path.basename(x)[:-4])

def viewbox(svg):
    s=open(svg,encoding="utf-8").read()
    m=re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"',s)
    return (int(float(m.group(1))),int(float(m.group(2)))) if m else (960,560)

def render(svgpath,key):
    w,h=viewbox(svgpath); out=os.path.join(FIG,key+".png")
    for _ in range(2):
        prof=tempfile.mkdtemp(prefix="png_"); t0=time.time()
        try:
            subprocess.run([CHROME,"--headless=new","--disable-gpu","--hide-scrollbars","--no-first-run",
                "--user-data-dir="+prof,"--default-background-color=FFFFFFFF","--force-device-scale-factor=2",
                "--screenshot="+out,"--window-size=%d,%d"%(w,h),
                os.path.abspath(svgpath).replace("\\","/")],capture_output=True,timeout=60)
        except Exception: pass
        finally: shutil.rmtree(prof,ignore_errors=True)
        if os.path.exists(out) and os.path.getmtime(out)>=t0-1: return True
    return False

# ギャップ問= 納品外 かつ 旧図あり かつ figureImageキーあり
jobs=[]; skip_nokey=[]; skip_nokyu=[]
for q in data["questions"]:
    num=q.get("number")
    if not num or not num.startswith("%d-"%ch): continue
    if num in deliv: continue           # 納品(revised)は対象外
    if num not in kyu: skip_nokyu.append(num); continue   # 旧図なし
    key=q.get("figureImage")
    if not key: skip_nokey.append(num); continue
    jobs.append((num,kyu[num],key))

print("ch%d: 納品(revised)=%d / ギャップ描画対象=%d / 旧図なし=%d / figキーなし=%d"%(ch,len(deliv),len(jobs),len(skip_nokyu),len(skip_nokey)))
print("  ギャップ:",[j[0] for j in jobs])
if skip_nokyu: print("  旧図なし(要確認):",skip_nokyu)
if skip_nokey: print("  figキーなし(要確認):",skip_nokey)

if WRITE and jobs:
    t0=time.time(); ok=0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs={ex.submit(render,s,k):(n,k) for n,s,k in jobs}
        for f in futs:
            n,k=futs[f]
            if f.result(): ok+=1
            else: print("  ★render失敗:",n,k)
    print("並列描画 %d/%d 完了 (%.1fs, %d並列)"%(ok,len(jobs),time.time()-t0,workers))
shutil.rmtree(TMP,ignore_errors=True)
