# LeetCode Flashcards

Study cards built from `../leetcode/notes` and `../leetcode/english` (Hard LeetCode problems excluded).

```bash
npm install
npm run dev        # http://localhost:5173
npm test           # progress + deck logic
npm run validate   # card schema, unique ids, no Hard problems
npm run build      # type-check + production build into dist/
```

Needs Node 18+ (Vite 5 is pinned because Vite 7/8 require Node >= 20.19).

## How it works

- **Themes** group the cards. Study a theme *in order* or *shuffled*, or start a **random mix** of all themes (or a chosen set).
- Reveal the answer, then grade yourself **Got it** (`1`) or **Missed it** (`2`). Space reveals / advances.
- A wrong answer resets the card's streak and queues it again at the end of the session.
- After **3 correct in a row** a **Mark as completed** button (`C`) appears. Completed cards are left out of every future session and listed under **Completed**, where **Mark as not completed** puts them back (streak restarts at 0).
- Progress lives in this browser's `localStorage`. Use **⚙ Progress** to export/import it as JSON or reset it.

## Adding or editing cards

Cards are JSON in `src/data/cards/<theme-id>.json`; themes are listed in `src/data/themes.ts`.

```json
{
  "id": "binary-search-lower-bound-template",
  "theme": "binary-search",
  "kind": "template",
  "front": "Template: lower bound (first index with nums[i] >= target)?",
  "back": "Markdown answer, code fences allowed.",
  "lc": 34,
  "source": "notes/binary_search.py"
}
```

- `id` must be kebab-case, start with the theme id, and be unique. **Never change an id** once you have progress - progress is keyed by it.
- `kind`: `concept | template | complexity | gotcha | pattern | problem`. `lc` is optional.
- `scripts/hard-problems.json` lists Hard LeetCode numbers; `npm run validate` fails if a card's `lc` is in it.
