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

### Template

1. Problem

- Inputs
- Ouputs
- Contsraints / Rules: e.g do not modify in place

2. Test Cases

- Standard
- Edge Cases

3. Approach

- Patter / Algo
- Stragegy / high level flow / pseudo code
- Complexity

4. Trace some examples to verfiy (optional)

## 8. While coding

- Handle edge cases first (empty input, single element) if they'd otherwise crash the main logic.
- Watch off-by-one errors on loop bounds and pointer moves — trace one example as you write.
- Prefer clarity first, optimize after it's correct.

## 9. After coding

- Trace through 1-2 of the test cases from step 3 against the actual code.
- Restate final time/space complexity.
- Sanity check: does it handle the trivial case (empty/single element) without special-casing bugs?

---

# Topic comparison — complexity & when to use

Covers everything through the Aug 14-20 schedule (sliding window/two pointers
through binary search). DP, heaps/priority queue, and intervals come later
and aren't included yet.

| Topic                        | Core idea                                                                                          | Time                                                               | Space                                                           | When to use / signal                                                                                                         |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Two Pointers                 | two indices moving toward each other or in step over a sorted/array structure                      | O(n)                                                               | O(1)                                                            | sorted array, pair/triplet sum, in-place partition, palindrome check                                                         |
| Sliding Window               | window `[left, right]` expands/shrinks over a contiguous range instead of recomputing from scratch | O(n) — each pointer moves forward at most n times                  | O(1) or O(k) for window state                                   | "contiguous subarray/substring", min/max length under a constraint (sum ≤ k, ≤ k distinct chars)                             |
| Hash Map / Set               | array + hash function for O(1) average key lookup                                                  | O(n) to build, O(1) avg per op                                     | O(n)                                                            | dedup, counting/frequency, one-pass lookup ("have I seen this"), anagrams, pairs summing to target when order doesn't matter |
| Stack                        | LIFO, push/pop from one end (Python `list`)                                                        | O(n) traversal, O(1) per push/pop                                  | O(n)                                                            | matching/nesting (parentheses), undo, backtracking, monotonic stack base, iterative DFS                                      |
| Queue                        | FIFO, enqueue one end / dequeue other (`collections.deque`, never `list`)                          | O(n) traversal, O(1) per enqueue/dequeue                           | O(n)                                                            | BFS frontier, level-order processing, task scheduling, rate limiting                                                         |
| Monotonic Stack              | stack kept increasing or decreasing; pop while the invariant would break                           | O(n) amortized — each element pushed/popped at most once           | O(n)                                                            | "next greater/smaller element", histogram/rectangle problems, span problems                                                  |
| Linked List                  | nodes with `val` + `next` pointer(s), no random access                                             | O(n) traversal/search, O(1) insert/delete at a known node          | O(n), O(1) extra if in-place                                    | frequent insert/delete at known position, LRU cache, reordering, fast/slow pointer problems (cycle detection, middle node)   |
| Binary Tree DFS              | recurse into children, process pre/in/post-order                                                   | O(n) — visits every node once                                      | O(h) call stack — O(log n) balanced, O(n) worst case (skewed)   | path sums, subtree properties, tree backtracking, "explore full path before backtracking"                                    |
| Binary Tree BFS              | level-by-level traversal via a queue                                                               | O(n)                                                               | O(w) queue width — worst case O(n) at the last level            | level-order output, shortest path/min depth in an unweighted tree, "process nodes grouped by distance"                       |
| Trie                         | tree of characters, each path from root = a prefix                                                 | O(L) insert/search, L = word length, independent of n words stored | O(total characters stored across all words)                     | prefix matching, autocomplete, word search / dictionary problems                                                             |
| Graph DFS                    | recurse/stack into unvisited neighbors, backtrack on dead ends                                     | O(V + E)                                                           | O(V) for visited set + O(V) recursion/explicit stack worst case | connected components, cycle detection, topological sort, "all paths", flood fill/islands                                     |
| Graph BFS                    | level-by-level traversal via a queue, optionally multi-source                                      | O(V + E)                                                           | O(V) for visited set + queue                                    | shortest path in an unweighted graph, "fewest steps", multi-source spread (rotting oranges, nearest water cell)              |
| Topological Sort             | DFS post-order reversed, or Kahn's BFS with in-degree counts                                       | O(V + E)                                                           | O(V)                                                            | ordering tasks with dependencies/prerequisites, detecting a cycle in a DAG, build/scheduling systems                         |
| Binary Search (index space)  | halve a _sorted_ search space each step                                                            | O(log n)                                                           | O(1)                                                            | searching a sorted array, peak finding, rotated sorted arrays                                                                |
| Binary Search (answer space) | halve the range of _possible answers_, using a monotonic feasibility check                         | O(log(range)) × O(cost of feasibility check)                       | O(1)                                                            | "minimum/maximum X such that condition holds" where feasibility is monotonic (min capacity, min speed, min time)             |

