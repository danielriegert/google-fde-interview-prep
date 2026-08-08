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
to have ready in an interview instead of a menu of options:

| Generic component | Concrete choice in this reference architecture |
|---|---|
| Agent development framework | Agent Development Kit (ADK) |
| Agent tools | MCP servers/toolsets (e.g. MCP Toolbox for Databases) — the agent reaches external data/APIs through MCP rather than hand-rolled tool code |
| Agent memory | Short-term: ADK `Session`/state, optionally backed by **Memorystore for Redis**; long-term (cross-session, same user): **Memory Bank** |
| Agent runtime | **Cloud Run** by default (scale-to-zero, low ops overhead) — or Agent Runtime on Gemini Enterprise Agent Platform, or GKE, for the same agent when more control/scale is needed |
| AI models | Gemini, or any model available via Model Garden |
| Model runtime | Vertex AI |
| Build/deploy | `adk deploy cloud_run` packages the agent, builds the container, pushes it to Artifact Registry, and deploys to Cloud Run in one step (Cloud Build backs the build) |
| Supporting services | Secret Manager (credentials/API keys), Cloud Storage (artifacts/files), and optionally Cloud SQL or RAG Engine when the agent needs structured data or RAG |

https://docs.cloud.google.com/architecture/single-agent-ai-system-adk-cloud-run?hl=en

Same services as file 05 §1/§5 and file 02 §10's GCP mapping — this is
those menus of options shown wired together as one concrete system.
