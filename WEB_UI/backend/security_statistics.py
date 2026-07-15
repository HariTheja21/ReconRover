from dataclasses import dataclass

@dataclass
class SecurityStatistics:
    total_logins_successful: int = 0
    total_logins_failed: int = 0
    total_accounts_locked: int = 0
    total_authorizations_granted: int = 0
    total_authorizations_denied: int = 0
    total_audit_events: int = 0
