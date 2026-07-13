"""
context_formatter.py
Recon Rover V1 - Unified Multimodal Context Builder

Generates the final deterministic string prompt block for the LLM.
"""

from typing import List, Tuple

class ContextFormatter:
    def format_prompt_block(self, prioritized_blocks: List[Tuple[str, str]]) -> str:
        """
        Creates a clean, token-efficient string.
        Format: [LABEL] content \n
        """
        if not prioritized_blocks:
            return "[SYSTEM] No telemetry available."
            
        formatted_lines = []
        for label, content in prioritized_blocks:
            formatted_lines.append(f"[{label}] {content}")
            
        return "\n".join(formatted_lines)
