// 図の差し替え表：OTAで落とした図のローカルURIを優先し、無ければ同梱(FIGURES=require)を返す。
// ※ src/figures.ts は tools/gen_figures_ts.py の自動生成物なので触らない。解決はこの別モジュールで行う。
import type { ImageSourcePropType } from 'react-native';
import { FIGURES } from '../figures';

let uris: Record<string, string> = {};

/** 起動時に、端末キャッシュから見つけた図のローカルURI(figures/キー→file://…)をセットする。 */
export function setFigureUris(m: Record<string, string> | null | undefined): void {
  uris = m ?? {};
}

/** 図キー(例 figures/xxx.png ではなく FIGURES と同じキー) の画像ソース。OTA版{uri}優先→同梱require。 */
export function figureSource(key: string | undefined | null): ImageSourcePropType | undefined {
  if (!key) return undefined;
  if (Object.prototype.hasOwnProperty.call(uris, key)) return { uri: uris[key] };
  return FIGURES[key];
}

/** その図が表示可能か（OTA版か同梱のどちらかにあるか）。 */
export function hasFigure(key: string | undefined | null): boolean {
  if (!key) return false;
  return Object.prototype.hasOwnProperty.call(uris, key)
    || Object.prototype.hasOwnProperty.call(FIGURES, key);
}
