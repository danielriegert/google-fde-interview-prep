"""
Key Python operations: Matrices / 2D grids.
"""

# Iterating Over Rows

grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

for row_idx, row in enumerate(grid):
  print(f"Row {row_idx}: {row}")

# Element-wise Iteration
for r in range(len(grid)):
  for c in range(len(grid[0])):
    print(f"Element at ({r}, {c}): {grid[r][c]}")

# Getting columns from grid
columns = []
n = len(grid)
for c in range(n):
    col = [grid[r][c] for r in range(n)]
    columns.append(col)

# Getting columns from grid using zip
columns = list(zip(*grid))  # Transpose the grid

# Extract rows and columns in n^3 time complexity
def has_matching_row_and_col(grid):
  # Get all columns by transposing the grid
  columns = list(zip(*grid))

  # Check every row against every column
  # row is n
  for row in grid:
    # col is n
    for col in columns:
      # Convert col (tuple) to list or compare directly
      # comparison is also n. compare n items in row and col
      # hence n^3
      if row == list(col):  # or tuple(row) == col
        return True

  return False

# Extract rows and columns in n^2 time complexity
from collections import Counter


def count_equal_row_col_pairs(grid):
  # Count occurrences of each row (must convert lists to tuples to be hashable)
  # This is n^2
  row_counts = Counter(tuple(row) for row in grid) # looks like Counter({(1, 2, 3): 2, (1, 4, 5): 1})

  # Get columns by transposing
  # This is n^2
  columns = zip(*grid)

  # Count how many columns exist in our row counts dictionary
  # This is n^2
  total_matches = 0
  for col in columns:
    # Looks up the column tuple in the row counts. 
    # Counter will automaticaly return 0 if the column is not found in the row counts.
    total_matches += row_counts[col]  

  return total_matches

