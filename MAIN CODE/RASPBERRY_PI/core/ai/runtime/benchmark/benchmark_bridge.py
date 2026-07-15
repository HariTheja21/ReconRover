import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class BenchmarkBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "benchmark.runtime"
            if event_type in ["BenchmarkCompleted", "PerformanceReportGenerated"]:
                topic = "benchmark.execution"
            elif event_type in ["LatencyStatisticsUpdated", "ThroughputStatisticsUpdated", "BenchmarkHealthUpdated"]:
                topic = "benchmark.telemetry"
                
            payload = {"_benchmark_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Benchmark event {event_type}: {e}")
