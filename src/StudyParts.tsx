import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { RichText } from './MathText';
import { EasyExplanation } from './EasyExplanation';
import { LearningFigure } from './LearningFigure';
import type { Question, StudyResponses } from './types';

type Colors = { bg: string; card: string; text: string; sub: string; primary: string; onPrimary?: string; border: string; correct: string; wrong: string };

/** 公式1問の中に、与件を共有する選択式・記述式を並べる。答えは小問ごとに開示する。 */
export function StudyParts(props: {
  question: Question; responses: StudyResponses; colors: Colors; locked: boolean;
  onChange: (responses: StudyResponses) => void; onOpenPaywall: () => void;
  onScrollActiveChange: (active: boolean) => void;
}) {
  const { question, responses, colors: c, locked } = props;
  return <View>
    {question.studyParts?.map((part, i) => {
      const state = responses[part.id] ?? {};
      const written = part.responseType === 'written';
      const revealed = !locked && (written ? Boolean(state.revealed) : state.choice != null);
      const update = (patch: typeof state) => props.onChange({ ...responses, [part.id]: { ...state, ...patch } });
      const figureKeys = part.preFigures?.length ? part.preFigures : part.preFigureImage
        ? [{ figureImage: part.preFigureImage, caption: 'この小問で使う条件・候補図です。' }] : [];
      return <View key={part.id} style={[s.part, { borderTopColor: c.border }]}>
        <View style={s.headingRow}>
          <Text accessibilityRole="header" style={[s.heading, { color: c.text }]}>（{i + 1}）{part.title}</Text>
          <Text style={[s.kind, { color: c.sub }]}>{written ? '記述式' : `${part.choices.length}択`}</Text>
        </View>
        <RichText text={part.question} color={c.text} fontSize={18} bg={c.bg} scroll scrollOnlyOverflow onScrollActiveChange={props.onScrollActiveChange} />
        {!locked && figureKeys.map((figure, j) => <LearningFigure key={j} figure={figure} colors={c} />)}
        {written ? <View style={s.answerArea}>
          {!locked && <>
            <Text style={[s.inputLabel, { color: c.sub }]}>自分の考え（入力は任意・紙に書いても構いません）</Text>
            <TextInput multiline textAlignVertical="top" value={state.draft ?? ''}
              onChangeText={draft => update({ draft })} accessibilityLabel={`小問${i + 1}の解答メモ`}
              placeholder="式・考え方・結論を書いてみましょう" placeholderTextColor={c.sub}
              style={[s.input, { color: c.text, borderColor: c.border, backgroundColor: c.card }]} />
          </>}
          {!revealed && <Pressable accessibilityRole="button" onPress={() => locked ? props.onOpenPaywall() : update({ revealed: true })}
            style={[s.button, { backgroundColor: c.primary }]}>
            <Text style={[s.buttonText, { color: c.onPrimary ?? '#fff' }]}>{locked ? '解答例を解除する' : '解答例・解説を見る'}</Text>
          </Pressable>}
        </View> : <View style={s.choices}>
          {part.choices.map((choice, j) => {
            const n = j + 1;
            const right = revealed && n === part.answer;
            const wrong = revealed && n === state.choice && !right;
            return <Pressable key={n} accessibilityRole="button" accessibilityLabel={`小問${i + 1}の選択肢${n}`}
              accessibilityState={{ disabled: revealed, selected: state.choice === n }}
              onPress={() => { if (locked) props.onOpenPaywall(); else if (!revealed) update({ choice: n }); }}
              style={[s.option, { backgroundColor: c.card, borderColor: right ? c.correct : wrong ? c.wrong : c.border }]}>
              <Text style={[s.optionIndex, { color: right ? c.correct : wrong ? c.wrong : c.sub }]}>{right ? '✓ ' : wrong ? '× ' : ''}{n}</Text>
              <View style={{ flex: 1, minWidth: 0 }}><RichText text={choice} color={c.text} fontSize={17} bg={c.card} /></View>
            </Pressable>;
          })}
        </View>}
        {revealed && <>
          {written ? <View style={[s.model, { backgroundColor: c.card, borderColor: c.border }]}>
            <Text accessibilityRole="header" style={[s.heading, { color: c.text }]}>解答例</Text>
            <RichText text={part.modelAnswer ?? ''} color={c.text} fontSize={17} bg={c.card} scroll scrollOnlyOverflow onScrollActiveChange={props.onScrollActiveChange} />
          </View> : <Text accessibilityLiveRegion="polite" style={[s.verdict, { color: state.choice === part.answer ? c.correct : c.wrong }]}>
            {state.choice === part.answer ? '正解です' : 'もう一度確認しましょう'}　正解：{part.answer}
          </Text>}
          <EasyExplanation question={{ ...part, explanationMode: 'guided' }} answered locked={false} colors={c} onScrollActiveChange={props.onScrollActiveChange} />
          {written && <View style={[s.model, { borderColor: c.border, backgroundColor: c.card }]}>
            <Text accessibilityRole="header" style={[s.heading, { color: c.text }]}>自分の解答を確認</Text>
            <Text style={[s.inputLabel, { color: c.sub }]}>同じ言い回しでなくても、次の内容が説明できていれば大丈夫です。</Text>
            {part.answerCheckpoints?.map((text, j) => <View key={j} style={{ marginVertical: 6 }}><RichText text={`・${text}`} color={c.text} fontSize={17} bg={c.card} scroll scrollOnlyOverflow onScrollActiveChange={props.onScrollActiveChange} /></View>)}
            <View style={s.ratingRow}>
              {[{ value: true, label: '説明できた' }, { value: false, label: '復習したい' }].map(item => <Pressable key={item.label}
                accessibilityRole="button" accessibilityState={{ selected: state.understood === item.value, disabled: state.understood != null }}
                onPress={() => { if (state.understood == null) update({ understood: item.value }); }}
                style={[s.rating, { borderColor: c.border, backgroundColor: state.understood === item.value ? c.primary : c.bg }]}>
                <Text style={{ color: state.understood === item.value ? (c.onPrimary ?? '#fff') : c.text, fontSize: 16 }}>{item.label}</Text>
              </Pressable>)}
            </View>
          </View>}
        </>}
      </View>;
    })}
  </View>;
}

