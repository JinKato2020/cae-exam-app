import { useEffect, useMemo, useState } from 'react';
import {
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  useColorScheme,
  View,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

import type { AnswerRecord, Question } from './src/types';
import { loadWrongIds, updateWrongIds } from './src/storage';
import {
  CATALOG,
  questionsByIds,
  type ChapterEntry,
  type FieldEntry,
  type GradeEntry,
} from './src/catalog';

type Screen = 'field' | 'grade' | 'chapter' | 'questions' | 'quiz' | 'result';
type Source = 'chapter' | 'single' | 'review';

export default function App() {
  const scheme = useColorScheme();
  const t = scheme === 'dark' ? dark : light;

  const [screen, setScreen] = useState<Screen>('field');
  const [field, setField] = useState<FieldEntry | null>(null);
  const [grade, setGrade] = useState<GradeEntry | null>(null);
  const [chapter, setChapter] = useState<ChapterEntry | null>(null);
  const [wrongIds, setWrongIds] = useState<string[]>([]);

  // 出題状態
  const [quiz, setQuiz] = useState<Question[]>([]);
  const [quizTitle, setQuizTitle] = useState('');
  const [source, setSource] = useState<Source>('chapter');
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [records, setRecords] = useState<AnswerRecord[]>([]);

  useEffect(() => {
    loadWrongIds().then(setWrongIds);
  }, []);

  const wrongQuestions = useMemo(() => questionsByIds(wrongIds), [wrongIds]);

  function beginQuiz(list: Question[], title: string, src: Source) {
    if (list.length === 0) return;
    setQuiz(list);
    setQuizTitle(title);
    setSource(src);
    setIndex(0);
    setSelected(null);
    setRecords([]);
    setScreen('quiz');
  }

  const current = quiz[index];
  const answered = selected !== null;

  function onSelect(choiceNum: number) {
    if (answered) return;
    setSelected(choiceNum);
    setRecords((r) => [...r, { id: current.id, correct: choiceNum === current.answer }]);
  }

  async function onNext() {
    if (index + 1 < quiz.length) {
      setIndex(index + 1);
      setSelected(null);
      return;
    }
    const next = await updateWrongIds(wrongIds, records);
    setWrongIds(next);
    setScreen('result');
  }

  const quitTarget: Screen = source === 'review' ? 'field' : 'questions';

  // ---------- 描画 ----------
  return (
    <SafeAreaProvider>
      <SafeAreaView style={[styles.container, { backgroundColor: t.bg }]}>
        <StatusBar style={scheme === 'dark' ? 'light' : 'dark'} />

        {screen === 'field' && (
          <ListScreen
            t={t}
            title="CAE 試験対策"
            subtitle="分野を選んでください"
            items={CATALOG.map((f) => ({
              key: f.id,
              label: f.name,
              sub: chapterCount(f) > 0 ? `${chapterCount(f)} 章` : '準備中',
              disabled: chapterCount(f) === 0,
              onPress: () => {
                setField(f);
                setScreen('grade');
              },
            }))}
            reviewCount={wrongQuestions.length}
            onReview={() => beginQuiz(wrongQuestions, '間違い復習', 'review')}
          />
        )}

        {screen === 'grade' && field && (
          <ListScreen
            t={t}
            title={field.name}
            subtitle="級を選んでください"
            onBack={() => setScreen('field')}
            items={field.grades.map((g) => ({
              key: g.id,
              label: g.name,
              sub: g.chapters.length > 0 ? `${g.chapters.length} 章` : '準備中',
              disabled: g.chapters.length === 0,
              onPress: () => {
                setGrade(g);
                setScreen('chapter');
              },
            }))}
          />
        )}

        {screen === 'chapter' && field && grade && (
          <ListScreen
            t={t}
            title={`${field.name}／${grade.name}`}
            subtitle="章を選んでください"
            onBack={() => setScreen('grade')}
            items={grade.chapters.map((c) => ({
              key: c.id,
              label: c.title,
              sub: `${c.data.questions.length} 問`,
              onPress: () => {
                setChapter(c);
                setScreen('questions');
              },
            }))}
          />
        )}

        {screen === 'questions' && chapter && (
          <ListScreen
            t={t}
            title={chapter.title}
            subtitle="問題を選ぶ（1問だけ挑戦）／または全問に挑戦"
            onBack={() => setScreen('chapter')}
            topAction={{
              label: `全 ${chapter.data.questions.length} 問に挑戦（順番に）`,
              onPress: () => beginQuiz(chapter.data.questions, chapter.title, 'chapter'),
            }}
            items={chapter.data.questions.map((q) => ({
              key: q.id,
              label: `${q.number}　${q.title ?? q.topic ?? ''}`,
              sub: wrongIds.includes(q.id) ? '前回まちがえた問題' : undefined,
              onPress: () =>
                beginQuiz([q], `${chapter.title}　${q.number}`, 'single'),
            }))}
          />
        )}

        {screen === 'quiz' && current && (
          <QuizScreen
            t={t}
            title={quizTitle}
            q={current}
            index={index}
            total={quiz.length}
            selected={selected}
            answered={answered}
            onSelect={onSelect}
            onNext={onNext}
            onQuit={() => setScreen(quitTarget)}
          />
        )}

        {screen === 'result' && (
          <ResultScreen
            t={t}
            title={quizTitle}
            quiz={quiz}
            records={records}
            wrongCount={wrongQuestions.length}
            onRetry={() => beginQuiz(quiz, quizTitle, source)}
            onReview={() => beginQuiz(wrongQuestions, '間違い復習', 'review')}
            onBackList={() => setScreen(quitTarget)}
            onHome={() => setScreen('field')}
          />
        )}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

function chapterCount(f: FieldEntry): number {
  return f.grades.reduce((n, g) => n + g.chapters.length, 0);
}

// ---------- 一覧画面（分野/級/章/問題 共通） ----------
function ListScreen(props: {
  t: Theme;
  title: string;
  subtitle: string;
  items: {
    key: string;
    label: string;
    sub?: string;
    disabled?: boolean;
    onPress: () => void;
  }[];
  onBack?: () => void;
  topAction?: { label: string; onPress: () => void };
  reviewCount?: number;
  onReview?: () => void;
}) {
  const { t } = props;
  return (
    <ScrollView contentContainerStyle={styles.content}>
      {props.onBack && (
        <Pressable onPress={props.onBack} style={styles.back}>
          <Text style={[styles.backText, { color: t.primary }]}>‹ 戻る</Text>
        </Pressable>
      )}
      <Text style={[styles.title, { color: t.text }]}>{props.title}</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>{props.subtitle}</Text>

      {props.topAction && (
        <Button t={t} kind="primary" label={props.topAction.label} onPress={props.topAction.onPress} />
      )}
      {props.topAction && <View style={{ height: 8 }} />}

      {props.items.map((it) => (
        <Pressable
          key={it.key}
          onPress={it.disabled ? undefined : it.onPress}
          style={[
            styles.row,
            { backgroundColor: t.card, borderColor: t.border, opacity: it.disabled ? 0.5 : 1 },
          ]}
        >
          <Text style={[styles.rowLabel, { color: t.text }]}>{it.label}</Text>
          {it.sub && <Text style={[styles.rowSub, { color: t.wrong }]}>{it.sub}</Text>}
        </Pressable>
      ))}

      {props.onReview && (
        <Button
          t={t}
          kind="review"
          disabled={(props.reviewCount ?? 0) === 0}
          label={
            (props.reviewCount ?? 0) > 0
              ? `間違いだけ復習（${props.reviewCount} 問）`
              : '復習する間違いはありません'
          }
          onPress={props.onReview}
        />
      )}
    </ScrollView>
  );
}

// ---------- 出題 ----------
function QuizScreen(props: {
  t: Theme;
  title: string;
  q: Question;
  index: number;
  total: number;
  selected: number | null;
  answered: boolean;
  onSelect: (n: number) => void;
  onNext: () => void;
  onQuit: () => void;
}) {
  const { t, q, answered, selected } = props;
  const isCorrect = selected === q.answer;
  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Pressable onPress={props.onQuit} style={styles.back}>
        <Text style={[styles.backText, { color: t.primary }]}>‹ やめる</Text>
      </Pressable>
      <Text style={[styles.progress, { color: t.sub }]}>
        {props.title}　{props.index + 1} / {props.total}
        {q.title ? `　・　${q.title}` : ''}
      </Text>
      <Text style={[styles.question, { color: t.text }]}>{q.question}</Text>

      {q.choices.map((choice, i) => {
        const num = i + 1;
        const c = choiceColor(t, { num, answer: q.answer, selected, answered });
        return (
          <Pressable
            key={num}
            onPress={() => props.onSelect(num)}
            style={[styles.choice, { backgroundColor: c.bg, borderColor: c.border }]}
          >
            <Text style={[styles.choiceText, { color: c.text }]}>
              {num}. {choice}
            </Text>
          </Pressable>
        );
      })}

      {answered && (
        <View style={[styles.explainBox, { backgroundColor: t.card, borderColor: t.border }]}>
          <Text style={[styles.verdict, { color: isCorrect ? t.correct : t.wrong }]}>
            {isCorrect ? '◯ 正解' : '✕ 不正解'}（正解：{q.answer}）
          </Text>
          <Text style={[styles.explainText, { color: t.text }]}>{q.explanation}</Text>
          {q.figure ? (
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.figureWrap}>
              <Text style={[styles.figure, { color: t.text, borderColor: t.border, backgroundColor: t.bg }]}>
                {q.figure}
              </Text>
            </ScrollView>
          ) : null}
        </View>
      )}

      {answered && (
        <Button
          t={t}
          kind="primary"
          label={props.index + 1 < props.total ? '次へ' : '結果を見る'}
          onPress={props.onNext}
        />
      )}
    </ScrollView>
  );
}

// ---------- 結果 ----------
function ResultScreen(props: {
  t: Theme;
  title: string;
  quiz: Question[];
  records: AnswerRecord[];
  wrongCount: number;
  onRetry: () => void;
  onReview: () => void;
  onBackList: () => void;
  onHome: () => void;
}) {
  const { t } = props;
  const correct = props.records.filter((r) => r.correct).length;
  const total = props.quiz.length;
  const pct = total > 0 ? Math.round((correct / total) * 100) : 0;
  const wrong = props.quiz.filter(
    (q) => props.records.find((r) => r.id === q.id)?.correct === false
  );
  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>結果</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>{props.title}</Text>
      <Text style={[styles.score, { color: t.text }]}>
        {correct} / {total} 問正解（{pct}%）
      </Text>

      {wrong.length > 0 ? (
        <View style={{ width: '100%', marginTop: 8 }}>
          <Text style={[styles.subtitle, { color: t.sub }]}>間違えた問題</Text>
          {wrong.map((q) => (
            <View
              key={q.id}
              style={[styles.row, { backgroundColor: t.card, borderColor: t.border }]}
            >
              <Text style={[styles.rowSub, { color: t.wrong, marginBottom: 4 }]}>
                {q.number}　{q.title ?? q.topic ?? ''}
              </Text>
              <Text style={[styles.rowLabel, { color: t.text, fontWeight: '400' }]}>
                {q.question}
              </Text>
            </View>
          ))}
        </View>
      ) : (
        <Text style={[styles.note, { color: t.correct }]}>全問正解です！</Text>
      )}

      <View style={{ height: 8 }} />
      <Button t={t} kind="primary" label="もう一度" onPress={props.onRetry} />
      <Button
        t={t}
        kind="review"
        disabled={props.wrongCount === 0}
        label={props.wrongCount > 0 ? `間違いだけ復習（${props.wrongCount} 問）` : '復習する間違いはありません'}
        onPress={props.onReview}
      />
      <Button t={t} kind="ghost" label="問題一覧へ戻る" onPress={props.onBackList} />
      <Button t={t} kind="ghost" label="ホームへ" onPress={props.onHome} />
    </ScrollView>
  );
}

