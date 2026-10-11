// アプリ内レビュー依頼（App Store / Google Play の公式レビューポップアップ）。
//
// ・ネイティブの正規機能（iOS: SKStoreReviewController / Android: In-App Review）を使う。
//   ダイアログの文言・見た目は OS 側が固定で、アプリからは変更できない（アプリ名だけ差し込まれる）。
//   「実際に表示するか・年に何回まで出すか」も OS が最終判断するため、確実には出せない。
// ・だからこそ「良い体験の直後」に、控えめな回数だけ依頼するのが定石。
//   契機（＝良い瞬間）は複数あってよいが、依頼どうしは 90 日以上あけ、同じ契機では一度だけにする。
//   例）解いた累計が節目に達した / 章を一つ解き終えた / 正解が続いた。
// ・「レビューしてね」というボタンには絶対に紐付けない（Apple ガイドライン違反になる）。
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as StoreReview from 'expo-store-review';

const KEY = 'cae.review.v1';

// 累計解答数（distinct）の節目。到達するたびに、その節目で最大1回だけ依頼。
const MILESTONES = [20, 80, 200];
// 依頼どうしの最短間隔（日）。OS 側の制限に加え、こちらでも間隔を空ける（全契機で共有）。
const MIN_GAP_DAYS = 90;

type ReviewState = {
  firedKeys: string[]; // 依頼済みの契機キー（'count:20' / 'done:…' / 'streak' 等）
  lastAskTs: number; // 最後に依頼した時刻（Date.now()）
};

async function load(): Promise<ReviewState> {
  try {
    const raw = await AsyncStorage.getItem(KEY);
    if (!raw) return { firedKeys: [], lastAskTs: 0 };
    const o = JSON.parse(raw);
    const keys: string[] = Array.isArray(o?.firedKeys) ? o.firedKeys.filter((k: unknown) => typeof k === 'string') : [];
    // 旧バージョン（firedMilestones:number[]）からの移行：節目を 'count:N' キーに読み替える。
    if (Array.isArray(o?.firedMilestones)) for (const m of o.firedMilestones) if (typeof m === 'number') keys.push('count:' + m);
    return { firedKeys: Array.from(new Set(keys)), lastAskTs: typeof o?.lastAskTs === 'number' ? o.lastAskTs : 0 };
  } catch {
    return { firedKeys: [], lastAskTs: 0 };
  }
}

async function save(s: ReviewState): Promise<void> {
  try {
    await AsyncStorage.setItem(KEY, JSON.stringify(s));
  } catch {
    /* 保存に失敗してもクラッシュさせない */
  }
}

// 指定の契機(key)でまだ依頼しておらず、前回の依頼から 90 日以上空いていれば、
// OS のレビュー依頼を一度だけ出す。条件を満たさなければ静かに何もしない。
async function askOnce(key: string): Promise<void> {
  try {
    if (!key) return;
    // この端末でレビュー依頼が使えるか（シミュレータや一部環境では false）。
    if (!(await StoreReview.isAvailableAsync())) return;
    if (typeof StoreReview.hasAction === 'function' && !(await StoreReview.hasAction())) return;

    const s = await load();
    if (s.firedKeys.includes(key)) return; // 同じ契機では二度と出さない
    if (Date.now() - s.lastAskTs < MIN_GAP_DAYS * 86400000) return; // 依頼どうしは 90 日以上あける（初回は必ず通る）

    await StoreReview.requestReview();

    s.firedKeys.push(key);
    s.lastAskTs = Date.now();
    await save(s);
  } catch {
    // OS がポップアップを出さない等で失敗してもクラッシュさせない。
  }
}

// 解いた累計問題数（distinct）が節目に達していれば、その節目で一度だけ依頼。
// 低い節目から順に試す（90 日ガードにより実際に出るのは最大1つ）。
export async function maybeAskForReview(answeredCount: number): Promise<void> {
  for (const m of MILESTONES) {
    if (answeredCount < m) break;
    // eslint-disable-next-line no-await-in-loop
    await askOnce('count:' + m);
  }
}

// 「章を一つ解き終えた」「正解が続いた」など“満足度が高い瞬間”に、その契機で一度だけ依頼。
// 同じ契機キーでは二度と出さず、他契機とも 90 日以上あける。
export async function maybeAskForReviewEvent(eventKey: string): Promise<void> {
  await askOnce(eventKey);
}

export async function resetReviewState(): Promise<void> {
  try {
    await AsyncStorage.removeItem(KEY);
  } catch {
    /* noop */
  }
}
