import { useCallback, useEffect, useRef, useState } from 'react';
import type { Card, ProgressMap } from '../types';
import { COMPLETE_STREAK, canComplete, getProgress } from '../lib/progress';
import { Markdown } from './Markdown';
import { StreakDots } from './StreakDots';
import { THEMES } from '../data/themes';

interface Props {
  title: string;
  deck: Card[];
  progress: ProgressMap;
  onAnswer: (id: string, correct: boolean) => void;
  onComplete: (id: string) => void;
  onExit: () => void;
}

type Phase = 'front' | 'back' | 'graded';

const themeTitle = (id: string) => THEMES.find((t) => t.id === id)?.title ?? id;
const noFocus = (e: React.MouseEvent) => e.preventDefault(); // keep keyboard shortcuts working after a mouse click

export function StudySession({ title, deck, progress, onAnswer, onComplete, onExit }: Props) {
  const [queue, setQueue] = useState<Card[]>(deck);
  const [pos, setPos] = useState(0);
  const [phase, setPhase] = useState<Phase>('front');
  const [lastCorrect, setLastCorrect] = useState(false);
  const [tally, setTally] = useState({ correct: 0, missed: 0, completed: 0 });

  const current: Card | undefined = queue[pos];
  const p = current ? getProgress(progress, current.id) : undefined;

  const reveal = useCallback(() => setPhase((ph) => (ph === 'front' ? 'back' : ph)), []);

  const grade = useCallback(
    (correct: boolean) => {
      if (!current || phase !== 'back') return;
      onAnswer(current.id, correct);
      if (!correct) setQueue((q) => [...q, current]); // missed cards come round again at the end
      setTally((t) => ({ ...t, correct: t.correct + (correct ? 1 : 0), missed: t.missed + (correct ? 0 : 1) }));
      setLastCorrect(correct);
      setPhase('graded');
    },
    [current, phase, onAnswer],
  );

  const complete = useCallback(() => {
    if (!current || !p || !canComplete(p)) return;
    onComplete(current.id);
    setTally((t) => ({ ...t, completed: t.completed + 1 }));
  }, [current, p, onComplete]);

  const next = useCallback(() => {
    let n = pos + 1;
    // skip anything completed in the meantime
    while (n < queue.length && getProgress(progress, queue[n].id).completed) n++;
    setPos(n);
    setPhase('front');
  }, [pos, queue, progress]);

  // Keyboard shortcuts. Latest handlers live in a ref so the listener is registered once.
  const handlers = useRef({ reveal, grade, next, complete, phase });
  handlers.current = { reveal, grade, next, complete, phase };
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement;
      if (el.closest('input, textarea, select')) return;
      const h = handlers.current;
      const isActivate = e.key === ' ' || e.key === 'Enter';
      if (isActivate && el.closest('button, a')) return; // a focused button handles its own activation
      if (isActivate) {
        e.preventDefault();
        if (h.phase === 'front') h.reveal();
        else if (h.phase === 'graded') h.next();
      } else if (e.key === '1') h.grade(true);
      else if (e.key === '2') h.grade(false);
      else if (e.key.toLowerCase() === 'c') h.complete();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  if (!current || !p) {
    return (
      <section className="panel center">
        <h2>{deck.length === 0 ? 'Nothing to study here' : 'Session complete 🎉'}</h2>
        {deck.length === 0 ? (
          <p className="muted">There are no active cards in this selection - everything is completed.</p>
        ) : (
          <p>
            <strong>{tally.correct}</strong> correct · <strong>{tally.missed}</strong> missed · <strong>{tally.completed}</strong> newly completed
          </p>
        )}
        <button className="btn primary" onClick={onExit}>
          Back to themes
        </button>
      </section>
    );
  }

  const remaining = queue.length - pos;
  const canMark = canComplete(p);

  return (
    <div>
      <div className="session-head">
        <button className="btn ghost" onClick={onExit}>
          ← Exit
        </button>
        <div className="session-title">
          <strong>{title}</strong>
          <span className="muted small">
            {remaining} left{queue.length > deck.length ? ` (incl. ${queue.length - deck.length} to retry)` : ''}
          </span>
        </div>
        <div className="session-score small">
          ✓ {tally.correct} · ✗ {tally.missed}
        </div>
      </div>

      <div className="bar thin">
        <div style={{ width: `${Math.round((pos / queue.length) * 100)}%` }} />
      </div>

      <article className="card">
        <header className="card-meta">
          <span className="chip">{themeTitle(current.theme)}</span>
          <span className="chip kind">{current.kind}</span>
          {current.lc && <span className="chip">LC {current.lc}</span>}
          <span className="spacer" />
          <StreakDots streak={p.streak} />
        </header>

        <div className="card-face question">
          <div className="label">Question</div>
          <Markdown>{current.front}</Markdown>
        </div>

        {phase === 'front' ? (
          <button className="btn primary wide" onMouseDown={noFocus} onClick={reveal}>
            Show answer <kbd>Space</kbd>
          </button>
        ) : (
          <div className="card-face answer">
            <div className="label">Answer</div>
            <Markdown>{current.back}</Markdown>
          </div>
        )}

        {phase === 'back' && (
          <div className="grade-row">
            <button className="btn good" onMouseDown={noFocus} onClick={() => grade(true)}>
              ✓ Got it <kbd>1</kbd>
            </button>
            <button className="btn bad" onMouseDown={noFocus} onClick={() => grade(false)}>
              ✗ Missed it <kbd>2</kbd>
            </button>
          </div>
        )}

        {phase === 'graded' && (
          <div className="graded">
            <p className={lastCorrect ? 'result good-text' : 'result bad-text'}>
              {lastCorrect
                ? p.streak >= COMPLETE_STREAK
                  ? `Correct - ${p.streak} in a row!`
                  : `Correct - streak ${p.streak}/${COMPLETE_STREAK}`
                : 'Missed - streak reset; this card will come around again.'}
            </p>
            <div className="grade-row">
              {canMark && (
                <button className="btn accent" onMouseDown={noFocus} onClick={complete}>
                  ★ Mark as completed <kbd>C</kbd>
                </button>
              )}
              {p.completed && <span className="chip done">Completed ✓ - won't appear again</span>}
              <button className="btn primary" onMouseDown={noFocus} onClick={next}>
                Next <kbd>Space</kbd>
              </button>
            </div>
          </div>
        )}
      </article>
    </div>
  );
}
