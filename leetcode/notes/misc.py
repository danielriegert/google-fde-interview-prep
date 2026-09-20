"""
Key Python operations: Misc.
Grab-bag of general-purpose Python patterns that do not belong to one specific data structure or algorithm topic.
"""

# ==========================================================
# while-else loop
# ==========================================================
# else block only runs if the loop finishes naturally (meaning it finished without hitting a break).
while stack and ast < 0 < stack[-1]:
    ...
    if stack[-1] < -ast:
        stack.pop()
        continue 
    elif stack[-1] == -ast:
        stack.pop()
    break
else:
    stack.append(ast)

# ==========================================================
# while-else loop
# ==========================================================
# Square a number in python
squared = n ** 2  # Using the exponentiation operator

# ==========================================================
# Division
# ==========================================================
# Performs ceiling division (rounding up to the nearest whole integer).
math.ceil(p / k)  

# Performs floor division (integer division, rounding down). For the same pile, $7 // 3$ evaluates to $2$.
p // k