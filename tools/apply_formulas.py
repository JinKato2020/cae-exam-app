#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""公式・用語の正本JSON(完成版)を content/formulas/ へ**章ごと丸ごと差し替え**で反映するツール(2026-10-09)。
= apply_content.py の公式用語版。本文(questions)と違い、公式用語は「最重要だけに選び直す」ため
  章の items 配列ごと入れ替える(個別パッチではない)。

正本フォーマット(どれでも可):
  (a) 単章 : {"chapter":2, "title":"...", "intro":"...", "items":[ {id,kind,term,formula,body,example,figureImage}, ... ]}
  (b) 複数章: {"ch2":{...単章...}, "ch3":{...}}  または  {"chapters":[ {...単章...}, ... ]}
  title/intro を省いた章は、既存ファイルの値を温存する。

分野(--field): solid2=無印 chN.json / solid1・vib1・vib2・thermal1・thermal2=同名接頭辞。

機械チェック:
  FAIL(書込中止) : 必須欠落(id/kind/term)・kindが formula|term 以外・figureImageキーの画像が実在しない
  WARN(報告のみ) : KaTeXの二重エスケープ疑い(\\\\+文字 / リテラル \\n \\t)・$の個数が奇数(未閉じ疑い)

使い方:
  python tools/apply_formulas.py <正本.json> --field solid2           # dry-run(件数と差分サマリのみ)
  python tools/apply_formulas.py <正本.json> --field solid2 --write   # 該当章へ丸ごと書込
"""
import json, sys, os, glob, re
from collections import defaultdict

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FDIR = os.path.join(CAE, "content", "formulas")
ADIR = os.path.join(CAE, "assets", "figures")
KNOWN_PREFIXES = ("solid1-", "thermal1-", "thermal2-", "vib1-", "vib2-", "solid2-")

def fig_exists_set():
    """assets/figures 内の拡張子を除いたキー集合(png/svg 両対応)。"""
    s = set()
    for p in glob.glob(os.path.join(ADIR, "*.png")) + glob.glob(os.path.join(ADIR, "*.svg")):
        s.add(os.path.splitext(os.path.basename(p))[0])
    return s

def chapter_file(field, n):
    """(field, 章番号) → content/formulas 内のファイル名(拡張子なし)。"""
    return "ch%d" % n if field == "solid2" else "%s-ch%d" % (field, n)

def iter_chapters(doc):
    """正本doc → [(章番号, 章dict)] に正規化。"""
    if isinstance(doc, dict) and "items" in doc:             # (a) 単章
        return [(int(doc.get("chapter")), doc)]
    if isinstance(doc, dict) and "chapters" in doc:          # (c) chapters配列
        return [(int(c.get("chapter")), c) for c in doc["chapters"]]
    if isinstance(doc, dict):                                # (b) {"chN": {...}}
        out = []
        for k, v in doc.items():
            m = re.match(r"ch(\d+)$", str(k))
            if m and isinstance(v, dict):
                out.append((int(m.group(1)), v))
        return out
    return []

RE_DBL = re.compile(r"\\\\[A-Za-z]")       # 二重エスケープ疑い(\\ の後に英字 = \\dfrac 等)
RE_LIT = re.compile(r"\\[nt](?![A-Za-z])")  # リテラル \n \t のみ(\nu \tau \times \theta 等の正規命令は除外)

def check_item(it, figset):
    """1項目を検査 → (fail理由 or None, [warn...])"""
    for k in ("id", "kind", "term"):
        if not it.get(k):
            return "必須欠落:%s" % k, []
    if it["kind"] not in ("formula", "term"):
        return "kind不正:%s" % it["kind"], []
    fig = it.get("figureImage")
    if fig and fig not in figset:
        return "図キー不在:%s" % fig, []
    warns = []
    text = " ".join(str(it.get(k, "")) for k in ("term", "formula", "body", "example"))
    if RE_DBL.search(text): warns.append("二重エスケープ疑い")
    if RE_LIT.search(text): warns.append("リテラル\\n/\\t")
    if text.count("$") % 2 != 0: warns.append("$が奇数")
    return None, warns

def main():
    if len(sys.argv) < 2 or "--field" not in sys.argv:
        print(__doc__); sys.exit(1)
    src = sys.argv[1]
    field = sys.argv[sys.argv.index("--field") + 1]
    WRITE = "--write" in sys.argv

    doc = json.load(open(src, encoding="utf-8"))
    chapters = iter_chapters(doc)
    if not chapters:
        print("ABORT: 正本から章を認識できません(chapter/items か chN か chapters が必要)"); sys.exit(1)
    figset = fig_exists_set()

    plans, fails, warns, needs = [], [], [], []   # plans: (fn, path, newdoc, old_n, new_n) / needs: 作図依頼
    for n, ch in chapters:
        fn = chapter_file(field, n)
        path = os.path.join(FDIR, fn + ".json")
        if not os.path.exists(path):
            fails.append(("ch%d" % n, "対象ファイル無し:%s" % os.path.basename(path))); continue
        old = json.load(open(path, encoding="utf-8"))
        items = ch.get("items", [])
        for it in items:
            f, w = check_item(it, figset)
            if f: fails.append(("ch%d:%s" % (n, it.get("id", "?")), f))
            for x in w: warns.append(("ch%d:%s" % (n, it.get("id", "?")), x))
            # 穴A: 図が無い項目=新規作図の候補。figureNeed(作図指示)を拾ってから本文JSONからは除去する。
            if not it.get("figureImage"):
                needs.append(("ch%d:%s" % (n, it.get("id", "?")),
                              it.get("figureNeed") or "(figureNeed未記入) " + it.get("term", "")))
            it.pop("figureNeed", None)   # content JSON には残さない
        new = dict(old)
        new["chapter"] = n
        if ch.get("title"): new["title"] = ch["title"]
        if ch.get("intro"): new["intro"] = ch["intro"]
        new["items"] = items
        plans.append((fn, path, new, len(old.get("items", [])), len(items)))

    print("=== field=%s / 章数=%d ===" % (field, len(plans)))
    for fn, _, _, o, nn in sorted(plans):
        print("  %-14s 項目 %2d → %2d" % (fn, o, nn))
    wc = defaultdict(int)
    for _, x in warns: wc[x] += 1
    print("--- WARN=%d %s / FAIL=%d / 作図依頼=%d ---" % (len(warns), dict(wc), len(fails), len(needs)))
    if needs:
        print("--- [作図依頼] figureImage空=②でChatGPT作図に回す項目 ---")
        for who, msg in needs: print("  -", who, ":", msg)
    if warns:
        for who, x in warns[:15]: print("  ! WARN", who, x)
    if fails:
        for who, why in fails[:20]: print("  ★FAIL", who, why)
        print("FAILがあるため書込中止(--writeでも)。正本を確認してください。"); sys.exit(2)
    if WRITE:
        for fn, path, new, _, _ in plans:
            with open(path, "w", encoding="utf-8", newline="\r\n") as f:
                json.dump(new, f, ensure_ascii=False, indent=2); f.write("\n")
            print("WROTE", path)
    else:
        print("(dry-run。書き込むには --write)")

if __name__ == "__main__":
    main()
