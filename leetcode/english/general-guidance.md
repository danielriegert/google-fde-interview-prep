# LeetCode Problem-Solving Playbook

## 1. Understand the problem

- Restate the problem in your own words out loud before coding.
- Identify: inputs, outputs, and the exact transformation between them.
- Note the return type precisely (index vs value, list of pairs, in-place mutation, boolean, etc).
- Is the answer unique, or could there be multiple valid answers (any one accepted)?

## 2. Ask clarifying questions

- Can the input be empty / null / length 0 or 1?
- Are there duplicates in the input? Does that matter?
- Is the array/list sorted? Can I assume it, or do I need to sort it myself?
- Are values only positive, or can they be negative / zero?
- Can I modify the input in place, or must I preserve it?
- What's the expected size of input (n)? This hints at required time complexity
  (n <= 20 -> exponential ok, n <= 10^4 -> O(n^2) ok, n <= 10^6 -> need O(n log n) or O(n)).
- Are there ties, and if so how should they be broken?
- What should happen if no valid answer exists (return -1, empty list, throw)?

## 3. Work through test cases before coding

- Trivial case: empty input, single element.
- Normal case: small example, trace by hand.
- Duplicates / repeated values.
- Already sorted / reverse sorted (if relevant).
- All same value.
- Negative numbers / zero (if relevant).
- Largest allowed input (mentally check complexity holds up).
- The one given in the prompt — actually trace it, don't just eyeball it.

## 4. Look for pattern clues in the problem statement

