"""
object_tracker.py
Recon Rover V1 - Vision Pipeline

Assigns stable IDs to detected objects across consecutive frames.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ObjectTracker(ABC):
    @abstractmethod
    def track(self, detections: List[Dict], timestamp: float) -> List[Dict]:
        """
        Matches current detections against known tracks.
        Assigns UUIDs and expires lost tracks.
        """
        raise NotImplementedError("Subclasses must implement track")

class SimpleTracker(ObjectTracker):
    """A highly simplified, memory-bounded mock tracker."""
    def __init__(self, max_missing_time: float = 1.0):
        self.max_missing_time = max_missing_time
        self.tracks = {}
        self.next_id = 1
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="Tracker")

    async def run_tracking(self, detections: List[Dict], timestamp: float) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.track, detections, timestamp)

    def track(self, detections: List[Dict], timestamp: float) -> List[Dict]:
        # In a real system, this would use IOU (Intersection Over Union) or SORT.
        # For this mock, we just assign random IDs for demonstration.
        
        tracked_objects = []
        for det in detections:
            # Naive assignment
            track_id = f"trk_{self.next_id}"
            self.next_id += 1
            
            det_out = det.copy()
            det_out["track_id"] = track_id
            tracked_objects.append(det_out)
            
            self.tracks[track_id] = {"last_seen": timestamp, "data": det_out}
            
        # Expire stale tracks
        stale_ids = [tid for tid, track in self.tracks.items() if (timestamp - track["last_seen"]) > self.max_missing_time]
        for tid in stale_ids:
            del self.tracks[tid]
            
        return tracked_objects
