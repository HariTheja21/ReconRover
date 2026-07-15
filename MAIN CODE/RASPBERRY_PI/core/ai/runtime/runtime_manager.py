import asyncio
from typing import Any
from .runtime_health import RuntimeHealth
from .runtime_statistics import RuntimeStatistics
from .runtime_bridge import RuntimeBridge
from .configuration_manager import ConfigurationManager
from .gpu_detector import GPUDetector
from .cpu_detector import CPUDetector
from .memory_detector import MemoryDetector
from .device_manager import DeviceManager
from .package_manager import PackageManager
from .dependency_manager import DependencyManager
from .provider_registry import ProviderRegistry
from .provider_loader import ProviderLoader
from .provider_manager import ProviderManager
from .model_cache import ModelCache
from .model_version_manager import ModelVersionManager
from .model_downloader import ModelDownloader
from .model_updater import ModelUpdater
from .model_installer import ModelInstaller
from .model_repository import ModelRepository
from .resource_monitor import ResourceMonitor
from .performance_monitor import PerformanceMonitor
from .benchmark_manager import BenchmarkManager
from .runtime_environment import RuntimeEnvironment
from .runtime_loader import RuntimeLoader
from .runtime_scheduler import RuntimeScheduler

class RuntimeManager:
    def __init__(self, event_bus: Any):
        self.health = RuntimeHealth()
        self.stats = RuntimeStatistics()
        self.bridge = RuntimeBridge(event_bus)
        self.config = ConfigurationManager()
        
        # Hardware
        self.device = DeviceManager(GPUDetector(), CPUDetector(), MemoryDetector())
        self.env = RuntimeEnvironment(self.device, self.config)
        
        # Dependencies & Providers
        self.deps = DependencyManager(PackageManager())
        self.prov_reg = ProviderRegistry()
        self.prov_loader = ProviderLoader(self.prov_reg, self.deps)
        self.prov_mgr = ProviderManager(self.prov_reg, self.prov_loader)
        
        # Models
        self.cache = ModelCache(self.config.get("cache_dir"))
        self.versions = ModelVersionManager()
        self.downloader = ModelDownloader()
        self.updater = ModelUpdater(self.downloader)
        self.installer = ModelInstaller(self.downloader, self.cache)
        self.repo = ModelRepository(self.installer, self.updater, self.versions, self.cache)
        
        # Core
        self.loader = RuntimeLoader(self.prov_mgr, self.repo)
        self.scheduler = RuntimeScheduler()
        
        # Monitoring
        self.res_mon = ResourceMonitor()
        self.perf_mon = PerformanceMonitor()
        self.bench_mgr = BenchmarkManager(self.bridge.publish_event)
        
    async def initialize(self):
        if not self.env.validate_environment():
            self.health.set_error("Insufficient environment resources")
            return False
            
        self.bridge.publish_event("RuntimeInitialized", {
            "device": self.device.get_system_profile()["cpu"]["arch"],
            "timestamp": asyncio.get_event_loop().time()
        })
        
        asyncio.create_task(self.scheduler.run_monitoring_loop())
        return True
