from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# Load the same embedding model used during ingestion
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to the existing ChromaDB
chroma_client = chromadb.PersistentClient(
    path=str(VECTOR_STORE_DIR)
)


# Load our collection
collection = chroma_client.get_collection(
    name="mental_health_documents"
)


def retrieve_documents(query: str, top_k: int = 3) -> list[str]:
    """
    Find the most relevant documents for a user query.
    """

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    return results["documents"][0]