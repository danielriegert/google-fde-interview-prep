"""
Key Python operations: Dynamic Programming.
Covers 1D DP, 2D DP (grid and subsequence problems), and top-down memoization.
"""

# ==========================================================
# DP 1D
# ==========================================================
"""
1. The Two Core Mathematical Properties
For a problem to be solvable by DP, it must possess two specific traits:
- Overlapping Subproblems: The same smaller subproblems are repeatedly encountered and solved when exploring different choices. If you draw a recursive tree and see identical nodes repeating across different branches, DP will save you from redundant work.
- Optimal Substructure: The optimal solution to the overall problem can be built using the optimal solutions of its subproblems. For example, knowing if a string up to index 4 can be broken helps you determine if the string up to index 8 can be broken.

2. Clues in the Problem Statement
When reading a coding problem description, certain phrases and requirements strongly hint at DP:
- Finding Extremes: Words like minimum cost, maximum profit, longest path, or shortest distance.
- Counting Combinations: Questions that ask "How many ways are there to..." (e.g., Coin Change, Climbing Stairs).
- Existence Questions: Questions that ask "Is it possible to reach the target?" or "Can this be formed?" (like the Word Break problem we just looked at).
- Sequence Decisions: Problems where you make a series of choices (e.g., "take this item or leave it", "cut the rope here or there"), and each choice alters the state of what remains.

Important: Instead of asking "Where can I go from here?", dynamic programming asks "How could I have possibly arrived here?"
When problem can be thought of decision tree. DP is a clever way to solve that tree without actually building it or recalculating duplicate branches.
Brute force approach is usually DFS using recursion.
Check:
- Can I break it into smaller subproblems?
- Do past choices restrict future choices?
- Are choices independent of how I got here?

Step 1: Define the State (dp[i])
Ask yourself: What does the subproblem represent? For 1D array problems, dp[i] usually means: "The optimal answer (max profit, min cost, total ways) considering elements from index 0 up to i."

Step 2: Find the Recurrence Relation (Transition)
Ask yourself: What choices do I have at the current element i?
Usually involves taking the maximum or minimum between:
    Skipping the current element (looking back at dp[i-1]).
    Taking the current element (combining it with dp[i-2] or an earlier state based on constraints).

Step 3: Establish the Base Cases (cases that cannot be split into smaller subproblems, are defined by transition i.e. how fast back we need to look)
Ask yourself: What are the smallest valid inputs where the answer is obvious?
Handle edge cases (empty array, single element).
Initialize dp[0] and often dp[1] manually before entering a loop.

Step 4: Determine the Final Answer & Optimize Space
The final answer is typically at the end of your DP array (e.g., dp[-1]).S
pace Optimization Trick: If dp[i] only depends on the previous 1 or 2 values (i-1, i-2), you can drop the array entirely and use variables to achieve $O(1)$ space.

Time Complexity: O(n) where n is the length of the input array.
Space Complexity: O(n) for the DP array, or O(1) if optimized to use variables instead of an array.
"""

# Lesson Learned
"""
General:
- Transition might involve iterating wiht nested for loop about all possible combinations e.g. coin exchange, word break where we have two inputs
 or where we skip elements e.g. longest subsequeunce (LC 3000)
- state table usually tracks what we need to return as final result
- trying to decompose into sub problems that build up to final solution
- we look back at how we could have arrived at the current point
- can space optimize if we only rely on i previous results
String problems:
- For string problems base case is usually empty string for array check samallest possible value e.g. 0

Array problems:
- Index of dp might be the target value (like the amount in Coin Change) 

"""

# Common Transitions
"""
1. Liner choice (House Robber LC198, Climbing Stairs 70)
Decide whether to take the current element and combine with immediate neighbors.
Transition examples: 
- dp[i] = max(dp[i-1], dp[i-2] + nums[i])
- dp[i] = dp[i - 1] + dp[i - 2]

2. Partition / Jump (WordBreak LC139)
Build current state by checking all valid previous split or jump points.
Might need nested for loop
Transition examples:

3. Subsequeune


4. Longest Increasing Subsequeunce
Check all previous elements to see if the current one can extend an increasing sequence.
Might need nested for loop

5. Subarray (Kadane)
Decide whether to extend the previous contiguous subarray or start fresh.
Transition examples:
dp[i] = max(nums[i], dp[i-1] + nums[i])

6. String prefix
Count valid decodings/paths by looking back 1 or 2 characters in a string.

7. State machine
Track mutually exclusive actions or states (e.g., holding vs. not holding) at step $i$.
"""

