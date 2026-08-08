# Evaluation & Observability for Agentic/GenAI Systems

## 1. Why this matters more than in classic software

Traditional software: deterministic, unit tests give a clear pass/fail.
GenAI systems: **non-deterministic outputs**, quality is graded/fuzzy, and
a "correct" tool-call trajectory can still be graded wrong for style/tone.
You can't just assert `output == expected`. This is why the JD explicitly
calls out building "high-performance evaluation pipelines and observability
frameworks" as a core FDE responsibility — without them, you can't safely
ship changes to a production agent.

## 2. Offline evaluation

Run before shipping a change (new prompt, new model, new tool, new
retrieval config).

- **Golden dataset**: curated set of representative (input, expected
  behavior) pairs — ideally covering common cases, edge cases, and known
  past failures. Build this incrementally from real production
  interactions (with PII scrubbed) plus synthetic cases.
- **Scoring methods**:
  - _Exact/rule-based match_: works for structured outputs (did it call
    the right tool with the right args? did it return valid JSON?).
  - _LLM-as-judge_: use a strong model to score a response against a
    rubric (faithfulness, relevance, tone, correctness). Cheap and
    scalable vs. human review, but has known biases (see below).
  - _Human review_: gold standard for subjective quality, expensive —
    reserve for calibrating the LLM-judge and spot-checking.
- **Regression testing**: run the golden set on every meaningful change
  (prompt edit, model swap, retrieval tuning) and diff scores against the
  last known-good baseline before deploying — this is "CI for prompts."

### LLM-as-judge pitfalls to know

- **Position bias**: judge favors whichever answer is shown first/second.
  Mitigate: randomize order, average over both orderings.
- **Self-preference bias**: a model judges its own outputs (or same-family
  outputs) more favorably. Mitigate: use a different/stronger model as
  judge where possible.
- **Verbosity bias**: judges tend to favor longer answers regardless of
  quality. Mitigate: explicit rubric criteria that penalize unnecessary
  length.
- **Calibration**: periodically validate judge scores against human
  ratings on a sample to confirm the judge is still trustworthy.

## 3. Key metrics

| Category     | Metric                                   | Notes                                                         |
| ------------ | ---------------------------------------- | ------------------------------------------------------------- |
| Task quality | Task success rate                        | Did the agent actually accomplish the user's goal end-to-end? |
| Groundedness | Faithfulness / hallucination rate        | Is the answer supported by retrieved context / tool outputs?  |
| Relevance    | Answer relevancy                         | Does the response address what was asked?                     |
| Retrieval    | Precision@k, recall@k                    | Is RAG retrieving the right chunks (see file 01)?             |
| Latency      | p50/p95/p99 latency, time-to-first-token | Tail latency matters more than average for UX                 |
| Cost         | Cost-per-request, tokens/sec             | Explicitly named in JD as an "LLM-native metric" to track     |
| Efficiency   | Tool-call count per task, retries        | Rising tool-call count often signals prompt/tool-design drift |
| Safety       | Guardrail trigger rate, PII leak rate    | See guardrails section below                                  |

**Cost-per-request** breaks down into input tokens + output tokens (priced
differently) × model tier — track separately so you know whether a cost
regression came from longer prompts, longer outputs, or a model upgrade.

## 4. Evaluating RAG applications

RAG systems have two failure surfaces — **retrieval** (did we find the right
context?) and **generation** (did the model use that context correctly?).
Effective RAG eval scores these separately: a good final answer can hide bad
retrieval (the model got lucky or already knew the answer), and good
retrieval can be undermined by bad generation (the model ignored or
misread good context).

### 4.1 The four-evaluator pattern (LangSmith RAG tutorial)

