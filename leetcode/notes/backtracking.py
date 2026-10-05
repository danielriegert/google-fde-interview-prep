"""
Backtracking is essentially an optimized brute-force technique. It systematically searches through all
 possible configurations by building solutions incrementally and abandoning ("backtracking") a path the moment it violates 
 the problem's constraints

Key Indicators in the Problem Statement

* **"Find all possible..." or "Generate all...":** The prompt asks for every valid configuration, subset, permutation, 
or combination rather than a single optimal answer.
* **Sequential Decision-Making:** At any given step, you must choose between multiple paths, and each choice alters the state 
for subsequent steps.
* **Early Pruning:** A partial solution can be evaluated before it is fully complete, allowing you to stop exploring
 invalid branches early.


Common LeetCode Problem Categories

* **Combinatorics:** Classic generation tasks like *Subsets*, *Permutations*, *Combinations*, and *Letter Combinations of a Phone Number*.
* **Constraint Satisfaction & Games:** Board or grid puzzles with strict rules, such as *N-Queens*, *Sudoku Solver*, or *Word Search*.
* **Partitioning:** Breaking down a sequence into valid segments that meet specific criteria, like *Palindrome Partitioning*.

Clues from Constraints and Complexity

* **Small Input Sizes:** Constraints like $N \le 15$ or $N \le 20$ strongly hint at exponential time complexity ($O(2^n)$ or $O(N!)$), which backtracking naturally handles.
* **The "Choose, Explore, Un-choose" Pattern:** If your algorithmic logic requires you to modify a state (e.g., add to a path), recurse deeper, and then undo that modification upon return, you are writing backtracking.

Solution space:
- Permutations: N!.
- Combinations: N! / (N - k)!k!.
- Subsets: 2^N, since each element could be absent or present.

Common backtracking problems:
Subsets
Subsets II
Permutations
Permutations II
Combinations
Combination Sum II
Combination Sum III
Palindrome Partition
"""
# Template for Subset backtracking problems
def solve(self, input_data):
    result = []
    
    def backtrack(path, start_index, other_state_params):
        # 1. Base Case: Check if the current path forms a valid complete solution
        if self.is_goal(path):
            result.append(path[:])  # Make a deep copy of the path
            return
        
        # 2. Iterate through available choices
        for i in range(start_index, len(input_data)):
            choice = input_data[i]
            
            # 3. Pruning: Skip invalid choices if necessary
            if not self.is_valid(choice, path):
                continue
                
            # 4. CHOOSE: Make the choice
            path.append(choice)
            
            # 5. EXPLORE: Recurse deeper with the updated state
            backtrack(path, i + 1, other_state_params)  # i + 1 or i depending on reuse rules
            
            # 6. UN-CHOOSE: Backtrack by undoing the choice
            path.pop()

    backtrack([], 0, initial_params)
    return result

# LC 78: Subsets
"""
We define a backtrack function named backtrack(first, curr) that takes the index of the first element to add and a current 
combination as arguments.

    If the current combination is done, we add the combination to the final output.

    Otherwise, we iterate over the indexes i from first to the length of the entire sequence n.

        Add integer nums[i] into the current combination curr.

        Proceed to add more integers into the combination: backtrack(i + 1, curr).

        Backtrack by removing nums[i] from curr.

Time: O(N x 2^n) to generate all subsets and then copy them into the output list.
Space: We are using O(N) space to maintain curr, and are modifying curr in-place with backtracking. 

Tree of choices for nums = [1, 2] (the numbers in the input array) is shown below. The root of the tree is an empty set, and each
node's children are the numbers that can be added to the current combination.
                [] 
            /      \
      (Add 1)      (Add 2)
          /          \
       [1]           [2] 2 is last item in the list, you can't pick anything after it, branch terminates immediately after creating [2]
       /
  (Add 2)
    /
 [1, 2]
"""
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        # Every path is a valid subset, so we add it immediately
        result.append(path[:])

        # recursion will terminate and unwind back up when start reaches the length of nums, so we don't need an explicit base case here
        for i in range(start, len(nums)):
            path.append(nums[i])       # Choose
            backtrack(i + 1, path)     # Explore
            path.pop()                 # Un-choose
            
    backtrack(0, [])
    return result

# LC 90: Subsets II
class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        res = []
        nums.sort()
        
        def backtrack(start, path):
            # Every state is a valid subset
            res.append(path[:])
            
            for i in range(start, len(nums)):
                # Skip duplicates at the same recursion level
                if i > start and nums[i] == nums[i - 1]:
                    continue
                
                # Choose
                path.append(nums[i])
                
                # Explore (next index is i + 1)
                backtrack(i + 1, path)
                
                # Un-choose (Backtrack)
                path.pop()
                
        backtrack(0, [])
        return res

