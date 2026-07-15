import asyncio
from .calibration_engine import CalibrationEngine

class CalibrationManager:
    def __init__(self, publish_callback):
        self.publish = publish_callback
        self.engine = CalibrationEngine(publish_callback)

    async def run_calibration(self) -> bool:
        """
        Entry point to run the hardware calibration sequence.
        """
        return await self.engine.execute_calibration()
