"""
Mapping Events Module
Recon Rover V2 - Phase 3.4
"""
from dataclasses import dataclass
from typing import Dict, Any, List

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

@dataclass
class MapUpdated(Event):
    timestamp: float
    map_size: int
    new_cells_added: int

@dataclass
class OccupancyGridUpdated(Event):
    timestamp: float
    occupied_cells: List[tuple] # List of (x, y) coordinates
    free_cells: List[tuple]

@dataclass
class MapStatisticsUpdated(Event):
    timestamp: float
    total_cells: int
    resolution_cm: float

@dataclass
class MappingHealthUpdated(Event):
    is_healthy: bool
    status_flags: Dict[str, bool]
