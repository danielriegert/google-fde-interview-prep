"""
Key Python operations: Dynamic Programming.
Covers 1D DP, 2D DP (grid and subsequence problems), and top-down memoization.
"""

# ==========================================================
# DP 1D
# ==========================================================
"""
Important: Instead of asking "Where can I go from here?", dynamic programming asks "How could I have possibly arrived here?"
When problem can be thought of decision tree. DP is a clever way to solve that tree without actually building it or recalculating duplicate branches.
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
"""

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

# ==========================================================
# DP 2D
# ==========================================================
"""
Can think of it as graph. DP optimized way of solving it.
Brute force: DFS with memoization. DP: Bottom up tabulation.
"""
# ----------------Grid Problems: 2D DP-----------------------
# See Leetcode 62. Unique Paths
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

# ----------------Subsequence Problems: 2D DP (Leetcode 1143)-----------------------
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
