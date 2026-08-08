# GCP / Vertex AI Specifics

Know this layer well enough to place every other building block (RAG,
agents, evals) onto concrete GCP services — interviewers will expect
GCP-native answers given the role.

## 1. Vertex AI platform map

| Need | Vertex AI / GCP service |
|---|---|
| Foundation models | Model Garden (Gemini family + third-party/open models) |
| Agent orchestration | Vertex AI Agent Builder, Google ADK |
| Managed RAG pipeline | **RAG Engine** — managed corpus management, chunking/embedding, and retrieval API; the default answer for "how do you build RAG on GCP" unless you need the lower-level control below |
| Vector search / RAG index (low-level) | Vertex AI Vector Search (managed ANN, HNSW-based) — reach for this when RAG Engine's managed pipeline doesn't give you enough control over chunking/embedding/retrieval logic |
| Managed search + grounding | Vertex AI Search (turnkey RAG-like search over docs) |
| Grounding with live web data | Grounding with Google Search |
| Long-term agent memory | **Memory Bank** (Vertex AI Agent Engine) — cross-session memory (semantic/episodic/procedural), addressed by namespace, retrieved like RAG (see file 02 §10) |
| Short-term memory / session state | **Memorystore for Redis** (low-latency in-memory cache for hot session state), **Firestore** (durable document-store state, easy per-user/session partitioning), or **Gemini Enterprise Agent Platform Sessions** (managed session state when already building on that platform) — pick based on latency needs, durability needs, and whether you're already inside the managed platform |
| Eval | Vertex AI Evaluation Service (offline eval, LLM-as-judge tooling) |
| Structured data | BigQuery (warehouse), Cloud SQL/AlloyDB (+ pgvector) |
| Data pipelines | Pub/Sub (streaming events), Dataflow (batch/stream ETL) |
| Compute for custom serving | Cloud Run (serverless containers), GKE (Kubernetes), Vertex AI Endpoints (managed model serving) |
| Secrets/identity | Secret Manager, IAM, VPC Service Controls |
| Observability | Cloud Logging/Monitoring/Trace, Vertex AI monitoring |

## 2. Gemini model family — know the tradeoffs

- **Flash vs Pro tier**: Flash = lower latency, lower cost, smaller
  effective capability ceiling — good default for high-volume,
  latency-sensitive, or simpler tasks (routing, classification, simple
  tool calls). Pro = higher capability for complex reasoning, at higher
  cost/latency — reserve for the steps that actually need it.
- **Context window**: Gemini models support very large context windows
  (millions of tokens in top-tier models) — enables long-document
  reasoning without RAG in some cases, but large context ≠ free: cost and
  latency still scale with tokens actually sent, and "needle in haystack"
  recall degrades with excessive irrelevant context. RAG usually still
  wins for precision + cost even when a huge context window is available.
- **Multimodality**: native image/video/audio input — relevant for
  document-heavy enterprise use cases (scanned forms, diagrams,
  screenshots) without a separate OCR pipeline in some cases.
- **Function calling**: native structured tool-calling support — the
  mechanism underlying agent tool use (file 02).
- **Model routing/mixing**: production systems often use Flash for
  cheap/high-volume steps (routing, simple extraction) and Pro for the
  few steps needing deep reasoning — a cost lever, not just a capability
  choice.

## 3. Vertex AI Agent Builder & ADK

- **Agent Builder**: higher-level, more managed path to stand up
  search/agent experiences quickly (good for fast customer POCs).
- **ADK (Agent Development Kit)**: code-first framework for building
  custom multi-agent systems that deploy on Vertex AI — gives the control
  LangGraph/CrewAI give, but natively integrated with Vertex's model
  serving, tool ecosystem, and evaluation tooling. This is the JD's
  preferred framework for a reason: it's the path that keeps you inside
  GCP's managed ecosystem end-to-end (build → eval → deploy → monitor).
- Both support **MCP** integration as a way to plug in custom
  tools/data sources (file 02, section 7).

## 4. Vertex AI Vector Search vs Vertex AI Search

Easy to conflate — know the distinction:
- **Vector Search**: the low-level managed ANN vector index (HNSW-based).
  You control chunking, embedding model, retrieval logic yourself —
  maximum flexibility, more engineering.
- **Vertex AI Search**: a higher-level, more turnkey product — point it at
  a data source (GCS bucket, BigQuery, website) and it handles
  ingestion/chunking/embedding/retrieval/grounding largely for you. Faster
  to stand up, less control over the internals — a good default for
  simpler RAG needs or fast POCs; drop to raw Vector Search when you need
  custom chunking, hybrid search tuning, or non-standard data shapes.

## 5. Deployment: where does the agent backend run?

| Option | Fits when | Overhead |
|---|---|---|
| Vertex AI Agent Engine | Agent built with ADK; want the fastest managed path — handles scaling + integrated memory/session mgmt, single-CLI deploy, native A2A protocol support. Also the runtime **Gemini Enterprise** builds on to govern custom + pre-built agents. | Lowest |
| Cloud Run | Stateless custom agent backend, needs to scale to zero, max control over runtime (CPU/GPU) without managing a cluster — good default for most non-ADK agent APIs, exposes as web UI / REST / A2A | Low |
| GKE | Need fine-grained control over networking/scaling, many concurrent agent instances, specialized hardware, complex multi-component orchestration or sidecar requirements (e.g. custom MCP servers with special networking needs). AI-aware autoscaling via GKE Inference Gateway + custom HPAs. | High |
| Vertex AI Endpoints | Serving a custom-trained/fine-tuned model directly (not just calling Gemini API), need Vertex's built-in model monitoring/versioning | Medium |
| App Engine | Agent built on the **Conversational Agents** platform; runtime/language pinned in `app.yaml`; UI delivered via Dialogflow Messenger embedded in a webpage | Low-Medium |
| Compute Engine | Rigid OS/kernel/networking requirements, legacy workload migration, long-running stateful agent that shouldn't scale to zero | Highest |

