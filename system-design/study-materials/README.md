# GenAI Core Building Blocks — Study Materials

Deep-dive study guides for the concepts listed in section 3 of
`../system-design-prep-plan.md`. Each file is self-contained: read it,
then close it and try to redraw/re-explain the diagrams and tradeoffs
from memory.

| File | Covers |
|---|---|
| [01-rag.md](./01-rag.md) | Retrieval-Augmented Generation: chunking, embeddings, vector search, hybrid search, re-ranking, advanced RAG patterns, failure modes |
| [02-agentic-systems.md](./02-agentic-systems.md) | Agents, tool use, ReAct, multi-agent orchestration, LangGraph/CrewAI/ADK, MCP, memory & state |
| [03-evaluation-observability.md](./03-evaluation-observability.md) | Offline/online evals, LLM-as-judge, metrics, tracing, guardrails, regression testing |
| [04-integration-data-readiness.md](./04-integration-data-readiness.md) | Enterprise integration, auth/security perimeters, structured+unstructured data, ACL-aware retrieval |
| [05-gcp-vertex-ai.md](./05-gcp-vertex-ai.md) | Vertex AI platform, Gemini models, ADK, Vector Search, deployment options, cost/latency levers |

## How to use these

1. Read a file top to bottom once.
2. Cover it, and from memory: draw the main diagram, list the key
   tradeoffs, and explain 2 failure modes out loud.
3. Pick one prompt from the prep plan's prompt bank (section 4) that
   exercises this building block and sketch a design using it.
4. Come back after a few days and re-test recall — spaced repetition
   beats one long read.

Each file ends with a **"Could you explain/draw this cold?"** self-check
list — use it as your final pass before the interview.
