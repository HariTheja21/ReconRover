"""
application_state.py
Recon Rover V1 - System Orchestrator

Defines absolute lifecycle states for all modules and the master app.
"""

from enum import Enum, auto

class LifecycleState(Enum):
    UNINITIALIZED = auto()
    REGISTERED = auto()
    INITIALIZING = auto()
    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPING = auto()
    STOPPED = auto()
    FAILED = auto()
    RECOVERING = auto()
    SHUTDOWN = auto()
