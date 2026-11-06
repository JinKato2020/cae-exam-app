import type { ReactNode } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import type { FormulaItem } from './formulas';
import { RichText } from './MathText';
import { LearningFigure } from './LearningFigure';

type Colors = { bg: string; card: string; text: string; sub: string; primary: string; border: string; reviewBtn: string; onPrimary?: string };

// 原稿で指定した改行だけを使い、長い式を途中で折らない。
export function formulaDisplay(text: string): string {
  return text.trim().split('\n').map(line => {
    const s = line.trim();
    if (!s || s.startsWith('$$')) return s;
    if (s.startsWith('$') && s.endsWith('$') && !s.slice(1, -1).includes('$')) return `$$${s.slice(1, -1)}$$`;
    if (s.includes('$') || (/[぀-ヿ一-龯]/.test(s) && !/\\[a-zA-Z]/.test(s))) return s;
    return `$$${s}$$`;
  }).join('\n');
}

/** 用語から来ても問題から来ても、同じ順序・文字サイズで読む。旧OTA原稿も表示する。 */
export function FormulaCard({ t, item, right, onScrollActive }: {
  t: Colors; item: FormulaItem; right?: ReactNode; onScrollActive?: (active: boolean) => void;
}) {
  const read = (text: string, bg = t.card, fontSize = 17) => (
    <RichText text={text} color={t.text} fontSize={fontSize} style={{ lineHeight: 30 }} scroll scrollOnlyOverflow bg={bg}
      onScrollActiveChange={onScrollActive} />
  );
  return (
    <View style={[s.card, { backgroundColor: t.card, borderColor: t.border }]}>
      <View style={s.meta}>
        <Text style={[s.badge, { backgroundColor: item.kind === 'formula' ? t.primary : t.bg, color: item.kind === 'formula' ? t.onPrimary || '#fff' : t.text }]}>
          {item.kind === 'formula' ? '公式' : '用語'}
        </Text>
        {right}
      </View>
      <Text accessibilityRole="header" selectable style={[s.title, { color: t.text }]}>{item.term}</Text>
      {!!item.summary && <Text selectable style={[s.summary, { color: t.text }]}>{item.summary}</Text>}
      {!!item.formula && <View style={[s.formula, { backgroundColor: t.bg, borderColor: t.border }]}>
        <Text style={[s.label, { color: t.sub }]}>基本の式</Text>
        {read(formulaDisplay(item.formula), t.bg, 20)}
      </View>}
      <View style={s.section}>
        {!!item.summary && <Text style={[s.label, { color: t.primary }]}>{item.formula ? '式の意味と使い方' : '意味と使い方'}</Text>}
        {read(item.body)}
      </View>
      {!!item.figureImage && <LearningFigure figure={{ figureImage: item.figureImage,
        caption: item.figureCaption || `${item.term}の図` }} colors={t} />}
      {!!item.example && <View style={[s.example, { borderColor: t.border }]}>
        <Text style={[s.label, { color: t.primary }]}>{item.exampleLabel || '具体例・補足'}</Text>
        {read(item.example)}
      </View>}
    </View>
  );
}

const s = StyleSheet.create({
  card: { padding: 16, borderWidth: 1, borderRadius: 16, marginBottom: 20, minWidth: 0 },
  meta: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  badge: { color: '#fff', paddingHorizontal: 10, paddingVertical: 5, borderRadius: 8, fontSize: 13, fontWeight: '700' },
  title: { fontSize: 20, lineHeight: 30, fontWeight: '700', marginBottom: 12, flexShrink: 1 },
  summary: { fontSize: 17, lineHeight: 29, marginBottom: 16 },
  formula: { padding: 12, borderWidth: 1, borderRadius: 10, marginBottom: 18, minWidth: 0 },
  section: { minWidth: 0 },
  label: { fontSize: 15, lineHeight: 23, fontWeight: '700', marginBottom: 8 },
  example: { marginTop: 18, paddingTop: 16, borderTopWidth: 1, minWidth: 0 },
});
