Here is the comprehensive guide combining the core approaches, operational sequences, code snippets, and explanations for all **five two-pointer variations**.

---

## Key Variations

- Left / Right (Converging)
- Slow / Fast same start point
- Slow 7 Fast different speeds

## Quick decision checklist

| Question                                                                     | If yes ->                                           |
| ---------------------------------------------------------------------------- | --------------------------------------------------- |
| Sorted array + looking for pair/triplet by sum?                              | Opposite-direction pointers                         |
| Need to compact/filter array in place, no extra space?                       | Fast-slow, same start                               |
| Linked list, need O(1) space cycle/midpoint detection?                       | Fast-slow, different speeds                         |
| Contiguous subarray/substring, constraint monotonic as window grows/shrinks? | Sliding window                                      |
| None of the above but "two things converge/compare"?                         | Probably not two pointers -- check hashmap/DP first |

Usually time complexity is O(n) and space complexity O(1) for these.

## **1. Opposite Direction (Converging Pointers)**

### **Core Approach**

Place pointers at opposite ends of a collection (e.g., the start and end of a sorted array) and move them toward each other to systematically shrink the search space until they meet.

Pre-requisite:

- Array needs to be sorted or can be sorted
- Searching for pair/ triplet satisfying a sum or comparison

### **Sequence of Operations**

1. Initialize `left = 0` and `right = n - 1`.
2. Run a `while left < right` loop.
3. Evaluate the pair `(left, right)` against the target condition.
4. Move **one** pointer inward based on the evaluation (increment `left` if the value is too small; decrement `right` if it is too large).
5. Stop and return the result when the pointers meet or cross.

### Template

```python
left, right = 0, len(nums) -1
while left < right:
  s = nums[left] + nums[right]
  if s == target: ...
  if s < target: l += 1
  else: right -= 1

```

### **Code Snippet & Example** (_Two Sum II - LeetCode 167_)

```python
def twoSum(numbers: list[int], target: int) -> list[int]:
  left, right = 0, len(numbers) - 1
  while left < right:
    s = numbers[left] + numbers[right]
    if s == target:
      return [left + 1, right + 1]
    elif s < target:
      left += 1  # Sum is too small, move left pointer up
    else:
      right -= 1  # Sum is too large, move right pointer down
  return []

```

- **Explanation:** Because the array is sorted, if the sum of `left` and `right` is smaller than the target, we _must_ increase our sum, which means moving the `left` pointer to a larger number. If the sum is too large, we decrease it by moving the `right` pointer inward.

---

## **2. Same Direction (Fast & Slow Pointers)**

### **Core Approach**

Use two pointers starting at the same origin. The `fast` pointer scans ahead to explore or find elements, while the `slow` pointer trails behind to track positions for in-place modifications or filtering.
**Use when:** you need to **overwrite an array in place** to keep only elements matching some condition, without extra space, preserving order.

### **Sequence of Operations**

1. Initialize `slow = 0` and `fast = 0`.
2. Run a loop where `fast` iterates through the entire collection.
3. Evaluate the element at `fast` against a specific condition.
4. If the condition is met, process or swap the element into the `slow` index, then increment `slow`.
5. Always increment `fast` to keep scanning.

### Template

```python
slow = 0
for fast in range(len(nums)):
  if keep_condition(nums[fast]):
    nums[slow] = nums[fast]
    slow += 1
```

### **Code Snippet & Example** (_Move Zeroes - LeetCode 283_)

```python
def moveZeroes(nums: list[int]) -> None:
  slow = 0
  for fast in range(len(nums)):
    if nums[fast] != 0:
      # Swap non-zero element to the slow pointer position
      nums[slow], nums[fast] = nums[fast], nums[slow]
      slow += 1

```

- **Explanation:** `fast` looks for any non-zero element. When it finds one, it swaps it with whatever is sitting at the `slow` pointer. This pushes all zeros to the back of the array while keeping the relative order of non-zero elements intact.

---

## **3. Sliding Window (Dynamic Fast/Slow)**

### **Core Approach**

Maintain a dynamic window defined by a `left` and `right` pointer over a contiguous sequence. The `right` pointer expands the window to capture data, and the `left` pointer shrinks it the moment a constraint is violated.

**Use when:** contiguous subarray/substring problem with a constraint that's monotonic — i.e. if the window satisfies the constraint, shrinking it from the left still satisfies it (or the reverse). That monotonicity is the prerequisite; without it, sliding window gives wrong answers and you need prefix sums / DP instead.

