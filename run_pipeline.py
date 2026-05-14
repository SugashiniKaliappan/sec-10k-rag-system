import subprocess

steps = [
    "python3 src/parsing/parse_10k.py",
    "python3 src/parsing/extract_sections.py",
    "python3 src/chunking/chunk_sections.py",
    "python3 src/embeddings/create_vector_db.py",
]

for step in steps:
    print(f"\nRunning: {step}")
    result = subprocess.run(step, shell=True)

    if result.returncode != 0:
        print(f"Failed: {step}")
        break

print("\nPipeline completed.")
