// ブックマーク（栞）を端末に保存する。問題ごとに「登録したか・登録時刻」を持つ。
// 後で見返したい問題にユーザーが栞を付け、ホームの「ブックマークを復習」でまとめて解き直せる。
// 保存の仕組みは学習記録（src/progress.ts）と同じ：AsyncStorage に1キーでJSON保存。
import AsyncStorage from '@react-native-async-storage/async-storage';

const KEY = 'cae.bookmarks.v1';

// 問題ID → 登録した時刻（Date.now()）。新しく登録した順に並べ替えるのに使う。
export type BookmarkMap = Record<string, number>;

export async function loadBookmarks(): Promise<BookmarkMap> {
  try {
    const raw = await AsyncStorage.getItem(KEY);
    if (!raw) return {};
    const obj = JSON.parse(raw);
    return obj && typeof obj === 'object' ? (obj as BookmarkMap) : {};
  } catch {
    return {};
  }
}

async function save(map: BookmarkMap): Promise<void> {
  try {
    await AsyncStorage.setItem(KEY, JSON.stringify(map));
  } catch {
    // 保存に失敗してもクラッシュさせない
  }
}

// 栞をトグル（付いていれば外す・無ければ付ける）。更新後のマップを返す（イミュータブル更新）。
export async function toggleBookmark(map: BookmarkMap, id: string): Promise<BookmarkMap> {
  const out = { ...map };
  if (out[id]) delete out[id];
  else out[id] = Date.now();
  await save(out);
  return out;
}

export function isBookmarked(map: BookmarkMap, id: string): boolean {
  return !!map[id];
}

// 登録が新しい順の問題ID（復習の並び＝最近付けた栞から）。
export function bookmarkIdsFrom(map: BookmarkMap): string[] {
  return Object.keys(map).sort((a, b) => (map[b] ?? 0) - (map[a] ?? 0));
}

export async function resetBookmarks(): Promise<BookmarkMap> {
  try {
    await AsyncStorage.removeItem(KEY);
  } catch {
    /* noop */
  }
  return {};
}
