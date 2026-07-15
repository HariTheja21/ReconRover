from dataclasses import asdict
import json
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class VisionBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_obj: Any):
        if not self.event_bus:
            return
            
        try:
            payload = asdict(event_obj)
            payload["_vision_event_type"] = event_type
            
            # High-priority semantic detections go to autonomy stack
            if event_type == "DetectionEvent":
                self.event_bus.publish("vision.detections", json.dumps(payload))
            else:
                self.event_bus.publish("telemetry.vision", json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Vision event {event_type}: {e}")
