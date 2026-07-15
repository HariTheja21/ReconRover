import asyncio
import time
from typing import Callable, Optional
from .mission_storage import MissionStorage
from .mission_statistics import MissionStatistics
from .mission_events import MissionStatusEvent

class MissionScheduler:
    def __init__(self, storage: MissionStorage, stats: MissionStatistics, publish_callback: Callable):
        self.storage = storage
        self.stats = stats
        self.publish = publish_callback
        
        self.active_mission_id: Optional[str] = None
        self.active_task: Optional[asyncio.Task] = None

    async def execute_mission(self, mission_id: str) -> bool:
        if self.active_mission_id is not None:
            return False # Mission already running
            
        mission = self.storage.load_mission(mission_id)
        if not mission:
            return False
            
        self.active_mission_id = mission_id
        self.stats.total_missions_executed += 1
        
        # Publish START
        self.publish("MissionStatusEvent", MissionStatusEvent(
            mission_id=mission_id, status="RUNNING", progress=0.0, current_waypoint_index=0, timestamp=time.time()
        ))
        
        # In a real system, we bridge this down to the Navigation Engine.
        # The Navigation engine drives, and emits progress events which we bridge back up.
        
        return True

    def cancel_mission(self) -> bool:
        if self.active_mission_id:
            mission_id = self.active_mission_id
            self.active_mission_id = None
            self.publish("MissionStatusEvent", MissionStatusEvent(
                mission_id=mission_id, status="CANCELLED", progress=0.0, current_waypoint_index=0, timestamp=time.time()
            ))
            return True
        return False
