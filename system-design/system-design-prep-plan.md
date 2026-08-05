# Google GenAI FDE — System Design Interview Prep Plan

Prep plan tailored to the Forward Deployed Engineer (GenAI), Google Cloud role
(see `../job-description.md`). This role's system design interviews skew
toward **applied AI systems architecture**: agentic pipelines, RAG, data
integration, evaluation/observability, and production hardening on GCP —
not generic distributed-systems trivia (though that foundation still matters).

Target timeline: 3-4 weeks, ~1-1.5 hrs/weekday + longer weekend session.

---

## 1. What this interview actually tests

FDE system design ≠ classic "design Twitter." Expect prompts framed as a
**customer engagement**: "A retail customer wants an AI agent that answers
questions over their product catalog and order history — design it." Signals
they're grading:

- Can you translate a vague business ask into a scoped technical architecture?
- Do you reach for the right AI-specific building blocks (RAG, agents, tool
  use, evals) instead of just generic web-app patterns?
- Do you handle the "boring but critical" production concerns: auth, data
  freshness, latency/cost, safety, observability, failure modes?
- Can you talk tradeoffs out loud and adapt when the interviewer moves the
  goalposts ("now it needs to handle 10x traffic" / "now it must cite
  sources" / "the data is in an on-prem SQL Server")?

---

## 2. Foundational system design (week 1)

Even applied-AI interviews probe baseline distributed systems fluency.
Refresh, don't relearn from scratch:

- [ ] Load balancing, horizontal scaling, caching layers (CDN, Redis)
- [ ] SQL vs NoSQL vs vector DB — when each fits
- [ ] Async processing: message queues (Pub/Sub, Kafka), event-driven design
- [ ] API design: REST vs gRPC, idempotency, rate limiting, backpressure
- [ ] Consistency models, CAP theorem — just enough to reason about tradeoffs
- [ ] Back-of-envelope estimation: QPS, storage, latency budgets

Resources: *Designing Data-Intensive Applications* (skim relevant chapters),
"Grokking the System Design Interview," ByteByteGo YouTube/newsletter.

Practice: pick 2 classic prompts (design a URL shortener, design a rate
limiter) just to warm up the estimation/tradeoff muscle — don't over-invest
here, it's not the core of this interview.

---

## 3. Core GenAI architecture building blocks (week 1-2)

This is the heart of the prep. For each, know the "why," the alternatives,
and the failure modes.

### 3.1 RAG (Retrieval-Augmented Generation)
- [ ] Chunking strategies (fixed-size, semantic, hierarchical) and tradeoffs
- [ ] Embedding models, vector DBs (Vertex AI Vector Search, pgvector,
      Pinecone, Elastic) — indexing (HNSW/IVF), ANN tradeoffs
- [ ] Hybrid search (keyword + vector), re-ranking
- [ ] Structured + unstructured data pipelines feeding a single retrieval
      layer (mentioned explicitly in the JD)
- [ ] Freshness: batch vs streaming ingestion, incremental re-indexing
- [ ] Grounding, citation, hallucination mitigation
- [ ] Failure modes: retrieval miss, stale index, chunk fragmentation losing
      context, embedding drift

### 3.2 Agentic systems / multi-agent orchestration
- [ ] Single-agent tool-use (ReAct) vs multi-agent (hierarchical delegation,
      supervisor/worker, debate)
- [ ] Frameworks named in JD: LangGraph, CrewAI, Google ADK — know the
      mental model of at least LangGraph (graph/state machine) and ADK
- [ ] MCP (Model Context Protocol) servers as the "connective tissue" to
      customer APIs/data — be able to sketch how an MCP server exposes a
      legacy system's capability as a tool
- [ ] State management across multi-turn / multi-agent workflows (session
      state, memory, checkpointing)
- [ ] When to use a single well-prompted agent vs decomposing into multiple
      agents (cost/latency/complexity tradeoff — don't over-architect)
- [ ] Self-reflection / critique loops, planning vs reactive execution

### 3.3 Evaluation & observability
- [ ] Offline eval pipelines: golden datasets, LLM-as-judge, human-in-loop
- [ ] Online monitoring: tracing agent steps, tool calls, token usage
- [ ] Metrics: accuracy/groundedness, latency, cost-per-request, tokens/sec
      (explicitly called out in JD as "LLM-native metrics")
- [ ] Regression testing for prompt/model changes
- [ ] Guardrails: safety filters, PII redaction, prompt-injection defenses

### 3.4 Integration & data readiness
- [ ] Connecting to legacy/enterprise systems: APIs, ETL, data silos
- [ ] Auth/security perimeters (OAuth, service accounts, VPC-SC, IAM)
- [ ] Handling structured (SQL/warehouses) + unstructured (docs, PDFs,
      tickets) sources in one architecture
- [ ] Data governance: PII handling, access control at retrieval time
      (row/doc-level security in RAG)

### 3.5 GCP / Vertex AI specifics
- [ ] Vertex AI platform: Model Garden, Agent Builder/ADK, Vector Search,
      Grounding, Evaluation service
- [ ] Gemini model family: context windows, multimodality, function calling
- [ ] Deployment: Cloud Run vs GKE vs Vertex endpoints for agent backends
- [ ] Pub/Sub, Dataflow, BigQuery for data pipelines feeding RAG
- [ ] Cost/latency levers: model selection (Flash vs Pro), caching,
      batching, streaming responses

### 3.6 LLM fundamentals: training, serving, fine-tuning
- [ ] Training pipeline: pretraining → SFT → alignment (RLHF/RLAIF/DPO)
- [ ] Serving/inference: decoding (temperature/top-p), KV cache, batching,
      quantization, prefill vs decode latency
- [ ] Structured troubleshooting: isolate retrieval vs generation vs
      serving-layer faults
- [ ] Fine-tuning: prompt → RAG → fine-tune decision framework, LoRA/
      QLoRA/PEFT, data requirements, risks (forgetting, staleness)
- [ ] Articulate your role in a client's "digital transformation" —
      crawl/walk/run narrative from prototype to production

Resources: Google Cloud Vertex AI docs, ADK docs, LangGraph docs, Google's
"Agents" whitepaper (Kaggle 5-day GenAI course), MCP spec (modelcontextprotocol.io).

**Deep-dive study guides for all of 3.1-3.6 live in
[`study-materials/`](./study-materials/README.md)** — read those for the
actual concepts, definitions, diagrams, and self-check questions.

---

## 4. Applied design practice (week 2-3)

Practice full end-to-end designs, out loud, timeboxed to ~35-45 min each.
Use the framework in section 5.

Prompt bank (write these up):
1. Customer support agent over a knowledge base + live ticketing system
   (structured + unstructured data, needs citations)
2. Multi-agent system to triage and resolve internal IT tickets, with
   escalation to a human
3. Enterprise search/RAG over a mix of Confluence, PDFs, and a SQL data
   warehouse, with row-level access control
4. Agent that reads a legacy SOAP/REST API and exposes it via an MCP server
   to a Gemini-based orchestrator
5. Evaluation + observability pipeline for a production agent handling
   10K requests/day, need to detect regressions before rollout
6. Design for scaling an agent from prototype (single customer, 100
   req/day) to production (50 customers, 100K req/day) — what breaks first
7. Real-time agent with a strict latency SLA (e.g., <2s) doing retrieval +
   generation — where do you cut corners safely?
8. Design a system to convert repeatable field patterns into a reusable
   internal module (meta: reflects the JD's "convert friction into product
   feedback" responsibility)

For each: write a 1-page architecture doc (diagram + component list +
key tradeoffs + failure modes) — mirrors how FDEs actually document
customer solutions.

---

## 5. Interview framework (memorize the shape, not a script)

**Note**: the timing below is a generic default for an unscoped "design
X" prompt. The actual FDE interview has a stated, different split —
**15 min discovery/stakeholder alignment + 30 min deep-dive**, with a
forced choice between two named scenarios up front. See
[`study-materials/08-interview-structure-and-discovery.md`](./study-materials/08-interview-structure-and-discovery.md)
for the calibrated timing, scenario-choice guidance, stakeholder-alignment
technique, and discovery question banks — use that file's timing script
for practice reps, not the one below.

1. **Clarify scope** (3-5 min): who's the customer, what's the business
   outcome, scale (users/QPS), latency/cost constraints, data sources,
   compliance/security constraints, existing infra.
2. **High-level architecture** (5-10 min): draw boxes — ingestion, retrieval/
   knowledge layer, orchestration/agent layer, tool/integration layer,
   serving, eval/observability. Narrate as you draw.
3. **Deep dive** (15-20 min): interviewer will pick 1-2 components to go
   deep — usually RAG pipeline design, agent orchestration, or the
   integration layer. Be ready to write pseudo-schemas, sequence flows.
4. **Production concerns** (5-10 min): failure modes, monitoring, rollout
   strategy (canary/shadow), cost controls, security review.
5. **Tradeoffs & alternatives** (throughout): always state 2 options and
   why you picked one — this is the "founder's mindset" signal they want.

---

## 6. Behavioral overlap to prep alongside (FDE-specific)

System design answers should be laced with "customer-facing engineer" signal:
- [ ] Story: led a technical discovery session, scoped ambiguous requirements
- [ ] Story: took a prototype to production, what broke, how you hardened it
- [ ] Story: identified a repeatable pattern and turned it into a reusable
      tool/module (maps directly to JD responsibility)
- [ ] Story: pushed back on a customer ask or influenced product roadmap
      based on field feedback

---

## 7. Weekly checklist

- [ ] Week 1: Foundational refresh + read Vertex AI/ADK/LangGraph/MCP docs
- [ ] Week 2: Deep-dive each building block (3.1-3.5), start prompt bank
      (prompts 1-4)
- [ ] Week 3: Finish prompt bank (5-8), do 2 mock interviews (peer or
      self-recorded), refine framework timing
- [ ] Week 4 (buffer): weak-area review, behavioral story polish, rest

---

## 8. Quick reference — things to be able to draw from memory

- RAG pipeline: source → chunk → embed → index → query → retrieve → rerank
  → augment prompt → generate → cite
- Agent loop (ReAct): observe → think → act (tool call) → observe → ...
  → final answer
- Multi-agent supervisor pattern: orchestrator agent routes to specialist
  sub-agents, aggregates results
- MCP architecture: MCP client (agent host) ↔ MCP server (exposes tools/
  resources) ↔ underlying system (API/DB/file system)
- Eval loop: golden set → run pipeline → score (automated + human) → track
  regression → gate deploy
