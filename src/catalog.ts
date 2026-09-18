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

// 固体1級（新トラック）。完成した章から順に有効化する。
import s1ch1 from '../content/questions/solid1-01-nonlinear-stress-strain.json';
import s1ch2 from '../content/questions/solid1-02-material-nonlinear.json';
import s1ch3 from '../content/questions/solid1-03-geometric-nonlinear.json';
import s1ch4 from '../content/questions/solid1-04-contact-nonlinear.json';
import s1ch5 from '../content/questions/solid1-05-fracture-fatigue.json';
import s1ch6 from '../content/questions/solid1-06-dynamic-analysis.json';
import s1ch7 from '../content/questions/solid1-07-heat-transfer.json';
import s1ch8 from '../content/questions/solid1-08-element-technology.json';
import s1ch9 from '../content/questions/solid1-09-numerical-analysis.json';
import s1ch10 from '../content/questions/solid1-10-analysis-verification.json';
import s1ch11 from '../content/questions/solid1-11-modeling-techniques.json';

// 熱流体力学 2級
import t2ch1 from '../content/questions/thermal2-01-math-basics.json';
import t2ch2 from '../content/questions/thermal2-02-fluid-basics.json';
import t2ch3 from '../content/questions/thermal2-03-thermo-heat.json';
import t2ch4 from '../content/questions/thermal2-04-numerical-methods.json';
import t2ch5 from '../content/questions/thermal2-05-grid-generation.json';
import t2ch6 from '../content/questions/thermal2-06-turbulence.json';
import t2ch7 from '../content/questions/thermal2-07-boundary-conditions.json';
import t2ch8 from '../content/questions/thermal2-08-post-processing.json';

// ready: 章が使えるか（省略時は true＝使える）。準備中の章は false。
// formulaId: 公式・用語の参照キー（FORMULA_DOCS のキー。省略時は id を使う）。
//   ※2級と1級で章 id が同じ('ch8')でも公式は別物なので、1級側は 's1ch8' を指す。
export type ChapterEntry = { id: string; title: string; data: Chapter; ready?: boolean; formulaId?: string };
export type GradeEntry = { id: string; name: string; chapters: ChapterEntry[] };
export type FieldEntry = { id: string; name: string; grades: GradeEntry[] };

// 1級の準備中プレースホルダ章（問題ゼロ・タップ不可表示用）。
const s1stub = (n: number, title: string): ChapterEntry => ({
  id: `ch${n}`,
  title: `第${n}章 ${title}`,
  data: { meta: { grade: '固体力学 1級', category: title, chapter: n, count: 0 }, questions: [] },
  ready: false,
});

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
      {
        id: 'g1',
        name: '1級',
        chapters: [
          { id: 'ch1', title: '第1章 非線形解析における応力とひずみ', data: s1ch1 as unknown as Chapter, ready: true, formulaId: 's1ch1' },
          { id: 'ch2', title: '第2章 材料非線形（弾塑性・クリープ・粘弾性）', data: s1ch2 as unknown as Chapter, ready: true, formulaId: 's1ch2' },
          { id: 'ch3', title: '第3章 幾何学的非線形', data: s1ch3 as unknown as Chapter, ready: true, formulaId: 's1ch3' },
          { id: 'ch4', title: '第4章 境界非線形（接触）', data: s1ch4 as unknown as Chapter, ready: true, formulaId: 's1ch4' },
          { id: 'ch5', title: '第5章 破壊力学・疲労解析', data: s1ch5 as unknown as Chapter, ready: true, formulaId: 's1ch5' },
          { id: 'ch6', title: '第6章 動的解析', data: s1ch6 as unknown as Chapter, ready: true, formulaId: 's1ch6' },
          { id: 'ch7', title: '第7章 伝熱解析', data: s1ch7 as unknown as Chapter, ready: true, formulaId: 's1ch7' },
          { id: 'ch8', title: '第8章 要素テクノロジー', data: s1ch8 as unknown as Chapter, ready: true, formulaId: 's1ch8' },
          { id: 'ch9', title: '第9章 数値解析法', data: s1ch9 as unknown as Chapter, ready: true, formulaId: 's1ch9' },
          { id: 'ch10', title: '第10章 解析の検証', data: s1ch10 as unknown as Chapter, ready: true, formulaId: 's1ch10' },
          { id: 'ch11', title: '第11章 各種モデリング技術', data: s1ch11 as unknown as Chapter, ready: true, formulaId: 's1ch11' },
        ],
      },
    ],
  },
  {
    id: 'thermal',
    name: '熱流体力学',
    grades: [
      {
        id: 'g2',
        name: '2級',
        chapters: [
          { id: 'ch1', title: '第1章 計算力学のための数学の基礎', data: t2ch1 as unknown as Chapter, ready: true, formulaId: 't2ch1' },
          { id: 'ch2', title: '第2章 流体力学の基礎', data: t2ch2 as unknown as Chapter, ready: true, formulaId: 't2ch2' },
          { id: 'ch3', title: '第3章 熱力学・伝熱学の基礎', data: t2ch3 as unknown as Chapter, ready: true, formulaId: 't2ch3' },
          { id: 'ch4', title: '第4章 数値計算法', data: t2ch4 as unknown as Chapter, ready: true, formulaId: 't2ch4' },
          { id: 'ch5', title: '第5章 格子生成法', data: t2ch5 as unknown as Chapter, ready: true, formulaId: 't2ch5' },
          { id: 'ch6', title: '第6章 乱流モデル', data: t2ch6 as unknown as Chapter, ready: true, formulaId: 't2ch6' },
          { id: 'ch7', title: '第7章 境界条件', data: t2ch7 as unknown as Chapter, ready: true, formulaId: 't2ch7' },
          { id: 'ch8', title: '第8章 ポスト処理の基礎', data: t2ch8 as unknown as Chapter, ready: true, formulaId: 't2ch8' },
        ],
      },
    ],
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

// 問題ID → 公式ドキュメントID（関連用語・公式リンクの解決に使う。
//   章 id は2級/1級で衝突する('ch1'等)ので、必ず formulaId(あれば)を優先して引く）
export const QUESTION_FORMULA_ID: Record<string, string> = (() => {
  const m: Record<string, string> = {};
  for (const f of CATALOG) {
    for (const g of f.grades) {
      for (const c of g.chapters) {
        for (const q of c.data.questions) m[q.id] = c.formulaId ?? c.id;
      }
    }
  }
  return m;
})();
