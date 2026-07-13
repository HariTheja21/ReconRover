"""
path_selector.py
Recon Rover V1 - Cognitive Layer

Deterministic path selection logic based on obstacle avoidance inputs.
"""

from typing import Dict
from .navigation_state import NavState
from .navigation_context import NavigationContext

class PathSelector:
    """
    Selects the next optimal navigation state strictly based on priority:
    1. Forward
    2. Left
    3. Right
    4. Reverse
    5. Recovery
    """
    
    def __init__(self):
        pass

    def select_path(self, free_directions: Dict[str, bool], context: NavigationContext, threat_level: str) -> NavState:
        """
        Returns the new desired NavState.
        """
        if threat_level == "CRITICAL":
            return NavState.EMERGENCY_STOP

        if context.is_oscillating():
            # Break the cycle by forcing a recovery behavior
            return NavState.RECOVERY

        if context.current_state == NavState.MANUAL:
            return NavState.MANUAL

        # 1. Forward
        if free_directions["front"]:
            return NavState.FORWARD

        # 2. Left
        if free_directions["left"]:
            return NavState.TURN_LEFT

        # 3. Right
        if free_directions["right"]:
            return NavState.TURN_RIGHT

        # 4. Reverse
        if free_directions["rear"]:
            return NavState.BACKWARD

        # 5. Trapped
        return NavState.RECOVERY
