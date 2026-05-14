import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "/Users/sugashinikaliappan/sec-rag-project/vector_db"

COLLECTION_NAME = "nvidia_10k_2026"

TOP_K = 3


def search(query):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    return results


if __name__ == "__main__":

    query = "What cybersecurity risks does NVIDIA mention?"

    results = search(query)

    print("\nQUERY:\n")
    print(query)

    print("\nTOP RESULTS:\n")

    for idx, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][idx]

        print("=" * 80)

        print(f"SECTION: {metadata['section']}")

        print("\nTEXT:\n")

        print(document[:1200])
