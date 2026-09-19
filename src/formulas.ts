// 公式・用語コンテンツの束ね（章 → 公式/用語カード）。
// ※Metro は動的 import 不可なので、章ごとの JSON をここで静的 import する。
import ch1 from '../content/formulas/ch1.json';
import ch2 from '../content/formulas/ch2.json';
import ch3 from '../content/formulas/ch3.json';
import ch4 from '../content/formulas/ch4.json';
import ch5 from '../content/formulas/ch5.json';
import ch6 from '../content/formulas/ch6.json';
import ch7 from '../content/formulas/ch7.json';
import ch8 from '../content/formulas/ch8.json';
import ch9 from '../content/formulas/ch9.json';
import ch10 from '../content/formulas/ch10.json';
import ch11 from '../content/formulas/ch11.json';
import ch12 from '../content/formulas/ch12.json';
import ch13 from '../content/formulas/ch13.json';
// 固体1級（章 id は2級と重複するため 's1' 接頭辞のキーで束ねる）。
import s1ch1 from '../content/formulas/solid1-ch1.json';
import s1ch2 from '../content/formulas/solid1-ch2.json';
import s1ch3 from '../content/formulas/solid1-ch3.json';
import s1ch4 from '../content/formulas/solid1-ch4.json';
import s1ch5 from '../content/formulas/solid1-ch5.json';
import s1ch6 from '../content/formulas/solid1-ch6.json';
import s1ch7 from '../content/formulas/solid1-ch7.json';
import s1ch8 from '../content/formulas/solid1-ch8.json';
import s1ch9 from '../content/formulas/solid1-ch9.json';
import s1ch10 from '../content/formulas/solid1-ch10.json';
import s1ch11 from '../content/formulas/solid1-ch11.json';

import t2ch1 from '../content/formulas/thermal2-ch1.json';
import t2ch2 from '../content/formulas/thermal2-ch2.json';
import t2ch3 from '../content/formulas/thermal2-ch3.json';
import t2ch4 from '../content/formulas/thermal2-ch4.json';
import t2ch5 from '../content/formulas/thermal2-ch5.json';
import t2ch6 from '../content/formulas/thermal2-ch6.json';
import t2ch7 from '../content/formulas/thermal2-ch7.json';
import t2ch8 from '../content/formulas/thermal2-ch8.json';
import t2ch9 from '../content/formulas/thermal2-ch9.json';
import t2ch10 from '../content/formulas/thermal2-ch10.json';
import t2ch11 from '../content/formulas/thermal2-ch11.json';
// 熱流体力学 1級（単相流）
import t1ch1 from '../content/formulas/thermal1-ch1.json';
import t1ch2 from '../content/formulas/thermal1-ch2.json';
import t1ch3 from '../content/formulas/thermal1-ch3.json';
import t1ch4 from '../content/formulas/thermal1-ch4.json';
import t1ch5 from '../content/formulas/thermal1-ch5.json';

export type FormulaItem = {
  id: string;
  kind: 'formula' | 'term';
  term: string;
  formula?: string; // $...$ を含んでよい（KaTeX描画）
  body: string;
  example?: string;
  figureImage?: string; // src/figures.ts の FIGURES キー
};

export type FormulaDoc = {
  chapter: number;
  title: string;
  intro?: string;
  items: FormulaItem[];
};

// 章ID(catalog と一致: ch1..ch13) → コンテンツ。null は準備中。
export const FORMULA_DOCS: Record<string, FormulaDoc | null> = {
  ch1: ch1 as unknown as FormulaDoc,
  ch2: ch2 as unknown as FormulaDoc,
  ch3: ch3 as unknown as FormulaDoc,
  ch4: ch4 as unknown as FormulaDoc,
  ch5: ch5 as unknown as FormulaDoc,
  ch6: ch6 as unknown as FormulaDoc,
  ch7: ch7 as unknown as FormulaDoc,
  ch8: ch8 as unknown as FormulaDoc,
  ch9: ch9 as unknown as FormulaDoc,
  ch10: ch10 as unknown as FormulaDoc,
  ch11: ch11 as unknown as FormulaDoc,
  ch12: ch12 as unknown as FormulaDoc,
  ch13: ch13 as unknown as FormulaDoc,
  // 固体1級 第8章 要素テクノロジー（catalog の formulaId と一致）
  s1ch1: s1ch1 as unknown as FormulaDoc,
  s1ch2: s1ch2 as unknown as FormulaDoc,
  s1ch3: s1ch3 as unknown as FormulaDoc,
  s1ch4: s1ch4 as unknown as FormulaDoc,
  s1ch5: s1ch5 as unknown as FormulaDoc,
  s1ch6: s1ch6 as unknown as FormulaDoc,
  s1ch7: s1ch7 as unknown as FormulaDoc,
  s1ch8: s1ch8 as unknown as FormulaDoc,
  s1ch9: s1ch9 as unknown as FormulaDoc,
  s1ch10: s1ch10 as unknown as FormulaDoc,
  s1ch11: s1ch11 as unknown as FormulaDoc,
  // 熱流体力学 2級
  t2ch1: t2ch1 as unknown as FormulaDoc,
  t2ch2: t2ch2 as unknown as FormulaDoc,
  t2ch3: t2ch3 as unknown as FormulaDoc,
  t2ch4: t2ch4 as unknown as FormulaDoc,
  t2ch5: t2ch5 as unknown as FormulaDoc,
  t2ch6: t2ch6 as unknown as FormulaDoc,
  t2ch7: t2ch7 as unknown as FormulaDoc,
  t2ch8: t2ch8 as unknown as FormulaDoc,
  t2ch9: t2ch9 as unknown as FormulaDoc,
  t2ch10: t2ch10 as unknown as FormulaDoc,
  t2ch11: t2ch11 as unknown as FormulaDoc,
  // 熱流体力学 1級（単相流）
  t1ch1: t1ch1 as unknown as FormulaDoc,
  t1ch2: t1ch2 as unknown as FormulaDoc,
  t1ch3: t1ch3 as unknown as FormulaDoc,
  t1ch4: t1ch4 as unknown as FormulaDoc,
  t1ch5: t1ch5 as unknown as FormulaDoc,
};

export function formulaDoc(chapterId: string): FormulaDoc | null {
  return FORMULA_DOCS[chapterId] ?? null;
}
