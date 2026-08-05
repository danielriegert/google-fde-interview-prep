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
[Source / load docs] → chunk → enroch cjunks (opitonal) -> embed → [Vector Index]
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

## 3. Preparation Phase

The phase before any pipeline gets built: define the domain, analyze your
content, gather representative test content, and gather test queries. Done
**in parallel**, since they're interrelated — content analysis tells you
what test content/queries to gather, and queries must be answerable from
that content.

- **Determine the solution domain** — nail down business requirements
  first: what questions must the solution answer, what source data is
  needed. This also informs your embedding model choice later.
- **Analyze content** — understand the collection before picking a
  loading/chunking strategy:
  - _Classifications_: product specs vs. contracts vs. training videos,
    etc. — don't over/under-represent any type in test data.
  - _Types/formats_: PDF, DOCX, HTML, MP4, MP3, images, PPT — drives
    technical requirements (parsers, transcription services, vision
    models).
  - _Security constraints_: auth/authz/network isolation on content and
    any embedded media; access-control requirements must carry through
    into the chunking/index design (see file 04).
  - _Structure & characteristics_: decide what to ignore (TOCs, headers/
    footers, watermarks, disclaimers) vs. what adds context; assess
    multi-column layouts, tables, images, video/audio quality, and
    language before choosing a chunking strategy.
- **Gather representative test content** — prefer real content (PII-
  scrubbed) over synthetic; it must be pertinent, representative (aim for
  ≥2 examples per content variant/format), and high quality — garbage
  input degrades every downstream stage.
- **Gather test queries** — collect `(query, context, answer)` triples
  alongside the content:
  - _Synthetic query generation_: chunk docs ad hoc (not your production
    chunking strategy), have an LLM generate Q&A pairs per chunk, then
    have an SME verify them.
  - Include **unanswerable queries** too — you need to test that the
    system says "I don't know" instead of hallucinating when context is
    missing.
  - For multimedia, make sure queries actually require the image/video/
    audio content itself, not just text around it.

This is the offline, evaluation-dataset-building phase — chunking,
retrieval, and evaluation (files below) all get tested against what comes
out of it.

## 4. Ingestion: loading and chunking

Why chunk at all: embeddings compress meaning into a fixed vector; a
whole 50-page doc embedded as one vector loses too much specificity to
match a narrow query. Chunks need to be small enough to be specific, big
enough to retain context. Breaks down the media file into semantically relevant parts that ideally have a single idea or concept.

**Loading vs. chunking — separate phases or combined?** Loading turns a
raw file into an in-memory representation; chunking splits that
representation into pieces. Default to combining them (simpler). Separate
them when you need to: persist the preprocessed doc so you can iterate on
chunking strategy without re-running expensive preprocessing (OCR, image
captioning); run loading/chunking on different compute/hardware; or
bulkhead for security (e.g. PII scrubbing happens in an isolated process
before chunking code — possibly untrusted — ever sees the doc). Avoid
converting to a lossy intermediate format if you do separate them.

### Strategy — document structure drives the choice

Documents sit on a spectrum from fully structured to unstructured, and
that spectrum is the primary signal for which chunking approach to use —
a strong prior, not a fixed rule, worth deviating from only after
experimentation:

