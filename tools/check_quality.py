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
import sys, os, json, glob, re, unicodedata, hashlib
from pathlib import Path

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

def editorial_digest(q):
    """Bind the semantic review to the complete current question, excluding review flags."""
    body = {k: v for k, v in q.items() if k not in ("editorialReview", "reviewed")}
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def question_nodes(data):
    """Include OTA subquestions in the same semantic/math/figure gates as ordinary questions."""
    def visit(q):
        yield q
        for field in ("parts", "studyParts"):
            parts = q.get(field)
            if isinstance(parts, list):
                for part in parts:
                    if isinstance(part, dict):
                        yield from visit(part)
    for q in data.get("questions", []):
        yield from visit(q)


def part_structure_errors(data):
    errors, ids = [], set()
    for q in question_nodes(data):
        parts = q.get("parts")
        if parts is not None and (not isinstance(parts, list) or any(not isinstance(p, dict) for p in parts)):
            errors.append(f"{q.get('number', '?')}: partsは設問オブジェクトの配列が必要")
            continue
        if parts:
            first, common = q, []
            while isinstance(first.get('parts'), list) and first['parts'] and isinstance(first['parts'][0], dict):
                if first.get('sharedQuestion'):
                    common.append(first['sharedQuestion'])
                first = first['parts'][0]
            if first.get('sharedQuestion'):
                common.append(first['sharedQuestion'])
            fallback = '\n\n'.join(common + [first.get('question', '')])
            if q.get('question') != fallback or any(q.get(k) != first.get(k) for k in ('choices', 'answer', 'explanation', 'easyExplanation', 'figure', 'figureImage', 'preFigureImage')):
                errors.append(f"{q.get('number', '?')}: 旧本体向けフィールドを先頭設問と同期してください")
            for p in parts:
                missing = [k for k in REQUIRED if k not in p]
                if missing:
                    errors.append(f"{q.get('number', '?')}: 設問の必須項目欠落 {missing}")
                if len(p.get('choices', [])) != 4 or type(p.get('answer')) is not int or not 1 <= p['answer'] <= 4:
                    errors.append(f"{p.get('number', '?')}: 設問の4択・正解番号が不正")
        else:
            key = q.get('id')
            if not isinstance(key, str) or not key or key in ids:
                errors.append(f"{q.get('number', '?')}: 学習対象のIDが空または重複")
            if isinstance(key, str):
                ids.add(key)
    return errors


EASY_EXPLANATION_MIN_CHARS = 1200


def easy_explanation_body_length(sections):
    """Count body text only: omit headings/whitespace; include inline math source."""
    return sum(len(re.sub(r"\s", "", section["body"])) for section in sections)


