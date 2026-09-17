import { useEffect, useMemo, useState } from 'react';
import {
  Alert,
  Image,
  Linking,
  Pressable,
  ScrollView,
  StyleSheet,
  Switch,
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
import AsyncStorage from '@react-native-async-storage/async-storage';

import type { Question } from './src/types';
import { FIGURES, FIGURE_ASPECT } from './src/figures';
import { RichText } from './src/MathText';
import { CATALOG, questionsByIds, type ChapterEntry } from './src/catalog';
import { formulaDoc, type FormulaItem } from './src/formulas';
import Svg, { Circle, Line, Polygon, Text as SvgText } from 'react-native-svg';
import {
  chapterStats,
  fieldStats,
  loadProgress,
  overallStat,
  recordAnswer,
  resetProgress,
  resetDaily,
  wrongIdsFrom,
  snapshotFields,
  loadFieldSnaps,
  fieldCompareFrom,
  type ProgressMap,
  type GradeId,
  type QProgress,
  type FieldSnapStore,
  type FieldCompare,
} from './src/progress';
import Paywall, { type PayTarget } from './src/pro/Paywall';
import { TERMS_URL, PRIVACY_URL } from './src/config/revenuecat';
import {
  loadProState,
  saveOwned,
  saveDevPro,
  hasAnyPurchase,
  isLocked,
  entOfQuestion,
  ENTITLEMENTS,
  FREE_PER_CHAPTER,
  DEFAULT_PRO_STATE,
  type ProState,
} from './src/pro/proState';
import { initPurchases, syncEntitlements, restore as restorePurchases } from './src/pro/purchases';

const APP_VERSION = '1.0.0';

// 課程（分野＋級）。固体2級・固体1級のみ表示。他分野はまだ無いので出さない。
function solidGradeChapters(gradeId: string): ChapterEntry[] {
  const solid = CATALOG.find((f) => f.id === 'solid');
  return solid?.grades.find((g) => g.id === gradeId)?.chapters ?? [];
}
const solid2Chapters = (): ChapterEntry[] => solidGradeChapters('g2');
const solid1Chapters = (): ChapterEntry[] => solidGradeChapters('g1');
type Course = { id: string; name: string; chapters: ChapterEntry[]; ready: boolean };
// 1級は完成した章だけ出す（他章は準備中）。章側の ready フラグで出し分ける。
// 問題 → その問題が属する買い切り(分野×級)。ロック中にタップされたら、その級のPaywallを開くため。
function payTargetOf(q: Question): PayTarget | null {
  const e = entOfQuestion(q.id);
  return e ? { key: e.key, title: e.title } : null;
}

const COURSES: Course[] = [
  { id: 'solid-2', name: '固体力学 2級', chapters: solid2Chapters(), ready: true },
  { id: 'solid-1', name: '固体力学 1級', chapters: solid1Chapters(), ready: true },
];

type Tab = 'home' | 'study' | 'formula' | 'settings';
type ThemePref = 'system' | 'light' | 'dark';
type StudyView = 'course' | 'chapters' | 'tiles' | 'problem';
type FormulaView = 'course' | 'chapters' | 'titles' | 'item';

export default function App() {
  return (
    <SafeAreaProvider>
      <AppInner />
    </SafeAreaProvider>
  );
}

const THEME_KEY = 'cae.theme'; // 'system' | 'light' | 'dark'
const HOME_GRADE_KEY = 'cae.homeGrade'; // ホームで前回開いた級 'g1' | 'g2'

function AppInner() {
  const systemScheme = useColorScheme();
  // 外観の好み（システム追従／ライト固定／ダーク固定）。端末に保存。
  const [themePref, setThemePref] = useState<ThemePref>('system');
  const scheme = themePref === 'system' ? systemScheme : themePref;
  const t = scheme === 'dark' ? dark : light;
  const insets = useSafeAreaInsets();

  const [tab, setTab] = useState<Tab>('home');
  const [progress, setProgress] = useState<ProgressMap>({});

  // Pro（買い切り＝分野×級ごと）状態と購入画面の表示。target＝今売る級。
  const [proSt, setProSt] = useState<ProState>(DEFAULT_PRO_STATE);
  const [showPaywall, setShowPaywall] = useState(false);
  const [payTarget, setPayTarget] = useState<PayTarget | null>(null);

  // ロック中の問題／設定から購入画面を開く。target＝その級（無ければ最初の未購入級）。
  function openPaywall(target: PayTarget | null) {
    const fallback = ENTITLEMENTS.find((e) => !proSt.owned.includes(e.key)) ?? ENTITLEMENTS[0] ?? null;
    setPayTarget(target ?? (fallback ? { key: fallback.key, title: fallback.title } : null));
    setShowPaywall(true);
  }

  // 「購入を復元」：全級をまとめて復元し、端末に反映。
  async function restoreAll() {
    const owned = await restorePurchases();
    if (owned) {
      await saveOwned(owned);
      setProSt((s) => ({ ...s, owned }));
    }
    Alert.alert(
      owned && owned.length > 0 ? '購入を復元しました' : '復元できる購入がありません',
      owned && owned.length > 0 ? '購入済みの級が有効になりました。' : '同じApple IDで購入済みかご確認ください。',
    );
  }

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

  // 公式・用語タブ（課程 → 章 → タイトル一覧 → 個別解説）
  const [formulaView, setFormulaView] = useState<FormulaView>('course');
  const [formulaCourse, setFormulaCourse] = useState<Course | null>(null);
  const [formulaChapterId, setFormulaChapterId] = useState<string | null>(null);
  const [formulaItemId, setFormulaItemId] = useState<string | null>(null);

  useEffect(() => {
    loadProgress().then(async (p) => {
      setProgress(p);
      // 分野バランスを1日1回記録しておき、レーダーの「1週前比の成長」を出せるようにする。
      await snapshotFields(p, 'g2');
      await snapshotFields(p, 'g1');
    });
  }, []);

  // Proの初期化・同期。まず端末保存値を読み（オフラインでも即反映）、次にストアと同期して最新化。
  // キー未設定(src/config/revenuecat.ts が空)なら syncEntitlements は null＝状態を変えない＝アプリは従来どおり無料動作。
  useEffect(() => {
    (async () => {
      const local = await loadProState();
      setProSt(local);
      await initPurchases(null);
      const owned = await syncEntitlements();
      if (owned) {
        await saveOwned(owned);
        setProSt((s) => ({ ...s, owned }));
      }
    })();
  }, []);

  // 購入・復元の成功後に呼ぶ（保存はPaywall側で済んでいる）。端末値を読み直してPro反映＆画面を閉じる。
  async function onProUnlocked() {
    setProSt(await loadProState());
    setShowPaywall(false);
  }

  // 外観の好みを端末から復元。
  useEffect(() => {
    AsyncStorage.getItem(THEME_KEY)
      .then((v) => {
        if (v === 'light' || v === 'dark' || v === 'system') setThemePref(v);
      })
      .catch(() => {});
  }, []);

  function changeTheme(pref: ThemePref) {
    setThemePref(pref);
    AsyncStorage.setItem(THEME_KEY, pref).catch(() => {});
  }

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
            proState={proSt}
            onOpenPaywall={openPaywall}
          />
        )}

        {tab === 'formula' && (
          <FormulaTab
            t={t}
            view={formulaView}
            course={formulaCourse}
            chapterId={formulaChapterId}
            itemId={formulaItemId}
            onPickCourse={(c) => {
              setFormulaCourse(c);
              setFormulaView('chapters');
            }}
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
            owned={proSt.owned}
            devPro={proSt.devPro}
            onOpenPaywall={openPaywall}
            onRestoreAll={restoreAll}
            onToggleDevPro={async (on) => {
              await saveDevPro(on);
              setProSt((s) => ({ ...s, devPro: on }));
            }}
            themePref={themePref}
            onChangeTheme={changeTheme}
          />
        )}
      </SafeAreaView>

      <TabBar t={t} tab={tab} insetsBottom={insets.bottom} onChange={setTab} />

      {showPaywall && (
        <View style={StyleSheet.absoluteFill}>
          <Paywall t={t} target={payTarget} onClose={() => setShowPaywall(false)} onPurchased={onProUnlocked} />
        </View>
      )}
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
  // ホームの分析は級ごと。左=1級 / 右=2級。起動時は「前回開いた級」を復元（初回のみ2級）。
  const [grade, setGrade] = useState<GradeId>('g2');
  useEffect(() => {
    AsyncStorage.getItem(HOME_GRADE_KEY)
      .then((v) => {
        if (v === 'g1' || v === 'g2') setGrade(v);
      })
      .catch(() => {});
  }, []);
  function chooseGrade(g: GradeId) {
    setGrade(g);
    AsyncStorage.setItem(HOME_GRADE_KEY, g).catch(() => {});
  }
  const overall = useMemo(() => overallStat(props.progress, grade), [props.progress, grade]);
  const stats = useMemo(() => chapterStats(props.progress, grade), [props.progress, grade]);
  const fields = useMemo(() => fieldStats(props.progress, grade), [props.progress, grade]);
  // レーダーの「1週前比の成長」。端末に貯めた分野スナップショットと今を比べる。
  const [snaps, setSnaps] = useState<FieldSnapStore>([]);
  useEffect(() => {
    loadFieldSnaps().then(setSnaps);
  }, [props.progress]);
  const compare: FieldCompare = useMemo(
    () => fieldCompareFrom(snaps, fields, grade),
    [snaps, fields, grade]
  );
  const hasGrowth = Object.values(compare.growth).some((v) => v != null);
  const attemptedStats = stats.filter((s) => s.attempted > 0);
  const weak = [...attemptedStats].sort((a, b) => a.accuracy - b.accuracy).slice(0, 3);
  const strong = [...attemptedStats].sort((a, b) => b.accuracy - a.accuracy).slice(0, 3);

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>学習の記録</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>
        {grade === 'g1' ? '固体力学 1級' : '固体力学 2級'}
      </Text>

      {/* 級の切り替え（1級=左 / 2級=右） */}
      <View style={[styles.segment, { borderColor: t.border, backgroundColor: t.card }]}>
        {(['g1', 'g2'] as GradeId[]).map((g) => {
          const on = grade === g;
          return (
            <Pressable
              key={g}
              onPress={() => chooseGrade(g)}
              style={[styles.segmentItem, on && { backgroundColor: t.primary }]}
            >
              <Text style={[styles.segmentText, { color: on ? '#fff' : t.sub }]}>
                {g === 'g2' ? '2級' : '1級'}
              </Text>
            </Pressable>
          );
        })}
      </View>

      {/* 全体サマリ */}
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <View style={styles.summaryRow}>
          <Summary t={t} label="挑戦した問題" value={`${overall.attempted} / ${overall.totalQuestions}`} />
          <Summary t={t} label="正答率" value={`${Math.round(overall.accuracy * 100)}%`} />
          <Summary t={t} label="要復習" value={`${props.wrongCount} 問`} />
        </View>
      </View>

      {/* 5分野レーダー（正五角形） */}
      <Text style={[styles.sectionHead, { color: t.text }]}>分野別のバランス</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border, alignItems: 'center' }]}>
        <RadarChart t={t} fields={fields} baseAcc={compare.baseAcc} />
        <View style={styles.radarLegend}>
          {fields.map((f) => {
            const g = compare.growth[f.id];
            const gColor = g == null || g === 0 ? t.sub : g > 0 ? t.correct : t.wrong;
            const gText = g == null ? '' : g > 0 ? ` ▲+${g}` : g < 0 ? ` ▼${g}` : ' ±0';
            return (
              <Text key={f.id} style={[styles.radarLegendItem, { color: t.sub }]}>
                {f.id}：{f.label}（
                {f.attempted > 0 ? `${Math.round(f.accuracy * 100)}%` : '未挑戦'}）
                {gText ? <Text style={{ color: gColor, fontWeight: 'bold' }}>{gText}</Text> : null}
              </Text>
            );
          })}
        </View>
        {hasGrowth ? (
          <Text style={[styles.radarNote, { color: t.sub }]}>
            ▲▼ は1週間前との差（pt）。薄い五角形が1週間前の形。
          </Text>
        ) : (
          <Text style={[styles.radarNote, { color: t.sub }]}>
            続けて解くと、1週間前と比べた分野ごとの伸びがここに出ます。
          </Text>
        )}
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

      {/* 章別の正答率は「問題」タブの各章タイトル下へ移動（見やすさのため） */}
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

