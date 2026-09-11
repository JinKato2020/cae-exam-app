import { useEffect, useMemo, useState } from 'react';
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  useColorScheme,
  View,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

import type { AnswerRecord, Chapter, Question } from './src/types';
import { loadWrongIds, updateWrongIds } from './src/storage';

// 配布ビルドには自作オリジナル問題のみを含める（公式問題集は gitignore 済でローカルのみ）。
import chapterJson from './content/questions/math-basics.json';

const chapter = chapterJson as unknown as Chapter;
const ALL_QUESTIONS: Question[] = chapter.questions;

type Screen = 'home' | 'quiz' | 'result';

export default function App() {
  const scheme = useColorScheme();
  const t = scheme === 'dark' ? dark : light;

  const [screen, setScreen] = useState<Screen>('home');
  const [wrongIds, setWrongIds] = useState<string[]>([]);

  // 出題中の問題列と進行状態
  const [quiz, setQuiz] = useState<Question[]>([]);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState<number | null>(null); // 1始まり
  const [records, setRecords] = useState<AnswerRecord[]>([]);

  // 起動時に、前回までの「間違いリスト」を端末から読み込む
  useEffect(() => {
    loadWrongIds().then(setWrongIds);
  }, []);

  const wrongQuestions = useMemo(
    () => ALL_QUESTIONS.filter((q) => wrongIds.includes(q.id)),
    [wrongIds]
  );

  function startQuiz(list: Question[]) {
    if (list.length === 0) return;
    setQuiz(list);
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
    // 最終問題 → 記録を端末に反映して結果画面へ
    const next = await updateWrongIds(wrongIds, records);
    setWrongIds(next);
    setScreen('result');
  }

  // ---------- 画面 ----------
  return (
    <SafeAreaProvider>
      <SafeAreaView style={[styles.container, { backgroundColor: t.bg }]}>
        <StatusBar style={scheme === 'dark' ? 'light' : 'dark'} />
        {screen === 'home' && (
          <HomeScreen
            t={t}
            total={ALL_QUESTIONS.length}
            wrongCount={wrongQuestions.length}
            grade={chapter.meta.grade}
            category={chapter.meta.category}
            onStartAll={() => startQuiz(ALL_QUESTIONS)}
            onStartReview={() => startQuiz(wrongQuestions)}
          />
        )}
        {screen === 'quiz' && current && (
          <QuizScreen
            t={t}
            q={current}
            index={index}
            total={quiz.length}
            selected={selected}
            answered={answered}
            onSelect={onSelect}
            onNext={onNext}
          />
        )}
        {screen === 'result' && (
          <ResultScreen
            t={t}
            quiz={quiz}
            records={records}
            onRetry={() => startQuiz(quiz)}
            onReview={() => startQuiz(wrongQuestions)}
            wrongCount={wrongQuestions.length}
            onHome={() => setScreen('home')}
          />
        )}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

// ---------- ホーム ----------
function HomeScreen(props: {
  t: Theme;
  total: number;
  wrongCount: number;
  grade: string;
  category: string;
  onStartAll: () => void;
  onStartReview: () => void;
}) {
  const { t } = props;
  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>CAE 試験対策</Text>
      <Text style={[styles.subtitle, { color: t.sub }]}>
        {props.grade}／{props.category}（全 {props.total} 問）
      </Text>

      <Button t={t} label={`全 ${props.total} 問に挑戦`} kind="primary" onPress={props.onStartAll} />
      <Button
        t={t}
        label={
          props.wrongCount > 0
            ? `間違いだけ復習（${props.wrongCount} 問）`
            : '復習する間違いはありません'
        }
        kind="review"
        disabled={props.wrongCount === 0}
        onPress={props.onStartReview}
      />

      <Text style={[styles.note, { color: t.sub }]}>
        間違えた問題は端末に記録され、次回も「間違い復習」で挑戦できます。
      </Text>
    </ScrollView>
  );
}

// ---------- 出題 ----------
function QuizScreen(props: {
  t: Theme;
  q: Question;
  index: number;
  total: number;
  selected: number | null;
  answered: boolean;
  onSelect: (n: number) => void;
  onNext: () => void;
}) {
  const { t, q, answered, selected } = props;
  const isCorrect = selected === q.answer;

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.progress, { color: t.sub }]}>
        {props.index + 1} / {props.total}
        {q.topic ? `　・　${q.topic}` : ''}
      </Text>
      <Text style={[styles.question, { color: t.text }]}>{q.question}</Text>

      {q.choices.map((choice, i) => {
        const num = i + 1;
        const bg = choiceColor(t, { num, answer: q.answer, selected, answered });
        return (
          <Pressable
            key={num}
            onPress={() => props.onSelect(num)}
            style={[styles.choice, { backgroundColor: bg.bg, borderColor: bg.border }]}
          >
            <Text style={[styles.choiceText, { color: bg.text }]}>
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
        </View>
      )}

      {answered && (
        <Button
          t={t}
          label={props.index + 1 < props.total ? '次へ' : '結果を見る'}
          kind="primary"
          onPress={props.onNext}
        />
      )}
    </ScrollView>
  );
}

