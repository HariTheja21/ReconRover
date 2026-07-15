class Reranker:
    def __init__(self):
        pass
        
    def rerank(self, query: str, results: list) -> list:
        # Stub: Cross-encoder reranking
        return sorted(results, key=lambda x: x.get("score", 0), reverse=True)
