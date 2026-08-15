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
# Stack
# =========================================================