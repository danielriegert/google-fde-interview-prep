# RAG — Retrieval-Augmented Generation

## 1. Why RAG exists

LLMs have three structural limits RAG addresses:
- **Knowledge cutoff** — model doesn't know about data after training, or
  private/enterprise data it never saw.
- **Hallucination** — model will confidently invent facts when it doesn't
  know the answer.
- **No cost-effective way to keep facts current via fine-tuning** —
  fine-tuning is slow, expensive, and bad at injecting precise facts you
  need updated daily/hourly.

RAG's fix: retrieve relevant, current, private documents at query time and
put them **in the prompt** so the model generates grounded in real text
instead of parametric memory alone.

## 2. The canonical pipeline

```
[Source docs] → chunk → embed → [Vector Index]
                                        ▲
                                        │ similarity search
[User query] → embed query ────────────┘
                                        │
                              top-k chunks retrieved
                                        │
                          (optional) re-rank / filter
                                        │
                    augment prompt: query + retrieved context
                                        │
                                  LLM generates answer
                                        │
                          (optional) cite sources / verify
```

Two phases to always separate in your head: **ingestion** (offline,
batch/streaming) and **query-time retrieval + generation** (online, latency
sensitive).

## 3. Ingestion: chunking

Why chunk at all: embeddings compress meaning into a fixed vector; a
whole 50-page doc embedded as one vector loses too much specificity to
match a narrow query. Chunks need to be small enough to be specific, big
enough to retain context.

| Strategy | How | Tradeoff |
|---|---|---|
| Fixed-size (e.g. 512 tokens) | Split by token/char count, often with overlap (10-20%) | Simple, fast; can cut sentences/ideas in half |
| Recursive/structure-aware | Split on paragraph → sentence boundaries, respecting document structure (headers, markdown) | Better semantic coherence; more engineering |
| Semantic chunking | Embed sentences, split where embedding similarity drops (topic shift) | Best coherence; expensive, non-deterministic boundaries |
| Hierarchical / parent-child | Index small chunks for precise matching, but retrieve the larger parent chunk/section for generation context | Best of both — precise recall, rich context; more index complexity |

**Overlap** between chunks (e.g. 50-100 tokens) prevents losing information
that straddles a chunk boundary.

**Metadata matters as much as text**: store source, section title, doc
date, ACL/permission tags, doc type alongside each chunk — needed for
filtering, citation, and access control at query time.

## 4. Embeddings & vector search

- **Embedding model** maps text → dense vector (e.g. 768/1536 dims) such
  that semantically similar text has vectors close together.
- **Distance metrics**: cosine similarity (most common, scale-invariant),
  dot product (fast, used when vectors are normalized), Euclidean/L2.
- **Exact vs approximate nearest neighbor (ANN)**: exact search is O(n) per
  query — too slow at scale. ANN indexes trade a small accuracy loss for
  huge speed gains.
  - **HNSW** (Hierarchical Navigable Small World): graph-based, very fast
    query, good recall, higher memory footprint. Default choice for most
    managed vector DBs (Vertex AI Vector Search, pgvector, Pinecone).
  - **IVF** (Inverted File Index): clusters vectors, searches nearest
    clusters only. Lower memory, needs a training/clustering step, tunable
    recall/speed via `nprobe`.
- **Vector DB options**: Vertex AI Vector Search (managed, GCP-native),
  pgvector (Postgres extension, good if already on Cloud SQL/AlloyDB),
  Pinecone/Weaviate/Elastic (third-party managed).

## 5. Hybrid search & re-ranking

Pure vector search misses exact keyword matches (IDs, part numbers, exact
phrases) — embeddings blur precise tokens. Fix: **hybrid search**.

- **Keyword/lexical search**: BM25 (classic TF-IDF-family ranking) —
  excellent for exact term matches.
- **Hybrid**: run both vector and BM25, combine scores (e.g. **Reciprocal
  Rank Fusion**) or weighted sum.
- **Re-ranking**: retrieve a larger candidate set (top 50-100) cheaply via
  vector/hybrid search, then apply a more expensive but more accurate
  **cross-encoder** re-ranker to re-score and cut to top-k (e.g. top 5) that
  actually go in the prompt. Cross-encoders jointly encode query+doc
  (vs. bi-encoders that embed separately) — much better relevance,
  much slower, so only run on the shortlist.

## 6. Query-time techniques

- **Query rewriting/expansion**: reformulate a vague user query into a
  better search query (e.g. resolve pronouns, add synonyms) via a cheap
  LLM call before retrieval.
