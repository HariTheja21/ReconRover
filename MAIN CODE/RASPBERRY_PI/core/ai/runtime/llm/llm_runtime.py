import asyncio
from typing import Any

from .llm_health import LLMHealth
from .llm_statistics import LLMStatistics
from .llm_bridge import LLMBridge
from .llm_registry import LLMRegistry
from .llm_loader import LLMLoader
from .provider_manager import ProviderManager
from .authentication_manager import AuthenticationManager
from .session_manager import SessionManager
from .streaming_manager import StreamingManager
from .provider_failover import ProviderFailover
from .model_discovery import ModelDiscovery
from .response_parser import ResponseParser
from .provider_health import ProviderHealth
from .provider_statistics import ProviderStatistics
from .llm_scheduler import LLMScheduler

from .providers.ollama_provider import OllamaProvider
from .providers.openai_provider import OpenAIProvider
from .providers.lmstudio_provider import LMStudioProvider
from .providers.llamacpp_provider import LlamaCPPProvider
from .providers.vllm_provider import vLLMProvider
from .providers.gemini_provider import GeminiProvider
from .providers.claude_provider import ClaudeProvider

class LLMRuntime:
    def __init__(self, event_bus: Any):
        self.bridge = LLMBridge(event_bus)
        
        self.registry = LLMRegistry()
        self._register_default_providers()
        
        self.loader = LLMLoader(self.registry)
        self.auth = AuthenticationManager()
        self.provider_manager = ProviderManager(self.loader, self.auth)
        
        self.session = SessionManager()
        self.streaming = StreamingManager(self.bridge.publish_event)
        self.failover = ProviderFailover(self.provider_manager, self.bridge.publish_event)
        self.discovery = ModelDiscovery()
        self.parser = ResponseParser()
        
        self.p_health = ProviderHealth(self.bridge.publish_event)
        self.p_stats = ProviderStatistics()
        
        self.scheduler = LLMScheduler(self.failover, self.session, self.parser, self.bridge.publish_event)
        
    def _register_default_providers(self):
        self.registry.register("ollama", OllamaProvider)
        self.registry.register("openai", OpenAIProvider)
        self.registry.register("lmstudio", LMStudioProvider)
        self.registry.register("llamacpp", LlamaCPPProvider)
        self.registry.register("vllm", vLLMProvider)
        self.registry.register("gemini", GeminiProvider)
        self.registry.register("claude", ClaudeProvider)
        
    async def initialize(self):
        return True
