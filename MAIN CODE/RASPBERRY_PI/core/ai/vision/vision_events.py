from dataclasses import dataclass
from typing import List

@dataclass
class DetectionEvent:
    class_id: int
    class_name: str
    confidence: float
    bbox: List[int] # [x, y, w, h]
    tracking_id: int
    timestamp: float

@dataclass
class VisionInferenceEvent:
    model_name: str
    latency_ms: float
    num_detections: int
    timestamp: float

@dataclass
class VisionPipelineErrorEvent:
    component: str
    error_message: str
    timestamp: float
