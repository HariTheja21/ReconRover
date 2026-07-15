"""
Mission Scheduler Module
Recon Rover V2 - Phase 3.9
"""
import threading
from typing import Any
from .mission_queue import MissionQueue

class MissionScheduler:
    """Pulls missions from the queue based on priority."""
    def __init__(self):
        self._lock = threading.RLock()
        self.queue = MissionQueue()
        self.active_mission = None
        
    def submit_mission(self, mission: dict):
        with self._lock:
            self.queue.push(mission)
            
    def get_next_mission(self) -> dict:
        with self._lock:
            return self.queue.pop()
            
    def set_active(self, mission: dict):
        with self._lock:
            self.active_mission = mission
            
    def clear_active(self):
        with self._lock:
            self.active_mission = None
            
    def cancel_mission(self, mission_id: str) -> bool:
        with self._lock:
            if self.active_mission and self.active_mission.get('mission_id') == mission_id:
                # Engine will handle aborting active
                return False
            return self.queue.remove(mission_id)
