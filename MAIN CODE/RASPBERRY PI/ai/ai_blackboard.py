"""
ai_blackboard.py
Recon Rover V1 - AI Decision Engine

Shared, immutable reasoning state passed between engines during a single decision tick.
Prevents global mutable state.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class CandidateAction:
    intent: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    priority_score: int = 0
    source: str = "reasoning_engine"

@dataclass
class AIBlackboard:
    """An immutable snapshot created per tick for passing data down the pipeline."""
    timestamp: float
    candidate_actions: List[CandidateAction] = field(default_factory=list)
    filtered_actions: List[CandidateAction] = field(default_factory=list)
    final_decision: Optional[CandidateAction] = None
    rule_overrides: List[str] = field(default_factory=list)
