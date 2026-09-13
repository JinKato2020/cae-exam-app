import { useEffect, useMemo, useState } from 'react';
import {
  Alert,
  Image,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  useColorScheme,
  View,
  type DimensionValue,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import {
  SafeAreaProvider,
  SafeAreaView,
  useSafeAreaInsets,
} from 'react-native-safe-area-context';

import type { Question } from './src/types';
import { FIGURES, FIGURE_ASPECT } from './src/figures';
import { RichText } from './src/MathText';
import { CATALOG, questionsByIds, type ChapterEntry } from './src/catalog';
import { formulaDoc, type FormulaItem } from './src/formulas';
import {
  chapterStats,
  loadProgress,
  overallStat,
  recordAnswer,
  resetProgress,
  wrongIdsFrom,
  type ProgressMap,
} from './src/progress';

const APP_VERSION = '1.0.0';

// 課程（分野＋級）。固体2級・固体1級のみ表示。他分野はまだ無いので出さない。
function solid2Chapters(): ChapterEntry[] {
  const solid = CATALOG.find((f) => f.id === 'solid');
  const g2 = solid?.grades.find((g) => g.id === 'g2');
  return g2?.chapters ?? [];
}
type Course = { id: string; name: string; chapters: ChapterEntry[]; ready: boolean };
const COURSES: Course[] = [
  { id: 'solid-2', name: '固体力学 2級', chapters: solid2Chapters(), ready: true },
  { id: 'solid-1', name: '固体力学 1級', chapters: [], ready: false },
];

type Tab = 'home' | 'study' | 'formula' | 'settings';
type StudyView = 'course' | 'chapters' | 'tiles' | 'problem';
type FormulaView = 'chapters' | 'titles' | 'item';

export default function App() {
  return (
    <SafeAreaProvider>
      <AppInner />
    </SafeAreaProvider>
  );
}

function AppInner() {
  const scheme = useColorScheme();
  const t = scheme === 'dark' ? dark : light;
  const insets = useSafeAreaInsets();

  const [tab, setTab] = useState<Tab>('home');
  const [progress, setProgress] = useState<ProgressMap>({});

  // 問題タブのサブ画面状態
  const [studyView, setStudyView] = useState<StudyView>('course');
  const [course, setCourse] = useState<Course | null>(null);
  const [chapter, setChapter] = useState<ChapterEntry | null>(null);
  // 出題中のリスト（章の全問 or 復習リスト）と現在位置
  const [activeList, setActiveList] = useState<Question[]>([]);
  const [activeTitle, setActiveTitle] = useState('');
  const [qIndex, setQIndex] = useState(0);
  // 出題セッション内の選択（問題ID → 選んだ番号）。前後移動しても選択が残る。
  const [answers, setAnswers] = useState<Record<string, number>>({});

  // 公式・用語タブ（章 → タイトル一覧 → 個別解説）
  const [formulaView, setFormulaView] = useState<FormulaView>('chapters');
  const [formulaChapterId, setFormulaChapterId] = useState<string | null>(null);
  const [formulaItemId, setFormulaItemId] = useState<string | null>(null);

  useEffect(() => {
    loadProgress().then(setProgress);
  }, []);

  const wrongIds = useMemo(() => wrongIdsFrom(progress), [progress]);
  const wrongQuestions = useMemo(() => questionsByIds(wrongIds), [wrongIds]);

  // 出題を開始（章 or 復習）。startIndex から表示。
  function openProblems(list: Question[], title: string, startIndex = 0) {
    if (list.length === 0) return;
    setActiveList(list);
    setActiveTitle(title);
    setQIndex(Math.min(Math.max(startIndex, 0), list.length - 1));
    setAnswers({});
    setStudyView('problem');
    setTab('study');
  }

  async function onSelectAnswer(q: Question, choiceNum: number) {
    if (answers[q.id] != null) return; // 既に回答済みなら無視
    setAnswers((a) => ({ ...a, [q.id]: choiceNum }));
    const next = await recordAnswer(progress, q.id, choiceNum === q.answer);
    setProgress(next);
  }

  return (
    <View style={[styles.container, { backgroundColor: t.bg }]}>
      <StatusBar style={scheme === 'dark' ? 'light' : 'dark'} />
      <SafeAreaView style={{ flex: 1 }} edges={['top', 'left', 'right']}>
        {tab === 'home' && (
          <HomeTab
            t={t}
            progress={progress}
            wrongCount={wrongQuestions.length}
            onReview={() => openProblems(wrongQuestions, '間違い復習')}
            onGoStudy={() => {
              setStudyView('course');
              setTab('study');
            }}
          />
        )}

        {tab === 'study' && (
          <StudyTab
            t={t}
            view={studyView}
            course={course}
            chapter={chapter}
            activeList={activeList}
            activeTitle={activeTitle}
            qIndex={qIndex}
            answers={answers}
            progress={progress}
            onPickCourse={(c) => {
              setCourse(c);
              setChapter(null);
              setStudyView('chapters');
            }}
            onPickChapter={(c) => {
              setChapter(c);
              setStudyView('tiles');
            }}
            onPickTile={(i) =>
              openProblems(chapter?.data.questions ?? [], chapter?.title ?? '', i)
            }
            onSelectAnswer={onSelectAnswer}
            setQIndex={setQIndex}
            goBack={(v) => setStudyView(v)}
          />
        )}

        {tab === 'formula' && (
          <FormulaTab
            t={t}
            view={formulaView}
            chapterId={formulaChapterId}
            itemId={formulaItemId}
            onOpenChapter={(id) => {
              setFormulaChapterId(id);
              setFormulaView('titles');
            }}
            onOpenItem={(itemId) => {
              setFormulaItemId(itemId);
              setFormulaView('item');
            }}
            onBack={(v) => setFormulaView(v)}
          />
        )}

        {tab === 'settings' && (
          <SettingsTab
            t={t}
            progress={progress}
            onReset={async () => {
              const cleared = await resetProgress();
              setProgress(cleared);
            }}
          />
        )}
      </SafeAreaView>

      <TabBar t={t} tab={tab} insetsBottom={insets.bottom} onChange={setTab} />
    </View>
  );
}

// ================= ボトムナビ =================
function TabBar(props: {
  t: Theme;
  tab: Tab;
  insetsBottom: number;
  onChange: (tab: Tab) => void;
}) {
  const { t } = props;
  const items: { key: Tab; label: string }[] = [
    { key: 'home', label: 'ホーム' },
    { key: 'study', label: '問題' },
    { key: 'formula', label: '公式・用語' },
    { key: 'settings', label: '設定' },
  ];
  return (
    <View
      style={[
        styles.tabBar,
        { backgroundColor: t.card, borderColor: t.border, paddingBottom: Math.max(props.insetsBottom, 8) },
      ]}
    >
      {items.map((it) => {
        const active = props.tab === it.key;
        const c = active ? t.primary : t.sub;
        return (
          <Pressable key={it.key} style={styles.tabItem} onPress={() => props.onChange(it.key)}>
            <View style={styles.tabIconBox}>
              <TabIcon tab={it.key} color={c} bg={t.card} />
            </View>
            <Text style={[styles.tabLabel, { color: c }]}>{it.label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

// ミニマルな線だけのアイコン（絵文字不使用・新ライブラリ不要・テーマ色に追従）
function TabIcon(props: { tab: Tab; color: string; bg: string }) {
  const c = props.color;
  if (props.tab === 'home') {
    // 家
    return (
      <View style={icon.box}>
        <View
          style={{
            width: 0,
            height: 0,
            borderLeftWidth: 8,
            borderRightWidth: 8,
            borderBottomWidth: 8,
            borderLeftColor: 'transparent',
            borderRightColor: 'transparent',
            borderBottomColor: c,
          }}
        />
        <View style={{ width: 13, height: 8, borderWidth: 2, borderTopWidth: 0, borderColor: c }} />
      </View>
    );
  }
  if (props.tab === 'study') {
    // 問題用紙（枠＋2本線）
    return (
      <View style={icon.box}>
        <View
          style={{
            width: 15,
            height: 19,
            borderWidth: 2,
            borderColor: c,
            borderRadius: 3,
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <View style={{ width: 8, height: 2, backgroundColor: c, marginBottom: 3 }} />
          <View style={{ width: 8, height: 2, backgroundColor: c }} />
        </View>
      </View>
    );
  }
  if (props.tab === 'formula') {
    // 本（枠＋背表紙の線）
    return (
      <View style={icon.box}>
        <View style={{ width: 17, height: 16, borderWidth: 2, borderColor: c, borderRadius: 2 }} />
        <View style={{ position: 'absolute', width: 2, height: 12, backgroundColor: c }} />
      </View>
    );
  }
  // 設定（スライダー：3本線＋つまみ）
  const Row = ({ side }: { side: 'l' | 'r' }) => (
    <View style={{ width: 20, height: 6, justifyContent: 'center', marginVertical: 1.5 }}>
      <View style={{ position: 'absolute', left: 0, right: 0, height: 2, backgroundColor: c }} />
      <View
        style={[
          { position: 'absolute', width: 7, height: 7, borderRadius: 4, borderWidth: 2, borderColor: c, backgroundColor: props.bg },
          side === 'l' ? { left: 3 } : { right: 3 },
        ]}
      />
    </View>
  );
  return (
    <View style={icon.box}>
      <Row side="r" />
      <Row side="l" />
      <Row side="r" />
    </View>
  );
}

const icon = StyleSheet.create({
  box: { width: 24, height: 24, alignItems: 'center', justifyContent: 'center' },
});

// ================= ホーム / 分析 =================
function HomeTab(props: {
  t: Theme;
  progress: ProgressMap;
  wrongCount: number;
  onReview: () => void;
  onGoStudy: () => void;
}) {
  const { t } = props;
  const overall = useMemo(() => overallStat(props.progress), [props.progress]);
  const stats = useMemo(() => chapterStats(props.progress), [props.progress]);
  const attemptedStats = stats.filter((s) => s.attempted > 0);
  const weak = [...attemptedStats].sort((a, b) => a.accuracy - b.accuracy).slice(0, 3);
  const strong = [...attemptedStats].sort((a, b) => b.accuracy - a.accuracy).slice(0, 3);

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>学習の記録</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>固体力学 2級</Text>

      {/* 全体サマリ */}
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <View style={styles.summaryRow}>
          <Summary t={t} label="挑戦した問題" value={`${overall.attempted} / ${overall.totalQuestions}`} />
          <Summary t={t} label="正答率" value={`${Math.round(overall.accuracy * 100)}%`} />
          <Summary t={t} label="要復習" value={`${props.wrongCount} 問`} />
        </View>
      </View>

      {props.wrongCount > 0 && (
        <Button t={t} kind="review" label={`間違いだけ復習（${props.wrongCount} 問）`} onPress={props.onReview} />
      )}

      {overall.attempted === 0 && (
        <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
          <Text style={[styles.bodyText, { color: t.sub }]}>
            まだ記録がありません。「問題」タブから章を選んで解いてみましょう。
          </Text>
          <Button t={t} kind="primary" label="問題を解きに行く" onPress={props.onGoStudy} />
        </View>
      )}

      {/* 苦手・得意 */}
      {weak.length > 0 && (
        <>
          <Text style={[styles.sectionHead, { color: t.text }]}>苦手な章（優先復習）</Text>
          {weak.map((s) => (
            <RankRow key={s.id} t={t} stat={s} tone="weak" />
          ))}
          <Text style={[styles.sectionHead, { color: t.text }]}>得意な章</Text>
          {strong.map((s) => (
            <RankRow key={s.id} t={t} stat={s} tone="strong" />
          ))}
        </>
      )}

      {/* 章別 正答率バー */}
      <Text style={[styles.sectionHead, { color: t.text }]}>章別の正答率</Text>
      {stats.map((s) => (
        <View key={s.id} style={[styles.card, { backgroundColor: t.card, borderColor: t.border, marginBottom: 8 }]}>
          <View style={styles.barHeadRow}>
            <Text style={[styles.barTitle, { color: t.text }]} numberOfLines={1}>
              {s.title}
            </Text>
            <Text style={[styles.barPct, { color: t.sub }]}>
              {s.attempted > 0 ? `${Math.round(s.accuracy * 100)}%` : '未挑戦'}
            </Text>
          </View>
          <ProgressBar t={t} accuracy={s.accuracy} attempted={s.attempted} />
          <Text style={[styles.barSub, { color: t.sub }]}>
            {s.attempted} / {s.total} 問挑戦・{s.correct} 問正解
          </Text>
        </View>
      ))}
    </ScrollView>
  );
}

function Summary(props: { t: Theme; label: string; value: string }) {
  const { t } = props;
  return (
    <View style={styles.summaryItem}>
      <Text style={[styles.summaryValue, { color: t.text }]}>{props.value}</Text>
      <Text style={[styles.summaryLabel, { color: t.sub }]}>{props.label}</Text>
    </View>
  );
}

function RankRow(props: { t: Theme; stat: ReturnType<typeof chapterStats>[number]; tone: 'weak' | 'strong' }) {
  const { t, stat } = props;
  const color = props.tone === 'weak' ? t.wrong : t.correct;
  return (
    <View style={[styles.rankRow, { backgroundColor: t.card, borderColor: t.border }]}>
      <Text style={[styles.rankTitle, { color: t.text }]} numberOfLines={1}>
        {stat.title}
      </Text>
      <Text style={[styles.rankPct, { color }]}>{Math.round(stat.accuracy * 100)}%</Text>
    </View>
  );
}

function ProgressBar(props: { t: Theme; accuracy: number; attempted: number }) {
  const { t } = props;
  const pct = Math.round(props.accuracy * 100);
  const color =
    props.attempted === 0 ? t.border : pct >= 80 ? t.correct : pct >= 50 ? t.amber : t.wrong;
  const w = `${Math.max(pct, props.attempted > 0 ? 4 : 0)}%` as DimensionValue;
  return (
    <View style={[styles.barTrack, { backgroundColor: t.bg, borderColor: t.border }]}>
      <View style={[styles.barFill, { width: w, backgroundColor: color }]} />
    </View>
  );
}

// ================= 問題タブ =================
function StudyTab(props: {
  t: Theme;
  view: StudyView;
  course: Course | null;
  chapter: ChapterEntry | null;
  activeList: Question[];
  activeTitle: string;
  qIndex: number;
  answers: Record<string, number>;
  progress: ProgressMap;
  onPickCourse: (c: Course) => void;
  onPickChapter: (c: ChapterEntry) => void;
  onPickTile: (i: number) => void;
  onSelectAnswer: (q: Question, n: number) => void;
  setQIndex: (i: number) => void;
  goBack: (v: StudyView) => void;
}) {
  const { t } = props;

  // 課程選択
  if (props.view === 'course') {
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={[styles.title, { color: t.text }]}>問題</Text>
        <Text style={[styles.subtitle, { color: t.sub }]}>学習する課程を選んでください</Text>
        {COURSES.map((c) => (
          <Pressable
            key={c.id}
            onPress={c.ready ? () => props.onPickCourse(c) : undefined}
            style={[styles.row, { backgroundColor: t.card, borderColor: t.border, opacity: c.ready ? 1 : 0.5 }]}
          >
            <Text style={[styles.rowLabel, { color: t.text }]}>{c.name}</Text>
            <Text style={[styles.rowSub, { color: c.ready ? t.sub : t.wrong }]}>
              {c.ready ? `全 ${c.chapters.length} 章` : '準備中'}
            </Text>
          </Pressable>
        ))}
      </ScrollView>
    );
  }

  // 章の目次
  if (props.view === 'chapters' && props.course) {
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <BackLink t={t} label="課程を選び直す" onPress={() => props.goBack('course')} />
        <Text style={[styles.title, { color: t.text }]}>{props.course.name}</Text>
        <Text style={[styles.subtitle, { color: t.sub }]}>章を選んでください（全13章）</Text>
        {props.course.chapters.map((c) => {
          const ids = c.data.questions.map((q) => q.id);
          const done = ids.filter((id) => props.progress[id]).length;
          return (
            <Pressable
              key={c.id}
              onPress={() => props.onPickChapter(c)}
              style={[styles.row, { backgroundColor: t.card, borderColor: t.border }]}
            >
              <Text style={[styles.rowLabel, { color: t.text }]}>{c.title}</Text>
              <Text style={[styles.rowSub, { color: t.sub }]}>
                {c.data.questions.length} 問　・　{done > 0 ? `${done} 問挑戦済` : '未挑戦'}
              </Text>
            </Pressable>
          );
        })}
      </ScrollView>
    );
  }

  // タイル一覧
  if (props.view === 'tiles' && props.chapter) {
    const qs = props.chapter.data.questions;
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <BackLink t={t} label="章の目次へ" onPress={() => props.goBack('chapters')} />
        <Text style={[styles.title, { color: t.text }]}>{props.chapter.title}</Text>
        <Text style={[styles.subtitle, { color: t.sub }]}>
          問題を選ぶ（緑=正解／赤=不正解／灰=未挑戦）
        </Text>
        <Button
          t={t}
          kind="primary"
          label={`最初から順に解く（全 ${qs.length} 問）`}
          onPress={() => props.onPickTile(0)}
        />
        <View style={styles.tileGrid}>
          {qs.map((q, i) => {
            const p = props.progress[q.id];
            const tone = !p ? 'none' : p.lastCorrect ? 'correct' : 'wrong';
            const bg = tone === 'correct' ? t.correctBg : tone === 'wrong' ? t.wrongBg : t.card;
            const bd = tone === 'correct' ? t.correct : tone === 'wrong' ? t.wrong : t.border;
            return (
              <Pressable
                key={q.id}
                onPress={() => props.onPickTile(i)}
                style={[styles.tile, { backgroundColor: bg, borderColor: bd }]}
              >
                <Text style={[styles.tileNum, { color: t.text }]}>{q.number}</Text>
                <Text style={[styles.tileTitle, { color: t.sub }]} numberOfLines={2}>
                  {q.title ?? q.topic ?? ''}
                </Text>
                <Text style={[styles.tileMeta, { color: p ? (p.lastCorrect ? t.correct : t.wrong) : t.sub }]}>
                  {p ? `${p.lastCorrect ? '◯' : '✕'} ${fmtDate(p.lastTs)}` : '—'}
                </Text>
              </Pressable>
            );
          })}
        </View>
      </ScrollView>
    );
  }

  // 1問表示（前後ナビ）
  if (props.view === 'problem' && props.activeList.length > 0) {
    const q = props.activeList[props.qIndex];
    return (
      <ProblemScreen
        t={t}
        title={props.activeTitle}
        q={q}
        index={props.qIndex}
        total={props.activeList.length}
        selected={props.answers[q.id] ?? null}
        onSelect={(n) => props.onSelectAnswer(q, n)}
        onPrev={() => props.setQIndex(Math.max(props.qIndex - 1, 0))}
        onNext={() => props.setQIndex(Math.min(props.qIndex + 1, props.activeList.length - 1))}
        onBack={() => props.goBack(props.chapter ? 'tiles' : 'course')}
      />
    );
  }

  return null;
}

function ProblemScreen(props: {
  t: Theme;
  title: string;
  q: Question;
  index: number;
  total: number;
  selected: number | null;
  onSelect: (n: number) => void;
  onPrev: () => void;
  onNext: () => void;
  onBack: () => void;
}) {
  const { t, q, selected } = props;
  const answered = selected !== null;
  const isCorrect = selected === q.answer;
  const atFirst = props.index === 0;
  const atLast = props.index === props.total - 1;

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <BackLink t={t} label="一覧へ戻る" onPress={props.onBack} />
      <Text style={[styles.progress, { color: t.sub }]}>
        {props.title}　{props.index + 1} / {props.total}
        {q.title ? `　・　${q.title}` : ''}
      </Text>
      <View style={{ marginBottom: 18 }}>
        <RichText text={q.question} color={t.text} fontSize={18} bold />
      </View>

      {q.choices.map((choice, i) => {
        const num = i + 1;
        const c = choiceColor(t, { num, answer: q.answer, selected, answered });
        return (
          <Pressable
            key={num}
            onPress={() => props.onSelect(num)}
            style={[styles.choice, { backgroundColor: c.bg, borderColor: c.border }]}
          >
            <RichText text={`${num}. ${choice}`} color={c.text} fontSize={16} />
          </Pressable>
        );
      })}

      {answered && (
        <View style={[styles.explainBox, { backgroundColor: t.card, borderColor: t.border }]}>
          <Text style={[styles.verdict, { color: isCorrect ? t.correct : t.wrong }]}>
            {isCorrect ? '◯ 正解' : '✕ 不正解'}（正解：{q.answer}）
          </Text>
          <RichText text={q.explanation} color={t.text} fontSize={14} />
          {q.figureImage && FIGURES[q.figureImage] ? <AutoFigure t={t} source={FIGURES[q.figureImage]} /> : null}
        </View>
      )}

      {/* 前へ / 次へ */}
      <View style={styles.navRow}>
        <NavButton t={t} label="‹ 前へ" disabled={atFirst} onPress={props.onPrev} />
        <NavButton t={t} label="次へ ›" disabled={atLast} onPress={props.onNext} />
      </View>
    </ScrollView>
  );
}

// ================= 公式・用語タブ =================
function FormulaTab(props: {
  t: Theme;
  view: FormulaView;
  chapterId: string | null;
  itemId: string | null;
  onOpenChapter: (id: string) => void;
  onOpenItem: (itemId: string) => void;
  onBack: (v: FormulaView) => void;
}) {
  const { t } = props;

  // 個別解説（タイトルをタップして飛んでくる画面）
  if (props.view === 'item' && props.chapterId && props.itemId) {
    const doc = formulaDoc(props.chapterId);
    const item = doc?.items.find((x) => x.id === props.itemId);
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <BackLink t={t} label="公式・用語の一覧へ" onPress={() => props.onBack('titles')} />
        {item ? (
          <FormulaCard t={t} item={item} />
        ) : (
          <Text style={[styles.bodyText, { color: t.sub }]}>項目が見つかりません。</Text>
        )}
      </ScrollView>
    );
  }

  // タイトル一覧（目次）
  if (props.view === 'titles' && props.chapterId) {
    const doc = formulaDoc(props.chapterId);
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <BackLink t={t} label="章の一覧へ" onPress={() => props.onBack('chapters')} />
        {doc ? (
          <>
            <Text style={[styles.title, { color: t.text }]}>{doc.title}</Text>
            <Text style={[styles.subtitle, { color: t.sub }]}>
              タイトルを選ぶと、その解説に移ります（全 {doc.items.length} 項目）
            </Text>
            {doc.items.map((it) => (
              <Pressable
                key={it.id}
                onPress={() => props.onOpenItem(it.id)}
                style={[styles.row, { backgroundColor: t.card, borderColor: t.border }]}
              >
                <View style={styles.titleRow}>
                  <View
                    style={[
                      styles.badge,
                      { backgroundColor: it.kind === 'formula' ? t.primary : t.reviewBtn, marginRight: 10 },
                    ]}
                  >
                    <Text style={styles.badgeText}>{it.kind === 'formula' ? '公式' : '用語'}</Text>
                  </View>
                  <Text style={[styles.rowLabel, { color: t.text, flex: 1 }]}>{it.term}</Text>
                  <Text style={[styles.chevron, { color: t.sub }]}>›</Text>
                </View>
              </Pressable>
            ))}
          </>
        ) : (
          <Text style={[styles.bodyText, { color: t.sub }]}>この章は準備中です。</Text>
        )}
      </ScrollView>
    );
  }

  // 章の一覧
  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>公式・用語</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>章を選ぶと、公式・用語のタイトル一覧が出ます</Text>
      {solid2Chapters().map((c) => {
        const doc = formulaDoc(c.id);
        const ready = !!doc;
        return (
          <Pressable
            key={c.id}
            onPress={ready ? () => props.onOpenChapter(c.id) : undefined}
            style={[styles.row, { backgroundColor: t.card, borderColor: t.border, opacity: ready ? 1 : 0.5 }]}
          >
            <Text style={[styles.rowLabel, { color: t.text }]}>{c.title}</Text>
            <Text style={[styles.rowSub, { color: ready ? t.sub : t.wrong }]}>
              {ready ? `${doc!.items.length} 項目` : '準備中'}
            </Text>
          </Pressable>
        );
      })}
    </ScrollView>
  );
}

function FormulaCard(props: { t: Theme; item: FormulaItem }) {
  const { t, item } = props;
  const badge = item.kind === 'formula' ? '公式' : '用語';
  const badgeColor = item.kind === 'formula' ? t.primary : t.reviewBtn;
  return (
    <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border, marginBottom: 12 }]}>
      <View style={styles.formulaHead}>
        <View style={[styles.badge, { backgroundColor: badgeColor }]}>
          <Text style={styles.badgeText}>{badge}</Text>
        </View>
        <Text style={[styles.formulaTerm, { color: t.text }]}>{item.term}</Text>
      </View>
      {item.formula ? (
        <View style={[styles.formulaBox, { backgroundColor: t.bg, borderColor: t.border }]}>
          <RichText text={displayMath(item.formula)} color={t.text} fontSize={18} bold />
        </View>
      ) : null}
      <RichText text={item.body} color={t.text} fontSize={14} />
      {item.example ? (
        <View style={[styles.exampleBox, { borderColor: t.border }]}>
          <Text style={[styles.exampleLabel, { color: t.primary }]}>数値例</Text>
          <RichText text={item.example} color={t.text} fontSize={14} />
        </View>
      ) : null}
      {item.figureImage && FIGURES[item.figureImage] ? <AutoFigure t={t} source={FIGURES[item.figureImage]} /> : null}
    </View>
  );
}

