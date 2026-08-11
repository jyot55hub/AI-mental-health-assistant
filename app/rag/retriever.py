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
    Find relevant mental-health documents for a user query.

    Returns an empty list when the closest document is not
    relevant enough to the query.
    """

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    # Reject weak matches.
    RELEVANCE_THRESHOLD = 1.2

    relevant_documents = [
        document
        for document, distance in zip(documents, distances)
        if distance <= RELEVANCE_THRESHOLD
    ]

    return relevant_documents