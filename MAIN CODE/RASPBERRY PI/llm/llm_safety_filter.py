"""
llm_safety_filter.py
Recon Rover V1 - Local LLM Framework

The final firewall. Rejects any malicious or hallucinatory content.
"""

from typing import List
from ai.ai_blackboard import CandidateAction

class LLMSafetyFilter:
    DANGEROUS_STRINGS = [
        "import os", "import sys", "subprocess", "eval(", "exec(",
        "__import__", "open(", "sh ", "bash ", "rm -rf", "sudo"
    ]
    
    @classmethod
    def check_raw_text(cls, text: str) -> bool:
        """Returns True if safe, False if dangerous code is detected."""
        lower_text = text.lower()
        for threat in cls.DANGEROUS_STRINGS:
            if threat in lower_text:
                return False
        return True

    @classmethod
    def filter_actions(cls, actions: List[CandidateAction]) -> List[CandidateAction]:
        """
        Filters out actions that attempt direct hardware access.
        Only allows high-level semantic intents.
        """
        safe_actions = []
        for action in actions:
            # The validator already restricts intents to a safe whitelist,
            # but we do an additional parameters check here.
            
            # Example: deny manually setting PWM values
            if "pwm" in action.parameters or "gpio" in action.parameters:
                continue
                
            safe_actions.append(action)
            
        return safe_actions
