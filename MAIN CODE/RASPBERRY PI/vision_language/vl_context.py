"""
vl_context.py
Recon Rover V1 - Vision-Language Cognitive Integration

Maintains the working state for the Vision-Language engine.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class VLContext:
    latest_detections: List[Dict[str, Any]] = field(default_factory=list)
    world_state: Dict[str, Any] = field(default_factory=dict)
    hazard_state: str = "NONE"
    
    def clear_detections(self):
        self.latest_detections.clear()
