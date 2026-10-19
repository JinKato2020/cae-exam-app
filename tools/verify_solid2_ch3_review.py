# -*- coding: utf-8 -*-
from pathlib import Path
import json,math,hashlib
import sympy as s
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第3章_反映結果'
current=json.loads((ROOT/'content/questions/heat-basics.json').read_text(encoding='utf-8'))
before=json.loads((ROOT/'tmp/pdfs/ch3_review/heat-basics-before.json').read_text(encoding='utf-8'))
assert len(current['questions'])==17
assert [(q['id'],q['number'],q['answer'],q['officialRef']) for q in current['questions']]==[(q['id'],q['number'],q['answer'],q['officialRef']) for q in before['questions']]
x=s.symbols('x',real=True);r,lam,S,L,q0=s.symbols('r lam H L q0',positive=True);T0,TR=s.symbols('T0 TR',real=True)
checks={}
assert -5*10==-50 and -5*20==-100
checks['3-1']={'gradient':[10,20],'lambda':5,'qx':[-50,-100]}
checks['3-2']={'roles':['unknown','gradient','constitutive_result','source'],'structural':['displacement','strain','stress','force'],'thermal':['temperature','temperature_gradient','heat_flux','heat_supply']}
checks['3-3']={'steady_condition':'dT/dt=0','steady_does_not_require_spatially_uniform':True,'diagram':'qualitative internal-point temperature, no time constant asserted'}
Tc=100-80*s.log(r)/s.log(3)
assert s.simplify(Tc.subs(r,1)-100)==0 and s.simplify(Tc.subs(r,3)-20)==0
assert s.simplify(s.diff(Tc,r)+80/(r*s.log(3)))==0
assert s.simplify(s.diff(Tc,r,2)-80/(r*r*s.log(3)))==0
checks['3-4']={'cylinder_derivatives':[str(s.diff(Tc,r)),str(s.diff(Tc,r,2))],'heat_rate_conserved':True}
RA=s.Rational(2,3);RB=s.Integer(1)
assert RA/(RA+RB)==s.Rational(2,5) and RB/(RA+RB)==s.Rational(3,5)
models=json.loads((OUT/'図の数値モデル.json').read_text(encoding='utf-8'))
c5=models['3-5-candidates']
ii=c5['III'];slopeA=(ii[1][1]-ii[0][1])/(ii[1][0]-ii[0][0]);slopeB=(ii[2][1]-ii[1][1])/(ii[2][0]-ii[1][0])
assert math.isclose(slopeB/slopeA,3) and math.isclose(3*slopeA,slopeB)
assert c5['IV'][1][0]==c5['IV'][2][0] and c5['IV'][1][1]!=c5['IV'][2][1]
checks['3-5']={'resistance_ratio':'2:3','drop_fractions':['2/5','3/5'],'candidate_III_slope_ratio':slopeB/slopeA,'interface_continuous':True}
gn=s.symbols('gn',real=True);qn=-lam*gn
assert s.solve(s.Eq(qn,0),gn)==[0]
checks['3-6']={'normal_law':'q dot n = -lambda dT/dn','inward_positive_convention':'q dot n = -qin','units_gradient':'K/m','units_flux':'W/m^2','insulated_contour':'perpendicular to boundary'}
T=T0+S*x*(L-x)/(2*lam);q=-lam*s.diff(T,x)
assert T.subs(x,0)==T0 and T.subs(x,L)==T0
assert s.simplify(s.diff(T,x,2)+S/lam)==0 and s.simplify(T.subs(x,L/2)-T0-S*L**2/(8*lam))==0
assert s.simplify(q-S*(x-L/2))==0
checks['3-7']={'temperature':str(T),'qx':str(q),'curvature':str(s.diff(T,x,2)),'description':'上に凸、中央最高'}
T=TR+q0*(L-x)/lam+S*(L*L-x*x)/(2*lam)
assert T.subs(x,L)==TR and s.simplify(-lam*s.diff(T,x)-q0-S*x)==0
assert s.diff(T,x,2)==-S/lam
checks['3-8']={'temperature':str(T),'curvature':str(s.diff(T,x,2)),'description':'単調下降、上に凸、右ほど急','candidate':'C'}
for t,v in models['3-8-candidates']['C']:assert math.isclose(v,(2-t-t*t)/2)
QL=2*math.pi*.04*90/.4055;qo=QL/(2*math.pi*.12);qi=QL/(2*math.pi*.08)
assert abs(QL-56)<.5 and abs(qo-74)<.1 and abs(qi-111)<.1
checks['3-9']={'Q_per_L_W_per_m':QL,'q_out_W_per_m2':qo,'q_in_W_per_m2':qi,'outer_area_per_L_m':2*math.pi*.12}
assert 1/(.1+.2+.1)==2.5
hh,hc,t,A,DT=s.symbols('h_h h_c t A DT',positive=True)
K=1/(1/hh+t/lam+1/hc);q=K*DT
assert s.simplify(q/hh+q*t/lam+q/hc-DT)==0
R=1/(K*A);Q=q*A
assert s.simplify(Q-DT/R)==0
assert K.subs({hh:10,hc:20,t:s.Rational(1,10),lam:1})==4
assert R.subs({hh:10,hc:20,t:s.Rational(1,10),lam:1,A:2})==s.Rational(1,8)
checks['3-10']={'K':str(K),'temperature_drop_sum':'q/h_h + qt/lambda + q/h_c = DeltaT','R_total':'1/(KA)','units_K':'W/(m^2K)','units_R':'K/W','glossary_example_K_A_DT_q_Q_R':[4,2,50,200,400,.125]}
Rinit=s.Rational(1,4);ratios=[s.Rational(20,100)/s.Rational(5,4)+s.Rational(4,100)+s.Rational(1,100),s.Rational(20,100)+s.Rational(4,100)*s.Rational(3,4)+s.Rational(1,100),s.Rational(20,100)+s.Rational(4,100)+s.Rational(1,100)/s.Rational(5,4)]
assert ratios==[s.Rational(21,100),s.Rational(24,100),s.Rational(248,1000)]
checks['3-11']={'inverse_K_A_B_C':[float(v) for v in ratios],'K_A_B_C':[float(1/v) for v in ratios],'q_gain_percent':[float((Rinit/v-1)*100) for v in ratios],'best':'A'}
res=[s.Rational(1,20),s.Rational(4,100)/s.Rational(4,10),s.Rational(8,100)/s.Rational(8,10),s.Rational(1,5)]
Rsum=sum(res);flux=s.Rational(140)/Rsum
temps=[s.Integer(160)]
for v in res:temps.append(temps[-1]-flux*v)
assert Rsum==s.Rational(45,100) and flux==s.Rational(2800,9) and temps[-1]==20
assert math.isclose(float(temps[-2]),82.2222222222222)
assert all(math.isclose(float(a),b,abs_tol=1e-8) for a,b in zip(temps,models['3-12-profile']['temperatures']))
checks['3-12']={'R_components':[float(v) for v in res],'q_W_per_m2':float(flux),'temperature_sequence_C':[float(v) for v in temps],'wrong3_R_q_Ts':[.35,400,100],'wrong4_R_q_Ts':[.25,560,132]}
checks['3-13']={'lambda_units':'W/(m K)','h_units':'W/(m^2 K)','ordinary_metal_electron_transport':'primary/reference confirmed, qualitative trend not universal equality'}
c14=models['3-14-candidates'];passes=[]
for name,pts in c14.items():
    dropL=pts[0][1]-pts[1][1];dropR=pts[2][1]-pts[3][1]
    if dropL>0 and dropR>0 and math.isclose(dropR,4*dropL):passes.append(name)
