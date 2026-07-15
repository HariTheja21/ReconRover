class KnowledgeRetriever:
    def __init__(self, engine, publish):
        self.engine = engine
        self.publish = publish
        
    def get_knowledge(self, topic: str) -> list:
        res = self.engine.retrieve(f"Knowledge about: {topic}")
        self.publish("KnowledgeRetrieved", {
            "topic": topic,
            "results": res,
            "timestamp": 0.0
        })
        return res
