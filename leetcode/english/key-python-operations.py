"""
Key Python operations: lists and dictionaries.
Adding, removing, and different ways to iterate.
"""

# =========================================================
# LISTS
# =========================================================

nums = [1, 2, 3]

# --- Adding ---
nums.append(4)              # [1, 2, 3, 4]         add single item to the end
nums.extend([5, 6])         # [1, 2, 3, 4, 5, 6]    add multiple items to the end
nums.insert(0, 0)           # [0, 1, 2, 3, 4, 5, 6] insert at a specific index
nums = nums + [7]           # [0, 1, 2, 3, 4, 5, 6, 7]  concatenation (new list)
nums += [8]                 # [.., 8]               in-place concatenation

# --- Removing ---
nums.remove(0)               # removes first occurrence of value 0
last = nums.pop()            # removes & returns last item
first = nums.pop(0)          # removes & returns item at index 0
del nums[0]                  # removes item at index 0 (no return value)
del nums[0:2]                # removes a slice
nums.clear()                 # removes everything -> []

# --- Iterating ---
nums = [10, 20, 30, 40]

for x in nums:                        # values only
    pass

for i in range(len(nums)):            # index only
    pass

for i, x in enumerate(nums):          # index + value
    pass

for x in reversed(nums):              # backwards
    pass

for x in sorted(nums, reverse=True):  # sorted copy, original unchanged
    pass

a, b = [1, 2, 3], [4, 5, 6]
for x, y in zip(a, b):                # iterate two lists in parallel
    pass

squares = [x * x for x in nums]              # list comprehension
evens = [x for x in nums if x % 2 == 0]      # list comprehension with filter


# =========================================================
# DICTIONARIES
# =========================================================

d = {"a": 1, "b": 2}

# --- Adding / updating ---
d["c"] = 3                     # add new key or overwrite existing key
d.update({"d": 4, "a": 10})    # add/overwrite multiple keys at once
d.setdefault("e", 5)           # set only if key doesn't already exist

# --- Removing ---
del d["e"]                     # remove key (raises KeyError if missing)
val = d.pop("d")               # remove & return value (raises KeyError if missing)
val = d.pop("missing", None)   # remove with default if key not found (no error)
key, value = d.popitem()       # remove & return the last inserted (key, value) pair
d.clear()                      # remove everything -> {}

# --- Iterating ---
d = {"a": 1, "b": 2, "c": 3}

for key in d:                  # keys only (default iteration)
    pass

for key in d.keys():           # keys only (explicit)
    pass

for value in d.values():       # values only
    pass

for key, value in d.items():   # key + value pairs
    pass

doubled = {k: v * 2 for k, v in d.items()}     # dict comprehension
filtered = {k: v for k, v in d.items() if v > 1}  # dict comprehension with filter

# safe lookup without KeyError
value = d.get("z")             # None if missing
value = d.get("z", 0)          # default value if missing

# =========================================================
# Set
# =========================================================

### Summary of Set Operations
"""
| Operation | Operator | Equivalent Method | Description |
| --- | --- | --- | --- |
| **Union** | `&#124;` | `set.union(other)` | Combines elements from both sets (removes duplicates). |
| **Intersection** | `&` | `set.intersection(other)` | Keeps only elements found in **both** sets. |
| **Difference** | `-` | `set.difference(other)` | Keeps elements in the first set that are **not** in the second. |
| **Symmetric Difference** | `^` | `set.symmetric_difference(other)` | Keeps elements in **either** set, but **not in both**. |
| **Subset** | `<=` | `set.issubset(other)` | Checks if all elements of the set are in the other. |
| **Superset** | `>=` | `set.issuperset(other)` | Checks if the set contains all elements of the other. |
| **Disjoint** | N/A | `set.isdisjoint(other)` | Checks if sets share **no** common elements. |
"""

### 1. Union (`&#124;` or `.union()`)

# Combines two or more sets, automatically removing duplicate values.

python_devs = {"Alice", "Bob", "Charlie"}
java_devs = {"Bob", "David", "Eve"}

# Using the | operator
all_devs = python_devs | java_devs
print(all_devs)  # Output: {'Alice', 'Bob', 'Charlie', 'David', 'Eve'}


### 2. Intersection (`&` or `.intersection()`)

# Finds the common elements that exist in all participating sets.

python_devs = {"Alice", "Bob", "Charlie"}
java_devs = {"Bob", "David", "Eve"}

# Using the & operator
both_devs = python_devs & java_devs
print(both_devs)  # Output: {'Bob'}

### 3. Difference (`-` or `.difference()`)

# Returns elements present in the first set but removed from the second set. *(Note: This operation is not commutative).*

python_devs = {"Alice", "Bob", "Charlie"}
java_devs = {"Bob", "David", "Eve"}

# Developers who know Python only (not Java)
only_python = python_devs - java_devs
print(only_python)  # Output: {'Alice', 'Charlie'}


### 4. Symmetric Difference (`^` or `.symmetric_difference()`)

# Returns elements that are in either of the sets, excluding those present in both.

python_devs = {"Alice", "Bob", "Charlie"}
java_devs = {"Bob", "David", "Eve"}

# Developers who know only one of the languages, not both
exclusive_devs = python_devs ^ java_devs
print(exclusive_devs)  # Output: {'Alice', 'Charlie', 'David', 'Eve'}

### 5. Subset and Superset Checks (`<=`, `>=`)

# Used to determine if a set is contained within another set.

team_lead = {"Alice", "Bob"}
all_devs = {"Alice", "Bob", "Charlie", "David"}

# Is team_lead a subset of all_devs?
print(team_lead.issubset(all_devs))  # Output: True

# Is all_devs a superset of team_lead?
print(all_devs.issuperset(team_lead))  # Output: True

### 6. Disjoint Check (`.isdisjoint()`)

# Returns `True` if two sets have a null intersection (i.e., no elements in common).

frontend = {"HTML", "CSS", "JavaScript"}
backend = {"Python", "SQL", "Java"}

# Check if they share any technology
print(frontend.isdisjoint(backend))  # Output: True


# **Tip:** Operators (`|`, `&`, `-`, `^`) require both operands to be sets, whereas methods (like `.union()`, `.intersection()`) accept any iterable (like lists or tuples) as an argument.

### 6. Other
# Convert a list to a set to remove duplicates:
s = set([1, 2, 2, 3])  # s = {1, 2, 3}

# Convert a set back to a list:
l = list(s)  # l = [1, 2, 3] (order may vary)

# Converting string into a set
s = set("absca") # s = {a, b, s, c}

# Use from collections import Counter to count frequencies
# Note: cannot use list with Counter, must use string or tuple or dict as not hashable. Use tuple([]) to convert list to tuple.
from collections import Counter

c1 = Counter("abbcb") # returns counter Counter({"a": 1, "b": 3, "c": 1}) i.e. iterator
c1.keys() # returns keys
c1.items() # returns items

# Add items to a set
s = {1, 2, 3}
s.add(4) # s = {1, 2, 3, 4}
s.remove(2) # s = {1, 3, 4}

# Add multiple items to a set
s.update([5, 6]) # s = {1, 2, 3, 4, 5, 6}

# =========================================================
# Matrix
# =========================================================
# Iterating Over Rows

grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

for row_idx, row in enumerate(grid):
  print(f"Row {row_idx}: {row}")

# Element-wise Iteration
for r in range(len(grid)):
  for c in range(len(grid[0])):
    print(f"Element at ({r}, {c}): {grid[r][c]}")

