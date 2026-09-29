# 1. Merging Intervals
# Concept: Sort by start time, maintain a running result list, and merge overlapping blocks by extending the end time.
def merge_intervals(intervals):
  if not intervals:
    return []

  # Step 1: Sort intervals by their start times. This guarantees that
  # any overlapping intervals will sit right next to each other.
  intervals.sort(key=lambda x: x[0])

  # Initialize the merged list with the very first interval
  merged = [intervals[0]]

  # Step 2: Iterate through the remaining intervals
  for current in intervals[1:]:
    prev = merged[-1]  # Get the last interval added to our merged list

    # Step 3: Check for overlap (current interval starts at or before previous ends)
    if current[0] <= prev[1]:
      # Merge by extending the previous interval's end to the max of both ends
      prev[1] = max(prev[1], current[1])
    else:
      # No overlap; safe to append the current interval as a distinct block
      merged.append(current)

  return merged


# --- Example ---
# Input:
intervals_input = [[1, 3], [2, 6], [8, 10], [15, 18]]
# Output:
# [[1, 6], [8, 10], [15, 18]]
print(merge_intervals(intervals_input))

# 2. Checking for Overlaps
# Concept: Two intervals overlap if and only if the later i.e. max of their start times is strictly less than the earlier i.e. min of their end times.
def is_overlapping(interval_a, interval_b):
  start1, end1 = interval_a
  start2, end2 = interval_b

  # Step 1: max(start1, start2) finds the latest point where both intervals have started.
  # Step 2: min(end1, end2) finds the earliest point where one of the intervals finishes.
  # If the latest start happens BEFORE the earliest end, they must overlap.
  return max(start1, start2) < min(end1, end2)


# --- Example ---
# Input 1:
a, b = [1, 5], [3, 8]
# Output 1: True (They overlap from 3 to 5)
print(is_overlapping(a, b))

# Input 2:
c, d = [1, 3], [4, 6]
# Output 2: False (No overlap)
print(is_overlapping(c, d))

# 3. Counting Overlapping Intervals (Sweep-Line Algorithm)
# Concept: Break intervals into discrete start (+1) and end (-1) events, sort them chronologically, and track the peak active load.
def max_overlapping_intervals(intervals):
  events = []

  # Step 1: Deconstruct each interval into two independent timeline events
  for start, end in intervals:
    events.append((start, 1))  # +1 means an interval begins (resource acquired)
    events.append((end, -1))  # -1 means an interval ends (resource freed)

  # Step 2: Sort events chronologically by time.
  # If two events occur at the exact same timestamp, Python naturally sorts
  # -1 before 1 (ending before starting), which handles touching edges accurately.
  events.sort(key=lambda x: (x[0], x[1]))

  max_active = 0
  current_active = 0

  # Step 3: Sweep through timeline events sequentially
  for time, event_type in events:
    current_active += event_type  # Adjust active count based on event type
    max_active = max(max_active, current_active)  # Track the peak concurrent load

  return max_active


# --- Example ---
# Input: Intervals representing overlapping tasks/meetings
intervals_input = [[1, 4], [2, 5], [7, 9], [3, 6]]
# Output: 3 (At time 3, intervals [1,4], [2,5], and [3,6] all overlap simultaneously)
print(max_overlapping_intervals(intervals_input))

# 4. Interval Partitioning (Meeting Rooms / Group Allocation)
# Concept: Track ongoing resource end times using a Min-Heap to reuse groups efficiently.
import heapq


def min_partition_groups(intervals):
  # Step 1: Sort intervals by start time to process them chronologically
  intervals.sort(key=lambda x: x[0])
  min_heap = []  # Stores the end times of currently active groups/rooms

  for start, end in intervals:
    # Step 2: Check if the earliest ending group finishes before the current interval starts
    if min_heap and min_heap[0] <= start:
      # Reuse that group by popping its previous end time out of the heap
      heapq.heappop(min_heap)

    # Step 3: Allocate or update the group with the current interval's end time
    heapq.heappush(min_heap, end)

  # Step 4: The maximum size the heap ever reaches represents the minimum groups needed
  return len(min_heap)


