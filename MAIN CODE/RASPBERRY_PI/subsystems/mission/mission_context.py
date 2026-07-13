"""
mission_context.py
Recon Rover V1 - Mission Manager

Lightweight container for the current and previous mission execution data.
"""

from dataclasses import dataclass, field
import time
from typing import Optional
from .mission_state import MissionLifecycle

@dataclass
class MissionContext:
    mission_id: str
    mission_type: str
    owner: str
    priority: int
    state: MissionLifecycle = MissionLifecycle.CREATED
    start_time_ms: int = 0
    timeout_ms: int = 0
    progress: float = 0.0
    confidence: float = 1.0
    metadata: dict = field(default_factory=dict)
    
    @property
    def is_terminal(self) -> bool:
        return self.state in {
            MissionLifecycle.COMPLETED, MissionLifecycle.FAILED, 
            MissionLifecycle.CANCELLED, MissionLifecycle.TIMED_OUT, MissionLifecycle.ABORTED
        }

class MissionStore:
    """Holds active and history contexts."""
    def __init__(self):
        self.active_mission: Optional[MissionContext] = None
        self.previous_mission: Optional[MissionContext] = None
