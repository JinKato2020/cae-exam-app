# 問題コンテンツ（CAE試験対策）

アプリが読み込む「問題・正解データ」を置く場所。1問＝1レコードのJSON。

## 構造
- `index.json` … 全体の索引（級・章・ファイル・問題数）
- `questions/<級>-<章>.json` … 問題本体（`meta` ＋ `questions[]`）

## 問題レコードのスキーマ
| キー | 型 | 説明 |
|---|---|---|
| `id` | string | 一意ID（例 `solid2-math-1-1`） |
| `number` | string | 問題番号の表示（例 `問1-1`） |
| `question` | string | 問題文 |
| `choices` | string[] | 選択肢（通常4つ） |
| `answer` | number | 正解の選択肢番号（1始まり） |
| `explanation` | string | 解説 |
| `hasMath` | boolean | 数式を含むか（将来の数式表示用フラグ） |

## 注意
- 元PDFはスキャン画像のため、OCRではなく画面を読んで手作業でデータ化している。
- 各章の解答は現状「問題編本文からの読み取り」。公式解答冊子（解説編）との照合は別途。
