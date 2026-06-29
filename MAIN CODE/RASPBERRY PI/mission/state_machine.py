"""
state_machine.py
Recon Rover V1 - Behavior Engine

Defines operational behavior states for the rover.
"""

from enum import Enum, auto
from logger import Logger

class RobotBehaviorState(Enum):
    IDLE = auto()
    READY = auto()
    EXPLORING = auto()
    FOLLOW_TARGET = auto()
    AVOIDING = auto()
    INSPECTING = auto()
    RETURN_HOME = auto()
    MISSION_COMPLETE = auto()
    MISSION_FAILED = auto()
    SAFE_MODE = auto()
    EMERGENCY_STOP = auto()

class BehaviorStateMachine:
    """
    Manages the internal operational state of the rover.
    """
    def __init__(self):
        self._state = RobotBehaviorState.IDLE
        self.log = Logger.get("BehaviorStateMachine")

    @property
    def current_state(self) -> RobotBehaviorState:
        return self._state

    def set_state(self, new_state: RobotBehaviorState):
        if self._state != new_state:
            self.log.info(f"Behavior State Transition: {self._state.name} -> {new_state.name}")
            self._state = new_state
