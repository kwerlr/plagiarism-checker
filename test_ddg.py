from duckduckgo_search import DDGS

def test_duckduckgo_search(query, max_results=5):
    with DDGS() as ddgs:
        results = []
        for result in ddgs.text(query, max_results=max_results):
            results.append(result)
        return results

if __name__ == "__main__":
    query = "test query"
    search_results = test_duckduckgo_search(query)
    
    print(f"Search results for query: '{query}'\n")
    for i, res in enumerate(search_results, 1):
        print(f"Result {i}:")
        print(f"Title: {res.get('title')}")
        print(f"URL: {res.get('href')}")
        print(f"Snippet: {res.get('body')}\n")
