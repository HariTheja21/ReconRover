class ChunkManager:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def chunk(self, text: str) -> list:
        # Stub chunking
        return [text[i:i+self.chunk_size] for i in range(0, len(text), self.chunk_size - self.overlap)]
