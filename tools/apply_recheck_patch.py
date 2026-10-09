#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ChatGPT再チェックパッチ(JSON)を content/questions の問題JSONへ反映する恒久ツール(2026-10-09)。
対応パッチ形式(どちらも correctAnswerIndexBase=1 前提):
  A) questions_patch.json : {correctAnswerIndexBase, questions:[{id,title,question,options,correctAnswer,explanation}]}
  B) text_patches.json    : {correctAnswerIndexBase, patches:[{id, replaceFields:{...}, reason:[...]}]}
フィールド対応: options->choices / correctAnswer->answer(base=1=JSONと同じ・変換なし)。問は number で突合。
図フィールド(figure/preFigureImage/figureImage)は変更しない(図反映は別工程)。
使い方: python tools/apply_recheck_patch.py <questions_json> <patch_json> [--write]
"""
import json, sys, os

jpath, ppath = sys.argv[1], sys.argv[2]
WRITE = "--write" in sys.argv
FMAP = {"options": "choices", "correctAnswer": "answer", "title": "title",
        "question": "question", "explanation": "explanation"}

patch = json.load(open(ppath, encoding="utf-8"))
base = patch.get("correctAnswerIndexBase", 1)
if base != 1:
    print("WARN correctAnswerIndexBase=%s (このツールは1前提)" % base)

items = []
if "questions" in patch:        # 形式A
    for q in patch["questions"]:
        fields = {k: q[k] for k in ("title", "question", "options", "correctAnswer", "explanation") if k in q}
        items.append((q.get("number") or q.get("id"), fields))
elif "patches" in patch:        # 形式B
    for p in patch["patches"]:
        items.append((p.get("number") or p.get("id"), p.get("replaceFields", {})))
else:
    print("未知のパッチ形式"); sys.exit(1)

data = json.load(open(jpath, encoding="utf-8"))
byno = {q.get("number"): q for q in data["questions"]}

applied, nomatch = [], []
for num, fields in items:
    tgt = byno.get(num)
    if not tgt:
        nomatch.append(num); continue        # この問は対象JSONに無い=別章のパッチ(スキップ)
    changed = []
    for src_k, val in fields.items():
        dst_k = FMAP.get(src_k, src_k)
        if tgt.get(dst_k) != val:
            changed.append(dst_k)
            if WRITE: tgt[dst_k] = val
    if WRITE and ("question" in fields or "options" in fields or "explanation" in fields):
        hm = any("$" in str(tgt.get(k, "")) for k in ("question", "explanation")) or \
             any("$" in c for c in tgt.get("choices", []))
        tgt["hasMath"] = hm
    if changed: applied.append((num, changed))

print("パッチ対象:%d / この章で適用:%d / 別章(スキップ):%d" % (len(items), len(applied), len(nomatch)))
from collections import Counter
c = Counter()
for _, ch in applied:
    for f in ch: c[f] += 1
print("フィールド別変更:", dict(c))
print("適用番号:", [a[0] for a in applied])
if WRITE:
    with open(jpath, "w", encoding="utf-8", newline="\r\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("WROTE", jpath)
