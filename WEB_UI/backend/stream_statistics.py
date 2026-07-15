from dataclasses import dataclass

@dataclass
class StreamStatistics:
    frames_encoded: int = 0
    frames_dropped: int = 0
    total_bytes_sent: int = 0
    active_viewers: int = 0
    current_fps: float = 0.0
    encoding_latency_ms: float = 0.0
