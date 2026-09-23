// アプリ内レビュー依頼（App Store / Google Play の公式レビューポップアップ）。
//
// ・ネイティブの正規機能（iOS: SKStoreReviewController / Android: In-App Review）を使う。
//   OS 側が「実際に表示するか・年に何回まで出すか」を最終判断するため、
//   アプリからこちらの都合で確実に出すことはできない（Apple / Google の仕様）。
// ・だからこそ「良い体験の直後」に、控えめな回数だけ依頼するのが定石。
//   ここでは “解いた累計問題数が節目に達したとき” に一度だけ依頼する。
// ・「レビューしてね」というボタンには絶対に紐付けない（Apple ガイドライン違反になる）。
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as StoreReview from 'expo-store-review';

const KEY = 'cae.review.v1';

// 依頼を出す「解いた累計問題数（distinct）」の節目。到達するたびに最大1回だけ依頼。
const MILESTONES = [20, 80, 200];
// 依頼どうしの最短間隔（日）。OS 側の制限に加え、こちらでも間隔を空ける。
const MIN_GAP_DAYS = 90;

type ReviewState = {
  firedMilestones: number[]; // 既に依頼を出した節目
  lastAskTs: number; // 最後に依頼した時刻（Date.now()）
};

async function load(): Promise<ReviewState> {
  try {
    const raw = await AsyncStorage.getItem(KEY);
    if (!raw) return { firedMilestones: [], lastAskTs: 0 };
    const o = JSON.parse(raw);
    return {
      firedMilestones: Array.isArray(o?.firedMilestones) ? o.firedMilestones : [],
      lastAskTs: typeof o?.lastAskTs === 'number' ? o.lastAskTs : 0,
    };
  } catch {
    return { firedMilestones: [], lastAskTs: 0 };
  }
}

async function save(s: ReviewState): Promise<void> {
  try {
    await AsyncStorage.setItem(KEY, JSON.stringify(s));
  } catch {
    /* 保存に失敗してもクラッシュさせない */
  }
}

// 解いた累計問題数（distinct）を渡すと、条件を満たせばレビュー依頼を出す。
// 条件を満たさない場合は静かに何もしない（学習の邪魔をしない）。
export async function maybeAskForReview(answeredCount: number): Promise<void> {
  try {
    // この端末でレビュー依頼が使えるか（シミュレータや一部環境では false）。
    if (!(await StoreReview.isAvailableAsync())) return;
    if (typeof StoreReview.hasAction === 'function' && !(await StoreReview.hasAction())) return;

    const s = await load();
    // まだ依頼していない節目のうち、到達済みのもの。
    const due = MILESTONES.filter((m) => answeredCount >= m && !s.firedMilestones.includes(m));
    if (due.length === 0) return;
    // 前回の依頼から十分間隔を空ける（初回は lastAskTs=0 なので必ず通る）。
    if (Date.now() - s.lastAskTs < MIN_GAP_DAYS * 86400000) return;

    await StoreReview.requestReview();

    // 到達済みの節目は「依頼済み」の印を付ける（同じ節目で二度と依頼しない）。
    const fired = Array.from(new Set([...s.firedMilestones, ...due]));
    await save({ firedMilestones: fired, lastAskTs: Date.now() });
  } catch {
    // OS がポップアップを出さない等で失敗してもクラッシュさせない。
  }
}

export async function resetReviewState(): Promise<void> {
  try {
    await AsyncStorage.removeItem(KEY);
  } catch {
    /* noop */
  }
}
