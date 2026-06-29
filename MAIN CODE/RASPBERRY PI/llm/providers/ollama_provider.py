"""
ollama_provider.py
Recon Rover V1 - Local LLM Framework

Asynchronous HTTP integration for the Ollama REST API.
"""

import aiohttp
import asyncio
from typing import Optional
from llm.llm_provider import LLMProvider
from .provider_config import ProviderConfig
from .provider_health import ProviderHealth
from .provider_statistics import ProviderStatistics

class OllamaProvider(LLMProvider):
    def __init__(self, config: ProviderConfig, health: ProviderHealth, stats: ProviderStatistics):
        self.config = config
        self.health = health
        self.stats = stats
        self.url = f"{self.config.host}/api/generate"

    async def generate(self, prompt: str) -> Optional[str]:
        """
        Executes a non-blocking POST to Ollama.
        Implements exponential backoff on failure.
        """
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "top_p": self.config.top_p,
                "num_ctx": self.config.context_length
            },
            "keep_alive": self.config.keep_alive
        }

        for attempt in range(self.config.retry_count):
            try:
                # Use a very generous timeout for LLM inference (e.g. 30 seconds)
                timeout = aiohttp.ClientTimeout(total=self.config.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(self.url, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # Record Token Telemetry
                            p_tokens = data.get("prompt_eval_count", 0)
                            c_tokens = data.get("eval_count", 0)
                            self.stats.record_success(p_tokens, c_tokens)
                            
                            return data.get("response")
                        else:
                            self.health.record_failure()
                            
            except asyncio.TimeoutError:
                self.health.record_failure(is_timeout=True)
            except aiohttp.ClientError:
                self.health.record_failure()
            except Exception:
                self.health.record_failure()

            # Exponential backoff: 1s, 2s, 4s...
            if attempt < self.config.retry_count - 1:
                self.health.record_retry()
                await asyncio.sleep(2 ** attempt)

        # All retries failed
        self.stats.record_failure()
        return None
