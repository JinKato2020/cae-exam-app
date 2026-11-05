export type EasyExplanationSection = {
  title: string;
  body: string;
};

// 問題データの型（content/questions/*.json に対応）
export type Question = {
  id: string;
  number: string;
  title?: string;
  question: string;
  choices: string[];
  answer: number; // 1始まりの正解番号
  explanation: string;
  easyExplanation?: EasyExplanationSection[]; // 回答後に開く、公式・導出・具体例を含む補足解説
  sharedQuestion?: string; // 複数設問に共通する条件。旧本体向けのquestionは別途維持する
  parts?: Question[]; // 固定IDを持つ任意数の設問。入れ子にも対応し、各末端を独立採点する
  rootQuestionId?: string; // 以下2項目はカタログ構築時に付与する表示・更新用の情報
  partLabel?: string;
  groupSize?: number; // 共通問題に属する末端設問数。限定復習の範囲をOTA更新時にも維持する
  figure?: string; // 図の表示タイミング: 'required'=回答前から表示 / 'helpful'=回答後(解説と一緒)
  figureImage?: string; // 実画像のキー（src/figures.ts の FIGURES に対応）。preFigureImage がある時は「回答後の解説図」として使う
  preFigureImage?: string; // 回答前用の図キー（答えを一切示さない配置図/概念図）。あれば回答前はこちらを表示し、回答後は figureImage を表示（前後2図）
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
