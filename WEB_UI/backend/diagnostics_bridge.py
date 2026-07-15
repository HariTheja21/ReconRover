from typing import Callable
from .diagnostics_events import LogEvent, HealthStatusEvent, PerformanceMetricsEvent

class DiagnosticsBridge:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback

    # This class exists to cleanly route data TO the frontend over WebSockets
    def route_to_frontend(self, event_name: str, event_data: any):
        self.publish(event_name, event_data)
