"""
Key Python operations: Stacks & Queues.
"""

# ==========================================================
# Queues
# ==========================================================
# deque
# Important: left end is front of queue
# Unlike stack where right end is top

# ==========================================================
# Stack
"""
- Useful when we need to evaluate sequences in LIFO
- When I am given a sequence then most likely need to iterate through it and based on conditions append or pop from stack.
Stack will hold my result e.g. LC 150, 71
- Might need to combine wiht hasmap where I need to match pairs e.g. opening and closing brackets such as LC 5
- In some cases might need while loop within for loop where I need to modify stack until certain condition is met i.e. remove multiple elements (see LC 735)
"""
# ==========================================================
# Basic Stack Using List

# Initialize a stack
stack = []

# 1. Push items onto the stack
stack.append(10)
stack.append(20)
stack.append(30)
print("Stack after pushes:", stack)  # Output: [10, 20, 30]

# 2. Peek at the top item
print("Top item (Peek):", stack[-1])  # Output: 30

# 3. Pop an item from the stack
removed_item = stack.pop()
print("Popped item:", removed_item)     # Output: 30
print("Stack after pop:", stack)      # Output: [10, 20]

# 4. Check if empty
if not stack:
    print("Stack is empty")
else:
    print("Stack is not empty")

# 5. Get the size
print("Stack size:", len(stack))        # Output: 2

# Basic Stack Using Deque (from collections)
from collections import deque

# Initialize a deque as a stack
stack = deque()

# Push items
stack.append('a')
stack.append('b')
stack.append('c')

# Peek
print("Top:", stack[-1])  # Output: c

# Pop items
print("Popped:", stack.pop())  # Output: c
print("Remaining stack:", list(stack))  # Output: ['a', 'b']

# Monotonic Stack:
"""
A monotonic stack is a stack whose elements are kept in a specific order—either strictly increasing or strictly decreasing. 
As you iterate through a dataset, you pop elements from the stack that violate this order before pushing the new element.
Monotonically Increasing Stack: Elements from bottom to top are in increasing order (smallest to largest). 
Used to find the next smaller element.
Monotonically Decreasing Stack: Elements from bottom to top are in decreasing order (largest to smallest). 
Used to find the next greater element.

Time and Space Complexity: O(n) for both, where n is the number of elements in the input list. 
Each element is pushed and popped at most once.
"""

# Monotonically Decreasing Stack (next greater element)
def next_greater_element(nums):
    """
    Finds the next greater element for each number in the array.
    For each element, it looks to its right for the first element that is strictly greater.
    If no such element exists, it defaults to -1.
    """
    n = len(nums)
    
    # Initialize the result array with -1. 
    # Any element that doesn't find a larger element to its right will remain -1.
    result = [-1] * n
    
    # Initialize an empty stack. 
    # We store indices rather than values so we can easily update the result array.
    stack = []  

    # Iterate through every element in the array by its index
    for i in range(n):
        # Maintain a monotonically decreasing stack (from bottom to top).
        # While the stack is not empty AND the current element (nums[i]) 
        # is STRICTLY GREATER THAN the element at the index sitting at the top of the stack:
        while stack and nums[i] > nums[stack[-1]]:
            # Pop the index from the stack because we have found its next greater element
            idx = stack.pop()
            
            # The current element (nums[i]) is the first greater element 
            # for the element located at 'idx'
            # result contains the actual number i.e. the next greater element for the number at index 'idx'
            result[idx] = nums[i]  
        
        # Push the current index onto the stack. 
        # It will wait here until a greater element to its right is encountered.
        stack.append(i)

    return result

# Example usage:
# nums = [2, 1, 2, 4, 3]
# print(next_greater_element(nums))  # Output: [4, 2, 4, -1, -1]

# Monotonically Increasing Stack (next smaller element)
def next_smaller_element(nums):
    """
    Finds the next smaller element for each number in the array.
    For each element, it looks to its right for the first element that is strictly smaller.
    If no such element exists, it defaults to -1.
    """
    n = len(nums)
    # Initialize the result array with -1. 
    # Any element that doesn't find a smaller element to its right will remain -1.
    result = [-1] * n
    
    # Initialize an empty stack. 
    # We store indices rather than values so we can easily update the result array.
    stack = []  

    # Iterate through every element in the array by its index
    for i in range(n):
        # Maintain a monotonically increasing stack.
        # While the stack is not empty AND the current element (nums[i]) 
        # is STRICTLY LESS THAN the element at the index sitting at the top of the stack:
        while stack and nums[i] < nums[stack[-1]]:
            # Pop the index from the stack because we have found its next smaller element
            idx = stack.pop()
            
            # The current element (nums[i]) is the first smaller element 
            # for the element located at 'idx'
            result[idx] = nums[i]  
        
        # Push the current index onto the stack. 
        # It will wait here until a smaller element to its right is encountered.
        stack.append(i)

    return result

