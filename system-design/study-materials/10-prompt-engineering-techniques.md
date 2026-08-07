# Prompt Engineering Techniques

Source: [IBM — Prompt Engineering Techniques](https://www.ibm.com/think/topics/prompt-engineering-techniques)

## 1. What a prompt is, and three ways to structure one

A **prompt** is the input text/query that guides a model's behavior,
defines the task, and sets context.

## 3. Foundational techniques (how much example data you give the model)

| Technique               | What it does                                                                                          | Example framing                                                                                   |
| ----------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Zero-shot prompting** | Ask the model to do the task with no examples, relying entirely on pretrained knowledge.              | "Explain climate change... in simple terms." — no examples given.                                 |
| **One-shot prompting**  | Give exactly one example to anchor format/tone before the real ask.                                   | Show one worked "topic → explanation" pair, then ask for climate change.                          |
| **Few-shot prompting**  | Give a handful of examples in-prompt to demonstrate the task pattern (a form of in-context learning). | Show 2 "topic → explanation" pairs (photosynthesis, gravity), then "Now explain: Climate Change." |

Tradeoff: zero-shot costs the fewest tokens and works well when the task
is common/well-represented in pretraining; few-shot costs more context
but sharply narrows output format/tone/difficulty-level, which matters
most for structured or stylistically specific outputs.

## 4. Reasoning-enhancement techniques

| Technique                                | What it does                                                                                                                                                                                        |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chain of thought (CoT)**               | Prompt the model to reason step by step, breaking the task into intermediate components before the final answer. Classic "Step 1... Step 2... Step 3..." scaffolding.                               |
| **Self-consistency**                     | Generate multiple independent reasoning paths/answers, then pick the most coherent/consistent one. Trades extra inference cost for reliability on reasoning-heavy tasks.                            |
| **Tree of thoughts (ToT)**               | Explore multiple branches of reasoning or candidate approaches in parallel, evaluate each, then select/elaborate the best one — a superset of CoT that searches instead of committing to one chain. |
| **Generated knowledge prompting**        | Ask the model to first generate relevant background facts/principles, then use that generated context to answer the real question.                                                                  |
| **Directional stimulus prompting (DSP)** | Nudge the model toward a specific angle, perspective, or tone with cue words (e.g., "from an environmentalist's perspective").                                                                      |
| **Multimodal CoT**                       | Chain-of-thought reasoning that spans modalities — text plus images/audio/infographics — not just text.                                                                                             |
| **Graph prompting**                      | Use graph-structured input (nodes/edges representing concepts or data relationships) so the model reasons over explicit relationships rather than linear text.                                      |

CoT and ToT are the two most interview-relevant here: CoT = one reasoning
chain, ToT = branch, evaluate, prune, pick — pay the extra compute when
the task has multiple plausible solution paths and picking the wrong one
early is costly.

## 5. Self-directing / optimization techniques

| Technique                            | What it does                                                                                                                                                                                                                                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Meta prompting**                   | Ask the model to generate or refine its own prompt for the task before executing it.                                                                                                                                                                                                         |
| **Automatic prompt engineer**        | Use the model itself to generate and optimize candidate prompts for a task, automating what a human prompt engineer would iterate on by hand.                                                                                                                                                |
| **Active-prompt**                    | Dynamically refine the prompt based on the model's own intermediate outputs — an initial prompt is followed by a targeted follow-up that fills gaps the first response left.                                                                                                                 |
| **Prompt tuning**                    | A lightweight fine-tuning variant: learn a small set of continuous "soft prompt" embeddings prepended to the input while the base model stays frozen. Sits between pure prompting and full fine-tuning — see [07-fine-tuning.md](./07-fine-tuning.md) for where this fits against LoRA/PEFT. |
| **Prompt optimization (e.g., DSPy)** | Programmatic frameworks that search/optimize prompt structure and few-shot examples against a metric, rather than hand-tuning wording.                                                                                                                                                       |
| **Prompt caching**                   | An infra technique, not a wording technique: cache the (often large, static) prefix of a prompt — system instructions, few-shot examples, retrieved context — so repeated calls skip reprocessing it. Pure latency/cost lever: cache the stable prefix, vary only the suffix.                |

## 6. Agentic / tool-integrated techniques

These are the techniques that turn a single prompt into a system — heavy
overlap with [02-agentic-systems.md](./02-agentic-systems.md), which goes
deeper on the architecture side.

| Technique                                           | What it does                                                                                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prompt chaining**                                 | Link multiple prompts so one's output feeds the next's input — decomposes a multi-step task into a pipeline (define → causes → effects, for the climate example).                           |
| **ReAct**                                           | Interleave reasoning ("Thought") with actions/tool calls ("Action") and observations, so the model reasons about what to do next between tool invocations. Covered in depth in file 02.     |
| **Reflexion**                                       | The model evaluates and critiques its own prior output, then produces an improved version — a self-refinement loop (verbal reinforcement rather than gradient-based).                       |
| **Automatic reasoning and tool-use (ART / ARTool)** | Integrates reasoning with external tools/APIs (calculators, search, data lookups) so the model can act on real data mid-reasoning, not just narrate about it.                               |
| **Program-aided language models (PAL)**             | The model writes and (conceptually) executes code as part of answering — offloads precise computation to a programming language interpreter instead of doing arithmetic/logic in free text. |
| **Retrieval-augmented generation (RAG)**            | Combine retrieval of external/up-to-date/domain-specific knowledge with generation. Full treatment in [01-rag.md](./01-rag.md).                                                             |

## 7. Prompt hacking and security (adjacent, worth knowing by name)

- **Prompt injection** — malicious or unintended instructions smuggled
  into the input (directly by a user, or indirectly via retrieved/tool
  content) that override the system's intended behavior.
- **AI jailbreak** — prompting strategies designed to bypass a model's
  safety/alignment guardrails.

These matter operationally any time untrusted content (user input, web
pages, tool output, retrieved documents) enters the context window — see
the "tool output should be treated as untrusted input" note in file 02.

## 8. Quick reference: which technique for which problem

- Task is common and well-defined → **zero-shot**, cheapest.
- Need a specific output format/tone/difficulty level → **few-shot** (or
  one-shot if a single example is enough to anchor it).
- Task requires multi-step logic (math, multi-hop reasoning) → **CoT**.
- Multiple plausible solution paths, wrong-branch cost is high →
  **tree of thoughts**.
- Need higher reliability on a reasoning task and can afford extra calls
  → **self-consistency** (sample + vote).
- Task needs facts the model may not reliably recall → **generated
  knowledge prompting** or, better, **RAG** if the facts are external/
  volatile.
- Multi-step pipeline where each step's output shapes the next →
  **prompt chaining**.
- Task needs live data, computation, or side effects → **ReAct** / **ART**
  / **PAL** (tool-use family) — this is where "prompting" becomes
  "agent design."
- Output quality benefits from self-critique → **Reflexion**.
- You want to stop hand-tuning wording and optimize systematically →
  **DSPy-style prompt optimization** or **prompt tuning** (if you can
  afford to train soft-prompt embeddings).
- Repeated calls share a large static prefix (system prompt, few-shot
  examples, long context) → **prompt caching**, purely for cost/latency.

## 9. Known limitations

- **Hallucination** — models can produce fabricated or inaccurate content
  regardless of how well the prompt is engineered; prompting reduces but
  doesn't eliminate this.
- **No universal prompt** — designing prompts that generalize across
  diverse scenarios remains largely trial-and-error; what works for one
  model/task doesn't transfer cleanly.
- **General vs. task-specific tension** — balancing a model's broad
  capabilities against a narrow, domain-specific objective is genuinely
  hard, especially for specialized enterprise tasks.
- Prompting is one lever among several (RAG, fine-tuning) — see
  [07-fine-tuning.md](./07-fine-tuning.md) for the decision framework on
  when prompting alone isn't enough.

---

## Could you explain/draw this cold?

- [ ] Name the three prompt-structure categories (direct, open-ended,
      task-specific) and give an example of each
- [ ] Explain zero-shot vs. one-shot vs. few-shot and when you'd reach
      for each
- [ ] Walk through chain-of-thought on a concrete example, then explain
      how tree-of-thoughts differs (branch/evaluate/select vs. one chain)
- [ ] Explain self-consistency and why it costs more but improves
      reliability on reasoning tasks
- [ ] Explain the difference between generated knowledge prompting and
      RAG (internal generated facts vs. external retrieved facts)
- [ ] Describe prompt chaining with a 3-step example pipeline
- [ ] Explain ReAct's Thought/Action/Observation loop and how it differs
      from plain CoT (see [02-agentic-systems.md](./02-agentic-systems.md))
- [ ] Explain Reflexion (self-critique loop) and PAL (code-execution
      offload) and when each earns its extra cost
- [ ] Explain prompt tuning vs. full fine-tuning vs. plain prompting as a
      spectrum (see [07-fine-tuning.md](./07-fine-tuning.md))
- [ ] Explain why prompt caching is an infra/cost lever, not a wording
      technique
- [ ] Name prompt injection and jailbreaking, and explain why any
      untrusted input into a prompt (user text, retrieved docs, tool
      output) is an injection surface
- [ ] State the three main limitations of prompt engineering per IBM:
      hallucination, lack of generalizable prompts, and the
      general-vs-task-specific tradeoff
