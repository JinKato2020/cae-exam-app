// 公式・用語コンテンツの解決。【データ駆動】
// 章立て(content/catalog.json)が持つ formulaId→公式JSONキー(FORMULA_KEY_BY_ID)を使い、
// getContent で「OTA版→同梱版」の順に公式ドキュメントを引く。これで公式・用語の修正もOTAで反映できる。
import { getContent } from './data/contentStore';
import { FORMULA_KEY_BY_ID } from './catalog';

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

/** 章ID/公式ID（catalog の formulaId。既定は章 id）→ 公式ドキュメント。無ければ null（準備中）。 */
export function formulaDoc(chapterId: string): FormulaDoc | null {
  const key = FORMULA_KEY_BY_ID[chapterId];
  if (!key) return null;
  return getContent<FormulaDoc>(key);
}
