from dataclasses import dataclass
from typing import Any, List, Dict

@dataclass
class VisionInferenceCompleted:
    model_name: str
    inference_time_ms: float
    timestamp: float

@dataclass
class ObjectDetectionUpdated:
    detections: List[Dict[str, Any]]
    timestamp: float

@dataclass
class SegmentationUpdated:
    masks_info: str
    timestamp: float

@dataclass
class DepthMapUpdated:
    depth_info: str
    timestamp: float

@dataclass
class VisionPerformanceUpdated:
    fps: float
    memory_usage_mb: float
    timestamp: float

@dataclass
class VisionStatisticsUpdated:
    total_inferences: int
    avg_latency_ms: float
    timestamp: float

@dataclass
class VisionHealthUpdated:
    is_healthy: bool
    error_message: str
    timestamp: float
