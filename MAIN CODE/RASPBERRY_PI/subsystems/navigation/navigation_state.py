"""
navigation_state.py
Recon Rover V1 - Cognitive Layer

Defines the core states and semantic requests for the Navigation Engine.
"""

from enum import Enum
from dataclasses import dataclass

class NavState(Enum):
    IDLE = 1
    MANUAL = 2
    FORWARD = 3
    TURN_LEFT = 4
    TURN_RIGHT = 5
    BACKWARD = 6
    AVOID_OBSTACLE = 7
    RECOVERY = 8
    EMERGENCY_STOP = 9
    WAITING = 10

class MovementAction(Enum):
    STOP = "Stop"
    FORWARD = "MoveForward"
    REVERSE = "Reverse"
    TURN_LEFT = "RotateLeft"
    TURN_RIGHT = "RotateRight"
    WAIT = "Wait"

@dataclass
class MovementRequest:
    action: MovementAction
    speed_factor: float = 0.0  # 0.0 to 1.0
