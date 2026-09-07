"""
Key Python operations: Lists.
Adding, removing, and different ways to iterate.
"""


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


