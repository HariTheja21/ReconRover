"""
autonomy_engine.py
Recon Rover V1 - Autonomous Intelligence

The central orchestrator loop for the Phase 5.0 Autonomy layer.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, MissionUpdated, NavigationUpdated, WorldStateUpdated, 
    SceneUpdated, AudioSceneUpdated, HealthUpdated, LLMDecisionReady, 
    DecisionUpdated, ObjectiveFailed, AutonomyUpdated, AutonomyHealthUpdated,
    PlanningStarted, PlanningFinished, BatteryUpdated
)

from .autonomy_context import AutonomyContext
from .autonomy_manager import AutonomyManager

class AutonomyEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.context = AutonomyContext()
        self.manager = AutonomyManager(self.event_bus)
        
        self._running = False
        self._task = None
        self._subscribe_events()

    def _subscribe_events(self):
        # State updates
        self.event_bus.subscribe(MissionUpdated, self._on_mission)
        self.event_bus.subscribe(NavigationUpdated, self._on_nav)
        self.event_bus.subscribe(WorldStateUpdated, self._on_world)
        self.event_bus.subscribe(SceneUpdated, self._on_vision)
        self.event_bus.subscribe(AudioSceneUpdated, self._on_audio)
        self.event_bus.subscribe(HealthUpdated, self._on_health)
        self.event_bus.subscribe(BatteryUpdated, self._on_battery)
        
        # Subsystem intelligence inputs
        self.event_bus.subscribe(LLMDecisionReady, self._on_llm_decision)
        self.event_bus.subscribe(DecisionUpdated, self._on_ai_decision)
        
        # Feedback
        self.event_bus.subscribe(ObjectiveFailed, self._on_objective_failed)

    async def initialize(self):
        self.log.info("AutonomyEngine (Phase 5.0) initialized.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._autonomy_loop())
        self.log.info("AutonomyEngine started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("AutonomyEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Callbacks ---
    async def _on_mission(self, event: MissionUpdated):
        self.context.mission_state = event.state
        
    async def _on_nav(self, event: NavigationUpdated):
        self.context.navigation_state = event.state
        
    async def _on_world(self, event: WorldStateUpdated):
        self.context.world_state = event.state
        
    async def _on_vision(self, event: SceneUpdated):
        self.context.vision_state = event.semantics
        
    async def _on_audio(self, event: AudioSceneUpdated):
        self.context.audio_state = event.semantics
        
    async def _on_health(self, event: HealthUpdated):
        self.context.health_status = event.status
        
    async def _on_battery(self, event: BatteryUpdated):
        self.context.battery_critical = (event.level < 15.0)
        
    async def _on_llm_decision(self, event: LLMDecisionReady):
        if event.candidates:
            self.context.llm_decision = {"intent": event.candidates[0].intent}
            
    async def _on_ai_decision(self, event: DecisionUpdated):
        self.context.ai_decision = {"intent": event.intent}
        
    async def _on_objective_failed(self, event: ObjectiveFailed):
        self.manager.stats.record_failed()
        self.log.warning(f"Autonomy Objective Failed: {event.objective} ({event.reason})")

    # --- Core Loop ---
    async def _autonomy_loop(self):
        """Ticks at 1Hz to oversee macro-objectives."""
        while self._running:
            try:
                self.event_bus.publish(PlanningStarted())
                
                # Execute the manager pipeline
                self.manager.run_planning_cycle(self.context)
                
                self.event_bus.publish(PlanningFinished())
                self.event_bus.publish(AutonomyHealthUpdated(status=self.manager.health.status))
                
                # Slower cycle for macro-autonomy
                await asyncio.sleep(1.0) 
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"Autonomy loop exception: {e}")
                self.manager.health.record_failure()
                await asyncio.sleep(2.0)
