# Merge Sort
https://leetcode.com/problems/merge-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150

"""
The key insight: merge from the back, not the front.

Why from the back? If you merge left-to-right into nums1, you'd overwrite real elements in nums1[:m] before you've had a chance to read them (since the front of nums1 is exactly where you're writing). Merging from the back writes into the currently-unused tail (nums1[m:]), so you never clobber data you still need.

Three pointers:

p1 = m - 1 — last real element in nums1
p2 = n - 1 — last element in nums2
p = m + n - 1 — last slot in nums1, where the next (largest remaining) value goes
At each step, place the bigger of nums1[p1] / nums2[p2] at nums1[p], then move that pointer and p left. Stop once nums2 is exhausted — if nums1 still has leftover elements, they're already in the correct spot (since they're the smallest and already sitting at the front).
"""

def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    p1 = m - 1
    p2 = n - 1
    p = m + n - 1

    while p2 >= 0:                     # only need to stop when nums2 is empty
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
"""
Trace: nums1 = [1,2,3,0,0,0], m=3, nums2 = [2,5,6], n=3

p1	p2	p	comparison	write	nums1
2	2	5	3 vs 6 → 6 wins	nums1[5]=6	[1,2,3,0,0,6]
2	1	4	3 vs 5 → 5 wins	nums1[4]=5	[1,2,3,0,5,6]
2	0	3	3 vs 2 → 3 wins	nums1[3]=3, p1→1	[1,2,3,3,5,6]
1	0	2	2 vs 2 → nums2 wins (tie goes to else)	nums1[2]=2	[1,2,2,3,5,6]
1	-1	—	p2 < 0, loop ends		[1,2,2,3,5,6] ✓
Notice the loop only checks p2 >= 0, not p1 >= 0, as its exit condition — once nums2 is fully placed, any remaining nums1 elements are already sitting correctly at the front, so there's nothing left to do. That's the part people usually get wrong when writing this from scratch.

This is O(m+n) time, O(1) extra space — no sort() needed.
"""


# =========================================================
# Two Pointers (opposite-direction / converging)
# =========================================================

# Two Sum II - Input Array Is Sorted
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

"""
The key insight: sorted input means you can rule out a whole pointer position in one comparison, instead of checking every pair.

left = 0 (smallest value), right = len(nums) - 1 (largest value).
At each step, look at nums[left] + nums[right]:
- If it's exactly target, done.
- If it's too small, the ONLY way to increase the sum is to move left forward (right is already the biggest value available, moving it would only make the sum smaller).
- If it's too big, the ONLY way to decrease the sum is to move right backward.

Because the array is sorted, each comparison eliminates one index permanently — you never need to revisit it. That's what gets this to O(n) instead of the O(n^2) brute-force pair check.
"""

def two_sum(nums: List[int], target: int) -> List[int]:
    left, right = 0, len(nums) - 1

    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left + 1, right + 1]   # LeetCode wants 1-indexed positions
        elif total < target:
            left += 1
        else:
            right -= 1

    return []

"""
Trace: nums = [2, 7, 11, 15], target = 9

left  right  nums[left]+nums[right]  compare        action
0     3      2 + 15 = 17             17 > 9  (big)   right -= 1
0     2      2 + 11 = 13             13 > 9  (big)   right -= 1
0     1      2 + 7  = 9              9 == 9  (match) return [1, 2]

Each row moves exactly one pointer, never both, and never backtracks — that's the O(n) guarantee.
"""


# =========================================================
# Two Pointers (same-direction / fast-slow)
# =========================================================

# Remove Duplicates from Sorted Array
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

"""
The key insight: slow marks the boundary of the "cleaned" region; fast does all the scanning.

slow always points at the last element known to be unique so far. fast walks ahead
looking for the next value that's different from nums[slow]. When it finds one, slow
advances by one and copies that value into place — so writes only happen when there's
actually something new to keep. Everything fast skips over (duplicates) just gets
overwritten later or ignored.

Because the array is sorted, all duplicates of a value are adjacent, so "different from
nums[slow]" is a sufficient check for "this is a new unique value."
"""

def remove_duplicates(nums: List[int]) -> int:
    if not nums:
        return 0

    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1

"""
Trace: nums = [0, 0, 1, 1, 1, 2, 2, 3]

fast  nums[fast]  vs nums[slow]  action                  slow  nums (first slow+1 entries)
1     0           == 0           skip                    0     [0]
2     1           != 0           slow=1, nums[1]=1        1     [0, 1]
3     1           == 1           skip                    1     [0, 1]
4     1           == 1           skip                    1     [0, 1]
5     2           != 1           slow=2, nums[2]=2        2     [0, 1, 2]
6     2           == 2           skip                    2     [0, 1, 2]
7     3           != 2           slow=3, nums[3]=3        3     [0, 1, 2, 3]

Return slow + 1 = 4 -> nums[:4] = [0, 1, 2, 3] are the unique values, in place, O(1) extra space.
"""