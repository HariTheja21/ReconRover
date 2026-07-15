class BootHealth:
    def __init__(self):
        self.is_booted: bool = False
        self.critical_failure: bool = False
        self.failure_reason: str = ""

    def mark_booted(self) -> None:
        self.is_booted = True
        self.critical_failure = False

    def mark_failure(self, reason: str) -> None:
        self.is_booted = False
        self.critical_failure = True
        self.failure_reason = reason
