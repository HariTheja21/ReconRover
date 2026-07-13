"""
object_classifier.py
Recon Rover V1 - Vision Pipeline

Abstract interface for fine-grained object classification.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ObjectClassifier(ABC):
    @abstractmethod
    def classify(self, frame_data: Any, detections: List[Dict]) -> List[Dict]:
        """
        Takes raw detections (e.g., generic 'object' bounding boxes)
        and classifies them into specific categories (e.g., 'Coffee Mug').
        """
        raise NotImplementedError("Subclasses must implement classify")

class MockClassifier(ObjectClassifier):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="Classifier")

    async def run_classification(self, frame_data: Any, detections: List[Dict]) -> List[Dict]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.classify, frame_data, detections)

    def classify(self, frame_data: Any, detections: List[Dict]) -> List[Dict]:
        # Mocking inference
        import time
        time.sleep(0.002)
        
        results = []
        for det in detections:
            det_copy = det.copy()
            # If the detector just said "object", the classifier refines it.
            if det_copy.get("label") == "mock_obstacle":
                det_copy["subclass"] = "box"
            results.append(det_copy)
        return results
