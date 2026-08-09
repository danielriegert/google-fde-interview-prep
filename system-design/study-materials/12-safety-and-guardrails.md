# Safety & Guardrails for Agentic/GenAI Systems

## 1. Why guardrails matter

Guardrails are safety mechanisms that validate and filter content at
strategic points in an agent's execution — detecting sensitive
information, enforcing policy, and blocking unsafe behavior before it
escalates. Unlike traditional input validation, GenAI systems face two
extra failure modes: the **model itself** can be tricked into unsafe
behavior (prompt injection), and the **output** is free-form text that can
leak sensitive data even when the input was clean. Primary use cases:

- Preventing PII leakage (into logs, into the model, back out to a user
  who shouldn't see it)
- Detecting/blocking prompt injection
- Blocking inappropriate or harmful content
- Enforcing business rules and compliance requirements
- Validating output quality/format before it reaches a user or a
  downstream system

## 2. Two implementation strategies

| Strategy               | How it works                                           | Trade-off                                                              |
| ----------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Deterministic**       | Regex, keyword matching, explicit rule checks             | Fast, cheap, fully explainable — but brittle, misses nuanced/novel violations |
| **Model-based**         | LLM or classifier scores content against a policy/rubric  | Catches subtle/semantic violations (paraphrased PII, indirect injection) — slower, costlier, and itself imperfect (needs its own eval, see file 03) |

In practice you layer both: cheap deterministic checks run first and
catch the bulk of cases; model-based checks catch what regex misses. This
mirrors the offline-eval "LLM-as-judge" pattern in
[03-evaluation-observability.md](03-evaluation-observability.md) — a
guardrail is really just an evaluator running inline, synchronously,
before a step is allowed to proceed.

## 3. Where guardrails attach in an agent's execution

- **Input guardrails**: prompt-injection detection, PII
  detection/redaction on the incoming user message, topic/scope filters
  (reject out-of-scope requests early, before spending a model call).
- **Output guardrails**: safety classifiers (toxicity, policy violations),
  PII leak detection before returning a response, schema/format
  validation for structured outputs.
- **Tool-use guardrails**: least-privilege tool permissions (an agent
  shouldn't have a `delete_record` tool if its job is read-only Q&A),
  human-approval gates for high-risk actions (sending an email, making a
  payment).
- **Tool-result guardrails**: often overlooked — a tool can return
  attacker-controlled or sensitive content (e.g. a web search result
  containing injected instructions, or a database row containing a
  customer's SSN) just as easily as user input can. Any guardrail applied
  to input should generally also be considered for tool output.

**Prompt injection**: malicious instructions embedded in retrieved
documents or tool outputs, trying to hijack the agent. Mitigate by
treating all retrieved/tool content as untrusted **data**, never as
instructions — reinforce this in the system prompt, and validate/sanitize
before acting on anything derived from it.

## 4. PII guardrails — LangChain's `PIIMiddleware`

Reference: [LangChain guardrails docs](https://docs.langchain.com/oss/python/langchain/guardrails#built-in-pii-types-and-configuration).

LangChain ships built-in middleware for detecting and handling PII in
agent conversations — useful shorthand for a pattern worth knowing even
outside LangChain specifically: PII handling should be a declarative,
composable policy attached per data type, not scattered regex checks
inline in application code.

### 4.1 Built-in PII types

Detected out of the box, with no custom regex needed:

| `pii_type`    | Detects                          |
| ------------- | ----------------------------------- |
| `email`       | Email addresses                     |
| `credit_card` | Credit card numbers (Luhn-validated — rejects random 16-digit numbers that aren't real card numbers) |
| `ip`          | IP addresses                        |
| `mac_address` | MAC addresses                       |
| `url`         | URLs                                |

Anything else (API keys, SSNs, internal customer IDs, phone numbers) is
supported via a custom `detector` (regex or function) passed to the same
middleware — the built-in list is a starting set, not a ceiling.

### 4.2 Handling strategies

| `strategy` | Behavior                                                             |
| ---------- | ------------------------------------------------------------------- |
| `redact`   | Replace with `[REDACTED_{PII_TYPE}]` (default)                      |
| `mask`     | Partially obscure, preserving a recognizable remnant — e.g. a credit card becomes `****-****-****-1234` |
| `hash`     | Replace with a deterministic hash — irreversible, but the same input always hashes the same way, so you can still de-duplicate/correlate without ever storing the raw value |
| `block`    | Raise an exception when detected — use for hard policy violations rather than something you want to silently strip and continue on (e.g. a leaked API key in a user message) |

`redact`/`mask`/`hash` all let the conversation continue with the
sensitive value neutralized; `block` stops execution entirely. Pick
`block` for PII types where continuing at all is the wrong call (secrets,
credentials) and `redact`/`mask`/`hash` for PII that's expected to show up
in normal conversation and just needs to be handled safely (a customer
giving their email in a support chat).

### 4.3 Configuration parameters

| Parameter               | Purpose                                | Default |
| ------------------------ | ----------------------------------------- | ------- |
| `pii_type`               | Which PII type to detect (built-in name or custom label) | required |
| `strategy`                | How to handle a detection (`redact`/`mask`/`hash`/`block`) | `"redact"` |
| `detector`                | Custom regex pattern or detection function, for types beyond the built-in five | uses built-in pattern for known types |
| `apply_to_input`          | Check user messages                      | `True`  |
| `apply_to_output`         | Check AI-generated responses             | `False` |
| `apply_to_tool_results`   | Check tool call outputs                  | `False` |

Note the asymmetric defaults: input scanning is on by default, but output
and tool-result scanning are opt-in. That's a reasonable default for a
generic library, but for anything handling regulated data (healthcare,
financial services) you should treat `apply_to_output` and
`apply_to_tool_results` as things to explicitly turn on — the model can
echo PII it was never directly given (e.g. inferred from context, or
pulled from a tool call) just as easily as a user can type it in.

### 4.4 Example configuration

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-5.5",
    tools=[customer_service_tool, email_tool],
    middleware=[
        # Redact emails in user input before sending to the model
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        # Mask credit cards in user input
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        # Block API keys outright via a custom regex detector
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
)
```

Middleware entries are independent and additive — each `PIIMiddleware`
instance handles exactly one `pii_type`, so a real configuration is
typically a list of several, one per sensitive field the application
cares about, each with the strategy appropriate to that field.

## 5. Human-in-the-loop guardrails

A middleware pattern that requires human approval before executing
sensitive operations — financial transactions, data modifications,
external communications (sending an email, posting to an external API).
Configure which specific tools require approval and auto-approve safe
ones; use a thread/session ID to persist the paused state across the
approval round-trip (the agent run suspends, waits for a human decision,
then resumes with that decision fed back in). This is the tool-use
guardrail from §3 made concrete — least-privilege tool grants stop an
agent from having a dangerous capability at all; human-in-the-loop is for
capabilities the agent legitimately needs but shouldn't exercise
unsupervised.

## 6. Custom guardrails

Beyond built-ins, custom middleware hooks at two points:

- **Before-agent hooks**: run at invocation start, for session-level
  checks — authentication, rate limiting, input content filtering. Cheap
  because they run before any model call.
- **After-agent hooks**: run on the final output before it returns to the
  user — model-based safety scoring, compliance scans, schema validation.

Both support short-circuiting straight to the "end" node when a violation
is detected, so a blocked request never reaches (or leaves) the model.

## 7. Layered defense in depth

Guardrails compose in order rather than substituting for each other:
**deterministic input filters → PII protection → human approval for
high-risk tool calls → model-based output safety validation**. Each layer
catches what the previous one is bad at — regex is fast but blind to
paraphrase, PII middleware is targeted but doesn't know about business
policy, human approval is expensive but perfect for the handful of
truly high-stakes actions, and a model-based output check catches
whatever slipped through everything upstream. Design the layering so
the cheapest, fastest checks run first and only genuinely ambiguous
cases fall through to the expensive ones.

## 8. Measuring guardrails in production

Guardrails are a system component like any other and need the same
observability treatment as file 03's eval/monitoring guidance:

- **Guardrail trigger rate**: how often each guardrail fires, broken out
  by type. A sudden spike is often the earliest signal of either an
  attack (prompt injection attempts ramping up) or a false-positive
  regression (a prompt change made the model start phrasing normal
  responses in a way that trips a filter).
- **PII leak rate**: PII that reached a user/log/downstream system
  *despite* guardrails — the metric that actually matters, since trigger
  rate only tells you the guardrail fired, not that it fired on
  everything it should have. Requires sampling production traffic (or a
  held-out eval set with known PII injected) and checking for leakage
  the guardrail should have caught.
- False positives (legitimate content blocked/redacted unnecessarily)
  matter too — track them the same way you'd track LLM-as-judge
  miscalibration in file 03, since an over-aggressive guardrail degrades
  the product experience just as much as an under-aggressive one creates
  risk.

## 9. GCP-native guardrails: Model Armor

**Model Armor** is GCP's managed screening service for prompts and
responses — the concrete GCP answer for "where do output/input guardrails
actually run" instead of hand-rolling the checks in §2-§3:

- Screens both **prompts** (input) and **responses** (output) for prompt
  injection/jailbreak attempts, sensitive-data leakage (integrates with
  Sensitive Data Protection/DLP for PII), and harmful content — i.e. it
  covers the input-guardrail and output-guardrail attachment points from
  §3 as a single managed service rather than two custom middlewares.
- Deployable inline in the request path (e.g. in front of a Vertex AI/
  Model Garden model call, or as a Cloud Run/GKE sidecar check) so a
  violation is caught before the model call or before the response
  reaches the user — the same "short-circuit before proceeding" pattern
  as the before/after-agent hooks in §6.
- Complements, doesn't replace, the LangChain-style middleware above: use
  Model Armor for the deterministic + policy-classifier layer that's
  common across an org's agents, and app-level middleware (`PIIMiddleware`,
  human-in-the-loop) for logic specific to one agent's tools/workflow —
  consistent with the layered-defense ordering in §7.

---

## Could you explain/draw this cold?

- [ ] Explain the difference between deterministic and model-based
      guardrails, and why real systems layer both rather than picking one
- [ ] Name the four points in an agent's execution where a guardrail can
      attach (input, output, tool-use, tool-result), with one example
      violation each
- [ ] Name the five built-in PII types LangChain's `PIIMiddleware`
      detects out of the box, and how you'd add a sixth (e.g. SSN) that
      isn't built in
- [ ] Explain the four PII handling strategies (redact/mask/hash/block)
      and when you'd choose each — specifically why `hash` beats `redact`
      when you need to correlate records without storing the raw value
- [ ] Explain why `apply_to_output` and `apply_to_tool_results` default
      to off, and why that default is risky for regulated data
- [ ] Explain the difference between least-privilege tool permissions and
      human-in-the-loop approval as two ways of guarding tool use
- [ ] Explain the "layered defense in depth" ordering for guardrails and
      why cheap checks should run before expensive ones
- [ ] Explain the difference between guardrail trigger rate and PII leak
      rate, and why trigger rate alone can't tell you the guardrail is
      working
- [ ] Name the GCP-native guardrail service (Model Armor), what it screens
      (prompt injection, sensitive-data leakage, harmful content) on both
      input and output, and how it relates to app-level middleware like
      `PIIMiddleware`
