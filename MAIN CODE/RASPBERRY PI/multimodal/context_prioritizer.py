"""
context_prioritizer.py
Recon Rover V1 - Unified Multimodal Context Builder

Sorts the context blocks. Highest priority elements (Hazards) go to the top.
"""

from .multimodal_context import MultimodalContext
from typing import List, Tuple

class ContextPrioritizer:
    def prioritize(self, context: MultimodalContext) -> List[Tuple[str, str]]:
        """
        Returns a sorted list of tuples: (Label, Content)
        Priority Order:
        1. Hazards
        2. Battery/Health
        3. Mission Goals
        4. Navigation State
        5. Vision
        6. Audio
        7. World Model
        8. Recalled Memories
        """
        blocks = []
        
        if context.hazard.content and context.hazard.content != "NONE":
            blocks.append(("HAZARD", context.hazard.content))
            
        if context.battery.content:
            blocks.append(("BATTERY", context.battery.content))
            
        if context.health.content:
            blocks.append(("HEALTH", context.health.content))
            
        if context.mission.content:
            blocks.append(("MISSION", context.mission.content))
            
        if context.navigation.content:
            blocks.append(("NAVIGATION", context.navigation.content))
            
        if context.vision.content:
            blocks.append(("VISION", context.vision.content))
            
        if context.audio.content:
            blocks.append(("AUDIO", context.audio.content))
            
        if context.world.content:
            blocks.append(("WORLD", context.world.content))
            
        if context.memory.content:
            blocks.append(("MEMORY", context.memory.content))
            
        return blocks