def easy_explanation_errors(data):
    """The length floor prevents under-explanation; semantic clarity is reviewed separately."""
    errors = []
    for q in question_nodes(data):
        num = q.get('number', '?')
        mode = q.get('explanationMode', data.get('meta', {}).get('explanationMode'))
        if mode not in (None, 'standard', 'guided'):
            errors.append(f'{num}: 解説表示形式が不正')
        if mode == 'guided' and (not q.get('easyExplanation') or not q.get('answerSummary')):
            errors.append(f'{num}: 標準詳解には本文と答えの要点が必要')
        figures = q.get('preFigures', [])
        if not isinstance(figures, list):
            errors.append(f'{num}: 回答前図は配列が必要')
            figures = []
        figures = list(figures)
        for section in q.get('easyExplanation', []) if isinstance(q.get('easyExplanation'), list) else []:
            if isinstance(section, dict):
                extra = section.get('figures', [])
                if not isinstance(extra, list):
                    errors.append(f'{num}: 解説図は配列が必要')
                else:
                    figures += extra
        for figure in figures:
            if not isinstance(figure, dict) or any(not isinstance(figure.get(k), str) or not figure[k].strip() for k in ('figureImage', 'caption')):
                errors.append(f'{num}: 図の参照と読み方の説明が必要')
        if "easyExplanation" not in q:
            continue
        sections = q["easyExplanation"]
        num = q.get("number", "?")
        if (not isinstance(sections, list)
                or any(not isinstance(section, dict)
                       or any(not isinstance(section.get(key), str) or not section[key].strip()
                              for key in ("title", "body")) for section in sections)):
            errors.append(f"{num}: やさしい解説の見出し・本文が不正または欠落")
            continue
        # 空配列は任意の補足を表示しない指定。作成された補足は下記の適用対象で下限を守る。
        # 固体1級は1〜6章の導出・読みやすさ優先を残りの章にも適用（2026-11-02）。
        meta = data.get("meta", {})
        concise_solid1 = (meta.get("grade") == "固体力学 1級"
                          and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
        # 統一解説へ改稿した固体2級1〜13章も、必要な導出と読みやすさで判断する。
        concise_solid2_guided = (meta.get("grade") == "固体力学 2級"
                                and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13) and mode == 'guided')
        # 熱流体1級・単相流1〜8章も統一教材へ移行。小問ごとに必要な説明を残し、水増ししない。
        concise_thermal1_guided = (meta.get("grade") == "熱流体力学 1級"
                                  and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8) and mode == 'guided')
        # 熱流体2級1〜11章も統合。必要な導出を優先し、文字数で水増ししない。
        concise_thermal2_guided = (meta.get("grade") == "熱流体力学 2級"
                                  and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11) and mode == 'guided')
        # JSONで数式のバックスラッシュを落とすと、nu等が制御文字として保存されても描画は通る。
        # 改稿済み単相流のインライン数式には実際の改行・タブ等を入れない。
        if concise_thermal1_guided or concise_thermal2_guided:
            for section in sections:
                for formula in re.findall(r'\$([^$]*)\$', section['body']):
                    if any(ord(c) < 32 for c in formula):
                        errors.append(f"{num}: 数式内に制御文字があります。LaTeXのエスケープを確認してください")
        if sections and not (concise_solid1 or concise_solid2_guided or concise_thermal1_guided or concise_thermal2_guided):
            length = easy_explanation_body_length(sections)
            if length < EASY_EXPLANATION_MIN_CHARS:
                errors.append(f"{num}: やさしく解説の本文が{length}字で"
                              f"{EASY_EXPLANATION_MIN_CHARS}字未満（見出し・空白除外）")
    return errors