# --- Example ---
# Input: Meeting times
intervals_input = [[0, 30], [5, 10], [15, 20]]
# Output: 2 (Room 1 handles [0, 30]; Room 2 handles [5, 10] and is reused for [15, 20])
print(min_partition_groups(intervals_input))

# 5. Finding Gaps
# Concept: Sweep through sorted intervals within a defined timeframe to spot unallocated spaces.
def find_gaps(intervals, day_start, day_end):
  if not intervals:
    return [(day_start, day_end)]

  # Step 1: Sort intervals by start time
  intervals.sort(key=lambda x: x[0])
  gaps = []
  current_end = day_start  # Tracks the furthest point reached so far

  # Step 2: Scan through the intervals
  for start, end in intervals:
    # If the current interval starts after our timeline pointer, there's a gap
    if start > current_end:
      gaps.append((current_end, start))
    # Push our tracker forward to the end of the current interval
    current_end = max(current_end, end)

  # Step 3: Check if there is remaining time between the last interval and day_end
  if current_end < day_end:
    gaps.append((current_end, day_end))

  return gaps


# --- Example ---
# Input:
intervals_input = [[9, 10], [12, 13]]
day_start, day_end = 8, 17
# Output: [(8, 9), (10, 12), (13, 17)]
print(find_gaps(intervals_input, day_start, day_end))

# LC 56: Merge overlapping intervals
"""
1. check if interval is empty
2. sort by start
3. add first element into merged list
4. iterate trough remaining intervals
5. check if current interval start time is equal or less to previous interval (merged[-1]) end
6. if equal or less extend previous interval end time to max end time of current and previous interval
7. if NOT equal or less add interval into merged list

Time Complexity: O(n log n), where n is the number of intervals. 
This is dominated by the sorting step, while the subsequent linear scan takes O(n) time.

Space Complexity: O(n) to store the output array.
"""

def merge(intervals):
    if not intervals:
        return []
    
    # Sort intervals based on the starting value
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # If current overlaps with the last merged interval, merge them
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
            
    return merged

# LC 57
# Insert new interval into sorted (by start time) list of intervals that are not overlapping.
# After insert intervals should still be sorted and not overlapping.
"""
1. Add all non-overlapping intervals to result list. check if end of current interval is less i.e. before start of interval to insert
2. Process overlapping intervals and merge them then add to result list
3. Add remaining intervals

Time Complexity: O(n), where n is the number of intervals. Each interval is visited at most once.
Space Complexity: O(n) to store and return the result array.
"""
def insert(intervals, newInterval):
    result = []
    i = 0
    n = len(intervals)
    
    # Phase 1: Add all intervals that come before newInterval i.e. end is less than start of new interval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # ToDo: understand why we update both start and end i.e. this is different from merging intervals (e.g. LC 56)
    # Phase 2: Merge overlapping intervals (i.e. interval start is less or equal to new interval end) with newInterval
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1
    result.append(newInterval)
    
    # Phase 3: Add all remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
        
    return result

# LC 452
"""
1. Sort by End Coordinate: 
Sort the balloons based on their end positions in ascending order (points[i][1]). 
Sorting by end time ensures that we greedily place our arrows as far right as possible,
 maximizing the chance of catching subsequent overlapping balloons.
2. Greedy Arrow Placement: 
Shoot the first arrow at the end coordinate of the first balloon.
3. Scan and Count:
 Iterate through the remaining balloons. If a balloon starts after our current arrow's position (points[i][0] > current_arrow_pos),
   it means it cannot be burst by the existing arrow. You must shoot a new arrow and update your target position to this new balloon's 
   end coordinate.

Time Complexity: O(n log n), where n is the number of balloons, due to the initial sorting step. 
The subsequent linear scan runs in O(n) time.
Space Complexity: O(1).
"""
def findMinArrowShots(points):
    if not points:
        return 0
    
    # Sort balloons by their end coordinates
    points.sort(key=lambda x: x[1])
    
    arrows = 1
    current_arrow_pos = points[0][1]
    
    for i in range(1, len(points)):
        # If the current balloon starts after our arrow position, we need a new arrow
        if points[i][0] > current_arrow_pos:
            arrows += 1
            current_arrow_pos = points[i][1]
            
    return arrows

