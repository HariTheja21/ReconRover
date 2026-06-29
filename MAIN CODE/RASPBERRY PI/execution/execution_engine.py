"""
execution_engine.py
Recon Rover V1 - Action Execution Orchestrator

Subscribes to DecisionPlanReady. Drives the ExecutionManager loop.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, DecisionPlanReady, MissionUpdated, HazardDetected,
    BatteryUpdated, HealthUpdated, EmergencyStop,
    ExecutionStarted, ExecutionCompleted, ExecutionFailed, ExecutionCancelled,
    ExecutionHealthUpdated
)

from .execution_manager import ExecutionManager

class ExecutionEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = ExecutionManager(self.event_bus)
        
        self._running = False
        self._task = None
        
        self._subscribe_events()

    def _subscribe_events(self):
        # Trigger
        self.event_bus.subscribe(DecisionPlanReady, self._on_plan_ready)
        
        # Telemetry for Context Preemption
        self.event_bus.subscribe(MissionUpdated, self._on_mission)
        self.event_bus.subscribe(HazardDetected, self._on_hazard)
        self.event_bus.subscribe(BatteryUpdated, self._on_battery)
        
        # Absolute Overrides
        self.event_bus.subscribe(EmergencyStop, self._on_e_stop)
        
        # Feedback loop from hardware (Phase 6)
        self.event_bus.subscribe(ExecutionCompleted, self._on_exec_complete)
        self.event_bus.subscribe(ExecutionFailed, self._on_exec_failed)

    async def initialize(self):
        self.log.info("ExecutionEngine (Phase 5.8) initialized.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._execution_loop())
        self.log.info("ExecutionEngine started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("ExecutionEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Callbacks ---
    async def _on_mission(self, event: MissionUpdated):
        self.manager.context.mission_status = event.status

    async def _on_hazard(self, event: HazardDetected):
        self.manager.context.update_hazard(event.hazard_type)

    async def _on_battery(self, event: BatteryUpdated):
        self.manager.context.update_battery(event.level)

    async def _on_e_stop(self, event: EmergencyStop):
        """Immediately flushes the queue and sets the E-Stop flag."""
        self.log.warning("EMERGENCY STOP RECEIVED. Flushing execution queue.")
        self.manager.context.trigger_e_stop()
        self.manager.queue.flush()

    async def _on_plan_ready(self, event: DecisionPlanReady):
        """Adds a new cognitive plan to the priority queue."""
        self.manager.process_new_plan(
            event.plan_id,
            event.priority,
            event.immediate_action,
            event.short_term_actions,
            event.long_term_goals
        )

    async def _on_exec_complete(self, event: ExecutionCompleted):
        self.manager.monitor.mark_completed(event.plan_id)

    async def _on_exec_failed(self, event: ExecutionFailed):
        self.manager.monitor.mark_failed(event.plan_id)
        self.manager.health.record_failure()
        self.event_bus.publish(ExecutionHealthUpdated(status=self.manager.health.status))

    # --- Engine Loop ---
    async def _execution_loop(self):
        """
        Runs continuously, attempting to dispatch the highest priority plan.
        Runs at 10Hz to ensure minimal latency between decision and execution request.
        """
        while self._running:
            try:
                self.manager.tick()
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Execution loop exception: {e}")
                await asyncio.sleep(0.1)
