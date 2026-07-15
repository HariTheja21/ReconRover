from dataclasses import dataclass

@dataclass
class ValidationStatistics:
    tests_passed: int = 0
    tests_failed: int = 0
    total_latency_ms: int = 0
    average_latency_ms: int = 0
