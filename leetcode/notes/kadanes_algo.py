# Kadanes Algorithm
"""
This is also DP. Just space optimized

**Kadane's Algorithm** is an efficient, linear-time dynamic programming algorithm used to find the maximum possible sum of a 
**contiguous subarray** within a one-dimensional array of numbers (which can include both positive and negative integers).

### How It Works
The core intuition behind the algorithm is to iterate through the array while maintaining two primary values:
1. **Current Subarray Sum (`current_max`):** At each element, the algorithm decides whether to:
* **Extend** the existing subarray by adding the current element to it.
* **Start a fresh** subarray at the current element (abandoning the previous running sum because it has become a net negative 
and would drag down future sums).

2. **Global Maximum (`global_max`):** Throughout the iteration, it continuously compares the `current_max` against the highest 
sum seen so far, updating the global record whenever a new maximum is reached.

### Why It's Efficient

A naive brute-force approach would check every possible starting and ending index combination, 
resulting in an $O(n^2)$ or $O(n^3)$ time complexity. Kadane's algorithm solves the problem in a **single pass**, 
reducing the time complexity to **$O(n)$** with **$O(1)$ auxiliary space**, making it the optimal solution for the Maximum Subarray Problem.
"""
# LC 53:
def max_subarray_sum(nums: list[int]) -> int:
    if not nums:
        return 0
        
    current_max = nums[0]
    global_max = nums[0]
    
    for num in nums[1:]:
        # Decide whether to add the current number to the existing subarray 
        # or start a new subarray from the current number
        current_max = max(num, current_max + num)
        
        # Update the global maximum if the current subarray sum is greater
        global_max = max(global_max, current_max)
        
    return global_max

# Example usage:
numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_sum(numbers))  # Output: 6 (from the subarray [4, -1, 2, 1])

#--------------------------------
# when we start a new window need to track temp statr index and whenever we update the global max we update start ad end index
def max_subarray_with_indices(nums: list[int]) -> tuple[int, int, int]:
    if not nums:
        return 0, -1, -1
        
    global_max = current_max = nums[0]
    start = end = temp_start = 0
    
    for i in range(1, len(nums)):
        num = nums[i]
        
        # Decide whether to add to the existing subarray or start a new one
        if num > current_max + num:
            current_max = num
            temp_start = i
        else:
            current_max = current_max + num
            
        # Update the global maximum and index bounds if a new maximum is found
        if current_max > global_max:
            global_max = current_max
            start = temp_start
            end = i
            
    return global_max, start, end

# Example usage:
numbers = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_sum, start_idx, end_idx = max_subarray_with_indices(numbers)

print(f"Maximum Sum: {max_sum}")
print(f"Indices: {start_idx} to {end_idx}")
print(f"Subarray: {numbers[start_idx:end_idx + 1]}")
# Output: 
# Maximum Sum: 6
# Indices: 3 to 6
# Subarray: [4, -1, 2, 1]


# LC 152
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        # Edge case: if the array is empty, return 0
        if len(nums) == 0:
            return 0

        # Initialize tracking variables with the first element
        max_so_far = nums[0]  # Tracks the max product ending at the current position
        min_so_far = nums[0]  # Tracks the min product (crucial for flipping negatives)
        result = max_so_far   # Global maximum product found across the whole array

        # Iterate through the rest of the array starting from index 1
        for i in range(1, len(nums)):
            curr = nums[i]
            
            # Compute the new max product ending at 'curr'. 
            # We look at three choices: 
            # 1. Start fresh at 'curr' (drops previous history). Needed for 0s and negative numbers.
            # 2. Extend previous max_so_far * curr
            # 3. Extend previous min_so_far * curr (if curr is negative, min * negative = max)
            # We store this in a temporary variable so we don't overwrite max_so_far prematurely.
            temp_max = max(curr, max(max_so_far * curr, min_so_far * curr))
            
            # Compute the new min product ending at 'curr'.
            # Note: This relies on the *old* value of max_so_far, which is why 
            # we use temp_max instead of updating max_so_far right away.
            min_so_far = min(curr, min(max_so_far * curr, min_so_far * curr))

            # Now safely update max_so_far from our temporary storage
            max_so_far = temp_max
            
            # Update the global result if the current local max is the highest seen so far
            result = max(max_so_far, result)

        return result


# LC 918: Maximum Sum Circular Subarray
# ToDo: Review
# Key Insight: The maximum sum of a circular subarray can be:
# 1. Using standard Kadane's algorithm to find the maximum subarray sum in the non-circular case.
# 2. Finding the minimum subarray sum (using a variant of Kadane's) and subtracting it from the total sum of the array. 
# This effectively gives us the maximum sum of the circular subarray.
def maxSubarraySumCircular(nums: list[int]) -> int:
    total = 0
    cur_max, max_sum = 0, nums[0]
    cur_min, min_sum = 0, nums[0]

    for n in nums:
        total += n
        
        # Standard Kadane for maximum
        cur_max = max(n, cur_max + n)
        max_sum = max(max_sum, cur_max)
        
        # Kadane variant for minimum (to find the part we drop)
        cur_min = min(n, cur_min + n)
        min_sum = min(min_sum, cur_min)

    # Edge case: if all numbers are negative, total == min_sum, 
    # and total - min_sum would be 0, which is invalid. Return max_sum instead.
    if max_sum < 0:
        return max_sum

    return max(max_sum, total - min_sum)