# Template
def solveSimilarProblem(self, nums: list[int]) -> int:
    # Step 2: Handle edge cases and base cases
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    # Step 1: Initialize DP array (or variables for space optimization)
    dp = [0] * len(nums)
    dp[0] = ... # base case 1 e.g. only one house to rob
    dp[1] = ... # base case 2 e.g. two houses, choose the max/min based on problem context
    
    # Step 3: Iterate and apply recurrence relation
    for i in range(2, len(nums)):
        dp[i] = max/min(
            dp[i - 1],              # Choice 1: Skip
            dp[i - 2] + nums[i]     # Choice 2: Take (with constraint)
        )
        
    # Step 4: Return final state
    return dp[-1]

def solveSpaceOptimized(self, nums: list[int]) -> int:
    # Step 1: Initialize variables to represent previous states
    # (The number of variables depends on how far back your recurrence relation looks)
    prev2 = 0  # Represents i - 2 (or older)
    prev1 = 0  # Represents i - 1 (the immediate predecessor)
    
    # Step 2: Iterate through the input data
    for item in nums:
        # Step 3: Compute the optimal choice for the current step
        # Replace this logic with your specific problem's rule (e.g., max, min, sum)
        current = max(prev1, prev2 + item) 
        
        # Step 4: Shift the history forward for the next iteration
        prev2 = prev1
        prev1 = current
        
    # Step 5: Return the final state variable
    return prev1


# ---------------------------------
# LC 322
"""
Coin Change is a classic introduction to the Unbounded Knapsack Pattern (where an item can be used an unlimited number of times).

In dynamic programming, you use the array index as the target value (like the amount in Coin Change) when the value itself is the state you are trying to optimize or reach, rather than a position in an input list.
    Use it when: The problem asks you to find a combination, count, or minimum/maximum cost to reach a specific numerical target (e.g., amount = 11, target sum = 7). 
    The index i directly represents "amount i".
    Do not use it when: The problem gives you a fixed array and wants you to pick elements based on their spatial position or sequence (e.g., House Robber, where index i means "house i").

State: Fewest numbers of coins need to maek up to given sub amount i
Base: number of coins to make up amount 0
Transition: For every amount i from 1 to amount, we look at each available coin:
If the coin can fit into the current amount (coin <= i), we check whether using this coin gives us a smaller total number of coins than what we currently have recorded for dp[i].

Formula:
dp[i] = min(dp[i], dp[i - coin] + 1)

Time complexity: O(a∗c)
    a is number of amount and c is number of coins
Space complexity: O(a)

"""
def coinChange(self, coins: list[int], amount: int) -> int:
    # Inint array with current amount + 1 representing not reachable to ensure
    # min() will work
    # Index represents amount and value min number of coins to make it
    min_coins = [amount + 1] * (amount + 1)

    # Base case is number of coins needed for amount 0
    min_coins[0] = 0

    # iterate through all possible amounts including actual amount
    for i in range(1, amount + 1):
        # for each sub amount check all coin combinations to get min number to reach sub amount
        for coin in coins:
            # check if coin is less than amount. if yes we update table by checking how many steps we needed for current amount - coin
            # then we add 1 for current coin
            if i - coin >= 0:
                min_coins[i] = min(min_coins[i], 1 + min_coins[i - coin])
    
    # Check if we found valid combination
    return min_coins[-1] if min_coins[-1] != amount + 1 else -1

