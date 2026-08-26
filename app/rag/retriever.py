from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# --------------------------------------------------
# Load Embedding Model
# --------------------------------------------------

print("Loading retriever model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# Connect to ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(VECTOR_STORE_DIR)
)

collection = client.get_collection(
    name="mental_health_knowledge"
)


# --------------------------------------------------
# Retrieve Relevant Context
# --------------------------------------------------

def retrieve_context(query, n_results=5):
    """
    Search the vector database and return the most
    relevant knowledge chunks.
    """

    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    contexts = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_items = []

    for context, metadata, distance in zip(
        contexts,
        metadatas,
        distances
    ):
        retrieved_items.append({
            "text": context,
            "source": metadata.get("source", "Unknown"),
            "distance": round(distance, 4)
        })

    return retrieved_items


# --------------------------------------------------
# Test Retriever
# --------------------------------------------------

if __name__ == "__main__":

    test_query = (
        "I feel very stressed because of exams "
        "and I cannot concentrate on my studies."
    )

    print("\nTest Query:")
    print(test_query)

    print("\nSearching knowledge base...\n")

    results = retrieve_context(
        test_query,
        n_results=5
    )

    for index, item in enumerate(results, start=1):

        print(f"Result {index}")
        print(f"Source: {item['source']}")
        print(f"Distance: {item['distance']}")
        print("Text:")
        print(item["text"])
        print("-" * 60)