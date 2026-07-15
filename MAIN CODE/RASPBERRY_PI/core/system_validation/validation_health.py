class ValidationHealth:
    def __init__(self):
        self.is_validated: bool = False
        self.critical_failure: bool = False
        self.failure_reason: str = ""

    def mark_validated(self) -> None:
        self.is_validated = True
        self.critical_failure = False

    def mark_failure(self, reason: str) -> None:
        self.is_validated = False
        self.critical_failure = True
        self.failure_reason = reason
