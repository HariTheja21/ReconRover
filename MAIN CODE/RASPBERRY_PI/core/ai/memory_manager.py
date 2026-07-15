import logging
from typing import Dict

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, max_memory_mb: int = 4096):
        self.max_memory_mb = max_memory_mb
        self.allocated_memory_mb = 0
        self.allocations: Dict[str, int] = {} # model_id -> MB allocated

    def can_allocate(self, requested_mb: int) -> bool:
        return (self.allocated_memory_mb + requested_mb) <= self.max_memory_mb

    def allocate(self, model_id: str, requested_mb: int) -> bool:
        if self.can_allocate(requested_mb):
            self.allocations[model_id] = requested_mb
            self.allocated_memory_mb += requested_mb
            logger.debug(f"Allocated {requested_mb}MB for {model_id}. Total: {self.allocated_memory_mb}/{self.max_memory_mb}")
            return True
        logger.warning(f"Failed to allocate {requested_mb}MB for {model_id}. Not enough memory.")
        return False

    def free(self, model_id: str):
        if model_id in self.allocations:
            freed = self.allocations.pop(model_id)
            self.allocated_memory_mb -= freed
            logger.debug(f"Freed {freed}MB from {model_id}. Total: {self.allocated_memory_mb}/{self.max_memory_mb}")