| Document structure                                           | Typical approach                        | Examples                                    |
| ------------------------------------------------------------ | --------------------------------------- | ------------------------------------------- |
| **Structured** (fixed layout, data always in the same place) | Prebuilt / custom extraction models     | W-2 forms, insurance cards                  |
| **Semi-structured** (consistent schema, variable layout)     | Document layout analysis (OCR + ML)     | Invoices, receipts, web pages, Markdown     |
| **Inferred** (structure exists but isn't in markup)          | Custom code (regex/structure parsing)   | Legal/regulation text, scripts, specs       |
| **Unstructured** (free-form prose)                           | Sentence-based or fixed-size w/ overlap | Survey feedback, forum posts, emails, notes |

| Strategy                          | How                                                                                                                                 | Tradeoff                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Sentence-based                    | Split on complete sentences                                                                                                         | Simplest fallback; a single sentence often lacks full context                                |
| Fixed-size (e.g. 512 tokens)      | Split by token count (prefer model tokens, e.g. BERT, over raw char count), often with overlap (10-20%)                             | Simple, fast; can cut sentences/ideas in half                                                |
| Recursive/structure-aware         | Split on paragraph → sentence boundaries, respecting document structure (headers, markdown)                                         | Better semantic coherence; more engineering                                                  |
| Semantic chunking                 | Embed sentences, split where embedding similarity drops (topic shift)                                                               | Best coherence; expensive, non-deterministic boundaries                                      |
| Hierarchical / parent-child       | Index small chunks for precise matching, but retrieve the larger parent chunk/section for generation context                        | Best of both — precise recall, rich context; more index complexity                           |
| Custom code (regex/parsing)       | Hand-written parsing against a known/inferred structure (e.g. numbered clauses in a legal doc)                                      | High control, low cost/doc; high engineering cost, brittle to format drift                   |
| Document layout analysis          | OCR + layout ML extracts structure (headers, tables, figures) and text together (e.g. GCP Document AI, Azure Document Intelligence) | Handles scanned/complex layouts well; per-doc service cost, upload/compliance considerations |
| LLM augmentation                  | LLM generates a text description/summary of an image or table, which becomes (or feeds) a chunk                                     | Captures non-text content in retrievable form; slow, highest per-doc $ cost                  |
| Graph-based chunking              | LLM extracts entities/relationships from initial chunks and incrementally builds a knowledge graph (see GraphRAG, section 9)        | Enables relational/multi-hop queries; high engineering + processing cost                     |
| Prebuilt/custom extraction models | Domain-specific model trained (or provided) for a known form type — pulls fields directly instead of generic chunking               | Best quality for structured docs; only works when doc type is well-known/stable              |

**Overlap** between chunks (e.g. 50-100 tokens) prevents losing information
that straddles a chunk boundary.

**Metadata matters as much as text**: store source, section title, doc
date, ACL/permission tags, doc type alongside each chunk — needed for
filtering, citation, and access control at query time.

### Chunking economics

- Treat your chunking strategy as **semi-permanent** — switching it later
  means re-processing and re-indexing the whole corpus, so validate against
  real test content/queries (section 3) before committing to production.
- Approaches that call an LLM per document (image captioning, table
  summarization) dominate processing cost and scale with corpus size —
  budget per-document $ and latency, not just engineering effort.
- Use a cheaper classifier pass first to decide whether an image/table is
  worth the expensive LLM call at all (does it carry information the
  surrounding text doesn't already capture?), instead of captioning
  everything indiscriminately.
- **Cache-aside on content hash**: before generating an expensive
  description (image caption, table summary), hash the content and check a
  cache; only call the model on a miss, then populate the cache. Avoids
  paying twice for identical or reprocessed content across pipeline runs.
- Multimodal content has an architecture choice, not just a chunking one:
  generate a text description at ingestion time and chunk that (cheaper at
  query time, lossy), vs. pass the raw image/table to a multimodal model
  at inference time (higher query-time cost/latency, no information loss).

## 5. Chunk Enrichment

After chunking, enrich each chunk by **cleaning** it and **augmenting** it
with metadata. Both operations extend the chunk's schema and land in the
same row as the embedding in the vector store — cleaning improves vector
match quality, augmenting enables search beyond pure semantic similarity
(filtering, keyword/exact match, citation).

### Cleaning

Goal: eliminate differences that aren't semantically material, so
closeness in vector space tracks closeness in meaning.

- **Lowercase** — embeddings are case-sensitive ("Cheetah" ≠ "cheetah" as
  vectors); decide whether to lowercase everything or just sentence-initial
  words.
- **Guard against prompt injection** — if attackers know a repo feeds your
  index, they can plant instructions in content for your LLM/agents to
  later execute. Never treat ingested content as instructions during any
  processing step; flag/exclude media with embedded instructions, and
  consider a constrained-decoding LLM pass to classify/sanitize inputs.
- **Remove stop words** ("a", "an", "the") — shrinks vector dimensionality,
  but some stop words carry real semantic weight (e.g. "not") — test the
  effect before removing.
- **Fix spelling mistakes** — a misspelled word embeds differently from the
  correct one ("cheatah" ≠ "cheetah").
- **Remove Unicode noise** — cuts dimensionality; test first since some
  Unicode is semantically relevant.
- **Normalize text** — expand abbreviations and contractions ("I'm" → "I
  am"), convert numbers to words.
- **Normalize localization** — localize per-document and reprocess each
  language separately rather than storing unvalidated translations; confirm
  the embedding model actually supports multilingual input.
- Store the cleaned/vectorized text in its own field and keep the
  **original chunk** in another — clean for matching, return/cite the
  original.

### Augmenting with metadata

Which fields to add depends on the problem domain and query types you need
to support (pure semantic search isn't enough for exact-match or
filtered queries). Common fields:

| Field                          | Purpose                                                                                                                             | Typical tool                            |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| ID                             | Uniquely identify a chunk; dedupe during (re)processing                                                                             | Hashing library                         |
| Title                          | Quick summary; also useful as an indexed-search field                                                                               | LLM                                     |
| Summary                        | Longer than title; common return + indexed-search value                                                                             | LLM                                     |
| Rephrasing                     | Captures synonyms/paraphrasing to widen vector-search recall                                                                        | LLM                                     |
| Keywords                       | Exact-term/noncontextual matches (e.g. product+year codes)                                                                          | LLM, RAKE, KeyBERT, multi-rake          |
| Tags                           | Classifiers (e.g. MIME type) for hybrid search + filtering                                                                          | LLM                                     |
| Entities                       | People/orgs/locations for exact-match search                                                                                        | spaCy, Stanford NER, scikit-learn, NLTK |
| Cleaned chunk text             | The cleaned version described above                                                                                                 | LLM                                     |
| Questions the chunk can answer | Precomputed Q&A closes the gap when a short query embeds far from a long chunk — search query-vs-question instead of query-vs-chunk | LLM                                     |
| Source                         | Lets the querier cite provenance                                                                                                    | —                                       |
| Language                       | Filter field                                                                                                                        | —                                       |

**Multimodal enrichment**: generate descriptive text per artifact
(image/video/audio) plus localized translations, and consider generating
multiple representations per artifact (e.g. caption + transcript) rather
than one.

**Cost**: LLM-based enrichment (captioning, summarizing, rephrasing) is
priced per chunk and multiplies by corpus size — cost out each enrichment
field × chunk volume before committing, same as the [chunking
economics](#chunking-economics) argument for images/tables above.

## 6. Embeddings

- **What an embedding is**: a dense vector (e.g. 768/1536 dims) that
  captures an object's semantic meaning, positioned so semantically similar
  objects land close together and relationships become arithmetic —
  `embedding(king) − embedding(man) + embedding(woman) ≈ embedding(queen)`.
  In RAG, chunks and the user query are embedded with the **same model**
  so their vectors are comparable.
- **Vocabulary is the hidden constraint**: every embedding model trains on
  a fixed vocabulary (BERT's is ~30k words). A word outside it gets split
  into subwords the model does know — e.g. "histamine" → "his" + "ta" +
  "mine" — and the aggregated subword vector is a much weaker semantic
  match than the real word would have been. Check your corpus's vocabulary
  overlap with a candidate model before committing to it.
- **Choosing a model**:
  - Decide if your content is domain-specific first — a rough test: could
    a general web search find the same entities/keywords? If yes, it's
    general content; start from the [MTEB / Hugging Face leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
    and test top-ranked general models against your own data.
  - If domain-specific, look for a domain model first (e.g. BioGPT for
    biomedical text). If none exists, or it underperforms on your data,
    fine-tune a general model on your domain vocabulary instead.
  - Always confirm license terms and language support before adopting any
    model — vocabulary/language mismatch silently degrades every
    downstream retrieval.
- **Fine-tuning**: adjusts model weights toward your vocabulary/semantics
  and can meaningfully improve retrieval accuracy for specialized domains
  (legal, code search), but needs careful evaluation — poor training data
  can just as easily degrade quality. Try prompt engineering or constrained
  decoding first; fine-tune only once retrieval evaluation shows a real
  gap a general/domain model can't close.
- **Multimodal embeddings**: the load → embed → store pattern extends to
  images/audio/video (e.g. CLIP for images), but model choice and
  preprocessing vary by modality. Prefer converting non-text media to a
  structured text representation first — e.g. Azure Content Understanding
  turns docs/images/video/audio into Markdown + JSON with scene
  descriptions, inline transcripts, and speaker diarization — and embed
  that with a standard text embedding model, rather than feeding raw media
  straight into an embedding model. Define a schema for the specific
  features you want extracted (object presence, narrative summary, etc.)
  so the resulting embeddings are optimized for your actual retrieval
  goals, not generic media understanding.
- **Dimensionality reduction**: high-dimensional vectors cost more to
  store and compare. Post-processing techniques like PCA or t-SNE can
  shrink dimensions, cutting cost and sometimes improving semantic clarity
  by discarding noisy/unused features — apply this after embedding
  generation, not as a substitute for choosing a smaller model.
- **Distance/comparison metrics**: cosine similarity (angle between
  vectors, scale-invariant, most common for semantic closeness), dot
  product (fast, requires normalized vectors), Euclidean/L2 (straight-line
  distance, literal proximity), Manhattan distance (sum of absolute
  differences). Pick based on what "similar" should mean for your data —
  these same metrics are what the retrieval index (section 7) uses under
  the hood.
- **Evaluating embedding models**: visualize chunk/question vectors (e.g.
  via t-SNE) to sanity-check that relevant chunks cluster near real
  questions, and measure retrieval performance directly — embed real
  content, run a vector search, check whether the right items come back.
  This is more trustworthy than public benchmark leaderboards, which are
  often academic datasets that don't reflect your business data or query
  patterns.
- **Embedding economics**: bigger models generally score better on
  benchmarks but cost more — larger vectors mean more storage and slower
  comparison at query time. Validate through experimentation rather than
  assuming a bigger/higher-ranked model is worth it; a good-enough smaller
  model is often the right trade for production cost/latency budgets.

## 7. Retrieval

### Vector search & indexing

- **Exact vs approximate nearest neighbor (ANN)**: exact search (e.g.
  exhaustive/brute-force KNN) is O(n) per query — too slow at scale. ANN
  indexes trade a small accuracy loss for huge speed gains.
  - **HNSW** (Hierarchical Navigable Small World): graph-based, very fast
    query, good recall, higher memory footprint. Default choice for most
    managed vector DBs (Vertex AI Vector Search, pgvector, Pinecone, Azure
    AI Search).
  - **IVF** (Inverted File Index): clusters vectors, searches nearest
    clusters only. Lower memory, needs a training/clustering step, tunable
    recall/speed via `nprobe`.
- **Vector DB options**: Vertex AI Vector Search (managed, GCP-native),
  pgvector (Postgres extension, good if already on Cloud SQL/AlloyDB),
  Pinecone/Weaviate/Elastic/Azure AI Search (third-party/cloud managed).
- **HNSW tuning knobs** (naming follows Azure AI Search, but the concepts
  generalize to any HNSW-based index):
  - `efConstruction` — how many nearest neighbors get connected to a
    vector at index-build time. Higher = better-quality index but more
    build time/storage/compute; scale it up as chunk volume grows, down
    for small corpora.
  - `efSearch` — how many nearest neighbors the query considers at search
    time; the main query-time accuracy/latency knob.
  - `m` — bidirectional link count (~4-10 typical range); lower values
    return less noise in results.
  - Treat all three as things to tune experimentally against your own
    test content/queries (section 3), not fixed defaults.
- **Similarity metric** should match what the embedding model expects:
  cosine (angle, scale-invariant — default for most embedding APIs incl.
  Azure OpenAI), dot product (fast, requires normalized vectors), or
  Euclidean/L2 (straight-line distance). Same metrics as section 6's
  distance discussion — this is where they're actually configured.

### Search types

- **Vector search**: compares the embedded query against vector field(s).
  Run the **same cleaning/preprocessing** on the query at retrieval time
  that you ran on chunks at ingestion (section 5) — e.g. if chunks were
  lowercased, lowercase the query too — and embed with the same model
  used for the chunks. Querying multiple vector fields in one call
  (content vector + generated-questions vector, etc.) is itself a form of
  hybrid search on some platforms.
- **Full-text/keyword search**: matches plain text via BM25/Lucene-style
  ranking (any-match or all-match) — excellent for exact term matches
  (IDs, part numbers, phrases) that embeddings blur. Run it against the
  keyword/entity metadata fields from section 5, plus title/summary/chunk
  text, especially where content is semantically similar but differs by a
  specific keyword, entity, or code.
- **Hybrid search**: platform runs vector + full-text queries in
  parallel, combines via **Reciprocal Rank Fusion** (RRF, see Reranking
  below) or a weighted sum, returns the merged top-N. Per-vector-field
  weights (default 1.0) let you bias, e.g., a content vector over a
  generated-questions vector.
- **Manual multiple queries**: run separate queries yourself (vector +
  keyword, or keyword against several different metadata fields) and
  merge/rerank client-side. Reach for this when: the platform has no
  native hybrid support; you want field-specific full-text queries
  (keywords field vs. entities field); you want control over the
  reranking step; or the query needs decomposition into subqueries
  pulled from multiple sources. If the agent instead needs to decide
  _at runtime_ whether/how to decompose and iterate on intermediate
  results, that's agentic RAG (sections 9/13), not a fixed pipeline.
- **General tips**: search multiple fields per query — you rarely know
  upfront whether vector or keyword will win, or which field holds the
  match; return title/summary/source/raw-uncleaned-content so you have
  both match quality and citation data; combine keyword filtering with
  vector search (keyword narrows the candidate set, vector search finds
  the best matches within it).

### Query-time techniques (query translation)

Optional transforms applied to the raw user query before retrieval —
composable into a pipeline: augment → decompose → (per subquery: rewrite
→ search → rerank) → accumulate context → rewrite/search/rerank the
original query against that accumulated context.

- **Query augmentation**: LLM adds context/specificity to a vague query
  _without_ changing its intent or discarding the original — e.g.
  "Compare the earnings of Microsoft" → "...in the current year vs. last
  year by quarter." Only augment when the model actually has grounding
  for what it adds (its own knowledge, or context you supply) — don't let
  it invent specifics it can't support.
- **Decomposition**: LLM first classifies the query as simple (single
  fact, answerable from one passage) vs. complex (multi-part, needs
  synthesis across sources) — e.g. "How do electric cars work, and how do
  they compare to ICE vehicles?" splits into two independently-answerable
  subqueries. Run each subquery as its own retrieval, aggregate top
  results as accumulated context for the final generation call. This is a
  **fixed flow decided before any search runs**; if the agent needs to
  reason about intermediate results to decide decomposition/next steps at
  runtime, that's agentic RAG instead.
- **Rewriting**: LLM rewrites the query to fix vagueness, missing
  keywords, unnecessary words, or unclear semantics — optimizing for
  keyword search and semantic-similarity search simultaneously (synonyms
  - specific terms + natural phrasing in one rewritten query).
- **HyDE (Hypothetical Document Embeddings)**: ask the LLM to write a
  hypothetical answer, embed _that_, and search with it — the
  hypothetical answer's embedding often matches real docs better than the
  raw question's (answer-to-answer similarity instead of
  question-to-answer).
- **Multi-query retrieval**: generate several reformulated queries,
  retrieve for each, merge/dedupe results — improves recall for ambiguous
  questions.
- **Query routing**: classify the query first (e.g. "this needs SQL
  lookup" vs "this needs doc search") and route to the right retriever —
  this is where RAG starts to blend into agentic tool-use (see file 02).
- **Passing images directly at query time**: for multimodal models
  (GPT-4V/4o-class), an alternative to chunking images at ingestion is
  passing the raw image straight into the prompt — weigh this against the
  captioning-at-ingestion approach (section 6) on cost/latency/quality.
  Alternatively, pre-generate structured figure descriptions (e.g. chart/
  diagram descriptions in a structured syntax) during ingestion so
  figures become searchable via ordinary text/vector queries without
  passing raw images at inference at all.

### Filtering & field weighting

- **Filtering**: restrict to filterable fields (keywords, entities,
  ACL/permission tags, date) to shrink the candidate set before/alongside
  similarity search — improves relevance and performance, and is where
  access-control enforcement actually happens at query time (file 04).
  Test whether it helps specifically on queries with missing/inaccurate
  keywords, abbreviations, or acronyms.
- **Field weighting**: bias ranking toward specific fields by query type/
  use case — e.g. weight entity/keyword fields higher for a
  keyword-centric query like "Where is Microsoft headquartered?". Only
  keep weighting profiles you actually use in production; unused profiles
  are pure tuning-surface debt.

### Reranking

Retrieval optimizes for **recall** (cast a wide net); reranking optimizes
for **precision** (reorder so the truly relevant chunks surface first).
Without it you're stuck with raw vector-similarity or keyword-frequency
scores, neither of which directly evaluates "does this specific chunk
answer this specific query."

Rerank when: you combined multiple searches (hybrid/manual-multi) and
need one unified order across score distributions that aren't otherwise
comparable; you deliberately over-retrieved (e.g. top 50 instead of top 10) to protect recall and now need to cut back down; your index spans
varied doc types/lengths where raw scores aren't directly comparable; or
answer quality matters more than the extra latency reranking adds — every
method below (cross-encoder, LLM, semantic ranking) adds a real,
non-trivial processing step after initial retrieval, so factor that into
latency-sensitive designs.

| Approach                                         | How                                                                                                                                        | Tradeoff                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Cross-encoder                                    | Jointly encodes (query, chunk) pairs and scores relevance                                                                                  | Higher accuracy than bi-encoder vector search; too slow to run over a full corpus — only run on an already-narrowed candidate set. Smaller models (`ms-marco-MiniLM-L6-v2`) = faster/less accurate; larger (`-L12-v2`) = slower/more accurate. Scores are relative (for ordering), not absolute — don't threshold without empirical calibration. |
| LLM reranking                                    | Prompt an LLM to score/order candidates                                                                                                    | Most flexible (custom relevance criteria, reasoning about _why_ something's relevant); most expensive per call — reserve for cases where cross-encoders underperform. Batch requests, cap chunk length to a token budget, and validate/parse returned scores programmatically.                                                                   |
| Reciprocal Rank Fusion (RRF)                     | Score-free: merges ranked lists using each item's _rank position_, not its raw score — `RRF(d) = Σ 1/(c + rank(d))` across lists, `c ≈ 60` | Cheap, negligible latency; the right tool specifically when merging lists with incompatible score distributions (e.g. BM25 vs. cosine similarity). Good first-stage merge before a heavier reranker. Azure AI Search applies it automatically on hybrid queries; implement it yourself for manual multi-query.                                   |
| Semantic ranking (managed, e.g. Azure AI Search) | Deep-learning reranker rescoring the top ~50 BM25/hybrid results using summarized field content                                            | Managed/no-infra to run; also yields semantic captions/highlights and direct "semantic answer" extraction as side benefits.                                                                                                                                                                                                                      |
| Non-Microsoft rerank APIs (e.g. Cohere Rerank)   | Hosted cross-encoder-style rerank service                                                                                                  | No model hosting/ops burden; evaluate domain relevance, pricing, latency, and whether sending chunk content to a third party clears your security/compliance bar.                                                                                                                                                                                |

**Pipeline pattern**: retrieve broadly (e.g. top 50) → merge multi-search
results via RRF → rerank the merged set with a model-based reranker
(cross-encoder / semantic ranking / LLM) → truncate to the final top-N
(e.g. 5-10) that actually goes in the prompt. Tune candidate-set size
(20-50 is a typical starting range), reranker model choice, and final N
against your eval metrics (section 10) — more chunks lowers the chance of
missing relevant info but raises token cost/noise; fewer chunks is
cheaper/cleaner but risks dropping something relevant.

## 8. Grounding & citations

- Instruct the model to answer **only** from provided context, and to say
  "I don't know" if the context doesn't contain the answer — reduces but
  doesn't eliminate hallucination.
- Have the model emit citations (chunk IDs / source links) alongside claims
  — lets you verify and lets the UI show provenance.
- **Faithfulness/groundedness check**: a secondary pass (often another LLM
  call, or NLI-style entailment model) verifies the generated answer is
  actually supported by the retrieved context — catches hallucination
  before it reaches the user.

## 9. Advanced RAG patterns

- **Self-refelctive RAG / corrective RAG**: model critiques its own retrieval —
  "were these chunks actually relevant?" — and re-retrieves or falls back
  if not.
- **Agentic RAG**:
  Standard RAG works well for queries that map to a single search against a single index. But some scenarios, such as multistep reasoning, dynamic source selection, query decomposition at runtime, and combining retrieval with actions, exceed what a fixed pipeline can handle. In these cases, consider agentic RAG. In agentic RAG, an AI agent treats retrieval as a tool that it can invoke on demand.
  retrieval becomes a _tool_ the agent calls, possibly
  multiple times, interleaved with reasoning (vs. a fixed one-shot
  retrieve-then-generate pipeline). Handles multi-hop questions
  ("compare X's Q1 and Q3 revenue" needs two retrievals).
- **GraphRAG**: build a knowledge graph from documents (entities +
  relationships), retrieve via graph traversal in addition to/instead of
  vector similarity — better for questions requiring relational reasoning
  across many docs ("summarize everything connected to project X").

## 10. Evaluating RAG quality

By this point you should already trust chunking, embedding, and retrieval
individually (sections 3-7) — this phase evaluates the **final call to the
LLM**, i.e. does it produce a good response given the grounding context it
was handed. LLM responses are non-deterministic — the same prompt can
return different results — so evaluate against a **target range**, not a
single expected score.

- **Retrieval metrics**: precision@k, recall@k, MRR (mean reciprocal rank)
  — did we retrieve the right chunks at all?
- **Generation metrics** (often via LLM-as-judge or RAGAS-style
  frameworks) — see breakdown below.
- See file 03 for the full evaluation/observability picture.

### Generation metrics (LLM-as-judge)

| Metric                          | What it measures                                                                 | How to calculate                                                                                                                                                  | If low                                                                                                                                                             |
| ------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Groundedness** (faithfulness) | Is the response based _entirely_ on the provided context, with nothing invented? | NLI-style entailment model (e.g. Azure AI Content Safety groundedness), LLM-based judge, Ragas `faithfulness`, MLflow faithfulness                                | Model isn't treating the chunks as relevant — revisit retrieval, chunking, or the grounding prompt.                                                                |
| **Completeness**                | Does the response answer _all_ parts of the query?                               | LLM rephrases the query to extract intent(s), checks each intent against the retrieved docs (yes/no), takes the ratio of "yes" answers, squares it to punish gaps | Check embedding-model vocabulary fit, consider a larger chunk size (fixed-size chunking), confirm test content actually contains a full answer.                    |
| **Utilization**                 | How much of the _response_ is actually built from the retrieved chunks?          | LLM judge counts how many of the passed-in chunks show up in the response                                                                                         | Evaluate jointly with completeness (matrix below).                                                                                                                 |
| **Relevance**                   | Is the response pertinent to the query at all?                                   | LLM judge, Ragas `answer_relevancy`, MLflow relevance                                                                                                             | Check whether relevant chunks exist but weren't retrieved (embedding/chunking issue) vs. were retrieved but the prompt didn't use them (prompt issue).             |
| **Correctness**                 | Is the response factually accurate?                                              | LLM judge (ideally a _different_ model than the generator) scoring factuality; optionally cross-check against an external trusted source                          | Check source docs for factual errors/bias first, then the prompt, then whether the base model has an inherent inaccuracy that needs more grounding or fine-tuning. |

**Utilization × completeness** — evaluate together, since each explains
a different failure the other metric alone would miss:

| —                     | High utilization                                                                                                                                                           | Low utilization                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **High completeness** | No action needed.                                                                                                                                                          | Answer is fine but pulled in irrelevant chunks too — lower top-k.                                                      |
| **Low completeness**  | Model used what it was given, but wasn't given enough — enlarge chunks, raise top-k, check whether a chunk that would've completed the answer exists but wasn't retrieved. | Answer is both incomplete _and_ barely using what it has — enlarge chunks (esp. fixed-size), and fine-tune the prompt. |

**Other useful combinations**:

- **Groundedness + correctness**: high groundedness + low correctness means
  the model is using the right context but drawing the wrong conclusion from
  it (e.g. conflating two facts that were merely adjacent in the context) —
  a genuinely different failure than not using context at all. Which metric
  to prioritize is workload-dependent — e.g. if source data intentionally
  contains claims you want repeated verbatim, prioritize groundedness over
  correctness.
- **Groundedness + utilization + similarity**: both high but similarity low
  means the model is grounded and using the right chunks, just paraphrasing
  badly — a prompt-tuning problem, not a retrieval problem.

Agentic RAG (section 9) adds more evaluation dimensions on top of this: tool
selection accuracy, retrieval efficiency (tool calls per request), and
end-to-end latency across reasoning steps.

### Responsible AI, content safety, and security evaluation

Evaluation must extend past groundedness/completeness/etc. into whether
retrieved and generated content is safe, private, and non-infringing —
retrieval can surface or amplify unsafe content that was merely sitting in
the corpus, not just content the model invented.

- **Content safety**: scan retrieved _and_ generated content for hate/bias,
  violent content, self-harm references, sexual content — e.g. via Azure AI
  Content Safety — and feed those scores into the evaluation pipeline
  itself, not just a separate compliance check.
- **IP protection**: detect and exclude copyrighted textual (lyrics,
  articles, proprietary docs) or visual (logos, artwork, characters)
  material from both the retrieval source and the generated response.
- **Security / adversarial**: retrieved documents are an injection surface
  — a poisoned doc can leak data, manipulate the response, or bypass safety
  controls (this is the query-time counterpart to the ingestion-time
  prompt-injection guard in section 5). Evaluate via adversarial testing,
  document sanitization, and monitoring for anomalous retrieval patterns.
- **Privacy**: source repos may contain direct identifiers, contact info,
  financial/biometric/health data, employment data, or credentials — run
  automated PII/PHI detection and enforce the same access-control filtering
  at retrieval time described in file 04.
- **Key considerations**: curated/vetted sources reduce risk more than any
  downstream filter; a weak retrieval strategy can surface unsafe content
  _more_ often than random chance would; document corruption (an attacker
  planting content in the corpus) is a threat class distinct from model
  hallucination; continuous auditing of the document repository and
  retrieval patterns is required, not a one-time review.

## 11. Failure modes & mitigations

| Failure                               | Cause                                       | Mitigation                                                                         |
| ------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------- |
| Retrieval miss                        | Query/doc vocabulary mismatch, bad chunking | Hybrid search, query rewriting, better chunking                                    |
| Stale answers                         | Index not updated after source changes      | Incremental re-indexing, CDC pipelines, freshness metadata + filtering             |
| Lost context at chunk boundary        | Fixed-size chunking cuts mid-idea           | Overlap, semantic/structure-aware chunking, parent-child retrieval                 |
| Hallucination despite retrieval       | Model ignores context or fills gaps         | Strict grounding prompts, faithfulness check, "I don't know" fallback              |
| Irrelevant chunks crowd out good ones | Weak similarity search, no re-ranking       | Cross-encoder re-ranking, better embedding model                                   |
| Unauthorized data exposure            | No access control at retrieval              | ACL/permission metadata filtering at query time (see file 04)                      |
| Context window overflow               | Too many/too-large chunks stuffed in prompt | Re-ranking to cut top-k, summarization of retrieved chunks, hierarchical retrieval |

## 12. Data freshness: batch vs streaming ingestion

- **Batch**: nightly/hourly re-index jobs (Dataflow/Airflow) — simple,
  fine for docs that change infrequently.
- **Streaming/CDC**: change-data-capture from source systems (e.g.
  Pub/Sub triggered on doc update) → incremental embed + upsert into
  vector index — needed when freshness SLA is tight (e.g. inventory,
  ticket status).
- Always version/tag chunks with a timestamp so stale entries can be
  filtered or superseded, not just appended forever.

## 13. End to End RAG on GCP

https://docs.cloud.google.com/architecture/rag-genai-gemini-enterprise-vertexai
https://cloud.google.com/use-cases/retrieval-augmented-generation

## 14. Resources

- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-preparation-phase
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-generate-embeddings
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-agentic
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-llm-evaluation-phase

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

---

## Further Research

- how to improve latency
- how to address haluciation
- how to enfroce acces at doc level
- prevent context window overlfow
- explainabiltiy