# LC 435
"""
1. Sort by End Time: 
Sort the intervals based on their end positions in ascending order (intervals[i][1]). 
By picking the interval that ends the earliest, you leave the maximum possible room for all subsequent intervals.

2. Greedy Selection: 
Keep track of the end time of the last interval you decided to keep (prev_end).

3. Scan and Check Overlaps: 
Iterate through the remaining intervals:
If the current interval starts before the previous interval ends (intervals[i][0] < prev_end), they overlap. You are forced to remove this interval, so increment your removal count.
If they do not overlap, you can safely keep this interval and update your prev_end to this interval's end time.

Time Complexity: O(n log n), where n is the number of intervals, due to the initial sorting step. 
The subsequent linear scan runs in O(n) time.
Space Complexity: O(1).
"""
def eraseOverlapIntervals(intervals):
    if not intervals:
        return 0

    # ToDo: understand why we sort by end time
    # Sort intervals by their end times
    intervals.sort(key=lambda x: x[1])
    
    removals = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        # If current interval starts before the previous one ends, it's an overlap
        if intervals[i][0] < prev_end:
            removals += 1
        else:
            # No overlap, update the end pointer to the current interval's end
            prev_end = intervals[i][1]
            
    return removals

# ToDo: Review
# LC Meeting rooms 2
"""
To find the minimum number of conference rooms required, we need to find the maximum number of overlapping meetings occurring at 
any single point in time.

Instead of checking every interval against every other interval, we can use the Chronological Ordering (Two-Pointer) technique:

    Separate and Sort Times: Extract all start times into one sorted list and all end times into another sorted list.

    Sweep-Line Pointer Logic: Use two pointers (s_ptr for starts, e_ptr for ends) to simulate a timeline.

        If the next meeting starts before the earliest ongoing meeting ends (starts[s_ptr] < ends[e_ptr]), it means a new room is needed.
          Increment our room count and advance the start pointer.

        If a meeting has ended (starts[s_ptr] >= ends[e_ptr]), a room has been freed up. 
        Decrement our room count and advance the end pointer.

    Track Peak Usage: Keep a running maximum of rooms used at any point during the sweep.

Time Complexity: O(n log n), where n is the number of intervals, dominated by the sorting of the start and end time arrays. 
The linear scan runs in O(n) time.

Space Complexity: O(n) to store the separated start and end lists.
"""
def minMeetingRooms(intervals):
    if not intervals:
        return 0
    
    # Separate and sort start and end times independently
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = 0
    max_rooms = 0
    s_ptr = 0
    e_ptr = 0
    n = len(intervals)
    
    while s_ptr < n:
        # If a meeting starts before the previous one ends, we need another room
        if starts[s_ptr] < ends[e_ptr]:
            rooms += 1
            s_ptr += 1
        else:
            # Otherwise, a meeting has finished, freeing up a room
            rooms -= 1
            e_ptr += 1
            
        max_rooms = max(max_rooms, rooms)
        
    return max_rooms


# LC 2345
from collections import Counter
from typing import List

class Solution:
    def visibleMountains(self, peaks: List[List[int]]) -> int:
        # Convert peaks to base intervals [left, right]
        intervals = [(x - y, x + y) for x, y in peaks]
        
        # Count frequencies to handle duplicate/identical mountains
        counts = Counter(intervals)
        
        # Sort by left endpoint ascending, then right endpoint descending
        intervals.sort(key=lambda x: (x[0], -x[1]))
        
        visible_count = 0
        max_right = float('-inf')
        
        for l, r in intervals:
            # If the current mountain is strictly contained within a previous one, skip it
            if r <= max_right:
                continue
            
            # Update the max right boundary seen so far
            max_right = r
            
            # If the mountain is unique (not a duplicate peak), it is visible
            if counts[(l, r)] == 1:
                visible_count += 1
                
        return visible_count