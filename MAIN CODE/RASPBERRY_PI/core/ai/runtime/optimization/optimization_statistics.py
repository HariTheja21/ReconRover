from dataclasses import dataclass

@dataclass
class OptimizationStatistics:
    total_optimizations: int = 0
    memory_saved_mb: float = 0.0
    avg_latency_reduction_ms: float = 0.0
    active_batch_jobs: int = 0
    thermal_throttles_triggered: int = 0
