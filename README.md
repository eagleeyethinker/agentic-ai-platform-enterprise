# Enterprise Agentic AI Platform

A compact reference implementation for an enterprise-style agentic AI workflow built with FastAPI, LangGraph, Qdrant, Neo4j, and an OpenAI-compatible reasoning layer.

## What It Does

The platform routes an incoming operational question through specialized agents:

- `router_agent` selects the branch to run
- `retrieval_agent` queries vectorized operational documents in Qdrant
- `tool_agent` calls the weather MCP service
- `graph_agent` queries Neo4j for graph context
- `reasoning_agent` produces the final recommendation

Current routing behavior:

- Weather and flight-impact queries go through the weather branch
- General policy and operations queries go through the RAG branch

## Stack

| Layer | Technology |
| --- | --- |
| API | FastAPI |
| Workflow orchestration | LangGraph |
| Reasoning | OpenAI-compatible chat completions |
| Vector store | Qdrant |
| Graph store | Neo4j |
| Embeddings | SentenceTransformers |
| Tool service | FastAPI weather MCP |
| Runtime | Docker Compose |

## Repository Layout

```text
agentic-ai-platform-enterprise/
├── agents/
├── api/
├── rag/
├── tools/
├── workflows/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Configuration

The repo now includes a root [`.env`](./.env) file. The main settings are:

```env
API_PORT=8000
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=all-MiniLM-L6-v2
QDRANT_COLLECTION=airline_docs
QDRANT_URL=http://qdrant:6333
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
WEATHER_MCP_URL=http://weather-mcp:9001
DEFAULT_AIRPORT=ATL
```

Notes:

- `OPENAI_API_KEY` is optional for local testing
- If no OpenAI key is set, the app returns a deterministic fallback recommendation
- `API_PORT` controls the host port exposed by Docker Compose

## Quick Start

1. Start the stack:

```bash
docker compose up --build -d
```

2. Ingest the sample RAG documents into Qdrant:

```bash
docker compose exec api python rag/ingest_docs.py
```

3. Query the API:

```text
http://localhost:8000/query?q=Storm expected in ATL at 17:00
```

If port `8000` is already in use, set `API_PORT` in [`.env`](./.env) before starting Compose.

## API Response Shape

`GET /query?q=...` returns a structured response:

```json
{
  "query": "Storm expected in ATL at 17:00",
  "route": "weather",
  "decision": "Monitor ATL operations due to high storm conditions.",
  "weather": {
    "airport": "ATL",
    "event": "Storm",
    "severity": "High"
  },
  "rag_context": null,
  "graph_data": [],
  "errors": []
}
```

For RAG-oriented queries, `route` will be `rag` and `rag_context` will contain retrieved document snippets.

## Local Behavior Notes

- The weather service is internal to Compose and is called through `WEATHER_MCP_URL`
- Qdrant and Neo4j are networked internally in Compose and do not need host port bindings for normal app usage
- Neo4j graph results are currently best-effort; if the sample database has no `Flight` nodes, the app still returns a response
- The reasoning layer records upstream failures in the `errors` field instead of silently masking them

## Example Queries

Weather route:

```text
/query?q=Storm expected in ATL at 17:00
```

RAG route:

```text
/query?q=What does the ops manual say about hub congestion?
```

## Development Notes

- The Dockerfile installs dependencies before copying the rest of the source to improve build caching
- `.gitignore` excludes Python bytecode, virtual environments, local env files, and common cache directories
- `.dockerignore` keeps the build context smaller by excluding cache and local development artifacts

## Author

Satish Gopinathan  
Website: https://www.eagleeyethinker.com

## License

MIT
