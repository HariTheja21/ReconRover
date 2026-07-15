from dataclasses import dataclass

@dataclass
class ToolStatistics:
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    avg_latency_ms: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.total_executions == 0:
            return 100.0
        return (self.successful_executions / self.total_executions) * 100.0
