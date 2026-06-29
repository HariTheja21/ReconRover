"""
vl_statistics.py
Recon Rover V1 - Vision-Language Cognitive Integration

Tracks statistics regarding scene graph generation.
"""

class VLStatistics:
    def __init__(self):
        self.graphs_built = 0
        self.observations_published = 0
        self.memories_triggered = 0
        
    def record_graph(self):
        self.graphs_built += 1
        
    def record_observation(self):
        self.observations_published += 1
        
    def record_memory(self):
        self.memories_triggered += 1
