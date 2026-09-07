"""
Key Python operations: Linked Lists.
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


"""
A linked list is a linear data structure where elements (nodes) are stored in
non-contiguous memory locations. Each node contains two parts:
1. Data: The value stored in the node.
2. Next: A reference (or pointer) to the next node in the sequence.
"""
# Find the middle of the linked list using slow and fast pointers
slow = head
fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

# Traverse to the end of the linked list
while head and head.next:
    head = head.next

# Reverse a linked list
def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        current = head

        while current:
            nxt = current.next      # 1. Save the next node
            current.next = prev     # 2. Reverse the current node's pointer
            prev = current          # 3. Move prev forward (fixed order)
            current = nxt           # 4. Move current forward
        
        return prev                 # Return the new head of the reversed list

# Iterate through both halves simultaneously and find max twin sum
max_sum = 0
first_half = head
second_half = prev  # 'prev' is the new head of the reversed second half

while second_half:
    current_sum = first_half.val + second_half.val
    max_sum = max(max_sum, current_sum)
    
    first_half = first_half.next
    second_half = second_half.next

# --- Summary of Time Complexities (Singly Linked List) ---
# Traversal:                O(N)
# Insertion (Beginning):    O(1)
# Insertion (End):          O(N)
# Deletion (Value):         O(N)
# Search:                   O(N)

