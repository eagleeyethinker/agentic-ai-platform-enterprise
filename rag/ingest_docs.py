
import os
import uuid
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

collection = "airline_docs"

def ingest():
    client.recreate_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    docs = Path(__file__).resolve().parent / "docs"

    for file in docs.glob("*.txt"):
        text = file.read_text(encoding="utf-8")
        vector = model.encode(text).tolist()

        client.upsert(
            collection_name=collection,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={"text": text},
                )
            ],
        )

if __name__ == "__main__":
    ingest()
