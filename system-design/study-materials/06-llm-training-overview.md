# LLM Training & Serving — Overview

Why this file exists: the JD/interview explicitly names "LLMs (training,
serving, and troubleshooting them, and your role in a client's digital
transformation)" as a GenAI Concepts criterion. As an FDE you will almost
never pretrain a foundation model — but you need enough of the pipeline to
(a) explain tradeoffs to a client, (b) know what's actually adjustable vs
fixed when something goes wrong, and (c) place fine-tuning (file 07)
correctly against prompting/RAG.

## 1. The full pipeline, end to end

```
[Massive web-scale corpus]
        │
        ▼
  PRETRAINING  (self-supervised, next-token prediction)
        │  → base model: fluent, broad knowledge, NOT instruction-following
        ▼
  SUPERVISED FINE-TUNING (SFT)  (instruction/response pairs)
        │  → follows instructions, adopts a "helpful assistant" style
        ▼
  ALIGNMENT  (RLHF / RLAIF / DPO — human or AI preference data)
        │  → helpful, harmless, honest; reduces unwanted behaviors
        ▼
  [Released foundation model]  (e.g. Gemini)
        │
        ▼
  (optional) TASK/DOMAIN FINE-TUNING  ← this is where FDEs sometimes operate (file 07)
        │
        ▼
  SERVING / INFERENCE  ← this is where FDEs mostly operate
        │
        ▼
  PRODUCTION MONITORING & TROUBLESHOOTING  ← and here
```

**The FDE reality**: you live almost entirely in the bottom two boxes
(serving, monitoring) plus occasionally the optional fine-tuning box.
Pretraining and alignment are done once, upstream, by the model provider
(Google, in this role). Know the pipeline well enough to explain *why* the
model behaves as it does, not to reproduce it.

## 2. Pretraining, at the depth you need

- **Architecture**: transformer decoder, self-attention over token
  sequences — you don't need to derive attention math, but should be able
  to say *why* it works: every token attends to every other token in
  context, capturing long-range dependencies that RNNs struggled with.
- **Objective**: next-token prediction on massive unlabeled text/code/
  multimodal corpora — this is why base models are fluent completers but
  not naturally instruction-followers or safe by default.
- **Tokenization**: text is split into subword tokens (e.g. BPE/
  SentencePiece) before modeling — matters practically because cost,
  context window, and latency are all measured in tokens, not words/chars.
  Non-English languages and code often tokenize less efficiently (more
  tokens per unit of content) — relevant to cost estimates for
  international clients.
- **Scale**: performance improves predictably with more data + parameters
  + compute, up to a point — the **Chinchilla scaling law** finding was
  that most large models of the era were *under-trained* on data relative
  to their parameter count; "bigger" isn't automatically "better" without
  proportionally more data.
- **What you'd tell a client**: "the base model's knowledge is frozen at a
  training cutoff and is a statistical distillation of its training
  corpus — that's precisely the gap RAG (file 01) exists to fill, and why
  a model can be fluent yet confidently wrong about anything post-cutoff
  or proprietary."

## 3. Post-training: SFT and alignment

- **SFT (Supervised Fine-Tuning)**: train the base model further on curated
  (instruction, ideal response) pairs — this is what turns a raw completer
  into something that follows "summarize this" or "write a SQL query"
  style prompts.
- **RLHF (Reinforcement Learning from Human Feedback)**: humans rank
  multiple model outputs for the same prompt → train a reward model on
  those rankings → use RL (classically PPO) to optimize the LLM against
  the reward model. Expensive (human labeling), but effective at aligning
  tone/safety/helpfulness.
- **RLAIF**: same idea, but an AI judge ranks outputs instead of humans —
  cheaper, scales better, quality depends on the judge model.
- **DPO (Direct Preference Optimization)**: a simpler alternative to
  RLHF/PPO — directly optimizes the model on preference pairs (chosen vs
  rejected response) without training a separate reward model or running
  full RL. Increasingly common because it's simpler to implement and
  tune, with comparable results in many cases.
- **Why this matters for you**: alignment is *why* a production model
  refuses certain requests, hedges, or has a particular "voice" — when a
  client says "the model won't do X" or "the tone is wrong," you're often
  fighting alignment-time behavior with prompting/system-instructions
  rather than something you can retrain.

## 4. Serving / inference — the part you actually own