// ================= 設定タブ =================
function SettingsTab(props: { t: Theme; progress: ProgressMap; onReset: () => void }) {
  const { t } = props;
  const overall = overallStat(props.progress);

  function confirmReset() {
    Alert.alert('学習記録をリセット', '正誤や日付の記録をすべて消します。よろしいですか？（元に戻せません）', [
      { text: 'キャンセル', style: 'cancel' },
      { text: 'リセットする', style: 'destructive', onPress: props.onReset },
    ]);
  }

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>設定</Text>

      <Text style={[styles.sectionHead, { color: t.text }]}>アプリ情報</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <InfoRow t={t} label="バージョン" value={`v${APP_VERSION}`} />
        <InfoRow t={t} label="収録" value="固体力学 2級・全13章" />
        <InfoRow t={t} label="解いた問題" value={`${overall.attempted} / ${overall.totalQuestions} 問`} />
        <InfoRow t={t} label="外観" value="端末の設定に自動で追従（ライト/ダーク）" last />
      </View>

      <Text style={[styles.sectionHead, { color: t.text }]}>学習記録</Text>
      <Button t={t} kind="danger" label="学習記録をリセット" onPress={confirmReset} />

      <Text style={[styles.sectionHead, { color: t.text }]}>このアプリについて</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <Text style={[styles.bodyText, { color: t.sub }]}>
          計算力学技術者（CAE）試験の対策アプリです。収録している問題・解説はすべてオリジナルで作成しています。学習の記録は端末内にのみ保存され、外部には送信されません。
        </Text>
      </View>
    </ScrollView>
  );
}

