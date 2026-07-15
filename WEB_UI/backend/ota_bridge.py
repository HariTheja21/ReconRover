from typing import Callable
from .configuration_events import OTADeploymentEvent

class OTABridge:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback

    def broadcast_status(self, event: OTADeploymentEvent):
        """
        Publishes OTA status updates to the EventBus so that UI clients and internal logs
        can track deployment progress.
        """
        self.publish("OTADeploymentEvent", event)
