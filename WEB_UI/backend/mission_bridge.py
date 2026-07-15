from typing import Callable
from .mission_events import MissionCreatedEvent, MissionExecutionRequestEvent

class MissionBridge:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback

    def route_to_eventbus(self, event_name: str, event_data: any):
        """
        Takes verified mission structures and injects them into the robot's EventBus.
        """
        self.publish(event_name, event_data)
