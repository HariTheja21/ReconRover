import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class VisionBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "vision.runtime"
            if event_type in ["ObjectDetectionUpdated", "SegmentationUpdated", "DepthMapUpdated"]:
                topic = "vision.perception"
            elif event_type in ["VisionPerformanceUpdated", "VisionStatisticsUpdated", "VisionHealthUpdated"]:
                topic = "vision.telemetry"
                
            payload = {"_vision_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Vision event {event_type}: {e}")
