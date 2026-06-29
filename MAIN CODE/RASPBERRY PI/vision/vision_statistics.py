"""
vision_statistics.py
Recon Rover V1 - Vision Pipeline

Tracks long-term statistics for the vision pipeline.
"""

from dataclasses import dataclass
import time

@dataclass
class VisionStatsSnapshot:
    frames_captured: int = 0
    frames_processed: int = 0
    frames_dropped: int = 0
    total_detections: int = 0
    average_fps: float = 0.0
    uptime_sec: float = 0.0

class VisionStatistics:
    def __init__(self):
        self._start_time = time.time()
        self._frames_captured = 0
        self._frames_processed = 0
        self._frames_dropped = 0
        self._total_detections = 0

    def record_capture(self, latency_ms: float):
        self._frames_captured += 1

    def record_processed(self):
        self._frames_processed += 1

    def record_dropped_frame(self):
        self._frames_dropped += 1

    def record_detection(self, count: int):
        self._total_detections += count

    def get_snapshot(self) -> VisionStatsSnapshot:
        now = time.time()
        elapsed = max(now - self._start_time, 1.0)
        
        return VisionStatsSnapshot(
            frames_captured=self._frames_captured,
            frames_processed=self._frames_processed,
            frames_dropped=self._frames_dropped,
            total_detections=self._total_detections,
            average_fps=self._frames_captured / elapsed,
            uptime_sec=elapsed
        )
