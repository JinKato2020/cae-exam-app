// 起動時のコンテンツ初期化。App() のレンダー前に一度だけ呼ぶ。
//  1) 端末キャッシュ（前回DLした差し替え分）を読み込む
//  2) それを反映してカタログ／Pro状態を再構築（＝直した問題・解説が表示される）
//  3) 裏で最新を取り込む（起動は待たせない）。取り込みで更新があれば "この起動中に" 反映し、
//     onApplied() で画面へ通知する（＝2回起動しなくても新章・修正がその場で出る）。
import { setOverrides } from './contentStore';
import { setFigureUris } from './figureStore';
import { loadCache, syncContent } from './contentOta';
import { rebuildCatalog } from '../catalog';
import { rebuildProState } from '../pro/proState';

// 端末キャッシュを読み直してカタログ／Pro状態へ反映する共通処理。
async function applyCache(): Promise<void> {
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
}

// onApplied: 裏の同期で新しいコンテンツを取り込み、この起動中に反映したときに呼ばれる（画面の再描画用）。
export async function initContent(onApplied?: () => void): Promise<void> {
  await applyCache();
  // 最新（テキスト＋図）を裏で取り込む。起動表示は待たない。
  void syncContent().then(async (r) => {
    // 更新が無ければ従来どおり何もしない（＝不要な再描画を出さない）。
    if (!r || r.updated <= 0) return;
    await applyCache();     // 取り込んだ差分を同セッションで反映
    onApplied?.();          // 画面へ「反映した」と通知（再描画）
  }).catch(() => {});
}
