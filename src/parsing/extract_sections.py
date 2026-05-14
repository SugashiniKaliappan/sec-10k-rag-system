from pathlib import Path
import re
import json

INPUT_FILE = Path(
    "/Users/sugashinikaliappan/sec-rag-project/data/processed/nvidia/2026/10-K/nvda-20260125_clean.txt"
)

OUTPUT_FILE = Path(
    "/Users/sugashinikaliappan/sec-rag-project/data/processed/nvidia/2026/10-K/nvda-20260125_sections.json"
)

SECTION_PATTERNS = {
    "item_1_business": r"Item\s+1\.\s+Business",

    "item_1a_risk_factors": r"Item\s+1A\.\s+Risk Factors",

    "item_1b_unresolved_comments":
        r"Item\s+1B\.\s+Unresolved Staff Comments",

    "item_1c_cybersecurity":
        r"Item\s+1C\.\s+Cybersecurity",

    "item_2_properties":
        r"Item\s+2\.\s+Properties",

    "item_3_legal_proceedings":
        r"Item\s+3\.\s+Legal Proceedings",

    "item_4_mine_safety":
        r"Item\s+4\.\s+Mine Safety",

    "item_5_market_information":
        r"Item\s+5\.\s+Market.*?Registrant",

    "item_6_reserved":
        r"Item\s+6\.\s+Reserved",

    "item_7_mda":
        r"Item\s+7\.\s+Management.*?Discussion.*?Analysis",

    "item_8_financial_statements":
        r"Item\s+8\.\s+Financial Statements"
}

# Skip early matches from Table of Contents
MIN_SECTION_START = 10000


def load_text(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def find_sections(text):
    matches = []

    for section_name, pattern in SECTION_PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):

            # Ignore Table of Contents matches
            if match.start() < MIN_SECTION_START:
                continue

            matches.append({
                "section": section_name,
                "start": match.start(),
                "matched_text": match.group()
            })

    matches = sorted(matches, key=lambda x: x["start"])
    return matches


def keep_first_match_per_section(matches):
    seen = set()
    filtered = []

    for match in matches:
        if match["section"] not in seen:
            filtered.append(match)
            seen.add(match["section"])

    return filtered


def extract_section_content(text, matches):
    sections = []

    for i, match in enumerate(matches):
        start = match["start"]

        end = (
            matches[i + 1]["start"]
            if i + 1 < len(matches)
            else len(text)
        )

        sections.append({
            "company": "NVIDIA",
            "filing_type": "10-K",
            "fiscal_year": 2026,
            "section": match["section"],
            "matched_text": match["matched_text"],
            "content": text[start:end].strip()
        })

    return sections


if __name__ == "__main__":

    text = load_text(INPUT_FILE)

    matches = find_sections(text)

    matches = keep_first_match_per_section(matches)

    print("\nFound REAL section matches:\n")

    for m in matches:
        print(
            f"{m['section']} | position={m['start']} | text={m['matched_text']}"
        )

    sections = extract_section_content(text, matches)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(sections, indent=2),
        encoding="utf-8"
    )

    print(f"\nSaved sections to:\n{OUTPUT_FILE}")

    print(f"\nTotal sections extracted: {len(sections)}")
