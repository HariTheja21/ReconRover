"""
llm_response.py
Recon Rover V1 - Local LLM Decision Engine

Strongly typed representation of a parsed LLM decision.
"""

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class LLMResponse:
    raw_text: str
    is_valid_json: bool
    parsed_data: Dict[str, Any] = field(default_factory=dict)
    
    # Core Decision Fields
    movement_intent: str = "STOP"
    priority: str = "NORMAL"
    reasoning_summary: str = ""
    confidence: float = 0.0
    mission_recommendation: str = ""
    safety_assessment: str = "SAFE"
