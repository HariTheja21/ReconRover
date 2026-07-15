from dataclasses import dataclass

@dataclass
class VisionStatistics:
    frames_processed: int = 0
    frames_dropped: int = 0
    total_detections: int = 0
    avg_inference_latency_ms: float = 0.0
    avg_pipeline_latency_ms: float = 0.0
