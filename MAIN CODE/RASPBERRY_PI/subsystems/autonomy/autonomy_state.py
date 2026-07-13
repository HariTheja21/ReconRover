"""
autonomy_state.py
Recon Rover V1 - Autonomous Intelligence

Defines the macro-states for the Autonomy Engine.
"""

from enum import Enum, auto

class AutonomyState(Enum):
    IDLE = auto()
    PLANNING = auto()
    EXECUTING = auto()
    SUSPENDED = auto()
    FAULT = auto()
