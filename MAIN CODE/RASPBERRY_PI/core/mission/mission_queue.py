"""
Mission Queue Module
Recon Rover V2 - Phase 3.9
"""
import threading
import heapq
from typing import List, Dict

class MissionQueue:
    """Thread-safe Priority Queue for Missions."""
    def __init__(self):
        self._lock = threading.RLock()
        self.queue = []
        self.counter = 0 # Tie breaker
        
    def push(self, mission: dict):
        with self._lock:
            # heapq is min-queue, so lower number = higher priority
            heapq.heappush(self.queue, (mission.get('priority', 10), self.counter, mission))
            self.counter += 1
            
    def pop(self) -> dict:
        with self._lock:
            if not self.queue:
                return None
            return heapq.heappop(self.queue)[2]
            
    def peek(self) -> dict:
        with self._lock:
            if not self.queue:
                return None
            return self.queue[0][2]
            
    def remove(self, mission_id: str) -> bool:
        with self._lock:
            new_queue = []
            removed = False
            for p, c, m in self.queue:
                if m.get('mission_id') == mission_id:
                    removed = True
                else:
                    new_queue.append((p, c, m))
            self.queue = new_queue
            heapq.heapify(self.queue)
            return removed
            
    def clear(self):
        with self._lock:
            self.queue.clear()
            self.counter = 0
