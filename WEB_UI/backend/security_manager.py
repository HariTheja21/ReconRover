import time
from typing import Callable, Tuple, Optional
from .security_policy import SecurityPolicy
from .security_statistics import SecurityStatistics
from .security_health import SecurityHealth
from .token_manager import TokenManager
from .password_manager import PasswordManager
from .audit_manager import AuditManager
from .authentication_manager import AuthenticationManager
from .authorization_manager import AuthorizationManager
from .security_bridge import SecurityBridge
from .security_events import AuditEvent

class SecurityManager:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.stats = SecurityStatistics()
        self.health = SecurityHealth()
        
        self.policy = SecurityPolicy()
        self.audit = AuditManager()
        self.token_manager = TokenManager(self.policy)
        self.password_manager = PasswordManager()
        self.auth_manager = AuthenticationManager(self.policy, self.token_manager, self.password_manager, self.stats)
        self.authz_manager = AuthorizationManager(self.stats)
        self.bridge = SecurityBridge(publish_callback)

    def login(self, username: str, password_plaintext: str, ip_address: str) -> Tuple[bool, str, str]:
        success, msg, token = self.auth_manager.authenticate(username, password_plaintext, ip_address)
        
        # Log Audit Event
        event = AuditEvent(
            actor=username,
            action="LOGIN_ATTEMPT",
            target="GroundStation",
            details=f"IP: {ip_address}, Status: {'SUCCESS' if success else 'FAILED'}, Msg: {msg}",
            timestamp=time.time()
        )
        self.audit.log_event(event)
        
        if success:
            return True, "Login successful", token
        else:
            if "locked" in msg.lower():
                self.bridge.broadcast_security_alert(event)
            return False, msg, ""

    def validate_session(self, token: str) -> Tuple[bool, str, str]:
        payload = self.token_manager.validate_token(token)
        if not payload:
            return False, "", ""
        return True, payload["sub"], payload["role"]

    def authorize_action(self, token: str, action: str) -> bool:
        valid, username, role = self.validate_session(token)
        if not valid:
            return False
            
        success = self.authz_manager.check_permission(role, action)
        
        event = AuditEvent(
            actor=username,
            action="AUTHORIZATION_CHECK",
            target=action,
            details=f"Status: {'GRANTED' if success else 'DENIED'}",
            timestamp=time.time()
        )
        self.audit.log_event(event)
        
        return success
