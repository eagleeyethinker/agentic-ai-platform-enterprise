
# Enterprise Agentic AI Platform

A **production-style enterprise reference architecture** demonstrating how modern organizations build **Agentic AI decision systems**.

This platform shows how multiple AI capabilities can be combined:

• Multi-agent orchestration (LangGraph)  
• Retrieval-Augmented Generation (Qdrant vector database)  
• Knowledge Graph reasoning (Neo4j)  
• Tool integration using MCP servers  
• LLM reasoning (OpenAI-compatible models)  
• Observability-ready design (Langfuse hooks)  
• Containerized infrastructure (Docker)  

---

# Architecture

The platform coordinates multiple agents to answer operational questions.

Example:

> Storm expected in Atlanta at 17:00  
> Which flights should be delayed?

Agents collaborate to gather context and produce an operational decision.

Flow:

User → API → LangGraph Orchestrator → Agents → Decision

Agents:

• Router Agent  
• Retrieval Agent (Vector RAG)  
• Tool Agent (MCP APIs)  
• Graph Agent (Neo4j Knowledge Graph)  
• Reasoning Agent (LLM)

---

# Technology Stack

| Layer | Technology |
|------|-------------|
| API | FastAPI |
| Agent Orchestration | LangGraph |
| LLM Reasoning | OpenAI |
| Vector Database | Qdrant |
| Knowledge Graph | Neo4j |
| Embeddings | SentenceTransformers |
| Tool Layer | MCP servers |
| Containers | Docker |
| Dev Environment | Docker Compose |

---

# Repository Structure

```
agentic-ai-platform-v14
│
├── api
├── agents
├── workflows
├── rag
├── tools
├── observability
├── infra
│   ├── terraform
│   └── helm
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Quick Start

Start the environment:

```
docker compose up
```

Ingest example documents into the vector database:

```
python rag/ingest_docs.py
```

Query the API:

```
http://localhost:8000/query?q=Storm expected in ATL
```

---

# Example Output

```
Delay ATL departures between 17:00–18:30 due to severe thunderstorm activity.
Prioritize rerouting aircraft with international connections.
```

---

# Extending This Architecture

Enterprise teams can extend the platform by:

• Integrating airline operational APIs  
• Adding new MCP tool servers  
• Expanding the knowledge graph schema  
• Deploying to Kubernetes clusters  
• Adding CI/CD pipelines  

---

# Author

Satish Gopinathan  
Newsletter: **The Pragmatic Architect**  
Website: https://www.eagleeyethinker.com

---

# License

MIT License
