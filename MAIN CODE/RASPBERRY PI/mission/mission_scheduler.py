"""
mission_scheduler.py
Recon Rover V1 - Mission Manager

Deterministic priority-based mission scheduler.
"""

from typing import Optional
from logger import Logger
from .mission_registry import MissionRegistry
from .mission_context import MissionContext, MissionStore
from .mission_state import MissionLifecycle
import time
import uuid

class MissionScheduler:
    def __init__(self, registry: MissionRegistry, store: MissionStore):
        self.registry = registry
        self.store = store
        self.log = Logger.get("MissionScheduler")

    def evaluate_request(self, mission_type: str, owner: str) -> Optional[MissionContext]:
        """
        Evaluates a new mission request against the currently active mission.
        Returns a new MissionContext if it wins priority, else None.
        """
        new_def = self.registry.get_definition(mission_type)
        if not new_def:
            return None
            
        # If no active mission, this wins
        if not self.store.active_mission or self.store.active_mission.is_terminal:
            return self._create_context(new_def, owner)
            
        # Compare priorities (lower number = higher priority)
        current_priority = self.store.active_mission.priority
        new_priority = new_def.priority
        
        if new_priority < current_priority:
            self.log.info(f"Priority override: '{mission_type}' ({new_priority}) preempts '{self.store.active_mission.mission_type}' ({current_priority})")
            return self._create_context(new_def, owner)
        else:
            self.log.info(f"Priority rejected: '{mission_type}' ({new_priority}) is lower/equal to '{self.store.active_mission.mission_type}' ({current_priority})")
            return None

    def _create_context(self, definition, owner: str) -> MissionContext:
        return MissionContext(
            mission_id=str(uuid.uuid4()),
            mission_type=definition.mission_type,
            owner=owner,
            priority=definition.priority,
            state=MissionLifecycle.CREATED,
            start_time_ms=0, # Set by executor
            timeout_ms=definition.default_timeout_ms
        )
