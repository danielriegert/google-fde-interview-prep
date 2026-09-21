import type { ProgressMap } from '../types';

export const STORAGE_KEY = 'fc-progress-v1';

export function loadRaw(): unknown {
  try {
    const s = window.localStorage.getItem(STORAGE_KEY);
    return s ? JSON.parse(s) : {};
  } catch {
    return {};
  }
}

export function save(map: ProgressMap): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
  } catch {
    /* storage unavailable (private mode / quota) - progress lives in memory for this session */
  }
}
