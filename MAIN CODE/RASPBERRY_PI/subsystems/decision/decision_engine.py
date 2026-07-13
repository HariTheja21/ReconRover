"""
decision_engine.py
Recon Rover V1 - Decision Interpretation & Action Planning

Subscribes to LLMDecisionReady. Publishes DecisionPlanReady.
Does not control hardware directly.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, LLMDecisionReady, DecisionPlanReady, DecisionRejected,
    DecisionHealthUpdated, MissionUpdated, NavigationStateUpdated,
    WorldStateUpdated, HealthUpdated, BatteryUpdated, HazardDetected
)

from .decision_manager import DecisionManager

class DecisionEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = DecisionManager()
        
        self._subscribe_events()

    def _subscribe_events(self):
        # Trigger
        self.event_bus.subscribe(LLMDecisionReady, self._on_llm_decision)
        
        # Context Streams
        self.event_bus.subscribe(MissionUpdated, self._on_mission)
        self.event_bus.subscribe(NavigationStateUpdated, self._on_nav)
        self.event_bus.subscribe(WorldStateUpdated, self._on_world)
        self.event_bus.subscribe(HealthUpdated, self._on_health)
        self.event_bus.subscribe(BatteryUpdated, self._on_battery)
        self.event_bus.subscribe(HazardDetected, self._on_hazard)

    async def initialize(self):
        self.log.info("DecisionEngine (Phase 5.7) initialized.")

    async def start(self):
        self.log.info("DecisionEngine started.")

    async def stop(self):
        self.log.info("DecisionEngine stopped.")

    def health(self) -> str:
        return self.manager.health.status

    # --- Callbacks for Context ---
    async def _on_mission(self, event: MissionUpdated):
        self.manager.context.update_mission(event.status)

    async def _on_nav(self, event: NavigationStateUpdated):
        self.manager.context.update_nav(event.state)

    async def _on_world(self, event: WorldStateUpdated):
        self.manager.context.update_world(str(event.state))

    async def _on_health(self, event: HealthUpdated):
        self.manager.context.update_health(event.status)

    async def _on_battery(self, event: BatteryUpdated):
        self.manager.context.update_battery(event.level)

    async def _on_hazard(self, event: HazardDetected):
        self.manager.context.update_hazard(event.hazard_type)

    # --- Main Interpretation Trigger ---
    async def _on_llm_decision(self, event: LLMDecisionReady):
        """Triggered when the Local LLM outputs a raw decision intent."""
        
        plan = self.manager.build_plan_from_llm(
            movement=event.movement_intent,
            priority=event.priority,
            reasoning=event.reasoning_summary,
            mission_rec=event.mission_recommendation
        )
        
        if plan:
            # Publish the safe, verified plan for Phase 6 (Navigation Execution)
            self.event_bus.publish(DecisionPlanReady(
                plan_id=plan.plan_id,
                priority=plan.priority,
                immediate_action=plan.immediate_action,
                short_term_actions=plan.short_term_actions,
                long_term_goals=plan.long_term_goals
            ))
        else:
            self.event_bus.publish(DecisionRejected(reason="Invalid logic or impossible state transition."))
            
        # Update System Health
        self.event_bus.publish(DecisionHealthUpdated(status=self.manager.health.status))
