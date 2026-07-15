import time
from typing import Callable
from .model_registry import ModelRegistry
from .memory_manager import MemoryManager
from .gpu_resource_manager import GPUResourceManager
from .ai_statistics import AIStatistics
from .ai_events import ModelLoadEvent

class ModelManager:
    def __init__(self, registry: ModelRegistry, memory: MemoryManager, gpu: GPUResourceManager, stats: AIStatistics, publish: Callable):
        self.registry = registry
        self.memory = memory
        self.gpu = gpu
        self.stats = stats
        self.publish = publish
        self.loaded_models = {}

    def load_model(self, model_id: str) -> bool:
        meta = self.registry.get_model_metadata(model_id)
        if not meta:
            return False
            
        req_mem = meta.get("required_memory_mb", 0)
        if not self.memory.allocate(model_id, req_mem):
            self._emit_event(model_id, meta.get("type", "unknown"), "FAILED")
            return False
            
        # GPU acquire logic if needed
        if meta.get("requires_gpu") and not self.gpu.acquire_device():
            self.memory.free(model_id)
            self._emit_event(model_id, meta.get("type", "unknown"), "FAILED")
            return False
            
        # Stub: Actually load the model instance here
        self.loaded_models[model_id] = {"status": "READY", "loaded_at": time.time()}
        self.stats.total_models_loaded += 1
        self._emit_event(model_id, meta.get("type", "unknown"), "READY")
        return True
        
    def unload_model(self, model_id: str):
        if model_id in self.loaded_models:
            # Stub: Actually free the model instance here
            meta = self.registry.get_model_metadata(model_id)
            if meta.get("requires_gpu"):
                self.gpu.release_device()
            self.memory.free(model_id)
            del self.loaded_models[model_id]
            self._emit_event(model_id, meta.get("type", "unknown"), "UNLOADED")

    def _emit_event(self, model_id: str, m_type: str, status: str):
        evt = ModelLoadEvent(model_id, m_type, status, time.time())
        self.publish("ModelLoadEvent", evt)
