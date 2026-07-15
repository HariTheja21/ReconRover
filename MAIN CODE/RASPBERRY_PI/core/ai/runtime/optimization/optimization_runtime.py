from typing import Any
import asyncio

from .optimization_events import OptimizationApplied
from .optimization_bridge import OptimizationBridge
from .optimization_health import OptimizationHealth
from .optimization_statistics import OptimizationStatistics

from .inference_optimizer import InferenceOptimizer
from .model_optimizer import ModelOptimizer
from .memory_optimizer import MemoryOptimizer
from .cache_optimizer import CacheOptimizer
from .batch_scheduler import BatchScheduler
from .thread_pool_manager import ThreadPoolManager
from .device_allocator import DeviceAllocator
from .resource_allocator import ResourceAllocator
from .load_balancer import LoadBalancer
from .priority_scheduler import PriorityScheduler
from .thermal_manager import ThermalManager
from .power_manager import PowerManager
from .latency_monitor import LatencyMonitor
from .throughput_monitor import ThroughputMonitor

from .optimization_manager import OptimizationManager
from .optimization_scheduler import OptimizationScheduler

class OptimizationRuntime:
    def __init__(self, event_bus: Any):
        self.bridge = OptimizationBridge(event_bus)
        self.health = OptimizationHealth()
        self.stats = OptimizationStatistics()
        
        self.inference_optimizer = InferenceOptimizer()
        self.model_optimizer = ModelOptimizer()
        self.memory_optimizer = MemoryOptimizer()
        self.cache_optimizer = CacheOptimizer()
        
        self.batch_scheduler = BatchScheduler()
        self.thread_pool = ThreadPoolManager()
        self.device_allocator = DeviceAllocator()
        self.resource_allocator = ResourceAllocator(self.device_allocator)
        
        self.load_balancer = LoadBalancer()
        self.priority_scheduler = PriorityScheduler()
        
        self.thermal_manager = ThermalManager(self.bridge.publish_event, self.health)
        self.power_manager = PowerManager()
        
        self.latency_monitor = LatencyMonitor(self.bridge.publish_event)
        self.throughput_monitor = ThroughputMonitor(self.bridge.publish_event)
        
        self.manager = OptimizationManager(
            self.inference_optimizer, 
            self.model_optimizer, 
            self.memory_optimizer, 
            self.cache_optimizer
        )
        self.scheduler = OptimizationScheduler(self.manager)
        
    async def initialize(self):
        return True
