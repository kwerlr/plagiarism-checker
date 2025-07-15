DeepDetect Pro
DeepDetect Pro is an AI-powered plagiarism checker for academic, professional, and personal documents. It uses semantic analysis and web search to detect both internal (within or across documents) and external (web) plagiarism. The tool supports multi-file uploads, highlights plagiarized sentences, and provides direct links to matched web sources for transparency and trust.

Features
Upload and check multiple .txt and .pdf files

Semantic plagiarism detection using sentence embeddings

Detect internal plagiarism across all uploaded files

Detect web plagiarism using DuckDuckGo web results

Match sentences to web snippets with clickable source links

Adjustable similarity threshold

Easy-to-use interface powered by Streamlit

How It Works
Uploaded files are split into individual sentences.

Each sentence is converted to an embedding using a SentenceTransformer model.

Internal plagiarism is checked by comparing all sentence pairs within and across the uploaded files.

Web plagiarism is checked by searching each sentence via DuckDuckGo, comparing the similarity, and providing the best match with a link to the source.

Installation
Clone this repository and install the required packages:

text
git clone https://github.com/kwerlr/plagiarism-checker.git
cd plagiarism-checker
pip install -r requirements.txt
For PDF support, install poppler-utils:

Windows: Use a pre-built binary (see official documentation)

macOS: brew install poppler

Linux: sudo apt install poppler-utils

Usage
To start the app locally:

text
streamlit run app.py
Then open your browser to http://localhost:8501.

Example Use Cases
Academic plagiarism detection

Journal or manuscript originality review

Business and publisher content screening

Reviewing student assignments and projects

Tech Stack
Frontend: Streamlit

Embedding model: SentenceTransformer (all-MiniLM-L6-v2)

PDF parsing: pdfplumber

Web search: duckduckgo_search

Project Structure
text
plagiarism-checker/
│
├── app.py
├── plagiarism.py
├── utils.py
├── requirements.txt
└── README.md

Author
Developed by Vagisha
