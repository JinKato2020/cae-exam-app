# tools/content_manifest.py — コンテンツOTA用 manifest 生成（量産共通ツール）
#
# 役割: アプリに載る「テキスト(content/*.json)」と「図(assets/figures/*.png)」の
#       全ファイルの sha256 と size を1つの _manifest.json に書き出す。
#   ・アプリ本体にはこの _manifest.json を「同梱baseline」として import する。
#   ・同じ _manifest.json を配信先 content.safa-lang.com/<APP_ID>/ にも置く。
#   ・端末は「配信manifestのsha」と「手持ちsha」を比べ、変わったファイルだけDLする(P2/P3)。
#
# 量産方針: このツールは app 非依存。新しい資格アプリでは下の CONFIG を数行変えるだけ。
#   キー体系(端末/配信で共通の相対パス):
#     content/index.json, content/questions/<x>.json, content/formulas/<x>.json, figures/<x>.png
#   配信URL = f"https://content.safa-lang.com/{APP_ID}/{key}"
#
# 使い方: python tools/content_manifest.py   （リポジトリ直下で実行）

from check_quality import require_editorial_review

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

# ---- CONFIG（新アプリではここだけ変える）--------------------------------
APP_ID = "cae"
# (manifestキーのprefix, ソースの実ディレクトリ, 対象拡張子)
SOURCES = [
    ("content", "content", (".json",)),          # テキスト: content/ 以下をそのままのキーで
    ("figures", "assets/figures", (".png", ".jpg")),  # 図: assets/figures/ を figures/ キーへ
]
MANIFEST_OUT = "content/_manifest.json"           # 同梱baseline兼配信ファイルの出力先
EXCLUDE_BASENAMES = {"_manifest.json"}            # 自分自身は含めない
# ------------------------------------------------------------------------


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect(root: str):
    """SOURCES を走査して {key: {sha256, size}} を返す。key はスラッシュ区切りの相対パス。"""
    files = {}
    for key_prefix, src_rel, exts in SOURCES:
        src_dir = os.path.join(root, src_rel)
        if not os.path.isdir(src_dir):
            print(f"[warn] ソース無し: {src_rel}", file=sys.stderr)
            continue
        for dirpath, _dirs, names in os.walk(src_dir):
            for name in sorted(names):
                if name in EXCLUDE_BASENAMES:
                    continue
                if not name.lower().endswith(exts):
                    continue
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, src_dir).replace(os.sep, "/")
                key = f"{key_prefix}/{rel}"
                files[key] = {"sha256": sha256_of(full), "size": os.path.getsize(full)}
    return files


def main():
    root = os.getcwd()
    # Full releases review every chapter. Scoped releases review every selected chapter
    # and require all other payloads to equal the currently published manifest.
    from pathlib import Path
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="+", default=os.environ.get("CAE_OTA_QUESTION_FILES", "").split())
    selected = set(parser.parse_args().only)
    files = collect(root)
    if selected:
        import re
        import time
        import urllib.request
        if any(not re.fullmatch(r"content/questions/[A-Za-z0-9_-]+\.json", key)
               or key not in files for key in selected):
            raise ValueError("限定配信の対象は既存の問題JSONだけ指定できます")
        request = urllib.request.Request(
            f"https://content.safa-lang.com/{APP_ID}/_manifest.json?t={time.time_ns()}",
            headers={"User-Agent": "CAE-content-release/1.0", "Cache-Control": "no-cache"})
        with urllib.request.urlopen(request, timeout=30) as response:
            published = json.load(response)
        if published.get("appId") != APP_ID or published.get("schema") != 1:
            raise ValueError("公開manifestのアプリ・スキーマが不一致")
        previous = published["files"]
        changed = {key for key in set(files) | set(previous)
                   if files.get(key) != previous.get(key)}
        if changed - selected:
            raise ValueError("限定配信の対象外に差分があります: " + ", ".join(sorted(changed - selected)))
        question_paths = [Path(root) / key for key in sorted(selected)]
    else:
        question_paths = sorted((Path(root) / "content" / "questions").glob("*.json"))
    for question_path in question_paths:
        require_editorial_review(json.loads(question_path.read_bytes()))
    manifest = {
        "appId": APP_ID,
        "schema": 1,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": dict(sorted(files.items())),  # キー順を安定化(差分diffを見やすく)
    }
    out_path = os.path.join(root, MANIFEST_OUT)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        f.write("\n")

    # サマリだけ表示（生データは会話に載せない）
    n_content = sum(1 for k in files if k.startswith("content/"))
    n_fig = sum(1 for k in files if k.startswith("figures/"))
    total_mb = sum(v["size"] for v in files.values()) / 1024 / 1024
    print(f"appId={APP_ID}  files={len(files)}  (content={n_content} / figures={n_fig})  "
          f"total={total_mb:.1f}MB")
    print(f"out: {out_path}  ({os.path.getsize(out_path)/1024:.0f}KB)")


if __name__ == "__main__":
    main()
