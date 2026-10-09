# -*- coding: utf-8 -*-
"""CAE各分野の「ChatGPT作図命令文」の生成＆機械ゲート（恒久ツール・多分野対応）。

方針(恒久・ユーザー厳命 2026-10-07): 図はChatGPT製を採用する。Claudeは自分(figlib)の図を推さない。
★分担(確定):
  ・ChatGPTが作るのは「回答前(中立)図」だけ。図1枚につきプロンプトは常に1本(答え・結論・数値を描かない)。
  ・回答前(中立)図を「基盤画像」とし、回答後図はその同じ図に解説・答えを追記して作る。
  ・[中立] = 構造/モデル配置など。その中立図を回答前後で共用(追記なしで同じ1枚を使い回せる)。
  ・[導出] = 自由体図の解・応力/モーメント分布・固有モード・応答曲線など。ChatGPTは中立図(回答前)だけ作り、
            その中立SVGに Claude がテキスト・式・答えを追記して「回答後図」を完成させる。
            ※回答後をChatGPTプロンプトにしない(「回答前/回答後の2プロンプト」は誤り)。

命令文ファイルの各図の行構造:
  [中立] <番号>  — <タイトル>
  図: <ChatGPT用の中立プロンプト1本>
  [導出] <番号>  — <タイトル>
  図: <ChatGPT用の中立プロンプト1本(回答前=基盤画像)>
  Claude回答後: <Claudeが中立SVGへ追記して回答後図を完成させる内容>

使い方:
  python tools/figprompt.py scaffold [target] [--force]  命令文の骨組みを生成(既存は上書きしない。--forceで再生成)
  python tools/figprompt.py check [target|file]          機械ゲート: 網羅性・各図の「図:」・[導出]の「Claude回答後:」・未記述を検査
  python tools/figprompt.py list                         対応分野(target)の一覧

target 既定 = vib2。例: python tools/figprompt.py scaffold solid2
「未ChatGPT化」= 問題が図を持つ(figureImage か preFigureImage のPNGが存在)のに、対象分野の SVG が未作成のもの。
ゲートは cae-quality-check.mjs フックから自動実行される(命令文ファイルを保存するたびに検査)。
"""
import json, glob, os, sys, re

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(CAE, "content", "questions")
FIG = os.path.join(CAE, "assets", "figures")
PLACEHOLDER = "《未記述》"

# 共通: [導出](=回答後にClaudeが答え・式入り図を追編集する)と判定するキーワード。figureHintに含めば導出扱い。
DERIV_COMMON = ["導出", "線図", "グラフ", "曲線", "軌跡", "分布", "数値解", "収束",
                "自由体", "FBD", "力のつり合い", "つり合い", "つりあい", "釣り合い", "ベクトル線図"]
DERIV_VIB = ["モード", "固有モード", "モード形状", "応答曲線", "周波数応答", "ボード", "ナイキスト",
             "波形", "時刻歴", "スペクトル", "伝達関数", "共振", "位相", "固有値", "ハミルトン"]
DERIV_SOLID = ["せん断力図", "曲げモーメント", "モーメント図", "SFD", "BMD", "たわみ", "たわみ曲線",
               "応力分布", "ひずみ分布", "変位分布", "応力状態", "モール円", "モール", "座屈モード",
               "座屈", "変形図", "降伏", "塑性域", "応力集中"]


def _grade_select(substr_all):
    """meta.grade が与語を全て含むファイルを章順で返す(汎用セレクタ)。"""
    def sel():
        out = []
        for fp in sorted(glob.glob(os.path.join(QDIR, "*.json"))):
            try:
                d = json.load(open(fp, encoding="utf-8"))
            except Exception:
                continue
            g = (d.get("meta", {}).get("grade") or "")
            if all(s in g for s in substr_all):
                out.append(fp)
        return out
    return sel


