Here is the comprehensive guide combining the core approaches, operational sequences, code snippets, and explanations for all **five two-pointer variations**.

---

## **1. Opposite Direction (Converging Pointers)**

### **Core Approach**

Place pointers at opposite ends of a collection (e.g., the start and end of a sorted array) and move them toward each other to systematically shrink the search space until they meet.

### **Sequence of Operations**

1. Initialize `left = 0` and `right = n - 1`.
2. Run a `while left < right` loop.
3. Evaluate the pair `(left, right)` against the target condition.
4. Move **one** pointer inward based on the evaluation (increment `left` if the value is too small; decrement `right` if it is too large).
5. Stop and return the result when the pointers meet or cross.

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

### **Sequence of Operations**

1. Initialize `slow = 0` and `fast = 0`.
2. Run a loop where `fast` iterates through the entire collection.
3. Evaluate the element at `fast` against a specific condition.
4. If the condition is met, process or swap the element into the `slow` index, then increment `slow`.
5. Always increment `fast` to keep scanning.

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

### **Sequence of Operations**

1. Initialize `left = 0`, an optimal tracking variable, and a state tracker (like a hash map or set).
2. Loop `right` from `0` to `n - 1` to expand the right boundary.
3. Add the element at `right` to your tracker state.
4. Run a `while` loop checking if the window violates a constraint. If violated, increment `left` to shrink the window and update the state.
5. Record or update your optimal metric at each step.

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

## **4. Two-Array / Merge Pattern**

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

## **5. Expand Around Center**

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
    while left >= 0 and right < len(s) and s[left] == s[right]:
      left -= 1
      right += 1
    return right - left - 1  # Returns the length of the palindrome

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
