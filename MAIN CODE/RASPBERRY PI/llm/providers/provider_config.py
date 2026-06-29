"""
provider_config.py
Recon Rover V1 - Local LLM Framework

Configuration dataclass for the LLM Provider layer.
"""

from dataclasses import dataclass

@dataclass
class ProviderConfig:
    provider_type: str = "OLLAMA"
    host: str = "http://localhost:11434"
    model: str = "llama3" # Default, can be overridden by ProviderModels
    timeout: float = 30.0
    retry_count: int = 3
    temperature: float = 0.1
    top_p: float = 0.9
    context_length: int = 4096
    max_tokens: int = 500
    keep_alive: str = "5m"
