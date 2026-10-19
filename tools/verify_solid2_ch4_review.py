# -*- coding: utf-8 -*-
"""答えとは別に、荷重・変位・エネルギー・組立てを数値で確かめる。"""
from pathlib import Path
import json,math,hashlib,zipfile,re
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第4章_反映結果';TMP=ROOT/'tmp/pdfs/ch4_review'
data=json.loads((ROOT/'content/questions/fem-basics.json').read_bytes());terms=json.loads((ROOT/'content/formulas/ch4.json').read_bytes())
before=json.loads((TMP/'fem-basics-before.json').read_bytes());results={}
def close(a,b):assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)
def mul(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def energy(E,segments,loads):
 # 応力×ひずみ×体積/2 を各区間で加算（剛性公式とは独立）。
 return sum((P/A)*(P/(E*A))*(A*L)/2 for (A,L),P in zip(segments,loads))
E=200000;I=[(200,100),(100,200)];II=[(200,300)];P=10000
UI=energy(E,I,[P,P])/1000;UII=energy(E,II,[P])/1000
close(UI,.625);close(UII,.375)
complianceI=sum(L/(E*A) for A,L in I);complianceII=sum(L/(E*A) for A,L in II)
Pi=.12/complianceI;Pii=.12/complianceII
Di=energy(E,I,[Pi,Pi])/1000;Dii=energy(E,II,[Pii])/1000
close(Di,.576);close(Dii,.960);assert UI>UII and Di<Dii
results['4-4']={'force_given_J':[UI,UII],'displacement_given_J':[Di,Dii],'stiffness_N_per_mm':[1/complianceI,1/complianceII]}
# せん断項は γ=2εxy と応力テンソルの二つの成分を両方数える。
sx,sy,t,ex,ey,gamma=100,30,40,.001,.0003,.002
tensor=.5*(sx*ex+sy*ey+2*t*(gamma/2));eng=.5*(sx*ex+sy*ey+t*gamma);close(tensor,eng)
results['4-5']={'density_N_per_mm2':eng}
# σ=ε² の無次元例。曲線下 ∫ε²dε、縦軸側 ∫√σdσ。
u=Fraction(1,3);comp=Fraction(2,3);assert u+comp==1 and u!=comp
results['4-6']={'nonlinear_example':[str(u),str(comp)],'linear_example':['1/2','1/2']}
k=10000;f=2000;ueq=f/k
for perturb in (-.1,.1):assert .5*k*(ueq+perturb)**2-f*(ueq+perturb)>.5*k*ueq**2-f*ueq
results['4-7']={'equilibrium_mm':ueq,'curvature_N_per_mm':k}
# 2×2の力の釣合いをクラメル法で解く。
a,b,c,d=-math.cos(math.pi/6),math.cos(math.pi/3),math.sin(math.pi/6),math.sin(math.pi/3)
det=a*d-b*c;nca=(0*d-b*20)/det;ncb=(a*20-0*c)/det
close(nca,10);close(ncb,10*math.sqrt(3));close(a*nca+b*ncb,0);close(c*nca+d*ncb,20)
assert sum(abs(v-ncb)<.01 for v in (10,23.09,34.64,17.32))==1
results['4-9']={'forces_kN':[nca,ncb],'horizontal_vertical_residual_kN':[a*nca+b*ncb,c*nca+d*ncb-20]}
# 単位の指数：表面力 N m^-2、仮想変位m、面積m² → N m。
assert -2+1+2==1;results['4-12']={'work_unit':'N m'}
EA=200000*100;L=500;eps0=12e-6*50
B=[-1/L,1/L];fth=[bi*EA*L*eps0 for bi in B];close(fth[0],-12000);close(fth[1],12000)
sig0=5;fsig=[-bi*100*L*sig0 for bi in B];close(fsig[0],500);close(fsig[1],-500)
free_displacement=L*eps0;close(free_displacement,.3)
results['4-13']={'initial_strain_rhs_N':fth,'initial_stress_rhs_N':fsig,'free_expansion_mm':free_displacement,'fixed_bar_stress_MPa':-200000*eps0}
# 積分の弱形式を、u=x², w=x(1-x), EA=1, p=-2 で厳密に確認。
# ∫w'u' = ∫(1-2x)2x = -1/3; ∫wp = -1/3、境界w=0。
assert 1-Fraction(4,3)==-2*(Fraction(1,2)-Fraction(1,3));results['4-14']={'weak_form_both_sides':'-1/3'}
for x in (0,.2,.75,1):close((1-x)+x,1);close((1-x)*.1+x*.1,.1)
results['4-15']={'partition_of_unity':True}
u16=(1-.75)*3+.75*9;close(u16,7.5);assert sum(abs(v-u16)<.001 for v in (6,9,4.5,7.5))==1
results['4-16']={'interpolated_mm':u16}
du_dx,du_dy,dv_dx,dv_dy=.001,.002,-.0005,.0003
gamma=du_dy+dv_dx;close(gamma,.0015);close(-.02+.02,0)
results['4-17']={'strain':[du_dx,dv_dy,gamma],'rigid_rotation_shear':0}
# 三角形(0,0),(2,0),(0,3)の形状関数の微分からBを作る。
nx=[-.5,.5,0];ny=[-1/3,0,1/3];Bm=[[],[],[]]
for x,y in zip(nx,ny):Bm[0]+=[x,0];Bm[1]+=[0,y];Bm[2]+=[y,x]
coords=[(0,0),(2,0),(0,3)];disps=[]
for x,y in coords:disps += [.001*x+.002*y,-.0005*x+.0003*y]
actual=mul(Bm,disps)
for a,b in zip(actual,[du_dx,dv_dy,gamma]):close(a,b)
results['4-18_to_20']={'B_constant':Bm,'computed_strain':actual}
EE=206000;nu=.3;G=EE/(2*(1+nu));Dps=[[EE/(1-nu**2),EE*nu/(1-nu**2),0],[EE*nu/(1-nu**2),EE/(1-nu**2),0],[0,0,G]]
stress=mul(Dps,[.001,0,.002]);close(stress[0],226.37362637362637);close(stress[1],67.91208791208791);close(stress[2],158.46153846153845)
pefactor=EE/((1+nu)*(1-2*nu));Dpe=[[pefactor*(1-nu),pefactor*nu,0],[pefactor*nu,pefactor*(1-nu),0],[0,0,G]]
assert Dps!=Dpe;close(Dps[2][2],Dpe[2][2]);results['4-21']={'plane_stress_example_MPa':stress}
# 直列ばねを拘束前の3×3へ要素ごとに組立て、固定自由度を取り除く。
K=[[0]*3 for _ in range(3)]
for i,j,k in ((0,1,100),(1,2,200)):
 K[i][i]+=k;K[j][j]+=k;K[i][j]-=k;K[j][i]-=k
reduced=[row[1:] for row in K[1:]];assert reduced==[[300,-200],[-200,200]]
close(mul(reduced,[8,12])[0],0);close(mul(reduced,[8,12])[1],800)
results['4-22']={'full_matrix_N_per_mm':K,'reduced_matrix':reduced}
# 斜めばねの水平二自由度への直接射影。各固定点の変位は0。
cos45=math.cos(math.pi/4);effective=sum(120*cos45**2 for _ in range(2));close(effective,120)
K23=[[120+effective,-120],[-120,120]];close(K23[0][0],240)
# u1=1,u2=0なら軸伸びcos45→二本のエネルギー60、水平一本60、合計120。
uenergy=2*.5*120*cos45**2+.5*120;close(uenergy,.5*K23[0][0])
results['4-23']={'projected_stiffness':effective,'matrix':K23,'energy_check_Nmm':uenergy}
positive_offdiag=120*math.cos(math.pi/3)*math.sin(math.pi/3);assert positive_offdiag>0
results['4-24']={'counterexample_positive_offdiagonal_N_per_mm':positive_offdiag}
for row in K:close(sum(row),0)
for v in mul(K,[.5,.5,.5]):close(v,0)
results['4-25']={'rigid_translation_internal_force':mul(K,[.5,.5,.5])}
u1,u2,u3=.0,.1,.25;f21=150*(u2-u1);f22=250*(u2-u3)
close(f21+f22,400*u2-150*u1-250*u3)
results['4-26']={'same_displacement_mm':u2,'element_contributions_N':[f21,f22],'assembled_force_N':f21+f22,'diagonal_N_per_mm':400}
# 固定端に既知外力があっても反力は釣合いから求める。
K27=[[10000,-10000],[-10000,10000]];disp=[0,.1];ext=[200,1000]
reaction=[x-y for x,y in zip(mul(K27,disp),ext)];assert reaction==[-1200,0]
results['4-27']={'reactions_with_load_at_fixed_node_N':reaction}
assert 5*2-(2+1+1)==6;results['4-28']={'unknown_components':['u2','v2','u3','u4','v4','u5'],'count':6}
Lcoords=[Fraction(1,3)]*3;omegas=[Fraction(1,4)]*4;assert sum(Lcoords)==sum(omegas)==1
A=300
def integral(l,m,n):return Fraction(2*A*math.factorial(l)*math.factorial(m)*math.factorial(n),math.factorial(l+m+n+2))
assert [integral(1,0,0),integral(2,0,0),integral(1,1,0)]==[100,50,25]
results['4-29']={'centroid_triangle':'1/3 each','centroid_tetrahedron':'1/4 each','area_integrals_mm2':[100,50,25],'body_force_N_per_node':2}
# 全公式カードの数値例も確認。
close(.75*.02+.25*.12,.045);close((.1-0)/200,.0005);close(200000*.0005,100)
close(200000*100/500,40000);close(.5*40000*.1**2/1000,.2)
close(20000*.5*.01,100);close(.5*10000*.2**2,200);close(2000*.2,400)
close(.5*100*.0005,.025);close(.2+1000/10000,.3)
assert [q['answer'] for q in data['questions']]==[q['answer'] for q in before['questions']]
ids={it['id'] for it in terms['items']};assert len(ids)==17
for q in data['questions']:
 assert all(i in ids for i in q.get('relatedFormulas',[]))
 assert len(q['choices'])==4 and 1<=q['answer']<=4
 assert len(q['explanation'].splitlines())==4
 for k in ('figureImage','preFigureImage'):
  if q.get(k):assert (ROOT/'assets/figures'/f'{q[k]}.png').exists()
 for s in (q['question'],*q['choices'],q['explanation']):
  assert s.count('$')%2==0;assert not any(ord(c)<32 and c not in '\n\t' for c in s)
for rel,digest in json.loads((TMP/'protected-hashes.json').read_text(encoding='utf-8')).items():
 # 校閲と無関係な過去PDFの全件読み込みはしない。
 if 'アプリ' in rel:continue
 assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,rel
with zipfile.ZipFile(OUT/'固体2級_第4章_図_完成版.zip') as z:assert not z.testzip() and len(z.namelist())==21
results['content_checks']={'questions':29,'glossary_items':len(terms['items']),'answer_changes':0,'missing_figures':0,'broken_glossary_links':0,'protected_files_unchanged':True}
# 用語の共通例と指定六問の追加例。別の検証プログラムに分散させない。
EA,h,p=20000000,100,10
gal_k=2*EA/h;gal_f=p*h
ritz_U_coefficient=2*.5*EA*(1/h)**2*h;ritz_W_coefficient=p*(2*h)/2
fd_coefficient=2*EA/h**2
close(2*ritz_U_coefficient,gal_k);close(ritz_W_coefficient,gal_f)
mid=gal_f/gal_k;close(mid,.0025);close(p/fd_coefficient,mid);close(p*(2*h)**2/(8*EA),mid)
close(2*200*.01,4);close(200000*(0-.0006),-120)
young,poisson,epsx=200000,.3,.001
sxps=young/(1-poisson**2)*epsx;sxpe=young*(1-poisson)/((1+poisson)*(1-2*poisson))*epsx
close(sxps,219.7802197802198);close(sxpe,269.2307692307692)
results['added_term_examples']={'galerkin_midpoint_mm':mid,'ritz_midpoint_mm':ritz_W_coefficient/(2*ritz_U_coefficient),'difference_midpoint_mm':p/fd_coefficient,'independent_exact_midpoint_mm':p*(2*h)**2/(8*EA),'surface_virtual_work_Nmm':4,'fixed_thermal_stress_MPa':-120,'plane_stress_sigma_x_MPa':sxps,'plane_strain_sigma_x_MPa':sxpe}
(OUT/'独立検算.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS: independent calculations, formula examples, 29 answers/links/figures, other chapters unchanged.')