function InfoRow(props: { t: Theme; label: string; value: string; last?: boolean }) {
  const { t } = props;
  return (
    <View style={[styles.infoRow, props.last ? null : { borderBottomWidth: 1, borderColor: t.border }]}>
      <Text style={[styles.infoLabel, { color: t.sub }]}>{props.label}</Text>
      <Text style={[styles.infoValue, { color: t.text }]}>{props.value}</Text>
    </View>
  );
}

// ================= 共通部品 =================
function BackLink(props: { t: Theme; label: string; onPress: () => void }) {
  return (
    <Pressable onPress={props.onPress} style={styles.back}>
      <Text style={[styles.backText, { color: props.t.primary }]}>‹ {props.label}</Text>
    </Pressable>
  );
}

// 図の幅は「コンテナの実測幅」を使う（Fabricで width:'100%'+aspectRatio が効かない対策）。
function AutoFigure(props: { t: Theme; source: any }) {
  const [figW, setFigW] = useState(0);
  return (
    <View
      style={styles.figureWrap}
      onLayout={(e) => {
        const w = e.nativeEvent.layout.width;
        if (w && Math.abs(w - figW) > 1) setFigW(w);
      }}
    >
      {figW > 0 ? (
        <Image
          source={props.source}
          style={[styles.figureImg, { width: figW, height: figW / FIGURE_ASPECT, borderColor: props.t.border }]}
          resizeMode="contain"
        />
      ) : null}
    </View>
  );
}

