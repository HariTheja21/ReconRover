class RecoveryManager:
    def __init__(self):
        self.in_recovery = False
        
    def plan_recovery(self, robot_pose: tuple) -> tuple[str, float, float]:
        # Stub: Plan a safe backing up or spinning maneuver to escape deadlock
        self.in_recovery = True
        rx, ry = robot_pose
        # backup 1 meter
        return "reverse_clearance", rx - 1.0, ry - 1.0
        
    def clear_recovery(self):
        self.in_recovery = False
