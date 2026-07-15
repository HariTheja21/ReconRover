class RetrievalRanker:
    def __init__(self, reranker):
        self.reranker = reranker
        
    def process(self, query: str, results: list) -> list:
        return self.reranker.rerank(query, results)
