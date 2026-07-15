import uuid

class SessionManager:
    def __init__(self):
        self.active_session = str(uuid.uuid4())
        
    def new_session(self):
        self.active_session = str(uuid.uuid4())
        return self.active_session
        
    def get_session(self) -> str:
        return self.active_session
