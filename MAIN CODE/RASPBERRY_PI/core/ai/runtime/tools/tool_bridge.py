import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class ToolBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "tools.runtime"
            if event_type in ["ToolExecutionStarted", "ToolExecutionCompleted", "ToolExecutionFailed", "ToolResultGenerated"]:
                topic = "tools.execution"
            elif event_type in ["ToolStatisticsUpdated", "ToolHealthUpdated"]:
                topic = "tools.telemetry"
                
            payload = {"_tool_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Tool event {event_type}: {e}")
