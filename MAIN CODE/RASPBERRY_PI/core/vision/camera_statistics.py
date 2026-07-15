"""
Camera Statistics Module
Recon Rover V2 - Phase 2.7

Thread-safe telemetry tracking for vision pipeline metrics (FPS, drops).
"""

import threading
import time

class CameraStatistics:
    """Maintains counts and calculates FPS."""
    
    def __init__(self):
        self._lock = threading.RLock()
        self.total_frames = 0
        self.dropped_frames = 0
        self.current_fps = 0.0
        
        self._last_fps_time = time.time()
        self._frames_since_last_calc = 0
        
    def add_frame(self):
        with self._lock:
            self.total_frames += 1
            self._frames_since_last_calc += 1
            self._recalc_fps()
            
    def add_drop(self):
        with self._lock:
            self.dropped_frames += 1
            
    def _recalc_fps(self):
        now = time.time()
        dt = now - self._last_fps_time
        if dt >= 1.0:
            self.current_fps = self._frames_since_last_calc / dt
            self._frames_since_last_calc = 0
            self._last_fps_time = now

    def get_snapshot(self) -> dict:
        with self._lock:
            # Force recalc if it's been over a second to avoid stale FPS
            self._recalc_fps()
            return {
                "total_frames": self.total_frames,
                "dropped_frames": self.dropped_frames,
                "current_fps": round(self.current_fps, 2)
            }
