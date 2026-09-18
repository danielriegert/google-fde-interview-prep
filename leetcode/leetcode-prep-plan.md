# LeetCode Prep Plan — Data Structures, Algorithms & Mixed Practice

Companion to `../system-design/system-design-prep-plan.md`. This plan covers
the coding-round side of prep: a refresh of core data structures and
algorithms, then unlabeled mixed practice to simulate the real interview
(where nobody tells you which pattern to use).

This repo already has topic notebooks under `english/` (and `chinese/`) —
this plan tells you what order to hit them in and which specific problems
to solve at each stop. Aim for **untimed** on the refresher problems (focus
on correctness + explaining tradeoffs out loud) and **timed, 25-35 min**
on the uncategorized set (simulate interview pressure).

---

## 1. Data structures refresher

For each structure: know how it works, how to implement it in plain Python
(not just call the builtin), when to reach for it, its advantages/
disadvantages, and its complexity — you should be able to say all of this
out loud before opening the notebook.

### 1.1 Arrays & Strings

- **How it works:** contiguous block of memory, O(1) index access via
  address arithmetic. Python `list` is a dynamic array (over-allocates and
  resizes); `str` is an immutable array of characters.
- **When to use:** ordered data, random access by index, cache-friendly
  iteration.
- **Pros:** O(1) access, cache locality, simple. **Cons:** O(n) insert/
  delete in the middle, resizing cost (amortized O(1) append, but a real
  O(n) spike on resize), strings being immutable means concatenation in a
  loop is O(n²) unless you use `''.join(...)`.
- **Complexity:** access O(1), search O(n), append O(1) amortized,
  insert/delete (middle) O(n).
- Notebook: `english/Array_String_LinkedList.ipynb`

### 1.2 Linked Lists

- **How it works:** nodes holding `value` + `next` (and `prev` for
  doubly-linked), scattered in memory, traversed pointer-by-pointer.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

- **When to use:** frequent insert/delete at known positions (e.g. head),
  when you don't need random access, building blocks for LRU caches,
  stacks/queues.
- **Pros:** O(1) insert/delete given a node reference, no resizing.
  **Cons:** O(n) access/search, extra memory per node for pointers, poor
  cache locality.
- **Complexity:** access/search O(n), insert/delete at known node O(1).
- Notebook: `english/Array_String_LinkedList.ipynb`

### 1.3 Hash Tables (dict / set)

- **How it works:** array + hash function mapping keys to bucket indices;
  collisions resolved via chaining or open addressing. Python `dict`/`set`
  are hash tables under the hood.
- **When to use:** O(1) average lookup/insert/delete by key, dedup,
  counting, membership tests, caching (key → value).
- **Pros:** average O(1) ops. **Cons:** no ordering guarantee (insertion
  order is preserved in CPython dicts as an implementation detail, not a
  structural property), worst case O(n) with pathological collisions,
  extra memory overhead vs. an array.
- **Complexity:** average O(1) search/insert/delete, worst case O(n).
- Notebook: `english/Hash_Table.ipynb`

### 1.4 Stacks & Queues

- **How it works:** stack = LIFO (push/pop same end); queue = FIFO (enqueue
  one end, dequeue the other). Implement a stack with a Python `list`
  (`append`/`pop`); implement a queue with `collections.deque` (never a
  `list` — `pop(0)` is O(n)).
- **When to use:** stack — matching/backtracking (parentheses, DFS,
  undo), monotonic stack problems. Queue — BFS, task scheduling, rate
  limiting (sliding window of timestamps).
- **Pros:** O(1) push/pop at the working end. **Cons:** no random access.
- **Complexity:** push/pop/enqueue/dequeue O(1).
- Notebooks: `english/Stack_and_Queue_Part1_Stack.ipynb`,
  `english/Stack_and_Queue_Part2_Queue.ipynb`

### 1.5 Trees & Heaps

- **How it works (tree):** nodes with `val` + child pointers (`left`/
  `right` for binary trees); BST keeps left < node < right for O(log n)
  search when balanced.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

- **How it works (heap):** complete binary tree stored in an array where
  parent ≤ (min-heap) or ≥ (max-heap) both children. Python: `heapq`
  (min-heap only — negate values for a max-heap).
