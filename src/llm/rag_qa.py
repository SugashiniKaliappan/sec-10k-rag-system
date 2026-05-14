import os
import chromadb
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_PATH = "/Users/sugashinikaliappan/sec-rag-project/vector_db"
COLLECTION_NAME = "nvidia_10k_2026"
TOP_K = 3

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def retrieve_chunks(query):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    db_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = db_client.get_collection(COLLECTION_NAME)

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    return results


def build_context(results):
    context_parts = []

    for idx, doc in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][idx]

        context_parts.append(
            f"""
Source {idx + 1}
Company: {metadata['company']}
Filing: {metadata['filing_type']}
Year: {metadata['fiscal_year']}
Section: {metadata['section']}

Text:
{doc}
"""
        )

    return "\n\n".join(context_parts)


def ask_llm(question, context):
    prompt = f"""
You are a financial filing assistant.

Answer the question using ONLY the SEC filing context below.
If the answer is not present in the context, say:
"I don't have enough information from the filing context."

Question:
{question}

Context:
{context}

Answer format:
1. Clear answer
2. Key points
3. Source sections
"""

    model = genai.GenerativeModel("gemini-flash-lite-latest")
    response = model.generate_content(prompt)

    return response.text


if __name__ == "__main__":
    question = "What cybersecurity risks does NVIDIA mention?"

    results = retrieve_chunks(question)
    context = build_context(results)
    answer = ask_llm(question, context)

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)
