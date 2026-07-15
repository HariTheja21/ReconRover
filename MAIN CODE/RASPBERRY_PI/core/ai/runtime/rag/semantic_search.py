class SemanticSearch:
    def __init__(self, embedder, vdb):
        self.embedder = embedder
        self.vdb = vdb
        
    def search(self, query: str, top_k: int = 5) -> list:
        emb = self.embedder.get_embeddings(query)
        return self.vdb.search(emb, top_k)
