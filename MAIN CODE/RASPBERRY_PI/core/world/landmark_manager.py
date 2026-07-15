"""
Landmark Manager Module
Recon Rover V2 - Phase 3.1
"""
import threading
import time

class LandmarkManager:
    def __init__(self):
        self._lock = threading.RLock()
        self.landmarks = {}
        
    def add_landmark(self, landmark_id: str, semantic_class: str, confidence: float):
        with self._lock:
            self.landmarks[landmark_id] = {
                "class": semantic_class,
                "confidence": confidence,
                "timestamp": time.time()
            }
            
    def get_all(self):
        with self._lock:
            return self.landmarks.copy()
