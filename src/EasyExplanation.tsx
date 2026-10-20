import { useEffect, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { RichText } from './MathText';
import type { Question } from './types';

type Colors = {
  bg: string;
  card: string;
  text: string;
  sub: string;
  primary: string;
  border: string;
};

export function EasyExplanation(props: {
  question: Question;
  answered: boolean;
  locked: boolean;
  colors: Colors;
  onScrollActiveChange?: (active: boolean) => void;
}) {
  const { question, answered, locked, colors: c } = props;
  const [open, setOpen] = useState(false);
  const sections = question.easyExplanation;
  const available = Boolean(sections?.length);
  useEffect(() => { setOpen(false); }, [question.id, answered, locked, available]);

  // 分野・級・問題番号で限定せず、OTAで届いたデータの有無だけで表示する。
  if (locked || !answered || !sections?.length) return null;

  return (
    <View style={s.container}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel="やさしく解説"
        accessibilityState={{ expanded: open }}
        onPress={() => setOpen(value => !value)}
        style={[s.button, { backgroundColor: c.card, borderColor: c.primary }]}
      >
        <Text style={[s.buttonTitle, { color: c.primary }]}>やさしく解説</Text>
        <Text style={[s.buttonAction, { color: c.sub }]}>{open ? '閉じる −' : '開く ＋'}</Text>
      </Pressable>
      {open && (
        <View style={[s.body, { backgroundColor: c.card, borderColor: c.border }]}>
          {sections.map((section, i) => (
            <View key={i} style={s.section}>
              <Text accessibilityRole="header" style={[s.heading, { color: c.primary }]}>
                {i + 1}. {section.title}
              </Text>
              {section.body.split(/\n\s*\n/).map((paragraph, j) => (
                <View key={j} style={s.paragraph}>
                  <RichText
                    text={paragraph}
                    color={c.text}
                    fontSize={16}
                    bg={c.card}
                    scroll
                    scrollOnlyOverflow
                    onScrollActiveChange={props.onScrollActiveChange}
                  />
                </View>
              ))}
            </View>
          ))}
        </View>
      )}
    </View>
  );
}

const s = StyleSheet.create({
  container: { marginTop: 16 },
  button: { minHeight: 52, paddingHorizontal: 16, paddingVertical: 14, borderWidth: 1, borderRadius: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  buttonTitle: { fontSize: 17, fontWeight: '700' },
  buttonAction: { fontSize: 14, marginLeft: 12 },
  body: { marginTop: 10, borderWidth: 1, borderRadius: 14, padding: 16 },
  section: { marginBottom: 18 },
  heading: { fontSize: 17, lineHeight: 25, fontWeight: '700', marginBottom: 8 },
  paragraph: { marginBottom: 10 },
});
