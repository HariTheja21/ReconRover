"""
navigation.py
Recon Rover V1 - Cognitive Layer

Navigation Engine. Deterministically converts WorldState into MovementRequests.
"""

from lifecycle_manager import BaseModule
from event_bus import (
    EventBus, WorldStateUpdated, NavigationDecision, 
    NavigationStateChanged, RecoveryStarted, RecoveryCompleted, 
    EmergencyStopRequested, PathSelected, MovementRequestEvent
)
from navigation.navigation_state import NavState, MovementAction
from navigation.navigation_context import NavigationContext
from navigation.obstacle_avoidance import ObstacleAvoidance
from navigation.path_selector import PathSelector
from navigation.movement_policy import MovementPolicy
from navigation.recovery_behaviors import RecoveryBehaviors

class NavigationEngine(BaseModule):
    """
    Subscribes to WorldStateUpdated. Runs the deterministic navigation pipeline.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.context = NavigationContext()
        self.obstacle_avoidance = ObstacleAvoidance()
        self.path_selector = PathSelector()
        self.movement_policy = MovementPolicy()
        self.recovery_behaviors = RecoveryBehaviors()

    async def initialize(self):
        self.event_bus.subscribe(WorldStateUpdated, self._on_world_state_updated)
        self.log.info("NavigationEngine initialized.")

    async def start(self):
        self.log.info("NavigationEngine started.")

    async def stop(self):
        self.log.info("NavigationEngine stopped.")

    def health(self) -> str:
        return "OK"

    async def _on_world_state_updated(self, event: WorldStateUpdated):
        world_state = event.state
        
        # 1. Evaluate safe directions
        free_directions = self.obstacle_avoidance.evaluate_directions(world_state)
        
        # 2. Check Recovery State
        if self.context.current_state == NavState.RECOVERY:
            new_state = self.recovery_behaviors.handle_recovery(self.context)
            if new_state == NavState.IDLE:
                self.event_bus.publish(RecoveryCompleted())
            # Otherwise we stick with the recovery command (e.g. EMERGENCY_STOP or WAITING)
        else:
            # 3. Normal Path Selection
            new_state = self.path_selector.select_path(free_directions, self.context, world_state.threat_level)
            
            # Transitioning into recovery?
            if new_state == NavState.RECOVERY and self.context.current_state != NavState.RECOVERY:
                self.event_bus.publish(RecoveryStarted(reason="PathSelector forced recovery"))
                new_state = self.recovery_behaviors.handle_recovery(self.context)

        # 4. Update Context
        old_state = self.context.current_state
        self.context.update_state(new_state)
        
        if old_state != new_state:
            self.log.info(f"NavState changed: {old_state.name} -> {new_state.name}")
            self.event_bus.publish(NavigationStateChanged(old_state=old_state.name, new_state=new_state.name))
            
            if new_state == NavState.EMERGENCY_STOP:
                self.event_bus.publish(EmergencyStopRequested(reason="Critical threat or Recovery halt"))

        # 5. Apply Movement Policy
        request = self.movement_policy.generate_request(new_state, self.context)
        
        # Publish MovementRequest (for the Command Builder eventually)
        self.event_bus.publish(MovementRequestEvent(
            action=request.action.value, 
            speed_factor=request.speed_factor
        ))
