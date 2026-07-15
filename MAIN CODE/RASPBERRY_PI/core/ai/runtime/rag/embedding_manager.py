class EmbeddingManager:
    def __init__(self, provider):
        self.provider = provider
        
    def get_embeddings(self, text: str) -> list:
        return self.provider.embed(text)
