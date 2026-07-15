import time
from typing import Callable, Tuple, Dict, Any, List

from .mission_storage import MissionStorage
from .mission_validator import MissionValidator
from .mission_scheduler import MissionScheduler
from .mission_bridge import MissionBridge
from .mission_statistics import MissionStatistics
from .mission_health import MissionHealth
from .mission_events import MissionCreatedEvent

class MissionEngine:
    def __init__(self, publish_callback: Callable):
        self.stats = MissionStatistics()
        self.health = MissionHealth()
        self.storage = MissionStorage()
        self.validator = MissionValidator()
        self.bridge = MissionBridge(publish_callback)
        self.scheduler = MissionScheduler(self.storage, self.stats, publish_callback)

    def save_mission(self, mission_data: Dict[str, Any]) -> Tuple[bool, str, str]:
        """Returns (success, message, mission_id)"""
        is_valid, msg = self.validator.validate_mission(mission_data)
        if not is_valid:
            return False, msg, ""
            
        try:
            mission_id = self.storage.save_mission(mission_data)
            self.stats.total_missions_created += 1
            
            # Broadcast to EventBus that a new mission exists
            event = MissionCreatedEvent(mission_id, mission_data["name"], mission_data["waypoints"], time.time())
            self.bridge.route_to_eventbus("MissionCreatedEvent", event)
            
            return True, "Mission saved successfully", mission_id
        except Exception as e:
            self.health.set_storage_error(str(e))
            return False, f"Storage error: {str(e)}", ""

    def load_mission(self, mission_id: str) -> Optional[Dict[str, Any]]:
        return self.storage.load_mission(mission_id)
        
    def list_missions(self) -> List[dict]:
        return self.storage.list_missions()
        
    def delete_mission(self, mission_id: str) -> bool:
        return self.storage.delete_mission(mission_id)

    async def execute_mission(self, mission_id: str) -> bool:
        return await self.scheduler.execute_mission(mission_id)

    def cancel_mission(self) -> bool:
        return self.scheduler.cancel_mission()
