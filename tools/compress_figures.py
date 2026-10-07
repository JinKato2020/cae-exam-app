# -*- coding: utf-8 -*-
r"""assets/figures/*.png を画質を保ったまま軽量化(パレット化+最適化)。
図は平面的な線画・表・概念図が大半なので、PNG-8(パレット)化で見た目そのまま大幅減。
画像ごとに色数を見て自動判定:
  色数 <= 4000      : 128色パレット(単純な線画・表)
  4000 < 色数       : 256色パレット(アンチエイリアス多・淡いグラデーション)
  色数 > 300000     : 写真級 → RGBのまま optimize のみ(パレット化しない=バンディング防止)
元がパレットPNGや既に小さいものは、増えたら元を維持(退行防止)。
  python tools/compress_figures.py --dry    … 見積りのみ(書き換えない)
  python tools/compress_figures.py [接頭辞] … 実行(接頭辞指定で対象限定 例 v2e)
"""
import os, sys, glob, io
from PIL import Image

CAE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(CAE, "assets", "figures")

def compress_bytes(path):
    """圧縮後のPNGバイト列を返す(書き込みはしない)。元より大きければ None。"""
    orig = os.path.getsize(path)
    im = Image.open(path).convert("RGB")
    colors = im.getcolors(maxcolors=300000)  # 色数が多すぎると None
    buf = io.BytesIO()
    if colors is None:
        im.save(buf, format="PNG", optimize=True)               # 写真級: 無劣化で最適化のみ
    else:
        n = 128 if len(colors) <= 4000 else 256
        q = im.quantize(colors=n, method=Image.FASTOCTREE, dither=Image.NONE)
        q.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    return data if len(data) < orig else None                   # 増えるなら据え置き

def main(dry, prefix):
    fs = sorted(glob.glob(os.path.join(FIG, prefix + "*.png")))
    before = after = 0; changed = skipped = 0
    for i, p in enumerate(fs):
        o = os.path.getsize(p); before += o
        try:
            data = compress_bytes(p)
        except Exception as e:
            data = None; print("  ! skip", os.path.basename(p), e)
        if data is None:
            after += o; skipped += 1
        else:
            after += len(data); changed += 1
            if not dry:
                open(p, "wb").write(data)
        if (i + 1) % 500 == 0:
            print("  ...%d/%d" % (i + 1, len(fs)))
    print("[%s] %d枚: %.0fMB → %.0fMB (−%.0f%%)  圧縮%d / 据置%d"
          % ("DRY" if dry else "DONE", len(fs), before / 1048576, after / 1048576,
             (1 - after / before) * 100 if before else 0, changed, skipped))

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if a != "--dry"]
    main("--dry" in sys.argv, args[0] if args else "")
