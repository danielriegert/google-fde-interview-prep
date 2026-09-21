import type { Card, ProgressMap } from '../types';
import { getProgress } from './progress';

/** Fisher-Yates. Returns a new array; the input is not mutated. */
export function shuffle<T>(items: readonly T[], rand: () => number = Math.random): T[] {
  const a = items.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export interface DeckOptions {
  /** Theme ids to include; omit/empty for all themes. */
  themes?: string[];
  shuffled: boolean;
  rand?: () => number;
}

/** Active (non-completed) cards for the chosen themes, in authored order or shuffled. */
export function buildDeck(cards: readonly Card[], progress: ProgressMap, opts: DeckOptions): Card[] {
  const themeSet = opts.themes && opts.themes.length > 0 ? new Set(opts.themes) : null;
  const active = cards.filter((c) => (!themeSet || themeSet.has(c.theme)) && !getProgress(progress, c.id).completed);
  return opts.shuffled ? shuffle(active, opts.rand) : active;
}
