"""
provider_factory.py
Recon Rover V1 - Local LLM Framework

Instantiates the correct provider instance based on configuration.
"""

from llm.llm_provider import LLMProvider, MockLLMProvider
from .provider_config import ProviderConfig
from .provider_health import ProviderHealth
from .provider_statistics import ProviderStatistics
from .ollama_provider import OllamaProvider

class ProviderFactory:
    @staticmethod
    def create_provider(
        config: ProviderConfig, 
        health: ProviderHealth, 
        stats: ProviderStatistics
    ) -> LLMProvider:
        """
        Returns the appropriate provider instance.
        """
        provider_type = config.provider_type.upper()
        
        if provider_type == "OLLAMA":
            return OllamaProvider(config, health, stats)
        elif provider_type == "MOCK":
            return MockLLMProvider()
        else:
            # Fallback for unconfigured/unsupported providers
            return MockLLMProvider()
