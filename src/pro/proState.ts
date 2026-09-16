// Pro（買い切り）の状態管理と「無料で見せる範囲」の判定をまとめた場所。
// 方針（ユーザー確定 2026-09-16）:
//   ・買い切りは「分野×級」ごと（例：固体力学2級／固体力学1級を別々に購入）。買った級だけ解除。
//   ・各章の先頭5問は無料。6問目以降は「正解・解説・図」がロック（問題文と選択肢は見える）。
//   ・公式・用語ページは全問無料（このファイルはゲートしない）。
//   ・非消耗（一度購入で永久）。iOSのみ。
// 通信が切れても権利が剥がれないよう、購入状態は端末に保存した値を信じる（正本はストアのレシート）。
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Question } from '../types';
import { CATALOG } from '../catalog';

/** 各章、無料で全部見られる先頭の問題数。 */
export const FREE_PER_CHAPTER = 5;

/** 1つの買い切り単位（分野×級）。key は RevenueCat の Entitlement / Package 識別子と一致させる。 */
export interface EntInfo {
  key: string; // 例 'solid_g2'（= RevenueCatのEntitlement ID / Package ID）
  title: string; // 例 '固体力学 2級'（購入画面の見出し）
  fieldId: string; // 例 'solid'
  gradeId: string; // 例 'g2'
}

/** 分野ID・級ID から買い切りの識別子を作る（ここを唯一の綴りの正とする）。 */
export function entKey(fieldId: string, gradeId: string): string {
  return `${fieldId}_${gradeId}`;
}

// カタログから「課金対象になる分野×級」の一覧を作る。問題が1問も無い級（準備中）は課金対象に含めない。
export const ENTITLEMENTS: EntInfo[] = (() => {
  const list: EntInfo[] = [];
  for (const f of CATALOG) {
    for (const g of f.grades) {
      const hasQ = g.chapters.some((c) => (c.data.questions?.length ?? 0) > 0);
      if (!hasQ) continue;
      list.push({ key: entKey(f.id, g.id), title: `${f.name} ${g.name}`, fieldId: f.id, gradeId: g.id });
    }
  }
  return list;
})();

// 問題ID → その問題が属する買い切りkey。ロック判定と「どの級のPaywallを開くか」に使う。
const ENT_OF_QID: Map<string, string> = (() => {
  const m = new Map<string, string>();
  for (const f of CATALOG) {
    for (const g of f.grades) {
      const k = entKey(f.id, g.id);
      for (const c of g.chapters) for (const q of c.data.questions ?? []) m.set(q.id, k);
    }
  }
  return m;
})();

// 章ごとに先頭 FREE_PER_CHAPTER 問の問題IDを集めた「無料集合」。
// 章/復習など出題順に関係なく、問題そのものが無料かどうかで判定できる（＝どの入口でも一貫）。
export const FREE_QUESTION_IDS: Set<string> = (() => {
  const s = new Set<string>();
  for (const f of CATALOG) {
    for (const g of f.grades) {
      for (const c of g.chapters) {
        c.data.questions.slice(0, FREE_PER_CHAPTER).forEach((q) => s.add(q.id));
      }
    }
  }
  return s;
})();

/** key から表示情報を引く。 */
export function entInfoByKey(key: string): EntInfo | null {
  return ENTITLEMENTS.find((e) => e.key === key) ?? null;
}

/** ある問題が属する買い切り（分野×級）の情報。無料集合の問題でも「属する級」を返す（Paywallの見出し用）。 */
export function entOfQuestion(qid: string): EntInfo | null {
  const k = ENT_OF_QID.get(qid);
  return k ? entInfoByKey(k) : null;
}

// ---- 端末に保存する購入状態 ----
const K_OWNED = 'cae.pro.owned'; // 購入済みkeyの配列(JSON)。ストア同期で得た「今持っている権利」のキャッシュ
const K_DEVPRO = 'cae.pro.devpro'; // 開発用の全解除（審査・テスト用。実購入なしで解除画面を確認）
const K_LEGACY = 'cae.pro.active'; // 旧: 単一Pro('1'=全解除)。移行のため一度だけ読む

export interface ProState {
  owned: string[]; // 購入(レシート)由来で持っている買い切りkeyの集合
  devPro: boolean; // 開発用の全解除
}

export const DEFAULT_PRO_STATE: ProState = { owned: [], devPro: false };

/** 端末保存のPro状態を読む。壊れていても落とさず既定値。 */
export async function loadProState(): Promise<ProState> {
  try {
    const [o, d, legacy] = await Promise.all([
      AsyncStorage.getItem(K_OWNED),
      AsyncStorage.getItem(K_DEVPRO),
      AsyncStorage.getItem(K_LEGACY),
    ]);
    let owned: string[] = [];
    if (o) {
      try {
        const a = JSON.parse(o);
        if (Array.isArray(a)) owned = a.filter((x) => typeof x === 'string');
      } catch {
        /* 壊れていたら空 */
      }
    }
    // 旧・単一Pro('1')だった端末は「全部の級を持っていた」扱いに移行（既存ユーザーを剥がさない）。
    if (!o && legacy === '1') owned = ENTITLEMENTS.map((e) => e.key);
    return { owned, devPro: d === '1' };
  } catch {
    return { ...DEFAULT_PRO_STATE };
  }
}

/** 購入(同期)結果として「今持っている権利一式」を保存。RevenueCatは全権利を返すので置き換えで正しい。 */
export async function saveOwned(owned: string[]): Promise<void> {
  try {
    await AsyncStorage.setItem(K_OWNED, JSON.stringify(Array.from(new Set(owned))));
  } catch {
    /* 保存失敗は無視（次回同期で復帰） */
  }
}

/** 開発用の全解除を保存。 */
export async function saveDevPro(on: boolean): Promise<void> {
  try {
    await AsyncStorage.setItem(K_DEVPRO, on ? '1' : '0');
  } catch {
    /* 無視 */
  }
}

/** 指定の買い切り(分野×級)を今持っているか。開発用全解除ONなら常に true。 */
export function isEntitled(s: ProState, key: string | null | undefined): boolean {
  if (s.devPro) return true;
  return !!key && s.owned.includes(key);
}

/** 何か1つでも購入済み（設定画面の状態表示用）。 */
export function hasAnyPurchase(s: ProState): boolean {
  return s.devPro || s.owned.length > 0;
}

/** その問題の「正解・解説・図」が今ロックされているか。属する級を持っていれば false。 */
export function isLocked(q: Question, s: ProState): boolean {
  if (s.devPro) return false;
  if (FREE_QUESTION_IDS.has(q.id)) return false;
  const key = ENT_OF_QID.get(q.id);
  if (!key) return false; // どの級にも属さない(想定外)は無料扱いで安全側
  return !s.owned.includes(key);
}
