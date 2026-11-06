export type LearningFigure = {
  figureImage: string;
  caption: string; // 図のどこを読むかを文章でも伝える。読み上げにも使用する
};

export type EasyExplanationSection = {
  title: string;
  body: string;
  figures?: LearningFigure[]; // この段階の説明と一緒に読む図。順序・枚数はOTAで変更可能
};

export type StudyResponse = { choice?: number; draft?: string; revealed?: boolean; understood?: boolean };
export type StudyResponses = Record<string, StudyResponse>;

// 問題データの型（content/questions/*.json に対応）
export type Question = {
  id: string;
  number: string;
  title?: string;
  question: string;
  choices: string[];
  answer: number; // 選択式は1始まり。記述小問は0（自動採点せず自己確認する）
  explanation: string;
  easyExplanation?: EasyExplanationSection[]; // 公式・導出・具体例を含む詳解。guidedでは回答後に標準表示
  explanationMode?: 'guided' | 'standard'; // guidedは詳解を標準表示。章から継承し、設問単位で上書き可能
  answerSummary?: string; // 正解の理由を一息で読める要点。詳しい手順はeasyExplanationへ
  preFigures?: LearningFigure[]; // 共通条件・候補図。回答後も問題のそばに保持する
  studyParts?: Question[]; // 同じ公式番号の中で学ぶ小問。旧本体では親の4択を維持
  responseType?: 'choice' | 'written';
  modelAnswer?: string; // 記述式の独自表現による解答例
  answerCheckpoints?: string[]; // 記述式の自己確認点。完全一致採点はしない
  officialWrittenEvidence?: { file: string; excerpt: string }; // 公式が記述式とする根拠。生成・配信前ゲートで照合
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
    explanationMode?: 'guided' | 'standard';
    [k: string]: unknown;
  };
  questions: Question[];
};
