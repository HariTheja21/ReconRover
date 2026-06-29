"""
audio_statistics.py
Recon Rover V1 - Audio Pipeline

Tracks long-term statistics for the audio pipeline.
"""

from dataclasses import dataclass
import time

@dataclass
class AudioStatsSnapshot:
    chunks_captured: int = 0
    chunks_processed: int = 0
    chunks_dropped: int = 0
    total_sounds_detected: int = 0
    processing_rate_hz: float = 0.0
    uptime_sec: float = 0.0

class AudioStatistics:
    def __init__(self):
        self._start_time = time.time()
        self._chunks_captured = 0
        self._chunks_processed = 0
        self._chunks_dropped = 0
        self._total_sounds_detected = 0

    def record_capture(self, latency_ms: float):
        self._chunks_captured += 1

    def record_processed(self):
        self._chunks_processed += 1

    def record_dropped_chunk(self):
        self._chunks_dropped += 1

    def record_detection(self, count: int):
        self._total_sounds_detected += count

    def get_snapshot(self) -> AudioStatsSnapshot:
        now = time.time()
        elapsed = max(now - self._start_time, 1.0)
        
        return AudioStatsSnapshot(
            chunks_captured=self._chunks_captured,
            chunks_processed=self._chunks_processed,
            chunks_dropped=self._chunks_dropped,
            total_sounds_detected=self._total_sounds_detected,
            processing_rate_hz=self._chunks_processed / elapsed,
            uptime_sec=elapsed
        )
