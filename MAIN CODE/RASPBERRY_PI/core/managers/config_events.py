"""
Config Events Module
Recon Rover V2 - Phase 2.3

Defines events for runtime configuration management.
"""

from dataclasses import dataclass
from typing import Dict, Any

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class ConfigurationRequest(Event):
    """
    Request to fetch the current runtime configuration.
    """
    source_module: str

@dataclass
class ConfigurationUpdate(Event):
    """
    Request to update one or more configuration keys.
    """
    updates: Dict[str, Any]

@dataclass
class ConfigurationUpdated(Event):
    """
    Published when configuration has been successfully updated and validated.
    """
    current_config: Dict[str, Any]
    changed_keys: list
