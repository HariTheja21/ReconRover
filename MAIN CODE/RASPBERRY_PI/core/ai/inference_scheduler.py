import asyncio
import time
import heapq
from typing import Dict, Any, Callable
from .ai_events import InferenceRequestEvent, InferenceResultEvent
from .ai_statistics import AIStatistics

class InferenceScheduler:
    def __init__(self, stats: AIStatistics, publish: Callable):
        self.stats = stats
        self.publish = publish
        # Priority queue for incoming requests
        self.queue = []
        self._counter = 0 # To resolve priority collisions
        
    async def schedule(self, request_id: str, model_id: str, priority: int, payload: Any):
        # Lower priority number = higher execution precedence (e.g., 0 is critical)
        heapq.heappush(self.queue, (priority, self._counter, request_id, model_id, payload))
        self._counter += 1
        
        self.stats.total_inferences_requested += 1
        self.publish("InferenceRequestEvent", InferenceRequestEvent(request_id, model_id, priority, time.time()))
        
    async def process_queue(self):
        # Stub for the worker loop that dequeues and executes models
        pass
        
    def complete_inference(self, request_id: str, model_id: str, success: bool, latency_ms: float):
        if success:
            self.stats.total_inferences_completed += 1
        else:
            self.stats.total_inferences_failed += 1
            
        # Update rolling average
        current_avg = self.stats.average_inference_latency_ms
        total = self.stats.total_inferences_completed + self.stats.total_inferences_failed
        if total > 0:
            self.stats.average_inference_latency_ms = current_avg + (latency_ms - current_avg) / total
            
        self.publish("InferenceResultEvent", InferenceResultEvent(request_id, model_id, "SUCCESS" if success else "ERROR", latency_ms, time.time()))
