// Pro（買い切り）の状態管理と「無料で見せる範囲」の判定をまとめた場所。
// 方針（ユーザー確定 2026-09-16）:
//   ・各章の先頭5問は無料。6問目以降は「正解・解説・図」がロック（問題文と選択肢は見える）。
//   ・公式・用語ページは全問無料（このファイルはゲートしない）。
//   ・買い切り（非消耗・一回購入で永久Pro）。iOSのみ。
// 通信が切れてもProが剥がれないよう、購入状態は端末に保存した値を信じる（正本はストアのレシート）。
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Question } from '../types';
import { CATALOG } from '../catalog';

/** 各章、無料で全部見られる先頭の問題数。 */
export const FREE_PER_CHAPTER = 5;

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

/** その問題の「正解・解説・図」が今ロックされているか。Proなら常に false。 */
export function isLocked(q: Question, isPro: boolean): boolean {
  if (isPro) return false;
  return !FREE_QUESTION_IDS.has(q.id);
}

// ---- 端末に保存する購入状態 ----
const K_ACTIVE = 'cae.pro.active'; // ストア同期で得た「購入済み」フラグのキャッシュ
const K_DEVPRO = 'cae.pro.devpro'; // 開発用の強制Pro（審査・テスト用。実購入なしでPro画面を確認）

export interface ProState {
  active: boolean; // 購入(レシート)由来のPro
  devPro: boolean; // 開発用の強制Pro
}

export const DEFAULT_PRO_STATE: ProState = { active: false, devPro: false };

/** 端末保存のPro状態を読む。壊れていても落とさず既定値。 */
export async function loadProState(): Promise<ProState> {
  try {
    const [a, d] = await Promise.all([AsyncStorage.getItem(K_ACTIVE), AsyncStorage.getItem(K_DEVPRO)]);
    return { active: a === '1', devPro: d === '1' };
  } catch {
    return { ...DEFAULT_PRO_STATE };
  }
}

/** 購入(同期)結果を保存。 */
export async function saveProActive(active: boolean): Promise<void> {
  try {
    await AsyncStorage.setItem(K_ACTIVE, active ? '1' : '0');
  } catch {
    /* 保存失敗は無視（次回同期で復帰） */
  }
}

/** 開発用の強制Proを保存。 */
export async function saveDevPro(on: boolean): Promise<void> {
  try {
    await AsyncStorage.setItem(K_DEVPRO, on ? '1' : '0');
  } catch {
    /* 無視 */
  }
}

/** 実効的に「今Proか」。開発用強制ProがONなら購入なしでもPro。 */
export function effectiveIsPro(s: ProState): boolean {
  return s.devPro || s.active;
}
