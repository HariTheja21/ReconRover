from typing import Callable
from .collaboration_events import ActivityFeedEvent, OperatorPresenceEvent, OwnershipTransferEvent

class CollaborationBridge:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback

    def broadcast_activity(self, event: ActivityFeedEvent):
        self.publish("ActivityFeedEvent", event)
