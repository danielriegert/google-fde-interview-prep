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

