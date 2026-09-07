"""
Key Python operations: Graphs.
Covers DFS/BFS traversal and topological sort (Kahns algorithm).
"""

import collections
from collections import deque
from typing import List


# ==========================================================
# Graph DFS
# ==========================================================
"""
Depth-First Search (DFS) is a fundamental graph traversal algorithm that explores as deep as possible along each branch before backtracking. 
- LIFO (Last-In, First-Out): DFS relies on a stack data structure, prioritizing the most recently discovered vertex to dive deeper into the graph.
- Backtracking: When the algorithm hits a dead end or a node with no unvisited neighbors, it steps back to the previous node to explore alternative branches.
- Node States & Tracking
Visited Tracking: A boolean array or hash set tracks visited vertices to prevent infinite loops in cyclic graphs.
Three-State Coloring: Advanced implementations use color markings—White (unvisited), Gray (currently being explored in the recursion stack), and Black (fully explored).
- Core Operations
Initialization: Select a starting vertex, mark it as visited, and push it onto the stack (or enter the recursive call).
Recursive Exploration: Look at an unvisited adjacent neighbor of the current node, mark it, and immediately shift focus to it.
Backtracking Step: When a vertex has no remaining unvisited neighbors, the algorithm pops it or returns from the recursive function to resume exploration from the parent node.
"""
# Recursive DFS Implementation
def dfs_recursive(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    
    # 1. Initialization/Visit operation
    visited.add(vertex)
    print(f"Visited: {vertex}")
    
    # 2. Recursive exploration of neighbors
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            # Backtracking happens automatically when the recursive call returns
            dfs_recursive(graph, neighbor, visited)
            
    return visited

# Example graph represented as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# Run DFS starting from 'A'
dfs_recursive(graph, 'A')

#-----------------------------------------------------
# Iterative DFS using an explicit stack
def dfs_iterative(graph, start_vertex):
    visited = set()
    stack = [start_vertex]  # Explicit stack initialization
    
    while stack:
        # 1. Pop operation (LIFO)
        vertex = stack.pop()
        
        if vertex not in visited:
            # 2. Visit operation
            visited.add(vertex)
            print(f"Visited: {vertex}")
            
            # 3. Push unvisited neighbors onto the stack
            # Reversed is often used to match the left-to-right order of recursive DFS
            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return visited

# Run iterative DFS starting from 'A'
dfs_iterative(graph, 'A')

#-----------------------------------------------------
# Connected Components in an Undirected Graph using DFS
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        # Get the total number of cities (n) from the size of the adjacency matrix.
        n = len(isConnected)
        
        # Initialize a boolean tracking list of size n, all set to False.
        # This keeps track of whether we have already explored a given city.
        visited = [False] * n
        
        # Initialize our counter to store the total number of independent provinces found.
        provinces = 0
        
        # Iterate through every city from 0 to n - 1 to find unvisited components.
        for i in range(n):
            # If the current city has not been visited yet, it belongs to a new province.
            if not visited[i]:
                # Increment our province count since we found a new starting node.
                provinces += 1
                
                # Launch the helper DFS method. 
                # Notice we must use 'self.dfs' and explicitly pass down the 
                # state variables because this method is no longer nested.
                self.dfs(i, isConnected, visited)
                
        # After checking all cities, return the total count of provinces.
        return provinces

    def dfs(self, city: int, isConnected: List[List[int]], visited: list[bool]):
        # Mark the current city as visited so we don't process it multiple times.
        visited[city] = True
        
        # Loop through all possible neighboring cities from 0 to n - 1.
        for neighbor in range(len(isConnected)):
            # Check two conditions:
            # 1. isConnected[city][neighbor] == 1: Is there a direct road/connection?
            # 2. not visited[neighbor]: Have we NOT visited this neighbor yet?
            if isConnected[city][neighbor] == 1 and not visited[neighbor]:
                # Recursively call self.dfs to explore further down this path,
                # passing along the exact same state references.
                self.dfs(neighbor, isConnected, visited)

#-----------------------------------------------------
# Reversing directions of edges in a tree to ensure all paths lead to the root (city 0).

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        """
        Main function that initializes the graph and triggers the recursive DFS.
        """
        # Step 1: Build the adjacency list to represent the tree as an undirected graph.
        # We store tuples of (neighbor, cost) for each edge.
        graph = collections.defaultdict(list)
        for u, v in connections:
            # If we travel from u to v, we are moving AWAY from city 0. 
            # This requires a reversal if we want paths to lead to 0, so cost = 1.
            graph[u].append((v, 1))
            
            # If we travel from v to u, we are moving TOWARD city 0. 
            # This is already in the correct direction, so cost = 0.
            graph[v].append((u, 0))
            
        # Step 2: Keep track of visited nodes to prevent infinite loops (since it's a cyclic graph representation)
        visited = set()
        
        # Step 3: Start the recursive DFS traversal from the capital city (city 0).
        # We pass the graph, the starting node, and the visited set into our helper method.
        return self._dfs(0, graph, visited)

    def _dfs(self, node: int, graph: dict, visited: set) -> int:
        """
        Recursive helper method that explores the graph, counts necessary road reversals,
        and returns the total count for the current subtree.
        """
        # Mark the current node as visited so we don't traverse back to it.
        visited.add(node)
        
        # Initialize the reversal count for this branch of the recursion.
        reversals = 0
        
        # Iterate through all adjacent nodes (neighbors) and the cost associated with moving to them.
        for neighbor, cost in graph[node]:
            # If the neighbor has not been visited yet, it means we are moving outward from city 0.
            if neighbor not in visited:
                # Add the cost of this specific edge (1 if it needs flipping, 0 if it's already correct).
                reversals += cost
                
                # Recursively call DFS on the neighbor and add its subtree's reversals to our total.
                reversals += self._dfs(neighbor, graph, visited)
                
        # Return the accumulated reversals for this node and its entire subtree.
        return reversals


# ==========================================================
# Graph BFS
# ==========================================================
"""
Key Concepts of BFSBreadth-First Search (BFS) is a graph traversal algorithm that explores a graph level by level, visiting all neighbor nodes at the current depth before moving on to the nodes at the next depth level.
Queue (FIFO): The core data structure that manages traversal order using a First-In, First-Out approach, ensuring nodes are processed in the exact order they are discovered.
Visited Tracking: A hash set used to keep track of nodes already visited, which prevents infinite loops in graphs with cycles.
Time & Space Complexity: Operates in $O(V + E)$ time and $O(V)$ space (where $V$ is vertices and $E$ is edges), as every vertex and edge is visited and stored in memory.
Algorithm Operations
1. Initialization: Add the starting node to a queue and mark it as visited.
2. Removal: Dequeue the front node from the queue to make it the current active node.
3. Neighbor Exploration: Check all adjacent neighbors of the current node.
4. Queue Insertion: For each neighbor not yet visited, mark it as visited and enqueue it.
5. Iteration: Repeat steps 2 through 4 until the queue becomes empty.
"""


def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    traversal_order = []
    
    while queue:
        current = queue.popleft()
        traversal_order.append(current)
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return traversal_order

# Example usage with an adjacency list:
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("BFS Traversal:", bfs(graph, 'A')) # Output: BFS Traversal: ['A', 'B', 'C', 'D', 'E', 'F']

# Shortest Path in Unweighted Graph using BFS

def bfs_shortest_path(graph, start, target):
    # Base case: If the starting node is already the target node,
    # we don't need to search; return a list containing just the start node.
    if start == target:
        return [start]
        
    # A set to keep track of nodes we have already visited.
    # This prevents infinite loops in cyclic graphs and redundant work.
    visited = {start}
    
    # A FIFO (First-In, First-Out) queue for level-order traversal,
    # initialized with our starting node.
    queue = deque([start])
    
    # A dictionary to act as our "breadcrumb trail" (parent pointers).
    # It maps each node to the node that discovered it, allowing us to 
    # reconstruct the path later. The start node has no parent (None).
    parent = {start: None}  
    
    # Continue exploring as long as there are nodes left in the queue.
    while queue:
        # Remove and retrieve the node at the front of the queue.
        # This becomes our current active node for this iteration.
        current = queue.popleft()
        
        # Check if we have reached our destination. Because BFS explores 
        # level by level, the first time we pop the target, we are guaranteed 
        # to have found the shortest path.
        if current == target:
            path = []
            
            # Trace backward from the target to the start using the parent dictionary.
            while current is not None:
                path.append(current)          # Add the current node to our path list
                current = parent[current]     # Move back to the node's parent
                
            # Since we traced backward (Target -> ... -> Start), 
            # we reverse the list using slicing ([::-1]) to get Start -> ... -> Target.
            return path[::-1]  
            
        # Iterate through all adjacent neighbors of the current node.
        for neighbor in graph[current]:
            # If we haven't visited this neighbor yet, process it.
            if neighbor not in visited:
                visited.add(neighbor)             # Mark it as visited immediately
                parent[neighbor] = current        # Record that 'current' discovered this neighbor
                queue.append(neighbor)            # Add it to the queue to explore its neighbors later
                
    # If the queue becomes empty and we never hit the target, 
    # it means no path exists between the start and target nodes.
    return None  

# Example graph represented as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Find the shortest path from node 'A' to node 'F'
path = bfs_shortest_path(graph, 'A', 'F')
print("Shortest Path:", path) # Output: Shortest Path: ['A', 'C', 'F']

# Maze Solving

class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        # Get the dimensions of the maze: m rows and n columns
        m, n = len(maze), len(maze[0])
        
        # Initialize a queue for BFS containing tuples of: (row, col, current_steps)
        # We start at the entrance coordinates with 0 steps taken.
        queue = deque([(entrance[0], entrance[1], 0)])
        
        # Mark the entrance as visited by changing it to a wall ('+').
        # This prevents the BFS from accidentally looping back to the entrance later.
        maze[entrance[0]][entrance[1]] = '+'
        
        # Define the 4 possible movement directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Standard BFS loop: process nodes level by level (layer by layer)
        while queue:
            # Pop the front element from the queue
            row, col, steps = queue.popleft()
            
            # Explore all 4 neighboring directions from the current cell
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check 1: Ensure the neighbor is within the boundaries of the maze.
                # Check 2: Ensure the neighbor is an open cell ('.'), not a wall ('+').
                if 0 <= new_row < m and 0 <= new_col < n and maze[new_row][new_col] == '.':
                    
                    # Check if this valid open cell is located on the outer border of the maze.
                    # Note: Because we started from the neighbors of the entrance, 
                    # an entrance sitting on the border will never trigger this for itself.
                    if new_row == 0 or new_row == m - 1 or new_col == 0 or new_col == n - 1:
                        # Since BFS guarantees the shortest path, the first border cell 
                        # we hit is guaranteed to be the nearest exit! Return total steps.
                        return steps + 1
                    
                    # Otherwise, it's a regular empty cell inside the maze:
                    # 1. Mark it as visited by turning it into a wall ('+') so we don't visit it again.
                    maze[new_row][new_col] = '+'
                    # 2. Add it to the queue with incremented step count to explore its neighbors next.
                    queue.append((new_row, new_col, steps + 1))
                    
        # If the queue becomes completely empty and we never hit a border exit,
        # it means no exit is reachable. Return -1.
        return -1

# ==========================================================
# Graph Topological Sort
# ==========================================================
# Topological Sort using Kahn's Algorithm


def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
  """Returns a valid topological sort order for a DAG.

  If a cycle exists, returns an empty list.
  """
  # STEP 1: Graph Representation Setup
  # Create an empty adjacency list for each course (0 to num_courses - 1).
  adj = {i: [] for i in range(num_courses)}
  # Track incoming edge counts (prerequisite count) for every course, initialized to 0.
  in_degree = [0] * num_courses

  # STEP 2: Building the Graph from Edge List
  # Each prerequisite pair is given as [course, prereq], meaning "prereq must be taken before course".
  for course, prereq in prerequisites:
    # Add a directed edge from prerequisite -> course in our adjacency list.
    adj[prereq].append(course)
    # Increment the in-degree count of the target course because it has one more dependency.
    in_degree[course] += 1

  # STEP 3: Seeding the Queue
  # Find all nodes that have an in-degree of 0 (no prerequisites/dependencies).
  # These are our starting points because they can be processed immediately.
  queue = deque([i for i in range(num_courses) if in_degree[i] == 0])

  # List to store the final topological order sequence.
  top_order = []

  # STEP 4: BFS Processing Loop
  while queue:
    # Pop the node from the front of the queue (it has 0 unresolved prerequisites).
    curr = queue.popleft()
    # Add it to our valid topological order.
    top_order.append(curr)

    # For every course that depends on 'curr' (its neighbors):
    for neighbor in adj[curr]:
      # Since 'curr' is now processed, we remove its dependency constraint.
      in_degree[neighbor] -= 1
      # If all prerequisites for this neighbor are now satisfied (in-degree hits 0):
      if in_degree[neighbor] == 0:
        # Push it to the queue so it can be processed next.
        queue.append(neighbor)

  # STEP 5: Cycle Detection & Validation
  # If the total number of nodes in our topological order equals the total number of courses,
  # it means we successfully processed every node (no cycles trapped any nodes).
  if len(top_order) == num_courses:
    return top_order

  # If length doesn't match, a cycle exists (deadlock where remaining nodes have in-degree > 0).
  return []
