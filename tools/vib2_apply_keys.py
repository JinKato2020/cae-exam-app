# -*- coding: utf-8 -*-
r"""振動2級: vib2_overlay.py が出力した _png を assets/figures の既存キーへ差し替え、
導出51問には preFigureImage(回答前=中立)を設定して回答後(figureImage=答え入り)と2図化する。
ルール(確定・2026-10-08):
  中立(preなし)      : {num}.png → assets/figures/{figureImage}.png を上書き(前後同一)
  中立(既存preあり)  : {num}.png → assets/figures/{preFigureImage}.png を上書き(回答前のみ更新・回答後は保持)
  導出(preなし)      : {num}.png → 新規preキー(figureImage+"Pre")・{num}-ans.png → figureImage を上書き
  導出(既存preあり)  : {num}.png → preFigureImage・{num}-ans.png → figureImage
実行後は tools/gen_figures_ts.py で src/figures.ts を再生成すること。
  python tools/vib2_apply_keys.py [--dry]
"""
import os, sys, json, glob, shutil

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG = os.path.join(CAE, "図", "振動2級", "_png")
FIG = os.path.join(CAE, "assets", "figures")
QDIR = os.path.join(CAE, "content", "questions")

DERIV = set("3-5 3-13 4-9 4-11 4-19 4-20 4-23 4-29 4-31 4-32 4-33 4-36 4-37 4-38 4-42 4-43 "
            "5-11 5-19 6-1 6-5 7-1 7-4 8-14 8-15 8-20 9-2 9-6 9-7 9-8 9-9 9-10 9-11 9-12 "
            "9-14 9-15 9-17 9-18 9-19 10-2 10-4 10-6 10-7 10-9 10-14 10-15 10-16 10-17 10-19 "
            "11-2 11-7 11-17".split())

def main(dry):
    # 対象番号 = _png にある中立PNG(番号.png・-ans除く)
    nums = sorted({os.path.basename(f)[:-4] for f in glob.glob(os.path.join(PNG, "*.png"))
                   if not os.path.basename(f).endswith("-ans.png")},
                  key=lambda s: (int(s.split('-')[0]), int(s.split('-')[1])))
    # 問題JSONを番号→(ファイル, index)で索引
    files = {}; idx = {}
    for p in sorted(glob.glob(os.path.join(QDIR, "vib2-*.json"))):
        d = json.load(open(p, encoding="utf-8")); files[p] = d
        for i, q in enumerate(d["questions"]):
            idx[q["number"]] = (p, i)

    copies = []      # (src_png, dst_key)
    jsonmods = []    # (num, "set preFigureImage", key)
    report = {"中立単": 0, "中立pre更新": 0, "導出新pre": 0, "導出既pre": 0, "欠落": []}

    for n in nums:
        if n not in idx:
            report["欠落"].append(n + "(JSON無)"); continue
        p, i = idx[n]; q = files[p]["questions"][i]
        fig = q.get("figureImage"); pre = q.get("preFigureImage")
        neu = os.path.join(PNG, n + ".png"); ans = os.path.join(PNG, n + "-ans.png")
        if not os.path.exists(neu):
            report["欠落"].append(n + "(中立png無)"); continue

        if n in DERIV:
            if not os.path.exists(ans):
                report["欠落"].append(n + "(ans png無)"); continue
            copies.append((ans, fig))                      # 回答後 → figureImage
            if pre:
                copies.append((neu, pre)); report["導出既pre"] += 1
            else:
                newpre = fig + "Pre"
                copies.append((neu, newpre))
                jsonmods.append((p, i, newpre)); report["導出新pre"] += 1
        else:  # 中立
            if pre:
                copies.append((neu, pre)); report["中立pre更新"] += 1   # 回答前のみ更新
            else:
                copies.append((neu, fig)); report["中立単"] += 1

    # 実行
    for src, key in copies:
        dst = os.path.join(FIG, key + ".png")
        if dry:
            pass
        else:
            shutil.copyfile(src, dst)
    if not dry:
        for p, i, newpre in jsonmods:
            files[p]["questions"][i]["preFigureImage"] = newpre
        for p, d in files.items():
            if any(m[0] == p for m in jsonmods):
                crlf = b"\r\n" in open(p, "rb").read(400)   # 元ファイルの改行を検出して維持
                s = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
                if crlf:
                    s = s.replace("\n", "\r\n")
                open(p, "wb").write(s.encode("utf-8"))      # バイト書き込み(OS変換を回避)

    print("[%s] copies=%d  jsonmods=%d" % ("DRY" if dry else "APPLY", len(copies), len(jsonmods)))
    print("  中立単(fig上書き)=%d / 中立pre更新=%d / 導出新pre=%d / 導出既pre=%d"
          % (report["中立単"], report["中立pre更新"], report["導出新pre"], report["導出既pre"]))
    if report["欠落"]: print("  ★欠落:", report["欠落"])
    print("  新preキー(%d):" % len(jsonmods), " ".join(m[2] for m in jsonmods))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main("--dry" in sys.argv)
