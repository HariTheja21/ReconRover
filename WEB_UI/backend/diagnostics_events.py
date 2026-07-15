from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class LogEvent:
    timestamp: float
    level: str # TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL
    source: str
    message: str

@dataclass
class HealthStatusEvent:
    category: str
    status: str # OK, WARNING, ERROR, OFFLINE
    message: str
    timestamp: float

@dataclass
class PerformanceMetricsEvent:
    cpu_usage: float
    memory_usage: float
    temperature: float
    network_rx: int
    network_tx: int
    timestamp: float
