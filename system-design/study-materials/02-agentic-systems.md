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

Cost of splitting: more latency (extra LLM round-trips), more orchestration
complexity, harder to debug, more tokens burned on inter-agent
coordination. **This tradeoff is a strong interview signal** — don't
default to multi-agent just because it sounds sophisticated.

## 5. Multi-agent orchestration patterns

| Pattern | Shape | Use case |
|---|---|---|
| Sequential/pipeline | A → B → C, each hands off output to next | Well-defined multi-stage workflow (draft → review → format) |
| Supervisor/worker (hierarchical) | Orchestrator agent routes tasks to specialist sub-agents, aggregates results | Most common enterprise pattern — e.g. router decides "billing agent" vs "technical agent" |
| Network/swarm | Agents can hand off to each other directly, no fixed hierarchy | Flexible but harder to reason about/debug; higher risk of loops |
| Debate/critique | Two+ agents argue/critique to converge on a better answer | Higher-stakes reasoning tasks where single-pass quality isn't enough |

## 6. Frameworks (know the mental model, not every API)

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
you should be able to say *"I'd model this as a state graph with a router
node and two specialist nodes, checkpointed so it can resume after a human
approval step"* — i.e., use the vocabulary correctly.

## 7. MCP — Model Context Protocol

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

## 8. Memory & state management

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

## 9. Failure modes specific to agents

| Failure | Cause | Mitigation |
|---|---|---|
| Infinite/runaway loop | Agent keeps calling tools without converging | Max-iteration caps, loop detection, cost/step budgets |
| Wrong tool selected | Ambiguous tool descriptions, too many similar tools | Tighter tool descriptions, tool routing/grouping, fewer tools per agent |
| Tool arg hallucination | Model invents plausible-looking but wrong args | Strict JSON-schema validation, reject and re-prompt on invalid args |
| Context window overflow | Long tool outputs or long histories | Summarize tool outputs, truncate history, hierarchical memory |
| Cost explosion | Unbounded multi-agent chatter or retries | Token/cost budgets per request, circuit breakers |
| Silent partial failure | One sub-agent fails, orchestrator proceeds anyway | Explicit error propagation, supervisor checks sub-agent status before aggregating |
| Prompt injection via tool output | Malicious content in retrieved doc/API response steers the agent | Treat tool output as untrusted data, not instructions; sanitize/sandbox; least-privilege tool permissions |

---

## Could you explain/draw this cold?

- [ ] Draw the ReAct loop and narrate a concrete example
- [ ] Explain the tradeoff of splitting one agent into multiple, with a
      concrete scenario where it's worth it and one where it isn't
- [ ] Explain the supervisor/worker pattern and why it's the most common
      enterprise choice
- [ ] Draw the MCP host/server relationship and explain why it beats
      bespoke per-integration glue code
- [ ] Explain checkpointing and why it matters for human-in-the-loop
      workflows
- [ ] List 3 agent-specific failure modes and their mitigations
- [ ] Explain why tool output should be treated as untrusted input