**Quick disambiguation:**

- Stack vs. Queue vs. Monotonic Stack: stack = undo/matching (LIFO), queue = BFS/ordering (FIFO), monotonic stack = "next greater/smaller" (maintains an invariant, not just insertion order).
- Tree DFS vs. Tree BFS: DFS for path/subtree properties and backtracking, BFS for level-order or shortest-path-by-edges.
- Graph DFS vs. Graph BFS vs. Topological Sort: DFS for components/cycles/all-paths, BFS for shortest path (unweighted), topo sort specifically for dependency ordering (and it's really DFS or BFS underneath).
- Binary search index space vs. answer space: index space searches an already-sorted array; answer space searches a range of candidate answers using a pass/fail check per candidate (the array itself need not be sorted).

---

# Quick reference notes

## Two Pointers

- non-decreasing = can have duplicates, can increase, just not decrease e.g. [0, 2, 2, 3, 4, 4]
- check if list is sorted
- check if modify in place required (affects whether extra space is allowed)
- Python strings are **immutable** — can't modify in place; convert to `list(s)`, mutate, then `''.join(...)` at the end
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

## Sliding Windows

- Prefer sets over lists for membership checks (in).
- del list[0] or list.pop(0) takes \mathcal{O}(k) time because every remaining element in the list must shift left in memory. Repeating this across an array of length n turns an optimal \mathcal{O}(n) algorithm into an \mathcal{O}(n \cdot k) runtime
- When a problem asks for a quantity (e.g., maximum count, length, or sum) rather than the actual items, avoid storing the items themselves.
- In a sliding window, updates at the right boundary (s[i]) and left boundary (s[window_start]) must evaluate the exact character entering or leaving
- Instead of starting from 0 build the first window of size k e.g.
  current_vowels = sum(1 for i in range(k) if s[i] in vowels)
  max_vowels = current_vowels

Then slide the window from index k to the end e.g. for i in range(k, len(s)): . First char of window will be s[i-k]

- ​Count the constraint, not the target: Your original instinct was to count the 1s. The key unlock is to track your limited resource instead—the 0s you are allowed to flip. If you control the 0s, the 1s take care of themselves.
  ​- Let the window length do the math: You don't need a dedicated counter for the maximum 1s seen. Because every element inside a valid window is either a native 1 or a flipped 0, the formula end - start + 1 automatically gives you the total length of the sequence.
  ​- Maintain a strict "validity state": The logic for shrinking the window should directly match your constraint limit. As soon as zero_count > k, the window is invalid. A simple while loop cleanly advances the start pointer and reclaims your flips until the window is valid again.
- ​Reclaim resources cleanly: Only update your constraint counter (zero_count -= 1) when the exact element leaving the window (at the start pointer) is the resource you were tracking (a 0).
- When using indexes as count need to add 1 to result
- Check if window has validity constraint that needs to be maintenance at all times e.g. only k number of 0s

# Sets and Hashmap

- can use set theory e.g. intersection to check if two strings contain the same characters. BUT this alone migh not be enough need to also check that the chars have same frequency e.g. using collections.Counter()
- When there is duplicate logic e.g. nested for loops, see if it can be pre-processed and results stored to dedupe logic
- Cannot use list with Counter, must use string or tuple or dict as not hashable. Use tuple([]) to convert list to tuple.
- Can use list(zip(`*`[[]])) to transpose a matrix. Placing an asterisk in front of grid unpacks the list, passing its individual rows as separate arguments. Writing `*`grid is equivalent to writing: [1, 2, 3], [4, 5, 6], [7, 8, 9]. zip() takes multiple iterables (like lists or tuples) and aggregates them by their index position. It pairs up the 1st element*s*, then the 2nd element*s*, then the 3rd element*s*, and so on.
Before: grid is organized by rows: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]. After: columns is organized by columns: [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

# Stack

- Think of a stack whenever a problem involves "Undo," "Backtracking," "Cancellation," or "Matching" actions. Last-In, First-Out (LIFO) Dependency: The most recent element added is the very first one that needs to be affected, removed, or validated.
- How to Apply a Stack (The Pattern)
  - Step 1: Initialize an empty container. Use a simple Python list (stack = []).
  - Step 2: Iterate through the sequence. Examine elements one by one from left to right.
  - Step 3: Branch on conditions:
    Trigger/Action Element (e.g., \*): Modify the stack (usually a .pop()). Note: Always trust that the problem constraints guarantee valid inputs, meaning you won't pop from an empty stack unless specified.
    Normal Element (e.g., any letter): Push it onto the stack (.append()).
  - Step 4: Reconstruct the result. Convert the stack back to the required data type at the end (e.g., "".join(stack) for strings).
- In some cases a while loop might be needed if need to check other elements in stack as well not just top
- Instead of using stack can also use a pointer that directly operate on the input:

```python
class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        # We will use the list itself as a stack, with 'j' pointing to the top element.
        # Initially, the stack is empty, so pointer j starts at -1.
        j = -1

        for ast in asteroids:
            # Handle collisions while the stack has a right-moving asteroid
            # and current asteroid is left-moving
            while j >= 0 and ast < 0 < asteroids[j]:
                if asteroids[j] < -ast:
                    # Top of stack is smaller, it explodes (move pointer back)
                    j -= 1
                    continue
                elif asteroids[j] == -ast:
                    # Both explode
                    j -= 1
                # Current asteroid is smaller or equal, so current asteroid dies.
                # We break out of the collision check.
                break
            else:
                # If the loop finished without breaking, the current asteroid survives.
                # Place it in the next available position and increment pointer j.
                j += 1
                asteroids[j] = ast

        # Return only the surviving portion of the array up to pointer j
        return asteroids[:j + 1]
```

- Sometimes I moght have to use 2 stacks especially, when they are for different things
- Might have to handle multi digit numbers e.g. ´k = k \* 10 + int(char)´

# Linked List

- Cannot jump directly to index (e.g. l[1]) need to follow the links
- Cannot call len() on linked list
- Deleting middle node (leetcode 2095). Step-by-Step Procedure

1.  Handle the Edge Case
    Check: If the linked list is empty (head is None) or has only one node (head.next is None), you cannot delete a middle node.
    Action: Return None immediately, because removing the only element leaves an empty list.
2.  Initialize the Pointers and Dummy Node
    Create a Dummy Node: Instantiate a dummy node whose .next points to the head of the list (e.g., dummy = ListNode(0, head)).
    Why? This ensures that if the middle node happens to be the very first node (or if the list is short), your tracking pointer has a valid node to sit on before the target.
    Set Slow Pointer: Point slow to the dummy node.
    Set Fast Pointer: Point fast to the head node.
3.  Traverse the List (Finding the Middle)
    Run a loop while fast and fast.next are not None:
    Move the slow pointer forward by 1 step (slow = slow.next).
    Move the fast pointer forward by 2 steps (fast = fast.next.next).
    Why this works: Because fast travels twice as fast as slow, when fast reaches the end of the list (None), slow will have traveled exactly half the distance. Crucially, because slow started one step back at dummy, it will stop precisely one node before the middle node.
4.  Delete the Target Node
    Bypass the Middle Node: Update slow.next to point to the node after the middle node (slow.next = slow.next.next).
    Result: The middle node is now completely unlinked from the chain, effectively deleting it. (Python's garbage collector will automatically clean up the orphaned node).
5.  Return the Modified List
    Return dummy.next, which points to the new head of your modified linked list (in case the original head was preserved or adjusted correctly).

- Re-ordering a linked list (leetcode 328):

1. First check `if not head and not head.next` if it only has one or two nodes it is laready in right order and can just return head
2. Initialize even and odd. store curren head of even as in the end it will be merged with end of odd
3. Iterate through linked list with while loop condition `while even and even.next` (use even as it is the fast pointer, odd is slow pointer)
4. We start to build out two seperate linked lists. One for odd and one for even
   `odd.next = even.next, odd = odd.next` -> set odd.next to next odd element which is the one after the even one, thenset current odd pointer to the same position
   `even.next = odd.next, even = even.next` -> same as above but for even
5. Merge the two lists `odd.next = even_head` -> we point then end off the odd list to the start of the even list
6. Return the head

# Trees - DFS

- If paths can start and end anywhere, a single top-down traversal is insufficient, and you need a mechanism (like prefix sums or a double-recursion pattern) to evaluate sub-paths from every possible starting point.
- Whenever a problem asks for subarrays or sub-paths that sum to a target, think Prefix Sums combined with a Hash Map
- Backtrack: State modification must be undone when exiting a node's subtree. Always reverse your changes (e.g., decrementing the frequency map) during the "unwinding" phase of recursion to keep your data structure localized to the current path.
- Path starting directly at the current root/sub-root needs to be counted
- When a problem has strict path constraints (like alternating directions), you need to pass state parameters down the recursion tree.
  Tracking incoming direction: By passing both left-incoming (l) and right-incoming (r) path lengths, each node instantly knows how it was reached and whether a continuation is valid.
- Look closely at the problem statement's guarantees. LeetCode 236 guarantees that both p and q exist in the tree.
  This guarantee allows the algorithm to short-circuit safely. The moment you hit one of the target nodes, you don't need to look any further down that branch because the existence of the other node dictates the final outcome at the parent level.

# Tree BFS

- When using BFS level order traversal and I need to rack the level then I need to use seperate counter for level.
  Can NOT use size of queue as it doesn't equal the level.

# Trie

- If order matters, might be beneficial to sort input before inserting into Trie

# Graph DFS

Exploring All Paths or Backtracking: When you need to find all possible solutions, combinations, or paths (e.g., solving Sudoku, N-Queens, or finding a path through a maze).
Cycle Detection: Checking whether a graph contains a loop or cycle.
Topological Sorting: Ordering tasks based on dependencies (prerequisites).
Connected Components / Flood Fill: Finding how many distinct "islands" or groups exist in a grid, or filling a connected region with a new color.

Note: Tree is a specialized, restricted type of graph. It is hierarchical, undirected, connected, and acyclic (meaning it has no loops or circuits).

1. Recognizing Connected Components
   The Pattern: Whenever a problem asks you to find "clusters," "groups," "islands," or "provinces" of connected elements, you are dealing with a Connected Components problem in graph theory.
   The Strategy: The standard approach is to iterate through every node, and whenever you find an unvisited node, trigger a traversal (like DFS or BFS) to explore the entire component, incrementing your group counter by 1.

2. Adjacency Matrix vs. Adjacency List
   Matrix Representation (isConnected): The input gives us a 2D grid where rows and columns represent nodes, and cells represent edges ($1$ or $0$).
   The Trade-off: While a matrix makes it easy to see all connections at a glance, checking a node's neighbors requires scanning an entire row of length $n$. This makes the time complexity $O(n^2)$, unlike an adjacency list which lets you iterate directly over actual neighbors.
3. The Power of the visited Array
   Avoiding Infinite Loops: In graph problems with cycles (like City A connecting to City B, and City B connecting back to City A), tracking visited nodes prevents your code from running infinitely.
   Preventing Double-Counting: The visited array ensures that once a city is processed as part of a province, future iterations of the main loop will safely ignore it.

- Dual-Direction Graph Modeling: When dealing with directed trees/graphs where you need to check alignment relative to a root, store edges in both directions in your adjacency list. Assign weights/costs (1 for moving away from the root, 0 for moving toward it) to easily evaluate edge correctness on the fly.

# Graph BFS

BFS explores the graph level by level, moving outward in expanding rings from the starting node. Use BFS when:
Finding Shortest Paths: In an unweighted graph or grid, BFS guarantees that the first time you reach a target node, you have taken the shortest possible path.
Level-Order Processing: When you need to process nodes grouped by their distance from the source (e.g., finding all friends within 2 degrees of connection).
Multi-Source Scenarios: When multiple starting points need to spread outward simultaneously (like our Rotting Oranges problem or finding the nearest water cell).

- Maze Solving Approach using BFS:
  - get size of maaze (n,m)
  - initiate queue and pop entrance doodrdinates with step = 0
  - mark entrance as visited
  - set up list of all possible directions we can move in
  - while queue is not empty
    - pop element from queue
    - iterate over list of possible directions to move
      - calcaulte new coordinates to move to
      - check if in boundaries of maze
      - check if at edge. if yes return step + 1. we are done
      - if not at edge mark as visited and append() to queue
  - if no entrance found return -1
  - Time Complexity: O(m x n) and Space Complexity: O(m x n)

- Multi-Source Breadth-First Search (BFS) e.g. Leetcode 994 is a variation of the standard BFS algorithm where, instead of starting your search from a single starting node, you start from multiple nodes simultaneously.
  In a standard BFS, you typically push one starting coordinate or node into your queue and explore outward layer by layer. In a Multi-Source BFS, you seed your initial queue with all starting nodes at the very beginning (at step 0).

# Binary Search

- Might not alway be exat match e.g. we are only looking for lower boundary
- Array needs to be sorted for binray search to work. In some cases we will be able to still perform binary search by using a modified version of the algo were we check if we are on an upward or donwward slope amnd move the pointer closer to each other unitl peak is found
- Remember array can also contain DUPLICATES
- Use below when need to dviide and round up when float

```python
import math
min_potion = math.ceil(success / spell)
```

| Feature       | `right = len(arr) - 1` | `right = len(arr)` |
| ------------- | ---------------------- | ------------------ |
| Interval Type | Closed `[0, n-1]`      | Half-Open `[0, n)` |

- Type of Binary Search
  | Type of Binary Search | What low and high represent | When to use |
  | --- | --- | --- |
  | Index Space | Array indices (0 to N-1) | Searching inside a sorted array, peak finding, rotated arrays. |
  | Value Space | Numerical bounds of the solution (e.g., min/max possible answers) | Optimization problems ("find the minimum/maximum capacity/speed/time"). |

- In binary search on the answer (often called binary search on the solution space), the search space is always the range of possible values for the answer you are trying to find (in this case, the time $T$).
  Here is why this rule of thumb works so well:
  - Identify the target: You ask yourself, "What is the final value I am trying to minimize or maximize?" (e.g., minimum time, maximum capacity, minimum speed).
  - Determine the bounds: Find the absolute minimum and absolute maximum possible values that this target could possibly take.
  - Monotonicity check: Verify if the problem has a "threshold" property—meaning if a value $X$ works, does every value greater than $X$ also work (for minimization) or vice versa?

# Other

- .sort( ) -> sorts in place
- sorted([]) -> creates new object. also works on strings and tuples
