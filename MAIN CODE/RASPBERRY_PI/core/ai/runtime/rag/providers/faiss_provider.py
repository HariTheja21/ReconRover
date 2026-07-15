from ..vector_database import VectorDatabase

class FAISSProvider(VectorDatabase):
    def __init__(self):
        super().__init__()
        self.index = None
        
    def add(self, embeddings: list, metadata: list, ids: list):
        # Stub FAISS
        pass
        
    def search(self, query_embedding: list, top_k: int = 5):
        # Stub FAISS
        return [{"id": "mock_id_2", "score": 0.90, "metadata": {"text": "mock document from FAISS"}}]
