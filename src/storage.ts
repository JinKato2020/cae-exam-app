// 間違えた問題ID・学習記録を端末に保存する（次回起動しても復習できる）。
import AsyncStorage from '@react-native-async-storage/async-storage';

const WRONG_KEY = 'cae.wrongIds.v1';

// 間違いID集合を読み込む
export async function loadWrongIds(): Promise<string[]> {
  try {
    const raw = await AsyncStorage.getItem(WRONG_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    return Array.isArray(arr) ? arr.filter((x) => typeof x === 'string') : [];
  } catch {
    // 保存領域が使えない場合でもアプリは動く（空扱い）
    return [];
  }
}

// 回答結果を反映：正解した問題は復習リストから外し、間違えた問題は追加する
export async function updateWrongIds(
  current: string[],
  results: { id: string; correct: boolean }[]
): Promise<string[]> {
  const set = new Set(current);
  for (const r of results) {
    if (r.correct) set.delete(r.id);
    else set.add(r.id);
  }
  const next = Array.from(set);
  try {
    await AsyncStorage.setItem(WRONG_KEY, JSON.stringify(next));
  } catch {
    // 保存に失敗してもクラッシュさせない
  }
  return next;
}
