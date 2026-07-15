import asyncio
import numpy as np
from typing import Callable, Any
from .vision_pipeline import VisionPipeline
from .vision_events import VisionInferenceEvent, DetectionEvent

class InferenceWorker:
    def __init__(self, pipeline: VisionPipeline, stats: Any, publish: Callable):
        self.pipeline = pipeline
        self.stats = stats
        self.publish = publish
        
    async def execute(self, frame: np.ndarray, model_name: str):
        processed_frame, detections, latency = await self.pipeline.process_frame(frame)
        
        # Update Stats
        self.stats.frames_processed += 1
        self.stats.total_detections += len(detections)
        
        # Update running averages
        self.stats.avg_inference_latency_ms = (self.stats.avg_inference_latency_ms * 0.9) + (latency * 0.1)
        
        # Emit Inference Event
        self.publish("VisionInferenceEvent", VisionInferenceEvent(
            model_name, latency, len(detections), asyncio.get_event_loop().time()
        ))
        
        # Emit semantic events for each detection
        for det in detections:
            evt = DetectionEvent(
                det.get("class_id", -1),
                det.get("class_name", "unknown"),
                det.get("confidence", 0.0),
                det.get("bbox", [0,0,0,0]),
                det.get("tracking_id", -1),
                asyncio.get_event_loop().time()
            )
            self.publish("DetectionEvent", evt)
            
        return processed_frame, detections
