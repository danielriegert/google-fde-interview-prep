"""
Key Python operations: Trees.
Covers DFS/BFS traversal, BST operations, general tree helpers, and Tries.
"""
# ==========================================================
# Trees - Types
# ==========================================================
"""
- Perfect Binary Tree	All internal nodes have two children, and all leaves are at the exact same depth (every level is completely full)
- Complete Binary Tree	Every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible.
- Balanced Binary Tree	The height difference between the left and right subtrees of any node is at most 1, and all subtrees are also balanced
- Skewed (Degenerate) Tree	Every parent node has only one child, causing the tree to lean entirely to one side (essentially a linked list).
"""
# ==========================================================
# Trees - Edge Cases
# ==========================================================
"""
- **Empty tree (`root = None`):** The tree has no nodes. The algorithm should immediately handle this and return an empty list `[]` without throwing errors.
- **Single-node tree:** The tree only contains the root node (`root.val = 1`, no left or right children). The output should be `[[1]]`.
- **Skewed tree (Left-heavy or Right-heavy):** Every node only has a left child or only has a right child (essentially a linked list). 
    The algorithm needs to correctly alternate directions level by level even when each level has a width of exactly 1.
- **Complete/Balanced binary tree:** A tree where all levels are fully populated. This tests the core alternating logic across multiple levels (e.g., Level 0 left-to-right, Level 1 right-to-left, Level 2 left-to-right).
- **Unbalanced or asymmetric tree:** A tree where some subtrees are deeper than others, resulting in varying queue sizes and level counts across different branches.
"""

from typing import List, Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ==========================================================
# Tree General Operations
# ==========================================================
# Get node count of tree using dfs
def count_nodes(root):
    if not root:
        return 0

    left_count = count_nodes(root.left)
    right_count = count_nodes(root.right)

    return left_count + 1 + right_count
# Example
#    1
# 2     3

# add 1 to call stack, call f on 2, explore left and right of 2 which are both None,
# now we hit return left_count + 1 + right_count = 0 + 1 + 0 = 1, return to call stack for 1, 
# now call f on 3, explore left and right of 3 which are both None,
# now we hit return left_count + 1 + right_count = 0 + 1 + 0 = 1
# now return to call stack for 1, we have explored both left (1) and right (1) of 1, 
# so return left_count + 1 + right_count = 1 + 1 + 1 = 3


# Get height of a binary tree using dfs
def get_tree_height(root):
    if not root:
        return 0

    left_height = get_tree_height(root.left)
    right_height = get_tree_height(root.right)

    return max(left_height, right_height) + 1

# Get height of a complete binary tree. A complete binary tree is a binary tree in which every level, except possibly the last, is completely filled, and all nodes are as far left as possible.
# Can just traverse down the leftmost path to get the height, since all levels are filled except possibly the last.
# Time complexity: O(log n) where n is the number of nodes in the tree.
def get_complete_tree_height(root):
    height = 0
    while root:
        height += 1
        root = root.left
    return height

