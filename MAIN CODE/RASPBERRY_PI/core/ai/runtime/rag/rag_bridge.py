import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class RAGBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "rag.runtime"
            if event_type in ["RetrievalCompleted", "ContextBuilt", "KnowledgeRetrieved", "MemoryRetrieved"]:
                topic = "rag.inference"
            elif event_type in ["RAGStatisticsUpdated", "RAGHealthUpdated"]:
                topic = "rag.telemetry"
                
            payload = {"_rag_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish RAG event {event_type}: {e}")
