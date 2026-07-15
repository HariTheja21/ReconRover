from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class OperatorPresenceEvent:
    operator_id: str
    username: str
    role: str
    status: str # ONLINE, IDLE, OFFLINE
    timestamp: float

@dataclass
class OwnershipTransferEvent:
    resource: str # "DRIVE", "MISSION", "CAMERA"
    previous_owner: str
    new_owner: str
    timestamp: float

@dataclass
class ActivityFeedEvent:
    operator_id: str
    username: str
    action: str
    details: str
    timestamp: float
