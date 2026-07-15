from typing import Callable
from .security_events import AuditEvent, AuthenticationEvent, AuthorizationEvent

class SecurityBridge:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback

    def broadcast_security_alert(self, event: AuditEvent):
        # Fire to EventBus so that UI dashboards can highlight critical security events
        self.publish("SecurityAlertEvent", event)