# 対応分野。select=対象JSONの集合, svgdir/out=成果物, chname=章番号→章名(空ならmeta.category), deriv_kw=導出判定語。
TARGETS = {
    "vib2": {
        "label": "振動2級",
        "select": lambda: sorted(glob.glob(os.path.join(QDIR, "vib2-*.json"))),
        "svgdir": os.path.join(CAE, "図", "振動2級"),
        "out": os.path.join(CAE, "図", "振動2級", "命令文_未ChatGPT化_全183.md"),
        "chname": {1: "数学基礎", 2: "材料・構造の力学", 3: "材料力学", 4: "振動・音響",
                   5: "FEM基礎", 6: "要素と要素分割", 7: "モデル化の基礎", 8: "境界条件・荷重条件",
                   9: "数値計算技術", 10: "ポスト処理", 11: "結果の検証", 12: "計算機の基礎", 13: "技術者倫理"},
        "deriv_kw": DERIV_COMMON + DERIV_VIB,
    },
    "solid2": {
        "label": "固体2級",
        "select": _grade_select(["固体", "2"]),
        "svgdir": os.path.join(CAE, "図", "固体2級"),
        "out": os.path.join(CAE, "図", "固体2級", "命令文_固体2級.md"),
        "chname": {},  # 空=各JSONの meta.category を章名に使う(データ由来で誤りを避ける)
        "deriv_kw": DERIV_COMMON + DERIV_SOLID,
    },
}


def png(k):
    return bool(k) and os.path.exists(os.path.join(FIG, k + ".png"))


def svg_done(svgdir, num):
    return os.path.exists(os.path.join(svgdir, f"fig{num}.svg"))


def needed(cfg):
    """未ChatGPT化の図: [(ch, chname, number, title, figureHint, 'deriv'|'neutral'), ...] を章順で返す。"""
    rows = []
    for fp in cfg["select"]():
        d = json.load(open(fp, encoding="utf-8"))
        ch = d["meta"].get("chapter")
        chname = cfg["chname"].get(ch) if cfg["chname"] else (d["meta"].get("category") or "")
        for q in d["questions"]:
            num = q["number"]
            if not (png(q.get("figureImage")) or png(q.get("preFigureImage"))):
                continue
            if svg_done(cfg["svgdir"], num):
                continue
            hint = (q.get("figureHint") or "").strip()
            kind = "deriv" if any(k in hint for k in cfg["deriv_kw"]) else "neutral"
            rows.append((ch, chname, num, q.get("title", ""), hint, kind))
    rows.sort(key=lambda r: (r[0] if r[0] is not None else 999, r[2]))
    return rows


def scaffold(cfg, force=False):
    rows = needed(cfg)
    out = cfg["out"]
    if os.path.exists(out) and not force:
        print(f"[skip] 既存のため上書きしません(再生成は --force): {out}")
        print(f"       対象(未ChatGPT化)= {len(rows)}枚")
        return
    os.makedirs(cfg["svgdir"], exist_ok=True)
    L = []
    L.append(f"<!-- FIGPROMPT v2 | {cfg['label']} 未ChatGPT化 図の作図命令文 -->")
    L.append("# 方針(恒久): 図はChatGPT製を採用。Claudeは自分の図を推さない。")
    L.append("# ★分担: ChatGPTが作るのは「回答前(中立)図」だけ。図1枚につき『図:』プロンプト1本(答え・結論・数値を描かない)。")
    L.append("#   回答前(中立)図を『基盤画像』とし、回答後図はその同じ図に解説・答えを追記して作る。")
    L.append("#   [中立]=構造/モデル配置など。中立図を回答前後で共用(追記なしで同じ1枚)。")
    L.append("#   [導出]=自由体図の解/応力・モーメント分布/固有モード/応答曲線など。ChatGPTは中立図(回答前)だけ作り、その中立SVGにClaudeがテキスト・式・答えを追記して回答後図を完成(=『Claude回答後:』)。回答後はChatGPTプロンプトにしない。")
    L.append("# 共通スタイル(『図:』に適用): viewBox指定・先頭に白背景rect・フラットな線画(画像/影/グラデ禁止)。")
    L.append("#   配色 主線=ネイビー#1F3A65(太2.5) / 強調=赤#C82D2D / 軸・補助・寸法=グレー#888(細1.2,破線\"5 4\") / 面塗り=淡ネイビー#E1E7F2。")
    L.append("#   日本語ラベル可(sans-serif,変数はitalic)・重なり回避・矢印は三角矢尻。中立図は答え・結論・数値を描かない。")
    L.append(f"#   末尾に『その内容を「fig{{番号}}.svg」という名前のDL可能なSVGファイルとして保存・提供して』を付ける。")
    L.append(f"# 生成手順: ①各『図:』をChatGPTへ投げる ②SVGを {os.path.relpath(cfg['svgdir'], CAE)}/fig{{番号}}.svg に保存 ③python tools/figprompt.py check {next(k for k,v in TARGETS.items() if v is cfg)} で検査 ④ClaudeがPNG化し既存キーへ差替([導出]は『Claude回答後:』に従い回答後SVGも作成)。")
    cur = None
    for ch, chname, num, title, hint, kind in rows:
        if ch != cur:
            cur = ch
            L.append("")
            L.append(f"### {chname}" if chname else f"### 第{ch}章")
        tag = "導出" if kind == "deriv" else "中立"
        L.append("")
        L.append(f"[{tag}] {num}  — {title}")
        L.append(f"図: {PLACEHOLDER}")
        if kind == "deriv":
            L.append(f"Claude回答後: {PLACEHOLDER}")
        if hint:
            L.append(f"<!-- hint: {hint} -->")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    nd = sum(1 for r in rows if r[5] == "deriv")
    print(f"[生成] {out}")
    print(f"       未ChatGPT化 {len(rows)}枚 (中立 {len(rows)-nd} / 導出 {nd})。各《…》を記述後、check で検査。")


