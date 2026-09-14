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
import s1ch8 from '../content/formulas/solid1-ch8.json';
import s1ch9 from '../content/formulas/solid1-ch9.json';

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
  s1ch8: s1ch8 as unknown as FormulaDoc,
  s1ch9: s1ch9 as unknown as FormulaDoc,
};

export function formulaDoc(chapterId: string): FormulaDoc | null {
  return FORMULA_DOCS[chapterId] ?? null;
}
