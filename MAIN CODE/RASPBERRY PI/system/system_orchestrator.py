"""
system_orchestrator.py
Recon Rover V1 - System Orchestrator

Master controller of the system lifecycle, holding all infrastructure components.
"""

from logger import Logger
from event_bus import EventBus
from .dependency_container import DependencyContainer
from .module_loader import ModuleLoader
from .system_health import SystemHealth
from .system_statistics import SystemStatistics
from .boot_sequence import BootSequence
from .shutdown_sequence import ShutdownSequence
from .startup_validator import StartupValidator
from .runtime_monitor import RuntimeMonitor

# Import modules to load
from scheduler import Scheduler
from serial.serial_manager import SerialManager
from telemetry.telemetry_manager import TelemetryManager
from communication.command_dispatcher import CommandDispatcher
from health_monitor import HealthMonitor
from diagnostics import Diagnostics
from sensor_fusion import SensorFusion
from world_model import WorldModel
from navigation import NavigationEngine
from command_builder import CommandBuilder
from ai.ai_engine import AIEngine
from vision.vision_pipeline import VisionPipeline
from audio.audio_pipeline import AudioPipeline
from mission.mission_manager import MissionManager
from mission.behavior_engine import BehaviorEngine
import asyncio
from config import Config

class SystemOrchestrator:
    def __init__(self):
        self.log = Logger.get("SystemOrchestrator")
        
        # 1. Initialize core infrastructure
        self.event_bus = EventBus()
        self.container = DependencyContainer()
        self.health = SystemHealth()
        self.stats = SystemStatistics()
        
        # 2. Setup sequences and supervision
        self.boot_seq = BootSequence(self.event_bus, self.stats)
        self.shutdown_seq = ShutdownSequence(self.event_bus, self.stats)
        self.validator = StartupValidator(self.event_bus)
        self.monitor = RuntimeMonitor(self.event_bus, self.health, self.stats)
        self.loader = ModuleLoader(self.container)

    def _register_dependencies(self):
        self.container.provide("EventBus", self.event_bus)
        self.container.provide("asyncio.loop", asyncio.get_running_loop())

    def _load_modules(self):
        """Loads modules in dependency order."""
        # Note: EventBus is passed explicitly to satisfy legacy initializations, 
        # though the container could resolve it.
        eb = self.event_bus
        loop = asyncio.get_running_loop()
        
        self.loader.load("Scheduler", Scheduler)
        self.loader.load("SerialManager", SerialManager, eb, loop)
        self.loader.load("TelemetryManager", TelemetryManager, eb)
        self.loader.load("CommandDispatcher", CommandDispatcher, eb)
        
        # The old health monitor and diagnostics (Phase 1 legacy)
        hm = self.loader.load("HealthMonitor", HealthMonitor, eb)
        diag = self.loader.load("Diagnostics", Diagnostics, eb)
        
        # High level pipelines
        self.loader.load("SensorFusion", SensorFusion, eb)
        self.loader.load("WorldModel", WorldModel, eb)
        self.loader.load("NavigationEngine", NavigationEngine, eb)
        self.loader.load("CommandBuilder", CommandBuilder, eb)
        self.loader.load("AIEngine", AIEngine, eb)
        self.loader.load("VisionPipeline", VisionPipeline, eb)
        self.loader.load("AudioPipeline", AudioPipeline, eb)
        self.loader.load("MissionManager", MissionManager, eb)
        self.loader.load("BehaviorEngine", BehaviorEngine, eb)
        
        # Schedule periodic legacy checks
        sched = self.container.resolve("Scheduler")
        if sched:
            sched.schedule_periodic(Config.HEALTH_HZ, hm.check_modules)
            sched.schedule_periodic(Config.DIAGNOSTICS_HZ, diag.gather_metrics)

    async def boot(self) -> bool:
        """Starts the entire application."""
        self._register_dependencies()
        await self.event_bus.start()
        
        self._load_modules()
        
        await self.boot_seq.execute()
        
        if self.validator.validate():
            self.monitor.start()
            return True
            
        return False

    async def shutdown(self):
        """Tears down the application."""
        self.monitor.stop()
        await self.shutdown_seq.execute()
        await self.event_bus.stop()