// ---------- 共通ボタン ----------
function Button(props: {
  t: Theme;
  label: string;
  kind: 'primary' | 'review' | 'ghost';
  disabled?: boolean;
  onPress: () => void;
}) {
  const { t } = props;
  const base =
    props.kind === 'primary' ? t.primary : props.kind === 'review' ? t.reviewBtn : 'transparent';
  const bg = props.disabled ? t.disabled : base;
  const textColor = props.kind === 'ghost' ? t.sub : '#ffffff';
  return (
    <Pressable
      onPress={props.disabled ? undefined : props.onPress}
      style={[styles.button, { backgroundColor: bg, borderColor: t.border }]}
    >
      <Text style={[styles.buttonText, { color: props.disabled ? t.sub : textColor }]}>
        {props.label}
      </Text>
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

// ---------- テーマ ----------
type Theme = typeof light;
const light = {
  bg: '#ffffff',
  text: '#1a1a1a',
  sub: '#666666',
  card: '#f6f7f9',
  border: '#dfe3e8',
  primary: '#2563eb',
  reviewBtn: '#7c3aed',
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
  disabled: '#3a3f47',
  correct: '#22c55e',
  correctBg: '#132b1c',
  wrong: '#ef4444',
  wrongBg: '#2b1414',
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 16, paddingBottom: 40 },
  back: { paddingVertical: 6, marginBottom: 2 },
  backText: { fontSize: 15, fontWeight: '600' },
  title: { fontSize: 26, fontWeight: 'bold', marginBottom: 4 },
  subtitle: { fontSize: 14, marginBottom: 16 },
  note: { fontSize: 14, marginTop: 12, lineHeight: 20 },
  row: { borderWidth: 1, borderRadius: 10, padding: 16, marginBottom: 10 },
  rowLabel: { fontSize: 17, fontWeight: '600', lineHeight: 23 },
  rowSub: { fontSize: 13, marginTop: 4 },
  progress: { fontSize: 13, marginBottom: 10 },
  question: { fontSize: 18, lineHeight: 26, fontWeight: '600', marginBottom: 18 },
  choice: { borderWidth: 1.5, borderRadius: 10, padding: 14, marginBottom: 10 },
  choiceText: { fontSize: 16, lineHeight: 22 },
  explainBox: { borderWidth: 1, borderRadius: 10, padding: 14, marginTop: 6, marginBottom: 8 },
  verdict: { fontSize: 15, fontWeight: 'bold', marginBottom: 6 },
  explainText: { fontSize: 14, lineHeight: 21 },
  figureWrap: { marginTop: 10 },
  figure: {
    fontFamily: Platform.select({ ios: 'Courier', android: 'monospace', default: 'monospace' }),
    fontSize: 12,
    lineHeight: 17,
    padding: 10,
    borderWidth: 1,
    borderRadius: 8,
  },
  button: {
    borderRadius: 10,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 10,
    borderWidth: 1,
  },
  buttonText: { fontSize: 16, fontWeight: 'bold' },
  score: { fontSize: 22, fontWeight: 'bold', marginBottom: 8 },
});
