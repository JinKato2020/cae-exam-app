import type { Chapter, Question } from './types';

/** 生データは親1問のまま維持し、学習画面には末端の設問を任意数展開する。 */
export function expandChapter(chapter: Chapter): Chapter {
  const questions: Question[] = [];
  function visit(q: Question, root: Question, common: string[], labels: string[]) {
    const context = q.sharedQuestion ? [...common, q.sharedQuestion] : common;
    if (q.parts?.length) {
      q.parts.forEach((part, i) => visit({
        ...part,
        officialRef: part.officialRef ?? q.officialRef,
        relatedFormulas: part.relatedFormulas ?? q.relatedFormulas,
      }, root, context, [...labels, `${i + 1} / ${q.parts!.length}`]));
      return;
    }
    if (!labels.length) { questions.push(q); return; }
    const { parts, sharedQuestion, ...leaf } = q;
    questions.push({
      ...leaf,
      question: [...context, q.question].join('\n\n'),
      rootQuestionId: root.id,
      partLabel: `設問 ${labels.join(' · ')}`,
    });
  }
  chapter.questions.forEach(q => visit(q, q, [], []));
  const sizes = new Map<string, number>();
  for (const q of questions) if (q.rootQuestionId) sizes.set(q.rootQuestionId, (sizes.get(q.rootQuestionId) ?? 0) + 1);
  for (const q of questions) if (q.rootQuestionId) q.groupSize = sizes.get(q.rootQuestionId);
  return { ...chapter, meta: { ...chapter.meta, count: questions.length }, questions };
}

/** OTAで設問が増減・並べ替えされても、開いていたIDを保ち、有効な一覧へ差し替える。 */
export function refreshQuestionSession(previous: Question[], index: number, latest: Question[]) {
  const groups = new Map<string, Question[]>();
  for (const q of latest) {
    const root = q.rootQuestionId ?? q.id;
    const group = groups.get(root) ?? [];
    group.push(q);
    groups.set(root, group);
  }
  const seen = new Set<string>();
  const questions = previous.flatMap(q => {
    const root = q.rootQuestionId ?? q.id;
    if (seen.has(root)) return [];
    seen.add(root);
    const updated = groups.get(root) ?? [];
    const selected = previous.filter(item => (item.rootQuestionId ?? item.id) === root);
    // 苦手問題や栞で一部の設問だけを開いていた場合、未選択の兄弟を勝手に追加しない。
    if (q.groupSize && selected.length < q.groupSize) {
      const ids = new Set(selected.map(item => item.id));
      return updated.filter(item => ids.has(item.id));
    }
    return updated;
  });
  const currentId = previous[index]?.id;
  const retained = questions.findIndex(q => q.id === currentId);
  return { questions, index: retained >= 0 ? retained : Math.max(0, Math.min(index, questions.length - 1)) };
}
