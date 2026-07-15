import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class LLMBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "llm.runtime"
            if event_type in ["LLMResponseReceived", "StreamingStarted", "StreamingCompleted"]:
                topic = "llm.inference"
            elif event_type in ["ProviderChanged", "ProviderHealthUpdated", "LLMStatisticsUpdated"]:
                topic = "llm.telemetry"
                
            payload = {"_llm_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish LLM event {event_type}: {e}")
