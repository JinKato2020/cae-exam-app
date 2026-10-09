#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""正本JSON(完成版)を content/questions へ**全章まとめて1コマンドで**反映する統合ツール(2026-10-09)。
= 従来 apply_recheck_patch.py を章ごとに5回叩いていた「本文反映」の簡略版(案A)。
  さらに ChatGPT がアプリ直系スキーマ(choices/answer)で納品しても、旧スキーマ(options/correctAnswer)でも
  どちらでも受け付ける(案B)。問番号("9-2")から対象ファイルを自動判定するので章↔ファイル対応表は不要。

正本フォーマット(どちらでも可・correctAnswerIndexBase=1前提):
  list[ {id|number, title?, question?, choices|options?, answer|correctAnswer?, explanation?} ]
  または {correctAnswerIndexBase, questions:[ 同上 ]}
図フィールド(figure/figureImage/preFigureImage)は、正本に明示的に含まれる時だけ更新。
  含まれない=触らない(図反映は deploy_recheck_figures.py の担当。誤って図を剥がさない)。

分野の絞り込み(--field): 問番号は分野をまたいで重複しうるので必須。
  solid2 = 無印13ファイル / solid1・thermal1・thermal2・vib1・vib2 = 同名接頭辞のファイル群。

安全: 選択肢数の不一致・answer範囲外・番号不在 は FAIL として集計し、FAILのある章は --write でも書かない。
使い方:
  python tools/apply_content.py <正本.json> --field solid2            # dry-run(差分表示のみ)
  python tools/apply_content.py <正本.json> --field solid2 --write    # 全章へ書込
"""
import json, sys, os, glob, re
from collections import defaultdict

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(CAE, "content", "questions")
KNOWN_PREFIXES = ("solid1-", "thermal1-", "thermal2-", "vib1-", "vib2-", "solid2-")

def field_files(field):
    names = [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(QDIR, "*.json"))]
    if field == "solid2":   # 無印(既知接頭辞を持たない)=固体2級
        sel = [n for n in names if not any(n.startswith(p) for p in KNOWN_PREFIXES)]
    else:
        sel = [n for n in names if n.startswith(field + "-")]
    return sorted(sel)

def norm_item(it):
    """正本1件→(番号, {アプリスキーマのフィールド})。旧新どちらのキーも受ける。"""
    num = it.get("number") or it.get("id")
    f = {}
    for k in ("title", "question", "explanation"):
        if k in it: f[k] = it[k]
    if "choices" in it: f["choices"] = it["choices"]
    elif "options" in it: f["choices"] = it["options"]
    if "answer" in it: f["answer"] = it["answer"]
    elif "correctAnswer" in it: f["answer"] = it["correctAnswer"]
    for k in ("figure", "figureImage", "preFigureImage"):   # 明示時のみ
        if k in it: f[k] = it[k]
    return num, f

def main():
    if len(sys.argv) < 2 or "--field" not in sys.argv:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    field = sys.argv[sys.argv.index("--field") + 1]
    WRITE = "--write" in sys.argv

    doc = json.load(open(src, encoding="utf-8"))
    items = doc["questions"] if isinstance(doc, dict) and "questions" in doc else doc
    base = doc.get("correctAnswerIndexBase", 1) if isinstance(doc, dict) else 1
    if base != 1:
        print("ABORT: correctAnswerIndexBase=%s (本ツールは1前提)" % base); sys.exit(1)

    files = field_files(field)
    if not files:
        print("ABORT: field=%s に該当する content ファイルがありません" % field); sys.exit(1)
    # 番号→ファイル の索引(章マップ不要)
    num2file, data_cache = {}, {}
    for fn in files:
        d = json.load(open(os.path.join(QDIR, fn + ".json"), encoding="utf-8"))
        data_cache[fn] = d
        for q in d.get("questions", []):
            num2file[q.get("number")] = fn

    per_file_changes = defaultdict(list)   # fn -> [(num, [changed fields])]
    fails, nomatch = [], []
    for it in items:
        num, fields = norm_item(it)
        fn = num2file.get(num)
        if not fn:
            nomatch.append(num); continue
        q = {x.get("number"): x for x in data_cache[fn]["questions"]}[num]
        # 検証
        if "choices" in fields:
            if not isinstance(fields["choices"], list) or len(fields["choices"]) != len(q.get("choices", [])):
                fails.append((num, "choices数不一致 %s→%s" % (len(q.get("choices", [])), len(fields.get("choices", []))))); continue
        if "answer" in fields:
            n = len(fields.get("choices", q.get("choices", [])))
            if not (1 <= fields["answer"] <= n):
                fails.append((num, "answer範囲外 %s/%s" % (fields["answer"], n))); continue
        changed = [k for k, v in fields.items() if q.get(k) != v]
        if changed:
            per_file_changes[fn].append((num, changed))
            if WRITE:
                for k in changed: q[k] = fields[k]
                if any(k in changed for k in ("question", "explanation", "choices")):
                    q["hasMath"] = ("$" in str(q.get("question", "")) or "$" in str(q.get("explanation", ""))
                                    or any("$" in c for c in q.get("choices", [])))

    # 報告
    print("=== field=%s / 対象ファイル=%d / 正本=%d件 ===" % (field, len(files), len(items)))
    tot = 0
    for fn in sorted(per_file_changes):
        ch = per_file_changes[fn]; tot += len(ch)
        fc = defaultdict(int)
        for _, ks in ch:
            for k in ks: fc[k] += 1
        print("  %-28s 変更=%2d  %s" % (fn, len(ch), dict(fc)))
    print("--- 変更予定=%d問 / 別分野スキップ(番号不在)=%d / FAIL=%d ---" % (tot, len(nomatch), len(fails)))
    if fails:
        for n, why in fails[:20]: print("  ★FAIL", n, why)
        print("FAILがあるため書込中止(--writeでも)。正本を確認してください。"); sys.exit(2)
    if WRITE:
        for fn in per_file_changes:
            p = os.path.join(QDIR, fn + ".json")
            with open(p, "w", encoding="utf-8", newline="\r\n") as f:
                json.dump(data_cache[fn], f, ensure_ascii=False, indent=2); f.write("\n")
            print("WROTE", p)
    else:
        print("(dry-run。書き込むには --write)")

if __name__ == "__main__":
    main()