# 公式で記述指定を確認済みの根拠の指紋。非公開原本を持たない配信CIでも制約を維持する。
# 新しい記述番号は保存済み公式テキストを人が確認した後にだけ登録する。
OFFICIAL_WRITTEN_EVIDENCE = {
    ('熱流体力学 1級', '7-1'): '89889cdee5f310ef434e32c7a5a76bf5f830b8d9f42bc5b9417bd1274614af33',
    ('熱流体力学 1級', '7-2'): '764f0065c06a844440e6b2bf8739b6fa59139e0ce651ae82dc111ce6ca9c9d37',
    ('熱流体力学 1級', '7-10'): 'a227b87861f13eeaea848314869aa21f424e7382cca5e949fedaa205f7f1f8b8',
    ('熱流体力学 1級', '8-7'): '26c0bea1da6a39e0f8affe8a83a9c7383173267dd4d9e4ece8d3873494b91b07',
    ('熱流体力学 1級', '8-8'): '4aa1368ed847f8d9f3ed400e7286d7bc12999bb05e5a4e054f02e78afc681b87',
    ('熱流体力学 1級', '8-12'): '9a2b29477c75f465b7a16fa2f703ac1f1bf256c7d02ee874a8e273d82379b2dd',
    ('熱流体力学 1級', '8-14'): '023a20e18fe2ff543d308b4904f03fa02bd5041932912cf27a8e664b59c984d2',
    ('熱流体力学 1級', '5-1'): '029c00140cdc2103f07967173c0d364be3ef199665e5cbdafa18e8e289f498e3',
    ('熱流体力学 1級', '5-5'): '68464147cdeb806d49a797ecc00397e8ba70bedd66fbe6ab797b994985cacb7c',
    ('熱流体力学 1級', '5-6'): 'a805ae4cebbab071834816d29066bacbddecde501fb78b726fee46801387e716',
    ('熱流体力学 1級', '5-10'): 'd82f9c29fd4ff722aa23e1df23e0e22062a406ed1caa938c1b37574e658f758c',
    ('熱流体力学 1級', '6-2'): '853a2e0b78c56064351affd735065f206f8978a85bb6554736b9e6b1fd8008d8',
    ('熱流体力学 1級', '6-3'): '391e17b8ada47e1657a4b8a05834436c3b44c2d2e62bfb379b8dd3202a97c5c8',
    ('熱流体力学 1級', '6-4'): 'cc95314aea2f80411a3907b78f48f86ee19eaf69d03807f457186746d243e847',
    ('熱流体力学 1級', '6-5'): 'e4099ed7a18ba3c51dad445e10709c5d84bfcae73aa74005e47e7f1c3838c5e7',
    ('熱流体力学 1級', '6-6'): '52e86e4d8de96cd0bcf06cc5a2b6a52f12ea06cd62f1d368a74bc75b0cb5b7d3',
    ('熱流体力学 1級', '6-7'): '8382eb6a4cbcfe3d45cb97c3604707ee8a39bf1e573dcf8353c58549d6276a6d',
    ('熱流体力学 1級', '6-8'): '99c9ff26998b5d3b3c294a2c40c978da663c6540a2d34005bbfab931e829e1b3',
    ('熱流体力学 1級', '6-9'): '5ac5266648ae7b6f7770f376624946db132257763bb101f96269e5bd48ea535d',
    ('熱流体力学 1級', '6-10'): 'f352b339a6fe2fc67b856f0980a380d86622b3cdccb42d4a473246e51df5b404',
    ('熱流体力学 1級', '6-11'): '4b1b2fe593d060a044c00ce59bbbf59c32ab03dcaff4e636407864d4ed4f803d',
    ('熱流体力学 1級', '6-12'): '3009eb399207e303cc118c81a4e79b3c4321fe1837306038aad009156f9275e3',
    ('熱流体力学 1級', '3-11'): '553f6f1db23dabbbf25d4556c4aa71127d3bfdefdb612af4ad3d1ca294fc2193',
    ('熱流体力学 1級', '3-12'): '8cf28030d510466d612d27e3223d1ba367e4b72e645ca1cc112d73def02b9a25',
    ('熱流体力学 1級', '4-3'): 'e72ae82fd9cc57dc07312561f423dbb9cd275a6b921b9870557dd9dfc956f76f',
    ('熱流体力学 1級', '4-4'): 'bd4b831d049fb36fdda86da563854fbec0f78f024c42331e7c5960ef4335f183',
    ('熱流体力学 1級', '4-6'): 'ff61e44dd0c90d3fc0df4af7462be489f13dbc504664308d901c888b11ecafb7',
    ('熱流体力学 1級', '4-10'): 'aeb2c81a4d263ebdbca7929b00898011ed19db232031ebb26103aa7db294b28f',
    ('熱流体力学 1級', '1-1'): '6b1f2f7fa9f4739ea360ed97d318524d059ecdcdd74de68508ed74edaa985c0f',
    ('熱流体力学 1級', '1-2'): '1e69a5795c0307dae5b815d3ac028c02d4504ce3080ee4c07fd0cf98773df3be',
    ('熱流体力学 1級', '1-3'): '61a0c0f219bdf57aee01d1446865fb1fe71ec870ffc82e7c701a97db6a9002f7',
    ('熱流体力学 1級', '2-7'): 'e615b446064eddbdcc35f87e996de37c086c770c0cea4e96711ee4c2d36a403c',
    ('熱流体力学 1級', '2-8'): 'bfa26875e205f91e92c5d69974f84f7c16e76a66d20626b8136ca4842c4e878d',
    ('固体力学 1級', '10-1'): 'df57380ec5af6c02cda36667e44bf92b88964f8f273c69347a402503ade41881',
    ('固体力学 1級', '10-6'): '9943656f19f0f52926da8a58451d6ad536b0c920f87478cd3b66f1daff343ed0',
    ('固体力学 1級', '10-7'): 'bc98c5666d4eb2f42f035e813c11960a8f2b9d14c59d47dd6e76d25adde0ed31',
    ('固体力学 1級', '10-10'): 'a378bcebb6477cd8d15437627e717f5850238b0765b531009b759e5e339ff975',
    ('固体力学 1級', '11(1)-2'): '763fd0cc610f06a5187d59974af9e5d12ef41f766a5c5329b6ddaef6ff069092',
    ('固体力学 1級', '11(1)-4'): '64193e884e83c41374aabbef71d20f9877cb17514092a83d20e6c5f034a448b9',
    ('固体力学 1級', '11(2)-2'): 'b6629cc2c71c47ebe761f3ca3966b1f3fbd0944d4a50f17d6bba27ace0b9103e',
    ('固体力学 1級', '11(2)-3'): 'f604afd434d65f447934fec8155ce2e18234cbd5b621d87cbc85eda530302b7d',
    ('固体力学 1級', '11(2)-4'): '37fd0070379282fdb9b4862c3cecf013667a25d40af75635130ef2542cf4c1a3',
    ('固体力学 1級', '11(3)-1'): '952906612a56f65e1bb72421b1b8f2d7a51a92e252eb81509212bd46344b587a',
    ('固体力学 1級', '11(3)-2'): 'faaa61badc0e5eb2657b3b2db8f57317e62082af8035e6b86376c593bd859c19',
    ('固体力学 1級', '11(3)-3'): '2306d976289ddfdec5dbdc11cf280b33328d3e10e76f4dbeb8a6eb3dc528d825',
    ('固体力学 1級', '11(3)-4'): '08cc8a77c1aabd8becc1f81027ade2a662b2aed8b8a5febee16dfcde629b1345',
    ('固体力学 1級', '1-8'): 'f2e3da5dd2af3e0c4083cef41a77b1864c79f67d65ab6d016356cc9393dda000',
    ('固体力学 1級', '1-9'): '0c84bc18c8a6ba825cd849ff52eb0d20760c6c5a79ee4ba233a3560bed1e9aca',
    ('固体力学 1級', '1-10'): 'b3d667371e311a526821fc7869e497c15301958c10879d2f1e8a862732a44835',
    ('固体力学 1級', '1-11'): '88e8aa961cbda36124b4a8e85b3a15c7a0d63b86ad317c410865b63787a5cef0',
    ('固体力学 1級', '1-17'): 'dcb489d5ede0360363f3274a9223e1c93195a8ea26d3e542d73041bbc16d51b2',
    ('固体力学 1級', '1-18'): 'b9fbcb67a7ee373036ebb13bc6af4a05aa615401085479d7837d09059cca8d19',
    ('固体力学 1級', '2-8'): '923acceee1ea8db892ce2f8292cbdd719256bba9849d9ffd5710096896701ebf',
    ('固体力学 1級', '2-13'): '239ed1275aed786ddf58b4fdefb90538ace95450e2c8d223a2212c23b6409cdb',
    ('固体力学 1級', '3-2'): '68bd72f583179d43faa2a0c11ea1b835b4d50b50d2f77b2469f439459a5dbed1',
    ('固体力学 1級', '3-7'): '6773dbe09d81966243ed0862042a33dfd54b1d6aec86c72d4ed798cb8718886a',
    ('固体力学 1級', '4-4'): 'ca43f53ec951a75c51e6e9c25f528e9e3f223e6edcf4e95a7f9c4086f540856a',
    ('固体力学 1級', '4-7'): '09953b153fd8e46fd6d88ffbf41b358234dddfcf64b2a407d11b0ed48dba2159',
    ('固体力学 1級', '4-8'): '476ecd2a6f7315e66fefabbaa87534ba5553aebabca5d16ddf34f20167c6567a',
    ('固体力学 1級', '4-10'): '303ffbf2c3be62f4da69ca41ad8da2fc62d550f09c122aa0f1bffc413e9b0f3d',
    ('固体力学 1級', '4-11'): '3ab564ea805c6f291e5680044f4060410a39a9a1c3a3da8d8aac3f275a4936a3',
    ('固体力学 1級', '4-12'): '92d4fe24e25d673d4d5178dd540c5964784cc681bf75d48823fc11197c68adc5',
    ('固体力学 1級', '5-13'): '27ba22d777aaa30b5592b9bc6a86d46dc3555d2e7474f399d449e8fea39178b0',
    ('固体力学 1級', '6-3'): '51cee17d8ff06d9e919ed515b82039f7d0ddf95eb805982f84c3c5541da6597d',
    ('固体力学 1級', '6-4'): 'a08eaf5d6d4f76fded78c2b5ebdd3316c63d750442e056bf4b7b415b06ca59b4',
    ('固体力学 1級', '6-6'): '7c0fa25216c4e5df460ddd964cb7a9d18bc0fc3431878c35f40436300fb8699e',
    ('固体力学 1級', '6-10'): 'd1d2a7cbeaaca9ba8f671a5d3c7505241923bf488792ae6efa0a3092d150ab00',
    ('固体力学 1級', '6-15'): 'a0399176f63bf71cc309b2ff7a7e8df20c1ba622b1d0ae874d5f9b67c8ffa808',
    ('固体力学 1級', '6-16'): 'c0b27bcd234d7afb65b49aa0130bb03e0702a85cf422ade7ce00999f5ca83e3b',
    ('固体力学 1級', '6-17'): '621e561756eb9f0fc2611c62eb3945cca131e1273a99f2c59b48ba8805accca0',
    ('固体力学 1級', '6-18'): 'd4aa58d8cff596ba16dd190468fb693def6b502300319f02f4f2709287af393f',
    ('固体力学 1級', '6-19'): '946752a84e756449c81533305fb47f359bd37a7dcd69aede28670c3aa688a4df',
    ('固体力学 1級', '7-4'): '8e7946a66eea301c81a22d262fcc1cb8ea0116e0c444648eb952946ed2302bfa',
    ('固体力学 1級', '7-9'): 'e95066ccc349d0f2d0f46da1a2db43a2e8afc2377eaab72d7c3af2e78fbd7333',
    ('固体力学 1級', '7-10'): '46c968c6b578a4ac5a425c36c80ec7e955650babbc346c47afa509f759b37a87',
    ('固体力学 1級', '7-11'): '2140cf35970fd4d63f2a2c74f5532f0fcdf2dab8f5f70ccc35442def1eecba3d',
    ('固体力学 1級', '8-2'): '1b50cfc1c8c5e22944cffaa5e3d8d6851dd3eb06611e8aeb2efc5600232e8a15',
    ('固体力学 1級', '8-8'): '3cecb8a4a8e0e82f7143c09f66e816e9617358d8b7e33e64facac3342ff42873',
    ('固体力学 1級', '8-9'): '7b8502000f5af92247bf274cbe5c0fb8c4ce90332b34dacfb95a80ff4ffd356e',
    ('固体力学 1級', '8-10'): 'cf6b1493bb7e8d104113d70e3d0cdb9cddd05a690e174dade7ae64333dc0cecc',
    ('固体力学 1級', '8-12'): 'e626e6e78f1aa020873455cd502e3bfbb469ad368d470bf906e4b238b97bb205',
    ('固体力学 1級', '8-13'): '51023d46632b259c25ae2d1f278e383df86620bc4e9ffe882a5801cb47d80e11',
    ('固体力学 1級', '8-14'): '87481f069b2e42eca0665781dc4445cc9e936ff47be8c79da172b352fbf7ddac',
    ('固体力学 1級', '8-15'): 'fca77c93fc929a4cb31297601069187a625ed145d46970dac9251f0cd270e607',
    ('固体力学 1級', '8-19'): '02b414760fe2f76344ba88d26567ebac3c07114e9cd8aa6cdb1569b7315fbbde',
    ('固体力学 1級', '9-9'): 'ff22c3288ac80dbdcfd99599322405f2810c2e550cb05c2d27c0bf9aa387ae11',
}


