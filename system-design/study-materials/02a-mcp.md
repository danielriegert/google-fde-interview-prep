# MCP — Model Context Protocol

Split out from [02-agentic-systems.md](./02-agentic-systems.md) since it's
dense enough (and the JD calls it out explicitly) to warrant its own pass.

## 1. What MCP standardizes

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

## 2. When should you use authorization?

_(source: [MCP docs — Understanding Authorization §"When Should You Use
Authorization?"](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization#when-should-you-use-authorization))_

Authorization is **optional** in the MCP spec, but the official guidance
is to turn it on whenever:

- The server accesses user-specific data (emails, documents, databases)
- You need to audit who performed which action
- The server grants access to APIs that require user consent
- You're building for enterprise environments with strict access controls
- You want per-user rate limiting or usage tracking

**Transport determines the mechanism, not just the decision.** For
**STDIO** servers (local, spawned as a child process), you don't need
the OAuth dance at all — the server can lean on environment-based
credentials or a third-party library's own credential store, because the
process already runs inside the user's trust boundary. **OAuth 2.1 is
for HTTP-based transports**, where the server is remote and the client
has no other way to prove the user authorized it.

## 3. The OAuth flow for MCP (HTTP transports)

**The core roles.** The MCP OAuth ecosystem operates via a conversation
between these parties:

- **Resource Owner (the user)**: the person granting the AI permission to
  access their accounts (e.g. Notion, GitHub, Google Drive).
- **MCP Client (the AI host)**: the application or LLM interface executing
  the requests (e.g. Claude Desktop).
- **MCP Server**: the backend API providing the specific tools, prompts, or
  data — and, from the MCP Client's point of view, the OAuth "Resource
  Server."
- **Authorization Server (identity provider)**: the engine that verifies
  credentials and handles token distribution (e.g. Auth0, Clerk, Stytch).
- **Resource Server (the underlying API)**: the system actually holding the
  data the MCP server wraps (e.g. Facebook's data servers) — distinct from
  the MCP Server whenever the MCP Server acts as a proxy in front of a
  separate backend.

```
[ MCP Client ] -------- 1. Discovery (/.well-known) --------> [ MCP Server ]
      |                                                             ^
      |--- 2. Dynamic Client Registration (DCR) ---> [ Authorization |
      |                                                    Server ]  |
      |<-- 3. Browser Login & Consent (PKCE Exchange) ---------------|
      |                                                              |
      +----------------- 4. Authenticated Request -------------------+
                          (Bearer Token in Header)
```

1. **Discovery**: the MCP Client requests a protected resource/tool from
   the MCP Server. If unauthenticated, the server responds `401
   Unauthorized`. The client then queries the server's metadata endpoint
   (`/.well-known/oauth-authorization-server`) to discover the auth
   endpoints.
2. **Registration**: if the client doesn't already have credentials for
   this server, it performs Dynamic Client Registration (DCR) — it
   introduces itself to the Authorization Server, provides its redirect
   URL, and receives a unique client ID.
3. **Authorization & consent**: the client generates a PKCE verifier and
   launches a browser for the user. The user logs into the identity
   provider and approves the requested scopes; the authorization server
   returns a temporary authorization code via the browser callback. The
   client exchanges that code (plus its PKCE verifier) for a short-lived
   access token (JWT) and a refresh token.
4. **Token exchange & API request**: the client retries the original
   request, attaching the access token as a Bearer token on the header of
   all subsequent tool/data calls.
5. **Downstream token exchange (server side)**: an MCP server should never
   act as a dumb proxy for a client token. Instead it uses OAuth 2.0 Token
   Exchange (RFC 8693) — it validates the incoming client token, then calls
   the Authorization Server's token exchange endpoint to swap it for a
   Downstream Access Token scoped to that single backend API call. This
   token embeds claims identifying both the initiating client and the
   executing proxy server.

**OAuth Client Credentials flow (service identities).** For autonomous,
machine-to-machine (M2M) operations, the human identity is replaced
entirely by a service account or workload identity:

```
[ Autonomous Client ] --- 1. POST /token (ID + Secret) ---> [ Authorization Server ]
        |                                                              |
        |<-------------- 2. Issues Signed JWT Token ------------------|
        |
        +--------------- 3. JSON-RPC (Bearer Token) -----------------> [ MCP Server ]
```

- **Pre-registration**: the autonomous agent client is registered directly
  with the Authorization Server as a confidential client, assigned a
  `client_id` and `client_secret` (or, better, an infrastructure-asserted
  cryptographic certificate).
- **Direct token fetching**: the client bypasses the browser entirely and
  sends a programmatic `POST` to the identity provider's `/token` endpoint
  with `grant_type=client_credentials` plus the required tool scopes.
- **No refresh tokens**: the client-credentials flow issues a short-lived
  access token only. When it expires, the client simply requests a fresh
  one using its stored credentials.
- **Tool call execution**: the agent attaches the M2M token to the MCP
  JSON-RPC payload like a standard user call; the MCP server treats the
  machine itself as the authorized principal.

## 5. Authentication & authorization in multi-agent MCP deployments

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

## 6. MCP vs A2A, one line each

MCP = how an agent calls a tool/data source. **A2A** = how one agent
delegates rich, contextual work to another agent as a peer — see
[02-agentic-systems.md §9](./02-agentic-systems.md#9-a2a--agent-to-agent-protocol)
for the full comparison. A supervisor/worker system typically uses both —
MCP inside each agent for its tools, A2A between the orchestrator and its
subagents (or between subagents in a network/swarm topology).

---

## Could you explain/draw this cold?

- [ ] Draw the MCP host/server relationship and explain why it beats
      bespoke per-integration glue code
- [ ] Name the three things an MCP server exposes (tools, resources,
      prompts)
- [ ] State when authorization is recommended for an MCP server, and why
      STDIO servers can skip the OAuth flow while remote/HTTP servers
      can't
- [ ] Explain "token passthrough" as an anti-pattern and why the spec
      forbids it
- [ ] Explain the confused-deputy attack on an MCP proxy server and its
      mitigation (per-client consent, checked before forwarding)
- [ ] Explain how an MCP server should authenticate to the internal/legacy
      API it wraps — terminate the client token, mint its own
      backend-scoped credential (service account / token exchange),
      never relay the original token
- [ ] Explain why MCP access control must live in the server, not the
      system prompt, and give a concrete per-agent permission example
- [ ] Explain why tool schema quality is a security property, not just UX
- [ ] Explain the MCP server versioning/lifecycle risk and its mitigation
- [ ] Give the one-line distinction between MCP and A2A

---

## Further research
