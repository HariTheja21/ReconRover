"""
llm_engine.py
Recon Rover V1 - Local LLM Decision Engine

The main EventBus orchestrator for Phase 5.6.
Listens exclusively to ContextReadyForLLM and publishes LLMDecisionReady.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, ContextReadyForLLM, LLMDecisionReady,
    LLMHealthUpdated, LLMInferenceCompleted,
    MissionUpdated, SystemHealthUpdated
)

from .llm_manager import LLMManager

class LLMEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.manager = LLMManager()
        self._is_inferencing = False
        
        self._subscribe_events()

    def _subscribe_events(self):
        # We NO LONGER listen to Vision/Audio/Nav individually.
        # Phase 5.5 Unified Multimodal Context is the ONLY trigger.
        self.event_bus.subscribe(ContextReadyForLLM, self._on_context_ready)
        
        # Global overrides/states
        self.event_bus.subscribe(MissionUpdated, self._on_mission)
        self.event_bus.subscribe(SystemHealthUpdated, self._on_health)

    async def initialize(self):
        # Discover models asynchronously during startup
        await self.manager.client.provider.initialize()
        self.log.info("LLMEngine (Phase 5.6) initialized.")

    async def start(self):
        self.log.info("LLMEngine started. Awaiting ContextReadyForLLM.")

    async def stop(self):
        self.log.info("LLMEngine stopped.")

    def health(self) -> str:
        if not self.manager.client.health.is_online:
            return "DEGRADED (Provider Offline)"
        return self.manager.health.status

    # --- Callbacks ---
    async def _on_mission(self, event: MissionUpdated):
        pass # Reserved for future override logic

    async def _on_health(self, event: SystemHealthUpdated):
        pass # Reserved for future override logic

    async def _on_context_ready(self, event: ContextReadyForLLM):
        """Triggered at 1Hz by Phase 5.5"""
        
        if self._is_inferencing:
            self.log.warning("LLM Inference in progress. Skipping 1Hz context tick.")
            return
            
        self._is_inferencing = True
        
        try:
            # 1. Execute Inference Pipeline
            response = await self.manager.execute_decision_cycle(event.prompt_block)
            
            # 2. Publish Telemetry
            self.event_bus.publish(LLMInferenceCompleted())
            self.event_bus.publish(LLMHealthUpdated(diagnostics=self.manager.health.get_diagnostics()))
            
            # 3. Publish Decisions (if parsed successfully)
            if response and response.is_valid_json:
                self.event_bus.publish(LLMDecisionReady(
                    movement_intent=response.movement_intent,
                    priority=response.priority,
                    reasoning_summary=response.reasoning_summary,
                    confidence=response.confidence,
                    mission_recommendation=response.mission_recommendation,
                    safety_assessment=response.safety_assessment
                ))
            else:
                self.log.warning("LLM Decision failed or produced invalid JSON.")
                
        finally:
            self._is_inferencing = False
