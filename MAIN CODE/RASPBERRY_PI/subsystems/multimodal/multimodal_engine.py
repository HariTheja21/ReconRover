"""
multimodal_engine.py
Recon Rover V1 - Unified Multimodal Context Builder

The EventBus orchestrator. Subscribes to all cognitive and telemetry streams.
Runs the MultimodalManager on a fixed clock to prevent spamming the LLM.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, VisionLanguageContextUpdated, AudioLanguageContextUpdated,
    WorldStateUpdated, NavigationStateUpdated, MemoryRetrieved,
    SceneSummaryUpdated, HealthUpdated, BatteryUpdated, HazardDetected,
    MissionUpdated
)

from .multimodal_manager import MultimodalManager

class MultimodalEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = MultimodalManager(self.event_bus)
        
        self._running = False
        self._task = None
        self._subscribe_events()

    def _subscribe_events(self):
        # Vision & Audio
        self.event_bus.subscribe(VisionLanguageContextUpdated, self._on_vl)
        self.event_bus.subscribe(AudioLanguageContextUpdated, self._on_al)
        
        # Telemetry
        self.event_bus.subscribe(WorldStateUpdated, self._on_world)
        self.event_bus.subscribe(NavigationStateUpdated, self._on_nav)
        self.event_bus.subscribe(HealthUpdated, self._on_health)
        self.event_bus.subscribe(BatteryUpdated, self._on_battery)
        
        # High Priority
        self.event_bus.subscribe(HazardDetected, self._on_hazard)
        self.event_bus.subscribe(MissionUpdated, self._on_mission)
        self.event_bus.subscribe(MemoryRetrieved, self._on_memory)

    async def initialize(self):
        self.log.info("MultimodalEngine (Phase 5.5) initialized.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._context_loop())
        self.log.info("MultimodalEngine started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("MultimodalEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Callbacks ---
    async def _on_vl(self, event: VisionLanguageContextUpdated):
        self.manager.builder.merger.update_vision(event.semantics)

    async def _on_al(self, event: AudioLanguageContextUpdated):
        self.manager.builder.merger.update_audio(event.semantics)

    async def _on_world(self, event: WorldStateUpdated):
        self.manager.builder.merger.update_world(str(event.state))

    async def _on_nav(self, event: NavigationStateUpdated):
        self.manager.builder.merger.update_navigation(event.state)

    async def _on_health(self, event: HealthUpdated):
        self.manager.builder.merger.update_health(event.status)

    async def _on_battery(self, event: BatteryUpdated):
        self.manager.builder.merger.update_battery(f"{event.level}%")

    async def _on_hazard(self, event: HazardDetected):
        self.manager.builder.merger.update_hazard(event.hazard_type)

    async def _on_mission(self, event: MissionUpdated):
        self.manager.builder.merger.update_mission(event.status)

    async def _on_memory(self, event: MemoryRetrieved):
        self.manager.builder.merger.update_memory(str(event.query_tags))

    # --- Engine Loop ---
    async def _context_loop(self):
        """
        Runs at 1Hz. Merges all asynchronous streams and publishes ONE context block
        for the LLM, preventing the LLM from being spammed by 100 sensors per second.
        """
        while self._running:
            try:
                self.manager.process_and_publish()
                await asyncio.sleep(1.0)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Multimodal loop exception: {e}")
                await asyncio.sleep(1.0)
