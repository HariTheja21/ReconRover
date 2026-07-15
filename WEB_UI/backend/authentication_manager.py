import time
from typing import Dict, Any, Tuple
from .password_manager import PasswordManager
from .token_manager import TokenManager
from .security_policy import SecurityPolicy
from .security_statistics import SecurityStatistics
from .security_events import AuthenticationEvent

class AuthenticationManager:
    def __init__(self, policy: SecurityPolicy, token_manager: TokenManager, password_manager: PasswordManager, stats: SecurityStatistics):
        self.policy = policy
        self.token_manager = token_manager
        self.password_manager = password_manager
        self.stats = stats
        
        # Mock user database
        self.users: Dict[str, Dict[str, Any]] = {
            "admin": {
                "password_hash": self.password_manager.hash_password("admin123"),
                "role": "Administrator",
                "failed_attempts": 0,
                "lockout_until": 0
            }
        }

    def authenticate(self, username: str, password_plaintext: str, ip_address: str) -> Tuple[bool, str, str]:
        user = self.users.get(username)
        current_time = time.time()
        
        if not user:
            self.stats.total_logins_failed += 1
            return False, "Invalid credentials", ""
            
        if user["lockout_until"] > current_time:
            self.stats.total_logins_failed += 1
            return False, "Account locked. Try again later.", ""
            
        if self.password_manager.verify_password(password_plaintext, user["password_hash"]):
            user["failed_attempts"] = 0
            self.stats.total_logins_successful += 1
            token = self.token_manager.generate_token(username, user["role"])
            return True, "Success", token
            
        # Failed attempt
        user["failed_attempts"] += 1
        self.stats.total_logins_failed += 1
        
        if user["failed_attempts"] >= self.policy.max_failed_attempts:
            user["lockout_until"] = current_time + self.policy.lockout_duration_seconds
            self.stats.total_accounts_locked += 1
            return False, "Account locked due to too many failed attempts", ""
            
        return False, "Invalid credentials", ""
