// RevenueCat(react-native-purchases)の薄いラッパー。UI・起動処理はこの関数だけを呼ぶ(SDKを直接触らない)。
// 【重要】キー未設定(src/config/revenuecat.ts が空)なら、全メソッドが安全に何もしない＝アプリは従来どおり動く。
// 例外は決してUIへ投げない(課金の失敗でアプリを落とさない)。Proかどうかの正本はストアのレシート。
// （JLPTアプリの同名ファイルを土台に、CAEの買い切り(iOS)向けへ整理）
import Purchases, {
  LOG_LEVEL,
  type CustomerInfo,
  type PurchasesOffering,
  type PurchasesPackage,
} from 'react-native-purchases';
import { revenueCatApiKey, purchasesConfigured } from '../config/revenuecat';

let configured = false;

/** 起動時に1回。Proでなくても必要(購入・復元・権利同期の土台)。キー未設定なら何もしない。 */
export async function initPurchases(appUserID?: string | null): Promise<void> {
  if (configured || !purchasesConfigured()) return;
  try {
    // eslint-disable-next-line no-undef
    if (typeof __DEV__ !== 'undefined' && __DEV__) await Purchases.setLogLevel(LOG_LEVEL.WARN);
    Purchases.configure({ apiKey: revenueCatApiKey(), appUserID: appUserID ?? null });
    configured = true;
  } catch {
    /* 課金初期化に失敗してもアプリは止めない */
  }
}

/** CustomerInfo から「今持っている買い切りkeyの一覧」を読む純粋な写像。
 *  RevenueCat の active な Entitlement の識別子（= proState の entKey と一致させる）をそのまま返す。 */
function activeKeys(info: CustomerInfo): string[] {
  return Object.keys(info.entitlements.active);
}

/** RevenueCat と同期して「今持っている買い切りkey一覧」を返す。呼び出し側は結果を端末へ保存する。
 *  未設定・通信失敗時は null(=状態を変えない＝端末に保存済みの前回値を保つ)。 */
export async function syncEntitlements(): Promise<string[] | null> {
  if (!configured) return null;
  try {
    return activeKeys(await Purchases.getCustomerInfo());
  } catch {
    return null;
  }
}

/** 購入画面に出す商品一式。未設定・失敗時は null(画面は「まもなく提供」を出す)。 */
export async function getCurrentOffering(): Promise<PurchasesOffering | null> {
  if (!configured) return null;
  try {
    return (await Purchases.getOfferings()).current ?? null;
  } catch {
    return null;
  }
}

/** 指定key（分野×級）の買い切りパッケージを選ぶ。Package識別子が key と一致するものを返す。無ければ null。 */
export function pickPackage(offering: PurchasesOffering | null, key: string): PurchasesPackage | null {
  if (!offering) return null;
  const pkgs = offering.availablePackages ?? [];
  return pkgs.find((p) => p.identifier === key) ?? null;
}

/** 購入。成功後に「今持っている買い切りkey一覧」を返す。ユーザーキャンセル・失敗は null。 */
export async function purchase(pkg: PurchasesPackage): Promise<string[] | null> {
  if (!configured) return null;
  try {
    const { customerInfo } = await Purchases.purchasePackage(pkg);
    return activeKeys(customerInfo);
  } catch {
    return null; // キャンセルもここに来る(RevenueCatはキャンセルを例外で返す)
  }
}

/** 購入の復元(Apple審査で必須)。復元後に「今持っている買い切りkey一覧」を返す。失敗は null。 */
export async function restore(): Promise<string[] | null> {
  if (!configured) return null;
  try {
    return activeKeys(await Purchases.restorePurchases());
  } catch {
    return null;
  }
}

/** ログイン時: RevenueCat のユーザーを実IDへ紐付け(機種変・複数端末で権利がfollowする)。→ 今持っているkey一覧。 */
export async function linkAccount(userId: string): Promise<string[] | null> {
  if (!configured) return null;
  try {
    const { customerInfo } = await Purchases.logIn(userId);
    return activeKeys(customerInfo);
  } catch {
    return null;
  }
}

/** ログアウト時: 匿名IDへ戻す(すでに匿名なら例外→無視)。 */
export async function unlinkAccount(): Promise<void> {
  if (!configured) return;
  try {
    await Purchases.logOut();
  } catch {
    /* すでに匿名などは無視 */
  }
}
