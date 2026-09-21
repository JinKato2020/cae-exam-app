# -*- coding: utf-8 -*-
"""
check_quality.py  —  作問の「難易度・品質」を機械チェックする恒久ゲート。

目的（2026-09-12・ユーザー厳命）:
  「すぐ楽をする傾向があるので、難易度を落とさず“第2章の品質”を今後も保つ仕組み」。
  今回診断した3欠陥を、作問のたびに機械で炙り出して見逃しを構造で防ぐ。
    ① 断定語（必ず/常に/まったく…）で言葉だけ消せる誤答
    ② 1式に代入するだけの単純計算・概念の丸暗記が多すぎる
    ③ 章内・章間のトピック重複／正解が最長という“長さで当たる”作り

較正方針: gold standard = 第2章 solid-basics.json / 第3章 heat-basics.json。
  この2章が PASS になるよう、しきい値は「割合」で持つ（孤発の1件では WARN にしない）。
  常に WARN だと警告が形骸化する。PASS を“達成可能な基準”に保つのが要点。

使い方:
    python tools/check_quality.py            # content/questions/*.json 全部
    python tools/check_quality.py <file.json>   # 1章だけ（重複判定は他章も読んで比較）
判定:
    FAIL = 構造エラー（4択でない/answer範囲外/必須キー欠落/meta.count不一致/番号重複）
    WARN = 品質シグナルがしきい値超過（易問過多/計算過少/答え偏り/“長さで当たる”多発/単純計算多発/トピック重複/図欠落）
    PASS = しきい値内
  🔎/ℹ️ 行は「参考・要目視」で判定には影響しない（断定語の誤答＝正当な引っかけのこともある）。
"""
import sys, os, json, glob, re, unicodedata

# ---- しきい値（甘くしない。緩める時は理由をコミットに残す） ----
D1_MAX_SHARE      = 0.35   # 難易度1（易しい）割合の上限
CALC_MIN_SHARE    = 0.20   # 計算問題割合の下限（概念丸暗記への偏り防止）
LEN_TELL_RATIO    = 1.7    # 正解が誤答平均の何倍長いと「長さで当たる」と疑うか
LEN_TELL_GAP      = 18     # かつ文字数差もこれ以上
LEN_TELL_SHARE    = 0.25   # “長さで当たる”問がこの割合を超えたら WARN
SIMPLE_CALC_MIN   = 3      # 単純計算疑いがこの数以上で WARN
ANS_MAX_DEV_SHARE = 0.20   # 答え①②③④の最多-最少が n*これを超えたら偏り
BAN = ["まったく", "全く", "必ず", "つねに", "常に", "無視してよい", "一切",
       "どんな", "絶対", "のみである", "にしか", "同じもので", "区別する意味はない"]
REQUIRED = ["id","number","title","topic","type","difficulty","question",
            "choices","answer","explanation","origin","reviewed"]

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(r"[\s　・（）()\[\]。、,.]", "", s).lower()

def calc_body(q):
    e = q.get("explanation", "")
    return e.split("【計算】")[1].split("【")[0] if "【計算】" in e else ""

def is_calc(q):
    return "【計算】" in q.get("explanation", "")