function NavButton(props: { t: Theme; label: string; disabled?: boolean; onPress: () => void }) {
  const { t } = props;
  return (
    <Pressable
      onPress={props.disabled ? undefined : props.onPress}
      style={[
        styles.navButton,
        { backgroundColor: props.disabled ? t.disabled : t.primary, borderColor: t.border },
      ]}
    >
      <Text style={[styles.buttonText, { color: props.disabled ? t.sub : '#ffffff' }]}>{props.label}</Text>
    </Pressable>
  );
}

function Button(props: {
  t: Theme;
  label: string;
  kind: 'primary' | 'review' | 'ghost' | 'danger';
  disabled?: boolean;
  onPress: () => void;
}) {
  const { t } = props;
  const base =
    props.kind === 'primary'
      ? t.primary
      : props.kind === 'review'
      ? t.reviewBtn
      : props.kind === 'danger'
      ? t.wrong
      : 'transparent';
  const bg = props.disabled ? t.disabled : base;
  const textColor = props.kind === 'ghost' ? t.sub : '#ffffff';
  return (
    <Pressable
      onPress={props.disabled ? undefined : props.onPress}
      style={[styles.button, { backgroundColor: bg, borderColor: t.border }]}
    >
      <Text style={[styles.buttonText, { color: props.disabled ? t.sub : textColor }]}>{props.label}</Text>
    </Pressable>
  );
}

