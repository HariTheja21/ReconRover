"""
vision_health.py
Recon Rover V1 - Vision Pipeline

Tracks internal health metrics for the vision pipeline.
"""

from dataclasses import dataclass

@dataclass
class VisionHealthMetrics:
    camera_status: str = "DISCONNECTED"
    capture_latency_ms: float = 0.0
    processing_latency_ms: float = 0.0
    detection_latency_ms: float = 0.0
    buffer_utilization: float = 0.0

class VisionHealth:
    def __init__(self):
        self.metrics = VisionHealthMetrics()

    @property
    def camera_status(self) -> str:
        return self.metrics.camera_status
        
    @camera_status.setter
    def camera_status(self, value: str):
        self.metrics.camera_status = value

    @property
    def capture_latency_ms(self) -> float:
        return self.metrics.capture_latency_ms
        
    @capture_latency_ms.setter
    def capture_latency_ms(self, value: float):
        self.metrics.capture_latency_ms = value
        
    @property
    def processing_latency_ms(self) -> float:
        return self.metrics.processing_latency_ms
        
    @processing_latency_ms.setter
    def processing_latency_ms(self, value: float):
        self.metrics.processing_latency_ms = value

    @property
    def detection_latency_ms(self) -> float:
        return self.metrics.detection_latency_ms
        
    @detection_latency_ms.setter
    def detection_latency_ms(self, value: float):
        self.metrics.detection_latency_ms = value

    @property
    def buffer_utilization(self) -> float:
        return self.metrics.buffer_utilization
        
    @buffer_utilization.setter
    def buffer_utilization(self, value: float):
        self.metrics.buffer_utilization = value
