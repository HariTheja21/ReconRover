"""
llm_session.py
Recon Rover V1 - Local LLM Framework

Maintains a bounded rolling conversation history for the LLM context.
"""

from typing import List, Dict

class LLMSession:
    def __init__(self, max_history_turns: int = 5):
        self.max_history_turns = max_history_turns
        self.history: List[Dict[str, str]] = []

    def add_turn(self, context_prompt: str, raw_response: str):
        """Records a single inference turn."""
        self.history.append({"prompt": context_prompt, "response": raw_response})
        self._prune()

    def get_history_string(self) -> str:
        """Formats the history for injection into the next prompt."""
        if not self.history:
            return "No previous history."
            
        lines = []
        for i, turn in enumerate(self.history):
            lines.append(f"--- Turn -{len(self.history)-i} ---")
            lines.append(f"Decision: {turn['response']}")
        return "\n".join(lines)

    def _prune(self):
        """Evicts oldest turns to maintain token bounds."""
        while len(self.history) > self.max_history_turns:
            self.history.pop(0)
