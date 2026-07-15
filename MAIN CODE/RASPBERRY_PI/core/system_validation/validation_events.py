from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ValidationStartedEvent:
    timestamp: float

@dataclass
class TestStartedEvent:
    test_name: str
    timestamp: float

@dataclass
class TestCompletedEvent:
    test_name: str
    passed: bool
    metrics: Dict[str, Any]

@dataclass
class ValidationFailedEvent:
    test_name: str
    reason: str

@dataclass
class ValidationCompletedEvent:
    total_time_ms: int
    statistics: Dict[str, Any]
