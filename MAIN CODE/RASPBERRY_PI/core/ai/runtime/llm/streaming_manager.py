class StreamingManager:
    def __init__(self, publish):
        self.publish = publish
        
    async def process_stream(self, provider_name: str, session_id: str, stream_generator):
        self.publish("StreamingStarted", {
            "provider": provider_name,
            "session_id": session_id,
            "timestamp": 0.0
        })
        
        full_text = ""
        async for chunk in stream_generator:
            full_text += chunk
            # Would publish partial chunks here in reality
            
        self.publish("StreamingCompleted", {
            "provider": provider_name,
            "session_id": session_id,
            "total_tokens": len(full_text.split()),
            "timestamp": 0.0
        })
        return full_text
