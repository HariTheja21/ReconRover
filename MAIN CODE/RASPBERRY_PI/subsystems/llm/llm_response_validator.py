"""
llm_response_validator.py
Recon Rover V1 - Local LLM Framework

Validates that the parsed JSON strictly conforms to the CandidateAction schema.
"""

from typing import List, Dict, Optional
from ai.ai_blackboard import CandidateAction

class LLMResponseValidator:
    ALLOWED_INTENTS = {
        "Patrol", "Explore", "ReturnHome", "EmergencyStop", 
        "GreetHuman", "ProcessSpeech", "ScanArea", "FollowTarget", "Idle"
    }

    @classmethod
    def validate(cls, parsed_data: List[Dict]) -> Optional[List[CandidateAction]]:
        """
        Converts raw dictionaries into CandidateAction objects if they pass validation.
        Returns None if validation fails structurally.
        """
        valid_actions = []
        for item in parsed_data:
            if not isinstance(item, dict):
                continue
                
            intent = item.get("intent")
            if not intent or intent not in cls.ALLOWED_INTENTS:
                continue # Skip unknown intents
                
            priority_score = item.get("priority_score", 0)
            if not isinstance(priority_score, int):
                priority_score = 0
                
            target = item.get("target")
            parameters = item.get("parameters", {})
            if not isinstance(parameters, dict):
                parameters = {}
                
            valid_actions.append(CandidateAction(
                intent=intent,
                target=target,
                parameters=parameters,
                priority_score=priority_score,
                source="llm"
            ))
            
        if not valid_actions:
            return None
            
        return valid_actions
