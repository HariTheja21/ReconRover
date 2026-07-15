from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BootStartedEvent:
    timestamp: float

@dataclass
class SubsystemStartedEvent:
    name: str
    startup_time_ms: int

@dataclass
class SubsystemFailedEvent:
    name: str
    reason: str

@dataclass
class HardwareDiscoveredEvent:
    device_type: str
    port: str
    status: str

@dataclass
class BootCompletedEvent:
    total_time_ms: int
    diagnostics: Dict[str, Any]

@dataclass
class BootFailedEvent:
    reason: str
    failed_subsystem: str