# -------------------------------
# LC 300
"""
State: lenght longest subsequence that ends at index i. init with all 1s
Base case: dp[i] = 1 for all indices i
Transition: For each index i, loop through all previous indices j from 0 to i-1. 
If nums[i] > nums[j], update dp[i] to be the maximum of its current value or dp[j] + 1.

Time: O(n^2)
Space: O(n)

Can also be solve using binray search.
Can NOT be solved with slidign window
"""
def lengthOfLIS(self, nums: list[int]) -> int:
    longest_sub_so_far = [1] * len(nums)

    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                longest_sub_so_far[i] = max(longest_sub_so_far[i], longest_sub_so_far[j] + 1)
    
    return max(longest_sub_so_far)

# -------------------------------
# LC 139
"""
State: If it is a match so far i.e. True or False
Base case: epmty string
Transition: Can we form a valid prefix of length i if we already know whether smaller prefixes can be formed?

Time complexity: O(n∗m∗k)
    n is length of input string.
    m is number of words in wordDict
    k is average size of substrings.

Space complexity: O(n)

"""
def wordBreak(self, s: str, wordDict: list[str]) -> bool:
    # init with False and len + 1 to account for empty sting
    match_so_far = [False] * (len(s) + 1)
    # base case empty string
    match_so_far[0] = True

    # iterate through all prefixes of s
    for i in range(1, len(s) + 1):
        # check if last chars of s can make up a word in dict
        for word in wordDict:
            # calculate start of prefix to check
            start = i -len(word)

            # check if word is at least same size as prefix, if previous prefix before current one can be segmented, if current prefix is a match
            if start >= 0 and match_so_far[start] and s[start:i] ==  word:
                match_so_far[i] = True
                break

    return match_so_far[-1]


def wordBreak(self, s: str, wordDict: list[str]) -> bool:
    memo = {}

    def dfs(i: int) -> bool:
        # Base case: if we've reached the end of the string, it's a valid break
        if i == len(s):
            return True
        
        # Return cached result if we've already solved for this index
        if i in memo:
            return memo[i]

        for word in wordDict:
            # Check if the dictionary word fits and matches the substring starting at index i
            if s.startswith(word, i):
                # Recursively check the rest of the string starting after this word
                if dfs(i + len(word)):
                    memo[i] = True
                    return True

        # If no words work from this index, cache as False and return
        memo[i] = False
        return False

    return dfs(0)


# LC 790

# ==========================================================
# DP 2D
# ==========================================================
"""
Key signs:
Optimization Objective: e..g minimum number of operations.
Choices at Every Step: you have multiple valid choices at a given step that branch out into future states.
Overlapping Subproblems: A recursive solution without memoization would repeatedly compute the result for the same inputs.
You know a problem requires 2D DP when your state depends on two independent, changing inputs

Can think of it as graph. DP optimized way of solving it.
Brute force: DFS with memoization. DP: Bottom up tabulation.
"""
# ----------------Grid Problems: 2D DP-----------------------
"""
Grid based problems: 2D DP:
Base case for bottom up: first row and first column (or first cell)
    - Often, the first row and first column are initialized based on the problem's constraints (e.g., only one way to reach any cell in the first row or column).
Transition: For each cell (r, c), the value is derived from its neighbors (usually the cell above and the cell to the left). The specific formula depends on the problem (e.g., sum, min, max, count).
    - Example: dp[r][c] = dp[r-1][c] + dp[r][c-1] for counting paths, or dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c] for minimum path sum problems.
"""
# Templates
def gridDPProblem(m: int, n: int) -> int:
    # Step 1 & 2: Initialize DP table with base cases
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1 # or whatever the starting base case is
    
    # Fill base case edges (if applicable)
    for r in range(1, m):
        dp[r][0] = ... 
    for c in range(1, n):
        dp[0][c] = ...

    # Step 3 & 4: Iterate starting after base cases and apply transition
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1] # Example transition
            
    return dp[m-1][n-1]


