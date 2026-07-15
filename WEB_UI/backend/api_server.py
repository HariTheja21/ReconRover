# Simulated FastAPI router structure for the sake of architecture
class ApiServer:
    def __init__(self, session_manager, authentication):
        self.session_manager = session_manager
        self.auth = authentication
        self.system_status = {"status": "offline"}

    def handle_login(self, request: dict) -> dict:
        username = request.get("username", "")
        password = request.get("password", "")
        token = self.auth.authenticate(username, password)
        if token:
            self.session_manager.create_session(token, username)
            return {"success": True, "token": token}
        return {"success": False, "error": "Invalid credentials"}

    def get_status(self, token: str) -> dict:
        if not self.session_manager.validate_session(token):
            return {"error": "Unauthorized"}
        return self.system_status

    def get_system(self, token: str) -> dict:
        if not self.session_manager.validate_session(token):
            return {"error": "Unauthorized"}
        return {"cpu": 45, "ram": 25, "temp": 50.5}
        
    def get_config(self, token: str) -> dict:
        if not self.session_manager.validate_session(token):
            return {"error": "Unauthorized"}
        return {"version": "2.0.0", "mode": "rover"}
