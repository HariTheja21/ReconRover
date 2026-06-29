"""
llm_request.py
Recon Rover V1 - Local LLM Decision Engine

Strongly typed representation of an outbound LLM request.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMRequest:
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.1
    max_tokens: int = 500
    require_json: bool = True