function choiceColor(
  t: Theme,
  a: { num: number; answer: number; selected: number | null; answered: boolean }
) {
  if (!a.answered) return { bg: t.card, border: t.border, text: t.text };
  if (a.num === a.answer) return { bg: t.correctBg, border: t.correct, text: t.text };
  if (a.num === a.selected) return { bg: t.wrongBg, border: t.wrong, text: t.text };
  return { bg: t.card, border: t.border, text: t.sub };
}

function fmtDate(ts: number): string {
  const d = new Date(ts);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

// 公式は「ディスプレイ数式」（中央・大きめ）で表示したいので、
// インライン $...$ をブロック $$...$$ に変換する（問題文と同じKaTeX経路）。
function displayMath(s: string): string {
  const x = s.trim();
  if (x.startsWith('$$')) return x;
  if (x.startsWith('$') && x.endsWith('$') && x.length > 2) return `$$${x.slice(1, -1)}$$`;
  return x;
}

// ================= テーマ =================
type Theme = typeof light;
const light = {
  bg: '#ffffff',
  text: '#1a1a1a',
  sub: '#666666',
  card: '#f6f7f9',
  border: '#dfe3e8',
  primary: '#2563eb',
  reviewBtn: '#7c3aed',
  amber: '#f59e0b',
  disabled: '#c8ccd2',
  correct: '#16a34a',
  correctBg: '#e7f6ec',
  wrong: '#dc2626',
  wrongBg: '#fdeaea',
};
const dark: Theme = {
  bg: '#0f1115',
  text: '#f2f3f5',
  sub: '#9aa0a6',
  card: '#1a1d23',
  border: '#2a2e35',
  primary: '#3b82f6',
  reviewBtn: '#8b5cf6',
  amber: '#f59e0b',
  disabled: '#3a3f47',
  correct: '#22c55e',
  correctBg: '#132b1c',
  wrong: '#ef4444',
  wrongBg: '#2b1414',
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 16, paddingBottom: 32 },
  back: { paddingVertical: 6, marginBottom: 2 },
  backText: { fontSize: 15, fontWeight: '600' },
  title: { fontSize: 26, fontWeight: 'bold', marginBottom: 4 },
  subtitle: { fontSize: 14, marginBottom: 16 },
  sectionHead: { fontSize: 16, fontWeight: 'bold', marginTop: 18, marginBottom: 8 },
  bodyText: { fontSize: 14, lineHeight: 21 },
  card: { borderWidth: 1, borderRadius: 12, padding: 14, marginBottom: 10 },
  row: { borderWidth: 1, borderRadius: 10, padding: 16, marginBottom: 10 },
  rowLabel: { fontSize: 17, fontWeight: '600', lineHeight: 23 },
  rowSub: { fontSize: 13, marginTop: 4 },
  titleRow: { flexDirection: 'row', alignItems: 'center' },
  chevron: { fontSize: 22, marginLeft: 8, fontWeight: '400' },

  // 全体サマリ
  summaryRow: { flexDirection: 'row', justifyContent: 'space-between' },
  summaryItem: { flex: 1, alignItems: 'center' },
  summaryValue: { fontSize: 20, fontWeight: 'bold' },
  summaryLabel: { fontSize: 11, marginTop: 4, textAlign: 'center' },

  // ランキング
  rankRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 14,
    marginBottom: 8,
  },
  rankTitle: { fontSize: 15, fontWeight: '600', flex: 1, marginRight: 8 },
  rankPct: { fontSize: 16, fontWeight: 'bold' },

  // バー
  barHeadRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  barTitle: { fontSize: 14, fontWeight: '600', flex: 1, marginRight: 8 },
  barPct: { fontSize: 13, fontWeight: '600' },
  barTrack: { height: 10, borderRadius: 6, borderWidth: 1, overflow: 'hidden' },
  barFill: { height: '100%', borderRadius: 5 },
  barSub: { fontSize: 12, marginTop: 6 },

  // タイル
  tileGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', marginTop: 12 },
  tile: {
    width: '48%',
    borderWidth: 1.5,
    borderRadius: 10,
    padding: 12,
    marginBottom: 10,
    minHeight: 92,
  },
  tileNum: { fontSize: 15, fontWeight: 'bold' },
  tileTitle: { fontSize: 12, marginTop: 4, lineHeight: 16, minHeight: 32 },
  tileMeta: { fontSize: 12, marginTop: 6, fontWeight: '600' },

  // 出題
  progress: { fontSize: 13, marginBottom: 10 },
  choice: { borderWidth: 1.5, borderRadius: 10, padding: 14, marginBottom: 10 },
  explainBox: { borderWidth: 1, borderRadius: 10, padding: 14, marginTop: 6, marginBottom: 8 },
  verdict: { fontSize: 15, fontWeight: 'bold', marginBottom: 6 },
  navRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12, gap: 10 },
  navButton: {
    flex: 1,
    borderRadius: 10,
    paddingVertical: 15,
    alignItems: 'center',
    borderWidth: 1,
  },

  // 公式カード
  formulaHead: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  badge: { borderRadius: 6, paddingHorizontal: 8, paddingVertical: 3, marginRight: 8 },
  badgeText: { color: '#ffffff', fontSize: 12, fontWeight: 'bold' },
  formulaTerm: { fontSize: 17, fontWeight: 'bold', flex: 1 },
  formulaBox: { borderWidth: 1, borderRadius: 8, padding: 12, marginBottom: 10 },
  exampleBox: { borderLeftWidth: 3, borderRadius: 4, paddingLeft: 10, paddingVertical: 4, marginTop: 10 },
  exampleLabel: { fontSize: 12, fontWeight: 'bold', marginBottom: 2 },

  // 設定
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  infoLabel: { fontSize: 14 },
  infoValue: { fontSize: 14, fontWeight: '600', flexShrink: 1, textAlign: 'right', marginLeft: 12 },

  // 図
  figureImg: { borderWidth: 1, borderRadius: 8, backgroundColor: '#ffffff' },
  figureWrap: { marginTop: 10, width: '100%' },

  // ボタン
  button: { borderRadius: 10, paddingVertical: 15, alignItems: 'center', marginTop: 10, borderWidth: 1 },
  buttonText: { fontSize: 16, fontWeight: 'bold' },

  // ボトムナビ
  tabBar: {
    flexDirection: 'row',
    borderTopWidth: 1,
    paddingTop: 8,
  },
  tabItem: { flex: 1, alignItems: 'center' },
  tabIconBox: { height: 24, justifyContent: 'center', alignItems: 'center' },
  tabLabel: { fontSize: 11, marginTop: 3, fontWeight: '600' },
});
