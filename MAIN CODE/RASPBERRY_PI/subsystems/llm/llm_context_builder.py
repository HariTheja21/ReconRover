"""
llm_context_builder.py
Recon Rover V1 - Local LLM Framework

Compresses the AIContext dataclass into a token-efficient text format.
"""

from typing import Any
import json
from .llm_memory_bridge import LLMMemoryBridge

class LLMContextBuilder:
    @staticmethod
    def build_context_string(ai_context: Any, memory_dict: dict) -> str:
        """
        Flattens and compresses the context safely.
        Assumes ai_context is the Phase 4.5 AIContext object.
        """
        # Compress Vision (e.g. drop raw coordinates, keep counts)
        vision_summary = "None"
        if ai_context.vision_semantics:
            vision_summary = json.dumps(ai_context.vision_semantics)
            
        audio_summary = "None"
        if ai_context.audio_semantics:
            audio_summary = json.dumps(ai_context.audio_semantics)
            
        memory_summary = LLMMemoryBridge.format_memory(memory_dict)
            
        context_str = (
            f"SYSTEM_HEALTH: {ai_context.system_health}\n"
            f"BATTERY_CRITICAL: {ai_context.battery_critical}\n"
            f"MISSION_STATE: {ai_context.mission_state}\n"
            f"NAV_STATE: {ai_context.navigation_state}\n"
            f"CURRENT_OBJECTIVE: {ai_context.current_objective}\n"
            f"---\n"
            f"VISION: {vision_summary}\n"
            f"AUDIO: {audio_summary}\n"
            f"---\n"
            f"RECENT_MEMORY:\n{memory_summary}"
        )
        return context_str
