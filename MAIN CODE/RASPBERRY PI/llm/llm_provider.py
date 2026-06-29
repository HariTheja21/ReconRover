"""
llm_provider.py
Recon Rover V1 - Local LLM Framework

Abstract interface for communicating with local or cloud inference engines.
"""

from abc import ABC, abstractmethod
from typing import Optional
import asyncio

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> Optional[str]:
        """
        Executes inference against the model asynchronously.
        Returns the raw string output or None if failure.
        """
        pass

class MockLLMProvider(LLMProvider):
    async def generate(self, prompt: str) -> Optional[str]:
        """
        A safe mock generator to verify the pipeline architecture without heavy GPUs.
        """
        await asyncio.sleep(0.5) # Simulate inference latency
        
        # We output a mocked, valid JSON response as requested by the system prompt.
        mock_response = '''
        [
            {"intent": "Patrol", "target": "corridor", "parameters": {}, "priority_score": 5},
            {"intent": "ScanArea", "target": "left", "parameters": {"angle": -45}, "priority_score": 3}
        ]
        '''
        return mock_response
