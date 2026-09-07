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

