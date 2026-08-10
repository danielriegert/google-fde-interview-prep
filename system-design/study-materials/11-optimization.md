# Optimizin and Meassuring Latency & Througpput

- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/latency

# Optimizing Cost

- prompt caching, etc.
- model selection

## Context caching

- Cache the token-processing cost of a large, **repeated** prefix (a long
  system prompt, a big retrieved document, few-shot examples) so it isn't
  re-paid on every request that reuses it — you pay full price once to
  create the cache, then a reduced rate per request that hits it.
- Cuts both **cost** (cached tokens are billed at a fraction of the
  standard input-token rate) and **latency** (the model skips
  re-processing the cached prefix, so time-to-first-token drops).
- GCP: **Vertex AI / Gemini context caching** — create an explicit cache
  keyed to a fixed prefix, with a TTL; subsequent requests reference the
  cache instead of resending the full content.
- Best fit: high-volume traffic sharing a large, unchanging prefix (a RAG
  system prompt reused across many users' queries, a coding agent with a
  large fixed codebase context) — not worth it for one-off or highly
  variable prompts, since the cache-creation cost only pays off once it's
  reused enough times before the TTL expires.

## Context / State Optimization

Compaction: when a conversation gets long, summarize the older parts into a compact form and discard the raw history, keeping only what's needed to continue (recent messages, key decisions, open threads). Claude Code does this automatically when nearing context limits.

Sub-agents / isolation: spin up a separate agent with its own context window to do a bounded task (e.g., "search the codebase for X"), and have it return only a condensed result to the parent. The parent's context stays clean; the exploratory noise stays isolated. This is what the Agent tool in this environment does.

Just-in-time retrieval instead of eager loading: rather than pre-loading entire files, databases, or docs into context up front, give the agent lightweight references (file paths, IDs, links) and let it fetch content only when it's actually needed. This mirrors how humans work — you don't memorize a filesystem, you navigate it.

Structured note-taking / scratchpads: have the agent persist important intermediate state (a todo list, key facts, a plan) to a file or memory outside the context window, then re-read it as needed rather than keeping everything live in-context. This also survives context resets.

Tool result minimization: truncate or summarize large tool outputs before they enter context — e.g., returning a diff instead of a full file, or the first N rows of a query result with an offer to fetch more.

Deferred tool loading: instead of listing every possible tool's full schema in the system prompt (there might be hundreds), keep tool definitions off to the side and load a tool's schema only when it looks relevant to the current task. This is literally the ToolSearch mechanism I use.

## Batch LLM calls

- For requests that aren't latency-sensitive (bulk classification, offline
  eval runs, nightly summarization/enrichment jobs), submit a large set of
  prompts as one **batch** job instead of one synchronous call per prompt.
- Cuts **cost** — batch inference is priced at a discount vs. standard
  synchronous requests (roughly half, in line with other providers' batch
  APIs) — in exchange for **no latency guarantee**: the job is processed
  asynchronously and results land within a completion window (e.g. hours),
  not per-request in real time.
- GCP: **Vertex AI batch prediction** — submit inputs (e.g. a file/table
  of prompts), poll or get notified on completion, read outputs in bulk;
  no need to manage your own request queue/concurrency/retry logic.
- Complements model tier selection and context caching (file 05 §10) as a
  third cost lever — but only applies where the workload can tolerate
  async, non-interactive turnaround; never use it for anything on a
  user-facing request path.
