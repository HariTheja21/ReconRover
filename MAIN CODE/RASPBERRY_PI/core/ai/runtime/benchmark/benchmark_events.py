from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BenchmarkCompleted:
    benchmark_id: str
    results: Dict[str, Any]
    timestamp: float

@dataclass
class PerformanceReportGenerated:
    report_id: str
    summary: Dict[str, Any]
    timestamp: float

@dataclass
class LatencyStatisticsUpdated:
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    timestamp: float

@dataclass
class ThroughputStatisticsUpdated:
    avg_tps: float
    peak_tps: float
    timestamp: float

@dataclass
class BenchmarkHealthUpdated:
    is_healthy: bool
    active_profilers: int
    timestamp: float
