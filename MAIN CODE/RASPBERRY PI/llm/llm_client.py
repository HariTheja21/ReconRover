"""
llm_client.py
Recon Rover V1 - Local LLM Decision Engine

Wraps the underlying ProviderFactory with timeouts and retries.
"""

import asyncio
from typing import Optional
from .llm_request import LLMRequest
from .providers.provider_factory import ProviderFactory
from .providers.provider_config import ProviderConfig
from .providers.provider_health import ProviderHealth
from .providers.provider_statistics import ProviderStatistics

class LLMClient:
    def __init__(self):
        self.config = ProviderConfig(provider_type="OLLAMA")
        self.health = ProviderHealth()
        self.stats = ProviderStatistics()
        
        self.provider = ProviderFactory.create_provider(
            self.config, self.health, self.stats
        )

    async def execute_request(self, request: LLMRequest, timeout_sec: float = 10.0, max_retries: int = 2) -> Optional[str]:
        """Executes inference with strict timeout and exponential backoff retry."""
        attempt = 0
        while attempt <= max_retries:
            try:
                # We enforce timeout at the async level to ensure we never block forever
                raw_response = await asyncio.wait_for(
                    self.provider.generate(request.prompt, system_prompt=request.system_prompt),
                    timeout=timeout_sec
                )
                return raw_response
            except asyncio.TimeoutError:
                self.health.record_timeout()
                attempt += 1
                if attempt <= max_retries:
                    await asyncio.sleep(2 ** attempt) # Exponential backoff
            except Exception as e:
                self.health.record_error(str(e))
                attempt += 1
                if attempt <= max_retries:
                    await asyncio.sleep(1.0)
                    
        return None
