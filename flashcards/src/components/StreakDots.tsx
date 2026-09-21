import { COMPLETE_STREAK } from '../lib/progress';

export function StreakDots({ streak }: { streak: number }) {
  return (
    <span className="streak" title={`${streak} correct in a row`} aria-label={`${streak} correct in a row`}>
      {Array.from({ length: COMPLETE_STREAK }, (_, i) => (
        <span key={i} className={i < streak ? 'dot on' : 'dot'} />
      ))}
      {streak > COMPLETE_STREAK && <span className="streak-extra">+{streak - COMPLETE_STREAK}</span>}
    </span>
  );
}
