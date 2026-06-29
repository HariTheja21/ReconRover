"""
llm_manager.py
Recon Rover V1 - Local LLM Decision Engine

Orchestrates the entire internal LLM transaction loop.
"""

from typing import Optional
from .llm_client import LLMClient
from .llm_request import LLMRequest
from .llm_response import LLMResponse
from .llm_prompt_builder import LLMPromptBuilder
from .llm_response_parser import LLMResponseParser
from .llm_context_manager import LLMContextManager
from .llm_health import LLMHealth
from .llm_statistics import LLMStatistics

class LLMManager:
    def __init__(self):
        self.client = LLMClient()
        self.context_manager = LLMContextManager()
        self.health = LLMHealth()
        self.stats = LLMStatistics()

    async def execute_decision_cycle(self, multimodal_context: str) -> Optional[LLMResponse]:
        """
        Takes the unified multimodal context, wraps it in the prompt, queries the LLM,
        and parses the result.
        """
        self.stats.record_request()
        
        # 1. Build Prompts
        system_prompt = LLMPromptBuilder.build_system_prompt()
        history_str = self.context_manager.get_history_string()
        user_prompt = LLMPromptBuilder.build_user_prompt(multimodal_context, history_str)
        
        # 2. Build Request
        request = LLMRequest(
            prompt=user_prompt,
            system_prompt=system_prompt,
            require_json=True
        )
        
        # 3. Execute with Timeout
        raw_text = await self.client.execute_request(request)
        if not raw_text:
            self.stats.record_failure()
            self.health.record_timeout()
            return None
            
        # 4. Parse JSON
        parsed_response = LLMResponseParser.parse(raw_text)
        if not parsed_response.is_valid_json:
            self.stats.record_failure()
            self.health.record_parse_error()
            return parsed_response # Return anyway to allow fallback logic in Engine
            
        # 5. Success
        self.stats.record_success()
        self.health.record_success()
        
        # 6. Update Context Memory
        self.context_manager.add_interaction(user_prompt, raw_text)
        
        return parsed_response
