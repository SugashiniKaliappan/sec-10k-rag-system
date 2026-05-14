from pathlib import Path
import json

INPUT_FILE = Path(
    "/Users/sugashinikaliappan/sec-rag-project/data/processed/nvidia/2026/10-K/nvda-20260125_sections.json"
)

OUTPUT_FILE = Path(
    "/Users/sugashinikaliappan/sec-rag-project/data/chunks/nvidia/2026/10-K/nvda-20260125_chunks.json"
)

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def load_sections(path):
    return json.loads(path.read_text(encoding="utf-8"))


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def create_chunks(sections):
    all_chunks = []

    for section in sections:
        section_chunks = chunk_text(section["content"])

        for idx, chunk in enumerate(section_chunks, start=1):
            all_chunks.append({
                "company": section["company"],
                "filing_type": section["filing_type"],
                "fiscal_year": section["fiscal_year"],
                "section": section["section"],
                "chunk_id": f"{section['section']}_chunk_{idx}",
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    sections = load_sections(INPUT_FILE)
    chunks = create_chunks(sections)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(chunks, indent=2), encoding="utf-8")

    print(f"Total sections loaded: {len(sections)}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Chunks saved to: {OUTPUT_FILE}")
