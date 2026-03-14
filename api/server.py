
from fastapi import FastAPI
from workflows.workflow import run_query

app = FastAPI(title="Enterprise Agentic AI Platform")

@app.get("/query")
def query(q: str):
    result = run_query(q)
    return {
        "query": q,
        "route": result.get("route"),
        "decision": result.get("decision"),
        "weather": result.get("weather"),
        "rag_context": result.get("rag_context"),
        "graph_data": result.get("graph_data"),
        "errors": result.get("errors", []),
    }
