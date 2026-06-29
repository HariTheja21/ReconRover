"""
dependency_graph.py
Recon Rover V1 - Full System Integration

Defines the absolute strict topological order for module initialization.
"""

from typing import List

class DependencyGraph:
    """
    Returns the ordered list of module names representing the required
    startup sequence.
    """
    @staticmethod
    def get_startup_sequence() -> List[str]:
        return [
            "EventBus",
            "HardwareInterface",
            "SensorFusion",
            "WorldModel",
            "NavigationEngine",
            "VisionLanguage",
            "AudioLanguage",
            "MemoryEngine",
            "MultimodalContext",
            "LocalLLM",
            "DecisionEngine",
            "ExecutionEngine",
            "Dashboard"
        ]
        
    @staticmethod
    def get_shutdown_sequence() -> List[str]:
        seq = DependencyGraph.get_startup_sequence()
        seq.reverse()
        return seq
