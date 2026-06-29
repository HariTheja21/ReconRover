"""
context_statistics.py
Recon Rover V1 - Unified Multimodal Context Builder

Tracks statistics regarding context generation.
"""

class ContextStatistics:
    def __init__(self):
        self.contexts_built = 0
        
    def record_build(self):
        self.contexts_built += 1
