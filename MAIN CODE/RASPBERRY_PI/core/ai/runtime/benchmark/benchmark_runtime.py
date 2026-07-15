from typing import Any
import asyncio

from .benchmark_events import BenchmarkCompleted, PerformanceReportGenerated
from .benchmark_bridge import BenchmarkBridge
from .benchmark_health import BenchmarkHealth
from .benchmark_statistics import BenchmarkStatistics

from .latency_profiler import LatencyProfiler
from .throughput_profiler import ThroughputProfiler
from .memory_profiler import MemoryProfiler
from .cpu_profiler import CpuProfiler
from .gpu_profiler import GpuProfiler
from .network_profiler import NetworkProfiler
from .eventbus_profiler import EventbusProfiler
from .tool_profiler import ToolProfiler
from .agent_profiler import AgentProfiler
from .vision_profiler import VisionProfiler
from .speech_profiler import SpeechProfiler
from .llm_profiler import LlmProfiler
from .rag_profiler import RagProfiler

from .metrics_database import MetricsDatabase
from .metrics_store import MetricsStore
from .metrics_exporter import MetricsExporter
from .report_generator import ReportGenerator
from .performance_dashboard import PerformanceDashboard

from .benchmark_manager import BenchmarkManager
from .benchmark_scheduler import BenchmarkScheduler

class BenchmarkRuntime:
    def __init__(self, event_bus: Any):
        self.bridge = BenchmarkBridge(event_bus)
        self.health = BenchmarkHealth()
        self.stats = BenchmarkStatistics()
        
        self.profilers = [
            LatencyProfiler(), ThroughputProfiler(), MemoryProfiler(),
            CpuProfiler(), GpuProfiler(), NetworkProfiler(),
            EventbusProfiler(), ToolProfiler(), AgentProfiler(),
            VisionProfiler(), SpeechProfiler(), LlmProfiler(), RagProfiler()
        ]
        
        self.db = MetricsDatabase()
        self.store = MetricsStore(self.db)
        self.exporter = MetricsExporter(self.db)
        self.report_generator = ReportGenerator(self.db)
        self.dashboard = PerformanceDashboard(self.db)
        
        self.manager = BenchmarkManager(self.profilers, self.store, self.report_generator)
        self.scheduler = BenchmarkScheduler(self.manager)
        
    async def initialize(self):
        return True
