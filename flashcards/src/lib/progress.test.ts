import { describe, expect, it } from 'vitest';
import { blankProgress, canComplete, markActive, markCompleted, recordAnswer, sanitizeProgress } from './progress';

const answer = (p: ReturnType<typeof blankProgress>, results: boolean[]) =>
  results.reduce((acc, ok) => recordAnswer(acc, ok, 1), p);

describe('recordAnswer', () => {
  it('increments streak and correct on a right answer', () => {
    const p = recordAnswer(blankProgress(), true, 5);
    expect(p).toMatchObject({ streak: 1, correct: 1, wrong: 0, lastSeen: 5 });
  });

  it('resets streak but keeps lifetime counts on a wrong answer', () => {
    const p = answer(blankProgress(), [true, true, false]);
    expect(p).toMatchObject({ streak: 0, correct: 2, wrong: 1 });
  });

  it('does not mutate its input', () => {
    const p = blankProgress();
    recordAnswer(p, true);
    expect(p.streak).toBe(0);
  });
});

describe('completion', () => {
  it('unlocks only after 3 correct in a row', () => {
    expect(canComplete(answer(blankProgress(), [true, true]))).toBe(false);
    expect(canComplete(answer(blankProgress(), [true, true, true]))).toBe(true);
  });

  it('a miss in the middle restarts the count', () => {
    expect(canComplete(answer(blankProgress(), [true, true, false, true]))).toBe(false);
    expect(canComplete(answer(blankProgress(), [true, true, false, true, true, true]))).toBe(true);
  });

  it('markCompleted is a no-op without a full streak', () => {
    const p = answer(blankProgress(), [true, true]);
    expect(markCompleted(p).completed).toBe(false);
  });

  it('markCompleted works with a full streak and blocks a second completion', () => {
    const p = markCompleted(answer(blankProgress(), [true, true, true]));
    expect(p.completed).toBe(true);
    expect(canComplete(p)).toBe(false);
  });

  it('markActive returns the card to the pool with the streak reset and counts kept', () => {
    const done = markCompleted(answer(blankProgress(), [false, true, true, true]));
    const back = markActive(done);
    expect(back).toMatchObject({ completed: false, streak: 0, correct: 3, wrong: 1 });
    expect(canComplete(back)).toBe(false);
  });
});

describe('sanitizeProgress', () => {
  it('drops unknown ids and repairs bad fields', () => {
    const out = sanitizeProgress(
      { a: { streak: 2, correct: -1, wrong: 'x', completed: 'yes', lastSeen: 9 }, gone: { streak: 1 } },
      new Set(['a', 'b']),
    );
    expect(out).toEqual({ a: { streak: 2, correct: 0, wrong: 0, completed: false, lastSeen: 9 } });
  });

  it('tolerates garbage input', () => {
    expect(sanitizeProgress(null, new Set(['a']))).toEqual({});
    expect(sanitizeProgress('nope', new Set(['a']))).toEqual({});
  });
});