// 正五角形レーダー。5分野の正答率を頂点にプロットする。
// baseAcc があれば「約1週間前の形」を薄い五角形で重ねて、伸びを一目で見せる。
function RadarChart(props: {
  t: Theme;
  fields: ReturnType<typeof fieldStats>;
  baseAcc?: Record<string, number> | null;
}) {
  const { t, fields } = props;
  const N = fields.length; // 5
  const size = 250;
  const cx = size / 2;
  const cy = size / 2;
  const R = 82; // データ領域の最大半径
  const labelR = R + 22; // ラベルを外側に配置

  // 上（12時方向）から時計回りに配置
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / N;
  const at = (i: number, r: number) => ({
    x: cx + r * Math.cos(angle(i)),
    y: cy + r * Math.sin(angle(i)),
  });
  const poly = (r: number) =>
    fields.map((_, i) => { const p = at(i, r); return `${p.x},${p.y}`; }).join(' ');

  const grid = [0.25, 0.5, 0.75, 1]; // 目盛りの正五角形
  const dataPts = fields
    .map((f, i) => { const p = at(i, R * Math.max(0, Math.min(1, f.accuracy))); return `${p.x},${p.y}`; })
    .join(' ');
  const hasData = fields.some((f) => f.attempted > 0);
  // 約1週間前の形（薄い五角形）。基準がある分野だけ点を置く。
  const basePts =
    props.baseAcc &&
    fields.some((f) => props.baseAcc![f.id] != null)
      ? fields
          .map((f, i) => {
            const a = props.baseAcc![f.id];
            const p = at(i, R * Math.max(0, Math.min(1, a ?? 0)));
            return `${p.x},${p.y}`;
          })
          .join(' ')
      : null;

  return (
    <Svg width={size} height={size}>
      {/* 目盛りの正五角形 */}
      {grid.map((k) => (
        <Polygon key={k} points={poly(R * k)} fill="none" stroke={t.border} strokeWidth={1} />
      ))}
      {/* 約1週間前の形（薄い比較五角形） */}
      {basePts && (
        <Polygon points={basePts} fill="none" stroke={t.sub} strokeWidth={1.5} strokeDasharray="4 3" opacity={0.55} />
      )}
      {/* 中心からの軸線 */}
      {fields.map((_, i) => {
        const p = at(i, R);
        return <Line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke={t.border} strokeWidth={1} />;
      })}
      {/* データ多角形 */}
      {hasData && (
        <Polygon points={dataPts} fill={t.primary} fillOpacity={0.22} stroke={t.primary} strokeWidth={2} />
      )}
      {/* 各頂点の点 */}
      {hasData &&
        fields.map((f, i) => {
          const p = at(i, R * Math.max(0, Math.min(1, f.accuracy)));
          return <Circle key={i} cx={p.x} cy={p.y} r={3} fill={t.primary} />;
        })}
      {/* 頂点ラベル（分野記号） */}
      {fields.map((f, i) => {
        const p = at(i, labelR);
        return (
          <SvgText
            key={f.id}
            x={p.x}
            y={p.y}
            fill={t.sub}
            fontSize={12}
            fontWeight="bold"
            textAnchor="middle"
            alignmentBaseline="middle"
          >
            {f.id}
          </SvgText>
        );
      })}
    </Svg>
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
  proState: ProState;
  onOpenPaywall: (target: PayTarget | null) => void;
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
        <Text style={[styles.subtitle, { color: t.sub }]}>章を選んでください（全 {props.course.chapters.length} 章）</Text>
        {props.course.chapters.map((c) => {
          const ready = c.ready !== false && c.data.questions.length > 0;
          const ids = c.data.questions.map((q) => q.id);
          const done = ids.filter((id) => props.progress[id]).length;
          const correct = ids.filter((id) => props.progress[id]?.lastCorrect).length;
          const acc = done > 0 ? correct / done : 0;
          return (
            <Pressable
              key={c.id}
              onPress={ready ? () => props.onPickChapter(c) : undefined}
              style={[styles.row, { backgroundColor: t.card, borderColor: t.border, opacity: ready ? 1 : 0.5 }]}
            >
              <Text style={[styles.rowLabel, { color: t.text }]}>{c.title}</Text>
              <Text style={[styles.rowSub, { color: ready ? t.sub : t.wrong }]}>
                {ready ? `${c.data.questions.length} 問　・　${done > 0 ? `${done} 問挑戦済` : '未挑戦'}` : '準備中'}
              </Text>
              {ready && done > 0 && (
                <View style={{ marginTop: 8 }}>
                  <ProgressBar t={t} accuracy={acc} attempted={done} />
                  <Text style={[styles.barSub, { color: t.sub }]}>
                    正答率 {Math.round(acc * 100)}%　・　{correct} / {done} 問正解
                  </Text>
                </View>
              )}
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
                  {p
                    ? `${p.lastCorrect ? '◯' : '✕'} ${fmtDate(p.lastTs)}${p.attempts >= 2 ? ` ・${p.attempts}回` : ''}`
                    : '—'}
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
        past={props.progress[q.id]}
        index={props.qIndex}
        total={props.activeList.length}
        selected={props.answers[q.id] ?? null}
        onSelect={(n) => props.onSelectAnswer(q, n)}
        onPrev={() => props.setQIndex(Math.max(props.qIndex - 1, 0))}
        onNext={() => props.setQIndex(Math.min(props.qIndex + 1, props.activeList.length - 1))}
        onBack={() => props.goBack(props.chapter ? 'tiles' : 'course')}
        locked={isLocked(q, props.proState)}
        onOpenPaywall={() => props.onOpenPaywall(payTargetOf(q))}
      />
    );
  }

  return null;
}

function ProblemScreen(props: {
  t: Theme;
  title: string;
  q: Question;
  past?: QProgress;
  index: number;
  total: number;
  selected: number | null;
  onSelect: (n: number) => void;
  onPrev: () => void;
  onNext: () => void;
  onBack: () => void;
  locked: boolean;
  onOpenPaywall: () => void;
}) {
  const { t, q, selected, past } = props;
  const locked = props.locked;
  const answered = selected !== null;
  const isCorrect = selected === q.answer;
  const atFirst = props.index === 0;
  const atLast = props.index === props.total - 1;
  const pastRate = past && past.attempts > 0 ? Math.round((past.correctCount / past.attempts) * 100) : 0;

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <BackLink t={t} label="一覧へ戻る" onPress={props.onBack} />
      <Text style={[styles.progress, { color: t.sub }]}>
        {props.title}　{props.index + 1} / {props.total}
        {q.title ? `　・　${q.title}` : ''}
      </Text>
      {/* 過去の学習履歴（前回の正誤・回答日・挑戦回数・正答率） */}
      <Text style={[styles.historyLine, { color: t.sub }]}>
        学習履歴：
        {past ? (
          <Text style={{ color: past.lastCorrect ? t.correct : t.wrong, fontWeight: '600' }}>
            前回 {past.lastCorrect ? '◯' : '✕'}・{fmtDate(past.lastTs)}・{past.attempts}回挑戦（正答率 {pastRate}%）
          </Text>
        ) : (
          'まだ解いていません'
        )}
      </Text>
      {/* 公式標準問題との対応（§1.6・番号は対応学習用の参照。本アプリは非公認） */}
      {q.officialRef ? (
        <Text style={[styles.officialLine, { color: t.sub }]}>
          公式標準問題 {q.officialRef} に対応{q.role === 'branch' ? '（補足）' : ''}／本アプリは非公認の独自補助教材・番号は対応学習用の参照です
        </Text>
      ) : null}
      <View style={{ marginBottom: 18 }}>
        <RichText text={q.question} color={t.text} fontSize={18} bold />
      </View>

      {q.choices.map((choice, i) => {
        const num = i + 1;
        // ロック中は正誤の色分け（＝正解の露出）をしない。タップは購入導線へ。
        const c = locked
          ? choiceColor(t, { num, answer: -1, selected: null, answered: false })
          : choiceColor(t, { num, answer: q.answer, selected, answered });
        return (
          <Pressable
            key={num}
            onPress={() => (locked ? props.onOpenPaywall() : props.onSelect(num))}
            style={[styles.choice, { backgroundColor: c.bg, borderColor: c.border }]}
          >
            <RichText text={`${num}. ${choice}`} color={c.text} fontSize={16} />
          </Pressable>
        );
      })}

      {!locked && answered && (
        <View style={[styles.explainBox, { backgroundColor: t.card, borderColor: t.border }]}>
          <Text style={[styles.verdict, { color: isCorrect ? t.correct : t.wrong }]}>
            {isCorrect ? '◯ 正解' : '✕ 不正解'}（正解：{q.answer}）
          </Text>
          <RichText text={q.explanation} color={t.text} fontSize={14} />
          {q.figureImage && FIGURES[q.figureImage] ? <AutoFigure t={t} source={FIGURES[q.figureImage]} /> : null}
        </View>
      )}

      {locked && (
        <Pressable
          onPress={props.onOpenPaywall}
          style={[styles.lockBox, { backgroundColor: t.card, borderColor: t.primary }]}
        >
          <Text style={styles.lockEmoji}>🔒</Text>
          <Text style={[styles.lockTitle, { color: t.text }]}>この問題の正解・解説・図は買い切りで解除</Text>
          <Text style={[styles.lockSub, { color: t.sub }]}>
            各章の最初の{FREE_PER_CHAPTER}問は無料です。{FREE_PER_CHAPTER + 1}問目以降の答え合わせ・解説・図は、この級の買い切りで見られます（公式・用語は無料）。
          </Text>
          <View style={[styles.lockBtn, { backgroundColor: t.primary }]}>
            <Text style={styles.lockBtnTxt}>この級を解除する</Text>
          </View>
        </Pressable>
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
  course: Course | null;
  chapterId: string | null;
  itemId: string | null;
  onPickCourse: (c: Course) => void;
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

  // 章の一覧（選んだ課程の中）
  if (props.view === 'chapters' && props.course) {
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <BackLink t={t} label="課程を選び直す" onPress={() => props.onBack('course')} />
        <Text style={[styles.title, { color: t.text }]}>{props.course.name}</Text>
        <Text style={[styles.subtitle, { color: t.sub }]}>章を選ぶと、公式・用語のタイトル一覧が出ます</Text>
        {props.course.chapters.map((c) => {
          const fid = c.formulaId ?? c.id;
          const doc = formulaDoc(fid);
          const ready = !!doc && c.ready !== false;
          return (
            <Pressable
              key={c.id}
              onPress={ready ? () => props.onOpenChapter(fid) : undefined}
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

  // 課程の選択
  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>公式・用語</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>課程を選んでください</Text>
      {COURSES.map((c) => (
        <Pressable
          key={c.id}
          onPress={c.ready ? () => props.onPickCourse(c) : undefined}
          style={[styles.row, { backgroundColor: t.card, borderColor: t.border, opacity: c.ready ? 1 : 0.5 }]}
        >
          <Text style={[styles.rowLabel, { color: t.text }]}>{c.name}</Text>
          <Text style={[styles.rowSub, { color: c.ready ? t.sub : t.wrong }]}>{c.ready ? '公式・用語' : '準備中'}</Text>
        </Pressable>
      ))}
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
          {/* 公式は縮小せず文字サイズを揃える。長い式ではみ出す分は横スクロール（右端フェードで誘導） */}
          <RichText text={displayMath(item.formula)} color={t.text} fontSize={22} bold scroll bg={t.bg} />
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
function SettingsTab(props: {
  t: Theme;
  progress: ProgressMap;
  onReset: () => void;
  owned: string[];
  devPro: boolean;
  onOpenPaywall: (target: PayTarget | null) => void;
  onRestoreAll: () => void;
  onToggleDevPro: (on: boolean) => void;
  themePref: ThemePref;
  onChangeTheme: (p: ThemePref) => void;
}) {
  const { t } = props;
  // バージョン表示を7回タップで開発用ロック解除（Android風の隠しジェスチャ。TestFlightでも使える）。
  const [verTaps, setVerTaps] = useState(0);
  function onTapVersion() {
    const n = verTaps + 1;
    if (n >= 7) {
      setVerTaps(0);
      const next = !props.devPro;
      props.onToggleDevPro(next);
      Alert.alert('開発用ロック', next ? '解除しました（全問アンロック）。' : '元に戻しました（無料表示）。');
    } else {
      setVerTaps(n);
      if (n >= 4) Alert.alert('開発用ロック', `あと ${7 - n} 回タップで切り替わります。`);
    }
  }

  const themeOptions: { key: ThemePref; label: string }[] = [
    { key: 'system', label: 'システム' },
    { key: 'light', label: 'ライト' },
    { key: 'dark', label: 'ダーク' },
  ];

  function confirmReset() {
    Alert.alert('学習記録をリセット', '正誤や日付の記録をすべて消します。よろしいですか？（元に戻せません）', [
      { text: 'キャンセル', style: 'cancel' },
      { text: 'リセットする', style: 'destructive', onPress: props.onReset },
    ]);
  }

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>設定</Text>

      <Text style={[styles.sectionHead, { color: t.text }]}>外観</Text>
      <View style={[styles.segment, { borderColor: t.border }]}>
        {themeOptions.map((o) => {
          const on = props.themePref === o.key;
          return (
            <Pressable
              key={o.key}
              onPress={() => props.onChangeTheme(o.key)}
              style={[styles.segmentItem, on && { backgroundColor: t.primary }]}
            >
              <Text style={[styles.segmentText, { color: on ? '#fff' : t.sub }]}>{o.label}</Text>
            </Pressable>
          );
        })}
      </View>

      <Text style={[styles.sectionHead, { color: t.text }]}>買い切り（級ごと）</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        {ENTITLEMENTS.map((e, i) => {
          const owned = props.devPro || props.owned.includes(e.key);
          return (
            <View key={e.key}>
              <InfoRow
                t={t}
                label={e.title}
                value={owned ? '解除済み' : '未購入'}
                last={i === ENTITLEMENTS.length - 1}
              />
              {!owned ? (
                <Button
                  t={t}
                  kind="primary"
                  label={`${e.title}を購入する`}
                  onPress={() => props.onOpenPaywall({ key: e.key, title: e.title })}
                />
              ) : null}
            </View>
          );
        })}
      </View>
      <Button t={t} kind="ghost" label="購入を復元する" onPress={props.onRestoreAll} />

      <Text style={[styles.sectionHead, { color: t.text }]}>学習記録</Text>
      <Button t={t} kind="danger" label="学習記録をリセット" onPress={confirmReset} />

      <Text style={[styles.sectionHead, { color: t.text }]}>このアプリについて</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <Text style={[styles.bodyText, { color: t.sub }]}>
          計算力学技術者（CAE）試験の対策アプリです。収録している問題・解説はすべてオリジナルで作成しています。学習の記録は端末内に保存されます。ログインすると、記録が安全にクラウドへバックアップされ、機種変更や再インストールのあとでも引き継げます。
        </Text>
      </View>

      {/* 審査必須：利用規約・プライバシーポリシーへの導線（購入画面だけでなく設定からも常に到達可能に）。 */}
      <Text style={[styles.sectionHead, { color: t.text }]}>規約</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <Pressable onPress={() => Linking.openURL(TERMS_URL)} style={{ paddingVertical: 10 }} hitSlop={8}>
          <Text style={[styles.bodyText, { color: t.primary }]}>利用規約</Text>
        </Pressable>
        <View style={{ height: 1, backgroundColor: t.border }} />
        <Pressable onPress={() => Linking.openURL(PRIVACY_URL)} style={{ paddingVertical: 10 }} hitSlop={8}>
          <Text style={[styles.bodyText, { color: t.primary }]}>プライバシーポリシー</Text>
        </Pressable>
      </View>

      {/* 開発用：Proモード全解除(devPro)トグル。TestFlight/実機での動作確認用に常時表示している。
          ⚠️ App Store 公開版でも一般ユーザーに見えてしまうため、公開ビルド前に必ず除去または __DEV__ で囲い直すこと。
          （本番で隠したまま切り替えたいときは、最下部バージョンの7回タップの隠しジェスチャも併用可） */}
      <Text style={[styles.sectionHead, { color: t.text }]}>開発用</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <View style={styles.infoRow}>
          <Text style={[styles.infoLabel, { color: t.text }]}>Proモード全解除（devPro）</Text>
          <Switch
            value={props.devPro}
            onValueChange={props.onToggleDevPro}
            trackColor={{ true: t.primary, false: t.border }}
          />
        </View>
      </View>

      {/* 最下部のバージョン表示。7回タップで開発用ロック解除（隠しジェスチャ）。 */}
      <Pressable onPress={onTapVersion} style={styles.versionFooter} hitSlop={8}>
        <Text style={[styles.versionText, { color: t.sub }]}>
          CAE 固体力学　v{APP_VERSION}{props.devPro ? '　・　開発ロック解除中' : ''}
        </Text>
      </Pressable>
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
// 公式・用語タブの「主役の数式」を必ず $$…$$（大きい中央表示）に統一する。
//
// 長い公式は横に収まらないと右が切れる。ただ縮小すると 34% 等になって読めないので、
// できる限り「改行して縦に積む」ことで各行を短くし、原寸に近い大きさで読ませる：
//   ① 独立した複数式を区切る トップレベルの \quad / \qquad で分割
//   ② それでも長い行は トップレベルの + と（先頭以外の）= でさらに改行
// いずれも括弧・ブレースの深さ0だけが対象で、\left(…\right) や {…} の中は分割しない。
// ここまでやっても割れない単一の長大式だけ、最後に MathText 側の縮小で収める。

// 括弧/ブレース深さ0の \quad / \qquad で分割。
function splitTopQuad(inner: string): string[] {
  const parts: string[] = [];
  let depth = 0;
  let last = 0;
  for (let i = 0; i < inner.length; i++) {
    const c = inner[i];
    if (c === '\\') {
      const m = /^\\q?quad(?![a-zA-Z])/.exec(inner.slice(i));
      if (depth === 0 && m) {
        parts.push(inner.slice(last, i));
        i += m[0].length - 1;
        last = i + 1;
      } else {
        const nx = inner[i + 1]; // \{ \} \( \) \[ \] は括弧として深さに反映
        if (nx === '{' || nx === '(' || nx === '[') depth++;
        else if (nx === '}' || nx === ')' || nx === ']') depth = Math.max(0, depth - 1);
        i += 1; // 次の1文字を消費（\left \right \, なども1文字読み飛ばし）
      }
      continue;
    }
    if (c === '{' || c === '(' || c === '[') depth++;
    else if (c === '}' || c === ')' || c === ']') depth = Math.max(0, depth - 1);
  }
  parts.push(inner.slice(last));
  return parts.map((p) => p.trim()).filter((p) => p.length > 0);
}

// 1本の式を、括弧/ブレース深さ0の「+」と（先頭以外の）「=」の直前で改行して複数行に。
// 継続行は演算子始まり（+ や =）になる。分割点が無ければ元の1行を返す。
function breakAtOps(seg: string): string[] {
  const idx: number[] = [];
  let depth = 0;
  for (let i = 0; i < seg.length; i++) {
    const c = seg[i];
    if (c === '\\') { // \{ \} \( \) \[ \] は括弧として深さに反映。他は次の1文字を読み飛ばす
      const nx = seg[i + 1];
      if (nx === '{' || nx === '(' || nx === '[') depth++;
      else if (nx === '}' || nx === ')' || nx === ']') depth = Math.max(0, depth - 1);
      i += 1; continue;
    }
    if (c === '{' || c === '(' || c === '[') { depth++; continue; }
    if (c === '}' || c === ')' || c === ']') { depth = Math.max(0, depth - 1); continue; }
    if (depth !== 0) continue;
    if (c === '+' && i > 0) idx.push(i);
    else if (c === '=' && i > 8) idx.push(i); // 先頭付近の = (左辺が短い) は割らず「LHS=RHS」を保つ
  }
  if (idx.length === 0) return [seg];
  const lines: string[] = [];
  let start = 0;
  for (const p of idx) {
    if (p > start) lines.push(seg.slice(start, p));
    start = p;
  }
  lines.push(seg.slice(start));
  return lines.map((s) => s.trim()).filter((s) => s.length > 0);
}

function wrapLongDisplay(inner: string): string {
  if (inner.length < 50) return inner; // 短い式は現状どおり1行
  const lines: string[] = [];
  for (const seg of splitTopQuad(inner)) {
    if (seg.length >= 60) lines.push(...breakAtOps(seg));
    else lines.push(seg);
  }
  if (lines.length <= 1) return inner; // 割れない→縮小に任せる
  return `\\begin{gather*}${lines.join(' \\\\ ')}\\end{gather*}`;
}

function displayMath(s: string): string {
  const x = s.trim();
  let inner: string;
  if (x.startsWith('$$') && x.endsWith('$$') && x.length > 4) inner = x.slice(2, -2);
  // 全体が単一の $…$（途中に区切りの $ を含まない）
  else if (x.startsWith('$') && x.endsWith('$') && x.length > 2 && x.slice(1, -1).indexOf('$') === -1)
    inner = x.slice(1, -1);
  // $ を全く含まない素の数式テキスト
  else if (x.indexOf('$') === -1 && x.length > 0) inner = x;
  else return x; // $ を途中に含む複合テキストは触らない
  return `$$${wrapLongDisplay(inner)}$$`;
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
  // 級切り替えのセグメント（2級 / 1級）
  segment: { flexDirection: 'row', borderWidth: 1, borderRadius: 10, padding: 3, marginBottom: 16 },
  segmentItem: { flex: 1, paddingVertical: 8, borderRadius: 8, alignItems: 'center' },
  segmentText: { fontSize: 14, fontWeight: '600' },
  sectionHead: { fontSize: 16, fontWeight: 'bold', marginTop: 18, marginBottom: 8 },
  radarLegend: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', marginTop: 8 },
  radarLegendItem: { fontSize: 12, marginHorizontal: 6, marginVertical: 2 },
  radarNote: { fontSize: 11, marginTop: 8, textAlign: 'center', paddingHorizontal: 8, lineHeight: 16 },
  historyLine: { fontSize: 13, marginBottom: 6 },
  officialLine: { fontSize: 12, marginBottom: 14, lineHeight: 17 },
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
  lockBox: { borderWidth: 1.5, borderRadius: 12, padding: 18, marginTop: 6, marginBottom: 8, alignItems: 'center', gap: 8 },
  lockEmoji: { fontSize: 30 },
  lockTitle: { fontSize: 15, fontWeight: '700', textAlign: 'center', lineHeight: 22 },
  lockSub: { fontSize: 13, textAlign: 'center', lineHeight: 20 },
  lockBtn: { borderRadius: 10, paddingVertical: 12, paddingHorizontal: 22, marginTop: 4 },
  lockBtnTxt: { color: '#ffffff', fontSize: 15, fontWeight: '800' },
  versionFooter: { alignItems: 'center', paddingVertical: 20, marginTop: 12 },
  versionText: { fontSize: 12 },
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
  formulaBox: { borderWidth: 1, borderRadius: 8, paddingVertical: 16, paddingHorizontal: 12, marginBottom: 10 },
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