def check_file(path, all_titles):
    d = json.load(open(path, encoding="utf-8"))
    qs = d.get("questions", [])
    n = len(qs)
    hard, warn, info, review = [], [], [], []

    # --- 構造(FAIL) ---
    if d.get("meta", {}).get("count") != n:
        hard.append(f"meta.count={d.get('meta',{}).get('count')} ≠ 実問数{n}")
    nums = {}
    for q in qs:
        num = q.get("number", "?")
        for k in REQUIRED:
            if k not in q: hard.append(f"{num}: 必須キー欠落 '{k}'")
        if len(q.get("choices", [])) != 4: hard.append(f"{num}: 選択肢が4個でない")
        a = q.get("answer")
        if not (isinstance(a, int) and 1 <= a <= 4): hard.append(f"{num}: answer範囲外({a})")
        nums[num] = nums.get(num, 0) + 1
    for num, c in nums.items():
        if c > 1: hard.append(f"番号重複 {num}×{c}")

    # --- 難易度・計算比率(WARN) ---
    d1 = sum(1 for q in qs if q.get("difficulty") == 1)
    calc = sum(1 for q in qs if is_calc(q))
    if n and d1 / n > D1_MAX_SHARE:
        warn.append(f"易問(d1)が多すぎ: {d1}/{n}={d1/n:.0%} > {D1_MAX_SHARE:.0%}")
    if n and calc / n < CALC_MIN_SHARE:
        warn.append(f"計算問題が少なすぎ: {calc}/{n}={calc/n:.0%} < {CALC_MIN_SHARE:.0%}（概念丸暗記に偏り）")

    # --- 答え分布(WARN) ---
    ans = [0,0,0,0]
    for q in qs:
        a = q.get("answer")
        if isinstance(a, int) and 1 <= a <= 4: ans[a-1] += 1
    if n and (max(ans) - min(ans)) > n * ANS_MAX_DEV_SHARE:
        warn.append(f"答え分布が偏り: ①②③④={'/'.join(map(str,ans))}")

    # --- “長さで当たる”/断定語/単純計算 ---
    len_tell, simple_calc = [], []
    for q in qs:
        ch = q.get("choices", []); a = q.get("answer")
        if len(ch) == 4 and isinstance(a, int) and 1 <= a <= 4:
            lc = len(ch[a-1]); ld = [len(c) for i, c in enumerate(ch,1) if i != a]
            md = sum(ld)/len(ld) if ld else 0
            if md and lc > LEN_TELL_RATIO*md and lc-md > LEN_TELL_GAP:
                len_tell.append(q.get("number"))
            for i, c in enumerate(ch, 1):
                if i != a and any(w in c for w in BAN):
                    review.append(f"{q.get('number')}:選択肢{i}")
        if is_calc(q):
            body = calc_body(q)
            if body.count("=") <= 1 and len(q.get("question","")) < 85:
                simple_calc.append(q.get("number"))
    if len_tell:
        share = len(len_tell)/n if n else 0
        line = f"正解が最長=“長さで当たる”疑い {len(len_tell)}/{n}={share:.0%}: {len_tell}"
        (warn if share > LEN_TELL_SHARE else info).append(line)
    if simple_calc:
        line = f"単純計算(1式代入)疑い {len(simple_calc)}問: {simple_calc}"
        (warn if len(simple_calc) >= SIMPLE_CALC_MIN else info).append(line)

    # --- 図の欠落(WARN) --- path=<root>/content/questions/<f>.json → root は3階層上
    root_of = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(path))))
    figdir = os.path.join(root_of, "assets", "figures")
    miss = sorted({q["figureImage"] for q in qs
                   if q.get("figureImage") and not os.path.exists(os.path.join(figdir, q["figureImage"]+".png"))})
    if miss:
        warn.append(f"図PNG欠落 {len(miss)}: {miss}（tools/gen_figures_ts.py も参照）")

    # --- 図の必須化＋「回答前/回答後」タグ整合(FAIL・恒久ルール／ユーザー厳命2026-09-18) ---
    #   厳命: 初学者のため【全問に例外なく図を付ける】。かつ各図は回答前/回答後を明示する。
    #   仕組み: App.tsx は figure=='required' の時だけ図を回答前から表示し、'helpful' は回答後(解説と一緒)。
    #   ゆえに全問が「figureImage(図キー) を持ち、figure が required か helpful」でなければならない。
    #     required = 問題理解に必要で答えを示唆しない図（回答前から表示）
    #     helpful  = 答えの根拠/答えを示唆しうる図（回答後に解説と一緒に表示）
    #   ※ 'none'・未設定・図キー欠落・不正タグは【すべて禁止＝抜け穴封じ】。作図が難しい抽象題材でも
    #     概念図/対比表/各項ラベル図などで必ず1枚付ける（[[cae-figure-before-after-rule]]）。
    #   例外: 文章主体で意味のある図が作れない題材(ISO9001品質保証・倫理・契約など)は
    #     q["figureExempt"]=true（かつ理由 figureExemptReason 必須）で図必須から除外(2026-09-21ユーザー承認)。
    #     技術題材ではこのフラグは使わない＝抜け穴にしない。
    no_or_bad_fig = [q.get("number") for q in qs
                     if not q.get("figureExempt")
                     and (q.get("figure") not in ("required", "helpful") or not q.get("figureImage"))]
    bad_exempt = [q.get("number") for q in qs
                  if q.get("figureExempt") and not str(q.get("figureExemptReason","")).strip()]
    if bad_exempt:
        hard.append(f"figureExempt に理由(figureExemptReason)が無い問 {len(bad_exempt)}: {bad_exempt}")
    if no_or_bad_fig:
        hard.append(
            f"図なし/不完全な問 {len(no_or_bad_fig)}/{n}: {no_or_bad_fig}"
            f"（全問に図必須。figureImage(図キー)＋前後タグ required=回答前 / helpful=回答後 を必ず付ける。"
            f"none・未設定・図キー欠落・不正タグは禁止）")

    # --- 回答前(required)の図に答えが写り込む事故ガード(FAIL) ---
    #   過去事故: 答えを図に描いて回答前(required)に出しネタバレ。required図は問題理解用で
    #   【答え・正解の値・結論を描かない】。少しでも答えを示唆するなら helpful(回答後)にする。
    #   PNGの中身は機械判定できないので、説明(figureHint)に正解がそのまま写る典型ケースを検出する。
    def _n(s): return re.sub(r"[\s$\\{}()\[\]、。,\.]+", "", str(s or ""))
    spoiler = []
    for q in qs:
        if q.get("figure") != "required":
            continue
        a = q.get("answer")
        chs = q.get("choices", [])
        if not (isinstance(a, int) and 1 <= a <= len(chs)):
            continue
        ans_txt = _n(chs[a-1]); hint = _n(q.get("figureHint", ""))
        # 正解選択肢の本文(数値/式)がそのまま図の説明に含まれる＝回答前に答えを見せる疑い
        if len(ans_txt) >= 4 and ans_txt in hint:
            spoiler.append(q.get("number"))
    if spoiler:
        hard.append(
            f"回答前(required)の図に正解が写り込む疑い {len(spoiler)}: {spoiler}"
            f"（答えを図に描いて回答前に出す事故。helpful=回答後に回すか、図から答え・結論を除く）")

    # --- トピック重複(WARN) ---
    keys = [(q.get("number"), norm(q.get("title","")), q.get("title","")) for q in qs]
    seen = {}; dup = []
    for num, k, _t in keys:
        if k and k in seen: dup.append(f"{seen[k]}≒{num}")
        seen[k] = num
    cross = []
    base = os.path.basename(path)
    for num, k, t in keys:
        if len(k) >= 4 and k in all_titles and all_titles[k] != base:
            cross.append(f"{num}『{t}』↔{all_titles[k]}")
    if dup:   warn.append(f"章内トピック重複: {dup}")
    if cross: warn.append(f"章間トピック重複(要統合): {cross[:6]}")

    # --- 公式標準問題との1:1対応/枝問ポリシー(§1.6) ---
    #  officialRef を1問でも持てば発動（既存章=未タグは無検査で通す＝後方互換）。
    if any("officialRef" in q for q in qs):
        prim = {}  # officialRef -> 本体(primary)件数
        for q in qs:
            num = q.get("number", "?"); ref = q.get("officialRef"); role = q.get("role")
            if not ref: hard.append(f"{num}: officialRef 欠落（1:1方針=全問に公式対応を付与）")
            if role not in ("primary", "branch"): hard.append(f"{num}: role は 'primary'|'branch' 必須(現:{role})")
            if role == "primary" and ref: prim[ref] = prim.get(ref, 0) + 1
        for ref, c in prim.items():
            if c > 1: hard.append(f"公式 {ref} に本体(primary)が{c}問（1:1違反=公式1問にアプリ本体は1問）")
        for q in qs:
            if q.get("role") == "branch":
                ref = q.get("officialRef")
                if ref and ref not in prim:
                    hard.append(f"{q.get('number')}: 枝問の対応先 {ref} に本体が無い（枝問は既存の公式番号に付ける・新番号禁止）")
        oc = d.get("meta", {}).get("officialCount"); P = len(prim)
        b = sum(1 for q in qs if q.get("role") == "branch")
        if isinstance(oc, int):
            if P > oc: hard.append(f"本体(標準問題)が公式Nを超過: 本体{P} > 公式{oc}（『超えない』違反）")
            elif P < oc: warn.append(f"1:1に不足: 本体{P} < 公式{oc}（公式{oc}問に本体が足りない=追加作成候補）")
        else:
            info.append("meta.officialCount 未設定（公式Nを入れると1:1超過を自動ガード）")
        info.append(f"1:1対応: 本体{P}・枝問{b}（officialRef方針・§1.6）")

    verdict = "FAIL" if hard else ("WARN" if warn else "PASS")
    return verdict, n, ans, hard, warn, info, review

