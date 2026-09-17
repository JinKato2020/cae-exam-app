# -*- coding: utf-8 -*-
"""CAE図の共通描画ライブラリ。白地660x420・黒線画で体裁を統一する。
使い方: import sys; sys.path.insert(0, r"<scratchpadパス>"); from figlib import *
  im,d = new()
  ... 各プリミティブで描画 ...
  save(im, "femXxx")   # assets/figures/femXxx.png に保存
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = r"c:\Users\jwpsa\Documents\desktop\claude\CAE\assets\figures"
W, H = 660, 420
BLACK=(0,0,0); GRAY=(120,120,120); LGRAY=(205,205,205)
RED=(200,40,40); BLUE=(40,80,190); GREEN=(30,150,60); ORANGE=(210,130,20)
FILL1=(245,245,245); FILL2=(232,232,232); FILL3=(220,220,220)

def font(sz):
    for p in [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\YuGothR.ttc",
              r"C:\Windows\Fonts\msgothic.ttc", r"C:\Windows\Fonts\arial.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()
FL=font(27); F=font(23); FS=font(19); FT=font(16)

def new():
    im=Image.new("RGB",(W,H),"white"); return im, ImageDraw.Draw(im)

def save(im,name):
    os.makedirs(OUT,exist_ok=True)
    p=os.path.join(OUT,name+".png"); im.save(p); print("saved",name); return p

def title(d,s):
    ctext(d, W/2, 30, s, F)

def ctext(d,x,y,s,fnt=FS,fill=BLACK,anchor="mm"):
    d.text((x,y),s,font=fnt,fill=fill,anchor=anchor)

def arrow(d,x1,y1,x2,y2,col=BLACK,wd=3,head=13):
    d.line((x1,y1,x2,y2),fill=col,width=wd)
    ang=math.atan2(y2-y1,x2-x1)
    for s in (0.5,-0.5):
        d.line((x2,y2,x2-head*math.cos(ang-s),y2-head*math.sin(ang-s)),fill=col,width=wd)

def force(d,x,y,dx,dy,label="",col=RED,fnt=F):
    x2,y2=x+dx,y+dy; arrow(d,x,y,x2,y2,col,4,15)
    if label:
        lx,ly = x2 + (12 if dx>=0 else -12), y2 + (0 if abs(dy)>abs(dx) else -18)
        ctext(d,lx,ly,label,fnt,col, "lm" if dx>=0 else "rm")

def dim(d,x1,y1,x2,y2,label,off=0,col=GRAY):
    """寸法線(両端矢印+ラベル)。"""
    d.line((x1,y1,x2,y2),fill=col,width=2)
    for (ax,ay,bx,by) in [(x1,y1,x2,y2),(x2,y2,x1,y1)]:
        ang=math.atan2(by-ay,bx-ax)
        for s in (0.5,-0.5):
            d.line((ax,ay,ax+11*math.cos(ang-s),ay+11*math.sin(ang-s)),fill=col,width=2)
    mx,my=(x1+x2)/2,(y1+y2)/2
    ctext(d,mx,my-12,label,FT,col)

def wall(d,x,y0,y1,side=1,n=9):
    """固定壁。side=1:右にハッチ, -1:左にハッチ。"""
    d.line((x,y0,x,y1),fill=BLACK,width=3)
    step=(y1-y0)/n
    for i in range(n):
        yy=y0+i*step
        d.line((x,yy+step,x+side*15,yy),fill=BLACK,width=2)

def hwall(d,x0,x1,y,side=1,n=10):
    """水平な固定面(天井/床)。side=1:下にハッチ, -1:上。"""
    d.line((x0,y,x1,y),fill=BLACK,width=3)
    step=(x1-x0)/n
    for i in range(n):
        xx=x0+i*step
        d.line((xx+step,y,xx,y+side*15),fill=BLACK,width=2)

def spring(d,x1,y,x2,y2=None,coils=6,amp=16,wd=3):
    y2=y if y2 is None else y2
    dx=x2-x1; dy=y2-y; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L
    px,py=-uy,ux; lead=18
    a=(x1+ux*lead, y+uy*lead); b=(x2-ux*lead, y2-uy*lead)
    pts=[(x1,y),a]; seg=coils*2
    for i in range(1,seg):
        t=i/seg; s=amp if i%2 else -amp
        pts.append((a[0]+(b[0]-a[0])*t+px*s, a[1]+(b[1]-a[1])*t+py*s))
    pts+=[b,(x2,y2)]
    d.line(pts,fill=BLACK,width=wd,joint="curve")

def node(d,x,y,r=7,fill="white",col=BLACK):
    d.ellipse((x-r,y-r,x+r,y+r),outline=col,width=3,fill=fill)

def bar(d,x1,y1,x2,y2,thick=0,fill=FILL1):
    """棒/部材。thick>0で太い矩形、0で太線。"""
    if thick>0:
        ang=math.atan2(y2-y1,x2-x1); px,py=-math.sin(ang)*thick/2, math.cos(ang)*thick/2
        d.polygon([(x1+px,y1+py),(x2+px,y2+py),(x2-px,y2-py),(x1-px,y1-py)],outline=BLACK,width=3,fill=fill)
    else:
        d.line((x1,y1,x2,y2),fill=BLACK,width=5)

def pin_support(d,x,y,size=24):
    d.polygon((x,y,x-size,y+size*1.4,x+size,y+size*1.4),outline=BLACK,width=3)
    for i in range(6):
        d.line((x-size+i*9,y+size*1.4,x-size-9+i*9,y+size*1.4+14),fill=BLACK,width=2)

def roller_support(d,x,y,size=24):
    d.polygon((x,y,x-size,y+size*1.25,x+size,y+size*1.25),outline=BLACK,width=3)
    yy=y+size*1.25
    for cx in (x-size*0.6,x,x+size*0.6):
        d.ellipse((cx-6,yy,cx+6,yy+12),outline=BLACK,width=2)
    d.line((x-size-2,yy+14,x+size+2,yy+14),fill=BLACK,width=2)

def matrix_grid(d,x,y,vals,cell=52,highlight=None,fnt=FS):
    """valsは2次元リスト(文字列)。highlight=(r,c)で赤枠。"""
    rows=len(vals); cols=len(vals[0])
    for i in range(rows+1):
        d.line((x,y+i*cell,x+cols*cell,y+i*cell),fill=BLACK,width=2)
    for j in range(cols+1):
        d.line((x+j*cell,y,x+j*cell,y+rows*cell),fill=BLACK,width=2)
    for r in range(rows):
        for c in range(cols):
            col= RED if (highlight and r==highlight[0] and c==highlight[1]) else BLACK
            ctext(d,x+c*cell+cell/2,y+r*cell+cell/2,vals[r][c],fnt,col)
    if highlight:
        d.rectangle((x+highlight[1]*cell,y+highlight[0]*cell,x+(highlight[1]+1)*cell,y+(highlight[0]+1)*cell),outline=RED,width=4)

def axes(d,ox,oy,xlen,ylen,xlabel="x",ylabel="y",col=BLACK):
    arrow(d,ox,oy,ox+xlen,oy,col,2,11); ctext(d,ox+xlen+10,oy,xlabel,FS,col,"lm")
    arrow(d,ox,oy,ox,oy-ylen,col,2,11); ctext(d,ox-10,oy-ylen-4,ylabel,FS,col,"rm")

def plot(d,ox,oy,pts,col=BLUE,wd=3):
    """pts=[(px,py)...] は既にピクセル座標。折れ線。"""
    d.line(pts,fill=col,width=wd,joint="curve")

def iso_box(d,ox,oy,w,h,dp):
    dx=int(dp*0.8); dy=int(dp*0.5)
    d.polygon([(ox,oy),(ox+w,oy),(ox+w,oy+h),(ox,oy+h)],outline=BLACK,width=3,fill=FILL1)
    d.polygon([(ox,oy),(ox+dx,oy-dy),(ox+w+dx,oy-dy),(ox+w,oy)],outline=BLACK,width=3,fill=FILL2)
    d.polygon([(ox+w,oy),(ox+w+dx,oy-dy),(ox+w+dx,oy+h-dy),(ox+w,oy+h)],outline=BLACK,width=3,fill=FILL3)

def _isoslab(d,ox,oy,w,h,dx,dy,crackface=False):
    """アイソメ直方体スラブ1枚(前面/上面/右面)。crackface=Trueなら上面をき裂面として濃色に。"""
    d.polygon([(ox,oy),(ox+w,oy),(ox+w,oy+h),(ox,oy+h)],outline=BLACK,width=2,fill=FILL1)          # 前面
    d.polygon([(ox,oy),(ox+dx,oy-dy),(ox+w+dx,oy-dy),(ox+w,oy)],outline=BLACK,width=2,
              fill=(255,236,236) if crackface else FILL2)                                            # 上面(=き裂面)
    d.polygon([(ox+w,oy),(ox+w+dx,oy-dy),(ox+w+dx,oy+h-dy),(ox+w,oy+h)],outline=BLACK,width=2,fill=FILL3)  # 右面

def crack_mode(d,cx,cy,mode):
    """き裂の3変形モードを立体(アイソメ)で描く。cy=き裂面の高さ。mode=1:開口 2:面内せん断 3:面外せん断。
    直方体を上下2スラブに割り、モード別に相対変位させて赤矢印で運動方向を示す。"""
    w,hh,dp=92,40,52
    dx,dy=int(dp*0.8),int(dp*0.5)     # 42,26
    bx=cx-w//2-dx//2
    uy,ly=cy-hh,cy                    # 上/下スラブの前面左上y(変位前)
    if mode==1:      # 開口:縦に開く
        op=12; u=(bx,uy-op); l=(bx,ly+op)
    elif mode==2:    # 面内せん断:き裂進展方向(x)にずれる
        s=18; u=(bx+s,uy); l=(bx-s,ly)
    else:            # 面外せん断:き裂前縁方向(z=奥行)にずれる
        kx,ky=16,10; u=(bx+kx,uy-ky); l=(bx-kx,ly+ky)
    # 上スラブ(奥)→下スラブの順。割れた面(上スラブの下面/下スラブの上面)を淡赤で見せる
    _isoslab(d,u[0],u[1],w,hh,dx,dy)                 # 上スラブ
    _isoslab(d,l[0],l[1],w,hh,dx,dy,crackface=True)  # 下スラブ(上面=き裂面)
    if mode==1:
        arrow(d,u[0]+w//2,u[1]-6,u[0]+w//2,u[1]-34,RED,4,14)
        arrow(d,l[0]+w//2,l[1]+hh+6,l[0]+w//2,l[1]+hh+34,RED,4,14)
    elif mode==2:
        arrow(d,u[0]+w-6,u[1]+hh//2,u[0]+w+28,u[1]+hh//2,RED,4,14)
        arrow(d,l[0]+6,l[1]+hh//2,l[0]-28,l[1]+hh//2,RED,4,14)
    else:
        arrow(d,u[0]+w//2,u[1]+hh//2,u[0]+w//2+34,u[1]+hh//2-20,RED,4,13)
        arrow(d,l[0]+w//2,l[1]+hh//2,l[0]+w//2-34,l[1]+hh//2+20,RED,4,13)

def angle_arc(d,cx,cy,r,a0,a1,label="",col=GRAY):
    """a0,a1は度(数学系:反時計回り、右=0°)。画像座標に変換して描く。"""
    d.arc((cx-r,cy-r,cx+r,cy+r), -a1, -a0, fill=col, width=2)
    am=math.radians((a0+a1)/2)
    if label: ctext(d,cx+ (r+16)*math.cos(am), cy-(r+16)*math.sin(am), label, FT, col)

def note(d,s,y=None):
    ctext(d, W/2, y if y else H-26, s, FT, GRAY)
