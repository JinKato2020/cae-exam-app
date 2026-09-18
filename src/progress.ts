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

// 固体分野の指定した級の章配列（分析はこの級を対象にする。既定は2級）。
export type GradeId = 'g1' | 'g2';
function gradeChapters(gradeId: GradeId) {
  const solid = CATALOG.find((f) => f.id === 'solid');
  const g = solid?.grades.find((gg) => gg.id === gradeId);
  return g?.chapters ?? [];
}

export function chapterStats(map: ProgressMap, gradeId: GradeId = 'g2'): ChapterStat[] {
  return gradeChapters(gradeId).map((c) => {
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

export function overallStat(map: ProgressMap, gradeId: GradeId = 'g2'): OverallStat {
  const stats = chapterStats(map, gradeId);
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
// 2級（全13章）を5分野に束ねる。
export const FIELDS_G2: FieldDef[] = [
  { id: 'A', label: '数学・数値', chapters: ['ch1', 'ch6', 'ch12'] }, // 数学/数値計算/コンピュータ
  { id: 'B', label: '材料・熱', chapters: ['ch2', 'ch3'] }, // 固体力学/熱伝導
  { id: 'C', label: 'FEM理論', chapters: ['ch4', 'ch5', 'ch7'] }, // 定式化/実践/要素
  { id: 'D', label: 'モデリング', chapters: ['ch8', 'ch9', 'ch10'] }, // モデリング/境界条件/プリポスト
  { id: 'E', label: '検証・倫理', chapters: ['ch11', 'ch13'] }, // 結果検証/技術者倫理
];
// 1級（全11章）を5分野に束ねる。
export const FIELDS_G1: FieldDef[] = [
  { id: 'A', label: '非線形', chapters: ['ch1', 'ch3'] }, // 応力ひずみ/幾何学的非線形
  { id: 'B', label: '材料・破壊', chapters: ['ch2', 'ch5'] }, // 材料非線形/破壊・疲労
  { id: 'C', label: '接触・動的', chapters: ['ch4', 'ch6'] }, // 境界非線形(接触)/動的
  { id: 'D', label: '伝熱・要素', chapters: ['ch7', 'ch8'] }, // 伝熱/要素テクノロジー
  { id: 'E', label: '数値・検証', chapters: ['ch9', 'ch10', 'ch11'] }, // 数値解析/検証/モデリング
];
export function fieldsOf(gradeId: GradeId): FieldDef[] {
  return gradeId === 'g1' ? FIELDS_G1 : FIELDS_G2;
}
// 後方互換（既定=2級）
export const FIELDS = FIELDS_G2;

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
export function fieldStats(map: ProgressMap, gradeId: GradeId = 'g2'): FieldStat[] {
  const byChapter = new Map(chapterStats(map, gradeId).map((s) => [s.id, s]));
  return fieldsOf(gradeId).map((f) => {
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

// ---- 分野別スナップショット（ホームのレーダー「1週前比の成長」表示用） ----
// 分野ごとの正答率を1日1回・級ごとに端末へ貯める。
// これがあると「今の五角形」と「約1週間前の五角形」を比べて伸びを出せる。
const FSNAP_KEY = 'cae.fieldsnap.v1';
export type FieldSnap = {
  ts: number; // 記録した時刻
  grade: GradeId;
  acc: Record<string, number>; // 分野id → 正答率(0..1)
  att: Record<string, number>; // 分野id → 挑戦数
};
export type FieldSnapStore = FieldSnap[];

export async function loadFieldSnaps(): Promise<FieldSnapStore> {
  try {
    const raw = await AsyncStorage.getItem(FSNAP_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? (arr as FieldSnapStore) : [];
  } catch {
    return [];
  }
}

// 現在の分野正答率を記録する。同じ級の当日分が既にあれば何もしない（1日1回）。
// 40日より古いスナップショットは間引く。
export async function snapshotFields(map: ProgressMap, gradeId: GradeId): Promise<void> {
  try {
    const store = await loadFieldSnaps();
    const today = ymd(new Date());
    if (store.some((s) => s.grade === gradeId && ymd(new Date(s.ts)) === today)) return;
    const fs = fieldStats(map, gradeId);
    // 全分野が未挑戦なら記録しない（空の基準を作らない）。
    if (!fs.some((f) => f.attempted > 0)) return;
    const acc: Record<string, number> = {};
    const att: Record<string, number> = {};
    for (const f of fs) {
      acc[f.id] = f.accuracy;
      att[f.id] = f.attempted;
    }
    const cutoff = Date.now() - 40 * 86400000;
    const next = [...store.filter((s) => s.ts >= cutoff), { ts: Date.now(), grade: gradeId, acc, att }];
    await AsyncStorage.setItem(FSNAP_KEY, JSON.stringify(next));
  } catch {
    /* 保存失敗はクラッシュさせない */
  }
}

export async function resetFieldSnaps(): Promise<void> {
  try {
    await AsyncStorage.removeItem(FSNAP_KEY);
  } catch {
    /* noop */
  }
}

export type FieldGrowth = Record<string, number | null>; // 分野id → 変化ポイント(現在-約1週前)。基準無しは null。
export type FieldCompare = {
  growth: FieldGrowth;
  baseAcc: Record<string, number> | null; // 約1週前の分野正答率（レーダーの薄い比較図用）
  baseTs: number | null;
};

// 「7日以上前で最も新しい」スナップショットを基準にして、分野ごとの伸び(pt)を出す。
export function fieldCompareFrom(
  store: FieldSnapStore,
  current: FieldStat[],
  gradeId: GradeId
): FieldCompare {
  const cutoff = Date.now() - 7 * 86400000;
  const base = store
    .filter((s) => s.grade === gradeId && s.ts <= cutoff)
    .sort((a, b) => b.ts - a.ts)[0];
  const growth: FieldGrowth = {};
  for (const f of current) {
    if (!base || base.acc[f.id] == null || (base.att?.[f.id] ?? 0) === 0) {
      growth[f.id] = null; // 1週前にその分野の記録が無ければ比較しない
      continue;
    }
    growth[f.id] = Math.round(f.accuracy * 100) - Math.round(base.acc[f.id] * 100);
  }
  return { growth, baseAcc: base ? base.acc : null, baseTs: base ? base.ts : null };
}

// 問題ID → 章ID（未使用の警告回避のため re-export ラッパ）
export function chapterOf(id: string): string | undefined {
  return QUESTION_CHAPTER[id];
}

// ---- 章別スナップショット（ホームの章別レーダー「今週/先週/先月」比較用）----
// 章ごとの正答率を1日1回・級ごとに端末へ貯める。今の形・約1週前・約1か月前の3本を重ねて成長を見せる。
const CSNAP_KEY = 'cae.chaptersnap.v1';
export type ChapterSnap = {
  ts: number;
  grade: GradeId;
  acc: Record<string, number>; // 章id → 正答率(0..1)
  att: Record<string, number>; // 章id → 挑戦数
};
export type ChapterSnapStore = ChapterSnap[];

export async function loadChapterSnaps(): Promise<ChapterSnapStore> {
  try {
    const raw = await AsyncStorage.getItem(CSNAP_KEY);
    if (!raw) return [];
    const a = JSON.parse(raw);
    return Array.isArray(a) ? (a as ChapterSnapStore) : [];
  } catch {
    return [];
  }
}

// 現在の章別正答率を記録（同じ級の当日分があれば何もしない＝1日1回）。60日より古いものは間引く。
export async function snapshotChapters(map: ProgressMap, gradeId: GradeId): Promise<void> {
  try {
    const store = await loadChapterSnaps();
    const today = ymd(new Date());
    if (store.some((s) => s.grade === gradeId && ymd(new Date(s.ts)) === today)) return;
    const cs = chapterStats(map, gradeId);
    if (!cs.some((c) => c.attempted > 0)) return; // 全章未挑戦なら記録しない
    const acc: Record<string, number> = {};
    const att: Record<string, number> = {};
    for (const c of cs) {
      acc[c.id] = c.accuracy;
      att[c.id] = c.attempted;
    }
    const cutoff = Date.now() - 60 * 86400000;
    const next = [...store.filter((s) => s.ts >= cutoff), { ts: Date.now(), grade: gradeId, acc, att }];
    await AsyncStorage.setItem(CSNAP_KEY, JSON.stringify(next));
  } catch {
    /* 保存失敗はクラッシュさせない */
  }
}

// 指定日数以上前で最も新しいスナップの章別正答率を返す（無ければ null）。先週=7日, 先月=28日 で使う。
export function chapterSeriesAt(
  store: ChapterSnapStore,
  gradeId: GradeId,
  minAgeDays: number
): Record<string, number> | null {
  const cutoff = Date.now() - minAgeDays * 86400000;
  const snap = store
    .filter((s) => s.grade === gradeId && s.ts <= cutoff)
    .sort((a, b) => b.ts - a.ts)[0];
  return snap ? snap.acc : null;
}
