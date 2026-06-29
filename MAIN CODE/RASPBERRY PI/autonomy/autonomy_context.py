"""
autonomy_context.py
Recon Rover V1 - Autonomous Intelligence

A unified cognitive snapshot of the entire rover state.
"""

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class AutonomyContext:
    mission_state: str = "UNKNOWN"
    navigation_state: str = "UNKNOWN"
    world_state: Dict[str, Any] = field(default_factory=dict)
    vision_state: Dict[str, Any] = field(default_factory=dict)
    audio_state: Dict[str, Any] = field(default_factory=dict)
    llm_decision: Dict[str, Any] = field(default_factory=dict)
    ai_decision: Dict[str, Any] = field(default_factory=dict)
    health_status: str = "OK"
    battery_critical: bool = False
