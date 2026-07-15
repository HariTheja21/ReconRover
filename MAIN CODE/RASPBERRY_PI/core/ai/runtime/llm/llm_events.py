from dataclasses import dataclass

@dataclass
class LLMResponseReceived:
    text: str
    provider: str
    model: str
    latency_ms: float
    timestamp: float

@dataclass
class ProviderChanged:
    old_provider: str
    new_provider: str
    reason: str
    timestamp: float

@dataclass
class StreamingStarted:
    provider: str
    session_id: str
    timestamp: float

@dataclass
class StreamingCompleted:
    provider: str
    session_id: str
    total_tokens: int
    timestamp: float

@dataclass
class ProviderHealthUpdated:
    provider: str
    is_healthy: bool
    latency_ms: float
    timestamp: float

@dataclass
class LLMStatisticsUpdated:
    total_requests: int
    total_tokens: int
    failovers: int
    timestamp: float
