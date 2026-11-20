import { useEffect, useRef, useState } from 'react';
import { Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import { getContent } from './data/contentStore';
import { CATALOG, questionsByIds } from './catalog';
import type { FieldId, GradeId } from './progress';
import type { Question } from './types';
import type { ProState } from './pro/proState';
import type { PayTarget } from './pro/Paywall';

export type WrittenReviewEntry = {
  id: string; field: FieldId; grade: GradeId; chapter: number;
  officialNumber: string; title: string; kind: string; answerTypes?: string[];
  questionId?: string;
};
type WrittenReviewDoc = { schema: number; entries: WrittenReviewEntry[] };
type Colors = { bg: string; card: string; text: string; sub: string; border: string; primary: string };

// 古いOTAデータに本文が残っていても、復習カードでは一切描画しない。
export function writtenReviewEntries(field: FieldId, grade: GradeId, chapters: ReadonlySet<number> | null) {
  const doc = getContent<WrittenReviewDoc>('content/exam/written-review.json');
  if (doc?.schema !== 1 || !Array.isArray(doc.entries)) return [];
  return doc.entries.filter(e => e.field === field && e.grade === grade
    && (!chapters || chapters.has(e.chapter)))
    .sort((a, b) => a.chapter - b.chapter
      || a.officialNumber.localeCompare(b.officialNumber, 'ja', { numeric: true }));
}

// IDが別課程や削除済み問題を指す場合は、別の問題を代わりに開かない。
export function reviewQuestion(entry: WrittenReviewEntry): Question | undefined {
  if (!entry.questionId) return undefined;
  const candidates = questionsByIds([entry.questionId]);
  const course = CATALOG.find(f => f.id === entry.field)?.grades.find(g => g.id === entry.grade);
  return course?.chapters.flatMap(c => c.data.questions).find(q => candidates.includes(q));
}

export function WrittenReviewButton(props: {
  field: FieldId; grade: GradeId; chapters: ReadonlySet<number> | null;
  subjectLabel: string; t: Colors; proState: ProState;
  onOpenPaywall: (target: PayTarget | null) => void;
  onOpenQuestion: (questionId: string, cardId: string) => void;
  resumeCardId?: string | null;
}) {
  const doc = getContent<WrittenReviewDoc>('content/exam/written-review.json');
  const contentReady = doc?.schema === 1 && Array.isArray(doc.entries);
  const entries = writtenReviewEntries(props.field, props.grade, props.chapters);
  const [open, setOpen] = useState(false);
  const listRef = useRef<ScrollView>(null);
  const returnCardId = useRef<string | null>(null);
  const cardPositions = useRef(new Map<string, number>());
  const listHeight = useRef(0);
  const contentHeight = useRef(0);
  function restoreListPosition() {
    const y = returnCardId.current ? cardPositions.current.get(returnCardId.current) : undefined;
    if (y === undefined || !listRef.current || !listHeight.current || !contentHeight.current) return;
    listRef.current.scrollTo({
      y: Math.max(0, Math.min(y - 8, contentHeight.current - listHeight.current)),
      animated: false,
    });
    returnCardId.current = null;
  }
  function showList(cardId: string | null) {
    returnCardId.current = cardId;
    cardPositions.current.clear(); listHeight.current = 0; contentHeight.current = 0;
    setOpen(true);
  }
  useEffect(() => {
    setOpen(false); returnCardId.current = null; cardPositions.current.clear();
  }, [props.field, props.grade, props.chapters]);
  useEffect(() => {
    if (props.resumeCardId) showList(props.resumeCardId);
  }, [props.resumeCardId]);
  const { t } = props;
  return <>
    <Pressable accessibilityRole="button" accessibilityLabel="記述・計算・導出を復習"
      onPress={() => showList(null)} style={[s.launch, { borderColor: t.primary }]}>
      <Text style={[s.launchText, { color: t.primary }]}>復習 · 記述・計算・導出{contentReady ? '（' + entries.length + '問）' : ''} ›</Text>
    </Pressable>
    <Modal visible={open} animationType="slide" onRequestClose={() => setOpen(false)}>
      <SafeAreaProvider>
        <SafeAreaView style={[s.screen, { backgroundColor: t.bg }]}>
          <View style={[s.header, { borderBottomColor: t.border }]}>
            <Text style={[s.heading, { color: t.text }]}>記述・計算・導出の復習</Text>
            <Pressable accessibilityRole="button" accessibilityLabel="復習を閉じる" hitSlop={8}
              onPress={() => setOpen(false)} style={s.close}>
              <Text style={[s.link, { color: t.primary }]}>閉じる</Text>
            </Pressable>
          </View>
          <Text style={[s.subject, { color: t.sub }]}>{props.subjectLabel} · {entries.length}問</Text>
          <ScrollView ref={listRef} style={s.flex} contentContainerStyle={s.content}
            onLayout={e => { listHeight.current = e.nativeEvent.layout.height; restoreListPosition(); }}
            onContentSizeChange={(_width, height) => { contentHeight.current = height; restoreListPosition(); }}>
            {entries.length === 0 && <Text style={[s.paragraph, { color: t.text }]}>{contentReady
              ? 'この範囲には復習カードがまだ登録されていません。'
              : '復習カードを読み込んでいます。'}</Text>}
            {entries.map((entry, i) => {
              const q = reviewQuestion(entry);
              return <View key={entry.id} onLayout={e => {
                cardPositions.current.set(entry.id, e.nativeEvent.layout.y); restoreListPosition();
              }}>
                {(i === 0 || entries[i - 1].chapter !== entry.chapter) &&
                  <Text style={[s.chapter, { color: t.sub }]}>第{entry.chapter}章</Text>}
                <Pressable accessibilityRole="button" disabled={!q}
                  accessibilityLabel={'問' + entry.officialNumber + 'のアプリ問題を開く'}
                  onPress={() => {
                    if (!q) return;
                    setOpen(false); props.onOpenQuestion(q.id, entry.id);
                  }} style={[s.card, { backgroundColor: t.card, borderColor: t.border, opacity: q ? 1 : 0.5 }]}>
                  <Text style={[s.itemTitle, { color: t.text }]}>問{entry.officialNumber}　{q?.title ?? entry.title} ›</Text>
                  <View style={s.tags}>{(entry.answerTypes ?? [entry.kind]).map(label =>
                    <Text key={label} style={[s.tag, { color: t.primary, borderColor: t.border }]}>{label}</Text>)}</View>
                  <Text style={[s.subject, { color: t.sub }]}>{q ? 'アプリの問題で学習する' : '対応するアプリ問題は準備中です'}</Text>
                </Pressable>
              </View>;
            })}
          </ScrollView>
        </SafeAreaView>
      </SafeAreaProvider>
    </Modal>
  </>;
}

const s = StyleSheet.create({
  screen: { flex: 1 }, flex: { flex: 1 },
  tags: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, marginVertical: 10 },
  tag: { fontSize: 13, lineHeight: 20, borderWidth: 1, borderRadius: 7, paddingHorizontal: 8, paddingVertical: 3 },
  launch: { marginTop: 16, padding: 14, borderRadius: 12, borderWidth: 1, backgroundColor: '#0E1728' },
  launchText: { fontSize: 16, fontWeight: '700', textAlign: 'center' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingVertical: 8, borderBottomWidth: 1, flexShrink: 0 },
  heading: { flex: 1, marginRight: 12, fontSize: 19, fontWeight: '700', lineHeight: 28 },
  link: { fontSize: 16, fontWeight: '600' },
  close: { minWidth: 76, minHeight: 48, padding: 12, flexShrink: 0, alignItems: 'center', justifyContent: 'center' },
  subject: { fontSize: 13, lineHeight: 21, marginTop: 6, marginHorizontal: 2 },
  content: { padding: 16, paddingBottom: 32 },
  card: { borderRadius: 14, padding: 16, borderWidth: 1, marginVertical: 8, gap: 12 },
  chapter: { fontSize: 16, fontWeight: '700', marginTop: 18, marginBottom: 4 },
  itemTitle: { fontSize: 17, fontWeight: '600', lineHeight: 26 },
  paragraph: { fontSize: 17, lineHeight: 27, margin: 16 },
});
