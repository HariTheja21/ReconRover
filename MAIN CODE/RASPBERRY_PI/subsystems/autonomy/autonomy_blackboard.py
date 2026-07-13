"""
autonomy_blackboard.py
Recon Rover V1 - Autonomous Intelligence

Working memory for one planning cycle. Destroyed after every cycle.
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AutonomyBlackboard:
    timestamp: float
    candidate_objectives: List[str] = field(default_factory=list)
    selected_objective: Optional[str] = None
    coordinator_constraints: List[str] = field(default_factory=list)
    supervisor_overrides: List[str] = field(default_factory=list)
