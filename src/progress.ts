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

// 問題ID → 章ID（未使用の警告回避のため re-export ラッパ）
export function chapterOf(id: string): string | undefined {
  return QUESTION_CHAPTER[id];
}
