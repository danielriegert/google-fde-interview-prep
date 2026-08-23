#  API Log Parsing & Top-K Error SignaturesExtracts error signatures from a stream of log strings and tracks the top-$K$ most frequent ones using a hash map and a min-heap.

import re
from collections import Counter
import heapq

def get_top_k_errors(log_stream: list[str], k: int) -> list[tuple[str, int]]:
    """
    Parses unstructured logs to extract error signatures and returns top-K frequencies.
    """
    error_counts = Counter()
    
    # Regex to match HTTP error codes or explicit error keywords
    error_pattern = re.compile(r"(ERROR|CRITICAL|5\d{2})[:\s]+([\w\s\-\.]+)", re.IGNORECASE)
    
    for log in log_stream:
        match = error_pattern.search(log)
        if match:
            # Normalize signature by stripping whitespace and lowercasing
            signature = match.group(0).strip().lower()
            error_counts[signature] += 1
            
    # Use a min-heap to efficiently track top K elements
    # Heap stores tuples of (frequency, signature)
    min_heap = []
    for sig, freq in error_counts.items():
        heapq.heappush(min_heap, (freq, sig))
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    # Return sorted descending by frequency
    return [(sig, freq) for freq, sig in sorted(min_heap, reverse=True)]

# Complexity:
# Time: O(N log K) where N is the number of logs, since heap size is capped at K.
# Space: O(U) where U is the number of unique error signatures stored in memory.

#-----------------------------------------------------------------------------------
# 2. Service Dependency & Deployment Order Validation
# Performs a topological sort on microservices. If a cycle exists, it isolates and returns the exact dependency cycle path for debugging

#-----------------------------------------------------------------------------------
# 3. Document Permission & Access Control FilterFilters search or RAG candidate chunks against a user's security clearances and group memberships in $O(1)$ lookup time per documen
def filter_authorized_documents(documents: list[dict], user_profile: dict) -> list[dict]:
    """
    Filters documents based on user groups and security classification levels.
    """
    user_groups = set(user_profile.get("groups", []))
    user_clearance_level = user_profile.get("clearance_level", 0)
    
    authorized_docs = []
    for doc in documents:
        doc_acl_groups = set(doc.get("acl_groups", []))
        doc_min_clearance = doc.get("min_clearance", 0)
        
        # Check clearance level first (numeric comparison)
        if user_clearance_level < doc_min_clearance:
            continue
            
        # Check if user belongs to at least one required ACL group (set intersection)
        if doc_acl_groups and not (doc_acl_groups & user_groups):
            continue
            
        authorized_docs.append(doc)
        
    return authorized_docs

# Complexity:
# Time: O(D) where D is the number of documents (set operations are average O(1)).
# Space: O(1) auxiliary space beyond output list storage.

#-----------------------------------------------------------------------------------
# 4. Enterprise Maintenance Window Interval Merging
# Merges overlapping maintenance intervals and computes total aggregate downtime.
def merge_maintenance_windows(intervals: list[list[int]]) -> tuple[list[list[int]], int]:
    """
    Merges overlapping time intervals [start, end] and calculates total downtime.
    """
    if not intervals:
        return [], 0
        
    # Sort intervals by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    total_downtime = 0
    
    for current in sorted_intervals[1:]:
        prev_start, prev_end = merged[-1]
        curr_start, curr_end = current
        
        if curr_start <= prev_end: # Overlap detected
            merged[-1][1] = max(prev_end, curr_end)
        else:
            merged.append(current)
            
    # Calculate aggregate duration
    for start, end in merged:
        total_downtime += (end - start)
        
    return merged, total_downtime

# Complexity:
# Time: O(N log N) due to sorting.
# Space: O(N) to store merged intervals.

#-----------------------------------------------------------------------------------
# 5. Context-Window Token Packing
# Packs textual context chunks into an LLM context window using a greedy utility-to-cost ratio strategy (Knapsack variant).
def pack_context_chunks(chunks: list[dict], max_tokens: int) -> list[dict]:
    """
    Greedily selects chunks maximizing relevance score without exceeding token budget.
    Chunk format: {'id': str, 'text': str, 'tokens': int, 'score': float}
    """
    # Calculate utility ratio: relevance score per token
    scored_chunks = []
    for chunk in chunks:
        if chunk['tokens'] > 0:
            ratio = chunk['score'] / chunk['tokens']
            scored_chunks.append((ratio, chunk))
            
    # Sort descending by value density ratio
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    packed = []
    current_tokens = 0
    
    for _, chunk in scored_chunks:
        if current_tokens + chunk['tokens'] <= max_tokens:
            packed.append(chunk)
            current_tokens += chunk['tokens']
            
    return packed

