# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第4章_反映結果';TMP=ROOT/'tmp/pdfs/ch4_review'
data=json.loads((ROOT/'content/questions/fem-basics.json').read_bytes());old=json.loads((TMP/'fem-basics-before.json').read_bytes());oldqs={q['number']:q for q in old['questions']}
mapping=json.loads((OUT/'図マッピング.json').read_text(encoding='utf-8'))
notes={
1:'不定形の離散化図を、厚みと貫通穴をもつ実在可能な板部品のモデルへ変更。三角形要素と節点を区別する。',
2:'離散化と連立方程式の反復解法を、二つの計算段階として簡潔に区別する。',
3:'元の問題はガラーキン法による対称性を中心にしており、対応する公式問題の残差・重み・積分条件という主題からずれていた。残差の定義とガラーキン重みを主題へ戻す。',
4:'元の単独のエネルギー計算0.625Jは正しいが、力一定と伸び一定で比較が逆転する論点が抜けていた。独自の段付き棒と一様棒を比較する問題にする。',
5:'エネルギー密度、1/2、工学せん断ひずみを明示し、難しいテンソルの二重積を前面に出さない。',
6:'元の変分原理の許容場の比較は正しいが、線形・非線形で二つのエネルギーが等しいかという主題からずれていた。曲線での面積の区別へ戻す。',
7:'微分が必要な箇所では、一次微分による釣合いと二次微分による最小判定を順に説明する。',
8:'公式と同じ応力法・補仮想仕事の対応を追加する。未知量と仮に変化させる量を図で対比する。',
9:'固定支持点A・Bと自重無視を明示。30°・60°の独自設定を水平・鉛直力から検算し、図の角度も合わせる。',
10:'静的平衡と最小ポテンシャルエネルギーの対応が分かるよう、安定な線形弾性・保守荷重の前提を明示する。',
11:'弱形式が代替する平衡式と、別に必要な材料則・ひずみ変位関係・指定変位を区別する。',
12:'表面力は単位面積当たり、表面での積分、仕事のN mへの単位確認を一つずつ説明する。',
13:'初期ひずみをDで応力へ変える理由と、内力式から右辺への移項を示す。英語主体の旧図を日本語の対応図へ変更。',
14:'残差→重み→積分→部分積分→内部仕事・表面項の順に説明する。',
15:'形状関数は節点値から変位を補う重み。和が1なら同じ平行移動を再現することを式で示す。',
16:'1/4と3/4の重み、途中の加算、右端に近い値になる検算を残す。',
17:'垂直ひずみの微分方向と、二つの角度変化の和としての工学せん断を説明する。',
18:'一定応力には一定Dだけでなく初期応力・初期ひずみの条件も必要。初期項なしを明記する。',
19:'Nは変位、Bはひずみ、Dは応力への変換という流れに絞る。',
20:'元のCSTの一定Bの性質は4-18と重複し、公式のB成分の並べ方の論点が抜けていた。自由度順を明示し、各行をひずみの式から作る問題へ戻す。',
21:'問題文の「両者」が何を指すか不明。平面応力と平面ひずみを明示する。',
22:'元の変位累積計算は正しいが、公式の剛性方程式の係数を作る論点が抜けていた。独自の二ばねの式を節点ごとに作る。',
23:'元の単一斜めばねの混合成分は正しいが、公式の斜め二本と水平ばねの剛性方程式の論点が不足。cosの二回の投影と二本の加算を説明する。',
24:'公式抽出の「非対角項は負」は一般要素へ無条件に広げられない。対称・正の対角を中心にし、斜め要素の正の非対角を例として区別する。',
25:'行和0の説明を拘束前の一次元系に限定し、全成分1のベクトルとの積として示す。',
26:'元の対角剛性の数値計算は正しいが、公式の「変位は共通・力は加算」の関係が直接問われていなかった。共有節点の組立てへ戻す。',
27:'反力と既知集中外力を区別し、境界条件・自由度の用語リンクを付ける。',
28:'独立な指定成分を一つずつ数え、10−4=6を検算。境界条件・自由度へリンクする。',
29:'三角形だけでなく、公式と同じ四面体の体積座標の論点も含める。3個と4個の座標と重心を対比する。'}
report='# 第4章 校閲・反映結果\n\n2026-10-14。公式PDFは参照せず、抽出テキスト「固体2級_04_有限要素法の定式化.md」の問題側・解説側の全29問に照合。問題文・設定・図・解説は独自作成。\n\n「要修正」は作業前の判定。全問で指定四節と番号別誤答説明が不足していたため、物理的な正誤とは別に体裁修正が必要。元の計算が正しい問題も、公式の学習ポイント不足ならその理由を区別して記載。以下の修正案は実ファイルへ適用済み。\n\n'
for q in data['questions']:
 n=int(q['number'].split('-')[1]);oq=oldqs[q['number']]
 report+=f'## {q["number"]}：要修正（反映済み）\n\n〔誤り〕指定四節と番号別の誤答説明が未完備。'
 if n in (3,4,6,8,20,22,23,26,29):report+='公式の学習ポイントにも不足・ずれがあった。'
 if n in (9,10,18,21):report+='問題文の前提・指示にも補足が必要。'
 report+=f'\n\n〔理由〕{notes[n]}\n\n〔修正案〕正解は{q["answer"]}、番号の変更なし。'
 if oq['question']!=q['question'] or oq['choices']!=q['choices']:
  report+='次の独自問題へ差し替え。\n\n'+q['question']+'\n\n'
  for i,c in enumerate(q['choices'],1):report+=f'{i}. {c}\n'
 report+='\n\n解説の具体文言：\n\n'+q['explanation'].replace('\n','\n\n')+'\n\n'
 if q['number'] in mapping:report+=f'〔図が必要〕{notes[n]} 使用図：{mapping[q["number"]]["after_svg"]}\n\n'
 else:report+='〔図〕既存図で十分。図の内容と修正後の説明が整合することを確認。\n\n'
