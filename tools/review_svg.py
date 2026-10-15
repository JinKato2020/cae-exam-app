# -*- coding: utf-8 -*-
"""教材レビュー用SVG部品。660×420、規定色、メイリオをパス化。副作用なし。"""
from pathlib import Path
import math,html,re,hashlib,xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
N,R,G,F,W='#1F3A65','#C82D2D','#888888','#E1E7F2','#FFFFFF'
font=TTFont('C:/Windows/Fonts/meiryo.ttc',fontNumber=0)
glyphs=font.getGlyphSet();cmap=font.getBestCmap();units=font['head'].unitsPerEm
class SVG:
    def __init__(self,title):self.p=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 660 420" width="660" height="420" role="img" data-style="cae-standard-v1" data-font="Meiryo"><title>{html.escape(title)}</title><rect width="660" height="420" fill="{W}"/>']
    def text(self,x,y,label,size=16,color=N,center=False):
        if re.search(r'[\^_]|\b[A-Z]dot\b|\\(?:frac|mathbf|partial|sqrt)', label):
            raise ValueError("図中へ数式コードを直接描かず、上付き・下付き・分数を組版してください")
        supers = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ᵀ', '0123456789−+T'))
        subs = dict(zip('₀₁₂₃₄₅₆₇₈₉', '0123456789'))
        runs=[]
        for c in label:
            if c in supers:runs.append((supers[c],size*.68,y-size*.43))
            elif c in subs:runs.append((subs[c],size*.75,y+size*.17))
            else:runs.append((c,size,y))
        width=sum(glyphs[cmap[ord(c)]].width*z/units for c,z,_ in runs if c not in '̂̇̄')
        if center:x-=width/2
        assert 0<=x and x+width<=660 and 0<y<=413,(label,x,y,width)
        self.p.append(f'<g aria-label="{html.escape(label,quote=True)}" fill="{color}">')
        previous_width=0
        for c,z,baseline in runs:
            mark=c in '̂̇̄'
            mark_width=glyphs[cmap[ord(c)]].width*z/units
            draw_x=x-previous_width/2-mark_width/2 if mark else x
            name=cmap[ord(c)];pen=SVGPathPen(glyphs);glyphs[name].draw(pen)
            self.p.append(f'<path d="{pen.getCommands()}" transform="translate({draw_x:.3f} {baseline}) scale({z/units:.6f} {-z/units:.6f})"/>')
            if not mark:
                previous_width=glyphs[name].width*z/units
                x+=previous_width
        self.p.append('</g>')
    def path(self,points,color=N,width=2,dash=''):
        self.p.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{x:.3f} {y:.3f}' for i,(x,y) in enumerate(points))+f'" fill="none" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def rect(self,x,y,w,h,color=F,stroke=None,width=2):self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"'+(f' stroke="{stroke}" stroke-width="{width}"' if stroke else '')+'/>')
    def circle(self,x,y,r,color=F,stroke=N):self.p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="{stroke}" stroke-width="2"/>')
    def dot(self,x,y,color=R,r=4):self.p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
    def arrow(self,x,y,X,Y,color=R,width=2):
        self.path([(x,y),(X,Y)],color,width)
        dx,dy=X-x,Y-y;L=math.hypot(dx,dy);dx/=L;dy/=L
        self.p.append(f'<path d="M{X} {Y} L{X-9*dx-4*dy} {Y-9*dy+4*dx} L{X-9*dx+4*dy} {Y-9*dy-4*dx} Z" fill="{color}"/>')
    def title(self,label,size=19):self.text(330,31,label,size,center=True)
    def save(self,path):
        document=''.join(self.p)+'</svg>'
        svg=ET.fromstring(document)
        palette={N,R,G,F,W,'none'}
        for e in svg.iter():
            if e.tag.rsplit('}',1)[-1] in ('text','image','foreignObject','script','style'):
                raise ValueError('指定体裁以外の文字・画像・スタイルは保存できません')
            for a,v in e.attrib.items():
                if a in ('fill','stroke') and v not in palette:
                    raise ValueError('指定外の色は保存できません: '+v)
                if a.endswith('href') or a=='style' or ('opacity' in a and v!='1'):
                    raise ValueError('外部参照・透過・個別CSSは使用できません')
                if a=='aria-label' and re.search(r'[\^_]|\b[A-Z]dot\b|\\[a-zA-Z]',v):
                    raise ValueError('数式コードを図にそのまま表示できません')
        Path(path).write_text(document,encoding='utf-8')

def graph(d,x,y,w,h,points,color=N,xlabel='x',ylabel='T',endlabels=None):
    d.arrow(x,y+h,x+w+12,y+h,G,1.2);d.arrow(x,y+h,x,y-10,G,1.2)
    d.text(x-12,y-15,ylabel,14,G);d.text(x+w+(40 if endlabels else 14),y+h+18,xlabel,14,G)
    d.path([(x+w*t,y+h-h*v) for t,v in points],color,2.5)
    if endlabels:
        d.text(x,y+h+23,endlabels[0],12,G,center=True);d.text(x+w,y+h+23,endlabels[1],12,G,center=True)
    return lambda t,v:(x+w*t,y+h-h*v)
def samples(func,n=100):return [(i/n,func(i/n)) for i in range(n+1)]


def save_standard_figure(d, svg_path, asset_key):
    """Save the approved vector and bind its registered PNG, using existing render tools."""
    import fitz
    root=Path(__file__).resolve().parent.parent
    svg_path=Path(svg_path);svg_path.parent.mkdir(parents=True,exist_ok=True)
    d.save(svg_path)
    doc=fitz.open(stream=svg_path.read_bytes(),filetype='svg')
    pdf=fitz.open('pdf',doc.convert_to_pdf())
    pix=pdf[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    asset=root/'assets'/'figures'/(asset_key+'.png')
    pix.save(asset)
    svg=ET.fromstring(svg_path.read_bytes())
    svg.set('data-asset-key',asset_key)
    svg.set('data-png-sha256',hashlib.sha256(asset.read_bytes()).hexdigest())
    # Preserve unprefixed SVG for normal editors and existing tools.
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    svg_path.write_bytes(ET.tostring(svg,encoding='utf-8'))
    svg_path.with_suffix('.png').write_bytes(asset.read_bytes())
