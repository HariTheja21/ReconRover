import asyncio
import numpy as np
from typing import Any
from .vision_manager import VisionManager

class VisionRuntime:
    """
    Top-level facade for the Vision AI Engine.
    Handles high-level model loading and frame ingestion API.
    """
    def __init__(self, event_bus: Any):
        self.manager = VisionManager(event_bus)
        
    async def initialize(self):
        await self.manager.start()
        
    def load_model(self, model_path: str, model_name: str) -> bool:
        success = self.manager.loader.load(model_path, model_name)
        self.manager.health.set_model_status(success)
        return success
        
    def unload_model(self):
        self.manager.loader.unload()
        self.manager.health.set_model_status(False)
        
    def set_allowed_classes(self, classes: list[str]):
        self.manager.det_filter.set_allowed_classes(classes)
        
    def set_confidence_threshold(self, threshold: float):
        self.manager.conf_filter.threshold = threshold
        
    async def process_frame(self, frame: np.ndarray, model_name: str):
        # Asynchronously push frame to scheduler queue
        await self.manager.scheduler.enqueue_frame(frame, model_name)
