// アプリの内容カタログ（分野 → 級 → 章 → 問題）。【データ駆動】
// 章立ては content/catalog.json（＝OTAで差し替え可能なデータ）から構築する。各章の問題データは
// getContent(章のcontentキー) で「OTA版→同梱版」の順に解決する。これで問題・解説の修正も、
// 新しい分野・章の追加も、棚(R2)にデータを置くだけでビルド無しに反映できる（[[cae-content-ota-design-inflight]]）。
// ※起動時に initContent()→rebuildCatalog() を呼ぶ前提。呼ばれなくても同梱データで従来どおり動く。
import type { Chapter, Question } from './types';
import { getContent } from './data/contentStore';

export type ChapterEntry = { id: string; title: string; data: Chapter; ready?: boolean; formulaId?: string };
export type GradeEntry = { id: string; name: string; chapters: ChapterEntry[] };
export type FieldEntry = { id: string; name: string; grades: GradeEntry[] };

// content/catalog.json のスキーマ。
type CatChapter = { id: string; title: string; content?: string; formula?: string; formulaId?: string; ready?: boolean };
type CatGrade = { id: string; name: string; chapters: CatChapter[] };
type CatField = { id: string; name: string; grades: CatGrade[] };
type CatalogFile = { schema?: number; fields: CatField[] };

const emptyChapter = (title: string): Chapter =>
  ({ meta: { grade: '', category: title, chapter: 0, count: 0 }, questions: [] });

function buildCatalog(): FieldEntry[] {
  const cat = getContent<CatalogFile>('content/catalog.json');
  if (!cat || !Array.isArray(cat.fields)) return [];
  return cat.fields.map((f) => ({
    id: f.id,
    name: f.name,
    grades: (f.grades ?? []).map((g) => ({
      id: g.id,
      name: g.name,
      chapters: (g.chapters ?? []).map((c) => {
        const data = (c.content ? getContent<Chapter>(c.content) : null) ?? emptyChapter(c.title);
        return { id: c.id, title: c.title, data, ready: c.ready ?? true, formulaId: c.formulaId };
      }),
    })),
  }));
}

// formulaId → 公式JSONキー（formulas.ts の formulaDoc が引く）。
function buildFormulaKeyById(): Record<string, string> {
  const cat = getContent<CatalogFile>('content/catalog.json');
  const m: Record<string, string> = {};
  if (cat?.fields) {
    for (const f of cat.fields) for (const g of f.grades ?? []) for (const c of g.chapters ?? []) {
      if (c.formula) m[c.formulaId ?? c.id] = c.formula;
    }
  }
  return m;
}

function deriveAll(): Question[] {
  return CATALOG.flatMap((f) => f.grades.flatMap((g) => g.chapters.flatMap((c) => c.data.questions)));
}
function deriveChapterMap(): Record<string, string> {
  const m: Record<string, string> = {};
  for (const f of CATALOG) for (const g of f.grades) for (const c of g.chapters) for (const q of c.data.questions) m[q.id] = c.id;
  return m;
}
function deriveFormulaIdMap(): Record<string, string> {
  const m: Record<string, string> = {};
  for (const f of CATALOG) for (const g of f.grades) for (const c of g.chapters) for (const q of c.data.questions) m[q.id] = c.formulaId ?? c.id;
  return m;
}

// ホーム「用語問題／計算・数値問題」の専用セット（章とは別建て・分野×級ごと）。
// content/quiz/<kind>-<分野>-<級数字>.json（例 content/quiz/term-solid-2.json）を getContent で解決＝OTAで差し替え可。
// カタログの章に属さない＝isLocked で無料タスター扱い（proState.ts）。呼出しの都度読むので OTA 反映も即時。
export function quizList(kind: 'term' | 'calc', fieldId: string, gradeId: string): Question[] {
  const g = gradeId === 'g1' ? '1' : '2';
  const doc = getContent<{ questions?: Question[] }>(`content/quiz/${kind}-${fieldId}-${g}.json`);
  return doc?.questions ?? [];
}

// live binding（export let）＝ rebuildCatalog で作り直すと、呼出し時に読む消費側へ自動反映される。
export let CATALOG: FieldEntry[] = buildCatalog();
export let FORMULA_KEY_BY_ID: Record<string, string> = buildFormulaKeyById();
export let ALL_QUESTIONS: Question[] = deriveAll();
export let QUESTION_CHAPTER: Record<string, string> = deriveChapterMap();
export let QUESTION_FORMULA_ID: Record<string, string> = deriveFormulaIdMap();

/** OTAの差し替えを反映してカタログ一式を作り直す（initContent から呼ぶ）。 */
export function rebuildCatalog(): void {
  CATALOG = buildCatalog();
  FORMULA_KEY_BY_ID = buildFormulaKeyById();
  ALL_QUESTIONS = deriveAll();
  QUESTION_CHAPTER = deriveChapterMap();
  QUESTION_FORMULA_ID = deriveFormulaIdMap();
}

export function questionsByIds(ids: string[]): Question[] {
  const set = new Set(ids);
  return ALL_QUESTIONS.filter((q) => set.has(q.id));
}
