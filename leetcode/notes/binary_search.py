"""
Key Python operations: Binary Search.
"""

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

# Binary Search: Inclusive Bounds
# This is a closed interval [left, right] binary search, meaning both ends of the search space are inclusive.
# Use this when working with unique elements (no duplicates) and you only care whether the exact item exists.
# If the target is not in the array, it tells you it's missing (usually by returning -1),
#  though it can be adapted to return the insertion point i.e. return left instead of -1.
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

    return -1  # Target is not present in the array or return left if the insertion point is needed.


# Example usage:
numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target_val = 23
result = binary_search_iterative(numbers, target_val)
print(f"Index of {target_val}: {result}")  # Output: Index of 23: 5

# Binary Search: Lower Bound
# Finds the first position where an element is greater than or equal to the target.
# Uses half-open interval [left, right)
# Use this when you need to find an insertion position to maintain sorted order (like LeetCode 35)
# or when you need to find the first occurrence of a target in an array with duplicate values.
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

# Binary Search: Upper Bound
# Finds the first position where an element is strictly greater than the target.
# Uses half-open interval [left, right)
# Useful when you want to find the upper boundary of a range of duplicate elements (e.g., Finding the cut-off point where elements exceed a maximum limit.)
def upperBound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] <= target:
            # Target or smaller elements are at mid or to the left; 
            # move right to search for something strictly greater
            left = mid + 1
        else:
            # nums[mid] is strictly greater than target, 
            # but there might be an earlier valid element on the left
            right = mid
            
    return left

# Binary Search: Upper and Lower Bound Combined
#  Use both together when you need to find the entire range (start and end indices) of a duplicate element, such as in LeetCode 34 (Find First and Last Position of Element in Sorted Array).
# How it works: The lower bound gives you the starting index of the target, and the upper bound minus one (upper_bound - 1) gives you the ending index

# LC 34: Find First and Last Position of Element in Sorted Array
class Solution:
    # Check lower bound. This will find index of the first occurrence of the target in the sorted array if it exists,
    # or the index where it could be inserted to maintain sorted order if it doesn't exist.
    def lower_bound(self, nums: List[int], target: int):
        left = 0
        right = len(nums)

        while left < right:
            mid = (left + right) // 2

            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid
        
        return left

    # Check upper bound. This will find index of the first element that is strictly greater than the target in the sorted array if it exists,
    # or the index where it could be inserted to maintain sorted order if it doesn't exist.
    # !!!We will need to subtract 1 from the result of upper_bound to get the last occurrence of the target.!!!
    def upper_bound(self, nums: List[int], target: int):
        left = 0
        right = len(nums)

        while left < right:
            mid = (left + right) // 2

            if nums[mid] <= target:
                left = mid + 1
            else:
                right = mid
        
        return left

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        left_idx = self.lower_bound(nums, target)
        right_idx = self.upper_bound(nums, target)

        # We need to check if the target exists in the range (NOT if valid range)
        # 1. check if left_idx is out of bounds (greater than the last index)
        # 2. check if the element at left_idx is not equal to the target (meaning the target doesn't exist in the array)
        if left_idx > len(nums) - 1 or nums[left_idx] != target:
            return [-1, -1]
        else:
            return [left_idx, right_idx - 1]

#--------------------------------
# LeetCode 162: Find Peak Element
# In this case we don't need to sort the array instead we rely on the slope of the array to find a peak element.
# lower_bound / upper_bound are designed to find the insertion point, first occurrence, or last occurrence of a specific target value in a sorted array.
# In LC 162, there is no target value. You are looking for an arbitrary peak based on a local property rather than matching a specific number.
#--------------------------------
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

# LC 162: Find Peak Element (Brute Force)
def findPeakElement(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        # Check left neighbor (or treat as -inf if out of bounds)
        is_greater_left = (i == 0) or (nums[i] > nums[i - 1])
        # Check right neighbor (or treat as -inf if out of bounds)
        is_greater_right = (i == n - 1) or (nums[i] > nums[i + 1])
        
        if is_greater_left and is_greater_right:
            return i
            
    return 0

#--------------------------------
# LC 74: 2D Matrix
class Solution:
    """
    Approach: Treat the 2D matrix as a 1D sorted array (virtually flatten it) and perform binary search.
    1. Calculate the total number of elements in the matrix (m * n).
    2. Use binary search on the range [0, m * n - 1].
    3. For each mid index, map it back to 2D coordinates using:
       row = mid // n -> integer division to get the row index. Since each row has $n$ elements, dividing the 1D index by n tells you how many full rows precede your target index.
       col = mid % n -> modulo operation to get the column index. The remainder after dividing by n tells you how far into the current row your target index is.
    4. Compare the value at matrix[row][col] with the target.
    5. Adjust the search space based on the comparison.
    6. If the target is found, return True; otherwise, return False after the loop ends.

    Time complexity: O(log(m * n))
    Space complexity: O(1)
    """
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        left, right = 0, (m * n) - 1
        
        while left <= right:
            mid = (left + right) // 2
            # Map 1D index 'mid' back to 2D coordinates
            row = mid // n
            col = mid % n
            val = matrix[row][col]
            
            if val == target:
                return True
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return False
# --------------------------------
# Answer Space Problem
#--------------------------------
# Template
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

