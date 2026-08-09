# GenAI Core Building Blocks — Study Materials

Deep-dive study guides for the concepts listed in section 3 of
`../system-design-prep-plan.md`. Each file is self-contained: read it,
then close it and try to redraw/re-explain the diagrams and tradeoffs
from memory.

| File | Covers |
|---|---|
| [01-rag.md](./01-rag.md) | Retrieval-Augmented Generation: chunking, embeddings, vector search, hybrid search, re-ranking, advanced RAG patterns, failure modes |
| [02-agentic-systems.md](./02-agentic-systems.md) | Agents, tool use, ReAct, multi-agent orchestration, LangGraph/CrewAI/ADK, A2A, memory & state |
| [02a-mcp.md](./02a-mcp.md) | Model Context Protocol: host/server model, tools/resources/prompts, when to use authorization, calling backend APIs safely (token passthrough, confused deputy), multi-agent auth, MCP vs A2A |
| [03-evaluation-observability.md](./03-evaluation-observability.md) | Offline/online evals, LLM-as-judge, metrics, tracing, guardrails, regression testing |
| [04-integration-data-readiness.md](./04-integration-data-readiness.md) | Enterprise integration, auth/security perimeters, structured+unstructured data, ACL-aware retrieval |
| [05-gcp-vertex-ai.md](./05-gcp-vertex-ai.md) | Vertex AI platform, Gemini models, ADK, RAG Engine/Vector Search, agent memory & state (Memory Bank, Memorystore, Firestore, Gemini Enterprise Agent Platform Sessions), deployment options (Agent Engine/Cloud Run/GKE/Endpoints/App Engine/Compute Engine), security (IAM/VPC-SC/scoped creds), monitoring (Logging/Trace/Monitoring/agent analytics), lifecycle/versioning, cost/latency levers |
| [06-llm-training-overview.md](./06-llm-training-overview.md) | Pretraining → SFT → alignment (RLHF/DPO) → serving, decoding params, KV cache, batching, LLM troubleshooting, FDE's role in a client's digital transformation |
| [07-fine-tuning.md](./07-fine-tuning.md) | Prompt vs RAG vs fine-tune decision framework, LoRA/QLoRA/PEFT, data requirements, Vertex AI tuning, risks (forgetting, staleness, maintenance) |
| [08-interview-structure-and-discovery.md](./08-interview-structure-and-discovery.md) | This interview's actual timing (15 min discovery/stakeholder alignment + 30 min deep-dive), choosing between the two named scenarios, stakeholder-alignment technique vs generic discovery, question banks per scenario |
| [09-generic-architecture.md](./09-generic-architecture.md) | Generic agentic system architecture components: frontend framework, agent dev framework, agent tools, agent memory, design patterns, agent runtime, AI models, model runtime; worked examples mapping these onto single-agent and multi-agent (coordinator/subagent, Model Armor inline) ADK + Cloud Run reference architectures |
| [10-prompt-engineering-techniques.md](./10-prompt-engineering-techniques.md) | Prompt structure types, zero/one/few-shot, CoT/self-consistency/tree-of-thoughts, meta prompting, prompt chaining/ReAct/Reflexion/PAL, prompt tuning vs. caching, prompt injection/jailbreaking, known limitations |

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
