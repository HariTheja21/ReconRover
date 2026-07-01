"""
memory_engine.py
Recon Rover V1 - Persistent Memory

EventBus bridge for the memory subsystem.
Listens for significant events and autonomously writes them to the DB.
"""

import asyncio
from typing import Optional
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, MissionCompleted, ObjectiveCompleted, DecisionSelected,
    SceneUpdated, WorldStateUpdated, HazardDetected, BatteryCritical,
    MemoryCreated, MemoryUpdated, MemoryRetrieved, MemorySummarized,
    MemoryHealthUpdated
)

from .memory_manager import MemoryManager
from .memory_types import MemoryEntry

class MemoryEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = MemoryManager()
        
        self._running = False
        self._task = None
        self._subscribe_events()

    def _subscribe_events(self):
        self.event_bus.subscribe(ObjectiveCompleted, self._on_objective)
        self.event_bus.subscribe(DecisionSelected, self._on_decision)
        self.event_bus.subscribe(HazardDetected, self._on_hazard)
        self.event_bus.subscribe(BatteryCritical, self._on_battery_critical)

    async def initialize(self):
        await self.manager.initialize()
        self.log.info("MemoryEngine (Phase 5.2) initialized. DB loaded.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._maintenance_loop())
        self.log.info("MemoryEngine started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        await self.manager.db.close()
        self.log.info("MemoryEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Event Translators ---
    
    async def _on_hazard(self, event: HazardDetected):
        entry = MemoryEntry(
            category="SEMANTIC",
            importance=8.0,
            tags=["hazard", event.hazard_type],
            summary=f"Encountered hazard: {event.hazard_type}",
            source_module="Vision"
        )
        await self._write_and_publish(entry)

    async def _on_objective(self, event: ObjectiveCompleted):
        entry = MemoryEntry(
            category="EPISODIC",
            importance=5.0,
            tags=["objective", event.objective],
            summary=f"Successfully completed objective: {event.objective}",
            source_module="Autonomy"
        )
        await self._write_and_publish(entry)

    async def _on_battery_critical(self, event: BatteryCritical):
        entry = MemoryEntry(
            category="EPISODIC",
            importance=9.0,
            tags=["battery", "critical", "emergency"],
            summary=f"Battery critically low: {event.level}%",
            source_module="Hardware"
        )
        await self._write_and_publish(entry)
        
    async def _on_decision(self, event: DecisionSelected):
        if getattr(event, 'importance', 0.0) >= 7.0:
            entry = MemoryEntry(
                category="EPISODIC",
                importance=getattr(event, 'importance', 7.0),
                tags=["decision", getattr(event, 'action', 'unknown')],
                summary=f"Crucial decision made: {getattr(event, 'action', 'unknown')}",
                source_module="AI"
            )
            await self._write_and_publish(entry)

    async def _write_and_publish(self, entry: MemoryEntry):
        await self.manager.write_memory(entry)
        self.event_bus.publish(MemoryCreated(memory_id=entry.id))

    # --- Core Loop ---
    async def _maintenance_loop(self):
        """Periodically runs summarization and decay (e.g., every 5 minutes)."""
        while self._running:
            try:
                # 300 seconds = 5 minutes
                await asyncio.sleep(300.0)
                await self.manager.run_maintenance()
                self.event_bus.publish(MemoryHealthUpdated(status=self.manager.health.status))
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Memory maintenance loop exception: {e}")
                await asyncio.sleep(10.0)
