"""
context_window.py
Recon Rover V1 - Unified Multimodal Context Builder

Manages rolling buffers of observations to bound memory and token usage.
"""

from typing import List
import time

class ContextWindow:
    def __init__(self, max_items: int = 5, max_age_seconds: float = 300.0):
        self.items: List[str] = []
        self.max_items = max_items
        self.max_age_seconds = max_age_seconds
        
    def add(self, item: str):
        if item not in self.items:
            self.items.append(item)
        if len(self.items) > self.max_items:
            self.items.pop(0)
            
    def get_all(self) -> str:
        return "\n".join(self.items)
        
    def clear(self):
        self.items.clear()
