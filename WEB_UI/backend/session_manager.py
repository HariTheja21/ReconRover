import time
from typing import Dict, Optional

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.timeout_seconds = 3600

    def create_session(self, token: str, username: str) -> None:
        self.sessions[token] = {
            "username": username,
            "created_at": time.time(),
            "last_activity": time.time()
        }

    def validate_session(self, token: str) -> bool:
        session = self.sessions.get(token)
        if not session:
            return False
            
        if time.time() - session["last_activity"] > self.timeout_seconds:
            del self.sessions[token]
            return False
            
        session["last_activity"] = time.time()
        return True

    def invalidate_session(self, token: str) -> None:
        if token in self.sessions:
            del self.sessions[token]
