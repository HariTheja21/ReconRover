import asyncio
from .validation_engine import ValidationEngine

class ValidationManager:
    def __init__(self, publish_callback):
        self.publish = publish_callback
        self.engine = ValidationEngine(publish_callback)

    async def run_validation(self) -> bool:
        """
        Entry point to run the closed-loop system validation.
        """
        return await self.engine.execute_validation()
