from sentence_transformers import SentenceTransformer, util
from duckduckgo_search import DDGS

# Load the pre-trained sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(sentences):
    """Compute embeddings for a list of sentences."""
    return model.encode(sentences, convert_to_tensor=True)

def compare_internal(embeddings_a, embeddings_b, threshold=0.8):
    """Compare two lists of embeddings and return sentence pairs with high similarity."""
    cosine_scores = util.cos_sim(embeddings_a, embeddings_b)
    matches = []
    for i in range(len(embeddings_a)):
        for j in range(len(embeddings_b)):
            score = cosine_scores[i][j].item()
            if i != j and score >= threshold:
                matches.append((i, j, score))
    return matches

def search_web_ddg(sentence, max_results=5):
    """Search DuckDuckGo for the sentence and return (snippet, url) tuples."""
    with DDGS() as ddgs:
        results = ddgs.text(sentence, max_results=max_results)
        snippets_and_urls = []
        for r in results:
            snippet = r.get("body")
            url = r.get("href")
            if isinstance(snippet, str) and isinstance(url, str):
                snippets_and_urls.append((snippet, url))
        # For debugging: print the snippets and URLs
        print(f"Web snippets for '{sentence}': {snippets_and_urls}")
        return snippets_and_urls

def compare_to_web(sentence, snippets_and_urls, threshold=0.8):
    """Compare a sentence to web snippets and return (max_score, index_of_max_score)."""
    if not snippets_and_urls:
        return 0.0, None
    snippets = [s for s, u in snippets_and_urls]
    sentence_embedding = get_embeddings([sentence])
    snippet_embeddings = get_embeddings(snippets)
    cosine_scores = util.cos_sim(sentence_embedding, snippet_embeddings)
    max_score = float(cosine_scores.max())
    max_idx = int(cosine_scores.argmax())
    return max_score, max_idx
