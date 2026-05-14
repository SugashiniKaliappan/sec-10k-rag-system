# SEC 10-K RAG System

An end-to-end Retrieval-Augmented Generation (RAG) pipeline for processing SEC 10-K filings, extracting structured financial sections, generating embeddings, and enabling AI-powered question answering using Gemini and FAISS.

---

# Project Overview

This project builds a production-style financial document intelligence pipeline using SEC filings.

The pipeline performs:

* SEC 10-K ingestion
* HTML parsing and cleaning
* Section extraction
* Document chunking
* Embedding generation
* Vector database creation
* Retrieval-Augmented QA
* Workflow orchestration

---

# Architecture

```text
SEC 10-K Filing
        ↓
HTML Parsing
        ↓
Section Extraction
        ↓
Chunking Pipeline
        ↓
Embedding Generation
        ↓
FAISS Vector Store
        ↓
Gemini RAG QA
```

---

# Tech Stack

## Languages

* Python 3.12

## AI / ML

* Gemini API
* Sentence Transformers
* FAISS

## Data Processing

* BeautifulSoup
* Regex
* JSON

## Orchestration

* Airflow
* Python orchestration pipeline

## Cloud (Planned)

* GCP Cloud Storage
* Cloud Composer
* Vertex AI

---

# Project Structure

```text
sec-rag-project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── chunks/
│
├── src/
│   ├── parsing/
│   ├── chunking/
│   ├── embeddings/
│   └── llm/
│
├── dags/
│
├── airflow/
│
├── vector_store/
│
├── run_pipeline.py
├── requirements.txt
└── README.md
```

---

# Pipeline Steps

## 1. Parse SEC Filing

```bash
python3 src/parsing/parse_10k.py
```

Cleans and extracts readable text from SEC filing HTML.

---

## 2. Extract Filing Sections

```bash
python3 src/parsing/extract_sections.py
```

Extracts sections such as:

* Item 1 Business
* Item 1A Risk Factors
* Item 1C Cybersecurity
* Item 7 MD&A
* Item 8 Financial Statements

---

## 3. Chunk Documents

```bash
python3 src/chunking/chunk_sections.py
```

Splits long financial text into embedding-friendly chunks.

---

## 4. Create Vector Database

```bash
python3 src/embeddings/create_vector_db.py
```

Generates embeddings and stores vectors in FAISS.

---

## 5. Run RAG QA

```bash
python3 src/llm/rag_qa.py
```

Example question:

```text
What cybersecurity risks does NVIDIA mention?
```

---

# Orchestration

## Local Orchestration

Run the entire pipeline:

```bash
python3 run_pipeline.py
```

This executes:

```text
parse → extract → chunk → embed
```

---

# Airflow Integration

Airflow DAG created for workflow orchestration:

```text
sec_10k_rag_pipeline
```

Tasks:

* parse_html
* extract_sections
* chunk_sections
* create_vector_db

---

# Environment Variables

Create `.env`

```env
GEMINI_API_KEY=your_key_here
HF_TOKEN=your_huggingface_token
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/SugashiniKaliappan/sec-10k-rag-system.git
cd sec-10k-rag-system
```


# Future Improvements

* Automated SEC EDGAR downloader
* Metadata-aware retrieval
* Cloud deployment on GCP
* Cloud Composer orchestration
* FastAPI backend
* Streamlit UI
* Vector DB migration
* Multi-company filing support

---

# Status

Current Status:

* End-to-end local pipeline completed
* RAG QA working successfully
* Airflow orchestration initialized
* GitHub integration completed

---

# Author

Sugashini Kaliappan