- **Decoding strategy**: how the next token is chosen from the model's
  probability distribution.
  - **Greedy**: always pick the highest-probability token — deterministic,
    can be repetitive/bland.
  - **Temperature sampling**: scales the probability distribution before
    sampling — low temp (~0-0.3) = more deterministic/focused (good for
    extraction, code, factual QA); high temp (~0.7-1.0) = more diverse/
    creative (good for brainstorming, creative content generation).
  - **Top-k / top-p (nucleus) sampling**: restrict sampling to the k most
    likely tokens, or the smallest set of tokens whose cumulative
    probability exceeds p — prevents sampling from the low-probability
    "long tail" that produces incoherent output.
  - **Practical rule of thumb**: temperature near 0 for
    agents/tool-calling/data-extraction (you want reliability, not
    creativity); higher temperature for open-ended creative generation
    (relevant to the GenMedia scenario's creative copy/brief generation).
- **KV cache**: during autoregressive generation, attention key/value
  tensors for already-generated tokens are cached instead of recomputed
  every step — this is *the* reason generation is fast at all; cache size
  grows with sequence length and is a real memory constraint at long
  context lengths.
- **Batching**: serving frameworks batch concurrent requests to maximize
  GPU/TPU utilization. **Continuous/dynamic batching** (vs static batching)
  lets new requests join a batch mid-flight instead of waiting for the
  whole batch to finish — standard in modern serving stacks, big latency
  win under concurrent load.
- **Quantization**: reduce numeric precision of model weights (e.g. FP16 →
  INT8/INT4) to cut memory footprint and increase throughput, at some
  quality cost — a lever for cost/latency-sensitive deployments, usually
  decided by the model provider/serving platform rather than the FDE, but
  you should know it's why smaller/cheaper model tiers exist and behave
  slightly differently than the full-precision original.
- **Prefill vs decode**: two distinct phases of a single inference call —
  **prefill** processes the entire input prompt in parallel (compute-bound,
  scales with input length), **decode** generates output tokens one at a
  time (memory-bandwidth-bound, scales with output length). Useful for
  explaining latency: a long prompt with a short answer has a very
  different bottleneck than a short prompt with a long generated answer.
- **Where this lives on GCP**: you call a hosted endpoint (Vertex AI /
  Gemini API) — Google owns the serving infra, decoding params
  (temperature, top-p, max tokens) are what you actually control via the
  API. See file 05 for Cloud Run/GKE/Vertex Endpoints deployment choices
  for *your* orchestration layer around the model call.

## 5. Troubleshooting LLMs in production

A structured way to reason about "the model is misbehaving" reports —
this maps directly to the interview's Troubleshooting criterion.

| Symptom | Likely layer | How to isolate |
|---|---|---|
| Wrong/outdated facts | Knowledge gap (pretraining cutoff or missing private data) | Check if RAG is even wired to the query path; check retrieval logs for a miss vs a bad generation |
| Confidently wrong (hallucination) despite correct context | Generation, not retrieval | Replay the exact retrieved context through the prompt manually — if context was right and answer still wrong, it's a grounding/prompting issue, not a data issue |
| Output tone/format suddenly changed | Model version upgrade, alignment behavior, or a system prompt change | Diff the system prompt / model version between last-known-good and now; providers periodically update model versions behind a stable endpoint name |
| Latency spike | Serving layer — prefill (long input) vs decode (long output) vs infra (cold start, autoscaling lag, regional load) | Check input/output token counts separately; check for cold-start patterns (first request after idle); check provider status page |
| Cost spike | Token volume, model tier, or retry storms | Break down cost by model tier and by request; check for a retry loop or an unbounded context (e.g. unbounded chat history growth) |
| Inconsistent output for the same input | Non-zero temperature/sampling, or a race condition in retrieval (index updated mid-session) | Test at temperature 0 to isolate sampling variance from a real non-determinism bug |
| Regression after a prompt/model change | Missing regression testing | This is exactly what an eval harness (file 03) exists to catch pre-deploy — if you don't have one, that's the actual root cause |

**General diagnostic posture** (the thing interviewers are grading): don't
guess-fix. State a hypothesis, name the specific log/trace/test you'd pull
to confirm or rule it out, then narrow. "Is this a retrieval problem or a
generation problem?" is almost always the first fork for a RAG/agent
system — answer it before touching prompts.

## 6. Your role in a client's digital transformation

The interview names this explicitly — it's asking you to place the above
technical knowledge into a change-management narrative, not just an
architecture diagram:

- Most clients don't need a custom-trained model; they need **help
  choosing** among prompting / RAG / fine-tuning for their actual
  constraints (data sensitivity, latency, budget, in-house ML maturity) —
  your value is translating their business problem into the right point
  on that spectrum, and explaining *why* simpler is usually right first.
- Be ready to narrate the "crawl → walk → run" arc: prompt-engineered
  prototype (fast, cheap, validates the use case) → add RAG for
  grounding/freshness → add evals/guardrails for production trust → only
  then consider fine-tuning if prompting/RAG genuinely can't hit the bar
  (see file 07, section 1, for that decision explicitly).
- Digital transformation framing = you are also the person who explains
  *why* a hallucination happened, *what* guardrail now prevents its class
  of failure, and *how* the client's own team can eventually operate the
  system without you — production hardening and knowledge transfer are
  part of the technical answer, not just an afterthought.

---

## Could you explain/draw this cold?

- [ ] Draw the full pipeline from pretraining to production monitoring and
      point to the 1-2 boxes an FDE actually operates in
- [ ] Explain SFT vs RLHF vs DPO in one sentence each
- [ ] Explain temperature and top-p, and pick appropriate values for (a)
      a tool-calling agent step, (b) a creative ad-copy generation step
- [ ] Explain why KV caching matters and what happens to latency/memory
      as context length grows
- [ ] Walk through the diagnostic fork for "the agent gave a wrong
      answer": how do you determine retrieval vs generation fault in
      under 2 minutes of log-reading?
- [ ] Explain prefill vs decode and use it to explain why a long-prompt/
      short-answer request and a short-prompt/long-answer request have
      different latency profiles
- [ ] Give the 60-second "crawl/walk/run" narrative for a client asking
      "should we just fine-tune our own model?"
