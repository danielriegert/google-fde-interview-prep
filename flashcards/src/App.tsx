import { useState } from 'react';
import type { Card } from './types';
import { ALL_CARDS, THEMES, VALID_IDS } from './data';
import { useProgress } from './hooks/useProgress';
import { buildDeck } from './lib/deck';
import { getProgress } from './lib/progress';
import { ThemeGrid, type StartRequest } from './components/ThemeGrid';
import { StudySession } from './components/StudySession';
import { CompletedView } from './components/CompletedView';
import { SettingsMenu } from './components/SettingsMenu';

type View = { name: 'themes' } | { name: 'completed' } | { name: 'study'; title: string; deck: Card[]; key: number };

export default function App() {
  const { progress, answer, complete, reactivate, reset, replaceAll } = useProgress(VALID_IDS);
  const [view, setView] = useState<View>({ name: 'themes' });

  const completedCount = ALL_CARDS.filter((c) => getProgress(progress, c.id).completed).length;

  const start = (req: StartRequest) =>
    setView({
      name: 'study',
      title: req.title,
      key: Date.now(),
      deck: buildDeck(ALL_CARDS, progress, { themes: req.themes, shuffled: req.shuffled }),
    });

  return (
    <div className="app">
      <header className="topbar">
        <button className="brand" onClick={() => setView({ name: 'themes' })}>
          🃏 LeetCode Flashcards
        </button>
        <nav>
          <button className={view.name === 'themes' || view.name === 'study' ? 'tab on' : 'tab'} onClick={() => setView({ name: 'themes' })}>
            Study
          </button>
          <button className={view.name === 'completed' ? 'tab on' : 'tab'} onClick={() => setView({ name: 'completed' })}>
            Completed ({completedCount})
          </button>
        </nav>
        <SettingsMenu progress={progress} onImport={replaceAll} onReset={reset} />
      </header>

      <main>
        {view.name === 'themes' && <ThemeGrid themes={THEMES} cards={ALL_CARDS} progress={progress} onStart={start} />}
        {view.name === 'study' && (
          <StudySession
            key={view.key}
            title={view.title}
            deck={view.deck}
            progress={progress}
            onAnswer={answer}
            onComplete={complete}
            onExit={() => setView({ name: 'themes' })}
          />
        )}
        {view.name === 'completed' && <CompletedView themes={THEMES} cards={ALL_CARDS} progress={progress} onReactivate={reactivate} />}
      </main>
    </div>
  );
}
