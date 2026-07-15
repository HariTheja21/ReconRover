from typing import Callable, Dict, Any, Tuple, Optional, List
from .mission_engine import MissionEngine

class MissionManager:
    """
    Main entry point for the Ground Station Backend for handling Mission Planning.
    Integrates with FastAPI routes and WebSocket bridges.
    """
    def __init__(self, publish_callback: Callable):
        self.engine = MissionEngine(publish_callback)

    def handle_save_mission(self, mission_data: Dict[str, Any]) -> Tuple[bool, str, str]:
        return self.engine.save_mission(mission_data)

    def handle_load_mission(self, mission_id: str) -> Optional[Dict[str, Any]]:
        return self.engine.load_mission(mission_id)
        
    def handle_list_missions(self) -> List[dict]:
        return self.engine.list_missions()
        
    def handle_delete_mission(self, mission_id: str) -> bool:
        return self.engine.delete_mission(mission_id)

    async def handle_execute_mission(self, mission_id: str) -> bool:
        return await self.engine.execute_mission(mission_id)

    def handle_cancel_mission(self) -> bool:
        return self.engine.cancel_mission()
