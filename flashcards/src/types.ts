export type CardKind = 'concept' | 'template' | 'complexity' | 'gotcha' | 'pattern' | 'problem';

export interface Card {
  /** Stable, hand-written slug. Progress is keyed by this - never change it once cards are in use. */
  id: string;
  theme: string;
  kind: CardKind;
  /** Markdown */
  front: string;
  /** Markdown; fenced code blocks allowed */
  back: string;
  /** LeetCode problem number, when the card is about a specific problem (never a Hard one). */
  lc?: number;
  /** Where the material came from, relative to leetcode/ */
  source: string;
}

export interface Theme {
  id: string;
  title: string;
  description: string;
}

export interface CardProgress {
  /** Consecutive correct answers; a wrong answer resets it to 0. */
  streak: number;
  correct: number;
  wrong: number;
  completed: boolean;
  lastSeen: number;
}

export type ProgressMap = Record<string, CardProgress>;
