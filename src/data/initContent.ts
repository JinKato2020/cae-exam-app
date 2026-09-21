// 起動時のコンテンツ初期化。App() のレンダー前に一度だけ呼ぶ。
//  1) 端末キャッシュ（前回DLした差し替え分）を読み込む
//  2) それを反映してカタログ／Pro状態を再構築（＝直した問題・解説が表示される）
//  3) 裏で最新を取り込む（待たない＝起動を遅らせない。反映は次回起動＝ユーザー確定方針(a)）
import { setOverrides } from './contentStore';
import { setFigureUris } from './figureStore';
import { loadCache, syncContent } from './contentOta';
import { rebuildCatalog } from '../catalog';
import { rebuildProState } from '../pro/proState';

export async function initContent(): Promise<void> {
  try {
    const cached = await loadCache();
    setOverrides(cached.content);
    setFigureUris(cached.figures);
  } catch {
    setOverrides({});
    setFigureUris({});
  }
  // 差し替えを反映（override が無ければ同梱=従来どおり）。
  rebuildCatalog();
  rebuildProState();
  // 次回起動用に最新（テキスト＋図）を取り込む（この起動では待たない・反映しない）。
  void syncContent();
}
