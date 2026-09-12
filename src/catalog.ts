// アプリの内容カタログ（分野 → 級 → 章 → 問題）。
// コンテンツを増やすときは、ここに1項目足して、対応する JSON を content/questions/ に置くだけ。
// ※React Native(Metro) は動的 import 不可なので、問題ファイルはここで静的に import して束ねる。
import type { Chapter, Question } from './types';

import ch1 from '../content/questions/math-basics.json';
import ch2 from '../content/questions/solid-basics.json';
import ch3 from '../content/questions/heat-basics.json';
import ch4 from '../content/questions/fem-basics.json';
import ch5 from '../content/questions/fem-practice.json';
import ch6 from '../content/questions/numerical-basics.json';
import ch7 from '../content/questions/element-tech.json';
import ch8 from '../content/questions/modeling-basics.json';
import ch9 from '../content/questions/boundary-conditions.json';
import ch10 from '../content/questions/prepost-basics.json';
import ch11 from '../content/questions/verification-basics.json';
import ch12 from '../content/questions/computer-basics.json';
import ch13 from '../content/questions/ethics.json';

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
          { id: 'ch1', title: '第1章 数学の基礎', data: ch1 as unknown as Chapter },
          { id: 'ch2', title: '第2章 固体力学の基礎', data: ch2 as unknown as Chapter },
          { id: 'ch3', title: '第3章 熱伝導の基礎', data: ch3 as unknown as Chapter },
          { id: 'ch4', title: '第4章 有限要素法の定式化', data: ch4 as unknown as Chapter },
          { id: 'ch5', title: '第5章 有限要素法の実践', data: ch5 as unknown as Chapter },
          { id: 'ch6', title: '第6章 数値計算法の基礎', data: ch6 as unknown as Chapter },
          { id: 'ch7', title: '第7章 要素テクノロジーの基礎', data: ch7 as unknown as Chapter },
          { id: 'ch8', title: '第8章 モデリングの基礎', data: ch8 as unknown as Chapter },
          { id: 'ch9', title: '第9章 境界条件の使い方の基礎', data: ch9 as unknown as Chapter },
          { id: 'ch10', title: '第10章 プリポスト処理の基礎', data: ch10 as unknown as Chapter },
          { id: 'ch11', title: '第11章 結果の検証の基礎', data: ch11 as unknown as Chapter },
          { id: 'ch12', title: '第12章 コンピューターの基礎', data: ch12 as unknown as Chapter },
          { id: 'ch13', title: '第13章 計算力学技術者倫理', data: ch13 as unknown as Chapter },
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

// 問題ID → 章ID（章別分析・タイル色分けで使う）
export const QUESTION_CHAPTER: Record<string, string> = (() => {
  const m: Record<string, string> = {};
  for (const f of CATALOG) {
    for (const g of f.grades) {
      for (const c of g.chapters) {
        for (const q of c.data.questions) m[q.id] = c.id;
      }
    }
  }
  return m;
})();
