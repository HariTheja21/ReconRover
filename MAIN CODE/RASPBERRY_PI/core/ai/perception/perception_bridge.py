import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class PerceptionBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, topic: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            self.event_bus.publish(topic, json.dumps(event_dict))
        except Exception as e:
            logger.error(f"Failed to publish Perception event to {topic}: {e}")
