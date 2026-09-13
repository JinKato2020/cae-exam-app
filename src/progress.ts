// 学習記録を端末に保存する（次回起動しても引き継ぐ）。
// 問題ごとに「最後の正誤・日時・挑戦回数・正解回数」を持つ。
// これを章別に集計して分析タブ（得意/苦手）とタイルの色分けに使う。
import AsyncStorage from '@react-native-async-storage/async-storage';
import { CATALOG, QUESTION_CHAPTER } from './catalog';

const KEY = 'cae.progress.v1';

// 1問の記録
export type QProgress = {
  lastCorrect: boolean; // 直近の正誤
  lastTs: number; // 直近の回答日時（Date.now()）
  attempts: number; // 挑戦回数
  correctCount: number; // 正解した回数
};

export type ProgressMap = Record<string, QProgress>;

export async function loadProgress(): Promise<ProgressMap> {
  try {
    const raw = await AsyncStorage.getItem(KEY);
    if (!raw) return {};
    const obj = JSON.parse(raw);
    return obj && typeof obj === 'object' ? (obj as ProgressMap) : {};
  } catch {
    return {};
  }
}

async function save(map: ProgressMap): Promise<void> {
  try {
    await AsyncStorage.setItem(KEY, JSON.stringify(map));
  } catch {
    // 保存に失敗してもクラッシュさせない
  }
}

// 1問の回答を記録し、更新後のマップを返す（イミュータブル更新でReactに反映）。
export async function recordAnswer(
  map: ProgressMap,
  id: string,
  correct: boolean
): Promise<ProgressMap> {
  const prev = map[id];
  const next: QProgress = {
    lastCorrect: correct,
    lastTs: Date.now(),
    attempts: (prev?.attempts ?? 0) + 1,
    correctCount: (prev?.correctCount ?? 0) + (correct ? 1 : 0),
  };
  const out = { ...map, [id]: next };
  await save(out);
  return out;
}

export async function resetProgress(): Promise<ProgressMap> {
  try {
    await AsyncStorage.removeItem(KEY);
  } catch {
    /* noop */
  }
  return {};
}

// 直近で間違えている問題ID（復習対象）
export function wrongIdsFrom(map: ProgressMap): string[] {
  return Object.keys(map).filter((id) => map[id].lastCorrect === false);
}

// ---- 章別集計 ----
export type ChapterStat = {
  id: string;
  title: string;
  total: number; // 章の総問題数
  attempted: number; // 挑戦済みの問題数（distinct）
  correct: number; // 直近正解の問題数
  accuracy: number; // correct / attempted（未挑戦は0）
};

// 固体2級の章配列（分析はこの級を対象にする）
function solid2Chapters() {
  const solid = CATALOG.find((f) => f.id === 'solid');
  const g2 = solid?.grades.find((g) => g.id === 'g2');
  return g2?.chapters ?? [];
}

export function chapterStats(map: ProgressMap): ChapterStat[] {
  return solid2Chapters().map((c) => {
    const ids = c.data.questions.map((q) => q.id);
    let attempted = 0;
    let correct = 0;
    for (const id of ids) {
      const p = map[id];
      if (!p) continue;
      attempted += 1;
      if (p.lastCorrect) correct += 1;
    }
    return {
      id: c.id,
      title: c.title,
      total: ids.length,
      attempted,
      correct,
      accuracy: attempted > 0 ? correct / attempted : 0,
    };
  });
}

export type OverallStat = {
  totalQuestions: number;
  attempted: number;
  correct: number;
  accuracy: number;
};

export function overallStat(map: ProgressMap): OverallStat {
  const stats = chapterStats(map);
  const totalQuestions = stats.reduce((n, s) => n + s.total, 0);
  const attempted = stats.reduce((n, s) => n + s.attempted, 0);
  const correct = stats.reduce((n, s) => n + s.correct, 0);
  return {
    totalQuestions,
    attempted,
    correct,
    accuracy: attempted > 0 ? correct / attempted : 0,
  };
}

// ---- 分野別集計（ホームの正五角形レーダー用） ----
// 13章を「実際の問題内容から自然に分かれる」5分野に束ねる（正五角形の5頂点）。
export type FieldDef = { id: string; label: string; chapters: string[] };
export const FIELDS: FieldDef[] = [
  { id: 'A', label: '数学・数値', chapters: ['ch1', 'ch6', 'ch12'] }, // 数学/数値計算/コンピュータ
  { id: 'B', label: '材料・熱', chapters: ['ch2', 'ch3'] }, // 固体力学/熱伝導
  { id: 'C', label: 'FEM理論', chapters: ['ch4', 'ch5', 'ch7'] }, // 定式化/実践/要素
  { id: 'D', label: 'モデリング', chapters: ['ch8', 'ch9', 'ch10'] }, // モデリング/境界条件/プリポスト
  { id: 'E', label: '検証・倫理', chapters: ['ch11', 'ch13'] }, // 結果検証/技術者倫理
];

