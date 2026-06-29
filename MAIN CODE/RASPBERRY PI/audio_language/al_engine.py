"""
al_engine.py
Recon Rover V1 - Audio-Language Cognitive Integration

The EventBus orchestrator for the AL cognitive layer.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, SpeechRecognized, SoundDetected, WorldStateUpdated, HazardDetected
)

from .al_manager import ALManager

class ALEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = ALManager(self.event_bus)
        
        self._subscribe_events()

    def _subscribe_events(self):
        self.event_bus.subscribe(SpeechRecognized, self._on_speech)
        self.event_bus.subscribe(SoundDetected, self._on_sound)
        self.event_bus.subscribe(WorldStateUpdated, self._on_world_updated)
        self.event_bus.subscribe(HazardDetected, self._on_hazard_updated)

    async def initialize(self):
        self.log.info("ALEngine (Phase 5.4) initialized.")

    async def start(self):
        self.log.info("ALEngine started. Translating audio to language.")

    async def stop(self):
        self.log.info("ALEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Callbacks ---
    async def _on_speech(self, event: SpeechRecognized):
        self.manager.process_speech(event.semantics)

    async def _on_sound(self, event: SoundDetected):
        self.manager.process_sound(event.semantics)

    async def _on_world_updated(self, event: WorldStateUpdated):
        self.manager.context.world_state = event.state

    async def _on_hazard_updated(self, event: HazardDetected):
        self.manager.context.hazard_state = event.hazard_type
