class SessionManager:
    def __init__(self):
        self.sessions = {}
        
    def create_session(self, session_id: str):
        self.sessions[session_id] = []
        
    def append_context(self, session_id: str, message: dict):
        if session_id in self.sessions:
            self.sessions[session_id].append(message)
            
    def get_context(self, session_id: str):
        return self.sessions.get(session_id, [])
