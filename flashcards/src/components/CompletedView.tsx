import { useState } from 'react';
import type { Card, ProgressMap, Theme } from '../types';
import { getProgress } from '../lib/progress';
import { Markdown } from './Markdown';

interface Props {
  themes: Theme[];
  cards: Card[];
  progress: ProgressMap;
  onReactivate: (id: string) => void;
}

const preview = (front: string) => front.replace(/[`*_#>]/g, '').split('\n')[0];

export function CompletedView({ themes, cards, progress, onReactivate }: Props) {
  const [open, setOpen] = useState<Set<string>>(new Set());
  const done = cards.filter((c) => getProgress(progress, c.id).completed);

  const toggle = (id: string) =>
    setOpen((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });

  if (done.length === 0) {
    return (
      <section className="panel center">
        <h2>No completed cards yet</h2>
        <p className="muted">Answer a card correctly 3 times in a row, then choose “Mark as completed”. It will show up here.</p>
      </section>
    );
  }

  return (
    <div>
      <h1>Completed ({done.length})</h1>
      <p className="muted">These cards are left out of every study session. Mark one as not completed to put it back in the active stack.</p>
      {themes.map((t) => {
        const list = done.filter((c) => c.theme === t.id);
        if (list.length === 0) return null;
        return (
          <section key={t.id} className="panel">
            <h3>
              {t.title} <span className="muted small">({list.length})</span>
            </h3>
            <ul className="done-list">
              {list.map((c) => {
                const p = getProgress(progress, c.id);
                const isOpen = open.has(c.id);
                return (
                  <li key={c.id}>
                    <div className="done-row">
                      <button className="linklike" onClick={() => toggle(c.id)} aria-expanded={isOpen}>
                        {isOpen ? '▾' : '▸'} {preview(c.front)}
                      </button>
                      <span className="muted small">
                        ✓ {p.correct} · ✗ {p.wrong}
                      </span>
                      <button className="btn small-btn" onClick={() => onReactivate(c.id)}>
                        Mark as not completed
                      </button>
                    </div>
                    {isOpen && (
                      <div className="done-body">
                        <Markdown>{c.front}</Markdown>
                        <hr />
                        <Markdown>{c.back}</Markdown>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })}
    </div>
  );
}