ENTRY = re.compile(r"^\[(中立|導出)\]\s+(\S+)")


def check(cfg, filearg=None):
    f = filearg or cfg["out"]
    if not os.path.exists(f):
        print(f"FAIL: 命令文ファイルが無い: {f}  (先に scaffold)")
        return 1
    req = {num: kind for ch, cn, num, t, h, kind in needed(cfg)}  # 本来必要な全番号と分類
    txt = open(f, encoding="utf-8").read()
    entries = {}  # num -> {"tag":, "fields": {name: text}}
    cur = None
    for ln in txt.splitlines():
        m = ENTRY.match(ln.strip())
        if m:
            cur = m.group(2)
            entries[cur] = {"tag": m.group(1), "fields": {}}
            continue
        if cur:
            fm = re.match(r"^(図|Claude回答後)\s*[:：]\s*(.*)$", ln.strip())
            if fm:
                entries[cur]["fields"][fm.group(1)] = fm.group(2).strip()

    def filled(s):
        return bool(s) and PLACEHOLDER not in s and "《" not in s

    hard = []
    # 1) 網羅性: 必要な番号が全てファイルに在るか
    missing = [n for n in req if n not in entries]
    if missing:
        hard.append(f"命令文に無い図 {len(missing)}: {sorted(missing)}")
    # 2) 各図に ChatGPT用「図:」が1本・記述済みか / [導出]は「Claude回答後:」も記述済みか
    for num, e in entries.items():
        fld = e["fields"]
        if "図" not in fld:
            hard.append(f"{num}: ChatGPT用「図:」(中立プロンプト)が無い")
        elif not filled(fld.get("図")):
            hard.append(f"{num}: 「図:」プロンプト未記述")
        if e["tag"] == "導出":
            if "Claude回答後" not in fld:
                hard.append(f"{num}: [導出]だが「Claude回答後:」(中立SVGへの追記内容)が無い")
            elif not filled(fld.get("Claude回答後")):
                hard.append(f"{num}: 「Claude回答後:」未記述")
    n_deriv = sum(1 for e in entries.values() if e["tag"] == "導出")
    print(f"[figprompt check] {os.path.basename(f)}: 必要{len(req)}枚 / 記載{len(entries)}枚 (導出{n_deriv}) / FAIL {len(hard)}件")
    for h in hard:
        print("  FAIL:", h)
    if hard:
        print("→ 恒久ルール違反。全図に中立『図:』1本・[導出]は『Claude回答後:』も必須・全図を記載・《…》は全て記述。")
        return 1
    print("→ OK: 全図を網羅・全図に中立プロンプト・[導出]は回答後追記メモあり・未記述なし。")
    return 0


def resolve(args):
    """引数から (cfg, 残り) を返す。target名でなければ vib2 既定。"""
    tgt = "vib2"
    rest = list(args)
    if rest and rest[0] in TARGETS:
        tgt = rest.pop(0)
    return TARGETS[tgt], rest


def main():
    args = sys.argv[1:]
    if args and args[0] == "list":
        for k, v in TARGETS.items():
            print(f"{k:<8} {v['label']}  out={os.path.relpath(v['out'], CAE)}")
        return 0
    if args and args[0] == "scaffold":
        cfg, rest = resolve(args[1:])
        scaffold(cfg, force=("--force" in rest))
        return 0
    if args and args[0] == "check":
        rest = args[1:]
        # check の引数は target名 か ファイルパス のどちらか
        if rest and rest[0] in TARGETS:
            return check(TARGETS[rest[0]], rest[1] if len(rest) > 1 else None)
        return check(TARGETS["vib2"], rest[0] if rest else None)
    # 無引数 = vib2 check
    return check(TARGETS["vib2"])


if __name__ == "__main__":
    sys.exit(main())