def spaceOptimizedGridDP(self, m: int, n: int) -> int:
    # Optimization: Notice that to compute any row, you only need the values from the current row and the previous row.
    # This drops your space complexity to $O(n)$ by keeping just a single 1D array of size $n$ and updating it iteratively
    # Step 1: Initialize a 1D DP array of size n (number of columns)
    # Set base cases for the first row/column depending on the problem
    dp = [1] * n  # Example: 1s for counting paths, or 0s for sums/mins
    
    # Step 2: Iterate through each row starting from the second row (index 1)
    for r in range(1, m):
        # Step 3: Iterate through each column starting from the second column (index 1)
        for c in range(1, n):
            # Step 4: Apply the transition rule using the in-place update trick
            # dp[c] currently holds the value from the ABOVE row.
            # dp[c - 1] holds the newly updated value from the LEFT cell.
            
            # Example for Unique Paths:
            dp[c] += dp[c - 1] 
            
            # (Alternative for Min Path Sum, you would do something like:
            # dp[c] = grid[r][c] + min(dp[c], dp[c - 1]))
            
    # Step 5: The final answer rests in the last element of the 1D array
    return dp[-1]

# LC 62: Unique Paths
def uniquePaths(self, m: int, n: int) -> int:
    # Initialize a 2D DP table with dimensions m x n, filled with 1s
    # Each cell dp[r][c] will represent the number of unique paths to reach that cell from the top-left corner (0, 0)
    dp = [[1] * n for _ in range(m)]

    # start at 1 as there is only one way to reach right and bottom for col and row 1
    # can never come from left or above
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r -1][c] + dp[r][c-1]
    
    return dp[m-1][n-1]

# LC 63: Unique Paths II
# Bottom up:
# Time Complexity O(MxN) where M is number of rows and N is number of columns as we visit each cell once
# Space Complexity O(MxN) where M is number of rows and N is number of
def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
    if not obstacleGrid or obstacleGrid[0][0] == 1:
        return 0

    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [[0] * n for _ in range(m)]
    
    # Initialize the starting point
    dp[0][0] = 1
    
    # Initialize the first column
    # Set it to 1 if reachable,0 if blocked
    for r in range(1, m):
        if obstacleGrid[r][0] == 0 and dp[r - 1][0] == 1:
            dp[r][0] = 1
            
    # Initialize the first row
    # Set it to 1 if reachable,0 if blocked
    for c in range(1, n):
        if obstacleGrid[0][c] == 0 and dp[0][c - 1] == 1:
            dp[0][c] = 1

    for r in range(1, m):
        for c in range(1, n):
            if obstacleGrid[r][c] == 1:
                dp[r][c] = 0
            else:
                dp[r][c] = dp[r -1][c] + dp[r][c-1]
    
    return dp[m-1][n-1]

# Bottom Up: Space Optimized
# Time Complexity O(MxN) where M is number of rows and N is number of columns as we visit each cell once
# Space Complexity O(N) where N is number of columns as we only store the current row
def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
    # Edge case: If the grid is empty or the starting cell is blocked, 
    # there are 0 possible paths to the destination.
    if not obstacleGrid or obstacleGrid[0][0] == 1:
        return 0
    
    # Get the dimensions of the grid (m rows, n columns)
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    
    # Create a 1D array of size n to store path counts for the current row.
    # This optimizes space from O(m * n) to O(n) by only keeping track of the previous row's values.
    dp = [0] * n
    
    # There is 1 way to be at the starting position (0, 0)
    dp[0] = 1
    
    # Iterate through every row and column of the grid
    for r in range(m):
        for c in range(n):
            # If there is an obstacle at the current cell, set the path count to 0.
            if obstacleGrid[r][c] == 1:
                dp[c] = 0
            # If it's a valid cell and not the very first column, 
            # add the paths coming from the left cell (dp[c - 1]) 
            # to the paths coming from the cell above (stored currently in dp[c]).
            elif c > 0:
                dp[c] += dp[c - 1]
                
    # Return the total number of paths to reach the bottom-right corner (n - 1)
    return dp[n - 1]

# DFS with memoization (Top-down DP)
# Space and Time complexity: O(m*n) where m is number of rows and n is number of columns as we visit each cell once
def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
    rows, columns = len(obstacleGrid), len(obstacleGrid[0])
    memo = {}

    def dfs(row, column):
        # Base case: Out of bounds or hit an obstacle
        if row >= rows or column >= columns or obstacleGrid[row][column] == 1:
            return 0
        
        # Base case: Reached the bottom-right destination
        if row == rows - 1 and column == columns - 1:
            return 1
        
        # Check if result is already memoized
        if (row, column) in memo:
            return memo[(row, column)]
        
        # Recurse down and right, then save to memo
        # IMPORTANT: here it is +1 vs in bottom up it is -1 as we are looking back there!!!
        memo[(row, column)] = dfs(row + 1, column) + dfs(row, column + 1)
        
        return memo[(row, column)]

    return dfs(0, 0)

