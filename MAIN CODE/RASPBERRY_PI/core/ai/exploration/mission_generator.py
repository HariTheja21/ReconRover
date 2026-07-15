import time

class MissionGenerator:
    def __init__(self):
        pass
        
    def create_mission(self, target_x: float, target_y: float) -> tuple[str, int]:
        # Generates a mission ID and priority
        mission_id = f"EXPLORE_{int(time.time())}"
        priority = 2
        return mission_id, priority
