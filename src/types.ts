// 問題データの型（content/questions/*.json に対応）
export type Question = {
  id: string;
  number: string;
  title?: string;
  question: string;
  choices: string[];
  answer: number; // 1始まりの正解番号
  explanation: string;
  figure?: string; // 等幅フォントで表示する文字図（任意・旧方式）
  figureImage?: string; // 実画像のキー（src/figures.ts の FIGURES に対応）
  topic?: string;
  type?: string;
  difficulty?: number;
  hasMath?: boolean;
  origin?: string;
  reviewed?: boolean;
  officialRef?: string; // 対応する公式標準問題の番号（例 "問5-3"）。§1.6の1:1対応。番号=参照のみ
  role?: 'primary' | 'branch'; // primary=公式と1:1の本体 / branch=補足(枝問)
  relatedFormulas?: string[]; // この問題に関連する公式・用語（同章 formulas の item.id）。解答画面からカードへリンク
};

export type Chapter = {
  meta: {
    grade: string;
    category: string;
    chapter: number;
    count: number;
    [k: string]: unknown;
  };
  questions: Question[];
};