# LC 120: Triangle
"""
Bottom up approach: start solving the problem from the smallest, base-case subproblems (the beginning of the array, houses 0 and 1) and iteratively build your way up to the final answer

State: minimum path sum from r,c to the bottom
Base case: first element in triangle
Transition: dp[row][col] = triangle[row][col] + min(dp[row + 1][col], dp[row + 1][col + 1])

Time: O(N^2)
Space: O(1)
"""
def minimumTotal(self, triangle: list[list[int]]) -> int:
    # in place solution instead of using dp table to achive O(1) space complexity
    # Iterate from bottom (starting at second-to-last row) to top, updating each cell with the minimum path sum to the bottom
    # for each element in the current row, add the minimum of the two adjacent numbers from the row below
    for row in range(len(triangle) - 2, -1 , -1 ):
        for column in range(len(triangle[row])):
            triangle[row][column] = triangle[row][column] + min(triangle[row + 1][column], triangle[row + 1][column + 1])

    return triangle[0][0]



# Graph DFs with memo top down approach
"""
Time: O(N^2)
Space: O(N^2)
"""
def minimumTotal(self, triangle: List[List[int]]) -> int:
    n = len(triangle)
    # Alternatively: 
    # Initialize a 2D memo table matching the triangle's shape with None
    # memo = [[None] * len(row) for row in triangle]
    memo = {}
    
    def dfs(row, col):
        if row == n - 1:
            return triangle[row][col]
        
        if (row, col) in memo:
            return memo[(row, col)]
        
        res = triangle[row][col] + min(dfs(row + 1, col), dfs(row + 1, col + 1))
        memo[(row, col)] = res
        return res
    
    return dfs(0, 0)

# LC 64: Minimum Path Sum
"""
State: min path sum to reach row,col
Transition: grid[row][col] += min(grid[row - 1][col], grid[row][col - 1])
Base case: first row and first column

Space: O(1) if we modify the grid in place, otherwise O(m*n) for a separate dp table
Time: O(m*n) where m is number of rows and n is number of columns as we visit each cell once
"""
def minPathSum(self, grid: list[list[int]]) -> int:
    # Base case 1: Top row can only be reached by going left
    for col in range(1, len(grid[0])):
        grid[0][col] += grid[0][col - 1]

        # Base case 2: First column can only be reached by going down
    for row in range(1, len(grid)):
        grid[row][0] += grid[row - 1][0]

    # Start at second row and column
    for row in range(1, len(grid)):
        for col in range(1, len(grid[0])):
            # We look at how we could have reach this cell which is either from the left or from the top
            grid[row][col] += min(grid[row - 1][col], grid[row][col - 1])
    
    return grid[-1][-1]


def minPathSum(self, grid: list[list[int]]) -> int:
        """ 
        Graph DFS Top down approach with memo.
        Space: O(m*n) as the memoization dictionary stores up to m * n states. 
        Recursion stack space is O(m+n) in the worst case, but this is dominated by the memoization space.
        Time: O(m*n) where m is number of rows and n is number of columns as we visit each cell once
        """
        rows, columns = len(grid), len(grid[0])
        memo = {}

        def dfs(row, col):
            # Base Case: bottom rihgt corner
            if row == rows - 1 and col == columns -1:
                return grid[row][col]
            
            # Base Case: Out of bounds
            if row == rows or col == columns:
                return float('inf')

            # Check if result alread computed
            if (row, col) in memo:
                return memo[(row, col)]
            
            result = grid[row][col] + min(dfs(row + 1, col), dfs(row, col + 1))
            memo[(row, col)] = result

            return result
        
        return dfs(0, 0)

