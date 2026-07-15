import time
from typing import Callable, Dict, Any
from .diagnostics_events import PerformanceMetricsEvent

class PerformanceMonitor:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.latest_metrics: Dict[str, Any] = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "temperature": 0.0,
            "network_rx": 0,
            "network_tx": 0,
            "timestamp": 0.0
        }

    def process_metrics(self, event: PerformanceMetricsEvent):
        self.latest_metrics = {
            "cpu_usage": event.cpu_usage,
            "memory_usage": event.memory_usage,
            "temperature": event.temperature,
            "network_rx": event.network_rx,
            "network_tx": event.network_tx,
            "timestamp": event.timestamp
        }
        # Bridge to frontend
        self.publish("LivePerformanceEvent", event)

    def get_latest(self) -> Dict[str, Any]:
        return self.latest_metrics
