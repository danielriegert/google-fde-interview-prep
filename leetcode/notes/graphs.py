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
def dfs_recursive_adjacency_list(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    
    # 1. Initialization/Visit operation
    visited.add(vertex)
    print(f"Visited: {vertex}")
    
    # 2. Recursive exploration of neighbors
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            # Backtracking happens automatically when the recursive call returns
            dfs_recursive_adjacency_list(graph, neighbor, visited)
            
    return visited

def dfs_recursive_adjacency_matrix(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    
    # 1. Initialization/Visit operation
    visited.add(vertex)
    print(f"Visited: {vertex}")
    
    # 2. Recursive exploration of neighbors
    # Iterate through all possible node indices in the matrix row
    for neighbor in range(len(graph)):
        # Check if a connection exists and the neighbor is unvisited
        if graph[vertex][neighbor] == 1 and neighbor not in visited:
            dfs_recursive_adjacency_matrix(graph, neighbor, visited)
            
    return visited

def dfs_recursive_matrix(graph, vertex, visited=None):
    if visited is None:
        visited = set()
    
    # 1. Initialization/Visit operation
    visited.add(vertex)
    print(f"Visited: {vertex}")
    
    # 2. Recursive exploration of neighbors
    # Iterate through all possible node indices in the matrix row
    for neighbor in range(len(graph)):
        # Check if a connection exists and the neighbor is unvisited
        if graph[vertex][neighbor] == 1 and neighbor not in visited:
            dfs_recursive_matrix(graph, neighbor, visited)
            
    return visited

# Example graph represented as an adjacency list
# Use for non-integer problems
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

# Node 0 connects to 1 and 2; Node 1 connects to 0 and 3, etc.
# Use for integer problems
graph = [
    [1, 2],
    [0, 3],
    [0],
    [1]
]

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
# Cloning a graph using DFS (LeetCode 133. Clone Graph)
"""
1. **Handle Edge Cases**
Check if the input node is `None`. If the graph is empty, immediately return `None` to prevent attribute errors during traversal.
2. **Initialize a Tracking Hash Map**
Create a hash map (or dictionary) to map every original node reference to its newly created clone (`old_to_new`). T
his data structure serves a dual purpose: it acts as a visited set to prevent infinite loops in cyclic graphs, and it stores references to the clones so they can be reused.
3. **Choose a Traversal Strategy**
Decide whether to use Depth-First Search (DFS) or Breadth-First Search (BFS) to explore the graph's structure node by node.
4. **Instantiate and Cache Clones**
When encountering a node for the first time, immediately create its clone using its value (`Node(curr.val)`) and save it in the hash map *before* exploring any of its neighbors. 
This ensures the clone exists in memory if a neighbor tries to reference it back.
If a node is already cloned, just return it (recursion base case)
5. **Reconstruct Neighbor Connections**
Iterate through all the neighbors of the current node. For each neighbor, recursively or iteratively fetch its corresponding clone from the hash map (creating it if it doesn't exist yet) and append it to the current clone's `neighbors` list.
"""
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        
        old_to_new = {}
        return self.dfs(node, old_to_new)
        
    def dfs(self, curr, old_to_new):
        # If the node is already cloned, return its copy from the hash map
        if curr in old_to_new:
            return old_to_new[curr]
        
        # Create the clone for the current node and save it before exploring neighbors
        copy = Node(curr.val)
        old_to_new[curr] = copy
        
        # Recursively clone all neighbors and add them to the copy's neighbor list
        for neighbor in curr.neighbors:
            copy.neighbors.append(self.dfs(neighbor, old_to_new))
            
        return copy

#-----------------------------------------------------
# Template finding the number of connected components in an undirected graph for Matrix problems (DFS).
# e.g. LeetCode 133,  LeetCode 200. Number of Islands, Leetcode 261. Graph Valid Tree
class Solution:
    def solveMatrixProblem(self, grid: list[list[str]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        rows, cols = len(grid), len(grid[0])
        # 4-directional movement vectors (Up, Down, Left, Right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        result = 0
        for r in range(rows):
            for c in range(cols):
                # Trigger condition (e.g., finding an unvisited target)
                if grid[r][c] == 'target_condition':
                    result += 1
                    self.dfs(grid, r, c, rows, cols, directions)
                    
        return result

    def dfs(self, grid: list[list[str]], r: int, c: int, rows: int, cols: int, directions: list[tuple[int, int]]) -> None:
        # 1. Base case: Check bounds and problem-specific termination conditions
        # Important >= and <= as this len and gird is 0 indexed
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 'invalid_condition':
            return
        
        # 2. Mark current cell as visited (in-place modification)
        grid[r][c] = 'visited_condition'
        
        # 3. Explore all valid neighbors
        for dr, dc in directions:
            self.dfs(grid, r + dr, c + dc, rows, cols, directions)
#-----------------------------------------------------
# Connected Components in an Undirected Graph using DFS Adjacency Matrix
# LeetCode 547. Number of Provinces:
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
# Weighted Graphs e.g. LC 399. Evaluate Division
"""
Weighted graphs extend standard graph theory by assigning numerical values (weights) to edges, representing costs, distances, capacities, or relative ratios.
Core ComponentsNodes / Vertices ($V$): 
- The fundamental entities or points in the network (e.g., cities, variables, network routers).
- Edges / Arcs ($E$): The connections between nodes. In a weighted graph, each edge $e = (u, v)$ is associated with a weight function $w(e)$ or $w(u, v)$.
- Directed vs. Undirected Weighted Edges: Edges can be bidirectional with symmetric weights (e.g., physical distance between two towns) or unidirectional with asymmetric or directional relationships (e.g., currency exchange rates or division ratios like LeetCode 399, where $a / b = k$ implies $b / a = 1 / k$).

Fundamental Properties
- Path Weight: The total cost or accumulated value of a path, calculated either by summing individual edge weights (additive, e.g., shortest path problems) or multiplying them (multiplicative, e.g., probability or conversion ratios).
Adjacency Representation: Typically stored using Adjacency Lists where each node points to a list of pairs (neighbor, weight), or Adjacency Matrices where the cell at matrix[i][j] holds the edge weight between node $i$ and node $j$ (or infinity/null if no edge exists).
"""
from collections import defaultdict
from typing import List

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        
        # ==========================================
        # STEP 1: Build the Adjacency List Graph
        # ==========================================
        # defaultdict(dict) creates a nested dictionary where missing keys 
        # automatically initialize as empty dictionaries. 
        # Structure will look like: { node: { neighbor: weight } }
        graph = defaultdict(dict)
        
        # zip() pairs each equation pair [A, B] with its corresponding division value
        for (A, B), value in zip(equations, values):
            # Direction A -> B: A / B = value (e.g., a / b = 2.0 means a = 2 * b)
            graph[A][B] = value
            
            # Direction B -> A: B / A = 1.0 / value (the inverse relationship)
            graph[B][A] = 1.0 / value
            
        # ==========================================
        # STEP 2: Define the DFS Traversal Function
        # ==========================================
        # This recursive function searches for a path from 'curr' to 'target'
        def dfs(curr: str, target: str, seen: set) -> float:
            
            # Base Case 1: If our current node is already the target, 
            # we've successfully reached the destination. We return 1.0 
            # because multiplying by 1.0 does not change our accumulated product.
            if curr == target:
                return 1.0
                
            # Mark the current node as visited so we don't loop infinitely 
            # (e.g., going back and forth between A and B).
            seen.add(curr)
            
            # Explore all direct neighbors of the current node
            for neighbor, weight in graph[curr].items():
                
                # Only visit neighbors we haven't explored in this path yet
                if neighbor not in seen:
                    
                    # Recursively search from the neighbor to the target
                    res = dfs(neighbor, target, seen)
                    
                    # If res != -1.0, it means a valid path was found downstream!
                    if res != -1.0:
                        # Multiply the edge weight to get to this neighbor 
                        # by the result obtained from the rest of the path.
                        return weight * res
                        
            # Base Case 2: If we check all neighbors and find no valid path to the target,
            # return -1.0 to signify that this path is a dead end.
            return -1.0

        # ==========================================
        # STEP 3: Process Each Query
        # ==========================================
        ans = []
        
        for A, C in queries:
            # Check if either variable in the query doesn't exist in our graph at all.
            # If it's missing, it's impossible to evaluate, so we immediately output -1.0.
            if A not in graph or C not in graph:
                ans.append(-1.0)
            else:
                # Otherwise, trigger our DFS traversal starting from variable A,
                # looking for variable C, and passing a fresh 'set()' to track visited nodes.
                ans.append(dfs(A, C, set()))
                
        # Return the final list of evaluated query results
        return ans
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
Time & Space Complexity: Operates in O(V + E) time and O(V) space (where V is vertices and E is edges), as every vertex and edge is visited and stored in memory.
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

# Shortest Path in Unweighted Graph using BFS.
# This is when we actually need to return the path not just the step count.
# ToDo: practice this with matrix problems

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

# Maze Solving. Find nearest exit from the entrance.
# This is also BFS shortest path problem but we usually only need to return the step count not the actual path.
# BFS will guarantee the shortest path in an unweighted graph like a maze.

# Template
"""
1. Define the State Space: Determine what a single "state" represents (e.g., coordinates (r, c) for a 2D grid maze, or an integer square for linear board games).
2. Initialize Tracking Structures:
    A FIFO queue (via collections.deque) to process states level-by-level, ensuring shortest-path discovery.
    A visited set to prevent infinite loops and redundant expansions.
3. Seed the Search: Add the starting state to both the queue and the visited set, tracking initial cost or step counts alongside it.
4. Process Level-by-Level (BFS Loop): Pop from the front of the queue and immediately check if the current state satisfies the target condition.
5. Generate and Filter Neighbors: Compute all legal transitions from the current state. For each neighbor, check boundaries, game rules (like walls, snakes, or ladders), and the visited set before pushing it to the queue.

Key Variations to Keep in Mind:
- Multi-Source BFS: If you can start from multiple locations (e.g., nearest exit problems with multiple exits), seed the queue with all starting positions simultaneously and add them all to visited at the very beginning.
- State Compression: If your state requires multiple variables (e.g., (r, c, keys_held)), ensure the entire state tuple is hashable so it can be safely stored in the visited set.

Time and Space Complexity: O(N^2) dereived from BFS (V + E)

"""
from collections import deque

def bfs_shortest_path(start_state, target_condition):
    # Queue stores tuples of (state, distance/steps)
    queue = deque([(start_state, 0)])  
    visited = {start_state}
    
    while queue:
        current, steps = queue.popleft()
        
        # 1. Check if we've reached the target
        if current == target_condition:
            return steps
            
        # 2. Generate and evaluate all valid next moves
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, steps + 1))
                
    # Target is unreachable
    return -1

# LC ?
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

# LC 909
class Solution:
    def get_coordinates(self, square, n):
        r = n - 1 - (square - 1) // n
        c = (square - 1) % n
        if (n - 1 - r) % 2 == 1:
            c = n - 1 - c
        return r, c

    def snakesAndLadders(self, board: List[List[int]]) -> int:
        from collections import deque
        n = len(board)
        target_square = n * n
        # Keep track of visited squares to avoid cycles and redundant work
        visited = {1}
        queue = deque([(1, 0)])
        
        while queue:
            current_square, steps = queue.popleft()
            # Check if current is target
            if current_square == target_square:
                return steps

            # Visit next squares based on dice rolls (1 to 6)
            for next_square in range(current_square + 1, min(current_square + 6, target_square) + 1):
                # Need to check if we are jumping to a ladder or snake
                r, c = self.get_coordinates(next_square, n)
                destination = board[r][c] if board[r][c] != -1 else next_square
                
                if destination not in visited:
                    visited.add(destination)
                    queue.append((destination, steps + 1))
        
        return -1
# ==========================================================
# Graph Topological Sort
# ==========================================================
# Topological Sort using Kahn's Algorithm (BFS)
# LC 207 & 210. Course Schedule I & II
"""
Note: Yes, topological sorting only works on directed graphs, specifically Directed Acyclic Graphs (DAGs).
If there are cycles no topological ordering exists.

Time Complexity: O(V + E)
* V is the number of vertices (nodes/courses).
* E is the number of edges (prerequisites/connections).

**Breakdown:**
* Calculating initial in-degrees and building the adjacency list takes O(E) time.
* Pushing the initial nodes with an in-degree of 0 into the queue takes O(V) time.
* The BFS traversal processes each vertex once (O(V)) and iterates through every outgoing edge for each node exactly once (O(E)).

Space Complexity: O(V + E)

**Breakdown:**

* The adjacency list requires O(V + E) space to store all nodes and their directed edges.
* The in-degree array or dictionary takes O(V) space to keep track of the count for each node.
* The BFS queue holds up to V elements in the worst-case scenario, taking O(V) space.

1. **Initialize graph and in-degrees:** Create an adjacency list to represent directed edges and an array to track the incoming edge count for each node.
2. **Build the graph:** Loop through the edges to populate the adjacency list and increment the in-degree count for target nodes.
3. **Queue root nodes:** Find all nodes with an in-degree of `0` (nodes with no dependencies) and push them into a queue.
4. **Process via BFS:** Pop a node from the queue, record it in your output/processed count, and decrement the in-degree of all its neighbors.
5. **Add newly unlocked nodes:** If a neighbor's in-degree drops to `0` after decrementing, push it into the queue.
6. **Check for cycles:** Ensure all nodes were successfully processed; if the count of visited nodes doesn't match the total number of nodes, a cycle exists and a valid topological sort is impossible.

Edge Cases:
* Empty Graph: If there are no nodes, return an empty list.
* Single Node: If there's only one node with no edges, return that node as the topological order.
* Cyclic Graph: If a cycle is detected (i.e., not all nodes are processed), return an empty list or indicate that a topological sort is impossible.
"""

from collections import deque
from typing import List

def topological_sort(num_nodes: int, edges: List[List[int]]) -> List[int]:
    # 1. Initialize adjacency list and in-degree array
    adj = [[] for _ in range(num_nodes)]
    in_degree = [0] * num_nodes
    
    # 2. Build the graph and compute in-degrees i.e. number of dependencies for each node
    # adjacencey list asks for each node, which nodes it points to (outgoing edges)
    # in_degree counts how many edges point to each node (incoming edges)
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
        
    # 3. Find all nodes with 0 in-degree (no prerequisites)
    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    result = []
    
    # 4. Process the queue (BFS)
    while queue:
        curr = queue.popleft()
        result.append(curr)
        
        # Reduce in-degree for all neighboring nodes
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 5. Cycle check: if result doesn't include all nodes, a cycle exists
    if len(result) != num_nodes:
        return []  # Cycle detected, valid topological order impossible
        
    return result

#-----------------------------------------------------
from collections import deque

def topological_sort_dict(adj):
    # 1. Initialize in_degree dictionary for all nodes
    in_degree = {node: 0 for node in adj}
    
    # Ensure any node that only appears as a neighbor (value) is also tracked
    for u in adj:
        for v in adj[u]:
            if v not in in_degree:
                in_degree[v] = 0

    # 2. Calculate in-degrees from the adjacency list
    for u in adj:
        for v in adj[u]:
            in_degree[v] += 1
            
    # 3. Find all nodes with 0 in-degree
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []
    
    # 4. Process the queue (BFS)
    while queue:
        curr = queue.popleft()
        result.append(curr)
        
        for neighbor in adj.get(curr, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 5. Cycle check
    if len(result) != len(in_degree):
        return []  # Cycle detected
        
    return result

#-----------------------------------------------------
# Example Course Schedule I
def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        from collections import deque

        # init adjacency list and indegree
        adjacency_list = [[] for _ in range(numCourses)]
        in_degree = [0] * numCourses

        # adjacency list: [[1], []] -> meaning course 0 is prerequisite for course 1, course 1 is not prerquisite for anything
        # asks for each course (index), which courses depend on it (outgoing edges)
        # in degree:[0, 1] -> course 0 has no prerequisites, course 1 has 1 prerequisite
        # counts number of prerequisites for each course (incoming edges)
        for course, pre in prerequisites:
            adjacency_list[pre].append(course)
            in_degree[course] += 1
        
        # Add courses with no dependencies i.e. indegree of 0
        # could also write range(len(in_degree))
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])

        processed_courses = 0

        while queue:
            current = queue.popleft()
            processed_courses += 1

            for neighbour in adjacency_list[current]:
                in_degree[neighbour] -= 1

                if in_degree[neighbour] == 0:
                    queue.append(neighbour)
        
        return processed_courses == numCourses

#-----------------------------------------------------
# Example Course Schedule II
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        from collections import deque

        # init adjacency list (for each course what other courses depend on it) and in degree (counts for each course (index) how many prerequisites)
        adjacency_list = [[] for _ in range(numCourses)]
        in_degree = [0] * numCourses

        # built full adjacnency list and in degrees
        # adjacency list asks: for each course what other courses depend on it (outgoing edges)
        # in degree asks: how many dependencies does a course have (incoming edges)
        for course, pre in prerequisites:
            adjacency_list[pre].append(course)
            in_degree[course] += 1
        
        # add courses with no prerequisites into the queue. this is our starting point
        queue = deque([i for i in range(numCourses) if in_degree[i] == 0])

        course_order = []
        while queue:
            # pope element and add to course order
            current = queue.popleft()
            course_order.append(current)

            # start to visit dependencies of current course
            for neighbour in adjacency_list[current]:
                # decrese dependency for preqresuisite by one as we visited one of them
                in_degree[neighbour] -= 1

                # if neighbour has no univisted dependencies we can add it to queue and process next
                if in_degree[neighbour] == 0:
                    queue.append(neighbour)
        
        # Check if valid topological sort i.e. no cycles
        if len(course_order) == numCourses:
            return course_order
        
        # if no valid topological sort exists
        return []