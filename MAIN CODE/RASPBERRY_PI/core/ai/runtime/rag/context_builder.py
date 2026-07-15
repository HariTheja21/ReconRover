class ContextBuilder:
    def __init__(self, publish):
        self.publish = publish
        
    def build(self, session_id: str, retrieved_docs: list) -> str:
        context = "\n".join([doc.get("metadata", {}).get("text", "") for doc in retrieved_docs])
        self.publish("ContextBuilt", {
            "session_id": session_id,
            "context_length": len(context),
            "timestamp": 0.0
        })
        return f"Context:\n{context}"
