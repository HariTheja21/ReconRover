from dataclasses import dataclass

@dataclass
class LLMStatistics:
    total_requests: int = 0
    total_tokens: int = 0
    failovers: int = 0
    avg_latency_ms: float = 0.0
