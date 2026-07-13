"""
vl_engine.py
Recon Rover V1 - Vision-Language Cognitive Integration

The EventBus orchestrator for the VL cognitive layer.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, SceneUpdated, WorldStateUpdated, HazardDetected
)

from .vl_manager import VLManager

class VLEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = VLManager(self.event_bus)
        
        self._subscribe_events()

    def _subscribe_events(self):
        # We only need the semantic dictionary list from Phase 4.3 Vision Pipeline
        self.event_bus.subscribe(SceneUpdated, self._on_scene_updated)
        self.event_bus.subscribe(WorldStateUpdated, self._on_world_updated)
        self.event_bus.subscribe(HazardDetected, self._on_hazard_updated)

    async def initialize(self):
        self.log.info("VLEngine (Phase 5.3) initialized.")

    async def start(self):
        self.log.info("VLEngine started. Translating vision to language.")

    async def stop(self):
        self.log.info("VLEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Callbacks ---
    async def _on_scene_updated(self, event: SceneUpdated):
        # This is where the magic happens. We intercept raw semantic vision 
        # and turn it into cognitive text.
        # Run in a small executor if the graph gets massive, but for a simple
        # dictionary iteration, async loop is fine.
        
        # Pass the semantic objects into the manager
        if "objects" in event.semantics:
            self.manager.process_detections(event.semantics["objects"])

    async def _on_world_updated(self, event: WorldStateUpdated):
        self.manager.context.world_state = event.state

    async def _on_hazard_updated(self, event: HazardDetected):
        self.manager.context.hazard_state = event.hazard_type