def study_parts_errors(data):
    errors, ids = [], set()
    root = Path(__file__).resolve().parent.parent
    for parent in question_nodes(data):
        if 'studyParts' not in parent:
            continue
        parts = parent['studyParts']
        if not isinstance(parts, list) or not parts or any(not isinstance(p, dict) for p in parts):
            errors.append(f"{parent.get('number')}: 小問は空でない配列が必要")
            continue
        for part in parts:
            num = part.get('number', '?')
            key = part.get('id')
            if not key or key in ids or key == parent.get('id'):
                errors.append(f'{num}: 小問の固定IDが空または重複')
            ids.add(key)
            if part.get('number') != parent.get('number') or part.get('officialRef') != parent.get('officialRef'):
                errors.append(f'{num}: 小問は親の公式番号を保持してください')
            if part.get('parts') or part.get('studyParts'):
                errors.append(f'{num}: 同一画面の小問は入れ子にしません')
            if part.get('responseType') == 'written':
                if part.get('choices') != [] or part.get('answer') != 0 or not part.get('modelAnswer') or not part.get('answerCheckpoints'):
                    errors.append(f'{num}: 記述式には解答例・自己確認点が必要です')
                evidence = part.get('officialWrittenEvidence', {})
                source = root / evidence.get('file', '')
                excerpt = evidence.get('excerpt', '')
                allowed = (root / '_原本(非公開)' / '_抽出テキスト').resolve()
                fingerprint = hashlib.sha256((evidence.get('file', '') + '\n' + excerpt).encode('utf-8')).hexdigest()
                registered = OFFICIAL_WRITTEN_EVIDENCE.get((data.get('meta', {}).get('grade'), num))
                # 記述・数値記入・語句記入の形式を原文で確認した指紋だけを許可する。
                # 「記述選択」等のキーワード一致では登録せず、手元では根拠の原文にも照合する。
                if (not source.resolve().is_relative_to(allowed) or fingerprint != registered
                    or not re.search(r'(?:問\s*|^(?:#{1,6}|-)\s+)' + re.escape(str(num)) + r'(?![\d-])', excerpt, re.MULTILINE)
                    or (source.is_file() and excerpt not in source.read_text(encoding='utf-8-sig'))):
                    errors.append(f'{num}: 公式の記述式である根拠を保存済みテキストから確認してください')
            elif part.get('responseType', 'choice') != 'choice' or len(part.get('choices', [])) not in (2, 4) or type(part.get('answer')) is not int or not 1 <= part['answer'] <= len(part['choices']):
                errors.append(f'{num}: 小問は2択・4択または公式記述式にしてください')
    return errors


