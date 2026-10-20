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

// 同期中の復帰イベントは同じ処理を共有し、並行ダウンロードを避ける。
let refreshInFlight: Promise<boolean> | undefined;

export function refreshContent(): Promise<boolean> {
  if (refreshInFlight) return refreshInFlight;
  refreshInFlight = (async () => {
    const result = await syncContent();
    if (!result || result.updated <= 0) return false;
    await applyCache();
    return true;
  })().catch(() => false).finally(() => {
    refreshInFlight = undefined;
  });
  return refreshInFlight;
}

// onApplied: 新しい教材を反映したとき、表示中の問題も最新データで描き直す。
export async function initContent(onApplied?: () => void): Promise<void> {
  await applyCache();
  // 起動表示はローカル読込だけで進め、ネット同期を待たない。
  void refreshContent().then(updated => {
    if (updated) onApplied?.();
  });
}
