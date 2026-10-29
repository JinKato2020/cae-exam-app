import { useEffect, useRef, useState } from 'react';
import { Image, Modal, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { getContent } from './data/contentStore';
import { figureSource } from './data/figureStore';
import { questionsByIds } from './catalog';
import { RichText } from './MathText';
import type { FieldId, GradeId } from './progress';
import { entInfoByKey, entKey, isLocked, type ProState } from './pro/proState';
import type { PayTarget } from './pro/Paywall';

export type WrittenReviewImage = { key: string; width: number; height: number; page?: string };
export type WrittenReviewEntry = {
  id: string;
  field: FieldId;
  grade: GradeId;
  chapter: number;
  officialNumber: string;
  title: string;
  kind: string;
  questionId?: string;
  question: string;
  questionImages?: WrittenReviewImage[];
  explanation?: string;
  explanationImages?: WrittenReviewImage[];
  source: { kind: 'verbatim' | 'extracted'; label: string };
};
type WrittenReviewDoc = { schema: number; entries: WrittenReviewEntry[] };
type Colors = { bg: string; card: string; text: string; sub: string; border: string; primary: string };

// OTAの追加・修正・削除をそのまま読む。対象問題を本体側の固定リストにしない。
export function writtenReviewEntries(field: FieldId, grade: GradeId, chapters: ReadonlySet<number> | null) {
  const doc = getContent<WrittenReviewDoc>('content/exam/written-review.json');
  if (doc?.schema !== 1 || !Array.isArray(doc.entries)) return [];
  return doc.entries.filter((e) => e.field === field && e.grade === grade
    && (!chapters || chapters.has(e.chapter)))
    .sort((a, b) => a.chapter - b.chapter
      || a.officialNumber.localeCompare(b.officialNumber, 'ja', { numeric: true }));
}

function OriginalImageZoom(props: { image: WrittenReviewImage | null; onClose: () => void; t: Colors }) {
  const [scale, setScale] = useState(1);
  const { width } = useWindowDimensions();
  useEffect(() => { setScale(1); }, [props.image?.key]);
  const imageWidth = Math.max(1, width - 32) * scale;
  return (
    <Modal visible={!!props.image} animationType="slide" onRequestClose={props.onClose}>
      <SafeAreaView style={[s.screen, { backgroundColor: props.t.bg }]}>
        <Pressable accessibilityRole="button" onPress={props.onClose} style={s.close}>
          <Text style={[s.link, { color: props.t.primary }]}>‹ 説明に戻る</Text>
        </Pressable>
        <View style={s.navigation}>
          <Pressable accessibilityRole="button" accessibilityLabel="縮小" disabled={scale <= 1}
            onPress={() => setScale((v) => Math.max(1, v - 0.5))} style={s.navButton}>
            <Text style={[s.link, { color: props.t.primary }]}>− 縮小</Text>
          </Pressable>
          <Text style={{ color: props.t.text }}>{Math.round(scale * 100)}％</Text>
          <Pressable accessibilityRole="button" accessibilityLabel="拡大" disabled={scale >= 4}
            onPress={() => setScale((v) => Math.min(4, v + 0.5))} style={s.navButton}>
            <Text style={[s.link, { color: props.t.primary }]}>＋ 拡大</Text>
          </Pressable>
        </View>
        <ScrollView style={s.flex} nestedScrollEnabled>
          <ScrollView horizontal nestedScrollEnabled>
            {props.image && <Image source={figureSource(props.image.key)} resizeMode="contain"
              style={{ margin: 16, width: imageWidth, height: imageWidth * props.image.height / props.image.width }} />}
          </ScrollView>
        </ScrollView>
      </SafeAreaView>
    </Modal>
  );
}

export function WrittenReviewButton(props: {
  field: FieldId; grade: GradeId; chapters: ReadonlySet<number> | null;
  subjectLabel: string; t: Colors; proState: ProState;
  onOpenPaywall: (target: PayTarget | null) => void;
}) {
  const reviewDocument = getContent<WrittenReviewDoc>('content/exam/written-review.json');
  const contentReady = reviewDocument?.schema === 1 && Array.isArray(reviewDocument.entries);
  const entries = writtenReviewEntries(props.field, props.grade, props.chapters);
  const [open, setOpen] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [zoom, setZoom] = useState<WrittenReviewImage | null>(null);
  const scroller = useRef<ScrollView>(null);
  const index = entries.findIndex((e) => e.id === selectedId);
  const entry = entries[index];
  useEffect(() => {
    setSelectedId(null); setShowExplanation(false); setZoom(null); setOpen(false);
  }, [props.field, props.grade, props.chapters]);
  useEffect(() => {
    setShowExplanation(false);
    scroller.current?.scrollTo({ y: 0, animated: false });
  }, [selectedId]);
  const q = entry?.questionId ? questionsByIds([entry.questionId])[0] : undefined;
  const locked = entry ? (q ? isLocked(q, props.proState)
    : !props.proState.devPro && !props.proState.owned.includes(entKey(props.field, props.grade))) : false;
  function purchase() {
    setOpen(false);
    const info = entInfoByKey(entKey(props.field, props.grade));
    props.onOpenPaywall(info ? { key: info.key, title: info.title } : null);
  }
  const { t } = props;
  return (
    <>
      <Pressable accessibilityRole="button" accessibilityLabel="記述式問題を復習"
        onPress={() => { setSelectedId(null); setOpen(true); }}
        style={[s.launch, { borderColor: t.primary }]}>
        <Text style={[s.launchText, { color: t.primary }]}>復習 · 記述式問題{contentReady ? '（' + entries.length + '問の候補）' : ''} ›</Text>
      </Pressable>
      <Modal visible={open} animationType="slide" onRequestClose={() => setOpen(false)}>
        <SafeAreaView style={[s.screen, { backgroundColor: t.bg }]}>
          <View style={[s.header, { borderBottomColor: t.border }]}>
            <Text style={[s.heading, { color: t.text }]}>記述式の復習</Text>
            <Pressable accessibilityRole="button" onPress={() => setOpen(false)} style={s.close}>
              <Text style={[s.link, { color: t.primary }]}>閉じる</Text>
            </Pressable>
          </View>
          <Text style={[s.subject, { color: t.sub }]}>{props.subjectLabel} · {entries.length}問</Text>
          {entry ? <>
            <Pressable accessibilityRole="button" onPress={() => setSelectedId(null)} style={s.back}>
              <Text style={[s.link, { color: t.primary }]}>‹ 問題一覧に戻る</Text>
            </Pressable>
            <ScrollView ref={scroller} contentContainerStyle={s.content}>
              <Text style={[s.heading, { color: t.text }]}>問{entry.officialNumber}　{entry.title}</Text>
              <Text style={[s.subject, { color: t.sub }]}>{entry.kind}</Text>
              <View style={[s.card, { backgroundColor: t.card, borderColor: t.border }]}>
                <RichText text={entry.question} color={t.text} fontSize={17} scroll scrollOnlyOverflow bg={t.card} />
                {!locked && (entry.questionImages ?? []).map((image) => (
                  <Pressable key={image.key} accessibilityRole="button" accessibilityLabel="設問図を拡大"
                    onPress={() => setZoom(image)} style={s.image}>
                    <Image source={figureSource(image.key)} style={{ width: '100%', aspectRatio: image.width / image.height }} resizeMode="contain" />
                    <Text style={[s.subject, { color: t.primary }]}>タップして拡大{image.page ? ' · ' + image.page : ''}</Text>
                  </Pressable>
                ))}
              </View>
              <Pressable accessibilityRole="button" onPress={locked ? purchase : () => setShowExplanation((v) => !v)}
                style={[s.answerButton, { borderColor: t.primary }]}>
                <Text style={[s.launchText, { color: t.primary }]}>{locked ? '購入して説明を見る'
                  : showExplanation ? '説明を隠す' : '説明を見る'}</Text>
              </Pressable>
              {showExplanation && !locked && <View style={[s.card, { backgroundColor: t.card, borderColor: t.border }]}>
                <Text style={[s.heading, { color: t.text }]}>{entry.source.kind === 'verbatim' ? '公式の説明（原文）' : '公式資料の抽出テキスト（要約を含む）'}</Text>
                {!!entry.explanation && <RichText text={entry.explanation} color={t.text} fontSize={17} scroll scrollOnlyOverflow bg={t.card} />}
                {(entry.explanationImages ?? []).map((image) => (
                  <Pressable key={image.key} accessibilityRole="button" accessibilityLabel="公式の説明を拡大"
                    onPress={() => setZoom(image)} style={s.image}>
                    <Image source={figureSource(image.key)} style={{ width: '100%', aspectRatio: image.width / image.height }} resizeMode="contain" />
                    <Text style={[s.subject, { color: t.primary }]}>タップして拡大{image.page ? ' · ' + image.page : ''}</Text>
                  </Pressable>
                ))}
                <Text style={[s.subject, { color: t.sub }]}>{entry.source.label}</Text>
              </View>}
              <View style={s.navigation}>
                <Pressable disabled={index === 0} accessibilityRole="button"
                  onPress={() => setSelectedId(entries[index - 1].id)} style={[s.navButton, { opacity: index === 0 ? 0.35 : 1 }]}>
                  <Text style={[s.link, { color: t.primary }]}>‹ 前へ</Text>
                </Pressable>
                <Text style={{ color: t.sub }}>{index + 1} / {entries.length}</Text>
                <Pressable disabled={index === entries.length - 1} accessibilityRole="button"
                  onPress={() => setSelectedId(entries[index + 1].id)} style={[s.navButton, { opacity: index === entries.length - 1 ? 0.35 : 1 }]}>
                  <Text style={[s.link, { color: t.primary }]}>次へ ›</Text>
                </Pressable>
              </View>
            </ScrollView>
          </> : <ScrollView contentContainerStyle={s.content}>
            {entries.some((e) => e.source.kind === 'extracted') && <Text style={[s.subject, { color: t.sub }]}>保存済みの公式資料から拾った復習候補です。説明には要約を含み、公式原文との照合・全件の確認は未完了です。</Text>}
            {entries.length === 0 && <Text style={[s.paragraph, { color: t.text }]}>{contentReady
              ? 'この範囲には復習候補がまだ登録されていません。記述式問題がないと確認したものではありません。'
              : '記述式の復習データがまだ登録されていません。'}</Text>}
            {entries.map((e, i) => <View key={e.id}>
              {(i === 0 || entries[i - 1].chapter !== e.chapter) && <Text style={[s.chapter, { color: t.sub }]}>第{e.chapter}章</Text>}
              <Pressable accessibilityRole="button" onPress={() => setSelectedId(e.id)}
                style={[s.card, { backgroundColor: t.card, borderColor: t.border }]}>
                <Text style={[s.itemTitle, { color: t.text }]}>問{e.officialNumber}　{e.title} ›</Text>
                <Text style={[s.subject, { color: t.sub }]}>{e.kind}</Text>
              </Pressable>
            </View>)}
          </ScrollView>}
        </SafeAreaView>
        <OriginalImageZoom image={zoom} onClose={() => setZoom(null)} t={t} />
      </Modal>
    </>
  );
}

const s = StyleSheet.create({
  screen: { flex: 1 }, flex: { flex: 1 },
  launch: { marginTop: 16, padding: 14, borderRadius: 12, borderWidth: 1, backgroundColor: '#0E1728' },
  launchText: { fontSize: 16, fontWeight: '700', textAlign: 'center' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 16, borderBottomWidth: 1 },
  heading: { fontSize: 19, fontWeight: '700', lineHeight: 28 }, link: { fontSize: 16, fontWeight: '600' },
  close: { minHeight: 44, padding: 12, justifyContent: 'center' },
  subject: { fontSize: 13, lineHeight: 21, marginTop: 6, marginHorizontal: 2 },
  back: { paddingHorizontal: 16, paddingVertical: 12 }, content: { padding: 16, paddingBottom: 32 },
  card: { borderRadius: 14, padding: 16, borderWidth: 1, marginVertical: 8, gap: 12 },
  chapter: { fontSize: 16, fontWeight: '700', marginTop: 18, marginBottom: 4 },
  itemTitle: { fontSize: 17, fontWeight: '600', lineHeight: 26 },
  answerButton: { padding: 14, borderRadius: 12, borderWidth: 1, marginVertical: 12 },
  paragraph: { fontSize: 17, lineHeight: 27, margin: 16 },
  image: { marginTop: 8 }, navigation: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: 20 },
  navButton: { padding: 12, minHeight: 44 },
});
