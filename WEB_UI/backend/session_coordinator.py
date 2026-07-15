import time
import asyncio
from typing import Callable, List
from .operator_manager import OperatorManager
from .collaboration_events import OperatorPresenceEvent

class SessionCoordinator:
    def __init__(self, operator_manager: OperatorManager, publish_callback: Callable):
        self.op_manager = operator_manager
        self.publish = publish_callback
        self.idle_timeout = 300 # seconds

    def sync_presence(self):
        current_time = time.time()
        for op in self.op_manager.get_all_operators():
            if current_time - op["last_active"] > self.idle_timeout and op["status"] == "ONLINE":
                op["status"] = "IDLE"
                self._broadcast_presence(op)

    def _broadcast_presence(self, op: dict):
        event = OperatorPresenceEvent(
            operator_id=op["operator_id"],
            username=op["username"],
            role=op["role"],
            status=op["status"],
            timestamp=time.time()
        )
        self.publish("OperatorPresenceEvent", event)

    def operator_connected(self, operator_id: str, username: str, role: str):
        self.op_manager.add_operator(operator_id, username, role)
        op = self.op_manager.get_operator(operator_id)
        self._broadcast_presence(op)

    def operator_disconnected(self, operator_id: str):
        op = self.op_manager.get_operator(operator_id)
        if op:
            op["status"] = "OFFLINE"
            self._broadcast_presence(op)
            self.op_manager.remove_operator(operator_id)
