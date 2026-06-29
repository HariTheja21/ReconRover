"""
llm_response_parser.py
Recon Rover V1 - Local LLM Decision Engine

Safely parses raw LLM output, aggressively stripping markdown and enforcing JSON.
"""

import json
from .llm_response import LLMResponse

class LLMResponseParser:
    @staticmethod
    def parse(raw_text: str) -> LLMResponse:
        """Attempts to extract and parse JSON from the raw text."""
        cleaned_text = raw_text.strip()
        
        # Strip potential markdown fences
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
            
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        cleaned_text = cleaned_text.strip()
        
        response = LLMResponse(raw_text=raw_text, is_valid_json=False)
        
        try:
            parsed_data = json.loads(cleaned_text)
            response.is_valid_json = True
            response.parsed_data = parsed_data
            
            # Map known fields securely
            response.movement_intent = parsed_data.get("MovementIntent", "STOP")
            response.priority = parsed_data.get("Priority", "NORMAL")
            response.reasoning_summary = parsed_data.get("ReasoningSummary", "Parse error fall-through.")
            response.confidence = float(parsed_data.get("Confidence", 0.0))
            response.mission_recommendation = parsed_data.get("MissionRecommendation", "")
            response.safety_assessment = parsed_data.get("SafetyAssessment", "SAFE")
            
        except json.JSONDecodeError:
            pass # Fails safely, defaults to STOP and SAFE.
            
        return response
