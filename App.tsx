import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ScrollView } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import mathChapter from './content/questions/solid2-math.json';

// 土台段階のプレースホルダ画面。
// 次段階で「4択で解いて採点」「間違い復習」などの中身を作り込む。
export default function App() {
  const { meta, questions } = mathChapter;

  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.container}>
        <StatusBar style="auto" />
        <ScrollView contentContainerStyle={styles.content}>
          <Text style={styles.title}>CAE 試験対策</Text>
          <Text style={styles.subtitle}>
            {meta.grade}／{meta.category}（全 {questions.length} 問）
          </Text>
          {questions.map((q) => (
            <View key={q.id} style={styles.card}>
              <Text style={styles.qnum}>{q.number}</Text>
              <Text style={styles.qtext}>{q.question}</Text>
              <Text style={styles.answer}>正解：{q.answer}</Text>
            </View>
          ))}
        </ScrollView>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 16 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 4 },
  subtitle: { fontSize: 14, color: '#555', marginBottom: 16 },
  card: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    backgroundColor: '#fafafa',
  },
  qnum: { fontSize: 12, color: '#2563eb', fontWeight: 'bold', marginBottom: 4 },
  qtext: { fontSize: 14, lineHeight: 20, marginBottom: 8 },
  answer: { fontSize: 13, fontWeight: 'bold', color: '#16a34a' },
});
