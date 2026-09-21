import { useMemo, useState } from 'react';
import type { Card, ProgressMap, Theme } from '../types';
import { getProgress } from '../lib/progress';

export interface StartRequest {
  themes?: string[];
  shuffled: boolean;
  title: string;
}

interface Props {
  themes: Theme[];
  cards: Card[];
  progress: ProgressMap;
  onStart: (req: StartRequest) => void;
}

export function ThemeGrid({ themes, cards, progress, onStart }: Props) {
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const stats = useMemo(() => {
    const m = new Map<string, { total: number; done: number }>();
    for (const c of cards) {
      const s = m.get(c.theme) ?? { total: 0, done: 0 };
      s.total++;
      if (getProgress(progress, c.id).completed) s.done++;
      m.set(c.theme, s);
    }
    return m;
  }, [cards, progress]);

  const visible = themes.filter((t) => (stats.get(t.id)?.total ?? 0) > 0);
  const total = cards.length;
  const done = [...stats.values()].reduce((a, s) => a + s.done, 0);
  const active = total - done;
  const selectedActive = [...selected].reduce((a, id) => {
    const s = stats.get(id);
    return a + (s ? s.total - s.done : 0);
  }, 0);

  const toggle = (id: string) =>
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  return (
    <div>
      <section className="panel hero">
        <div>
          <h1>Ready to study?</h1>
          <p className="muted">
            {active} active · {done} completed · {total} total cards
          </p>
        </div>
        <div className="actions">
          <button className="btn primary" disabled={active === 0} onClick={() => onStart({ shuffled: true, title: 'Random mix · all themes' })}>
            🔀 Random mix ({active})
          </button>
          <button
            className="btn"
            disabled={selectedActive === 0}
            onClick={() =>
              onStart({ themes: [...selected], shuffled: true, title: `Random mix · ${selected.size} theme${selected.size === 1 ? '' : 's'}` })
            }
          >
            Random mix of selected ({selectedActive})
          </button>
          {selected.size > 0 && (
            <button className="btn ghost" onClick={() => setSelected(new Set())}>
              Clear selection
            </button>
          )}
        </div>
      </section>

      <div className="grid">
        {visible.map((t) => {
          const s = stats.get(t.id)!;
          const left = s.total - s.done;
          const pct = Math.round((s.done / s.total) * 100);
          const isSel = selected.has(t.id);
          return (
            <article key={t.id} className={`tile${isSel ? ' selected' : ''}`}>
              <label className="tile-head">
                <input type="checkbox" checked={isSel} onChange={() => toggle(t.id)} aria-label={`Select ${t.title} for a custom random mix`} />
                <h3>{t.title}</h3>
              </label>
              <p className="muted small">{t.description}</p>
              <div className="bar" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
                <div style={{ width: `${pct}%` }} />
              </div>
              <p className="small">
                <strong>{left}</strong> active · {s.done} completed
              </p>
              <div className="actions">
                <button className="btn" disabled={left === 0} onClick={() => onStart({ themes: [t.id], shuffled: false, title: t.title })}>
                  In order
                </button>
                <button className="btn" disabled={left === 0} onClick={() => onStart({ themes: [t.id], shuffled: true, title: `${t.title} · shuffled` })}>
                  Shuffled
                </button>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
