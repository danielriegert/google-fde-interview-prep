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
- Should ask if linked list can have a cycle
- in most cases assingn head to new variable e.g. current = head as we need the unmodified head
- use dummy node to handle head edge cases like remnoving head
- be creaful with mutation e.g. LC 234. cannot jsut reverse entire list and compare against original as I am mutating the linked list
- pay attention when using for loop what to set for range. often need to subtract 1.
 Also remember for loop is 0 indexed and upper range not inclusive whereas linked list is 1 indexed
- In some scenarios we might want to link the tail wiht the head of the list and then break it again at the new tail e.g. LC 61
"""
# Delete from a Linked List
def delete_by_value(head, key):
    if not head:
        print("List is empty.")
        return head

    # If head is the node to be deleted
    if head.data == key:
        return head.next

    # Init current and previous
    current = head
    prev = None
    while current and current.data != key:
        prev = current
        current = current.next

    # if value is not found
    if not current:
        print(f"Value {key} not found in the list.")
        return head

    # if we find value it will be at current. so we point pre.next at the element after current i.e. current.next
    prev.next = current.next
    return head

# LC 83:
# This removes dupes so that there are only unique values e.g. 1,2,2,3 -> 1,2,3
def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
    if not head:
        return None
        
    prev = head
    current = head.next
    
    while current:
        if current.val == prev.val:
            # Duplicate found: bypass it using prev
            prev.next = current.next
        else:
            # Unique node found: move prev forward to it
            prev = current
            
        # Always move current forward to check the next node
        current = current.next
        
    return head

# LC 82
# This removes ALL elements that are duplicates e.g. 1,2,2,3 -> 1,3
def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
    # need dummy node to handle head edge cases
    dummy = ListNode(0, head)
    prev = dummy
    
    current = head
    while current:
        # Check if it's the start of a duplicate sub-sequence
        if current.next and current.val == current.next.val:
            # Skip all nodes with the same value
            while current.next and current.val == current.next.val:
                current = current.next
            # Link prev to the node after the duplicates
            prev.next = current.next
        else:
            # No duplicate, move prev forward
            prev = prev.next
            
        current = current.next
        
    return dummy.next

# LC 19
def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
    """
    By moving fast n steps ahead first, the distance between fast and slow is always n nodes.
    When fast.next reaches the end of the list, slow is sitting directly before the node that needs to be deleted.
    The dummy node ensures that if head itself is deleted, dummy.next correctly points to the new head of the list
    Time: O(n)
    Space: O(1)
    """
    # Use a dummy node to handle edge cases (like removing the head)
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy

    # 1. Move fast n steps ahead to create the gap
    for _ in range(n):
        fast = fast.next

    # 2. Move both pointers until fast reaches the end
    # need to include fast.next to avoid None with slow.next.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next

    # 3. Skip the target node
    slow.next = slow.next.next

    return dummy.next

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
# if it has cycle then might not finish
slow = head
fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

# Traverse to the end of the linked list
# if we don#t do and head.next last value of head will be None
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


# LC 92
def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        """
        Time: O(n)
        Space: O(1)
        """
        if not head or left == right:
            return head

        # Use a dummy node to handle edge cases where left == 1
        dummy = ListNode(0, head)
        prev_node = dummy

        # 1. Move prev_node to the node just before the 'left' position
        for _ in range(left - 1):
            prev_node = prev_node.next

        # 2. 'current' will point to the first node of the sublist to reverse
        current = prev_node.next
        
        # 3. Reverse the sublist from left to right
        prev = None
        for _ in range(right - left + 1):
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        # 4. Reconnect the reversed sublist with the rest of the list
        # prev is now the new head of the reversed section
        # prev_node.next was the old start of the section (now points to the node after 'right')
        # the old head of the list is now the tail
        tail = prev_node.next
        # connect the tail of the list with the next element after right
        tail.next = current
        # connect the element before left with the new head of the list
        prev_node.next = prev

        return dummy.next

# LC 61
def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:
    if not head or not head.next or k == 0:
        return head
    
    # Step 1: Find the length and the tail
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1
        
    # Step 2: Handle cases where k is a multiple of length
    k = k % length
    if k == 0:
        return head
    
    # Step 3: Make it a circular linked list
    tail.next = head
    
    # Step 4: Find the new tail (length - k steps from head) and subtract 1
    steps_to_new_tail = length - k - 1
    new_tail = head
    for _ in range(steps_to_new_tail):
        new_tail = new_tail.next
        
    # Step 5: Break the circle and get the new head
    new_head = new_tail.next
    new_tail.next = None
    
    return new_head


# LC 86
def partition(self, head: ListNode | None, x: int) -> ListNode | None:
    """
    1. Init dummy heads for smaller and larger sub linked lists
    2. Iterate through current list and link elements to sub lists
    3. Terminate larger sub list to make sure no cycles
    4. Link lists together
    """
    # Create dummy heads for the two partitions
    smaller_head = ListNode(0, None)
    larger_head = ListNode(0, None)

    current = head
    larger_current = larger_head
    smaller_current = smaller_head
    while current:
        if current.val < x:
            smaller_current.next = current
            smaller_current = current
        else:
            larger_current.next = current
            larger_current = current
        current = current.next

    # Terminate the greater list to avoid cycles
    larger_current.next = None
    # Link the lists together
    smaller_current.next = larger_head.next

    return smaller_head.next

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

# LC 239
"""
Can NOT reverse entire list and then compare as I would mutate the list.
Would have to copy it instead e.g. copy nodes or iterate linked list and store all values in array.
Right approach:
- Find middle of linked list
- Reverse one half
- Compare the two halfs
Time: O(n)
Space: O(1)
"""
def isPalindrome(self, head: ListNode | None) -> bool:
    # Step 1: Find the middle of the linked list
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Reverse the second half of the list
    prev = None
    while slow:
        nxt = slow.next
        slow.next = prev
        prev = slow
        slow = nxt
    
    # Step 3: Compare the first half and the reversed second half
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
        
    return True