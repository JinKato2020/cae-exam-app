// 購入画面（Paywall）。CAEの配色(Theme)に合わせた自前UI。買い切り1商品（iOS）。
// 価格はストア登録値を RevenueCat 経由で表示（アプリに金額を書かない）。
// Apple審査の必須要素: 価格の明示 /「購入を復元」/ 規約・プライバシーへの導線。
// キー未設定・商品未登録のうちは pkg=null →「まもなく提供」を出すだけ（壊れない）。
import { useEffect, useState } from 'react';
import { View, Text, Pressable, ScrollView, ActivityIndicator, Alert, Linking, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import type { PurchasesPackage } from 'react-native-purchases';
import { getCurrentOffering, pickLifetimePackage, purchase, restore, syncEntitlement } from './purchases';
import { saveProActive } from './proState';
import { TERMS_URL, PRIVACY_URL } from '../config/revenuecat';

type PayTheme = {
  bg: string; text: string; sub: string; card: string; border: string;
  primary: string; correct: string; amber: string; disabled: string;
};

export default function Paywall(props: { t: PayTheme; onClose: () => void; onPurchased: () => void }) {
  const { t } = props;
  const s = makeStyles(t);
  const [pkg, setPkg] = useState<PurchasesPackage | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const off = await getCurrentOffering();
      if (!cancelled) {
        setPkg(pickLifetimePackage(off));
        setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  async function onBuy() {
    if (busy || !pkg) return;
    setBusy(true);
    const ok = await purchase(pkg);
    if (ok) {
      await saveProActive(true);
      Alert.alert('ありがとうございます', 'すべての問題の正解・解説・図が見られるようになりました。');
      props.onPurchased();
    } else {
      // キャンセルも false。静かに戻す（誤タップ配慮で失敗メッセージは出さない）
      setBusy(false);
    }
  }

  async function onRestore() {
    if (busy) return;
    setBusy(true);
    const ok = await restore();
    const active = ok ? true : await syncEntitlement();
    if (typeof active === 'boolean') await saveProActive(active);
    setBusy(false);
    if (active) {
      Alert.alert('購入を復元しました', 'Proが有効になりました。');
      props.onPurchased();
    } else {
      Alert.alert('復元できる購入がありません', '同じApple IDで購入済みかご確認ください。');
    }
  }

  return (
    <SafeAreaView style={s.wrap} edges={['top', 'left', 'right']}>
      <ScrollView contentContainerStyle={s.scroll} showsVerticalScrollIndicator={false}>
        <View style={s.hero}>
          <Text style={s.heroEmoji}>🎓</Text>
          <Text style={s.title}>CAE Pro（買い切り）</Text>
          <Text style={s.subtitle}>一度の購入で、すべての問題をずっと使えます。</Text>
        </View>

        <View style={s.benefits}>
          <Text style={s.benefit}>✓ すべての章・すべての問題の「正解・解説・図」が見放題</Text>
          <Text style={s.benefit}>✓ 2級・1級の全章に対応</Text>
          <Text style={s.benefit}>✓ 買い切り（月額なし）。一度きりの購入で永久に有効</Text>
          <Text style={s.benefit}>✓ 公式・用語ページは無料のまま（購入は問題の解説向け）</Text>
        </View>

        {loading ? (
          <ActivityIndicator color={t.primary} style={{ marginVertical: 28 }} />
        ) : pkg ? (
          <Pressable style={[s.buy, busy && s.busy]} onPress={onBuy} disabled={busy} hitSlop={4}>
            <Text style={s.buyLabel}>このアプリを解除する</Text>
            <Text style={s.buyPrice}>{pkg.product.priceString}（買い切り）</Text>
          </Pressable>
        ) : (
          <Text style={s.soon}>購入はまもなく提供予定です。</Text>
        )}

        <Pressable style={s.restore} onPress={onRestore} disabled={busy} hitSlop={8}>
          <Text style={s.restoreTxt}>購入を復元</Text>
        </Pressable>

        <Text style={s.note}>
          本アプリは非公認の独自補助教材です。公式標準問題の番号は対応学習のための参照です。
        </Text>

        {(TERMS_URL || PRIVACY_URL) ? (
          <View style={s.links}>
            {TERMS_URL ? (
              <Pressable onPress={() => Linking.openURL(TERMS_URL)} hitSlop={8}>
                <Text style={s.link}>利用規約</Text>
              </Pressable>
            ) : null}
            {TERMS_URL && PRIVACY_URL ? <Text style={s.sep}>·</Text> : null}
            {PRIVACY_URL ? (
              <Pressable onPress={() => Linking.openURL(PRIVACY_URL)} hitSlop={8}>
                <Text style={s.link}>プライバシーポリシー</Text>
              </Pressable>
            ) : null}
          </View>
        ) : null}

        <Pressable style={s.close} onPress={props.onClose} hitSlop={8}>
          <Text style={s.closeTxt}>閉じる</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

function makeStyles(t: PayTheme) {
  return StyleSheet.create({
    wrap: { flex: 1, backgroundColor: t.bg },
    scroll: { padding: 20, paddingBottom: 40, gap: 14 },
    hero: { alignItems: 'center', gap: 8, paddingVertical: 16 },
    heroEmoji: { fontSize: 44 },
    title: { fontSize: 24, fontWeight: '800', color: t.text, textAlign: 'center' },
    subtitle: { fontSize: 14, color: t.sub, textAlign: 'center', lineHeight: 21 },
    benefits: { gap: 10, backgroundColor: t.card, borderColor: t.border, borderWidth: 1, borderRadius: 14, padding: 16 },
    benefit: { fontSize: 15, color: t.text, lineHeight: 22 },
    soon: { fontSize: 15, color: t.sub, textAlign: 'center', marginVertical: 24 },
    buy: {
      backgroundColor: t.primary, borderRadius: 14, paddingVertical: 16, paddingHorizontal: 18,
      alignItems: 'center', gap: 4, marginTop: 4,
    },
    busy: { opacity: 0.5 },
    buyLabel: { fontSize: 17, fontWeight: '800', color: '#ffffff' },
    buyPrice: { fontSize: 14, color: '#ffffff', opacity: 0.92 },
    restore: { alignItems: 'center', paddingVertical: 12, marginTop: 2 },
    restoreTxt: { fontSize: 15, fontWeight: '700', color: t.primary },
    note: { fontSize: 12, color: t.sub, textAlign: 'center', lineHeight: 18, marginTop: 4 },
    links: { flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: 8, marginTop: 2 },
    link: { fontSize: 13, color: t.sub, textDecorationLine: 'underline' },
    sep: { fontSize: 13, color: t.sub },
    close: { alignItems: 'center', paddingVertical: 12, marginTop: 6 },
    closeTxt: { fontSize: 15, color: t.sub },
  });
}
