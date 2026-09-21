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

# --- Summary of Time Complexities (Singly Linked List) ---
# Traversal:                O(N)
# Insertion (Beginning):    O(1)
# Insertion (End):          O(N)
# Deletion (Value):         O(N)
# Search:                   O(N)

Useful tips:
- When creating a new linked list we might have to creat a dummy head to which we can link the new nodes then we return dummy_head.next
- Should check for empty head as edge case
"""
# Delete from a Linked List
def delete_by_value(head, key):
    if not head:
        print("List is empty.")
        return head

    # If head is the node to be deleted
    if head.data == key:
        return head.next

    current = head
    prev = None
    while current and current.data != key:
        prev = current
        current = current.next

    if not current:
        print(f"Value {key} not found in the list.")
        return head

    prev.next = current.next
    return head

# Insert into Linked List
def insert_at_position(head, position, data):
    """
    Inserts a new node with the specified data at a given 0-indexed position.
    Returns the updated head of the linked list.
    """
    new_node = Node(data)

    # Case 1: Insert at the head (position 0)
    if position == 0:
        new_node.next = head
        return new_node

    # Traverse to the node *before* the target position
    current = head
    count = 0
    while current and count < position - 1:
        current = current.next
        count += 1

    # If the position is out of bounds
    if not current:
        print("Position out of range.")
        return head

    # Insert the new node
    new_node.next = current.next
    current.next = new_node

    return head

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

# Copy Linked List
def copyLinkedList(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return None
    
    # Dummy head to help build the new list
    dummy_head = ListNode(0)
    curr_new = dummy_head
    
    # Traverse the original list and copy each node
    while head:
        curr_new.next = ListNode(head.val)
        curr_new = curr_new.next
        head = head.next
        
    return dummy_head.next

# Cycle detection in Linked List (LC 141)
# Note: a linked list can only have one cycle
"""
Floyd's Cycle-Finding Algorithm (Tortoise and Hare)
Strategy: Use two pointers starting at the head: a slow pointer (moves 1 step at a time) and a fast pointer (moves 2 steps at a time).
Why it works: If there is no cycle, the fast pointer will straightforwardly reach null. 
If a cycle exists, the fast pointer loops around and eventually catches up to the slow pointer from behind, 
meaning they will point to the exact same node object (slow == fast). 
Where they intersect is random point NOT necessarily start or end of cycle.

Time complexity: O(n)
Space complexity: O(1)
"""
def hasCycle(self, head: Optional[ListNode]) -> bool:
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next          # Moves 1 step
        fast = fast.next.next     # Moves 2 steps
        
        if slow == fast:
            return True           # Cycle detected
            
    return False                  # Reached end of list (no cycle)


# Detect Cycle in Linked List and find start as well as end of cycle
"""
1. Finding the Start of the Cycle
Once the slow and fast pointers meet inside the cycle (detecting that a cycle exists), you can find the exact entrance node by:
    Leave one pointer at the meeting point and reset the other pointer back to the head of the linked list.
    Move both pointers forward one step at a time.
    The exact node where they meet again is the start of the cycle.

2. Finding the End of the Cycle
Once you have located the start node of the cycle:
    Start a traversal pointer at the start node.
    Follow the .next pointers until you reach the node whose .next pointer points back to that start node.
    That final node is the end of the cycle.
