from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path(
    "/Users/sugashinikaliappan/sec-rag-project/data/chunks/nvidia/2026/10-K/nvda-20260125_chunks.json"
)

CHROMA_PATH = "/Users/sugashinikaliappan/sec-rag-project/vector_db"

COLLECTION_NAME = "nvidia_10k_2026"


def load_chunks(path):
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    chunks = load_chunks(CHUNKS_FILE)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk["text"]).tolist()

        collection.add(
            ids=[chunk["chunk_id"]],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{
                "company": chunk["company"],
                "filing_type": chunk["filing_type"],
                "fiscal_year": chunk["fiscal_year"],
                "section": chunk["section"]
            }]
        )

        if idx % 50 == 0:
            print(f"Inserted {idx} chunks")

    print("Vector DB created successfully")
    print(f"Total chunks inserted: {len(chunks)}")
