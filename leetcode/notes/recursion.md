# Recursion

## Gotchas

- Cannot pass immutable items to a recursive function e.g. number or string if I need to keep track of something accross recursive calls e.g. count, sum, etc. Need to use class variable or nested function with nonlocal

## General Approach

- Define base case and recurisve case
- It will go top down -> defered execution add to stack
- Once base case hit it will unwind bottom up i.e. pop fomr stack
- Only look at one element / node and see what I need to do with it e.g. check if leave, meets some condition,etc
- Think about what I need to pass to subsequent recusrive calls e.g. count so far, sum so far

# Template

```python
def recursive_function(parameters):
    # 1. Base Case(s): Check if the problem is small enough to solve directly
    if base_condition_met:
        return base_value  # or exit without calling self

    # 2. Optional: Process data / preprocessing before the recursive call

    # 3. Recursive Step: Call the function with a modified/smaller parameter
    #    This MUST move the state closer to the base case.
    return combine_result(sub_problem_result, recursive_function(modified_parameters))
```
