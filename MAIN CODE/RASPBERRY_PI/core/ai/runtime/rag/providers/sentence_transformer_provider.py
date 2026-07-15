from ..embedding_provider import EmbeddingProvider

class SentenceTransformerProvider(EmbeddingProvider):
    def __init__(self):
        super().__init__()
        
    def embed(self, text: str) -> list:
        # Stub Sentence Transformers (e.g. all-MiniLM-L6-v2)
        return [0.1, 0.2, 0.3, 0.4] # Stub 384d vector