**Signals:** "longest/shortest substring/subarray with property X," "at most K distinct," "minimum window containing."

### **Sequence of Operations**

1. Initialize `left = 0`, an optimal tracking variable, and a state tracker (like a hash map or set).
2. Loop `right` from `0` to `n - 1` to expand the right boundary.
3. Add the element at `right` to your tracker state.
4. Run a `while` loop checking if the window violates a constraint. If violated, increment `left` to shrink the window and update the state.
5. Record or update your optimal metric at each step.

### Template

```python
left = 0
for right in range(len(nums)):
  # expand window
  add(s[r])
  # shrink window unitl valid again
  while window_invalid():
    remove(s[l])
    l += 1
  # update answer
  update_answer(r - l + 1)
```

Sometimes the answer might require us to count elements / combinations in the window e.g. count += right - left + 1 in LC 713 to get
all possible subarrays in the window that are smaller than a target.
If we look for exact match then not needed

### **Code Snippet & Example** (_Longest Substring Without Repeating Characters - LeetCode 3_)

```python
def lengthOfLongestSubstring(s: str) -> int:
  char_set = set()
  left = 0
  max_len = 0

  for right in range(len(s)):
    # Shrink window from the left until duplicate is removed
    while s[right] in char_set:
      char_set.remove(s[left])
      left += 1
    char_set.add(s[right])
    max_len = max(max_len, right - left + 1)

  return max_len

```

- **Explanation:** As `right` expands the window, if we encounter a duplicate character already in our `char_set`, we shrink the window from the `left` side, removing elements until the duplicate is cleared out.

---

## 4. Fast-slow, different speeds (cycle detection)

**Use when:** linked list / functional graph, and you need to detect a cycle or find a midpoint **without extra memory** (the O(n) hashset approach is the "obvious" alternative, so this pattern is specifically the space-optimized answer).