# Getting columns from grid
columns = []
n = len(grid)
for c in range(n):
    col = [grid[r][c] for r in range(n)]
    columns.append(col)

# Getting columns from grid using zip
columns = list(zip(*grid))  # Transpose the grid

# Extract rows and columns in n^3 time complexity
def has_matching_row_and_col(grid):
  # Get all columns by transposing the grid
  columns = list(zip(*grid))

  # Check every row against every column
  # row is n
  for row in grid:
    # col is n
    for col in columns:
      # Convert col (tuple) to list or compare directly
      # comparison is also n. compare n items in row and col
      # hence n^3
      if row == list(col):  # or tuple(row) == col
        return True

  return False

# Extract rows and columns in n^2 time complexity
from collections import Counter


def count_equal_row_col_pairs(grid):
  # Count occurrences of each row (must convert lists to tuples to be hashable)
  # This is n^2
  row_counts = Counter(tuple(row) for row in grid) # looks like Counter({(1, 2, 3): 2, (1, 4, 5): 1})

  # Get columns by transposing
  # This is n^2
  columns = zip(*grid)

  # Count how many columns exist in our row counts dictionary
  # This is n^2
  total_matches = 0
  for col in columns:
    # Looks up the column tuple in the row counts. 
    # Counter will automaticaly return 0 if the column is not found in the row counts.
    total_matches += row_counts[col]  

  return total_matches

# =========================================================
# Queues
# =========================================================


# =========================================================
# Heap & Priority Queue (heapq)
# =========================================================
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

# =========================================================
# Stack
# =========================================================
# Basic Stack Using List

# Initialize a stack
stack = []

# 1. Push items onto the stack
stack.append(10)
stack.append(20)
stack.append(30)
print("Stack after pushes:", stack)  # Output: [10, 20, 30]

# 2. Peek at the top item
print("Top item (Peek):", stack[-1])  # Output: 30

# 3. Pop an item from the stack
removed_item = stack.pop()
print("Popped item:", removed_item)     # Output: 30
print("Stack after pop:", stack)      # Output: [10, 20]

# 4. Check if empty
if not stack:
    print("Stack is empty")
else:
    print("Stack is not empty")

# 5. Get the size
print("Stack size:", len(stack))        # Output: 2

# Basic Stack Using Deque (from collections)
from collections import deque

# Initialize a deque as a stack
stack = deque()

# Push items
stack.append('a')
stack.append('b')
stack.append('c')

# Peek
print("Top:", stack[-1])  # Output: c

# Pop items
print("Popped:", stack.pop())  # Output: c
print("Remaining stack:", list(stack))  # Output: ['a', 'b']

# Monotonic Stack:
"""
A monotonic stack is a stack whose elements are kept in a specific order—either strictly increasing or strictly decreasing. 
As you iterate through a dataset, you pop elements from the stack that violate this order before pushing the new element.
Monotonically Increasing Stack: Elements from bottom to top are in increasing order (smallest to largest). 
Used to find the next smaller element.
Monotonically Decreasing Stack: Elements from bottom to top are in decreasing order (largest to smallest). 
Used to find the next greater element.

Time and Space Complexity: O(n) for both, where n is the number of elements in the input list. 
Each element is pushed and popped at most once.
"""

# Monotonically Decreasing Stack (next greater element)
def next_greater_element(nums):
    """
    Finds the next greater element for each number in the array.
    For each element, it looks to its right for the first element that is strictly greater.
    If no such element exists, it defaults to -1.
    """
    n = len(nums)
    
    # Initialize the result array with -1. 
    # Any element that doesn't find a larger element to its right will remain -1.
    result = [-1] * n
    
    # Initialize an empty stack. 
    # We store indices rather than values so we can easily update the result array.
    stack = []  

    # Iterate through every element in the array by its index
    for i in range(n):
        # Maintain a monotonically decreasing stack (from bottom to top).
        # While the stack is not empty AND the current element (nums[i]) 
        # is STRICTLY GREATER THAN the element at the index sitting at the top of the stack:
        while stack and nums[i] > nums[stack[-1]]:
            # Pop the index from the stack because we have found its next greater element
            idx = stack.pop()
            
            # The current element (nums[i]) is the first greater element 
            # for the element located at 'idx'
            # result contains the actual number i.e. the next greater element for the number at index 'idx'
            result[idx] = nums[i]  
        
        # Push the current index onto the stack. 
        # It will wait here until a greater element to its right is encountered.
        stack.append(i)

    return result

# Example usage:
# nums = [2, 1, 2, 4, 3]
# print(next_greater_element(nums))  # Output: [4, 2, 4, -1, -1]

# Monotonically Increasing Stack (next smaller element)
def next_smaller_element(nums):
    """
    Finds the next smaller element for each number in the array.
    For each element, it looks to its right for the first element that is strictly smaller.
    If no such element exists, it defaults to -1.
    """
    n = len(nums)
    # Initialize the result array with -1. 
    # Any element that doesn't find a smaller element to its right will remain -1.
    result = [-1] * n
    
    # Initialize an empty stack. 
    # We store indices rather than values so we can easily update the result array.
    stack = []  

    # Iterate through every element in the array by its index
    for i in range(n):
        # Maintain a monotonically increasing stack.
        # While the stack is not empty AND the current element (nums[i]) 
        # is STRICTLY LESS THAN the element at the index sitting at the top of the stack:
        while stack and nums[i] < nums[stack[-1]]:
            # Pop the index from the stack because we have found its next smaller element
            idx = stack.pop()
            
            # The current element (nums[i]) is the first smaller element 
            # for the element located at 'idx'
            result[idx] = nums[i]  
        
        # Push the current index onto the stack. 
        # It will wait here until a smaller element to its right is encountered.
        stack.append(i)

    return result

# Example usage:
# nums = [4, 8, 5, 2, 25]
# print(next_smaller_element(nums))  # Output: [2, 5, 2, -1, -1]

# =========================================================
# Linked List
# =========================================================
"""
A linked list is a linear data structure where elements (nodes) are stored in
non-contiguous memory locations. Each node contains two parts:
1. Data: The value stored in the node.
2. Next: A reference (or pointer) to the next node in the sequence.
"""
# Find the middle of the linked list using slow and fast pointers
slow = head
fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

# Traverse to the end of the linked list
while head and head.next:
    head = head.next

# Reverse a linked list
def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        current = head

        while current:
            nxt = current.next      # 1. Save the next node
            current.next = prev     # 2. Reverse the current node's pointer
            prev = current          # 3. Move prev forward (fixed order)
            current = nxt           # 4. Move current forward
        
        return prev                 # Return the new head of the reversed list

# Iterate through both halves simultaneously and find max twin sum
max_sum = 0
first_half = head
second_half = prev  # 'prev' is the new head of the reversed second half

while second_half:
    current_sum = first_half.val + second_half.val
    max_sum = max(max_sum, current_sum)
    
    first_half = first_half.next
    second_half = second_half.next

# --- Summary of Time Complexities (Singly Linked List) ---
# Traversal:                O(N)
# Insertion (Beginning):    O(1)
# Insertion (End):          O(N)
# Deletion (Value):         O(N)
# Search:                   O(N)

# =========================================================
# Trees - DFS (Depth-First Search)
# =========================================================
"""
Depth-First Search (DFS) is a graph and tree traversal algorithm that explores as deep as possible along each branch before backtracking.
In a binary tree, a DFS traversal visits a node, dives into its left subtree until it hits a leaf (or null), backtracks, 
and then dives into its right subtree. Depending on the problem, you can process nodes in different orders (Pre-order, In-order, Post-order)

        4
       / \
      2   5
     / \   
    1   3
"""

