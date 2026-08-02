# Agentic Systems — Tool Use, Orchestration, MCP

## 1. What makes something an "agent"

A plain LLM call: `prompt → completion`, one shot, no interaction with the
world. An **agent** adds a loop: the model can decide to call **tools**
(functions/APIs), observe the result, and decide again — repeating until
it produces a final answer. The defining property is **the model controls
control flow**, not a fixed script.

Minimum ingredients: LLM + tool definitions + an execution loop + (usually)
memory/state.

## 2. Function/tool calling mechanics

- You give the model a list of tool schemas (name, description, JSON-schema
  args) alongside the prompt.
- Model outputs a structured tool-call request (name + args) instead of
  free text when it decides a tool is needed.
- Your code executes the actual function/API call, feeds the result back
  into the conversation as a new message, and calls the model again.
- Model can chain multiple tool calls before producing a final answer.

This is the mechanism that makes **RAG-as-a-tool**, **MCP**, and
**multi-agent hand-off** all work — they're all "tool calling" at
different granularities.

## 3. ReAct: the base reasoning pattern

**Re**ason + **Act**, interleaved:

```
Thought: I need the customer's order status to answer this.
Action: call get_order_status(order_id=123)
Observation: {"status": "shipped", "eta": "2026-08-03"}
Thought: I have what I need.
Final Answer: Your order shipped and should arrive Aug 3.
```

The model narrates reasoning between tool calls, which (a) improves
accuracy by forcing explicit intermediate steps, (b) gives you an audit
trail for debugging/observability.

Other planning patterns worth knowing:

