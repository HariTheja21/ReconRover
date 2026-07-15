from typing import Dict, Any

class CommandParser:
    def __init__(self):
        # Stub for mapping transcripts directly to rigid commands 
        # (prior to LLM integration)
        pass
        
    def parse(self, text: str) -> tuple[str, Dict[str, Any], float]:
        text_lower = text.lower()
        if "move forward" in text_lower:
            return "drive_forward", {"distance": 5.0}, 0.9
        if "stop" in text_lower:
            return "emergency_stop", {}, 1.0
            
        return "unknown", {}, 0.0