report+='## 総括\n\n29問を技術・条件・選択肢・四節・公式の学習ポイントの観点で確認し、全問へ新原則を適用。正解番号・ID・公式参照は全問維持。計算問題と関連用語の数値例を独立に解き直し、単位も確認。14用語への44リンクが解決することを確認。\n\n4-1は追加指示により、厚みと貫通穴をもつ板部品と、その三角形メッシュを対比する立体図へ更新。\n\n規定名PDF：回答前12ページ（問題29問・与件図7点）、回答後72ページ（各問の問題・図と解説を分けた58ページ＋関連用語14ページ）。全84ページをレンダリングして目視確認。数式表示エラー・画像欠落・はみ出しなし。回答前に答えの情報を含まない。44内部リンクは対応する用語ページへ到達。\n\n補助的な理論確認：[MIT・仮想仕事とFEM](https://ocw.mit.edu/courses/res-2-002-finite-element-procedures-for-solids-and-structures-spring-2010/cfd7146f3ce0fdfb261ddf4aa1f43492_20WSeL4tz2k.pdf)、[Illinois・微小ひずみ](https://mechref.engr.illinois.edu/sol/strain.html)。公式問題の出題範囲照合はローカル抽出テキストのみを使用。\n'
(OUT/'第4章_校閲・反映結果.md').write_text(report,encoding='utf-8')
record='# 第4章 完成記録\n\n'+report.split('## 総括\n\n')[1]+'\n\n再生成は tools/apply_solid2_ch4_review.py → tools/solid2_ch4_review_figures.py → tools/gen_figures_ts.py → tools/build_solid2_ch4_review_pdfs.py → tools/print_solid2_ch4_review_pdfs.cjs。検算は tools/verify_solid2_ch4_review.py、数式は tools/check_solid2_ch4_katex.cjs、PDFは tools/verify_solid2_ch4_pdfs.py。PDF生成は4章限定。他章は変更しない。\n\n3-1は利用者が承認した以前の「温度勾配2倍→熱流束の大きさ2倍」の比較図 solid2Ch3Review01After を維持。60℃・20℃と符号を主役にする図は採用しない。現在の参照と図の内容を確認済み。\n'
(OUT/'第4章_完成記録.md').write_text(record,encoding='utf-8')
for path in (ROOT/'CODEX_作問・校閲・解説方針.md',ROOT/'CODEX_引き継ぎ_固体2級_解説体裁統一.md'):
 text=path.read_text(encoding='utf-8')
 marker='\n## 第4章の適用と4-1図の修正（2026-10-14）\n'
 if marker in text:text=text.split(marker)[0]
 text+=marker+'\n第4章29問へ最新原則を適用済み。公式資料は抽出済みの第4章テキストのみを使用。重み付き残差、力一定と伸び一定のエネルギー比較、応力法と補仮想仕事、B行列の成分順、斜めばねの剛性方程式、共有節点の組立て、体積座標を公式の論点に合わせた。正解番号・ID・officialRefは維持。問題JSONは content/questions/fem-basics.json、用語は content/formulas/ch4.json。14用語への44リンクを検証。\n\n4-1は利用者の追加指示で、厚みと貫通穴をもつ板部品と同じ形状の三角形メッシュを対比する立体図へ修正。新キー solid2Ch4Review01After。規定SVG/PNG、節点・要素の区別を日本語ラベルで明示。複雑さを増やすだけの図にせず、実際の部品と有限要素モデルの対応を分かりやすく示す。\n\n3-1は承認済みの比較図 solid2Ch3Review01After を採用し続ける。温度60℃・20℃と符号を中心にする案は採用しない。\n\nPDFは アプリ/固体2級/固体2級_第4章_有限要素法の定式化_回答前.pdf（12ページ）と回答後.pdf（72ページ）。回答後は関連用語14ページ付き。検算・KaTeX・リンク・全ページ目視確認済み。詳細と再生成手順は output/固体2級_第4章_反映結果/第4章_完成記録.md。次の未着手章は第5章。4章の更新スクリプト以外の旧図生成を不用意に実行しない。\n'
 if path.name.startswith('CODEX_引き継ぎ'):
  text=text.replace('**第4〜13章: 未着手（これが残タスク）。**','**第4章: 校閲・四節・図・用語リンク・PDFまで完了（末尾の最新完成記録参照）。**\n- **第5〜13章: 未着手（これが残タスク）。**')
 path.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
outputs=[ROOT/'アプリ/固体2級'/f'固体2級_第4章_有限要素法の定式化_{mode}.pdf' for mode in ('回答前','回答後')]
(OUT/'成果物SHA256.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Review, completion record, handoff and principles saved.')