- **Plan-and-Execute**: model writes a full multi-step plan up front, then
  executes each step (vs. ReAct's step-by-step improvisation). More
  predictable, less adaptive to surprises mid-execution.
- **Reflection / self-critique**: after producing an answer or plan, the
  model (or a second call) critiques it and revises — improves quality at
  the cost of latency/tokens.
- **Tree of Thought**: explore multiple reasoning branches, prune bad ones
  — expensive, used for hard reasoning tasks, rarely needed for typical
  enterprise agent tasks.

## 4. Single agent vs multi-agent — when to split

Default to **one well-prompted agent with good tools** first. Split into
multiple agents only when you hit a real limit:

- Context window pressure (one agent's job needs too much context to hold
  at once)
- Distinct specialized skill sets that benefit from separate system
  prompts/tools (e.g. a SQL-writing specialist vs a customer-tone
  specialist)
- Need for parallelism (independent sub-tasks that can run concurrently)
- Reliability via separation of concerns (a "critic" agent checking a
  "worker" agent's output)

When to stay single-agent

    Tasks that fit comfortably within one context window with room to spare
    Workflows where the steps are tightly interdependent and parallelism provides no benefit
    Prototyping or early development phases where simplicity matters more than scale
    Cases where the orchestration overhead would exceed the performance benefit

Cost of splitting: more latency (extra LLM round-trips), more orchestration
complexity, harder to debug, more tokens burned on inter-agent
coordination. **This tradeoff is a strong interview signal** — don't
default to multi-agent just because it sounds sophisticated.

## 5. Multi-agent orchestration patterns

https://docs.langchain.com/oss/python/langchain/multi-agent

| Pattern                          | Shape                                                                        | Use case                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Sequential/pipeline              | A → B → C, each hands off output to next                                     | Well-defined multi-stage workflow (draft → review → format)                               |
| Supervisor/worker (hierarchical) | Orchestrator agent routes tasks to specialist sub-agents, aggregates results | Most common enterprise pattern — e.g. router decides "billing agent" vs "technical agent" |
| Network/swarm                    | Agents can hand off to each other directly, no fixed hierarchy               | Flexible but harder to reason about/debug; higher risk of loops                           |
| Debate/critique                  | Two+ agents argue/critique to converge on a better answer                    | Higher-stakes reasoning tasks where single-pass quality isn't enough                      |

## 6. Anatomy of a multi-agent system & routing patterns

_(source: [AWS — Multi-Agent Architectures](https://aws.amazon.com/marketplace/build-learn/ai-agent-learning-series/multi-agent-architectures#anatomy-of-a-multi-agent-system--e6infr))_

### Four structural planes

Useful mental model for decomposing _any_ multi-agent system in a design
discussion — map the system onto these four planes before picking a
framework:

- **Control plane (orchestration)** — the orchestrator holds the
  high-level task understanding, decomposes goals into subtasks, assigns
  work, monitors progress, and synthesizes results. Critically, **the
  orchestrator doesn't perform the work itself — it directs**. Keeping
  that separation clean is what makes the system debuggable.
- **Execution plane (specialized agents)** — each agent has a narrowly
  scoped responsibility, a domain-tailored system prompt, a curated set of
  MCP tools, and (if relevant) its own retrieval corpus. Agents can be
  deployed and evolved independently — this is the main advantage over a
  monolithic single agent.
- **State plane (shared memory)** — three distinct data categories, each
  wanting a different store:
  - _Task state_ — durable tracking of requests/completions/remaining
    work (e.g. DynamoDB).
  - _Session context_ — short-lived conversation history and
    intermediate results (e.g. ElastiCache/Redis).
  - _Domain knowledge_ — read-only retrieval layer for facts/specs (e.g.
    a RAG knowledge base).
- **Capability plane (tools and MCP)** — MCP servers expose standardized,
  discoverable tool interfaces shared across the execution plane, so
  capability isn't duplicated per agent and updates propagate to every
  consumer.

### Routing patterns — how work actually gets dispatched

These are the mechanics underneath "supervisor/worker" and "network" above
— i.e., _how_ the orchestrator (or router) decides where a piece of work
goes:

| Routing pattern                  | Mechanics                                                                                                                             | Strength                                                                                                              | Weakness / risk                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Centralized orchestration**    | A lead agent decomposes the task and delegates to subagents while holding full task context throughout                                | Supports dynamic decisions and real-time adaptation (e.g. Amazon Bedrock Multi-Agent Collaboration's supervisor mode) | Orchestrator is a single point of failure and reasoning bottleneck  |
| **Skill-based dispatch**         | An agent picks from a fixed catalog of pre-built, parameterized "skills," each a well-defined operation executing a specific workflow | Excels with a stable, known set of operations                                                                         | Struggles with open-ended or improvised tasks outside the catalog   |
| **Handoff chains**               | Sequential agent-to-agent transfer — each agent processes the predecessor's output and passes enriched results forward                | Maps naturally onto pipeline architectures (e.g. AWS Step Functions state machines)                                   | Inflexible — can't easily branch based on intermediate results      |
| **Parallel fan-out & synthesis** | A router dispatches the _same_ task to multiple specialists simultaneously; a synthesizer collects and unifies their outputs          | Fast multi-domain evaluation (e.g. security + ops + cost review in parallel)                                          | Needs a real conflict-resolution strategy when specialists disagree |

Interview framing: pick the routing pattern from the _shape of the
decision_, not habit — "does the next step depend on this step's result?"
(handoff chain), "do I need N independent opinions on the same input?"
(fan-out/synthesis), "is this one of a small fixed set of known
operations?" (skill-based dispatch), "does one brain need to hold the
whole plan?" (centralized orchestration).

## 7. Frameworks (know the mental model, not every API)

- **LangGraph**: models the agent as a **state graph** — nodes are
  functions (often LLM calls or tool calls), edges define transitions,
  including **conditional edges** for branching logic. Ships built-in
  **checkpointing** (persist state at each node, resume later) and
  **human-in-the-loop** interrupts (pause graph execution for approval).
  Good mental model: an explicit, inspectable state machine instead of a
  hidden agent loop — this is why it fits production systems that need
  auditability.
- **CrewAI**: models agents as a **crew** of role-based agents (each with a
  role, goal, backstory) executing a set of **tasks**, with a **process**
  mode of `sequential` or `hierarchical` (manager agent delegates).
  Higher-level/opinionated than LangGraph — faster to prototype
  role-based workflows, less low-level control.
- **Google ADK (Agent Development Kit)**: Google's framework for building
  agents that deploy natively on Vertex AI; first-class support for
  multi-agent hierarchies, tool integration (including MCP), and
  evaluation. Relevant because it's the JD's named preferred framework and
  is Vertex-AI-native (tight fit with GCP deployment story).

Interview framing: you don't need to write LangGraph code from memory, but
you should be able to say _"I'd model this as a state graph with a router
node and two specialist nodes, checkpointed so it can resume after a human
approval step"_ — i.e., use the vocabulary correctly.

## 8. MCP — Model Context Protocol

MCP standardizes **how an agent host talks to a tool/data provider**, so
you don't write a bespoke integration per agent-framework × per-system
combination.

```
┌─────────────┐        MCP (JSON-RPC over        ┌──────────────┐
│  MCP Host    │        stdio / HTTP+SSE)          │  MCP Server   │
│ (agent /     │ ───────────────────────────────▶ │ (wraps a      │
│  orchestrator)│ ◀─────────────────────────────── │  system: DB,  │
└─────────────┘        tools / resources /          │  legacy API,  │
                        prompts exposed              │  file system) │
                                                      └──────────────┘
```

- **MCP server**: exposes **tools** (callable functions), **resources**
  (readable data, like RAG documents), and **prompts** (reusable prompt
  templates) from an underlying system.
- **MCP client/host**: the agent runtime that discovers and calls what the
  server exposes, without needing custom code per integration.
- **Why it matters for this role specifically**: the JD calls MCP servers
  out explicitly — this is exactly the "connective tissue between Google's
  AI products and customer's live infrastructure" pattern. Think of an
  MCP server as the standardized adapter you'd build once per customer
  legacy system (SAP, ServiceNow, an internal REST API) that any
  Vertex/ADK-based agent can then use, instead of one-off glue code.
- **Design implication**: MCP servers are a natural **unit of reuse** —
  build one per system, reuse across customer engagements — directly maps
  to the JD's "convert repeatable field patterns into reusable modules."

### Authentication & authorization in multi-agent MCP deployments

Single-agent MCP setups often get away with one static API key. That
breaks down the moment **multiple agents with different trust levels
share one MCP server** — which is the normal case in a supervisor/worker
system:

- **Multi-tenancy with agent-aware access control**: the server must know
  _which agent_ is calling, not just that _some_ authenticated caller is
  calling. Concretely: "the repository-analysis agent can call read-only
  GitHub tools but not write tools; the infrastructure-generation agent
  can write CDK templates to a staging S3 bucket but not deploy them."
- **Enforce at the server, not the prompt**: access control must live in
  the MCP server's authorization layer, never in the system prompt alone
  — "an agent should not do X" is not a security control, because
  prompt-based instructions "can be overridden by prompt injection or
  model reasoning errors." The server should reject the tool call
  outright regardless of what the model was told.
- **Least-privilege, scoped credentials per call**: don't hand every agent
  the orchestrator's full credentials. Issue short-lived, task-scoped
  credentials per delegation (e.g. via IAM Roles Anywhere / STS-style
  temporary tokens) so a compromised or misbehaving agent has a small
  blast radius.
- **Rate limits and parameter constraints are part of auth**: "which
  agents can call which tools, with what parameters, and subject to what
  rate limits" is the actual authorization surface — not just yes/no
  access. An MCP server that lets any agent call any tool with any
  parameters is a security liability, full stop.
- **Tool schema quality is a security property, not just UX**: precise
  parameter descriptions (acceptable values, consequences of misuse),
  consistent return structures including error cases, and informative
  error responses all help the _model_ make safe decisions — a vague
  schema increases the odds of a costly wrong call.
- **Lifecycle/versioning**: MCP servers evolve; a breaking schema or
  behavior change can silently corrupt every agent that calls that tool.
  Track MCP server versions explicitly in agent configs, and test against
  a new server version before promoting it to production (staged
  rollouts with evaluation gates, e.g. Amazon Bedrock AgentCore's
  approach).

## 9. A2A — Agent-to-Agent protocol

MCP standardizes agent → tool/data. **A2A standardizes agent → agent**
communication, and is a fundamentally different shape: **peer-to-peer,
not client-server**.

- **Task objects, not function calls**: the unit A2A passes between
  agents is a rich task object, not a thin RPC call — it carries the
  task description, prior work done by other agents, authorized
  resources, the expected output format/schema, and applicable
  constraints. Example: an orchestrator delegating a deployment step
  sends a task object containing "the service manifest produced by the
  analysis agent, the deployment target constraints approved by the user,
  the IaC pattern preference, and a structured output schema" — far more
  context than a bare function call could carry, which is why A2A fits
  delegation better than MCP does.
- **Agent cards (discoverability)**: agents publish a "card" at a known
  endpoint advertising what they accept (task types, input/output
  schemas), what they require (auth requirements, rate limits), and their
  processing constraints. This is what enables a **loosely coupled agent
  ecosystem** — a new agent built by a different team can be added to an
  orchestrated workflow "immediately, without changes to the
  orchestrator's code," because the orchestrator discovers its contract
  from the card instead of hardcoding it.
- **A2A security — an expanded attack surface**: because agents accept
  rich task objects from _other agents_ (not just from a trusted
  orchestrator calling a tool), a receiving agent must:
  - Validate the task object against its schema before processing it.
  - Apply content filtering to task descriptions and context fields (they
    may embed injected instructions).
  - Enforce its own access controls regardless of what the task object
    _claims_ the sender is authorized to do — never trust a claim of
    authorization carried inside the payload itself.
  - Guardrail layers (e.g. Amazon Bedrock Guardrails) can be applied at
    the agent boundary to filter both incoming task objects and outgoing
    responses.

**MCP vs A2A, one line each**: MCP = how an agent calls a tool/data
source. A2A = how one agent delegates rich, contextual work to another
agent as a peer. A supervisor/worker system typically uses both — MCP
inside each agent for its tools, A2A between the orchestrator and its
subagents (or between subagents in a network/swarm topology).

## 10. Memory & state management

- **Short-term/working memory**: the current conversation/context window —
  bounded by token limits, needs pruning/summarization for long sessions.
- **Long-term memory**: persisted across sessions, typically stored in a
  vector DB (semantic recall) or structured store (facts, preferences) and
  retrieved like RAG at the start of a new session.
- **Episodic memory**: record of past agent actions/trajectories — useful
  for learning from past runs or auditing.
- **Checkpointing**: persisting full agent/graph state at each step so
  execution can pause (human approval), crash-recover, or resume later —
  critical for long-running or human-in-the-loop workflows in production.
- **Session vs. global state**: separate what's scoped to one
  conversation/task vs. what should persist/be shared across users or
  sessions (e.g. a learned preference vs. a one-off fact).

## 11. Failure modes specific to agents

| Failure                          | Cause                                                            | Mitigation                                                                                                |
| -------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Infinite/runaway loop            | Agent keeps calling tools without converging                     | Max-iteration caps, loop detection, cost/step budgets                                                     |
| Wrong tool selected              | Ambiguous tool descriptions, too many similar tools              | Tighter tool descriptions, tool routing/grouping, fewer tools per agent                                   |
| Tool arg hallucination           | Model invents plausible-looking but wrong args                   | Strict JSON-schema validation, reject and re-prompt on invalid args                                       |
| Context window overflow          | Long tool outputs or long histories                              | Summarize tool outputs, truncate history, hierarchical memory                                             |
| Cost explosion                   | Unbounded multi-agent chatter or retries                         | Token/cost budgets per request, circuit breakers                                                          |
| Silent partial failure           | One sub-agent fails, orchestrator proceeds anyway                | Explicit error propagation, supervisor checks sub-agent status before aggregating                         |
| Prompt injection via tool output | Malicious content in retrieved doc/API response steers the agent | Treat tool output as untrusted data, not instructions; sanitize/sandbox; least-privilege tool permissions |

## 12. Failure modes specific to _multi_-agent systems

Splitting one agent into several doesn't just add the failures above per
agent — it introduces new failure classes at the _boundaries between_
agents. These are the ones worth naming explicitly in a design interview:

| Failure                                    | Cause                                                                                                                                | Mitigation                                                                                                                                                                                                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cascading failure                          | One agent's failure propagates downstream until the whole workflow collapses                                                         | Circuit breakers that detect repeated failures and route work away, so the system degrades instead of collapsing (e.g. Step Functions catch/retry); durable workflow engines (e.g. Temporal) resume from the failure point instead of re-running everything |
| Orchestration loop (runaway delegation)    | Validation fails → orchestrator asks for a revision → still fails → repeat, with unbounded cost                                      | Explicit loop detection with a max delegation count per task, forcing termination or human escalation; hard execution-time/step limits                                                                                                                      |
| Conflicting outputs from parallel agents   | Fan-out/synthesis specialists reach opposite conclusions (e.g. security says block, ops says ship)                                   | Domain-appropriate resolution policy decided up front — conservative bias (any concern surfaces) for safety-critical domains, relevance-weighting for operational ones                                                                                      |
| Context corruption at handoffs             | Malformed/truncated/semantically-inconsistent payload from a serialization bug or schema mismatch                                    | Schema validation at _every_ handoff boundary; return a structured error and halt rather than silently proceeding on corrupt data                                                                                                                           |
| Non-determinism propagation                | Per-agent error compounds across the pipeline — four agents at 90% accuracy each ≈ 66% end-to-end correctness                        | Individual agent quality must be well above the acceptable _system-level_ error rate; full end-to-end evaluation is non-optional, not a nice-to-have                                                                                                        |
| Low-confidence output passed downstream    | An uncertain agent still emits a confident-looking answer, and the next agent trusts it                                              | Structured/schema-validated outputs with a confidence score; agents should be able to **abstain** and escalate instead of guessing                                                                                                                          |
| Over-privileged sub-agents                 | A sub-agent is handed the orchestrator's full credentials "for convenience"                                                          | Least-privilege, time-limited, task-scoped credentials generated per delegation (e.g. IAM Roles Anywhere / STS), never the parent's full grant                                                                                                              |
| Prompt injection propagating across agents | Content from an external source (a repo, an upload, a third-party API) carries an injection that a later agent in the chain executes | Treat _all_ externally-originated content as untrusted from the moment it enters the system, not just at the first agent that touches it; filter/sanitize before it enters any handoff payload                                                              |

The through-line: **every agent boundary is also a trust boundary and a
validation boundary.** If you can't name what's validated/authorized at a
given handoff, that's the gap an interviewer will probe.

Also worth naming: **observability across agents is harder than within
one.** A single trace ID needs to propagate through every agent and tool
call so failures can be correlated across boundaries (distributed tracing
— e.g. CloudWatch/X-Ray-style trace graphs, or LangSmith's hierarchical
multi-agent trace view). Evaluate at three layers: per-agent (isolated),
full end-to-end workflow (does the _system_ succeed), and a differential
pass correlating per-agent scores with system-level outcomes — a
locally-good agent whose errors always show up in bad end-to-end runs is
a real finding, not noise. See file 03 for the full picture.

---

## Could you explain/draw this cold?

- [ ] Draw the ReAct loop and narrate a concrete example
- [ ] Explain the tradeoff of splitting one agent into multiple, with a
      concrete scenario where it's worth it and one where it isn't
- [ ] Explain the supervisor/worker pattern and why it's the most common
      enterprise choice
- [ ] Name the four planes of a multi-agent system (control, execution,
      state, capability) and what lives in each
- [ ] Pick the right routing pattern (centralized orchestration,
      skill-based dispatch, handoff chain, parallel fan-out/synthesis)
      for a given scenario and justify it
- [ ] Draw the MCP host/server relationship and explain why it beats
      bespoke per-integration glue code
- [ ] Explain why MCP access control must live in the server, not the
      system prompt, and give a concrete per-agent permission example
- [ ] Explain what A2A adds over MCP (task objects, agent cards) and when
      you'd reach for it
- [ ] Explain checkpointing and why it matters for human-in-the-loop
      workflows
- [ ] List 3 agent-specific failure modes and their mitigations
- [ ] List 3 multi-agent-specific (cross-boundary) failure modes and
      their mitigations, including the compounding-error-rate math
- [ ] Explain why tool output should be treated as untrusted input

--

## Further research
