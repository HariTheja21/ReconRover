import asyncio
from typing import Callable

from .dashboard_events import LoginAttemptEvent
from .dashboard_health import DashboardHealth
from .dashboard_statistics import DashboardStatistics
from .session_manager import SessionManager
from .authentication import Authentication
from .websocket_manager import WebsocketManager
from .telemetry_bridge import TelemetryBridge
from .api_server import ApiServer

class DashboardEngine:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.health = DashboardHealth()
        self.stats = DashboardStatistics()
        
        self.auth = Authentication()
        self.session_manager = SessionManager()
        self.ws_manager = WebsocketManager(publish_callback)
        self.telemetry_bridge = TelemetryBridge(self.ws_manager)
        self.api_server = ApiServer(self.session_manager, self.auth)

    async def start(self):
        # In a real FastAPI app, this engine wraps the uvicorn execution
        self.health.mark_healthy()
        self.api_server.system_status = {"status": "online"}
        
    async def process_login(self, request: dict, ip_address: str):
        self.stats.api_requests += 1
        username = request.get("username", "")
        res = self.api_server.handle_login(request)
        
        success = res.get("success", False)
        if success:
            self.stats.total_logins += 1
            self.stats.active_sessions += 1
        else:
            self.stats.failed_logins += 1
            
        self.publish("LoginAttemptEvent", LoginAttemptEvent(username, success, ip_address))
        return res
