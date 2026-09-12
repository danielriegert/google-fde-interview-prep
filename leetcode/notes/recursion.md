# Recursion

## Gotchas

- Cannot pass immutable items to a recursive function e.g. number or string if I need to keep track of something accross recursive calls e.g. count, sum, etc. Need to use class variable or nested function with nonlocal

## General Approach

- Define base case and recurisve case
- It will go top down -> defered execution add to stack
- Once base case hit it will unwind bottom up i.e. pop fomr stack
