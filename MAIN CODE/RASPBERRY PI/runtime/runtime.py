"""
runtime.py
Recon Rover V1 - Full System Integration

The main entry point for the Recon Rover V1.
Instantiates all modules and blocks on the main event loop.
"""

import asyncio
import logging
import signal
import sys

from event_bus import EventBus
from hardware.esp32_interface import ESP32Interface
from decision.decision_engine import DecisionEngine
from execution.execution_engine import ExecutionEngine
from llm.llm_engine import LLMEngine
from runtime.runtime_manager import RuntimeManager
from runtime.lifecycle_manager import BaseModule

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# A mock for unbuilt modules to satisfy the dependency graph for Phase 6
class MockModule(BaseModule):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._health_status = "OK"
    async def initialize(self):
        self.log.info(f"Mock {self.name} initialized.")
    async def start(self):
        self.log.info(f"Mock {self.name} started.")
    async def stop(self):
        self.log.info(f"Mock {self.name} stopped.")

class MainRuntime:
    def __init__(self):
        self.log = logging.getLogger("MAIN")
        self.event_bus = EventBus()
        self.modules = {}
        self.manager = None
        self._shutdown_event = asyncio.Event()

    def _build_registry(self):
        """Instantiates all required modules."""
        
        # 1. Core
        self.modules["EventBus"] = MockModule("EventBus") # The bus is native, mock the lifecycle
        
        # 2. Hardware
        self.modules["HardwareInterface"] = ESP32Interface(self.event_bus)
        
        # 3. Perception / Mapping (Mocked for V1)
        self.modules["SensorFusion"] = MockModule("SensorFusion")
        self.modules["WorldModel"] = MockModule("WorldModel")
        self.modules["NavigationEngine"] = MockModule("NavigationEngine")
        self.modules["VisionLanguage"] = MockModule("VisionLanguage")
        self.modules["AudioLanguage"] = MockModule("AudioLanguage")
        self.modules["MemoryEngine"] = MockModule("MemoryEngine")
        self.modules["MultimodalContext"] = MockModule("MultimodalContext")
        
        # 4. Cognition
        self.modules["LocalLLM"] = LLMEngine(self.event_bus)
        
        # 5. Execution
        self.modules["DecisionEngine"] = DecisionEngine(self.event_bus)
        self.modules["ExecutionEngine"] = ExecutionEngine(self.event_bus)
        
        # 6. UI
        self.modules["Dashboard"] = MockModule("Dashboard")
        
        self.manager = RuntimeManager(self.modules, self.event_bus)

    def _setup_signals(self):
        """Catches Ctrl+C (SIGINT) to trigger graceful shutdown."""
        loop = asyncio.get_event_loop()
        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, self._shutdown_event.set)
        except NotImplementedError:
            # Windows fallback
            signal.signal(signal.SIGINT, lambda *args: self._shutdown_event.set())
            signal.signal(signal.SIGTERM, lambda *args: self._shutdown_event.set())

    async def run_forever(self):
        self.log.info("=== RECON ROVER V1 RUNTIME STARTING ===")
        self._build_registry()
        self._setup_signals()
        
        success = await self.manager.boot_system()
        if not success:
            sys.exit(1)
            
        self.log.info("System running. Press Ctrl+C to halt.")
        
        # Block until a shutdown signal is received
        await self._shutdown_event.wait()
        
        self.log.info("Shutdown signal received.")
        await self.manager.halt_system()
        self.log.info("=== RECON ROVER V1 RUNTIME TERMINATED ===")

if __name__ == "__main__":
    runtime = MainRuntime()
    try:
        asyncio.run(runtime.run_forever())
    except KeyboardInterrupt:
        pass # Handled by signal