# Template for Permutation backtracking problems
"""
The Twist: The order of elements matters, meaning [1, 2] and [2, 1] are treated as separate valid solutions.
How it changes: Instead of a start index that only moves forward, you loop through the entire array on every recursive call. 
To prevent reusing the exact same element index twice, you maintain a used boolean array or check if num in path.
"""
def permute(nums):
    result = []
    
    def backtrack(path):
        # Base Case: If the path length matches nums, we have a full permutation
        if len(path) == len(nums):
            result.append(path[:])
            return
            
        for i in range(len(nums)):
            # Pruning: Skip if the element is already used in the current path
            if nums[i] in path:
                continue
                
            path.append(nums[i])       # Choose
            backtrack(path)            # Explore (starts from index 0 again)
            path.pop()                 # Un-choose
            
    backtrack([])
    return result
# LC 46: Permutations
"""
Core idea:
Try all numbers in the first position. For each number in the first position,
 try all other numbers in the second position. For each pair of numbers in the first and second positions, 
 try all other numbers in the third position, and so on.

Once we find all permutations that start with a given prefix, we backtrack and try the next number in the first position.

Each element can only appear once in a valid permutation.
         (Root)
        /  |  \
       1   2   3
      / \ / \ / \
     2  3 1 3 1  2
     |  | | | |  |
     3  2 3 1 2  1
     
[1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]

Time: O(N x N!) to generate all permutations and then copy them into the output list.
Space: We are using O(N) space to maintain path, and are modifying path in-place with backtracking.
"""
class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        # This list will store all the completed permutations
        result = []

        def backtrack(path):
            # Base Case: If our current path has the same length as nums,
            # it means we have formed a valid complete permutation.
            if len(path) == len(nums):
                # We append a copy of the path (path[:]) because 'path' 
                # will change later as we backtrack and pop elements.
                result.append(path[:])
                return
            
            # Choice & Exploration: Iterate through each number in the input list
            for num in nums:
                # Constraint: Only use numbers that are not already in our current path
                if num not in path:
                    # 1. CHOOSE: Add the number to the current permutation path
                    path.append(num)
                    
                    # 2. EXPLORE: Recursively call backtrack to fill the next position
                    backtrack(path)
                    
                    # 3. UN-CHOOSE (BACKTRACK): Remove the last number so we can 
                    # try a different number in the next loop iteration
                    path.pop()
        
        # Kick off the recursive backtracking process with an empty path
        backtrack([])
        
        # Return all collected permutations
        return result

# LC 47: Permutations II
# This problem is similar to LC 46, but the input list may contain duplicates.
class Solution:
    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        result = []
        
        # 1. Sort the array so duplicates are adjacent to each other
        nums.sort()
        
        # Track which elements (by index) have already been used in the current path
        visited = [False] * len(nums)

        def backtrack(path):
            # Base Case: If our current path has the same length as nums,
            # we have formed a valid complete permutation.
            if len(path) == len(nums):
                result.append(path[:])
                return
            
            for i in range(len(nums)):
                # If this specific element is already used in this path, skip it
                if visited[i]:
                    continue
                
                # Deduplication Check:
                # If the current number is the same as the previous number, 
                # AND the previous number was NOT used in this branch of recursion, 
                # we skip it to prevent generating duplicate permutations.
                if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                    continue
                
                # 1. CHOOSE: Mark index as visited and add to path
                visited[i] = True
                path.append(nums[i])
                
                # 2. EXPLORE: Recurse to fill the next position
                backtrack(path)
                
                # 3. UN-CHOOSE (BACKTRACK): Reset state for the next iteration
                path.pop()
                visited[i] = False
        
        backtrack([])
        return result
    
# Template for Combination backtracking problems
"""
The Twist: Elements can be picked multiple times, usually constrained by a target sum or limit.
How it changes: When you recurse deeper, you pass i instead of i + 1 as the start index, allowing the next recursive step 
to consider the exact same element again.
"""
def combinationSum(candidates, target):
    result = []
    
    def backtrack(start, path, current_sum):
        # Base Case: Hit the target sum
        if current_sum == target:
            result.append(path[:])
            return
            
        # Pruning: Stop if we overshoot the target
        if current_sum > target:
            return
            
        for i in range(start, len(candidates)):
            path.append(candidates[i])                               # Choose
            # Important: need to pass current_sum + candidates[i] directly to avoid modifying it for future iterations
            # by passing 'i' instead of 'i + 1', we allow the same candidate to be reused in the next recursive call
            backtrack(i, path, current_sum + candidates[i])          # Explore (Notice 'i', not 'i + 1')
            path.pop()                                               # Un-choose
            
    backtrack(0, [], 0)
    return result

