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
  - *Exact/rule-based match*: works for structured outputs (did it call
    the right tool with the right args? did it return valid JSON?).
  - *LLM-as-judge*: use a strong model to score a response against a
    rubric (faithfulness, relevance, tone, correctness). Cheap and
    scalable vs. human review, but has known biases (see below).
  - *Human review*: gold standard for subjective quality, expensive —
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

| Category | Metric | Notes |
|---|---|---|
| Task quality | Task success rate | Did the agent actually accomplish the user's goal end-to-end? |
| Groundedness | Faithfulness / hallucination rate | Is the answer supported by retrieved context / tool outputs? |
| Relevance | Answer relevancy | Does the response address what was asked? |
| Retrieval | Precision@k, recall@k | Is RAG retrieving the right chunks (see file 01)? |
| Latency | p50/p95/p99 latency, time-to-first-token | Tail latency matters more than average for UX |
| Cost | Cost-per-request, tokens/sec | Explicitly named in JD as an "LLM-native metric" to track |
| Efficiency | Tool-call count per task, retries | Rising tool-call count often signals prompt/tool-design drift |
| Safety | Guardrail trigger rate, PII leak rate | See guardrails section below |

**Cost-per-request** breaks down into input tokens + output tokens (priced
differently) × model tier — track separately so you know whether a cost
regression came from longer prompts, longer outputs, or a model upgrade.

## 4. Online monitoring & tracing

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
  a bad answer, you need to see *which* tool call or retrieval step went
  wrong — input/output logging alone can't localize the failure.
- **Dashboards & alerting**: track the metrics above over time, alert on
  drift (e.g. success rate drop, latency spike, cost spike, guardrail
  trigger spike).
- **Sampling for human review**: continuously sample a percentage of live
  traffic (plus 100% of flagged/low-confidence responses) for human
  review — feeds back into the golden dataset.

## 5. Guardrails

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

## 6. Rollout strategy for changes

Treat prompt/model/retrieval changes like code changes needing a safe
rollout path:
- **Shadow mode**: run the new version alongside production on real
  traffic, compare outputs, but don't serve the new version's output to
  users yet.
- **Canary**: serve the new version to a small % of traffic, monitor
  metrics, ramp up gradually.
- **Rollback plan**: version prompts/configs so you can instantly revert if
  a metric regresses.

## 7. What "good" observability enables (tie back to the JD)

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
