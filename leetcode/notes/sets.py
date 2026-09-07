"""
Key Python operations: Sets.
Union, intersection, difference, and other set operations.
"""


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


# Delete from set
my_set = {1, 2, 3, 4, 5}
my_set.discard(3)  # Removes 3 if it exists; does nothing if it doesn't
