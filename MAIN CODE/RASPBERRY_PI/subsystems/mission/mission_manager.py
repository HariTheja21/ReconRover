"""
mission_manager.py
Recon Rover V1 - Mission Manager

Executive controller for the Raspberry Pi.
"""

import asyncio
import time
from lifecycle_manager import BaseModule
from event_bus import (
    EventBus, MissionRequested, GoalReached, BatteryCritical,
    EmergencyStopRequested, ManualOverrideEnabled, ManualOverrideDisabled
)

from .mission_state import MissionStateMachine, MissionLifecycle
from .mission_context import MissionStore
from .mission_registry import MissionRegistry
from .mission_validator import MissionValidator
from .mission_scheduler import MissionScheduler
from .mission_executor import MissionExecutor
from .mission_health import MissionHealth
from .mission_statistics import MissionStatistics

class MissionManager(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        
        self.registry = MissionRegistry()
        self.store = MissionStore()
        self.state_machine = MissionStateMachine()
        self.health_tracker = MissionHealth()
        self.stats = MissionStatistics()
        
        self.validator = MissionValidator(self.registry, self.store, self.state_machine)
        self.scheduler = MissionScheduler(self.registry, self.store)
        self.executor = MissionExecutor(self.store, self.state_machine, self.event_bus)
        
        self._running = False
        self._task = None

    async def initialize(self):
        # Subscribe to trigger events
        self.event_bus.subscribe(MissionRequested, self._on_mission_requested)
        self.event_bus.subscribe(GoalReached, self._on_goal_reached)
        self.event_bus.subscribe(BatteryCritical, self._on_battery_critical)
        self.event_bus.subscribe(EmergencyStopRequested, self._on_emergency)
        self.event_bus.subscribe(ManualOverrideEnabled, self._on_manual_enabled)
        self.event_bus.subscribe(ManualOverrideDisabled, self._on_manual_disabled)
        self.log.info("MissionManager initialized.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._manager_loop())
        
        # Start Idle mission by default
        self._request_mission("Idle", "System")
        self.log.info("MissionManager started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("MissionManager stopped.")

    def health(self) -> str:
        if self.store.active_mission:
            return f"OK (Active: {self.store.active_mission.mission_type})"
        return "IDLE"

    # --- Event Handlers ---
    async def _on_mission_requested(self, event: MissionRequested):
        self._request_mission(event.mission_type, event.requested_by)

    async def _on_emergency(self, event: EmergencyStopRequested):
        self._request_mission("Emergency Stop", "Safety Subsystem")

    async def _on_battery_critical(self, event: BatteryCritical):
        self._request_mission("Return Home", "Power Subsystem")

    async def _on_manual_enabled(self, event: ManualOverrideEnabled):
        self._request_mission("Manual Override", "User")
        
    async def _on_manual_disabled(self, event: ManualOverrideDisabled):
        if self.store.active_mission and self.store.active_mission.mission_type == "Manual Override":
            self.executor.cancel_mission("Manual Override Released")
            self._request_mission("Idle", "System")

    async def _on_goal_reached(self, event: GoalReached):
        if self.store.active_mission and not self.store.active_mission.is_terminal:
            self.executor.complete_mission()
            self.stats.record_mission_completed()
            self._request_mission("Idle", "System")

    # --- Core Logic ---
    def _request_mission(self, mission_type: str, owner: str):
        start = time.perf_counter()
        
        if not self.validator.validate_request(mission_type):
            self.health_tracker.record_validation_failure()
            return

        new_mission = self.scheduler.evaluate_request(mission_type, owner)
        self.stats.record_scheduler_decision()
        
        if new_mission:
            self.health_tracker.record_ownership_change()
            self.stats.record_mission_start(new_mission.mission_type)
            self.executor.execute_new_mission(new_mission)
            
        latency = (time.perf_counter() - start) * 1000
        self.health_tracker.scheduler_latency_ms = latency

    # --- Manager Loop ---
    async def _manager_loop(self):
        """Periodically checks timeouts and maintains health stats."""
        while self._running:
            try:
                self.executor.check_timeouts()
                if self.store.active_mission and self.store.active_mission.state == MissionLifecycle.TIMED_OUT:
                    self.stats.record_timeout()
                    # Fallback to idle if timed out
                    self._request_mission("Idle", "System")
                    
                if self.store.active_mission:
                    self.health_tracker.current_mission = self.store.active_mission.mission_type
                    
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"MissionManager loop error: {e}")
                await asyncio.sleep(1.0)
