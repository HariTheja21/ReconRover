class RetrievalEngine:
    def __init__(self, optimizer, searcher, ranker, publish):
        self.optimizer = optimizer
        self.searcher = searcher
        self.ranker = ranker
        self.publish = publish
        
    def retrieve(self, raw_query: str, top_k: int = 5) -> list:
        query = self.optimizer.optimize(raw_query)
        raw_results = self.searcher.search(query, top_k * 2)
        final_results = self.ranker.process(query, raw_results)[:top_k]
        
        self.publish("RetrievalCompleted", {
            "query": raw_query,
            "num_results": len(final_results),
            "latency_ms": 50.0,
            "timestamp": 0.0
        })
        return final_results