LangSmith's RAG evaluation guide ([evaluate-rag-tutorial](https://docs.langchain.com/langsmith/evaluate-rag-tutorial),
[evaluation-approaches](https://docs.langchain.com/langsmith/evaluation-approaches#evaluate-rag-applications))
structures RAG eval as: build a dataset of `(question, reference answer)`
pairs → run the RAG pipeline on each question, capturing the retrieved
documents and the generated answer → score with four LLM-as-judge
evaluators — two reference-based (need a ground-truth answer) and two
reference-free (self-consistency checks against the retrieved context):

| Evaluator           | Compares                                 | Needs a reference answer? | Question it answers                                                |
| ------------------- | ---------------------------------------- | ------------------------- | ------------------------------------------------------------------ |
| Correctness         | generated answer vs. reference answer    | Yes                       | Is the answer factually right?                                     |
| Relevance           | generated answer vs. input question      | No                        | Does the answer actually address the question?                     |
| Groundedness        | generated answer vs. retrieved documents | No                        | Is the answer supported by the retrieved context, or hallucinated? |
| Retrieval relevance | retrieved documents vs. input question   | No                        | Did retrieval find the right documents?                            |

Each is implemented as an LLM-as-judge returning a boolean (or graded)
score against a rubric — e.g. groundedness asks the judge to confirm the
answer contains no claims beyond what the retrieved facts support.
Workflow-wise: build the dataset (e.g. via the LangSmith `Client`), run the
app to produce `(question, retrieved_docs, answer)` triples, then run all
four evaluator functions over the dataset (`client.evaluate()` in
LangSmith) to get per-example and aggregate scores you can regression-test
against a baseline — the same "CI for prompts" pattern from §2.

**Why decompose into four scores instead of one end-to-end accuracy
number:**

- Low correctness + high groundedness → the model faithfully used the
  retrieved context, but that context was wrong or insufficient — the bug
  is in **retrieval**, not generation.
- High correctness + low groundedness → the model likely answered from its
  own pretrained knowledge instead of the retrieved context. This can look
  fine on accuracy but is risky for citations/trust and won't generalize
  to questions the base model doesn't already know — a classic case where
  end-to-end accuracy alone hides a real problem.

### 4.2 Precision and recall for retrieval

The "Retrieval relevance" evaluator above gives a coarse relevant/not
judgment for a whole retrieved set. To diagnose retrieval quality more
precisely, apply standard information-retrieval metrics per query, using
either human-labeled relevance judgments or an LLM-as-judge grading each
retrieved chunk individually (same machinery as retrieval relevance, but
applied per-chunk rather than per-set).

For a given query, let:

- **Retrieved** = the top-_k_ chunks your retriever actually returned
- **Relevant** = all chunks in the corpus that are truly relevant to the
  query (ground truth, from labeling)

```
Precision@k = |Retrieved ∩ Relevant| / |Retrieved|   ( = |Retrieved ∩ Relevant| / k )
  "Of the chunks I returned, what fraction were actually relevant?"

Recall@k    = |Retrieved ∩ Relevant| / |Relevant|
  "Of all the relevant chunks that exist, what fraction did I return?"
```

**Worked example:** the corpus has 5 chunks truly relevant to a query. The
retriever returns the top 4 chunks, of which 3 are relevant.
Precision@4 = 3/4 = 0.75. Recall@4 = 3/5 = 0.6.

**Computing it in practice:** for each query in your golden dataset,
annotate once which corpus chunks are relevant (human review, or an LLM
judge grading candidate chunks binary relevant/not-relevant). Then, for
each query, compute precision@k and recall@k against what the retriever
actually returned, and macro-average across the eval set for an aggregate
score.

**Interpreting the results:**

- **Low precision, high recall** — the retriever is over-fetching: it
  catches the relevant chunks but buries them in noise. Symptom:
  groundedness/relevance drop because the generation step has a noisy
  context window, and cost/latency rise from unnecessary tokens. Fix:
  tighten the similarity threshold, add a reranker, reduce _k_.
- **High precision, low recall** — the retriever is too narrow: what it
  returns is relevant, but it's missing other relevant chunks. Symptom:
  correctness drops even though groundedness looks fine, because the model
  never saw the missing information. Fix: increase _k_, improve
  chunking/embeddings, add query rewriting/expansion, hybrid search
  (BM25 + vector).
- **Both low** — a fundamental retrieval problem (bad embeddings, bad
  chunking, or the corpus genuinely lacks the answer). Fix retrieval before
  touching the generation prompt.
- **Precision/recall trade off against _k_** — raising _k_ mechanically
  increases recall (more chances to catch relevant chunks) and typically
  lowers precision (more noise let in). Pick _k_ based on how much noise
  your generation step tolerates, and validate any _k_ sweep against
  downstream correctness/groundedness, not precision/recall in isolation.
- **F1@k** = `2 × (precision@k × recall@k) / (precision@k + recall@k)`
  collapses both into one number for ranking candidate retrieval configs —
  but weight it deliberately: a long-form generation step can often afford
  higher recall (an extra borderline chunk is cheap; the model can ignore
  it), while a system with a tight context budget should weight precision
  higher.

**Ranking-aware metrics** (worth knowing beyond precision/recall, which
treat the retrieved set as unordered): **MRR** (mean reciprocal rank — how
high the first relevant chunk ranks) and **NDCG** (normalized discounted
cumulative gain — rewards relevant chunks ranking higher, and supports
graded rather than just binary relevance). These matter more when chunk
_order_ affects the model (e.g. recency-weighted prompts) or when only the
first few chunks fit the context budget.

## 5. Evaluating agents (multi-step / tool-using)

Agents add a third axis beyond RAG's retrieval/generation split: the
**trajectory** — the sequence of steps (tool calls, routing decisions,
intermediate reasoning) the agent takes to arrive at an answer. LangSmith's
agent evaluation guides ([evaluation-approaches#agents](https://docs.langchain.com/langsmith/evaluation-approaches#agents),
[evaluate-complex-agent](https://docs.langchain.com/langsmith/evaluate-complex-agent))
describe three complementary approaches, trading off effort against
diagnostic depth.

### 5.1 Three evaluation approaches

| Approach | What it evaluates | Pros | Cons |
|---|---|---|---|
| Final response | treats the agent as a black box; grades only the final output vs. a reference answer (LLM-as-judge) | matches what the user actually experiences; simple to set up | doesn't reveal *where* a failure happened; slow/expensive to run the full agent for every candidate change |
| Single-step | one decision in isolation — e.g. did the router/intent-classifier pick the right tool, given a fixed prior state | pinpoints the exact failing component; cheap and fast (one LLM call, no full run needed) | only tests one step, not compounding errors across a real run; datasets get harder to build for steps deep in a trajectory |
| Trajectory | the full sequence of steps (tool calls + routing decisions) vs. a reference trajectory | most comprehensive; catches errors invisible in the final answer (right answer via the wrong/unsafe path) | most effort to build reference trajectories for and to score |

### 5.2 Trajectory evaluation in detail

LangSmith's `evaluate-complex-agent` tutorial (a LangGraph customer-support
agent handling refunds and music lookups) works like this:
- **Dataset**: each example's `inputs` is the user request; `outputs`
  contains both a reference final answer *and* a reference trajectory (the
  ordered list of expected node/tool names).
- **Capturing the actual trajectory**: stream the LangGraph run in debug
  mode, recording every node visited, and — whenever the tools node
  executes — append the tool name pulled from `AIMessage.tool_calls`. This
  produces an ordered list of what the agent actually did, directly
  comparable to the reference list.
- **Scoring**: instead of binary exact-match, score **partial credit** —
  walk the actual trajectory and count how many reference steps were
  completed, in the correct order; score = (matched reference steps) /
  (total reference steps). This rewards an agent that executed most of the
  correct plan even if it didn't reach the exact expected final state,
  where a binary pass/fail would zero it out entirely.
- **Why this catches what final-response grading misses**: an agent that
  skips the refund-eligibility check tool but still happens to return
  answer text that matches the reference would *pass* a final-response
  evaluator but *fail* (correctly) on trajectory. This is the agent
  equivalent of the RAG "high correctness / low groundedness" trap in
  §4.1 — the right answer arrived at via the wrong process, and only a
  process-aware evaluator catches it.

### 5.3 Single-step evaluation in detail

Isolate one LLM call — e.g. the intent classifier/router deciding which
tool or sub-agent to hand off to. Build a dataset of `(state up to this
point, expected route)` pairs; the evaluator does a direct equality check
between the routed destination and the reference. Because it invokes only
one LLM call, it's cheap enough to run on every commit as a fast regression
check on the highest-risk routing/tool-selection decisions, ahead of
paying for a full trajectory or final-response eval. The limitation is
dataset construction: an early step (e.g. the first router call on the raw
user message) is easy to seed, but a step several turns into a plan needs
realistic intermediate state — which means either running the agent partway
or hand-constructing a plausible partial trajectory.

### 5.4 Picking an approach in practice

Layer these the same way as the offline/online split in §2 and §4: use
**single-step** evals as fast, cheap regression tests on the highest-risk
decision points (routing, tool selection) in CI; use **trajectory**
evaluation for regression-testing larger changes (new tool, prompt
rewrite, model swap), since it catches the compounding/silent failures
final-response grading misses; reserve **final-response** LLM-as-judge
grading for end-to-end acceptance criteria and production sampling, where
the final output is fundamentally all you have to grade against
user-reported outcomes. This also connects to the "tool-call count per
task, retries" efficiency metric in §3 — a rising trajectory-eval failure
rate is often the leading indicator that shows up as a tool-call-count
regression in production before it becomes a task-success-rate drop.

## 6. Online monitoring & tracing

Production behavior always diverges from offline eval sets (real users are
messier). You need live visibility.

- **Tracing**: capture every step of an agent's execution — each LLM call
  (prompt, completion, tokens, latency), each tool call (args, result,
  duration), each retrieval (query, retrieved chunks, scores) — as a
  structured **trace** (parent span = the overall request, child spans =
  each step). Standard approach: OpenTelemetry-style spans; tooling
  options include Vertex AI's evaluation/monitoring, LangSmith, or custom
  logging into BigQuery.
- **Why trace-level (not just input/output) matters**: when an agent gives
  a bad answer, you need to see _which_ tool call or retrieval step went
  wrong — input/output logging alone can't localize the failure.
- **Dashboards & alerting**: track the metrics above over time, alert on
  drift (e.g. success rate drop, latency spike, cost spike, guardrail
  trigger spike).
- **Sampling for human review**: continuously sample a percentage of live
  traffic (plus 100% of flagged/low-confidence responses) for human
  review — feeds back into the golden dataset.

## 7. Guardrails

- **Input guardrails**: prompt-injection detection, PII detection/redaction
  on inputs, topic/scope filters (reject out-of-scope requests early).
- **Output guardrails**: safety classifiers (toxicity, policy violations),
  PII leak detection before returning a response, schema/format validation
  for structured outputs.
- **Tool-use guardrails**: least-privilege tool permissions (an agent
  shouldn't have a `delete_record` tool if its job is read-only Q&A),
  human-approval gates for high-risk actions (e.g. sending an email,
  making a payment).
- **Prompt injection**: malicious instructions embedded in retrieved
  documents or tool outputs trying to hijack the agent. Mitigate by
  treating all retrieved/tool content as untrusted **data**, never as
  instructions — reinforce this in the system prompt and validate/sanitize
  before acting on anything derived from it.

## 8. Rollout strategy for changes

Treat prompt/model/retrieval changes like code changes needing a safe
rollout path:

- **Shadow mode**: run the new version alongside production on real
  traffic, compare outputs, but don't serve the new version's output to
  users yet.
- **Canary**: serve the new version to a small % of traffic, monitor
  metrics, ramp up gradually.
- **Rollback plan**: version prompts/configs so you can instantly revert if
  a metric regresses.

## 9. What "good" observability enables (tie back to the JD)

- Faster root-causing of customer-reported issues (trace-level visibility)
- Confident, fast iteration (regression tests catch breakage before
  customers see it)
- Defensible cost/latency conversations with customers (you can show
  exactly where tokens/time go)
- The feedback loop the JD asks for: "identify repeatable field patterns
  and friction points... converting them into reusable modules or formal
  product feature requests" — you can't identify patterns you're not
  measuring.

---

## Could you explain/draw this cold?

- [ ] Explain the difference between offline eval and online monitoring,
      and when each catches a problem
- [ ] Name 3 LLM-as-judge biases and how to mitigate each
- [ ] Explain why trace-level observability beats input/output-only
      logging, with a concrete debugging example
- [ ] Draw a rollout pipeline for a prompt change: golden-set regression →
      shadow → canary → full rollout, with a rollback trigger
- [ ] Explain the difference between an input guardrail, an output
      guardrail, and a tool-use guardrail, with one example each
- [ ] Explain how you'd break down a cost-per-request regression to find
      the root cause
- [ ] Name the four RAG evaluators (correctness, relevance, groundedness,
      retrieval relevance), which need a reference answer, and what a
      low-correctness/high-groundedness result vs. a
      high-correctness/low-groundedness result each tell you
- [ ] Write the precision@k and recall@k formulas for retrieval from
      memory, and work a small numeric example
- [ ] Given a retrieval eval with low precision/high recall vs. high
      precision/low recall, explain the likely root cause and fix for each
- [ ] Explain why increasing k trades recall for precision, and how you'd
      pick k in practice
- [ ] Name the three agent evaluation approaches (final response,
      single-step, trajectory) and the effort/diagnostic-depth trade-off
      of each
- [ ] Explain how trajectory evaluation scores partial credit, and give an
      example where an agent passes final-response grading but fails
      trajectory grading
- [ ] Explain why single-step evaluation is cheap to run in CI but hard to
      build datasets for on later trajectory steps