- "sorted array" -> binary search, two pointers.
- "subarray / substring, contiguous" -> sliding window, prefix sum.
- "pairs / triplets that sum to target" -> two pointers (if sortable) or hash set.
- "in-place, O(1) space" -> two pointers / cyclic sort, not extra data structures.
- "k-th largest/smallest", "top k" -> heap, or quickselect.
- "all combinations / permutations / subsets" -> backtracking.
- "shortest path / fewest steps / levels" -> BFS.
- "connected components / can you reach / all paths" -> DFS or Union-Find.
- "next greater/smaller element" -> monotonic stack.
- "sliding maximum / minimum" -> monotonic deque.
- "overlapping intervals / merge / scheduling" -> sort by start (or end), sweep.
- "counts of characters / anagram / frequency" -> hash map / array as counter.
- "linked list, detect cycle / find middle" -> fast-slow pointers (Floyd's).
- "min/max cost to reach state, count ways" -> dynamic programming.
- "repeated overlapping subproblems with choices" -> DP (top-down memo or bottom-up table).
- "range queries, updates" -> prefix sum, difference array, or segment tree / BIT.
- "matrix, grid, islands" -> DFS/BFS flood fill, or union-find.
- "words, prefixes" -> trie.
- "min number of X to cover Y", "max Y under a budget/capacity", "non-overlapping intervals / scheduling" -> greedy: sort by a key, one pass, prove with an exchange argument (or fall back to DP if you find a counterexample). See `Greedy_Algorithms.ipynb` for the full pattern writeup.

## 5. Pick the algorithm / data structure

Rough decision order once a pattern is identified:

1. Can I do it in one pass with a hash map/set? (O(n) time, O(n) space)
2. Is the input sorted or sortable, letting me use two pointers / binary search? (O(n log n) or O(n))
3. Is there a sliding window over a contiguous range? (O(n))
4. Do I need ordering/priority at each step? (heap, O(n log k))
5. Is this a graph/tree traversal? (BFS for shortest/levels, DFS for exploring/backtracking)
6. Are there overlapping subproblems / optimal substructure? (DP — define state, transition, base case)
7. Nothing else fits and n is small? (brute force / backtracking is fine)

## 6. Time & space complexity quick guidance

**Reading complexity off input size (n).** Use this to sanity-check the approach against constraints:
| n | acceptable complexity |
|---|---|
| <= ~10-12 | O(2^n), O(n!) — brute force, permutations |
| <= ~20-25 | O(2^n) with pruning, bitmask DP |
| <= ~500 | O(n^3) |
| <= ~5,000 | O(n^2) |
| <= ~10^5 - 10^6 | O(n log n) or O(n) |
| <= ~10^8 | O(n) with a tight constant, or O(log n) / O(1) |
| huge / streaming | O(log n) or O(1) per operation |

**Reading complexity off code shape:**

- Single loop over n -> O(n).
- Nested loop, both over n -> O(n^2). Nested loop where inner shrinks (e.g. `for j in range(i, n)`) -> still O(n^2), just half the constant.
- Loop that halves the search space each time (binary search) -> O(log n).
- Loop + inner binary search -> O(n log n).
- Sorting -> O(n log n) time; usually O(n) or O(log n) extra space depending on implementation.
- Recursion: complexity = (number of calls) x (work per call). Count branching factor and depth, or use the recurrence (e.g. T(n) = 2T(n/2) + O(n) -> O(n log n), à la merge sort).
- Two pointers / sliding window, each pointer only moves forward -> O(n) total even though it looks nested.
- Visiting every node/edge of a graph once -> O(V + E).
- Backtracking that explores all subsets -> O(2^n); all permutations -> O(n!).

**Common data structure operation costs** (average case, hash-based unless noted):

- Array: index O(1), search O(n), insert/delete at end O(1) amortized, insert/delete at front or middle O(n).
- Hash map / set: insert, delete, lookup O(1) average, O(n) worst case.
- Sorted array: binary search O(log n), insert/delete O(n) (shifting).
- Heap: push/pop O(log n), peek min/max O(1), build-heap from array O(n).
- Balanced BST (e.g. TreeMap): insert/delete/search O(log n), in-order traversal gives sorted order.
- Linked list: insert/delete at known node O(1), search O(n).
- Union-Find (with path compression + union by rank): effectively O(1) (technically O(α(n))) per operation.
- Trie: insert/search O(L) where L = length of the word/key, independent of n words stored.

**Space complexity gotchas:**

- Recursion uses O(depth) stack space even with no extra data structures — a deep recursion can blow the stack even if "no extra space" was claimed.
- Output/return array usually isn't counted toward extra space unless the problem says otherwise — clarify if unsure.
- In-place means O(1) _extra_ space, not counting the input/output.
- Memoization tables in DP add O(state space) space — state count x transitions per state = time complexity.

## 7. Before coding

- State time and space complexity target out loud.
- Sketch the approach in a couple lines of pseudocode or bullet steps.
- Decide on variable names for pointers/indices up front (left/right, slow/fast, i/j) to avoid confusion mid-write.

## 8. While coding

- Handle edge cases first (empty input, single element) if they'd otherwise crash the main logic.
- Watch off-by-one errors on loop bounds and pointer moves — trace one example as you write.
- Prefer clarity first, optimize after it's correct.

## 9. After coding

- Trace through 1-2 of the test cases from step 3 against the actual code.
- Restate final time/space complexity.
- Sanity check: does it handle the trivial case (empty/single element) without special-casing bugs?

---

# Quick reference notes

- non-decreasing = can have duplicates, can increase, just not decrease e.g. [0, 2, 2, 3, 4, 4]
- check if list is sorted
- check if modify in place required (affects whether extra space is allowed)
- Python strings are immutable — can't modify in place; convert to `list(s)`, mutate, then `''.join(...)` at the end
- `reversed(x)` returns a reverse iterator, not a list/string — wrap in `list(...)` or `''.join(list[])` to materialize it
- Clearly articulate different cases and create placeholders in code for it.
- Be careful with conteol flow if I only use `if` multiple cases might be triggered although not desired. Use `elif` or `else` with nested `if`. Can use `comtinue` alternatively to avoid deep nesting
- With arrays pay attention to first and last elements. These often require special logic
- When using two pointers / sliding window be very clear about **when** and **where** to move pointers
- After initial implementation work interviewer through non trivial test cases to verify solution / edge cases
- If checking whether index is at end of of sequence need to compare i to len(s) - 1 as index starts at 0
- When struggling run through different scenarios
- Sometimes pointer should be initialized with -1 not 0
- When modifiying an array in place never delete elments as it will mess up index. Need to use two pointers approach e.g. swap elements (sorting, re-arranging),overwrite elements (de-dupe or removal), etc.
- If parts of problems are independent then tehy might be solved in two sepeprate steps and then combined e.g. first move all non-0 elements to front then fill remaining with zeroes
- range(0,2) -> first element included, second NOT. same for [1:8] -> 1 to 7
- Use hashmap ONLY if order doesn't matter
- Need to think about ALL edge cases e.g. duplicates, empty strings, end or beginning of string, conditions that might cause out of index
- Think about conditions for early stop
