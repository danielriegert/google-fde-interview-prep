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
