import secrets

class Authentication:
    def __init__(self):
        # In a real system, this would be hashed and stored in a database
        self.mock_users = {
            "admin": "recon_rover_2026"
        }

    def authenticate(self, username: str, password: str) -> str:
        """
        Returns a session token if authenticated, else empty string.
        """
        if username in self.mock_users and self.mock_users[username] == password:
            return secrets.token_hex(16)
        return ""
