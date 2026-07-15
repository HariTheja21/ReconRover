import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class LLMScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        self.prompt_queue = asyncio.Queue()
        
    async def enqueue_prompt(self, text: str):
        await self.prompt_queue.put(text)
        
    async def run_llm_loop(self):
        logger.info("Starting LLM Processing Loop")
        while True:
            try:
                text = await self.prompt_queue.get()
                await self.engine.process_prompt(text)
                self.prompt_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in LLM Loop: {e}")
                await asyncio.sleep(1.0)
