import type { Card } from '../types';
import { THEMES } from './themes';

const files = import.meta.glob<Card[]>('./cards/*.json', { eager: true, import: 'default' });

const byTheme = new Map<string, Card[]>();
for (const cards of Object.values(files)) {
  for (const c of cards) {
    const list = byTheme.get(c.theme) ?? [];
    list.push(c);
    byTheme.set(c.theme, list);
  }
}

/** All cards: themes in THEMES order, cards in authored order within a theme. */
export const ALL_CARDS: Card[] = THEMES.flatMap((t) => byTheme.get(t.id) ?? []);
export const VALID_IDS = new Set(ALL_CARDS.map((c) => c.id));
export { THEMES };