def editorial_errors(data):
    """Semantic judgement is manual; missing/stale judgement is a blocking error.

    Unchanged legacy material is grandfathered once, never automatically certified.
    Do not regenerate the baseline after an edit: review the changed question instead.
    """
    meta = data.get("meta", {})
    target = ((meta.get("grade") == "振動 1級" and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9))
              or (meta.get("grade") == "振動 2級" and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
              or meta.get("grade") == "固体力学 2級"
              or (meta.get("grade") == "固体力学 1級" and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
              or (meta.get("grade") == "熱流体力学 1級" and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8))
              or (meta.get("grade") == "熱流体力学 2級" and meta.get("chapter") in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)))
    if not target:
        return easy_explanation_errors(data) + part_structure_errors(data) + study_parts_errors(data)
    baseline_path = Path(__file__).with_name("solid2_editorial_baseline.json")
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))["legacy"]
    legacy = {key: value for chapter in baseline.values() for key, value in chapter.items()}
    errors = easy_explanation_errors(data) + part_structure_errors(data) + study_parts_errors(data)
    for q in question_nodes(data):
        num = q.get("number", "?")
        review = q.get("editorialReview")
        signature = editorial_digest(q)
        if review is None and legacy.get(q.get("id")) == signature:
            continue
        if not isinstance(review, dict):
            errors.append(f"{num}: 公式論点・誤答肢の内容確認が未記録")
            continue
        for key in ("officialPoint", "alignment"):
            if not isinstance(review.get(key), str) or not review[key].strip():
                errors.append(f"{num}: {key} の内容確認が未記録")
        expected = {str(i) for i in range(1, len(q.get('choices', [])) + 1) if i != q.get("answer")}
        reasons = review.get("distractorMisconceptions")
        if (not isinstance(reasons, dict) or set(reasons) != expected
                or any(not isinstance(v, str) or not v.strip() for v in reasons.values())):
            errors.append(f"{num}: 各誤答肢が表す同一論点内の誤解が未記録")
        if not q.get("officialRef"):
            errors.append(f"{num}: officialRef が未記録")
        if review.get("sha256") != signature:
            errors.append(f"{num}: 内容変更後の公式論点・誤答肢の再確認が必要")
    return errors



