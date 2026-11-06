import type { Chapter, Question, StudyResponses } from './types';

/** 同一公式問の選択回答と記述の自己確認を集約。途中回答は完了にしない。 */
export function studyResult(parts: Question[], responses: StudyResponses) {
  const complete = parts.length > 0 && parts.every(p => p.responseType === 'written'
    ? responses[p.id]?.understood != null && responses[p.id]?.revealed === true
    : responses[p.id]?.choice != null);
  const correct = complete && parts.every(p => p.responseType === 'written'
    ? responses[p.id]?.understood === true : responses[p.id]?.choice === p.answer);
  return { complete, correct };
}

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
        explanationMode: part.explanationMode ?? q.explanationMode,
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
  chapter.questions.forEach(q => {
    const effective = q.explanationMode || !chapter.meta.explanationMode
      ? q : { ...q, explanationMode: chapter.meta.explanationMode };
    visit(effective, q, [], []);
  });
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
      // 独立ページだった旧小問が同一ページへ統合されても、開いた問題を失わない。
      return updated.filter(item => ids.has(item.id) || item.studyParts?.some(part => ids.has(part.id)));
    }
    return updated;
  });
  const currentId = previous[index]?.id;
  const retained = questions.findIndex(q => q.id === currentId);
  return { questions, index: retained >= 0 ? retained : Math.max(0, Math.min(index, questions.length - 1)) };
}