# Complexity:
# Time: O(N log N) for sorting chunks by utility ratio.
# Space: O(N) to store sorted references.

#-----------------------------------------------------------------------------------
# 6. Streaming Event Deduplication (Rolling Window)
# Deduplicates incoming real-time events using a sliding time window with bounded memory.

from collections import deque

class StreamingDeduplicator:
    """
    Deduplicates events if identical signature occurs within sliding window T seconds.
    """
    def __init__(self, window_seconds: int):
        self.window_seconds = window_seconds
        self.seen_events = set()
        self.queue = deque() # Stores tuples of (timestamp, event_signature)
        
    def process_event(self, timestamp: int, signature: str) -> bool:
        """Returns True if event is unique, False if it's a duplicate within window."""
        # Evict expired elements from the sliding window
        while self.queue and timestamp - self.queue[0][0] > self.window_seconds:
            _, old_sig = self.queue.popleft()
            self.seen_events.discard(old_sig)
            
        if signature in self.seen_events:
            return False # Duplicate
            
        self.seen_events.add(signature)
        self.queue.append((timestamp, signature))
        return True

# Complexity:
# Time: O(1) amortized per event (each event is pushed and popped at most once).
# Space: O(M) where M is the maximum number of unique events fitting inside time window T.

#-----------------------------------------------------------------------------------
# 7. Nested JSON Payload Flattener
# Recursively flattens deeply nested JSON dictionaries into dot-notation key-value pairs.

# The nested JSON can be thought of as a tree: dicts/lists are internal nodes,
# scalars are leaves, and keys/indices are the edge labels connecting them.
# Flattening = DFS (pre-order) over that tree, accumulating the root-to-leaf
# path as we descend, and recording one output entry per leaf reached.
#
# Example input:
# {
#     "user": {
#         "name": "Alice",
#         "address": {"city": "NYC", "zip": "10001"}
#     },
#     "roles": ["admin", "editor"],
#     "active": True
# }
#
# Tree representation:
#                     root
#           /          |          \
#        user        roles      active
#       /    \       /   \         |
#    name   address  [0]  [1]     True
#     |      /   \    |    |
#   "Alice" city  zip "admin" "editor"
#           |     |
#         "NYC" "10001"
#
# Expected output:
# {
#     "user.name": "Alice",
#     "user.address.city": "NYC",
#     "user.address.zip": "10001",
#     "roles[0]": "admin",
#     "roles[1]": "editor",
#     "active": True
# }

