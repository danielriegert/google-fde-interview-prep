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
Permutations: N!.
Combinations: N! / (N - k)!k!.
Subsets: 2^N, since each element could be absent or present.

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
            backtrack(i, path, current_sum + candidates[i])          # Explore (Notice 'i', not 'i + 1')
            path.pop()                                               # Un-choose
            
    backtrack(0, [], 0)
    return result

# LC 39: Combination Sum


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