# Recursive DFS - In-Order (Left -> Root -> Right)
# Order of visiting: Go all the way to the leftmost leaf first, process it, process its parent, then visit its right child.
# Output: [1, 2, 3, 4, 5]
def inorder_recursive(root):
    if not root:
        return
    
    inorder_recursive(root.left)   # 1. Traverse left
    print(root.val)                # 2. Process root
    inorder_recursive(root.right)  # 3. Traverse right


# Recursive DFS - Pre-Order (Root -> Left -> Right)
# Order of visiting: Process the current node first, then go down the left branch completely, then the right branch.
# Output: [4, 2, 1, 3, 5]
def preorder_recursive(root):
    if not root:
        return
    
    print(root.val)                # 1. Process root
    preorder_recursive(root.left)  # 2. Traverse left
    preorder_recursive(root.right) # 3. Traverse right

# Recursive DFS - Post-Order (Left -> Right -> Root)
# Order of visiting: Process both children completely before touching their parent node. The root is always printed last.
# Output: [1, 3, 2, 5, 4]
def postorder_recursive(root):
    if not root:
        return
    
    postorder_recursive(root.left)  # 1. Traverse left
    postorder_recursive(root.right) # 2. Traverse right
    print(root.val)                 # 3. Process root

# Iterative DFS using Stack - In-Order
def inorder_iterative(root):
    stack = []
    current = root

    while stack or current:
        # Reach the leftmost node of the current node
        while current:
            stack.append(current)
            current = current.left
        
        # Current must be None at this point, so we pop from the stack
        current = stack.pop()
        print(current.val)  # Process the node
        
        # Now, we need to visit the right subtree
        current = current.right

# Iterative DFS using Stack - Pre-Order
def preorder_iterative(root):
    if not root:
        return
    
    stack = [root]

    while stack:
        current = stack.pop()
        print(current.val)  # Process the node
        
        # Push right child first so that left is processed first
        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)

# Iterative DFS using Stack - Post-Order
def postorder_iterative(root):
    if not root:
        return []
        
    stack = [root]
    output = []
    
    while stack:
        node = stack.pop()
        output.append(node.val)
        
        # Push left first, then right. 
        # (Since stack is LIFO, right gets processed/popped next)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
            
    # Reverse the output to get Left -> Right -> Root
    return output[::-1]

# DFS with prefix sum and backtracking
def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # Dictionary to store the count of prefix sums encountered so far
        prefix_sums = {0: 1}
        
        def dfs(node, current_sum):
            if not node:
                return 0
            
            current_sum += node.val
            # Find if there is a prefix sum we can subtract to get targetSum
            count = prefix_sums.get(current_sum - targetSum, 0)
            
            # Add current sum to the prefix map
            prefix_sums[current_sum] = prefix_sums.get(current_sum, 0) + 1
            
            # Recurse left and right
            count += dfs(node.left, current_sum)
            count += dfs(node.right, current_sum)
            
            # Backtrack: remove current sum from map so it doesn't affect other branches
            prefix_sums[current_sum] -= 1
            
            return count
            
        return dfs(root, 0)

