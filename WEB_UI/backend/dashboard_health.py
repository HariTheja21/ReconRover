class DashboardHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.critical_failure: bool = False
        self.failure_reason: str = ""

    def mark_healthy(self) -> None:
        self.is_healthy = True
        self.critical_failure = False

    def mark_failure(self, reason: str) -> None:
        self.is_healthy = False
        self.critical_failure = True
        self.failure_reason = reason
