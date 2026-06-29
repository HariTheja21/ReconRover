"""
llm_context_manager.py
Recon Rover V1 - Local LLM Decision Engine

Maintains the short-term conversation history for the LLM session.
Prevents context window explosion.
"""

from typing import List, Dict

class LLMContextManager:
    def __init__(self, max_history: int = 5):
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        
    def add_interaction(self, user_prompt: str, assistant_reply: str):
        self.history.append({"role": "user", "content": user_prompt})
        self.history.append({"role": "assistant", "content": assistant_reply})
        
        # Trim history if it exceeds limit (keep pairs)
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2):]
            
    def get_history_string(self) -> str:
        if not self.history:
            return "No previous history."
            
        lines = []
        for msg in self.history:
            lines.append(f"{msg['role'].upper()}: {msg['content']}")
        return "\n".join(lines)
        
    def clear(self):
        self.history.clear()