- **When to use:** trees — hierarchical data, sorted-order operations
  (BST), prefix matching (tries). Heaps — top-K, priority scheduling,
  merge-K-sorted, running median.
- **Pros:** BST O(log n) search/insert/delete when balanced; heap O(1)
  peek-min, O(log n) insert/extract. **Cons:** unbalanced BST degrades to
  O(n) (linked list worst case); heap gives no O(1) arbitrary search.
- **Complexity:** balanced BST O(log n) search/insert/delete, worst case
  O(n); heap O(log n) insert/extract, O(1) peek, O(n) build-heap.
- Notebooks: `english/Tree_and_Graph_Part1_Tree.ipynb`,
  `english/Tree_and_Graph_Part2_Advanced_Tree.ipynb`, `english/Heap.ipynb`

### 1.6 Data structures — 5 categorized problems

| #   | Structure   | Problem                                                                                                | Difficulty | Focus                                       |
| --- | ----------- | ------------------------------------------------------------------------------------------------------ | ---------- | ------------------------------------------- |
| 1   | Array       | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)       | Medium     | prefix/suffix arrays, no division           |
| 2   | Linked List | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)                         | Easy       | pointer manipulation, iterative + recursive |
| 3   | Hash Table  | [1. Two Sum](https://leetcode.com/problems/two-sum/)                                                   | Easy       | one-pass hashmap lookup                     |
| 4   | Stack       | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)                              | Easy       | stack matching                              |
| 5   | Tree / Heap | [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Medium     | heap vs. quickselect tradeoff               |

- [ ] Implement each structure from scratch (no builtins) once, even if the
      problem itself doesn't require it — that's the "refresh" part.
- [ ] For each solved problem, state its time/space complexity out loud.

---

## 2. Algorithms refresher

### 2.1 Sorting

- **How it works:** comparison-based (merge, quick, heap sort) or
  non-comparison (counting, radix). Python's built-in `sorted()`/`.sort()`
  is Timsort (hybrid merge/insertion sort).
- **When to use:** need ordered output, enables binary search / two
  pointers afterward, dedup adjacent items.
- **Complexity:**
  | Algorithm | Time (avg) | Time (worst) | Space | Stable |
  |---|---|---|---|---|
  | Bubble/Insertion/Selection | O(n²) | O(n²) | O(1) | mostly yes |
  | Merge Sort | O(n log n) | O(n log n) | O(n) | yes |
  | Quick Sort | O(n log n) | O(n²) | O(log n) | no |
  | Heap Sort | O(n log n) | O(n log n) | O(1) | no |
  | Python Timsort | O(n log n) | O(n log n) | O(n) | yes |
- Notebook: `english/Sorting_Algorithms.ipynb`

### 2.2 Dynamic Programming

- **How it works:** break a problem into overlapping subproblems, cache
  results (memoization, top-down) or build a table bottom-up. Recognize
  it by "optimal substructure + overlapping subproblems."
- **When to use:** counting paths, min/max cost, "can you reach X,"
  problems where brute-force recursion re-solves the same subproblem many
  times.
- **Pros:** turns exponential brute force into polynomial. **Cons:** can
  need O(n) or O(n²) extra space for the table; state definition is the
  hard part and easy to get wrong.
- **Complexity:** typically O(states × transitions); space often
  reducible from O(n²) to O(n) or O(1) by keeping only the last row(s).
- Notebook: `english/Dynamic_Programming.ipynb`

### 2.3 Recursion

- **How it works:** a function calls itself on a smaller subproblem with a
  base case that stops it. Every recursive solution can be rewritten
  iteratively with an explicit stack — know why you'd pick one over the
  other (call stack depth limits in Python, ~1000 by default).

```python
def fib(n, memo={}):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

- **When to use:** naturally recursive structures (trees, graphs,
  backtracking/combinatorics, divide & conquer).
- **Pros:** often the clearest expression of the problem. **Cons:** call
  stack overhead, risk of `RecursionError` on deep inputs, easy to blow up
  to exponential time without memoization.
- **Complexity:** depends on branching factor and depth; always state it
  per-problem (e.g. naive Fibonacci O(2ⁿ) vs. memoized O(n)).
- Notebooks: `english/Topic_DFS_and_Memoization.ipynb`,
  `english/Template_Summary.ipynb`

### 2.4 Greedy

- **How it works:** make the locally optimal choice at each step and never
  revisit it, betting that local optimality leads to global optimality.
  Only valid when the problem has the "greedy choice property" — be ready
  to justify why greedy works (or prove it doesn't with a counterexample).
- **When to use:** interval scheduling, activity selection, some graph
  problems (Kruskal/Prim/Dijkstra are greedy), problems where sorting by
  the right key first makes the answer fall out.
- **Pros:** simple, fast (often O(n log n) from the sort). **Cons:** wrong
  answer silently if the greedy-choice property doesn't actually hold —
  always sanity check with a small counterexample before committing.
- **Complexity:** usually O(n log n) (dominated by an initial sort) then
  O(n) single pass.
- Notebook: `english/Greedy_Algorithms.ipynb`

### 2.5 Sliding Window

- **How it works:** maintain a window `[left, right]` over an array/string,
  expand `right` to grow it, shrink `left` when a constraint is violated —
  avoids the O(n²)/O(n³) cost of recomputing from scratch for every
  subarray.

```python
def longest_unique_substring(s):
    seen = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

- **When to use:** contiguous subarray/substring problems with a
  min/max-length or a constraint (sum ≤ k, at most k distinct chars, etc.).
- **Pros:** turns O(n²) brute force into O(n). **Cons:** only applies to
  contiguous ranges; fixed vs. variable window is a design choice you need
  to get right up front.
- **Complexity:** O(n) time (each pointer moves forward at most n times),
  O(1) or O(k) space for the window state.
- Notebook: `english/Two_Pointers.ipynb` (sliding window is covered as a
  two-pointer variant)

### 2.6 Algorithms — 5 categorized problems

| #   | Technique           | Problem                                                                                                                            | Difficulty | Focus                                            |
| --- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------ |
| 1   | Sorting             | [912. Sort an Array](https://leetcode.com/problems/sort-an-array/)                                                                 | Medium     | implement merge sort or quicksort by hand        |
| 2   | Dynamic Programming | [322. Coin Change](https://leetcode.com/problems/coin-change/)                                                                     | Medium     | bottom-up table, state definition                |
| 3   | Recursion           | [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)                                                    | Medium     | recursion/backtracking, pruning invalid branches |
| 4   | Greedy              | [55. Jump Game](https://leetcode.com/problems/jump-game/)                                                                          | Medium     | greedy reachability, prove the greedy choice     |
| 5   | Sliding Window      | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Medium     | variable-size window with a hashmap              |

- [ ] For sorting, actually write the algorithm — don't just call
      `sorted()`.
- [ ] For DP, write both the recursive+memo version and the bottom-up
      table version of at least one problem, to see the equivalence.

---

## 3. Uncategorized practice (mixed / mock-interview mode)

The real interview never tells you "this is a sliding window problem."
This set is deliberately mixed across structures and techniques, several
combine two concepts, and difficulty ramps up. Solve **cold** — don't
peek at which category a problem belongs to before attempting it.

| #   | Problem                                                                                          | Difficulty | Combines                                            |
| --- | ------------------------------------------------------------------------------------------------ | ---------- | --------------------------------------------------- |
| 1   | [146. LRU Cache](https://leetcode.com/problems/lru-cache/)                                       | Medium     | hashmap + doubly linked list                        |
| 2   | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/)                       | Medium     | grid + DFS/BFS                                      |
| 3   | [127. Word Ladder](https://leetcode.com/problems/word-ladder/)                                   | Hard       | graph BFS + hashset                                 |
| 4   | [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Hard       | two heaps                                           |
| 5   | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)                    | Hard       | two pointers / DP / stack (solve with 2 approaches) |
| 6   | [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)          | Hard       | sliding window + hashmap counting                   |
| 7   | [133. Clone Graph](https://leetcode.com/problems/clone-graph/)                                   | Medium     | graph traversal + hashmap                           |
| 8   | [621. Task Scheduler](https://leetcode.com/problems/task-scheduler/)                             | Medium     | greedy + heap/counting                              |

- [ ] Timebox each to 25-35 minutes before looking at hints.
- [ ] After solving, do the "what if" follow-up: what if input doesn't fit
      in memory, what if it needs to be thread-safe, what's the
      streaming/online version — this role (FDE) rewards production
      thinking layered on top of the raw algorithm.
- Once through this list, pull further unlabeled reps from
  `english/Google_Real_Interview_Questions.ipynb` and `english/Mini_Topics.ipynb`.

---

## 4. Suggested schedule

- August 14: Sliding window (& Two Pointers) -> done
- August 15: Hash map / set -> done
- August 16: Stack, queue, and monotonic stacks -> queue missing
- August 17: Linked list -> done
- August 18: Binary tree DFS/BFS and Tries -> done
- August 19: Graph DFS/BFS and Topological Sort -> Topological sort missing
- August 20: Binary search (focus on answer space)
- August 21: Dynamic programming (focus on 1D/2D grids & memoization)
- August 22: Heap and priority queue (plus quick review of Intervals if time permits), time and space complexity

Accross: all sections also study top google interview questions

### 4.1 Second Round

## Week 1: Core Fundamentals & Data Structures

| Day       | Focus Area                                     | Key Concepts & Target Problems                                                                                                                                                                   |
| --------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---- |
| **Day 1** | Arrays, Strings, Sliding Window & Two Pointers | Contiguous subarrays/substrings, window state maintenance. Practice **Longest Substring Without Repeating Characters (LC 3)**, **Container With Most Water (LC 11)**, and **3Sum (LC 15)**.      | Done |
| **Day 2** | Hash Maps, Sets & Linked Lists                 | Frequency counting, fast & slow pointers, and dummy node manipulation. Practice **Subarray Sum Equals K (LC 560)**, **Linked List Cycle II (LC 142)**, and **LRU Cache (LC 146)**.               |
| **Day 3** | Stacks, Queues, & Monotonic Stacks             | LIFO/FIFO structures, next greater elements, and window maximums. Practice **Daily Temperatures (LC 739)**, **Sliding Window Maximum (LC 239)**, and **Valid Parentheses (LC 20)**.              |
| **Day 4** | Binary Trees, DFS/BFS & Tries                  | Tree traversals, root-to-leaf paths, prefix matching. Practice **Binary Tree Maximum Path Sum (LC 124)**, **Lowest Common Ancestor of a Binary Tree (LC 236)**, and **Implement Trie (LC 208)**. |
| **Day 5** | Graphs, DFS/BFS & Topological Sort             | Component traversal, unweighted shortest paths, and dependency DAG ordering. Practice **Number of Islands (LC 200)**, **Word Ladder (LC 127)**, and **Course Schedule II (LC 210)**.             |
| **Day 6** | Intervals                                      | Start/end time sorting, interval overlapping, and merging logic. Practice **Merge Intervals (LC 56)**, **Insert Interval (LC 57)**, and **Meeting Rooms II (LC 253)**.                           |
| **Day 7** | Week 1 Review                                  | Re-attempt any missed problems on a blank page with a strict 30-minute timer.                                                                                                                    |

Week1 problem review:
Tow pointers: leetcode 5
3 (done), 15 (done - review de-dedupe), 105 (done), 236 (done - review again), 222 (done), practice recursion (done), 103 (done), 98 (done), 437 (done- review)
Pathsum problems: 112, 64, 113,437

Graph: 200 (done), 547 (done - review again), 130 (done), 399, 133 (done), 207 & 210 (Topological sort). 433 (understan teim and space)

ToDos: define common edge cases for each data structure, learn time and space complexity for each, review data structure general knowledge,

---

## Week 2: Advanced Paradigms & Algorithms

| Day        | Focus Area                             | Key Concepts & Target Problems                                                                                                                                                                                           |
| ---------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Day 8**  | Time & Space Complexity                | Analyzing recursion trees, amortized array/hash map operations, and bit manipulation constraints. Practice **Single Number (LC 136)** and **Counting Bits (LC 338)**.                                                    |
| **Day 9**  | Binary Search (Answer Space)           | Defining low/high bounds on monotonic predicates, minimization/maximization. Practice **Koko Eating Bananas (LC 875)**, **Capacity To Ship Packages Within D Days (LC 1011)**, and **Split Array Largest Sum (LC 410)**. |
| **Day 10** | Heaps & Priority Queues                | Min/max heaps, custom comparators, dynamic streaming stats. Practice **Top K Frequent Elements (LC 347)**, **Find Median from Data Stream (LC 295)**, and **Merge k Sorted Lists (LC 23)**.                              |
| **Day 11** | Dynamic Programming (1D & Memoization) | State definitions, overlapping subproblems, and bottom-up iterations. Practice **Coin Change (LC 322)**, **Longest Increasing Subsequence (LC 300)**, and **Word Break (LC 139)**.                                       |
| **Day 12** | Dynamic Programming (2D Grids)         | Matrix coordinate states and string alignment sequences. Practice **Unique Paths II (LC 63)**, **Longest Common Subsequence (LC 1143)**, and **Edit Distance (LC 72)**.                                                  |
| **Day 13** | Backtracking & Greedy Algorithms       | Exhaustive search pruning vs. local invariant choices. Practice **Letter Combinations of a Phone Number (LC 17)**, **Word Search (LC 79)**, and **Jump Game II (LC 45)**.                                                |
| **Day 14** | Week 2 Review                          | Focus heavily on identifying hidden DP states and writing clean backtracking templates.                                                                                                                                  |

Trie: 211
Binary Search: 162, 34, 74, 33, 153, practice answer space problems
DP 1D: 139, 140, 322 and Coin Change 2, different flavours of 1d DP, 300
DP 2D: 120, 62 & 63, 64

## Greedy: 55, 122

## Week 3: Top Google Problems & Mock Interviews

| Day           | Focus Area                              | Key Concepts & Target Problems                                                                                                                                                               |
| ------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Day 15**    | Top Google Practice Set (Part 1)        | High-frequency array and string challenges. Practice **Trapping Rain Water (LC 42)**, **Next Permutation (LC 31)**, and **Minimum Window Substring (LC 76)**.                                |
| **Day 16**    | Top Google Practice Set (Part 2)        | Complex multi-system data structures. Practice **Serialize and Deserialize Binary Tree (LC 297)**, **Design Add and Search Words Data Structure (LC 211)**, and **Word Search II (LC 212)**. |
| **Day 17**    | Hard Edge Cases & Optimization          | Drills on space-time trade-offs and code modularization. Practice **Median of Two Sorted Arrays (LC 4)** and **Binary Tree Maximum Path Sum (LC 124)**.                                      |
| **Day 18**    | Mock Interview 1 (Timed Loop)           | Simulate a full 45-minute Google interview. Code entirely on a plain text editor without syntax highlighting, state your assumptions early, and talk through trade-offs.                     |
| **Day 19**    | Mock Interview 2 (Post-Mortem & Polish) | Run another simulation focusing on code quality, variable naming, and proactive time/space complexity disclosure. Review errors from Mock 1.                                                 |
| **Day 20–21** | Final Review & Rest                     | Lightly review your personal error log and key template structures. Prioritize rest over cramming before your loop.                                                                          |

# Approach:

Recommended Time Split: 30 / 70

    30% Coding / Syntax / Edge Cases: Writing out the actual code (or heavily typing it out) to build muscle memory.

    70% Pattern Identification, High-Level Solution, & Trade-offs: Reading, diagramming, talking through the approach, and analyzing time/space complexity.

How to Structure Each Day (Per Problem)

Spend roughly 20–30 minutes total per problem, broken down like this:

    Read & Identify (3 mins): Look at the constraints. What data structure or pattern does this scream? (e.g., “Sorted array with a search condition? Binary search on answer.”)

    High-Level Design & Walkthrough (7–10 mins):

        Write down the core algorithm in plain English or pseudocode.

        Trace an example on paper or mentally to catch edge cases (empty inputs, duplicates, boundary values).

        State the target Time and Space complexity before you code.

    Write Code / Pseudo-Code (10 mins):

        If you are short on time, write clean pseudo-code focusing purely on the core logic (the loops, pointer adjustments, or recursive calls) rather than worrying about boilerplate syntax.

        If a problem uses a tricky standard template (like Dijkstra's or a specific Trie implementation), type it out fully once to lock it in.

    The Look-Up Rule (The 15-Minute Hard Stop):

        If you stare at a problem for 15 minutes and cannot figure out the optimal pattern, stop.

        Read the solution immediately, understand why that pattern works, and write down the key takeaway. Do not waste precious hours spinning your wheels on brute force.
