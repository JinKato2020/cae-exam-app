# -*- coding: utf-8 -*-
r"""公式リスト等の \begin{aligned} 式を「左詰め」に揃え直す(=列揃えを廃止)。
 - 右詰め(LHS &= RHS / LHS=\ &RHS)→ 先頭& の左寄せ("& LHS = RHS")。
 - 多列(& 区切り)は \quad へ。
 - 行列(vmatrix 等)を内包する式は & の意味が違うのでスキップ。
App.tsx alignLeft / build_formula_pdfs._align_at_eq と同じ方針。CRLF・体裁は保つ(surgical 置換)。
使い方: python tools/leftalign_formulas.py        … 置換実行
       python tools/leftalign_formulas.py --dry  … 変更点のみ表示(書き込まない)"""
import json, glob, re, sys, os

BEG = "\\begin{aligned}"
END = "\\end{aligned}"
NESTED = re.compile(r"\\begin\{(vmatrix|matrix|bmatrix|pmatrix|cases|array|smallmatrix)\}")
SEP = "\\" + "\\"  # LaTeX 改行 = 連続2バックスラッシュ


def left_line(line):
    line = re.sub(r"\s*&\s*=", " =", line)           # &= (= の前の &)
    line = re.sub(r"=\s*\\?\s*&", "= ", line)          # =& / =\ & (= の後の &)
    line = re.sub(r"\s*&\s*", lambda m: " \\quad ", line)  # 残りの列区切り & → \quad
    return "& " + line.strip()


def transform(formula):
    i = formula.find(BEG)
    j = formula.rfind(END)
    if i < 0 or j < 0:
        return None
    pre = formula[:i + len(BEG)]
    inner = formula[i + len(BEG):j]
    post = formula[j:]
    # 行break(=連続2バックスラッシュ)で分割。直後が \command でも分割できるよう後読みは付けない。
    lines = re.split(r"(?<!\\)" + re.escape(SEP), inner)
    newinner = (" " + SEP + " ").join(left_line(x) for x in lines if x.strip())
    return pre + newinner + post


def main():
    dry = "--dry" in sys.argv
    CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    total = 0
    for f in sorted(glob.glob(os.path.join(CAE, "content", "**", "*.json"), recursive=True)):
        raw = open(f, "rb").read().decode("utf-8")
        d = json.loads(raw)
        changed = 0
        for it in (d.get("items") or []):
            fm = it.get("formula") or ""
            if BEG not in fm or NESTED.search(fm):
                continue
            new = transform(fm)
            if not new or new == fm:
                continue
            old_esc = json.dumps(fm, ensure_ascii=False)[1:-1]
            new_esc = json.dumps(new, ensure_ascii=False)[1:-1]
            if old_esc not in raw:
                print("  !! not found in raw:", it.get("term"))
                continue
            raw = raw.replace(old_esc, new_esc, 1)
            changed += 1
            if dry:
                print("  -", os.path.basename(f), "|", it.get("term"))
        if changed and not dry:
            open(f, "wb").write(raw.encode("utf-8"))
        if changed:
            print(f"{os.path.basename(f)}: {changed}件")
            total += changed
    print(("[DRY] " if dry else "") + f"合計 {total} 件")


if __name__ == "__main__":
    main()
