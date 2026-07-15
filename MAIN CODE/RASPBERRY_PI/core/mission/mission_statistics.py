"""
Mission Statistics Module
Recon Rover V2 - Phase 3.9
"""
import threading

class MissionStatistics:
    def __init__(self):
        self._lock = threading.RLock()
        self.missions_completed = 0
        self.missions_failed = 0
        self.tasks_completed = 0
        
    def increment_mission_completed(self):
        with self._lock:
            self.missions_completed += 1
            
    def increment_mission_failed(self):
        with self._lock:
            self.missions_failed += 1
            
    def increment_task_completed(self):
        with self._lock:
            self.tasks_completed += 1
