import { describe, expect, it } from 'vitest';
import type { Card, ProgressMap } from '../types';
import { blankProgress } from './progress';
import { buildDeck, shuffle } from './deck';

const mk = (id: string, theme: string): Card => ({ id, theme, kind: 'concept', front: id, back: id, source: 'x' });
const cards = [mk('a-1', 'a'), mk('a-2', 'a'), mk('b-1', 'b'), mk('c-1', 'c')];

describe('shuffle', () => {
  it('keeps the same items and does not mutate the input', () => {
    const input = [1, 2, 3, 4, 5, 6];
    const copy = input.slice();
    const out = shuffle(input);
    expect(input).toEqual(copy);
    expect(out.slice().sort()).toEqual(copy);
  });

  it('is deterministic for a given rand source', () => {
    const rand = () => 0;
    expect(shuffle([1, 2, 3, 4], rand)).toEqual(shuffle([1, 2, 3, 4], rand));
  });
});

describe('buildDeck', () => {
  it('returns every active card in authored order when not shuffled', () => {
    expect(buildDeck(cards, {}, { shuffled: false }).map((c) => c.id)).toEqual(['a-1', 'a-2', 'b-1', 'c-1']);
  });

  it('filters by theme', () => {
    expect(buildDeck(cards, {}, { themes: ['b', 'c'], shuffled: false }).map((c) => c.id)).toEqual(['b-1', 'c-1']);
  });

  it('never includes completed cards, shuffled or not', () => {
    const progress: ProgressMap = { 'a-2': { ...blankProgress(), completed: true } };
    for (const shuffled of [false, true]) {
      const ids = buildDeck(cards, progress, { shuffled }).map((c) => c.id);
      expect(ids).not.toContain('a-2');
      expect(ids.slice().sort()).toEqual(['a-1', 'b-1', 'c-1']);
    }
  });

  it('a card that was un-completed is back in the deck', () => {
    const progress: ProgressMap = { 'a-2': { ...blankProgress(), completed: false } };
    expect(buildDeck(cards, progress, { shuffled: false }).map((c) => c.id)).toContain('a-2');
  });
});
