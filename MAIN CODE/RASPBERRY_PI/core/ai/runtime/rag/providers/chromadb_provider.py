from ..vector_database import VectorDatabase

class ChromaDBProvider(VectorDatabase):
    def __init__(self):
        super().__init__()
        self.collections = {}
        
    def add(self, embeddings: list, metadata: list, ids: list):
        # Stub ChromaDB
        pass
        
    def search(self, query_embedding: list, top_k: int = 5):
        # Stub ChromaDB
        return [{"id": "mock_id_1", "score": 0.95, "metadata": {"text": "mock document from ChromaDB"}}]
