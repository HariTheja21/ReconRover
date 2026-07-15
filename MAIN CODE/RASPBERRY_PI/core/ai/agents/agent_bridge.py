import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class AgentBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "agents.events"
            if event_type in ["AgentTaskCreated", "AgentTaskCompleted"]:
                topic = "agents.tasks"
            elif event_type == "SharedContextUpdated":
                topic = "agents.context"
                
            payload = {"_agent_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Agent event {event_type}: {e}")