export type FieldStat = {
  id: string;
  label: string;
  chapters: string[];
  total: number; // 分野内の総問題数
  attempted: number; // 挑戦済み（distinct）
  correct: number; // 直近正解数
  accuracy: number; // correct / attempted（未挑戦は0）
};

// 章別集計を分野単位に束ね直す。
export function fieldStats(map: ProgressMap): FieldStat[] {
  const byChapter = new Map(chapterStats(map).map((s) => [s.id, s]));
  return FIELDS.map((f) => {
    let total = 0;
    let attempted = 0;
    let correct = 0;
    for (const cid of f.chapters) {
      const s = byChapter.get(cid);
      if (!s) continue;
      total += s.total;
      attempted += s.attempted;
      correct += s.correct;
    }
    return {
      id: f.id,
      label: f.label,
      chapters: f.chapters,
      total,
      attempted,
      correct,
      accuracy: attempted > 0 ? correct / attempted : 0,
    };
  });
}

// ---- 定着率（復習が効いているか） ----
// 2回以上挑戦した問題のうち、今 正解になっている割合。
export function retentionRate(map: ProgressMap): { rate: number; base: number } {
  let base = 0;
  let ok = 0;
  for (const id in map) {
    const p = map[id];
    if (p.attempts >= 2) {
      base += 1;
      if (p.lastCorrect) ok += 1;
    }
  }
  return { rate: base > 0 ? ok / base : 0, base };
}

// ---- 日別の学習ログ（連続日数・30日ヒート・推移グラフ用） ----
// 問題ごとの記録とは別に「その日 何問解いて 何問正解したか」を日単位で貯める。
const DAILY_KEY = 'cae.daily.v1';
export type DayRec = { n: number; c: number };
export type DailyMap = Record<string, DayRec>; // key = 'YYYY-MM-DD'

function ymd(d: Date): string {
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${m}-${dd}`;
}

export async function loadDaily(): Promise<DailyMap> {
  try {
    const raw = await AsyncStorage.getItem(DAILY_KEY);
    if (!raw) return {};
    const obj = JSON.parse(raw);
    return obj && typeof obj === 'object' ? (obj as DailyMap) : {};
  } catch {
    return {};
  }
}

export async function recordDaily(map: DailyMap, correct: boolean): Promise<DailyMap> {
  const k = ymd(new Date());
  const prev = map[k] ?? { n: 0, c: 0 };
  const next: DayRec = { n: prev.n + 1, c: prev.c + (correct ? 1 : 0) };
  const out = { ...map, [k]: next };
  try {
    await AsyncStorage.setItem(DAILY_KEY, JSON.stringify(out));
  } catch {
    /* noop */
  }
  return out;
}

export async function resetDaily(): Promise<DailyMap> {
  try {
    await AsyncStorage.removeItem(DAILY_KEY);
  } catch {
    /* noop */
  }
  return {};
}

export type DailyDigest = {
  streak: number; // 今日（未学習なら昨日）から遡って連続で学習した日数
  last30: { key: string; n: number; c: number }[]; // 古い→新しい 30日
  trend: number[]; // 学習した日の日次正答率(%)、最大14点（古い→新しい）
  weekDelta: number; // 直近7日と前7日の正答率差（ポイント）
};

export function dailyDigest(map: DailyMap): DailyDigest {
  const base = new Date();
  const keyOf = (offset: number) =>
    ymd(new Date(base.getFullYear(), base.getMonth(), base.getDate() - offset));

  // 連続日数：今日が未学習なら昨日から数える（学習中の連続を切らさない）
  let streak = 0;
  const start = (map[keyOf(0)]?.n ?? 0) > 0 ? 0 : 1;
  for (let i = start; i < 400; i++) {
    const r = map[keyOf(i)];
    if (r && r.n > 0) streak += 1;
    else break;
  }

  const last30: { key: string; n: number; c: number }[] = [];
  for (let i = 29; i >= 0; i--) {
    const k = keyOf(i);
    const r = map[k];
    last30.push({ key: k, n: r?.n ?? 0, c: r?.c ?? 0 });
  }

  const trend = last30
    .filter((d) => d.n > 0)
    .slice(-14)
    .map((d) => Math.round((d.c / d.n) * 100));

  const sum = (arr: { n: number; c: number }[]) =>
    arr.reduce((a, d) => ({ n: a.n + d.n, c: a.c + d.c }), { n: 0, c: 0 });
  const acc = (x: { n: number; c: number }) => (x.n > 0 ? (x.c / x.n) * 100 : 0);
  const weekDelta = Math.round(acc(sum(last30.slice(23))) - acc(sum(last30.slice(16, 23))));

  return { streak, last30, trend, weekDelta };
}

// 問題ID → 章ID（未使用の警告回避のため re-export ラッパ）
export function chapterOf(id: string): string | undefined {
  return QUESTION_CHAPTER[id];
}
