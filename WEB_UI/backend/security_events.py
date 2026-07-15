from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AuthenticationEvent:
    username: str
    status: str # SUCCESS, FAILED, LOCKED
    ip_address: str
    timestamp: float

@dataclass
class AuthorizationEvent:
    username: str
    action: str
    resource: str
    status: str # GRANTED, DENIED
    timestamp: float

@dataclass
class AuditEvent:
    actor: str
    action: str
    target: str
    details: str
    timestamp: float
