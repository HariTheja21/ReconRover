import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ExplorationBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            # Map events to appropriate topics
            topic = "exploration.events"
            if event_type == "ExplorationMissionGenerated":
                topic = "exploration.missions"
            elif event_type == "CoverageUpdated":
                topic = "exploration.coverage"
                
            payload = {"_exploration_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Exploration event {event_type}: {e}")
