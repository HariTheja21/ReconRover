"""
llm_health.py
Recon Rover V1 - Local LLM Decision Engine

Tracks the health of the LLM inference pipeline.
"""

class LLMHealth:
    def __init__(self):
        self.status = "OK"
        self.timeout_errors = 0
        self.parse_errors = 0
        self.general_errors = 0
        
    def record_timeout(self):
        self.timeout_errors += 1
        self._evaluate()
        
    def record_parse_error(self):
        self.parse_errors += 1
        self._evaluate()
        
    def record_general_error(self):
        self.general_errors += 1
        self._evaluate()
        
    def record_success(self):
        self.timeout_errors = max(0, self.timeout_errors - 1)
        self.parse_errors = max(0, self.parse_errors - 1)
        self.general_errors = 0
        self._evaluate()
        
    def _evaluate(self):
        if self.timeout_errors > 3 or self.general_errors > 3:
            self.status = "DEGRADED"
        elif self.timeout_errors == 0 and self.general_errors == 0:
            self.status = "OK"
            
    def get_diagnostics(self) -> dict:
        return {
            "status": self.status,
            "timeouts": self.timeout_errors,
            "parse_errors": self.parse_errors
        }
