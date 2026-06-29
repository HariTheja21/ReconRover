"""
app.py
Recon Rover V1 - System Orchestrator

Master application runner. Replaces the procedural logic in main.py.
"""

import asyncio
import signal
import sys
from logger import Logger
from .system_orchestrator import SystemOrchestrator

class App:
    def __init__(self):
        Logger.setup()
        self.log = Logger.get("App")
        self.orchestrator = SystemOrchestrator()
        self._shutdown_event = asyncio.Event()

    async def run(self):
        self.log.info("=== Recon Rover V1 OS Starting ===")
        
        # Setup graceful shutdown handlers
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self._signal_handler)

        try:
            success = await self.orchestrator.boot()
            if not success:
                self.log.critical("System failed to boot properly. Shutting down.")
                await self.orchestrator.shutdown()
                sys.exit(1)
                
            self.log.info("System is fully operational. Awaiting termination signal...")
            await self._shutdown_event.wait()
            
        except Exception as e:
            self.log.critical(f"Fatal application error: {e}")
        finally:
            await self.orchestrator.shutdown()
            self.log.info("=== Recon Rover V1 OS Stopped ===")

    def _signal_handler(self):
        self.log.info("Termination signal received. Triggering graceful shutdown.")
        self._shutdown_event.set()
