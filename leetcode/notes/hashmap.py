# LC 1: Two Sum
from ast import List


def twoSum(self, nums: List[int], target: int) -> List[int]:
    complements = {}

    for i in range(len(nums)):
        complement = target - nums[i]

        if complement in complements:
            return [i, complements[complement]]
        
        complements[nums[i]] = i
    
    return []

# LC 560: Subarray Sum Equals K
from typing import List
"""
Core idea:
Keep track of cummulative sum up to current element and store it in a HashMap.
Check if there is a previous cummulative sum that, when subtracted from the current cummulative sum, equals k.
If such a previous cummulative sum exists, it means there is a subarray that sums to k.
We increase the overall count by the frequency of that previous cummulative sum in the HashMap.
Time Complexity: O(n) - We traverse the list once.
Space Complexity: O(n) - In the worst case, we may store all prefix sums in the HashMap.
"""
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # Tracks the total number of continuous subarrays that sum up to k
        count = 0
        
        # Maintains the cumulative sum of elements from index 0 up to the current index
        current_sum = 0
        
        # HashMap to store the frequency of each prefix sum encountered so far.
        # Format: { prefix_sum: frequency }
        # {0: 1} is the base case: a prefix sum of 0 has occurred once. 
        # This handles subarrays that start directly from index 0 and equal k.
        prefix_sums = {0: 1}  

        for num in nums:
            # Step 1: Accumulate the running prefix sum
            current_sum += num
            
            # Step 2: Find the required past prefix sum (complement) such that it adds up to k.
            # Mathematical logic: 
            # If (current_sum - previous_prefix_sum) == k,
            # then previous_prefix_sum = current_sum - k.
            # We are looking to see if this 'complement' exists in our history. If it does then there exists a subarray that sums to k.
            complement = current_sum - k

            # Step 3: Check if the complement exists in our HashMap
            if complement in prefix_sums:
                # If it exists, it means one or more subarrays ending at the current index sum to k.
                # We add the frequency of that prefix sum to our total count because 
                # each time that prefix sum occurred in the past, it formed a valid subarray with the current index.
                count += prefix_sums[complement]
            
            # Step 4: Record the current prefix sum into the HashMap for future iterations.
            # We use .get() to safely initialize new keys at 0 before adding 1, 
            # avoiding a KeyError if this prefix sum has never been seen before.
            prefix_sums[current_sum] = prefix_sums.get(current_sum, 0) + 1
        
        # Return the total number of valid subarrays found
        return count

# Brute Force Approach (for reference):
from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        n = len(nums)
        
        # Outer loop: choose the starting point of the subarray
        for i in range(n):
            current_sum = 0
            
            # Inner loop: extend the subarray to the right
            for j in range(i, n):
                current_sum += nums[j]
                
                # Check if this subarray's sum matches the target
                if current_sum == k:
                    count += 1
                    
        return count