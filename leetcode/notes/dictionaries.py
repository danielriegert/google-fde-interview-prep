"""
Key Python operations: Dictionaries.
Adding, removing, and different ways to iterate.
"""


d = {"a": 1, "b": 2}

# --- Adding / updating ---
d["c"] = 3                     # add new key or overwrite existing key
d.update({"d": 4, "a": 10})    # add/overwrite multiple keys at once
d.setdefault("e", 5)           # set only if key doesn't already exist

# --- Removing ---
del d["e"]                     # remove key (raises KeyError if missing)
val = d.pop("d")               # remove & return value (raises KeyError if missing)
val = d.pop("missing", None)   # remove with default if key not found (no error)
key, value = d.popitem()       # remove & return the last inserted (key, value) pair
d.clear()                      # remove everything -> {}

# --- Iterating ---
d = {"a": 1, "b": 2, "c": 3}

for key in d:                  # keys only (default iteration)
    pass

for key in d.keys():           # keys only (explicit)
    pass

for value in d.values():       # values only
    pass

for key, value in d.items():   # key + value pairs
    pass

doubled = {k: v * 2 for k, v in d.items()}     # dict comprehension
filtered = {k: v for k, v in d.items() if v > 1}  # dict comprehension with filter

# safe lookup without KeyError
value = d.get("z")             # None if missing
value = d.get("z", 0)          # default value if missing


# --- Sorting ---
# Sort intervals by start time
sorted_intervals = sorted(intervals, key=lambda x: x[0])

data = {'a': 5, 'b': 1, 'c': 9}
sorted(data.items(), key= lambda x: x[1])
# Output: [('b', 1), ('a', 5), ('c', 9)]
