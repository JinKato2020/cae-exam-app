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

---

## 4. 内容方針(必読・2026-10-16-R16)

**公式問題集の問題に記載のない要点・用語・出題傾向を勝手に付け足さないこと。** 受験生にとって不要な用語や問題の傾向を増やすと負担になる。あくまで**最低限の労力で合格できる範囲**に絞る。

- 解説(explanation)は、その**原問が問うている点を理解するのに必要な範囲だけ**書く。問題文・公式問題に無い論点、発展的な話題、余談、別解の網羅、新しい専門用語の導入はしない。
- 「難所は丁寧に説明」は、原問の論点を噛み砕くことであって、**新しい要点を足すことではない**。易しい問題は短く。
- 公式にない名称・専門用語で言い換えない。平易な日本語で、原問の範囲内で説明する。
- この原則は全分野・全級に適用する。チェックは `tools/check_quality.py` が脱線・発展を示す語(参考までに/発展として/余談 等)をWARNで検出するが、**最終判断は公式問題と照合して人/AIが行う**(WARNはFAILにしない)。
- 詳細の経緯は `CODEX_作問・校閲・解説方針.md` / `CODEX_引き継ぎ.md` の 2026-10-16-R16 を参照。

## 5. 図ファイルの必要セットと不要画像をためない（2026-10-17-IMG-CLEANUP）

納品図が最終的にアプリへ出る経路と、どれが“必要な正本”かを明確にして、幽霊PNGの堆積を防ぐ。

- **アプリ表示に必要なのは2種だけ**：(a) `assets/figures/<キー>.png`（全問題/用語JSONの figureImage・preFigureImage のキー。`tools/gen_figures_ts.py` が `src/figures.ts` を自動生成）＋ (b) 相関図 `map_<field>_<級数字>_{all,chN}.png`（OTAで解決）。納品図はこのキー体系に載せて初めて表示される。
- **図の原本は `図/<分野級>/第NN章/*.svg`**。`図/**/*.png` や各種レンダ出力は原本から再生成できる中間物＝正本ではない。差し替え時は原本svgとキーを更新し、旧版PNGは残さない。
- **ためない**：`tmp/`（レンダ中間物・配信済みzip・孤立worktree）、`tools/_srcimg/`（gitignore済の一時素材）、`assets/figures` の孤立PNG（キー差し替え後の旧図）は不要。定期掃除の対象。
- **掃除の安全則**：`tmp/` はCodexとの共有作業領域で生きたgit worktreeが入り得る→一括削除しない（`git worktree list` で除外）。`.git` 履歴の縮小はSHAが変わりOTA配信基準が壊れるため軽々に行わない。詳細は `CODEX_作問・校閲・解説方針.md` / `CODEX_引き継ぎ.md` の 2026-10-17-IMG-CLEANUP を参照。

