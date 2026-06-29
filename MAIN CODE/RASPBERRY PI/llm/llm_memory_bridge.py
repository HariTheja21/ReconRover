"""
llm_memory_bridge.py
Recon Rover V1 - Local LLM Framework

Translates transient AIMemory into a token-efficient semantic string for the LLM context.
"""

from typing import Dict
import time

class LLMMemoryBridge:
    @staticmethod
    def format_memory(memory_dict: Dict[str, float]) -> str:
        """
        Converts the AIMemory internal dictionary to a chronological text summary.
        Example output: "- 3.2s ago: speech_heard"
        """
        if not memory_dict:
            return "No recent events."
            
        current_time = time.perf_counter()
        lines = []
        for key, timestamp in memory_dict.items():
            delta = current_time - timestamp
            lines.append(f"- {delta:.1f}s ago: {key}")
            
        return "\n".join(lines)