Default answer for "where do you deploy the agent orchestration layer" in
an interview: **Cloud Run** for a custom agent, or **Vertex AI Agent
Engine** if it's built with ADK — unless a specific requirement (custom
networking, long-lived stateful connections, existing GKE investment)
pushes you elsewhere. Justify, don't just name-drop.

## 6. Security and access control

Three distinct concerns — don't conflate them in an interview answer:

| Concern | Service | What it actually prevents |
|---|---|---|
| Identity & authorization | IAM | Wrong human reaching the agent, or the agent's own service account holding excess permissions (least privilege) |
| Data perimeter | VPC Service Controls | Data exfiltration out of the perimeter around sensitive resources (data stores, vector DBs) |
| Tool permissions | Scoped credentials / service accounts | Agent's tools (file 02) reaching further than the task requires when calling external APIs |

These map to three different attack surfaces — *who talks to the agent*,
*what the agent's environment can reach*, and *what the agent's tools are
allowed to do on its behalf*. "Secure the agent" answers that only name IAM
are incomplete.

## 7. Monitoring — four signal types

1. **Logging** (Cloud Logging) — structured record of every interaction,
   tool invocation, error.
2. **Tracing** (Cloud Trace) — where latency is actually going: LLM call
   vs. tool webhook vs. memory retrieval.
3. **Metrics** (Cloud Monitoring) — infra-level QPS, error rate, latency.
4. **Agent-specific analytics** (Conversational Agents platform) —
   business-level signals (escalation rate, conversation outcomes, tool
   failure rate) that generic infra metrics don't capture.

(1)-(3) are generic to any backend service; (4) is what makes it *agent*
observability rather than just infra observability — ties into eval/
observability practices in file 03.

## 8. Lifecycle management

Use built-in versioning on Vertex AI Agent Engine or Cloud Run to snapshot
code + model + config together at stable points. An agent's "version" is
code+model+config as one unit — a model swap or prompt change can change
behavior as much as a code change, so version them together, not just the
code.

## 9. Data pipeline services

- **Pub/Sub**: event backbone — source-system change events, triggering
  incremental re-indexing, decoupling ingestion producers from consumers.
- **Dataflow**: batch or streaming ETL (Apache Beam) — chunking/embedding
  jobs at scale, scheduled re-indexing, CDC processing.
- **BigQuery**: structured data warehouse — target for text-to-SQL
  queries, and also a viable place to store/query embeddings at scale
  (BigQuery ML / vector search functions) if you want one system for both
  structured and vector data.

## 10. Cost & latency levers (be ready to enumerate these under pressure)

1. **Model tier selection** — Flash vs Pro per step, not globally.
2. **Prompt/context size** — trim retrieved context to what's needed
   (re-ranking, file 01); large context windows aren't free.
3. **Caching** — cache repeated/common queries or sub-results (e.g. a
   context cache for a system prompt reused across many requests).
4. **Batching** — batch non-latency-sensitive requests (e.g. offline
   eval runs, bulk classification) instead of one-at-a-time calls.
5. **Streaming responses** — improve perceived latency (time-to-first-
   token) even if total generation time is unchanged.
6. **Parallel tool calls** — where independent, run tool calls
   concurrently instead of sequentially to cut wall-clock latency.
7. **Right-sizing retrieval** — smaller top-k, better re-ranking, avoids
   paying to process irrelevant tokens.
8. **Autoscaling/scale-to-zero** — Cloud Run scale-to-zero for
   spiky/low-volume workloads avoids paying for idle capacity.

## 11. A "customer engagement" framing to practice

Interviewers may want you to think like an FDE, not just a generic
architect: given a customer's existing environment (say, mostly on GCP,
data in BigQuery + Confluence + a legacy ticketing SOAP API), sketch which
Vertex AI services you'd actually reach for and why, respecting whatever
constraints they mention (data residency, latency SLA, existing
investment in GKE, etc.) — the "right" answer is the one justified by
their constraints, not the maximal, most-impressive-sounding stack.

---

## Could you explain/draw this cold?

- [ ] Explain Flash vs Pro tradeoff and give an example of mixing both in
      one pipeline
- [ ] Explain the difference between Vertex AI Search and Vertex AI Vector
      Search, and when you'd pick each
- [ ] Explain RAG Engine vs. raw Vertex AI Vector Search, and when you'd
      drop down to the lower-level service
- [ ] Name the GCP service for long-term agent memory (Memory Bank) and the
      three options for short-term/session state (Memorystore for Redis,
      Firestore, Gemini Enterprise Agent Platform Sessions), and justify a
      pick among the three for a given latency/durability requirement
- [ ] Justify Cloud Run vs GKE vs Vertex Endpoints vs Agent Engine vs App
      Engine vs Compute Engine for a given scenario
- [ ] Explain why VPC Service Controls and IAM are not redundant — what
      does each stop that the other doesn't?
- [ ] Name all four monitoring signal types and give an example question
      each one answers that the others can't
- [ ] Explain why an agent "version" bundles code + model + config, and
      what breaks if you version only the code
- [ ] List 5 cost/latency levers and which one you'd reach for first for
      a customer complaining about response time vs. one complaining
      about cost
- [ ] Sketch a full GCP-native architecture for the "customer support
      agent over knowledge base + ticketing system" prompt from the prep
      plan's prompt bank, naming a specific GCP service for every box
