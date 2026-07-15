from dataclasses import dataclass

@dataclass
class VisionStatistics:
    total_inferences: int = 0
    total_objects_detected: int = 0
    total_segmentations: int = 0
    total_depth_maps: int = 0
    avg_latency_ms: float = 0.0
