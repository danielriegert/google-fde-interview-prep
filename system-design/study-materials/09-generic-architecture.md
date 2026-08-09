The agentic system architecture includes the following components:

    Frontend framework: A collection of prebuilt components, libraries, and tools that you use to build the user interface (UI) for your application.
    Agent development framework: The frameworks and libraries that you use to build and structure your agent's logic.
    Agent tools: The collection of tools, such as APIs, services, and functions, that fetch data and perform actions or transactions.
    Agent memory: The system that your agent uses to store and recall information.
    Agent design patterns: Common architectural approaches for structuring your agentic application.
    Agent runtime: The compute environment where your agent's application logic runs.
    AI models: The core reasoning engine that powers your agent's decision-making capabilities.
    Model runtime: The infrastructure that hosts and serves your AI model.

https://docs.cloud.google.com/architecture/choose-agentic-ai-architecture-components?hl=en

## Concrete example: single-agent AI system (ADK + Cloud Run)

Google's reference architecture for a single-agent system maps the generic
components above onto specific GCP services — useful as a worked example
to have ready in an interview instead of a menu of options.
(source: https://docs.cloud.google.com/architecture/single-agent-ai-system-adk-cloud-run)

### Architecture components → generic component

| Component in the doc | Generic component | Role |
|---|---|---|
| Frontend | Frontend framework | Chat-style UI — itself a serverless Cloud Run service |
| Agent | — | Receives requests, interprets intent, selects tools, synthesizes the answer |
| Agent runtime | Agent runtime | Built with ADK, deployed as a serverless **Cloud Run** service by default — or on **Agent Runtime** (Gemini Enterprise Agent Platform), or as a container on **GKE** |
| ADK | Agent development framework | Develops/tests/deploys the agent; exposes built-in tools (e.g. Google Search) so you're not hand-rolling them |
| AI model + model runtime | AI models / Model runtime | **Gemini**, served via **Gemini Enterprise Agent Platform** |
| MCP Toolbox | Agent tools | MCP Toolbox for Databases — database-specific tools with connection pooling/auth handled for you |
| MCP clients, servers, tools | Agent tools | MCP standardizes agent↔tool access — one client/server pair per tool (file system, API, Google Search, StackOverflow, ...) |
| Observability | — | Google Cloud Observability (Logging, Monitoring, Trace) |

### Agentic flow

1. User prompt enters via the frontend (Cloud Run).
2. Frontend forwards it to the agent.
3. Agent reasons over the prompt with the model: decides which tools to
   call, performs the tool calls and folds results into context, then
   grounds and validates before responding.

### Memory & session storage

Deliberately **not** in the base diagram — the doc calls this out as
something you add for a production deployment:

- **Session** = the conversational thread from first message to last.
  **State** = what the agent accumulates within that session (message
  history, tool-call results, working variables).
- Short-term: ADK `Session`/`state` objects, optionally backed by
  **Memorystore for Redis**.
- Long-term (cross-session, same user): **Memory Bank**.
- Reliability rationale for the same choice: to survive a Cloud Run
  instance recycling/restarting, decouple state from the runtime into an
  external store — Memory Bank, Memorystore for Redis, or a DB like Cloud
  SQL. A stateless agent process + external state store is what makes
  horizontal scaling and crash recovery work.

Matches file 02 §10's GCP mapping and file 05 §1 exactly — this doc is
where Google shows those choices wired into one concrete system.

### Products used

Cloud Run, Gemini, Gemini Enterprise Agent Platform, MCP, MCP Toolbox for
Databases, Google Cloud Observability (Logging/Monitoring/Trace).

### Design considerations worth knowing cold

- **Security** — least-privilege IAM per agent; human-in-the-loop for
  business-critical flows; disable the default `run.app` URL and front the
  frontend with a regional external HTTPS load balancer (+ Cloud Armor);
  IAP for internal users, Identity Platform/Firebase Auth for external
  users; Binary Authorization + Artifact Analysis for container
  supply-chain security; Model Armor to inspect prompts/responses for
  injection and sensitive-data leakage.
- **Reliability** — scale horizontally behind a load balancer (Cloud Run's
  instance autoscaling does this for you); decouple state from the
  runtime (Memory Bank/Memorystore/Cloud SQL) so a restart doesn't lose
  context; simulate failures before shipping to production.
- **Cost** — baseline QPS/TPS to decide if Provisioned Throughput is
  needed; start with the cheapest model that clears the quality bar and
  scale up only where needed; context caching for repeated high-token
  prompts; batch non-latency-sensitive requests.
- **Performance** — same model-selection and context-caching levers as
  cost; tune Cloud Run CPU/memory allocation to the workload.

### Use cases named in the doc

Bug-report triage, retail customer service, time-series forecasting, and
document retrieval (backed by **RAG Engine**) — each links to a runnable
ADK sample agent in the source doc.

## Concrete example: multi-agent AI system (ADK + Cloud Run, coordinator/subagent pattern)

Google's multi-agent counterpart to the single-agent architecture above —
same frontend/runtime/model backbone, but the "Agent" box becomes a
**Coordinator Agent** delegating to **subagents**, which is where the
multi-agent orchestration patterns from file 02 §5-§6 show up concretely.
(source: https://docs.cloud.google.com/architecture/multiagent-ai-system)

### Flow

1. Application user sends a prompt to the **Frontend** (Cloud Run service).
2. Frontend forwards it to the **Coordinator Agent** — the root agent,
   built with ADK, playing the orchestrator role from file 02's
   supervisor/worker (hierarchical) pattern: it holds task context and
   delegates, it doesn't do the work itself.
3. Coordinator invokes subagents. The diagram shows **two composition
   patterns side by side**, both valid within the same system:
   - **Sequence**: Task-A Subagent → Task-A.1 Subagent — the
     Sequential/pipeline pattern (file 02 §5), a straight hand-off chain.
   - **Iterative refinement**: Task-B Subagent produces a draft, a
     **Quality evaluator Subagent** checks it; if rework is required, a
     **Prompt enhancer Subagent** rewrites the prompt and feeds an
     "updated prompt" back into Task-B, looping until quality passes —
     an evaluator-optimizer/reflection loop, distinct from the
     Debate/critique row in file 02 §5 (one worker + one critic + one
     rewriter in a loop, not two peers arguing).
4. Both branches converge into a **Response Generator Subagent**.
5. The Response Generator returns its output to the Coordinator, which
   returns it to the Frontend, which returns it to the user. A separate
   **human-in-the-loop interaction** path lets a person intervene directly
   (file 02 §7 checkpointing / file 12 §5 human-in-the-loop guardrails),
   without necessarily routing back through the full agent chain.

### Inference path: Model Armor sits inline, not just at the edge

Every inference request from the coordinator/subagents to the AI model
(Gemini) is screened by **Model Armor** before it reaches the model, and
the response is screened again on the way back — i.e. Model Armor sits
**between the agent and the model on every call**, not only at the
frontend/user boundary. This is a sharper version of the guardrail
placement in file 12 §3/§9: in a multi-agent system, each agent's calls to
the model are a separate enforcement point, not just the one path a user's
request takes in and out.

### Runtime options (same three-way choice, twice)

- **Agents runtime** (where the coordinator + subagents execute): Cloud
  Run, Agent Runtime on Gemini Enterprise Agent Platform, or GKE.
- **Model runtime** (where the AI model itself is served): Gemini
  Enterprise Agent Platform, Cloud Run, or GKE.

These are independent choices — the agents and the model they call don't
have to share a runtime. Same options as file 05 §5's deployment table,
now shown as two separate decisions in one system rather than one.

### Tools: MCP clients, two tool pools

MCP clients (inside the Google Cloud boundary, alongside the agents) talk
to MCP servers exposing two distinct pools of tools — the capability plane
from file 02 §6, made concrete:

- **Tools within Google Cloud**: databases, APIs — reached via MCP servers
  running inside the same Google Cloud region as the agents.
- **External tools**: services, files outside Google Cloud — reached via
  MCP servers outside the Google Cloud boundary. Crossing this boundary is
  exactly the trust boundary called out in file 02 §12 and file 02a's MCP
  security guidance — external tool output should be treated as untrusted
  data, same as any other tool result.

### Other actors and components

- **AI developers** build the agents using **ADK**.
- **Platform administrators / DevOps engineers** operate the deployed
  system (distinct from AI developers — worth naming both personas in an
  interview when asked "who interacts with this system").
- **Google Cloud Observability**, fed from the agents runtime, same as the
  single-agent architecture above.

Net takeaway for an interview: this is the single-agent architecture with
the "Agent" box expanded into a coordinator + subagents, Model Armor
pushed onto every model call instead of just the edges, and MCP tool
access split into an internal pool and an external pool — everything else
(frontend, runtimes, observability) is unchanged from the single-agent
version.
