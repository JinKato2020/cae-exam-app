// 公式・用語コンテンツの束ね（章 → 公式/用語カード）。
// ※Metro は動的 import 不可なので、章ごとの JSON をここで静的 import する。
// 中身のある章だけ登録し、未整備の章は null（アプリ上「準備中」表示）。
import ch1 from '../content/formulas/ch1.json';
import ch2 from '../content/formulas/ch2.json';

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
  ch3: null,
  ch4: null,
  ch5: null,
  ch6: null,
  ch7: null,
  ch8: null,
  ch9: null,
  ch10: null,
  ch11: null,
  ch12: null,
  ch13: null,
};

export function formulaDoc(chapterId: string): FormulaDoc | null {
  return FORMULA_DOCS[chapterId] ?? null;
}
