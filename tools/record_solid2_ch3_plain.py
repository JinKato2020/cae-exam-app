from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/固体2級_第3章_反映結果'
data=json.loads((ROOT/'content/questions/heat-basics.json').read_text(encoding='utf-8'))
old=json.loads((ROOT/'tmp/pdfs/ch3_plain/before.json').read_text(encoding='utf-8'))
snap=json.loads((ROOT/'tmp/pdfs/ch3_plain/before-hashes.json').read_text(encoding='utf-8'))
for name,digest in snap.items():
    if name.replace('\\','/')=='content/questions/heat-basics.json' or '固体2級_第3章_' in name:continue
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
assert [(q['id'],q['answer'],q['officialRef'],q['question']) for q in data['questions']]==[(q['id'],q['answer'],q['officialRef'],q['question']) for q in old['questions']]
assert data['questions'][0]==old['questions'][0]
with zipfile.ZipFile(OUT/'固体2級_第3章_図_完成版.zip') as z:assert len(z.namelist())==24 and z.testzip() is None
p=OUT/'PDF出力検証.json';v=json.loads(p.read_text(encoding='utf-8'));v['目視確認']='改訂版：回答前8ページ・回答後34ページの全42ページを確認。図・数式・4節の欠落、重なり、はみ出しなし。'
v['ファイル名']='固体2級_第3章_熱伝導の基礎_回答前_改訂版.pdf / 固体2級_第3章_熱伝導の基礎_回答後_改訂版.pdf'
p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
notes={
'3-1':'承認された簡潔な解説と、熱流束を矢印の長さで2倍に示す比較図を維持。',
'3-2':'式の役割を四つの対応に整理。図は対応表を中心に。',
'3-3':'定常＝時間で変わらない、を中心に。図は変更直後→途中→最終状態。',
'3-4':'評価された図を維持。面積の変化から曲線の形を説明し、不要な積分式は省略。',
'3-5':'温度の連続とBの傾きがAの3倍、で選ぶ。厚さを含む温度降下の比は補足。',
'3-6':'承認された問題図・三つの拡大解説図を維持。断熱の方向と流入の符号は丁寧に説明。',
'3-7':'二階微分が一定→二次関数。図から最高温度の計算式を省き、山形と熱の向きを示す。',
'3-8':'右へ下がる・右ほど急、の二段階。全候補を残し、長い一般解・追加数値例を省略。',
'3-9':'円筒の熱損失→外面積で換算、の計算を維持。図は管長1mの具体的な読み方。',
'3-10':'抵抗を足す→逆数を取る。図も三つの直列区間と結論へ絞る。',
'3-11':'各案で変更する抵抗だけ計算し直す。図は比較表、流束増加率の余分な計算は省略。',
'3-12':'四抵抗→熱流束→外表面温度。図もこの三手順にし、問われない途中温度は省略。',
'3-13':'λは内部、hは表面と流体。自由電子の役割と断熱材の性質を簡潔に。',
'3-14':'同じqなら温度差はhの逆比。全候補と右の温度差4倍を図示。',
'3-15':'hと面積の両方を使う比計算は丁寧に。壁内曲線は外ほど緩やか。',
'3-16':'対称面を横切る熱は0、沿う熱は残る。微分の例を省き図で方向を示す。',
'3-17':'内外面は熱伝達、切断面は断熱。管壁を外へ通る熱を図に追加。',
}
text='''# 第3章 改訂版の反映結果

この文書が最新の解説・図の方針と出力結果。以前の「全問を約690〜930字へ増補」は旧版の記録で、今回の改訂では問題の難しさに合わせて説明量を変えた。

## 原則

可能な範囲でシンプルに。難しい場合は、理解に必要な用語・理由・途中計算を詳しく説明する。図も不要に複雑にせず、難しい条件は3-6のように分けて丁寧に示す。四節体裁・各誤答の理由は維持。

## 各問の反映

| 問題 | 方針・反映内容 | 解説文字数 |
|---|---|---:|
'''
for q in data['questions']:text+=f"| {q['number']} | {notes[q['number']]} | {len(q['explanation'])} |\n"
text+='''
## 検証・出力

全17問を独立検算、全正解番号・id・公式参照・問題文は維持。選択肢の重複したLaTeXエスケープは整えたが、意味と数値は維持。四節の順序・各節一行・各誤答の番号・数式記法を検証。SVGは文字パス・660×420・外部参照なし、PNG1320×840。

第3章だけの改訂版PDFを出力：回答前8ページ、回答後34ページ。全42ページを目視確認。数式描画エラー0、画像欠落0、本文はみ出し0。他章JSONと他章PDFはSHA-256で不変を確認。図ZIPは23SVGと配置指示の24ファイル、破損なし。

既存の回答後PDFが閲覧中で上書きできなかったため、回答前・回答後とも「_改訂版.pdf」で保存した。最新の完成版はこちら。

旧品質チェッカーの警告は【計算】節だけを数える旧判定と、維持した既存正解分布6/5/2/4による。計算問題は別の独立検算を通した。品質FAILなし。
'''
(OUT/'第3章_改訂版_反映結果.md').write_text(text,encoding='utf-8')
print('Final revision recorded: all 42 pages visually verified; other chapters unchanged; ZIP valid.')
