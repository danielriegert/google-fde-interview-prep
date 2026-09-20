# Kadanes Algorithm
"""
This is also DP. Just space optimized

**Kadane's Algorithm** is an efficient, linear-time dynamic programming algorithm used to find the maximum possible sum of a 
contiguous subarray within a one-dimensional array of numbers (which can include both positive and negative integers).

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