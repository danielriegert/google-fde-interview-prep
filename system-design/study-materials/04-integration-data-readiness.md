# Integration & Data Readiness

This is the "unglamorous but where FDEs earn their keep" building block —
the JD's "solving the integration complexities, data readiness issues, and
state-management issues that prevent AI from reaching enterprise-grade
maturity."

## 1. The core problem

A demo agent talks to clean, pre-loaded data. A production agent has to
talk to a customer's actual environment: legacy APIs with inconsistent
auth, data spread across a SQL warehouse + a document store + a ticketing
system, and a security team that needs to sign off before anything touches
production data. Most of the "system design" work in this role is bridging
that gap.

## 2. Integration patterns

- **Direct API integration**: agent (or an MCP server in front of it) calls
  a REST/SOAP/GraphQL API directly. Simplest when the API is modern and
  well-documented; often it isn't (legacy SOAP, undocumented internal
  APIs, rate-limited).
- **ETL/ELT pipeline**: pull data out of source systems on a schedule,
  transform, and land it somewhere the AI stack can use efficiently
  (a data warehouse for structured data, a vector index for
  unstructured). Needed when direct real-time API calls are too slow,
  too rate-limited, or the source system can't handle AI-driven query
  volume.
- **Change Data Capture (CDC) / event-driven**: source system emits events
  on change (e.g. via Pub/Sub) → pipeline incrementally updates the
  index/warehouse. Needed when freshness matters and full batch reload is
  too slow/expensive.
- **MCP server as the integration unit**: wrap a legacy system behind an
  MCP server once, exposing clean tools/resources — turns a bespoke
  one-off integration into a reusable asset (see file 02, section 7).

Decision framework: **read-heavy + can tolerate some staleness → ETL into
a warehouse/index. Needs real-time/write access → direct API via a tool.
Needs both → hybrid (cached/indexed for fast reads, direct API for
writes/real-time lookups).**

## 3. Structured + unstructured data, one architecture

Enterprise data is rarely all one shape. A realistic design has to combine:
- **Structured**: SQL warehouses (BigQuery, Snowflake), relational DBs —
  best queried via **text-to-SQL** (LLM generates a query) or a
  pre-built tool/API rather than embedding rows as text.
- **Unstructured**: PDFs, wikis, tickets, emails — best queried via RAG
  (chunk + embed + retrieve, file 01).
- **Semi-structured**: JSON/API responses, logs — often need
  normalization/flattening before either path fits well.

A common production shape: a **router** (see file 02) classifies the
incoming question and dispatches to the right retrieval path — "what's the
order status" → tool call to the order API; "what's our return policy" →
RAG over the policy docs; "how many orders shipped late last month" →
text-to-SQL over the warehouse.

**Text-to-SQL specifics**: give the model the schema (table/column names +
descriptions, not raw data), constrain it to read-only queries, validate/
sandbox-execute before returning results, and consider a fixed library of
parameterized queries for high-stakes or frequently-asked questions instead
of fully free-form SQL generation (much safer, more predictable).

## 4. Auth & security perimeters

- **OAuth2 / service accounts**: agent backend authenticates to customer
  APIs — prefer scoped service accounts with least-privilege roles over
  broad admin credentials.
- **IAM**: fine-grained roles on GCP resources (who/what can call Vertex
  endpoints, read from a bucket, query BigQuery).
- **VPC Service Controls (VPC-SC)**: create a security perimeter around
  GCP resources to prevent data exfiltration even if credentials leak —
  relevant when a customer requires data to never leave a defined network
  boundary.
- **Secrets management**: API keys/credentials for legacy systems belong in
  a secrets manager (Secret Manager), never hardcoded or logged — agent
  tool code fetches at runtime.
- **Network boundary**: on-prem/legacy systems often require a private
  connection (VPN, Interconnect, or a private MCP server deployed inside
  the customer's network) rather than public internet exposure.

## 5. Data governance & access control at retrieval time

The failure mode unique to RAG/agents: a single shared vector index can
leak data across users/departments if you don't enforce access control
*at retrieval time*, not just at the UI layer.

- **ACL-aware retrieval**: tag each chunk/document with permission
  metadata (owning team, sensitivity level, allowed roles/users) at
  ingestion time; filter retrieval results by the requesting user's
  permissions *before* they ever reach the prompt — never rely on the
  LLM to "choose not to use" data it shouldn't have seen.
- **PII handling**: classify and redact/mask PII during ingestion where
  possible; if PII must be retained for the use case, ensure downstream
  logging/tracing (file 03) doesn't leak it into eval datasets or logs
  without redaction.
- **Data residency/compliance**: some customers require data to stay in a
  specific region or never be sent to a third-party model provider —
  affects model choice, deployment region, and pipeline design.
- **Audit trail**: log who asked what and what data was retrieved to
  answer it — needed for compliance review and incident investigation.

## 6. Data readiness — before you can even build

Common blockers an FDE has to solve before the "fun" agent-building
starts:
- Data is siloed across systems with no unified schema/identifiers
- Documents are inconsistent formats (scanned PDFs needing OCR, wikis with
  broken structure)
- No existing API for a system — may need to stand up a thin
  wrapper/service first
- Stale or duplicate data across systems with no clear source of truth
- No labeled/golden data to build an eval set from — may need to
  bootstrap one from SME interviews or historical support tickets

## 7. Failure modes & mitigations

| Failure | Cause | Mitigation |
|---|---|---|
| Cross-user data leakage | No ACL enforcement at retrieval | Metadata-filtered retrieval, tested with adversarial "can user A see user B's data" cases |
| Broken integration under load | Direct API calls to a rate-limited legacy system | Caching layer, ETL into a faster store, backoff/queueing |
| Stale structured answers | Text-to-SQL against a replica lagging behind source | Freshness SLAs, monitoring replication lag |
| Credential sprawl | Ad hoc API keys per integration, no central management | Centralized secrets manager, scoped service accounts per MCP server/tool |
| Unsafe generated SQL | Free-form text-to-SQL with write access | Read-only DB roles, query validation/sandboxing, parameterized query library for critical paths |

---

## Could you explain/draw this cold?

- [ ] Explain the decision framework for ETL/index vs. direct API
      integration, with an example of each
- [ ] Draw a router architecture that dispatches between text-to-SQL, RAG,
      and a direct API tool based on query type
- [ ] Explain ACL-aware retrieval and why filtering must happen before the
      prompt, not after
- [ ] Explain the difference between IAM and VPC-SC and when you'd need
      the latter
- [ ] Walk through how you'd safely expose a legacy SOAP API to an agent
