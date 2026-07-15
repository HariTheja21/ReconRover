from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class OptimizationApplied:
    optimization_type: str
    target: str
    impact: Dict[str, Any]
    timestamp: float

@dataclass
class OptimizationStatisticsUpdated:
    total_optimizations: int
    memory_saved_mb: float
    avg_latency_reduction_ms: float
    timestamp: float

@dataclass
class OptimizationHealthUpdated:
    is_healthy: bool
    thermal_throttling: bool
    timestamp: float

@dataclass
class LatencyUpdated:
    subsystem: str
    latency_ms: float
    timestamp: float

@dataclass
class ThroughputUpdated:
    subsystem: str
    requests_per_second: float
    timestamp: float
