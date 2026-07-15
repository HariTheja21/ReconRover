class AudioBuffer:
    def __init__(self):
        self.buffer = []
        
    def add(self, chunk: bytes):
        self.buffer.append(chunk)
        
    def clear(self):
        self.buffer.clear()
        
    def get_audio(self) -> bytes:
        return b"".join(self.buffer)
