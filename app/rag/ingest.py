from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(VECTOR_STORE_DIR)
)

collection = client.get_or_create_collection(
    name="mental_health_knowledge"
)


# --------------------------------------------------
# Text Chunking
# --------------------------------------------------

def chunk_text(text, chunk_size=800, overlap=150):
    """
    Split text into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# --------------------------------------------------
# Read and Store Documents
# --------------------------------------------------

def ingest_documents():
    """
    Read all .txt files, create embeddings,
    and store them in ChromaDB.
    """

    files = list(DOCUMENTS_DIR.glob("*.txt"))

    if not files:
        print("No .txt files found in documents folder.")
        return

    print(f"Found {len(files)} documents.")

    documents = []
    ids = []
    metadatas = []

    for file_path in files:

        print(f"Processing: {file_path.name}")

        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            if not chunk.strip():
                continue

            documents.append(chunk)

            ids.append(
                f"{file_path.stem}_chunk_{index}"
            )

            metadatas.append({
                "source": file_path.name
            })

    print(f"Created {len(documents)} chunks.")

    if not documents:
        print("No content was available to ingest.")
        return

    print("Creating embeddings...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    print("Saving to ChromaDB...")

    # Clear old data so rerunning the script
    # does not create duplicate IDs.
    try:
        client.delete_collection(
            name="mental_health_knowledge"
        )
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name="mental_health_knowledge"
    )

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print("\nIngestion completed successfully!")
    print(f"Total chunks stored: {len(documents)}")


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    ingest_documents()