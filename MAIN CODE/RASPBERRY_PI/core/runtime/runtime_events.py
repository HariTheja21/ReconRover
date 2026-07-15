"""
Runtime Events Module
Recon Rover V2 - Phase 3.0
"""

from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

# Inbound Requests
@dataclass
class SystemStartRequest(Event):
    pass

@dataclass
class SystemShutdownRequest(Event):
    reason: str = "User Requested"

@dataclass
class ModuleFailure(Event):
    module_name: str
    error_msg: str

@dataclass
class HeartbeatTimeout(Event):
    module_name: str

# Outbound State
@dataclass
class SystemStarted(Event):
    pass

@dataclass
class SystemStopped(Event):
    pass

@dataclass
class ModuleStarted(Event):
    module_name: str

@dataclass
class ModuleStopped(Event):
    module_name: str

@dataclass
class ModuleRestarted(Event):
    module_name: str

@dataclass
class RuntimeHealthy(Event):
    is_healthy: bool

@dataclass
class RuntimeFault(Event):
    faulting_modules: list