# Example usage:
# nums = [4, 8, 5, 2, 25]
# print(next_smaller_element(nums))  # Output: [2, 5, 2, -1, -1]

# LC 155: Min Stack
# Time complexity: O(1)
# Space complexity: O(N)
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # If min_stack is empty or val is smaller/equal to current min, push val
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
        else:
            self.min_stack.append(self.min_stack[-1])

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1] if self.stack else None

    def getMin(self) -> int:
        return self.min_stack[-1] if self.min_stack else None


# LC 71
def simplifyPath(self, path: str) -> str:
        # Initialize a stack to keep track of valid directory names. 
        # A stack works perfectly here because '..' requires us to 
        # step back to the most recently entered directory (LIFO).
        stack = []
        
        # Split the input path string by '/' into individual components.
        # For example, "/a/./b/../../c/" splits into:
        # ['', 'a', '.', 'b', '..', '..', 'c', '']
        components = path.split('/')
        
        # Iterate through every directory or special token in the split list
        for comp in components:
            # Case 1: '..' means go up one directory level
            if comp == '..':
                # If the stack is not empty, pop the top element to move up
                if stack:
                    stack.pop()
            
            # Case 2: Process valid directory names
            # 'comp and comp != "."' filters out:
            # - Empty strings '' (caused by consecutive slashes like '//' or leading/trailing slashes)
            # - Current directory symbols '.' (which mean stay in place)
            elif comp and comp != '.':
                # Valid directory name; push it onto the stack
                stack.append(comp)
                
        # Reconstruct the canonical path by joining all remaining stack elements with '/'
        # Prepend a leading '/' to ensure it forms a valid absolute path.
        # If the stack is empty, this simply evaluates to '/'.
        return '/' + '/'.join(stack)

# LC 150
def evalRPN(self, tokens: list[str]) -> int:
    """
    Time and space: O(n)
    """
    stack = []

    for token in tokens:
        if token not in {"+", "-", "*", "/"}:  # Using a set is slightly faster for lookups
            stack.append(int(token))
        else:
            right = stack.pop()
            left = stack.pop()
            
            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            else:
                # int() truncates toward zero, matching problem requirements
                result = int(left / right) 
            
            stack.append(result)
    
    return stack[-1]

# LC 5
def isValid(self, s: str) -> bool:
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        
        for char in s:
            if char in mapping:
                # Pop the top element if stack is not empty, else assign a dummy value
                top_element = stack.pop() if stack else '#'
                
                # If the mapped opening bracket doesn't match the stack's top
                if mapping[char] != top_element:
                    return False
            else:
                # It's an opening bracket, push to stack
                stack.append(char)
                
        # If stack is empty, all brackets matched correctly
        return not stack

# LC 735
"""
input: asteroides
output: asteroids after collision
cases: all negative, all positive, empty, same numbers
Approach:
Remove if:
- current element negative and greater then previous positive element
- current neagtive and previous positive are equal remove both

"""
def asteroidCollision(self, asteroids: List[int]) -> List[int]:
    stack = []

    for asteroid in asteroids:
        # current astroid needs to be negative and previous one positive to collide
        while stack and asteroid < 0 < stack[-1]:
            # If current is bigger then previous then previous one is being destroyed
            if abs(asteroid) > stack[-1]:
                stack.pop()
                continue
            # both have the same size then both get destroyed i.e. pop previous one and do not add current one
            elif abs(asteroid) == stack[-1]:
                stack.pop()
            break
        else:
            stack.append(asteroid)
        

    return stack

# LC 2390
"""
Input: string
Output: string
Cases:
Brute Force: load string into list and count all stars, iterate through string and remove star if element left to it is not a star otherwise keep moving, reduce star count by one for each removal, continue until star count is 0, join output into string
Optimal: iterate through string, add each character to the stack, for each star pop char from stack
"""
def removeStars(self, s: str) -> str:
    stack = []

    for char in s:
        if char != "*":
            stack.append(char)
        else:
            stack.pop()
    
    return "".join(stack)

# LC 394
def decodeString(self, s: str) -> str:
    count_stack = []
    string_stack = []
    
    current_string = ""
    k = 0
    
    for char in s:
        if char.isdigit():
            # Handle multi-digit numbers (e.g., "12" instead of just "1" and "2")
            k = k * 10 + int(char)
        elif char == '[':
            # Push the current state onto the stacks and reset for the inner scope
            count_stack.append(k)
            string_stack.append(current_string)
            k = 0
            current_string = ""
        elif char == ']':
            # Pop the previous string and repeat count, then decode the current segment
            prev_string = string_stack.pop()
            repeat_times = count_stack.pop()
            current_string = prev_string + (current_string * repeat_times)
        else:
            # Append normal letters to the current working string
            current_string += char
            
    return current_string