def presentation_errors(data):
    """Block unapproved vector/PNG pairs and unrendered math, without new ledgers.

    The active chapter opts in; solid1 chapter1 is mandatory. Visual clarity remains
    a manual judgement. Standard-library checks also run in the OTA job.
    """
    import xml.etree.ElementTree as ET
    import struct
    meta = data.get("meta", {})
    mandatory = meta.get("grade") == "固体力学 1級" and meta.get("chapter") == 1
    if not mandatory and not meta.get("presentationStyle"):
        return []
    errors = []
    if meta.get("presentationStyle") != "cae-standard-v1":
        errors.append("指定図式の確認が未適用: presentationStyle")
    root = Path(__file__).resolve().parent.parent
    grade = "1級" if "1級" in meta.get("grade", "") else "2級"
    thermal = "熱流体" in meta.get("grade", "")
    vibration = "振動" in meta.get("grade", "")
    directory = root / "図" / (("振動" if vibration else "熱流体" if thermal else "固体") + grade) / ("第%02d章" % meta["chapter"])
    records = list(question_nodes(data))
    term_path = root / "content" / "formulas" / (("vib" + grade[0] + "-" if vibration else "thermal" + grade[0] + "-" if thermal else "solid1-" if grade == "1級" else "") + "ch%d.json" % meta["chapter"])
    if term_path.exists():
        records += json.loads(term_path.read_bytes()).get("items", [])
    keys = set()
    def visible(v):
        if isinstance(v, str):
            # 旧用語データの表示数式もレンダラーが処理する。本文への露出だけを検出する。
            plain = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$]*\$", "", v)
            if "^" in plain or re.search(r"\\(?:frac|mathbf|partial|sqrt|begin)\b", plain):
                errors.append("未組版の数式記号が本文に露出しています")
            if v.count("$") % 2:
                errors.append("数式の区切りが閉じていません")
        elif isinstance(v, list):
            for x in v: visible(x)
        elif isinstance(v, dict):
            for x in v.values(): visible(x)
    def collect_figures(value):
        if isinstance(value, dict):
            for k, v in value.items():
                if k in ('figureImage', 'preFigureImage') and isinstance(v, str) and v:
                    keys.add(v)
                elif isinstance(v, (dict, list)):
                    collect_figures(v)
        elif isinstance(value, list):
            for v in value: collect_figures(v)
    for record in records:
        collect_figures(record)
        if record.get("term") and record.get("summary"):
            if any("$" in record.get(k, "") for k in ("term", "summary", "figureCaption")):
                errors.append(record.get("id", "用語") + ": 通常文字の見出し・要点・図注に数式コードがあります")
            if record.get("figureImage") and not record.get("figureCaption", "").strip():
                errors.append(record.get("id", "用語") + ": 図と説明を結ぶ図注がありません")
        for key, value in record.items():
            if key in ("question", "sharedQuestion", "choices", "explanation", "easyExplanation", "formula", "body", "example", "term", "summary", "figureCaption", "exampleLabel", "title", "answerSummary", "modelAnswer", "answerCheckpoints", "preFigures"):
                visible(value)
            if key in ("figureImage", "preFigureImage") and value:
                keys.add(value)
    assets = {}
    for source in directory.glob("*.svg"):
        try:
            svg = ET.fromstring(source.read_bytes())
            key = svg.get("data-asset-key")
            if key in keys:
                if key in assets: errors.append(key + ": 図原本の登録が重複")
                assets[key] = (source, svg)
        except ET.ParseError:
            errors.append(source.name + ": SVGが不正")
    colors = {"#1F3A65", "#C82D2D", "#888888", "#E1E7F2", "#FFFFFF", "none"}
    for key in sorted(keys):
        if key not in assets:
            errors.append(key + ": 指定体裁のSVG原本が未確認")
            continue
        source, svg = assets[key]
        if svg.get("data-style") != "cae-standard-v1" or svg.get("data-font") != "Meiryo" or svg.get("viewBox") != "0 0 660 420":
            errors.append(key + ": 図の体裁・フォント・寸法が指定外")
        for e in svg.iter():
            tag = e.tag.rsplit("}", 1)[-1]
            if tag in ("text", "image", "foreignObject", "script", "style"):
                errors.append(key + ": 未パス化文字・ラスター等の指定外要素")
            for attr, val in e.attrib.items():
                if attr in ("fill", "stroke") and val not in colors:
                    errors.append(key + ": 指定外の色 " + val)
                if attr.endswith("href") or attr == "style" or ("opacity" in attr and val != "1"):
                    errors.append(key + ": 外部参照・透過・個別CSSを使用")
                if attr == "aria-label" and ("^" in val or "_" in val or re.search(r"\b[A-Z]dot\b|\\[a-zA-Z]", val)):
                    errors.append(key + ": 図中の数式コードが未組版")
        rect = next((e for e in svg if e.tag.endswith("}rect")), None)
        if rect is None or any(rect.get(k) != v for k, v in {"width":"660","height":"420","fill":"#FFFFFF"}.items()):
            errors.append(key + ": 白い不透明背景がありません")
        asset = root / "assets" / "figures" / (key + ".png")
        if not asset.exists():
            errors.append(key + ": PNGがありません")
            continue
        png = asset.read_bytes()
        if png[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", png[16:24]) != (1320, 840):
            errors.append(key + ": PNG寸法が指定外")
        if svg.get("data-png-sha256") != hashlib.sha256(png).hexdigest():
            errors.append(key + ": PNGが確認済みSVGの出力と不一致（図の差替えを拒否）")
    return list(dict.fromkeys(errors))

def require_editorial_review(data):
    errors = editorial_errors(data) + presentation_errors(data)
    if errors:
        raise ValueError("教材の内容確認ゲート: " + "; ".join(errors))


def check_file(path, all_titles):
    d = json.load(open(path, encoding="utf-8"))
    qs = d.get("questions", [])
    n = len(qs)
    hard, warn, info, review = editorial_errors(d) + presentation_errors(d), [], [], []

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

    # --- 公式問題に無い要点の付け足し疑い(WARN・2026-10-16-R16) ---
    #   受験生の負担になる脱線・発展・別論点の付け足しを機械で“気づかせる”signal。
    #   最終判断は人/AIが公式問題と照合して行う(R10と同じ思想・FAILにはしない)。
    OFF_SCOPE = ("参考までに", "ちなみに", "余談", "発展として", "発展的",
                 "応用として", "さらに発展", "本題から外れ", "試験には出",
                 "より進んだ", "より高度", "余力があれば")
    off = [q.get("number") for q in qs
           if any(m in (q.get("explanation", "") or "") for m in OFF_SCOPE)]
    if off:
        warn.append(f"公式問題に無い要点の付け足し疑い(脱線・発展) {len(off)}問: {off}"
                    f"（R16: 原問が問う点だけに絞り、最小労力で合格できる範囲にする）")

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
    figkeys = set()
    for q in qs:
        for kk in (q.get("figureImage"), q.get("preFigureImage")):  # 回答後図＋回答前図の両方
            if kk:
                figkeys.add(kk)
    miss = sorted({k for k in figkeys if not os.path.exists(os.path.join(figdir, k+".png"))})
    if miss:
        warn.append(f"図PNG欠落 {len(miss)}: {miss}（tools/gen_figures_ts.py も参照）")

    # --- 前後2図(preFigureImage)の整合(FAIL・恒久ルール[[cae-figure-before-after-rule]]) ---
    #   必要に応じ1問に図を2枚持てる: preFigureImage=回答前(答えを一切示さない配置図/概念図)、
    #   figureImage=回答後(答えの根拠・解説図)。前後で出し分ける(App.tsx)。
    #   ・preFigureImage を使うなら figureImage(回答後図) も必須。回答前だけ図で回答後に図なしは不可。
    #   ・回答前図に答えを描かない(値・結論・公式の結果)。描くなら回答後(figureImage)に回す。
    pre_bad = [q.get("number") for q in qs
               if q.get("preFigureImage") and not q.get("figureImage")]
    if pre_bad:
        hard.append(f"preFigureImage(回答前図)があるのに figureImage(回答後図)が無い問 {len(pre_bad)}: {pre_bad}"
                    f"（前後2図は回答前=preFigureImage/回答後=figureImage の対で使う）")

    # 不要な図を省く現行方針。固体1級の統一教材でも文章だけで明快な問へ図を強制しない。
    solid2 = d.get("meta", {}).get("grade") == "固体力学 2級"
    optional_figures = solid2 or (
        d.get("meta", {}).get("grade") == "固体力学 1級"
        and d.get("meta", {}).get("explanationMode") == "guided")
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
                     and (not optional_figures or q.get("figureImage") or q.get("figure") in ("required", "helpful"))
                     and (q.get("figure") not in ("required", "helpful") or not q.get("figureImage"))]
    bad_exempt = [q.get("number") for q in qs
                  if q.get("figureExempt") and not str(q.get("figureExemptReason","")).strip()]
    if bad_exempt:
        hard.append(f"figureExempt に理由(figureExemptReason)が無い問 {len(bad_exempt)}: {bad_exempt}")
    if no_or_bad_fig:
        hard.append(
            f"図なし/不完全な問 {len(no_or_bad_fig)}/{n}: {no_or_bad_fig}"
            f"（図を付ける問はキーと前後タグをそろえる。固体2級・固体1級の統一教材は不要図の省略可）")

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
            worst = "FAIL"
            print(f"[FAIL] {os.path.basename(path)}: 検査できない({e})"); continue
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
