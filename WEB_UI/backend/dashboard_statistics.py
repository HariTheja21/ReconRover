from dataclasses import dataclass

@dataclass
class DashboardStatistics:
    active_sessions: int = 0
    total_logins: int = 0
    failed_logins: int = 0
    api_requests: int = 0
    websocket_messages_sent: int = 0
    websocket_messages_received: int = 0