- **HyDE (Hypothetical Document Embeddings)**: ask the LLM to write a
  hypothetical answer, embed *that*, and search with it — the hypothetical
  answer's embedding often matches real docs better than the raw question.
- **Multi-query retrieval**: generate several reformulated queries, retrieve
  for each, merge/dedupe results — improves recall for ambiguous questions.
- **Query routing**: classify the query first (e.g. "this needs SQL
  lookup" vs "this needs doc search") and route to the right retriever —
  this is where RAG starts to blend into agentic tool-use (see file 02).

## 7. Grounding & citations

- Instruct the model to answer **only** from provided context, and to say
  "I don't know" if the context doesn't contain the answer — reduces but
  doesn't eliminate hallucination.
- Have the model emit citations (chunk IDs / source links) alongside claims
  — lets you verify and lets the UI show provenance.
- **Faithfulness/groundedness check**: a secondary pass (often another LLM
  call, or NLI-style entailment model) verifies the generated answer is
  actually supported by the retrieved context — catches hallucination
  before it reaches the user.

## 8. Advanced RAG patterns

- **Self-RAG / corrective RAG**: model critiques its own retrieval —
  "were these chunks actually relevant?" — and re-retrieves or falls back
  if not.
- **Agentic RAG**: retrieval becomes a *tool* the agent calls, possibly
  multiple times, interleaved with reasoning (vs. a fixed one-shot
  retrieve-then-generate pipeline). Handles multi-hop questions
  ("compare X's Q1 and Q3 revenue" needs two retrievals).
- **GraphRAG**: build a knowledge graph from documents (entities +
  relationships), retrieve via graph traversal in addition to/instead of
  vector similarity — better for questions requiring relational reasoning
  across many docs ("summarize everything connected to project X").

## 9. Evaluating RAG quality

- **Retrieval metrics**: precision@k, recall@k, MRR (mean reciprocal rank)
  — did we retrieve the right chunks at all?
- **Generation metrics** (often via LLM-as-judge or RAGAS-style
  frameworks): *faithfulness* (is the answer supported by context?),
  *answer relevancy* (does it address the question?), *context precision*
  (is retrieved context actually used/relevant?).
- See file 03 for the full evaluation/observability picture.

## 10. Failure modes & mitigations

| Failure | Cause | Mitigation |
|---|---|---|
| Retrieval miss | Query/doc vocabulary mismatch, bad chunking | Hybrid search, query rewriting, better chunking |
| Stale answers | Index not updated after source changes | Incremental re-indexing, CDC pipelines, freshness metadata + filtering |
| Lost context at chunk boundary | Fixed-size chunking cuts mid-idea | Overlap, semantic/structure-aware chunking, parent-child retrieval |
| Hallucination despite retrieval | Model ignores context or fills gaps | Strict grounding prompts, faithfulness check, "I don't know" fallback |
| Irrelevant chunks crowd out good ones | Weak similarity search, no re-ranking | Cross-encoder re-ranking, better embedding model |
| Unauthorized data exposure | No access control at retrieval | ACL/permission metadata filtering at query time (see file 04) |
| Context window overflow | Too many/too-large chunks stuffed in prompt | Re-ranking to cut top-k, summarization of retrieved chunks, hierarchical retrieval |

## 11. Data freshness: batch vs streaming ingestion

- **Batch**: nightly/hourly re-index jobs (Dataflow/Airflow) — simple,
  fine for docs that change infrequently.
- **Streaming/CDC**: change-data-capture from source systems (e.g.
  Pub/Sub triggered on doc update) → incremental embed + upsert into
  vector index — needed when freshness SLA is tight (e.g. inventory,
  ticket status).
- Always version/tag chunks with a timestamp so stale entries can be
  filtered or superseded, not just appended forever.

---

## Could you explain/draw this cold?

- [ ] Draw the full ingestion + query-time RAG pipeline from memory
- [ ] Explain HNSW vs IVF and when you'd pick each
- [ ] Explain why hybrid search beats pure vector search, with an example
      query it fixes
- [ ] Explain bi-encoder vs cross-encoder and why re-ranking uses a
      two-stage retrieve-then-rerank design instead of cross-encoding
      everything
- [ ] Name 3 chunking strategies and their tradeoffs
- [ ] Explain HyDE and why it can outperform naive query embedding
- [ ] Walk through what breaks and how you'd catch it: a customer says
      the agent gave a wrong, confidently-stated answer about a policy
      that changed yesterday
