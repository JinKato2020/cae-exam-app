from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第3章_反映結果'
assert (ROOT/'_原本(非公開)/_抽出テキスト').is_dir()
q=json.loads((ROOT/'content/questions/heat-basics.json').read_text(encoding='utf-8'))
f=json.loads((ROOT/'content/formulas/ch3.json').read_text(encoding='utf-8'))
ids={it['id'] for it in f['items']};assert len(ids)==13
linked=[it['number'] for it in q['questions'] if 'heat-transfer-rate-resistance' in it['relatedFormulas']]
assert linked==['3-5','3-9','3-10','3-11','3-12','3-14','3-15']
for it in q['questions']:
    assert all(k in ids for k in it['relatedFormulas'])
for it in f['items']:
    assert Image.open(ROOT/'assets/figures'/f"{it['figureImage']}.png").size[0]>0
snap=json.loads((ROOT/'tmp/pdfs/ch3_aligned/before-hashes.json').read_text(encoding='utf-8'))
for name,digest in snap.items():
    name=name.replace('\\','/')
    if name in ('content/questions/heat-basics.json','content/formulas/ch3.json') or '固体2級_第3章_' in name:continue
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
with zipfile.ZipFile(OUT/'固体2級_第3章_図_完成版.zip') as z:assert len(z.namelist())==25 and z.testzip() is None
v=json.loads((OUT/'PDF出力検証.json').read_text(encoding='utf-8'))
assert v['回答前']['pages']==9 and v['回答後']['pages']==36
v['目視確認']='回答前9ページ・回答後36ページの全45ページを目視確認。図・数式・4節の欠落、重なり、はみ出しなし。'
v['用語リンク']={'app_all_questions_resolve':True,'new_term_questions':linked,'pdf_links':7,'pdf_destination_page':35}
v['最新ファイル']='固体2級_第3章_熱伝導の基礎_回答前_原則反映版.pdf / 固体2級_第3章_熱伝導の基礎_回答後_原則反映版.pdf'
(OUT/'PDF出力検証.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
notes={
1:'承認された簡潔な説明と勾配2倍・熱流束2倍の図を維持。',2:'構造と熱の対応を式の役割として説明。材料係数の位置を補足。',
3:'定常は各場所の温度が時間で変わらないこと。簡潔な説明を維持。',4:'評価された平板・円筒の比較図を維持。面積から温度曲線を判断。',
5:'高校生向けに勾配の式を両層へ適用する手順と、厚さを含む温度降下を補足。',6:'F・D・Hを分けた丁寧な図と、断熱の方向・流入の符号を維持。',
7:'内部発熱Hへそろえ、二回積分の途中式・積分定数の意味を補足。',8:'Hを使い、発熱分Hxの意味・単位と温度曲線の向きを説明。',
9:'公式の外表面熱流束の式と半径a・bを採用。面積換算を順に説明。',10:'熱通過率Kの問題・四選択肢・導出・図へ改訂。三区間の温度差を足す。',
11:'熱通過率Kで案を比較。変更後1/KとKを両方計算し、関係を明示。',12:'二層壁のKから流束を求め、局所のh₂から表面温度を求める。',
13:'λとhの場所・自由電子の役割を簡潔に説明。',14:'h₁・h₂と温度差の逆比を式で確認。候補図の縦の温度差を比較。',
15:'半径a・b、h₁・h₂へそろえ、Qが共通で温度差の比を取る手順を補足。',16:'対称面を横切る熱だけが0。方向を図で説明。',17:'内外の熱伝達と、軸方向一様による切断面の断熱を説明。'}
text='''# 第3章 原則反映版の完成記録

この文書が第3章の最新の適用結果。以前の「記録のみ」「3-10未改訂」は履歴であり、現在は問題・解説・図・用語・リンクへ実際に適用済み。

原則：可能な範囲でシンプルに。工学系高校生が難しいと感じる場合は、前提・式の意味・途中計算・単位・理由を丁寧に説明。図も必要な情報へ絞り、難しい条件は分けて示す。公式と同じ学習ポイント・用語・主役の公式を使い、問題設定・文章・図は独自にする。

今回の確認では公式第3章の問題・解説を照合した。3-10・3-11では熱通過率K、q=K(Th−Tc)、1/K=1/hh+t/λ+1/hcが主役。問題集の34ページ、解説195・196ページで確認。以後は利用者指定の `_原本(非公開)/_抽出テキスト` から各章の問題・解説を取得し、PDFを読み直さない。

## 各問の適用

| 問題 | 適用内容 | 解説文字数 |
|---|---|---:|
'''
for it in q['questions']:
    n=int(it['number'].split('-')[1]);text+=f"| {it['number']} | {notes[n]} | {len(it['explanation'])} |\n"
text+='''
## 用語・リンク・検証

用語「熱通過率Kと熱抵抗Rの関係」を図と数値例付きで追加。面積当たりはq=KΔT、全体はQ=Aq=KAΔT=ΔT/R、R=1/(KA)。KはW/(m²K)、1/Kはm²K/W、RはK/W。面積2m²の例ではK=4、q=200、Q=400、R=0.125を検算。

関連7問は3-5・3-9・3-10・3-11・3-12・3-14・3-15。既存の古い関連IDも実在する用語IDへ修正し、全17問の関連リンクが解決。第3章用語の重複LaTeXエスケープを整えた。アプリと同じKaTeX 0.16.9で問題・全13用語の276式を検証、エラー0。

第3章だけの最新PDFは「_原則反映版.pdf」。回答前9ページ、回答後36ページ。回答後の35・36ページに用語の図と計算例を収録。関連7問から35ページへの内部リンク7件を検証。全45ページを目視確認、文字はみ出し0、数式描画エラー0、画像欠落0、4節欠落0。

全17問の独立検算を再実施。正解番号・id・公式参照は維持。必要な記号・主役の公式に合わせて問題文・選択肢も改訂。他章の問題・用語JSONとPDFはSHA-256で不変を確認。図ZIPは24SVG＋配置指示の25ファイル、破損なし。commit・push・OTA配信・アプリビルドは行っていない。

今後の継続原則と学びは、ルートの `CODEX_作問・校閲・解説方針.md` に保存した。作業途中の入出力・ログ・画像プレビューは会話に表示しない。
'''
(OUT/'第3章_原則反映版_完成記録.md').write_text(text,encoding='utf-8')
older=OUT/'第3章_改訂版_反映結果.md';content=older.read_text(encoding='utf-8')
if not content.startswith('> 旧版'):
    older.write_text('> 旧版の履歴。最新の適用結果は「第3章_原則反映版_完成記録.md」を参照。3-10の未改訂状態は解消済み。\n\n'+content,encoding='utf-8')
