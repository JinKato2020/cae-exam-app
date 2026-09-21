// コンテンツの「差し替え表」。OTAで落としたデータ(override)を優先し、無ければ同梱(BUNDLED)を返す。
// キーは manifest と同じ相対パス（例 content/questions/math-basics.json / content/catalog.json）。
// これで「直した所はOTA版・直していない所は同梱版」を1問単位でなくファイル単位で切り替えられる。
import { BUNDLED } from './bundled.generated';

let overrides: Record<string, unknown> = {};

/** 起動時に、端末キャッシュから読んだ差し替え分をまとめてセットする。 */
export function setOverrides(files: Record<string, unknown> | null | undefined): void {
  overrides = files ?? {};
}

/** キーでコンテンツを引く。override（OTA）優先 → BUNDLED（同梱）→ null。 */
export function getContent<T = unknown>(key: string): T | null {
  if (Object.prototype.hasOwnProperty.call(overrides, key)) return overrides[key] as T;
  if (Object.prototype.hasOwnProperty.call(BUNDLED, key)) return BUNDLED[key] as T;
  return null;
}

/** そのキーのコンテンツが存在するか（override か同梱のどちらかにあるか）。 */
export function hasContent(key: string): boolean {
  return Object.prototype.hasOwnProperty.call(overrides, key)
    || Object.prototype.hasOwnProperty.call(BUNDLED, key);
}
