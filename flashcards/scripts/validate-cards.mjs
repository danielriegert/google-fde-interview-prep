// Validates every card file. Run with `npm run validate`.
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const cardsDir = join(root, 'src/data/cards');
const KINDS = new Set(['concept', 'template', 'complexity', 'gotcha', 'pattern', 'problem']);
const ID_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;

const themeIds = [...readFileSync(join(root, 'src/data/themes.ts'), 'utf8').matchAll(/\bid:\s*'([^']+)'/g)].map((m) => m[1]);
const hard = new Set(JSON.parse(readFileSync(join(root, 'scripts/hard-problems.json'), 'utf8')).hard);

const errors = [];
const warnings = [];
const seen = new Map();
const perTheme = Object.fromEntries(themeIds.map((t) => [t, 0]));

for (const file of readdirSync(cardsDir).filter((f) => f.endsWith('.json')).sort()) {
  const fileTheme = basename(file, '.json');
  let cards;
  try {
    cards = JSON.parse(readFileSync(join(cardsDir, file), 'utf8'));
  } catch (e) {
    errors.push(`${file}: invalid JSON (${e.message})`);
    continue;
  }
  if (!Array.isArray(cards)) {
    errors.push(`${file}: top level must be an array`);
    continue;
  }
  if (!themeIds.includes(fileTheme)) errors.push(`${file}: file name is not a known theme id`);

  cards.forEach((c, i) => {
    const where = `${file}[${i}]${c && c.id ? ` (${c.id})` : ''}`;
    const str = (k) => typeof c[k] === 'string' && c[k].trim().length > 0;
    for (const k of ['id', 'theme', 'kind', 'front', 'back', 'source']) if (!str(k)) errors.push(`${where}: missing/empty "${k}"`);
    if (!str('id')) return;
    if (!ID_RE.test(c.id)) errors.push(`${where}: id must be kebab-case`);
    if (c.theme !== fileTheme) errors.push(`${where}: theme "${c.theme}" != file theme "${fileTheme}"`);
    if (!c.id.startsWith(`${fileTheme}-`)) errors.push(`${where}: id must start with "${fileTheme}-"`);
    if (!KINDS.has(c.kind)) errors.push(`${where}: bad kind "${c.kind}"`);
    if (c.lc !== undefined) {
      if (!Number.isInteger(c.lc)) errors.push(`${where}: lc must be an integer`);
      else if (hard.has(c.lc)) errors.push(`${where}: LC ${c.lc} is a HARD problem - not allowed`);
    }
    for (const k of Object.keys(c)) if (!['id', 'theme', 'kind', 'front', 'back', 'lc', 'source'].includes(k)) errors.push(`${where}: unknown field "${k}"`);
    if (seen.has(c.id)) errors.push(`${where}: duplicate id (also in ${seen.get(c.id)})`);
    seen.set(c.id, file);
    if (typeof c.back === 'string' && c.back.length > 2200) warnings.push(`${where}: back is ${c.back.length} chars - consider trimming`);
    if (typeof c.front === 'string' && c.front.length > 400) warnings.push(`${where}: front is ${c.front.length} chars - keep questions short`);
    // Mentions of a Hard problem number in the text as "LC 123"/"LeetCode 123"
    for (const text of [c.front, c.back]) {
      for (const m of String(text).matchAll(/\b(?:LC|LeetCode)\s*#?(\d{1,4})\b/gi)) {
        if (hard.has(Number(m[1]))) warnings.push(`${where}: text mentions Hard problem LC ${m[1]}`);
      }
    }
    if (perTheme[fileTheme] !== undefined) perTheme[fileTheme]++;
  });
}

const total = Object.values(perTheme).reduce((a, b) => a + b, 0);
console.log('Cards per theme:');
for (const [t, n] of Object.entries(perTheme)) console.log(`  ${String(n).padStart(3)}  ${t}`);
console.log(`  ${String(total).padStart(3)}  TOTAL`);
if (warnings.length) console.log(`\n${warnings.length} warning(s):\n  - ${warnings.join('\n  - ')}`);
if (errors.length) {
  console.error(`\n${errors.length} error(s):\n  - ${errors.join('\n  - ')}`);
  process.exit(1);
}
console.log('\nOK');
