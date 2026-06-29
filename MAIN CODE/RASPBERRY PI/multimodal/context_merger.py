"""
context_merger.py
Recon Rover V1 - Unified Multimodal Context Builder

Safely overwrites or merges new subsystem events into the active context.
"""

from .multimodal_context import MultimodalContext

class ContextMerger:
    def __init__(self, context: MultimodalContext):
        self.context = context

    def update_vision(self, observation: str):
        self.context.vision.update(observation)

    def update_audio(self, observation: str):
        self.context.audio.update(observation)

    def update_world(self, state_str: str):
        self.context.world.update(state_str)

    def update_navigation(self, nav_str: str):
        self.context.navigation.update(nav_str)

    def update_memory(self, memory_str: str):
        # We append/merge recent memories rather than blind overwrite
        current = self.context.memory.content
        if current:
            # Simple deductive replacement for Phase 5.5
            self.context.memory.update(f"{current} | {memory_str}")
        else:
            self.context.memory.update(memory_str)

    def update_mission(self, mission_str: str):
        self.context.mission.update(mission_str)

    def update_health(self, health_str: str):
        self.context.health.update(health_str)

    def update_battery(self, battery_str: str):
        self.context.battery.update(battery_str)

    def update_hazard(self, hazard_str: str):
        self.context.hazard.update(hazard_str)
