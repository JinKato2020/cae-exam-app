// RevenueCat の「公開SDKキー」設定（CAE専用・iOS/Android）。
// これは公開キー（アプリに埋め込んで安全。秘密鍵ではない）。空のうちは課金機能は一切起動しない(no-op)＝
// アプリは今までどおり無料で全部動く。CAE用のRevenueCatプロジェクトを作り、そのiOS公開キーをここに入れて初めて有効化。
//   入れ方: RevenueCat ダッシュボード → Project → API keys → Apple App Store の "appl_..." を IOS_KEY へ。
// ※ JLPTアプリのキーを流用しないこと（別アプリ＝別プロジェクト）。
import { Platform } from 'react-native';

// ▼▼ CAE用RevenueCatのiOS公開キー（appl_...）。2026-09-16 設定。 ▼▼
const IOS_KEY = 'appl_qvyTIYAdQbBhSifdwfVIAmxKCUe';
// ▲▲ CAE用RevenueCatのAndroid公開キー（goog_...）。2026-09-27 設定。Google Play=com.safa.nepali.jp ▲▲
const ANDROID_KEY = 'goog_ZqItVqIEXCEvNmVQaMfyGVKXSct';

// 【買い切りの単位＝分野×級】RevenueCat の Entitlement / Package の識別子は、
//   src/pro/proState.ts の entKey(fieldId, gradeId)（例 'solid_g2' / 'solid_g1'）と一致させること。
//   ・RevenueCat の Entitlements に級ごとに1つ（'solid_g2' 等）を作る。
//   ・Current Offering の Package 識別子も同じ 'solid_g2' 等にして、対応する商品を割り当てる。
//   ・対応する App Store の製品IDは 'com.safa.cae.solid.g2' 等（RevenueCat側で商品に紐づけ）。
// （旧・単一Pro('pro'/'lifetime')は廃止。分野×級ごとの個別購入に変更）

// 審査で必要な導線（利用規約・プライバシーポリシー・サポート）。公開先=公開リポ JinKato2020/LEGAL の GitHub Pages（/LEGAL/cae/ 配下）。
export const TERMS_URL = 'https://jinkato2020.github.io/LEGAL/cae/terms.html';
export const PRIVACY_URL = 'https://jinkato2020.github.io/LEGAL/cae/privacy.html';
// サポートページ（審査・ストア掲載で必要なサポートURL）。/LEGAL/cae/ 配下。
export const SUPPORT_URL = 'https://jinkato2020.github.io/LEGAL/cae/support.html';

// 問い合わせ窓口。JLPT等 別アプリと同じ受信箱(contact@safa-lang.com)を共有するため、
// 件名に必ず【CAE】を自動付与して、どのアプリからの問い合わせか一目で分かるようにする(混同防止)。
export const SUPPORT_EMAIL = 'contact@safa-lang.com';
export const SUPPORT_SUBJECT = '【CAE】お問い合わせ';
/** タップでメール作成（宛先＋件名「【CAE】お問い合わせ」を自動セット）。Linking.openURL に渡す。 */
export const SUPPORT_MAILTO_URL =
  `mailto:${SUPPORT_EMAIL}?subject=${encodeURIComponent(SUPPORT_SUBJECT)}`;

// ▼▼ 設定画面の「アプリを評価する」ボタン用。ストアのレビュー作成ページ（星＋コメントが書ける）を開く。
//   ※ OS標準の自動ポップアップ(expo-store-review)とは別物。ボタンはこちら＝ストアに飛ばす方式のみ使う
//     （ボタンに requestReview を紐付けるのは Apple ガイドライン違反）。
// APP_STORE_ID = App Store の数値ID（App Store URL ".../id0000000000" の数字）。
//   未設定('')のうちは iOS のレビューボタンは表示しない（Android は下記パッケージで動く）。
export const APP_STORE_ID = '6811044269';
export const ANDROID_PACKAGE = 'com.safa.nepali.jp';
/** ストアのレビュー作成ページURL（星＋コメントを書ける）。開けない環境では null。 */
export function reviewUrl(): string | null {
  if (Platform.OS === 'ios') {
    return APP_STORE_ID ? `itms-apps://itunes.apple.com/app/id${APP_STORE_ID}?action=write-review` : null;
  }
  if (Platform.OS === 'android') {
    return `market://details?id=${ANDROID_PACKAGE}`;
  }
  return null;
}

/** 今のプラットフォームの公開SDKキー。未設定なら ''(=課金を起動しない)。 */
export function revenueCatApiKey(): string {
  return (Platform.OS === 'ios' ? IOS_KEY : ANDROID_KEY).trim();
}

/** キーが入っているか(=課金を有効化してよいか)。 */
export function purchasesConfigured(): boolean {
  return revenueCatApiKey().length > 0;
}
