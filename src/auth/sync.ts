// 学習記録のクラウド同期（Firestore）。
// 保存先は 1ユーザー1ドキュメント: users/{uid} = { progress, daily, clientUpdatedAt, updatedAt }。
// データの取りこぼしを防ぐため「まるごと上書き（LWW）」ではなく、
// 問題ごと・日ごとに新しい方を残す「レコード単位マージ」を行う。
import { doc, getDoc, setDoc, deleteDoc, serverTimestamp } from 'firebase/firestore';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { db } from '../config/firebase';
import type { ProgressMap, QProgress } from '../progress';

const PROGRESS_KEY = 'cae.progress.v1';
const DAILY_KEY = 'cae.daily.v1';

type DayRec = { n: number; c: number };
type DailyMap = Record<string, DayRec>;

function safeParse<T>(raw: string | null): T | null {
  if (!raw) return null;
  try {
    const o = JSON.parse(raw);
    return o && typeof o === 'object' ? (o as T) : null;
  } catch {
    return null;
  }
}

async function readLocal(): Promise<{ progress: ProgressMap; daily: DailyMap }> {
  const [p, d] = await Promise.all([
    AsyncStorage.getItem(PROGRESS_KEY),
    AsyncStorage.getItem(DAILY_KEY),
  ]);
  return {
    progress: safeParse<ProgressMap>(p) ?? {},
    daily: safeParse<DailyMap>(d) ?? {},
  };
}

async function writeLocal(progress: ProgressMap, daily: DailyMap): Promise<void> {
  await Promise.all([
    AsyncStorage.setItem(PROGRESS_KEY, JSON.stringify(progress)),
    AsyncStorage.setItem(DAILY_KEY, JSON.stringify(daily)),
  ]);
}

// 問題ごと：直近回答が新しい方（lastTs 大）を採用。同時刻なら挑戦回数が多い方。
function mergeProgress(a: ProgressMap, b: ProgressMap): ProgressMap {
  const out: ProgressMap = { ...a };
  for (const id in b) {
    const x: QProgress | undefined = a[id];
    const y = b[id];
    if (!x || y.lastTs > x.lastTs || (y.lastTs === x.lastTs && y.attempts > x.attempts)) {
      out[id] = y;
    }
  }
  return out;
}

// 日ごと：その日の解答数が多い方を残す（両端末で解いた日を取りこぼさない）。
function mergeDaily(a: DailyMap, b: DailyMap): DailyMap {
  const out: DailyMap = { ...a };
  for (const k in b) {
    const x = a[k];
    const y = b[k];
    if (!x || y.n > x.n) out[k] = y;
  }
  return out;
}

async function pushDoc(uid: string, progress: ProgressMap, daily: DailyMap): Promise<void> {
  await setDoc(
    doc(db, 'users', uid),
    { progress, daily, clientUpdatedAt: Date.now(), updatedAt: serverTimestamp() },
    { merge: true }
  );
}

// ログイン直後：クラウドと端末を統合し、両方を最新化。統合後の progress を返す（画面反映用）。
export async function syncOnLogin(uid: string): Promise<ProgressMap> {
  const local = await readLocal();
  let remote: { progress: ProgressMap; daily: DailyMap } = { progress: {}, daily: {} };
  try {
    const snap = await getDoc(doc(db, 'users', uid));
    if (snap.exists()) {
      const d: any = snap.data();
      remote = { progress: d.progress ?? {}, daily: d.daily ?? {} };
    }
  } catch {
    // オフライン等はクラウド分を空扱いにして端末データで続行（消さない）。
  }
  const progress = mergeProgress(local.progress, remote.progress);
  const daily = mergeDaily(local.daily, remote.daily);
  await writeLocal(progress, daily);
  try {
    await pushDoc(uid, progress, daily);
  } catch {
    // 送信失敗は無視（次の schedulePush で再送）。
  }
  return progress;
}

// 回答のたびに呼ぶ想定。短時間の連打をまとめて送る（デバウンス）。ログイン中のみ動作。
let timer: ReturnType<typeof setTimeout> | null = null;
export function schedulePush(uid: string | undefined | null): void {
  if (!uid) return;
  if (timer) clearTimeout(timer);
  timer = setTimeout(async () => {
    timer = null;
    try {
      const local = await readLocal();
      await pushDoc(uid, local.progress, local.daily);
    } catch {
      // 通信失敗は無視（次回の保存で再送される）。
    }
  }, 1500);
}

// 端末の最新を今すぐ確実に送る（ログアウト直前に使う）。
export async function pushNow(uid: string): Promise<void> {
  const local = await readLocal();
  await pushDoc(uid, local.progress, local.daily);
}

// アカウント削除に伴い、クラウド上のこのユーザーのデータを消す。
export async function deleteCloudData(uid: string): Promise<void> {
  try {
    await deleteDoc(doc(db, 'users', uid));
  } catch {
    // 失敗しても致命的ではない（アカウント自体の削除が主）。
  }
}
