# -*- coding: utf-8 -*-
r"""固体2級 ChatGPT製フラットSVG → PNG化＆既存figureキーへ差替(恒久ツール・2026-10-08)。

前提: 図\固体2級\fig{番号}.svg はChatGPT生成の中立(回答前)図・フラット構造(vib2のoverlay構造は無し)。
分担:
  ・中立(preFigureImage無し)   : fig{番号}.svg → figureImage キーのPNG(前後共用の1枚)。
  ・導出(preFigureImage有り)   : fig{番号}.svg(中立) → preFigureImage キー(回答前)。
                                 fig{番号}-ans.svg(注記入り) → figureImage キー(回答後)。
                                 ※ pre==fig の同一キー問題は中立扱い(fig{番号}.svgを1枚だけレンダ)。
レンダ: headless Chrome(viewBox読取り2x)。Bash実行時 dangerouslyDisableSandbox:true。

使い方:
  python tools/solid2_figures.py map [章]          章の fig番号→(figキー,preキー,中立/導出) を表示
  python tools/solid2_figures.py render [章]       章の中立/回答前PNG(+ -ans.svgがあれば回答後)を assets/figures へ出力
  python tools/solid2_figures.py render [章] --dry  実際に書かず対象だけ表示
  (章 省略で固体2級の全図。複数章は "5,6" のように)
"""
import os, re, glob, json, subprocess, sys, time, tempfile, shutil

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDIR = os.path.join(CAE, "content", "questions")
SVGDIR = os.path.join(CAE, "図", "固体2級")
FIG = os.path.join(CAE, "assets", "figures")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def solid2_files():
    out = []
    for fp in sorted(glob.glob(os.path.join(QDIR, "*.json"))):
        try:
            d = json.load(open(fp, encoding="utf-8"))
        except Exception:
            continue
        g = d.get("meta", {}).get("grade") or ""
        if "固体" in g and "2" in g:
            out.append(fp)
    return out


def build_map(chapters=None):
    """num -> {figKey, preKey, chapter} (図あり問題のみ)。chapters=章番号set で絞り込み。"""
    m = {}
    for fp in solid2_files():
        d = json.load(open(fp, encoding="utf-8"))
        ch = d["meta"].get("chapter")
        if chapters and ch not in chapters:
            continue
        for q in d["questions"]:
            fk = q.get("figureImage")
            pk = q.get("preFigureImage")
            if not (fk or pk):
                continue
            m[q["number"]] = {"fig": fk, "pre": pk, "ch": ch}
    return m


def viewbox(svg):
    s = open(svg, encoding="utf-8").read()
    mt = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', s)
    return (int(float(mt.group(1))), int(float(mt.group(2)))) if mt else (720, 420)


def render(svgpath, key):
    """呼び出しごとに専用プロファイルでレンダ(プロファイル競合の無音失敗を回避)。
    出力の更新時刻が呼出後であることを検証(旧ファイル残存での誤成功を防ぐ)。失敗時1回リトライ。"""
    w, h = viewbox(svgpath)
    out = os.path.join(FIG, key + ".png")
    for attempt in range(2):
        prof = tempfile.mkdtemp(prefix="s2fig_")
        t0 = time.time()
        try:
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                            "--user-data-dir=" + prof, "--default-background-color=FFFFFFFF",
                            "--force-device-scale-factor=2", "--screenshot=" + out,
                            "--window-size=%d,%d" % (w, h),
                            os.path.abspath(svgpath).replace("\\", "/")], capture_output=True, timeout=60)
        except Exception:
            pass
        finally:
            shutil.rmtree(prof, ignore_errors=True)
        if os.path.exists(out) and os.path.getsize(out) > 0 and os.path.getmtime(out) >= t0 - 1:
            return True
    return False


def do_render(chapters, dry=False):
    m = build_map(chapters)
    done = []; miss_ans = []; miss_svg = []
    for num, info in sorted(m.items(), key=lambda kv: (kv[1]["ch"] or 0, kv[0])):
        svg = os.path.join(SVGDIR, f"fig{num}.svg")
        if not os.path.exists(svg):
            miss_svg.append(num); continue
        fk, pk = info["fig"], info["pre"]
        deriv = bool(pk) and pk != fk
        neutral_key = pk if deriv else fk          # 回答前/中立の行き先
        if dry:
            tag = "導出" if deriv else "中立"
            print(f"  fig{num}.svg -> {neutral_key} [{tag}]" + (f"  / -ans -> {fk}" if deriv else ""))
        else:
            if neutral_key and render(svg, neutral_key):
                done.append(f"{num}->{neutral_key}")
        if deriv:
            ans = os.path.join(SVGDIR, f"fig{num}-ans.svg")
            if os.path.exists(ans):
                if not dry and render(ans, fk):
                    done.append(f"{num}-ans->{fk}")
            else:
                miss_ans.append(num)
    if not dry:
        print(f"[render] 出力 {len(done)} 枚")
    print(f"回答後(-ans.svg)未作成の導出: {len(miss_ans)}  {miss_ans}")
    if miss_svg:
        print(f"SVG欠落: {miss_svg}")


def do_map(chapters):
    m = build_map(chapters)
    n = dv = 0
    for num, info in sorted(m.items(), key=lambda kv: (kv[1]["ch"] or 0, kv[0])):
        fk, pk = info["fig"], info["pre"]
        deriv = bool(pk) and pk != fk
        if deriv: dv += 1
        else: n += 1
        print(f"  fig{num}.svg ch{info['ch']} fig={fk} pre={pk} [{'導出' if deriv else '中立'}]")
    print(f"合計 {n+dv} (中立{n} / 導出{dv})")


def parse_ch(args):
    for a in args:
        if re.fullmatch(r"[\d,]+", a):
            return set(int(x) for x in a.split(",") if x)
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 0
    cmd = args[0]; rest = args[1:]
    chapters = parse_ch(rest)
    if cmd == "map":
        do_map(chapters)
    elif cmd == "render":
        do_render(chapters, dry=("--dry" in rest))
    else:
        print("unknown:", cmd); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
