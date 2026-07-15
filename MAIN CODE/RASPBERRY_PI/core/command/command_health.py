"""
Command Health Module
Recon Rover V2 - Phase 2.5

Publishes health snapshots to the EventBus.
"""

from typing import Any
from .command_statistics import CommandStatistics
from .command_events import CommandStatisticsUpdated

class CommandHealth:
    """Periodically retrieves stats and queue depth, then publishes."""
    
    def __init__(self, event_bus: Any, stats: CommandStatistics, get_qsize: Any):
        self._bus = event_bus
        self._stats = stats
        self._get_qsize = get_qsize
        
    def broadcast(self):
        """Dispatches the current throughput metrics."""
        snapshot = self._stats.get_snapshot()
        
        event = CommandStatisticsUpdated(
            processed=snapshot["processed"],
            rejected=snapshot["rejected"],
            sent=snapshot["sent"],
            queue_depth=self._get_qsize()
        )
        self._bus.publish(event)
