from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ClientConnectedEvent:
    client_id: str
    ip_address: str

@dataclass
class ClientDisconnectedEvent:
    client_id: str

@dataclass
class CommandReceivedEvent:
    client_id: str
    command: str
    payload: Dict[str, Any]

@dataclass
class LoginAttemptEvent:
    username: str
    success: bool
    ip_address: str