def build_title_index(files):
    idx = {}
    for f in files:
        try: d = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        b = os.path.basename(f)
        for q in d.get("questions", []):
            t = norm(q.get("title",""))
            if len(t) >= 4: idx.setdefault(t, b)
    return idx

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qdir = os.path.join(root, "content", "questions")
    allfiles = sorted(glob.glob(os.path.join(qdir, "*.json")))
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    targets = allfiles if arg == "all" else [arg if os.path.isabs(arg) else os.path.join(root, arg)]
    order = {"PASS":0, "WARN":1, "FAIL":2}; worst = "PASS"
    for path in targets:
        others = [f for f in allfiles if os.path.abspath(f) != os.path.abspath(path)]
        all_titles = build_title_index(others)
        try:
            v, n, ans, hard, warn, info, review = check_file(path, all_titles)
        except Exception as e:
            print(f"[SKIP] {os.path.basename(path)}: 読めない({e})"); continue
        if order[v] > order[worst]: worst = v
        mark = {"PASS":"✅","WARN":"⚠️","FAIL":"❌"}[v]
        print(f"{mark} {v}  {os.path.basename(path)}  ({n}問, 答え①②③④={'/'.join(map(str,ans))})")
        for h in hard: print(f"    ❌ {h}")
        for w in warn: print(f"    ⚠️ {w}")
        for i in info: print(f"    ℹ️ {i}（しきい値内・参考）")
        if review:     print(f"    🔎 断定語の誤答(要目視・正当な引っかけかを確認): {review}")
    print(f"\n総合: {worst}  — FAIL=必ず修正 / WARN=しきい値超過（安易に見逃さない）/ PASS=基準クリア。"
          f"\n基準=第2章(solid-basics)・第3章(heat-basics)。新章はこの2章に品質を寄せる。")
    sys.exit(2 if worst == "FAIL" else 0)

if __name__ == "__main__":
    main()
