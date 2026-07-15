import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class RuntimeBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "runtime.events"
            if event_type == "RuntimeInitialized":
                topic = "runtime.system"
            elif event_type in ["ProviderLoaded", "ModelDownloaded"]:
                topic = "runtime.models"
            elif event_type in ["BenchmarkCompleted", "ResourceAlert"]:
                topic = "runtime.performance"
                
            payload = {"_runtime_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Runtime event {event_type}: {e}")
