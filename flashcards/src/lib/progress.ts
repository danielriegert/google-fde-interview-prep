import type { CardProgress, ProgressMap } from '../types';

/** Consecutive correct answers needed before a card can be marked completed. */
export const COMPLETE_STREAK = 3;

export const blankProgress = (): CardProgress => ({
  streak: 0,
  correct: 0,
  wrong: 0,
  completed: false,
  lastSeen: 0,
});

export const getProgress = (map: ProgressMap, id: string): CardProgress => map[id] ?? blankProgress();

/** Correct: streak + 1. Wrong: streak resets to 0. Lifetime counts always accumulate. */
export function recordAnswer(p: CardProgress, correct: boolean, now = Date.now()): CardProgress {
  return correct
    ? { ...p, streak: p.streak + 1, correct: p.correct + 1, lastSeen: now }
    : { ...p, streak: 0, wrong: p.wrong + 1, lastSeen: now };
}

/** The user may only mark a card completed once it has a full streak. */
export const canComplete = (p: CardProgress): boolean => !p.completed && p.streak >= COMPLETE_STREAK;

export const markCompleted = (p: CardProgress): CardProgress => (canComplete(p) ? { ...p, completed: true } : p);

/** Returns the card to the active pool. The streak restarts so the card is genuinely re-studied. */
export const markActive = (p: CardProgress): CardProgress => ({ ...p, completed: false, streak: 0 });

/** Keep only progress for cards that still exist and sanitise field types (used on load/import). */
export function sanitizeProgress(raw: unknown, validIds: Set<string>): ProgressMap {
  const out: ProgressMap = {};
  if (!raw || typeof raw !== 'object') return out;
  for (const [id, v] of Object.entries(raw as Record<string, unknown>)) {
    if (!validIds.has(id) || !v || typeof v !== 'object') continue;
    const r = v as Partial<CardProgress>;
    const num = (n: unknown) => (typeof n === 'number' && Number.isFinite(n) && n >= 0 ? Math.floor(n) : 0);
    out[id] = {
      streak: num(r.streak),
      correct: num(r.correct),
      wrong: num(r.wrong),
      completed: r.completed === true,
      lastSeen: num(r.lastSeen),
    };
  }
  return out;
}
