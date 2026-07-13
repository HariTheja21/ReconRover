"""
movement_policy.py
Recon Rover V1 - Cognitive Layer

Translates logical NavStates into semantic MovementRequests.
"""

from .navigation_state import NavState, MovementAction, MovementRequest
from .navigation_context import NavigationContext

class MovementPolicy:
    """
    Enforces safe state transitions to avoid hardware damage (e.g. motor torque spikes).
    """
    
    def __init__(self):
        pass

    def generate_request(self, target_state: NavState, context: NavigationContext) -> MovementRequest:
        """
        Takes the desired state and the context, producing a safe MovementRequest.
        """
        
        # Protect against sudden direction reversals
        if self._requires_stop_transition(context.current_state, target_state):
            return MovementRequest(action=MovementAction.STOP, speed_factor=0.0)

        # Map state to action
        if target_state == NavState.FORWARD:
            return MovementRequest(action=MovementAction.FORWARD, speed_factor=0.5)
            
        if target_state == NavState.BACKWARD:
            return MovementRequest(action=MovementAction.REVERSE, speed_factor=0.4)
            
        if target_state == NavState.TURN_LEFT:
            return MovementRequest(action=MovementAction.TURN_LEFT, speed_factor=0.4)
            
        if target_state == NavState.TURN_RIGHT:
            return MovementRequest(action=MovementAction.TURN_RIGHT, speed_factor=0.4)
            
        if target_state == NavState.EMERGENCY_STOP:
            return MovementRequest(action=MovementAction.STOP, speed_factor=0.0)
            
        if target_state == NavState.RECOVERY:
            return MovementRequest(action=MovementAction.STOP, speed_factor=0.0)
            
        if target_state == NavState.WAITING:
            return MovementRequest(action=MovementAction.WAIT, speed_factor=0.0)
            
        return MovementRequest(action=MovementAction.STOP, speed_factor=0.0)

    def _requires_stop_transition(self, current: NavState, target: NavState) -> bool:
        """Returns True if a STOP must be inserted between these two states."""
        # e.g., Moving Forward -> Backward requires a stop
        if current == NavState.FORWARD and target == NavState.BACKWARD:
            return True
        if current == NavState.BACKWARD and target == NavState.FORWARD:
            return True
        # Similarly for high speed turns reversing direction
        if current == NavState.TURN_LEFT and target == NavState.TURN_RIGHT:
            return True
        if current == NavState.TURN_RIGHT and target == NavState.TURN_LEFT:
            return True
            
        return False
