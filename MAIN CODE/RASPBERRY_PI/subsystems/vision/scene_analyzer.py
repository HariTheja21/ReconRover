"""
scene_analyzer.py
Recon Rover V1 - Vision Pipeline

Maps raw detections into semantic EventBus events.
"""

from typing import List, Dict
from event_bus import (
    EventBus, ObjectDetected, SceneUpdated,
    PersonDetected, AnimalDetected, MarkerDetected, PathVisible, UnknownObjectDetected
)
import time

class SceneAnalyzer:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def analyze(self, detections: List[Dict]):
        """
        Translates raw detections into high level events.
        """
        now = int(time.time() * 1000)
        
        # Always publish the generic ObjectDetected events for logging/telemetry
        for det in detections:
            self.event_bus.publish(ObjectDetected(
                timestamp_ms=now,
                object_class=det["class"],
                confidence=det["confidence"],
                bbox=det["bbox"]
            ))
            
            # Semantic translation
            cls = det["class"].lower()
            if cls == "person":
                self.event_bus.publish(PersonDetected())
            elif cls in ["dog", "cat", "bird", "animal"]:
                self.event_bus.publish(AnimalDetected())
            elif cls == "marker" or cls == "aruco":
                self.event_bus.publish(MarkerDetected())
            elif cls == "path" or cls == "road":
                self.event_bus.publish(PathVisible())
            else:
                self.event_bus.publish(UnknownObjectDetected())
                
        # Publish a heartbeat scene update
        self.event_bus.publish(SceneUpdated(timestamp_ms=now, object_count=len(detections)))
