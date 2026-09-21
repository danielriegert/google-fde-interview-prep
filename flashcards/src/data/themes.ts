import type { Theme } from '../types';

export const THEMES: Theme[] = [
  { id: 'complexity', title: 'Complexity & Interview Approach', description: 'Big-O, reading complexity off code, and the interview playbook.' },
  { id: 'python', title: 'Python Toolkit', description: 'lists, dicts, sets, Counter/defaultdict, sorting helpers and handy tricks.' },
  { id: 'recursion', title: 'Recursion & Backtracking', description: 'Base cases, call-stack thinking, and the backtracking skeleton.' },
  { id: 'arrays', title: 'Arrays, Strings & Prefix Sums', description: 'Traversal, matrices, prefix sums and difference arrays.' },
  { id: 'two-pointers', title: 'Two Pointers & Sliding Window', description: 'Converging, fast/slow, and window templates.' },
  { id: 'linked-list', title: 'Linked List', description: 'Dummy heads, reversal, Floyd cycle detection, copying.' },
  { id: 'hash-table', title: 'Hash Table', description: 'Hashing, collisions, counting and prefix-sum + map patterns.' },
  { id: 'stack-queue', title: 'Stack, Queue & Monotonic', description: 'LIFO/FIFO, monotonic stack and queue.' },
  { id: 'heap', title: 'Heap / Priority Queue', description: 'Heap mechanics, top-K, two heaps, lazy deletion.' },
  { id: 'sorting', title: 'Sorting', description: 'Algorithm trade-offs, quickselect, bucket sort, custom comparators.' },
  { id: 'binary-search', title: 'Binary Search', description: 'Interval conventions, bounds, rotated arrays, answer-space search.' },
  { id: 'trees', title: 'Trees, BST & Trie', description: 'Traversals, BST ops, LCA, tries, BIT / segment tree concepts.' },
  { id: 'graphs', title: 'Graphs', description: 'BFS/DFS, topological sort, union-find, Dijkstra, MST.' },
  { id: 'dp', title: 'Dynamic Programming', description: 'The four steps, 1D/2D DP, knapsack, Kadane.' },
  { id: 'greedy', title: 'Greedy', description: 'When greedy works, exchange argument, and when it fails.' },
  { id: 'bits', title: 'Bit Manipulation', description: 'Bit ops, XOR tricks and masks.' },
  { id: 'technique', title: 'Pick the Technique', description: 'Problem signal -> which technique to reach for.' },
  { id: 'problems', title: 'Problem Patterns (Easy/Medium)', description: 'Approach cards for specific non-Hard LeetCode problems.' },
  { id: 'fde', title: 'FDE Practical Coding', description: 'Real-world coding exercises: top-K, dedup, retries, inverted index...' },
];
