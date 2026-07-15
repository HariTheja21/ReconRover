import time
import json
import base64
from typing import Dict, Any, Optional
from .security_policy import SecurityPolicy

class TokenManager:
    def __init__(self, policy: SecurityPolicy):
        self.policy = policy

    def generate_token(self, username: str, role: str) -> str:
        # MOCK JWT Implementation
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": username,
            "role": role,
            "iat": time.time(),
            "exp": time.time() + self.policy.session_timeout_seconds
        }
        
        # In prod: use PyJWT
        b_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        b_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        signature = "mock_signature" # Would be HMAC-SHA256
        
        return f"{b_header}.{b_payload}.{signature}"

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        # MOCK JWT validation
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            # Padding might be missing
            b_payload = parts[1]
            b_payload += "=" * ((4 - len(b_payload) % 4) % 4)
            payload_str = base64.urlsafe_b64decode(b_payload).decode()
            payload = json.loads(payload_str)
            
            if time.time() > payload.get("exp", 0):
                return None # Expired
                
            return payload
        except Exception:
            return None
