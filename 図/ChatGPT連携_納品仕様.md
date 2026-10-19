# ChatGPT 納品フォーマット仕様(案B)＋反映手順(案A)

目的: ChatGPT からの修正を**変換ゼロ・1コマンド**でアプリへ反映できるようにする。
正本は「完成版の問題JSON」1本だけ。text_patches / option_order_changes / questions_patch などの中間ファイルは**不要**(監査用に添付は自由だが反映には使わない)。

---

## 1. ChatGPT に出してもらう正本フォーマット(アプリ直系スキーマ)

分野級ごとに1ファイル。全章まとめて1ファイルでよい(問番号で章を自動判定するため)。

```json
{
  "correctAnswerIndexBase": 1,
  "questions": [
    {
      "number": "9-2",
      "title": "……",
      "question": "……($…$ でKaTeX可)",
      "choices": ["肢1", "肢2", "肢3", "肢4"],
      "answer": 2,
      "explanation": "……"
    }
  ]
}
```

ルール:
- **キーはアプリと同じ**: `choices`(配列)・`answer`(**1始まり**の整数)・`question`・`title`・`explanation`。
  - 旧式の `options` / `correctAnswer` でも受け付ける(自動変換)が、新式推奨。
- `number` は **"章-通し番号"**(例 `9-2`)。これで対象ファイルを自動判定する。
- **選択肢の数は変えない**(並べ替え・文言修正は可。数を増減すると FAIL)。
- 並べ替えをした場合は、`choices` を**並べ替え後の順**で書き、`answer` を**その順での正解番号**にする(差分やold/newの指示は不要。完成形だけでよい)。
- **図は原則書かない**。図を変える時だけ `figure`("required"/"helpful"/"none")・`figureImage`・`preFigureImage` を含める。含めなければ既存の図設定はそのまま保持される(=図を誤って消さない)。図そのもの(SVG/PNG)の反映は別工程 `deploy_recheck_figures.py` が担当。
- 全文は UTF-8。`\n`(本文中の改行)は**実際の改行**で。リテラルな `\\n` を書かない。

---

## 2. 反映手順(案A・1コマンド)

```bash
# dry-run（差分だけ表示・書き込まない）
python tools/apply_content.py <正本.json> --field solid2

# 本番反映（全章まとめて）
python tools/apply_content.py <正本.json> --field solid2 --write
```

- `--field` は分野級: `solid2`(固体2級=無印13ファイル) / `solid1` / `thermal1` / `thermal2` / `vib1` / `vib2`。
- **章ごとに叩く必要なし**。問番号から対象ファイルを自動で振り分けて一括反映。
- 安全装置: 選択肢数の不一致・answer範囲外・番号不在があると **FAILとして中止**(壊れた正本をそのまま書き込まない)。
- 図フィールドは正本に書いた時だけ反映。書かなければ従来どおり保持。

### 図も一緒に反映する場合(従来どおり)
```bash
python tools/deploy_recheck_figures.py <章> --write
```
(図パックの SVG を Chrome で PNG 化し assets/figures へ。manifest=figure_manifest.json)

---

## 3. 旧方式との対応(なぜ楽になったか)

| 旧 | 新(本仕様) |
|---|---|
| questions_verified / text_patches / option_order_changes / questions_patch と複数の中間JSON | **正本1本**だけ |
| `apply_recheck_patch.py` を章ファイルごとに手動で5回 | `apply_content.py … --field solid2 --write` の**1回** |
| 章↔ファイル対応表を各ツールに手書き | 問番号から**自動判定**(手書き表なし) |
| `options→choices` / `correctAnswer→answer` の変換を意識 | ChatGPTが**アプリと同じキー**で出す(変換不要) |

※ 従来の `apply_recheck_patch.py` も残置(過去パック互換)。今後の本文反映は `apply_content.py` を標準とする。
