# -*- coding: utf-8 -*-
"""全分野・全級の問題PDF+公式用語PDFを最新データで一括出力(既存があれば _r採番)。
catalog.json の ready 章を対象に build_pdfs.py / build_formula_pdfs.py を呼ぶ。
使い方: python tools/build_all_pdfs.py [--list]   (--list は対象一覧のみ表示)
"""
import json, os, subprocess, sys

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stems():
    cat = json.load(open(os.path.join(CAE, "content", "catalog.json"), encoding="utf-8"))
    q, f, rows = [], [], []
    for fld in cat["fields"]:
        for g in fld["grades"]:
            for ch in g["chapters"]:
                if not ch.get("ready"):
                    continue
                c = ch.get("content")
                fm = ch.get("formula")
                qs = os.path.splitext(os.path.basename(c))[0] if c else None
                fs = os.path.splitext(os.path.basename(fm))[0] if fm else ch.get("formulaId")
                if qs:
                    q.append(qs)
                if fs:
                    f.append(fs)
                rows.append(f"{fld['name']}{g['name']} {ch['id']}: q={qs} f={fs}")

    def dd(x):
        s, o = set(), []
        for i in x:
            if i not in s:
                s.add(i); o.append(i)
        return o
    return dd(q), dd(f), rows


def main():
    q, f, rows = stems()
    print(f"対象: 問題{len(q)}章 / 公式用語{len(f)}章")
    for r in rows:
        print(" ", r)
    if "--list" in sys.argv[1:]:
        return
    py = sys.executable
    print("\n=== 問題PDF ===", flush=True)
    subprocess.run([py, os.path.join(CAE, "tools", "build_pdfs.py"), *q])
    print("\n=== 公式用語PDF ===", flush=True)
    subprocess.run([py, os.path.join(CAE, "tools", "build_formula_pdfs.py"), *f])
    print("\nALL PDF DONE")


if __name__ == "__main__":
    main()
