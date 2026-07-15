class CalibrationHealth:
    def __init__(self):
        self.is_calibrated: bool = False
        self.critical_failure: bool = False
        self.failure_reason: str = ""

    def mark_calibrated(self) -> None:
        self.is_calibrated = True
        self.critical_failure = False

    def mark_failure(self, reason: str) -> None:
        self.is_calibrated = False
        self.critical_failure = True
        self.failure_reason = reason
