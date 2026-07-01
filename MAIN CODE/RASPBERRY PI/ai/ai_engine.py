"""
ai_engine.py
Recon Rover V1 - AI Decision Engine

Central orchestrator for the deterministic cognitive reasoning layer (Phase 4.5).
"""

import asyncio
import time
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, SceneUpdated, AudioSceneUpdated, 
    NavigationStateChanged, MissionUpdated, WorldStateUpdated, HealthReceived, 
    BatteryCritical, ObstacleAppeared, ObstacleCleared, HazardDetected, HazardCleared
)

from .ai_context import AIContext
from .ai_memory import AIMemory
from .ai_blackboard import AIBlackboard
from .reasoning_engine import ReasoningEngine
from .rule_engine import RuleEngine
from .decision_engine import DecisionEngine
from .objective_manager import ObjectiveManager
from .action_selector import ActionSelector
from .ai_health import AIHealth
from .ai_statistics import AIStatistics

class AIEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        
        # State & Memory
        self.context = AIContext()
        self.memory = AIMemory(expiry_seconds=5.0)
        self.objective_manager = ObjectiveManager()
        
        # Reasoning Pipeline
        self.reasoning = ReasoningEngine()
        self.rules = RuleEngine()
        self.decision = DecisionEngine()
        self.action_selector = ActionSelector(self.event_bus)
        
        # Diagnostics
        self.health_tracker = AIHealth()
        self.stats = AIStatistics()
        
        self._running = False
        self._task = None
        
        self._subscribe_events()

    def _subscribe_events(self):
        # Perception
        self.event_bus.subscribe(SceneUpdated, self._on_scene_updated)
        self.event_bus.subscribe(AudioSceneUpdated, self._on_audio_updated)
        
        # State
        self.event_bus.subscribe(NavigationStateChanged, self._on_nav_updated)
        self.event_bus.subscribe(WorldStateUpdated, self._on_world_state_updated)
        
        # Health & Triggers
        self.event_bus.subscribe(HealthReceived, self._on_health_updated)
        self.event_bus.subscribe(BatteryCritical, self._on_battery_critical)
        
        # Obstacles & Hazards
        self.event_bus.subscribe(ObstacleAppeared, self._on_obstacle_appeared)
        self.event_bus.subscribe(ObstacleCleared, self._on_obstacle_cleared)
        self.event_bus.subscribe(HazardDetected, self._on_hazard_detected)
        self.event_bus.subscribe(HazardCleared, self._on_hazard_cleared)
        
    async def initialize(self):
        self.log.info("AIEngine (Phase 4.5) initialized.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._reasoning_loop())
        self.log.info("AIEngine started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("AIEngine stopped.")

    def health(self) -> str:
        return "OK"

    # --- Event Handlers (Update Context) ---
    async def _on_scene_updated(self, event: SceneUpdated):
        self.context.update_vision(event.semantics)
        
    async def _on_audio_updated(self, event: AudioSceneUpdated):
        self.context.update_audio(event.semantics)
        
    async def _on_nav_updated(self, event: NavigationStateChanged):
        self.context.navigation_state = event.new_state
        
    async def _on_world_state_updated(self, event: WorldStateUpdated):
        self.context.world_state = event.state.__dict__ if hasattr(event.state, '__dict__') else {}

    async def _on_health_updated(self, event: HealthReceived):
        self.context.system_health = event.data.get('status', 'OK')
        
    async def _on_battery_critical(self, event: BatteryCritical):
        self.context.update_battery(critical=True)
        
    async def _on_obstacle_appeared(self, event: ObstacleAppeared):
        self.context.obstacle_detected = True

    async def _on_obstacle_cleared(self, event: ObstacleCleared):
        self.context.obstacle_detected = False
        
    async def _on_hazard_detected(self, event: HazardDetected):
        self.context.hazard_detected = True
        
    async def _on_hazard_cleared(self, event: HazardCleared):
        self.context.hazard_detected = False

    # --- Main Loop ---
    async def _reasoning_loop(self):
        """Ticks the decision engine at 5Hz."""
        while self._running:
            try:
                # 1. Create a fresh immutable blackboard for this tick
                blackboard = AIBlackboard(timestamp=time.perf_counter())
                
                # 2. Reason (Generate candidates)
                self.reasoning.evaluate(self.context, self.memory, blackboard)
                
                # 3. Apply Rules (Filter or Emergency Override)
                self.rules.enforce(self.context, blackboard)
                
                # 4. Decide (Resolve priority and calculate confidence)
                self.decision.decide(blackboard)
                
                # 5. Execute (Map to Semantic Event)
                if blackboard.final_decision:
                    self.action_selector.execute(blackboard.final_decision)
                
                # 6. Record diagnostics
                self.stats.record_decision()
                
                # Sleep to maintain ~5Hz tick rate
                await asyncio.sleep(0.2)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"AIEngine loop error: {e}")
                await asyncio.sleep(0.5)
