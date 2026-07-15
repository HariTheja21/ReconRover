from typing import Callable
from .command_router import CommandRouter
from .control_statistics import ControlStatistics
from .control_health import ControlHealth

class ControlManager:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.stats = ControlStatistics()
        self.health = ControlHealth()
        self.router = CommandRouter(self.publish, self.stats)

    def process_incoming_command(self, client_id: str, command: str, payload: dict) -> bool:
        """
        Entry point for commands coming from the WebSocket bridge.
        """
        return self.router.handle_incoming_command(client_id, command, payload)

    def handle_client_disconnect(self, client_id: str):
        """
        Safety interlock: Handles client disconnection to prevent runaway.
        """
        self.router.handle_client_disconnect(client_id)