# Count nodes in a complete binary tree. A complete binary tree is a binary tree in which every level, except possibly the last, is completely filled, and all nodes are as far left as possible.
# Time complexity: O(log^2 n)
# Space complexity: O(log n)
# Leetcode 222. Count Complete Tree Nodes
def countNodes(self, root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    def get_height(node, go_left):
        h = 0
        while node:
            h += 1
            node = node.left if go_left else node.right
        return h
    
    left_height = get_height(root, True)
    right_height = get_height(root, False)
    
    # If left and right heights are equal, the subtree is a "perfect" binary tree i.e. (every level is completely filled).
    if left_height == right_height:
        # formula for the total number of nodes in a perfect binary tree of height h.
        return 2**left_height - 1
    
    # Otherwise, recurse on left and right subtrees + 1 for the current root
    return 1 + self.countNodes(root.left) + self.countNodes(root.right)

# LC 236
# Use post order traversal i.e. left, right, root.
# Time complexity O(n) where n is the number of nodes in the tree.
# Space complexity O(h) where h is the height of the tree.
def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Base case: if root is null, or we found p or q
        if not root or root == p or root == q:
            return root
        
        # Recursively search left and right subtrees
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        
        # If both left and right are non-null, p and q are on separate sides; root is the LCA
        if left and right:
            return root
        
        # Otherwise, return the non-null child (or null if both were null)
        # p and q are on the same side of the tree are good one we found one as guranteed 
        # that the other one is in the same subtree, so we return the non-null child.
        return left if left else right

# ==========================================================
# Trees - DFS (Depth-First Search)
# ==========================================================
"""
Depth-First Search (DFS) is a graph and tree traversal algorithm that explores as deep as possible along each branch before backtracking.
In a binary tree, a DFS traversal visits a node, dives into its left subtree until it hits a leaf (or null), backtracks, 
and then dives into its right subtree. Depending on the problem, you can process nodes in different orders (Pre-order, In-order, Post-order)

        4
       / \
      2   5
     / \   
    1   3

Time Complexity: O(n) - Each node is visited exactly once.
Space Complexity: O(h) - The maximum depth of the recursion stack is equal to the height

For a balanced binary tree, the height is O(log N), making the space complexity logarithmic.
For a skewed binary tree (resembling a linked list), the height equals the number of nodes (H = N), resulting in a worst-case space complexity of O(N).
"""

# Recursive DFS - In-Order (Left -> Root -> Right)
# Order of visiting: Go all the way to the leftmost leaf first, process it, process its parent, then visit its right child.
# Output: [1, 2, 3, 4, 5]
def inorder_recursive(root):
    if not root:
        return
    
    inorder_recursive(root.left)   # 1. Traverse left
    print(root.val)                # 2. Process root
    inorder_recursive(root.right)  # 3. Traverse right

class Solution:
    def in_order_traversal(self, root: Optional[TreeNode], result: List[int]):
        if not root:
            return
        
        self.in_order_traversal(root.left, result)
        result.append(root.val)
        self.in_order_traversal(root.right, result)

    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        elements = []
        self.in_order_traversal(root, elements)

        return elements[k - 1]

# Recursive DFS - Pre-Order (Root -> Left -> Right)
# Order of visiting: Process the current node first, then go down the left branch completely, then the right branch.
# Output: [4, 2, 1, 3, 5]
def preorder_recursive(root):
    if not root:
        return
    
    print(root.val)                # 1. Process root
    preorder_recursive(root.left)  # 2. Traverse left
    preorder_recursive(root.right) # 3. Traverse right

# Recursive DFS - Post-Order (Left -> Right -> Root)
# Order of visiting: Process both children completely before touching their parent node. The root is always printed last.
# Output: [1, 3, 2, 5, 4]
def postorder_recursive(root):
    if not root:
        return
    
    postorder_recursive(root.left)  # 1. Traverse left
    postorder_recursive(root.right) # 2. Traverse right
    print(root.val)                 # 3. Process root

# Iterative DFS using Stack - In-Order
def inorder_iterative(root):
    stack = []
    current = root

    while stack or current:
        # Reach the leftmost node of the current node
        while current:
            stack.append(current)
            current = current.left
        
        # Current must be None at this point, so we pop from the stack
        current = stack.pop()
        print(current.val)  # Process the node
        
        # Now, we need to visit the right subtree
        current = current.right

# Iterative DFS using Stack - Pre-Order
def preorder_iterative(root):
    if not root:
        return
    
    stack = [root]

    while stack:
        current = stack.pop()
        print(current.val)  # Process the node
        
        # Push right child first so that left is processed first
        if current.right:
            stack.append(current.right)
        if current.left:
            stack.append(current.left)

# Iterative DFS using Stack - Post-Order
def postorder_iterative(root):
    if not root:
        return []
        
    stack = [root]
    output = []
    
    while stack:
        node = stack.pop()
        output.append(node.val)
        
        # Push left first, then right. 
        # (Since stack is LIFO, right gets processed/popped next)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
            
    # Reverse the output to get Left -> Right -> Root
    return output[::-1]

# DFS with prefix sum and backtracking
def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # Dictionary to store the count of prefix sums encountered so far
        prefix_sums = {0: 1}
        
        def dfs(node, current_sum):
            if not node:
                return 0
            
            current_sum += node.val
            # Find if there is a prefix sum we can subtract to get targetSum
            count = prefix_sums.get(current_sum - targetSum, 0)
            
            # Add current sum to the prefix map
            prefix_sums[current_sum] = prefix_sums.get(current_sum, 0) + 1
            
            # Recurse left and right
            count += dfs(node.left, current_sum)
            count += dfs(node.right, current_sum)
            
            # Backtrack: remove current sum from map so it doesn't affect other branches
            prefix_sums[current_sum] -= 1
            
            return count
            
        return dfs(root, 0)

# Build Binary Tree from Preorder and Inorder Traversal LC 105:
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Base case
        if not preorder or not inorder:
            return None

        root = preorder[0]
        mid = inorder.index(root)

        # left subtree are elemnts in inorder up to mid, for preorder, skip the first element (root) and take the same number of elements as in the left subtree
        # right subtree are elements in inorder after mid, for preorder, take the remaining elements after the left subtree
        root.left = self.buildTree(preorder[1: mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])

        return root

# ==========================================================
# Trees - BFS
# ==========================================================
"""
Breadth-First Search (BFS) on a tree is an algorithm used to traverse or search tree structures level by level, 
starting from the root node and exploring all neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.

        1
       / \
      2   3
     / \   \
    4   5   6

BFS Traversal Order: 1 -> 2 -> 3 -> 4 -> 5 -> 6

1. Initialize a Queue: Place the root node into a queue (FIFO: First-In, First-Out).
2. Loop Until Empty: While the queue is not empty:
    Dequeue the front node from the queue and visit/process it.
    Enqueue all of its direct children (left to right, or right to left) into the queue.
3. Repeat: Continue the process until the queue is completely empty.
"""

def bfs_tree(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        # Pop the node from the front of the queue
        current_node = queue.popleft()
        result.append(current_node.val)
        
        # Add left child to the queue if it exists
        if current_node.left:
            queue.append(current_node.left)
            
        # Add right child to the queue if it exists
        if current_node.right:
            queue.append(current_node.right)
            
    return result

# Level-Order Traversal (Grouping by Levels)
"""
Often in tree problems, you need to keep track of individual levels 
(for example, to return a 2D array where each sub-list represents a tree level). 
You can achieve this by recording the size of the queue at the start of each iteration.
 Time:  O(n)
Space: O(w) space (where w is the maximum width of the tree)
"""

def level_order_traversal(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        result.append(current_level)
        
    return result


# ==========================================================
# BST
# ==========================================================
"""
A Binary Search Tree (BST) is a node-based binary tree data structure that satisfies the following property for every node:
    The left subtree of a node contains only nodes with keys less than the node's key.
    The right subtree of a node contains only nodes with keys greater than the node's key.
    Both the left and right subtrees must also be binary search trees.

Time Complexity:Average Case: O(log n) for search, insertion, 
and deletion (when the tree is balanced).
Worst Case: O(n) (when the tree becomes skewed, resembling a linked list).
Space Complexity: O(h) where h is the height of the tree, due to the recursion stack during operations.

In-Order Traversal: Visiting nodes in the order: Left $\rightarrow$ Root $\rightarrow$ Right. For a BST, 
this always yields elements in sorted ascending order!!!.
"""

# Using bounds to validate the BST property. Each node must be within a specific range defined by its ancestors.
def isValidBST(self, root: Optional[TreeNode]) -> bool:
    """
    Time complexity: O(n) - We visit each node exactly once.
    Space complexity: O(h) - The space used by the stack is proportional to the height
    """
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
        
    return validate(root)

def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        
        def dfs(current):
            # Base case: if node is None or we found the value, return the node
            if not current or current.val == val:
                return current
            
            # Use BST properties to choose left or right, and make sure to RETURN the result
            if val < current.val:
                return dfs(current.left)
            else:
                return dfs(current.right)
        
        # Call the nested function starting from the root
        return dfs(root)


class Solution:
    """
    Base Case: If the root is None, return None (target not found).
    Search Phase:
        If the target key is smaller than root.val, look in the left subtree: root.left = deleteNode(root.left, key).
        If the target key is larger than root.val, look in the right subtree: root.right = deleteNode(root.right, key).
    Deletion Phase (Target Found):
        Case 1 & 2 (Zero or One Child): If root.left is None, return root.right. If root.right is None, return root.left.
        Case 3 (Two Children):
            Find the minimum node in the right subtree (curr = root.right, loop while curr.left is not None).
            Copy its value to root.val.
            Recursively delete that minimum node from the right subtree: root.right = deleteNode(root.right, root.val).
    Return: Return the updated root node.
    """
    def deleteNode(self, root: TreeNode | None, key: int) -> TreeNode | None:
        if not root:
            return None
        
        # 1. Traverse to find the node
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            # Node with 0 or 1 child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            # Node with 2 children: Get the inorder successor (min in right subtree)
            curr = root.right
            while curr.left:
                curr = curr.left
            
            # Replace value with inorder successor's value
            root.val = curr.val
            
            # Delete the inorder successor from the right subtree
            root.right = self.deleteNode(root.right, curr.val)
            
        return root


# ==========================================================
# Trie
# ==========================================================
"""
Every node represents a single character of a word, and paths down the tree trace out prefixes and complete words.
Root Node: The starting point of the Trie, which represents an empty string ("") and contains no character.
Child Nodes: Each node contains a collection of pointers or references to its children, typically mapped by character (e.g., using a dictionary/hash map or a fixed-size array).
End-of-Word Marker: A boolean flag (often called is_end_of_word) stored in each node to signify whether the path from the root up to that node represents a complete, valid word inserted into the Trie.
Prefix Sharing: Words sharing a common prefix (e.g., "cat", "cats", "cattle") share the same nodes for that prefix, significantly reducing memory overhead and speeding up prefix-based searches.

After inserting cat and car, the Trie would look like this:
Root ("")
 └── 'c'
      └── 'a'
           ├── 't' (is_end_of_word = True)
           └── 'r' (is_end_of_word = True)
"""
class TrieNode:
    """Represents a single node in the Trie data structure."""

    def __init__(self):
        # A dictionary mapping a character (str) to its corresponding child TrieNode.
        # This acts as the branching mechanism of the tree, allowing dynamic
        # child allocation for any character set (alphabetic, numeric, unicode, etc.).
        self.children = {}

        # A boolean flag that indicates whether the path from the root node
        # down to this specific node forms a complete, valid word.
        # This is crucial because a node might just represent a prefix
        # (e.g., 'app' inside 'apple') rather than a finalized, inserted word.
        self.is_end_of_word = False


class Trie:
    """Represents the Prefix Tree (Trie) managing the collection of words."""

    def __init__(self):
        # Every Trie starts with a blank root node.
        # The root node does not store any character and serves purely
        # as the entry point for all subsequent tree traversals.
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the trie character by character."""
        # Start the traversal pointer at the root node.
        current = self.root

        # Iterate through each character in the target word sequentially.
        for char in word:
            # Check if the current character already exists as a branch/child
            # of the current node.
            if char not in current.children:
                # If it doesn't exist, instantiate a new TrieNode and link it
                # to the current node's dictionary under the character key.
                current.children[char] = TrieNode()

            # Move the pointer down to the child node corresponding to the current character.
            current = current.children[char]

        # After looping through all characters, the pointer rests on the final node
        # representing the last character of the word. Set its flag to True
        # to formally signify that this path forms a complete word.
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns true if the exact word is present in the trie."""
        # Begin traversal from the root node.
        current = self.root

        # Traverse character by character following the path of the word.
        for char in word:
            # If any character along the path is missing from the children dictionary,
                # it means the word was never inserted into the Trie.
            if char not in current.children:
                return False

            # Step down to the next node.
            current = current.children[char]

        # Once the loop finishes, we have successfully found all characters.
        # However, to confirm it is an *exact* word (and not just a prefix of a longer word),
        # we must return the boolean value of `is_end_of_word` at this final node.
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns true if there is any previously inserted word that begins with the given prefix."""
        # Begin traversal from the root node.
        current = self.root

        # Traverse character by character along the prefix string.
        for char in prefix:
            # If any character in the prefix is missing, no word in the Trie
            # can possibly start with this sequence.
            if char not in current.children:
                return False

            # Step down to the child node.
            current = current.children[char]

        # If we successfully trace every character of the prefix without interruption,
        # it means at least one word in the Trie shares this prefix path.
        # Unlike `search`, we don't care if `is_end_of_word` is True or False here.
        return True

class TrieNode:

  def __init__(self):
    # Maps a character (e.g., 'a', 'b') to its corresponding child TrieNode.
    self.children = {}

    # Caches up to 3 lexicographically sorted product suggestions
    # that pass through or terminate at this specific node (prefix).
    self.suggestions = []

# V1
class Solution:

  def suggestedProducts(
      self, products: List[str], searchWord: str
  ) -> List[List[str]]:
    # Step 1: Sort products lexicographically.
    # Why? Since we insert them into the Trie in sorted order, any node
    # will naturally see words in alphabetical order. This ensures that
    # the first 3 words appended to `node.suggestions` are guaranteed
    # to be the top 3 lexicographically smallest ones.
    products.sort()
    root = TrieNode()

    # Step 2: Build the Trie and pre-compute suggestions
    for product in products:
      node = root
      for char in product:
        # If the character path doesn't exist yet, create a new TrieNode.
        if char not in node.children:
          node.children[char] = TrieNode()

        # Move down to the child node representing the current character.
        node = node.children[char]

        # Because `products` was sorted initially, words are processed in
        # alphabetical order. Therefore, the first 3 unique products we push
        # into this node's suggestion list will always be the correct top 3.
        # Once we have 3, we skip appending more to save time and space.
        if len(node.suggestions) < 3:
          node.suggestions.append(product)

    # Step 3: Search phase (processing the searchWord character by character)
    res = []
    node = root
    found = True  # Tracks whether the current prefix exists in the Trie

    for char in searchWord:
      # If a path for the prefix still exists and hasn't broken off yet:
      if found and char in node.children:
        # Step down to the next node in the Trie
        node = node.children[char]
        # Append the pre-calculated suggestions stored directly at this node
        res.append(node.suggestions)
      else:
        # Once a character breaks the prefix path, all subsequent
        # character lookups will fail. Mark `found` as False and return [].
        found = False
        res.append([])

    return res

# V2
class Solution:

  def suggestedProducts(
      self, products: List[str], searchWord: str
  ) -> List[List[str]]:
    
    # -------------------------------------------------------------------------
    # Step 1: Build the Standard Trie
    # -------------------------------------------------------------------------
    root = TrieNode()
    for product in products:
      node = root
      for char in product:
        # If the character path doesn't exist yet, create a new TrieNode.
        if char not in node.children:
          node.children[char] = TrieNode()
        # Move down to the child node representing the current character.
        node = node.children[char]
      # Mark the final node of this product as the end of a valid word.
      node.is_word = True

    # -------------------------------------------------------------------------
    # Step 2: Define the DFS Helper Function for Dynamic Traversal
    # -------------------------------------------------------------------------
    def dfs(node, path, results):
      # Optimization: Stop searching immediately once we have found 3 suggestions.
      if len(results) == 3:
        return
      
      # If the current node marks the end of a complete product, add it to results.
      if node.is_word:
        results.append(path)

      # Traverse children in alphabetical order. 
      # Why `sorted(node.children.keys())`? 
      # Because a Trie's children are stored in an unordered hash map (`{}`), 
      # sorting the keys ensures our DFS explores branches lexicographically 
      # (e.g., 'a' before 'b'), guaranteeing our results are sorted alphabetically.
      for char in sorted(node.children.keys()):
        if len(results) == 3:
          break
        dfs(node.children[char], path + char, results)

    # -------------------------------------------------------------------------
    # Step 3: Search Phase (Processing searchWord Character by Character)
    # -------------------------------------------------------------------------
    res = []
    node = root
    prefix = ""
    found = True  # Tracks whether the current prefix path exists in the Trie

    for char in searchWord:
      prefix += char
      
      # If the prefix path is still valid and the character exists in the Trie:
      if found and char in node.children:
        # Step down to the child node representing this character
        node = node.children[char]
        
        suggestions = []
        # Run DFS starting from this node to discover up to 3 valid words
        dfs(node, prefix, suggestions)
        res.append(suggestions)
      else:
        # Once a character breaks the prefix path, no matching products exist.
        # Mark `found` as False and append an empty list for all subsequent characters.
        found = False
        res.append([])

    return res

