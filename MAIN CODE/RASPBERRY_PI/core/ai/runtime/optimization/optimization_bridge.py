import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class OptimizationBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "optimization.runtime"
            if event_type in ["OptimizationApplied"]:
                topic = "optimization.execution"
            elif event_type in ["OptimizationStatisticsUpdated", "OptimizationHealthUpdated", "LatencyUpdated", "ThroughputUpdated"]:
                topic = "optimization.telemetry"
                
            payload = {"_optimization_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Optimization event {event_type}: {e}")
