
import os
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
    return _model

def retrieval_agent(state):
    state.setdefault("rag_context", [])

    try:
        client = QdrantClient(url=os.getenv("QDRANT_URL", "http://qdrant:6333"))
        vector = get_model().encode(state["query"]).tolist()
        collection_name = os.getenv("QDRANT_COLLECTION", "airline_docs")
        if hasattr(client, "search"):
            results = client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=3,
            )
        else:
            response = client.query_points(
                collection_name=collection_name,
                query=vector,
                limit=3,
            )
            results = response.points
        state["rag_context"] = [r.payload.get("text", "") for r in results if r.payload]
    except Exception as exc:
        state["errors"] = [*state.get("errors", []), f"retrieval_agent: {exc}"]

    return state
