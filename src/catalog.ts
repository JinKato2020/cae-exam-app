// アプリの内容カタログ（分野 → 級 → 章 → 問題）。
// コンテンツを増やすときは、ここに1項目足して、対応する JSON を content/questions/ に置くだけ。
// ※React Native(Metro) は動的 import 不可なので、問題ファイルはここで静的に import して束ねる。
import type { Chapter, Question } from './types';

import solidCh1 from '../content/questions/math-basics.json';

export type ChapterEntry = { id: string; title: string; data: Chapter };
export type GradeEntry = { id: string; name: string; chapters: ChapterEntry[] };
export type FieldEntry = { id: string; name: string; grades: GradeEntry[] };

// 固体/熱流体/振動の3分野。まだ章が無い級・分野はアプリ上「準備中」表示。
export const CATALOG: FieldEntry[] = [
  {
    id: 'solid',
    name: '固体力学',
    grades: [
      {
        id: 'g2',
        name: '2級',
        chapters: [
          { id: 'ch1', title: '第1章 数学の基礎', data: solidCh1 as unknown as Chapter },
        ],
      },
    ],
  },
  {
    id: 'thermal',
    name: '熱流体力学',
    grades: [{ id: 'g2', name: '2級', chapters: [] }],
  },
  {
    id: 'vibration',
    name: '振動',
    grades: [{ id: 'g2', name: '2級', chapters: [] }],
  },
];

// 全問題のフラット一覧（間違い復習で ID から問題を引くのに使う）
export const ALL_QUESTIONS: Question[] = CATALOG.flatMap((f) =>
  f.grades.flatMap((g) => g.chapters.flatMap((c) => c.data.questions))
);

export function questionsByIds(ids: string[]): Question[] {
  const set = new Set(ids);
  return ALL_QUESTIONS.filter((q) => set.has(q.id));
}
