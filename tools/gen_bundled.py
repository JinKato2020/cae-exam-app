# tools/gen_bundled.py — 同梱baseline登録表を生成（量産共通・再実行可）。
# content/ 以下の全JSON（catalog.json・questions・formulas 等）を manifestキーで require する
# 表 src/data/bundled.generated.ts を作る。アプリはこの表を「土台（オフライン初期値）」に使う。
# 図(assets/figures)は含めない（figures.ts が別途 require する）。

import io
import os

ROOT = os.getcwd()
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "src", "data", "bundled.generated.ts")

keys = []
for dirpath, _dirs, names in os.walk(CONTENT):
    for name in sorted(names):
        if name == "_manifest.json" or not name.endswith(".json"):
            continue
        full = os.path.join(dirpath, name)
        key = os.path.relpath(full, CONTENT).replace(os.sep, "/")
        keys.append(f"content/{key}")
keys.sort()

lines = [
    "// 自動生成（tools/gen_bundled.py）。手で編集しない。",
    "// アプリ本体に同梱する content/*.json の登録表（＝OTA前の土台データ）。",
    "// キーは manifest と同じ相対パス。値は require（Metro が JSON をバンドルする）。",
    "export const BUNDLED: Record<string, unknown> = {",
]
for k in keys:
    rel = k[len("content/"):]  # content/ を除いた実パス
    lines.append(f"  {chr(39)}{k}{chr(39)}: require('../../content/{rel}'),")
lines.append("};")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"bundled entries={len(keys)}  out={OUT}")
