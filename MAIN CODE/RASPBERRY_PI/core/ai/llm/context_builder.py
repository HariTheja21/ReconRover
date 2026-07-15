class ContextBuilder:
    def __init__(self):
        self.system_prompt = "You are Recon Rover V2, an advanced autonomous agent."
        
    def build_context(self, memory_context: str, spatial_context: str) -> list:
        return [
            {"role": "system", "content": f"{self.system_prompt}\nMemory: {memory_context}\nSpatial: {spatial_context}"}
        ]
