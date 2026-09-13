# -*- coding: utf-8 -*-
"""全問題JSONの figureImage を走査して src/figures.ts を自動生成。
未使用PNG(幽霊)と欠落PNGを検出して報告。"""
import json, os, glob
CAE=r"C:\Users\jwpsa\Documents\desktop\claude\CAE"
QDIR=os.path.join(CAE,"content","questions")
FDIR=os.path.join(CAE,"content","formulas")
FIG=os.path.join(CAE,"assets","figures")
TS=os.path.join(CAE,"src","figures.ts")

FORMULA_GROUP=200  # 公式専用の図はまとめて末尾のグループに置く
CHTITLE={1:"第1章 数学の基礎",2:"第2章 固体力学の基礎",3:"第3章 熱伝導の基礎",
         4:"第4章 有限要素法の定式化",5:"第5章 有限要素法の実践",
         6:"第6章 数値計算法の基礎",7:"第7章 要素テクノロジーの基礎",
         FORMULA_GROUP:"公式・用語の図（問題と共用しない専用図）"}

used={}  # key -> chapter
missing=[]
for p in glob.glob(os.path.join(QDIR,"*.json")):
    data=json.load(open(p,encoding="utf-8"))
    ch=data.get("meta",{}).get("chapter",99)
    for q in data.get("questions",[]):
        k=q.get("figureImage")
        if k:
            used[k]=ch
            if not os.path.exists(os.path.join(FIG,k+".png")):
                missing.append((k,q["number"]))

# 公式・用語(content/formulas/*.json)の figureImage も登録。問題と共用の図(既にusedにある)は
# 元の章グループを保ち、公式専用の図(例 s1f8*)だけ FORMULA_GROUP にまとめる。
for p in glob.glob(os.path.join(FDIR,"*.json")):
    data=json.load(open(p,encoding="utf-8"))
    for it in data.get("items",[]):
        k=it.get("figureImage")
        if k and k not in used:
            used[k]=FORMULA_GROUP
            if not os.path.exists(os.path.join(FIG,k+".png")):
                missing.append((k,it.get("id","?")))

# figures.ts 生成
lines=["// 問題の図解（実画像）。キー → 画像。",
       "// ※このファイルは tools/gen_figures_ts.py で自動生成（全問題JSON＋公式JSONの figureImage を走査）。",
       "// 画像は assets/figures/ に置く（figlib.py で生成した白地660x420 PNG）。",
       "import type { ImageSourcePropType } from 'react-native';",
       "",
       "export const FIGURES: Record<string, ImageSourcePropType> = {"]
for ch in sorted(set(used.values())):
    lines.append(f"  // {CHTITLE.get(ch, '第'+str(ch)+'章')}")
    for k in sorted(k for k,c in used.items() if c==ch):
        lines.append(f"  {k}: require('../assets/figures/{k}.png'),")
lines.append("};")
lines.append("")
lines.append("// 図の縦横比（全図とも 660x420 で生成）")
lines.append("export const FIGURE_ASPECT = 660 / 420;")
open(TS,"w",encoding="utf-8").write("\n".join(lines)+"\n")

# 幽霊PNG(参照されていないPNG)
allpng={os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(FIG,"*.png"))}
orphan=sorted(allpng - set(used.keys()))
print(f"figures.ts 生成: 使用キー {len(used)} 個")
print(f"欠落PNG(JSONが参照するがPNG無し): {missing if missing else 'なし'}")
print(f"幽霊PNG(PNGあるがどのJSONも未参照): {orphan if orphan else 'なし'}")
