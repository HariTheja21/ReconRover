import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

class SpeechScheduler:
    def __init__(self, engine: Any):
        self.engine = engine
        self.audio_queue = asyncio.Queue(maxsize=50) # audio chunks
        self.tts_queue = asyncio.Queue(maxsize=10)   # text to speak
        
    async def enqueue_audio(self, chunk: bytes):
        try:
            self.audio_queue.put_nowait(chunk)
        except asyncio.QueueFull:
            pass # Drop audio if overwhelmed
            
    async def enqueue_tts(self, text: str, voice: str):
        try:
            self.tts_queue.put_nowait((text, voice))
        except asyncio.QueueFull:
            pass
            
    async def run_audio_loop(self):
        logger.info("Starting Speech Audio Loop")
        while True:
            try:
                chunk = await self.audio_queue.get()
                await self.engine.process_audio_chunk(chunk)
                self.audio_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Speech Audio Loop: {e}")
                
    async def run_tts_loop(self):
        logger.info("Starting Speech TTS Loop")
        while True:
            try:
                text, voice = await self.tts_queue.get()
                await self.engine.process_tts_request(text, voice)
                self.tts_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in Speech TTS Loop: {e}")
