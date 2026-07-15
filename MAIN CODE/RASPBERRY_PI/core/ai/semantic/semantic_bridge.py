import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class SemanticBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "semantic.events"
            if event_type == "SemanticMapUpdated":
                topic = "semantic.map"
            elif event_type == "RoomClassified":
                topic = "semantic.spatial"
                
            payload = {"_semantic_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Semantic event {event_type}: {e}")
