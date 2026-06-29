"""
mission_state.py
Recon Rover V1 - Mission Manager

Defines mission lifecycle states and strict transitions.
"""

from enum import Enum, auto

class MissionLifecycle(Enum):
    CREATED = auto()
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    RESUMED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    TIMED_OUT = auto()
    ABORTED = auto()

class MissionStateMachine:
    def __init__(self):
        self._state = MissionLifecycle.CREATED
        
        self._valid_transitions = {
            MissionLifecycle.CREATED: {MissionLifecycle.READY, MissionLifecycle.CANCELLED},
            MissionLifecycle.READY: {MissionLifecycle.RUNNING, MissionLifecycle.CANCELLED},
            MissionLifecycle.RUNNING: {
                MissionLifecycle.PAUSED, MissionLifecycle.COMPLETED, 
                MissionLifecycle.FAILED, MissionLifecycle.CANCELLED, 
                MissionLifecycle.TIMED_OUT, MissionLifecycle.ABORTED
            },
            MissionLifecycle.PAUSED: {
                MissionLifecycle.RESUMED, MissionLifecycle.CANCELLED, MissionLifecycle.ABORTED
            },
            MissionLifecycle.RESUMED: {
                MissionLifecycle.RUNNING, MissionLifecycle.PAUSED, MissionLifecycle.CANCELLED, MissionLifecycle.ABORTED
            },
            # Terminal states below. No transitions allowed out of these.
            MissionLifecycle.COMPLETED: set(),
            MissionLifecycle.FAILED: set(),
            MissionLifecycle.CANCELLED: set(),
            MissionLifecycle.TIMED_OUT: set(),
            MissionLifecycle.ABORTED: set(),
        }

    @property
    def current_state(self) -> MissionLifecycle:
        return self._state

    def can_transition(self, target_state: MissionLifecycle) -> bool:
        if target_state == self._state:
            return True
        return target_state in self._valid_transitions[self._state]

    def transition(self, target_state: MissionLifecycle) -> bool:
        if self.can_transition(target_state):
            self._state = target_state
            return True
        return False
