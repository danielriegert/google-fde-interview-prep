"""
Key Python operations: Heaps & Priority Queues (heapq).
"""

"""
heapq has no heap class -- it operates in place on an ordinary list, which it
treats as a min-heap. There is no built-in max-heap; negate values to simulate one.

Complexity (n = heap size, k = items requested for top-k operations):
| Operation      | Call                              | Cost       |
| --------------- | ---------------------------------- | ---------- |
| heapify         | heapq.heapify(list)                | O(n)       |
| push            | heapq.heappush(h, x)               | O(log n)   |
| pop min         | heapq.heappop(h)                   | O(log n)   |
| peek min        | h[0]                                | O(1)       |
| push + pop      | heapq.heappushpop(h, x)            | O(log n)   |
| pop + push      | heapq.heapreplace(h, x)            | O(log n)   |
| top-k           | heapq.nlargest/nsmallest(k, it)    | O(n log k) |
| merge sorted    | heapq.merge(*its)                  | O(n log k) |
"""
import heapq

# --- heapify: rearrange an existing list into heap order, in place ---
# Faster than pushing items one at a time. O(n)
nums = [5, 1, 8, 3, 9, 2]
heapq.heapify(nums)          # nums is now heap-ordered, not fully sorted
# nums[0] is now the smallest value; the rest only satisfy the heap property

# --- push: add x, then sift it up until the heap property holds again ---
heapq.heappush(nums, 4)      # O(log n)

# --- pop: remove & return the smallest item ---
# The last leaf moves to the root, then sifts down. O(log n)
smallest = heapq.heappop(nums)

# --- peek: there is no heapq.peek -- the list IS the heap, min sits at index 0 ---
smallest = nums[0]           # O(1), read-only -- does not remove or reorder anything

# --- heappushpop / heapreplace: combine a push and a pop in one call ---
# Cheaper than two separate operations, but each has a different order.
heapq.heappushpop(nums, 4)   # compares 4 to the root FIRST -- may never enter the heap
heapq.heapreplace(nums, 4)   # pops the root FIRST, then pushes 4 -- heap must be non-empty
# use heapreplace for fixed-size "keep the k smallest seen so far" windows

# --- nlargest / nsmallest: top-k without sorting the whole collection ---
# Accepts a key function -- handy on dicts and objects. O(n log k)
data = {'a': 5, 'b': 1, 'c': 9}
heapq.nlargest(2, data.items(), key=lambda x: x[1])   # [('c', 9), ('a', 5)]

# --- merge: lazily merge already-sorted iterables into one sorted iterator ---
# Does not load everything into memory. O(n log k)
a = [1, 4, 7]
b = [2, 5, 8]
list(heapq.merge(a, b))      # [1, 2, 4, 5, 7, 8]

# --- Priority queue pattern ---
# Push (priority, item) tuples. Tuples compare element-by-element, so the
# heap naturally orders by the first field. Lower number = higher priority
# since heapq is a min-heap.
pq = []
heapq.heappush(pq, (2, 'do laundry'))
heapq.heappush(pq, (1, 'fix bug'))
heapq.heappush(pq, (3, 'read book'))

while pq:
    priority, task = heapq.heappop(pq)
    print(priority, task)
# Output: 1 fix bug   2 do laundry   3 read book

# --- Max-heap via negation ---
# heapq only implements a min-heap. Negate on push, negate again on pop.
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -9)
largest = -heapq.heappop(max_heap)   # 9

# --- Tie-breaking with a counter ---
# Equal priorities fall through to comparing the task itself -- add a unique
# middle field to avoid that (and to avoid TypeError on unorderable items).
import itertools

counter = itertools.count()
pq = []
heapq.heappush(pq, (2, next(counter), 'do laundry'))
heapq.heappush(pq, (1, next(counter), 'fix bug'))
# ties now resolve by insertion order -- the queue becomes stable

"""
Gotchas:
- TIE: Two equal-priority tuples with an unorderable second field (a dict, a
  custom object) raise TypeError on comparison. Fix with the itertools.count()
  tiebreaker above.
- DEL: heapq has no decrease-key or remove(item). The standard workaround is
  lazy deletion: mark an entry stale in a side dict and skip it when it
  surfaces at pop time -- this is the exact friction point in implementing
  Dijkstra's algorithm.
- SORT: A heap is only partially ordered. Iterating the underlying list gives
  no useful order beyond "index 0 is the minimum" -- it is not a sorted array.

Heap vs. deque, in one line each:
- heapq: answers "what's the smallest/largest value I currently hold?" --
  ordered by value, O(log n) to insert or extract the extreme, O(1) to peek it.
- collections.deque: answers "what did I add first or most recently?" --
  ordered by insertion, O(1) to push or pop at either end, no notion of priority.
"""

