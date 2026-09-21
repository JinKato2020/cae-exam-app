# -*- coding: utf-8 -*-
"""固体1級 技術系16問の図(概念図/対比表/グラフ)。figlib使用・白地660x420。
使い方: python tools/figs_s1_tech16.py [キー...]   引数なしで全部。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *

# ---- 共通ヘルパ -----------------------------------------------------------
def table(d, x, y, colw, rowh, cells, header=True, fills=None, fnt=FT, pad=6):
    """cells=2次元リスト(文字列, \\n可)。colw=各列幅リスト, rowh=行高。
    header=True で1行目を淡色。fills={(r,c):color}で個別背景。"""
    rows=len(cells); cols=len(cells[0]); totw=sum(colw)
    cx=[x]
    for w in colw: cx.append(cx[-1]+w)
    for r in range(rows):
        yy=y+r*rowh
        for c in range(cols):
            fill=None
            if fills and (r,c) in fills: fill=fills[(r,c)]
            elif header and r==0: fill=FILL2
            if fill: d.rectangle((cx[c],yy,cx[c+1],yy+rowh),fill=fill)
    # 罫線
    for r in range(rows+1):
        d.line((x,y+r*rowh,x+totw,y+r*rowh),fill=BLACK,width=2)
    for c in range(cols+1):
        d.line((cx[c],y,cx[c],y+rows*rowh),fill=BLACK,width=2)
    # 文字
    for r in range(rows):
        for c in range(cols):
            txt=cells[r][c]
            lines=txt.split("\n")
            fnc = F if (header and r==0 and False) else fnt
            th=len(lines)*(fnc.size+3)
            y0=y+r*rowh+rowh/2-th/2+fnc.size/2
            col=BLACK
            for k,ln in enumerate(lines):
                ctext(d,cx[c]+colw[c]/2,y0+k*(fnc.size+3),ln,fnc,col)
    return cx

def box(d,x0,y0,x1,y1,label="",fill=FILL1,fnt=FS,col=BLACK,lw=3):
    d.rectangle((x0,y0,x1,y1),outline=col,width=lw,fill=fill)
    if label:
        lines=label.split("\n"); th=len(lines)*(fnt.size+3)
        yy=(y0+y1)/2-th/2+fnt.size/2
        for k,ln in enumerate(lines):
            ctext(d,(x0+x1)/2,yy+k*(fnt.size+3),ln,fnt,col)

# ---- 2-24 弾塑性 vs 剛塑性 -------------------------------------------------
def s1e2RigidPlastCmp():
    im,d=new(); title(d,"弾塑性解析と剛塑性解析の比較")
    cells=[
      ["項目","弾塑性解析","剛塑性解析"],
      ["弾性ひずみ","考慮する","無視(≒0)"],
      ["除荷・スプリングバック","追える","追えない"],
      ["除荷後の残留応力","求まる","求まらない"],
      ["指導原理","仮想仕事の原理\n(速度形)","上界定理"],
      ["主な用途","一般の弾塑性問題","塑性加工の\n大変形解析"],
    ]
    colw=[210,190,190]; rowh=51
    table(d,35,54,colw,rowh,cells,
          fills={(2,2):(255,236,236),(3,2):(255,236,236)})
    note(d,"弾性回復(除荷)が本質の残留応力・スプリングバックは剛塑性では扱えない")
    save(im,"s1e2RigidPlastCmp")

BLUET=(226,233,250); GREENT=(226,244,231); REDT=(255,236,236); YELT=(255,247,222)

# ---- 2-25 剛塑性FEMの指導原理=上界定理 -----------------------------------
def s1e2UpperBound():
    im,d=new(); title(d,"剛塑性有限要素法の指導原理:上界定理")
    # 真の解 帯
    d.line((60,215,600,215),fill=RED,width=3)
    ctext(d,70,199,"真の解",FS,RED,"lm")
    # 上界(上から)
    box(d,150,60,510,130,"上界定理\n運動学的に可容な速度場のうちエネルギー散逸率が最小のもの",BLUET,FT)
    arrow(d,330,130,330,205,BLUE,4,14); ctext(d,345,168,"上から近づく",FT,BLUE,"lm")
    # 下界(下から)
    box(d,150,300,510,368,"下界定理\n静力学的に可容な応力場から",GREENT,FT)
    arrow(d,330,300,330,225,GREEN,4,14); ctext(d,345,262,"下から近づく",FT,GREEN,"lm")
    # 該当ハイライト
    box(d,528,150,652,280,"剛塑性FEM\n速度場を\n未知数にとる\n→上界定理",REDT,FT,RED)
    note(d,"仮想仕事の原理(速度形)は弾塑性FEMの指導原理で別物")
    save(im,"s1e2UpperBound")

# ---- 2-26 上界定理の汎関数(速度場) ---------------------------------------
def s1e2Functional():
    im,d=new(); title(d,"上界定理の汎関数(速度場で最小化)")
    box(d,30,60,630,120,"Π = ∫(相当応力×相当ひずみ速度)dV − ∫(物体力×速度)dV − ∫(表面力×速度)dS  → 最小",FILL1,FT)
    ctext(d,175,140,"内部エネルギー散逸率",FT,BLUE)
    ctext(d,470,140,"外力の仕事率(物体力+表面力)",FT,GREEN)
    arrow(d,175,150,175,124,BLUE,2,9); arrow(d,470,150,470,124,GREEN,2,9)
    box(d,30,175,630,225,"付帯条件:境界条件と非圧縮性(体積一定)を満たす運動学的に可容な速度場",YELT,FT)
    # 弾性 vs 剛塑性 対比
    box(d,30,250,325,360,"弾性体\n∫σ dε = ½E εε\n最小ポテンシャル\nエネルギーの原理",BLUET,FT)
    box(d,335,250,630,360,"剛塑性体\n∫σ dε̇ = 相当応力×\n相当ひずみ速度\nエネルギー散逸の最小化",GREENT,FT)
    note(d,"弾性体の量(応力→応力・ひずみ→ひずみ速度・変位→速度)に置換した非線形最小化")
    save(im,"s1e2Functional")

# ---- 2-27 温度変化項=みかけの物体力 --------------------------------------
def s1e2ThermalLoad():
    im,d=new(); title(d,"熱弾塑性:温度変化項はみかけの物体力")
    cells=[
      ["荷重ベクトルの項","現れ方","分類"],
      ["物体力","体積積分 ∫[B]^T(力)dV","体積積分"],
      ["表面力","面積分 ∫(力)dS","面積分"],
      ["慣性力","加速度(未知量)を含む","動的項"],
      ["温度変化項","体積積分 ∫[B]^T・T̂{Θ}dV","体積積分"],
    ]
    colw=[180,290,120]; rowh=52
    table(d,35,56,colw,rowh,cells,
          fills={(1,0):BLUET,(1,1):BLUET,(1,2):BLUET,(4,0):REDT,(4,1):REDT,(4,2):REDT})
    # 対応の矢印(温度項→物体力)
    d.line((25,56+rowh*1+rowh/2,15,56+rowh*1+rowh/2),fill=RED,width=2)
    d.line((25,56+rowh*4+rowh/2,15,56+rowh*4+rowh/2),fill=RED,width=2)
    d.line((15,56+rowh*1+rowh/2,15,56+rowh*4+rowh/2),fill=RED,width=2)
    ctext(d,330,380,"温度変化項は物体力と同じ体積積分=みかけの物体力(等価節点力)",FT,RED)
    save(im,"s1e2ThermalLoad")

# ---- 2-28 交互増分解析フロー ---------------------------------------------
def s1e2StaggeredFlow():
    im,d=new(); title(d,"非定常熱伝導↔熱弾塑性 の交互増分解析")
    box(d,60,70,600,120,"① 非定常熱伝導解析 → 節点温度を求める",BLUET,FS)
    arrow(d,330,120,330,150,BLACK,3,12)
    box(d,60,150,600,205,"② 形状関数で積分点(ガウス点)温度に内挿し、\n前ステップとの差を積分点の温度増分に",YELT,FT)
    arrow(d,330,205,330,235,BLACK,3,12)
    box(d,60,235,600,290,"③ 温度増分をみかけの物体力の増分として\n離散化し、熱弾塑性応力解析に供する",GREENT,FT)
    # ループ(次の時間増分へ)
    arrow(d,600,262,625,262,BLACK,3,10); d.line((625,262,635,262),fill=BLACK,width=3)
    d.line((635,262,635,95),fill=BLACK,width=3); arrow(d,635,95,600,95,BLACK,3,10)
    ctext(d,643,178,"次の",FT,GRAY); ctext(d,643,196,"時間",FT,GRAY); ctext(d,643,214,"増分",FT,GRAY)
    note(d,"応力・ひずみは積分点で評価→温度も積分点の『増分』に換算するのが要点")
    save(im,"s1e2StaggeredFlow")

# ---- 2-29 超弾性(ゴム)の応力ひずみ曲線 -----------------------------------
def s1e2Hyperelastic():
    im,d=new(); title(d,"超弾性材料(ゴム)の応力-ひずみ関係")
    ox,oy=90,330; axes(d,ox,oy,455,250,"ひずみ ε","応力 σ")
    # 大変形で立ち上がる非線形弾性曲線(loading=unloadingが一致)
    pts=[]
    import math as _m
    for i in range(0,101):
        e=i/100.0
        y=oy-(30*e + 200*(e**3))   # 大ひずみで急立ち上がり
        pts.append((ox+ e*440, y))
    plot(d,ox,oy,pts,BLUE,4)
    ctext(d,500,105,"除荷でも同じ曲線を戻り",FT,RED); ctext(d,500,124,"原点に復帰=弾性(塑性でない)",FT,RED)
    arrow(d,500,140,470,182,RED,2,10)
    box(d,70,150,395,235,"応力=ひずみエネルギー密度\n(弾性ポテンシャル)関数の微分\n例:Neo-Hookean/Ogden/Mooney-Rivlin",YELT,FT)
    note(d,"大変形で強い非線形だが塑性ではない大変形弾性=超弾性")
    save(im,"s1e2Hyperelastic")

# ---- 5-22 き裂先端の特異要素 ---------------------------------------------
def s1e5SingularElem():
    im,d=new(); title(d,"き裂先端の応力特異性と特異要素")
    # 左: 応力 σ∝1/√r (発散)
    ox,oy=70,300; axes(d,ox,oy,215,215,"r","σ")
    ctext(d,ox+110,325,"先端からの距離 r",FT,GRAY)
    pts=[]
    for i in range(1,101):
        r=i/100.0; y=oy-min(28/math.sqrt(r),205)
        pts.append((ox+r*205,y))
    plot(d,ox,oy,pts,RED,4)
    ctext(d,ox+120,95,"σ ∝ 1/√r",FS,RED)
    ctext(d,ox+120,118,"r→0 で∞に発散",FT,RED)
    # 右: 変位 u∝√r
    ox2=390; axes(d,ox2,oy,215,215,"r","u")
    ctext(d,ox2+110,325,"先端からの距離 r",FT,GRAY)
    pts2=[(ox2+ (i/100.0)*205, oy-190*math.sqrt(i/100.0)) for i in range(0,101)]
    plot(d,ox2,oy,pts2,BLUE,4)
    ctext(d,ox2+120,120,"u ∝ √r",FS,BLUE)
    note(d,"特異要素は要素自体に 1/√r 特異性をもたせ、少ない要素数で先端場を精度よく表す")
    save(im,"s1e5SingularElem")

# ---- 5-26 パリス則の計算 --------------------------------------------------
def s1e5Paris():
    im,d=new(); title(d,"パリス則による疲労き裂進展速度")
    # 左: log-log 直線
    ox,oy=70,320; axes(d,ox,oy,300,235,"ΔK","da/dN")
    ctext(d,ox+45,100,"両対数",FT,GRAY)
    plot(d,ox,oy,[(ox+20,oy-30),(ox+280,oy-215)],BLUE,4)
    ctext(d,ox+150,oy-80,"傾き m=3",FS,BLUE)
    # 該当点
    px,py=ox+205,oy-155; node(d,px,py,6,RED,RED)
    d.line((px,oy,px,py),fill=LGRAY,width=1); d.line((ox,py,px,py),fill=LGRAY,width=1)
    ctext(d,px,py-16,"ΔK=15",FT,RED)
    # 右: 荷重サイクル inset と計算
    ox2,oy2=430,150;
    d.rectangle((ox2-10,60,650,235),outline=LGRAY,width=2)
    axes(d,ox2,oy2,180,80,"時間","K")
    # 正弦(5〜20)
    sp=[(ox2+ t*1.8, oy2-(12.5+7.5*math.sin(t*0.25))*4) for t in range(0,100)]
    plot(d,ox2,oy2,sp,GREEN,3)
    d.line((ox2,oy2-20*4,ox2+180,oy2-20*4),fill=LGRAY,width=1); ctext(d,ox2+195,oy2-80,"20",FT,GRAY,"lm")
    d.line((ox2,oy2-5*4,ox2+180,oy2-5*4),fill=LGRAY,width=1); ctext(d,ox2+195,oy2-20,"5",FT,GRAY,"lm")
    ctext(d,ox2+90,50,"Kmax=20, Kmin=5",FT,GREEN)
    box(d,405,255,650,375,"ΔK=Kmax−Kmin=20−5=15\nda/dN=C(ΔK)^m\n=1e-11×15³=3.375e-8\n≒3.4×10⁻⁸ m/cycle",YELT,FT)
    note(d,"駆動力は振幅 ΔK=Kmax−Kmin(最大値そのものではない)")
    save(im,"s1e5Paris")

# ---- 6-23 変位応答スペクトルとモード重合/応答スペクトル法 ----------------
def s1e6ResponseSpectrum():
    im,d=new(); title(d,"変位応答スペクトルと応答スペクトル法")
    ox,oy=70,300; axes(d,ox,oy,315,225,"f","変位")
    ctext(d,ox+150,325,"横軸:固有振動数 f",FT,GRAY)
    for zeta,col,lab in [(0.02,RED,"ζ=0.02"),(0.05,BLUE,"ζ=0.05"),(0.1,GREEN,"ζ=0.1")]:
        pts=[]
        for i in range(1,101):
            f=i/100.0
            base=1.0/(1.0+ (f*4)**1.6)         # 高振動数で減衰
            bump=0.5*math.exp(-((f-0.18)/(0.10+zeta*2))**2)*(0.03/ (zeta+0.02))
            v=(base+bump)
            pts.append((ox+f*325, oy-min(v*150,215)))
        plot(d,ox,oy,pts,col,3)
        ctext(d,ox+250, oy-40-[0,22,44][[0.02,0.05,0.1].index(zeta)], lab,FT,col,"lm")
    ctext(d,ox+150,90,"(C) 変位応答スペクトル",FS,BLACK)
    box(d,415,70,650,360,"(A) モード重合法\n= 卓越モードの時刻歴\n  を重ね合わせ\n\n(B) 横軸 = 固有振動数\n(C) 変位応答スペクトル\n= 最大応答変位の分布\n\n(D) 応答スペクトル法\n= SRSS で最大応答を\n  統計的に合成",FILL1,FT)
    save(im,"s1e6ResponseSpectrum")

# ---- 8-19b 3次元8節点六面体のアワーグラスモード数 ------------------------
def s1e8HexHourglass():
    im,d=new(); title(d,"3次元8節点六面体(1点積分)のアワーグラスモード数")
    # 六面体アイソメ
    iso_box(d,60,110,120,90,60)
    for (x,y) in [(60,110),(180,110),(180,200),(60,200),(108,84),(228,84),(228,174),(108,174)]:
        node(d,x,y,5,"white",BLACK)
    node(d,140,165,6,RED,RED); ctext(d,140,192,"1点積分",FT,RED)
    ctext(d,150,235,"8節点×並進3自由度",FT,GRAY)
    # 数え上げチェーン
    bx=320
    box(d,bx,80,640,124,"全自由度 8×3 = 24",BLUET,FS)
    arrow(d,bx+160,124,bx+160,150,BLACK,3,11); ctext(d,bx+250,137,"−剛体運動(並進3+回転3)=6",FT,GRAY,"lm") if False else None
    box(d,bx,150,640,194,"− 剛体運動 6 → 変形モード 18",GREENT,FS)
    arrow(d,bx+160,194,bx+160,220,BLACK,3,11)
    box(d,bx,220,640,272,"− 評価できるひずみ 6\n(εx,εy,εz,γxy,γyz,γzx)",YELT,FT)
    arrow(d,bx+160,272,bx+160,298,BLACK,3,11)
    box(d,bx,298,640,342,"アワーグラスモード = 12",REDT,FS,RED)
    note(d,"2次元4節点1点積分は2個 → 3次元8節点では12個(砂時計制御が重要)")
    save(im,"s1e8HexHourglass")

# ---- 10-10 非線形解析と実験の比較(検証の注意点) -------------------------
def s1e10ValidExp():
    im,d=new(); title(d,"非線形解析と実験を比較するときの注意点")
    # 値の軸
    d.line((70,215,590,215),fill=BLACK,width=2); ctext(d,590,235,"得られた値",FT,GRAY,"rm")
    # 解析値
    ax=230; node(d,ax,215,7,BLUE,BLUE); ctext(d,ax,180,"解析値",FS,BLUE); ctext(d,ax,258,"再現性あり",FT,BLUE)
    # 実験値(誤差バー)
    ex=430; d.line((ex-45,215,ex+45,215),fill=RED,width=3)
    for xx in (ex-45,ex+45): d.line((xx,207,xx,223),fill=RED,width=3)
    node(d,ex,215,7,RED,RED); ctext(d,ex,180,"実験値",FS,RED); ctext(d,ex,258,"誤差・ばらつき",FT,RED)
    # 差ブラケット
    dim(d,ax,150,ex,150,"差",0,GRAY)
    # 2つの注意点
    box(d,30,290,335,368,"① 実験値=真値ではない\n(よく管理された実験でも\n ばらつきは避けられない)",YELT,FT)
    box(d,345,290,650,368,"② 解析と実験の条件は\n 完全には一致しない\n(モデルの仮定が入る)",BLUET,FT)
    note(d,"両面(実験の誤差範囲・条件差)を吟味したうえで差を評価する")
    save(im,"s1e10ValidExp")

# ---- 11-3 連成問題 クラスII vs クラスI ------------------------------------
def s1e11CoupledClass():
    im,d=new(); title(d,"連成問題のクラスII(領域重複・構成則連成)")
    # クラスII: 重なる領域
    box(d,40,70,320,150,"",BLUET); ctext(d,180,60,"クラスII(該当)",FS,RED)
    ctext(d,110,95,"力学場",FS,BLUE); ctext(d,250,95,"電場",FS,GREEN)
    ctext(d,180,120,"同一領域が重複",FT,BLACK)
    arrow(d,150,135,210,135,RED,3,11); arrow(d,210,142,150,142,RED,3,11)
    box(d,40,160,320,240,"例:圧電体\nσ=CS−eE(ひずみ→応力・電界)\nD=eS+εE(電界→電束)\n構成則で双方向に連成",YELT,FT)
    # クラスI: 別領域が境界で接する
    ctext(d,505,60,"クラスI(非該当)",FS,GRAY)
    box(d,360,70,500,240,"領域A",FILL1,FS)
    box(d,510,70,650,240,"領域B",FILL2,FS)
    d.line((505,70,505,240),fill=RED,width=3)
    arrow(d,470,150,540,150,GRAY,3,11); arrow(d,540,165,470,165,GRAY,3,11)
    ctext(d,505,255,"別領域・境界条件で連成",FT,GRAY)
    note(d,"同じ領域・構成則で双方向=クラスII / 別領域が境界で接する=クラスI")
    save(im,"s1e11CoupledClass")

# ---- 11-13 4階弾性テンソルの対称性と独立成分21 ---------------------------
def s1e11ElasTensorSym():
    im,d=new(); title(d,"4階弾性テンソル D_ijkl の対称性と独立成分")
    # 縮約チェーン
    box(d,30,60,190,120,"81成分\n(3⁴)",FILL1,FT)
    arrow(d,190,90,230,90,BLACK,3,11)
    box(d,230,60,430,120,"6×6行列 36\n(添字対称)",BLUET,FT)
    arrow(d,430,90,470,90,BLACK,3,11)
    box(d,470,60,650,120,"対称→21独立\n(メジャー対称)",GREENT,FT)
    ctext(d,110,138,"Dijkl=Djikl=Dijlk",FT,GRAY)
    ctext(d,560,138,"Dijkl=Dklij",FT,GRAY)
    # 6x6行列 上三角=21
    gx,gy,cell=235,150,30
    for r in range(6):
        for c in range(6):
            if c>=r: d.rectangle((gx+c*cell,gy+r*cell,gx+(c+1)*cell,gy+(r+1)*cell),fill=(255,241,224))
    for i in range(7):
        d.line((gx,gy+i*cell,gx+6*cell,gy+i*cell),fill=BLACK,width=1)
        d.line((gx+i*cell,gy,gx+i*cell,gy+6*cell),fill=BLACK,width=1)
    ctext(d,gx+3*cell,gy+6*cell+18,"対称行列の上三角=21成分が独立",FT,ORANGE)
    ctext(d,120,220,"添字対称:\nεの対称→ijlk\nσの対称→jikl",FT,GRAY)
    note(d,"実際の独立数は材料対称性で減る(直交異方性9・等方性2)")
    save(im,"s1e11ElasTensorSym")

# ---- 11-14 直交異方性の独立弾性定数9 -------------------------------------
def s1e11Orthotropic():
    im,d=new(); title(d,"直交異方性材料の独立な弾性定数")
    # 進行バー 21→9→2
    box(d,40,66,220,118,"一般異方性\n21",FILL1,FT)
    arrow(d,220,92,260,92,BLACK,3,11)
    box(d,260,66,440,118,"直交異方性\n9",GREENT,FS,GREEN)
    arrow(d,440,92,480,92,BLACK,3,11)
    box(d,480,66,640,118,"等方性\n2",FILL2,FT)
    # 直交3対称面のイメージ
    iso_box(d,70,175,120,95,60)
    ctext(d,150,300,"互いに直交する",FT,GRAY)
    ctext(d,150,318,"3つの対称面",FT,GRAY)
    # 9定数リスト
    box(d,300,150,650,320,"独立な9定数\n\n縦弾性係数 Ex, Ey, Ez (3)\nせん断弾性係数 Gyz, Gzx, Gxy (3)\nポアソン比 3個(νxy/Ex=νyx/Ey 等)\n\n計 3+3+3 = 9",YELT,FT)
    note(d,"異方性21 → 直交異方性9 → 等方性2(G=E/2(1+ν)で結合)")
    save(im,"s1e11Orthotropic")

# ---- 11-16 線膨張係数(等方性 vs 異方性) ----------------------------------
def s1e11ThermalExp():
    im,d=new(); title(d,"線膨張係数 α_ij:等方性と異方性")
    # 等方性: 一様膨張
    ctext(d,180,66,"等方性材料",FS,BLUE)
    d.rectangle((110,110,250,230),outline=BLACK,width=3,fill=FILL1)
    d.rectangle((95,95,265,245),outline=BLUE,width=2)
    ctext(d,180,265,"全方向に同率で膨張",FT,BLUE)
    ctext(d,180,288,"α11=α22=α33",FT,BLUE)
    # 異方性: 方向で異なる
    ctext(d,490,66,"異方性材料",FS,RED)
    d.rectangle((430,110,570,230),outline=BLACK,width=3,fill=FILL1)
    d.rectangle((405,112,600,228),outline=RED,width=2)   # 横に大きく膨張(縦は僅か)
    ctext(d,500,265,"方向ごとに膨張率が異なる",FT,RED)
    ctext(d,500,288,"α11≠α22≠α33",FT,RED)
    box(d,60,310,640,374,"熱ひずみ (εT)ij=αij ΔT。αij は対称2階テンソルで主軸系では非対角0。\nα11=α22=α33 が成り立つのは等方性のみ(全材料ではない=これが誤り)",YELT,FT)
    save(im,"s1e11ThermalExp")

# ---- 11-22 連続体損傷力学 -------------------------------------------------
def s1e11DamageMech():
    im,d=new(); title(d,"連続体損傷力学:損傷を場の量で扱う")
    # 微視空隙のある要素
    box(d,40,80,240,230,"",FILL1)
    import random as _r; _r.seed(3)
    for _ in range(22):
        x=60+_r.random()*160; y=100+_r.random()*110; s=3+_r.random()*4
        d.ellipse((x-s,y-s,x+s,y+s),fill=GRAY,outline=BLACK)
    ctext(d,140,240,"微視的な空隙・き裂",FT,GRAY)
    arrow(d,245,155,320,155,BLACK,4,14); ctext(d,282,138,"平均化",FT,BLACK)
    # 損傷変数の場
    box(d,325,80,525,230,"損傷変数 D\n(場の量)\n\n0=健全 … 1=破断",GREENT,FS)
    box(d,540,80,652,230,"有効応力\nσ̃=σ/(1−D)\n剛性低下\nを表す",YELT,FT)
    box(d,40,250,650,308,"連続体力学の枠組みで損傷・破壊の進行を解析する。\n個々のき裂を1本ずつ陽に追う破壊力学とは立場が異なる。",BLUET,FT)
    note(d,"キーワード:損傷変数 D と連続体的な扱い")
    save(im,"s1e11DamageMech")

FIGS={
 "s1e2RigidPlastCmp":s1e2RigidPlastCmp,
 "s1e2UpperBound":s1e2UpperBound,
 "s1e2Functional":s1e2Functional,
 "s1e2ThermalLoad":s1e2ThermalLoad,
 "s1e2StaggeredFlow":s1e2StaggeredFlow,
 "s1e2Hyperelastic":s1e2Hyperelastic,
 "s1e5SingularElem":s1e5SingularElem,
 "s1e5Paris":s1e5Paris,
 "s1e6ResponseSpectrum":s1e6ResponseSpectrum,
 "s1e8HexHourglass":s1e8HexHourglass,
 "s1e10ValidExp":s1e10ValidExp,
 "s1e11CoupledClass":s1e11CoupledClass,
 "s1e11ElasTensorSym":s1e11ElasTensorSym,
 "s1e11Orthotropic":s1e11Orthotropic,
 "s1e11ThermalExp":s1e11ThermalExp,
 "s1e11DamageMech":s1e11DamageMech,
}

if __name__=="__main__":
    keys=sys.argv[1:] or list(FIGS)
    for k in keys:
        FIGS[k]()
