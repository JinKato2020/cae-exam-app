// RevenueCat の「公開SDKキー」設定（CAE専用・iOSのみ）。
// これは公開キー（アプリに埋め込んで安全。秘密鍵ではない）。空のうちは課金機能は一切起動しない(no-op)＝
// アプリは今までどおり無料で全部動く。CAE用のRevenueCatプロジェクトを作り、そのiOS公開キーをここに入れて初めて有効化。
//   入れ方: RevenueCat ダッシュボード → Project → API keys → Apple App Store の "appl_..." を IOS_KEY へ。
// ※ JLPTアプリのキーを流用しないこと（別アプリ＝別プロジェクト）。
import { Platform } from 'react-native';

// ▼▼ CAE用RevenueCatのiOS公開キー（appl_...）。2026-09-16 設定。 ▼▼
const IOS_KEY = 'appl_qvyTIYAdQbBhSifdwfVIAmxKCUe';
// ▲▲ （Androidは当面対象外。将来 goog_... を足す場合はここに） ▲▲
const ANDROID_KEY = '';

// 【買い切りの単位＝分野×級】RevenueCat の Entitlement / Package の識別子は、
//   src/pro/proState.ts の entKey(fieldId, gradeId)（例 'solid_g2' / 'solid_g1'）と一致させること。
//   ・RevenueCat の Entitlements に級ごとに1つ（'solid_g2' 等）を作る。
//   ・Current Offering の Package 識別子も同じ 'solid_g2' 等にして、対応する商品を割り当てる。
//   ・対応する App Store の製品IDは 'com.safa.cae.solid.g2' 等（RevenueCat側で商品に紐づけ）。
// （旧・単一Pro('pro'/'lifetime')は廃止。分野×級ごとの個別購入に変更）

// 審査で必要な導線（利用規約・プライバシーポリシー）。公開先=公開リポ JinKato2020/cae-legal の GitHub Pages。
export const TERMS_URL = 'https://jinkato2020.github.io/cae-legal/terms.html';
export const PRIVACY_URL = 'https://jinkato2020.github.io/cae-legal/privacy.html';

/** 今のプラットフォームの公開SDKキー。未設定なら ''(=課金を起動しない)。 */
export function revenueCatApiKey(): string {
  return (Platform.OS === 'ios' ? IOS_KEY : ANDROID_KEY).trim();
}

/** キーが入っているか(=課金を有効化してよいか)。 */
export function purchasesConfigured(): boolean {
  return revenueCatApiKey().length > 0;
}
