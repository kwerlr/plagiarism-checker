# DeepDetect Pro

**DeepDetect Pro** is an AI-powered plagiarism checker for academic, professional, and personal documents. It combines semantic analysis and live web search to detect both **internal plagiarism** (within or across uploaded files) and **external plagiarism** (from the web).

It supports multi-file uploads, highlights matched sentences, and provides links to matched web sources for clarity and verification.

---

## Features

- Upload and scan multiple `.txt` and `.pdf` files
- Semantic similarity detection using sentence embeddings
- Internal plagiarism detection across all uploaded content
- External plagiarism detection via DuckDuckGo web search
- Sentence-level match display with direct web source links
- Adjustable similarity threshold for precision tuning
- Clean, user-friendly interface powered by Streamlit

---

## How It Works

1. Uploaded files are split into individual sentences.
2. Each sentence is encoded using a SentenceTransformer model (`all-MiniLM-L6-v2`).
3. Internal similarity is computed across all sentence pairs.
4. For external checks:
   - Each sentence is queried on DuckDuckGo.
   - Snippets are extracted and compared semantically.
   - Matching snippets are shown with a similarity score and source link.

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/kwerlr/plagiarism-checker.git
cd plagiarism-checker
pip install -r requirements.txt


PDF Support
Install Poppler to enable .pdf reading:

Windows: Download from Poppler for Windows

macOS: brew install poppler

Linux: sudo apt install poppler-utils

Usage
To start the application:
streamlit run app.py
Then open your browser to: http://localhost:8501

Example Use Cases
Academic research and thesis plagiarism detection

Manuscript and journal originality screening

Business content duplication checks

Classroom assignment reviews and project evaluations

Tech Stack
Frontend: Streamlit

Embedding Model: SentenceTransformer (all-MiniLM-L6-v2)

PDF Parsing: pdfplumber

Web Search: duckduckgo_search (DuckDuckGo API)


Project Structureplagiarism-checker/
├── app.py             # Streamlit app interface
├── plagiarism.py      # Core logic: embedding + web check
├── utils.py           # File handling and sentence processing
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation

Author
Developed by Vagisha Sharma
