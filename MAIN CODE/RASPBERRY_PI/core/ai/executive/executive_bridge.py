import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ExecutiveBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "executive.events"
            if event_type.startswith("Mission"):
                topic = "executive.mission"
            elif event_type == "ExecutiveDecisionGenerated":
                topic = "executive.decisions"
                
            payload = {"_executive_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Executive event {event_type}: {e}")
