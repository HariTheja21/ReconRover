from dataclasses import asdict
import json
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class AIBridge:
    def __init__(self, event_bus: Any): # Avoid circular dependency type-hinting
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_obj: Any):
        if not self.event_bus:
            return
            
        try:
            payload = asdict(event_obj)
            payload["_ai_event_type"] = event_type
            # Route all AI events to the telemetry topic for ground station sync
            self.event_bus.publish("telemetry.ai", json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish AI event {event_type}: {e}")
