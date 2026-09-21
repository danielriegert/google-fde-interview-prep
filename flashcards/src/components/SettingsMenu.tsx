import { useRef, useState } from 'react';
import type { ProgressMap } from '../types';

interface Props {
  progress: ProgressMap;
  onImport: (raw: unknown) => void;
  onReset: () => void;
}

export function SettingsMenu({ progress, onImport, onReset }: Props) {
  const [open, setOpen] = useState(false);
  const [msg, setMsg] = useState('');
  const fileRef = useRef<HTMLInputElement>(null);

  const exportJson = () => {
    const blob = new Blob([JSON.stringify(progress, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `flashcard-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const importFile = async (file: File) => {
    try {
      onImport(JSON.parse(await file.text()));
      setMsg('Progress imported.');
    } catch {
      setMsg('That file is not valid progress JSON.');
    }
  };

  return (
    <div className="settings">
      <button className="btn ghost" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
        ⚙ Progress
      </button>
      {open && (
        <div className="menu">
          <button className="btn" onClick={exportJson}>
            Export progress (JSON)
          </button>
          <button className="btn" onClick={() => fileRef.current?.click()}>
            Import progress…
          </button>
          <input ref={fileRef} type="file" accept="application/json" hidden onChange={(e) => e.target.files?.[0] && importFile(e.target.files[0])} />
          <button
            className="btn bad"
            onClick={() => {
              if (window.confirm('Reset ALL progress (streaks, counts and completed cards)? This cannot be undone.')) {
                onReset();
                setMsg('Progress reset.');
              }
            }}
          >
            Reset all progress
          </button>
          {msg && <p className="muted small">{msg}</p>}
          <p className="muted small">Progress is stored in this browser only - export it to back it up or move it.</p>
        </div>
      )}
    </div>
  );
}
