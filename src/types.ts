// 問題データの型（content/questions/*.json に対応）
export type Question = {
  id: string;
  number: string;
  title?: string;
  question: string;
  choices: string[];
  answer: number; // 1始まりの正解番号
  explanation: string;
  figure?: string; // 等幅フォントで表示する文字図（任意）
  topic?: string;
  type?: string;
  difficulty?: number;
  hasMath?: boolean;
  origin?: string;
  reviewed?: boolean;
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

// 1問ごとの回答記録
export type AnswerRecord = {
  id: string;
  correct: boolean;
};
