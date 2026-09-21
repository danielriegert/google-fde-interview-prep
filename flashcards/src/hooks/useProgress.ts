import { useCallback, useEffect, useState } from 'react';
import type { CardProgress, ProgressMap } from '../types';
import { getProgress, markActive, markCompleted, recordAnswer, sanitizeProgress } from '../lib/progress';
import { loadRaw, save } from '../lib/storage';

export function useProgress(validIds: Set<string>) {
  const [progress, setProgress] = useState<ProgressMap>(() => sanitizeProgress(loadRaw(), validIds));

  useEffect(() => save(progress), [progress]);

  const update = useCallback(
    (id: string, fn: (p: CardProgress) => CardProgress) => setProgress((m) => ({ ...m, [id]: fn(getProgress(m, id)) })),
    [],
  );

  return {
    progress,
    answer: useCallback((id: string, correct: boolean) => update(id, (p) => recordAnswer(p, correct)), [update]),
    complete: useCallback((id: string) => update(id, markCompleted), [update]),
    reactivate: useCallback((id: string) => update(id, markActive), [update]),
    reset: useCallback(() => setProgress({}), []),
    replaceAll: useCallback((raw: unknown) => setProgress(sanitizeProgress(raw, validIds)), [validIds]),
  };
}
