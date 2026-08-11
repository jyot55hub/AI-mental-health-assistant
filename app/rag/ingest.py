from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Create ChromaDB client
chroma_client = chromadb.PersistentClient(
    path=str(VECTOR_STORE_DIR)
)


# Create or load our collection
collection = chroma_client.get_or_create_collection(
    name="mental_health_documents"
)


def ingest_documents():
    """Read text documents and store them in ChromaDB."""

    documents = []
    ids = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(text)
        ids.append(file_path.stem)

    if not documents:
        print("No documents found.")
        return

    embeddings = embedding_model.encode(documents).tolist()

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
    )

    print(f"Ingested {len(documents)} document(s).")
    print(f"Stored in: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    ingest_documents()