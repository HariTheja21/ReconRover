"""
navigation_context.py
Recon Rover V1 - Cognitive Layer

Maintains bounded historical context to prevent navigation oscillations.
"""

from dataclasses import dataclass, field
from typing import List
import collections
from .navigation_state import NavState

@dataclass
class NavigationContext:
    current_state: NavState = NavState.IDLE
    previous_state: NavState = NavState.IDLE
    
    target_direction: str = "front"
    last_successful_direction: str = "front"
    
    # Bounded history of past states to detect cyclic oscillations
    state_history: collections.deque = field(default_factory=lambda: collections.deque(maxlen=10))
    
    recovery_attempts: int = 0
    navigation_confidence: float = 1.0

    def update_state(self, new_state: NavState):
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_history.append(new_state)

    def is_oscillating(self) -> bool:
        """
        Detects if the rover is bouncing rapidly between states 
        (e.g., TURN_LEFT -> TURN_RIGHT -> TURN_LEFT).
        """
        if len(self.state_history) < 4:
            return False
            
        history = list(self.state_history)
        if (history[-1] == NavState.TURN_LEFT and history[-2] == NavState.TURN_RIGHT and 
            history[-3] == NavState.TURN_LEFT and history[-4] == NavState.TURN_RIGHT):
            return True
            
        if (history[-1] == NavState.TURN_RIGHT and history[-2] == NavState.TURN_LEFT and 
            history[-3] == NavState.TURN_RIGHT and history[-4] == NavState.TURN_LEFT):
            return True
            
        return False