def flatten_json(nested_json: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flattens a nested dictionary into dot-notation key-value pairs.
    """
    items = {}
    for k, v in nested_json.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        elif isinstance(v, list):
            # Optional: handle lists by indexing
            for i, item in enumerate(v):
                list_key = f"{new_key}[{i}]"
                if isinstance(item, dict):
                    items.update(flatten_json(item, list_key, sep=sep))
                else:
                    items[list_key] = item
        else:
            items[new_key] = v
            
    return items

# Complexity:
# Time: O(N) where N is the total number of key-value nodes across all nesting levels.
# Space: O(D) where D is the maximum depth of recursion stack.

#-----------------------------------------------------------------------------------
# 8. API Pagination & Rate-Limited Retry Queue
# Simulates a retry worker handling rate limits (429) with backoff state management.
import time

def simulate_paginated_api_fetch(fetch_page_fn, max_retries: int = 3) -> list:
    """
    Fetches pages sequentially while handling rate limits with exponential backoff.
    """
    results = []
    page_token = None
    
    while True:
        retries = 0
        success = False
        response = None
        
        while retries <= max_retries and not success:
            try:
                response = fetch_page_fn(page_token)
                if response.get("status_code") == 429:
                    raise ConnectionError("Rate limited (429)")
                success = True
            except (ConnectionError, TimeoutError):
                retries += 1
                if retries > max_retries:
                    raise RuntimeError("Max retries exceeded due to persistent rate limiting.")
                # Exponential backoff with jitter
                sleep_time = (2 ** retries) * 0.1
                time.sleep(sleep_time)
                
        results.extend(response.get("data", []))
        page_token = response.get("next_page_token")
        if not page_token:
            break
            
    return results

# Complexity:
# Time: O(P * R) where P is the number of pages and R is retry overhead.
# Space: O(Total Records Accumulated).

#-----------------------------------------------------------------------------------
# 10. Agent Tool-Call Loop Detector
# Detects agentic execution loops using a sliding sequence window.
from collections import deque
import json

class AgentLoopDetector:
    """
    Monitors tool call traces to detect execution loops.
    """
    def __init__(self, history_limit: int = 5):
        self.history_limit = history_limit
        self.call_history = deque(maxlen=history_limit)
        
    def check_loop(self, tool_name: str, arguments: dict) -> bool:
        """
        Returns True if a repeated execution sequence is detected (infinite loop).
        """
        # Create a deterministic signature of the tool call
        signature = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"
        
        # Check if signature matches recent sequence history
        if signature in self.call_history:
            return True
            
        self.call_history.append(signature)
        return False

# Complexity:
# Time: O(K) where K is the fixed history window size for lookup checks.
# Space: O(K) bounded memory usage storing recent tool signatures.

#-----------------------------------------------------------------------------------
from collections import defaultdict
import re
from typing import List, Dict

class InvertedIndexSearchEngine:
    """
    In-memory search engine using an inverted index with support for 
    boolean retrieval (AND/OR) and exact phrase matching.
    """
    def __init__(self):
        # Maps token -> set of doc_ids containing the token
        self.index: Dict[str, set[int]] = defaultdict(set)
        
        # Maps doc_id -> list of tokens in exact sequential order (for phrase search)
        self.doc_token_sequences: Dict[int, List[str]] = {}

    def _tokenize(self, text: str) -> List[str]:
        """
        Normalizes text: strips punctuation, lowercases, and splits by whitespace.
        """
        if not text:
            return []
        # Keep alphanumeric tokens only, convert to lowercase
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def index_document(self, doc_id: int, text: str) -> None:
        """
        Indexes a document by parsing its tokens and updating the inverted index 
        and sequential token map.
        """
        tokens = self._tokenize(text)
        self.doc_token_sequences[doc_id] = tokens
        
        # Add doc_id to the posting list for each unique token in the document
        for token in set(tokens):
            self.index[token].add(doc_id)

    def search(self, query_tokens: List[str], match_all: bool = True) -> List[int]:
        """
        Searches the index for query tokens. 
        If match_all is True, returns documents containing ALL tokens (AND).
        If match_all is False, returns documents containing ANY of the tokens (OR).
        """
        normalized_queries = self._tokenize(" ".join(query_tokens))
        if not normalized_queries:
            return []
        
        # Retrieve posting lists for each query token
        posting_lists = [self.index[token] for token in normalized_queries]
        
        if match_all:
            # Optimization: Sort posting lists by size (ascending) to perform 
            # intersections starting with the smallest sets first.
            posting_lists.sort(key=len)
            
            # Start with the smallest set
            result_set = set(posting_lists[0])
            for p_list in posting_lists[1:]:
                # If any posting list is empty, intersection is immediately empty
                if not result_set:
                    break
                # Optimized intersection: Python's set intersection handles 
                # O(min(len(s1), len(s2))) under the hood.
                result_set.intersection_update(p_list)
        else:
            # Union for 'any' matching
            result_set = set()
            for p_list in posting_lists:
                result_set.update(p_list)
                
        # Return sorted list of matching document IDs for determinism
        return sorted(list(result_set))

    def search_phrase(self, phrase: str) -> List[int]:
        """
        Follow-up Extension: Exact phrase search.
        Matches multi-word phrases sequentially (e.g., 'connection timeout').
        """
        phrase_tokens = self._tokenize(phrase)
        if not phrase_tokens:
            return []
            
        # Step 1: Candidate filtering using the first token's posting list
        first_token = phrase_tokens[0]
        candidate_docs = self.index.get(first_token, set())
        
        if not candidate_docs:
            return []
            
        matching_docs = []
        phrase_len = len(phrase_tokens)
        
        # Step 2: Verification step over candidate sequences
        for doc_id in candidate_docs:
            tokens = self.doc_token_sequences[doc_id]
            # Scan the document sequence for the exact contiguous phrase match
            for i in range(len(tokens) - phrase_len + 1):
                if tokens[i:i + phrase_len] == phrase_tokens:
                    matching_docs.append(doc_id)
                    break # Found in this doc, move to next document
                    
        return sorted(matching_docs)
