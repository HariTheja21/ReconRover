from dataclasses import dataclass
from typing import Any

@dataclass
class FrameBroadcastEvent:
    frame_data: bytes
    timestamp: float
    width: int
    height: int
    format: str

@dataclass
class StreamQualityChangeEvent:
    client_id: str
    resolution: str
    quality: int
