# tools/gen_catalog_json.py — 【1回きりの移行ツール】
# 既存 src/catalog.ts の CATALOG 構造を content/catalog.json（データ駆動カタログ）へ書き出す。
# 以降はこの catalog.json を直接編集する（catalog.ts はこれを読むだけになる）。
#
# 出力スキーマ:
#   { "schema":1, "fields":[ { "id","name","grades":[ { "id","name","chapters":[
#       { "id","title","content":<問題JSONキー>,"formulaId","formula":<公式JSONキー>,"ready" } ] } ] } ] }
#   ※ content/formula の値は manifest と同じ相対キー（例 content/questions/math-basics.json）。

import io
import json
import re

CAT = io.open("src/catalog.ts", encoding="utf-8").read()
FORM = io.open("src/formulas.ts", encoding="utf-8").read()

# var -> 問題JSONキー
qmap = {m.group(1): f"content/questions/{m.group(2)}.json"
        for m in re.finditer(r"import (\w+) from '\.\./content/questions/([\w-]+)\.json';", CAT)}
# var -> 公式JSONキー
fvar = {m.group(1): f"content/formulas/{m.group(2)}.json"
        for m in re.finditer(r"import (\w+) from '\.\./content/formulas/([\w-]+)\.json';", FORM)}
# FORMULA_DOCS の formulaId(=キー) -> 公式JSONキー（key と var は同名運用）
fid_to_file = {}
for m in re.finditer(r"^\s*(\w+):\s*(\w+) as unknown as FormulaDoc", FORM, re.M):
    fid_to_file[m.group(1)] = fvar.get(m.group(2))

fields = []
cur_field = None
cur_grade = None
pending = None  # ('field'|'grade', id) 直後の name 行を待つ

for line in CAT.splitlines():
    mf = re.search(r"id: '(solid|thermal|vibration)'", line)
    mg = re.search(r"id: '(g1|g2)'", line)
    is_chapter = ("data:" in line and "title:" in line)

    if mf and not is_chapter:
        pending = ("field", mf.group(1)); continue
    if mg and not is_chapter:
        pending = ("grade", mg.group(1)); continue
    if pending:
        mn = re.search(r"name: '([^']+)'", line)
        if mn:
            if pending[0] == "field":
                cur_field = {"id": pending[1], "name": mn.group(1), "grades": []}
                fields.append(cur_field); cur_grade = None
            else:
                cur_grade = {"id": pending[1], "name": mn.group(1), "chapters": []}
                cur_field["grades"].append(cur_grade)
            pending = None
            continue
        pending = None  # name が続かなければ破棄

    if is_chapter and cur_grade is not None:
        cid = re.search(r"id: '([^']+)'", line).group(1)
        ctitle = re.search(r"title: '([^']+)'", line).group(1)
        cvar = re.search(r"data: (\w+)", line).group(1)
        cready = re.search(r"ready: (true|false)", line)
        cfid = re.search(r"formulaId: '([^']+)'", line)
        fid = cfid.group(1) if cfid else cid
        ch = {"id": cid, "title": ctitle,
              "content": qmap.get(cvar),
              "formulaId": fid,
              "ready": (cready.group(1) == "true") if cready else True}
        ff = fid_to_file.get(fid)
        if ff:
            ch["formula"] = ff
        cur_grade["chapters"].append(ch)

# 振動は1級・2級とも「準備中の棚」を用意（後で棚にデータを置けば生える）。
vib = next((f for f in fields if f["id"] == "vibration"), None)
if vib:
    have = {g["id"] for g in vib["grades"]}
    order = [("g1", "1級"), ("g2", "2級")]
    vib["grades"] = [{"id": gid, "name": gname, "chapters": next((g["chapters"] for g in vib["grades"] if g["id"] == gid), [])}
                     for gid, gname in order]

out = {"schema": 1, "fields": fields}
io.open("content/catalog.json", "w", encoding="utf-8").write(
    json.dumps(out, ensure_ascii=False, indent=1) + "\n")

# サマリのみ
nch = sum(len(g["chapters"]) for f in fields for g in f["grades"])
miss = [f"{f['id']}/{g['id']}/{c['id']}" for f in fields for g in f["grades"] for c in g["chapters"] if not c.get("content")]
print(f"fields={len(fields)}  chapters={nch}")
for f in fields:
    print("  ", f["id"], "=", [f"{g['id']}:{len(g['chapters'])}" for g in f["grades"]])
if miss:
    print("  [warn] content未解決:", miss[:8])
