class VectorDatabase:
    def __init__(self):
        pass
        
    def add(self, embeddings: list, metadata: list, ids: list):
        raise NotImplementedError
        
    def search(self, query_embedding: list, top_k: int = 5):
        raise NotImplementedError
