class MemoryRetriever:
    def __init__(self, engine, publish):
        self.engine = engine
        self.publish = publish
        
    def get_memory(self, memory_query: str) -> list:
        res = self.engine.retrieve(f"Memory: {memory_query}")
        self.publish("MemoryRetrieved", {
            "memory_type": "episodic",
            "results": res,
            "timestamp": 0.0
        })
        return res
