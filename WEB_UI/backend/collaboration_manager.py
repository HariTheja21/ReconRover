import time
from typing import Callable, Tuple
from .role_manager import RoleManager
from .permission_manager import PermissionManager
from .operator_manager import OperatorManager
from .ownership_manager import OwnershipManager
from .session_coordinator import SessionCoordinator
from .collaboration_bridge import CollaborationBridge
from .collaboration_events import ActivityFeedEvent
from .collaboration_statistics import CollaborationStatistics
from .collaboration_health import CollaborationHealth

class CollaborationManager:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.stats = CollaborationStatistics()
        self.health = CollaborationHealth()
        
        self.role_manager = RoleManager()
        self.perm_manager = PermissionManager(self.role_manager, self.stats)
        self.op_manager = OperatorManager()
        
        self.bridge = CollaborationBridge(publish_callback)
        self.ownership_manager = OwnershipManager(self.op_manager, self.perm_manager, publish_callback)
        self.session_coordinator = SessionCoordinator(self.op_manager, publish_callback)

    def handle_operator_connect(self, operator_id: str, username: str, role: str):
        self.session_coordinator.operator_connected(operator_id, username, role)
        self.stats.total_operators_connected += 1
        self._log_activity(operator_id, username, "Connected", f"Joined as {role}")

    def handle_operator_disconnect(self, operator_id: str):
        op = self.op_manager.get_operator(operator_id)
        if op:
            self.ownership_manager.release_all_for_operator(operator_id)
            self._log_activity(operator_id, op["username"], "Disconnected", "Left session")
            self.session_coordinator.operator_disconnected(operator_id)

    def handle_activity(self, operator_id: str, action: str, details: str):
        op = self.op_manager.get_operator(operator_id)
        if op:
            self.op_manager.update_activity(operator_id)
            self._log_activity(operator_id, op["username"], action, details)

    def request_ownership(self, operator_id: str, resource: str) -> Tuple[bool, str]:
        self.op_manager.update_activity(operator_id)
        success, msg = self.ownership_manager.request_ownership(operator_id, resource)
        if success:
            self.stats.total_ownership_transfers += 1
            op = self.op_manager.get_operator(operator_id)
            self._log_activity(operator_id, op["username"], "Ownership Acquired", f"Took control of {resource}")
        return success, msg

    def _log_activity(self, operator_id: str, username: str, action: str, details: str):
        self.stats.total_activity_events += 1
        event = ActivityFeedEvent(
            operator_id=operator_id,
            username=username,
            action=action,
            details=details,
            timestamp=time.time()
        )
        self.bridge.broadcast_activity(event)
