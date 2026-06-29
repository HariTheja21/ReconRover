"""
provider_models.py
Recon Rover V1 - Local LLM Framework

Handles discovery of available models on the provider.
"""

import aiohttp
from typing import List, Optional
from .provider_config import ProviderConfig

class ProviderModels:
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.available_models: List[str] = []

    async def discover_ollama_models(self) -> List[str]:
        """Queries the Ollama /api/tags endpoint to find installed models."""
        url = f"{self.config.host}/api/tags"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5.0) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.available_models = [m["name"] for m in data.get("models", [])]
                        return self.available_models
        except Exception:
            pass
            
        return []

    def select_default_model(self) -> str:
        """Selects a safe default from the discovered list."""
        if not self.available_models:
            return self.config.model # fallback
            
        # Priority list
        preferred = ["llama3", "mistral", "phi3", "llava"]
        for pref in preferred:
            for model in self.available_models:
                if pref in model.lower():
                    return model
                    
        # Return first available if no preference matched
        return self.available_models[0]
