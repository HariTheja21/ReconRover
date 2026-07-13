"""
ai_state_machine.py
Recon Rover V1 - AI Decision Engine

Defines the states and allowed transitions for the cognitive layer.
"""

from enum import Enum, auto

class AIState(Enum):
    IDLE = auto()
    EXPLORING = auto()
    AVOIDING = auto()
    SCANNING = auto()
    RETURNING = auto()
    PAUSED = auto()
    EMERGENCY = auto()

class AIStateMachine:
    def __init__(self):
        self._current_state = AIState.IDLE
        
        # Define allowed transitions
        self._valid_transitions = {
            AIState.IDLE: {AIState.EXPLORING, AIState.RETURNING, AIState.PAUSED, AIState.EMERGENCY, AIState.SCANNING},
            AIState.EXPLORING: {AIState.IDLE, AIState.AVOIDING, AIState.EMERGENCY, AIState.PAUSED, AIState.RETURNING},
            AIState.AVOIDING: {AIState.IDLE, AIState.EXPLORING, AIState.EMERGENCY, AIState.PAUSED, AIState.SCANNING},
            AIState.SCANNING: {AIState.IDLE, AIState.EXPLORING, AIState.AVOIDING, AIState.EMERGENCY, AIState.PAUSED},
            AIState.RETURNING: {AIState.IDLE, AIState.AVOIDING, AIState.EMERGENCY, AIState.PAUSED},
            AIState.PAUSED: {AIState.IDLE, AIState.EMERGENCY},
            AIState.EMERGENCY: {AIState.IDLE}  # Must reset to IDLE after emergency
        }

    @property
    def current_state(self) -> AIState:
        return self._current_state

    def can_transition(self, target_state: AIState) -> bool:
        if target_state == self._current_state:
            return True
        return target_state in self._valid_transitions[self._current_state]

    def transition(self, target_state: AIState) -> bool:
        if self.can_transition(target_state):
            self._current_state = target_state
            return True
        return False
