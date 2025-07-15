import spacy
import pdfplumber

nlp = spacy.load("en_core_web_sm")

def read_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception as e:
        print("⚠️ Error reading PDF:", e)
        return ""

def split_sentences(text):
    if not text or not isinstance(text, str):
        print("⚠️ Text is empty or invalid")
        return []
    try:
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    except Exception as e:
        print("⚠️ spaCy failed to process text:", e)
        return []
