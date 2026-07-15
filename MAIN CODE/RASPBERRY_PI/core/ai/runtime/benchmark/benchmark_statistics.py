from dataclasses import dataclass

@dataclass
class BenchmarkStatistics:
    total_benchmarks_run: int = 0
    total_reports_generated: int = 0
    metrics_collected: int = 0
    avg_profiling_overhead_ms: float = 0.0