**Signals:** "find duplicate number" (287 — treats array as implicit linked list via indices), "linked list cycle" (141/142 — Floyd's algorithm, then reset one pointer to head to find the cycle start), "find middle of linked list."

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast: break  # cycle found
```

---

# ToDo -> practice

## **5. Two-Array / Merge Pattern**

### **Core Approach**

Manage two separate collections simultaneously by placing an independent pointer at the start of each, stepping through them by comparing their current values.

### **Sequence of Operations**

1. Initialize pointer `i = 0` for the first array and pointer `j = 0` for the second array.
2. Run a loop that continues as long as **both** pointers are within their respective bounds.
3. Compare elements (`array1[i]` vs `array2[j]`).
4. Take action based on the comparison and increment **only** the pointer corresponding to the item processed.
5. Append any leftover elements from whichever collection still has remaining items.

### **Code Snippet & Example** (_Merge Sorted Array - LeetCode 88, merging backwards_)

```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
  p1, p2, p = m - 1, n - 1, m + n - 1
  while p1 >= 0 and p2 >= 0:
    if nums1[p1] > nums2[p2]:
      nums1[p] = nums1[p1]
      p1 -= 1
    else:
      nums1[p] = nums2[p2]
      p2 -= 1
    p -= 1
  # Copy leftover elements from nums2 if any remain
  nums1[: p2 + 1] = nums2[: p2 + 1]

```

- **Explanation:** By starting pointers at the _back_ of both arrays (`m - 1` and `n - 1`), we can compare the largest elements first and place them safely at the end of `nums1` without overwriting data we haven't processed yet.

---

# ToDo -> practice. leetcode 5

## **6. Expand Around Center**

### **Core Approach**

Instead of scanning from the edges, treat every element (and the spaces between elements) as a center point, then stretch pointers outward to find valid matching patterns.

### **Sequence of Operations**

1. Loop an index `i` from `0` to `n - 1` to act as your center anchor.
2. For each index, check two potential center configurations: **odd-length** (single element center) and **even-length** (two-element space center).
3. Run an inner loop while `left` and `right` are within bounds and their values match.
4. Inside the inner loop, expand outward (`left -= 1`, `right += 1`).
5. Track and update the maximum valid span found.

### **Code Snippet & Example** (_Longest Palindromic Substring - LeetCode 5_)

```python
def longestPalindrome(s: str) -> str:
  if not s:
    return ""
  start, end = 0, 0

  def expandAroundCenter(left: int, right: int) -> int:
    # string is valid palindrome if start and end match and start-i and end-i match
    while left >= 0 and right < len(s) and s[left] == s[right]:
      left -= 1
      right += 1
    return right - left - 1  # Returns the length of the palindrome

  # Two different cases: 1. odd length 2. even length
  for i in range(len(s)):
    len1 = expandAroundCenter(i, i)  # Odd length (e.g., "aba")
    len2 = expandAroundCenter(i, i + 1)  # Even length (e.g., "abba")
    max_len = max(len1, len2)

    if max_len > (end - start):
      start = i - (max_len - 1) // 2
      end = i + max_len // 2

  return s[start : end + 1]

```

- **Explanation:** For every index `i`, we test how far we can stretch outward to the left and right while characters match. This checks every possible palindrome center in $O(n^2)$ time without redundant checks.

---

# LC Questions:

# LC: 581

Core idea:
Instead of checking vevery possible subarray we check for violations in the order.
A sorted array naturally increases left from right.
We try to find the right and left most elements that are out of order.
We divided it into two subproblems.
The difference is the lenght of the subarray.
Time: O(n)
Space: O(1)

```python
def findUnsortedSubarray(self, nums: list[int]) -> int:
    n = len(nums)

    # Initialize pointers for the unsorted window boundaries.
    # If they remain -1 at the end, it means the array is already sorted.
    left, right = -1, -1

    # Track the maximum element seen so far from left to right.
    # Initialized to negative infinity so the first element is always larger.
    max_seen = -float('inf')

    # Track the minimum element seen so far from right to left.
    # Initialized to positive infinity so the last element is always smaller.
    min_seen = float('inf')

    # -------------------------------------------------------------
    # PASS 1: Find the RIGHT boundary of the unsorted subarray
    # -------------------------------------------------------------
    # As we move forward, numbers should strictly increase or stay equal.
    for i in range(n):
        if nums[i] < max_seen:
            # Violation found! This number is smaller than a previous max,
            # meaning it's out of order and forces the right boundary out.
            right = i
        else:
            # No violation; update our maximum tracked value.
            max_seen = nums[i]

    # -------------------------------------------------------------
    # PASS 2: Find the LEFT boundary of the unsorted subarray
    # -------------------------------------------------------------
    # As we move backward, numbers should strictly decrease or stay equal.
    for i in range(n - 1, -1, -1):
        if nums[i] > min_seen:
            # Violation found! This number is larger than a subsequent min,
            # meaning it's out of order and pulls the left boundary back.
            left = i
        else:
            # No violation; update our minimum tracked value.
            min_seen = nums[i]

    # -------------------------------------------------------------
    # RESULT CALCULATION
    # -------------------------------------------------------------
    # If the left pointer never moved, no violations were found anywhere.
    if left == -1:
        return 0

    # The length of the subarray between the left and right violations.
    return right - left + 1

# Alternatively
# We sort the array first the we compare the sorted array with the original one and find the most left and right elements that differ.
# Time: O(n log n), Space: O(n)
def findUnsortedSubarray(self, nums: list[int]) -> int:
    # Create a sorted copy of the array (equivalent to nums.clone() + Arrays.sort())
    snums = sorted(nums)

    # Initialize start to max possible index, end to 0
    start, end = len(nums), 0

    # Compare the original array with the sorted array element by element
    for i in range(len(nums)):
        if snums[i] != nums[i]:
            start = min(start, i)
            end = max(end, i)

    # If end - start >= 0, return the length of the window; otherwise, return 0
    return end - start + 1 if end - start >= 0 else 0
```

LC 15

```python
"""
sort list
fix one number
two pointer to find two numbers that sum up 0 - fixed
have left and right pointer
add up left and right
if > sum move right pointer
if < sum move left pointer

Time O(n^2)
Space O(n)
"""
def threeSum(self, nums: list[int]) -> list[list[int]]:
    triplets = []
    nums.sort()
    for i in range(len(nums)):
      # need to skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        # init left at i+1 as target is i
        left = i + 1
        right = len(nums) - 1
        target = -nums[i]

        while left < right:
            current_sum = nums[left] + nums[right]  # Avoids shadowing built-in 'sum'
            if current_sum == target:
                triplets.append([nums[i], nums[left], nums[right]])

                # skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                # Must advance pointers past the matched pair
                left += 1
                right -= 1

            elif current_sum > target:
                right -= 1
            else:
                left += 1

    return triplets
```