# ----------------Subsequence / String Problems: 2D DP (Leetcode 1143)-----------------------
"""
State: 
Initialize 2d dp with all 0s
Base Case: usually empty string, potentially intit base case in 2d grid if not 0
Transition:
"""
# Longest Common Subsequence (LCS) Problem
def subsequenceProblem(self, text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    
    # 1. Initialize DP table with +1 offset for base cases (empty strings)
    # Size: (m + 1) x (n + 1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 2. (Optional) Initialize base cases if they aren't 0
    # e.g., for Edit Distance, dp[i][0] = i and dp[0][j] = j
    
    # 3. Fill the DP table using nested loops
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            # 4. Check if elements match
            if text1[i - 1] == text2[j - 1]:
                # Match case: typically take diagonal + 1 (or add current weight)
                dp[i][j] = dp[i - 1][j - 1] + 1  # (modify based on problem)
            else:
                # Mismatch/Choice case: typically take max or min of skipping elements
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # (or min for cost problems)
                
    # 5. Return the bottom-right cell containing the final answer
    return dp[m][n]


def spaceOptimizedSubsequence(self, text1: str, text2: str) -> int:
    # 1. Optimization: Ensure text1 is the shorter string 
    # This guarantees the inner array size (and space complexity) is min(m, n)
    if len(text1) > len(text2):
        text1, text2 = text2, text1
        
    m, n = len(text1), len(text2)
    
    # 2. Initialize two 1D arrays instead of a 2D matrix
    # prev represents row i-1, curr represents row i
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    # (Optional) Handle base cases for the first row if needed (e.g., Edit Distance)
    # for j in range(n + 1): prev[j] = j
    
    # 3. Outer loop iterates over the rows
    for i in range(1, m + 1):
        
        # (Optional) Handle base case for the start of the current row if needed
        # curr[0] = i 
        
        # Inner loop iterates over the columns
        for j in range(1, n + 1):
            
            # 4. Apply your transition logic
            if text1[i - 1] == text2[j - 1]:
                # Match case: depends on diagonal value (which was in prev[j-1])
                curr[j] = prev[j - 1] + 1  # (Modify for counting/cost if needed)
            else:
                # Mismatch case: depends on top (prev[j]) and left (curr[j-1])
                curr[j] = max(prev[j], curr[j - 1])  # (Use min for cost problems)
        
        # 5. Shift current row to previous row for the next iteration
        prev = curr[:]  # or prev, curr = curr, [0] * (n + 1)
        
    # 6. The final answer resides at the end of the last processed row
    return prev[n]
    
# Variations
"""
Counting Subsequences (e.g., "Distinct Subsequences")
    Goal: Find how many ways a subsequence can be formed.
    Modification: Instead of max or min, you accumulate (add) the paths. 
    When characters match, you have the choice to use the match or skip the character in the first string.
"""
# Inside the loop:
if text1[i - 1] == text2[j - 1]:
    # Add ways from using the match AND ways from skipping the current char in text1
    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
else:
    # If they don't match, we must skip the character in text1
    dp[i][j] = dp[i - 1][j]

"""
2. Minimum Cost / Operations (e.g., "Edit Distance" / "Minimum ASCII Delete Sum")
    Goal: Find the minimum operations or cost to transform one sequence into another.
    Modification: Change max to min, adjust base cases to account for deletion/insertion costs, and include all choice branches (Insert, Delete, Substitute).
"""

# Base case setup (outside loop):
for i in range(m + 1): dp[i][0] = i  # cost of deleting all chars
for j in range(n + 1): dp[0][j] = j  # cost of inserting all chars

# Inside the loop:
if text1[i - 1] == text2[j - 1]:
    dp[i][j] = dp[i - 1][j - 1]  # No cost if they match
else:
    dp[i][j] = 1 + min(
        dp[i - 1][j],     # Deletion
        dp[i][j - 1],     # Insertion
        dp[i - 1][j - 1]  # Substitution
    )

"""
3. Single Sequence Problems (e.g., "Longest Increasing Subsequence")
    Goal: Find patterns within a single array (no second string to compare against).
    Modification: Drop the 2D grid entirely. Use a 1D array where dp[i] represents the answer ending at index i, and loop backward through previous elements.
"""

# 1D Table initialization
dp = [1] * n  # Base case: every element is a subsequence of length 1

for i in range(1, n):
    for j in range(i):
        if text[i] > text[j]:  # Condition (e.g., increasing)
            dp[i] = max(dp[i], dp[j] + 1)
            
return max(dp)

"""
4. Interval / Palindrome Subsequences (e.g., "Longest Palindromic Subsequence")
    Goal: Find subsequences inside a string by shrinking or expanding an interval (i, j).
    Modification: Instead of prefixes, your loops manage interval lengths from start (i) to end (j).
"""

# dp[i][j] = longest palindromic subsequence between index i and j
dp = [[0] * n for _ in range(n)]
for i in range(n): dp[i][i] = 1  # Base case: single letters are palindromes of length 1

# Iterate by length of the interval
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if text[i] == text[j]:
            dp[i][j] = dp[i + 1][j - 1] + 2
        else:
            dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

return dp[0][n - 1]

# LC 72: Edit Distance
"""
State: The minimum number of operations required to convert the first i characters of word1 into the first j characters of word2.
Base case: one string is empty 
Minimum number of operations to get from horse to ros?
         " "  r    o   s
    " "   0   1    2   3
    h     1   1    2   3
    o     2   2    1   2
    r     3   2    2   2
    s     4   3    3   2
    e     5   4    4   3
"""
def minDistance(self, word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # Initialize a 2D DP array with dimensions (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base case empty string: filling the first row and first column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    # Fill the DP table
    # need to do +1 as we added empty string, start at second row and column
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # if characters match then cary over cost from last cell
            # need to do -1 to get right chars
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            # otherwise min of 3 possible operations
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Delete / move above
                    dp[i][j - 1],    # Insert / move left
                    dp[i - 1][j - 1] # Replace / move diagonal above left
                )
                
    return dp[m][n]

def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        
        # Instead of a 2D grid, we just keep track of two rows:
        # 'prev_row' starts as the base case for row 0 (0, 1, 2, ..., n)
        prev_row = list(range(n + 1))
        
        for i in range(1, m + 1):
            # Create a new row for the current step, starting with [i]
            curr_row = [i] + [0] * n
            
            for j in range(1, n + 1):
                # need -1 to account for additional row we added for base case
                if word1[i - 1] == word2[j - 1]:
                    curr_row[j] = prev_row[j - 1]
                else:
                    curr_row[j] = 1 + min(
                        prev_row[j],     # Delete (comes from row above)
                        curr_row[j - 1], # Insert (comes from left in current row)
                        prev_row[j - 1]  # Replace (comes from diagonal above-left)
                    )
            
            # Move curr_row to prev_row for the next loop iteration
            prev_row = curr_row
            
        # The final answer is the last number in our final row
        return prev_row[n]

# ==========================================================
# Memoization with DFS (Top-Down DP)
# ==========================================================
# Memoization with DFS
"""
Think of memoization as keeping a cheat sheet (usually a 2D array or a hash map).
    Check the cache: Before doing any work at cell (r, c), look at your cheat sheet to see if you've already calculated the answer for this cell. If you have, immediately return that saved value.
    Compute if missing: If it's not in the cheat sheet, run your normal DFS logic (explore down and right).
    Save to the cache: Before returning the final result for cell (r, c), save it to your cheat sheet so you never have to calculate it again.
"""
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Step 1: Create a memoization table (cheat sheet) initialized to -1
        memo = [[-1] * n for _ in range(m)]
        
        def dfs(r, c):
            # Base Case 1: Out of bounds
            if r == m or c == n:
                return 0
            
            # Base Case 2: Reached destination
            if r == m - 1 and c == n - 1:
                return 1
            
            # Step 2: Check if we've already solved this subproblem
            if memo[r][c] != -1:
                return memo[r][c]
            
            # Step 3: Compute the result normally (DFS branches)
            move_down = dfs(r + 1, c)
            move_right = dfs(r, c + 1)
            
            # Step 4: Save the result in the memo table before returning
            memo[r][c] = move_down + move_right
            return memo[r][c]

        return dfs(0, 0)