const s = StyleSheet.create({
  part: { marginTop: 28, paddingTop: 24, borderTopWidth: 1 },
  headingRow: { marginBottom: 14 }, heading: { fontSize: 18, lineHeight: 28, fontWeight: '700', marginBottom: 10 },
  kind: { fontSize: 14 }, choices: { marginTop: 16, gap: 10 },
  option: { flexDirection: 'row', alignItems: 'flex-start', borderWidth: 1.5, borderRadius: 12, padding: 14, minHeight: 56 },
  optionIndex: { minWidth: 32, fontSize: 17, lineHeight: 26, fontWeight: '700', marginRight: 10 },
  answerArea: { marginTop: 16 }, inputLabel: { fontSize: 14, lineHeight: 23, marginBottom: 12 },
  input: { minHeight: 130, borderWidth: 1, borderRadius: 12, padding: 14, fontSize: 17, lineHeight: 28 },
  button: { minHeight: 50, borderRadius: 12, alignItems: 'center', justifyContent: 'center', padding: 14, marginTop: 12 },
  buttonText: { color: '#fff', fontSize: 17, fontWeight: '700' },
  model: { marginTop: 16, borderWidth: 1, borderRadius: 14, padding: 16 },
  verdict: { marginTop: 16, fontSize: 17, lineHeight: 28, fontWeight: '700' },
  ratingRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 14 },
  rating: { flexGrow: 1, minHeight: 48, padding: 12, alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderRadius: 10 },
});
