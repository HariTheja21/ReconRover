from typing import Any, Dict, List
from dataclasses import dataclass

@dataclass
class VisionResults:
    detections: List[Dict[str, Any]] = None
    segmentations: Any = None
    depth_map: Any = None
    latency_ms: float = 0.0
