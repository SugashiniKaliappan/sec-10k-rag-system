

#RAW_FILE = Path("/Users/sugashinikaliappan/Downloads/0001045810-26-000021-xbrl/nvda-20260125.htm")

    
from bs4 import BeautifulSoup
from pathlib import Path

RAW_FILE = Path("/Users/sugashinikaliappan/sec-rag-project/data/raw/nvidia/2026/10-K/nvda-20260125.htm")
OUTPUT_FILE = Path("/Users/sugashinikaliappan/sec-rag-project/data/processed/nvidia/2026/10-K/nvda-20260125_clean.txt")

def load_html(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()

def parse_html(html):
    return BeautifulSoup(html, "lxml")

def clean_html(soup):
    for hidden in soup.find_all(style=lambda value: value and "display:none" in value.replace(" ", "")):
        hidden.decompose()

    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(" ", strip=True)

if __name__ == "__main__":
    html = load_html(RAW_FILE)
    soup = parse_html(html)
    clean_text = clean_html(soup)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(clean_text)

    print("Clean text saved successfully")
    print(f"Output file: {OUTPUT_FILE}")
    print(clean_text[:1000])