# LC 39: Combination Sum
# This allows reuse of the same element multiple times in a combination, as long as the sum does not exceed the target.
"""
                                  [ ]
                                   |
         +-------------------------+-------------------------+
         |                         |                         |
       [3]                       [4]                       [5]
         |                         |                         |
   +-----+-----+           +-------+-------+                 |
   |     |     |           |               |                 |
 [3,3] [3,4] [3,5]*      [4,4]*          [4,5]#            [5,5]#
   |     |                   
 [3,3,3]# [3,4,4]#           
 
Legend:
----------------------------------------
[ ]    : Root / Empty path[cite: 1]
*      : Valid path or branch point
#      : Exceeds target (Terminates / Red node in diagram)[cite: 1]

An important detail on choosing the next number for the combination is that we select the candidates in order, 
where the total candidates are treated as a list.
Once a candidate is added into the current combination, we will not look back to all the previous candidates in the next explorations.

Time: O(N^target/min(candidates) + 1) where N is the number of candidates. The depth of the recursion tree can go up to target/min(candidates) and at each level, we have N choices.
Space: O(target/min(candidates)) for the recursion stack and the path list.
"""
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        result = []  # Stores all valid combinations that sum up to the target

        def backtrack(start, path, current_sum):
            # Base Case 1: If the current sum equals the target, 
            # add a copy of the current path to our results list and return.
            if current_sum == target:
                result.append(path[:])
                return
            
            # Base Case 2: If the current sum exceeds the target, 
            # stop exploring this branch (known as pruning).
            if current_sum > target:
                return
            
            # Iterate through candidates starting from the 'start' index
            for i in range(start, len(candidates)):
                path.append(candidates[i])  # Choose: add the current candidate to our path
                
                # Recurse: pass 'i' (instead of i + 1) to allow reusing the same element,
                # and update the running sum.
                backtrack(i, path, current_sum + candidates[i])
                
                path.pop()  # Unchoose (Backtrack): remove the last element to try the next candidate

        backtrack(0, [], 0)  # Kick off the backtracking from index 0 with an empty path and 0 sum
        return result        # Return the accumulated list of valid combinations

# LC 216: Combination Sum III
# Each number can only be used once in the combination, and the numbers are chosen from 1 to 9.
class Solution:
    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        result = []

        def backtrack(start, path, current_sum):
            # Base Case 1: If we have picked exactly k numbers AND their sum equals n (target)
            if len(path) == k and current_sum == n:
                result.append(path[:])
                return
            
            # Base Case 2: Pruning. Stop early if we exceed the length 'k' 
            # or exceed the target sum 'n'.
            if len(path) > k or current_sum > n:
                return
            
            # Iterate through valid numbers from 1 to 9 (using 'start' to avoid duplicates)
            for i in range(start, 10):
                path.append(i)  # Choose: add number to path
                
                # Recurse: 
                # - Pass 'i + 1' so the same number cannot be reused
                # - Update current_sum by adding 'i'
                backtrack(i + 1, path, current_sum + i)
                
                path.pop()  # Unchoose (Backtrack): remove the number to try the next one

        # Start backtracking from number 1, with an empty path and 0 sum
        backtrack(1, [], 0)
        return result

# Grid and Matrix Backtracking Template
"""
Key adjustment: Instead of a linear loop over an array, you branch out in four directions (up, down, left, right). 
You "choose" by temporarily mutating the board cell or using a visited set, and "un-choose" by reverting it.
"""
def exist(board, word):
    rows, cols = len(board), len(board[0])
    
    def backtrack(r, c, index):
        # Base Case: Found all characters of the word
        if index == len(word):
            return True
            
        # Pruning: Check boundaries and if current cell matches the target character
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[index]:
            return False
            
        # Choose: Temporarily mark cell as visited so we don't reuse it in this path
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore: Search all 4 directions for the next character
        found = (backtrack(r + 1, c, index + 1) or
                 backtrack(r - 1, c, index + 1) or
                 backtrack(r, c + 1, index + 1) or
                 backtrack(r, c - 1, index + 1))
                 
        # Un-choose: Restore the cell back to its original value
        board[r][c] = temp
        return found

    # Trigger the search from every cell on the board
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
                
    return False

# LC 79: Word Search



