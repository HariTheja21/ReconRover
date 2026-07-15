class HybridSearch:
    def __init__(self, semantic, keyword):
        self.semantic = semantic
        self.keyword = keyword
        
    def search(self, query: str, top_k: int = 5) -> list:
        # Stub: fuse BM25 with Vector Search
        return self.semantic.search(query, top_k)
