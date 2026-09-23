import { useEffect, useMemo, useRef, useState } from 'react';
import {
  Alert,
  Image,
  ImageBackground,
  Linking,
  Modal,
  PanResponder,
  Pressable,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
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

import type { Question, Chapter } from './src/types';
import { FIGURE_ASPECT } from './src/figures';
import { figureSource, hasFigure } from './src/data/figureStore';
import { RichText } from './src/MathText';
import { CATALOG, questionsByIds, QUESTION_FORMULA_ID, quizList, examRule, type ChapterEntry } from './src/catalog';
import { formulaDoc, type FormulaItem } from './src/formulas';
import { initContent } from './src/data/initContent';
import Svg, { Circle, Line, Polygon, Text as SvgText, Defs, LinearGradient, RadialGradient, Stop, Rect } from 'react-native-svg';
import {
  chapterStats,
  fieldStats,
  loadProgress,
  overallStat,
  recordAnswer,
  resetProgress,
  resetDaily,
  loadDaily,
  recordDaily,
  dailyDigest,
  wrongIdsFrom,
  snapshotFields,
  loadFieldSnaps,
  fieldCompareFrom,
  snapshotChapters,
  loadChapterSnaps,
  chapterSeriesAt,
  type ProgressMap,
  type GradeId,
  type FieldId,
  type QProgress,
  type FieldSnapStore,
  type FieldCompare,
  type ChapterSnapStore,
  type ChapterStat,
  type DailyMap,
  type DailyDigest,
} from './src/progress';
import Paywall, { type PayTarget } from './src/pro/Paywall';
import { TERMS_URL, PRIVACY_URL, SUPPORT_MAILTO_URL } from './src/config/revenuecat';
import {
  loadProState,
  saveOwned,
  saveDevPro,
  hasAnyPurchase,
  isLocked,
  entOfQuestion,
  entKey,
  entInfoByKey,
  ENTITLEMENTS,
  FREE_PER_CHAPTER,
  DEFAULT_PRO_STATE,
  type ProState,
} from './src/pro/proState';
import { initPurchases, syncEntitlements, restore as restorePurchases } from './src/pro/purchases';

const APP_VERSION = '1.0.0';
// 規定の受験日（公式・JSME 2026年度・分野×級ごと）。出典: https://www.jsme.or.jp/cee/examinee/outline（2026-09-19確認）
// 1級は各分野とも 11/27(金)。2級は 固体=12/4(金) / 熱流体・振動=12/3(木)。
// 設定させず、選択中の分野・級に連動して自動表示する。分野は CATALOG.id と一致（'solid'|'thermal'|'vibration'）。
const OFFICIAL_EXAM_DATES: Record<FieldId, Record<GradeId, string>> = {
  solid: { g1: '2026-11-27', g2: '2026-12-04' },
  thermal: { g1: '2026-11-27', g2: '2026-12-03' },
  vibration: { g1: '2026-11-27', g2: '2026-12-03' },
};

// ホーム上部で切り替えられる分野（＝CATALOG の分野id）。振動は今後の追加に備えて枠だけ用意。
// ready はカタログに実データの章があるかで自動判定するので、ここに足すだけで選べるようになる。
const DISCIPLINES: { id: FieldId; label: string }[] = [
  { id: 'solid', label: '固体力学' },
  { id: 'thermal', label: '熱流体力学' },
  { id: 'vibration', label: '振動' },
];

// ── 合格・足切りルール（本番の判定基準）──────────────────────────────
// 出典＝日本機械学会 2025年度「計算力学技術者（CAE技術者）1・2級 認定試験のご案内」
//   https://www.jsme.or.jp/cee/uploads/sites/3/2025/06/25cmnintei12.pdf
// 固体力学・熱流体力学・振動の3分野いずれも合格基準は共通で、条件は級だけで異なる（同案内より）。
// 数値は上記一次情報の原文どおり。年度で変わり得るため画面には必ず公式確認の注意を併記する。
const EXAM_PASS_RULES: Record<GradeId, { rules: string[]; plain: string }> = {
  g2: {
    rules: [
      '全体の正答率が 70％以上であること。',
      'かつ、全問不正解の分野が 2 分野以下であること。',
    ],
    // 素人にも分かる噛み砕き（足切り＝ここに引っかかると総合点が良くても不合格）。
    plain: '「全体で7割以上」に加えて、1問も正解できない分野が3つ以上あると足切りで不合格になります。得意分野だけで点を稼ぎ、苦手分野を捨て過ぎないことが大切です。',
  },
  g1: {
    rules: [
      '全体の正答率が 50％以上であること。',
      'かつ、正答率 70％以上の分野が 3 分野以上あること。',
      'かつ、全問不正解の分野が 2 分野以下であること。',
    ],
    plain: '全体で5割以上でも、「7割以上取れた分野が3つ以上」なければ合格できません。さらに、1問も正解できない分野が3つ以上あると足切りで不合格です。広く得点し、極端な苦手分野を作らないことが鍵です。',
  },
};
const EXAM_RULE_SOURCE = {
  label: '出典：日本機械学会 2025年度 計算力学技術者（CAE技術者）1・2級 認定試験のご案内',
  url: 'https://www.jsme.or.jp/cee/uploads/sites/3/2025/06/25cmnintei12.pdf',
};
// その分野×級が使えるか（カタログに章が1つでもあるか）。振動のように未整備なら false＝選べるが準備中表示。
function disciplineReady(fieldId: FieldId, gradeId: GradeId): boolean {
  const f = CATALOG.find((x) => x.id === fieldId);
  const g = f?.grades.find((gg) => gg.id === gradeId);
  return (g?.chapters?.length ?? 0) > 0;
}
function disciplineLabel(fieldId: FieldId): string {
  return DISCIPLINES.find((d) => d.id === fieldId)?.label ?? '固体力学';
}
const DAILY_GOAL = 10; // 今日のミッション＝1日の目標問題数（可変パラメータ）

// 分野×級の章一覧をカタログから引く（コース定義で使う汎用版）。
function fieldGradeChapters(fieldId: string, gradeId: string): ChapterEntry[] {
  const f = CATALOG.find((x) => x.id === fieldId);
  return f?.grades.find((g) => g.id === gradeId)?.chapters ?? [];
}
type Course = { id: string; name: string; chapters: ChapterEntry[]; ready: boolean };
// 1級は完成した章だけ出す（他章は準備中）。章側の ready フラグで出し分ける。
// 問題 → その問題が属する買い切り(分野×級)。ロック中にタップされたら、その級のPaywallを開くため。
function payTargetOf(q: Question): PayTarget | null {
  const e = entOfQuestion(q.id);
  return e ? { key: e.key, title: e.title } : null;
}

// 分野順は固体→熱流体→振動。各分野は1級を上に。
// 熱流体は2級を全章リリース済み。1級は中身をこれから作るので枠だけ用意（章0＝開くと「全 0 章」、
// カタログに章を足せば自動で並ぶ）。振動はまだ無いので ready:false＝「準備中」表示。
// コースの静的メタ（名前・準備中フラグ）。章はカタログから毎回引く＝OTAの差し替えを受けられる
// （固定配列にすると起動時のカタログで凍結され、OTA更新が反映されないため）。
const COURSE_META: Record<string, { name: string; ready: boolean }> = {
  'solid-1': { name: '固体力学 1級', ready: true },
  'solid-2': { name: '固体力学 2級', ready: true },
  'thermal-1': { name: '熱流体力学 1級', ready: true },
  'thermal-2': { name: '熱流体力学 2級', ready: true },
  vibration: { name: '振動', ready: false },
};

// 分野×級 → コース（問題/公式タブが表示する対象）。ホームの選択に問題/公式タブを追従させる要。
function courseOf(fieldId: FieldId, gradeId: GradeId): Course | null {
  const id = fieldId === 'vibration' ? 'vibration' : `${fieldId}-${gradeId === 'g1' ? '1' : '2'}`;
  const meta = COURSE_META[id];
  if (!meta) return null;
  return { id, name: meta.name, chapters: fieldGradeChapters(fieldId, gradeId), ready: meta.ready };
}

type Tab = 'home' | 'study' | 'formula' | 'settings';
type ThemePref = 'system' | 'light' | 'dark';
type StudyView = 'chapters' | 'tiles' | 'problem';
type FormulaView = 'chapters' | 'titles' | 'item';

export default function App() {
  // 起動時に一度だけコンテンツOTAを初期化（端末キャッシュの差し替えを反映→カタログ再構築）。
  // 完了するまでは短い暗色スプラッシュ（ローカル読込のみなので通常は一瞬）。ネット同期は裏で走り、
  // 更新があれば contentVersion を上げて "この起動中に" 画面へ反映する（＝2回起動しなくてよい）。
  const [contentReady, setContentReady] = useState(false);
  const [contentVersion, setContentVersion] = useState(0);
  useEffect(() => {
    initContent(() => setContentVersion((v) => v + 1)).finally(() => setContentReady(true));
  }, []);
  return (
    <SafeAreaProvider>
      {contentReady ? <AppInner contentVersion={contentVersion} /> : <View style={{ flex: 1, backgroundColor: '#0b1526' }} />}
    </SafeAreaProvider>
  );
}

const THEME_KEY = 'cae.theme'; // 'system' | 'light' | 'dark'
const HOME_GRADE_KEY = 'cae.homeGrade'; // ホームで前回開いた級 'g1' | 'g2'
const HOME_FIELD_KEY = 'cae.homeField'; // ホームで前回開いた分野 'solid' | 'thermal' | 'vibration'

function AppInner(props: { contentVersion: number }) {
  // FEMネイビー世界観をアプリ全体で統一（ホームと同じ暗色＋シアンのアクセント。ライト/ダークは廃止）。
  const t = navy;
  const insets = useSafeAreaInsets();

  const [tab, setTab] = useState<Tab>('home');
  const [progress, setProgress] = useState<ProgressMap>({});
  // 日別ログ（連続日数・今日の学習量・直近の活動グラフ用）
  const [daily, setDaily] = useState<DailyMap>({});

  // Pro（買い切り＝分野×級ごと）状態と購入画面の表示。target＝今売る級。
  const [proSt, setProSt] = useState<ProState>(DEFAULT_PRO_STATE);
  const [showPaywall, setShowPaywall] = useState(false);
  const [payTarget, setPayTarget] = useState<PayTarget | null>(null);

  // ロック中の問題／設定から購入画面を開く。
  // target 指定あり（ロック問題からの導線）＝その級をそのまま売る。
  // target 未指定（設定の「プレミアムの購入」）＝ホームで選択中の分野×級を既定にする（動的追従）。
  //   選択中が課金対象でない（例：振動＝準備中で問題なし）時は、未購入の級→先頭 の順でフォールバック。
  function openPaywall(target: PayTarget | null) {
    const current = entInfoByKey(entKey(field, grade)); // ホーム選択中の分野×級（課金対象なら見つかる）
    const fallback =
      current ?? ENTITLEMENTS.find((e) => !proSt.owned.includes(e.key)) ?? ENTITLEMENTS[0] ?? null;
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

  // ホームで選んだ分野×級を「アプリ全体の唯一の選択」として保持（問題/公式タブもこれに追従＝
  // タブ側で分野・級を選び直す2度手間をなくす）。起動時は前回値を復元（初回のみ固体2級）。
  const [grade, setGrade] = useState<GradeId>('g2');
  const [field, setField] = useState<FieldId>('solid');
  useEffect(() => {
    AsyncStorage.getItem(HOME_GRADE_KEY).then((v) => { if (v === 'g1' || v === 'g2') setGrade(v); }).catch(() => {});
    AsyncStorage.getItem(HOME_FIELD_KEY).then((v) => { if (v && DISCIPLINES.some((d) => d.id === v)) setField(v as FieldId); }).catch(() => {});
  }, []);
  function chooseFieldGrade(f: FieldId, g: GradeId) {
    setField(f); AsyncStorage.setItem(HOME_FIELD_KEY, f).catch(() => {});
    setGrade(g); AsyncStorage.setItem(HOME_GRADE_KEY, g).catch(() => {});
  }
  // 選択中の分野×級に対応するコース。問題タブ・公式タブはこれをそのまま表示する。
  const course = useMemo(() => courseOf(field, grade), [field, grade, props.contentVersion]);
  const formulaCourse = course; // 公式・用語も同じ分野×級に追従

  // 問題タブのサブ画面状態（コース選択画面は廃止＝章の目次から始まる）
  const [studyView, setStudyView] = useState<StudyView>('chapters');
  const [chapter, setChapter] = useState<ChapterEntry | null>(null);
  // 出題中のリスト（章の全問 or 復習リスト）と現在位置
  const [activeList, setActiveList] = useState<Question[]>([]);
  const [activeTitle, setActiveTitle] = useState('');
  const [qIndex, setQIndex] = useState(0);
  // 出題セッション内の選択（問題ID → 選んだ番号）。前後移動しても選択が残る。
  const [answers, setAnswers] = useState<Record<string, number>>({});

  // 公式・用語タブ（課程 → 章 → タイトル一覧 → 個別解説）
  const [formulaView, setFormulaView] = useState<FormulaView>('chapters');
  const [formulaChapterId, setFormulaChapterId] = useState<string | null>(null);
  const [formulaItemId, setFormulaItemId] = useState<string | null>(null);
  // 問題画面から公式へ飛んだか（true の時、公式カードに「問題に戻る」を出す）
  const [formulaFrom, setFormulaFrom] = useState<null | 'study'>(null);
  useEffect(() => {
    loadProgress().then(async (p) => {
      setProgress(p);
      // 分野バランス＋章別を1日1回記録しておき、レーダーの成長比較（今週/先週/先月）を出せるようにする。
      // 分野×級ごとに別々のスナップとして貯める（固体と熱流体が混ざらないよう分野キーで分離）。
      for (const d of DISCIPLINES) {
        for (const g of ['g1', 'g2'] as GradeId[]) {
          if (!disciplineReady(d.id, g)) continue;
          await snapshotFields(p, g, d.id);
          await snapshotChapters(p, g, d.id);
        }
      }
    });
    loadDaily().then(setDaily);
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

  const wrongIds = useMemo(() => wrongIdsFrom(progress), [progress]);
  const wrongQuestions = useMemo(() => questionsByIds(wrongIds), [wrongIds]);
  // 要復習（間違い）はホームで選んだ分野×級に限定する。固体1級の弱点を熱流体1級のホームに出さない＝混同防止。
  const courseWrongQuestions = useMemo(() => {
    const ids = new Set(fieldGradeChapters(field, grade).flatMap((c) => c.data.questions.map((q) => q.id)));
    return wrongQuestions.filter((q) => ids.has(q.id));
  }, [wrongQuestions, field, grade, props.contentVersion]);

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

  // 今日のミッション：未挑戦（まだ一度も解いていない）問題を集めて出題（踏破率アップ）。
  function solveUnattempted(gradeId: GradeId, fieldId: FieldId = 'solid') {
    const all = fieldGradeChapters(fieldId, gradeId).flatMap((c) => c.data.questions);
    const un = all.filter((q) => !progress[q.id]);
    openProblems(un.length ? un : all, '今日のミッション');
  }

  // 章別ステータス/レーダーの章をタップ → その章の問題を開く。
  function openChapterById(gradeId: GradeId, chapterId: string, fieldId: FieldId = 'solid') {
    const c = fieldGradeChapters(fieldId, gradeId).find((x) => x.id === chapterId);
    if (c) openProblems(c.data.questions, c.title);
  }

  // ホームの「用語問題／計算・数値問題」カード → まずタイトル一覧（tiles）を出し、
  // タイルを選ぶと個別問題へ。章と同じ導線なので、問題→一覧→ホームと戻れる。
  // 章に属さない専用セットなので合成の ChapterEntry（id='__quiz__'）に包んで tiles に流用する。
  function openQuiz(kind: 'term' | 'calc', label: string) {
    const list = quizList(kind, field, grade);
    if (list.length === 0) {
      // 未配信ならフォールバック（用語→公式・用語タブ／計算→問題タブの章目次）。
      if (kind === 'term') { setFormulaFrom(null); setFormulaView('chapters'); setTab('formula'); }
      else { setStudyView('chapters'); setTab('study'); }
      return;
    }
    const synthetic: ChapterEntry = {
      id: '__quiz__',
      title: label,
      data: { meta: { grade: '', category: label, chapter: 0, count: list.length }, questions: list } as Chapter,
      ready: true,
    };
    setChapter(synthetic);
    setStudyView('tiles');
    setTab('study');
  }

  async function onSelectAnswer(q: Question, choiceNum: number) {
    if (answers[q.id] != null) return; // 既に回答済みなら無視
    setAnswers((a) => ({ ...a, [q.id]: choiceNum }));
    const correct = choiceNum === q.answer;
    const next = await recordAnswer(progress, q.id, correct);
    setProgress(next);
    // 「今日 何問解いて 何問正解したか」を日単位で記録（継続日数・活動グラフの素）。
    setDaily(await recordDaily(daily, correct));
  }

  // ボトムナビのタブをスワイプでも切替（左=次のタブ / 右=前のタブ）。ただし問題画面・
  // 公式/用語の個別画面では前後移動が優先（内側のスワイプが担当するのでタブは切り替えない）。
  const TAB_ORDER: Tab[] = ['home', 'study', 'formula', 'settings'];
  function swipeTab(dir: 1 | -1) {
    if (tab === 'study' && studyView === 'problem') return;
    if (tab === 'formula' && formulaView === 'item') return;
    const i = TAB_ORDER.indexOf(tab);
    const ni = i + dir;
    if (ni >= 0 && ni < TAB_ORDER.length) { setFormulaFrom(null); setTab(TAB_ORDER[ni]); }
  }
  const tabPan = useSwipeNav(() => swipeTab(1), () => swipeTab(-1));

  return (
    <View style={[styles.container, { backgroundColor: t.bg }]}>
      <StatusBar style="light" />
      <SafeAreaView style={{ flex: 1 }} edges={['top', 'left', 'right']}>
        <View style={{ flex: 1 }} {...tabPan}>
        {tab === 'home' && (
          <HomeTab
            t={t}
            progress={progress}
            daily={daily}
            grade={grade}
            field={field}
            onChooseFieldGrade={chooseFieldGrade}
            wrongCount={courseWrongQuestions.length}
            onReview={() => openProblems(courseWrongQuestions, '間違い復習')}
            onGoStudy={() => {
              setStudyView('chapters');
              setTab('study');
            }}
            onGoFormula={() => {
              setFormulaFrom(null);
              setFormulaView('chapters');
              setTab('formula');
            }}
            onGoTermQuiz={() => openQuiz('term', '用語問題')}
            onGoCalcQuiz={() => openQuiz('calc', '計算・数値問題')}
            onSolveUnattempted={solveUnattempted}
            onOpenChapter={openChapterById}
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
            onExitHome={() => setTab('home')}
            proState={proSt}
            onOpenPaywall={openPaywall}
            onOpenFormula={(formulaId, itemId) => {
              // 問題画面から公式・用語カードへ直接ジャンプ（公式コースは選択中の分野×級に自動追従）。
              setFormulaChapterId(formulaId);
              setFormulaItemId(itemId);
              setFormulaView('item');
              setFormulaFrom('study');
              setTab('formula');
            }}
          />
        )}

        {tab === 'formula' && (
          <FormulaTab
            t={t}
            view={formulaView}
            course={formulaCourse}
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
            fromStudy={formulaFrom === 'study'}
            onBackToStudy={() => {
              setFormulaFrom(null);
              setTab('study');
            }}
          />
        )}

        {tab === 'settings' && (
          <SettingsTab
            t={t}
            progress={progress}
            onReset={async () => {
              const cleared = await resetProgress();
              setProgress(cleared);
              setDaily(await resetDaily());
            }}
            owned={proSt.owned}
            devPro={proSt.devPro}
            onOpenPaywall={openPaywall}
            onRestoreAll={restoreAll}
            onToggleDevPro={async (on) => {
              await saveDevPro(on);
              setProSt((s) => ({ ...s, devPro: on }));
            }}
          />
        )}
        </View>
      </SafeAreaView>

      <TabBar t={t} tab={tab} insetsBottom={insets.bottom} onChange={(k) => { setFormulaFrom(null); setTab(k); }} />

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
// FEMホームの画像素材（assets/home/・黒背景の解析画像）。
const HOME_IMG = {
  header: require('./assets/home/header.jpg'),
  beam: require('./assets/home/beam.jpg'),
  frame: require('./assets/home/frame.jpg'),
  formula: require('./assets/home/formula.jpg'),
  radarbg: require('./assets/home/radarbg.jpg'),
  exambg: require('./assets/home/exambg.jpg'),
};
// ホーム専用のダーク世界観パレット（アプリのテーマに依らず常にこの世界観で表示）。
const HOME = {
  bg0: '#060A13', bg2: '#0E1728', surface: 'rgba(150,190,235,0.06)',
  border: 'rgba(125,199,255,0.16)', borderStrong: 'rgba(125,199,255,0.32)',
  text: '#EAF2FF', muted: '#8CA1C1', faint: '#5C6E8C',
  cyan: '#3BE6F2', cyanDeep: '#0B93B4', good: '#4ADE80', warn: '#FBBF24', bad: '#FB7185',
};
// 写真の上に文字を載せるための暗幕（react-native-svg の縦グラデ）。id は衝突回避のため一意に。
function Veil(props: { id: string; stops: { o: number; op: number }[] }) {
  return (
    <Svg style={StyleSheet.absoluteFill} pointerEvents="none">
      <Defs>
        <LinearGradient id={props.id} x1="0" y1="0" x2="0" y2="1">
          {props.stops.map((s, i) => (
            <Stop key={i} offset={s.o} stopColor="#060A13" stopOpacity={s.op} />
          ))}
        </LinearGradient>
      </Defs>
      <Rect x="0" y="0" width="100%" height="100%" fill={`url(#${props.id})`} />
    </Svg>
  );
}

// 受験日までの残り日数（過ぎていれば負・未設定は null）。
function examDaysLeft(dateStr: string | null): number | null {
  if (!dateStr) return null;
  const d = new Date(dateStr + 'T00:00:00');
  if (isNaN(d.getTime())) return null;
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  return Math.round((d.getTime() - today.getTime()) / 86400000);
}

// 規定受験日の表示ラベル（例: 11月27日(金)）。
const WEEKDAY_JA = ['日', '月', '火', '水', '木', '金', '土'];
function fmtExamDate(dateStr: string): string {
  const d = new Date(dateStr + 'T00:00:00');
  if (isNaN(d.getTime())) return dateStr;
  return `${d.getMonth() + 1}月${d.getDate()}日(${WEEKDAY_JA[d.getDay()]})`;
}

// 章別レーダー：軸＝各章の正答率。今週(シアン塗り)/先週(緑破線)/先月(灰破線)の3期を重ねて成長を見せる。
function GrowthRadar(props: {
  stats: ChapterStat[];
  week: Record<string, number> | null;
  month: Record<string, number> | null;
}) {
  const items = props.stats;
  const N = Math.max(items.length, 3);
  const size = 236, cx = size / 2, cy = size / 2, R = 86, labelR = R + 13;
  const ang = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / N;
  const at = (i: number, r: number) => ({ x: cx + r * Math.cos(ang(i)), y: cy + r * Math.sin(ang(i)) });
  const clip = (v: number) => Math.max(0, Math.min(1, v));
  const toPoly = (vals: number[]) =>
    items.map((_, i) => { const p = at(i, R * clip(vals[i])); return `${p.x.toFixed(1)},${p.y.toFixed(1)}`; }).join(' ');
  const ring = (k: number) =>
    items.map((_, i) => { const p = at(i, R * k); return `${p.x.toFixed(1)},${p.y.toFixed(1)}`; }).join(' ');
  const cur = items.map((s) => s.accuracy);
  const week = props.week ? items.map((s) => props.week![s.id] ?? 0) : null;
  const month = props.month ? items.map((s) => props.month![s.id] ?? 0) : null;
  return (
    <Svg width={size} height={size}>
      {[0.25, 0.5, 0.75, 1].map((k) => (
        <Polygon key={k} points={ring(k)} fill="none" stroke="rgba(125,199,255,0.15)" strokeWidth={1} />
      ))}
      {items.map((_, i) => { const p = at(i, R); return (
        <Line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke="rgba(125,199,255,0.12)" strokeWidth={1} />
      ); })}
      {month ? <Polygon points={toPoly(month)} fill="none" stroke="#5C6E8C" strokeWidth={1.3} strokeDasharray="3,3" /> : null}
      {week ? <Polygon points={toPoly(week)} fill="none" stroke="#4ADE80" strokeWidth={1.6} strokeDasharray="4,3" /> : null}
      <Polygon points={toPoly(cur)} fill="rgba(59,230,242,0.16)" stroke="#3BE6F2" strokeWidth={2} />
      {items.map((s, i) => { const p = at(i, labelR); return (
        <SvgText key={s.id} x={p.x} y={p.y} fill="#8CA1C1" fontSize={9} fontWeight="bold" textAnchor="middle" alignmentBaseline="middle">
          {String(i + 1)}
        </SvgText>
      ); })}
    </Svg>
  );
}

const home = StyleSheet.create({
  scroll: { paddingBottom: 28 },
  hero: { height: 300, justifyContent: 'flex-end' },
  heroImg: {},
  heroTop: { position: 'absolute', top: 14, left: 16, right: 16, flexDirection: 'row', justifyContent: 'flex-start' },
  nowtag: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingVertical: 8, paddingHorizontal: 14, borderRadius: 999, backgroundColor: 'rgba(59,230,242,0.16)', borderWidth: 1, borderColor: HOME.cyan },
  nowdot: { width: 7, height: 7, borderRadius: 4, backgroundColor: HOME.cyan },
  nowtagTxt: { color: '#EAF2FF', fontWeight: '800', fontSize: 14 },
  nowchev: { color: '#EAF2FF', fontSize: 11, opacity: 0.85 },
  heroCopy: { paddingHorizontal: 20, paddingBottom: 16 },
  kicker: { color: '#CBDAF0', fontSize: 13 },
  headline: { color: HOME.text, fontWeight: '900', fontSize: 28, marginTop: 6 },
  pct: { color: HOME.cyan, fontSize: 44, fontWeight: '900' },
  pctSmall: { color: HOME.cyan, fontSize: 20, fontWeight: '900' },
  prog: { marginTop: 12, height: 8, borderRadius: 999, backgroundColor: 'rgba(255,255,255,0.12)', borderWidth: 1, borderColor: HOME.border, overflow: 'hidden' },
  progFill: { height: '100%', backgroundColor: HOME.cyan },
  capRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 6 },
  capTxt: { color: '#93A6C4', fontSize: 11 },
  body: { paddingHorizontal: 16, paddingTop: 8, gap: 14 },
  card: { backgroundColor: HOME.surface, borderWidth: 1, borderColor: HOME.border, borderRadius: 20, padding: 16 },
  cardGlow: { borderColor: HOME.borderStrong },
  missionTop: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  missionIco: { width: 44, height: 44, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(59,230,242,0.12)', borderWidth: 1, borderColor: HOME.borderStrong },
  missionH3: { color: HOME.text, fontSize: 17, fontWeight: '900' },
  missionP: { color: HOME.muted, fontSize: 12, marginTop: 3 },
  missionCount: { color: HOME.cyan, fontWeight: '800', fontSize: 15 },
  mini: { marginTop: 12, height: 7, borderRadius: 999, backgroundColor: 'rgba(255,255,255,0.06)', overflow: 'hidden' },
  miniFill: { height: '100%', backgroundColor: HOME.cyan },
  cta: { marginTop: 14, borderRadius: 14, paddingVertical: 15, alignItems: 'center', backgroundColor: HOME.cyan },
  ctaTxt: { color: '#04141b', fontWeight: '900', fontSize: 16 },
  duo: { flexDirection: 'row', gap: 12 },
  imgCard: { flex: 1, height: 150, borderRadius: 18, overflow: 'hidden', borderWidth: 1, borderColor: HOME.border, justifyContent: 'flex-end', padding: 14 },
  cardImg: {},
  tag: { position: 'absolute', top: 12, left: 12, paddingVertical: 5, paddingHorizontal: 9, borderRadius: 999, backgroundColor: 'rgba(9,14,26,0.55)', borderWidth: 1, borderColor: HOME.borderStrong },
  tagTxt: { color: HOME.cyan, fontWeight: '700', fontSize: 10 },
  imgCardIn: {},
  cardH4: { color: HOME.text, fontSize: 16, fontWeight: '900' },
  cardP: { color: '#B6C6E0', fontSize: 11, marginTop: 3 },
  secH: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: 6, marginBottom: -2, paddingHorizontal: 2 },
  secTitle: { color: HOME.text, fontSize: 16, fontWeight: '900' },
  secSub: { color: HOME.cyan, fontSize: 12 },
  radarCard: { position: 'relative', overflow: 'hidden' },
  radarInner: { position: 'relative' },
  rlegend: { flexDirection: 'row', justifyContent: 'center', gap: 16, marginTop: 8 },
  rlegItem: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  rlegLine: { width: 16, height: 3, borderRadius: 2 },
  rlegDash: { width: 16, height: 0, borderTopWidth: 3, borderStyle: 'dashed' },
  rlegTxt: { color: HOME.muted, fontSize: 11 },
  rnote: { color: HOME.faint, fontSize: 11, textAlign: 'center', marginTop: 8 },
  wgrid: { flexDirection: 'row', gap: 8, marginTop: 14 },
  wtile: { flex: 1, backgroundColor: 'rgba(255,255,255,0.03)', borderWidth: 1, borderColor: HOME.border, borderRadius: 12, paddingVertical: 10, alignItems: 'center' },
  wtileV: { color: HOME.text, fontWeight: '800', fontSize: 17 },
  wtileL: { color: HOME.muted, fontSize: 10, marginTop: 3 },
  examCard: { position: 'relative', overflow: 'hidden', borderRadius: 20, borderWidth: 1, borderColor: 'rgba(251,191,36,0.4)', backgroundColor: '#0E1728' },
  examBgWrap: { position: 'absolute', left: 0, right: 0, bottom: 0, height: 168, overflow: 'hidden' },
  examImg: { position: 'absolute', left: 0, right: 0, bottom: 0, width: '100%', aspectRatio: 1232 / 472, opacity: 1 },
  examIn: { position: 'relative', padding: 16, paddingBottom: 150 },
  examHead: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  examIco: { width: 44, height: 44, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(251,191,36,0.16)', borderWidth: 1, borderColor: 'rgba(251,191,36,0.4)' },
  examChev: { color: HOME.cyan, fontSize: 22, fontWeight: '700', marginLeft: 4 },
  examLi: { flexDirection: 'row', alignItems: 'center', gap: 9, marginTop: 8 },
  examDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: HOME.warn },
  examLiTxt: { color: '#EAF2FF', fontSize: 13, flex: 1 },
  examCautn: { color: '#F6C89A', fontSize: 11, marginTop: 11 },
  quote: { borderRadius: 20, borderWidth: 1, borderColor: HOME.border, paddingVertical: 22, paddingHorizontal: 18, alignItems: 'center', backgroundColor: 'rgba(14,23,40,0.5)' },
  quoteJa: { color: '#DCE8FA', fontWeight: '700', fontSize: 15, textAlign: 'center' },
  quoteEn: { color: HOME.cyan, fontWeight: '700', fontSize: 11, letterSpacing: 2, marginTop: 8 },
  modalWrap: { flex: 1, backgroundColor: 'rgba(3,6,12,0.62)', justifyContent: 'flex-end' },
  sheet: { backgroundColor: HOME.bg2, borderTopLeftRadius: 20, borderTopRightRadius: 20, borderTopWidth: 1, borderColor: HOME.borderStrong, padding: 18, gap: 8 },
  sheetH: { color: HOME.text, fontWeight: '900', fontSize: 16, textAlign: 'center', marginBottom: 4 },
  sheetSec: { color: HOME.muted, fontSize: 11, marginTop: 6 },
  opt: { backgroundColor: HOME.surface, borderWidth: 1, borderColor: HOME.border, borderRadius: 12, paddingVertical: 13, paddingHorizontal: 14 },
  optOn: { borderColor: HOME.cyan, backgroundColor: 'rgba(59,230,242,0.12)' },
  optTxt: { color: HOME.text, fontWeight: '700', fontSize: 15 },
  dateInput: { backgroundColor: HOME.surface, borderWidth: 1, borderColor: HOME.border, borderRadius: 12, paddingVertical: 12, paddingHorizontal: 14, color: HOME.text, fontSize: 16 },
  clearBtn: { alignItems: 'center', paddingVertical: 10 },
  clearTxt: { color: HOME.muted, fontSize: 13 },
  // 合格・足切りルール モーダル
  ruleBadge: { alignSelf: 'center', backgroundColor: 'rgba(251,191,36,0.14)', borderWidth: 1, borderColor: 'rgba(251,191,36,0.45)', borderRadius: 999, paddingVertical: 4, paddingHorizontal: 12, marginBottom: 6 },
  ruleBadgeTxt: { color: HOME.warn, fontWeight: '800', fontSize: 12 },
  ruleSecH: { color: HOME.cyan, fontWeight: '800', fontSize: 12, marginTop: 10, marginBottom: 2 },
  ruleRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 10, backgroundColor: HOME.surface, borderWidth: 1, borderColor: HOME.border, borderRadius: 12, paddingVertical: 11, paddingHorizontal: 12, marginTop: 6 },
  ruleNum: { width: 22, height: 22, borderRadius: 11, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(59,230,242,0.16)', borderWidth: 1, borderColor: 'rgba(59,230,242,0.4)' },
  ruleNumTxt: { color: HOME.cyan, fontWeight: '900', fontSize: 12 },
  ruleTxt: { color: '#EAF2FF', fontSize: 14, flex: 1, lineHeight: 21, fontWeight: '600' },
  rulePlain: { color: HOME.text, fontSize: 13, lineHeight: 21, marginTop: 4 },
  ruleNote: { color: HOME.muted, fontSize: 11, lineHeight: 17, marginTop: 8 },
  ruleSrcBtn: { paddingVertical: 8, marginTop: 8 },
  ruleSrcTxt: { color: HOME.cyan, fontSize: 12, textDecorationLine: 'underline' },
});

function HomeTab(props: {
  t: Theme;
  progress: ProgressMap;
  daily: DailyMap;
  grade: GradeId;
  field: FieldId;
  onChooseFieldGrade: (f: FieldId, g: GradeId) => void;
  wrongCount: number;
  onReview: () => void;
  onGoStudy: () => void;
  onGoFormula: () => void;
  onGoTermQuiz: () => void;
  onGoCalcQuiz: () => void;
  onSolveUnattempted: (gradeId: GradeId, fieldId: FieldId) => void;
  onOpenChapter: (gradeId: GradeId, chapterId: string, fieldId: FieldId) => void;
}) {
  const { t } = props;
  // 継続日数・今日の学習量・直近の活動（級に依らず端末全体の学習ログから）。
  const digest = useMemo(() => dailyDigest(props.daily), [props.daily]);
  // 分野×級はアプリ共通の選択（AppInner保持）をそのまま使う。問題/公式タブと必ず一致させるため。
  const grade = props.grade;
  const field = props.field;
  const overall = useMemo(() => overallStat(props.progress, grade, field), [props.progress, grade, field]);
  const stats = useMemo(() => chapterStats(props.progress, grade, field), [props.progress, grade, field]);
  const fields = useMemo(() => fieldStats(props.progress, grade, field), [props.progress, grade, field]);
  // レーダーの「1週前比の成長」。端末に貯めた分野スナップショットと今を比べる。
  const [snaps, setSnaps] = useState<FieldSnapStore>([]);
  useEffect(() => {
    loadFieldSnaps().then(setSnaps);
  }, [props.progress]);
  const compare: FieldCompare = useMemo(
    () => fieldCompareFrom(snaps, fields, grade, field),
    [snaps, fields, grade, field]
  );
  const hasGrowth = Object.values(compare.growth).some((v) => v != null);
  const attemptedStats = stats.filter((s) => s.attempted > 0);
  const weak = [...attemptedStats].sort((a, b) => a.accuracy - b.accuracy).slice(0, 3);
  const strong = [...attemptedStats].sort((a, b) => b.accuracy - a.accuracy).slice(0, 3);

  // ---- FEM世界観ホーム ----
  const [chapSnaps, setChapSnaps] = useState<ChapterSnapStore>([]);
  useEffect(() => { loadChapterSnaps().then(setChapSnaps); }, [props.progress]);
  const [showGrade, setShowGrade] = useState(false);
  const [showExamRule, setShowExamRule] = useState(false); // 試験前の準備カード→合格・足切りルールの詳細モーダル
  // 分野と級を1タップでまとめて確定（固体1級/固体2級/熱流体1級…の6ボタン用）。
  // 従来は分野と級を別々に押す必要があり「両方変えたい」時に片方だけ確定してしまっていた。
  function chooseFieldGrade(f: FieldId, g: GradeId) {
    props.onChooseFieldGrade(f, g); // アプリ共通の選択を更新（保存も親側）。問題/公式タブも自動追従。
    setShowGrade(false);
  }

  // サブ部品へ渡すダーク派生テーマ
  const ht = { ...t, bg: HOME.bg0, card: HOME.surface, text: HOME.text, sub: HOME.muted,
    border: HOME.border, primary: HOME.cyan, correct: HOME.good, wrong: HOME.bad, amber: HOME.warn } as Theme;
  const subjectLabel = `${disciplineLabel(field)} ${grade === 'g1' ? '1級' : '2級'}`;
  // 試験前の準備カードの合格・足切りルール（分野×級ごと・OTAで差し替え可）。
  // OTA/同梱の content/exam/passrule-*.json を優先し、万一無ければ同梱既定（EXAM_PASS_RULES）へフォールバック。
  const examRuleDoc = examRule(field, grade) ?? {
    rules: EXAM_PASS_RULES[grade].rules,
    plain: EXAM_PASS_RULES[grade].plain,
    note: '※「分野」＝試験内のいくつかの出題区分のこと。全問不正解の分野が3つ以上になると、総合点に関わらず足切りで不合格です。',
    sourceLabel: EXAM_RULE_SOURCE.label,
    sourceUrl: EXAM_RULE_SOURCE.url,
  };
  const examDate = OFFICIAL_EXAM_DATES[field]?.[grade] ?? OFFICIAL_EXAM_DATES.solid[grade]; // 分野×級に連動した規定の受験日（自動・設定不要）
  const daysLeft = examDaysLeft(examDate);
  const coverPct = overall.totalQuestions > 0 ? Math.round((overall.attempted / overall.totalQuestions) * 100) : 0;
  const today = digest.last30[digest.last30.length - 1] ?? { key: '', n: 0, c: 0 };
  const goalDone = Math.min(today.n, DAILY_GOAL);
  const goalPct = Math.round((goalDone / DAILY_GOAL) * 100);
  const weekN = digest.last30.slice(-7).reduce((a, d) => a + d.n, 0);
  const wd = digest.weekDelta;
  const wdColor = wd > 0 ? HOME.good : wd < 0 ? HOME.bad : HOME.muted;
  const wdText = wd > 0 ? `▲+${wd}` : wd < 0 ? `▼${wd}` : '±0';
  const weekAcc = chapterSeriesAt(chapSnaps, grade, 7, field);
  const monthAcc = chapterSeriesAt(chapSnaps, grade, 28, field);

  return (
    <>
    <ScrollView style={{ backgroundColor: HOME.bg0 }} contentContainerStyle={home.scroll}>
      {/* ヒーロー（FEM解析建築の夜景） */}
      <ImageBackground source={HOME_IMG.header} style={home.hero} imageStyle={home.heroImg}>
        <Veil id="heroVeil" stops={[{ o: 0, op: 0.72 }, { o: 0.3, op: 0 }, { o: 0.58, op: 0 }, { o: 1, op: 1 }]} />
        <View style={home.heroTop}>
          <Pressable style={home.nowtag} onPress={() => setShowGrade(true)}>
            <View style={home.nowdot} />
            <Text style={home.nowtagTxt}>{subjectLabel}</Text>
            <Text style={home.nowchev}>▾</Text>
          </Pressable>
        </View>
        <View style={home.heroCopy}>
          <View>
            {daysLeft != null && daysLeft >= 0 ? (
              <Text style={home.headline}>試験まで あと <Text style={home.pct}>{daysLeft}</Text> 日</Text>
            ) : (
              <Text style={home.headline}>受験おつかれさまでした</Text>
            )}
            <Text style={home.capTxt}>{grade === 'g1' ? '1級' : '2級'} 試験日 {fmtExamDate(examDate)}</Text>
          </View>
          <View style={home.prog}><View style={[home.progFill, { width: `${coverPct}%` as DimensionValue }]} /></View>
          <View style={home.capRow}>
            <Text style={home.capTxt}>学習範囲 {overall.attempted}/{overall.totalQuestions}問 踏破</Text>
            <Text style={home.capTxt}>継続 {digest.streak}日</Text>
          </View>
        </View>
      </ImageBackground>

      <View style={home.body}>
        {/* 章別の到達度と成長（ヒーロー直下・レーダー3期比較＋週サマリ＋弱点克服） */}
        <View style={home.secH}>
          <Text style={home.secTitle}>章別の到達度と成長</Text>
          <Text style={home.secSub}>{subjectLabel} · 全{stats.length}章</Text>
        </View>
        <View style={[home.card, home.radarCard]}>
          {/* 背景画像なし（土台の不透明カード HOME.surface の上にレーダーを表示）。 */}
          <View style={home.radarInner}>
            <View style={{ alignItems: 'center' }}>
              <GrowthRadar stats={stats} week={weekAcc} month={monthAcc} />
            </View>
            <View style={home.rlegend}>
              <View style={home.rlegItem}><View style={[home.rlegLine, { backgroundColor: HOME.cyan }]} /><Text style={home.rlegTxt}>今週</Text></View>
              <View style={home.rlegItem}><View style={[home.rlegDash, { borderTopColor: HOME.good }]} /><Text style={home.rlegTxt}>先週</Text></View>
              <View style={home.rlegItem}><View style={[home.rlegDash, { borderTopColor: HOME.faint }]} /><Text style={home.rlegTxt}>先月</Text></View>
            </View>
            <Text style={home.rnote}>
              軸＝各章の正答率。今週の線が外へ広がるほど成長。{!weekAcc && !monthAcc ? '（続けると先週・先月の線が増えます）' : ''}
            </Text>
            <View style={home.wgrid}>
              <View style={home.wtile}><Text style={home.wtileV}>🔥{digest.streak}</Text><Text style={home.wtileL}>継続</Text></View>
              <View style={home.wtile}><Text style={[home.wtileV, { color: HOME.cyan }]}>{today.n}</Text><Text style={home.wtileL}>今日</Text></View>
              <View style={home.wtile}><Text style={home.wtileV}>{weekN}</Text><Text style={home.wtileL}>今週の問題</Text></View>
              <View style={home.wtile}><Text style={[home.wtileV, { color: wdColor }]}>{wdText}</Text><Text style={home.wtileL}>今週正答率</Text></View>
            </View>
            <Pressable style={[home.cta, { marginTop: 14 }]} onPress={props.onReview} disabled={props.wrongCount === 0}>
              <Text style={home.ctaTxt}>⚡ 弱点を克服{props.wrongCount > 0 ? `（要復習 ${props.wrongCount}問）` : '（なし）'}</Text>
            </Pressable>
          </View>
        </View>

        {/* 今日のミッション（未挑戦から DAILY_GOAL 問） */}
        <View style={[home.card, home.cardGlow]}>
          <View style={home.missionTop}>
            <View style={home.missionIco}><Text style={{ fontSize: 20 }}>📐</Text></View>
            <View style={{ flex: 1 }}>
              <Text style={home.missionH3}>今日のミッション</Text>
              <Text style={home.missionP}>未挑戦から{DAILY_GOAL}問 · あと{Math.max(0, DAILY_GOAL - goalDone)}問（踏破率アップ）</Text>
            </View>
            <Text style={home.missionCount}>{goalDone}/{DAILY_GOAL}</Text>
          </View>
          <View style={home.mini}><View style={[home.miniFill, { width: `${goalPct}%` as DimensionValue }]} /></View>
          <Pressable style={home.cta} onPress={() => props.onSolveUnattempted(grade, field)}>
            <Text style={home.ctaTxt}>▶ 未挑戦を解く</Text>
          </Pressable>
        </View>

        {/* 用語問題 / 計算・数値問題 */}
        <View style={home.duo}>
          <Pressable style={home.imgCard} onPress={props.onGoTermQuiz}>
            <ImageBackground source={HOME_IMG.formula} style={StyleSheet.absoluteFill} imageStyle={home.cardImg}>
              <Veil id="veilFormula" stops={[{ o: 0, op: 0.02 }, { o: 0.5, op: 0.42 }, { o: 1, op: 0.92 }]} />
            </ImageBackground>
            <View style={home.tag}><Text style={home.tagTxt}>用語</Text></View>
            <View style={home.imgCardIn}>
              <Text style={home.cardH4}>用語問題</Text>
              <Text style={home.cardP}>公式・専門用語を一問一答で</Text>
            </View>
          </Pressable>
          <Pressable style={home.imgCard} onPress={props.onGoCalcQuiz}>
            <ImageBackground source={HOME_IMG.frame} style={StyleSheet.absoluteFill} imageStyle={home.cardImg}>
              <Veil id="veilFrame" stops={[{ o: 0, op: 0.05 }, { o: 0.45, op: 0.5 }, { o: 1, op: 0.94 }]} />
            </ImageBackground>
            <View style={home.tag}><Text style={home.tagTxt}>演習</Text></View>
            <View style={home.imgCardIn}>
              <Text style={home.cardH4}>計算・数値問題</Text>
              <Text style={home.cardP}>手を動かして得点源に</Text>
            </View>
          </Pressable>
        </View>

        {/* 全体サマリ */}
        <View style={[home.card, { paddingVertical: 14 }]}>
          <View style={styles.summaryRow}>
            <Summary t={ht} label="挑戦した問題" value={`${overall.attempted} / ${overall.totalQuestions}`} />
            <Summary t={ht} label="正答率" value={`${Math.round(overall.accuracy * 100)}%`} />
            <Summary t={ht} label="要復習" value={`${props.wrongCount} 問`} />
          </View>
        </View>

        {/* 試験前の準備（モック準拠: 琥珀の淡い温かみ＋下部にデスク画像がマスクでふわっと出る）。
            タップで、いま選んでいる分野×級の「合格・足切りルール」詳細モーダルを開く。 */}
        <Pressable style={home.examCard} onPress={() => setShowExamRule(true)}>
          {/* 琥珀→ネイビーの淡いグラデを土台に敷く（カード全体をほのかに温める） */}
          <Svg style={StyleSheet.absoluteFill} pointerEvents="none">
            <Defs>
              <LinearGradient id="examAmber" x1="0" y1="0" x2="0" y2="1">
                <Stop offset="0" stopColor="#FBBF24" stopOpacity={0.12} />
                <Stop offset="1" stopColor="#0E1728" stopOpacity={0.55} />
              </LinearGradient>
            </Defs>
            <Rect x="0" y="0" width="100%" height="100%" fill="url(#examAmber)" />
          </Svg>
          <View style={home.examBgWrap}>
            {/* 画像を下寄せ配置（机・ノート・PCが見える位置）。上部の窓＝夜景は帯からはみ出して隠れる。
                absoluteFill+coverだと縦中央=窓が出て机が切れるため、bottom固定＋アスペクト比で下端を合わせる。 */}
            <Image source={HOME_IMG.exambg} style={home.examImg} resizeMode="cover" />
            <Svg style={StyleSheet.absoluteFill} pointerEvents="none">
              <Defs>
                <LinearGradient id="examFade" x1="0" y1="0" x2="0" y2="1">
                  <Stop offset="0" stopColor="#0E1728" stopOpacity={1} />
                  <Stop offset="0.42" stopColor="#0E1728" stopOpacity={0.35} />
                  <Stop offset="1" stopColor="#0E1728" stopOpacity={0} />
                </LinearGradient>
              </Defs>
              <Rect x="0" y="0" width="100%" height="100%" fill="url(#examFade)" />
            </Svg>
          </View>
          <View style={home.examIn}>
            <View style={home.examHead}>
              <View style={home.examIco}><Text style={{ fontSize: 20 }}>📋</Text></View>
              <View style={{ flex: 1 }}>
                <Text style={home.missionH3}>試験前の準備</Text>
                <Text style={home.missionP}>本番で力を出し切るために</Text>
              </View>
              <Text style={home.examChev}>›</Text>
            </View>
            {[`${subjectLabel}の足切り・合格ルールを確認`, '持ち物チェック（受験票・電卓・時計 ほか）', '前日に見直す重要公式まとめ'].map((li) => (
              <View key={li} style={home.examLi}><View style={home.examDot} /><Text style={home.examLiTxt}>{li}</Text></View>
            ))}
            <Text style={home.examCautn}>※ タップで詳細 ／ 足切り・持ち込み可否は必ず公式の受験要項でご確認ください</Text>
          </View>
        </Pressable>

        {/* 名言（最後） */}
        <View style={home.quote}>
          <Text style={home.quoteJa}>「解析する力は、いつか世界の構造を支える。」</Text>
          <Text style={home.quoteEn}>ANALYZE · SOLVE · BUILD A BETTER TOMORROW</Text>
        </View>
      </View>
    </ScrollView>

    {/* 分野・級セレクター */}
    <Modal visible={showGrade} transparent animationType="fade" onRequestClose={() => setShowGrade(false)}>
      <Pressable style={home.modalWrap} onPress={() => setShowGrade(false)}>
        <Pressable style={home.sheet} onPress={() => {}}>
          <Text style={home.sheetH}>学習する分野・級を選ぶ</Text>
          {/* 分野×級を1タップで確定できる6ボタン（固体1級/固体2級/熱流体1級/熱流体2級/振動1級/振動2級）。
              「両方を変えたい」時に片方だけ確定してしまう問題を解消。未整備の組は「準備中」で無効化。 */}
          {DISCIPLINES.flatMap((d) =>
            (['g1', 'g2'] as GradeId[]).map((g) => {
              const on = field === d.id && grade === g;
              const ready = disciplineReady(d.id, g);
              return (
                <Pressable
                  key={`${d.id}-${g}`}
                  disabled={!ready}
                  style={[home.opt, on && home.optOn, !ready && { opacity: 0.4 }]}
                  onPress={() => chooseFieldGrade(d.id, g)}
                >
                  <Text style={home.optTxt}>{d.label} {g === 'g1' ? '1級' : '2級'}{ready ? '' : '（準備中）'}</Text>
                </Pressable>
              );
            })
          )}
        </Pressable>
      </Pressable>
    </Modal>

    {/* 合格・足切りルール詳細（いま選んでいる分野×級に連動）。数値は公式案内の原文どおり＋要公式確認。 */}
    <Modal visible={showExamRule} transparent animationType="fade" onRequestClose={() => setShowExamRule(false)}>
      <Pressable style={home.modalWrap} onPress={() => setShowExamRule(false)}>
        <Pressable style={home.sheet} onPress={() => {}}>
          <Text style={home.sheetH}>合格・足切りルール</Text>
          <View style={home.ruleBadge}><Text style={home.ruleBadgeTxt}>{subjectLabel}</Text></View>

          <Text style={home.ruleSecH}>合格の基準（すべて満たすと合格）</Text>
          {examRuleDoc.rules.map((r, i) => (
            <View key={i} style={home.ruleRow}>
              <View style={home.ruleNum}><Text style={home.ruleNumTxt}>{i + 1}</Text></View>
              <Text style={home.ruleTxt}>{r}</Text>
            </View>
          ))}

          <Text style={home.ruleSecH}>かみ砕くと</Text>
          <Text style={home.rulePlain}>{examRuleDoc.plain}</Text>
          {!!examRuleDoc.note && <Text style={home.ruleNote}>{examRuleDoc.note}</Text>}

          {!!examRuleDoc.sourceUrl && (
            <Pressable onPress={() => Linking.openURL(examRuleDoc.sourceUrl!)} hitSlop={8} style={home.ruleSrcBtn}>
              <Text style={home.ruleSrcTxt}>{examRuleDoc.sourceLabel ?? '出典（公式PDF）'}（公式PDFを開く ›）</Text>
            </Pressable>
          )}
          <Text style={home.examCautn}>※ 基準は年度で変わることがあります。受験前に必ず公式の受験要項でご確認ください。</Text>

          <Pressable onPress={() => setShowExamRule(false)} style={home.clearBtn}>
            <Text style={home.clearTxt}>閉じる</Text>
          </Pressable>
        </Pressable>
      </Pressable>
    </Modal>

    </>
  );
}

// ホーム上部のモチベーション帯。継続日数を主役に、今日の学習量・今週の伸び・
// 直近14日の活動棒（高さ=解いた量 / 色=その日の正答率）を1枚に集約する。
function StreakHero(props: { t: Theme; digest: DailyDigest }) {
  const { t, digest } = props;
  const today = digest.last30[digest.last30.length - 1] ?? { n: 0, c: 0 };
  const todayPct = today.n > 0 ? Math.round((today.c / today.n) * 100) : 0;
  const strip = digest.last30.slice(-14); // 直近14日（古い→新しい）
  const maxN = Math.max(1, ...strip.map((d) => d.n));
  const wd = digest.weekDelta;
  const wdColor = wd > 0 ? t.correct : wd < 0 ? t.wrong : t.sub;
  const wdText = wd > 0 ? `▲+${wd}` : wd < 0 ? `▼${wd}` : '±0';
  return (
    <View style={styles.heroWrap}>
      {/* 継続日数タイル（主役） */}
      <View style={[styles.heroStreak, { backgroundColor: t.primary }]}>
        <Text style={styles.heroFlame}>🔥</Text>
        <Text style={styles.heroStreakNum}>{digest.streak}</Text>
        <Text style={styles.heroStreakLabel}>日連続</Text>
      </View>
      {/* 今日 ＋ 今週の伸び ＋ 直近14日の活動 */}
      <View style={[styles.heroRight, { backgroundColor: t.card, borderColor: t.border }]}>
        <View style={styles.heroTopRow}>
          <View style={{ flexShrink: 1 }}>
            <Text style={[styles.heroToday, { color: t.text }]}>
              今日 <Text style={{ color: t.primary }}>{today.n}</Text> 問
            </Text>
            <Text style={[styles.heroTodaySub, { color: t.sub }]}>
              {today.n > 0 ? `正答率 ${todayPct}%` : 'まだ今日の記録なし'}
            </Text>
          </View>
          <View style={{ alignItems: 'flex-end' }}>
            <Text style={[styles.heroWeekDelta, { color: wdColor }]}>{wdText}</Text>
            <Text style={[styles.heroTodaySub, { color: t.sub }]}>今週の正答率</Text>
          </View>
        </View>
        {/* 直近14日：棒の高さ=解いた量 / 色=その日の正答率 */}
        <View style={styles.heroStrip}>
          {strip.map((d, i) => {
            const h = d.n > 0 ? 4 + Math.round((d.n / maxN) * 14) : 3;
            const pct = d.n > 0 ? (d.c / d.n) * 100 : -1;
            const color =
              pct < 0 ? t.border : pct >= 80 ? t.correct : pct >= 50 ? t.amber : t.wrong;
            return <View key={i} style={[styles.heroBar, { height: h, backgroundColor: color }]} />;
          })}
        </View>
      </View>
    </View>
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
  onPickChapter: (c: ChapterEntry) => void;
  onPickTile: (i: number) => void;
  onSelectAnswer: (q: Question, n: number) => void;
  setQIndex: (i: number) => void;
  goBack: (v: StudyView) => void;
  onExitHome: () => void;
  proState: ProState;
  onOpenPaywall: (target: PayTarget | null) => void;
  onOpenFormula: (formulaId: string, itemId: string) => void;
}) {
  const { t } = props;

  // 章の目次（コース＝分野×級はホームの選択に追従。タブ側での課程選択は廃止）
  if (props.view === 'chapters' && props.course) {
    return (
      <ScrollView contentContainerStyle={styles.content}>
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
    // ホームの用語/計算カードから来た専用セットは「__quiz__」。戻る先は章目次でなくホーム。
    const isQuiz = props.chapter.id === '__quiz__';
    return (
      <ScrollView contentContainerStyle={styles.content}>
        <BackLink
          t={t}
          label={isQuiz ? 'ホームへ' : '章の目次へ'}
          onPress={() => (isQuiz ? props.onExitHome() : props.goBack('chapters'))}
        />
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
                  {tileHeading(q)}
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
        onBack={() => props.goBack(props.chapter ? 'tiles' : 'chapters')}
        locked={isLocked(q, props.proState)}
        onOpenPaywall={() => props.onOpenPaywall(payTargetOf(q))}
        onOpenFormula={props.onOpenFormula}
      />
    );
  }

  return null;
}

// タイル見出し。章の問題は title/topic を持つが、ホームの専用セット（用語/計算）は
// title が無いので、問題文の冒頭を見出しに使う（数式記号は簡易に除去して読みやすく）。
function tileHeading(q: Question): string {
  if (q.title) return q.title;
  if (q.topic) return q.topic;
  return (q.question ?? '')
    .replace(/\$+/g, '')
    .replace(/\\[a-zA-Z]+/g, ' ')
    .replace(/[{}\\]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

// 解説文（【基礎】…【引っかけ】…）をラベル別ブロックに分解する。【】が無ければ全体を1ブロック。
function parseExplanation(text: string): { label: string | null; body: string }[] {
  const out: { label: string | null; body: string }[] = [];
  const re = /【([^】]+)】/g;
  let m: RegExpExecArray | null;
  let idx = 0;
  let cur: string | null = null;
  while ((m = re.exec(text)) !== null) {
    const body = text.slice(idx, m.index).trim();
    if (body) out.push({ label: cur, body });
    cur = m[1];
    idx = re.lastIndex;
  }
  const tail = text.slice(idx).trim();
  if (tail) out.push({ label: cur, body: tail });
  if (out.length === 0 && text.trim()) out.push({ label: null, body: text.trim() });
  return out;
}

// 解説ラベルの色（意味で色分け）。基礎=控えめ / ポイント=緑 / 引っかけ=アンバー / その他=主色。
function sectionAccent(t: Theme, label: string | null): string {
  if (!label) return t.sub;
  if (label.indexOf('ポイント') >= 0) return t.correct;
  if (label.indexOf('引っかけ') >= 0 || label.indexOf('注意') >= 0) return t.amber;
  if (label.indexOf('基礎') >= 0) return t.sub;
  return t.primary;
}

// 問題に紐づく関連用語・公式を、その問題の章の formulas から解決する。
// （章 id は級間で衝突するため QUESTION_FORMULA_ID で必ず formulaId を引く）
function relatedFormulaItems(q: Question): FormulaItem[] {
  const ids = q.relatedFormulas;
  if (!ids || ids.length === 0) return [];
  const doc = formulaDoc(QUESTION_FORMULA_ID[q.id]);
  if (!doc) return [];
  const byId = new Map(doc.items.map((it) => [it.id, it]));
  return ids
    .map((id) => byId.get(id))
    .filter((x): x is FormulaItem => !!x);
}

// 横スワイプで前後移動。縦スクロールは邪魔しない（横成分が縦より十分大きい時だけ発火）。
function useSwipeNav(onLeft: () => void, onRight: () => void) {
  const cb = useRef({ onLeft, onRight });
  cb.current = { onLeft, onRight };
  const pan = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: (_e, g) =>
        Math.abs(g.dx) > 24 && Math.abs(g.dx) > Math.abs(g.dy) * 1.8,
      onPanResponderRelease: (_e, g) => {
        if (g.dx <= -50) cb.current.onLeft();
        else if (g.dx >= 50) cb.current.onRight();
      },
    })
  ).current;
  return pan.panHandlers;
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
  onOpenFormula: (formulaId: string, itemId: string) => void;
}) {
  const { t, q, selected, past } = props;
  const locked = props.locked;
  const answered = selected !== null;
  const isCorrect = selected === q.answer;
  const atFirst = props.index === 0;
  const atLast = props.index === props.total - 1;
  const pastRate = past && past.attempts > 0 ? Math.round((past.correctCount / past.attempts) * 100) : 0;
  const related = relatedFormulaItems(q);
  const relFormulaId = QUESTION_FORMULA_ID[q.id];
  // 左スワイプ=次の問題 / 右スワイプ=前の問題（ボタンと同じ動作。両端はクランプ済）
  const pan = useSwipeNav(props.onNext, props.onPrev);

  return (
    <View style={{ flex: 1 }} {...pan}>
    <ScrollView contentContainerStyle={styles.content}>
      {/* 上部バー：戻る・課程/章・問番号 */}
      <View style={styles.qTopbar}>
        <Pressable onPress={props.onBack} hitSlop={8} style={[styles.qChev, { backgroundColor: t.card }]}>
          <Text style={[styles.qChevTxt, { color: t.text }]}>‹</Text>
        </Pressable>
        <Text style={[styles.qSetLabel, { color: t.sub }]} numberOfLines={1}>
          {props.title}
        </Text>
        <View style={[styles.qCounter, { backgroundColor: t.primary + '18' }]}>
          <Text style={[styles.qCounterTxt, { color: t.primary }]}>
            {props.index + 1} / {props.total}
          </Text>
        </View>
      </View>

      {/* 進捗バー */}
      <View style={[styles.qTrack, { backgroundColor: t.border }]}>
        <View
          style={[
            styles.qTrackFill,
            { backgroundColor: t.primary, width: `${Math.round(((props.index + 1) / props.total) * 100)}%` },
          ]}
        />
      </View>

      {/* チップ：学習履歴・公式対応 */}
      <View style={styles.qChipRow}>
        <View
          style={[
            styles.qChip,
            { backgroundColor: (past ? (past.lastCorrect ? t.correct : t.wrong) : t.sub) + '18' },
          ]}
        >
          {past ? (
            <>
              <View style={[styles.qChipDot, { backgroundColor: past.lastCorrect ? t.correct : t.wrong }]} />
              <Text style={[styles.qChipTxt, { color: past.lastCorrect ? t.correct : t.wrong }]}>
                前回{past.lastCorrect ? '◯' : '✕'} {pastRate}%
              </Text>
            </>
          ) : (
            <Text style={[styles.qChipTxt, { color: t.sub }]}>未挑戦</Text>
          )}
        </View>
        {q.officialRef ? (
          <View style={[styles.qChip, { backgroundColor: t.primary + '18' }]}>
            <Text style={[styles.qChipTxt, { color: t.primary }]}>
              公式 {q.officialRef.replace(/^問/, '')}{q.role === 'branch' ? '（補足）' : ''}
            </Text>
          </View>
        ) : null}
      </View>

      {/* 問題文（主役・余白広め） */}
      <View style={styles.qQuestion}>
        <RichText text={q.question} color={t.text} fontSize={18} bold />
      </View>

      {/* 図：解答に必要(figure:'required')なら常時。それ以外(helpful等)は答えを示唆しうるので回答後のみ出す。 */}
      {!locked && q.figureImage && hasFigure(q.figureImage) && (q.figure === 'required' || answered) ? (
        <View style={[styles.qFigCard, { backgroundColor: t.card }]}>
          <AutoFigure t={t} source={figureSource(q.figureImage)} />
        </View>
      ) : null}

      {/* 選択肢：丸番号カード */}
      <View style={styles.qChoices}>
        {q.choices.map((choice, i) => {
          const num = i + 1;
          // ロック中は正誤の色分け（＝正解の露出）をしない。タップは購入導線へ。
          const c = locked
            ? choiceColor(t, { num, answer: -1, selected: null, answered: false })
            : choiceColor(t, { num, answer: q.answer, selected, answered });
          const isAns = !locked && answered && num === q.answer;
          return (
            <Pressable
              key={num}
              onPress={() => (locked ? props.onOpenPaywall() : props.onSelect(num))}
              style={[styles.qOpt, { backgroundColor: c.bg, borderColor: c.border }]}
            >
              <View style={[styles.qOptIdx, { backgroundColor: isAns ? t.correct : t.border }]}>
                <Text style={[styles.qOptIdxTxt, { color: isAns ? '#ffffff' : t.sub }]}>{num}</Text>
              </View>
              <View style={styles.qOptTxt}>
                <RichText text={choice} color={c.text} fontSize={15} />
              </View>
              {isAns ? <Text style={[styles.qOptTick, { color: t.correct }]}>✓</Text> : null}
            </Pressable>
          );
        })}
      </View>

      {/* 解説：正誤＋ラベル別ブロック */}
      {!locked && answered && (
        <View style={[styles.qExplain, { backgroundColor: t.card }]}>
          <View style={styles.qVerdictRow}>
            <View style={[styles.qVerdictPill, { backgroundColor: isCorrect ? t.correct : t.wrong }]}>
              <Text style={styles.qVerdictPillTxt}>{isCorrect ? '正解' : '不正解'}</Text>
            </View>
            <Text style={[styles.qVerdictAns, { color: t.sub }]}>正解は {q.answer}</Text>
          </View>
          {parseExplanation(q.explanation).map((sec, i) => {
            const accent = sectionAccent(t, sec.label);
            return (
              <View key={i} style={styles.qSec}>
                {sec.label ? (
                  <View style={[styles.qSecLabel, { backgroundColor: accent + '22' }]}>
                    <Text style={[styles.qSecLabelTxt, { color: accent }]}>{sec.label}</Text>
                  </View>
                ) : null}
                <RichText text={sec.body} color={t.text} fontSize={14} />
              </View>
            );
          })}
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

      {/* 関連する用語・公式（無料。タップで公式・用語カードへ移動） */}
      {related.length > 0 ? (
        <View style={[styles.qRelated, { backgroundColor: t.card }]}>
          <Text style={[styles.qRelatedHead, { color: t.sub }]}>関連する用語・公式</Text>
          <View style={styles.qRelatedRow}>
            {related.map((it) => (
              <Pressable
                key={it.id}
                onPress={() => props.onOpenFormula(relFormulaId, it.id)}
                style={[styles.qRelatedChip, { borderColor: t.border, backgroundColor: t.bg }]}
              >
                <View
                  style={[
                    styles.qRelatedBadge,
                    { backgroundColor: it.kind === 'formula' ? t.primary : t.reviewBtn },
                  ]}
                >
                  <Text style={styles.qRelatedBadgeTxt}>{it.kind === 'formula' ? '公式' : '用語'}</Text>
                </View>
                <Text style={[styles.qRelatedTxt, { color: t.text }]} numberOfLines={1}>
                  {it.term}
                </Text>
                <Text style={[styles.qRelatedChev, { color: t.sub }]}>›</Text>
              </Pressable>
            ))}
          </View>
        </View>
      ) : null}

      {/* 前へ / 次の問題へ */}
      <View style={styles.qNav}>
        <Pressable
          onPress={props.onPrev}
          disabled={atFirst}
          style={[styles.qNavPrev, { borderColor: t.border, opacity: atFirst ? 0.4 : 1 }]}
        >
          <Text style={[styles.qNavPrevTxt, { color: t.sub }]}>‹ 前へ</Text>
        </Pressable>
        <Pressable
          onPress={props.onNext}
          disabled={atLast}
          style={[styles.qNavNext, { backgroundColor: t.primary, opacity: atLast ? 0.4 : 1 }]}
        >
          <Text style={styles.qNavNextTxt}>次の問題へ ›</Text>
        </Pressable>
      </View>

      {/* 非公認の注記（毎問の長文はやめ、下に小さく） */}
      {q.officialRef ? (
        <Text style={[styles.qDisclaimer, { color: t.sub }]}>
          本アプリは非公認の独自補助教材です。番号は対応学習用の参照です。
        </Text>
      ) : null}
    </ScrollView>
    </View>
  );
}

// ================= 公式・用語タブ =================
function FormulaTab(props: {
  t: Theme;
  view: FormulaView;
  course: Course | null;
  chapterId: string | null;
  itemId: string | null;
  onOpenChapter: (id: string) => void;
  onOpenItem: (itemId: string) => void;
  onBack: (v: FormulaView) => void;
  fromStudy?: boolean;
  onBackToStudy?: () => void;
}) {
  const { t } = props;

  // 個別解説（タイトルをタップ、または問題からのリンクで飛んでくる画面）
  if (props.view === 'item' && props.chapterId && props.itemId) {
    return (
      <FormulaItemScreen
        t={t}
        chapterId={props.chapterId}
        itemId={props.itemId}
        fromStudy={props.fromStudy}
        onBackToStudy={props.onBackToStudy}
        onOpenItem={props.onOpenItem}
        onBackToList={() => props.onBack('titles')}
      />
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

  // 章の一覧（コース＝分野×級はホームの選択に追従。タブ側での課程選択は廃止）
  if (props.view === 'chapters' && props.course) {
    return (
      <ScrollView contentContainerStyle={styles.content}>
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

  // 選択中の分野×級がまだ準備中（章なし）の場合のフォールバック。
  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>公式・用語</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>この分野・級は準備中です。</Text>
    </ScrollView>
  );
}

// 公式・用語の個別ページ。隣の項目へボタン/スワイプで移動。問題から来た時は「問題に戻る」を出す。
function FormulaItemScreen(props: {
  t: Theme;
  chapterId: string;
  itemId: string;
  fromStudy?: boolean;
  onBackToStudy?: () => void;
  onOpenItem: (itemId: string) => void;
  onBackToList: () => void;
}) {
  const { t } = props;
  const doc = formulaDoc(props.chapterId);
  const items = doc?.items ?? [];
  const idx = items.findIndex((x) => x.id === props.itemId);
  const item = idx >= 0 ? items[idx] : undefined;
  const prev = idx > 0 ? items[idx - 1] : null;
  const next = idx >= 0 && idx < items.length - 1 ? items[idx + 1] : null;
  const goPrev = () => { if (prev) props.onOpenItem(prev.id); };
  const goNext = () => { if (next) props.onOpenItem(next.id); };
  const pan = useSwipeNav(goNext, goPrev); // 左スワイプ=次 / 右スワイプ=前

  return (
    <View style={{ flex: 1 }} {...pan}>
      <ScrollView contentContainerStyle={styles.content}>
        {props.fromStudy && props.onBackToStudy ? (
          <BackLink t={t} label="問題に戻る" onPress={props.onBackToStudy} />
        ) : (
          <BackLink t={t} label="公式・用語の一覧へ" onPress={props.onBackToList} />
        )}
        {item ? (
          <>
            <FormulaCard t={t} item={item} />
            {/* 隣の用語へ（スワイプでも移動可） */}
            <View style={styles.qNav}>
              <Pressable
                onPress={goPrev}
                disabled={!prev}
                style={[styles.qNavPrev, { borderColor: t.border, opacity: prev ? 1 : 0.4 }]}
              >
                <Text style={[styles.qNavPrevTxt, { color: t.sub }]}>‹ 前の用語</Text>
              </Pressable>
              <Pressable
                onPress={goNext}
                disabled={!next}
                style={[styles.qNavNext, { backgroundColor: t.primary, opacity: next ? 1 : 0.4 }]}
              >
                <Text style={styles.qNavNextTxt}>次の用語 ›</Text>
              </Pressable>
            </View>
            {/* 問題から来た時は、一覧へも行けるよう下に補助リンク */}
            {props.fromStudy ? (
              <BackLink t={t} label="公式・用語の一覧へ" onPress={props.onBackToList} />
            ) : null}
          </>
        ) : (
          <Text style={[styles.bodyText, { color: t.sub }]}>項目が見つかりません。</Text>
        )}
      </ScrollView>
    </View>
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
      {item.figureImage && hasFigure(item.figureImage) ? <AutoFigure t={t} source={figureSource(item.figureImage)} /> : null}
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
}) {
  const { t } = props;
  // バージョン表示を7回タップで開発用ロック解除（隠しジェスチャ）。
  // 【公開方針 2026-09-20】発売版では裏口を一切残さない＝開発中(__DEV__)のみ有効。
  // 公開/TestFlightビルド(__DEV__=false)では何も起きない。開発者の無料利用は ASC のオファーコード(100%割引)で行う。
  const [verTaps, setVerTaps] = useState(0);
  function onTapVersion() {
    if (!__DEV__) return; // 本番では隠しジェスチャを無効化
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

  function confirmReset() {
    Alert.alert('学習記録をリセット', '正誤や日付の記録をすべて消します。よろしいですか？（元に戻せません）', [
      { text: 'キャンセル', style: 'cancel' },
      { text: 'リセットする', style: 'destructive', onPress: props.onReset },
    ]);
  }

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>設定</Text>

      <Text style={[styles.sectionHead, { color: t.text }]}>購入</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        {ENTITLEMENTS.map((e, i) => {
          const owned = props.devPro || props.owned.includes(e.key);
          return (
            <InfoRow
              key={e.key}
              t={t}
              label={e.title}
              value={owned ? '解除済み' : '未購入'}
              last={i === ENTITLEMENTS.length - 1}
            />
          );
        })}
      </View>
      {/* 級ごとの個別ボタンはやめ、「プレミアムの購入」1つに集約。押すと購入画面（Paywallで級を選ぶ）を開く。 */}
      <Button t={t} kind="primary" label="プレミアムの購入" onPress={() => props.onOpenPaywall(null)} />
      <Button t={t} kind="ghost" label="購入を復元する" onPress={props.onRestoreAll} />

      <Text style={[styles.sectionHead, { color: t.text }]}>学習記録</Text>
      <Button t={t} kind="danger" label="学習記録をリセット" onPress={confirmReset} />

      <Text style={[styles.sectionHead, { color: t.text }]}>このアプリについて</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <Text style={[styles.bodyText, { color: t.sub }]}>
          計算力学技術者（CAE）試験の対策アプリです。収録している問題・解説・図はすべてオリジナルで作成しています。学習の記録は端末内に保存されます。
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

      {/* お問い合わせ導線：JLPT等 別アプリと同じ受信箱を共有するため、件名に【CAE】を自動付与して混同を防ぐ。 */}
      <Text style={[styles.sectionHead, { color: t.text }]}>お問い合わせ</Text>
      <View style={[styles.card, { backgroundColor: t.card, borderColor: t.border }]}>
        <Pressable onPress={() => Linking.openURL(SUPPORT_MAILTO_URL)} style={{ paddingVertical: 10 }} hitSlop={8}>
          <Text style={[styles.bodyText, { color: t.primary }]}>お問い合わせ（メール）</Text>
        </Pressable>
        <Text style={[styles.bodyText, { color: t.sub, fontSize: 12 }]}>
          タップするとメールが開き、件名に「【CAE】お問い合わせ」が自動で入ります。
        </Text>
      </View>

      {/* 開発用：Proモード全解除(devPro)トグル。開発中(__DEV__)のみ表示。
          公開/TestFlightビルドでは表示されない＝一般ユーザーに裏口を見せない（2026-09-20 公開方針）。 */}
      {__DEV__ && (
        <>
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
        </>
      )}

      {/* 最下部のバージョン表示。7回タップで開発用ロック解除（隠しジェスチャ）。 */}
      <Pressable onPress={onTapVersion} style={styles.versionFooter} hitSlop={8}>
        <Text style={[styles.versionText, { color: t.sub }]}>
          計算力学技術者　v{APP_VERSION}{props.devPro ? '　・　開発ロック解除中' : ''}
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
  const textColor = props.kind === 'ghost' ? t.sub : props.kind === 'primary' ? t.onPrimary : '#ffffff';
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
// 配色は「ネイビー1色を主役」に統一。中立色（白/グレー）＋正誤の緑・赤だけを添える。
// primary=ブランドのネイビー、reviewBtn=同系のセカンダリ青（色相を増やさない）、
// amber=「引っかけ/中位」を示す唯一の暖色アクセント。ビビッド・紫は使わない。
type Theme = typeof light;
const light = {
  bg: '#ffffff',
  text: '#16233a', // ネイビー寄りの濃色（黒より柔らかく統一感）
  sub: '#5f6b7a',
  card: '#f4f6f9',
  border: '#e3e8ef',
  primary: '#1f3d63', // ブランドのネイビー（ボタン・選択・ヘッダー・レーダー）
  reviewBtn: '#3a6491', // 同じ青系のセカンダリ（復習・用語バッジ）
  amber: '#d98a2b', // 唯一の暖色アクセント（注意・中位の正答率）
  disabled: '#c8ccd2',
  correct: '#2f9e63', // ソフトな緑（正解フィードバック専用）
  correctBg: '#e6f4ec',
  wrong: '#d1544f', // ソフトな赤（不正解フィードバック専用）
  wrongBg: '#fbe9e8',
  onPrimary: '#ffffff', // primary（塗り）の上に載せる文字色
};
const dark: Theme = {
  bg: '#0f1115',
  text: '#eef1f5',
  sub: '#9aa4b0',
  card: '#171b22',
  border: '#29303a',
  primary: '#3d6aa6', // ネイビーの明るめ（暗背景で白文字が読める）
  reviewBtn: '#5586bd',
  amber: '#dd9a3a',
  disabled: '#3a3f47',
  correct: '#35b877',
  correctBg: '#12291d',
  wrong: '#e0625d',
  wrongBg: '#2a1514',
  onPrimary: '#ffffff',
};

// FEMネイビー世界観をアプリ全体に適用するテーマ（ホームと同じ暗色＋シアンのアクセント）。
// ホーム＝HOMEパレット、その他タブ＝この navy を使い、全画面で世界観を統一する。
const navy: Theme = {
  bg: '#060A13',        // HOME.bg0
  text: '#EAF2FF',      // HOME.text
  sub: '#8CA1C1',       // HOME.muted
  card: '#0E1728',      // HOME.bg2（不透明カード＝読みやすさ確保）
  border: 'rgba(125,199,255,0.18)',
  primary: '#3BE6F2',   // HOME.cyan（主ボタン。上の文字は onPrimary の濃紺）
  reviewBtn: '#0B93B4', // HOME.cyanDeep（セカンダリ）
  amber: '#FBBF24',     // HOME.warn
  disabled: '#2A3852',
  correct: '#4ADE80',   // HOME.good
  correctBg: 'rgba(74,222,128,0.16)',
  wrong: '#FB7185',     // HOME.bad
  wrongBg: 'rgba(251,113,133,0.16)',
  onPrimary: '#06121F', // シアンの上は濃紺文字（白だと読めない）
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
  // モチベーション帯（継続日数・今日・活動棒）
  heroWrap: { flexDirection: 'row', marginBottom: 12 },
  heroStreak: { width: 96, borderRadius: 12, paddingVertical: 12, marginRight: 10, alignItems: 'center', justifyContent: 'center' },
  heroFlame: { fontSize: 22 },
  heroStreakNum: { color: '#fff', fontSize: 30, fontWeight: 'bold', lineHeight: 34 },
  heroStreakLabel: { color: '#fff', fontSize: 12, opacity: 0.9 },
  heroRight: { flex: 1, borderWidth: 1, borderRadius: 12, padding: 12, justifyContent: 'space-between' },
  heroTopRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  heroToday: { fontSize: 18, fontWeight: 'bold' },
  heroTodaySub: { fontSize: 11, marginTop: 2 },
  heroWeekDelta: { fontSize: 18, fontWeight: 'bold' },
  heroStrip: { flexDirection: 'row', alignItems: 'flex-end', height: 20, marginTop: 10 },
  heroBar: { flex: 1, borderRadius: 2, marginHorizontal: 1.5, minWidth: 3 },
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

  // 出題（新デザイン）
  qTopbar: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 12 },
  qChev: { width: 34, height: 34, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  qChevTxt: { fontSize: 20, fontWeight: '700', lineHeight: 22, marginTop: -2 },
  qSetLabel: { flex: 1, fontSize: 12, fontWeight: '600' },
  qCounter: { paddingHorizontal: 11, paddingVertical: 6, borderRadius: 999 },
  qCounterTxt: { fontSize: 12, fontWeight: '700', fontVariant: ['tabular-nums'] },
  qTrack: { height: 5, borderRadius: 999, overflow: 'hidden', marginBottom: 18 },
  qTrackFill: { height: '100%', borderRadius: 999 },
  qChipRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 7, marginBottom: 16 },
  qChip: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 6, borderRadius: 999 },
  qChipDot: { width: 7, height: 7, borderRadius: 4 },
  qChipTxt: { fontSize: 12, fontWeight: '700' },
  qQuestion: { marginBottom: 20 },
  qFigCard: { borderRadius: 14, padding: 12, marginBottom: 20 },
  qChoices: { gap: 10 },
  qOpt: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 1.5, borderRadius: 15, paddingVertical: 12, paddingHorizontal: 14 },
  qOptIdx: { width: 26, height: 26, borderRadius: 13, alignItems: 'center', justifyContent: 'center' },
  qOptIdxTxt: { fontSize: 13, fontWeight: '700' },
  qOptTxt: { flex: 1 },
  qOptTick: { fontSize: 16, fontWeight: '800' },
  qExplain: { borderRadius: 18, padding: 16, marginTop: 20 },
  qVerdictRow: { flexDirection: 'row', alignItems: 'center', gap: 9, marginBottom: 6 },
  qVerdictPill: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 999 },
  qVerdictPillTxt: { color: '#ffffff', fontSize: 12, fontWeight: '800' },
  qVerdictAns: { fontSize: 12, fontWeight: '600' },
  qSec: { marginTop: 14 },
  qSecLabel: { alignSelf: 'flex-start', paddingHorizontal: 9, paddingVertical: 4, borderRadius: 7, marginBottom: 7 },
  qSecLabelTxt: { fontSize: 11, fontWeight: '800', letterSpacing: 0.3 },
  qRelated: { marginTop: 16, padding: 14, borderRadius: 14 },
  qRelatedHead: { fontSize: 11, fontWeight: '800', letterSpacing: 0.3, marginBottom: 9 },
  qRelatedRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  qRelatedChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 7,
    paddingHorizontal: 10,
    paddingVertical: 8,
    borderRadius: 11,
    borderWidth: 1.5,
    maxWidth: '100%',
  },
  qRelatedBadge: { paddingHorizontal: 7, paddingVertical: 2, borderRadius: 6 },
  qRelatedBadgeTxt: { color: '#ffffff', fontSize: 10, fontWeight: '800' },
  qRelatedTxt: { fontSize: 13, fontWeight: '700', flexShrink: 1 },
  qRelatedChev: { fontSize: 16, fontWeight: '700' },
  qNav: { flexDirection: 'row', gap: 11, marginTop: 22 },
  qNavPrev: { paddingVertical: 14, paddingHorizontal: 18, borderRadius: 14, borderWidth: 1.5 },
  qNavPrevTxt: { fontSize: 14, fontWeight: '700' },
  qNavNext: { flex: 1, alignItems: 'center', paddingVertical: 14, borderRadius: 14 },
  qNavNextTxt: { color: '#ffffff', fontSize: 14, fontWeight: '800' },
  qDisclaimer: { fontSize: 10, textAlign: 'center', lineHeight: 15, marginTop: 16 },

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