"""
def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Step 1: Detect if cycle exists and find meeting point
    slow = head
    fast = head
    has_cycle = False
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break
            
    if not has_cycle:
        return None # No cycle, so no start/end
        
    # Step 2: Find the Start of the Cycle
    pointer = head
    while pointer != slow:
        pointer = pointer.next
        slow = slow.next
    cycle_start = pointer # This is the start of the cycle
    
    # Step 3: Find the End of the Cycle
    current = cycle_start
    while current.next != cycle_start:
        current = current.next
    cycle_end = current # This is the end of the cycle
    
    return cycle_start # (Or return both depending on your needs)


# Delete every other node in Linked List Cycle
def deleteEveryOtherNodeInCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head
        
    # Step 1: Detect cycle and find meeting point (Floyd's Algorithm)
    slow, fast = head, head
    has_cycle = False
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break
            
    if not has_cycle:
        return head  # No cycle, return original list
        
    # Find the exact start of the cycle
    pointer = head
    while pointer != slow:
        pointer = pointer.next
        slow = slow.next
    cycle_start = pointer
    
    # Step 2: Delete every other node on the fly
    curr = cycle_start
    while curr and curr.next != cycle_start:
        # Bypass the next node (delete it)
        curr.next = curr.next.next
        
        # Move curr to the next kept node
        curr = curr.next
        
        # Stop if we've wrapped back around to the start
        if curr == cycle_start:
            break
            
    return head


# LC 2: Add Two Numbers
"""
Time Complexity: O(max(N, M)), where N and M are the lengths of the two linked lists. 
We traverse both lists at most once.
Space Complexity: O(max(N, M)), as the length of the new list is at most max(N, M) + 1.
"""
def addTwoNumbers(self, l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    # Create a dummy head of new linked list so we can link results to it
    dummy_head = ListNode(0)
    # Assign dummy head to current ot leave it unchanged
    current = dummy_head
    # Amount to carry over
    carry = 0

    while l1 or l2 or carry:
        l1_val = l1.val if l1 else 0 
        l2_val = l2.val if l2 else 0
        
        # Calculate carray over and total
        total = l1_val + l2_val + carry
        carry = total // 10
        new_digit = total % 10

        # Add the new node
        current.next = ListNode(new_digit)

        # Advance the pointer in the new linked list we are building
        current = current.next
        # Advance l1 and l2 pointers if we have not reached the end
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    
    # return head of the new list. need to inlcude dummy head
    return dummy_head.next

# LC 138: Copy List with Random Pointer
"""
Time Complexity: O(N)
We iterate through the linked list twice: once to create all the nodes and populate the hash map, and a second time to assign the `next` and `random` pointers. Since $N$ is the number of nodes in the linked list, this takes linear time.

Space Complexity: O(N)
We use a hash map (`old_to_new`) to store the mapping between each original node and its corresponding cloned node. Because we store $N$ key-value pairs, the extra space required grows linearly with the size of the input list.
"""
def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
    if not head:
        return None
    
    # Dictionary to hold the mapping from original node to copied node
    old_to_new = {}
    
    # First pass: Create all the cloned nodes (without pointers yet)
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next
        
    # Second pass: Connect the next and random pointers
    # This is needed as they cannot point at previous linked list
    # Hence need to first create new linked list and then add references
    curr = head
    while curr:
        if curr.next:
            old_to_new[curr].next = old_to_new[curr.next]
        if curr.random:
            old_to_new[curr].random = old_to_new[curr.random]
        curr = curr.next
        
    # Return the head of the cloned list
    return old_to_new[head]

# LC 138: Copy List with Random Pointer (Space O(1))
"""
To achieve O(1) extra space, you can avoid using a hash map entirely by interweaving the cloned nodes directly into the original linked list.
This allows you to find the correct random pointer locations implicitly through adjacent node relationships.

The Three-Step AlgorithmInterweave Clones: 
1. Traverse the original list and insert a cloned node right after each original node. 
For example, if your list is A -> B, it becomes A -> A' -> B -> B'.
2. Assign Random Pointers: Traverse the list again. Since every original node's clone is right next to it (curr.next), 
you can set the clone's random pointer using: curr.next.random = curr.random.next.
3. Restore and Separate: Separate the interweaved list back into two independent lists: the original list and the cloned list.
"""
def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
    if not head:
        return None
    
    # Step 1: Create cloned nodes and interweave them with the original list
    curr = head
    while curr:
        clone = Node(curr.val, curr.next)
        curr.next = clone
        curr = clone.next
        
    # Step 2: Assign random pointers for the cloned nodes
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
        
    # Step 3: Separate the original list from the cloned list
    curr = head
    dummy_head = Node(0)
    copy_curr = dummy_head
    
    while curr:
        # Extract the clone
        copy_curr.next = curr.next
        copy_curr = copy_curr.next
        
        # Restore the original list
        curr.next = curr.next.next
        curr = curr.next
        
        return dummy_head.next