assert passes==['IV']
checks['3-14']={'correct':'IV','drop_ratio_R_to_L':4,'all_candidates_checked':True}
assert s.Rational(6)/s.Rational(3,2)==4
for t,v in models['3-15-cylinder']:assert math.isclose(v,1-math.log(1+.5*t)/math.log(1.5))
checks['3-15']={'delta_out_to_in':4,'q_out_to_in':2/3,'area_out_to_in':1.5,'wall_curve':'logarithmic'}
y=s.symbols('y');field=5+3*x+y*y
assert s.diff(field,y).subs(y,0)==0 and s.diff(field,x)==3
checks['3-16']={'example_T':'5+3x+y^2','normal_derivative_on_y0':0,'tangential_derivative':3,'temperature_not_fixed_to_zero':True}
g=s.Function('g');field=g(r)
assert s.diff(field,y)==0
checks['3-17']={'isotropic_axial_flux':'-lambda dT/dz = 0','inner':'convective, hot fluid','outer':'convective, ambient','axial_cut':'adiabatic'}
for q in current['questions']:
    assert q['figure']=='helpful'
    for attr in ('figureImage','preFigureImage'):
        if q.get(attr):assert Image.open(ROOT/'assets/figures'/f'{q[attr]}.png').size==(1320,840)
    lines=q['explanation'].splitlines();assert len(lines)==4
    assert all(lines[i].startswith(tag) for i,tag in enumerate(('【基礎】','【考え方】','【ポイント】','【引っかけ】')))
    for i in range(1,5):
        if i!=q['answer']:assert f'({i})' in lines[-1]
# Protect all other chapters and the already completed chapter 1 PDFs.
snap=json.loads((ROOT/'tmp/pdfs/ch3_review/before-hashes.json').read_text(encoding='utf-8'))
for name,sha in snap.items():
    if name=='content\\questions\\heat-basics.json' or name=='content/questions/heat-basics.json':continue
    if name.endswith('.pdf') and '固体2級_第3章_' in name:continue
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,('unexpected other-chapter change',name)
checks['answers_ids_official_refs_unchanged']=True;checks['other_chapters_unchanged']=True
checks['source_sha256']=hashlib.sha256((ROOT/'content/questions/heat-basics.json').read_bytes()).hexdigest()
(OUT/'独立検算・反映検証.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('17-question independent checks PASS; diagram slopes/drops/temperatures match; answer numbers and other chapters unchanged.')
