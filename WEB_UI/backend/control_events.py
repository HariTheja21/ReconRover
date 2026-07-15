from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class OperatorCommandEvent:
    client_id: str
    command: str
    payload: Dict[str, Any]
    timestamp: float

@dataclass
class EmergencyStopEvent:
    source: str
    reason: str
    timestamp: float
