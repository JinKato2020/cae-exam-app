from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
ex=r'''【基礎】物体の内部で、高温側から低温側へ熱が伝わる関係を表すのがフーリエ則です。熱流束は、単位面積を通る熱の流れの強さ。温度勾配は、距離に対して温度がどれだけ変わるかを表します。
【考え方】同じ材料では、温度勾配が大きいほど熱流束も大きくなります。熱伝導率が一定なら両者は比例するので、温度勾配を2倍にすると熱流束の大きさも2倍です。熱は高温側から低温側へ流れるため、温度が増える向きとは逆になります。したがって正解は1です。
【ポイント】覚える中心は「フーリエ則」「熱は高温から低温へ」「勾配2倍なら熱流束も2倍」の三つです。式は $q_x=-\lambda\,\partial T/\partial x$。マイナスは熱が温度の下がる向きへ流れることを示します。
【引っかけ】(2)ニュートン冷却則は、物体表面と周囲の流体との熱のやり取りです。(3)ステファン・ボルツマン則は熱放射の関係です。(4)熱容量は、温度を上げるのに必要な熱の量に関係します。どれも本問の「固体内部の温度勾配と熱流束」の関係ではありません。'''
def enc(d):return (json.dumps(d,ensure_ascii=False,indent=2).replace('\n','\r\n')+'\r\n').encode('utf-8')
p=ROOT/'content/questions/heat-basics.json';raw=p.read_bytes();d=json.loads(raw);assert enc(d)==raw
old=json.loads(raw);q=next(q for q in d['questions'] if q['number']=='3-1');q['explanation']=ex
assert q['answer']==1 and len(ex.splitlines())==4
for a,b in zip(old['questions'],d['questions']):
    if a['number']!='3-1':assert a==b
p.write_bytes(enc(d));(ROOT/'output/固体2級_第3章_反映結果/第3章_完成問題.json').write_bytes(enc(d))
p=ROOT/'tools/apply_solid2_ch3_review.py';t=p.read_text(encoding='utf-8');start=t.index("'3-1':r\"\"\"");end=t.index("'3-2':",start)
t=t[:start]+"'3-1':r\"\"\""+ex+'""",\n'+t[end:];p.write_text(t,encoding='utf-8',newline='\r\n')
print('3-1 only: concise four sections applied; other questions unchanged.')