# =========================================================
# Trees - BFS
# =========================================================
"""
Breadth-First Search (BFS) on a tree is an algorithm used to traverse or search tree structures level by level, 
starting from the root node and exploring all neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.

        1
       / \
      2   3
     / \   \
    4   5   6

BFS Traversal Order: 1 -> 2 -> 3 -> 4 -> 5 -> 6

1. Initialize a Queue: Place the root node into a queue (FIFO: First-In, First-Out).
2. Loop Until Empty: While the queue is not empty:
    Dequeue the front node from the queue and visit/process it.
    Enqueue all of its direct children (left to right, or right to left) into the queue.
3. Repeat: Continue the process until the queue is completely empty.
"""

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bfs_tree(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        # Pop the node from the front of the queue
        current_node = queue.popleft()
        result.append(current_node.val)
        
        # Add left child to the queue if it exists
        if current_node.left:
            queue.append(current_node.left)
            
        # Add right child to the queue if it exists
        if current_node.right:
            queue.append(current_node.right)
            
    return result

# Level-Order Traversal (Grouping by Levels)
"""
Often in tree problems, you need to keep track of individual levels 
(for example, to return a 2D array where each sub-list represents a tree level). 
You can achieve this by recording the size of the queue at the start of each iteration:
"""

def level_order_traversal(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        result.append(current_level)
        
    return result

# =========================================================
#BST
# =========================================================
"""
A Binary Search Tree (BST) is a node-based binary tree data structure that satisfies the following property for every node:
    The left subtree of a node contains only nodes with keys less than the node's key.
    The right subtree of a node contains only nodes with keys greater than the node's key.
    Both the left and right subtrees must also be binary search trees.

Time Complexity:Average Case: O(log n) for search, insertion, 
and deletion (when the tree is balanced).Worst Case: O(n) (when the tree becomes skewed, resembling a linked list).

In-Order Traversal: Visiting nodes in the order: Left $\rightarrow$ Root $\rightarrow$ Right. For a BST, 
this always yields elements in sorted ascending order.
"""
def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        
        def dfs(current):
            # Base case: if node is None or we found the value, return the node
            if not current or current.val == val:
                return current
            
            # Use BST properties to choose left or right, and make sure to RETURN the result
            if val < current.val:
                return dfs(current.left)
            else:
                return dfs(current.right)
        
        # Call the nested function starting from the root
        return dfs(root)

"""
Base Case: If the root is None, return None (target not found).
Search Phase:
    If the target key is smaller than root.val, look in the left subtree: root.left = deleteNode(root.left, key).
    If the target key is larger than root.val, look in the right subtree: root.right = deleteNode(root.right, key).
Deletion Phase (Target Found):
    Case 1 & 2 (Zero or One Child): If root.left is None, return root.right. If root.right is None, return root.left.
    Case 3 (Two Children):
        Find the minimum node in the right subtree (curr = root.right, loop while curr.left is not None).
        Copy its value to root.val.
        Recursively delete that minimum node from the right subtree: root.right = deleteNode(root.right, root.val).
Return: Return the updated root node.

"""
class Solution:
    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        if not root:
            return None
        
        # 1. Traverse to find the node
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            # Node with 0 or 1 child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            # Node with 2 children: Get the inorder successor (min in right subtree)
            curr = root.right
            while curr.left:
                curr = curr.left
            
            # Replace value with inorder successor's value
            root.val = curr.val
            
            # Delete the inorder successor from the right subtree
            root.right = self.deleteNode(root.right, curr.val)
            
        return root

# =========================================================
#Trie
# =========================================================
"""
Every node represents a single character of a word, and paths down the tree trace out prefixes and complete words.
Root Node: The starting point of the Trie, which represents an empty string ("") and contains no character.
Child Nodes: Each node contains a collection of pointers or references to its children, typically mapped by character (e.g., using a dictionary/hash map or a fixed-size array).
End-of-Word Marker: A boolean flag (often called is_end_of_word) stored in each node to signify whether the path from the root up to that node represents a complete, valid word inserted into the Trie.
Prefix Sharing: Words sharing a common prefix (e.g., "cat", "cats", "cattle") share the same nodes for that prefix, significantly reducing memory overhead and speeding up prefix-based searches.

After inserting cat and car, the Trie would look like this:
Root ("")
 └── 'c'
      └── 'a'
           ├── 't' (is_end_of_word = True)
           └── 'r' (is_end_of_word = True)
"""
class TrieNode:
    """Represents a single node in the Trie data structure."""

    def __init__(self):
        # A dictionary mapping a character (str) to its corresponding child TrieNode.
        # This acts as the branching mechanism of the tree, allowing dynamic
        # child allocation for any character set (alphabetic, numeric, unicode, etc.).
        self.children = {}

        # A boolean flag that indicates whether the path from the root node
        # down to this specific node forms a complete, valid word.
        # This is crucial because a node might just represent a prefix
        # (e.g., 'app' inside 'apple') rather than a finalized, inserted word.
        self.is_end_of_word = False


class Trie:
    """Represents the Prefix Tree (Trie) managing the collection of words."""

    def __init__(self):
        # Every Trie starts with a blank root node.
        # The root node does not store any character and serves purely
        # as the entry point for all subsequent tree traversals.
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the trie character by character."""
        # Start the traversal pointer at the root node.
        current = self.root

        # Iterate through each character in the target word sequentially.
        for char in word:
            # Check if the current character already exists as a branch/child
            # of the current node.
            if char not in current.children:
                # If it doesn't exist, instantiate a new TrieNode and link it
                # to the current node's dictionary under the character key.
                current.children[char] = TrieNode()

            # Move the pointer down to the child node corresponding to the current character.
            current = current.children[char]

        # After looping through all characters, the pointer rests on the final node
        # representing the last character of the word. Set its flag to True
        # to formally signify that this path forms a complete word.
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns true if the exact word is present in the trie."""
        # Begin traversal from the root node.
        current = self.root

        # Traverse character by character following the path of the word.
        for char in word:
            # If any character along the path is missing from the children dictionary,
                # it means the word was never inserted into the Trie.
            if char not in current.children:
                return False

            # Step down to the next node.
            current = current.children[char]

        # Once the loop finishes, we have successfully found all characters.
        # However, to confirm it is an *exact* word (and not just a prefix of a longer word),
        # we must return the boolean value of `is_end_of_word` at this final node.
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns true if there is any previously inserted word that begins with the given prefix."""
        # Begin traversal from the root node.
        current = self.root

        # Traverse character by character along the prefix string.
        for char in prefix:
            # If any character in the prefix is missing, no word in the Trie
            # can possibly start with this sequence.
            if char not in current.children:
                return False

            # Step down to the child node.
            current = current.children[char]

        # If we successfully trace every character of the prefix without interruption,
        # it means at least one word in the Trie shares this prefix path.
        # Unlike `search`, we don't care if `is_end_of_word` is True or False here.
        return True

class TrieNode:

  def __init__(self):
    # Maps a character (e.g., 'a', 'b') to its corresponding child TrieNode.
    self.children = {}

    # Caches up to 3 lexicographically sorted product suggestions
    # that pass through or terminate at this specific node (prefix).
    self.suggestions = []

# V1
class Solution:

  def suggestedProducts(
      self, products: List[str], searchWord: str
  ) -> List[List[str]]:
    # Step 1: Sort products lexicographically.
    # Why? Since we insert them into the Trie in sorted order, any node
    # will naturally see words in alphabetical order. This ensures that
    # the first 3 words appended to `node.suggestions` are guaranteed
    # to be the top 3 lexicographically smallest ones.
    products.sort()
    root = TrieNode()

    # Step 2: Build the Trie and pre-compute suggestions
    for product in products:
      node = root
      for char in product:
        # If the character path doesn't exist yet, create a new TrieNode.
        if char not in node.children:
          node.children[char] = TrieNode()

        # Move down to the child node representing the current character.
        node = node.children[char]

        # Because `products` was sorted initially, words are processed in
        # alphabetical order. Therefore, the first 3 unique products we push
        # into this node's suggestion list will always be the correct top 3.
        # Once we have 3, we skip appending more to save time and space.
        if len(node.suggestions) < 3:
          node.suggestions.append(product)

    # Step 3: Search phase (processing the searchWord character by character)
    res = []
    node = root
    found = True  # Tracks whether the current prefix exists in the Trie

    for char in searchWord:
      # If a path for the prefix still exists and hasn't broken off yet:
      if found and char in node.children:
        # Step down to the next node in the Trie
        node = node.children[char]
        # Append the pre-calculated suggestions stored directly at this node
        res.append(node.suggestions)
      else:
        # Once a character breaks the prefix path, all subsequent
        # character lookups will fail. Mark `found` as False and return [].
        found = False
        res.append([])

    return res

# V2
class Solution:

  def suggestedProducts(
      self, products: List[str], searchWord: str
  ) -> List[List[str]]:
    
    # -------------------------------------------------------------------------
    # Step 1: Build the Standard Trie
    # -------------------------------------------------------------------------
    root = TrieNode()
    for product in products:
      node = root
      for char in product:
        # If the character path doesn't exist yet, create a new TrieNode.
        if char not in node.children:
          node.children[char] = TrieNode()
        # Move down to the child node representing the current character.
        node = node.children[char]
      # Mark the final node of this product as the end of a valid word.
      node.is_word = True

    # -------------------------------------------------------------------------
    # Step 2: Define the DFS Helper Function for Dynamic Traversal
    # -------------------------------------------------------------------------
    def dfs(node, path, results):
      # Optimization: Stop searching immediately once we have found 3 suggestions.
      if len(results) == 3:
        return
      
      # If the current node marks the end of a complete product, add it to results.
      if node.is_word:
        results.append(path)

      # Traverse children in alphabetical order. 
      # Why `sorted(node.children.keys())`? 
      # Because a Trie's children are stored in an unordered hash map (`{}`), 
      # sorting the keys ensures our DFS explores branches lexicographically 
      # (e.g., 'a' before 'b'), guaranteeing our results are sorted alphabetically.
      for char in sorted(node.children.keys()):
        if len(results) == 3:
          break
        dfs(node.children[char], path + char, results)

    # -------------------------------------------------------------------------
    # Step 3: Search Phase (Processing searchWord Character by Character)
    # -------------------------------------------------------------------------
    res = []
    node = root
    prefix = ""
    found = True  # Tracks whether the current prefix path exists in the Trie

    for char in searchWord:
      prefix += char
      
      # If the prefix path is still valid and the character exists in the Trie:
      if found and char in node.children:
        # Step down to the child node representing this character
        node = node.children[char]
        
        suggestions = []
        # Run DFS starting from this node to discover up to 3 valid words
        dfs(node, prefix, suggestions)
        res.append(suggestions)
      else:
        # Once a character breaks the prefix path, no matching products exist.
        # Mark `found` as False and append an empty list for all subsequent characters.
        found = False
        res.append([])

    return res

# =========================================================
#Graph DFS
# =========================================================
"""
Depth-First Search (DFS) is a fundamental graph traversal algorithm that explores as deep as possible along each branch before backtracking. 
- LIFO (Last-In, First-Out): DFS relies on a stack data structure, prioritizing the most recently discovered vertex to dive deeper into the graph.
- Backtracking: When the algorithm hits a dead end or a node with no unvisited neighbors, it steps back to the previous node to explore alternative branches.
- Node States & Tracking
Visited Tracking: A boolean array or hash set tracks visited vertices to prevent infinite loops in cyclic graphs.
Three-State Coloring: Advanced implementations use color markings—White (unvisited), Gray (currently being explored in the recursion stack), and Black (fully explored).
- Core Operations
Initialization: Select a starting vertex, mark it as visited, and push it onto the stack (or enter the recursive call).
Recursive Exploration: Look at an unvisited adjacent neighbor of the current node, mark it, and immediately shift focus to it.
Backtracking Step: When a vertex has no remaining unvisited neighbors, the algorithm pops it or returns from the recursive function to resume exploration from the parent node.
"""
# Recursive DFS Implementation
def dfs_recursive(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    
    # 1. Initialization/Visit operation
    visited.add(vertex)
    print(f"Visited: {vertex}")
    
    # 2. Recursive exploration of neighbors
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            # Backtracking happens automatically when the recursive call returns
            dfs_recursive(graph, neighbor, visited)
            
    return visited

# Example graph represented as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# Run DFS starting from 'A'
dfs_recursive(graph, 'A')

#-----------------------------------------------------
# Iterative DFS using an explicit stack
def dfs_iterative(graph, start_vertex):
    visited = set()
    stack = [start_vertex]  # Explicit stack initialization
    
    while stack:
        # 1. Pop operation (LIFO)
        vertex = stack.pop()
        
        if vertex not in visited:
            # 2. Visit operation
            visited.add(vertex)
            print(f"Visited: {vertex}")
            
            # 3. Push unvisited neighbors onto the stack
            # Reversed is often used to match the left-to-right order of recursive DFS
            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return visited

# Run iterative DFS starting from 'A'
dfs_iterative(graph, 'A')

#-----------------------------------------------------
# Connected Components in an Undirected Graph using DFS
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        # Get the total number of cities (n) from the size of the adjacency matrix.
        n = len(isConnected)
        
        # Initialize a boolean tracking list of size n, all set to False.
        # This keeps track of whether we have already explored a given city.
        visited = [False] * n
        
        # Initialize our counter to store the total number of independent provinces found.
        provinces = 0
        
        # Iterate through every city from 0 to n - 1 to find unvisited components.
        for i in range(n):
            # If the current city has not been visited yet, it belongs to a new province.
            if not visited[i]:
                # Increment our province count since we found a new starting node.
                provinces += 1
                
                # Launch the helper DFS method. 
                # Notice we must use 'self.dfs' and explicitly pass down the 
                # state variables because this method is no longer nested.
                self.dfs(i, isConnected, visited)
                
        # After checking all cities, return the total count of provinces.
        return provinces

    def dfs(self, city: int, isConnected: List[List[int]], visited: list[bool]):
        # Mark the current city as visited so we don't process it multiple times.
        visited[city] = True
        
        # Loop through all possible neighboring cities from 0 to n - 1.
        for neighbor in range(len(isConnected)):
            # Check two conditions:
            # 1. isConnected[city][neighbor] == 1: Is there a direct road/connection?
            # 2. not visited[neighbor]: Have we NOT visited this neighbor yet?
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                # Recursively call self.dfs to explore further down this path,
                # passing along the exact same state references.
                self.dfs(neighbor, isConnected, visited)

#-----------------------------------------------------
# Reversing directions of edges in a tree to ensure all paths lead to the root (city 0).
import collections
from typing import List

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        """
        Main function that initializes the graph and triggers the recursive DFS.
        """
        # Step 1: Build the adjacency list to represent the tree as an undirected graph.
        # We store tuples of (neighbor, cost) for each edge.
        graph = collections.defaultdict(list)
        for u, v in connections:
            # If we travel from u to v, we are moving AWAY from city 0. 
            # This requires a reversal if we want paths to lead to 0, so cost = 1.
            graph[u].append((v, 1))
            
            # If we travel from v to u, we are moving TOWARD city 0. 
            # This is already in the correct direction, so cost = 0.
            graph[v].append((u, 0))
            
        # Step 2: Keep track of visited nodes to prevent infinite loops (since it's a cyclic graph representation)
        visited = set()
        
        # Step 3: Start the recursive DFS traversal from the capital city (city 0).
        # We pass the graph, the starting node, and the visited set into our helper method.
        return self._dfs(0, graph, visited)

    def _dfs(self, node: int, graph: dict, visited: set) -> int:
        """
        Recursive helper method that explores the graph, counts necessary road reversals,
        and returns the total count for the current subtree.
        """
        # Mark the current node as visited so we don't traverse back to it.
        visited.add(node)
        
        # Initialize the reversal count for this branch of the recursion.
        reversals = 0
        
        # Iterate through all adjacent nodes (neighbors) and the cost associated with moving to them.
        for neighbor, cost in graph[node]:
            # If the neighbor has not been visited yet, it means we are moving outward from city 0.
            if neighbor not in visited:
                # Add the cost of this specific edge (1 if it needs flipping, 0 if it's already correct).
                reversals += cost
                
                # Recursively call DFS on the neighbor and add its subtree's reversals to our total.
                reversals += self._dfs(neighbor, graph, visited)
                
        # Return the accumulated reversals for this node and its entire subtree.
        return reversals

# =========================================================
#Graph BFS
# =========================================================
"""
Key Concepts of BFSBreadth-First Search (BFS) is a graph traversal algorithm that explores a graph level by level, visiting all neighbor nodes at the current depth before moving on to the nodes at the next depth level.
Queue (FIFO): The core data structure that manages traversal order using a First-In, First-Out approach, ensuring nodes are processed in the exact order they are discovered.
Visited Tracking: A hash set used to keep track of nodes already visited, which prevents infinite loops in graphs with cycles.
Time & Space Complexity: Operates in $O(V + E)$ time and $O(V)$ space (where $V$ is vertices and $E$ is edges), as every vertex and edge is visited and stored in memory.
Algorithm Operations
1. Initialization: Add the starting node to a queue and mark it as visited.
2. Removal: Dequeue the front node from the queue to make it the current active node.
3. Neighbor Exploration: Check all adjacent neighbors of the current node.
4. Queue Insertion: For each neighbor not yet visited, mark it as visited and enqueue it.
5. Iteration: Repeat steps 2 through 4 until the queue becomes empty.
"""

from collections import deque

def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    traversal_order = []
    
    while queue:
        current = queue.popleft()
        traversal_order.append(current)
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return traversal_order

# Example usage with an adjacency list:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("BFS Traversal:", bfs(graph, 'A')) # Output: BFS Traversal: ['A', 'B', 'C', 'D', 'E', 'F']

# Shortest Path in Unweighted Graph using BFS
from collections import deque

def bfs_shortest_path(graph, start, target):
    # Base case: If the starting node is already the target node,
    # we don't need to search; return a list containing just the start node.
    if start == target:
        return [start]
        
    # A set to keep track of nodes we have already visited.
    # This prevents infinite loops in cyclic graphs and redundant work.
    visited = {start}
    
    # A FIFO (First-In, First-Out) queue for level-order traversal,
    # initialized with our starting node.
    queue = deque([start])
    
    # A dictionary to act as our "breadcrumb trail" (parent pointers).
    # It maps each node to the node that discovered it, allowing us to 
    # reconstruct the path later. The start node has no parent (None).
    parent = {start: None}  
    
    # Continue exploring as long as there are nodes left in the queue.
    while queue:
        # Remove and retrieve the node at the front of the queue.
        # This becomes our current active node for this iteration.
        current = queue.popleft()
        
        # Check if we have reached our destination. Because BFS explores 
        # level by level, the first time we pop the target, we are guaranteed 
        # to have found the shortest path.
        if current == target:
            path = []
            
            # Trace backward from the target to the start using the parent dictionary.
            while current is not None:
                path.append(current)          # Add the current node to our path list
                current = parent[current]     # Move back to the node's parent
                
            # Since we traced backward (Target -> ... -> Start), 
            # we reverse the list using slicing ([::-1]) to get Start -> ... -> Target.
            return path[::-1]  
            
        # Iterate through all adjacent neighbors of the current node.
        for neighbor in graph[current]:
            # If we haven't visited this neighbor yet, process it.
            if neighbor not in visited:
                visited.add(neighbor)             # Mark it as visited immediately
                parent[neighbor] = current        # Record that 'current' discovered this neighbor
                queue.append(neighbor)            # Add it to the queue to explore its neighbors later
                
    # If the queue becomes empty and we never hit the target, 
    # it means no path exists between the start and target nodes.
    return None  

# Example graph represented as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Find the shortest path from node 'A' to node 'F'
path = bfs_shortest_path(graph, 'A', 'F')
print("Shortest Path:", path) # Output: Shortest Path: ['A', 'C', 'F']

# Maze Solving
from collections import deque

class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        # Get the dimensions of the maze: m rows and n columns
        m, n = len(maze), len(maze[0])
        
        # Initialize a queue for BFS containing tuples of: (row, col, current_steps)
        # We start at the entrance coordinates with 0 steps taken.
        queue = deque([(entrance[0], entrance[1], 0)])
        
        # Mark the entrance as visited by changing it to a wall ('+').
        # This prevents the BFS from accidentally looping back to the entrance later.
        maze[entrance[0]][entrance[1]] = '+'
        
        # Define the 4 possible movement directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Standard BFS loop: process nodes level by level (layer by layer)
        while queue:
            # Pop the front element from the queue
            row, col, steps = queue.popleft()
            
            # Explore all 4 neighboring directions from the current cell
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check 1: Ensure the neighbor is within the boundaries of the maze.
                # Check 2: Ensure the neighbor is an open cell ('.'), not a wall ('+').
                if 0 <= new_row < m and 0 <= new_col < n and maze[new_row][new_col] == '.':
                    
                    # Check if this valid open cell is located on the outer border of the maze.
                    # Note: Because we started from the neighbors of the entrance, 
                    # an entrance sitting on the border will never trigger this for itself.
                    if new_row == 0 or new_row == m - 1 or new_col == 0 or new_col == n - 1:
                        # Since BFS guarantees the shortest path, the first border cell 
                        # we hit is guaranteed to be the nearest exit! Return total steps.
                        return steps + 1
                    
                    # Otherwise, it's a regular empty cell inside the maze:
                    # 1. Mark it as visited by turning it into a wall ('+') so we don't visit it again.
                    maze[new_row][new_col] = '+'
                    # 2. Add it to the queue with incremented step count to explore its neighbors next.
                    queue.append((new_row, new_col, steps + 1))
                    
        # If the queue becomes completely empty and we never hit a border exit,
        # it means no exit is reachable. Return -1.
        return -1
# =========================================================
#Graph Topological Sort
# =========================================================

# =========================================================
#Binary Search
# =========================================================
"""
Binary search is an efficient algorithm used to find the position of a target value within a sorted array or list. 
It works on the principle of Divide and Conquer.
Key Concepts
Prerequisite: The input list must be sorted (either ascending or descending).
Time Complexity: $O(\log n)$, making it exponentially faster than linear search ($O(n)$) for large datasets.Space Complexity: $O(1)$ for the iterative approach and $O(\log n)$ for the recursive approach (due to the call stack).
How it Works:
1. Find the middle element of the array (left + right) // 2.
2. Compare the target value with the middle element.
3. If the target matches the middle element, return its index.
4. If the target is less than the middle element, narrow the search to the left half.
5. If the target is greater than the middle element, narrow the search to the right half.
6. Repeat the process until the target is found or the sub-array size drops to zero.
"""
# Build in Python
import bisect

numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target_value = 23

# Find the insertion point to maintain sorted order
index = bisect.bisect_left(numbers, target_value)

# Verify if the element actually exists at that index
if index < len(numbers) and numbers[index] == target_value:
    print(f"Element found at index {index}")
else:
    print("Element not found")

import bisect

# Upper and lower bounds using bisect
def find_range_indices(arr, lower_bound, upper_bound):
    # 1. Find the first index where element >= lower_bound
    left_idx = bisect.bisect_left(arr, lower_bound)
    
    # 2. Find the first index strictly > upper_bound, then subtract 1 
    # to get the last element <= upper_bound
    right_idx = bisect.bisect_right(arr, upper_bound) - 1
    
    # Check if a valid range exists
    if left_idx <= right_idx and left_idx < len(arr) and right_idx >= 0:
        return left_idx, right_idx
        
    return None  # No elements found in this range

# Example usage:
numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

# Let's find elements between 10 and 50
result = find_range_indices(numbers, 10, 50)

if result:
    start, end = result
    print(f"Indices: {start} to {end}")
    print(f"Matching elements: {numbers[start:end + 1]}")
else:
    print("No elements found in this range")

# Manual Implementation of Binary Search
def binary_search_iterative(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        # Check if target is present at mid
        if arr[mid] == target:
            return mid

        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1

        # If target is smaller, ignore right half
        else:
            right = mid - 1

    return -1  # Target is not present in the array


# Example usage:
numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target_val = 23
result = binary_search_iterative(numbers, target_val)
print(f"Index of {target_val}: {result}")  # Output: Index of 23: 5

# Lower Bound Using Binary Search
def lower_bound(arr: list[int], target: int) -> int:
    left = 0
    right = len(arr)
    
    while left < right:
        mid = (left + right) // 2

        # for upper boud <=
        if arr[mid] < target:
            # mid is too small, discard it and everything to the left
            left = mid + 1
        else:
            # arr[mid] >= target, so it's a potential answer. 
            # Keep mid in bounds to check if there's a smaller valid index to the left.
            right = mid
            
    # 'left' points to the first element >= target.
    # It can equal len(arr) if all elements are smaller than target.
    return left

def findPeakElement(self, nums: list[int]) -> int:
    # Initialize two pointers: 
    # 'left' starts at the beginning of the array (index 0).
    # 'right' starts at the end of the array (index len(nums) - 1).
    # We are searching within the inclusive range [left, right].
    left, right = 0, len(nums) - 1
    
    # Continue searching as long as our search space has more than one element.
    # When left == right, we have narrowed down our search to a single index, 
    # which is guaranteed to be a peak.
    while left < right:
        
        # Find the middle index of the current search space.
        # Using integer division '//' prevents floating-point results.
        mid = (left + right) // 2
        
        # Check the slope by comparing the middle element with its immediate right neighbor.
        # Problem constraints guarantee that out-of-bounds indices aren't an issue 
        # because 'mid' will always be less than 'right' inside the loop, 
        # meaning 'mid + 1' is a valid index up to 'right'.
        if nums[mid] < nums[mid + 1]:
            # ---------------------------------------------------------
            # UPWARD SLOPE CASE:
            # ---------------------------------------------------------
            # If nums[mid] is smaller than nums[mid + 1], it means the values 
            # are climbing as we move right. 
            # 
            # Why does a peak always exist to the right?
            # Because the values are increasing, either:
            # 1. They will keep increasing all the way to the end of the array 
            #    (making the last element a peak, since problem treats out-of-bounds 
            #    as negative infinity).
            # 2. Or they will eventually go down, meaning a peak must exist 
            #    somewhere ahead.
            # 
            # Therefore, 'mid' itself cannot be a peak. We safely discard 'mid' 
            # and everything to its left by setting left to mid + 1.
            left = mid + 1
            
        else:
            # ---------------------------------------------------------
            # DOWNWARD SLOPE OR PEAK CASE:
            # ---------------------------------------------------------
            # If nums[mid] is greater than or equal to nums[mid + 1], it means 
            # the slope is going down as we move right (or we hit a flat spot/peak).
            # 
            # Why does a peak always exist to the left (including 'mid')?
            # Because the values are dropping or holding steady to the right, 
            # a peak must either be 'mid' itself or hidden somewhere to the left 
            # where the climb originated.
            # 
            # Therefore, we discard everything to the right of 'mid' by setting 
            # right to 'mid'. We keep 'mid' in the search space because it could 
            # potentially be the peak itself.
            right = mid
            
    # When the loop terminates, left and right have converged to the exact same index.
    # This index represents our peak element, so we return it.
    return left

# Answer Space Problem
def solve_answer_space_problem(constraints) -> int:
    # Step 1: Define search space
    # This is usually the min and max of the variable we are trying to find.
    left = min_possible_answer
    right = max_possible_answer
    res = -1
    
    # Step 2: Binary search loop
    while left <= right:
        mid = (left + right) // 2
        
        # Step 3: Check if 'mid' is valid
        if is_valid(mid, constraints):
            res = mid              # Save valid answer
            # Adjust pointers depending on Min vs Max:
            right = mid - 1        # (Use left = mid + 1 if looking for MAX)
        else:
            left = mid + 1         # (Use right = mid - 1 if looking for MAX)
            
    return res

# =========================================================
# DP 1D
# =========================================================
"""
Important: Instead of asking "Where can I go from here?", dynamic programming asks "How could I have possibly arrived here?"
When problem can be thought of decision tree. DP is a clever way to solve that tree without actually building it or recalculating duplicate branches.
Check:
- Can I break it into smaller subproblems?
- Do past choices restrict future choices?
- Are choices independent of how I got here?

Step 1: Define the State (dp[i])
Ask yourself: What does the subproblem represent? For 1D array problems, dp[i] usually means: "The optimal answer (max profit, min cost, total ways) considering elements from index 0 up to i."

Step 2: Find the Recurrence Relation (Transition)
Ask yourself: What choices do I have at the current element i?
Usually involves taking the maximum or minimum between:
    Skipping the current element (looking back at dp[i-1]).
    Taking the current element (combining it with dp[i-2] or an earlier state based on constraints).

Step 3: Establish the Base Cases (cases that cannot be split into smaller subproblems, are defined by transition i.e. how fast back we need to look)
Ask yourself: What are the smallest valid inputs where the answer is obvious?
Handle edge cases (empty array, single element).
Initialize dp[0] and often dp[1] manually before entering a loop.

Step 4: Determine the Final Answer & Optimize Space
The final answer is typically at the end of your DP array (e.g., dp[-1]).S
pace Optimization Trick: If dp[i] only depends on the previous 1 or 2 values (i-1, i-2), you can drop the array entirely and use variables to achieve $O(1)$ space.
"""

def solveSimilarProblem(self, nums: list[int]) -> int:
    # Step 2: Handle edge cases and base cases
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    # Step 1: Initialize DP array (or variables for space optimization)
    dp = [0] * len(nums)
    dp[0] = ... # base case 1 e.g. only one house to rob
    dp[1] = ... # base case 2 e.g. two houses, choose the max/min based on problem context
    
    # Step 3: Iterate and apply recurrence relation
    for i in range(2, len(nums)):
        dp[i] = max/min(
            dp[i - 1],              # Choice 1: Skip
            dp[i - 2] + nums[i]     # Choice 2: Take (with constraint)
        )
        
    # Step 4: Return final state
    return dp[-1]

def solveSpaceOptimized(self, nums: list[int]) -> int:
    # Step 1: Initialize variables to represent previous states
    # (The number of variables depends on how far back your recurrence relation looks)
    prev2 = 0  # Represents i - 2 (or older)
    prev1 = 0  # Represents i - 1 (the immediate predecessor)
    
    # Step 2: Iterate through the input data
    for item in nums:
        # Step 3: Compute the optimal choice for the current step
        # Replace this logic with your specific problem's rule (e.g., max, min, sum)
        current = max(prev1, prev2 + item) 
        
        # Step 4: Shift the history forward for the next iteration
        prev2 = prev1
        prev1 = current
        
    # Step 5: Return the final state variable
    return prev1
# =========================================================
# DP 2D
# =========================================================
"""
Can think of it as graph. DP optimized way of solving it.
Brute force: DFS with memoization. DP: Bottom up tabulation.
"""
# ----------------Grid Problems: 2D DP-----------------------
# See Leetcode 62. Unique Paths
def gridDPProblem(m: int, n: int) -> int:
    # Step 1 & 2: Initialize DP table with base cases
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1 # or whatever the starting base case is
    
    # Fill base case edges (if applicable)
    for r in range(1, m):
        dp[r][0] = ... 
    for c in range(1, n):
        dp[0][c] = ...

    # Step 3 & 4: Iterate starting after base cases and apply transition
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1] # Example transition
            
    return dp[m-1][n-1]


def spaceOptimizedGridDP(self, m: int, n: int) -> int:
    # Optimization: Notice that to compute any row, you only need the values from the current row and the previous row.
    # This drops your space complexity to $O(n)$ by keeping just a single 1D array of size $n$ and updating it iteratively
    # Step 1: Initialize a 1D DP array of size n (number of columns)
    # Set base cases for the first row/column depending on the problem
    dp = [1] * n  # Example: 1s for counting paths, or 0s for sums/mins
    
    # Step 2: Iterate through each row starting from the second row (index 1)
    for r in range(1, m):
        # Step 3: Iterate through each column starting from the second column (index 1)
        for c in range(1, n):
            # Step 4: Apply the transition rule using the in-place update trick
            # dp[c] currently holds the value from the ABOVE row.
            # dp[c - 1] holds the newly updated value from the LEFT cell.
            
            # Example for Unique Paths:
            dp[c] += dp[c - 1] 
            
            # (Alternative for Min Path Sum, you would do something like:
            # dp[c] = grid[r][c] + min(dp[c], dp[c - 1]))
            
    # Step 5: The final answer rests in the last element of the 1D array
    return dp[-1]

# ----------------Subsequence Problems: 2D DP (Leetcode 1143)-----------------------
# Longest Common Subsequence (LCS) Problem
def subsequenceProblem(self, text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    
    # 1. Initialize DP table with +1 offset for base cases (empty strings)
    # Size: (m + 1) x (n + 1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 2. (Optional) Initialize base cases if they aren't 0
    # e.g., for Edit Distance, dp[i][0] = i and dp[0][j] = j
    
    # 3. Fill the DP table using nested loops
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            # 4. Check if elements match
            if text1[i - 1] == text2[j - 1]:
                # Match case: typically take diagonal + 1 (or add current weight)
                dp[i][j] = dp[i - 1][j - 1] + 1  # (modify based on problem)
            else:
                # Mismatch/Choice case: typically take max or min of skipping elements
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # (or min for cost problems)
                
    # 5. Return the bottom-right cell containing the final answer
    return dp[m][n]


def spaceOptimizedSubsequence(self, text1: str, text2: str) -> int:
    # 1. Optimization: Ensure text1 is the shorter string 
    # This guarantees the inner array size (and space complexity) is min(m, n)
    if len(text1) > len(text2):
        text1, text2 = text2, text1
        
    m, n = len(text1), len(text2)
    
    # 2. Initialize two 1D arrays instead of a 2D matrix
    # prev represents row i-1, curr represents row i
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    # (Optional) Handle base cases for the first row if needed (e.g., Edit Distance)
    # for j in range(n + 1): prev[j] = j
    
    # 3. Outer loop iterates over the rows
    for i in range(1, m + 1):
        
        # (Optional) Handle base case for the start of the current row if needed
        # curr[0] = i 
        
        # Inner loop iterates over the columns
        for j in range(1, n + 1):
            
            # 4. Apply your transition logic
            if text1[i - 1] == text2[j - 1]:
                # Match case: depends on diagonal value (which was in prev[j-1])
                curr[j] = prev[j - 1] + 1  # (Modify for counting/cost if needed)
            else:
                # Mismatch case: depends on top (prev[j]) and left (curr[j-1])
                curr[j] = max(prev[j], curr[j - 1])  # (Use min for cost problems)
        
        # 5. Shift current row to previous row for the next iteration
        prev = curr[:]  # or prev, curr = curr, [0] * (n + 1)
        
    # 6. The final answer resides at the end of the last processed row
    return prev[n]
    
# Variations
"""
Counting Subsequences (e.g., "Distinct Subsequences")
    Goal: Find how many ways a subsequence can be formed.
    Modification: Instead of max or min, you accumulate (add) the paths. 
    When characters match, you have the choice to use the match or skip the character in the first string.
"""
# Inside the loop:
if text1[i - 1] == text2[j - 1]:
    # Add ways from using the match AND ways from skipping the current char in text1
    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
else:
    # If they don't match, we must skip the character in text1
    dp[i][j] = dp[i - 1][j]

"""
2. Minimum Cost / Operations (e.g., "Edit Distance" / "Minimum ASCII Delete Sum")
    Goal: Find the minimum operations or cost to transform one sequence into another.
    Modification: Change max to min, adjust base cases to account for deletion/insertion costs, and include all choice branches (Insert, Delete, Substitute).
"""

# Base case setup (outside loop):
for i in range(m + 1): dp[i][0] = i  # cost of deleting all chars
for j in range(n + 1): dp[0][j] = j  # cost of inserting all chars

# Inside the loop:
if text1[i - 1] == text2[j - 1]:
    dp[i][j] = dp[i - 1][j - 1]  # No cost if they match
else:
    dp[i][j] = 1 + min(
        dp[i - 1][j],     # Deletion
        dp[i][j - 1],     # Insertion
        dp[i - 1][j - 1]  # Substitution
    )

"""
3. Single Sequence Problems (e.g., "Longest Increasing Subsequence")
    Goal: Find patterns within a single array (no second string to compare against).
    Modification: Drop the 2D grid entirely. Use a 1D array where dp[i] represents the answer ending at index i, and loop backward through previous elements.
"""

# 1D Table initialization
dp = [1] * n  # Base case: every element is a subsequence of length 1

for i in range(1, n):
    for j in range(i):
        if text[i] > text[j]:  # Condition (e.g., increasing)
            dp[i] = max(dp[i], dp[j] + 1)
            
return max(dp)

"""
4. Interval / Palindrome Subsequences (e.g., "Longest Palindromic Subsequence")
    Goal: Find subsequences inside a string by shrinking or expanding an interval (i, j).
    Modification: Instead of prefixes, your loops manage interval lengths from start (i) to end (j).
"""

# dp[i][j] = longest palindromic subsequence between index i and j
dp = [[0] * n for _ in range(n)]
for i in range(n): dp[i][i] = 1  # Base case: single letters are palindromes of length 1

# Iterate by length of the interval
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if text[i] == text[j]:
            dp[i][j] = dp[i + 1][j - 1] + 2
        else:
            dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

return dp[0][n - 1]
# =========================================================
#OTHER
# =========================================================
# while-else loop

# else block only runs if the loop finishes naturally (meaning it finished without hitting a break).
while stack and ast < 0 < stack[-1]:
    ...
    if stack[-1] < -ast:
        stack.pop()
        continue 
    elif stack[-1] == -ast:
        stack.pop()
    break
else:
    stack.append(ast)

# Memoization with DFS
"""
Think of memoization as keeping a cheat sheet (usually a 2D array or a hash map).
    Check the cache: Before doing any work at cell (r, c), look at your cheat sheet to see if you've already calculated the answer for this cell. If you have, immediately return that saved value.
    Compute if missing: If it's not in the cheat sheet, run your normal DFS logic (explore down and right).
    Save to the cache: Before returning the final result for cell (r, c), save it to your cheat sheet so you never have to calculate it again.
"""
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Step 1: Create a memoization table (cheat sheet) initialized to -1
        memo = [[-1] * n for _ in range(m)]
        
        def dfs(r, c):
            # Base Case 1: Out of bounds
            if r == m or c == n:
                return 0
            
            # Base Case 2: Reached destination
            if r == m - 1 and c == n - 1:
                return 1
            
            # Step 2: Check if we've already solved this subproblem
            if memo[r][c] != -1:
                return memo[r][c]
            
            # Step 3: Compute the result normally (DFS branches)
            move_down = dfs(r + 1, c)
            move_right = dfs(r, c + 1)
            
            # Step 4: Save the result in the memo table before returning
            memo[r][c] = move_down + move_right
            return memo[r][c]

        return dfs(0, 0)

# Sort intervals by start time
sorted_intervals = sorted(intervals, key=lambda x: x[0])

data = {'a': 5, 'b': 1, 'c': 9}
sorted(data.items(), key= lambda x: x[1])
# Output: [('b', 1), ('a', 5), ('c', 9)]

# Delete from set
my_set = {1, 2, 3, 4, 5}
my_set.discard(3)  # Removes 3 if it exists; does nothing if it doesn't

# deque
# Important: left end is front of queue
# Unlike stack where right end is top

# Topological Sort using Kahn's Algorithm
from collections import deque
from typing import List


def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
  """Returns a valid topological sort order for a DAG.

  If a cycle exists, returns an empty list.
  """
  # STEP 1: Graph Representation Setup
  # Create an empty adjacency list for each course (0 to num_courses - 1).
  adj = {i: [] for i in range(num_courses)}
  # Track incoming edge counts (prerequisite count) for every course, initialized to 0.
  in_degree = [0] * num_courses

  # STEP 2: Building the Graph from Edge List
  # Each prerequisite pair is given as [course, prereq], meaning "prereq must be taken before course".
  for course, prereq in prerequisites:
    # Add a directed edge from prerequisite -> course in our adjacency list.
    adj[prereq].append(course)
    # Increment the in-degree count of the target course because it has one more dependency.
    in_degree[course] += 1

  # STEP 3: Seeding the Queue
  # Find all nodes that have an in-degree of 0 (no prerequisites/dependencies).
  # These are our starting points because they can be processed immediately.
  queue = deque([i for i in range(num_courses) if in_degree[i] == 0])

  # List to store the final topological order sequence.
  top_order = []

  # STEP 4: BFS Processing Loop
  while queue:
    # Pop the node from the front of the queue (it has 0 unresolved prerequisites).
    curr = queue.popleft()
    # Add it to our valid topological order.
    top_order.append(curr)

    # For every course that depends on 'curr' (its neighbors):
    for neighbor in adj[curr]:
      # Since 'curr' is now processed, we remove its dependency constraint.
      in_degree[neighbor] -= 1
      # If all prerequisites for this neighbor are now satisfied (in-degree hits 0):
      if in_degree[neighbor] == 0:
        # Push it to the queue so it can be processed next.
        queue.append(neighbor)

  # STEP 5: Cycle Detection & Validation
  # If the total number of nodes in our topological order equals the total number of courses,
  # it means we successfully processed every node (no cycles trapped any nodes).
  if len(top_order) == num_courses:
    return top_order

  # If length doesn't match, a cycle exists (deadlock where remaining nodes have in-degree > 0).
  return []