// ---------- 結果 ----------
function ResultScreen(props: {
  t: Theme;
  quiz: Question[];
  records: AnswerRecord[];
  wrongCount: number;
  onRetry: () => void;
  onReview: () => void;
  onHome: () => void;
}) {
  const { t } = props;
  const correctCount = props.records.filter((r) => r.correct).length;
  const total = props.quiz.length;
  const pct = total > 0 ? Math.round((correctCount / total) * 100) : 0;
  const wrongInThisRun = props.quiz.filter(
    (q) => props.records.find((r) => r.id === q.id)?.correct === false
  );

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={[styles.title, { color: t.text }]}>結果</Text>
      <Text style={[styles.score, { color: t.text }]}>
        {correctCount} / {total} 問正解（{pct}%）
      </Text>

      {wrongInThisRun.length > 0 ? (
        <View style={{ width: '100%', marginTop: 8 }}>
          <Text style={[styles.subtitle, { color: t.sub }]}>間違えた問題</Text>
          {wrongInThisRun.map((q) => (
            <View
              key={q.id}
              style={[styles.wrongItem, { backgroundColor: t.card, borderColor: t.border }]}
            >
              <Text style={[styles.wrongTopic, { color: t.wrong }]}>
                {q.topic ?? q.number}
              </Text>
              <Text style={[styles.wrongQ, { color: t.text }]}>{q.question}</Text>
            </View>
          ))}
        </View>
      ) : (
        <Text style={[styles.note, { color: t.correct }]}>全問正解です！</Text>
      )}

      <View style={{ height: 8 }} />
      <Button t={t} label="もう一度（同じ問題）" kind="primary" onPress={props.onRetry} />
      <Button
        t={t}
        label={props.wrongCount > 0 ? `間違いだけ復習（${props.wrongCount} 問）` : '復習する間違いはありません'}
        kind="review"
        disabled={props.wrongCount === 0}
        onPress={props.onReview}
      />
      <Button t={t} label="ホームへ" kind="ghost" onPress={props.onHome} />
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

// 選択肢の色（回答後：正解=緑、選んだ誤答=赤、他=通常）
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
  title: { fontSize: 26, fontWeight: 'bold', marginBottom: 4 },
  subtitle: { fontSize: 14, marginBottom: 16 },
  note: { fontSize: 13, marginTop: 16, lineHeight: 19 },
  progress: { fontSize: 13, marginBottom: 10 },
  question: { fontSize: 18, lineHeight: 26, fontWeight: '600', marginBottom: 18 },
  choice: { borderWidth: 1.5, borderRadius: 10, padding: 14, marginBottom: 10 },
  choiceText: { fontSize: 16, lineHeight: 22 },
  explainBox: { borderWidth: 1, borderRadius: 10, padding: 14, marginTop: 6, marginBottom: 8 },
  verdict: { fontSize: 15, fontWeight: 'bold', marginBottom: 6 },
  explainText: { fontSize: 14, lineHeight: 21 },
  button: {
    borderRadius: 10,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 10,
    borderWidth: 1,
  },
  buttonText: { fontSize: 16, fontWeight: 'bold' },
  score: { fontSize: 22, fontWeight: 'bold', marginBottom: 8 },
  wrongItem: { borderWidth: 1, borderRadius: 8, padding: 12, marginBottom: 8 },
  wrongTopic: { fontSize: 12, fontWeight: 'bold', marginBottom: 4 },
  wrongQ: { fontSize: 14, lineHeight: 20 },
});
